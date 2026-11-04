> **Historical note:** this is a prior-session review. It is superseded by `docs/research.md`, `docs/index.html`, and `docs/executive-summary.html`. The current repository contains a validated, unique TIF; do not use this file's "no candidate" conclusion.

# Korea7 — GEMS fault-prospectivity submission audit

> **Session starting point:** Read this README before each project session. Keep the objective, evidence rules, and experiment limits below in force. This repository currently contains documentation only; it does not contain competition rasters, cached features, validation code, a submission writer, or an existing website.

## Objective and non-negotiable evidence rules

Build an auditable workflow for predicting unmapped faults relevant to geothermal exploration for the DOE GEMS competition. Improve the chance of a strong leaderboard result without claiming a score that has not been measured. Generated competition predictions must be a single-band GeoTIFF matching the organizer's CRS, dimensions, and affine transform, with valid finite predictions in `[0, 1]` over the submission footprint. Make a downloadable file and its exact validation status obvious; never call an unvalidated file ready to submit.

- Distinguish **HOLDOUT-DTI** (evaluator/version, withheld-positive count, and 95% confidence interval) from **ORGANIZER-CONFIRMED** (a score copied from a submission receipt). A model projection is not a score.
- Do not copy or republish another entrant's prediction raster. Novelty claims require actual raster comparisons and SHA-256 records. Check registry-raster rank correlation and dot overlap before and after candidate placement; the lane limits stated in the project brief are correlation `<= 0.90` and no more than `70%` of dots within 3 pixels of one registry raster. Report a violation as duplicate/drift and stop.
- Use the shared template's cached feature stack, holdout evaluator, and submission writer where they exist. Hold out whole fault segments with a buffer, derive catalogue-dependent features from visible faults only, mask visible faults pixel-exactly, and evaluate pooled DTI with alpha `0.2`, beta `0.8`, and a 300 m triangular kernel. Test each feature alone; AUC above `0.90` is a leakage alarm until explained.
- Experiment ceiling: at most 3 experiments or 2 hours, whichever comes first. Do not spend a weekly competition submission slot as part of model selection. A negative result is a valid deliverable.
- Final run card must include hypothesis, mechanism, plausible non-fault mimic, holdout DTI + CI, registry correlation/overlap, raster SHA-256, validator results (finite footprint, `[0,1]`, CRS/shape/transform), submission name and <=140-character note, and `promote` or `negative` verdict.

## Current repository state (verified locally 2026-11-04)

The checkout is branch `arena/edf0fdc5-korea7`, based on the initial commit. At review time it contained only this README and no data, scripts, tests, raster assets, cached feature stack, site, or trained model. Consequently no holdout experiment, leakage test, raster uniqueness comparison, submission validation, or TIFF generation can honestly be performed here. Do not invent these results or claim a TIFF is ready. The supplied competition dataset is gated behind DrivenData login according to the project brief; no credentials or data files are present in this checkout.

## Prior-reported leaderboard results — unverified reports, not scores measured here

The numbers below are reproduced from the user's supplied project notes. They are **not** independently confirmed receipts and must not be described as this repo's validation results. Sites in scope: GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, and 36.

| Site | Reported leading submission | Reported score | Status / submit guidance |
|---|---|---:|---|
| GEMSDOE24 | `h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan` | 0.2477 | User-reported only; not an independent submission recommendation |
| GEMSDOE25 | `dotted-h19-5-d2-8-20261002-e56ea318af89-nan` | 0.2600 | User-reported only; not an independent submission recommendation |
| GEMSDOE27 | `topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan` | 0.2449 | User-reported only; not an independent submission recommendation |
| GEMSDOE28 | `h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan` | 0.2710 | User-reported only; not an independent submission recommendation |
| GEMSDOE30 | `d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca` | 0.2600 | User-reported only; not an independent submission recommendation |
| GEMSDOE31 | `h27-4-solo-d28-20261004-8acb75e1-nan` | 0.2708 | User-reported only; not an independent submission recommendation |
| GEMSDOE32 | `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` | 0.2778 | Highest among supplied results for these target sites; user-reported only; no raster/receipt available here |
| GEMSDOE33 | `h33d-analog-tip-stepover-r30-20261004-cb490425926e` | 0.2632 | User-reported only; not an independent submission recommendation |
| GEMSDOE36 | `anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros` | 0.2750 | User-reported only; not an independent submission recommendation |

**Executive conclusion:** Based only on the supplied list, GEMSDOE32's listed result (0.2778) is the best reported result among the nine sites. This does not explain causality, establish that its raster is unique, confirm the result with the organizer, or show that a new method can beat it. No file is currently confirmed OK to download and submit. The reported `nan` suffixes on several names are a warning, not proof of invalid pixel values: inspect actual rasters with the organizer's footprint/format requirements before any submission. The prompt separately states a current competition high score of `0.3195` (and elsewhere `0.4413`); these are conflicting, undated user-provided claims and require leaderboard/receipt verification.

## Submission validation gate

A submission is **OK to download and submit** only when all of the following are true and reported from the actual output:

1. It is one-band GeoTIFF (or ZIP with exactly one such TIFF).
2. CRS, shape, and geotransform exactly match the organizer's sample submission.
3. Every prediction inside the evaluation footprint is finite and within `[0,1]`; nodata handling is correct. No accidental NaNs or out-of-range values.
4. Spatially blocked holdout beats the current internal baseline, with version, positive count, and 95% CI documented; no leakage-canary failure remains unexplained.
5. It passes the lane correlation/overlap comparison against registry rasters, and SHA-256 is recorded.
6. Output is uniquely named, accompanied by a <=140-character note, and available as a direct downloadable artifact.
7. The file is never labelled organizer-scored until a submission receipt confirms the score.

At present this gate cannot be run: the reference/sample raster, catalogue, features, evaluator, writer, and candidate raster are absent. The only substantiated answer to “can we beat 0.2778?” is **not yet known**; a positive answer requires a valid holdout and ultimately an organizer receipt. The values in the table are organizer-reported only if independently backed by receipts; in this repo they remain user-reported.

## Candidate research queue (not tested; no implementation/score claims)

The competition brief and repo currently provide no local raster stack or official source data to evaluate these ideas. These are hypotheses for a later, capped experiment cycle—not validated candidates and not yet confirmed absent from other projects:

| Rank | Candidate hypothesis | Layers/signature and missing-fault rationale | Main mimic | Expected value / cost | Validation prerequisite |
|---|---|---|---|---|---|
| 1 | Multi-scale magnetic-gradient discontinuity coherence | Geodawn magnetic grid; compare analytic-signal amplitude and directional horizontal-gradient edges across scales. A coherent basement boundary may reveal unmapped structures not captured by mapped-fault proximity. | Lithologic contacts, survey-line artifacts, cultural magnetic sources | Medium / medium | Numerical features raster and segment-blocked holdout; verify transform definitions and each feature AUC |
| 2 | DEM-derived drainage/valley deflection at structural intersections | Official 1 m DEM; quantify channel curvature, local relief, and aligned knickpoints where independent topographic lineaments intersect. May detect subtle active/young structures absent from catalogue. | Lithology, roads, vegetation, drainage engineering | Medium / high | DEM coverage, hydrology preprocessing, catalogue-masked spatial holdout |
| 3 | Radiometric boundary concordance conditioned on magnetic edges | Geodawn K, eTh, eU channels; test cross-channel compositional gradients that align with independent structural edges. Could surface alteration/exposure contrasts around unrepresented breaks. | Soil/moisture, surficial deposits, flight-line striping | Low–medium / medium | Numerical feature channels, acquisition QA, feature-only leakage checks |
| 4 | Multi-source lineament orientation discontinuity | DEM aspect/slope and magnetic gradient orientations; seek segmented, cross-scale orientation changes rather than simply densifying known lineaments. | Bedding, drainage networks, glacial/erosional forms | Low–medium / high | DEM plus Geodawn grids; preregistered lineament extraction and blocked holdout |
| 5 | Geothermal alteration proxy from public chemistry/mineral mapping | No chemistry/mineral alteration layer is present in this repo. USGS/INGEIOUS source data would need to be identified, confirmed openly downloadable, spatially complete, and license/coverage checked before considering. | Lithologic variation and sampling bias | Unknown / very high | Specific official datasets and verified access; therefore not currently viable |

Do not assert any candidate is “new” until comparing against actual repository methods and the listed registry rasters. Prior user notes cite a USGS GeoDawn survey landing page and the GBC/INGENIOUS project; links below are supplied for review, not independently fetched in this checkout.

## Sources for manual review

- DrivenData competition overview: <https://www.drivendata.org/competitions/306/competition-doe-gems/>
- Competition problem description: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/>
- Competition about page: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/>
- Competition data page (login may be required): <https://www.drivendata.org/competitions/306/competition-doe-gems/data/>
- Leaderboard (dynamic; verify current date and score): <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
- DrivenData reference solution: <https://github.com/drivendataorg/gems-prize-reference-solution>
- DOE/NLR GEMS solicitation PDF cited in brief: <https://docs.nlr.gov/docs/fy26osti/96647.pdf>
- USGS GeoDawn survey page: <https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and>
- GBC/INGENIOUS: <https://gbcge.org/current-projects/ingenious/>
- EPSG:32611: <https://epsg.io/32611>
- Tversky index background: <https://en.wikipedia.org/wiki/Tversky_index>
- User-supplied reported-results sites: [24](https://buffedlizard55-lab.github.io/GEMSDOE24/), [25](https://buffedlizard55-lab.github.io/GEMSDOE25/), [27](https://buffedlizard55-lab.github.io/GEMSDOE27/), [28](https://buffedlizard55-lab.github.io/GEMSDOE28/), [30](https://buffedlizard55-lab.github.io/GEMSDOE30/), [31](https://buffedlizard55-lab.github.io/GEMSDOE31/docs/), [32](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html), [33](https://buffedlizard55-lab.github.io/GEMSDOE33/), [36](https://buffedlizard55-lab.github.io/GEMSDOE36/docs/).

## Next work / limitations

1. Establish authenticated, permitted access to competition data; place the official sample submission, catalogue/labels, feature raster, and any allowed DEM inputs in documented data paths. Never commit credentials or large protected data.
2. Recover the shared template cache and the canonical `evaluate_holdout.py` / `submission_writer.py` from the appropriate maintained source; this checkout has none. Verify their metric and exact masking semantics before trusting them.
3. Download the nine registry rasters and metadata where permitted; calculate hashes, correlation and dot overlap. Confirm leaderboard results from organizer receipts rather than page summaries alone.
4. Implement automated tests for validator edge cases (NaN, infinity, values just outside bounds, nodata/footprint, band count, CRS, dimensions, transform, ZIP member count) and a report generator that makes “not ready” explicit.
5. Run no more than three predeclared experiments or two hours; attach code/version, holdout DTI and CI, canary, uniqueness diagnostics, and run card for each. Only then consider a separate selector/weekly-slot decision.
6. Build the requested simple public site only once the tested workflow exists; never publish a fabricated download or score.

**Current run card:** `hypothesis`: none evaluated; `mechanism`: none evaluated; `non-fault mimic`: not applicable; `HOLDOUT-DTI + CI`: unavailable (no evaluator/data); `registry correlation/overlap`: unavailable (no registry rasters); `raster SHA-256`: none (no generated raster); `validator`: not run (no reference raster); `submission name/note`: none; `verdict`: `negative` (no promotable artifact; this is a deliverable status, not a model performance result).
