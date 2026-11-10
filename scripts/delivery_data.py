"""Scoped November 10 source-read supplement; no changes to ranking inputs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def integrate(c):
    d = json.loads((ROOT / 'data/canonical/delivery-2026-11-10.json').read_text())
    refreshed = {}
    for i, sid in enumerate(d['source_ids'], 105):
        new_id = 'S' + str(i)
        c.SOURCES[new_id] = dict(c.SOURCES[sid], checked=d['checked_date'], label=c.SOURCES[sid]['label'] + ' — November 10 selected-field read')
        refreshed[sid] = new_id
    c.TABLES['delivery_checks'] = {
        'caption': 'Selected official fields re-read November 10; historical ranking inputs unchanged.',
        'columns': ['Business / record', 'Official facts re-read', 'Source timestamp / limits', 'Job price', 'Verification', 'Source'],
        'rows': [
            {'cells': [r['business'], r['facts'], r['record_timestamp'] + ' · ' + r['limits'], c.BLANK + ' ' + c.UNVERIFIED, 'Direct read 2026-11-10'], 'src': [refreshed[sid] for sid in r['sources']]}
            for r in d['checks']
        ],
    }
    c.PAGES['delivery.html'] = {
        'title': 'Latest verification', 'eyebrow': 'Dated evidence supplement · 2026-11-10',
        'h1': 'Latest verification & decision limits',
        'lede': 'Three leading candidates rechecked against official records and their own sites. This is a source audit, not a booking or a contractor endorsement.',
        'sections': [
            {'type': 'callout', 'tone': 'warn', 'html': '<strong>No provider is confirmed for this job.</strong> Exact stuck-linkage experience, a safe access route, ceiling restoration under one contract, occupied-unit precautions, total price and availability remain UNVERIFIED. No outreach or booking was performed.'},
            {'type': 'table', 'title': 'Official pages read on November 10', 'ref': 'delivery_checks'},
            {'type': 'prose', 'title': 'Executive decision', 'html': '<p>Start with <strong>Ace Plumbing &amp; Rooter — (415) 824-6444</strong>: the existing license-based model ranks it first, and its own site describes San Francisco HOA/property-manager work. Genteel is the next licensing-model candidate; use its published office line <strong>(415) 465-5853</strong>, while retaining the differing CSLB line in the contact directory. Handyman Heroes advertises both plumbing and construction, and carries a drywall-patching testimonial on its own site, but its record has a complaint-disclosure notice. These are reasons to shortlist, not proof that any firm can free the seized assembly safely.</p><p><a href="ranking.html">Full ranking, criterion weights and reasoning</a> · <a href="contacts.html">Official phones and business links</a> · <a href="estimates.html">Three owner-reported estimates and scope differences</a></p>'},
            {'type': 'prose', 'title': 'How to interpret the ranking and cost', 'html': '<p>The numerical ranking measures the disclosed license-record criteria; it does not measure repair skill or predict success. San Francisco address and tenure are model preferences, not proof of competence. Workers’ compensation exemptions do not by themselves establish unlawful conduct. A company-hosted testimonial is not an independently verified project record.</p><p>No job-specific official price was confirmed in these reads. Cost therefore remains blank and UNVERIFIED. The three owner estimates describe different scopes and cannot be treated as competing all-inclusive bids. No ceiling opening size, assembly material, restoration cost or work duration is inferred.</p>'},
            {'type': 'prose', 'title': 'Verification boundary', 'html': '<p>The CSLB pages returned November 9 database timestamps during November 10 reads; those timestamps are preserved above. Other contractor facts retain their historical read dates. Automated row/link checks do not prove external link reachability, contractor quality or every factual statement. <a href="flagged.html">Flagged for Review</a> contains remaining evidence gaps. <a href="data/canonical/delivery-2026-11-10.json">Download this dated evidence transcription</a>.</p>'},
        ],
    }
    c.NAV[-1]['links'].insert(0, ('delivery.html', 'Latest verification'))
    for page in ('index.html', 'summary.html'):
        c.PAGES[page]['sections'].insert(0, {'type': 'callout', 'tone': 'info', 'html': '<strong>November 10 update:</strong> all sixteen CSLB license records were fetched again and compared field by field — <strong>16 matched, 0 corrections</strong>; the official SF permit and exemption pages, B&amp;P §7048 and the C-36 / B / C-9 classification definitions also match. Job-specific experience, one-contract ceiling restoration, price and availability remain unconfirmed, and Yelp still blocks automated reads. <a href="delivery.html">Read the dated verification and decision limits</a>.'})
    c.TABLES['flagged']['rows'].append({
        'cells': ['U45', 'Freshness and ranking limits', 'Only six top-three official/company pages were re-read November 10. Other checks retain historical dates; the license-based score is not a repair-skill rating.', 'Use the dated supplement; obtain job-specific written scope and current availability before selecting a contractor.', c.UNVERIFIED],
        'src': ['S11', 'S64', 'S10'],
    })
    c.META['session'] = 'arena/ccf3d3c5-korea7'
    for block in c.PAGES['index.html']['sections']:
        if block['type'] == 'cards':
            for card in block['items']:
                if card['k'] == 'Flagged for review':
                    card['v'] = str(len(c.TABLES['flagged']['rows']))

    # Independent scope-fit supplement; preserve historical numerical model inputs.
    c.SOURCES['S111'] = {
        'label': 'Handyman Heroes — construction services',
        'publisher': 'Handyman Heroes Inc',
        'url': 'https://www.handymanhero.es/construction-services/',
        'tier': 'company', 'status': 'verified', 'checked': '2026-11-10',
        'supports': 'Advertises bathroom remodels and publishes 1-844-382-4376.',
        'note': 'Direct selected-field read by arena/fd9508fc-korea7. Company marketing, not confirmation of seized overflow work, a one-contract ceiling restoration commitment, price or availability. Page focuses on South San Francisco; the homepage separately advertises SF County.',
    }
    c.TABLES['scope_fit_closeout'] = {
        'caption': 'Scope-fit analysis, not a replacement for the licensing-model ranking. Independent selected-field reads November 10.',
        'columns': ['Candidate', 'Official evidence', 'Decision analysis', 'All-in price', 'Source'],
        'rows': [
            {'cells': ['Ace Plumbing & Rooter · (415) 824-6444', 'Active #829071; B and C36; company advertises SF residential and HOA/property-manager service.', 'First diagnostic shortlist under the existing license model. Occupied-property marketing is relevant, but safe extraction and ceiling restoration are not confirmed.', c.BLANK + ' ' + c.UNVERIFIED], 'src': ['S105', 'S108']},
            {'cells': ['Genteel Plumbers · (415) 465-5853', 'Official contact page publishes this office line and San Francisco location.', 'Alternative contact from the existing shortlist. A contact-page read alone does not establish drywall capability or exact repair experience. Retain the different CSLB line in the directory.', c.BLANK + ' ' + c.UNVERIFIED], 'src': ['S109', 'S106']},
            {'cells': ['Handyman Heroes · (844) 382-4376', 'Homepage advertises plumbing and construction, with a company-hosted drywall-patching testimonial; construction page advertises bathroom remodels.', 'Potential combined-trade fit worth evaluating alongside Ace, not proof of an all-in-one commitment. Existing complaint-notice and license-marketing discrepancies remain on Flagged for Review. No exact overflow project verified.', c.BLANK + ' ' + c.UNVERIFIED], 'src': ['S110', 'S111', 'S107']},
        ],
    }
    c.PAGES['delivery.html']['sections'].append({
        'type': 'table', 'title': 'Practical scope-fit comparison', 'ref': 'scope_fit_closeout',
    })
    c.PAGES['delivery.html']['sections'].append({
        'type': 'prose', 'title': 'Independent corroboration boundary',
        'html': '<p>The independent close-out checked five selected source pages, not every historical fact. The Genteel and Handyman Heroes CSLB rows above belong to the earlier dated check, not this independent read. <a href="data/canonical/closeout-2026-11-10.json">Read the exact fields corroborated</a>. No testimonial reviewed establishes the complete combination of seized overflow extraction, occupied-unit work and ceiling restoration. No contractor has been contacted, booked or confirmed for this project.</p>',
    })

    # ------------------------------------------------------------------
    # G1 full-record re-verification by arena/33211fbf-korea7 (2026-11-10).
    # Every one of the 16 canonical CSLB records was fetched again and compared
    # field-by-field. Nothing below is inferred; a field the live page did not
    # print would have been blank and flagged.
    # ------------------------------------------------------------------
    full = json.loads((ROOT / 'data/canonical/verification-2026-11-10-g1.json').read_text())

    c.SOURCES['S112'] = {
        'label': 'Live re-verification record — 16 CSLB records, 2026-11-10',
        'publisher': 'This project (transcription of official CSLB page reads)',
        'url': 'data/canonical/verification-2026-11-10-g1.json',
        'tier': 'primary', 'status': 'verified', 'checked': '2026-11-10',
        'supports': 'Field-by-field comparison of all sixteen CSLB License Detail records against the committed dataset: 16 matched, 0 mismatched.',
        'note': 'Transcription of live reads by arena/33211fbf-korea7. Reviewer script scripts/audit_live_sources.py repeats the comparison where outbound HTTP is available.',
    }
    c.SOURCES['S113'] = {
        'label': 'CSLB — C-9 Drywall classification',
        'publisher': 'California Contractors State License Board (CSLB)',
        'url': 'https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9',
        'tier': 'official', 'status': 'verified', 'checked': '2026-11-10',
        'supports': 'Drywall contractor lay out and install gypsum wallboard assemblies, including nonstructural metal framing, taping and texturing.',
        'note': 'Read directly 2026-11-10. Classification text only; does not establish any firm\'s willingness or ability to take this job.',
    }

    all_in_one = [r for r in full['cslb_records']['per_record']
                  if 'C36' in r['classes'] and 'B' in r['classes'].replace(' ', '')]
    rows = []
    for r in full['cslb_records']['per_record']:
        rows.append({
            'cells': [
                '%s — CSLB #%s' % (r['name'], r['license']),
                '%s; classes %s; phone %s; expires %s; entity %s; issued %s; %s' % (
                    r['status'], r['classes'], r['phone'], r['expire'], r['entity'],
                    r['issue'], r['wc']),
                'Data current as of 11/9/2026 · license record only; no job acceptance, '
                'no price, no acknowledgement of this project.' + (
                    ' Additional status: %s.' % r['additional_status'] if r.get('additional_status') else ''),
                c.BLANK + ' ' + c.UNVERIFIED,
                'Match — 2026-11-10',
            ],
            'src': ['S112'],
        })
    c.TABLES['delivery_full_recheck'] = {
        'caption': 'All sixteen canonical CSLB records fetched again on 2026-11-10 and compared to the committed dataset. '
                   '0 mismatches. Job price is blank everywhere because no official source publishes one.',
        'columns': ['Licensee', 'Official fields as re-read', 'Record timestamp / limits', 'Job price', 'Verification', 'Source'],
        'rows': rows,
    }

    c.TABLES['delivery_definition_check'] = {
        'caption': 'Classification and statutory text re-read 2026-11-10 to confirm the rules the ranking and the permits page rely on.',
        'columns': ['Rule or definition', 'What the official page states', 'How this project uses it', 'Verified', 'Source'],
        'rows': [
            {'cells': ['C-36 Plumbing', full['classification_definitions'][0]['confirmed'],
                       'Establishes that concealed waste-and-overflow work is within the plumbing trade.', '2026-11-10'], 'src': ['S05']},
            {'cells': ['B General Building (B&P §7057)',
                       full['classification_definitions'][1]['confirmed'],
                       'A B licence alone does not authorise plumbing trade work; it needs the specialty class or a subcontract. This is why "B + C-36 on one licence" is the all-in-one test rather than "B alone".',
                       '2026-11-10'], 'src': ['S83']},
            {'cells': ['C-9 Drywall', full['classification_definitions'][2]['confirmed'],
                       'Defines the separate-restoration route when the ceiling is opened.', '2026-11-10'], 'src': ['S113']},
            {'cells': ['SF plumbing-permit rule', '“You need a permit before cutting into or replacing pipes, particularly pipes that will be covered by a wall or buried in the ground.” Contractor classes accepted: C4, C16, C20, C36, C54, B, A.',
                       'Neutral reporting only. This site takes no position on whether a permit is obtained for this job.', '2026-11-10'], 'src': ['S01']},
            {'cells': ['SF permit-exempt work', '“Minor repairs to existing interior plaster or wallboard, unless they are required for fire protection” is listed as not needing a permit.',
                       'Reported as published. Whether a ceiling opening for concealed plumbing falls inside it is not determined here.', '2026-11-10'], 'src': ['S02']},
            {'cells': ['B&P §7048', 'Exempts only work under $1,000 aggregate that is casual, minor or inconsequential AND does not require a building permit (as amended by AB 1170, effective 2026-01-01).',
                       'Explains why older "$500" references are out of date. Not applied to this job as a conclusion.', '2026-11-10'], 'src': ['S13']},
        ],
    }

    c.PAGES['delivery.html']['sections'].append({'type': 'table',
        'title': 'Full re-verification — all 16 CSLB records, 2026-11-10',
        'ref': 'delivery_full_recheck'})
    c.PAGES['delivery.html']['sections'].append({'type': 'table',
        'title': 'Rules and definitions behind the ranking and the permits page',
        'ref': 'delivery_definition_check'})
    c.TABLES['flagged']['rows'].append({
        'cells': ['U46', 'Live re-verification scope — 2026-11-10',
                  'All sixteen CSLB records and four official rule/definition pages were re-read and match. Yelp returned HTTP 403 again, so no rating or review count was read; Angi, BuildZoom, Thumbtack, BBB, ten company websites, publisher cost benchmarks and manufacturer literature keep their 2026-11-07/08 read dates.',
                  'Treat non-CSLB figures as of their stated read date. Re-open any review platform manually before relying on it, and re-check a licence on CSLB on the hire date.',
                  c.UNVERIFIED],
        'src': ['S112', 'S11', 'S01'],
    })
    c.TABLES['flagged']['rows'].append({
        'cells': ['U47', 'Nobody has been contacted or booked',
                  'No provider has been asked whether it can free a seized trip lever from above, open a tenant-occupied storage-unit ceiling, restore it under one contract, or what it would charge. Every price cell on this site is blank.',
                  'Use the ranked shortlist and the Contacts page to request one written fixed-price scope per firm covering the from-above attempt, below access, ceiling cut/patch/finish and a fill-and-drain test.',
                  c.UNVERIFIED],
        'src': ['S88', 'S91'],
    })

    c.PAGES['delivery.html']['sections'].append({'type': 'prose',
        'title': 'What this re-verification does and does not establish',
        'html': '<p>Every one of the sixteen license records was fetched again on 2026-11-10 and compared to the stored values field by field: <strong>16 matched, 0 differed, 0 corrections were needed</strong>. The official pages printed 11/9/2026 database timestamps; those are reproduced exactly and not rewritten to today. '
                'Separately, the SF plumbing-permit page, the SF permit-exemptions page, B&P §7048, and the CSLB C-36, B and C-9 classification definitions were read again and match the text this site already publishes.</p>'
                '<p><strong>It does not establish</strong> that any firm can free a seized trip lever without opening the ceiling, has done this exact repair, will take a tenant-occupied unit, will restore the ceiling under one contract, or will do it for any particular price. '
                '<strong>Yelp still returned HTTP 403</strong> to every automated fetch on 2026-11-10, so no rating, review count or badge was read today and none is restated. Angi, BuildZoom, Thumbtack, BBB, the remaining company websites, the publisher cost benchmarks and the manufacturer literature keep their earlier read dates and are not relabelled as rechecked.</p>'
                '<p><a href="data/canonical/verification-2026-11-10-g1.json">Download the exact fields compared</a>.</p>',
    })
    c.META['session'] = 'arena/33211fbf-korea7'
