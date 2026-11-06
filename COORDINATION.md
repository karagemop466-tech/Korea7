# COORDINATION.md — shared task board

> This file is the shared task board for parallel agent sessions. A status of `needs review`
> means the item is published on the "Flagged for Review" page and does **not** block anything.

**Last updated:** 2026-11-06T13:45Z

## Session registry

| Session ID | Branch | Task | Status |
|---|---|---|---|
| `arena-e6f84d88` | `arena/e6f84d88-korea7` | Bathtub overflow trip-lever project + repo audit + site | in progress |

## Task board

| ID | Task | Status | Owner | Files in scope (exclusive) |
|---|---|---|---|---|
| T1 | Coordination + repo review | in progress | arena-e6f84d88 | `COORDINATION.md`, `reports/repo-audit-2026-11-06.md` |
| T2 | Requirements register (full list) | in progress | arena-e6f84d88 | `bathtub/data/requirements.json` |
| T3 | Official-source registry + verification log | in progress | arena-e6f84d88 | `bathtub/data/sources.json` |
| T4 | Estimates / bid comparison data | in progress | arena-e6f84d88 | `bathtub/data/estimates.json` |
| T5 | Contractor shortlist (CSLB-verified) | in progress | arena-e6f84d88 | `bathtub/data/contractors.json` |
| T6 | Technical/mechanism notes | in progress | arena-e6f84d88 | `bathtub/data/technical.json` |
| T7 | Compliance matrix (permit, lead, asbestos, tenant access) | in progress | arena-e6f84d88 | `bathtub/data/compliance.json` |
| T8 | Flagged-for-review register | in progress | arena-e6f84d88 | `bathtub/data/flagged.json` |
| T9 | Site generator + link checker | in progress | arena-e6f84d88 | `scripts/build_bathtub_site.py` |
| T10 | Site build (landing + 7 subpages) | in progress | arena-e6f84d88 | `docs/bathtub/**` |
| T11 | Nav link from existing site | in progress | arena-e6f84d88 | `docs/index.html` (single nav addition only) |
| T12 | Integration: PR to main, merge, Pages deploy check | unclaimed | — | — |

## Scope rules

* Every table row on the site carries a `source_url` pointing at an **official** site
  (`*.ca.gov`, `*.gov`, `ecfr.gov`, `leginfo.legislature.ca.gov`, `codelibrary.amlegal.com`
  for SF Municipal Code, `cslb.ca.gov`, `epa.gov`).
* Rows whose value cannot be confirmed from an official source stay **blank** and are
  listed on **Flagged for Review**.
* Owner-supplied facts (three quotes, site observations) are recorded as
  `owner_reported` — never presented as externally verified.
* `docs/index.html` is shared output. This session only **adds one nav link**; it does not
  restructure the GEMS audit pages. That is logged here as an integration-scope change.

## Change log

### 2026-11-06T13:45Z — arena-e6f84d88 — claim
Created board. Claimed T1–T11. Created `bathtub/`, `docs/bathtub/`.
No other sessions active at claim time (repo had no `COORDINATION.md`; `git log` shows a
single merge commit `91a0cbf`).

### 2026-11-06T13:50Z — arena-e6f84d88 — scope note / conflict avoidance
The repo is a **DOE GEMS geothermal competition audit** (Python + static site under `docs/`).
The request in this session is a **bathtub overflow trip-lever** procurement/repair project.
These are unrelated subject areas. To avoid destroying existing work:

* The GEMS site, data, tests and artifacts are **not modified** (only one nav link added).
* All new work lives under `bathtub/` (data) and `docs/bathtub/` (site) — new directories,
  non-overlapping with any existing file.
* The repo review is written to `reports/repo-audit-2026-11-06.md` and published at
  `docs/bathtub/repo-audit.html`.

### 2026-11-06T14:05Z — arena-e6f84d88 — irregularity found in repo (logged, not fixed)
`README.md` and `docs/index.html` state the relay-corridor lane has **30,000 dots**
("korea7-k7-offcatalogue-relay-corridor-30000dots"). Measured from the committed raster:
**10,944 non-zero cells**. Logged as F-01 on Flagged for Review. Not fixed by this session
because the GEMS files are outside this session's scope.

## Blocked / needs human input

| Item | Why blocked | What unblocks it |
|---|---|---|
| Yelp review verification | `yelp.com` returns HTTP 403 to automated fetches | Owner opens the Yelp search links on the Vendors page |
| Contractor "no-permit" willingness | Not publishable / not verifiable | Owner asks on the phone; CSLB does not publish this |
| Whether the stalled overflow/plunger is actually stuck vs. seized | Needs on-site inspection | Any licensed C-36 plumber's on-site diagnosis |
