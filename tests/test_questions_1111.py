#!/usr/bin/env python3
"""Regression checks for the 2026-11-11 decision-register addendum.

The base questions page belongs to `scripts/questions_data.py` (another
session). These tests assert that this session's addendum appends rows without
rewriting the base rows, that every new row carries a dated official source, and
that the built page keeps one source link per row.

Run:  python3 -m pytest tests/test_questions_1111.py -q
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import build_dashboard as B  # noqa: E402
import verify_dashboard as V  # noqa: E402

CHECKED = "2026-11-11"
NEW_SOURCE_IDS = ["S220", "S221", "S222", "S223", "S224", "S225", "S226", "S227"]


def _text(cell: str) -> str:
    return re.sub(r"<[^>]+>", " ", str(cell))


class DecisionRegisterAddendum(unittest.TestCase):
    def test_base_page_is_owned_elsewhere_and_still_present(self):
        self.assertIn("questions.html", C.PAGES)
        self.assertTrue((ROOT / "scripts/questions_data.py").exists())
        # This module must not define the page; it only appends to it.
        source = (ROOT / "scripts/questions_1111.py").read_text(encoding="utf-8")
        self.assertNotIn('c.PAGES["questions.html"] =', source)
        self.assertIn("_questions_1111.integrate", (ROOT / "scripts/dashboard_content.py").read_text(encoding="utf-8"))

    def test_base_rows_are_unchanged(self):
        questions = C.TABLES["questions"]["rows"]
        answers = C.TABLES["answers"]["rows"]
        discovery = C.TABLES["discovery"]["rows"]
        self.assertEqual(len(questions), 14)
        self.assertEqual([r["cells"][0] for r in questions], ["Q%02d" % i for i in range(1, 15)])
        self.assertEqual([r["cells"][0] for r in answers], ["A%02d" % i for i in range(1, 11)])
        self.assertEqual([r["cells"][0] for r in discovery], ["D%02d" % i for i in range(1, 10)])
        self.assertTrue(_text(answers[0]["cells"][1]).startswith("Which license classes"))
        self.assertTrue(_text(discovery[0]["cells"][1]).startswith("Original written quotes"))
        self.assertIn("S44", discovery[0]["src"])

    def test_added_rows_are_well_formed_and_sourced(self):
        for table_key, first_id, last_id in (("answers", "A07", "A10"), ("discovery", "D07", "D09")):
            table = C.TABLES[table_key]
            added = [r for r in table["rows"] if r["cells"][0] >= first_id]
            self.assertEqual([r["cells"][0] for r in added],
                             [first_id] + ["%s%02d" % (first_id[0], i) for i in range(int(first_id[1:]) + 1, int(last_id[1:]) + 1)])
            for row in added:
                self.assertEqual(len(row["cells"]), len(table["columns"]) - 1)
                self.assertTrue(row["src"])
                external = [s for s in row["src"] if C.SOURCES[s]["url"].startswith("https://")]
                self.assertTrue(external, row["cells"][0])
                self.assertIn("pill", row["cells"][3])
            # The appending session names itself in the caption.
            self.assertIn("2026-11-11", table["caption"])

    def test_new_sources_are_dated_official_reads(self):
        for sid in NEW_SOURCE_IDS:
            src = C.SOURCES[sid]
            self.assertEqual(src["checked"], CHECKED, sid)
            self.assertEqual(src["tier"], "official", sid)
            self.assertEqual(src["status"], "verified", sid)
            self.assertTrue(src["url"].startswith("https://"), sid)
            self.assertIn("2026-11-11", src["note"], sid)
        for sid, lic in (("S220", "829071"), ("S221", "1025814"), ("S222", "1003394")):
            self.assertIn("LicNum=" + lic, C.SOURCES[sid]["url"])
        self.assertIn("sectionNum=1954", C.SOURCES["S227"]["url"])

    def test_new_section_is_on_the_page(self):
        titles = [b.get("title") for b in C.PAGES["questions.html"]["sections"]]
        self.assertIn("Contract, insurance and access requirements (official, read 2026-11-11)", titles)
        self.assertEqual(C.PAGES["questions.html"]["sections"][-1]["type"], "callout")

    def test_integrate_is_idempotent(self):
        import questions_1111 as Q
        before_answers = len(C.TABLES["answers"]["rows"])
        before_findings = len(C.TABLES["findings"]["rows"])
        Q.integrate(C)
        self.assertEqual(len(C.TABLES["answers"]["rows"]), before_answers)
        self.assertEqual(len(C.TABLES["findings"]["rows"]), before_findings)

    def test_findings_record_the_drift_check_and_the_extension(self):
        ids = [r["cells"][0] for r in C.TABLES["findings"]["rows"]]
        self.assertIn("F20", ids)
        self.assertIn("F21", ids)
        f20 = [r for r in C.TABLES["findings"]["rows"] if r["cells"][0] == "F20"][0]
        self.assertIn("no drift", _text(f20["cells"][1]))
        for sid in ("S220", "S221", "S222", "S223"):
            self.assertIn(sid, f20["src"])

    def test_rendered_page_keeps_a_source_link_per_row(self):
        html = (ROOT / "questions.html").read_text(encoding="utf-8")
        bodies = re.findall(r"<tbody>(.*?)</tbody>", html, re.S)
        self.assertEqual(len(bodies), 3)
        for body in bodies:
            for i, row in enumerate(re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S), 1):
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
                self.assertIn("<a href=", cells[-1], "row %d source cell" % i)

    def test_no_private_hiring_wording_on_the_page(self):
        html = (ROOT / "questions.html").read_text(encoding="utf-8")
        for pattern in V.PRIVACY_PATTERNS:
            self.assertIsNone(re.search(pattern, html, re.I), pattern)

    def test_no_unsupported_provider_claims(self):
        text = " ".join(_text(c) for t in ("answers", "discovery")
                        for r in C.TABLES[t]["rows"] for c in r["cells"]).lower()
        for phrase in ("has accepted", "has agreed to", "the price is", "scheduled for"):
            self.assertNotIn(phrase, text)

    def test_dataset_validates(self):
        self.assertEqual(B.validate(), [])


if __name__ == "__main__":
    unittest.main()
