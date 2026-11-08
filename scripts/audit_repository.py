#!/usr/bin/env python3
"""Non-destructive tracked-file audit and reproducible line inventory.

Every tracked text file is decoded and split into lines; JSON/Python syntax,
HTML links/anchors, merge markers and pinned download hashes are checked.
This is not semantic certification of unrelated scientific claims. The full
pytest suite is run and its actual exit code/summary recorded. No network check.
"""
from __future__ import annotations
import ast
import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT=Path(__file__).resolve().parents[1]
REPO="https://github.com/karagemop466-tech/Korea7"
OUT=ROOT/"data/canonical"
TEXT_SUFFIXES={".py",".md",".html",".css",".js",".json",".txt",".csv",".yml",".yaml",".toml",".cfg",".ini",".sh",".svg",".xml",".gitignore",".nojekyll"}

class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ids=set(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if a.get("name") and tag=="a": self.ids.add(a["name"])
        for key in ("href","src"):
            if a.get(key): self.refs.append((tag,key,a[key]))
    def handle_entityref(self,name):
        # Preserve URL query entities such as &sectionNum; HTMLParser otherwise
        # can interpret named entities without a terminating semicolon.
        pass


def tracked():
    raw=subprocess.check_output(["git","ls-files","-z"],cwd=ROOT)
    return sorted(x.decode() for x in raw.split(b"\0") if x)


def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()


def category(path):
    p=path.lower()
    if p.startswith(("gems/","evidence/","registry/","vendor/","data/bridge/","data/focus/","data/reference/","data/registry/")) or "gems" in p or p.endswith((".tif",".tiff")):
        return "legacy-scientific-or-vendor"
    if p.startswith(("bathtub-overflow/","docs/bath/","sf-overflow-audit/","trip-lever/")) or p.startswith("docs/overflow-") or p in {"shortlist.html","verification-log.html","docs/plumbing-index.html","docs/parallel-index.html","executive-summary.md"}:
        return "historical-overflow"
    if p.startswith(("scripts/","tests/","assets/","data/canonical/")) or "/" not in p and p.endswith(".html") or p.startswith(".github/"):
        return "canonical-or-shared"
    return "other-documentation-data"


def main():
    files=tracked(); inventory=[]; json_errors=[]; python_errors=[]; merge_markers=[]
    html_pages={}; text_lines=0; binary_count=0; total_bytes=0
    for rel in files:
        p=ROOT/rel
        if not p.is_file(): continue
        data=p.read_bytes(); total_bytes+=len(data)
        item={"path":rel,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"category":category(rel)}
        is_text=(p.suffix.lower() in TEXT_SUFFIXES or p.name in {".gitignore",".nojekyll","LICENSE"}) and b"\0" not in data
        if is_text:
            try: text=data.decode("utf-8-sig")
            except UnicodeDecodeError as e:
                item.update(kind="binary-or-non-utf8",lines=None,decode_error=str(e)); binary_count+=1; inventory.append(item); continue
            lines=text.splitlines(); item.update(kind="text",lines=len(lines)); text_lines+=len(lines)
            for n,line in enumerate(lines,1):
                if re.match(r"^(<{7}|={7}|>{7})( |$)",line): merge_markers.append({"path":rel,"line":n})
            if p.suffix==".json":
                try: json.loads(text); item["json_syntax"]="PASS"
                except json.JSONDecodeError as e: item["json_syntax"]="FAIL"; json_errors.append({"path":rel,"error":str(e)})
            if p.suffix==".py":
                try: ast.parse(text,filename=rel); item["python_syntax"]="PASS"
                except SyntaxError as e: item["python_syntax"]="FAIL"; python_errors.append({"path":rel,"line":e.lineno,"error":e.msg})
            if p.suffix==".html":
                scan=PageScan(); scan.feed(text); html_pages[rel]=scan
        else:
            item.update(kind="binary",lines=None); binary_count+=1
        inventory.append(item)
    broken=[]; anchors=[]; directory_links=[]; external=set(); internal_checked=0
    for rel,scan in html_pages.items():
        page=ROOT/rel
        for tag,key,raw in scan.refs:
            url=raw.replace("&amp;","&")
            if url.startswith(("http://","https://")): external.add(url); continue
            if url.startswith(("mailto:","tel:","data:","javascript:")): continue
            parsed=urlparse(url); path=unquote(parsed.path)
            target=(page.parent/path).resolve() if path else page.resolve()
            if path:
                internal_checked+=1
                if not target.exists(): broken.append({"page":rel,"url":raw})
                elif target.is_dir(): directory_links.append({"page":rel,"url":raw,"target":target.relative_to(ROOT).as_posix() if target.is_relative_to(ROOT) else str(target),"index_exists":(target/"index.html").exists()})
            if parsed.fragment:
                try: keypath=target.relative_to(ROOT).as_posix()
                except ValueError: continue
                if keypath in html_pages and unquote(parsed.fragment) not in html_pages[keypath].ids:
                    anchors.append({"page":rel,"url":raw})
    pinned=[]
    sums=ROOT/"docs/downloads/SHA256SUMS.txt"
    for line in sums.read_text().splitlines():
        expected,rel=line.split(maxsplit=1); rel=rel.strip().lstrip("*"); path=ROOT/"docs/downloads"/rel
        actual=sha(path) if path.is_file() else None
        pinned.append({"path":"docs/downloads/"+rel,"expected":expected,"actual":actual,"match":actual==expected})
    # Explicit README/download artifact pairs, independently recomputed.
    for rel,expected in [
        ("docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif","9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c"),
        ("docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.zip","7460b2dd99ba2cd44d412b3d021fa1c30fb0a25b071b6e5f66a0c661a0d2a6a5"),
        ("docs/downloads/gemsdoe32-korea7-scarprad-b2cov-r100-20261104T201931Z-7dcabf26-zeros.tif","f013b9c451a38730bb2527d7d096b98d9447b67df9af45902fc998a2ec7bb40d"),
    ]:
        actual=sha(ROOT/rel) if (ROOT/rel).is_file() else None
        pinned.append({"path":rel,"expected":expected,"actual":actual,"match":actual==expected})
    run_cards=[]
    for rel in files:
        if re.search(r"(^|/)run[-_]card.*\.json$",rel):
            d=json.loads((ROOT/rel).read_text())
            run_cards.append({"path":rel,"top_level_keys":sorted(d) if isinstance(d,dict) else [],"bytes":(ROOT/rel).stat().st_size})
    # Actual test result, not an inferred PASS.
    proc=subprocess.run([sys.executable,"-m","pytest","-q","--tb=short"],cwd=ROOT,text=True,capture_output=True)
    test_output=proc.stdout+proc.stderr
    test_summary=next((line for line in reversed(test_output.splitlines()) if re.search(r"\b(passed|failed|error|no tests ran)\b",line)),"No summary emitted")
    findings=[
        {"id":"RA-01","severity":"info","status":"preserved","finding":"Unrelated legacy DOE GEMS code/data coexist with overflow research; scientific claims are outside this repair dashboard's certification.","paths":["README.md","gems/","data/"],"official_source":REPO+"/blob/main/README.md"},
        {"id":"RA-02","severity":"flag","status":"corrected-in-canonical","finding":"README banner had an outdated date/category count; canonical navigation and current audit are linked instead.","paths":["README.md"],"official_source":REPO+"/blob/main/README.md"},
        {"id":"RA-03","severity":"info","status":"checked","finding":"Pinned download hashes independently recomputed; results are in pinned_hashes. This does not validate scientific predictions.","paths":["docs/downloads/SHA256SUMS.txt"],"official_source":REPO+"/blob/main/docs/downloads/SHA256SUMS.txt"},
        {"id":"RA-04","severity":"flag","status":"preserved","finding":"Multiple run-card filenames/schemas coexist; keys and bytes inventoried, not silently normalized.","paths":[x["path"] for x in run_cards],"official_source":REPO+"/blob/main/run-card.json"},
        {"id":"RA-05","severity":"flag","status":"historical-flag","finding":"Legacy directory links may lack index.html and return 404 on Pages even when the directory exists locally; see directory_links.","paths":["docs/parallel-index.html","docs/results/"],"official_source":REPO+"/blob/main/docs/parallel-index.html"},
        {"id":"RA-06","severity":"flag","status":"corrected-in-canonical","finding":"Archived $500 licensing wording is superseded by current BPC 7048 under-$1,000 aggregate threshold plus other conditions.","paths":["docs/overflow-permits.html"],"official_source":"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048"},
        {"id":"RA-07","severity":"flag","status":"corrected-in-canonical","finding":"Owner-only amounts are blank in verified-value cells and retained only as labeled transcriptions; drywall inclusion is unknown, not assumed excluded.","paths":["estimates.html","brief.html","flagged.html"],"official_source":REPO+"/blob/main/data/canonical/source_evidence.json"},
        {"id":"RA-08","severity":"info","status":"integrated","finding":"Concurrent claims, U21/U22, BPC 7059 caveat, S61–S63 and regression tests retained; shared canonical output rebuilt after integration.","paths":["COORDINATION.md","scripts/dashboard_content.py","tests/"],"official_source":REPO+"/blob/main/COORDINATION.md"},
        {"id":"RA-09","severity":"flag","status":"corrected","finding":"Repository HTML walker previously entered hidden virtual environments and scanned dependency documentation; now excludes hidden/environment/build directories.","paths":["tests/test_overflow_site.py"],"official_source":REPO+"/blob/main/tests/test_overflow_site.py"},
        {"id":"RA-10","severity":"flag","status":"corrected-in-canonical","finding":"Source-link presence was previously described too broadly as verification; row audit now distinguishes source roles and direct-read evidence consistency.","paths":["scripts/verify_dashboard.py","verification.html"],"official_source":REPO+"/blob/main/data/canonical/source_evidence.json"},
        {"id":"RA-11","severity":"flag","status":"historical-flag","finding":"Historical internal broken links/anchors, if any, are inventoried rather than silently rewriting other sessions' archives. Canonical links must pass separately.","paths":sorted({x["page"] for x in broken+anchors}),"official_source":REPO+"/blob/main/data/canonical/repo_audit.json"},
        {"id":"RA-12","severity":"flag","status":"delivery-check","finding":"Pages deployment must be confirmed from the new Actions run and live content after merge; an older reachable page is not proof of a successful new deployment.","paths":["COORDINATION.md",".github/workflows/pages-check.yml"],"official_source":"https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages"},
    ]
    report={"schema_version":1,"generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "scope":"All tracked files inventoried; every UTF-8 text line read for count/merge markers; syntax and link structure checked. Not semantic certification of unrelated scientific claims. No network check.",
        "counts":{"tracked_files":len(files),"inventoried_files":len(inventory),"text_files":sum(x["kind"]=="text" for x in inventory),"text_lines":text_lines,"binary_or_non_utf8_files":binary_count,"tracked_bytes":total_bytes,"html_files":len(html_pages),"json_files":sum(x.get("json_syntax") is not None for x in inventory),"python_files":sum(x.get("python_syntax") is not None for x in inventory),"internal_file_references":internal_checked,"unique_external_links":len(external),"categories":dict(Counter(x["category"] for x in inventory))},
        "checks":{"json_syntax_errors":json_errors,"python_syntax_errors":python_errors,"merge_markers":merge_markers,"broken_internal_links":broken,"broken_anchors":anchors,"directory_links":directory_links,"pinned_hashes":pinned,"run_cards":run_cards},
        "tests":{"command":sys.executable+" -m pytest -q --tb=short","exit_code":proc.returncode,"summary":test_summary,"output_tail":test_output[-12000:]},
        "findings":findings,"inventory_file":"data/canonical/repo_line_inventory.json",
        "official_source":REPO+"/blob/main/data/canonical/repo_audit.json"}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"repo_line_inventory.json").write_text(json.dumps({"schema_version":1,"commit":report["commit"],"line_count_method":"UTF-8 text splitlines(); binary files have null lines. Hashes are captured at audit start; generated audit outputs may be rewritten during the run.","files":inventory},indent=2)+"\n")
    (OUT/"repo_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"counts":report["counts"],"json_errors":len(json_errors),"python_errors":len(python_errors),"merge_markers":len(merge_markers),"broken_internal":len(broken),"broken_anchors":len(anchors),"hashes_matched":sum(x["match"] for x in pinned),"hashes_checked":len(pinned),"tests":test_summary,"test_exit":proc.returncode},indent=2))
    hard_fail=bool(json_errors or python_errors or merge_markers or any(not x["match"] for x in pinned) or proc.returncode)
    return 1 if hard_fail else 0

if __name__=="__main__": raise SystemExit(main())
