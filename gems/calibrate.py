"""Turn a ranking score into a probability.

Why this matters more than usual here
-------------------------------------
FP_w is a *sum* of submitted values over every positive pixel, while TP_w is a
*max* over the kernel.  A model whose background sits at 0.3 therefore pays
0.3 x (number of background positives) in false positives, even if its ranking
is perfect.  Two submission families that differ only in calibration can
differ by a factor of ten in DTI, so calibration is treated as part of the
method, not as cosmetic post-processing.

``isotonic`` is pool-adjacent-violators (monotone least-squares), implemented
here so the repository does not need scikit-learn; ``binned`` is a robust
alternative that also returns the sample count per bin so the report can show
how thin the top bin is.
"""
from __future__ import annotations

import numpy as np


def _pav(y, w):
    """Pool adjacent violators. Returns block values and block boundaries."""
    y = np.asarray(y, dtype=np.float64)
    w = np.asarray(w, dtype=np.float64)
    n = len(y)
    val = list(y)
    wt = list(w)
    cnt = [1] * n
    i = 0
    while i < len(val) - 1:
        if val[i] > val[i + 1]:
            new_w = wt[i] + wt[i + 1]
            new_v = (val[i] * wt[i] + val[i + 1] * wt[i + 1]) / new_w
            val[i:i + 2] = [new_v]
            wt[i:i + 2] = [new_w]
            cnt[i:i + 2] = [cnt[i] + cnt[i + 1]]
            if i > 0:
                i -= 1
        else:
            i += 1
    out = []
    for v, c in zip(val, cnt):
        out.extend([v] * c)
    return np.asarray(out)


def isotonic(scores, labels, n_bins=256):
    """Fit a monotone mapping score -> P(label), returned as a callable."""
    s = np.asarray(scores, dtype=np.float64).ravel()
    y = np.asarray(labels, dtype=np.float64).ravel() > 0.5
    if s.size == 0 or y.sum() == 0:
        raise ValueError("isotonic needs non-empty scores with some positives")
    s = np.where(np.isfinite(s), s, np.nanmin(s[np.isfinite(s)]) if np.isfinite(s).any() else 0.0)
    edges = np.quantile(s, np.linspace(0, 1, n_bins + 1))
    edges = np.unique(edges)
    if edges.size < 3:
        # degenerate (near-constant) scores: fall back to the base rate
        prior = float(np.clip(y.mean(), 1e-6, 1 - 1e-6))
        return (lambda x, clip=1e-6, _p=prior: np.full(np.shape(x), _p, dtype=np.float32),
                {"kind": "constant-prior", "prior": prior, "n_samples": int(y.size)})
    idx = np.clip(np.searchsorted(edges, s, side="right") - 1, 0, len(edges) - 2)
    rate = np.bincount(idx, weights=y.astype(np.float64), minlength=len(edges) - 1)
    cnt = np.bincount(idx, minlength=len(edges) - 1).astype(np.float64)
    ok = cnt > 0
    rate = rate[ok] / cnt[ok]
    centres = 0.5 * (edges[:-1] + edges[1:])[ok]
    mono = _pav(rate, cnt[ok])
    # keep the mapping finite and strictly inside (0, 1)
    mono = np.clip(mono, 1e-6, 1.0 - 1e-6)

    def apply(x, clip=1e-6):
        x = np.asarray(x, dtype=np.float64)
        return np.clip(np.interp(x, centres, mono), clip, 1.0 - clip)

    return apply, {"kind": "isotonic-pav", "n_bins": int(len(centres)),
                   "n_samples": int(s.size), "n_positive": int(y.sum()),
                   "prior": float(y.mean())}


def binned(scores, labels, n_bins=32):
    """Reliability bins; returns ((edges, rates, counts), info)."""
    s = np.asarray(scores, dtype=np.float64).ravel()
    y = np.asarray(labels, dtype=np.float64).ravel() > 0.5
    qs = np.linspace(0, 1, n_bins + 1)
    edges = np.unique(np.quantile(s, qs))
    idx = np.clip(np.searchsorted(edges, s, side="right") - 1, 0, len(edges) - 2)
    rates = np.bincount(idx, weights=y.astype(np.float64), minlength=len(edges) - 1)
    counts = np.bincount(idx, minlength=len(edges) - 1).astype(np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        rates = np.where(counts > 0, rates / np.maximum(counts, 1), np.nan)
    return (edges, rates, counts), {"kind": "reliability-bins", "n_bins": int(len(edges) - 1)}


def apply_binned(edges, rates, scores, clip=1e-6):
    centres = 0.5 * (edges[:-1] + edges[1:])
    ok = np.isfinite(rates)
    if ok.sum() < 2:
        prior = float(np.nanmean(rates))
        return np.full(np.shape(scores), prior, dtype=np.float32)
    return np.clip(np.interp(np.asarray(scores, dtype=np.float64).ravel(),
                             centres[ok], rates[ok]), clip, 1.0 - clip
                   ).astype(np.float32).reshape(np.shape(scores))


def auc(scores, labels):
    """Rank AUC with ties counted as half (no scikit-learn needed)."""
    s = np.asarray(scores, dtype=np.float64).ravel()
    y = np.asarray(labels).ravel() > 0.5
    n_pos = int(y.sum())
    n_neg = int(y.size - n_pos)
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(s.size, dtype=np.float64)
    ranks[order] = np.arange(1, s.size + 1, dtype=np.float64)
    # average ranks for ties
    ss = s[order]
    i = 0
    while i < ss.size:
        j = i
        while j + 1 < ss.size and ss[j + 1] == ss[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    return float((ranks[y].sum() - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))
