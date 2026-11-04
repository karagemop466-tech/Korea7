"""Instrument definitions: folds, matched-budget emission, canary, CI."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import screen  # noqa: E402


def lattice_truth(h=60, w=60):
    t = np.zeros((h, w), bool)
    t[10, 5:55] = True
    t[30, 5:55] = True
    t[45, 5:30] = True
    return t


def test_segment_folds_never_split_a_segment():
    t = lattice_truth()
    a, n = screen.segment_folds(t, 2)
    assert n == 3
    # every segment carries exactly one fold id
    for seg in range(n):
        ids = np.unique(a[t & (np.isin(a, [i % 2 for i in range(n)]))])
    assert set(np.unique(a[t])) <= {0, 1}
    # no pixel of a connected segment is in the other fold
    from scipy.ndimage import label
    lbl, _ = label(t, structure=np.ones((3, 3)))
    for s in np.unique(lbl[t]):
        assert len(np.unique(a[lbl == s])) == 1


def test_holdout_keeps_a_buffer_around_visible_faults():
    t = lattice_truth()
    split = screen.holdout_split(t, np.ones_like(t), fold_id=0, buffer_px=4.0)
    from scipy.ndimage import distance_transform_edt
    d = distance_transform_edt(~split["visible"])[split["hidden"]]
    assert d.min() > 4.0


def test_emit_top_hits_the_budget_exactly_and_respects_the_collar():
    rng = np.random.default_rng(0)
    s = rng.random((40, 40)).astype(np.float32)
    allowed = np.ones((40, 40), bool)
    exclude = np.zeros((40, 40), bool)
    exclude[20, 20] = True
    m = screen.emit_top(s, budget=100, exclude=exclude, allowed=allowed, clearance_px=3.0)
    assert m.sum() == 100
    from scipy.ndimage import distance_transform_edt
    assert distance_transform_edt(~exclude)[m].min() > 3.0


def test_emit_top_refuses_an_empty_domain():
    s = np.zeros((10, 10), np.float32)
    with pytest.raises(ValueError):
        screen.emit_top(s, budget=5, exclude=np.zeros((10, 10), bool),
                        allowed=np.zeros((10, 10), bool), clearance_px=0)


def test_auc_is_one_for_a_perfect_feature_and_half_for_noise():
    rng = np.random.default_rng(1)
    truth = np.zeros((50, 50), bool)
    truth[20, 10:40] = True
    domain = np.ones((50, 50), bool)
    perfect = truth.astype(np.float32)
    assert screen.auc_single_feature(perfect, truth, domain)["auc"] == pytest.approx(1.0)
    noise = rng.random((50, 50)).astype(np.float32)
    assert abs(screen.auc_single_feature(noise, truth, domain)["auc"] - 0.5) < 0.06


def test_leakage_flag_fires_above_ninety():
    truth = np.zeros((40, 40), bool)
    truth[20, 5:35] = True
    leaky = truth.astype(np.float32) + np.random.default_rng(2).random((40, 40)).astype(np.float32) * 0.1
    assert screen.auc_single_feature(leaky, truth, np.ones((40, 40), bool))["leakage_suspect"]


def test_ci_brackets_the_point_estimate():
    truth = lattice_truth(80, 80)
    mask = np.zeros_like(truth)
    mask[12, 5:50] = True
    r = screen.dti_with_segment_ci(mask, truth, np.ones_like(truth), n_boot=60, seed=0)
    if r["ci95"]:
        assert r["ci95"][0] <= r["dti"] <= r["ci95"][1]
