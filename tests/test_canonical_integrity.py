"""Regression checks for the 2026-11-08 supplemental canonical overflow integration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard_content as C  # noqa: E402


def test_decision_weights_and_totals():
    decision = json.loads((ROOT / 'data/canonical/decision_analysis.json').read_text())
    criteria = decision['criteria']
    assert sum(c['weight'] for c in criteria) == 100
    weights = [c['weight'] for c in criteria]
    ids = [c['id'] for c in criteria]
    for cand in decision['candidates']:
        scores = [cand['scores'][i] for i in ids]
        assert all(0 <= s <= 2 for s in scores)
        assert cand['total'] == sum(w * s / 2 for w, s in zip(weights, scores))
    ranked = sorted(decision['candidates'], key=lambda c: c['rank'])
    assert [c['rank'] for c in ranked] == list(range(1, len(ranked) + 1))
    keys = [(-c['total'], -c['scores']['C3'], -c['scores']['C1'], c['name']) for c in ranked]
    assert keys == sorted(keys)


def test_source_checks_cover_eleven_active_licenses():
    checks = json.loads((ROOT / 'data/canonical/source_checks.json').read_text())
    licenses = checks['licenses']
    assert len(licenses) == 11
    assert checks['checked_date'] == '2026-11-08'
    for lic in licenses:
        assert lic['status'] == 'current and active'
        assert lic['data_current'].startswith('11/8/2026 ')
        assert lic['phone'] and lic['address'] and lic['bond'] == '$25,000'
        assert f"LicNum={lic['number']}" in lic['source']


def test_source_check_licenses_are_in_canonical_register():
    checks = json.loads((ROOT / 'data/canonical/source_checks.json').read_text())
    numbers = {lic['number'] for lic in checks['licenses']}
    rendered = ' '.join(' '.join(r['cells']) for tid in ('contractors', 'cslb_register', 'contacts') for r in C.TABLES[tid]['rows'])
    for number in numbers:
        assert f'LicNum={number}' in rendered


def test_flag_ids_are_unique_and_include_supplemental_flag():
    rows = C.TABLES['flagged']['rows']
    ids = [r['cells'][0] for r in rows]
    assert len(ids) == len(set(ids))
    assert 'U44' in ids


def test_angi_bathtub_category_correction():
    s24 = C.SOURCES['S24']
    assert '17 verified reviews' in s24['supports']
    assert 'October 14, 2024' in s24['supports']
    assert '873' not in s24['supports']
    assert '2026-08-01' not in s24['supports']
    for row in C.TABLES['findings']['rows']:
        if row['cells'][0] == 'F08':
            assert 'S24' not in row['src']


def test_texas_publisher_not_used_for_sf_permits():
    assert 'Houston' in C.SOURCES['S22']['note'] or 'Texas' in C.SOURCES['S22']['note']
    for row in C.TABLES['permits']['rows']:
        assert 'S22' not in row['src']


def test_advanced_identity_mismatch_is_flagged():
    assert C.SOURCES['S101']['url'] == 'https://advancedplumbinganddrain.com/'
    assert 'NOT matched' in C.SOURCES['S101']['note']
    assert any(r['cells'][0] == 'U44' and 'S101' in r['src'] for r in C.TABLES['flagged']['rows'])


def test_supplemental_artifacts_are_cited():
    for sid in ('S102', 'S103', 'S104'):
        assert sid in C.SOURCES
    assert any('S102' in r['src'] and 'S103' in r['src'] and 'S104' in r['src'] for r in C.TABLES['repo_review']['rows'])
