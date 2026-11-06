# Repo audit — `karagemop466-tech/Korea7`

**Audit date:** 2026-11-06
**Session:** `arena-e6f84d88`
**Branch audited:** `arena/e6f84d88-korea7` at commit `91a0cbf`
**Auditor note:** every number below was measured in this session with the commands shown, or read from an official source with the link given. Anything not measured is marked **not measured**.

---

## 0. What this repository is

The repo is **not** about bathtubs. It is an audit trail for a submission to the
**DOE GEMS (Geothermal Exploration using Machine learning and Subsurface data)** competition,
hosted on DrivenData as competition 306.

| Aspect | Observed |
|---|---|
| Nature | Python research/audit package + static GitHub Pages site |
| Domain | Geothermal fault-prospectivity prediction from raster geology |
| Deliverable in repo | Single-band GeoTIFFs of "fault dots" at 100 m pixels, EPSG:32611 |
| Tests | `pytest` suite, 84 passed |
| Site | Static HTML in `docs/`, published by GitHub Pages |

**Owner action item:** the request in this session describes a bathtub repair, which has no
relationship to this repository's contents. Nothing was deleted or restructured to hide that.
All new work is in new paths (`bathtub/`, `docs/bathtub/`, `reports/`). See §6.

---

## 1. Checks that passed

| # | Check | Command | Result |
|---|---|---|---|
| 1.1 | Test suite | `pytest -q` (numpy 2.4.6, scipy 1.17.1, rasterio 1.4.4) | **84 passed** in 5.98 s |
| 1.2 | Every committed JSON parses | `json.load()` over `*.json`, `docs/**/*.json`, `evidence/*.json` | **0 invalid** |
| 1.3 | Internal site links resolve | regex over `docs/**/*.html` `href=` values, filesystem check | **0 broken** |
| 1.4 | Candidate SHA-256 matches README | `sha256sum docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif` | `9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c` — **matches README** |
| 1.5 | Candidate ZIP SHA-256 matches README | `sha256sum ...zeros.zip` | `7460b2dd99ba2cd44d412b3d021fa1c30fb0a25b071b6e5f66a0c661a0d2a6a5` — **matches README** |
| 1.6 | E3 SHA-256 matches README | `sha256sum ...7dcabf26-zeros.tif` | `f013b9c451a38730bb2527d7d096b98d9447b67df9af45902fc998a2ec7bb40d` — **matches README** |
| 1.7 | ZIPs contain exactly one TIFF with byte-identical payload | `zipfile` extract + sha256 | Consensus ZIP entry hashes to `9e3454…`, identical to the loose TIF. E3 ZIP entry hashes to `f013b9…`, identical. **PASS** |
| 1.8 | `SHA256SUMS.txt` matches the three rasters it lists | `sha256sum -c` semantics by inspection | **all 3 match** |
| 1.9 | Grid constants match the committed bridge files | `sha256sum data/bridge/*.tif` vs `vendor/gems57/grid.py` docstring | `2176d08e…` and `7ba308cc…` — **both match the docstring** |
| 1.10 | `data/labels.tif` is byte-identical to `data/bridge/existing_faults.tif` | `sha256sum` | both `7ba308cc…` — **identical, as the docstring claims** |
| 1.11 | NaN/finite counts in the sample submission | rasterio read | 7,111,787 NaN and 5,167,373 finite — **matches the `grid.py` docstring exactly** |
| 1.12 | All committed prediction rasters share one grid | rasterio transform read | origin `(243350, 4508550)`, pixel `100 m`, shape `3730×3292`, **all identical** |
| 1.13 | Dot counts of the named candidates | non-zero cell count | consensus **20,000** (claim 20,000 ✓), E3 **37,654** (✓), sdcc1 **37,654** (✓), sdcc1 **44,090** (✓) |
| 1.14 | Catalogue collision for the two promoted candidates | overlap with `data/labels.tif` non-zero cells | consensus **0**, E3 **0** — supports the "zero dots on catalogue" claim |

---

## 2. Irregularities

Severity scale: **HIGH** = contradicts the repo's own verification story. **MEDIUM** = misleading.
**LOW** = cosmetic or documentation drift.

### F-01 — A file named "30000dots" contains 10,944 dots — MEDIUM

| | |
|---|---|
| Claim location | Filename and every reference to it: `docs/downloads/korea7-k7-offcatalogue-relay-corridor-30000dots-20261104T000000Z-zeros.tif`, cited in `README.md:208` and `docs/index.html:241` |
| Claimed | 30,000 dots (in the name) |
| **Measured** | **10,944** non-zero cells (`(a>0).sum()`) |
| Self-disclosure | The raster's own `.receipt.json` **does** disclose it: `"n_dots": 10944, "n_dots_target": 30000` |
| Assessment | The receipt is honest; the filename is not. Any downstream page or person that quotes the filename asserts 2.7× the real dot count. |
| Recommended fix | Rename to `…-10944dots-…` or add "(target 30 000, produced 10 944)" wherever the name appears. |
| Fixed in this session? | **No.** GEMS artifacts are outside this session's file scope; logged in `COORDINATION.md`. |

### F-02 — The parallel lane's own fail reason is inverted — HIGH

This is the most serious finding, because the repo's entire value proposition is verifiability.

| | |
|---|---|
| Claim location | `docs/parallel-readme.md` rows 124–126 |
| Claim | All three parallel candidates **FAIL** the format gate because "geotransform origin `(243350, 4508550)` differs from the recorded grid `(250000, 4520000)`" |
| **Measured** | The three rasters are at origin **`(243350, 4508550)`**. The repo's own authoritative constant `vendor/gems57/grid.py: TRANSFORM = Affine(100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0)` is **`(243350, 4508550)`**. The only committed raster at `(250000, 4520000)` is **`docs/downloads/format_probe_score_0.0000_do_not_submit.tif`**. |
| Assessment | The stated reason for the FAIL is backwards: the three parallel rasters match the repo's recorded grid, and the probe file is the one that does not. Either (a) the FAIL verdict is wrong and these three files do pass the transform check, or (b) the FAIL is right for a different, unstated reason. Both possibilities matter, and neither can be left in a page whose purpose is audit. |
| Recommended fix | Replace rows 124–126 with the measured transform per file, and restate the verdict and its actual reason. If the verdict is retained, cite the check that produces it. |
| Fixed in this session? | **No** — `docs/parallel-readme.md` is pre-existing shared output. Logged in `COORDINATION.md` as a cross-session request. |

### F-03 — "Off-catalogue" lane places 72 dots on the mapped catalogue — MEDIUM

| | |
|---|---|
| Claim | Lane name is `k7-offcatalogue-relay-corridor`; `parallel-readme.md` describes it as off-catalogue |
| **Measured** | **72** of its 10,944 non-zero cells coincide with non-zero cells of `data/labels.tif`. That is 0.66 % of its dots sitting on the mapped fault catalogue. |
| For contrast | The two promoted candidates score **0** on the same test. |
| Assessment | Not a fatal defect and possibly intended (a corridor prior may legitimately cross mapped faults), but the word "off-catalogue" is then doing too much work, and the repo elsewhere treats catalogue overlap as a hard gate. |
| Recommended fix | State the 72-dot overlap explicitly on the page that cites the lane. |
| Fixed in this session? | **No.** Logged. |

### F-04 — Two different entry points for the site — LOW

| | |
|---|---|
| Observed | GitHub Pages `source.path` is `/` (repo root), `build_type: legacy`. The root URL renders `README.md` as a page. The designed site is `docs/index.html`, reachable only at `/Korea7/docs/`. |
| Consequence | A visitor landing on the repo's Pages URL sees the raw README rendering, not the designed landing page. The `docs/.nojekyll` file has no effect on a root-sourced site. |
| Assessment | Not broken, but the site's actual front door is hidden one level down. |
| Fixed in this session? | **No.** This session adds a link from `docs/index.html` to the new bathtub page and leaves the root behaviour untouched. Changing `source.path` to `/docs` would fix it properly, but that is a repo-wide publishing decision for the owner. |

### F-05 — `format_probe_score_0.0000_do_not_submit.tif` is a trap file that is nevertheless served — LOW

| | |
|---|---|
| Observed | The file is committed under `docs/downloads/`, so GitHub Pages serves it at a public URL. It is all zeros and its name says "do not submit". |
| Assessment | The naming is good defensive practice. The risk is that it is still a live, downloadable "submission-shaped" file next to real candidates. |
| Fixed in this session? | **No.** Noted only. |

---

## 3. What could **not** be verified, and why

Per the project rule that unverifiable values stay blank and are flagged rather than filled in:

| Item | Why not verified |
|---|---|
| Holdout DTI figures (0.0963, 0.1023, 0.0000, …) | These are the repo's own internal evaluator outputs. Re-running them needs the withheld proxy labels; the repo states the scored truth is not published. **Not independently checkable**, so they are not re-asserted here as true, only transcribed as the repo's claim. |
| "USER-REPORTED" leaderboard scores (0.2477 … 0.2778) | No organizer receipt exists in the repo. The repo says so itself. **Unverified by design.** |
| The 13GEMS covering-lattice probe | The 13GEMS registry raster is git-ignored (`registry/*.tif` in `.gitignore`) and is not in the checkout. Cannot be re-measured from the repo. |
| Whether the candidate would score well on the real leaderboard | No submission receipt. Nothing in this repo can answer it. |
| Nine-focus-site pair overlaps (> 0.70) | The nine `data/focus/*.tif` rasters **are** present, so this **is** re-runnable; it was not re-run in this session because the GEMS audit is outside this task's scope. Flagged as **not measured**, not as false. |

---

## 4. Official sources used in this audit

| Claim | Source |
|---|---|
| Grid/transform convention and the candidate's own byte identity | the repo's bytes themselves (`sha256sum`, `rasterio`), which are primary |
| Everything else in this file | measured locally; no external source was needed |

The bathtub project's external claims, by contrast, are all sourced from official sites and are
listed on the **Sources** page of the site.

---

## 5. Bottom line on the repo

The measured engineering is solid: tests pass, hashes match, ZIPs are byte-identical, the grid is
consistent, and the removed-catalogue discipline is real (0 collisions for both promoted rasters).
The weak point is **prose that outran the data in two places** — a filename that overstates a dot
count by 2.7×, and a FAIL verdict whose stated reason is measurably inverted. In a repo whose value
is auditability, F-02 should be corrected before the next session builds on it.

---

## 6. Change log for this session (for conflict avoidance)

| Path | Status |
|---|---|
| `COORDINATION.md` | **new** |
| `reports/repo-audit-2026-11-06.md` | **new** (this file) |
| `bathtub/` | **new** — data and briefs for the bathtub project |
| `docs/bathtub/` | **new** — the new site |
| `scripts/build_bathtub_site.py`, `scripts/check_bathtub_site.py` | **new** |
| `docs/index.html` | **one nav link added only** — no other change |
| Everything else | **untouched** |
