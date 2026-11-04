import json

import numpy as np
import pytest

from gems import holdout as H, network as N, registry, writer


def test_folds_withhold_disjoint_segments():
    net = N.make_calibrated_network(shape=(400, 400), seed=0)
    folds = H.make_folds(net, k=4, buffer_px=5)
    seen = np.zeros_like(net, bool)
    for f in folds:
        t = H.fold_targets(net, f) > 0
        assert not (t & seen).any(), "a segment appears in two folds"
        assert not (t & ~f["buffer"]).any(), "withheld cells must be inside the buffer"
        seen |= t
    assert seen.any()


def test_train_mask_excludes_the_buffer():
    net = N.make_calibrated_network(shape=(300, 300), seed=1)
    f = H.make_folds(net, k=3, buffer_px=4)[0]
    assert not (H.train_mask(f) & f["buffer"]).any()


def test_canary_flags_a_leaky_feature():
    rng = np.random.default_rng(0)
    truth = np.zeros((60, 60), np.float32)
    truth[10:40, 30] = 1.0
    leaky = truth + 0.01 * rng.random((60, 60))
    honest = rng.random((60, 60))
    out = H.canary({"leaky": leaky, "honest": honest}, truth)
    assert out["leaky"]["leakage_canary"] is True
    assert out["honest"]["leakage_canary"] is False


def test_bootstrap_interval_brackets_the_mean():
    vals = [0.30, 0.34, 0.28, 0.31, 0.33]
    ci = H.bootstrap_ci(vals)
    assert ci["lo"] < ci["mean"] < ci["hi"]
    assert ci["n"] == 5


def test_registry_blocks_an_exact_copy(tmp_path):
    a = np.zeros((60, 60), np.float32)
    a[10:50, 30] = 1.0
    surf = 0.5 * a + 0.001 * np.arange(60)[None, :] / 60.0
    cand = tmp_path / "cand.tif"
    reg_dots = tmp_path / "reg_dots.tif"
    reg_surf = tmp_path / "reg_surf.tif"
    prof = writer.make_profile(height=60, width=60)
    writer.write_submission(cand, a, profile=prof)
    writer.write_submission(reg_dots, a, profile=prof)
    writer.write_submission(reg_surf, surf, profile=prof)
    items = [{"site": s, "surface": "reg_surf.tif",
              "surface_sha256": registry.sha256(reg_surf),
              "dots": "reg_dots.tif", "dots_sha256": registry.sha256(reg_dots)}
             for s in registry.REQUIRED_SITES]
    man = tmp_path / "registry.json"
    man.write_text(json.dumps(items))
    rep = registry.screen(cand, manifest=man)
    assert rep["status"] == "BLOCKED"
    assert rep["comparisons"][0]["duplicate"] is True


def test_registry_is_unknown_without_a_manifest(tmp_path):
    a = np.zeros((40, 40), np.float32)
    a[20, 20] = 1.0
    cand = tmp_path / "cand.tif"
    writer.write_submission(cand, a, profile=writer.make_profile(height=40, width=40))
    rep = registry.screen(cand)
    assert rep["status"] == "UNKNOWN"


def test_registry_rejects_a_non_binary_candidate(tmp_path):
    a = np.zeros((40, 40), np.float32)
    a[20, 20] = 0.5
    cand = tmp_path / "cand.tif"
    writer.write_submission(cand, a, profile=writer.make_profile(height=40, width=40))
    rep = registry.screen(cand)
    assert rep["status"] == "BLOCKED"
