"""Shipped-artifact integrity: SHA256SUMS must match the files byte-for-byte,
and the run card must reference the shipped primary candidate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "docs" / "downloads"


def test_sha256sums_match_files():
    sums = (DL / "SHA256SUMS.txt").read_text().strip().splitlines()
    assert sums, "SHA256SUMS.txt is empty"
    for line in sums:
        digest, name = line.split()
        p = DL / name
        assert p.exists(), name
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        assert h == digest, f"hash mismatch for {name}"


def test_run_card_references_shipped_primary():
    card = json.loads((ROOT / "run-card.json").read_text())
    primary = card["holdout_dti"]["primary_candidate"]
    assert (DL / primary).exists()
    assert card["raster_sha256"]["primary_44090"] == hashlib.sha256(
        (DL / primary).read_bytes()).hexdigest()
    assert card["verdict"] in {"promote", "negative"}
    assert len(card["submission_note"]) <= 140


def test_evidence_receipts_present():
    ev = ROOT / "evidence"
    for f in ["exp1_canary.json", "final_lane_checks.json",
              "holdout_v2b_full.json", "holdout_v2a_full.json"]:
        assert (ev / f).exists(), f


def test_lane_checks_pass():
    d = json.loads((ROOT / "evidence" / "final_lane_checks.json").read_text())
    for tag, res in d["final_checks"].items():
        assert res["max_overlap"] <= 0.70, tag
        assert res["max_abs_spearman"] <= 0.90, tag
