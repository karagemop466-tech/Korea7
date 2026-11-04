# Korea7 — DOE GEMS Prize submission research

**Read this file and [`docs/index.html`](docs/index.html) at the start of every session.**

---

## Current decision (2026-11-04)

> # ⛔ DO NOT SUBMIT
>
> A unique, format-passing GeoTIFF was generated and gated. It clears the **format**,
> **uniqueness** and **holdout-vs-control** gates and fails the **score** gate.
> MODEL-ESTIMATE **0.0434** (95% 0.0205-0.0662) against an owner-reported programme best of
> **0.2778** and a leaderboard high of **0.4413**.
>
> File: [`docs/downloads/k7-oslf-lat11-n27159-20261104T210000Z.tif`](docs/downloads/k7-oslf-lat11-n27159-20261104T210000Z.tif)
> · sha256 `ebdf0342273688a26dab6a5bbd539b17b8d8cfa98355b63b406c095cc268c7b7`
> · 27,159 dots · worst 3 px overlap vs any of the nine focus sites **16.9%** (fail above 70%)
> · worst surface |ρ| **0.0057** (fail above 0.90).
>
> Nothing was uploaded: the DrivenData portal is login-walled and unreachable from the sandbox.

**Start here:** [decision page](docs/index.html) · [nine-site executive summary](docs/executive.html)
· [hypotheses register](docs/hypotheses.html) · [submission mechanics](docs/submission.html)
· [sources](docs/sources.html) · [the range-error explanation](docs/portal-error.html)

---

## Standing brief (the owner's requirements, restated once)

Maximise the probability of winning. Own the outcome end to end. No fabricated numbers, no
hallucinated sources, no projection written as a score.

1. **Place at the top of the DrivenData DOE GEMS leaderboard.** Study the highest-scoring submissions
   from **GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, 36** and produce an executive summary and a
   comparison table for each: which file to download, what its score is or is estimated at, and
   whether it is unique.
2. **Generate a UNIQUE TIF.** Never copy a previous submission except for learning or forensic
   comparison. The file must be obviously marked OK / NOT OK to download and submit, decided
   automatically inside the project — no human inspection step.
3. **Validate without a human in the loop.** Gates run in code, fail closed, and record their own
   evidence.
4. **Label every number** as HOLDOUT-DTI (instrument version, withheld positives, 95% CI),
   MODEL-ESTIMATE, USER-/OWNER-REPORTED, or ORGANIZER-CONFIRMED. A projection is never a score.
5. **Lane discipline.** If the surface's rank correlation with any registry raster exceeds 0.90, or
   more than 70% of the dots fall within 3 px of one registry raster's dots, it is a duplicate lane:
   log it and stop. Check the surface before placement and the final dots after.
6. **Reuse, don't rebuild**, shared tools (`evaluate_holdout`, submission writer, cached features).
   Fix a shared tool once where it lives and report the fix; never keep a private fork.
7. **Leakage canary.** Test each feature alone on the holdout first. Single-feature AUC above 0.90
   means leakage until proven otherwise.
8. **Run card** in JSON: hypothesis, mechanism, the named non-fault process that could mimic it,
   holdout DTI + CI, registry correlation and overlap, raster sha256, validator output,
   submission name and a ≤140-character note, and a verdict of promote or negative. Negative
   results are deliverables.
9. **Budget.** Stop after 3 experiments or 2 hours per lane. Promotion to a real submission slot is
   a separate decision, within the weekly cap shown on the submission page.
10. **Hypotheses before code.** 3–5 untried geological hypotheses, each naming the layer(s), the
    physical signature, why it catches a catalogue-missing fault rather than a catalogue one, and
    how it differs from this repo's prior art; ranked by expected DTI gain and cost; validated on a
    spatially-blocked holdout before any submission slot is touched. If a hypothesis needs new
    external data, name the free official source and verify it is obtainable first.

**Not supplied:** the "single method paragraph" that the parallel-run protocol says defines a lane
was never provided in any session. It is not guessed here. This repository instead occupies a lane
it states for itself: *catalogue-independent, coverage-first emission validated on a
hide-and-recover instrument.*

---

## What is actually established here

### Why `h33-h33-2-b2` on GEMSDOE32 scored 0.2778

Three measured facts, in order of weight. Details and links in [`docs/index.html`](docs/index.html).

1. **The organisers do not score the faults you can see.** DrivenData staff, 16 Sep 2025
   ([thread 11516](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516)):
   *"Pixels corresponding to known USGS/INGENIOUS faults are masked / excluded from evaluation, so
   they do not count towards penalty terms."* The test set is a set of faults **absent** from the
   public database. Read in full on 2026-11-04.
2. **The nine focus files are one family and the champion is its most pruned member.** Exact
   dot-set algebra, measured here (`symdiff = 0` in every line):
   `GEMSDOE25 ≡ GEMSDOE30` → `GEMSDOE31 = GEMSDOE25 − {dots within 1 px of catalogue}` →
   `GEMSDOE32 = GEMSDOE31 − {dots within 2 px of catalogue}` → `GEMSDOE36 = GEMSDOE32 + 1,200 dots`
   and scores 0.0028 **lower**.
3. **The score is monotone in how few dots sit within 3 px of the catalogue**:
   12,187 → 0.2449, 11,938 → 0.2477, 8,607 → 0.2600, 4,716 → 0.2708, 2,171 → **0.2778**.

The mechanism: those dots sit on the 100–200 m flank of mapped traces, where the truth is a *new*
fault that is usually absent, so each one pays a false-positive tax. Removing them costs no credit.
The pruning stops paying at 2 px, which is why 0.2778 is this family's ceiling.

**What the champion is not.** Its recovery of the *visible* catalogue is DTI **0.0067**, below a
uniform random field of the same size (**0.0692**), because it deliberately avoids the catalogue.
Any model trained to predict the labels you can see is being optimised in the wrong direction. This
is the most important structural fact about this competition.

### The score estimator (`src/gems/estimate.py`)

For a binary prediction the metric collapses to

```
DTI = c · K / (0.2·N + 0.8·K)
```

with `c` kernel-weighted recall, `N` dots, `K` withheld truth pixels. `K` is pinned by one anchor
whose mechanism is known — the 5 px lattice `13GEMSDOE_r13-lattice-s5`, measured here at exactly
**206,895 dots**, owner-reported **0.0904** → **K = 12,773**. The model then *predicts*, unfitted,
that the best square lattice is s = 5 — the spacing the programme actually chose. Absolute error is
unmeasurable without organiser receipts, so every estimate carries ±0.02 model risk.

Consequences: 0.2778 implies `c = 0.386`; 0.4413 at the same budget implies `c = 0.611`. **The gap
at the top is recall, 1.6×, not formatting and not metric games.**

### What blocks the only viable path to more recall

1. **`training_features.tif` is unreachable.** 418,912,844 bytes, sha256 `4371c82e…`. Login-walled
   at DrivenData; the mirror the programme used (`buffedlizard55-lab/GEMSDOE`) now returns **HTTP
   404** and that GitHub account does not exist. Verified 2026-11-04.
2. **The 1 m DEM is unreachable.** The highest-value missing input by a wide margin — 100× the
   competition's posting — but the tiles are tens of GB on 3DEP/OpenTopography and the competition's
   link file is login-walled.
3. **No organiser receipts exist** anywhere in the programme. Every historical score is
   OWNER-REPORTED.

---

## Experiments run this session (3, within budget)

Instrument **K7-HIDE-RECOVER-1.0**: whole connected fault segments withheld with a 10 px buffer;
scored domain = footprint minus visible faults and their buffer; every arm emitted at a **matched
20,000-dot budget** with a 3 px collar removed; official pooled DTI with a segment-level bootstrap
95% CI. Unbiased for a catalogue-free surface; **not** live-valid for catalogue-derived ones.

| # | Question | Result |
|---|---|---|
| 1 | Does a seismogenic-lineament surface find blind faults? | **NEGATIVE** — 0.0144 vs 0.0391 for uniform random. AUC 0.558/0.537, so not leakage, just weak. |
| 2 | Which emission strategy wins when skill is weak? | Lattice modulated by the surface **0.0463** > random 0.0405 > hard-selected top 0.0144 > tip collar 0.0031. Coverage beats concentration, and the tip-collar arm reproduces the live GEMSDOE27/33 losses. |
| 3 | Can the programme's own family be beaten by re-tuning? | **No.** The pruning optimum is at 2 px; both live attempts to add dots lost. Closed by measurement, not assertion. |

---

## Reproduce

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt

python scripts/fetch_external.py             # official external layers -> evidence/external_layers.json
python scripts/characterise_registry.py      # nine-site forensics  -> evidence/registry_forensics.json
python scripts/holdout_experiment.py         # experiment 1         -> evidence/holdout_experiment.json
python scripts/experiment2_emission.py       # experiment 2         -> evidence/experiment2_emission.json
python scripts/build_candidate.py            # candidate + 4 gates  -> evidence/run_card.json
python scripts/build_site.py                 # regenerates docs/*.html from the evidence
.venv/bin/pytest -q                          # test suite
```

Re-running `holdout_experiment.py` → `experiment2_emission.py` → `build_candidate.py` from a
clean `.cache` reproduces the delivered GeoTIFF **bit-for-bit** (verified 2026-11-04: identical
sha256 before and after).

`scripts/build_candidate.py` exits **0 only when all four gates pass** — format, uniqueness,
holdout-vs-control, and estimate-beats-programme-best. It currently exits **2**. The site banner is
generated from the same JSON, so the published verdict cannot disagree with the evidence.

## Layout

```
src/gems/          metric (vendored, re-verified) · grid · registry · surface · screen · external · estimate
scripts/           measure, experiment, build, gate, publish
data/reference/    official sample_submission.tif + labels.tif (hash-pinned)
data/registry/     the nine focus-site rasters + receipts.json
evidence/          every JSON the site is generated from
docs/              the published site and the downloadable artefact
tests/             the test suite
```

## Known limitations and what to do next

1. **The estimator is a model, not a measurement.** It rests on `F = N − T` and on one owner-reported
   anchor. First action for any future session with portal access: capture organiser receipts and
   re-fit `K`. That single step converts this whole project from inference to measurement.
2. **The holdout instrument cannot validate catalogue-derived surfaces.** It anti-correlates with the
   live board for them (prior sessions measured ρ ≈ −0.85). It is used only where it is unbiased.
3. **Only one external layer survived.** Seismicity from GDR 1391 via a GitHub mirror. The 19-band
   stack, the 1 m DEM and the GeoDAWN rasters are all unreachable.
4. **Highest-value next step, in order:** (a) restore `training_features.tif` from an unrestricted
   machine using the hash pin, then re-run Experiments 1–2 on the real 19 bands with spatially
   blocked folds; (b) acquire the 1 m DEM and implement H5; (c) obtain one organiser receipt to
   calibrate the estimator; (d) only then consider spending a submission slot.
5. **No submission slot was used.** Promotion is deliberately a separate, manual decision.
