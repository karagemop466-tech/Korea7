#!/usr/bin/env python3
"""
Korea7 — GEMS Prize submission validator.

Checks a candidate GeoTIFF against the official submission format gates:
  * single band, float32
  * CRS == EPSG:32611
  * shape == (3730, 3292)
  * transform == (100, 0, 243350, 0, -100, 4508550)
  * all in-footprint values finite and in [0, 1]
  * no NaN inside the footprint
  * reports SHA-256

This is the automated gate that replaces any human inspector.  It prints a
machine-readable JSON report to stdout and exits non-zero on any gate failure.

Usage:
  python3 scripts/validate_submission.py docs/downloads/<file>.tif
"""

from __future__ import annotations

import hashlib
import json
import sys

import numpy as np
import rasterio
from rasterio.crs import CRS

# Official competition grid (DrivenData problem description / GEMSDOE77).
EXPECTED_HEIGHT = 3730
EXPECTED_WIDTH = 3292
EXPECTED_CRS = "EPSG:32611"
EXPECTED_TRANSFORM = [100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0]
EXPECTED_DTYPE = "float32"
EXPECTED_BANDS = 1


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(path: str) -> dict:
    report = {"path": path, "passed": True, "gates": [], "errors": []}

    def gate(name: str, ok: bool, detail: str = "") -> None:
        report["gates"].append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            report["passed"] = False
            report["errors"].append(name + ": " + detail)

    try:
        ds = rasterio.open(path)
    except Exception as exc:  # noqa: BLE001
        report["passed"] = False
        report["errors"].append("open: " + repr(exc))
        print(json.dumps(report, indent=2))
        sys.exit(1)

    report["driver"] = ds.driver
    report["width"] = ds.width
    report["height"] = ds.height
    report["count"] = ds.count
    report["dtype"] = ds.dtypes[0] if ds.count else None
    report["crs"] = ds.crs.to_string() if ds.crs is not None else None
    report["transform"] = list(ds.transform)[:6]
    report["nodata"] = ds.nodata
    report["bounds"] = list(ds.bounds)
    report["sha256"] = sha256_file(path)

    gate("single_band", ds.count == EXPECTED_BANDS,
         "count=%d" % ds.count)
    gate("dtype_float32", ds.dtypes[0] == EXPECTED_DTYPE if ds.count else False,
         "dtype=%s" % (ds.dtypes[0] if ds.count else None))
    gate("crs_epsg32611", report["crs"] == EXPECTED_CRS,
         "crs=%s" % report["crs"])
    gate("shape_3730x3292", (ds.height, ds.width) == (EXPECTED_HEIGHT, EXPECTED_WIDTH),
         "shape=(%d,%d)" % (ds.height, ds.width))
    gate("transform_match", [round(float(v), 6) for v in ds.transform[:6]] ==
         [round(float(v), 6) for v in EXPECTED_TRANSFORM],
         "transform=%s" % report["transform"])

    band = ds.read(1)  # float32 array
    finite_mask = np.isfinite(band)
    n_total = int(band.size)
    n_nan = int((~np.isfinite(band)).sum())
    report["n_pixels"] = n_total
    report["n_nan"] = n_nan
    report["n_finite"] = int(finite_mask.sum())

    gate("no_nan_inside_footprint", n_nan == 0,
         "n_nan=%d" % n_nan)

    if finite_mask.any():
        finite_vals = band[finite_mask]
        vmin = float(np.nanmin(finite_vals))
        vmax = float(np.nanmax(finite_vals))
        n_out_of_range = int(((finite_vals < 0.0) | (finite_vals > 1.0)).sum())
        report["min_value"] = vmin
        report["max_value"] = vmax
        report["n_out_of_range"] = n_out_of_range
        gate("values_in_0_to_1", n_out_of_range == 0,
             "range=[%s,%s] out_of_range=%d" % (vmin, vmax, n_out_of_range))
    else:
        report["min_value"] = None
        report["max_value"] = None
        report["n_out_of_range"] = None
        gate("values_in_0_to_1", False, "no finite values")

    ds.close()

    print(json.dumps(report, indent=2))
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_submission.py <file.tif>", file=sys.stderr)
        sys.exit(2)
    validate(sys.argv[1])
