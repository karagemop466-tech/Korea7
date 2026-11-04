#!/usr/bin/env python3
"""Experiment 2: sparse-segment extension model + clearance/budget sweep.

Experiment 1 modelled an extension as every catalogue pixel pushed outward.
Under that model denser halos win monotonically, which contradicts the observed
leaderboard (rho(dots, score) = -0.983: sparser scored better).  A model is
only useful if it reproduces what was actually measured, so this experiment
uses the alternative that does.

SPARSE-SEGMENT MODEL
--------------------
A newly mapped trace is a *contiguous segment* flanking a known trace, covering
only a fraction ``f`` of that trace's length, at a 1-2 px offset.  Only a small
share of the halo shell is therefore on new ground truth.  This is the
geometry that makes the marginal halo dot net-negative and produces the
observed negative dots/score relation, because the shell contains far more
candidate positions than real extensions.

We sweep (clearance, dot budget) and report expected DTI under a mixture of
such extensions plus independent discovery traces.  Output is a MODEL-BASED
ESTIMATE, never a score.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation, label

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from k7.grid import load_grid  # noqa: E402
from k7.metric import dti  # noqa: E402
from k7.method import catalogue_distance, lattice_mask  # noqa: E402

OUT = ROOT / "evidence" / "sweep_experiment.json"


def sparse_segment_extensions(truth, footprint, rng, frac_structures, cover_frac,
                              offset_px=(1, 2), min_size=8):
    """Contiguous offset segments covering ``cover_frac`` of selected structures."""
    lbl, n = label(truth, structure=np.ones((3, 3), int))
    out = np.zeros(truth.shape, dtype=bool)
    sizes = np.bincount(lbl.ravel())
    cand = [i for i in range(1, n + 1) if sizes[i] >= min_size]
    if not cand:
        return out
    take = rng.choice(cand, size=max(1, int(len(cand) * frac_structures)), replace=False)
    h, w = truth.shape
    for i in take:
        rr, cc = np.nonzero(lbl == i)
        order = np.argsort(rr * 10000 + cc)
        rr, cc = rr[order], cc[order]
        seg_len = max(3, int(len(rr) * cover_frac))
        start = rng.integers(0, max(1, len(rr) - seg_len))
        rr, cc = rr[start:start + seg_len], cc[start:start + seg_len]
        ang = rng.uniform(0, 2 * np.pi)
        rad = rng.integers(offset_px[0], offset_px[1] + 1)
        nr = np.clip(rr + int(round(rad * np.sin(ang))), 0, h - 1)
        nc = np.clip(cc + int(round(rad * np.cos(ang))), 0, w - 1)
        out[nr, nc] = True
    return out & footprint & ~truth


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


def main() -> int:
    g = load_grid()
    foot, truth = g.footprint, g.truth
    dist = catalogue_distance(truth)
    valid = foot & ~truth          # organiser masks the catalogue pixel-exactly
    halo_shell = binary_dilation(truth, iterations=6) & ~truth & foot

    budgets = [20_000, 30_000, 37_654, 44_090, 60_069]
    clearances = [0, 1, 2, 3, 4, 5]

    runs = []
    for seed in range(4):
        rng = np.random.default_rng(7000 + seed)
        hidden = sparse_segment_extensions(truth, foot, rng, frac_structures=0.55, cover_frac=0.35)
        if hidden.sum() < 500:
            continue
        rec = {"seed": seed, "hidden_px": int((hidden & valid).sum())}
        for k in clearances:
            shell_k = halo_shell & (dist > k)
            for b in budgets:
                cand = thin(shell_k, b)
                rec[f"k{k}_b{b}"] = float(dti(cand.astype(np.float32), hidden, valid=valid))
        # reference: the uniform lattice at 400 m clearance
        uni = lattice_mask(foot.shape) & foot & (dist > 4)
        rec["lattice400_29270"] = float(dti(thin(uni, 29270).astype(np.float32), hidden, valid=valid))
        runs.append(rec)
        print(f"seed {seed} hidden={rec['hidden_px']:,}")

    keys = [k for k in runs[0] if k.startswith(("k", "lattice"))]
    agg = {k: float(np.mean([r[k] for r in runs])) for k in keys}

    print("\n=== mean DTI vs sparse-segment extensions, by clearance (rows) x budget (cols) ===")
    print("clear".ljust(7) + "".join(f"{b:>10d}" for b in budgets))
    for k in clearances:
        print(f"k={k}".ljust(7) + "".join(f"{agg[f'k{k}_b{b}']:10.4f}" for b in budgets))
    print(f"\nuniform lattice @400 m, 29,270 dots: {agg['lattice400_29270']:.4f}")

    best = max(agg, key=agg.get)
    print(f"\nBEST cell: {best} -> {agg[best]:.4f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": "MODEL-BASED ESTIMATE - NOT A SCORE",
        "model": "sparse contiguous offset segments (55% of structures, 35% of length, 1-2 px offset)",
        "valid_domain": "footprint minus pixel-exact catalogue mask (organiser rule)",
        "budgets": budgets,
        "clearances": clearances,
        "aggregate": agg,
        "runs": runs,
        "best_cell": best,
    }, indent=2) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
