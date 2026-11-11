#!/usr/bin/env python3
"""Regression checks for the 2026-11-11 known-vs-missing information inventory (arena/a4fcce50-korea7)."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import build_dashboard as B  # noqa: E402
import verify_dashboard as V  # noqa: E402
import info_inventory_1111 as INV  # noqa: E402


class InfoInventory1111Tests(unittest.TestCase):
    def test_page_and_navigation_wired(self):
        self.assertIn("info-inventory.html", C.PAGES)
        overview = next(g for g in C.NAV if g["group"] == "Overview")
        self.assertIn(("info-inventory.html", "Information inventory"), overview["links"])
        quick = next(b for b in C.PAGES["index.html"]["sections"] if b.get("type") == "quick")
        self.assertTrue(any(it.get("href") == "info-inventory.html" for it in quick["items"]))
        self.assertTrue(any("info-inventory.html" in b.get("html", "")
                            for b in C.PAGES["summary.html"]["sections"]))

    def test_all_three_tables_well_formed_and_blank_flagged(self):
        expected = {
            "info_have_vs_missing": (["I%02d" % i for i in range(1, 11)], 4),
            "staged_contract_rules": (["SC%02d" % i for i in range(1, 6)], 3),
            "discovery_protocol_1111": (["P%02d" % i for i in range(1, 7)], 4),
        }
        for tid, (ids, blank_col) in expected.items():
            table = C.TABLES[tid]
            self.assertEqual(table["columns"][-1], "Source")
            rows = table["rows"]
            self.assertEqual([r["cells"][0] for r in rows], ids)
            for row in rows:
                self.assertEqual(len(row["cells"]), len(table["columns"]) - 1)
                self.assertIn(C.BLANK, row["cells"][blank_col])
                self.assertIn(C.UNVERIFIED, row["cells"][blank_col])
                self.assertTrue(row["src"])
                self.assertTrue(any(
                    C.SOURCES[s]["tier"] in ("official", "manufacturer")
                    and C.SOURCES[s]["status"] == "verified"
                    for s in row["src"]
                ))
                joined = " ".join(row["cells"])
                for lic in re.findall(r"#(\d{6,8})", joined):
                    self.assertIn("LicNum=%s" % lic, joined)

    def test_r31_findings_and_fire_rating_flag_present(self):
        reqs = {r["cells"][0]: r for r in C.TABLES["requirements"]["rows"]}
        self.assertIn("R31", reqs)
        self.assertIn("questions, information", reqs["R31"]["cells"][1])

        fids = {r["cells"][0]: r for r in C.TABLES["findings"]["rows"]}
        self.assertIn("F22", fids)
        self.assertIn("F23", fids)
        self.assertIn("7159.10", fids["F22"]["cells"][1])
        self.assertIn("fire protection", fids["F23"]["cells"][1])

        flags = C.TABLES["flagged"]["rows"]
        fire_flags = [r for r in flags if "required for fire protection" in str(r["cells"][2])]
        self.assertEqual(len(fire_flags), 1)
        self.assertIn(C.UNVERIFIED, fire_flags[0]["cells"][-1])
        card = next(
            card for block in C.PAGES["index.html"]["sections"] if block["type"] == "cards"
            for card in block["items"] if card["k"] == "Flagged for review"
        )
        self.assertEqual(int(card["v"]), len(flags))

    def test_sources_and_json_artifact_match(self):
        artifact = json.loads((ROOT / "data/canonical/info-inventory-2026-11-11.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["meta"]["checked_date"], "2026-11-11")
        self.assertFalse(artifact["meta"]["provider_contacted"])
        self.assertFalse(artifact["meta"]["booking_confirmed"])
        self.assertIsNone(artifact["meta"]["verified_all_in_price"])
        for entry in artifact["direct_official_reads_2026_11_11"] + artifact["statutory_and_code_reads_2026_11_11"]:
            sid = entry["source_id"]
            self.assertIn(sid, C.SOURCES)
            self.assertEqual(C.SOURCES[sid]["url"], entry["url"])
            self.assertEqual(C.SOURCES[sid]["checked"], "2026-11-11")
            self.assertEqual(C.SOURCES[sid]["status"], "verified")

    def test_integrate_is_idempotent(self):
        before_reqs = len(C.TABLES["requirements"]["rows"])
        before_findings = len(C.TABLES["findings"]["rows"])
        before_flags = len(C.TABLES["flagged"]["rows"])
        INV.integrate(C)
        self.assertEqual(len(C.TABLES["requirements"]["rows"]), before_reqs)
        self.assertEqual(len(C.TABLES["findings"]["rows"]), before_findings)
        self.assertEqual(len(C.TABLES["flagged"]["rows"]), before_flags)

    def test_rendered_page_and_privacy_clean(self):
        html = (ROOT / "info-inventory.html").read_text(encoding="utf-8")
        bodies = re.findall(r"<tbody>(.*?)</tbody>", html, re.S)
        self.assertEqual(len(bodies), 3)
        for body in bodies:
            for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
                self.assertIn("<a href=", cells[-1])
        artifact_txt = (ROOT / "data/canonical/info-inventory-2026-11-11.json").read_text(encoding="utf-8")
        for pat in V.PRIVACY_PATTERNS:
            self.assertIsNone(re.search(pat, html, re.I), pat)
            self.assertIsNone(re.search(pat, artifact_txt, re.I), pat)
        self.assertEqual(B.validate(), [])


if __name__ == "__main__":
    unittest.main()
