"""Dated accuracy and occupant-safety follow-up for the plumbing dashboard.

Keep previously integrated research and scores, but correct unsupported
project-specific conclusions.  Government links establish general guidance,
not the condition, legal status, scope or price of a particular property.
"""
from __future__ import annotations

import re


NEW_SOURCES = {
    "S500": {
        "label": "EPA — Lead Renovation, Repair and Painting Program",
        "publisher": "U.S. Environmental Protection Agency",
        "url": "https://www.epa.gov/lead/lead-renovation-repair-and-painting-program",
        "tier": "official", "status": "verified", "checked": "2026-11-11",
        "supports": "EPA describes lead-safe requirements for covered paid renovations disturbing painted surfaces in pre-1978 housing and child-occupied facilities.",
        "note": "Direct read 2026-11-11. Building age, paint and applicability to this job are unknown; exceptions and the complete rule must be checked.",
    },
    "S501": {
        "label": "EPA — Protect Your Family from Exposures to Asbestos",
        "publisher": "U.S. Environmental Protection Agency",
        "url": "https://www.epa.gov/asbestos/protect-your-family-exposures-asbestos",
        "tier": "official", "status": "verified", "checked": "2026-11-11",
        "supports": "EPA advises leaving suspected asbestos material undisturbed and using trained and accredited professionals for assessment or work that could disturb it.",
        "note": "Direct read 2026-11-11. No asbestos has been identified at this property.",
    },
    "S502": {
        "label": "San Francisco Rent Board — Landlord Access to a Unit",
        "publisher": "San Francisco Rent Board",
        "url": "https://www.sf.gov/information--landlord-access-unit",
        "tier": "official", "status": "verified", "checked": "2026-11-11",
        "supports": "For covered landlord entry, the Rent Board discusses written notice, mailing timing, normal hours, exceptions and consent.",
        "note": "Direct read 2026-11-11. Whether and how these rules apply to the particular dwelling and storage arrangement remains unconfirmed.",
    },
}


def _section(c, page: str, title: str):
    return next(b for b in c.PAGES[page]["sections"] if b.get("title") == title)


def _replace_once(value: str, old: str, new: str) -> str:
    if old not in value:
        raise ValueError("Expected dashboard wording not found: %r" % old)
    return value.replace(old, new, 1)


def integrate(c) -> None:
    if "safety_followup_1111" in c.TABLES:
        return
    if set(NEW_SOURCES) & set(c.SOURCES):
        raise ValueError("November 11 source IDs collide")
    c.SOURCES.update(NEW_SOURCES)
    blank = c.BLANK + " " + c.UNVERIFIED

    # The figures are useful owner-supplied context, not independently confirmed
    # values. Keep them in explicitly attributed prose, not in numerical cells.
    quote_table = c.TABLES["brief_quotes"]
    quote_table["columns"][3] = "Independently confirmed amount"
    for row in quote_table["rows"]:
        row["cells"][3] = blank
    quote_table["caption"] = (
        "Scope and date are transcribed as owner-reported context, not independently confirmed. "
        "The independently confirmed amount cells are blank and flagged; the owner-provided figures "
        "are described in the non-table note above. CSLB verifies business records, not private quotes."
    )
    c.TABLES["estimates"]["columns"][2] = "Reported scope (not verified)"
    c.TABLES["estimates"]["columns"][4] = "Reported date (not verified)"
    c.TABLES["estimates"]["caption"] = (
        "Scopes and dates are owner-reported; the amounts are blank because the estimates have not "
        "been independently confirmed. CSLB verifies the business and license, not the private quote. "
        "Ceiling restoration, access method and total price remain unconfirmed."
    )
    owner_note = {
        "type": "prose", "title": "Owner-reported estimates — not confirmed",
        "html": (
            "<p>The owner reports receiving the following estimates on 2026-08-30: "
            "<strong>Expert Plumbing Solutions $614</strong> for replacing the waste and overflow; "
            "<strong>Bay Area Plumbing $550</strong> for the bathtub plug lever and diverter spout "
            "including labor and materials; and <strong>Fast Response $135</strong> to repair or adjust "
            "the plunger handle. These are attributed reports, not independently verified bids or "
            "comparable all-in totals. Whether any includes ceiling opening or restoration is unknown. "
            "Obtain the original written proposals and itemized updates before relying on them. "
            "See <a href=\"flagged.html\">Flagged for Review</a>.</p>"
        ),
    }
    for page in ("brief.html", "estimates.html"):
        c.PAGES[page]["sections"].insert(0, dict(owner_note))
    for row in c.TABLES["requirements"]["rows"]:
        if row["cells"][0] in {"R05", "R06", "R07"}:
            row["cells"][1] = re.sub(r"; owner-reported \$(?:614|550|135)", "; owner-reported scope", row["cells"][1])
    flags = {row["cells"][0]: row for row in c.TABLES["flagged"]["rows"]}
    flags["U01"]["cells"][1] = "Three owner-reported estimate amounts and the supplied problem facts"
    for row in c.TABLES["job_fit_1012"]["rows"]:
        row["cells"][2] = row["cells"][2].replace(
            "The owner reports a $135 handle-adjustment quote, not an independently verified price or a ceiling-inclusive scope.",
            "The owner reports a handle-adjustment quote; the amount and ceiling-inclusive scope are not independently confirmed.",
        )

    # A blocked platform cannot verify a current numeric rating or review count.
    snapshots = c.TABLES["review_snapshots"]
    snapshots["columns"][1] = "Current rating / count confirmed from platform"
    snapshots["caption"] = (
        "Direct Yelp access returned HTTP 403 on 2026-11-11, so rating and count cells are blank. "
        "The linked historical excerpts are third-party material, not proof of licensure or job-specific workmanship."
    )
    for row in snapshots["rows"]:
        row["cells"][1] = blank
    reviews = c.TABLES["reviews_1108"]
    reviews["columns"][2] = "Current rating confirmed"
    reviews["columns"][3] = "Current count confirmed"
    for row in reviews["rows"]:
        row["cells"][2] = blank
        row["cells"][3] = blank
    reviews["caption"] += " Current numeric rating and count cells are blank; excerpts remain third-party search snapshots."
    for sid in ("S32", "S33", "S34", "S35", "S36", "S37"):
        c.SOURCES[sid]["note"] = "Direct Yelp access returned HTTP 403; prior-session numeric snapshots were not re-verified and are not current values."
    c.SOURCES["S40"]["supports"] = "Company states CSLB #1024971, C-36, service to houses/apartments/HOAs/property managers, and a review aggregate; its aggregate is not independent verification."
    c.SOURCES["S79"]["supports"] = "Handyman Heroes result snapshot includes a platform badge and review text; the review count varies across results."
    c.SOURCES["S80"]["supports"] = "Third-party result lists drywall repair, wall patching, wall finishing and texturing; numeric values are not independently confirmed."
    c.SOURCES["S81"]["supports"] = "Third-party search result and FAQ show inconsistent numeric ratings; neither is an official verification."
    flags["U09"]["cells"][1] = "Fast Response company aggregate review claim"
    flags["U26"]["cells"][2] = "Prior indexed Yelp results showed inconsistent ratings or counts for several firms; direct Yelp access was blocked."

    # Published estimates are publisher statements, not official job prices.
    for row in c.TABLES["benchmarks"]["rows"]:
        row["cells"][4] = c.pill("publisher estimate; job cost UNVERIFIED", "warn")
        if row["cells"][0].startswith("New drywall"):
            row["cells"][3] = "National publisher estimate; whether any received quote includes ceiling work is unconfirmed"
    c.TABLES["benchmarks"]["caption"] = (
        "Each link is the publisher's own article; these are third-party national estimates, not "
        "government-verified prices, San Francisco bids or confirmed prices for this job. "
        "Publisher dates not available in the source remain blank and flagged."
    )
    numbers = _section(c, "summary.html", "3. What the numbers mean")
    numbers["html"] = _replace_once(
        numbers["html"], "Drywall is not included in any of the three quoted scopes.",
        "The supplied descriptions do not establish whether ceiling or drywall restoration is included in any quote.",
    )

    # City wallboard guidance contains a material fire-protection exception.
    c.SOURCES["S02"]["checked"] = "2026-11-11"
    c.SOURCES["S02"]["supports"] = "The City lists minor repairs to existing interior plaster or wallboard unless required for fire protection; applicability to this ceiling is not established."
    c.SOURCES["S02"]["note"] = "Direct re-read 2026-11-11. The City states the fire-protection qualifier; determine the actual ceiling assembly and scope with SF DBI."
    c.SOURCES["S01"]["note"] += " Directly re-read 2026-11-11; the City references exemptions and says license scope depends on the work."
    c.TABLES["questions"]["columns"][2] = "Known source statements and owner reports"
    questions = {row["cells"][0]: row for row in c.TABLES["questions"]["rows"]}
    questions["Q03"]["cells"][2] = (
        "SF.gov lists minor repairs to existing interior plaster or wallboard, unless required for fire protection, "
        "among work not needing a building permit. Whether this ceiling qualifies is unknown. "
        "The owner reports a storage unit below."
    )
    questions["Q09"]["cells"][2] = (
        "SF.gov describes permits for cutting or replacing pipes and refers to exemptions; it lists minor "
        "interior plaster or wallboard repairs unless required for fire protection. License classes and scope "
        "limitations are described by the City. BPC §7048 describes a conditional minor-work licensing exemption."
    )
    answers = {row["cells"][0]: row for row in c.TABLES["answers"]["rows"]}
    answers["A06"]["cells"][2] = (
        "SF.gov lists minor repairs to existing interior plaster or wallboard unless required for fire protection. "
        "Whether this ceiling or the plumbing work qualifies is unconfirmed."
    )
    rules = _section(c, "summary.html", "5. Official rules (neutral)")
    rules["html"] = _replace_once(
        rules["html"], "“minor repairs to existing interior plaster or wallboard”",
        "“minor repairs to existing interior plaster or wallboard, unless they are required for fire protection”",
    )
    ranking = _section(c, "summary.html", "License-record ranking (added 2026-11-08)")
    ranking["html"] = _replace_once(
        ranking["html"],
        "which is what lets one contractor perform the plumbing and the ceiling restoration under one contract",
        "a screening signal for a combined request, not a commitment to perform or arrange ceiling restoration",
    )
    next_steps = _section(c, "summary.html", "6. Recommended next steps")
    next_steps["html"] = (
        "<ol class=\"tight\"><li><strong>Start with the practical call priority</strong> on the "
        "<a href=\"ranking.html\">ranked hiring page</a>; its job-fit inquiry order is distinct "
        "from the historical license-only score. Obtain at least three comparable written bids "
        "(" + c.slink("S91", "CSLB hiring guidance") + ").</li>"
        "<li>Ask for an above-first assessment, a separately priced below-access option, ceiling finish, "
        "tenant protection, an appropriate leak test and a stop-and-price point.</li>"
        "<li>Recheck the chosen CSLB record and complaint disclosure on the hire date; verify actual "
        "crew coverage and expiring policies. See the <a href=\"reread-1111.html\">November 11 record re-read</a>.</li>"
        "<li>Confirm access, material and permit applicability for the exact work; review "
        "<a href=\"decision-checklist.html\">the decision checklist</a> and "
        "<a href=\"flagged.html\">Flagged for Review</a>.</li></ol>"
    )

    # Earlier checklist-session limitations remain true for that session only.
    for page in ("index.html", "flagged.html", "decision-checklist.html"):
        for block in c.PAGES[page]["sections"]:
            if "html" not in block:
                continue
            block["html"] = block["html"].replace(
                "No new external verification is claimed on November 11: this runtime restricts non-GitHub network access.",
                "No new external verification is claimed for the earlier checklist session; a later November 11 follow-up re-read selected sources, not every site claim.",
            ).replace(
                "external non-GitHub source access is restricted in this runtime.",
                "the earlier checklist session could not access external non-GitHub sources.",
            ).replace(
                "no new contractor acceptance, quote or external re-verification is claimed.",
                "no contractor acceptance or confirmed quote is claimed; the later source spot-check is separately dated.",
            )
    for block in c.PAGES["requirements.html"]["sections"]:
        if block.get("type") == "callout" and "Internal-only instructions" in block.get("html", ""):
            block["html"] = "The register lists the repair requirements and their current verification status. See <a href=\"flagged.html\">Flagged for Review</a> for unresolved items."
    for page in ("index.html", "estimates.html", "brief.html"):
        for block in c.PAGES[page]["sections"]:
            if block.get("type") == "callout" and ("Brief transcription table" in block.get("html", "") or "three amounts above" in block.get("html", "")):
                block["html"] = (
                    "<strong>Unconfirmed values remain blank.</strong> The figures in the owner-reported prose are "
                    "not confirmed quotes or comparable all-in totals; scope, drywall inclusion and current price "
                    "remain open. See <a href=\"flagged.html\">Flagged for Review</a>."
                )

    c.TABLES["safety_followup_1111"] = {
        "title": "Occupied-unit and ceiling precautions — verify before opening",
        "columns": ["Question", "Confirmed property-specific answer", "Official guidance and next step", "Source"],
        "rows": [
            {"cells": ["Is the ceiling required for fire protection?", blank,
                       "SF's wallboard listing excludes work required for fire protection. Ask the building manager, contractor and SF DBI to establish the existing assembly and an appropriate repair before cutting."], "src": ["S02"]},
            {"cells": ["Could painted surfaces trigger lead-safe requirements?", blank,
                       "EPA describes requirements for covered paid renovations disturbing paint in pre-1978 housing. Determine building age, surfaces, exceptions and applicable certification; no lead condition is assumed."], "src": ["S500"]},
            {"cells": ["Could materials contain asbestos?", blank,
                       "EPA advises leaving suspected material undisturbed and involving trained, accredited professionals when disturbance is possible. No asbestos is diagnosed here."], "src": ["S501"]},
            {"cells": ["How should tenant and storage access be arranged?", blank,
                       "The Rent Board describes generally at least 24-hour written notice for covered entry, six days if mailed, and exceptions or consent. Confirm the rule and access arrangements for the particular spaces."], "src": ["S502"]},
        ],
        "caption": "The official sources describe general rules or precautions, not this property's age, materials, fire rating, legal access or actual work. Confirm applicability with the relevant authority and qualified provider.",
    }
    c.PAGES["decision-checklist.html"]["sections"].insert(2, {"type": "table", "ref": "safety_followup_1111"})
    c.PAGES["summary.html"]["sections"].insert(1, {
        "type": "callout", "tone": "warn", "html": (
            "<strong>Before any ceiling opening:</strong> the fire-protection status, building age and materials are unknown. "
            "Review the official <a href=\"decision-checklist.html\">occupant and ceiling precautions</a>; "
            "ask the contractor and relevant authorities about the exact scope and tenant access."
        ),
    })

    extra_flags = [
        ("Ceiling fire-protection status and wallboard repair", "SF's wallboard listing contains an exception for work required for fire protection; this ceiling's assembly is unknown.", "Identify the existing assembly and confirm the restoration and any applicable approvals before opening.", ["S02"]),
        ("Building age, paint and possible asbestos", "No property-specific material or lead assessment was supplied; official guidance describes conditional precautions, not a diagnosis.", "Determine building age and the proposed disturbance; use appropriate qualified assessors if needed.", ["S500", "S501"]),
        ("Tenant and storage access", "The relevant access arrangements and applicability of entry-notice rules to these spaces are unknown.", "Confirm notice, consent where applicable, access windows, contents protection and responsible contact.", ["S502"]),
        ("Legacy project-specific technical and scope conclusions", "Earlier published pages inferred drywall exclusions, exact concealed parts or access outcomes without inspection or complete written quotes.", "Use the corrected current dashboard; obtain written bids and a qualified on-site assessment before authorizing work.", ["S02", "S14", "S44"]),
    ]
    existing = [int(str(row["cells"][0])[1:]) for row in c.TABLES["flagged"]["rows"]
                if re.fullmatch(r"U\d+", str(row["cells"][0]))]
    next_flag = max(existing, default=0) + 1
    for item, why, action, src in extra_flags:
        fid = "U%d" % next_flag
        next_flag += 1
        c.TABLES["flagged"]["rows"].append({"cells": [fid, item, why, action, c.UNVERIFIED], "src": src})
    import session_1012_verification
    session_1012_verification._normalise_flags(c)
    c.META["updated"] = "2026-11-11"
    c.META["session"] = "arena/87bf58c3-korea7"
