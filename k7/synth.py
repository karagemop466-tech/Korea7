"""Synthetic-geology upper bound for the catalogue-silent lattice.

The method makes one falsifiable geometric claim: *a uniform lattice at a fixed
clearance from mapped structure will land within 300 m of structure that has
not been mapped yet.*  Without the withheld ground truth that claim cannot be
tested directly.  What can be tested is the idealised generator: simulate
unmapped fault traces drawn from the same anisotropic, length-skewed population
as the catalogue, hide them, and measure the DTI the lattice achieves.

This is a **model-based upper bound**, not a holdout measurement and not a
score.  It is reported with that label everywhere it appears.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import gaussian_filter, label

from .metric import dti
from .method import MethodSpec, build_surface, catalogue_distance


@dataclass(frozen=True)
class FaultPopulation:
    """Empirical descriptors of the catalogue trace population (measured, see evidence)."""

    n_structures: int = 3_199
    median_length_px: int = 12
    mean_length_px: float = 19.1
    max_length_px: int = 360
    # Walker Lane structural grain is NNW; measured on labels.tif in evidence/measurements.json
    strike_deg: float = 155.0
    strike_spread_deg: float = 18.0


def simulate_traces(
    shape: tuple[int, int],
    footprint: np.ndarray,
    pop: FaultPopulation,
    rng: np.random.Generator,
    density_scale: float = 1.0,
) -> np.ndarray:
    """Draw trace-like structures: long, thin, strike-clustered, length-skewed."""
    h, w = shape
    truth = np.zeros(shape, dtype=bool)
    n = int(pop.n_structures * density_scale)
    # log-normal-ish lengths anchored on the measured median/mean, clipped
    mu = np.log(pop.median_length_px)
    lengths = np.clip(np.exp(rng.normal(mu, 1.0, n)), 3, pop.max_length_px * 3).astype(int)
    strikes = rng.normal(pop.strike_deg, pop.strike_spread_deg, n)
    ys = rng.integers(0, h, n)
    xs = rng.integers(0, w, n)
    for y0, x0, L, th in zip(ys, xs, lengths, strikes):
        t = np.linspace(-L / 2, L / 2, max(2, L * 2))
        rad = np.deg2rad(th)
        # strike measured from +x, rotated into image coords (y grows downward)
        yy = np.rint(y0 - t * np.sin(rad)).astype(int)
        xx = np.rint(x0 + t * np.cos(rad)).astype(int)
        ok = (yy >= 0) & (yy < h) & (xx >= 0) & (xx < w)
        truth[yy[ok], xx[ok]] = True
    return truth & footprint


def upper_bound(
    footprint: np.ndarray,
    pop: FaultPopulation | None = None,
    spec: MethodSpec | None = None,
    regimes: tuple[int, ...] = (0, 1, 2, 3, 4, 6, 8),
    density_scales: tuple[float, ...] = (0.5, 1.0, 2.0),
    seeds: int = 3,
) -> list[dict]:
    """DTI of the lattice against simulated withheld structure, per clearance regime."""
    pop = pop or FaultPopulation()
    spec = spec or MethodSpec("HALO-32k", 4, 32_000)
    out: list[dict] = []
    for ds in density_scales:
        for seed in range(seeds):
            rng = np.random.default_rng(1000 * seed + int(ds * 10))
            hidden = simulate_traces(footprint.shape, footprint, pop, rng, density_scale=ds)
            if hidden.sum() < 100:
                continue
            dist = catalogue_distance(hidden)
            for k in regimes:
                # candidate = idealised dots covering the STRUCTURE POPULATION
                # at clearance k from the candidate's own view; here we measure
                # what a uniform lattice placed by the same rule achieves.
                cand = _ideal_lattice(footprint, spec, k)
                score = dti(cand.astype(np.float32), hidden, valid=footprint)
                out.append({
                    "density_scale": ds,
                    "seed": seed,
                    "clearance_px": k,
                    "hidden_px": int(hidden.sum()),
                    "dots": int(cand.sum()),
                    "dti_vs_hidden": float(score),
                })
    return out


def _ideal_lattice(footprint: np.ndarray, spec: MethodSpec, clearance_px: int) -> np.ndarray:
    from .method import lattice_mask

    lat = lattice_mask(footprint.shape, spec.basis_a, spec.basis_b) & footprint
    n = int(lat.sum())
    if n <= spec.target_dots:
        return lat
    idx = np.flatnonzero(lat.ravel())
    stride = len(idx) / spec.target_dots
    out = np.zeros(footprint.shape, dtype=bool)
    out.ravel()[idx[(np.arange(spec.target_dots) * stride).astype(np.int64)]] = True
    return out


def summarise(rows: list[dict]) -> dict:
    """Group simulated clearspace results by clearance and report mean/CI."""
    groups: dict[int, list[float]] = {}
    for r in rows:
        groups.setdefault(r["clearance_px"], []).append(r["dti_vs_hidden"])
    summary = {}
    for k, vals in sorted(groups.items()):
        v = np.asarray(vals, dtype=float)
        summary[k] = {
            "mean": float(v.mean()),
            "p05": float(np.percentile(v, 5)),
            "p95": float(np.percentile(v, 95)),
            "n": int(v.size),
        }
    return summary
