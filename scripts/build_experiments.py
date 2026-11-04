#!/usr/bin/env python3
"""Korea7 lane experiments E1/E2 (E3 = road control, run after E1/E2 are scored).

LANE (single method paragraph): build a blind-fault surface only from the
external lidar-scarp and GeoDAWN radiometric/magnetic u8 stacks by AND-gating
(geometric mean of footprint rank maps) a coherent topographic step with a
radiometric-ratio edge (E1) and additionally an upward-continued magnetic edge
(E2); emit binary dots by lazy-greedy maximization of surface-weighted
300 m triangular-kernel coverage (the exact credit kernel of the official
DTI), restricted to >2 px from the catalogue (the champion's measured "b2"
geometry), at the champion's budget of 37,654 dots. Named non-fault mimic:
lithologic contacts and roads (E3 controls roads). No catalogue-derived
feature is used, so hide-and-recover fold leakage via catalogue features is
impossible by construction; the >2 px gate uses the full catalogue exactly as
the champion's static emission did (disclosed in the run card).

Outputs: work/<exp>_surface.tif (float32 rank surface, for the pre-placement
uniqueness gate), work/<exp>_mask.npy (binary emission for the shared writer),
evidence/experiments_build.json (parameters + hashes).
"""
from __future__ import annotations

import hashlib
import heapq
import json
import time
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt, sobel

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"
WORK = ROOT / "work"
BUDGET = 37_654
CAT_MIN_DIST_PX = 2.0  # champion geometry: measured min dot distance = 2.24 px
MAX_CANDIDATES = 400_000

# 300 m triangular kernel offsets (R = 3 px), k(d) = max(1 - d/3, 0), k > 0 only.
OFFS = [(dy, dx, 1.0 - np.hypot(dy, dx) / 3.0)
        for dy in range(-3, 4) for dx in range(-3, 4) if np.hypot(dy, dx) < 3.0]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rank01(a: np.ndarray, valid: np.ndarray) -> np.ndarray:
    """Percentile rank in [0,1] over valid pixels; 0 elsewhere."""
    out = np.zeros(a.shape, dtype=np.float32)
    v = a[valid]
    order = np.argsort(v, kind="mergesort")
    r = np.empty(len(v), dtype=np.float64)
    r[order] = np.arange(len(v)) / max(len(v) - 1, 1)
    out[valid] = r.astype(np.float32)
    return out


def grad_rank(a: np.ndarray, valid: np.ndarray) -> np.ndarray:
    g = np.hypot(sobel(a, axis=0), sobel(a, axis=1))
    return rank01(g, valid)


def greedy_cover(surf: np.ndarray, eligible: np.ndarray, budget: int) -> np.ndarray:
    """Lazy greedy submodular coverage: gain_i = s_i * sum_k k*(1-cov)."""
    ys, xs = np.nonzero(eligible)
    svals = surf[ys, xs]
    if len(svals) > MAX_CANDIDATES:
        keep = np.argpartition(svals, -MAX_CANDIDATES)[-MAX_CANDIDATES:]
        ys, xs, svals = ys[keep], xs[keep], svals[keep]
    H, W = surf.shape
    cov = np.zeros((H, W), dtype=np.float32)
    ksum = sum(k for _, _, k in OFFS)

    def gain(y: int, x: int, s: float) -> float:
        acc = 0.0
        for dy, dx, k in OFFS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W:
                acc += k * (1.0 - float(cov[ny, nx]))
        return s * acc

    heap = [(-float(s) * ksum, i) for i, s in enumerate(svals)]
    heapq.heapify(heap)
    mask = np.zeros((H, W), dtype=bool)
    placed = 0
    while placed < budget and heap:
        negg, i = heapq.heappop(heap)
        y, x, s = int(ys[i]), int(xs[i]), float(svals[i])
        g = gain(y, x, s)
        if heap and g < -heap[0][0] - 1e-12:
            heapq.heappush(heap, (-g, i))
            continue
        mask[y, x] = True
        placed += 1
        for dy, dx, k in OFFS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and cov[ny, nx] < k:
                cov[ny, nx] = k
    return mask


def main() -> int:
    WORK.mkdir(exist_ok=True)
    t0 = time.time()
    with rasterio.open(D / "sample_submission.tif") as s:
        foot = np.isfinite(s.read(1))
        profile = s.profile.copy()
    with rasterio.open(D / "labels.tif") as s:
        labels = (s.read(1) > 0) & foot
    d_cat = distance_transform_edt(~labels)

    with rasterio.open(D / "external/lidar_scarp_features_u8.tif") as s:
        bands = {s.descriptions[i]: s.read(i + 1).astype(np.float64) for i in range(s.count)}
    valid = foot & (bands["valid"] > 0)
    lidar_step = np.exp(np.mean(np.log(np.clip(np.stack([
        rank01(bands["step_max"], valid),
        rank01(bands["cross_max"], valid),
        rank01(np.maximum(bands["downface_max"], bands["upface_max"]), valid),
    ]), 1e-6, None)), axis=0)).astype(np.float32)

    with rasterio.open(D / "external/geodawn_extensions_u8.tif") as s:
        ext = {s.descriptions[i]: s.read(i + 1).astype(np.float64) for i in range(s.count)}
    # u8 stacks use 0 as nodata; restrict edge ranks to jointly-valid pixels.
    rad_valid = foot & (ext["ThK"] > 0) & (ext["UK"] > 0)
    rad_edge = np.mean([grad_rank(ext[b], rad_valid) for b in ("ThK", "UK", "UTh")], axis=0).astype(np.float32)
    tmi_edge = grad_rank(ext["TMI_up150"], foot & (ext["TMI_up150"] > 0))

    base_valid = valid & rad_valid
    surfaces = {
        "E1": np.sqrt(np.clip(lidar_step, 0, None) * np.clip(rad_edge, 0, None)).astype(np.float32),
        "E2": np.cbrt(np.clip(lidar_step, 0, None) * np.clip(rad_edge, 0, None)
                      * np.clip(tmi_edge, 0, None)).astype(np.float32),
    }
    eligible = base_valid & (d_cat > CAT_MIN_DIST_PX)
    meta = {"budget": BUDGET, "cat_min_dist_px_exclusive": CAT_MIN_DIST_PX,
            "eligible_px": int(eligible.sum()), "experiments": {}}
    profile.update(dtype="float32", count=1, nodata=None, compress="deflate")
    for name, surf in surfaces.items():
        surf_e = np.where(eligible, surf, 0.0).astype(np.float32)
        sp = WORK / f"{name}_surface.tif"
        with rasterio.open(sp, "w", **profile) as dst:
            dst.write(surf_e, 1)
        mask = greedy_cover(surf_e, eligible & (surf_e > 0), BUDGET)
        mp = WORK / f"{name}_mask.npy"
        np.save(mp, mask)
        meta["experiments"][name] = {
            "dots": int(mask.sum()),
            "surface_tif": str(sp.relative_to(ROOT)),
            "surface_sha256": sha256_bytes(sp.read_bytes()),
            "mask_npy": str(mp.relative_to(ROOT)),
            "mask_sha256": sha256_bytes(mp.read_bytes()),
            "min_dist_to_catalogue_px": float(d_cat[mask].min()),
        }
        print(name, meta["experiments"][name])
    meta["seconds"] = round(time.time() - t0, 1)
    (ROOT / "evidence/experiments_build.json").write_text(json.dumps(meta, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
