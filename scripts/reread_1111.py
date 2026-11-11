"""Dated 2026-11-11 re-read of every CSLB licence record used on the dashboard.

Session ``arena/12cacfe5-korea7``. Supplement only: it does not rewrite the
historical 2026-11-08 snapshot, the 2026-11-10 re-check, scores or rankings.

What was done
-------------
Each official CSLB License Detail page below was fetched and read directly on
2026-11-11 (UTC). Fields are transcribed verbatim. Every page printed a
database stamp of the form "Data current as of 11/10/2026 6:1x:xx PM"; those
stamps are preserved exactly as returned and are not rewritten to the read date.

Comparison baselines (computed, never asserted):
* the sixteen scored records -> ``recheck_data.READS`` (direct reads 2026-11-10);
* the separately checked #1034873 -> ``data/canonical/session-1012-verification.json``.

The only derived numbers are calendar arithmetic: days from the read date to
each workers'-compensation policy expiry printed on the record. No value is
inferred, and nothing here says anything about workmanship, job acceptance,
price or availability.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_DATE = "2026-11-11"
SESSION = "arena/12cacfe5-korea7"
ARTIFACT = ROOT / "data" / "canonical" / "reread-2026-11-11.json"
CSLB_URL = "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum="
CHECK_A_LICENSE = "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx"
WATCH_DAYS = 60  # same 60-day window the published ranking rubric uses for criterion B

# Source ids: 133-156 and 200-213 are used by earlier sessions; this session uses 300+.
FIRST_SID = 300


def _wc(kind, carrier=None, policy=None, effective=None, expires=None):
    return {"kind": kind, "carrier": carrier, "policy": policy, "effective": effective, "expires": expires}


def _bond(amount, effective, carrier):
    return {"amount_usd": amount, "effective": effective, "carrier": carrier}


# --- Field-by-field transcription, read directly 2026-11-11 ----------------------------
READS = [
    {"license": "977638", "name_on_record": "EXPERT PLUMBING SOLUTIONS", "dba": None,
     "street": "1465 44TH AVENUE", "city": "SAN FRANCISCO", "zip": "94122", "phone_on_record": "(415) 531-5340",
     "entity": "Corporation", "issue_date": "2012-10-09", "reissue_date": None, "expire_date": "2028-10-31",
     "status": "current and active", "classifications": ["C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-09-19", "ATLANTIC SPECIALTY INSURANCE COMPANY"),
     "workers_compensation": _wc("insured", "EVEREST PREMIER INSURANCE COMPANY", "7600025915261", "2026-07-19", "2027-07-19"),
     "record_stamp": "Data current as of 11/10/2026 6:16:51 PM"},
    {"license": "757796", "name_on_record": "BAY AREA PLUMBING", "dba": None,
     "street": "335 14TH AVENUE", "city": "SAN FRANCISCO", "zip": "94118", "phone_on_record": "(415) 668-8000",
     "entity": "Sole Ownership", "issue_date": "1999-01-07", "reissue_date": None, "expire_date": "2027-01-31",
     "status": "current and active", "classifications": ["C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2026-09-01", "ATLANTIC SPECIALTY INSURANCE COMPANY"),
     "workers_compensation": _wc("exempt", effective="2024-12-11", expires=None),
     "record_stamp": "Data current as of 11/10/2026 6:17:53 PM"},
    {"license": "1024971", "name_on_record": "JOSEPH TINSLEY", "dba": "FAST RESPONSE PLUMBING AND ROOTER",
     "street": "236 W POTRAL AVE #459", "city": "SAN FRANCISCO", "zip": "94127", "phone_on_record": "(415) 596-6115",
     "entity": "Sole Ownership", "issue_date": "2017-03-20", "reissue_date": None, "expire_date": "2027-03-31",
     "status": "current and active", "classifications": ["C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2026-09-01", "ATLANTIC SPECIALTY INSURANCE COMPANY"),
     "workers_compensation": _wc("insured", "EMPLOYERS PREFERRED INSURANCE COMPANY", "EIG576950801", "2025-12-18", "2026-12-18"),
     "record_stamp": "Data current as of 11/10/2026 6:17:36 PM"},
    {"license": "959843", "name_on_record": "GENERALSF", "dba": None,
     "street": "3624 IRVING STREET STE A", "city": "SAN FRANCISCO", "zip": "94122", "phone_on_record": "(650) 303-1515",
     "entity": "Sole Ownership", "issue_date": "2011-04-12", "reissue_date": None, "expire_date": "2027-04-30",
     "status": "current and active", "classifications": ["B", "C10", "C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-04-30", "BUSINESS ALLIANCE INSURANCE COMPANY"),
     "workers_compensation": _wc("exempt", effective="2025-03-10", expires=None),
     "record_stamp": "Data current as of 11/10/2026 6:18:01 PM"},
    {"license": "1003394", "name_on_record": "HANDYMAN HEROES INC", "dba": None,
     "street": "912 COLE ST # 202", "city": "SAN FRANCISCO", "zip": "94117", "phone_on_record": "(844) 382-4376",
     "entity": "Corporation", "issue_date": "2015-05-05", "reissue_date": None, "expire_date": "2027-05-31",
     "status": "current and active", "classifications": ["B", "C36"], "additional_status": [],
     "complaint_disclosure": "There is Complaint Disclosure information for this license.",
     "contractors_bond": _bond(25000, "2026-09-01", "WESTERN SURETY COMPANY"),
     "workers_compensation": _wc("insured", "OMAHA NATIONAL CASUALTY COMPANY", "ONCC0701424403", "2026-04-25", "2027-04-25"),
     "record_stamp": "Data current as of 11/10/2026 6:16:14 PM"},
    {"license": "829071", "name_on_record": "ACE PLUMBING & ROOTER", "dba": None,
     "street": "1090 BRYANT STREET", "city": "SAN FRANCISCO", "zip": "94103-4417", "phone_on_record": "(415) 824-6444",
     "entity": "Corporation", "issue_date": "2003-12-18", "reissue_date": "2007-06-07", "expire_date": "2027-06-30",
     "status": "current and active", "classifications": ["C36", "A", "C-4", "C16", "B", "C10"], "additional_status": [],
     "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2026-09-04", "MERCHANTS BONDING COMPANY (MUTUAL)"),
     "workers_compensation": _wc("insured", "FINANCIAL PACIFIC INSURANCE COMPANY", "10147545585", "2026-07-13", "2027-07-13"),
     "record_stamp": "Data current as of 11/10/2026 6:17:57 PM"},
    {"license": "1115649", "name_on_record": "RAPID FLOW PLUMBING & ROOTER INC", "dba": None,
     "street": "230 EDINBURGH ST", "city": "SAN FRANCISCO", "zip": "94112", "phone_on_record": "(415) 866-8401",
     "entity": "Corporation", "issue_date": "2024-01-29", "reissue_date": None, "expire_date": "2028-01-31",
     "status": "current and active", "classifications": ["B", "C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-03-03", "MERCHANTS BONDING COMPANY (MUTUAL)"),
     "workers_compensation": _wc("exempt", effective="2026-02-03", expires=None),
     "record_stamp": "Data current as of 11/10/2026 6:18:01 PM"},
    {"license": "841229", "name_on_record": "MANNY'S PLUMBING & ROOTER", "dba": None,
     "street": "41 MIDVALE DRIVE", "city": "DALY CITY", "zip": "94015", "phone_on_record": "(650) 207-5733",
     "entity": "Sole Ownership", "issue_date": "2004-06-21", "reissue_date": None, "expire_date": "2028-06-30",
     "status": "current and active", "classifications": ["C36", "B"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2026-05-29", "MERCHANTS BONDING COMPANY (MUTUAL)"),
     "workers_compensation": _wc("exempt", effective="2026-06-28", expires=None),
     "record_stamp": "Data current as of 11/10/2026 6:18:01 PM"},
    {"license": "1025814", "name_on_record": "THE GENTEEL PLUMBERS INC", "dba": None,
     "street": "1181 REVERE AVE", "city": "SAN FRANCISCO", "zip": "94124", "phone_on_record": "(833) 436-8335",
     "entity": "Corporation", "issue_date": "2017-04-14", "reissue_date": None, "expire_date": "2027-04-30",
     "status": "current and active", "classifications": ["C36", "B"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2023-01-01", "AMERICAN CONTRACTORS INDEMNITY COMPANY"),
     "workers_compensation": _wc("insured", "TECHNOLOGY INSURANCE COMPANY INC", "TES4729399", "2026-01-24", "2027-01-24"),
     "record_stamp": "Data current as of 11/10/2026 6:18:06 PM"},
    {"license": "1009195", "name_on_record": "ADVANCED PLUMBING AND DRAIN INC", "dba": None,
     "street": "3450 SACRAMENTO ST 204", "city": "SAN FRANCISCO", "zip": "94118", "phone_on_record": "(415) 744-4944",
     "entity": "Corporation", "issue_date": "2015-11-24", "reissue_date": None, "expire_date": "2027-11-30",
     "status": "current and active", "classifications": ["C36"],
     "additional_status": ["The license may be suspended at a future date for failure to resolve an outstanding final "
                           "liability from the Franchise Tax Board, Department of Industrial Relations, Employment "
                           "Development Department, or the Contractors State License Board."],
     "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-09-26", "ATLANTIC SPECIALTY INSURANCE COMPANY"),
     "workers_compensation": _wc("insured", "HARTFORD ACCIDENT AND INDEMNITY COMPANY", "57WECBA5ARZ", "2026-08-21", "2027-08-21"),
     "record_stamp": "Data current as of 11/10/2026 6:18:16 PM"},
    {"license": "995163", "name_on_record": "BERNAL HILL DRYWALL INC", "dba": None,
     "street": "720 ANDERSON ST", "city": "SAN FRANCISCO", "zip": "94110", "phone_on_record": "(415) 533-8274",
     "entity": "Corporation", "issue_date": "2014-07-28", "reissue_date": None, "expire_date": "2028-07-31",
     "status": "current and active", "classifications": ["C-9", "B"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2023-03-29", "AMERICAN CONTRACTORS INDEMNITY COMPANY"),
     "workers_compensation": _wc("insured", "ENDURANCE ASSURANCE CORPORATION", "EAW0000274901", "2026-03-10", "2027-03-10"),
     "record_stamp": "Data current as of 11/10/2026 6:18:06 PM"},
    {"license": "1089561", "name_on_record": "TARO GROUP INC", "dba": "HEISES PLUMBING",
     "street": "1610 EVANS AVE", "city": "SAN FRANCISCO", "zip": "94124", "phone_on_record": "(415) 333-0704",
     "entity": "Corporation", "issue_date": "2022-04-06", "reissue_date": None, "expire_date": "2028-04-30",
     "status": "current and active", "classifications": ["C36", "C10", "A", "C20"], "additional_status": [],
     "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-05-27", "AMERICAN CONTRACTORS INDEMNITY COMPANY"),
     "workers_compensation": _wc("insured", "EMPLOYERS PREFERRED INSURANCE COMPANY", "EIG6235466", "2026-01-11", "2027-01-11"),
     "record_stamp": "Data current as of 11/10/2026 6:18:16 PM"},
    {"license": "632743", "name_on_record": "CALPLUMBING CO", "dba": None,
     "street": "P O BOX 31042", "city": "SAN FRANCISCO", "zip": "94131", "phone_on_record": "(415) 221-4633",
     "entity": "Sole Ownership", "issue_date": "1991-12-06", "reissue_date": None, "expire_date": "2027-12-31",
     "status": "current and active", "classifications": ["C36"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2026-09-01", "ATLANTIC SPECIALTY INSURANCE COMPANY"),
     "workers_compensation": _wc("exempt", effective="2025-12-08", expires=None),
     "record_stamp": "Data current as of 11/10/2026 6:18:10 PM"},
    {"license": "868994", "name_on_record": "ATLAS PLUMBING & ROOTER", "dba": None,
     "street": "3311 MISSION STREET UNIT 165", "city": "SAN FRANCISCO", "zip": "94110", "phone_on_record": "(650) 871-9863",
     "entity": "Corporation", "issue_date": "2005-12-08", "reissue_date": "2008-03-25", "expire_date": "2028-03-31",
     "status": "current and active", "classifications": ["C36", "A"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2023-01-01", "AMERICAN CONTRACTORS INDEMNITY COMPANY"),
     "workers_compensation": _wc("employee_service_group", None, "WC051666394CA", "2026-07-01", "2027-07-01"),
     "record_stamp": "Data current as of 11/10/2026 6:18:06 PM"},
    {"license": "1140843", "name_on_record": "DISCOUNT PLUMBING ROOTER SERVICES LLC", "dba": None,
     "street": "1325 HOWARD AVE BLDG 710", "city": "BURLINGAME", "zip": "94010", "phone_on_record": "(650) 991-2100",
     "entity": "Ltd Liability", "issue_date": "2025-07-22", "reissue_date": None, "expire_date": "2027-07-31",
     "status": "current and active", "classifications": ["C36", "A"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2025-06-09", "LEXINGTON NATIONAL INSURANCE CORPORATION"),
     "workers_compensation": _wc("insured", "A I U INSURANCE COMPANY", "020396018", "2025-04-01", "2027-04-01"),
     "record_stamp": "Data current as of 11/10/2026 6:18:16 PM"},
    {"license": "1075566", "name_on_record": "BAY AREA PIPE & EQUIPMENT INC", "dba": "BAY AREA MECHANICAL",
     "street": "1320 UNDERWOOD AVE", "city": "SAN FRANCISCO", "zip": "94124", "phone_on_record": "(925) 642-9768",
     "entity": "Corporation", "issue_date": "2021-05-07", "reissue_date": None, "expire_date": "2027-05-31",
     "status": "current and active", "classifications": ["C36", "C20"], "additional_status": [], "complaint_disclosure": None,
     "contractors_bond": _bond(25000, "2023-01-01", "AMERICAN CONTRACTORS INDEMNITY COMPANY"),
     "workers_compensation": _wc("insured", "PREFERRED EMPLOYERS INSURANCE COMPANY", "PEG324521720", "2025-12-02", "2026-12-02"),
     "record_stamp": "Data current as of 11/10/2026 6:18:10 PM"},
]

# Separately identified candidate (outside the historical 16-record score), read the same day.
EXTRA_READ = {
    "license": "1034873", "name_on_record": "PLUMBING 1 BUILDER'S INC", "dba": None,
    "street": "25125 SANTA CLARA STREET E106", "city": "HAYWARD", "zip": "94544", "phone_on_record": "(650) 868-8059",
    "entity": "Corporation", "issue_date": "2018-01-16", "reissue_date": "2021-12-14", "expire_date": "2027-12-31",
    "status": "current and active", "classifications": ["C36", "B"], "additional_status": [], "complaint_disclosure": None,
    "contractors_bond": _bond(25000, "2024-12-14", "WESTERN SURETY COMPANY"),
    "workers_compensation": _wc("insured", "PACIFIC COMPENSATION INSURANCE COMPANY", "WC1062363", "2025-12-30", "2026-12-30"),
    "record_stamp": "Data current as of 11/10/2026 6:18:32 PM",
}

ALL_READS = READS + [EXTRA_READ]

COMPARE_FIELDS = (
    "name_on_record", "dba", "street", "city", "zip", "phone_on_record", "entity",
    "issue_date", "reissue_date", "expire_date", "status", "classifications",
)


def _fmt(value):
    if value is None or value == []:
        return "—"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _norm(value):
    return sorted(value) if isinstance(value, list) else value


def _baseline_1110():
    import recheck_data  # direct reads of 2026-11-10 by arena/2a57ff73-korea7
    return {r["license"]: r for r in recheck_data.READS}


def _baseline_1034873():
    """Map the 2026-11-10 job-fit record onto comparable fields (only the fields it stored)."""
    ev = json.loads((ROOT / "data" / "canonical" / "session-1012-verification.json").read_text(encoding="utf-8"))
    a = ev["additional_candidate"]
    return {
        "name_on_record": a["name_on_record"],
        "phone_on_record": a["business_phone"],
        "issue_date": a["issue_date"],
        "reissue_date": a["reissue_date"],
        "expire_date": a["license_expiry"],
        "status": a["status"],
        "classifications": a["classifications"],
        "address": a["address"],
        "bond_amount_usd": a["contractor_bond_usd"],
        "wc_carrier": a["workers_compensation"]["carrier"],
        "wc_effective": a["workers_compensation"]["effective"],
        "wc_expires": a["workers_compensation"]["expires"],
    }


def _diff_record(old, new):
    deltas = []
    for field in COMPARE_FIELDS:
        if _norm(old.get(field)) != _norm(new.get(field)):
            deltas.append("%s: 11/10 %s → 11/11 %s" % (field, _fmt(old.get(field)), _fmt(new.get(field))))
    for key in ("contractors_bond", "workers_compensation"):
        a, b = old.get(key) or {}, new.get(key) or {}
        for sub in sorted(set(a) | set(b)):
            if sub in ("text", "class_codes"):
                continue
            if _norm(a.get(sub)) != _norm(b.get(sub)):
                deltas.append("%s.%s: 11/10 %s → 11/11 %s" % (key, sub, _fmt(a.get(sub)), _fmt(b.get(sub))))
    for key in ("complaint_disclosure", "additional_status"):
        if bool(old.get(key)) != bool(new.get(key)):
            deltas.append("%s present: 11/10 %s → 11/11 %s" % (key, bool(old.get(key)), bool(new.get(key))))
    return deltas


def compare():
    """Return [(license, [delta strings])] for all 17 reads. Only real transcription differences."""
    base = _baseline_1110()
    out = []
    for read in READS:
        old = base.get(read["license"])
        out.append((read["license"], ["absent from the 2026-11-10 re-check"] if old is None else _diff_record(old, read)))
    b = _baseline_1034873()
    r = EXTRA_READ
    now = {
        "name_on_record": r["name_on_record"], "phone_on_record": r["phone_on_record"],
        "issue_date": r["issue_date"], "reissue_date": r["reissue_date"], "expire_date": r["expire_date"],
        "status": r["status"], "classifications": r["classifications"],
        "address": "%s, %s, CA %s" % (r["street"], r["city"], r["zip"]),
        "bond_amount_usd": r["contractors_bond"]["amount_usd"],
        "wc_carrier": r["workers_compensation"]["carrier"],
        "wc_effective": r["workers_compensation"]["effective"],
        "wc_expires": r["workers_compensation"]["expires"],
    }
    deltas = ["%s: 11/10 %s → 11/11 %s" % (k, _fmt(b[k]), _fmt(now[k]))
              for k in b if _norm(b[k]) != _norm(now[k])]
    out.append((r["license"], deltas))
    return out


def summary_text(deltas):
    if not deltas:
        return "No change in any compared identity, status, classification, bond or workers'-compensation field"
    return "; ".join(deltas)


def days_until(iso_date, today=READ_DATE):
    if not iso_date:
        return None
    return (_dt.date.fromisoformat(iso_date) - _dt.date.fromisoformat(today)).days


def wc_watch():
    """Insured records whose printed workers'-comp expiry is within WATCH_DAYS of the read date."""
    rows = []
    for r in ALL_READS:
        wc = r["workers_compensation"]
        d = days_until(wc.get("expires"))
        if d is not None and d <= WATCH_DAYS:
            rows.append((r, d))
    return sorted(rows, key=lambda x: x[1])


def _label(r):
    return r["name_on_record"] + ((" dba " + r["dba"]) if r["dba"] else "")


def integrate(c):
    if "reread1111_licenses" in c.TABLES:
        return None
    planned = {"S%d" % i for i in range(FIRST_SID, FIRST_SID + len(ALL_READS) + 2)}
    collisions = planned.intersection(c.SOURCES)
    if collisions:
        raise ValueError("reread_1111 source-ID collision: %s" % sorted(collisions))
    deltas = dict(compare())
    sid = {}
    n = FIRST_SID
    for r in ALL_READS:
        key = "S%d" % n
        n += 1
        sid[r["license"]] = key
        c.SOURCES[key] = {
            "label": "CSLB License Detail #%s — November 11 re-read" % r["license"],
            "publisher": "Contractors State License Board",
            "url": CSLB_URL + r["license"],
            "tier": "official",
            "status": "verified",
            "checked": READ_DATE,
            "supports": ("Status, classifications, address, phone, issue/expiry dates, bond and workers' "
                         "compensation as returned on 2026-11-11"),
            "note": "Direct read 2026-11-11 by %s; the page printed '%s'." % (SESSION, r["record_stamp"]),
        }
    artifact_sid = "S%d" % n
    c.SOURCES[artifact_sid] = {
        "label": "Dated re-read transcription — 2026-11-11",
        "publisher": "This repository",
        "url": "data/canonical/reread-2026-11-11.json",
        "tier": "primary",
        "status": "verified",
        "checked": READ_DATE,
        "supports": "Machine-readable transcription of the 2026-11-11 CSLB reads and the computed field deltas",
        "note": "Generated by scripts/reread_1111.py during the build; primary record of this session's own reads.",
    }
    n += 1
    cal_sid = "S%d" % n
    c.SOURCES[cal_sid] = {
        "label": "CSLB — Check a License (search form)",
        "publisher": "Contractors State License Board",
        "url": CHECK_A_LICENSE,
        "tier": "official",
        "status": "verified",
        "checked": READ_DATE,
        "supports": "Official entry point for re-checking any licence on the hire date",
        "note": "Linked from every License Detail page read on 2026-11-11 ('Check a License or HIS Registration').",
    }

    change_count = sum(1 for v in deltas.values() if v)
    lic_rows = []
    for r in ALL_READS:
        changed = deltas[r["license"]]
        wc = r["workers_compensation"]
        if wc["kind"] == "exempt":
            wc_txt = "Exempt (no employees certified) since %s" % wc["effective"]
        elif wc["kind"] == "employee_service_group":
            wc_txt = "Employee service group; policy expires %s" % wc["expires"]
        else:
            wc_txt = "%s; expires %s" % (wc["carrier"], wc["expires"])
        extra = []
        if r["complaint_disclosure"]:
            extra.append("Complaint disclosure notice on record")
        if r["additional_status"]:
            extra.append("Additional status: possible future suspension notice")
        lic_rows.append({
            "cells": [
                "<strong>%s</strong><br><code>#%s</code>%s%s" % (
                    r["name_on_record"], r["license"],
                    ("<br><small>dba %s</small>" % r["dba"]) if r["dba"] else "",
                    "<br><small>separately checked lead — not in the 16-record score</small>"
                    if r is EXTRA_READ else ""),
                '<span class="pill ok">%s</span>' % r["status"],
                ", ".join(r["classifications"]),
                r["expire_date"],
                r["phone_on_record"],
                wc_txt + (("<br><small>%s</small>" % "; ".join(extra)) if extra else ""),
                r["record_stamp"].replace("Data current as of ", ""),
                '<span class="pill ok">no change</span>' if not changed
                else '<span class="pill warn">changed — see deltas</span>',
            ],
            "src": [sid[r["license"]]],
        })
    c.TABLES["reread1111_licenses"] = {
        "title": "All 17 CSLB records on this site, re-read 2026-11-11",
        "columns": ["Company on record / license", "License status", "Classifications", "Licence expires",
                    "Phone on record", "Workers' compensation (as printed)", "CSLB database stamp",
                    "Change vs 2026-11-10 read", "Source"],
        "rows": lic_rows,
        "caption": ("Read directly on the official CSLB License Detail pages on 2026-11-11 (UTC). Every page printed "
                    "a 11/10/2026 database stamp, shown exactly as returned. A licence record confirms status and "
                    "scope only — not experience with a seized trip lever, work in an occupied unit, price or "
                    "availability."),
    }

    delta_rows = []
    for r in ALL_READS:
        if deltas[r["license"]]:
            delta_rows.append({"cells": ["<strong>%s</strong> <code>#%s</code>" % (r["name_on_record"], r["license"]),
                                         "<br>".join(deltas[r["license"]]),
                                         '<span class="pill warn">review</span>'],
                               "src": [sid[r["license"]]]})
    if not delta_rows:
        delta_rows.append({"cells": ["None — no compared field differed",
                                     "All 17 records matched their 2026-11-10 direct reads on every compared identity, "
                                     "status, classification, contractor's-bond and workers'-compensation field. "
                                     "Only the CSLB database stamp advanced (11/9/2026 → 11/10/2026).",
                                     '<span class="pill ok">no change</span>'],
                           "src": [artifact_sid]})
    c.TABLES["reread1111_deltas"] = {
        "title": "Field-level differences against the 2026-11-10 direct reads",
        "columns": ["Company / license", "Fields that differ", "Disposition", "Source"],
        "rows": delta_rows,
        "caption": ("Computed by scripts/reread_1111.py: the 16 scored records are compared with "
                    "scripts/recheck_data.py (2026-11-10 reads); #1034873 is compared with the fields stored in "
                    "data/canonical/session-1012-verification.json. A difference would be a record change or a "
                    "transcription correction to review — not a judgement about the business."),
    }

    watch_rows = []
    for r, d in wc_watch():
        watch_rows.append({"cells": ["<strong>%s</strong> <code>#%s</code>" % (_label(r), r["license"]),
                                     r["workers_compensation"]["carrier"] or "Employee service group",
                                     r["workers_compensation"]["expires"],
                                     "%d days" % d,
                                     "Ask for a current certificate of workers' compensation insurance and re-open "
                                     "the CSLB record on the hire date; if work could run past the expiry, confirm "
                                     "the renewal is on the record first."],
                           "src": [sid[r["license"]], cal_sid]})
    c.TABLES["reread1111_wc_watch"] = {
        "title": "Workers' compensation policies that expire within %d days of 2026-11-11" % WATCH_DAYS,
        "columns": ["Company / license", "Carrier on record", "Policy expires", "Days from 2026-11-11",
                    "What to do before hiring", "Source"],
        "rows": watch_rows,
        "caption": ("Dates are transcribed from the CSLB records; 'days' is calendar arithmetic from the read date. "
                    "An upcoming expiry is not a defect — policies are commonly renewed — but CSLB shows only what "
                    "is on file, so confirm on the hire date. Exempt licensees certified they have no employees; "
                    "ask who will actually be on site."),
    }

    n_watch = len(watch_rows)
    c.PAGES["reread-1111.html"] = {
        "title": "Re-read 2026-11-11",
        "eyebrow": "Dated evidence · re-read 2026-11-11",
        "h1": "Licence re-read — November 11, 2026",
        "lede": ("Every CSLB licence record shown on this site — the sixteen scored records and the separately checked "
                 "#1034873 — was read again directly on 2026-11-11 and compared field by field with the previous "
                 "day's direct reads."),
        "sections": [
            {"type": "callout", "tone": "ok" if change_count == 0 else "warn", "html":
                (("<strong>17 of 17 licence records returned current and active; no compared field changed.</strong> "
                  "Only the CSLB database stamp advanced to 11/10/2026.") if change_count == 0 else
                 ("<strong>17 of 17 licence records returned current and active.</strong> %d record(s) show a "
                  "field-level difference; each is listed below." % change_count))
                + (" %d insured record(s) carry a workers'-compensation expiry within %d days — see the watch table."
                   % (n_watch, WATCH_DAYS) if n_watch else "")
                + " Licence status does not establish experience with this repair, willingness to open a ceiling in "
                  "an occupied unit, price or availability — those remain UNVERIFIED."},
            {"type": "table", "ref": "reread1111_licenses"},
            {"type": "table", "ref": "reread1111_deltas"},
            {"type": "table", "ref": "reread1111_wc_watch"},
            {"type": "prose", "title": "What this re-read does and does not prove", "html":
                ("<p>These are direct reads of seventeen government records on 2026-11-11. The CSLB pages are the "
                 "authority; this page is a transcription with a source link on every row. The historical "
                 "2026-11-08 snapshot, the 2026-11-10 <a href=\"recheck.html\">live re-check</a> and the "
                 "<a href=\"ranking.html\">ranking</a> scores are unchanged by this page.</p>"
                 "<p>It does not prove that any firm can free a seized trip lever without damaging concealed "
                 "piping, will open and restore a ceiling under one contract, has worked in an occupied unit, or "
                 "will accept this job at any price. No provider was contacted and nothing was booked. Review "
                 "platforms remain third-party material and are never used as licence evidence. Quoted amounts "
                 "remain owner-supplied and unverified.</p>")},
            {"type": "prose", "title": "How to use it", "html":
                ("<p>Pick from the <a href=\"ranking.html\">ranked decision</a> and the "
                 "<a href=\"contacts.html\">contact directory</a>, then re-open the chosen licence on "
                 "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">CSLB Check a License</a> on the hire "
                 "day. Machine-readable transcription and computed deltas: "
                 "<a href=\"data/canonical/reread-2026-11-11.json\">reread-2026-11-11.json</a>. Open questions stay on "
                 "<a href=\"flagged.html\">Flagged for review</a>.</p>") % CHECK_A_LICENSE},
        ],
    }
    for group in c.NAV:
        if group["group"] == "Audit":
            if ("reread-1111.html", "Re-read 2026-11-11") not in group["links"]:
                group["links"].insert(0, ("reread-1111.html", "Re-read 2026-11-11"))
            break
    for page in ("index.html", "summary.html"):
        c.PAGES[page]["sections"].insert(0, {"type": "callout", "tone": "ok", "html":
            ("<strong>2026-11-11 re-read:</strong> all 17 CSLB licence records on this site were read directly again "
             "today — 17 current and active, %d field-level change(s), %d workers'-comp expiry date(s) within %d days. "
             "<a href=\"reread-1111.html\">See the dated re-read</a>.") % (change_count, n_watch, WATCH_DAYS)})

    import re as _re
    existing = [int(m.group(1)) for row in c.TABLES["flagged"]["rows"]
                for m in [_re.fullmatch(r"U(\d+)", str(row["cells"][0]))] if m]
    flag_id = "U%d" % (max(existing) + 1)
    if n_watch:
        names = ", ".join("#%s (%s, %d days)" % (r["license"], r["workers_compensation"]["expires"], d)
                          for r, d in wc_watch())
        c.TABLES["flagged"]["rows"].append({
            "cells": [
                flag_id,
                "Workers' compensation expiries close to any likely hire date",
                ("On the 2026-11-11 CSLB re-read, %d insured licence(s) print a workers'-compensation policy expiry "
                 "within %d days: %s. Renewal status after those dates cannot be known today.") % (n_watch, WATCH_DAYS, names),
                "Before signing, obtain a current certificate of insurance and re-open the CSLB record on the hire date.",
                '<span class="pill warn">UNVERIFIED</span>',
            ],
            "src": [sid[r["license"]] for r, _ in wc_watch()] + [cal_sid],
        })
    # Re-publish flag range/count everywhere they are quoted (index card, "U01–Uxx", "N flagged items").
    import session_1012_verification as _norm_mod
    _norm_mod._normalise_flags(c)
    c.META["updated"] = READ_DATE
    c.META["session"] = SESSION

    payload = {
        "checked_date": READ_DATE,
        "session": SESSION,
        "method": ("Direct fetch and read of each official CSLB License Detail page on 2026-11-11 (UTC). Fields "
                   "transcribed verbatim; the database stamp printed on each page (11/10/2026) is preserved exactly."),
        "baselines": {
            "scored_16": "scripts/recheck_data.py READS (direct reads 2026-11-10)",
            "1034873": "data/canonical/session-1012-verification.json additional_candidate (direct read 2026-11-10)",
        },
        "records": [dict(r, source_url=CSLB_URL + r["license"], source_id=sid[r["license"]],
                         in_historical_score=r is not EXTRA_READ,
                         deltas=deltas[r["license"]], delta_summary=summary_text(deltas[r["license"]]),
                         wc_days_to_expiry=days_until(r["workers_compensation"].get("expires")))
                    for r in ALL_READS],
        "wc_watch_window_days": WATCH_DAYS,
        "wc_watch": [{"license": r["license"], "expires": r["workers_compensation"]["expires"], "days": d}
                     for r, d in wc_watch()],
        "flag_id": flag_id if n_watch else None,
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
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    for lic, items in compare():
        print(lic, "|", summary_text(items))
    for r, d in wc_watch():
        print("WC watch:", r["license"], r["workers_compensation"]["expires"], d, "days")
