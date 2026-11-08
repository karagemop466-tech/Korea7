#!/usr/bin/env python3
"""Line-by-line repository inventory and non-destructive project audit.

This script does not revalidate legacy GEMS science. It inventories every tracked
file, hashes text/binary bytes, parses JSON/Python where applicable, scans HTML
links, and publishes a bounded irregularity register for the plumbing dashboard.

Usage: python3 scripts/audit_project.py
Outputs: data/review-2026-11-08/repo_inventory.json, repo_findings.json, REPO-AUDIT.md
"""
from __future__ import annotations

import ast
import hashlib
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "review-2026-11-08"
REPO_URL = "https://github.com/karagemop466-tech/Korea7"
CANONICAL_PAGES = {
    "index.html", "summary.html", "requirements.html", "estimates.html",
    "contractors.html", "technical.html", "permits.html", "findings.html",
    "sources.html", "verification.html", "repo-review.html", "brief.html",
    "flagged.html",
}
PRIVACY_PATTERNS = [
    r"reasons\s+that\s+need\s+to\s+stay\s+private",
    r"never\s+mentioned\s+on\s+the\s+site",
    r"permit\s+for\s+this\s+week",
    r"cannot\s+pull\s+a\s+permit",
    r"can't\s+pull\s+a\s+permit",
    r"most\s+contractors\s+and\s+plumbers\s+are\s+ok",
]
# Generic compliance-test fixtures are not owner context. They are reported as
# informational matches, not as publication of private rationale.
TEST_FIXTURE_PATHS = {"tests/test_bath_site.py", "tests/test_overflow_site.py", "scripts/verify_dashboard.py"}
HREF_RE = re.compile(r'(?:href|src)="([^"]+)"', re.I)


def tracked_files() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return sorted(x for x in raw.decode("utf-8").split("\0") if x)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def category(rel: str) -> str:
    if rel in CANONICAL_PAGES or rel.startswith("assets/dashboard.") or rel in {
        "scripts/build_dashboard.py", "scripts/dashboard_content.py",
        "scripts/verify_dashboard.py", "tests/test_dashboard.py",
    } or rel.startswith("data/canonical/"):
        return "canonical-dashboard"
    if rel.startswith("data/review-2026-11-08/") or rel in {"scripts/audit_project.py", "tests/test_project_audit.py"}:
        return "current-audit"
    if rel == "COORDINATION.md":
        return "coordination"
    if rel in {"README.md", "EXECUTIVE-SUMMARY.md"}:
        return "shared-summary"
    if rel.startswith(("bathtub-overflow/", "docs/bath/", "sf-overflow-audit/", "trip-lever/")) or rel.startswith("docs/overflow-") or rel in {
        "docs/plumbing-index.html", "shortlist.html", "verification-log.html",
    }:
        return "archived-overflow"
    return "legacy-or-other"


def blob_url(rel: str, line: int | None = None) -> str:
    url = f"{REPO_URL}/blob/main/{rel}"
    return url + (f"#L{line}" if line else "")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    files = tracked_files()
    inventory = []
    json_errors = []
    python_errors = []
    privacy_hits = []
    fixture_hits = []
    broken_links = []
    directory_links = []
    link_count = 0
    text_lines = 0

    for rel in files:
        path = ROOT / rel
        if not path.is_file():
            continue
        data = path.read_bytes()
        entry = {
            "path": rel,
            "category": category(rel),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "text": False,
            "lines": 0,
        }
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            inventory.append(entry)
            continue
        entry["text"] = True
        lines = text.splitlines()
        entry["lines"] = len(lines)
        text_lines += len(lines)
        inventory.append(entry)

        if rel.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_errors.append({"path": rel, "line": exc.lineno, "error": str(exc)})
        if rel.endswith(".py"):
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                python_errors.append({"path": rel, "line": exc.lineno, "error": str(exc)})

        for i, line in enumerate(lines, 1):
            for pat in PRIVACY_PATTERNS:
                if re.search(pat, line, re.I):
                    hit = {"path": rel, "line": i, "pattern": pat, "excerpt": line.strip()[:180]}
                    if rel in TEST_FIXTURE_PATHS:
                        fixture_hits.append(hit)
                    else:
                        privacy_hits.append(hit)

        if rel.endswith(".html"):
            for raw in HREF_RE.findall(text):
                url = html.unescape(raw)
                parsed = urlparse(url)
                if parsed.scheme or parsed.netloc or url.startswith(("#", "data:")):
                    continue
                link_count += 1
                clean = unquote(url.split("#", 1)[0].split("?", 1)[0])
                if not clean:
                    continue
                target = (path.parent / clean).resolve()
                if not target.exists():
                    broken_links.append({"page": rel, "url": url})
                elif target.is_dir() and not (target / "index.html").exists():
                    directory_links.append({"page": rel, "url": url, "target": target.relative_to(ROOT).as_posix()})

    research = json.loads((OUT / "research.json").read_text(encoding="utf-8"))
    repo_flags = [f for f in research["flags"] if f["id"] in {"F18", "F19", "F20", "F21", "F22"}]
    findings = {
        "generated_at": now,
        "tracked_files": len(files),
        "text_files": sum(1 for e in inventory if e["text"]),
        "text_lines": text_lines,
        "html_links_checked": link_count,
        "json_errors": json_errors,
        "python_errors": python_errors,
        "privacy_hits": privacy_hits,
        "compliance_test_fixture_matches": fixture_hits,
        "broken_file_links": broken_links,
        "directory_links_without_index": directory_links,
        "repo_flags": repo_flags,
        "scope_note": "Legacy GEMS scientific claims are inventoried and preserved, not revalidated by this plumbing audit.",
    }
    (OUT / "repo_inventory.json").write_text(json.dumps({"generated_at": now, "files": inventory}, indent=2) + "\n", encoding="utf-8")
    (OUT / "repo_findings.json").write_text(json.dumps(findings, indent=2) + "\n", encoding="utf-8")

    cat_counts: dict[str, int] = {}
    for e in inventory:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1

    md = [
        "# Repository audit — 2026-11-08",
        "",
        f"Generated: {now}",
        "",
        "## Method and scope",
        "",
        "- Every tracked file was inventoried line by line where text-decodable; SHA-256 was computed from saved bytes.",
        "- JSON files were parsed and Python files were AST-parsed. HTML href/src targets were checked against the filesystem; directory targets were checked for index.html.",
        "- Official plumbing claims were re-read from the issuing government/company/manufacturer pages recorded in [research.json](research.json). Legacy GEMS science was preserved, not revalidated.",
        "- This is a static integrity and provenance audit, not a claim that every historical scientific or contractor statement has been independently reverified.",
        "",
        "## Inventory",
        "",
        "| Category | Files | Source |",
        "|---|---:|---|",
    ]
    for cat, count in sorted(cat_counts.items()):
        md.append(f"| {cat} | {count} | [repository]({REPO_URL}) |")
    md += [
        "",
        f"Total tracked files: **{len(files)}**. Text files: **{findings['text_files']}**. Text lines scanned: **{text_lines}**. HTML links checked: **{link_count}**.",
        "",
        "## Integrity results",
        "",
        "| Check | Result | Source |",
        "|---|---|---|",
        f"| JSON parse errors | {len(json_errors)} | [repo_findings.json](repo_findings.json) |",
        f"| Python syntax errors | {len(python_errors)} | [repo_findings.json](repo_findings.json) |",
        f"| Broken HTML file links | {len(broken_links)} | [repo_findings.json](repo_findings.json) |",
        f"| Directory links without index.html | {len(directory_links)} | [repo_findings.json](repo_findings.json) |",
        f"| Owner-context privacy matches | {len(privacy_hits)} | [repo_findings.json](repo_findings.json) |",
        f"| Generic compliance-test fixture matches | {len(fixture_hits)} | [repo_findings.json](repo_findings.json) |",
        "",
        "## Irregularities carried to the public Flagged for Review page",
        "",
        "| ID | Item | Detail | Source |",
        "|---|---|---|---|",
    ]
    for f in repo_flags:
        src = research["sources"][f["src"][0]]["url"]
        if not src.startswith("http"):
            src = REPO_URL + "/blob/main/" + src
        md.append(f"| {f['id']} | {f['item']} | {f['detail']} | [source]({src}) |")
    if directory_links:
        md += ["", "## Directory-link findings", "", "| Page | Link | Target | Source |", "|---|---|---|---|"]
        for d in directory_links:
            md.append(f"| {d['page']} | `{d['url']}` | {d['target']} | [page]({blob_url(d['page'])}) |")
    if broken_links:
        md += ["", "## Broken file links", "", "| Page | Link | Source |", "|---|---|---|"]
        for d in broken_links:
            md.append(f"| {d['page']} | `{d['url']}` | [page]({blob_url(d['page'])}) |")
    md += [
        "",
        "## Limitations",
        "",
        "- Archived overflow page sets and legacy GEMS artifacts were not edited; they remain available for history and are flagged where they conflict with the current canonical policy.",
        "- File hashes prove byte integrity, not factual correctness. External source verification is recorded separately in research.json and the canonical source ledger.",
        "- A generic compliance-test fixture may contain permit-related wording used only to test publication rules; it is not owner context.",
        "",
    ]
    (OUT / "REPO-AUDIT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"Audited {len(files)} tracked files; {text_lines} text lines; {link_count} HTML links.")
    print(f"JSON errors: {len(json_errors)}; Python errors: {len(python_errors)}; broken file links: {len(broken_links)}; directory-index warnings: {len(directory_links)}; privacy hits: {len(privacy_hits)}.")
    hard_fail = json_errors or python_errors or broken_links or privacy_hits
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
