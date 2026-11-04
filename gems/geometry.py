"""Fault-trace geometry: tips, along-strike extension, gap closure, proximity.

These are the ingredients every catalogue-anchored submission family needs.
They are re-implemented here from first principles (endpoint = a line pixel
with exactly one 8-neighbour; local strike = weighted principal axis of the
nearby trace) so that the repository owns and can test its own version.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

EIGHT = np.ones((3, 3))


def endpoints(binary, min_neighbours=1, max_neighbours=1):
    """Cells of a 1-px trace having exactly ``min..max`` 8-neighbours."""
    b = np.asarray(binary) > 0
    k = ndi.convolve(b.astype(np.int16), EIGHT.astype(np.int16), mode="constant", cval=0)
    n = k - b.astype(np.int16)          # exclude self
    return b & (n >= min_neighbours) & (n <= max_neighbours)


def local_strike(binary, y, x, r=4):
    """Unit vector of the local trace direction at (y, x), or None."""
    b = np.asarray(binary) > 0
    h, w = b.shape
    y0, y1 = max(0, y - r), min(h, y + r + 1)
    x0, x1 = max(0, x - r), min(w, x + r + 1)
    yy, xx = np.nonzero(b[y0:y1, x0:x1])
    if yy.size < 3:
        return None
    yy = yy + y0
    xx = xx + x0
    # weight pixels towards the tip more heavily (they define outgoing strike)
    d2 = (yy - y) ** 2 + (xx - x) ** 2
    wgt = 1.0 / (1.0 + d2)
    my = np.average(yy, weights=wgt)
    mx = np.average(xx, weights=wgt)
    cov = np.cov(np.vstack([yy - my, xx - mx]), aweights=wgt)
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, int(np.argmax(evals))]      # (dy, dx)
    # orient away from the trace centroid
    if v[0] * (y - my) + v[1] * (x - mx) < 0:
        v = -v
    return v


def extend_tips(binary, length=3, r=4):
    """Rasterise a straight continuation of ``length`` px beyond every tip."""
    out = np.zeros_like(np.asarray(binary), dtype=np.float32)
    b = np.asarray(binary) > 0
    tips = np.argwhere(endpoints(b))
    h, w = b.shape
    for y, x in tips:
        v = local_strike(b, int(y), int(x), r=r)
        if v is None:
            continue
        for t in np.arange(1.0, length + 0.5, 0.5):
            yy = int(round(y + v[0] * t))
            xx = int(round(x + v[1] * t))
            if 0 <= yy < h and 0 <= xx < w:
                out[yy, xx] = 1.0
    return out


def gap_closure(binary, max_gap=15.0, angle_tol_deg=35.0, r=4):
    """Join tip pairs that face each other across a short gap (a relay/step-over).

    Two tips are joined when their outgoing strikes point at each other
    within ``angle_tol_deg`` and the straight distance is at most ``max_gap``
    pixels.  This encodes 'the fault continues through the gap', which is the
    single most common way a mapped trace is incomplete.
    """
    b = np.asarray(binary) > 0
    h, w = b.shape
    tips = np.argwhere(endpoints(b))
    vecs = []
    keep = []
    for y, x in tips:
        v = local_strike(b, int(y), int(x), r=r)
        if v is not None:
            keep.append((int(y), int(x)))
            vecs.append(v)
    out = np.zeros_like(b, dtype=np.float32)
    cos_tol = np.cos(np.deg2rad(angle_tol_deg))
    n = len(keep)
    if n < 2:
        return out
    P = np.asarray(keep, dtype=np.float64)
    V = np.asarray(vecs, dtype=np.float64)
    for i in range(n):
        d = P - P[i]
        dist = np.hypot(d[:, 0], d[:, 1])
        cand = np.flatnonzero((dist > 2) & (dist <= max_gap))
        for j in cand:
            u = d[j] / dist[j]
            if (V[i] @ u) > cos_tol and (V[j] @ -u) > cos_tol:
                steps = int(np.ceil(dist[j] * 2))
                t = np.linspace(0, 1, steps + 1)
                ys = np.rint(P[i, 0] + t * d[j, 0]).astype(int)
                xs = np.rint(P[i, 1] + t * d[j, 1]).astype(int)
                out[np.clip(ys, 0, h - 1), np.clip(xs, 0, w - 1)] = 1.0
    return out


def proximity_field(binary, sigma=2.0, cap=12.0):
    """exp(-d^2 / (2 sigma^2)) on the Euclidean distance to the nearest trace."""
    b = np.asarray(binary) > 0
    d = ndi.distance_transform_edt(~b)
    d = np.minimum(d, cap)
    return np.exp(-(d ** 2) / (2.0 * sigma ** 2)).astype(np.float32)


def dilate(binary, r=1):
    b = np.asarray(binary) > 0
    if r <= 0:
        return b.astype(np.float32)
    return ndi.binary_dilation(b, structure=np.ones((2 * r + 1, 2 * r + 1))).astype(np.float32)
