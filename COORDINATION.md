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
| 1 | Repo review (line-by-line, flag irregularities) | in progress | `arena-a9ed5ccf` | `COORDINATION.md` (findings only), `docs/bath/` (notes page) | Repo contains unrelated GEMS project; do not modify it |
| 2 | Research + verification (quotes, contractors, CSLB licenses, technical background, cost benchmarks) | in progress | `arena-a9ed5ccf` | `docs/bath/data/*.json` | Every value source-linked; unverified → blank + flag |
| 3 | Executive summary | in progress | `arena-a9ed5ccf` | `docs/bath/executive-summary.md`, `docs/bath/executive-summary.html` | Derived from task 2 data only |
| 4 | Site build (`docs/bath/` dashboard + subpages) + generator + tests | in progress | `arena-a9ed5ccf` | `docs/bath/**`, `scripts/build_bath_site.py`, `tests/test_bath_site.py` | Static, no JS build step; link-checked |
| 5 | Final integration: re-verify combined data, link check, build | unclaimed | — | `docs/bath/**` (verify only), `README.md` (additive pointer section only) | To be done by this session after 1–4 complete, re-checked line by line |
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
