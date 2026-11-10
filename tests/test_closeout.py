"""The scope comparison must not convert marketing into a job commitment."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard_content as C


def test_scope_fit_rows_have_official_sources_and_blank_prices():
    rows = C.TABLES['scope_fit_closeout']['rows']
    assert len(rows) == 3
    for row in rows:
        assert C.BLANK in row['cells'][3]
        assert C.UNVERIFIED in row['cells'][3]
        assert row['src']
        for sid in row['src']:
            assert C.SOURCES[sid]['tier'] in ('company', 'official')


def test_independent_read_limits_are_explicit():
    d = json.loads((ROOT / 'data/canonical/closeout-2026-11-10.json').read_text())
    assert len(d['reads']) == 5
    assert d['job_price'] is None
    assert not d['provider_contacted']
    assert not d['exact_repair_experience_confirmed']
    assert not d['one_contract_restoration_confirmed']
    assert d['reads'][0]['timestamp'] == '11/9/2026 4:51:45 PM'
    assert C.SOURCES['S111']['url'] == 'https://www.handymanhero.es/construction-services/'
