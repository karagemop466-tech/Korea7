"""Canonical content for the bathtub-overflow trip-lever research dashboard.

This module is the single source of truth for the canonical dashboard. It was
created by integration session `arena/2eb487ad-korea7` (2026-11-07) and taken
over by integration session `arena/e070be24-korea7` (2026-11-08), which
re-verified every CSLB record, added the Decision ranking page and refreshed
the flagged/repo-review items. Every fact that appears in a table row cites one
or more source ids from SOURCES. Values that cannot be confirmed from an
official source are left blank and flagged. Nothing here is inferred.

Retrieval dates are recorded per source in the `checked` field. CSLB License
Detail pages re-read on 2026-11-08 printed "Data current as of 11/8/2026".
"""

META = {
    "updated": "2026-11-08",
    "session": "arena/e070be24-korea7",
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
    {"group": "Data", "links": [
        ("estimates.html", "Estimates & costs"),
        ("contractors.html", "Contractors & reviews"),
        ("findings.html", "Findings & analysis"),
        ("ranking.html", "Decision ranking"),
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
    "S01": {"label": "SF.gov — Apply for a plumbing and mechanical permit", "publisher": "SF Dept. of Building Inspection", "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Permit requirement for cutting into/replacing pipes; license classes allowed to apply; inspection before covering pipes; homeowner R-3 restriction", "note": "Read directly on sf.gov, 2026-11-07; re-read 2026-11-08 — text unchanged (permit trigger, C4/C16/C20/C36/C54/B/A list, inspection before covering, R-3 homeowner rule, Permit Center 628-652-4900)."},
    "S02": {"label": "SF.gov — Check if your construction project needs a permit", "publisher": "SF Dept. of Building Inspection", "url": "https://www.sf.gov/information--check-if-your-construction-project-needs-permit", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Published list of work that does not need a permit, including minor repairs to existing interior plaster or wallboard", "note": "Read directly on sf.gov, 2026-11-07."},
    "S03": {"label": "SF Building/Plumbing Code — Section 104.0 Permits", "publisher": "American Legal Publishing code library (City and County of SF)", "url": "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Official code location for §104.2 exempt work referenced by sf.gov", "note": "Page title confirmed as 'SECTION 104.0 - PERMITS'. The code library page is JavaScript-heavy; the exemption text was not machine-parsed, so the link is provided for manual review and no section wording is quoted from it."},
    "S04": {"label": "CSLB — Check a License", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "tier": "official", "status": "verified", "checked": "2026-11-07", "supports": "Official license lookup by number or business name; CSLB advises checking status and complaint disclosure before hiring", "note": "Read directly on cslb.ca.gov, 2026-11-07."},
    "S05": {"label": "CSLB — C-36 Plumbing classification", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Official definition of the C-36 Plumbing classification (16 CCR, Div. 8, Art. 3)", "note": "Read directly on cslb.ca.gov, 2026-11-07; re-read 2026-11-08 — text unchanged (16 CCR Div. 8 Art. 3)."},
    "S06": {"label": "CSLB License Detail #977638 — Expert Plumbing Solutions", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:22 PM'; all values unchanged from the 2026-11-07 read. Business phone on record (415) 531-5340."},
    "S07": {"label": "CSLB License Detail #757796 — Bay Area Plumbing", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation exemption", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:52 PM'; all values unchanged. Business phone on record (415) 668-8000. Bond effective 2026-09-01."},
    "S08": {"label": "CSLB License Detail #1024971 — Fast Response Plumbing and Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' compensation policy dates", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:34 PM'; all values unchanged. Business phone on record (415) 596-6115. Workers' comp policy still shows expiry 12/18/2026."},
    "S09": {"label": "CSLB License Detail #959843 — GENERALSF", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/expiry dates, status, B/C10/C36 classifications, bond, workers' compensation exemption", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:52 PM'; all values unchanged. Business phone on record (650) 303-1515."},
    "S10": {"label": "CSLB License Detail #1003394 — Handyman Heroes Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/expiry dates, status, B/C36 classifications, bond, workers' compensation, complaint-disclosure flag", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:52 PM'; all values unchanged, complaint-disclosure link still present. Business phone on record (844) 382-4376."},
    "S11": {"label": "CSLB License Detail #829071 — Ace Plumbing & Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, address, entity, issue/reissue/expiry dates, status, A/B/C-4/C10/C16/C36 classifications, bond, workers' compensation", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:57 PM'; all values unchanged. Business phone on record (415) 824-6444. Bond effective 2026-09-04."},
    "S12": {"label": "CSLB Complaint Disclosure #1003394", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Citation 2 2020 001045, dated 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'", "note": "Read directly on cslb.ca.gov, 2026-11-07 and again 2026-11-08: one citation, 2 2020 001045, dated 07/12/2020, status 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'. Reported verbatim, no interpretation."},
    "S13": {"label": "California Business & Professions Code §7048", "publisher": "California Legislative Information (leginfo)", "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Current small-job licensing exemption: aggregate price under $1,000, casual/minor/inconsequential, and no building permit required; amended by Stats. 2025 ch. 67 (AB 1170), effective 2026-01-01", "note": "Read directly on leginfo, 2026-11-07; re-read 2026-11-08 — text unchanged: '(Amended by Stats. 2025, Ch. 67, Sec. 12. (AB 1170) Effective January 1, 2026.)'."},
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
    "S34": {"label": "Yelp — Fast Response Plumbing & Rooter", "publisher": "Yelp", "url": "https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3", "tier": "platform", "status": "blocked-403", "checked": "2026-11-08", "supports": "Business review page for one of the three quoting companies", "note": "HTTP 403 on automated fetch (2026-11-07 and 2026-11-08). A 2026-11-06 snapshot (4.8, 906 reviews) exists in prior-session notes; Yelp search-result text seen on 2026-11-08 showed 4.8 ★ (870). Neither value is verified on the listing page — flagged."},
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
    "S56": {"label": "CSLB License Detail #1115649 — Rapid Flow Plumbing & Rooter Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, 230 Edinburgh St SF 94112, corporation, issued 2024-01-29, expires 2028-01-31, B + C-36 classifications, $25,000 bond, workers'-compensation exemption", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:34 PM'; all values unchanged. Business phone on record (415) 866-8401."},
    "S57": {"label": "CSLB License Detail #841229 — Manny's Plumbing & Rooter", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Business name, 41 Midvale Drive Daly City CA 94015, sole ownership, issued 2004-06-21, expires 2028-06-30, C-36 + B classifications, $25,000 bond, workers'-compensation exemption", "note": "Re-read 2026-11-08: record printed 'Data current as of 11/8/2026 2:55:34 PM'; all values unchanged. Business phone on record (650) 207-5733. Daly City address — service area to be confirmed."},
    "S58": {"label": "Shortlist — who can do the plumbing and the drywall", "publisher": "This repository (parallel session)", "url": "shortlist.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Ranked shortlist of dual-classified (B + C-36) firms with a vetting script", "note": "Page produced by a concurrent session, merged unchanged and linked from the dashboard navigation."},
    "S60": {"label": "SF overflow audit — parallel session dashboard", "publisher": "This repository (parallel session)", "url": "sf-overflow-audit/index.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Independent 9-page audit dashboard with 11 CSLB records, Watco/Oatey technical notes and 15 flagged items", "note": "Disjoint file scope produced by session arena/2baecdab-korea7, merged unchanged; linked here in response to its cross-link request."},
    "S59": {"label": "Verification log — earlier session", "publisher": "This repository (parallel session)", "url": "verification-log.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Earlier session's line-by-line verification and correction log", "note": "Preserved verbatim from the add/add conflict on verification.html; linked from repo-review.html."},
    "S55": {"label": "Source ledger (this site)", "publisher": "This dashboard", "url": "sources.html", "tier": "primary", "status": "verified", "checked": "2026-11-07", "supports": "Documentation rows about sources removed from active citations", "note": "Internal page on this site. Dead URLs are shown there as plain text, never as links."},
    "S54": {"label": "InspectAndTest — bathtub overflow guide (DEAD)", "publisher": "InspectAndTest", "url": "https://inspectandtest.net/guides/bathtub-overflow-drain/", "tier": "publisher", "status": "dead", "checked": "2026-11-07", "supports": "Removed from all active citations", "note": "HTTP 500 on 2026-11-07. Not linked from any table row; retained here as a labeled documentation row."},
    # --- added by integration session arena/e070be24-korea7, all read directly on 2026-11-08 ---
    "S64": {"label": "CSLB License Detail #1025814 — The Genteel Plumbers Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1025814", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Corporation, 1181 Revere Ave, San Francisco, CA 94124, business phone (833) 436-8335; issued 2017-04-14, expires 2027-04-30; current and active; C-36 Plumbing + B General Building; $25,000 bond (American Contractors Indemnity, eff. 2023-01-01); workers' compensation insured (Technology Insurance Co., 2026-01-24 → 2027-01-24); no complaint-disclosure or additional-status line", "note": "Record printed 'Data current as of 11/8/2026 2:56:58 PM'. Candidate first identified by the sf-overflow-audit session; read directly here before inclusion."},
    "S65": {"label": "CSLB License Detail #995163 — Bernal Hill Drywall Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Corporation, 720 Anderson St, San Francisco, CA 94110, business phone (415) 533-8274; issued 2014-07-28, expires 2028-07-31; current and active; C-9 Drywall + B General Building; $25,000 bond; workers' compensation insured (Endurance Assurance, 2026-03-10 → 2027-03-10, class 5447 wallboard installation); no disclosure line", "note": "Record printed 'Data current as of 11/8/2026 2:58:18 PM'. Drywall specialist — not a plumbing candidate; listed as a ceiling-restoration partner option."},
    "S66": {"label": "CSLB License Detail #1009195 — Advanced Plumbing and Drain Inc", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1009195", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "Corporation, 3450 Sacramento St 204, San Francisco, CA 94118, business phone (415) 744-4944; expires 2027-11-30; current and active; C-36 only; Additional Status printed verbatim: 'The license may be suspended at a future date for failure to resolve an outstanding final liability from the Franchise Tax Board, Department of Industrial Relations, Employment Development Department, or the Contractors State License Board.'; workers' comp insured (Hartford, 2026-08-21 → 2027-08-21)", "note": "Record printed 'Data current as of 11/8/2026 2:58:23 PM'. Screened out of the ranking because of the official notice; reported verbatim, no interpretation."},
    "S67": {"label": "CSLB — B General Building classification (B&P §7057)", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "§7057(b): a general building contractor shall not take a prime contract for a project involving trades other than framing or carpentry unless it requires at least two unrelated trades, or unless the contractor holds the appropriate license classification or subcontracts with an appropriately licensed specialty contractor", "note": "Read directly on cslb.ca.gov, 2026-11-08. Basis for weighting B + C-36 on one license as the single-provider criterion."},
    "S68": {"label": "CSLB — C-9 Drywall classification", "publisher": "Contractors State License Board", "url": "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9", "tier": "official", "status": "verified", "checked": "2026-11-08", "supports": "A drywall contractor lays out and installs gypsum wall board and assemblies and performs taping and texturing (16 CCR Div. 8 Art. 3)", "note": "Read directly on cslb.ca.gov, 2026-11-08."},
    "S69": {"label": "Genteel Plumbers — official site", "publisher": "The Genteel Plumbers Inc", "url": "https://www.genteelplumbers.com/", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Company states: office at 1181 Revere Avenue, San Francisco (matches CSLB); phone 415-465-5853; dispatch fee $149 applied to the cost of services; same-day service in San Francisco and San Mateo County; does not cross the Golden Gate or Bay Bridge and does not serve the Financial District; founded 2016 by Graham W. Jones", "note": "Read directly. Company self-description is not independent verification; the license number was not printed on the fetched home page — license facts come from CSLB #1025814. Phone differs from the CSLB record — flagged."},
    "S70": {"label": "Rapid Flow Plumbing & Rooter — official site", "publisher": "Rapid Flow Plumbing & Rooter Inc", "url": "https://www.rapidflowbayarea.com/", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Company prints 'CA License #1115649 · B General Building · C-36 Plumbing', 230 Edinburgh St, San Francisco 94112, phones 844-BAY-FLOW and (415) 866-8401; lists general contracting (remodels, renovations), leak detection and repair, 'residential and commercial expertise', 'fully bonded'", "note": "Read directly. Company self-description is not independent verification; license, address and phone match CSLB #1115649."},
    "S71": {"label": "Manny's Plumbing & Rooters — official site", "publisher": "Manny's Plumbing & Rooter", "url": "https://www.mannysplumbingandremodeling.com/", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Company prints 'License # 841229', 'C-36 Plumbing / General B - Insured & Bonded'; services include tub install, drain clean and drain replacement, kitchen and bathroom remodeling, residential and commercial; serves nine San Mateo County cities 'and surrounding areas of San Mateo & San Francisco Counties'", "note": "Read directly. 'Insured' is a company statement; the CSLB record shows a workers'-compensation exemption ('no employees') — flagged for a certificate request."},
    "S72": {"label": "General SF — Building services page", "publisher": "General SF", "url": "https://generalsf.com/building", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Building page lists 'Sheetrock/Tape and Texture' and 'Rough and Finish Plumbing' among services; footer prints 'CSLB. 959843' and phone (650)-303-1515", "note": "Read directly. Company self-description is not independent verification; license and phone match CSLB #959843."},
    "S73": {"label": "Handyman Heroes — Handyman services page", "publisher": "Handyman Heroes Inc", "url": "https://www.handymanhero.es/handyman-services/", "tier": "company", "status": "verified", "checked": "2026-11-08", "supports": "Page states 'sheetrock and wall repairs', 'plumbing and electrical services', service to 'San Francisco homes and apartments', bathroom remodeling including tub and shower upgrades, license #1003394 and phone 1-844-382-4376; lists dated customer testimonials (latest 2026-11-06)", "note": "Read directly. Company self-description and testimonials are not independent verification; license and phone match CSLB #1003394."},
    "S74": {"label": "Yelp — Genteel Plumbers (two listings)", "publisher": "Yelp", "url": "https://www.yelp.com/biz/genteel-plumbers-san-francisco-7", "tier": "platform", "status": "blocked-403", "checked": "2026-11-08", "supports": "Search-result snapshot 2026-11-08: listing '-7' shows 4.7 ★ (519 reviews) at 1314 22nd Ave Ste 007, phone (415) 598-0562; a second listing '-8' shows 4.6 ★ (17 reviews) at 1181 Revere Ave, phone (415) 484-3631", "note": "Direct page fetch returned HTTP 403 on 2026-11-08; values come from Yelp search-result text and are third-party, point-in-time and unverified. Two listings for one company — flagged."},
    "S75": {"label": "Yelp — Ace Plumbing & Rooter", "publisher": "Yelp", "url": "https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco", "tier": "platform", "status": "blocked-403", "checked": "2026-11-08", "supports": "Search-result snapshot 2026-11-08: 4.7 ★ with 1.4k–1.5k reviews, 'Verified License', 'Serving San Francisco and the Surrounding Area'", "note": "Direct page fetch is blocked (HTTP 403); values are third-party and unverified. 'Verified License' is a platform badge, not CSLB verification."},
    "S76": {"label": "Yelp — Manny's Plumbing & Rooters", "publisher": "Yelp", "url": "https://www.yelp.com/biz/mannys-plumbing-and-rooter-daly-city", "tier": "platform", "status": "blocked-403", "checked": "2026-11-08", "supports": "Search-result snapshot 2026-11-08: 4.7 ★ (175 reviews), 41 Midvale Dr, Daly City, (650) 207-5733; the business's own specialties text lists 'tub and shower valve repair and install' and 'tub overflow repair and replacement'; 'Bathtub repair' appears under services 'Verified by Business'", "note": "Direct page fetch is blocked (HTTP 403); values are third-party and unverified. The specialties text is the business's own description on the platform."},
    "S77": {"label": "Yelp — Rapid Flow Plumbing (search)", "publisher": "Yelp", "url": "https://www.yelp.com/search?find_desc=Rapid+Flow+Plumbing&find_loc=San+Francisco%2C+CA", "tier": "platform", "status": "blocked-403", "checked": "2026-11-08", "supports": "Prior-session snapshot 2026-11-07: 5.0 ★ (8 reviews); not re-seen in 2026-11-08 search results", "note": "Direct fetch blocked (HTTP 403). Third-party, thin evidence (8 reviews) — treated as a low score on the review criterion, not as verification."},
    "S78": {"label": "GitHub Actions — Pages run 42413503253 for main @ 1faccdc (deploy failed)", "publisher": "GitHub (this repository)", "url": "https://github.com/karagemop466-tech/Korea7/actions/runs/42413503253", "tier": "primary", "status": "verified", "checked": "2026-11-08", "supports": "'pages build and deployment' for commit 1faccdc: build job success, deploy job failure; deployment 7626930247 went in_progress 2026-11-07T20:57:32Z and failure at 21:08:10Z", "note": "Checked with gh run view / gh api on 2026-11-08. The live site kept serving the previous successful deploy (08fa03b). Re-triggered by this session's merge."},
    "S79": {"label": "Open PR #42 (stale parallel session)", "publisher": "GitHub", "url": "https://github.com/karagemop466-tech/Korea7/pull/42", "tier": "primary", "status": "verified", "checked": "2026-11-08", "supports": "Open, mergeable=CONFLICTING, last updated 2026-11-08T20:41:27Z, branch arena/7e5f723c-korea7, overlaps the root dashboard pages", "note": "Checked with gh pr list on 2026-11-08. Not merged, closed or edited by this session (owned by another session). Four older GEMS-era PRs (#20, #18, #15, #2) are also open and conflicting."},
}


def pill(text, tone="info"):
    return '<span class="pill %s">%s</span>' % (tone, text)


def slink(sid, label=None):
    s = SOURCES[sid]
    text = label or s["label"]
    url = s["url"]
    if url.startswith("http"):
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (url, text)
    return '<a href="%s">%s</a>' % (url, text)


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
            {"cells": ["<strong>Expert Plumbing Solutions</strong><br>" + slink("S38", "site") + " · " + slink("S32", "Yelp"), slink("S06", "#977638"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2028-10-31", "Insured, policy effective 2026-07-19 → 2027-07-19; $25,000 bond", "1465 44th Avenue, San Francisco, CA 94122<br><small>Tel on CSLB record: (415) 531-5340</small>", "Quoted the full waste-and-overflow scope; C-36 covers plumbing work", pill("CSLB verified 2026-11-08", "ok")], "src": ["S06", "S38", "S05"]},
            {"cells": ["<strong>Bay Area Plumbing</strong><br>" + slink("S39", "site") + " · " + slink("S33", "Yelp"), slink("S07", "#757796"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-01-31", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "335 14th Avenue, San Francisco, CA 94118<br><small>Tel on CSLB record: (415) 668-8000</small>", "Quoted lever + spout/diverter scope; C-36 covers plumbing work", pill("CSLB verified 2026-11-08", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S07", "S39", "S05"]},
            {"cells": ["<strong>Fast Response Plumbing &amp; Rooter</strong><br>" + slink("S40", "site") + " · " + slink("S34", "Yelp"), slink("S08", "#1024971"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-03-31", "Insured, policy effective 2025-12-18 → " + pill("expires 2026-12-18", "warn") + "; $25,000 bond", "236 W POTRAL AVE #459, San Francisco, CA 94127<br><small>Tel on CSLB record: (415) 596-6115</small>", "Quoted the adjustment scope; site states service to apartments, HOAs and property managers", pill("CSLB verified 2026-11-08", "ok") + " " + pill("address mismatch flagged", "warn")], "src": ["S08", "S40", "S05"]},
            {"cells": ["<strong>GENERALSF</strong> (General SF)<br>" + slink("S41", "site") + " · " + slink("S35", "Yelp"), slink("S09", "#959843"), "B General Building · C-10 Electrical · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-04-30", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "3624 Irving Street Ste A, San Francisco, CA 94122<br><small>Tel on CSLB record: (650) 303-1515</small>", "One license lists both building and plumbing classifications — matches the single-provider requirement", pill("CSLB verified 2026-11-08", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S09", "S41", "S05"]},
            {"cells": ["<strong>Handyman Heroes Inc</strong><br>" + slink("S42", "site") + " · " + slink("S36", "Yelp"), slink("S10", "#1003394"), "B General Building · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-05-31", "Insured, policy effective 2026-04-25 → 2027-04-25; $25,000 bond", "912 Cole St # 202, San Francisco, CA 94117<br><small>Tel on CSLB record: (844) 382-4376</small>", "One license lists building + plumbing; official CSLB complaint disclosure exists", pill("CSLB verified 2026-11-08", "ok") + " " + pill("disclosure flagged", "warn")], "src": ["S10", "S12", "S42"]},
            {"cells": ["<strong>Ace Plumbing &amp; Rooter Inc</strong><br>" + slink("S43", "site") + " · " + slink("S75", "Yelp"), slink("S11", "#829071"), "A · B · C-4 · C-10 · C-16 · C-36", pill("current and active", "ok") + "<br>expires 2027-06-30", "Insured, policy effective 2026-07-13 → 2027-07-13; $25,000 bond", "1090 Bryant Street, San Francisco, CA 94103-4417<br><small>Tel on CSLB record: (415) 824-6444</small>", "Broadest verified classification set including B + C-36; site describes HOA/property-manager service", pill("CSLB verified 2026-11-08", "ok")], "src": ["S11", "S43", "S05"]},
            {"cells": ["<strong>Rapid Flow Plumbing &amp; Rooter Inc</strong><br>" + slink("S70", "site") + " · " + slink("S77", "Yelp") + " · " + slink("S58", "shortlist"), slink("S56", "#1115649"), "B General Building · C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2028-01-31", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "230 Edinburgh St, San Francisco, CA 94112<br><small>Tel on CSLB record: (415) 866-8401</small>", "One license lists building + plumbing; added from the concurrent shortlist session and re-verified here", pill("CSLB verified 2026-11-08", "ok") + " " + pill("WC exemption flagged", "warn")], "src": ["S56", "S05", "S58"]},
            {"cells": ["<strong>Manny's Plumbing &amp; Rooter</strong><br>" + slink("S71", "site") + " · " + slink("S76", "Yelp") + " · " + slink("S58", "shortlist"), slink("S57", "#841229"), "C-36 Plumbing · B General Building", pill("current and active", "ok") + "<br>expires 2028-06-30", pill("exempt — “no employees at this time”", "warn") + "; $25,000 bond", "41 Midvale Drive, Daly City, CA 94015<br><small>Tel on CSLB record: (650) 207-5733</small>", "One license lists plumbing + building; address is outside San Francisco proper — confirm service area", pill("CSLB verified 2026-11-08", "ok") + " " + pill("service area flagged", "warn")], "src": ["S57", "S05", "S58"]},
            {"cells": ["<strong>The Genteel Plumbers Inc</strong><br>" + slink("S69", "site") + " · " + slink("S74", "Yelp"), slink("S64", "#1025814"), "C-36 Plumbing · B General Building", pill("current and active", "ok") + "<br>expires 2027-04-30", "Insured, policy effective 2026-01-24 → 2027-01-24; $25,000 bond", "1181 Revere Ave, San Francisco, CA 94124<br><small>Tel on CSLB record: (833) 436-8335</small>", "One license lists plumbing + building and workers' comp is insured; company site confirms the Revere Ave office, states a $149 dispatch fee credited to the work, and says it does not serve the Financial District; company phone differs from the CSLB record", pill("CSLB verified 2026-11-08", "ok") + " " + pill("phone mismatch flagged", "warn")], "src": ["S64", "S69", "S05", "S67"]},
            {"cells": ["<strong>Bernal Hill Drywall Inc</strong> — drywall partner option, not a plumber", slink("S65", "#995163"), "C-9 Drywall · B General Building", pill("current and active", "ok") + "<br>expires 2028-07-31", "Insured, policy effective 2026-03-10 → 2027-03-10 (class 5447 wallboard); $25,000 bond", "720 Anderson St, San Francisco, CA 94110<br><small>Tel on CSLB record: (415) 533-8274</small>", "No plumbing classification — cannot do the trip-lever work; listed only as a licensed, insured ceiling cut/patch/finish partner if a C-36-only plumber is chosen", pill("CSLB verified 2026-11-08", "ok") + " " + pill("not a plumbing candidate", "info")], "src": ["S65", "S68", "S67"]},
            {"cells": ["<strong>Advanced Plumbing and Drain Inc</strong> — screened out", slink("S66", "#1009195"), "C-36 Plumbing", pill("current and active", "ok") + "<br>expires 2027-11-30<br>" + pill("official notice: may be suspended at a future date", "bad"), "Insured, policy effective 2026-08-21 → 2027-08-21; $25,000 bond", "3450 Sacramento St 204, San Francisco, CA 94118<br><small>Tel on CSLB record: (415) 744-4944</small>", "Excluded from the ranking: the CSLB record carries an 'Additional Status' notice about an unresolved final liability (quoted verbatim on the source ledger); C-36 only", pill("CSLB verified 2026-11-08", "ok") + " " + pill("screened out", "bad")], "src": ["S66", "S05"]},
        ],
        "caption": "Every license fact (status, classifications, expiry, bond, workers' compensation, address, business phone) was read from the linked official CSLB License Detail page; the first eight records were read on 2026-11-07 and re-read on 2026-11-08 with no changes, and the last three were read on 2026-11-08 — each record printed a 'Data current as of 11/8/2026' stamp. Phone numbers are the business phone printed on the CSLB record; company-site or platform phones that differ are flagged. The Analysis column is this site's reasoning from those verified classifications — not a vendor promise and not a finding that any firm can perform this specific repair. C-36 definition: " + slink("S05", "CSLB C-36") + ". Re-check any license at " + slink("S04", "CSLB Check a License") + " on the hire date.",
    },
    "review_snapshots": {
        "title": "Review-platform snapshots (not independently verified)",
        "columns": ["Candidate", "Prior-session Yelp snapshot (2026-11-06)", "Re-check 2026-11-07 / 2026-11-08 (search-result text only)", "Official license source", "Status", "Source"],
        "rows": [
            {"cells": ["Expert Plumbing Solutions", "4.8 ★ (81 reviews)", BLANK + " " + UNVERIFIED, slink("S06", "CSLB #977638"), SNAPSHOT], "src": ["S32", "S06"]},
            {"cells": ["Bay Area Plumbing", "4.8 ★ (175 reviews)", BLANK + " " + UNVERIFIED, slink("S07", "CSLB #757796"), SNAPSHOT], "src": ["S33", "S07"]},
            {"cells": ["Fast Response Plumbing &amp; Rooter", "4.8 ★ (906 reviews)", "2026-11-08 search-result text: 4.8 ★ (870) " + pill("third-party, unverified", "warn"), slink("S08", "CSLB #1024971"), SNAPSHOT], "src": ["S34", "S08"]},
            {"cells": ["GENERALSF", "4.8 ★ (336 reviews)", BLANK + " " + UNVERIFIED, slink("S09", "CSLB #959843"), SNAPSHOT], "src": ["S35", "S09"]},
            {"cells": ["Handyman Heroes Inc", "4.7 ★ (410 reviews)", BLANK + " " + UNVERIFIED, slink("S10", "CSLB #1003394"), SNAPSHOT], "src": ["S36", "S10"]},
            {"cells": ["Ace Plumbing &amp; Rooter Inc", "4.7 ★ (1.4k reviews)", "2026-11-08 search-result text: 4.7 ★ (1.5k) " + pill("third-party, unverified", "warn"), slink("S11", "CSLB #829071"), SNAPSHOT], "src": ["S75", "S11"]},
            {"cells": ["The Genteel Plumbers Inc", BLANK + " (not in the 2026-11-06 snapshot)", "2026-11-08 search-result text: listing '-7' 4.7 ★ (519); listing '-8' 4.6 ★ (17) " + pill("two listings — flagged", "warn") + " " + UNVERIFIED, slink("S64", "CSLB #1025814"), SNAPSHOT], "src": ["S74", "S64"]},
            {"cells": ["Manny's Plumbing &amp; Rooters", BLANK + " (not in the 2026-11-06 snapshot)", "2026-11-08 search-result text: 4.7 ★ (175); business's own specialties text lists 'tub overflow repair and replacement' " + pill("third-party, unverified", "warn") + " " + UNVERIFIED, slink("S57", "CSLB #841229"), SNAPSHOT], "src": ["S76", "S57"]},
            {"cells": ["Rapid Flow Plumbing &amp; Rooter Inc", BLANK + " (not in the 2026-11-06 snapshot)", "2026-11-07 shortlist-session snapshot: 5.0 ★ (8); not re-seen 2026-11-08 " + pill("thin evidence", "warn") + " " + UNVERIFIED, slink("S56", "CSLB #1115649"), SNAPSHOT], "src": ["S77", "S56"]},
            {"cells": ["Szeto Plumbing and Handyman (Daly City)", "4.8 ★ (89 reviews)", BLANK + " " + UNVERIFIED, BLANK + " " + pill("no CSLB record found", "warn"), SNAPSHOT], "src": ["S37", "S04"]},
            {"cells": ["Fast Response — company's own aggregate claim", "“4.9 · 1,500 Reviews on Yelp &amp; Google”", BLANK + " " + UNVERIFIED, slink("S08", "CSLB #1024971"), pill("company claim — flagged", "warn")], "src": ["S40", "S34"]},
        ],
        "caption": "Yelp blocks direct page access with HTTP 403 in this environment, so no rating could be confirmed from a listing page on 2026-11-07 or 2026-11-08. The left column reproduces a 2026-11-06 snapshot recorded by an earlier session; the re-check column is blank where nothing new was seen and otherwise quotes Yelp search-result text captured on 2026-11-08 — third-party, point-in-time and unverified. Review counts change daily. Platform badges and company aggregates are not CSLB license verification. See the Flagged for Review page.",
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
            {"cells": ["R21", "Every table row has an official source link; unconfirmable values are blank and flagged", "Verification", BLANK + " " + UNVERIFIED, pill("enforced by build + verify scripts", "ok")], "src": ["S44", "S45"]},
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
            {"cells": ["F04", "All nine plumbing candidates hold active CSLB licenses, re-verified 2026-11-08 with no changes since 2026-11-07", "Nine official License Detail pages each print 'current and active' and a 'Data current as of 11/8/2026' stamp; the ninth (#1025814) was added on 2026-11-08", pill("verified", "ok")], "src": ["S06", "S07", "S08", "S09", "S10", "S11", "S56", "S57", "S64"]},
            {"cells": ["F05", "Drywall/ceiling work is not included in any of the three quoted scopes", "Owner brief scopes; Angi lists new drywall ≈ $2,100 and post-leak patching $300–$930 as separate costs", pill("analysis", "info") + " " + pill("no drywall quote exists", "warn")], "src": ["S44", "S15", "S16"]},
            {"cells": ["F06", "Two licenses show a workers'-compensation exemption 'no employees', and one policy expires 2026-12-18", "CSLB #757796, #959843, #1024971", pill("verified on CSLB", "ok") + " " + pill("flagged", "warn")], "src": ["S07", "S09", "S08"]},
            {"cells": ["F07", "Review counts and badges are not license verification", "Yelp HTTP 403; Thumbtack 'Licensed pro' badge; BBB states it does not verify third-party information; CSLB is the authority", pill("verified sources", "ok")], "src": ["S04", "S27", "S28", "S29"]},
            {"cells": ["F08", "Occupied-unit / property-manager experience is only partially documented", "Fast Response site (apartments, HOAs, property managers), Ace site (HOAs/property managers), Angi SF review mentions a tenant-occupied multi-unit project", pill("company/review statements only", "warn")], "src": ["S40", "S43", "S24"]},
            {"cells": ["F09", "Two previously cited sources are dead and were removed from all active claims", "SFGate redirect to empty page; InspectAndTest HTTP 500 — both re-checked 2026-11-07", pill("irregularity — flagged", "warn")], "src": ["S55", "S45"]},
            {"cells": ["F10", "The repository's root content belongs to an unrelated legacy project", "README describes a DOE GEMS fault-prospectivity audit; legacy site remains under docs/", pill("irregularity — flagged", "warn")], "src": ["S47", "S48"]},
            {"cells": ["F11", "Recommended shortlist order: firms whose verified classes cover both building and plumbing first", "Six verified B + C-36 licenses: " + slink("S11", "#829071") + ", " + slink("S64", "#1025814") + ", " + slink("S10", "#1003394") + ", " + slink("S09", "#959843") + ", " + slink("S57", "#841229") + ", " + slink("S56", "#1115649") + "; B&amp;P §7057(b) is why one license covering both trades matters", pill("recommendation", "info")], "src": ["S11", "S64", "S10", "S09", "S57", "S56", "S67", "S58"]},
            {"cells": ["F12", "Decision ranking (1–9): Ace, Genteel, Handyman Heroes, General SF, Manny's, Rapid Flow, then the three C-36-only firms Fast Response, Expert, Bay Area", "Weighted score out of 100 over seven published criteria (license coverage 30, workers' comp 15, official record 15, address 10, cost evidence 10, company-page statements 10, review snapshot 10); every input is cited on the <a href=\"ranking.html\">Decision ranking</a> page", pill("analysis", "info") + " " + pill("weights are this site's own; no provider contacted", "warn")], "src": ["S11", "S64", "S10", "S09", "S57", "S56", "S08", "S06", "S07", "S67"]},
            {"cells": ["F13", "One C-36-only candidate carries an official CSLB notice and was screened out", "CSLB #1009195 prints 'The license may be suspended at a future date for failure to resolve an outstanding final liability…' (quoted verbatim, no interpretation)", pill("verified on CSLB", "ok") + " " + pill("screened out", "bad")], "src": ["S66"]},
            {"cells": ["F14", "Genteel's phone and Yelp presence are inconsistent across sources", "CSLB business phone (833) 436-8335; company site 415-465-5853; Yelp shows two listings with two more numbers and two addresses", pill("irregularity — flagged", "warn")], "src": ["S64", "S69", "S74"]},
            {"cells": ["F15", "The previous main deploy (1faccdc) failed at the deploy step while the build succeeded; the live site kept serving the prior deploy", "GitHub Actions run 42413503253: build success, deploy failure 2026-11-07T21:08:10Z; resolved by re-deploying from this session's merge (see Verification)", pill("irregularity — flagged", "warn")], "src": ["S78", "S45"]},
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
            {"cells": ["U06", "Workers'-compensation exemptions on #757796, #959843, #1115649 and #841229", "All four CSLB records state the licensee certified 'no employees at this time' (re-read 2026-11-08); Manny's company site nevertheless says 'Insured &amp; Bonded'", "Confirm in writing who will be on site and what coverage applies to the crew; request a certificate of insurance", pill("verified fact / needs review", "warn")], "src": ["S07", "S09", "S56", "S57"]},
            {"cells": ["U07", "Handyman Heroes CSLB complaint disclosure", "CSLB shows citation 2 2020 001045 dated 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6' — reported verbatim, no interpretation", "Open the official disclosure yourself and decide before hiring", pill("verified fact / needs review", "warn")], "src": ["S12", "S10"]},
            {"cells": ["U08", "Handyman Heroes site claims 'Licensed C-10'", "The official CSLB #1003394 record lists B and C-36 only", "Ask the company which license covers electrical work", pill("irregularity", "warn")], "src": ["S42", "S10"]},
            {"cells": ["U09", "Fast Response company aggregate '4.9 / 1,500 Reviews on Yelp &amp; Google'", "Company self-claim combining two platforms; Yelp page could not be re-fetched", "Re-open each platform separately", pill("irregularity", "warn")], "src": ["S40", "S34"]},
            {"cells": ["U10", "Szeto Plumbing and Handyman — license not found", "A prior session's CSLB name search on 2026-11-06 found no record; not re-verified on 2026-11-07, and the business is in Daly City with a 310 area code", "Ask for a CSLB number and verify it directly, or drop the candidate", pill("unverified", "warn")], "src": ["S37", "S04"]},
            {"cells": ["U11", "Two dead source URLs from earlier sessions", "SFGate Home Guides redirects to an empty page; InspectAndTest returns HTTP 500 (both re-checked 2026-11-07)", "Removed from all active citations; retained only as labeled documentation rows on the Source ledger", pill("resolved / documented", "ok")], "src": ["S55", "S45"]},
            {"cells": ["U12", "Repository content mismatch", "The README and docs/ describe an unrelated DOE GEMS fault-prospectivity audit; this dashboard occupies the site root", "No action required; legacy files deliberately untouched", pill("irregularity", "warn")], "src": ["S47", "S48"]},
            {"cells": ["U13", "Stale conflicting PR #32 from a parallel session", "Open since 2026-11-06, mergeable=CONFLICTING, also touches index.html; left untouched and not merged or closed by this session", "Owner may close or rebase it after this integration", pill("needs review", "warn")], "src": ["S52", "S45"]},
            {"cells": ["U14", "No combined written quote for plumbing + drywall exists", "No official or company source publishes a combined scope for this job", "Request one contingent written scope covering above-attempt, below access, ceiling cut/patch/finish and tenant coordination", UNVERIFIED], "src": ["S44", "S15", "S16"]},
            {"cells": ["U15", "Job-specific capability, tenant-occupied experience and service-area confirmation", "CSLB verifies license classes, not the ability to perform this specific delicate repair; company sites and reviews are self- or customer statements", "Ask each shortlisted firm for references on concealed waste-and-overflow work in occupied units", UNVERIFIED], "src": ["S04", "S24", "S40", "S43"]},
            {"cells": ["U16", "Yelp “Verified License” badges are third-party", "A platform badge is not CSLB verification; Yelp returned HTTP 403 on re-check", "Verify the license number directly on CSLB", pill("irregularity", "warn")], "src": ["S36", "S04", "S29"]},
            {"cells": ["U17", "Handyman Heroes address mismatch", "Official CSLB #1003394 lists 912 Cole St # 202; the prior Yelp snapshot lists 1525 Waller St", "Ask the company for its current service address", pill("irregularity", "warn")], "src": ["S10", "S36"]},
            {"cells": ["U18", "Outdated $500 contractor-licensing references", "Widely repeated older $500 figures are outdated; current B&amp;P §7048 (AB 1170, effective 2026-01-01) uses under $1,000 and no building permit required", "Use the current statutory text linked here", pill("resolved / documented", "ok")], "src": ["S13"]},
            {"cells": ["U19", "Repository scope: earlier research sets are historical", "Earlier dashboards under docs/ and bathtub-overflow/ are archived. A previously reported legacy link docs/parallel-index.html → docs/results/ resolves; no change made", "No action required; historical pages untouched", pill("needs review", "warn")], "src": ["S45", "S47", "S48"]},
            {"cells": ["U20", "No provider has been contacted and none has confirmed this job", "This is desk research; no capability, availability, price or service-area confirmation exists from any provider", "Contact shortlisted firms with the written scope", UNVERIFIED], "src": ["S44", "S45", "S58"]},
            {"cells": ["U23", "Previous Pages deploy of main failed", "Run 42413503253 for main @ 1faccdc: build success, deploy failure (2026-11-07T21:08:10Z); the live site kept serving the earlier deploy 08fa03b", "Re-deploy from the next merge to main and confirm the Actions run and the deployment status both succeed — recorded on the Verification page and the coordination board", pill("irregularity", "warn")], "src": ["S78", "S45"]},
            {"cells": ["U24", "Genteel Plumbers phone and Yelp listings inconsistent", "CSLB #1025814 business phone (833) 436-8335; company site prints 415-465-5853; Yelp shows two listings (4.7 ★/519 at 1314 22nd Ave with (415) 598-0562, and 4.6 ★/17 at 1181 Revere Ave with (415) 484-3631)", "Call the CSLB-record number first and ask the company which listing and number are current", pill("irregularity", "warn") + " " + UNVERIFIED], "src": ["S64", "S69", "S74"]},
            {"cells": ["U25", "Advanced Plumbing and Drain Inc — official CSLB notice", "CSLB #1009195 prints an 'Additional Status' line stating the license may be suspended at a future date for failure to resolve an outstanding final liability", "Screened out of the ranking; re-read the record before any contact", pill("irregularity", "bad")], "src": ["S66"]},
            {"cells": ["U26", "Five stale open pull requests, all conflicting", "PR #42 (parallel dashboard session, updated 2026-11-08) and GEMS-era PRs #20, #18, #15, #2 are open with mergeable=CONFLICTING; none was merged, closed or edited by this session", "Owners of those branches should rebase onto main or close them; the canonical dashboard is on main", pill("irregularity", "warn")], "src": ["S79", "S45", "S47"]},
            {"cells": ["U27", "Decision ranking is documentation-based", "Weights (30/15/15/10/10/10/10) are this site's own; company-page and review criteria rest on self-statements and third-party snapshots; no provider was contacted, no site visit occurred and no combined plumbing + drywall quote exists", "Treat the ranking as a calling order, not a selection; re-score after written quotes arrive", pill("analysis", "info") + " " + UNVERIFIED], "src": ["S67", "S11", "S64", "S44"]},
            {"cells": ["U28", "Time-sensitive expiries among candidates", "Fast Response workers' comp policy expires 2026-12-18 (#1024971); Bay Area Plumbing license expires 2027-01-31 (#757796); Genteel workers' comp expires 2027-01-24 (#1025814)", "Re-read each CSLB record on the hire date and request a current certificate of insurance", pill("verified on CSLB", "ok") + " " + pill("time-sensitive", "warn")], "src": ["S08", "S07", "S64"]},
            {"cells": ["U29", "Review-platform figures are search-result text, not listing pages", "Every 2026-11-08 review figure (Ace 4.7/1.5k, Genteel 4.7/519, Manny's 4.7/175, Fast Response 4.8/870) was read from Yelp search-result text because listing pages return HTTP 403", "Open each linked listing manually on the decision date", pill("third-party", "warn") + " " + UNVERIFIED], "src": ["S75", "S74", "S76", "S34"]},
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
            {"cells": ["Open PRs", "PR #32 (parallel session) was open and conflicting on 2026-11-07; on 2026-11-08 PR #42 (parallel dashboard session) plus GEMS-era #20, #18, #15 and #2 are open, all mergeable=CONFLICTING", "Checked with gh pr list on 2026-11-07 and 2026-11-08; none merged, closed or edited by either integration session", pill("needs review", "warn")], "src": ["S52", "S79"]},
            {"cells": ["Pages deploy history", "The 2026-11-07 merge of PR #46 → main @ 1faccdc built successfully but its deploy job failed after about 11 minutes; GitHub kept serving the previous deploy (08fa03b) and the Pages API reported status 'errored'", "Checked with gh run view 42413503253 and gh api repos/…/pages on 2026-11-08; job logs could not be downloaded from this sandbox", pill("irregularity — re-deployed by this session", "warn")], "src": ["S78", "S45"]},
            {"cells": ["Re-verification 2026-11-08", "All eight CSLB records cited on 2026-11-07 were re-read on 2026-11-08 (stamp 'Data current as of 11/8/2026'): no change in status, classifications, expiry, bond, workers' comp or address; three further records (#1025814, #995163, #1009195) were read and added; sf.gov, CSLB classification pages and B&amp;P §7048 re-read unchanged", "Per-source dates and notes are on the Sources page; the Verification page's checks were re-run after the content update", pill("re-verified", "ok")], "src": ["S06", "S07", "S08", "S09", "S10", "S11", "S56", "S57", "S64", "S65", "S66", "S01", "S13"]},
            {"cells": ["Decision ranking page", "No formal scored ranking existed: shortlist.html lists dual-classified firms without weights or cost explanations and the findings table gave an unscored order", "ranking.html was added, generated from the same data file as every other page; its criteria, weights, scores and cost notes are in tables with source links and its limitations are flagged (U27)", pill("added 2026-11-08", "ok")], "src": ["S58", "S67", "S45"]},
            {"cells": ["Pages configuration", "GitHub Pages builds from branch main, path / (legacy build type); .nojekyll is present at the repo root", "Confirmed with gh api repos/.../pages on 2026-11-07", pill("verified", "ok")], "src": ["S46"]},
            {"cells": ["Tests / scripts", "Existing Python scripts and tests belong to the legacy GEMS project; pytest is not installed in this sandbox", "This session added standalone unittest-based dashboard checks runnable with python3", pill("reviewed", "ok")], "src": ["S47"]},
            {"cells": ["Privacy sweep", "A grep for internal-only hiring constraints across all published HTML/MD/JSON/CSS/JS returned zero matches", "See the Verification page for the exact pattern list and result", pill("pass", "ok")], "src": ["S45"]},
            {"cells": ["Concurrent session output", "shortlist.html (ranked B + C-36 candidates and vetting script), verification-log.html (earlier line-by-line log) and sf-overflow-audit/ (independent 9-page audit) were merged and preserved unchanged", "All three are linked from the dashboard navigation, quick links and this review page", pill("preserved", "ok")], "src": ["S58", "S59", "S60", "S45"]},
        ],
        "caption": "Repo review was performed by reading the files in the checkout and querying the GitHub API. Links point to the repository files and Pages site for manual review. Irregularities are also published on the Flagged for Review page.",
    },
    "ranking_criteria": {
        "title": "Ranking criteria and weights (this site's own decision model)",
        "columns": ["ID", "Criterion", "Weight", "Scoring rule", "Why it matters (basis)", "Input quality", "Source"],
        "rows": [
            {"cells": ["C1", "Both trades on one license", "30", "B General Building + C-36 Plumbing on the same CSLB record = 30 · C-36 only = 5 · no C-36 = not ranked", "The brief asks for one provider covering plumbing and drywall. B&amp;P §7057(b) limits a general building contractor's prime contracts to projects with two or more unrelated trades unless it holds the specialty classification or subcontracts it; C-36 covers the trip-lever work itself", pill("official basis", "ok")], "src": ["S67", "S05", "S44"]},
            {"cells": ["C2", "Workers' compensation on record", "15", "Insured policy on the CSLB record = 15 · exemption 'no employees' = 5", "Work in an occupied building with a ceiling opening is more than a one-person task; an exemption means any helper on site is not covered by a policy CSLB knows about", pill("official basis", "ok")], "src": ["S04", "S07", "S09", "S56", "S57"]},
            {"cells": ["C3", "Official record", "15", "No disclosure or additional-status line = 15 · complaint disclosure only (B&amp;P §7124.6) = 7 · suspension notice = 0 and screened out", "Read verbatim from CSLB; the 2020 disclosure on #1003394 is reported, not interpreted", pill("official basis", "ok")], "src": ["S12", "S10", "S66"]},
            {"cells": ["C4", "Address on record", "10", "San Francisco address on the CSLB record = 10 · adjacent (Daly City) = 7", "Proximity for a repeat-visit job (above attempt, below access, patch, finish, water test) in a tenant-occupied unit", pill("official basis", "ok")], "src": ["S06", "S57", "S44"]},
            {"cells": ["C5", "Cost evidence for this job", "10", "Owner-held quote for the full waste-and-overflow scope = 10 · quote for a different scope = 8 · adjust-only quote = 4 · published dispatch fee only = 3 · nothing = 0", "Rewards firms whose price for this job is at least partly known; quote amounts are owner-provided and unverified, so this criterion scores the existence and scope of evidence, not its accuracy", pill("owner-provided inputs", "warn") + " " + UNVERIFIED], "src": ["S44", "S69", "S15"]},
            {"cells": ["C6", "Company-page statements", "10", "Page states apartments / HOAs / property managers = 10 · states residential + commercial = 5 · page read, trades listed, no occupancy statement = 3 · no page = 0", "Closest available proxy for occupied-unit experience; every value is a self-statement and is labeled as such", pill("company statements", "warn")], "src": ["S40", "S43", "S73", "S39", "S70", "S71", "S38", "S72", "S69"]},
            {"cells": ["C7", "Third-party review snapshot", "10", "≥ 4.5 ★ with ≥ 300 reviews = 10 · 100–299 reviews = 8 · fewer than 100 = 4 · none = 0", "Volume-weighted customer feedback; all figures are point-in-time Yelp search-result or prior-session snapshots because listing pages return HTTP 403 — third-party and unverified", pill("third-party", "warn") + " " + UNVERIFIED], "src": ["S75", "S74", "S36", "S35", "S76", "S77", "S34", "S32", "S33"]},
        ],
        "caption": "Weights sum to 100 and are this site's own judgment for this brief; they are not an official or industry standard. Ties are broken by the first differing criterion in the order C1 → C7. Change the weights and the order can change — see the sensitivity notes below the tables.",
    },
    "ranking_scores": {
        "title": "Score sheet — points per criterion (computed from the inputs above)",
        "columns": ["Rank", "Company", "C1 license (30)", "C2 workers' comp (15)", "C3 record (15)", "C4 address (10)", "C5 cost evidence (10)", "C6 company page (10)", "C7 reviews (10)", "Total / 100", "Source"],
        "rows": [],  # generated below from RANKING_INPUTS
        "caption": "Each cell shows the points awarded under the rule in the criteria table. Inputs: CSLB License Detail pages (C1–C4), the owner's brief and company pricing statements (C5), company pages (C6) and review snapshots (C7). C5–C7 rest on owner-provided, self-stated or third-party inputs and are flagged as such.",
    },
    "ranking": {
        "title": "Decision ranking — best choice first, with reasoning and cost per rank",
        "columns": ["Rank", "Company · CSLB license · phone on record", "Score", "Why this rank", "Cost position for this job", "Caveats", "Source"],
        "rows": [],  # generated below from RANKING_INPUTS
        "caption": "Phone numbers are the business phone printed on the official CSLB record (a company-site number that differs is noted). 'Cost position' repeats the owner-held quotes (unverified) and the published 2026 benchmarks; where no quote exists the cell is blank and marked UNVERIFIED — nothing is estimated. This is a calling order from desk research, not a selection; no provider has been contacted.",
    },
    "ranking_excluded": {
        "title": "Not ranked — and why",
        "columns": ["Company", "Reason", "Official source", "Status", "Source"],
        "rows": [
            {"cells": ["Advanced Plumbing and Drain Inc (#1009195)", "CSLB record prints an 'Additional Status' notice that the license may be suspended at a future date for failure to resolve an outstanding final liability; C-36 only", slink("S66", "CSLB #1009195"), pill("screened out", "bad")], "src": ["S66"]},
            {"cells": ["Bernal Hill Drywall Inc (#995163)", "C-9 Drywall + B, no C-36 — cannot do the trip-lever work; listed as a licensed, insured ceiling cut/patch/finish partner if a C-36-only plumber is chosen (ranks 7–9)", slink("S65", "CSLB #995163") + " · " + slink("S68", "C-9 definition"), pill("partner option, not a candidate", "info")], "src": ["S65", "S68"]},
            {"cells": ["Szeto Plumbing and Handyman (Daly City)", "Appears only in a 2026-11-06 Yelp snapshot (4.8 ★, 89 reviews); no CSLB record was found under that name, so no license fact can be cited", slink("S04", "CSLB Check a License") + " · " + slink("S37", "Yelp snapshot"), BLANK + " " + UNVERIFIED], "src": ["S37", "S04"]},
        ],
        "caption": "Exclusions are based on the cited official record or on the absence of one. Nothing here is a finding of wrongdoing; the CSLB notice is quoted verbatim on the Sources page.",
    },
    "source_ledger": {
        "title": "Source ledger — all sources with verification status",
        "columns": ["ID", "Source", "Publisher / tier", "Status", "What it supports", "Source"],
        "rows": [],  # generated by build_dashboard.py from SOURCES
        "caption": "Every external URL used on this dashboard is listed here with its publisher, tier, retrieval date and verification status. 'dead' sources are never linked from a table row; their URL is shown as plain text for documentation only.",
    },
}

# ---------------------------------------------------------------------------
# Decision ranking inputs. Points follow the rules in TABLES["ranking_criteria"];
# totals and the final order are computed here so that no sum is typed by hand.
# Every evidence string names the source id it was read from.
# ---------------------------------------------------------------------------
RANKING_WEIGHTS = {"C1": 30, "C2": 15, "C3": 15, "C4": 10, "C5": 10, "C6": 10, "C7": 10}

RANKING_INPUTS = [
    {
        "name": "Ace Plumbing &amp; Rooter Inc", "lic": "S11", "licnum": "#829071", "phone": "(415) 824-6444",
        "site": "S43", "review": "S75",
        "pts": {"C1": 30, "C2": 15, "C3": 15, "C4": 10, "C5": 0, "C6": 10, "C7": 10},
        "why": "Only candidate with the full set: B + C-36 (plus A, C-4, C-10, C-16) on one current license, an insured workers'-comp policy to 2027-07-13, a clean record, a San Francisco address, a company page that names HOAs and property managers, and the largest review volume in the set (4.7 ★, 1.4–1.5k, third-party).",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Benchmarks: drain replacement $500–$1,020 (avg $700), new drywall ≈ $2,100 (" + slink("S15", "Angi") + "); leak repair $150–$600 plus $300–$930 drywall/tile follow-up (" + slink("S16", "Angi") + ").",
        "caveats": "Capability for this specific concealed repair is unverified (U15); Yelp figures are search-result text (U29). Ask for a single written scope covering above-attempt, below access, ceiling patch/finish and a water test.",
    },
    {
        "name": "The Genteel Plumbers Inc", "lic": "S64", "licnum": "#1025814", "phone": "(833) 436-8335 (CSLB) · 415-465-5853 (company site)",
        "site": "S69", "review": "S74",
        "pts": {"C1": 30, "C2": 15, "C3": 15, "C4": 10, "C5": 3, "C6": 3, "C7": 10},
        "why": "B + C-36 on one license, insured workers' comp (to 2027-01-24), clean record and a San Francisco office. The company publishes its pricing model — a $149 dispatch fee credited to the work — which is the only published price evidence among the dual-classified firms. Loses points because its page makes no occupied-unit statement.",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Company states a $149 dispatch fee applied to the cost of services and flat-rate pricing (" + slink("S69", "company statement") + "). Benchmarks as for rank 1 (" + slink("S15", "Angi") + ").",
        "caveats": "Phone differs between CSLB and the company site, and Yelp shows two listings (U24); the company says it does not serve the Financial District (" + slink("S69", "site") + "). If only the 17-review Yelp listing is current, C7 would be 4 and the firm would score 80 (rank 3).",
    },
    {
        "name": "Handyman Heroes Inc", "lic": "S10", "licnum": "#1003394", "phone": "(844) 382-4376",
        "site": "S73", "review": "S36",
        "pts": {"C1": 30, "C2": 15, "C3": 7, "C4": 10, "C5": 0, "C6": 10, "C7": 10},
        "why": "B + C-36 on one license, insured workers' comp to 2027-04-25, San Francisco office, and a company page that explicitly offers 'sheetrock and wall repairs' plus plumbing for 'San Francisco homes and apartments'. Ranks below Genteel only because the CSLB record carries a 2020 complaint disclosure (reported verbatim, disclosure only).",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Benchmarks as for rank 1 (" + slink("S15", "Angi") + ", " + slink("S16", "Angi") + ").",
        "caveats": "Complaint disclosure 2 2020 001045 (" + slink("S12", "CSLB") + ") — read it before calling; company site also states 'Licensed C-10', which the CSLB record does not list (U08). Prior Yelp address differs from CSLB (U17).",
    },
    {
        "name": "GENERALSF (General SF)", "lic": "S09", "licnum": "#959843", "phone": "(650) 303-1515",
        "site": "S72", "review": "S35",
        "pts": {"C1": 30, "C2": 5, "C3": 15, "C4": 10, "C5": 0, "C6": 3, "C7": 10},
        "why": "B + C-10 + C-36 on one license with a clean record and a San Francisco address; the company's Building page lists 'Sheetrock/Tape and Texture' and 'Rough and Finish Plumbing', i.e. both halves of this job. Marked down because the CSLB record shows a workers'-comp exemption ('no employees') (U06).",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Benchmarks as for rank 1 (" + slink("S15", "Angi") + ").",
        "caveats": "Workers'-comp exemption (U06) — confirm in writing who will be on site and under what coverage; company page makes no occupied-unit statement.",
    },
    {
        "name": "Manny's Plumbing &amp; Rooters", "lic": "S57", "licnum": "#841229", "phone": "(650) 207-5733",
        "site": "S71", "review": "S76",
        "pts": {"C1": 30, "C2": 5, "C3": 15, "C4": 7, "C5": 0, "C6": 5, "C7": 8},
        "why": "C-36 + B on one license with a clean record and a license running to 2028-06-30; the business's own Yelp specialties text names 'tub overflow repair and replacement' and its site lists drain replacement and bathroom remodeling. Loses points for the Daly City address, the workers'-comp exemption and a smaller review base (175).",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Company page advertises 5% new-customer / 10% senior discounts (" + slink("S71", "company statement") + "). Benchmarks as for rank 1 (" + slink("S15", "Angi") + ").",
        "caveats": "Service area is stated as San Mateo County cities 'and surrounding areas of San Mateo &amp; San Francisco Counties' (" + slink("S71", "site") + ") — confirm the SF address is covered (U15); 'Insured' on the site vs workers'-comp exemption on CSLB (U06).",
    },
    {
        "name": "Rapid Flow Plumbing &amp; Rooter Inc", "lic": "S56", "licnum": "#1115649", "phone": "(415) 866-8401",
        "site": "S70", "review": "S77",
        "pts": {"C1": 30, "C2": 5, "C3": 15, "C4": 10, "C5": 0, "C6": 5, "C7": 4},
        "why": "B + C-36 on one license (valid to 2028-01-31), clean record, San Francisco address, and a site that lists general contracting/remodels and leak repair with 'residential and commercial expertise'. The newest license in the set with only an 8-review snapshot and a workers'-comp exemption, so it ranks last among the dual-classified firms.",
        "cost": BLANK + " " + UNVERIFIED + " — no quote on file. Benchmarks as for rank 1 (" + slink("S15", "Angi") + ").",
        "caveats": "Thin review evidence (8 reviews, prior-session snapshot) (U29) and a workers'-comp exemption (U06).",
    },
    {
        "name": "Fast Response Plumbing &amp; Rooter", "lic": "S08", "licnum": "#1024971", "phone": "(415) 596-6115",
        "site": "S40", "review": "S34",
        "pts": {"C1": 5, "C2": 15, "C3": 15, "C4": 10, "C5": 4, "C6": 10, "C7": 10},
        "why": "Best of the plumbing-only firms: insured, clean record, San Francisco address, a page that names apartments, HOAs and property managers, strong review volume, and the cheapest quote on file ($135, adjust/repair). Cannot satisfy the one-provider requirement alone — a C-9 drywall partner (e.g. Bernal Hill #995163) or a subcontract would be needed for the ceiling.",
        "cost": "$135 repair/adjust plunger handle (owner-provided quote, " + UNVERIFIED + ") — covers an adjustment only, not removal via the ceiling or drywall; add drywall patch $300–$930 (" + slink("S16", "Angi") + ") if below access is needed.",
        "caveats": "Workers'-comp policy expires 2026-12-18 (U05/U28); company aggregate '4.9 · 1,500 reviews' is a company claim (U09); address mismatch between CSLB and the company site (U04).",
    },
    {
        "name": "Expert Plumbing Solutions", "lic": "S06", "licnum": "#977638", "phone": "(415) 531-5340",
        "site": "S38", "review": "S32",
        "pts": {"C1": 5, "C2": 15, "C3": 15, "C4": 10, "C5": 10, "C6": 3, "C7": 4},
        "why": "Holds the only quote on file for the full waste-and-overflow replacement ($614), is insured with a clean record and the longest license term in the set (to 2028-10-31). Plumbing-only, so the ceiling work would need a drywall partner; small review base.",
        "cost": "$614 replace waste and overflow (owner-provided quote, " + UNVERIFIED + ") — within Angi's $500–$1,020 replacement range (" + slink("S15", "Angi") + "); drywall not included.",
        "caveats": "Quote scope does not mention below access or drywall (U14); review snapshot 81 reviews (U03).",
    },
    {
        "name": "Bay Area Plumbing", "lic": "S07", "licnum": "#757796", "phone": "(415) 668-8000",
        "site": "S39", "review": "S33",
        "pts": {"C1": 5, "C2": 5, "C3": 15, "C4": 10, "C5": 8, "C6": 5, "C7": 8},
        "why": "Plumbing-only sole owner with a workers'-comp exemption and a license that expires 2027-01-31 (about 12 weeks after this review); its $550 quote covers a different scope (lever + spout/diverter) rather than the stuck-lever removal itself.",
        "cost": "$550 replace lever for tub plug and spout with diverter, labor + materials (owner-provided quote, " + UNVERIFIED + ") — scope differs from the other two quotes; drywall not included.",
        "caveats": "License expiry 2027-01-31 and workers'-comp exemption (U06/U28); quote scope differs from the other two (U02/U14).",
    },
]


def _cited_ids(html_text, exclude=()):
    """Source ids whose URL is linked inside html_text (so the Source column lists every citation)."""
    return [sid for sid, src in SOURCES.items()
            if sid not in exclude and ('href="%s"' % src["url"]) in html_text]


def _rank_sort_key(item):
    total = sum(item["pts"][c] for c in RANKING_WEIGHTS)
    return tuple([-total] + [-item["pts"][c] for c in RANKING_WEIGHTS])


def build_ranking_rows():
    """Compute totals, sort with the documented tie-break and emit both tables."""
    for item in RANKING_INPUTS:
        for c, w in RANKING_WEIGHTS.items():
            assert 0 <= item["pts"][c] <= w, (item["name"], c)
        item["total"] = sum(item["pts"][c] for c in RANKING_WEIGHTS)
    ordered = sorted(RANKING_INPUTS, key=_rank_sort_key)
    scores, ranking = [], []
    for i, item in enumerate(ordered, 1):
        tier = pill("B + C-36 on one license", "ok") if item["pts"]["C1"] == 30 else pill("C-36 only — needs a drywall partner", "warn")
        srcs = [item["lic"], item["site"], item["review"], "S67"]
        scores.append({"cells": [str(i), item["name"] + "<br>" + slink(item["lic"], item["licnum"])] + [str(item["pts"][c]) for c in RANKING_WEIGHTS] + ["<strong>" + str(item["total"]) + "</strong>"], "src": srcs})
        ranking.append({"cells": [
            "<strong>" + str(i) + "</strong>",
            "<strong>" + item["name"] + "</strong><br>" + slink(item["lic"], "CSLB " + item["licnum"]) + " · " + slink(item["site"], "site") + "<br><small>Tel: " + item["phone"] + "</small><br>" + tier,
            "<strong>" + str(item["total"]) + "</strong> / 100",
            item["why"],
            item["cost"],
            item["caveats"],
        ], "src": srcs + (["S44"] if item["pts"]["C5"] in (4, 8, 10) else []) + _cited_ids(item["cost"] + item["caveats"], exclude=srcs)})
    return scores, ranking


TABLES["ranking_scores"]["rows"], TABLES["ranking"]["rows"] = build_ranking_rows()
RANKING_ORDER = [r["cells"][1].split("<br>")[0].replace("<strong>", "").replace("</strong>", "") for r in TABLES["ranking"]["rows"]]

PAGES = {
    "index.html": {
        "title": "Dashboard",
        "eyebrow": "Research dashboard · San Francisco · updated 2026-11-08",
        "h1": "Bathtub wastewater overflow trip lever",
        "lede": "A stuck trip lever in concealed plumbing behind the wall. From-above removal is preferred but has not been achievable; the reported fallback is access from below through a storage-unit ceiling. This dashboard organizes the requirements, three estimates, verified contractor records, review platforms, cost benchmarks, official rules, and every item that still needs review.",
        "sections": [
            {"type": "cards", "items": [
                {"k": "Estimates received", "v": "3", "s": "2026-08-30 · amounts owner-provided (unverified)", "tone": "warn"},
                {"k": "Contractor candidates ranked", "v": "9", "s": "All with active CSLB licenses re-verified 2026-11-08; +1 drywall partner, +1 screened out, +1 unverified lead", "tone": "ok"},
                {"k": "Verified official sources", "v": "AUTO_OFFICIAL", "s": "Government + manufacturer sources read directly 2026-11-07 / 2026-11-08", "tone": "info"},
                {"k": "Flagged for review", "v": "29", "s": "Unverified values and irregularities — none blocking", "tone": "warn"},
            ]},
            {"type": "table", "title": "Problem snapshot", "ref": "problem"},
            {"type": "quick", "title": "Browse by category", "items": [
                {"href": "summary.html", "t": "Executive summary", "d": "Important details, key findings and next steps."},
                {"href": "requirements.html", "t": "Requirements", "d": "The full brief, line by line, with verification status."},
                {"href": "estimates.html", "t": "Estimates & costs", "d": "The three quotes, blank verified cells, and 2026 cost benchmarks."},
                {"href": "contractors.html", "t": "Contractors & reviews", "d": "CSLB-verified licenses, Yelp/Angi/BuildZoom/Thumbtack/BBB discovery links."},
                {"href": "findings.html", "t": "Findings & analysis", "d": "Access options, one-provider shortlist, cost and occupied-unit analysis."},
                {"href": "ranking.html", "t": "Decision ranking", "d": "Nine candidates scored 1–9 with weights, reasoning, cost position and CSLB phone numbers."},
                {"href": "shortlist.html", "t": "Shortlist", "d": "Dual-classified firms and vetting script from a parallel session."},
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
            {"type": "callout", "tone": "ok", "html": "<strong>Every table row on this site carries a source link.</strong> License facts come from the official CSLB database (records printed “Data current as of 11/8/2026” on re-verification); permit and licensing rules come from sf.gov and California Legislative Information; technical and cost claims link to the manufacturer or publisher page they were read from."},
            {"type": "callout", "tone": "warn", "html": "<strong>Blank means unconfirmed.</strong> Where a value cannot be confirmed from an official source, the verified value cell is left blank and marked UNVERIFIED. Owner-provided figures appear only on the clearly labeled " + slink("S44", "Project brief") + " page, in the explicitly labeled Brief transcription table on <a href=\"estimates.html\">Estimates</a>, and on the <a href=\"flagged.html\">Flagged for Review</a> page. Nothing is inferred or filled in."},
            {"type": "callout", "tone": "info", "html": "Archived material from earlier sessions remains published at " + slink("S49", "bathtub-overflow/") + ", " + slink("S50", "docs/bath/") + ", " + slink("S51", "docs/plumbing-index.html") + " and the unrelated legacy GEMS site at " + slink("S48", "docs/index.html") + ". Those files were not edited by this integration session. Shared task board: " + slink("S45", "COORDINATION.md") + "."},
        ],
    },
    "summary.html": {
        "title": "Executive summary",
        "eyebrow": "Overview · updated 2026-11-08",
        "h1": "Executive summary",
        "lede": "The important details of the bathtub wastewater overflow trip lever project — the problem, the estimates, who can do the work, what the rules say, and what still needs review.",
        "sections": [
            {"type": "prose", "title": "1. The problem", "html": "<p>The bathtub's waste-and-overflow trip lever is " + pill("owner-provided", "info") + " stuck inside hidden plumbing behind the wall, in a hard-to-access area. More than five licensed plumbers reportedly declined to remove it from above because of the risk of damaging concealed plumbing, and recommended working from below — where a storage unit sits beneath the unit, so the drywall ceiling may need to be opened. The unit is tenant-occupied, so the owner wants one provider able to do both drywall and plumbing in a sensitive environment. Removing the overflow from above remains preferred if it can be done safely. None of these facts can be confirmed from a public source; see the " + "<a href=\"brief.html\">Project brief</a>" + " and " + "<a href=\"flagged.html\">Flagged for Review</a>" + " page. Context: " + slink("S18", "This Old House on below access") + ", " + slink("S17", "Angi on overflow function") + ".</p>"},
            {"type": "table", "title": "2. Estimates at a glance", "ref": "estimates"},
            {"type": "prose", "title": "3. What the numbers mean", "html": "<p>The three quotes describe three different scopes — an adjustment, a spout/lever replacement, and a full waste-and-overflow replacement. Independent 2026 publisher benchmarks put bathtub/shower drain replacement at <strong>$500–$1,020 (avg $700)</strong> (" + slink("S15", "Angi, 2026-09-18") + "), bathroom leak repair at <strong>$150–$600</strong> plus <strong>$300–$930</strong> for drywall/tile follow-up (" + slink("S16", "Angi, 2026-10-28") + "), and new drywall at about <strong>$2,100</strong> (" + slink("S15", "Angi") + "). Drywall is not included in any of the three quoted scopes. The quote amounts themselves are owner-provided and unverified, so this comparison is directional only. Full table: <a href=\"estimates.html\">Estimates &amp; costs</a>.</p>"},
            {"type": "prose", "title": "4. Who can do the work", "html": "<p>Nine San Francisco-area plumbing candidates were verified against the official CSLB database on 2026-11-07 and re-verified on 2026-11-08 with no changes (plus one unverified lead, one drywall-only partner option and one firm screened out because of an official notice). All nine hold <strong>current and active</strong> licenses. Six hold both a building classification and C-36 Plumbing on one license — " + slink("S11", "Ace #829071") + ", " + slink("S64", "Genteel #1025814") + ", " + slink("S10", "Handyman Heroes #1003394") + ", " + slink("S09", "GENERALSF #959843") + ", " + slink("S57", "Manny's #841229") + " and " + slink("S56", "Rapid Flow #1115649") + " — which matches the single-provider requirement for drywall plus plumbing (" + slink("S67", "B&amp;P §7057(b)") + "). CSLB verifies license classes, not the ability to perform this specific delicate repair; that remains unverified and flagged. " + slink("S05", "C-36 classification definition") + ". Full table: <a href=\"contractors.html\">Contractors &amp; reviews</a>.</p>"},
            {"type": "prose", "title": "4a. Decision ranking (best choice first)", "html": "<p>Scoring nine candidates on seven published criteria (license coverage 30, workers' comp 15, official record 15, address 10, cost evidence 10, company-page statements 10, review snapshot 10) gives this calling order: <strong>1 Ace Plumbing &amp; Rooter (90)</strong>, 2 The Genteel Plumbers (86), 3 Handyman Heroes (82), 4 General SF (73), 5 Manny's Plumbing &amp; Rooters (70), 6 Rapid Flow (69), then the plumbing-only firms 7 Fast Response (69), 8 Expert Plumbing Solutions (62), 9 Bay Area Plumbing (56). Ranks 1–6 can carry both trades on one license; ranks 7–9 would need a drywall partner such as " + slink("S65", "Bernal Hill Drywall #995163") + ". Cost per rank: no dual-classified firm has quoted yet (cells blank, unverified); Genteel publishes a $149 dispatch fee credited to the work (" + slink("S69", "company statement") + "); the owner-held quotes are $135 (Fast Response, adjust only), $614 (Expert, full waste-and-overflow) and $550 (Bay Area, different scope), all unverified, against Angi's 2026 range of $500–$1,020 for drain replacement (" + slink("S15", "Angi") + "). The weights are this site's own and no provider has been contacted. Full tables with per-criterion points, reasoning and CSLB phone numbers: <a href=\"ranking.html\">Decision ranking</a>.</p>"},
            {"type": "prose", "title": "5. Official rules (neutral)", "html": "<p>SF.gov states: “You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground” (" + slink("S01", "sf.gov") + "), and lists “minor repairs to existing interior plaster or wallboard” among work that does not need a permit (" + slink("S02", "sf.gov") + "). Contractors applying for a plumbing permit must hold C-4, C-16, C-20, C-36, C-54, B or A classifications (" + slink("S01", "sf.gov") + "). California B&amp;P §7048 sets the current small-job licensing exemption at under $1,000 for casual/minor work that does not require a building permit, effective 2026-01-01 (" + slink("S13", "leginfo") + "). The hiring party should confirm applicability for the exact scope with SF DBI and the selected contractor. Full table: <a href=\"permits.html\">Permits &amp; licensing</a>.</p>"},
            {"type": "prose", "title": "6. Recommended next steps", "html": "<ol class=\"tight\"><li><strong>Call in ranking order</strong> — " + slink("S11", "#829071") + ", " + slink("S64", "#1025814") + ", " + slink("S10", "#1003394") + ", " + slink("S09", "#959843") + ", " + slink("S57", "#841229") + ", " + slink("S56", "#1115649") + " (see <a href=\"ranking.html\">Decision ranking</a>) — and ask for one written scope covering an above-attempt, below access, ceiling cut/patch/finish, a fill-and-inspect water test, and tenant access windows.</li><li><strong>Confirm crew coverage in writing</strong>: four CSLB records show a workers'-compensation “no employees” exemption and one policy expires 2026-12-18 (" + slink("S07", "#757796") + ", " + slink("S09", "#959843") + ", " + slink("S56", "#1115649") + ", " + slink("S57", "#841229") + ", " + slink("S08", "#1024971") + ").</li><li><strong>Ask for references on concealed waste-and-overflow work in occupied units</strong>; no official source confirms job-specific capability (" + slink("S04", "CSLB Check a License") + ", " + slink("S24", "Angi SF bathtub reviews") + ").</li><li><strong>Re-verify the chosen license on the hire date</strong> at " + slink("S04", "cslb.ca.gov") + " and review the " + "<a href=\"flagged.html\">29 flagged items</a>" + ".</li></ol>"},
            {"type": "callout", "tone": "warn", "html": "<strong>Informational only.</strong> This summary is research, not legal advice, a quote, or a contractor endorsement. Every unverified value is blank in the data tables and listed on the Flagged for Review page."},
        ],
    },
    "requirements.html": {
        "title": "Requirements",
        "eyebrow": "Overview · full list · updated 2026-11-08",
        "h1": "Requirements register",
        "lede": "The owner's brief, broken out line by line. Each row links the project primary record and the relevant official page. Officially confirmed values are blank wherever no official source exists.",
        "sections": [
            {"type": "table", "ref": "requirements"},
            {"type": "callout", "tone": "info", "html": "The register covers every requirement in the brief that is suitable for publication. Internal-only instructions are deliberately omitted; the " + "<a href=\"verification.html\">Verification</a>" + " page documents the privacy sweep that enforces this."},
        ],
    },
    "estimates.html": {
        "title": "Estimates & costs",
        "eyebrow": "Data · updated 2026-11-08",
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
        "lede": "Six San Francisco candidates verified against the official California Contractors State License Board database, plus Yelp, Angi, BuildZoom, Thumbtack and BBB discovery links for this specific work type.",
        "sections": [
            {"type": "table", "ref": "contractors"},
            {"type": "table", "ref": "review_snapshots"},
            {"type": "table", "ref": "platforms"},
            {"type": "callout", "tone": "info", "html": "<strong>No provider has been contacted and no provider has confirmed this job.</strong> This dashboard is desk research only. All review-platform ratings, counts and badges are third-party data and are unverified where they could not be re-checked on 2026-11-07; only " + slink("S04", "CSLB") + " verifies a California contractor license. See " + slink("S58", "the shortlist") + " and <a href=\"flagged.html\">Flagged for Review</a>."},
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
        "eyebrow": "Data · analysis · updated 2026-11-08",
        "h1": "Findings & analysis",
        "lede": "What the verified data supports, what it does not, and the resulting shortlist rationale.",
        "sections": [
            {"type": "table", "ref": "findings"},
            {"type": "prose", "title": "Access decision matrix", "html": "<div class=\"table-wrap\"><table><thead><tr><th>Route</th><th>What the sources say</th><th>Verified?</th><th>Source</th></tr></thead><tbody><tr><td><strong>From above (preferred)</strong></td><td>Remove the overflow-plate screws and withdraw the upper linkage; cleaning or adjusting the link can free a stuck mechanism</td><td>" + pill("procedure documented; outcome for this tub unverified", "warn") + "</td><td>" + slink("S18") + " · " + slink("S21") + " · " + slink("S20") + "</td></tr><tr><td><strong>From below (reported fallback)</strong></td><td>Stubborn/seized drains may require access from below; new waste-and-overflow kits are aligned from below while a helper holds the shoe from above</td><td>" + pill("procedure documented; this tub's layout unverified", "warn") + "</td><td>" + slink("S18") + " · " + slink("S14") + "</td></tr><tr><td><strong>Drywall ceiling opening</strong></td><td>SF.gov lists minor interior plaster/wallboard repair among work not needing a building permit; the plumbing scope is governed by the plumbing-permit rule</td><td>" + pill("official rules cited; applicability to this scope to be confirmed with SF DBI", "warn") + "</td><td>" + slink("S02") + " · " + slink("S01") + "</td></tr></tbody><caption>Each row links the source it was read from. This matrix is analysis, not a scope of work or a legal determination.</caption></table></div>"},
            {"type": "prose", "title": "Shortlist rationale", "html": "<p>Start with firms whose single verified license lists both a building classification and C-36 Plumbing: " + slink("S11", "Ace #829071") + ", " + slink("S64", "Genteel #1025814") + ", " + slink("S10", "Handyman Heroes #1003394") + ", " + slink("S09", "GENERALSF #959843") + ", " + slink("S57", "Manny's #841229") + " and " + slink("S56", "Rapid Flow #1115649") + ". This follows from the CSLB classifications themselves (" + slink("S67", "B&amp;P §7057(b)") + "), not from any company claim. The scored order, with reasoning and cost position per rank, is on the <a href=\"ranking.html\">Decision ranking</a> page. Watch items: workers'-compensation exemptions on #959843, #757796, #1115649 and #841229, a policy expiring 2026-12-18 on #1024971, and the official complaint disclosure on #1003394 — all listed on the <a href=\"flagged.html\">Flagged for Review</a> page. Re-check every license at " + slink("S04", "CSLB") + " on the hire date.</p>"},
        ],
    },
    "ranking.html": {
        "title": "Decision ranking",
        "eyebrow": "Data · decision analysis · updated 2026-11-08",
        "h1": "Decision ranking — who to call first, and why",
        "lede": "Nine licensed candidates scored out of 100 on seven published criteria, best choice first. Each rank states the reasoning, the cost position (owner-held quotes and 2026 benchmarks — never an estimate of our own), the caveats, and the business phone printed on the official CSLB record.",
        "sections": [
            {"type": "cards", "items": [
                {"k": "Rank 1", "v": "Ace", "s": "Ace Plumbing &amp; Rooter Inc · CSLB #829071 · 90/100 · (415) 824-6444", "tone": "ok"},
                {"k": "Rank 2", "v": "Genteel", "s": "The Genteel Plumbers Inc · CSLB #1025814 · 86/100 · (833) 436-8335", "tone": "ok"},
                {"k": "Rank 3", "v": "Handyman Heroes", "s": "Handyman Heroes Inc · CSLB #1003394 · 82/100 · (844) 382-4376", "tone": "ok"},
                {"k": "Quotes on file", "v": "3", "s": "Ranks 7–9 only (plumbing-only firms) — all owner-provided and unverified", "tone": "warn"},
            ]},
            {"type": "callout", "tone": "info", "html": "<strong>How to read this page.</strong> The order is a calling sequence produced from documents — CSLB records, company pages, the owner's three quotes and review snapshots — not a selection. Ranks 1–6 hold B General Building and C-36 Plumbing on one license and can carry both the plumbing and the ceiling work (" + slink("S67", "B&amp;P §7057(b)") + "); ranks 7–9 are C-36-only and would need a drywall partner or subcontract. Weights are this site's own (U27). No provider has been contacted (U20)."},
            {"type": "table", "ref": "ranking"},
            {"type": "table", "ref": "ranking_scores"},
            {"type": "table", "ref": "ranking_criteria"},
            {"type": "table", "ref": "ranking_excluded"},
            {"type": "prose", "title": "Cost per rank — what is and is not known", "html": "<ul class=\"tight\"><li><strong>Ranks 1–6 (dual-classified):</strong> no quote exists; the cost cells are blank and marked unverified. The only published price signal is Genteel's $149 dispatch fee credited to the work (" + slink("S69", "company statement") + "). Manny's advertises 5% / 10% discounts (" + slink("S71", "company statement") + ").</li><li><strong>Ranks 7–9 (owner-held quotes, unverified):</strong> Fast Response $135 repair/adjust (adjustment only), Expert Plumbing Solutions $614 full waste-and-overflow replacement, Bay Area Plumbing $550 lever + spout/diverter (different scope). See <a href=\"estimates.html\">Estimates &amp; costs</a>.</li><li><strong>Benchmarks (publisher, 2026):</strong> bathtub/shower drain replacement $500–$1,020, average $700; new drywall ≈ $2,100 (" + slink("S15", "Angi") + "); bathroom leak repair $150–$600 with $300–$930 drywall/tile follow-up and $50–$200 call-out fees (" + slink("S16", "Angi") + "). None of the three quotes includes drywall, so a from-below job will cost more than any quote on file.</li><li><strong>Why the full quote (Expert, $614) does not win:</strong> it is a plumbing-only scope from a C-36-only firm; the brief's one-provider requirement and the ceiling access carry more weight than a known price for part of the job.</li></ul>"},
            {"type": "prose", "title": "Sensitivity — what would change the order", "html": "<ul class=\"tight\"><li>If only Genteel's 17-review Yelp listing is current, Genteel scores 80 and swaps with Handyman Heroes (U24).</li><li>If a C-36-only firm supplies a written subcontract with a C-9 drywall contractor (e.g. " + slink("S65", "Bernal Hill Drywall #995163") + ") and C1 is treated as satisfied for comparison, Fast Response would score 94 (rank 1), Expert 87 and Bay Area 81 — but the owner would then be managing two firms and two warranties, which is what the brief asked to avoid.</li><li>If Fast Response's workers'-comp policy is not renewed by 2026-12-18, its C2 falls to 5 and it scores 59, dropping behind Expert (U28).</li><li>Setting C6 and C7 (self-statements and third-party reviews) to zero puts Genteel (73) one place ahead of Ace (70) — the published dispatch fee is the only remaining difference — and leaves General SF and Rapid Flow tied at 60; the six dual-classified firms still occupy ranks 1–6.</li></ul>"},
            {"type": "prose", "title": "Next steps in ranking order", "html": "<ol class=\"tight\"><li>Call ranks 1–3 at the CSLB-record numbers and ask for a site visit and one written scope: attempt from above first; if not safe, access from below through the storage-unit ceiling, cut/patch/tape/texture, fill-and-inspect water test, tenant access windows, and clean-up.</li><li>Ask each for references on concealed waste-and-overflow work in occupied units and for a current certificate of insurance (U15, U28).</li><li>Re-read the chosen license at " + slink("S04", "CSLB Check a License") + " on the hire date; the records cited here were re-verified on 2026-11-08.</li><li>When quotes arrive, re-score C5 with real numbers — the Score sheet shows exactly which points move.</li></ol>"},
            {"type": "callout", "tone": "warn", "html": "<strong>Informational only.</strong> Review figures are Yelp search-result or prior-session snapshots (listing pages return HTTP 403); company statements are self-descriptions; quote amounts are owner-provided. All are labeled and listed on the <a href=\"flagged.html\">Flagged for Review</a> page. This page is research, not legal advice, a quote or an endorsement."},
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
            {"type": "prose", "title": "Method", "html": "<ol class=\"tight\"><li>Each table row is emitted with a Source column built from its source ids. The build script aborts if any row has no source, cites an unknown source, or cites a source marked dead.</li><li>Every official value was read directly from the issuing site on 2026-11-07; CSLB License Detail pages printed a “Data current as of 11/7/2026” stamp.</li><li>The verifier parses every generated HTML file: every <code>&lt;tbody&gt;</code> row must contain a link; every internal link (pages, CSS, JS, anchors) must resolve to an existing file; every external link must exist in the source ledger; no dead source may be linked from a row.</li><li>A privacy sweep greps all published HTML/MD/JSON/CSS/JS for internal-only hiring-constraint wording and returns zero matches.</li><li>After merge, the live GitHub Pages URL is fetched and the Pages build status is checked with the GitHub API.</li></ol>"},
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
            {"type": "callout", "tone": "warn", "html": "To request a change, note the item ID (U01–U29) and the correction. Unverified values are blank in the data tables; nothing was inferred to fill a gap. Full source ledger: <a href=\"sources.html\">Sources</a>."},
        ],
    },
}
