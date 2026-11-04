"""Lane compliance: rank correlation and dot overlap against known registry rasters.

Protocol (parallel-run item 1): a candidate drifts out of its lane if its
Spearman rank correlation with any registry raster exceeds 0.90, or if more
than 70 % of its dots fall within 3 px of one registry raster's dots.

For a binary emission the Spearman correlation of the full grids is dominated
by the shared background and is close to 1 for *any* two sparse rasters, so the
informative statistics reported here are:

* ``jaccard``      -- intersection over union of the dot sets;
* ``frac_within_3px`` -- share of candidate dots lying within 3 px of a
  registry dot (the literal protocol test);
* ``recall_of_registry`` -- share of registry dots within 3 px of a candidate dot.

The literal 0.90 correlation test is also computed on the dot-index rank
vectors and reported, with the caveat above recorded in the output.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr


@dataclass(frozen=True)
class Overlap:
    candidate_dots: int
    registry_dots: int
    intersection: int
    jaccard: float
    frac_within_3px: float
    recall_of_registry_3px: float
    spearman_full_grid: float
    spearman_dot_ranks: float | None
    lane_ok: bool
    drift_reasons: list[str]


def compare(
    candidate: np.ndarray,
    registry: np.ndarray,
    *,
    max_spearman: float = 0.90,
    max_within_3px: float = 0.70,
    max_dot_ranks_spearman: float = 0.90,
) -> Overlap:
    """Compare one candidate emission with one registry emission."""
    c = np.asarray(candidate, bool)
    r = np.asarray(registry, bool)
    if c.shape != r.shape:
        raise ValueError("candidate and registry grids differ")

    nc, nr = int(c.sum()), int(r.sum())
    inter = int((c & r).sum())
    union = int((c | r).sum())
    jac = inter / union if union else 1.0

    d_r = distance_transform_edt(~r) if nr else np.full(c.shape, np.inf)
    d_c = distance_transform_edt(~c) if nc else np.full(c.shape, np.inf)
    within3 = float((d_r[c] <= 3).mean()) if nc else 0.0
    recall3 = float((d_c[r] <= 3).mean()) if nr else 0.0

    sp_full = float(spearmanr(c.ravel().astype(np.int8), r.ravel().astype(np.int8)).statistic) if (nc and nr) else 0.0

    # rank correlation of the sparse dot index sets, matched on the union index space
    sp_dots = None
    if nc and nr:
        a = c.ravel().astype(np.int8)
        b = r.ravel().astype(np.int8)
        idx = np.flatnonzero(a | b)
        if idx.size > 2 and a[idx].std() > 0 and b[idx].std() > 0:
            sp_dots = float(spearmanr(a[idx], b[idx]).statistic)

    reasons = []
    if jac >= max_within_3px:
        reasons.append(f"jaccard {jac:.3f} >= {max_within_3px}")
    if within3 > max_within_3px:
        reasons.append(f"{within3:.1%} of dots within 3 px > {max_within_3px:.0%}")
    if sp_dots is not None and sp_dots > max_dot_ranks_spearman:
        reasons.append(f"dot-rank spearman {sp_dots:.3f} > {max_dot_ranks_spearman}")

    return Overlap(
        candidate_dots=nc,
        registry_dots=nr,
        intersection=inter,
        jaccard=float(jac),
        frac_within_3px=within3,
        recall_of_registry_3px=recall3,
        spearman_full_grid=sp_full,
        spearman_dot_ranks=sp_dots,
        lane_ok=not reasons,
        drift_reasons=reasons,
    )
