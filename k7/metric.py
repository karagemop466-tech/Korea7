"""Exact Distance-Weighted Tversky Index (DTI) for the DOE GEMS Prize.

Published definition
--------------------
The competition problem description (DrivenData, GEMS page 967, section
"Performance metric") specifies a distance-weighted Tversky index with
``alpha = 0.2`` (false-positive weight), ``beta = 0.8`` (false-negative weight)
and a triangular kernel of radius ``R = 300 m``.  At the competition grid
resolution of 100 m, ``R`` is exactly 3 pixels.

    TP_w = sum_{g in G} max_{x : d(x,g) <= R}  p(x) * max(1 - d(x,g)/R, 0)
    FP_w = sum_{x : p(x) > 0}  p(x) * (1 - max_{g in G} max(1 - d(x,g)/R, 0))
    FN_w = |G| - TP_w
    DTI  = TP_w / (TP_w + alpha*FP_w + beta*FN_w + eps)

Two independent implementations are provided.  ``dti_soft`` handles arbitrary
predictions in ``[0, 1]``; ``dti_bruteforce`` is a literal O(|G|*|P|)
transcription used only by the unit tests to prove the fast path is correct.
``tests/test_metric.py`` asserts agreement to 1e-9 on random inputs.
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import distance_transform_edt

ALPHA: float = 0.2
BETA: float = 0.8
RADIUS_PX: float = 3.0
KERNEL_RADIUS_M: float = 300.0
PIXEL_M: float = 100.0
EPS: float = 1e-12


def kernel(d: np.ndarray | float) -> np.ndarray:
    """Triangular kernel ``max(1 - d/R, 0)``; ``d`` in pixels, ``R = 3 px = 300 m``."""
    return np.maximum(1.0 - np.asarray(d, dtype=np.float64) / RADIUS_PX, 0.0)


def _offsets() -> list[tuple[int, int, float]]:
    r = int(np.ceil(RADIUS_PX))
    out: list[tuple[int, int, float]] = []
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            k = float(kernel(np.hypot(dy, dx)))
            if k > 0.0:
                out.append((dy, dx, k))
    return out


OFFSETS: tuple[tuple[int, int, float], ...] = tuple(_offsets())


def _shift(a: np.ndarray, dy: int, dx: int) -> np.ndarray:
    """Shift ``a`` by (dy, dx) with zero fill. Exact here because all inputs are >= 0."""
    out = np.zeros_like(a)
    h, w = a.shape
    ys0, ys1 = max(0, dy), min(h, h + dy)
    xs0, xs1 = max(0, dx), min(w, w + dx)
    out[ys0:ys1, xs0:xs1] = a[max(0, -dy):min(h, h - dy), max(0, -dx):min(w, w - dx)]
    return out


def _prepare(pred, truth, valid):
    p = np.asarray(pred, dtype=np.float64)
    g = np.asarray(truth, dtype=bool)
    if p.ndim != 2 or p.shape != g.shape:
        raise ValueError(f"prediction and truth must be equal-shaped 2-D grids, got {p.shape} vs {g.shape}")
    if valid is not None:
        m = np.asarray(valid, dtype=bool)
        if m.shape != p.shape:
            raise ValueError("valid-mask shape mismatch")
        p = np.where(m, p, 0.0)
        g = g & m
    if not np.isfinite(p).all():
        raise ValueError("prediction contains non-finite values")
    return np.clip(p, 0.0, 1.0), g


def components(pred, truth, valid=None) -> dict:
    """Return the exact sufficient statistics ``TP_w``, ``FP_w``, ``FN_w`` and DTI."""
    p, g = _prepare(pred, truth, valid)
    n = int(g.sum())
    if n == 0:
        return {"tp": 0.0, "fp": float(p.sum()), "fn": 0.0, "n_truth": 0, "dti": 0.0, "coverage": 0.0}
    if not (p > 0).any():
        return {"tp": 0.0, "fp": 0.0, "fn": float(n), "n_truth": n, "dti": 0.0, "coverage": 0.0}

    best = np.zeros(p.shape, dtype=np.float64)
    for dy, dx, k in OFFSETS:
        np.maximum(best, _shift(p, dy, dx) * k, out=best)
    best = np.clip(best, 0.0, 1.0)
    tp = float(best[g].sum())

    d_truth = distance_transform_edt(~g)
    fp = float((p * (1.0 - kernel(d_truth))).sum())
    fn = float(n) - tp
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "n_truth": n,
        "dti": float(tp / (tp + ALPHA * fp + BETA * fn + EPS)),
        "coverage": tp / n,
    }


def dti(pred, truth, valid=None) -> float:
    """Scalar DTI."""
    return components(pred, truth, valid)["dti"]


def dti_from_components(tp: float, fp: float, fn: float) -> float:
    """DTI from published sufficient statistics (used for pooling across folds)."""
    return float(tp / (tp + ALPHA * fp + BETA * fn + EPS))


def dti_bruteforce(pred, truth, radius: float = RADIUS_PX, alpha: float = ALPHA, beta: float = BETA) -> dict:
    """Literal O(|G|*|P|) transcription of the published equations. Unit-test oracle only."""
    pred = np.asarray(pred, dtype=np.float64)
    truth = np.asarray(truth, dtype=bool)
    gs = np.argwhere(truth)
    xs = np.argwhere(pred > 0)
    tp = 0.0
    for g in gs:
        best = 0.0
        for x in xs:
            d = float(np.hypot(*(x - g)))
            if d <= radius:
                best = max(best, pred[tuple(x)] * max(1.0 - d / radius, 0.0))
        tp += best
    fp = 0.0
    for x in xs:
        kmax = 0.0
        for g in gs:
            kmax = max(kmax, max(1.0 - float(np.hypot(*(x - g))) / radius, 0.0))
        fp += pred[tuple(x)] * (1.0 - kmax)
    fn = float(len(gs)) - tp
    return {"tp": tp, "fp": fp, "fn": fn, "dti": tp / (tp + alpha * fp + beta * fn + 1e-12)}
