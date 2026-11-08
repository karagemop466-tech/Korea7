#!/usr/bin/env python3
"""Offline dashboard verification — no network check.

Checks rendered links/anchors, row provenance, blank flags, source roles,
license-field agreement with direct-read excerpts, navigation and privacy.
A PASS is a structural/evidence-register check, not independent certification
of every sentence or a fresh license lookup.
"""
from __future__ import annotations
import datetime
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import dashboard_content as C  # noqa: E402

ASSET_RE = re.compile(r'(?:<link[^>]+href="([^"]+)"|<script[^>]+src="([^"]+)")')
HREF_RE = re.compile(r'<a\s[^>]*href="([^"]+)"', re.I)
ROW_RE = re.compile(r'<tbody>(.*?)</tbody>', re.S)
TR_RE = re.compile(r'<tr[^>]*>(.*?)</tr>', re.S)
TD_RE = re.compile(r'<td[^>]*>(.*?)</td>', re.S)
PRIVACY_PATTERNS = [
    r"without\s+a\s+permit", r"work\s+without\s+permit",
    r"no\s+permit\s+(?:is\s+)?(?:required|needed|pulled)",
    r"cannot\s+pull\s+a\s+permit", r"can(?:not|'?t)\s+pull\s+a\s+permit",
    r"permit\s+for\s+this\s+week", r"stay\s+private", r"never\s+mentioned",
    r"internal\s+use\s+only", r"most\s+contractors\s+and\s+plumbers",
    r"reasons\s+that\s+need\s+to\s+stay\s+private", r"private\s+rationale\s+for\s+",
]
PLACEHOLDER_PATTERNS = [r"\bTODO\b", r"\bTBD\b", r"\bPLACEHOLDER\b", r"example\.com", r"lorem ipsum"]
EXTENSIONS = {".html", ".md", ".json", ".css", ".js"}
SKIP_DIRS = {"node_modules", "vendor", "gems", "evidence", "registry", "data", "build", "dist", "out", "target", "coverage"}
GOVERNMENT_HOSTS = {"www2.cslb.ca.gov", "www.cslb.ca.gov", "cslb.ca.gov", "www.sf.gov", "sf.gov", "media.api.sf.gov", "leginfo.legislature.ca.gov", "docs.github.com", "github.com"}


def is_external(url):
    return url.startswith(("http://", "https://"))

def norm_url(url):
    # Do not html.unescape '&sectionNum' into a section sign.
    return url.replace("&amp;", "&")

def resolve_internal(page, url):
    clean = unquote(url.split("#",1)[0].split("?",1)[0])
    return page if not clean else (page.parent / clean).resolve()

def check(name, ok, detail):
    return {"name":name,"status":"PASS" if ok else "FAIL","detail":detail}

def plain(value):
    return html.unescape(re.sub(r"<[^>]+>", " ", value))

def row_issues(key, r, content=C):
    issues=[]
    t=content.TABLES[key]
    if len(r["cells"]) != len(t["columns"])-1:
        issues.append("cell count does not match columns")
    if not r["src"]:
        issues.append("no source")
    for sid in r["src"]:
        if sid not in content.SOURCES:
            issues.append("unknown source " + sid)
        elif content.SOURCES[sid]["status"] == "dead":
            issues.append("dead source " + sid)
    joined=" ".join(r["cells"])
    if content.BLANK in joined and content.UNVERIFIED not in joined:
        issues.append("blank without UNVERIFIED")
    tiers={content.SOURCES[s]["tier"] for s in r["src"] if s in content.SOURCES}
    # Official business sites are primary for their own statements, not government proof.
    if not tiers.intersection({"official","manufacturer","company"}):
        issues.append("no official/manufacturer/business source; contextual or blocked link only")
    if key == "estimates" and r["cells"][2] != content.UNKNOWN:
        issues.append("owner estimate entered as verified amount")
    if key == "ranking" and r["cells"][4] != content.UNKNOWN:
        issues.append("unverified job price entered in ranking")
    if key == "reviews" and (r["cells"][2] != content.UNKNOWN or r["cells"][3] != content.UNKNOWN):
        issues.append("blocked review values must remain blank")
    for number in re.findall(r"#(\d{6,8})", joined):
        if not any("LicNum="+number in content.SOURCES[s]["url"] for s in r["src"] if s in content.SOURCES):
            issues.append("license number lacks its official record link: " + number)
    return issues

def validate_content(content=C):
    issues=[]
    for key,t in content.TABLES.items():
        if not t["columns"] or t["columns"][-1] != "Source":
            issues.append(key + ": missing Source column")
        for i,r in enumerate(t["rows"],1):
            issues += [key+"-"+str(i)+": "+x for x in row_issues(key,r,content)]
    for sid,s in content.SOURCES.items():
        if not all(s.get(k) for k in ("url","tier","status","checked","supports")):
            issues.append(sid+": incomplete source metadata")
    evidence=json.loads((ROOT/"data/canonical/source_evidence.json").read_text())
    for lic in evidence["licenses"]:
        sid=lic["source"]
        s=content.SOURCES.get(sid)
        if not s or s["tier"]!="official" or "LicNum="+lic["number"] not in s["url"]:
            issues.append(sid+": license source mismatch")
        rows=[r for r in content.TABLES["contractors"]["rows"] if "LicNum="+lic["number"] in " ".join(content.SOURCES[x]["url"] for x in r["src"])]
        if len(rows)!=1:
            issues.append(lic["number"]+": expected one license register row")
            continue
        cells=[plain(x) for x in rows[0]["cells"]]
        for field,index in (("classes",2),("expires",3),("wc",4),("phone",6),("address",6)):
            values=lic[field] if isinstance(lic[field],list) else [lic[field]]
            for value in values:
                if str(value) not in cells[index]:
                    issues.append(lic["number"]+": register differs from evidence for "+field)
        if format(lic["bond"],",") not in cells[5] or lic["status"] not in cells[3]:
            issues.append(lic["number"]+": bond/status mismatch")
    for blocked in evidence["blocked"]:
        s=content.SOURCES.get(blocked["source"])
        if not s or s["url"]!=blocked["url"] or s["status"]!="blocked-403":
            issues.append(blocked["source"]+": blocked-source metadata mismatch")
    for page,spec in content.PAGES.items():
        for section in spec["sections"]:
            if section["type"]=="table" and section["ref"] not in content.TABLES:
                issues.append(page+": unknown table "+section["ref"])
    return issues


def analyze(root: Path, pages=None):
    pages=list(C.PAGES) if pages is None else pages
    checks=[]; broken_internal=[]; broken_anchors=[]; unknown_external=[]
    missing_row_links=[]; unflagged_blanks=[]; external_links=set(); internal_count=0
    row_count=0; nav_issues=[]; ids_by_page={}; privacy_hits=[]; placeholder_hits=[]
    source_urls={s["url"] for s in C.SOURCES.values()}
    dead_urls={s["url"] for s in C.SOURCES.values() if s["status"]=="dead"}
    for name in pages:
        p=root/name
        if not p.is_file():
            nav_issues.append("missing page "+name); continue
        text=p.read_text(encoding="utf-8")
        ids_by_page[name]=set(re.findall(r'\bid="([^"]+)"',text))
        for m in ASSET_RE.finditer(text):
            asset=m.group(1) or m.group(2)
            if is_external(asset): external_links.add(asset); continue
            internal_count+=1
            if not resolve_internal(p,asset).exists(): broken_internal.append(name+" -> "+asset)
    for name in pages:
        p=root/name
        if not p.is_file(): continue
        text=p.read_text(encoding="utf-8")
        if len(re.findall(r'aria-current="page"',text))!=1:
            nav_issues.append(name+": expected one current-page marker")
        for raw in HREF_RE.findall(text):
            url=norm_url(raw)
            if is_external(url):
                external_links.add(url)
                if url not in source_urls and not url.startswith((C.META["repo_url"],C.META["pages_url"])):
                    unknown_external.append(name+" -> "+url)
                if url in dead_urls: unknown_external.append(name+" -> DEAD "+url)
                continue
            if url.startswith(("mailto:","tel:","#")):
                if url.startswith("#") and len(url)>1 and url[1:] not in ids_by_page.get(name,set()):
                    broken_anchors.append(name+" -> "+url)
                continue
            internal_count+=1
            target=resolve_internal(p,url)
            if not target.exists(): broken_internal.append(name+" -> "+url); continue
            parts=url.split("#",1)
            if len(parts)>1 and parts[1]:
                try: key=target.relative_to(root).as_posix()
                except ValueError: key=target.as_posix()
                if key in ids_by_page and parts[1] not in ids_by_page[key]: broken_anchors.append(name+" -> "+url)
        for body in ROW_RE.findall(text):
            for idx,tr in enumerate(TR_RE.findall(body),1):
                row_count+=1; cells=TD_RE.findall(tr)
                if not cells or not HREF_RE.search(cells[-1]): missing_row_links.append(name+" row "+str(idx))
                if 'class="blank"' in tr and "UNVERIFIED" not in tr and "blank — unverified" not in tr:
                    unflagged_blanks.append(name+" row "+str(idx))
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat,text,re.I): placeholder_hits.append(name+": "+pat)
    # Scan published text, excluding hidden/environment directories and data archives.
    scanned=0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in EXTENSIONS: continue
        rel=path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]): continue
        if rel.as_posix().startswith("data/canonical/verification_report"): continue
        scanned+=1
        try: content=path.read_text(encoding="utf-8")
        except (UnicodeDecodeError,OSError): continue
        for pat in PRIVACY_PATTERNS:
            for m in re.finditer(pat,content,re.I):
                snippet=content[max(0,m.start()-60):m.end()+60].replace("\n"," ")
                privacy_hits.append(rel.as_posix()+": "+html.escape(snippet))
    content_issues=validate_content()
    snapshot_issues=[]
    snapshot_path=root/"data/canonical/site_data.json"
    if snapshot_path.is_file():
        data=json.loads(snapshot_path.read_text())
        if data.get("schema_version")!=2 or data.get("sources")!=C.SOURCES:
            snapshot_issues.append("source snapshot differs from generator")
        for key,t in C.TABLES.items():
            saved=data.get("tables",{}).get(key,{})
            if saved.get("columns")!=t["columns"] or len(saved.get("rows",[]))!=len(t["rows"]):
                snapshot_issues.append(key+": stale table snapshot")
            else:
                for actual,expected in zip(saved["rows"],t["rows"]):
                    if actual["cells"]!=expected["cells"] or actual["sources"]!=expected["src"]:
                        snapshot_issues.append(actual["id"]+": stale row")
    else: snapshot_issues.append("missing site_data.json")
    verified_sources=sum(s["status"]=="verified" for s in C.SOURCES.values())
    official_sources=sum(s["tier"] in ("official","manufacturer") and s["status"]=="verified" for s in C.SOURCES.values())
    checks += [
        check("Build output complete",not any(x.startswith("missing page") for x in nav_issues),"%d canonical pages"%len(pages)),
        check("Every table row has a source link",not missing_row_links,"%d rendered rows; %d missing"%(row_count,len(missing_row_links))),
        check("Blank values are flagged UNVERIFIED",not unflagged_blanks,"%d unflagged blanks"%len(unflagged_blanks)),
        check("Internal links resolve",not broken_internal,"%d links; %d broken"%(internal_count,len(broken_internal))),
        check("Anchor targets resolve",not broken_anchors,"%d broken anchors"%len(broken_anchors)),
        check("External links are in the source ledger",not unknown_external,"%d unique external links; %d unknown/dead"%(len(external_links),len(unknown_external))),
        check("Navigation consistent",not nav_issues,"%d issues"%len(nav_issues)),
        check("Privacy sweep (internal-only wording)",not privacy_hits,"%d published text files; %d matches"%(scanned,len(privacy_hits))),
        check("No unfilled template markers",not placeholder_hits,"%d matches"%len(placeholder_hits)),
        check("Dead sources not linked",not (dead_urls & external_links),"%d dead-source links"%len(dead_urls & external_links)),
        check("Source ledger records prior direct reads",official_sources>=10,"%d official/manufacturer; %d direct-read sources overall (metadata only; no network check)"%(official_sources,verified_sources)),
        check("Row source roles and evidence fields",not content_issues,"%d issues"%len(content_issues)),
        check("JSON snapshot matches generator",not snapshot_issues,"%d stale/missing entries"%len(snapshot_issues)),
    ]
    return {"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "scope":"Offline structural, privacy and direct-read register consistency; no network check",
            "pages":pages,"counts":{"pages":len(pages),"tables":len(C.TABLES),"rows":sum(len(t["rows"]) for t in C.TABLES.values()),
                "source_ledger_entries":len(C.SOURCES),"verified_sources":verified_sources,"official_or_manufacturer_verified":official_sources,
                "generated_tbody_rows":row_count,"internal_links_checked":internal_count,"unique_external_links":len(external_links),"published_text_files_scanned":scanned},
            "checks":checks,"broken_internal":broken_internal,"broken_anchors":broken_anchors,"unknown_external":unknown_external,
            "missing_row_links":missing_row_links,"unflagged_blanks":unflagged_blanks,"privacy_matches":privacy_hits,"nav_issues":nav_issues,
            "content_issues":content_issues,"snapshot_issues":snapshot_issues,"dead_sources":sorted(dead_urls),"external_links":sorted(external_links)}

def verify(root, content=C):
    # Content is the canonical module; retain the argument for the builder API.
    report=analyze(root)
    report.update(ok=all(c["status"]=="PASS" for c in report["checks"]),
                  tables=report["counts"]["tables"],rows=report["counts"]["rows"],sources=report["counts"]["source_ledger_entries"],
                  pages=report["counts"]["pages"],broken_links=report["broken_internal"]+report["broken_anchors"],
                  row_issues=report["content_issues"])
    return report

def markdown(report):
    lines=["# Dashboard verification report","", "Generated: "+report["generated_at"], "", report.get("scope",""), "", "| Check | Result | Detail |","|---|---|---|"]
    for c in report["checks"]:
        lines.append("| %s | %s | %s |"%(c["name"],c["status"],c["detail"].replace("|","\\|")))
    lines += ["","## Counts",""]+["- %s: %s"%(k,v) for k,v in report["counts"].items()]
    lines += ["","## Limitations","",
              "- Source links were read on 2026-11-08; this verifier performs no network check.",
              "- A source-role/structure PASS does not independently prove every sentence.",
              "- Owner-only amounts remain blank in verified-value cells; original transcriptions are labeled separately.",
              "- Blocked Yelp pages have no verified ratings, counts or exact-job reviews.",
              "- Repository-wide audit and deployment are separate checks; see repo-review.html and COORDINATION.md.",""]
    return "\n".join(lines)

def write_report(root,report):
    out=root/"data/canonical"; out.mkdir(parents=True,exist_ok=True)
    (out/"verification_report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    (out/"verification_report.md").write_text(markdown(report))

def main():
    report=verify(ROOT); write_report(ROOT,report)
    for c in report["checks"]: print("[%s] %s — %s"%(c["status"],c["name"],c["detail"]))
    return 0 if report["ok"] else 1

if __name__=="__main__": raise SystemExit(main())
