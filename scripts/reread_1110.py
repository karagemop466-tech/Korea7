"""2026-11-10 independent re-read: official plumbing-code exemption wording.

Adds one Reference subpage (`exempt-work.html`) that publishes the San
Francisco Plumbing Code §104.2 exempt-work list **verbatim** from the official
City PDF, plus the exact amendment scope printed on the same page. Until this
module existed the site only *pointed at* §104.2 ("link provided for manual
review of exemption wording"); the wording itself was never quoted.

Every statement on the page traces to the sources below. Nothing is inferred:
the one judgement the page makes (whether an item could cover this repair) is
labelled as this project's reading of the text, and job applicability is left
UNVERIFIED and flagged.
"""
from __future__ import annotations

import re

CODEX_PDF = 'https://media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf'

# --- sources -------------------------------------------------------------
# S96 already exists (same PDF, headline read 2026-11-08). These two entries
# record this session's independent 2026-11-10 re-reads so they are not
# confused with earlier snapshots.
NEW_SOURCES = {
    'S112': {
        'label': 'CSLB — License Detail #757796 re-read 2026-11-10',
        'publisher': 'California Contractors State License Board',
        'url': ('https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/'
                'LicenseDetail.aspx?LicNum=757796'),
        'tier': 'official',
        'status': 'verified',
        'checked': '2026-11-10',
        'supports': 'Bay Area Plumbing, business phone (415) 668-8000, C36 only, current and active',
        'note': ('Independent 2026-11-10 re-read for this session; the record printed the '
                 'November 9 database timestamp.'),
    },
    'S113': {
        'label': 'CSLB — License Detail #1024971 re-read 2026-11-10',
        'publisher': 'California Contractors State License Board',
        'url': ('https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/'
                'LicenseDetail.aspx?LicNum=1024971'),
        'tier': 'official',
        'status': 'verified',
        'checked': '2026-11-10',
        'supports': ("Joseph Tinsley dba Fast Response Plumbing and Rooter, C36 only, current and "
                     "active, workers' compensation policy expiring 2026-12-18"),
        'note': ('Independent 2026-11-10 re-read for this session; the record printed the '
                 'November 9 database timestamp.'),
    },
}

# --- verbatim §104.2 text (official PDF, fetched 2026-11-10, pages 4-5) ---
# PDF line breaks are presentation artefacts and are collapsed; wording unchanged.
EXEMPT_ITEMS = [
    'Repair of leaks not requiring cutting into or removing piping.',
    'Unstopping of traps, sewers, vents or waste pipes not requiring cutting into or removal of '
    'traps or piping.',
    'Replacement, repair or maintenance of faucets, angle stops, hose bibbs or roof drain not '
    'requiring cutting into or removal of piping.',
    'Replacement of toilets except in structures with alternate water piping.',
    'Replacement of furnace filters.',
    'Removal of drainage, water or gas piping from a building when the water supply, gas and '
    'drainage lines have been disconnected in an approved manner under a permit.',
    'Work involved in setting up for display of plumbing fixtures or appliances, when not '
    'connected to any supply or drainage lines, in a sales establishment.',
    'Replacement of water conservation devices not requiring cutting into or removal of piping.',
    'Work performed in buildings or structures owned and occupied by the State and Federal '
    'governments.',
]

# (item number, could-it-cover-this-repair, why)
EXEMPT_READING = [
    ('1', 'No',
     'A seized trip lever that must be freed or removed is not a leak repair, and concealed '
     'waste-and-overflow work is the situation sf.gov describes as needing a permit.'),
    ('2', 'No',
     'Covers unstopping a blocked trap, sewer, vent or waste pipe without cutting, not freeing, '
     'adjusting or replacing the trip-lever linkage.'),
    ('3', 'No',
     'Names faucets, angle stops, hose bibbs and roof drains only. The trip lever, overflow plate '
     'and waste-and-overflow assembly are not listed.'),
    ('4', 'No', 'Toilet replacement only.'),
    ('5', 'No', 'Furnace filters only.'),
    ('6', 'No',
     'Removing piping from a building after disconnection under an approved permit, not repairing '
     'or replacing a fixture assembly in place.'),
    ('7', 'No', 'Display fixtures not connected to supply or drainage lines only.'),
    ('8', 'No', 'Water conservation devices not requiring pipe cutting only.'),
    ('9', 'No', 'State- and Federally-owned and occupied buildings only.'),
]

AMENDMENT_TEXT = ('… 104.2 Replace Section 104.2(1) and the first paragraph of Section 104.2(2) '
                  'as follows:')
AMENDMENT_MEANING = (
    'The City’s amendment replaces only item (1), item (2) and the first paragraph of item (2). '
    'Items (3)–(9) above are the model code text as printed in the same official document; that '
    'document does not show they were amended locally.'
)
FEE_TEXT = ('104.5 Permit Fees. … The replacement of a plumbing fixture or a gas appliance without '
            'a change in drainage, piping or venting shall not require the payment of permit '
            'issuance fee.')
FEE_MEANING = (
    'A <em>fee</em> provision, not an exemption from the permit itself. It settles nothing about '
    'whether this repair needs a permit.'
)


def _readings():
    by_num = {num: (conclusion, why) for num, conclusion, why in EXEMPT_READING}
    rows = []
    for i, text in enumerate(EXEMPT_ITEMS, 1):
        conclusion, why = by_num[str(i)]
        rows.append({
            'cells': [str(i), '<q>%s</q>' % text, '%s <small>(this project’s reading)</small>'
                      % conclusion, why],
            'src': ['S96'],
        })
    return rows


TABLES = {
    'exempt_list': {
        'title': 'San Francisco Plumbing Code §104.2 — exempt work, verbatim (9 items)',
        'columns': ['Item', 'Official text (verbatim)', 'Could it cover this repair?',
                    'Why / why not', 'Source'],
        'rows': _readings(),
        'caption': (
            'Transcribed 2026-11-10 from the City and County of San Francisco publication '
            '<a href="%s" target="_blank" rel="noopener noreferrer">2025 San Francisco Plumbing '
            'Code (PDF)</a>, pages 4–5. Wording is unchanged; only PDF line breaks are collapsed. '
            'The third and fourth columns are this project’s reading of the quoted text, not a '
            'determination — the Department of Building Inspection decides applicability for a '
            'specific job.' % CODEX_PDF
        ),
    },
    'amendment_scope': {
        'title': 'What the City changed in §104.2 — and a fee rule often misread as an exemption',
        'columns': ['Official wording on the page', 'What it establishes', 'Verification', 'Source'],
        'rows': [
            {
                'cells': ['<q>%s</q>' % AMENDMENT_TEXT, AMENDMENT_MEANING,
                          'official — City PDF, read 2026-11-10'],
                'src': ['S96'],
            },
            {
                'cells': ['<q>%s</q>' % FEE_TEXT, FEE_MEANING,
                          'official — City PDF, read 2026-11-10'],
                'src': ['S96'],
            },
        ],
        'caption': (
            'Both quotations come from the same official PDF read on 2026-11-10. No interpretation '
            'of any individual job’s circumstances is recorded here.'
        ),
    },
    'source_basis': {
        'title': 'Official pages read for this page (2026-11-10)',
        'columns': ['Official page', 'What it says', 'Read', 'Source'],
        'rows': [
            {
                'cells': [
                    '<a href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" '
                    'target="_blank" rel="noopener noreferrer">sf.gov — Apply for a plumbing and '
                    'mechanical permit</a>',
                    '<q>You need a permit before cutting into or replacing pipes, particularly '
                    'pipes that will be covered by a wall or buried in the ground.</q> The page '
                    'then points to §104.2 for exemptions.',
                    '2026-11-10',
                ],
                'src': ['S01'],
            },
            {
                'cells': [
                    '<a href="https://www.sf.gov/information--check-if-your-construction-project-'
                    'needs-permit" target="_blank" rel="noopener noreferrer">sf.gov — Check if your '
                    'construction project needs a permit</a>',
                    '<q>Minor repairs to existing interior plaster or wallboard, unless they are '
                    'required for fire protection.</q> Listed as work that does not need a '
                    '<em>building</em> permit — a separate question from the plumbing permit above.',
                    '2026-11-10',
                ],
                'src': ['S02'],
            },
            {
                'cells': [
                    '<a href="%s" target="_blank" rel="noopener noreferrer">2025 San Francisco '
                    'Plumbing Code (PDF)</a>' % CODEX_PDF,
                    'Prints the nine exempt-work items above and states which of them the City '
                    'amended (§104.2(1) and the first paragraph of §104.2(2)).',
                    '2026-11-10',
                ],
                'src': ['S96'],
            },
        ],
        'caption': (
            'None of these official pages contains a plumbing-specific exemption for repairing or '
            'replacing a trip-lever waste-and-overflow assembly. That is a statement about the text '
            'of the code, not a determination for any individual job.'
        ),
    },
}

PERMIT_CAPTION_ADDITION = (
    ' The exempt-work list that sf.gov points to is transcribed word for word on the '
    '<a href="exempt-work.html">Code exemptions</a> page.'
)


def next_flag_id(c) -> str:
    """Return the next free U-number for this build."""
    highest = 0
    for row in c.TABLES['flagged']['rows']:
        m = re.fullmatch(r'U(\d+)', str(row['cells'][0]))
        if m:
            highest = max(highest, int(m.group(1)))
    return 'U%d' % (highest + 1)


def integrate(c):
    c.SOURCES.update(NEW_SOURCES)
    for tid, spec in TABLES.items():
        c.TABLES[tid] = spec

    c.PAGES['exempt-work.html'] = {
        'title': 'Code exemptions',
        'eyebrow': 'Reference · official code text · read 2026-11-10',
        'h1': 'What the plumbing code exempts — the actual wording',
        'lede': (
            'SF.gov says a permit is needed before cutting into or replacing pipes, and points to '
            'San Francisco Plumbing Code §104.2 for the exemptions. This page publishes that '
            'exempt-work list word for word from the City’s own PDF and shows what the City '
            'amended — so the test can be checked instead of trusted.'
        ),
        'sections': [
            {
                'type': 'callout',
                'tone': 'warn',
                'html': (
                    '<strong>Scope of this page.</strong> It reports official text. It contains no '
                    'instruction, request or recommendation about obtaining or not obtaining a '
                    'permit, and it records no private project rationale. Only the San Francisco '
                    'Department of Building Inspection can determine whether a specific job needs a '
                    'permit; sf.gov lists the Permit Center help desk and permitsf@sfgov.org as '
                    'contacts. Nothing here is legal advice.'
                ),
            },
            {
                'type': 'prose',
                'title': 'Why this page exists',
                'html': (
                    '<p>Until 2026-11-10 this site linked §104.2 but quoted none of it — the '
                    'permits table said “link provided for manual review of exemption wording”. '
                    'The official wording was read and transcribed on 2026-11-10, so the exemption '
                    'test can now be checked line by line. The permits page keeps its neutral '
                    'wording; the quoted text lives here.</p>'
                ),
            },
            {'type': 'table', 'title': 'The nine exempt-work items, verbatim', 'ref': 'exempt_list'},
            {'type': 'table', 'title': 'Amendment scope — and a fee rule often misread as an exemption',
             'ref': 'amendment_scope'},
            {'type': 'table', 'title': 'Official pages read for this page', 'ref': 'source_basis'},
            {
                'type': 'prose',
                'title': 'What this does and does not settle',
                'html': (
                    '<p><strong>Established:</strong> the nine exempt-work items in §104.2, the '
                    'fact that the City amended only items (1) and (2), and the separate sf.gov '
                    'wording on cutting into pipes and on patching interior wallboard.</p>'
                    '<p><strong>Not established:</strong> whether the repair in this project falls '
                    'inside or outside any exemption. No inspection has been performed, the '
                    'assembly model and the extent of any cutting are unknown, and the answer '
                    'belongs to the DBI, not to this site. That question stays open and is carried '
                    'on the <a href="flagged.html">Flagged for Review</a> page.</p>'
                ),
            },
        ],
    }

    # Navigation: place it beside the permits page in the Reference group.
    for group in c.NAV:
        if group['group'] == 'Reference':
            hrefs = [href for href, _ in group['links']]
            if 'exempt-work.html' not in hrefs:
                idx = hrefs.index('permits.html') + 1 if 'permits.html' in hrefs else len(group['links'])
                group['links'].insert(idx, ('exempt-work.html', 'Code exemptions'))
            break

    # Permits page: add the newly read official text as a row, and point the
    # old "link only" row at the published wording.
    rows = c.TABLES['permits']['rows']
    if not any(r['cells'][0].startswith('Exempt-work list') for r in rows):
        rows.insert(1, {
            'cells': [
                'Exempt-work list (§104.2) — now quoted in full',
                'The nine exempt-work items are transcribed verbatim on the Code exemptions page, '
                'with the City’s amendment scope and the separate fee rule in §104.5',
                'Lets the exemption test be checked line by line instead of taken on trust',
                'official — City PDF',
            ],
            'src': ['S96'],
        })
    for row in rows:
        if row['cells'][0] == 'Exempt-work pointer':
            row['cells'][2] = 'Full wording now published on the Code exemptions page'
            if 'S96' not in row['src']:
                row['src'].append('S96')
    if PERMIT_CAPTION_ADDITION not in c.TABLES['permits']['caption']:
        c.TABLES['permits']['caption'] = c.TABLES['permits']['caption'].rstrip() + PERMIT_CAPTION_ADDITION

    # Findings: record what today's read added.
    if not any(r['cells'][0] == 'F17' for r in c.TABLES['findings']['rows']):
        c.TABLES['findings']['rows'].append({
            'cells': [
                'F17',
                'The §104.2 exempt-work list contains no plumbing-specific exemption for repairing '
                'or replacing a trip-lever waste-and-overflow assembly',
                'Nine exempt-work items transcribed verbatim from the City PDF on 2026-11-10; the '
                'only items the City amended are (1) and (2); §104.5 is a fee rule, not an exemption',
                'official text quoted / job applicability still UNVERIFIED',
            ],
            'src': ['S96', 'S01'],
        })

    # Flagged for review: the open question this page cannot close.
    flag_id = next_flag_id(c)
    if not any('Permit exemption for this exact repair' in str(r['cells'][1])
               for r in c.TABLES['flagged']['rows']):
        c.TABLES['flagged']['rows'].append({
            'cells': [
                flag_id,
                'Permit exemption for this exact repair is not determined',
                'The §104.2 list has no item covering repair or replacement of a trip-lever '
                'waste-and-overflow assembly, but no inspection has been performed and the extent '
                'of any cutting is unknown. This site states official text only and does not '
                'conclude that a permit is or is not required.',
                'Ask SF DBI (Permit Center help desk, permitsf@sfgov.org) about the exact scope '
                'before work is scheduled.',
                c.UNVERIFIED,
            ],
            'src': ['S96', 'S01'],
        })

    c.META['session'] = 'arena/56d961a8-korea7'
