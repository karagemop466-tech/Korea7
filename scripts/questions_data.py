"""Questions, information & answers before decision (2026-11-11).

Adds the dedicated page the project brief asks for: a clear list of the
questions that must be addressed before any hiring decision can reasonably be
made, what is already known from verified sources, what is still missing, and
concrete suggestions for discovering the missing information.

Additive only: no existing row, score or page is rewritten. Every row cites
existing verified sources; owner-provided facts stay flagged UNVERIFIED and
no value is inferred. Permit content is neutral official reporting only.
"""
from __future__ import annotations


def integrate(c):
    pill = c.pill
    UNVERIFIED = c.UNVERIFIED

    c.TABLES["questions"] = {
        "title": "Open questions — what must be answered before a hiring decision",
        "columns": ["#", "Question", "What we know (verified)", "What is still missing", "How to discover it", "Status", "Source"],
        "rows": [
            {
                "cells": [
                    "Q01",
                    "Can the overflow be removed from above without damaging the hidden plumbing?",
                    "The from-above procedure is documented (remove overflow-plate screws, withdraw the upper linkage; cleaning/adjusting the link can free a stuck mechanism). The owner reports 5+ licensed plumbers declined from-above removal for this tub.",
                    "Whether this tub's seized assembly can be freed from above safely; the exact stuck point (linkage, stopper, or waste body).",
                    "Ask each shortlisted plumber for a cautious, non-forcing above-first assessment with a stated diagnostic fee and a written stop-and-price point before any opening. Do not force a seized linkage.",
                    UNVERIFIED + " " + pill("procedure documented; outcome unverified", "warn"),
                ],
                "src": ["S44", "S18", "S20", "S21"],
            },
            {
                "cells": [
                    "Q02",
                    "What exactly is stuck, and what parts will be needed?",
                    "A trip-lever bath waste-and-overflow assembly is a standard manufacturer product (Oatey Dearborn tubular trip-lever waste).",
                    "Photos, measurements, assembly material and part numbers for this tub; whether repair or full replacement is needed.",
                    "Supply reference photos of the overflow plate, lever and tub shoe; ask the assessing plumber to identify parts in writing before ordering.",
                    UNVERIFIED + " " + pill("component exists; this tub unverified", "warn"),
                ],
                "src": ["S44", "S14"],
            },
            {
                "cells": [
                    "Q03",
                    "Will the drywall ceiling from below need to be opened, and how large an opening?",
                    "SF.gov lists minor repairs to existing interior plaster or wallboard among work that does not need a building permit; the plumbing scope is governed by the plumbing-permit rule. The owner reports a storage unit below.",
                    "This tub's layout, the size of any ceiling opening, and whether patch, texture and paint are included in any quote.",
                    "Ask the contractor to state the opening size, patch/texture/paint finish and dust/contents protection in the written scope before authorizing any cut.",
                    UNVERIFIED + " " + pill("rules cited; layout unverified", "warn"),
                ],
                "src": ["S44", "S01", "S02"],
            },
            {
                "cells": [
                    "Q04",
                    "Who will do both the plumbing and the drywall under one contract?",
                    "Six licenses in the scored pool list both a building classification and C-36 Plumbing (Ace #829071, Genteel #1025814, Handyman Heroes #1003394, GENERALSF #959843, Rapid Flow #1115649, Manny's #841229). BPC §7059 allows specialty contractors incidental and supplemental work in other trades.",
                    "Whether any firm will actually perform the combined scope under one contract, and how the ceiling make-good is covered in writing.",
                    "Request one written scope naming the responsible trades for plumbing, ceiling cut, patch, texture and paint; or pair a plumbing-only firm with the verified C-9 restoration partner (Bernal Hill Drywall #995163).",
                    UNVERIFIED + " " + pill("licenses verified; execution unverified", "warn"),
                ],
                "src": ["S11", "S64", "S10", "S09", "S56", "S57", "S62", "S66"],
            },
            {
                "cells": [
                    "Q05",
                    "What is the total all-in price for this scope?",
                    "Three owner-reported estimates dated 2026-08-30 describe three different scopes (full waste-and-overflow replacement; lever/plug/spout with diverter; handle repair/adjustment). Independent 2026 benchmarks: drain replacement $500–$1,020 (avg $700); leak repair $150–$600 plus $300–$930 drywall/tile follow-up.",
                    "A single comparable all-in price covering the above-attempt, below access, ceiling restoration, testing and tenant coordination. No published price exists for this scope.",
                    "Ask each shortlisted firm for one fixed written price with inclusions/exclusions itemized. Compare only like-for-like written scopes; treat the three owner figures as different scopes, not competing all-in bids.",
                    UNVERIFIED + " " + pill("no verified price exists", "warn"),
                ],
                "src": ["S44", "S15", "S16"],
            },
            {
                "cells": [
                    "Q06",
                    "Is the chosen license current, active and correctly classified on the hire date?",
                    "All sixteen scored-pool CSLB records printed 'current and active' on their read dates (2026-11-07/08, re-read 2026-11-10). CSLB is the official lookup authority.",
                    "The hire-date status of the chosen license, bond and workers' compensation.",
                    "Re-check the license number on CSLB Check a License on the hire date and keep the printed record with the contract.",
                    pill("verified at read date; re-check required", "warn"),
                ],
                "src": ["S04", "S11", "S64", "S10"],
            },
            {
                "cells": [
                    "Q07",
                    "What do review platforms (Yelp and others) say about this specific work in San Francisco?",
                    "Yelp profiles/searches for the candidates were located as dated snapshots; direct Yelp fetching returned HTTP 403, so numeric ratings are not presented as verified. Review badges are not license verification.",
                    "Current ratings and job-specific reviews for concealed waste-and-overflow work in occupied units.",
                    "Open the linked Yelp/Angi/BuildZoom/Thumbtack/BBB pages manually on the decision date and read reviews for bathtub waste-and-overflow and occupied-unit work specifically.",
                    UNVERIFIED + " " + pill("snapshots only; open manually", "warn"),
                ],
                "src": ["S44", "S04"],
            },
            {
                "cells": [
                    "Q08",
                    "How will the tenant-occupied unit be protected and coordinated?",
                    "Two shortlisted firms publish HOA/property-manager experience (Ace; Fast Response). No official source confirms occupied-unit precautions for this job.",
                    "Access windows, dust/contents protection, water shut-off notice, and who coordinates with tenants.",
                    "Ask for the occupied-unit plan in writing: access windows, protection measures, shut-off notice and a single point of contact.",
                    UNVERIFIED + " " + pill("company statements only", "warn"),
                ],
                "src": ["S44", "S43", "S40"],
            },
            {
                "cells": [
                    "Q09",
                    "Which official requirements apply to the exact scope (plumbing, ceiling, licensing)?",
                    "SF.gov: a permit is needed before cutting into or replacing pipes, particularly pipes covered by a wall; minor interior plaster/wallboard repair is listed among work that does not need a building permit; plumbing-permit applicants must hold C-4, C-16, C-20, C-36, C-54, B or A. BPC §7048 sets the small-job licensing exemption at under $1,000 for casual/minor work that does not require a building permit.",
                    "The determination for this exact scope, which only SF DBI and the selected licensed contractor can make.",
                    "Confirm the final scope and applicable requirements with SF DBI (Permit Center help desk) and the selected licensed contractor before work begins. Nothing on this page is legal advice.",
                    pill("official rules cited; applicability to be confirmed", "warn"),
                ],
                "src": ["S01", "S02", "S13"],
            },
            {
                "cells": [
                    "Q10",
                    "What workers'-compensation and bond coverage will apply to the crew on site?",
                    "CSLB records show the bond and workers'-compensation fields for each licensee; five of the sixteen records carry a 'no employees' exemption and one policy expires 2026-12-18.",
                    "Current certificates covering the actual crew and dates of work.",
                    "Request a current certificate of insurance naming the job and dates; confirm in writing who will be on site and what coverage applies.",
                    pill("CSLB fields verified; current COI unverified", "warn"),
                ],
                "src": ["S04", "S07", "S08"],
            },
            {
                "cells": [
                    "Q11",
                    "Is there any complaint disclosure the hiring party should review?",
                    "CSLB publishes complaint disclosures per license; the audit read the disclosure page for all sixteen scored-pool licenses and found a published citation on #1003394 (2020, reported verbatim).",
                    "The hire-date disclosure status of the chosen license.",
                    "Open the CSLB complaint-disclosure page for the chosen license number and read it before signing.",
                    pill("audit read 2026-11-10; re-check required", "warn"),
                ],
                "src": ["S04", "S10", "S12"],
            },
            {
                "cells": [
                    "Q12",
                    "Will the firm service San Francisco and is it available?",
                    "CSLB addresses and company service claims are recorded for each candidate; exact address-level availability is not confirmed by any official source.",
                    "San Francisco service confirmation, earliest availability, and any travel charges.",
                    "Call the official phone on the Contacts page and confirm service area, availability and travel charges in writing.",
                    UNVERIFIED + " " + pill("service claims recorded; availability unverified", "warn"),
                ],
                "src": ["S04", "S43", "S40"],
            },
            {
                "cells": [
                    "Q13",
                    "What reference information (photos, measurements) is needed before quoting?",
                    "The owner noted reference pictures might be provided; none were supplied to the research sessions.",
                    "Photos of the overflow plate, lever, tub shoe and below-ceiling area; tub dimensions and access notes.",
                    "Photograph the overflow plate and lever, the tub shoe, and the storage-unit ceiling below; send them with the written scope request so quotes cover the same scope.",
                    UNVERIFIED + " " + pill("no photos on file", "warn"),
                ],
                "src": ["S44"],
            },
            {
                "cells": [
                    "Q14",
                    "What must be answered before any hiring decision is reasonable?",
                    "This page lists the questions; the Ranked hiring decision page orders the calls; the Flagged for Review page lists every unverified item.",
                    "Written answers to Q01–Q13 for the chosen firm: above-first assessment, below-access option, ceiling restoration, all-in price, license/COI re-check, occupied-unit plan, and applicable-requirements confirmation.",
                    "Do not sign until the chosen firm has answered in writing and the license has been re-checked on CSLB. Record the answers with the contract.",
                    UNVERIFIED + " " + pill("decision gate — not yet met", "warn"),
                ],
                "src": ["S44", "S04", "S01"],
            },
        ],
        "caption": "Each question is answered only to the extent a cited source supports. Owner-provided facts are flagged UNVERIFIED; official rules are cited for manual confirmation with SF DBI and the selected licensed contractor. Nothing here is legal advice.",
    }

    c.TABLES["answers"] = {
        "title": "Answers the official sources do give",
        "columns": ["#", "Question with an official answer", "Answer (official source)", "Status", "Source"],
        "rows": [
            {
                "cells": [
                    "A01",
                    "Which license classes may apply for a San Francisco plumbing permit?",
                    "C-4, C-16, C-20, C-36, C-54, B or A (B after approval based on scope).",
                    pill("official — sf.gov", "ok"),
                ],
                "src": ["S01"],
            },
            {
                "cells": [
                    "A02",
                    "What does a C-36 license cover?",
                    "The official C-36 Plumbing classification definition (16 CCR, Div. 8, Art. 3).",
                    pill("official — CSLB", "ok"),
                ],
                "src": ["S05"],
            },
            {
                "cells": [
                    "A03",
                    "What does a B license cover, and can a specialty contractor do incidental work in another trade?",
                    "B is the General Building classification (B&P §7057). BPC §7059 allows specialty contractors incidental and supplemental work in other trades; applicability to this ceiling is not established.",
                    pill("official — CSLB / leginfo", "ok"),
                ],
                "src": ["S83", "S62"],
            },
            {
                "cells": [
                    "A04",
                    "What is the current small-job licensing exemption?",
                    "BPC §7048 (AB 1170, effective 2026-01-01): aggregate price under $1,000, casual/minor/inconsequential, and no building permit required.",
                    pill("official — leginfo", "ok"),
                ],
                "src": ["S13"],
            },
            {
                "cells": [
                    "A05",
                    "How should a license be checked before hiring?",
                    "CSLB Check a License is the official lookup by number or business name; CSLB advises checking status and complaint disclosure before hiring.",
                    pill("official — CSLB", "ok"),
                ],
                "src": ["S04"],
            },
            {
                "cells": [
                    "A06",
                    "Is minor interior wallboard repair listed among work that does not need a building permit?",
                    "Yes — SF.gov lists minor repairs to existing interior plaster or wallboard among work that does not need a permit. The plumbing scope is governed by the plumbing-permit rule.",
                    pill("official — sf.gov", "ok"),
                ],
                "src": ["S02", "S01"],
            },
        ],
        "caption": "These answers are quoted or closely paraphrased from the cited official pages. They describe general rules; whether they apply to this exact repair is for SF DBI and the selected licensed contractor to confirm.",
    }

    c.TABLES["discovery"] = {
        "title": "How to discover the missing information",
        "columns": ["#", "Missing information", "Suggestion to discover it", "Status", "Source"],
        "rows": [
            {
                "cells": [
                    "D01",
                    "Original written quotes and photos for the three 2026-08-30 estimates",
                    "Attach the original quote documents and reference photos as project documents, then re-verify the transcribed figures against them.",
                    UNVERIFIED,
                ],
                "src": ["S44"],
            },
            {
                "cells": [
                    "D02",
                    "One comparable all-in written price (plumbing + ceiling + testing)",
                    "Send every shortlisted firm the same written scope (above-attempt, below-access option, ceiling cut/patch/texture/paint, fill-and-drain test, tenant coordination) and request one fixed price with inclusions/exclusions itemized.",
                    UNVERIFIED,
                ],
                "src": ["S44", "S15", "S16"],
            },
            {
                "cells": [
                    "D03",
                    "Hire-date license, bond and workers'-compensation status",
                    "Re-check the license number on CSLB Check a License and request a current certificate of insurance before signing.",
                    pill("official lookup available", "ok"),
                ],
                "src": ["S04"],
            },
            {
                "cells": [
                    "D04",
                    "Current review-platform ratings for this specific work",
                    "Open the Yelp/Angi/BuildZoom/Thumbtack/BBB pages manually on the decision date; automated fetching of Yelp returned HTTP 403.",
                    UNVERIFIED,
                ],
                "src": ["S04"],
            },
            {
                "cells": [
                    "D05",
                    "Applicable-requirements determination for the exact scope",
                    "Ask SF DBI (Permit Center help desk) and the selected licensed contractor to confirm applicability for the final written scope.",
                    pill("official contact available", "ok"),
                ],
                "src": ["S01", "S02"],
            },
            {
                "cells": [
                    "D06",
                    "Job-specific experience with a seized trip lever in an occupied unit",
                    "Ask each firm for references on concealed waste-and-overflow work in occupied units and confirm the above-first, non-forcing approach in writing.",
                    UNVERIFIED,
                ],
                "src": ["S04", "S43", "S40"],
            },
        ],
        "caption": "Suggestions only — no provider has been contacted and no answer has been obtained through these steps in this session. Each suggestion names the source to use.",
    }

    c.PAGES["questions.html"] = {
        "title": "Questions & decisions",
        "eyebrow": "Overview · questions before decision · updated 2026-11-11",
        "h1": "Questions, information & answers before decision",
        "lede": "The clear list of questions that must be addressed before any hiring decision can reasonably be made — what is known from verified sources, what is still missing, and how to discover it.",
        "sections": [
            {
                "type": "callout",
                "tone": "info",
                "html": "<strong>How to use this page.</strong> Work through Q01–Q14 in order. Q01–Q05 decide whether the job can be done and at what scope; Q06–Q12 decide whether the firm is licensed, insured and available; Q13–Q14 are the decision gate. Answers the official sources do give are in the second table; the third table gives a concrete suggestion for discovering each missing item. No provider has been contacted and no answer has been obtained through these steps in this session.",
            },
            {"type": "table", "ref": "questions"},
            {"type": "table", "ref": "answers"},
            {"type": "table", "ref": "discovery"},
            {
                "type": "prose",
                "title": "Decision gate — do not hire until these are answered in writing",
                "html": "<ol class=\"tight\"><li>Above-first, non-forcing assessment with diagnostic fee and stop-and-price point (Q01).</li><li>Below-access option priced separately, with ceiling cut/patch/texture/paint and dust protection stated (Q03–Q04).</li><li>One fixed all-in price with inclusions/exclusions itemized (Q05).</li><li>Hire-date CSLB re-check plus current certificate of insurance (Q06, Q10).</li><li>Complaint-disclosure page read for the chosen license (Q11).</li><li>Occupied-unit plan: access windows, shut-off notice, single point of contact (Q08).</li><li>Applicable-requirements confirmation with SF DBI and the selected licensed contractor (Q09).</li></ol><p>Full ranking and official phones: <a href=\"ranking.html\">Ranked hiring decision</a> · <a href=\"contacts.html\">Contacts &amp; licenses</a> · <a href=\"flagged.html\">Flagged for Review</a>.</p>",
            },
            {
                "type": "callout",
                "tone": "warn",
                "html": "<strong>Informational only.</strong> This page is research, not legal advice, a quote, or a contractor endorsement. Every unverified value is blank in the data tables and listed on the Flagged for Review page.",
            },
        ],
    }

    # Navigation: add to the Overview group after Requirements.
    for group in c.NAV:
        if group["group"] == "Overview":
            group["links"].insert(3, ("questions.html", "Questions & decisions"))
            break

    # Dashboard quick links: add after the Requirements entry.
    for block in c.PAGES["index.html"]["sections"]:
        if block.get("type") == "quick":
            for i, item in enumerate(block["items"]):
                if item["href"] == "requirements.html":
                    block["items"].insert(i + 1, {
                        "href": "questions.html",
                        "t": "Questions & decisions",
                        "d": "Open questions, official answers, and how to discover missing information.",
                    })
                    break
            break
