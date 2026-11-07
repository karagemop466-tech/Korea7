"""Tests for the canonical Bathtub Overflow Trip Lever site (repository root).

The project's own rules, enforced:

* every data row that names a company carries an official CSLB link;
* a licence value is either a real CSLB record or blank — never guessed;
* every table row in the generated pages carries a link (an external source, or a
  documented cross-reference) or is explicitly labelled owner-provided;
* every internal link and anchor resolves;
* no wording about permit strategy, private reasons or confidential constraints
  leaks into the published pages;
* the executive summary's numbers agree with the data files;
* the generated HTML is well-formed and deterministic.
"""

from __future__ import annotations

import html as html_mod
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "overflow"

PAGES = [
    "index.html",
    "summary.html",
    "shortlist.html",
    "estimates.html",
    "contractors.html",
    "findings.html",
    "plan.html",
    "verification.html",
    "sources.html",
    "flagged.html",
]


# --------------------------------------------------------------------------- helpers
def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def page(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def rows_of(document: str):
    """Yield every <tr> chunk inside a tbody."""
    for body in re.findall(r"<tbody>(.*?)</tbody>", document, flags=re.S):
        for row in re.findall(r"<tr>.*?</tr>", body, flags=re.S):
            yield row


class _Balance(HTMLParser):
    """Very small tag-balance checker for the elements this site uses."""

    VOID = {"br", "img", "meta", "link", "input", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}>")
            return
        if self.stack[-1] != tag:
            self.errors.append(f"expected </{self.stack[-1]}> but found </{tag}>")
            # recover
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()


# --------------------------------------------------------------------------- data layer
def test_data_files_parse_and_have_expected_shapes():
    contractors = load("contractors.json")["records"]
    estimates = load("estimates.json")["estimates"]
    benchmarks = load("benchmarks.json")["benchmarks"]
    flags = load("flags.json")["flags"]
    sources = load("sources.json")["sources"]

    assert len(contractors) == 11
    assert len(estimates) == 3
    assert len(benchmarks) >= 6
    assert len(flags) >= 15
    assert len(sources) >= 40

    assert [e["amount"] for e in estimates] == [614, 550, 135]
    assert all(e["amount_status"] == "owner-provided" for e in estimates)
    assert all(e["official_confirmation"] is None for e in estimates)
    assert all(e["source_url"].startswith("https://www.cslb.ca.gov/") for e in estimates)


def test_licence_is_either_a_cslb_record_or_blank():
    for c in load("contractors.json")["records"]:
        if c["license"]:
            assert re.fullmatch(r"\d{6,7}", c["license"]), c["name"]
            assert c["license"] in c["cslb_url"]
            assert c["cslb_url"].startswith("https://www.cslb.ca.gov/")
            assert c["cslb_status"] == "current and active", c["name"]
            assert c["classes"], c["name"]
        else:
            # blank means blank: no invented status, dates or classifications
            assert c["cslb_status"] == ""
            assert c["expires"] == ""
            assert c["classes"] == []
            assert c["flags"], f"{c['name']} has no licence and no flag"


def test_every_contractor_names_an_official_record_and_a_review_link():
    for c in load("contractors.json")["records"]:
        assert c["cslb_url"].startswith("https://")
        assert c["yelp_url"].startswith("https://www.yelp.com/")
        assert c["fit"] and c["notes"]
        if c["license"]:
            assert c["phone"], c["name"]
            assert c["bond"] and c["workers_comp"], c["name"]


def test_all_in_one_contractors_really_hold_both_classifications():
    for c in load("contractors.json")["records"]:
        if not c["all_in_one"]:
            continue
        joined = " ".join(c["classes"])
        assert "C-36" in joined, c["name"]
        assert "B General Building" in joined, c["name"]


def test_contractor_flag_references_exist():
    flag_ids = {f["id"] for f in load("flags.json")["flags"]}
    for c in load("contractors.json")["records"]:
        for flag in c["flags"]:
            assert flag in flag_ids, f"{c['name']} references unknown flag {flag}"


def test_every_flag_has_a_source_and_an_action():
    for f in load("flags.json")["flags"]:
        assert f["detail"] and f["action"] and f["title"]
        assert f["source_url"] and f["source_label"]
        assert f["severity"] in {"unverified", "caution", "info"}


def test_every_source_has_a_url_and_a_read_status():
    for s in load("sources.json")["sources"]:
        assert s["url"].startswith("https://")
        assert s["read"]
        assert s["supports"]
        assert s["publisher"]


# --------------------------------------------------------------------------- generated pages
def test_pages_exist_and_share_navigation():
    for name in PAGES:
        text = page(name)
        assert "<main id=\"main\"" in text
        assert "assets/site.css" in text
        for href in ["index.html", "summary.html", "flagged.html"]:
            assert f'href="{href}"' in text, f"{name} missing nav link {href}"
        # the active page marks itself
        assert 'aria-current="page"' in text


def test_internal_links_and_anchors_resolve():
    ids_cache = {}
    for name in PAGES:
        text = page(name)
        ids_cache[name] = set(re.findall(r'id="([^"]+)"', text))

    for name in PAGES:
        text = page(name)
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target, _, anchor = href.partition("#")
            target = target or name
            assert (ROOT / target).is_file(), f"{name}: broken internal link {href}"
            if anchor:
                assert anchor in ids_cache.get(target, set()), (
                    f"{name}: missing anchor #{anchor} in {target}"
                )


def test_every_table_row_carries_a_link_or_is_labelled_owner_provided():
    for name in PAGES:
        for row in rows_of(page(name)):
            has_link = 'href="' in row
            labelled = "owner-provided" in row or "unverified" in row.lower()
            assert has_link or labelled, f"{name}: row without source or label: {row[:180]}"


def test_contractor_and_benchmark_rows_link_external_sources():
    for name in ("contractors.html", "estimates.html"):
        text = page(name)
        for row in rows_of(text):
            assert 'href="https://' in row, f"{name}: row missing an external source: {row[:160]}"


def test_estimate_amounts_appear_with_their_provenance():
    text = page("estimates.html")
    assert "$614" in text and "$550" in text and "$135" in text
    # each amount is followed by the owner-provided tag inside the same cell
    assert text.count("owner-provided") >= 3
    assert "no official confirmation exists" in text


def test_no_private_or_permit_strategy_language_is_published():
    banned = [
        r"without a permit",
        r"\bno permit\b",
        r"avoid(?:ing)? (?:a |the )?permit",
        r"permit[- ]free",
        r"unpermitted",
        r"cannot pull",
        r"can't pull",
        r"don't pull",
        r"under the table",
        r"off the books",
        r"confidential",
        r"private reason",
        r"keep (?:this|it) private",
        r"do not mention",
        r"don't mention",
    ]
    for name in PAGES:
        text = page(name).lower()
        for pattern in banned:
            assert not re.search(pattern, text), f"{name}: banned phrasing /{pattern}/"
    # and in the site's own markdown/data that gets published
    for extra in ["data/overflow/flags.json", "data/overflow/project.json"]:
        text = (ROOT / extra).read_text(encoding="utf-8").lower()
        for pattern in banned:
            assert not re.search(pattern, text), f"{extra}: banned phrasing /{pattern}/"


def test_executive_summary_numbers_match_the_data():
    text = page("summary.html")
    amounts = [e["amount"] for e in load("estimates.json")["estimates"]]
    assert f"${amounts[0]:,}" in text and f"${amounts[1]:,}" in text and f"${amounts[2]:,}" in text
    contractor_count = len(load("contractors.json")["records"])
    licensed = sum(1 for c in load("contractors.json")["records"] if c["license"])
    assert f"{licensed} of {contractor_count} candidates" in text
    flag_count = len(load("flags.json")["flags"])
    assert f"{flag_count} items" in text


def test_html_is_well_formed():
    for name in PAGES:
        parser = _Balance()
        parser.feed(page(name))
        assert not parser.errors, f"{name}: {parser.errors[:5]}"
        assert not parser.stack, f"{name}: unclosed tags {parser.stack}"


def test_no_placeholder_or_unfilled_values():
    for name in PAGES:
        text = page(name)
        for bad in ["{", "}", "TODO", "FIXME", "None.", "&amp;lt;", "\\n"]:
            assert bad not in text, f"{name}: placeholder {bad!r} found"


def test_titles_and_meta_descriptions_are_present_and_unique():
    titles = []
    for name in PAGES:
        text = page(name)
        m = re.search(r"<title>(.*?)</title>", text, flags=re.S)
        assert m, name
        titles.append(html_mod.unescape(m.group(1)).strip())
        assert 'name="description" content="' in text or 'name="description"\n' in text, name
    assert len(set(titles)) == len(titles)


def test_build_is_deterministic(tmp_path=None):
    """Re-running the builder must not change the committed pages."""
    before = {name: page(name) for name in PAGES}
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_overflow_site.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    after = {name: page(name) for name in PAGES}
    assert before == after, "build is not deterministic — generated pages changed on rebuild"


# --------------------------------------------------------------------------- carried over from the concurrent session's test file
def test_licence_numbers_link_to_their_own_official_record():
    """Any CSLB number shown as a licence must be paired with that record's link."""
    for name in ("contractors.html", "shortlist.html", "verification.html", "summary.html", "findings.html"):
        text = page(name)
        for num in set(re.findall(r"#(\d{6,8})", text)):
            assert f"LicNum={num}" in text, f"{name}: #{num} stated without its CSLB record link"


def test_no_outdated_licensing_threshold():
    """B&P 7048 was amended by AB 1170 (effective 2026-01-01): the figure is $1,000, not $500."""
    for name in PAGES:
        text = page(name).lower()
        assert "$500 or more" not in text, name
        assert "500 threshold" not in text, name
    assert "$1,000" in page("findings.html")
