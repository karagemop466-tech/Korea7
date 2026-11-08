"""Regression tests for the shortlist's licensing and verification caveats."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dashboard_content as content


def test_shortlist_does_not_exclude_incidental_work():
    page = (ROOT / "shortlist.html").read_text(encoding="utf-8")
    assert "incidental and supplemental" in page
    assert "sectionNum=7059." in page
    assert "not automatically required" in page
    assert "specific job coverage unverified" in page
    assert "ceiling patch needs a second trade" not in page


def test_review_flag_and_source_are_in_generator():
    assert content.SOURCES["S61"]["checked"] == "2026-11-08"
    assert any(row["cells"][0] == "U21" and "S61" in row["src"]
               for row in content.TABLES["flagged"]["rows"])


def test_verifier_does_not_claim_to_recheck_sources():
    verifier = (ROOT / "scripts" / "verify_dashboard.py").read_text(encoding="utf-8")
    assert "not live checks" in verifier
    assert "verified 2026-11-07; %d sources verified overall" not in verifier
