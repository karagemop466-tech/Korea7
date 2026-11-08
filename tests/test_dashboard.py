#!/usr/bin/env python3
"""Standalone checks for the canonical dashboard (no third-party deps).

Run:  python3 tests/test_dashboard.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import verify_dashboard as V  # noqa: E402
import build_dashboard as B  # noqa: E402


class TestContent(unittest.TestCase):
    def test_every_row_has_sources(self):
        B.build_source_ledger_rows()
        for tid, table in C.TABLES.items():
            for i, row in enumerate(table["rows"], 1):
                self.assertTrue(row["src"], "%s row %d has no sources" % (tid, i))
                for sid in row["src"]:
                    self.assertIn(sid, C.SOURCES, "%s row %d cites unknown %s" % (tid, i, sid))
                    self.assertNotEqual(C.SOURCES[sid]["status"], "dead",
                                        "%s row %d cites dead %s" % (tid, i, sid))

    def test_cell_counts_match_columns(self):
        B.build_source_ledger_rows()
        for tid, table in C.TABLES.items():
            self.assertEqual(table["columns"][-1], "Source")
            for i, row in enumerate(table["rows"], 1):
                self.assertEqual(len(row["cells"]), len(table["columns"]) - 1,
                                 "%s row %d cell count" % (tid, i))

    def test_unverified_blanks_are_flagged(self):
        B.build_source_ledger_rows()
        for tid, table in C.TABLES.items():
            for i, row in enumerate(table["rows"], 1):
                joined = " ".join(row["cells"])
                if C.BLANK in joined:
                    self.assertIn(C.UNVERIFIED, joined,
                                  "%s row %d has a blank without an UNVERIFIED flag" % (tid, i))

    def test_official_sources_present(self):
        official = [s for s in C.SOURCES.values()
                    if s["tier"] in ("official", "manufacturer") and s["status"] == "verified"]
        self.assertGreaterEqual(len(official), 10)
        for sid in ("S01", "S02", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13"):
            self.assertEqual(C.SOURCES[sid]["tier"], "official")

    def test_no_private_wording_in_content(self):
        blob = "\n".join(" ".join(r["cells"]) + " " + t.get("caption", "")
                         for t in C.TABLES.values() for r in t["rows"])
        blob += "\n" + "\n".join(b.get("html", "") for p in C.PAGES.values() for b in p["sections"])
        for pat in V.PRIVACY_PATTERNS:
            import re
            self.assertIsNone(re.search(pat, blob, re.I), "private wording matched: %s" % pat)


    def test_current_ranking_sources_are_fresh_and_official_or_company(self):
        for row in C.TABLES["ranking"]["rows"]:
            self.assertTrue(row["src"])
            for sid in row["src"]:
                src = C.SOURCES[sid]
                self.assertIn(src["tier"], ("official", "company"))
                self.assertEqual(src["status"], "verified")
                self.assertEqual(src["checked"], C.META["updated"])
            self.assertIn(C.BLANK, row["cells"][-1])
            self.assertIn(C.UNVERIFIED, row["cells"][-1])

    def test_top_pick_and_contacts_are_source_linked(self):
        top = C.TABLES["top_picks"]["rows"][0]
        self.assertIn("General SF", top["cells"][1])
        self.assertIn("(650) 303-1515", top["cells"][2])
        self.assertIn("S09", top["src"])
        self.assertEqual(len(C.TABLES["contacts"]["rows"]), 8)
        for row in C.TABLES["contacts"]["rows"]:
            self.assertRegex(row["cells"][1], r"\(\d{3}\) \d{3}-\d{4}")
            self.assertTrue(any(C.SOURCES[s]["tier"] == "official" for s in row["src"]))

    def test_review_numbers_and_drywall_inclusion_remain_unverified(self):
        for row in C.TABLES["review_snapshots"]["rows"]:
            self.assertIn(C.BLANK, row["cells"][3])
            self.assertIn(C.UNVERIFIED, row["cells"][3])
        flags = {r["cells"][0]: r for r in C.TABLES["flagged"]["rows"]}
        self.assertIn("U33", flags)
        self.assertIn("does not state", flags["U33"]["cells"][2])
        requirements = {r["cells"][0]: r for r in C.TABLES["requirements"]["rows"]}
        self.assertIn("partial", requirements["R22"]["cells"][4])

    def test_inventory_files_exist_and_match(self):
        import csv, json, re
        data = json.loads((ROOT / "data/canonical/repo_inventory.json").read_text())
        with (ROOT / "data/canonical/repo_inventory.csv").open(newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(data), len(rows))
        self.assertGreater(len(data), 200)
        for item in data:
            self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
            self.assertFalse(item["path"].startswith(".git/"))

    def test_verification_does_not_call_all_rows_official(self):
        text = (ROOT / "verification.html").read_text()
        self.assertIn("project primary record", text)
        self.assertIn("historical", text)
        self.assertIn("not independent proof", text)

class TestBuiltSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = V.analyze(ROOT, list(C.PAGES.keys()))

    def test_all_checks_pass(self):
        for c in self.report["checks"]:
            self.assertEqual(c["status"], "PASS", "%s: %s" % (c["name"], c["detail"]))

    def test_pages_exist(self):
        for name in C.PAGES:
            self.assertTrue((ROOT / name).exists(), name)

    def test_every_row_renders_a_source_link(self):
        self.assertEqual(self.report["missing_row_links"], [])

    def test_no_broken_internal_links(self):
        self.assertEqual(self.report["broken_internal"], [])

    def test_no_unknown_external_links(self):
        self.assertEqual(self.report["unknown_external"], [])

    def test_privacy_sweep_clean(self):
        self.assertEqual(self.report["privacy_matches"], [])

    def test_reports_exist(self):
        self.assertTrue((ROOT / "data/canonical/verification_report.json").exists())
        self.assertTrue((ROOT / "data/canonical/site_data.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
