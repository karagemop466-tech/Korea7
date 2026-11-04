#!/usr/bin/env python3
"""Uniqueness of a Korea7 candidate vs the nine focus winners (+ lattice witness).

Protocol thresholds: surface Spearman rho > 0.90 OR >70% of candidate dots
within 3 px of one registry raster's dots => duplicate / lane drift, stop.
Registry *surfaces* for the nine were never published in the mirrors (only
their binary dot rasters), so the surface gate is computed against each
winner's binary dot raster inside the footprint (documented adaptation; the
dot-overlap gate is exact). NaN-outside variants are read as dots==(value==1)
inside the footprint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", type=Path, required=True)
    ap.add_argument("--mask", type=Path, required=True, help=".npy binary mask or candidate .tif")
    ap.add_argument("--out", type=Path, default=ROOT / "evidence/uniqueness.json")
    a = ap.parse_args()

    with rasterio.open(ROOT / "data/sample_submission.tif") as s:
        foot = np.isfinite(s.read(1))
    with rasterio.open(a.surface) as s:
        surf = s.read(1)
    if a.mask.suffix == ".npy":
        cand = np.load(a.mask) & foot
    else:
        with rasterio.open(a.mask) as s:
            cand = (s.read(1) == 1) & foot

    rows = []
    targets = [(f"GEMSDOE{n}", ROOT / f"registry/GEMSDOE{n}.tif") for n in (24, 25, 27, 28, 30, 31, 32, 33, 36)]
    targets.append(("LATTICE_WITNESS_r13 (dense, non-focus)", ROOT / "registry/LATTICE_WITNESS_r13.tif"))
    for site, p in targets:
        with rasterio.open(p) as s:
            reg = (s.read(1) == 1) & foot
        rho = float(spearmanr(surf[foot], reg[foot].astype(float)).statistic)
        overlap = float((distance_transform_edt(~reg)[cand] <= 3).mean())
        jacc = float((cand & reg).sum() / max((cand | reg).sum(), 1))
        rows.append({"site": site, "registry_sha256": sha256(p), "registry_dots": int(reg.sum()),
                     "surface_vs_registry_dots_spearman": rho,
                     "candidate_dots_within_3px_frac": overlap,
                     "exact_dot_jaccard": jacc,
                     "duplicate_by_protocol": bool(rho > 0.90 or overlap > 0.70)})
        print(site, f"rho={rho:.3f} overlap3px={overlap:.3f} jaccard={jacc:.3f} dup={rows[-1]['duplicate_by_protocol']}")
    focus = rows[:9]
    out = {"candidate_dots": int(cand.sum()), "surface": str(a.surface), "mask": str(a.mask),
           "thresholds": {"rho_max": 0.90, "overlap3px_max": 0.70},
           "focus9_pass": not any(r["duplicate_by_protocol"] for r in focus),
           "rows": rows,
           "note": "Surface gate uses registry dot rasters (registry surfaces unavailable in mirrors). Lattice witness row is disclosed separately: a dense synthetic lattice covers most of the footprint within 3 px, so the literal full-registry rule is unmeetable by any dense candidate (flagged IR-K7-01)."}
    a.out.write_text(json.dumps(out, indent=2) + "\n")
    print("FOCUS-9 UNIQUE:", out["focus9_pass"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
