#!/usr/bin/env python3
"""Line-by-line repository audit for the overflow dashboard integration.

Scans every tracked file, counts text lines, parses JSON/Python, checks internal
HTML links/anchors, and flags merge markers, privacy wording and unfilled template
markers. Writes data/canonical/repo_audit.json and repo_audit.md.

This is a reproducible inventory/scan, not a claim that unrelated legacy scientific
content has been officially validated. Legacy flags are reported, not silently edited.
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
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import verify_dashboard as V  # noqa: E402

BINARY_EXT = {
    '.tif', '.tiff', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.ico',
    '.pdf', '.zip', '.gz', '.tar', '.pyc', '.pyo', '.so', '.dylib', '.dll',
    '.exe', '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4', '.mov', '.avi',
}
MERGE_RE = re.compile(r'^(<{7}|={7}|>{7})(?:\s|$)')
HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')


def tracked_files() -> list[Path]:
    out = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT)
    return [ROOT / p.decode() for p in out.split(b'\0') if p]


def is_text(path: Path) -> bool:
    return path.suffix.lower() not in BINARY_EXT


def main() -> int:
    files = tracked_files()
    inventory = []
    flags = []
    counts = Counter()
    total_bytes = 0
    total_lines = 0
    html_ids: dict[str, set[str]] = {}
    html_links: list[tuple[str, str]] = []

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        total_bytes += len(data)
        counts[path.suffix.lower() or '(none)'] += 1
        entry = {'path': rel, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'text': is_text(path)}
        if not is_text(path):
            entry['lines'] = None
            inventory.append(entry)
            continue
        text = data.decode('utf-8', errors='replace')
        lines = text.splitlines()
        entry['lines'] = len(lines)
        total_lines += len(lines)
        parse = 'not-applicable'
        if path.suffix == '.json':
            try:
                json.loads(text)
                parse = 'pass'
            except Exception as exc:
                parse = 'fail'
                flags.append({'path': rel, 'line': None, 'kind': 'json-parse', 'detail': str(exc)})
        elif path.suffix == '.py':
            try:
                ast.parse(text)
                parse = 'pass'
            except Exception as exc:
                parse = 'fail'
                flags.append({'path': rel, 'line': getattr(exc, 'lineno', None), 'kind': 'python-parse', 'detail': str(exc)})
        entry['parse'] = parse
        file_flags = 0
        generated_report = rel in {'data/canonical/repo_audit.json', 'data/canonical/repo_audit.md'}
        if generated_report:
            entry['generated'] = True
            entry['sha256'] = None
            entry['note'] = 'Generated audit output; final bytes are written after this scan.'
            inventory.append(entry)
            continue
        for lineno, line in enumerate(lines, 1):
            kinds = []
            if MERGE_RE.match(line):
                kinds.append('merge-marker')
            for pat in V.PRIVACY_PATTERNS:
                if re.search(pat, line, re.I):
                    kinds.append('privacy-pattern')
                    break
            for pat in V.PLACEHOLDER_PATTERNS:
                if re.search(pat, line, re.I):
                    kinds.append('placeholder')
                    break
            for kind in kinds:
                detail = line.strip()[:160]
                if kind == 'placeholder' and (
                    'placeholder=' in line.lower()
                    or 'input.placeholder' in line.lower()
                    or 'PLACEHOLDER_PATTERNS' in line
                    or '"PLACEHOLDER" in' in line
                    or "'PLACEHOLDER' in" in line
                    or "kinds.append('placeholder')" in line
                    or 'placeholder scan' in line.lower()
                    or 'template-marker scan' in line.lower()
                    or 'placeholder text' in line.lower()
                    or 'placeholder left' in line.lower()
                ):
                    kind = 'benign-placeholder-reference'
                elif kind == 'privacy-pattern' and rel.startswith('tests/') and ('r"' in line or "r'" in line):
                    kind = 'benign-privacy-pattern-definition'
                flags.append({'path': rel, 'line': lineno, 'kind': kind, 'detail': detail})
                file_flags += 1
        entry['line_flags'] = file_flags
        if path.suffix == '.html':
            html_ids[rel] = set(ID_RE.findall(text))
            for raw in HREF_RE.findall(text):
                html_links.append((rel, html.unescape(raw)))
        inventory.append(entry)

    broken = []
    broken_anchors = []
    for page, url in html_links:
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        path_part, _, frag = url.partition('#')
        clean = unquote(path_part.split('?', 1)[0])
        target_rel = page
        if clean:
            target = (ROOT / page).parent / clean
            try:
                target_rel = target.resolve().relative_to(ROOT).as_posix()
            except ValueError:
                broken.append({'page': page, 'url': url})
                continue
            if not (ROOT / target_rel).exists():
                broken.append({'page': page, 'url': url})
                continue
        if frag and target_rel.endswith('.html') and frag not in html_ids.get(target_rel, set()):
            broken_anchors.append({'page': page, 'url': url})
    for f in broken:
        flags.append({'path': f['page'], 'line': None, 'kind': 'broken-internal-link', 'detail': f['url']})
    for f in broken_anchors:
        flags.append({'path': f['page'], 'line': None, 'kind': 'broken-internal-anchor', 'detail': f['url']})

    flag_counts = Counter(f['kind'] for f in flags)
    report = {
        'generated_by': 'scripts/audit_repository.py',
        'tracked_files': len(files),
        'total_bytes': total_bytes,
        'text_lines': total_lines,
        'extension_counts': dict(sorted(counts.items())),
        'json_files': sum(1 for e in inventory if e['path'].endswith('.json')),
        'python_files': sum(1 for e in inventory if e['path'].endswith('.py')),
        'parse_failures': [f for f in flags if f['kind'].endswith('-parse')],
        'broken_internal_links': broken,
        'broken_internal_anchors': broken_anchors,
        'flag_counts': dict(flag_counts),
        'flags': flags,
        'inventory': inventory,
        'note': 'Line-by-line scan of tracked files. Legacy scientific/GEMS content is inventoried and scanned, not officially validated or edited.',
    }
    out = ROOT / 'data' / 'canonical'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'repo_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')

    md = ['# Repository line-by-line audit', '',
          f"- Tracked files: {len(files)}",
          f"- Total bytes: {total_bytes}",
          f"- Text lines scanned: {total_lines}",
          f"- JSON files: {report['json_files']}; Python files: {report['python_files']}",
          f"- Parse failures: {len(report['parse_failures'])}",
          f"- Broken internal links: {len(broken)}",
          f"- Broken internal anchors: {len(broken_anchors)}",
          f"- Line flags: {dict(flag_counts)}", '',
          '## Flags', '']
    if flags:
        md += ['| Path | Line | Kind | Detail |', '|---|---:|---|---|']
        for f in flags[:500]:
            detail = str(f['detail']).replace('|', '\\|')
            md.append(f"| {f['path']} | {f['line'] or ''} | {f['kind']} | {detail} |")
        if len(flags) > 500:
            md.append(f"\n… {len(flags)-500} more flags in repo_audit.json.")
    else:
        md.append('No merge-marker, privacy-pattern, placeholder, parse or broken-internal-link flags found.')
    md += ['', '## File inventory', '', '| Path | Bytes | Lines | Parse | Line flags |', '|---|---:|---:|---|---:|']
    for e in inventory:
        md.append(f"| {e['path']} | {e['bytes']} | {e['lines'] if e['lines'] is not None else 'binary'} | {e.get('parse', 'binary')} | {e.get('line_flags', 0)} |")
    md += ['', 'Full machine-readable inventory and flag list: `repo_audit.json`.', '']
    (out / 'repo_audit.md').write_text('\n'.join(md))
    print(f"Audited {len(files)} tracked files, {total_lines} text lines; flags={dict(flag_counts)}; broken={len(broken)}; broken_anchors={len(broken_anchors)}; parse_failures={len(report['parse_failures'])}")
    return 0 if not report['parse_failures'] and not broken and not broken_anchors else 1


if __name__ == '__main__':
    raise SystemExit(main())
