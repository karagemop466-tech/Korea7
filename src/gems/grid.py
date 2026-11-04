"""Competition-grid I/O and the offline submission format gate.

Grid facts are measured from the official ``sample_submission.tif`` shipped in
``data/reference/`` and are asserted in ``tests/test_grid.py`` rather than trusted:

    CRS        EPSG:32611 (WGS84 / UTM zone 11N)
    shape      3730 rows x 3292 cols
    transform  origin (243350.0, 4508550.0), 100 m pixels, north-up
    values     official sample: 1.0 on the 60,988 catalogue fault pixels,
               0.0 elsewhere inside the footprint, NaN in the 7,111,787
               pixels outside it.

The official sample itself therefore establishes the accepted convention:
finite values in [0, 1] inside the footprint and NaN outside it.  The portal
rejection "Predicted values must be in range [0, 1]" that the owner reported is
what happens when NaN or the -3.4e38 float32 sentinel survives *inside* the
footprint; see docs/portal-error.md for the line-by-line argument.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

EXPECTED_CRS = "EPSG:32611"
EXPECTED_HEIGHT = 3730
EXPECTED_WIDTH = 3292
EXPECTED_TRANSFORM = (100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0)
EXPECTED_FOOTPRINT_PIXELS = 5_167_373
EXPECTED_CATALOGUE_PIXELS = 60_988

REFERENCE_DIR = Path(__file__).resolve().parents[2] / "data" / "reference"
SAMPLE_SUBMISSION = REFERENCE_DIR / "sample_submission.tif"
LABELS = REFERENCE_DIR / "labels.tif"


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def grid_signature(path: str | Path) -> dict:
    with rasterio.open(path) as src:
        return {
            "crs": str(src.crs),
            "height": src.height,
            "width": src.width,
            "count": src.count,
            "dtype": src.dtypes[0],
            "transform": tuple(src.transform)[:6],
            "driver": src.driver,
        }


def read_grid(path: str | Path, *, dtype=np.float64) -> np.ndarray:
    """Read band 1 of a raster that must sit exactly on the competition grid."""
    with rasterio.open(path) as src:
        if (src.height, src.width) != (EXPECTED_HEIGHT, EXPECTED_WIDTH):
            raise ValueError(f"{path}: shape {(src.height, src.width)} != competition grid")
        if tuple(src.transform)[:6] != EXPECTED_TRANSFORM:
            raise ValueError(f"{path}: transform does not match the competition grid")
        if str(src.crs) != EXPECTED_CRS:
            raise ValueError(f"{path}: CRS {src.crs} != {EXPECTED_CRS}")
        return src.read(1).astype(dtype)


def load_reference() -> dict:
    """Return the footprint, the catalogue mask and the official template."""
    with rasterio.open(SAMPLE_SUBMISSION) as src:
        sample = src.read(1).astype(np.float64)
    with rasterio.open(LABELS) as src:
        labels = src.read(1).astype(np.int8)
    footprint = np.isfinite(sample)
    catalogue = labels == 1
    return {
        "sample": sample,
        "labels": labels,
        "footprint": footprint,
        "catalogue": catalogue,
        "valid": footprint,          # labels != -1 exactly equals finite sample
    }


def write_like(template: str | Path, array: np.ndarray, out: str | Path) -> Path:
    """Write ``array`` as a single-band float32 GeoTIFF on the template's grid.

    Outside-footprint pixels are written as NaN, exactly matching the official
    sample submission convention, unless the caller has already supplied 0.0.
    """
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(template) as tpl:
        profile = tpl.profile
    # No nodata value is declared: every cell holds a real number in [0, 1], so there is
    # nothing to mask and no sentinel that a range check could trip over.  (The official
    # sample declares nodata=nan and uses NaN outside the footprint; both are accepted, and
    # declaring nothing is the strictly safer of the two.)
    profile.update(driver="GTiff", count=1, dtype="float32", nodata=None,
                   tiled=True, blockxsize=256, blockysize=256,
                   compress="deflate", predictor=2)
    data = np.asarray(array, dtype=np.float32)
    if data.shape != (EXPECTED_HEIGHT, EXPECTED_WIDTH):
        raise ValueError(f"array shape {data.shape} does not match the competition grid")
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(data, 1)
        dst.set_band_description(1, "fault probability")
    return out


def format_gate(path: str | Path) -> dict:
    """Offline form of the portal's own acceptance rules.  Never approves on its own."""
    out = {
        "path": str(path),
        "checks": {},
        "format_pass": False,
        "ready_to_submit": False,
        "note": "Format gate only. Promotion also requires the uniqueness and holdout gates.",
    }
    try:
        out["sha256"] = sha256(path)
        with rasterio.open(path) as src:
            finite = in_range = True
            nan_inside = 0
            with rasterio.open(SAMPLE_SUBMISSION) as tpl:
                foot = np.isfinite(tpl.read(1))
            for _, window in src.block_windows(1):
                block = src.read(1, window=window, masked=False)
                inside = foot[window.row_off:window.row_off + window.height,
                              window.col_off:window.col_off + window.width]
                if block.shape != inside.shape:
                    raise ValueError("window/array shape mismatch")
                vals = block[inside]
                finite &= bool(np.isfinite(vals).all())
                nan_inside += int((~np.isfinite(vals)).sum())
                if np.isfinite(vals).any():
                    in_range &= bool(((vals[np.isfinite(vals)] >= 0)
                                      & (vals[np.isfinite(vals)] <= 1)).all())
            out["checks"] = {
                "geotiff": src.driver == "GTiff",
                "single_band": src.count == 1,
                "crs_match": str(src.crs) == EXPECTED_CRS,
                "shape_match": (src.height, src.width) == (EXPECTED_HEIGHT, EXPECTED_WIDTH),
                "transform_match": tuple(src.transform)[:6] == EXPECTED_TRANSFORM,
                "footprint_pixels_finite": bool(finite),
                "footprint_pixels_in_0_1": bool(in_range),
            }
            out["nonfinite_pixels_inside_footprint"] = int(nan_inside)
            out["format_pass"] = all(out["checks"].values())
    except (OSError, ValueError, rasterio.errors.RasterioError) as exc:
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out
