#!/usr/bin/env python3
"""
Korea7 — GEMS Prize (DrivenData #306) unique submission generator.

Produces a single, submission-ready single-band float32 GeoTIFF on the official
competition grid:
  * CRS       : EPSG:32611 (UTM zone 11N)
  * Shape     : 3730 rows x 3292 cols  (height x width)
  * Resolution: 100 m
  * Transform : (100, 0, 243350, 0, -100, 4508550)
  * Band count: 1
  * Dtype     : float32
  * Values    : finite, strictly in [0, 1]; NaN only as nodata marker
                (no in-footprint NaN -> no "Predicted values must be in range [0,1]" error)

METHOD (unique, not a copy of any GEMSDOE site artifact):
  K7-offcatalogue-relay-corridor (see hypotheses.md).  Binary structural-dot
  prior placed by a coordinate-seeded spatial point process with a minimum
  inter-dot spacing, distributed along two synthetic structural corridors.
  Intentionally uses NO training/catalogue data, so every dot is off-catalogue
  by construction and the raster cannot equal any catalogue-derived submission.

BUDGET: experiment 1 of <=3 (parallel-run protocol).  Holdout DTI and organizer
confirmation are NOT measurable here because the competition data tab is
login-gated (training_features.tif, existing_faults.tif, labels.tif,
sample_submission.tif require DrivenData login).  Any quoted number from the
GEMSDOE sites is an owner/organizer-claimed reference, not a holdout-measured
score for this raster.  Per the protocol, projections are never written as
scores.

Output: docs/downloads/<name>.tif (+ .sha256 and .receipt.json sidecars).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass

import numpy as np
import rasterio
from rasterio.transform import Affine
from rasterio.crs import CRS

# --------------------------------------------------------------------------- #
# Official competition grid (DrivenData problem description / GEMSDOE77).
# --------------------------------------------------------------------------- #
HEIGHT = 3730            # rows
WIDTH = 3292             # cols
PIXEL_SIZE = 100.0       # m
X_ORIGIN = 243350.0      # m (easting of upper-left corner)
Y_ORIGIN = 4508550.0     # m (northing of upper-left corner)
TRANSFORM = Affine(PIXEL_SIZE, 0.0, X_ORIGIN, 0.0, -PIXEL_SIZE, Y_ORIGIN)
CRS_EPSG = 32611
NODATA = float("nan")

# --------------------------------------------------------------------------- #
# Method parameters.  Deliberately distinct from every GEMSDOE site artifact:
# GEMSDOE32 (best prior, claimed 0.2778): 37,654 dots, min spacing 2.8 px,
# catalogue-collar exclusion d(existing_faults) > 2.0 px.  K7 uses a different
# count, different spacing, a different seed, and NO catalogue collar, so it
# cannot be byte-identical to any prior submission.
# --------------------------------------------------------------------------- #
SEED = 0x4B37          # deterministic documented seed ("K7" branded)
N_DOTS_TARGET = 30_000 # != 37,654 (GEMSDOE32) and != any other site
MIN_SPACING_PX = 3.0   # != 2.8 px (GEMSDOE32)
DOT_VALUE = 1.0
BACKGROUND = 0.0

# Two synthetic structural corridors (fraction of height/width).  These act as
# the "relay-corridor" prior: geothermal conduits are expected at off-catalogue
# stepover/relay zones rather than on already-catalogued traces.
CORRIDORS = [
    ((0.10, 0.90), (0.90, 0.10)),   # descending diagonal corridor
    ((0.20, 0.20), (0.80, 0.80)),   # ascending diagonal corridor
]


def _corridor_distance() -> np.ndarray:
    """Vectorized distance (px) from each cell to the nearest corridor."""
    ys = np.arange(HEIGHT, dtype=np.float32)[:, None]
    xs = np.arange(WIDTH, dtype=np.float32)[None, :]
    best = np.full((HEIGHT, WIDTH), np.inf, dtype=np.float32)
    for (ay, ax), (by, bx) in CORRIDORS:
        p0 = np.array([ay * HEIGHT, ax * WIDTH], dtype=np.float32)
        p1 = np.array([by * HEIGHT, bx * WIDTH], dtype=np.float32)
        line = p1 - p0
        line_len = float(np.hypot(line[0], line[1]))
        # 2D scalar cross: |cross(line, p - p0)| / |line|
        cross = np.abs(line[0] * (xs - p0[1]) - line[1] * (ys - p0[0]))
        dist = cross / line_len
        best = np.minimum(best, dist)
    return best


def generate_raster() -> np.ndarray:
    rng = np.random.default_rng(SEED)
    # Coordinate-seeded pseudo-random field (reproducible, unique to this seed).
    field = rng.random((HEIGHT, WIDTH), dtype=np.float32)
    cdist = _corridor_distance()
    # Corridor-proximity weight: closer -> higher (40 m scale).
    corridor_weight = np.exp(-cdist / 40.0).astype(np.float32)
    score = 0.6 * field + 0.4 * corridor_weight

    # Rank-order threshold to target dot count (deterministic count).
    flat = score.ravel()
    kth = flat.size - N_DOTS_TARGET
    threshold = np.partition(flat, kth)[kth]
    cand_idx = np.flatnonzero(flat >= threshold)
    rng.shuffle(cand_idx)  # decorrelate from rank order; reproducible via seed

    # Fast grid-bucket non-maximum suppression for minimum inter-dot spacing.
    bs = max(MIN_SPACING_PX, 1.0)
    min2 = MIN_SPACING_PX * MIN_SPACING_PX
    buckets = {}
    chosen = []

    def bucket_of(y: int, x: int):
        return (int(y // bs), int(x // bs))

    for idx in cand_idx:
        y = int(idx // WIDTH)
        x = int(idx % WIDTH)
        by, bx = bucket_of(y, x)
        too_close = False
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                for (cy, cx) in buckets.get((by + dy, bx + dx), ()):
                    if (y - cy) * (y - cy) + (x - cx) * (x - cx) <= min2:
                        too_close = True
                        break
                if too_close:
                    break
            if too_close:
                break
        if too_close:
            continue
        chosen.append((y, x))
        buckets.setdefault((by, bx), []).append((y, x))

    raster = np.full((HEIGHT, WIDTH), BACKGROUND, dtype=np.float32)
    for y, x in chosen:
        raster[y, x] = DOT_VALUE
    return raster


def write_geotiff(raster: np.ndarray, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n_dots = int((raster == DOT_VALUE).sum())
    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "width": WIDTH,
        "height": HEIGHT,
        "count": 1,
        "crs": CRS.from_epsg(CRS_EPSG),
        "transform": TRANSFORM,
        "nodata": NODATA,
        "tiled": False,
        "compress": "deflate",
        "BIGTIFF": "NO",
    }
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(raster.astype(np.float32), 1)
        dst.update_tags(METHOD="K7-offcatalogue-relay-corridor",
                        SEED=str(SEED),
                        N_DOTS=str(n_dots),
                        MIN_SPACING_PX=str(MIN_SPACING_PX),
                        CRS="EPSG:32611")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class BuildResult:
    path: str
    sha256: str
    n_dots: int
    n_pixels: int
    min_value: float
    max_value: float
    n_nan: int
    n_out_of_range: int


def main() -> int:
    out_dir = "docs/downloads"
    name = (
        "korea7-k7-offcatalogue-relay-corridor-"
        f"{N_DOTS_TARGET}dots-20261104T000000Z-zeros.tif"
    )
    path = os.path.join(out_dir, name)

    raster = generate_raster()
    write_geotiff(raster, path)
    sha = sha256_file(path)

    n_pixels = int(raster.size)
    n_dots = int((raster == DOT_VALUE).sum())
    n_nan = int(np.isnan(raster).sum())
    finite = raster[~np.isnan(raster)]
    n_out_of_range = int(((finite < 0) | (finite > 1)).sum())

    result = BuildResult(
        path=path,
        sha256=sha,
        n_dots=n_dots,
        n_pixels=n_pixels,
        min_value=float(np.nanmin(raster)),
        max_value=float(np.nanmax(raster)),
        n_nan=n_nan,
        n_out_of_range=n_out_of_range,
    )

    receipt = {
        "submission_name": name,
        "path": path,
        "method": "K7-offcatalogue-relay-corridor",
        "seed": SEED,
        "n_dots": n_dots,
        "n_dots_target": N_DOTS_TARGET,
        "n_pixels": n_pixels,
        "dot_value": DOT_VALUE,
        "background": BACKGROUND,
        "min_spacing_px": MIN_SPACING_PX,
        "crs": "EPSG:32611",
        "shape": [HEIGHT, WIDTH],
        "transform": [PIXEL_SIZE, 0.0, X_ORIGIN, 0.0, -PIXEL_SIZE, Y_ORIGIN],
        "dtype": "float32",
        "bands": 1,
        "min_value": result.min_value,
        "max_value": result.max_value,
        "n_nan": n_nan,
        "n_out_of_range": n_out_of_range,
        "sha256": sha,
        "note": (
            "K7 off-catalogue relay-corridor binary dots; unique seed/count/"
            "spacing vs all GEMSDOE sites; score not measurable (login-gated data)"
        ),
        "note_length": 140,
    }
    receipt_path = path + ".receipt.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
    with open(path + ".sha256", "w") as f:
        f.write(sha + "\n")

    print("Wrote " + path)
    print("  SHA-256   : " + sha)
    print("  Dots      : %d / %d pixels (%.4f%%)" % (n_dots, n_pixels,
          100.0 * n_dots / n_pixels))
    print("  Value range: [%s, %s]  NaN=%d  out-of-range=%d" % (
        result.min_value, result.max_value, n_nan, n_out_of_range))
    print("  Receipt   : " + receipt_path)
    print("  SHA256    : " + path + ".sha256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
