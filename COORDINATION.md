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
| `session-arena-68d76eff` | `arena/68d76eff-korea7` | `COORDINATION.md`, `EXECUTIVE-SUMMARY.md`, `index.html`, `bathtub-overflow/**`, `.nojekyll`, `assets/**` | active | 2026-11-06 |

> **Platform constraint (logged 2026-11-06):** this session's agent runtime pins all work to
> branch `arena/68d76eff-korea7` (branched from `main` @ `91a0cbf`). The runtime does not
> permit creating or pushing other branches, so the `session-<id>/<task>` branch convention
> cannot be followed literally. Conflicts are instead avoided by strict file scopes as listed
> above. Any other session should take different file scopes or take over claims per the
> 60-minute handoff rule.

## Task board

| # | Task | Status | Owner | Files touched | Sources / verification / notes |
|---|---|---|---|---|---|
| 1 | Repo review — inspect existing repo contents, flag irregularities | in progress | `session-arena-68d76eff` | `COORDINATION.md` (log only) | see log below |
| 2 | Verify client-provided estimates (3 companies: identity, license, official sites) | in progress | `session-arena-68d76eff` | `bathtub-overflow/estimates.html`, data rows | see log below |
| 3 | Verify official rules: SF permit requirements + CSLB licensing thresholds | in progress | `session-arena-68d76eff` | `bathtub-overflow/permits-compliance.html` | see log below |
| 4 | Research and verify candidate service providers (plumbing + drywall access, SF, occupied unit) | unclaimed | — | `bathtub-overflow/providers.html` | depends on #3 |
| 5 | Build static GitHub Pages site (landing + category subpages, tables, flagged page) | unclaimed | — | `index.html`, `bathtub-overflow/**`, `assets/**` | depends on #2–#4 |
| 6 | Final integration — re-verify combined data, confirm build + no broken links, PR to `main`, merge, confirm Pages deploy | unclaimed | — | `main` via PR | depends on #5 |

## Cross-session edit requests

| Requested by | File needed | Owning session | Status |
|---|---|---|---|
| — | — | — | — |

## Handoffs / conflict log

| Time (UTC) | Session | Event |
|---|---|---|
| 2026-11-06 | `session-arena-68d76eff` | Board created; tasks #1–#3 claimed. No other claims present at board creation. |
