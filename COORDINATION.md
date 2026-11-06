# Coordination board — Korea7 / arena/7379ee3c-korea7

Shared task board for parallel agent sessions. Claims are recorded here with session ID, status, and file scope. Never start a task another session has claimed. Scopes must be non-overlapping. Make small, frequent commits; run `git pull --rebase` before every push. On conflict, resolve without discarding the other session's work and log the handoff. When a task finishes, record sources, verification performed, and irregularities here, then mark it done.

Session ID convention: the working branch name, e.g. `arena/7379ee3c-korea7`. This session works directly on `arena/7379ee3c-korea7` (only active session); new pages are under `docs/` and do not touch the pre-existing GEMS pages.

## Task legend
- unclaimed / in progress / done / needs review
- "needs review" = published on the Flagged for Review page; does not block other work.

## Tasks

| # | Task | Status | Owner | File scope | Notes |
|---|------|--------|-------|------------|-------|
| 1 | Create COORDINATION.md task board | done | arena/7379ee3c-korea7 | COORDINATION.md | Created at session start; committed 9d80dab. |
| 2 | Repo review line by line; verify from official sources; flag irregularities | done | arena/7379ee3c-korea7 | README.md, docs/*, root files | Irregularity #1: repo is a DOE GEMS geothermal fault-prospectivity audit; the user's project is a bathtub overflow trip lever repair in San Francisco — unrelated content. New plumbing pages added under docs/ without altering GEMS pages. Flagged on overflow-flagged-review.html item 1. |
| 3 | Executive summary for the bathtub overflow trip lever project | done | arena/7379ee3c-korea7 | docs/overflow-executive-summary.html | Problem, 3 user-supplied estimates dated 2026-08-30 ($614/$550/$135), access constraints, tenant-occupied unit, next steps. All prices marked user-supplied/unverified. |
| 4 | Plumber/contractor research: SF licensed plumbers, Yelp + review sources, CSLB license checks, SF DBI permit info | done | arena/7379ee3c-korea7 | docs/overflow-contractors.html, docs/data/overflow-entries.csv | Candidates: Expert Plumbing Solutions #977638, Bay Area Plumbing #757796, Fast Response #1024971 C-36. Yelp ratings from yelp.com search results. License numbers from company sites/BBB/BuildZoom — NOT re-verified on cslb.ca.gov (flagged). SF permit rules from sf.gov. |
| 5 | Site creation: landing page + category subpages, entries/findings tables with source links | done | arena/7379ee3c-korea7 | docs/plumbing-index.html, overflow-*.html, docs/index.html nav link | Dashboard + 7 subpages; every table row carries a source link; design matches assets/site.css; internal link check passed. |
| 6 | Verification: every table row has an official source link; blanks + "unverified" flags where unconfirmed | done | arena/7379ee3c-korea7 | all docs pages | Estimate prices: blank official-source confirmation, flagged UNVERIFIED (user-supplied). CSLB statuses flagged; third-party sources cited. No inferred values. |
| 7 | Flagged-for-review page with sources for irregularities and unverified items | done | arena/7379ee3c-korea7 | docs/overflow-flagged-review.html | 6 flagged items with source links and suggested actions; values-left-blank table. Does not block merge. |
| 8 | Integration: rebuild/re-verify combined data, check site builds with no broken links | in progress | arena/7379ee3c-korea7 | all docs pages | Internal link check passed (0 missing). External key sources reachable: cslb.ca.gov Check a License page, sf.gov permit pages. Yelp pages fetch with 403 from sandbox but are listed as third-party links only. |
| 9 | GitHub Pages publish + confirm deploy | unclaimed | arena/7379ee3c-korea7 | repo Pages setting (/docs) | Repo has docs/.nojekyll; confirm Pages enabled and deploy succeeds. |
| 10 | Pull request to main + merge + record PR link and result | unclaimed | arena/7379ee3c-korea7 | GitHub PR | Create PR from arena/7379ee3c-korea7 to main, merge without waiting once site is live. |

## Claims & handoffs
- 2026-11-06: session `arena/7379ee3c-korea7` claims tasks 1–10 on branch `arena/7379ee3c-korea7` (only active session). No other sessions detected. No handoffs.

## Verification log
- 2026-11-06: internal link audit across all 9 new/existing HTML files — 0 broken internal links.
- 2026-11-06: official sources confirmed reachable — cslb.ca.gov Check a License page; sf.gov/apply-plumbing-and-mechanical-permit; sf.gov/apply-kitchen-or-bath-remodel-permit; SF Building Code via amlegal (106A, 104.2).
- 2026-11-06: Yelp data captured via web search (yelp.com search pages 403 on direct fetch in this sandbox; treated as third-party listing, not official verification).
- Irregularities flagged: repo content mismatch; estimates user-supplied/unverified (3); Expert Plumbing Solutions #977638 possibly expired per BBB (10/31/2026 pre-dates 2026-11-06); no license re-verified on official CSLB record; Yelp "Verified License" badges are not CSLB verification.
