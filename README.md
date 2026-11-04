# Korea7 — DOE GEMS fault-detection submissions

**Current decision (2026-11-04): ✅ OK TO DOWNLOAD — candidate KOREA7-E3 is promoted to the owner's selector step.** It is a new, unique, format-valid GeoTIFF that beats every focus-site winner on the leaderboard-aligned holdout instrument with a non-overlapping 95% CI. Spending a weekly submission slot remains the owner's separate decision (read the risk box first). **[Executive summary & download](docs/index.html)** · **[How to submit](docs/submission.html)** · **[Run card](run-card.json)**

| Download this file | SHA-256 | Estimated score (labelled) | Unique? |
|---|---|---|---|
| [docs/downloads/gemsdoe32-korea7-scarprad-b2cov-r100-20261104T201931Z-7dcabf26-zeros.tif](docs/downloads/gemsdoe32-korea7-scarprad-b2cov-r100-20261104T201931Z-7dcabf26-zeros.tif) | `f013b9c451a38730bb2527d7d096b98d9447b67df9af45902fc998a2ec7bb40d` | **HOLDOUT-DTI 0.0963 [0.0799, 0.1113]** (GEMSDOE32-SGMC-CAL-v3.0, 62,703 withheld proxy positives) vs nine-site best 0.0644. No defensible leaderboard point estimate (brackets in summary §5); never quote the proxy as a leaderboard score. | **YES** vs GEMSDOE24/25/27/28/30/31/32/33/36: surface ρ ≤ 0.036 (limit 0.90), ≤27.3% dots within 3 px of any winner (limit 70%), Jaccard ≤ 0.008 |

Submission note (106/140 chars): `Korea7 E3 scarpXrad concordance b2 greedy kernel-cover 37654 roadctl zeros SGMCcal 0.0963 unique-vs-focus9`

**Why the nine-site champion (GEMSDOE32 h33-…-b2, USER-REPORTED 0.2778) won** — measured from its bytes, reproduced here: all nine winners are one h19-5 ridge family (25 ≡ 30 identical; champion ⊂ 25/30/31/36). The champion is its parent minus exactly 2,545 dots lying 1.41–2.00 px from catalogue traces; scored truth is off-catalogue, so that ring earns ~0 and only pays false-positive tax under the 300 m-kernel DTI (α 0.2, β 0.8). Fewer, well-spaced (2.8 px), off-catalogue dots win; the family is at its optimum (champion + 1,200 dots on GEMSDOE36 scored lower). Beating it requires a better *surface*, which is what KOREA7-E3 tests: lidar scarp × radiometric-edge concordance, greedy kernel-coverage emission, b2 gate, road-mimic control. Whether it beats 0.2778 on the leaderboard is **unknown until an organizer receipt** — evidence and risks are itemized in the executive summary.

## Standing brief (read at the start of every session)

Build an auditable, automated workflow for unique, high-scoring GEMS submissions. Focus sites: GEMSDOE24, 25, 27, 28, 30, 31, 32, 33, 36. Never copy a previous submission as new work; uniqueness gate ρ ≤ 0.90 and ≤70% dots within 3 px, on surface before placement and on final dots. Reuse the shared template (`evaluate_holdout.py`, `submission_writer.py` — vendored byte-identical in `vendor/gems32/`, do not fork). Holdout = buffered whole-segment hide-and-recover + off-catalogue SGMC-CAL, pooled DTI α 0.2 / β 0.8 / 300 m triangular kernel. Label every number HOLDOUT-DTI / USER-REPORTED / ORGANIZER-CONFIRMED (only with a receipt); a projection is never a score. Leakage canary: single-feature AUC > 0.90 = leakage until proven otherwise. Budget ≤3 experiments or 2 h per lane; promotion/slot is a separate selector step. End every run with a JSON run card; negative results are deliverables. **Maximize P(Win). Own the Outcome.** No hallucinations — verify line by line from official sources (competition: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/), flag irregularities, never ask for credentials.

## Reproduce (CPU, ≈3 min once restored)

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/restore_data.py          # 17 hash-pinned mirror files -> data/, registry/
.venv/bin/python scripts/canary.py                 # leakage canary (max AUC 0.599)
.venv/bin/python scripts/build_experiments.py      # E1/E2 surfaces + greedy emissions -> work/
.venv/bin/python scripts/build_e3.py               # E3 road-mimic control
.venv/bin/python vendor/gems32/scripts/evaluate_holdout.py work/E3_mask.npy --data-dir data --name KOREA7-E3
.venv/bin/python scripts/uniqueness.py --surface work/E3_surface.tif --mask work/E3_mask.npy
.venv/bin/python vendor/gems32/scripts/submission_writer.py work/E3_mask.npy --slug korea7-scarprad-b2cov-r100 \
  --candidate-id KOREA7-E3 --note "Korea7 E3 scarpXrad concordance b2 greedy kernel-cover 37654 roadctl zeros SGMCcal 0.0963 unique-vs-focus9" --out-dir docs/downloads --data-dir data
.venv/bin/python scripts/validate_submission.py docs/downloads/*-zeros.tif data/sample_submission.tif
.venv/bin/pytest -q
```

Anatomy/fleet evidence: `scripts/analyze_champion.py`, `scripts/fleet_stats.py`, `scripts/calibrate.py` → `evidence/`. The strict validators (`validate_submission.py`, `validate_raster.py`, `check_candidate.py`) are preflights whose `ready_to_submit` is intentionally always false — the promotion decision lives in `run-card.json`, not in any single tool.

## Limitations (flagged, not hidden)

- Inputs are SHA-256-pinned **owner GitHub mirrors**, not organizer-authenticated downloads; the original GEMSDOE* repos return 404 today and the 19-band `training_features.tif` has no live mirror (organizer login download is the fix). See `evidence/data_provenance.json`.
- Every leaderboard value in this programme is **user-reported**; zero organizer receipts exist in any repo examined.
- The literal “any registry raster” uniqueness reading is unmeetable against the dense r13 lattice witness (99.3% coverage of any candidate); Korea7 gates on the nine focus sites per the brief — owner ruling needed (IR-K7-01).
- SGMC-CAL is a proxy whose ground truth (geologic-map faults) may reward contact-tracing; the nine-point projection (0.4268) is recorded and **rejected** as extrapolation. Live scarp-led analogs scored 0.04–0.16.
- GitHub Pages deployment of `docs/` must be enabled in repo settings (Settings → Pages → branch `main`, folder `/docs`) — not verifiable from this sandbox.
- Next: authenticate data via DrivenData; selector decision + receipt capture; if submitted and disappointing, preregister a fold-local family+E3 union experiment.
