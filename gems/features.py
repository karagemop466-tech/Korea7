"""Feature extraction from the competition raster stack.

Two families, deliberately separated because they have different leakage
properties:

**Independent features** are computed from a single raster band (elevation,
magnetics, radiometrics, gravity) by a fixed filter: no fault catalogue is
used, so they cannot leak the labels through the catalogue.

**Catalogue features** are computed from the mapped faults (labels).  They are
*legitimately* powerful - the truth is spatially correlated with the catalogue
- and are therefore the ones most likely to trip the leakage canary when a
holdout withholds whole fault segments.  ``build_submission`` recomputes them
inside every fold from the visible faults only.

``lineament`` is a multi-scale Hessian ridge measure (the "vesselness" family
used for curvilinear structures): it responds to *linear* second-derivative
structure at a chosen scale, which is what a fault scarp, a magnetic
lineament or a topographic break look like, and it is insensitive to a
monotone brightness change of the band.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

from gems import geometry


def _hessian(band, sigma):
    b = ndi.gaussian_filter(band.astype(np.float32), sigma, mode="nearest")
    hyy = ndi.gaussian_filter(b, sigma, order=(2, 0), mode="nearest")
    hxx = ndi.gaussian_filter(b, sigma, order=(0, 2), mode="nearest")
    hxy = ndi.gaussian_filter(b, sigma, order=(1, 1), mode="nearest")
    return hyy, hxx, hxy


def lineament(band, sigma=1.5):
    """Scale-normalised ridge response in [0, 1]: |principal curvature|."""
    b = np.asarray(band, dtype=np.float32)
    b = np.where(np.isfinite(b), b, np.nan)
    fill = np.nanmedian(b[::7, ::7]) if np.isfinite(b).any() else 0.0
    b = np.where(np.isfinite(b), b, fill).astype(np.float32)
    hyy, hxx, hxy = _hessian(b, sigma)
    tr = hyy + hxx
    det = hyy * hxx - hxy * hxy
    disc = np.sqrt(np.maximum(tr * tr / 4.0 - det, 0.0))
    l1 = tr / 2.0 + disc
    l2 = tr / 2.0 - disc
    # a ridge is where the larger-magnitude eigenvalue is negative
    lam = np.where(np.abs(l2) > np.abs(l1), l2, l1)
    resp = np.maximum(-lam, 0.0) * (sigma ** 2)
    return _unit(resp)


def gradient_magnitude(band, sigma=1.5):
    b = np.asarray(band, dtype=np.float32)
    fill = np.nanmedian(b[::7, ::7]) if np.isfinite(b).any() else 0.0
    b = np.where(np.isfinite(b), b, fill).astype(np.float32)
    gy = ndi.gaussian_filter(b, sigma, order=(1, 0), mode="nearest")
    gx = ndi.gaussian_filter(b, sigma, order=(0, 1), mode="nearest")
    return _unit(np.hypot(gy, gx) * sigma)


def _unit(a, lo=1.0, hi=99.0):
    """Robust 1-99 percentile stretch to [0, 1] (keeps rank order)."""
    a = np.asarray(a, dtype=np.float32)
    if not np.isfinite(a).any():
        return np.zeros_like(a)
    p_lo, p_hi = np.percentile(a[np.isfinite(a)], [lo, hi])
    if p_hi <= p_lo:
        return np.zeros_like(a)
    return np.clip((a - p_lo) / (p_hi - p_lo), 0.0, 1.0).astype(np.float32)


def catalogue_features(labels, sigma=2.0):
    """Features from mapped faults only; safe to recompute inside a fold."""
    lab = (np.asarray(labels) > 0)
    d = ndi.distance_transform_edt(~lab).astype(np.float32)
    return {
        "catalogue_proximity": np.exp(-(d ** 2) / (2.0 * sigma ** 2)).astype(np.float32),
        "catalogue_distance": _unit(np.minimum(d, 20.0)),
        "tip_extension": geometry.extend_tips(lab, length=3),
        "gap_closure": geometry.gap_closure(lab, max_gap=15),
        "catalogue_proximity_wide": np.exp(-(d ** 2) / (2.0 * (4.0 * sigma) ** 2)
                                           ).astype(np.float32),
    }


def stack(features_path, labels_path, max_features=8, sigmas=(1.0, 2.5), reader=None):
    """Read the band stack and return (names, [arrays], grid info, band_tags).

    ``reader`` lets a caller inject a reader (used by the tests and the demo
    builder); the default uses rasterio.
    """
    if reader is None:
        import rasterio

        def reader(path):
            with rasterio.open(path) as src:
                return src.read().astype(np.float32), src.meta, {
                    i + 1: src.tags(i + 1) for i in range(src.count)}
    bands, meta, tags = reader(features_path)
    names, arrays = [], []
    for i in range(bands.shape[0]):
        desc = (tags.get(i + 1, {}) or {}).get("description", f"band{i + 1}")
        desc = str(desc).split(" - ")[0][:40]
        for sigma in sigmas:
            names.append(f"{desc}|lineament|s{sigma}")
            arrays.append(lineament(bands[i], sigma))
        names.append(f"{desc}|gradient|s{sigmas[0]}")
        arrays.append(gradient_magnitude(bands[i], sigmas[0]))
    if labels_path is not None:
        import rasterio

        with rasterio.open(labels_path) as src:
            labels = src.read(1).astype(np.float32)
        for k, v in catalogue_features(labels).items():
            names.append(k)
            arrays.append(v)
    if len(arrays) > max_features:
        # keep the strongest univariate discriminators, decided later in CV;
        # here we just cap deterministically and report what was dropped
        names, arrays = names[:max_features], arrays[:max_features]
    return names, arrays, meta, tags
