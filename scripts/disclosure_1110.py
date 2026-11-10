"""2026-11-10 complaint-disclosure audit — every ranked licence, read directly.

Why this module exists
----------------------
Before this module the site cited the CSLB complaint-disclosure page for one
licence (#1003394) and reproduced only its citation number, date and status.
It never read the disclosure page for the other fifteen licences, and it never
read CSLB's Citation Violation Disclosure page, which prints the individual
violation codes. The published ranking tells the owner to "read it before
hiring" without saying what is on it.

What was done on 2026-11-10
---------------------------
Each of the sixteen licence numbers published in this project's ranking was
looked up on the official CSLB complaint-disclosure page and read directly.
Fifteen pages print only the licence number and contractor name with no
Citations table; one (#1003394, Handyman Heroes Inc) publishes citation
2 2020 001045 dated 07/12/2020 with status "FOR DISCLOSURE ONLY PER B&P CODE
7124.6", and its Citation Violation Disclosure page lists 34 violation entries.

Nothing here is inferred or scored differently: the ranking rubric's disclosure
input ("Complaint disclosure present = 5 of 15") already accounts for the
existence of a disclosure, so the computed order does not change. The verified
detail is published so the owner can weigh it before calling.

Sources: S155 (CSLB Citation Violation Disclosure #1003394), S156 (this
session's machine-readable audit of all sixteen disclosure reads),
plus each licence's existing License Detail source and S12 (the complaint
disclosure page for #1003394, read again on 2026-11-10).
"""
from __future__ import annotations

import html
import re

import ranking_data as R

CHECKED = "2026-11-10"
ARTIFACT = "data/canonical/complaint-disclosures-2026-11-10.json"

CITATION_URL = (
    "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CitationViolationDisclosure.aspx"
    "?LicType=LIC&LicNum=1003394&LmfPre=&Class=2&FiscalYear=2020&SeqNbr=1045&ActionCde=K"
    "&Status=FOR+DISCLOSURE+ONLY+PER+B%26P+CODE+7124.6&LicName=HANDYMAN+HEROES+INC"
    "&StatusDt=07/12/2020"
)

# Order follows the published Route 1 / Route 2 ranking, then the remaining records.
RECORDS = [
    ("829071", "ACE PLUMBING & ROOTER", None),
    ("1025814", "GENTEEL PLUMBERS INC THE", None),
    ("1003394", "HANDYMAN HEROES INC", "citation"),
    ("959843", "GENERALSF", None),
    ("841229", "MANNY'S PLUMBING & ROOTER", None),
    ("1115649", "RAPID FLOW PLUMBING & ROOTER INC", None),
    ("868994", "ATLAS PLUMBING & ROOTER", None),
    ("977638", "EXPERT PLUMBING SOLUTIONS", None),
    ("1089561", "HEISES PLUMBING", None),
    ("1024971", "FAST RESPONSE PLUMBING AND ROOTER", None),
    ("757796", "BAY AREA PLUMBING", None),
    ("632743", "CALPLUMBING CO", None),
    ("1075566", "BAY AREA MECHANICAL", None),
    ("1140843", "DISCOUNT PLUMBING ROOTER SERVICES LLC", None),
    ("1009195", "ADVANCED PLUMBING AND DRAIN INC", None),
    ("995163", "BERNAL HILL DRYWALL INC", None),
]

# Verbatim from CSLB's Citation Violation Disclosure page, read 2026-11-10.
VIOLATIONS = [
    ("7109.A", "Departed from trade standards"),
    ("7113", "Exceeded contract amount"),
    ("7154.D", "Employed non-registered salesperson"),
    ("7159", "Violated provisions of the home improvement contract"),
    ("7159.C4", "No unconditional lien release provided as work progresses"),
    ("7159.C5", "Change order not incorporated in the contract"),
    ("7159.C6", "No notice re: obtaining a performance and pymnt bond"),
    ("7159.D2", "No name or registration no. of salesperson"),
    ("7159.D3", "No home improvement label on the contract"),
    ("7159.D4", "Notice that docs are to be complete before work is started"),
    ("7159.D7", "No description of project, materials or equip to be used"),
    ("7159.D8A", "No heading for a down payment"),
    ("7159.D8C", "No statement about excessive down payment."),
    ("7159.D9A", "No payment schedule heading"),
    ("7159.D10A", "No notice describing substantial commencement of work"),
    ("7159.D10B", "No approximate start date heading"),
    ("7159.D10C", "No date as to the beginning of work"),
    ("7159.D11A", "No approximate completion date heading"),
    ("7159.D11B", "No approximate completion date"),
    ("7159.D12", "No heading re: list of documents being part of the contract"),
    ("7159.D13", "No notice as to the impact of work and change orders"),
    ("7159.E1", "No notice regarding general liability insurance"),
    ("7159.E1B", "No notice re: name & phone of liability insurance carrier"),
    ("7159.E1C", "No notice re: contractor is self insured w/liability ins."),
    ("7159.E2A", "No notice as to not having employees and exemption from WC"),
    ("7159.E2B", "No notice as to the name of the Work Comp carrier"),
    ("7159.E3A", "No notice RE: addtnl/changes in writing prior to work begin"),
    ("7159.E3B", "No ntc: un-enforceability of chnge orders not complying"),
    ("7159.E3C", "No notice as to limitation of unjust enrichment"),
    ("7159.E4", "No heading or notice as to the mechanic's lien"),
    ("7159.E5", "No notice regarding the CSLB"),
    ("7159.E6A", 'HIC No notice title "three" or "five" "Day Right to Cancel"'),
    ("7159.E6B", "HIC No three day right to cancel language"),
    ("7159.5A3", "Exceeded down pymnt of $1000 or 10% whichever is least"),
]

NEW_SOURCES = {
    "S155": {
        "label": "CSLB — Citation Violation Disclosure, license #1003394",
        "publisher": "Contractors State License Board",
        "url": CITATION_URL,
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": ("Citation 2 2020 1045 dated 07/12/2020 (status 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6') "
                     "and its 34 violation entries, including B&P 7109.A 'Departed from trade standards', "
                     "7113 'Exceeded contract amount' and 7154.D 'Employed non-registered salesperson'"),
        "note": ("Read directly on cslb.ca.gov, 2026-11-10. Violation codes and descriptions are transcribed "
                 "verbatim; no interpretation of the outcome is offered. The page prints no 'Data current as of' "
                 "timestamp."),
    },
    "S156": {
        "label": "Complaint-disclosure audit of all sixteen licences (JSON)",
        "publisher": "This repository — direct CSLB reads, 2026-11-10",
        "url": ARTIFACT,
        "tier": "primary",
        "status": "verified",
        "checked": CHECKED,
        "supports": ("Per-licence result of reading CSLB's complaint-disclosure page for all sixteen published "
                     "licence numbers: fifteen with no citation disclosure, one (#1003394) with citation "
                     "2 2020 001045"),
        "note": ("Session record written 2026-11-10. It records the disclosure-page result only; the official "
                 "pages themselves are the authority and are linked from each row."),
    },
}


def _rows_table():
    rows = []
    for lic, name, citation in RECORDS:
        sid = R.LICENSE_SRC[lic]
        licence_cell = "%s<br><small>%s</small>" % (html.escape(name), "CSLB record linked in Source column")
        if citation:
            result = (pill_text("citation published", "warn") +
                      "<br><small>Disclosure page lists one citation; the violations are transcribed in the "
                      "next table.</small>")
            cited = ("Citation <strong>2 2020 001045</strong><br><small>07/12/2020<br>"
                     "FOR DISCLOSURE ONLY PER B&amp;P CODE 7124.6</small>")
            src = [sid, "S12", "S155", "S156"]
        else:
            result = (pill_text("no citation disclosure published", "ok") +
                      "<br><small>The page prints the licence number and contractor name only — no Citations "
                      "table.</small>")
            cited = "None published"
            src = [sid, "S156"]
        rows.append({"cells": [licence_cell, result, cited], "src": src})
    return rows


def pill_text(text, tone="info"):
    return '<span class="pill %s">%s</span>' % (tone, html.escape(text))


def link(sid, label=None):
    s = NEW_SOURCES.get(sid) or R.SOURCES.get(sid)
    if s is None:
        # Fall back to the shared ledger populated by dashboard_content.
        import dashboard_content as _c
        s = _c.SOURCES[sid]
    text = html.escape(label or s["label"])
    if s["url"].startswith("http"):
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (html.escape(s["url"]), text)
    return '<a href="%s">%s</a>' % (html.escape(s["url"]), text)


def licence_link(lic, label=None):
    import dashboard_content as _c
    sid = R.LICENSE_SRC[lic]
    s = _c.SOURCES[sid]
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (
        html.escape(s["url"]), html.escape(label or ("#" + lic)))


def integrate(c):
    c.SOURCES.update(NEW_SOURCES)

    # --- Table 1: the disclosure read for every published licence -----------
    c.TABLES["disclosure_check"] = {
        "title": "CSLB complaint-disclosure check — all 16 published licences, read 2026-11-10",
        "columns": ["Licence", "Result of the official complaint-disclosure page",
                    "Citation, date and status as published", "Source"],
        "rows": _rows_table(),
        "caption": (
            "Each row is one licence number from this project's ranking. The complaint-disclosure page for every "
            "number was fetched and read directly on <strong>2026-11-10</strong>; the full session record is in "
            + link("S156", "the audit JSON") + ". Fifteen pages print only the licence number and contractor name "
            "with no Citations table; one publishes a citation. The Source column links each licence's official "
            "CSLB License Detail page (which carries the complaint-disclosure notice) and the audit record. "
            "A disclosure is a CSLB record fact, not a finding about the quality of anyone's work."),
    }

    # --- Table 2: the citation detail, verbatim -----------------------------
    vrows = []
    for i, (code, description) in enumerate(VIOLATIONS, 1):
        vrows.append({
            "cells": [str(i), "<code>%s</code>" % html.escape(code), "Business &amp; Professions Code",
                      html.escape(description)],
            "src": ["S155", "S12"],
        })
    c.TABLES["citation_violations"] = {
        "title": "Citation 2 2020 001045 — violation entries as published by CSLB (34 entries)",
        "columns": ["#", "Violation code", "Code family (as published)", "Description as published", "Source"],
        "rows": vrows,
        "caption": (
            "Transcribed verbatim from CSLB's Citation Violation Disclosure page for licence #1003394, read "
            "<strong>2026-11-10</strong> (" + link("S155", "S155") + "). The disclosure page prints the citation "
            "number, the date 07/12/2020 and the status “FOR DISCLOSURE ONLY PER B&amp;P CODE 7124.6”. CSLB states "
            "on every licence record that complaint disclosure is restricted by law (B&amp;P §7124.6); this table "
            "reproduces the printed codes and descriptions and adds no interpretation, no penalty amount and no "
            "finding about the outcome. Weight it with the ranking rubric's disclosure input (complaint disclosure "
            "present = 5 of 15), which is unchanged."),
    }

    # --- Ranking page: publish the audit next to the decision ---------------
    rank_sections = c.PAGES["ranking.html"]["sections"]
    insert_at = len(rank_sections) - 1 if rank_sections and rank_sections[-1]["type"] == "callout" else len(rank_sections)
    rank_sections[insert_at:insert_at] = [
        {"type": "prose", "title": "Complaint-disclosure audit (2026-11-10)", "html": (
            "<p>CSLB tells consumers to review complaint disclosure before hiring, and this site previously told "
            "the owner to “read it before hiring” while publishing only the citation number. On "
            "<strong>2026-11-10</strong> the official complaint-disclosure page for <strong>all sixteen</strong> "
            "published licence numbers was read directly (" + link("S156", "audit record") + "). "
            "<strong>Fifteen publish no citation disclosure.</strong> One — <strong>#1003394 Handyman Heroes "
            "Inc</strong>, ranked #3 on the all-in-one route — publishes citation <strong>2 2020 001045</strong> "
            "dated <strong>07/12/2020</strong>, status “FOR DISCLOSURE ONLY PER B&amp;P CODE 7124.6”, with "
            "<strong>34 violation entries</strong> on CSLB's Citation Violation Disclosure page "
            "(" + link("S155", "official detail") + "), among them B&amp;P 7109.A “Departed from trade standards”, "
            "7113 “Exceeded contract amount” and 7154.D “Employed non-registered salesperson”.</p>"
            "<p><strong>Effect on the ranking: none.</strong> The rubric's disclosure input already scores a "
            "complaint disclosure at 5 of 15, so the computed order is unchanged. The detail is published because "
            "it is material to <em>how</em> the owner should contract with that firm — written contract with the "
            "statutory notices, a payment schedule and unconditional lien releases — and it is a reason to ask "
            "the question before booking rather than after. The other fifteen candidates have no published "
            "citation disclosure; that is not a statement about the quality of their work, availability or "
            "price.</p>")},
        {"type": "table", "ref": "disclosure_check"},
        {"type": "table", "ref": "citation_violations"},
    ]

    # --- Ranking rationale for #3: append the verified detail ---------------
    for row in c.TABLES["rank_allinone"]["rows"]:
        company = " ".join(row["cells"])
        if "Handyman Heroes" in company:
            why = row["cells"][4]
            addition = (
                " On 2026-11-10 the page behind that disclosure was read in full: CSLB publishes 34 "
                "violation entries on that citation, including B&amp;P 7109.A “departed "
                "from trade standards” and 7113 “exceeded contract amount” (the 34 entries are transcribed "
                "verbatim in the complaint-disclosure audit below, and the official page is linked in the "
                "Source column as S155). The rubric input is unchanged; treat the written contract, payment "
                "schedule and lien releases as the condition of using this firm.")
            if "34 violation entries" not in why:
                row["cells"][4] = why + addition
            for sid in ("S12", "S155", "S156"):
                if sid not in row["src"]:
                    row["src"].append(sid)
            row["cells"][2] = row["cells"][2].replace(
                "complaint disclosure</span>",
                "complaint disclosure</span><br><small>34 citation entries — see the audit below</small>")
            break

    # --- Call order: add the question to ask -------------------------------
    call_rows = c.TABLES["call_order"]["rows"]
    already = any("2 2020 001045" in " ".join(r["cells"]) for r in call_rows)
    if not already:
        call_rows.insert(3, {"cells": [
            "3 — ask before booking",
            "Handyman Heroes Inc (only if #3 remains a finalist)",
            "(844) 382-4376",
            "Ask the firm to explain CSLB citation 2 2020 001045 (07/12/2020) and what changed in its contracting "
            "practice; then require a written contract with the statutory notices, a payment schedule, and "
            "unconditional lien releases as work progresses.",
            "CSLB's citation disclosure for #1003394 lists 34 violation entries, including B&amp;P 7109.A "
            "“Departed from trade standards”, 7113 “Exceeded contract amount” and 7159 home-improvement-contract "
            "notice failures. The rubric score is unchanged; the contract terms are the safeguard.",
        ], "src": ["S10", "S12", "S155", "S156"]})

    # --- Findings -----------------------------------------------------------
    c.TABLES["findings"]["rows"].append({
        "cells": [
            "F18",
            "Only one of the sixteen ranked licensees publishes a citation disclosure, and it has 34 entries",
            "CSLB complaint-disclosure pages for all sixteen licence numbers were read on 2026-11-10: fifteen "
            "publish none. " + link("S12", "#1003394") + " publishes citation 2 2020 001045 (07/12/2020) and its "
            + link("S155", "violation detail") + " lists 34 entries: B&amp;P 7109.A “Departed from trade "
            "standards”, 7113 “Exceeded contract amount”, 7154.D “Employed non-registered salesperson”, and 31 "
            "entries citing §7159 home-improvement-contract provisions. Recorded as verified detail; the rubric's "
            "disclosure score is unchanged. Counts here were computed from the transcribed list, not estimated.",
            pill_text("verified 2026-11-10", "ok"),
        ],
        "src": ["S12", "S155", "S156", "S10"],
    })

    # --- Flagged for review (adverse but verified — owner should weigh it) ---
    flag_ids = [int(r["cells"][0][1:]) for r in c.TABLES["flagged"]["rows"]
                if re.fullmatch(r"U\d+", str(r["cells"][0]))]
    next_id = max(flag_ids) + 1 if flag_ids else 1
    if not any(r["cells"][0] == "U%d" % next_id for r in c.TABLES["flagged"]["rows"]):
        c.TABLES["flagged"]["rows"].append({
            "cells": [
                "U%d" % next_id,
                "Ranked #3 candidate carries a 2020 CSLB citation with 34 violation entries",
                "This is verified, not unknown: CSLB publishes citation 2 2020 001045 (07/12/2020) for "
                "#1003394 Handyman Heroes Inc with 34 violation entries. It does not change the computed score "
                "(the rubric already deducts for a disclosure) but it is adverse information the owner should "
                "weigh before hiring that firm.",
                "Needs owner review before booking; ask the firm to explain the citation and contract in writing",
                pill_text("needs review", "warn"),
            ],
            "src": ["S10", "S12", "S155", "S156"],
        })

    # --- Verification page: record the audit --------------------------------
    c.PAGES["verification.html"]["sections"].insert(1, {
        "type": "prose",
        "title": "Complaint-disclosure audit — 2026-11-10",
        "html": (
            "<p>Session <code>arena/4c075a93-korea7</code> read the official complaint-disclosure page for every "
            "one of the <strong>sixteen</strong> licence numbers published in the ranking, and then read the "
            "Citation Violation Disclosure page behind the only citation found. Fifteen pages print no Citations "
            "table; #1003394 publishes citation 2 2020 001045 (07/12/2020, “FOR DISCLOSURE ONLY PER B&amp;P CODE "
            "7124.6”) with 34 violation entries (" + link("S155", "official detail") + "; "
            + link("S156", "session audit record") + "). The full transcription is published on "
            "<a href=\"ranking.html\">Ranked hiring decision</a>. No score, rank or value was changed by this "
            "audit; no provider was contacted.</p>"),
    })

    # --- Executive summary page --------------------------------------------
    summary_sections = c.PAGES["summary.html"]["sections"]
    pos = len(summary_sections) - 1 if summary_sections and summary_sections[-1]["type"] == "callout" else len(summary_sections)
    summary_sections.insert(pos, {
        "type": "prose",
        "title": "7. Complaint-disclosure check on the candidates (2026-11-10)",
        "html": (
            "<p>CSLB advises consumers to read complaint disclosure before hiring. All sixteen published licence "
            "numbers were checked on the official disclosure page on <strong>2026-11-10</strong>: fifteen publish "
            "no citation, and <strong>#1003394 Handyman Heroes Inc</strong> — third on the all-in-one route — "
            "publishes citation 2 2020 001045 (07/12/2020) with 34 violation entries, including “Departed from "
            "trade standards” and “Exceeded contract amount” (" + link("S155", "official detail") + "; "
            + link("S156", "audit record") + "). The ranking is unchanged because the rubric already deducts for "
            "a disclosure; if that firm is used, require the written contract, payment schedule and lien releases. "
            "Full tables: <a href=\"ranking.html\">Ranked hiring decision</a>.</p>"),
    })

    # --- Dashboard callout: point at the new audit -------------------------
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "callout" and "2026-11-10 re-check" in block.get("html", ""):
            if "Complaint-disclosure audit" not in block["html"]:
                block["html"] = block["html"].rstrip() + (
                    " <strong>Complaint-disclosure audit:</strong> the official disclosure page for all sixteen "
                    "licence numbers was read on 2026-11-10; only #1003394 publishes a citation — see "
                    "<a href=\"ranking.html\">Ranked hiring decision</a>.")
            break

    # --- Repo/verification provenance --------------------------------------
    c.TABLES["repo_review"]["rows"].append({
        "cells": [
            "Complaint-disclosure audit 2026-11-10 (arena/4c075a93-korea7)",
            "Read CSLB's complaint-disclosure page for all sixteen published licence numbers, then the Citation "
            "Violation Disclosure page for the single citation found. Published the per-licence result and the "
            "34 violation entries verbatim, and added the question to the call order.",
            "16/16 disclosure pages read; 15 with no citation, 1 with citation 2 2020 001045 (34 entries). "
            "Desk verification only — no provider was contacted, and a disclosure record does not establish job "
            "capability, availability or price.",
            pill_text("reviewed 2026-11-10", "ok"),
        ],
        "src": ["S12", "S155", "S156", "S45"],
    })

    # --- Re-run the shared normalisation so flag IDs/counts stay correct ---
    flag_ids = [r["cells"][0] for r in c.TABLES["flagged"]["rows"]
                if re.fullmatch(r"U\d+", str(r["cells"][0]))]
    max_flag = max(int(f[1:]) for f in flag_ids)
    c.TABLES["flagged"]["rows"].sort(
        key=lambda r: (int(re.fullmatch(r"U(\d+)", str(r["cells"][0])).group(1))
                       if re.fullmatch(r"U\d+", str(r["cells"][0])) else 10 ** 6))
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
    c.META["updated"] = "2026-11-10"
    c.META["session"] = "arena/4c075a93-korea7"
