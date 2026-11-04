#!/usr/bin/env python3
"""Regression tests for the Korea7 submission audit.

These tests read the saved artifacts and the candidate TIF. They do not run the
holdout (slow) or the site build; they verify the numbers that the site displays.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import rasterio
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57 import grid as ggrid          # noqa: E402
from gems57 import uniqueness             # noqa: E402
from gems57 import validate as gvalidate   # noqa: E402

DATA = ROOT / "data"
DOCS_DATA = ROOT / "docs" / "data"
DOCS = ROOT / "docs"
CANDIDATE = DOCS / "downloads/korea7-consensus-offcat-20k-20261104-zeros.tif"
CANDIDATE_ZIP = CANDIDATE.with_suffix(".zip")
CANDIDATE_JSON = CANDIDATE.with_suffix(".json")
CARD = json.loads((DOCS_DATA / "consensus_run_card.json").read_text())
VAL = json.loads((DOCS_DATA / "consensus_validation.json").read_text())
UNIQ = json.loads((DOCS_DATA / "consensus_uniqueness.json").read_text())
SITES = json.loads((DOCS_DATA / "site_analysis.json").read_text())
FOCUS = json.loads((DOCS_DATA / "focus_analysis.json").read_text())
MANIFEST = json.loads((DOCS_DATA / "site_manifest.json").read_text())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def test_candidate_exists():
    assert CANDIDATE.is_file()
    assert CANDIDATE_ZIP.is_file()
    assert CANDIDATE_JSON.is_file()
    assert CANDIDATE.stat().st_size == CARD["raster"]["bytes"]


def test_candidate_sha256():
    assert sha256(CANDIDATE) == CARD["raster"]["sha256"]
    assert sha256(CANDIDATE_ZIP) == CARD["raster"]["zip_sha256"]


def test_candidate_format():
    g = ggrid.load_grid(DATA / "bridge")
    receipt = gvalidate.validate(CANDIDATE, g.footprint, g.catalogue)
    assert receipt["all_checks_passed"]
    assert receipt["meta"]["count"] == 1
    assert receipt["meta"]["dtype"] == "float32"
    assert receipt["meta"]["crs"] == "EPSG:32611"
    assert receipt["meta"]["shape"] == [3730, 3292]
    assert receipt["meta"]["transform"] == [100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0]
    assert receipt["n_nan"] == 0
    assert receipt["n_infinite"] == 0
    assert receipt["min"] == 0.0
    assert receipt["max"] == 1.0
    assert receipt["on_catalogue_positive_pixels"] == 0
    assert receipt["in_footprint_positive_pixels"] == 20000


def test_candidate_zip():
    with zipfile.ZipFile(CANDIDATE_ZIP) as z:
        names = z.namelist()
        assert names == [CANDIDATE.name]
        assert z.read(names[0]) == CANDIDATE.read_bytes()


def test_candidate_name_and_note():
    assert 1 <= len(CARD["name"]) <= 140
    assert 1 <= len(CARD["note"]) <= 140
    assert CARD["name"] == CANDIDATE.stem
    assert CARD["note_chars"] == len(CARD["note"])


def test_candidate_geometry():
    geo = CARD["geometry"]
    assert geo["dots"] == 20000
    assert geo["on_catalogue"] == 0
    assert geo["far_fraction"] == pytest.approx(0.857, abs=1e-3)
    assert geo["near2_fraction"] == 0.0
    assert geo["median_distance_px"] > 30


def test_candidate_projection():
    p = CARD["projection"]
    assert p["evidence_class"].startswith("PROJECTED")
    assert p["projected_value"] == pytest.approx(0.3382, abs=1e-3)
    assert p["bootstrap_95_interval"][0] < p["projected_value"] < p["bootstrap_95_interval"][1]
    assert p["delta_vs_B2_projection"] > 0


def test_candidate_holdout():
    h = CARD["holdout"]
    assert h["evidence_class"] == "HOLDOUT-DTI"
    assert h["pooled_dti"] == pytest.approx(0.0, abs=1e-9)
    assert h["ci95"] == [0.0, 0.0]
    assert CARD["random_control_holdout"]["pooled_dti"] > 0
    assert CARD["verdict"] == "negative"
    assert CARD["ok_to_submit"] is False


def test_candidate_unique_vs_focus():
    g = ggrid.load_grid(DATA / "bridge")
    with rasterio.open(CANDIDATE) as src:
        cand = src.read(1)
    for site, row in SITES["sites"].items():
        with rasterio.open(ROOT / row["file"]) as src:
            a = src.read(1)
        fwd = uniqueness.dot_overlap(cand, a)
        assert fwd == pytest.approx(0.0, abs=1e-9), (site, fwd)
        assert not np.array_equal((cand > 0) & g.footprint, (a > 0) & g.footprint)
    assert UNIQ["nine_focus_gate_passes"] is True
    assert UNIQ["max_abs_surface_spearman_focus"] < 0.90


def test_candidate_lattice_flagged():
    lat = CARD["uniqueness_vs_focus"]["13GEMSDOE_lattice"]
    assert lat["forward_3px_overlap"] > 0.70
    assert "covering-grid" in lat["note"]


def test_nine_focus_are_duplicates():
    for site, row in SITES["sites"].items():
        assert row["unique_vs_other_focus"] is False
        assert row["max_forward_overlap_other_focus"] > 0.70


def test_nine_focus_highest_reported():
    best = max(SITES["sites"], key=lambda s: SITES["sites"][s]["user_reported_score"])
    assert best == "GEMSDOE32"
    assert SITES["sites"][best]["user_reported_score"] == 0.2778


def test_nine_focus_highest_holdout():
    best = max(SITES["sites"], key=lambda s: SITES["sites"][s]["holdout"]["pooled_dti"])
    assert best in ("GEMSDOE25", "GEMSDOE30")
    assert SITES["sites"][best]["holdout"]["pooled_dti"] == pytest.approx(0.1023, abs=1e-3)


def test_projection_model_fits_b2():
    model = FOCUS["projection_model"]
    assert model["n_observations"] == 9
    assert model["loo_rmse"] < 0.01
    assert model["fitted_B2"] == pytest.approx(0.2769, abs=1e-3)


def test_site_pages_exist():
    for name in MANIFEST["pages"]:
        assert (DOCS / name).is_file(), name


def test_site_download_links():
    for name in ("index.html", "executive-summary.html", "how-to-submit.html", "validation.html"):
        s = (DOCS / name).read_text()
        assert "korea7-consensus-offcat-20k-20261104-zeros.tif" in s
        assert "NOT CLEARED" in s or "not cleared" in s


def test_site_status_obvious():
    s = (DOCS / "index.html").read_text()
    assert "Download: OK. Submit: NOT CLEARED." in s
    assert "Research artifact" in s
    assert "HOLDOUT-DTI" in s
    assert "PROJECTED" in s


def test_site_manifest():
    c = MANIFEST["candidate"]
    assert c["name"] == CARD["name"]
    assert c["sha256"] == CARD["raster"]["sha256"]
    assert c["ok_to_submit"] is False
    assert c["verdict"] == "negative"
    assert c["nine_focus_gate_passes"] is True
    assert c["lattice_overlap"] > 0.70


def test_run_card_fields():
    for key in ("hypothesis", "mechanism", "named_non_fault_mimic", "holdout",
                "projection", "uniqueness_vs_focus", "raster", "validator_output",
                "name", "note", "verdict"):
        assert key in CARD
    assert CARD["raster"]["sha256"] == VAL["validator"]["sha256"]
    assert VAL["all_checks_passed"] is True
    assert CARD["zip_check"]["single_tiff"] is True
