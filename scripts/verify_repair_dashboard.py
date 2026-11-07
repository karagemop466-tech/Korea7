#!/usr/bin/env python3
"""Offline verification for the canonical repair dashboard artifact.

Checks structure, internal links/anchors, row-level source links, blank
unconfirmed values, privacy wording, data consistency, and deterministic build.
External primary-source reading is recorded in the source register; this script
does not make network calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO = Path(__file__).resolve().parents[1]
REQUIRED_PAGES = [
    "index.html", "summary.html", "requirements.html", "estimates.html",
    "contractors.html", "reviews.html", "findings.html", "access-plan.html",
    "compliance.html", "sources.html", "flagged.html", "verification.html", "archive.html",
]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
FORBIDDEN_PUBLIC = [
    "requester-only", "requester only", "private reasons", "without a permit this week",
    "no permit this week",
]
OWNER_AMOUNTS = ["$614", "$550", "$135", "614", "550", "135"]


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.stack = []
        self.errors = []
        self.rows = []
        self._row = None
        self._in_tbody = False
        self._cell = None
        self._cells = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
            if self._row is not None:
                self._row["links"].append(attrs["href"])
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._row = {"links": [], "cells": []}
            self._cells = []
        if tag in {"td", "th"} and self._row is not None:
            self._cell = {"text": [], "html": []}
        if self._cell is not None:
            self._cell["html"].append(self.get_starttag_text() or "")

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        else:
            # Tolerate optional HTML closing tags only if the tag exists in stack.
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
                if self.stack:
                    self.stack.pop()
            else:
                self.errors.append(f"mismatched closing </{tag}>")
        if self._cell is not None and tag in {"td", "th"}:
            self._cells.append({"text": "".join(self._cell["text"]).strip(), "html": "".join(self._cell["html"])})
            self._cell = None
        if tag == "tr" and self._row is not None:
            self._row["cells"] = self._cells
            self.rows.append(self._row)
            self._row = None
            self._cells = []
        if tag == "tbody":
            self._in_tbody = False
        if self._cell is not None:
            self._cell["html"].append(f"</{tag}>")

    def handle_data(self, data):
        self.text.append(data)
        if self._cell is not None:
            self._cell["text"].append(data)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_external(href: str) -> bool:
    return bool(urlparse(href).scheme) or href.startswith("//")


def verify(site: Path, report_path: Path | None = None, check_determinism: bool = True) -> dict:
    checks = []
    failures = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            failures.append(f"{name}: {detail}")

    missing = [p for p in REQUIRED_PAGES if not (site / p).is_file()]
    check("required_pages", not missing, f"missing={missing}")
    check("nojekyll", (site / ".nojekyll").exists())
    check("css", (site / "assets" / "site.css").is_file())

    parsers = {}
    html_files = sorted(site.rglob("*.html"))
    for path in html_files:
        parser = AuditParser()
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        parsers[path.relative_to(site).as_posix()] = parser
        if parser.stack:
            check(f"html_balance:{path.relative_to(site)}", False, f"unclosed={parser.stack}")
        if parser.errors:
            check(f"html_structure:{path.relative_to(site)}", False, "; ".join(parser.errors[:5]))

    # Internal links and anchors.
    broken = []
    external = set()
    for rel, parser in parsers.items():
        page = site / rel
        for href in parser.links:
            if is_external(href):
                external.add(href)
                parsed = urlparse(href)
                if parsed.scheme not in {"http", "https"}:
                    broken.append(f"{rel}: non-http external scheme {href}")
                if parsed.hostname in {"localhost", "127.0.0.1", "0.0.0.0"}:
                    broken.append(f"{rel}: localhost link {href}")
                continue
            target, _, frag = href.partition("#")
            target = unquote(target)
            if target:
                dest = (page.parent / target).resolve()
                if not dest.exists():
                    broken.append(f"{rel}: missing target {href}")
                    continue
            else:
                dest = page
            if frag:
                dest_rel = dest.relative_to(site.resolve()).as_posix() if dest.is_relative_to(site.resolve()) else None
                if dest_rel in parsers and unquote(frag) not in parsers[dest_rel].ids:
                    broken.append(f"{rel}: missing anchor {href}")
    check("internal_links_and_anchors", not broken, "; ".join(broken[:10]))

    # Every data table row must contain a source/context link.
    unsourced = []
    row_count = 0
    for rel, parser in parsers.items():
        if rel.startswith(("docs/", "bathtub-overflow/")):
            continue  # compatibility redirects
        for i, row in enumerate(parser.rows, 1):
            row_count += 1
            if not row["links"]:
                unsourced.append(f"{rel} row {i}")
    check("every_table_row_has_source_link", not unsourced, f"rows={row_count}; unsourced={unsourced[:10]}")

    # Data consistency and blank-value policy.
    data_dir = site / "data" / "repair"
    providers = json.loads((data_dir / "providers.json").read_text())["providers"]
    estimates = json.loads((data_dir / "estimates.json").read_text())["estimates"]
    flags = json.loads((data_dir / "flags.json").read_text())["flags"]
    flag_ids = {f["id"] for f in flags}
    verified = [p for p in providers if p.get("license")]
    discovery = [p for p in providers if not p.get("license")]
    check("provider_counts", len(providers) == 21 and len(verified) == 14 and len(discovery) == 7,
          f"total={len(providers)} verified={len(verified)} discovery={len(discovery)}")
    check("verified_have_cslb_links", all(p.get("cslb_url", "").startswith("https://www2.cslb.ca.gov/") for p in verified))
    check("discovery_licenses_blank", all(p.get("license") is None and p.get("status") is None for p in discovery))
    check("estimate_amounts_blank", all(q["amount_usd"] is None and q["official_amount_source"] is None for q in estimates))
    check("ratings_blank", all(p.get("rating") is None and p.get("review_count") is None for p in providers))
    referenced_flags = {fid for p in providers for fid in p.get("flags", [])}
    check("provider_flags_resolve", referenced_flags <= flag_ids, f"missing={sorted(referenced_flags - flag_ids)}")

    all_text = "\n".join("".join(p.text) for p in parsers.values())
    leaked_amounts = [x for x in OWNER_AMOUNTS if re.search(r"(?<!\d)" + re.escape(x) + r"(?!\d)", all_text)]
    # Allow license numbers and dates; only flag currency-formatted owner amounts.
    currency_leaks = [x for x in leaked_amounts if x.startswith("$")]
    check("owner_amounts_not_published", not currency_leaks, f"leaks={currency_leaks}")
    privacy_hits = [phrase for phrase in FORBIDDEN_PUBLIC if phrase.lower() in all_text.lower()]
    check("privacy_wording", not privacy_hits, f"hits={privacy_hits}")
    check("no_contact_claim", "No provider was contacted" in all_text or "no provider was contacted" in all_text.lower())

    # Blank cells in key tables.
    est_parser = parsers.get("estimates.html")
    blank_amount_cells = 0
    if est_parser:
        for row in est_parser.rows:
            if len(row["cells"]) >= 4 and 'class="blank"' in row["cells"][3]["html"]:
                blank_amount_cells += 1
    check("estimate_amount_cells_blank", blank_amount_cells == len(estimates), f"blank={blank_amount_cells}/{len(estimates)}")

    # Source register coverage.
    sources = json.loads((data_dir / "sources.json").read_text())["sources"]
    source_urls = {s["url"] for s in sources}
    check("source_register_nonempty", len(sources) >= 40, f"sources={len(sources)}")
    check("all_cslb_records_in_sources", all(p["cslb_url"] in source_urls for p in verified))

    if check_determinism:
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a"
            b = Path(td) / "b"
            for out in (a, b):
                subprocess.run([sys.executable, str(REPO / "scripts" / "build_repair_dashboard.py"), "--output", str(out)], check=True, capture_output=True)
            files_a = {p.relative_to(a).as_posix(): sha256(p) for p in sorted(a.rglob("*")) if p.is_file()}
            files_b = {p.relative_to(b).as_posix(): sha256(p) for p in sorted(b.rglob("*")) if p.is_file()}
            check("deterministic_build", files_a == files_b, "build outputs differ" if files_a != files_b else f"files={len(files_a)}")

    report = {
        "status": "passed" if not failures else "failed",
        "site": str(site),
        "pages": len(REQUIRED_PAGES),
        "html_files": len(html_files),
        "data_rows_checked": row_count,
        "providers": {"total": len(providers), "verified_licenses": len(verified), "discovery_only": len(discovery)},
        "external_links_unique": len(external),
        "sources_registered": len(sources),
        "checks": checks,
        "failures": failures,
        "page_sha256": {p: sha256(site / p) for p in REQUIRED_PAGES if (site / p).exists()},
        "note": "Offline artifact verification. External primary-source reading is recorded in data/repair/sources.json; Yelp direct fetches were restricted and no current Yelp numeric values are asserted.",
    }
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", type=Path, default=REPO)
    ap.add_argument("--report", type=Path, default=None)
    ap.add_argument("--no-determinism", action="store_true")
    args = ap.parse_args()
    report = verify(args.site.resolve(), args.report.resolve() if args.report else None, not args.no_determinism)
    print(json.dumps({"status": report["status"], "failures": report["failures"], "checks": len(report["checks"]), "rows": report["data_rows_checked"]}, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
