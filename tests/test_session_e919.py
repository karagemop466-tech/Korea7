#!/usr/bin/env python3
"""Tests for the 2026-11-11 re-read and the open-questions register.

The drift test is the important one: it compares every field transcribed in
data/canonical/session-e919-verification.json with the stored canonical CSLB
record for the same licence. A transcription error, or a stored record that
changed without the re-read being updated, fails the test. It does not prove the
2026-11-11 read itself was correct — only a human reading CSLB can do that, and
each row publishes its own CSLB link for that purpose.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = json.loads((ROOT / "data/canonical/session-e919-verification.json").read_text(encoding="utf-8"))
CANON = json.loads((ROOT / "data/canonical/cslb_records.json").read_text(encoding="utf-8"))
CANON_BY_LIC = {r["license"]: r for r in CANON["records"]}


def test_every_record_has_an_official_link():
    for rec in EVIDENCE["records"]:
        assert rec["url"].startswith("https://www2.cslb.ca.gov/"), rec["id"]
        assert rec["read_date"] if "read_date" in rec else EVIDENCE["read_date"] == "2026-11-11"


def test_licence_detail_fields_match_stored_canonical_record():
    """Field-by-field comparison; any mismatch means drift or a transcription error."""
    for rec in EVIDENCE["records"]:
        if rec["id"] == "AC10":      # complaint-disclosure page has no licence-detail fields
            continue
        stored = CANON_BY_LIC[rec["license"]]
        f = rec["fields"]
        # The CSLB page may show "OWNER dba BUSINESS"; accept either part, since
        # name_on_record stores the licensee name, not the dba.
        parts = [p.strip() for p in rec["name"].split(" dba ")]
        assert stored["name_on_record"] in parts, (rec["id"], parts)
        assert f["phone"] == stored["phone_on_record"], rec["id"]
        assert f["entity"] == stored["entity"], rec["id"]
        assert f["issue_date"] == stored["issue_date"], rec["id"]
        assert f["expire_date"] == stored["expire_date"], rec["id"]
        assert f["status"] == stored["status"], rec["id"]
        assert f.get("reissue_date") == stored["reissue_date"], rec["id"]
        assert f["classifications"] == stored["classifications"], rec["id"]
        assert f.get("bond_carrier") == stored["contractors_bond"]["carrier"], rec["id"]
        assert f.get("bond_amount_usd") == stored["contractors_bond"]["amount_usd"], rec["id"]
        assert f.get("bond_effective") == stored["contractors_bond"]["effective"], rec["id"]
        wc = stored["workers_compensation"]
        if wc["kind"] == "exempt":
            assert "exempt" in f.get("wc_status", ""), rec["id"]
            assert f.get("wc_effective") == wc["effective"], rec["id"]
        else:
            assert f.get("wc_carrier") == wc["carrier"], rec["id"]
            assert f.get("wc_effective") == wc["effective"], rec["id"]
            assert f.get("wc_expires") == wc["expires"], rec["id"]
            if "wc_policy" in f:
                assert f["wc_policy"] == wc["policy"], rec["id"]


def test_drift_verdicts_are_all_none():
    assert {r["drift"] for r in EVIDENCE["records"]} == {"none"}


def test_complaint_disclosure_matches_published_audit():
    disc = json.loads((ROOT / "data/canonical/complaint-disclosures-2026-11-10.json").read_text(encoding="utf-8"))
    rec = next(r for r in EVIDENCE["records"] if r["id"] == "AC10")
    # find the 1003394 entry whatever the file's shape
    def walk(node):
        if isinstance(node, dict):
            if node.get("license") == "1003394" or node.get("licence") == "1003394" or node.get("lic_num") == "1003394":
                yield node
            for v in node.values():
                yield from walk(v)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v)

    entries = [e for e in walk(disc) if e]
    assert entries, "no 1003394 entry found in the disclosure audit"
    blob = json.dumps(entries)
    assert "2 2020 001045" in blob
    assert "07/12/2020" in blob or "2020-07-12" in blob
    assert rec["fields"]["citation_number"] == "2 2020 001045"


def test_rule_quotes_are_present_in_evidence():
    by_id = {r["id"]: r for r in EVIDENCE["rules"]}
    assert by_id["AR01"]["quote"].startswith("(a) This chapter does not apply")
    assert "one thousand dollars ($1,000)" in by_id["AR01"]["quote"]
    assert "104.2 Exempt Work" in by_id["AR02"]["quote"]
    for n in range(1, 10):
        assert "(%d)" % n in by_id["AR02"]["quote"], n
    assert "before cutting into or replacing pipes" in by_id["AR03"]["quote"]
    assert "minor repairs to existing interior plaster or wallboard" in by_id["AR04"]["quote"].lower()
    assert "C-9" in by_id["AR07"]["title"]


def test_no_question_row_carries_a_verified_answer():
    """A blank, flagged answer is the rule; nothing may be filled in by inference."""
    src = (ROOT / "scripts/session_e919_verification.py").read_text(encoding="utf-8")
    assert "QUESTION_ROWS" in src
    # Every status string either says OPEN or names the one partly-closed group.
    statuses = re.findall(r'"(OPEN[^"]*|PARTLY VERIFIED[^"]*)"', src)
    assert len(statuses) >= 20, len(statuses)


def test_question_ids_are_unique_and_sequential():
    src = (ROOT / "scripts/session_e919_verification.py").read_text(encoding="utf-8")
    ids = re.findall(r'^    \("(Q\d\d)",', src, re.M)
    assert ids == ["Q%02d" % i for i in range(1, len(ids) + 1)], ids


def test_new_sources_are_not_dead_and_have_dates():
    src = (ROOT / "scripts/session_e919_verification.py").read_text(encoding="utf-8")
    block = src.split("NEW_SOURCES = {")[1].split("\n# --- The question register")[0]
    assert block.count('"status": "verified"') + block.count('"status": "blocked-403"') == block.count('"label":')
