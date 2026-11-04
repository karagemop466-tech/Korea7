import numpy as np
import pytest

from gems import metric as M


def dot(n=21, y=10, x=10):
    a = np.zeros((n, n), np.float32)
    a[y, x] = 1.0
    return a


def test_hand_worked_points():
    t = dot()
    assert M.dti(dot(), t)["score"] == pytest.approx(1.0, abs=1e-6)
    assert M.dti(dot(x=11), t)["score"] == pytest.approx(2 / 3, abs=1e-4)
    assert M.dti(dot(x=12), t)["score"] == pytest.approx(1 / 3, abs=1e-4)
    assert M.dti(dot(x=13), t)["score"] == 0.0          # outside the 3 px kernel


def test_worked_example_from_the_description():
    # the published worked example: tp 3, fp 1.89, fn 2 -> 0.60
    assert M.score_from_counts(3, 1.89, 2) == pytest.approx(0.6027, abs=1e-3)


def test_empty_prediction_scores_zero():
    assert M.dti(np.zeros((21, 21), np.float32), dot())["score"] == 0.0


def test_dense_background_is_catastrophic():
    pred = np.full((201, 201), 0.02, np.float32)
    truth = dot(201, 100, 100)
    assert M.dti(pred, truth)["score"] < 1e-3


def test_fast_equals_reference_on_random_grids():
    rng = np.random.default_rng(0)
    for _ in range(5):
        t = (rng.random((17, 19)) < 0.08).astype(np.float32)
        p = (rng.random((17, 19)) < 0.10).astype(np.float32) * 0.8
        a, b = M.dti(p, t), M.dti_reference(p, t)
        assert a["tp"] == pytest.approx(b["tp"], abs=1e-4)
        assert a["fp"] == pytest.approx(b["fp"], abs=1e-4)
        assert a["score"] == pytest.approx(b["score"], abs=1e-6)


def test_nan_and_out_of_range_are_clipped_not_propagated():
    t = dot()
    p = dot()
    p[3, 3] = np.nan
    r = M.dti(p, t)
    assert np.isfinite(r["score"])
    p2 = dot() * 5.0
    assert M.dti(p2, t)["score"] <= 1.0


def test_mask_restricts_scoring():
    t = dot()
    p = dot()
    m = np.zeros((21, 21), bool)
    m[0:5, 0:5] = True
    assert M.dti(p, t, mask=m)["n"] == 0


def test_band_table_shape_penalty():
    # one-pixel band on target is perfect; wide bands are strictly worse
    assert M.band_table(1, 0) == pytest.approx(1.0, abs=1e-6)
    assert M.band_table(3, 0) < M.band_table(1, 0)
    assert M.band_table(5, 0) < M.band_table(3, 0)
    assert M.band_table(1, 3) == 0.0


def test_kernel_offsets_are_the_25_cells_within_3_px():
    offs = M.kernel_offsets()
    assert len(offs) == 25
    assert max(k for *_, k in offs) == 1.0
    assert all(0 < k <= 1.0 for *_, k in offs)
