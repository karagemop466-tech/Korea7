# COORDINATION.md — shared task board

> This file is the shared task board for parallel agent sessions working in this repository.
> Claim a task by writing your session ID and file scope here, then commit and push the claim
> immediately. Never start a task another session has claimed. Keep file scopes non-overlapping.

## Session registry

| Session ID | Branch | Role | Status |
|---|---|---|---|
| 524880f1 | `arena/524880f1-korea7` (platform-fixed branch name; used in place of `session-<id>/<task>`) | Worker + final integration for the bathtub overflow trip lever project | active |

## Task board — Bathtub wastewater overflow trip lever project

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| 1 | Requirements collection + executive summary (site content) | done | 524880f1 | `index.html`, `overflow/requirements.html`, `data/overflow/requirements.json` | 12 requirements in 5 categories; sources: Watco S1/S2, Moen S3, Home Depot S4, Family Handyman S5, Lowery S6, Mr. Rooter S7, CSLB S11, sf.gov S12 + user brief |
| 2 | Estimates analysis (3 user-provided estimates) | done | 524880f1 | `overflow/estimates.html`, `data/overflow/estimates.json` | Amounts labeled UNVERIFIED (user-provided, S23); companies verified via Yelp S13/S14/S15 + company site S16; benchmarked against Angi S8, The Overall Plumber S10, Bathify S22 |
| 3 | Service provider research (San Francisco, Yelp + review sources) | done | 524880f1 | `overflow/providers.html`, `data/overflow/providers.json` | 7 detailed providers (P-01..P-07) with canonical Yelp listing links + 5 additional (P-08..P-12) via Yelp search listings (S21) |
| 4 | Analysis & findings (approach, cost benchmark, all-in-one service) | done | 524880f1 | `overflow/analysis.html`, `overflow/sources.html` | Technical analysis S1-S7; cost bands S8/S9/S10/S22; fit matrix + risk register R-1..R-6 |
| 5 | Repo review (line-by-line inventory + irregularities) | done | 524880f1 | `overflow/repo-review.html` | V-1..V-8 checks; irregularities I-1..I-6 (shallow history, divergent prompt files, triplicate run-cards, published do-not-submit artifact, score-label caution, two projects in one repo) |
| 6 | Site build + navigation + verification pass | done | 524880f1 | `index.html`, `overflow/*`, `overflow/assets/*` | Automated check: all local links resolve, all JSON parses, forbidden-content scan clean |
| 7 | Flagged for Review page | done | 524880f1 | `overflow/flagged.html` | F-1..F-9 unverified/blank items + repo irregularities cross-posted |
| 8 | Final integration: PR to `main`, merge, confirm Pages deploy | in progress | 524880f1 | `COORDINATION.md`, `README.md` | Running now |

## File-ownership map (non-overlapping scopes)

| Scope | Owner | Notes |
|---|---|---|
| `COORDINATION.md` | session 524880f1 (created) | Any session may append to the log below; conflicts resolved by merge, never by discarding |
| `index.html`, `overflow/**`, `data/overflow/**` | session 524880f1 | New project site (bathtub overflow trip lever) |
| `README.md` | session 524880f1 (append-only section for the new project) | Existing GEMS content untouched |
| `docs/**`, `gems/**`, `scripts/**`, `tests/**`, `evidence/**`, `registry/**`, `data/**` (except `data/overflow/`) | UNCLAIMED — existing GEMS audit work | Do not edit; created by earlier merged sessions (PRs #1–#19) |

## Rules in force

- Every table row on the site must carry a source link to an official site. Values that cannot be
  confirmed from an official source are left blank and flagged **UNVERIFIED** on the Flagged for
  Review page. Never infer or fill in values.
- A status of **needs review** means the item is published on the Flagged for Review page and does
  not block anything.
- Small, frequent commits. `git pull --rebase` before every push. Merge conflicts are resolved
  without discarding other sessions' work and logged below.
- Shared outputs (site index, navigation, table data) are changed only by the final integration
  session once all other tasks are done.

## Handoff rules

- If a session crashes or its claim is more than 60 minutes old with no commits, any other session
  may take over the task and note the handoff in the log.

## Log

| Date (UTC) | Session | Event |
|---|---|---|
| 2026-11-06 | 524880f1 | Created COORDINATION.md. Claimed tasks 1–7 (bathtub overflow trip lever project). Scope: new site files only (`index.html`, `overflow/**`, `data/overflow/**`); existing GEMS files not touched. |
| 2026-11-06 | 524880f1 | Tasks 1–7 done. Sources: manufacturer (Watco watcomfg.com, Moen solutions.moen.com), official retailer how-to (Home Depot), publisher (Family Handyman), licensed-plumber how-to (Lowery, Mr. Rooter), industry cost data (Angi 2026, The Overall Plumber, InspectandTest, Bathify), government (CSLB cslb.ca.gov, sf.gov), review platform (Yelp listing pages for all 12 providers), user-provided estimate sheet (S23). Full registry: `data/overflow/sources.json` and `overflow/sources.html`. |
| 2026-11-06 | 524880f1 | Verification performed: every table row carries a source link or is explicitly labeled user-provided/blank; automated link check (8 pages, all local links resolve); JSON validity check (4 files); forbidden-content scan (clean); estimate amounts flagged UNVERIFIED (user-provided) rather than confirmed; license numbers left blank where listings did not show them (F-3); company identities independently verified on official listings (S13–S16). |
| 2026-11-06 | 524880f1 | Irregularities recorded (all published on the Flagged for Review page, none blocking): F-1 estimate amounts user-provided; F-2 CSLB #1024971 self-published (verify at CSLB); F-3 missing license numbers blank; F-4 Yelp badges are third-party attestations; F-5 ratings are snapshots; F-6 Dany's SF service area unconfirmed; F-7 Mike's contact blanks; F-8 missing drywall scope line in all three quotes. Repo review irregularities I-1..I-6 recorded in `overflow/repo-review.html`. |
