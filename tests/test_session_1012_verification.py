"""Regression checks for the 2026-11-10 job-specific source audit."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dashboard_content as C  # noqa: E402
import ranking_data as R  # noqa: E402
import session_1012_verification as J  # noqa: E402


def test_added_candidate_is_separately_transcribed_and_officially_linked():
    record = J.EVIDENCE["additional_candidate"]
    assert record["license"] == "1034873"
    assert record["status"] == "current and active"
    assert set(record["classifications"]) == {"C36", "B"}
    assert record["business_phone"] == "(650) 868-8059"
    assert record["record_stamp"].startswith("Data current as of 11/9/2026")
    assert C.SOURCES["S205"]["tier"] == "official"
    assert C.SOURCES["S205"]["url"] == record["sources"]["license"]
    assert C.SOURCES["S212"]["url"] == record["sources"]["complaint_disclosure"]
    assert record["workers_compensation"]["expires"] == "2026-12-30"
    # The original score remains reproducible and was not silently extended.
    assert len(R.RECORDS) == 16
    assert record["license"] not in R.RECORDS


def test_unconfirmed_fields_are_null_or_flagged_not_invented():
    record = J.EVIDENCE["additional_candidate"]
    for key in ("official_website_verified", "san_francisco_service_confirmed_by_company",
                "trip_lever_experience_confirmed", "single_contract_ceiling_restoration_confirmed",
                "availability_confirmed", "job_price_confirmed"):
        assert record[key] is None
    row = C.TABLES["additional_contact_1012"]["rows"][0]
    assert C.BLANK in row["cells"][2]
    assert C.UNVERIFIED in row["cells"][2]
    assert C.SOURCES["S211"]["status"] == "dead"


def test_job_fit_priorities_link_cslb_and_do_not_claim_confirmed_prices():
    table = C.TABLES["job_fit_1012"]
    assert len(table["rows"]) == 5
    assert [re.search(r"(\d+) ·", row["cells"][0]).group(1) for row in table["rows"]] == ["1", "2", "3", "4", "5"]
    for row in table["rows"]:
        assert any(C.SOURCES[sid]["tier"] == "official" and
                   "LicNum=" in C.SOURCES[sid]["url"] for sid in row["src"])
        assert C.BLANK in row["cells"][4]
        assert C.UNVERIFIED in row["cells"][4]
    assert "not part of the original score" in table["rows"][2]["cells"][3]
    assert "No contractor" in table["caption"]
    assert "S155" in table["rows"][0]["src"]
    assert "citation" in table["rows"][0]["cells"][3]


def test_vendor_phone_discrepancy_and_review_sources_are_labeled():
    atlas = next(row for row in C.TABLES["contacts"]["rows"] if "Atlas Plumbing" in row["cells"][0])
    assert "(650) 871-9863" in atlas["cells"][1]
    assert "(415) 849-2346" in atlas["cells"][2]
    assert "differs" in atlas["cells"][4]
    assert {"S69", "S200"}.issubset(atlas["src"])
    assert C.SOURCES["S207"]["tier"] == "platform"
    assert C.SOURCES["S207"]["status"] == "blocked-403"
    assert C.SOURCES["S210"]["tier"] == "platform"
    assert "third-party" in C.SOURCES["S210"]["note"]
    assert "not independently" in C.SOURCES["S207"]["note"]


def test_incorrect_review_attributions_are_removed():
    reviews = json.loads((ROOT / "data/canonical/review_snapshots.json").read_text(encoding="utf-8"))
    ace = next(item for item in reviews["snapshots"] if item["license"] == "829071")
    heroes = next(item for item in reviews["snapshots"] if item["license"] == "1003394")
    assert "withdrawn" in ace["quote"]
    assert "Mikhail" not in heroes["quote"]
    assert "bathtub installed with a valve" not in R.REASON["829071"].lower()
    for row in C.TABLES["reviews_1108"]["rows"]:
        assert any(C.SOURCES[sid]["tier"] == "official" for sid in row["src"])
        assert "third-party" in " ".join(row["cells"]).lower()


def test_prior_disclosure_audit_and_flag_counts_remain_accurate():
    disclosure = C.TABLES["disclosure_check"]
    assert len(disclosure["rows"]) == 16
    assert "original scored" in disclosure["title"].lower()
    flags = C.TABLES["flagged"]["rows"]
    ids = [row["cells"][0] for row in flags]
    assert len(ids) == len(set(ids))
    assert all(any(C.SOURCES[sid]["tier"] == "official" for sid in row["src"])
               for row in flags[-3:])
    card = next(card for block in C.PAGES["index.html"]["sections"] if block["type"] == "cards"
                for card in block["items"] if card["k"] == "Flagged for review")
    assert int(card["v"]) == len(flags)


def test_pages_contain_job_fit_table_and_contact():
    assert any(block.get("ref") == "job_fit_1012" for block in C.PAGES["ranking.html"]["sections"])
    assert any(block.get("ref") == "additional_contact_1012" for block in C.PAGES["contacts.html"]["sections"])
    assert J.EVIDENCE["meta"]["outreach_performed"] is False
