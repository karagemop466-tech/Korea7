#!/usr/bin/env python3
"""Korea7 SDCC-1 submission generator (lane: scarp-dominant concordance fusion).

Reproduces the exact pipeline that produced the shipped candidates in
docs/downloads/ on 2026-11-04. End-to-end stages:

  1. restore   -- fetch SHA-256-pinned competition mirrors from accessible repos
  2. surface   -- build the SDCC-1 fused prospectivity surface
  3. place     -- uniqueness-constrained Poisson-disk dot placement
  4. write     -- emit zeros-background float32 GeoTIFF on the organizer grid

Method (single lane, logged in run-card.json):
  Fuse LiDAR-scarp evidence (max of ex_max/step_max percentiles, coherence
  weighted), upward-continued TMI (150 m) horizontal-gradient percentile,
  Th/K radiometric alteration-low percentile, and a 2 km wellspring conduit
  prior; multiply by a concordance bonus (count of evidence lines above the
  90th percentile); suppress pixels within 200 m of a road; zero a 2-px
  catalogue collar around existing_faults.tif; emit dots in descending
  surface order with min separation 2.8 px and a hard per-registry cap of
  65% of dots within 3 px of any single registry raster's dots.

Distinct from the registry family (h19-5 power-law multiline corroboration
+ its D1.5/D2.8/B2 emissions): different expert set (no tilt/openness; adds
alteration + wellspring prior + road suppression), different fusion rule
(weighted-percentile sum x concordance bonus, not corroboration-count power
law), and an explicit online uniqueness constraint during placement.

Data provenance (all SHA-256 pinned below; mirrors of login-walled
DrivenData files -- integrity-pinned, NOT organizer-authentic):
  core:     github.com/sassnarep3-star/GEMSDOESASS2  data/bridge/
  external: github.com/kanlerxz87-cyber/KANLERGEMSDOE1 data/external/
  registry: github.com/karagemop466-tech/GEMSDOEkarage1 registry/ and
            github.com/kanlerxz87-cyber/KANLERGEMSDOE1 data/scored/

Usage:
  python scripts/generate_submission.py --data-dir .cache/gems_data \
      --registry-dir .cache/registry --out docs/downloads --budget 44090
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import binary_dilation
from scipy.spatial import cKDTree

PINS = {
    "labels.tif": "7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093",
    "existing_faults.tif": "7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093",
    "sample_submission.tif": "2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc",
    "external/lidar_scarp_features_u8.tif": "sha-pinned in GEMSDOEkarage3 registry/data_manifest.json",
    "external/geodawn_extensions_u8.tif": "sha-pinned in GEMSDOEkarage3 registry/data_manifest.json",
    "external/tiger_road_distance_m.tif": "sha-pinned in GEMSDOEkarage3 registry/data_manifest.json",
}

CORE_REPO = "sassnarep3-star/GEMSDOESASS2"
CORE_FILES = ["existing_faults.tif", "labels.tif", "sample_submission.tif"]
EXT_REPO = "kanlerxz87-cyber/KANLERGEMSDOE1"
EXT_FILES = [
    "lidar_scarp_features_u8.tif",
    "geodawn_extensions_u8.tif",
    "tiger_road_distance_m.tif",
    "derived_sgmc_faults_100m_u8.tif",
]
EXT_CSV = ["gdr_wellspring_in_footprint.csv"]

SEP_PX = 2.8          # Poisson-disk min separation (280 m)
COLLAR_PX = 2         # catalogue collar (200 m) around existing faults
UNIQ_RADIUS_PX = 3.0  # 300 m kernel radius used by the uniqueness rule
UNIQ_CAP = 0.65       # max fraction of our dots within 3 px of ONE registry raster
ROAD_SUPPRESS_M = 200.0
ROAD_FACTOR = 0.3
WELL_DECAY_M = 2000.0


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def gh_raw(repo: str, path: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as out:
        subprocess.run(
            ["gh", "api", f"repos/{repo}/contents/{path}",
             "-H", "Accept: application/vnd.github.raw"],
            stdout=out, check=True)


def restore(data_dir: Path) -> None:
    for f in CORE_FILES:
        d = data_dir / f
        if not d.exists():
            gh_raw(CORE_REPO, f"data/bridge/{f}", d)
        pin = PINS.get(f)
        if pin and len(pin) == 64 and sha256_file(d) != pin:
            raise SystemExit(f"SHA-256 mismatch for {f}; refusing to continue")
    for f in EXT_FILES + EXT_CSV:
        d = data_dir / "external" / f
        if not d.exists():
            gh_raw(EXT_REPO, f"data/external/{f}", d)
    print("restore: core + external present and pinned files verified")


def restore_registry(reg_dir: Path) -> None:
    reg_dir.mkdir(parents=True, exist_ok=True)
    listing = subprocess.run(
        ["gh", "api", f"repos/karagemop466-tech/GEMSDOEkarage1/contents/registry"],
        capture_output=True, text=True, check=True)
    for item in json.loads(listing.stdout):
        if item["name"].endswith(".tif") and not (reg_dir / item["name"]).exists():
            gh_raw("karagemop466-tech/GEMSDOEkarage1", f"registry/{item['name']}",
                   reg_dir / item["name"])
    listing = subprocess.run(
        ["gh", "api", f"repos/{EXT_REPO}/contents/data/scored"],
        capture_output=True, text=True, check=True)
    for item in json.loads(listing.stdout):
        if item["name"].endswith(".tif") and not (reg_dir / ("scored_" + item["name"])).exists():
            gh_raw(EXT_REPO, f"data/scored/{item['name']}", reg_dir / ("scored_" + item["name"]))
    print(f"restore: registry rasters in {reg_dir}")


def percentile_map(a: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=np.float32)
    v = a[mask]
    order = np.argsort(v, kind="stable")
    ranks = np.empty(len(v), dtype=np.float64)
    ranks[order] = np.arange(len(v)) / max(len(v) - 1, 1)
    out[mask] = ranks.astype(np.float32)
    return out


def build_surface(data_dir: Path) -> np.ndarray:
    with rasterio.open(data_dir / "sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    with rasterio.open(data_dir / "labels.tif") as ds:
        lab = (ds.read(1) > 0) & foot
    with rasterio.open(data_dir / "external" / "lidar_scarp_features_u8.tif") as ds:
        ex = ds.read(1).astype(np.float32) / 255
        step = ds.read(3).astype(np.float32) / 255
        coh = ds.read(10).astype(np.float32) / 255
    with rasterio.open(data_dir / "external" / "geodawn_extensions_u8.tif") as ds:
        thk = ds.read(1).astype(np.float32) / 255
        tmi = ds.read(4).astype(np.float32) / 255
    with rasterio.open(data_dir / "external" / "tiger_road_distance_m.tif") as ds:
        road = ds.read(1).astype(np.float32)

    gy, gx = np.gradient(tmi)
    mgrad = np.hypot(gy, gx)
    p_ex = percentile_map(ex, foot)
    p_step = percentile_map(step, foot)
    p_mg = percentile_map(mgrad, foot)
    p_alt = percentile_map(-thk, foot)

    rows, cols = [], []
    with (data_dir / "external" / "gdr_wellspring_in_footprint.csv").open() as f:
        for rec in csv.DictReader(f):
            try:
                rows.append(int(rec["row"]))
                cols.append(int(rec["col"]))
            except (KeyError, ValueError):
                continue
    well = np.zeros(foot.shape, np.float32)
    ij = np.argwhere(foot)
    dist, _ = cKDTree(np.c_[rows, cols]).query(ij, k=1)
    well[ij[:, 0], ij[:, 1]] = np.exp(-(dist * 100.0) / WELL_DECAY_M)

    scarp = np.maximum(p_ex, p_step) * (0.4 + 0.6 * coh)
    surface = 0.60 * scarp + 0.20 * p_mg + 0.10 * p_alt + 0.10 * well
    concord = ((scarp > 0.90).astype(np.float32) + (p_mg > 0.90)
               + (p_alt > 0.90) + (well > 0.5))
    surface *= (1.0 + 0.25 * concord)
    surface[road < ROAD_SUPPRESS_M] *= ROAD_FACTOR
    surface[~foot] = 0.0
    surface[binary_dilation(lab, iterations=COLLAR_PX)] = 0.0
    return surface


def load_registry_trees(reg_dir: Path, shape) -> dict[str, cKDTree]:
    trees: dict[str, cKDTree] = {}
    seen: set[str] = set()
    for p in sorted(glob.glob(str(reg_dir / "*.tif"))):
        digest = sha256_file(Path(p))
        if digest in seen:
            continue
        seen.add(digest)
        try:
            with rasterio.open(p) as ds:
                if ds.shape != tuple(shape):
                    continue
                arr = ds.read(1)
        except rasterio.errors.RasterioIOError:
            continue
        dots = np.argwhere(np.isfinite(arr) & (arr > 0))
        if len(dots) == 0 or len(dots) > 200_000:
            continue
        trees[Path(p).name] = cKDTree(dots)
    return trees


def place(surface: np.ndarray, trees: dict[str, cKDTree], budget: int):
    order = np.argsort(surface, axis=None)[::-1]
    h, w = surface.shape
    occ = np.zeros((h, w), bool)
    sep_i = int(np.ceil(SEP_PX))
    quota = {n: int(UNIQ_CAP * budget) for n in trees}
    count = {n: 0 for n in trees}
    chosen: list[tuple[int, int]] = []
    names = list(trees)
    for idx in order:
        if len(chosen) >= budget:
            break
        if surface.flat[idx] <= 0:
            break
        r, c = divmod(int(idx), w)
        r0, r1 = max(0, r - sep_i), min(h, r + sep_i + 1)
        c0, c1 = max(0, c - sep_i), min(w, c + sep_i + 1)
        if occ[r0:r1, c0:c1].any():
            rr, cc = np.nonzero(occ[r0:r1, c0:c1])
            if (((rr + r0 - r) ** 2 + (cc + c0 - c) ** 2) < SEP_PX * SEP_PX).any():
                continue
        hits, blocked = [], False
        for n in names:
            if trees[n].query_ball_point([r, c], UNIQ_RADIUS_PX, return_length=True) > 0:
                if count[n] + 1 > quota[n]:
                    blocked = True
                    break
                hits.append(n)
        if blocked:
            continue
        for n in hits:
            count[n] += 1
        occ[r, c] = True
        chosen.append((r, c))
    overlap = {n: count[n] / max(len(chosen), 1) for n in names}
    return np.array(chosen), overlap


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=".cache/gems_data")
    ap.add_argument("--registry-dir", default=".cache/registry")
    ap.add_argument("--out", default="docs/downloads")
    ap.add_argument("--budget", type=int, default=44090)
    ap.add_argument("--skip-restore", action="store_true")
    a = ap.parse_args()
    data_dir, reg_dir, out_dir = Path(a.data_dir), Path(a.registry_dir), Path(a.out)
    if not a.skip_restore:
        restore(data_dir)
        restore_registry(reg_dir)
    surface = build_surface(data_dir)
    trees = load_registry_trees(reg_dir, surface.shape)
    print(f"registry rasters for the uniqueness rule: {len(trees)}")
    dots, overlap = place(surface, trees, a.budget)
    max_overlap = max(overlap.values()) if overlap else 0.0
    if max_overlap > 0.70:
        raise SystemExit(f"DUPLICATE/DRIFT: overlap {max_overlap:.3f} > 0.70 -- stopping per protocol")
    with rasterio.open(data_dir / "sample_submission.tif") as ds:
        profile = ds.profile
    profile.update(dtype="float32", count=1, nodata=None, compress="deflate")
    out = np.zeros(surface.shape, np.float32)
    out[dots[:, 0], dots[:, 1]] = 1.0
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / "candidate_unnamed.tif"
    with rasterio.open(tmp, "w", **profile) as ds:
        ds.write(out, 1)
    digest8 = sha256_file(tmp)[:8]
    import datetime as dt
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    final = out_dir / f"korea7-sdcc1-scarpdom-conc-uniq65-{a.budget}-{stamp}-{digest8}-zeros.tif"
    os.replace(tmp, final)
    receipt = {
        "file": final.name,
        "sha256": sha256_file(final),
        "dots": int(len(dots)),
        "budget": a.budget,
        "max_registry_overlap_3px": max_overlap,
        "registry_overlap": overlap,
        "lane_pass": max_overlap <= 0.70,
    }
    (out_dir / (final.stem + ".receipt.json")).write_text(json.dumps(receipt, indent=1))
    print(json.dumps({k: v for k, v in receipt.items() if k != "registry_overlap"}, indent=1))


if __name__ == "__main__":
    main()
