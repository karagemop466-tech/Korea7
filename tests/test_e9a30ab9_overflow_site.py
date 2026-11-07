"""Offline integrity tests for the overflow-trip-lever-e9a30ab9 dashboard.

Run with:  python3 -m unittest tests/test_e9a30ab9_overflow_site.py -v

These tests enforce the project's verification rules on the generated site:
  * the committed output matches the generator (no hand edits, no drift);
  * every <tbody> row links to an official source;
  * every blank cell is explicitly flagged UNVERIFIED, and no requester-reported
    estimate amount appears inside any table body;
  * all internal links and anchors resolve, all external links are https and on
    the documented host allow-list;
  * the JSON data exports agree with the rendered tables;
  * the private/internal wording excluded from publication never appears.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "overflow-trip-lever-e9a30ab9"
GEN = REPO / "scripts" / "build_e9a30ab9_overflow_site.py"
sys.path.insert(0, str(GEN.parent))
import build_e9a30ab9_overflow_site as gen  # noqa: E402

PAGES = [
    "index.html", "executive-summary.html", "requirements.html", "estimates.html", "contractors.html",
    "compliance.html", "repo-review.html", "verification.html", "sources.html", "flagged-for-review.html",
]
OFFICIAL_HOSTS = {
    "www2.cslb.ca.gov", "www.cslb.ca.gov", "leginfo.legislature.ca.gov", "www.sf.gov", "github.com",
    "www.oatey.com", "generalsf.com", "www.handymanhero.es", "www.aceplumbingandrooter.com",
}
ALLOWED_HOSTS = OFFICIAL_HOSTS | {"www.yelp.com"}
# Requester-reported amounts must never be rendered as table values.
REPORTED_AMOUNTS = ["$614", "$550", "$135"]
# Internal-only wording that must never be published (assembled so this file does not itself contain it verbatim).
EXCLUDED_PHRASES = [
    "without a " + "permit", "without " + "permit", "no " + "permit", "un" + "permitted", "pull a " + "permit",
    "pulling a " + "permit", "skip the " + "permit", "avoid a " + "permit", "permit for this " + "week",
    "stay " + "private", "never " + "mentioned", "internal " + "use only", "reasons that " + "need",
]


def read(name: str) -> str:
    return (SITE / name).read_text(encoding="utf-8")


def tbody_rows(doc: str) -> list[str]:
    rows: list[str] = []
    for body in re.findall(r"<tbody\b[^>]*>(.*?)</tbody>", doc, re.S | re.I):
        rows.extend(re.findall(r"<tr\b[^>]*>(.*?)</tr>", body, re.S | re.I))
    return rows


def hrefs(doc: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', doc)


class _IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):  # noqa: D401
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)


def ids_in(doc: str) -> set[str]:
    p = _IdCollector()
    p.feed(doc)
    return p.ids


class GeneratorTests(unittest.TestCase):
    def test_committed_output_matches_generator(self):
        problems = gen.check_outputs(SITE, gen.build_outputs())
        self.assertEqual(problems, [], f"regenerate with: python3 scripts/build_e9a30ab9_overflow_site.py -> {problems}")

    def test_generator_is_deterministic(self):
        self.assertEqual(gen.build_outputs(), gen.build_outputs())

    def test_all_expected_files_exist(self):
        for name in PAGES + ["assets/style.css", "EXECUTIVE-SUMMARY.md", "REPO-REVIEW.md"]:
            self.assertTrue((SITE / name).is_file(), name)
        for name in ["cslb_records", "estimates", "requirements", "compliance", "repo_review", "flags", "sources", "verification"]:
            self.assertTrue((SITE / "data" / f"{name}.json").is_file(), name)


class TableRuleTests(unittest.TestCase):
    def test_every_tbody_row_links_to_an_official_source(self):
        total = 0
        for page in PAGES:
            doc = read(page)
            for i, row in enumerate(tbody_rows(doc), 1):
                total += 1
                hosts = {urlsplit(h).netloc for h in hrefs(row) if h.startswith("https://")}
                self.assertTrue(hosts & OFFICIAL_HOSTS, f"{page} tbody row {i} has no official https link: {row[:160]}")
        self.assertGreater(total, 90, "expected a substantial number of table rows")

    def test_blank_cells_are_flagged_and_no_silent_empty_cells(self):
        flagged = 0
        for page in PAGES:
            doc = read(page)
            for cell in re.findall(r"<td\b[^>]*>(.*?)</td>", doc, re.S):
                text = re.sub(r"<[^>]+>", "", cell).strip()
                if not text:
                    self.fail(f"{page}: silent empty cell")
            for cell in re.findall(r'<td class="blank">(.*?)</td>', doc, re.S):
                flagged += 1
                self.assertIn("UNVERIFIED", cell, page)
                self.assertTrue(re.sub(r"<[^>]+>", "", cell).replace("UNVERIFIED", "").strip(), f"{page}: blank cell without reason")
        self.assertGreaterEqual(flagged, 6, "estimate amount/date cells and unverified contractor cells must be flagged")

    def test_requester_amounts_never_appear_in_table_bodies(self):
        for page in PAGES:
            for row in tbody_rows(read(page)):
                for amt in REPORTED_AMOUNTS:
                    self.assertNotIn(amt, row, f"{page}: reported amount {amt} rendered inside a table row")

    def test_estimates_table_amount_and_date_cells_blank(self):
        doc = read("estimates.html")
        rows = tbody_rows(doc)
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(row.count('<td class="blank">'), 2, "amount and date cells must both be blank+flagged")
            self.assertIn("LicenseDetail.aspx?LicNum=", row)

    def test_no_third_party_rating_values(self):
        for page in PAGES:
            doc = read(page)
            self.assertIsNone(re.search(r"\b[0-5]\.\d\s*(?:★|stars?|/5)", doc), f"{page}: rating-like value rendered")
            self.assertNotRegex(doc, r"\(\s*\d+\s+reviews?\s*\)", f"{page}: review count rendered")

    def test_each_page_has_full_navigation_and_footer_rule(self):
        for page in PAGES:
            doc = read(page)
            for target, _ in gen.NAV:
                self.assertIn(f'href="{target}"', doc, f"{page} lacks nav link to {target}")
            self.assertIn("UNVERIFIED", doc)
            self.assertIn('rel="stylesheet" href="assets/style.css"', doc)


class LinkTests(unittest.TestCase):
    def test_internal_links_and_anchors_resolve(self):
        docs = {p: read(p) for p in PAGES}
        ids = {p: ids_in(d) for p, d in docs.items()}
        for page, doc in docs.items():
            for h in hrefs(doc):
                if h.startswith(("http://", "https://", "mailto:")):
                    continue
                target, _, frag = h.partition("#")
                if target == "":
                    self.assertIn(frag, ids[page], f"{page}: missing anchor #{frag}")
                    continue
                self.assertTrue((SITE / target).is_file(), f"{page}: broken internal link {h}")
                if frag and target in ids:
                    self.assertIn(frag, ids[target], f"{page}: {h} anchor missing in {target}")

    def test_external_links_https_and_on_allow_list(self):
        for page in PAGES:
            for h in hrefs(read(page)):
                if h.startswith("http"):
                    self.assertTrue(h.startswith("https://"), f"{page}: non-https link {h}")
                    self.assertIn(urlsplit(h).netloc, ALLOWED_HOSTS, f"{page}: unexpected host in {h}")

    def test_external_links_open_safely(self):
        for page in PAGES:
            doc = read(page)
            for m in re.finditer(r'<a href="https://[^"]+"([^>]*)>', doc):
                self.assertIn('rel="noopener noreferrer"', m.group(1), page)

    def test_github_line_links_use_pinned_commit(self):
        doc = read("repo-review.html")
        links = [h for h in hrefs(doc) if h.startswith("https://github.com/")]
        self.assertTrue(links)
        for h in links:
            self.assertIn(f"/blob/{gen.MAIN_SHA}/", h)
        self.assertRegex(gen.MAIN_SHA, r"^[0-9a-f]{40}$")


class DataTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((SITE / "data" / f"{name}.json").read_text(encoding="utf-8"))

    def test_estimates_json_has_null_unverified_values(self):
        for e in self.load("estimates"):
            self.assertIsNone(e["verified_amount_usd"])
            self.assertIsNone(e["verified_date"])
            self.assertIn("UNVERIFIED", e["verification"])
            self.assertTrue(e["source"].startswith(gen.CSLB_DETAIL))

    def test_json_counts_match_rendered_tables(self):
        self.assertEqual(len(self.load("cslb_records")), len(tbody_rows(read("index.html"))))
        self.assertEqual(len(self.load("flags")), len(tbody_rows(read("flagged-for-review.html"))))
        self.assertEqual(len(self.load("repo_review")), len(tbody_rows(read("repo-review.html"))))
        self.assertEqual(len(self.load("requirements")), len(tbody_rows(read("requirements.html"))))
        self.assertEqual(len(self.load("compliance")), len(tbody_rows(read("compliance.html"))))
        self.assertEqual(len(self.load("verification")), len(tbody_rows(read("verification.html"))))
        self.assertEqual(len(self.load("sources")), len(tbody_rows(read("sources.html"))))
        self.assertEqual(len(self.load("cslb_records")), sum(len(tbody_rows(t)) for t in re.findall(r"(<table.*?</table>)", read("contractors.html"), re.S)))

    def test_every_record_and_source_has_official_url_and_read_date(self):
        for r in self.load("cslb_records"):
            self.assertTrue(r["source"].startswith(gen.CSLB_DETAIL + r["license_number"]))
            self.assertEqual(r["read_date"], gen.READ_DATE)
            self.assertEqual(r["bond_amount"], "$25,000")
            self.assertIn("C-36", r["classifications"])
        for s in self.load("sources"):
            self.assertTrue(s["url"].startswith("https://"))
            self.assertEqual(s["read_date"], gen.READ_DATE)
        for item in self.load("flags") + self.load("requirements") + self.load("compliance") + self.load("verification"):
            self.assertTrue(any(urlsplit(u).netloc in OFFICIAL_HOSTS for u in item["sources"]), item)

    def test_all_in_one_classification_logic(self):
        recs = {r["license_number"]: r for r in self.load("cslb_records")}
        for lic in ["959843", "1003394", "829071", "1025814", "1115649", "841229"]:
            self.assertTrue(recs[lic]["covers_plumbing_and_general_building"], lic)
            self.assertIn("B", recs[lic]["classifications"])
        for lic in ["977638", "757796", "1024971", "1089561"]:
            self.assertFalse(recs[lic]["covers_plumbing_and_general_building"], lic)
            self.assertNotIn("B", recs[lic]["classifications"])


class PublicationHygieneTests(unittest.TestCase):
    def test_excluded_wording_absent_from_site_and_generator(self):
        files = [p for p in SITE.rglob("*") if p.is_file()] + [GEN]
        for f in files:
            text = f.read_text(encoding="utf-8").lower()
            for phrase in EXCLUDED_PHRASES:
                self.assertNotIn(phrase, text, f"{f.relative_to(REPO)} contains excluded wording: {phrase!r}")

    def test_markdown_deliverables_reference_official_sources(self):
        for name in ["EXECUTIVE-SUMMARY.md", "REPO-REVIEW.md"]:
            md = read(name)
            self.assertIn("https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/", md)
            self.assertIn("UNVERIFIED", md)
        self.assertEqual(read("REPO-REVIEW.md").count("| RR-"), len(gen.REPO_REVIEW))


if __name__ == "__main__":
    unittest.main()
