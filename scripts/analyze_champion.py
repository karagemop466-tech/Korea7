#!/usr/bin/env python3
"""Measured anatomy of the nine focus-site winners (why did GEMSDOE32-B2 lead?).

Inputs are the hash-pinned local mirrors in data/ and registry/ (see
scripts/restore_data.py). Everything printed here is computed from the actual
raster bytes in this checkout; user-reported leaderboard values are joined from
registry/owner_score_ledger.csv and are NOT organizer receipts.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import binary_dilation, distance_transform_edt
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
DATA, REG = ROOT / "data", ROOT / "registry"
SITES = [24, 25, 27, 28, 30, 31, 32, 33, 36]
BANDS = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 10), (10, 20), (20, 40), (40, 1e9)]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read(p: Path) -> np.ndarray:
    with rasterio.open(p) as s:
        return s.read(1)


def band_hist(d: np.ndarray) -> dict:
    out = {}
    for lo, hi in BANDS:
        key = f"[{lo},{hi if hi < 1e8 else 'inf'})px"
        out[key] = float(((d >= lo) & (d < hi)).mean()) if d.size else 0.0
    return out


def main() -> int:
    sample = read(DATA / "sample_submission.tif")
    foot = np.isfinite(sample)
    labels = (read(DATA / "labels.tif") > 0) & foot
    sgmc = (read(DATA / "external/derived_sgmc_faults_100m_u8.tif") > 0)
    near = binary_dilation(labels, iterations=3)
    sgmc_off = sgmc & ~labels & ~near & foot
    d_cat = distance_transform_edt(~labels)
    d_sgmc_off = distance_transform_edt(~sgmc_off)

    dots = {}
    rows = []
    for n in SITES:
        p = REG / f"GEMSDOE{n}.tif"
        a = read(p)
        m = np.isfinite(a) & (a == 1)
        dots[n] = m & foot
        ys, xs = np.nonzero(dots[n])
        tree = cKDTree(np.column_stack([ys, xs]))
        nn, _ = tree.query(np.column_stack([ys, xs]), k=2)
        dcat = d_cat[dots[n]]
        rows.append({
            "site": f"GEMSDOE{n}", "file": p.name, "sha256": sha256(p),
            "dots_in_footprint": int(dots[n].sum()),
            "values": sorted(set(np.unique(a[np.isfinite(a)]).tolist()))[:5],
            "outside_footprint_nan_frac": float(np.isnan(a[~foot]).mean()),
            "outside_footprint_zero_frac": float((a[~foot] == 0).mean()),
            "min_dist_to_catalogue_px": float(dcat.min()),
            "dist_to_catalogue_hist": band_hist(dcat),
            "frac_dots_within_3px_of_sgmc_offcat": float((d_sgmc_off[dots[n]] <= 3).mean()),
            "nn_spacing_px_median": float(np.median(nn[:, 1])),
            "nn_spacing_px_p10": float(np.percentile(nn[:, 1], 10)),
        })

    # Pairwise <=3px overlap (fraction of row's dots within 3px of column's dots)
    # and exact subset relations.
    overlap, subsets = {}, []
    d_to = {n: distance_transform_edt(~dots[n]) for n in SITES}
    for i in SITES:
        overlap[f"GEMSDOE{i}"] = {
            f"GEMSDOE{j}": float((d_to[j][dots[i]] <= 3).mean()) for j in SITES
        }
        for j in SITES:
            if i != j and not (dots[i] & ~dots[j]).any():
                subsets.append({"subset": f"GEMSDOE{i}", "superset": f"GEMSDOE{j}",
                                  "dots_removed": int(dots[j].sum() - dots[i].sum())})

    # What distinguishes the champion (32) from its superset (31)?
    removed = dots[31] & ~dots[32]
    champ = {
        "champion": "GEMSDOE32", "superset_compared": "GEMSDOE31",
        "removed_dots": int(removed.sum()),
        "removed_dist_to_catalogue_px": {
            "min": float(d_cat[removed].min()), "max": float(d_cat[removed].max()),
            "hist": band_hist(d_cat[removed])},
        "removed_frac_within_3px_of_sgmc_offcat": float((d_sgmc_off[removed] <= 3).mean()),
        "kept_frac_within_3px_of_sgmc_offcat": float((d_sgmc_off[dots[32]] <= 3).mean()),
    }

    # Where do off-catalogue SGMC proxy faults live, by distance to catalogue?
    gt_by_band = {}
    for lo, hi in BANDS:
        key = f"[{lo},{hi if hi < 1e8 else 'inf'})px"
        band = foot & (d_cat >= lo) & (d_cat < hi)
        gt_by_band[key] = {
            "footprint_px": int(band.sum()),
            "sgmc_offcat_gt_px": int((sgmc_off & band).sum()),
            "gt_density_per_1000px": float(1000 * (sgmc_off & band).sum() / max(band.sum(), 1)),
            "champion_dots": int((dots[32] & band).sum()),
            "champion_hit_frac_within_3px": (
                float((d_sgmc_off[dots[32] & band] <= 3).mean())
                if (dots[32] & band).any() else None),
        }

    out = {
        "grid": {"shape": list(foot.shape), "footprint_px": int(foot.sum()),
                 "catalogue_px": int(labels.sum()), "sgmc_offcat_gt_px": int(sgmc_off.sum())},
        "sites": rows, "pairwise_overlap_3px": overlap, "exact_subsets": subsets,
        "champion_vs_superset": champ, "sgmc_gt_by_catalogue_distance_band": gt_by_band,
        "note": "All values measured from local mirror bytes 2026-11-04. Leaderboard values are user-reported (registry/owner_score_ledger.csv), not organizer receipts.",
    }
    (ROOT / "evidence/champion_anatomy.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"grid": out["grid"], "champion_vs_superset": champ,
                      "exact_subsets": subsets}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
