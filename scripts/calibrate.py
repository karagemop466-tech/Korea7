#!/usr/bin/env python3
"""Calibration: what actually drives a GEMS leaderboard score.

Inputs, all verified in this checkout:

* ``evidence/registry/*.tif`` -- the nine focus-site rasters, recovered from
  ``karagemop466-tech/GEMSDOEkarage3``.  Their original GitHub Pages host
  ``buffedlizard55-lab`` returns HTTP 404 on both the REST API and
  ``codeload`` (checked 2026-11-04), so these copies are the only surviving
  evidence and are retained for uniqueness auditing only.  They must never be
  submitted: several are pixel-identical to files already scored.
* ``evidence/ledger_measured.csv`` -- 38 rows of *measured* structure
  descriptors copied from the shared account ledger
  (``sassnarep3-star/GEMSDOESASS2 docs/data/org-ledger-measured.csv``),
  each paired with the score its owner reported.

Outputs ``evidence/calibration.json``.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation, distance_transform_edt, label
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from k7.grid import load_grid  # noqa: E402
from k7.metric import dti  # noqa: E402
from k7.overlap import compare  # noqa: E402

REG = ROOT / "evidence" / "registry"
OUT = ROOT / "evidence" / "calibration.json"

REPORTED = {
    "GEMSDOE24": 0.2477, "GEMSDOE25": 0.2600, "GEMSDOE27": 0.2449, "GEMSDOE28": 0.2710,
    "GEMSDOE30": 0.2600, "GEMSDOE31": 0.2708, "GEMSDOE32": 0.2778, "GEMSDOE33": 0.2632,
    "GEMSDOE36": 0.2750,
}


def main() -> int:
    import rasterio

    g = load_grid()
    foot, truth = g.footprint, g.truth
    dist = distance_transform_edt(~truth)
    out: dict = {"grid": {"footprint": g.n_footprint, "catalogue_positives": g.n_truth}}

    # ---------- 1. catalogue-dilation ladder (the in-sample optimum)
    ladder = []
    for k in range(0, 9):
        m = truth if k == 0 else binary_dilation(truth, iterations=k)
        m = m & foot
        ladder.append({"dilate_px": k, "emitted": int(m.sum()),
                       "in_sample_dti": float(dti(m.astype(np.float32), truth, foot))})
    out["catalogue_dilation_ladder"] = ladder

    # ---------- 2. measure the nine focus rasters
    files = sorted(REG.glob("*.tif"))
    measured = {}
    masks = {}
    for p in files:
        site = p.name.split("-")[0]
        with rasterio.open(p) as ds:
            a = ds.read(1)
        m = np.nan_to_num(a) > 0
        masks[site] = m
        dm = dist[m]
        measured[site] = {
            "file": p.name,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "nan_cells": int(np.isnan(a).sum()) if np.issubdtype(a.dtype, np.floating) else 0,
            "dots": int(m.sum()),
            "frac_within_2px": float((dm <= 2).mean()),
            "frac_within_3px": float((dm <= 3).mean()),
            "median_dist_px": float(np.median(dm)),
            "in_sample_dti": float(dti(m.astype(np.float32), truth, foot)),
            "reported_score": REPORTED.get(site),
        }
    out["focus_rasters"] = measured

    # ---------- 3. exact mechanism of the best file
    A25, A31, A32 = masks["GEMSDOE25"], masks["GEMSDOE31"], masks["GEMSDOE32"]
    out["mechanism"] = {
        "A32_equals_A25_pruned_at_2px": bool((A25 & (dist > 2) == A32).all() and (A32 & ~A25).sum() == 0),
        "A32_equals_A31_pruned_at_2px": bool((A31 & (dist > 2) == A32).all() and (A32 & ~A31).sum() == 0),
        "dots_removed_25_to_32": int(A25.sum() - A32.sum()),
        "dots_removed_31_to_32": int(A31.sum() - A32.sum()),
        "A32_has_any_dot_within_2px": bool(((dist <= 2) & A32).any()),
        "A25_has_any_dot_within_1px": bool(((dist <= 1) & A25).any()),
    }

    # ---------- 4. duplicate scan across the nine
    dups = []
    keys = sorted(masks)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            ov = compare(masks[a], masks[b])
            if ov.jaccard >= 0.90:
                dups.append({"a": a, "b": b, "jaccard": ov.jaccard,
                             "identical": ov.intersection == ov.candidate_dots == ov.registry_dots})
    out["duplicates"] = dups

    # ---------- 5. dots vs score across the nine
    xs = [measured[k]["dots"] for k in keys]
    ys = [REPORTED[k] for k in keys]
    rho, p = spearmanr(xs, ys)
    out["dots_vs_score_focus9"] = {"spearman_rho": float(rho), "p_value": float(p), "n": len(keys)}

    # ---------- 6. dots vs score across the ledger (38 rows)
    rows = list(csv.DictReader(open(ROOT / "evidence" / "ledger_measured.csv")))
    L = []
    for r in rows:
        try:
            n = float(r["dots_gt0"]); s = float(r["owner_reported_score"])
        except (ValueError, KeyError):
            continue
        if n <= 0:
            continue
        L.append({"site": r["site"], "stem": r["stem"], "dots": n, "score": s,
                  "frac_beyond_2px": float(r["dots_beyond_2px_of_catalogue"]) / n,
                  "frac_beyond_3px": float(r["dots_beyond_3px_of_catalogue"]) / n,
                  "median_dist_px": float(r["median_dist_to_catalogue_px"]),
                  "inrow_gap_px": float(r["median_inrow_dot_gap_px"])})
    lr, lp = spearmanr([x["dots"] for x in L], [x["score"] for x in L])
    out["ledger"] = {"n": len(L), "spearman_rho_dots_score": float(lr), "p_value": float(lp)}

    # clearance contrast: does every dot being beyond 2 px separate the top of the table?
    clean = sorted([x for x in L if x["frac_beyond_2px"] == 1.0], key=lambda x: -x["score"])
    dirty = sorted([x for x in L if x["frac_beyond_2px"] < 1.0], key=lambda x: -x["score"])
    out["clearance_contrast"] = {
        "all_beyond_2px": {"n": len(clean), "mean_score": float(np.mean([x["score"] for x in clean])),
                           "median_score": float(np.median([x["score"] for x in clean])),
                           "top": clean[:5]},
        "some_within_2px": {"n": len(dirty), "mean_score": float(np.mean([x["score"] for x in dirty])),
                            "median_score": float(np.median([x["score"] for x in dirty])),
                            "top": dirty[:5]},
    }
    out["ledger_rows"] = L

    OUT.write_text(json.dumps(out, indent=2, default=str) + "\n")

    # ---------- console summary
    print(f"grid: footprint={g.n_footprint:,} catalogue={g.n_truth:,}")
    print("\ncatalogue-dilation ladder (in-sample DTI vs labels):")
    for r in ladder[:6]:
        print(f"  k={r['dilate_px']}px emitted={r['emitted']:7d} DTI={r['in_sample_dti']:.4f}")
    print("\nmechanism of GEMSDOE32 (0.2778):")
    for k, v in out["mechanism"].items():
        print(f"  {k}: {v}")
    print(f"\nfocus-9 rho(dots, score) = {rho:.4f} (p={p:.2e}, n={len(keys)})")
    print(f"ledger    rho(dots, score) = {lr:.4f} (p={lp:.2e}, n={len(L)})")
    c = out["clearance_contrast"]
    print(f"\nall dots beyond 2 px : n={c['all_beyond_2px']['n']:2d} mean={c['all_beyond_2px']['mean_score']:.4f} median={c['all_beyond_2px']['median_score']:.4f}")
    print(f"some dots within 2 px: n={c['some_within_2px']['n']:2d} mean={c['some_within_2px']['mean_score']:.4f} median={c['some_within_2px']['median_score']:.4f}")
    print("\nduplicates at Jaccard>=0.90:")
    for d in dups:
        print(f"  {d['a']} ~ {d['b']}  Jaccard={d['jaccard']:.4f} identical={d['identical']}")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
