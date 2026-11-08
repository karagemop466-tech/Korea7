#!/usr/bin/env python3
"""Ranked hiring decision + verified contact directory for the overflow trip-lever project.

Session arena/0e9ee506-korea7, 2026-11-08.

Inputs (all committed, all transcribed from sources read directly on 2026-11-08):
  data/canonical/cslb_records.json    official CSLB License Detail records
  data/canonical/vendor_sites.json    each business's own website, as published
  data/canonical/review_snapshots.json  third-party platform snapshots (never scored)

Design rule: the numeric score is computed ONLY from fields on the official CSLB
record. Review ratings, review counts and company marketing claims are published
alongside the ranking as clearly labelled third-party / vendor statements and are
NOT inputs to the score. No value is inferred: anything an official source does
not confirm is rendered blank and flagged UNVERIFIED.

This module is imported at the end of scripts/dashboard_content.py and merges its
sources, tables and pages into the canonical dashboard dataset.
"""
from __future__ import annotations

import datetime as _dt
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = _dt.date(2026, 11, 8)
CHECKED = "2026-11-08"

CSLB = json.loads((ROOT / "data/canonical/cslb_records.json").read_text(encoding="utf-8"))
VENDORS = json.loads((ROOT / "data/canonical/vendor_sites.json").read_text(encoding="utf-8"))
REVIEWS = json.loads((ROOT / "data/canonical/review_snapshots.json").read_text(encoding="utf-8"))
RECORDS = {r["license"]: r for r in CSLB["records"]}
SITES = VENDORS["sites"]


def esc(s):
    return html.escape(str(s), quote=True)


def pill(text, tone="info"):
    return '<span class="pill %s">%s</span>' % (tone, text)


BLANK = '<span class="blank" aria-label="blank — unverified">—</span>'
UNVER = pill("UNVERIFIED", "warn")


def ext(url, label):
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (esc(url), esc(label))


# ---------------------------------------------------------------------------
# Sources. S01-S60 already exist in dashboard_content.py; these are additive.
# ---------------------------------------------------------------------------
def _cslb_source(lic, label):
    r = RECORDS[lic]
    return {
        "label": "CSLB License Detail #%s — %s" % (lic, label),
        "publisher": "Contractors State License Board",
        "url": r["source_url"],
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Business name, address, business phone number on record, entity, issue/expiry dates, "
                    "status, classifications, bond, workers' compensation"
                    + (", liability insurance" if r.get("liability_insurance") else "")
                    + (", complaint disclosure" if r.get("complaint_disclosure") else "")
                    + (", additional status" if r.get("additional_status") else ""),
        "note": "Read directly on cslb.ca.gov; record printed '%s'." % r["record_stamp"],
    }


SOURCES = {
    "S61": _cslb_source("1025814", "The Genteel Plumbers Inc"),
    "S62": _cslb_source("1009195", "Advanced Plumbing and Drain Inc"),
    "S63": _cslb_source("995163", "Bernal Hill Drywall Inc"),
    "S64": _cslb_source("1089561", "Taro Group Inc dba Heises Plumbing"),
    "S65": _cslb_source("632743", "Calplumbing Co"),
    "S66": _cslb_source("868994", "Atlas Plumbing & Rooter"),
    "S67": _cslb_source("1140843", "Discount Plumbing Rooter Services LLC"),
    "S68": _cslb_source("1075566", "Bay Area Pipe & Equipment Inc dba Bay Area Mechanical"),
    "S69": {
        "label": "Genteel Plumbers — official contact page",
        "publisher": "The Genteel Plumbers Inc",
        "url": "https://www.genteelplumbers.com/contact",
        "tier": "company", "status": "verified", "checked": CHECKED,
        "supports": "Published phone 415-465-5853, office address 1181 Revere Avenue, office hours",
        "note": "Read directly. The published phone differs from the CSLB phone on record; both are recorded, neither is reconciled.",
    },
    "S70": {
        "label": "Bernal Hill Drywall — official site",
        "publisher": "Bernal Hill Drywall Inc",
        "url": "https://www.bernalhilldrywall.com/",
        "tier": "company", "status": "verified", "checked": CHECKED,
        "supports": "Drywall patching/finishing and build-back after water damage; states it also holds a general contractors license; estimate link tel:4155338274",
        "note": "Read directly. Service claims are the company's own; the C-9 and B classifications come from CSLB.",
    },
    "S71": {
        "label": "Rapid Flow Plumbing & Rooter — official contact page",
        "publisher": "Rapid Flow Plumbing & Rooter Inc",
        "url": "https://www.rapidflowbayarea.com/contact",
        "tier": "company", "status": "verified", "checked": CHECKED,
        "supports": "States CA #1115649 B + C-36; primary line 844-BAY-FLOW; (415) 866-8401 for photo texts; General Contracting / Remodel offered",
        "note": "Read directly. Both numbers appear on the company's own page; the CSLB record carries (415) 866-8401.",
    },
    "S72": {
        "label": "Manny's Plumbing & Rooters — official site",
        "publisher": "Manny's Plumbing & Rooters",
        "url": "https://www.mannysplumbingandremodeling.com/",
        "tier": "company", "status": "verified", "checked": CHECKED,
        "supports": "States License # 841229 and 'C-36 Plumbing / General B - Insured & Bonded'; tub install, drain replacement, kitchen/bath remodeling; service city list",
        "note": "Read directly. No phone number rendered in the content read; the CSLB phone on record is used instead.",
    },
    "S73": {
        "label": "Yelp — Plumbing Companies in San Francisco (result snapshot)",
        "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Plumbing+Companies&find_loc=San+Francisco%2C+CA",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Point-in-time ratings/review counts for Ace, Genteel and Fast Response read from result text",
        "note": "Yelp returns HTTP 403 to automated fetches (re-confirmed 2026-11-08). Values read from search-result text; third-party, not official, never scored.",
    },
    "S74": {
        "label": "Yelp — Plumbing near Mission, San Francisco (result snapshot)",
        "publisher": "Yelp", "url": "https://www.yelp.com/search?cflt=plumbing&find_loc=Mission,+San+Francisco,+CA+94110",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Ace 4.7 with a portfolio caption 'Install new bathtub with a valve inside the wall'; Genteel 4.7; 'Verified License' badges",
        "note": "Third-party result text, 2026-11-08. A Yelp 'Verified License' badge is not CSLB verification.",
    },
    "S75": {
        "label": "Yelp — Handyman Drywall near Lower Haight, San Francisco (result snapshot)",
        "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Handyman+Drywall&find_loc=Lower+Haight%2C+San+Francisco%2C+CA",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Handyman Heroes appears in a drywall-repair category with reviews describing drywall repair and rehanging",
        "note": "Third-party result text, 2026-11-08; review counts differ between result pages captured the same day.",
    },
    "S76": {
        "label": "Yelp — Handyman Services in San Francisco (result snapshot)",
        "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Handyman+Services&find_loc=San+Francisco%2C+CA",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Handyman Heroes 4.7 with a review count that differs from other result pages the same day",
        "note": "Third-party result text, 2026-11-08; not official and not scored.",
    },
    "S77": {
        "label": "Yelp — Bernal Hill Drywall business page",
        "publisher": "Yelp", "url": "https://www.yelp.com/biz/bernal-hill-drywall-san-francisco",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Category 'Drywall Installation & Repair'; services include drywall repair, wall patching, wall finish repair, wall texturing; 4.9 with 37 reviews in the result snapshot",
        "note": "Direct fetch returned HTTP 403 on 2026-11-08; values read from search-result text. Third-party only.",
    },
    "S78": {
        "label": "Yelp — Handyman Heroes business page",
        "publisher": "Yelp", "url": "https://www.yelp.com/biz/handyman-heroes-san-francisco?osq=Handyman&start=60",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Categories 'Handyman, Electricians, Plumbing'; a result snapshot shows 4.7 (201 reviews) while the page FAQ text shows 4.5 stars",
        "note": "Conflicting third-party values on the same business; recorded as observed, not reconciled. Not official, not scored.",
    },
    "S79": {
        "label": "California EDD Labor Market Information — employer details, Bernal Hill Drywall Inc",
        "publisher": "CA Employment Development Department (data provided by Data Axle)",
        "url": "https://labormarketinfo.edd.ca.gov/aspdotnet/databrowsing/empDetails.aspx?menuChoice=emp&empid=432614093&geogArea=0604000075",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Employer name, 720 Anderson St address, telephone 415-533-8274, website BERNALHILLDRYWALL.COM, owner Jerry Calderon, NAICS 238310 drywall",
        "note": "Read directly on a ca.gov host. The page states the employer information is provided by Data Axle, so it is official-hosted third-party data, not a licensing record.",
    },
    "S80": {
        "label": "CSLB — B General Building classification (B&P §7057)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "A general building contractor may not take a prime contract for other trades unless it holds the appropriate classification or subcontracts an appropriately licensed specialty contractor",
        "note": "Statutory text read directly; this is the legal basis for the single-provider gate in the ranking.",
    },
    "S81": {
        "label": "CSLB — C-9 Drywall classification",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "A drywall contractor installs gypsum wall board and assemblies and performs taping and texturing to a continuous smooth or textured surface",
        "note": "Read directly; defines the ceiling cut/patch/finish trade for the restoration partner.",
    },
    "S82": {
        "label": "CSLB record transcriptions (this project's dataset)",
        "publisher": "This project, transcribed from CSLB",
        "url": "data/canonical/cslb_records.json",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "16 License Detail records transcribed field by field, each with its source URL and 'Data current as of 11/8/2026' stamp",
        "note": "Machine-readable input to the ranking; every field is traceable to the linked CSLB record.",
    },
    "S83": {
        "label": "Business-site transcriptions (this project's dataset)",
        "publisher": "This project, transcribed from each business's own site",
        "url": "data/canonical/vendor_sites.json",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "10 official business sites read on 2026-11-08 with published phone and service statements; six license numbers have no site verified and stay blank",
        "note": "Vendor statements are verified as published, not as true. They never feed the score.",
    },
    "S84": {
        "label": "Review-platform snapshots (this project's dataset)",
        "publisher": "This project, transcribed from platform result text",
        "url": "data/canonical/review_snapshots.json",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "Six dated third-party snapshots with their result URLs and the observed rating/count ranges",
        "note": "Explicitly third-party and explicitly excluded from the ranking score.",
    },
    "S85": {
        "label": "Ranking rubric and score inputs (this site)",
        "publisher": "This project's analysis",
        "url": "ranking.html",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "The five scoring criteria, their weights, the tie-break rule and the per-candidate input values",
        "note": "Weights are analyst judgement and are labelled as such; every input value is an official CSLB field.",
    },
}

# License -> existing canonical source id (S06-S11, S56, S57) or new id.
LICENSE_SRC = {
    "977638": "S06", "757796": "S07", "1024971": "S08", "959843": "S09",
    "1003394": "S10", "829071": "S11", "1115649": "S56", "841229": "S57",
    "1025814": "S61", "1009195": "S62", "995163": "S63", "1089561": "S64",
    "632743": "S65", "868994": "S66", "1140843": "S67", "1075566": "S68",
}
SITE_SRC = {
    "977638": "S38", "757796": "S39", "1024971": "S40", "959843": "S41",
    "1003394": "S42", "829071": "S43", "1025814": "S69", "995163": "S70",
    "1115649": "S71", "841229": "S72",
}
DISPLAY = {
    "977638": "Expert Plumbing Solutions", "757796": "Bay Area Plumbing",
    "1024971": "Fast Response Plumbing & Rooter", "959843": "General SF (GENERALSF)",
    "1003394": "Handyman Heroes Inc", "829071": "Ace Plumbing & Rooter",
    "1115649": "Rapid Flow Plumbing & Rooter Inc", "841229": "Manny's Plumbing & Rooter",
    "1025814": "The Genteel Plumbers Inc", "1009195": "Advanced Plumbing and Drain Inc",
    "995163": "Bernal Hill Drywall Inc", "1089561": "Heises Plumbing (Taro Group Inc)",
    "632743": "Calplumbing Co", "868994": "Atlas Plumbing & Rooter",
    "1140843": "Discount Plumbing Rooter Services LLC", "1075566": "Bay Area Mechanical",
}

# ---------------------------------------------------------------------------
# Scoring — official CSLB fields only.
# ---------------------------------------------------------------------------
CRITERIA = [
    ("A", "Trade coverage on one license", 40,
     "C-36 Plumbing <em>and</em> B General Building (or C-9 Drywall) on the same active license = 40. "
     "C-36 with no building/drywall class = 15, because a second trade is needed for the ceiling. "
     "Restoration role: C-9 + B = 40.",
     "Classifications field on the CSLB record; legal basis is B&P §7057 as published by CSLB."),
    ("B", "Workers' compensation on record", 25,
     "Insured (or an employee service group holds the policy) with more than 60 days left at 2026-11-08 = 25. "
     "Insured but expiring within 60 days = 15. Exempt, certified 'no employees at this time' = 10.",
     "Workers' Compensation section of the CSLB record."),
    ("C", "CSLB disclosure posture", 15,
     "No complaint disclosure and no additional status = 15. Complaint disclosure present = 5. "
     "Additional status warning of possible future suspension = 0.",
     "License Status / Additional Status / Complaint Disclosure on the CSLB record."),
    ("D", "License tenure at 2026-11-08", 10,
     "First issued 10 or more years ago = 10; 5 to under 10 years = 7; under 5 years = 4.",
     "Issue Date on the CSLB record (reissue dates are not used)."),
    ("E", "Principal address on record", 10,
     "San Francisco = 10; any other California city = 6.",
     "Business Information address on the CSLB record."),
]


def _years(issue):
    d = _dt.date.fromisoformat(issue)
    return (TODAY - d).days / 365.25


def role_of(r):
    cl = set(r["classifications"])
    if "C36" in cl and ("B" in cl or "C-9" in cl):
        return "all-in-one"
    if "C36" in cl:
        return "plumbing-only"
    return "restoration-only"


def score(r):
    cl = set(r["classifications"])
    role = role_of(r)
    a = 40 if (role == "all-in-one" or (role == "restoration-only" and {"C-9", "B"} <= cl)) else 15
    wc = r["workers_compensation"]
    if wc["kind"] == "exempt":
        b, bnote = 10, "exempt — “no employees at this time”"
    else:
        days = (_dt.date.fromisoformat(wc["expires"]) - TODAY).days
        if days <= 60:
            b, bnote = 15, "insured, expires %s (%d days)" % (wc["expires"], days)
        else:
            b, bnote = 25, "insured to %s" % wc["expires"]
    if r["additional_status"]:
        c, cnote = 0, "additional status warning on the record"
    elif r["complaint_disclosure"]:
        c, cnote = 5, "complaint disclosure on the record"
    else:
        c, cnote = 15, "no disclosure on the record"
    yrs = _years(r["issue_date"])
    d = 10 if yrs >= 10 else (7 if yrs >= 5 else 4)
    e = 10 if r["city"].upper() == "SAN FRANCISCO" else 6
    return {"A": a, "B": b, "C": c, "D": d, "E": e, "total": a + b + c + d + e,
            "role": role, "bnote": bnote, "cnote": cnote, "years": yrs}


SCORES = {lic: score(r) for lic, r in RECORDS.items()}


def ranked(role):
    lic = [l for l in RECORDS if SCORES[l]["role"] == role]
    # Deterministic tie-break: higher score, then longer tenure, then lower license number.
    return sorted(lic, key=lambda l: (-SCORES[l]["total"], RECORDS[l]["issue_date"], int(l)))


ALL_IN_ONE = ranked("all-in-one")
PLUMBING_ONLY = ranked("plumbing-only")
RESTORATION = ranked("restoration-only")

# ---------------------------------------------------------------------------
# Per-candidate reasoning and cost position (analysis, not vendor claims).
# ---------------------------------------------------------------------------
REASON = {
    "829071": "Highest verified score. The CSLB record carries B and C-36 plus A, C-4, C-16 and C-10, "
              "an active workers' compensation policy and no disclosure. Its own site documents two decades of "
              "work directly for HOAs and property managers, including insurance requirements, purchase orders and "
              "not-to-exceed limits — the closest published match to a managed, tenant-occupied building. A Yelp "
              "result portfolio caption shows a bathtub installed with a valve inside the wall (third-party). "
              "Drywall self-performance is not advertised, so confirm it in writing.",
    "1025814": "B and C-36 on one active license, workers' compensation insured, no disclosure, San Francisco "
               "address. Three points behind the leader on tenure only (first licensed 2017). Its own pages list "
               "plumbing services and make no mention of drywall or ceiling restoration, so the B classification is "
               "verified while the ceiling capability is not. Two different official phone numbers exist "
               "(CSLB record vs the company contact page) — confirm which line to call.",
    "1003394": "B and C-36 with workers' compensation insured, and the strongest published evidence of the "
               "combined trade: its own site carries a customer review describing drywall patching, and a Yelp "
               "result quotes a review where the crew repaired a wall after plumbing work. Ten points are lost "
               "because CSLB shows a complaint disclosure (citation 2 2020 001045, 07/12/2020, marked for "
               "disclosure only) — read it before hiring. The site's “Licensed C-10” claim is not on the CSLB record.",
    "959843": "One license carries B, C-10 and C-36, and the site offers Building and Bathroom & Kitchen work, so "
              "the single-provider requirement is met on paper. Points are lost for the workers' compensation "
              "exemption (“no employees at this time”). Its homepage describes commercial properties, educational "
              "institutions and corporate offices as its clients, so ask specifically about a small residential "
              "repair in an occupied unit and who will attend.",
    "841229": "C-36 and B on one license, with tub installation, drain replacement and bathroom remodeling listed "
              "on its own site. Points are lost for the workers' compensation exemption and for a Daly City "
              "address on record — confirm San Francisco service. The site says “Insured & Bonded” while the "
              "record shows a workers' compensation exemption; ask what coverage applies to the attending crew.",
    "1115649": "B and C-36 on one license and a “General Contracting / Remodel” service category, so the combined "
               "scope is available. Lowest of the dual-classified set because the license was first issued in 2024 "
               "and workers' compensation is exempt. The primary call line on its contact page differs from the "
               "number on the CSLB record; both are published by the company.",
    "868994": "Plumbing-only on the verified record (C-36 and A, no building or drywall class), so the ceiling work "
              "needs a second trade or a subcontract. Strong on the other verified inputs: an employee service "
              "group holds the workers' compensation policy, no disclosure, licensed since 2005, San Francisco "
              "address. No official business website was verified in this session, so service scope and published "
              "phone stay blank.",
    "977638": "C-36 only, so it cannot self-perform the ceiling restoration under its own license. It is one of the "
              "three firms the owner reports already quoted this job, and its own site publishes the same phone and "
              "license number as the CSLB record, with fixture installation and general repair services listed. "
              "Workers' compensation insured and no disclosure. Pair with a C-9/B restoration contractor if the "
              "ceiling has to be opened.",
    "1089561": "C-36, C-10, A and C-20 but no B or C-9, so the ceiling needs a second trade. Workers' compensation "
               "insured, no disclosure, San Francisco address; the license was issued in 2022. No official business "
               "website verified this session, so scope and published phone stay blank.",
    "1140843": "The only record in this set that publishes general liability insurance ($2,000,000) alongside a "
               "$100,000 LLC employee/worker bond and workers' compensation to 2027 — relevant to risk in an "
               "occupied building. Still C-36 and A only, first licensed in 2025, and the address on record is "
               "Burlingame rather than San Francisco. Liability cover is noted here but is not a scoring criterion, "
               "because CSLB only requires it of LLC licensees.",
    "1024971": "C-36 only. The owner reports this firm quoted an adjust/repair scope rather than a replacement, and "
               "its own site says most of its work is residential for homeowners, HOAs and property managers, with "
               "free in-person estimates and per-job quotes — a good fit for a first, least-invasive attempt. "
               "Points are lost because the workers' compensation policy expires 2026-12-18, inside the 60-day "
               "window; ask for a renewal certificate if work runs past that date.",
    "1075566": "C-36 and C-20, no building or drywall class. Workers' compensation expires 2026-12-02, inside the "
               "60-day window. The record's workers' compensation codes include outside salespersons and a "
               "hardware/electrical/plumbing store category, so confirm a service crew rather than a supply "
               "counter. No official business website verified this session.",
    "757796": "C-36 only, licensed since 1999, no disclosure, San Francisco address; its own site lists leak "
              "detection, pipe repair and bathroom remodeling with a photo caption describing a galvanized drain "
              "replaced with DWV copper. Points are lost for the workers' compensation exemption. One of the three "
              "firms the owner reports quoted the job; the ceiling would need a second trade.",
    "632743": "C-36 only and the longest tenure in the set (first issued 1991), but workers' compensation is exempt "
              "and the address on record is a post-office box. No official business website verified this session, "
              "so service scope and published phone stay blank.",
    "1009195": "Ranked last on the verified inputs: the CSLB record carries an additional status warning that the "
               "license may be suspended at a future date for failure to resolve an outstanding final liability. "
               "It is C-36 only and workers' compensation is insured. Resolve that status directly with CSLB "
               "before any engagement; no official business website was verified this session.",
    "995163": "The ceiling-restoration specialist. The CSLB record carries C-9 Drywall and B General Building with "
              "workers' compensation insured under a wallboard-installation class code. Its own site describes "
              "drywall patching, level-5 finishing and complete build-back after water damage, and a state-hosted "
              "employer listing confirms the same phone and website. There is no C-36 on the record, so it is the "
              "restoration partner for a plumbing-only firm, or the general contractor that subcontracts the "
              "plumbing to a C-36 licensee.",
}

BENCH = ("Publisher benchmarks for orientation only: bathtub/shower drain replacement $500–$1,020 "
         "(average $700) and drywall/tile follow-up after a leak $300–$930.")


def cost_note(lic):
    base = BLANK + " " + UNVER + "<br><small>No official source publishes a price for this scope.</small> "
    if lic in ("977638", "757796", "1024971"):
        base += ("An owner-reported quote from this firm exists; the amount is transcribed only in the "
                 '<a href="estimates.html">Brief transcription table</a> and stays unverified. ')
    if SCORES[lic]["role"] == "all-in-one":
        base += ("Ask for <strong>one fixed price</strong> covering the from-above attempt, access from below, "
                 "ceiling cut/patch/finish and a fill-and-drain test. ")
    elif SCORES[lic]["role"] == "restoration-only":
        base += ("Price the ceiling opening, patch, texture-match and painting as a separate line, "
                 "and ask it to coordinate with the plumber's access opening. ")
    else:
        base += ("Price the plumbing separately and add a ceiling-restoration line from a C-9/B contractor; "
                 "no combined quote exists yet. ")
    return base + BENCH


def cls_text(r):
    return " · ".join(r["classifications"])


def wc_text(r):
    wc = r["workers_compensation"]
    if wc["kind"] == "exempt":
        return (pill("WC exempt", "warn") + '<br><small>“no employees at this time”, effective %s</small>'
                % esc(wc["effective"]))
    if wc["kind"] == "employee_service_group":
        return (pill("WC — employee service group", "ok")
                + '<br><small>policy %s, %s → %s</small>' % (esc(wc["policy"]), esc(wc["effective"]), esc(wc["expires"])))
    tone = "warn" if SCORES[r["license"]]["B"] == 15 else "ok"
    return (pill("WC insured", tone) + '<br><small>%s<br>%s → %s</small>'
            % (esc(wc["carrier"]), esc(wc["effective"]), esc(wc["expires"])))


def company_cell(lic):
    r = RECORDS[lic]
    parts = ["<strong>%s</strong>" % esc(DISPLAY[lic])]
    if lic in SITES:
        parts.append(ext(SITES[lic]["official_url"], "official site"))
    else:
        parts.append('<small>official site %s %s</small>' % (BLANK, UNVER))
    parts.append('<small>CSLB phone on record: <strong>%s</strong></small>' % esc(r["phone_on_record"]))
    return "<br>".join(parts)


def score_cell(lic):
    s = SCORES[lic]
    return ("<strong>%d / 100</strong><br><small>A %d · B %d · C %d · D %d · E %d</small>"
            % (s["total"], s["A"], s["B"], s["C"], s["D"], s["E"]))


def rank_rows(lics):
    rows = []
    for i, lic in enumerate(lics, 1):
        r = RECORDS[lic]
        src = [LICENSE_SRC[lic], "S80" if SCORES[lic]["role"] != "restoration-only" else "S81", "S85", "S15", "S16"]
        if lic in SITE_SRC:
            src.append(SITE_SRC[lic])
        if r["complaint_disclosure"]:
            src.append("S12")
        if lic == "995163":
            src.append("S79")
        status = pill("current and active", "ok") + "<br><small>expires %s</small>" % esc(r["expire_date"])
        if r["complaint_disclosure"]:
            status += "<br>" + pill("complaint disclosure", "warn")
        if r["additional_status"]:
            status += "<br>" + pill("additional status", "bad")
        rows.append({"cells": [
            "<strong>#%d</strong>" % i,
            company_cell(lic),
            "%s<br><small>%s</small><br>%s" % (
                ext(r["source_url"], "#%s" % lic), esc(cls_text(r)), status),
            score_cell(lic),
            esc(REASON[lic]),
            cost_note(lic),
            wc_text(r),
        ], "src": src})
    return rows


RANK_CAPTION = (
    "Order is computed, not asserted: the score uses only fields on the official CSLB record "
    "(criteria A–E below). Ties break on longer license tenure, then the lower license number. "
    "Weights are analyst judgement and are published in the rubric so the order can be recomputed; "
    "review ratings and company marketing claims are shown elsewhere on this site and are never score inputs. "
    "Every cost cell is blank and flagged because no official source publishes a price for this scope. "
    "No provider has been contacted and none has confirmed this job."
)

TABLES = {
    "rank_allinone": {
        "title": "Route 1 — ranked all-in-one candidates (C-36 plumbing + B building on one license)",
        "columns": ["Rank", "Company & contact", "CSLB license, classes, status",
                    "Score", "Why this rank (analysis)", "Cost position", "Crew cover on record", "Source"],
        "rows": rank_rows(ALL_IN_ONE),
        "caption": RANK_CAPTION + " Gate: CSLB's B classification text says a general building contractor may not "
                  "take a prime contract for other trades unless it holds the appropriate classification or "
                  "subcontracts an appropriately licensed specialty contractor — holding C-36 on the same license "
                  "is what lets one firm do the plumbing and the ceiling together.",
    },
    "rank_plumbing": {
        "title": "Route 2 — ranked plumbing-only specialists (ceiling needs a second trade)",
        "columns": ["Rank", "Company & contact", "CSLB license, classes, status",
                    "Score", "Why this rank (analysis)", "Cost position", "Crew cover on record", "Source"],
        "rows": rank_rows(PLUMBING_ONLY),
        "caption": RANK_CAPTION + " None of these records carries a B or C-9 classification, so pair the chosen "
                  "plumber with the restoration contractor below, or require a written subcontract.",
    },
    "rank_restoration": {
        "title": "Ceiling restoration partner — ranked on the drywall/building role",
        "columns": ["Rank", "Company & contact", "CSLB license, classes, status",
                    "Score", "Why this rank (analysis)", "Cost position", "Crew cover on record", "Source"],
        "rows": rank_rows(RESTORATION),
        "caption": "Scored with the same rubric, with criterion A applied to the drywall/building role. "
                  "CSLB's C-9 definition covers gypsum board installation, taping and texturing to a continuous "
                  "smooth or textured surface — the ceiling cut, patch and finish this job may need. "
                  "This record has no C-36, so it is not a plumber.",
    },
    "rubric": {
        "title": "Scoring rubric — every input is an official CSLB field",
        "columns": ["Criterion", "What it measures", "Max", "How points are assigned",
                    "Where the input comes from", "Grade", "Source"],
        "rows": [{"cells": [c[0], esc(c[1]), str(c[2]), c[3], esc(c[4]),
                            pill("input verified · weight is analyst judgement", "info")],
                  "src": ["S04", "S80", "S81", "S85"]} for c in CRITERIA],
        "caption": "Maximum 100 points. Computed at 2026-11-08 from data/canonical/cslb_records.json by "
                  "scripts/ranking_data.py, so the order is reproducible from the committed inputs. "
                  "Nothing in the score comes from a review platform, a marketing claim or an owner-supplied figure.",
    },
    "call_order": {
        "title": "Recommended call order and what to ask",
        "columns": ["Step", "Who", "Verified phone", "Ask for exactly this", "Why here", "Source"],
        "rows": [],
        "caption": "Call order follows the computed ranking within each route. Phone numbers are the business "
                  "numbers on the official CSLB record; where a company publishes a different line on its own "
                  "site, both appear in the contact directory and the difference is flagged. No outreach has "
                  "been performed by this project.",
    },
    "contacts": {
        "title": "Verified contact directory — official links and phone numbers",
        "columns": ["Company", "Phone on the CSLB record (official)", "Phone published on its own site",
                    "Official business website", "Do they match?", "License", "Source"],
        "rows": [],
        "caption": "The CSLB License Detail record publishes a Business Phone Number for every licensee; that is "
                  "the official value in column 2. Column 3 is filled only where the number appeared in the "
                  "business's own page content read on 2026-11-08; otherwise it is blank and flagged. "
                  "Third-party directory numbers are not used.",
    },
    "cslb_register": {
        "title": "CSLB register — all 16 license records re-read on 2026-11-08",
        "columns": ["License & name on record", "Classifications", "Status / expiry", "First issued",
                    "Workers' compensation on record", "Bond / liability on record", "Address on record",
                    "Change vs the 2026-11-07 snapshot", "Source"],
        "rows": [],
        "caption": "Every row was read directly from the issuing agency; each record printed "
                  "“Data current as of 11/8/2026”. Fields are transcribed verbatim into "
                  "data/canonical/cslb_records.json. A license record establishes classification and status only — "
                  "it does not establish ability to perform this specific repair.",
    },
    "reviews_1108": {
        "title": "Review-platform snapshots re-captured 2026-11-08 (third-party, not scored)",
        "columns": ["Candidate", "Platform", "Rating observed", "Review count observed",
                    "What the result text shows", "Status", "Source"],
        "rows": [],
        "caption": "Yelp returned HTTP 403 to a direct page fetch again on 2026-11-08, so these values were read "
                  "from platform result text returned by web search. Counts differ between result pages captured "
                  "on the same day and are reported as observed ranges rather than reconciled. None of this is an "
                  "official source and none of it feeds the ranking score.",
    },
    "scope_evidence": {
        "title": "What each business publishes about the two trades this job needs",
        "columns": ["Company", "Plumbing scope as published", "Drywall / building scope as published",
                    "Occupied-unit or managed-building statement", "Grade", "Source"],
        "rows": [],
        "caption": "Transcribed from each business's own website on 2026-11-08. These are vendor statements: "
                  "verified as published, not verified as true, and not score inputs. Where no site was verified "
                  "the cells are blank and flagged. No official source rates job-specific experience.",
    },
}

# --- call order -------------------------------------------------------------
_order = ALL_IN_ONE + PLUMBING_ONLY[:3]
_steps = []
for i, lic in enumerate(_order, 1):
    r = RECORDS[lic]
    s = SCORES[lic]
    if s["role"] == "all-in-one":
        ask = ("One written fixed-price scope: attempt removal from above first; if it cannot be done safely, "
               "open the ceiling below, replace the waste-and-overflow, patch/texture-match and paint the ceiling, "
               "then fill-and-drain test. Confirm dust containment, floor protection, tenant access windows and "
               "who attends. Confirm the ceiling work is self-performed under the B classification.")
        why = "Rank %d on Route 1 (score %d). Both trades on one verified license." % (ALL_IN_ONE.index(lic) + 1, s["total"])
    else:
        ask = ("Plumbing-only written scope for the waste-and-overflow, plus a named C-9/B subcontractor for the "
               "ceiling, or accept a separate ceiling quote. Confirm whether a from-above attempt is possible "
               "before any ceiling is opened.")
        why = "Rank %d on Route 2 (score %d). No building class on the record, so a second trade is required." % (
            PLUMBING_ONLY.index(lic) + 1, s["total"])
    src = [LICENSE_SRC[lic], "S85"]
    if lic in SITE_SRC:
        src.append(SITE_SRC[lic])
    _steps.append({"cells": [str(i), esc(DISPLAY[lic]), "<strong>%s</strong>" % esc(r["phone_on_record"]),
                             esc(ask), esc(why)], "src": src})
_steps.append({"cells": [
    str(len(_steps) + 1), esc("Bernal Hill Drywall Inc — ceiling restoration"),
    "<strong>%s</strong>" % esc(RECORDS["995163"]["phone_on_record"]),
    esc("Separate line item for the ceiling: opening, patch, tape, texture match and paint, coordinated with the "
        "plumber's access. Ask for dust containment and a made-good finish in an occupied storage unit."),
    esc("C-9 Drywall + B General Building verified; the restoration partner if Route 2 is chosen.")],
    "src": ["S63", "S70", "S79", "S81"]})
TABLES["call_order"]["rows"] = _steps

# --- contacts ---------------------------------------------------------------
_crows = []
for lic in sorted(RECORDS, key=lambda l: (-SCORES[l]["total"], DISPLAY[l])):
    r = RECORDS[lic]
    site = SITES.get(lic)
    if site and site["published_phone"]:
        pub = "<strong>%s</strong>" % esc(site["published_phone"])
        same = site["published_phone"].strip() == r["phone_on_record"].strip()
        norm_pub = "".join(ch for ch in site["published_phone"] if ch.isdigit())
        norm_rec = "".join(ch for ch in r["phone_on_record"] if ch.isdigit())
        if norm_pub and norm_pub == norm_rec:
            match = pill("match", "ok")
        elif lic == "1115649":
            match = pill("both published by the company", "info") + "<br><small>contact page primary line differs; the CSLB number also appears on that page for photo texts</small>"
        else:
            match = pill("differs — flagged", "warn") + "<br><small>%s</small>" % esc(site["phone_note"])
    else:
        pub = BLANK + " " + UNVER
        match = BLANK + " " + UNVER + "<br><small>%s</small>" % esc(
            site["phone_note"] if site else "No official business website verified in this session.")
    website = ext(site["official_url"], site["official_url"].replace("https://", "")) if site else BLANK + " " + UNVER
    src = [LICENSE_SRC[lic]] + ([SITE_SRC[lic]] if lic in SITE_SRC else [])
    if lic == "995163":
        src.append("S79")
    _crows.append({"cells": [
        "<strong>%s</strong>" % esc(DISPLAY[lic]),
        "<strong>%s</strong><br><small>Business Phone Number on the CSLB record</small>" % esc(r["phone_on_record"]),
        pub, website, match, ext(r["source_url"], "#%s" % lic)], "src": src})
TABLES["contacts"]["rows"] = _crows

# --- CSLB register ----------------------------------------------------------
_prev = {"977638", "757796", "1024971", "959843", "1003394", "829071", "1115649", "841229"}
_reg = []
for lic in sorted(RECORDS, key=lambda l: DISPLAY[l].lower()):
    r = RECORDS[lic]
    bond = "$25,000 contractor's bond<br><small>effective %s</small>" % esc(r["contractors_bond"]["effective"])
    if r.get("llc_worker_bond"):
        bond += "<br><small>+ $100,000 LLC employee/worker bond</small>"
    if r.get("liability_insurance"):
        bond += "<br><small>+ $2,000,000 liability insurance to %s</small>" % esc(r["liability_insurance"]["expires"])
    status = pill("current and active", "ok") + "<br><small>expires %s</small>" % esc(r["expire_date"])
    if r["complaint_disclosure"]:
        status += "<br>" + pill("complaint disclosure", "warn")
    if r["additional_status"]:
        status += "<br>" + pill("may be suspended at a future date", "bad")
    change = ("No change to status, classes or expiry vs the 2026-11-07 reading; re-read directly today."
              if lic in _prev else "Newly transcribed in this session from the official record.")
    src = [LICENSE_SRC[lic], "S82"]
    if r["complaint_disclosure"]:
        src.append("S12")
    _reg.append({"cells": [
        "%s<br><strong>%s</strong>%s" % (ext(r["source_url"], "#%s" % lic), esc(r["name_on_record"]),
                                        ("<br><small>dba %s</small>" % esc(r["dba"])) if r["dba"] else ""),
        esc(cls_text(r)), status, esc(r["issue_date"]), wc_text(r), bond,
        esc("%s, %s %s" % (r["street"].title(), r["city"].title(), r["zip"])), esc(change)], "src": src})
TABLES["cslb_register"]["rows"] = _reg

# --- reviews ----------------------------------------------------------------
_rev_src = {
    "829071": ["S74", "S73"], "1025814": ["S74", "S73"],
    "1003394": ["S75", "S76", "S78"], "995163": ["S77"],
    "959843": ["S76"], "1024971": ["S40"],
}
TABLES["reviews_1108"]["rows"] = [{"cells": [
    esc(s["candidate"]), esc(s["platform"]), esc(s["rating"]), esc(s["review_count"]),
    esc(s["quote"]), pill("third-party snapshot — UNVERIFIED", "warn")],
    "src": _rev_src[s["license"]] + ["S84"]} for s in REVIEWS["snapshots"]]

# --- scope evidence ---------------------------------------------------------
PLUMB_SUMMARY = {
    "977638": "General plumbing repairs, drain and clog work, water heaters, sewer lines, fixture installations.",
    "757796": "Leak detection and pipe repair, drain cleaning, kitchen and bathroom remodeling; photo captions describe a galvanized drain replaced with DWV copper and a bathtub/faucet installation.",
    "1024971": "Plumbing repair and replacement, sewer line service, water heaters, hydro jetting, drain cleaning, leak detection.",
    "959843": "Plumbing is one of four service categories (Electrical, Plumbing, Building, Bathroom & Kitchen).",
    "1003394": "Plumbing block lists leaky faucets, water heaters, toilets and “New Water & Waste Lines”, labelled Licensed C-36.",
    "829071": "Residential and commercial plumbing, sewer and drain repair, leak detection, fixture replacement/repair, water heaters, backflow, fire protection.",
    "1025814": "Water heaters, toilets, hydro jetting, leak detection, drain and sewer services, trenchless sewer replacement.",
    "1115649": "Estimate form lists drain cleaning, water heaters, leak detection, sewer line, pipe repair/repiping and fixture installation.",
    "841229": "Sewer line repair, hydro jetting, re-piping, water heaters, faucets/sinks/toilets, “Tub Install & Lavy Sink”, drain cleaning and drain replacement.",
    "995163": "No plumbing service published; no C-36 on the CSLB record.",
}
DRYWALL_SUMMARY = {
    "977638": "No drywall, ceiling or building service listed.",
    "757796": "Bathroom plumbing remodeling listed; no drywall or ceiling restoration service listed.",
    "1024971": "No drywall or building service listed.",
    "959843": "Building and Bathroom & Kitchen categories offered; B classification on the CSLB record.",
    "1003394": "Construction block lists Kitchens & Bathrooms and Licensed GC; a company-published review describes drywall patching.",
    "829071": "No drywall service advertised; B General Building is on the CSLB record and on the company's own certification list.",
    "1025814": "No drywall or building service listed, although B is on the CSLB record.",
    "1115649": "“General Contracting / Remodel” is an offered service category; B is on the CSLB record.",
    "841229": "Kitchen and bathroom remodeling listed; site states “C-36 Plumbing / General B”.",
    "995163": "Core business: drywall installation and finishing, patching and painting, level 5 smooth finish, texture matching, and complete build-back after water, fire or mold remediation.",
}
OCCUPIED = {
    "977638": "Homeowners in San Francisco and nearby cities; no managed-building statement.",
    "757796": "Residential and commercial, 24/7 emergency, same-day service; no managed-building statement.",
    "1024971": "“For houses, apartments, and HOAs across San Francisco”; “Most of our work is residential for homeowners, HOAs, and property managers.”",
    "959843": "Clients described as commercial properties, educational institutions and corporate offices.",
    "1003394": "Marin & SF County home services; company-published reviews describe work inside occupied homes.",
    "829071": "Two decades serving HOAs and property management companies, including insurance requirements, purchase orders and not-to-exceed limits.",
    "1025814": "Same-day service, office hours Mon–Fri 8–5 with a 24/7 answering service; no managed-building statement.",
    "1115649": "Mon–Fri 7am–7pm with 24/7 emergency; service area SF, Oakland, San Jose and beyond.",
    "841229": "Residential and commercial; service city list covers San Mateo and San Francisco counties.",
    "995163": "Residential and commercial drywall; build-back after remediation implies work in occupied properties, but no tenant statement is published.",
}
TABLES["scope_evidence"]["rows"] = [{"cells": [
    "<strong>%s</strong>" % esc(DISPLAY[lic]), esc(PLUMB_SUMMARY[lic]), esc(DRYWALL_SUMMARY[lic]),
    esc(OCCUPIED[lic]), pill("vendor statement — not independent verification", "info")],
    "src": [SITE_SRC[lic], LICENSE_SRC[lic], "S83"]}
    for lic in ["829071", "1025814", "1003394", "959843", "841229", "1115649",
                "977638", "757796", "1024971", "995163"]]

# ---------------------------------------------------------------------------
# New flags and findings, appended to the canonical tables by the merge block.
# ---------------------------------------------------------------------------
NEW_FLAGS = [
    (["U21", "Genteel Plumbers publishes two different official phone numbers",
      "The CSLB record for #1025814 shows (833) 436-8335; the company's own contact page shows 415-465-5853. "
      "Third-party directories show further numbers. Neither official value is inferred or reconciled.",
      "Call both numbers or ask the company which line dispatches service; keep the CSLB value as the record copy.",
      UNVER], ["S61", "S69"]),
    (["U22", "Advanced Plumbing and Drain #1009195 carries a CSLB additional-status warning",
      "The official record states the license may be suspended at a future date for failure to resolve an "
      "outstanding final liability from the FTB, DIR, EDD or CSLB. It is still current and active today.",
      "Re-check the record on the hire date and ask CSLB what remains outstanding before any engagement.",
      pill("verified warning", "bad")], ["S62"]),
    (["U23", "Handyman Heroes' site claims a C-10 classification that is not on its CSLB record",
      "The electrical block on the company's homepage says “Licensed C-10”; the CSLB record for #1003394 lists "
      "only B and C-36. Re-confirmed directly on both sources 2026-11-08.",
      "Ask which license the electrical work would run under; do not rely on the site claim.",
      UNVER], ["S42", "S10"]),
    (["U24", "Yelp ratings and review counts differ between result pages captured the same day",
      "On 2026-11-08 Handyman Heroes appeared with 201, 389 and 402 reviews and one page's FAQ text said 4.5 stars "
      "while the header said 4.7; Ace appeared as both 1.4k and 1.5k; Genteel between 475 and 532.",
      "Treat platform numbers as drifting snapshots. They are excluded from the ranking score.",
      pill("third-party — UNVERIFIED", "warn")], ["S75", "S76", "S78", "S73", "S74"]),
    (["U25", "Two workers' compensation policies expire inside 60 days",
      "#1024971 expires 2026-12-18 and #1075566 expires 2026-12-02. Both are insured today, so both lose points "
      "on criterion B rather than being excluded.",
      "If work extends past those dates, request a renewal certificate before the crew returns.",
      pill("verified dates", "warn")], ["S08", "S68"]),
    (["U26", "Four shortlisted firms are workers'-compensation exempt",
      "#757796, #959843, #1115649 and #841229 certified “no employees at this time”. Manny's site nonetheless says "
      "“Insured & Bonded”. An exemption is not a statement about general liability cover.",
      "Ask who physically attends and what liability coverage applies to them in a tenant-occupied unit.",
      pill("verified exemption", "warn")], ["S07", "S09", "S56", "S57", "S72"]),
    (["U27", "No candidate publishes a price for this scope",
      "Every cost cell on the ranking pages is blank and flagged. The only figures available are the owner's "
      "three quotes (unverified, transcribed on the brief page) and national publisher benchmarks.",
      "Obtain written fixed-price scopes; the rubric ranks verified licence facts, not price.",
      UNVER], ["S44", "S15", "S16", "S85"]),
    (["U28", "Dual classification does not prove the firm will self-perform the drywall",
      "Genteel and Ace hold B on the CSLB record but advertise no drywall or ceiling service on their own sites. "
      "CSLB verifies classes, not capability or willingness.",
      "Get written confirmation that the ceiling opening, patch, texture match and paint are in the same contract.",
      UNVER], ["S61", "S11", "S69", "S43", "S80"]),
    (["U29", "Six verified licensees have no official business website confirmed in this session",
      "#1009195, #1089561, #632743, #868994, #1140843 and #1075566 are verified on CSLB, but their published phone "
      "and service-scope cells stay blank rather than being filled from directories.",
      "Verify a business site and phone directly before adding them to a call list.",
      UNVER], ["S62", "S64", "S65", "S66", "S67", "S68"]),
    (["U30", "Ranking weights are analyst judgement",
      "The five criteria and their weights were chosen for this job's constraints; only the input values are "
      "official. A different weighting can reorder candidates.",
      "Recompute with scripts/ranking_data.py if the priorities change; the rubric publishes every weight.",
      pill("analysis — disclosed", "info")], ["S85", "S82", "S80"]),
    (["U31", "General SF describes commercial, educational and corporate clients",
      "Its homepage does not describe small residential repairs in occupied dwellings, although the license "
      "covers building and plumbing.",
      "Ask directly whether it takes a single-unit residential repair with tenant access windows.",
      UNVER], ["S41", "S09"]),
    (["U32", "State-hosted employer listing is third-party data",
      "The EDD Labor Market Information page used to corroborate Bernal Hill Drywall's phone and website states "
      "the employer information is provided by Data Axle. It is official-hosted, not a licensing record.",
      "Use CSLB for licence facts; use the company's own site for its published contact.",
      pill("graded", "info")], ["S79", "S63", "S70"]),
]

NEW_FINDINGS = [
    (["F12", "Six firms can legally do both trades under one license, not five",
      "Re-reading every cited license on 2026-11-08 added The Genteel Plumbers #1025814 (C-36 + B) to the "
      "dual-classified set already published: #829071, #959843, #1003394, #1115649, #841229.",
      pill("verified", "ok")], ["S61", "S11", "S09", "S10", "S56", "S57", "S80"]),
    (["F13", "A ranked, reproducible decision order now exists",
      "Scores are computed from five official CSLB fields only. Route 1 order: "
      + ", ".join("%s (%d)" % (DISPLAY[l], SCORES[l]["total"]) for l in ALL_IN_ONE)
      + ". Route 2 and the restoration partner are ranked on the same rubric.",
      pill("analysis on verified inputs", "info")], ["S85", "S82"]),
    (["F14", "Every candidate now has an officially published phone number",
      "CSLB License Detail records publish a Business Phone Number, so all 16 licensees have a verified contact "
      "number with an official source link. Company-published numbers were added where they were actually read; "
      "differences are flagged rather than reconciled.",
      pill("verified", "ok")], ["S82", "S83", "S69", "S71"]),
    (["F15", "A dedicated C-9 drywall partner is verified for the two-trade route",
      "Bernal Hill Drywall Inc #995163 holds C-9 and B with workers' compensation insured under a "
      "wallboard-installation class code, and its own site describes patching, texture matching and build-back "
      "after water damage.",
      pill("verified", "ok")], ["S63", "S70", "S79", "S81"]),
    (["F16", "Review evidence for the exact combination exists but is third-party only",
      "A Yelp result quotes a Handyman Heroes review describing a wall repair after plumbing work, and an Ace "
      "portfolio caption describes a bathtub installed with a valve inside the wall. Neither is an official "
      "source, so neither affects the score.",
      pill("third-party — UNVERIFIED", "warn")], ["S75", "S74", "S84"]),
]

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
PAGES = {
    "ranking.html": {
        "title": "Ranked hiring decision",
        "eyebrow": "Decision analysis · San Francisco · scored 2026-11-08",
        "h1": "Who to hire, in order",
        "lede": "A computed ranking of every verified candidate, split by the two ways this job can be bought: "
                "one firm that holds both the plumbing and the building classification, or a plumber paired with a "
                "drywall contractor. Every score input is a field on an official CSLB record. Reviews and company "
                "marketing are published as labelled third-party evidence and never scored. Costs stay blank "
                "where no official source publishes them.",
        "sections": [
            {"type": "cards", "items": [
                {"k": "License records re-read", "v": "16", "s": "All read directly on CSLB, 2026-11-08", "tone": "ok"},
                {"k": "All-in-one candidates", "v": str(len(ALL_IN_ONE)), "s": "C-36 + B on one active license", "tone": "ok"},
                {"k": "Plumbing-only specialists", "v": str(len(PLUMBING_ONLY)), "s": "Need a second trade for the ceiling", "tone": "info"},
                {"k": "Published prices for this scope", "v": "0", "s": "Every cost cell blank and flagged", "tone": "warn"},
            ]},
            {"type": "callout", "tone": "info", "html":
                "<strong>How to read this page.</strong> Route 1 is the preferred purchase: one contract, one "
                "contractor, both trades. Route 2 plus the restoration partner is the fallback when the best "
                "plumber for the concealed waste-and-overflow does not hold a building classification. The "
                "score ranks <em>verified licence facts</em> — it is not a price comparison and not a guarantee "
                "of workmanship. No provider has been contacted and none has confirmed this job."},
            {"type": "table", "ref": "rank_allinone"},
            {"type": "table", "ref": "rank_plumbing"},
            {"type": "table", "ref": "rank_restoration"},
            {"type": "table", "ref": "rubric"},
            {"type": "table", "ref": "call_order"},
            {"type": "table", "ref": "scope_evidence"},
            {"type": "callout", "tone": "warn", "html":
                "<strong>Limits of this ranking.</strong> CSLB records establish classification, status, bond and "
                "insurance — not the ability to remove this particular trip lever without damaging concealed "
                "pipework, and not experience in an occupied unit. Those remain unverified and are listed on "
                '<a href="flagged.html">Flagged for Review</a>. See also <a href="contacts.html">the contact '
                'directory</a>, <a href="estimates.html">Estimates</a> and <a href="findings.html">Findings</a>.'},
        ],
    },
    "contacts.html": {
        "title": "Contacts & license register",
        "eyebrow": "Verified directory · read 2026-11-08",
        "h1": "Official links, phone numbers and license records",
        "lede": "Every phone number in the second column is the Business Phone Number published on the official "
                "CSLB license record. Company-published numbers and websites were added only where they were read "
                "on the business's own pages; anything else is blank and flagged. Nothing is taken from a "
                "third-party directory.",
        "sections": [
            {"type": "table", "ref": "contacts"},
            {"type": "table", "ref": "cslb_register"},
            {"type": "table", "ref": "reviews_1108"},
            {"type": "callout", "tone": "info", "html":
                'Machine-readable inputs: <a href="data/canonical/cslb_records.json">cslb_records.json</a>, '
                '<a href="data/canonical/vendor_sites.json">vendor_sites.json</a> and '
                '<a href="data/canonical/review_snapshots.json">review_snapshots.json</a>. '
                'Re-run the ranking with <code>python3 scripts/build_dashboard.py</code>. '
                'Re-check the chosen license at <a href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                'target="_blank" rel="noopener noreferrer">CSLB Check a License</a> on the hire date.'},
        ],
    },
}

SUMMARY_BLOCK = {
    "type": "prose",
    "title": "Ranked recommendation (added 2026-11-08)",
    "html": (
        "<p>All sixteen license records cited anywhere in this project were re-read directly on CSLB on "
        "2026-11-08, and every one is <strong>current and active</strong>. Six firms hold C-36 Plumbing "
        "<em>and</em> B General Building on a single license, which is what lets one contractor perform the "
        "plumbing and the ceiling restoration under one contract. The ranking is computed from five official "
        "CSLB fields — trade coverage, workers' compensation, disclosure posture, tenure and address — so it can "
        "be recomputed from the committed data. Reviews and marketing claims are never score inputs.</p>"
        "<ol class=\"tight\">"
        + "".join("<li><strong>%s</strong> — score %d/100. %s</li>" % (
            esc(DISPLAY[l]), SCORES[l]["total"], esc(REASON[l].split(". ")[0] + "."))
            for l in ALL_IN_ONE[:3])
        + "</ol>"
        "<p>The full order, the plumbing-only fallback list, the C-9 drywall partner and the rubric are on "
        '<a href="ranking.html">Ranked hiring decision</a>; official links and phone numbers for all sixteen '
        'licensees are on <a href="contacts.html">Contacts &amp; license register</a>. No candidate publishes a '
        'price for this scope, so every cost cell is blank and flagged; the only figures available are the '
        'owner-reported quotes (unverified) and national publisher benchmarks. Two records need attention before '
        'hiring: a complaint disclosure on '
        + ext(RECORDS["1003394"]["source_url"], "#1003394")
        + ' and an additional-status warning on '
        + ext(RECORDS["1009195"]["source_url"], "#1009195")
        + '.</p>'
    ),
}
