"""Vendored DTI metric vs a literal transcription of the official equations.

Official source (fetched 2026-11-04):
https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
alpha=0.2, beta=0.8, triangular kernel k(d)=max(1-d/R,0), R=300 m = 3 px.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vendor/gems32/src"))
from gems32.metric import dti_binary, dti_bruteforce, dti_exact  # noqa: E402


def test_exact_matches_literal_equations():
    rng = np.random.default_rng(7)
    for _ in range(3):
        p = (rng.random((30, 30)) > 0.9) * rng.random((30, 30))
        g = rng.random((30, 30)) > 0.95
        assert abs(dti_exact(p, g)["dti"] - dti_bruteforce(p, g)["dti"]) < 1e-9


def test_binary_matches_exact():
    rng = np.random.default_rng(11)
    p = rng.random((40, 40)) > 0.9
    g = rng.random((40, 40)) > 0.95
    assert abs(dti_binary(p, g)["dti"] - dti_exact(p.astype(float), g)["dti"]) < 1e-9


def test_perfect_and_empty():
    g = np.zeros((9, 9), bool)
    g[4, 4] = True
    assert dti_binary(g, g)["dti"] > 0.999999
    assert dti_binary(np.zeros_like(g), g)["dti"] == 0.0


def test_kernel_radius():
    # One truth pixel; one dot 2 px away earns k=1/3 credit:
    # TP=1/3, FP=2/3, FN=2/3 -> DTI = (1/3)/((1/3)+0.2*(2/3)+0.8*(2/3)) = 1/3
    g = np.zeros((9, 9), bool); g[4, 4] = True
    p = np.zeros((9, 9), bool); p[4, 6] = True
    assert abs(dti_binary(p, g)["dti"] - 1 / 3) < 1e-9
    # Dot at exactly R=3 px earns 0 credit.
    p2 = np.zeros((9, 9), bool); p2[4, 7] = True
    assert dti_binary(p2, g)["dti"] == 0.0
