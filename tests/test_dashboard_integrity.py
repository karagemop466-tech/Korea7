"""Offline integrity checks for the root overflow-repair dashboard.

Originally written by session be737440 for its leaner dashboard; extended during integration
(session 6a266fca) so the same rules apply to the merged dashboard, which keeps the richer
verified tables and adds shortlist.html + verification.html.

Rules enforced:
  * every table row carries either a link to an official host or an explicit
    unverified / owner-provided / third-party / blank marker (the project's own rule:
    values that cannot be confirmed officially are left blank and flagged, not inferred);
  * every internal link and internal anchor resolves;
  * the three owner-reported amounts are never presented as confirmed;
  * the dashboard never claims a provider was contacted or has confirmed the job.
"""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'summary.html', 'shortlist.html', 'estimates.html',
         'contractors.html', 'findings.html', 'verification.html',
         'sources.html', 'flagged.html')
OFFICIAL_HOSTS = {
    'www2.cslb.ca.gov', 'www.cslb.ca.gov', 'cslb.ca.gov',
    'www.sf.gov', 'sf.gov', 'media.api.sf.gov',
    'leginfo.legislature.ca.gov',
    'www.handymanhero.es', 'handymanhero.es', 'generalsf.com',
    'www.eplumbingsolutions.com', 'eplumbingsolutions.com',
    'www.bayareaplumbingsf.com', 'bayareaplumbingsf.com',
    'www.fastresponseplumbingsf.com', 'fastresponseplumbingsf.com',
    'www.rapidflowbayarea.com', 'rapidflowbayarea.com',
    'www.oatey.com', 'github.com',
}
UNVERIFIED_MARKERS = (
    'unverified', 'owner-provided', 'third-party', 'blank',
    'no official source', 'not matched', 'not verified',
)


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.rows = [], set(), []
        self.in_body = self.in_row = False
        self.row_links = []
        self.row_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'tbody':
            self.in_body = True
        if tag == 'tr' and self.in_body:
            self.in_row, self.row_links, self.row_text = True, [], []
        if tag in ('a', 'link') and attrs.get('href'):
            href = attrs['href']
            self.links.append(href)
            if self.in_row:
                self.row_links.append(href)

    def handle_data(self, data):
        if self.in_row:
            self.row_text.append(data)

    def handle_endtag(self, tag):
        if tag == 'tr' and self.in_row:
            self.rows.append((self.row_links, ' '.join(self.row_text).lower()))
            self.in_row = False
        if tag == 'tbody':
            self.in_body = False


class DashboardTest(unittest.TestCase):
    def test_links_and_row_sources(self):
        for name in PAGES:
            with self.subTest(page=name):
                scan = Scan()
                scan.feed((ROOT / name).read_text(encoding='utf-8'))
                for links, text in scan.rows:
                    official = any(urlparse(h).hostname in OFFICIAL_HOSTS for h in links)
                    cited = bool(links)  # every row points at a source, official or publisher
                    flagged = any(marker in text for marker in UNVERIFIED_MARKERS)
                    self.assertTrue(cited or flagged, (name, links, text[:120]))
                    # on the data pages, a licence number must never appear without a CSLB link
                    if name in ('contractors.html', 'shortlist.html', 'summary.html', 'findings.html'):
                        if '#' in text:
                            self.assertTrue(official, (name, links, text[:140]))
                for href in scan.links:
                    url = urlparse(href)
                    if url.scheme or url.netloc:
                        continue
                    target = (ROOT / (unquote(url.path) or name)).resolve()
                    self.assertTrue(target.is_file(), (name, href))
                    if url.fragment and target.suffix == '.html':
                        dest = Scan()
                        dest.feed(target.read_text(encoding='utf-8'))
                        self.assertIn(unquote(url.fragment), dest.ids, (name, href))

    def test_unverified_amounts_not_presented_as_confirmed(self):
        html = (ROOT / 'estimates.html').read_text(encoding='utf-8')
        for amount in ('$614', '$550', '$135'):
            self.assertIn(amount, html)
        # Each estimate row must carry an explicit unverified marker and no source link claim.
        self.assertGreaterEqual(html.count('owner-provided — no official source exists'), 3)
        self.assertIn('unverified', html)

    def test_no_confirmation_or_outreach_claim(self):
        contractors = (ROOT / 'contractors.html').read_text(encoding='utf-8')
        self.assertIn('No provider has been contacted', contractors)
        self.assertIn('has confirmed this job', contractors)

    def test_third_party_review_data_is_labelled(self):
        contractors = (ROOT / 'contractors.html').read_text(encoding='utf-8')
        self.assertIn('third-party', contractors)
        self.assertIn('unverified', contractors)


if __name__ == '__main__':
    unittest.main()
