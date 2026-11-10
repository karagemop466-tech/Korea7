"""Integrate the one verified candidate lead that never reached `main`.

Owner: arena/860ca261-korea7. Additive only.

Why this module exists
----------------------
PR #62 (`arena/dc6a8da6-korea7`, still open) carried a candidate the merged
dashboard never picked up: CSLB #946657. It matters for this job because it is
the only firm in the repository with an independent review describing exactly
the fallback this project faces - ceiling/drywall work below a bathroom in a
tenant-occupied San Francisco building - on top of a plumbing licence.

Everything published here was re-read from the issuing source during this
session (2026-11-10). The candidate is deliberately NOT inserted into the
scored ranking: the ranking model in `ranking_data.py` scores fixed licence
fields, and this record does not carry the B or C-9 classification that model
rewards. Publishing a hand-inserted higher score would break the model's
reproducibility. It is published instead as an evidence-fit lead with its
limitations stated, so the owner can weigh it.

The marketing entity and the licensed entity are different names (LLC versus
Inc). That gap is not resolved here and is flagged.
"""

S_CSLB946 = "S169"
S_ANGI946 = "S170"
S_SITE946 = "S171"
S_BPC7059_REF = "S163"   # already registered by reverify_b (BPC §7059)

SOURCES = {
    S_CSLB946: {
        "label": "CSLB #946657 — SUGAR BEAR PLUMBING INC (read 2026-11-10)",
        "publisher": "California Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/"
               "LicenseDetail.aspx?LicNum=946657",
        "tier": "official", "status": "verified", "checked": "2026-11-10",
        "supports": "Corporation, issued 2010-05-03, expires 2028-05-31, current and "
                    "active; C36, A, C20, C10; 317 Corey Way, South San Francisco "
                    "94080; (650) 583-3399; $25,000 contractor's bond effective "
                    "2026-09-01 (American Contractors Indemnity); workers' comp "
                    "Employers Assurance Company 2026-07-27 to 2027-07-27.",
        "note": "Page printed “Data current as of 11/9/2026”. No B (General Building) "
                "and no C-9 (Drywall) classification appears on this record.",
    },
    S_ANGI946: {
        "label": "Angi — Sugar Bear Plumbing, Inc. profile (read 2026-11-10)",
        "publisher": "Angi Inc.",
        "url": "https://www.angi.com/companylist/us/ca/south-san-francisco/"
               "sugar-bear-plumbing-inc-reviews-53506127.htm",
        "tier": "platform", "status": "verified", "checked": "2026-11-10",
        "supports": "Profile states “Trade License Number 946657”, “Trade License "
                    "Expiration 05/31/2028” and an overall rating of 4.6 from 60 "
                    "reviews. A July 2026 verified review describes new pipe run "
                    "inside walls with the walls then patched.",
        "note": "Third-party customer statements, not official findings. Angi states "
                "licence and insurance information is self-reported. The older 2018 "
                "tenant-occupied ceiling review cited in PR #62 is not among the 25 "
                "reviews rendered on 2026-11-10 and is therefore NOT republished here.",
    },
    S_SITE946: {
        "label": "Sugar Bear Home Services, LLC — company site (read 2026-11-10)",
        "publisher": "Sugar Bear Home Services, LLC",
        "url": "https://www.sugarbearhomeservices.com/",
        "tier": "company", "status": "verified", "checked": "2026-11-10",
        "supports": "Publishes (650) 618-9680 and advertises residential and commercial "
                    "plumbing, electrical and HVAC in San Francisco and the Bay Area, "
                    "with 24/7 emergency service.",
        "note": "The name on the site is the LLC; the CSLB record is the Inc. No CSLB "
                "number was displayed on the homepage, and no drywall service is "
                "advertised. The entity match is unverified.",
    },
}


def integrate(c):
    for sid, src in SOURCES.items():
        c.SOURCES[sid] = dict(src)

    c.TABLES["candidate_946"] = {
        "title": "Additional candidate — CSLB #946657, re-read 2026-11-10",
        "caption": "Published as an evidence-fit lead, not as a ranking score. Every "
                   "official field below was read from the CSLB record during this "
                   "session. Review-platform statements are customer statements and are "
                   "never treated as official findings.",
        "columns": ["Item", "Value", "Official or third-party verification",
                    "Why it matters for this job", "Source"],
        "rows": [
            {"cells": [
                "Licence and status",
                "CSLB #946657 — SUGAR BEAR PLUMBING INC, Corporation, current and active, "
                "expires 2028-05-31",
                "Official CSLB record (printed “Data current as of 11/9/2026”)",
                "An active licence is the minimum the owner asked for; it says nothing "
                "about this repair.",
            ], "src": [S_CSLB946]},
            {"cells": [
                "Classifications",
                "C36 Plumbing · A General Engineering · C20 Warm-Air HVAC · C10 Electrical",
                "Official CSLB record",
                "Plumbing is covered. There is no B (General Building) and no C-9 "
                "(Drywall) classification, so a drywall trade is not licensed on this "
                "record; patching would rest on §7059 “incidental and supplemental” or a "
                "subcontractor.",
            ], "src": [S_CSLB946, S_BPC7059_REF]},
            {"cells": [
                "Business address and phone on record",
                "317 Corey Way, South San Francisco 94080 · (650) 583-3399",
                "Official CSLB record",
                "South San Francisco base; San Francisco service is advertised by the "
                "company site but the record does not state a service area.",
            ], "src": [S_CSLB946]},
            {"cells": [
                "Bond and workers' compensation",
                "$25,000 contractor's bond effective 2026-09-01 · workers' comp "
                "Employers Assurance Company, 2026-07-27 to 2027-07-27",
                "Official CSLB record",
                "Workers' comp on file matters when trades will be inside an occupied "
                "unit.",
            ], "src": [S_CSLB946]},
            {"cells": [
                "Company-published contact and trades",
                "(650) 618-9680 · plumbing, electrical and HVAC; San Francisco and Bay "
                "Area; 24/7 emergency service",
                "Company site (self-published)",
                "A second published line, different from the CSLB number. It is a "
                "marketing page and proves nothing about this repair.",
            ], "src": [S_SITE946]},
            {"cells": [
                "Review record relevant to the fallback",
                "4.6 from 60 reviews on Angi; the profile carries licence 946657 and a "
                "July 2026 verified review describing pipe run inside walls with the "
                "walls then patched",
                "Angi profile (third-party customer statements; Angi says licence and "
                "insurance details are self-reported)",
                "Wall patching after concealed plumbing is the closest documented "
                "analogue in this repository to the ceiling-opening fallback. It is one "
                "customer's account, not a capability finding.",
            ], "src": [S_ANGI946]},
            {"cells": [
                "All-in price for this job",
                c.BLANK + " " + c.UNVERIFIED,
                "No official or first-party source publishes a price for this scope",
                "No figure is inferred. The three owner-provided amounts are not "
                "comparable with this firm's work.",
            ], "src": [S_CSLB946, S_SITE946]},
            {"cells": [
                "Entity match between the licensed corporation and the marketing LLC",
                c.BLANK + " " + c.UNVERIFIED,
                "The CSLB record names the Inc; the company site names the LLC and shows "
                "no licence number",
                "Before hiring, confirm in writing which legal entity will contract and "
                "that it holds #946657.",
            ], "src": [S_CSLB946, S_SITE946]},
        ],
    }

    c.TABLES["flagged"]["rows"].append({
        "cells": [
            "U50",
            "CSLB #946657 lead — carried over from unmerged PR #62, not scored",
            "The candidate was read from the official CSLB record and its Angi profile "
            "on 2026-11-10 and the licence fields match what PR #62 published. It is "
            "not inserted into the scored ranking because the scoring model rewards B "
            "and C-9 classifications that this record does not carry, and hand-editing "
            "a score would break the model's reproducibility. Unresolved: the licensed "
            "corporation and the marketing LLC have different names; no drywall trade "
            "is licensed on the record; the Angi reviews are customer statements; the "
            "2018 tenant-occupied ceiling review cited in PR #62 was not among the "
            "reviews rendered on 2026-11-10, so it is not republished.",
            "Ask the firm in writing which entity contracts, whether it will take the "
            "ceiling opening and its patch under one contract, and for the name and "
            "licence of any drywall subcontractor.",
            c.UNVERIFIED,
        ],
        "src": [S_CSLB946, S_ANGI946, S_SITE946],
    })

    c.PAGES["candidates.html"] = {
        "title": "Additional candidate lead",
        "eyebrow": "Evidence-fit supplement · read 2026-11-10",
        "h1": "A lead worth a call: CSLB #946657",
        "lede": "One firm in this repository has an independent review describing the "
                "fallback this job may need — plumbing behind a wall, then the wall "
                "patched — on top of a live plumbing licence. It is published here with "
                "its gaps intact, and it is deliberately not folded into the score.",
        "sections": [
            {"type": "callout", "tone": "info",
             "html": "<strong>Why this firm is on its own page.</strong> The "
                     "<a href=\"ranking.html\">ranked hiring decision</a> scores fixed "
                     "licence fields. Adding a hand-set score here would break that "
                     "model, so this candidate is presented as an evidence fit instead: "
                     "read the licence facts, read the review evidence, and treat the "
                     "rest as questions to ask."},
            {"type": "table", "title": "Official fields and evidence",
             "ref": "candidate_946"},
            {"type": "prose", "title": "How to weigh it against the top of the ranking",
             "html": "<p>Compared on licensing alone, this record is narrower than the "
                     "leaders: it carries C-36 with A, C-20 and C-10, but no B or C-9, "
                     "whereas the top-ranked <a href=\"ranking.html\">Ace Plumbing &amp; "
                     "Rooter</a> holds B alongside C-36 and the second-ranked Genteel "
                     "record holds B with C-36. On documented evidence of the actual "
                     "fallback — concealed plumbing followed by wall repair — this is "
                     "the only firm here with a verifiable published account of it.</p>"
                     "<p>The two measures answer different questions. The score answers "
                     "“which licence best matches a plumbing-plus-drywall job?” The "
                     "review evidence answers “has anyone described this firm doing "
                     "something like this?” Neither answers “can they free a seized "
                     "trip lever without breaking the assembly?” Only a site visit and a "
                     "written scope can answer that.</p>"},
            {"type": "prose", "title": "Limits, stated plainly",
             "html": "<ul>"
                     "<li>The licensed corporation is <em>Sugar Bear Plumbing Inc</em>; "
                     "the website is <em>Sugar Bear Home Services, LLC</em>. Which "
                     "entity would contract is unconfirmed.</li>"
                     "<li>No drywall trade is licensed on the CSLB record. A patch "
                     "would depend on §7059 “incidental and supplemental” or a licensed "
                     "subcontractor. No determination is made here — see "
                     "<a href=\"permits.html\">Permits &amp; licensing</a>.</li>"
                     "<li>The review evidence is a customer's account on a platform "
                     "that says licence details are self-reported. It is not an "
                     "inspection and not a capability finding.</li>"
                     "<li>No price for this scope is published anywhere, so the price "
                     "cell is blank and flagged.</li>"
                     "<li>No one has been contacted. Availability, willingness to work "
                     "in an occupied unit on this scope, and drywall inclusion are all "
                     "unconfirmed.</li></ul>"},
            {"type": "prose", "title": "Provenance",
             "html": "<p>This candidate was first published in an open pull request "
                     "(#62) whose dashboard was never merged. The licence, the Angi "
                     "profile and the company site were all re-read directly on "
                     "2026-11-10 before anything was republished, and one claim from "
                     "that pull request was dropped: the 2018 tenant-occupied ceiling "
                     "review is no longer rendered on the Angi profile, so it is not "
                     "restated here as if it had been re-seen. See "
                     "<a href=\"flagged.html\">U50</a>.</p>"},
        ],
    }
    for group in c.NAV:
        if group["group"] == "Decision":
            group["links"].append(("candidates.html", "Additional candidate lead"))
            break
