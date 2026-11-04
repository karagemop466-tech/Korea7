#!/usr/bin/env python3
"""Korea7 — GEMS Prize submission validator (automated gate, no human inspector).

Checks a candidate GeoTIFF against the submission format gates:
  * single band, float32
  * CRS / shape / geotransform match the reference raster when one is given,
    otherwise the pinned official competition grid (EPSG:32611, 3730x3292,
    transform (100, 0, 243350, 0, -100, 4508550))
  * all pixels finite and in [0, 1]; no nodata/masked pixels
  * reports SHA-256

`validate(candidate, reference=None)` returns a machine-readable dict and
never exits; the CLI prints JSON and exits non-zero on gate failure.
Passing this gate never authorizes submission by itself (`ready_to_submit`
is always False here; promotion is a separate selector step).

Usage:
  python3 scripts/validate_submission.py docs/downloads/<file>.tif [reference.tif]
"""
from __future__ import annotations

import hashlib
import json
import sys

import numpy as np
import rasterio

EXPECTED_HEIGHT = 3730
EXPECTED_WIDTH = 3292
EXPECTED_CRS = "EPSG:32611"
EXPECTED_TRANSFORM = [100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0]
EXPECTED_BANDS = 1
EXPECTED_DTYPE = "float32"


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(candidate, reference=None) -> dict:
    checks: dict[str, bool] = {}
    report = {"path": str(candidate), "checks": checks, "errors": [],
              "format_pass": False, "ready_to_submit": False, "sha256": ""}

    exp_crs, exp_shape = EXPECTED_CRS, (EXPECTED_HEIGHT, EXPECTED_WIDTH)
    exp_transform = EXPECTED_TRANSFORM
    if reference is not None:
        try:
            with rasterio.open(reference) as ref:
                exp_crs = ref.crs.to_string() if ref.crs is not None else None
                exp_shape = (ref.height, ref.width)
                exp_transform = list(ref.transform)[:6]
        except Exception as exc:  # noqa: BLE001
            report["errors"].append("reference open: " + repr(exc))
            return report

    try:
        ds = rasterio.open(candidate)
    except Exception as exc:  # noqa: BLE001
        report["errors"].append("open: " + repr(exc))
        return report

    with ds:
        report["sha256"] = sha256_file(candidate)
        checks["single_band"] = ds.count == EXPECTED_BANDS
        checks["dtype_float32"] = bool(ds.count) and ds.dtypes[0] == EXPECTED_DTYPE
        crs = ds.crs.to_string() if ds.crs is not None else None
        checks["crs_match"] = crs == exp_crs
        checks["shape_match"] = (ds.height, ds.width) == tuple(exp_shape)
        checks["transform_match"] = (
            [round(float(v), 6) for v in list(ds.transform)[:6]]
            == [round(float(v), 6) for v in exp_transform])
        band = ds.read(1, masked=True)
        checks["no_masked_or_nodata_pixels"] = (
            ds.nodata is None and not np.ma.is_masked(band))
        data = np.ma.getdata(band)
        finite = np.isfinite(data)
        report["n_nan_or_inf"] = int((~finite).sum())
        checks["all_pixels_finite"] = bool(finite.all())
        if finite.any():
            vals = data[finite]
            report["min_value"] = float(vals.min())
            report["max_value"] = float(vals.max())
            checks["values_in_0_to_1"] = bool(
                (vals >= 0.0).all() and (vals <= 1.0).all())
        else:
            checks["values_in_0_to_1"] = False

    report["format_pass"] = all(checks.values())
    for name, ok in checks.items():
        if not ok:
            report["errors"].append(name)
    return report


def main(argv) -> int:
    if len(argv) not in (2, 3):
        print("Usage: python3 scripts/validate_submission.py <file.tif> [reference.tif]",
              file=sys.stderr)
        return 2
    report = validate(argv[1], argv[2] if len(argv) == 3 else None)
    print(json.dumps(report, indent=2))
    return 0 if report["format_pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
