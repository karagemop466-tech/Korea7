# Standing prompt — Korea7 GEMS submission project

> This is the working brief for every session. Read it before changing code, generating a
> raster, or recommending a submission. The full original prompt is in the conversation;
> this file preserves the requirements that govern the work.

## Objective

Build an auditable, automated, continuously improving scientific workflow that produces a
**unique, high-scoring GEMS fault submission** for the DrivenData / DOE GEMS Prize Challenge.
The goal is to place at the top of the leaderboard, not merely to produce a syntactically valid
GeoTIFF.

## Competition facts (official)

- Competition: <https://www.drivendata.org/competitions/306/competition-doe-gems/>
- Problem description and metric: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/>
- About the data: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/>
- Data tab (login required): <https://www.drivendata.org/competitions/306/competition-doe-gems/data/>
- Leaderboard: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
- Reference solution: <https://github.com/drivendataorg/gems-prize-reference-solution>
- Metric: distance-weighted Tversky index, α=0.2, β=0.8, 300 m triangular kernel.
- Submission: single-band float32 GeoTIFF, EPSG:32611, 100 m, same bounds as training data,
  values in [0,1], null or NaN outside the bounds.
- Test set: newly identified faults **not contained in the current public USGS database**.
- One scored submission per person per UTC day. One final submission per team.

## Focus sites and reported results

The nine focus sites are GEMSDOE24, GEMSDOE25, GEMSDOE27, GEMSDOE28, GEMSDOE30, GEMSDOE31,
GEMSDOE32, GEMSDOE33, GEMSDOE36. Their best reported files and scores (USER-REPORTED, not
organizer-confirmed) are:

| Site | Best reported file | Reported score |
|---|---|---:|
| GEMSDOE24 | h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan | 0.2477 |
| GEMSDOE25 | dotted-h19-5-d2-8-20261002-e56ea318af89-nan | 0.2600 |
| GEMSDOE27 | topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan | 0.2449 |
| GEMSDOE28 | h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan | 0.2710 |
| GEMSDOE30 | d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca | 0.2600 |
| GEMSDOE31 | h27-4-solo-d28-20261004-8acb75e1-nan | 0.2708 |
| GEMSDOE32 | h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros | 0.2778 |
| GEMSDOE33 | h33d-analog-tip-stepover-r30-20261004-cb490425926e | 0.2632 |
| GEMSDOE36 | anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros | 0.2750 |

The user also cites a current competition high score of 0.4413 and, elsewhere, 0.3195. A
public leaderboard snapshot from 31 Oct 2026 showed #1 = 0.4544, #50 = 0.3195, and 0.4413
absent from the top 50. Treat all of these as time-sensitive, user-reported or
organizer-public values, not as receipts for any file in this repo.

## Why GEMSDOE32 scored 0.2778

GEMSDOE32's file is a strict subset of GEMSDOE25: 44,090 dots become 37,654 after removing
6,436 dots that are 1–2 px from the mapped catalogue. Under the official metric, removing a
dot that earns no credit reduces FP and raises DTI; adding a dot helps only if its expected
credit exceeds 0.2·DTI. The test set is new faults not in the catalogue, so catalogue-adjacent
dots are likely false positives. That is the mechanism behind the reported +0.0178 gain.
**But the file is not unique:** it is 100% within 3 px of GEMSDOE25, and the nine focus-site
files are 97.6–100% contained in one another.

## What we built in this session

- A fresh block-inversion TIF: `docs/downloads/korea7-blockinv-b4-n12000-k106922-20261104T200956Z.tif`.
  - 106,922 dots, one per 400 m block, descending expected-credit order.
  - Estimate 0.386 (LOO sd 0.066) from a 10-raster ridge inversion with N ≤ 12,512.
  - Worst 3 px overlap vs the nine focus sites: 39.8% (limit 70%).
  - All format, range, null-encoding, grid, ZIP, and uniqueness gates pass.
  - SHA-256: `39eb9e1d7961ce2befb87d6fea841933f820b470abd274de73639184a196be43`.
- A validated fallback: `docs/downloads/korea7-blockinv3-123899-20261031T062457Z-nullmask.tif`.
  - 123,899 dots, estimate 0.3138 (LOO sd 0.021), worst 3 px overlap 34.7%.
  - SHA-256: `f9f219371ef7e3e4239cbf7ce895e72797801a8ac49342c71240cceb497e22be`.
- A public site: `docs/index.html` and `docs/executive-summary.html` with the download button
  at the top, the nine-site table, the validation gates, the run card, and the submission steps.

## Parallel-run protocol (binding)

1. **Lane.** Stay inside the assigned method paragraph. If the raster's rank correlation with
   any registry raster exceeds 0.90, or more than 70% of its dots fall within 3 px of one
   registry raster's dots, log it as a duplicate and stop. Check this before placement and on
   the final dots.
2. **Reuse, don't rebuild.** Use the template's cached feature stack, `evaluate_holdout.py`,
   and `submission_writer.py`. Holdout = hide-and-recover: withhold whole fault segments with
   a buffer, derive every catalogue-based feature only from the visible faults, mask visible
   faults pixel-exactly, score pooled DTI (α=0.2, β=0.8, 300 m triangular kernel). If a shared
   tool is wrong, fix it once in the template and report it; never keep a private fork.
3. **Label every number** as HOLDOUT-DTI (evaluator version, number of withheld positives,
   95% CI) or ORGANIZER-CONFIRMED (copied from a submission-page receipt). A projection is
   never written as a score.
4. **Leakage canary.** Test each feature alone on the holdout before trusting any result.
   AUC above 0.90 means leakage until proven otherwise.
5. **Run card.** End with one JSON card: hypothesis; mechanism; the named non-fault process
   that could mimic it; holdout DTI + CI; correlation/overlap vs registry; raster SHA-256;
   validator output (no NaN inside the footprint, values in [0,1], CRS/shape/transform match);
   submission name + note of at most 140 characters; verdict promote / negative. Negative
   results are deliverables.
6. **Budget.** Stop after 3 experiments or 2 hours. Do not pick submissions: promotion to a
   real slot is a separate selector step, within the weekly cap shown on the submission page.

## Core values

- **Maximize P(Win).** Weigh tradeoffs, assess risk, and choose the path that maximizes the
  probability of a real, unique, validated win.
- **Own the Outcome.** Own results end to end. Report negatives, blocked gates, and
  irregularities plainly. Do not wait for permission when we have the means to act.

## Evidence rules

- Do not copy or republish another entrant's prediction raster. Novelty claims require actual
  raster comparisons and SHA-256 records.
- Do not call an estimate an organizer score. Do not call a user-reported number
  organizer-confirmed without a receipt.
- Do not recommend submission if any gate is unknown.
- Use official verified sources for every factual claim. Provide links for manual review.
- No hallucinations. Verify line by line.

## Site requirements

- Clean, user-friendly, simple, easy to use, organized.
- The download button for the submission TIF must be at the very beginning, obvious.
- Include the executive summary table: file to download, estimate score, unique vs the other
  sites.
- Explain exactly how to make a submission into the contest.
- Include official verified links as sources for review.
- The site is static; it is not a live feed. Do not claim a live score without a receipt.

## Data placement

The competition's `training_features.tif`, `labels.tif`, `sample_submission.tif`, and
`1m_DEM_links.csv` are behind DrivenData login. The repo uses a sample-submission grid and a
labels raster recovered from a public mirror. The full feature stack is not present. To train
a model, run `bash scripts/download_competition_data.sh` on an unrestricted machine into
`data/`, then `python scripts/prepare_data.py`. After that the train→inference→validate
pipeline is ready to run (GPU needed for training; metric/losses/validation verified on CPU).

## Final deliverable

- A unique TIF that passes all format and uniqueness gates.
- An executive summary that makes the download decision obvious.
- A pull request merged onto `main`.
- A list of next steps and limitations for the next session.
