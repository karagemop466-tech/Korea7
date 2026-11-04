#!/usr/bin/env python3
"""One command: competition data in, validated unique GeoTIFF out.

    python scripts/build_submission.py --data data --out out/submission.tif

What it does, in order, and refuses to skip:

1. loads the feature stack, the mapped faults, and (if present) the official
   sample submission that defines the required grid;
2. builds independent (per-band lineament / gradient) and catalogue-derived
   features, and recomputes the catalogue ones *inside every fold* from the
   visible faults only;
3. runs a buffered, segment-blocked holdout with a per-feature leakage canary;
4. fits a ridge logistic model, calibrates score -> probability, and emits
   cells with the DTI-optimal emitter;
5. writes the GeoTIFF, validates the format, screens it against the GEMSDOE
   registry if one is supplied, and writes a run card.

Without the gated competition data the script stops at step 1 and says so.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gems import calibrate, emission, features as F, grid as G, holdout as H  # noqa: E402
from gems import metric as M, model, registry, validate, writer  # noqa: E402

CANDIDATE_NAMES = ("numeric_features.tif", "gems-geodawn-numerical-features.tif",
                   "training_features.tif")
LABEL_NAMES = ("labels.tif", "existing_faults.tif", "faults.tif")
REFERENCE_NAMES = ("sample_submission.tif", "example_submission.tif")


def find(data: Path, names):
    for n in names:
        p = data / n
        if p.exists():
            return p
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(ROOT / "data"))
    ap.add_argument("--out", default=str(ROOT / "out" / "submission.tif"))
    ap.add_argument("--emit", default="threshold",
                    choices=("coverage", "topk", "threshold", "nms"),
                    help="emitter; 'threshold' is the default because it won the "
                         "E2 comparison (see docs/results/e2_emission.json). "
                         "'coverage' is available but did not beat it.")
    ap.add_argument("--top-k", type=int, default=44090)
    ap.add_argument("--lam", type=float, default=0.30)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--buffer-px", type=int, default=5)
    ap.add_argument("--max-features", type=int, default=8)
    ap.add_argument("--train-pixels", type=int, default=300_000)
    ap.add_argument("--registry", default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--l2", type=float, default=10.0)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args(argv)

    t0 = time.time()
    data = Path(args.data)
    feats_p = find(data, CANDIDATE_NAMES)
    labels_p = find(data, LABEL_NAMES)
    ref_p = find(data, REFERENCE_NAMES)
    run = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "grid": G.describe(), "inputs": {"features": str(feats_p),
                                            "labels": str(labels_p),
                                            "reference": str(ref_p)},
           "status": "BLOCKED", "label": "no organizer confirmation"}
    if feats_p is None or labels_p is None:
        run["errors"] = [
            f"missing competition data in {data}: features={feats_p} labels={labels_p}",
            "These files are behind the DrivenData login; place them in data/ and rerun.",
            "No submission is written and no score is claimed.",
        ]
        _emit(run, args.out)
        print("\n".join(run["errors"]))
        return 2

    import rasterio
    names, arrays, meta, tags = F.stack(feats_p, labels_p, max_features=args.max_features)
    with rasterio.open(labels_p) as src:
        labels = src.read(1).astype(np.float32)
    truth = labels > 0
    shape = truth.shape
    run["shape"] = list(shape)
    run["features"] = names
    if ref_p is not None:
        with rasterio.open(ref_p) as src:
            ref_profile = {"width": src.width, "height": src.height,
                           "epsg": src.crs.to_epsg(), "transform": tuple(src.transform)[:6]}
        run["reference_profile"] = ref_profile
        if (ref_profile["height"], ref_profile["width"]) != shape:
            run["errors"] = ["label array does not match the reference grid; stop"]
            _emit(run, args.out)
            return 3

    indep_names = [n for n in names]
    # ---- holdout, with the catalogue features recomputed per fold from the
    #      visible faults only, and model selection done *inside* the holdout
    folds = H.make_folds(labels, k=args.folds, buffer_px=args.buffer_px, seed=args.seed)
    rng = np.random.default_rng(args.seed)
    variants = ("independent", "independent_plus_catalogue")
    fold_scores = {v: [] for v in variants}
    canaries, fold_rows = [], []
    for fold in folds:
        visible = np.where(~fold["buffer"], labels, 0)
        cat = F.catalogue_features(visible)
        feat = {n: a for n, a in zip(indep_names, arrays)}
        feat.update(cat)
        canaries.append({"fold": int(fold["fold"]), **H.canary(cat, H.fold_targets(labels, fold))})
        idx = _sample_idx(shape, rng, args.train_pixels)
        tgt = H.fold_targets(labels, fold)
        sm = H.scoring_mask(fold)
        tr = H.train_mask(fold).ravel()[idx] & (~fold["withheld"].ravel()[idx])
        row = {"fold": int(fold["fold"]), "withheld_px": int(fold["n_withheld_px"])}
        for v in variants:
            sub = indep_names if v == "independent" else list(feat)
            X = np.column_stack([feat[n].ravel()[idx] for n in sub]).astype(np.float64)
            y = truth.ravel()[idx]
            mu, sd = X[tr].mean(0), X[tr].std(0)
            keep = sd > 1e-6
            if not keep.any():
                fold_scores[v].append(0.0)
                row[v] = 0.0
                continue
            Xs = (X[:, keep] - mu[keep]) / (sd[keep] + 1e-9)
            mdl = model.fit_logistic(Xs[tr], y[tr], l2=args.l2)
            p = model.predict_logistic(mdl, Xs)
            cal, _ = calibrate.isotonic(p[tr], y[tr])
            q = np.zeros(shape, dtype=np.float32)
            q.ravel()[idx] = cal(p).astype(np.float32)
            lam = _best_lambda(q, tgt, sm)
            # the fold is scored with the *same* emitter that will produce the
            # delivered file, so the holdout number describes the file
            sel = _emit_like(args.emit, q, args, lam) * sm
            sc = M.dti(sel, tgt, mask=sm)["score"]
            fold_scores[v].append(sc)
            row[v] = round(sc, 4)
            row[f"{v}_lambda"] = lam
        fold_rows.append(row)
    chosen_variant = max(variants, key=lambda v: float(np.mean(fold_scores[v])))
    boot = H.bootstrap_ci(fold_scores[chosen_variant])
    run["holdout"] = {
        "variant_scores": {v: [round(x, 4) for x in fold_scores[v]] for v in variants},
        "variant_means": {v: round(float(np.mean(fold_scores[v])), 4) for v in variants},
        "chosen_variant": chosen_variant,
        "per_fold": fold_rows,
        "mean": round(float(np.mean(fold_scores[chosen_variant])), 4),
        "ci95": {"lo": None if boot["lo"] is None else round(boot["lo"], 4),
                 "hi": None if boot["hi"] is None else round(boot["hi"], 4)},
        "units": "fault segments (whole segments withheld, 5 px buffer)",
        "n_folds": len(folds), "evaluator": M.KERNEL_VERSION,
        "withheld_positive_px": [int(f["n_withheld_px"]) for f in folds],
    }
    trips = {f"fold{c['fold']}": [k for k, v in c.items()
                                 if isinstance(v, dict) and v.get("leakage_canary")]
             for c in canaries}
    run["leakage_canary"] = {"threshold_auc": H.CANARY_AUC, "trips": trips,
                             "detail": {k: v for k, v in canaries[0].items() if k != "fold"}}

    # ---- final model on all data
    cat_all = F.catalogue_features(labels)
    feat_all = {n: a for n, a in zip(indep_names, arrays)}
    feat_all.update(cat_all)
    sub = indep_names if chosen_variant == "independent" else list(feat_all)
    idx = _sample_idx(shape, rng, args.train_pixels)
    X = np.column_stack([feat_all[n].ravel()[idx] for n in sub]).astype(np.float64)
    y = truth.ravel()[idx]
    mu, sd = X.mean(0), X.std(0)
    keep = sd > 1e-6
    Xs = (X[:, keep] - mu[keep]) / (sd[keep] + 1e-9)
    mdl = model.fit_logistic(Xs, y, l2=args.l2)
    p = model.predict_logistic(mdl, Xs)
    calib_fn, calib_info = calibrate.isotonic(p, y)
    q_full = np.zeros(shape, dtype=np.float32)
    q_full.ravel()[idx] = calib_fn(p).astype(np.float32)
    sel, info = _emit_like(args.emit, q_full, args, args.lam, with_info=True)
    sel = np.clip(sel, 0.0, 1.0).astype(np.float32)

    profile = writer.make_profile()
    if ref_p is not None:
        profile = writer.make_profile(width=ref_profile["width"],
                                      height=ref_profile["height"],
                                      transform=ref_profile["transform"],
                                      epsg=ref_profile["epsg"])
    run["final_model"] = {"variant": chosen_variant, "n_features": int(keep.sum()),
                          "features_used": [n for n, k in zip(sub, keep) if k],
                          "features_dropped_constant": [n for n, k in zip(sub, keep) if not k],
                          "coefficients": [round(float(c), 4) for c in mdl["coef"]]}
    run["emission"] = {"method": args.emit, "emitted_cells": int((sel > 0).sum()),
                       "coverage_notes": info.get("dinkelbach") if info else None,
                       "calibration": calib_info}
    if args.no_write:
        run["status"] = "DRY-RUN"
        _emit(run, args.out)
        return 0

    wrep = writer.write_submission(args.out, sel, profile=profile)
    run["file"] = wrep
    vrep = validate.validate(args.out, reference=ref_p)
    run["validator"] = vrep
    if args.registry:
        run["uniqueness"] = registry.screen(args.out, manifest=args.registry)
    leakage_tripped = any(v for v in trips.values())
    gates = {
        "format_valid": vrep["status"] == "PASS",
        "holdout_beats_zero": float(np.mean(fold_scores[chosen_variant])) > 0.0,
        "no_leakage_canary_trip": not leakage_tripped,
        "uniqueness_pass": (run.get("uniqueness", {}).get("status") == "PASS"),
    }
    run["gates"] = gates
    run["status"] = ("READY_FOR_SELECTOR" if all(gates.values())
                     else "NOT_READY")
    run["note"] = ("HOLDOUT-DTI is our evaluator on withheld segments; it is not "
                   "a leaderboard score. Only an organizer receipt is a score.")
    run["wall_seconds"] = round(time.time() - t0, 1)
    _emit(run, args.out)
    print(json.dumps({k: run[k] for k in ("status", "gates", "holdout")}, indent=2))
    return 0 if run["status"] == "READY_FOR_SELECTOR" else 1


def _emit_like(method, q, args, lam, with_info=False):
    """One place where the emitter is chosen, used for folds and the final map."""
    if method == "coverage":
        sel, info = emission.coverage_emission(q, lam0=lam, rounds=5, top_k=args.top_k)
    elif method == "topk":
        sel, info = emission.topk_emission(q, args.top_k), None
    elif method == "nms":
        sel, info = emission.nms_emission(q, lam), None
    else:
        sel, info = emission.threshold_emission(q, lam), None
    return (sel, info) if with_info else sel


def _sample_idx(shape, rng, n):
    total = int(np.prod(shape))
    n = min(n, total)
    return np.sort(rng.choice(total, size=n, replace=False))


def _best_lambda(q, truth, mask, grid=(0.1, 0.2, 0.3, 0.4, 0.5)):
    best = (None, -1.0)
    for lam in grid:
        s = M.dti(emission.threshold_emission(q, lam), truth, mask=mask)["score"]
        if s > best[1]:
            best = (lam, s)
    return best[0]


def _emit(run, out):
    p = Path(out).with_suffix(".run.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(run, indent=2, default=str))
    print(f"run card: {p}")


if __name__ == "__main__":
    raise SystemExit(main())
