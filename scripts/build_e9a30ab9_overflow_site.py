#!/usr/bin/env python3
"""Build the verified bathtub-overflow trip-lever dashboard for session arena/e9a30ab9-korea7.

Output directory: overflow-trip-lever-e9a30ab9/ (HTML dashboard, assets, data/*.json,
EXECUTIVE-SUMMARY.md, REPO-REVIEW.md).

Rules enforced by this generator (and checked by tests/test_e9a30ab9_overflow_site.py):
  * every <tbody> row carries at least one link to an official source (https://...);
  * any value that could not be confirmed from an official source is rendered as an
    empty cell carrying an explicit UNVERIFIED flag — values are never inferred;
  * requester-provided statements are shown only as clearly attributed prose, never
    as verified table values;
  * the output is deterministic (no run-time timestamps), so `--check` can prove the
    committed output matches the generator.

Usage:
  python3 scripts/build_e9a30ab9_overflow_site.py            # write the site
  python3 scripts/build_e9a30ab9_overflow_site.py --check    # verify committed output is current
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR_NAME = "overflow-trip-lever-e9a30ab9"
SESSION = "arena/e9a30ab9-korea7"
READ_DATE = "2026-11-07"
BRIEF_DATE_HEADING = "8/30/26"
MAIN_SHA = "9b9cbaa8c24b11d8c5945cffa82fe799a20179fe"  # origin/main reviewed (PR #45)
GH_BLOB = f"https://github.com/karagemop466-tech/Korea7/blob/{MAIN_SHA}/"
SITE_TITLE = "Bathtub Overflow Trip Lever — Verified Dashboard (San Francisco)"

# ---------------------------------------------------------------------------
# Sources (every one of these was opened directly on READ_DATE unless noted)
# ---------------------------------------------------------------------------
CSLB_DETAIL = "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
CSLB_CLASS = "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class="

SOURCES: dict[str, dict] = {
    "cslb-check": dict(
        label="CSLB — Check a License (official lookup)",
        url="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx",
        publisher="Contractors State License Board (CA)", kind="Official — government",
        verifies="Entry point used for every license record below; CSLB publishes license status, classifications, bond and workers' compensation data — it does not publish job prices or reviews."),
    "cslb-c36": dict(label="CSLB classification C-36 Plumbing Contractor", url=CSLB_CLASS + "C36",
                     publisher="CSLB", kind="Official — government",
                     verifies="Official definition of the C-36 plumbing trade."),
    "cslb-b": dict(label="CSLB classification B General Building Contractor", url=CSLB_CLASS + "B",
                   publisher="CSLB", kind="Official — government",
                   verifies="Official definition of the B general building classification."),
    "cslb-c9": dict(label="CSLB classification C-9 Drywall Contractor", url=CSLB_CLASS + "C-9",
                    publisher="CSLB", kind="Official — government",
                    verifies="Official definition of the C-9 drywall trade."),
    "cslb-hire": dict(label="CSLB — Finding the right contractor (consumer guide)",
                      url="https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx",
                      publisher="CSLB", kind="Official — government",
                      verifies="Consumer rules: $25,000 contractor bond; down payment capped at 10% or $1,000 (whichever is less); verify workers' compensation and liability insurance."),
    "bpc-7048": dict(label="California Business & Professions Code § 7048",
                     url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048",
                     publisher="California Legislative Information", kind="Official — government",
                     verifies="Minor-work exemption from contractor licensing: aggregate contract price under $1,000 (as amended by AB 1170, effective 2026-01-01); the exemption does not apply where a building permit is required or where the person employs others."),
    "bpc-7057": dict(label="California Business & Professions Code § 7057",
                     url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057",
                     publisher="California Legislative Information", kind="Official — government",
                     verifies="Definition of a Class B general building contractor: a contract must involve at least two unrelated building trades or crafts other than framing/carpentry, unless the contractor holds (or subcontracts to) the relevant specialty license."),
    "civ-1954": dict(label="California Civil Code § 1954 (landlord entry to make repairs)",
                     url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954",
                     publisher="California Legislative Information", kind="Official — government",
                     verifies="A landlord may enter to make necessary or agreed repairs; reasonable written notice (24 hours presumed reasonable) stating date, approximate time and purpose; entry during normal business hours unless the tenant consents; landlord and tenant may agree orally to an entry for agreed repairs within one week."),
    "sf-plumbing-permit": dict(label="SF.gov — Apply for a plumbing and mechanical permit",
                               url="https://www.sf.gov/apply-plumbing-and-mechanical-permit",
                               publisher="City and County of San Francisco (DBI)", kind="Official — government",
                               verifies="City guidance on when a plumbing permit is required (including before cutting into or replacing pipes behind walls, with exemptions listed in SF Plumbing Code § 104.2) and which license classes may apply (A; B subject to conditions; C-4; C-36; C-16; C-20; C-54). DBI Help Desk 628-652-4900."),
    "sf-kb-permit": dict(label="SF.gov — Apply for a kitchen or bath remodel permit",
                         url="https://www.sf.gov/apply-kitchen-or-bath-remodel-permit",
                         publisher="City and County of San Francisco (DBI)", kind="Official — government",
                         verifies="City guidance for bathroom work; for R-2 apartment buildings the property owner may perform drywall/sheetrock work but must hire licensed contractors for plumbing and electrical."),
    "oatey": dict(label="Oatey — Dearborn plastic tubular trip-lever bath waste (manufacturer specification)",
                  url="https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste",
                  publisher="Oatey Co. (manufacturer)", kind="Official — manufacturer",
                  verifies="Component identification: a trip-lever bath waste is a full waste-and-overflow kit (e.g., Part #A9226 UPC 041193058379 black polypropylene; Part #P9226 UPC 041193057099 white polypropylene) with a chrome-finish trip-lever stopper assembly."),
    "generalsf": dict(label="General SF — Building services page (company site)", url="https://generalsf.com/building",
                      publisher="General SF (official company site)", kind="Official — company",
                      verifies="Company advertises both plumbing (rough and finish) and sheetrock / tape and texture; site references CSLB #959843."),
    "handyman": dict(label="Handyman Heroes — Handyman services page (company site)", url="https://www.handymanhero.es/handyman-services/",
                     publisher="Handyman Heroes Inc (official company site)", kind="Official — company",
                     verifies="Company advertises sheetrock and wall repairs and plumbing services."),
    "ace": dict(label="Ace Plumbing & Rooter — home page (company site)", url="https://www.aceplumbingandrooter.com/",
                publisher="Ace Plumbing & Rooter (official company site)", kind="Official — company",
                verifies="Company states license classes A, B, C-4, C-10, C-16, C-36 and lists HOA / property-manager services; no drywall service statement was seen on the page viewed."),
    "yelp": dict(label="Yelp business page (third-party review platform) — retrieval attempt",
                 url="https://www.yelp.com/biz/general-sf-san-francisco-2",
                 publisher="Yelp (third-party; not an official source)", kind="Third-party — not official",
                 verifies="Nothing. Automated retrieval returned HTTP 403 on 2026-11-07, so no rating or review count is published anywhere on this site. Listed only to document the attempt."),
}

CSLB_RECORDS: list[dict] = [
    dict(key="expert", group="quoted", name="EXPERT PLUMBING SOLUTIONS", lic="977638",
         addr="1465 44th Avenue, San Francisco, CA 94122", phone="(415) 531-5340", entity="Corporation",
         issued="10/09/2012", expires="10/31/2028", status="Current and active", classes=["C-36"],
         bond_surety="Atlantic Specialty Insurance Company", bond_no="800209947", bond_amt="$25,000",
         wc="Insured", wc_carrier="Everest Premier Insurance Company", wc_policy="7600025915261", wc_exp="07/19/2027", wc_exempt_eff=None,
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
    dict(key="bayarea", group="quoted", name="BAY AREA PLUMBING", lic="757796",
         addr="335 14th Avenue, San Francisco, CA 94118", phone="(415) 668-8000", entity="Sole Ownership",
         issued="01/07/1999", expires="01/31/2027", status="Current and active", classes=["C-36"],
         bond_surety="Atlantic Specialty", bond_no="800268354", bond_amt="$25,000",
         wc="Exempt", wc_carrier=None, wc_policy=None, wc_exp=None, wc_exempt_eff="12/11/2024",
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
    dict(key="fast", group="quoted", name="JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER", lic="1024971",
         addr="236 W POTRAL AVE #459, San Francisco, CA 94127 (street name exactly as printed on the CSLB record)", phone="(415) 596-6115", entity="Sole Ownership",
         issued="03/20/2017", expires="03/31/2027", status="Current and active", classes=["C-36"],
         bond_surety="Atlantic Specialty", bond_no="800273981", bond_amt="$25,000",
         wc="Insured", wc_carrier="Employers Preferred", wc_policy="EIG576950801", wc_exp="12/18/2026", wc_exempt_eff=None,
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
    dict(key="generalsf", group="allinone", name="GENERALSF", lic="959843",
         addr="3624 Irving Street Suite A, San Francisco, CA 94122", phone="(650) 303-1515", entity="Sole Ownership",
         issued="04/12/2011", expires="04/30/2027", status="Current and active", classes=["B", "C-10", "C-36"],
         bond_surety="Business Alliance", bond_no="G150306734690", bond_amt="$25,000",
         wc="Exempt", wc_carrier=None, wc_policy=None, wc_exp=None, wc_exempt_eff="03/10/2025",
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco",
         site_src="generalsf", site_claim="Official site lists “Rough and Finish Plumbing” and “Sheetrock / Tape and Texture” among building services."),
    dict(key="handyman", group="allinone", name="HANDYMAN HEROES INC", lic="1003394",
         addr="912 Cole Street #202, San Francisco, CA 94117", phone="(844) 382-4376", entity="Corporation",
         issued="05/05/2015", expires="05/31/2027", status="Current and active", classes=["B", "C-36"],
         bond_surety="Western Surety", bond_no="89021781", bond_amt="$25,000",
         wc="Insured", wc_carrier="Omaha National", wc_policy="ONCC0701424403", wc_exp="04/25/2027", wc_exempt_eff=None,
         disclosure="Complaint disclosure on file: Citation #2 2020 001045 dated 07/12/2020 (disclosed under B&P § 7124.6)", city="San Francisco",
         site_src="handyman", site_claim="Official site lists “sheetrock and wall repairs” and “plumbing” among handyman services."),
    dict(key="ace", group="allinone", name="ACE PLUMBING & ROOTER", lic="829071",
         addr="1090 Bryant Street, San Francisco, CA 94103", phone="(415) 824-6444", entity="Corporation",
         issued="12/18/2003", expires="06/30/2027", status="Current and active", classes=["C-36", "A", "C-4", "C-16", "B", "C-10"],
         bond_surety="Merchants Bonding", bond_no="101993376", bond_amt="$25,000",
         wc="Insured", wc_carrier="Financial Pacific", wc_policy="10147545585", wc_exp="07/13/2027", wc_exempt_eff=None,
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco",
         site_src="ace", site_claim="Official home page states classes A, B, C-4, C-10, C-16, C-36 and HOA / property-manager services; no drywall service statement seen."),
    dict(key="genteel", group="allinone", name="THE GENTEEL PLUMBERS INC", lic="1025814",
         addr="1181 Revere Avenue, San Francisco, CA 94124", phone="(833) 436-8335", entity="Corporation",
         issued="04/14/2017", expires="04/30/2027", status="Current and active", classes=["C-36", "B"],
         bond_surety="American Contractors", bond_no="100343809", bond_amt="$25,000",
         wc="Insured", wc_carrier="Technology Insurance", wc_policy="TES4729399", wc_exp="01/24/2027", wc_exempt_eff=None,
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
    dict(key="rapidflow", group="allinone", name="RAPID FLOW PLUMBING & ROOTER INC", lic="1115649",
         addr="230 Edinburgh Street, San Francisco, CA 94112", phone="(415) 866-8401", entity="Corporation",
         issued="01/29/2024", expires="01/31/2028", status="Current and active", classes=["B", "C-36"],
         bond_surety="Merchants Bonding", bond_no="101423907", bond_amt="$25,000",
         wc="Exempt", wc_carrier=None, wc_policy=None, wc_exp=None, wc_exempt_eff="02/03/2026",
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
    dict(key="mannys", group="allinone", name="MANNY'S PLUMBING & ROOTER", lic="841229",
         addr="41 Midvale Drive, Daly City, CA 94015", phone="(650) 207-5733", entity="Sole Ownership",
         issued="06/21/2004", expires="06/30/2028", status="Current and active", classes=["C-36", "B"],
         bond_surety="Merchants Bonding", bond_no="101892287", bond_amt="$25,000",
         wc="Exempt", wc_carrier=None, wc_policy=None, wc_exp=None, wc_exempt_eff="06/28/2026",
         disclosure="No complaint-disclosure link shown on the license detail page", city="Daly City (adjacent to San Francisco)"),
    dict(key="heises", group="other", name="TARO GROUP INC dba HEISES PLUMBING", lic="1089561",
         addr="1610 Evans Avenue, San Francisco, CA 94124", phone="(415) 333-0704", entity="Corporation",
         issued="04/06/2022", expires="04/30/2028", status="Current and active", classes=["C-36", "C-10", "A", "C-20"],
         bond_surety="American Contractors", bond_no="100963071", bond_amt="$25,000",
         wc="Insured", wc_carrier="Employers Preferred", wc_policy="EIG6235466", wc_exp="01/11/2027", wc_exempt_eff=None,
         disclosure="No complaint-disclosure link shown on the license detail page", city="San Francisco"),
]
for _r in CSLB_RECORDS:
    SOURCES[f"cslb-{_r['lic']}"] = dict(
        label=f"CSLB license detail #{_r['lic']} — {_r['name']}", url=CSLB_DETAIL + _r["lic"],
        publisher="CSLB", kind="Official — government",
        verifies=f"Business name, address, phone, entity, issue/expiry dates, status, classifications, bond and workers' compensation data (CSLB data-current stamp {READ_DATE}).")
SOURCES["cslb-complaint-1003394"] = dict(
    label="CSLB complaint disclosure for license #1003394 (Handyman Heroes Inc)",
    url="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394",
    publisher="CSLB", kind="Official — government",
    verifies="Citation #2 2020 001045 dated 07/12/2020 is publicly disclosed under B&P § 7124.6.")

REC = {r["key"]: r for r in CSLB_RECORDS}
DISPLAY = {
    "expert": "Expert Plumbing Solutions", "bayarea": "Bay Area Plumbing",
    "fast": "Fast Response Plumbing and Rooter (Joseph Tinsley dba)", "generalsf": "General SF",
    "handyman": "Handyman Heroes Inc", "ace": "Ace Plumbing & Rooter", "genteel": "The Genteel Plumbers Inc",
    "rapidflow": "Rapid Flow Plumbing & Rooter Inc", "mannys": "Manny's Plumbing & Rooter",
    "heises": "Heises Plumbing (Taro Group Inc dba)",
}

# ---------------------------------------------------------------------------
# Requester-provided brief (verbatim where quoted). Not an official source.
# ---------------------------------------------------------------------------
BRIEF_PROBLEM = [
    "The bathtub wastewater overflow trip lever is stuck inside the concealed plumbing behind the bathroom wall of a tenant-occupied unit in San Francisco.",
    "The overflow sits in a hard-to-access location; reaching the plumbing may require opening drywall.",
    "More than five licensed plumbers have declined to remove the lever from above because of the risk of damaging the hidden plumbing; all recommended working from below.",
    "Below the bathroom is a storage unit; access from below may require opening that unit's drywall ceiling.",
    "Removing the overflow from above remains the preferred approach if it can be done safely.",
    "One provider is wanted for both the plumbing and the drywall work, experienced in delicate work while tenants occupy the unit.",
]
ESTIMATES = [
    dict(n=1, rec="expert", brief_name="Expert plumbing solutions",
         scope="Remove bathtub wastewater overflow trip lever — “Replacing waste and overflow”", amount_reported="$614"),
    dict(n=2, rec="bayarea", brief_name="Bay Area plumbing",
         scope="“Replace lever for the bathtub plug and spout with diverter includes labor and materials”", amount_reported="$550"),
    dict(n=3, rec="fast", brief_name="Fast response",
         scope="“repair or adjust bath tub wastewater plunger handle”", amount_reported="$135"),
]

# ---------------------------------------------------------------------------
# Small HTML helpers
# ---------------------------------------------------------------------------
def esc(t) -> str:
    return html.escape(str(t), quote=True)


def a(url: str, label: str) -> str:
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


def src(*ids: str) -> str:
    return "<br>".join(a(SOURCES[i]["url"], SOURCES[i]["label"]) for i in ids)


def pill(kind: str, text: str) -> str:
    return f'<span class="pill {kind}">{esc(text)}</span>'


def blank(note: str) -> str:
    return f'<td class="blank">{pill("unverified", "UNVERIFIED")}<small>{esc(note)}</small></td>'


def td(content: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return f"<td{c}>{content}</td>"


def tdt(text: str, cls: str = "") -> str:
    return td(esc(text), cls)


def table(tid: str, headers: list[str], rows: list[list[str]], caption: str = "") -> str:
    cap = f"<caption>{esc(caption)}</caption>" if caption else ""
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "\n".join("<tr>" + "".join(r) + "</tr>" for r in rows)
    return (f'<div class="tablewrap"><table id="{tid}">{cap}<thead><tr>{th}</tr></thead>'
            f"<tbody>\n{body}\n</tbody></table></div>")


def gh(path: str, lines: str = "") -> str:
    label = f"{path} {lines}" if lines else path
    return a(GH_BLOB + path + (f"#{lines}" if lines else ""), f"{label} @ main {MAIN_SHA[:7]}")


# ---------------------------------------------------------------------------
# Derived helpers for CSLB rows
# ---------------------------------------------------------------------------
def classes_text(r: dict) -> str:
    return ", ".join(r["classes"])


def has_b(r: dict) -> bool:
    return "B" in r["classes"]


def wc_text(r: dict) -> str:
    if r["wc"] == "Insured":
        return f"Insured — {r['wc_carrier']} policy {r['wc_policy']}, expires {r['wc_exp']}"
    return f"Exempt — licensee certified it has no employees (effective {r['wc_exempt_eff']})"


def bond_text(r: dict) -> str:
    return f"{r['bond_amt']} contractor's bond — {r['bond_surety']} #{r['bond_no']}"


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("requirements.html", "Requirements"),
    ("estimates.html", "Estimates"),
    ("contractors.html", "Contractors"),
    ("compliance.html", "Licensing & compliance"),
    ("repo-review.html", "Repo review"),
    ("verification.html", "Verification log"),
    ("sources.html", "Sources"),
    ("flagged-for-review.html", "Flagged for review"),
]


def layout(page: str, title: str, lead: str, body: str) -> str:
    nav_parts = []
    for href, label in NAV:
        active = ' class="active"' if href == page else ""
        nav_parts.append(f'<a href="{href}"{active}>{esc(label)}</a>')
    nav = "".join(nav_parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(SITE_TITLE)}</title>
<meta name="description" content="{esc(lead)}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html">Overflow trip lever · SF</a>
    <nav aria-label="Site">{nav}</nav>
  </div>
</header>
<main class="wrap">
  <h1>{esc(title)}</h1>
  <p class="lead">{esc(lead)}</p>
{body}
</main>
<footer class="wrap foot">
  <p>Session <code>{esc(SESSION)}</code> · generated by <code>scripts/build_e9a30ab9_overflow_site.py</code> · official sources read directly on {READ_DATE}.
  Blank cells marked <span class="pill unverified">UNVERIFIED</span> mean no official source confirmed the value; nothing is inferred.
  License data changes — re-check the linked CSLB record on the day of hiring. This site is organised information, not legal advice.</p>
</footer>
</body>
</html>
"""


CSS = """:root{--bg:#f5f7fa;--card:#fff;--ink:#1b2430;--mute:#5b6775;--line:#dde3ea;--brand:#0b5fff;--ok:#1f7a3a;--warn:#9a6700;--bad:#b42318;--info:#175cd3}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
header.top .wrap{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{font-weight:700;color:var(--ink);text-decoration:none;white-space:nowrap}
nav{display:flex;flex-wrap:wrap;gap:4px}
nav a{color:var(--mute);text-decoration:none;padding:6px 10px;border-radius:8px;font-size:14px}
nav a:hover{background:var(--bg);color:var(--ink)}nav a.active{background:var(--brand);color:#fff}
main{padding:26px 20px 40px}h1{margin:0 0 6px;font-size:28px}h2{margin:34px 0 10px;font-size:21px}h3{margin:22px 0 8px;font-size:17px}
.lead{color:var(--mute);margin:0 0 18px;font-size:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.card h3{margin:0 0 6px;font-size:16px}.card p{margin:0;color:var(--mute);font-size:14px}
.card a.more{display:inline-block;margin-top:10px;color:var(--brand);text-decoration:none;font-weight:600}
.stat{display:flex;flex-direction:column;gap:2px}.stat .n{font-size:30px;font-weight:700;color:var(--brand)}.stat .l{color:var(--mute);font-size:13px}
.note{background:#fff8e6;border:1px solid #f3dc9a;border-radius:10px;padding:12px 14px;margin:14px 0}
.note.info{background:#eef4ff;border-color:#c7d7fe}.note.ok{background:#eefbf1;border-color:#b7e4c3}
.tablewrap{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:12px;margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}caption{text-align:left;padding:10px 12px;font-weight:600;color:var(--mute)}
th,td{padding:9px 11px;border-top:1px solid var(--line);vertical-align:top;text-align:left}
thead th{background:#f0f3f7;border-top:0;position:sticky;top:0;font-size:12.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--mute)}
tbody tr:hover{background:#fafbfd}td.blank{background:#fffaf0}td.blank small{display:block;color:var(--mute);margin-top:4px}
td a,li a,p a{color:var(--brand)}
.pill{display:inline-block;font-size:11.5px;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
.pill.ok{background:#e6f6ea;color:var(--ok);border-color:#b7e4c3}.pill.warn{background:#fff4d6;color:var(--warn);border-color:#f3dc9a}
.pill.bad{background:#fde8e6;color:var(--bad);border-color:#f5b5ae}.pill.info{background:#e8f0fe;color:var(--info);border-color:#c7d7fe}
.pill.unverified{background:#fff1d6;color:#8a5a00;border-color:#f0c36d}.pill.mute{background:#eef1f4;color:var(--mute);border-color:#dde3ea}
ul.tight li{margin:4px 0}code{background:#eef1f4;padding:1px 5px;border-radius:5px;font-size:13px}
.foot{color:var(--mute);font-size:13px;padding:10px 20px 40px;border-top:1px solid var(--line)}
.muted{color:var(--mute)}
@media (max-width:640px){h1{font-size:23px}nav a{padding:5px 8px}}
"""


# ---------------------------------------------------------------------------
# Requirements register
# ---------------------------------------------------------------------------
REQUIREMENTS = [
    dict(id="R1", cat="Problem", req="Free or remove a bathtub wastewater overflow trip lever that is seized inside the concealed waste-and-overflow plumbing behind the bathroom wall.",
         basis="Requester-stated condition. Component type confirmed against the manufacturer specification: a trip-lever bath waste is a complete waste-and-overflow assembly with a trip-lever stopper, so the seized part sits inside the overflow/waste tube.",
         status=("info", "Requester-stated; component type verified"), srcs=["oatey"]),
    dict(id="R2", cat="Access", req="Attempt removal from above first (preferred) and only open walls/ceilings if that cannot be done safely.",
         basis="Requester preference. Plumbing on the concealed assembly is C-36 trade work under the official CSLB classification.",
         status=("info", "Requester-stated; trade scope verified"), srcs=["cslb-c36"]),
    dict(id="R3", cat="Access", req="Be prepared to work from below through the storage unit's drywall ceiling and restore the ceiling afterwards.",
         basis="Requester-stated fallback recommended by the plumbers consulted. Ceiling opening/patching is drywall work (CSLB C-9 trade); the City's permit guidance addresses work on pipes behind walls.",
         status=("info", "Requester-stated; trade scope verified"), srcs=["cslb-c9", "sf-plumbing-permit"]),
    dict(id="R4", cat="Provider", req="One licensed provider for both plumbing and drywall (all-in-one service).",
         basis="Under CSLB classifications a C-36 licence covers plumbing and C-9 covers drywall; a Class B general building contractor may take a contract involving two or more unrelated trades (BPC § 7057). Six active B + C-36 licensees were found in San Francisco / Daly City — see Contractors.",
         status=("ok", "Verified — candidates identified"), srcs=["cslb-b", "bpc-7057", "cslb-c36", "cslb-c9"]),
    dict(id="R5", cat="Provider", req="Provider must be a licensed plumber or contractor.",
         basis="Every candidate on this site was checked against the official CSLB record on 2026-11-07 (status, classifications, bond, workers' compensation). Note BPC § 7048: the licensing exemption for jobs under $1,000 does not apply where a building permit is required or where the person employs others.",
         status=("ok", "Verified via CSLB"), srcs=["cslb-check", "bpc-7048"]),
    dict(id="R6", cat="Provider", req="Experience with delicate work in an occupied unit; ability to work around tenants.",
         basis="No official source rates job-specific experience; it must be asked for in writing. The legal frame for entering an occupied unit is CIV § 1954: entry to make necessary or agreed repairs, reasonable written notice (24 hours presumed reasonable) stating date, approximate time and purpose, during normal business hours, or an oral agreement with the tenant for agreed repairs within one week.",
         status=("warn", "Partly verifiable — legal frame verified, experience must be confirmed with provider"), srcs=["civ-1954"]),
    dict(id="R7", cat="Provider", req="Serves San Francisco.",
         basis="CSLB business addresses: nine candidates are in San Francisco; Manny's Plumbing & Rooter is in Daly City (adjacent). Service area itself is a company statement, not a CSLB field.",
         status=("ok", "Address verified via CSLB"), srcs=["cslb-check"]),
    dict(id="R8", cat="Provider", req="Positive reviews on Yelp or similar platforms for this type of work.",
         basis="Yelp returned HTTP 403 to automated retrieval on 2026-11-07; no rating or review count could be captured, so none is shown. Review platforms are third-party sources in any case and cannot verify licence status — use the CSLB record for that.",
         status=("unverified", "UNVERIFIED — platform inaccessible"), srcs=["yelp", "cslb-check"]),
    dict(id="R9", cat="Budget", req="Organise and analyse the three estimates received (list headed 8/30/26).",
         basis="Company identities verified via CSLB; the reported scopes and amounts come only from the requester's brief (no written quotes were supplied) and are therefore not shown as verified values — see Estimates.",
         status=("unverified", "Amounts UNVERIFIED"), srcs=["cslb-977638", "cslb-757796", "cslb-1024971"]),
    dict(id="R10", cat="Contracting", req="Contractor must carry the required $25,000 contractor's bond and have workers' compensation coverage or a valid exemption.",
         basis="CSLB consumer guide; every candidate's bond and workers' compensation data is tabulated on the Contractors page from the official record.",
         status=("ok", "Verified for all 10 records"), srcs=["cslb-hire", "cslb-check"]),
    dict(id="R11", cat="Contracting", req="Down payment must not exceed 10% of the contract price or $1,000, whichever is less; get a written contract with a single scope covering plumbing, access and restoration.",
         basis="CSLB consumer guide (home-improvement down-payment rule). The written-scope recommendation is this review's analysis.",
         status=("ok", "Rule verified"), srcs=["cslb-hire"]),
    dict(id="R12", cat="Compliance", req="Follow City plumbing-permit guidance for work on pipes behind walls; use a licence class the City accepts for plumbing permits.",
         basis="SF.gov: a plumbing permit is required before cutting into or replacing pipes behind walls (exemptions in SF Plumbing Code § 104.2); classes accepted for plumbing permits include A, B (subject to conditions), C-4, C-36, C-16, C-20 and C-54. For R-2 apartment buildings the owner may perform drywall/sheetrock work but must hire licensed contractors for plumbing.",
         status=("ok", "Official guidance recorded"), srcs=["sf-plumbing-permit", "sf-kb-permit"]),
    dict(id="R13", cat="Documentation", req="Publish all findings with an official source on every table row; leave unconfirmed values blank and flagged.",
         basis="Met by construction: the generator and the test suite reject any table row without an https:// official link and render unconfirmed values as blank UNVERIFIED cells.",
         status=("ok", "Enforced by tests"), srcs=["cslb-check"]),
]


def page_requirements() -> str:
    rows = []
    for r in REQUIREMENTS:
        rows.append([tdt(r["id"]), tdt(r["cat"]), tdt(r["req"]), tdt(r["basis"]),
                     td(pill(r["status"][0], r["status"][1])), td(src(*r["srcs"]))])
    body = f"""
<div class="note info"><strong>How to read this register.</strong> “Requirement” restates what the requester asked for. “Basis / what was verified” separates requester statements (which no official source can confirm) from facts checked against the linked official source on {READ_DATE}.</div>
{table("requirements", ["ID", "Category", "Requirement", "Basis / what was verified", "Status", "Official source"], rows, "Requirements register — 13 items")}
"""
    return layout("requirements.html", "Requirements register", "Every requirement for the trip-lever repair, with the official rule or record it was checked against.", body)


# ---------------------------------------------------------------------------
# Estimates
# ---------------------------------------------------------------------------
def page_estimates() -> str:
    rows = []
    for e in ESTIMATES:
        r = REC[e["rec"]]
        rows.append([
            tdt(str(e["n"])),
            td(f"{esc(e['brief_name'])}<br><small class=\"muted\">CSLB record: {esc(r['name'])}</small>"),
            td(f"#{esc(r['lic'])} · {pill('ok', r['status'])}<br><small class=\"muted\">expires {esc(r['expires'])}</small>"),
            tdt(classes_text(r)),
            td(f"<em>{esc(e['scope'])}</em><br>{pill('mute', 'requester-reported wording')}"),
            blank("Amount cannot be confirmed from any official source (no written quote supplied; CSLB publishes no prices). The requester-reported figure is listed in prose below, not as a value."),
            blank(f"The brief carries one heading date ({BRIEF_DATE_HEADING}) for the whole list; no per-estimate document confirms it."),
            td(src(f"cslb-{r['lic']}")),
        ])
    reported = "".join(
        f"<li><strong>{esc(e['brief_name'])}</strong> — {esc(e['scope'])} — reported amount {esc(e['amount_reported'])}</li>" for e in ESTIMATES)
    body = f"""
<div class="note"><strong>Verification boundary.</strong> The three companies were matched to official CSLB records (linked in each row). The scopes and amounts exist only in the requester's brief; no written quotes were supplied and no official source publishes repair prices, so the amount and date cells are blank and flagged. Figures are repeated below strictly as requester-reported text.</div>
{table("estimates", ["#", "Company (as written in brief)", "CSLB licence & status", "Classification(s)", "Scope as reported by requester", "Verified amount (USD)", "Verified estimate date", "Official source"], rows, "Estimates received — company identity verified, values not verifiable")}
<h2 id="reported">Requester-reported figures (not verified — reproduced from the brief)</h2>
<p class="muted">List heading in the brief: “{esc(BRIEF_DATE_HEADING)}”. These figures are the requester's own report and are shown here only so the record is complete.</p>
<ul class="tight">{reported}</ul>
<h2 id="analysis">Analysis of the three estimates</h2>
<ul class="tight">
<li><strong>They describe three different jobs, not three prices for one job.</strong> As reported, estimate 1 replaces the waste-and-overflow assembly (the concealed tube-and-lever kit the manufacturer specification describes), estimate 2 replaces the lever plus the spout with a diverter, and estimate 3 only repairs or adjusts the plunger handle. Comparing the figures as like-for-like would be misleading. ({a(SOURCES['oatey']['url'], 'Oatey trip-lever bath waste specification')})</li>
<li><strong>None of the reported scopes mentions access from below or ceiling restoration.</strong> The brief says every plumber consulted recommended working from below through the storage unit's ceiling; none of the three reported scopes includes opening or restoring drywall.</li>
<li><strong>All three companies hold only C-36 Plumbing on their CSLB records</strong> (no B General Building, no C-9 Drywall). Whether a plumbing contractor may patch the ceiling as work incidental to a plumbing contract was not verified from an official source and is flagged. ({a(SOURCES['cslb-c36']['url'], 'C-36 classification')} · {a(SOURCES['cslb-c9']['url'], 'C-9 classification')})</li>
<li><strong>Licence status is current for all three</strong>, with the earliest expiry being Bay Area Plumbing (01/31/2027) and the earliest workers' compensation expiry being Fast Response (policy expires 12/18/2026). Bay Area Plumbing is workers' compensation exempt (certified no employees). ({a(SOURCES['cslb-757796']['url'], 'CSLB #757796')} · {a(SOURCES['cslb-1024971']['url'], 'CSLB #1024971')})</li>
<li><strong>Next step that keeps the record verifiable:</strong> ask each candidate for a written quote on letterhead that states the licence number, the top-down attempt, the below-access plan, the restoration scope and the price. Written quotes can then be attached as sources.</li>
</ul>
"""
    return layout("estimates.html", "Estimates", "The three estimates received, matched to official CSLB records; amounts and dates are left blank because no official source confirms them.", body)


# ---------------------------------------------------------------------------
# Contractors
# ---------------------------------------------------------------------------
def contractor_row(r: dict, with_fit: bool) -> list[str]:
    srcs = [f"cslb-{r['lic']}"]
    if r.get("site_src"):
        srcs.append(r["site_src"])
    if r["key"] == "handyman":
        srcs.append("cslb-complaint-1003394")
    disclosure = r["disclosure"]
    disc_cell = td(pill("warn", "Disclosure on file") + "<br><small>" + esc(disclosure) + "</small>") if "Citation" in disclosure else td(pill("ok", "None shown") + "<br><small class=\"muted\">" + esc(disclosure) + "</small>")
    cells = [
        td(f"<strong>{esc(r['name'])}</strong><br><small class=\"muted\">{esc(r['entity'])} · issued {esc(r['issued'])}</small>"),
        td(f"#{esc(r['lic'])}<br>{pill('ok', r['status'])}<br><small class=\"muted\">expires {esc(r['expires'])}</small>"),
        tdt(classes_text(r)),
        tdt(f"{r['addr']} · {r['phone']}"),
        tdt(bond_text(r)),
        td((pill("ok", "WC insured") if r["wc"] == "Insured" else pill("warn", "WC exempt")) + "<br><small>" + esc(wc_text(r)) + "</small>"),
        disc_cell,
    ]
    if with_fit:
        if has_b(r):
            fit = pill("ok", "B + C-36 — both trades within licence scope") + "<br><small>Class B may contract for two or more unrelated trades (BPC § 7057); C-36 covers the plumbing.</small>"
        else:
            fit = pill("warn", "No B or C-9 on record — plumbing scope") + "<br><small>Holds " + esc(classes_text(r)) + "; drywall restoration would need another licensee unless incidental (not verified).</small>"
        cells.append(td(fit))
        if r.get("site_claim"):
            cells.append(td(esc(r["site_claim"])))
        else:
            cells.append(blank("Company website not retrieved by this session; advertised services unconfirmed."))
        cells.append(blank("Yelp blocked automated retrieval (HTTP 403, 2026-11-07); third-party ratings are not official and were not captured."))
    cells.append(td(src(*srcs)))
    return cells


def page_contractors() -> str:
    hdr_full = ["Business (CSLB name)", "Licence & status", "Classifications", "CSLB address · phone", "Bond", "Workers' compensation", "Complaint disclosure", "Single-licence fit for plumbing + drywall", "Services advertised on official company site", "Review-platform rating", "Official sources"]
    allin = [contractor_row(REC[k], True) for k in ["generalsf", "handyman", "ace", "genteel", "rapidflow", "mannys"]]
    quoted = [contractor_row(REC[k], True) for k in ["expert", "bayarea", "fast"]]
    other = [contractor_row(REC["heises"], True)]
    body = f"""
<div class="note info"><strong>What this page can and cannot verify.</strong> Licence status, classifications, bond, workers' compensation, address and phone come from the official CSLB record read on {READ_DATE}. “Single-licence fit” is an analysis of those classifications against the official CSLB definitions and BPC § 7057 — it says what a licence <em>permits</em>, not whether a company will take this job, is available, or has done this exact repair before. Those must be confirmed directly with the company and documented in writing.</div>
<h2 id="all-in-one">Candidates holding B General Building + C-36 Plumbing (one licence covers both trades)</h2>
{table("allinone", hdr_full, allin, "Six active licensees in San Francisco / Daly City with B + C-36")}
<div class="note ok"><strong>Strongest documented fit on official sources:</strong> <strong>General SF</strong> (#959843) and <strong>Handyman Heroes Inc</strong> (#1003394) are the two B + C-36 licensees whose official company sites explicitly advertise both plumbing and sheetrock/wall repair. General SF is workers' compensation exempt (certified no employees) — ask who will attend. Handyman Heroes has a 2020 citation on its CSLB disclosure page — read it before engaging. Ace Plumbing &amp; Rooter (#829071) has the widest classification set and WC insurance, but no drywall service statement was seen on its home page.</div>
<h2 id="quoted">The three companies that provided estimates (C-36 Plumbing only)</h2>
{table("quoted", hdr_full, quoted, "Quoted plumbers — plumbing licence verified; no drywall classification on record")}
<h2 id="other">Other San Francisco plumber audited from earlier repository pages</h2>
{table("other", hdr_full, other, "Holds A, C-10, C-20 and C-36 but not B or C-9")}
<h2 id="review-platforms">Review platforms (Yelp and similar)</h2>
<p>The brief asked for Yelp research. On {READ_DATE} Yelp answered automated retrieval with HTTP 403, so no ratings, review counts or review text could be captured, and none is shown. Review sites are third-party sources; a Yelp “verified licence” badge is not a CSLB check. Manual review link for the requester: {a('https://www.yelp.com/search?find_desc=Plumbing+and+drywall&find_loc=San+Francisco%2C+CA', 'Yelp search — plumbing and drywall, San Francisco')} (third-party, unverified).</p>
"""
    return layout("contractors.html", "Contractors", "Official CSLB records for the quoted plumbers and for licensees whose classifications cover both plumbing and drywall, plus what each company's own site advertises.", body)


# ---------------------------------------------------------------------------
# Licensing & compliance references
# ---------------------------------------------------------------------------
COMPLIANCE = [
    dict(topic="Who may do the plumbing", rule="C-36 Plumbing Contractor is the CSLB classification covering plumbing systems; all ten licensees on this site hold it.", applies="The concealed waste-and-overflow assembly is plumbing work.", srcs=["cslb-c36", "cslb-check"]),
    dict(topic="Who may do the drywall", rule="C-9 Drywall Contractor is the CSLB classification covering drywall; none of the ten licensees holds C-9. A Class B General Building Contractor may contract for work involving at least two unrelated trades or crafts other than framing/carpentry, or hold/subcontract the specialty licence (BPC § 7057).", applies="The ceiling opening and restoration under the storage unit.", srcs=["cslb-c9", "cslb-b", "bpc-7057"]),
    dict(topic="Licensing threshold", rule="BPC § 7048 exempts work whose aggregate contract price for labour, materials and all other items is under $1,000 (as amended by AB 1170, effective 2026-01-01), but the exemption does not apply where a building permit is required or where the person employs others.", applies="Context only — the requester asked for a licensed provider regardless of price.", srcs=["bpc-7048"]),
    dict(topic="City plumbing-permit guidance", rule="SF.gov: apply for a plumbing permit before cutting into or replacing pipes behind walls; exemptions are listed in SF Plumbing Code § 104.2. Licence classes accepted for plumbing permits: A; B (subject to conditions such as an approved scope or a linked kitchen/bath permit); C-4; C-36; C-16; C-20; C-54. DBI Help Desk 628-652-4900.", applies="Official reference for the concealed-pipe work described in the brief; applicability to a specific job is determined by the City, not by this site.", srcs=["sf-plumbing-permit"]),
    dict(topic="Owner-performed work in apartment buildings", rule="SF.gov kitchen/bath remodel guidance: for R-2 apartment buildings the property owner may do drywall/sheetrock work but must hire licensed contractors for plumbing and electrical.", applies="Alternative split of the drywall and plumbing scopes if a single provider cannot be engaged.", srcs=["sf-kb-permit"]),
    dict(topic="Entering a tenant-occupied unit", rule="CIV § 1954: a landlord may enter to make necessary or agreed repairs; reasonable written notice stating date, approximate time and purpose (24 hours presumed reasonable), entry during normal business hours unless the tenant consents; landlord and tenant may agree orally to an entry for agreed repairs within one week; access must not be abused.", applies="The bathroom is tenant-occupied; the storage unit below may also require coordination.", srcs=["civ-1954"]),
    dict(topic="Bond", rule="CSLB requires licensed contractors to carry a $25,000 contractor's bond; each record on this site shows the bond and surety.", applies="All ten records show a $25,000 bond on file.", srcs=["cslb-hire", "cslb-check"]),
    dict(topic="Workers' compensation", rule="CSLB consumer guidance: confirm workers' compensation (and liability) insurance. A CSLB exemption means the licensee certified it has no employees.", applies="Four candidates are WC-exempt (Bay Area Plumbing, General SF, Rapid Flow, Manny's) — confirm who will physically perform the work.", srcs=["cslb-hire", "cslb-757796", "cslb-959843", "cslb-1115649", "cslb-841229"]),
    dict(topic="Down payment", rule="CSLB consumer guidance: a home-improvement down payment may not exceed 10% of the contract price or $1,000, whichever is less.", applies="Applies to the written contract with whichever provider is engaged.", srcs=["cslb-hire"]),
    dict(topic="Complaint disclosure", rule="CSLB discloses certain citations and actions under B&P § 7124.6 via a link on the licence detail page.", applies="Handyman Heroes Inc (#1003394) shows Citation #2 2020 001045 dated 07/12/2020; no disclosure link was shown for the other nine records.", srcs=["cslb-complaint-1003394", "cslb-1003394"]),
]


def page_compliance() -> str:
    rows = [[tdt(c["topic"]), tdt(c["rule"]), tdt(c["applies"]), td(src(*c["srcs"]))] for c in COMPLIANCE]
    body = f"""
<div class="note info">Neutral references only. Each row quotes or paraphrases the linked official text as read on {READ_DATE}; whether a rule applies to a specific job is decided by the authority concerned.</div>
{table("compliance", ["Topic", "Official rule (as read)", "How it bears on this project", "Official source"], rows, "Licensing, City guidance, tenancy and consumer-protection references")}
"""
    return layout("compliance.html", "Licensing & compliance references", "Official CSLB, California statute and SF.gov references that govern who may do the plumbing and drywall, and how an occupied unit is entered for repairs.", body)


# ---------------------------------------------------------------------------
# Repository review
# ---------------------------------------------------------------------------
REPO_REVIEW = [
    dict(id="RR-01", sev="warn", area="Root dashboard — index.html",
         finding="“Problem snapshot” table rows (lines 80–85) have no official source link; the values are owner-provided statements rendered as table values.",
         check="Rule: every table row needs an official source link; requester statements belong in attributed prose (as done on this site's dashboard).",
         locs=[("index.html", "L80-L85")], srcs=[]),
    dict(id="RR-02", sev="warn", area="Root dashboard — estimate tables",
         finding="The three requester-reported estimate amounts are rendered inside table value cells on index.html (lines 100–112), summary.html (58–70), estimates.html (47–69) and shortlist.html (117–131), and in the root EXECUTIVE-SUMMARY.md table. They are labelled “unverified” but not left blank.",
         check="No official source publishes these figures (CSLB publishes licence data only). The project rule is blank cell + flag.",
         locs=[("index.html", "L100-L112"), ("summary.html", "L58-L70"), ("estimates.html", "L47-L69"), ("shortlist.html", "L117-L131"), ("EXECUTIVE-SUMMARY.md", "")], srcs=["cslb-check"]),
    dict(id="RR-03", sev="warn", area="Root dashboard — estimates.html benchmark table",
         finding="Rows 101–167 present third-party cost figures (Angi, This Old House, a trade blog) with a “verified” label.",
         check="These publishers are not official sources; the label should read third-party / contextual, and the figures should not be used to validate the estimates.",
         locs=[("estimates.html", "L101-L167")], srcs=[]),
    dict(id="RR-04", sev="warn", area="Root dashboard — review-platform values",
         finding="Yelp star ratings and review counts are displayed in contractors.html (52–166), summary.html (102–150), shortlist.html (59–91) and sources.html (187–199).",
         check="Yelp refused automated retrieval on 2026-11-07 (HTTP 403), so the values cannot be re-verified; they are volatile third-party data and should be blank/UNVERIFIED under the project rule.",
         locs=[("contractors.html", "L52-L166"), ("summary.html", "L102-L150"), ("shortlist.html", "L59-L91"), ("sources.html", "L187-L199")], srcs=["yelp"]),
    dict(id="RR-05", sev="ok", area="Root dashboard — verification.html CSLB table",
         finding="Licence numbers, entities, issue/expiry dates, classifications, $25,000 bonds and workers' compensation status for the eight licensees at lines 45–115 match the official CSLB records this session read independently on 2026-11-07.",
         check="Verified — no discrepancy except RR-06.",
         locs=[("verification.html", "L45-L115")], srcs=["cslb-977638", "cslb-757796", "cslb-1024971", "cslb-959843", "cslb-829071", "cslb-1003394", "cslb-1115649", "cslb-841229"]),
    dict(id="RR-06", sev="info", area="Root dashboard — verification.html line 64",
         finding="Fast Response's address is shown as “236 W Portal Ave #459”; the official CSLB record prints “236 W POTRAL AVE #459”.",
         check="The record's spelling appears to be a CSLB typo, but silently correcting an official value hides the discrepancy. Show it as printed with a note (as this site does).",
         locs=[("verification.html", "L64")], srcs=["cslb-1024971"]),
    dict(id="RR-07", sev="warn", area="Root dashboard — rows without source links",
         finding="Rows without any https:// link: findings.html line 171 and verification.html line 118 (Szeto Plumbing and Handyman — “no matching CSLB record”), shortlist.html lines 164–182 (experience / tenant / access rows), verification.html lines 190–192, sources.html lines 239–242 (owner-provided items), flagged.html lines 43 and 52.",
         check="This session did not re-run a CSLB business-name search for Szeto, so that claim is left as reported, unverified. The other rows are requester statements or methodology notes that should be prose, not table rows.",
         locs=[("findings.html", "L171"), ("verification.html", "L118"), ("shortlist.html", "L164-L182"), ("verification.html", "L190-L192"), ("sources.html", "L239-L242"), ("flagged.html", "L43-L52")], srcs=["cslb-check"]),
    dict(id="RR-08", sev="ok", area="docs/overflow-permits.html line 73",
         finding="States the licensing exemption threshold as $1,000 under B&P § 7048 as amended by AB 1170 effective 2026-01-01.",
         check="Matches the statute text read on 2026-11-07. (Earlier repository versions cited an outdated $500 figure; the current page is correct.)",
         locs=[("docs/overflow-permits.html", "L73")], srcs=["bpc-7048"]),
    dict(id="RR-09", sev="warn", area="Legacy overflow pages under docs/ and bathtub-overflow/",
         finding="Table rows lacking any external source link: docs/overflow-analysis.html (6 of 6), docs/overflow-contractors.html (8 of 8), docs/overflow-estimates.html (4 of 4), docs/overflow-executive-summary.html (4 of 4), docs/overflow-permits.html (7 of 7), docs/plumbing-index.html (8 of 8), bathtub-overflow/problem-scope.html (11 of 12), bathtub-overflow/analysis.html (6 of 10). The same pages print the reported amounts in value cells (e.g., docs/overflow-estimates.html lines 40–69; docs/plumbing-index.html lines 39–56).",
         check="These page sets predate the verification rule and remain publicly reachable on GitHub Pages; they should carry a historical notice or be brought up to the rule.",
         locs=[("docs/overflow-estimates.html", "L40-L69"), ("docs/plumbing-index.html", "L39-L56"), ("bathtub-overflow/problem-scope.html", ""), ("docs/overflow-permits.html", "")], srcs=[]),
    dict(id="RR-10", sev="warn", area="docs/data/overflow-entries.csv",
         finding="Estimate rows cite Yelp search URLs in the source_link column for requester-supplied amounts (lines 2–3).",
         check="A Yelp search page is neither official nor evidence of the amount; the source cell should be blank/UNVERIFIED.",
         locs=[("docs/data/overflow-entries.csv", "L2-L3")], srcs=["yelp"]),
    dict(id="RR-11", sev="warn", area="bathtub-overflow/permits-compliance.html",
         finding="Lines 52–54 map each reported estimate to a permit outcome; line 58 states that SF.gov lists C-4 or C-36 (and C-54) for plumbing permits.",
         check="The current SF.gov page lists A, B (subject to conditions), C-4, C-36, C-16, C-20 and C-54, so the list is incomplete; job-specific permit outcomes are determined by the City, not by a quote description.",
         locs=[("bathtub-overflow/permits-compliance.html", "L52-L58")], srcs=["sf-plumbing-permit"]),
    dict(id="RR-12", sev="warn", area="tests/test_bath_site.py and scripts/build_bath_site.py",
         finding="The test suite asserts that the reported amounts remain numeric and appear in the generated pages (lines 66, 138–139, 147–150), so the docs/bath generator is locked into printing unverified values.",
         check="If docs/bath is to follow the blank-cell rule, these assertions must change together with the generator. This session did not modify either file (outside its claimed scope).",
         locs=[("tests/test_bath_site.py", "L66"), ("tests/test_bath_site.py", "L138-L150")], srcs=[]),
    dict(id="RR-13", sev="info", area="Repository identity — README.md and docs/ GEMS pages",
         finding="README.md still describes the repository as a geothermal (GEMS) fault-prospectivity audit, and docs/index.html, docs/executive-summary.html, docs/validation.html, docs/parallel-*.html and docs/site-GEMSDOE*.html belong to that unrelated project; their tables (e.g., 38 rows in docs/index.html) have no external links.",
         check="Not plumbing content; flagged because the GitHub Pages root serves both projects and a reader can confuse them. A README section pointing to the plumbing dashboards would resolve it (README is owned by another session).",
         locs=[("README.md", ""), ("docs/index.html", "")], srcs=[]),
    dict(id="RR-14", sev="info", area="COORDINATION.md",
         finding="Audit blocks are duplicated from repeated rebases (the same “$500 licensing claim (A17)” paragraph appears at lines 97, 233, 303 and 439).",
         check="Informational; content was preserved rather than deleted to respect other sessions' entries.",
         locs=[("COORDINATION.md", "L97"), ("COORDINATION.md", "L233"), ("COORDINATION.md", "L303"), ("COORDINATION.md", "L439")], srcs=[]),
    dict(id="RR-15", sev="ok", area="Existing automated checks",
         finding="python3 -m unittest tests/test_dashboard_integrity.py, scripts/build_overflow_verification.py --check and the 12 checks in tests/test_bath_site.py all passed when run by this session.",
         check="Passing tests do not establish source accuracy (see RR-12), but the committed artefacts are internally consistent.",
         locs=[("tests/test_dashboard_integrity.py", ""), ("scripts/build_overflow_verification.py", "")], srcs=[]),
]


def page_repo_review() -> str:
    rows = []
    for f in REPO_REVIEW:
        links = "<br>".join(gh(p, l) for p, l in f["locs"])
        if f["srcs"]:
            links += "<br>" + src(*f["srcs"])
        sev = {"ok": pill("ok", "Verified OK"), "warn": pill("warn", "Needs review"), "info": pill("info", "Informational")}[f["sev"]]
        rows.append([tdt(f["id"]), tdt(f["area"]), tdt(f["finding"]), tdt(f["check"]), td(sev), td(links)])
    body = f"""
<div class="note info">Scope: every HTML, Markdown, CSV, JSON, script and test file in the repository at <code>main {MAIN_SHA[:7]}</code> was inventoried; 63 HTML files and 714 table rows were scanned for missing source links, displayed unverified amounts and third-party ratings, and the CSLB/statute facts on the root dashboard were re-read from the official sources. Each row links to the exact lines on GitHub (the authoritative copy of the file) and, where a fact was checked, to the official source.</div>
{table("repo-review", ["ID", "Area", "Finding", "Check performed / recommendation", "Status", "Repository lines & official source"], rows, "Repository review — 15 findings")}
<p class="muted">The same findings are available as Markdown in <a href="REPO-REVIEW.md">REPO-REVIEW.md</a>.</p>
"""
    return layout("repo-review.html", "Repository review", "Line-by-line review of the repository against official sources, with links to the exact lines for manual review.", body)


# ---------------------------------------------------------------------------
# Verification log
# ---------------------------------------------------------------------------
def verification_rows() -> list[dict]:
    rows = []
    for r in CSLB_RECORDS:
        rows.append(dict(item=f"CSLB licence #{r['lic']} — {r['name']}",
                         method=f"Opened the official licence detail page; read status, entity, issue/expiry, classifications, bond and workers' compensation (CSLB data-current stamp {READ_DATE}).",
                         result=f"{r['status']}; {classes_text(r)}; expires {r['expires']}; {bond_text(r)}; {wc_text(r)}.",
                         status="ok", srcs=[f"cslb-{r['lic']}"]))
    rows.append(dict(item="CSLB complaint disclosure #1003394", method="Opened the disclosure page linked from the licence record.",
                     result="Citation #2 2020 001045 dated 07/12/2020 is disclosed.", status="warn", srcs=["cslb-complaint-1003394"]))
    rows.append(dict(item="CSLB classification definitions B, C-36, C-9", method="Opened the three official classification pages.",
                     result="Trade scopes recorded; used only to classify licence fit.", status="ok", srcs=["cslb-b", "cslb-c36", "cslb-c9"]))
    rows.append(dict(item="BPC § 7048 and § 7057", method="Read the statute text on leginfo.legislature.ca.gov.",
                     result="$1,000 threshold with building-permit and employee carve-outs; Class B two-trade rule.", status="ok", srcs=["bpc-7048", "bpc-7057"]))
    rows.append(dict(item="CIV § 1954", method="Read the statute text on leginfo.legislature.ca.gov.",
                     result="Entry for repairs with reasonable written notice (24 hours presumed), normal business hours, oral agreement option within one week.", status="ok", srcs=["civ-1954"]))
    rows.append(dict(item="SF.gov plumbing permit and kitchen/bath remodel guidance", method="Read both City pages.",
                     result="Permit before cutting into/replacing pipes behind walls (exemptions § 104.2); accepted classes A, B (conditions), C-4, C-36, C-16, C-20, C-54; R-2 owners may do drywall but must hire licensed plumbers.", status="ok", srcs=["sf-plumbing-permit", "sf-kb-permit"]))
    rows.append(dict(item="CSLB consumer guide", method="Read the official hiring guide.",
                     result="$25,000 bond; down payment ≤ 10% or $1,000 whichever is less; verify insurance.", status="ok", srcs=["cslb-hire"]))
    rows.append(dict(item="Manufacturer specification (Oatey trip-lever bath waste)", method="Read the product specification page.",
                     result="Trip-lever bath waste = full waste-and-overflow kit with trip-lever stopper (Part #A9226 / #P9226).", status="ok", srcs=["oatey"]))
    rows.append(dict(item="Company websites — General SF, Handyman Heroes, Ace", method="Read each official company page.",
                     result="General SF and Handyman Heroes advertise plumbing and sheetrock/wall repair; Ace lists licence classes and property-manager services without a drywall statement.", status="ok", srcs=["generalsf", "handyman", "ace"]))
    rows.append(dict(item="Yelp (third-party reviews)", method="Attempted to open a business page.",
                     result="HTTP 403 — no values captured; nothing from Yelp is shown as a value on this site. Licence status is taken from the official CSLB lookup instead.", status="unverified", srcs=["yelp", "cslb-check"]))
    rows.append(dict(item="Estimate amounts and dates", method="Searched for an official or company-issued document; none exists in the repository or the brief.",
                     result="Left blank and flagged on the Estimates page; requester-reported figures shown only as attributed prose.", status="unverified", srcs=["cslb-check"]))
    rows.append(dict(item="This site's own tables", method="tests/test_e9a30ab9_overflow_site.py checks every <tbody> row for an https:// link, every blank cell for an UNVERIFIED flag, all internal links/anchors, and that the committed output matches the generator.",
                     result="All checks pass at build time; see the test file in the repository.", status="ok", srcs=["cslb-check"]))
    return rows


def page_verification() -> str:
    rows = []
    for v in verification_rows():
        st = {"ok": pill("ok", "Verified"), "warn": pill("warn", "Verified — review"), "unverified": pill("unverified", "UNVERIFIED")}[v["status"]]
        rows.append([tdt(v["item"]), tdt(v["method"]), tdt(v["result"]), td(st), tdt(READ_DATE), td(src(*v["srcs"]))])
    body = f"""
{table("verification", ["Item", "Method", "Result", "Status", "Date read", "Official source"], rows, "Verification log — every check performed by this session")}
"""
    return layout("verification.html", "Verification log", "Each check this session performed, how it was done, the result, and the official source it was read from.", body)


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
def page_sources() -> str:
    order = ["cslb-check"] + [f"cslb-{r['lic']}" for r in CSLB_RECORDS] + ["cslb-complaint-1003394", "cslb-c36", "cslb-b", "cslb-c9", "cslb-hire", "bpc-7048", "bpc-7057", "civ-1954", "sf-plumbing-permit", "sf-kb-permit", "oatey", "generalsf", "handyman", "ace", "yelp"]
    rows = []
    for i, k in enumerate(order, 1):
        s = SOURCES[k]
        kind_pill = pill("ok", s["kind"]) if s["kind"].startswith("Official — government") else pill("info", s["kind"]) if s["kind"].startswith("Official") else pill("unverified", s["kind"])
        verifies = esc(s["verifies"])
        if not s["kind"].startswith("Official"):
            verifies += "<br>Official cross-reference for licence status: " + a(SOURCES["cslb-check"]["url"], SOURCES["cslb-check"]["label"])
        rows.append([tdt(f"S{i:02d}"), td(a(s["url"], s["label"])), tdt(s["publisher"]), td(kind_pill), td(verifies), tdt(READ_DATE)])
    body = f"""
<div class="note info">All sources were opened directly by this session on {READ_DATE}. “Official — government” sources are CSLB, the California Legislature and the City and County of San Francisco; “Official — company/manufacturer” are the organisations' own sites; the single third-party entry documents a failed retrieval and verifies nothing.</div>
{table("sources", ["ID", "Source", "Publisher", "Type", "What it verifies", "Date read"], rows, f"{len(order)} sources")}
"""
    return layout("sources.html", "Sources", "Every source used on this site, with publisher, type and what it was used to verify.", body)


# ---------------------------------------------------------------------------
# Flagged for review
# ---------------------------------------------------------------------------
FLAGS = [
    dict(id="F01", kind="unverified", item="Estimate amounts (three figures reported in the brief)", detail="No written quote or official publication confirms them; CSLB publishes no prices. Shown blank on the Estimates table; repeated only as requester-reported prose.", action="Obtain written quotes on company letterhead and attach them as sources.", srcs=["cslb-977638", "cslb-757796", "cslb-1024971"]),
    dict(id="F02", kind="unverified", item="Estimate dates", detail=f"The brief has a single heading date ({BRIEF_DATE_HEADING}); nothing confirms the date of each individual estimate.", action="Confirm dates from the written quotes.", srcs=["cslb-check"]),
    dict(id="F03", kind="unverified", item="Review-platform ratings (Yelp)", detail="Yelp returned HTTP 403 to automated retrieval on 2026-11-07; no rating or count was captured. Third-party ratings are not official in any case.", action="Review Yelp manually if desired; rely on CSLB for licence status.", srcs=["yelp", "cslb-check"]),
    dict(id="F04", kind="warn", item="Handyman Heroes Inc — complaint disclosure", detail="CSLB discloses Citation #2 2020 001045 dated 07/12/2020 under B&P § 7124.6.", action="Read the disclosure before engaging; ask the company about it.", srcs=["cslb-complaint-1003394", "cslb-1003394"]),
    dict(id="F05", kind="warn", item="Workers' compensation exemptions", detail="Bay Area Plumbing (#757796), General SF (#959843), Rapid Flow (#1115649) and Manny's (#841229) are exempt because they certified having no employees.", action="Ask who will physically perform the work; if anyone other than the licensee attends, request proof of coverage.", srcs=["cslb-757796", "cslb-959843", "cslb-1115649", "cslb-841229"]),
    dict(id="F06", kind="unverified", item="Advertised drywall service — Ace, Genteel, Rapid Flow, Manny's", detail="Ace's home page shows licence classes and property-manager services but no drywall statement; the other three company sites were not retrieved. Licence scope permits the work, but the service offer is unconfirmed.", action="Ask each for a single written scope covering plumbing, ceiling access and restoration.", srcs=["ace", "cslb-1025814", "cslb-1115649", "cslb-841229"]),
    dict(id="F07", kind="unverified", item="May a C-36 plumber patch the ceiling as incidental work?", detail="The CSLB rule on incidental and supplemental work was not read by this session, so the question is left open rather than answered.", action="Ask CSLB or the contractor to cite the rule; otherwise use a B + C-36 licensee.", srcs=["cslb-c36", "cslb-c9"]),
    dict(id="F08", kind="unverified", item="Job-specific experience in tenant-occupied units", detail="No official source records whether a company has freed a seized trip lever from below or worked in occupied units; CIV § 1954 gives the entry/notice frame only.", action="Request references for comparable jobs in writing.", srcs=["civ-1954"]),
    dict(id="F09", kind="info", item="Fast Response CSLB address spelling", detail="The official record prints “236 W POTRAL AVE #459” (apparently “Portal”); this site shows it as printed.", action="Confirm the mailing address with the company; the licence number is the identifier.", srcs=["cslb-1024971"]),
    dict(id="F10", kind="info", item="Nearest licence and insurance expiries", detail="Fast Response workers' compensation policy expires 12/18/2026; Bay Area Plumbing licence expires 01/31/2027; Genteel WC expires 01/24/2027; Heises WC expires 01/11/2027.", action="Re-check the CSLB record on the day of hiring.", srcs=["cslb-1024971", "cslb-757796", "cslb-1025814", "cslb-1089561"]),
    dict(id="F11", kind="info", item="Heises Plumbing — not an all-in-one candidate on classification", detail="Holds C-36, C-10, A and C-20 but neither B nor C-9.", action="None; listed for completeness because earlier repository pages mention it.", srcs=["cslb-1089561"]),
    dict(id="F12", kind="warn", item="Repository: root dashboard rows without official links and unverified values in cells (RR-01, RR-02, RR-03, RR-04, RR-07)", detail="See the Repository review for exact lines.", action="Owner of the root pages to reconcile with the blank-cell rule (logged in COORDINATION.md).", srcs=["cslb-check"]),
    dict(id="F13", kind="warn", item="Repository: legacy page sets and CSV (RR-09, RR-10, RR-11, RR-12)", detail="Older overflow pages print reported amounts, cite Yelp search pages as sources, and carry an incomplete permit licence-class list; the docs/bath tests lock in printed amounts.", action="Add a historical notice or bring the pages up to the rule.", srcs=["sf-plumbing-permit", "yelp"]),
    dict(id="F14", kind="info", item="Repository identity (RR-13)", detail="README.md and several docs/ pages describe an unrelated geothermal project served from the same Pages root.", action="Add a README pointer to the plumbing dashboards (README owned by another session).", srcs=["cslb-check"]),
    dict(id="F15", kind="info", item="Szeto Plumbing and Handyman (named on root pages)", detail="Root pages state no matching CSLB record; this session did not repeat the business-name search.", action="Run the CSLB name search before considering this company.", srcs=["cslb-check"]),
]


def page_flagged() -> str:
    rows = []
    for f in FLAGS:
        kp = {"unverified": pill("unverified", "UNVERIFIED"), "warn": pill("warn", "Needs review"), "info": pill("info", "Informational")}[f["kind"]]
        rows.append([tdt(f["id"]), td(kp), tdt(f["item"]), tdt(f["detail"]), tdt(f["action"]), td(src(*f["srcs"]))])
    body = f"""
<div class="note"><strong>Flagged for Review.</strong> Everything on this page is either a value that could not be confirmed from an official source (left blank elsewhere on the site), a verified fact that deserves attention before hiring, or a repository irregularity. None of these items blocks publication; they are listed so the requester can review them and request changes.</div>
{table("flags", ["ID", "Type", "Item", "Detail", "Suggested action", "Official source"], rows, f"{len(FLAGS)} flagged items")}
"""
    return layout("flagged-for-review.html", "Flagged for review", "Unverified values, verified facts that need attention, and repository irregularities — each with its official source link.", body)


# ---------------------------------------------------------------------------
# Executive summary (Markdown + HTML from one structure)
# ---------------------------------------------------------------------------
def exec_sections() -> list[tuple[str, list[str]]]:
    quoted = ", ".join(f"{DISPLAY[e['rec']]} (#{REC[e['rec']]['lic']})" for e in ESTIMATES)
    allin = ", ".join(f"{DISPLAY[k]} (#{REC[k]['lic']})" for k in ["generalsf", "handyman", "ace", "genteel", "rapidflow", "mannys"])
    return [
        ("Situation (as described by the requester — not independently verifiable)", BRIEF_PROBLEM),
        ("What was verified, and from where", [
            f"Ten CSLB licence records read directly on {READ_DATE}: the three quoted companies plus seven other San Francisco / Daly City licensees ([CSLB lookup]({SOURCES['cslb-check']['url']})).",
            f"Official CSLB classification definitions for B, C-36 and C-9; California BPC § 7048 and § 7057; California CIV § 1954; SF.gov plumbing-permit and kitchen/bath guidance; the CSLB consumer hiring guide; the Oatey trip-lever bath-waste specification; and the official websites of General SF, Handyman Heroes and Ace Plumbing & Rooter (see [Sources](sources.html)).",
            "Yelp refused automated retrieval (HTTP 403), so no review-platform values appear anywhere on the site.",
        ]),
        ("Key findings", [
            f"All three quoted companies — {quoted} — are current and active, but each holds only C-36 Plumbing. None holds B General Building or C-9 Drywall, so none can self-perform the ceiling restoration within its own licence scope on the face of the CSLB record (whether a patch could be incidental to a plumbing contract is flagged, not assumed).",
            f"Six current licensees whose classifications cover both trades (B + C-36) were identified: {allin}. Under BPC § 7057 a Class B contractor may contract for work involving two or more unrelated trades, and C-36 covers the plumbing.",
            "Of the six, two advertise both plumbing and sheetrock/wall repair on their official websites: General SF (also C-10; workers' compensation exempt — certified no employees) and Handyman Heroes Inc (workers' compensation insured; a 2020 citation is on its CSLB disclosure page). Ace Plumbing & Rooter has the widest classification set and WC insurance but no drywall statement was seen on its home page; Genteel, Rapid Flow and Manny's websites were not retrieved.",
            "The three reported estimates describe three different scopes (replace the waste-and-overflow assembly; replace lever and spout with diverter; repair/adjust the plunger handle) and none mentions access from below or ceiling restoration. Their amounts and dates cannot be confirmed from any official source, so they are blank and flagged on the Estimates page and repeated only as requester-reported prose.",
            "Entering the tenant-occupied unit for repairs is governed by CIV § 1954: reasonable written notice (24 hours presumed reasonable) stating date, approximate time and purpose, entry during normal business hours, or an oral agreement for agreed repairs within one week.",
            "City guidance (SF.gov) calls for a plumbing permit before cutting into or replacing pipes behind walls, with exemptions in SF Plumbing Code § 104.2, and lists the licence classes accepted for plumbing permits; for R-2 apartment buildings the owner may do drywall/sheetrock work but must hire licensed contractors for plumbing. These are recorded as neutral references.",
            "Consumer-protection rules from CSLB: $25,000 bond (all ten records comply); down payment capped at 10% or $1,000, whichever is less; confirm workers' compensation — four candidates are exempt because they certified having no employees.",
        ]),
        ("Recommended next steps (organised information, not legal advice)", [
            "Contact General SF and Handyman Heroes first (both trades on one licence and both advertised), then Ace, Genteel, Rapid Flow and Manny's; ask each for one written scope covering a careful top-down attempt, the below-access plan through the storage-unit ceiling, restoration, tenant coordination and price.",
            "Re-check each CSLB record on the day of hiring (statuses, bonds and insurance change); the earliest dates on file are Fast Response's WC policy (12/18/2026) and Bay Area Plumbing's licence (01/31/2027).",
            "For WC-exempt licensees, confirm who will attend; for Handyman Heroes, read the citation disclosure first.",
            "Give the tenant written notice that meets CIV § 1954, and coordinate access to the storage unit below.",
            "Attach written quotes to the repository so the estimate values can move from UNVERIFIED to sourced.",
        ]),
        ("Repository review in brief", [
            "Fifteen findings are recorded on the Repository review page with links to exact lines: the root dashboard renders requester-reported amounts and third-party ratings in value cells and has rows without official links; legacy page sets predate the rule; one CSV cites Yelp search pages as sources; one permit page lists an incomplete set of licence classes; the docs/bath tests lock in printed amounts; the root CSLB table otherwise matches the official records exactly.",
            f"Flagged items: {len(FLAGS)} (see Flagged for review). Unverified items do not block publication.",
        ]),
    ]


def exec_markdown() -> str:
    out = [f"# Executive Summary — Bathtub wastewater overflow trip lever (San Francisco)\n",
           f"Prepared {READ_DATE} by session `{SESSION}`. Live dashboard: `overflow-trip-lever-e9a30ab9/index.html`. Every official source was read directly on {READ_DATE}; requester statements are labelled as such and never presented as verified values.\n"]
    for title, items in exec_sections():
        out.append(f"## {title}\n")
        out.extend(f"- {i}" for i in items)
        out.append("")
    out.append("## Official sources\n")
    for k in ["cslb-check", "cslb-b", "cslb-c36", "cslb-c9", "bpc-7048", "bpc-7057", "civ-1954", "sf-plumbing-permit", "sf-kb-permit", "cslb-hire", "oatey", "generalsf", "handyman", "ace"]:
        s = SOURCES[k]
        out.append(f"- [{s['label']}]({s['url']})")
    for r in CSLB_RECORDS:
        s = SOURCES[f"cslb-{r['lic']}"]
        out.append(f"- [{s['label']}]({s['url']})")
    s = SOURCES["cslb-complaint-1003394"]
    out.append(f"- [{s['label']}]({s['url']})")
    return "\n".join(out) + "\n"


def md_inline_to_html(text: str) -> str:
    """Escape text, then convert [label](url) markdown links to anchors."""
    parts = []
    pos = 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(esc(text[pos:m.start()]))
        url = m.group(2)
        if url.startswith("http"):
            parts.append(a(url, m.group(1)))
        else:
            parts.append(f'<a href="{esc(url)}">{esc(m.group(1))}</a>')
        pos = m.end()
    parts.append(esc(text[pos:]))
    return "".join(parts)


def page_exec() -> str:
    body = []
    for title, items in exec_sections():
        body.append(f"<h2>{esc(title)}</h2><ul class=\"tight\">" + "".join(f"<li>{md_inline_to_html(i)}</li>" for i in items) + "</ul>")
    body.append(f'<p class="muted">Markdown copy: <a href="EXECUTIVE-SUMMARY.md">EXECUTIVE-SUMMARY.md</a>. Tables with per-row official sources: <a href="estimates.html">Estimates</a>, <a href="contractors.html">Contractors</a>, <a href="requirements.html">Requirements</a>.</p>')
    return layout("executive-summary.html", "Executive summary", "The important details in one page: what the requester described, what was verified from official sources, what it means, and what to do next.", "\n".join(body))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def page_index() -> str:
    n_sources = len(SOURCES)
    stats = [
        (str(len(CSLB_RECORDS)), "CSLB licence records verified"),
        ("6", "licensees with B + C-36 (both trades)"),
        ("3", "estimates — amounts UNVERIFIED"),
        (str(len(REQUIREMENTS)), "requirements registered"),
        (str(len(REPO_REVIEW)), "repository findings"),
        (str(len(FLAGS)), "items flagged for review"),
        (str(n_sources - 1), "official sources read " + READ_DATE),
    ]
    stat_html = "".join(f'<div class="card stat"><span class="n">{esc(n)}</span><span class="l">{esc(l)}</span></div>' for n, l in stats)
    cards = [
        ("executive-summary.html", "Executive summary", "Situation, verified facts, findings and next steps on one page."),
        ("requirements.html", "Requirements", "13 requirements with the official rule or record each was checked against."),
        ("estimates.html", "Estimates", "The three estimates matched to CSLB records; unverifiable amounts left blank."),
        ("contractors.html", "Contractors", "Official licence data for quoted plumbers and B + C-36 all-in-one candidates."),
        ("compliance.html", "Licensing & compliance", "CSLB classes, state statutes, SF.gov guidance and tenant-entry rules."),
        ("repo-review.html", "Repository review", "15 line-referenced findings across the repository."),
        ("verification.html", "Verification log", "Every check performed, with method, result and source."),
        ("sources.html", "Sources", f"{n_sources - 1} official sources plus one documented failed third-party retrieval."),
        ("flagged-for-review.html", "Flagged for review", f"{len(FLAGS)} unverified or attention-worthy items for the requester."),
    ]
    card_html = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="more" href="{h}">Open →</a></div>' for h, t, d in cards)
    problem = "".join(f"<li>{esc(p)}</li>" for p in BRIEF_PROBLEM)
    # Snapshot table: only official facts (one row per licensee)
    rows = []
    for k in ["generalsf", "handyman", "ace", "genteel", "rapidflow", "mannys", "expert", "bayarea", "fast", "heises"]:
        r = REC[k]
        fit = pill("ok", "B + C-36") if has_b(r) else pill("warn", "No B or C-9 on record")
        rows.append([td(f"<strong>{esc(r['name'])}</strong>"), tdt(f"#{r['lic']}"), td(pill("ok", r["status"])), tdt(classes_text(r)), td(fit), tdt(r["expires"]),
                     td(pill("ok", "insured") if r["wc"] == "Insured" else pill("warn", "exempt")), td(src(f"cslb-{r['lic']}"))])
    body = f"""
<div class="grid">{stat_html}</div>
<h2>Problem statement (as provided by the requester)</h2>
<div class="note info"><p class="muted" style="margin:0 0 6px">These statements come from the requester's brief. No official source can confirm them, so they are shown as attributed prose rather than as table values.</p><ul class="tight" style="margin:0">{problem}</ul></div>
<h2>Answer in brief</h2>
<ul class="tight">
<li>The quoted plumbers are all licensed (C-36) but none holds a drywall or general-building classification; the all-in-one requirement points to a <strong>B + C-36 licensee</strong>. Six were verified; <strong>General SF</strong> and <strong>Handyman Heroes</strong> also advertise both trades on their official sites — see <a href="contractors.html">Contractors</a>.</li>
<li>Estimate amounts cannot be confirmed from any official source and are blank/flagged; the three reported scopes describe different jobs and none covers ceiling access or restoration — see <a href="estimates.html">Estimates</a>.</li>
<li>Tenant-occupied access is governed by CIV § 1954 (written notice, 24 hours presumed reasonable); City guidance on pipes behind walls and the CSLB consumer rules are on <a href="compliance.html">Licensing &amp; compliance</a>.</li>
</ul>
<h2>Licence snapshot (official CSLB data, read {READ_DATE})</h2>
{table("snapshot", ["Licensee", "Licence", "Status", "Classifications", "Covers both trades?", "Expires", "Workers' comp", "Official source"], rows, "Ten licence records — details on the Contractors page")}
<h2>Pages</h2>
<div class="grid">{card_html}</div>
<h2>How this site treats evidence</h2>
<ul class="tight">
<li>Every table row links to an official source (CSLB, California Legislature, SF.gov, or the organisation's own site). Repository findings link to the exact lines on GitHub.</li>
<li>If a value could not be confirmed, the cell is blank and carries an <span class="pill unverified">UNVERIFIED</span> flag with the reason. Nothing is inferred or filled in.</li>
<li>Requester statements (the problem description, the reported estimates) are quoted as attributed prose, never as verified values.</li>
<li>Third-party review sites are not official; Yelp refused automated retrieval, so no ratings are shown.</li>
</ul>
"""
    return layout("index.html", SITE_TITLE, "A clean, source-linked dashboard: the three estimates, verified licence data for plumbing-plus-drywall contractors in San Francisco, the governing rules, a repository review and everything flagged for review.", body)


# ---------------------------------------------------------------------------
# Repo review markdown
# ---------------------------------------------------------------------------
def repo_review_markdown() -> str:
    out = [f"# Repository review — {READ_DATE} (session `{SESSION}`)\n",
           f"Reviewed `main` at `{MAIN_SHA}`. 63 HTML files and 714 table rows were scanned; CSLB and statutory facts on the root dashboard were re-read from the official sources. Links point to the exact lines on GitHub and to the official source used for each check.\n",
           "| ID | Area | Finding | Check / recommendation | Status | Links |", "|---|---|---|---|---|---|"]
    for f in REPO_REVIEW:
        links = " · ".join(f"[{p}{(' ' + l) if l else ''}]({GH_BLOB}{p}{('#' + l) if l else ''})" for p, l in f["locs"])
        if f["srcs"]:
            links += " · " + " · ".join(f"[{SOURCES[s]['label']}]({SOURCES[s]['url']})" for s in f["srcs"])
        status = {"ok": "Verified OK", "warn": "Needs review", "info": "Informational"}[f["sev"]]
        out.append(f"| {f['id']} | {f['area']} | {f['finding']} | {f['check']} | {status} | {links} |")
    out.append("\nAll findings are also published at `overflow-trip-lever-e9a30ab9/repo-review.html` and summarised on `flagged-for-review.html`.\n")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# JSON data exports
# ---------------------------------------------------------------------------
def data_files() -> dict[str, object]:
    cslb = []
    for r in CSLB_RECORDS:
        cslb.append(dict(business_name=r["name"], license_number=r["lic"], status=r["status"], classifications=r["classes"],
                         entity=r["entity"], issue_date=r["issued"], expire_date=r["expires"], address_as_printed=r["addr"], phone=r["phone"],
                         bond_amount=r["bond_amt"], bond_surety=r["bond_surety"], bond_number=r["bond_no"], workers_comp=r["wc"],
                         workers_comp_carrier=r["wc_carrier"], workers_comp_policy=r["wc_policy"], workers_comp_expires=r["wc_exp"],
                         workers_comp_exemption_effective=r["wc_exempt_eff"], complaint_disclosure=r["disclosure"],
                         covers_plumbing_and_general_building=has_b(r), source=SOURCES[f"cslb-{r['lic']}"]["url"], read_date=READ_DATE))
    estimates = []
    for e in ESTIMATES:
        r = REC[e["rec"]]
        estimates.append(dict(n=e["n"], company_as_written=e["brief_name"], cslb_business_name=r["name"], license_number=r["lic"],
                              license_status=r["status"], classifications=r["classes"], scope_as_reported_by_requester=e["scope"],
                              verified_amount_usd=None, verified_date=None, verification="UNVERIFIED — amount and date exist only in the requester's brief",
                              requester_reported_amount_text=e["amount_reported"], brief_list_heading_date=BRIEF_DATE_HEADING,
                              source=SOURCES[f"cslb-{r['lic']}"]["url"], read_date=READ_DATE))
    return {
        "data/cslb_records.json": cslb,
        "data/estimates.json": estimates,
        "data/requirements.json": [dict(id=r["id"], category=r["cat"], requirement=r["req"], basis=r["basis"], status=r["status"][1], sources=[SOURCES[s]["url"] for s in r["srcs"]]) for r in REQUIREMENTS],
        "data/compliance.json": [dict(topic=c["topic"], rule=c["rule"], applies=c["applies"], sources=[SOURCES[s]["url"] for s in c["srcs"]]) for c in COMPLIANCE],
        "data/repo_review.json": [dict(id=f["id"], area=f["area"], finding=f["finding"], check=f["check"], status=f["sev"], locations=[GH_BLOB + p + (("#" + l) if l else "") for p, l in f["locs"]], sources=[SOURCES[s]["url"] for s in f["srcs"]]) for f in REPO_REVIEW],
        "data/flags.json": [dict(id=f["id"], type=f["kind"], item=f["item"], detail=f["detail"], action=f["action"], sources=[SOURCES[s]["url"] for s in f["srcs"]]) for f in FLAGS],
        "data/sources.json": [dict(id=k, **v, read_date=READ_DATE) for k, v in SOURCES.items()],
        "data/verification.json": [dict(item=v["item"], method=v["method"], result=v["result"], status=v["status"], date=READ_DATE, sources=[SOURCES[s]["url"] for s in v["srcs"]]) for v in verification_rows()],
    }


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build_outputs() -> dict[str, str]:
    files: dict[str, str] = {
        "index.html": page_index(),
        "executive-summary.html": page_exec(),
        "requirements.html": page_requirements(),
        "estimates.html": page_estimates(),
        "contractors.html": page_contractors(),
        "compliance.html": page_compliance(),
        "repo-review.html": page_repo_review(),
        "verification.html": page_verification(),
        "sources.html": page_sources(),
        "flagged-for-review.html": page_flagged(),
        "assets/style.css": CSS,
        "EXECUTIVE-SUMMARY.md": exec_markdown(),
        "REPO-REVIEW.md": repo_review_markdown(),
    }
    for name, obj in data_files().items():
        files[name] = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    return files


def write_outputs(out_dir: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        p = out_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


def check_outputs(out_dir: Path, files: dict[str, str]) -> list[str]:
    problems = []
    for rel, content in files.items():
        p = out_dir / rel
        if not p.exists():
            problems.append(f"missing: {rel}")
        elif p.read_text(encoding="utf-8") != content:
            problems.append(f"stale: {rel}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify the committed output matches the generator")
    ap.add_argument("--out", default=str(REPO_ROOT / OUT_DIR_NAME), help="output directory")
    args = ap.parse_args(argv)
    out_dir = Path(args.out)
    files = build_outputs()
    if args.check:
        problems = check_outputs(out_dir, files)
        if problems:
            print("\n".join(problems))
            return 1
        print(f"OK — {len(files)} generated files are current in {out_dir}")
        return 0
    write_outputs(out_dir, files)
    print(f"wrote {len(files)} files to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
