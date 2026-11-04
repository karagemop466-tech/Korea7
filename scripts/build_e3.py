#!/usr/bin/env python3
"""E3 (predeclared): E1 surface + TIGER road-distance mimic control.

Identical to E1 except pixels <100 m from a road are ineligible; the greedy
coverage emission refills the 37,654-dot budget from the remaining surface.
Roads are the named non-fault mimic for scarp detectors.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_experiments import greedy_cover, BUDGET  # noqa: E402

ROAD_MIN_M = 100.0


def main() -> int:
    D = ROOT / "data"
    with rasterio.open(D / "sample_submission.tif") as s:
        foot = np.isfinite(s.read(1))
    with rasterio.open(D / "labels.tif") as s:
        labels = (s.read(1) > 0) & foot
    with rasterio.open(D / "external/tiger_road_distance_m.tif") as s:
        road = s.read(1).astype(np.float64)
    with rasterio.open(ROOT / "work/E1_surface.tif") as s:
        surf = s.read(1)
    d_cat = distance_transform_edt(~labels)
    e1 = np.load(ROOT / "work/E1_mask.npy")
    eligible = (surf > 0) & foot & (d_cat > 2.0) & (road >= ROAD_MIN_M)
    mask = greedy_cover(np.where(eligible, surf, 0.0).astype(np.float32), eligible, BUDGET)
    mp = ROOT / "work/E3_mask.npy"
    np.save(mp, mask)
    meta = {"dots": int(mask.sum()), "road_min_m": ROAD_MIN_M,
            "e1_dots_within_100m_of_road": int((e1 & (road < ROAD_MIN_M)).sum()),
            "mask_sha256": hashlib.sha256(mp.read_bytes()).hexdigest(),
            "road_band_stats_m": {"min": float(np.nanmin(road[foot])),
                                  "median": float(np.nanmedian(road[foot])),
                                  "max": float(np.nanmax(road[foot]))}}
    (ROOT / "evidence/e3_build.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
