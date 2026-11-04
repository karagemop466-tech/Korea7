#!/usr/bin/env python3
"""Fold-local OOF emission of E1 for the shared hide-and-recover evaluator.

Static masks are construction-censored on hide-and-recover (their full-
catalogue b2 gate removes dots near segments a fold hides). This script
re-emits E1 separately inside every evaluator cell using ONLY that cell's
visible faults for the >2 px gate (d_visible_sub), so the resulting pooled
HOLDOUT-DTI is the leak-free instrument reading. Surface and greedy rule are
identical to scripts/build_experiments.py; per-cell budget is the champion
budget scaled by the cell domain's share of footprint pixels.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor/gems32/src"))
sys.path.insert(0, str(ROOT / "scripts"))
from gems32 import holdout  # noqa: E402
from build_experiments import greedy_cover, BUDGET  # noqa: E402


def main() -> int:
    ctx = holdout.load_holdout_context(ROOT / "data")
    with rasterio.open(ROOT / "work/E1_surface.tif") as s:
        surf = s.read(1)
    cells = {}
    info = {}
    for cell in ctx.cells:
        sl = cell.bbox
        sub_surf = surf[sl]
        eligible = cell.active_sub & (cell.d_visible_sub > 2.0) & (sub_surf > 0)
        domain_px = int(cell.active_sub.sum())
        budget = int(round(BUDGET * domain_px / int(ctx.foot.sum())))
        mask = greedy_cover(np.where(eligible, sub_surf, 0.0).astype(np.float32),
                            eligible, budget)
        cells[cell.key] = mask
        info[cell.key] = {"domain_px": domain_px, "budget": budget, "dots": int(mask.sum())}
        print(cell.key, info[cell.key])
    out = ROOT / "work/E1_oof.npz"
    np.savez_compressed(out, **cells)
    (ROOT / "evidence/e1_oof_build.json").write_text(json.dumps(info, indent=2) + "\n")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
