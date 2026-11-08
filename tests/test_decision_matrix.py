"""Regression checks for the strict 2026-11-08 decision analysis."""
from __future__ import annotations

import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_decision_matrix as builder  # noqa: E402

DATA = json.loads((ROOT / "data" / "decision_matrix.json").read_text(encoding="utf-8"))
GENERATED = ["decision-matrix.html", "shortlist.html"]
PRIVATE_PATTERNS = [
    r"without\s+a\s+permit", r"\bno\s+permit\b",
    r"do\s+not\s+pull\s+a\s+permit", r"cannot\s+pull\s+a\s+permit",
    r"private\s+project\s+rationale", r"reasons\s+that\s+need\s+to\s+stay\s+private",
]
OWNER_AMOUNTS = ("$614", "$550", "$135")
RATING_VALUES = ("4.7 ★", "4.8 ★", "5.0 ★", "4.9 · 1,500")


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_row = False
        self.rows: list[list[str]] = []
        self.current: list[str] = []
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.in_row = True
            self.current = []
        if tag == "a" and a.get("href"):
            href = a["href"]
            self.links.append(href)
            if self.in_row:
                self.current.append(href)

    def handle_data(self, data):
        self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.rows.append(self.current)
            self.in_row = False
        if tag == "tbody":
            self.in_tbody = False


def scan(path: str) -> Scan:
    parser = Scan()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    return parser


class DecisionMatrixTests(unittest.TestCase):
    def test_dataset_official_basis_and_consecutive_ranks(self):
        ranks = [c["rank"] for c in DATA["candidates"]]
        self.assertEqual(ranks, list(range(1, 10)))
        self.assertEqual(DATA["meta"]["verification_date"], "2026-11-08")
        licensed = [c for c in DATA["candidates"] if c["license"]]
        self.assertEqual(len(licensed), 8)
        for c in licensed:
            self.assertTrue(c["phone"])
            self.assertEqual(DATA["sources"][c["cslb"]]["tier"], "official")
            self.assertIn("cslb.ca.gov", DATA["sources"][c["cslb"]]["url"])
        lead = DATA["candidates"][-1]
        for field in ("license", "phone", "address", "status", "classes"):
            self.assertEqual(lead[field], "")

    def test_five_dual_classified_and_four_exemptions(self):
        dual = [c for c in DATA["candidates"] if "B" in c["classes"] and "C-36" in c["classes"]]
        self.assertEqual(len(dual), 5)
        exempt = [c for c in DATA["candidates"] if "no-employee exemption" in c["workers_comp"]]
        self.assertEqual(len(exempt), 4)
        self.assertIn("2026-12-18", DATA["candidates"][5]["workers_comp"])

    def test_every_generated_table_row_has_an_official_link(self):
        for name in GENERATED:
            parsed = scan(name)
            self.assertGreater(len(parsed.rows), 0, name)
            for i, links in enumerate(parsed.rows, 1):
                self.assertTrue(
                    any(builder.is_official_url(href) for href in links),
                    "%s row %d: %s" % (name, i, links),
                )

    def test_no_owner_amounts_ratings_or_private_wording(self):
        raw_json = (ROOT / "data" / "decision_matrix.json").read_text(encoding="utf-8")
        for amount in OWNER_AMOUNTS:
            self.assertNotIn(amount, raw_json)
        for name in GENERATED:
            text = (ROOT / name).read_text(encoding="utf-8")
            for amount in OWNER_AMOUNTS:
                self.assertNotIn(amount, text, name)
            for rating in RATING_VALUES:
                self.assertNotIn(rating, text, name)
            for pattern in PRIVATE_PATTERNS:
                self.assertNotRegex(text, re.compile(pattern, re.I))

    def test_unverified_values_are_blank_and_flagged(self):
        text = (ROOT / "decision-matrix.html").read_text(encoding="utf-8")
        self.assertIn('aria-label="blank — unverified"', text)
        self.assertGreaterEqual(text.count("UNVERIFIED"), 20)
        shortlist = (ROOT / "shortlist.html").read_text(encoding="utf-8")
        self.assertIn('aria-label="blank — unverified"', shortlist)
        self.assertIn("UNVERIFIED", shortlist)

    def test_internal_links_and_anchors_resolve(self):
        for name in GENERATED:
            parsed = scan(name)
            for href in parsed.links:
                url = urlparse(href)
                if url.scheme or url.netloc:
                    continue
                if not url.path:
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), parsed.ids, (name, href))
                    continue
                target = ((ROOT / name).parent / unquote(url.path)).resolve()
                self.assertTrue(target.is_file(), (name, href, str(target)))
                if url.fragment and target.suffix == ".html":
                    dest = Scan()
                    dest.feed(target.read_text(encoding="utf-8"))
                    self.assertIn(unquote(url.fragment), dest.ids, (name, href))

    def test_all_external_links_are_in_the_source_ledger(self):
        allowed = {s["url"] for s in DATA["sources"].values()}
        allowed.add("https://github.com/karagemop466-tech/Korea7")
        for name in GENERATED:
            for href in scan(name).links:
                url = urlparse(href)
                if url.scheme in ("http", "https"):
                    self.assertIn(href, allowed, (name, href))

    def test_pages_cross_link_and_summary_points_to_decision_matrix(self):
        self.assertIn("decision-matrix.html", (ROOT / "shortlist.html").read_text(encoding="utf-8"))
        self.assertIn("shortlist.html", (ROOT / "decision-matrix.html").read_text(encoding="utf-8"))
        summary = (ROOT / "EXECUTIVE-SUMMARY.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("decision-matrix.html", summary)
        self.assertIn("2026-11-08", summary)
        self.assertIn("decision-matrix.html", readme)
        self.assertIn("2026-11-08", readme)
        self.assertTrue((ROOT / "trip-lever" / "e7305a26-verification.md").is_file())

    def test_every_source_is_absolute_and_recent(self):
        for sid, src in DATA["sources"].items():
            self.assertTrue(src["url"].startswith("https://"), sid)
            self.assertEqual(src["checked"], "2026-11-08", sid)
            self.assertTrue(src["label"] and src["publisher"] and src["supports"], sid)

    def test_concurrent_bpc_7059_nuance_is_preserved(self):
        self.assertIn("7059", DATA["sources"]["O18"]["url"])
        self.assertTrue(any(f["id"] == "D06" for f in DATA["flags"]))
        for name in GENERATED:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("7059", text, name)
            self.assertIn("U22", text, name)
        self.assertIn("not automatically required", DATA["candidates"][5]["ranking_reason"])


if __name__ == "__main__":
    unittest.main()
