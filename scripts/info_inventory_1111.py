#!/usr/bin/env python3
"""Known-vs-missing information inventory, two-stage contracting statutes, and R31 (2026-11-11).

Session: arena/a4fcce50-korea7

Publishes `info-inventory.html` with a side-by-side register of:
  1. Information already verified from official/manufacturer sources vs. owner/third-party
     unverified statements vs. missing information (blank + UNVERIFIED) across all 10
     decision domains (I01–I10);
  2. Official statutory and municipal answers read directly on 2026-11-11, including the
     two-stage California contracting distinction between a Service and Repair Contract
     (BPC §7159.10, <= $750, signed written price before starting, zero payment until
     completion) and a Home Improvement Contract (BPC §7159, > $500, prime contractor
     completion responsibility, 10%/$1,000 down-payment cap), plus SF.gov's fire-protection
     exception on minor wallboard repairs and stand-alone R-3 homeowner permit boundary
     (SC01–SC05);
  3. A six-step discovery protocol naming who to inspect/ask and what written evidence
     closes each gap before any hiring decision is made (P01–P06).

Also appends Requirement `R31` to `requirements.html`, Findings `F22`–`F23` to
`findings.html`, and Flag `U54` (dynamic ID) to `flagged.html`. Strictly additive and
idempotent: no existing row, score, or page owned by another module is rewritten.
"""
from __future__ import annotations

import re

CHECKED = "2026-11-11"
SESSION = "arena/a4fcce50-korea7"

NEW_SOURCES = {
    "S400": {
        "label": "CSLB License Detail #829071 — Ace Plumbing & Rooter (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active C-36 + B (and A, C-4, C-16, C-10), (415) 824-6444, $25,000 bond #101993376, workers' compensation insured through 2027-07-13, no complaint disclosure",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:17:57 PM'.",
    },
    "S401": {
        "label": "CSLB License Detail #977638 — Expert Plumbing Solutions (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active C-36, (415) 531-5340, expires 2028-10-31, $25,000 bond #800209947, workers' compensation insured through 2027-07-19; does not verify owner-reported quote amount",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:16:51 PM'.",
    },
    "S402": {
        "label": "CSLB License Detail #757796 — Bay Area Plumbing (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active C-36, (415) 668-8000, expires 2027-01-31, $25,000 bond #800268354, workers'-compensation exemption ('no employees at this time', effective 2024-12-11)",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:17:53 PM'.",
    },
    "S403": {
        "label": "CSLB License Detail #1024971 — Fast Response Plumbing and Rooter (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active C-36, (415) 596-6115, expires 2027-03-31, $25,000 bond #800273981, workers'-compensation policy #EIG576950801 expiring 2026-12-18 (37 days from 2026-11-11)",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:17:36 PM'.",
    },
    "S404": {
        "label": "CSLB License Detail #1003394 — Handyman Heroes Inc (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active B + C-36, (844) 382-4376, expires 2027-05-31, $25,000 bond #89021781, workers' compensation insured through 2027-04-25, complaint-disclosure link present",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:16:14 PM'.",
    },
    "S405": {
        "label": "CSLB License Detail #995163 — Bernal Hill Drywall Inc (2026-11-11 read)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Current and active C-9 Drywall + B General Building, (415) 533-8274, expires 2028-07-31, $25,000 bond #100728251, workers' compensation insured through 2027-03-10",
        "note": "Read directly on 2026-11-11; page printed 'Data current as of 11/10/2026 6:18:06 PM'.",
    },
    "S406": {
        "label": "SF.gov — Apply for a plumbing and mechanical permit (2026-11-11 read)",
        "publisher": "City and County of San Francisco (DBI)",
        "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Permit needed before cutting into or replacing pipes (exemptions in SF Plumbing Code §104.2); eligible classes C4, C16, C20, C36, C54, B (upon scope approval), A; homeowner self-application limited to stand-alone R-3 single-family dwellings; Permit Center 628-652-4900 / permitsf@sfgov.org",
        "note": "Read directly on 2026-11-11; does not determine the exact regulatory classification of an uninspected repair.",
    },
    "S407": {
        "label": "SF.gov — Check if your construction project needs a permit (2026-11-11 read)",
        "publisher": "City and County of San Francisco (DBI)",
        "url": "https://www.sf.gov/information--check-if-your-construction-project-needs-permit",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Lists 'Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection' and 'Painting, papering and similar finish work' among interior work not needing a building permit",
        "note": "Read directly on 2026-11-11; the 'unless they are required for fire protection' condition is critical when a ceiling separates a storage space from a dwelling unit above.",
    },
    "S408": {
        "label": "California Business & Professions Code §7159 — Home improvement contracts",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7159.",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Written home improvement contract required over $500 (§7159(b)) unless governed by a conforming §7159.10 service-and-repair contract (§7159(a)(2)); prime/direct contractor is administratively responsible for project completion per contract, plans and specifications (§7159(a)(5)(B))",
        "note": "Read directly on 2026-11-11 on leginfo.legislature.ca.gov.",
    },
    "S409": {
        "label": "California Business & Professions Code §7159.10 — Service and repair contracts",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7159.10.",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Governs buyer-initiated service-and-repair contracts of $750 or less where no payment is due or accepted until completion (§7159.10(a)(1)(A)–(D)); requires signed written contract with license number and Commercial General Liability (CGL) insurance notice before any work starts (§7159.10(d)(4)–(7))",
        "note": "Read directly on 2026-11-11 on leginfo.legislature.ca.gov.",
    },
    "S410": {
        "label": "California Civil Code §1954 — Landlord entry into occupied dwelling unit (2026-11-11 read)",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Permits entry during normal business hours to make necessary or agreed repairs (§1954(a)(2), (b)); requires reasonable written notice (24 hours presumed reasonable; 6 days if mailed) stating date, approximate time and purpose, or oral agreement with tenant for agreed repairs within one week (§1954(d)(1), (3))",
        "note": "Read directly on 2026-11-11 on leginfo.legislature.ca.gov.",
    },
    "S411": {
        "label": "CSLB — C-9 Drywall Contractor classification (16 CCR Div. 8 Art. 3)",
        "publisher": "Contractors State License Board",
        "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9",
        "tier": "official",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Defines C-9 Drywall Contractor as laying out and installing gypsum wallboard and assemblies, nonstructural metal framing, and taping and texturing operations to produce a continuous smooth or textured surface",
        "note": "Read directly on 2026-11-11 on www2.cslb.ca.gov.",
    },
    "S412": {
        "label": "Oatey — Dearborn Plastic Tubular Trip-Lever Bath Waste (Part# A9226 / P9226)",
        "publisher": "Oatey (manufacturer)",
        "url": "https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste",
        "tier": "manufacturer",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Documents standard polypropylene tubular trip-lever bath waste full kit with chrome-finish stopper (variants Part# A9226 UPC 041193058379 and Part# P9226 UPC 041193057099)",
        "note": "Read directly on 2026-11-11; confirms standard assembly geometry, not the specific installed parts in this apartment.",
    },
    "S413": {
        "label": "Information inventory & two-stage contract verification record — 2026-11-11",
        "publisher": "This project, citing linked official and manufacturer sources",
        "url": "data/canonical/info-inventory-2026-11-11.json",
        "tier": "primary",
        "status": "verified",
        "checked": CHECKED,
        "supports": "Machine-readable transcription of the 2026-11-11 direct official reads, known-vs-missing inventory, and scope boundaries",
        "note": "Primary project artifact; government and manufacturer pages remain authoritative for external facts.",
    },
}


def integrate(c) -> None:
    if "info-inventory.html" in c.PAGES:
        return

    c.SOURCES.update(NEW_SOURCES)
    pill = c.pill
    BLANK = c.BLANK
    UNVERIFIED = c.UNVERIFIED
    MISSING = BLANK + " " + UNVERIFIED

    cslb = lambda lic, text=None: (
        '<a href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=%s" '
        'target="_blank" rel="noopener noreferrer">%s</a>' % (lic, text or ("CSLB #" + lic))
    )

    c.TABLES["info_have_vs_missing"] = {
        "title": "Information inventory — what we already have vs. what we do not have (10 decision domains)",
        "columns": [
            "#",
            "Decision domain",
            "Information we HAVE (officially verified)",
            "Information reported (owner / third-party — unverified)",
            "Information we DO NOT HAVE (verified project value)",
            "How to discover the missing information",
            "Source",
        ],
        "rows": [
            {
                "cells": [
                    "I01",
                    "Concealed waste-and-overflow mechanism & pipe material",
                    "Standard trip-lever bath waste kits use a faceplate lever, internal linkage/plunger and waste tee/shoe (e.g., Oatey Dearborn Part# A9226 / P9226).",
                    "Owner reports the bathtub wastewater overflow trip lever is stuck inside hidden plumbing behind the bathroom wall; no reference photos were supplied.",
                    MISSING + "<br><small>Exact seized part (linkage vs. plunger vs. corroded brass/cast-iron tee), pipe material, and rough-in dimensions</small>",
                    "Photograph the overflow faceplate, lever, and tub drain shoe; commission a non-destructive Stage 1 inspection before pricing concealed pipe replacement.",
                ],
                "src": ["S412", "S93", "S44"],
            },
            {
                "cells": [
                    "I02",
                    "From-above removal feasibility vs. hidden-pipe damage risk",
                    "Manufacturer instructions document overflow-plate screw removal and vertical linkage withdrawal when threads and tee are intact.",
                    "Owner prefers removal from above, but reports 5+ licensed plumbers declined from-above removal due to risk of damaging concealed plumbing.",
                    MISSING + "<br><small>On-site diagnostic finding on whether linkage is seized to the standpipe/tee and exact torque/stop threshold</small>",
                    "Require a written Stage 1 Service &amp; Repair diagnostic (BPC §7159.10) specifying cautious non-forcing inspection from above and an immediate stop condition if hidden fittings resist.",
                ],
                "src": ["S93", "S409", "S44"],
            },
            {
                "cells": [
                    "I03",
                    "Below-ceiling access via storage unit &amp; fire-rating status",
                    "SF.gov lists 'Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection' among work not needing a building permit.",
                    "Owner reports a storage unit sits directly below the bathtub and plumbers recommended opening the drywall ceiling from below.",
                    MISSING + "<br><small>Whether the storage-unit ceiling is a fire-resistance-rated separation assembly (e.g., Type X gypsum), joist/utility obstructions, opening size, and storage-access permission</small>",
                    "Inspect the storage ceiling before cutting; verify with the licensed contractor and SF DBI whether fire-rated wallboard restoration is required; obtain written storage-unit access consent.",
                ],
                "src": ["S407", "S406", "S44"],
            },
            {
                "cells": [
                    "I04",
                    "Existing 2026-08-30 estimates &amp; all-in cost comparability",
                    "All three named firms hold current and active C-36 licenses on 2026-11-11: Expert Plumbing Solutions (" + cslb("977638") + "), Bay Area Plumbing (" + cslb("757796") + "), and Fast Response (" + cslb("1024971") + ").",
                    "Owner reports three 2026-08-30 figures covering incompatible scopes ($614 waste-and-overflow replacement; $550 lever/plug/spout with diverter; $135 plunger handle adjustment).",
                    MISSING + "<br><small>Original written quote documents, whether any quote included drywall/ceiling restoration, and a comparable all-in price for plumbing + ceiling finish + leak testing</small>",
                    "Locate the original 2026-08-30 written estimates and request three new written bids on one identical two-stage scope (above-attempt diagnostic + contingent below-ceiling replacement and full ceiling restoration).",
                ],
                "src": ["S401", "S402", "S403", "S225", "S44"],
            },
            {
                "cells": [
                    "I05",
                    "Single-contract plumbing + drywall trade coverage",
                    "Active dual-classified B + C-36 candidates verified on CSLB include Ace (" + cslb("829071") + "), Genteel (" + cslb("1025814") + "), and Handyman Heroes (" + cslb("1003394") + "); Bernal Hill Drywall (" + cslb("995163") + ") holds C-9 + B. BPC §7159(a)(5)(B) makes the prime contractor responsible for project completion.",
                    "Company websites advertise plumbing and/or sheetrock patching, and HOA/property-manager coordination.",
                    MISSING + "<br><small>Signed single-contract commitment naming who cuts, patches, tapes, textures, primes, and paints the storage ceiling</small>",
                    "Require one prime contract naming all self-performed and subcontracted trades, drywall board type, texture match, primer/paint coats, and cleanup—or explicitly pair a C-36 plumber with C-9 partner " + cslb("995163") + ".",
                ],
                "src": ["S400", "S221", "S404", "S405", "S408", "S411", "S62"],
            },
            {
                "cells": [
                    "I06",
                    "Contract form, deposit limits &amp; change-order protection",
                    "BPC §7159.10 governs buyer-initiated Service &amp; Repair contracts &le; $750 (signed written contract before work starts; no payment until completion). BPC §7159 governs Home Improvement contracts &gt; $500 (10% or $1,000 max down payment; written change orders).",
                    "No draft contract, diagnostic fee schedule, or change-order cap has been provided.",
                    MISSING + "<br><small>Written Stage 1 diagnostic fee (&le; $750), credit of diagnostic fee toward Stage 2 repair, itemized Stage 2 fixed price, and written change-order cap</small>",
                    "Structure the engagement in two written stages: a BPC §7159.10 diagnostic/non-forcing adjustment visit first, and a pre-priced BPC §7159 Home Improvement Contract before any ceiling or concealed-pipe cut.",
                ],
                "src": ["S408", "S409", "S224"],
            },
            {
                "cells": [
                    "I07",
                    "Insurance, bond, workers'-comp expiry &amp; CSLB citation review",
                    "All 17 checked licenses carry a $25,000 bond; 5 carry 'no employees' WC exemptions (including " + cslb("757796") + "); 3 WC policies expire within 49 days (including " + cslb("1024971") + " on 2026-12-18); " + cslb("1003394") + " has 2020 citation 2 2020 001045 (34 entries). BPC §7159.10(d)(7) requires written CGL disclosure.",
                    "Some vendor sites advertise 'fully insured' without publishing policy numbers or limits.",
                    MISSING + "<br><small>Current Certificate of Insurance (Workers' Comp + Commercial General Liability) for the attending crew, hire-date CSLB status check, and written explanation of citation 2 2020 001045 if considering " + cslb("1003394") + "</small>",
                    "Request COI (naming CGL carrier/limits and WC policy) before work, re-verify the chosen license on CSLB on the hire morning, and obtain a written response on the 2020 citation before treating " + cslb("1003394") + " as finalist.",
                ],
                "src": ["S402", "S403", "S404", "S155", "S409", "S225"],
            },
            {
                "cells": [
                    "I08",
                    "San Francisco reviews &amp; delicate occupied-unit experience",
                    "CSLB confirms license classifications and public disclosures only; it does not verify workmanship or job-specific experience.",
                    "Third-party search snippets (Yelp HTTP 403 to direct automated fetch; HomeAdvisor; Angi; BBB) include an Atlas stuck-lever excerpt and a Handyman Heroes wall-after-plumbing excerpt.",
                    MISSING + "<br><small>Live manual review verification and 2 verifiable customer/property-manager references for concealed tub overflow repair in occupied SF units</small>",
                    "Open the linked Yelp/Angi/BBB profiles manually in a browser and ask the top 2–3 candidates for recent SF occupied-unit tub waste-and-overflow references.",
                ],
                "src": ["S04", "S225", "S207", "S210"],
            },
            {
                "cells": [
                    "I09",
                    "Occupied-unit tenant notice, water shut-off &amp; dust protection",
                    "California Civil Code §1954 permits entry during normal business hours for necessary/agreed repairs with reasonable written notice (24 hours presumed reasonable) or an oral agreed-repair arrangement within one week.",
                    "Owner reports tenants occupy the unit where the lever is stuck and a storage space is underneath.",
                    MISSING + "<br><small>Unit vs. building water shut-off valve location, tenant entry window, storage contents protection/plastic containment plan, and multi-visit drying/paint schedule</small>",
                    "Confirm water isolation valve before booking, serve/agree Civil Code §1954 entry windows with tenants, and write dust containment, daily cleanup, and compound-drying return visits into the scope.",
                ],
                "src": ["S410", "S44"],
            },
            {
                "cells": [
                    "I10",
                    "Applicable SF DBI code/permit path &amp; R-3 homeowner rule",
                    "SF.gov requires a permit before cutting into or replacing pipes (particularly behind walls), points to SF Plumbing Code §104.2 exemptions, and limits homeowner self-permitting to stand-alone R-3 single-family dwellings.",
                    "Whether the repair ends as a non-invasive linkage adjustment or requires cutting concealed waste piping and storage-ceiling drywall is not yet established.",
                    MISSING + "<br><small>Building occupancy classification (R-2 multi-unit vs. R-3) and SF DBI confirmation of requirements for the exact post-diagnostic repair scope</small>",
                    "After Stage 1 diagnosis establishes whether piping or fire-rated drywall must be cut, have the selected C-36 / B contractor confirm applicable requirements and inspections with SF DBI Permit Center (628-652-4900 / permitsf@sfgov.org).",
                ],
                "src": ["S406", "S407", "S96"],
            },
        ],
        "caption": "Every row separates officially verified rules/records from unverified owner/third-party statements and leaves unconfirmed project values blank with an explicit UNVERIFIED flag. Nothing is inferred.",
    }

    c.TABLES["staged_contract_rules"] = {
        "title": "Official statutory & municipal answers for staged contracting and ceiling restoration (read 2026-11-11)",
        "columns": [
            "#",
            "Pre-decision question",
            "Official rule / answer (verified 2026-11-11)",
            "Confirmed project value",
            "Source",
        ],
        "rows": [
            {
                "cells": [
                    "SC01",
                    "How can the owner authorize a cautious above-first diagnostic or adjustment visit without committing to open the ceiling?",
                    "Under California BPC §7159.10, a buyer-initiated Service and Repair Contract of $750 or less requires a signed, dated written contract before any work starts (with license number and CGL insurance notice) and prohibits collecting any payment until the contracted diagnostic/repair work is completed.",
                    MISSING + "<br><small>No contractor has quoted a Stage 1 diagnostic fee yet</small>",
                ],
                "src": ["S409"],
            },
            {
                "cells": [
                    "SC02",
                    "Which statutory contract protects the owner if concealed waste-and-overflow replacement plus ceiling restoration exceeds $500 / $750?",
                    "California BPC §7159 requires a written Home Improvement Contract when labor and materials exceed $500 (outside §7159.10): down payment is capped at 10% or $1,000 (whichever is less), extra work requires a signed written change order, and under §7159(a)(5)(B) the prime contractor is administratively responsible for completing the entire contracted scope.",
                    MISSING + "<br><small>No Stage 2 Home Improvement Contract price or scope drafted</small>",
                ],
                "src": ["S408", "S224"],
            },
            {
                "cells": [
                    "SC03",
                    "Does SF.gov's minor wallboard building-permit exemption automatically apply to cutting a storage-unit ceiling below an apartment?",
                    "No — conditional. SF.gov exempts 'Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection.' A ceiling separating a storage area from a dwelling unit above may be a fire-resistance-rated assembly; fire-protection status must be verified before assuming the wallboard repair is exempt or using standard non-rated drywall.",
                    MISSING + "<br><small>Ceiling fire-rating assembly unknown (flagged below)</small>",
                ],
                "src": ["S407", "S406"],
            },
            {
                "cells": [
                    "SC04",
                    "Can a property owner apply for a San Francisco plumbing permit personally if the unit is in a multi-unit or tenant-occupied building?",
                    "SF.gov states: 'Only property owners of stand-alone single-family dwellings (R-3 occupancy) may apply for a plumbing or mechanical permit to do the work themselves.' Non-R-3 buildings require an eligible licensed contractor (C-36, C-4, A, or B upon scope approval).",
                    MISSING + "<br><small>Property occupancy class not confirmed on Assessor/PIM record</small>",
                ],
                "src": ["S406"],
            },
            {
                "cells": [
                    "SC05",
                    "What trade scope does CSLB C-9 Drywall cover if a plumbing-only firm is paired with a restoration contractor?",
                    "Under 16 CCR Div. 8 Art. 3, a C-9 Drywall Contractor lays out and installs gypsum wallboard and assemblies (including nonstructural metal framing) and performs taping and texturing operations to produce a continuous smooth or textured surface—e.g., Bernal Hill Drywall Inc (" + cslb("995163") + ", C-9 + B). Painting should still be explicitly itemized.",
                    MISSING + "<br><small>Finish level (e.g., smooth vs. textured) and paint coats unquoted</small>",
                ],
                "src": ["S411", "S405"],
            },
        ],
        "caption": "Statutory and municipal rules read directly on 2026-11-11 at leginfo.legislature.ca.gov, sf.gov, and www2.cslb.ca.gov. Informational research only — not legal advice; confirm scope-specific applicability with SF DBI and the selected licensed contractor.",
    }

    c.TABLES["discovery_protocol_1111"] = {
        "title": "Six-step discovery plan — concrete suggestions to obtain all missing information before deciding",
        "columns": [
            "Step",
            "Target / party",
            "Missing information to discover",
            "Concrete action & written deliverable to collect",
            "Current status",
            "Source",
        ],
        "rows": [
            {
                "cells": [
                    "P01",
                    "On-site photo &amp; quote packet (Owner)",
                    "Exact visible hardware style, drain shoe condition, shut-off valve location, storage-ceiling finish, and text of the 2026-08-30 estimates",
                    "Take 5 clear photos (overflow plate/lever, tub drain shoe, bathroom access/shut-off, storage ceiling directly below, nearby ceiling framing/lights) and attach the written 2026-08-30 estimates so every bidder prices the same baseline.",
                    MISSING,
                ],
                "src": ["S44", "S412"],
            },
            {
                "cells": [
                    "P02",
                    "Building / storage-space check (Owner / Management)",
                    "Storage-unit entry authorization, contents clearance, building water shut-off rules, and whether the storage ceiling is fire-rated",
                    "Confirm written permission to access and protect the storage space below, check building records/plaques for fire-rated ceiling separation, and confirm water shut-off notice rules.",
                    MISSING,
                ],
                "src": ["S407", "S44"],
            },
            {
                "cells": [
                    "P03",
                    "Comparable two-stage RFP to top candidates",
                    "Stage 1 non-forcing above-first diagnostic fee (&le; $750) and Stage 2 all-in fixed price (concealed waste-and-overflow + ceiling cut, drywall/Type X patch, tape, texture, primer, paint, containment, fill-and-drain test)",
                    "Send identical written scope + P01 photo packet to dual-licensed candidates — Handyman Heroes (" + cslb("1003394") + "), Ace (" + cslb("829071") + "), Genteel (" + cslb("1025814") + ") — or pair a C-36 plumber (" + cslb("868994") + ", " + cslb("1024971") + ", " + cslb("977638") + ") with Bernal Hill Drywall (" + cslb("995163") + ").",
                    MISSING,
                ],
                "src": ["S404", "S400", "S221", "S69", "S403", "S401", "S405", "S408", "S409"],
            },
            {
                "cells": [
                    "P04",
                    "Finalist license, COI &amp; reference verification",
                    "Hire-date CSLB license/bond/WC status, Commercial General Liability policy limits, occupied-unit references, and " + cslb("1003394") + " citation explanation",
                    "Re-check CSLB on the morning of hire, obtain current COI (Workers' Comp + CGL) naming the business on the contract, check 2 occupied-unit references, and require written explanation of citation 2 2020 001045 before hiring " + cslb("1003394") + ".",
                    MISSING,
                ],
                "src": ["S04", "S225", "S404", "S155"],
            },
            {
                "cells": [
                    "P05",
                    "Post-diagnostic code &amp; inspection confirmation (Contractor + SF DBI)",
                    "Whether Stage 1 freed the linkage non-destructively or Stage 2 requires pipe cutting / fire-rated ceiling restoration and SF DBI permits/inspections",
                    "Stop after Stage 1 if concealed piping is at risk; have the selected licensed contractor confirm applicable SF Plumbing Code §104.2 / building requirements with SF DBI Permit Center (628-652-4900 / permitsf@sfgov.org) before cutting.",
                    MISSING,
                ],
                "src": ["S406", "S407", "S96"],
            },
            {
                "cells": [
                    "P06",
                    "Tenant &amp; storage coordination + pre-closure leak test",
                    "Lawful tenant entry window (Civil Code §1954), water shut-off window, open-ceiling water test before patching, and warranty terms",
                    "Deliver 24-hour written entry notice (or confirm 1-week oral agreed-repair schedule) under Civil Code §1954; witness a full tub fill, overflow, and drain leak test before closing the ceiling; collect photos and written warranty before final payment.",
                    MISSING,
                ],
                "src": ["S410", "S408", "S409"],
            },
        ],
        "caption": "No contractor, agency, or tenant has been contacted in this research session; all six steps remain unexecuted project recommendations.",
    }

    c.PAGES["info-inventory.html"] = {
        "title": "Information inventory",
        "eyebrow": "Overview · known vs. missing information · updated 2026-11-11",
        "h1": "Information we have, information we lack & how to discover it",
        "lede": "A complete pre-decision inventory contrasting every fact verified from official sources against unverified owner/third-party statements, the exact missing answers that block hiring today, two-stage California contracting rules (BPC §7159.10 and §7159), and a six-step discovery protocol.",
        "sections": [
            {
                "type": "callout",
                "tone": "ok",
                "html": "<strong>Why this page exists.</strong> Before any hiring decision can reasonably be made, the decision-maker needs four things side by side: (1) what is already confirmed from official records, (2) what comes only from unverified owner or third-party reports, (3) what critical project answers are still missing, and (4) concrete steps to discover every missing answer. Complementing <a href=\"questions.html\">Questions &amp; decisions</a> and <a href=\"decision-checklist.html\">Decision checklist</a>, this page maps all ten project domains and adds the 2026-11-11 statutory reads on staged diagnostic vs. repair contracts.",
            },
            {"type": "table", "ref": "info_have_vs_missing"},
            {"type": "table", "ref": "staged_contract_rules"},
            {"type": "table", "ref": "discovery_protocol_1111"},
            {
                "type": "prose",
                "title": "Summary of decision readiness (as of 2026-11-11)",
                "html": (
                    "<p><strong>What is ready now:</strong> Contractor license verification (17 active CSLB records re-verified on 2026-11-11; see <a href=\"reread-1111.html\">Re-read 2026-11-11</a>), complaint-disclosure screening (<a href=\"ranking.html\">Ranked hiring decision</a>), official contact numbers (<a href=\"contacts.html\">Contacts &amp; licenses</a>), and statutory contracting/entry rules (<a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7159.10.\" target=\"_blank\" rel=\"noopener noreferrer\">BPC §7159.10</a>, <a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7159.\" target=\"_blank\" rel=\"noopener noreferrer\">BPC §7159</a>, <a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&amp;sectionNum=1954\" target=\"_blank\" rel=\"noopener noreferrer\">Civil Code §1954</a>).</p>"
                    "<p><strong>What blocks an immediate unconditional hire:</strong> No contractor has inspected the seized linkage with a non-forcing diagnostic scope, no one has verified whether the storage-unit ceiling is a fire-rated separation assembly, and no bidder has provided a written, comparable all-in price covering concealed waste-and-overflow repair plus full ceiling patch, texture, primer, and paint. Execute Steps <strong>P01–P06</strong> above before authorizing any ceiling or pipe cut.</p>"
                ),
            },
            {
                "type": "callout",
                "tone": "warn",
                "html": "<strong>Informational only.</strong> Nothing on this page is legal or code-compliance advice, a contractor quote, or proof of workmanship. All unconfirmed project values remain blank and flagged on <a href=\"flagged.html\">Flagged for review</a>.",
            },
        ],
    }

    # Append R31 to the Requirements Register so the new brief requirement is tracked line by line.
    req_ids = {r["cells"][0] for r in c.TABLES["requirements"]["rows"]}
    if "R31" not in req_ids:
        c.TABLES["requirements"]["rows"].append({
            "cells": [
                "R31",
                "Clear list of questions, information we already have and do not have, answers needed before deciding, and suggestions to discover missing information",
                "Decision analysis",
                "Published on Information inventory, Questions & decisions, and Decision checklist pages; project-specific answers remain blank/unverified",
                pill("implemented / project answers unverified", "ok"),
            ],
            "src": ["S44", "S406", "S407", "S408", "S409", "S410", "S413"],
        })

    # Append F22 and F23 to Findings & Analysis.
    finding_ids = {r["cells"][0] for r in c.TABLES["findings"]["rows"]}
    if "F22" not in finding_ids:
        c.TABLES["findings"]["rows"].extend([
            {
                "cells": [
                    "F22",
                    "Two-stage California contract rules (BPC §7159.10 and §7159) fit an above-first diagnostic followed by contingent ceiling access",
                    "Direct 2026-11-11 reads of BPC §7159.10 (buyer-initiated Service & Repair contracts <= $750: signed written price and CGL insurance notice before work starts, zero payment until completion) and BPC §7159 (Home Improvement contracts > $500: prime contractor completion responsibility under §7159(a)(5)(B), down payment capped at 10% or $1,000, written change orders) give a clean statutory structure for separating non-forcing diagnosis from full replacement and ceiling restoration.",
                    pill("verified 2026-11-11", "ok"),
                ],
                "src": ["S408", "S409", "S224"],
            },
            {
                "cells": [
                    "F23",
                    "SF.gov minor-wallboard permit exemption excludes wallboard 'required for fire protection' — critical for a storage-unit ceiling below an apartment",
                    "SF.gov's building-permit exemption page lists 'Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection.' Because the ceiling separates a storage space below from an occupied residential unit above, fire-rated assembly status (e.g., Type X gypsum) is a critical missing fact affecting both code compliance and restoration specification.",
                    pill("verified rule / project status unverified", "warn"),
                ],
                "src": ["S407", "S406", "S44"],
            },
        ])

    # Append U54 (dynamically numbered) for the storage-ceiling fire-protection caveat.
    existing_nums = [
        int(m.group(1))
        for row in c.TABLES["flagged"]["rows"]
        for m in [re.fullmatch(r"U(\d+)", str(row["cells"][0]))]
        if m
    ]
    already_flagged = any(
        "required for fire protection" in str(row["cells"][2])
        for row in c.TABLES["flagged"]["rows"]
    )
    if not already_flagged:
        next_flag = "U%d" % (max(existing_nums) + 1)
        c.TABLES["flagged"]["rows"].append({
            "cells": [
                next_flag,
                "Storage-unit ceiling fire-protection rating unknown (SF.gov wallboard exception)",
                "SF.gov exempts 'Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection.' Whether the ceiling between the storage unit below and the occupied dwelling unit above is a required fire-resistance-rated separation (e.g., Type X gypsum board) is not confirmed.",
                "Inspect and confirm ceiling fire-rating status with the licensed contractor and SF DBI before cutting, and specify matching fire-rated gypsum assembly if required.",
                UNVERIFIED,
            ],
            "src": ["S407", "S406", "S44"],
        })

    # Add navigation link under Overview after Questions & decisions.
    for group in c.NAV:
        if group["group"] == "Overview":
            if ("info-inventory.html", "Information inventory") not in group["links"]:
                idx = next(
                    (i + 1 for i, (h, _) in enumerate(group["links"]) if h == "questions.html"),
                    len(group["links"]),
                )
                group["links"].insert(idx, ("info-inventory.html", "Information inventory"))
            break

    # Add quick-link card on index.html after Questions & decisions.
    for block in c.PAGES["index.html"]["sections"]:
        if block.get("type") == "quick":
            if not any(it.get("href") == "info-inventory.html" for it in block["items"]):
                idx = next(
                    (i + 1 for i, it in enumerate(block["items"]) if it.get("href") == "questions.html"),
                    len(block["items"]),
                )
                block["items"].insert(idx, {
                    "href": "info-inventory.html",
                    "t": "Information inventory",
                    "d": "Side-by-side register of verified facts, unverified reports, missing answers, BPC §7159.10/§7159 contract rules, and a 6-step discovery plan.",
                })
            break

    # Add callout on summary.html pointing to the complete known-vs-missing inventory.
    summary_sections = c.PAGES["summary.html"]["sections"]
    if not any("info-inventory.html" in b.get("html", "") for b in summary_sections):
        summary_sections.insert(1, {
            "type": "callout",
            "tone": "info",
            "html": "<strong>Known vs. missing information &amp; discovery plan (2026-11-11):</strong> see <a href=\"info-inventory.html\">Information inventory</a> for the side-by-side breakdown of verified facts vs. missing project answers across all 10 domains, the two-stage contracting rules (<a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7159.10.\" target=\"_blank\" rel=\"noopener noreferrer\">BPC §7159.10</a> &le; $750 diagnostic vs. <a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7159.\" target=\"_blank\" rel=\"noopener noreferrer\">BPC §7159</a> full repair), the storage-ceiling fire-rating check, and the 6-step discovery protocol.",
        })

    # Re-sort and synchronize flag counts across all pages/cards.
    c.TABLES["flagged"]["rows"].sort(
        key=lambda r: (
            int(re.fullmatch(r"U(\d+)", str(r["cells"][0])).group(1))
            if re.fullmatch(r"U\d+", str(r["cells"][0]))
            else 10 ** 6
        )
    )
    import session_1012_verification as _norm_mod
    _norm_mod._normalise_flags(c)
    c.META["updated"] = CHECKED
    c.META["session"] = SESSION
