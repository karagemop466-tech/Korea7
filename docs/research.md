# Research and evidence log

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

## Run card

```json
{"hypothesis":null,"mechanism":null,"named_non_fault_process":null,"holdout_dti":null,"evaluator_version":null,"withheld_positives":null,"ci_95":null,"registry_correlation":null,"registry_overlap":null,"raster_sha256":null,"validator_output":"BLOCKED: no candidate, reference, footprint, or complete registry","submission_name":null,"submission_note":null,"verdict":"negative"}
```
No experiment was run. This is a blocked run, not evidence that any scientific hypothesis failed.

---

# ADDENDUM — Session 2026-11-04 (arena/6a22835c-korea7): data found, nine reproduced, KOREA7-E3 generated

This addendum supersedes the "blocked / DO NOT SUBMIT" status above (preserved verbatim for audit). What changed: the owner's sister repositories — not accessible to the earlier session's checks of *this* checkout — contain hash-pinned mirrors of the competition grid, labels, nine focus winners, the shared template (evaluate_holdout.py / submission_writer.py), and external feature stacks. All were restored and SHA-256-verified here (`scripts/restore_data.py`, `evidence/data_provenance.json`); provenance is owner-mirror, not organizer-authenticated (IR-K7-02). The original buffedlizard55-lab repos return 404 today.

## Verified line by line this session
- Official metric fetched from DrivenData page 967 (alpha 0.2, beta 0.8, R=300 m triangular, worked example) and the vendored implementation cross-checked against a literal transcription (`tests/test_metric_official.py`).
- Nine-site HOLDOUT-DTI (SGMC-CAL-v3.0, 62,703 withheld) reproduced exactly vs GEMSDOEkarage3 2026-10-31 (e.g. champion 0.0641209376417646, CI identical).
- Champion anatomy reproduced from bytes: B2 = solo − 2,545 dots at 1.41–2.00 px from catalogue; 25 ≡ 30 exact; subset chain as tabled (`evidence/champion_anatomy.json`).
- Fleet statistics over the 160-row owner ledger (`evidence/fleet_stats.json`); leaderboard snapshots in-ledger resolve the prompt's 0.3195 (2026-10-03 #1) vs 0.4413 (2026-10-25 #1) conflict; sister snapshot 2026-10-31: #1 0.4544. Today's live board unreadable from sandbox (JS).
- Canary: max single-band AUC 0.599 (PASS). Hypotheses ranked pre-code (`docs/hypotheses.md`). Experiments E1 SGMC-CAL 0.0968, E2 0.0669, E3 (road control) 0.0963 [0.0799, 0.1113] vs nine-best 0.0644 — disjoint CIs. Fold-local OOF hide-recover E1 0.0049 [0.0040, 0.0058] (22,232 withheld) confirms no catalogue-feature leakage (surface has none).
- Final candidate KOREA7-E3 written by shared writer, validated on saved bytes by 3 tools; uniqueness vs nine: rho <= 0.036, overlap <= 27.3%, Jaccard <= 0.008. Full gate table + risk box: docs/index.html §5/§7. Run card: run-card.json (verdict promote-to-selector; slot decision = owner).
- Nine-point SGMC->reported projection = 0.4268, recorded and explicitly REJECTED as out-of-family extrapolation (`evidence/calibration.json`).

## Open irregularities
IR-K7-01 lattice-witness literal uniqueness unmeetable; IR-K7-02 mirror provenance / 404 originals / 19-band features unavailable; IR-K7-03 portal [0,1] error cause unresolved (mitigated); IR-K7-04 live leaderboard unverified today; IR-K7-06 zero organizer receipts in programme.

## Next steps (owner)
1. Optionally re-download data from DrivenData (login) and re-hash against `evidence/data_provenance.json` to authenticate provenance; restore 19-band features if obtainable.
2. Selector decision on KOREA7-E3 slot; if submitted, record organizer receipt into run-card.json.
3. If the receipt disappoints, the informative follow-up is a fold-local catalogue-anatomy + E3-surface union at fixed budget (tests whether SGMC or hide-recover is the transferable instrument) — preregister before running.
