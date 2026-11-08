# Repository audit — 2026-11-08

Generated: 2026-11-08T23:20:42+00:00

## Method and scope

- Every tracked file was inventoried line by line where text-decodable; SHA-256 was computed from saved bytes.
- JSON files were parsed and Python files were AST-parsed. HTML href/src targets were checked against the filesystem; directory targets were checked for index.html.
- Official plumbing claims were re-read from the issuing government/company/manufacturer pages recorded in [research.json](research.json). Legacy GEMS science was preserved, not revalidated.
- This is a static integrity and provenance audit, not a claim that every historical scientific or contractor statement has been independently reverified.

## Inventory

| Category | Files | Source |
|---|---:|---|
| archived-overflow | 60 | [repository](https://github.com/karagemop466-tech/Korea7) |
| canonical-dashboard | 22 | [repository](https://github.com/karagemop466-tech/Korea7) |
| coordination | 1 | [repository](https://github.com/karagemop466-tech/Korea7) |
| current-audit | 6 | [repository](https://github.com/karagemop466-tech/Korea7) |
| legacy-or-other | 226 | [repository](https://github.com/karagemop466-tech/Korea7) |
| shared-summary | 2 | [repository](https://github.com/karagemop466-tech/Korea7) |

Total tracked files: **317**. Text files: **288**. Text lines scanned: **61082**. HTML links checked: **1525**.

## Integrity results

| Check | Result | Source |
|---|---|---|
| JSON parse errors | 0 | [repo_findings.json](repo_findings.json) |
| Python syntax errors | 0 | [repo_findings.json](repo_findings.json) |
| Broken HTML file links | 0 | [repo_findings.json](repo_findings.json) |
| Directory links without index.html | 1 | [repo_findings.json](repo_findings.json) |
| Owner-context privacy matches | 0 | [repo_findings.json](repo_findings.json) |
| Generic compliance-test fixture matches | 0 | [repo_findings.json](repo_findings.json) |

## Irregularities carried to the public Flagged for Review page

| ID | Item | Detail | Source |
|---|---|---|---|
| F18 | Unrelated legacy GEMS project shares the repository | The repo contains a geothermal fault-prospectivity audit alongside plumbing dashboards. Legacy science was preserved, not revalidated as part of this plumbing project. | [source](https://github.com/karagemop466-tech/Korea7/blob/main/README.md) |
| F19 | Multiple archived overflow dashboards | Earlier page sets under bathtub-overflow/, docs/bath/, docs/overflow-* and sf-overflow-audit/ contain older quote/review presentation and provider lists. | [source](https://github.com/karagemop466-tech/Korea7/blob/main/trip-lever/secondary-pages-audit.md) |
| F20 | Stale open PRs #32 and #42 | Both overlap earlier dashboard work and are stale. They were left open and untouched; this session logged a bounded takeover under the 60-minute rule. | [source](https://github.com/karagemop466-tech/Korea7/pull/32) |
| F21 | docs/parallel-index.html links to a directory without an index | docs/results/ exists as a data directory but has no index.html, so a GitHub Pages directory request can fail even though a filesystem link check passes. | [source](https://github.com/karagemop466-tech/Korea7/blob/main/docs/index.html) |
| F22 | Run-card schema drift and stale README leaderboard figures | Multiple run-card JSON schemas and historical GEMS leaderboard statements coexist. They are unrelated to the plumbing decision and were not rewritten. | [source](https://github.com/karagemop466-tech/Korea7/blob/main/README.md) |

## Directory-link findings

| Page | Link | Target | Source |
|---|---|---|---|
| docs/parallel-index.html | `results/` | docs/results | [page](https://github.com/karagemop466-tech/Korea7/blob/main/docs/parallel-index.html) |

## Limitations

- Archived overflow page sets and legacy GEMS artifacts were not edited; they remain available for history and are flagged where they conflict with the current canonical policy.
- File hashes prove byte integrity, not factual correctness. External source verification is recorded separately in research.json and the canonical source ledger.
- A generic compliance-test fixture may contain permit-related wording used only to test publication rules; it is not owner context.
