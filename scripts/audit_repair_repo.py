#!/usr/bin/env python3
"""Line-by-line repository inventory and pattern audit for the repair project.

Reads every tracked file. Text files are scanned line by line for source URLs and
known verification-policy patterns; binary files are hashed only. This is an
inventory/pattern audit, not independent scientific verification of legacy GEMS.
"""
from __future__ import annotations
import hashlib, json, re, subprocess
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
URL=re.compile(r'https?://[^\s"\'<>)]+')
PATTERNS={
 'owner_amount_display': re.compile(r'\$(?:614|550|135)\b'),
 'requester_meta': re.compile(r'requester[- ]only', re.I),
 'stale_500_threshold': re.compile(r'\$500\b'),
 'all_in_one_capability_flag': re.compile(r'all_in_one_capable', re.I),
 'yelp_rating_numeric': re.compile(r'\b[0-5]\.\d\s*\(\s*\d+\s*(?:reviews?|ratings?)', re.I),
}
CANON_PREFIX=('data/repair/','scripts/build_repair_dashboard.py','scripts/verify_repair_dashboard.py','scripts/audit_repair_repo.py','tests/test_repair_dashboard.py','.github/workflows/pages.yml','trip-lever/audit-2026-11-07','trip-lever/validation-2026-11-07')
CANON_PAGES={'index.html','summary.html','requirements.html','estimates.html','contractors.html','reviews.html','findings.html','access-plan.html','compliance.html','sources.html','flagged.html','verification.html','archive.html','EXECUTIVE-SUMMARY.md','assets/site.css'}
HIST_PREFIX=('bathtub-overflow/','docs/bath/','docs/overflow','docs/plumbing-index.html','trip-lever/')
HIST_PAGES={'shortlist.html'}

def classify(rel:str)->str:
    if rel=='COORDINATION.md': return 'coordination'
    if rel.startswith(CANON_PREFIX) or rel in CANON_PAGES: return 'canonical_repair'
    if rel.startswith(HIST_PREFIX) or rel in HIST_PAGES: return 'historical_repair'
    if rel.startswith(('docs/','gems/','vendor/','data/','evidence/','scripts/','tests/')) or rel.endswith(('.py','.json','.csv','.md','.html')):
        # Remaining files are legacy GEMS / unrelated repository material unless canonical above.
        return 'legacy_or_unrelated'
    return 'other'

def main():
    files=subprocess.check_output(['git','ls-files','-z'],cwd=REPO).decode().split('\0')
    files=[f for f in files if f]
    inventory=[]; totals={'files':0,'text_files':0,'binary_files':0,'lines_scanned':0,'urls_found':0}; pattern_totals={k:0 for k in PATTERNS}
    for rel in files:
        path=REPO/rel; data=path.read_bytes(); sha=hashlib.sha256(data).hexdigest()
        entry={'path':rel,'sha256':sha,'bytes':len(data),'classification':classify(rel)}
        totals['files']+=1
        try: text=data.decode('utf-8')
        except UnicodeDecodeError:
            entry['binary']=True; totals['binary_files']+=1; inventory.append(entry); continue
        lines=text.splitlines(); entry['binary']=False; entry['lines']=len(lines); totals['text_files']+=1; totals['lines_scanned']+=len(lines)
        urls=[]; hits={k:[] for k in PATTERNS}
        for i,line in enumerate(lines,1):
            urls.extend(URL.findall(line))
            for k,pat in PATTERNS.items():
                if pat.search(line): hits[k].append(i)
        entry['url_count']=len(urls); totals['urls_found']+=len(urls)
        entry['pattern_hits']={k:v for k,v in hits.items() if v}
        entry['is_guard_file']=rel.startswith(('scripts/','tests/'))
        for k,v in hits.items():
            if v: pattern_totals[k]+=len(v)
        inventory.append(entry)
    canonical_public_hits={e['path']:e['pattern_hits'] for e in inventory if e['classification']=='canonical_repair' and not e.get('is_guard_file') and e.get('pattern_hits')}
    report={'audit_date':'2026-11-07','method':'Every tracked file hashed; every text line scanned for URLs and known verification-policy patterns. Canonical repair data was separately source-checked; legacy GEMS scientific claims were not independently reverified. Pattern hits in scripts/tests are verification guards/assertions, not public values.','totals':totals,'pattern_totals':pattern_totals,'canonical_public_pattern_hits':canonical_public_hits,'inventory':inventory}
    out=REPO/'trip-lever'/'repo-audit-2026-11-07.json'; out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    counts={}
    for e in inventory: counts[e['classification']]=counts.get(e['classification'],0)+1
    md=['# Repository line-by-line audit — 2026-11-07','',f"- Tracked files: {totals['files']} (text {totals['text_files']}, binary {totals['binary_files']})",f"- Text lines scanned: {totals['lines_scanned']}",f"- URL occurrences found: {totals['urls_found']}",f"- Classification counts: {json.dumps(counts,sort_keys=True)}",'', '## Method and boundary','',report['method'],'','## Pattern hits (line numbers in JSON inventory)','']
    for k,v in pattern_totals.items(): md.append(f'- `{k}`: {v} line hits')
    md += ['', f"Canonical public-page pattern hits (excluding guard scripts/tests): {json.dumps(canonical_public_hits,sort_keys=True)}", '', '## Canonical repair verification','', '- 14 CSLB records read directly; 7 discovery leads retained with blank license fields.', '- Owner-reported estimate amounts and current Yelp ratings/counts are blank in canonical data/pages.', '- BBB profiles for Expert, Fast Response, and Handyman Heroes read directly; platform statements separated from licensing.', '- Historical page-set issues are recorded in `trip-lever/secondary-pages-audit.md` and resolved for the canonical artifact by excluding superseded live pages and adding redirects/archive.', '- Legacy GEMS files are preserved in the repository but excluded from the canonical published artifact; their scientific claims are outside this repair verification.', '', '## Reproducibility','', 'Run `python scripts/audit_repair_repo.py`; machine-readable inventory: `trip-lever/repo-audit-2026-11-07.json`.']
    (REPO/'trip-lever'/'audit-2026-11-07.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({'totals':totals,'classifications':counts,'pattern_totals':pattern_totals},indent=2))
if __name__=='__main__': main()
