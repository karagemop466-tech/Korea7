"""Acquisition and warping of official, free external layers onto the competition grid.

Provenance of every layer used here
-----------------------------------
INGENIOUS regional data, hosted on the Geothermal Data Repository as GDR submission
1391 (DOI 10.15121/1881483, CC BY 4.0) and mirrored on GitHub in
``jklinck/geothermal_research`` (the mirror's README states the same two sources).
The mirror exists because gdr.openei.org is not reachable from this sandbox; the
bytes are fetched from GitHub, and each file's SHA-256 is recorded in
``evidence/external_layers.json`` so a reviewer can re-fetch and compare.

The organisers permit additional data sources provided the participant holds a
licence that permits use and sharing with the sponsor (competition problem
description, "External datasets").  CC BY 4.0 satisfies that; attribution is in
docs/sources.md.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject

from . import grid

MIRROR = "jklinck/geothermal_research"
MIRROR_README = "https://github.com/jklinck/geothermal_research"
RAW = "https://api.github.com/repos/{repo}/contents/{path}"

#: Official INGENIOUS layers used by this project.  Only layers that the
#: competition's own 19-band stack does NOT already expose are used for candidate
#: generation; see docs/hypotheses.md.
LAYERS = {
    "seis_n200a15": {
        "path": ("seismicity_INGENIOUS_regional_data/independent_eq/geotiffs/"
                 "ieq_n200a15.tif"),
        "what": ("INGENIOUS *independent* (declustered) earthquake rate-density grid, "
                 "variant ieq_n200a15, 500 m, NAD83 Contiguous USA Albers (CM 117)"),
        "caveat": ("The filename token semantics (n200 / a15) are not documented in the "
                   "mirror; treated as an ordinal seismic-activity density only."),
    },
    "seis_n100a05": {
        "path": ("seismicity_INGENIOUS_regional_data/independent_eq/geotiffs/"
                 "ieq_n100a05.tif"),
        "what": "INGENIOUS declustered earthquake rate-density grid, variant ieq_n100a05",
        "caveat": "Same undocumented token semantics as seis_n200a15.",
    },
}

CACHE = Path(__file__).resolve().parents[2] / ".cache" / "external"
EVIDENCE = Path(__file__).resolve().parents[2] / "evidence" / "external_layers.json"


def _download(path: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = RAW.format(repo=MIRROR, path=path)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.raw",
        "User-Agent": "korea7-gems-research",
    })
    with urllib.request.urlopen(req, timeout=600) as resp, open(dest, "wb") as f:
        while True:
            block = resp.read(1 << 20)
            if not block:
                break
            f.write(block)
    if dest.stat().st_size < 1024:
        raise OSError(f"{path}: suspiciously small download ({dest.stat().st_size} bytes)")
    return dest


def warp_to_competition_grid(src_path: str | Path) -> tuple[np.ndarray, dict]:
    """Reproject an external raster onto the competition grid, bilinear, NaN outside."""
    with rasterio.open(src_path) as src:
        dst_transform = rasterio.Affine(*grid.EXPECTED_TRANSFORM)
        dst = np.full((grid.EXPECTED_HEIGHT, grid.EXPECTED_WIDTH), np.nan, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,
            dst_transform=dst_transform,
            dst_crs=grid.EXPECTED_CRS,
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
        )
        info = {
            "source": str(src_path),
            "source_crs": str(src.crs),
            "source_shape": [src.height, src.width],
            "source_res": list(src.res),
            "source_nodata": src.nodata,
            "source_bounds": [float(v) for v in src.bounds],
        }
    return dst, info


def finite_fraction_inside(arr: np.ndarray, footprint: np.ndarray) -> float:
    return float(np.isfinite(arr[footprint]).mean())


def build(layer: str, footprint: np.ndarray, *, force: bool = False) -> dict:
    spec = LAYERS[layer]
    src = _download(spec["path"], CACHE / Path(spec["path"]).name)
    arr, info = warp_to_competition_grid(src)
    frac = finite_fraction_inside(arr, footprint)
    if frac < 0.50:
        raise ValueError(f"{layer}: only {frac:.1%} of the footprint received finite values; "
                         "the layer does not cover the study region")
    url = f"https://github.com/{MIRROR}/blob/main/{spec['path']}"
    return {
        "layer": layer,
        "array": arr,
        "covers_footprint_fraction": frac,
        "sha256_source_file": grid.sha256(src),
        "bytes": src.stat().st_size,
        "upstream": MIRROR,
        "upstream_repo_url": MIRROR_README,
        "upstream_file_url": url,
        "official_source": "GDR submission 1391 (DOI 10.15121/1881483), CC BY 4.0",
        "what": spec["what"],
        "caveat": spec["caveat"],
        **info,
    }


def write_receipt(records: list[dict], footprint: np.ndarray) -> None:
    EVIDENCE.parent.mkdir(exist_ok=True)
    out_path = EVIDENCE
    payload = {
        "generated_utc": "2026-11-04",
        "note": ("External bytes are fetched from a GitHub mirror of GDR submission 1391 because "
                 "gdr.openei.org is not reachable from this sandbox. SHA-256 of the fetched file is "
                 "recorded so a reviewer can verify the same bytes."),
        "layers": [],
    }
    if out_path.exists():
        payload["layers"] = json.loads(out_path.read_text()).get("layers", [])
    for rec in records:
        rec = {k: v for k, v in rec.items() if k != "array"}
        payload["layers"] = [r for r in payload["layers"] if r.get("layer") != rec["layer"]]
        payload["layers"].append(rec)
    out_path.write_text(json.dumps(payload, indent=2) + "\n")


CACHE_NPY = CACHE


def load_on_grid(layer: str, footprint: np.ndarray, *, refresh: bool = False) -> np.ndarray:
    """Return ``layer`` warped to the competition grid, building and caching it if needed.

    Self-healing: a fresh clone has no ``.cache``, so the layer is fetched from the mirror and
    warped on first use.  The SHA-256 of the fetched source file is written to
    ``evidence/external_layers.json`` on every build, so the provenance is reproducible.
    """
    cached = CACHE / f"{layer}_grid.npy"
    if cached.exists() and not refresh:
        arr = np.load(cached)
        if arr.shape == (grid.EXPECTED_HEIGHT, grid.EXPECTED_WIDTH):
            return arr
    rec = build(layer, footprint, force=refresh)
    np.save(cached, rec["array"].astype(np.float32))
    write_receipt([rec], footprint)
    return rec["array"]
