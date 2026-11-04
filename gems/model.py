"""Small, dependency-free models: ridge logistic regression and block splits."""
from __future__ import annotations

import numpy as np


def fit_logistic(X, y, l2=1.0, iters=60, tol=1e-6, class_weight="balanced"):
    """Ridge-penalised logistic regression by Newton/IRLS (numpy only).

    X must already be standardised; an intercept is added internally.
    ``class_weight='balanced'`` re-weights the two classes to equal total
    weight.  Without it a strong 'distance to mapped faults' feature separates
    the training data almost perfectly and drives the intercept to -infinity,
    which is precisely the failure the segment holdout is built to expose: the
    model then returns probability ~0 for every withheld fault.  The balanced
    fit gives a well-spread score, and isotonic calibration afterwards restores
    the real base rate.
    """
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64).ravel()
    n, p = X.shape
    A = np.hstack([np.ones((n, 1)), X])
    if class_weight == "balanced":
        pos = max(y.sum(), 1.0)
        neg = max(n - pos, 1.0)
        cw = np.where(y > 0.5, n / (2.0 * pos), n / (2.0 * neg))
    else:
        cw = np.ones(n)
    coef = np.zeros(p + 1)
    pen = np.full(p + 1, l2)
    pen[0] = 0.0                      # never penalise the intercept
    pen[0] = 1e-8                     # (tiny value keeps H invertible)
    hist = []
    for _ in range(iters):
        z = A @ coef
        mu = 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))
        sw = cw * np.maximum(mu * (1.0 - mu), 1e-9)
        g = A.T @ (cw * (y - mu)) - pen * coef
        H = (A * sw[:, None]).T @ A + np.diag(pen)
        step = np.linalg.solve(H, g)
        coef = coef + step
        hist.append(float(np.abs(step).max()))
        if hist[-1] < tol:
            break
    return {"coef": coef[1:], "intercept": float(coef[0]), "iters": len(hist),
            "max_step": hist[-1] if hist else None, "class_weight": class_weight}


def predict_logistic(model, X):
    X = np.asarray(X, dtype=np.float64)
    z = model["intercept"] + X @ model["coef"]
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def block_ids(shape, block=512):
    """Assign every pixel to a square block id (spatial block cross-validation)."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    return (yy // block).astype(np.int32) * (int(np.ceil(w / block)) + 1) + (xx // block)


def fold_assignment(block_ids_arr, k=5, seed=0):
    """Map block ids to folds, so whole spatial blocks move together."""
    ids = np.unique(block_ids_arr)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(ids.size)
    lookup = {int(b): int(perm[i] % k) for i, b in enumerate(ids)}
    out = np.empty(block_ids_arr.shape, dtype=np.int8)
    for b, f in lookup.items():
        out[block_ids_arr == b] = f
    return out
