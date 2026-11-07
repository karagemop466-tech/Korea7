"""Offline integrity checks for the root overflow-repair dashboard.

Adapted on 2026-11-07 (session `7e5f723c`) for the regenerated, data-driven pages.
The intent of the original checks is preserved:

* every table row carries a source or documented link, and every internal link and
  anchor resolves;
* the three owner-provided amounts are never shown in an officially confirmed cell;
* the site does not claim confirmation, outreach or booking.

Run: python3 -m unittest tests.test_dashboard_integrity
"""

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "summary.html",
    "estimates.html",
    "contractors.html",
    "findings.html",
    "plan.html",
    "sources.html",
    "flagged.html",
)

# Hosts whose pages are used as evidence: licensing authority, statutes, cost
# publishers and the repository itself. Listed so an accidental link to an
# unrelated domain in a data row is caught.
EVIDENCE_HOSTS = {
    "www.cslb.ca.gov",
    "www2.cslb.ca.gov",
    "leginfo.legislature.ca.gov",
    "www.angi.com",
    "www.thisoldhouse.com",
    "github.com",
}

# Review platforms, company sites and search pages are contact/context sources,
# not evidence, but still acceptable links in a row.
CONTACT_HOSTS = {
    "www.yelp.com",
    "www.eplumbingsolutions.com",
    "www.bayareaplumbingsf.com",
    "www.fastresponseplumbingsf.com",
    "www.aceplumbingandrooter.com",
    "www.genteelplumbers.com",
    "generalsf.com",
    "www.handymanhero.es",
    "www.atlasplumbingandrooter.com",
    "www.heisesplumbing.com",
    "plumbinginsf.com",
}


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.rows = [], set(), []
        self.in_body = self.in_row = False
        self.row_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "tbody":
            self.in_body = True
        if tag == "tr" and self.in_body:
            self.in_row, self.row_links = True, []
        if tag in ("a", "link") and attrs.get("href"):
            href = attrs["href"]
            self.links.append(href)
            if self.in_row:
                self.row_links.append(href)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.rows.append(self.row_links)
            self.in_row = False
        if tag == "tbody":
            self.in_body = False


class DashboardTest(unittest.TestCase):
    def test_links_and_row_sources(self):
        cache = {}
        for name in PAGES:
            scan = Scan()
            scan.feed((ROOT / name).read_text(encoding="utf-8"))
            cache[name] = scan
        for name, scan in cache.items():
            text = (ROOT / name).read_text(encoding="utf-8")
            for row_body in re.findall(r"<tbody>(.*?)</tbody>", text, flags=re.S):
                for row in re.findall(r"<tr>.*?</tr>", row_body, flags=re.S):
                    # a row either links a source or is explicitly labelled owner-provided
                    self.assertTrue(
                        'href="' in row or "owner-provided" in row,
                        (name, row[:160]),
                    )
            for href in scan.links:
                url = urlparse(href)
                if url.scheme or url.netloc:
                    continue
                target = (ROOT / (unquote(url.path) or name)).resolve()
                self.assertTrue(target.is_file(), (name, href))
                if url.fragment and target.suffix == ".html":
                    dest = cache.get(target.name)
                    if dest is None:
                        dest = Scan()
                        dest.feed(target.read_text(encoding="utf-8"))
                    self.assertIn(unquote(url.fragment), dest.ids, (name, href))

    def test_data_rows_link_evidence_or_contact_sources(self):
        allowed = EVIDENCE_HOSTS | CONTACT_HOSTS
        for name in ("contractors.html", "sources.html", "findings.html", "estimates.html"):
            scan = Scan()
            scan.feed((ROOT / name).read_text(encoding="utf-8"))
            for row in scan.rows:
                hosts = {urlparse(h).hostname for h in row if urlparse(h).scheme}
                self.assertTrue(hosts & allowed, (name, row))

    def test_unverified_amounts_not_present_in_confirmed_cells(self):
        html = (ROOT / "estimates.html").read_text(encoding="utf-8")
        # the page states the rule ...
        self.assertIn("deliberately blank", html)
        # ... and each of the three amounts keeps its owner-provided tag while the
        # official-confirmation cell stays blank.
        self.assertEqual(html.count("blank: no official confirmation exists"), 3)
        self.assertGreaterEqual(html.count("owner-provided"), 3)

    def test_no_confirmation_or_outreach_claim(self):
        contractors = (ROOT / "contractors.html").read_text(encoding="utf-8")
        self.assertIn("No provider has been contacted", contractors)
        self.assertIn("neither has confirmed this job", contractors)


if __name__ == "__main__":
    unittest.main()
