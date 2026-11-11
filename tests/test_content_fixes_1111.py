"""Regression tests for the 2026-11-11 line-by-line content repairs.

These assert only integrity properties of the published content — unique row
identifiers, no stale candidate counts, a dated snapshot note on the static
shortlist page — plus the rule that every repaired cell keeps a source link.
No external claim is made or upgraded by this module.
"""
from __future__ import annotations

import collections
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402


def _plain(name: str) -> str:
    return re.sub(r"<[^>]+>", " ", (ROOT / name).read_text(encoding="utf-8"))


class Identifiers(unittest.TestCase):
    def test_finding_identifiers_are_unique(self):
        ids = [str(r["cells"][0]) for r in C.TABLES["findings"]["rows"]]
        self.assertEqual([k for k, v in collections.Counter(ids).items() if v > 1], [])

    def test_flagged_identifiers_are_unique(self):
        ids = [str(r["cells"][0]) for r in C.TABLES["flagged"]["rows"]]
        self.assertEqual([k for k, v in collections.Counter(ids).items() if v > 1], [])

    def test_renumbered_finding_is_the_workers_comp_row(self):
        rows = {str(r["cells"][0]): r for r in C.TABLES["findings"]["rows"]}
        self.assertIn("F20", rows)
        self.assertIn("workers'-compensation", str(rows["F20"]["cells"][1]))
        self.assertTrue(rows["F20"]["src"])
        # The cross-reference from the earlier flag now points at F20.
        u46 = [r for r in C.TABLES["flagged"]["rows"] if str(r["cells"][0]) == "U46"]
        if u46:
            self.assertNotIn("see F10", str(u46[0]["cells"][2]))


class CandidateCounts(unittest.TestCase):
    def test_lede_and_requirements_state_sixteen(self):
        self.assertNotIn("Eight candidates", C.PAGES["contractors.html"]["lede"])
        self.assertIn("Sixteen candidates", C.PAGES["contractors.html"]["lede"])
        req = {r["cells"][0]: r for r in C.TABLES["requirements"]["rows"]}
        self.assertIn("Sixteen", req["R09"]["cells"][3])
        self.assertIn("sixteen", req["R15"]["cells"][3])

    def test_no_stale_eight_strings_in_published_pages(self):
        for name in ("contractors.html", "requirements.html", "findings.html", "shortlist.html", "summary.html"):
            text = _plain(name)
            self.assertIsNone(re.search(r"\bEight (candidates|named|official|licensed)", text), name)

    def test_shortlist_snapshot_note_and_current_counts(self):
        text = _plain("shortlist.html")
        self.assertIn("Snapshot note — updated 2026-11-11", text)
        self.assertIn("Sixteen CSLB records each held a current, active licence", text)
        self.assertNotIn("verified for 8 of 9", text)
        self.assertIn("ranking.html", (ROOT / "shortlist.html").read_text())

    def test_shortlist_links_every_licence_number(self):
        text = (ROOT / "shortlist.html").read_text(encoding="utf-8")
        for number in set(re.findall(r"#(\d{6,8})", text)):
            self.assertIn("LicNum=%s" % number, text)


class FlagRecord(unittest.TestCase):
    def test_repair_is_published_as_a_flag(self):
        flags = {str(r["cells"][0]): r for r in C.TABLES["flagged"]["rows"]}
        matches = [r for r in flags.values()
                   if "duplicated finding identifier" in str(r["cells"][1])]
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0]["src"])
        for sid in matches[0]["src"]:
            self.assertIn(sid, C.SOURCES)

    def test_published_flag_count_matches_table(self):
        card = next(card for block in C.PAGES["index.html"]["sections"] if block["type"] == "cards"
                    for card in block["items"] if card["k"] == "Flagged for review")
        self.assertEqual(int(card["v"]), len(C.TABLES["flagged"]["rows"]))


if __name__ == "__main__":
    unittest.main()
