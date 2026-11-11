#!/usr/bin/env python3
"""Open questions, information gaps and a 2026-11-11 official-source re-read.

Additive integration module for session `arena/e919fdc0-korea7`. It is imported
at the end of the existing chain in `dashboard_content.py` and follows the same
pattern as `reread_1110.py`, `disclosure_1110.py` and
`session_1012_verification.py`: it appends sources, tables, a finding and a
page. It does not rewrite any existing row, score or flag.

Two deliverables live here:

1. `questions.html` — a register of every question that has to be answered
   before a hiring decision can reasonably be made, who can answer it, how to
   get the answer, what it changes, and its current status. Each row names the
   discovery method, not just the gap.
2. `recheck.html` gains nothing; the dated 2026-11-11 re-read is published as
   `verification.html` rows plus a new table on its own section of
   `questions.html` so the two are read together.

Nothing in this module is inferred: a row that has no source is marked
UNVERIFIED and left blank.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = json.loads((ROOT / "data" / "canonical" / "session-e919-verification.json").read_text(encoding="utf-8"))
CHECKED = "2026-11-11"

NEW_SOURCES = {
    "S221": {
        "label": "B&P Code §7048 — contractor licensing exemption",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Aggregate contract price under $1,000, casual/minor/inconsequential work, and no building permit required — all three conditions must hold; the exemption is lost if the person advertises as a contractor or employs others",
        "note": "Read directly 2026-11-11. Amended by Stats. 2025, Ch. 67, Sec. 12 (AB 1170), effective 2026-01-01.",
    },
    "S222": {
        "label": "SF Plumbing Code §104.2 — exempt work (official PDF)",
        "publisher": "City and County of San Francisco",
        "url": "https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "The nine permit-exempt plumbing items, verbatim; items (1) and (2) both stop at work 'not requiring cutting into or removal of piping'",
        "note": "PDF read directly 2026-11-11; the quoted text matches the transcription published on the Code exemptions page.",
    },
    "S223": {
        "label": "sf.gov — apply for a kitchen or bath remodel permit",
        "publisher": "SF Department of Building Inspection",
        "url": "https://www.sf.gov/apply-kitchen-or-bath-remodel-permit",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "The online kitchen/bath permit route is limited to in-kind fixture work with no wall removal or plans and to an R-2 unit or R-3 building; plumbing is a separate permit started from that application",
        "note": "Read directly 2026-11-11. The page does not state that a ceiling opening is covered by a kitchen/bath permit.",
    },
    "S224": {
        "label": "CSLB — B General Building Contractor classification (B&P §7057)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "A B licensee without the specialty class must subcontract an appropriately licensed specialty contractor for other trades — the reason a dual-classified licence is a screening signal, not a requirement",
        "note": "Read directly 2026-11-11.",
    },
    "S225": {
        "label": "CSLB — C-9 Drywall Contractor classification",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "The classification that names gypsum wall board installation, taping and texturing explicitly",
        "note": "Read directly 2026-11-11.",
    },
    "S226": {
        "label": "CSLB License Detail #829071 — Ace Plumbing & Rooter (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active; C-36, A, C-4, C-16, B, C-10; expires 2027-06-30; (415) 824-6444; workers' compensation 2026-07-13 to 2027-07-13",
        "note": "Record printed 'Data current as of 11/10/2026 6:17:57 PM'. Zero field-level drift against the stored record.",
    },
    "S227": {
        "label": "CSLB License Detail #1003394 — Handyman Heroes Inc (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active; B + C-36; expires 2027-05-31; (844) 382-4376; the record itself displays a complaint-disclosure link",
        "note": "Record printed 'Data current as of 11/10/2026 6:16:14 PM'. Zero field-level drift.",
    },
    "S228": {
        "label": "CSLB — complaint disclosure #1003394 (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "One citation: 2 2020 001045, dated 07/12/2020, status 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'",
        "note": "Read directly 2026-11-11; matches the published disclosure audit.",
    },
    "S229": {
        "label": "CSLB License Detail #1025814 — The Genteel Plumbers Inc (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1025814",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active; C-36 + B; expires 2027-04-30; CSLB phone (833) 436-8335",
        "note": "Record printed 'Data current as of 11/10/2026 6:18:06 PM'. Zero field-level drift. The two-phone discrepancy (flag U23) is unchanged.",
    },
    "S230": {
        "label": "CSLB License Detail #1024971 — Fast Response Plumbing and Rooter (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active; C-36 only; expires 2027-03-31; workers' compensation policy expires 2026-12-18",
        "note": "Record printed 'Data current as of 11/10/2026 6:17:36 PM'. Zero field-level drift; the near-term insurance expiry stands.",
    },
    "S231": {
        "label": "CSLB License Detail #757796 — Bay Area Plumbing (2026-11-11 re-read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796",
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active; C-36 only; expires 2027-01-31; workers' compensation exempt — 'no employees at this time'",
        "note": "Record printed 'Data current as of 11/10/2026 6:17:53 PM'. Zero field-level drift.",
    },
    "S232": {
        "label": "Session 2026-11-11 re-read record (machine-readable)",
        "publisher": "This repository",
        "url": "data/canonical/session-e919-verification.json",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "The transcribed fields, quotes and drift verdicts for every page re-read on 2026-11-11",
        "note": "Written by this session; it records the re-read, it is not independent corroboration.",
    },
}

# --- The question register -------------------------------------------------
# Columns: ID, question, why it matters / what it changes, who can answer it,
# how to get the answer, status, sources.
QUESTION_ROWS = [
    ("Q01",
     "What exactly is seized — the trip-lever linkage, the plunger, the overflow plate, or the drain shoe?",
     "Determines whether this is a from-above trim repair or a concealed waste-and-overflow replacement, and therefore which of the three owner-reported prices is even comparable. A handle adjustment (the $135 scope) and a full waste-and-overflow replacement (the $614 scope) are different jobs.",
     "A licensed plumber on site; the manufacturer once the model is known",
     "Photograph the overflow plate, the lever, and the tub drain from above before booking; ask the first plumber to describe the assembly in writing.",
     "OPEN — owner reports 'stuck inside the hidden plumbing'; no photo, model number or inspection record has been supplied",
     ["S44", "S14", "S232"]),
    ("Q02",
     "What is behind the wall — copper, brass, ABS, PVC, galvanised, lead, or a brass shoe with a soldered overflow elbow?",
     "Sets the failure mode of a from-above attempt: a brass or plastic tubular assembly can often be withdrawn; a soldered or corroded connection cannot, which is exactly why plumbers have declined. It also sets the ceiling-opening scope.",
     "The plumber performing the assessment",
     "Ask for a written assessment after a from-above inspection; request that any attempt start with the least destructive step and stop at a named point.",
     "OPEN — not established by any source read; five or more plumbers reportedly declined from-above removal",
     ["S44", "S14"]),
    ("Q03",
     "Which model of waste-and-overflow assembly is installed, and is a replacement kit still available?",
     "A like-for-like replacement avoids cutting. If the model is discontinued, the plumber may need to open the wall to convert to a different assembly.",
     "Owner (receipts, building records); plumber on site; manufacturer parts list",
     "Check the overflow plate for a brand; ask the building's maintenance records; photograph the plate and drain.",
     "OPEN — no model identification supplied",
     ["S14", "S44"]),
    ("Q04",
     "Can the assembly be removed from above at all, and what is the written stop point before concealed piping is at risk?",
     "This is the owner's stated preference and the difference between a tub-side job and a ceiling opening in an occupied building.",
     "A licensed plumber who will attempt it, on site",
     "Ask each candidate to quote a staged scope: (1) from-above attempt with a named abort point, (2) access from below only if step 1 fails, (3) restoration.",
     "OPEN — more than five licensed plumbers reportedly could not remove it without concern; no written attempt or abort criterion exists",
     ["S44", "S18"]),
    ("Q05",
     "What access exists from the storage unit below — ceiling type, height, obstructions, services in the void?",
     "A drywall ceiling at reachable height with clear space is a straightforward patch; a plaster ceiling, a soffit, ductwork, or a fire-rated assembly changes the scope, the cost and possibly the permit path.",
     "Owner or building manager (site inspection); the contractor",
     "Photograph the storage-unit ceiling under the tub, measure the clear height, and note anything fixed to the ceiling. Ask the contractor to price from those photos before visiting.",
     "OPEN — owner states the unit sits below and the drywall ceiling may need opening; no inspection or photo supplied",
     ["S44"]),
    ("Q06",
     "Is the ceiling a fire-rated or fire-protection assembly, and is that what makes the difference to the permit question?",
     "sf.gov exempts only 'minor repairs to existing interior plaster or wallboard, unless they are required for fire protection'. A rated ceiling changes the exemption analysis and the patching method.",
     "SF Department of Building Inspection; the contractor",
     "Ask the Permit Center help desk (628-652-4900, permitsf@sfgov.org) whether the ceiling under this tub is a rated assembly and what a patch requires.",
     "OPEN — no building records or inspection",
     ["S02", "S01"]),
    ("Q07",
     "Does this exact repair need a permit, and if so which one?",
     "Determines sequencing, inspection-before-covering, cost, and who may legally do the work. This is the single largest unresolved compliance question.",
     "SF Department of Building Inspection only",
     "Call the Permit Center help desk with the measured scope and ask for a written answer. The plumbing code's exempt list does not name waste-and-overflow replacement and both of its repair items stop at work 'not requiring cutting into or removal of piping'.",
     "OPEN — not determined; only DBI can decide. The site publishes the official text and reaches no conclusion",
     ["S222", "S01", "S232"]),
    ("Q08",
     "Who carries the ceiling repair — the plumber, a drywall subcontractor, or two separate contracts?",
     "The owner asked for one all-in-one service. If no single licence holder will self-perform both trades, the job becomes two contracts with a hand-off risk at the opening.",
     "Each candidate contractor",
     "Require a written scope naming who opens the ceiling, who closes it, who primes and paints, and who is responsible if the patch cracks.",
     "OPEN — five CSLB licences carry both B and C-36, but no company has confirmed it will self-perform the ceiling",
     ["S09", "S10", "S11", "S56", "S57", "S224", "S225"]),
    ("Q09",
     "What is the total cost including access, plumbing, leak test, patch, texture, primer, paint, cleanup and disposal?",
     "The three reported amounts ($614, $550, $135) cover visibly different scopes and none states whether drywall is included. Comparing them as-is would be wrong.",
     "Each candidate contractor",
     "Ask for one itemised written quote on an identical scope sheet; require the ceiling restoration to be a named line item.",
     "OPEN — all amounts are owner-supplied and unverified; no published price exists for this scope",
     ["S44", "S06", "S07", "S08"]),
    ("Q10",
     "Are the reported quotes still valid at today's date?",
     "The estimates are dated 2026-08-30. Prices, availability and insurance records move.",
     "The three companies that quoted",
     "Ask each to re-confirm the amount in writing and state how long it holds.",
     "OPEN — quotes dated 2026-08-30; no re-confirmation",
     ["S44"]),
    ("Q11",
     "Is each candidate's licence, bond and insurance current on the hire date?",
     "CSLB status can change between the last read and the day work starts. Workers' compensation gaps expose the owner.",
     "CSLB Check-a-License; the contractor's certificate of insurance",
     "Re-read each CSLB record on the day of hire and ask for a certificate of insurance naming the policy dates.",
     "PARTLY VERIFIED — six records re-read 2026-11-11 with no drift; eleven records and the additional lead were not re-read this session",
     ["S226", "S227", "S229", "S230", "S231", "S232"]),
    ("Q12",
     "Is the business address on the CSLB record the address that will actually serve this property?",
     "Two records publish a phone that differs from the company's own site, and one shortlisted firm is outside San Francisco. Service area and dispatch address are not licence facts.",
     "Each contractor",
     "Ask, in writing, which office will dispatch and whether travel or minimum charges apply.",
     "OPEN — CSLB addresses recorded; service to this specific address unconfirmed",
     ["S229", "S231", "S233"]),
    ("Q13",
     "Which number reaches a human who can book this job?",
     "Two candidates publish two different phone numbers on official sources. Calling the wrong one wastes the first contact.",
     "The contractor",
     "Call both published numbers, note which answers, and record the result.",
     "OPEN — Genteel (833) 436-8335 vs 415-465-5853 and Atlas (650) 871-9863 vs (415) 849-2346 are unreconciled",
     ["S229", "S233", "S234"]),
    ("Q14",
     "When can the work be done, and how long is the unit without a usable tub?",
     "A tenant occupies the unit. Water shut-off and a missing tub are habitability issues, not just scheduling ones.",
     "The contractor; the tenant; the owner",
     "Ask for a duration in writing and agree the water-off window with the tenant before booking.",
     "OPEN — no availability or duration confirmed by any provider",
     ["S44"]),
    ("Q15",
     "What protection and notice does the tenant need — dust containment, access hours, belongings in the storage unit?",
     "The owner specifically asked for a provider experienced in occupied units. Dust from a ceiling opening travels into both units.",
     "The contractor; the tenant",
     "Require containment and cleanup in the written scope; put the access window and notice period in writing.",
     "OPEN — no provider has confirmed occupied-unit practice for this job",
     ["S40", "S43"]),
    ("Q16",
     "Does the storage unit hold anything that must be moved before a ceiling is opened?",
     "A ceiling opening above stored goods requires clearing the area. This affects scheduling and the risk of damage claims.",
     "The owner or building manager",
     "Walk the storage unit, photograph the ceiling and the items below it, and plan the clear-out.",
     "OPEN — not inspected",
     ["S44"]),
    ("Q17",
     "Who is authorised to approve access to the storage unit and the tenant's unit?",
     "Without written authorisation the contractor cannot start, and a tenant dispute mid-job leaves the wall open.",
     "The owner; the property manager; the tenant",
     "Put the access authorisation in the contract and confirm it with the tenant in writing.",
     "OPEN — not documented",
     ["S44"]),
    ("Q18",
     "What happens if the wall is opened and the concealed piping is worse than expected?",
     "Concealed conditions are the classic change-order trap. Without a named stop-and-price trigger the owner loses control of cost.",
     "The contractor, agreed in writing before work starts",
     "Require a written change-order procedure with a stated hourly rate and a requirement to stop and call before extra work.",
     "OPEN — no change-order terms exist",
     ["S44"]),
    ("Q19",
     "What warranty covers the repair, and what does it exclude?",
     "A trip-lever assembly failure can recur. The warranty determines who pays the second time.",
     "Each contractor",
     "Ask for the warranty term in the written quote, and whether it covers the concealed connection.",
     "OPEN — no warranty terms supplied",
     ["S44"]),
    ("Q20",
     "Has the chosen contractor actually done this repair behind a finished wall before?",
     "The CSLB record proves classification, not experience with a seized concealed assembly. The owner's core requirement is delicate work in a sensitive environment.",
     "The contractor, with references",
     "Ask for two references for concealed waste-and-overflow work in an occupied residential building, and call them.",
     "OPEN — no provider capability or reference has been verified",
     ["S04", "S232"]),
    ("Q21",
     "Is the receiving drain or trap arm partially blocked, and will the repair expose a second problem?",
     "If the tub drains slowly, the obstruction may be downstream of the trip lever. Opening the ceiling and replacing the assembly without testing the drain risks a repeat visit.",
     "The plumber on site",
     "Ask for a drain test and a camera inspection of the waste line as part of the assessment.",
     "OPEN — owner reports a stuck lever, not a slow drain; drain condition not established",
     ["S18"]),
    ("Q22",
     "What is the building's occupancy class — R-2 apartment or R-3 — and does it change the permit route?",
     "sf.gov's online kitchen/bath route is limited to an R-3 building or an R-2 unit. Occupancy also drives the fire-rating question in Q06.",
     "SF Planning / Assessor property record; SF DBI",
     "Look the address up on the Property Information Map and confirm the occupancy class with DBI.",
     "OPEN — occupancy class not established",
     ["S223"]),
    ("Q23",
     "Are there photographs of the current condition?",
     "The owner offered reference pictures but none were supplied. Every contractor will ask for them.",
     "The owner",
     "Photograph the overflow plate, the lever, the drain, and the storage-unit ceiling with a scale reference.",
     "OPEN — no pictures supplied to this research",
     ["S44"]),
    ("Q24",
     "Which of the two routes does the owner actually want to buy: one contract at a higher price, or a specialist plumber plus a separate drywall partner?",
     "This is the decision the ranking is built around. The site can rank, but only the owner can choose between one-stop convenience and specialist trade coverage.",
     "The owner",
     "Read the ranked routes, then ask the top two candidates in each route for a price on the same written scope before choosing.",
     "OPEN — owner has not chosen a route",
     ["S91", "S224"]),
    ("Q25",
     "Should the failed linkage be replaced with a lift-and-turn or push-pull drain instead of another trip lever?",
     "A conversion removes the linkage that failed inside the wall and makes future operation independent of concealed parts. It changes the parts list and may change the ceiling question.",
     "The plumber on site; the manufacturer's conversion kit instructions",
     "Ask the plumber whether a conversion is possible from above on this tub, and price both options.",
     "OPEN — not assessed",
     ["S20"]),
]

RECHECK_ROWS = [
    ("AC08", "Ace Plumbing & Rooter", "#829071", "current and active · C-36, A, C-4, C-16, B, C-10 · expires 2027-06-30", "No drift", "S226"),
    ("AC09", "Handyman Heroes Inc", "#1003394", "current and active · B + C-36 · expires 2027-05-31 · complaint-disclosure link displayed on the record", "No drift", "S227"),
    ("AC10", "Handyman Heroes — complaint disclosure", "#1003394", "one citation 2 2020 001045, 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'", "No drift", "S228"),
    ("AC11", "The Genteel Plumbers Inc", "#1025814", "current and active · C-36 + B · expires 2027-04-30 · CSLB phone (833) 436-8335", "No drift", "S229"),
    ("AC12", "Fast Response Plumbing and Rooter", "#1024971", "current and active · C-36 only · expires 2027-03-31 · workers' comp expires 2026-12-18", "No drift", "S230"),
    ("AC13", "Bay Area Plumbing", "#757796", "current and active · C-36 only · expires 2027-01-31 · workers' comp exempt", "No drift", "S231"),
]

RULE_ROWS = [
    ("AR01", "B&amp;P §7048", "Licensing exemption requires all of: under $1,000 aggregate, casual/minor/inconsequential, and no building permit required", "Confirmed verbatim", "S221", "S13"),
    ("AR02", "SF Plumbing Code §104.2", "Nine exempt items; items (1) and (2) both require that no cutting into or removal of piping occurs", "Confirmed verbatim", "S222", "S96"),
    ("AR03", "sf.gov plumbing permit", "Permit needed before cutting into or replacing pipes, particularly pipes covered by a wall", "Confirmed word for word", "S01", "S01"),
    ("AR04", "sf.gov no-permit list", "Minor repairs to existing interior plaster or wallboard need no building permit, unless required for fire protection", "Confirmed word for word", "S02", "S02"),
    ("AR05", "CSLB C-36", "Plumbing contractor scope: waste disposal and maintenance/replacement of the listed items; no wallboard or texturing language", "Confirmed", "S05", "S05"),
    ("AR06", "CSLB B (§7057)", "A B licensee may subcontract a specialty trade instead of holding the class — dual classification is a signal, not a requirement", "Confirmed", "S224", "S15"),
    ("AR07", "CSLB C-9", "Drywall contractor: gypsum board, taping and texturing named explicitly", "Confirmed", "S225", "S16"),
    ("AR08", "sf.gov kitchen/bath permit", "Online route limited to in-kind work with no wall removal/plans in an R-2 unit or R-3 building; plumbing is a separate permit", "Confirmed", "S223", "S03"),
]


def _next_flag(c):
    ids = [r["cells"][0] for r in c.TABLES["flagged"]["rows"] if re.fullmatch(r"U\d+", str(r["cells"][0]))]
    return "U%d" % (max(int(i[1:]) for i in ids) + 1)


def integrate(c) -> None:
    if "open_questions" in c.TABLES:
        return
    collisions = set(NEW_SOURCES).intersection(c.SOURCES)
    if collisions:
        raise ValueError("Session e919 source-ID collision: %s" % sorted(collisions))
    c.SOURCES.update(NEW_SOURCES)

    # Bridge ids so each row cites a source actually about its subject. A
    # per-company phone entry is recorded only because the official record was
    # read again today with the same value (drift: none).
    c.SOURCES["S233"] = {
        "label": "Yelp — The Genteel Plumbers Inc (platform listing; not used as licence evidence)",
        "publisher": "Yelp", "url": "https://www.yelp.com/biz/the-genteel-plumbers-san-francisco",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Third-party review listing for one of the shortlisted firms. No rating or count from it is used here.",
        "note": "Direct fetch returns HTTP 403 in this environment, as in earlier sessions. It is listed as a platform link only.",
    }
    c.SOURCES["S234"] = {
        "label": "Yelp — Atlas Plumbing & Rooter (platform listing; not used as licence evidence)",
        "publisher": "Yelp", "url": "https://www.yelp.com/biz/atlas-plumbing-and-rooter-san-francisco",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Third-party review listing for one of the candidates. The stuck-lever excerpt is attributed to Atlas in search-result text.",
        "note": "Direct fetch returns HTTP 403 in this environment. Separately, the CSLB record for #868994 lists (650) 871-9863 while the company site publishes (415) 849-2346 — flag U51.",
    }

    # 1. Question register ---------------------------------------------------
    q_rows = []
    for qid, question, why, who, how, status, src in QUESTION_ROWS:
        tone = "ok" if status.startswith("PARTLY") else "warn"
        q_rows.append({
            "cells": [
                "<strong>%s</strong>" % qid,
                question,
                why,
                who,
                how,
                c.BLANK + " " + c.UNVERIFIED + "<br><small>%s</small>" % status if not status.startswith("PARTLY")
                else c.pill(status, "warn"),
            ],
            "src": src,
        })
    c.TABLES["open_questions"] = {
        "title": "Questions that must be answered before a hiring decision (%d)" % len(q_rows),
        "columns": ["#", "Question", "Why it changes the decision", "Who can answer it", "How to get the answer", "Verified answer / status", "Source"],
        "rows": q_rows,
        "caption": "Every row is an open question: the 'verified answer' column is blank and flagged because no source read for this project answers it. "
                   "The discovery method in column five is this project's suggestion; it is not itself a sourced fact. "
                   "Closed rows would carry a quoted official answer and a source link; there are none yet.",
    }

    # 2. Dated re-read -------------------------------------------------------
    re_rows = [{
        "cells": [rid, "<strong>%s</strong><br>%s" % (name, c.slink(src, lic)), detail, c.pill(verdict, "ok"), CHECKED],
        "src": [src, "S232"],
    } for rid, name, lic, detail, verdict, src in RECHECK_ROWS]
    c.TABLES["recheck_1111"] = {
        "title": "Official CSLB records re-read on 2026-11-11 (%d)" % len(re_rows),
        "columns": ["#", "Business and licence", "What the official record states on 2026-11-11", "Drift against the stored record", "Read date", "Source"],
        "rows": re_rows,
        "caption": "Six decision-critical licence records were read directly from CSLB on 2026-11-11 and compared field by field with "
                   "data/canonical/cslb_records.json. No field changed. Each record printed a database stamp of 11/10/2026, "
                   "which is the CSLB database's own last-updated marker, not the read date. The other eleven scored records "
                   "and the additional lead were not re-read this session and keep their earlier read dates.",
    }

    # 3. Rule re-read --------------------------------------------------------
    rule_rows = [{
        "cells": [rid, "<strong>%s</strong>" % title, finding, c.pill(verdict, "ok"), CHECKED],
        "src": [src1, src2] if src2 != src1 else [src1],
    } for rid, title, finding, verdict, src1, src2 in RULE_ROWS]
    c.TABLES["rules_1111"] = {
        "title": "Official rule pages re-read on 2026-11-11 (%d)" % len(rule_rows),
        "columns": ["#", "Rule", "What the official text says", "Result of this re-read", "Read date", "Source"],
        "rows": rule_rows,
        "caption": "The governing text was read again on 2026-11-11, not taken on trust from an earlier session. The quoted wording is on the "
                   "Code exemptions and Permits pages; this table records the re-check. Reading a rule does not decide this job's permit "
                   "question — only SF DBI can (Q07).",
    }

    # 4. Where the information is missing, by category -----------------------
    gap_rows = [
        ("G1", "Physical condition", "Assembly model, pipe material, ceiling construction, drain condition, photographs", "Q01, Q02, Q03, Q05, Q21, Q23",
         "On-site inspection plus owner photographs", c.pill("no data", "warn"), ["S44"]),
        ("G2", "Compliance", "Permit applicability, occupancy class, fire-rating of the ceiling", "Q06, Q07, Q22",
         "Written answer from SF DBI Permit Center", c.pill("no data", "warn"), ["S01", "S222"]),
        ("G3", "Price and scope", "Itemised all-in price for an identical written scope, including restoration", "Q08, Q09, Q10, Q18",
         "Three comparable written quotes on one scope sheet", c.pill("no data", "warn"), ["S44"]),
        ("G4", "Provider capability", "Concealed-assembly experience, occupied-unit practice, references", "Q15, Q20",
         "Two references per finalist, called", c.pill("no data", "warn"), ["S04"]),
        ("G5", "Scheduling and access", "Availability, duration, water-off window, storage-unit clear-out, authorisation", "Q14, Q16, Q17",
         "Written schedule and access agreement", c.pill("no data", "warn"), ["S44"]),
        ("G6", "Contract terms", "Change-order trigger, warranty, insurance certificate, lien releases", "Q11, Q18, Q19",
         "Contract review before the first payment", c.pill("no data", "warn"), ["S44"]),
        ("G7", "Licensing currency", "Six records re-read 2026-11-11 with no drift; eleven plus one lead not re-read", "Q11",
         "Re-read each record on the day of hire", c.pill("partial", "info"), ["S226", "S232"]),
    ]
    c.TABLES["gaps"] = {
        "title": "Where the information is missing, and what would close it (%d)" % len(gap_rows),
        "columns": ["#", "Category", "Information that does not exist yet", "Questions it blocks", "Suggested way to obtain it", "Status", "Source"],
        "rows": [{"cells": list(r[:5]) + [r[5]], "src": r[6]} for r in gap_rows],
        "caption": "Grouped view of the register above. 'No data' means no source read for this project supplies the information; it does not mean "
                   "the information is unknowable. Nothing in this table is inferred from the owner's description.",
    }

    # 5. Recommended discovery sequence --------------------------------------
    seq_rows = [
        ("1", "Photograph the overflow plate, lever, drain and the storage-unit ceiling; note any brand or model marking",
         "Costs nothing, needs no appointment, and is the first thing every contractor will ask for", "Owner", "Q01, Q03, Q05, Q23", ["S44"]),
        ("2", "Call the SF DBI Permit Center help desk with the measured scope and ask, in writing, whether a permit is required and which one",
         "Settles the compliance question that no website can answer for this specific job", "Permit Center help desk, 628-652-4900 / permitsf@sfgov.org", "Q06, Q07, Q22", ["S01", "S222"]),
        ("3", "Write one scope sheet and send it to the finalists so every quote covers the same work",
         "Makes the three existing quotes comparable and forces the ceiling restoration onto the line items", "Owner", "Q08, Q09, Q18", ["S44"]),
        ("4", "Ask two finalists for a from-above assessment with a named abort point before any opening",
         "Honours the stated preference and limits the risk the earlier plumbers flagged", "Finalist contractors", "Q02, Q04", ["S18"]),
        ("5", "Re-read every CSLB record on the hire date and request a certificate of insurance",
         "Licences and policies move; workers' compensation expiries are inside 60 days on two records", "CSLB Check-a-License; contractor", "Q11", ["S226", "S232"]),
        ("6", "Agree the tenant notice, water-off window and storage-unit clear-out in writing before the first payment",
         "Prevents a mid-job stop with the ceiling open in an occupied building", "Owner, tenant, contractor", "Q14, Q15, Q16, Q17", ["S44"]),
    ]
    c.TABLES["discovery_sequence"] = {
        "title": "Suggested order for closing the gaps (%d steps)" % len(seq_rows),
        "columns": ["Step", "Action", "Why this order", "Who does it", "Questions closed", "Source"],
        "rows": [{"cells": list(r[:5]), "src": r[5]} for r in seq_rows],
        "caption": "This sequence is this project's suggestion, ordered by cost and by what blocks the most other answers. "
                   "It is editorial, not an official recommendation, and no step has been performed by this session.",
    }

    # 6. Finding + flag ------------------------------------------------------
    c.TABLES["findings"]["rows"].append({
        "cells": [
            "F20",
            "Twenty-five questions stand between the current evidence and a defensible hiring decision",
            "They fall into seven groups: physical condition, compliance, price and scope, provider capability, scheduling and access, "
            "contract terms, and licensing currency. Only the licensing-currency group is partly closed, and only for the six records "
            "re-read on 2026-11-11. Every other group has no data at all — not weak data.",
            c.pill("gap register published", "warn"),
        ],
        "src": ["S232", "S44"],
    })
    c.TABLES["findings"]["rows"].append({
        "cells": [
            "F21",
            "The cheapest reported price and the most expensive reported price are not the same job",
            "The $135 report is described as a repair or adjustment of the plunger handle; the $550 report replaces the lever, plug and spout "
            "with a diverter; the $614 report replaces the waste and overflow. None of the three states drywall restoration. "
            "Ranking them by price would compare different scopes.",
            c.pill("owner-provided, unverified", "warn"),
        ],
        "src": ["S44"],
    })

    flag_id = _next_flag(c)
    c.TABLES["flagged"]["rows"].append({
        "cells": [
            flag_id,
            "Twenty-five questions stand open; the two official ones are anchored in the code text itself",
            "The compliance question is anchored in official documents and is still unanswered for this job: sf.gov requires a permit "
            "before cutting into or replacing pipes, and the §104.2 exempt list has no item for waste-and-overflow replacement — both "
            "of its repair items stop at work 'not requiring cutting into or removal of piping'. The other twenty-three questions "
            "(physical condition, price and scope, provider capability, scheduling, contract terms) have no official source at all; "
            "no source read for this project answers them, so they are published with a discovery method rather than a value.",
            "Ask SF DBI in writing for the permit answer (Q07), then work the discovery sequence; its first two steps cost nothing "
            "but a phone call and a photograph.",
            c.pill("open — not an error", "warn"),
        ],
        "src": ["S01", "S222", "S232", "S44"],
    })

    # 7. Page ----------------------------------------------------------------
    c.PAGES["questions.html"] = {
        "title": "Open questions &amp; gaps",
        "eyebrow": "Decision support · every unresolved question · updated 2026-11-11",
        "h1": "What still has to be answered",
        "lede": "A hiring decision needs answers to these questions first. Each row states the question, why it changes the decision, "
                "who can answer it, and how to get the answer. Where no source answers a question the verified-answer cell is left blank "
                "and flagged — it is never filled in by inference.",
        "sections": [
            {"type": "callout", "tone": "info",
             "html": "<strong>How to use this page.</strong> Read the question register first. Then the gap table, which groups the "
                     "same questions by what kind of information is missing. Then the suggested discovery sequence, ordered by cost "
                     "and by what unblocks the most other answers. The 2026-11-11 re-read tables at the bottom record what was "
                     "checked today, so the age of each verified fact is visible."},
            {"type": "table", "ref": "open_questions"},
            {"type": "table", "ref": "gaps"},
            {"type": "table", "ref": "discovery_sequence"},
            {"type": "prose", "title": "What this page does not do",
             "html": "<p>It does not answer the questions, and it does not rank the contractors a second time — the ranked hiring "
                     "decision stays on its own page. It does not conclude whether a permit is required: only the San Francisco "
                     "Department of Building Inspection can decide that for a specific job, and Q07 records that the question is open. "
                     "It does not contact, book or price any provider.</p>"
                     "<p class=\"src\">Sources: the owner-provided project brief, the official pages named in each row, and this "
                     "session's dated re-read record. See the <a href=\"verification.html\">Verification</a> page and "
                     "<a href=\"flagged.html\">Flagged for Review</a>.</p>"},
            {"type": "table", "ref": "recheck_1111"},
            {"type": "table", "ref": "rules_1111"},
        ],
    }

    # Navigation: add the page to the Decision group, after the ranking links.
    for group in c.NAV:
        if group["group"] == "Decision":
            if not any(href == "questions.html" for href, _ in group["links"]):
                group["links"].append(("questions.html", "Open questions &amp; gaps"))
            break

    # Dashboard quick-link card, appended so existing cards keep their order.
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "quick":
            if not any(item["href"] == "questions.html" for item in block["items"]):
                block["items"].insert(3, {
                    "href": "questions.html",
                    "t": "Open questions &amp; gaps",
                    "d": "Every question that must be answered before hiring, who can answer it, and how to get the answer.",
                })
            break

    # Summary-page pointer so the executive summary links to the register.
    for block in c.PAGES["summary.html"]["sections"]:
        if block["type"] == "prose":
            block["html"] = block["html"] + (
                "<p class=\"src\"><strong>2026-11-11:</strong> twenty-five questions still have to be answered before a hiring "
                "decision — see the <a href=\"questions.html\">open questions and gaps register</a>, which states who can answer "
                "each one and how to get the answer.</p>")
            break

    _normalise(c)
    c.META["updated"] = "2026-11-11"
    c.META["session"] = "arena/e919fdc0-korea7"


def _normalise(c) -> None:
    ids = [r["cells"][0] for r in c.TABLES["flagged"]["rows"] if re.fullmatch(r"U\d+", str(r["cells"][0]))]
    max_flag = max(int(i[1:]) for i in ids)
    c.TABLES["flagged"]["rows"].sort(
        key=lambda r: (int(re.fullmatch(r"U(\d+)", str(r["cells"][0])).group(1))
                       if re.fullmatch(r"U\d+", str(r["cells"][0])) else 10 ** 6)
    )
    for page in c.PAGES.values():
        for block in page["sections"]:
            for key, value in list(block.items()):
                if isinstance(value, str):
                    value = re.sub(r"U01–U\d+", "U01–U%d" % max_flag, value)
                    value = re.sub(r"\b\d+ flagged items\b", "%d flagged items" % len(c.TABLES["flagged"]["rows"]), value)
                    block[key] = value
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "cards":
            for card in block["items"]:
                if card["k"] == "Flagged for review":
                    card["v"] = str(len(c.TABLES["flagged"]["rows"]))
