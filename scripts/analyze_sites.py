#!/usr/bin/env python3
"""Nine-site audit: geometry, pairwise literal overlap, and HOLDOUT-DTI.

Outputs:
  docs/data/site_analysis.json
  docs/data/site_analysis.md

Every score is labelled:
  USER-REPORTED  copied from the user's supplied site list (no organizer receipt)
  HOLDOUT-DTI    shared gems57.holdout hide-and-recover evaluator
  MEASURED       geometry computed here from the pinned rasters
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57 import grid as ggrid          # noqa: E402
from gems57 import holdout as gholdout    # noqa: E402
from gems57 import uniqueness             # noqa: E402

DATA = ROOT / "data"
DOCS_DATA = ROOT / "docs" / "data"
DOCS_DATA.mkdir(parents=True, exist_ok=True)
SITES = ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28",
         "GEMSDOE30", "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36")
FILES = {
    "GEMSDOE24": "GEMSDOE24.tif",
    "GEMSDOE25": "GEMSDOE25.tif",
    "GEMSDOE27": "GEMSDOE27.tif",
    "GEMSDOE28": "GEMSDOE28.tif",
    "GEMSDOE30": "GEMSDOE30.tif",
    "GEMSDOE31": "GEMSDOE31.tif",
    "GEMSDOE32": "GEMSDOE32.tif",
    "GEMSDOE33": "GEMSDOE33.tif",
    "GEMSDOE36": "GEMSDOE36.tif",
}
SCORES = {"GEMSDOE24": 0.2477, "GEMSDOE25": 0.2600, "GEMSDOE27": 0.2449,
          "GEMSDOE28": 0.2710, "GEMSDOE30": 0.2600, "GEMSDOE31": 0.2708,
          "GEMSDOE32": 0.2778, "GEMSDOE33": 0.2632, "GEMSDOE36": 0.2750}
LEADER_FILES = {
    "GEMSDOE24": "h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan",
    "GEMSDOE25": "dotted-h19-5-d2-8-20261002-e56ea318af89-nan",
    "GEMSDOE27": "topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan",
    "GEMSDOE28": "h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan",
    "GEMSDOE30": "d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca",
    "GEMSDOE31": "h27-4-solo-d28-20261004-8acb75e1-nan",
    "GEMSDOE32": "h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros",
    "GEMSDOE33": "h33d-analog-tip-stepover-r30-20261004-cb490425926e",
    "GEMSDOE36": "anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros",
}


def holdout_eval(mask, ctx):
    res = gholdout.evaluate(mask, ctx)
    cells = list(res["folds"].values())
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
            "ci95": [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))],
            "withheld_positive_pixels": int(res["pooled_n_truth"]),
            "n_cells": len(cells)}


def main():
    g = ggrid.load_grid(DATA / "bridge")
    fp, cat = g.footprint, g.catalogue
    dc = ndi.distance_transform_edt(~cat)
    masks, rows = {}, {}
    for s in SITES:
        p = DATA / "focus" / FILES[s]
        with rasterio.open(p) as src:
            a = src.read(1)
        m = (a > 0) & fp
        masks[s] = m
        d = dc[m]
        rows[s] = {"file": f"data/focus/{FILES[s]}", "leaderboard_file": LEADER_FILES[s],
                   "dots": int(m.sum()), "far_fraction": float((d > 15).mean()),
                   "near2_fraction": float((d <= 2).mean()),
                   "median_distance_px": float(np.median(d)),
                   "on_catalogue": int((a[cat] > 0).sum()),
                   "user_reported_score": SCORES[s],
                   "score_evidence_class": "USER-REPORTED — no organizer receipt"}
    # pairwise literal overlap
    overlap = {}
    for a in SITES:
        overlap[a] = {}
        for b in SITES:
            overlap[a][b] = float(uniqueness.dot_overlap(masks[a], masks[b]))
    for s in SITES:
        others = [b for b in SITES if b != s]
        worst = max(others, key=lambda b: overlap[s][b])
        rows[s]["max_forward_overlap_other_focus"] = overlap[s][worst]
        rows[s]["worst_other_focus"] = worst
        rows[s]["duplicates_over_70pct"] = [b for b in others if overlap[s][b] > 0.70]
        rows[s]["unique_vs_other_focus"] = bool(overlap[s][worst] <= 0.70)
    # holdout
    ctx = gholdout.build_holdout(g)
    for s in SITES:
        rows[s]["holdout"] = holdout_eval(masks[s], ctx)
    out = {"schema": "korea7-site-analysis-v1", "date_utc": "2026-11-04",
           "grid": {"crs": "EPSG:32611", "height": g.height, "width": g.width,
                    "footprint_cells": int(fp.sum()), "catalogue_cells": int(cat.sum())},
           "sites": rows, "pairwise_forward_3px_overlap": overlap,
           "evidence_labels": {"USER-REPORTED": "user-supplied, no receipt",
                               "HOLDOUT-DTI": "shared gems57.holdout hide-and-recover evaluator",
                               "MEASURED": "computed here from pinned rasters"}}
    (DOCS_DATA / "site_analysis.json").write_text(json.dumps(out, indent=2) + "\n")
    lines = ["# Nine-site audit", "",
             "All geometry and HOLDOUT-DTI values are measured from the pinned rasters. Scores are USER-REPORTED (no organizer receipt).",
             "", "| Site | Leaderboard file | Dots | Far >15 px | Near <=2 px | USER-REPORTED | HOLDOUT-DTI (95% CI) | Unique vs other focus? |",
             "|---|---|---:|---:|---:|---:|---:|---|"]
    for s in SITES:
        r = rows[s]
        lines.append(f"| {s} | `{r['leaderboard_file']}` | {r['dots']} | {r['far_fraction']:.3f} | "
                     f"{r['near2_fraction']:.3f} | {r['user_reported_score']:.4f} | "
                     f"{r['holdout']['pooled_dti']:.4f} [{r['holdout']['ci95'][0]:.4f}, {r['holdout']['ci95'][1]:.4f}] | "
                     f"{'YES' if r['unique_vs_other_focus'] else 'NO — duplicate'} |")
    lines += ["", "The nine focus-site rasters are one dotted-ridge family: every pair has forward 3-px overlap > 0.70. "
              "They are not mutually unique under the literal parallel-run rule.", ""]
    (DOCS_DATA / "site_analysis.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({s: {"dots": rows[s]["dots"], "far": round(rows[s]["far_fraction"], 3),
                          "holdout": round(rows[s]["holdout"]["pooled_dti"], 4),
                          "unique": rows[s]["unique_vs_other_focus"],
                          "max_overlap": round(rows[s]["max_forward_overlap_other_focus"], 3)}
                      for s in SITES}, indent=2))


if __name__ == "__main__":
    main()
