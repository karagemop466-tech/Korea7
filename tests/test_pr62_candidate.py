"""Tests for the CSLB #946657 candidate lead (arena/860ca261-korea7).

The risk this guards against: publishing a plausible-looking firm without the
official fields being right, or quietly folding it into the score.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pr62_candidate as P  # noqa: E402


class CandidateSources(unittest.TestCase):
    def test_official_source_is_cslb(self):
        src = P.SOURCES[P.S_CSLB946]
        self.assertTrue(src["url"].startswith(
            "https://www2.cslb.ca.gov/onlineservices/CheckLicenseII/LicenseDetail.aspx"))
        self.assertIn("LicNum=946657", src["url"])
        self.assertEqual(src["tier"], "official")

    def test_review_source_is_marked_third_party(self):
        src = P.SOURCES[P.S_ANGI946]
        self.assertEqual(src["tier"], "platform")
        self.assertIn("self-reported", src["note"])

    def test_cslb_facts_are_complete(self):
        supports = P.SOURCES[P.S_CSLB946]["supports"]
        for fact in ("2010-05-03", "2028-05-31", "C36", "A,", "C20", "C10",
                     "(650) 583-3399", "317 Corey Way"):
            self.assertIn(fact, supports)

    def test_missing_drywall_classification_is_recorded(self):
        note = P.SOURCES[P.S_CSLB946]["note"]
        self.assertIn("No B", note)
        self.assertIn("C-9", note)


class CandidatePublication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import dashboard_content as C
        C2 = sys.modules["dashboard_content"]
        P.integrate(C2)
        cls.table = C2.TABLES["candidate_946"]
        cls.page = (ROOT / "candidates.html").read_text()
        cls.text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cls.page))

    def test_every_row_has_a_source(self):
        for row in self.table["rows"]:
            self.assertTrue(row["src"], row["cells"][0])

    def test_price_stays_blank_and_flagged(self):
        price_row = [r for r in self.table["rows"] if "price" in r["cells"][0].lower()][0]
        self.assertIn("blank", price_row["cells"][1])
        self.assertIn("UNVERIFIED", price_row["cells"][1])

    def test_page_says_it_is_not_scored(self):
        self.assertIn("not as a ranking score", self.text)
        self.assertIn("deliberately not folded into the score", self.text)
        self.assertIn("only a site visit and a written scope", self.text.lower())

    def test_page_does_not_republish_unverified_2018_review(self):
        self.assertNotIn("2018 review describes", self.text)
        self.assertIn("not restated here", self.text)

    def test_page_has_no_prohibited_permit_wording(self):
        for pattern in (r"without\s+a\s+permit", r"skip\s+the\s+permit",
                        r"internal\s+use\s+only"):
            self.assertIsNone(re.search(pattern, self.text, re.I), pattern)


if __name__ == "__main__":
    unittest.main()
