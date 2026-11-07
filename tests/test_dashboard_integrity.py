"""Offline integrity checks for the root overflow-repair dashboard."""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'summary.html', 'estimates.html', 'contractors.html',
         'findings.html', 'sources.html', 'flagged.html')
OFFICIAL_HOSTS = {'www2.cslb.ca.gov', 'www.cslb.ca.gov', 'www.handymanhero.es',
                  'generalsf.com', 'www.eplumbingsolutions.com',
                  'www.bayareaplumbingsf.com', 'www.fastresponseplumbingsf.com',
                  'www.oatey.com', 'github.com'}

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.rows = [], set(), []
        self.in_body = self.in_row = False
        self.row_links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag == 'tbody': self.in_body = True
        if tag == 'tr' and self.in_body:
            self.in_row, self.row_links = True, []
        if tag in ('a', 'link') and attrs.get('href'):
            href = attrs['href']
            self.links.append(href)
            if self.in_row: self.row_links.append(href)
    def handle_endtag(self, tag):
        if tag == 'tr' and self.in_row:
            self.rows.append(self.row_links)
            self.in_row = False
        if tag == 'tbody': self.in_body = False

class DashboardTest(unittest.TestCase):
    def test_links_and_row_sources(self):
        for name in PAGES:
            with self.subTest(page=name):
                scan = Scan(); scan.feed((ROOT / name).read_text())
                for row in scan.rows:
                    self.assertTrue(any(urlparse(href).hostname in OFFICIAL_HOSTS for href in row), (name, row))
                for href in scan.links:
                    url = urlparse(href)
                    if url.scheme or url.netloc: continue
                    target = (ROOT / (unquote(url.path) or name)).resolve()
                    self.assertTrue(target.is_file(), (name, href))
                    if url.fragment and target.suffix == '.html':
                        dest = Scan(); dest.feed(target.read_text())
                        self.assertIn(unquote(url.fragment), dest.ids, (name, href))
    def test_unverified_amounts_not_present_in_confirmed_cells(self):
        html = (ROOT / 'estimates.html').read_text()
        self.assertIn('official-confirmed amount is intentionally blank', html)
        self.assertEqual(html.count('<td></td><td>Unverified owner report</td>'), 3)
    def test_no_confirmation_or_outreach_claim(self):
        contractors = (ROOT / 'contractors.html').read_text()
        self.assertIn('No provider has been contacted', contractors)
        self.assertIn('neither has confirmed this job', contractors)

if __name__ == '__main__':
    unittest.main()
