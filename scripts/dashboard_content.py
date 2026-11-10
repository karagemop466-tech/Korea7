"""Canonical content for the bathtub-overflow trip-lever research dashboard.

This module is the single source of truth for the integration session
`arena/2eb487ad-korea7`. Every fact that appears in a table row cites one or
more source ids from SOURCES. Values that cannot be confirmed from an official
source are left blank and flagged. Nothing here is inferred.

Retrieval date for every source: 2026-11-07 (UTC), unless the source note says
otherwise. Official government records were read directly from the issuing
agency; CSLB License Detail pages printed "Data current as of 11/7/2026".
"""

META = {
    "updated": "2026-11-10",
    "session": "arena/33211fbf-korea7",
    "title": "Bathtub overflow trip lever — repair research dashboard",
    "pages_url": "https://karagemop466-tech.github.io/Korea7/",
    "repo_url": "https://github.com/karagemop466-tech/Korea7",
}

NAV = [
    {"group": "Overview", "links": [
        ("index.html", "Dashboard"),
        ("summary.html", "Executive summary"),
        ("requirements.html", "Requirements"),
    ]},
    {"group": "Decision", "links": [
        ("ranking.html", "Ranked hiring decision"),
        ("contacts.html", "Contacts & licenses"),
    ]},
    {"group": "Data", "links": [
        ("estimates.html", "Estimates & costs"),
        ("contractors.html", "Contractors & reviews"),
        ("findings.html", "Findings & analysis"),
        ("shortlist.html", "Shortlist"),
    ]},
    {"group": "Reference", "links": [
        ("technical.html", "Technical background"),
        ("permits.html", "Permits & licensing"),
        ("brief.html", "Project brief"),
        ("sources.html", "Source ledger"),
    ]},
    {"group": "Audit", "links": [
        ("verification.html", "Verification"),
        ("repo-review.html", "Repo review"),
        ("verification-log.html", "Prior verification log"),
        ("flagged.html", "Flagged for review"),
    ]},
]

# tier: official / manufacturer / publisher / platform / company / primary
# status: verified / blocked-403 / dead / removed
SOURCES = {
    "S01": {"label": "SF.gov — Apply for a plumbing and mechanical permit", "publisher": "SF Dept. of Building Inspection", "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Permit requirement for cutting into/replacing pipes; license classes allowed to apply; inspection before covering pipes; homeowner R-3 restriction", "note": "Read directly on sf.gov, 2026-11-07."},
    "S02": {"label": "SF.gov — Check if your construction project needs a permit", "publisher": "SF Dept. of Building Inspection", "url": "https://www.sf.gov/information--check-if-your-construction-project-needs-permit", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Published list of work that does not need a permit, including minor repairs to existing interior plaster or wallboard", "note": "Read directly on sf.gov, 2026-11-07."},
    "S03": {"label": "SF Building/Plumbing Code — Section 104.0 Permits", "publisher": "American Legal Publishing code library (City and County of SF)", "url": "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Official code location for §104.2 exempt work referenced by sf.gov", "note": "Page title confirmed as 'SECTION 104.0 - PERMITS'. The code library page is JavaScript-heavy; the exemption text was not machine-parsed, so the link is provided for manual review and no section wording is quoted from it."},
    "S04": {"label": "CSLB — Check a License", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Official license lookup by number or business name; CSLB advises checking status and complaint disclosure before hiring", "note": "Read directly on cslb.ca.gov, 2026-11-07."},
    "S05": {"label": "CSLB — C-36 Plumbing classification", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Official definition of the C-36 Plumbing classification (16 CCR, Div. 8, Art. 3)", "note": "Read directly on cslb.ca.gov, 2026-11-07."},
    "S06": {"label": "CSLB License Detail #977638 — Expert Plumbing Solutions", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation", "note": "Record printed 'Data current as of 11/7/2026 12:22:23 PM'."},
    "S07": {"label": "CSLB License Detail #757796 — Bay Area Plumbing", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation exemption", "note": "Record printed 'Data current as of 11/7/2026 12:22:25 PM'."},
    "S08": {"label": "CSLB License Detail #1024971 — Fast Response Plumbing and Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation policy dates", "note": "Record printed 'Data current as of 11/7/2026 12:22:23 PM'."},
    "S09": {"label": "CSLB License Detail #959843 — GENERALSF", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/expiry dates, status, B/C10/C36 classifications, bond, workers' compensation exemption", "note": "Record printed 'Data current as of 11/7/2026 12:21:47 PM'."},
    "S10": {"label": "CSLB License Detail #1003394 — Handyman Heroes Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/expiry dates, status, B/C36 classifications, bond, workers' compensation, complaint-disclosure flag", "note": "Record printed 'Data current as of 11/7/2026 12:21:47 PM'."},
    "S11": {"label": "CSLB License Detail #829071 — Ace Plumbing & Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, address, entity, issue/reissue/expiry dates, status, A/B/C-4/C10/C16/C36 classifications, bond, workers' compensation", "note": "Record printed 'Data current as of 11/7/2026 12:23:38 PM'."},
    "S12": {"label": "CSLB Complaint Disclosure #1003394", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Citation 2 2020 001045, dated 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'", "note": "Read directly on cslb.ca.gov, 2026-11-07. Reported verbatim, no interpretation."},
    "S13": {"label": "California Business & Professions Code §7048", "publisher": "California Legislative Information (leginfo)", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Current small-job licensing exemption: aggregate price under $1,000, casual/minor/inconsequential, and no building permit required; amended by Stats. 2025 ch. 67 (AB 1170), effective 2026-01-01", "note": "Read directly on leginfo, 2026-11-07."},
    "S14": {"label": "Oatey — Dearborn Plastic Tubular Trip-Lever Bath Waste", "publisher": "Oatey (manufacturer)", "url": "https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste", "tier": "manufacturer", "status": "verified", "checked": "2026-11-07", "supports": "Existence and naming of a full trip-lever bath waste-and-overflow kit with chrome-finish stopper", "note": "Manufacturer product page read directly, 2026-11-07."},
    "S15": {"label": "Angi — Cost to Replace a Bathtub or Shower Drain (2026)", "publisher": "Angi", "url": "https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "$500–$1,020 range, $700 average, $230 low / $1,170 high; labor $45–$200/hr; drywall ~$2,100; drain clearing avg $225; water damage $1,350–$6,100", "note": "Article states 'Updated Sep 18, 2026'. Read directly."},
    "S16": {"label": "Angi — Bathroom Leak Repair Cost (2026)", "publisher": "Angi", "url": "https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "$150–$600 leak repair range, $275 average, up to $4,000 complex; drywall/tile follow-up $300–$930; call-out $50–$200; labor $45–$200/hr; worn-out tub drain avg $700", "note": "Article states 'Updated Oct 28, 2026'. Read directly."},
    "S17": {"label": "Angi — What Is a Bathtub Overflow Drain?", "publisher": "Angi", "url": "https://www.angi.com/articles/what-is-overflow-drain.htm", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Overflow drain function; concealed channel; traditional vs integral overflow; trip-lever/rod diagram", "note": "Article states 'Updated Jul 9, 2026'. Read directly."},
    "S18": {"label": "This Old House — How To Replace a Tub Drain", "publisher": "This Old House", "url": "https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Bath waste-and-overflow components (drain shoe, linkage assembly, overflow plate, trap); remove the two overflow-plate screws from above; for stubborn drains access plumbing from below; 3–4 hour DIY estimate", "note": "Read directly. Article is a DIY guide, not San Francisco code guidance."},
    "S19": {"label": "This Old House — Bathtub Installation Cost (2026)", "publisher": "This Old House", "url": "https://www.thisoldhouse.com/bathrooms/bathtub-installation-cost", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Itemized component table including Overflow $163, Drain $190, Spout $82; total $2,110", "note": "Article states 'Updated 03/05/2026'. Read directly."},
    "S20": {"label": "Family Handyman — Replace a bathtub drain stopper", "publisher": "Family Handyman", "url": "https://www.familyhandyman.com/project/how-to-convert-bathtub-drain-lever-to-a-lift-and-turn-drain/", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Removing an old-style trip-lever linkage begins at the overflow plate; lift-and-turn conversion", "note": "Article states 'Updated on Feb. 14, 2024'. Read directly."},
    "S21": {"label": "Hunker — The Trip Lever In My Bathtub Is Stuck", "publisher": "Hunker", "url": "https://www.hunker.com/13417812/the-trip-lever-in-my-bathtub-is-stuck/", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Trip lever is hidden behind the tub wall; diagnosis begins by removing the cover plate and checking links", "note": "Article states 'Updated Oct 3, 2020'. Read directly."},
    "S22": {"label": "The Overall Plumber — Bathtub Drain Drama", "publisher": "The Overall Plumber (trade blog, Houston TX)", "url": "https://www.theoverallplumber.com/home-improvement/bathtub-drain-drama-why-you-need-a-licensed-and-insured-plumber-fast/", "tier": "publisher", "status": "verified", "checked": "2026-11-07", "supports": "Typical repair range $80–$600; most repairs 1–4 hours; repair-vs-replacement decision table; hydrostatic/water test of drain assembly", "note": "Published date not shown on the fetched page — left blank, not inferred. Trade blog; not a San Francisco authority."},
    "S23": {"label": "Angi — Best plumbers in San Francisco, CA", "publisher": "Angi", "url": "https://www.angi.com/companylist/us/ca/san-francisco/plumbing.htm", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "San Francisco plumbing category with verified-review counts; 873 verified plumbing reviews; review text about older SF homes", "note": "Page states 'Last update on August 01, 2026'. Read directly. Platform reviews are not license verification."},
    "S24": {"label": "Angi — Bathtub restoration pros in San Francisco, CA", "publisher": "Angi", "url": "https://www.angi.com/companylist/us/ca/san-francisco/bathtub-refinishing.htm", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "SF bathtub-specific verified reviews, including a small SF property owner describing plumbing plus drywall/ceiling work in a tenant-occupied multi-unit building", "note": "Read directly. Review text is a customer statement, not an official capability finding."},
    "S25": {"label": "BuildZoom — Plumbers in San Francisco, CA", "publisher": "BuildZoom", "url": "https://www.buildzoom.com/san-francisco-ca/plumbers", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "San Francisco plumbing directory with client reviews, verified projects and permit/license-derived profiles", "note": "Read directly. Page shows '683 experts'; count is a point-in-time platform figure."},
    "S26": {"label": "BuildZoom — Drywall and plaster contractors in San Francisco, CA", "publisher": "BuildZoom", "url": "https://www.buildzoom.com/san-francisco-ca/drywall-contractors", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "San Francisco drywall/plaster directory with reviews and project photos", "note": "Read directly. Page shows '83 experts'; point-in-time platform figure."},
    "S27": {"label": "Thumbtack — Bathtub services near San Francisco, CA", "publisher": "Thumbtack", "url": "https://www.thumbtack.com/ca/san-francisco/bathtub-refinishing", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "San Francisco bathtub-service listings with customer reviews and 'Licensed pro' badges", "note": "Read directly. A platform 'Licensed pro' badge is not a CSLB license verification."},
    "S28": {"label": "BBB — Expert Plumbing Solutions business profile", "publisher": "Better Business Bureau", "url": "https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492", "tier": "platform", "status": "verified", "checked": "2026-11-07", "supports": "Business profile: not BBB accredited, no BBB rating, no complaints in last 3 years, license number 977638 on record, 1465 44th Avenue SF", "note": "Read directly. BBB states it does not verify third-party information."},
    "S29": {"label": "Yelp — Bathtub Repair in San Francisco", "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Category search for the specific work type in San Francisco", "note": "Direct fetch returned HTTP 403 to automated access; the live link is provided for manual review. No rating values are claimed from this URL."},
    "S30": {"label": "Yelp — Plumbers in San Francisco", "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Category search for licensed plumbers serving San Francisco", "note": "HTTP 403 on automated fetch; link provided for manual review."},
    "S31": {"label": "Yelp — Drywall Installation & Repair in San Francisco", "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Category search for the drywall half of the combined scope", "note": "HTTP 403 on automated fetch; link provided for manual review."},
    "S32": {"label": "Yelp — Expert Plumbing Solutions", "publisher": "Yelp", "url": "https://www.yelp.com/biz/expert-plumbing-solutions-san-francisco", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for one of the three quoting companies", "note": "HTTP 403 on automated fetch. A 2026-11-06 snapshot (4.8, 81 reviews) exists in prior-session notes; not re-verified — flagged."},
    "S33": {"label": "Yelp — Bay Area Plumbing", "publisher": "Yelp", "url": "https://www.yelp.com/biz/bay-area-plumbing-san-francisco", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for one of the three quoting companies", "note": "HTTP 403 on automated fetch. A 2026-11-06 snapshot (4.8, 175 reviews) exists in prior-session notes; not re-verified — flagged."},
    "S34": {"label": "Yelp — Fast Response Plumbing & Rooter", "publisher": "Yelp", "url": "https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for one of the three quoting companies", "note": "HTTP 403 on automated fetch. A 2026-11-06 snapshot (4.8, 906 reviews) exists in prior-session notes; not re-verified — flagged."},
    "S35": {"label": "Yelp — General SF", "publisher": "Yelp", "url": "https://www.yelp.com/biz/general-sf-san-francisco-2", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for an all-in-one candidate", "note": "HTTP 403 on automated fetch. Prior-session snapshot (4.8, 336 reviews) not re-verified — flagged."},
    "S36": {"label": "Yelp — Handyman Heroes", "publisher": "Yelp", "url": "https://www.yelp.com/biz/handyman-heroes-san-francisco-5", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for an all-in-one candidate", "note": "HTTP 403 on automated fetch. Prior-session snapshot (4.7, 410 reviews) not re-verified — flagged."},
    "S37": {"label": "Yelp — Szeto Plumbing and Handyman", "publisher": "Yelp", "url": "https://www.yelp.com/biz/szeto-plumbing-and-handyman-daly-city-2", "tier": "platform", "status": "blocked-403", "checked": "2026-11-07", "supports": "Business review page for a plumbing+drywall lead outside SF proper", "note": "HTTP 403 on automated fetch. Prior-session snapshot (4.8, 89 reviews) not re-verified — flagged; license not found on CSLB."},
    "S38": {"label": "Expert Plumbing Solutions — official site", "publisher": "Expert Plumbing Solutions", "url": "https://www.eplumbingsolutions.com/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company states License # 977638, San Francisco address 1465 44th Avenue, phone (415) 531-5340", "note": "Read directly. Company self-description is not independent verification; license facts come from CSLB."},
    "S39": {"label": "Bay Area Plumbing — official site", "publisher": "Bay Area Plumbing", "url": "https://www.bayareaplumbingsf.com/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company states it has served San Francisco since 1995, phone (415) 668-8000, residential and commercial plumbing", "note": "Read directly. Company self-description is not independent verification."},
    "S40": {"label": "Fast Response Plumbing & Rooter — official site", "publisher": "Fast Response Plumbing & Rooter", "url": "https://www.fastresponseplumbingsf.com/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company states CSLB #1024971, C-36, service to houses/apartments/HOAs/property managers, and '4.9 / 1,500 Reviews on Yelp & Google'", "note": "Read directly. The review aggregate is a company claim, not verified — flagged. License facts come from CSLB."},
    "S41": {"label": "General SF — official site", "publisher": "General SF", "url": "https://generalsf.com/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company site lists Electrical, Plumbing, Building and Bathroom & Kitchen services and prints 'CSLB. 959843'", "note": "Read directly. Company self-description is not independent verification."},
    "S42": {"label": "Handyman Heroes — official site", "publisher": "Handyman Heroes Inc", "url": "https://www.handymanhero.es/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company site advertises construction, electrical, plumbing and handyman services; states 'Licensed C-10' and 'Licensed C-36'", "note": "Read directly. CSLB #1003394 lists B + C-36 only — the C-10 claim is an irregularity (flagged)."},
    "S43": {"label": "Ace Plumbing & Rooter — official site", "publisher": "Ace Plumbing & Rooter Inc", "url": "https://www.aceplumbingandrooter.com/", "tier": "company", "status": "verified", "checked": "2026-11-07", "supports": "Company lists license #829071 with A, B, C4, C10, C16 and C36 classifications; describes service to HOAs and property managers", "note": "Read directly. Classifications independently confirmed on CSLB #829071."},
    "S44": {"label": "Project brief (owner-provided primary record)", "publisher": "This project's own record, published on this site", "url": "brief.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Owner-provided problem statement, three 2026-08-30 estimates, access constraints, service requirements and tenant-occupancy context", "note": "Primary record only — not an independent public source. Every value taken from it is marked UNVERIFIED in official-verification columns."},
    "S45": {"label": "COORDINATION.md — shared task board", "publisher": "This repository", "url": "https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Task claims, handoffs, verification log, irregularities, PR and merge record", "note": "Repository file, read locally 2026-11-07."},
    "S46": {"label": "Published GitHub Pages site", "publisher": "GitHub Pages / this repository", "url": "https://karagemop466-tech.github.io/Korea7/", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Live landing page location for this dashboard", "note": "Pages source is branch main, path /."},
    "S47": {"label": "Repository README", "publisher": "This repository", "url": "https://github.com/karagemop466-tech/Korea7/blob/main/README.md", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Legacy GEMS project description and current status, used for the repo-review irregularity", "note": "Read locally."},
    "S48": {"label": "Legacy GEMS site (archived)", "publisher": "This repository", "url": "docs/index.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Unrelated legacy project pages retained in the repo", "note": "Internal link, not edited by this session."},
    "S49": {"label": "Parallel microsite (archived)", "publisher": "This repository", "url": "bathtub-overflow/executive-summary.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Prior session's overflow pages, retained unpublished-from-nav as archive", "note": "Internal link, not edited by this session."},
    "S50": {"label": "Parallel microsite (archived)", "publisher": "This repository", "url": "docs/bath/index.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Prior session's docs/bath pages, retained as archive", "note": "Internal link, not edited by this session."},
    "S51": {"label": "Parallel dashboard (archived)", "publisher": "This repository", "url": "docs/plumbing-index.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Prior session's docs/overflow dashboard, retained as archive", "note": "Internal link, not edited by this session."},
    "S52": {"label": "Open PR #32 (stale parallel session)", "publisher": "GitHub", "url": "https://github.com/karagemop466-tech/Korea7/pull/32", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Open, conflicting PR from a 2026-11-06 parallel session that also touched index.html", "note": "Checked with gh: state OPEN, mergeable CONFLICTING, last updated 2026-11-06 13:45 UTC. Left untouched."},
    "S53": {"label": "SFGate Home Guides — trip lever article (DEAD)", "publisher": "SFGate / Weekand", "url": "https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html", "tier": "publisher", "status": "dead", "checked": "2026-11-07", "supports": "Removed from all active citations", "note": "Redirects to weekand.com with empty content on 2026-11-07. Not linked from any table row; retained here as a labeled documentation row."},
    "S56": {"label": "CSLB License Detail #1115649 — Rapid Flow Plumbing & Rooter Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, 230 Edinburgh St SF 94112, corporation, issued 2024-01-29, expires 2028-01-31, B + C-36 classifications, $25,000 bond, workers'-compensation exemption", "note": "Record printed 'Data current as of 11/7/2026 12:46:25 PM'. Added from the concurrent shortlist session, re-read directly here."},
    "S57": {"label": "CSLB License Detail #841229 — Manny's Plumbing & Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Business name, 41 Midvale Drive Daly City CA 94015, sole ownership, issued 2004-06-21, expires 2028-06-30, C-36 + B classifications, $25,000 bond, workers'-compensation exemption", "note": "Record printed 'Data current as of 11/7/2026 12:46:25 PM'. Daly City address — service area to be confirmed. Added from the concurrent shortlist session, re-read directly here."},
    "S58": {"label": "Shortlist — who can do the plumbing and the drywall", "publisher": "This repository (parallel session)", "url": "shortlist.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Ranked shortlist of dual-classified (B + C-36) firms with a vetting script", "note": "Page produced by a concurrent session; license-scope clarification added 2026-11-08."},
    "S61": {"label": "Fast Response — plumbing repair and replacement", "publisher": "Fast Response Plumbing & Rooter", "url": "https://www.fastresponseplumbingsf.com/plumbing-repair-replacement", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Company lists bathtub waste and overflow repair and replacement in San Francisco and publishes a phone number", "note": "Company self-description, not proof of experience with this stuck mechanism, drywall, availability or acceptance of this job."},
    "S62": {"label": "California BPC §7059 — specialty contractor incidental work", "publisher": "California Legislative Information", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7059.&lawCode=BPC", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Specialty contractors may undertake other trades when incidental and supplemental to their licensed work", "note": "Directly read 2026-11-08; applicability to this particular ceiling repair is not established."},
    "S63": {"label": "Archived overflow verification page", "publisher": "This repository (parallel session)", "url": "docs/overflow-verification.html", "tier": "primary", "status": "verified", "checked": "2026-11-08", "supports": "Historical page containing overly categorical licensing statements; see U22", "note": "Historical claims should not be treated as current legal advice."},
    "S60": {"label": "SF overflow audit — parallel session dashboard", "publisher": "This repository (parallel session)", "url": "sf-overflow-audit/index.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Independent 9-page audit dashboard with 11 CSLB records, Watco/Oatey technical notes and 15 flagged items", "note": "Disjoint file scope produced by session arena/2baecdab-korea7, merged unchanged; linked here in response to its cross-link request."},
    "S59": {"label": "Verification log — earlier session", "publisher": "This repository (parallel session)", "url": "verification-log.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Earlier session's line-by-line verification and correction log", "note": "Preserved verbatim from the add/add conflict on verification.html; linked from repo-review.html."},
    "S55": {"label": "Source ledger (this site)", "publisher": "This dashboard", "url": "sources.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Documentation rows about sources removed from active citations", "note": "Internal page on this site. Dead URLs are shown there as plain text, never as links."},
    "S54": {"label": "InspectAndTest — bathtub overflow guide (DEAD)", "publisher": "InspectAndTest", "url": "https://inspectandtest.net/guides/bathtub-overflow-drain/", "tier": "publisher", "status": "dead", "checked": "2026-11-07", "supports": "Removed from all active citations", "note": "HTTP 500 on 2026-11-07. Not linked from any table row; retained here as a labeled documentation row."},
}


def _dual_classified_sentence():
    """Build the B + C-36 sentence from the dataset so the count cannot drift."""
    import json as _json
    from pathlib import Path as _Path
    recs = _json.loads((_Path(__file__).resolve().parents[1] / "data/canonical/cslb_records.json").read_text())["records"]
    dual = [r for r in recs if "C36" in r["classifications"] and "B" in r["classifications"]]
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
             8: "Eight", 9: "Nine", 10: "Ten"}
    word = words.get(len(dual), str(len(dual)))
    source_for = {"829071": "S11", "959843": "S09", "1003394": "S10", "1115649": "S56",
                  "841229": "S57", "1025814": "S64"}
    links = ", ".join(slink(source_for[r["license"]], "#" + r["license"])
                      for r in dual if r["license"] in source_for)
    return "%s verified licences list both B and C-36 on one record: %s. Count and list are read from the committed CSLB dataset." % (word, links)


def pill(text, tone="info"):
    return '<span class="pill %s">%s</span>' % (tone, text)


def slink(sid, label=None):
    s = SOURCES[sid]
    text = label or s["label"]
    url = s["url"]
    if url.startswith("http"):
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (url, text)
    return '<a href="%s">%s</a>' % (url, text)


# New sources for the 2026-11-08 ranking/contact integration are registered here,
# before TABLES and PAGES are defined, so slink() can reference them. The tables,
# pages and appended rows are merged at the end of this file.
import ranking_data as R  # noqa: E402

SOURCES.update(R.SOURCES)

UNVERIFIED = pill("UNVERIFIED", "warn")
BLANK = '<span class="blank" aria-label="blank — unverified">—</span>'
SNAPSHOT = pill("platform snapshot — not re-verified", "warn")

# ---------------------------------------------------------------------------
# Tables. Every row carries at least one source id; the generator renders a
# Source column from those ids. Blank official-verification cells are explicit.
# ---------------------------------------------------------------------------

TABLES = {
    "problem": {
        "title": "Problem snapshot (owner-provided)",
        "columns": ["Item", "Detail as provided", "Official verification", "Provenance", "Source"],
        "rows": [
            {"cells": ["Failed component", "Bathtub wastewater overflow trip lever — stuck inside the hidden plumbing behind the wall", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S14"]},
            {"cells": ["Access problem", "Overflow sits in a hard-to-reach area; more than five licensed plumbers declined to remove it from above for fear of damaging the hidden plumbing", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S18"]},
            {"cells": ["Reported fallback", "Work from below; a storage unit is underneath, so the drywall ceiling may need to be opened to reach the concealed plumbing", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S02"]},
            {"cells": ["Service requirement", "One provider for drywall and plumbing; delicate work in a tenant-occupied unit", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S05"]},
            {"cells": ["Preference", "Removing the overflow from above is preferred if it can be done safely", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S20"]},
            {"cells": ["Location", "San Francisco, California", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S01"]},
            {"cells": ["Pictures", "Owner said reference pictures might be provided; none were supplied to this session", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S45"]},
        ],
        "caption": "All facts in this table come from the owner's project brief, transcribed on the " + slink("S44", "Project brief") + " page. No public source publishes them, so the official-verification column is blank and each row is flagged. Context links in the Source column point to official or manufacturer pages that describe the relevant component or rule — they do not confirm the owner's facts.",
    },
    "estimates": {
        "title": "Estimates received — 2026-08-30",
        "columns": ["#", "Company (identity source)", "Scope as quoted", "Verified amount", "Date", "Verification", "License status", "Source"],
        "rows": [
            {"cells": ["1", "<strong>Expert Plumbing Solutions</strong><br>" + slink("S38", "official site") + " · " + slink("S06", "CSLB #977638"), "Remove bathtub wastewater overflow trip lever — “replacing waste and overflow”", BLANK, "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("C-36 active", "ok")], "src": ["S44", "S06", "S38"]},
            {"cells": ["2", "<strong>Bay Area Plumbing</strong><br>" + slink("S39", "official site") + " · " + slink("S07", "CSLB #757796"), "Replace lever for the bathtub plug and spout with diverter; includes labor and materials", BLANK, "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("C-36 active", "ok")], "src": ["S44", "S07", "S39"]},
            {"cells": ["3", "<strong>Fast Response Plumbing &amp; Rooter</strong><br>" + slink("S40", "official site") + " · " + slink("S08", "CSLB #1024971"), "Repair or adjust bathtub wastewater plunger handle", BLANK, "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("C-36 active", "ok")], "src": ["S44", "S08", "S40"]},
        ],
        "caption": "Amounts are deliberately blank in the Verified amount column: no official source publishes these private quotes. The owner's transcribed figures are retained only on the clearly labeled " + slink("S44", "Project brief") + " page and are listed as unverified on the Flagged for Review page. Company identity and license status are independently verified on CSLB. Nothing is inferred or filled in.",
    },
    "brief_quotes": {
        "title": "Brief transcription — quoted amounts (NOT verified)",
        "columns": ["#", "Company", "Quoted scope (transcription)", "Amount as stated in brief", "Date stated", "Status", "Record type", "Source"],
        "rows": [
            {"cells": ["1", "Expert Plumbing Solutions", "Remove bathtub wastewater overflow trip lever; replacing waste and overflow", "$614", "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("primary record only", "mute")], "src": ["S44", "S06"]},
            {"cells": ["2", "Bay Area Plumbing", "Replace lever for the bathtub plug and spout with diverter, includes labor and materials", "$550", "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("primary record only", "mute")], "src": ["S44", "S07"]},
            {"cells": ["3", "Fast Response", "Repair or adjust bath tub wastewater plunger handle", "$135", "2026-08-30", UNVERIFIED + "<br><small>owner-provided — no official source exists</small>", pill("primary record only", "mute")], "src": ["S44", "S08"]},
        ],
        "caption": "This is a transcription of the owner's brief, not a verification table. These three figures are not used in any officially verified value column anywhere on this site. Source: " + slink("S44", "Project brief") + "; identity cross-checks: " + slink("S06", "CSLB #977638") + ", " + slink("S07", "#757796") + ", " + slink("S08", "#1024971") + ".",
    },
    "benchmarks": {
        "title": "Independent 2026 cost benchmarks",
        "columns": ["Benchmark", "Value as published", "Publisher's own date", "Scope note", "Verification", "Source"],
        "rows": [
            {"cells": ["Bathtub/shower drain replacement — typical range", "<strong>$500–$1,020</strong><br>avg $700 · low $230 · high $1,170", "2026-09-18", "National figure, not a San Francisco quote", pill("verified", "ok")], "src": ["S15"]},
            {"cells": ["Plumber labor rate for drain replacement", "$45–$200 / hour", "2026-09-18", "National figure", pill("verified", "ok")], "src": ["S15"]},
            {"cells": ["New drywall installation (if wall/ceiling opened)", "≈ $2,100", "2026-09-18", "Add-on cost, not part of any received quote", pill("verified", "ok")], "src": ["S15"]},
            {"cells": ["Drain unclogging (if debris also cleared)", "avg $225", "2026-09-18", "Add-on cost", pill("verified", "ok")], "src": ["S15"]},
            {"cells": ["Water damage repair (if a hidden leak is found)", "$1,350–$6,100", "2026-09-18", "Add-on cost", pill("verified", "ok")], "src": ["S15"]},
            {"cells": ["Bathroom leak repair — typical range", "<strong>$150–$600</strong><br>avg $275 · complex up to $4,000", "2026-10-28", "Hidden pipes behind walls raise labor time", pill("verified", "ok")], "src": ["S16"]},
            {"cells": ["Drywall/tile follow-up after a leak", "$300–$930", "2026-10-28", "Add-on cost", pill("verified", "ok")], "src": ["S16"]},
            {"cells": ["Small-job plumber call-out minimum", "$50–$200", "2026-10-28", "Relevant to an adjustment-only visit", pill("verified", "ok")], "src": ["S16"]},
            {"cells": ["Worn-out tub drain replacement (access note)", "avg $700", "2026-10-28", "Publisher notes easier access lowers cost", pill("verified", "ok")], "src": ["S16"]},
            {"cells": ["Overflow component, itemized bathtub installation", "$163", "2026-03-05", "Component cost only, not labor", pill("verified", "ok")], "src": ["S19"]},
            {"cells": ["Typical bathtub drain repairs", "$80–$600", BLANK + " " + UNVERIFIED, "Publisher date not shown on the fetched page; value read directly, date left blank", pill("verified value / date blank", "warn")], "src": ["S22"]},
            {"cells": ["Typical repair duration", "1–4 hours", BLANK + " " + UNVERIFIED, "Publisher date not shown; trade blog, not SF-specific", pill("verified value / date blank", "warn")], "src": ["S22"]},
        ],
        "caption": "Each row links to the publisher's own article — the official source for what that article states. Values were read directly on 2026-11-07. These are national benchmarks, not quotes for this job and not San Francisco price data. Where a publisher date was not visible, the date cell is blank and flagged rather than inferred.",
    },
    "contractors": {
        "title": "San Francisco contractor candidates — official license records",
        "columns": ["Company", "CSLB license", "Classifications on record", "Status / expiry", "Workers' compensation on record", "Address on record", "Analysis (not a vendor claim)", "Verification", "Source"],
        "rows": [
            {"cells": ["<strong>Expert Plumbing Solutions</strong><br>" + slink("S38", "site") + " · " + slink("S32", "Yelp"), slink("S06", "#977638"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2028-10-31", "Insured, policy effective 2026-07-19 → 2027-07-19; $25,000 bond", "1465 44th Avenue, San Francisco, CA 94122", "Quoted the full waste-and-overflow scope; C-36 covers plumbing work", pill("CSLB verified", "ok")], "src": ["S06", "S38", "S05"]},
            {"cells": ["<strong>Bay Area Plumbing</strong><br>" + slink("S39", "site") + " · " + slink("S33", "Yelp"), slink("S07", "#757796"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-01-31", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "335 14th Avenue, San Francisco, CA 94118", "Quoted lever + spout/diverter scope; C-36 covers plumbing work", pill("CSLB verified", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S07", "S39", "S05"]},
            {"cells": ["<strong>Fast Response Plumbing &amp; Rooter</strong><br>" + slink("S40", "site") + " · " + slink("S34", "Yelp"), slink("S08", "#1024971"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-03-31", "Insured, policy effective 2025-12-18 → " + pill("expires 2026-12-18", "warn") + "; $25,000 bond", "236 W POTRAL AVE #459, San Francisco, CA 94127", "Quoted the adjustment scope; site states service to apartments, HOAs and property managers", pill("CSLB verified", "ok") + " " + pill("address mismatch flagged", "warn")], "src": ["S08", "S40", "S05"]},
            {"cells": ["<strong>GENERALSF</strong> (General SF)<br>" + slink("S41", "site") + " · " + slink("S35", "Yelp"), slink("S09", "#959843"), "B General Building · C-10 Electrical · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-04-30", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "3624 Irving Street Ste A, San Francisco, CA 94122", "One license lists both building and plumbing classifications — matches the single-provider requirement", pill("CSLB verified", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S09", "S41", "S05"]},
            {"cells": ["<strong>Handyman Heroes Inc</strong><br>" + slink("S42", "site") + " · " + slink("S36", "Yelp"), slink("S10", "#1003394"), "B General Building · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-05-31", "Insured, policy effective 2026-04-25 → 2027-04-25; $25,000 bond", "912 Cole St # 202, San Francisco, CA 94117", "One license lists building + plumbing; official CSLB complaint disclosure exists", pill("CSLB verified", "ok") + " " + pill("disclosure flagged", "warn")], "src": ["S10", "S12", "S42"]},
            {"cells": ["<strong>Ace Plumbing &amp; Rooter Inc</strong><br>" + slink("S43", "site"), slink("S11", "#829071"), "A · B · C-4 · C-10 · C-16 · C-36", pill("current and active", "ok") + "<br>expires 2027-06-30", "Insured, policy effective 2026-07-13 → 2027-07-13; $25,000 bond", "1090 Bryant Street, San Francisco, CA 94103-4417", "Broadest verified classification set including B + C-36; site describes HOA/property-manager service", pill("CSLB verified", "ok")], "src": ["S11", "S43", "S05"]},
            {"cells": ["<strong>Rapid Flow Plumbing &amp; Rooter Inc</strong><br>" + slink("S58", "shortlist"), slink("S56", "#1115649"), "B General Building · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2028-01-31", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "230 Edinburgh St, San Francisco, CA 94112", "One license lists building + plumbing; added from the concurrent shortlist session and re-verified here", pill("CSLB verified", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S56", "S05", "S58"]},
            {"cells": ["<strong>Manny's Plumbing &amp; Rooter</strong><br>" + slink("S58", "shortlist"), slink("S57", "#841229"), "C-36 Plumbing · B General Building", pill("current and active", "ok") + "<br>expires 2028-06-30", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "41 Midvale Drive, Daly City, CA 94015", "One license lists plumbing + building; address is outside San Francisco proper — confirm service area", pill("CSLB verified", "ok") + " " + pill("service area flagged", "warn")], "src": ["S57", "S05", "S58"]},
        ],
        "caption": "Every license fact (status, classifications, expiry, bond, workers' compensation, address) was read from the linked official CSLB License Detail page on 2026-11-07; each record printed a 'Data current as of 11/7/2026' stamp. The Analysis column is this site's reasoning from those verified classifications — not a vendor promise and not a finding that any firm can perform this specific repair. C-36 definition: " + slink("S05", "CSLB C-36") + ". Re-check any license at " + slink("S04", "CSLB Check a License") + " on the hire date. <strong>Update 2026-11-08:</strong> all sixteen license records cited in this project were re-read directly on CSLB and every one is current and active; eight further licensees are added below, and the full field-by-field transcription with the official business phone numbers is on <a href=\"contacts.html\">Contacts &amp; licenses</a>. The computed order is on <a href=\"ranking.html\">Ranked hiring decision</a>.",
    },
    "review_snapshots": {
        "title": "Review-platform snapshots (not independently verified)",
        "columns": ["Candidate", "Prior-session Yelp snapshot (2026-11-06)", "Re-check 2026-11-07", "Official license source", "Status", "Source"],
        "rows": [
            {"cells": ["Expert Plumbing Solutions", "4.8 ★ (81 reviews)", BLANK + " " + UNVERIFIED, slink("S06", "CSLB #977638"), SNAPSHOT], "src": ["S32", "S06"]},
            {"cells": ["Bay Area Plumbing", "4.8 ★ (175 reviews)", BLANK + " " + UNVERIFIED, slink("S07", "CSLB #757796"), SNAPSHOT], "src": ["S33", "S07"]},
            {"cells": ["Fast Response Plumbing &amp; Rooter", "4.8 ★ (906 reviews)", BLANK + " " + UNVERIFIED, slink("S08", "CSLB #1024971"), SNAPSHOT], "src": ["S34", "S08"]},
            {"cells": ["GENERALSF", "4.8 ★ (336 reviews)", BLANK + " " + UNVERIFIED, slink("S09", "CSLB #959843"), SNAPSHOT], "src": ["S35", "S09"]},
            {"cells": ["Handyman Heroes Inc", "4.7 ★ (410 reviews)", BLANK + " " + UNVERIFIED, slink("S10", "CSLB #1003394"), SNAPSHOT], "src": ["S36", "S10"]},
            {"cells": ["Szeto Plumbing and Handyman (Daly City)", "4.8 ★ (89 reviews)", BLANK + " " + UNVERIFIED, BLANK + " " + pill("no CSLB record found", "warn"), SNAPSHOT], "src": ["S37", "S04"]},
            {"cells": ["Fast Response — company's own aggregate claim", "“4.9 · 1,500 Reviews on Yelp &amp; Google”", BLANK + " " + UNVERIFIED, slink("S08", "CSLB #1024971"), pill("company claim — flagged", "warn")], "src": ["S40", "S34"]},
        ],
        "caption": "Yelp blocks automated access with HTTP 403 in this environment, so no rating could be confirmed from the platform on 2026-11-07. The left column reproduces a 2026-11-06 snapshot recorded by an earlier session; the re-check column is blank and flagged. Review counts change daily. Platform badges and company aggregates are not CSLB license verification. See the Flagged for Review page.",
    },
    "platforms": {
        "title": "Where to look for reviews of this specific work in San Francisco",
        "columns": ["Platform", "San Francisco link for this work type", "What the page provides (as read)", "Verification", "Source"],
        "rows": [
            {"cells": ["Yelp — Bathtub Repair", slink("S29", "Bathtub Repair in San Francisco"), "Category search for the exact repair type", pill("HTTP 403 on automated fetch — manual review link", "warn")], "src": ["S29"]},
            {"cells": ["Yelp — Plumbers", slink("S30", "Plumbers in San Francisco"), "General plumbing category with business reviews", pill("HTTP 403 — manual review link", "warn")], "src": ["S30"]},
            {"cells": ["Yelp — Drywall Installation &amp; Repair", slink("S31", "Drywall Installation &amp; Repair in San Francisco"), "Category search for the drywall half of the combined scope", pill("HTTP 403 — manual review link", "warn")], "src": ["S31"]},
            {"cells": ["Angi — plumbers", slink("S23", "Best plumbers in San Francisco, CA"), "873 verified plumbing reviews; page last updated 2026-08-01", pill("read directly 2026-11-07", "ok")], "src": ["S23"]},
            {"cells": ["Angi — bathtub restoration", slink("S24", "Bathtub restoration pros in San Francisco"), "SF bathtub-specific reviews, including a multi-unit tenant-occupied plumbing + drywall project", pill("read directly 2026-11-07", "ok")], "src": ["S24"]},
            {"cells": ["BuildZoom — plumbers", slink("S25", "Plumbers in San Francisco, CA"), "Client reviews, verified projects, permit/license-derived profiles; 683 experts listed", pill("read directly 2026-11-07", "ok")], "src": ["S25"]},
            {"cells": ["BuildZoom — drywall", slink("S26", "Drywall and plaster contractors in San Francisco"), "Drywall/plaster directory with reviews and project photos; 83 experts listed", pill("read directly 2026-11-07", "ok")], "src": ["S26"]},
            {"cells": ["Thumbtack — bathtub services", slink("S27", "Bathtub services near San Francisco, CA"), "Bathtub-service listings with customer reviews and 'Licensed pro' badges", pill("read directly 2026-11-07", "ok") + " " + pill("badge ≠ CSLB", "warn")], "src": ["S27"]},
            {"cells": ["BBB — business profile", slink("S28", "Expert Plumbing Solutions profile"), "Accreditation status, complaint history, license number on record", pill("read directly 2026-11-07", "ok")], "src": ["S28"]},
            {"cells": ["CSLB — official license lookup", slink("S04", "Check a License"), "Definitive license status, classifications, bond, workers' comp, complaint disclosure", pill("official", "ok")], "src": ["S04"]},
        ],
        "caption": "Platform links are discovery aids, not proof that any firm can perform this delicate repair. Only " + slink("S04", "CSLB") + " verifies a California contractor license. Specific-work review text found on " + slink("S24", "Angi's SF bathtub page") + " is a customer statement and is not treated as an official capability finding.",
    },
    "requirements": {
        "title": "Requirements register — line by line",
        "columns": ["#", "Requirement as stated", "Category", "Officially confirmed value", "Status", "Source"],
        "rows": [
            {"cells": ["R01", "Collect, organize and analyze a full list of requirements", "Project scope", BLANK + " " + UNVERIFIED, pill("implemented on this page", "ok")], "src": ["S44", "S45"]},
            {"cells": ["R02", "Create an executive summary outlining important details", "Deliverable", BLANK + " " + UNVERIFIED, pill("implemented", "ok") + " — " + "<a href=\"summary.html\">Executive summary</a>"], "src": ["S44", "S46"]},
            {"cells": ["R03", "Problem: bathtub overflow in a hard-to-access area; may require opening drywall to reach the plumbing", "Problem", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S02"]},
            {"cells": ["R04", "Remove the bathtub wastewater overflow trip lever", "Scope of work", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S14"]},
            {"cells": ["R05", "Estimate dated 8/30/26 — Expert Plumbing Solutions — replacing waste and overflow — $614", "Estimate", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S06"]},
            {"cells": ["R06", "Estimate dated 8/30/26 — Bay Area Plumbing — replace lever for bathtub plug and spout with diverter, labor and materials — $550", "Estimate", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S07"]},
            {"cells": ["R07", "Estimate dated 8/30/26 — Fast Response — $135 for repair or adjust bathtub wastewater plunger handle", "Estimate", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S08"]},
            {"cells": ["R08", "Find someone who can perform the work we need", "Objective", BLANK + " " + UNVERIFIED, pill("candidates on Contractors page", "ok")], "src": ["S44", "S04"]},
            {"cells": ["R09", "Removing the overflow from above is preferred if possible", "Preference", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S18"]},
            {"cells": ["R10", "Over five licensed plumbers could not remove it from above without concern over damaging hidden plumbing", "Constraint", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S21"]},
            {"cells": ["R11", "Plumbers recommend working from below; a storage unit is below and the drywall ceiling may need opening", "Access", BLANK + " " + UNVERIFIED, pill("owner-provided", "info")], "src": ["S44", "S02"]},
            {"cells": ["R12", "One all-in-one service covering drywall and plumbing", "Service requirement", slink("S09", "#959843") + ", " + slink("S10", "#1003394") + ", " + slink("S11", "#829071") + ", " + slink("S56", "#1115649") + ", " + slink("S57", "#841229") + " list B + C-36 combinations", pill("license classes verified", "ok") + " " + pill("job capability unverified", "warn")], "src": ["S44", "S09", "S10", "S11", "S56", "S57"]},
            {"cells": ["R13", "Look on Yelp and other review services for this specific type of work in San Francisco", "Research", BLANK + " " + UNVERIFIED, pill("platforms table on Contractors page", "ok")], "src": ["S44", "S23", "S25", "S27"]},
            {"cells": ["R14", "Provider should be a licensed plumber or licensed contractor", "Provider", slink("S04", "CSLB Check a License") + " verifies California licenses", pill("official rule source linked", "ok")], "src": ["S44", "S04", "S05", "S13"]},
            {"cells": ["R15", "Provider must service our area (San Francisco)", "Provider", slink("S06", "CSLB #977638") + " and other records list San Francisco addresses", pill("addresses verified on CSLB", "ok")], "src": ["S44", "S06", "S07", "S08"]},
            {"cells": ["R16", "Experience with delicate work in a sensitive, tenant-occupied unit", "Environment", BLANK + " " + UNVERIFIED, pill("not confirmable from an official source", "warn")], "src": ["S44", "S24", "S40"]},
            {"cells": ["R17", "Reference pictures may be supplied; work from the description if absent", "Input", BLANK + " " + UNVERIFIED, pill("no pictures received", "warn")], "src": ["S44", "S45"]},
            {"cells": ["R18", "No manual input from the owner; complete all tasks autonomously", "Process", BLANK + " " + UNVERIFIED, pill("executed by this integration session", "ok")], "src": ["S44", "S45"]},
            {"cells": ["R19", "Review the repo, verify from official trusted sources, provide links for manual review, flag irregularities", "Repo work", BLANK + " " + UNVERIFIED, pill("Repo review + Verification pages", "ok")], "src": ["S44", "S45", "S47"]},
            {"cells": ["R20", "Create a GitHub Pages live site with a clean landing page, category subpages and table-format entries/findings", "Site", slink("S46", "Live site root"), pill("implemented", "ok")], "src": ["S44", "S46"]},
            {"cells": ["R21", "Every table row has an official source link; unconfirmable values are blank and flagged", "Verification", BLANK + " " + UNVERIFIED, pill("not fully enforced — see U21", "warn")], "src": ["S44", "S45"]},
            {"cells": ["R22", "Parallel sessions must coordinate via COORDINATION.md on non-overlapping scopes", "Coordination", slink("S45", "Shared board"), pill("claim committed and pushed", "ok")], "src": ["S44", "S45"]},
            {"cells": ["R23", "Publish flagged irregularities and unverified items on a clearly labeled Flagged for Review page", "Site", BLANK + " " + UNVERIFIED, pill("Flagged for Review page", "ok")], "src": ["S44", "S46"]},
            {"cells": ["R24", "Create a PR to main, merge it, confirm GitHub Pages deploys, record PR link and result", "Delivery", BLANK + " " + UNVERIFIED, pill("recorded on Verification + board", "ok")], "src": ["S44", "S45"]},
        ],
        "caption": "Requirements are transcribed from the owner's brief (" + slink("S44") + "). The 'Officially confirmed value' column is blank wherever no official source can confirm the requirement; the Source column always links the primary record plus the relevant official page. Internal-only instructions are intentionally absent from this register — see the Verification page's privacy note.",
    },
    "technical": {
        "title": "Technical background — bathtub waste-and-overflow trip lever",
        "columns": ["Topic", "What the source states", "Relevance to this job", "Verification", "Source"],
        "rows": [
            {"cells": ["Trip-lever mechanism", "The trip lever operates a hidden linkage behind the tub wall connected to the stopper; diagnosis starts by removing the overflow cover plate and inspecting the links", "Explains why a seized linkage is not visible from the tub side", pill("verified", "ok")], "src": ["S21", "S17"]},
            {"cells": ["Bath waste-and-overflow parts", "Drain shoe, linkage assembly, overflow plate and trap form the system; the overflow plate is a safety feature", "Defines the concealed assembly at issue", pill("verified", "ok")], "src": ["S18", "S17"]},
            {"cells": ["Above-access removal", "Remove the two screws in the overflow plate and pull the plate away; the upper linkage should follow", "Supports the preferred from-above approach when the linkage is free", pill("verified", "ok")], "src": ["S18", "S20"]},
            {"cells": ["Stuck / corroded drains", "For stubborn drains, access the plumbing from below the tub; extreme cases may require cutting out old drain components from below", "Explains why five-plus plumbers recommended below access", pill("verified", "ok")], "src": ["S18"]},
            {"cells": ["Below-access assembly", "Installing a new kit requires aligning the rubber gasket and drain elbow from below while a helper holds the shoe from above", "Concealed work usually needs an opening or access panel", pill("verified", "ok")], "src": ["S18"]},
            {"cells": ["Replacement kit", "Oatey publishes a full 'Dearborn Plastic Tubular Trip-Lever Bath Waste' kit with a chrome-finish stopper", "Confirms the component type is a standard manufactured assembly", pill("manufacturer", "ok")], "src": ["S14"]},
            {"cells": ["Overflow function", "The overflow directs excess water into a concealed channel connected to the drain; traditional and integral types exist", "Distinguishes the overflow plate from the trip-lever linkage", pill("verified", "ok")], "src": ["S17"]},
            {"cells": ["Testing after replacement", "Trade guidance describes a hydrostatic / fill-and-inspect test of the drain and overflow connections", "Plan access to the space below for a water test", pill("verified", "ok")], "src": ["S22"]},
        ],
        "caption": "All technical statements are linked to the publisher or manufacturer page they were read from on 2026-11-07. These sources describe typical assemblies and procedures; none of them inspected this specific bathtub, and none is San Francisco code guidance.",
    },
    "permits": {
        "title": "Official permit and licensing references (neutral)",
        "columns": ["Topic", "Official text / fact", "Applies to this project", "Grade", "Source"],
        "rows": [
            {"cells": ["Plumbing permit requirement", "“You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground.”", "Replacement of concealed waste-and-overflow piping is the scope described by the rule", pill("official — sf.gov", "ok")], "src": ["S01"]},
            {"cells": ["Exempt-work pointer", "SF.gov points to San Francisco Plumbing Code Section 104.2 for exemptions; the official code library hosts Section 104.0 Permits", "Link provided for manual review of exemption wording", pill("official", "ok")], "src": ["S01", "S03"]},
            {"cells": ["Work exempt from a building permit", "SF.gov lists “minor repairs to existing interior plaster or wallboard, unless they are required for fire protection” among work that does not need a permit", "Relevant to the ceiling-opening / patching discussion", pill("official — sf.gov", "ok")], "src": ["S02"]},
            {"cells": ["Who may apply for a plumbing permit", "Contractors must hold C-4, C-16, C-20, C-36, C-54, B or A classifications; scope may be further limited by license type", "Matches the requirement for a licensed plumber or contractor", pill("official — sf.gov", "ok")], "src": ["S01", "S05"]},
            {"cells": ["Inspection before covering", "After a permit is issued, work must be inspected before covering pipes", "Sequencing consideration if a ceiling is opened and re-closed", pill("official — sf.gov", "ok")], "src": ["S01"]},
            {"cells": ["Homeowner route", "Only owners of stand-alone single-family dwellings (R-3) may apply to do the work themselves", "Tenant-occupied multi-unit context should be checked directly with SF DBI", pill("official — sf.gov", "ok")], "src": ["S01"]},
            {"cells": ["Small-job licensing exemption", "B&amp;P §7048 exempts work only when the aggregate price is under $1,000, the work is casual/minor/inconsequential, and no building permit is required (as amended by AB 1170, effective 2026-01-01)", "Current statutory text; widely repeated older $500 figures are outdated", pill("official — leginfo", "ok")], "src": ["S13"]},
            {"cells": ["Kitchen/bath permit route",
                        "DBI: “You need a permit before renovating and replacing kitchen or bath fixtures.” The online route is limited to work that does not remove or move walls, is in an R-2 or R-3 building, and remodels a legally permitted kitchen or bath. Related electrical and plumbing permits are applied for separately. Only property owners and licensed B contractors may apply for the kitchen/bath permit itself.",
                        "Reported as published. A plumbing-only firm would take the plumbing permit route instead; this page draws no conclusion about which route fits this job.",
                        pill("official — sf.gov", "ok")],
             "src": ["S94", "S01"]},
            {"cells": ["Specialty contractor and other trades",
                        "B&amp;P §7059(a): a specialty contractor may take and execute a contract involving two or more crafts or trades if the work outside its own trade is “incidental and supplemental” to the licensed craft. A B contractor may not take a prime contract for non-framing trades unless the contract requires two unrelated trades or it holds the specialty licence or subcontracts it out (§7057(b)).",
                        "Reported as published. Whether a ceiling cut-and-patch counts as incidental and supplemental to C-36 plumbing is not determined here and should be confirmed in writing with the contractor and DBI.",
                        pill("official — leginfo / CSLB", "ok")],
             "src": ["S62", "S83", "S05"]},
            {"cells": ["Covering work before inspection",
                        "DBI: after a permit is issued, have the plumbing or mechanical work “inspected … before covering pipes”. The kitchen/bath route adds that final inspections cannot be scheduled until the related plumbing work has passed final inspection.",
                        "Sequencing note only, for the case in which a ceiling is opened and re-closed.",
                        pill("official — sf.gov", "ok")],
             "src": ["S01", "S94"]},
            {"cells": ["Confirm applicability", "SF.gov lists the Permit Center help desk and permitsf@sfgov.org as contacts", "The hiring party should confirm permit applicability for the exact scope with SF DBI and the contractor", pill("official — sf.gov", "ok")], "src": ["S01"]},
        ],
        "caption": "This page reports official requirements only. It contains no instruction, request or recommendation about obtaining or not obtaining a permit, and it records no private project rationale. Confirm the final scope with SF DBI and the selected licensed contractor. Nothing here is legal advice.",
    },
    "findings": {
        "title": "Analysis and findings",
        "columns": ["#", "Finding", "Basis (verified sources)", "Status", "Source"],
        "rows": [
            {"cells": ["F01", "Three quotes bracket three different scopes: adjustment, stopper/spout replacement, and full waste-and-overflow replacement", "Owner brief scopes; Angi's replacement range $500–$1,020 and leak-repair range $150–$600", pill("analysis", "info") + " " + pill("amounts unverified", "warn")], "src": ["S44", "S15", "S16"]},
            {"cells": ["F02", "Below-access is the documented norm when above-access fails on a seized assembly", "This Old House: stubborn drains may need access from below; new kits are aligned from below", pill("analysis supported by publisher", "ok")], "src": ["S18", "S21"]},
            {"cells": ["F03", "A single license can cover both building/drywall and plumbing work", "CSLB #959843 (B + C10 + C36), #1003394 (B + C36), #829071 (A + B + C36 among others)", pill("license classes verified", "ok") + " " + pill("job capability unverified", "warn")], "src": ["S09", "S10", "S11"]},
            {"cells": ["F04", "All eight verified candidates hold active CSLB licenses checked 2026-11-07", "Eight official License Detail pages each print 'current and active'", pill("verified", "ok")], "src": ["S06", "S07", "S08", "S09", "S10", "S11", "S56", "S57"]},
            {"cells": ["F05", "Drywall/ceiling work is not included in any of the three quoted scopes", "Owner brief scopes; Angi lists new drywall ≈ $2,100 and post-leak patching $300–$930 as separate costs", pill("analysis", "info") + " " + pill("no drywall quote exists", "warn")], "src": ["S44", "S15", "S16"]},
            {"cells": ["F06", "Four licenses show a workers'-compensation exemption 'no employees', and one policy expires 2026-12-18", "CSLB #757796, #959843, #1115649, #841229, #1024971", pill("verified on CSLB", "ok") + " " + pill("flagged", "warn")], "src": ["S07", "S09", "S56", "S57", "S08"]},
            {"cells": ["F07", "Review counts and badges are not license verification", "Yelp HTTP 403; Thumbtack 'Licensed pro' badge; BBB states it does not verify third-party information; CSLB is the authority", pill("verified sources", "ok")], "src": ["S04", "S27", "S28", "S29"]},
            {"cells": ["F08", "Occupied-unit / property-manager experience is only partially documented", "Fast Response site (apartments, HOAs, property managers), Ace site (HOAs/property managers), Angi SF review mentions a tenant-occupied multi-unit project", pill("company/review statements only", "warn")], "src": ["S40", "S43", "S24"]},
            {"cells": ["F09", "Two previously cited sources are dead and were removed from all active claims", "SFGate redirect to empty page; InspectAndTest HTTP 500 — both re-checked 2026-11-07", pill("irregularity — flagged", "warn")], "src": ["S55", "S45"]},
            {"cells": ["F10", "The repository's root content belongs to an unrelated legacy project", "README describes a DOE GEMS fault-prospectivity audit; legacy site remains under docs/", pill("irregularity — flagged", "warn")], "src": ["S47", "S48"]},
            {"cells": ["F11", "Recommended shortlist order: firms whose verified classes cover both building and plumbing first", _dual_classified_sentence(), pill("recommendation", "info")], "src": ["S11", "S09", "S10", "S56", "S57", "S64", "S58"]},
        ],
        "caption": "Findings marked 'analysis' are this site's reasoning from the cited verified sources; they are not vendor claims, quotes, or official determinations. Values that could not be confirmed from an official source remain blank on the data pages and are listed on the Flagged for Review page.",
    },
    "flagged": {
        "title": "Flagged for Review — unverified values and irregularities",
        "columns": ["ID", "Item", "Why it is flagged", "What would clear it", "Status", "Source"],
        "rows": [
            {"cells": ["U01", "Three estimate amounts ($614, $550, $135) and all owner-provided problem facts", "No official or public source publishes private quotes or the owner's description; officially verified value cells are blank", "Attach the original written quotes and photos as project documents, then re-verify", UNVERIFIED], "src": ["S44", "S06", "S07", "S08"]},
            {"cells": ["U02", "Estimate scope wording and dates", "Transcribed from the brief only", "Supply the original quote documents", UNVERIFIED], "src": ["S44", "S45"]},
            {"cells": ["U03", "Yelp ratings and review counts", "Direct Yelp fetch returns HTTP 403 on 2026-11-07; only a 2026-11-06 prior-session snapshot exists", "Open the linked Yelp pages manually on the decision date", UNVERIFIED], "src": ["S29", "S32", "S33", "S34"]},
            {"cells": ["U04", "Fast Response address mismatch", "Yelp listing shows 4444 Geary Blvd Ste 203 (prior snapshot); official CSLB #1024971 shows 236 W POTRAL AVE #459", "Ask the company which is the service vs mailing address", pill("irregularity", "warn")], "src": ["S08", "S34", "S40"]},
            {"cells": ["U05", "Fast Response workers'-compensation policy expires 2026-12-18", "CSLB #1024971 shows a policy with that expiry date; re-check on the hire date", "Request a current certificate of insurance", pill("verified fact / time-sensitive", "warn")], "src": ["S08"]},
            {"cells": ["U06", "Workers'-compensation exemptions on #757796, #959843, #1115649 and #841229", "All four CSLB records state the licensee certified 'no employees at this time'", "Confirm in writing who will be on site and what coverage applies to the crew", pill("verified fact / needs review", "warn")], "src": ["S07", "S09", "S56", "S57"]},
            {"cells": ["U07", "Handyman Heroes CSLB complaint disclosure", "CSLB shows citation 2 2020 001045 dated 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6' — reported verbatim, no interpretation", "Open the official disclosure yourself and decide before hiring", pill("verified fact / needs review", "warn")], "src": ["S12", "S10"]},
            {"cells": ["U08", "Handyman Heroes site claims 'Licensed C-10'", "The official CSLB #1003394 record lists B and C-36 only", "Ask the company which license covers electrical work", pill("irregularity", "warn")], "src": ["S42", "S10"]},
            {"cells": ["U09", "Fast Response company aggregate '4.9 / 1,500 Reviews on Yelp &amp; Google'", "Company self-claim combining two platforms; Yelp page could not be re-fetched", "Re-open each platform separately", pill("irregularity", "warn")], "src": ["S40", "S34"]},
            {"cells": ["U10", "Szeto Plumbing and Handyman — license not found", "A prior session's CSLB name search on 2026-11-06 found no record; not re-verified on 2026-11-07, and the business is in Daly City with a 310 area code", "Ask for a CSLB number and verify it directly, or drop the candidate", pill("unverified", "warn")], "src": ["S37", "S04"]},
            {"cells": ["U11", "Two dead source URLs from earlier sessions", "SFGate Home Guides redirects to an empty page; InspectAndTest returns HTTP 500 (both re-checked 2026-11-07)", "Removed from all active citations; retained only as labeled documentation rows on the Source ledger", pill("resolved / documented", "ok")], "src": ["S55", "S45"]},
            {"cells": ["U12", "Repository content mismatch", "The README and docs/ describe an unrelated DOE GEMS fault-prospectivity audit; this dashboard occupies the site root", "No action required; legacy files deliberately untouched", pill("irregularity", "warn")], "src": ["S47", "S48"]},
            {"cells": ["U13", "Stale conflicting PR #32 from a parallel session", "Open since 2026-11-06, mergeable=CONFLICTING, also touches index.html; left untouched and not merged or closed by this session", "Owner may close or rebase it after this integration", pill("needs review", "warn")], "src": ["S52", "S45"]},
            {"cells": ["U14", "No combined written quote for plumbing + drywall exists", "No official or company source publishes a combined scope for this job", "Request one contingent written scope covering above-attempt, below access, ceiling cut/patch/finish and tenant coordination", UNVERIFIED], "src": ["S44", "S15", "S16"]},
            {"cells": ["U16", "Yelp “Verified License” badges are third-party", "A platform badge is not CSLB verification; Yelp returned HTTP 403 on re-check", "Verify the license number directly on CSLB", pill("irregularity", "warn")], "src": ["S36", "S04", "S29"]},
            {"cells": ["U17", "Handyman Heroes address mismatch", "Official CSLB #1003394 lists 912 Cole St # 202; the prior Yelp snapshot lists 1525 Waller St", "Ask the company for its current service address", pill("irregularity", "warn")], "src": ["S10", "S36"]},
            {"cells": ["U18", "Outdated $500 contractor-licensing references", "Widely repeated older $500 figures are outdated; current B&amp;P §7048 (AB 1170, effective 2026-01-01) uses under $1,000 and no building permit required", "Use the current statutory text linked here", pill("resolved / documented", "ok")], "src": ["S13"]},
            {"cells": ["U19", "Repository scope: earlier research sets are historical", "Earlier dashboards under docs/ and bathtub-overflow/ are archived. A previously reported legacy link docs/parallel-index.html → docs/results/ resolves; no change made", "No action required; historical pages untouched", pill("needs review", "warn")], "src": ["S45", "S47", "S48"]},
            {"cells": ["U20", "No provider was contacted during this desk-research session", "The owner reported prior estimates; this research session did not contact providers or independently confirm job-specific scope, current price or availability", "Contact shortlisted firms with the written scope", UNVERIFIED], "src": ["S44", "S45", "S58"]},
            {"cells": ["U22", "License classifications do not establish the only possible repair arrangement", "B + C-36 is a useful screening signal, not proof of acceptance or an exclusive route. BPC §7059 allows qualifying incidental and supplemental work by specialty contractors; application to this ceiling is not established. The archived docs/overflow-verification.html contains more categorical statements that omit this qualification", "Ask each contractor for a written scope, responsible trades and confirmation of applicable requirements", UNVERIFIED], "src": ["S62", "S58", "S63"]},
            {"cells": ["U21", "Official-source coverage and automated verification limits", "Some rows cite only publishers, platforms or internal project records, not government sources; source-link checks do not establish truth, relevance or live availability. Prior verification dates are historical.", "Review each row and its cited source manually; do not treat a generic official link as proof of unrelated facts", UNVERIFIED], "src": ["S04", "S45"]},
            {"cells": ["U15", "Job-specific capability, tenant-occupied experience and service-area confirmation", "CSLB verifies license classes, not the ability to perform this specific delicate repair; company sites and reviews are self- or customer statements", "Ask each shortlisted firm for references on concealed waste-and-overflow work in occupied units", UNVERIFIED], "src": ["S04", "S24", "S40", "S43"]},
        ],
        "caption": "Flagged items do not block the site, the analysis, or the merge. They are published here, with their source links, so they can be reviewed after the site is live. Blank means unconfirmed — nothing was inferred to fill a gap.",
    },
    "repo_review": {
        "title": "Repository review — line by line",
        "columns": ["Area", "What was found", "Verification", "Result", "Source"],
        "rows": [
            {"cells": ["Root", "A prior session published a 7-page dashboard (index, summary, estimates, contractors, findings, sources, flagged) at the site root", "Files read locally 2026-11-07; this integration replaces them with a 13-page canonical dashboard", pill("reviewed", "ok")], "src": ["S46", "S45"]},
            {"cells": ["Legacy project", "README documents a DOE GEMS geothermal fault-prospectivity submission audit with GeoTIFF datasets under data/, docs/, vendor/, gems/, evidence/, registry/", "README read locally; legacy content is unrelated to the bathtub project and is untouched", pill("irregularity", "warn")], "src": ["S47", "S48"]},
            {"cells": ["Parallel microsites", "bathtub-overflow/, docs/bath/, docs/overflow-*.html and docs/plumbing-index.html contain earlier, partly overlapping research", "Linked as archive; files not edited", pill("reviewed", "ok")], "src": ["S49", "S50", "S51"]},
            {"cells": ["Coordination board", "COORDINATION.md contains 548 lines from six prior sessions with claims, handoffs and a verification log", "Read at session start; this session appended its own board section and pushed the claim", pill("reviewed", "ok")], "src": ["S45"]},
            {"cells": ["Prior compliance gap", "The earlier root estimates table displayed owner-provided amounts in value cells and had rows with no source links", "Reproduced by a local row-link audit; fixed in this build (blank verified cells, every row linked)", pill("fixed", "ok")], "src": ["S45", "S44"]},
            {"cells": ["Dead external links", "Earlier pages cited homeguides.sfgate.com and inspectandtest.net; both fail on re-check", "Removed from active citations; retained as labeled documentation rows", pill("fixed / flagged", "warn")], "src": ["S55", "S45"]},
            {"cells": ["Open PR", "PR #32 from a parallel session is open and conflicting", "Checked with gh; not merged, not closed, not edited", pill("needs review", "warn")], "src": ["S52"]},
            {"cells": ["Pages configuration", "GitHub Pages builds from branch main, path / (legacy build type); .nojekyll is present at the repo root", "Confirmed with gh api repos/.../pages on 2026-11-07", pill("verified", "ok")], "src": ["S46"]},
            {"cells": ["Tests / scripts", "Existing Python scripts and tests belong to the legacy GEMS project; pytest is not installed in this sandbox", "This session added standalone unittest-based dashboard checks runnable with python3", pill("reviewed", "ok")], "src": ["S47"]},
            {"cells": ["Privacy sweep", "A grep for internal-only hiring constraints across all published HTML/MD/JSON/CSS/JS returned zero matches", "See the Verification page for the exact pattern list and result", pill("pass", "ok")], "src": ["S45"]},
            {"cells": ["Concurrent session output", "shortlist.html (ranked B + C-36 candidates and vetting script), verification-log.html (earlier line-by-line log) and sf-overflow-audit/ (independent 9-page audit) were merged and preserved; shortlist wording was clarified 2026-11-08", "All three are linked from the dashboard navigation, quick links and this review page", pill("preserved", "ok")], "src": ["S58", "S59", "S60", "S45"]},
        ],
        "caption": "Repo review was performed by reading the files in the checkout and querying the GitHub API. Links point to the repository files and Pages site for manual review. Irregularities are also published on the Flagged for Review page.",
    },
    "source_ledger": {
        "title": "Source ledger — all sources with verification status",
        "columns": ["ID", "Source", "Publisher / tier", "Status", "What it supports", "Source"],
        "rows": [],  # generated by build_dashboard.py from SOURCES
        "caption": "Every external URL used on this dashboard is listed here with its publisher, tier, retrieval date and verification status. 'dead' sources are never linked from a table row; their URL is shown as plain text for documentation only.",
    },
}

PAGES = {
    "index.html": {
        "title": "Dashboard",
        "eyebrow": "Research dashboard · San Francisco · updated 2026-11-07",
        "h1": "Bathtub wastewater overflow trip lever",
        "lede": "A stuck trip lever in concealed plumbing behind the wall. From-above removal is preferred but has not been achievable; the reported fallback is access from below through a storage-unit ceiling. This dashboard organizes the requirements, three estimates, verified contractor records, review platforms, cost benchmarks, official rules, and every item that still needs review.",
        "sections": [
            {"type": "cards", "items": [
                {"k": "Estimates received", "v": "3", "s": "2026-08-30 · amounts owner-provided (unverified)", "tone": "warn"},
                {"k": "Verified license records", "v": "16", "s": "All re-read on CSLB 2026-11-08 · 6 hold plumbing + building", "tone": "ok"},
                {"k": "Verified official sources", "v": "AUTO_OFFICIAL", "s": "Ledger entries graded official/manufacturer; direct reads dated per source", "tone": "info"},
                {"k": "Flagged for review", "v": "AUTO_FLAGS", "s": "Unverified values and irregularities — none blocking", "tone": "warn"},
            ]},
            {"type": "table", "title": "Problem snapshot", "ref": "problem"},
            {"type": "quick", "title": "Browse by category", "items": [
                {"href": "ranking.html", "t": "Ranked hiring decision", "d": "Every candidate ranked best-to-worst on verified CSLB facts, with reasoning and cost position."},
                {"href": "contacts.html", "t": "Contacts & licenses", "d": "Official business links, verified phone numbers and all 16 license records."},
                {"href": "summary.html", "t": "Executive summary", "d": "Important details, key findings and next steps."},
                {"href": "requirements.html", "t": "Requirements", "d": "The full brief, line by line, with verification status."},
                {"href": "estimates.html", "t": "Estimates & costs", "d": "The three quotes, blank verified cells, and 2026 cost benchmarks."},
                {"href": "contractors.html", "t": "Contractors & reviews", "d": "CSLB-verified licenses, Yelp/Angi/BuildZoom/Thumbtack/BBB discovery links."},
                {"href": "findings.html", "t": "Findings & analysis", "d": "Access options, one-provider shortlist, cost and occupied-unit analysis."},
                {"href": "shortlist.html", "t": "Shortlist (prior session)", "d": "Earlier ranked dual-classified list and vetting script, preserved unchanged."},
                {"href": "technical.html", "t": "Technical background", "d": "How a trip-lever waste-and-overflow assembly works and how it is accessed."},
                {"href": "permits.html", "t": "Permits & licensing", "d": "Neutral, official sf.gov / CSLB / state-law references."},
                {"href": "brief.html", "t": "Project brief", "d": "Owner-provided primary record and quoted amounts (unverified)."},
                {"href": "sources.html", "t": "Source ledger", "d": "Every source, publisher, tier, status and retrieval date."},
                {"href": "verification.html", "t": "Verification", "d": "Line-by-line row audit, link check, privacy sweep and build results."},
                {"href": "repo-review.html", "t": "Repo review", "d": "What is in this repository and what was irregular."},
                {"href": "verification-log.html", "t": "Prior verification log", "d": "Line-by-line log preserved from an earlier session."},
                {"href": "sf-overflow-audit/index.html", "t": "Parallel SF overflow audit", "d": "Independent audit dashboard from another session, merged unchanged."},
                {"href": "flagged.html", "t": "Flagged for review", "d": "Everything unverified or irregular, with source links."},
            ]},
            {"type": "callout", "tone": "ok", "html": "<strong>Source links are provided, but not every row has a government source.</strong> The automated check tests link presence, not whether a source proves every claim; see <a href=\"flagged.html\">U21</a>. License facts come from the official CSLB database (all sixteen records re-read 2026-11-08, each printing “Data current as of 11/8/2026”); permit and licensing rules come from sf.gov and California Legislative Information; technical and cost claims link to the manufacturer or publisher page they were read from."},
            {"type": "callout", "tone": "warn", "html": "<strong>Blank means unconfirmed.</strong> Where a value cannot be confirmed from an official source, the verified value cell is left blank and marked UNVERIFIED. Owner-provided figures appear only on the clearly labeled " + slink("S44", "Project brief") + " page, in the explicitly labeled Brief transcription table on <a href=\"estimates.html\">Estimates</a>, and on the <a href=\"flagged.html\">Flagged for Review</a> page. Nothing is inferred or filled in."},
            {"type": "callout", "tone": "info", "html": "Archived material from earlier sessions remains published at " + slink("S49", "bathtub-overflow/") + ", " + slink("S50", "docs/bath/") + ", " + slink("S51", "docs/plumbing-index.html") + " and the unrelated legacy GEMS site at " + slink("S48", "docs/index.html") + ". Those files were not edited by this integration session. Shared task board: " + slink("S45", "COORDINATION.md") + "."},
        ],
    },
    "summary.html": {
        "title": "Executive summary",
        "eyebrow": "Overview · updated 2026-11-07",
        "h1": "Executive summary",
        "lede": "The important details of the bathtub wastewater overflow trip lever project — the problem, the estimates, who can do the work, what the rules say, and what still needs review.",
        "sections": [
            {"type": "prose", "title": "1. The problem", "html": "<p>The bathtub's waste-and-overflow trip lever is " + pill("owner-provided", "info") + " stuck inside hidden plumbing behind the wall, in a hard-to-access area. More than five licensed plumbers reportedly declined to remove it from above because of the risk of damaging concealed plumbing, and recommended working from below — where a storage unit sits beneath the unit, so the drywall ceiling may need to be opened. The unit is tenant-occupied, so the owner wants one provider able to do both drywall and plumbing in a sensitive environment. Removing the overflow from above remains preferred if it can be done safely. None of these facts can be confirmed from a public source; see the " + "<a href=\"brief.html\">Project brief</a>" + " and " + "<a href=\"flagged.html\">Flagged for Review</a>" + " page. Context: " + slink("S18", "This Old House on below access") + ", " + slink("S17", "Angi on overflow function") + ".</p>"},
            {"type": "table", "title": "2. Estimates at a glance", "ref": "estimates"},
            {"type": "prose", "title": "3. What the numbers mean", "html": "<p>The three quotes describe three different scopes — an adjustment, a spout/lever replacement, and a full waste-and-overflow replacement. Independent 2026 publisher benchmarks put bathtub/shower drain replacement at <strong>$500–$1,020 (avg $700)</strong> (" + slink("S15", "Angi, 2026-09-18") + "), bathroom leak repair at <strong>$150–$600</strong> plus <strong>$300–$930</strong> for drywall/tile follow-up (" + slink("S16", "Angi, 2026-10-28") + "), and new drywall at about <strong>$2,100</strong> (" + slink("S15", "Angi") + "). Drywall is not included in any of the three quoted scopes. The quote amounts themselves are owner-provided and unverified, so this comparison is directional only. Full table: <a href=\"estimates.html\">Estimates &amp; costs</a>.</p>"},
            {"type": "prose", "title": "4. Who can do the work", "html": "<p>Sixteen license records were re-read directly on the official CSLB database on 2026-11-08 (eight of them previously published on 2026-11-07, plus one unverified lead that still has no license number). All sixteen hold <strong>current and active</strong> licenses. Six hold both a building classification and C-36 Plumbing on one license — " + slink("S64", "Genteel #1025814") + ", " + slink("S11", "Ace #829071") + ", " + slink("S09", "GENERALSF #959843") + ", " + slink("S10", "Handyman Heroes #1003394") + ", " + slink("S56", "Rapid Flow #1115649") + " and " + slink("S57", "Manny's #841229") + " — which makes them useful candidates for a single-provider request. Classifications do not establish that they will perform all work or that other arrangements are excluded; see " + slink("S62", "BPC §7059") + ". CSLB verifies license classes, not the ability to perform this specific delicate repair; that remains unverified and flagged. " + slink("S05", "C-36 classification definition") + ". A dedicated C-9 drywall contractor, " + slink("S66", "Bernal Hill Drywall #995163") + ", is verified for a two-trade arrangement. Full tables: <a href=\"contractors.html\">Contractors &amp; reviews</a> and <a href=\"contacts.html\">Contacts &amp; licenses</a>.</p>"},
            {"type": "prose", "title": "5. Official rules (neutral)", "html": "<p>SF.gov states: “You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground” (" + slink("S01", "sf.gov") + "), and lists “minor repairs to existing interior plaster or wallboard” among work that does not need a permit (" + slink("S02", "sf.gov") + "). Contractors applying for a plumbing permit must hold C-4, C-16, C-20, C-36, C-54, B or A classifications (" + slink("S01", "sf.gov") + "). California B&amp;P §7048 sets the current small-job licensing exemption at under $1,000 for casual/minor work that does not require a building permit, effective 2026-01-01 (" + slink("S13", "leginfo") + "). The hiring party should confirm applicability for the exact scope with SF DBI and the selected contractor. Full table: <a href=\"permits.html\">Permits &amp; licensing</a>.</p>"},
            {"type": "prose", "title": "6. Recommended next steps", "html": "<ol class=\"tight\"><li><strong>Work down the computed ranking</strong> — <a href=\"ranking.html\">Ranked hiring decision</a> orders every candidate on verified CSLB facts; the top three are " + slink("S11", "Ace #829071") + ", " + slink("S64", "Genteel #1025814") + " and " + slink("S10", "Handyman Heroes #1003394") + ", ahead of " + slink("S09", "#959843") + ", " + slink("S57", "#841229") + " and " + slink("S56", "#1115649") + ". Ask for one written scope covering an above-attempt, below access, ceiling cut/patch/finish, a fill-and-inspect water test, and tenant access windows.</li><li><strong>Confirm crew coverage in writing</strong>: four CSLB records show a workers'-compensation “no employees” exemption and one policy expires 2026-12-18 (" + slink("S07", "#757796") + ", " + slink("S09", "#959843") + ", " + slink("S56", "#1115649") + ", " + slink("S57", "#841229") + ", " + slink("S08", "#1024971") + ").</li><li><strong>Ask for references on concealed waste-and-overflow work in occupied units</strong>; no official source confirms job-specific capability (" + slink("S04", "CSLB Check a License") + ", " + slink("S24", "Angi SF bathtub reviews") + ").</li><li><strong>Re-verify the chosen license on the hire date</strong> at " + slink("S04", "cslb.ca.gov") + " and review the " + "<a href=\"flagged.html\">34 flagged items</a>" + ".</li></ol>"},
            {"type": "callout", "tone": "warn", "html": "<strong>Informational only.</strong> This summary is research, not legal advice, a quote, or a contractor endorsement. Every unverified value is blank in the data tables and listed on the Flagged for Review page."},
        ],
    },
    "requirements.html": {
        "title": "Requirements",
        "eyebrow": "Overview · full list · updated 2026-11-07",
        "h1": "Requirements register",
        "lede": "The owner's brief, broken out line by line. Each row links the project primary record and the relevant official page. Officially confirmed values are blank wherever no official source exists.",
        "sections": [
            {"type": "table", "ref": "requirements"},
            {"type": "callout", "tone": "info", "html": "The register covers every requirement in the brief that is suitable for publication. Internal-only instructions are deliberately omitted; the " + "<a href=\"verification.html\">Verification</a>" + " page documents the privacy sweep that enforces this."},
        ],
    },
    "estimates.html": {
        "title": "Estimates & costs",
        "eyebrow": "Data · updated 2026-11-07",
        "h1": "Estimates & cost benchmarks",
        "lede": "The three quotes received on 2026-08-30, plus independent 2026 publisher benchmarks for comparable work.",
        "sections": [
            {"type": "table", "ref": "estimates"},
            {"type": "table", "ref": "brief_quotes", "title": "Brief transcription — quoted amounts (NOT verified)"},
            {"type": "callout", "tone": "warn", "html": "<strong>Why the amount column is blank.</strong> No official source publishes a private quote. Per the verification rule the verified-amount cell is left blank and flagged; the owner's figures are transcribed only on the <a href=\"brief.html\">Project brief</a> page, in the labeled Brief transcription table on this page, and on the <a href=\"flagged.html\">Flagged for Review</a> page."},
            {"type": "table", "ref": "benchmarks"},
            {"type": "prose", "title": "Analysis", "html": "<ul class=\"tight\"><li>The two replacement-style scopes sit inside the published <strong>$500–$1,020</strong> replacement range, while the adjustment scope sits near the <strong>$150–$600</strong> leak-repair range and the <strong>$50–$200</strong> call-out minimum (" + slink("S15", "Angi") + ", " + slink("S16", "Angi") + ").</li><li>Drywall is a separate budget line: about <strong>$2,100</strong> for new drywall, or <strong>$300–$930</strong> for post-leak patching (" + slink("S15", "Angi") + ", " + slink("S16", "Angi") + ").</li><li>Component-level context: this publisher's itemized bathtub installation lists the overflow at <strong>$163</strong> (" + slink("S19", "This Old House, 2026-03-05") + ").</li><li>All benchmark figures are national publisher data, not San Francisco prices and not quotes for this job.</li></ul>"},
        ],
    },
    "contractors.html": {
        "title": "Contractors & reviews",
        "eyebrow": "Data · official CSLB records checked 2026-11-07",
        "h1": "Contractors & review platforms",
        "lede": "Eight candidates had active CSLB license records on 2026-11-07; one additional lead is unverified. Service area and this specific scope must be confirmed.",
        "sections": [
            {"type": "table", "ref": "contractors"},
            {"type": "table", "ref": "review_snapshots"},
            {"type": "table", "ref": "platforms"},
            {"type": "callout", "tone": "info", "html": "<strong>No provider has been contacted by the research session, and none has confirmed this job to that session. The owner reported prior estimates; current job acceptance and availability remain unconfirmed.</strong> This dashboard is desk research only. All review-platform ratings, counts and badges are third-party data and are unverified where they could not be re-checked on 2026-11-08; only " + slink("S04", "CSLB") + " verifies a California contractor license. See " + slink("S58", "the shortlist") + " and <a href=\"flagged.html\">Flagged for Review</a>."},
            {"type": "callout", "tone": "info", "html": "<strong>Relevant advertised scope:</strong> " + slink("S61", "Fast Response’s own repair page") + " lists bathtub waste and overflow repair in San Francisco and gives (415) 596-6115; its " + slink("S08", "CSLB record") + " shows active C-36 status on 2026-11-08. This is a company claim, not proof it can safely extract this stuck lever or arrange drywall repair. Request one written scope including patching and occupied-unit precautions."},
            {"type": "prose", "title": "How to re-verify a license", "html": "<ol class=\"tight\"><li>Open " + slink("S04", "CSLB Check a License") + " and enter the 7-digit number from the table (or the business name).</li><li>Confirm <strong>current and active</strong> status, that the classification covers the work (" + slink("S05", "C-36 Plumbing") + "), the bond, and workers' compensation coverage.</li><li>Open the complaint-disclosure section of the record before signing anything — see " + slink("S12", "the official disclosure for #1003394") + ".</li></ol><p class=\"src\">CSLB's own page recommends reading its hiring guidance and checking complaint disclosure before hiring. Records on this site were read 2026-11-07; statuses change.</p>"},
        ],
    },
    "technical.html": {
        "title": "Technical background",
        "eyebrow": "Reference · verified publisher and manufacturer pages",
        "h1": "Technical background",
        "lede": "How a trip-lever bath waste-and-overflow assembly works, and why above-access can fail while below-access is the documented fallback.",
        "sections": [
            {"type": "table", "ref": "technical"},
            {"type": "callout", "tone": "info", "html": "These sources describe typical assemblies and procedures. None inspected this bathtub, and none is San Francisco code guidance. For the official permit and licensing rules see <a href=\"permits.html\">Permits &amp; licensing</a>."},
        ],
    },
    "permits.html": {
        "title": "Permits & licensing",
        "eyebrow": "Reference · official sources only",
        "h1": "Permits & licensing — official references",
        "lede": "Neutral reporting of current official San Francisco and California requirements. This page contains no instruction or recommendation about obtaining or not obtaining a permit, and records no private project rationale.",
        "sections": [
            {"type": "table", "ref": "permits"},
            {"type": "callout", "tone": "info", "html": "Confirm the exact scope with the SF Department of Building Inspection and the selected licensed contractor. sf.gov lists the Permit Center help desk and permitsf@sfgov.org as contacts (" + slink("S01", "sf.gov") + "). Nothing on this page is legal advice."},
        ],
    },
    "brief.html": {
        "title": "Project brief",
        "eyebrow": "Primary record · owner-provided · NOT independently verified",
        "h1": "Project brief (primary record)",
        "lede": "A transcription of the owner-provided project information, published as this project's own primary record. It is not an official public source. Every value taken from it is blank in the officially verified columns elsewhere on this site and flagged as unverified.",
        "sections": [
            {"type": "table", "ref": "brief_quotes"},
            {"type": "table", "title": "Problem snapshot", "ref": "problem"},
            {"type": "prose", "title": "What the brief says about the work", "html": "<p>The owner wants someone who can service San Francisco and has experience with delicate work in a sensitive environment where tenants occupy the unit. The trip lever is stuck inside hidden plumbing behind the wall. Removing the overflow from above is preferred, but more than five licensed plumbers could not do so without concern over destroying the hidden plumbing, and recommended working from below — where a storage unit sits beneath the unit, so the drywall ceiling may need to be opened. One all-in-one service is wanted for drywall and plumbing. The owner asked for research using Yelp and other review services, a licensed plumber or contractor, an executive summary, a verified live site, a Flagged for Review page, and completion of all tasks without manual input. Reference pictures were mentioned but not supplied.</p><p class=\"src\">Source: this project's own brief as transcribed here (" + slink("S44", "primary record") + "); task board: " + slink("S45", "COORDINATION.md") + ". No independent public source confirms these statements.</p>"},
            {"type": "callout", "tone": "warn", "html": "<strong>Not verified.</strong> The three amounts above are reproduced only so the project's entries remain complete. They do not appear in any verified value column on this site and must not be treated as confirmed prices. See <a href=\"flagged.html\">Flagged for Review · U01/U02</a>."},
        ],
    },
    "findings.html": {
        "title": "Findings & analysis",
        "eyebrow": "Data · analysis · updated 2026-11-07",
        "h1": "Findings & analysis",
        "lede": "What the verified data supports, what it does not, and the resulting shortlist rationale.",
        "sections": [
            {"type": "table", "ref": "findings"},
            {"type": "prose", "title": "Access decision matrix", "html": "<div class=\"table-wrap\"><table><thead><tr><th>Route</th><th>What the sources say</th><th>Verified?</th><th>Source</th></tr></thead><tbody><tr><td><strong>From above (preferred)</strong></td><td>Remove the overflow-plate screws and withdraw the upper linkage; cleaning or adjusting the link can free a stuck mechanism</td><td>" + pill("procedure documented; outcome for this tub unverified", "warn") + "</td><td>" + slink("S18") + " · " + slink("S21") + " · " + slink("S20") + "</td></tr><tr><td><strong>From below (reported fallback)</strong></td><td>Stubborn/seized drains may require access from below; new waste-and-overflow kits are aligned from below while a helper holds the shoe from above</td><td>" + pill("procedure documented; this tub's layout unverified", "warn") + "</td><td>" + slink("S18") + " · " + slink("S14") + "</td></tr><tr><td><strong>Drywall ceiling opening</strong></td><td>SF.gov lists minor interior plaster/wallboard repair among work not needing a building permit; the plumbing scope is governed by the plumbing-permit rule</td><td>" + pill("official rules cited; applicability to this scope to be confirmed with SF DBI", "warn") + "</td><td>" + slink("S02") + " · " + slink("S01") + "</td></tr></tbody><caption>Each row links the source it was read from. This matrix is analysis, not a scope of work or a legal determination.</caption></table></div>"},
            {"type": "prose", "title": "Shortlist rationale", "html": "<p>Start with firms whose single verified license lists both a building classification and C-36 Plumbing: " + slink("S11", "Ace #829071") + ", " + slink("S09", "GENERALSF #959843") + ", " + slink("S10", "Handyman Heroes #1003394") + ", " + slink("S56", "Rapid Flow #1115649") + " and " + slink("S57", "Manny's #841229") + ". This follows from the CSLB classifications themselves, not from any company claim. Watch items: workers'-compensation exemptions on #959843, #757796, #1115649 and #841229, a policy expiring 2026-12-18 on #1024971, and the official complaint disclosure on #1003394 — all listed on the <a href=\"flagged.html\">Flagged for Review</a> page. Re-check every license at " + slink("S04", "CSLB") + " on the hire date.</p>"},
        ],
    },
    "sources.html": {
        "title": "Source ledger",
        "eyebrow": "Reference · every URL used on this site",
        "h1": "Source ledger",
        "lede": "Every source used by the dashboard, with publisher, tier, retrieval date, verification status and what it supports. Official government sources are graded separately from publishers, platforms, company sites and the project's own primary records.",
        "sections": [
            {"type": "table", "ref": "source_ledger"},
            {"type": "callout", "tone": "info", "html": "<strong>Tiers.</strong> <em>official</em> = government agency or official code publisher; <em>manufacturer</em> = product maker's own page; <em>publisher</em> = the article's own site (authoritative for what that article says); <em>platform</em> = review/directory site; <em>company</em> = a contractor's own site (self-description); <em>primary</em> = this project's own records. Dead sources are documented but never cited by a table row."},
        ],
    },
    "verification.html": {
        "title": "Verification",
        "eyebrow": "Audit · generated by scripts/verify_dashboard.py",
        "h1": "Verification",
        "lede": "Line-by-line verification of the combined dataset, the site build and the published links. Generated from the same data file that builds the site, so the audit cannot drift from the content.",
        "sections": [
            {"type": "verification_summary"},
            {"type": "row_audit"},
            {"type": "prose", "title": "Method", "html": "<ol class=\"tight\"><li>Each table row is emitted with a Source column built from its source ids. The build script aborts if any row has no source, cites an unknown source, or cites a source marked dead.</li><li>Source reads are dated per source in the ledger. The 2026-11-08 integration re-read all sixteen CSLB License Detail records (each printing “Data current as of 11/8/2026”), ten official business websites, the CSLB B and C-9 classification pages and the Handyman Heroes complaint disclosure. Earlier sessions' reads keep their own dates. The automated verifier itself performs no network check.</li><li>The verifier parses every generated HTML file: every <code>&lt;tbody&gt;</code> row must contain a link; every internal link (pages, CSS, JS, anchors) must resolve to an existing file; every external link must exist in the source ledger; no dead source may be linked from a row.</li><li>A privacy sweep greps all published HTML/MD/JSON/CSS/JS for internal-only hiring-constraint wording and returns zero matches.</li><li>After merge, the live GitHub Pages URL is fetched and the Pages build status is checked with the GitHub API.</li></ol>"},
            {"type": "callout", "tone": "ok", "html": "<strong>Interpretation of “blank”.</strong> Owner-provided values (the three quotes and the problem description) have no official public source. Their <em>verified</em> value cells are blank and flagged; the original figures are transcribed only on the explicitly labeled <a href=\"brief.html\">Project brief</a> page and on <a href=\"flagged.html\">Flagged for Review</a>. This preserves all entries without presenting an unverified value as confirmed."},
        ],
    },
    "repo-review.html": {
        "title": "Repo review",
        "eyebrow": "Audit · line-by-line repository review",
        "h1": "Repository review",
        "lede": "What is in this checkout, what prior sessions produced, what was verified against official sources, and every irregularity found.",
        "sections": [
            {"type": "table", "ref": "repo_review"},
            {"type": "callout", "tone": "info", "html": "Links for manual review: " + slink("S47", "README") + " · " + slink("S45", "COORDINATION.md") + " · " + slink("S46", "live Pages site") + " · " + slink("S52", "open PR #32") + ", " + slink("S58", "shortlist.html") + ", " + slink("S59", "verification-log.html") + ", " + slink("S60", "sf-overflow-audit/") + ". Archived parallel work: " + slink("S49", "bathtub-overflow/") + ", " + slink("S50", "docs/bath/") + ", " + slink("S51", "docs/plumbing-index.html") + "."},
        ],
    },
    "flagged.html": {
        "title": "Flagged for review",
        "eyebrow": "Audit · clearly labeled · does not block anything",
        "h1": "Flagged for Review",
        "lede": "Every value that could not be confirmed from an official source, and every irregularity found during repo and source review. None of these items blocks the site, the analysis, or the merge — they are published here, with source links, for review after the site is live.",
        "sections": [
            {"type": "table", "ref": "flagged"},
            {"type": "callout", "tone": "warn", "html": "To request a change, note the item ID (U01–U34) and the correction. Unverified values are blank in the data tables; nothing was inferred to fill a gap. Full source ledger: <a href=\"sources.html\">Sources</a>."},
        ],
    },
}


# ===========================================================================
# Integration merge — session arena/0e9ee506-korea7, 2026-11-08.
#
# Adds the ranked hiring decision and the verified contact directory built by
# scripts/ranking_data.py from three committed, source-traceable datasets:
#   data/canonical/cslb_records.json      16 official CSLB records, read 2026-11-08
#   data/canonical/vendor_sites.json      10 official business sites, read 2026-11-08
#   data/canonical/review_snapshots.json  dated third-party snapshots (never scored)
# Existing rows from prior sessions are preserved; new rows are appended.
# Source ids S64-S88 and flag ids U23-U34 were allocated after the concurrent
# session's S61-S63 / U21-U22 so nothing already published is renumbered.
# ===========================================================================
TABLES.update(R.TABLES)
PAGES.update(R.PAGES)

# Sources re-read directly during this session: refresh the retrieval date and
# record the new "Data current as of" stamp instead of leaving a stale date.
for _lic, _sid in R.LICENSE_SRC.items():
    if _sid in SOURCES and _sid not in R.SOURCES:
        _rec = R.RECORDS[_lic]
        SOURCES[_sid]["checked"] = R.CHECKED
        SOURCES[_sid]["supports"] = (
            "Business name, address, business phone number on record, entity, issue/expiry dates, "
            "status, classifications, bond, workers' compensation")
        SOURCES[_sid]["note"] = (
            "Re-read directly on cslb.ca.gov on 2026-11-08; record printed '%s'. "
            "Previously read 2026-11-07: no change to status, classifications or expiry."
            % _rec["record_stamp"])
for _sid in ("S12", "S38", "S39", "S40", "S41", "S42", "S43", "S61", "S62"):
    SOURCES[_sid]["checked"] = R.CHECKED
    if "Re-read directly on 2026-11-08." not in SOURCES[_sid]["note"]:
        SOURCES[_sid]["note"] = SOURCES[_sid]["note"].rstrip() + " Re-read directly on 2026-11-08."

# Eight further licensees, appended to the existing contractor table.
_PREV_LIC = ("977638", "757796", "1024971", "959843", "1003394", "829071", "1115649", "841229")
for _lic in sorted(R.RECORDS, key=lambda l: R.DISPLAY[l].lower()):
    if _lic in _PREV_LIC:
        continue
    _rec = R.RECORDS[_lic]
    _src = [R.LICENSE_SRC[_lic], "S85"]
    _site = R.SITES.get(_lic)
    if _site:
        _src.append(R.SITE_SRC[_lic])
    _company = "<strong>%s</strong>" % R.esc(R.DISPLAY[_lic])
    if _site:
        _company += "<br>" + R.ext(_site["official_url"], "site")
    else:
        _company += "<br><small>official site %s %s</small>" % (BLANK, UNVERIFIED)
    _company += "<br><small>CSLB phone: %s</small>" % R.esc(_rec["phone_on_record"])
    _status = pill("current and active", "ok") + "<br>expires %s" % R.esc(_rec["expire_date"])
    if _rec["additional_status"]:
        _status += "<br>" + pill("additional status — read the record", "bad")
    _ver = pill("CSLB verified 2026-11-08", "ok")
    if _rec["additional_status"]:
        _ver += " " + pill("status warning flagged", "warn")
    if not _site:
        _ver += " " + pill("no business site verified", "warn")
    TABLES["contractors"]["rows"].append({"cells": [
        _company,
        R.ext(_rec["source_url"], "#%s" % _lic),
        R.esc(R.cls_text(_rec)),
        _status,
        R.wc_text(_rec) + "<br><small>$25,000 bond</small>",
        R.esc("%s, %s %s" % (_rec["street"].title(), _rec["city"].title(), _rec["zip"])),
        R.esc(R.REASON[_lic]),
        _ver,
    ], "src": _src})

# New flagged items and findings (existing IDs are never renumbered).
for _cells, _src in R.NEW_FLAGS:
    TABLES["flagged"]["rows"].append({"cells": _cells, "src": _src})
for _cells, _src in R.NEW_FINDINGS:
    TABLES["findings"]["rows"].append({"cells": _cells, "src": _src})

# Repo-review rows for this session's audit.
TABLES["repo_review"]["rows"].append({"cells": [
    "Prior Pages deployment",
    "The pages build/deploy run for main commit 1faccdc failed at the deploy step; the preceding run "
    "succeeded, so the live site served the earlier deployment. Recorded as an open item by session "
    "arena/89ae6815-korea7 and taken over by this session.",
    "Checked with gh run list / gh api repos/.../pages on 2026-11-08: later runs for main completed "
    "successfully and the Pages status returned to built. The live dashboard was fetched and matched "
    "the repository content.",
    pill("resolved by later runs", "ok")], "src": ["S46", "S45"]})
TABLES["repo_review"]["rows"].append({"cells": [
    "New verified datasets",
    "data/canonical/cslb_records.json (16 records), vendor_sites.json (10 business sites) and "
    "review_snapshots.json (6 dated platform snapshots) added, each field carrying its source URL and "
    "retrieval date. scripts/ranking_data.py computes the ranking from the CSLB fields only.",
    "Every CSLB record and every business site was fetched and read directly on 2026-11-08; "
    "no value was inferred and unconfirmed cells are blank.",
    pill("added", "ok")], "src": ["S85", "S86", "S87", "S88"]})
TABLES["repo_review"]["rows"].append({"cells": [
    "Candidate pool completeness",
    "Every CSLB license number cited anywhere in the repository (16 distinct numbers across the root "
    "dashboard, shortlist.html, sf-overflow-audit/ and docs/ archives) was re-verified, so the canonical "
    "tables now cover the union of all parallel sessions' candidates.",
    "License numbers extracted by grep across all HTML/JSON/MD files, then each record read on CSLB.",
    pill("verified", "ok")], "src": ["S85", "S58", "S60"]})
TABLES["repo_review"]["rows"].append({"cells": [
    "Concurrent ID collision",
    "A concurrent session published sources S61-S63 and flags U21-U22 while this session was drafting "
    "S61-S85 / U21-U32. This session renumbered its own additions to S64-S88 and U23-U34 rather than "
    "overwriting the published ids.",
    "Merge resolved by taking the concurrent version of the generator and re-applying this session's "
    "edits on top; the concurrent session's regression tests still pass.",
    pill("resolved", "ok")], "src": ["S45"]})

# Executive summary: insert the ranked recommendation before the closing callout.
_sections = PAGES["summary.html"]["sections"]
_sections.insert(len(_sections) - 1, R.SUMMARY_BLOCK)

# Keep the flagged-count card in step with the table.
for _block in PAGES["index.html"]["sections"]:
    if _block["type"] == "cards":
        for _card in _block["items"]:
            if _card["v"] == "AUTO_FLAGS":
                _card["v"] = str(len(TABLES["flagged"]["rows"]))


# --- Integration audit additions (session arena/52d35ede-korea7, PR #60/#61 merge) ---
SOURCES.update({'S89': {'label': 'Handyman Heroes — Handyman services',
         'publisher': 'Handyman Heroes Inc',
         'url': 'https://www.handymanhero.es/handyman-services/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists sheetrock and wall repairs, plumbing and electrical services, San '
                     'Francisco homes and apartments; phone 1-844-382-4376; license #1003394.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S90': {'label': 'Rapid Flow Plumbing & Rooter — home',
         'publisher': 'Rapid Flow Plumbing & Rooter Inc',
         'url': 'https://www.rapidflowbayarea.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists B and C-36 license #1115649, plumbing and general contracting/remodels, '
                     'San Francisco Bay Area service; marketing phone 844-BAY-FLOW.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S91': {'label': 'CSLB — How to find the right licensed contractor',
         'publisher': 'Contractors State License Board',
         'url': 'https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'CSLB advises at least three written bids on identical scope, checking '
                     "license/personnel, address/phone, workers' compensation and general liability "
                     'insurance; bond is not a competency guarantee.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S92': {'label': 'California Civil Code §1954 — landlord entry',
         'publisher': 'California Legislative Information',
         'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Civil Code 1954 limits landlord entry, generally requires reasonable written notice '
                     'with date/approximate time/purpose and normal business hours; 24 hours is presumed '
                     'reasonable absent contrary evidence; exceptions include emergency, consent at entry '
                     'and agreed repair entry within one week.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S93': {'label': 'Watco — Trip Lever Installation Instructions (PDF)',
         'publisher': 'Watco Manufacturing Co.',
         'url': 'https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf',
         'tier': 'manufacturer',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Watco trip-lever instructions: drain elbow/gasket secured under tub; overflow elbow '
                     'aligned behind tub; overflow plate and drop cylinder installed with screws; linkage '
                     'must not be kinked; readjust to ensure drain stops water. Model-specific instructions, '
                     'not identification of this tub.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S94': {'label': 'SF.gov — Apply for a kitchen or bath remodel permit',
         'publisher': 'SF Department of Building Inspection',
         'url': 'https://www.sf.gov/apply-kitchen-or-bath-remodel-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'SF DBI kitchen/bath permit guidance for in-kind fixture renovation with no structural '
                     'work; online route limited to no wall removal/moving and R-2/R-3 legally permitted '
                     'kitchens/baths; related plumbing/electrical permits and inspections are separate.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S95': {'label': 'Yelp — Ace Plumbing & Rooter profile',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco?start=160',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': "Search excerpt located Ace Plumbing & Rooter's Yelp profile and plumbing categories. "
                     'Numeric rating/count not used as verified evidence.',
         'note': 'web_search excerpt; direct Yelp fetch HTTP 403 Preserved by integration session '
                 'arena/52d35ede-korea7 during PR #61 merge.'},
 'S96': {'label': '2025 San Francisco Plumbing Code PDF — §104.2',
         'publisher': 'City and County of San Francisco',
         'url': 'https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'SF Plumbing Code 104.2 exempt work includes repair of leaks not requiring cutting into '
                     'or removing piping, and unstopping traps/sewers/vents/waste pipes not requiring '
                     'cutting into or removal of traps or piping.',
         'note': 'direct fetch, chunk 1, printed pages 4-5 Preserved by integration session '
                 'arena/52d35ede-korea7 during PR #61 merge.'},
 'S97': {'label': 'Prior canonical research snapshot (2026-11-07/08)',
         'publisher': 'This repository',
         'url': 'data/canonical/research-history-2026-11-07.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Preserved prior tables/sources before this refresh',
         'note': 'Historical data retained; not current verification. Preserved by integration session '
                 'arena/52d35ede-korea7 during PR #61 merge.'},
 'S98': {'label': 'Repository source/artifact inventory',
         'publisher': 'This repository',
         'url': 'data/canonical/repo_inventory.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'File paths, byte counts, SHA-256 hashes and review category',
         'note': 'Generated pages/reports excluded to avoid self-reference; external factual claims in '
                 'unrelated files not verified. Preserved by integration session arena/52d35ede-korea7 '
                 'during PR #61 merge.'},
 'S99': {'label': 'General SF — Building services',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/building',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists Rough and Finish Plumbing; Sheetrock/Tape and Texture; phone '
                     '(650)-303-1515; CSLB 959843.',
         'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'},
 'S100': {'label': 'General SF — Plumbing services',
          'publisher': 'General SF',
          'url': 'https://generalsf.com/plumbing',
          'tier': 'company',
          'status': 'verified',
          'checked': '2026-11-08',
          'supports': 'Company lists plumbing installation/repair, sewer/water lines, '
                      'faucet/toilet/tub/shower replacement; phone (650)-303-1515; CSLB 959843.',
          'note': 'direct fetch Preserved by integration session arena/52d35ede-korea7 during PR #61 merge.'}})
TABLES["requirements"] = {'title': 'Requirements register — line by line',
 'columns': ['#',
             'Requirement as stated',
             'Category',
             'Officially confirmed value / implementation',
             'Status',
             'Source'],
 'rows': [{'cells': ['R01',
                     'Collect, organize and analyze a full list of requirements',
                     'Project scope',
                     'Implemented in this register',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R02',
                     'Create an executive summary of important details',
                     'Deliverable',
                     'Executive summary page and Markdown file',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S46']},
          {'cells': ['R03',
                     'Bathtub overflow is hard to access; drywall may need opening',
                     'Problem',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S02']},
          {'cells': ['R04',
                     'Remove the bathtub wastewater overflow trip lever',
                     'Scope',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S14', 'S93']},
          {'cells': ['R05',
                     'Expert Plumbing Solutions: replacing waste and overflow; owner-reported $614',
                     'Estimate',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S06']},
          {'cells': ['R06',
                     'Bay Area Plumbing: lever/plug/spout with diverter, labor/materials; owner-reported '
                     '$550',
                     'Estimate',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S07']},
          {'cells': ['R07',
                     'Fast Response: repair/adjust plunger handle; owner-reported $135',
                     'Estimate',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S08']},
          {'cells': ['R08',
                     'Estimates dated 8/30/26',
                     'Estimate date',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44']},
          {'cells': ['R09',
                     'Find someone who can perform the needed work',
                     'Objective',
                     'Sixteen CSLB-verified candidates researched; no provider acceptance confirmed',
                     '<span class="pill warn">research done / acceptance unverified</span>'],
           'src': ['S44', 'S04']},
          {'cells': ['R10',
                     'Removal from above is preferred if possible',
                     'Preference',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S93']},
          {'cells': ['R11',
                     '5+ licensed plumbers could not remove it from above without damage concern',
                     'Constraint',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S04']},
          {'cells': ['R12',
                     'Work from below; storage unit below; ceiling drywall may need opening',
                     'Access',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S02', 'S96']},
          {'cells': ['R13',
                     'One all-in-one service for drywall and plumbing',
                     'Service requirement',
                     'Six B+C-36 licenses verified; combined execution and drywall scope unconfirmed',
                     '<span class="pill warn">license verified / execution unverified</span>'],
           'src': ['S44', 'S09', 'S10', 'S11', 'S56', 'S57', 'S83']},
          {'cells': ['R14',
                     'Look on Yelp and other review services for this specific work in San Francisco',
                     'Research',
                     'Yelp profiles/searches located; direct fetch blocked; numeric values blank',
                     '<span class="pill warn">research done / reviews unverified</span>'],
           'src': ['S44', 'S32', 'S33', 'S34', 'S35', 'S36', 'S95']},
          {'cells': ['R15',
                     'Provider should be a licensed plumber or contractor',
                     'Provider',
                     'CSLB records checked for sixteen candidates',
                     '<span class="pill ok">license records verified</span>'],
           'src': ['S44', 'S04', 'S05']},
          {'cells': ['R16',
                     'Provider must service the San Francisco area',
                     'Service area',
                     'Company service claims and CSLB addresses recorded; exact address availability '
                     'unconfirmed',
                     '<span class="pill warn">recorded / availability unverified</span>'],
           'src': ['S44', 'S41', 'S43', 'S75']},
          {'cells': ['R17',
                     'Experience with delicate work in a sensitive, tenant-occupied unit',
                     'Environment',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S92', 'S91']},
          {'cells': ['R18',
                     'Reference pictures may be supplied; work from description if absent',
                     'Input',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R19',
                     'No manual input; complete tasks autonomously',
                     'Process',
                     'No clarification requested; desk research/build performed',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R20',
                     'Review repo line by line; official trusted sources; links; flag irregularities',
                     'Repo work',
                     'Repository inventory and dashboard row audit generated; unrelated GEMS facts not '
                     'externally verified',
                     '<span class="pill warn">inventory done / external facts flagged</span>'],
           'src': ['S44', 'S45', 'S47', 'S98']},
          {'cells': ['R21',
                     'GitHub Pages site: clean landing page, category subpages, simple tables',
                     'Site',
                     'Static dashboard built at repository root',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S46']},
          {'cells': ['R22',
                     'Every table row has an official source link; unconfirmable values blank and flagged',
                     'Verification',
                     'Source links present; owner/third-party rows lack official confirmation and are '
                     'flagged (U21)',
                     '<span class="pill warn">partial / needs review</span>'],
           'src': ['S44', 'S04', 'S45']},
          {'cells': ['R23',
                     'Rank contractors best-to-hire with reasoning, costs, official links and phone numbers',
                     'Decision analysis',
                     'Conditional ranking and contact directory published; combined costs blank/unverified',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S91']},
          {'cells': ['R24',
                     'No hallucinations; never infer or fill unconfirmed values',
                     'Verification',
                     'Blank + UNVERIFIED policy and source grades enforced; manual review still required',
                     '<span class="pill ok">policy implemented</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R25',
                     'Coordinate parallel sessions through COORDINATION.md; non-overlapping scopes; frequent '
                     'commits',
                     'Coordination',
                     'Claim pushed; concurrent board entries preserved',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R26',
                     'Publish Flagged for Review page; flags do not block merge',
                     'Site',
                     'Flagged page published with source links',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S46']},
          {'cells': ['R27',
                     'Create PR to main, merge after checks, confirm Pages, record result',
                     'Delivery',
                     'See COORDINATION.md for the actual PR, merge and Pages deployment record',
                     '<span class="pill info">delivery record in board</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R28',
                     'Keep requester-only context out of public artifacts',
                     'Privacy boundary',
                     'Privacy sweep and public-content review performed',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S45']},
          {'cells': ['R29',
                     'Build must have no broken links; do not merge a broken site',
                     'Quality gate',
                     'Internal links/anchors/assets checked; deploy confirmed separately',
                     '<span class="pill ok">implemented / see evidence</span>'],
           'src': ['S44', 'S45', 'S46']},
          {'cells': ['R30',
                     'Tenants occupy the unit where the lever is stuck',
                     'Environment',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>',
                     '<span class="pill warn">owner-provided / unverified</span>'],
           'src': ['S44', 'S92']}],
 'caption': 'Owner requirements cannot be “officially verified” as facts. Implementation status is a project '
            'record; external facts use the cited official/company sources. Blank means no official '
            'confirmation.'}
TABLES["access_options"] = {'title': 'Access options — what is and is not established',
 'columns': ['Route', 'Evidence', 'Project-specific conclusion', 'Source'],
 'rows': [{'cells': ['From above (preferred)',
                     'Watco instructions show overflow plate/linkage removal and adjustment for its models; '
                     'this tub model is unknown',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>'],
           'src': ['S93', 'S44']},
          {'cells': ['From below (reported fallback)',
                     'This Old House describes below access for stubborn drains; SF rules govern any '
                     'cutting/replacement and covering',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>'],
           'src': ['S18', 'S01', 'S44']},
          {'cells': ['Ceiling drywall opening',
                     'SF DBI lists minor wallboard repairs as exempt unless fire-protection related; exact '
                     'ceiling assembly/scope unknown',
                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                     'warn">UNVERIFIED</span>'],
           'src': ['S02', 'S96', 'S44']}],
 'caption': 'No access method, opening size or permit exemption is inferred. A licensed site assessment is '
            'required.'}
TABLES["repo_inventory"] = {'title': 'Line-by-line source/artifact inventory',
 'columns': ['Path', 'Bytes', 'SHA-256', 'Category', 'Review scope', 'Source'],
 'rows': [],
 'caption': 'Generated at build time.'}
for _r in TABLES["findings"]["rows"]:
    if _r["cells"][0] == "F02":
        _r["cells"][1] = "Below access is a publisher-described fallback for stubborn drains, not a verified project-specific norm"
        _r["cells"][2] = "This Old House describes below access for stubborn drains; the exact access route for this tub remains unverified"
        _r["cells"][3] = pill("publisher guidance / project unverified", "warn")
    if _r["cells"][0] == "F04":
        _r["cells"][1] = "All sixteen canonical candidates hold active CSLB licenses checked 2026-11-08"
        _r["cells"][2] = "The canonical CSLB dataset transcribes each official record and its retrieval stamp"
        _r["src"] = ["S85"]
    if _r["cells"][0] == "F05":
        _r["cells"][1] = "Drywall inclusion in the three owner-reported estimates is not stated"
        _r["cells"][2] = "The supplied wording does not confirm inclusion or exclusion; no combined plumbing + drywall quote is verified"
        _r["cells"][3] = pill("owner-provided / unverified", "warn")
        _r["src"] = ["S44"]
TABLES["flagged"]["rows"].extend([{'cells': ['U35',
            '[Integration audit] Drywall inclusion in the three owner-reported estimates',
            'The supplied wording does not state whether drywall/ceiling patch and finish is included; '
            'earlier blanket exclusions were unsupported',
            'Obtain written scope inclusions/exclusions for each estimate',
            '<span class="pill warn">UNVERIFIED</span>'],
  'src': ['S44']},
 {'cells': ['U36',
            '[Integration audit] No reference photos or model identification',
            'No photos, model number or inspection were supplied; assembly type and access route are not '
            'inferred',
            'Provide photos/model to the contractor for assessment; verified cells remain blank until then',
            '<span class="pill warn">UNVERIFIED</span>'],
  'src': ['S44', 'S93']},
 {'cells': ['U37',
            '[Integration audit] Permit applicability is not determined',
            'Official rules and exemptions are cited, but the exact concealed plumbing/ceiling scope has not '
            'been assessed by DBI',
            'Confirm scope and applicable requirements with DBI and the licensed contractor',
            '<span class="pill warn">UNVERIFIED</span>'],
  'src': ['S01', 'S02', 'S96', 'S94']},
 {'cells': ['U38',
            "[Integration audit] Manny's exact San Francisco service availability",
            'Company lists surrounding San Mateo & San Francisco Counties but not a specific SF address '
            'commitment; CSLB address is Daly City',
            'Confirm the job address is within the service area and obtain a written quote',
            '<span class="pill warn">UNVERIFIED</span>'],
  'src': ['S57', 'S75']},
 {'cells': ['U39',
            '[Integration audit] Handyman Heroes workers’ compensation classification codes',
            'CSLB #1003394 lists carpentry/high-low wage and clerical codes; adequacy for plumbing work is '
            'not established by the record',
            'Ask the carrier/contractor to confirm coverage for the actual plumbing crew',
            '<span class="pill warn">needs review</span>'],
  'src': ['S10', 'S91']},
 {'cells': ['U40',
            '[Integration audit] General SF crew and insurance',
            'CSLB #959843 shows a no-employee workers’ compensation exemption; a bond is not liability '
            'insurance',
            'Confirm crew identity, workers’ compensation and general liability coverage before work',
            '<span class="pill warn">verified fact / needs review</span>'],
  'src': ['S09', 'S91']},
 {'cells': ['U41',
            '[Integration audit] Public repository / Pages visibility',
            'GitHub Pages is public; only project-suitable content is published and requester-only context '
            'is excluded',
            'Review public artifacts before adding any sensitive material',
            '<span class="pill info">privacy boundary</span>'],
  'src': ['S46', 'S45']},
 {'cells': ['U42',
            '[Integration audit] Supplemental 8-provider conditional inquiry order is editorial',
            'The earlier 8-provider order is preserved as structured evidence; the primary published ranking '
            'is the computed 16-record CSLB rubric',
            'Re-rank after written quotes, references and site assessment',
            '<span class="pill info">analysis</span>'],
  'src': ['S91', 'S09', 'S10', 'S11']},
 {'cells': ['U43',
            '[Integration audit] Rapid Flow / Manny’s / Szeto review evidence',
            'No directly verified Yelp profile was established for these leads in this pass; review cells '
            'remain blank',
            'Locate and review platform profiles independently; do not infer ratings',
            '<span class="pill warn">UNVERIFIED</span>'],
  'src': ['S56', 'S57', 'S37', 'S04']}])
for _page, _ref, _idx in (("technical.html", "access_options", 1), ("repo-review.html", "repo_inventory", 1)):
    _sections = PAGES[_page]["sections"]
    if not any(_b.get("ref") == _ref for _b in _sections if _b["type"] == "table"):
        _sections.insert(_idx, {"type": "table", "ref": _ref})
PAGES["repo-review.html"]["sections"].insert(2, {'type': 'prose',
 'title': 'Integration audit downloads',
 'html': '<p><a href="data/canonical/evidence-2026-11-08.json">Current evidence extracts</a> · <a '
         'href="data/canonical/providers-2026-11-08.json">Supplemental 8-provider records</a> · <a '
         'href="data/canonical/research-history-2026-11-07.json">Prior canonical snapshot</a> · <a '
         'href="data/canonical/repo_inventory.csv">Repository inventory CSV</a>. The computed <a '
         'href="ranking.html">16-record ranking</a> remains the primary hiring decision.</p>'})
PAGES["sources.html"]["sections"].insert(len(PAGES["sources.html"]["sections"]) - 1, {'type': 'prose',
 'title': 'Integration evidence files',
 'html': '<p><a href="data/canonical/evidence-2026-11-08.json">Evidence extracts</a> · <a '
         'href="data/canonical/providers-2026-11-08.json">Provider records</a> · <a '
         'href="data/canonical/cslb_records.json">Canonical CSLB records</a> · <a '
         'href="data/canonical/vendor_sites.json">Business-site transcriptions</a> · <a '
         'href="data/canonical/review_snapshots.json">Review snapshots</a>.</p>'})
for _block in PAGES["index.html"]["sections"]:
    if _block["type"] == "cards":
        for _card in _block["items"]:
            if _card["k"] == "Flagged for review":
                _card["v"] = str(len(TABLES["flagged"]["rows"]))
for _page in PAGES.values():
    for _b in _page["sections"]:
        for _k, _v in list(_b.items()):
            if isinstance(_v, str):
                _b[_k] = _v.replace("U01–U34", "U01–U43").replace("34 flagged items", "43 flagged items")
META["session"] = "arena/52d35ede-korea7"

# --- Supplemental integration corrections — arena/6696a17e-korea7 (2026-11-08) ---
# Preserve the concurrent 16-record primary ranking while adding field-level checks
# and correcting source statements re-read in this session.
SOURCES["S22"].update({
    "checked": "2026-11-08",
    "supports": "Generic bathtub-drain repair range $80–$600, 1–4 hour duration, repair-vs-replacement table and hydrostatic/fill-and-inspect testing context",
    "note": "Re-read 2026-11-08. Houston/Galveston, Texas trade blog; publication date not shown. Its permit/licensing statements are NOT used as San Francisco guidance.",
})
SOURCES["S23"].update({
    "checked": "2026-11-08",
    "note": "Re-read directly 2026-11-08. Page states 'Last update on August 01, 2026' and 873 verified plumbing reviews. Platform reviews are not license verification.",
})
SOURCES["S24"].update({
    "checked": "2026-11-08",
    "supports": "SF bathtub-restoration category shows 17 verified reviews and last update October 14, 2024; review themes include older SF homes, apartment complexes and concealed leaks, but some listed firms are not candidates and one listing is explicitly unlicensed",
    "note": "Re-read directly 2026-11-08. Third-party customer statements; not license verification. It does not establish a candidate-specific tenant-occupied plumbing + drywall project.",
})
SOURCES["S101"] = {
    "label": "Advanced Plumbing & Drain Cleaning — New Jersey website (not matched)",
    "publisher": "AAA Advanced Plumbing & Drain Cleaning, Inc.",
    "url": "https://advancedplumbinganddrain.com/",
    "tier": "company",
    "status": "verified",
    "checked": "2026-11-08",
    "supports": "Fetched site describes a Totowa, New Jersey business serving Hudson/Passaic counties; phone (973) 278-1948",
    "note": "Read directly 2026-11-08. NOT matched to CSLB #1009195 (San Francisco). Used only to flag the identity mismatch.",
}
SOURCES["S102"] = {
    "label": "Field-level source checks (JSON)",
    "publisher": "This repository",
    "url": "data/canonical/source_checks.json",
    "tier": "primary",
    "status": "verified",
    "checked": "2026-11-08",
    "supports": "Exact CSLB timestamps, official phones/addresses/classes/status for 11 re-read records, company-page observations, rule sources and blocked Yelp fetches",
    "note": "Persisted 2026-11-08 from direct reads; no provider outreach.",
}
SOURCES["S103"] = {
    "label": "Supplemental evidence-strength decision analysis (JSON)",
    "publisher": "This dashboard",
    "url": "data/canonical/decision_analysis.json",
    "tier": "primary",
    "status": "verified",
    "checked": "2026-11-08",
    "supports": "Explicit weights, 0-2 evidence scores and weighted totals for a supplemental 10-candidate inquiry model",
    "note": "Analyst judgment from cited evidence; not the primary computed CSLB ranking, not an official rating or capability guarantee.",
}
SOURCES["S104"] = {
    "label": "Repository line-by-line audit artifact",
    "publisher": "This repository",
    "url": "data/canonical/repo_audit.md",
    "tier": "primary",
    "status": "verified",
    "checked": "2026-11-08",
    "supports": "Per-file inventory, text-line counts, parse checks, merge-marker/privacy/template-marker scan and irregularity flags",
    "note": "Generated by scripts/audit_repository.py; structural audit, not official validation of unrelated legacy claims.",
}
for _r in TABLES["platforms"]["rows"]:
    if _r["src"] == ["S24"]:
        _r["cells"][2] = "17 verified reviews; last update October 14, 2024; category-level customer statements, not candidate-specific capability"
        _r["cells"][3] = pill("read directly 2026-11-08", "ok")
TABLES["platforms"]["caption"] = (
    "Platform links are discovery aids, not proof that any firm can perform this delicate repair. Only "
    + slink("S04", "CSLB") + " verifies a California contractor license. Angi bathtub-restoration review text is "
    + "category-level third-party customer statement and is not treated as an official capability finding."
)
for _r in TABLES["requirements"]["rows"]:
    if _r["cells"][0] == "R16":
        _r["src"] = ["S44", "S40", "S43"]
for _r in TABLES["findings"]["rows"]:
    if _r["cells"][0] == "F08":
        _r["cells"][2] = "Fast Response site advertises apartments/HOAs/property managers; Ace site advertises HOAs/property managers; job-specific occupied-unit references remain unverified"
        _r["src"] = ["S40", "S43"]
for _r in TABLES["flagged"]["rows"]:
    if _r["cells"][0] == "U15":
        _r["src"] = ["S04", "S40", "S43"]
TABLES["flagged"]["rows"].append({
    "cells": [
        "U44",
        "Advanced Plumbing and Drain #1009195 website identity mismatch",
        "The fetched advancedplumbinganddrain.com site is a Totowa, New Jersey business, not the San Francisco CSLB #1009195 licensee",
        "Do not use that website for capability claims; obtain the correct business site/phone from the licensee and re-check CSLB",
        pill("irregularity", "warn"),
    ],
    "src": ["S65", "S101"],
})
TABLES["repo_review"]["rows"].append({
    "cells": [
        "Supplemental field-level audit",
        "This session adds exact CSLB timestamps for 11 re-read records, a supplemental evidence-strength model and a line-by-line repository audit",
        "Preserved alongside the concurrent 16-record primary ranking; structural checks are not official capability validation",
        pill("reviewed", "ok"),
    ],
    "src": ["S102", "S103", "S104"],
})
for _page in ("repo-review.html", "sources.html"):
    for _b in PAGES[_page]["sections"]:
        if _b.get("title") in ("Integration audit downloads", "Integration evidence files"):
            _b["html"] = _b["html"].replace(
                "</p>",
                " Supplemental: <a href=\"data/canonical/source_checks.json\">field-level source checks</a> · "
                "<a href=\"data/canonical/decision_analysis.json\">evidence-strength model</a> · "
                "<a href=\"data/canonical/repo_audit.md\">line-by-line repo audit</a>.</p>",
            )
for _page in PAGES.values():
    for _b in _page["sections"]:
        for _k, _v in list(_b.items()):
            if isinstance(_v, str):
                _b[_k] = _v.replace("U01–U43", "U01–U44").replace("43 flagged items", "44 flagged items")
for _b in PAGES["index.html"]["sections"]:
    if _b["type"] == "cards":
        for _card in _b["items"]:
            if _card["k"] == "Flagged for review":
                _card["v"] = str(len(TABLES["flagged"]["rows"]))
META["session"] = "arena/6696a17e-korea7"
PAGES["index.html"]["eyebrow"] = "Research dashboard · San Francisco · updated 2026-11-10"

# Dated delivery supplement; original model inputs and archived pages preserved.
import delivery_data as _delivery
_delivery.integrate(__import__(__name__))
