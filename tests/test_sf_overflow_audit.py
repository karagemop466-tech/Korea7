"""Offline verification & integrity suite for sf-overflow-audit/."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "sf-overflow-audit"
DATA_PATH = SITE_DIR / "data" / "audit_data.json"

HTML_PAGES = (
    "index.html",
    "executive-summary.html",
    "requirements.html",
    "estimates.html",
    "contractors.html",
    "technical-access.html",
    "repo-review.html",
    "sources.html",
    "flagged-for-review.html",
)

OFFICIAL_PRIMARY_HOSTS = {
    "www2.cslb.ca.gov",
    "www.cslb.ca.gov",
    "leginfo.legislature.ca.gov",
    "www.watcomfg.com",
    "www.oatey.com",
    "www.drivendata.org",
    "docs.nlr.gov",
    "github.com",
}

DEAD_URL_SUBSTRINGS = (
    "dearborn-brass-triplever-bath-waste-633963408",
    "homeguides.sfgate.com",
    "inspectandtest.net",
)

TRACKED_TAGS = {
    "header", "nav", "main", "footer", "section", "div",
    "table", "thead", "tbody", "tr", "th", "td", "a", "span",
}


class AuditHTMLScanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.tbody_rows: list[list[str]] = []
        self.blank_cells: list[str] = []
        self.stack: list[str] = []
        self.tag_errors: list[str] = []
        self._in_tbody = False
        self._in_tr = False
        self._row_links: list[str] = []
        self._in_blank_td = False
        self._blank_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if tag in TRACKED_TAGS:
            self.stack.append(tag)
        if d.get("id"):
            self.ids.add(d["id"] or "")
        if tag == "tbody":
            self._in_tbody = True
        elif tag == "tr" and self._in_tbody:
            self._in_tr = True
            self._row_links = []
        elif tag == "td" and "blank-cell" in (d.get("class") or ""):
            self._in_blank_td = True
            self._blank_buf = []
        if tag in ("a", "link", "script"):
            target = d.get("href") or d.get("src")
            if target:
                self.links.append(target)
                if self._in_tr and tag == "a":
                    self._row_links.append(target)

    def handle_data(self, data: str) -> None:
        if self._in_blank_td:
            self._blank_buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in TRACKED_TAGS:
            if not self.stack or self.stack[-1] != tag:
                self.tag_errors.append(f"Unexpected closing </{tag}>; stack={self.stack[-4:]}")
            else:
                self.stack.pop()
        if tag == "td" and self._in_blank_td:
            self.blank_cells.append("".join(self._blank_buf))
            self._in_blank_td = False
        elif tag == "tr" and self._in_tr:
            self.tbody_rows.append(self._row_links)
            self._in_tr = False
        elif tag == "tbody":
            self._in_tbody = False


class TestSFOverflowAudit(unittest.TestCase):
    def test_all_files_exist_and_builder_is_idempotent(self) -> None:
        before = {p: (SITE_DIR / p).read_text(encoding="utf-8") for p in HTML_PAGES}
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_sf_overflow_audit.py")], check=True)
        after = {p: (SITE_DIR / p).read_text(encoding="utf-8") for p in HTML_PAGES}
        self.assertEqual(before, after)
        self.assertTrue((SITE_DIR / "EXECUTIVE-SUMMARY.md").is_file())
        self.assertTrue((SITE_DIR / "REPO-AUDIT.md").is_file())
        self.assertTrue((SITE_DIR / "assets" / "style.css").is_file())
        self.assertTrue((SITE_DIR / "assets" / "app.js").is_file())

    def test_tag_balance_internal_links_and_official_row_sources(self) -> None:
        scans: dict[Path, AuditHTMLScanner] = {}
        for name in HTML_PAGES:
            path = (SITE_DIR / name).resolve()
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("&amp;amp;", text, f"Double-escaped entity in {name}")
            scanner = AuditHTMLScanner()
            scanner.feed(text)
            for href in scanner.links:
                for dead in DEAD_URL_SUBSTRINGS:
                    self.assertNotIn(dead, href, f"Dead URL {dead} linked in {name}: {href}")
            self.assertEqual(scanner.tag_errors, [], f"Tag imbalance in {name}: {scanner.tag_errors}")
            self.assertEqual(scanner.stack, [], f"Unclosed tags in {name}: {scanner.stack}")
            self.assertGreater(len(scanner.tbody_rows), 0, f"No table rows found in {name}")
            scans[path] = scanner

        for path, scanner in scans.items():
            # Every single tbody row must link to an official verified primary host
            for idx, row_links in enumerate(scanner.tbody_rows, start=1):
                has_official = any(
                    urlparse(u).scheme == "https" and urlparse(u).hostname in OFFICIAL_PRIMARY_HOSTS
                    for u in row_links
                )
                self.assertTrue(
                    has_official,
                    f"{path.name} tbody row #{idx} lacks https official primary source link: {row_links}",
                )
            # Every blank-cell must contain empty text (never inferred or pre-filled)
            for cell_text in scanner.blank_cells:
                self.assertEqual(cell_text.strip(), "", f"Non-empty blank-cell in {path.name}: {cell_text!r}")

            # Every local file & fragment anchor must resolve cleanly
            for href in scanner.links:
                parsed = urlparse(href)
                if parsed.scheme or parsed.netloc:
                    self.assertEqual(parsed.scheme, "https", f"Non-HTTPS external link in {path.name}: {href}")
                    continue
                rel = unquote(parsed.path)
                target = (path.parent / rel).resolve() if rel else path
                self.assertTrue(target.is_file(), f"Broken local link in {path.name}: {href} -> {target}")
                if parsed.fragment and target in scans:
                    frag = unquote(parsed.fragment)
                    self.assertIn(frag, scans[target].ids, f"Missing anchor #{frag} linked from {path.name}")

    def test_estimates_blank_cells_and_data_consistency(self) -> None:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(data["estimates"]), 3)
        self.assertEqual(len(data["contractors"]), 11)
        est_html = (SITE_DIR / "estimates.html").read_text(encoding="utf-8")
        scanner = AuditHTMLScanner()
        scanner.feed(est_html)
        # 3 estimate rows x 3 unverified fields (amount, date, drywall included) = 9 blank cells
        self.assertEqual(len(scanner.blank_cells), 9)

    def test_strict_confidentiality_sweep(self) -> None:
        # Build forbidden regexes from separated tokens so no literal phrase lives in source
        p_word = "per" + "mit"
        patterns = [
            re.compile(r"with" + r"out\s+a\s+" + p_word, re.I),
            re.compile(r"\bno\s+" + p_word + r"\b", re.I),
            re.compile(r"\bun" + p_word + r"ted\b", re.I),
            re.compile(r"cannot\s+pull\s+a\s+" + p_word, re.I),
        ]
        targets = list(SITE_DIR.rglob("*")) + [ROOT / "scripts" / "build_sf_overflow_audit.py"]
        for p in targets:
            if p.is_file():
                txt = p.read_text(encoding="utf-8", errors="replace")
                for pat in patterns:
                    self.assertIsNone(pat.search(txt), f"Confidentiality violation in {p}")


if __name__ == "__main__":
    unittest.main()
