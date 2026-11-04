"""The vendored metric must reproduce a literal transcription of the published equations."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import metric as M  # noqa: E402


def brute(pred, truth, radius=3.0):
    p = np.asarray(pred, float)
    g = np.asarray(truth).astype(bool)
    h, w = p.shape
    gt = np.argwhere(g)
    tp = 0.0
    for gy, gx in gt:
        best = 0.0
        for y in range(h):
            for x in range(w):
                d = math.hypot(y - gy, x - gx)
                if d <= radius:
                    best = max(best, p[y, x] * max(1.0 - d / radius, 0.0))
        tp += best
    fp = 0.0
    for y in range(h):
        for x in range(w):
            if p[y, x] > 0:
                near = max((max(1.0 - math.hypot(y - gy, x - gx) / radius, 0.0)
                            for gy, gx in gt), default=0.0)
                fp += p[y, x] * (1.0 - near)
    return tp, fp, len(gt) - tp


def test_published_worked_example():
    # problem description: TP=3.00, FP=1.89, FN=2.00 -> 0.60
    assert M.dti(3.00, 1.89, 2.00) == pytest.approx(0.6026, abs=5e-4)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_exact_matches_literal_transcription(seed):
    rng = np.random.default_rng(seed)
    h, w = 26, 24
    truth = np.zeros((h, w), bool)
    truth[8, 4:20] = True
    truth[17, 6:18] = True
    p = rng.random((h, w))
    got = M.dti_exact(p, truth)
    tp, fp, fn = brute(p, truth)
    assert got["tp"] == pytest.approx(tp, abs=1e-9)
    assert got["fp"] == pytest.approx(fp, abs=1e-9)
    assert got["fn"] == pytest.approx(fn, abs=1e-9)


def test_binary_agrees_with_exact():
    rng = np.random.default_rng(5)
    truth = np.zeros((40, 40), bool)
    truth[10, 5:35] = True
    m = np.zeros((40, 40), bool)
    m[rng.choice(1600, 120, replace=False).reshape(-1) // 40,
      rng.choice(1600, 120, replace=False).reshape(-1) % 40] = True
    a = M.dti_binary(m, truth)["dti"]
    b = M.dti_exact(m.astype(float), truth)["dti"]
    assert a == pytest.approx(b, abs=1e-9)


def test_known_faults_are_masked_out_of_both_terms():
    """A dot on a known fault contributes neither TP nor FP (organiser clarification 11516)."""
    truth = np.zeros((20, 20), bool)
    truth[5, 5:15] = True
    known = np.zeros((20, 20), bool)
    known[14, 5:15] = True
    m = np.zeros((20, 20), bool)
    m[14, 5:15] = True                      # sits entirely inside the known-fault mask
    masked = M.dti_binary(m, truth, known=known)
    unmasked = M.dti_binary(m, truth)
    assert unmasked["fp"] == 10.0
    assert masked["fp"] == 0.0 and masked["tp"] == 0.0


def test_range_and_shape_validation():
    truth = np.zeros((10, 10), bool)
    truth[5, 5] = True
    bad = np.zeros((10, 10))
    bad[1, 1] = 1.5
    with pytest.raises(ValueError):
        M.dti_exact(bad, truth)
    with pytest.raises(ValueError):
        M.dti_exact(np.zeros((9, 10)), truth)
