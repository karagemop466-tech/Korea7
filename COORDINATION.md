# Coordination board — Korea7 / arena/7379ee3c-korea7

Shared task board for parallel agent sessions. Claims are recorded here with session ID, status, and file scope. Never start a task another session has claimed. Scopes must be non-overlapping. Make small, frequent commits; run `git pull --rebase` before every push. On conflict, resolve without discarding the other session's work and log the handoff. When a task finishes, record sources, verification performed, and irregularities here, then mark it done.

Session ID convention: the working branch name, e.g. `arena/7379ee3c-korea7`. Branch for work: `session-<id>/<task>` (this session works directly on `arena/7379ee3c-korea7` since it is the only active session).

## Task legend
- unclaimed / in progress / done / needs review
- "needs review" = published on the Flagged for Review page; does not block other work.

## Tasks

| # | Task | Status | Owner | File scope | Notes |
|---|------|--------|-------|------------|-------|
| 1 | Create COORDINATION.md task board | done | arena/7379ee3c-korea7 | COORDINATION.md | Created at session start. |
| 2 | Repo review line by line; verify from official sources; flag irregularities | in progress | arena/7379ee3c-korea7 | README.md, docs/*, root files | Repo is a GEMS geothermal audit, NOT a plumbing project — flagged as irregularity #1. |
| 3 | Executive summary for the bathtub overflow trip lever project | unclaimed | arena/7379ee3c-korea7 | docs/executive-summary.md (new) | Based on user-supplied estimates dated 8/30/26. |
| 4 | Plumber/contractor research: SF licensed plumbers, Yelp + review sources, CSLB license checks, SF DBI permit info | unclaimed | arena/7379ee3c-korea7 | docs/contractors.md (new), docs/data/contractors.csv (new) | Web research only; no hiring performed. |
| 5 | Site creation: landing page + category subpages, entries/findings tables with source links | unclaimed | arena/7379ee3c-korea7 | docs/index.html, docs/*.html, docs/assets/* | Static HTML; GitHub Pages from /docs (.nojekyll present). |
| 6 | Verification: every table row has an official source link; blanks + "unverified" flags where unconfirmed | unclaimed | arena/7379ee3c-korea7 | all docs pages | No inferred or filled-in values. |
| 7 | Flagged-for-review page with sources for irregularities and unverified items | unclaimed | arena/7379ee3c-korea7 | docs/flagged-review.html (new) | Does not block merge. |
| 8 | Integration: rebuild/re-verify combined data, check site builds with no broken links | unclaimed | arena/7379ee3c-korea7 | all docs pages | Final integration session duties (this session is the only one). |
| 9 | GitHub Pages publish + confirm deploy | unclaimed | arena/7379ee3c-korea7 | repo settings via gh | Confirm deploy succeeds before merge. |
| 10 | Pull request to main + merge + record PR link and result | unclaimed | arena/7379ee3c-korea7 | GitHub PR | Merge without waiting for approval once site is live. |

## Claims & handoffs
- 2026-11-06: session `arena/7379ee3c-korea7` claims tasks 1–10 on branch `arena/7379ee3c-korea7` (only active session). No other sessions detected.

## Verification log
- (empty at session start)
