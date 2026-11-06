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
| 1 | Requirements collection + executive summary (site content) | in progress | 524880f1 | `index.html`, `overflow/requirements.html`, `overflow/executive-summary.html`, `data/overflow/*.json` | Research from official manufacturer/industry sources |
| 2 | Estimates analysis (3 user-provided estimates) | in progress | 524880f1 | `overflow/estimates.html` | Values are USER-PROVIDED; company identity verified where possible |
| 3 | Service provider research (San Francisco, Yelp + review sources) | in progress | 524880f1 | `overflow/providers.html` | Every row must carry a source link |
| 4 | Analysis & findings (approach, cost benchmark, all-in-one service) | in progress | 524880f1 | `overflow/analysis.html`, `overflow/sources.html` | |
| 5 | Repo review (line-by-line inventory + irregularities) | in progress | 524880f1 | `overflow/repo-review.html` | Does not modify existing GEMS files |
| 6 | Site build + navigation + verification pass | in progress | 524880f1 | `index.html`, `overflow/*`, `overflow/assets/*` | Link check before merge |
| 7 | Flagged for Review page | in progress | 524880f1 | `overflow/flagged.html` | Unverified items do not block merge |
| 8 | Final integration: PR to `main`, merge, confirm Pages deploy | unclaimed | — | — | Runs after tasks 1–7 |

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
