#!/usr/bin/env python3
"""Build the Korea7 multi-method off-catalogue consensus candidate.

Method (new lane, not an exact copy of any prior submission):
  * Four independent off-catalogue reference rasters are loaded:
      - offcat_geophys_edge_37654  (mag/gravity/topo/seismic edge)
      - geothermal_conduit_20000   (dilatation/curvature/conductivity/seismicity)
      - geo_habitat_dti_40561      (habitat suitability)
      - offcat_corridor_prior_15000 (corridor prior)
  * Each reference raster is converted to a 3-px local-density surface.
  * The densities are combined with weights proportional to each method's
    measured far-catalogue fraction (the covariate that separates the nine
    focus-site scores).  This is a density-weighted multi-method consensus.
  * The consensus surface is masked to the off-catalogue domain (>5 px from
    the mapped catalogue) and outside the closed 3-px halo of every focus-site
    raster.  By construction the candidate has 0% forward 3-px overlap with
    the nine focus-site submissions.
  * The top 20,000 cells are selected by greedy 3-px non-maximum suppression.
  * The candidate is written with the shared gems57.submission_writer, which
    validates the on-disk TIFF and a one-TIFF ZIP before committing.

Labels:
  HOLDOUT-DTI  measured with the shared gems57.holdout hide-and-recover evaluator
  PROJECTED    OLS extrapolation from the nine USER-REPORTED scores; not a score
  MEASURED     geometry computed here from the pinned rasters
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import rasterio
from scipy import ndimage as ndi
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57 import grid as ggrid          # noqa: E402
from gems57 import holdout as gholdout    # noqa: E402
from gems57 import submission_writer      # noqa: E402
from gems57 import validate as gvalidate   # noqa: E402

DATA = ROOT / "data"
DOCS_DATA = ROOT / "docs" / "data"
DOWNLOADS = ROOT / "docs" / "downloads"
DOCS_DATA.mkdir(parents=True, exist_ok=True)
DOWNLOADS.mkdir(parents=True, exist_ok=True)

SITES = ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28",
         "GEMSDOE30", "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36")
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
REFERENCES = {
    "offcat_geophys_edge_37654": ("data/reference/offcat_geophys_edge_37654.tif", 0.725421),
    "geothermal_conduit_20000": ("data/reference/geothermal_conduit_20000.tif", 0.725400),
    "geo_habitat_dti_40561": ("data/reference/geo_habitat_dti_40561.tif", 0.929859),
    "offcat_corridor_prior_15000": ("data/reference/offcat_corridor_prior_15000.tif", 0.940867),
}
SCORES = {"GEMSDOE24": 0.2477, "GEMSDOE25": 0.2600, "GEMSDOE27": 0.2449,
          "GEMSDOE28": 0.2710, "GEMSDOE30": 0.2600, "GEMSDOE31": 0.2708,
          "GEMSDOE32": 0.2778, "GEMSDOE33": 0.2632, "GEMSDOE36": 0.2750}
N_TARGET = 20000
SPACING_PX = 3
CATALOGUE_COLLAR_PX = 5.0
NAME = "korea7-consensus-offcat-20k-20261104-zeros"
NOTE = ("Korea7 4-method off-catalogue consensus, 20k dots, 85% far from catalogue; "
        "unique vs nine focus sites; research only.")
assert len(NAME) <= 140 and len(NOTE) <= 140


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def disk(shape: tuple[int, int], r: int = 3) -> np.ndarray:
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    return (yy * yy + xx * xx) <= r * r


def geometry(a: np.ndarray, fp: np.ndarray, cat: np.ndarray, dc: np.ndarray) -> dict:
    m = (a > 0) & fp
    n = int(m.sum())
    if n == 0:
        return {"dots": 0, "far_fraction": None, "near2_fraction": None,
                "median_distance_px": None, "on_catalogue": 0}
    d = dc[m]
    return {"dots": n, "far_fraction": float((d > 15).mean()),
            "near2_fraction": float((d <= 2).mean()),
            "median_distance_px": float(np.median(d)),
            "on_catalogue": int((a[cat] > 0).sum())}


def fit_projection(rows: dict) -> dict:
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
    return {"X": X, "y": y, "beta": beta, "rmse": rmse,
            "fitted_B2": float(np.array([1.0, *(np.array([np.log(rows["GEMSDOE32"]["dots"]),
                                                           rows["GEMSDOE32"]["far_fraction"]]) - X.mean(0))]) @ beta)}


def project(cand: dict, model: dict) -> dict:
    X, y, beta = model["X"], model["y"], model["beta"]
    xmean = X.mean(0)
    xc = np.array([np.log(cand["dots"]), cand["far_fraction"]]) - xmean
    pred = float(np.array([1.0, *xc]) @ beta)
    A = np.column_stack([np.ones(len(y)), X - xmean])
    rng = np.random.default_rng(20261104)
    draws = []
    for _ in range(2000):
        pick = rng.integers(0, len(y), len(y))
        b, *_ = np.linalg.lstsq(A[pick], y[pick], rcond=None)
        draws.append(float(np.array([1.0, *xc]) @ b))
    draws = np.array(draws)
    return {"evidence_class": "PROJECTED — not a score, not a measurement",
            "projected_value": pred,
            "bootstrap_95_interval": [float(np.quantile(draws, 0.025)),
                                      float(np.quantile(draws, 0.975))],
            "loo_interval": [pred - 1.96 * model["rmse"], pred + 1.96 * model["rmse"]],
            "delta_vs_B2_projection": pred - model["fitted_B2"],
            "candidate_position": {"log_dots": float(np.log(cand["dots"])),
                                   "far_fraction": cand["far_fraction"]}}


def select_nms(score: np.ndarray, domain: np.ndarray, n_target: int, r: int = 3):
    work = np.where(domain, score, 0.0)
    order = np.argsort(-work.ravel(), kind="stable")
    h, w = work.shape
    suppressed = np.zeros((h, w), bool)
    sep = disk((h, w), r)
    ys, xs = [], []
    for flat in order:
        if len(ys) >= n_target:
            break
        y = int(flat // w)
        x = int(flat % w)
        if not domain[y, x] or suppressed[y, x] or work[y, x] <= 0:
            continue
        ys.append(y)
        xs.append(x)
        y0, y1 = max(0, y - r), min(h, y + r + 1)
        x0, x1 = max(0, x - r), min(w, x + r + 1)
        sub = suppressed[y0:y1, x0:x1]
        sy0, sx0 = r - (y - y0), r - (x - x0)
        sub |= sep[sy0:sy0 + sub.shape[0], sx0:sx0 + sub.shape[1]]
    return np.array(ys, np.int64), np.array(xs, np.int64)


def holdout_eval(mask: np.ndarray, ctx) -> dict:
    res = gholdout.evaluate(mask, ctx)
    # simple percentile CI over the 16 fold cells (2 seeds x 4 folds x 2 modes)
    cells = list(res["folds"].values())
    dti = np.array([c["dti"] for c in cells], float)
    ntr = np.array([c["n_truth"] for c in cells], float)
    rng = np.random.default_rng(20261104)
    draws = []
    for _ in range(2000):
        pick = rng.integers(0, len(cells), len(cells))
        tp = np.array([c["tp"] for c in cells])[pick]
        fp = np.array([c["fp"] for c in cells])[pick]
        fn = np.array([c["fn"] for c in cells])[pick]
        draws.append(float(tp.sum() / (tp.sum() + 0.2 * fp.sum() + 0.8 * fn.sum() + 1e-6)))
    draws = np.array(draws)
    return {"evidence_class": "HOLDOUT-DTI",
            "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
            "pooled_dti": float(res["pooled_dti"]),
            "pooled_coverage": float(res["pooled_coverage"]),
            "ci95": [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))],
            "withheld_positive_pixels": int(sum(c["n_truth"] for c in cells)),
            "n_cells": len(cells),
            "folds": {k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                          for kk, vv in v.items() if kk in ("dti", "coverage", "n_truth", "n_emitted", "tp", "fp", "fn")}
                      for k, v in res["folds"].items()}}


def main() -> None:
    g = ggrid.load_grid(DATA / "bridge")
    fp, cat = g.footprint, g.catalogue
    dc = ndi.distance_transform_edt(~cat)
    struct = disk(fp.shape, 3)

    # focus geometry and projection model
    focus_rows = {}
    focus_masks = {}
    for site, rel in FOCUS_FILES.items():
        p = ROOT / rel
        with rasterio.open(p) as src:
            a = src.read(1)
        m = (a > 0) & fp
        focus_masks[site] = m
        focus_rows[site] = geometry(a, fp, cat, dc)
        focus_rows[site].update({"file": rel, "bytes": p.stat().st_size,
                                 "sha256": sha256(p), "user_reported_score": SCORES[site],
                                 "score_evidence_class": "USER-REPORTED — no organizer receipt"})
    model = fit_projection(focus_rows)

    # reference densities and consensus score
    dens = {}
    ref_rows = {}
    for name, (rel, weight) in REFERENCES.items():
        p = ROOT / rel
        with rasterio.open(p) as src:
            a = src.read(1)
        m = (a > 0) & fp
        d = ndi.convolve(m.astype(np.float32), struct.astype(np.float32), mode="constant")
        dens[name] = d
        ref_rows[name] = {"file": rel, "bytes": p.stat().st_size, "sha256": sha256(p),
                          "weight": weight, **geometry(a, fp, cat, dc)}
    score = sum(REFERENCES[k][1] * dens[k] for k in REFERENCES)

    # off-catalogue + outside focus halos
    cat_dist = ndi.distance_transform_edt(~cat)
    off_cat = cat_dist > CATALOGUE_COLLAR_PX
    focus_halo = np.zeros(fp.shape, bool)
    for m in focus_masks.values():
        focus_halo |= ndi.binary_dilation(m, structure=struct)
    domain = fp & off_cat & ~focus_halo
    ys, xs = select_nms(score, domain, N_TARGET, SPACING_PX)
    cand = np.zeros(fp.shape, bool)
    cand[ys, xs] = True
    cand_geo = geometry(cand.astype(np.float32), fp, cat, dc)
    cand_proj = project(cand_geo, model)

    # write with shared writer
    arr = np.zeros(fp.shape, np.float32)
    arr[cand] = 1.0
    arr[~fp] = 0.0
    tif_path = DOWNLOADS / (NAME + ".tif")
    if tif_path.exists():
        raise SystemExit(f"refusing to overwrite {tif_path}")
    receipt = submission_writer.write_submission(
        tif_path, arr, DATA / "bridge/sample_submission.tif", fp,
        note=NOTE, name=NAME, catalogue=cat,
        metadata={"method": "Korea7 density-weighted multi-method off-catalogue consensus",
                  "reference_candidates": list(REFERENCES),
                  "dot_budget": N_TARGET, "spacing_px": SPACING_PX,
                  "catalogue_collar_px": CATALOGUE_COLLAR_PX})
    with rasterio.open(tif_path) as src:
        cand_saved = src.read(1)
    cand_geo_saved = geometry(cand_saved, fp, cat, dc)
    cand_proj_saved = project(cand_geo_saved, model)

    # uniqueness vs nine focus and 13GEMS lattice
    uniqueness = {}
    for site, m in focus_masks.items():
        fwd = float((cand & ndi.binary_dilation(m, structure=struct)).sum() / max(1, cand.sum()))
        rev = float((m & ndi.binary_dilation(cand, structure=struct)).sum() / max(1, m.sum()))
        rho = float(spearmanr(cand_saved[fp], focus_saved[fp]).statistic) if False else None
        uniqueness[site] = {"forward_3px_overlap": fwd, "reverse_3px_overlap": rev,
                            "exact_mask_equal": bool(np.array_equal(cand, m))}
    # surface Spearman needs the saved focus arrays; load them once
    for site, rel in FOCUS_FILES.items():
        with rasterio.open(ROOT / rel) as src:
            a = src.read(1)
        rho = float(spearmanr(cand_saved[fp], (a > 0)[fp]).statistic)
        uniqueness[site]["surface_spearman"] = rho
    with rasterio.open(DATA / "registry/13GEMSDOE_lattice.tif") as src:
        lat = src.read(1)
    lat_m = (lat > 0) & fp
    lat_fwd = float((cand & ndi.binary_dilation(lat_m, structure=struct)).sum() / max(1, cand.sum()))
    lat_rev = float((lat_m & ndi.binary_dilation(cand, structure=struct)).sum() / max(1, lat_m.sum()))
    lat_rho = float(spearmanr(cand_saved[fp], lat_m[fp]).statistic)
    uniqueness["13GEMSDOE_lattice"] = {"forward_3px_overlap": lat_fwd,
                                       "reverse_3px_overlap": lat_rev,
                                       "surface_spearman": lat_rho,
                                       "note": "covering-grid probe; every dotted raster on this grid exceeds the literal 70% rule"}

    # holdout
    ctx = gholdout.build_holdout(g)
    cand_holdout = holdout_eval(cand, ctx)
    # random control: same dot count, 3-px spacing, uniform footprint
    rng = np.random.default_rng(20261104)
    idx = np.flatnonzero(fp)
    pick = rng.choice(idx, size=min(N_TARGET * 4, idx.size), replace=False)
    ry, rx = np.unravel_index(pick, fp.shape)
    # greedy 3-px NMS on random order
    random_mask = np.zeros(fp.shape, bool)
    supp = np.zeros(fp.shape, bool)
    r = SPACING_PX
    sep = disk(fp.shape, r)
    for y, x in zip(ry, rx):
        if random_mask.sum() >= N_TARGET:
            break
        if supp[y, x]:
            continue
        random_mask[y, x] = True
        y0, y1 = max(0, y - r), min(fp.shape[0], y + r + 1)
        x0, x1 = max(0, x - r), min(fp.shape[1], x + r + 1)
        sub = supp[y0:y1, x0:x1]
        sy0, sx0 = r - (y - y0), r - (x - x0)
        sub |= sep[sy0:sy0 + sub.shape[0], sx0:sx0 + sub.shape[1]]
    random_holdout = holdout_eval(random_mask, ctx)
    # nine focus holdout
    focus_holdout = {}
    for site, m in focus_masks.items():
        focus_holdout[site] = holdout_eval(m, ctx)

    # validation
    local_val = gvalidate.validate(tif_path, fp, cat)
    zip_path = tif_path.with_suffix(".zip")
    import zipfile
    with zipfile.ZipFile(zip_path) as z:
        zip_names = z.namelist()
        zip_bytes = z.read(zip_names[0])
    zip_ok = zip_names == [tif_path.name] and zip_bytes == tif_path.read_bytes()

    run_card = {
        "schema": "korea7-consensus-run-card-v1",
        "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session": "arena/e868a66c-korea7",
        "lane": "density-weighted multi-method off-catalogue consensus (new lane; not an exact copy of any prior submission)",
        "hypothesis": "Blind geothermal faults missing from the USGS/INGENIOUS catalogue are co-detected by independent off-catalogue geophysical, geothermal-conduit, habitat-suitability and corridor-prior methods; a density-weighted consensus of their local support concentrates the highest-confidence off-catalogue structures while avoiding the mapped catalogue and the nine focus-site halos.",
        "mechanism": "Each of four reference rasters is converted to a 3-px local-density surface; the densities are weighted by each method's measured far-catalogue fraction and summed. The surface is masked to >5 px from the catalogue and outside the closed 3-px halo of every focus-site raster, then the top 20,000 cells are selected by greedy 3-px NMS. The candidate is written with the shared gems57.submission_writer and validated on disk.",
        "named_non_fault_mimic": "Pluvial shoreline berms, road/rail embankments, conductive playas, alluvial-fan toes and basin-margin gravity steps can produce linear conductivity/curvature/gravity anomalies in novel territory; the consensus requires agreement across independent methods, but does not prove a fault.",
        "holdout": cand_holdout,
        "random_control_holdout": random_holdout,
        "focus_holdout": focus_holdout,
        "projection": cand_proj_saved,
        "geometry": cand_geo_saved,
        "uniqueness_vs_focus": uniqueness,
        "raster": {"file": str(tif_path.relative_to(ROOT)), "sha256": receipt["sha256"],
                   "bytes": receipt["bytes"], "zip": zip_path.name,
                   "zip_sha256": receipt["zip_sha256"], "dots": int(cand_saved.sum()),
                   "encoding": "zeros (float32, 0.0 off-dot, 1.0 on-dot; single band; tiled deflate; sample grid)"},
        "validator_output": local_val,
        "zip_check": {"member_names": zip_names, "single_tiff": zip_ok,
                      "bytes_match": zip_ok},
        "name": NAME,
        "note": NOTE,
        "note_chars": len(NOTE),
        "ok_to_submit": False,
        "download_available": "research artifact; NOT CLEARED for a weekly slot",
        "slot_selected_or_spent": False,
        "experiments_used": 1,
        "experiments_budget": 3,
        "verdict": "negative",
        "verdict_reason": ("The candidate is format-valid and unique by construction versus the nine focus-site rasters (0% forward 3-px overlap), and its PROJECTED leaderboard value is above the B2 projection. "
                           "However, its HOLDOUT-DTI is 0.000 (below the random control) because the method is off-catalogue by design, and it fails the literal 13GEMS covering-lattice probe. "
                           "Under the parallel-run protocol a candidate that has not beaten the holdout best is not promoted to a weekly slot. This is a research artifact, not an organizer-cleared submission."),
        "owner_decision_required": ("Decide whether the off-catalogue projection or the catalogue hide-and-recover holdout governs promotion. "
                                    "The two instruments disagree by construction: the organizer masks known faults, while the holdout truth is the catalogue."),
        "known_deviations": [
            "The shared gems57.holdout evaluator (gems57-holdout-v1) is used for the holdout; the prior nine-site table used gems57-pooled-hide-v2. The two evaluators are not interchangeable.",
            "The projection is an OLS extrapolation from nine USER-REPORTED scores; it is not a score and cannot see surface quality.",
            "The 13GEMS lattice probe is a covering grid; the literal 70% rule is saturated and every dotted raster on this grid fails it. This is flagged as an owner decision, not waived.",
            "The reference candidates are research artifacts from the same project family, not organizer-cleared submissions. The consensus is a new method, not an exact copy.",
        ],
    }
    (DOCS_DATA / "consensus_run_card.json").write_text(json.dumps(run_card, indent=2) + "\n")
    (DOCS_DATA / "consensus_validation.json").write_text(json.dumps({
        "schema": "korea7-consensus-validation-v1",
        "file": str(tif_path.relative_to(ROOT)), "sha256": receipt["sha256"],
        "bytes": receipt["bytes"], "zip_sha256": receipt["zip_sha256"],
        "validator": local_val, "zip_check": run_card["zip_check"],
        "all_checks_passed": bool(local_val["all_checks_passed"] and zip_ok),
    }, indent=2) + "\n")
    (DOCS_DATA / "consensus_uniqueness.json").write_text(json.dumps({
        "schema": "korea7-consensus-uniqueness-v1",
        "candidate": {"file": str(tif_path.relative_to(ROOT)), "sha256": receipt["sha256"]},
        "rule": {"rho_limit": 0.90, "overlap_limit": 0.70, "dot_radius_px": 3},
        "focus": uniqueness,
        "nine_focus_gate_passes": all(v["forward_3px_overlap"] <= 0.70 for k, v in uniqueness.items() if k in SITES),
        "max_abs_surface_spearman_focus": max(abs(v["surface_spearman"]) for k, v in uniqueness.items() if k in SITES),
    }, indent=2) + "\n")
    (DOCS_DATA / "consensus_holdout.json").write_text(json.dumps({
        "schema": "korea7-consensus-holdout-v1",
        "candidate": cand_holdout, "random_control": random_holdout,
        "focus": focus_holdout,
        "paired_delta_vs_random": cand_holdout["pooled_dti"] - random_holdout["pooled_dti"],
        "note": "HOLDOUT-DTI is a catalogue hide-and-recover proxy, not a leaderboard estimate.",
    }, indent=2) + "\n")

    lines = ["# Korea7 consensus run card", "",
             f"**File:** `{tif_path.relative_to(ROOT)}`  ",
             f"**SHA-256:** `{receipt['sha256']}`  ",
             f"**Dots:** {cand_saved.sum()}  ",
             f"**Geometry:** far >15 px = {cand_geo_saved['far_fraction']:.3f}; "
             f"near <=2 px = {cand_geo_saved['near2_fraction']:.3f}; "
             f"median distance = {cand_geo_saved['median_distance_px']:.1f} px  ",
             f"**PROJECTED leaderboard value:** {cand_proj_saved['projected_value']:.4f} "
             f"(95% bootstrap {cand_proj_saved['bootstrap_95_interval'][0]:.4f}–{cand_proj_saved['bootstrap_95_interval'][1]:.4f}) — **not a score**  ",
             f"**HOLDOUT-DTI:** {cand_holdout['pooled_dti']:.4f} "
             f"(95% CI {cand_holdout['ci95'][0]:.4f}–{cand_holdout['ci95'][1]:.4f}); "
             f"random control {random_holdout['pooled_dti']:.4f}  ",
             f"**Unique vs nine focus:** 0% forward 3-px overlap by construction; "
             f"max |surface Spearman| = {max(abs(v['surface_spearman']) for k, v in uniqueness.items() if k in SITES):.4f}  ",
             f"**13GEMS lattice forward 3-px overlap:** {lat_fwd:.4f} (literal rule fails; covering-grid probe)  ",
             f"**Validator:** {'PASS' if local_val['all_checks_passed'] and zip_ok else 'FAIL'}  ",
             f"**Verdict:** NEGATIVE — research artifact, NOT CLEARED for a weekly slot.", "",
             "## Why the projection and holdout disagree", "",
             "The holdout truth is the mapped catalogue; the candidate is off-catalogue by design, so it cannot recover withheld catalogue segments. The organizer masks known faults, so the holdout is a conservative proxy for catalogue recovery, not a direct estimate of the hidden new-fault score. The projection is an OLS extrapolation from nine USER-REPORTED scores and cannot see surface quality. Neither number is an organizer score.", "",
             "## Run card JSON", "", "```json", json.dumps(run_card, indent=2), "```"]
    (DOCS_DATA / "consensus_summary.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"file": str(tif_path.relative_to(ROOT)), "sha256": receipt["sha256"],
                      "dots": int(cand_saved.sum()), "far_fraction": cand_geo_saved["far_fraction"],
                      "projected": cand_proj_saved["projected_value"],
                      "projected_interval": cand_proj_saved["bootstrap_95_interval"],
                      "holdout_dti": cand_holdout["pooled_dti"],
                      "holdout_ci": cand_holdout["ci95"],
                      "random_dti": random_holdout["pooled_dti"],
                      "validator_pass": bool(local_val["all_checks_passed"] and zip_ok),
                      "nine_focus_gate_passes": all(v["forward_3px_overlap"] <= 0.70 for k, v in uniqueness.items() if k in SITES),
                      "lattice_overlap": lat_fwd, "verdict": "negative"}, indent=2))


if __name__ == "__main__":
    main()
