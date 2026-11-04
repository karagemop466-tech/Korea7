"""Distance-weighted Tversky index (DTI) for the DOE GEMS Prize.

Definition used by every other module (transcribed from the competition's
problem description as quoted and independently implemented by two public
repositories; see docs/verification.md):

    k(d)  = max(1 - d / R, 0)                    triangular kernel, R = 300 m
    TP_w  = sum_{g in G} max_{x} p(x) * k(d(x, g))       (a MAX --> density is free)
    FN_w  = |G| - TP_w
    FP_w  = sum_{x : p(x) > 0} p(x) * (1 - max_{g in G} k(d(x, g)))   (a SUM)
    DTI   = TP_w / (TP_w + alpha * FP_w + beta * FN_w + eps),  alpha=0.2, beta=0.8

The asymmetry between ``max`` in TP_w and ``sum`` in FP_w is the single most
important fact about this metric: spreading probability mass around a fault
buys no extra true-positive credit but is charged in full as false positive.
Any map with a non-zero background (a raw sigmoid field) is therefore
catastrophic, while a binary map is not.
"""
from __future__ import annotations

import math

import numpy as np

ALPHA = 0.2
BETA = 0.8
RADIUS_PX = 3.0
EPS = 1e-9

KERNEL_VERSION = "dti-tri-300m-a0.2-b0.8-v1"


def kernel_offsets(radius_px: float = RADIUS_PX):
    """All (dy, dx, weight) with weight = 1 - d/radius > 0, plus the centre."""
    r = int(math.floor(radius_px))
    offs = [(0, 0, 1.0)]
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            d = math.hypot(dy, dx)
            if 0.0 < d < radius_px:
                offs.append((dy, dx, 1.0 - d / radius_px))
    return offs


_OFFSETS = kernel_offsets()


def as_float(a) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    return np.where(np.isfinite(a), a, 0.0).astype(np.float32)


def binarize_truth(truth, threshold: float = 0.5) -> np.ndarray:
    """Truth is a fault pixel where the label raster exceeds ``threshold``.

    The official reference notebook uses ``y[y < 1] = 0`` on a 0/1 label
    raster, i.e. an effective threshold of 1.0; the default 0.5 agrees with it
    on 0/1 data and is safer on interpolated labels.
    """
    t = as_float(truth)
    return t > threshold


def _coverage(p: np.ndarray, t: np.ndarray):
    """Return (best, near) arrays used for TP_w and FP_w."""
    r = int(math.floor(RADIUS_PX))
    h, w = p.shape
    pp = np.pad(p, r)
    tp_ = np.pad(t.astype(np.float32), r)
    best = np.zeros((h, w), dtype=np.float32)
    near = np.zeros((h, w), dtype=np.float32)
    for dy, dx, k in _OFFSETS:
        win = (slice(r + dy, r + dy + h), slice(r + dx, r + dx + w))
        np.maximum(best, pp[win] * np.float32(k), out=best)
        np.maximum(near, tp_[win] * np.float32(k), out=near)
    return best, near


def dti(pred, truth, alpha: float = ALPHA, beta: float = BETA, mask=None,
        truth_threshold: float = 0.5) -> dict:
    """Fast vectorised DTI. ``mask`` (bool) restricts scoring to its True cells."""
    p = np.clip(as_float(pred), 0.0, 1.0)
    t = binarize_truth(truth, truth_threshold)
    if mask is not None:
        m = np.asarray(mask, dtype=bool)
        if m.shape != p.shape:
            raise ValueError("mask shape mismatch")
        p = np.where(m, p, np.float32(0.0))
        t = t & m
    best, near = _coverage(p, t)
    n = int(t.sum())
    tp = float(best[t].sum(dtype=np.float64))
    fp = float((p * (1.0 - near)).sum(dtype=np.float64))
    fn = float(n) - tp
    return {"tp": tp, "fp": fp, "fn": fn, "n": n,
            "score": score_from_counts(tp, fp, fn, alpha, beta),
            "alpha": alpha, "beta": beta, "kernel_version": KERNEL_VERSION}


def score_from_counts(tp: float, fp: float, fn: float,
                      alpha: float = ALPHA, beta: float = BETA) -> float:
    return float(tp / (tp + alpha * fp + beta * fn + EPS))


def dti_reference(pred, truth, alpha: float = ALPHA, beta: float = BETA,
                  mask=None, truth_threshold: float = 0.5) -> dict:
    """Plain-Python DTI, O(n * 25). Only for unit tests and hand-checked grids."""
    p = np.clip(as_float(pred), 0.0, 1.0)
    t = binarize_truth(truth, truth_threshold)
    if mask is not None:
        m = np.asarray(mask, dtype=bool)
        p = np.where(m, p, np.float32(0.0))
        t = t & m
    h, w = p.shape
    offs = _OFFSETS
    tp = 0.0
    n = 0
    for y in range(h):
        for x in range(w):
            if not t[y, x]:
                continue
            n += 1
            best = 0.0
            for dy, dx, k in offs:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w:
                    v = float(p[yy, xx]) * k
                    if v > best:
                        best = v
            tp += best
    fp = 0.0
    for y in range(h):
        for x in range(w):
            if p[y, x] <= 0:
                continue
            near = 0.0
            for dy, dx, k in offs:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and t[yy, xx]:
                    if k > near:
                        near = k
            fp += float(p[y, x]) * (1.0 - near)
    fn = float(n) - tp
    return {"tp": tp, "fp": fp, "fn": fn, "n": n,
            "score": score_from_counts(tp, fp, fn, alpha, beta),
            "alpha": alpha, "beta": beta, "kernel_version": KERNEL_VERSION}


def band_table(width_px: int = 1, offset_px: float = 0.0,
               alpha: float = ALPHA, beta: float = BETA) -> float:
    """Exact DTI of an infinite straight band of ``width_px`` against a parallel
    straight truth fault, with the band's inner edge ``offset_px`` pixels away.

    Implemented exactly (not analytically) on a tall, one-column-wide grid with
    the scoring restricted to interior rows by a mask, so the answer carries no
    edge effect and no approximation. Used as a hand-checkable anchor.
    """
    n = 200
    pad = 10
    t = np.zeros((n, 1), dtype=np.float32)
    t[:, 0] = 1.0                      # truth: the x = 0 column
    p = np.zeros((n, 1 + int(np.ceil(offset_px)) + width_px), dtype=np.float32)
    start = int(round(offset_px))
    p[:, start:start + width_px] = 1.0
    mask = np.zeros_like(p, dtype=bool)
    mask[pad:n - pad, :] = True
    # widen truth to the prediction's width so the mask applies to both
    tt = np.zeros_like(p, dtype=np.float32)
    tt[:, 0] = 1.0
    return dti(p, tt, alpha=alpha, beta=beta, mask=mask)["score"]
