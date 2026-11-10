"""Tests for the 2026-11-10 session-B independent re-read (arena/860ca261-korea7).

These guard three things:
  1. the transcription artifact matches the canonical CSLB data with no drift;
  2. every published licence/rule row carries a resolvable official source link;
  3. the re-check page does not overclaim what a licence record proves.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "data" / "canonical" / "reverify-2026-11-10b.json"
CSLB = ROOT / "data" / "canonical" / "cslb_records.json"
PAGE = ROOT / "reverify.html"

CSLB_URL = "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx?LicNum="


class ReverifyArtifact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.art = json.loads(ARTIFACT.read_text())
        cls.cslb = {r["license"]: r for r in json.loads(CSLB.read_text())["records"]}

    def test_sixteen_records_recorded(self):
        self.assertEqual(len(self.art["licenses"]), 16)
        self.assertEqual(self.art["meta"]["licenses_re_read"], 16)

    def test_every_license_present_in_canonical_data(self):
        for row in self.art["licenses"]:
            self.assertIn(row["license"], self.cslb, row["license"])

    def test_no_field_drift(self):
        """Each transcribed field must equal the canonical CSLB record."""
        for row in self.art["licenses"]:
            want = self.cslb[row["license"]]
            with self.subTest(license=row["license"]):
                self.assertEqual(row["issue_date"], want["issue_date"])
                self.assertEqual(row["expire_date"], want["expire_date"])
                self.assertEqual(row["entity"], want["entity"])
                self.assertEqual(row["phone"], want["phone_on_record"])
                self.assertEqual(row["status"], want["status"])
                self.assertEqual(
                    row["classifications"].split(" · "), want["classifications"])
                self.assertTrue(row["matches_published_data"])

    def test_artifact_declares_its_limits(self):
        meta = self.art["meta"]
        self.assertEqual(meta["field_differences_found"], 0)
        self.assertIn("does_not_prove", " ".join(meta))
        self.assertIn("competence", meta["what_this_does_not_prove"].lower())

    def test_every_row_has_an_official_cslb_link(self):
        for row in self.art["licenses"]:
            self.assertEqual(row["cslb_url"], CSLB_URL + row["license"])

    def test_rule_rows_are_official(self):
        self.assertGreaterEqual(len(self.art["rules"]), 8)
        for rule in self.art["rules"]:
            with self.subTest(page=rule["page"]):
                self.assertTrue(
                    rule["url"].startswith(("https://www.sf.gov/", "https://www2.cslb.ca.gov/",
                                            "https://leginfo.legislature.ca.gov/",
                                            "https://codelibrary.amlegal.com/",
                                            "https://media.api.sf.gov/")),
                    rule["url"])


class ReverifyPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text()
        cls.text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cls.html))

    def test_page_built(self):
        self.assertIn("Second independent re-read", self.text)

    def test_page_does_not_overclaim(self):
        self.assertIn("does not show that a firm has ever freed a seized trip lever",
                      self.text)
        self.assertIn("No contractor was contacted", self.text)

    def test_page_is_in_navigation(self):
        self.assertIn('href="reverify.html"', self.html + (ROOT / "index.html").read_text())

    def test_no_private_permit_rationale(self):
        for pattern in (r"without\s+a\s+permit", r"cannot\s+pull\s+a\s+permit",
                        r"internal\s+use\s+only", r"stay\s+private"):
            self.assertIsNone(re.search(pattern, self.text, re.I), pattern)


if __name__ == "__main__":
    unittest.main()
