#!/usr/bin/env python3
"""Decision-register addendum for the overflow trip-lever project (2026-11-11).

The project brief asks for a clear list of questions, information and answers
needed before a decision. A concurrent session had already published that page
(`questions.html`, module `scripts/questions_data.py`, merged as PR #92) with
fourteen questions, six official answers and six discovery suggestions. This
module does **not** create or rewrite that page. It appends only:

* four official answers the published table did not cover — the CSLB home
  improvement contract requirements, how to compare bids and verify a firm, the
  insurance/bond evidence to request, and the statutory basis for entering an
  occupied unit;
* three discovery actions that close gaps no existing action named — obtain a
  certificate of insurance, ask the cited firm to explain its citation, and
  record the tenant-entry agreement in writing;
* one prose section on the existing page, pointing at those requirements;
* two findings: today's drift check and this extension.

Sources registered here (S220-S227) were each read directly on 2026-11-11 and
carry the data stamp the page itself printed. Nothing is inferred: a rule is
quoted or closely paraphrased, and any fact that only the owner, the tenant, a
contractor or the permit desk can supply is left to those rows.
"""
from __future__ import annotations

CHECKED = "2026-11-11"

NEW_SOURCES = {
    "S220": {
        "label": "CSLB License Detail #829071 — Ace Plumbing & Rooter — November 11 re-read",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current/active status; classifications C36, A, C-4, C16, B, C10; business address 1090 Bryant Street, San Francisco; business phone (415) 824-6444; expiry 06/30/2027; contractor's bond $25,000; workers' compensation policy 07/13/2026-07/13/2027",
        "note": "Read directly on cslb.ca.gov, 2026-11-11. The page printed 'Data current as of 11/10/2026 6:17:57 PM'.",
    },
    "S221": {
        "label": "CSLB License Detail #1025814 — The Genteel Plumbers Inc — November 11 re-read",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1025814",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current/active status; classifications C36, B; business address 1181 Revere Ave, San Francisco; business phone (833) 436-8335; expiry 04/30/2027; contractor's bond $25,000; workers' compensation policy 01/24/2026-01/24/2027",
        "note": "Read directly on cslb.ca.gov, 2026-11-11. The page printed 'Data current as of 11/10/2026 6:18:06 PM'.",
    },
    "S222": {
        "label": "CSLB License Detail #1003394 — Handyman Heroes Inc — November 11 re-read",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current/active status; classifications B, C36; business address 912 Cole St #202, San Francisco; business phone (844) 382-4376; expiry 05/31/2027; contractor's bond $25,000; workers' compensation policy 04/25/2026-04/25/2027; a complaint-disclosure link is published on the record",
        "note": "Read directly on cslb.ca.gov, 2026-11-11. The page printed 'Data current as of 11/10/2026 6:16:14 PM'.",
    },
    "S223": {
        "label": "SF.gov — Apply for a plumbing and mechanical permit — November 11 re-read",
        "publisher": "SF Department of Building Inspection",
        "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Permit required before cutting into or replacing pipes, particularly pipes covered by a wall; §104.2 exemptions; A, B, C4, C16, C20, C36 and C54 permit scopes; inspection before covering pipes; Permit Center help desk 628-652-4900 and permitsf@sfgov.org",
        "note": "Read directly on sf.gov, 2026-11-11. The page carried a City holiday notice for Wednesday, November 11.",
    },
    "S224": {
        "label": "CSLB — What should I look for in a contract and binding agreements?",
        "publisher": "Contractors State License Board",
        "url": "https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Written contract required for home improvement projects over $500 in combined labour and materials; required contents (work, price, payment schedule, who gets permits, completion, contractor identity/address/licence number); written change orders; three-day cancellation; down payment no more than 10% of the contract price or $1,000, whichever is less",
        "note": "Read directly on cslb.ca.gov, 2026-11-11. No page date is printed; the requirements above are quoted or closely paraphrased.",
    },
    "S225": {
        "label": "CSLB — How do I find the right licensed contractor?",
        "publisher": "Contractors State License Board",
        "url": "https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Licence number must appear on advertisements, bids and contracts; check status online or at (800) 321-CSLB (2752); get at least three written bids compared on identical plans/specifications/scope; ask for a Certificate of Insurance or the carrier's name; workers' compensation required for employers; commercial general liability not required but covers property damage; contractor licence bond $25,000 and its limits",
        "note": "Read directly on cslb.ca.gov, 2026-11-11 (page returned in two parts; the quoted text is from the part read in full).",
    },
    "S226": {
        "label": "California Business & Professions Code §7059 — November 11 re-read",
        "publisher": "California Legislative Information (leginfo)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7059",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "A specialty contractor may take and execute a contract involving two or more crafts or trades when the work outside its own craft is 'incidental and supplemental' to the work it is licensed for",
        "note": "Read directly on leginfo.legislature.ca.gov, 2026-11-11. The section is marked 'Amended by Stats. 2024, Ch. 485, Sec. 6. (SB 1455) Effective January 1, 2025.'",
    },
    "S227": {
        "label": "California Civil Code §1954 — landlord entry — November 11 re-read",
        "publisher": "California Legislative Information (leginfo)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "A landlord may enter to make necessary or agreed repairs; entry only during normal business hours except in an emergency or with the tenant's consent; the landlord must give reasonable written notice stating the date, approximate time and purpose (24 hours is presumed reasonable; six days if mailed); the tenant and landlord may agree orally to an agreed repair within one week",
        "note": "Read directly on leginfo.legislature.ca.gov, 2026-11-11. The section is marked 'Amended by Stats. 2018, Ch. 445, Sec. 1. (SB 721) Effective January 1, 2019.'",
    },
}


def _row(c, ident, first, second, third, status):
    return {"cells": [ident, first, second, third], "src": []}


def integrate(c) -> None:
    """Append the 2026-11-11 rows to the existing questions page. Additive only."""
    if "S227" in c.SOURCES:
        return
    missing = [t for t in ("questions", "answers", "discovery") if t not in c.TABLES]
    if missing or "questions.html" not in c.PAGES:
        raise RuntimeError(
            "questions_data.py must run before questions_1111.py (missing %s)" % missing)
    collisions = set(NEW_SOURCES).intersection(c.SOURCES)
    if collisions:
        raise ValueError("Session 16f70752 source-ID collision: %s" % sorted(collisions))
    c.SOURCES.update(NEW_SOURCES)

    answers = c.TABLES["answers"]
    answers["rows"].extend([
        {
            "cells": [
                "A07",
                "What must a home improvement contract contain, and how much can be paid up front?",
                "A written contract is required for home improvement work over $500 in combined labour and materials. CSLB says it should state the work, price, payment schedule, "
                "who obtains the necessary building permits and when the job will finish, and must identify the contractor with address and licence number; changes must be written change orders; "
                "there is a three-day right to cancel; and the down payment should never exceed 10% of the contract price or $1,000, whichever is less.",
                c.pill("official — CSLB", "ok"),
            ],
            "src": ["S224"],
        },
        {
            "cells": [
                "A08",
                "How many bids should be obtained, and how is the firm behind a bid verified?",
                "CSLB advises getting at least three written bids and comparing them on identical plans, specifications and scope, and warns that an abnormally low bid may omit work. "
                "The licence number must appear on advertisements, bids and contracts; the licence can be checked online or at (800) 321-CSLB (2752); the business address and phone on record can be verified, "
                "and the pocket licence and photo ID can be requested on site.",
                c.pill("official — CSLB", "ok"),
            ],
            "src": ["S225"],
        },
        {
            "cells": [
                "A09",
                "What insurance and bond evidence should be requested before work starts?",
                "CSLB advises asking for a copy of the Certificate of Insurance or the carrier's name. Workers' compensation is required if the contractor has employees; commercial general liability is not required "
                "but covers damage to the property, and a licensed contractor must give information about both types of insurance in the written contract. Every licensed contractor must file a $25,000 contractor licence bond, "
                "which CSLB warns is often not enough to cover a project worth more than the bond and does not assure integrity or competency.",
                c.pill("official — CSLB", "ok"),
            ],
            "src": ["S225", "S224"],
        },
        {
            "cells": [
                "A10",
                "On what basis may the landlord enter the occupied unit for the repair?",
                "Civil Code §1954 permits entry to make necessary or agreed repairs, only during normal business hours unless there is an emergency or the tenant consents, and requires reasonable written notice stating the date, "
                "approximate time and purpose; 24 hours is presumed reasonable (six days if mailed). The tenant and landlord may agree orally to an entry for an agreed repair within one week. "
                "The specific access window and notice for this unit remain a private arrangement.",
                c.pill("official — leginfo", "ok"),
            ],
            "src": ["S227", "S44"],
        },
    ])
    answers["caption"] = answers["caption"].rstrip() + (
        " Rows A07–A10 were added on 2026-11-11 from the CSLB consumer pages and Civil Code §1954 read that day; "
        "rows A01–A06 are unchanged.")

    discovery = c.TABLES["discovery"]
    discovery["rows"].extend([
        {
            "cells": [
                "D07",
                "Insurance evidence for the specific job (workers' compensation and general liability)",
                "Request a current Certificate of Insurance or the carrier's name, compare the policy dates with the CSLB record, and require the contract to state both insurance types.",
                c.pill("official requirement available", "ok"),
            ],
            "src": ["S225", "S224", "S220"],
        },
        {
            "cells": [
                "D08",
                "The significance of the 2020 citation published against one candidate",
                "Read the citation detail and ask the firm for a written explanation before it is treated as a finalist; CSLB publishes the citation but no penalty or outcome on the disclosure page.",
                c.pill("record available; explanation required", "warn"),
            ],
            "src": ["S151", "S155"],
        },
        {
            "cells": [
                "D09",
                "A documented, lawful access arrangement with the sitting tenant",
                "Agree the entry date, approximate time and purpose in writing under Civil Code §1954, or use the agreed-repair oral arrangement within one week, and give the schedule to the contractor.",
                c.pill("official requirement available", "ok"),
            ],
            "src": ["S227", "S44"],
        },
    ])
    discovery["caption"] = discovery["caption"].rstrip() + (
        " Rows D07–D09 were added on 2026-11-11 and are actions only: none has been carried out.")

    # One prose section on the existing page; the page's own callouts and order are untouched.
    sections = c.PAGES["questions.html"]["sections"]
    insert_at = len(sections)
    for i in range(len(sections) - 1, -1, -1):
        if sections[i]["type"] == "callout":
            insert_at = i
            break
    sections.insert(insert_at, {
        "type": "prose",
        "title": "Contract, insurance and access requirements (official, read 2026-11-11)",
        "html": (
            "<p>Four requirements decide how the chosen firm must be engaged, and each is stated by an official page read on "
            "2026-11-11. They are listed as answers A07–A10 and actions D07–D09 above; nothing in the earlier rows is changed.</p>"
            "<ul>"
            "<li><strong>The contract.</strong> For home improvement work over $500 in combined labour and materials a written contract is required. "
            "It should state the work, price, payment schedule, who obtains permits and the completion date, identify the contractor with address and licence number, and any change must be a written change order. "
            "The down payment should never exceed 10% of the contract price or $1,000, whichever is less. Source: " +
            c.slink("S224", "CSLB contracts page") + ".</li>"
            "<li><strong>The bids and the licence check.</strong> CSLB advises at least three written bids compared on identical plans, specifications and scope; the licence number must appear on bids and contracts; "
            "the licence can be checked at CSLB or (800) 321-CSLB (2752), and the business address and phone on record verified. Source: " +
            c.slink("S225", "CSLB finding the right contractor") + ".</li>"
            "<li><strong>Insurance and the bond.</strong> Ask for a Certificate of Insurance; workers' compensation is required for employers; commercial general liability is not required but covers property damage. "
            "The $25,000 contractor licence bond is on record for each leading candidate but CSLB warns it may not cover a project worth more than the bond and does not assure integrity or competency. Sources: " +
            c.slink("S225", "CSLB") + ", " + c.slink("S220", "Ace") + ", " + c.slink("S221", "Genteel") + ", " + c.slink("S222", "Handyman Heroes") + ".</li>"
            "<li><strong>Entering the occupied unit.</strong> Civil Code §1954 allows entry to make necessary or agreed repairs, requires reasonable written notice with the date, approximate time and purpose, and presumes 24 hours (six days if mailed) to be reasonable. Source: " +
            c.slink("S227", "Civil Code §1954") + ".</li>"
            "</ul>"
            "<p>The three licence records and the sf.gov permit page were re-read the same day with no field-level drift from what this dashboard already published. "
            "That is a check of the records, not evidence that any firm will accept this job, name a price, or perform the ceiling work.</p>"
        ),
    })

    c.TABLES["findings"]["rows"].extend([
        {
            "cells": [
                "F20",
                "The three leading licence records and the sf.gov permit page re-read on 2026-11-11 show no drift from the published dashboard",
                "CSLB #829071, #1025814 and #1003394 re-read directly: all current and active; the classes, business phones and addresses already published; workers' compensation and $25,000 bond fields present; "
                "each record printed a 11/10/2026 data stamp. The sf.gov plumbing/mechanical permit page carried the same requirement wording and the same Permit Center contact details.",
                c.pill("verified 2026-11-11", "ok"),
            ],
            "src": ["S220", "S221", "S222", "S223"],
        },
        {
            "cells": [
                "F21",
                "The questions page did not yet cite the contract, insurance or tenant-entry requirements",
                "The published page listed fourteen questions, six official answers and six discovery suggestions but did not cite the CSLB contract requirements, the CSLB bidding/verification guidance, "
                "the insurance and bond limits, or Civil Code §1954. Four answers and three actions were appended on 2026-11-11; no existing row, score or page was rewritten and no provider was contacted.",
                c.pill("addressed 2026-11-11", "info"),
            ],
            "src": ["S224", "S225", "S227", "S45"],
        },
    ])

    c.META["updated"] = "2026-11-11"
    c.META["session"] = "arena/16f70752-korea7"
