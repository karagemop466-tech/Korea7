# COORDINATION.md — shared task board

> **Repo:** `karagemop466-tech/Korea7` · **Session branch:** `arena/e8f4f286-korea7`
> **Project:** Bathtub wastewater overflow trip lever — collect, organize and analyze a full
> list of requirements; source and verify a San Francisco plumber/contractor; publish a clean
> GitHub Pages dashboard.
> **Session ID:** `e8f4f286-korea7`
> **Last updated:** 2026-11-06

## Standing rules (owner brief)

1. Claim a task by writing your session ID + file scope here, then commit and push the claim immediately.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping: each session edits only the files in its claimed scope.
4. If a task needs a file owned by another session, log the request here — do not edit it.
5. Small, frequent commits; run `git pull --rebase` before every push.
6. On a merge conflict: stop, resolve without discarding the other session's work, and log it.
7. Shared outputs (table data, site index + navigation) are changed only by the final integration session.
8. Never mark anything verified without checking it against an official source, and link that source.
9. A `needs review` item is published on the Flagged for Review page and does not block.
10. If a session crashes or its claim is >60 min old with no commits, any session may take over and note the handoff.
11. Owner-restricted internal details are never published on the site, in email, or in any public artifact.

## Task board

| Task | Status | Session | File scope | Notes |
|---|---|---|---|---|
| T1 Coordination + repo review | in progress | e8f4f286-korea7 | `COORDINATION.md`, `site/repo-review.html` | Repo review verifies the Korea7/GEMS claims against the official DrivenData competition page. |
| T2 Requirements | in progress | e8f4f286-korea7 | `site/data/project-brief.md`, `site/requirements.html` | Requirements are owner-supplied; each row cites the brief extract or an official rule. |
| T3 Estimates | in progress | e8f4f286-korea7 | `site/estimates.html` | 3 owner-reported quotes; prices flagged UNVERIFIED (no official confirmation). |
| T4 Vendor sourcing | in progress | e8f4f286-korea7 | `site/vendors.html` | SF vendors from Yelp listings; license badges recorded as shown on Yelp. |
| T5 Regulatory reference | in progress | e8f4f286-korea7 | `site/regulatory.html` | Official CSLB C-36 + SF.gov DBI references. |
| T6 Verification + flagged + sources | in progress | e8f4f286-korea7 | `site/verification.html`, `site/flagged-review.html`, `site/sources.html` | Per-row source map; flagged items published, non-blocking. |
| T7 Site shell + integration | in progress | e8f4f286-korea7 | `site/index.html`, `site/executive-summary.html`, `site/assets/*` | Final integration session: merge, re-verify, confirm build, publish. |

## Claim log

| Time (UTC) | Session | Task | Scope claimed | Commit |
|---|---|---|---|---|
| 2026-11-06 | e8f4f286-korea7 | T1–T7 | all `site/**` + `COORDINATION.md` | initial claim |

## Handoffs / conflicts

- No other session has claimed work in this checkout. This session owns all `site/**` files and
  `COORDINATION.md`. Non-overlapping by construction (single writer).

## Verification performed (rolling)

| Item | Checked against | Result |
|---|---|---|
| GEMS competition identity, end date, prize pool, submission limit | DrivenData competition 306 (official) | Confirmed |
| CSLB C-36 classification scope | cslb.ca.gov classification detail (official) | Confirmed |
| SF kitchen/bath permit requirement + minimum valuations | sf.gov DBI service page (official) | Confirmed |
| Owner-reported prices ($614 / $550 / $135) | no official source available | **UNVERIFIED** |
| Yelp vendor ratings/review counts | yelp.com listing pages | Recorded as shown; dynamic |

## Irregularities flagged for review

See `site/flagged-review.html`. Summary:

1. All three quoted prices are owner-reported and cannot be confirmed from an official source.
2. The repo's GEMS leaderboard scores are user-reported; no organizer receipt exists in the repo.
3. The repo's 13GEMS covering-lattice rule is saturated (>99% overlap for every dotted raster).
4. Yelp ratings/review counts are dynamic and were captured on 2026-11-06.
