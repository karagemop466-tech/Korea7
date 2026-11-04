# Research log and hypothesis queue

*Updated 2026-11-04. Read this with the [executive summary](index.html) and the
[source audit](verification.html).*

## Current state, stated plainly

| Item | Status |
|---|---|
| Competition data (`numeric_features.tif`, `labels.tif`, `sample_submission.tif`) | **absent** (DrivenData login; unreachable from the build sandbox) |
| Nine GEMSDOE sites | **unreachable** (`*.github.io` does not resolve; `api.github.com/users/buffedlizard55-lab` = 404) |
| Metric implementation | reproduced and unit-tested; provenance is the public description plus two independent implementations, **not** organizer code |
| Holdout harness, validator, writer, registry screen | implemented, tested, exercised end to end on synthetic data |
| Submission-grade GeoTIFF | **none** - and none should be produced without the three files above |
| Organizer receipt for any score | **none** |

## Why 0.2778 led the nine sites (answer, with the arithmetic)

The metric credits true positives with a **max** over a 300 m kernel and charges false positives with
a **sum** over every positive pixel. A sparse binary map therefore pays no density tax, while a
smooth probability field pays for every cell. Exact consequences (`gems.metric.band_table`):
a 1-px band on target scores 1.0000; 3 px scores 0.8333; 5 px scores 0.6250; a 3-px offset scores 0.
A uniform 0.02 background over 201x201 cells with one true fault cell scores 0.0001.

Every leader in the nine-site list is a sparse, catalogue-anchored binary map ("dotted", "offcat",
"tip step-over", "gap closure", "rung"). Every smooth-field method elsewhere in the wider list lands
at 0.02-0.15. So 0.24-0.28 is an **emission** result, not a detection result.

Simulation (E3, calibrated testbed) says the same thing quantitatively: against unmapped faults,
catalogue geometry is worth 0.0146 +/- 0.0059 (95% CI), a weak evidence field (pixel AUC 0.62-0.65)
is worth 0.2705 +/- 0.0408, and perfect placement of everything visible caps at 0.5869 +/- 0.1361 -
which is where the reported 0.4413 leader sits. **Beating 0.28 is an evidence problem, not a
placement trick.** Note also that emitting *more* than the scored set is penalised: in the
near-miss regime the oracle (0.1237) scores worse than the weak evidence field (0.2154).

## Five candidate hypotheses we have not tried, ranked

Each names the layers, the physical signature, why it should catch a *missing* fault rather than one
already catalogued, the non-fault process that could mimic it, the implementation cost, and whether it
can be validated **without new external data**. "Expected gain" is a judgement, not a measurement;
nothing here has been run, because the features are gated.

| Rank | Hypothesis, layers and signature | Why it catches an unmapped fault | Named non-fault mimic | Cost | Validatable without new data? | Expected gain |
|---|---|---|---|---|---|---|
| 1 | **Cross-band second-derivative concordance.** Elevation, magnetics (RTP/tilt), gravity, K, eTh, eU. Require the Hessian ridge orientation to agree within +/-15 deg across at least three *independent* physical fields, then combine by rank product. | A real fault perturbs several independent potential fields coherently; a lithologic contact or a drainage line typically appears in one or two, not five. Concordance therefore raises precision exactly where the catalogue is blank. | Flight-line striping (shared orientation across magnetic *and* radiometric channels - gate on acquisition type), and vegetation/moisture in radiometrics. | Medium (already supported by `gems/features.py`; needs an orientation-agreement stage) | **Yes** - uses only bands already in the stack | High |
| 2 | **Tilt-angle "worm" morphology.** Magnetics. Skeletonise the ridges of the tilt derivative and classify worms by length, curvature and whether they are paired: long worms = faults, paired = dykes, short = contacts. | Worm length and pairing discriminate *structure* from *contact*, which proximity-to-catalogue cannot do; worms extend under cover where scarps are invisible. | Dyke swarms, acquisition levelling artefacts, and deep-source noise in low-gradient areas. | Medium | **Yes** (magnetics band present; needs ridge/topology code) | Medium-high |
| 3 | **Relay-ramp curvature asymmetry.** DEM only. Across-strike profile of the second derivative, normalised by along-strike continuity, looking for opposing-facing scarps in an overlapping-tip geometry. | Relay ramps sit *between* mapped tips, i.e. exactly in the gaps the catalogue leaves; opposing scarp polarity is a geometric signature no single-point feature captures. | Fluvial cut banks, landslide head scarps, and shorelines (all single-sided, so polarity agreement is the discriminator). | Low-medium | **Yes** (DEM band) | Medium |
| 4 | **Transverse-drainage deflection and knickpoint alignment.** DEM. Extract channel centrelines, measure lateral deflection and along-channel slope breaks; test whether breakpoints cluster on one line. | Active faults with no scarp expression still deflect channels and align knickpoints; this reaches faults the topographic-ridge features cannot see. | Lithologic hardness boundaries and regional base-level fall (both produce knickpoints but not *aligned* ones). | High (hydrology preprocessing) | **Yes**, but computationally the heaviest | Medium |
| 5 | **Euler depth-cluster alignment.** Magnetics plus gravity. Euler deconvolution source depths, clustered along strike: fault-controlled hydrothermal systems give 2-6 km clusters. | Gives a *depth* dimension the other features lack, separating deep basement structures from shallow surficial noise. | Depth-to-basement variation from lithology; window-size sensitivity in Euler deconvolution. | High | **Yes** in principle; needs careful window tuning to be trustworthy | Unknown |

Two further ideas were rejected before ranking, and the reason is worth recording:

* **"Use a more complete external fault catalogue"** (e.g. USGS Qfaults national, public domain,
  free: `earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults/MapServer/21`). It is legitimate
  outside data and it does differ from the 2021 Nevada release, but E3 shows geometry-only placement
  scoring 0.015 against unmapped faults; a second geometry source adds a small amount of *new*
  geometry, not a new physical signature. It is also already attempted publicly ("sgmc-off-catalogue",
  "offcat" families). **Rejected as a primary lane; kept as a candidate union member.**
* **"Denser placement near the catalogue to raise recall"** (dilation, buffer bands). Exactly
  backwards: 5-px bands lose 37% of the achievable score before a single mistake, and E3's
  `catalogue_dilate3` scores 0.0059 against unmapped faults. **Rejected on arithmetic.**

## External data, if we go beyond the provided stack

| Need | Free official source | Accessible from this sandbox? |
|---|---|---|
| Magnetic/radiometric grids (GeoDAWN) | USGS data release, `https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and` | No (`usgs.gov` not on the allowlist) |
| Fault catalogue, national | USGS Qfaults REST service (public domain) | No |
| Nevada ML data release (gravity, lineations, heat flow) | `https://doi.org/10.5066/P9V5SQRD` | No |
| 1 m lidar DEM tiles | competition `1m_DEM_links.csv` (login) | No |
| Projection definition | `https://epsg.io/32611` | No (but PROJ ships the definition locally, which is how the grid was verified) |

Nothing in the ranked list above needs any of these; that is deliberate, because the sandbox cannot
reach them and a hypothesis that cannot be validated is not a hypothesis we should spend a slot on.

## Next steps, in order

1. Put the three competition files in `data/` and run
   `python scripts/build_submission.py --data data --out out/submission.tif`. Read the run card.
2. Build a registry manifest from the nine sites' rasters (if you can obtain them) so the uniqueness
   gate can move from `UNKNOWN` to a real verdict.
3. Implement hypothesis **#1** (cross-band concordance) behind a flag, and test it in the existing
   buffered segment holdout against the current best. Three experiments, two hours, then stop.
4. Only after that: decide about a weekly slot, separately from the experiment that produced the
   candidate.

## Run card (this session)

```json
{
  "hypothesis": "the 0.24-0.28 plateau is an emission artefact and the leaderboard headroom is in per-cell evidence",
  "mechanism": "TP_w is a max over a 300 m kernel, FP_w is a sum over positives; sparse calibrated binary emission removes the density tax",
  "named_non_fault_process": "dilation of already-mapped faults raises recall on new faults near old ones without any new information (measured: 0.0059 against unmapped faults)",
  "holdout_dti": "SIMULATION only: 0.2705 (CI half-width 0.0408) for weak evidence vs 0.0146 (0.0059) for catalogue geometry, R2 regime; no competition holdout exists (data gated)",
  "evaluator_version": "dti-tri-300m-a0.2-b0.8-v1",
  "withheld_positives": "5 folds, 568-7829 px per fold, 5 px buffer, segment-blocked",
  "ci_95": "segment bootstrap, 2000 resamples",
  "registry_correlation": "UNKNOWN - the nine GEMSDOE rasters are unreachable",
  "registry_overlap": "UNKNOWN",
  "raster_sha256": null,
  "validator_output": "format probe file validates PASS (single band, CRS/shape/transform match, finite, in [0,1]); no submission-grade raster produced",
  "submission_name": null,
  "submission_note": null,
  "verdict": "negative for the novel emitter (coverage greedy -0.2319 vs top-k); positive for the engineering path; no promotion"
}
```
