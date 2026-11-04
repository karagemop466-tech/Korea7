#!/usr/bin/env python3
"""Build and rank the final candidate surfaces.

Each candidate is a deterministic rotated-square lattice (``k7.method``) gated by
a catalogue-clearance rule and thinned to a dot budget.  Candidates are scored
on (a) expected DTI against the sparse-segment extension population and (b)
lane compliance against all nine recovered registry rasters.  Only a candidate
that is both competitive and unique may be promoted.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import binary_dilation

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from k7.grid import load_grid  # noqa: E402
from k7.metric import dti  # noqa: E402
from k7.method import catalogue_distance, lattice_mask  # noqa: E402
from k7.overlap import compare  # noqa: E402

REG = ROOT / "evidence" / "registry"
OUT = ROOT / "evidence" / "final_candidates.json"


def thin(mask, budget):
    mask = np.asarray(mask, bool)
    n = int(mask.sum())
    if n <= budget:
        return mask
    idx = np.flatnonzero(mask.ravel())
    stride = n / budget
    out = np.zeros(mask.shape, dtype=bool)
    out.ravel()[idx[(np.arange(budget) * stride).astype(np.int64)]] = True
    return out


def sparse_ext(truth, foot, rng, frac=0.55, cover=0.35, off=(1, 2), min_size=8):
    from scipy.ndimage import label

    lbl, n = label(truth, structure=np.ones((3, 3), int))
    sizes = np.bincount(lbl.ravel())
    cand = [i for i in range(1, n + 1) if sizes[i] >= min_size]
    out = np.zeros(truth.shape, dtype=bool)
    h, w = truth.shape
    take = rng.choice(cand, size=max(1, int(len(cand) * frac)), replace=False)
    for i in take:
        rr, cc = np.nonzero(lbl == i)
        o = np.argsort(rr * 10000 + cc)
        rr, cc = rr[o], cc[o]
        L = max(3, int(len(rr) * cover))
        s = rng.integers(0, max(1, len(rr) - L))
        rr, cc = rr[s:s + L], cc[s:s + L]
        ang = rng.uniform(0, 2 * np.pi)
        rad = rng.integers(off[0], off[1] + 1)
        nr = np.clip(rr + int(round(rad * np.sin(ang))), 0, h - 1)
        nc = np.clip(cc + int(round(rad * np.cos(ang))), 0, w - 1)
        out[nr, nc] = True
    return out & foot & ~truth


def main() -> int:
    g = load_grid()
    foot, truth = g.footprint, g.truth
    dist = catalogue_distance(truth)
    lat = lattice_mask(foot.shape) & foot
    valid = foot & ~truth

    defs = {
        "K7-HALO-37654-k3-band8": (lat & (dist > 3) & (dist <= 8), 37_654),
        "K7-HALO-40199-k3-band8": (lat & (dist > 3) & (dist <= 8), 40_199),
        "K7-HALO-32000-k3-band8": (lat & (dist > 3) & (dist <= 8), 32_000),
        "K7-UNIFORM-29270-k4": (lat & (dist > 4), 29_270),
        "K7-HALO-37654-k4-band8": (lat & (dist > 4) & (dist <= 8), 37_654),
    }

    # registry masks + a "dilate2" reference for context
    reg = {}
    for p in sorted(REG.glob("*.tif")):
        with rasterio.open(p) as ds:
            reg[p.name.split("-")[0]] = np.nan_to_num(ds.read(1)) > 0
    ref_dil2 = thin(binary_dilation(truth, iterations=2) & foot, 37_654)

    # sparse-segment extension population, 4 seeds
    hiddens = []
    for s in range(4):
        rng = np.random.default_rng(7000 + s)
        hiddens.append(sparse_ext(truth, foot, rng))

    cands = {}
    for name, (raw, budget) in defs.items():
        m = thin(raw, budget)
        dm = dist[m]
        scores = [float(dti(m.astype(np.float32), h, valid=valid)) for h in hiddens]
        worst = {}
        for site, rm in reg.items():
            ov = compare(m, rm)
            if not worst or ov.jaccard > worst["jaccard"]:
                worst = {"site": site, "jaccard": ov.jaccard,
                         "frac_within_3px": ov.frac_within_3px,
                         "dot_rank_spearman": ov.spearman_dot_ranks}
        cands[name] = {
            "dots": int(m.sum()),
            "min_dist_px": float(dm.min()),
            "median_dist_px": float(np.median(dm)),
            "frac_within_2px": float((dm <= 2).mean()),
            "frac_within_3px": float((dm <= 3).mean()),
            "ext_model_dti_mean": float(np.mean(scores)),
            "ext_model_dti_min": float(np.min(scores)),
            "closest_registry": worst,
            "unique": bool(worst["jaccard"] < 0.70 and worst["frac_within_3px"] <= 0.70),
            "sha256_lattice_gate": hashlib.sha256(
                np.packbits(m).tobytes()).hexdigest()[:16],
        }

    ref_scores = [float(dti(ref_dil2.astype(np.float32), h, valid=valid)) for h in hiddens]
    payload = {
        "label": "MODEL-BASED ESTIMATE - NOT A SCORE",
        "reference_dilate2_37654": {
            "dots": int(ref_dil2.sum()),
            "ext_model_dti_mean": float(np.mean(ref_scores)),
            "ext_model_dti_min": float(np.min(ref_scores)),
        },
        "candidates": cands,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"{'candidate':30s} {'dots':>6s} {'minD':>5s} {'f<=2':>5s} {'extDTI':>7s} {'jacc':>6s} {'f3px':>6s} {'uniq':>5s}")
    print(f"{'REF dilate2':30s} {int(ref_dil2.sum()):6d} {'-':>5s} {'-':>5s} {np.mean(ref_scores):7.4f} {'-':>6s} {'-':>6s} {'-':>5s}")
    for name, c in sorted(cands.items(), key=lambda kv: -kv[1]["ext_model_dti_mean"]):
        print(f"{name:30s} {c['dots']:6d} {c['min_dist_px']:5.2f} {c['frac_within_2px']:5.3f} "
              f"{c['ext_model_dti_mean']:7.4f} {c['closest_registry']['jaccard']:6.3f} "
              f"{c['closest_registry']['frac_within_3px']:6.3f} {str(c['unique']):>5s}")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
