#!/usr/bin/env python3
"""Build the canonical bathtub-overflow dashboard from one audited dataset.

Usage:  python3 scripts/build_dashboard.py

The script validates every table row (source ids, dead sources, cell counts),
renders the static site at the repository root, emits a machine-readable
data snapshot, runs the link/row/privacy verification, and re-renders the
Verification page with the final results. It exits non-zero on any failure.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import dashboard_content as C  # noqa: E402
import verify_dashboard as V  # noqa: E402

DATA_DIR = ROOT / "data" / "canonical"


GENERATED_OUTPUTS = {
    "data/canonical/site_data.json",
    "data/canonical/verification_report.json",
    "data/canonical/verification_report.md",
    "data/canonical/repo_inventory.json",
    "data/canonical/repo_inventory.csv",
    "data/canonical/repo_audit.json",
    "data/canonical/repo_audit.md",
    "data/canonical/recheck-2026-11-10.json",
    "data/canonical/reread-2026-11-11.json",
    "COORDINATION.md",
}
INVENTORY_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".venv"}


def refresh_repo_inventory():
    """Hash source/preserved artifacts; exclude generated pages and self-referential reports."""
    import csv
    import hashlib
    from urllib.parse import quote

    rows = []
    generated_pages = set(C.PAGES)
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in INVENTORY_SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in GENERATED_OUTPUTS or rel in generated_pages:
            continue
        data = path.read_bytes()
        current = rel.startswith((
            "scripts/dashboard_content.py", "scripts/build_dashboard.py", "scripts/verify_dashboard.py",
            "assets/dashboard", "tests/test_dashboard", "tests/test_dashboard_integrity.py",
            "tests/test_followup_audit.py", "tests/test_canonical_integrity.py", "scripts/audit_repository.py",
            "data/canonical/evidence-", "data/canonical/providers-", "data/canonical/source_checks.json",
            "data/canonical/decision_analysis.json", "data/canonical/recheck-",
            "scripts/recheck_data.py", "tests/test_recheck.py",
            "scripts/reread_1111.py", "tests/test_reread_1111.py",
        ))
        rows.append({
            "path": rel,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "category": "current-plumbing-source" if current else "preserved-archive-or-unrelated",
            "review": "hashed source/artifact inventory; external factual claims not verified by this hash",
        })
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "repo_inventory.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (DATA_DIR / "repo_inventory.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "bytes", "sha256", "category", "review"], lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    table_rows = []
    # Pages is deployed from main. A historical session branch can be missing
    # files integrated by later sessions, even though they are in this build.
    branch = "main"
    for item in rows:
        url = C.META["repo_url"] + "/blob/" + branch + "/" + quote(item["path"], safe="/")
        table_rows.append({"cells": [
            '<a href="%s" target="_blank" rel="noopener noreferrer"><code>%s</code></a>' % (esc(url), esc(item["path"])),
            str(item["bytes"]),
            '<code class="hash">%s</code>' % item["sha256"],
            esc(item["category"]),
            esc(item["review"]),
        ], "src": ["S98"]})
    C.TABLES["repo_inventory"] = {
        "title": "Line-by-line source/artifact inventory (%d files)" % len(rows),
        "columns": ["Path", "Bytes", "SHA-256", "Category", "Review scope", "Source"],
        "rows": table_rows,
        "caption": "Hashed at build time. Generated dashboard pages/reports, this inventory and the post-deploy coordination log are excluded to avoid self-reference. Hashing verifies file identity, not external factual claims. Unrelated GEMS content is preserved, not plumbing evidence.",
    }
    return rows


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def validate() -> list[str]:
    errors = []
    for sid, src in C.SOURCES.items():
        for key in ("label", "publisher", "url", "tier", "status", "checked", "supports", "note"):
            if key not in src:
                errors.append("source %s missing %s" % (sid, key))
        if not (src["url"].startswith("https://") or src["url"].startswith("http://")
                or src["url"].endswith((".html", ".json", ".csv", ".md"))):
            errors.append("source %s has an unexpected url %r" % (sid, src["url"]))
    for tid, table in C.TABLES.items():
        if tid == "source_ledger":
            continue
        ncol = len(table["columns"])
        if not table["columns"] or table["columns"][-1] != "Source":
            errors.append("table %s must end with a Source column" % tid)
        for i, row in enumerate(table["rows"], 1):
            if len(row["cells"]) != ncol - 1:
                errors.append("table %s row %d has %d cells, expected %d"
                              % (tid, i, len(row["cells"]), ncol - 1))
            if not row.get("src"):
                errors.append("table %s row %d has no source ids" % (tid, i))
            for sid in row["src"]:
                if sid not in C.SOURCES:
                    errors.append("table %s row %d cites unknown source %s" % (tid, i, sid))
                elif C.SOURCES[sid]["status"] == "dead":
                    errors.append("table %s row %d cites dead source %s" % (tid, i, sid))
            joined = " ".join(row["cells"])
            if C.BLANK in joined and C.UNVERIFIED not in joined and "blank" not in joined.lower():
                errors.append("table %s row %d has a blank cell without an UNVERIFIED flag" % (tid, i))
    for page, spec in C.PAGES.items():
        for block in spec["sections"]:
            if block["type"] == "table" and block["ref"] not in C.TABLES:
                errors.append("page %s references unknown table %s" % (page, block["ref"]))
    return errors


def build_source_ledger_rows():
    rows = []
    for sid in sorted(C.SOURCES, key=lambda x: int(x[1:])):
        s = C.SOURCES[sid]
        url_cell = esc(s["url"])
        if s["status"] in ("verified", "blocked-403"):
            url_cell = '<a href="%s" target="_blank" rel="noopener noreferrer" class="src-url">%s</a>' % (
                esc(s["url"]), esc(s["url"]))
        else:
            url_cell = '<code class="dead-url">%s</code>' % esc(s["url"])
        status = {
            "verified": C.pill("verified " + s["checked"], "ok"),
            "blocked-403": C.pill("HTTP 403 — manual review", "warn"),
            "dead": C.pill("DEAD — removed from citations", "bad"),
            "removed": C.pill("removed", "mute"),
        }.get(s["status"], C.pill(s["status"], "mute"))
        # Dead sources are never linked from a row; link the flagged page instead.
        src_ids = [sid] if s["status"] != "dead" else ["S45"]
        rows.append({
            "cells": [
                "<code>%s</code>" % sid,
                "<strong>%s</strong><br><small>%s</small>" % (esc(s["label"]), url_cell),
                "%s<br>%s" % (esc(s["publisher"]), C.pill(esc(s["tier"]), "info")),
                status,
                "%s<br><small>%s</small>" % (esc(s["supports"]), esc(s["note"])),
            ],
            "src": src_ids,
        })
    C.TABLES["source_ledger"]["rows"] = rows


def nav_html(current: str) -> str:
    parts = ['<aside class="sidebar" aria-label="Site navigation">',
             '<a class="side-brand" href="index.html"><span class="mark">TL</span>'
             '<span>Overflow Trip Lever<small>San Francisco repair project</small></span></a>']
    for group in C.NAV:
        parts.append('<div class="nav-group"><div class="nav-group-title">%s</div>' % esc(group["group"]))
        for href, label in group["links"]:
            active = ' aria-current="page" class="active"' if href == current else ""
            parts.append('<a href="%s"%s>%s</a>' % (href, active, esc(label)))
        parts.append('</div>')
    parts.append('<div class="side-foot">Updated %s<br>Session <span class="mono">%s</span></div>'
                 % (C.META["updated"], C.META["session"]))
    parts.append('</aside>')
    return "\n".join(parts)


def source_cell(row) -> str:
    links = []
    for sid in row["src"]:
        s = C.SOURCES[sid]
        if s["status"] == "dead":
            continue
        label = sid
        if s["url"].startswith("http"):
            links.append('<a href="%s" target="_blank" rel="noopener noreferrer" '
                         'title="%s">%s</a>' % (esc(s["url"]), esc(s["label"]), label))
        else:
            links.append('<a href="%s" title="%s">%s</a>' % (esc(s["url"]), esc(s["label"]), label))
    if not links:
        links.append('<a href="flagged.html">flagged</a>')
    return '<span class="src-ids">%s</span>' % " · ".join(links)


def render_table(tid: str, title: str | None = None) -> str:
    t = C.TABLES[tid]
    out = ['<section class="section">',
           '<h2>%s</h2>' % esc(title or t["title"]),
           '<div class="table-wrap" tabindex="0" role="region" aria-label="%s table"><table class="data-table">' % esc(title or t["title"]),
           '<thead><tr>']
    for col in t["columns"]:
        out.append('<th>%s</th>' % col)
    out.append('</tr></thead><tbody>')
    for row in t["rows"]:
        out.append('<tr>')
        for cell in row["cells"]:
            out.append('<td>%s</td>' % cell)
        out.append('<td class="src-col">%s</td>' % source_cell(row))
        out.append('</tr>')
    out.append('</tbody>')
    out.append('<caption>%s</caption>' % t["caption"])
    out.append('</table></div></section>')
    return "\n".join(out)


def render_verification_summary(report: dict | None) -> str:
    if report is None:
        return '<section class="section"><h2>Build &amp; link checks</h2><p>Pending final verification pass.</p></section>'
    checks = report["checks"]
    rows = []
    for c in checks:
        tone = "ok" if c["status"] == "PASS" else "bad"
        rows.append('<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (esc(c["name"]), C.pill(c["status"], tone),
                       esc(c["detail"]), C.slink("S45", "task board")))
    return ('<section class="section"><h2>Build &amp; link checks</h2>'
            '<div class="table-wrap"><table class="data-table"><thead><tr>'
            '<th>Check</th><th>Result</th><th>Detail</th><th>Source</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody><caption>Generated by '
            '<code>scripts/verify_dashboard.py</code> from the built HTML on %s. '
            'Full machine-readable report: <a href="data/canonical/verification_report.json">verification_report.json</a> '
            'and <a href="data/canonical/verification_report.md">verification_report.md</a>.</caption></table></div></section>'
            % esc(report["generated_at"][:10]))


def render_row_audit(report: dict | None) -> str:
    rows = []
    for tid, table in C.TABLES.items():
        for i, row in enumerate(table["rows"], 1):
            srcs = [s for s in row["src"] if C.SOURCES[s]["status"] != "dead"]
            tiers = {C.SOURCES[s]["tier"] for s in srcs}
            statuses = {C.SOURCES[s]["status"] for s in srcs}
            text = re.sub(r"<[^>]+>", " ", " ".join(row["cells"])).lower()
            if tiers & {"official", "manufacturer", "company"} and "verified" in statuses:
                grade, tone, state = "official / company / manufacturer", "ok", "SOURCE PRESENT"
            elif "primary" in tiers:
                grade, tone, state = "project primary record", "info", "SOURCE PRESENT"
            elif "historical" in statuses or "historical" in text:
                grade, tone, state = "historical — not current verification", "warn", "FLAGGED"
            elif tiers & {"publisher", "platform"}:
                grade, tone, state = "publisher / platform — third-party", "warn", "UNVERIFIED" if "unverified" in text else "REVIEW"
            else:
                grade, tone, state = "other", "warn", "REVIEW"
            preview = re.sub(r"<[^>]+>", " ", row["cells"][0])
            preview = html.unescape(preview).strip()[:70] or "(row %d)" % i
            rows.append('<tr><td><code>%s</code></td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                        % (esc(tid), i, esc(preview), C.pill(grade, tone), C.pill(state, tone), source_cell(row)))
    total = len(rows)
    return ('<section class="section"><h2>Line-by-line row audit (%d rows)</h2>'
            '<p class="sub">One row per table row in the combined dataset. “Source present” means a cited source exists in the ledger; '
            'it is not independent proof of every claim. Owner, publisher, platform and historical rows are labeled rather than '
            'called officially verified. Blank verified values are flagged on the Flagged for Review page.</p>'
            '<div class="table-wrap"><table class="data-table"><thead><tr><th>Table</th><th>Row</th>'
            '<th>First cell</th><th>Strongest source grade</th><th>Audit label</th><th>Source</th></tr></thead><tbody>'
            % total) + "".join(rows) + ('</tbody><caption>Row audit generated from '
            '<code>data/canonical/site_data.json</code>. Current ranking sources were read 2026-11-08; historical sources are excluded '
            'from the current ranking. Verification method: <a href="https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" '
            'target="_blank" rel="noopener noreferrer">CSLB Check a License</a> and '
            '<a href="https://www.sf.gov/apply-plumbing-and-mechanical-permit" target="_blank" '
            'rel="noopener noreferrer">sf.gov permit guidance</a>.</caption></table></div></section>')


def render_block(block: dict, report: dict | None) -> str:
    t = block["type"]
    if t == "table":
        return render_table(block["ref"], block.get("title"))
    if t == "cards":
        cards = []
        official_count = sum(1 for s in C.SOURCES.values()
                             if s["tier"] in ("official", "manufacturer") and s["status"] == "verified")
        for c in block["items"]:
            value = str(official_count) if c["v"] == "AUTO_OFFICIAL" else c["v"]
            cards.append('<div class="card stat %s"><div class="k">%s</div><div class="v">%s</div>'
                         '<div class="s">%s</div></div>' % (c.get("tone", ""), esc(c["k"]),
                                                            esc(value), c["s"]))
        return '<div class="grid cols-4">%s</div>' % "".join(cards)
    if t == "quick":
        items = []
        for q in block["items"]:
            items.append('<a href="%s"><div class="t">%s</div><div class="d">%s</div></a>'
                         % (q["href"], esc(q["t"]), q["d"]))
        return ('<section class="section"><h2>%s</h2><div class="quick">%s</div></section>'
                % (esc(block.get("title", "Browse")), "".join(items)))
    if t == "prose":
        return '<section class="section"><h2>%s</h2>%s</section>' % (esc(block["title"]), block["html"])
    if t == "callout":
        icons = {"ok": "✓", "warn": "!", "info": "i", "bad": "×"}
        return '<div class="callout %s"><div class="icon">%s</div><p>%s</p></div>' % (
            block["tone"], icons.get(block["tone"], "i"), block["html"])
    if t == "verification_summary":
        return render_verification_summary(report)
    if t == "row_audit":
        return render_row_audit(report)
    raise ValueError("unknown block type %r" % t)


def render_page(filename: str, report: dict | None) -> str:
    spec = C.PAGES[filename]
    body = "\n".join(render_block(b, report) for b in spec["sections"])
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Bathtub Overflow Trip Lever</title>
<meta name="description" content="Verified research dashboard for the bathtub wastewater overflow trip lever repair project in San Francisco.">
<link rel="stylesheet" href="assets/dashboard.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="layout">
{nav}
<main id="main" class="content">
<header class="page-head">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</header>
{body}
<footer class="site">
  <span>Research dashboard · San Francisco · updated {updated} · session <span class="mono">{session}</span></span>
  <span><a href="index.html">Dashboard</a> · <a href="sources.html">Sources</a> · <a href="flagged.html">Flagged for review</a> · <a href="{repo}">Repository</a></span>
</footer>
</main>
</div>
<script src="assets/dashboard.js" defer></script>
</body>
</html>
""".format(title=esc(spec["title"]), nav=nav_html(filename), eyebrow=spec["eyebrow"],
           h1=spec["h1"], lede=spec["lede"], body=body, updated=C.META["updated"],
           session=C.META["session"], repo=C.META["repo_url"])


def write_pages(report=None):
    for filename in C.PAGES:
        (ROOT / filename).write_text(render_page(filename, report), encoding="utf-8")


def write_data_snapshot():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": C.META,
        "nav": C.NAV,
        "sources": C.SOURCES,
        "tables": C.TABLES,
    }
    (DATA_DIR / "site_data.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    refresh_repo_inventory()
    errors = validate()
    if errors:
        print("CONTENT VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    build_source_ledger_rows()
    write_data_snapshot()
    write_pages(None)
    report1 = V.analyze(ROOT, list(C.PAGES.keys()))
    write_pages(report1)
    # Create the report artifacts early so the Verification page links resolve.
    V.write_report(ROOT, report1)
    report2 = V.analyze(ROOT, list(C.PAGES.keys()))
    write_pages(report2)
    report3 = V.analyze(ROOT, list(C.PAGES.keys()))
    V.write_report(ROOT, report3)
    failed = [c for c in report3["checks"] if c["status"] != "PASS"]
    print("Built %d pages, %d tables, %d rows, %d sources."
          % (len(C.PAGES), len(C.TABLES),
             sum(len(t["rows"]) for t in C.TABLES.values()), len(C.SOURCES)))
    for c in report3["checks"]:
        print("  [%s] %s — %s" % (c["status"], c["name"], c["detail"]))
    if failed:
        print("VERIFICATION FAILED")
        return 1
    print("VERIFICATION PASS — report: data/canonical/verification_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
