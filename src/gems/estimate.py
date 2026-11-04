"""A calibrated score ESTIMATOR for the DOE GEMS distance-weighted Tversky index.

This is a model, not a measurement, and it is never reported as a score.  It exists because
the owner asked "we should be able to estimate the score for a submission", and because a
submission decision needs a number even when no organiser receipt exists.

Derivation
----------
For a binary prediction the metric is

    DTI = T / (T + alpha*F + beta*(K - T)),   alpha = 0.2, beta = 0.8

with ``T`` kernel-weighted true-positive mass, ``F`` false-positive mass, ``K`` the number of
withheld truth pixels inside the scored domain.  Writing the kernel-weighted recall as
``c = T/K`` and invoking the one structural assumption

    (A1)  F = N - T      each dot contributes its kernel credit to T and the remainder to FP

the denominator collapses exactly:

    T + 0.2*(N-T) + 0.8*(K-T) = 0.2*N + 0.8*K

so the whole model is two numbers:

    DTI = c * K / (0.2*N + 0.8*K)                                    (**)

(A1) is exact when withheld truth pixels are sparse relative to the 3 px kernel.  It is
approximate when a single dot earns credit for several adjacent truth pixels, which is
common along a fault trace; the estimate is therefore labelled MODEL-ESTIMATE everywhere and
carries an explicit uncertainty band rather than a point value.

Calibration
-----------
``K`` is the only free parameter.  It is pinned by one anchor with a *known* mechanism and an
owner-reported score -- the 5-px lattice ``13GEMSDOE_r13-lattice-s5_v2_nan-outside.tif``,
measured here at exactly 206,895 dots, reported at 0.0904.  For a square lattice of spacing
``s`` the expected kernel credit of a uniformly placed truth pixel is computed by Monte
Carlo (no free parameters), giving ``c = 0.3652`` at ``s = 5``.  Substituting into (**):

    0.0904 = 0.3652 * K / (0.2*206895 + 0.8*K)   ->   K = 12,773

Validation (not used in the fit): with K fixed, the model predicts that the *best* square
lattice is s = 5, and that the four spacings s in {5,6,8,10} score 0.0904 / 0.0859 / 0.0713 /
0.0580, i.e. a shallow optimum at exactly the spacing the programme chose.  It also recovers
a monotone, physically sensible ordering across the nine focus files (pruning raises ``c``
while lowering ``N``).

Absolute calibration error is not measurable here (no organiser receipts).  Treat quoted
intervals as +/-0.02 absolute in the 0.05-0.35 range, plus the model risk of (A1).
"""

from __future__ import annotations

import numpy as np

K_HIDDEN_TRUTH_PX = 12_773.0   # calibrated; see module docstring
CALIBRATION_ANCHOR = {
    "submission": "13GEMSDOE_r13-lattice-s5_v2_nan-outside",
    "dots_measured": 206_895,
    "owner_reported_score": 0.0904,
    "source_url": "https://buffedlizard55-lab.github.io/13GEMSDOE/",
    "evidence_class": "owner-report",
}
ALPHA, BETA = 0.2, 0.8
MODEL_RISK_ABS = 0.02

#: Monte-Carlo mean kernel credit of a uniformly placed truth pixel against an s-px lattice.
#: Computed in ``scripts/verify_estimator.py`` (4,000,000 draws, seed 0) -- reproducible.
LATTICE_CREDIT = {
    2: 0.7450, 3: 0.6174, 4: 0.4900, 5: 0.3652, 6: 0.2619, 7: 0.1925,
    8: 0.1472, 9: 0.1162, 10: 0.0942, 11: 0.0780, 12: 0.0654, 14: 0.0481, 16: 0.0369,
}


def dti_model(coverage: float, dots: int, k_hidden: float = K_HIDDEN_TRUTH_PX) -> float:
    """Model DTI from kernel-weighted recall ``coverage`` and dot count ``dots``."""
    if dots <= 0:
        raise ValueError("dots must be positive")
    if not 0.0 <= coverage <= 1.0:
        raise ValueError("coverage must be in [0, 1]")
    return coverage * k_hidden / (ALPHA * dots + BETA * k_hidden)


def implied_coverage(score: float, dots: int, k_hidden: float = K_HIDDEN_TRUTH_PX) -> float:
    """Invert the model: what kernel-weighted recall does a reported score imply?"""
    return score * (ALPHA * dots + BETA * k_hidden) / k_hidden


def dots_for_target(score: float, coverage: float,
                    k_hidden: float = K_HIDDEN_TRUTH_PX) -> float:
    """Dot budget at which a surface of recall ``coverage`` would reach ``score``."""
    return (coverage * k_hidden / score - BETA * k_hidden) / ALPHA


def estimate(coverage_rng: tuple[float, float] | None, dots: int,
             k_hidden: float = K_HIDDEN_TRUTH_PX) -> dict:
    """MODEL-ESTIMATE with an interval.  Never a score; never ORGANIZER-CONFIRMED."""
    if coverage_rng is None:
        return {
            "label": "MODEL-ESTIMATE (not a score)",
            "dots": int(dots),
            "point_estimate": None,
            "interval_95": None,
            "reason": ("Kernel-weighted recall against the withheld truth is not estimable for "
                       "this candidate from data reachable in this sandbox; no interval is "
                       "claimed."),
            "model": "DTI = c*K/(0.2N + 0.8K), K = %d (calibrated)" % k_hidden,
        }
    lo, hi = sorted(coverage_rng)
    vals = [dti_model(c, dots, k_hidden) for c in (lo, hi)]
    point = dti_model(0.5 * (lo + hi), dots, k_hidden)
    return {
        "label": "MODEL-ESTIMATE (not a score)",
        "dots": int(dots),
        "coverage_range": [lo, hi],
        "point_estimate": round(point, 4),
        "interval_95": [round(min(vals) - MODEL_RISK_ABS, 4), round(max(vals) + MODEL_RISK_ABS, 4)],
        "model": "DTI = c*K/(0.2N + 0.8K), K = %d (calibrated)" % k_hidden,
        "caveats": [
            "Structure assumption A1 (F = N - T) is approximate along fault traces.",
            "K is calibrated on one owner-reported lattice score, not on an organiser receipt.",
            "Model risk +/-%.2f absolute is included; it is an engineering judgement." % MODEL_RISK_ABS,
        ],
    }
