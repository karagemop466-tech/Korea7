"""Regression checks for the 2026-11-08 follow-up corrections."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dashboard_content as content


class FollowupAudit(unittest.TestCase):
    def test_four_exemptions_are_named_with_official_sources(self):
        row = next(r for r in content.TABLES["flagged"]["rows"] if r["cells"][0] == "U06")
        self.assertEqual(set(row["src"]), {"S07", "S09", "S56", "S57"})
        for number in ("757796", "959843", "1115649", "841229"):
            self.assertIn(number, row["cells"][1])

    def test_limitations_and_provider_claim_are_explicit(self):
        flags = {row["cells"][0]: row for row in content.TABLES["flagged"]["rows"]}
        self.assertIn("not government sources", flags["U21"]["cells"][2])
        self.assertIn("owner reported prior estimates", flags["U20"]["cells"][2])
        self.assertEqual(content.SOURCES["S61"]["tier"], "company")
        self.assertIn("not proof", content.SOURCES["S61"]["note"])


if __name__ == "__main__":
    unittest.main()
