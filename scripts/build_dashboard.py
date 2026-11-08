#!/usr/bin/env python3
"""Render the canonical dashboard and a single structured data snapshot."""
from __future__ import annotations
import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dashboard_content as C
import verify_dashboard as V


def build_source_ledger_rows():
    """Compatibility API for existing regression tests; ledger is already structured."""
    return C.TABLES["source_ledger"]["rows"]


def validate():
    return V.validate_content(C)


def table_html(ref, title=None):
    t = C.TABLES[ref]
    heading = title or t["title"]
    out = ['<section class="panel" id="%s"><h2>%s</h2><div class="table-wrap" tabindex="0" role="region" aria-label="%s"><table class="data-table">' % (ref, C.esc(heading), C.esc(heading))]
    out.append("<thead><tr>" + "".join("<th scope='col'>%s</th>" % C.esc(c) for c in t["columns"]) + "</tr></thead><tbody>")
    for i,r in enumerate(t["rows"], 1):
        out.append("<tr id='%s-%d' data-row-id='%s-%d' data-sources='%s'>" % (ref,i,ref,i,html.escape(",".join(r["src"]),quote=True)))
        for cell in r["cells"]:
            out.append("<td>%s</td>" % cell)
        out.append("<td class='sources'>" + C.source_links(r["src"]) + "</td></tr>")
    out.append("</tbody></table></div><p class='caption'>%s</p></section>" % C.esc(t["caption"]))
    return "\n".join(out)


def render_section(section, page):
    typ = section["type"]
    if typ == "table":
        return table_html(section["ref"], section.get("title"))
    if typ == "prose":
        return "<section class='panel prose'><h2>%s</h2>%s</section>" % (C.esc(section["title"]),section["html"])
    if typ == "callout":
        return "<aside class='callout %s'>%s</aside>" % (section.get("tone","info"),section["html"])
    if typ == "cards":
        return "<div class='cards'>" + "".join("<div class='card %s'><div class='k'>%s</div><div class='v'>%s</div><div class='s'>%s</div></div>" % (i.get("tone","info"),C.esc(i["k"]),C.esc(i["v"]),C.esc(i["s"])) for i in section["items"]) + "</div>"
    if typ == "quick":
        return "<section class='panel'><h2>%s</h2><div class='quick'>" % C.esc(section["title"]) + "".join("<a class='tile' href='%s'><h3>%s</h3><p>%s</p></a>" % (C.esc(i["href"]),C.esc(i["t"]),C.esc(i["d"])) for i in section["items"]) + "</div></section>"
    if typ == "verification_summary":
        report = V.verify(ROOT, C)
        rows = []
        for check in report["checks"]:
            status = check["status"]
            rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (C.esc(check["name"]),C.pill(status,"ok" if status == "PASS" else "bad"),C.esc(check["detail"]),(C.slink(check["source"]) if check.get("source") else C.slink("S86"))))
        return "<section class='panel'><h2>Build checks</h2><div class='table-wrap'><table class='data-table'><thead><tr><th>Check</th><th>Result</th><th>Detail</th><th>Source</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div><p class='caption'>%s source IDs · %s tables · %s rows · %s canonical pages · %s unresolved internal links. These are offline structural/data checks, not live network verification.</p></section>" % (len(C.SOURCES),len(C.TABLES),sum(len(t['rows']) for t in C.TABLES.values()),len(C.PAGES),len(report["broken_links"]))
    if typ == "row_audit":
        rows = []
        for key,t in C.TABLES.items():
            for i,r in enumerate(t["rows"],1):
                issues = V.row_issues(key,r,C)
                rows.append("<tr><td>%s-%d</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (key,i,C.pill("PASS" if not issues else "FAIL","ok" if not issues else "bad"),C.esc("Source roles, source IDs and cell count valid; see row limitations" if not issues else "; ".join(issues)),C.source_links(r["src"])))
        return "<section class='panel'><h2>Row-level source audit</h2><div class='table-wrap'><table class='data-table'><thead><tr><th>Row</th><th>Structural result</th><th>Scope of check</th><th>Original sources</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div><p class='caption'>PASS means a valid, role-appropriate source reference, not independent proof of every statement. Owner-only and unverified values remain flagged. Company pages are not government verification.</p></section>"
    raise ValueError("Unknown section type: " + typ)


def shell(name, page):
    nav = []
    for group in C.NAV:
        nav.append("<div class='nav-group'><p>%s</p>" % C.esc(group["group"]))
        for href,label in group["links"]:
            nav.append("<a href='%s'%s>%s</a>" % (href, ' aria-current="page"' if href==name else "",C.esc(label)))
        nav.append("</div>")
    sections = "\n".join(render_section(s,name) for s in page["sections"])
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Source-first bathtub overflow repair decision dashboard for San Francisco."><title>%(title)s · Overflow repair dashboard</title><link rel="stylesheet" href="assets/dashboard.css"></head><body>
<a class="skip" href="#main">Skip to content</a><header class="topbar"><a class="brand" href="index.html">Overflow repair dashboard</a><button id="nav-toggle" aria-controls="sidebar" aria-expanded="false">Menu</button><span class="stamp">Evidence checked %(updated)s</span></header>
<div class="layout"><nav id="sidebar" aria-label="Dashboard navigation">%(nav)s</nav><main id="main"><div class="eyebrow">%(eyebrow)s</div><h1>%(h1)s</h1><p class="lede">%(lede)s</p>%(sections)s<footer><p>Desk research, not a confirmed contractor proposal. Official license facts, company statements and owner statements are distinguished throughout.</p><p><a href="sources.html">Sources</a> · <a href="verification.html">Verification</a> · <a href="flagged.html">Flagged for review</a> · <a href="%(repo)s">Repository</a></p><p>Historical archives: <a href="shortlist.html">shortlist</a> · <a href="bathtub-overflow/executive-summary.html">earlier dashboard</a> · <a href="docs/plumbing-index.html">docs archive</a> · <a href="docs/index.html">unrelated GEMS project</a></p></footer></main></div><script src="assets/dashboard.js"></script></body></html>""" % {
        "title":C.esc(page["title"]),"updated":C.CHECKED,"nav":"".join(nav),
        "eyebrow":C.esc(page["eyebrow"]),"h1":C.esc(page["h1"]),"lede":C.esc(page["lede"]),"sections":sections,"repo":C.META["repo_url"]}


def snapshot():
    tables = {}
    for key,t in C.TABLES.items():
        tables[key] = {"title":t["title"],"columns":t["columns"],"caption":t["caption"],"rows":[]}
        for i,r in enumerate(t["rows"],1):
            tables[key]["rows"].append({"id":"%s-%d" % (key,i),"cells":r["cells"],"sources":r["src"],"source_urls":[C.SOURCES[s]["url"] for s in r["src"]],"issues":V.row_issues(key,r,C)})
    return {"schema_version":2,"generated_by":"scripts/build_dashboard.py","metadata":C.META,
            "verification_scope":"Offline structure, source roles and direct-read register consistency; not a network or scientific certification",
            "sources":C.SOURCES,"tables":tables,"pages":C.PAGES,"navigation":C.NAV,
            "evidence_register":"data/canonical/source_evidence.json"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=ROOT)
    ap.add_argument("--verify-only",action="store_true")
    args=ap.parse_args()
    out=args.output
    if not args.verify_only:
        out.mkdir(parents=True,exist_ok=True)
        for name,page in C.PAGES.items():
            (out/name).write_text(shell(name,page))
        (out/"shortlist.html").write_text(C.HISTORICAL_SHORTLIST)
        # Preserve the prior verification archive while replacing the live dashboard.
        old_log=out/"verification-log.html"
        if old_log.exists() and old_log.read_text() == C.HISTORICAL_SHORTLIST:
            raise RuntimeError("Historical verification archive missing")
        (out/"assets").mkdir(exist_ok=True)
        for name in ("dashboard.css","dashboard.js"):
            src=ROOT/"assets"/name
            if src.resolve()!=(out/"assets"/name).resolve():
                shutil.copy2(src,out/"assets"/name)
        (out/"data"/"canonical").mkdir(parents=True,exist_ok=True)
        (out/"data"/"canonical"/"site_data.json").write_text(json.dumps(snapshot(),indent=2,ensure_ascii=False)+"\n")
        if (ROOT/"data"/"canonical"/"source_evidence.json").resolve() != (out/"data"/"canonical"/"source_evidence.json").resolve():
            shutil.copy2(ROOT/"data"/"canonical"/"source_evidence.json",out/"data"/"canonical"/"source_evidence.json")
        (out/".nojekyll").touch()
    report=V.verify(out,C)
    (ROOT/"data"/"canonical").mkdir(parents=True,exist_ok=True)
    (ROOT/"data"/"canonical"/"verification_report.json").write_text(json.dumps(report,indent=2)+"\n")
    (ROOT/"data"/"canonical"/"verification_report.md").write_text(V.markdown(report))
    print(json.dumps({k:report[k] for k in ("ok","pages","tables","rows","sources","broken_links","row_issues")},indent=2))
    return 0 if report["ok"] else 1

if __name__=="__main__":
    raise SystemExit(main())
