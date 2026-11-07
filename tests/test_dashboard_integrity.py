"""Offline integrity checks for the root overflow-repair dashboard.

Originally written by session be737440 for a leaner dashboard, extended by session
6a266fca for the shortlist/verification pages, and consolidated on 2026-11-07 by
session `7e5f723c` for the regenerated, data-driven pages. The intent of every
original rule is preserved:

* every table row carries a link to a source, or an explicit owner-provided /
  unverified marker;
* every internal link and internal anchor resolves;
* the three owner-provided amounts are never shown in an officially confirmed cell;
* the site never claims a provider was contacted or has confirmed the job.

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
    "shortlist.html",
    "estimates.html",
    "contractors.html",
    "findings.html",
    "plan.html",
    "verification.html",
    "sources.html",
    "flagged.html",
)

# Licensing authority, statutes, cost publishers and the repository itself.
EVIDENCE_HOSTS = {
    "www.cslb.ca.gov",
    "www2.cslb.ca.gov",
    "leginfo.legislature.ca.gov",
    "www.angi.com",
    "www.thisoldhouse.com",
    "github.com",
}

# Review platforms, company sites and search pages: contact/context, not evidence.
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
                    self.assertTrue(
                        'href="' in row or "owner-provided" in row or "unverified" in row.lower(),
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
        for name in ("contractors.html", "shortlist.html", "verification.html", "sources.html", "findings.html", "estimates.html"):
            scan = Scan()
            scan.feed((ROOT / name).read_text(encoding="utf-8"))
            for row in scan.rows:
                hosts = {urlparse(h).hostname for h in row if urlparse(h).scheme}
                internal = [h for h in row if not urlparse(h).scheme]
                # the verification log cross-references this site's own evidence pages
                # for a few flags; every other data row must reach an external source.
                self.assertTrue(
                    (hosts & allowed) or (name == "verification.html" and bool(internal)),
                    (name, row),
                )

    def test_unverified_amounts_not_present_in_confirmed_cells(self):
        html = (ROOT / "estimates.html").read_text(encoding="utf-8")
        self.assertIn("deliberately blank", html)
        self.assertEqual(html.count("blank: no official confirmation exists"), 3)
        self.assertGreaterEqual(html.count("owner-provided"), 3)

    def test_no_confirmation_or_outreach_claim(self):
        contractors = (ROOT / "contractors.html").read_text(encoding="utf-8")
        self.assertIn("No provider has been contacted", contractors)
        self.assertIn("neither has confirmed this job", contractors)


if __name__ == "__main__":
    unittest.main()
