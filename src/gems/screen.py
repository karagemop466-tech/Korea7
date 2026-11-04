"""Hide-and-recover screening, leakage canary and the spatially-blocked holdout.

Instrument (v1.0, defined before any result was computed)
---------------------------------------------------------
1. The catalogue is split into spatially interleaved *folds* at the level of connected
   fault segments, so a whole segment is always wholly visible or wholly hidden.  A
   hidden segment is guaranteed to be separated from visible segments by at least
   ``buffer_px`` pixels, otherwise it is dropped from the truth set (this is the
   "withhold whole segments with a buffer" protocol).
2. The scored domain is the footprint minus the visible faults and their buffer, so
   nothing is scored inside ground the detector was allowed to see.
3. Truth = hidden-segment pixels inside the scored domain.
4. Every candidate is emitted under the *same* rule it would face live: rank the surface,
   take the top dots, drop anything within 3 px of the visible faults.
5. Score = pooled distance-weighted Tversky index, alpha 0.2 / beta 0.8, 300 m triangular
   kernel; 95% CI by bootstrapping over *segments* (the unit of dependence), not pixels.

Because a catalogue-free surface (OSLF) never sees any fault label, this instrument is
unbiased for it.  For catalogue-derived surfaces (every registry file) the same numbers
are *not* an unbiased estimate of live skill -- prior sessions measured a rank correlation
of about -0.85 between this style of holdout and the live leaderboard, and that is
reproduced here as a control, not used as a selection criterion.
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import binary_dilation, distance_transform_edt, label

from . import metric

INSTRUMENT_VERSION = "K7-HIDE-RECOVER-1.0"
KERNEL_RADIUS_PX = 3.0
CATALOGUE_CLEARANCE_PX = 3.0


def segment_folds(catalogue: np.ndarray, n_folds: int = 2,
                  structure: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Assign connected fault segments to interleaved folds; return (fold_id, n_segments).

    Segments are ordered by their first pixel in raster order and dealt round-robin, so
    each fold is spread across the whole map rather than being one geographic quadrant.
    """
    structure = np.ones((3, 3), dtype=int) if structure is None else structure
    lbl, n = label(catalogue, structure=structure)
    if n < n_folds:
        raise ValueError(f"only {n} connected segments; cannot build {n_folds} folds")
    fold = np.full(catalogue.shape, -1, dtype=np.int8)
    labels_present = np.unique(lbl[catalogue])
    labels_present = labels_present[labels_present > 0]
    for i, seg in enumerate(labels_present):
        fold[lbl == seg] = i % n_folds
    return fold, int(len(labels_present))


def _buffer(mask: np.ndarray, px: float) -> np.ndarray:
    if px <= 0:
        return mask.copy()
    return binary_dilation(mask, iterations=int(round(px)))


def holdout_split(catalogue: np.ndarray, footprint: np.ndarray, *, fold_id: int = 0,
                  n_folds: int = 2, buffer_px: float = 10.0) -> dict:
    """Build one (visible, hidden, active-domain) split."""
    fold, n_seg = segment_folds(catalogue, n_folds)
    visible = catalogue & (fold != fold_id)
    hidden_all = catalogue & (fold == fold_id)
    if not hidden_all.any():
        raise ValueError("no hidden segments")
    # Only keep hidden pixels that are far enough from every visible fault.
    dist_visible = distance_transform_edt(~visible)
    hidden = hidden_all & (dist_visible > buffer_px)
    if not hidden.any():
        raise ValueError("buffer removed every hidden pixel; reduce buffer_px")
    active = footprint & ~_buffer(visible, buffer_px)
    return {
        "fold_id": fold_id,
        "n_segments": n_seg,
        "visible": visible,
        "hidden": hidden & active,
        "active": active,
        "hidden_pixels_kept": int((hidden & active).sum()),
        "hidden_pixels_discarded_by_buffer": int(hidden_all.sum() - (hidden & active).sum()),
    }


def auc_single_feature(surface: np.ndarray, truth: np.ndarray, domain: np.ndarray) -> dict:
    """Leakage canary: AUC of one feature against the held-out truth (protocol rule 4)."""
    m = domain & np.isfinite(surface)
    y, x = truth[m], surface[m].astype(np.float64)
    n_pos = int(y.sum())
    if n_pos == 0 or n_pos == y.size or np.ptp(x) == 0:
        return {"auc": None, "positives": n_pos, "leakage_suspect": False,
                "reason": "degenerate domain"}
    # Rank-based Mann-Whitney AUC (avoids a scikit-learn dependency in the core path).
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(x.size, dtype=np.float64)
    ranks[order] = np.arange(1, x.size + 1, dtype=np.float64)
    # average ties
    xs = x[order]
    i = 0
    while i < xs.size:
        j = i
        while j + 1 < xs.size and xs[j + 1] == xs[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    r_pos = ranks[y].sum()
    auc = (r_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * (y.size - n_pos))
    return {"auc": float(auc), "positives": n_pos,
            "leakage_suspect": bool(auc > 0.90),
            "rule": "AUC > 0.90 = leakage until proven otherwise"}


def emit_top(surface: np.ndarray, *, budget: int, exclude: np.ndarray,
             allowed: np.ndarray, clearance_px: float = CATALOGUE_CLEARANCE_PX) -> np.ndarray:
    """Take the top-``budget`` finite pixels by surface rank, then apply exclusions.

    Exclusions are applied by *rejection with refill*, so the emitted dot count is exactly
    ``budget`` whenever enough eligible pixels exist.  This matters: comparing candidates at
    different dot counts confounds the metric, so every candidate is compared at a matched
    budget.
    """
    eligible = allowed & np.isfinite(surface)
    if clearance_px > 0 and exclude.any():
        eligible &= distance_transform_edt(~exclude) > clearance_px
    n_elig = int(eligible.sum())
    if n_elig == 0:
        raise ValueError("no eligible pixels to emit")
    budget = min(int(budget), n_elig)
    flat_idx = np.flatnonzero(eligible.ravel())
    vals = surface.ravel()[flat_idx]
    # top-k by value; deterministic tie-break on index
    k = flat_idx.size - budget
    part = np.argpartition(vals, k)[k:]
    keep = part[np.lexsort((flat_idx[part], -vals[part]))]
    mask = np.zeros(surface.size, dtype=bool)
    mask[flat_idx[keep]] = True
    return mask.reshape(surface.shape)


def dti_with_segment_ci(mask: np.ndarray, truth: np.ndarray, domain: np.ndarray,
                        *, n_boot: int = 200, seed: int = 0) -> dict:
    """Pooled HOLDOUT-DTI plus a segment-level bootstrap 95% CI.

    The CI resamples connected truth segments, because pixels inside one segment are
    strongly dependent; a pixel-level bootstrap would be far too narrow and is not used.
    """
    lbl, n = label(truth, structure=np.ones((3, 3), dtype=int))
    base = metric.dti_binary(mask, truth, valid=domain)
    if n < 2:
        return {**base, "instrument": INSTRUMENT_VERSION, "ci95": None,
                "n_segments": n, "note": "fewer than 2 segments: CI undefined"}
    seg_ids = np.unique(lbl[truth])
    # kernel credit of every truth pixel, computed once
    k_truth = metric.kernel(distance_transform_edt(~mask))[truth]
    seg_of_truth = lbl[truth]
    credit_by_seg = {}
    size_by_seg = {}
    for sid in seg_ids:
        sel = seg_of_truth == sid
        credit_by_seg[int(sid)] = float(k_truth[sel].sum())
        size_by_seg[int(sid)] = int(sel.sum())

    rng = np.random.default_rng(seed)
    fp = float(base["fp"])  # not identifiable under resampling; held fixed (stated caveat)
    d = []
    for _ in range(n_boot):
        pick = rng.choice(seg_ids, size=seg_ids.size, replace=True)
        tp = float(sum(credit_by_seg[int(s)] for s in pick))
        n_truth = float(sum(size_by_seg[int(s)] for s in pick))
        tp = min(tp, n_truth)   # TP cannot exceed the resampled truth set
        d.append(tp / (tp + metric.ALPHA * fp + metric.BETA * (n_truth - tp) + metric.EPS))
    lo, hi = np.percentile(d, [2.5, 97.5])
    return {**base, "instrument": INSTRUMENT_VERSION, "n_segments": int(seg_ids.size),
            "ci95": [float(lo), float(hi)],
            "ci_method": "segment bootstrap, 200 reps, FP held at the observed value",
            "ci_caveat": "FP is not identifiable under resampling; the interval reflects "
                         "truth-set sampling error only."}
