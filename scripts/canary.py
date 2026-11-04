#!/usr/bin/env python3
"""Leakage canary: single-feature AUC of every available band.

Targets: (a) off-catalogue SGMC proxy faults (blind-fault proxy used by the
SGMC-CAL evaluator), (b) catalogue labels. AUC > 0.90 on a single band means
leakage until proven otherwise (parallel-run protocol rule 4). Negatives are
sampled inside the footprint with a fixed seed; AUC is the rank (Mann-Whitney)
statistic, identical to sklearn roc_auc_score on the same sample.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import binary_dilation
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
FILES = {
    "lidar_scarp_features_u8": D / "external/lidar_scarp_features_u8.tif",
    "geodawn_rad_u8": D / "external/geodawn_rad_u8.tif",
    "geodawn_extensions_u8": D / "external/geodawn_extensions_u8.tif",
}


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    r = rankdata(np.concatenate([pos, neg]))
    return float((r[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def main() -> int:
    with rasterio.open(D / "sample_submission.tif") as s:
        foot = np.isfinite(s.read(1))
    with rasterio.open(D / "labels.tif") as s:
        labels = (s.read(1) > 0) & foot
    with rasterio.open(D / "external/derived_sgmc_faults_100m_u8.tif") as s:
        sgmc = s.read(1) > 0
    sgmc_off = sgmc & ~labels & ~binary_dilation(labels, iterations=3) & foot

    rng = np.random.default_rng(20261104)
    def sample(mask: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
        ys, xs = np.nonzero(mask)
        idx = rng.choice(len(ys), size=min(n, len(ys)), replace=False)
        return ys[idx], xs[idx]

    pos_s = sample(sgmc_off, 20000)
    neg_s = sample(foot & ~sgmc & ~labels, 20000)
    pos_c = sample(labels, 20000)
    neg_c = sample(foot & ~labels, 20000)

    rows = []
    for name, path in FILES.items():
        with rasterio.open(path) as s:
            for i in range(1, s.count + 1):
                band = s.descriptions[i - 1] or f"band{i}"
                a = s.read(i).astype(np.float64)
                rows.append({
                    "file": name, "band": band,
                    "auc_sgmc_offcat": auc(a[pos_s], a[neg_s]),
                    "auc_catalogue": auc(a[pos_c], a[neg_c]),
                })
    out = {"seed": 20261104, "n_pos_neg_each": 20000,
           "rule": "single-feature AUC > 0.90 => leakage until proven otherwise",
           "max_auc": max(max(r["auc_sgmc_offcat"], r["auc_catalogue"]) for r in rows),
           "bands": rows}
    (ROOT / "evidence/canary.json").write_text(json.dumps(out, indent=2) + "\n")
    for r in rows:
        print(f"{r['file']:26s} {r['band']:12s} AUC sgmc-offcat {r['auc_sgmc_offcat']:.3f}  catalogue {r['auc_catalogue']:.3f}")
    print("max AUC:", round(out["max_auc"], 3), "-> canary", "FAIL" if out["max_auc"] > 0.90 else "PASS (no band > 0.90)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
