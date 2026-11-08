"""Canonical content for the bathtub-overflow trip-lever research dashboard.

This module is the single source of truth for the integration session
`arena/52d35ede-korea7`. Every fact that appears in a table row cites one or
more source ids from SOURCES. Values that cannot be confirmed from an official
source are left blank and flagged. Nothing here is inferred.

Current ranking sources were re-read on 2026-11-08 (UTC). Historical sources
are labeled and excluded from the current ranking. CSLB records printed
"Data current as of 11/8/2026". Owner/publisher/platform values remain flagged.
"""

META = {'updated': '2026-11-08',
 'session': 'arena/52d35ede-korea7',
 'title': 'Bathtub overflow trip lever — repair research dashboard',
 'pages_url': 'https://karagemop466-tech.github.io/Korea7/',
 'repo_url': 'https://github.com/karagemop466-tech/Korea7'}

NAV = [{'group': 'Overview',
  'links': [('index.html', 'Dashboard'),
            ('summary.html', 'Executive summary'),
            ('requirements.html', 'Requirements')]},
 {'group': 'Decision',
  'links': [('contractors.html', 'Hiring ranking & contacts'),
            ('estimates.html', 'Estimates & costs'),
            ('findings.html', 'Findings & analysis')]},
 {'group': 'Reference',
  'links': [('technical.html', 'Technical background'),
            ('permits.html', 'Permits & licensing'),
            ('brief.html', 'Project brief'),
            ('sources.html', 'Source ledger')]},
 {'group': 'Audit',
  'links': [('verification.html', 'Verification'),
            ('repo-review.html', 'Repo review'),
            ('flagged.html', 'Flagged for review')]}]

# tier: official / manufacturer / publisher / platform / company / primary
# status: verified / blocked-403 / dead / removed
SOURCES = {'S01': {'label': 'SF.gov — Apply for a plumbing and mechanical permit',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/apply-plumbing-and-mechanical-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'A permit is needed before cutting into or replacing pipes, particularly pipes covered '
                     'by a wall; exemptions are in SF Plumbing Code 104.2. After issuance, plumbing work is '
                     'inspected before covering pipes. Permit Center help desk: 628-652-4900; '
                     'permitsf@sfgov.org.',
         'note': 'direct fetch'},
 'S02': {'label': 'SF.gov — Check if your construction project needs a permit',
         'publisher': 'SF Dept. of Building Inspection',
         'url': 'https://www.sf.gov/information--check-if-your-construction-project-needs-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Minor repairs to existing interior plaster or wallboard are listed as not needing a '
                     'permit unless required for fire protection.',
         'note': 'direct fetch'},
 'S03': {'label': 'SF Building/Plumbing Code — Section 104.0 Permits',
         'publisher': 'American Legal Publishing code library (City and County of SF)',
         'url': 'https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830',
         'tier': 'official',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Official code location for §104.2 exempt work referenced by sf.gov',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S04': {'label': 'CSLB — Check a License',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Official lookup by license number, business name or personnel name; CSLB recommends '
                     'reading hiring guidance and complaint disclosure before hiring.',
         'note': 'direct fetch'},
 'S05': {'label': 'CSLB — C-36 Plumbing classification',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'C-36 covers proper disposal of fluid waste and maintenance/replacement of the '
                     'described plumbing items.',
         'note': 'direct fetch'},
 'S06': {'label': 'CSLB License Detail #977638 — Expert Plumbing Solutions',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'EXPERT PLUMBING SOLUTIONS; (415) 531-5340; 1465 44TH AVENUE, SAN FRANCISCO, CA 94122; '
                     "current and active; C36; expires 10/31/2028; $25,000 bond; workers' compensation "
                     'policy 07/19/2026-07/19/2027.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:22 PM'},
 'S07': {'label': 'CSLB License Detail #757796 — Bay Area Plumbing',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'BAY AREA PLUMBING; (415) 668-8000; 335 14TH AVENUE, SAN FRANCISCO, CA 94118; current '
                     "and active; C36; expires 01/31/2027; $25,000 bond; workers' compensation exempt, "
                     'certified no employees at this time.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:52 PM'},
 'S08': {'label': 'CSLB License Detail #1024971 — Fast Response Plumbing and Rooter',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'JOSEPH TINSLEY dba FAST RESPONSE PLUMBING AND ROOTER; (415) 596-6115; 236 W POTRAL AVE '
                     '#459, SAN FRANCISCO, CA 94127; current and active; C36; expires 03/31/2027; $25,000 '
                     "bond; workers' compensation policy 12/18/2025-12/18/2026.",
         'note': 'direct fetch. Data current 11/8/2026 2:55:34 PM'},
 'S09': {'label': 'CSLB License Detail #959843 — GENERALSF',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'GENERALSF; (650) 303-1515; 3624 IRVING STREET STE A, SAN FRANCISCO, CA 94122; current '
                     "and active; B, C10, C36; expires 04/30/2027; $25,000 bond; workers' compensation "
                     'exempt, certified no employees at this time.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:52 PM'},
 'S10': {'label': 'CSLB License Detail #1003394 — Handyman Heroes Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'HANDYMAN HEROES INC; (844) 382-4376; 912 COLE ST # 202, SAN FRANCISCO, CA 94117; '
                     "current and active; B, C36; expires 05/31/2027; $25,000 bond; workers' compensation "
                     'policy 04/25/2026-04/25/2027; complaint-disclosure link present.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:52 PM'},
 'S11': {'label': 'CSLB License Detail #829071 — Ace Plumbing & Rooter',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'ACE PLUMBING & ROOTER; (415) 824-6444; 1090 BRYANT STREET, SAN FRANCISCO, CA '
                     '94103-4417; current and active; C36, A, C-4, C16, B, C10; expires 06/30/2027; $25,000 '
                     "bond; workers' compensation policy 07/13/2026-07/13/2027.",
         'note': 'direct fetch. Data current 11/8/2026 2:55:57 PM'},
 'S12': {'label': 'CSLB Complaint Disclosure #1003394',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'HANDYMAN HEROES INC; citation 2 2020 001045; date 07/12/2020; status FOR DISCLOSURE '
                     'ONLY PER B&P CODE 7124.6.',
         'note': 'direct fetch'},
 'S13': {'label': 'California Business & Professions Code §7048',
         'publisher': 'California Legislative Information (leginfo)',
         'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'BPC 7048: aggregate contract price less than $1,000, casual/minor/inconsequential '
                     'work, and no building permit required; larger-operation and advertising/employee '
                     'limitations apply. Amended by Stats. 2025, Ch. 67, Sec. 12 (AB 1170), effective '
                     'January 1, 2026.',
         'note': 'direct fetch'},
 'S14': {'label': 'Oatey — Dearborn Plastic Tubular Trip-Lever Bath Waste',
         'publisher': 'Oatey (manufacturer)',
         'url': 'https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste',
         'tier': 'manufacturer',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Manufacturer lists Dearborn Plastic Tubular Trip-Lever Bath Waste Full Kit with '
                     'chrome-finish stopper; variants A9226 and P9226.',
         'note': 'direct fetch'},
 'S15': {'label': 'Angi — Cost to Replace a Bathtub or Shower Drain (2026)',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Publisher updated Sep 18, 2026; national bathtub/shower drain replacement range '
                     '$500-$1,020, average $700; labor $45-$200/hour; new drywall about $2,100. Publisher '
                     'data, not an official San Francisco quote.',
         'note': 'direct fetch'},
 'S16': {'label': 'Angi — Bathroom Leak Repair Cost (2026)',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': '$150–$600 leak repair range, $275 average, up to $4,000 complex; drywall/tile '
                     'follow-up $300–$930; call-out $50–$200; labor $45–$200/hr; worn-out tub drain avg $700',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S17': {'label': 'Angi — What Is a Bathtub Overflow Drain?',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/articles/what-is-overflow-drain.htm',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Overflow drain function; concealed channel; traditional vs integral overflow; '
                     'trip-lever/rod diagram',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S18': {'label': 'This Old House — How To Replace a Tub Drain',
         'publisher': 'This Old House',
         'url': 'https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain',
         'tier': 'publisher',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Publisher describes drain shoe, linkage assembly, overflow plate and trap; remove two '
                     'overflow-plate screws; stubborn drains may need access from below; new kit '
                     'gasket/elbow aligned from below. DIY guidance, not a diagnosis of this tub.',
         'note': 'direct fetch'},
 'S19': {'label': 'This Old House — Bathtub Installation Cost (2026)',
         'publisher': 'This Old House',
         'url': 'https://www.thisoldhouse.com/bathrooms/bathtub-installation-cost',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Itemized component table including Overflow $163, Drain $190, Spout $82; total $2,110',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S20': {'label': 'Family Handyman — Replace a bathtub drain stopper',
         'publisher': 'Family Handyman',
         'url': 'https://www.familyhandyman.com/project/how-to-convert-bathtub-drain-lever-to-a-lift-and-turn-drain/',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Removing an old-style trip-lever linkage begins at the overflow plate; lift-and-turn '
                     'conversion',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S21': {'label': 'Hunker — The Trip Lever In My Bathtub Is Stuck',
         'publisher': 'Hunker',
         'url': 'https://www.hunker.com/13417812/the-trip-lever-in-my-bathtub-is-stuck/',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Trip lever is hidden behind the tub wall; diagnosis begins by removing the cover plate '
                     'and checking links',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S22': {'label': 'The Overall Plumber — Bathtub Drain Drama',
         'publisher': 'The Overall Plumber (trade blog, Houston TX)',
         'url': 'https://www.theoverallplumber.com/home-improvement/bathtub-drain-drama-why-you-need-a-licensed-and-insured-plumber-fast/',
         'tier': 'publisher',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Typical repair range $80–$600; most repairs 1–4 hours; repair-vs-replacement decision '
                     'table; hydrostatic/water test of drain assembly',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S23': {'label': 'Angi — Best plumbers in San Francisco, CA',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/companylist/us/ca/san-francisco/plumbing.htm',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'San Francisco plumbing category with verified-review counts; 873 verified plumbing '
                     'reviews; review text about older SF homes',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S24': {'label': 'Angi — Bathtub restoration pros in San Francisco, CA',
         'publisher': 'Angi',
         'url': 'https://www.angi.com/companylist/us/ca/san-francisco/bathtub-refinishing.htm',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'SF bathtub-specific verified reviews, including a small SF property owner describing '
                     'plumbing plus drywall/ceiling work in a tenant-occupied multi-unit building',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S25': {'label': 'BuildZoom — Plumbers in San Francisco, CA',
         'publisher': 'BuildZoom',
         'url': 'https://www.buildzoom.com/san-francisco-ca/plumbers',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'San Francisco plumbing directory with client reviews, verified projects and '
                     'permit/license-derived profiles',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S26': {'label': 'BuildZoom — Drywall and plaster contractors in San Francisco, CA',
         'publisher': 'BuildZoom',
         'url': 'https://www.buildzoom.com/san-francisco-ca/drywall-contractors',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'San Francisco drywall/plaster directory with reviews and project photos',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S27': {'label': 'Thumbtack — Bathtub services near San Francisco, CA',
         'publisher': 'Thumbtack',
         'url': 'https://www.thumbtack.com/ca/san-francisco/bathtub-refinishing',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': "San Francisco bathtub-service listings with customer reviews and 'Licensed pro' badges",
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S28': {'label': 'BBB — Expert Plumbing Solutions business profile',
         'publisher': 'Better Business Bureau',
         'url': 'https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Business profile: not BBB accredited, no BBB rating, no complaints in last 3 years, '
                     'license number 977638 on record, 1465 44th Avenue SF',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S29': {'label': 'Yelp — Bathtub Repair in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Category search for the specific work type in San Francisco',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S30': {'label': 'Yelp — Plumbers in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Category search for licensed plumbers serving San Francisco',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S31': {'label': 'Yelp — Drywall Installation & Repair in San Francisco',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Category search for the drywall half of the combined scope',
         'note': 'Historical prior-session source. Not reverified or used for the current ranking; preserved '
                 'for audit.'},
 'S32': {'label': 'Yelp — Expert Plumbing Solutions',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/expert-plumbing-solutions-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Search excerpt located the business profile and plumbing category. Numeric '
                     'rating/count not used as verified evidence.',
         'note': 'web_search excerpt; direct fetch HTTP 403'},
 'S33': {'label': 'Yelp — Bay Area Plumbing',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/bay-area-plumbing-san-francisco',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Search excerpt includes bathtub/shower drain leak repair and bathtub installation '
                     'captions. Review content is third-party and unverified.',
         'note': 'web_search excerpt; direct fetch HTTP 403'},
 'S34': {'label': 'Yelp — Fast Response Plumbing & Rooter',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Search excerpt located the profile; address shown as 4444 Geary Blvd. Numeric '
                     'rating/count not used as verified evidence.',
         'note': 'web_search excerpt; direct fetch HTTP 403'},
 'S35': {'label': 'Yelp — General SF',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/general-sf-san-francisco-2',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Search excerpts located the profile; one older excerpt describes bead board work and '
                     "replacing a long-leaking drain. Third-party review content, not proof of this job's "
                     'capability.',
         'note': 'web_search excerpt; direct fetch HTTP 403'},
 'S36': {'label': 'Yelp — Handyman Heroes',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/handyman-heroes-san-francisco-5',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': 'Search excerpt located the profile; address shown as 1525 Waller St; categories '
                     'include Handyman, Electricians, Plumbing. Numeric rating/count not used as verified '
                     'evidence.',
         'note': 'web_search excerpt; direct fetch HTTP 403'},
 'S37': {'label': 'Yelp — Szeto Plumbing and Handyman',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/szeto-plumbing-and-handyman-daly-city-2',
         'tier': 'platform',
         'status': 'historical',
         'checked': '2026-11-07',
         'supports': 'Prior session lead only. No matching CSLB record was established in this pass; license '
                     'and phone remain blank/unverified.',
         'note': 'Historical lead from prior session; not reverified and excluded from current ranking.'},
 'S38': {'label': 'Expert Plumbing Solutions — official site',
         'publisher': 'Expert Plumbing Solutions',
         'url': 'https://www.eplumbingsolutions.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists license #977638, phone 415-531-5340, San Francisco residential plumbing, '
                     'drain/clog and fixture services.',
         'note': 'direct fetch'},
 'S39': {'label': 'Bay Area Plumbing — official site',
         'publisher': 'Bay Area Plumbing',
         'url': 'https://www.bayareaplumbingsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists phone (415) 668-8000, San Francisco plumbing, leak detection/pipe '
                     'repair, drain cleaning and bathtub/faucet installation caption.',
         'note': 'direct fetch'},
 'S40': {'label': 'Fast Response Plumbing & Rooter — official site',
         'publisher': 'Fast Response Plumbing & Rooter',
         'url': 'https://www.fastresponseplumbingsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists CSLB #1024971, phone (415) 596-6115, San Francisco residential plumbing '
                     'for houses, apartments and HOAs; aggregate review claim is self-reported.',
         'note': 'direct fetch'},
 'S41': {'label': 'General SF — official site',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists CSLB 959843, phone (650) 303-1515, San Francisco Bay Area electrical, '
                     'plumbing and building services.',
         'note': 'direct fetch'},
 'S42': {'label': 'Handyman Heroes — official site',
         'publisher': 'Handyman Heroes Inc',
         'url': 'https://www.handymanhero.es/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists license #1003394, phone 1-844-382-4376, construction/plumbing/handyman '
                     'services; page also says Licensed C-10, which is not on CSLB #1003394.',
         'note': 'direct fetch'},
 'S43': {'label': 'Ace Plumbing & Rooter — official site',
         'publisher': 'Ace Plumbing & Rooter Inc',
         'url': 'https://www.aceplumbingandrooter.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists license #829071, phone (415) 824-6444, San Francisco '
                     'residential/commercial plumbing and HOA/property-manager services.',
         'note': 'direct fetch'},
 'S44': {'label': 'Project brief (owner-provided primary record)',
         'publisher': "This project's own record, published on this site",
         'url': 'brief.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Owner-provided problem statement, three 2026-08-30 estimates, access constraints, '
                     'service requirements and tenant-occupancy context',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S45': {'label': 'COORDINATION.md — shared task board',
         'publisher': 'This repository',
         'url': 'https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Task claims, handoffs, verification log, irregularities, PR and merge record',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S46': {'label': 'Published GitHub Pages site',
         'publisher': 'GitHub Pages / this repository',
         'url': 'https://karagemop466-tech.github.io/Korea7/',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Live landing page location for this dashboard',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S47': {'label': 'Repository README',
         'publisher': 'This repository',
         'url': 'https://github.com/karagemop466-tech/Korea7/blob/main/README.md',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Legacy GEMS project description and current status, used for the repo-review '
                     'irregularity',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S48': {'label': 'Legacy GEMS site (archived)',
         'publisher': 'This repository',
         'url': 'docs/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Unrelated legacy project pages retained in the repo',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S49': {'label': 'Parallel microsite (archived)',
         'publisher': 'This repository',
         'url': 'bathtub-overflow/executive-summary.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Prior session's overflow pages, retained unpublished-from-nav as archive",
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S50': {'label': 'Parallel microsite (archived)',
         'publisher': 'This repository',
         'url': 'docs/bath/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Prior session's docs/bath pages, retained as archive",
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S51': {'label': 'Parallel dashboard (archived)',
         'publisher': 'This repository',
         'url': 'docs/plumbing-index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Prior session's docs/overflow dashboard, retained as archive",
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S52': {'label': 'Open PR #32 (stale parallel session)',
         'publisher': 'GitHub',
         'url': 'https://github.com/karagemop466-tech/Korea7/pull/32',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Open, conflicting PR from a 2026-11-06 parallel session that also touched index.html',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S53': {'label': 'SFGate Home Guides — trip lever article (DEAD)',
         'publisher': 'SFGate / Weekand',
         'url': 'https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html',
         'tier': 'publisher',
         'status': 'dead',
         'checked': '2026-11-07',
         'supports': 'Removed from all active citations',
         'note': 'Redirects to weekand.com with empty content on 2026-11-07. Not linked from any table row; '
                 'retained here as a labeled documentation row.'},
 'S56': {'label': 'CSLB License Detail #1115649 — Rapid Flow Plumbing & Rooter Inc',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'RAPID FLOW PLUMBING & ROOTER INC; (415) 866-8401; 230 EDINBURGH ST, SAN FRANCISCO, CA '
                     "94112; current and active; B, C36; expires 01/31/2028; $25,000 bond; workers' "
                     'compensation exempt, certified no employees at this time.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:34 PM'},
 'S57': {'label': "CSLB License Detail #841229 — Manny's Plumbing & Rooter",
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "MANNY'S PLUMBING & ROOTER; (650) 207-5733; 41 MIDVALE DRIVE, DALY CITY, CA 94015; "
                     "current and active; C36, B; expires 06/30/2028; $25,000 bond; workers' compensation "
                     'exempt, certified no employees at this time.',
         'note': 'direct fetch. Data current 11/8/2026 2:55:34 PM'},
 'S58': {'label': 'Shortlist — who can do the plumbing and the drywall',
         'publisher': 'This repository (parallel session)',
         'url': 'shortlist.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Ranked shortlist of dual-classified (B + C-36) firms with a vetting script',
         'note': 'Page produced by a concurrent session; license-scope clarification added 2026-11-08.'},
 'S61': {'label': 'Fast Response — plumbing repair and replacement',
         'publisher': 'Fast Response Plumbing & Rooter',
         'url': 'https://www.fastresponseplumbingsf.com/plumbing-repair-replacement',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists Bathtubs (waste & overflow), phone (415) 596-6115, San Francisco '
                     'service, and working alongside a general contractor for remodels. Not proof of drywall '
                     'self-performance or this stuck mechanism.',
         'note': 'direct fetch Company self-description, not proof of this stuck mechanism, drywall '
                 'self-performance, availability or acceptance.'},
 'S60': {'label': 'SF overflow audit — parallel session dashboard',
         'publisher': 'This repository (parallel session)',
         'url': 'sf-overflow-audit/index.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Independent 9-page audit dashboard with 11 CSLB records, Watco/Oatey technical notes '
                     'and 15 flagged items',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S59': {'label': 'Verification log — earlier session',
         'publisher': 'This repository (parallel session)',
         'url': 'verification-log.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': "Earlier session's line-by-line verification and correction log",
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S55': {'label': 'Source ledger (this site)',
         'publisher': 'This dashboard',
         'url': 'sources.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Documentation rows about sources removed from active citations',
         'note': 'Local/repository artifact existence checked in this pass; not independent verification of '
                 'external facts.'},
 'S54': {'label': 'InspectAndTest — bathtub overflow guide (DEAD)',
         'publisher': 'InspectAndTest',
         'url': 'https://inspectandtest.net/guides/bathtub-overflow-drain/',
         'tier': 'publisher',
         'status': 'dead',
         'checked': '2026-11-07',
         'supports': 'Removed from all active citations',
         'note': 'HTTP 500 on 2026-11-07. Not linked from any table row; retained here as a labeled '
                 'documentation row.'},
 'S64': {'label': 'Handyman Heroes — Handyman services',
         'publisher': 'Handyman Heroes Inc',
         'url': 'https://www.handymanhero.es/handyman-services/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists sheetrock and wall repairs, plumbing and electrical services, San '
                     'Francisco homes and apartments; phone 1-844-382-4376; license #1003394.',
         'note': 'direct fetch'},
 'S65': {'label': 'Rapid Flow Plumbing & Rooter — home',
         'publisher': 'Rapid Flow Plumbing & Rooter Inc',
         'url': 'https://www.rapidflowbayarea.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists B and C-36 license #1115649, plumbing and general contracting/remodels, '
                     'San Francisco Bay Area service; marketing phone 844-BAY-FLOW.',
         'note': 'direct fetch'},
 'S66': {'label': 'Rapid Flow Plumbing & Rooter — contact',
         'publisher': 'Rapid Flow Plumbing & Rooter Inc',
         'url': 'https://www.rapidflowbayarea.com/contact',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company contact page lists 230 Edinburgh St, San Francisco; SF Bay Area service; '
                     'license #1115649; phone/text (415) 866-8401 and marketing line 844-BAY-FLOW.',
         'note': 'direct fetch'},
 'S67': {'label': "Manny's Plumbing & Rooters — home",
         'publisher': "Manny's Plumbing & Rooters",
         'url': 'https://www.mannysplumbingandremodeling.com/',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists license #841229, C-36/B, tub installation, drain replacement, '
                     'kitchen/bathroom remodeling; named service list includes Daly City and San Mateo '
                     'County cities plus surrounding San Mateo & San Francisco Counties. Exact SF address '
                     'availability unconfirmed.',
         'note': 'direct fetch'},
 'S68': {'label': 'CSLB — B General Building classification',
         'publisher': 'Contractors State License Board',
         'url': 'https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'B General Building definition and BPC 7057 limits: non-framing/carpentry trades '
                     'require appropriate classification or appropriately licensed subcontractor, subject to '
                     'the stated multi-trade rules.',
         'note': 'direct fetch'},
 'S69': {'label': 'CSLB — How to find the right licensed contractor',
         'publisher': 'Contractors State License Board',
         'url': 'https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'CSLB advises at least three written bids on identical scope, checking '
                     "license/personnel, address/phone, workers' compensation and general liability "
                     'insurance; bond is not a competency guarantee.',
         'note': 'direct fetch'},
 'S70': {'label': 'California Civil Code §1954 — landlord entry',
         'publisher': 'California Legislative Information',
         'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Civil Code 1954 limits landlord entry, generally requires reasonable written notice '
                     'with date/approximate time/purpose and normal business hours; 24 hours is presumed '
                     'reasonable absent contrary evidence; exceptions include emergency, consent at entry '
                     'and agreed repair entry within one week.',
         'note': 'direct fetch'},
 'S71': {'label': 'Watco — Trip Lever Installation Instructions (PDF)',
         'publisher': 'Watco Manufacturing Co.',
         'url': 'https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf',
         'tier': 'manufacturer',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Watco trip-lever instructions: drain elbow/gasket secured under tub; overflow elbow '
                     'aligned behind tub; overflow plate and drop cylinder installed with screws; linkage '
                     'must not be kinked; readjust to ensure drain stops water. Model-specific instructions, '
                     'not identification of this tub.',
         'note': 'direct fetch'},
 'S72': {'label': 'SF.gov — Apply for a kitchen or bath remodel permit',
         'publisher': 'SF Department of Building Inspection',
         'url': 'https://www.sf.gov/apply-kitchen-or-bath-remodel-permit',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'SF DBI kitchen/bath permit guidance for in-kind fixture renovation with no structural '
                     'work; online route limited to no wall removal/moving and R-2/R-3 legally permitted '
                     'kitchens/baths; related plumbing/electrical permits and inspections are separate.',
         'note': 'direct fetch'},
 'S73': {'label': 'Yelp — Ace Plumbing & Rooter profile',
         'publisher': 'Yelp',
         'url': 'https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco?start=160',
         'tier': 'platform',
         'status': 'blocked-403',
         'checked': '2026-11-08',
         'supports': "Search excerpt located Ace Plumbing & Rooter's Yelp profile and plumbing categories. "
                     'Numeric rating/count not used as verified evidence.',
         'note': 'web_search excerpt; direct Yelp fetch HTTP 403'},
 'S74': {'label': '2025 San Francisco Plumbing Code PDF — §104.2',
         'publisher': 'City and County of San Francisco',
         'url': 'https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'SF Plumbing Code 104.2 exempt work includes repair of leaks not requiring cutting into '
                     'or removing piping, and unstopping traps/sewers/vents/waste pipes not requiring '
                     'cutting into or removal of traps or piping.',
         'note': 'direct fetch, chunk 1, printed pages 4-5'},
 'S75': {'label': 'Prior canonical research snapshot (2026-11-07/08)',
         'publisher': 'This repository',
         'url': 'data/canonical/research-history-2026-11-07.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Preserved prior tables/sources before this refresh',
         'note': 'Historical data retained; not current verification.'},
 'S76': {'label': 'Repository source/artifact inventory',
         'publisher': 'This repository',
         'url': 'data/canonical/repo_inventory.json',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'File paths, byte counts, SHA-256 hashes and review category',
         'note': 'Generated pages/reports excluded to avoid self-reference; external factual claims in '
                 'unrelated files not verified.'},
 'S77': {'label': 'General SF — Building services',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/building',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists Rough and Finish Plumbing; Sheetrock/Tape and Texture; phone '
                     '(650)-303-1515; CSLB 959843.',
         'note': 'direct fetch'},
 'S78': {'label': 'General SF — Plumbing services',
         'publisher': 'General SF',
         'url': 'https://generalsf.com/plumbing',
         'tier': 'company',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Company lists plumbing installation/repair, sewer/water lines, '
                     'faucet/toilet/tub/shower replacement; phone (650)-303-1515; CSLB 959843.',
         'note': 'direct fetch'},
 'S62': {'label': 'California BPC §7059 — specialty contractor incidental work',
         'publisher': 'California Legislative Information',
         'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7059.&lawCode=BPC',
         'tier': 'official',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Specialty contractors may undertake other trades when incidental and supplemental to '
                     'their licensed work',
         'note': 'Directly read 2026-11-08; applicability to this particular ceiling repair is not '
                 'established.'},
 'S63': {'label': 'Archived overflow verification page',
         'publisher': 'This repository (parallel session)',
         'url': 'docs/overflow-verification.html',
         'tier': 'primary',
         'status': 'verified',
         'checked': '2026-11-08',
         'supports': 'Historical page containing overly categorical licensing statements; see U22',
         'note': 'Historical claims should not be treated as current legal advice.'}}


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

TABLES = {'problem': {'title': 'Problem snapshot — owner-provided, not independently verified',
             'columns': ['Item', 'Detail as provided', 'Official verification', 'Provenance', 'Source'],
             'rows': [{'cells': ['Failed component',
                                 'Bathtub wastewater overflow trip lever stuck in concealed plumbing behind '
                                 'the wall',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S14', 'S71']},
                      {'cells': ['Access constraint',
                                 'Hard-to-reach area; drywall may need to be opened to reach plumbing',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S02']},
                      {'cells': ['Preferred route',
                                 'Remove from above if it can be done safely',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S71']},
                      {'cells': ['Reported prior attempts',
                                 'More than five licensed plumbers could not remove it from above without '
                                 'concern over damaging hidden plumbing',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S04']},
                      {'cells': ['Reported fallback',
                                 'Work from below; storage unit underneath may require opening the drywall '
                                 'ceiling',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S02', 'S74']},
                      {'cells': ['Service requirement',
                                 'One provider for plumbing and drywall; delicate work in a tenant-occupied '
                                 'San Francisco unit',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S68', 'S70']},
                      {'cells': ['Reference photos',
                                 'Mentioned as possible; none supplied to this session',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>',
                                 '<span class="pill info">owner-provided</span>'],
                       'src': ['S44', 'S45']}],
             'caption': 'Owner statements are transcribed from the project brief. Context links describe '
                        'components/rules; they do not confirm the owner’s facts.'},
 'estimates': {'title': 'Estimates received — 2026-08-30',
               'columns': ['#',
                           'Company / identity',
                           'Scope as owner-reported',
                           'Verified amount',
                           'Official quote date',
                           'Verification',
                           'License status',
                           'Source'],
               'rows': [{'cells': ['1',
                                   '<strong>Expert Plumbing Solutions</strong><br><a '
                                   'href="https://www.eplumbingsolutions.com/" target="_blank" rel="noopener '
                                   'noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #977638</a>',
                                   'Remove bathtub wastewater overflow trip lever — “replacing waste and '
                                   'overflow”',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                   'official source exists</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S06', 'S38']},
                        {'cells': ['2',
                                   '<strong>Bay Area Plumbing</strong><br><a '
                                   'href="https://www.bayareaplumbingsf.com/" target="_blank" rel="noopener '
                                   'noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #757796</a>',
                                   'Replace lever for the bathtub plug and spout with diverter; includes '
                                   'labor and materials',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                   'official source exists</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S07', 'S39']},
                        {'cells': ['3',
                                   '<strong>Fast Response Plumbing &amp; Rooter</strong><br><a '
                                   'href="https://www.fastresponseplumbingsf.com/" target="_blank" '
                                   'rel="noopener noreferrer">official site</a> · <a '
                                   'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                   'target="_blank" rel="noopener noreferrer">CSLB #1024971</a>',
                                   'Repair or adjust bathtub wastewater plunger handle',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="blank" aria-label="blank — unverified">—</span>',
                                   '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — no '
                                   'official source exists</small>',
                                   '<span class="pill ok">C-36 active</span>'],
                         'src': ['S44', 'S08', 'S40']}],
               'caption': 'Verified amount and official quote-date cells are blank because no official '
                          'source publishes these private estimates. Owner-reported figures are retained '
                          'only in the labeled transcription below. License identity is independently '
                          'checked; scope, price and drywall inclusion remain unverified.'},
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
                                      'Remove bathtub wastewater overflow trip lever; replacing waste and '
                                      'overflow',
                                      '$614',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — '
                                      'no official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S06']},
                           {'cells': ['2',
                                      'Bay Area Plumbing',
                                      'Replace lever for the bathtub plug and spout with diverter, includes '
                                      'labor and materials',
                                      '$550',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — '
                                      'no official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S07']},
                           {'cells': ['3',
                                      'Fast Response',
                                      'Repair or adjust bath tub wastewater plunger handle',
                                      '$135',
                                      '2026-08-30',
                                      '<span class="pill warn">UNVERIFIED</span><br><small>owner-provided — '
                                      'no official source exists</small>',
                                      '<span class="pill mute">primary record only</span>'],
                            'src': ['S44', 'S08']}],
                  'caption': 'Transcription of the owner’s brief only. These are not verified prices, not '
                             'current acceptances, and not combined plumbing + drywall quotes.'},
 'benchmarks': {'title': 'Cost context — publisher data, NOT official San Francisco quotes',
                'columns': ['Benchmark',
                            'Publisher value (UNVERIFIED)',
                            'Official SF job quote',
                            'Publisher date',
                            'Limitation',
                            'Source'],
                'rows': [{'cells': ['Bathtub/shower drain replacement',
                                    '$500–$1,020; average $700 <span class="pill warn">UNVERIFIED</span>',
                                    '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                    'class="pill warn">UNVERIFIED</span>',
                                    '2026-09-18',
                                    'National publisher data; not this concealed-access job'],
                          'src': ['S15']},
                         {'cells': ['Plumber labor for drain replacement',
                                    '$45–$200/hour <span class="pill warn">UNVERIFIED</span>',
                                    '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                    'class="pill warn">UNVERIFIED</span>',
                                    '2026-09-18',
                                    'National publisher data; not a local bid'],
                          'src': ['S15']},
                         {'cells': ['New drywall installation if wall opened',
                                    'About $2,100 <span class="pill warn">UNVERIFIED</span>',
                                    '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                    'class="pill warn">UNVERIFIED</span>',
                                    '2026-09-18',
                                    'Publisher add-on context; ceiling patch/finish scope unknown'],
                          'src': ['S15']}],
                'caption': 'Publisher figures are explicitly unverified as official/project values. They are '
                           'not used to rank contractors or infer a total.'},
 'contractors': {'title': 'License records — checked directly on CSLB 2026-11-08',
                 'columns': ['Company',
                             'CSLB license',
                             'Classifications',
                             'Status / expiry',
                             'Workers’ compensation / bond',
                             'Address on record',
                             'Verification',
                             'Source'],
                 'rows': [{'cells': ['<strong>General SF</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843" '
                                     'target="_blank" rel="noopener noreferrer">#959843</a>',
                                     'B · C-10 · C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-04-30',
                                     'Exempt — certified no employees at this time<br><small>Bond '
                                     '$25,000</small>',
                                     '3624 Irving Street Ste A, San Francisco, CA 94122',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S09']},
                          {'cells': ['<strong>Handyman Heroes Inc</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394" '
                                     'target="_blank" rel="noopener noreferrer">#1003394</a>',
                                     'B · C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-05-31',
                                     'Policy on CSLB record<br><small>2026-04-25 to '
                                     '2027-04-25</small><br><small>Bond $25,000</small>',
                                     '912 Cole St # 202, San Francisco, CA 94117',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S10']},
                          {'cells': ['<strong>Ace Plumbing &amp; Rooter Inc</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071" '
                                     'target="_blank" rel="noopener noreferrer">#829071</a>',
                                     'A · B · C-4 · C-10 · C-16 · C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-06-30',
                                     'Policy on CSLB record<br><small>2026-07-13 to '
                                     '2027-07-13</small><br><small>Bond $25,000</small>',
                                     '1090 Bryant Street, San Francisco, CA 94103-4417',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S11']},
                          {'cells': ['<strong>Rapid Flow Plumbing &amp; Rooter Inc</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649" '
                                     'target="_blank" rel="noopener noreferrer">#1115649</a>',
                                     'B · C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2028-01-31',
                                     'Exempt — certified no employees at this time<br><small>Bond '
                                     '$25,000</small>',
                                     '230 Edinburgh St, San Francisco, CA 94112',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S56']},
                          {'cells': ['<strong>Manny&#x27;s Plumbing &amp; Rooter</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229" '
                                     'target="_blank" rel="noopener noreferrer">#841229</a>',
                                     'C-36 · B',
                                     '<span class="pill ok">current and active</span><br>expires 2028-06-30',
                                     'Exempt — certified no employees at this time<br><small>Bond '
                                     '$25,000</small>',
                                     '41 Midvale Drive, Daly City, CA 94015',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S57']},
                          {'cells': ['<strong>Expert Plumbing Solutions</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                     'target="_blank" rel="noopener noreferrer">#977638</a>',
                                     'C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2028-10-31',
                                     'Policy on CSLB record<br><small>2026-07-19 to '
                                     '2027-07-19</small><br><small>Bond $25,000</small>',
                                     '1465 44th Avenue, San Francisco, CA 94122',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S06']},
                          {'cells': ['<strong>Fast Response Plumbing &amp; Rooter</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                     'target="_blank" rel="noopener noreferrer">#1024971</a>',
                                     'C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-03-31',
                                     'Policy on CSLB record<br><small>2025-12-18 to '
                                     '2026-12-18</small><br><small>Bond $25,000</small>',
                                     '236 W POTRAL AVE #459, San Francisco, CA 94127',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S08']},
                          {'cells': ['<strong>Bay Area Plumbing</strong>',
                                     '<a '
                                     'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                     'target="_blank" rel="noopener noreferrer">#757796</a>',
                                     'C-36',
                                     '<span class="pill ok">current and active</span><br>expires 2027-01-31',
                                     'Exempt — certified no employees at this time<br><small>Bond '
                                     '$25,000</small>',
                                     '335 14th Avenue, San Francisco, CA 94118',
                                     '<span class="pill ok">CSLB checked 2026-11-08</span>'],
                           'src': ['S07']}],
                 'caption': 'Active license status does not prove experience with this seized mechanism, '
                            'drywall capability, availability, insurance adequacy for the actual crew, or '
                            'acceptance of this job.'},
 'review_snapshots': {'title': 'Review evidence — Yelp located, numeric values unverified',
                      'columns': ['Company',
                                  'Yelp profile',
                                  'What was checked',
                                  'Rating / count',
                                  'Official license source',
                                  'Status',
                                  'Source'],
                      'rows': [{'cells': ['<strong>General SF</strong>',
                                          '<a href="https://www.yelp.com/biz/general-sf-san-francisco-2" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Older search excerpt mentions bead board and replacing a '
                                          'long-leaking drain; third-party, unverified. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #959843</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S09', 'S35']},
                               {'cells': ['<strong>Handyman Heroes Inc</strong>',
                                          '<a '
                                          'href="https://www.yelp.com/biz/handyman-heroes-san-francisco-5" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #1003394</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S10', 'S36']},
                               {'cells': ['<strong>Ace Plumbing &amp; Rooter Inc</strong>',
                                          '<a '
                                          'href="https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco?start=160" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #829071</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S11', 'S73']},
                               {'cells': ['<strong>Rapid Flow Plumbing &amp; Rooter Inc</strong>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #1115649</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S56', 'S65', 'S66']},
                               {'cells': ['<strong>Manny&#x27;s Plumbing &amp; Rooter</strong>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #841229</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S57', 'S67']},
                               {'cells': ['<strong>Expert Plumbing Solutions</strong>',
                                          '<a '
                                          'href="https://www.yelp.com/biz/expert-plumbing-solutions-san-francisco" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #977638</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S06', 'S32']},
                               {'cells': ['<strong>Fast Response Plumbing &amp; Rooter</strong>',
                                          '<a '
                                          'href="https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Profile located through search; direct page blocked. Numeric '
                                          'rating/count left blank. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #1024971</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S08', 'S34']},
                               {'cells': ['<strong>Bay Area Plumbing</strong>',
                                          '<a '
                                          'href="https://www.yelp.com/biz/bay-area-plumbing-san-francisco" '
                                          'target="_blank" rel="noopener noreferrer">Yelp profile</a>',
                                          'Search excerpt includes bathtub/shower drain leak repair '
                                          'captions; third-party, unverified. <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<a '
                                          'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                          'target="_blank" rel="noopener noreferrer">CSLB #757796</a>',
                                          '<span class="pill warn">platform evidence only</span>'],
                                'src': ['S07', 'S33']},
                               {'cells': ['Szeto Plumbing and Handyman <span class="pill '
                                          'warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          'Historical lead; no matching CSLB record established in this pass',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<span class="blank" aria-label="blank — unverified">—</span> '
                                          '<span class="pill warn">UNVERIFIED</span>',
                                          '<span class="pill warn">excluded from ranking</span>'],
                                'src': ['S04', 'S37']}],
                      'caption': 'Direct Yelp fetches returned HTTP 403. Search excerpts are third-party '
                                 'discovery evidence only; ratings/counts are deliberately blank and '
                                 'flagged. Company testimonials are self-published, not independent '
                                 'verification.'},
 'platforms': {'title': 'Review and license discovery links',
               'columns': ['Platform', 'Link', 'Use / limit', 'Status', 'Source'],
               'rows': [{'cells': ['Yelp — bathtub repair',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">SF bathtub repair search</a>',
                                   'Category discovery; direct fetch blocked',
                                   '<span class="pill warn">historical / unverified</span>'],
                         'src': ['S29']},
                        {'cells': ['Yelp — plumbers',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">SF plumbers search</a>',
                                   'Category discovery; direct fetch blocked',
                                   '<span class="pill warn">historical / unverified</span>'],
                         'src': ['S30']},
                        {'cells': ['Yelp — drywall',
                                   '<a '
                                   'href="https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA" '
                                   'target="_blank" rel="noopener noreferrer">SF drywall search</a>',
                                   'Drywall half of scope; direct fetch blocked',
                                   '<span class="pill warn">historical / unverified</span>'],
                         'src': ['S31']},
                        {'cells': ['Angi / BuildZoom / Thumbtack / BBB',
                                   '<a '
                                   'href="https://www.angi.com/companylist/us/ca/san-francisco/plumbing.htm" '
                                   'target="_blank" rel="noopener noreferrer">Angi</a> · <a '
                                   'href="https://www.buildzoom.com/san-francisco-ca/plumbers" '
                                   'target="_blank" rel="noopener noreferrer">BuildZoom</a> · <a '
                                   'href="https://www.thumbtack.com/ca/san-francisco/bathtub-refinishing" '
                                   'target="_blank" rel="noopener noreferrer">Thumbtack</a> · <a '
                                   'href="https://www.bbb.org/us/ca/san-francisco/profile/plumber/expert-plumbing-solutions-1116-458492" '
                                   'target="_blank" rel="noopener noreferrer">BBB</a>',
                                   'Prior-session discovery links; not reverified or used for current '
                                   'ranking',
                                   '<span class="pill warn">historical / unverified</span>'],
                         'src': ['S23', 'S25', 'S27', 'S28']},
                        {'cells': ['CSLB — official license lookup',
                                   '<a '
                                   'href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                                   'target="_blank" rel="noopener noreferrer">Check a License</a>',
                                   'Authoritative license status, classifications, bond, workers’ '
                                   'compensation and disclosure',
                                   '<span class="pill ok">official</span>'],
                         'src': ['S04']}],
               'caption': 'Platform badges are not CSLB verification. Current contractor rows cite official '
                          'CSLB and company sources; review numerics remain blank/unverified.'},
 'requirements': {'title': 'Requirements register — line by line',
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
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S02']},
                           {'cells': ['R04',
                                      'Remove the bathtub wastewater overflow trip lever',
                                      'Scope',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S14', 'S71']},
                           {'cells': ['R05',
                                      'Expert Plumbing Solutions: replacing waste and overflow; '
                                      'owner-reported $614',
                                      'Estimate',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S06']},
                           {'cells': ['R06',
                                      'Bay Area Plumbing: lever/plug/spout with diverter, labor/materials; '
                                      'owner-reported $550',
                                      'Estimate',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S07']},
                           {'cells': ['R07',
                                      'Fast Response: repair/adjust plunger handle; owner-reported $135',
                                      'Estimate',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S08']},
                           {'cells': ['R08',
                                      'Estimates dated 8/30/26',
                                      'Estimate date',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44']},
                           {'cells': ['R09',
                                      'Find someone who can perform the needed work',
                                      'Objective',
                                      'Eight licensed candidates researched; no provider acceptance '
                                      'confirmed',
                                      '<span class="pill warn">research done / acceptance unverified</span>'],
                            'src': ['S44', 'S04']},
                           {'cells': ['R10',
                                      'Removal from above is preferred if possible',
                                      'Preference',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S71']},
                           {'cells': ['R11',
                                      '5+ licensed plumbers could not remove it from above without damage '
                                      'concern',
                                      'Constraint',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S04']},
                           {'cells': ['R12',
                                      'Work from below; storage unit below; ceiling drywall may need opening',
                                      'Access',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S02', 'S74']},
                           {'cells': ['R13',
                                      'One all-in-one service for drywall and plumbing',
                                      'Service requirement',
                                      'Five B+C-36 licenses verified; combined execution and drywall scope '
                                      'unconfirmed',
                                      '<span class="pill warn">license verified / execution '
                                      'unverified</span>'],
                            'src': ['S44', 'S09', 'S10', 'S11', 'S56', 'S57', 'S68']},
                           {'cells': ['R14',
                                      'Look on Yelp and other review services for this specific work in San '
                                      'Francisco',
                                      'Research',
                                      'Yelp profiles/searches located; direct fetch blocked; numeric values '
                                      'blank',
                                      '<span class="pill warn">research done / reviews unverified</span>'],
                            'src': ['S44', 'S32', 'S33', 'S34', 'S35', 'S36', 'S73']},
                           {'cells': ['R15',
                                      'Provider should be a licensed plumber or contractor',
                                      'Provider',
                                      'CSLB records checked for eight candidates',
                                      '<span class="pill ok">license records verified</span>'],
                            'src': ['S44', 'S04', 'S05']},
                           {'cells': ['R16',
                                      'Provider must service the San Francisco area',
                                      'Service area',
                                      'Company service claims and CSLB addresses recorded; exact address '
                                      'availability unconfirmed',
                                      '<span class="pill warn">recorded / availability unverified</span>'],
                            'src': ['S44', 'S41', 'S43', 'S67']},
                           {'cells': ['R17',
                                      'Experience with delicate work in a sensitive, tenant-occupied unit',
                                      'Environment',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S70', 'S69']},
                           {'cells': ['R18',
                                      'Reference pictures may be supplied; work from description if absent',
                                      'Input',
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R19',
                                      'No manual input; complete tasks autonomously',
                                      'Process',
                                      'No clarification requested; desk research/build performed',
                                      '<span class="pill ok">implemented / see evidence</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R20',
                                      'Review repo line by line; official trusted sources; links; flag '
                                      'irregularities',
                                      'Repo work',
                                      'Repository inventory and dashboard row audit generated; unrelated '
                                      'GEMS facts not externally verified',
                                      '<span class="pill warn">inventory done / external facts '
                                      'flagged</span>'],
                            'src': ['S44', 'S45', 'S47', 'S76']},
                           {'cells': ['R21',
                                      'GitHub Pages site: clean landing page, category subpages, simple '
                                      'tables',
                                      'Site',
                                      'Static dashboard built at repository root',
                                      '<span class="pill ok">implemented / see evidence</span>'],
                            'src': ['S44', 'S46']},
                           {'cells': ['R22',
                                      'Every table row has an official source link; unconfirmable values '
                                      'blank and flagged',
                                      'Verification',
                                      'Source links present; owner/third-party rows lack official '
                                      'confirmation and are flagged (U21)',
                                      '<span class="pill warn">partial / needs review</span>'],
                            'src': ['S44', 'S04', 'S45']},
                           {'cells': ['R23',
                                      'Rank contractors best-to-hire with reasoning, costs, official links '
                                      'and phone numbers',
                                      'Decision analysis',
                                      'Conditional ranking and contact directory published; combined costs '
                                      'blank/unverified',
                                      '<span class="pill ok">implemented / see evidence</span>'],
                            'src': ['S44', 'S69']},
                           {'cells': ['R24',
                                      'No hallucinations; never infer or fill unconfirmed values',
                                      'Verification',
                                      'Blank + UNVERIFIED policy and source grades enforced; manual review '
                                      'still required',
                                      '<span class="pill ok">policy implemented</span>'],
                            'src': ['S44', 'S45']},
                           {'cells': ['R25',
                                      'Coordinate parallel sessions through COORDINATION.md; non-overlapping '
                                      'scopes; frequent commits',
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
                                      'See COORDINATION.md for the actual PR, merge and Pages deployment '
                                      'record',
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
                                      '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                      'class="pill warn">UNVERIFIED</span>',
                                      '<span class="pill warn">owner-provided / unverified</span>'],
                            'src': ['S44', 'S70']}],
                  'caption': 'Owner requirements cannot be “officially verified” as facts. Implementation '
                             'status is a project record; external facts use the cited official/company '
                             'sources. Blank means no official confirmation.'},
 'technical': {'title': 'Technical background — manufacturer and publisher evidence',
               'columns': ['Topic', 'What the source supports', 'Relevance / limit', 'Grade', 'Source'],
               'rows': [{'cells': ['Trip-lever assembly',
                                   'Watco diagrams show overflow plate, linkage, drop cylinder, overflow '
                                   'elbow, tee, drain elbow and strainer',
                                   'Typical assembly; does not identify this tub’s model',
                                   '<span class="pill ok">manufacturer</span>'],
                         'src': ['S71']},
                        {'cells': ['Full kit exists',
                                   'Oatey lists a Dearborn plastic tubular trip-lever bath waste full kit',
                                   'Component naming only; not a diagnosis',
                                   '<span class="pill ok">manufacturer</span>'],
                         'src': ['S14']},
                        {'cells': ['Above access',
                                   'This Old House describes removing two overflow-plate screws; stubborn '
                                   'drains may need below access',
                                   'Publisher DIY guidance; outcome for this seized lever unverified <span '
                                   'class="pill warn">UNVERIFIED</span>',
                                   '<span class="pill warn">publisher</span>'],
                         'src': ['S18']},
                        {'cells': ['Below access',
                                   'This Old House describes aligning gasket/elbow from below while a helper '
                                   'holds the shoe above',
                                   'Publisher guidance; exact opening size/location unverified <span '
                                   'class="pill warn">UNVERIFIED</span>',
                                   '<span class="pill warn">publisher</span>'],
                         'src': ['S18']},
                        {'cells': ['Model-specific adjustment',
                                   'Watco says linkage must not be kinked and the drop cylinder may need '
                                   'readjustment',
                                   'Follow the actual manufacturer/model instructions; do not force the '
                                   'mechanism',
                                   '<span class="pill ok">manufacturer</span>'],
                         'src': ['S71']},
                        {'cells': ['Inspection before covering',
                                   'SF DBI says permitted plumbing work is inspected before covering pipes',
                                   'Sequencing rule if a permit applies; not a determination that this job '
                                   'is exempt',
                                   '<span class="pill ok">official</span>'],
                         'src': ['S01']},
                        {'cells': ['Wallboard/fire protection',
                                   'SF DBI lists minor interior wallboard repairs as exempt unless required '
                                   'for fire protection',
                                   'Ceiling assembly and exact scope must be checked; no exemption inferred',
                                   '<span class="pill ok">official</span>'],
                         'src': ['S02']},
                        {'cells': ['This tub’s cause/model',
                                   'No photo, model number or inspection was supplied',
                                   '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                   'class="pill warn">UNVERIFIED</span>',
                                   '<span class="pill warn">unverified</span>'],
                         'src': ['S44', 'S71']}],
               'caption': 'Manufacturer instructions are authoritative for their own products only. '
                          'Publisher guidance is not an official code source or a site-specific diagnosis.'},
 'permits': {'title': 'Official permit, licensing and occupied-unit references',
             'columns': ['Topic', 'Official rule / fact', 'Project application', 'Grade', 'Source'],
             'rows': [{'cells': ['Cutting/replacing pipes',
                                 'SF DBI: permit needed before cutting into or replacing pipes, especially '
                                 'pipes covered by a wall; see §104.2 exemptions',
                                 'Exact waste-and-overflow scope must be assessed; no exemption inferred',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S01', 'S74']},
                      {'cells': ['Plumbing exemptions',
                                 'SF Plumbing Code §104.2 includes leak repair and unstopping that do not '
                                 'require cutting into/removing piping or traps',
                                 'Whether a seized trip-lever repair fits is unverified <span class="pill '
                                 'warn">UNVERIFIED</span>',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S74']},
                      {'cells': ['Interior wallboard',
                                 'Minor repairs to existing interior plaster/wallboard are listed as exempt '
                                 'unless required for fire protection',
                                 'Ceiling opening/patch may differ from a minor repair; confirm '
                                 'assembly/scope',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S02']},
                      {'cells': ['Kitchen/bath route',
                                 'SF DBI online kitchen/bath route is for in-kind fixtures, no structural '
                                 'work, no wall removal/moving, R-2/R-3 legally permitted rooms',
                                 'Related plumbing/electrical permits and finals are separate',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S72']},
                      {'cells': ['Who may apply',
                                 'C-4/C-36 plumbing; B after scope approval; other listed classes for their '
                                 'scopes',
                                 'Match applicant classification to actual work',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S01', 'S05']},
                      {'cells': ['B general building limits',
                                 'BPC 7057 requires appropriate classification or licensed subcontractor for '
                                 'other trades, subject to multi-trade rules',
                                 'B + C-36 supports a combined plumbing/building contract; drywall execution '
                                 'still unconfirmed',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S68']},
                      {'cells': ['Small-job licensing exemption',
                                 'BPC §7048: aggregate price under $1,000, casual/minor/inconsequential, no '
                                 'building permit required; limitations apply',
                                 'Licensing exemption is not a permit exemption; current text effective '
                                 '2026-01-01',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S13']},
                      {'cells': ['Tenant entry',
                                 'Civil Code §1954 generally requires reasonable written notice, '
                                 'date/approximate time/purpose and normal business hours; exceptions apply',
                                 'Coordinate lawful access; 24 hours is a presumption, not an unconditional '
                                 'rule',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S70']},
                      {'cells': ['Confirm with DBI',
                                 'Permit Center help desk 628-652-4900; permitsf@sfgov.org',
                                 'Confirm exact scope before work; this site is not legal advice',
                                 '<span class="pill ok">official</span>'],
                       'src': ['S01']},
                      {'cells': ['Specialty contractor incidental work',
                                 'BPC §7059',
                                 'Specialty contractors may undertake other trades when incidental and '
                                 'supplemental to their licensed work; exact ceiling-repair applicability is '
                                 'not established',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S62']}],
             'caption': 'Neutral official guidance only. Applicability to this concealed repair is not '
                        'determined here.'},
 'findings': {'title': 'Findings and decision analysis',
              'columns': ['#', 'Finding', 'Basis', 'Status', 'Source'],
              'rows': [{'cells': ['F01',
                                  'The three owner-reported estimates describe different scopes and are not '
                                  'comparable all-in prices',
                                  'Adjustment vs lever/spout/diverter vs waste-and-overflow replacement; '
                                  'drywall inclusion is not stated',
                                  '<span class="pill warn">owner-provided / unverified</span>'],
                        'src': ['S44']},
                       {'cells': ['F02',
                                  'General SF is the best documented combined-scope inquiry',
                                  'Company advertises plumbing and sheetrock/tape/texture; CSLB B+C-36 '
                                  'active',
                                  '<span class="pill info">conditional recommendation</span>'],
                        'src': ['S09', 'S77', 'S78']},
                       {'cells': ['F03',
                                  'Handyman Heroes is the second documented combined-scope inquiry',
                                  'Company advertises wall repair and plumbing; CSLB B+C-36 active; '
                                  'disclosure exists',
                                  '<span class="pill info">conditional recommendation</span>'],
                        'src': ['S10', 'S12', 'S64']},
                       {'cells': ['F04',
                                  'Ace has a strong license/insurance profile but drywall self-performance '
                                  'is unconfirmed',
                                  'CSLB B+C-36 and workers’ compensation policy; company property-manager '
                                  'work',
                                  '<span class="pill warn">license verified; scope unverified</span>'],
                        'src': ['S11', 'S43']},
                       {'cells': ['F05',
                                  'Eight candidate licenses are current and active on CSLB',
                                  'Eight official records read 2026-11-08',
                                  '<span class="pill ok">verified</span>'],
                        'src': ['S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S56', 'S57']},
                       {'cells': ['F06',
                                  'Four records show no-employee workers’ compensation exemptions; Fast '
                                  'Response policy expires 2026-12-18',
                                  'CSLB #757796, #959843, #1115649, #841229; #1024971 policy dates',
                                  '<span class="pill warn">verified / time-sensitive</span>'],
                        'src': ['S07', 'S09', 'S56', 'S57', 'S08']},
                       {'cells': ['F07',
                                  'Yelp numeric ratings/counts are not verified',
                                  'Direct fetch HTTP 403; search excerpts only; numeric cells blank',
                                  '<span class="pill warn">unverified</span>'],
                        'src': ['S32', 'S33', 'S34', 'S35', 'S36', 'S73']},
                       {'cells': ['F08',
                                  'Exact concealed waste-and-overflow experience in an occupied unit is '
                                  'unverified for every candidate',
                                  'License records and company service claims do not establish this job '
                                  'capability',
                                  '<span class="pill warn">unverified</span>'],
                        'src': ['S04', 'S40', 'S43', 'S69']},
                       {'cells': ['F09',
                                  'Access route cannot be determined from the description alone',
                                  'Manufacturer instructions are model-specific; no photos/model/inspection '
                                  'supplied',
                                  '<span class="pill warn">unverified</span>'],
                        'src': ['S44', 'S71', 'S14']},
                       {'cells': ['F10',
                                  'Permit applicability depends on the exact plumbing and ceiling scope',
                                  'SF DBI rules and §104.2 exemptions cited; no project determination made',
                                  '<span class="pill ok">official context</span>'],
                        'src': ['S01', 'S02', 'S74', 'S72']},
                       {'cells': ['F11',
                                  'No combined written quote or provider acceptance exists in this research',
                                  'Owner reported prior estimates; this session did not contact providers',
                                  '<span class="pill warn">unverified</span>'],
                        'src': ['S44', 'S45']},
                       {'cells': ['F12',
                                  'Unrelated GEMS material and earlier dashboards are preserved, not treated '
                                  'as plumbing evidence',
                                  'Repository inventory and historical snapshot',
                                  '<span class="pill warn">irregularity / flagged</span>'],
                        'src': ['S47', 'S75', 'S76']}],
              'caption': 'Analysis is explicitly separated from verified license facts, company '
                         'self-descriptions, owner statements and third-party reviews.'},
 'flagged': {'title': 'Flagged for Review — unverified values and irregularities',
             'columns': ['ID', 'Item', 'Why it is flagged', 'What would clear it', 'Status', 'Source'],
             'rows': [{'cells': ['U01',
                                 'Three estimate amounts ($614, $550, $135) and all owner-provided problem '
                                 'facts',
                                 "No official or public source publishes private quotes or the owner's "
                                 'description; officially verified value cells are blank',
                                 'Attach the original written quotes and photos as project documents, then '
                                 're-verify',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S06', 'S07', 'S08']},
                      {'cells': ['U02',
                                 'Estimate scope wording and dates',
                                 'Transcribed from the brief only',
                                 'Supply the original quote documents',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S45']},
                      {'cells': ['U03',
                                 'Yelp ratings and review counts',
                                 'Direct Yelp fetches returned HTTP 403 on 2026-11-08; search excerpts '
                                 'located profiles but numeric values are not independently verified',
                                 'Open linked profiles on the decision date; numeric cells remain blank',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S32', 'S33', 'S34', 'S35', 'S36', 'S73', 'S04']},
                      {'cells': ['U04',
                                 'Fast Response address differences',
                                 'CSLB #1024971 lists 236 W POTRAL AVE #459; Yelp excerpt lists 4444 Geary '
                                 'Blvd; company repair page gives a mailing address 236 W Portal Ave #259',
                                 'Confirm mailing vs service address and legal entity before hiring',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S08', 'S34', 'S61']},
                      {'cells': ['U05',
                                 "Fast Response workers'-compensation policy expires 2026-12-18",
                                 'CSLB #1024971 shows a policy with that expiry date; re-check on the hire '
                                 'date',
                                 'Request a current certificate of insurance',
                                 '<span class="pill warn">verified fact / time-sensitive</span>'],
                       'src': ['S08']},
                      {'cells': ['U06',
                                 "Workers'-compensation exemptions on #757796, #959843, #1115649 and #841229",
                                 'All four CSLB records state the licensee certified no employees at this '
                                 'time',
                                 'Confirm in writing who will be on site and what coverage applies to the '
                                 'crew',
                                 '<span class="pill warn">verified fact / needs review</span>'],
                       'src': ['S07', 'S09', 'S56', 'S57']},
                      {'cells': ['U07',
                                 'Handyman Heroes CSLB complaint disclosure',
                                 "CSLB shows citation 2 2020 001045 dated 07/12/2020, 'FOR DISCLOSURE ONLY "
                                 "PER B&P CODE 7124.6' — reported verbatim, no interpretation",
                                 'Open the official disclosure yourself and decide before hiring',
                                 '<span class="pill warn">verified fact / needs review</span>'],
                       'src': ['S12', 'S10']},
                      {'cells': ['U08',
                                 'Handyman Heroes site claims Licensed C-10',
                                 'Official CSLB #1003394 lists B and C-36 only; company home page still says '
                                 'Licensed C-10',
                                 'Ask which license/entity covers any electrical work; no electrical scope '
                                 'is assumed',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S42', 'S10']},
                      {'cells': ['U09',
                                 "Fast Response company aggregate '4.9 / 1,500 Reviews on Yelp &amp; Google'",
                                 'Company self-claim combining two platforms; Yelp page could not be '
                                 're-fetched',
                                 'Re-open each platform separately',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S40', 'S34']},
                      {'cells': ['U10',
                                 'Szeto Plumbing and Handyman — license not established',
                                 'Historical lead only; no matching CSLB record was established in this '
                                 'pass; phone/license left blank',
                                 'Obtain a license number and verify directly, or exclude',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S37', 'S04']},
                      {'cells': ['U11',
                                 'Two dead source URLs from earlier sessions',
                                 'SFGate Home Guides redirects to an empty page; InspectAndTest returns HTTP '
                                 '500 (both re-checked 2026-11-07)',
                                 'Removed from all active citations; retained only as labeled documentation '
                                 'rows on the Source ledger',
                                 '<span class="pill ok">resolved / documented</span>'],
                       'src': ['S55', 'S45']},
                      {'cells': ['U12',
                                 'Repository content mismatch',
                                 'The README and docs/ describe an unrelated DOE GEMS fault-prospectivity '
                                 'audit; this dashboard occupies the site root',
                                 'No action required; legacy files deliberately untouched',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S47', 'S48']},
                      {'cells': ['U13',
                                 'Stale conflicting PR #32 from a parallel session',
                                 'Open since 2026-11-06, mergeable=CONFLICTING, also touches index.html; '
                                 'left untouched and not merged or closed by this session',
                                 'Owner may close or rebase it after this integration',
                                 '<span class="pill warn">needs review</span>'],
                       'src': ['S52', 'S45']},
                      {'cells': ['U14',
                                 'No combined written quote for plumbing + drywall',
                                 'No official/company source publishes a combined price for this job; '
                                 'owner-reported amounts are not combined quotes',
                                 'Request one written scope with access, plumbing, patch/finish, testing and '
                                 'tenant coordination',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S69']},
                      {'cells': ['U15',
                                 'Job-specific capability, occupied-unit experience and exact service area',
                                 'CSLB verifies license classes, not this delicate repair; company '
                                 'claims/reviews are not independent capability proof',
                                 'Request references for concealed waste-and-overflow work in occupied units '
                                 'and confirm the service address',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S04', 'S40', 'S43', 'S67', 'S69']},
                      {'cells': ['U16',
                                 'Yelp “Verified License” badges are third-party',
                                 'A platform badge is not CSLB verification; Yelp returned HTTP 403 on '
                                 're-check',
                                 'Verify the license number directly on CSLB',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S36', 'S04', 'S29']},
                      {'cells': ['U17',
                                 'Handyman Heroes address mismatch',
                                 'Official CSLB #1003394 lists 912 Cole St # 202; the prior Yelp snapshot '
                                 'lists 1525 Waller St',
                                 'Ask the company for its current service address',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S10', 'S36']},
                      {'cells': ['U18',
                                 'Outdated $500 contractor-licensing references',
                                 'Widely repeated older $500 figures are outdated; current B&amp;P §7048 (AB '
                                 '1170, effective 2026-01-01) uses under $1,000 and no building permit '
                                 'required',
                                 'Use the current statutory text linked here',
                                 '<span class="pill ok">resolved / documented</span>'],
                       'src': ['S13']},
                      {'cells': ['U19',
                                 'Repository scope: earlier research sets are historical',
                                 'Earlier dashboards under docs/ and bathtub-overflow/ are archived. A '
                                 'previously reported legacy link docs/parallel-index.html → docs/results/ '
                                 'resolves; no change made',
                                 'No action required; historical pages untouched',
                                 '<span class="pill warn">needs review</span>'],
                       'src': ['S45', 'S47', 'S48']},
                      {'cells': ['U20',
                                 'No provider was contacted during this desk-research session',
                                 'The owner reported prior estimates; this research session did not contact '
                                 'providers or independently confirm job-specific scope, current price or '
                                 'availability',
                                 'Contact shortlisted firms with the written scope',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S45', 'S58']},
                      {'cells': ['U21',
                                 'Official-source coverage and automated verification limits',
                                 'Some historical rows cite only publishers, platforms or internal project '
                                 'records, not government sources; source-link checks do not establish '
                                 'truth, relevance or live availability',
                                 'Review each row and its cited source; current ranking uses directly '
                                 'checked official/company sources',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S04', 'S45', 'S75']},
                      {'cells': ['U22',
                                 'License classifications do not establish the only possible repair '
                                 'arrangement',
                                 'B + C-36 is a useful screening signal, not proof of acceptance or an '
                                 'exclusive route. BPC §7059 allows qualifying incidental and supplemental '
                                 'work by specialty contractors; application to this ceiling is not '
                                 'established. The archived docs/overflow-verification.html contains more '
                                 'categorical statements that omit this qualification',
                                 'Ask each contractor for a written scope, responsible trades and '
                                 'confirmation of applicable requirements',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S62', 'S58', 'S63']},
                      {'cells': ['U33',
                                 'Drywall inclusion in the three owner-reported estimates',
                                 'The supplied wording does not state whether drywall/ceiling patch and '
                                 'finish is included; earlier blanket exclusions were unsupported',
                                 'Obtain written scope inclusions/exclusions for each estimate',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44']},
                      {'cells': ['U23',
                                 'General SF crew and insurance',
                                 'CSLB #959843 shows a no-employee workers’ compensation exemption; a bond '
                                 'is not liability insurance',
                                 'Confirm crew identity, workers’ compensation and general liability '
                                 'coverage before work',
                                 '<span class="pill warn">verified fact / needs review</span>'],
                       'src': ['S09', 'S69']},
                      {'cells': ['U24',
                                 'Handyman Heroes workers’ compensation classification codes',
                                 'CSLB #1003394 lists carpentry/high-low wage and clerical codes; adequacy '
                                 'for plumbing work is not established by the record',
                                 'Ask the carrier/contractor to confirm coverage for the actual plumbing '
                                 'crew',
                                 '<span class="pill warn">needs review</span>'],
                       'src': ['S10', 'S69']},
                      {'cells': ['U25',
                                 "Manny's exact San Francisco service availability",
                                 'Company lists surrounding San Mateo & San Francisco Counties but not a '
                                 'specific SF address commitment; CSLB address is Daly City',
                                 'Confirm the job address is within the service area and obtain a written '
                                 'quote',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S57', 'S67']},
                      {'cells': ['U26',
                                 'Rapid Flow / Manny’s / Szeto review evidence',
                                 'No directly verified Yelp profile was established for these leads in this '
                                 'pass; review cells remain blank',
                                 'Locate and review platform profiles independently; do not infer ratings',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S56', 'S57', 'S37', 'S04']},
                      {'cells': ['U27',
                                 'Historical sources and prior dashboards',
                                 'Prior publisher/platform rows are preserved but not reverified and are '
                                 'excluded from the current ranking',
                                 'Use the current source ledger and historical snapshot for audit only',
                                 '<span class="pill warn">historical</span>'],
                       'src': ['S75', 'S45']},
                      {'cells': ['U28',
                                 'Unrelated repository content',
                                 'GEMS geothermal audit files are inventoried but their external factual '
                                 'claims were not verified as part of this plumbing project',
                                 'Treat GEMS content as a separate archived project',
                                 '<span class="pill warn">irregularity</span>'],
                       'src': ['S47', 'S76']},
                      {'cells': ['U29',
                                 'Public repository / Pages visibility',
                                 'GitHub Pages is public; only project-suitable content is published and '
                                 'requester-only context is excluded',
                                 'Review public artifacts before adding any sensitive material',
                                 '<span class="pill info">privacy boundary</span>'],
                       'src': ['S46', 'S45']},
                      {'cells': ['U30',
                                 'Ranking is conditional editorial analysis',
                                 'Ordering uses documented scope, license class, insurance/disclosure and '
                                 'service-area evidence; it is not a measured quality score or endorsement',
                                 'Re-rank after written quotes, references and site assessment',
                                 '<span class="pill info">analysis</span>'],
                       'src': ['S69', 'S09', 'S10', 'S11']},
                      {'cells': ['U31',
                                 'Permit applicability is not determined',
                                 'Official rules and exemptions are cited, but the exact concealed '
                                 'plumbing/ceiling scope has not been assessed by DBI',
                                 'Confirm scope and applicable requirements with DBI and the licensed '
                                 'contractor',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S01', 'S02', 'S74', 'S72']},
                      {'cells': ['U32',
                                 'No reference photos or model identification',
                                 'No photos, model number or inspection were supplied; assembly type and '
                                 'access route are not inferred',
                                 'Provide photos/model to the contractor for assessment; verified cells '
                                 'remain blank until then',
                                 '<span class="pill warn">UNVERIFIED</span>'],
                       'src': ['S44', 'S71']}],
             'caption': 'Flagged items are published for review and do not block the site or merge. '
                        '“Verified fact / needs review” means the cited record was read, but a hiring '
                        'decision still requires confirmation.'},
 'repo_review': {'title': 'Repository review — current integration pass',
                 'columns': ['Area', 'What was found / done', 'Verification', 'Result', 'Source'],
                 'rows': [{'cells': ['Canonical dashboard',
                                     'Existing root dashboard refreshed rather than duplicated; prior data '
                                     'snapshot preserved',
                                     'Local files and build',
                                     'reviewed'],
                           'src': ['S46', 'S75', 'S45']},
                          {'cells': ['Source policy',
                                     'Current ranking uses directly checked CSLB/company/manufacturer '
                                     'sources; publisher/platform/owner values are flagged',
                                     'Evidence ledger and row audit',
                                     'implemented'],
                           'src': ['S04', 'S45']},
                          {'cells': ['Contractor records',
                                     'Eight CSLB records re-read 2026-11-08; four no-employee exemptions and '
                                     'one near-term policy expiry recorded',
                                     'Official CSLB pages',
                                     'verified'],
                           'src': ['S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S56', 'S57']},
                          {'cells': ['Unsupported prior claims',
                                     'Blanket drywall exclusion from owner quotes and “below access is the '
                                     'norm” corrected to unverified/site-specific',
                                     'Owner wording and manufacturer/publisher limits',
                                     'corrected / flagged'],
                           'src': ['S44', 'S71', 'S18']},
                          {'cells': ['Legacy project',
                                     'README and data/docs include an unrelated DOE GEMS audit; preserved '
                                     'unchanged',
                                     'Repository inventory',
                                     'irregularity'],
                           'src': ['S47', 'S76']},
                          {'cells': ['Parallel archives',
                                     'Earlier dashboards, shortlist and verification logs preserved and '
                                     'linked as historical',
                                     'Local artifact existence',
                                     'preserved'],
                           'src': ['S49', 'S50', 'S51', 'S58', 'S59', 'S60']},
                          {'cells': ['Coordination',
                                     'Board read before edits; claim pushed; concurrent entries preserved '
                                     'during rebase',
                                     'Git history and board',
                                     'reviewed'],
                           'src': ['S45']},
                          {'cells': ['Open stale PRs',
                                     'PR #32 and #42 remain open/conflicting from earlier sessions; not '
                                     'merged or closed here',
                                     'GitHub API checked 2026-11-08',
                                     'needs review'],
                           'src': ['S52', 'S45']},
                          {'cells': ['Pages configuration',
                                     'GitHub Pages source main at /; legacy build type; .nojekyll present; '
                                     'deploy status checked separately',
                                     'GitHub API',
                                     'reviewed'],
                           'src': ['S46', 'S45']},
                          {'cells': ['Tests',
                                     'Dashboard build, link/row/privacy checks and site test modules run in '
                                     'this pass; unrelated GEMS model suite not run',
                                     'Verification report',
                                     'see verification page'],
                           'src': ['S45', 'S46']},
                          {'cells': ['Privacy',
                                     'Published text sweep for requester-only wording; no private rationale '
                                     'added',
                                     'Automated sweep + review',
                                     'pass'],
                           'src': ['S45']},
                          {'cells': ['Inventory',
                                     'Source/artifact files hashed and categorized; generated pages/reports '
                                     'excluded to avoid self-reference',
                                     'SHA-256 inventory',
                                     'downloadable'],
                           'src': ['S76']}],
                 'caption': 'This is a plumbing-project integration audit. Unrelated GEMS artifacts are '
                            'inventoried, not externally fact-checked. Historical pages are preserved for '
                            'provenance.'},
 'source_ledger': {'title': 'Source ledger — all sources with verification status',
                   'columns': ['ID', 'Source', 'Publisher / tier', 'Status', 'What it supports', 'Source'],
                   'rows': [],
                   'caption': 'Every external URL used on this dashboard is listed here with its publisher, '
                              "tier, retrieval date and verification status. 'dead' sources are never linked "
                              'from a table row; their URL is shown as plain text for documentation only.'},
 'ranking': {'title': 'Hiring priority — conditional, evidence-based ranking',
             'columns': ['Rank',
                         'Company / evidence tier',
                         'Why this rank',
                         'Conditions before hiring',
                         'Combined quote',
                         'Source'],
             'rows': [{'cells': ['1',
                                 '<strong>General SF</strong><br><small>A — both trades advertised</small>',
                                 'Best documented single-provider fit: the same company advertises plumbing '
                                 'and sheetrock/tape/texture, and CSLB confirms B + C-36 on one license.',
                                 "Workers' compensation exemption; confirm who attends, insurance, exact "
                                 'access method, tenant precautions and a combined written price.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S09', 'S41', 'S77', 'S78']},
                      {'cells': ['2',
                                 '<strong>Handyman Heroes Inc</strong><br><small>A — both trades '
                                 'advertised</small>',
                                 'Second documented combined-scope fit, with wall repair and plumbing '
                                 'advertised by the same licensed company.',
                                 'CSLB complaint disclosure must be reviewed; site claims C-10 but CSLB '
                                 "#1003394 lists only B/C-36; listed workers' compensation codes are "
                                 'carpentry/clerical, so confirm coverage for the actual crew.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S10', 'S42', 'S64']},
                      {'cells': ['3',
                                 '<strong>Ace Plumbing & Rooter Inc</strong><br><small>B — dual license, '
                                 'drywall unconfirmed</small>',
                                 'Strong license/insurance profile and documented property-manager work; B + '
                                 'C-36 supports a combined contract, but drywall self-performance was not '
                                 'found on the reviewed page.',
                                 'Ask whether drywall patch/finish is self-performed or subcontracted and '
                                 'for concealed waste-and-overflow references.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S11', 'S43']},
                      {'cells': ['4',
                                 '<strong>Rapid Flow Plumbing & Rooter Inc</strong><br><small>B — dual '
                                 'license, drywall unconfirmed</small>',
                                 'Dual B + C-36 license and advertised remodeling support a combined-scope '
                                 'inquiry.',
                                 "Workers' compensation exemption; no directly verified Yelp profile in this "
                                 'pass; confirm crew, insurance, drywall scope and exact repair experience.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S56', 'S65', 'S66']},
                      {'cells': ['5',
                                 "<strong>Manny's Plumbing & Rooter</strong><br><small>B — dual license, "
                                 'drywall unconfirmed</small>',
                                 'Dual license and tub/drain/remodel services make it a reasonable backup '
                                 'inquiry.',
                                 "Daly City address, workers' compensation exemption and exact service-area "
                                 'availability require confirmation.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S57', 'S67']},
                      {'cells': ['6',
                                 '<strong>Expert Plumbing Solutions</strong><br><small>C — plumbing-only '
                                 'license</small>',
                                 'Broadest owner-reported quote scope (waste-and-overflow replacement) and '
                                 "current workers' compensation policy, but only C-36 is verified.",
                                 'Drywall scope/arrangement is unconfirmed; ask whether patch/finish is '
                                 'included and who performs it. BPC §7059 may allow qualifying '
                                 'incidental/supplemental work, but applicability here is unverified. '
                                 'owner-reported $614 is unverified and not a combined quote.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S06', 'S38']},
                      {'cells': ['7',
                                 '<strong>Fast Response Plumbing & Rooter</strong><br><small>C — '
                                 'plumbing-only license</small>',
                                 'Company explicitly advertises bathtub waste-and-overflow repair and has a '
                                 "current workers' compensation policy; owner-reported adjustment quote is "
                                 'the lowest of the three.',
                                 'Only C-36 verified; policy expires 2026-12-18; CSLB/Yelp/site addresses '
                                 'differ; $135 is owner-reported and not a combined quote.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S08', 'S40', 'S61']},
                      {'cells': ['8',
                                 '<strong>Bay Area Plumbing</strong><br><small>C — plumbing-only '
                                 'license</small>',
                                 'Relevant plumbing/tub experience is advertised and an owner-reported quote '
                                 'exists, but the verified license is C-36 only.',
                                 "Workers' compensation exemption; drywall requires another appropriately "
                                 'licensed provider/subcontractor; $550 is owner-reported and not a combined '
                                 'quote.',
                                 '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                 'class="pill warn">UNVERIFIED</span>'],
                       'src': ['S07', 'S39']}],
             'caption': 'Editorial decision analysis, not a contractor endorsement. Tier A: both trades '
                        'advertised + B/C-36 license. Tier B: B/C-36 license but drywall self-performance '
                        'unconfirmed. Tier C: C-36-only verified license. Within tiers, documented scope, '
                        'insurance/disclosure and service-area evidence break ties. No numeric quality score '
                        'is invented. All combined quotes are blank/unverified.'},
 'contacts': {'title': 'Contact directory — official business and CSLB sources',
              'columns': ['Company',
                          'Phone',
                          'Official website',
                          'CSLB record',
                          'Address on CSLB record',
                          'Source'],
              'rows': [{'cells': ['<strong>General SF</strong>',
                                  '(650) 303-1515',
                                  '<a href="https://generalsf.com/" target="_blank" rel="noopener '
                                  'noreferrer">site</a> · <a href="https://generalsf.com/building" '
                                  'target="_blank" rel="noopener noreferrer">service page</a> · <a '
                                  'href="https://generalsf.com/plumbing" target="_blank" rel="noopener '
                                  'noreferrer">service page</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843" '
                                  'target="_blank" rel="noopener noreferrer">#959843</a>',
                                  '3624 Irving Street Ste A, San Francisco, CA 94122'],
                        'src': ['S09', 'S41', 'S77', 'S78']},
                       {'cells': ['<strong>Handyman Heroes Inc</strong>',
                                  '(844) 382-4376',
                                  '<a href="https://www.handymanhero.es/" target="_blank" rel="noopener '
                                  'noreferrer">site</a> · <a '
                                  'href="https://www.handymanhero.es/handyman-services/" target="_blank" '
                                  'rel="noopener noreferrer">service page</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394" '
                                  'target="_blank" rel="noopener noreferrer">#1003394</a>',
                                  '912 Cole St # 202, San Francisco, CA 94117'],
                        'src': ['S10', 'S42', 'S64']},
                       {'cells': ['<strong>Ace Plumbing &amp; Rooter Inc</strong>',
                                  '(415) 824-6444',
                                  '<a href="https://www.aceplumbingandrooter.com/" target="_blank" '
                                  'rel="noopener noreferrer">site</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071" '
                                  'target="_blank" rel="noopener noreferrer">#829071</a>',
                                  '1090 Bryant Street, San Francisco, CA 94103-4417'],
                        'src': ['S11', 'S43']},
                       {'cells': ['<strong>Rapid Flow Plumbing &amp; Rooter Inc</strong>',
                                  '(415) 866-8401',
                                  '<a href="https://www.rapidflowbayarea.com/" target="_blank" rel="noopener '
                                  'noreferrer">site</a> · <a href="https://www.rapidflowbayarea.com/contact" '
                                  'target="_blank" rel="noopener noreferrer">service page</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115649" '
                                  'target="_blank" rel="noopener noreferrer">#1115649</a>',
                                  '230 Edinburgh St, San Francisco, CA 94112'],
                        'src': ['S56', 'S65', 'S66']},
                       {'cells': ['<strong>Manny&#x27;s Plumbing &amp; Rooter</strong>',
                                  '(650) 207-5733',
                                  '<a href="https://www.mannysplumbingandremodeling.com/" target="_blank" '
                                  'rel="noopener noreferrer">site</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=841229" '
                                  'target="_blank" rel="noopener noreferrer">#841229</a>',
                                  '41 Midvale Drive, Daly City, CA 94015'],
                        'src': ['S57', 'S67']},
                       {'cells': ['<strong>Expert Plumbing Solutions</strong>',
                                  '(415) 531-5340',
                                  '<a href="https://www.eplumbingsolutions.com/" target="_blank" '
                                  'rel="noopener noreferrer">site</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638" '
                                  'target="_blank" rel="noopener noreferrer">#977638</a>',
                                  '1465 44th Avenue, San Francisco, CA 94122'],
                        'src': ['S06', 'S38']},
                       {'cells': ['<strong>Fast Response Plumbing &amp; Rooter</strong>',
                                  '(415) 596-6115',
                                  '<a href="https://www.fastresponseplumbingsf.com/" target="_blank" '
                                  'rel="noopener noreferrer">site</a> · <a '
                                  'href="https://www.fastresponseplumbingsf.com/plumbing-repair-replacement" '
                                  'target="_blank" rel="noopener noreferrer">service page</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971" '
                                  'target="_blank" rel="noopener noreferrer">#1024971</a>',
                                  '236 W POTRAL AVE #459, San Francisco, CA 94127'],
                        'src': ['S08', 'S40', 'S61']},
                       {'cells': ['<strong>Bay Area Plumbing</strong>',
                                  '(415) 668-8000',
                                  '<a href="https://www.bayareaplumbingsf.com/" target="_blank" '
                                  'rel="noopener noreferrer">site</a>',
                                  '<a '
                                  'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796" '
                                  'target="_blank" rel="noopener noreferrer">#757796</a>',
                                  '335 14th Avenue, San Francisco, CA 94118'],
                        'src': ['S07', 'S39']}],
              'caption': 'Phone numbers are shown from CSLB and cross-checked against company pages where '
                         'available. Addresses are CSLB addresses of record, not necessarily service '
                         'locations.'},
 'top_picks': {'title': 'Start here — top three conditional inquiries',
               'columns': ['Priority', 'Company', 'Phone', 'Why it leads', 'Source'],
               'rows': [{'cells': ['1',
                                   '<strong>General SF</strong><br><small>A — both trades advertised</small>',
                                   '(650) 303-1515',
                                   'Best documented single-provider fit: the same company advertises '
                                   'plumbing and sheetrock/tape/texture, and CSLB confirms B + C-36 on one '
                                   'license.'],
                         'src': ['S09', 'S41', 'S77', 'S78']},
                        {'cells': ['2',
                                   '<strong>Handyman Heroes Inc</strong><br><small>A — both trades '
                                   'advertised</small>',
                                   '(844) 382-4376',
                                   'Second documented combined-scope fit, with wall repair and plumbing '
                                   'advertised by the same licensed company.'],
                         'src': ['S10', 'S42', 'S64']},
                        {'cells': ['3',
                                   '<strong>Ace Plumbing & Rooter Inc</strong><br><small>B — dual license, '
                                   'drywall unconfirmed</small>',
                                   '(415) 824-6444',
                                   'Strong license/insurance profile and documented property-manager work; B '
                                   '+ C-36 supports a combined contract, but drywall self-performance was '
                                   'not found on the reviewed page.'],
                         'src': ['S11', 'S43']}],
               'caption': 'Conditional inquiry order, not booked work or a quality guarantee. See the full '
                          'ranking for caveats and blank combined-quote cells.'},
 'access_options': {'title': 'Access options — what is and is not established',
                    'columns': ['Route', 'Evidence', 'Project-specific conclusion', 'Source'],
                    'rows': [{'cells': ['From above (preferred)',
                                        'Watco instructions show overflow plate/linkage removal and '
                                        'adjustment for its models; this tub model is unknown',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>'],
                              'src': ['S71', 'S44']},
                             {'cells': ['From below (reported fallback)',
                                        'This Old House describes below access for stubborn drains; SF rules '
                                        'govern any cutting/replacement and covering',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>'],
                              'src': ['S18', 'S01', 'S44']},
                             {'cells': ['Ceiling drywall opening',
                                        'SF DBI lists minor wallboard repairs as exempt unless '
                                        'fire-protection related; exact ceiling assembly/scope unknown',
                                        '<span class="blank" aria-label="blank — unverified">—</span> <span '
                                        'class="pill warn">UNVERIFIED</span>'],
                              'src': ['S02', 'S74', 'S44']}],
                    'caption': 'No access method, opening size or permit exemption is inferred. A licensed '
                               'site assessment is required.'},
 'repo_inventory': {'title': 'Line-by-line source/artifact inventory',
                    'columns': ['Path', 'Bytes', 'SHA-256', 'Category', 'Review scope', 'Source'],
                    'rows': [],
                    'caption': 'Generated at build time.'}}

PAGES = {'index.html': {'title': 'Dashboard',
                'eyebrow': 'Research dashboard · San Francisco · updated 2026-11-08',
                'h1': 'Bathtub wastewater overflow trip lever',
                'lede': 'Decision dashboard for a reported stuck trip lever in concealed plumbing. It '
                        'organizes the owner’s requirements, three unverified estimates, eight active '
                        'license records, official business contacts, review limits and a conditional hiring '
                        'order.',
                'sections': [{'type': 'cards',
                              'items': [{'k': 'Owner-reported estimates',
                                         'v': '3',
                                         's': '2026-08-30 · amounts unverified',
                                         'tone': 'warn'},
                                        {'k': 'Active CSLB licenses',
                                         'v': '8',
                                         's': 'Official records read 2026-11-08',
                                         'tone': 'ok'},
                                        {'k': 'Confirmed combined quotes',
                                         'v': '0',
                                         's': 'No provider acceptance or all-in price confirmed',
                                         'tone': 'warn'},
                                        {'k': 'Flagged for review',
                                         'v': '33',
                                         's': 'Unverified values and irregularities · non-blocking',
                                         'tone': 'info'}]},
                             {'type': 'callout',
                              'tone': 'warn',
                              'html': '<strong>Best documented fit: General SF.</strong> Its own site lists '
                                      'plumbing and sheetrock/tape/texture, and CSLB confirms B + C-36. This '
                                      'is a conditional inquiry recommendation, not proof it can safely '
                                      'extract this lever. No provider has been contacted by this research '
                                      'session or confirmed this job. <a href="contractors.html">See the '
                                      'full ranking and caveats</a>.'},
                             {'type': 'table', 'ref': 'top_picks'},
                             {'type': 'table', 'ref': 'problem'},
                             {'type': 'quick',
                              'title': 'Browse by category',
                              'items': [{'href': 'summary.html',
                                         't': 'Executive summary',
                                         'd': 'Decision, costs, rules and next steps.'},
                                        {'href': 'requirements.html',
                                         't': 'Requirements',
                                         'd': 'Line-by-line register with verification status.'},
                                        {'href': 'contractors.html',
                                         't': 'Hiring ranking & contacts',
                                         'd': 'Eight candidates, phones, official sites and caveats.'},
                                        {'href': 'estimates.html',
                                         't': 'Estimates & costs',
                                         'd': 'Owner figures separated from verified cells.'},
                                        {'href': 'findings.html',
                                         't': 'Findings & analysis',
                                         'd': 'Access, scope, insurance and cost reasoning.'},
                                        {'href': 'permits.html',
                                         't': 'Permits & licensing',
                                         'd': 'Neutral official SF/California references.'},
                                        {'href': 'sources.html',
                                         't': 'Source ledger',
                                         'd': 'Current, historical, blocked and dead sources.'},
                                        {'href': 'flagged.html',
                                         't': 'Flagged for review',
                                         'd': 'All 32 open review items with sources.'}]},
                             {'type': 'callout',
                              'tone': 'info',
                              'html': '<strong>How to read this site.</strong> Official = '
                                      'government/manufacturer; company = business self-description; '
                                      'publisher/platform = third-party; owner-provided = project brief. A '
                                      'source link is not proof of every claim. Unconfirmed values are blank '
                                      'and marked UNVERIFIED. <a href="verification.html">Row-by-row '
                                      'audit</a>.'}]},
 'summary.html': {'title': 'Executive summary',
                  'eyebrow': 'Overview · updated 2026-11-08',
                  'h1': 'Executive summary',
                  'lede': 'The hiring decision, cost limits, official rules and unresolved items in one '
                          'place.',
                  'sections': [{'type': 'prose',
                                'title': '1. Problem and objective',
                                'html': '<p>The owner reports a bathtub wastewater overflow trip lever stuck '
                                        'in concealed plumbing behind the wall, in a tenant-occupied San '
                                        'Francisco unit. More than five licensed plumbers reportedly could '
                                        'not remove it from above without damage concern; the reported '
                                        'fallback is below access through a storage-unit ceiling. The '
                                        'objective is one licensed provider for plumbing and drywall, with '
                                        'delicate occupied-unit precautions. These are owner statements, not '
                                        'independently verified facts. <a href="brief.html">Project '
                                        'brief</a> · <a '
                                        'href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954" '
                                        'target="_blank" rel="noopener noreferrer">Official entry '
                                        'rules</a>.</p>'},
                               {'type': 'table',
                                'ref': 'estimates',
                                'title': '2. Estimates — official amount cells blank'},
                               {'type': 'callout',
                                'tone': 'warn',
                                'html': 'The owner-reported figures are $614, $550 and $135 for different '
                                        'scopes. They are not comparable all-in prices. Whether '
                                        'drywall/ceiling patch and finish is included is <strong>not '
                                        'stated</strong> and remains unverified. No combined quote or '
                                        'provider acceptance was confirmed.'},
                               {'type': 'table', 'ref': 'top_picks', 'title': '3. Conditional hiring order'},
                               {'type': 'prose',
                                'title': '4. Key findings',
                                'html': '<ul class="tight"><li>Eight licenses are current and active on CSLB '
                                        '(2026-11-08). Five list B + C-36; only General SF and Handyman '
                                        'Heroes had both trades explicitly advertised on the reviewed '
                                        'company pages. <a '
                                        'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843" '
                                        'target="_blank" rel="noopener noreferrer">General SF</a> · <a '
                                        'href="https://generalsf.com/building" target="_blank" rel="noopener '
                                        'noreferrer">building services</a> · <a '
                                        'href="https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394" '
                                        'target="_blank" rel="noopener noreferrer">Handyman Heroes</a> · <a '
                                        'href="https://www.handymanhero.es/handyman-services/" '
                                        'target="_blank" rel="noopener noreferrer">wall/plumbing '
                                        'services</a>.</li><li>Four records show no-employee workers’ '
                                        'compensation exemptions; Handyman Heroes has a CSLB complaint '
                                        'disclosure; Fast Response’s policy expires 2026-12-18. Confirm crew '
                                        'coverage and review disclosures before hiring. <a '
                                        'href="https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx" '
                                        'target="_blank" rel="noopener noreferrer">CSLB hiring '
                                        'guidance</a>.</li><li>Yelp profiles were located through search, '
                                        'but direct fetches returned HTTP 403. Numeric ratings/counts are '
                                        'blank/unverified and do not drive the ranking.</li><li>Manufacturer '
                                        'instructions are model-specific. No photos/model were supplied, so '
                                        'the access route and cause are not inferred. <a '
                                        'href="https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf" '
                                        'target="_blank" rel="noopener noreferrer">Watco '
                                        'instructions</a>.</li></ul>'},
                               {'type': 'prose',
                                'title': '5. Official rules and next action',
                                'html': '<p>SF DBI requires a permit before cutting into or replacing pipes, '
                                        'subject to §104.2 exemptions; minor wallboard repairs have a '
                                        'separate fire-protection limitation. Confirm the exact scope with '
                                        'DBI and the contractor. <a '
                                        'href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" '
                                        'target="_blank" rel="noopener noreferrer">SF plumbing guidance</a> '
                                        '· <a '
                                        'href="https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf" '
                                        'target="_blank" rel="noopener noreferrer">§104.2 PDF</a> · <a '
                                        'href="https://www.sf.gov/information--check-if-your-construction-project-needs-permit" '
                                        'target="_blank" rel="noopener noreferrer">wallboard guidance</a>. '
                                        'Request one written scope covering above assessment, below access '
                                        'if needed, ceiling cut/patch/finish, dust/occupant protection, '
                                        'testing before closure, insurance and tenant scheduling. Re-check '
                                        'the chosen license on the hire date. <a '
                                        'href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                                        'target="_blank" rel="noopener noreferrer">CSLB lookup</a>.</p> <a '
                                        'href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7059.&lawCode=BPC" '
                                        'target="_blank" rel="noopener noreferrer">BPC §7059</a> addresses '
                                        'incidental/supplemental specialty work; applicability to this '
                                        'ceiling is unverified.'},
                               {'type': 'callout',
                                'tone': 'info',
                                'html': '<a href="flagged.html">Flagged for Review</a> lists 33 items. <a '
                                        'href="EXECUTIVE-SUMMARY.md">Download the Markdown summary</a>. This '
                                        'is research, not legal advice, a quote or an endorsement.'}]},
 'requirements.html': {'title': 'Requirements',
                       'eyebrow': 'Overview · line-by-line register',
                       'h1': 'Requirements register',
                       'lede': 'Each requirement from the brief is tracked below. Owner statements are not '
                               'treated as officially verified facts; implementation status and external '
                               'evidence are separated.',
                       'sections': [{'type': 'table', 'ref': 'requirements'}]},
 'estimates.html': {'title': 'Estimates & costs',
                    'eyebrow': 'Decision · owner reports separated from verified values',
                    'h1': 'Estimates & costs',
                    'lede': 'Three owner-reported estimates dated 2026-08-30. Official amount/date cells are '
                            'blank because no official source publishes the private quotes.',
                    'sections': [{'type': 'table', 'ref': 'estimates'},
                                 {'type': 'table', 'ref': 'brief_quotes'},
                                 {'type': 'table', 'ref': 'benchmarks'},
                                 {'type': 'prose',
                                  'title': 'Cost reasoning',
                                  'html': '<p>The scopes differ: adjustment, lever/spout/diverter '
                                          'replacement, and waste-and-overflow replacement. The supplied '
                                          'wording does not state whether drywall is included, so no '
                                          'exclusion or inclusion is inferred. CSLB advises comparing '
                                          'written bids on identical scope rather than choosing the lowest '
                                          'number. <a '
                                          'href="https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx" '
                                          'target="_blank" rel="noopener noreferrer">CSLB guidance</a>. '
                                          'Publisher benchmarks are national context only and are flagged '
                                          'unverified as project values. <a '
                                          'href="https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm" '
                                          'target="_blank" rel="noopener noreferrer">Angi</a>.</p>'},
                                 {'type': 'callout',
                                  'tone': 'warn',
                                  'html': 'No all-in plumbing + drywall price is confirmed. Ask each '
                                          'provider to itemize diagnosis/above attempt, below access, '
                                          'plumbing parts/labor, ceiling patch/finish, protection/cleanup, '
                                          'testing, permit fees if applicable, and tenant coordination.'}]},
 'contractors.html': {'title': 'Hiring ranking & contacts',
                      'eyebrow': 'Decision · CSLB and company sources checked 2026-11-08',
                      'h1': 'Contractor ranking, contacts and reviews',
                      'lede': 'Eight active license records, official business phones/sites, and a '
                              'conditional best-to-hire inquiry order. No provider has confirmed this job.',
                      'sections': [{'type': 'callout',
                                    'tone': 'info',
                                    'html': '<strong>No provider has been contacted by this research session '
                                            'and no provider has confirmed this job.</strong> The owner '
                                            'reported prior estimates. Ranking is editorial analysis based '
                                            'on documented scope, license class, insurance/disclosure and '
                                            'service-area evidence — not a numeric quality score or '
                                            'endorsement.'},
                                   {'type': 'table', 'ref': 'ranking'},
                                   {'type': 'table', 'ref': 'contacts'},
                                   {'type': 'table', 'ref': 'contractors'},
                                   {'type': 'table', 'ref': 'review_snapshots'},
                                   {'type': 'table', 'ref': 'platforms'},
                                   {'type': 'prose',
                                    'title': 'Before hiring',
                                    'html': '<ol class="tight"><li>Re-check the license, classifications, '
                                            'bond, workers’ compensation and complaint disclosure on <a '
                                            'href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">CSLB</a>.</li><li>Confirm the legal entity, crew, '
                                            'general liability and workers’ compensation coverage for the '
                                            'actual work. <a '
                                            'href="https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx" '
                                            'target="_blank" rel="noopener noreferrer">CSLB '
                                            'guidance</a>.</li><li>Request references for concealed '
                                            'waste-and-overflow repair in occupied units and one written '
                                            'combined scope.</li><li>Review all <a '
                                            'href="flagged.html">flagged items</a>, especially U06, U07, '
                                            'U08, U22–U25 and U30.</li></ol>'}]},
 'findings.html': {'title': 'Findings & analysis',
                   'eyebrow': 'Decision · evidence and limits',
                   'h1': 'Findings & analysis',
                   'lede': 'What the sources support, what remains unverified, and how the conditional '
                           'ranking was derived.',
                   'sections': [{'type': 'table', 'ref': 'findings'},
                                {'type': 'table', 'ref': 'ranking'},
                                {'type': 'table', 'ref': 'access_options'},
                                {'type': 'prose',
                                 'title': 'Ranking method',
                                 'html': '<p>Tier A requires both trades advertised by the company and a '
                                         'verified B+C-36 license. Tier B has B+C-36 but drywall '
                                         'self-performance unconfirmed. Tier C has only C-36 verified. '
                                         'Within tiers, documented scope, workers’ compensation/disclosure '
                                         'and service-area evidence break ties. Costs are not scored because '
                                         'no comparable combined quote exists. This transparent ordering '
                                         'avoids invented numeric scores. <a '
                                         'href="https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B" '
                                         'target="_blank" rel="noopener noreferrer">B classification</a> · '
                                         '<a '
                                         'href="https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36" '
                                         'target="_blank" rel="noopener noreferrer">C-36 classification</a> '
                                         '· <a '
                                         'href="https://www.cslb.ca.gov/consumers/hire_a_contractor/finding_the_right_contractor.aspx" '
                                         'target="_blank" rel="noopener noreferrer">hiring guidance</a>.</p> '
                                         '<p><a '
                                         'href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7059.&lawCode=BPC" '
                                         'target="_blank" rel="noopener noreferrer">BPC §7059</a> allows '
                                         'qualifying incidental and supplemental work by specialty '
                                         'contractors; dual classification is a screening signal, not the '
                                         'only possible arrangement or proof of job acceptance.</p>'}]},
 'technical.html': {'title': 'Technical background',
                    'eyebrow': 'Reference · manufacturer first',
                    'h1': 'Technical background',
                    'lede': 'Model-specific manufacturer instructions and clearly labeled publisher '
                            'guidance. No diagnosis of this tub is inferred.',
                    'sections': [{'type': 'table', 'ref': 'technical'},
                                 {'type': 'callout',
                                  'tone': 'info',
                                  'html': 'No photos, model number or inspection were supplied. A licensed '
                                          'contractor should identify the assembly and choose the access '
                                          'method. Manufacturer instructions apply to their own products '
                                          'only.'}]},
 'permits.html': {'title': 'Permits & licensing',
                  'eyebrow': 'Reference · official sources only',
                  'h1': 'Permits, licensing and occupied-unit rules',
                  'lede': 'Neutral official San Francisco and California references. Applicability to the '
                          'exact concealed repair is not determined here.',
                  'sections': [{'type': 'table', 'ref': 'permits'},
                               {'type': 'callout',
                                'tone': 'info',
                                'html': 'Confirm the exact scope with SF DBI and the selected licensed '
                                        'contractor. Permit Center help desk: 628-652-4900; '
                                        'permitsf@sfgov.org. <a '
                                        'href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" '
                                        'target="_blank" rel="noopener noreferrer">sf.gov</a>. This page is '
                                        'not legal advice.'}]},
 'brief.html': {'title': 'Project brief',
                'eyebrow': 'Primary record · owner-provided · unverified',
                'h1': 'Project brief',
                'lede': 'Transcription of owner-provided project information. It is not an official public '
                        'source; verified value cells elsewhere remain blank and flagged.',
                'sections': [{'type': 'table', 'ref': 'brief_quotes'},
                             {'type': 'table', 'ref': 'problem'},
                             {'type': 'prose',
                              'title': 'What the brief says',
                              'html': '<p>The owner wants a provider serving San Francisco with experience '
                                      'in delicate work in a tenant-occupied unit. The trip lever is '
                                      'reported stuck inside hidden plumbing. Above removal is preferred, '
                                      'but 5+ licensed plumbers reportedly could not do so without damage '
                                      'concern and recommended below access; a storage unit underneath may '
                                      'require opening the ceiling drywall. One all-in-one plumbing/drywall '
                                      'service is wanted. Yelp and other review services were requested, '
                                      'along with an executive summary, ranked contractors, official '
                                      'links/phones, a live dashboard and a Flagged for Review page. '
                                      'Reference photos were mentioned but not supplied.</p><p '
                                      'class="src"><a href="brief.html">Primary record</a> · <a '
                                      'href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md" '
                                      'target="_blank" rel="noopener noreferrer">Coordination log</a>. No '
                                      'independent public source confirms these statements.</p>'},
                             {'type': 'callout',
                              'tone': 'warn',
                              'html': 'The three amounts are reproduced only to preserve the owner’s '
                                      'entries. They are not confirmed prices and must not be treated as '
                                      'combined quotes. See U01/U02/U33 on the <a '
                                      'href="flagged.html">Flagged for Review</a> page.'}]},
 'sources.html': {'title': 'Source ledger',
                  'eyebrow': 'Reference · current and historical evidence',
                  'h1': 'Source ledger',
                  'lede': 'Every source used or preserved by the dashboard, with tier, retrieval date, '
                          'status and the exact claim it supports. Current ranking sources were read '
                          '2026-11-08.',
                  'sections': [{'type': 'table', 'ref': 'source_ledger'},
                               {'type': 'prose',
                                'title': 'Evidence files',
                                'html': '<p><a href="data/canonical/evidence-2026-11-08.json">Current '
                                        'evidence extracts</a> · <a '
                                        'href="data/canonical/providers-2026-11-08.json">Structured provider '
                                        'records</a> · <a '
                                        'href="data/canonical/research-history-2026-11-07.json">Prior '
                                        'research snapshot</a> · <a '
                                        'href="data/canonical/site_data.json">Rendered site data</a>.</p>'},
                               {'type': 'callout',
                                'tone': 'info',
                                'html': '<strong>Tiers.</strong> official = government/official code '
                                        'publisher; manufacturer = product maker; company = business '
                                        'self-description; publisher = article’s own site; platform = '
                                        'review/directory; primary = project record. Historical sources are '
                                        'preserved but excluded from the current ranking. Dead sources are '
                                        'never linked from data rows.'}]},
 'verification.html': {'title': 'Verification',
                       'eyebrow': 'Audit · generated checks',
                       'h1': 'Verification',
                       'lede': 'Structural checks and a line-by-line row audit. A passing link check is not '
                               'independent proof of every factual claim.',
                       'sections': [{'type': 'verification_summary'},
                                    {'type': 'row_audit'},
                                    {'type': 'prose',
                                     'title': 'Method and limits',
                                     'html': '<ol class="tight"><li>Current ranking rows cite CSLB records '
                                             'and company pages read on 2026-11-08; extracts are saved in '
                                             'the <a href="data/canonical/evidence-2026-11-08.json">evidence '
                                             'ledger</a>.</li><li>Every generated table row has a Source '
                                             'column. The audit labels the strongest source tier and flags '
                                             'owner/publisher/platform/historical rows rather than calling '
                                             'them officially verified.</li><li>Internal pages, assets and '
                                             'anchors must resolve; external links must be in the ledger; '
                                             'dead sources must not be linked.</li><li>Blank verified cells '
                                             'require an UNVERIFIED flag. Privacy wording is swept from '
                                             'published text, including canonical data.</li><li>External '
                                             'availability is not continuously monitored. Yelp direct '
                                             'fetches returned HTTP 403; search excerpts are discovery '
                                             'evidence only.</li><li>GitHub Pages deployment is checked '
                                             'separately after merge and recorded in the coordination '
                                             'log.</li></ol>'},
                                    {'type': 'callout',
                                     'tone': 'warn',
                                     'html': 'Automated checks prove structure and provenance metadata, not '
                                             'contractor competence, job acceptance or legal applicability. '
                                             'Those remain on <a href="flagged.html">Flagged for '
                                             'Review</a>.'}]},
 'repo-review.html': {'title': 'Repo review',
                      'eyebrow': 'Audit · repository inventory and irregularities',
                      'h1': 'Repository review',
                      'lede': 'Current plumbing-dashboard audit plus a hashed inventory of preserved '
                              'source/artifact files. Unrelated GEMS content is not externally fact-checked '
                              'here.',
                      'sections': [{'type': 'table', 'ref': 'repo_review'},
                                   {'type': 'table', 'ref': 'repo_inventory'},
                                   {'type': 'prose',
                                    'title': 'Downloads and preserved work',
                                    'html': '<p><a href="data/canonical/repo_inventory.json">File inventory '
                                            'JSON</a> · <a href="data/canonical/repo_inventory.csv">File '
                                            'inventory CSV</a> · <a '
                                            'href="data/canonical/research-history-2026-11-07.json">Prior '
                                            'canonical snapshot</a> · <a '
                                            'href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md" '
                                            'target="_blank" rel="noopener noreferrer">COORDINATION.md</a> · '
                                            '<a '
                                            'href="https://github.com/karagemop466-tech/Korea7/blob/main/README.md" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">README</a>.</p><p>Archived parallel pages: <a '
                                            'href="bathtub-overflow/executive-summary.html">bathtub-overflow/</a> '
                                            '· <a href="docs/bath/index.html">docs/bath/</a> · <a '
                                            'href="docs/plumbing-index.html">docs/plumbing-index.html</a> · '
                                            '<a href="shortlist.html">shortlist.html</a> · <a '
                                            'href="verification-log.html">verification-log.html</a> · <a '
                                            'href="sf-overflow-audit/index.html">sf-overflow-audit/</a> · <a '
                                            'href="docs/index.html">legacy GEMS site</a>.</p>'},
                                   {'type': 'callout',
                                    'tone': 'warn',
                                    'html': 'Earlier pages may contain historical claims superseded by this '
                                            'refresh. Use the canonical root dashboard and current source '
                                            'ledger for the hiring decision.'}]},
 'flagged.html': {'title': 'Flagged for review',
                  'eyebrow': 'Audit · non-blocking review items',
                  'h1': 'Flagged for Review',
                  'lede': 'Unverified values, source conflicts and irregularities, each with source links. '
                          'These items do not block the site or merge.',
                  'sections': [{'type': 'table', 'ref': 'flagged'},
                               {'type': 'callout',
                                'tone': 'warn',
                                'html': 'To request a change, note the item ID (U01–U33). Blank verified '
                                        'cells were not filled by inference. Full evidence: <a '
                                        'href="sources.html">Source ledger</a>.'}]}}
