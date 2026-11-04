# Korea7 — GEMS submission research

**Current decision: DO NOT SUBMIT.** No competition raster, prior-submission registry, shared template, spatial holdout, or validated candidate exists in this checkout. [Executive summary and submission instructions](docs/index.html) · [Research and next steps](docs/research.md).

## Project starting point

At the start of each session, read this README and the [research log](docs/research.md). The standing user brief is to build an auditable, automated, continuously improving scientific workflow for unique, high-scoring GEMS fault-detection submissions; review the nine named GEMSDOE sites; preserve the distinction between organizer receipts, holdout results, and speculation; test feature leakage; run buffered fault-segment holdouts and duplicate checks; and provide a plainly marked, validated GeoTIFF only after all gates pass. Maximize the probability of a defensible win and own the outcome. Limit each parallel lane to three experiments or two hours; promotion and use of a weekly slot are separate. **The requested single method paragraph was not actually supplied.** Do not guess it. The full original user prompt is in the conversation, not reproduced verbatim here.

The user asks for autonomous work, but that does not override data access restrictions, uncertainty, or the need to follow competition rules. Never report a projection as a score, call user-reported numbers organizer-confirmed without a receipt, or recommend submission if any gate is unknown.

## What this repository actually contains

This branch began with only `README.md`. There is no `scripts/download_competition_data.sh`, `scripts/prepare_data.py`, cached feature stack, `evaluate_holdout.py`, `submission_writer.py`, prior run history, data, or website from previous sessions. The claim that data placement is the only remaining blocker therefore does not apply to this checkout. The [official reference repository](https://github.com/drivendataorg/gems-prize-reference-solution) is available separately and describes a notebook, not the requested shared template.

## Screening tool (not a submission approval)

`python -m venv .venv && .venv/bin/pip install -r requirements.txt`

`python scripts/check_candidate.py --candidate candidate.tif --surface surface.tif --reference sample_submission.tif --footprint footprint.tif --manifest registry.json`

All inputs are required. The footprint is an independently verified binary 0/1 raster on the reference grid; no footprint is inferred from nodata. The candidate and registry dots must be binary. The registry JSON is an array of objects with `site`, `surface`, `surface_sha256`, `dots`, and `dots_sha256`; paths resolve relative to the manifest. It must contain at least one entry for each of GEMSDOE24, 25, 27, 28, 30, 31, 32, 33 and 36, but this **does not prove registry completeness**. Hashes are full SHA-256 hex strings. The tool checks full-image finiteness and range (more conservative than checking only the footprint), grid alignment, surface rank correlation, and fraction of candidate dots within three Euclidean pixels of each registry dot raster. A threshold breach blocks. Constant or invalid surfaces block. `SCREENED_NOT_APPROVED` is deliberately not permission to submit: holdout performance, feature leakage, registry completeness, rules, and provenance remain unverified. This tool can be memory-intensive on large rasters.

Run tests: `.venv/bin/pytest -q`. The screening checks both inputs in one invocation; **before placing any final dots**, use the same correlation method on the proposed surface against every complete registry surface. No implemented end-to-end pipeline or valid score estimate is claimed.
