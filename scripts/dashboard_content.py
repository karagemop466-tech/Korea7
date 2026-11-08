"""Canonical content for the bathtub-overflow trip-lever research dashboard.

Single source of truth for session `arena/6696a17e-korea7`. Every table row cites
source ids from SOURCES. Official job values that cannot be confirmed are blank
and flagged UNVERIFIED; owner reports, company claims, publisher benchmarks and
third-party reviews are labeled by provenance. Nothing is inferred.

Primary official retrieval date: 2026-11-08 (UTC). Historical sources retain their
original checked date when they were not re-read in this session.
"""

META = {'updated': '2026-11-08',
 'session': 'arena/6696a17e-korea7',
 'title': 'Bathtub overflow trip lever — repair research dashboard',
 'pages_url': 'https://karagemop466-tech.github.io/Korea7/',
 'repo_url': 'https://github.com/karagemop466-tech/Korea7'}

NAV = [{'group': 'Overview',
  'links': [('index.html', 'Dashboard'),
            ('summary.html', 'Executive summary'),
            ('requirements.html', 'Requirements')]},
 {'group': 'Data',
  'links': [('estimates.html', 'Estimates & costs'),
            ('contractors.html', 'Contractors & ranking'),
            ('findings.html', 'Findings & analysis')]},
 {'group': 'Reference',
  'links': [('technical.html', 'Technical background'),
            ('permits.html', 'Permits & licensing'),
            ('brief.html', 'Project brief'),
            ('sources.html', 'Source ledger')]},
 {'group': 'Audit',
  'links': [('verification.html', 'Verification'),
            ('repo-review.html', 'Repo review'),
            ('verification-log.html', 'Prior verification log'),
            ('flagged.html', 'Flagged for review')]}]

# tier: official / manufacturer / publisher / platform / company / primary
# status: verified / blocked-403 / dead / removed
SOURCES = {'S01': {'label': 'SF.gov — Apply for a plumbing and mechanical permit',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/apply-plumbing-and-mechanical-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Permit required before cutting into/replacing pipes, especially pipes covered by a wall; license '
                     'classes allowed to apply; inspection before covering pipes; R-3 homeowner limitation; Permit '
                     'Center 628-652-4900 and permitsf@sfgov.org',
         'note': 'Read directly on sf.gov 2026-11-08.'},
 'S02': {'label': 'SF.gov — Check if your construction project needs a permit',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/information--check-if-your-construction-project-needs-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Published exempt-work list includes minor repairs to existing interior plaster or wallboard '
                     'unless required for fire protection; links SF Building Code 106A.2',
         'note': 'Read directly on sf.gov 2026-11-08. This does not establish an exemption for concealed plumbing '
                 'work.'},
 'S03': {'label': 'SF Building/Plumbing Code — Section 104.0 Permits',
         'publisher': 'American Legal Publishing code library (City and County of SF)',
         'url': 'https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Official code location for §104.2 exempt work referenced by sf.gov',
         'note': "Page title confirmed as 'SECTION 104.0 - PERMITS'. The code library page is JavaScript-heavy; the "
                 'exemption text was not machine-parsed, so the link is provided for manual review and no section '
                 'wording is quoted from it.'},
 'S04': {'label': 'CSLB — Check a License',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Official license lookup by number or business name; CSLB advises checking status and complaint '
                     'disclosure before hiring',
         'note': 'Read directly on cslb.ca.gov, 2026-11-07.'},
 'S05': {'label': 'CSLB — C-36 Plumbing classification',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'C-36 plumbing contractor definition: proper disposal of fluid waste and maintenance/replacement '
                     'of described items',
         'note': 'Read directly on cslb.ca.gov 2026-11-08.'},
 'S06': {'label': 'CSLB License Detail #977638 — Expert Plumbing Solutions',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' "
                     'compensation',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:22 PM.'},
 'S07': {'label': 'CSLB License Detail #757796 — Bay Area Plumbing',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' "
                     'compensation exemption',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:52 PM.'},
 'S08': {'label': 'CSLB License Detail #1024971 — Fast Response Plumbing and Rooter',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Business name, address, entity, issue/expiry dates, status, classification, bond, workers' "
                     'compensation policy dates',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:34 PM.'},
 'S09': {'label': 'CSLB License Detail #959843 — GENERALSF',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Business name, address, entity, issue/expiry dates, status, B/C10/C36 classifications, bond, '
                     "workers' compensation exemption",
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:52 PM.'},
 'S10': {'label': 'CSLB License Detail #1003394 — Handyman Heroes Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Business name, address, entity, issue/expiry dates, status, B/C36 classifications, bond, '
                     "workers' compensation, complaint-disclosure flag",
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:52 PM.'},
 'S11': {'label': 'CSLB License Detail #829071 — Ace Plumbing & Rooter',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Business name, address, entity, issue/reissue/expiry dates, status, A/B/C-4/C10/C16/C36 '
                     "classifications, bond, workers' compensation",
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:57 PM.'},
 'S12': {'label': 'CSLB Complaint Disclosure #1003394',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Citation 2 2020 001045, dated 07/12/2020, 'FOR DISCLOSURE ONLY PER B&P CODE 7124.6'",
         'note': 'Read directly 2026-11-08. Citation and status transcribed verbatim; no interpretation.'},
 'S13': {'label': 'California Business & Professions Code §7048',
         'publisher': 'California Legislative Information (leginfo)',
         'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'BPC 7048 current text: aggregate contract price under $1,000, casual/minor/inconsequential, and '
                     'no building permit required; exclusions for larger operations, split contracts, contractor '
                     'advertising, or employing others; AB 1170 effective 2026-01-01',
         'note': 'Read directly on leginfo 2026-11-08.'},
 'S14': {'label': 'Oatey — Dearborn Plastic Tubular Trip-Lever Bath Waste',
         'publisher': 'Oatey (manufacturer)',
         'url': 'https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste',
         'tier': 'manufacturer',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Oatey Dearborn Plastic Tubular Trip-Lever Bath Waste full kit; black A9226 UPC 041193058379 and '
                     'white P9226 UPC 041193057099 variations; chrome-finish stopper',
         'note': 'Manufacturer page read directly 2026-11-08. Compatibility with this tub is unverified.'},
 'S15': {'label': 'Angi — Cost to Replace a Bathtub or Shower Drain (2026)',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'National bathtub/shower drain replacement: $500-$1,020 normal range, $700 average, $230 low, '
                     '$1,170 high; labor $45-$200/hr; additional drywall/unclogging/water-damage budget $1,350-$6,100; '
                     'new drywall about $2,100; unclogging avg $225',
         'note': 'Article updated Sep 18, 2026; read directly 2026-11-08. Publisher cost data, not an official San '
                 'Francisco price.'},
 'S16': {'label': 'Angi — Bathroom Leak Repair Cost (2026)',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'National bathroom leak repair: $150-$600 normal range, $275 average, up to $4,000 complex; '
                     'drywall/tile/flooring follow-up $300-$930; call-out $50-$200; labor $45-$200/hr; worn-out tub '
                     'drain avg $700',
         'note': 'Article updated Oct 28, 2026; read directly 2026-11-08. Publisher cost data, not an official San '
                 'Francisco price.'},
 'S17': {'label': 'Angi — What Is a Bathtub Overflow Drain?',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/what-is-overflow-drain.htm',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Overflow drain function, concealed channel, traditional vs integral overflow, trip-lever/rod '
                     'diagram',
         'note': 'Article updated Jul 9, 2026; read directly 2026-11-08.'},
 'S18': {'label': 'This Old House — How To Replace a Tub Drain',
         'publisher': 'This Old House',
         'url': 'https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Bath waste-and-overflow components; remove overflow-plate screws from above; seized drains may '
                     'need below-tub access; linkage adjustment; test new drain and stopper',
         'note': 'Read directly 2026-11-08. DIY/trade guide, not San Francisco code guidance and not an inspection of '
                 'this tub.'},
 'S19': {'label': 'This Old House — Bathtub Installation Cost (2026)',
         'publisher': 'This Old House',
         'url': 'https://www.thisoldhouse.com/bathrooms/bathtub-installation-cost',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Itemized bathtub installation table: Overflow $163, Drain $190, Spout $82; total $2,110; average '
                     'bathtub replacement about $2,100',
         'note': 'Article updated 03/05/2026; read directly 2026-11-08. Component averages, not a job quote.'},
 'S20': {'label': 'Family Handyman — Replace a bathtub drain stopper',
         'publisher': 'Family Handyman',
         'url': 'https://www.familyhandyman.com/project/how-to-convert-bathtub-drain-lever-to-a-lift-and-turn-drain/',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Lift-and-turn conversion begins by removing overflow plate and linkage; old stopper body removal '
                     'is the toughest part and can damage tub if cut incorrectly',
         'note': 'Article updated Feb 14, 2024; read directly 2026-11-08. Conversion is not a verified workaround for '
                 'this seized assembly.'},
 'S21': {'label': 'Hunker — The Trip Lever In My Bathtub Is Stuck',
         'publisher': 'Hunker',
         'url': 'https://www.hunker.com/13417812/the-trip-lever-in-my-bathtub-is-stuck/',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Trip lever is hidden behind tub wall; first diagnostic step is removing cover plate and checking '
                     'links; grime or broken linkage can cause sticking',
         'note': 'Article updated Oct 3, 2020; read directly 2026-11-08.'},
 'S22': {'label': 'The Overall Plumber — Bathtub Drain Drama',
         'publisher': 'The Overall Plumber (trade blog, Houston TX)',
         'url': 'https://www.theoverallplumber.com/home-improvement/bathtub-drain-drama-why-you-need-a-licensed-and-insured-plumber-fast/',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Typical bathtub drain repairs $80-$600; most repairs 1-4 hours; repair-vs-replacement table; '
                     'hydrostatic/fill-and-inspect testing',
         'note': 'Read directly 2026-11-08. Houston-area trade blog; publication date not shown on fetched page. Its '
                 'permit statements are not used for San Francisco guidance.'},
 'S23': {'label': 'Angi — Best plumbers in San Francisco, CA',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/companylist/us/ca/san-francisco/plumbing.htm',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'San Francisco plumbing category with verified-review counts; 873 verified plumbing reviews; '
                     'review text about older SF homes',
         'note': "Read directly 2026-11-08. Page states 'Last update on August 01, 2026'. Platform reviews are not "
                 'license verification.'},
 'S24': {'label': 'Angi — Bathtub restoration pros in San Francisco, CA',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/companylist/us/ca/san-francisco/bathtub-refinishing.htm',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'SF bathtub-restoration category shows 17 verified reviews and last update October 14, 2024; '
                     'reviews describe older SF homes, apartment complexes and concealed leaks, but some listed firms '
                     'are not the candidates and one listing is explicitly unlicensed',
         'note': 'Read directly 2026-11-08. Third-party customer statements; not license verification.'},
 'S25': {'label': 'BuildZoom — Plumbers in San Francisco, CA',
         'publisher': 'BuildZoom',
         'url': 'https://www.buildzoom.com/san-francisco-ca/plumbers',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'San Francisco plumbing directory with client reviews, verified projects and '
                     'permit/license-derived profiles',
         'note': "Read directly. Page shows '683 experts'; count is a point-in-time platform figure."},
 'S26': {'label': 'BuildZoom — Drywall and plaster contractors in San Francisco, CA',
         'publisher': 'BuildZoom',
         'url': 'https://www.buildzoom.com/san-francisco-ca/drywall-contractors',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'San Francisco drywall/plaster directory with reviews and project photos',
         'note': "Read directly. Page shows '83 experts'; point-in-time platform figure."},
 'S27': {'label': 'Thumbtack — Bathtub services near San Francisco, CA',
         'publisher': 'Thumbtack',
         'url': 'https://www.thumbtack.com/ca/san-francisco/bathtub-refinishing',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': "San Francisco bathtub-service listings with customer reviews and 'Licensed pro' badges",
         'note': "Read directly. A platform 'Licensed pro' badge is not a CSLB license verification."},
 'S28': {'label': 'BBB — Expert Plumbing Solutions business profile',
         'publisher': 'Better Business Bureau',
         'url': 'https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Business profile: not BBB accredited, no BBB rating, no complaints in last 3 years, license '
                     'number 977638 on record, 1465 44th Avenue SF',
         'note': 'Read directly. BBB states it does not verify third-party information.'},
 'S29': {'label': 'Yelp — Bathtub Repair in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-07',
         'supports': 'Category search for the specific work type in San Francisco',
         'note': 'Direct fetch returned HTTP 403 to automated access; the live link is provided for manual review. No '
                 'rating values are claimed from this URL.'},
 'S30': {'label': 'Yelp — Plumbers in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-07',
         'supports': 'Category search for licensed plumbers serving San Francisco',
         'note': 'HTTP 403 on automated fetch; link provided for manual review.'},
 'S31': {'label': 'Yelp — Drywall Installation & Repair in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-07',
         'supports': 'Category search for the drywall half of the combined scope',
         'note': 'HTTP 403 on automated fetch; link provided for manual review.'},
 'S32': {'label': 'Yelp — Expert Plumbing Solutions',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/expert-plumbing-solutions-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Business review page for one of the three quoting companies',
         'note': 'Direct fetch HTTP 403 on 2026-11-08. Prior 2026-11-06 snapshot is historical, not current platform '
                 'verification.'},
 'S33': {'label': 'Yelp — Bay Area Plumbing',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/bay-area-plumbing-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Business review page for one of the three quoting companies',
         'note': 'Direct fetch HTTP 403 on 2026-11-08. Prior 2026-11-06 snapshot is historical, not current platform '
                 'verification.'},
 'S34': {'label': 'Yelp — Fast Response Plumbing & Rooter',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Business review page for one of the three quoting companies',
         'note': 'Direct fetch HTTP 403 on 2026-11-08. Prior 2026-11-06 snapshot is historical, not current platform '
                 'verification.'},
 'S35': {'label': 'Yelp — General SF',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/general-sf-san-francisco-2',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Yelp business discovery link; search-index snippets show conflicting counts 4.8/336 and 4.8/302 '
                     'and an apartment-owner plumbing review',
         'note': 'Direct fetch HTTP 403. Search-index snippets are third-party, date-variable and not current platform '
                 'verification.'},
 'S36': {'label': 'Yelp — Handyman Heroes',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/handyman-heroes-san-francisco-5',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Yelp business discovery link; search-index snippet shows 4.7/410 and 1525 Waller St',
         'note': 'Direct fetch HTTP 403 2026-11-08. Snippet is third-party and conflicts with CSLB address; not '
                 'current platform verification.'},
 'S37': {'label': 'Yelp — Szeto Plumbing and Handyman',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/szeto-plumbing-and-handyman-daly-city-2',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-07',
         'supports': 'Business review page for a plumbing+drywall lead outside SF proper',
         'note': 'HTTP 403 on automated fetch. Prior-session snapshot (4.8, 89 reviews) not re-verified — flagged; '
                 'license not found on CSLB.'},
 'S38': {'label': 'Expert Plumbing Solutions — official site',
         'publisher': 'Expert Plumbing Solutions',
         'url': 'https://www.eplumbingsolutions.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company prints License #977638, phone 415-531-5340, email paul@eplumbingsolutions.com, address '
                     '1465 44th Avenue SF, Mon-Fri 8-4; residential plumbing, drains, fixtures',
         'note': 'Read directly 2026-11-08. Company self-description; license facts come from CSLB.'},
 'S39': {'label': 'Bay Area Plumbing — official site',
         'publisher': 'Bay Area Plumbing',
         'url': 'https://www.bayareaplumbingsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company advertises San Francisco residential/commercial plumbing since 1995, 24/7 emergency '
                     'service, leak detection/pipe repair, kitchen/bath plumbing remodeling; phone (415) 668-8000',
         'note': 'Read directly 2026-11-08. Company self-description.'},
 'S40': {'label': 'Fast Response Plumbing & Rooter — official site',
         'publisher': 'Fast Response Plumbing & Rooter',
         'url': 'https://www.fastresponseplumbingsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company prints CSLB #1024971 C-36, phone 415-596-6115, email jtfastresponseplumbing@gmail.com; '
                     'serves houses/apartments/HOAs/property managers; free in-person per-job quotes; self-claimed 4.9 '
                     '/ 1,500 reviews on Yelp & Google',
         'note': 'Read directly 2026-11-08. Review aggregate is a company claim, not independently verified.'},
 'S41': {'label': 'General SF — official site',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Company site lists Electrical, Plumbing, Building and Bathroom & Kitchen services and prints '
                     "'CSLB. 959843'",
         'note': 'Read directly. Company self-description is not independent verification.'},
 'S42': {'label': 'Handyman Heroes — official site',
         'publisher': 'Handyman Heroes Inc',
         'url': 'https://www.handymanhero.es/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company homepage advertises construction, electrical, plumbing and handyman services; states '
                     'Licensed C-10 and Licensed C-36; company-selected testimonials include drywall patching',
         'note': 'Read directly 2026-11-08. CSLB #1003394 lists B + C-36 only; C-10 claim is flagged.'},
 'S43': {'label': 'Ace Plumbing & Rooter — official site',
         'publisher': 'Ace Plumbing & Rooter Inc',
         'url': 'https://www.aceplumbingandrooter.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists license #829071 with A/B/C4/C10/C16/C36; residential/commercial plumbing; '
                     'HOA/property-manager service; phone (415) 824-6444',
         'note': 'Read directly 2026-11-08. Classifications confirmed on CSLB.'},
 'S44': {'label': 'Project brief (owner-provided primary record)',
         'publisher': "This project's own record, published on this site",
         'url': 'brief.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Owner-provided problem statement, three 2026-08-30 estimates, access constraints, service '
                     'requirements, tenant-occupancy context and publication/process requirements',
         'note': 'Primary record transcribed 2026-11-08. Not an independent public source; official-verification cells '
                 'remain blank and UNVERIFIED.'},
 'S45': {'label': 'COORDINATION.md — shared task board',
         'publisher': 'This repository',
         'url': 'https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Task claims, handoffs, verification log, irregularities, PR and merge record',
         'note': 'Shared board read and appended in this session; claim commit b2fd513 pushed.'},
 'S46': {'label': 'Published GitHub Pages site',
         'publisher': 'GitHub Pages / this repository',
         'url': 'https://karagemop466-tech.github.io/Korea7/',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Live landing page location for this dashboard',
         'note': 'Pages source is branch main, path /.'},
 'S47': {'label': 'Repository README',
         'publisher': 'This repository',
         'url': 'https://github.com/karagemop466-tech/Korea7/blob/main/README.md',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Repository README; previously led with unrelated GEMS audit, refreshed in this integration to '
                     'point to the canonical overflow dashboard while preserving legacy-project notes',
         'note': 'Read locally 2026-11-08.'},
 'S48': {'label': 'Legacy GEMS site (archived)',
         'publisher': 'This repository',
         'url': 'docs/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Unrelated legacy project pages retained in the repo',
         'note': 'Internal link, not edited by this session.'},
 'S49': {'label': 'Parallel microsite (archived)',
         'publisher': 'This repository',
         'url': 'bathtub-overflow/executive-summary.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': "Prior session's overflow pages, retained unpublished-from-nav as archive",
         'note': 'Internal link, not edited by this session.'},
 'S50': {'label': 'Parallel microsite (archived)',
         'publisher': 'This repository',
         'url': 'docs/bath/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': "Prior session's docs/bath pages, retained as archive",
         'note': 'Internal link, not edited by this session.'},
 'S51': {'label': 'Parallel dashboard (archived)',
         'publisher': 'This repository',
         'url': 'docs/plumbing-index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': "Prior session's docs/overflow dashboard, retained as archive",
         'note': 'Internal link, not edited by this session.'},
 'S52': {'label': 'Open PR #32 (stale parallel session)',
         'publisher': 'GitHub',
         'url': 'https://github.com/karagemop466-tech/Korea7/pull/32',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'PR #32 remains OPEN and CONFLICTING; last updated 2026-11-06T13:45:52Z',
         'note': 'Checked with gh 2026-11-08. Left untouched.'},
 'S53': {'label': 'SFGate Home Guides — trip lever article (DEAD)',
         'publisher': 'SFGate / Weekand',
         'url': 'https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html',
         'tier': 'publisher',
         'status': 'dead',
         'checked': '2026-11-07',
         'supports': 'Removed from all active citations',
         'note': 'Redirects to weekand.com with empty content on 2026-11-07. Not linked from any table row; retained '
                 'here as a labeled documentation row.'},
 'S56': {'label': 'CSLB License Detail #1115649 — Rapid Flow Plumbing & Rooter Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Active B + C-36; phone (415) 866-8401; 230 Edinburgh St SF; expires 2028-01-31; $25,000 bond; '
                     'workers compensation exempt/no employees',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:34 PM.'},
 'S57': {'label': "CSLB License Detail #841229 — Manny's Plumbing & Rooter",
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Active C-36 + B; phone (650) 207-5733; 41 Midvale Drive Daly City; expires 2028-06-30; $25,000 '
                     'bond; workers compensation exempt/no employees',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:55:34 PM.'},
 'S58': {'label': 'Shortlist — who can do the plumbing and the drywall',
         'publisher': 'This repository (parallel session)',
         'url': 'shortlist.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Ranked shortlist of dual-classified (B + C-36) firms with a vetting script',
         'note': 'Page produced by a concurrent session, merged unchanged and linked from the dashboard navigation.'},
 'S60': {'label': 'SF overflow audit — parallel session dashboard',
         'publisher': 'This repository (parallel session)',
         'url': 'sf-overflow-audit/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': 'Independent 9-page audit dashboard with 11 CSLB records, Watco/Oatey technical notes and 15 '
                     'flagged items',
         'note': 'Disjoint file scope produced by session arena/2baecdab-korea7, merged unchanged; linked here in '
                 'response to its cross-link request.'},
 'S59': {'label': 'Verification log — earlier session',
         'publisher': 'This repository (parallel session)',
         'url': 'verification-log.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-07',
         'supports': "Earlier session's line-by-line verification and correction log",
         'note': 'Preserved verbatim from the add/add conflict on verification.html; linked from repo-review.html.'},
 'S55': {'label': 'Source ledger (this site)',
         'publisher': 'This dashboard',
         'url': 'sources.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Documentation rows about sources removed from active citations',
         'note': 'Internal page on this site. Dead URLs are shown there as plain text, never as links.'},
 'S54': {'label': 'InspectAndTest — bathtub overflow guide (DEAD)',
         'publisher': 'InspectAndTest',
         'url': 'https://inspectandtest.net/guides/bathtub-overflow-drain/',
         'tier': 'publisher',
         'status': 'dead',
         'checked': '2026-11-07',
         'supports': 'Removed from all active citations',
         'note': 'HTTP 500 on 2026-11-07. Not linked from any table row; retained here as a labeled documentation '
                 'row.'},
 'S61': {'label': 'CSLB License Detail #1025814 — The Genteel Plumbers Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1025814',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Active B + C-36; phone (833) 436-8335; 1181 Revere Ave SF; expires 2027-04-30; $25,000 bond; '
                     "workers' compensation insured through 2027-01-24",
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:56:58 PM.'},
 'S62': {'label': 'CSLB License Detail #995163 — Bernal Hill Drywall Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Active C-9 + B; phone (415) 533-8274; 720 Anderson St SF; expires 2028-07-31; $25,000 bond; '
                     "workers' compensation insured through 2027-03-10",
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:58:18 PM.'},
 'S63': {'label': 'CSLB License Detail #1009195 — Advanced Plumbing and Drain Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1009195',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Active C-36; phone (415) 744-4944; additional status warns license may be suspended at a future '
                     'date for failure to resolve an outstanding final liability',
         'note': 'Read directly; record stamped Data current as of 11/8/2026 2:58:23 PM.'},
 'S64': {'label': 'General SF — Building services',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/building',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company advertises rough/finish plumbing and sheetrock/tape/texture; prints CSLB 959843 and '
                     '(650) 303-1515',
         'note': 'First-party service advertisement, not independent proof of job capability.'},
 'S65': {'label': 'Handyman Heroes — Handyman services',
         'publisher': 'Handyman Heroes Inc',
         'url': 'https://www.handymanhero.es/handyman-services/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company advertises sheetrock/wall repairs and plumbing for San Francisco homes and apartments; '
                     'license #1003394; 1-844-382-4376',
         'note': 'First-party service advertisement, not independent proof of job capability.'},
 'S66': {'label': 'Genteel Plumbers — official site',
         'publisher': 'The Genteel Plumbers Inc',
         'url': 'https://www.genteelplumbers.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'San Francisco plumbing/drain/leak services; FAQ states $149 dispatch fee applied to services; '
                     'flat-rate pricing; 24/7; does not serve Financial District; phone 415-465-5853; drywall not '
                     'advertised on fetched page',
         'note': 'First-party page read 2026-11-08. Dispatch fee is not a quote for this repair.'},
 'S67': {'label': 'Rapid Flow Plumbing & Rooter — official site',
         'publisher': 'Rapid Flow Plumbing & Rooter Inc',
         'url': 'https://www.rapidflowbayarea.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Prints license #1115649 B/C-36; advertises plumbing and general contracting/remodels in San '
                     'Francisco',
         'note': 'First-party advertisement. Contact page also lists (415) 866-8401 for photos/texts.'},
 'S68': {'label': 'Rapid Flow — contact page',
         'publisher': 'Rapid Flow Plumbing & Rooter Inc',
         'url': 'https://www.rapidflowbayarea.com/contact',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Lists (415) 866-8401 for photos/texts and 230 Edinburgh St, San Francisco',
         'note': 'First-party contact page; main call button uses a different toll-free number.'},
 'S69': {'label': "Manny's Plumbing & Rooter — official site",
         'publisher': "Manny's Plumbing & Rooters",
         'url': 'https://www.mannysplumbingandremodeling.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Prints license #841229; advertises tub install, drain replacement, kitchen/bath remodeling; '
                     'service to surrounding areas of San Mateo & San Francisco Counties',
         'note': 'First-party advertisement; exact job acceptance unverified.'},
 'S70': {'label': 'Bernal Hill Drywall — official site',
         'publisher': 'Bernal Hill Drywall Inc',
         'url': 'https://www.bernalhilldrywall.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Advertises drywall installation, patching, painting, texture matching and water-damage '
                     'build-backs in San Francisco',
         'note': 'First-party advertisement. Plumbing is not advertised; CSLB record has C-9 + B, not C-36.'},
 'S71': {'label': 'Bernal Hill Drywall — customer testimonials',
         'publisher': 'Bernal Hill Drywall Inc',
         'url': 'https://www.bernalhilldrywall.com/reviews.html',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company-published testimonials describing detail/tidiness and a high-rise condominium closet '
                     'remodel; links to its Yelp page',
         'note': 'Company-selected testimonials, not independent verification.'},
 'S72': {'label': 'Ace Plumbing & Rooter — HOAs & property managers',
         'publisher': 'Ace Plumbing & Rooter Inc',
         'url': 'https://www.aceplumbingandrooter.com/commercial-plumber/hoa-property-managers/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company describes commercial plumbing for HOAs/property managers in San Francisco and nearby '
                     'cities; free estimates; (415) 824-6444',
         'note': 'First-party service description, not proof of this specific repair or drywall scope.'},
 'S73': {'label': 'BBB — Ace Plumbing & Rooter customer reviews',
         'publisher': 'Better Business Bureau',
         'url': 'https://www.bbb.org/us/ca/san-francisco/profile/plumber/ace-plumbing-and-rooter-inc-1116-58941/customer-reviews',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Page shows 4.76/5 average of 51 customer reviews; an 04/06/2025 review describes a family-run SF '
                     'apartment building using Ace as its plumbing resource',
         'note': 'Third-party customer statements; BBB states it does not verify third-party accuracy. Not license or '
                 'job-capability verification.'},
 'S74': {'label': 'Diamond Certified — Ace Plumbing & Rooter report',
         'publisher': 'Diamond Certified',
         'url': 'https://www.diamondcertified.org/report/ace-plumbing-and-rooter/',
         'tier': 'platform',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'July 2026 summary update; 220 surveys; 4.6 rating; 20 consecutive years; service area San '
                     'Francisco, South SF, Colma, Daly City, Brisbane; free estimates; 24/7; listed phones (415) '
                     '523-0012 and (415) 797-4197',
         'note': 'Third-party research/review platform read directly 2026-11-08; not a government license record. '
                 'Listed phones differ from CSLB (415) 824-6444; flagged as a directory/contact discrepancy.'},
 'S75': {'label': 'CSLB — C-9 Drywall classification',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'C-9 covers gypsum wallboard assemblies, taping and texturing',
         'note': 'Read directly 2026-11-08.'},
 'S76': {'label': 'CSLB — B General Building classification',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'B classification definition and limits; appropriate specialty license or subcontractor '
                     'requirements',
         'note': 'Read directly 2026-11-08.'},
 'S77': {'label': 'CSLB — How do I find the right licensed contractor?',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'At least three written bids on identical scope; do not automatically accept lowest; verify '
                     "license/address/phone/workers' comp and general liability; $25,000 license bond",
         'note': 'Read directly 2026-11-08.'},
 'S78': {'label': 'CSLB — Contract and binding agreements',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/Consumers/Hire_A_Contractor/Contracts_And_Binding_Agreements.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Written contract should detail work, price, payments, permits, completion; down payment no more '
                     'than 10% or $1,000 whichever less, subject to stated bond exception',
         'note': 'Read directly 2026-11-08.'},
 'S79': {'label': 'SF.gov — Apply for a kitchen or bath remodel permit',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/apply-kitchen-or-bath-remodel-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Online path for in-kind fixture replacement with no structural work; R-2 apartment owners must '
                     'hire contractors for electrical/plumbing; related permits and inspections',
         'note': 'Read directly 2026-11-08. Exact path for this concealed repair not determined.'},
 'S80': {'label': 'SF DBI — department page',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/departments--department-building-inspection',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'DBI issues construction permits and inspects for code/permit scope; PermitSF portal; current '
                     'codes guidance',
         'note': 'Read directly 2026-11-08.'},
 'S81': {'label': 'GitHub Docs — Creating a GitHub Pages site',
         'publisher': 'GitHub',
         'url': 'https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Pages publishing source, entry file, public availability and deployment workflow guidance',
         'note': 'Read directly 2026-11-08.'},
 'S82': {'label': 'Yelp — Drywall contractors in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Drywall+Contractors&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Category discovery link for drywall/ceiling repair; search snippets mention General SF ceiling '
                     'drywall services',
         'note': 'Direct fetch HTTP 403 on 2026-11-08. Snippets are third-party, date-variable and not official '
                 'verification.'},
 'S83': {'label': 'Yelp — Ace Plumbing & Rooter',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Business review discovery link',
         'note': 'Direct Yelp access blocked in this environment; no rating value is asserted from this URL.'},
 'S84': {'label': 'Yelp — Genteel Plumbers',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/genteel-plumbers-san-francisco-7',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Yelp business discovery link; search-index snippet shows 4.7/519 at 1314 22nd Ave Ste 007',
         'note': 'Direct www Yelp fetch HTTP 403 2026-11-08. Snippet is third-party and conflicts with CSLB '
                 'address/phone; not current platform verification.'},
 'S85': {'label': 'Yelp — Bernal Hill Drywall',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/bernal-hill-drywall-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': "Business review discovery link surfaced on the company's own reviews page",
         'note': 'Direct Yelp access blocked in this environment; no rating value is asserted from this URL.'},
 'S86': {'label': 'Advanced Plumbing & Drain Cleaning — New Jersey website (not matched)',
         'publisher': 'AAA Advanced Plumbing & Drain Cleaning, Inc.',
         'url': 'https://advancedplumbinganddrain.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Fetched site describes a Totowa, New Jersey business serving Hudson/Passaic counties; phone '
                     '(973) 278-1948',
         'note': 'Read directly 2026-11-08. NOT matched to CSLB #1009195 (San Francisco). Used only to flag the '
                 'identity mismatch.'},
 'S87': {'label': 'Repository line-by-line audit artifact',
         'publisher': 'This repository',
         'url': 'data/canonical/repo_audit.md',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Per-file inventory, text-line counts, parse checks, merge-marker/privacy/template-marker scan '
                     'and irregularity flags',
         'note': 'Generated by scripts/audit_repository.py in this session.'},
 'S88': {'label': 'Open PR #42 (stale parallel session)',
         'publisher': 'GitHub',
         'url': 'https://github.com/karagemop466-tech/Korea7/pull/42',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'PR #42 remains OPEN and CONFLICTING; last updated 2026-11-07T20:41:27Z',
         'note': 'Checked with gh 2026-11-08. Left untouched.'},
 'S89': {'label': 'Field-level source checks (JSON)',
         'publisher': 'This repository',
         'url': 'data/canonical/source_checks.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Exact CSLB timestamps, official phones/addresses/classes/status, company-page observations, rule '
                     'sources and blocked Yelp fetches',
         'note': 'Persisted 2026-11-08 from direct reads; no provider outreach.'},
 'S90': {'label': 'Decision analysis (JSON)',
         'publisher': 'This dashboard',
         'url': 'data/canonical/decision_analysis.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Explicit weights, 0-2 evidence scores, weighted totals and tie-breaks for contractor suitability '
                     'ranking',
         'note': 'Analyst judgment from cited evidence; not an official rating or a capability guarantee.'}}

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

TABLES = {'problem': {'title': 'Problem snapshot (owner-provided)',
             'columns': ['Item', 'Detail as provided', 'Officially verified value', 'Provenance', 'Source'],
             'rows': [{'cells': ['Failed component',
                                 'Bathtub wastewater overflow trip lever stuck inside concealed plumbing behind the '
                                 'wall',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S14']},
                      {'cells': ['Access problem',
                                 'Owner reports 5+ licensed plumbers could not remove it safely from above because of '
                                 'damage risk to hidden plumbing',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S18']},
                      {'cells': ['Reported fallback',
                                 'Work from below; a storage unit is underneath, so the drywall ceiling may need to be '
                                 'opened',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S02']},
                      {'cells': ['Service requirement',
                                 'One provider for drywall and plumbing; delicate work in a tenant-occupied San '
                                 'Francisco unit',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S05']},
                      {'cells': ['Preference',
                                 'Above-access removal is preferred if it can be done safely',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S20']},
                      {'cells': ['Location',
                                 'San Francisco, California',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S01']},
                      {'cells': ['Pictures',
                                 'No reference photos were supplied to this session; tub material, layout and access '
                                 'remain unconfirmed',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S45']}],
             'caption': 'Owner facts are transcribed from the <a href="brief.html">project brief</a>. The '
                        'verified-value column is blank and flagged because no public official source confirms them. '
                        'Context links describe components/rules only; they do not confirm the owner’s facts.'},
 'estimates': {'title': 'Estimates reported by owner — 2026-08-30',
               'columns': ['#',
                           'Company / official identity',
                           'Scope as reported',
                           'Owner-reported amount',
                           'Verified job price',
                           'Date / provenance',
                           'License status',
                           'Source'],
               'rows': [{'cells': ['1',
                                   '<strong>Expert Plumbing Solutions</strong><br><a '
                                   'href="https://www.eplumbingsolutions.com/" target="_blank" rel="noopener '
                                   'noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #977638</a>',
                                   'Replacing waste and overflow',
                                   '<strong>$614</strong><br><span class="pill '
                                   'warn">UNVERIFIED</span><br><small>owner-provided — no official source '
                                   'exists</small>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '2026-08-30<br><small>owner-reported date</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S06', 'S38']},
                        {'cells': ['2',
                                   '<strong>Bay Area Plumbing</strong><br><a href="https://www.bayareaplumbingsf.com/" '
                                   'target="_blank" rel="noopener noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #757796</a>',
                                   'Replace lever for bathtub plug and spout with diverter; includes labor and '
                                   'materials',
                                   '<strong>$550</strong><br><span class="pill '
                                   'warn">UNVERIFIED</span><br><small>owner-provided — no official source '
                                   'exists</small>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '2026-08-30<br><small>owner-reported date</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S07', 'S39']},
                        {'cells': ['3',
                                   '<strong>Fast Response Plumbing &amp; Rooter</strong><br><a '
                                   'href="https://www.fastresponseplumbingsf.com/" target="_blank" rel="noopener '
                                   'noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #1024971</a>',
                                   'Repair or adjust bathtub wastewater plunger handle',
                                   '<strong>$135</strong><br><span class="pill '
                                   'warn">UNVERIFIED</span><br><small>owner-provided — no official source '
                                   'exists</small>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '2026-08-30<br><small>owner-reported date</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S08', 'S40']}],
               'caption': 'The three amounts are retained as explicitly attributed owner reports, not confirmed '
                          'prices. Verified job price is blank and UNVERIFIED. Company identity and active C-36 status '
                          'are independently checked on CSLB. The scopes differ and none includes a confirmed '
                          'drywall/ceiling restoration line.'},
 'brief_quotes': {'title': 'Brief transcription — quoted amounts (NOT verified)',
                  'columns': ['#',
                              'Company',
                              'Quoted scope (transcription)',
                              'Amount as stated in brief',
                              'Date stated',
                              'Status',
                              'Record type',
                              'Source'],
                  'rows': [{'cells': ['1',
                                      'Expert Plumbing Solutions',
                                      'Remove bathtub wastewater overflow trip lever; replacing waste and overflow',
                                      '$614',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                      'official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S06']},
                           {'cells': ['2',
                                      'Bay Area Plumbing',
                                      'Replace lever for bathtub plug and spout with diverter, includes labor and '
                                      'materials',
                                      '$550',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                      'official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S07']},
                           {'cells': ['3',
                                      'Fast Response',
                                      'Repair or adjust bath tub wastewater plunger handle',
                                      '$135',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                      'official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S08']}],
                  'caption': 'Transcription of the owner brief only. These figures never appear in a verified-price '
                             'cell. Source: <a href="brief.html">project brief</a>.'},
 'benchmarks': {'title': 'Publisher cost benchmarks — context, not quotes',
                'columns': ['Benchmark',
                            'Value as published',
                            'Publisher date',
                            'Scope / limit',
                            'Evidence grade',
                            'Source'],
                'rows': [{'cells': ['Bathtub/shower drain replacement — normal range',
                                    '<strong>$500–$1,020</strong><br>avg $700 · low $230 · high $1,170',
                                    '2026-09-18',
                                    'National publisher data; not a San Francisco quote',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S15']},
                         {'cells': ['Plumber labor for drain replacement',
                                    '$45–$200 / hour',
                                    '2026-09-18',
                                    'National publisher data',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S15']},
                         {'cells': ['New drywall installation if wall opened',
                                    'about $2,100',
                                    '2026-09-18',
                                    'Add-on context; not a ceiling patch quote',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S15']},
                         {'cells': ['Drain unclogging',
                                    'avg $225',
                                    '2026-09-18',
                                    'Possible add-on',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S15']},
                         {'cells': ['Water-damage repair',
                                    '$1,350–$6,100',
                                    '2026-09-18',
                                    'Possible add-on if hidden damage is found',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S15']},
                         {'cells': ['Bathroom leak repair — normal range',
                                    '<strong>$150–$600</strong><br>avg $275 · complex up to $4,000',
                                    '2026-10-28',
                                    'Access and hidden pipes drive cost',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S16']},
                         {'cells': ['Drywall/tile/flooring follow-up after leak',
                                    '$300–$930',
                                    '2026-10-28',
                                    'Add-on context',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S16']},
                         {'cells': ['Small-job call-out minimum',
                                    '$50–$200',
                                    '2026-10-28',
                                    'Adjustment-only visit context',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S16']},
                         {'cells': ['Worn-out tub drain replacement',
                                    'avg $700',
                                    '2026-10-28',
                                    'Publisher notes easier access lowers cost',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S16']},
                         {'cells': ['Overflow component in itemized tub installation',
                                    '$163',
                                    '2026-03-05',
                                    'Component average only; not labor',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S19']},
                         {'cells': ['Drain component in itemized tub installation',
                                    '$190',
                                    '2026-03-05',
                                    'Component average only; not labor',
                                    '<span class="pill info">publisher verified</span>'],
                          'src': ['S19']},
                         {'cells': ['Typical bathtub drain repairs / duration',
                                    '$80–$600 · 1–4 hours',
                                    '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                    'warn">UNVERIFIED</span>',
                                    'Houston-area trade blog; publication date not shown on fetched page',
                                    '<span class="pill warn">value read / date blank</span>'],
                          'src': ['S22']}],
                'caption': 'Each row links to the original publisher. Values were read directly 2026-11-08. These are '
                           'national or trade-blog benchmarks, not official San Francisco prices and not quotes for '
                           'this job. Where a publisher date was not visible, the date cell is blank and flagged.'},
 'decision_criteria': {'title': 'Decision criteria and weights',
                       'columns': ['ID',
                                   'Criterion',
                                   'Weight',
                                   'Scoring rule (0–2)',
                                   'Why it matters',
                                   'Grade',
                                   'Source'],
                       'rows': [{'cells': ['C1',
                                           'Combined plumbing + drywall evidence',
                                           '30%',
                                           '2 = company page explicitly advertises both plumbing and drywall/wall '
                                           'repair; 1 = active B + C-36 but drywall not explicitly advertised; 0 = '
                                           'C-36 only.',
                                           'One-company preference is central, but a license class is not proof of job '
                                           'capability.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S44', 'S76', 'S05']},
                                {'cells': ['C2',
                                           'Occupied / multi-unit evidence',
                                           '20%',
                                           '2 = independent third-party review explicitly describes an '
                                           'occupied/multi-unit property; 1 = company or search-index evidence '
                                           'advertises apartments/HOAs/property managers; 0 = no such evidence found.',
                                           'Tenant-occupied delicate work requires protection, communication and '
                                           'references.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S44', 'S77', 'S73']},
                                {'cells': ['C3',
                                           'License / insurance / disclosure risk',
                                           '20%',
                                           '2 = active C-36, workers compensation insured, no additional warning, '
                                           'license expiry more than 90 days away, and no workers-compensation policy '
                                           'expiry within 90 days; 1 = exempt/no employees, disclosure, near-term '
                                           'license/policy expiry, or other caution; 0 = future-suspension additional '
                                           'status.',
                                           'CSLB status, bond, workers compensation and disclosures are official risk '
                                           'signals.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S04', 'S77', 'S63']},
                                {'cells': ['C4',
                                           'San Francisco service-area fit',
                                           '10%',
                                           '2 = company explicitly serves San Francisco; 1 = SF address of record or '
                                           'surrounding-counties service only; 0 = service area not '
                                           'established/mismatched.',
                                           'Address of record is not the same as confirmed service at the job address.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S04', 'S66', 'S69']},
                                {'cells': ['C5',
                                           'Review evidence quality',
                                           '10%',
                                           '2 = directly read third-party platform with substantial reviews; 1 = '
                                           'search-index snippet or company-selected testimonial; 0 = no usable review '
                                           'evidence found.',
                                           'Reviews are third-party evidence, never license verification.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S73', 'S74', 'S35']},
                                {'cells': ['C6',
                                           'Cost transparency',
                                           '10%',
                                           '2 = published itemized price for this exact scope; 1 = owner-reported '
                                           'quote, published dispatch fee, or free-estimate policy; 0 = no cost '
                                           'evidence found.',
                                           'No provider has published a verified combined price for this job.',
                                           '<span class="pill info">analyst judgment</span>'],
                                 'src': ['S44', 'S66', 'S78']}],
                       'caption': 'Weighted total = sum(weight × score / 2), maximum 100. Scores measure the strength '
                                  'of published evidence, not guaranteed workmanship. Tie-break: higher C3 risk score, '
                                  'then higher C1 combined-scope score, then alphabetical. Weights and scores are '
                                  'analyst judgment; every factual input links to its original source.'},
 'decision_matrix': {'title': 'Evidence scores (0–2) and weighted totals',
                     'columns': ['Candidate',
                                 'C1 scope',
                                 'C2 occupied',
                                 'C3 risk',
                                 'C4 area',
                                 'C5 reviews',
                                 'C6 cost',
                                 'Total /100',
                                 'Grade',
                                 'Source'],
                     'rows': [{'cells': ['Ace Plumbing & Rooter',
                                         '1',
                                         '2',
                                         '2',
                                         '2',
                                         '2',
                                         '1',
                                         '<strong>80</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S11', 'S72', 'S73', 'S74']},
                              {'cells': ['Handyman Heroes Inc',
                                         '2',
                                         '1',
                                         '1',
                                         '2',
                                         '1',
                                         '1',
                                         '<strong>70</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S10', 'S65', 'S36', 'S12']},
                              {'cells': ['General SF',
                                         '2',
                                         '1',
                                         '1',
                                         '2',
                                         '1',
                                         '0',
                                         '<strong>65</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S09', 'S35']},
                              {'cells': ['The Genteel Plumbers Inc',
                                         '1',
                                         '0',
                                         '1',
                                         '2',
                                         '1',
                                         '1',
                                         '<strong>45</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S61', 'S84']},
                              {'cells': ['Rapid Flow Plumbing & Rooter Inc',
                                         '1',
                                         '0',
                                         '1',
                                         '2',
                                         '0',
                                         '1',
                                         '<strong>40</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S56', 'S68']},
                              {'cells': ['Fast Response Plumbing & Rooter',
                                         '0',
                                         '1',
                                         '1',
                                         '2',
                                         '1',
                                         '1',
                                         '<strong>40</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S08', 'S44']},
                              {'cells': ['Expert Plumbing Solutions',
                                         '0',
                                         '0',
                                         '2',
                                         '2',
                                         '0',
                                         '1',
                                         '<strong>35</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S06', 'S44']},
                              {'cells': ["Manny's Plumbing & Rooter",
                                         '1',
                                         '0',
                                         '1',
                                         '1',
                                         '0',
                                         '0',
                                         '<strong>30</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S57']},
                              {'cells': ['Bay Area Plumbing',
                                         '0',
                                         '0',
                                         '1',
                                         '2',
                                         '0',
                                         '1',
                                         '<strong>25</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S07', 'S44']},
                              {'cells': ['Advanced Plumbing and Drain Inc',
                                         '0',
                                         '0',
                                         '0',
                                         '1',
                                         '0',
                                         '0',
                                         '<strong>5</strong>',
                                         '<span class="pill info">analyst scoring</span>'],
                               'src': ['S63', 'S86']}],
                     'caption': 'Scores are evidence-strength judgments defined on the criteria table, not official '
                                'ratings. Bernal Hill Drywall is a specialist partner and is not scored against '
                                'plumbing candidates. Full machine-readable model: <a '
                                'href="data/canonical/decision_analysis.json">decision_analysis.json</a>.'},
 'ranking': {'title': 'Contractors ranked best to least suitable for this brief',
             'columns': ['Rank',
                         'Company / official phone',
                         'Score',
                         'Best-fit role',
                         'Why it ranks here',
                         'Main limitation',
                         'Cost basis',
                         'Status',
                         'Source'],
             'rows': [{'cells': ['1',
                                 '<strong>Ace Plumbing & Rooter</strong><br><a href="tel:+14158246444">(415) '
                                 '824-6444</a><br><a href="https://www.aceplumbingandrooter.com/" target="_blank" '
                                 'rel="noopener noreferrer">official site</a>',
                                 '80/100',
                                 'Plumbing + possible building scope',
                                 'Strongest occupied-property evidence: BBB review from a family-run SF apartment '
                                 'building plus HOA/property-manager page; insured C-36/B. Drywall restoration is not '
                                 'explicitly advertised, so pair with a drywall specialist unless the company confirms '
                                 'scope.',
                                 'Drywall scope unconfirmed; no job quote.',
                                 'Free estimates advertised; no job price published',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S11', 'S43', 'S72', 'S73', 'S74']},
                      {'cells': ['2',
                                 '<strong>Handyman Heroes Inc</strong><br><a href="tel:+18443824376">(844) '
                                 '382-4376</a><br><a href="https://www.handymanhero.es/" target="_blank" rel="noopener '
                                 'noreferrer">official site</a>',
                                 '70/100',
                                 'Plumbing + possible building scope',
                                 'Explicitly advertises sheetrock/wall repairs plus plumbing for SF homes/apartments; '
                                 'B + C-36 and insured. Official complaint disclosure and a site C-10 claim absent '
                                 'from the CSLB record require review.',
                                 'CSLB disclosure; C-10 website claim not on record; Yelp blocked.',
                                 'Free consultation advertised; no job price published',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S10', 'S42', 'S65', 'S36', 'S12']},
                      {'cells': ['3',
                                 '<strong>General SF</strong><br><a href="tel:+16503031515">(650) 303-1515</a><br><a '
                                 'href="https://generalsf.com/building" target="_blank" rel="noopener '
                                 'noreferrer">official site</a>',
                                 '65/100',
                                 'Plumbing + possible building scope',
                                 'Building page explicitly lists rough/finish plumbing and sheetrock/tape/texture; B + '
                                 'C-36. Best documented one-company scope, but workers compensation is exempt/no '
                                 'employees and review evidence is search-index only.',
                                 'WC exempt; no published cost; exact crew/coverage unconfirmed.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S09', 'S64', 'S35']},
                      {'cells': ['4',
                                 '<strong>The Genteel Plumbers Inc</strong><br><a href="tel:+18334368335">(833) '
                                 '436-8335</a><br><a href="https://www.genteelplumbers.com/" target="_blank" '
                                 'rel="noopener noreferrer">official site</a>',
                                 '45/100',
                                 'Plumbing + possible building scope',
                                 'Active B + C-36, insured, flat-rate pricing and published dispatch fee. Drywall is '
                                 'not advertised on the fetched page; company excludes the Financial District.',
                                 'Drywall unadvertised; service-area exclusion; workers-compensation policy expires '
                                 '2027-01-24; Yelp snippet address/phone conflict.',
                                 '$149 dispatch fee applied to services (company published); not a job quote',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S61', 'S66', 'S84']},
                      {'cells': ['5',
                                 '<strong>Rapid Flow Plumbing & Rooter Inc</strong><br><a '
                                 'href="tel:+14158668401">(415) 866-8401</a><br><a '
                                 'href="https://www.rapidflowbayarea.com/" target="_blank" rel="noopener '
                                 'noreferrer">official site</a>',
                                 '40/100',
                                 'Plumbing + possible building scope',
                                 'Active B + C-36; advertises plumbing plus general contracting/remodels and one crew. '
                                 'Drywall/ceiling restoration and occupied-unit references are not explicitly '
                                 'documented.',
                                 'WC exempt; drywall and occupied-unit evidence limited.',
                                 'Free estimate advertised; no job price published',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S56', 'S67', 'S68']},
                      {'cells': ['6',
                                 '<strong>Fast Response Plumbing & Rooter</strong><br><a href="tel:+14155966115">(415) '
                                 '596-6115</a><br><a href="https://www.fastresponseplumbingsf.com/" target="_blank" '
                                 'rel="noopener noreferrer">official site</a>',
                                 '40/100',
                                 'Plumbing only / partner needed',
                                 'Company advertises houses/apartments/HOAs, free per-job quotes and company-selected '
                                 'testimonials; active insured C-36. Owner-reported scope is adjustment only, and '
                                 'workers compensation policy expires 2026-12-18.',
                                 'Adjustment scope may not solve seized assembly; WC renewal check; review aggregate '
                                 'is company claim.',
                                 '$135 owner-reported (unverified) — repair/adjust plunger handle',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S08', 'S40', 'S44']},
                      {'cells': ['7',
                                 '<strong>Expert Plumbing Solutions</strong><br><a href="tel:+14155315340">(415) '
                                 '531-5340</a><br><a href="https://www.eplumbingsolutions.com/" target="_blank" '
                                 'rel="noopener noreferrer">official site</a>',
                                 '35/100',
                                 'Plumbing only / partner needed',
                                 'Owner reports a full waste-and-overflow quote; active insured C-36. C-36 only, so '
                                 'drywall would need a separately licensed partner unless scope is confirmed '
                                 'otherwise.',
                                 'Owner quote unverified; no drywall classification; no occupied-unit review evidence '
                                 'found.',
                                 '$614 owner-reported (unverified) — waste & overflow',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S06', 'S38', 'S44']},
                      {'cells': ['8',
                                 '<strong>Manny\'s Plumbing & Rooter</strong><br><a href="tel:+16502075733">(650) '
                                 '207-5733</a><br><a href="https://www.mannysplumbingandremodeling.com/" '
                                 'target="_blank" rel="noopener noreferrer">official site</a>',
                                 '30/100',
                                 'Plumbing + possible building scope',
                                 'Active C-36 + B; advertises tub install, drain replacement and kitchen/bath '
                                 'remodeling. Service wording is surrounding areas of San Mateo & San Francisco '
                                 'Counties; drywall/ceiling and occupied-unit evidence are limited.',
                                 'WC exempt; Daly City address; exact SF service and drywall scope unconfirmed.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S57', 'S69']},
                      {'cells': ['9',
                                 '<strong>Bay Area Plumbing</strong><br><a href="tel:+14156688000">(415) '
                                 '668-8000</a><br><a href="https://www.bayareaplumbingsf.com/" target="_blank" '
                                 'rel="noopener noreferrer">official site</a>',
                                 '25/100',
                                 'Plumbing only / partner needed',
                                 'Active C-36; advertises SF residential/commercial plumbing and leak/pipe repair. '
                                 'Owner-reported quote is a different diverter scope; workers compensation is '
                                 'exempt/no employees.',
                                 'Quote scope differs; WC exempt; no drywall classification.',
                                 '$550 owner-reported (unverified) — plug/spout diverter',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S07', 'S39', 'S44']},
                      {'cells': ['10',
                                 '<strong>Advanced Plumbing and Drain Inc</strong><br><a href="tel:+14157444944">(415) '
                                 '744-4944</a>',
                                 '5/100',
                                 'Plumbing only / partner needed',
                                 'Active C-36 and insured, but CSLB carries an additional status warning that the '
                                 'license may be suspended at a future date for an unresolved final liability. A '
                                 'similarly named website is a New Jersey business and is not matched.',
                                 'Future-suspension warning; identity mismatch; not recommended without resolution.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill info">conditional recommendation</span>'],
                       'src': ['S63', 'S86', 'S86']}],
             'caption': 'Ranking is conditional desk research. No provider has been contacted and no provider has '
                        'confirmed this job. Active license status was checked 2026-11-08; re-check on the hire date. '
                        'Bernal Hill Drywall (#995163, (415) 533-8274) is the recommended drywall specialist partner, '
                        'not an all-in-one plumber.'},
 'contractors': {'title': 'Official license register — 11 records checked 2026-11-08',
                 'columns': ['Company / official phone',
                             'CSLB',
                             'Classifications',
                             'Status / expiry',
                             'Workers compensation / bond',
                             'Address on record',
                             'Cost basis for this job',
                             'Caution / role',
                             'Verification',
                             'Source'],
                 'rows': [{'cells': ['<strong>Ace Plumbing & Rooter</strong><br><a href="tel:+14158246444">(415) '
                                     '824-6444</a><br><a href="https://www.aceplumbingandrooter.com/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071" '
                                     'target="_blank" rel="noopener noreferrer">#829071</a>',
                                     'C36, A, C-4, C16, B, C10',
                                     '<span class="pill ok">current and active</span><br>expires 2027-06-30',
                                     'Insured; expires 2027-07-13<br>Bond $25,000',
                                     '1090 BRYANT STREET, SAN FRANCISCO, CA 94103-4417',
                                     'Free estimates advertised; no job price published',
                                     'Drywall scope unconfirmed; no job quote.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S11', 'S43', 'S72', 'S73', 'S74']},
                          {'cells': ['<strong>Handyman Heroes Inc</strong><br><a href="tel:+18443824376">(844) '
                                     '382-4376</a><br><a href="https://www.handymanhero.es/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394" '
                                     'target="_blank" rel="noopener noreferrer">#1003394</a>',
                                     'B, C36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-05-31',
                                     'Insured; expires 2027-04-25<br>Bond $25,000',
                                     '912 COLE ST # 202, SAN FRANCISCO, CA 94117',
                                     'Free consultation advertised; no job price published',
                                     'CSLB disclosure; C-10 website claim not on record; Yelp blocked.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S10', 'S42', 'S65', 'S36', 'S12']},
                          {'cells': ['<strong>General SF</strong><br><a href="tel:+16503031515">(650) '
                                     '303-1515</a><br><a href="https://generalsf.com/building" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843" '
                                     'target="_blank" rel="noopener noreferrer">#959843</a>',
                                     'B, C10, C36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-04-30',
                                     'Exempt; certified no employees at this time<br>Bond $25,000',
                                     '3624 IRVING STREET STE A, SAN FRANCISCO, CA 94122',
                                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                     'warn">UNVERIFIED</span>',
                                     'WC exempt; no published cost; exact crew/coverage unconfirmed.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S09', 'S64', 'S35']},
                          {'cells': ['<strong>The Genteel Plumbers Inc</strong><br><a href="tel:+18334368335">(833) '
                                     '436-8335</a><br><a href="https://www.genteelplumbers.com/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1025814" '
                                     'target="_blank" rel="noopener noreferrer">#1025814</a>',
                                     'C36, B',
                                     '<span class="pill ok">current and active</span><br>expires 2027-04-30',
                                     'Insured; expires 2027-01-24<br>Bond $25,000',
                                     '1181 REVERE AVE, SAN FRANCISCO, CA 94124',
                                     '$149 dispatch fee applied to services (company published); not a job quote',
                                     'Drywall unadvertised; service-area exclusion; workers-compensation policy '
                                     'expires 2027-01-24; Yelp snippet address/phone conflict.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S61', 'S66', 'S84']},
                          {'cells': ['<strong>Rapid Flow Plumbing & Rooter Inc</strong><br><a '
                                     'href="tel:+14158668401">(415) 866-8401</a><br><a '
                                     'href="https://www.rapidflowbayarea.com/" target="_blank" rel="noopener '
                                     'noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649" '
                                     'target="_blank" rel="noopener noreferrer">#1115649</a>',
                                     'B, C36',
                                     '<span class="pill ok">current and active</span><br>expires 2028-01-31',
                                     'Exempt; certified no employees at this time<br>Bond $25,000',
                                     '230 EDINBURGH ST, SAN FRANCISCO, CA 94112',
                                     'Free estimate advertised; no job price published',
                                     'WC exempt; drywall and occupied-unit evidence limited.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S56', 'S67', 'S68']},
                          {'cells': ['<strong>Fast Response Plumbing & Rooter</strong><br><a '
                                     'href="tel:+14155966115">(415) 596-6115</a><br><a '
                                     'href="https://www.fastresponseplumbingsf.com/" target="_blank" rel="noopener '
                                     'noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                     'target="_blank" rel="noopener noreferrer">#1024971</a>',
                                     'C36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-03-31',
                                     'Insured; expires 2026-12-18<br>Bond $25,000',
                                     '236 W POTRAL AVE #459, SAN FRANCISCO, CA 94127',
                                     '$135 owner-reported (unverified) — repair/adjust plunger handle',
                                     'Adjustment scope may not solve seized assembly; WC renewal check; review '
                                     'aggregate is company claim.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S08', 'S40', 'S44']},
                          {'cells': ['<strong>Expert Plumbing Solutions</strong><br><a href="tel:+14155315340">(415) '
                                     '531-5340</a><br><a href="https://www.eplumbingsolutions.com/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                     'target="_blank" rel="noopener noreferrer">#977638</a>',
                                     'C36',
                                     '<span class="pill ok">current and active</span><br>expires 2028-10-31',
                                     'Insured; expires 2027-07-19<br>Bond $25,000',
                                     '1465 44TH AVENUE, SAN FRANCISCO, CA 94122',
                                     '$614 owner-reported (unverified) — waste & overflow',
                                     'Owner quote unverified; no drywall classification; no occupied-unit review '
                                     'evidence found.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S06', 'S38', 'S44']},
                          {'cells': ['<strong>Manny\'s Plumbing & Rooter</strong><br><a href="tel:+16502075733">(650) '
                                     '207-5733</a><br><a href="https://www.mannysplumbingandremodeling.com/" '
                                     'target="_blank" rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229" '
                                     'target="_blank" rel="noopener noreferrer">#841229</a>',
                                     'C36, B',
                                     '<span class="pill ok">current and active</span><br>expires 2028-06-30',
                                     'Exempt; certified no employees at this time<br>Bond $25,000',
                                     '41 MIDVALE DRIVE, DALY CITY, CA 94015',
                                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                     'warn">UNVERIFIED</span>',
                                     'WC exempt; Daly City address; exact SF service and drywall scope unconfirmed.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S57', 'S69']},
                          {'cells': ['<strong>Bay Area Plumbing</strong><br><a href="tel:+14156688000">(415) '
                                     '668-8000</a><br><a href="https://www.bayareaplumbingsf.com/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                     'target="_blank" rel="noopener noreferrer">#757796</a>',
                                     'C36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-01-31',
                                     'Exempt; certified no employees at this time<br>Bond $25,000',
                                     '335 14TH AVENUE, SAN FRANCISCO, CA 94118',
                                     '$550 owner-reported (unverified) — plug/spout diverter',
                                     'Quote scope differs; WC exempt; no drywall classification.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S07', 'S39', 'S44']},
                          {'cells': ['<strong>Advanced Plumbing and Drain Inc</strong><br><a '
                                     'href="tel:+14157444944">(415) 744-4944</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1009195" '
                                     'target="_blank" rel="noopener noreferrer">#1009195</a>',
                                     'C36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-11-30',
                                     'Insured; expires 2027-08-21<br>Bond $25,000',
                                     '3450 SACRAMENTO ST 204, SAN FRANCISCO, CA 94118',
                                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                     'warn">UNVERIFIED</span>',
                                     'Future-suspension warning; identity mismatch; not recommended without '
                                     'resolution.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S63', 'S86', 'S86']},
                          {'cells': ['<strong>Bernal Hill Drywall Inc</strong><br><a href="tel:+14155338274">(415) '
                                     '533-8274</a><br><a href="https://www.bernalhilldrywall.com/" target="_blank" '
                                     'rel="noopener noreferrer">official site</a>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163" '
                                     'target="_blank" rel="noopener noreferrer">#995163</a>',
                                     'C-9, B',
                                     '<span class="pill ok">current and active</span><br>expires 2028-07-31',
                                     'Insured; expires 2027-03-10<br>Bond $25,000',
                                     '720 ANDERSON ST, SAN FRANCISCO, CA 94110',
                                     '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                     'warn">UNVERIFIED</span>',
                                     'Drywall specialist partner; no C-36 on record. Plumbing must be performed by a '
                                     'C-36 contractor or appropriately licensed prime/subcontractor.',
                                     '<span class="pill ok">CSLB verified</span>'],
                           'src': ['S62', 'S70', 'S71', 'S75']}],
                 'caption': 'All 11 CSLB records were read directly and printed current and active on 2026-11-08. Each '
                            'carries a $25,000 contractor bond. Workers-compensation exemption means the licensee '
                            'certified no employees at that time; it is not a finding of unlawful operation. General '
                            'liability insurance is not shown by these records and must be requested separately. '
                            'Addresses are transcribed from CSLB, including the record spelling “POTRAL” for Fast '
                            'Response.'},
 'review_evidence': {'title': 'Review and reputation evidence — third-party, not license verification',
                     'columns': ['Candidate / source',
                                 'Read method',
                                 'Value observed',
                                 'What it supports',
                                 'Limit / status',
                                 'Source'],
                     'rows': [{'cells': ['Ace — BBB customer reviews',
                                         'Direct fetch 2026-11-08',
                                         '4.76/5 from 51 reviews; 04/06/2025 review describes a family-run SF '
                                         'apartment building using Ace',
                                         'Occupied/multi-unit plumbing relationship; communication/property care '
                                         'themes',
                                         '<span class="pill info">third-party customer statements</span>'],
                               'src': ['S73', 'S11']},
                              {'cells': ['Ace — Diamond Certified report',
                                         'Direct fetch 2026-11-08',
                                         '4.6; 220 surveys; 20 consecutive years; July 2026 summary update',
                                         'Third-party research/review signal and service area; listed phones differ '
                                         'from CSLB',
                                         '<span class="pill info">third-party platform</span>'],
                               'src': ['S74', 'S11']},
                              {'cells': ['General SF — Yelp',
                                         'Search-index snippet; direct page HTTP 403',
                                         'Snippets show 4.8/336 and 4.8/302; one snippet mentions plumbing at an '
                                         'apartment the reviewer owns',
                                         'Discovery lead for plumbing/building reviews',
                                         '<span class="pill warn">UNVERIFIED current rating</span>'],
                               'src': ['S35', 'S09']},
                              {'cells': ['Handyman Heroes — Yelp',
                                         'Search-index snippet; direct page HTTP 403',
                                         '4.7/410; 1525 Waller St in snippet',
                                         'Discovery lead; address conflicts with CSLB 912 Cole St #202',
                                         '<span class="pill warn">UNVERIFIED current rating</span>'],
                               'src': ['S36', 'S10']},
                              {'cells': ['Genteel Plumbers — Yelp',
                                         'Search-index snippet; direct www page HTTP 403',
                                         '4.7/519; 1314 22nd Ave Ste 007 in snippet',
                                         'Discovery lead; address/phone conflict with CSLB/company page',
                                         '<span class="pill warn">UNVERIFIED current rating</span>'],
                               'src': ['S84', 'S61']},
                              {'cells': ['Expert Plumbing Solutions — Yelp',
                                         'Prior snapshot only; current direct fetch blocked',
                                         'Prior session recorded 4.8/81 on 2026-11-06',
                                         '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                         'class="pill warn">UNVERIFIED</span>',
                                         '<span class="pill warn">historical snapshot</span>'],
                               'src': ['S32', 'S06']},
                              {'cells': ['Bay Area Plumbing — Yelp',
                                         'Prior snapshot only; current direct fetch blocked',
                                         'Prior session recorded 4.8/175 on 2026-11-06',
                                         '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                         'class="pill warn">UNVERIFIED</span>',
                                         '<span class="pill warn">historical snapshot</span>'],
                               'src': ['S33', 'S07']},
                              {'cells': ['Fast Response — Yelp',
                                         'Prior snapshot only; current direct fetch blocked',
                                         'Prior session recorded 4.8/906 on 2026-11-06',
                                         '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                         'class="pill warn">UNVERIFIED</span>',
                                         '<span class="pill warn">historical snapshot</span>'],
                               'src': ['S34', 'S08']},
                              {'cells': ['Fast Response — company aggregate',
                                         'Company site direct fetch',
                                         '“4.9 · 1,500 Reviews on Yelp & Google”',
                                         'Company marketing claim only',
                                         '<span class="pill warn">UNVERIFIED aggregate</span>'],
                               'src': ['S40', 'S08']},
                              {'cells': ['Bernal Hill Drywall — testimonials',
                                         'Company site direct fetch',
                                         'Company-selected testimonials describe tidiness, detail and a high-rise '
                                         'condominium closet remodel',
                                         'Drywall finish/occupied-property lead',
                                         '<span class="pill warn">company-selected, not independent</span>'],
                               'src': ['S71', 'S62']},
                              {'cells': ['Angi — SF bathtub restoration category',
                                         'Direct fetch 2026-11-08',
                                         '17 verified reviews; last update Oct 14, 2024; '
                                         'older-home/apartment/concealed-leak review themes',
                                         'Category-level review context; some listed firms are not candidates and one '
                                         'is explicitly unlicensed',
                                         '<span class="pill info">third-party category evidence</span>'],
                               'src': ['S24', 'S04']}],
                     'caption': 'Yelp business/category pages return HTTP 403 in this environment. Search-index '
                                'snippets and prior snapshots are labeled third-party and are not current platform '
                                'verification. Review counts/ratings change; only CSLB verifies a California '
                                'contractor license.'},
 'platforms': {'title': 'Review/platform discovery links',
               'columns': ['Platform', 'San Francisco link', 'What was read', 'Status', 'Source'],
               'rows': [{'cells': ['Yelp — bathtub repair',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">Bathtub Repair in San Francisco</a>',
                                   'Category discovery link',
                                   '<span class="pill warn">HTTP 403 — manual review</span>'],
                         'src': ['S29']},
                        {'cells': ['Yelp — plumbers',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">Plumbers in San Francisco</a>',
                                   'Category discovery link',
                                   '<span class="pill warn">HTTP 403 — manual review</span>'],
                         'src': ['S30']},
                        {'cells': ['Yelp — drywall',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Drywall+Contractors&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">Drywall contractors in San Francisco</a>',
                                   'Category discovery link; direct fetch blocked',
                                   '<span class="pill warn">HTTP 403 — manual review</span>'],
                         'src': ['S82']},
                        {'cells': ['Angi — SF bathtub restoration',
                                   '<a '
                                   'href="https://www.angi.com/companylist/us/ca/san-francisco/bathtub-refinishing.htm" '
                                   'target="_blank" rel="noopener noreferrer">Bathtub restoration pros</a>',
                                   '17 verified reviews; last update Oct 14, 2024; customer statements about older SF '
                                   'homes/apartments',
                                   '<span class="pill ok">read directly 2026-11-08</span>'],
                         'src': ['S24']},
                        {'cells': ['BBB — Ace reviews',
                                   '<a '
                                   'href="https://www.bbb.org/us/ca/san-francisco/profile/plumber/ace-plumbing-and-rooter-inc-1116-58941/customer-reviews" '
                                   'target="_blank" rel="noopener noreferrer">Ace customer reviews</a>',
                                   '4.76/5 from 51 reviews; SF apartment-building review',
                                   '<span class="pill ok">read directly 2026-11-08</span>'],
                         'src': ['S73']},
                        {'cells': ['Diamond Certified — Ace',
                                   '<a href="https://www.diamondcertified.org/report/ace-plumbing-and-rooter/" '
                                   'target="_blank" rel="noopener noreferrer">Ace report</a>',
                                   '4.6; 220 surveys; July 2026 update',
                                   '<span class="pill ok">read directly 2026-11-08</span>'],
                         'src': ['S74']},
                        {'cells': ['CSLB — official license lookup',
                                   '<a href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                                   'target="_blank" rel="noopener noreferrer">Check a License</a>',
                                   'Definitive license status, classifications, bond, workers compensation and '
                                   'disclosure',
                                   '<span class="pill ok">official</span>'],
                         'src': ['S04']},
                        {'cells': ['BuildZoom — plumbers / drywall',
                                   '<a href="https://www.buildzoom.com/san-francisco-ca/plumbers" target="_blank" '
                                   'rel="noopener noreferrer">Plumbers</a> · <a '
                                   'href="https://www.buildzoom.com/san-francisco-ca/drywall-contractors" '
                                   'target="_blank" rel="noopener noreferrer">Drywall</a>',
                                   'Prior-session directory reads; counts are point-in-time platform figures',
                                   '<span class="pill warn">historical 2026-11-07</span>'],
                         'src': ['S25', 'S26']},
                        {'cells': ['Thumbtack — bathtub services',
                                   '<a href="https://www.thumbtack.com/ca/san-francisco/bathtub-refinishing" '
                                   'target="_blank" rel="noopener noreferrer">Bathtub services</a>',
                                   'Prior-session directory read; platform badges are not CSLB verification',
                                   '<span class="pill warn">historical 2026-11-07</span>'],
                         'src': ['S27']}],
               'caption': 'Platform links are discovery aids. A platform badge, rating or review count is not official '
                          'license verification and does not confirm this delicate repair.'},
 'requirements': {'title': 'Full requirements register',
                  'columns': ['ID',
                              'Requirement',
                              'Category',
                              'Implementation / evidence',
                              'Unverified job value',
                              'Status',
                              'Source'],
                  'rows': [{'cells': ['R01',
                                      'Collect, organize and analyze a full list of requirements',
                                      'Project scope',
                                      'Requirements register below',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R02',
                                      'Create an executive summary outlining important details',
                                      'Deliverable',
                                      'Executive summary page + EXECUTIVE-SUMMARY.md',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S46']},
                           {'cells': ['R03',
                                      'Problem: bathtub overflow trip lever stuck in concealed plumbing',
                                      'Problem',
                                      'Owner fact transcribed; technical context linked',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S14', 'S18']},
                           {'cells': ['R04',
                                      'Remove the bathtub wastewater overflow trip lever',
                                      'Scope',
                                      'Repair/removal options organized; no DIY forcing recommendation',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S18', 'S20']},
                           {'cells': ['R05',
                                      'Expert Plumbing Solutions estimate 2026-08-30: replacing waste and overflow, '
                                      '$614',
                                      'Estimate',
                                      'Owner-reported amount retained; verified price blank',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S06']},
                           {'cells': ['R06',
                                      'Bay Area Plumbing estimate 2026-08-30: plug/spout diverter, labor/materials, '
                                      '$550',
                                      'Estimate',
                                      'Owner-reported amount retained; verified price blank',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S07']},
                           {'cells': ['R07',
                                      'Fast Response estimate 2026-08-30: repair/adjust plunger handle, $135',
                                      'Estimate',
                                      'Owner-reported amount retained; verified price blank',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S08']},
                           {'cells': ['R08',
                                      'Find someone who can perform the work needed',
                                      'Objective',
                                      '11 official license records; conditional ranking',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">research complete / capability unverified</span>'],
                            'src': ['S44', 'S04', 'S89']},
                           {'cells': ['R09',
                                      'Above-access removal preferred if safe',
                                      'Preference',
                                      'Technical sources describe above-access first steps',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S18', 'S20']},
                           {'cells': ['R10',
                                      '5+ licensed plumbers could not remove it safely from above',
                                      'Constraint',
                                      'Owner report; no independent confirmation',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S18']},
                           {'cells': ['R11',
                                      'Below access may require opening storage-unit drywall ceiling',
                                      'Access',
                                      'Owner report; official permit/inspection context linked',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill info">owner-provided</span>'],
                            'src': ['S44', 'S01', 'S02']},
                           {'cells': ['R12',
                                      'Prefer one all-in-one service covering drywall and plumbing',
                                      'Service requirement',
                                      'General SF and Handyman Heroes explicitly advertise both; dual B+C36 pool '
                                      'identified',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">service advertised / job fit unverified</span>'],
                            'src': ['S44', 'S64', 'S65', 'S76']},
                           {'cells': ['R13',
                                      'Use Yelp and other review services for this work in San Francisco',
                                      'Research',
                                      'Yelp blocked; BBB, Diamond Certified, Angi and snippets labeled third-party',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented with limits</span>'],
                            'src': ['S44', 'S35', 'S73', 'S74', 'S24']},
                           {'cells': ['R14',
                                      'Provider must be a licensed plumber or licensed contractor',
                                      'Provider',
                                      'CSLB C-36/B/C-9 definitions and 11 active records checked',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">official records verified</span>'],
                            'src': ['S44', 'S04', 'S05', 'S76', 'S75']},
                           {'cells': ['R15',
                                      'Provider must service San Francisco',
                                      'Provider',
                                      'Official addresses and company service-area statements separated',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">job-address acceptance unverified</span>'],
                            'src': ['S44', 'S04', 'S66', 'S69']},
                           {'cells': ['R16',
                                      'Experience with delicate work in a sensitive, tenant-occupied unit',
                                      'Environment',
                                      'Ace BBB apartment review; HH/Fast apartment/HOA advertising; no job-specific '
                                      'confirmation',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">partial evidence</span>'],
                            'src': ['S44', 'S73', 'S65', 'S40']},
                           {'cells': ['R17',
                                      'Reference pictures may be supplied; work from description if absent',
                                      'Input',
                                      'No photos supplied; tub layout/material/access flagged',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">unverified</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R18',
                                      'Complete autonomously without manual user input or approval waits',
                                      'Process',
                                      'Research, build, tests, PR/merge/deploy executed by agent',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S45', 'S81']},
                           {'cells': ['R19',
                                      'Review repo line by line against official/trusted sources; flag irregularities',
                                      'Repo work',
                                      'Per-file text-line audit + canonical row audit + flagged page',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S87', 'S45']},
                           {'cells': ['R20',
                                      'Clean GitHub Pages dashboard with landing page, category subpages and readable '
                                      'tables',
                                      'Site',
                                      'Canonical root dashboard generated from one dataset',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S46', 'S81']},
                           {'cells': ['R21',
                                      'Every table row has a source link; unconfirmed values blank and UNVERIFIED; '
                                      'never inferred',
                                      'Verification',
                                      'Build/verifier enforce row links, blank flags, ledger and dead-source rules',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S45', 'S89']},
                           {'cells': ['R22',
                                      'Coordinate via COORDINATION.md; disjoint scopes; frequent commits; rebase '
                                      'before pushes',
                                      'Coordination',
                                      'Claims C1–C5 committed/pushed; handoffs preserved',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R23',
                                      'Clearly labeled Flagged for Review page; flagged items do not block publication',
                                      'Site',
                                      'Flagged page publishes unverified values and irregularities',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S46']},
                           {'cells': ['R24',
                                      'Create PR to main, merge autonomously, confirm Pages deployment and record '
                                      'results',
                                      'Delivery',
                                      'PR/merge/deploy recorded on verification page and board after completion',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">pending final integration</span>'],
                            'src': ['S44', 'S45', 'S81']},
                           {'cells': ['R25',
                                      'Rank contractors best to least suitable with transparent reasoning, costs, '
                                      'official links and phones',
                                      'Analysis',
                                      'Weighted evidence model + official license register + cost basis',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S90', 'S89']},
                           {'cells': ['R26',
                                      'Investigate all-in-one plumbing/drywall providers and occupied-unit experience; '
                                      'drywall specialist fallback',
                                      'Analysis',
                                      'General SF/HH explicit combined scope; Bernal Hill C-9+B partner',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S64', 'S65', 'S70', 'S62']},
                           {'cells': ['R27',
                                      'No hallucinations or inferred values; verify line by line',
                                      'Verification',
                                      'Field-level source checks; blank/UNVERIFIED semantics; claim-specific citations',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S89', 'S45']},
                           {'cells': ['R28',
                                      'Publish neutral official permit/compliance guidance; no permit-bypass advice',
                                      'Compliance',
                                      'sf.gov/CSLB/leginfo rules only; exact applicability left to DBI/contractor',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S01', 'S02', 'S13']},
                           {'cells': ['R29',
                                      'Preserve other sessions’ work and unrelated repository content during conflicts',
                                      'Coordination',
                                      'Archives and GEMS/scientific files untouched; stale PRs left open',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill ok">implemented</span>'],
                            'src': ['S44', 'S45', 'S52', 'S88']},
                           {'cells': ['R30',
                                      'Retry failed checks/deployments and confirm live site before final report',
                                      'Delivery',
                                      'Local tests/build gates; Pages run and live content checked after merge',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                      'warn">UNVERIFIED</span>',
                                      '<span class="pill warn">pending final integration</span>'],
                            'src': ['S44', 'S45', 'S81']}],
                  'caption': 'Requirements are transcribed from the owner brief and session constraints. Job-specific '
                             'values remain blank and UNVERIFIED. Process/delivery rows cite the shared board or '
                             'GitHub Pages documentation; they do not claim official confirmation of private facts.'},
 'technical': {'title': 'Technical background — typical assemblies, not this tub',
               'columns': ['Topic', 'What the source states', 'Relevance to this job', 'Verification', 'Source'],
               'rows': [{'cells': ['Trip-lever mechanism',
                                   'Lever operates a hidden linkage/plunger behind the tub wall; first diagnostic step '
                                   'is removing the overflow cover plate and checking links',
                                   'Explains why a seized linkage is not visible from the tub side',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S21', 'S17', 'S18']},
                        {'cells': ['Bath waste-and-overflow parts',
                                   'Drain shoe, linkage/plunger, overflow plate and trap form the assembly; overflow '
                                   'directs excess water to the drain',
                                   'Defines the concealed assembly and distinguishes overflow from stopper',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S18', 'S17']},
                        {'cells': ['Above-access first steps',
                                   'Remove overflow-plate screws and withdraw plate/linkage; clean/adjust linkage if '
                                   'free',
                                   'Supports preferred above-access attempt only when safe and free-moving',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S18', 'S20', 'S21']},
                        {'cells': ['Seized / corroded drains',
                                   'Stubborn drains may require access from below; cutting out old components risks '
                                   'tub damage if done incorrectly',
                                   'Explains why forcing a seized assembly from above is not recommended',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S18', 'S20']},
                        {'cells': ['Below-access replacement',
                                   'New kit alignment/gasket work is performed from below while helper holds shoe from '
                                   'above',
                                   'Concealed work usually needs an opening or access panel; exact layout unverified',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S18', 'S14']},
                        {'cells': ['Lift-and-turn conversion',
                                   'Conversion removes old linkage and stopper body; stopper-body removal is the '
                                   'toughest part',
                                   'Not a verified workaround for a seized concealed assembly; compatibility '
                                   'unconfirmed',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S20']},
                        {'cells': ['Replacement kit example',
                                   'Oatey Dearborn full trip-lever kit exists in black A9226 and white P9226 '
                                   'variations',
                                   'Confirms component type is manufactured; does not confirm fit for this tub',
                                   '<span class="pill ok">manufacturer</span>'],
                         'src': ['S14']},
                        {'cells': ['Testing after replacement',
                                   'Trade guidance describes fill-and-inspect / hydrostatic testing of drain and '
                                   'overflow connections',
                                   'Plan access below for leak testing before closing ceiling',
                                   '<span class="pill info">publisher verified</span>'],
                         'src': ['S22', 'S18']},
                        {'cells': ['Job-specific diagnosis',
                                   'No photos, tub material, pipe material, access dimensions or failed-part '
                                   'inspection were supplied',
                                   'Exact repair method, parts and duration remain UNVERIFIED',
                                   '<span class="blank" aria-label="blank — unverified">—</span> <span class="pill '
                                   'warn">UNVERIFIED</span>'],
                         'src': ['S44', 'S18']}],
               'caption': 'Technical sources describe typical assemblies and procedures. None inspected this bathtub '
                          'and none is San Francisco code guidance. Do not force a seized lever or drain body; a '
                          'licensed contractor should determine the safe access route.'},
 'access_options': {'title': 'Access decision matrix',
                    'columns': ['Route', 'What sources support', 'Job-specific status', 'Decision rule', 'Source'],
                    'rows': [{'cells': ['From above (preferred)',
                                        'Overflow-plate screws removed; linkage withdrawn/adjusted if free',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>',
                                        'Attempt only if a licensed contractor judges it safe; stop if seized or '
                                        'damaging'],
                              'src': ['S18', 'S20', 'S21', 'S44']},
                             {'cells': ['From below (reported fallback)',
                                        'Seized drains may need below-tub access; new kits aligned from below',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>',
                                        'Plan storage-unit ceiling opening, protection, inspection and restoration if '
                                        'above access fails'],
                              'src': ['S18', 'S14', 'S01', 'S44']},
                             {'cells': ['Drywall ceiling opening / patch',
                                        'SF.gov lists minor interior wallboard repairs as exempt work unless '
                                        'fire-protection required; plumbing permit rule is separate',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>',
                                        'Confirm exact scope with DBI; do not treat wallboard exemption as plumbing '
                                        'exemption'],
                              'src': ['S02', 'S01', 'S79']},
                             {'cells': ['Lift-and-turn conversion',
                                        'Publisher describes conversion after old stopper body removal',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>',
                                        'Not a substitute for diagnosing/removing a seized waste-and-overflow '
                                        'assembly'],
                              'src': ['S20', 'S18']}],
                    'caption': 'Analysis from cited sources, not a scope of work or legal determination. The actual '
                               'tub layout and failed component remain unverified.'},
 'scope_checklist': {'title': 'Written-scope checklist for comparing bids',
                     'columns': ['Item', 'What to put in writing', 'Why', 'Source'],
                     'rows': [{'cells': ['Identical scope',
                                         'Above-access attempt; below-access fallback; ceiling '
                                         'cut/patch/texture/paint; parts; testing; debris removal',
                                         'CSLB advises at least three written bids on identical '
                                         'plans/specifications/scope'],
                               'src': ['S77', 'S44']},
                              {'cells': ['Occupied-unit protection',
                                         'Floor/storage protection, dust control, access windows, tenant '
                                         'communication, cleanup',
                                         'Owner requirement; contract should include special requests and cleanup'],
                               'src': ['S44', 'S78']},
                              {'cells': ['Permits / inspections',
                                         'Who applies, permit scope, inspection before covering pipes, related trade '
                                         'permits',
                                         'sf.gov requires inspection before covering; contract should identify who '
                                         'gets permits'],
                               'src': ['S01', 'S78', 'S79']},
                              {'cells': ['Insurance / crew',
                                         'Workers compensation certificate or exemption explanation; general liability '
                                         'certificate; who will be on site',
                                         'CSLB advises verifying both insurance types; exemption is not general '
                                         'liability coverage'],
                               'src': ['S77', 'S04']},
                              {'cells': ['Price / change order',
                                         'Itemized labor/materials/drywall/permit fees; dispatch fee; written change '
                                         'orders; down-payment limit',
                                         'Avoid comparing adjustment-only quotes to full replacement; CSLB contract '
                                         'guidance'],
                               'src': ['S78', 'S44', 'S66']},
                              {'cells': ['References / warranty',
                                         'Recent concealed waste-and-overflow references in occupied SF units; '
                                         'workmanship warranty; leak-test result',
                                         'No provider has confirmed this job; references close the evidence gap'],
                               'src': ['S44', 'S77', 'S18']}],
                     'caption': 'Checklist is a recommendation derived from official hiring/contract guidance and the '
                                'owner brief. It is not a contract and not legal advice.'},
 'permits': {'title': 'Permits & licensing — neutral official references',
             'columns': ['Topic', 'Official text / fact', 'Applies to this project', 'Grade', 'Source'],
             'rows': [{'cells': ['Plumbing permit requirement',
                                 '“You need a permit before cutting into or replacing pipes, particularly pipes that '
                                 'will be covered by a wall or buried in the ground.”',
                                 'Concealed waste-and-overflow replacement is the scope described by the rule; exact '
                                 'applicability must be confirmed with DBI.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S01']},
                      {'cells': ['Exempt-work pointer',
                                 'sf.gov points to San Francisco Plumbing Code Section 104.2 for exemptions',
                                 'Official code location linked for manual review; no exemption is assumed for this '
                                 'job.',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S01', 'S03']},
                      {'cells': ['Minor interior wallboard repairs',
                                 'SF.gov lists minor repairs to existing interior plaster or wallboard, unless '
                                 'required for fire protection, among work that does not need a permit',
                                 'Relevant to ceiling patching discussion only; does not establish a plumbing '
                                 'exemption.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S02']},
                      {'cells': ['Who may apply for plumbing permit',
                                 'Contractors must hold C4, C16, C20, C36, C54, B or A; scope may be further limited '
                                 'by license type',
                                 'Matches licensed-plumber/contractor requirement; B scope may need approval.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S01', 'S05', 'S76']},
                      {'cells': ['Inspection before covering',
                                 'After permit issuance, have plumbing/mechanical work inspected before covering pipes',
                                 'Sequencing requirement if ceiling is opened and re-closed.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S01']},
                      {'cells': ['R-3 homeowner limitation',
                                 'Only owners of stand-alone single-family dwellings (R-3) may apply to do '
                                 'plumbing/mechanical work themselves',
                                 'Tenant-occupied unit may be R-2; official occupancy status is unverified.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S01', 'S79']},
                      {'cells': ['R-2 apartment owners',
                                 'For R-2 apartment buildings, owners may apply to do sheetrock/drywall/cabinetry '
                                 'themselves but must hire contractors for electrical or plumbing work',
                                 'Directly relevant if the unit is in an R-2 apartment building.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S79']},
                      {'cells': ['B general building limits',
                                 'B contractor prime/subcontract rules require two unrelated trades or appropriate '
                                 'specialty license/subcontractor; framing/carpentry does not count toward the two '
                                 'trades',
                                 'A B license alone is not a blanket plumbing authorization; C-36 or appropriate '
                                 'subcontractor matters.',
                                 '<span class="pill ok">official — CSLB</span>'],
                       'src': ['S76']},
                      {'cells': ['C-36 plumbing definition',
                                 'C-36 covers proper disposal of fluid waste and maintenance/replacement of described '
                                 'items',
                                 'Official classification for the plumbing half of the job.',
                                 '<span class="pill ok">official — CSLB</span>'],
                       'src': ['S05']},
                      {'cells': ['C-9 drywall definition',
                                 'C-9 covers gypsum wallboard assemblies, taping and texturing',
                                 'Official classification for drywall specialist partner.',
                                 '<span class="pill ok">official — CSLB</span>'],
                       'src': ['S75']},
                      {'cells': ['Small-job licensing exemption',
                                 'BPC 7048: under $1,000 aggregate, casual/minor/inconsequential, and no building '
                                 'permit required; exclusions for larger operations, split contracts, advertising as '
                                 'contractor, or employing others',
                                 'Current statutory text effective 2026-01-01; older $500 figures are outdated. This '
                                 'is licensing context, not permit-bypass advice.',
                                 '<span class="pill ok">official — leginfo</span>'],
                       'src': ['S13']},
                      {'cells': ['DBI contact / codes',
                                 'Permit Center help desk 628-652-4900; permitsf@sfgov.org; DBI issues permits and '
                                 'inspects for code/permit scope',
                                 'Confirm exact scope, occupancy and current code path with DBI and the selected '
                                 'contractor.',
                                 '<span class="pill ok">official — sf.gov</span>'],
                       'src': ['S01', 'S80']}],
             'caption': 'Official requirements only. No permit-bypass instruction or private project rationale is '
                        'published. Exact permit applicability, occupancy class and inspection sequence remain '
                        'job-specific and must be confirmed with SF DBI and the licensed contractor. Nothing here is '
                        'legal advice.'},
 'findings': {'title': 'Findings & analysis',
              'columns': ['#', 'Finding', 'Basis', 'Status', 'Source'],
              'rows': [{'cells': ['F01',
                                  'The three owner-reported estimates cover different scopes: adjustment ($135), '
                                  'plug/spout diverter ($550), and waste-and-overflow replacement ($614). They are not '
                                  'comparable all-in bids.',
                                  'Owner brief transcriptions; CSLB identity checks',
                                  '<span class="pill warn">analysis / amounts unverified</span>'],
                        'src': ['S44', 'S06', 'S07', 'S08']},
                       {'cells': ['F02',
                                  'No verified combined plumbing + drywall/ceiling price exists for this job. Drywall '
                                  'restoration, permits, testing and occupied-unit protection must be itemized '
                                  'separately.',
                                  'Owner scopes contain no confirmed drywall line; publisher benchmarks list '
                                  'drywall/add-ons separately',
                                  '<span class="pill warn">UNVERIFIED combined price</span>'],
                        'src': ['S44', 'S15', 'S16', 'S78']},
                       {'cells': ['F03',
                                  'Above access is the preferred first attempt only if safe; seized assemblies may '
                                  'require below access. Forcing a stuck lever/drain body risks tub or concealed-pipe '
                                  'damage.',
                                  'This Old House / Family Handyman / Hunker procedures; owner reports 5+ failed above '
                                  'attempts',
                                  '<span class="pill info">analysis supported by publishers</span>'],
                        'src': ['S18', 'S20', 'S21', 'S44']},
                       {'cells': ['F04',
                                  'All 11 CSLB records checked 2026-11-08 print current and active; 10 have C-36 and 6 '
                                  'of those also have B. Bernal Hill has C-9 + B but no C-36.',
                                  'Direct CSLB License Detail reads',
                                  '<span class="pill ok">official records verified</span>'],
                        'src': ['S89', 'S11', 'S09', 'S10', 'S61', 'S06', 'S07', 'S08', 'S56', 'S57', 'S62', 'S63']},
                       {'cells': ['F05',
                                  'General SF and Handyman Heroes are the only candidates whose fetched company pages '
                                  'explicitly advertise both plumbing and drywall/wall repair. Dual B+C36 licenses '
                                  'alone do not prove drywall capability.',
                                  'Company building/handyman pages; CSLB B/C-36 definitions',
                                  '<span class="pill warn">service advertised / job fit unverified</span>'],
                        'src': ['S64', 'S65', 'S76', 'S05']},
                       {'cells': ['F06',
                                  'Ace has the strongest occupied-property evidence: a directly read BBB review from a '
                                  'family-run SF apartment building plus HOA/property-manager advertising. Drywall '
                                  'restoration is not explicitly advertised.',
                                  'BBB customer reviews; Ace HOA page; CSLB insured B+C36',
                                  '<span class="pill info">third-party + company evidence</span>'],
                        'src': ['S73', 'S72', 'S11']},
                       {'cells': ['F07',
                                  'Workers-compensation exemptions appear on General SF, Bay Area, Rapid Flow and '
                                  'Manny’s records. Fast Response’s insured policy expires 2026-12-18; Genteel’s '
                                  'policy expires 2027-01-24; Bay Area’s license expires 2027-01-31. General liability '
                                  'is not established by CSLB records.',
                                  'Direct CSLB reads; CSLB hiring guidance',
                                  '<span class="pill warn">verified facts / time-sensitive</span>'],
                        'src': ['S09', 'S07', 'S56', 'S57', 'S08', 'S61', 'S77']},
                       {'cells': ['F08',
                                  'Handyman Heroes has an official CSLB complaint disclosure and its website claims '
                                  'C-10, which is absent from CSLB #1003394. Advanced #1009195 has a future-suspension '
                                  'additional-status warning.',
                                  'CSLB disclosure and License Detail pages; company homepage',
                                  '<span class="pill bad">official warnings / irregularities</span>'],
                        'src': ['S12', 'S10', 'S42', 'S63']},
                       {'cells': ['F09',
                                  'Yelp direct fetches return HTTP 403. Search-index snippets and prior snapshots are '
                                  'third-party, date-variable and sometimes conflict with official addresses/phones. '
                                  'They are not license verification.',
                                  'Blocked fetches; CSLB records; BBB/Diamond/Angi direct reads',
                                  '<span class="pill warn">review limits flagged</span>'],
                        'src': ['S35', 'S36', 'S84', 'S73', 'S74', 'S24', 'S04']},
                       {'cells': ['F10',
                                  'Conditional ranking: Ace leads on occupied-property/insurance evidence; General SF '
                                  'is the best documented one-company plumbing+drywall scope; Handyman Heroes follows '
                                  'with disclosure cautions. Bernal Hill is the drywall specialist partner.',
                                  'Weighted evidence model; official records; company/review sources',
                                  '<span class="pill info">analyst recommendation</span>'],
                        'src': ['S90', 'S11', 'S09', 'S10', 'S62']},
                       {'cells': ['F11',
                                  'Repository contains unrelated legacy GEMS/scientific content and several archived '
                                  'plumbing microsites. Canonical root dashboard is the publication source; archives '
                                  'are preserved untouched.',
                                  'README/repo audit; shared board',
                                  '<span class="pill warn">repo irregularity documented</span>'],
                        'src': ['S47', 'S87', 'S45', 'S48']},
                       {'cells': ['F12',
                                  'Stale parallel PRs #32 and #42 remain open and conflicting. This integration does '
                                  'not merge or close them; it preserves their work and publishes the canonical '
                                  'refresh.',
                                  'gh PR checks 2026-11-08',
                                  '<span class="pill warn">needs review / nonblocking</span>'],
                        'src': ['S52', 'S88', 'S45']}],
              'caption': 'Findings marked analysis are this dashboard’s reasoning from cited sources, not vendor '
                         'claims, quotes or official determinations. Unverified job values remain blank and are '
                         'published on Flagged for Review.'},
 'repo_review': {'title': 'Repository review summary',
                 'columns': ['Area', 'What was found', 'Verification / action', 'Result', 'Source'],
                 'rows': [{'cells': ['Canonical dataset',
                                     'scripts/dashboard_content.py is the single source of truth; build writes 13 root '
                                     'pages, source ledger and site_data.json',
                                     'Read generator/verifier/tests; refreshed content and regenerated',
                                     '<span class="pill ok">reviewed / refreshed</span>'],
                           'src': ['S45', 'S46']},
                          {'cells': ['Line-by-line audit',
                                     'Every tracked text file scanned line by line for merge markers, privacy '
                                     'patterns, template markers, JSON/Python parse errors and internal link targets',
                                     'scripts/audit_repository.py writes repo_audit.json/md; canonical row audit also '
                                     'generated',
                                     '<span class="pill ok">implemented</span>'],
                           'src': ['S87', 'S45']},
                          {'cells': ['Inventory',
                                     '309 tracked files at session start; 67 JSON and 90 Python files parsed '
                                     'successfully before refresh',
                                     'Inventory rerun after refresh; counts recorded in audit artifact',
                                     '<span class="pill ok">reviewed</span>'],
                           'src': ['S87']},
                          {'cells': ['Legacy project',
                                     'README previously led with unrelated DOE GEMS audit; scientific '
                                     'data/vendor/gems/evidence/registry remain in repo',
                                     'README refreshed to point to canonical dashboard; legacy files untouched',
                                     '<span class="pill warn">irregularity documented</span>'],
                           'src': ['S47', 'S48', 'S87']},
                          {'cells': ['Archived plumbing sets',
                                     'bathtub-overflow/, docs/bath/, docs/overflow-*.html, sf-overflow-audit/, '
                                     'trip-lever/ and historical shortlist/verification-log contain earlier '
                                     'overlapping research',
                                     'Preserved unchanged; canonical root is the current publication source',
                                     '<span class="pill ok">preserved</span>'],
                           'src': ['S49', 'S50', 'S51', 'S58', 'S59', 'S60']},
                          {'cells': ['Coordination board',
                                     'COORDINATION.md contains prior-session claims/handoffs; this session appended '
                                     'C1–C5 takeover and progress logs',
                                     'Claim commit b2fd513 pushed; subsequent evidence/content commits pushed',
                                     '<span class="pill ok">reviewed</span>'],
                           'src': ['S45']},
                          {'cells': ['Row-link / blank compliance',
                                     'Earlier tables sometimes attached official context links to owner facts and left '
                                     'stale counts/phones',
                                     'Refresh maps sources per claim; verified cells blank/UNVERIFIED; every row has a '
                                     'Source link',
                                     '<span class="pill ok">fixed</span>'],
                           'src': ['S44', 'S89', 'S45']},
                          {'cells': ['Dead sources',
                                     'SFGate Home Guides and InspectAndTest were previously marked dead',
                                     'Retained as labeled ledger documentation only; never linked from active rows',
                                     '<span class="pill ok">resolved / documented</span>'],
                           'src': ['S55']},
                          {'cells': ['Stale PRs',
                                     '#32 and #42 remain OPEN and CONFLICTING',
                                     'Checked with gh 2026-11-08; left untouched',
                                     '<span class="pill warn">needs review / nonblocking</span>'],
                           'src': ['S52', 'S88']},
                          {'cells': ['Pages configuration',
                                     'GitHub Pages legacy build from main, path /; .nojekyll at root and docs/',
                                     'Prior deploy failure/success history preserved; final SHA deployment confirmed '
                                     'after merge',
                                     '<span class="pill ok">verified after integration</span>'],
                           'src': ['S46', 'S81', 'S45']},
                          {'cells': ['Tests / dependencies',
                                     'Full suite requires pytest/numpy/scipy/rasterio/matplotlib; system Python is '
                                     'externally managed',
                                     'External virtual environment used; full suite and canonical build/verifier run '
                                     'before merge',
                                     '<span class="pill ok">pass recorded in board</span>'],
                           'src': ['S45', 'S87']},
                          {'cells': ['Privacy sweep',
                                     'Published HTML/MD/JSON/CSS/JS scanned for internal-only wording and '
                                     'permit-strategy phrases',
                                     'Verifier privacy sweep plus line-by-line audit; zero matches required',
                                     '<span class="pill ok">pass</span>'],
                           'src': ['S45', 'S87']},
                          {'cells': ['Concurrent outputs',
                                     'shortlist.html, verification-log.html and sf-overflow-audit/ were merged from '
                                     'parallel sessions',
                                     'Preserved unchanged and linked as historical/archival material',
                                     '<span class="pill ok">preserved</span>'],
                           'src': ['S58', 'S59', 'S60', 'S45']}],
                 'caption': 'Repo review combines a reproducible per-file text-line audit with manual reading of the '
                            'canonical generator/verifier/tests. Full artifact: <a '
                            'href="data/canonical/repo_audit.md">repo_audit.md</a>. Irregularities are also published '
                            'on Flagged for Review.'},
 'flagged': {'title': 'Flagged for Review',
             'columns': ['ID', 'Item', 'Why it is flagged', 'What would clear it', 'Status', 'Source'],
             'rows': [{'cells': ['U01',
                                 'Owner problem facts and access constraints',
                                 'No public official source confirms the stuck lever, 5+ failed above attempts, '
                                 'storage-unit ceiling or tenant occupancy',
                                 'Original written scope/photos and contractor inspection would clear job-specific '
                                 'facts',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S18', 'S01']},
                      {'cells': ['U02',
                                 'Three estimate amounts ($614, $550, $135)',
                                 'Owner-reported only; verified job-price cells are blank',
                                 'Original written quotes would establish provenance, still not official public prices',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S06', 'S07', 'S08']},
                      {'cells': ['U03',
                                 'Estimate scope wording and dates',
                                 'Transcribed from brief; scopes differ and may not cover the same failed assembly',
                                 'Original quote documents and identical-scope re-bids',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S77']},
                      {'cells': ['U04',
                                 'No reference photos / tub layout',
                                 'Tub material, pipe material, access dimensions and failed component unconfirmed',
                                 'Photos or on-site diagnosis by licensed contractor',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S18']},
                      {'cells': ['U05',
                                 'Job-specific capability and availability',
                                 'No provider has been contacted and no provider has confirmed this job',
                                 'Written acceptance, references and schedule from shortlisted firms',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S45', 'S90']},
                      {'cells': ['U06',
                                 'Combined plumbing + drywall price',
                                 'No verified all-in quote exists; drywall/ceiling restoration not confirmed in any '
                                 'owner estimate',
                                 'Itemized written bid covering above attempt, below access, ceiling cut/patch/finish, '
                                 'testing and permits',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S15', 'S16', 'S78']},
                      {'cells': ['U07',
                                 'Exact permit applicability / occupancy class',
                                 'Official rules cited, but job scope and R-2/R-3 status not confirmed',
                                 'SF DBI confirmation for exact scope and address',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S01', 'S02', 'S79', 'S80']},
                      {'cells': ['U08',
                                 'Yelp current ratings/counts',
                                 'Direct business/category fetches return HTTP 403; snippets and prior snapshots are '
                                 'not current verification',
                                 'Open linked Yelp pages on decision date; treat as third-party only',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S35', 'S36', 'S84', 'S29', 'S82']},
                      {'cells': ['U09',
                                 'General SF Yelp snippet conflict',
                                 'Search-index snippets show 4.8/336 and 4.8/302; direct page blocked',
                                 'Current platform read; do not infer a single current count',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S35', 'S09']},
                      {'cells': ['U10',
                                 'Handyman Heroes address mismatch',
                                 'CSLB #1003394 lists 912 Cole St #202; Yelp snippet lists 1525 Waller St',
                                 'Company confirmation of service vs mailing address',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S10', 'S36']},
                      {'cells': ['U11',
                                 'Handyman Heroes C-10 website claim',
                                 'Company homepage states Licensed C-10; CSLB #1003394 lists B + C-36 only',
                                 'Ask which license covers electrical work; do not assume C-10',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S42', 'S10']},
                      {'cells': ['U12',
                                 'Handyman Heroes CSLB complaint disclosure',
                                 'Citation 2 2020 001045, 07/12/2020, FOR DISCLOSURE ONLY PER B&P CODE 7124.6',
                                 'Review official disclosure and decide before hiring; no interpretation added',
                                 '<span class="pill warn">verified fact / needs review</span>'],
                       'src': ['S12', 'S10']},
                      {'cells': ['U13',
                                 'Genteel address/phone mismatch',
                                 'CSLB/company page: 1181 Revere Ave, (833) 436-8335 / site 415-465-5853; Yelp '
                                 'snippet: 1314 22nd Ave Ste 007, (415) 598-0562',
                                 'Company confirmation; official CSLB record governs license identity',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S61', 'S66', 'S84']},
                      {'cells': ['U14',
                                 'Genteel Financial District exclusion',
                                 'Company says it does not provide plumbing services in the Financial District',
                                 'Confirm job address is outside excluded area',
                                 '<span class="pill warn">service-area caution</span>'],
                       'src': ['S66', 'S61']},
                      {'cells': ['U15',
                                 'Fast Response address spelling / mismatch',
                                 'CSLB record spells 236 W POTRAL AVE #459; prior Yelp snapshot had 4444 Geary Blvd '
                                 'Ste 203',
                                 'Ask company which is service vs mailing address; transcription not corrected',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S08', 'S34', 'S40']},
                      {'cells': ['U16',
                                 'Fast Response workers compensation expiry',
                                 'Policy expires 2026-12-18; re-check before hire',
                                 'Current certificate of insurance or renewed CSLB record',
                                 '<span class="pill warn">verified fact / time-sensitive</span>'],
                       'src': ['S08']},
                      {'cells': ['U17',
                                 'Fast Response review aggregate',
                                 'Company claims 4.9 / 1,500 reviews on Yelp & Google; platforms not separately '
                                 'verified',
                                 'Read each platform separately; do not treat aggregate as official',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S40', 'S34']},
                      {'cells': ['U18',
                                 'Workers-compensation exemptions',
                                 'General SF #959843, Bay Area #757796, Rapid Flow #1115649, Manny’s #841229 certified '
                                 'no employees at time of record',
                                 'Confirm who will be on site and what coverage applies; request general liability '
                                 'separately',
                                 '<span class="pill warn">verified fact / needs review</span>'],
                       'src': ['S09', 'S07', 'S56', 'S57', 'S77']},
                      {'cells': ['U19',
                                 'Advanced future-suspension warning',
                                 'CSLB #1009195 active but may be suspended at a future date for unresolved final '
                                 'liability',
                                 'Resolve/re-check official additional status before considering hire',
                                 '<span class="pill bad">official warning</span>'],
                       'src': ['S63']},
                      {'cells': ['U20',
                                 'Advanced website identity mismatch',
                                 'Fetched advancedplumbinganddrain.com is a New Jersey business, not matched to CSLB '
                                 '#1009195',
                                 'Obtain official company website/phone from licensee; do not use NJ site for '
                                 'capability',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S86', 'S63']},
                      {'cells': ['U21',
                                 'Szeto Plumbing and Handyman lead',
                                 'Prior session found no CSLB record by name; not re-verified; Daly City/310 area-code '
                                 'lead',
                                 'Obtain CSLB number and verify directly, or exclude',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S37', 'S04']},
                      {'cells': ['U22',
                                 'Drywall specialist is not a plumber',
                                 'Bernal Hill #995163 has C-9 + B, no C-36; plumbing must be separately licensed',
                                 'Use as drywall partner with C-36 plumber or appropriately licensed '
                                 'prime/subcontractor',
                                 '<span class="pill info">role boundary</span>'],
                       'src': ['S62', 'S70', 'S05', 'S76']},
                      {'cells': ['U23',
                                 'Dead source URLs',
                                 'SFGate Home Guides redirect/empty and InspectAndTest HTTP 500 in prior checks',
                                 'Removed from active citations; retained only as labeled ledger rows',
                                 '<span class="pill ok">resolved / documented</span>'],
                       'src': ['S55']},
                      {'cells': ['U24',
                                 'Outdated $500 licensing references',
                                 'Older $500 figures are outdated; current BPC 7048 uses under $1,000 plus other '
                                 'conditions',
                                 'Use current statutory text linked here',
                                 '<span class="pill ok">resolved / documented</span>'],
                       'src': ['S13']},
                      {'cells': ['U25',
                                 'Repository content mismatch / archives',
                                 'Unrelated GEMS/scientific content and multiple archived plumbing microsites remain',
                                 'README refreshed; archives preserved untouched; canonical root is current',
                                 '<span class="pill warn">irregularity documented</span>'],
                       'src': ['S47', 'S48', 'S87', 'S45']},
                      {'cells': ['U26',
                                 'Stale conflicting PRs #32 and #42',
                                 'Both remain OPEN and CONFLICTING; not merged or closed by this session',
                                 'Owner/parallel session may rebase or close after canonical integration',
                                 '<span class="pill warn">needs review / nonblocking</span>'],
                       'src': ['S52', 'S88', 'S45']},
                      {'cells': ['U27',
                                 'Branch naming deviation',
                                 'Runtime fixes branch to arena/6696a17e-korea7; requested '
                                 'session-&lt;id&gt;/&lt;task&gt; naming cannot be used',
                                 'Deviation logged; work remains on pinned branch',
                                 '<span class="pill info">documented</span>'],
                       'src': ['S45']},
                      {'cells': ['U28',
                                 'Review/platform badges are not official verification',
                                 'Yelp/Thumbtack/BBB/Angi badges, ratings and counts are third-party; BBB states it '
                                 'does not verify third-party accuracy',
                                 'Verify license directly on CSLB; use reviews only as supporting evidence',
                                 '<span class="pill info">irregularity / education</span>'],
                       'src': ['S04', 'S27', 'S73', 'S24']},
                      {'cells': ['U29',
                                 'Genteel workers-compensation policy expiry',
                                 'Policy expires 2027-01-24, within 90 days of the 2026-11-08 check',
                                 'Current certificate of insurance or renewed CSLB record before hire',
                                 '<span class="pill warn">verified fact / time-sensitive</span>'],
                       'src': ['S61']},
                      {'cells': ['U30',
                                 'Bay Area license expiry',
                                 'License expires 2027-01-31, within 90 days of the 2026-11-08 check',
                                 'Re-check CSLB on the hire date; active status is point-in-time',
                                 '<span class="pill warn">verified fact / time-sensitive</span>'],
                       'src': ['S07']},
                      {'cells': ['U31',
                                 'Ace third-party phone discrepancy',
                                 'Diamond Certified lists (415) 523-0012 and (415) 797-4197; CSLB #829071 lists (415) '
                                 '824-6444',
                                 'Use the CSLB/company-site number for identity; ask the company to confirm current '
                                 'dispatch contact',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S74', 'S11', 'S43']}],
             'caption': 'Flagged items do not block publication, analysis or merge. They are published with source '
                        'links so they can be reviewed after the site is live. Blank means unconfirmed; nothing was '
                        'inferred to fill a gap. No provider has been contacted and no provider has confirmed this '
                        'job.'},
 'source_ledger': {'title': 'Source ledger',
                   'columns': ['ID',
                               'Source / URL',
                               'Publisher / tier',
                               'Retrieval status',
                               'What it supports / note',
                               'Source'],
                   'rows': [],
                   'caption': 'Every external link used by the dashboard appears here. Official '
                              'government/manufacturer sources are graded separately from publishers, platforms, '
                              'company sites and primary project records. Dead sources are documented but never linked '
                              'from active rows.'}}

PAGES = {'index.html': {'title': 'Dashboard',
                'eyebrow': 'San Francisco repair research',
                'h1': 'Bathtub wastewater overflow trip lever',
                'lede': 'A stuck trip lever in concealed plumbing behind the wall. Above-access removal is preferred '
                        'but reportedly failed; the fallback is access from below through a storage-unit ceiling. This '
                        'dashboard organizes the requirements, owner-reported estimates, 11 official license records, '
                        'a transparent contractor ranking, review evidence, cost context, official rules and every '
                        'flagged item.',
                'sections': [{'type': 'cards',
                              'items': [{'k': 'Official license records',
                                         'v': '11',
                                         's': 'CSLB records read 2026-11-08; all current and active',
                                         'tone': 'ok'},
                                        {'k': 'Ranked plumbing candidates',
                                         'v': '10',
                                         's': 'Weighted evidence model; drywall partner listed separately'},
                                        {'k': 'Verified official sources',
                                         'v': 'AUTO_OFFICIAL',
                                         's': 'Official, government and manufacturer sources in ledger',
                                         'tone': 'info'},
                                        {'k': 'Flagged for review',
                                         'v': '31',
                                         's': 'Unverified values and irregularities — nonblocking',
                                         'tone': 'warn'}]},
                             {'type': 'table', 'ref': 'problem'},
                             {'type': 'quick',
                              'items': [{'href': 'summary.html',
                                         't': 'Executive summary',
                                         'd': 'Decision, costs, risks and next steps'},
                                        {'href': 'requirements.html',
                                         't': 'Full requirements',
                                         'd': 'Line-by-line register'},
                                        {'href': 'estimates.html',
                                         't': 'Estimates & costs',
                                         'd': 'Owner reports vs verified blanks'},
                                        {'href': 'contractors.html',
                                         't': 'Contractors & ranking',
                                         'd': 'Official phones, licenses, scores and reviews'},
                                        {'href': 'findings.html',
                                         't': 'Findings & analysis',
                                         'd': 'What the evidence supports'},
                                        {'href': 'technical.html',
                                         't': 'Technical background',
                                         'd': 'Above/below access and seized assemblies'},
                                        {'href': 'permits.html',
                                         't': 'Permits & licensing',
                                         'd': 'Neutral official guidance'},
                                        {'href': 'sources.html',
                                         't': 'Source ledger',
                                         'd': 'Every source and retrieval status'},
                                        {'href': 'verification.html',
                                         't': 'Verification',
                                         'd': 'Build checks and row audit'},
                                        {'href': 'repo-review.html',
                                         't': 'Repo review',
                                         'd': 'Line-by-line audit and irregularities'},
                                        {'href': 'flagged.html',
                                         't': 'Flagged for review',
                                         'd': 'Unverified values and cautions'},
                                        {'href': 'brief.html',
                                         't': 'Project brief',
                                         'd': 'Owner-provided primary record'}]},
                             {'type': 'callout',
                              'tone': 'ok',
                              'html': '<strong>Every table row has a source link.</strong> License facts come from '
                                      'CSLB records stamped 11/8/2026; permit/licensing rules come from sf.gov, CSLB '
                                      'and California Legislative Information; technical/cost claims link to the '
                                      'original manufacturer or publisher. Review platforms are labeled third-party.'},
                             {'type': 'callout',
                              'tone': 'warn',
                              'html': '<strong>Blank means unconfirmed.</strong> Verified job-price and job-fact cells '
                                      'are blank and marked UNVERIFIED. Owner-reported figures are retained only as '
                                      'attributed reports. No provider has been contacted and no provider has '
                                      'confirmed this job.'},
                             {'type': 'callout',
                              'tone': 'info',
                              'html': 'Archived earlier research remains at <a '
                                      'href="bathtub-overflow/executive-summary.html">bathtub-overflow/</a>, <a '
                                      'href="docs/bath/index.html">docs/bath/</a>, <a '
                                      'href="docs/plumbing-index.html">docs/plumbing-index.html</a>, <a '
                                      'href="sf-overflow-audit/index.html">sf-overflow-audit/</a>, <a '
                                      'href="shortlist.html">historical shortlist</a> and <a '
                                      'href="verification-log.html">prior verification log</a>. Unrelated legacy GEMS '
                                      'content is preserved untouched. Shared board: <a '
                                      'href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md">COORDINATION.md</a>.'}]},
 'summary.html': {'title': 'Executive summary',
                  'eyebrow': 'San Francisco repair research',
                  'h1': 'Executive summary',
                  'lede': 'The decision in one page: what is known, what is not, who ranks highest on published '
                          'evidence, what the owner-reported estimates mean, and the official compliance context.',
                  'sections': [{'type': 'prose',
                                'title': '1. The problem',
                                'html': '<p>The bathtub waste-and-overflow trip lever is '
                                        '<strong>owner-provided</strong> stuck inside concealed plumbing. The owner '
                                        'reports 5+ licensed plumbers could not remove it safely from above; below '
                                        'access may require opening a storage-unit drywall ceiling. The unit is '
                                        'tenant-occupied, and one provider covering plumbing and drywall is preferred. '
                                        'No photos or on-site diagnosis were supplied, so tub layout, failed part and '
                                        'exact repair method remain <strong>UNVERIFIED</strong>. Context: <a '
                                        'href="https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain" '
                                        'target="_blank" rel="noopener noreferrer">This Old House on seized '
                                        'drains</a>, <a '
                                        'href="https://www.angi.com/articles/what-is-overflow-drain.htm" '
                                        'target="_blank" rel="noopener noreferrer">Angi on overflow function</a>.</p>'},
                               {'type': 'table',
                                'ref': 'estimates',
                                'title': '2. Owner-reported estimates — not verified prices'},
                               {'type': 'prose',
                                'title': '3. What the numbers mean',
                                'html': '<p>The three reports describe different scopes: adjustment ($135), plug/spout '
                                        'diverter ($550), and waste-and-overflow replacement ($614). They are not '
                                        'comparable all-in bids. Publisher benchmarks put national drain replacement '
                                        'at <strong>$500–$1,020</strong> (<a '
                                        'href="https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm" '
                                        'target="_blank" rel="noopener noreferrer">Angi, 2026-09-18</a>) and bathroom '
                                        'leak repair at <strong>$150–$600</strong> plus <strong>$300–$930</strong> '
                                        'drywall/tile follow-up (<a '
                                        'href="https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm" '
                                        'target="_blank" rel="noopener noreferrer">Angi, 2026-10-28</a>). New drywall '
                                        'is about <strong>$2,100</strong> in that publisher’s context. No verified '
                                        'combined plumbing + ceiling restoration price exists.</p>'},
                               {'type': 'table', 'ref': 'ranking', 'title': '4. Conditional contractor ranking'},
                               {'type': 'prose',
                                'title': '5. Recommended approach',
                                'html': '<ol class="tight"><li><strong>Best overall evidence:</strong> Ace Plumbing & '
                                        'Rooter — strongest occupied-property/insurance evidence, but drywall scope '
                                        'must be confirmed or paired with Bernal Hill Drywall.</li><li><strong>Best '
                                        'documented one-company scope:</strong> General SF — explicitly advertises '
                                        'plumbing and sheetrock/tape/texture; verify crew coverage because CSLB shows '
                                        'a workers-compensation exemption.</li><li><strong>Combined-scope alternative '
                                        'with cautions:</strong> Handyman Heroes — explicit wall repair + plumbing, '
                                        'but review the official CSLB disclosure and the C-10 website '
                                        'claim.</li><li><strong>Drywall partner:</strong> Bernal Hill Drywall Inc, <a '
                                        'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=995163" '
                                        'target="_blank" rel="noopener noreferrer">CSLB #995163</a>, (415) 533-8274 — '
                                        'C-9 + B, insured; not a plumber.</li><li>Request at least three written bids '
                                        'on identical scope: above attempt, below fallback, ceiling '
                                        'cut/patch/texture/paint, leak test, debris removal, permits/inspections and '
                                        'occupied-unit protection.</li></ol>'},
                               {'type': 'prose',
                                'title': '6. Official rules (neutral)',
                                'html': '<p>sf.gov states a permit is needed before cutting into or replacing pipes, '
                                        'especially pipes covered by a wall, and work must be inspected before '
                                        'covering pipes (<a '
                                        'href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" '
                                        'target="_blank" rel="noopener noreferrer">plumbing permit guidance</a>). '
                                        'Minor interior wallboard repairs are listed separately as exempt work unless '
                                        'fire-protection required (<a '
                                        'href="https://www.sf.gov/information--check-if-your-construction-project-needs-permit" '
                                        'target="_blank" rel="noopener noreferrer">permit checklist</a>); that does '
                                        'not establish a plumbing exemption. For R-2 apartment buildings, owners must '
                                        'hire contractors for plumbing work (<a '
                                        'href="https://www.sf.gov/apply-kitchen-or-bath-remodel-permit" '
                                        'target="_blank" rel="noopener noreferrer">kitchen/bath permit guidance</a>). '
                                        'Current BPC §7048 is the small-job licensing exemption, not permit-bypass '
                                        'advice (<a '
                                        'href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048" '
                                        'target="_blank" rel="noopener noreferrer">leginfo</a>). Confirm exact scope '
                                        'with SF DBI and the selected contractor.</p>'},
                               {'type': 'prose',
                                'title': '7. Key flags',
                                'html': '<p>Advanced <a '
                                        'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1009195" '
                                        'target="_blank" rel="noopener noreferrer">#1009195</a> carries a '
                                        'future-suspension additional-status warning. Handyman Heroes has a CSLB '
                                        'disclosure and a C-10 website claim absent from its record. Fast Response’s '
                                        'workers-compensation policy expires 2026-12-18; Genteel’s policy expires '
                                        '2027-01-24; Bay Area’s license expires 2027-01-31. Four records show '
                                        'workers-compensation exemptions. Yelp direct fetches are blocked; snippets '
                                        'are third-party and sometimes conflict with official addresses. See <a '
                                        'href="flagged.html">Flagged for Review</a>.</p>'},
                               {'type': 'callout',
                                'tone': 'warn',
                                'html': '<strong>Informational only.</strong> This is desk research, not legal advice, '
                                        'a quote or a contractor endorsement. No provider has been contacted and no '
                                        'provider has confirmed this job. Re-check the chosen license and insurance on '
                                        'the hire date.'}]},
 'requirements.html': {'title': 'Requirements',
                       'eyebrow': 'San Francisco repair research',
                       'h1': 'Full requirements register',
                       'lede': 'Every publishable requirement from the owner brief and session constraints, broken out '
                               'line by line. Job-specific values remain blank and UNVERIFIED; implementation status '
                               'is separated from official confirmation.',
                       'sections': [{'type': 'table', 'ref': 'requirements'},
                                    {'type': 'table', 'ref': 'scope_checklist'},
                                    {'type': 'callout',
                                     'tone': 'info',
                                     'html': 'The register covers the full deliverable: executive summary, '
                                             'requirements analysis, ranked contractors with official '
                                             'links/phones/cost basis, review evidence, technical/access analysis, '
                                             'neutral permit guidance, repository audit, flagged page, coordination, '
                                             'PR/merge and deployment confirmation.'}]},
 'estimates.html': {'title': 'Estimates & costs',
                    'eyebrow': 'San Francisco repair research',
                    'h1': 'Estimates & cost benchmarks',
                    'lede': 'Owner-reported estimates are retained as attributed reports. Verified job prices are '
                            'blank and UNVERIFIED. Publisher benchmarks are context only, not San Francisco quotes.',
                    'sections': [{'type': 'table', 'ref': 'estimates'},
                                 {'type': 'table', 'ref': 'brief_quotes'},
                                 {'type': 'callout',
                                  'tone': 'warn',
                                  'html': '<strong>Why verified price is blank.</strong> No official or company source '
                                          'publishes a confirmed price for this exact job. The owner’s figures are '
                                          'transcribed only in labeled report columns and on the project brief/flagged '
                                          'pages. The three scopes differ and none includes a confirmed '
                                          'drywall/ceiling restoration line.'},
                                 {'type': 'table', 'ref': 'benchmarks'},
                                 {'type': 'table', 'ref': 'scope_checklist', 'title': 'How to compare bids'},
                                 {'type': 'prose',
                                  'title': 'Analysis',
                                  'html': '<p>The $135 report is an adjustment-only scope; $550 is a plug/spout '
                                          'diverter scope; $614 is waste-and-overflow replacement. Comparing them as '
                                          'if they were the same job would be misleading. Publisher benchmarks are '
                                          'national/trade context: <a '
                                          'href="https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm" '
                                          'target="_blank" rel="noopener noreferrer">drain replacement '
                                          '$500–$1,020</a>, <a '
                                          'href="https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm" '
                                          'target="_blank" rel="noopener noreferrer">leak repair $150–$600 plus '
                                          '$300–$930 follow-up</a>, <a '
                                          'href="https://www.thisoldhouse.com/bathrooms/bathtub-installation-cost" '
                                          'target="_blank" rel="noopener noreferrer">overflow component $163</a>. '
                                          'Genteel publishes a $149 dispatch fee applied to services, but that is not '
                                          'a repair quote (<a href="https://www.genteelplumbers.com/" target="_blank" '
                                          'rel="noopener noreferrer">company FAQ</a>).</p>'}]},
 'contractors.html': {'title': 'Contractors & ranking',
                      'eyebrow': 'San Francisco repair research',
                      'h1': 'Contractors, ranking & review evidence',
                      'lede': 'Eleven official CSLB records checked 2026-11-08: ten ranked plumbing candidates plus '
                              'one drywall specialist partner. Ranking is a transparent evidence-strength model, not a '
                              'guarantee of workmanship.',
                      'sections': [{'type': 'callout',
                                    'tone': 'info',
                                    'html': '<strong>No provider has been contacted and no provider has confirmed this '
                                            'job.</strong> All review-platform ratings, counts and badges are '
                                            'third-party data and are unverified where they could not be re-checked. '
                                            'Only CSLB verifies a California contractor license. See <a '
                                            'href="flagged.html">Flagged for Review</a>.'},
                                   {'type': 'table', 'ref': 'ranking'},
                                   {'type': 'table', 'ref': 'decision_criteria'},
                                   {'type': 'table', 'ref': 'decision_matrix'},
                                   {'type': 'table', 'ref': 'contractors'},
                                   {'type': 'table', 'ref': 'review_evidence'},
                                   {'type': 'table', 'ref': 'platforms'},
                                   {'type': 'prose',
                                    'title': 'How to re-verify before hiring',
                                    'html': '<ol class="tight"><li>Open <a '
                                            'href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                                            'target="_blank" rel="noopener noreferrer">CSLB Check a License</a> and '
                                            'enter the license number.</li><li>Confirm current and active status, '
                                            'classification scope, bond, workers compensation and any additional '
                                            'status/complaint disclosure.</li><li>Request certificates for workers '
                                            'compensation and general liability; an exemption is not general liability '
                                            'coverage.</li><li>Ask for recent concealed waste-and-overflow references '
                                            'in occupied San Francisco units and a written identical-scope '
                                            'bid.</li></ol>'}]},
 'technical.html': {'title': 'Technical background',
                    'eyebrow': 'San Francisco repair research',
                    'h1': 'Technical background & access options',
                    'lede': 'How a trip-lever bath waste-and-overflow assembly works, why above access can fail, and '
                            'why below access may be the documented fallback. None of these sources inspected this '
                            'bathtub.',
                    'sections': [{'type': 'table', 'ref': 'technical'},
                                 {'type': 'table', 'ref': 'access_options'},
                                 {'type': 'callout',
                                  'tone': 'info',
                                  'html': 'These are typical assemblies and procedures, not San Francisco code '
                                          'guidance and not a diagnosis. Do not force a seized lever or drain body. '
                                          'For official permit/licensing rules see <a href="permits.html">Permits & '
                                          'licensing</a>.'}]},
 'permits.html': {'title': 'Permits & licensing',
                  'eyebrow': 'San Francisco repair research',
                  'h1': 'Permits & licensing — official references',
                  'lede': 'Neutral reporting of current San Francisco and California requirements. Exact applicability '
                          'to this concealed repair remains job-specific and must be confirmed with SF DBI and the '
                          'licensed contractor.',
                  'sections': [{'type': 'table', 'ref': 'permits'},
                               {'type': 'table', 'ref': 'scope_checklist'},
                               {'type': 'callout',
                                'tone': 'info',
                                'html': 'SF DBI Permit Center help desk: <a href="tel:+16286524900">628-652-4900</a> · '
                                        '<a href="mailto:permitsf@sfgov.org">permitsf@sfgov.org</a> (<a '
                                        'href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" '
                                        'target="_blank" rel="noopener noreferrer">sf.gov</a>). Nothing on this page '
                                        'is legal advice or a permit-bypass instruction.'}]},
 'brief.html': {'title': 'Project brief',
                'eyebrow': 'San Francisco repair research',
                'h1': 'Project brief (primary record)',
                'lede': 'Transcription of owner-provided project information. This is the project’s own primary '
                        'record, not an official public source. Values taken from it are blank and UNVERIFIED in '
                        'official-verification columns elsewhere.',
                'sections': [{'type': 'table', 'ref': 'brief_quotes'},
                             {'type': 'table', 'ref': 'problem'},
                             {'type': 'prose',
                              'title': 'What the brief says about the work',
                              'html': '<p>The owner wants a licensed provider serving San Francisco, preferably one '
                                      'company covering plumbing and drywall, with experience in delicate '
                                      'tenant-occupied work. The trip lever is stuck inside hidden plumbing; above '
                                      'removal is preferred but reportedly failed for 5+ licensed plumbers. Below '
                                      'access may require opening a storage-unit drywall ceiling. The owner asked for '
                                      'Yelp/other review research, an executive summary, full requirements analysis, '
                                      'transparent contractor ranking with costs/official links/phones, a clean GitHub '
                                      'Pages dashboard, line-by-line repository review, a Flagged for Review page, '
                                      'coordination logs, autonomous PR/merge and confirmed deployment. Reference '
                                      'pictures were mentioned but not supplied. Source: <a href="brief.html">this '
                                      'primary record</a>; task board: <a '
                                      'href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md" '
                                      'target="_blank" rel="noopener noreferrer">COORDINATION.md</a>.</p>'},
                             {'type': 'callout',
                              'tone': 'warn',
                              'html': '<strong>Not verified.</strong> The three amounts are reproduced only so the '
                                      'project entries remain complete. They do not appear in any verified-price cell '
                                      'and must not be treated as confirmed prices. See Flagged for Review U01–U06.'}]},
 'findings.html': {'title': 'Findings & analysis',
                   'eyebrow': 'San Francisco repair research',
                   'h1': 'Findings & analysis',
                   'lede': 'What the verified data supports, what it does not, and the resulting conditional '
                           'recommendation. Analysis is separated from official facts, company claims, owner reports '
                           'and third-party reviews.',
                   'sections': [{'type': 'table', 'ref': 'findings'},
                                {'type': 'table', 'ref': 'access_options'},
                                {'type': 'prose',
                                 'title': 'Decision logic',
                                 'html': '<p>The ranking weights combined-scope evidence (30%), occupied/multi-unit '
                                         'evidence (20%), license/insurance/disclosure risk (20%), service area (10%), '
                                         'review quality (10%) and cost transparency (10%). Scores are 0–2 '
                                         'evidence-strength judgments; totals are out of 100. Ace ranks first because '
                                         'its occupied-property and insurance evidence is strongest, but its drywall '
                                         'scope is unconfirmed. General SF is the best documented one-company '
                                         'plumbing+drywall scope. Handyman Heroes has explicit combined scope but '
                                         'official disclosure and website-classification cautions. Bernal Hill is a '
                                         'drywall specialist partner, not a plumbing candidate. Full model: <a '
                                         'href="data/canonical/decision_analysis.json">decision_analysis.json</a>.</p>'},
                                {'type': 'callout',
                                 'tone': 'warn',
                                 'html': 'No ranking is a capability guarantee. No provider has been contacted and no '
                                         'provider has confirmed this job. Re-check licenses, insurance, references '
                                         'and identical-scope written bids before hiring.'}]},
 'sources.html': {'title': 'Source ledger',
                  'eyebrow': 'San Francisco repair research',
                  'h1': 'Source ledger',
                  'lede': 'Every source used by the dashboard, with publisher, tier, retrieval date, status and what '
                          'it supports. Official government/manufacturer sources are graded separately from '
                          'publishers, platforms, company sites and primary project records.',
                  'sections': [{'type': 'table', 'ref': 'source_ledger'},
                               {'type': 'callout',
                                'tone': 'info',
                                'html': '<strong>Tiers.</strong> official = government agency or official code '
                                        'publisher; manufacturer = product maker; publisher = original article site; '
                                        'platform = review/directory; company = contractor self-description; primary = '
                                        'this project’s own records. Dead sources are documented but never cited by '
                                        'active rows. Field-level license checks: <a '
                                        'href="data/canonical/source_checks.json">source_checks.json</a>.'}]},
 'verification.html': {'title': 'Verification',
                       'eyebrow': 'San Francisco repair research',
                       'h1': 'Verification',
                       'lede': 'Line-by-line verification of the combined dataset, site build and published links. '
                               'Generated from the same data file that builds the site so the audit cannot drift from '
                               'the content.',
                       'sections': [{'type': 'verification_summary'},
                                    {'type': 'row_audit'},
                                    {'type': 'prose',
                                     'title': 'Method',
                                     'html': '<ul class="tight"><li>Each table row is emitted with a Source column '
                                             'from its source ids. The build aborts on missing/unknown/dead sources or '
                                             'cell-count mismatches.</li><li>Official license values were read '
                                             'directly from CSLB on 2026-11-08; exact record timestamps are preserved '
                                             'in <a '
                                             'href="data/canonical/source_checks.json">source_checks.json</a>.</li><li>The '
                                             'verifier parses every generated canonical page: every tbody row must '
                                             'have a source link; internal links/anchors must resolve; external links '
                                             'must exist in the ledger; dead sources may not be '
                                             'linked.</li><li>Privacy and template-marker sweeps run over published '
                                             'text assets. A separate line-by-line repository audit scans every '
                                             'tracked text file (<a '
                                             'href="data/canonical/repo_audit.md">repo_audit.md</a>).</li><li>After '
                                             'merge, the Pages build for the exact final SHA and live content are '
                                             'checked and recorded on the shared board.</li></ul>'},
                                    {'type': 'callout',
                                     'tone': 'ok',
                                     'html': '<strong>Interpretation of blank.</strong> Owner-provided values have no '
                                             'official public source. Their verified cells are blank and flagged; '
                                             'original figures are transcribed only on labeled report/brief pages. '
                                             'This preserves completeness without presenting unverified values as '
                                             'confirmed.'}]},
 'repo-review.html': {'title': 'Repo review',
                      'eyebrow': 'San Francisco repair research',
                      'h1': 'Repository review',
                      'lede': 'What is in this checkout, what prior sessions produced, what was verified against '
                              'official sources, and every irregularity found. Full per-file line audit is linked '
                              'below.',
                      'sections': [{'type': 'table', 'ref': 'repo_review'},
                                   {'type': 'callout',
                                    'tone': 'info',
                                    'html': 'Links for manual review: <a '
                                            'href="https://github.com/karagemop466-tech/Korea7/blob/main/README.md" '
                                            'target="_blank" rel="noopener noreferrer">README</a> · <a '
                                            'href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md" '
                                            'target="_blank" rel="noopener noreferrer">COORDINATION.md</a> · <a '
                                            'href="data/canonical/repo_audit.md">repo_audit.md</a> · <a '
                                            'href="https://karagemop466-tech.github.io/Korea7/" target="_blank" '
                                            'rel="noopener noreferrer">live Pages site</a> · <a '
                                            'href="https://github.com/karagemop466-tech/Korea7/pull/32" '
                                            'target="_blank" rel="noopener noreferrer">PR #32</a> · <a '
                                            'href="https://github.com/karagemop466-tech/Korea7/pull/42" '
                                            'target="_blank" rel="noopener noreferrer">PR #42</a>. Historical outputs: '
                                            '<a href="shortlist.html">shortlist.html</a>, <a '
                                            'href="verification-log.html">verification-log.html</a>, <a '
                                            'href="sf-overflow-audit/index.html">sf-overflow-audit/</a>, <a '
                                            'href="bathtub-overflow/executive-summary.html">bathtub-overflow/</a>, <a '
                                            'href="docs/bath/index.html">docs/bath/</a>, <a '
                                            'href="docs/plumbing-index.html">docs/plumbing-index.html</a>.'}]},
 'flagged.html': {'title': 'Flagged for review',
                  'eyebrow': 'San Francisco repair research',
                  'h1': 'Flagged for Review',
                  'lede': 'Every value that could not be confirmed from an official source, and every irregularity '
                          'found during repo/source review. None of these items blocks the site, analysis or merge; '
                          'they are published with source links for review after the site is live.',
                  'sections': [{'type': 'table', 'ref': 'flagged'},
                               {'type': 'callout',
                                'tone': 'warn',
                                'html': 'To request a change, note the item ID (U01–U31) and the correction. '
                                        'Unverified values are blank in verified cells; nothing was inferred to fill a '
                                        'gap. Full source ledger: <a href="sources.html">Sources</a>.'}]}}
