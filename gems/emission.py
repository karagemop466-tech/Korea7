"""Turning a probability field into a submission: DTI-optimal emission.

The problem
-----------
The competition metric is *not* a per-pixel classification score.  With
``p`` the submitted value and ``T`` the truth set::

    TP_w = sum_{g in T} max_{x} p(x) k(d(x,g))      <-- a MAX
    FP_w = sum_{x: p(x)>0} p(x) (1 - max_{g in T} k) <-- a SUM

so the value of an extra positive pixel is *submodular*: it earns true-positive
credit only for the truth cells it newly covers (a pixel 3 px from one you
already emitted earns nothing), while it is charged a full false-positive
count whenever no truth lies within 300 m.  Optimising a threshold on a
probability field ignores this structure: it double-charges coverage (many
pixels for one truth cell) and under-charges recall.

What this module does
---------------------
``coverage_emission`` maximises an *expected* DTI

    E[DTI](S) = E[TP](S) / ( E[TP](S) + alpha E[FP](S) + beta E[FN](S) )

by (i) an outer Dinkelbach loop that turns the ratio into a linear objective
at the current best score ``lam``, and (ii) an inner greedy that adds the
pixel with the largest marginal ratio gain, recomputing coverage after each
addition.  The inner objective is submodular in ``S``, so plain greedy is
within ``1 - 1/e`` of the best any selection of the same size can do; the
outer loop only re-weights the terms, so the whole procedure is a
well-founded heuristic, not a proven global optimum.  That distinction is
stated everywhere the method is reported.

Baselines implemented for comparison are the ones the public run names
suggest are in common use: plain thresholding, threshold + dilation (a
"band"), 3x3 non-maximum suppression, and top-k dots.
"""
from __future__ import annotations

import numpy as np

from gems import metric as _m

ALPHA, BETA = _m.ALPHA, _m.BETA
R = 3  # kernel radius in pixels


# ---------------------------------------------------------------- baselines
def threshold_emission(q, lam=0.30, alpha=ALPHA, beta=BETA):
    """Emit where q exceeds the Dinkelbach threshold lam*alpha/(1-lam(1-beta))."""
    t = lam * alpha / (1.0 - lam * (1.0 - beta))
    return (np.asarray(q) >= t).astype(np.float32)


def dilate(binary, r=1):
    from scipy import ndimage as ndi
    b = np.asarray(binary) > 0
    if r <= 0:
        return b.astype(np.float32)
    return ndi.binary_dilation(b, structure=np.ones((2 * r + 1, 2 * r + 1))).astype(np.float32)


def nms_emission(q, lam=0.30, size=3):
    """Local-maximum suppression above a threshold (the usual ridge-thinning)."""
    from scipy import ndimage as ndi
    q = np.asarray(q, dtype=np.float32)
    t = lam * ALPHA / (1.0 - lam * (1.0 - BETA))
    peak = ndi.maximum_filter(q, size=size)
    return ((q >= t) & (q >= peak - 1e-12)).astype(np.float32)


def topk_emission(q, k):
    """The k highest-scoring pixels, emitted at 1.0 (a 'dots' submission)."""
    q = np.asarray(q, dtype=np.float32)
    shape = q.shape
    flat = q.ravel()
    k = int(min(k, flat.size))
    out = np.zeros(flat.size, dtype=np.float32)
    if k > 0:
        idx = np.argpartition(flat, -k)[-k:]
        out[idx] = 1.0
    return out.reshape(shape)


# ---------------------------------------------------------- expected counts
def _pairs():
    return [(dy, dx, k) for dy, dx, k in _m._OFFSETS if k > 0.0 and (dy or dx)]


_PAIRS = _pairs()


def _coverage_map(sel):
    """best[g] = max_x sel(x) k(d(x,g)) : how well each cell is covered."""
    sel = np.asarray(sel, dtype=np.float32)
    h, w = sel.shape
    pad = np.pad(sel, R)
    best = np.zeros((h, w), dtype=np.float32)
    for dy, dx, k in _PAIRS:
        win = (slice(R + dy, R + dy + h), slice(R + dx, R + dx + w))
        np.maximum(best, pad[win] * np.float32(k), out=best)
    return np.maximum(best, sel)


def truth_proximity(q, mode="max"):
    """c[x] = P(at least one truth cell lies within the kernel of x).

    Faults are *continuous* structures, so the naive independence product over
    the 49-cell window is badly biased upwards: 49 cells each at 0.05 would
    give 0.92, yet they are one fault, not 49 independent draws.  The default
    therefore uses the max approximation (the window is 'covered' to the extent
    of its most likely cell), which is the standard treatment for a correlated
    field.  ``mode='independence'`` is kept for comparison and is reported as
    conservative-in-the-wrong-direction: it makes false positives look free.
    """
    from scipy import ndimage as ndi
    q = np.clip(np.asarray(q, dtype=np.float64), 0.0, 1.0 - 1e-9)
    if mode == "independence":
        logc = np.log1p(-q)
        tot = ndi.uniform_filter(logc, size=2 * R + 1, mode="constant", cval=0.0)
        tot *= (2 * R + 1) ** 2
        return np.clip(1.0 - np.exp(tot), 0.0, 1.0)
    best = ndi.maximum_filter(q, size=2 * R + 1, mode="constant", cval=0.0)
    # soften by one cell so a single optimistic pixel does not make a whole
    # neighbourhood look safe
    return np.clip(ndi.uniform_filter(best, size=3, mode="constant", cval=0.0),
                   0.0, 1.0)


def expected_counts(q, sel):
    """Expected (TP_w, FP_w, FN_w) of a binary selection. ``q`` = P(cell in T)."""
    q = np.clip(np.asarray(q, dtype=np.float64), 0.0, 1.0)
    sel = (np.asarray(sel) > 0).astype(np.float32)
    best = _coverage_map(sel)
    etp = float((q * best).sum(dtype=np.float64))
    prox = truth_proximity(q)
    efp = float(((1.0 - prox) * (sel > 0)).sum(dtype=np.float64))
    efn = max(float(q.sum(dtype=np.float64)) - etp, 0.0)
    return etp, efp, efn


def expected_dti(q, sel, alpha=ALPHA, beta=BETA):
    etp, efp, efn = expected_counts(q, sel)
    return float(etp / (etp + alpha * efp + beta * efn + 1e-9))


# ------------------------------------------------------- coverage emission
def _gains(q, best, prox, lam, alpha, beta):
    """Vectorised marginal gain for every cell (single pass over the kernel)."""
    q32 = np.asarray(q, dtype=np.float32)
    h, w = q32.shape
    pad = np.pad(q32, R)
    bestp = np.pad(best, R)
    gain = np.zeros((h, w), dtype=np.float32)
    for dy, dx, k in _PAIRS:
        win = (slice(R + dy, R + dy + h), slice(R + dx, R + dx + w))
        contrib = np.float32(k) * pad[win] * (bestp[win] < np.float32(k))
        gain += contrib
    cost = (1.0 - prox).astype(np.float32) / np.float32(alpha)
    t = lam / (1.0 - lam * (1.0 - beta))       # gain must exceed t * (1 - prox)/alpha
    del cost
    return gain, t


def _greedy_fixed(q, lam, rounds, top_k, prox, candidate, alpha, beta, verbose=False):
    """Greedy selection at a *fixed* Dinkelbach score lam, from an empty map."""
    h, w = q.shape
    sel = np.zeros((h, w), dtype=np.float32)
    t = lam / (1.0 - lam * (1.0 - beta))
    added_total = 0
    for rnd in range(rounds):
        best = _coverage_map(sel)
        gain, _ = _gains(q, best, prox, lam, alpha, beta)
        thr = np.float32(t / alpha) * (1.0 - prox).astype(np.float32)
        ok = candidate & (sel == 0) & (gain > thr)
        if not ok.any():
            break
        idx = np.flatnonzero(ok.ravel())
        g = gain.ravel()[idx]
        order = idx[np.argsort(-g)[:top_k]]
        added = 0
        for flat in order:
            y, x = divmod(int(flat), w)
            y0, y1 = max(0, y - R), min(h, y + R + 1)
            x0, x1 = max(0, x - R), min(w, x + R + 1)
            patch_best = best[y0:y1, x0:x1]
            patch_q = q[y0:y1, x0:x1]
            yy, xx = np.mgrid[y0:y1, x0:x1]
            d = np.hypot(yy - y, xx - x)
            kk = np.where(d < R, 1.0 - d / R, 0.0).astype(np.float32)
            dtp = float((patch_q * np.maximum(kk - patch_best, 0.0)).sum())
            if dtp <= t * float(1.0 - prox[y, x]) / alpha:
                continue
            np.maximum(patch_best, kk, out=patch_best)
            sel[y, x] = 1.0
            added += 1
        added_total += added
        if verbose:
            print(f"     round {rnd}: +{added} (total {int(sel.sum())}) at lam {lam:.3f}")
        if added == 0:
            break
    return sel, added_total


def coverage_emission(q, lam0=0.25, rounds=6, top_k=4000, alpha=ALPHA, beta=BETA,
                      candidate=None, outer=3, damp=0.5, verbose=False):
    """Select cells to emit at 1.0, maximising the expected DTI.

    Dinkelbach is applied *properly*: each outer iteration re-solves the whole
    selection problem at the current best score and then updates that score
    from the resulting map.  (Extending a single growing map while the score
    rises would leave the early, over-dense cells in place; that mistake is
    visible as an emitted count far above the optimum.)  ``damp`` averages the
    score update to avoid oscillation between dense and sparse solutions.
    """
    q = np.clip(np.asarray(q, dtype=np.float32), 0.0, 1.0)
    h, w = q.shape
    if candidate is None:
        candidate = q > 0
    else:
        candidate = np.asarray(candidate, dtype=bool) & (q > 0)
    prox = truth_proximity(q).astype(np.float32)
    lam = float(lam0)
    hist = []
    sel = np.zeros((h, w), dtype=np.float32)
    for it in range(outer):
        sel, added = _greedy_fixed(q, lam, rounds, top_k, prox, candidate,
                                   alpha, beta, verbose=verbose)
        etp, efp, efn = expected_counts(q, sel)
        lam_new = float(etp / (etp + alpha * efp + beta * efn + 1e-9))
        hist.append({"outer": it, "lam_in": round(lam, 5),
                     "lam_out": round(lam_new, 5), "n_emitted": int(sel.sum()),
                     "e_tp": round(etp, 2), "e_fp": round(efp, 2),
                     "e_fn": round(efn, 2)})
        if verbose:
            print("   ", hist[-1])
        if it > 0 and abs(lam_new - lam) < 1e-3:
            lam = lam_new
            break
        lam = (1.0 - damp) * lam + damp * lam_new
    return sel, {"dinkelbach": hist, "lambda_final": lam}
