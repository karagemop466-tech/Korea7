# Korea7 — GEMS fault-prospectivity submission audit

> **Current dashboard (updated 2026-11-08):** The active bathtub overflow trip-lever decision workspace is published at the [site root](index.html), live at <https://karagemop466-tech.github.io/Korea7/>, with 13 canonical pages, a [Source ledger](sources.html), [Verification](verification.html), [Repo review](repo-review.html), [line inventory](data/canonical/repo_line_inventory.json) and a clearly labeled [Flagged for Review](flagged.html) page. Every canonical table row carries role-labeled source links; unverified values are blank and flagged. A source link is not proof of an unrelated claim. Earlier dashboards under `docs/`, `bathtub-overflow/` and `sf-overflow-audit/` are preserved as historical records. The GEMS audit content below is unrelated legacy work and is not certified by this repair dashboard.

> **Session starting point:** read this README and [the standing prompt](docs/prompt.md) before each project session. The objective, evidence rules, experiment limits, and submission requirements are in force. This repository contains the measured audit, the shared evaluator/writer, the candidate GeoTIFF, the validation artifacts, and the static GitHub Pages site.

## Core values

**Maximize P(Win).** In every decision, weigh tradeoffs, assess risk, and choose the path that maximizes the probability of winning. Set aside emotions and make tough decisions.

**Own the Outcome.** Own results end to end. When problems arise and we have the means to act, do so without waiting for permission. Treat failure and success as signals and use them to improve.

## Objective and non-negotiable evidence rules

Build an auditable workflow for predicting unmapped faults relevant to geothermal exploration for the DOE GEMS competition. Improve the chance of a strong leaderboard result without claiming a score that has not been measured. Generated competition predictions must be a single-band GeoTIFF matching the organizer's CRS, dimensions, and affine transform, with valid finite predictions in `[0, 1]` over the submission footprint. Make a downloadable file and its exact validation status obvious; never call an unvalidated file ready to submit.

- Distinguish **HOLDOUT-DTI** (evaluator version, withheld-positive count, and 95% confidence interval) from **ORGANIZER-CONFIRMED** (a score copied from a submission receipt). A model projection is not a score.
- Do not copy or republish another entrant's prediction raster. Novelty claims require actual raster comparisons and SHA-256 records. Check registry-raster rank correlation and dot overlap before and after candidate placement; the lane limits stated in the project brief are correlation `<= 0.90` and no more than `70%` of dots within 3 pixels of one registry raster. Report a violation as duplicate/drift and stop.
- Use the shared template's cached feature stack, holdout evaluator, and submission writer where they exist. Hold out whole fault segments with a buffer, derive catalogue-dependent features from visible faults only, mask visible faults pixel-exactly, and evaluate pooled DTI with alpha `0.2`, beta `0.8`, and a 300 m triangular kernel. Test each feature alone; AUC above `0.90` is a leakage alarm until explained.
- Experiment ceiling: at most 3 experiments or 2 hours, whichever comes first. Do not spend a weekly competition submission slot as part of model selection. A negative result is a valid deliverable.
- Final run card must include hypothesis, mechanism, plausible non-fault mimic, holdout DTI + CI, registry correlation/overlap, raster SHA-256, validator results (finite footprint, `[0,1]`, CRS/shape/transform), submission name and <=140-character note, and `promote` or `negative` verdict.

## Current status (2026-11-04)

**The candidate is a research artifact. It is NOT cleared for a weekly submission slot.**

| Item | Value |
|---|---|
| Candidate file | `docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif` |
| ZIP | `docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.zip` |
| SHA-256 | `9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c` |
| ZIP SHA-256 | `7460b2dd99ba2cd44d412b3d021fa1c30fb0a25b071b6e5f66a0c661a0d2a6a5` |
| Bytes | 102,331 |
| Dots | 20,000 |
| Far >15 px from catalogue | 0.857 |
| Near <=2 px from catalogue | 0.000 |
| Median catalogue distance | 34.1 px |
| PROJECTED leaderboard value | **0.3382** (95% bootstrap 0.3277–0.3525) — **not a score** |
| HOLDOUT-DTI | **0.0000** (95% CI 0.0000–0.0000) — below random control 0.0320 |
| Unique vs nine focus sites | **YES — 0% forward 3-px overlap** |
| 13GEMS covering-lattice probe | **99.96% forward 3-px overlap — literal rule fails** |
| Format validator | **PASS** (all checks; single band, float32, EPSG:32611, 3730×3292, transform matches, no NaN, values [0,1], zero dots on catalogue) |
| ZIP check | **PASS** (one TIF, identical bytes) |
| Submission name | `korea7-consensus-offcat-20k-20261104-zeros` |
| Note (117 chars) | `Korea7 4-method off-catalogue consensus, 20k dots, 85% far from catalogue; unique vs nine focus sites; research only.` |
| Verdict | **negative** — research artifact, not cleared |

**Download: OK. Submit: NOT CLEARED.** The file passes the format gate and the nine-focus uniqueness gate, but fails the catalogue hide-and-recover holdout gate (0.0000 below random) and the literal 13GEMS covering-lattice probe. No organizer receipt exists. Do not spend a weekly slot without an owner decision.

## Parallel lane KOREA7-E3 (merged 2026-11-04, PR #19) — OK TO DOWNLOAD, promote-to-selector

A second lane in this repo generated **KOREA7-E3** (`docs/downloads/gemsdoe32-korea7-scarprad-b2cov-r100-20261104T201931Z-7dcabf26-zeros.tif`, SHA-256 `f013b9c451a38730bb2527d7d096b98d9447b67df9af45902fc998a2ec7bb40d`, 37,654 dots): lidar scarp × radiometric-ratio-edge concordance, greedy 300 m-kernel coverage, >2 px catalogue gate, ≥100 m road-mimic control. **HOLDOUT-DTI 0.0963 [0.0799, 0.1113]** on `GEMSDOE32-SGMC-CAL-v3.0` (62,703 withheld proxy positives; all nine winners reproduced on the same instrument, best 0.0644) — disjoint-CI above the holdout best; canary max AUC 0.599; unique vs all nine focus winners (ρ ≤ 0.036, ≤27.3% within 3 px) and vs the consensus/SDCC1/relay lanes above (≤44.5%); strict all-pixel [0,1] format pass on saved bytes. Full evidence, per-site summaries, risk box (SGMC proxy-transfer and live-analog cautions; nine-point projection 0.4268 recorded and rejected), and step-by-step submission guide: [docs/executive-korea7-e3.html](docs/executive-korea7-e3.html), [docs/submission-korea7-e3.html](docs/submission-korea7-e3.html), run card [run-card-korea7-e3.json](run-card-korea7-e3.json). Instruments differ between lanes (hub lane above: gems57 hide-recover; E3 primary: SGMC-CAL) — neither is an organizer score. Slot decision remains the owner's separate selector step.

## Executive summary — nine focus sites

All geometry and HOLDOUT-DTI values are measured from the pinned rasters. Scores are USER-REPORTED (no organizer receipt). The nine focus-site rasters are one dotted-ridge family: every pair has forward 3-px overlap > 0.70. They are not nine independent submissions.

| Site | Highest file on that site | Dots | Far >15 px | USER-REPORTED score | HOLDOUT-DTI (95% CI) | Unique vs other focus? |
|---|---|---:|---:|---:|---:|---|
| GEMSDOE24 | `h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan` | 60,069 | 0.496 | 0.2477 | 0.0975 [0.0870, 0.1077] | NO — duplicate |
| GEMSDOE25 | `dotted-h19-5-d2-8-20261002-e56ea318af89-nan` | 44,090 | 0.499 | 0.2600 | 0.1023 [0.0909, 0.1133] | NO — duplicate |
| GEMSDOE27 | `topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan` | 61,328 | 0.486 | 0.2449 | 0.0972 [0.0867, 0.1073] | NO — duplicate |
| GEMSDOE28 | `h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan` | 37,660 | 0.549 | 0.2710 | 0.0315 [0.0282, 0.0347] | NO — duplicate |
| GEMSDOE30 | `d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca` | 44,090 | 0.499 | 0.2600 | 0.1023 [0.0909, 0.1133] | NO — duplicate |
| GEMSDOE31 | `h27-4-solo-d28-20261004-8acb75e1-nan` | 40,199 | 0.547 | 0.2708 | 0.0327 [0.0296, 0.0359] | NO — duplicate |
| GEMSDOE32 | `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` | 37,654 | 0.584 | **0.2778** | 0.0047 [0.0043, 0.0052] | NO — duplicate |
| GEMSDOE33 | `h33d-analog-tip-stepover-r30-20261004-cb490425926e` | 41,865 | 0.529 | 0.2632 | 0.0553 [0.0504, 0.0602] | NO — duplicate |
| GEMSDOE36 | `anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros` | 38,854 | 0.581 | 0.2750 | 0.0049 [0.0045, 0.0053] | NO — duplicate |

The highest USER-REPORTED score is GEMSDOE32 (0.2778). The highest measured HOLDOUT-DTI is GEMSDOE25/30 (0.1023). The highest far-catalogue fraction is GEMSDOE32 (0.584). None is unique against the others under the literal 70% rule.

## Candidate comparison

| File to download | Dots | Far >15 px | Estimate score | HOLDOUT-DTI | Unique vs nine focus? | 13GEMS lattice | Status |
|---|---:|---:|---:|---:|---|---|---|
| `korea7-consensus-offcat-20k-20261104-zeros.tif` | 20,000 | 0.857 | **0.3382 PROJECTED** | 0.0000 | **YES — 0% overlap** | 99.96% FAIL | **NOT CLEARED** |
| `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros.tif` (GEMSDOE32) | 37,654 | 0.584 | 0.2778 USER-REPORTED | 0.0047 | NO — duplicate | 99.92% FAIL | NOT A NEW SUBMISSION |
| `karage1-h31-visgrad-nms3px-40k-20261031-zeros.tif` (H-V31) | 40,000 | 0.008 | 0.1948 PROJECTED | 0.1143 | YES — max 38% | 99.75% FAIL | RESEARCH ONLY |

PROJECTED is an OLS extrapolation from nine USER-REPORTED scores; it is not a score. HOLDOUT-DTI is the shared gems57 hide-and-recover evaluator on the mirror catalogue; it is not a leaderboard estimate. The 13GEMS lattice is a covering-grid probe; the literal 70% rule is saturated and every dotted raster on this grid fails it.

## Why GEMSDOE32 (0.2778) led — and can we beat it?

The nine focus-site rasters are one dotted-ridge family. GEMSDOE32 is the most pruned member: 37,654 dots, 58.4% of them >15 px from the catalogue, and 0% within 2 px. That geometry is the best fit to the nine USER-REPORTED scores in the OLS projection (fitted B2 = 0.2769). The leaderboard reward appears to be driven by **precision away from the mapped catalogue**, not by recovering the catalogue. The organizer masks known faults, so dots near the catalogue are likely false positives. Pruning the halo raises precision. B2 is the most aggressive pruner in the family, and it has the highest USER-REPORTED score.

The consensus candidate pushes the far-catalogue fraction to 85.7% and reduces the dot count to 20,000, which is why its PROJECTED value is 0.3382. But the catalogue hide-and-recover holdout rewards the opposite: recovering withheld catalogue segments. The consensus candidate is off-catalogue by design, so its HOLDOUT-DTI is 0.0000, below the random control (0.0320). The holdout and the projection disagree by construction. Neither is an organizer score.

**Can we generate a higher score?** Possibly, but not demonstrated. The projection is above B2's 0.2769 and above the user's claimed 0.3195, but it is an OLS extrapolation from nine unverified scores and cannot see surface quality. The holdout is negative. No organizer receipt exists. The candidate is a research artifact, not a cleared submission.

## Method — density-weighted multi-method off-catalogue consensus

A new lane, not an exact copy of any prior submission.

1. **Four independent methods.** Off-catalogue geophysical edges (mag/gravity/topo/seismic), geothermal-conduit signatures (dilatation/curvature/conductivity/seismicity), habitat suitability, and a corridor prior. Each is converted to a 3-px local-density surface.
2. **Density-weighted consensus.** The densities are weighted by each method's measured far-catalogue fraction and summed. The consensus concentrates where independent methods agree, not where a single method fires.
3. **Hard off-catalogue mask.** The surface is masked to cells >5 px from the mapped catalogue and outside the closed 3-px halo of every focus-site raster. The candidate therefore has 0% forward 3-px overlap with all nine focus sites by construction.
4. **Greedy 3-px NMS.** The top 20,000 cells are selected with a 3-px minimum separation (300 m), matching the metric's triangular kernel.
5. **Shared writer + validator.** The candidate is written with the shared `gems57.submission_writer`, which validates the on-disk TIFF and a one-TIFF ZIP before committing. The validator checks CRS, shape, transform, dtype, range, NaN/inf, footprint, and catalogue.

## Candidate geological hypotheses (ranked)

| Rank | Hypothesis | Layers / signature | Why it catches missing faults | How it differs | Expected improvement / cost | Validation |
|---:|---|---|---|---|---|---|
| 1 | Multi-method off-catalogue consensus | Magnetic, gravity, radiometric, seismic, topographic, conductivity; coincident edges/lows/alteration | Targets blind geothermal structures outside the catalogue | Combines four independent off-catalogue methods with a density-weighted consensus and masks the nine focus halos | High / low | Implemented: holdout negative, projection positive |
| 2 | Catalogue-avoiding conductance-aware pruning | GDR wellsprings, volcanic vents, geodawn radiometry; conductance/alteration halos | Targets geothermal fluid pathways not in the catalogue | Uses a conductance prior, not just geophysical edges | Medium / medium | Not implemented — needs GDR data |
| 3 | Deep-learning off-catalogue segmentation | 19-band training features; multi-scale fault edges | Learns the fault signature from visible catalogue segments and applies it off-catalogue | Uses a U-Net instead of a LightGBM/consensus | High / high | Not implemented — needs GPU and training features |
| 4 | Drainage/valley deflection at structural intersections | 1 m DEM; channel curvature/knickpoints | Targets active young structures absent from the catalogue | Uses DEM hydrology, not geophysics | Medium / high | Not implemented — needs DEM |
| 5 | Seismicity-density off-catalogue corridors | Earthquake catalog; small-magnitude seismicity | Targets active faulting | Uses seismicity, not just geophysical edges | Medium / medium | Not implemented — needs seismicity data |

The specific free official sources needed for the unimplemented hypotheses:
- GDR wellsprings/volcanic vents: `https://gdr.openei.org/` (not accessible from this sandbox; the prior session cached a derived CSV, but it is not in this repo).
- 1 m DEM: USGS 3DEP / `https://www.usgs.gov/3d-elevation-program` (not accessible from this sandbox; the prior session's `1m_DEM_links.csv` is not in this repo).
- Seismicity: USGS earthquake catalog / `https://earthquake.usgs.gov/earthquakes/search/` (not accessible from this sandbox).
- 19-band training features: DrivenData competition data (login-walled; not accessible from this sandbox).

## Validation and limitations

**Format gate: PASS.** The validator re-reads the on-disk TIFF and the ZIP. It checks CRS, shape, transform, dtype, range, NaN/inf, footprint, catalogue, and the ZIP member. The candidate is single-band float32, EPSG:32611, 3730×3292, transform matches the sample, no NaN/inf, values in [0,1], zero dots on the catalogue, and the ZIP contains exactly one TIF with identical bytes.

**Nine-focus uniqueness gate: PASS.** The candidate has 0% forward 3-px overlap with every focus-site raster by construction. The surface Spearman correlations are all below 0.01 in absolute value.

**Holdout gate: FAIL.** The candidate's HOLDOUT-DTI is 0.0000 (95% CI 0.0000–0.0000), below the random control 0.0320 (95% CI 0.0296–0.0346). The holdout truth is the mirror catalogue; the candidate is off-catalogue by design. This is a negative result under the holdout gate, not a leaderboard estimate.

**13GEMS lattice gate: FAIL.** The candidate has 99.96% forward 3-px overlap with the 13GEMS covering lattice. The literal 70% rule is saturated: every dotted raster on this grid fails it. This is flagged for an owner decision, not waived silently.

**No organizer receipt.** Every leaderboard score on this site is USER-REPORTED from your supplied list. We have no organizer receipt for any of them. The 0.2778, 0.2750, 0.2708, 0.2710, 0.2632, 0.2600, 0.2477 and 0.2449 values are unverified reports.

**Conflicting leaderboard claims.** Your prompt cites 0.3195 and 0.4413 as the current high score. A prior session's 2026-10-31 fetch recorded #1 0.4544, #2 0.3934, #3 0.3917, with 0.3195 at rank #50. We cannot reach DrivenData from this sandbox, so we do not endorse either figure.

**The projection is an extrapolation.** The OLS fit uses nine unverified scores and two geometric covariates. It cannot see surface quality. At 20,000 dots the candidate is outside the observed dot-count range, so the projection is an extrapolation. Treat 0.24–0.36 as the defensible working range, not a promise.

**Data are a SHA-pinned mirror.** The competition data are restored from a third-party GitHub mirror, not an organizer-authenticated download. The hashes match the prior restore receipt, but the mirror is not the organizer. The DrivenData data tab is login-walled from this sandbox.

## Next steps

1. Obtain organizer-authenticated competition data and a submission receipt. The DrivenData data tab is login-walled from this sandbox.
2. Resolve the 13GEMS lattice rule with the owner. The literal 70% rule is saturated and cannot separate a copy from a legitimate candidate.
3. Decide whether the off-catalogue projection or the catalogue hide-and-recover holdout governs promotion. The two instruments disagree by construction.
4. Restore the 19-band training features and train a proper off-catalogue model (e.g., a U-Net or LightGBM) to improve surface quality. The current consensus uses the prior reference rasters, not a fresh model.
5. Obtain the GDR wellspring/volcanic vent data and the 1 m DEM to test the conductance and drainage hypotheses.
6. Verify the live leaderboard figures from an unrestricted machine.
7. Improve the site and add more tests/CI. The current site is a static GitHub Pages site with a clean UI, a prominent download button, and a clear status badge.
8. Consider a hedging strategy that combines the off-catalogue consensus with a small number of catalogue-adjacent dots, if the organizer's masking allows. This could improve the holdout and projection simultaneously, but it would need a new experiment and a new run card.

## Bathtub overflow trip lever project (San Francisco) — archived dashboard from an earlier session

Earlier-session dashboard; the current canonical site is [index.html](index.html).

A separate project housed in this repo: a contractor research dashboard for a stuck bathtub wastewater overflow trip lever in a hard-to-access, tenant-occupied unit. Existing GEMS audit content above is unaffected.

**Live site:** https://karagemop466-tech.github.io/Korea7/ — the site root is the current dashboard.

| Item | Link |
|---|---|
| Dashboard (landing page) | [index.html](index.html) |
| Executive summary | [summary.html](summary.html) · [EXECUTIVE-SUMMARY.md](EXECUTIVE-SUMMARY.md) |
| **Shortlist — who can do plumbing + drywall** | [shortlist.html](shortlist.html) |
| Estimates (owner-supplied 2026-08-30; unverified: $614 / $550 / $135) | [estimates.html](estimates.html) |
| Nine contractor candidates + CSLB verification status | [contractors.html](contractors.html) |
| Findings and analysis | [findings.html](findings.html) |
| **Verification log + correction log** | [verification.html](verification.html) |
| All sources | [sources.html](sources.html) |
| Flagged unverified items and irregularities (10) | [flagged.html](flagged.html) |

Earlier research sets from parallel sessions remain published and linked for cross-checking:
`bathtub-overflow/` and `docs/plumbing-index.html` + `docs/overflow-*.html`.

No contractor has been hired or contacted. All prices are owner-supplied estimates dated 2026-08-30 and are unverified. Licence facts come only from the official CSLB records; permit content only from official San Francisco sources.

## Repository structure

```
Korea7/
  README.md
  docs/prompt.md
  data/
    labels.tif
    sample_submission.tif
    bridge/
      existing_faults.tif
      sample_submission.tif
    focus/                 nine focus-site TIFs
    registry/              13GEMSDOE_lattice.tif
    reference/             six reference candidate TIFs
  vendor/gems57/           shared evaluator/writer, provenance-verified
  scripts/
    analyze_focus.py
    analyze_sites.py
    build_consensus.py
    build_site.py
    prepare_data.py
  docs/
    index.html
    executive-summary.html
    how-to-submit.html
    validation.html
    sources.html
    site-GEMSDOE*.html
    downloads/             candidate TIF, ZIP, receipt
    data/                  JSON artifacts
    assets/                CSS, JS
  tests/
    test_project.py
    test_evaluate_holdout.py
  conftest.py
```

## Reproduce

```bash
python3 scripts/analyze_focus.py
python3 scripts/analyze_sites.py
python3 scripts/build_consensus.py
python3 scripts/build_site.py
pytest -q
```

The scripts read the pinned rasters in `data/` and the shared `vendor/gems57` evaluator/writer. They do not call the DrivenData portal and do not spend a submission slot.

## Run card

The full JSON run card is in [`docs/data/consensus_run_card.json`](docs/data/consensus_run_card.json). The site displays it on the [validation page](docs/validation.html) and the [executive summary](docs/executive-summary.html).

## Parallel session (same brief, different lane)

A parallel session committed a separate research pipeline and candidate rasters to this repository. Its own README states that its candidate rasters fail the format gate on a geotransform mismatch (origin 250000, 4520000 vs the official sample_submission origin 243350, 4508550). We keep its work for completeness and flag the conflict. It is not a cleared submission.

- Parallel README: [docs/parallel-readme.md](docs/parallel-readme.md)
- Parallel index: [docs/parallel-index.html](docs/parallel-index.html)
- Parallel executive summary: [docs/parallel-executive-summary.html](docs/parallel-executive-summary.html)
- Parallel method: [docs/method.html](docs/method.html)
- Parallel verification: [docs/verification.html](docs/verification.html)
- Parallel research log: [docs/research.md](docs/research.md)

The parallel session's candidate rasters are `korea7-k7-offcatalogue-relay-corridor-30000dots-...`, `korea7-sdcc1-scarpdom-conc-uniq65-37654-...`, and `korea7-sdcc1-scarpdom-conc-uniq65-44090-...`. Its own README says they fail the format gate on the transform mismatch. Do not upload them.

## Sources for manual review

- DrivenData competition overview: <https://www.drivendata.org/competitions/306/competition-doe-gems/>
- Competition problem description: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/>
- Competition about page: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/>
- Competition data page (login may be required): <https://www.drivendata.org/competitions/306/competition-doe-gems/data/>
- Leaderboard (dynamic; verify current date and score): <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
- DrivenData reference solution: <https://github.com/drivendataorg/gems-prize-reference-solution>
- DOE/NLR GEMS solicitation PDF: <https://docs.nlr.gov/docs/fy26osti/96647.pdf>
- USGS GeoDawn survey page: <https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and>
- GBC/INGENIOUS: <https://gbcge.org/current-projects/ingenious/>
- EPSG:32611: <https://epsg.io/32611>
- Tversky index background: <https://en.wikipedia.org/wiki/Tversky_index>
- User-supplied reported-results sites: [GEMSDOE24](https://buffedlizard55-lab.github.io/GEMSDOE24/), [GEMSDOE25](https://buffedlizard55-lab.github.io/GEMSDOE25/), [GEMSDOE27](https://buffedlizard55-lab.github.io/GEMSDOE27/), [GEMSDOE28](https://buffedlizard55-lab.github.io/GEMSDOE28/), [GEMSDOE30](https://buffedlizard55-lab.github.io/GEMSDOE30/), [GEMSDOE31](https://buffedlizard55-lab.github.io/GEMSDOE31/docs/), [GEMSDOE32](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html), [GEMSDOE33](https://buffedlizard55-lab.github.io/GEMSDOE33/), [GEMSDOE36](https://buffedlizard55-lab.github.io/GEMSDOE36/docs/).
- Prior project repos (data provenance and reference candidates): [GEMSDOEkarage1](https://github.com/karagemop466-tech/GEMSDOEkarage1), [GEMSDOEkarage2](https://github.com/karagemop466-tech/GEMSDOEkarage2), [GEMSDOEkarage3](https://github.com/karagemop466-tech/GEMSDOEkarage3).

## Pinned data hashes

| File | SHA-256 | Note |
|---|---|---|
| `data/labels.tif` | `7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093` | mirror catalogue, not organizer hidden labels |
| `data/sample_submission.tif` | `2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc` | grid/footprint template |
| `docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif` | `9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c` | candidate |
| `docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.zip` | `7460b2dd99ba2cd44d412b3d021fa1c30fb0a25b071b6e5f66a0c661a0d2a6a5` | candidate ZIP |

## Irregularities flagged for review

1. **The 13GEMS lattice rule is saturated.** The 13GEMS lattice is a covering-grid probe with 206,895 dots. Every dotted raster on this grid has >99% of its dots within 3 px of a lattice dot. The literal 70% rule cannot separate a copy from a legitimate candidate. This is an owner decision, not a silent waiver.
2. **The holdout and projection disagree by construction.** The holdout truth is the mirror catalogue; the organizer masks known faults and scores hidden new faults. A candidate that avoids the catalogue will score 0 on the holdout by construction. The holdout is a conservative catalogue-recovery instrument, not a leaderboard estimate.
3. **The nine focus-site rasters are duplicates.** Every pair has forward 3-px overlap >0.70. They are one dotted-ridge family, not nine independent submissions.
4. **The leaderboard figures conflict.** The prompt cites 0.3195 and 0.4413; a prior session's 2026-10-31 fetch recorded #1 0.4544, #2 0.3934, #3 0.3917, with 0.3195 at rank #50. We cannot reach DrivenData from this sandbox.
5. **The data are a SHA-pinned third-party mirror.** The hashes match the prior restore receipt, but the mirror is not the organizer. The DrivenData data tab is login-walled from this sandbox.
6. **The candidate is a research artifact.** It is not organizer-cleared. The holdout gate fails. The 13GEMS lattice probe fails. No weekly slot is spent.

## Current run card

`hypothesis`: blind geothermal faults missing from the USGS/INGENIOUS catalogue are co-detected by independent off-catalogue geophysical, geothermal-conduit, habitat-suitability and corridor-prior methods; a density-weighted consensus concentrates the highest-confidence off-catalogue structures while avoiding the mapped catalogue and the nine focus-site halos.

`mechanism`: each of four reference rasters is converted to a 3-px local-density surface; the densities are weighted by each method's measured far-catalogue fraction and summed. The surface is masked to >5 px from the catalogue and outside the closed 3-px halo of every focus-site raster, then the top 20,000 cells are selected by greedy 3-px NMS. The candidate is written with the shared `gems57.submission_writer` and validated on disk.

`named_non_fault_mimic`: pluvial shoreline berms, road/rail embankments, conductive playas, alluvial-fan toes and basin-margin gravity steps can produce linear conductivity/curvature/gravity anomalies in novel territory; the consensus requires agreement across independent methods, but does not prove a fault.

`HOLDOUT-DTI + CI`: 0.0000 [0.0000, 0.0000], evaluator `gems57-holdout-v1`, 45,260 withheld positives; random control 0.0320 [0.0296, 0.0346].

`registry correlation/overlap`: 0% forward 3-px overlap with all nine focus-site rasters; max |surface Spearman| < 0.01; 13GEMS lattice forward 3-px overlap 0.9996 (literal rule fails).

`raster SHA-256`: `9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c`.

`validator output`: all format checks pass; single band, float32, EPSG:32611, 3730×3292, transform matches sample, no NaN/inf, values [0,1], zero dots on catalogue; ZIP contains one TIF with identical bytes.

`submission name + note`: `korea7-consensus-offcat-20k-20261104-zeros`; `Korea7 4-method off-catalogue consensus, 20k dots, 85% far from catalogue; unique vs nine focus sites; research only.` (117 characters).

`verdict`: **negative** — research artifact, not cleared for a weekly slot.

---

## Active project (2026-11-06): Bathtub wastewater overflow trip lever — San Francisco — archived

This earlier-session microsite is archived; the current canonical site is [index.html](index.html).

A second work package lives in this repository: a verified research and hiring brief for a stuck
bathtub waste-and-overflow **trip lever** in a tenant-occupied San Francisco unit (access may require
opening the ceiling below). It does not touch the GEMS project above.

- Site (dashboard + subpages): [`docs/bath/index.html`](docs/bath/index.html) — published at
  `https://karagemop466-tech.github.io/Korea7/docs/bath/` once this branch merges to `main`.
- Executive summary: [`docs/bath/executive-summary.md`](docs/bath/executive-summary.md)
- Verified data (all rows source-linked): [`docs/bath/data/`](docs/bath/data)
- Flagged for Review: [`docs/bath/flagged-for-review.html`](docs/bath/flagged-for-review.html)
- Coordination: [`COORDINATION.md`](COORDINATION.md)
- Build &amp; verify: `python3 scripts/build_bath_site.py && python3 -m pytest tests/test_bath_site.py -q`
