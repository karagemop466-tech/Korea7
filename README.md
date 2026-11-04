# Korea7 — GEMS fault-prospectivity research and submission audit

**Session start:** Read this README and [`docs/research.md`](docs/research.md) before project work. The goal is a rigorous, auditable workflow for identifying unmapped faults relevant to geothermal exploration and—only after independent gates pass—producing a unique, valid GeoTIFF for the DOE GEMS competition. Maximize the probability of a defensible win; own the outcome. A negative result is useful. Do not invent evidence, copy another entrant's prediction raster, or spend a weekly submission slot on an unvalidated idea.

## Executive decision

> **DO NOT DOWNLOAD OR SUBMIT a file from this checkout.** There is no generated candidate TIFF, no validated score estimate, and no completeness-verified registry. The site and local tools are review aids only; they do not approve or predict competition performance.

The strongest result supplied for the nine requested sites is the user-reported GEMSDOE32 entry `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` at **0.2778**. The value and mechanism have not been verified from an organizer receipt or the underlying raster. The prompt also gives two differing current-leader values (**0.3195** and **0.4413**); neither is independently confirmed here. No estimate should be presented as a score, and whether a new submission can beat 0.2778 is unknown until a trusted holdout is run and an organizer receipt exists.

- [Executive summary and nine-site comparison](docs/index.html)
- [Submission instructions and safety gates](docs/submission.html)
- [Evidence log, candidate hypotheses, limitations, and next steps](docs/research.md)
- [Historical parallel review](docs/prior-review.md)
- [Latest review and remaining blockers](docs/review-2026-11-04.md)
- [Current negative run card](docs/run-card.json)

## Standing evidence and experiment rules

1. Clearly distinguish **HOLDOUT-DTI** (evaluator version, withheld-positive count, and 95% CI) from **ORGANIZER-CONFIRMED** (copied from an actual submission receipt). A projection is never a score.
2. Use the shared template's cached feature stack, canonical holdout evaluator, and submission writer when they are available. Hold out whole fault segments with a buffer; derive every catalogue-dependent feature from visible faults only; mask visible faults pixel-exactly; use pooled DTI (alpha 0.2, beta 0.8, 300 m triangular kernel). Test each feature alone; AUC above 0.90 is a leakage alarm until explained. Fix a shared-tool defect once in the shared template, not a private fork.
3. Follow the assigned method lane only. Compare the pre-placement surface and final dots with the complete registry. If rank correlation is greater than 0.90, or more than 70% of candidate dots fall within 3 pixels of one registry raster's dots, mark duplicate/lane drift and stop. Do not infer uniqueness from a name or hash alone.
4. Stop at three experiments or two hours, whichever comes first. Promotion to a competition slot is a separate selector decision, under the current weekly cap.
5. A final run card must record hypothesis, mechanism, named non-fault mimic, HOLDOUT-DTI + CI, registry correlation/overlap, raster SHA-256, validator output (finite footprint, `[0,1]`, CRS/shape/transform), submission name, <=140-character note, and `promote` or `negative` verdict.

**Important protocol gap:** the prompt says this session's lane is “the single method paragraph below,” but no method paragraph is actually provided. Do not guess a lane or start a feature experiment until an authorized lane and the shared artifacts are present.

## Repository contents and limitations (reviewed 2026-11-04)

This checkout contains a static documentation site, raster format preflight/screening utilities, and synthetic unit tests. It does **not** contain the competition data, cached feature stack, complete prior-submission registry, official footprint/reference raster, canonical `evaluate_holdout.py`, canonical `submission_writer.py`, a model, or a submission GeoTIFF. The claimed data-placement-only blocker from earlier project notes does not match the current checkout. Competition data is described by the project brief as login-gated; no DrivenData credentials are available to this agent. Do not retrieve or use unofficial copies as if they were authoritative.

The nine GEMSDOE page values in the executive summary are reproduced from the user's prompt and are labelled user-reported. Site contents, exact historical raster bytes, receipts, uniqueness, and present leaderboard standings have not been independently verified in this environment. A file suffix such as `nan` is not proof of its pixel values.

### Local checks

Install dependencies and run the synthetic tests:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q
```

Pre-placement screening (no candidate dots yet):

```bash
.venv/bin/python scripts/check_candidate.py \
  --surface candidate_preplacement_surface.tif \
  --reference official_sample_submission.tif \
  --footprint official_footprint.tif --manifest complete_registry.json
```

Post-placement screening:

```bash
.venv/bin/python scripts/check_candidate.py \
  --candidate candidate.tif --surface candidate_preplacement_surface.tif \
  --reference official_sample_submission.tif \
  --footprint official_footprint.tif --manifest complete_registry.json
```

The manifest is a JSON array of entries with `site`, `surface`, `surface_sha256`, `dots`, and `dots_sha256`; paths resolve relative to the manifest. It must have an entry for each of GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, and 36. This checks only the supplied manifest—it cannot prove the registry is complete. The screen requires all inputs to be single-band GeoTIFFs with CRS and no masked/nodata pixels, and checks candidate format/range, grid alignment, hashes, surface rank correlation and dot proximity. Its statuses `SURFACE_SCREENED_NOT_APPROVED` and `SCREENED_NOT_APPROVED` are **not approval**. These strict checks may reject valid nodata outside the footprint. The tool does not implement the holdout or create a candidate raster; large-raster checks can be memory-intensive.

Format-only preflight (does **not** approve predictive skill, holdout performance, or uniqueness):

```bash
.venv/bin/python scripts/validate_submission.py candidate.tif official_sample_submission.tif
```

This requires a single-band GeoTIFF matching the reference grid and finite unmasked values in `[0,1]` across the entire image. The conservative all-pixel rule may reject valid outside-footprint nodata. `ready_to_submit` is always false: this is not an organizer validator.

## Research sources

Use the official links collected in [`docs/research.md`](docs/research.md), including the [DrivenData competition and rules](https://www.drivendata.org/competitions/306/competition-doe-gems/), [problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/), [data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/), [dynamic leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/), [official reference solution](https://github.com/drivendataorg/gems-prize-reference-solution), and [USGS GeoDAWN survey](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and). Links are supplied for source review, not as proof of current accessibility, licensing, coverage, or score claims. This static site is not a live feed.

## Remaining work before a defensible submission

1. Provide authorized competition data and sample raster, authoritative footprint/catalogue, the shared cached feature stack, canonical evaluator/writer, explicit method lane, and full prior-raster registry with pre-placement surfaces and hashes.
2. Verify current rules, official evaluation semantics, slot cap, and historical results against receipts. Resolve the conflicting reported leaderboard values.
3. Audit the canonical holdout/leakage workflow; correct shared defects once in the template. Run the top candidate on spatially buffered segment holdout before considering a slot.
4. Publish a downloadable TIFF only after predictive, uniqueness, format, provenance, and selector gates all pass. Keep the run card and artifact hash linked and explicit.
