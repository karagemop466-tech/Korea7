# COORDINATION.md — shared task board

Shared task board for parallel agent sessions working in this repository.
Rules (from the project brief): read this file before starting; claim a task by
writing your session ID and file scope here, then commit and push the claim
immediately; never start a task another session has claimed; keep scopes
non-overlapping; make small frequent commits; run `git pull --rebase` before
every push; log requests to change files owned by another session here instead
of editing them; record sources, verification, and irregularities here when a
task is done; never mark anything verified without linking an official source.

Status values: `unclaimed`, `in progress`, `done`, `needs review`
(`needs review` = published on the site's "Flagged for Review" page; does not
block anything). If a claim is more than 60 minutes old with no commits, any
other session may take over and note the handoff in the log.

## Sessions

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| `d5c5d85b` | `arena/d5c5d85b-korea7` | active | Arena session branch. Platform rules require all work on this exact branch, so the `session-<id>/<task>` branch-naming convention cannot be followed; this branch serves as the session's branch and this deviation is logged here per the conflict rules. |

## Task board

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review and irregularity log | done | `d5c5d85b` | `COORDINATION.md`, Flagged-for-Review page section |
| T2 | Source research and verification: problem description, three 2026-08-30 estimates, cost benchmarks, technical background (overflow/trip lever), San Francisco contractor candidates with reviews and license checks | done | `d5c5d85b` | `trip-lever/**` |
| T3 | GitHub Pages site build: landing page + category subpages (dashboard UI, table format) | done | `d5c5d85b` | `index.html`, `summary.html`, `estimates.html`, `contractors.html`, `findings.html`, `sources.html`, `flagged.html`, `assets/site.css` (fully static site; no JS needed) |
| T4 | Line-by-line verification pass: every table row has an official source link; blanks + flags for unconfirmed values; internal + external link check | done | `d5c5d85b` | `trip-lever/verification.md` |
| T5 | Final integration: re-verify combined data, confirm site builds with no broken links, PR to `main`, merge, confirm GitHub Pages deploy, record PR link here | in progress | `d5c5d85b` | `COORDINATION.md` |

## Sources summary (T1/T2 complete)

- **License authority (official):** CSLB LicenseDetail records fetched 2026-11-06 (data current 11/6/2026) verify
  five active licenses — Expert Plumbing Solutions **#977638** (C-36, exp 2028-10-31, WC insured), Bay Area Plumbing
  **#757796** (C-36, exp 2027-01-31, WC exempt), Fast Response **#1024971** (C-36, exp 2027-03-31, WC insured),
  General SF **#959843** (B + C-10 + C-36, exp 2027-04-30, WC exempt) — all-in-one candidate — and Handyman Heroes
  **#1003394** (B + C-36, exp 2027-05-31, WC insured, complaint disclosure). Szeto: no CSLB record → license left
  blank + flagged. CSLB complaint disclosure for #1003394 fetched and quoted verbatim on the Flagged page.
- **Cost benchmarks:** Angi (3 articles, upd. 2026-07-09/09-18/10-28), This Old House (3 articles, 2026-03-05/05-27/06-01),
  The Overall Plumber (2026-09-10), plus technical guides (Family Handyman, Hunker, Home Depot product reviews,
  Horow, Oatey manufacturer page).
- **Reviews (Yelp):** six business pages + four category searches for San Francisco (Bathtub Repair, Plumbers,
  Handyman Plumbing, Drywall Installation & Repair), values captured 2026-11-06.
- **Company primaries:** official sites of all three quoters + General SF + Handyman Heroes (license numbers on
  company sites match CSLB).
- Full line-by-line source notes: `trip-lever/research.md`.

## Verification summary (T4 complete)

`trip-lever/verification.md` — **PASS**: 7 pages; 0 broken internal/anchor links; 43 unique external URLs, all
accounted for: **31 fetched and content-verified** 2026-11-06, **10 Yelp URLs HTTP 403 to bots** (index-snapshot
confirmed, capture dates shown on site), **2 dead sources dropped** from all active claims and retained only as
labeled documentation rows (SFGate redirect→empty, InspectAndTest HTTP 500; two stale URLs replaced with working
equivalents). 0 unverified URLs, 0 inferred values; all estimate amounts marked owner-provided/unverified with no
source link (none exists); blanks used where confirmation failed (Szeto license).

## Irregularities summary (T1 complete — published on `flagged.html`, 7 items, none blocking)

1–2. Three 2026-08-30 estimates ($614/$550/$135) and all problem-description facts are owner-provided — no official
source → flagged unverified, no links invented. 3. Fast Response CSLB address ≠ Yelp address. 4. Handyman Heroes
CSLB complaint disclosure (citation 2 2020 001045, disclosure-only). 5. Workers'-comp “no employees” exemptions on
Bay Area Plumbing and General SF. 6. Szeto — no CSLB record found. 7. Cross-source drift: Yelp counts, Fast Response
site claim “4.9/1,500” vs Yelp 4.8/906, BBB index-snippet vs CSLB expiry, Handyman Heroes site claims C-10 not on
its CSLB record. Housekeeping: legacy GEMS project remains at `docs/` (noted on Flagged page; legacy files untouched).
Nine-item version with URLs: `trip-lever/research.md` §7.

Shared outputs (site `index.html` and site navigation) are owned by the
integration task T5 (same session in this run — single-session execution).

## Log

- 2026-11-06 — `d5c5d85b` — Session start. `COORDINATION.md` did not exist; created it and claimed T1–T5 in a single non-overlapping scope. No other session had claimed anything at read time.
- 2026-11-06 — `d5c5d85b` — Repo review findings (T1, details published on the site's Flagged for Review page): (a) repository root content belongs to an unrelated legacy project (GEMS fault-prospectivity audit) and its site remains at `docs/`; (b) the new project's landing page takes over the site root `index.html`; (c) the three 2026-08-30 estimates are user-provided and cannot be confirmed from any official source — flagged unverified; (d) GitHub Pages is configured as legacy build from `main`, path `/`.
- 2026-11-06 — `d5c5d85b` — T2 done: research complete (all five CSLB licenses verified active on the official site; official company sites of all three quoters confirmed license numbers; Angi/This Old House/trade cost benchmarks captured; Yelp discovery links prepared). Notes: `trip-lever/research.md`.
- 2026-11-06 — `d5c5d85b` — T3 done: dashboard site built — root `index.html` + `summary.html`, `estimates.html`, `contractors.html`, `findings.html`, `flagged.html`, `sources.html`, styled by `assets/site.css`. All tables in caption-attributed source-linked format.
- 2026-11-06 — `d5c5d85b` — T4 done: `trip-lever/verification.md` PASS — 43/43 external URLs accounted for (31 content-verified, 10 Yelp 403/index-confirmed, 2 dropped and de-cited), 0 broken internal links, 0 inferred values. Dropped sources replaced with working equivalents where possible (Oatey product page, Family Handyman canonical URL).
- 2026-11-06 — `d5c5d85b` — T5 in progress: PR to `main` opened — **https://github.com/karagemop466-tech/Korea7/pull/34** (site commit `4d5f3a3`). Merge + GitHub Pages deploy confirmation next; final status recorded below when done.
