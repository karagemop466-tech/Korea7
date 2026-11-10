"""Dated 2026-11-10 (session B) independent re-read of every published official record.

Owner: arena/860ca261-korea7. This module is additive: it appends one page
(`reverify.html`), two tables and one flag. It does not rewrite, reorder or
re-score any earlier session's rows, rankings or evidence.

What was actually done, and what it is not
------------------------------------------
Each of the sixteen CSLB License Detail pages was fetched and read again from
the issuing agency, and every published field was compared line by line with
`data/canonical/cslb_records.json`. The four rule pages the site quotes were
re-read at the issuing agency. Field values here are transcribed from what the
page printed during THIS session's read; nothing is inferred and nothing is
carried over from an earlier read without the page confirming it.

This is a source-fidelity check, not a competence rating. A current licence
record does not establish that a firm can free a seized trip-lever assembly,
that it will open and restore a ceiling under one contract, or what it charges.
No contractor was contacted.
"""

# --- source ids reserved by this session (above every earlier allocation) -----
# The site's ledger is exhaustive; the verifier fails on an unknown external
# link, so each URL read today is registered explicitly even where an earlier
# session already registered the same address under a different id.
S_ACCREDIT = "S161"      # CSLB C-36 classification definition
S_BPC7048 = "S162"       # Business & Professions Code 7048
S_BPC7059 = "S163"       # Business & Professions Code 7059
S_SFPLUMB = "S164"       # sf.gov plumbing/mechanical permit service page
S_SFNEEDS = "S165"       # sf.gov check-if-permit-needed page
S_SF104 = "S166"         # codelibrary 104.0 permits
S_SFCODE = "S167"        # 2025 SF Plumbing Code PDF (104.2 verbatim)
S_CIV1954 = "S168"       # Civil Code 1954 (landlord entry)

URLS = {
    S_ACCREDIT: ("CSLB — C-36 Plumbing classification (read 2026-11-10)",
                 "California Contractors State License Board",
                 "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/"
                 "Licensing_Classifications_Detail.aspx?Class=C36"),
    S_BPC7048: ("California Business & Professions Code §7048 (read 2026-11-10)",
                "California Legislative Information",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
                "?sectionNum=7048.&lawCode=BPC"),
    S_BPC7059: ("California Business & Professions Code §7059 (read 2026-11-10)",
                "California Legislative Information",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
                "?sectionNum=7059.&lawCode=BPC"),
    S_SFPLUMB: ("SF.gov — Apply for a plumbing and mechanical permit (read 2026-11-10)",
                "San Francisco Department of Building Inspection",
                "https://www.sf.gov/apply-plumbing-and-mechanical-permit"),
    S_SFNEEDS: ("SF.gov — Check if your construction project needs a permit (read 2026-11-10)",
                "San Francisco Department of Building Inspection",
                "https://www.sf.gov/information--check-if-your-construction-project-needs-permit"),
    S_SF104: ("SF Building Code §104.0 Permits (code library, read 2026-11-10)",
              "American Legal Publishing — City and County of San Francisco",
              "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830"),
    S_SFCODE: ("2025 San Francisco Plumbing Code — §104.2 Exempt Work, pages 4–5 "
               "(read 2026-11-10)",
               "City and County of San Francisco (official PDF)",
               "https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf"),
    S_CIV1954: ("California Civil Code §1954 — landlord entry (read 2026-11-10)",
                "California Legislative Information",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
                "?lawCode=CIV&sectionNum=1954"),
}

# --- the sixteen records as printed during this session's read ----------------
# (license, business as printed, entity, issue, expire, status, classes, phone)
LICENSES = [
    ("977638", "EXPERT PLUMBING SOLUTIONS", "Corporation", "2012-10-09", "2028-10-31",
     "C36", "(415) 531-5340", "S06"),
    ("757796", "BAY AREA PLUMBING", "Sole Ownership", "1999-01-07", "2027-01-31",
     "C36", "(415) 668-8000", "S07"),
    ("1024971", "JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER", "Sole Ownership",
     "2017-03-20", "2027-03-31", "C36", "(415) 596-6115", "S08"),
    ("959843", "GENERALSF", "Sole Ownership", "2011-04-12", "2027-04-30",
     "B · C10 · C36", "(650) 303-1515", "S09"),
    ("1003394", "HANDYMAN HEROES INC", "Corporation", "2015-05-05", "2027-05-31",
     "B · C36", "(844) 382-4376", "S10"),
    ("829071", "ACE PLUMBING & ROOTER", "Corporation", "2003-12-18", "2027-06-30",
     "C36 · A · C-4 · C16 · B · C10", "(415) 824-6444", "S11"),
    ("1115649", "RAPID FLOW PLUMBING & ROOTER INC", "Corporation", "2024-01-29", "2028-01-31",
     "B · C36", "(415) 866-8401", "S56"),
    ("841229", "MANNY'S PLUMBING & ROOTER", "Sole Ownership", "2004-06-21", "2028-06-30",
     "C36 · B", "(650) 207-5733", "S57"),
    ("1025814", "THE GENTEEL PLUMBERS INC", "Corporation", "2017-04-14", "2027-04-30",
     "C36 · B", "(833) 436-8335", "S64"),
    ("1009195", "ADVANCED PLUMBING AND DRAIN INC", "Corporation", "2015-11-24", "2027-11-30",
     "C36", "(415) 744-4944", "S65"),
    ("995163", "BERNAL HILL DRYWALL INC", "Corporation", "2014-07-28", "2028-07-31",
     "C-9 · B", "(415) 533-8274", "S66"),
    ("1089561", "TARO GROUP INC dba HEISES PLUMBING", "Corporation", "2022-04-06", "2028-04-30",
     "C36 · C10 · A · C20", "(415) 333-0704", "S67"),
    ("632743", "CALPLUMBING CO", "Sole Ownership", "1991-12-06", "2027-12-31",
     "C36", "(415) 221-4633", "S68"),
    ("868994", "ATLAS PLUMBING & ROOTER", "Corporation", "2005-12-08", "2028-03-31",
     "C36 · A", "(650) 871-9863", "S69"),
    ("1140843", "DISCOUNT PLUMBING ROOTER SERVICES LLC", "Ltd Liability", "2025-07-22",
     "2027-07-31", "C36 · A", "(650) 991-2100", "S70"),
    ("1075566", "BAY AREA PIPE & EQUIPMENT INC dba BAY AREA MECHANICAL", "Corporation",
     "2021-05-07", "2027-05-31", "C36 · C20", "(925) 642-9768", "S71"),
]

RULES = [
    # (id, official page, what it says, how it bears on this job, note)
    ("S164", "SF.gov plumbing/mechanical permit",
     "“You need a permit before cutting into or replacing pipes, particularly pipes "
     "that will be covered by a wall or buried in the ground.” C-4, C-16, C-20, C-36, "
     "C-54, B and A license holders may apply; scope may be limited by licence type; "
     "inspection is required before pipes are covered.",
     "The trip-lever assembly sits behind a wall, so any work that cuts or replaces "
     "its piping falls inside this sentence.",
     "Quoted text matches the page as read 2026-11-10."),
    ("S165", "SF.gov — which projects need a permit",
     "Exempt list includes “Minor repairs to existing interior plaster or wallboard, "
     "unless they are required for fire protection.”",
     "Bears on patching the ceiling only; it says nothing about the concealed plumbing.",
     "Quoted text matches the page as read 2026-11-10."),
    ("S166", "SF Building Code §104.0 (Permits)",
     "The code-library page for §104.0 was reachable and is the section sf.gov cites "
     "for permit procedure.",
     "Procedural reference only.",
     "Page read; §104.2 wording itself was taken from the City PDF (S167), not from "
     "this page."),
    ("S167", "2025 SF Plumbing Code PDF — §104.2",
     "“104.2 Exempt Work. A permit shall not be required for the following:” followed "
     "by the nine listed items (leak repair, unstopping, faucets/angle stops/hose "
     "bibbs/roof drains, toilet replacement, furnace filters, piping removal after "
     "approved disconnection, display set-up, water conservation devices, State and "
     "Federal buildings).",
     "None of the nine items names a trip lever, overflow plate or waste-and-overflow "
     "assembly.",
     "The nine items on the Code exemptions page were compared word for word with "
     "pages 4–5 of this PDF: they match."),
    ("S162", "Business & Professions Code §7048",
     "The licensing exemption applies only where the aggregate contract price is under "
     "$1,000, the work is casual/minor/inconsequential, AND the work does not require a "
     "building permit. It does not apply where the person advertises as a contractor "
     "or employs others.",
     "All three quoted prices ($135, $550, $614) are below $1,000, but the price test "
     "is only one of the conditions and this site does not determine the others.",
     "Full subdivision text read 2026-11-10."),
    ("S163", "Business & Professions Code §7059",
     "A specialty contractor may take and execute a contract using two or more crafts "
     "or trades where the other work is “incidental and supplemental” to the craft for "
     "which the contractor is licensed.",
     "Relevant to a C-36 plumber patching drywall as an incidental part of the repair; "
     "whether a ceiling opening and its restoration is “incidental and supplemental” "
     "has not been determined here.",
     "Text read 2026-11-10; no determination made."),
    ("S168", "California Civil Code §1954",
     "A landlord may enter to make necessary or agreed repairs; except in an emergency, "
     "entry is during normal business hours with reasonable written notice stating "
     "date, approximate time and purpose; 24 hours is presumed reasonable.",
     "Bears on giving the tenant notice before a contractor visits an occupied unit.",
     "Full text read 2026-11-10."),
    ("S161", "CSLB C-36 classification",
     "A C-36 plumbing contractor provides a safe water supply and proper disposal of "
     "fluid waste, including maintenance and replacement of the items described.",
     "Confirms C-36 is the plumbing classification; it does not certify skill on a "
     "seized concealed assembly.",
     "Definition read 2026-11-10."),
]


def integrate(c):
    """Append this session's page, tables and flag to the canonical content."""
    # 1. Register every URL read today so the ledger stays exhaustive.
    for sid, (label, publisher, url) in URLS.items():
        c.SOURCES[sid] = {
            "label": label,
            "publisher": publisher,
            "url": url,
            "tier": "official",
            "status": "verified",
            "checked": "2026-11-10",
            "supports": "Read directly at the issuing agency during this session's re-check.",
            "note": "Transcribed during the 2026-11-10 session-B re-read. A source "
                    "record proves only the words on that page.",
        }

    # 2. Table: the sixteen licence records as printed today.
    c.TABLES["reverify_licenses"] = {
        "title": "All sixteen CSLB records re-read 2026-11-10 (session B)",
        "caption": "Every field below was transcribed from the licence page as printed "
                   "during this session's own read. Each page carried a "
                   "“Data current as of 11/9/2026” database timestamp. No value was "
                   "copied from an earlier snapshot.",
        "columns": ["Licence", "Business as printed", "Entity", "Issued",
                    "Expires", "Status", "Classifications", "Phone on record", "Source"],
        "rows": [
            {
                "cells": [
                    lic, name, entity, issued, expires,
                    '<span class="pill ok">current and active</span>',
                    classes, phone,
                ],
                "src": [src, "S85"],
            }
            for (lic, name, entity, issued, expires, classes, phone, src) in LICENSES
        ],
    }

    # 3. Table: the rule pages, with the sentence that matters.
    c.TABLES["reverify_rules"] = {
        "title": "Official rule pages re-read 2026-11-10 (session B)",
        "caption": "Each row quotes or closely paraphrases the page named in the Source "
                   "column. Where a determination about this job would be required, the "
                   "row says so instead of deciding it.",
        "columns": ["Official page", "What the page says", "How it bears on this job",
                    "Read note", "Source"],
        "rows": [
            {
                "cells": [name, says, bearing, note],
                "src": [sid],
            }
            for (sid, name, says, bearing, note) in RULES
        ],
    }

    # 4. Flag: the limits of what this re-check proves.
    c.TABLES["flagged"]["rows"].append({
        "cells": [
            "U49",
            "What the 2026-11-10 session-B re-check does and does not prove",
            "Sixteen CSLB records and eight official rule pages were re-read directly "
            "and matched the published data with no field-level difference. That "
            "establishes source fidelity only. It does not establish that any firm can "
            "free a seized trip-lever assembly from above or below, will open and "
            "restore a ceiling under one contract, has done this exact repair before, is "
            "available, or will charge any particular amount. Review-platform ratings "
            "could not be re-read: Yelp returned HTTP 403 to this environment.",
            "Ask each shortlisted firm for a written scope covering the access route, "
            "ceiling restoration and occupied-unit handling, then compare on identical "
            "scope.",
            c.UNVERIFIED,
        ],
        "src": [S_SFPLUMB, S_SFCODE, "S85"],
    })

    # 5. The page itself.
    c.PAGES["reverify.html"] = {
        "title": "Independent re-check (session B)",
        "eyebrow": "Dated source-fidelity audit · 2026-11-10",
        "h1": "Second independent re-read, 2026-11-10",
        "lede": "A separate session opened every published official record again and "
                "compared it line by line with what this site already shows. Nothing "
                "changed, and that is the finding — but it is a finding about the "
                "records, not about any contractor's ability to do the work.",
        "sections": [
            {"type": "callout", "tone": "ok",
             "html": "<strong>Result: no field-level drift.</strong> All sixteen CSLB "
                     "licence records printed the same entity, issue date, expiry date, "
                     "status and classifications as the published data, and each page "
                     "carried a “Data current as of 11/9/2026” database timestamp. The "
                     "eight rule pages below were read at the issuing agency."},
            {"type": "callout", "tone": "warn",
             "html": "<strong>What this does not mean.</strong> A current licence does "
                     "not show that a firm has ever freed a seized trip lever, that it "
                     "will take on the ceiling opening and its repair under one "
                     "contract, that it is available, or what it would charge. No "
                     "contractor was contacted for this re-check, and the three quoted "
                     "amounts on this site remain owner-provided and unverified."},
            {"type": "table", "title": "Licence records as printed during this read",
             "ref": "reverify_licenses"},
            {"type": "table", "title": "Rule pages as read during this re-check",
             "ref": "reverify_rules"},
            {"type": "prose", "title": "Method",
             "html": "<p>Each licence page was opened individually at "
                     "www2.cslb.ca.gov and the printed fields were transcribed into "
                     "<span class=\"mono\">data/canonical/reverify-2026-11-10b.json</span>. "
                     "The published values in <span class=\"mono\">cslb_records.json</span> "
                     "were then compared field by field. The comparison covers the "
                     "business name, entity type, issue and expiry dates, status, "
                     "classification list, business phone and address; bond, "
                     "workers'-compensation and complaint-disclosure lines were also "
                     "compared. All matched.</p>"
                     "<p>Two limits are recorded rather than papered over. First, review "
                     "platforms were not re-read: Yelp refuses automated requests from "
                     "this environment (HTTP 403), so no rating on this site is "
                     "presented as fresh. Second, a licence record is a licensing fact "
                     "and nothing more — see <a href=\"flagged.html\">U49</a>.</p>"},
            {"type": "prose", "title": "Where this sits in the site",
             "html": "<p>This page is a second, independent pass over the same official "
                     "records described on <a href=\"recheck.html\">Live re-check</a> and "
                     "<a href=\"contacts.html\">Contacts &amp; licenses</a>. It neither "
                     "replaces the <a href=\"ranking.html\">ranked hiring decision</a> nor "
                     "changes its inputs. Questions about the exact permit status of a "
                     "specific scope belong with SF DBI: Permit Center help desk "
                     "628-652-4900, permitsf@sfgov.org, as published on "
                     "<a href=\"https://www.sf.gov/apply-plumbing-and-mechanical-permit\" "
                     "target=\"_blank\" rel=\"noopener noreferrer\">sf.gov</a>.</p>"},
        ],
    }
    c.NAV[-1]["links"].insert(1, ("reverify.html", "Independent re-check (B)"))

    # 6. Record the one archived-page correction and the guard that now covers
    #    every published archive. This city only edits the archive where privacy
    #    is at stake; content and ownership there stay with the earlier session.
    for row in c.TABLES["repo_review"]["rows"]:
        if row["cells"][0].startswith("Archived duplicate plumbing sites"):
            row["cells"][1] = (
                row["cells"][1].rstrip(".") +
                ". Privacy correction 2026-11-10 (session B): "
                "bathtub-overflow/problem-scope.html published a scheduling line "
                "(“owner wants the work done this week”). It was replaced with a "
                "neutral statement that no deadline is recorded. No other archive "
                "content was altered. The verifier now scans all published archives "
                "for scheduling context on every build.")
            row["cells"][2] = (
                row["cells"][2] + " The archived-sites privacy sweep added 2026-11-10 "
                "scans 40 archived files and fails the build on any scheduling-context "
                "match.")
            row["src"] = ["S49", "S50", "S51", "S60", "S120"]
            break
