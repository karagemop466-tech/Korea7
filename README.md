# Korea7 — GEMS submission research

**Current decision: DO NOT SUBMIT.** No competition raster, prior-submission registry, shared template, spatial holdout, or validated candidate exists in this checkout. [Executive summary and submission instructions](docs/index.html) · [Research and next steps](docs/research.md) · [Prior parallel review (historical)](docs/prior-review.md).

## Project starting point

At the start of each session, read this README and the [research log](docs/research.md). The standing user brief is to build an auditable, automated, continuously improving scientific workflow for unique, high-scoring GEMS fault-detection submissions; review the nine named GEMSDOE sites; preserve the distinction between organizer receipts, holdout results, and speculation; test feature leakage; run buffered fault-segment holdouts and duplicate checks; and provide a plainly marked, validated GeoTIFF only after all gates pass. Maximize the probability of a defensible win and own the outcome. Limit each parallel lane to three experiments or two hours; promotion and use of a weekly slot are separate. **The requested single method paragraph was not actually supplied.** Do not guess it. The full original user prompt is in the conversation, not reproduced verbatim here.

The user asks for autonomous work, but that does not override data access restrictions, uncertainty, or the need to follow competition rules. Never report a projection as a score, call user-reported numbers organizer-confirmed without a receipt, or recommend submission if any gate is unknown.

## What this repository actually contains

This branch began with only `README.md`. There is no `scripts/download_competition_data.sh`, `scripts/prepare_data.py`, cached feature stack, `evaluate_holdout.py`, `submission_writer.py`, prior run history, data, or website from previous sessions. The claim that data placement is the only remaining blocker therefore does not apply to this checkout. The [official reference repository](https://github.com/drivendataorg/gems-prize-reference-solution) is available separately and describes a notebook, not the requested shared template.

## Screening tool (not a submission approval)

`python -m venv .venv && .venv/bin/pip install -r requirements.txt`

`python scripts/check_candidate.py --candidate candidate.tif --surface surface.tif --reference sample_submission.tif --footprint footprint.tif --manifest registry.json`

All inputs are required. The footprint is an independently verified binary 0/1 raster on the reference grid; no footprint is inferred from nodata. The candidate and registry dots must be binary. The registry JSON is an array of objects with `site`, `surface`, `surface_sha256`, `dots`, and `dots_sha256`; paths resolve relative to the manifest. It must contain at least one entry for each of GEMSDOE24, 25, 27, 28, 30, 31, 32, 33 and 36, but this **does not prove registry completeness**. Hashes are full SHA-256 hex strings. The tool requires single-band GeoTIFF inputs with CRS, rejects any masked/nodata pixels, checks full-image finiteness and range (more conservative than checking only the footprint), grid alignment, surface rank correlation, and fraction of candidate dots within three Euclidean pixels of each registry dot raster. A threshold breach blocks. Constant or invalid surfaces block. `SCREENED_NOT_APPROVED` is deliberately not permission to submit: holdout performance, feature leakage, registry completeness, rules, and provenance remain unverified. This tool can be memory-intensive on large rasters.

Run tests: `.venv/bin/pytest -q`. Before placing dots, run `python scripts/check_candidate.py --surface surface.tif --reference sample_submission.tif --footprint footprint.tif --manifest registry.json` (omit `--candidate`). After placement run the full command above. Both statuses are screening only, not approval. All input rasters must be single-band GeoTIFFs without masked or nodata pixels; this conservative constraint can reject valid data outside the footprint. No implemented end-to-end pipeline or valid score estimate is claimed.

## Additional conservative format preflight

`scripts/validate_submission.py candidate.tif official_sample.tif` is a separate lightweight format-only check. It requires a single-band GeoTIFF, matching CRS, dimensions and transform, and finite unmasked values in [0,1] across the entire image. This conservative all-pixel rule may reject valid outside-footprint nodata. It reports SHA-256 but does not check holdout, leakage, uniqueness, ZIPs, or organizer acceptance; `ready_to_submit` is always false. See the [submission guide](docs/submission.html) and [negative run card](docs/run-card.json). The static site is not a live feed and deployment has not been verified.

The GitHub API returned HTTP 404 for the nine named site repositories on 2026-11-04; this does not establish that their sites or data do not exist. The [official reference README and notebook](https://github.com/drivendataorg/gems-prize-reference-solution) were accessed via GitHub: the notebook uses U-Net and random patch splits, not the required buffered segment holdout. No experiments or weekly submissions were performed in this session.

A parallel review also added `scripts/validate_raster.py` and its synthetic tests; like the other tools, it is a conservative format preflight, not a submission approval. The separate root `run-card.json` records that review's negative status.

## Latest review

The screening tool now has a separate pre-placement surface mode and rejects masked pixels, including masks hiding in-range values. See [review and remaining blockers](docs/review-2026-11-04.md). These are synthetic-test-backed safeguards, not a generated submission or validation against competition data.
