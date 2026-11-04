"""Tests: metric exactness, lattice determinism, validator gates, submission integrity."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from k7 import grid as gridmod  # noqa: E402
from k7.metric import ALPHA, BETA, RADIUS_PX, components, dti, dti_bruteforce  # noqa: E402
from k7.method import (  # noqa: E402
    BASIS_A,
    BASIS_B,
    DET,
    MULTIPLIER,
    MethodSpec,
    _congruence_multiplier,
    build_surface,
    catalogue_distance,
    lattice_mask,
    silence_audit,
)
from k7.validate import validate_raster, write_submission  # noqa: E402

DATA = ROOT / "data"
SUBS = ROOT / "submissions"
SLUG = "korea7-halo-band4-45-lat89-38000"

needs_data = pytest.mark.skipif(
    not (DATA / "sample_submission.tif").exists(), reason="competition templates not present"
)


# --------------------------------------------------------------------------- metric
@pytest.mark.parametrize("seed", range(5))
def test_metric_matches_published_equations(seed: int) -> None:
    """The fast path must equal a literal transcription of the published DTI."""
    rng = np.random.default_rng(seed)
    T = np.zeros((16, 16), bool)
    P = np.zeros((16, 16))
    for _ in range(5):
        T[rng.integers(0, 16), rng.integers(0, 16)] = True
    for _ in range(7):
        P[rng.integers(0, 16), rng.integers(0, 16)] = round(float(rng.uniform(0.2, 1.0)), 3)
    fast, slow = components(P, T), dti_bruteforce(P, T)
    assert abs(fast["tp"] - slow["tp"]) < 1e-9
    assert abs(fast["fp"] - slow["fp"]) < 1e-9
    assert abs(fast["dti"] - slow["dti"]) < 1e-9


def test_metric_constants_are_the_published_ones() -> None:
    assert ALPHA == 0.2
    assert BETA == 0.8
    assert RADIUS_PX == 3.0  # 300 m at the 100 m competition grid


def test_exact_catalogue_replication_scores_one() -> None:
    T = np.zeros((40, 40), bool)
    T[20, 5:35] = True
    assert dti(T.astype(np.float32), T) == pytest.approx(1.0)


def test_nothing_emitted_scores_zero() -> None:
    T = np.zeros((20, 20), bool)
    T[10, 5:15] = True
    r = components(np.zeros((20, 20)), T)
    assert r["dti"] == 0.0
    assert r["fn"] == 10.0


def test_kernel_radius_is_three_pixels() -> None:
    """A dot 3 px from truth gets zero credit; 1 px away gets 2/3."""
    T = np.zeros((21, 21), bool)
    T[10, 10] = True
    for dy, expected in ((0, 1.0), (1, 2 / 3), (2, 1 / 3), (3, 0.0)):
        P = np.zeros((21, 21))
        P[10 + dy, 10] = 1.0
        if expected == 0.0:
            assert components(P, T)["tp"] == pytest.approx(0.0)
        else:
            assert components(P, T)["tp"] == pytest.approx(expected)


def test_metric_rejects_bad_input() -> None:
    T = np.ones((4, 4), bool)
    with pytest.raises(ValueError):
        components(np.full((4, 4), np.nan), T)
    with pytest.raises(ValueError):
        components(np.zeros((4, 5)), T)


# --------------------------------------------------------------------------- lattice
def test_lattice_constants() -> None:
    assert (BASIS_A, BASIS_B) == (11, 6)
    assert DET == BASIS_A**2 + BASIS_B**2 == 157
    assert MULTIPLIER == 129
    assert _congruence_multiplier(11, 6) == 129


def test_lattice_density_is_uniform() -> None:
    """A rotated-square lattice of determinant det must have density exactly 1/det."""
    for (a, b) in ((11, 6), (8, 5), (9, 7)):
        det = a * a + b * b
        m = lattice_mask((600, 600), a, b)
        assert abs(m.mean() - 1.0 / det) < 1e-3, (a, b, m.mean(), 1 / det)


def test_lattice_is_deterministic() -> None:
    a = lattice_mask((200, 200))
    b = lattice_mask((200, 200))
    assert np.array_equal(a, b)


def test_lattice_points_satisfy_the_generating_congruence() -> None:
    """Every lattice cell must satisfy the generator's linear congruence."""
    a, b = 11, 6
    m = lattice_mask((300, 300), a, b)
    rr, cc = np.nonzero(m)
    assert np.all((a * rr + b * cc) % DET == 0)


# --------------------------------------------------------------------------- method
@needs_data
def test_surface_respects_clearance_and_footprint() -> None:
    g = gridmod.load_grid()
    dist = catalogue_distance(g.truth)
    mask, stats = build_surface(g.footprint, g.truth, MethodSpec("t", 4, 5_000), dist=dist)
    assert mask.shape == g.footprint.shape
    assert not (mask & ~g.footprint).any(), "dots outside the organiser footprint"
    assert dist[mask].min() > 4, "dot inside the clearance band"
    assert stats["dots"] == int(mask.sum())


@needs_data
def test_silence_audit_reports_zero_contamination() -> None:
    g = gridmod.load_grid()
    mask, _ = build_surface(g.footprint, g.truth, MethodSpec("t", 4, 5_000))
    a = silence_audit(mask, g.truth)
    assert a["frac_within_2px"] == 0.0
    assert a["frac_within_3px"] == 0.0
    assert a["min_dist_px"] > 4


# --------------------------------------------------------------------------- validate
@needs_data
def test_validator_accepts_the_shipped_submission() -> None:
    tif = SUBS / f"{SLUG}.tif"
    if not tif.exists():
        pytest.skip("submission not generated; run scripts/make_submission.py")
    r = validate_raster(tif)
    assert r.passed, [c for c in r.checks if not c[1]]


@needs_data
def test_validator_rejects_nan_inside_footprint() -> None:
    """The portal error 'Predicted values must be in range [0, 1]' must be caught."""
    g = gridmod.load_grid()
    arr = np.zeros(g.footprint.shape, dtype=np.float32)
    arr[g.truth] = 1.0
    arr[10, 10] = np.nan  # inside the footprint
    r = validate_raster(Path("dummy"), array=arr)
    assert not r.passed
    names = {n for n, ok, _ in r.checks if not ok}
    assert "no_nan_or_inf" in names


@needs_data
def test_validator_rejects_values_above_one() -> None:
    g = gridmod.load_grid()
    arr = np.zeros(g.footprint.shape, dtype=np.float32)
    arr[g.truth] = 1.0
    arr[arr > 0] = 2.5
    r = validate_raster(Path("dummy"), array=arr)
    assert not r.passed
    names = {n for n, ok, _ in r.checks if not ok}
    assert "values_in_0_1" in names


@needs_data
def test_validator_rejects_wrong_shape() -> None:
    arr = np.zeros((100, 100), dtype=np.float32)
    r = validate_raster(Path("dummy"), array=arr)
    assert not r.passed
    names = {n for n, ok, _ in r.checks if not ok}
    assert "shape" in names


# --------------------------------------------------------------------------- shipped file
@needs_data
def test_shipped_submission_is_unique_against_registry() -> None:
    reg = ROOT / "evidence" / "registry"
    if not reg.exists() or not any(reg.glob("*.tif")):
        pytest.skip("registry rasters not present")
    from k7.overlap import compare

    tif = SUBS / f"{SLUG}.tif"
    if not tif.exists():
        pytest.skip("submission not generated")
    with rasterio.open(tif) as ds:
        cand = ds.read(1) > 0
    for p in reg.glob("*.tif"):
        with rasterio.open(p) as ds:
            rm = np.nan_to_num(ds.read(1)) > 0
        ov = compare(cand, rm)
        assert ov.jaccard < 0.70, f"{p.name} jaccard {ov.jaccard}"
        assert ov.frac_within_3px <= 0.70, f"{p.name} within-3px {ov.frac_within_3px}"


@needs_data
def test_shipped_run_card_is_consistent() -> None:
    import json

    card = json.loads((SUBS / f"{SLUG}.json").read_text())
    assert card["validator"]["passed"] is True
    assert card["verdict"] == "promote"
    assert card["uniqueness"]["unique"] is True
    assert card["submission"]["note_chars"] <= 140
    assert card["submission"]["tif"]["dots"] == card["numbers"]["structural_profile"]["dots"]
