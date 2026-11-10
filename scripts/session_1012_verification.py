#!/usr/bin/env python3
"""Job-specific call priorities and a separately checked candidate (2026-11-10).

The historical 16-record, CSLB-only score is deliberately unchanged. The newer
call order is editorial: company self-descriptions and third-party reviews help
decide whom to ask, but do not prove a vendor will perform this job. Every new
candidate row links its own CSLB record; unknown website, price, service area,
availability and complete scope stay explicitly unverified.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = json.loads((ROOT / "data/canonical/session-1012-verification.json").read_text(encoding="utf-8"))
CHECKED = "2026-11-10"

NEW_SOURCES = {
    "S205": {
        "label": "CSLB License Detail #1034873 — Plumbing 1 Builder's Inc",
        "publisher": "Contractors State License Board",
        "url": EVIDENCE["additional_candidate"]["sources"]["license"],
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Current and active C-36 and B, Hayward address, (650) 868-8059, license expiry, bond and workers' compensation dates",
        "note": "Read directly on 2026-11-10; record printed 'Data current as of 11/9/2026 9:51:51 PM'. This separately identified candidate is outside the original 16-record score.",
    },
    "S207": {
        "label": "Yelp — Atlas stuck bathtub-lever search-result excerpt",
        "publisher": "Yelp",
        "url": EVIDENCE["review_evidence"]["atlas"]["url"],
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "Indexed third-party review excerpt attributed to Atlas describes stuck bathtub drain levers and replacement of their assemblies",
        "note": "Search-result text only; direct Yelp fetch returned HTTP 403. The conditions, access route, ceiling work and outcome are not independently verified.",
    },
    "S208": {
        "label": "Yelp — Bay Area Plumbing search-result portfolio excerpt",
        "publisher": "Yelp",
        "url": "https://www.yelp.com/search?find_desc=Bay+Area+Plumbing&find_loc=San+Francisco%2C+CA",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "A later third-party search result shows a similar bathtub portfolio caption under Bay Area Plumbing",
        "note": "Search-result text only. It demonstrates why the previous Ace attribution is unreliable; it is not independent proof of either firm's workmanship.",
    },
    "S209": {
        "label": "Yelp — Handlify wall-repair search-result excerpt",
        "publisher": "Yelp",
        "url": "https://www.yelp.com/search?find_desc=Wall+Repair&find_loc=Glen+Park%2C+San+Francisco%2C+CA",
        "tier": "platform", "status": "blocked-403", "checked": CHECKED,
        "supports": "A third-party search result associates the Mikhail drywall excerpt with Handlify rather than Handyman Heroes",
        "note": "Search-result text only; direct Yelp access was blocked. The excerpt is removed from the Handyman Heroes record and is not scored.",
    },
    "S210": {
        "label": "HomeAdvisor — Plumbing 1 Builder's Inc customer reviews",
        "publisher": "HomeAdvisor / Angi",
        "url": EVIDENCE["review_evidence"]["plumbing_1_builders"]["url"],
        "tier": "platform", "status": "verified", "checked": CHECKED,
        "supports": "An October 2025 customer review describes a larger project including bathtub installation and ceiling repair after leaks",
        "note": "The platform page was read directly. This is one third-party account, not proof that the ceiling was under that tub, that a stuck lever was fixed, or that the company will accept this project.",
    },
    "S211": {
        "label": "Previously listed Plumbing 1 Builders domain — unavailable",
        "publisher": "Website host response",
        "url": EVIDENCE["additional_candidate"]["previously_listed_domain"],
        "tier": "other", "status": "dead", "checked": CHECKED,
        "supports": "The previously listed domain returned a 'Site not found' page when fetched",
        "note": "The company website is not currently verified. Leave the website field blank; contact the business using the official CSLB phone.",
    },
    "S212": {
        "label": "CSLB Complaint Disclosure #1034873",
        "publisher": "Contractors State License Board",
        "url": EVIDENCE["additional_candidate"]["sources"]["complaint_disclosure"],
        "tier": "official", "status": "verified", "checked": CHECKED,
        "supports": "Complaint-disclosure page showed the business name and license number, with no Citations table",
        "note": "Read directly on 2026-11-10. This does not establish that no complaint exists; CSLB restricts public disclosure by law.",
    },
    "S213": {
        "label": "Job-fit verification record — 2026-11-10",
        "publisher": "This project, with linked primary and third-party sources",
        "url": "data/canonical/session-1012-verification.json",
        "tier": "primary", "status": "verified", "checked": CHECKED,
        "supports": "Dated transcription for the additional license, contact, disclosure, review limitations and attribution corrections",
        "note": "This record describes the reads; government and company source pages remain the authorities for their own facts.",
    },
}


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _link(c, sid: str, label: str) -> str:
    url = _esc(c.SOURCES[sid]["url"])
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (url, _esc(label))


def _company(c, name: str, license_sid: str, license_no: str, phone: str,
             website_sid: str | None, extra: str = "") -> str:
    parts = ["<strong>%s</strong>" % _esc(name),
             _link(c, license_sid, "CSLB #%s" % license_no),
             "CSLB phone: <strong>%s</strong>" % _esc(phone)]
    if website_sid:
        parts.append(_link(c, website_sid, "business website"))
    else:
        parts.append("Business website: %s %s" % (c.BLANK, c.UNVERIFIED))
    if extra:
        parts.append(_esc(extra))
    return "<br>".join(parts)


def _qualify_original_pool(c) -> None:
    """Keep prior 16-record audits explicitly scoped to the historical pool."""
    replacements = (
        ("all sixteen CSLB records and the three official rule pages cited here",
         "all sixteen CSLB records in the original scored pool and the three official rule pages cited there"),
        ("all sixteen licence numbers was read", "all sixteen original scored-pool licence numbers was read"),
        ("all sixteen records re-read", "all sixteen original scored-pool records re-read"),
        ("All sixteen published licence numbers", "All sixteen original scored-pool licence numbers"),
        ("all sixteen published licence numbers", "all sixteen original scored-pool licence numbers"),
        ("<strong>all sixteen</strong> published licence numbers", "<strong>all sixteen</strong> licence numbers in the original scored pool"),
        ("All sixteen CSLB License Detail records", "All sixteen original scored-pool CSLB License Detail records"),
        ("all sixteen licences used by the ranking", "all sixteen licences in the original numeric ranking"),
        ("all sixteen license records cited in this project", "all sixteen license records in the original scored pool"),
        ("all 16 published licences", "all 16 original scored-pool licences"),
    )

    def apply(value: str) -> str:
        for old, new in replacements:
            value = value.replace(old, new)
        return value

    for page in c.PAGES.values():
        for block in page["sections"]:
            for key, value in list(block.items()):
                if isinstance(value, str):
                    block[key] = apply(value)
    for table in c.TABLES.values():
        if "title" in table:
            table["title"] = apply(table["title"])
        if "caption" in table:
            table["caption"] = apply(table["caption"])
        for row in table["rows"]:
            row["cells"] = [apply(cell) if isinstance(cell, str) else cell for cell in row["cells"]]
    for source in c.SOURCES.values():
        for key in ("label", "supports", "note"):
            source[key] = apply(source[key])


def _normalise_flags(c) -> None:
    rows = c.TABLES["flagged"]["rows"]
    rows.sort(key=lambda row: int(row["cells"][0][1:]) if re.fullmatch(r"U\d+", str(row["cells"][0])) else 10**6)
    numbers = [int(row["cells"][0][1:]) for row in rows if re.fullmatch(r"U\d+", str(row["cells"][0]))]
    maximum = max(numbers)
    for page in c.PAGES.values():
        for block in page["sections"]:
            for key, value in list(block.items()):
                if isinstance(value, str):
                    value = re.sub(r"U01–U\d+", "U01–U%d" % maximum, value)
                    value = re.sub(r"\b\d+ flagged items\b", "%d flagged items" % len(rows), value)
                    block[key] = value
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "cards":
            for card in block["items"]:
                if card["k"] == "Flagged for review":
                    card["v"] = str(len(rows))


def integrate(c) -> None:
    if "job_fit_1012" in c.TABLES:
        return
    collisions = set(NEW_SOURCES).intersection(c.SOURCES)
    if collisions:
        raise ValueError("Session 1012 source-ID collision: %s" % sorted(collisions))
    c.SOURCES.update(NEW_SOURCES)
    _qualify_original_pool(c)

    blank_cost = c.BLANK + " " + c.UNVERIFIED
    rows = [
        {
            "cells": [
                "<strong>1 · conditional one-stop</strong>",
                _company(c, "Handyman Heroes", "S10", "1003394", "(844) 382-4376", "S201"),
                "CSLB lists B + C-36. Its company pages advertise bathtub plumbing and wall patching after plumbing openings; a company-selected testimonial describes a multifamily rental. A third-party Yelp excerpt describes wall work after plumbing, not necessarily the same contractor for both trades.",
                "Ask for a careful above-first assessment and one contract for any ceiling work. CSLB publishes a 2020 citation including departures from trade standards and contract issues; review it and ask for an explanation before hiring.",
                blank_cost,
            ],
            "src": ["S10", "S201", "S202", "S203", "S206", "S155"],
        },
        {
            "cells": [
                "<strong>2 · managed-building alternative</strong>",
                _company(c, "Ace Plumbing & Rooter", "S11", "829071", "(415) 824-6444", "S43"),
                "CSLB lists B + C-36. The company describes substantial HOA and property-manager experience, useful for coordinating an occupied building; it does not establish this repair's outcome.",
                "Drywall or ceiling self-performance is not advertised on the pages read. Ask who restores the ceiling, whether the work is included, and for a written stop-and-price point before any opening.",
                blank_cost,
            ],
            "src": ["S11", "S43", "S83"],
        },
        {
            "cells": [
                "<strong>3 · new conditional lead</strong>",
                _company(c, "Plumbing 1 Builder's Inc", "S205", "1034873", "(650) 868-8059", None),
                "CSLB lists active B + C-36. A third-party HomeAdvisor review describes a larger project with bathtub installation and separate ceiling repair. It does not establish that the ceiling was under the tub or that a seized lever was repaired.",
                "Hayward address; San Francisco service and a current company website are unconfirmed. Ask about travel, the combined scope, and workers' compensation renewal if work extends past 2026-12-30. Separately checked, not part of the original score.",
                blank_cost,
            ],
            "src": ["S205", "S212", "S210", "S213"],
        },
        {
            "cells": [
                "<strong>4 · job-specific plumbing lead</strong>",
                _company(c, "Atlas Plumbing & Rooter", "S69", "868994", "(650) 871-9863", "S200",
                         "Company site also publishes (415) 849-2346; difference unconfirmed."),
                "CSLB lists C-36 and A, not B or C-9. A third-party Yelp search excerpt attributes replacement of stuck bathtub drain lever assemblies to Atlas; it does not establish the same pipe condition or access route.",
                "Ask whether the actual seized assembly can be handled without stressing the hidden piping and who will open and restore the ceiling. Both published phone numbers need confirmation.",
                blank_cost,
            ],
            "src": ["S69", "S200", "S204", "S207", "S62"],
        },
        {
            "cells": [
                "<strong>5 · waste-and-overflow specialist lead</strong>",
                _company(c, "Fast Response Plumbing & Rooter", "S08", "1024971", "(415) 596-6115", "S61"),
                "CSLB lists C-36; the company's own page explicitly lists bathtubs (waste & overflow). The owner reports a $135 handle-adjustment quote, not an independently verified price or a ceiling-inclusive scope.",
                "Ask for a written staged price and how ceiling restoration would be covered. The workers' compensation policy on the record expires 2026-12-18; request renewal proof if the work extends beyond then.",
                blank_cost,
            ],
            "src": ["S08", "S61", "S44", "S62"],
        },
    ]
    c.TABLES["job_fit_1012"] = {
        "title": "Practical call priority for this job — 2026-11-10",
        "columns": ["Priority", "Company and official contact", "Why call (evidence and limits)",
                    "Key caution / question", "Verified all-in price", "Source"],
        "rows": rows,
        "caption": ("Editorial call priority, not a guarantee and not the CSLB-only numeric score below. "
                    "The newly identified Plumbing 1 Builders lead is outside the original 16-record scored pool. "
                    "Company statements are self-reported and reviews are third-party anecdotes. No contractor "
                    "has been contacted or confirmed this trip-lever job, ceiling scope, availability or price."),
    }
    c.TABLES["additional_contact_1012"] = {
        "title": "Additional separately checked contact — not in the 16-record score",
        "columns": ["Company", "CSLB phone", "Verified company site", "Status and limits", "Source"],
        "rows": [{
            "cells": [
                "<strong>Plumbing 1 Builder's Inc</strong><br>" + _link(c, "S205", "CSLB #1034873"),
                "(650) 868-8059",
                c.BLANK + " " + c.UNVERIFIED,
                "CSLB lists active B + C-36; website, San Francisco service and availability remain UNVERIFIED. The formerly listed domain returned a site-not-found page.",
            ],
            "src": ["S205", "S212", "S213"],
        }],
        "caption": "Phone and license from CSLB on 2026-11-10. A company site is left blank because no current business page was confirmed.",
    }

    ranking = c.PAGES["ranking.html"]
    ranking["lede"] = ("The first table prioritizes calls for the actual repair. The following numeric tables "
                       "score only the original 16 candidates' CSLB fields; the additional lead is checked "
                       "separately, not scored. Company claims and third-party reviews are evidence to investigate, "
                       "not guarantees or inputs to the numerical score.")
    ranking["sections"].insert(2, {"type": "table", "ref": "job_fit_1012"})
    for block in ranking["sections"]:
        if block["type"] == "cards":
            for card in block["items"]:
                if card["k"] == "License records re-read":
                    card["k"] = "Original scored-pool records"
                    card["s"] = "16 re-checked; one additional lead checked separately"
                elif card["k"] == "All-in-one candidates":
                    card["k"] = "Dual-classified in scored pool"
                    card["s"] = "C-36 + B; actual combined scope unconfirmed"
    c.TABLES["call_order"]["title"] = "Historical license-score call sequence and questions"
    c.TABLES["call_order"]["caption"] = ("This historical sequence follows the original CSLB-only score, not the "
        "job-fit priority above; the newly identified lead is not included. CSLB and company phone differences "
        "are flagged. No outreach has been performed.")

    lead = (
        "<p><strong>Practical first calls:</strong> " + _link(c, "S10", "Handyman Heroes") +
        " advertises both plumbing and wall patching (company statements); review its " +
        _link(c, "S155", "2020 CSLB citation") + " and require a clear written scope before hiring. " +
        _link(c, "S11", "Ace") + " is a second one-contract candidate, with company-reported property-manager "
        "experience but no advertised ceiling commitment. A separately checked " +
        _link(c, "S205", "Plumbing 1 Builders") + " is a conditional lead; " +
        _link(c, "S69", "Atlas") + " has a relevant third-party stuck-lever review excerpt. "
        "These are call priorities, not confirmed abilities or prices. "
        '<a href="ranking.html">See the job-fit comparison and all cautions</a>.</p>'
    )
    c.PAGES["summary.html"]["sections"].insert(2, {
        "type": "prose", "title": "Practical call order for this repair", "html": lead,
    })
    c.PAGES["index.html"]["sections"].insert(2, {
        "type": "callout", "tone": "info",
        "html": ("<strong>Start with a staged, written scope.</strong> See the "
                 '<a href="ranking.html">job-specific call priority</a> before the historical license-only scores; '
                 "review the CSLB citation, service-area and ceiling-restoration cautions before booking."),
    })
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "cards":
            for card in block["items"]:
                if card["k"] == "Verified license records":
                    card["v"] = "17"
                    card["s"] = "16 in the original scored pool; one additional CSLB record checked separately"
    c.PAGES["contacts.html"]["sections"].insert(1, {"type": "table", "ref": "additional_contact_1012"})

    for row in c.TABLES["repo_review"]["rows"]:
        if row["cells"][0] == "New verified datasets":
            row["cells"][1] = ("The original 2026-11-08 inputs contained 16 CSLB records, 10 company sites and "
                               "6 review snapshots. The company-site dataset was subsequently updated on 2026-11-10 "
                               "with Atlas and a Handyman Heroes re-read; reviews remain third-party.")
            row["cells"][2] = ("The original records and sites were read on 2026-11-08. Later company-page reads "
                               "are dated separately and do not verify workmanship or a current quote.")
            row["src"].extend(["S200", "S201"])
        elif row["cells"][0] == "Candidate pool completeness":
            row["cells"][1] = ("The original 2026-11-08 canonical pool covered 16 license numbers identified in "
                               "the earlier parallel sites. A separately checked lead, #1034873, was identified "
                               "on 2026-11-10 and is outside that historical score.")
            row["src"].append("S205")
        elif str(row["cells"][0]).startswith("Complaint-disclosure audit 2026-11-10"):
            row["cells"][1] = row["cells"][1].replace("all sixteen original scored-pool licence numbers", "all sixteen licence numbers in the original scored pool")
    original_license_sources = ["S06", "S07", "S08", "S09", "S10", "S11", "S56", "S57",
                                "S64", "S65", "S66", "S67", "S68", "S69", "S70", "S71"]
    for row in c.TABLES["findings"]["rows"]:
        if row["cells"][0] == "F04":
            row["cells"][1] = "All sixteen originally scored candidates held active CSLB licenses when checked 2026-11-08"
            row["src"].extend(original_license_sources)
        elif row["cells"][0] == "F14":
            row["cells"][1] = "Every originally scored candidate has a CSLB-published phone number"
            row["src"].extend(original_license_sources)
    for row in c.TABLES["technical"]["rows"]:
        if row["cells"][0] == "Above-access removal":
            row["cells"][1] = ("Routine publisher and manufacturer instructions describe removing the overflow "
                                "faceplate and withdrawing linkage on some free-moving assemblies.")
            row["cells"][2] = ("This fixture is reportedly seized; do not force it. A licensed plumber must "
                                "assess the actual assembly and stop if the hidden piping could be damaged.")
            row["src"].extend(["S93", "S44"])
    for row in c.TABLES["review_snapshots"]["rows"]:
        if row["cells"][0].startswith("Fast Response") and "S08" not in row["src"]:
            row["src"].append("S08")  # Identity only, not independent verification of the review claim.
    for table_id in ("delivery_checks", "recheck_company"):
        for row in c.TABLES[table_id]["rows"]:
            if "company" not in " ".join(row["cells"]).lower() and table_id == "delivery_checks":
                continue
            identity = " ".join(row["cells"])
            if table_id == "delivery_checks":
                sid = "S105" if "Ace" in identity else ("S106" if "Genteel" in identity else None)
            else:
                sid = "S138" if "Ace" in identity else ("S141" if "Genteel" in identity else None)
            if sid and sid not in row["src"]:
                row["src"].append(sid)
    for row in c.TABLES["recheck_deltas"]["rows"]:
        row["src"].extend("S%d" % n for n in range(133, 149))
    c.TABLES["findings"]["rows"].append({
        "cells": ["F19", "A job-specific call order can differ from a license-only score",
                  "Handyman Heroes advertises both plumbing and wall repair; Atlas has a third-party stuck-lever excerpt; the separately checked Plumbing 1 Builders has a third-party account of bathtub and ceiling work. These statements do not verify this job or a complete quote.",
                  c.pill("company and third-party statements — UNVERIFIED", "warn")],
        "src": ["S10", "S201", "S202", "S69", "S207", "S205", "S210"],
    })

    next_flag = max(int(r["cells"][0][1:]) for r in c.TABLES["flagged"]["rows"]
                    if re.fullmatch(r"U\d+", str(r["cells"][0]))) + 1
    flags = [
        ("Search-result attribution corrections",
         "A bathtub portfolio caption was withdrawn from Ace because the result attribution was ambiguous; a drywall excerpt attributed to Handyman Heroes was associated with another business in later search text. Both are third-party and unverified.",
         "Review original Yelp pages manually if accessible; do not use the withdrawn excerpts as evidence or score inputs.",
         ["S11", "S10", "S77", "S78", "S208", "S209"]),
        ("Atlas company and CSLB phone numbers differ",
         "The CSLB record lists (650) 871-9863 while Atlas's own site lists (415) 849-2346. Both are published; which line is preferred is not confirmed.",
         "Confirm the working contact with the company before arranging a visit.", ["S69", "S200"]),
        ("Additional lead: website, San Francisco service and scope unconfirmed",
         "Plumbing 1 Builder's Inc has an active B + C-36 record, but the previously listed domain returned site not found. San Francisco travel, current availability, trip-lever work and an integrated ceiling quote are unverified; the workers' compensation record expires 2026-12-30.",
         "Call the CSLB-listed number, confirm the current website and travel, obtain a complete written quote and verify coverage through the work dates.", ["S205", "S212", "S210", "S213"]),
    ]
    for offset, (title, why, action, src) in enumerate(flags):
        c.TABLES["flagged"]["rows"].append({
            "cells": ["U%d" % (next_flag + offset), title, why, action, c.UNVERIFIED], "src": src,
        })
    _normalise_flags(c)
    c.META["session"] = "arena/1012d038-korea7"
