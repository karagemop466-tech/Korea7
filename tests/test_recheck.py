"""Regression checks for the dated 2026-11-10 re-read supplement."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dashboard_content as C
import recheck_data as R


class RecheckChecks(unittest.TestCase):
    def setUp(self):
        self.artifact = json.loads((ROOT / "data/canonical/recheck-2026-11-10.json").read_text())

    def test_all_sixteen_records_reread_and_active(self):
        rows = C.TABLES["recheck_licenses"]["rows"]
        self.assertEqual(len(rows), 16)
        self.assertEqual(len(self.artifact["records"]), 16)
        numbers = [r["license"] for r in self.artifact["records"]]
        self.assertEqual(len(set(numbers)), 16)
        for rec in self.artifact["records"]:
            self.assertEqual(rec["status"], "current and active")
            self.assertTrue(rec["record_stamp"].startswith("Data current as of 11/9/2026 "))
            self.assertIn("LicNum=" + rec["license"], rec["source_url"])
            self.assertTrue(rec["phone_on_record"].startswith("("))

    def test_supplement_sources_are_dated_and_official(self):
        for rec in self.artifact["records"]:
            source = C.SOURCES[rec["source_id"]]
            self.assertEqual(source["checked"], "2026-11-10")
            self.assertEqual(source["tier"], "official")
            self.assertIn("LicNum=" + rec["license"], source["url"])

    def test_historical_snapshot_still_intact(self):
        stored = json.loads((ROOT / "data/canonical/cslb_records.json").read_text())
        self.assertEqual(stored["meta"]["retrieved_utc"], "2026-11-08")
        self.assertEqual(len(stored["records"]), 16)
        for sid in ("S06", "S10", "S11", "S64"):
            self.assertEqual(C.SOURCES[sid]["checked"], "2026-11-08")

    def test_deltas_are_computed_not_asserted(self):
        for rec, (licence, deltas) in zip(self.artifact["records"], R.compare()):
            self.assertEqual(rec["license"], licence)
            self.assertEqual(rec["deltas"], deltas)
            self.assertEqual(rec["delta_summary"], R.summary_text(deltas))
        raw = C.TABLES["recheck_deltas"]["rows"]
        self.assertGreaterEqual(len(raw), 1)

    def test_rule_pages_reread_with_quotes(self):
        rules = C.TABLES["recheck_rules"]["rows"]
        self.assertEqual(len(rules), 3)
        for rule in self.artifact["rule_checks"]:
            self.assertEqual(C.SOURCES[rule["source_id"]]["checked"], "2026-11-10")
            self.assertEqual(C.SOURCES[rule["source_id"]]["tier"], "official")
            self.assertTrue(rule["quote"])
            self.assertEqual(rule["consistent"], "yes")

    def test_company_page_reads_are_company_tier(self):
        rows = C.TABLES["recheck_company"]["rows"]
        self.assertEqual(len(rows), 2)
        for check in self.artifact["company_checks"]:
            source = C.SOURCES[check["source_id"]]
            self.assertEqual(source["tier"], "company")
            self.assertEqual(source["checked"], "2026-11-10")
            self.assertTrue(check["check"])

    def test_no_booking_or_capability_claim(self):
        limits = self.artifact["limits"]
        self.assertFalse(limits["provider_contacted"])
        self.assertFalse(limits["booking_confirmed"])
        self.assertIsNone(limits["job_specific_verified_price"])
        self.assertFalse(limits["job_specific_experience_verified"])
        self.assertFalse(limits["availability_confirmed"])
        text = (ROOT / "recheck.html").read_text()
        self.assertIn("No provider was contacted and nothing was booked", text)
        self.assertIn(("recheck.html", "Live re-check 2026-11-10"), C.NAV[-1]["links"])

    def test_flag_added_for_database_stamp_lag(self):
        ids = [r["cells"][0] for r in C.TABLES["flagged"]["rows"]]
        self.assertIn("U46", ids)


if __name__ == "__main__":
    unittest.main()
