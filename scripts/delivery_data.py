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
        c.PAGES[page]['sections'].insert(0, {'type': 'callout', 'tone': 'info', 'html': '<strong>November 10 update:</strong> top-three license/contact checks refreshed. Job-specific experience, one-contract ceiling restoration, price and availability remain unconfirmed. <a href="delivery.html">Read the dated verification and decision limits</a>.'})
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
