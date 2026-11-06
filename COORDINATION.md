# COORDINATION.md — Shared Task Board

This file is the coordination point for parallel agent sessions working in this
repository. **Read it before starting any task.** Claim a task by writing your
session ID and file scope in the table, then commit and push the claim
immediately. Never start a task another session has claimed.

## Session register

| Session ID | Branch | Started (UTC) | Last commit (UTC) | Status |
|---|---|---|---|---|
| `arena-a9ed5ccf` | `arena/a9ed5ccf-korea7` (platform-fixed; this session may not create other branches) | 2026-11-06 | — | active |

**Branch note:** the session platform pins this session to
`arena/a9ed5ccf-korea7` and forbids creating/pushing other branches. The
`session-<id>/<task>` branch convention is therefore approximated by
non-overlapping file scopes per task on this single branch. Any session with a
platform-fixed branch should record the same note here.

## Task board

Statuses: `unclaimed` → `in progress` → `needs review` / `done`.
A `needs review` item is published on the site's **Flagged for Review** page and
does not block anything.

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| 0 | Create/operate this coordination file | done | `arena-a9ed5ccf` | `COORDINATION.md` | Claims, log, handoff rules |
| 1 | Repo review (line-by-line, flag irregularities) | done | `arena-a9ed5ccf` | `COORDINATION.md` (findings only), `docs/bath/` (notes page) | Findings in Log entry 2026-11-06 #2; repo irregularity: docs/bath placed beside the existing GEMS site without touching it |
| 2 | Research + verification (quotes, contractors, CSLB licenses, technical background, cost benchmarks) | done | `arena-a9ed5ccf` | `docs/bath/data/*.json` | 8/8 licenses read directly from cslb.ca.gov detail pages 2026-11-06; sources in `docs/bath/data/sources.json`; see Log entry #3 |
| 3 | Executive summary | done | `arena-a9ed5ccf` | `docs/bath/executive-summary.md`, `docs/bath/executive-summary.html` | Numbers generated from/checked against task-2 data by `tests/test_bath_site.py` |
| 4 | Site build (`docs/bath/` dashboard + subpages) + generator + tests | done | `arena-a9ed5ccf` | `docs/bath/**`, `scripts/build_bath_site.py`, `scripts/bath_assets/bath.css`, `tests/test_bath_site.py` | 9 pages; 11 site tests + 84 existing tests all pass |
| 5 | Final integration: re-verify combined data, link check, build | in progress | `arena-a9ed5ccf` | `docs/bath/**` (verify only), `README.md` (additive pointer section only) | Line-by-line re-check + internal/external link audit before PR |
| 6 | PR, merge, confirm GitHub Pages deploy | unclaimed | — | `COORDINATION.md` (log only) | No approval wait; never merge a broken build |

**Rule:** shared outputs (table data, site index/navigation) are edited only by
the final integration session (task 5 owner). If your task needs a file another
session owns, log the request in the Log section below instead of editing it.
If a session's claim is >60 minutes old with no commits, another session may
take over and note the handoff in the Log.

## Project scope (current work package, 2026-11-06)

Bathtub wastewater **overflow trip lever** — stuck inside hidden plumbing behind
a wall in a tenant-occupied San Francisco unit. Overflow/valve assembly is not
reachable from above (5+ licensed plumbers declined); work from below would
require opening the drywall ceiling above a storage unit. Goal: identify
licensed, reviewed plumbers / all-in-one (plumbing + drywall) contractors
serving San Francisco; organize estimates and verified findings.

**Privacy rule (applies to every task):** the client's reasons for scheduling
must never appear on the site, in commit messages, in this file, or in any
public artifact. Permit strategy is not a site topic. Site content stays
neutral: licensed contractors, scope, estimates, verification.

## Verification rules (binding)

1. Every table row on the site carries a **Source link**.
2. Values not confirmable from an official/authoritative source are **left
   blank** and published on the Flagged for Review page. Never infer or
   backfill.
3. Client-provided quote amounts are labeled `client-provided` and are not
   presented as independently verified.
4. CSLB license numbers are included **only** when seen on an official/first-
   party page (CSLB lookup, contractor's own site, or a licensing listing on
   their Yelp/Angi profile), with the lookup link included.
5. Record sources + verification performed per task in the Log below.

## Log

| Time (UTC) | Session | Entry |
|---|---|---|
| 2026-11-06 | `arena-a9ed5ccf` | Created board; claimed tasks 0–4; noted platform-fixed branch constraint. |
| 2026-11-06 | `arena-a9ed5ccf` | **Task 1 (repo review) done.** Findings: (a) repo root contains the unrelated GEMS fault-prospectivity project with a live Pages site; the new bathtub project therefore builds under `docs/bath/` so nothing existing is moved, renamed, or overwritten (root `index.html`-level landing page deliberately NOT replaced — flagged on the site's Flagged for Review page for an owner decision); (b) GEMS lane documents their own flagged conflicts — out of scope here, left untouched; (c) no other sessions had claims (board did not exist before this session). |
| 2026-11-06 | `arena-a9ed5ccf` | **Task 2 (research + verification) done.** Verification performed: every license fact read directly from official CSLB license-detail pages (LicNum 977638, 757796, 1024971, 829071, 1025814, 868994, 1089561, 1140843) on 2026-11-06; B&P §7057 statutory text read from leginfo.legislature.ca.gov; UPC/CPC section titles read from official IAPMO epub readers; Watco official PDFs for trip-lever technique; company identities cross-checked against their own sites, Yelp and BBB listings. Client-provided quote amounts ($614/$550/$135) are labeled client-provided — never presented as verified. Name-to-entity matches for the three quoting companies documented in `docs/bath/data/flags.json` (`flag-name-mapping`) with a request for client confirmation. Irregularities caught during verification (misattributed aggregator licenses, stale BBB expiry, workers' comp exemption, duplicate Yelp listings, second 'Discount Plumbing' entity) all recorded in flags.json. |
| 2026-11-06 | `arena-a9ed5ccf` | **Tasks 3–4 (executive summary + site build) done.** `scripts/build_bath_site.py` renders 9 pages from `docs/bath/data/*.json`; `tests/test_bath_site.py` enforces the project's own rules (every data table row carries an external source link, all internal links resolve, client-provided amounts labeled, no strategy leakage, exec-summary/data consistency) — 11 tests pass; full repo suite 95 passed. |
| 2026-11-06 | `arena-a9ed5ccf` | **Task 5 (integration) started:** line-by-line re-verification of combined data, full link audit, build check, README pointer section. |
