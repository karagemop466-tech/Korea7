"""Regression tests for licensing and verification caveats.

Originally written by session arena/14c34f19-korea7 for source IDs S62/U22.
Updated during the 2026-11-08 final integration to the canonical research IDs
S73/F26 while preserving the same assertions: incidental/supplemental work is
not excluded, the flag/source exist, and the verifier does not claim live checks.
"""
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
    assert content.SOURCES["S73"]["checked"] == "2026-11-08"
    assert "7059" in content.SOURCES["S73"]["url"]
    assert any(row["cells"][0] == "F26" and "S73" in row["src"]
               for row in content.TABLES["flags"]["rows"])


def test_verifier_does_not_claim_to_recheck_sources():
    verifier = (ROOT / "scripts" / "verify_dashboard.py").read_text(encoding="utf-8")
    assert "no network check" in verifier
    assert "verified 2026-11-07; %d sources verified overall" not in verifier
