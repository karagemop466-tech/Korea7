#!/usr/bin/env python3
"""Analyse the nine focus-site rasters and the reference candidate pool.

Outputs (all numbers are measured from the bytes on disk):
  docs/data/focus_analysis.json   machine-readable table + OLS projection
  docs/data/focus_analysis.md     human-readable table for the site

Labels used by this script:
  USER-REPORTED  score copied from the user's supplied site list (no receipt)
  MEASURED       geometry computed here from the pinned rasters
  PROJECTED      OLS extrapolation from the nine USER-REPORTED scores; not a score
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS_DATA = ROOT / "docs" / "data"
DOCS_DATA.mkdir(parents=True, exist_ok=True)

# User-supplied reported scores for the nine focus sites.  No organizer receipt.
SCORES = {
    "GEMSDOE24": 0.2477,
    "GEMSDOE25": 0.2600,
    "GEMSDOE27": 0.2449,
    "GEMSDOE28": 0.2710,
    "GEMSDOE30": 0.2600,
    "GEMSDOE31": 0.2708,
    "GEMSDOE32": 0.2778,
    "GEMSDOE33": 0.2632,
    "GEMSDOE36": 0.2750,
}
FOCUS_FILES = {
    "GEMSDOE24": "data/focus/GEMSDOE24.tif",
    "GEMSDOE25": "data/focus/GEMSDOE25.tif",
    "GEMSDOE27": "data/focus/GEMSDOE27.tif",
    "GEMSDOE28": "data/focus/GEMSDOE28.tif",
    "GEMSDOE30": "data/focus/GEMSDOE30.tif",
    "GEMSDOE31": "data/focus/GEMSDOE31.tif",
    "GEMSDOE32": "data/focus/GEMSDOE32.tif",
    "GEMSDOE33": "data/focus/GEMSDOE33.tif",
    "GEMSDOE36": "data/focus/GEMSDOE36.tif",
}
REFERENCE_FILES = {
    "offcat_geophys_edge_37654": "data/reference/offcat_geophys_edge_37654.tif",
    "geothermal_conduit_20000": "data/reference/geothermal_conduit_20000.tif",
    "geo_habitat_dti_40561": "data/reference/geo_habitat_dti_40561.tif",
    "offcat_corridor_prior_15000": "data/reference/offcat_corridor_prior_15000.tif",
    "kp1_far_conduit_32000": "data/reference/kp1_far_conduit_32000.tif",
    "HV31_40000": "data/reference/HV31.tif",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_grid():
    import sys
    sys.path.insert(0, str(ROOT / "vendor"))
    from gems57 import grid
    return grid.load_grid(DATA / "bridge")


def geometry(a: np.ndarray, fp: np.ndarray, cat: np.ndarray, dc: np.ndarray) -> dict:
    m = (a > 0) & fp
    n = int(m.sum())
    if n == 0:
        return {"dots": 0, "far_fraction": None, "near2_fraction": None,
                "median_distance_px": None, "on_catalogue": 0}
    d = dc[m]
    return {
        "dots": n,
        "far_fraction": float((d > 15).mean()),
        "near2_fraction": float((d <= 2).mean()),
        "median_distance_px": float(np.median(d)),
        "on_catalogue": int((a[cat] > 0).sum()),
    }


def fit_projection(rows: dict[str, dict]) -> dict:
    sites = list(SCORES)
    X = np.array([[np.log(rows[s]["dots"]), rows[s]["far_fraction"]] for s in sites])
    y = np.array([SCORES[s] for s in sites])
    A = np.column_stack([np.ones(len(sites)), X - X.mean(0)])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    loo = []
    for i in range(len(sites)):
        keep = np.arange(len(sites)) != i
        b, *_ = np.linalg.lstsq(A[keep], y[keep], rcond=None)
        loo.append(float(A[i] @ b))
    loo = np.array(loo)
    resid = y - loo
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    return {
        "model": "OLS of USER-REPORTED score on [log(dots), fraction of dots > 15 px from catalogue]",
        "coefficients": {"intercept": float(beta[0]), "log_dots": float(beta[1]),
                         "far_fraction": float(beta[2])},
        "n_observations": len(sites),
        "loo_rmse": rmse,
        "loo_interval_halfwidth": 1.96 * rmse,
        "fitted_B2": float(np.array([1.0, *(np.array([np.log(rows["GEMSDOE32"]["dots"]),
                                                        rows["GEMSDOE32"]["far_fraction"]]) - X.mean(0))]) @ beta),
        "caveats": [
            "PROJECTED, not a score and not a measurement.",
            "n = 9 associational fit to unverified USER-REPORTED scores.",
            "The model cannot see surface quality; a candidate on the wrong terrain scores lower.",
            "Fewer dots always increases the projection, so the model is an extrapolation at low dot counts.",
        ],
    }


def project(cand: dict, model: dict, rows: dict) -> dict:
    sites = list(SCORES)
    X = np.array([[np.log(rows[s]["dots"]), rows[s]["far_fraction"]] for s in sites])
    xmean = X.mean(0)
    xc = np.array([np.log(cand["dots"]), cand["far_fraction"]]) - xmean
    beta = model["coefficients"]
    pred = float(beta["intercept"] + beta["log_dots"] * xc[0] + beta["far_fraction"] * xc[1])
    # parameter bootstrap: resample the nine (raster, score) pairs
    y = np.array([SCORES[s] for s in sites])
    A = np.column_stack([np.ones(len(sites)), X - xmean])
    rng = np.random.default_rng(20261104)
    draws = []
    for _ in range(2000):
        pick = rng.integers(0, len(sites), len(sites))
        b, *_ = np.linalg.lstsq(A[pick], y[pick], rcond=None)
        draws.append(float(np.array([1.0, *xc]) @ b))
    draws = np.array(draws)
    return {
        "evidence_class": "PROJECTED — not a score, not a measurement",
        "projected_value": pred,
        "bootstrap_95_interval": [float(np.quantile(draws, 0.025)),
                                  float(np.quantile(draws, 0.975))],
        "loo_interval": [pred - model["loo_interval_halfwidth"],
                         pred + model["loo_interval_halfwidth"]],
        "delta_vs_B2_projection": pred - model["fitted_B2"],
        "candidate_position": {"log_dots": float(np.log(cand["dots"])),
                               "far_fraction": cand["far_fraction"]},
    }


def main() -> None:
    g = load_grid()
    fp, cat = g.footprint, g.catalogue
    dc = ndi.distance_transform_edt(~cat)
    rows: dict[str, dict] = {}
    for site, rel in FOCUS_FILES.items():
        p = ROOT / rel
        with rasterio.open(p) as src:
            a = src.read(1)
        rows[site] = geometry(a, fp, cat, dc)
        rows[site].update({
            "file": rel,
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
            "user_reported_score": SCORES[site],
            "score_evidence_class": "USER-REPORTED — no organizer receipt",
        })
    model = fit_projection(rows)
    refs: dict[str, dict] = {}
    for name, rel in REFERENCE_FILES.items():
        p = ROOT / rel
        with rasterio.open(p) as src:
            a = src.read(1)
        geo = geometry(a, fp, cat, dc)
        refs[name] = {"file": rel, "bytes": p.stat().st_size, "sha256": sha256(p),
                      **geo, "projection": project(geo, model, rows)}
    out = {
        "schema": "korea7-focus-analysis-v1",
        "date_utc": "2026-11-04",
        "grid": {"crs": "EPSG:32611", "height": g.height, "width": g.width,
                 "footprint_cells": int(fp.sum()), "catalogue_cells": int(cat.sum())},
        "evidence_labels": {
            "USER-REPORTED": "score copied from the user's supplied site list; no organizer receipt",
            "MEASURED": "geometry computed here from the pinned rasters",
            "PROJECTED": "OLS extrapolation from the nine USER-REPORTED scores; not a score",
        },
        "focus": rows,
        "projection_model": model,
        "reference_candidates": refs,
        "data_provenance": {
            "labels.tif": {"sha256": sha256(DATA / "labels.tif"),
                           "note": "byte-identical to existing_faults.tif; mirror catalogue, not organizer hidden labels"},
            "sample_submission.tif": {"sha256": sha256(DATA / "sample_submission.tif"),
                                      "note": "grid/footprint template; mirror, not organizer-authenticated"},
        },
    }
    (DOCS_DATA / "focus_analysis.json").write_text(json.dumps(out, indent=2) + "\n")
    lines = ["# Focus-site analysis (MEASURED geometry + PROJECTED score)", "",
             "All geometry is measured from the pinned rasters. Scores are USER-REPORTED (no receipt).",
             "The projection is an OLS extrapolation and is **not a score**.", "",
             "| Site | File | Dots | Far >15 px | Near <=2 px | Median px | USER-REPORTED |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for site in FOCUS_FILES:
        r = rows[site]
        lines.append(f"| {site} | `{Path(r['file']).name}` | {r['dots']} | "
                     f"{r['far_fraction']:.3f} | {r['near2_fraction']:.3f} | "
                     f"{r['median_distance_px']:.1f} | {r['user_reported_score']:.4f} |")
    lines += ["", "## Reference candidates (PROJECTED, not scores)", "",
              "| Candidate | Dots | Far >15 px | Near <=2 px | PROJECTED | 95% interval |",
              "|---|---:|---:|---:|---:|---:|"]
    for name, r in refs.items():
        p = r["projection"]
        lines.append(f"| {name} | {r['dots']} | {r['far_fraction']:.3f} | "
                     f"{r['near2_fraction']:.3f} | {p['projected_value']:.4f} | "
                     f"[{p['bootstrap_95_interval'][0]:.4f}, {p['bootstrap_95_interval'][1]:.4f}] |")
    (DOCS_DATA / "focus_analysis.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"focus": {k: {kk: vv for kk, vv in v.items() if kk in ('dots', 'far_fraction', 'near2_fraction', 'user_reported_score')} for k, v in rows.items()},
                      "model": model, "references": {k: {"dots": v["dots"], "far_fraction": v["far_fraction"],
                                                          "projection": v["projection"]["projected_value"],
                                                          "interval": v["projection"]["bootstrap_95_interval"]}
                                                     for k, v in refs.items()}}, indent=2))


if __name__ == "__main__":
    main()
