"""Evidence completeness: the published site must be generated from complete, consistent JSON."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import estimate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"


def load(name):
    return json.loads((EV / name).read_text())


def test_every_experiment_artifact_exists():
    for name in ("registry_forensics.json", "holdout_experiment.json",
                 "experiment2_emission.json", "candidate_gates.json", "run_card.json",
                 "external_layers.json"):
        assert (EV / name).exists(), f"missing evidence/{name}"


def test_external_layer_receipt_pins_the_bytes_actually_used():
    layers = {r["layer"]: r for r in load("external_layers.json")["layers"]}
    used = layers["seis_n200a15"]
    assert used["covers_footprint_fraction"] == 1.0
    assert len(used["sha256_source_file"]) == 64
    assert "1391" in used["official_source"]
    assert used["upstream"] == "jklinck/geothermal_research"


def test_candidate_gates_are_all_recorded_and_fail_closed():
    gates = load("candidate_gates.json")
    assert set(gates) == {"G1_format", "G2_unique", "G3_holdout", "G4_beats_programme_best"}
    for name, g in gates.items():
        assert "pass" in g, name
    card = load("run_card.json")
    assert card["ok_to_submit"] == all(g["pass"] for g in gates.values())
    if not card["ok_to_submit"]:
        assert card["blocking_reason"]


def test_registry_forensics_covers_all_nine_sites_and_matches_the_model():
    forensics = load("registry_forensics.json")
    assert len(forensics["sites"]) == 9
    for row in forensics["sites"]:
        assert row["dots"] > 0
        assert row["le_1px"] <= row["le_2px"] <= row["le_3px"] <= row["dots"]
        c = estimate.implied_coverage(row["owner_reported_score"], row["dots"])
        assert 0.0 < c <= 1.0
        # every focus raster is within 3 px of a sister file
        assert row["max_overlap_vs_other_eight"] > 0.99


def test_the_champion_lineage_algebra_is_exact():
    checks = load("registry_forensics.json")["lineage_checks"]
    assert checks["champion_equals_solo_minus_le2px_symdiff"] == 0
    assert checks["solo_equals_d28_minus_le1px_symdiff"] == 0
    assert checks["pinn_missing_champion_dots"] == 0
    assert checks["pinn_minus_champion_dots"] == 1200


def test_holdout_experiment_is_labelled_and_has_cis():
    hold = load("holdout_experiment.json")
    assert hold["instrument"] == "K7-HIDE-RECOVER-1.0"
    for fold in hold["folds"]:
        for arm in fold["arms"].values():
            assert arm["ci95"] is not None
            assert arm["ci95"][0] <= arm["holdout_dti"] <= arm["ci95"][1]


def test_no_document_claims_an_organizer_confirmed_score():
    for f in list(EV.glob("*.json")) + list((ROOT / "docs").glob("*.html")):
        text = f.read_text().lower()
        assert "organizer-confirmed:" not in text, f
        assert "\"organizer_confirmed\": true" not in text, f
