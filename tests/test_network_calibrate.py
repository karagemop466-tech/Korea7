import numpy as np

from gems import network as N


def test_generator_reproduces_density_anchor():
    net = N.make_calibrated_network(shape=(900, 900), seed=0)
    st = N.stats(net)
    assert 0.010 < st["density"] < 0.020
    assert 0.06 < st["coverage_300m"] < 0.10


def test_perturbation_reduces_agreement_and_makes_unmapped_cells():
    net = N.make_calibrated_network(shape=(900, 900), seed=0)
    cat = N.perturb(net, seed=3, omission=0.08, jitter_px=0.5)
    score = None
    from gems import metric as M
    score = M.dti(cat, net)["score"]
    assert 0.6 < score < 0.95
    near = M._coverage(np.zeros_like(cat), cat > 0)[1] > 0
    unmapped = (net > 0) & (~near)
    assert unmapped.sum() > 100


def test_shifted_control_scores_near_chance():
    from gems import metric as M
    net = N.make_calibrated_network(shape=(900, 900), seed=1)
    assert M.dti(N.shifted(net, seed=5), net)["score"] < 0.15
