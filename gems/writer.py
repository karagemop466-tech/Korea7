"""Write a submission GeoTIFF that cannot be malformed.

The writer refuses rather than repairs: shape, CRS, transform, finiteness and
the [0, 1] range are all checked before a byte is written, and the file is
read back and re-checked afterwards.  The most common real-world failure on
the submission form ("Predicted values must be in range [0, 1]") is caused by
NaN written into the raster; here NaN is simply not allowed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import Affine

from gems import grid as G


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_array(arr, name="array"):
    a = np.asarray(arr)
    if a.ndim != 2:
        raise ValueError(f"{name}: expected a 2-D array, got shape {a.shape}")
    a = a.astype(np.float32)
    if not np.isfinite(a).all():
        n = int((~np.isfinite(a)).sum())
        raise ValueError(f"{name}: {n} non-finite values; the submission form "
                         "rejects them ('Predicted values must be in range [0, 1]')")
    if a.min() < 0.0 or a.max() > 1.0:
        raise ValueError(f"{name}: values outside [0,1]: min {a.min()}, max {a.max()}")
    return a


def make_profile(width=None, height=None, transform=None, epsg=None, compress="deflate"):
    return {
        "driver": "GTiff",
        "dtype": "float32",
        "count": 1,
        "height": int(height if height is not None else G.HEIGHT),
        "width": int(width if width is not None else G.WIDTH),
        "crs": rasterio.crs.CRS.from_epsg(int(epsg if epsg is not None else G.EPSG)),
        "transform": Affine(*transform) if transform is not None else Affine(*G.TRANSFORM),
        "nodata": None,
        "compress": compress,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
    }


def write_submission(path, arr, profile=None, verify=True):
    """Write ``arr`` as a single-band float32 GeoTIFF and return a report."""
    a = check_array(arr)
    prof = dict(profile or make_profile())
    if a.shape != (prof["height"], prof["width"]):
        raise ValueError(f"array shape {a.shape} does not match profile "
                         f"{(prof['height'], prof['width'])}")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(path, "w", **prof) as dst:
        dst.write(a, 1)
        dst.update_tags(ALGORITHM="see docs/method.md", UNITS="probability of fault")
    report = {"path": str(path), "sha256": sha256(path),
              "bytes": path.stat().st_size,
              "profile": {"width": prof["width"], "height": prof["height"],
                          "epsg": prof["crs"].to_epsg(),
                          "transform": list(prof["transform"])[:6]}}
    if verify:
        with rasterio.open(path) as src:
            back = src.read(1)
            checks = {
                "single_band": src.count == 1,
                "crs_match": src.crs.to_epsg() == prof["crs"].to_epsg(),
                "shape_match": (src.width, src.height) == (prof["width"], prof["height"]),
                "transform_match": tuple(src.transform)[:6] == tuple(prof["transform"])[:6],
                "finite": bool(np.isfinite(back).all()),
                "in_0_1": bool(back.min() >= 0.0 and back.max() <= 1.0),
            }
        report["checks"] = checks
        if not all(checks.values()):
            raise RuntimeError(f"written file failed read-back verification: {checks}")
    return report


def zero_probe(path, **kw):
    """A format probe: a valid, unique, useless raster (every value 0.0).

    Its expected DTI is exactly 0: TP_w = 0 forces the numerator to zero.
    Use it only to prove the submission form accepts our file format.
    """
    prof = make_profile(**kw)
    arr = np.zeros((prof["height"], prof["width"]), dtype=np.float32)
    return write_submission(path, arr, profile=prof)
