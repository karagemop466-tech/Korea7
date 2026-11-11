"""Regression tests for the older bathtub-overflow microsite's permit analysis.

The primary dashboard has its own structural verifier. These assertions protect
against the older subpages reintroducing unsupported permit-exemption conclusions.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "bathtub-overflow/permits-compliance.html",
    "bathtub-overflow/executive-summary.html",
    "bathtub-overflow/analysis.html",
    "bathtub-overflow/estimates.html",
    "bathtub-overflow/flagged-for-review.html",
    "bathtub-overflow/methodology.html",
    "bathtub-overflow/sources.html",
]


class LegacyPermitGuidanceTests(unittest.TestCase):
    def read(self, page: str) -> str:
        return (ROOT / page).read_text(encoding="utf-8")

    def test_permit_scope_rows_have_official_citations(self):
        page = self.read(PAGES[0])
        table = re.search(r"<table>.*?</table>", page, re.S)
        self.assertIsNotNone(table)
        rows = re.findall(r"<tr>(.*?)</tr>", table.group(0), re.S)
        self.assertEqual(len(rows), 5)  # header plus four scope rows
        official_domains = (
            "sf.gov/",
            "media.api.sf.gov/",
            "codelibrary.amlegal.com/",
        )
        for row in rows[1:]:
            self.assertEqual(row.count("<td>"), 3)
            links = re.findall(r'href="(https://[^\"]+)"', row)
            self.assertTrue(links, row)
            self.assertTrue(any(any(domain in link for domain in official_domains) for link in links), row)

    def test_no_unverified_permit_conclusions_remain(self):
        content = "\n".join(self.read(page) for page in PAGES)
        unsupported = (
            "plausibly falls under the exemption",
            "matches the permit-required description",
            "linkage adjustment may be exempt",
            "replacement scope is permit-type work",
            "matches the §104.2 exempt-work descriptions",
        )
        for phrase in unsupported:
            self.assertNotIn(phrase.lower(), content.lower())
        self.assertIn("exact permit applicability is unresolved", content.lower())
        self.assertIn("scope-specific answer", content.lower())

    def test_city_sources_replace_model_code_as_job_rule(self):
        permits = self.read(PAGES[0])
        sources = self.read(PAGES[-1])
        self.assertIn("media.api.sf.gov/documents/2025_SF_Plumbing_Code.pdf", permits)
        self.assertIn("codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830", permits)
        self.assertIn("not used to determine San Francisco permit applicability", sources)
        self.assertIn("IAPMO/model-code summary is not used", self.read(PAGES[4]))


if __name__ == "__main__":
    unittest.main()
