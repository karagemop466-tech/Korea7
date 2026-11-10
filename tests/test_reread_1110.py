"""Regression checks for the 2026-11-10 §104.2 exemption page.

Run:  python3 -m pytest -q tests/test_reread_1110.py
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
import reread_1110 as R  # noqa: E402


def plain(fragment: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip()


class ExemptWorkPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        B.build_source_ledger_rows()

    def test_nine_items_in_official_order(self):
        rows = C.TABLES["exempt_list"]["rows"]
        self.assertEqual(len(rows), 9)
        self.assertEqual([plain(r["cells"][0]) for r in rows],
                         [str(i) for i in range(1, 10)])
        # First and last items must match the official text word for word.
        self.assertEqual(plain(rows[0]["cells"][1]),
                         "Repair of leaks not requiring cutting into or removing piping.")
        self.assertEqual(plain(rows[8]["cells"][1]),
                         "Work performed in buildings or structures owned and occupied by the "
                         "State and Federal governments.")

    def test_every_row_cites_the_official_pdf(self):
        for i, row in enumerate(C.TABLES["exempt_list"]["rows"], 1):
            self.assertEqual(row["src"], ["S96"], "row %d must cite the official code PDF" % i)
            self.assertIn("api.sf.gov", C.SOURCES["S96"]["url"])
            self.assertEqual(C.SOURCES["S96"]["tier"], "official")

    def test_interpretation_is_labelled_not_presented_as_code(self):
        """The site must not put its own reading in the official-text column."""
        for row in C.TABLES["exempt_list"]["rows"]:
            self.assertTrue(row["cells"][1].startswith("<q>"),
                            "verbatim column must be a quotation")
            self.assertNotIn("this project’s reading", row["cells"][1])
            self.assertIn("this project’s reading", row["cells"][2])

    def test_amendment_scope_stated(self):
        text = " ".join(plain(c) for r in C.TABLES["amendment_scope"]["rows"] for c in r["cells"])
        self.assertIn("Replace Section 104.2(1) and the first paragraph of Section 104.2(2)", text)
        self.assertIn("fee", text.lower())

    def test_page_exists_and_is_navigable(self):
        self.assertIn("exempt-work.html", C.PAGES)
        reference = [grp for grp in C.NAV if grp["group"] == "Reference"][0]
        hrefs = [h for h, _ in reference["links"]]
        self.assertIn("exempt-work.html", hrefs)
        self.assertEqual(hrefs[hrefs.index("permits.html") + 1], "exempt-work.html")

    def test_permit_page_points_at_published_wording(self):
        rows = C.TABLES["permits"]["rows"]
        topics = [r["cells"][0] for r in rows]
        self.assertIn("Exempt-work list (§104.2) — now quoted in full", topics)
        pointer = [r for r in rows if r["cells"][0] == "Exempt-work pointer"][0]
        self.assertIn("exempt-work.html", C.TABLES["permits"]["caption"])

    def test_open_question_is_flagged(self):
        flags = C.TABLES["flagged"]["rows"]
        match = [r for r in flags if "Permit exemption for this exact repair" in str(r["cells"][1])]
        self.assertEqual(len(match), 1)
        self.assertIn(C.UNVERIFIED, match[0]["cells"][-1])
        # IDs stay unique after the append.
        ids = [str(r["cells"][0]) for r in flags]
        self.assertEqual(len(ids), len(set(ids)))

    def test_rendered_page_carries_no_permit_strategy_wording(self):
        text = (ROOT / "exempt-work.html").read_text(encoding="utf-8")
        for pat in ("without a permit", "no permit needed", "skip the permit",
                    "internal use", "private reason"):
            self.assertNotIn(pat, text.lower())
        self.assertIn("Nothing here is legal advice", text)

    def test_privacy_patterns_clean_for_new_content(self):
        blob = "\n".join(
            " ".join(r["cells"]) for tid in ("exempt_list", "amendment_scope", "source_basis")
            for r in C.TABLES[tid]["rows"])
        blob += "\n" + "\n".join(b.get("html", "")
                                 for b in C.PAGES["exempt-work.html"]["sections"])
        import verify_dashboard as V
        for pat in V.PRIVACY_PATTERNS:
            self.assertIsNone(re.search(pat, blob, re.I),
                              "privacy pattern matched in new content: %s" % pat)

    def test_new_sources_are_dated_reads_not_relabelled_history(self):
        for sid in ("S112", "S113"):
            self.assertEqual(C.SOURCES[sid]["checked"], "2026-11-10")
            self.assertEqual(C.SOURCES[sid]["tier"], "official")
            self.assertEqual(C.SOURCES[sid]["status"], "verified")
            self.assertTrue(C.SOURCES[sid]["url"].startswith("https://www2.cslb.ca.gov/"))


if __name__ == "__main__":
    unittest.main()
