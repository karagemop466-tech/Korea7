#!/usr/bin/env python3
"""Experiment 1 — spatially blocked hide-and-recover of a catalogue-free surface.

Question: does the seismogenic-lineament surface (OSLF) locate faults that the visible
catalogue does not show, better than (a) uniform random placement at a matched dot budget
and (b) the catalogue-proximity detector that the registry family approximates?

This is the only instrument in this repository that is *unbiased* for OSLF, because OSLF
never uses a fault label.  It is NOT an unbiased estimate of live leaderboard skill for
any catalogue-derived surface, and it is not used as one.

Writes evidence/holdout_experiment.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import external as ext, grid, screen, surface as surf  # noqa: E402
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
BUDGET = 20_000          # fixed, pre-registered matched dot budget
BUFFER_PX = 10.0
N_FOLDS = 2


def random_control(domain: np.ndarray, budget: int, seed: int) -> np.ndarray:
    flat = np.flatnonzero(domain.ravel())
    rng = np.random.default_rng(seed)
    take = rng.choice(flat.size, min(budget, flat.size), replace=False)
    m = np.zeros(domain.size, dtype=bool)
    m[flat[take]] = True
    return m.reshape(domain.shape)


def main() -> int:
    t0 = time.time()
    ref = grid.load_reference()
    foot, cat = ref["footprint"], ref["catalogue"]

    seis = ext.load_on_grid("seis_n200a15", foot)
    S = surf.build(seis, foot)
    oslf = S["surface"]
    print(f"OSLF surface built in {time.time() - t0:.1f}s")

    results = {"instrument": screen.INSTRUMENT_VERSION, "budget": BUDGET,
               "buffer_px": BUFFER_PX, "n_folds": N_FOLDS,
               "surface_definition": {"weights": S["weights"],
                                      "orientations_deg": S["orientations_deg"],
                                      "smooth_sigma_px": S["smooth_sigma_px"]},
               "folds": [], "generated_utc": "2026-11-04"}

    for f in range(N_FOLDS):
        split = screen.holdout_split(cat, foot, fold_id=f, n_folds=N_FOLDS,
                                     buffer_px=BUFFER_PX)
        vis, hid, act = split["visible"], split["hidden"], split["active"]
        print(f"\n--- fold {f}: {split['n_segments']} segments, hidden/active pixels "
              f"{split['hidden_pixels_kept']} (discarded by buffer "
              f"{split['hidden_pixels_discarded_by_buffer']}) ---")

        canary = screen.auc_single_feature(oslf, hid, act)
        print(f"  leakage canary  OSLF AUC = {canary['auc']:.4f} "
              f"(positives {canary['positives']}, suspect={canary['leakage_suspect']})")
        canary_dist = screen.auc_single_feature(
            (-distance_transform_edt(~vis)).astype(np.float32), hid, act)
        print(f"  leakage canary  distance-to-visible AUC = {canary_dist['auc']:.4f} "
              f"(suspect={canary_dist['leakage_suspect']})")

        arms = {
            "OSLF": screen.emit_top(oslf, budget=BUDGET, exclude=vis,
                                    allowed=act, clearance_px=3.0),
            "random_control": random_control(
                act & (distance_transform_edt(~vis) > 3.0), BUDGET, seed=1000 + f),
            "catalogue_proximity": screen.emit_top(
                (-distance_transform_edt(~vis)).astype(np.float32), budget=BUDGET,
                exclude=vis, allowed=act, clearance_px=3.0),
        }
        fold_rec = {"fold_id": f, "n_segments": split["n_segments"],
                    "hidden_pixels_in_domain": int(hid.sum()),
                    "active_pixels": int(act.sum()),
                    "canary_oslf": canary, "canary_distance_to_visible": canary_dist,
                    "arms": {}}
        for name, mask in arms.items():
            r = screen.dti_with_segment_ci(mask, hid, act, seed=7 + f)
            fold_rec["arms"][name] = {
                "dots": int(mask.sum()),
                "holdout_dti": r["dti"], "coverage": r["coverage"],
                "tp": r["tp"], "fp": r["fp"], "n_truth": r["n_truth"],
                "ci95": r.get("ci95"), "n_truth_segments": r.get("n_segments"),
            }
            ci = r.get("ci95")
            ci_s = f"[{ci[0]:.4f}, {ci[1]:.4f}]" if ci else "n/a"
            print(f"    {name:22s} dots={int(mask.sum()):6d}  "
                  f"HOLDOUT-DTI={r['dti']:.4f} 95%CI {ci_s}  "
                  f"coverage={r['coverage']:.3f}")
        results["folds"].append(fold_rec)

    # paired comparison: OSLF vs each control, per fold
    print("\n--- paired deltas (OSLF minus control) ---")
    deltas = {}
    for other in ("random_control", "catalogue_proximity"):
        ds = [fr["arms"]["OSLF"]["holdout_dti"] - fr["arms"][other]["holdout_dti"]
              for fr in results["folds"]]
        deltas[other] = {"per_fold": ds, "mean": float(np.mean(ds))}
        print(f"  vs {other:22s} " + " ".join(f"{d:+.4f}" for d in ds) +
              f"   mean {np.mean(ds):+.4f}")
    results["paired_deltas"] = deltas

    pool = np.mean([fr["arms"]["OSLF"]["holdout_dti"] for fr in results["folds"]])
    print(f"\nOSLF pooled-across-folds HOLDOUT-DTI = {pool:.4f}  "
          f"(instrument {screen.INSTRUMENT_VERSION})")
    results["oslf_pooled_mean_dti"] = float(pool)
    results["elapsed_s"] = round(time.time() - t0, 1)

    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "holdout_experiment.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nwrote evidence/holdout_experiment.json in {results['elapsed_s']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
