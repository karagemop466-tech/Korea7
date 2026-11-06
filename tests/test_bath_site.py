"""Tests for the Bathtub Overflow Trip Lever project site (docs/bath/).

Verifies the project's own rules:
- data files parse and every data row carries an official source link;
- generated pages exist and every internal link resolves to a real file;
- every generated data table row contains at least one source link;
- no scheduling/regulatory-strategy discussion leaks into the public site;
- the executive summary stays numerically consistent with the data.
"""

import html as html_mod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATH = ROOT / "docs" / "bath"
DATA = BATH / "data"

PAGES = [
    "index.html",
    "executive-summary.html",
    "problem-scope.html",
    "technical-background.html",
    "estimates.html",
    "contractors.html",
    "analysis.html",
    "flagged-for-review.html",
    "sources.html",
]


def _load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _page(name):
    return (BATH / name).read_text(encoding="utf-8")


def _rows(html):
    """Split a generated HTML document into table-row chunks (tr..tr)."""
    return re.findall(r"<tr>.*?</tr>", html, flags=re.S)


# --------------------------------------------------------------------------- data layer

def test_data_files_parse_and_shapes():
    contractors = _load("contractors.json")["contractors"]
    estimates = _load("estimates.json")["estimates"]
    benchmarks = _load("benchmarks.json")["benchmarks"]
    flags = _load("flags.json")["flags"]
    assert len(contractors) == 8
    assert len(estimates) == 3
    assert len(benchmarks) >= 2
    assert len(flags) >= 10
    for c in contractors:
        assert re.fullmatch(r"\d{6,7}", c["license_number"]), c["name"]
        assert c["cslb_detail_url"].startswith("https://www.cslb.ca.gov/")
        assert str(c["license_number"]) in c["cslb_detail_url"]
        assert c["cslb_detail_url"].endswith("LicNum=" + c["license_number"])
        assert "C36" in " ".join(c["classifications"])
        assert c["website"].startswith("https://")
        assert c["yelp_url"].startswith("https://www.yelp.com/")
    for e in estimates:
        assert isinstance(e["amount_usd"], int) and e["amount_usd"] > 0
        assert e["verified"] is False
        assert e["source_type"] == "client-provided"
        assert e["company_profile_link"].startswith("https://www.cslb.ca.gov/")
    for b in benchmarks:
        assert b["url"].startswith("https://")
    for f in flags:
        assert f["detail"] and f["action"]
        assert f["source_url"].startswith("https://")
        assert f["source_label"]


def test_every_contractor_license_string_matches_cslb_url():
    """License numbers must only appear paired with their own CSLB detail URL."""
    for c in _load("contractors.json")["contractors"]:
        assert f'LicenseDetail.aspx?LicNum={c["license_number"]}' in c["cslb_detail_url"]


# --------------------------------------------------------------------------- generated site

def test_all_pages_exist():
    for name in PAGES:
        assert (BATH / name).is_file(), name
    assert (BATH / "assets" / "bath.css").is_file()
    assert (BATH / "executive-summary.md").is_file()


def test_internal_links_resolve():
    for name in PAGES:
        html = _page(name)
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            assert (BATH / target).is_file(), f"{name}: broken internal link {href}"


def test_every_data_table_row_has_source_link():
    """Each generated <tr> that carries project data must include an external source link."""
    for name in PAGES:
        html = _page(name)
        for row in _rows(html):
            has_header = "<th>" in row
            has_ext = re.search(r'href="https?://', row) is not None
            assert has_header or has_ext, f"{name}: table row without source link: {row[:120]}"


def test_no_strategy_leak():
    """The public site must not discuss regulatory/scheduling strategy."""
    banned = [
        r"without a permit",
        r"\bno permit\b",
        r"\bunpermitted\b",
        r"permit-free",
        r"skip(?:ping)? the permit",
        r"avoid(?:s|ing)? (?:a|the) permit",
    ]
    for name in PAGES:
        html = _page(name).lower()
        for pattern in banned:
            assert not re.search(pattern, html), f"{name}: banned phrase {pattern}"


def test_executive_summary_consistent_with_data():
    estimates = _load("estimates.json")["estimates"]
    contractors = _load("contractors.json")["contractors"]
    flags = _load("flags.json")["flags"]
    exec_md = (BATH / "executive-summary.md").read_text(encoding="utf-8")
    exec_html = _page("executive-summary.html")
    for e in estimates:
        assert f'${e["amount_usd"]}' in exec_md
        assert f'${e["amount_usd"]}' in exec_html
        assert e["company_name"] in exec_md
    for c in contractors:
        assert c["license_number"] in exec_md or c["license_number"] in exec_html
    assert str(len(contractors)) in exec_html
    assert str(len(flags)) in exec_html


def test_client_provided_amounts_labeled_not_verified():
    est_html = _page("estimates.html")
    for amount in (135, 550, 614):
        assert f"${amount}" in est_html
    assert "client-provided" in est_html
    assert "not independently verifiable" in est_html.lower() or "cannot be independently verified" in est_html.lower()


def test_contractors_page_carries_cslb_links_and_review_links():
    raw = _page("contractors.html")
    unescaped = html_mod.unescape(raw)
    contractors = _load("contractors.json")["contractors"]
    for c in contractors:
        assert c["cslb_detail_url"] in unescaped
        assert c["name"] in unescaped, c["id"]
    assert raw.count("yelp.com") >= len(contractors)


def test_flagged_page_lists_every_flag():
    flags = _load("flags.json")["flags"]
    unescaped = html_mod.unescape(_page("flagged-for-review.html"))
    for f in flags:
        assert f["title"] in unescaped, f["id"]


def test_sources_page_lists_every_registered_source():
    sources = _load("sources.json")["groups"]
    unescaped = html_mod.unescape(_page("sources.html"))
    for group in sources:
        for s in group["sources"]:
            assert s["url"] in unescaped, s["id"]
