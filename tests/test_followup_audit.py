"""Regression checks for the 2026-11-08 follow-up corrections."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dashboard_content as content


class FollowupAudit(unittest.TestCase):
    def test_all_exemptions_are_named_with_official_sources(self):
        """U06 must name every CSLB record that carries the 'no employees' exemption.

        The flag was written when four exemptions were known. The candidate pool later grew to
        sixteen records, so 632743 (Calplumbing Co) is a fifth; the 2026-11-10 re-verification
        corrected the count rather than leaving a stale number on the page.
        """
        row = next(r for r in content.TABLES["flagged"]["rows"] if r["cells"][0] == "U06")
        self.assertEqual(set(row["src"]), {"S07", "S09", "S56", "S57", "S68", "S105"})
        for number in ("757796", "959843", "1115649", "841229", "632743"):
            self.assertIn(number, row["cells"][1])
        self.assertIn("five", row["cells"][2].lower())
        # Every named record really is exempt on the canonical CSLB transcription.
        exempt = {lic for lic, rec in content.R.RECORDS.items()
                  if rec["workers_compensation"]["kind"] == "exempt"}
        named = {n for n in ("757796", "959843", "1115649", "841229", "632743")}
        self.assertTrue(named <= exempt, exempt)
        self.assertEqual(len(exempt), 5)

    def test_limitations_and_provider_claim_are_explicit(self):
        flags = {row["cells"][0]: row for row in content.TABLES["flagged"]["rows"]}
        self.assertIn("not government sources", flags["U21"]["cells"][2])
        self.assertIn("owner reported prior estimates", flags["U20"]["cells"][2])
        self.assertEqual(content.SOURCES["S61"]["tier"], "company")
        self.assertIn("not proof", content.SOURCES["S61"]["note"])


if __name__ == "__main__":
    unittest.main()
