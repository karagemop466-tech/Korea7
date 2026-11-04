"""Grid facts, the format gate, and the delivered artefact."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import grid, registry  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_reference_grid_facts_are_as_asserted():
    ref = grid.load_reference()
    with rasterio.open(grid.SAMPLE_SUBMISSION) as src:
        assert str(src.crs) == grid.EXPECTED_CRS
        assert (src.height, src.width) == (grid.EXPECTED_HEIGHT, grid.EXPECTED_WIDTH)
        assert tuple(src.transform)[:6] == grid.EXPECTED_TRANSFORM
    assert int(ref["footprint"].sum()) == grid.EXPECTED_FOOTPRINT_PIXELS
    assert int(ref["catalogue"].sum()) == grid.EXPECTED_CATALOGUE_PIXELS
    # the official sample IS the catalogue raster: 60988 ones, NaN exactly outside
    assert bool(((ref["sample"] == 1) == ref["catalogue"]).all())
    assert bool((np.isnan(ref["sample"]) == ~ref["footprint"]).all())
    assert bool((ref["labels"] != -1).sum() == grid.EXPECTED_FOOTPRINT_PIXELS)


def test_delivered_artefact_passes_the_format_gate():
    card = json.loads((ROOT / "evidence" / "run_card.json").read_text())
    tif = ROOT / card["file"]
    assert tif.exists(), tif
    assert grid.sha256(tif) == card["sha256"]
    report = grid.format_gate(tif)
    assert report["format_pass"], report
    assert report["nonfinite_pixels_inside_footprint"] == 0
    with rasterio.open(tif) as src:
        a = src.read(1)
    assert set(np.unique(a)) <= {0.0, 1.0}
    assert int((a == 1).sum()) == card["build"]["final_dots"]


def test_artefact_is_binary_and_never_a_raw_score():
    card = json.loads((ROOT / "evidence" / "run_card.json").read_text())
    with rasterio.open(ROOT / card["file"]) as src:
        a = src.read(1)
    assert a.min() >= 0.0 and a.max() <= 1.0
    assert len(np.unique(a)) == 2


def test_registry_hashes_and_counts_match_the_receipts():
    files = registry.registry_files()
    receipts = {r["site"]: r for r in registry.load_receipts()["sites"]}
    assert set(files) == set(registry.SITES)
    ref = grid.load_reference()
    for site, path in files.items():
        assert grid.sha256(path) == receipts[site]["sha256"]
        n = int(registry.dots(path, ref["footprint"]).sum())
        assert n == receipts[site]["dots_measured"], site


def test_run_card_never_claims_organizer_confirmation():
    card = json.loads((ROOT / "evidence" / "run_card.json").read_text())
    blob = json.dumps(card).lower()
    assert "organizer-confirmed" not in blob
    assert card["estimate"]["label"] == "MODEL-ESTIMATE (not a score)"


def test_sha256_quoted_in_the_docs_matches_the_artefact():
    """Guards against the documented hash drifting from the delivered file."""
    card = json.loads((ROOT / "evidence" / "run_card.json").read_text())
    sha = card["sha256"]
    assert grid.sha256(ROOT / card["file"]) == sha
    for name in ("README.md", "docs/submission.html"):
        text = (ROOT / name).read_text()
        assert sha in text, f"{name} does not quote the current artefact sha256"
        assert "6f9af709" not in text, f"{name} still quotes a superseded hash"
