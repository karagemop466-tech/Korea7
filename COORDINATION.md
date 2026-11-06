# COORDINATION.md — shared task board

Session protocol: read this file before starting work. Claim a task by writing your session ID and file scope here, then commit and push the claim immediately. Never start a task another session has claimed. Keep scopes non-overlapping. Small, frequent commits. `git pull --rebase` before every push. Status values: `unclaimed`, `in progress`, `done`, `needs review` (needs review = published on the Flagged for Review page; does not block anything).

**Branch note (platform constraint):** this session runs on the Arena-managed branch `arena/d6a1ea39-korea7`. Platform rules forbid creating/pushing other branches, so the `session-<id>/<task>` branch convention cannot be used by this session. All claims below are owned by session `arena-d6a1ea39` on that branch. Other sessions must claim their own scopes here before editing files.

## Session registry

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| arena-d6a1ea39 | `arena/d6a1ea39-korea7` | active | Sole session at bootstrap (no prior claims existed). Acts as author + integration session. |

## Task board

| Task ID | Task | Status | Owner | Files (scope) | Notes |
|---|---|---|---|---|---|
| T1 | Bootstrap COORDINATION.md task board | done | arena-d6a1ea39 | `COORDINATION.md` | Created at session start; no prior file existed. |
| T2 | Repo review line-by-line; flag irregularities | in progress | arena-d6a1ea39 | `docs/plumbing/repo-audit.md` | Auditing README/claims vs files; sources linked. |
| T3 | Requirements list + executive summary | unclaimed | — | `docs/plumbing/executive-summary.html`, `docs/plumbing/requirements.html` | |
| T4 | Estimates intake (3 quotes, 2026-08-30) | unclaimed | — | `docs/plumbing/estimates.html`, `docs/plumbing/data/estimates.json` | User-provided values; verify existence of companies from official sources. |
| T5 | Technical access analysis (above vs below, drywall) | unclaimed | — | `docs/plumbing/access-analysis.html` | |
| T6 | Plumber/vendor research (SF, reviews) | unclaimed | — | `docs/plumbing/plumbers.html` | Yelp + official sites + license lookups. |
| T7 | Site shell: landing page, nav, CSS, link from main index | unclaimed | — | `docs/plumbing/index.html`, `docs/plumbing/assets/plumbing.css`, `docs/index.html` (single link insertion only) | |
| T8 | Verification + Flagged for Review page | unclaimed | — | `docs/plumbing/verification.html`, `docs/plumbing/flagged.html` | Every table row: source link or flagged unverified. |
| T9 | Integration: link check, PR to main, merge, Pages deploy, record results | unclaimed | — | `COORDINATION.md`, PR via `gh` | Final integration session. |

## Request log (cross-scope changes)

(No requests yet.)

## Irregularities log

(To be filled by T2 and T8.)

## Completion log

(To be filled by T9: sources, verification performed, PR link, merge result, Pages status.)
