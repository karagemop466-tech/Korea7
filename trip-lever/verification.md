# Current root-dashboard audit — 2026-11-07

This section supersedes the 2026-11-06 site audit below for the seven root dashboard pages. It does not claim to reverify the unrelated legacy repository, earlier plumbing microsites, or every historical citation. The static dashboard now distinguishes primary sources, third-party review links, and unverified owner reports. No provider was contacted or confirmed.

- Official CSLB records read on 2026-11-07: [Expert Plumbing Solutions](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638), [Bay Area Plumbing](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796), [Fast Response](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971), [General SF](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843), and [Handyman Heroes](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394). Each was current/active, with the classifications shown on the dashboard. General SF and Bay Area Plumbing each reported a no-employees workers' compensation exemption. Handyman Heroes has a [disclosure](https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394).
- Each of the five official company pages on the contractor page was fetched and read on 2026-11-07 for the name, telephone, and advertised service context. [Handyman Heroes](https://www.handymanhero.es/) advertises C-10, but the linked CSLB record lists B and C-36; the difference is flagged, not resolved by inference. [General SF](https://generalsf.com/) advertises commercial, educational and corporate work; its acceptance of this residential project is not assumed.
- [CSLB hiring guidance](https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx) and the [Oatey trip-lever kit](https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste) were fetched and read. They provide context only; they do not establish job-specific conditions or capacity.
- [Yelp Handyman Heroes](https://www.yelp.com/biz/handyman-heroes-san-francisco-5) returned HTTP 403 on direct fetch. Search snippets and review links were used for discovery only, not as verified metrics. No job-specific review was confirmed. Rating/count cells are omitted; no Yelp badge is treated as a license check.
- Estimates and problem facts are owner-provided without written source documents. Reported amounts are clearly identified as unverified in prose; official-confirmed amount cells are blank. CSLB links in those rows identify providers only and do not verify quotes.
- `python -m unittest discover -s tests -p test_dashboard_integrity.py -v` checks the seven pages' local links and anchors, one official contextual source link per body row, blank quote cells, and no-outreach wording. It does not test external availability or prove each claim. External Yelp access remains restricted. The full legacy pytest suite was not run: pytest is not installed in this environment.

## Historical audit (2026-11-06; refers to prior page versions)

# Verification log — Bathtub Overflow Trip Lever site

**Verifier:** session `d5c5d85b` · **Date:** 2026-11-06 (UTC) · **Site pages checked:** `index.html`, `summary.html`, `estimates.html`, `contractors.html`, `findings.html`, `flagged.html`, `sources.html`

Rule applied throughout: **every table row carries a source link; values that could not be confirmed from an
official source are left blank or marked unverified and flagged; nothing is inferred.** A row whose only source is
the owner has no link (none exists) and is flagged instead.

## 1. Link integrity (automated check)

| Check | Result |
|---|---|
| Pages scanned | 7 |
| Internal links (`assets/`, sibling pages, `docs/`) | **all resolve — 0 broken** |
| Anchor links | **0 broken** |
| Unique external URLs on the site | 43 |
| External URLs with fetched-and-read content (status A below) | 31/31 registered URLs |
| External URLs blocked by bot protection (status B) | 10 (all `yelp.com`) |
| Dead URLs kept only as labeled “dropped source” documentation rows (status C) | 2 |
| **External URLs with no verification status** | **0** |

## 2. Status codes

- **A — Content verified:** fetched with content read on 2026-11-06; the claims citing this source were confirmed in
  the fetched text.
- **A (redirected)** — fetched under a different final URL than linked; content read; link kept as the publisher's
  canonical entry. Occurred for `familyhandyman.com/bathroom/…/view-all` → `familyhandyman.com/project/…`
  (the site link was updated to the working canonical URL) and `homeguides.sfgate.com/…` → `weekand.com/…`
  (which then returned an **empty body** → source dropped, see C).
- **B — Access-restricted but indexed:** automated fetch returned **HTTP 403** (bot protection). The exact URL and
  its values were confirmed from search-engine index snapshots of that URL captured 2026-11-06. Human click-through
  works; re-check counts before any decision. All 10 are `yelp.com` URLs.
- **C — Dropped:** fetch failed persistently; the source was **removed from every active claim** on the site and is
  retained only as a labeled documentation row in `sources.html` (and notes below).

## 3. Status A — official/primary sources (content read 2026-11-06)

| # | URL | Confirmed on the fetched page |
|---|---|---|
| A1 | cslb.ca.gov/…/LicenseDetail.aspx?LicNum=977638 | Active C-36; exp 10/31/2028; bond $25k (eff. 2025-09-19); WC insured; “Data current as of 11/6/2026” |
| A2 | …/LicenseDetail.aspx?LicNum=757796 | Active C-36; exp 01/31/2027; bond $25k; WC **exempt “no employees”** (eff. 2024-12-11) |
| A3 | …/LicenseDetail.aspx?LicNum=1024971 | Active C-36 (Joseph Tinsley dba Fast Response); exp 03/31/2027; WC insured (→2026-12-18); CSLB addr 236 W Potral Ave #459 |
| A4 | …/LicenseDetail.aspx?LicNum=959843 | Active **B + C-10 + C-36**; exp 04/30/2027; bond $25k; WC **exempt** (eff. 2025-03-10) |
| A5 | …/LicenseDetail.aspx?LicNum=1003394 | Active **B + C-36**; exp 05/31/2027; WC insured (→2027-04-25); complaint-disclosure pointer present |
| A6 | …/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394 | Citation **2 2020 001045**, 07/12/2020, status “for disclosure only per B&P code 7124.6” (quoted verbatim on flagged page) |
| A7 | …/NameSearch.aspx?NextName=Szeto | **No matching records** → Szeto license cell left blank + flagged (correct per rule) |
| A8 | …/CheckLicense.aspx | Lookup form (published “how to verify” steps) |
| A9 | eplumbingsolutions.com | “License # 977638”; 1465 44th Ave; (415) 531-5340 |
| A10 | bayareaplumbingsf.com | License #757796 stated on site; services; (415) 668-8000 |
| A11 | fastresponseplumbingsf.com | “CSLB #1024971 · C-36”; free in-person estimates; 7 days; company review claim “4.9 · 1,500” (flagged, not adopted as fact) |
| A12 | generalsf.com | Footer “CSLB. 959843”; service categories; (650) 303-1515 |
| A13 | handymanhero.es | Marin & SF plumbing/electrical/handyman; “Licensed GC / C-10 / C-36” claims (C-10 vs CSLB noted in flagged #7); drywall-patching review |
| A14 | angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm | $500–$1,020 (avg $700, $230–$1,170); labor $45–$200/hr; drywall ≈$2,100; unclog $225; water damage $1,350–$6,100 (upd. 2026-09-18) |
| A15 | angi.com/articles/whats-potential-cost-plumbing-leak.htm | $150–$600 (avg $275); drywall/tile adds $300–$930; call-out $50–$200 (upd. 2026-10-28) |
| A16 | angi.com/articles/what-is-overflow-drain.htm | Overflow function/types + trip-lever illustration (upd. 2026-07-09) |
| A17 | thisoldhouse.com/plumbing/how-to-fix-a-bathtub-drain-stopper | Trip lever/plunger/threaded-rod mechanics; 12-step adjust-and-water-test procedure; when to call a pro (2026-05-27) |
| A18 | thisoldhouse.com/plumbing/replacing-bath-tub-drain | W&O system parts; **“For stubborn drains, you may need to access the plumbing from below the tub”**; cut-from-below fallback; 3–4 hr estimate (2026-06-01) |
| A19 | thisoldhouse.com/bathrooms/bathtub-installation-cost | Itemized table: **Overflow $163**, Drain $190; updated 03/05/2026 |
| A20 | familyhandyman.com/project/how-to-convert-bathtub-drain-lever-to-a-lift-and-turn-drain/ | Linkage/stopper-body removal, hacksaw/chisel cut-out, tools (upd. 2024-02-14) |
| A21 | oatey.com/products/P_041193058379/… | Dearborn Plastic Tubular **trip-lever bath waste full kit** (parts A9226/P9226) |
| A22 | theoverallplumber.com/…/bathtub-drain-drama-… | Access routes (panel / small ceiling cut / top-down); durations 2–4 h & 4+ h; costs $80–$200 / $150–$300 / **$300–$600 full W&O**; fill-and-inspect stress test (2026-09-10) |
| A23 | hunker.com/13417812/the-trip-lever-in-my-bathtub-is-stuck/ | Trip-lever definition (mechanism hidden behind wall); stuck causes; cover-plate inspection; full-replacement path (upd. 2020-10-03) |
| A24 | homedepot.com/p/reviews/Everbilt-Trip-Lever…/308507179/1 | “Everbilt Trip Lever … Bath Waste and Overflow” reviews page, 311 reviews (product category exists) |
| A25 | bbb.org/…/expert-plumbing-solutions-1116-458492 | License #977638; not accredited; no complaints last 3 yrs; started 2012; no expiry shown on fetched page (index-snippet discrepancy → flagged #7) |
| A26 | horow.com/blogs/guide/what-is-a-bathtub-overflow-drain-… | **“if you need to replace the whole waste-and-overflow assembly … you usually need access from a panel, the ceiling below, or the wall behind the tub”**; access-plan checklist; fill-above-overflow test from below/panel (page dated 2026-01-05) |

## 4. Status B — Yelp (HTTP 403 to automated fetch; index-confirmed 2026-11-06)

| URL | Values used on site (re-check on decision day) |
|---|---|
| yelp.com/biz/expert-plumbing-solutions-san-francisco | 4.8 ★ (81), page upd. Oct 2026 |
| yelp.com/biz/bay-area-plumbing-san-francisco | 4.8 ★ (175), page upd. Oct 2026 |
| yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3 | 4.8 ★ (906), page upd. Nov 2026; addr 4444 Geary Blvd Ste 203 |
| yelp.com/biz/general-sf-san-francisco-2 | 4.8 ★ (336), page upd. Jun 2026 |
| yelp.com/biz/handyman-heroes-san-francisco-5 | 4.7 ★ (410), page upd. Nov 2026; 1525 Waller St; Verified License badge |
| yelp.com/biz/szeto-plumbing-and-handyman-daly-city-2 | 4.8 ★ (89, Oct 2026); services incl. bathtub/drain/drywall; Daly City; (310) 628-9399 |
| yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA | discovery link |
| yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA | discovery link (URL form appeared verbatim in search index) |
| yelp.com/search?find_desc=Handyman+Plumbing&find_loc=San+Francisco%2C+CA | discovery link (standard Yelp search form) |
| yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA | discovery link (standard Yelp search form) |

**Ratings/reviews are the only figures on the site that depend on Status-B sources** — all other rows use Status-A
sources. Every Yelp figure is labeled with its capture date (2026-11-06).

## 5. Status C — dropped sources (no active claim depends on them)

| Source | Failure observed 2026-11-06 | Handling |
|---|---|---|
| `homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html` | redirected to `weekand.com/…` which returned an **empty body** on two attempts | Removed from research claims; kept only as a labeled “dropped” row in `sources.html` (S31) |
| `inspectandtest.net/guides/bathtub-overflow-drain/` | **HTTP 500** on three attempts | Removed; access/ceiling points re-sourced to This Old House, The Overall Plumber, Horow (all Status A); labeled “dropped” row in `sources.html` (S34) |
| `oatey.com/products/dearborn-brass-triplever-bath-waste-633963408` | **“Page Not Found”** | Replaced everywhere with the working Oatey product URL (A21) |
| `www2.familyhandyman.com/…/view-all` | fetch failed | Replaced with working canonical `familyhandyman.com/project/…` (A20) |

## 6. Unverified / blank register (values NOT confirmed → flagged, never inferred)

| Site row | Field(s) | Status | Where flagged |
|---|---|---|---|
| Estimates #1–3 (`estimates.html`, `summary.html`, `index.html`) | **$614 / $550 / $135** and scopes | Owner-provided 2026-08-30; no official source exists → “unverified” pill, no source link | Flagged #1, #2 |
| Problem snapshot (`index.html`) | stuck lever, 5+ plumbers, below-access, storage unit, tenants, above-preference | Owner-provided 2026-11-06 → “owner-provided” pill | Flagged #1 |
| Contractors Table B — Szeto | **license #**, status, classifications | CSLB name search returned nothing → **cells left blank** | Flagged #6 |
| Contractors Table A — Fast Response | address | CSLB ≠ Yelp → both shown, neither “corrected” | Flagged #3 |
| Contractors Table A/B — Bay Area, General SF | workers' comp | CSLB exemption shown verbatim (“no employees”), not interpreted | Flagged #5 |
| Contractors Table B — Handyman Heroes | complaint status | CSLB disclosure quoted verbatim, not interpreted | Flagged #4 |
| All Yelp rows | rating/review counts | Status-B (403); capture date shown | Flagged #7 |
| Fast Response site claim | “4.9 · 1,500 Reviews” | Company claim, marked unverified; not used as fact | Flagged #7 |
| Site-wide | license facts | CSLB treated as authority over BBB/other aggregators | Flagged #7 |

## 7. Grep audits performed

- Excluded-content sweep over all new site files and `COORDINATION.md` → **no matches** (standing exclusion honored).
- `inspectandtest|www2.familyhandyman|dearborn-brass-triplever|homeguides` → matches occur **only** inside labeled
  “dropped source” documentation rows/notes; zero active citations.
- Internal href check → **0 broken** (§1).
- Every table on every page has a `<caption>` or `<th>`-level source attribution → confirmed by construction; each
  caption either links sources or states “owner-provided — no official source exists”.

## 8. Result

**Status: PASS** — 43/43 external URLs accounted for (31 content-verified, 10 Yelp-restricted & index-confirmed,
2 dead kept only as labeled documentation), 0 broken internal links, 0 unverified URLs without a status,
0 inferred values, excluded content absent from every file.
Flagged items: **7** on `flagged.html` — published, none blocking.
