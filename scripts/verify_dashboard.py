#!/usr/bin/env python3
"""Verify the built dashboard: row links, internal/external links, privacy.

Usage:  python3 scripts/verify_dashboard.py

Exits non-zero if any check fails. Writes:
  data/canonical/verification_report.json
  data/canonical/verification_report.md
"""
from __future__ import annotations

import datetime
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import dashboard_content as C  # noqa: E402

ASSET_RE = re.compile(r'(?:<link[^>]+href="([^"]+)"|<script[^>]+src="([^"]+)")')
HREF_RE = re.compile(r'<a\s[^>]*href="([^"]+)"', re.I)
ROW_RE = re.compile(r'<tbody>(.*?)</tbody>', re.S)
TR_RE = re.compile(r'<tr[^>]*>(.*?)</tr>', re.S)
TD_RE = re.compile(r'<td[^>]*>(.*?)</td>', re.S)

# Internal-only hiring constraints must never appear on the public site.
PRIVACY_PATTERNS = [
    r"without\s+a\s+permit",
    r"work\s+without\s+permit",
    r"no\s+permit\s+(?:is\s+)?(?:required|needed|pulled)",
    r"cannot\s+pull\s+a\s+permit",
    r"can(?:not|'?t)\s+pull\s+a\s+permit",
    r"permit\s+for\s+this\s+week",
    r"stay\s+private",
    r"never\s+mentioned",
    r"internal\s+use\s+only",
    r"most\s+contractors\s+and\s+plumbers",
    r"reasons\s+that\s+need\s+to\s+stay\s+private",
    r"private\s+rationale\s+for\s+",
]
PLACEHOLDER_PATTERNS = [r"\bTODO\b", r"\bTBD\b", r"\bPLACEHOLDER\b", r"example\.com", r"lorem ipsum"]

EXTENSIONS = {".html", ".md", ".json", ".css", ".js"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "vendor", "gems", "evidence", "registry", "data"}


def is_external(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def norm_url(url: str) -> str:
    """Undo HTML attribute escaping without interpreting named entities.

    html.unescape() would turn '&sectionNum' into the section sign; attribute
    escaping only ever needs '&amp;' -> '&' here.
    """
    return url.replace("&amp;", "&")


def resolve_internal(page: Path, url: str) -> Path | None:
    clean = unquote(url.split("#", 1)[0].split("?", 1)[0])
    if not clean:
        return page
    return (page.parent / clean).resolve()


def check(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def analyze(root: Path, pages: list[str] | None = None) -> dict:
    if pages is None:
        pages = list(C.PAGES.keys())
    checks = []
    broken_internal = []
    broken_anchors = []
    unknown_external = []
    missing_row_links = []
    unflagged_blanks = []
    external_links = set()
    internal_count = 0
    row_count = 0
    nav_issues = []
    ids_by_page = {}

    # First pass: collect ids for anchor checks.
    for name in pages:
        p = root / name
        if not p.exists():
            nav_issues.append("missing page %s" % name)
            continue
        text = p.read_text(encoding="utf-8")
        ids_by_page[name] = set(re.findall(r'\bid="([^"]+)"', text))
        for m in ASSET_RE.finditer(text):
            asset = m.group(1) or m.group(2)
            if is_external(asset):
                external_links.add(asset)
                continue
            internal_count += 1
            target = resolve_internal(p, asset)
            if target is None or not target.exists():
                broken_internal.append("%s -> %s" % (name, asset))

    source_urls = {s["url"] for s in C.SOURCES.values()}
    dead_urls = {s["url"] for s in C.SOURCES.values() if s["status"] == "dead"}

    for name in pages:
        p = root / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        # Navigation consistency.
        current = re.findall(r'aria-current="page"', text)
        if len(current) != 1:
            nav_issues.append("%s has %d aria-current markers" % (name, len(current)))
        # All links.
        for raw_url in HREF_RE.findall(text):
            url = norm_url(raw_url)
            if is_external(url):
                external_links.add(url)
                if url not in source_urls and not url.startswith(C.META["repo_url"]) \
                        and not url.startswith(C.META["pages_url"]):
                    unknown_external.append("%s -> %s" % (name, url))
                if url in dead_urls:
                    unknown_external.append("%s -> DEAD %s" % (name, url))
                continue
            if url.startswith("mailto:") or url.startswith("tel:") or url.startswith("#"):
                if url.startswith("#") and len(url) > 1:
                    if url[1:] not in ids_by_page.get(name, set()):
                        broken_anchors.append("%s -> %s" % (name, url))
                continue
            internal_count += 1
            frag = url.split("#", 1)
            target_page = frag[0] or name
            target = resolve_internal(p, url)
            if target is None or not target.exists():
                broken_internal.append("%s -> %s" % (name, url))
            elif len(frag) > 1 and frag[1]:
                rel = (p.parent / target_page).resolve()
                key = rel.relative_to(root).as_posix() if rel.is_relative_to(root) else rel.as_posix()
                if key in ids_by_page and frag[1] not in ids_by_page[key]:
                    broken_anchors.append("%s -> %s" % (name, url))
        # Table rows.
        for body in ROW_RE.findall(text):
            for idx, tr in enumerate(TR_RE.findall(body), 1):
                row_count += 1
                cells = TD_RE.findall(tr)
                src_cell = cells[-1] if cells else ""
                if not re.search(r'<a\s[^>]*href=', tr):
                    missing_row_links.append("%s tbody row %d" % (name, idx))
                elif not re.search(r'<a\s[^>]*href=', src_cell):
                    missing_row_links.append("%s tbody row %d (Source column)" % (name, idx))
                if 'class="blank"' in tr and ("UNVERIFIED" not in tr and "blank — unverified" not in tr):
                    unflagged_blanks.append("%s tbody row %d" % (name, idx))

    checks.append(check("Build output complete", len(nav_issues) == 0 or all("missing page" not in x for x in nav_issues),
                        "%d pages generated" % len(pages)))
    checks.append(check("Every table row has a source link", not missing_row_links,
                        "%d tbody rows checked, %d missing links" % (row_count, len(missing_row_links))))
    checks.append(check("Blank values are flagged UNVERIFIED", not unflagged_blanks,
                        "%d unflagged blank rows" % len(unflagged_blanks)))
    checks.append(check("Internal links resolve", not broken_internal,
                        "%d internal links checked, %d broken%s" % (
                            internal_count, len(broken_internal),
                            (" — " + "; ".join(broken_internal[:5])) if broken_internal else "")))
    checks.append(check("Anchor targets resolve", not broken_anchors,
                        "%d broken anchors" % len(broken_anchors)))
    checks.append(check("External links are in the source ledger", not unknown_external,
                        "%d unique external links, %d unknown/dead%s" % (
                            len(external_links), len(unknown_external),
                            (" — " + "; ".join(unknown_external[:5])) if unknown_external else "")))
    checks.append(check("Navigation consistent", not nav_issues,
                        "%d nav issues%s" % (len(nav_issues), (" — " + "; ".join(nav_issues[:5])) if nav_issues else "")))

    # Privacy sweep over published text assets.
    privacy_hits = []
    scanned = 0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        if rel.as_posix().startswith("data/canonical/verification_report"):
            continue
        scanned += 1
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat in PRIVACY_PATTERNS:
            for m in re.finditer(pat, content, re.I):
                snippet = content[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                privacy_hits.append("%s: %s" % (rel.as_posix(), html.escape(snippet)))
    checks.append(check("Privacy sweep (internal-only wording)", not privacy_hits,
                        "%d files scanned, %d matches" % (scanned, len(privacy_hits))))

    placeholder_hits = []
    for name in pages:
        p = root / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat, text, re.I):
                placeholder_hits.append("%s: %s" % (name, pat))
    checks.append(check("No unfilled template markers", not placeholder_hits,
                        "%d template-marker matches" % len(placeholder_hits)))

    # Dead sources are documented but never linked.
    dead_linked = []
    for name in pages:
        p = root / name
        if not p.exists():
            continue
        for raw_url in HREF_RE.findall(p.read_text(encoding="utf-8")):
            url = norm_url(raw_url)
            if url in dead_urls:
                dead_linked.append("%s -> %s" % (name, url))
    checks.append(check("Dead sources not linked", not dead_linked,
                        "%d dead-source links" % len(dead_linked)))

    verified_sources = sum(1 for s in C.SOURCES.values() if s["status"] == "verified")
    official_sources = sum(1 for s in C.SOURCES.values()
                           if s["tier"] in ("official", "manufacturer") and s["status"] == "verified")
    checks.append(check("Source ledger records prior direct reads", official_sources >= 10,
                        "%d official/manufacturer sources marked verified; %d sources marked verified overall (metadata only; no network check)"
                        % (official_sources, verified_sources)))

    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "pages": pages,
        "counts": {
            "pages": len(pages),
            "tables": len(C.TABLES),
            "rows": sum(len(t["rows"]) for t in C.TABLES.values()),
            "source_ledger_entries": len(C.SOURCES),
            "verified_sources": verified_sources,
            "official_or_manufacturer_verified": official_sources,
            "generated_tbody_rows": row_count,
            "internal_links_checked": internal_count,
            "unique_external_links": len(external_links),
            "published_text_files_scanned": scanned,
        },
        "checks": checks,
        "broken_internal": broken_internal,
        "broken_anchors": broken_anchors,
        "unknown_external": unknown_external,
        "missing_row_links": missing_row_links,
        "unflagged_blanks": unflagged_blanks,
        "privacy_matches": privacy_hits,
        "nav_issues": nav_issues,
        "dead_sources": sorted(dead_urls),
        "external_links": sorted(external_links),
    }


def write_report(root: Path, report: dict) -> None:
    out = root / "data" / "canonical"
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Dashboard verification report",
        "",
        "Generated: %s" % report["generated_at"],
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for c in report["checks"]:
        lines.append("| %s | %s | %s |" % (c["name"], c["status"], c["detail"].replace("|", "\\|")))
    lines += ["", "## Counts", ""]
    for k, v in report["counts"].items():
        lines.append("- %s: %s" % (k, v))
    lines += ["", "## Notes", "",
              "- Every table row is emitted with a Source column from `data/canonical/site_data.json`.",
              "- Unverified values are blank in verified cells and published on `flagged.html`.",
              "- Official values were read directly from the issuing site on 2026-11-07; CSLB records printed",
              "  \"Data current as of 11/7/2026\".",
              "- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.",
              "- Dead sources: %s (documented, never linked from a row)." % ", ".join(report["dead_sources"]),
              ""]
    (out / "verification_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    report = analyze(ROOT)
    write_report(ROOT, report)
    for c in report["checks"]:
        print("[%s] %s — %s" % (c["status"], c["name"], c["detail"]))
    failed = [c for c in report["checks"] if c["status"] != "PASS"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
