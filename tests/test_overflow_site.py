"""Static checks for the bathtub overflow trip lever site (session 6a266fca).

These tests enforce the project's publication rules on the pages that serve the
GitHub Pages site:
  * every internal link and internal anchor resolves;
  * the dashboard, shortlist and verification pages exist and are reachable;
  * no page asserts the outdated "$500" contractor-licensing threshold;
  * no page publishes a permit-strategy instruction (privacy rule);
  * every contractor table row that states a CSLB licence number links to the
    official CSLB record for that number.
"""
from __future__ import annotations

import html
import os
import re

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages that make up the published site (root dashboard + parallel research sets).
SITE_PAGES = [
    "index.html", "summary.html", "shortlist.html", "estimates.html",
    "contractors.html", "findings.html", "verification.html", "sources.html",
    "flagged.html",
]


def _pages():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(out)


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def test_core_pages_exist():
    for page in SITE_PAGES:
        assert os.path.exists(os.path.join(ROOT, page)), page


def test_internal_links_resolve():
    broken = []
    for page in _pages():
        body = _read(page)
        for match in re.finditer(r'(?:href|src)="([^"]+)"', body):
            url = html.unescape(match.group(1))
            if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            path = url.split("#")[0].split("?")[0]
            if not path:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(page), path))
            if not os.path.exists(os.path.join(ROOT, target)):
                broken.append((page, url))
    assert not broken, broken


def test_internal_anchors_resolve():
    ids = {}
    for page in _pages():
        ids[page] = set(re.findall(r'id="([^"]+)"', _read(page)))
    missing = []
    for page in _pages():
        for match in re.finditer(r'href="([^"#]*#[^"]+)"', _read(page)):
            url = html.unescape(match.group(1))
            if url.startswith("http"):
                continue
            path, _, frag = url.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(page), path)) if path else page
            if target in ids and frag and frag not in ids[target]:
                missing.append((page, url))
    assert not missing, missing


def test_no_outdated_licensing_threshold():
    """B&P 7048 was amended by AB 1170 (eff. 2026-01-01): under $1,000 AND no building permit.

    Mentions that explicitly label the $500 figure as outdated are allowed; asserting it as
    the current rule is not.
    """
    allowed = re.compile(r"out of date|outdated|older|superseded|still quoted|widely cited|replaced with|used to", re.I)
    offenders = []
    for page in _pages():
        text = _read(page)
        for match in re.finditer(r"\$\s?500[^.<]{0,80}", text, re.I):
            window = text[max(0, match.start() - 220): match.end() + 220]
            if allowed.search(window):
                continue
            if re.search(r"or more|threshold|licensing requirement", window, re.I):
                offenders.append((page, match.group(0)[:80]))
    assert not offenders, offenders


def test_no_permit_strategy_instructions():
    """Privacy rule: no instruction to obtain or avoid a permit may be published."""
    banned = [
        r"without (?:a |the )?permit",
        r"no permit (?:is )?(?:needed|required)",
        r"skip (?:the )?permit",
        r"avoid (?:the )?permit",
        r"do not (?:pull|get) (?:a |the )?permit",
    ]
    offenders = []
    for page in _pages():
        text = _read(page)
        for pattern in banned:
            if re.search(pattern, text, re.I):
                offenders.append((page, pattern))
    assert not offenders, offenders


@pytest.mark.parametrize("page", ["contractors.html", "shortlist.html", "summary.html", "findings.html"])
def test_licence_numbers_link_to_official_record(page):
    """Any 6-7 digit CSLB number shown as a licence must link to that CSLB record."""
    text = _read(page)
    claims = set(re.findall(r"#(\d{6,8})", text))
    for num in claims:
        assert (
            f"LicNum={num}" in text
        ), f"{page}: license #{num} is stated without a CSLB LicenseDetail link"
