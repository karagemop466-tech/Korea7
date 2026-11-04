"""Spatially-blocked hide-and-recover holdout.

Protocol (parallel-run item 2): withhold whole structures with a buffer, derive
every catalogue-dependent feature from the visible set only, and mask visible
faults pixel-exactly before scoring pooled DTI.

Here the withheld population is *catalogue structure kept out of the clearance
set*, because the method under test uses the catalogue only as an exclusion
mask.  Concretely, for each spatial block we

1. hide every catalogue connected component whose centroid falls inside the
   block (a whole-structure hide, never a partial trace), with a 1.5 km collar
   so no train/test adjacency leaks;
2. re-derive the clearance set from the visible structure only;
3. score the candidate inside the block against the *hidden* structure.

This measures the one thing the method actually claims: that placing dots at a
fixed clearance from visible catalogue structure, on a uniform lattice, will
land near structure that has not yet been mapped.  It is an idealised
upper-bound generator (see ``k7/synth.py``) and is labelled as such wherever it
is reported.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import binary_dilation, label

from .metric import dti_from_components, kernel, ALPHA, BETA
from .method import catalogue_distance

COLLAR_PX = 15  # 1.5 km train/test separation
N_BLOCKS_DEFAULT = 256


@dataclass(frozen=True)
class Block:
    r0: int
    r1: int
    c0: int
    c1: int

    @property
    def rows(self) -> slice:
        return slice(self.r0, self.r1)

    @property
    def cols(self) -> slice:
        return slice(self.c0, self.c1)


def make_blocks(shape: tuple[int, int], n: int = N_BLOCKS_DEFAULT) -> list[Block]:
    """Square tiling of the grid into ``n`` contiguous spatial blocks."""
    side = int(round(np.sqrt(n)))
    h, w = shape
    rb = np.linspace(0, h, side + 1).astype(int)
    cb = np.linspace(0, w, side + 1).astype(int)
    return [Block(int(rb[i]), int(rb[i + 1]), int(cb[j]), int(cb[j + 1]))
            for i in range(side) for j in range(side)]


def evaluate_block(
    candidate: np.ndarray,
    truth: np.ndarray,
    footprint: np.ndarray,
    block: Block,
    collar_px: int = COLLAR_PX,
) -> dict | None:
    """Score one block under hide-and-recover. Returns None when the block is unusable."""
    truth = np.asarray(truth, bool)
    footprint = np.asarray(footprint, bool)
    candidate = np.asarray(candidate, bool)

    # 1. structures whose centroid lies in this block are *hidden*
    lbl, n = label(truth, structure=np.ones((3, 3), int))
    if n == 0:
        return None
    inside = np.zeros(n + 1, dtype=bool)
    rr, cc = np.nonzero(truth)
    comp = lbl[rr, cc]
    sel = (rr >= block.r0) & (rr < block.r1) & (cc >= block.c0) & (cc < block.c1)
    inside[comp[sel]] = True
    inside[0] = False
    hidden = inside[lbl] & truth
    if not hidden.any():
        return None

    # 2. everything else is visible; clearance is re-derived from visible only
    visible = truth & ~binary_dilation(hidden, iterations=collar_px)
    if not visible.any():
        return None
    dist_visible = catalogue_distance(visible)

    # 3. candidate dots inside the block that respect the visible-only clearance
    rows, cols = block.rows, block.cols
    cand_b = candidate[rows, cols]
    if not cand_b.any():
        return None
    keep = cand_b & (dist_visible[rows, cols] > 0)
    if not keep.any():
        return None

    # 4. score against the hidden structure, inside the block only
    hidden_b = hidden[rows, cols]
    if not hidden_b.any():
        return None
    hb = hidden_b
    from scipy.ndimage import distance_transform_edt

    p = keep.astype(np.float64)
    best = np.zeros(p.shape)
    from .metric import OFFSETS, _shift

    for dy, dx, k in OFFSETS:
        np.maximum(best, _shift(p, dy, dx) * k, out=best)
    best = np.clip(best, 0.0, 1.0)
    tp = float(best[hb].sum())
    d_h = distance_transform_edt(~hb)
    fp = float((p * (1.0 - kernel(d_h))).sum())
    fn = float(hb.sum()) - tp
    return {"tp": tp, "fp": fp, "fn": fn, "n_truth": int(hb.sum()),
            "dti": dti_from_components(tp, fp, fn)}


def evaluate_holdout(
    candidate: np.ndarray,
    truth: np.ndarray,
    footprint: np.ndarray,
    n_blocks: int = N_BLOCKS_DEFAULT,
    seed: int = 0,
    n_boot: int = 400,
) -> dict:
    """Pooled hide-and-recover DTI with a spatial block-bootstrap 95% CI."""
    blocks = make_blocks(footprint.shape, n_blocks)
    res = [evaluate_block(candidate, truth, footprint, b) for b in blocks]
    res = [r for r in res if r is not None]
    if not res:
        return {"status": "empty", "n_blocks_used": 0}

    tp = sum(r["tp"] for r in res)
    fp = sum(r["fp"] for r in res)
    fn = sum(r["fn"] for r in res)
    pooled = dti_from_components(tp, fp, fn)

    rng = np.random.default_rng(seed)
    tps = np.array([r["tp"] for r in res])
    fps = np.array([r["fp"] for r in res])
    fns = np.array([r["fn"] for r in res])
    n = len(res)
    boot = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot[i] = dti_from_components(tps[idx].sum(), fps[idx].sum(), fns[idx].sum())

    return {
        "status": "ok",
        "metric": "HOLDOUT-DTI",
        "evaluator_version": "K7-HIDE-RECOVER-v1.0",
        "n_blocks_used": n,
        "n_withheld_positives": int(sum(r["n_truth"] for r in res)),
        "pooled_dti": float(pooled),
        "ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
        "components": {"tp": tp, "fp": fp, "fn": fn, "alpha": ALPHA, "beta": BETA},
    }
