"""Regression checks for the 2026-11-08 follow-up corrections.

Originally written by session arena/e3044a3b-korea7 for IDs U06/U20/U21/S61.
Updated during final integration to canonical IDs F06/F09/F25/F27/S75 while
preserving intent: four no-employee exemptions are named with official sources,
verification limitations and the no-outreach boundary are explicit, and the
Fast Response company lead is labeled as self-published, not proof.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dashboard_content as content


class FollowupAudit(unittest.TestCase):
    def test_four_exemptions_are_named_with_official_sources(self):
        flags = {row["cells"][0]: row for row in content.TABLES["flags"]["rows"]}
        general = flags["F06"]
        others = flags["F09"]
        self.assertIn("S09", general["src"])
        self.assertTrue({"S07", "S46", "S49"}.issubset(set(others["src"])))
        text = " ".join(general["cells"] + others["cells"])
        for number in ("757796", "959843", "1115649", "841229"):
            self.assertIn(number, text)

    def test_limitations_and_provider_claim_are_explicit(self):
        flags = {row["cells"][0]: row for row in content.TABLES["flags"]["rows"]}
        self.assertIn("not government sources", flags["F27"]["cells"][3])
        self.assertIn("owner reported prior estimates", flags["F25"]["cells"][3])
        self.assertEqual(content.SOURCES["S75"]["tier"], "company")
        self.assertIn("not proof", content.SOURCES["S75"]["note"])


if __name__ == "__main__":
    unittest.main()
