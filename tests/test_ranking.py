#!/usr/bin/env python3
"""Integrity checks for the ranked hiring decision and the verified contact directory.

Session arena/0e9ee506-korea7, 2026-11-08.

Enforces the project's rules on the new pages:
  * every score input is a field on an official CSLB record, and the published
    order is exactly the order the committed data produces;
  * review ratings / counts and vendor marketing never enter the score;
  * every candidate's published phone matches the CSLB record it cites;
  * every cost cell is blank and flagged, because no official price exists;
  * every table row on the new pages carries a source link and every internal
    link resolves.

Run:  python3 -m pytest -q tests/test_ranking.py   (or python3 tests/test_ranking.py)
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import ranking_data as R  # noqa: E402

NEW_PAGES = ("ranking.html", "contacts.html")
RANK_TABLES = ("rank_allinone", "rank_plumbing", "rank_restoration")


class TestScoring(unittest.TestCase):
    def test_weights_total_one_hundred(self):
        self.assertEqual(sum(c[2] for c in R.CRITERIA), 100)

    def test_score_is_sum_of_published_criteria(self):
        for lic, s in R.SCORES.items():
            self.assertEqual(s["total"], sum(s[k] for k in "ABCDE"), lic)
            for key, _, maximum, _, _ in R.CRITERIA:
                self.assertLessEqual(s[key], maximum, "%s criterion %s" % (lic, key))
                self.assertGreaterEqual(s[key], 0)

    def test_scores_are_reproducible_from_committed_json(self):
        raw = json.loads((ROOT / "data/canonical/cslb_records.json").read_text(encoding="utf-8"))
        recomputed = {r["license"]: R.score(r)["total"] for r in raw["records"]}
        self.assertEqual(recomputed, {l: s["total"] for l, s in R.SCORES.items()})

    def test_review_data_cannot_change_a_score(self):
        """The scorer takes only a CSLB record; platform data is a separate file."""
        before = {l: s["total"] for l, s in R.SCORES.items()}
        saved = json.loads(json.dumps(R.REVIEWS))
        for snap in R.REVIEWS["snapshots"]:
            snap["rating"] = "1.0"
            snap["review_count"] = "0"
        after = {l: R.score(r)["total"] for l, r in R.RECORDS.items()}
        R.REVIEWS.clear()
        R.REVIEWS.update(saved)
        self.assertEqual(before, after)

    def test_role_gate_matches_classifications(self):
        for lic, r in R.RECORDS.items():
            cl = set(r["classifications"])
            if "C36" in cl and ("B" in cl or "C-9" in cl):
                self.assertIn(lic, R.ALL_IN_ONE)
            elif "C36" in cl:
                self.assertIn(lic, R.PLUMBING_ONLY)
                self.assertNotIn(lic, R.ALL_IN_ONE)
            else:
                self.assertIn(lic, R.RESTORATION)
        self.assertEqual(len(R.ALL_IN_ONE) + len(R.PLUMBING_ONLY) + len(R.RESTORATION),
                         len(R.RECORDS))

    def test_order_is_sorted_and_tie_broken(self):
        for group in (R.ALL_IN_ONE, R.PLUMBING_ONLY, R.RESTORATION):
            keys = [(-R.SCORES[l]["total"], R.RECORDS[l]["issue_date"], int(l)) for l in group]
            self.assertEqual(keys, sorted(keys))

    def test_disclosure_and_status_penalties_applied(self):
        self.assertEqual(R.SCORES["1003394"]["C"], 5)    # complaint disclosure
        self.assertEqual(R.SCORES["1009195"]["C"], 0)    # additional status warning
        self.assertEqual(R.SCORES["829071"]["C"], 15)    # clean

    def test_expiring_workers_compensation_penalised(self):
        self.assertEqual(R.SCORES["1024971"]["B"], 15)   # expires 2026-12-18
        self.assertEqual(R.SCORES["1075566"]["B"], 15)   # expires 2026-12-02
        self.assertEqual(R.SCORES["829071"]["B"], 25)
        self.assertEqual(R.SCORES["959843"]["B"], 10)    # exempt


class TestPublishedTables(unittest.TestCase):
    def test_every_record_has_a_matching_official_source(self):
        for lic, sid in R.LICENSE_SRC.items():
            self.assertIn(sid, C.SOURCES, lic)
            self.assertEqual(C.SOURCES[sid]["url"], R.RECORDS[lic]["source_url"], lic)
            self.assertEqual(C.SOURCES[sid]["tier"], "official", lic)
            self.assertEqual(C.SOURCES[sid]["checked"], "2026-11-08", lic)

    def test_rank_tables_cover_every_candidate_once(self):
        seen = []
        for tid in RANK_TABLES:
            for row in C.TABLES[tid]["rows"]:
                seen += re.findall(r"LicNum=(\d+)", " ".join(row["cells"]))
        self.assertEqual(sorted(set(seen)), sorted(R.RECORDS))
        self.assertEqual(len(seen), len(R.RECORDS))

    def test_every_cost_cell_is_blank_and_flagged(self):
        for tid in RANK_TABLES:
            idx = C.TABLES[tid]["columns"].index("Cost position")
            for i, row in enumerate(C.TABLES[tid]["rows"], 1):
                cell = row["cells"][idx]
                self.assertIn(C.BLANK, cell, "%s row %d" % (tid, i))
                self.assertIn("UNVERIFIED", cell, "%s row %d" % (tid, i))
                self.assertNotIn("$614", cell)
                self.assertNotIn("$550", cell)
                self.assertNotIn("$135", cell)

    def test_contact_phones_match_the_cslb_record(self):
        table = C.TABLES["contacts"]
        self.assertEqual(len(table["rows"]), len(R.RECORDS))
        for row in table["rows"]:
            nums = re.findall(r"LicNum=(\d+)", " ".join(row["cells"]))
            self.assertEqual(len(nums), 1)
            self.assertIn(R.RECORDS[nums[0]]["phone_on_record"], row["cells"][1])

    def test_unverified_sites_stay_blank(self):
        table = C.TABLES["contacts"]
        for row in table["rows"]:
            lic = re.findall(r"LicNum=(\d+)", " ".join(row["cells"]))[0]
            if lic not in R.SITES:
                self.assertIn(C.BLANK, row["cells"][2])
                self.assertIn("UNVERIFIED", row["cells"][2])
                self.assertIn(C.BLANK, row["cells"][3])

    def test_no_outreach_claim_on_new_pages(self):
        text = (ROOT / "ranking.html").read_text(encoding="utf-8")
        self.assertIn("No provider has been contacted", text)
        self.assertIn("none has confirmed this job", text)

    def test_new_flag_ids_are_unique_and_extend_the_range(self):
        ids = [r["cells"][0] for r in C.TABLES["flagged"]["rows"]]
        self.assertEqual(len(ids), len(set(ids)))
        for cells, _ in R.NEW_FLAGS:
            self.assertIn(cells[0], ids)


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.rows = [], set(), []
        self.in_body = self.in_row = False
        self.row_links = []
        self.row_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "tbody":
            self.in_body = True
        if tag == "tr" and self.in_body:
            self.in_row, self.row_links, self.row_text = True, [], []
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append(attrs["href"])
            if self.in_row:
                self.row_links.append(attrs["href"])

    def handle_data(self, data):
        if self.in_row:
            self.row_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.rows.append((self.row_links, " ".join(self.row_text).lower()))
            self.in_row = False
        if tag == "tbody":
            self.in_body = False


class TestNewPages(unittest.TestCase):
    def test_every_row_links_a_source_and_internal_links_resolve(self):
        for name in NEW_PAGES:
            with self.subTest(page=name):
                scan = Scan()
                scan.feed((ROOT / name).read_text(encoding="utf-8"))
                self.assertTrue(scan.rows, name)
                for links, text in scan.rows:
                    self.assertTrue(links, "%s: row without a source link" % name)
                    # A stated licence number must always link to its official record.
                    for num in re.findall(r"#(\d{6,8})", text):
                        self.assertIn("LicNum=%s" % num, " ".join(links),
                                      "%s: #%s without a CSLB link" % (name, num))
                    # Platform rows must be labelled third-party.
                    if any(urlparse(h).hostname == "www.yelp.com" for h in links):
                        self.assertIn("third-party", text, "%s: unlabelled platform row" % name)
                for href in scan.links:
                    url = urlparse(href)
                    if url.scheme or url.netloc:
                        continue
                    target = (ROOT / (unquote(url.path) or name)).resolve()
                    self.assertTrue(target.is_file(), (name, href))

    def test_pages_are_in_the_navigation(self):
        hrefs = {h for g in C.NAV for h, _ in g["links"]}
        for name in NEW_PAGES:
            self.assertIn(name, hrefs)
            self.assertIn(name, C.PAGES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
