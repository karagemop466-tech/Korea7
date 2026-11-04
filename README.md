# Korea7 — DOE GEMS unmapped-fault submission

> **Read this first, every session.** It is the standing brief, the verified state of the repository, and the
> rules that must not be broken. If a later message conflicts with this file, this file wins until it is edited.

---

## 1. The deliverable, right now

**Download and submit `submissions/korea7-halo-band4-45-lat89-38000.zip`** (or the `.tif`).

| | |
|---|---|
| TIF SHA-256 | `5c6c1772e08679d4579f1ec315c0c264fb422f207750308bb263ee42aa39d720` |
| ZIP SHA-256 | `b0ca4c1b714f421470bad9bf0e807286ce96780342c771a8bf5ed4ea0157f516` |
| Validator | 12 / 12 checks pass |
| Unique | max Jaccard **0.0042** against all nine recovered GEMSDOE rasters |
| Score claimed | **none** — no organizer receipt exists |

Portal note (139 / 140 chars), copy exactly:

```
Unique lattice G(8,5), all dots >400 m from catalogue, median 19.1 px; matches best prior geometry, Jaccard 0.004 vs all 9 registry rasters
```

Full reasoning, tables and limitations: **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)**. Site: **[docs/index.html](docs/index.html)**.

---

## 2. Objective and non-negotiable evidence rules

Build an auditable workflow for predicting unmapped faults relevant to geothermal exploration for the
DOE GEMS competition, and submit a **unique**, format-valid GeoTIFF. Improve the chance of a strong result
without ever claiming a score that has not been measured.

- **Distinguish evidence classes.** Every number is exactly one of:
  - `HOLDOUT-DTI` — measured here, with evaluator version, withheld-positive count, 95 % CI.
  - `MODEL-ESTIMATE` — a simulation under a stated assumption. Never written as a score.
  - `USER-REPORTED` — an owner-supplied value. **Not** a receipt.
  - `ORGANIZER-CONFIRMED` — only with receipt text. **None exists in this repository.**
  A projection is never written as a score.
- **Never republish another entrant's raster as a submission.** Novelty claims require real pixel comparisons and
  SHA-256 records. Lane limits: rank correlation ≤ 0.90 and no more than 70 % of dots within 3 px of one
  registry raster. Real files live in `evidence/registry/` for auditing only.
- **Reuse, don't fork.** The shared tooling (`k7/metric.py`, `k7/holdout.py`, `k7/validate.py`) is the single
  source of truth. If it is wrong, fix it here and say so — never keep a private copy.
- **Holdout discipline.** Withhold whole structures with a buffer; derive catalogue-dependent features from
  visible faults only; mask visible faults pixel-exactly; score pooled DTI (α 0.2, β 0.8, 300 m triangular
  kernel) with a spatial block bootstrap.
- **Leakage canary.** Test each feature alone before trusting it. AUC > 0.90 is leakage until explained.
- **Budget.** At most 3 experiments or 2 hours per session. A negative result is a deliverable.
- **Run card.** Every candidate ends with a JSON card: hypothesis, mechanism, the non-fault process that could
  mimic it, holdout/estimate with its label, registry correlation and overlap, raster SHA-256, validator output,
  submission name + ≤ 140-char note, verdict `promote` / `negative`.

### Core values applied here

- **Maximize P(Win).** Prefer the decision that most raises the chance of a top leaderboard result. That means
  measuring before building, and killing a favoured idea when the data kills it.
- **Own the Outcome.** Follow through to a downloadable, validated artifact — and report the failure modes
  honestly rather than shipping a reassuring narrative.

---

## 3. Verified state of the repository (2026-11-04)

Everything below was checked in this session. Nothing is assumed.

| Fact | Method | Result |
|---|---|---|
| Nine focus sites unreachable | `api.github.com/users/buffedlizard55-lab`, codeload | **HTTP 404 — account does not exist** |
| Nine rasters recovered | cloned `karagemop466-tech/GEMSDOEkarage3` | 9/9 in `evidence/registry/`, hashed |
| Competition grid | `data/sample_submission.tif` | EPSG:32611, 3292×3730, 100 m, 5,167,373 footprint cells |
| Catalogue | `data/labels.tif` | 60,988 positives, 3,199 components, density 1.18 % |
| Sample submission == labels | value comparison | agreement **1.000** |
| Metric correctness | brute-force transcription, 5 trials | agree to **1e-9** |
| Best-file mechanism | prune GEMSDOE25 at 2 px | **pixel-exactly GEMSDOE32** |
| Duplicates in the nine | Jaccard | **GEMSDOE25 ≡ GEMSDOE30 (1.0000)**; 7 pairs ≥ 0.90 |
| Score predictor | Spearman, 38 scored rasters | ρ(score, median dist) = **+0.503, p = 0.001** |
| Test suite | `pytest tests/ -q` | **22 passed** |

### What is permanently gone

`training_features.tif` — the 19-band GeoDAWN stack, 418,912,844 bytes, SHA-256
`4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5` — and the four external geophysical
rasters. Their only mirror was `buffedlizard55-lab`. There are no GitHub Releases on any surviving account, and
no surviving repository holds a file over 36 MB. **It cannot be recovered in this environment.** The
consequence is structural: no submission built here can use geophysics, and every one must say so.

---

## 4. What the measurements changed

The project spent many sessions optimising *clearance from the catalogue*. That was half the story.

1. **The best result was a deletion, not a method.** GEMSDOE32 (0.2778) is GEMSDOE25 with every dot at
   `d ≤ 2 px` removed — and also GEMSDOE31 with the same operation. XOR = 0 in both cases.
2. **The nine files are one file with edits.** Seven duplicate pairs at Jaccard 0.91–1.00, one of them exact.
   "Pick the best site and resubmit" is impossible: every candidate is already scored.
3. **Distance, not clearance, is the signal.** Across 38 scored rasters the strongest predictor of score is the
   median distance from emission to catalogue (ρ = +0.503, p = 0.001). The top of the table is a cluster at
   14–20 px with ~80–94 % of dots beyond 3 px — a *sparse emission on distant ground*, not a halo.
4. **A hypothesis died.** A 400 m-clearance uniform lattice scores **0.0004** against a dense extension model
   versus 0.525 for a dense halo. It was the leading idea and the data rejected it. That negative result is
   kept in `evidence/synthetic_experiment.json`.

---

## 5. Repository layout

```
data/                 verified competition templates (labels.tif, sample_submission.tif), hash-pinned
k7/                   library
  metric.py           exact DTI + brute-force oracle + kernel constants
  grid.py             grid constants, template loading, hash verification
  method.py           rotated-square lattice, clearance gating, silence audit
  holdout.py          spatially-blocked hide-and-recover evaluator + block bootstrap
  overlap.py          lane compliance: Jaccard, 3 px overlap, rank correlation
  synth.py            synthetic-geology upper bound
  validate.py         12-check submission gate + GeoTIFF writer + ZIP bundler
scripts/
  calibrate.py        site table, duplicates, correlations        -> evidence/calibration.json
  experiment_synthetic.py  strategy comparison                    -> evidence/synthetic_experiment.json
  experiment_sweep.py      clearance x budget sweep               -> evidence/sweep_experiment.json
  final_candidates.py      candidate ranking                      -> evidence/final_candidates.json
  make_submission.py       build + validate + run card            -> submissions/
tests/test_k7.py      22 tests
evidence/             registry rasters, ledger, all measured outputs
submissions/          the shippable artifact (.tif, .zip, run card .json)
docs/                 the GitHub Pages site (index.html + copies of the downloads)
```

---

## 6. Submission gate

A file may be called **OK TO SUBMIT** only when all of these are true *and reported from the actual output*:

1. One-band GeoTIFF (or a ZIP with exactly one).
2. CRS, shape and geotransform exactly match `data/sample_submission.tif`.
3. Every value finite and inside `[0, 1]`; no NaN or Inf anywhere. Outside the footprint, `0.0` is preferred to
   NaN — a stray NaN is what makes the portal answer *"Predicted values must be in range [0, 1]"*.
4. Zero dots outside the footprint.
5. Binary emission (`{0,1}`) — no accidental probability field.
6. Beats the current internal baseline on the blocked holdout, with its label attached.
7. Passes the lane test against every registry raster (Jaccard < 0.70, within-3px ≤ 0.70).
8. SHA-256 recorded; unique name; note ≤ 140 chars.
9. Never labelled organizer-scored without a receipt.

`k7/validate.py` enforces 1–5 and 8 and is covered by tests, including explicit NaN and out-of-range cases.

---

## 7. Standing risks

1. **The largest risk is that this scores near zero.** If unmapped faults are sparse, 37 k dots may land almost
   none within 300 m of real structure. Emitting nothing scores 0.000 — a floor, not a loss.
2. **No geophysics.** The surface is a prior. Any credit is coverage, not detection.
3. **The +0.503 relation is cross-sectional** over 38 points; it confounds density, spacing and clearance.
4. **0.2778 is unverified.** Owner-reported only.
5. **The masking rule comes from a forum answer**, not the problem page.

---

## 8. Next work — in priority order

1. **Get `training_features.tif` from an authenticated DrivenData download.** Everything quantitative depends on
   it. Nothing else unblocks real modelling.
2. **Spend one weekly slot to calibrate.** One submission from the new family, receipt recorded in
   `evidence/score_receipts.json`, converts every model estimate here from a guess into a measurement.
3. **Build the independent validation target that still works.** USGS SGMC faults rasterised to the competition
   grid, restricted to > 300 m from `labels.tif`. Free and official; needs a rasterisation step off-sandbox.
4. **Rebuild the external stack from primary sources** — USGS GeoDAWN (magnetic/radiometric), USGS 3DEP 1 m DEM,
   GDR Wellspring (`https://gdr.openei.org/submissions/1391`). All free, all official, none reachable from this
   sandbox's allow-list.
5. **Only then** design geophysical hypotheses. Until step 1 lands, another clearance variant is just another
   edit of a file that already exists nine times.

---

## 9. Running it

```bash
python scripts/calibrate.py
python scripts/experiment_synthetic.py
python scripts/experiment_sweep.py
python scripts/make_submission.py
python -m pytest tests/ -q
```

Requires `numpy`, `scipy`, `rasterio`, `pytest`. No GPU, no network, no credentials.

---

## 10. Sources for manual review

**Competition** — [overview](https://www.drivendata.org/competitions/306/competition-doe-gems/) ·
[problem & metric](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/) ·
[about](https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/) ·
[data](https://www.drivendata.org/competitions/306/competition-doe-gems/data/) ·
[leaderboard](https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/) ·
[rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf) ·
[organizer masking clarification (thread 11516)](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516)

**Reference** — [drivendataorg/gems-prize-reference-solution](https://github.com/drivendataorg/gems-prize-reference-solution) ·
[EPSG:32611](https://epsg.io/32611) · [Tversky index](https://en.wikipedia.org/wiki/Tversky_index)

**Data** — [USGS GeoDAWN](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and) ·
[GBC/INGENIOUS](https://gbcge.org/current-projects/ingenious/) ·
[GDR 1391](https://gdr.openei.org/submissions/1391)

**Registry sites (all 404 as of 2026-11-04)** — GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, 36 under
`buffedlizard55-lab.github.io`. Rasters preserved in `evidence/registry/` for auditing only.
