"""Buffered, segment-blocked spatial holdout with a leakage canary.

Design rules (from the run protocol, implemented rather than described):

* whole connected fault segments are withheld, never individual pixels;
* a buffer of ``buffer_px`` around every withheld segment is excluded from
  training *and* from scoring, so no model can win by memorising the ring
  around the hole;
* every catalogue-derived feature is recomputed from the visible faults only;
* the pooled DTI is computed with alpha 0.2, beta 0.8 and the 300 m kernel;
* the 95% interval is a *segment-level* bootstrap, which is the honest unit
  because the scorer is applied to correlated pixels;
* each feature is tested alone; AUC > 0.90 is reported as a leakage canary
  trip and blocks promotion.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

from gems import calibrate, metric as M

CANARY_AUC = 0.90


def segments(labels, min_px=20):
    lab = np.asarray(labels) > 0
    comp, n = ndi.label(lab, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        px = np.argwhere(comp == i)
        if px.shape[0] >= min_px:
            out.append(px)
    return out


def make_folds(labels, k=5, buffer_px=5, seed=0, block=512):
    """Assign whole segments to folds, spread over the map by block.

    Returns a list of dicts: ``withheld`` (pixel mask), ``buffer`` (pixel mask
    including the withheld ring), ``fold_of_segment``.
    """
    lab = np.asarray(labels) > 0
    h, w = lab.shape
    segs = segments(lab)
    if len(segs) < k:
        raise ValueError(f"need at least {k} segments with >=20 px, found {len(segs)}")
    rng = np.random.default_rng(seed)
    # order segments by their block so each fold spans the map
    cents = np.array([[p[:, 0].mean(), p[:, 1].mean()] for p in segs])
    bid = (cents[:, 0] // block).astype(int) * 10_000 + (cents[:, 1] // block).astype(int)
    sizes = np.array([p.shape[0] for p in segs], dtype=float)
    # largest segments first, each into the currently lightest fold: keeps the
    # withheld pixel count per fold comparable, which stabilises the CI
    order = np.argsort(-sizes + rng.normal(0, 1e-6, size=sizes.size))
    fold_of = np.empty(len(segs), dtype=int)
    load = np.zeros(k)
    for idx in order:
        f = int(np.argmin(load))
        fold_of[idx] = f
        load[f] += sizes[idx]
    folds = []
    for f in range(k):
        withheld = np.zeros((h, w), dtype=bool)
        for idx in np.flatnonzero(fold_of == f):
            withheld[segs[idx][:, 0], segs[idx][:, 1]] = True
        ring = ndi.binary_dilation(withheld, np.ones((2 * buffer_px + 1,) * 2))
        folds.append({"fold": f, "withheld": withheld, "buffer": ring,
                      "n_withheld_px": int(withheld.sum())})
    return folds


def fold_targets(labels, fold):
    """Truth for a fold: exactly the withheld fault cells."""
    lab = np.asarray(labels) > 0
    return (lab & fold["withheld"]).astype(np.float32)


def train_mask(fold):
    """Cells usable for training: everything except the buffered hole."""
    return ~fold["buffer"]


def scoring_mask(fold):
    """Cells that may contribute to the score.

    The buffer ring is excluded: it was withheld from training, so charging
    false positives there would punish a model for the experimenter's choice,
    not for its own error.  Everything else, including the withheld cells
    themselves, is scored.
    """
    return ~(fold["buffer"] & ~fold["withheld"])


def canary(features, truth, mask=None):
    """Univariate AUC of each feature against the withheld truth."""
    out = {}
    lab = (np.asarray(truth) > 0).astype(np.float32)
    if mask is not None:
        m = np.asarray(mask, dtype=bool)
    for name, arr in features.items():
        x = np.asarray(arr, dtype=np.float32)
        if mask is not None:
            x = x[m]
            y = lab[m]
        else:
            y = lab
        a = calibrate.auc(x.ravel(), y.ravel())
        out[name] = {"auc": None if not np.isfinite(a) else round(float(a), 4),
                     "leakage_canary": bool(np.isfinite(a) and a > CANARY_AUC)}
    return out


def pooled_dti(pred, truth, mask=None):
    return M.dti(pred, truth, mask=mask)


def bootstrap_ci(per_segment_scores, n_boot=2000, seed=0):
    """95% interval of the mean, resampling segments (the honest unit)."""
    v = np.asarray([s for s in per_segment_scores if np.isfinite(s)], dtype=float)
    if v.size < 3:
        return {"mean": float(v.mean()) if v.size else float("nan"),
                "lo": None, "hi": None, "n": int(v.size)}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    means = v[idx].mean(axis=1)
    return {"mean": float(v.mean()), "lo": float(np.percentile(means, 2.5)),
            "hi": float(np.percentile(means, 97.5)), "n": int(v.size),
            "method": "segment bootstrap, 2000 resamples"}
