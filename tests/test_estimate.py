"""The score estimator: calibration anchor, validation, and its stated limits."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import estimate as E  # noqa: E402


def test_calibration_anchor_reproduces_the_owner_reported_score():
    """The 5-px lattice anchor must round-trip to 0.0904 from the calibrated K."""
    anchor = E.CALIBRATION_ANCHOR
    dots = anchor["dots_measured"]
    c = E.LATTICE_CREDIT[5]
    fwd = E.dti_model(c, dots)
    assert fwd == pytest.approx(anchor["owner_reported_score"], abs=2e-4)


def test_model_predicts_the_optimal_lattice_at_s5():
    """Unfitted validation: the best square lattice under the model is the one chosen."""
    scores = {s: E.dti_model(E.LATTICE_CREDIT[s], int(5_167_373 / s ** 2))
              for s in E.LATTICE_CREDIT}
    assert max(scores, key=scores.get) == 5


def test_lattice_credit_is_monotone_decreasing():
    spacings = sorted(E.LATTICE_CREDIT)
    vals = [E.LATTICE_CREDIT[s] for s in spacings]
    assert all(a > b for a, b in zip(vals, vals[1:]))


def test_implied_coverage_inverts_the_model():
    for score, dots in ((0.2778, 37654), (0.0904, 206895), (0.4413, 37654)):
        c = E.implied_coverage(score, dots)
        assert E.dti_model(c, dots) == pytest.approx(score, abs=1e-9)


def test_estimate_is_labelled_a_model_estimate_never_a_score():
    out = E.estimate((0.02, 0.05), 27159)
    assert out["label"] == "MODEL-ESTIMATE (not a score)"
    lo, hi = out["interval_95"]
    assert lo < out["point_estimate"] < hi
    assert out["caveats"]


def test_unestimable_candidate_returns_no_number():
    out = E.estimate(None, 1000)
    assert out["point_estimate"] is None and out["interval_95"] is None
    assert out["reason"]


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        E.dti_model(0.5, 0)
    with pytest.raises(ValueError):
        E.dti_model(1.5, 10)
