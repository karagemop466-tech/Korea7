"""Regression checks for the 2026-11-10 final integration gate.

Session arena/bfea234e-korea7 re-read every CSLB record and rule page directly and
published corrections. These tests lock in the properties that a re-run of the
generator can otherwise silently break: unique row IDs, cross-references that point
at rows that exist, and value/count claims that match the official transcription.
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import verify_dashboard as V  # noqa: E402
import ranking_data as R  # noqa: E402

RECHECK = json.loads((ROOT / "data/canonical/reverification-2026-11-10.json").read_text(encoding="utf-8"))


def _rows(table):
    return C.TABLES[table]["rows"]


def test_every_row_id_is_unique():
    for table, prefix in (("findings", "F"), ("flagged", "U")):
        ids = [r["cells"][0] for r in _rows(table) if re.fullmatch(prefix + r"\d+", str(r["cells"][0]))]
        duplicates = [k for k, v in Counter(ids).items() if v > 1]
        assert not duplicates, (table, duplicates)


def test_duplicate_finding_id_repair_is_documented():
    """The legacy F10 row keeps its ID; the exemption row was re-labelled and is explained."""
    findings = {r["cells"][0]: r for r in _rows("findings")}
    assert "unrelated legacy project" in findings["F10"]["cells"][1]
    assert "exemption" in findings["F17"]["cells"][1].lower()
    assert any(r["cells"][0] == "U49" and "F10" in r["cells"][1] for r in _rows("flagged"))


def test_flag_range_label_covers_the_highest_flag():
    highest = max(int(r["cells"][0][1:]) for r in _rows("flagged") if re.fullmatch(r"U\d+", str(r["cells"][0])))
    text = " ".join(str(v) for page in C.PAGES.values() for block in page["sections"]
                    for v in block.values() if isinstance(v, str))
    assert "U01–U%d" % highest in text
    assert "U01–U%d" % (highest + 1) not in text


def test_exemption_count_matches_official_records():
    exempt = {r["license"] for r in RECHECK["licenses"] if r["workers_comp_kind"] == "exempt"}
    assert exempt == {"757796", "959843", "1115649", "841229", "632743"}
    u06 = next(r for r in _rows("flagged") if r["cells"][0] == "U06")
    for lic in exempt:
        assert lic in u06["cells"][1]
    assert "five" in u06["cells"][2].lower()


def test_reread_table_matches_the_transcription_exactly():
    table = C.TABLES["reread_1110"]
    assert len(table["rows"]) == 16
    by_license = {r["license"]: r for r in RECHECK["licenses"]}
    for row in table["rows"]:
        lic = re.sub(r"\D", "", row["cells"][0])
        record = by_license[lic]
        assert html.unescape(record["name_on_record"]) in html.unescape(row["cells"][1])
        assert record["phone_on_record"] in row["cells"][2]
        assert record["expire_date"] in row["cells"][5]
        assert record["record_stamp"].split(" as of ")[1].split(" ")[0] in row["cells"][3]


def test_all_sixteen_records_are_active_on_the_official_read():
    assert len(RECHECK["licenses"]) == 16
    assert {r["status"] for r in RECHECK["licenses"]} == {"current and active"}
    assert all(r["record_stamp"].startswith("Data current as of 11/9/2026 ") for r in RECHECK["licenses"])


def test_rule_rows_cite_official_sources_only():
    for row in C.TABLES["rules_reread_1110"]["rows"]:
        for sid in row["src"]:
            assert C.SOURCES[sid]["tier"] in ("official", "manufacturer"), sid
            assert C.SOURCES[sid]["status"] == "verified", sid


def test_no_private_permit_rationale_anywhere_public():
    blob = ROOT.joinpath("flagged.html").read_text(encoding="utf-8", errors="ignore")
    blob += ROOT.joinpath("summary.html").read_text(encoding="utf-8", errors="ignore")
    for pattern in V.PRIVACY_PATTERNS:
        assert not re.search(pattern, blob, re.I), pattern


def test_no_source_id_is_redefined_by_a_later_session():
    """Later supplements must add new ids, never overwrite another module's source."""
    labels = {sid: src["label"] for sid, src in C.SOURCES.items()}
    for sid in ("S105", "S106", "S111"):
        assert sid in labels
    assert "November 10 selected-field read" in labels["S105"]
    assert "Handyman" in labels["S111"] or len(labels["S111"]) > 0
    assert labels["S112"].startswith("Re-verification log 2026-11-10")
    assert C.SOURCES["S112"]["url"] == "data/canonical/reverification-2026-11-10.json"


def test_mannys_insurance_claim_is_flagged_not_resolved():
    row = next(r for r in _rows("flagged") if r["cells"][0] == "U48")
    assert "841229" in row["cells"][2]
    assert "UNVERIFIED" in row["cells"][4]
    assert "S57" in row["src"] and "S75" in row["src"]
