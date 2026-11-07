"""Regression tests for the canonical repair dashboard build and verification."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


build_mod = _load("build_repair_dashboard")
verify_mod = _load("verify_repair_dashboard")


@pytest.fixture(scope="module")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("repair-site")
    build_mod.build(out)
    return out


@pytest.fixture(scope="module")
def report(site) -> dict:
    return verify_mod.verify(site, check_determinism=False)


def test_build_is_deterministic(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    build_mod.build(a)
    build_mod.build(b)
    fa = {p.relative_to(a).as_posix(): p.read_bytes() for p in a.rglob("*") if p.is_file()}
    fb = {p.relative_to(b).as_posix(): p.read_bytes() for p in b.rglob("*") if p.is_file()}
    assert fa == fb


def test_required_pages_and_assets(site):
    for name in verify_mod.REQUIRED_PAGES:
        assert (site / name).is_file(), name
    assert (site / "assets" / "site.css").is_file()
    assert (site / ".nojekyll").exists()


def test_verification_passes(report):
    assert report["status"] == "passed", report["failures"]
    assert report["data_rows_checked"] > 150


def test_every_data_row_has_source_link(report):
    check = next(c for c in report["checks"] if c["name"] == "every_table_row_has_source_link")
    assert check["ok"], check["detail"]


def test_internal_links_and_anchors(report):
    check = next(c for c in report["checks"] if c["name"] == "internal_links_and_anchors")
    assert check["ok"], check["detail"]


def test_provider_counts_and_license_links(site):
    providers = json.loads((site / "data/repair/providers.json").read_text())["providers"]
    verified = [p for p in providers if p.get("license")]
    discovery = [p for p in providers if not p.get("license")]
    assert len(providers) == 21
    assert len(verified) == 14
    assert len(discovery) == 7
    assert all(p["cslb_url"].startswith("https://www2.cslb.ca.gov/") for p in verified)
    assert all(p["license"] is None and p["status"] is None for p in discovery)


def test_unconfirmed_values_are_blank(site):
    providers = json.loads((site / "data/repair/providers.json").read_text())["providers"]
    estimates = json.loads((site / "data/repair/estimates.json").read_text())["estimates"]
    assert all(p["rating"] is None and p["review_count"] is None for p in providers)
    assert all(q["amount_usd"] is None and q["official_amount_source"] is None for q in estimates)
    text = (site / "estimates.html").read_text()
    for amount in ("$614", "$550", "$135"):
        assert amount not in text


def test_estimate_amount_cells_render_blank(site):
    parser = verify_mod.AuditParser()
    parser.feed((site / "estimates.html").read_text())
    assert len(parser.rows) == 3
    for row in parser.rows:
        assert 'class="blank"' in row["cells"][3]["html"]
        assert "flagged.html#quotes" in row["cells"][3]["html"]


def test_privacy_and_no_contact_claim(report):
    privacy = next(c for c in report["checks"] if c["name"] == "privacy_wording")
    contact = next(c for c in report["checks"] if c["name"] == "no_contact_claim")
    assert privacy["ok"], privacy["detail"]
    assert contact["ok"]


def test_flags_resolve_and_are_published(site):
    flags = json.loads((site / "data/repair/flags.json").read_text())["flags"]
    providers = json.loads((site / "data/repair/providers.json").read_text())["providers"]
    ids = {f["id"] for f in flags}
    assert {fid for p in providers for fid in p["flags"]} <= ids
    html = (site / "flagged.html").read_text()
    for fid in ids:
        assert f'id="{fid}"' in html


def test_source_register_covers_primary_and_platform_evidence(site):
    sources = json.loads((site / "data/repair/sources.json").read_text())["sources"]
    urls = {s["url"] for s in sources}
    assert any("cslb.ca.gov" in u for u in urls)
    assert any("bbb.org" in u for u in urls)
    assert any("yelp.com" in u for u in urls)
    assert any("sf.gov" in u for u in urls)
    assert any("watcomfg.com" in u for u in urls)


def test_legacy_redirects_point_to_canonical_pages(site):
    expected = {
        "bathtub-overflow/index.html": "../index.html",
        "docs/plumbing-index.html": "../index.html",
        "docs/bath/index.html": "../../index.html",
        "docs/index.html": "../archive.html",
    }
    for old, target in expected.items():
        text = (site / old).read_text()
        assert f'href="{target}"' in text
        assert "canonical repair dashboard" in text


def test_no_historical_or_gems_data_in_artifact(site):
    # Canonical artifact contains only repair data plus compatibility redirects.
    assert not (site / "gems").exists()
    assert not (site / "docs/bath/data").exists()
    assert not (site / "docs/data").exists()
    data_files = {p.relative_to(site).as_posix() for p in (site / "data").rglob("*") if p.is_file()}
    assert all(p.startswith("data/repair/") or p == "data/validation.json" for p in data_files)
