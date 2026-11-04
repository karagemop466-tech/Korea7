"""Submission validator and writer.

Implements the gate stated in the README.  A file is reported ``OK TO SUBMIT``
only when every check passes against the organiser template verified in this
checkout.  The portal error the project owner hit --
``Predicted values must be in range [0, 1]`` -- is caused by NaN/Inf or values
outside the closed interval and is checked for explicitly, both inside and
outside the footprint.
"""

from __future__ import annotations

import hashlib
import io
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import rasterio

from .grid import CRS_EPSG, HEIGHT, TOTAL_CELLS, WIDTH, TRANSFORM, SAMPLE_SUBMISSION


@dataclass
class ValidationResult:
    checks: list[tuple[str, bool, str]] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append((name, bool(ok), detail))

    @property
    def passed(self) -> bool:
        return all(ok for _, ok, _ in self.checks)

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "n_checks": len(self.checks),
            "n_passed": sum(1 for _, ok, _ in self.checks if ok),
            "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in self.checks],
        }


def validate_raster(path: Path | str, template: Path | None = None, array: np.ndarray | None = None) -> ValidationResult:
    """Run the full 10-point gate on a GeoTIFF (or on an in-memory array)."""
    path = Path(path)
    template = Path(template or SAMPLE_SUBMISSION)
    r = ValidationResult()

    with rasterio.open(template) as t:
        t_crs, t_shape, t_transform = t.crs, t.shape, t.transform
        t_foot = np.isfinite(t.read(1))
        t_foot_cells = int(t_foot.sum())

    if array is not None:
        arr, crs, transform, shape, count, dtype = array, t_crs, t_transform, array.shape, 1, array.dtype
    else:
        if not path.exists():
            r.add("file_exists", False, "file not found")
            return r
        r.add("file_exists", True, f"{path.stat().st_size} bytes")
        with rasterio.open(path) as ds:
            count, shape, crs, transform, dtype = ds.count, ds.shape, ds.crs, ds.transform, ds.dtypes[0]
            arr = ds.read(1)

    r.add("single_band", count == 1, f"count={count}")
    r.add("shape", shape == t_shape, f"{shape} vs template {t_shape}")
    r.add("crs", crs is not None and crs.to_epsg() == CRS_EPSG, f"{crs}")
    r.add(
        "transform",
        tuple(round(v, 6) for v in transform.to_gdal()) == TRANSFORM,
        f"{tuple(round(v, 6) for v in transform.to_gdal())}",
    )
    r.add("dtype_float32", np.dtype(dtype) == np.dtype("float32"), f"{dtype}")

    if shape != t_shape:
        # Shape-independent checks still run; footprint comparisons cannot.
        finite = np.isfinite(arr)
        r.add("no_nan_or_inf", bool(finite.all()), f"{int((~finite).sum())} non-finite cells")
        if finite.any():
            lo_, hi_ = float(np.nanmin(arr)), float(np.nanmax(arr))
            r.add("values_in_0_1", bool(lo_ >= 0.0 and hi_ <= 1.0), f"min={lo_:.6g} max={hi_:.6g}")
        r.add("outside_footprint_clean", False, "skipped: grid does not match the template")
        r.add("all_dots_inside_footprint", False, "skipped: grid does not match the template")
        r.add("nonzero_prediction", bool((np.nan_to_num(arr) > 0).any()), "shape-independent")
        return r

    finite = np.isfinite(arr)
    n_nan = int((~finite).sum())
    r.add("no_nan_or_inf", n_nan == 0, f"{n_nan} non-finite cells")

    lo, hi = float(np.nanmin(arr)) if finite.any() else float("nan"), float(np.nanmax(arr)) if finite.any() else float("nan")
    r.add("values_in_0_1", bool(finite.all() and lo >= 0.0 and hi <= 1.0), f"min={lo:.6g} max={hi:.6g}")

    # Outside the footprint the organiser accepts "null or nan".  A filled 0 is
    # strictly safer than NaN: a stray NaN is what produces the portal error
    # "Predicted values must be in range [0, 1]".  Both conventions pass, and
    # the choice is reported so the file is self-describing.
    outside = ~t_foot
    n_zero_out = int((arr[outside] == 0).sum())
    n_nan_out = int((~np.isfinite(arr[outside])).sum())
    outside_clean = (n_zero_out + n_nan_out) == int(outside.sum())
    convention = "zeros" if n_nan_out == 0 else ("nan" if n_zero_out == 0 else "mixed")
    r.add("outside_footprint_clean", outside_clean,
          f"convention={convention}; {n_zero_out} zeros / {n_nan_out} nan outside footprint")

    n_emit = int((arr > 0).sum())
    n_emit_outside = int(((arr > 0) & ~t_foot).sum())
    r.add("all_dots_inside_footprint", n_emit_outside == 0, f"{n_emit_outside} dots outside footprint")
    r.add("binary_emission", bool(np.isin(arr[arr > 0], [1.0]).all()) if n_emit else True,
          f"{n_emit} dots, distinct values={np.unique(arr).size}")

    r.add("nonzero_prediction", n_emit > 0, f"{n_emit} dots")
    return r


def write_submission(mask: np.ndarray, out_path: Path | str, template: Path | None = None) -> dict:
    """Write a single-band float32 GeoTIFF matching the organiser template exactly."""
    template = Path(template or SAMPLE_SUBMISSION)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    mask = np.asarray(mask, bool)
    if mask.shape != (HEIGHT, WIDTH):
        raise ValueError(f"mask must be {HEIGHT}x{WIDTH}, got {mask.shape}")

    with rasterio.open(template) as t:
        foot = np.isfinite(t.read(1))
        crs, transform = t.crs, t.transform
        profile = t.profile.copy()

    if (mask & ~foot).any():
        raise ValueError(f"{int((mask & ~foot).sum())} dots fall outside the organiser footprint")

    arr = (mask & foot).astype(np.float32)
    profile.update(driver="GTiff", count=1, dtype="float32", nodata=None, compress="deflate",
                   tiled=True, blockxsize=256, blockysize=256)
    profile.pop("photometric", None)

    with rasterio.open(out_path, "w", **profile) as ds:
        ds.write(arr, 1)
        ds.update_tags(PURPOSE="DOE GEMS unmapped-fault prospectivity")
        band = {"description": "Korea7 HALO-32k catalogue-silent lattice", "data_category": "prediction"}
        ds.update_tags(1, **band)

    return {
        "path": str(out_path),
        "bytes": out_path.stat().st_size,
        "sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
        "dots": int(arr.sum()),
    }


def make_zip(tif_path: Path, zip_path: Path | None = None) -> dict:
    """Bundle the GeoTIFF into a single-member ZIP (the portal accepts either)."""
    tif_path = Path(tif_path)
    zip_path = Path(zip_path) if zip_path else tif_path.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(tif_path, arcname=tif_path.name)
    return {
        "path": str(zip_path),
        "bytes": zip_path.stat().st_size,
        "sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
        "members": zipfile.ZipFile(zip_path).namelist(),
    }
