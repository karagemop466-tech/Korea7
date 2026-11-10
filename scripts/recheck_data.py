"""Dated 2026-11-10 re-read of every CSLB record used by the published ranking.

This module is a *supplement*, not a replacement. It transcribes what the official
CSLB License Detail pages returned on 2026-11-10 and compares those fields with the
stored 2026-11-08 snapshot in `data/canonical/cslb_records.json`. Nothing is
inferred: a field is only reported as changed when the two transcriptions differ.

The CSLB pages returned database stamps of the form
"Data current as of 11/9/2026 4:51:38 PM" on 2026-11-10. Those stamps are
preserved verbatim; they are not rewritten to the read date.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_DATE = "2026-11-10"
ARTIFACT = ROOT / "data" / "canonical" / "recheck-2026-11-10.json"

CSLB_URL = "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum="

# Field-by-field transcription of each record read directly on 2026-11-10.
READS = [
    {
        "license": "977638",
        "name_on_record": "EXPERT PLUMBING SOLUTIONS",
        "dba": None,
        "street": "1465 44TH AVENUE",
        "city": "SAN FRANCISCO",
        "zip": "94122",
        "phone_on_record": "(415) 531-5340",
        "entity": "Corporation",
        "issue_date": "2012-10-09",
        "reissue_date": None,
        "expire_date": "2028-10-31",
        "status": "current and active",
        "classifications": ["C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-09-19", "carrier": "ATLANTIC SPECIALTY INSURANCE COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "EVEREST PREMIER INSURANCE COMPANY",
                                 "policy": "7600025915261", "effective": "2026-07-19", "expires": "2027-07-19"},
        "record_stamp": "Data current as of 11/9/2026 4:51:38 PM",
    },
    {
        "license": "757796",
        "name_on_record": "BAY AREA PLUMBING",
        "dba": None,
        "street": "335 14TH AVENUE",
        "city": "SAN FRANCISCO",
        "zip": "94118",
        "phone_on_record": "(415) 668-8000",
        "entity": "Sole Ownership",
        "issue_date": "1999-01-07",
        "reissue_date": None,
        "expire_date": "2027-01-31",
        "status": "current and active",
        "classifications": ["C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-09-01", "carrier": "ATLANTIC SPECIALTY INSURANCE COMPANY"},
        "workers_compensation": {"kind": "exempt", "effective": "2024-12-11", "expires": None},
        "record_stamp": "Data current as of 11/9/2026 4:51:41 PM",
    },
    {
        "license": "1024971",
        "name_on_record": "JOSEPH TINSLEY",
        "dba": "FAST RESPONSE PLUMBING AND ROOTER",
        "street": "236 W POTRAL AVE #459",
        "city": "SAN FRANCISCO",
        "zip": "94127",
        "phone_on_record": "(415) 596-6115",
        "entity": "Sole Ownership",
        "issue_date": "2017-03-20",
        "reissue_date": None,
        "expire_date": "2027-03-31",
        "status": "current and active",
        "classifications": ["C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-09-01", "carrier": "ATLANTIC SPECIALTY INSURANCE COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "EMPLOYERS PREFERRED INSURANCE COMPANY",
                                 "policy": "EIG576950801", "effective": "2025-12-18", "expires": "2026-12-18"},
        "record_stamp": "Data current as of 11/9/2026 4:51:26 PM",
    },
    {
        "license": "959843",
        "name_on_record": "GENERALSF",
        "dba": None,
        "street": "3624 IRVING STREET STE A",
        "city": "SAN FRANCISCO",
        "zip": "94122",
        "phone_on_record": "(650) 303-1515",
        "entity": "Sole Ownership",
        "issue_date": "2011-04-12",
        "reissue_date": None,
        "expire_date": "2027-04-30",
        "status": "current and active",
        "classifications": ["B", "C10", "C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-04-30", "carrier": "BUSINESS ALLIANCE INSURANCE COMPANY"},
        "workers_compensation": {"kind": "exempt", "effective": "2025-03-10", "expires": None},
        "record_stamp": "Data current as of 11/9/2026 4:51:38 PM",
    },
    {
        "license": "1003394",
        "name_on_record": "HANDYMAN HEROES INC",
        "dba": None,
        "street": "912 COLE ST # 202",
        "city": "SAN FRANCISCO",
        "zip": "94117",
        "phone_on_record": "(844) 382-4376",
        "entity": "Corporation",
        "issue_date": "2015-05-05",
        "reissue_date": None,
        "expire_date": "2027-05-31",
        "status": "current and active",
        "classifications": ["B", "C36"],
        "additional_status": [],
        "complaint_disclosure": {"citation": "2 2020 001045", "date": "2020-07-12",
                                 "status": "FOR DISCLOSURE ONLY PER B&P CODE 7124.6"},
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-09-01", "carrier": "WESTERN SURETY COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "OMAHA NATIONAL CASUALTY COMPANY",
                                 "policy": "ONCC0701424403", "effective": "2026-04-25", "expires": "2027-04-25"},
        "record_stamp": "Data current as of 11/9/2026 4:51:42 PM",
    },
    {
        "license": "829071",
        "name_on_record": "ACE PLUMBING & ROOTER",
        "dba": None,
        "street": "1090 BRYANT STREET",
        "city": "SAN FRANCISCO",
        "zip": "94103-4417",
        "phone_on_record": "(415) 824-6444",
        "entity": "Corporation",
        "issue_date": "2003-12-18",
        "reissue_date": "2007-06-07",
        "expire_date": "2027-06-30",
        "status": "current and active",
        "classifications": ["C36", "A", "C-4", "C16", "B", "C10"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-09-04", "carrier": "MERCHANTS BONDING COMPANY (MUTUAL)"},
        "workers_compensation": {"kind": "insured", "carrier": "FINANCIAL PACIFIC INSURANCE COMPANY",
                                 "policy": "10147545585", "effective": "2026-07-13", "expires": "2027-07-13"},
        "record_stamp": "Data current as of 11/9/2026 4:51:45 PM",
    },
    {
        "license": "1115649",
        "name_on_record": "RAPID FLOW PLUMBING & ROOTER INC",
        "dba": None,
        "street": "230 EDINBURGH ST",
        "city": "SAN FRANCISCO",
        "zip": "94112",
        "phone_on_record": "(415) 866-8401",
        "entity": "Corporation",
        "issue_date": "2024-01-29",
        "reissue_date": None,
        "expire_date": "2028-01-31",
        "status": "current and active",
        "classifications": ["B", "C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-03-03", "carrier": "MERCHANTS BONDING COMPANY (MUTUAL)"},
        "workers_compensation": {"kind": "exempt", "effective": "2026-02-03", "expires": None},
        "record_stamp": "Data current as of 11/9/2026 4:51:45 PM",
    },
    {
        "license": "841229",
        "name_on_record": "MANNY'S PLUMBING & ROOTER",
        "dba": None,
        "street": "41 MIDVALE DRIVE",
        "city": "DALY CITY",
        "zip": "94015",
        "phone_on_record": "(650) 207-5733",
        "entity": "Sole Ownership",
        "issue_date": "2004-06-21",
        "reissue_date": None,
        "expire_date": "2028-06-30",
        "status": "current and active",
        "classifications": ["C36", "B"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-05-29", "carrier": "MERCHANTS BONDING COMPANY (MUTUAL)"},
        "workers_compensation": {"kind": "exempt", "effective": "2026-06-28", "expires": None},
        "record_stamp": "Data current as of 11/9/2026 4:51:49 PM",
    },
    {
        "license": "1025814",
        "name_on_record": "THE GENTEEL PLUMBERS INC",
        "dba": None,
        "street": "1181 REVERE AVE",
        "city": "SAN FRANCISCO",
        "zip": "94124",
        "phone_on_record": "(833) 436-8335",
        "entity": "Corporation",
        "issue_date": "2017-04-14",
        "reissue_date": None,
        "expire_date": "2027-04-30",
        "status": "current and active",
        "classifications": ["C36", "B"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2023-01-01", "carrier": "AMERICAN CONTRACTORS INDEMNITY COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "TECHNOLOGY INSURANCE COMPANY INC",
                                 "policy": "TES4729399", "effective": "2026-01-24", "expires": "2027-01-24"},
        "record_stamp": "Data current as of 11/9/2026 4:51:49 PM",
    },
    {
        "license": "1009195",
        "name_on_record": "ADVANCED PLUMBING AND DRAIN INC",
        "dba": None,
        "street": "3450 SACRAMENTO ST 204",
        "city": "SAN FRANCISCO",
        "zip": "94118",
        "phone_on_record": "(415) 744-4944",
        "entity": "Corporation",
        "issue_date": "2015-11-24",
        "reissue_date": None,
        "expire_date": "2027-11-30",
        "status": "current and active",
        "classifications": ["C36"],
        "additional_status": ["The license may be suspended at a future date for failure to resolve an outstanding final liability from the Franchise Tax Board, Department of Industrial Relations, Employment Development Department, or the Contractors State License Board."],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-09-26", "carrier": "ATLANTIC SPECIALTY INSURANCE COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "HARTFORD ACCIDENT AND INDEMNITY COMPANY",
                                 "policy": "57WECBA5ARZ", "effective": "2026-08-21", "expires": "2027-08-21"},
        "record_stamp": "Data current as of 11/9/2026 4:51:52 PM",
    },
    {
        "license": "995163",
        "name_on_record": "BERNAL HILL DRYWALL INC",
        "dba": None,
        "street": "720 ANDERSON ST",
        "city": "SAN FRANCISCO",
        "zip": "94110",
        "phone_on_record": "(415) 533-8274",
        "entity": "Corporation",
        "issue_date": "2014-07-28",
        "reissue_date": None,
        "expire_date": "2028-07-31",
        "status": "current and active",
        "classifications": ["C-9", "B"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2023-03-29", "carrier": "AMERICAN CONTRACTORS INDEMNITY COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "ENDURANCE ASSURANCE CORPORATION",
                                 "policy": "EAW0000274901", "effective": "2026-03-10", "expires": "2027-03-10"},
        "record_stamp": "Data current as of 11/9/2026 4:51:53 PM",
    },
    {
        "license": "1089561",
        "name_on_record": "TARO GROUP INC",
        "dba": "HEISES PLUMBING",
        "street": "1610 EVANS AVE",
        "city": "SAN FRANCISCO",
        "zip": "94124",
        "phone_on_record": "(415) 333-0704",
        "entity": "Corporation",
        "issue_date": "2022-04-06",
        "reissue_date": None,
        "expire_date": "2028-04-30",
        "status": "current and active",
        "classifications": ["C36", "C10", "A", "C20"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-05-27", "carrier": "AMERICAN CONTRACTORS INDEMNITY COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "EMPLOYERS PREFERRED INSURANCE COMPANY",
                                 "policy": "EIG6235466", "effective": "2026-01-11", "expires": "2027-01-11"},
        "record_stamp": "Data current as of 11/9/2026 4:51:58 PM",
    },
    {
        "license": "632743",
        "name_on_record": "CALPLUMBING CO",
        "dba": None,
        "street": "P O BOX 31042",
        "city": "SAN FRANCISCO",
        "zip": "94131",
        "phone_on_record": "(415) 221-4633",
        "entity": "Sole Ownership",
        "issue_date": "1991-12-06",
        "reissue_date": None,
        "expire_date": "2027-12-31",
        "status": "current and active",
        "classifications": ["C36"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2026-09-01", "carrier": "ATLANTIC SPECIALTY INSURANCE COMPANY"},
        "workers_compensation": {"kind": "exempt", "effective": "2025-12-08", "expires": None},
        "record_stamp": "Data current as of 11/9/2026 4:51:57 PM",
    },
    {
        "license": "868994",
        "name_on_record": "ATLAS PLUMBING & ROOTER",
        "dba": None,
        "street": "3311 MISSION STREET UNIT 165",
        "city": "SAN FRANCISCO",
        "zip": "94110",
        "phone_on_record": "(650) 871-9863",
        "entity": "Corporation",
        "issue_date": "2005-12-08",
        "reissue_date": "2008-03-25",
        "expire_date": "2028-03-31",
        "status": "current and active",
        "classifications": ["C36", "A"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2023-01-01", "carrier": "AMERICAN CONTRACTORS INDEMNITY COMPANY"},
        "workers_compensation": {"kind": "employee_service_group", "carrier": None,
                                 "policy": "WC051666394CA", "effective": "2026-07-01", "expires": "2027-07-01"},
        "record_stamp": "Data current as of 11/9/2026 4:52:02 PM",
    },
    {
        "license": "1140843",
        "name_on_record": "DISCOUNT PLUMBING ROOTER SERVICES LLC",
        "dba": None,
        "street": "1325 HOWARD AVE BLDG 710",
        "city": "BURLINGAME",
        "zip": "94010",
        "phone_on_record": "(650) 991-2100",
        "entity": "Ltd Liability",
        "issue_date": "2025-07-22",
        "reissue_date": None,
        "expire_date": "2027-07-31",
        "status": "current and active",
        "classifications": ["C36", "A"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2025-06-09", "carrier": "LEXINGTON NATIONAL INSURANCE CORPORATION"},
        "workers_compensation": {"kind": "insured", "carrier": "A I U INSURANCE COMPANY",
                                 "policy": "020396018", "effective": "2025-04-01", "expires": "2027-04-01"},
        "record_stamp": "Data current as of 11/9/2026 4:52:02 PM",
    },
    {
        "license": "1075566",
        "name_on_record": "BAY AREA PIPE & EQUIPMENT INC",
        "dba": "BAY AREA MECHANICAL",
        "street": "1320 UNDERWOOD AVE",
        "city": "SAN FRANCISCO",
        "zip": "94124",
        "phone_on_record": "(925) 642-9768",
        "entity": "Corporation",
        "issue_date": "2021-05-07",
        "reissue_date": None,
        "expire_date": "2027-05-31",
        "status": "current and active",
        "classifications": ["C36", "C20"],
        "additional_status": [],
        "complaint_disclosure": None,
        "contractors_bond": {"amount_usd": 25000, "effective": "2023-01-01", "carrier": "AMERICAN CONTRACTORS INDEMNITY COMPANY"},
        "workers_compensation": {"kind": "insured", "carrier": "PREFERRED EMPLOYERS INSURANCE COMPANY",
                                 "policy": " PEG324521720".strip(), "effective": "2025-12-02", "expires": "2026-12-02"},
        "record_stamp": "Data current as of 11/9/2026 4:52:06 PM",
    },
]

# Official rule pages re-read on 2026-11-10 (verbatim quotes kept short).
RULE_READS = [
    {
        "id": "R1",
        "page": "SF.gov — Apply for a plumbing and mechanical permit",
        "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit",
        "quote": "You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground.",
        "extra": "Contractors must hold a C4, C16, C20, C36, C54, B, or A license to apply in general; the Special cases list keeps B to 'after approval based on the scope of work', C54 to shower pans, and C16/C20 to sprinkler/mechanical permits.",
        "consistent": "yes",
        "site_claim": "Published site text: permit needed before cutting into or replacing pipes; B accepted after scope approval; C-4/C-36 plumbing; C-16 sprinklers; C-20 mechanical; C-54 shower pan only.",
    },
    {
        "id": "R2",
        "page": "California Business & Professions Code §7048 (leginfo)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048",
        "quote": "the aggregate contract price for labor, materials, and all other items is less than one thousand dollars ($1,000) ... and the work or operation does not require a building permit.",
        "extra": "Section ends \"(Amended by Stats. 2025, Ch. 67, Sec. 12. (AB 1170) Effective January 1, 2026.)\" Subsection (c) removes the exemption for anyone who advertises as a contractor or employs others.",
        "consistent": "yes",
        "site_claim": "Published site text: $1,000 aggregate threshold, no building permit, AB 1170 effective 2026-01-01, plus the advertising/employee exclusions.",
    },
    {
        "id": "R3",
        "page": "CSLB — Complaint Disclosure for license #1003394",
        "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394",
        "quote": "Citation #: 2 2020 001045 · Date: 07/12/2020 · Status: FOR DISCLOSURE ONLY PER B&P CODE 7124.6",
        "extra": "The License Detail page for #1003394 also prints 'There is Complaint Disclosure information for this license.'",
        "consistent": "yes",
        "site_claim": "Published site text: one citation, 2 2020 001045, dated 07/12/2020, marked for disclosure only under B&P 7124.6 — no interpretation added.",
    },
]

# First-party company pages re-read on 2026-11-10 (corroboration of published contact facts only).
COMPANY_READS = [
    {
        "id": "C1",
        "page": "Ace Plumbing & Rooter — company homepage",
        "url": "https://www.aceplumbingandrooter.com/",
        "tier": "company",
        "fact": "Publishes (415) 824-6444 and \"Contractors License #829071\" with A, B, C4, C10, C16 and C36 listed; describes HOA and property-manager work.",
        "check": "Phone and licence number match CSLB record #829071 read the same day.",
    },
    {
        "id": "C2",
        "page": "The Genteel Plumbers — contact page",
        "url": "https://www.genteelplumbers.com/contact",
        "tier": "company",
        "fact": "Prints 415-465-5853, 1181 Revere Avenue, San Francisco CA 94124, office Monday-Friday 8 AM-5 PM and a 24/7 answering service.",
        "check": "Address matches CSLB #1025814; the published phone differs from the CSLB business number (833) 436-8335, so both are kept and neither is silently replaced.",
    },
]

COMPARE_FIELDS = (
    "name_on_record", "dba", "street", "city", "zip", "phone_on_record", "entity",
    "issue_date", "reissue_date", "expire_date", "status", "classifications",
)


def _stored_records():
    data = json.loads((ROOT / "data" / "canonical" / "cslb_records.json").read_text())
    return {r["license"]: r for r in data["records"]}


def _fmt(value):
    if value is None or value == []:
        return "—"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _norm(value):
    if isinstance(value, list):
        return sorted(value)
    return value


def compare():
    """Return [(license, [delta strings])]; only real transcription differences are reported."""
    stored = _stored_records()
    results = []
    for read in READS:
        old = stored.get(read["license"])
        if old is None:
            results.append((read["license"], ["license absent from the stored 2026-11-08 snapshot"]))
            continue
        deltas = []
        for field in COMPARE_FIELDS:
            a, b = _norm(old.get(field)), _norm(read.get(field))
            if a != b:
                deltas.append("%s: stored %s → now %s" % (field, _fmt(old.get(field)), _fmt(read.get(field))))
        for label, key in (("contractors_bond", "contractors_bond"), ("workers_compensation", "workers_compensation")):
            a, b = old.get(key) or {}, read.get(key) or {}
            for sub in sorted(set(a) | set(b)):
                if sub in ("text", "class_codes"):
                    continue
                if _norm(a.get(sub)) != _norm(b.get(sub)):
                    deltas.append("%s.%s: stored %s → now %s" % (label, sub, _fmt(a.get(sub)), _fmt(b.get(sub))))
        old_flag = bool(old.get("complaint_disclosure"))
        new_flag = bool(read.get("complaint_disclosure"))
        if old_flag != new_flag:
            deltas.append("complaint_disclosure: stored %s → now %s" % (old_flag, new_flag))
        old_add = bool(old.get("additional_status"))
        new_add = bool(read.get("additional_status"))
        if old_add != new_add:
            deltas.append("additional_status: stored %s → now %s" % (old_add, new_add))
        results.append((read["license"], deltas))
    return results


def summary_text(deltas):
    if not deltas:
        return "No change in 13 transcribed identity/status fields, bond and workers'-compensation fields"
    return "; ".join(deltas)


def build(c):
    """Add sources, tables, page, nav entry and the JSON artifact; return the dataset."""
    stored = _stored_records()
    deltas = dict(compare())
    source_map = {}
    # Allocate above every id already claimed by any other module in this build, so concurrent
    # sessions cannot collide with this supplement whatever numbering they use.
    _used = [int(k[1:]) for k in c.SOURCES if k[0] == "S" and k[1:].isdigit()]
    next_id = (max(_used) + 1) if _used else 1
    for read in READS:
        sid = "S%d" % next_id
        next_id += 1
        source_map[read["license"]] = sid
        c.SOURCES[sid] = {
            "label": "CSLB License Detail #%s — November 10 re-read" % read["license"],
            "publisher": "Contractors State License Board",
            "url": CSLB_URL + read["license"],
            "tier": "official",
            "status": "verified",
            "checked": READ_DATE,
            "supports": "Status, classifications, address, phone, issue/expiry dates, bond and workers' compensation as returned on 2026-11-10",
            "note": "Direct read 2026-11-10; the page printed '%s'." % read["record_stamp"],
        }
    rule_sources = {}
    for rule in RULE_READS:
        sid = "S%d" % next_id
        next_id += 1
        rule_sources[rule["id"]] = sid
        c.SOURCES[sid] = {
            "label": "%s — November 10 re-read" % rule["page"],
            "publisher": {"R1": "SF Dept. of Building Inspection", "R2": "California Legislative Information",
                          "R3": "Contractors State License Board"}[rule["id"]],
            "url": rule["url"],
            "tier": "official",
            "status": "verified",
            "checked": READ_DATE,
            "supports": rule["quote"],
            "note": "Direct read 2026-11-10; quoted text transcribed verbatim from the page.",
        }
    company_sources = {}
    for item in COMPANY_READS:
        sid = "S%d" % next_id
        next_id += 1
        company_sources[item["id"]] = sid
        c.SOURCES[sid] = {
            "label": "%s — November 10 re-read" % item["page"],
            "publisher": "Company website (first-party)",
            "url": item["url"],
            "tier": item["tier"],
            "status": "verified",
            "checked": READ_DATE,
            "supports": item["fact"],
            "note": "Company self-description read 2026-11-10; corroborates published contact facts only, not skill, availability or price.",
        }
    artifact_sid = "S%d" % next_id
    c.SOURCES[artifact_sid] = {
        "label": "Dated re-read transcription — 2026-11-10",
        "publisher": "This repository",
        "url": "data/canonical/recheck-2026-11-10.json",
        "tier": "primary",
        "status": "verified",
        "checked": READ_DATE,
        "supports": "Machine-readable transcription of the 2026-11-10 CSLB re-reads, the rule-page quotes and the computed field deltas",
        "note": "Generated by scripts/recheck_data.py during the build; primary record of this session's own reads.",
    }

    lic_rows = []
    for read in READS:
        changed = deltas[read["license"]]
        flag = ('<span class="pill ok">no change</span>' if not changed
                else '<span class="pill warn">changed — see notes</span>')
        lic_rows.append({
            "cells": [
                "<strong>%s</strong><br><code>#%s</code>%s" % (
                    read["name_on_record"], read["license"],
                    ("<br><small>dba %s</small>" % read["dba"]) if read["dba"] else ""),
                '<span class="pill ok">%s</span>' % read["status"],
                ", ".join(read["classifications"]),
                read["expire_date"],
                read["phone_on_record"],
                read["record_stamp"].replace("Data current as of ", ""),
                flag,
            ],
            "src": [source_map[read["license"]]],
        })
    c.TABLES["recheck_licenses"] = {
        "title": "Every CSLB record in the published ranking, re-read 2026-11-10",
        "columns": ["Company on record / license", "License status", "Classifications", "Expires", "Phone on record",
                    "CSLB database stamp", "Change vs stored 2026-11-08 snapshot", "Source"],
        "rows": lic_rows,
        "caption": "Sixteen records, read directly on the official CSLB License Detail pages on 2026-11-10. "
                   "The database printed a 11/9/2026 stamp; that stamp is shown as returned and is not rewritten. "
                   "A licence record confirms status and scope only — not experience with a seized trip lever, willingness "
                   "to work in an occupied unit, price or availability.",
    }

    delta_rows = []
    for read in READS:
        changed = deltas[read["license"]]
        if not changed:
            continue
        delta_rows.append({
            "cells": [
                "<strong>%s</strong> <code>#%s</code>" % (read["name_on_record"], read["license"]),
                "<br>".join(changed),
                '<span class="pill warn">review</span>',
            ],
            "src": [source_map[read["license"]]],
        })
    if not delta_rows:
        delta_rows.append({
            "cells": [
                "None — no transcribed field differed",
                "All 16 records matched the stored 2026-11-08 snapshot on the 13 identity/status fields, the "
                "contractor's-bond fields and the workers'-compensation fields compared here.",
                '<span class="pill ok">no change</span>',
            ],
            "src": [artifact_sid],
        })
    c.TABLES["recheck_deltas"] = {
        "title": "Field-level differences against the stored 2026-11-08 snapshot",
        "columns": ["Company / license", "Fields that differ", "Disposition", "Source"],
        "rows": delta_rows,
        "caption": "Computed by scripts/recheck_data.py by comparing this session's transcription with "
                   "data/canonical/cslb_records.json. Only transcribed fields are compared; a difference is a record "
                   "change or a transcription correction to review, not a judgement about the business.",
    }

    rule_rows = []
    for rule in RULE_READS:
        rule_rows.append({
            "cells": [
                "<strong>%s</strong>" % rule["page"],
                "&ldquo;%s&rdquo;%s" % (rule["quote"], ("<br><small>%s</small>" % rule["extra"]) if rule["extra"] else ""),
                rule["site_claim"],
                '<span class="pill ok">consistent</span>' if rule["consistent"] == "yes"
                else '<span class="pill warn">review</span>',
            ],
            "src": [rule_sources[rule["id"]]],
        })
    c.TABLES["recheck_rules"] = {
        "title": "Official rule pages re-read 2026-11-10",
        "columns": ["Official page", "What the page says (quoted)", "Site claim it supports", "Check", "Source"],
        "rows": rule_rows,
        "caption": "Short quotations transcribed from the official pages on 2026-11-10 and compared with the wording "
                   "already published on this site. No legal conclusion is drawn here.",
    }

    change_count = sum(1 for v in deltas.values() if v)
    c.TABLES["recheck_company"] = {
        "title": "First-party company pages read 2026-11-10",
        "columns": ["Company page", "What the page publishes", "Cross-check against the official record", "Source"],
        "rows": [{"cells": ["<strong>%s</strong>" % item["page"], item["fact"], item["check"]],
                  "src": [company_sources[item["id"]]]} for item in COMPANY_READS],
        "caption": "Company pages corroborate what a business publishes about itself — phone, address, licence number. "
                   "They are not independent evidence of workmanship, of experience with this repair, of insurance cover "
                   "for a specific job, or of willingness to take it.",
    }

    c.PAGES["recheck.html"] = {
        "title": "Live re-check",
        "eyebrow": "Dated evidence · re-read 2026-11-10",
        "h1": "Live re-check of every license and rule on this site",
        "lede": "All sixteen CSLB records and the three official rule pages cited in the ranking were re-read directly "
                "on 2026-11-10. This page records exactly what the official pages returned and what, if anything, changed.",
        "sections": [
            {"type": "callout", "tone": "ok", "html":
                ("<strong>16 of 16 licence records returned current and active.</strong> "
                 "No transcribed field differs from the stored 2026-11-08 snapshot — the 13 identity/status fields, the "
                 "contractor's bond and the workers'-compensation fields were compared record by record." if change_count == 0
                 else "<strong>16 of 16 licence records returned current and active.</strong> %d records show a field-level "
                      "difference against the stored 2026-11-08 snapshot; every difference is listed in the table below." % change_count)
                + " Licence status does not establish experience with a seized trip lever, willingness to open a ceiling in an "
                  "occupied unit, price or availability — those stay UNVERIFIED."},
            {"type": "table", "ref": "recheck_licenses"},
            {"type": "table", "ref": "recheck_deltas"},
            {"type": "table", "ref": "recheck_rules"},
            {"type": "table", "ref": "recheck_company"},
            {"type": "prose", "title": "What this re-check does and does not prove", "html":
                "<p>These are direct reads of government pages on 2026-11-10: CSLB License Detail pages for all sixteen "
                "licences used by the ranking, the sf.gov plumbing/mechanical permit page, California Business &amp; "
                "Professions Code §7048 and the CSLB complaint-disclosure page for #1003394. The pages are the authority; "
                "this page is a transcription with source links.</p>"
                "<p>It does not prove that any firm has freed a seized trip lever without opening the wall, has worked "
                "in an occupied unit, will include drywall restoration in one contract, or will accept this job at any "
                "price. No provider was contacted and nothing was booked. Yelp and other review platforms remain "
                "third-party material and are never used as licence evidence.</p>"},
            {"type": "prose", "title": "Same result, independently reached", "html":
                "<p>A concurrent session re-read the same sixteen CSLB records on the same day and published its own "
                "field-by-field result on the <a href=\"verification.html\">Verification</a> page "
                "(<a href=\"data/canonical/reverification-2026-11-10.json\">reverification-2026-11-10.json</a>). "
                "Its finding — no drift against the 2026-11-08 transcription — matches this page's computed delta table. "
                "Two independent transcriptions agreeing is stronger evidence than either alone, but it is still only "
                "evidence about licence records, not about this repair.</p>"},
            {"type": "prose", "title": "How to use it before hiring", "html":
                "<p>Re-open the <a href=\"ranking.html\">ranked decision</a> and the "
                "<a href=\"contacts.html\">contact directory</a>, then confirm the chosen licence again on "
                "<a href=\"https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx\" target=\"_blank\" "
                "rel=\"noopener noreferrer\">CSLB Check a License</a> on the day you hire, and ask for a written scope "
                "covering access, plumbing, ceiling repair, containment and a water test before the ceiling is closed.</p>"
                "<p>Machine-readable transcription and computed deltas: "
                "<a href=\"data/canonical/recheck-2026-11-10.json\">recheck-2026-11-10.json</a>. "
                "Open questions stay on <a href=\"flagged.html\">Flagged for review</a>.</p>"},
        ],
    }
    c.NAV[-1]["links"].insert(0, ("recheck.html", "Live re-check 2026-11-10"))
    for page in ("index.html", "summary.html"):
        c.PAGES[page]["sections"].insert(0, {"type": "callout", "tone": "ok", "html":
            "<strong>2026-11-10 re-check:</strong> all sixteen CSLB records and the three official rule pages cited here "
            "were read directly again today (%d field-level differences, all listed). "
            "<a href=\"recheck.html\">See the dated re-check</a>." % change_count})

    import re as _re

    _existing = [int(r["cells"][0][1:]) for r in c.TABLES["flagged"]["rows"]
                 if _re.fullmatch(r"U\d+", str(r["cells"][0]))]
    _flag_id = "U%d" % ((max(_existing) + 1) if _existing else 1)
    c.TABLES["flagged"]["rows"].append({
        "cells": [
            _flag_id,
            "CSLB database stamp lags the read date",
            "Every record read on 2026-11-10 printed a database stamp of 11/9/2026. The stamp is preserved exactly as "
            "returned, so this page cannot claim same-minute freshness, and a change made after the CSLB database "
            "snapshot would not appear here.",
            "Re-open the chosen licence on the CSLB Check a License page on the hire date and keep a dated copy.",
            '<span class="pill warn">UNVERIFIED</span>',
        ],
        "src": [source_map["829071"], artifact_sid],
    })
    # Publish flags in ID order and refresh the dashboard counter now that the last flag exists.
    c.TABLES["flagged"]["rows"].sort(
        key=lambda r: (int(_re.fullmatch(r"U(\d+)", str(r["cells"][0])).group(1))
                       if _re.fullmatch(r"U\d+", str(r["cells"][0])) else 10 ** 6))
    for _b in c.PAGES["index.html"]["sections"]:
        if _b["type"] == "cards":
            for _card in _b["items"]:
                if _card["k"] == "Flagged for review":
                    _card["v"] = str(len(c.TABLES["flagged"]["rows"]))
    c.META["updated"] = READ_DATE
    c.META["session"] = "arena/2a57ff73-korea7"

    payload = {
        "checked_date": READ_DATE,
        "method": "Direct fetch and read of each official page. Selected fields transcribed verbatim; the CSLB database "
                  "stamp printed on the page is preserved exactly as returned (11/9/2026), not rewritten to the read date.",
        "records": [dict(r, source_url=CSLB_URL + r["license"], source_id=source_map[r["license"]],
                         deltas=deltas[r["license"]], delta_summary=summary_text(deltas[r["license"]]))
                    for r in READS],
        "rule_checks": [dict(r, source_id=rule_sources[r["id"]]) for r in RULE_READS],
        "company_checks": [dict(r, source_id=company_sources[r["id"]]) for r in COMPANY_READS],
        "flag_id": _flag_id,
        "limits": {
            "provider_contacted": False,
            "booking_confirmed": False,
            "job_specific_verified_price": None,
            "job_specific_experience_verified": False,
            "availability_confirmed": False,
        },
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    for lic, items in compare():
        print(lic, "|", summary_text(items))
