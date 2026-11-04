#!/usr/bin/env python3
"""Figure for the executive summary: candidate vs champion dots + proxy scores.

Left: footprint with KOREA7-E3 dots (teal) and GEMSDOE32-B2 champion dots
(orange), block-max downsampled x8 for display only. Right: reproduced
GEMSDOE32-SGMC-CAL-v3.0 HOLDOUT-DTI with 95% CI for the nine + Korea7 E1/E3.
All numbers come from evidence/eval_*.json produced in this repo.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import rasterio  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def down(m: np.ndarray, f: int = 8) -> np.ndarray:
    h, w = m.shape
    return m[: h // f * f, : w // f * f].reshape(h // f, f, w // f, f).max(axis=(1, 3))


def main() -> int:
    with rasterio.open(ROOT / "data/sample_submission.tif") as s:
        foot = np.isfinite(s.read(1))
    e3 = np.load(ROOT / "work/E3_mask.npy")
    with rasterio.open(ROOT / "registry/GEMSDOE32.tif") as s:
        b2 = s.read(1) == 1
    img = np.zeros((*down(foot).shape, 3), dtype=np.float32) + 0.12
    img[down(foot) > 0] = (0.92, 0.94, 0.96)
    img[down(b2) > 0] = (0.95, 0.55, 0.10)
    img[down(e3) > 0] = (0.05, 0.55, 0.55)

    names, vals, lo, hi = [], [], [], []
    order = [24, 27, 25, 30, 33, 28, 31, 32, 36]
    for n in order:
        p = ROOT / (f"evidence/eval_GEMSDOE{n}.json" if n != 32 else "evidence/repro_GEMSDOE32.json")
        sg = json.loads(p.read_text())["sgmc_off_catalogue"]
        names.append(f"GEMSDOE{n}")
        vals.append(sg["sgmc_prevalence_calibrated_dti"])
        lo.append(sg["sgmc_calibrated_ci95"][0]); hi.append(sg["sgmc_calibrated_ci95"][1])
    for lab, f in [("KOREA7-E1", "eval_E1.json"), ("KOREA7-E3 ★", "eval_E3.json")]:
        sg = json.loads((ROOT / f"evidence/{f}").read_text())["sgmc_off_catalogue"]
        names.append(lab); vals.append(sg["sgmc_prevalence_calibrated_dti"])
        lo.append(sg["sgmc_calibrated_ci95"][0]); hi.append(sg["sgmc_calibrated_ci95"][1])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1, 1.25]})
    a1.imshow(img, interpolation="nearest")
    a1.set_title("Dots: KOREA7-E3 (teal) vs GEMSDOE32-B2 champion (orange)\nboth 37,654 dots; exact-dot Jaccard 0.007", fontsize=9)
    a1.axis("off")
    y = np.arange(len(names))
    colors = ["#8aa0b4"] * 9 + ["#7fb3b0", "#0b6b66"]
    a2.barh(y, vals, xerr=[np.array(vals) - lo, np.array(hi) - np.array(vals)],
            color=colors, error_kw={"lw": 0.8})
    a2.set_yticks(y, names, fontsize=8)
    a2.set_xlabel("HOLDOUT-DTI  (GEMSDOE32-SGMC-CAL-v3.0, 62,703 withheld proxy positives)")
    a2.set_title("Reproduced in this repo 2026-11-04 — proxy, NOT leaderboard score", fontsize=9)
    a2.invert_yaxis()
    for i, v in enumerate(vals):
        a2.text(v + 0.0015, i, f"{v:.4f}", va="center", fontsize=7.5)
    fig.tight_layout()
    out = ROOT / "docs/assets/korea7-e3-vs-nine.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
