#!/usr/bin/env python3
"""Write a small SYNTHETIC dataset in the competition's file format.

This exists so the whole pipeline (features -> holdout -> model -> emission ->
writer -> validator) can be integration-tested without the gated DrivenData
files.  Nothing produced from it is a submission: the rasters are simulated,
not observations.

    python scripts/make_demo_data.py --out demo --size 700x800
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import Affine
from scipy import ndimage as ndi

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gems import network as N  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="demo")
    ap.add_argument("--size", default="700x800", help="HEIGHTxWIDTH")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)
    h, w = (int(v) for v in args.size.lower().split("x"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    faults = N.make_calibrated_network(shape=(h, w), seed=args.seed)
    transform = Affine(100.0, 0.0, 250000.0, 0.0, -100.0, 4520000.0)
    # three synthetic bands whose lineament structure follows the faults
    bands = []
    for k, blur in enumerate((1.2, 2.0, 3.2)):
        signal = ndi.gaussian_filter(faults, blur) * (6.0 - k)
        texture = ndi.gaussian_filter(rng.normal(size=(h, w)), 6.0) * 0.6
        bands.append((signal + texture + rng.normal(0, 0.15, (h, w))).astype(np.float32))
    prof = dict(driver="GTiff", height=h, width=w, count=len(bands),
                dtype="float32", crs="EPSG:32611", transform=transform,
                compress="deflate")
    with rasterio.open(out / "numeric_features.tif", "w", **prof) as dst:
        for i, b in enumerate(bands, start=1):
            dst.write(b, i)
            dst.update_tags(i, description=f"DEMO synthetic band {i}", data_category="demo")
    with rasterio.open(out / "labels.tif", "w", **{**prof, "count": 1}) as dst:
        dst.write(faults.astype(np.float32), 1)
        dst.update_tags(1, description="DEMO synthetic faults", data_category="demo")
    with rasterio.open(out / "sample_submission.tif", "w",
                       **{**prof, "count": 1}) as dst:
        dst.write(np.zeros((h, w), np.float32), 1)
    print(f"wrote synthetic dataset to {out}/ ({h}x{w}, {len(bands)} bands) - NOT competition data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
