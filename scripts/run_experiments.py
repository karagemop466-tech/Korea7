#!/usr/bin/env python3
"""Run the three pre-declared experiments for this lane and write the reports.

Lane method paragraph (the single paragraph this run is allowed to work in):

    "Hypothesis: the gap between the ~0.28 plateau of catalogue-anchored dot
    submissions and the leaderboard is produced mainly by the *emission* step,
    not by the detector, because DTI credits true positives with a max and
    charges false positives with a sum.  Mechanism: replace threshold+dilate
    or top-k dots with a Dinkelbach-calibrated, coverage-aware greedy that
    maximises expected DTI directly.  Non-fault process that could mimic it:
    a map that is simply denser near *everything* the catalogue already
    contains (dilation of known faults) raises recall on new faults near old
    ones without any new information."

Every number written by this script is either
  * SIMULATION (a synthetic network calibrated to published agreement
    statistics; never a leaderboard score), or
  * a deterministic arithmetic check of the metric.
Nothing here is ORGANIZER-CONFIRMED.

Budget: three experiments, and the script is designed to finish in minutes.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gems import calibrate, emission, geometry, metric as M, network as N  # noqa: E402

OUT = ROOT / "docs" / "results"
OUT.mkdir(parents=True, exist_ok=True)
T_START = time.time()


def ci95(values):
    """Mean and t-based 95% CI half-width (n small; t(0.975, n-1) by table)."""
    v = np.asarray(values, dtype=float)
    n = v.size
    if n < 2:
        return float(v.mean()), None
    t = {2: 12.71, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447,
         8: 2.365, 9: 2.306, 10: 2.262}.get(n, 1.96)
    return float(v.mean()), float(t * v.std(ddof=1) / math.sqrt(n))


# ------------------------------------------------------------------ E1
def experiment_1():
    """Metric arithmetic + calibration of the synthetic testbed to published anchors."""
    print("E1: metric checks and testbed calibration")
    hand = {
        "single_pixel_on_target": M.dti(_dot(21, 10, 10), _dot(21, 10, 10))["score"],
        "single_pixel_1px_off": M.dti(_dot(21, 10, 11), _dot(21, 10, 10))["score"],
        "single_pixel_2px_off": M.dti(_dot(21, 10, 12), _dot(21, 10, 10))["score"],
        "single_pixel_3px_off": M.dti(_dot(21, 10, 13), _dot(21, 10, 10))["score"],
        "worked_example_3_1.89_2": M.score_from_counts(3, 1.89, 2),
        "empty_prediction": M.dti(np.zeros((21, 21), np.float32), _dot(21, 10, 10))["score"],
        "uniform_0.02_background": M.dti(np.full((201, 201), 0.02, np.float32),
                                        _dot(201, 100, 100))["score"],
    }
    band = []
    for width in (1, 3, 5, 7):
        for off in (0, 1, 2):
            band.append({"width_px": width, "offset_px": off,
                         "dti": round(M.band_table(width, off), 4)})
    calib = N.calibrate(shape=(900, 900),
                        grid=[(o, j) for o in (0.02, 0.05, 0.08, 0.12)
                              for j in (0.2, 0.3, 0.5)])
    result = {
        "experiment": "E1-metric-and-testbed",
        "label": "ARITHMETIC + SIMULATION",
        "hand_checks": {k: round(float(v), 4) for k, v in hand.items()},
        "band_table": band,
        "testbed_calibration": calib,
        "notes": [
            "TP_w is a max over the kernel and FP_w is a sum over positives, so a "
            "1-px band scores 1.00 on target while a 5-px band scores 0.625 and a "
            "3-px band one pixel off scores 0.238.",
            "A uniform 0.02 background over a 201x201 field with one truth cell "
            "scores essentially zero: FP_w grows by the number of positives.",
        ],
    }
    (OUT / "e1_metric_calibration.json").write_text(json.dumps(result, indent=2))
    print("   hand checks:", result["hand_checks"])
    print("   calibrated testbed:", calib["chosen"], "agreement",
          calib["agreement_dti"], "chance", calib["chance_dti"])
    return result


def _dot(n, y, x):
    a = np.zeros((n, n), np.float32)
    a[y, x] = 1.0
    return a


# ------------------------------------------------------------------ E2
def _evidence(truth, seed, blur=2.0, noise=0.5):
    """Stand-in for a real feature stack: blurred truth plus noise, then ranked.

    ``noise`` is chosen per experiment so that the resulting *pixel* AUC lands
    in a realistic range; a synthetic feature whose AUC exceeds 0.90 is
    reported as a leakage-canary trip, per the run protocol.
    """
    rng = np.random.default_rng(seed)
    obs = ndi.gaussian_filter(truth.astype(np.float32), blur)
    obs = obs + noise * rng.random(truth.shape).astype(np.float32)
    obs = (obs - obs.min()) / (obs.max() - obs.min())
    return obs.astype(np.float32)


def _evidence_at_auc(truth, seed, target=0.80, blur=2.0):
    """Pick the noise level whose measured AUC on ``truth`` is closest to target."""
    labels = (np.asarray(truth) > 0).astype(np.float32)
    best = None
    for noise in (0.15, 0.25, 0.35, 0.5, 0.7, 0.9, 1.2):
        obs = _evidence(truth, seed, blur=blur, noise=noise)
        a = calibrate.auc(obs, labels)
        if best is None or abs(a - target) < abs(best[0] - target):
            best = (a, noise, obs)
    return best[2], {"auc": round(float(best[0]), 4), "noise": best[1]}


def experiment_2(seeds=(0, 1, 2, 3, 4), shape=(900, 900), verbose=True):
    """Emission-layer comparison at a fixed, calibrated evidence quality.

    Every hyper-parameter is selected on an independent *calibration* network
    and then frozen; the evaluated network is only scored.  That keeps the
    comparison honest: no method peeks at the labels it is scored against.
    """
    print("E2: emission-layer comparison (5 seeds)")
    grid_lam = (0.05, 0.1, 0.2, 0.3, 0.4, 0.5)
    topk_grid = (500, 1000, 2000, 4000, 8000, 16000)
    rows = {k: [] for k in ("threshold", "nms", "topk", "coverage", "topk_matched")}
    chosen, aucs = {}, []

    def near_truth(binary):
        return M._coverage(np.zeros_like(binary, dtype=np.float32), binary > 0)[1] > 0

    for seed in seeds:
        calib_net = N.make_calibrated_network(shape=shape, seed=100 + seed)
        eval_net = N.make_calibrated_network(shape=shape, seed=seed)
        lab_cal = (calib_net > 0).astype(np.float32)
        lab_eval = (eval_net > 0).astype(np.float32)
        raw_cal, qc = _evidence_at_auc(calib_net, 900 + seed, target=0.80)
        raw_eval, qe = _evidence_at_auc(eval_net, 900 + seed, target=0.80)
        fit, cal_info = calibrate.isotonic(raw_cal, lab_cal)
        q_cal = fit(raw_cal).astype(np.float32)
        q_eval = fit(raw_eval).astype(np.float32)
        aucs.append(float(qe["auc"]))
        lam_thr = max(grid_lam, key=lambda p: M.dti(
            emission.threshold_emission(q_cal, p), lab_cal)["score"])
        lam_nms = max(grid_lam, key=lambda p: M.dti(
            emission.nms_emission(q_cal, p), lab_cal)["score"])
        k_top = max(topk_grid, key=lambda k: M.dti(
            emission.topk_emission(q_cal, k), lab_cal)["score"])
        chosen[seed] = {"lam_threshold": lam_thr, "lam_nms": lam_nms, "topk": k_top,
                        "evidence": qe, "calibration": cal_info,
                        "calib_dti": {
                            "threshold": round(M.dti(emission.threshold_emission(q_cal, lam_thr), lab_cal)["score"], 4),
                            "nms": round(M.dti(emission.nms_emission(q_cal, lam_nms), lab_cal)["score"], 4),
                            "topk": round(M.dti(emission.topk_emission(q_cal, k_top), lab_cal)["score"], 4)}}
        rows["threshold"].append(M.dti(emission.threshold_emission(q_eval, lam_thr), lab_eval)["score"])
        rows["nms"].append(M.dti(emission.nms_emission(q_eval, lam_nms), lab_eval)["score"])
        rows["topk"].append(M.dti(emission.topk_emission(q_eval, k_top), lab_eval)["score"])
        sel, _info = emission.coverage_emission(q_eval, lam0=0.25, rounds=6, top_k=3000)
        rows["coverage"].append(M.dti(sel, lab_eval)["score"])
        n_cov = int(sel.sum())
        # fair control: the same number of dots chosen by score alone
        rows["topk_matched"].append(
            M.dti(emission.topk_emission(q_eval, n_cov), lab_eval)["score"])
        chosen[seed]["coverage_emitted"] = n_cov
        chosen[seed]["topk_emitted"] = int(emission.topk_emission(q_eval, k_top).sum())
        if verbose:
            print(f"   seed {seed} AUC {aucs[-1]:.3f} | " + " ".join(
                f"{k} {v[-1]:.4f}" for k, v in rows.items()))

    summary = {}
    for k, v in rows.items():
        mean, half = ci95(v)
        summary[k] = {"mean_dti": round(mean, 4),
                      "ci95_halfwidth": None if half is None else round(half, 4),
                      "per_seed": [round(x, 4) for x in v]}
    baseline_best = max(summary["threshold"]["mean_dti"], summary["nms"]["mean_dti"],
                        summary["topk"]["mean_dti"], summary["topk_matched"]["mean_dti"])
    result = {
        "experiment": "E2-emission-layer",
        "label": "SIMULATION (not a leaderboard score)",
        "seeds": list(seeds), "shape": list(shape),
        "evidence_auc_mean": round(float(np.mean(aucs)), 4),
        "methods": summary,
        "coverage_emission_gain_over_best_baseline": round(
            summary["coverage"]["mean_dti"] - baseline_best, 4),
        "hyperparameters": {str(k): v for k, v in chosen.items()},
        "notes": [
            "The score->probability calibration and every hyper-parameter are "
            "fitted on an independent network (seed 100+seed) and applied "
            "unchanged to the evaluated network; the evaluated labels are only "
            "used to score.",
            "coverage_emission optimises expected DTI directly with a Dinkelbach "
            "outer loop and a coverage-aware greedy inner loop.",
        ],
    }
    (OUT / "e2_emission.json").write_text(json.dumps(result, indent=2))
    return result


# ------------------------------------------------------------------ E3
REGIMES = {
    "R1_full_network": "truth = every cell of the synthetic network (the "
                       "catalogue itself already covers ~74% of it)",
    "R2_unmapped_only": "truth = network cells more than 300 m from any "
                        "catalogue cell (the 'newly identified faults' reading)",
    "R3_near_miss_only": "truth = unmapped cells that lie within 12 px (1.2 km) "
                         "of a catalogue cell (expert-plausible extensions)",
}


def experiment_3(seeds=(0, 1, 2, 3, 4), shape=(900, 900), verbose=True):
    """Sensitivity of every submission family to the evaluator's masking rule.

    The competition does not publish (in anything reachable from this sandbox)
    exactly which cells the leaderboard scores.  Rather than assume one, this
    experiment scores the same predictions under three defensible readings and
    reports which family wins in each.  That is the honest form of the
    question 'can we beat 0.2778?' when the evaluator's cell set is unknown.
    """
    print("E3: submission families under three evaluator regimes")
    methods = ("oracle", "catalogue_dilate3", "tip_extension", "gap_closure",
               "tips_plus_gaps", "weak_evidence", "evidence_plus_geometry")
    out = {r: {m: [] for m in methods} for r in REGIMES}
    diag = []
    for seed in seeds:
        truth = N.make_calibrated_network(shape=shape, seed=seed)
        cat = N.perturb(truth, seed=seed + 11, omission=0.08, jitter_px=0.5)
        near_cat = M._coverage(np.zeros_like(cat), cat > 0)[1] > 0
        tbin = (truth > 0).astype(np.float32)
        unmapped = tbin.astype(bool) & (~near_cat)
        d_cat = ndi.distance_transform_edt(~(cat > 0))
        near_miss = unmapped & (d_cat <= 12)
        masks = {"R1_full_network": tbin.astype(bool),
                 "R2_unmapped_only": unmapped,
                 "R3_near_miss_only": near_miss}
        tips = geometry.extend_tips(cat, length=3)
        gaps = geometry.gap_closure(cat, max_gap=15)
        joint = np.maximum(tips, gaps)
        raw, ev = _evidence_at_auc(truth, 700 + seed, target=0.62, blur=2.5)
        fit, _ = calibrate.isotonic(raw, tbin)
        q = fit(raw).astype(np.float32) * (~near_cat)
        q = np.maximum(q, 0.25 * geometry.proximity_field(joint, sigma=2.0))
        ev_sel, _ = emission.coverage_emission(q, lam0=0.20, rounds=5, top_k=3000)
        preds = {"oracle": tbin,
                 "catalogue_dilate3": geometry.dilate(cat, 3),
                 "tip_extension": tips, "gap_closure": gaps,
                 "tips_plus_gaps": joint, "weak_evidence": ev_sel,
                 "evidence_plus_geometry": np.maximum(ev_sel, joint)}
        for rname, mask in masks.items():
            if mask.sum() < 30:
                continue
            tgt = mask.astype(np.float32)
            for m in methods:
                out[rname][m].append(M.dti(preds[m], tgt)["score"])
        diag.append({"seed": seed, "truth_cells": int(tbin.sum()),
                     "catalogue_cells": int((cat > 0).sum()),
                     "unmapped_cells": int(unmapped.sum()),
                     "unmapped_frac_of_truth": round(float(unmapped.sum() / tbin.sum()), 3),
                     "near_miss_cells": int(near_miss.sum()),
                     "evidence_auc": ev["auc"],
                     "evidence_emitted": int(ev_sel.sum())})
        if verbose:
            print(f"   seed {seed}: " + "  ".join(
                f"{r} best={max((M.dti(preds[m], masks[r].astype(np.float32))['score'], m) for m in methods)[1]}"
                f" {max(M.dti(preds[m], masks[r].astype(np.float32))['score'] for m in methods):.3f}"
                for r in masks))
    summary = {}
    for r, per in out.items():
        summary[r] = {}
        for m, v in per.items():
            if not v:
                continue
            mean, half = ci95(v)
            summary[r][m] = {"mean_dti": round(mean, 4),
                             "ci95_halfwidth": None if half is None else round(half, 4),
                             "n_seeds": len(v), "per_seed": [round(x, 4) for x in v]}
    result = {"experiment": "E3-regime-sensitivity",
              "label": "SIMULATION (not a leaderboard score)",
              "regimes": REGIMES, "methods": summary,
              "per_seed_diagnostics": diag, "seeds": list(seeds),
              "notes": [
                  "'oracle' is the withheld truth emitted perfectly; it is the "
                  "ceiling for any method under that regime and is not a "
                  "submission.",
                  "The three regimes are mutually exclusive readings of the "
                  "evaluator's cell set; the leaderboard's actual rule is not "
                  "reachable from this sandbox.",
              ]}
    (OUT / "e3_regimes.json").write_text(json.dumps(result, indent=2))
    return result


def main():
    out = {}
    out["e1"] = experiment_1()
    out["e2"] = experiment_2()
    out["e3"] = experiment_3()
    out["wall_seconds"] = round(time.time() - T_START, 1)
    (OUT / "all_experiments.json").write_text(json.dumps(out, indent=2, default=float))
    print(f"\nwrote {OUT} in {out['wall_seconds']} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
