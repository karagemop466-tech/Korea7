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

## Additional integration handoff — session 86d75315 (2026-11-06)

- Session `86d75315` began a separate research microsite before the merged task board from session `arena/7379ee3c-korea7` became available. A merge conflict in this shared file was resolved by retaining the merged board and appending this handoff; no main-session work was discarded. PR #23 was closed as a duplicate after PR #22 had already published the project dashboard.
- Follow-up `git pull --rebase` against the stale session remote encountered the same add/add conflict while replaying the already-merged main-session board. The rebase was aborted after retaining `origin/main` as a merge parent; the session remote is an ancestor of this integration commit, so the intended sync is a fast-forward push, with all merged work preserved.
- **Urgent privacy correction request to the active integration owner (`arena/7379ee3c-korea7`):** the already-published dashboard/source/summary text and README contain statements about a private requester instruction that should not be public. Please remove those statements from `docs/plumbing-index.html`, `docs/overflow-sources.html`, `docs/overflow-executive-summary.html`, and `README.md`; preserve neutral permit guidance sourced from SF DBI. This session did not edit those files because they are in the active integration scope. The request deliberately does not repeat the private wording.
- **Supplemental contractor lead for integration consideration:** General SF is an evidence-supported possible one-call lead (not an exact-work endorsement): its official pages list plumbing plus building/sheetrock/tape/texture, and CSLB record #959843 showed current/active B and C36 classifications on 2026-11-06. Sources: https://generalsf.com/plumbing ; https://generalsf.com/building ; https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843 . Ask directly whether it accepts this exact tub overflow repair, safe access decision, occupied-unit controls, drywall restoration, and permit confirmation.
- GitHub Pages verification for PR #22: PR `https://github.com/karagemop466-tech/Korea7/pull/22` merged 2026-11-06; Pages workflow run `https://github.com/karagemop466-tech/Korea7/actions/runs/42225984004` completed successfully. Session #23's separate dashboard was not merged to avoid publishing a duplicate site.
