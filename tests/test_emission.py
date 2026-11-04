import numpy as np
import pytest

from gems import emission, metric as M


def test_threshold_formula():
    # the Dinkelbach rule: emit where q > lam*alpha/(1-lam*(1-beta))
    q = np.linspace(0, 1, 101, dtype=np.float32).reshape(1, -1)
    for lam in (0.2, 0.3, 0.5):
        sel = emission.threshold_emission(q, lam)
        t = lam * 0.2 / (1 - lam * 0.2)
        assert sel.sum() == int((q >= t).sum())


def test_topk_emits_exactly_k_and_keeps_shape():
    q = np.random.default_rng(0).random((30, 40)).astype(np.float32)
    sel = emission.topk_emission(q, 100)
    assert sel.shape == q.shape
    assert int(sel.sum()) == 100
    flat = np.argsort(q.ravel())[-100:]
    assert (sel.ravel()[flat] == 1).all()


def test_dilation_widens_and_costs():
    q = np.zeros((9, 9), np.float32)
    q[4, 4] = 1.0
    thr = emission.threshold_emission(q, 0.3)
    assert M.dti(thr, thr)["score"] > M.dti(emission.dilate(thr, 1), thr)["score"]


def test_nms_is_a_subset_of_the_threshold_map():
    q = np.random.default_rng(1).random((20, 20)).astype(np.float32)
    thr = emission.threshold_emission(q, 0.3)
    nms = emission.nms_emission(q, 0.3)
    assert (nms <= thr).all()


def test_expected_dti_of_perfect_map_is_high():
    q = np.zeros((20, 20), np.float32)
    q[10, 10] = 1.0
    sel = np.zeros_like(q)
    sel[10, 10] = 1.0
    assert emission.expected_dti(q, sel) > 0.99


def test_coverage_emission_emits_binary_and_is_bounded():
    rng = np.random.default_rng(2)
    q = (rng.random((60, 60)) < 0.05).astype(np.float32) * 0.6
    sel, info = emission.coverage_emission(q, lam0=0.3, rounds=2, top_k=200, outer=2)
    assert set(np.unique(sel)).issubset({0.0, 1.0})
    assert sel.sum() > 0
    assert "dinkelbach" in info


def test_higher_lambda_emits_fewer_cells():
    rng = np.random.default_rng(3)
    q = (rng.random((60, 60)) < 0.05).astype(np.float32) * 0.6
    lo, _ = emission.coverage_emission(q, lam0=0.2, rounds=2, top_k=200, outer=1)
    hi, _ = emission.coverage_emission(q, lam0=0.6, rounds=2, top_k=200, outer=1)
    assert hi.sum() <= lo.sum()


def test_truth_proximity_max_mode_is_below_independence_mode():
    q = np.full((40, 40), 0.02, np.float32)
    assert emission.truth_proximity(q, "max").max() <= emission.truth_proximity(q, "independence").max()
