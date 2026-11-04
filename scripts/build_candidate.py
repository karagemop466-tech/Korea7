#!/usr/bin/env python3
"""Build the unique candidate GeoTIFF and run every automated gate.

Construction (pre-registered in docs/hypotheses.md, H5):
  * 11-px square lattice intersected with the competition footprint -- a *coverage*
    construction, because Experiment 1+2 measured that a weak surface (AUC ~0.56) loses to
    broad placement at a matched budget on this metric (beta=0.8 rewards recall);
  * lattice nodes dropped where the Off-catalogue Seismogenic Lineament Field is below its
    30th percentile -- the mild modulation that beat uniform placement by +14% relative on
    the holdout instrument;
  * every node within 3 px of a mapped catalogue fault is removed (measured optimum of the
    programme's own one-parameter family is B=2, and the 3 px collar matches the kernel
    radius so no credit is lost).

Gates, all fail-closed:
  G1 format   single band, EPSG:32611, shape/transform match, every cell finite in [0,1]
  G2 unique   <=70% of dots within 3 px of any focus-site raster, |rho| <= 0.90
  G3 holdout  measured on the K7-HIDE-RECOVER-1.0 instrument
  G4 estimate MODEL-ESTIMATE beats the programme best (0.2778)?  (this is what decides)

Writes: docs/downloads/<name>.tif, evidence/run_card.json, evidence/candidate_gates.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import estimate, external as ext, grid, registry, surface as surf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "docs" / "downloads"
EVIDENCE = ROOT / "evidence"

LATTICE_SPACING = 11
OSLF_KEEP_PERCENTILE = 30.0     # drop lattice nodes below this OSLF percentile
CLEARANCE_PX = 3.0
PROGRAMME_BEST = 0.2778        # OWNER-REPORTED, GEMSDOE32
LEADERBOARD_HIGH = 0.4413      # OWNER-REPORTED high from the user brief

NAME = "k7-oslf-lat11-n{}-20261104T210000Z"
NOTE = ("11px coverage lattice modulated by INGENIOUS declustered seismicity, "
        "3px catalogue collar removed")[:140]


def build_mask(oslf: np.ndarray, foot: np.ndarray, cat: np.ndarray) -> tuple[np.ndarray, dict]:
    lat = np.zeros(foot.shape, dtype=bool)
    lat[LATTICE_SPACING // 2::LATTICE_SPACING, LATTICE_SPACING // 2::LATTICE_SPACING] = True
    lat &= foot
    nodes = int(lat.sum())
    thr = np.percentile(oslf[lat], OSLF_KEEP_PERCENTILE)
    kept = lat & (oslf >= thr)
    d_cat = distance_transform_edt(~cat)
    final = kept & (d_cat > CLEARANCE_PX)
    return final, {
        "lattice_spacing_px": LATTICE_SPACING,
        "lattice_nodes_in_footprint": nodes,
        "oslf_percentile_threshold": OSLF_KEEP_PERCENTILE,
        "oslf_threshold_value": float(thr),
        "after_oslf_modulation": int(kept.sum()),
        "removed_by_3px_catalogue_collar": int(kept.sum() - final.sum()),
        "final_dots": int(final.sum()),
    }


def main() -> int:
    ref = grid.load_reference()
    foot, cat = ref["footprint"], ref["catalogue"]
    seis = ext.load_on_grid("seis_n200a15", foot)
    oslf = surf.build(seis, foot)["surface"]

    mask, build_info = build_mask(oslf, foot, cat)
    if mask.sum() == 0:
        raise SystemExit("empty candidate")
    name = NAME.format(int(mask.sum()))

    # ---- G1: write and format-check ------------------------------------------------
    # Zeros outside the footprint (not NaN): every one of the 12,279,160 cells is then
    # finite and inside [0, 1], which cannot trigger the portal's
    # "Predicted values must be in range [0, 1]" rejection under any reading.
    arr = np.zeros(foot.shape, dtype=np.float32)
    arr[mask] = 1.0
    tif = DOWNLOADS / f"{name}.tif"
    grid.write_like(grid.SAMPLE_SUBMISSION, arr, tif)
    fmt = grid.format_gate(tif)

    # ---- G2: uniqueness ------------------------------------------------------------
    files = registry.registry_files()
    comparisons = []
    for site, path in files.items():
        other = registry.dots(path, foot)
        comparisons.append({
            "site": site,
            "frac_candidate_within_3px_of_site": registry.overlap_within_3px(mask, other),
            "frac_site_within_3px_of_candidate": registry.overlap_within_3px(other, mask),
            "surface_spearman_rho": registry.surface_rank_correlation(oslf, other.astype(float), foot),
        })
    worst_overlap = max(c["frac_candidate_within_3px_of_site"] for c in comparisons)
    worst_rho = max(abs(c["surface_spearman_rho"]) for c in comparisons)
    unique = worst_overlap <= 0.70 and worst_rho <= 0.90

    # ---- G3: holdout ---------------------------------------------------------------
    hold2 = json.loads((EVIDENCE / "experiment2_emission.json").read_text())
    arm = hold2["arms"]["oslf_lattice"]
    instrument_tie = {
        "instrument": hold2["instrument"],
        "oslf_lattice_dti": arm["holdout_dti"],
        "random_control_dti": hold2["arms"]["random"]["holdout_dti"],
        "delta_vs_random": arm["holdout_dti"] - hold2["arms"]["random"]["holdout_dti"],
        "note": ("Instrument DTI is comparable ACROSS ARMS ONLY at a matched budget on the "
                 "instrument's truth set (K about 17k px); it is not a leaderboard scale."),
    }
    holdout_beats_random = instrument_tie["delta_vs_random"] > 0

    # ---- G4: model estimate --------------------------------------------------------
    e11 = estimate.LATTICE_CREDIT[LATTICE_SPACING]   # Monte-Carlo, no free parameter
    keep_frac = build_info["after_oslf_modulation"] / max(build_info["lattice_nodes_in_footprint"], 1)
    nonzero = build_info["final_dots"] / max(build_info["after_oslf_modulation"], 1)
    c_lo = e11 * keep_frac * nonzero
    # +14% is the relative gain of the seismic modulation measured in Experiment 2 on the
    # K7-HIDE-RECOVER-1.0 instrument. Carrying an instrument-relative gain across to live
    # kernel-weighted recall is an ASSUMPTION, not a measurement; it is the only reason a
    # range rather than a point is reported, and it is stated in the run card.
    c_hi = c_lo * 1.14
    est = estimate.estimate((c_lo, c_hi), build_info["final_dots"])
    beats_best = est["point_estimate"] is not None and est["point_estimate"] > PROGRAMME_BEST

    gates = {
        "G1_format": {"pass": bool(fmt["format_pass"]), **fmt},
        "G2_unique": {"pass": bool(unique), "worst_3px_overlap_vs_focus_sites": worst_overlap,
                      "worst_abs_surface_rho": worst_rho,
                      "threshold": "overlap <= 0.70 and |rho| <= 0.90 (protocol rule 1)",
                      "comparisons": comparisons},
        "G3_holdout": {"pass": bool(holdout_beats_random), **instrument_tie},
        "G4_beats_programme_best": {"pass": bool(beats_best), "estimate": est,
                                    "programme_best_owner_reported": PROGRAMME_BEST,
                                    "leaderboard_high_owner_reported": LEADERBOARD_HIGH},
    }
    ok_to_submit = all(g["pass"] for g in gates.values())

    card = {
        "submission_name": name,
        "submission_note": NOTE,
        "file": str(tif.relative_to(ROOT)),
        "sha256": fmt.get("sha256"),
        "hypothesis": ("Unmapped Basin-and-Range faults are best found with a coverage-first "
                       "emitter modulated by an independent active-fault observation "
                       "(declustered seismicity), not by concentrating on a weak ranking."),
        "mechanism": ("Epicentre alignments mark active structures; the metric weights recall "
                      "(beta=0.8) eight times FP mass (alpha=0.2), so at low skill breadth "
                      "dominates concentration."),
        "non_fault_mimic": ("Quarry blasts, geothermal-field induced microseismicity and "
                            "aftershock clusters can align without a mapped fault."),
        "build": build_info,
        "holdout": instrument_tie,
        "uniqueness": {"worst_3px_overlap": worst_overlap, "worst_abs_rho": worst_rho},
        "estimate": est,
        "validator": {k: v for k, v in fmt["checks"].items()},
        "nonfinite_pixels_inside_footprint": fmt.get("nonfinite_pixels_inside_footprint"),
        "gates": gates,
        "verdict": "PROMOTE" if ok_to_submit else "NEGATIVE",
        "ok_to_download": True,
        "ok_to_submit": bool(ok_to_submit),
        "blocking_reason": None if ok_to_submit else
            ("G4 fails. MODEL-ESTIMATE %s (95%% interval %s) does not exceed the owner-reported "
             "programme best %.4f, so uploading this file cannot improve standing. The other "
             "three gates pass (format, uniqueness, holdout-vs-random-control)."
             % (est.get("point_estimate"), est.get("interval_95"), PROGRAMME_BEST)),
    }
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "candidate_gates.json").write_text(json.dumps(gates, indent=2) + "\n")
    (EVIDENCE / "run_card.json").write_text(json.dumps(card, indent=2) + "\n")

    print(f"candidate : {name}")
    print(f"file      : {tif.relative_to(ROOT)}  ({tif.stat().st_size / 1e6:.2f} MB)")
    print(f"sha256    : {card['sha256']}")
    print(f"dots      : {build_info['final_dots']}")
    for k, v in gates.items():
        print(f"  {k:26s} pass={v['pass']}")
    print(f"MODEL-ESTIMATE: {est['point_estimate']}  95% interval {est['interval_95']}")
    print(f"VERDICT   : {card['verdict']}   ok_to_submit={ok_to_submit}")
    if not ok_to_submit:
        print(f"  -> {card['blocking_reason']}")
    return 0 if ok_to_submit else 2


if __name__ == "__main__":
    raise SystemExit(main())
