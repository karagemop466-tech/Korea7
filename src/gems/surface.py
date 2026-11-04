"""Candidate surface: the Off-catalogue Seismogenic Lineament Field (OSLF).

Design rationale
----------------
Measured fact (evidence/registry_forensics.json): the highest-scoring file in the
programme has a *catalogue* recovery of DTI 0.0067 -- below a uniform random field of
the same size (0.0692) -- because it deliberately removes every dot within 2 px of the
mapped catalogue.  The leaderboard therefore rewards predicting faults that are *not*
in the visible labels, and it mildly punishes predicting the labels themselves.

A model trained on the visible labels is optimised in the wrong direction.  The only
physically defensible alternative is a ranking surface built from an *independent*
observation of active faulting that never touches the catalogue except as an exclusion
mask.  The one such observation reachable from this sandbox is the INGENIOUS
declustered earthquake-rate field (GDR submission 1391, CC BY 4.0): earthquakes occur on
active structures whether or not they have been mapped, and a lineament of epicentres is
the classical seismological signature of an unmapped fault.

The surface is deliberately simple and pre-registered (see docs/hypotheses.md) so that it
cannot be tuned against the catalogue:

    L = log1p(seismic)                       (variance-stabilising)
    Sm = gaussian(L, sigma_smooth)
    R  = max_theta  -(Hessian of Sm projected on theta)     (oriented ridge response)
    G  = |grad Sm|                                          (structure-boundary magnitude)
    S  = 0.60 * z(R) + 0.25 * z(G) + 0.15 * z(Sm)

Weights, the 6 orientations and the smoothing scale were fixed before any catalogue-DTI
was computed.  They were NOT selected on the catalogue, which is the point.
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter, gaussian_filter1d

ORIENTATIONS_DEG = (0.0, 30.0, 60.0, 90.0, 120.0, 150.0)
WEIGHTS = {"ridge": 0.60, "gradient": 0.25, "intensity": 0.15}
SMOOTH_SIGMA_PX = 4.0


def log_seismic(seismic: np.ndarray, footprint: np.ndarray) -> np.ndarray:
    """log1p of the rate field, with non-finite values set to the footprint minimum."""
    x = np.array(seismic, dtype=np.float64)
    bad = ~np.isfinite(x)
    if bad.all():
        raise ValueError("seismic layer has no finite values")
    x[bad] = np.nanmin(x[footprint & ~bad]) if (footprint & ~bad).any() else 0.0
    x = np.clip(x, 0.0, None)
    return np.log1p(x)


def oriented_ridge(smoothed: np.ndarray) -> np.ndarray:
    """Maximum ridge (negative along-strike-normal curvature) over six orientations."""
    gy = gaussian_filter1d(smoothed, SMOOTH_SIGMA_PX, axis=0, order=1)
    gy = gaussian_filter1d(gy, SMOOTH_SIGMA_PX, axis=1, order=0)
    gx = gaussian_filter1d(smoothed, SMOOTH_SIGMA_PX, axis=0, order=0)
    gx = gaussian_filter1d(gx, SMOOTH_SIGMA_PX, axis=1, order=1)
    gyy = gaussian_filter1d(smoothed, SMOOTH_SIGMA_PX, axis=0, order=2)
    gyy = gaussian_filter1d(gyy, SMOOTH_SIGMA_PX, axis=1, order=0)
    gxx = gaussian_filter1d(smoothed, SMOOTH_SIGMA_PX, axis=0, order=0)
    gxx = gaussian_filter1d(gxx, SMOOTH_SIGMA_PX, axis=1, order=2)
    gxy = gaussian_filter1d(smoothed, SMOOTH_SIGMA_PX, axis=0, order=1)
    gxy = gaussian_filter1d(gxy, SMOOTH_SIGMA_PX, axis=1, order=1)

    best = np.full(smoothed.shape, -np.inf, dtype=np.float64)
    for theta in ORIENTATIONS_DEG:
        t = np.deg2rad(theta)
        c, s = np.cos(t), np.sin(t)
        # second derivative along the ridge-normal direction
        curvature = gxx * c * c + 2.0 * gxy * c * s + gyy * s * s
        np.maximum(best, -curvature, out=best)
    return best, np.hypot(gx, gy)


def zscore(x: np.ndarray, footprint: np.ndarray) -> np.ndarray:
    v = x[footprint]
    mu, sd = float(v.mean()), float(v.std())
    if sd == 0.0:
        raise ValueError("degenerate feature: zero variance inside the footprint")
    return (x - mu) / sd


def build(seismic: np.ndarray, footprint: np.ndarray) -> dict:
    """Return the OSLF surface (higher = more likely to be an unmapped fault)."""
    L = log_seismic(seismic, footprint)
    Sm = gaussian_filter(L, SMOOTH_SIGMA_PX, mode="nearest")
    R, G = oriented_ridge(L)
    S = (WEIGHTS["ridge"] * zscore(R, footprint)
         + WEIGHTS["gradient"] * zscore(G, footprint)
         + WEIGHTS["intensity"] * zscore(Sm, footprint))
    S = np.where(footprint & np.isfinite(S), S, np.nan).astype(np.float32)
    if not np.isfinite(S[footprint]).all():
        raise ValueError("surface has non-finite values inside the footprint")
    return {
        "surface": S,
        "components": {"ridge": R.astype(np.float32), "gradient": G.astype(np.float32),
                       "intensity": Sm.astype(np.float32)},
        "weights": WEIGHTS,
        "orientations_deg": list(ORIENTATIONS_DEG),
        "smooth_sigma_px": SMOOTH_SIGMA_PX,
    }
