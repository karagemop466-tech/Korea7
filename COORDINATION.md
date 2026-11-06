# COORDINATION.md — Shared Task Board

This is the shared task board for all agent sessions working in this repository.
Protocol (summary): read this file before starting; claim a task by writing your session ID and
file scope here, then **commit and push the claim immediately**; never start a task another
session has claimed; keep scopes non-overlapping; make small, frequent commits; run
`git pull --rebase` before every push; if a merge conflict occurs, stop, resolve it without
discarding the other session's work, and log what happened here; when a task is finished,
record its sources, verification performed, and irregularities here and mark it **done**;
a status of **needs review** means the item is published on the site's "Flagged for Review"
page and does not block anything; never mark anything verified without checking it against
an official source and linking that source; takeover of a stalled claim (60+ minutes with no
commits) must be noted here as a handoff.

## Session registry

| Session ID | Branch | File scope | Status | Last activity (UTC) |
|---|---|---|---|---|
| `session-arena-68d76eff` | `arena/68d76eff-korea7` (platform-pinned; cannot create session-* branches) | `COORDINATION.md`, `EXECUTIVE-SUMMARY.md`, `index.html`, `bathtub-overflow/**` | all claimed tasks done | 2026-11-06 |

> **Platform constraint (logged 2026-11-06):** this session's agent runtime pins all work to
> branch `arena/68d76eff-korea7` (branched from `main` @ `91a0cbf`). The runtime does not
> permit creating or pushing other branches, so the `session-<id>/<task>` branch convention
> cannot be followed literally. Conflicts are instead avoided by strict file scopes as listed
> above (flag F13 on the site's Flagged for Review page). Any other session should take
> different file scopes or take over claims per the 60-minute handoff rule.

## Task board

| # | Task | Status | Owner | Files touched | Sources / verification / notes |
|---|---|---|---|---|---|
| 1 | Repo review — inspect existing repo contents, flag irregularities | done | `session-arena-68d76eff` | `COORDINATION.md`, site Flagged-for-Review page (F1–F2) | Findings: repo contained a separate pre-existing DOE GEMS fault-prospectivity audit (≈15 MB GeoTIFFs, Python code, its own `/docs/` Pages site); untouched by this project. GitHub Pages was enabled (`main` root) but no root `index.html` existed → site root served no landing page; fixed by this project. Three run-card JSON variants (`run-card.json`, `run_card.json`, `run-card-korea7-e3.json`) — pre-existing inconsistency, noted only. |
| 2 | Verify client-provided estimates (3 companies) | done | `session-arena-68d76eff` | `bathtub-overflow/estimates.html` | Expert Plumbing Solutions: official site eplumbingsolutions.com shows Lic #977638 → CSLB record read 2026-11-06: active C-36, 1465 44th Ave SF (matches). Fast Response Plumbing & Rooter: official site shows CSLB #1024971 → CSLB record read 2026-11-06: active C-36, Joseph Tinsley dba, 236 W Portal Ave ("POTRAL" typo in CSLB record). Bay Area Plumbing: official site bayareaplumbingsf.com displays no license number → **left blank, flagged F3**; Yelp "Verified License" badge treated as third-party only. Quote amounts are client-provided → flagged F7 (no official source can confirm private quotes). |
| 3 | Verify official rules (SF permits + CSLB licensing) | done | `session-arena-68d76eff` | `bathtub-overflow/permits-compliance.html` | sf.gov "Apply for a plumbing and mechanical permit" (permit needed before cutting into/replacing pipes in walls; exemptions SF Plumbing Code §104.2; homeowner route only for stand-alone single-family dwellings). sf.gov "Register with the City as a licensed contractor" (C-4/C-36 for plumbing permits). B&P §7048 read on leginfo.legislature.ca.gov — **current text (AB 1170, eff. 2026-01-01): exemption under $1,000 AND no building permit required**; outdated "$500" third-party claims flagged F12. CPC §104.2 exemption text via IAPMO (publisher reference). CSLB classification pages B / B-2 / C-36 read for trade-scope rules. |
| 4 | Research and verify candidate providers | done | `session-arena-68d76eff` | `bathtub-overflow/providers.html` | 6 providers: Ace Plumbing & Rooter #829071 (active; A, B, C-4, C-10, C-16, C-36 — all-in-one capable), GENERALSF #959843 (active; B, C-10, C-36 — all-in-one capable; **WC exemption "no employees" → flag F6**), Expert Plumbing Solutions #977638, Fast Response #1024971 (**CSLB future-relevant note: WC policy exp. 12/18/2026; address typo → flag F9**), Advanced Plumbing & Drain #1009195 (**CSLB future-suspension warning → flag F5**; 3 published phone numbers → F10), Bay Area Plumbing (license unverified → F3). All CSLB License Detail records read 2026-11-06 ("Data current as of 11/6/2026" per CSLB). Yelp listings linked per owner request; ratings point-in-time → F11. |
| 5 | Build static GitHub Pages site (landing + category subpages, tables, flagged page) | done | `session-arena-68d76eff` | `index.html`, `bathtub-overflow/**` | 10 pages (root dashboard + 9 subpages), shared stylesheet, zero JS, responsive tables. Every table row carries source links; unverified values left blank + flagged. Internal-link check run across all 32 repo HTML pages: **no broken links**. Flag counts cross-checked (12 flags). |
| 6 | Final integration — re-verify combined data, confirm build + no broken links, PR to `main`, merge, confirm Pages deploy | done | `session-arena-68d76eff` | PR `arena/68d76eff-korea7` → `main` | Re-verified: license numbers re-checked against CSLB detail pages (same session, 2026-11-06); internal links re-checked post-edit (script: hrefs/src resolved against repo files — 0 broken); page count and flag counts consistent (12). PR created and merged (recorded in Handoffs log). Pages deploy confirmed via GitHub Pages API (`status: built/live`). Result recorded below. |

## Cross-session edit requests

| Requested by | File needed | Owning session | Status |
|---|---|---|---|
| — | — | — | — |

## Handoffs / conflict log

| Time (UTC) | Session | Event |
|---|---|---|
| 2026-11-06 | `session-arena-68d76eff` | Board created; tasks #1–#3 claimed. No other claims present at board creation. |
| 2026-11-06 | `session-arena-68d76eff` | Tasks #4–#6 claimed and executed sequentially (single-session integration; no competing claims detected via `git fetch` before each push). |
| 2026-11-06 | `session-arena-68d76eff` | Merge: PR opened from `arena/68d76eff-korea7` → `main` and merged without waiting for approval per owner instruction; Pages deploy confirmed. PR link recorded in the final commit message and EXECUTIVE-SUMMARY.md site link. |

## Verification & irregularity summary (final integration record)

- **Verification performed:** every provider row's license number/classification/status read from official CSLB License Detail pages (retrieved 2026-11-06); permit and statute text read from sf.gov, leginfo.legislature.ca.gov, cslb.ca.gov classification pages, and IAPMO (publisher); company facts read from the companies' own official sites; Yelp data point-in-time 2026-11-06. Unverifiable values (private quotes; Bay Area Plumbing license; drywall cost) left blank and flagged.
- **Flagged irregularities (12, published on the site's Flagged for Review page):** F1 repo hosts unrelated GEMS project; F2 Pages root previously lacked a landing page (fixed); F3 Bay Area Plumbing license unverified; F4 no-permit posture vs. official SF guidance (owner decision; no private circumstances documented anywhere); F5 Advanced Plumbing future-suspension warning; F6 GENERALSF workers'-comp exemption; F7 quotes client-provided; F8 no drywall quote (blank); F9 Fast Response CSLB typo + WC expiry 12/18/2026; F10 Advanced Plumbing phone-number mismatch; F11 Yelp data point-in-time / 403 on direct fetch; F12 outdated $500 threshold citations.
- **Site build:** static HTML/CSS, no build step; internal-link integrity script reported 0 broken links across all 32 HTML pages before push and again after final edits.
