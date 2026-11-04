"""Competition grid constants and template loading.

Verified locally from ``data/sample_submission.tif`` (SHA-256
``2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc``):

    driver      GTiff, single band, float32
    CRS         EPSG:32611  (WGS 84 / UTM zone 11N - https://epsg.io/32611)
    size        3292 x 3730  (width x height)
    transform   100 m, origin (243350.0, 4508550.0), -100 m north-up
    nodata      NaN; pixel-exact footprint of 5,167,373 valid cells
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

WIDTH, HEIGHT = 3292, 3730
TOTAL_CELLS = WIDTH * HEIGHT
CRS_EPSG = 32611
PIXEL_M = 100.0
TRANSFORM = (243350.0, 100.0, 0.0, 4508550.0, 0.0, -100.0)
FOOTPRINT_CELLS = 5_167_373
CATALOGUE_POSITIVES = 60_988
CATALOGUE_COMPONENTS = 3_199

SAMPLE_SUBMISSION = DATA / "sample_submission.tif"
LABELS = DATA / "labels.tif"

SAMPLE_SHA256 = "2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc"
LABELS_SHA256 = "7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093"


@dataclass(frozen=True)
class Grid:
    footprint: np.ndarray  # bool, True where the organiser footprint is valid
    truth: np.ndarray      # bool, catalogue fault pixels inside the footprint
    crs: object
    transform: object
    shape: tuple[int, int]

    @property
    def n_footprint(self) -> int:
        return int(self.footprint.sum())

    @property
    def n_truth(self) -> int:
        return int(self.truth.sum())


def load_grid(sample_path: Path | None = None, labels_path: Path | None = None) -> Grid:
    """Load the organiser footprint and the catalogue fault labels."""
    sample_path = sample_path or SAMPLE_SUBMISSION
    labels_path = labels_path or LABELS
    with rasterio.open(sample_path) as ds:
        foot = np.isfinite(ds.read(1)) & (ds.read_masks(1) > 0)
        crs, transform, shape = ds.crs, ds.transform, ds.shape
    with rasterio.open(labels_path) as ds:
        if (ds.crs, ds.shape, ds.transform) != (crs, shape, transform):
            raise ValueError("labels.tif grid does not match sample_submission.tif")
        raw = ds.read(1)
    truth = (raw > 0) & foot
    return Grid(footprint=foot, truth=truth, crs=crs, transform=transform, shape=shape)


def verify_pins() -> dict:
    """Re-hash the tracked data files and compare with the pinned digests."""
    import hashlib

    out = {}
    for name, path, pin in (
        ("sample_submission.tif", SAMPLE_SUBMISSION, SAMPLE_SHA256),
        ("labels.tif", LABELS, LABELS_SHA256),
    ):
        if not path.exists():
            out[name] = {"present": False, "pinned": pin}
            continue
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        out[name] = {"present": True, "sha256": h, "pinned": pin, "match": h == pin}
    return out
