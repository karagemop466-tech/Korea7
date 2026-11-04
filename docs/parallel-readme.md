
# Korea7 - DOE GEMS Prize: submission engineering and research

**Status, first line, no hedging: there is no submission file in this repository that should be
uploaded.** The three competition rasters are behind a DrivenData login; the nine GEMSDOE sites are
unreachable and their GitHub account returns 404. A GeoTIFF produced without them would be a guess
that spends a weekly slot for a score near zero. What *is* delivered is the measured machinery that
turns those three files into a unique, validated submission in one command.

*Read in this order:* **[executive summary](docs/index.html)** (the table you asked for) -
[how to submit](docs/submit.html) - [method and results](docs/method.html) -
[source audit](docs/verification.html) - [research log and hypothesis queue](docs/research.md).

---

## The standing brief (kept verbatim in intent, read at the start of every session)

Build an auditable, automated, continuously improving workflow for **unique, high-scoring DOE GEMS
fault-detection submissions**, and beat the leaderboard.

Requirements that must never be relaxed:

1. **A unique GeoTIFF submission.** Never copy or republish another entrant's raster. Copying a
   previous submission is acceptable only as a learning/education artefact, never as an output.
   Uniqueness must be *tested* (rank correlation and dot overlap against the registry), not asserted.
2. **It must be obvious whether a file is OK to download and submit.** The site says so at the top of
   the page and in the run card; the file's status is in its own name.
3. **Focus on the highest-scoring submissions of GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, 36**, explain
   *why* they scored what they did, and say whether we can beat them.
4. **A table in the executive summary** listing, per site: which file to download, the estimated
   score, and whether it is unique versus the others.
5. **No human inspection step.** Every gate (format, range, CRS/shape/transform, uniqueness, holdout)
   is automated and machine-verifiable. "Inspection" in this project means the validator and the run
   card, not a person looking at a picture.
6. **No hallucinations.** Every number is labelled ARITHMETIC, SIMULATION, HOLDOUT-DTI (with evaluator
   version, withheld positives and CI) or ORGANIZER-CONFIRMED. A projection is never written as a
   score. Irregularities are flagged, not smoothed over.
7. **Work line by line from official, verifiable sources, with links for manual review** - see
   `docs/verification.html`.
8. **Parallel-run protocol.** Stay in the lane described in `docs/method.html`; stop on rank
   correlation above 0.90 or more than 70% of dots within 3 px of one registry raster; reuse the shared
   evaluator and writer rather than forking them; three experiments or two hours, then stop; negative
   results are deliverables; promotion to a real slot is a separate selector decision.
9. **Score higher than the current leaderboard.** Design new strategy, research, testing and analysis
   rather than repeating the existing method; be contrarian but grounded.
10. **Solve the manual-checking problem.** A single command, a run card, and a page that is regenerated
    from the measurement files so it cannot drift.

### Core values applied to this project

* **Maximize P(win).** A submission that scores 0.0000 costs a weekly slot and the information a real
  attempt would have produced. When the data needed to place cells is missing, the decision that
  maximises the probability of winning is to *not* upload, and instead make the path to a real
  candidate one command long. That is what this repository does.
* **Own the outcome.** The gates, the writer, the validator, the registry screen and the run card are
  all implemented here, tested, and run end to end on synthetic data of the correct format. Failures
  are reported as failures (see the negative result on the coverage-aware emitter).

---

## Quick start

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt

# 1. reproduce the three experiments (~90 s) and the numbers on the site
.venv/bin/python scripts/run_experiments.py
.venv/bin/python scripts/make_report.py

# 2. end-to-end self-test on synthetic competition-format data (proves the code paths)
.venv/bin/python scripts/make_demo_data.py --out demo
.venv/bin/python scripts/build_submission.py --data demo --out out/demo.tif

# 3. the real run, once numeric_features.tif / labels.tif / sample_submission.tif are in data/
.venv/bin/python scripts/build_submission.py --data data --out out/submission.tif \
    --registry registry.json

# 4. gates
.venv/bin/python -m gems.validate out/submission.tif --reference data/sample_submission.tif
.venv/bin/python -m gems.registry --candidate out/submission.tif --manifest registry.json
.venv/bin/python -m pytest -q
```

## What each part does

| Path | Role |
|---|---|
| `gems/metric.py` | DTI (300 m triangular kernel, alpha 0.2, beta 0.8), fast and reference paths, exact band table |
| `gems/grid.py` | the verified competition grid, with provenance in the docstring |
| `gems/features.py` | multi-scale Hessian lineament and gradient features; catalogue features recomputed per fold |
| `gems/model.py` | ridge logistic regression (Newton/IRLS, class-balanced) and spatial block folds |
| `gems/calibrate.py` | isotonic PAV calibration, reliability bins, tie-aware AUC |
| `gems/emission.py` | Dinkelbach threshold, top-k, NMS, dilation, and the coverage-aware greedy (which lost) |
| `gems/holdout.py` | buffered segment-blocked holdout, leakage canary, segment bootstrap CI |
| `gems/geometry.py` | tips, along-strike extension, gap closure, proximity fields |
| `gems/network.py` | synthetic fault networks calibrated to four published statistics |
| `gems/writer.py` | cannot write NaN or out-of-range values; verifies by read-back |
| `gems/validate.py` | fail-closed format gate, single file or zip |
| `gems/registry.py` | uniqueness screen (rho > 0.90 or > 70% dots within 3 px blocks) |
| `scripts/build_submission.py` | the one command |
| `scripts/run_experiments.py` | E1 metric/calibration, E2 emitter contest, E3 evaluator-regime sensitivity |
| `scripts/make_report.py` | regenerates the site from the JSON, so the page cannot drift |
| `docs/` | executive summary, submission guide, method, source audit, results JSON |

## Honest limitations

* No competition data has ever been seen by this code; every model number is synthetic.
* The metric is transcribed from the public description and matched against two independent public
  implementations, not organizer code: absolute values are replicable, not certified.
* The nine sites are public only to the user, so no uniqueness or score claim about them is possible
  from here.
* The evaluator's scored cell set is not published anywhere reachable, and the winner changes with it
  (E3); the run card therefore always names the regime it used.

---

## Parallel lanes in this same repository (not produced by this lane, not verified by it)

Other sessions working from the same brief committed candidate rasters under `docs/downloads/`.
They are listed here so nothing is hidden and nobody mistakes them for this lane's output:

| File | Producer's claim | What this lane's tools say |
|---|---|---|
| `korea7-k7-offcatalogue-relay-corridor-30000dots-...-zeros.tif` | 10,944 dots, own receipt JSON, "score not measurable" | **FAIL** format gate: geotransform origin `(243350, 4508550)` differs from the recorded grid `(250000, 4520000)`; uniqueness UNKNOWN |
| `korea7-sdcc1-scarpdom-conc-uniq65-37654-...-d88f4742-zeros.tif` | SDCC-1 candidate, own receipt | **FAIL** on the same transform mismatch |
| `korea7-sdcc1-scarpdom-conc-uniq65-44090-...-5631ba53-zeros.tif` | SDCC-1 candidate, own receipt | **FAIL** on the same transform mismatch |

Two different grid origins now exist in one repository, and only the official
`sample_submission.tif` can settle which is right (see irregularity **F8** in
`docs/verification.html`). Until it does, none of these files should be uploaded.
