# Verification log — 2026-11-07 · session `7e5f723c`

Scope: re-verify the published bathroom-job pages line by line against official sources, rebuild the site from
verified data, and record exactly what was checked, what failed, and what was left blank.

Canonical outputs: repository-root `index.html`, `summary.html`, `estimates.html`, `contractors.html`,
`findings.html`, `plan.html`, `sources.html`, `flagged.html`, generated from `data/overflow/*.json` by
`scripts/build_overflow_site.py`, enforced by `tests/test_overflow_site.py`.

## 1. Official sources read directly (all successful)

| Source | URL | What was taken |
|---|---|---|
| CSLB licence detail #977638 | https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638 | current and active; Corporation; issued 10/09/2012; expires 10/31/2028; C-36; bond $25,000 eff. 09/19/2025; WC insured 07/19/2026–07/19/2027; record stamped “Data current as of 11/7/2026” |
| CSLB #757796 | …LicNum=757796 | current and active; Sole Ownership; 01/07/1999; exp 01/31/2027; C-36; bond $25,000 eff. 09/01/2026; WC **exempt** (“no employees”, eff. 12/11/2024) |
| CSLB #1024971 | …LicNum=1024971 | current and active; Joseph Tinsley dba Fast Response Plumbing and Rooter; 03/20/2017; exp 03/31/2027; C-36; bond $25,000 eff. 09/01/2026; WC insured 12/18/2025–12/18/2026; address printed “236 W POTRAL AVE #459” |
| CSLB #829071 | …LicNum=829071 | current and active; Corporation; 12/18/2003 (reissued 06/07/2007); exp 06/30/2027; C-36, A, C-4, C16, B, C10; bond $25,000 eff. 09/04/2026; WC 07/13/2026–07/13/2027 |
| CSLB #1025814 | …LicNum=1025814 | current and active; The Genteel Plumbers Inc; 04/14/2017; exp 04/30/2027; C-36 + B; bond $25,000 eff. 01/01/2023; WC 01/24/2026–01/24/2027 |
| CSLB #959843 | …LicNum=959843 | current and active; GENERALSF; 04/12/2011; exp 04/30/2027; B, C10, C36; bond $25,000 eff. 04/30/2025; WC **exempt** (eff. 03/10/2025) |
| CSLB #1003394 | …LicNum=1003394 | current and active; Handyman Heroes Inc; 05/05/2015; exp 05/31/2027; B + C36; bond $25,000 eff. 09/01/2026; WC 04/25/2026–04/25/2027; **complaint disclosure exists** |
| CSLB #868994 | …LicNum=868994 | current and active; Atlas Plumbing & Rooter; 12/08/2005 (reissued 03/25/2008); exp 03/31/2028; C36 + A; WC via employee service group 07/01/2026–07/01/2027 |
| CSLB #1089561 | …LicNum=1089561 | current and active; Taro Group Inc dba Heises Plumbing; 04/06/2022; exp 04/30/2028; C36, C10, A, C20; bond $25,000 eff. 05/27/2025; WC 01/11/2026–01/11/2027 |
| CSLB #1140843 | …LicNum=1140843 | current and active; Discount Plumbing Rooter Services LLC; 07/22/2025; exp 07/31/2027; C36 + A; bond $25,000 + LLC employee bond $100,000; WC 04/01/2025–04/01/2027; liability $2,000,000 |
| CSLB name search “Szeto” | https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/NameSearch.aspx?NextName=Szeto&NextLicNum= | No record for “Szeto Plumbing and Handyman” → licence left blank, flagged F14 |
| CSLB — hire a contractor | https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx | Licence check, three written bids, insurance verification, 10%/$1,000 down-payment limit |
| CSLB — B classification | …Licensing_Classifications_Detail.aspx?Class=B | Definition and two-unrelated-trades rule |
| CSLB — C-36 classification | …Licensing_Classifications_Detail.aspx?Class=C36 | Plumbing scope text |
| BPC §7048 | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048 | $1,000 threshold + “does not require a building permit”; amended by Stats. 2025 ch. 67 (AB 1170), eff. 2026-01-01 |
| BPC §7057 | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057 | General building contractor definition and prime-contract rule |
| Angi — drain replacement | https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm | $500–$1,020 (avg $700); +$1,350–$6,100 where drywall/unclog/water damage involved; drywall ≈$2,100; unclogging $225; page updated 2026-09-18 |
| Angi — bathroom leak | https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm | $150–$600 (avg $275); drywall/tile add-ons $300–$930; labour $45–$200/h; call-out $50–$200; up to $4,000 for hidden pipes; page updated 2026-10-28 |
| This Old House | https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain | “For stubborn drains, you may need to access the plumbing from below the tub”; cut-out from below in extreme cases |

## 2. Company sites read directly

| Site | Result |
|---|---|
| https://www.aceplumbingandrooter.com/ | Licence #829071 with the same six classifications as CSLB; HOA/property-manager practice text |
| https://generalsf.com/ | “CSLB. 959843”; building/plumbing/electrical services; since 1991; commercial/institutional client description |
| https://www.fastresponseplumbingsf.com/commercial-services | CSLB #1024971; HOA/apartment/property-manager practice; “4.9 · 1,500 reviews” marketing claim |
| https://www.handymanhero.es/plumbing-services/plumbing/ | Address 912 Cole St #202; lists “'B', C-10, C-36” — **C-10 is not on the CSLB record** (F7) |
| https://www.genteelplumbers.com/ | Founded 2016, Outer Sunset; SF + San Mateo County service area; same-day/24-7 |
| https://www.atlasplumbingandrooter.com/ | Since 2005; site phone (415) 849-2346 vs CSLB (650) 871-9863 |
| https://www.heisesplumbing.com/ | Licence #1089561 linked; links its own Yelp business page; advertises property repairs, electrical, appliances |
| https://plumbinginsf.com/ | Discount Plumbing Rooter Services; since 1992; site phone (415) 702-1079 vs CSLB (650) 991-2100 |

## 3. What could not be verified (and how it is published)

| Item | Result | Handling |
|---|---|---|
| Yelp business pages | HTTP 403 to automated requests (as in earlier sessions) | Ratings/counts taken from search-engine snapshots of those pages on 2026-11-07, dated in place, links given; flags F12/F13 |
| The three quote amounts | No official source exists | Amount shown as supplied, tagged “owner-provided”; “Official confirmation” column left blank; flag F2 |
| Quote → entity mapping | Shorthand names only | Matched by name/trade/city; flag F3 |
| Szeto licence | No CSLB record found | Licence cells blank; flag F14 |
| Discount entity match | Address of record Burlingame vs SF listing | Flag F15 |
| Job-specific experience | No register exists | Flag F16 |
| Heise's Yelp value | Read from search listing, not business page | Flag F10 |

## 4. Repository review

- Root previously served a dashboard (session `d5c5d85b`); `docs/` holds the unrelated GEMS geothermal project;
  three other overflow page-sets exist (`docs/bath/`, `docs/overflow-*.html`, `docs/plumbing-index.html`,
  `bathtub-overflow/`). All preserved; only root pages are canonical. Flagged F17.
- `README.md` carries a banner pointing to this project; the GEMS section is unchanged.
- `EXECUTIVE-SUMMARY.md` was rewritten to mirror the verified site data (previously listed six candidates and
  carried statements not re-verified in this pass).
- Earlier-session claims that could not be re-verified today were **dropped**, not carried forward (F18).

## 5. Automated checks

- `python3 scripts/build_overflow_site.py` — deterministic rebuild (test asserts identical output).
- `python3 -m pytest tests/test_overflow_site.py` — 18 tests, all passing on 2026-11-07:
  data shapes; licence-or-blank rule; all-in-one firms genuinely hold B + C-36; flag cross-references;
  every source has URL + read status; internal links and anchors resolve; every table row carries a link or an
  owner-provided/unverified label; contractor and benchmark rows carry external links; amounts appear with
  provenance; banned permit-strategy/confidentiality phrasing absent; summary numbers match data files;
  HTML tag balance; no placeholders; unique titles.
- Internal link audit: 8 pages, 0 broken internal links or anchors (test-enforced).
