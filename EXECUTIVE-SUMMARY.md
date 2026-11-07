# Executive Summary — Bathtub Wastewater Overflow Trip Lever (San Francisco)

**Project:** free a seized bathtub overflow trip lever inside concealed waste-and-overflow plumbing, in a
tenant-occupied San Francisco unit, with one provider covering plumbing **and** drywall.
**Verified:** 2026-11-07 · **Session:** `7e5f723c` · **Canonical site:** <https://karagemop466-tech.github.io/Korea7/>
(dashboard · executive summary · shortlist · estimates · contractors · analysis · hiring plan · verification log · sources · flagged)
**Data + build:** `data/overflow/*.json` → `scripts/build_overflow_site.py` → ten root pages ·
**Tests:** `tests/test_overflow_site.py`

> The canonical deliverable is the site. This file is a plain-markdown mirror of its executive summary.
> Every value that could not be confirmed from an official source is either left blank or explicitly
> tagged; the full list is on the site's [Flagged for review](flagged.html) page (18 items).

---

## 1. The situation

The trip lever is seized inside the concealed waste-and-overflow assembly. Access from above has already
failed: the owner reports that more than five licensed plumbers declined to force it for fear of destroying
the hidden plumbing. The reported fallback is access from below, through the ceiling of the storage unit
underneath — which means opening and later patching drywall while tenants remain in the building.

*Owner-provided. No public source exists for a private building's plumbing.*

## 2. The three quotes — 2026-08-30

| Company | Scope as quoted | Amount as stated | Official confirmation |
|---|---|---:|---|
| [Expert Plumbing Solutions](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638) — CSLB #977638 | Replacing waste and overflow | $614 | *blank — owner-provided, no official source* |
| [Bay Area Plumbing](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796) — CSLB #757796 | Replace lever for the plug and spout with diverter, labour + materials | $550 | *blank — owner-provided, no official source* |
| [Fast Response Plumbing & Rooter](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971) — CSLB #1024971 | Repair or adjust bathtub wastewater plunger handle | $135 | *blank — owner-provided, no official source* |

The spread reflects **scope, not competitiveness**: adjustment attempt → trim/diverter replacement →
concealed waste-and-overflow replacement. **None of the three includes the drywall work**, and none is a
combined plumbing-plus-drywall price.

## 3. What is established (re-read 2026-11-07)

| Point | What the source says | Source |
|---|---|---|
| Licences | 10 of 11 candidates read “current and active”; the eleventh (Szeto) has no matching CSLB record and its licence fields are left blank | [CSLB — Check a license](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx) |
| Single-contract capability | Four firms hold **B General Building + C-36 Plumbing** on one licence: Ace Plumbing & Rooter, Genteel Plumbers, General SF, Handyman Heroes | [BPC §7057](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057) |
| Below-tub access | “For stubborn drains, you may need to access the plumbing from below the tub”; in extreme cases the old drain is cut out from below | [This Old House](https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain) |
| Drain replacement cost | $500–$1,020 nationally in 2026 (average $700) — the band the $550 and $614 quotes sit inside | [Angi, upd. 2026-09-18](https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm) |
| Drywall cost | ≈$2,100 to install drywall where a wall is opened; $300–$930 for patching after a leak | [Angi, upd. 2026-10-28](https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm) |
| Licensing threshold | Licensing law does not apply below $1,000 aggregate price **and** where the work does not require a building permit (BPC §7048, amended eff. 2026-01-01) | [BPC §7048](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048) |

## 4. Recommendation

1. **Send one identical written scope** to the four B + C-36 firms — the scope checklist is on the site's
   [Hiring plan](plan.html) page. CSLB recommends at least three written bids on identical scope.
2. **Ask how they will reach the assembly before discussing price.** The access route, cut location and cut
   size belong in the quote.
3. **Price the drywall as its own line** on the same contract (benchmark ≈$2,100 when a wall opens).
4. **Verify the licence number on the written bid** on CSLB, and read the complaint disclosure if one exists.
5. **Keep payment inside the legal limit** — no more than 10% of the contract price or $1,000, whichever is
   less, as a down payment unless a blanket performance and payment bond is on file
   ([CSLB guidance](https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx)).

## 5. Open items (full detail on the site)

- Quote amounts are owner-provided and unverifiable (F2); shorthand names were mapped to licensed entities (F3).
- Two candidates show workers'-compensation exemptions on CSLB (F4, F5); one carries a complaint disclosure (F6).
- One vendor's site lists a classification its CSLB record does not show (F7).
- One candidate has no CSLB record at all (F14); one Yelp listing is not clearly matched to its licence (F15).
- Yelp ratings are dated snapshots and Yelp blocks automated reads (F12, F13).
- Job-specific experience in occupied units cannot be verified from an official source (F16).

## 6. Repository note

This repository also contains an unrelated legacy project (a geothermal fault-prospectivity analysis under
`docs/`) and three superseded draft page-sets for this same bathroom job (`docs/bath/`, `docs/overflow-*.html`,
`docs/plumbing-index.html`, `bathtub-overflow/`). Nothing was deleted; only the repository-root pages are
canonical. See flag F17 in `COORDINATION.md` and on the site.
