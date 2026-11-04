"""Verified competition grid constants.

Provenance (see docs/verification.md for the line-by-line audit):

* EPSG:32611 (WGS 84 / UTM zone 11N) and 100 m pixel size are stated in the
  official DrivenData reference notebook, cell 7, which titles its figure
  "Various numeric features (EPSG:32611, 100m resolution)".
  https://github.com/drivendataorg/gems-prize-reference-solution
* The full affine transform, width 3292 and height 3730 were read with
  rasterio from a GeoTIFF published on GitHub that is declared to be in the
  competition submission format.  They are cross-checked here against the
  reference notebook's 100 m EPSG:32611 statement and against the published
  bounds of the GeoDAWN study area (western Nevada / eastern California).

The constants are NOT taken on trust by the validator: `validate.py` always
compares a candidate against a user-supplied reference raster (the official
`sample_submission.tif`) when one is available and only falls back to these
constants for reporting.
"""

#: CRS of the competition grid.
EPSG = 32611

#: Pixel size in metres (square pixels).
PIXEL_M = 100.0

#: Raster width (columns) and height (rows), in pixels.
WIDTH = 3292
HEIGHT = 3730

#: Affine transform: (a, b, c, d, e, f) = (pixel_w, 0, x_min, 0, -pixel_h, y_max).
TRANSFORM = (100.0, 0.0, 250000.0, 0.0, -100.0, 4520000.0)

#: Bounds in projected metres: (left, bottom, right, top).
BOUNDS = (250000.0, 4147000.0, 579200.0, 4520000.0)

#: Number of pixels on the grid.
N_PIXELS = WIDTH * HEIGHT

#: Metric constants from the published problem description.
ALPHA = 0.2   # weight on false positives
BETA = 0.8    # weight on false negatives
RADIUS_M = 300.0
RADIUS_PX = RADIUS_M / PIXEL_M  # == 3.0


def describe():
    """Return the grid as a plain dict, for JSON reports."""
    return {
        "epsg": EPSG,
        "pixel_m": PIXEL_M,
        "width": WIDTH,
        "height": HEIGHT,
        "transform": list(TRANSFORM),
        "bounds": list(BOUNDS),
        "n_pixels": N_PIXELS,
        "alpha": ALPHA,
        "beta": BETA,
        "radius_m": RADIUS_M,
        "radius_px": RADIUS_PX,
    }
