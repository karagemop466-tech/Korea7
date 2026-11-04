#!/usr/bin/env python3
"""Projection (NOT a score): SGMC-CAL HOLDOUT-DTI -> user-reported leaderboard.

Fit on the nine focus winners only (x = reproduced GEMSDOE32-SGMC-CAL-v3.0
HOLDOUT-DTI in evidence/eval_GEMSDOE*.json, y = USER-REPORTED values from
registry/owner_score_ledger.csv; no organizer receipts exist). Reports OLS,
Spearman, leave-one-out RMSE, and the candidate projection with an explicit
extrapolation flag when x lies outside the nine-point range. A projection is
never written as a score (protocol rule 3).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
REPORTED = {24: 0.2477, 25: 0.2600, 27: 0.2449, 28: 0.2710, 30: 0.2600,
            31: 0.2708, 32: 0.2778, 33: 0.2632, 36: 0.2750}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate-sgmc", type=float, required=True)
    ap.add_argument("--out", type=Path, default=ROOT / "evidence/calibration.json")
    a = ap.parse_args()

    xs, ys = [], []
    for n, y in REPORTED.items():
        p = ROOT / (f"evidence/eval_GEMSDOE{n}.json" if n != 32 else "evidence/repro_GEMSDOE32.json")
        xs.append(json.loads(p.read_text())["sgmc_off_catalogue"]["sgmc_prevalence_calibrated_dti"])
        ys.append(y)
    x, y = np.array(xs), np.array(ys)
    A = np.column_stack([x, np.ones_like(x)])
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    loo = []
    for i in range(len(x)):
        m = np.arange(len(x)) != i
        s_, b_ = np.linalg.lstsq(A[m], y[m], rcond=None)[0]
        loo.append(y[i] - (s_ * x[i] + b_))
    rmse = float(np.sqrt(np.mean(np.square(loo))))
    proj = float(slope * a.candidate_sgmc + intercept)
    out = {
        "label": "PROJECTION (not a score, not organizer-confirmed)",
        "fit_points": [{"site": f"GEMSDOE{n}", "sgmc_cal_holdout_dti": float(xi),
                        "user_reported": float(yi)} for n, xi, yi in zip(REPORTED, x, y)],
        "ols": {"slope": float(slope), "intercept": float(intercept)},
        "spearman_rho": float(spearmanr(x, y).statistic),
        "loo_rmse": rmse,
        "candidate_sgmc": a.candidate_sgmc,
        "candidate_projection": proj,
        "candidate_projection_interval_pm_loo_rmse": [proj - rmse, proj + rmse],
        "extrapolation": bool(a.candidate_sgmc > x.max() or a.candidate_sgmc < x.min()),
        "warnings": [
            "All nine fit points are one surface family (exact subset chain); the fit does not transfer automatically to a different surface.",
            "y values are user-reported without organizer receipts.",
            "If extrapolation is true, the numeric projection is shown only to be rejected as evidence; use the qualitative proxy-relative statement in the executive summary.",
        ],
    }
    a.out.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
