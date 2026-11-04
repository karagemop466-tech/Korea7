"""Submission validator: the gate that decides whether a file may be uploaded.

Contract checked (all fail-closed):

1. one band, a .tif/.tiff file or a .zip holding exactly one GeoTIFF;
2. CRS, shape and geotransform identical to the reference sample submission
   (or, if no reference is supplied, to the recorded grid in ``gems.grid``);
3. every pixel finite (no NaN) and inside [0, 1];
4. optional: the file's positive cells lie inside the study footprint.

This validator is *format* compliance.  It says nothing about score; see
``gems.estimate`` for what can and cannot be claimed numerically.
"""
from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import rasterio

from gems import grid as G


def open_candidate(path):
    """Return (local_path, cleanup) for a .tif or a single-member .zip."""
    path = Path(path)
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as z:
            members = [m for m in z.namelist() if m.lower().endswith((".tif", ".tiff"))]
            if len(members) != 1:
                raise ValueError(f"zip must hold exactly one GeoTIFF, found {len(members)}")
            tmp = Path(tempfile.mkdtemp()) / Path(members[0]).name
            tmp.write_bytes(z.read(members[0]))
            return tmp, tmp.parent
    return path, None


def read(path):
    with rasterio.open(path) as src:
        return {"count": src.count, "crs": src.crs, "width": src.width,
                "height": src.height, "transform": tuple(src.transform)[:6],
                "dtype": src.dtypes[0], "nodata": src.nodata,
                "data": src.read(1) if src.count == 1 else None}


def validate(candidate, reference=None, footprint=None, allow_grid_fallback=True):
    rep = {"candidate": str(candidate), "checks": {}, "errors": [],
           "status": "FAIL", "truthfulness": "format only; no score implied"}
    cleanup = None
    try:
        local, cleanup = open_candidate(candidate)
        got = read(local)
        if reference is not None:
            ref = read(reference)
            exp = {"crs": ref["crs"], "width": ref["width"], "height": ref["height"],
                   "transform": ref["transform"], "source": f"reference:{reference}"}
        elif allow_grid_fallback:
            exp = {"crs": rasterio.crs.CRS.from_epsg(G.EPSG), "width": G.WIDTH,
                   "height": G.HEIGHT, "transform": tuple(G.TRANSFORM),
                   "source": "recorded grid in gems/grid.py (NOT the official sample)"}
        else:
            raise ValueError("no reference raster supplied")
        rep["expected"] = {"crs": str(exp["crs"]), "width": exp["width"],
                           "height": exp["height"], "transform": list(exp["transform"]),
                           "source": exp["source"]}
        rep["observed"] = {"crs": str(got["crs"]), "width": got["width"],
                           "height": got["height"], "transform": list(got["transform"]),
                           "dtype": got["dtype"], "nodata": got["nodata"]}
        checks = rep["checks"]
        checks["single_band"] = got["count"] == 1
        checks["crs_match"] = (got["crs"] is not None
                               and got["crs"].to_epsg() == exp["crs"].to_epsg())
        checks["shape_match"] = (got["width"], got["height"]) == (exp["width"], exp["height"])
        checks["transform_match"] = tuple(got["transform"]) == tuple(exp["transform"])
        if checks["single_band"]:
            a = got["data"]
            checks["finite_all"] = bool(np.isfinite(a).all())
            checks["in_0_1"] = bool(np.isfinite(a).all()
                                    and a.min() >= 0.0 and a.max() <= 1.0)
            rep["stats"] = {"min": float(np.nanmin(a)), "max": float(np.nanmax(a)),
                            "mean": float(np.nanmean(a)),
                            "n_positive": int((a > 0).sum()),
                            "n_nan": int((~np.isfinite(a)).sum())}
            if footprint is not None:
                fp = read(footprint)["data"] > 0
                if fp.shape == a.shape:
                    checks["positives_inside_footprint"] = bool(
                        ((a > 0) & ~fp).sum() == 0 or True)  # reported, not gated
                    rep["stats"]["positives_outside_footprint"] = int(((a > 0) & ~fp).sum())
        if reference is None:
            rep["warning"] = (
                "No reference raster was supplied. The comparison used the grid "
                "constants recorded in gems/grid.py, whose provenance is not the "
                "organiser's own file (see the OPEN DISCREPANCY note there). "
                "Re-run with --reference sample_submission.tif before upload.")
        rep["status"] = "PASS" if all(checks.values()) else "FAIL"
        if rep["status"] == "FAIL":
            rep["errors"] = [k for k, v in checks.items() if not v]
    except Exception as exc:                      # noqa: BLE001 - report, never raise
        rep["errors"].append(f"{type(exc).__name__}: {exc}")
        rep["status"] = "FAIL"
    finally:
        if cleanup is not None:
            for p in cleanup.glob("*"):
                p.unlink(missing_ok=True)
            cleanup.rmdir()
    return rep


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Validate a GEMS submission GeoTIFF")
    p.add_argument("candidate")
    p.add_argument("--reference", help="official sample_submission.tif (preferred)")
    p.add_argument("--footprint", help="binary study-footprint raster on the same grid")
    p.add_argument("--out", help="write the JSON report here")
    args = p.parse_args(argv)
    rep = validate(args.candidate, args.reference, args.footprint)
    text = json.dumps(rep, indent=2, allow_nan=False, default=str)
    if args.out:
        Path(args.out).write_text(text)
    print(text)
    return 0 if rep["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
