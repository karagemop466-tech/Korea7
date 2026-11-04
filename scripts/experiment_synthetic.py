#!/usr/bin/env python3
"""Experiment: which emission strategy wins against simulated *newly mapped* faults?

The scored label set is structure the catalogue does not contain.  We cannot
observe it, so we model the mapping process two ways and let the data choose:

  * EXTENSION -- a newly mapped trace continues or flanks a known trace a few
    hundred metres out.  This is how the catalogue grew historically and it is
    the process the registry's "halo" rasters (GEMSDOE24/25/27/30/31/32/36)
    are implicitly targeting.
  * DISCOVERY -- a newly mapped trace sits on the low-discrepancy background,
    far from anything already known.

Five emission strategies are scored against each mixture:

  A  dilation(k=1)                    -- best in-sample geometry (registry lane)
  B  dilation(k=2)                    -- GEMSDOE32's geometry
  C  uniform lattice, 400 m clearance -- the HALO-32k proposal
  D  near-catalogue halo (1 < d <= 6) -- targets EXTENSION only
  E  half halo + half uniform lattice -- the hybrid

Output is a MODEL-BASED UPPER BOUND under stated assumptions, not a score.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation, label

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from k7.grid import load_grid  # noqa: E402
from k7.metric import dti  # noqa: E402
from k7.method import MethodSpec, build_surface, catalogue_distance, lattice_mask  # noqa: E402

OUT = ROOT / "evidence" / "synthetic_experiment.json"
BUDGET = 32_000


def pick_budget(mask: np.ndarray, budget: int) -> np.ndarray:
    """Evenly thin a mask to at most ``budget`` cells (keeps spatial uniformity)."""
    mask = np.asarray(mask, bool)
    n = int(mask.sum())
    if n <= budget:
        return mask
    idx = np.flatnonzero(mask.ravel())
    stride = n / budget
    out = np.zeros(mask.shape, dtype=bool)
    out.ravel()[idx[(np.arange(budget) * stride).astype(np.int64)]] = True
    return out


def simulate_extension(truth: np.ndarray, footprint: np.ndarray, dist: np.ndarray,
                       rng: np.random.Generator, frac: float, index_px: int = 2) -> np.ndarray:
    """New traces flanking known ones: take catalogue pixels and push them ``index_px`` out."""
    out = np.zeros(truth.shape, dtype=bool)
    idx = np.flatnonzero((truth & footprint).ravel())
    if idx.size == 0:
        return out
    take = rng.choice(idx, size=int(idx.size * frac), replace=False)
    rr, cc = np.unravel_index(take, truth.shape)
    ang = rng.uniform(0, 2 * np.pi, rr.size)
    rad = rng.integers(1, index_px + 1, rr.size)
    nr = np.clip(rr + np.rint(rad * np.sin(ang)).astype(int), 0, truth.shape[0] - 1)
    nc = np.clip(cc + np.rint(rad * np.cos(ang)).astype(int), 0, truth.shape[1] - 1)
    out[nr, nc] = True
    return out & footprint & ~truth


def simulate_discovery(footprint: np.ndarray, truth: np.ndarray, dist: np.ndarray,
                       rng: np.random.Generator, n_structures: int, clearance_px: int = 8,
                       length_range: tuple[int, int] = (6, 40),
                       strike_deg: float = 155.0, spread_deg: float = 18.0) -> np.ndarray:
    """New traces on unmapped ground, longer than the catalogue median (discovery bias)."""
    out = np.zeros(footprint.shape, dtype=bool)
    cand = np.flatnonzero((footprint & (dist > clearance_px)).ravel())
    if cand.size == 0:
        return out
    seeds = rng.choice(cand, size=min(n_structures, cand.size), replace=False)
    h, w = footprint.shape
    for s in seeds:
        r0, c0 = np.unravel_index(s, footprint.shape)
        L = int(rng.integers(*length_range))
        th = np.deg2rad(rng.normal(strike_deg, spread_deg))
        t = np.linspace(-L / 2, L / 2, max(2, L * 2))
        yy = np.rint(r0 - t * np.sin(th)).astype(int)
        xx = np.rint(c0 + t * np.cos(th)).astype(int)
        ok = (yy >= 0) & (yy < h) & (xx >= 0) & (xx < w)
        out[yy[ok], xx[ok]] = True
    return out & footprint & ~truth


def main() -> int:
    g = load_grid()
    dist = catalogue_distance(g.truth)
    foot, truth = g.footprint, g.truth

    # ---- candidate strategies (all capped to the same 32k dot budget)
    A = pick_budget(binary_dilation(truth, iterations=1) & foot, BUDGET)
    B = pick_budget(binary_dilation(truth, iterations=2) & foot, BUDGET)
    C, cstats = build_surface(foot, truth, MethodSpec("HALO-32k", 4, BUDGET), dist=dist)
    D = pick_budget((dist > 1) & (dist <= 6) & foot, BUDGET)
    halo_band = lattice_mask(foot.shape) & foot & (dist > 2) & (dist <= 6)
    uniform = lattice_mask(foot.shape) & foot & (dist > 4)
    half = BUDGET // 2
    E = pick_budget(halo_band, half) | pick_budget(uniform & ~halo_band, half)
    E = pick_budget(E, BUDGET)
    strategies = {"A_dilate1": A, "B_dilate2": B, "C_lattice400": C, "D_halo": D, "E_hybrid": E}
    for k, v in strategies.items():
        print(f"strategy {k:14s} dots={int(v.sum()):6d}")

    results = []
    rng = np.random.default_rng(20261104)
    for mix_name, ext_frac, disc_structs in (
        ("extension_only", 1.00, 0),
        ("extension_heavy", 0.70, 1_500),
        ("balanced", 0.40, 3_000),
        ("discovery_heavy", 0.15, 5_000),
    ):
        for seed in range(3):
            rng = np.random.default_rng(1000 * seed + hash(mix_name) % 997)
            H = np.zeros(foot.shape, dtype=bool)
            if ext_frac > 0:
                H |= simulate_extension(truth, foot, dist, rng, ext_frac)
            if disc_structs > 0:
                H |= simulate_discovery(foot, truth, dist, rng, disc_structs)
            if H.sum() < 500:
                continue
            # Organiser rule: the known-fault mask is pixel-exact.  Catalogue pixels
            # are removed from the scored domain entirely, so a dot sitting on a known
            # trace earns nothing while a dot near one but far from new structure is
            # still charged the false-positive penalty.
            valid = foot & ~truth
            row = {"mix": mix_name, "seed": seed, "hidden_px": int((H & valid).sum())}
            for k, cand in strategies.items():
                row[k] = float(dti(cand.astype(np.float32), H, valid=valid))
            results.append(row)
            print(f"  {mix_name:16s} seed={seed} hidden={H.sum():7d} " +
                  " ".join(f"{k}={row[k]:.5f}" for k in strategies))

    # aggregate
    agg = {}
    for mix in {r["mix"] for r in results}:
        rows = [r for r in results if r["mix"] == mix]
        agg[mix] = {k: {"mean": float(np.mean([r[k] for r in rows])),
                        "min": float(np.min([r[k] for r in rows])),
                        "max": float(np.max([r[k] for r in rows]))}
                    for k in strategies}
    payload = {
        "label": "MODEL-BASED UPPER BOUND - NOT A SCORE",
        "budget_dots": BUDGET,
        "strategies": {k: int(v.sum()) for k, v in strategies.items()},
        "runs": results,
        "aggregate": agg,
        "assumptions": [
            "Newly mapped faults arise either as extensions flanking known traces (1-2 px out) "
            "or as independent discovery traces on unmapped ground with a 6-40 px length range "
            "and 155 +/- 18 degree strike, matching the measured catalogue grain.",
            "The organiser mask is pixel-exact on the known catalogue, so catalogue pixels score nothing.",
            "All candidates are capped to the same 32,000-dot budget.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nwrote {OUT}")
    print("\n=== aggregate (mean DTI vs simulated hidden structure) ===")
    hdr = "mix".ljust(18) + "".join(k.rjust(14) for k in strategies)
    print(hdr)
    for mix, d in agg.items():
        print(mix.ljust(18) + "".join(f"{d[k]['mean']:14.5f}" for k in strategies))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
