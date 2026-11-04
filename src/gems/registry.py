"""Forensics and lane-uniqueness measurements for the nine focus-site rasters.

Every number this module produces is measured from the raster bytes in
``data/registry/``; none is copied from a website.  The reported leaderboard
scores carried alongside are OWNER-REPORTED (no organiser receipt exists) and
are kept in ``data/registry/receipts.json`` as data, not as code.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt, label
from scipy.stats import rankdata

from . import grid

REGISTRY_DIR = Path(__file__).resolve().parents[2] / "data" / "registry"
RECEIPTS = REGISTRY_DIR / "receipts.json"

SITES = ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28",
         "GEMSDOE30", "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36")


def load_receipts() -> dict:
    return json.loads(RECEIPTS.read_text())


def registry_files() -> dict[str, Path]:
    """Map site -> raster path for the highest-scoring submission of each focus site."""
    out = {}
    for rec in load_receipts()["sites"]:
        p = REGISTRY_DIR / rec["file"]
        if not p.exists():
            raise FileNotFoundError(p)
        if grid.sha256(p) != rec["sha256"]:
            raise ValueError(f"{rec['site']}: registry hash mismatch (file edited?)")
        out[rec["site"]] = p
    return out


def dots(path: str | Path, footprint: np.ndarray) -> np.ndarray:
    a = grid.read_grid(path)
    inside = footprint & np.isfinite(a)
    return inside & (a >= 0.5) if np.nanmax(a) <= 1.0 + 1e-6 else inside & (a > 0)


def distance_to_catalogue(catalogue: np.ndarray) -> np.ndarray:
    """Euclidean pixel distance to the nearest catalogue fault pixel."""
    return distance_transform_edt(~catalogue)


def catalogue_ring_census(mask: np.ndarray, dist: np.ndarray) -> dict:
    d = dist[mask]
    return {
        "dots": int(mask.sum()),
        "le_1px": int((d <= 1).sum()),
        "le_2px": int((d <= 2).sum()),
        "le_3px": int((d <= 3).sum()),
        "gt_3px": int((d > 3).sum()),
        "frac_le_2px": float((d <= 2).mean()) if d.size else None,
        "frac_le_3px": float((d <= 3).mean()) if d.size else None,
    }


def overlap_within_3px(a: np.ndarray, b: np.ndarray) -> float:
    """Fraction of a's dots lying within 3 px of one of b's dots."""
    if not a.any():
        return 0.0
    if not b.any():
        return 0.0
    return float((distance_transform_edt(~b)[a] <= 3).mean())


def surface_rank_correlation(a: np.ndarray, b: np.ndarray, footprint: np.ndarray) -> float:
    x = rankdata(a[footprint])
    y = rankdata(b[footprint])
    if np.ptp(x) == 0 or np.ptp(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def pairwise(masks: dict[str, np.ndarray]) -> dict:
    sites = sorted(masks)
    out = {}
    for i, s1 in enumerate(sites):
        for s2 in sites[i + 1:]:
            a, b = masks[s1], masks[s2]
            inter = int((a & b).sum())
            union = int((a | b).sum())
            out[f"{s1}|{s2}"] = {
                "intersection": inter,
                "union": union,
                "iou": inter / union if union else None,
                "frac_a_within_3px_of_b": overlap_within_3px(a, b),
                "frac_b_within_3px_of_a": overlap_within_3px(b, a),
                "a_subset_of_b": bool(inter == int(a.sum())),
                "b_subset_of_a": bool(inter == int(b.sum())),
                "symmetric_difference": int((a ^ b).sum()),
            }
    return out


def implied_coverage(dti: float, dots: int) -> dict:
    """Invert the metric algebra to express a reported score as required recall.

    With binary predictions, ``TP + FP = dots`` exactly, so

        DTI = T / (0.2*dots + 0.8*K).

    Writing ``c = T/K`` for kernel-weighted recall and solving for N = dots
    given DTI and K:

        K = DTI * (0.2*N + 0.8*K) / c  ->  for a *fully precise* submission
        (FP = 0) this reduces to  DTI = c / (0.2c + 0.8).

    ``K`` (the number of withheld truth pixels in the scored domain) is not
    observable from here, so this returns a one-parameter family: the recall the
    submission must have achieved *if every emitted dot were on target*.
    """
    if not 0.0 < dti < 1.0:
        raise ValueError("DTI must be in (0, 1)")
    c = 0.8 * dti / (1.0 - 0.2 * dti)
    return {
        "reported_dti": dti,
        "dots": int(dots),
        "implied_recall_if_zero_false_positives": c,
        "note": ("Interpretation aid only: 'if this many dots were all on target, the score "
                 "implies this recall'. Not a measurement and not a projection."),
    }


def marginal_bar(current_dti: float, alpha: float = 0.2) -> dict:
    """Add-a-dot rule for binary predictions where TP + FP == dots.

        DTI' > DTI  <=>  gamma > alpha * DTI

    ``gamma`` is the expected kernel credit of the new dot: the probability it
    lands within 300 m of a withheld fault times the mean triangular kernel
    weight there.  This is exact, not a heuristic, under the stated identity.
    """
    return {
        "current_dti": current_dti,
        "alpha": alpha,
        "required_mean_kernel_credit_per_dot": alpha * current_dti,
        "equivalent_hit_rate_at_credit_0.5": alpha * current_dti / 0.5,
        "equivalent_hit_rate_at_credit_1.0": alpha * current_dti,
    }


def label_components(mask: np.ndarray) -> np.ndarray:
    return label(mask, structure=np.ones((3, 3), dtype=int))[0]
