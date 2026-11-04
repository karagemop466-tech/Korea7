#!/usr/bin/env python3
"""Experiment 2 — which emission strategy wins when surface skill is weak?

Experiment 1 showed a genuine but weak surface (AUC ~0.56) losing to uniform random
placement at a matched dot budget.  That is not a bug: with alpha=0.2 / beta=0.8 the metric
weights recall eight times more than false-positive mass, so when skill is weak, *coverage*
beats *concentration*.  Experiment 2 tests that claim and measures the no-skill ceiling.

Arms (all at the same dot budget, all excluding a 3 px collar around the visible faults):
  random          uniform over the eligible domain                (no-skill control)
  lattice_sN      square lattice, spacing N px                    (pure coverage)
  oslf_top        top-K of the seismogenic lineament surface      (weak skill)
  oslf_lattice    lattice, but thinned by OSLF rank               (mild skill)
  collar_3_10     annulus 3-10 px around the visible faults       (structural extrapolation)

Writes evidence/experiment2_emission.json.  Budget: report only; no submission here.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import external as ext, grid, screen, surface as surf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
BUDGET = 20_000
BUFFER_PX = 10.0


def lattice_mask(domain: np.ndarray, spacing: int) -> np.ndarray:
    m = np.zeros(domain.shape, dtype=bool)
    m[::spacing, ::spacing] = True
    return m & domain


def take_capped(mask: np.ndarray, budget: int, priority: np.ndarray | None = None,
                seed: int = 0) -> np.ndarray:
    """Reduce a mask to at most ``budget`` pixels, keeping the highest ``priority``."""
    flat = np.flatnonzero(mask.ravel())
    if flat.size <= budget:
        return mask
    if priority is None:
        rng = np.random.default_rng(seed)
        keep = rng.choice(flat.size, budget, replace=False)
    else:
        v = priority.ravel()[flat]
        k = flat.size - budget
        keep = np.argpartition(v, k)[k:]
    out = np.zeros(mask.size, dtype=bool)
    out[flat[keep]] = True
    return out.reshape(mask.shape)


def main() -> int:
    t0 = time.time()
    ref = grid.load_reference()
    foot, cat = ref["footprint"], ref["catalogue"]
    seis = ext.load_on_grid("seis_n200a15", foot)
    oslf = surf.build(seis, foot)["surface"]

    split = screen.holdout_split(cat, foot, fold_id=0, n_folds=2, buffer_px=BUFFER_PX)
    vis, hid, act = split["visible"], split["hidden"], split["active"]
    dvis = distance_transform_edt(~vis)
    eligible = act & (dvis > 3.0)

    arms: dict[str, np.ndarray] = {}
    arms["random"] = take_capped(eligible, BUDGET, seed=11)
    for spacing in (8, 11, 16):
        arms[f"lattice_s{spacing}"] = take_capped(lattice_mask(eligible, spacing), BUDGET, seed=11)
    arms["oslf_top"] = screen.emit_top(oslf, budget=BUDGET, exclude=vis, allowed=act,
                                       clearance_px=3.0)
    arms["oslf_lattice"] = take_capped(lattice_mask(eligible, 11), BUDGET, priority=oslf)
    ann = eligible & (dvis <= 10.0)
    arms["collar_3_10"] = take_capped(ann, BUDGET, priority=-dvis.astype(np.float32))

    out = {"instrument": screen.INSTRUMENT_VERSION, "budget": BUDGET,
           "fold": 0, "hidden_pixels": int(hid.sum()), "arms": {},
           "generated_utc": "2026-11-04"}
    print(f"fold 0, {split['n_segments']} segments, hidden px {int(hid.sum())}, "
          f"eligible px {int(eligible.sum())}\n")
    for name, mask in arms.items():
        r = screen.dti_with_segment_ci(mask, hid, act, seed=3)
        ci = r.get("ci95")
        out["arms"][name] = {"dots": int(mask.sum()), "holdout_dti": r["dti"],
                             "coverage": r["coverage"], "fp": r["fp"],
                             "ci95": ci, "n_truth": r["n_truth"]}
        print(f"  {name:14s} dots={int(mask.sum()):6d}  HOLDOUT-DTI={r['dti']:.4f}  "
              f"coverage={r['coverage']:.3f}  "
              f"95%CI [{ci[0]:.4f}, {ci[1]:.4f}]" if ci else name)

    best = max(out["arms"].items(), key=lambda kv: kv[1]["holdout_dti"])
    print(f"\nbest arm: {best[0]}  HOLDOUT-DTI={best[1]['holdout_dti']:.4f}")
    out["best_arm"] = best[0]

    # No-skill live-regime ceiling, from the metric algebra rather than a measurement.
    print("\n--- no-skill ceiling in the LIVE regime (algebra, K is an assumption) ---")
    fp_px = int(foot.sum())
    ceiling = {}
    for K in (30_000, 60_000, 120_000, 160_000):
        d_all = K / (0.2 * fp_px + 0.8 * K)          # predict every footprint pixel = 1
        ceiling[K] = d_all
        print(f"  K={K:7d}  full-footprint spray DTI = {d_all:.4f}")
    out["no_skill_ceiling_by_K"] = ceiling
    out["note"] = ("The instrument's K (~17k hidden px) is much smaller than the live K, so "
                   "absolute DTI values here are not live scores. Only the ordering of arms "
                   "at a matched budget is interpretable.")

    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "experiment2_emission.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwrote evidence/experiment2_emission.json in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
