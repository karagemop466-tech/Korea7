"""Regression checks for the dated 2026-11-11 licence re-read (session arena/12cacfe5-korea7)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dashboard_content as C  # noqa: E402  (runs every integrate step, writes the artifact)
import recheck_data  # noqa: E402
import reread_1111 as R  # noqa: E402


class Reread1111Checks(unittest.TestCase):
    def setUp(self):
        self.artifact = json.loads((ROOT / "data/canonical/reread-2026-11-11.json").read_text())

    def test_all_seventeen_records_read_and_active(self):
        self.assertEqual(len(R.ALL_READS), 17)
        numbers = [r["license"] for r in R.ALL_READS]
        self.assertEqual(len(set(numbers)), 17)
        # same 16 scored licences as the 2026-11-10 re-check, plus the separately checked lead
        self.assertEqual(set(numbers) - {"1034873"}, {r["license"] for r in recheck_data.READS})
        for rec in self.artifact["records"]:
            self.assertEqual(rec["status"], "current and active")
            self.assertTrue(rec["record_stamp"].startswith("Data current as of 11/10/2026 "))
            self.assertIn("LicNum=" + rec["license"], rec["source_url"])

    def test_sources_are_official_and_dated(self):
        for rec in self.artifact["records"]:
            src = C.SOURCES[rec["source_id"]]
            self.assertEqual(src["checked"], "2026-11-11")
            self.assertEqual(src["tier"], "official")
            self.assertTrue(src["url"].startswith("https://www2.cslb.ca.gov/"))
            self.assertIn("LicNum=" + rec["license"], src["url"])

    def test_deltas_are_computed_not_asserted(self):
        for rec, (lic, deltas) in zip(self.artifact["records"], R.compare()):
            self.assertEqual(rec["license"], lic)
            self.assertEqual(rec["deltas"], deltas)

    def test_comparator_detects_a_planted_change(self):
        planted = copy.deepcopy(R.READS[0])
        planted["phone_on_record"] = "(000) 000-0000"
        planted["workers_compensation"]["expires"] = "2099-01-01"
        base = {r["license"]: r for r in recheck_data.READS}[planted["license"]]
        diffs = R._diff_record(base, planted)
        self.assertTrue(any(d.startswith("phone_on_record") for d in diffs))
        self.assertTrue(any(d.startswith("workers_compensation.expires") for d in diffs))

    def test_wc_watch_is_date_arithmetic(self):
        for item in self.artifact["wc_watch"]:
            self.assertLessEqual(item["days"], R.WATCH_DAYS)
            self.assertEqual(item["days"], R.days_until(item["expires"], "2026-11-11"))
        self.assertEqual(R.days_until("2026-12-02", "2026-11-11"), 21)

    def test_page_nav_flag_and_rows_have_sources(self):
        self.assertIn("reread-1111.html", C.PAGES)
        self.assertIn(("reread-1111.html", "Re-read 2026-11-11"), C.NAV[-1]["links"])
        for tid in ("reread1111_licenses", "reread1111_deltas", "reread1111_wc_watch"):
            for row in C.TABLES[tid]["rows"]:
                self.assertTrue(row["src"])
                for sid in row["src"]:
                    self.assertIn(sid, C.SOURCES)
        if self.artifact["wc_watch"]:
            ids = [r["cells"][0] for r in C.TABLES["flagged"]["rows"]]
            self.assertIn(self.artifact["flag_id"], ids)

    def test_historical_records_untouched(self):
        stored = json.loads((ROOT / "data/canonical/cslb_records.json").read_text())
        self.assertEqual(stored["meta"]["retrieved_utc"], "2026-11-08")
        prior = json.loads((ROOT / "data/canonical/recheck-2026-11-10.json").read_text())
        self.assertEqual(prior["checked_date"], "2026-11-10")

    def test_limits_are_explicit(self):
        lim = self.artifact["limits"]
        self.assertFalse(lim["provider_contacted"])
        self.assertFalse(lim["booking_confirmed"])
        self.assertIsNone(lim["job_specific_verified_price"])


if __name__ == "__main__":
    unittest.main()
