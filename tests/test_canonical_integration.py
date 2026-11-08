"""Regression checks for the 2026-11-08 source-first canonical integration."""
from __future__ import annotations
import html
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dashboard_content as C
import verify_dashboard as V


class CanonicalIntegration(unittest.TestCase):
    def test_owner_amounts_are_blank_in_verified_cells(self):
        for r in C.TABLES["estimates"]["rows"]:
            self.assertEqual(r["cells"][2], C.UNKNOWN)
            self.assertEqual(r["cells"][3], C.UNKNOWN)
        amounts = {html.unescape(r["cells"][0]): r["cells"][1] for r in C.TABLES["brief_quotes"]["rows"]}
        self.assertIn("$614", amounts["Expert Plumbing Solutions"])
        self.assertIn("$550", amounts["Bay Area Plumbing"])
        self.assertIn("$135", amounts["Fast Response Plumbing & Rooter"])

    def test_ranking_costs_and_blocked_reviews_remain_blank(self):
        for r in C.TABLES["ranking"]["rows"]:
            self.assertEqual(r["cells"][4], C.UNKNOWN)
        for r in C.TABLES["reviews"]["rows"]:
            self.assertEqual(r["cells"][2], C.UNKNOWN)
            self.assertEqual(r["cells"][3], C.UNKNOWN)

    def test_drywall_inclusion_is_not_assumed_excluded(self):
        text = (ROOT / "estimates.html").read_text() + (ROOT / "EXECUTIVE-SUMMARY.md").read_text()
        self.assertNotIn("None of the three scopes includes drywall", text)
        self.assertIn("not stated", text)

    def test_license_register_matches_direct_read_evidence(self):
        self.assertEqual(V.validate_content(C), [])

    def test_every_canonical_row_has_role_labeled_sources(self):
        for key, table in C.TABLES.items():
            for r in table["rows"]:
                self.assertEqual(V.row_issues(key, r, C), [], (key, r["cells"][0]))
                self.assertTrue(r["src"])

    def test_build_is_idempotent_for_html(self):
        pages = list(C.PAGES) + ["shortlist.html"]
        before = {p: (ROOT / p).read_bytes() for p in pages}
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_dashboard.py")], check=True, capture_output=True)
        after = {p: (ROOT / p).read_bytes() for p in pages}
        self.assertEqual(before, after)

    def test_pages_workflow_has_required_permissions(self):
        workflow = (ROOT / ".github/workflows/pages-check.yml").read_text()
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("needs: validate", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)

    def test_audit_artifacts_exist_and_parse(self):
        for name in ("repo_audit.json", "repo_line_inventory.json", "source_evidence.json", "site_data.json"):
            json.loads((ROOT / "data/canonical" / name).read_text())


if __name__ == "__main__":
    unittest.main()
