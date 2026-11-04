# Korea7 — GEMS fault-prospectivity: unique validated submission + audit site

> **Session starting point:** Read this README (and the STANDING REFERENCE PROMPT at the bottom) before each project session. Keep the objective, evidence rules, and experiment limits below in force.

## Status (verified locally 2026-11-04, session 36cfbc6a)

**A unique, fully validated submission TIF now exists in this repository.**

| Artifact | Value |
|---|---|
| **Primary submission file** | [`docs/downloads/korea7-sdcc1-scarpdom-conc-uniq65-44090-20261104T201224Z-5631ba53-zeros.tif`](docs/downloads/korea7-sdcc1-scarpdom-conc-uniq65-44090-20261104T201224Z-5631ba53-zeros.tif) |
| SHA-256 | `5631ba539672f57187429b11867ba6a3d5c4ed8791001469b6f131534b09fd8c` |
| Format | single-band float32 GeoTIFF, EPSG:32611, 3730×3292, transform (100, 0, 243350, 0, −100, 4508550); **all pixels finite, all in [0, 1]** (zeros background) |
| HOLDOUT-DTI (SGMC-CAL v3.0, 62,703 withheld positives) | **0.062423**, 95% CI [0.0511, 0.0745] |
| HOLDOUT-DTI (HIDE-RECOVER v3.0, 22,232 withheld positives) | 0.004501 [0.0034, 0.0056] (low by construction — catalogue collar, same signature as the B2 champion's 0.004515) |
| Calibrated leaderboard projection (**not a score**) | 0.2672, range [0.2138, 0.3242] |
| Uniqueness (16 deduped registry rasters) | max 3-px dot overlap **39.6%** (limit 70%); max \|Spearman\| **0.012** (limit 0.90) → **PASS, in lane** |
| Leakage canary | all single-feature AUCs 0.48–0.58 (< 0.90) → clean |
| Experiments used | 3 of 3 (budget exhausted; stopped per protocol) |
| Verdict | **promote** (run card: [`run-card.json`](run-card.json)); slot use remains the owner's selector decision |
| Alternate (backup) | `…-37654-…-d88f4742-zeros.tif`, SGMC-CAL 0.0573 [0.0465, 0.0692], projection 0.2432 |
| Submission note (≤140 chars) | `Korea7 SDCC-1: scarp-dom concordance fusion (LiDAR scarp, TMI-up150 grad, ThK alt, wellspring), D2.8 Poisson, collar B2, uniq cap 65%` |

**Executive summary page (download + how-to-submit + focus-site table): [`docs/executive-summary.html`](docs/executive-summary.html).**

## Why GEMSDOE32 B2 scored 0.2778 (answered with measurements, not notes)

Byte-level forensics on the restored raster (37,654 binary dots, min NN spacing 2.83 px): B2 is the **h19-5 multiline-corroboration surface re-emitted** as a Poisson-disk D2.8 dot pattern with a 2-px catalogue collar. The 2.8-px spacing matches the 300 m triangular DTI kernel (α 0.2, β 0.8) so no two dots waste credit in one kernel disk; the collar reallocates ~15% of budget from known faults (worth nothing) to off-catalogue targets. Measured diagnostic: B2's hide-and-recover holdout is ~0 (0.0045) while its **off-catalogue SGMC-CAL holdout is the family's highest (0.0641)** — and across the nine focus rasters SGMC-CAL tracks owner-reported scores nearly linearly (LB ≈ −0.0271 + 4.715·SGMC-CAL, RMSE 0.0023). Goodhart warning: directly chasing SGMC faults scored 0.03–0.05 on the real board; the proxy only validates surfaces carrying real evidence. **Can we beat 0.2778?** Within this feature family only marginally; our unique candidate's projection CI [0.2138, 0.3242] straddles it. A decisive jump needs new physics (1 m DEM channel-deflection, learned fusion) — ranked queue in the executive summary.

## Focus-site table (all registry claims OWNER-REPORTED, holdouts measured here)

| Site | File | SGMC-CAL (HOLDOUT-DTI) | Reported LB | Unique? | Submit? |
|---|---|---:|---:|---|---|
| **Korea7** | `korea7-sdcc1-…-44090-…-5631ba53-zeros.tif` | **0.0624** | 0.2672 proj. | **YES** (39.6%) | **YES — primary** |
| Korea7 | `korea7-sdcc1-…-37654-…-d88f4742-zeros.tif` | 0.0573 | 0.2432 proj. | YES (40.6%) | backup |
| Korea7 (parallel lane) | `korea7-k7-offcatalogue-relay-corridor-30000dots-…` | not measured | unknown | YES (2.45%) | no — unmeasured |
| GEMSDOE32 | `h33-h33-2-b2-…-e5eb6e7e-zeros` | 0.0641 | 0.2778 | No (B2 family) | no — prior submission |
| GEMSDOE36 | `anderson-geothermal-pinn-38854-…-zeros` | 0.0644 | 0.2750 | No | no |
| GEMSDOE28 | `h36-1-rung30-blind-r1-…-nan` | 0.0630 | 0.2710 | No | no |
| GEMSDOE31 | `h27-4-solo-d28-…-nan` | 0.0630 | 0.2708 | No | no |
| GEMSDOE33 | `h33d-analog-tip-stepover-r30-…` | 0.0626 | 0.2632 | No | no |
| GEMSDOE25/30 | `dotted-h19-5-d2-8…` / `d28-poisson300m-offcat-44090…` | 0.0606 | 0.2600 | No (identical bytes) | no |
| GEMSDOE24 | `h25-1-dotted-h19-5-d1-5-…-nan` | 0.0579 | 0.2477 | No | no |
| GEMSDOE27 | `topo-gap-closure-t-v2-on-d1-5-…-nan` | 0.0583 | 0.2449 | No | no |

## Reproduction

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_submission.py --budget 44090   # restore → surface → place → write
.venv/bin/python scripts/validate_raster.py docs/downloads/<candidate>.tif <data>/sample_submission.tif
.venv/bin/pytest -q
```

- Holdout evaluation delegates to the **shared template** (no private fork): `GEMSDOEkarage3/scripts/evaluate_holdout.py` pinned at commit `6b0d7cd64b06c7b694eeae70032afc761f869171`. Toolchain reproduction check passed exactly: GEMSDOE25 hide-and-recover = `0.09674330401596999`.
- Data mirrors (SHA-256-pinned, mirrors of login-walled DrivenData files — integrity-pinned, NOT organizer-authentic): core from `sassnarep3-star/GEMSDOESASS2 data/bridge/` (`labels/existing_faults = 7ba308cc…`, `sample_submission = 2176d08e…`), externals from `kanlerxz87-cyber/KANLERGEMSDOE1 data/external/` (pins match `GEMSDOEkarage3 registry/data_manifest.json`), registry rasters from `karagemop466-tech/GEMSDOEkarage1 registry/` + `kanlerxz87-cyber/KANLERGEMSDOE1 data/scored/`.
- Evidence receipts: [`evidence/`](evidence/) (canary, placement, holdout JSONs, lane checks), [`run-card.json`](run-card.json).

## Non-negotiable evidence rules

- Label every number **HOLDOUT-DTI** (evaluator version, withheld-positive count, 95% CI) or **ORGANIZER-CONFIRMED** (submission receipt). A projection is never a score.
- Never copy/republish another entrant's raster as a submission; registry rasters are kept for learning and uniqueness checks only. Lane limits: raster rank-correlation ≤ 0.90, ≤ 70% of dots within 3 px of any one registry raster — checked on the surface before placement AND on final dots; violations are logged as duplicate and stop the run.
- Reuse the shared template's evaluator and writer; fix shared bugs upstream, never fork privately.
- Leakage canary before trusting any feature: alone-on-holdout AUC > 0.90 = leakage until proven otherwise.
- ≤ 3 experiments or 2 hours per session; negative results are deliverables; weekly submission slots are a separate selector decision.

## Irregularities flagged for review

1. **IR-K7-1:** `buffedlizard55-lab` (origin of all GEMSDOE site pages and the data bridge) is 404 on GitHub API and codeload (2026-11-04). All dependent URLs in prior notes are dead. Data restored from SHA-256-pinned mirrors instead; pins match the karage3 manifest exactly.
2. **IR-K7-2:** `training_features.tif` (419 MB, 19-band) is not restorable this session (bridge gone). Not needed for SDCC-1 or the evaluator; blocks training_features-based models until a new mirror or DrivenData login is available.
3. **IR-K7-3:** All focus-site scores remain OWNER-REPORTED (no organizer receipts); the brief's leaderboard highs (0.4413 vs 0.3195) conflict; drivendata.org is unreachable from this sandbox.
4. **IR-K7-4:** No method-paragraph lane was supplied with the parallel-run protocol; the SDCC-1 lane is self-declared and logged in the run card.

## Next work

1. **Submit** the primary TIF (owner action), paste back the organizer receipt, relabel ORGANIZER-CONFIRMED, and recalibrate the projection fit with a 10th point.
2. Implement hypothesis #1 (channel-deflection on 1 m 3DEP DEM) on an unrestricted machine; validate on the pinned holdout before any slot use.
3. Re-mirror `training_features.tif` from a logged-in DrivenData download to enable learned fusion (hypothesis #5) with strict OOF discipline.
4. Dedicated radiometric alteration-halo experiment (cheap; data already mirrored).
5. Keep the registry fresh: re-scan accessible sibling repos for new scored rasters before each uniqueness check.

## Sources for manual review

[Problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) · [About](https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/) · [Data](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) · [Leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) · [Reference solution](https://github.com/drivendataorg/gems-prize-reference-solution) · [GEMS prize PDF 96647](https://docs.nlr.gov/docs/fy26osti/96647.pdf) · [USGS GeoDAWN](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and) · [GDR 1391](https://gdr.openei.org/submissions/1391) · [INGENIOUS](https://gbcge.org/current-projects/ingenious/) · [EPSG:32611](https://epsg.io/32611) · [Tversky index](https://en.wikipedia.org/wiki/Tversky_index) · [3DEP 1 m lidar](https://registry.opendata.aws/usgs-lidar/)

---

## STANDING REFERENCE PROMPT (owner-supplied; read at the start of every session)

The owner's standing project brief. **Full verbatim text: [`docs/STANDING_PROMPT.md`](docs/STANDING_PROMPT.md)** (read it every session). Binding condensed obligations:

- Focus on the highest-scoring submissions from GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, 36. Produce an executive summary per site making it obvious which file is best to submit, with a table of: file to download, estimated score, and uniqueness vs the listed GEMSDOE sites.
- **HIGHEST URGENCY: generate a UNIQUE TIF submission. Never copy a previous submission except for learning. It must be obvious whether the generated TIF is OK to download and submit.** Inspection/validation must be done by the project without human intervention.
- Study why GEMSDOE32's `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` scored 0.2778 and whether it can be beaten (PhD-level analysis, then act on it). Current leaderboard highs quoted: 0.4413 and 0.3195 (conflicting — verify).
- PARALLEL-RUN PROTOCOL: stay in one method lane; duplicate limits 0.90 rank-correlation / 70% dots within 3 px (check surface pre-placement and final dots); reuse the template's cached feature stack, `evaluate_holdout.py`, `submission_writer.py` (hide-and-recover holdout, pooled DTI α 0.2 β 0.8, 300 m triangular kernel); label every number HOLDOUT-DTI or ORGANIZER-CONFIRMED; leakage canary (AUC > 0.90 alarm); end with one JSON run card (hypothesis, mechanism, non-fault mimic, holdout DTI + CI, correlation/overlap, SHA-256, validator output, name + ≤140-char note, promote/negative); stop after 3 experiments or 2 hours; promotion to a slot is a separate selector step.
- Before implementing: generate 3–5 new geological hypotheses (layers, physical signature, why it catches catalogue-missing faults, how it differs from this repo), rank by expected DTI gain and cost, validate the top one on the spatially-blocked holdout before spending any submission slot; name the specific free official source for any new external data and check obtainability first.
- Submission mechanics: single-band GeoTIFF (or zip with one GeoTIFF) matching the submission format's CRS/shape/geotransform; values must be in [0, 1] (a prior download failed the form with "Predicted values must be in range [0, 1]"); give each submission a unique name and a short distinguishing note. Create an executive-summary subpage explaining exactly how to submit; the download must be obvious at the top of the site.
- Work line by line from official verified trusted sources with links for manual review; no manual input; flag irregularities; no hallucinations; multi-pass (implement → review/fix → re-check). Store research knowledge for reuse. Core values: Maximize P(Win); Own the Outcome.
- Goal: top of the leaderboard of [DOE GEMS, DrivenData competition 306](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/). Known constraints: DrivenData data page is login-walled; this sandbox reaches only github.com/codeload/api.github.com, registry.npmjs.org, pypi.org, files.pythonhosted.org. Open a PR and merge it to main each session; list remaining work and limitations for the next session.
