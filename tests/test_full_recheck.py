"""Regression checks for the 2026-11-10 full-record re-verification (arena/33211fbf-korea7).

These tests do not re-fetch anything. They assert that what the site *claims*
about today's verification is internally consistent with the recorded evidence
and with the committed CSLB dataset.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import delivery_data  # noqa: E402

EVIDENCE = json.loads((ROOT / "data/canonical/verification-2026-11-10-g1.json").read_text())
DATASET = json.loads((ROOT / "data/canonical/cslb_records.json").read_text())
BY_LICENSE = {r["license"]: r for r in DATASET["records"]}
CHECKED = {r["license"]: r for r in EVIDENCE["cslb_records"]["per_record"]}


def norm_class(c: str) -> str:
    return c.upper().replace("-", "")


class FullRecheckTest(unittest.TestCase):
    def test_evidence_covers_every_canonical_record(self):
        self.assertEqual(len(EVIDENCE["cslb_records"]["per_record"]), len(DATASET["records"]))
        self.assertEqual(set(CHECKED), set(BY_LICENSE))

    def test_no_record_is_claimed_as_mismatched(self):
        self.assertEqual(EVIDENCE["cslb_records"]["records_mismatched"], 0)
        self.assertTrue(all(r["match"] is True for r in EVIDENCE["cslb_records"]["per_record"]))

    def test_every_evidence_row_agrees_with_the_committed_dataset(self):
        for lic, ev in CHECKED.items():
            ds = BY_LICENSE[lic]
            with self.subTest(license=lic):
                self.assertEqual(ev["status"], ds["status"])
                self.assertEqual(ev["classes"].split(", "),
                                 [c for c in ds["classifications"]])
                self.assertEqual(ev["phone"], ds["phone_on_record"])

    def test_claims_no_job_specific_evidence(self):
        d = EVIDENCE["determinations"]
        for key in ("job_specific_price_confirmed", "job_specific_capability_confirmed",
                    "one_contract_plumbing_and_restoration_confirmed",
                    "provider_contacted", "availability_confirmed"):
            self.assertIs(d[key], False, key)
        self.assertEqual(d["defects_found_in_prior_data"], 0)

    def test_blocked_review_platforms_are_disclosed(self):
        note = EVIDENCE["not_rechecked_today"]["note"]
        self.assertIn("historical read dates", note)
        self.assertTrue(any("Yelp" in item for item in EVIDENCE["not_rechecked_today"]["items"]))

    def test_timestamps_are_not_rewritten_to_today(self):
        self.assertEqual(EVIDENCE["cslb_records"]["database_timestamp_seen"],
                         "Data current as of 11/9/2026, between 4:51:26 PM and 4:52:06 PM")
        self.assertIn("11/9/2026", EVIDENCE["method"] + EVIDENCE["cslb_records"]["note"])


class DeliveryTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        delivery_data.integrate(C)

    def test_full_recheck_table_has_one_row_per_record(self):
        rows = C.TABLES["delivery_full_recheck"]["rows"]
        self.assertEqual(len(rows), 16)

    def test_every_full_recheck_row_is_source_linked(self):
        for row in C.TABLES["delivery_full_recheck"]["rows"]:
            self.assertEqual(row["src"], ["S112"])
            # The renderer appends the source column, so cell data is columns - 1.
            self.assertEqual(len(row["cells"]),
                             len(C.TABLES["delivery_full_recheck"]["columns"]) - 1)

    def test_full_recheck_prices_are_blank_and_flagged(self):
        idx = C.TABLES["delivery_full_recheck"]["columns"].index("Job price")
        for row in C.TABLES["delivery_full_recheck"]["rows"]:
            cell = row["cells"][idx]
            self.assertIn("UNVERIFIED", cell)
            self.assertNotRegex(cell, r"\$\d")

    def test_definition_table_rows_are_source_linked(self):
        t = C.TABLES["delivery_definition_check"]
        for row in t["rows"]:
            self.assertEqual(len(row["cells"]), len(t["columns"]) - 1)
            self.assertTrue(row["src"])
            for sid in row["src"]:
                self.assertIn(sid, C.SOURCES)

    def test_new_sources_are_official_or_transcribed_with_urls(self):
        for sid in ("S112", "S113"):
            s = C.SOURCES[sid]
            self.assertEqual(s["checked"], "2026-11-10")
            self.assertTrue(s["url"])
        self.assertEqual(C.SOURCES["S113"]["tier"], "official")

    def test_yelp_sources_are_never_scored_or_marked_verified(self):
        for sid, s in C.SOURCES.items():
            if "Yelp" in s.get("publisher", ""):
                self.assertEqual(s["status"], "blocked-403", sid)


if __name__ == "__main__":
    unittest.main()
