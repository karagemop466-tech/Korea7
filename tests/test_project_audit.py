"""Regression checks for the 2026-11-08 research dataset and repository audit."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import audit_project as A  # noqa: E402

OUT = ROOT / "data" / "review-2026-11-08"


def test_research_dataset_loads_and_is_canonical_source():
    data = json.loads((OUT / "research.json").read_text(encoding="utf-8"))
    assert data == C.DATA
    assert data["meta"]["updated"] == "2026-11-08"
    assert len(data["sources"]) == 75
    assert len(data["contractors"]) == 11
    assert len(data["estimates"]) == 3
    assert len(data["requirements"]) == 34
    assert len(data["flags"]) == 27


def test_source_ids_are_unique_and_statuses_are_bounded():
    ids = list(C.SOURCES)
    assert len(ids) == len(set(ids))
    allowed = {"verified", "blocked-403", "indexed-snapshot", "dead", "removed"}
    for sid, src in C.SOURCES.items():
        assert src["status"] in allowed, sid
        assert src["tier"] in {"official", "manufacturer", "company", "platform", "publisher", "primary"}, sid
        assert src["checked"] == "2026-11-08" or src["status"] in {"dead", "removed"}, sid


def test_ranking_is_interview_order_not_price_sort():
    ranked = sorted([c for c in C.CONTRACTORS if c["rank"]], key=lambda c: c["rank"])
    assert [c["rank"] for c in ranked] == list(range(1, 10))
    assert ranked[0]["id"] == "general-sf"
    assert ranked[1]["id"] == "handyman-heroes"
    assert ranked[2]["id"] == "ace"
    # The three reported quotes are not used as comparable combined-scope prices.
    assert [c["id"] for c in ranked[-3:]] == ["expert", "bay-area", "fast-response"]
    for c in ranked:
        assert c["rationale"] and c["caution"]
        assert c["cost"]


def test_unranked_leads_stay_flagged():
    unranked = {c["id"]: c for c in C.CONTRACTORS if not c["rank"]}
    assert set(unranked) == {"sugar-bear", "szeto"}
    assert "entity" in unranked["sugar-bear"]["caution"].lower()
    assert not unranked["szeto"]["license"]


def test_estimates_have_blank_verified_amounts_in_generated_site():
    html = (ROOT / "estimates.html").read_text(encoding="utf-8")
    assert html.count('class="blank"') >= 3
    assert html.count("UNVERIFIED") >= 3
    for amount in ("$614", "$550", "$135"):
        assert amount in html
    assert "reported" in html and "verified amount" in html.lower()


def test_audit_artifacts_exist_and_reference_resolves():
    for name in ("REPO-AUDIT.md", "repo_inventory.json", "repo_findings.json"):
        assert (OUT / name).exists(), name
    assert C.SOURCES["S72"]["url"].endswith("REPO-AUDIT.md")
    assert (ROOT / C.SOURCES["S72"]["url"]).exists()


def test_audit_findings_are_clean_except_documented_directory_warning():
    findings = json.loads((OUT / "repo_findings.json").read_text(encoding="utf-8"))
    assert findings["json_errors"] == []
    assert findings["python_errors"] == []
    assert findings["privacy_hits"] == []
    assert findings["broken_file_links"] == []
    assert findings["directory_links_without_index"] == [
        {"page": "docs/parallel-index.html", "url": "results/", "target": "docs/results"}
    ]
    assert findings["tracked_files"] > 300


def test_inventory_hashes_match_saved_bytes_for_canonical_files():
    inventory = json.loads((OUT / "repo_inventory.json").read_text(encoding="utf-8"))
    by_path = {e["path"]: e for e in inventory["files"]}
    for rel in ("index.html", "scripts/dashboard_content.py", "data/review-2026-11-08/research.json"):
        entry = by_path[rel]
        assert entry["sha256"] == hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def test_audit_categories_cover_canonical_pages():
    for page in A.CANONICAL_PAGES:
        assert A.category(page) == "canonical-dashboard"
    assert A.category("data/review-2026-11-08/research.json") == "current-audit"
    assert A.category("gems/anything.txt") == "legacy-or-other"
