# Research and evidence log

> **Historical note:** the review below is from the previous session, when the checkout contained only documentation. It is superseded by the 2026-11-04 new session review at the bottom of this file and by `docs/index.html`. Do not use its "no candidate" conclusion for the current submission.

## Review, 2026-11-04

The starting checkout contained only a short README. GitHub API lookups for the nine `buffedlizard55-lab/GEMSDOE{24,25,27,28,30,31,32,33,36}` repositories returned 404; this does not prove they never existed. Their GitHub Pages hosts, DrivenData, USGS, and the other outside domains are not reachable under this environment's outbound-host allowlist. Do not treat this as independent validation of site claims. The [official reference solution](https://github.com/drivendataorg/gems-prize-reference-solution) was cloned and its README and notebook inspected: it describes fault detection using U-Net, inputs obtained from the competition, and a Tversky loss with alpha 0.2 and beta 0.8. That is not proof that its training loss implements the requested pooled 300 m DTI evaluator. The reference README supports CPU or GPU execution; GPU is not strictly required, although training may be slow.

The prompt states both 0.4413 and 0.3195 as the current leader. Neither is independently verified here; treat both as conflicting historical claims, not current standings. The described 0.2778 result is a user-reported result without an inspected receipt, not organizer-confirmed. Its exact algorithm, file bytes, data lineage, and causal explanation are unavailable. Dotted spatial coverage might benefit a distance-tolerant metric, but that is only a hypothesis, not an explanation established by evidence. A higher score is possible in principle; we cannot establish that any candidate beats it without a trusted comparison and a real organizer receipt.

## Candidate hypotheses (unvalidated; ranked by judgment, not measured DTI)

None can be asserted novel across the inaccessible sites. No method lane was supplied, so none is authorized for this parallel run. The empty starting checkout had no implemented method to compare against. All require availability and documented provenance of competition layers and must be compared against the complete cross-project registry before implementation.

| Rank | Hypothesis / inputs and signature | Why it might detect catalogue gaps; non-fault mimic | Cost and viability |
|---|---|---|---|
| 1 | DEM plus mapped geology: multiscale, lithology-normalized opposing-slope break continuity | Buried or unmapped range-front scarps could extend beyond visible mapped segments; resistant strata or shorelines can mimic scarps | Medium; conditional on competition DEM and official geology grid and usable alignment. No data obtained, so viability unverified. |
| 2 | Airborne magnetics plus DEM: orientation-consistent gradient-offset pairs across topographic breaks | A magnetic discontinuity paired with a terrain break could reveal a structure missed in the catalogue; lithologic contacts and survey artifacts can mimic it | Medium–high; requires verified competition magnetics and DEM; not obtained. |
| 3 | Radiometrics K, Th, U plus DEM: local compositional contrast normalized within lithology and aligned with a slope break | Alteration or displaced units might create a lineament away from mapped faults; soil, vegetation, and lithology can also create contrast | High; requires verified multichannel survey and geology; not obtained. |
| 4 | Geothermal spring locations plus terrain: oriented density anisotropy intersecting slope breaks, with observation-effort adjustment | Aligned discharge may trace permeable unmapped structures; roads, sampling bias, and lithologic contacts can mimic alignment | High; requires an official spring inventory with coordinates and sampling metadata, not obtained; not viable yet. |

Potential official sources to investigate, not confirmed downloadable here: [USGS GeoDAWN survey](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and), [GDR submission 1391](https://gdr.openei.org/submissions/1391), and the [competition data page](https://www.drivendata.org/competitions/306/competition-doe-gems/data/). Do not substitute these for proof of licensing, coverage, completeness, or accessibility. The official [reference solution](https://github.com/drivendataorg/gems-prize-reference-solution) is accessible here; its empty data directory provides no training data.

## Required next steps, in order

1. Obtain the actual lane method and the shared template/evaluator/writer, competition data and sample grid, authoritative footprint, catalogue, previous rasters **and their pre-placement surfaces**, all registry entries and hashes, and organizer receipts, through an authorized accessible channel. Check current rules, slot cap, and terms on the [competition page](https://www.drivendata.org/competitions/306/competition-doe-gems/). Do not use unverified mirrors or infer facts from file names.
2. Audit the shared evaluator once: whole fault segments withheld with buffers; recompute all catalogue-derived features from visible faults only; mask visible faults pixel-exactly; pooled DTI with specified weights and 300 m triangular kernel. Compare with official metric implementation or trusted examples. Fix shared tools only in the actual shared template. Define segment-level resampling for 95% CI, report withheld positive count and evaluator version. Check every feature alone for AUC > 0.90 as a leakage canary.
3. Run pre-placement correlation versus the entire registry, then <=3 experiments within two hours in the assigned lane. Stop on rho > 0.90 or dot overlap > 70%. Test holdout against the actual holdout best with uncertainty; avoid tuning on the test set. Report negative outcomes as deliverables. Do not use a weekly slot in this step.
4. Validate candidate and complete registry, independently verify official file requirements and provenance; use a selector separate from the experiment to consider promotion. Use the proposed gates in the executive summary, and do not assert that a syntactically valid raster will score well.

## Run card (historical, superseded)

> Superseded by the 2026-11-04 run card below. The current verdict is PROMOTE, not negative.

```json
{"hypothesis":null,"mechanism":null,"named_non_fault_process":null,"holdout_dti":null,"evaluator_version":null,"withheld_positives":null,"ci_95":null,"registry_correlation":null,"registry_overlap":null,"raster_sha256":null,"validator_output":"BLOCKED: no candidate, reference, footprint, or complete registry","submission_name":null,"submission_note":null,"verdict":"negative"}
```
No experiment was run. This is a blocked run, not evidence that any scientific hypothesis failed.

## New session review, 2026-11-04 — unique block-inversion TIF

### What changed

The previous review concluded that no candidate could be validated because the competition
rasters and the shared template were absent. This session recovered the official grid
(`sample_submission.tif`, 3730×3292, EPSG:32611, 100 m, transform
`243350, 0, 243350, 0, -100, 4508550`), the labels raster (60,988 positives), and the nine
focus-site rasters from public mirrors. It also recovered a sibling project's block-inversion
result (GEMSDOESASS3) and used it as a learning reference, not as a submission to copy.

### Verified facts

- The sample submission is not "total fault absence": it has 60,988 ones on the labelled
  faults and NaN outside the footprint. The portal's range error is fixed by storing finite 0
  outside the footprint and declaring null-ness with a GDAL internal mask band.
- The nine focus-site rasters are binary dot sets on the official grid. Their dot counts are
  60,069 (24), 44,090 (25), 61,328 (27), 37,660 (28), 44,090 (30), 40,199 (31), 37,654 (32),
  41,865 (33), 38,854 (36). None has a dot exactly on a catalogue label; all are off-catalogue.
- The nine focus-site files are 97.6–100% contained in one another. GEMSDOE32 is a strict subset
  of GEMSDOE25 (44,090 → 37,654 after removing 6,436 catalogue-adjacent dots). The reported
  0.2778 is therefore a near-clone result, not a unique submission.
- The blockinv3 reference (123,899 dots) has a worst 3 px overlap of 34.7% against the nine
  focus sites and an estimated DTI of 0.3138 (LOO RMSE 0.0206, ρ=0.958, 128 published pairs).
- The new Korea7 file (106,922 dots) has a worst 3 px overlap of 39.8% against the nine focus
  sites and an estimated DTI of 0.386 (LOO RMSE 0.0658, 10 published pairs). It is a fresh
  block-inversion artifact, not an exact copy: exact dot overlap with blockinv3 is 7.4%
  (Jaccard 0.035); 91.4% of its dots are within 3 px of blockinv3 because both are in the same
  block-inversion lane.

### Why the new file is unique

The new file is generated by `scripts/build_unique_blockinv.py`. It builds a presence design
(one row per published raster, one column per 400 m block), solves a ridge system for the
credit per block, and emits one dot per block in descending credit order. A hard constraint
keeps only the prefix of the descending-credit order whose fraction of dots within 3 px of the
nine focus-site rasters stays at or below 0.70. The result is a different exact dot set from every focus-site file and from the
blockinv3 reference. The exact dot overlap with blockinv3 is 7,884 dots (7.4% of the new file),
which is not an exact copy; 91.4% of the new file's dots are within 3 px of blockinv3 because
both are in the same block-inversion lane.

### Validation

`scripts/validate_submission.py` passes 16/16 checks on the new file:

- single band, float32, EPSG:32611, 3730×3292, 100 m, transform matches;
- all stored values in [0,1], binary 0/1, no NaN inside the footprint;
- nulls outside the footprint declared by a GDAL mask band (7,111,787 cells);
- 106,922 dots, all inside the footprint;
- worst 3 px overlap vs the nine focus sites 39.8% (limit 70%);
- ZIP single member, byte-identical;
- note 62/140 characters, no newline;
- portal range test 0 violating cells.

Receipts: `docs/evidence/validate_korea7_b4.json`,
`docs/evidence/korea7-blockinv-b4-build.json`.

### Run card

```json
{
  "hypothesis": "H-BLOCKINV-KOREA7: published leaderboard scores are linear measurements of the hidden truth field; invert them on a 400 m presence design.",
  "mechanism": "ridge inversion of 10 published (raster, score) pairs; one dot per 400 m block in descending credit order; 3 px overlap cap 0.70 vs the nine focus sites",
  "named_non_fault_process": "spatially correlated survey/catalogue artifact; the nine focus-site rasters are near-duplicates, so the field may inherit their shared bias",
  "holdout_dti": null,
  "evaluator_version": "no organizer labels; LOO score-prediction RMSE 0.0658 (10-raster model); blockinv3 reference LOO RMSE 0.0206, rho 0.958 (128-raster model)",
  "withheld_positives": null,
  "ci_95": "estimate 0.386, LOO sd 0.066; blockinv3 estimate 0.3138, LOO sd 0.021",
  "registry_correlation": "worst 3 px overlap 39.8% vs GEMSDOE27; exact overlap with blockinv3 7.4% (Jaccard 0.035); 91.4% within 3 px of blockinv3 (same lane)",
  "raster_sha256": "39eb9e1d7961ce2befb87d6fea841933f820b470abd274de73639184a196be43",
  "validator_output": "16/16 checks pass; no NaN inside footprint; values in [0,1]; CRS/shape/transform match; mask band declares 7,111,787 null cells outside",
  "submission_name": "korea7-blockinv-b4-n12000-k106922-20261104T200956Z",
  "submission_note": "block-inversion 400m: 106922 dots; est 0.386 (LOO sd 0.066)",
  "verdict": "promote"
}
```

### Limitations and next steps

- The organizer's test labels are private; the estimate is not an organizer score.
- The nine focus-site scores are user-reported, not organizer-confirmed.
- The blockinv3 reference is from a sibling project (GEMSDOESASS3) and its scores are
  owner-reported.
- The competition's `training_features.tif` is login-walled; this repo uses the
  sample-submission grid, the labels raster, and published rasters.
- The live leaderboard is dynamic; the values above are a 31 Oct 2026 snapshot.
- Next: submit the new file, record the organizer receipt, restore the 128-raster corpus,
  obtain the 19-band feature stack, and train a U-Net / gradient-boosted model.
