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
