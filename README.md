# Korea7 — DOE GEMS Prize (DrivenData #306) submission system

> **Read this file every time work resumes on this project.** It is the standing project
> brief and starting point. Goal: place top of the GEMS leaderboard with a unique, valid,
> downloadable GeoTIFF submission. Core values: Maximize P(Win); Own the Outcome.

## Competition (official sources)

- Competition page: https://www.drivendata.org/competitions/306/competition-doe-gems/
- Problem description: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
- Additional resources: https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/
- Data tab (login-gated): https://www.drivendata.org/competitions/306/competition-doe-gems/data/
- Leaderboard: https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/
- Reference solution: https://github.com/drivendataorg/gems-prize-reference-solution
- Official prize rules (NREL/TP-5700-96647, Sept 2026): https://docs.nlr.gov/docs/fy26osti/96647.pdf
- USGS GeoDAWN: https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and
- INGENIOUS / GDR: https://gdr.openei.org/submissions/1391
- EPSG:32611: https://epsg.io/32611
- Tversky index: https://en.wikipedia.org/wiki/Tversky_index

## Submission format (official, problem description page/967)

A single-band GeoTIFF (.tif), or a .zip containing exactly one GeoTIFF:
- CRS: projected UTM zone 11N (EPSG:32611)
- Resolution: 100 m
- Bounds: same as training data; data outside bounds is null/NaN
- One layer, 32-bit float (float32)
- Values in [0, 1] (confidence/probability of fault presence; higher = more likely)
- Error to avoid: "Predicted values must be in range [0, 1]" -> keep every in-footprint
  value finite and in [0, 1]; no NaN inside the footprint.

Official grid (as documented across GEMSDOE sites / GEMSDOE77):
- Shape: 3730 rows x 3292 cols
- Transform: (100, 0, 243350, 0, -100, 4508550)

Metric: distance-weighted Tversky index (DTI), alpha=0.2, beta=0.8, 300 m kernel
(reference solution implements this).

Leaderboard references (moving snapshot; not scores for this raster):
- Public leaderboard #1 = 0.4413 (organizer-confirmed)
- Prompt benchmark 0.3195 (user-quoted, not generated here)
- GEMSDOE sites: GEMSDOE32 H33-2-B2 claimed 0.2778 (owner/organizer-reported; some sources
  mark it unscored), GEMSDOE36 0.2750, GEMSDOE28 0.2710, GEMSDOE31 0.2708,
  GEMSDOE25 0.2600, GEMSDOE33 0.2632, GEMSDOE24 0.2477, GEMSDOE27 0.2449.

## Parallel-run protocol (binding)

1. LANE — one assigned method; stop if raster rank-correlation > 0.90 with a registry raster,
   or > 70% of dots within 3 px of one registry raster's dots. Check surface before placement
   AND on final dots.
2. REUSE, DON'T REBUILD — shared cached feature stack, shared evaluate_holdout.py and
   submission_writer.py; fix shared bugs once, never keep a private fork.
3. LABEL EVERY NUMBER as HOLDOUT-DTI (evaluator version, withheld positives, 95% CI) or
   ORGANIZER-CONFIRMED (receipt). Never write a projection as a score.
4. LEAKAGE CANARY — single-feature AUC > 0.90 = leakage until proven otherwise.
5. RUN CARD — one JSON card (run_card.json): hypothesis, mechanism, non-fault mimic,
   holdout DTI + CI, correlation/overlap vs registry, raster sha256, validator output,
   submission name + note (<=140 chars), verdict promote/negative.
6. BUDGET — stop after 3 experiments or 2 hours.

## Data-access blocker (flagged)

The competition data tab requires DrivenData login and redirects to login when fetched
anonymously. training_features.tif, existing_faults.tif, labels.tif and sample_submission.tif
are NOT accessible here. Therefore:
- Holdout DTI cannot be measured; any score quoted is a projection (never written as a score).
- Byte-conformance to sample_submission.tif cannot be verified yet.
- The generated TIF is structurally valid (CRS/shape/transform/dtype/range/NaN gates pass) but
  is NOT yet cleared to submit. Verdict: negative (run_card.json).

## Repository contents

- scripts/generate_submission.py — builds the unique submission GeoTIFF on the official grid
- scripts/validate_submission.py — automated submission-format validator (no human inspector)
- docs/downloads/*.tif — the downloadable submission candidate
- docs/index.html — GitHub Pages landing page (one-click download at the top)
- docs/executive-summary.html — per-site executive summary and download/submit guide
- hypotheses.md — 5 ranked novel geological hypotheses with free official sources
- run_card.json — JSON run card (protocol rule 5)

## How to submit (also in docs/executive-summary.html)

1. Download docs/downloads/korea7-k7-offcatalogue-relay-corridor-30000dots-20261104T000000Z-zeros.tif
2. Go to the GEMS Prize on DrivenData -> submission form -> "New submission"
3. Choose the .tif file (single file; or a .zip containing exactly one .tif)
4. Note (<=140 chars): "K7 off-catalogue relay-corridor binary dots; unique vs all GEMSDOE sites; holdout-validated score pending data access."
5. Submit. Up to 3 feedback submissions per week; choose one final submission.

## Status

- Unique TIF generated: YES (docs/downloads/), SHA-256 ef8ef331…
- Validator: ALL GATES PASS (single band, float32, EPSG:32611, 3730x3292, transform match,
  values in [0,1], no NaN inside footprint)
- OK TO DOWNLOAD: YES (for inspection)
- OK TO SUBMIT: NOT YET — pending DrivenData data access to conform to sample_submission.tif
  and measure holdout DTI (see run_card.json, verdict: negative)
