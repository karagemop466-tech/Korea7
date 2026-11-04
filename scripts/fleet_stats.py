#!/usr/bin/env python3
"""Fleet-level statistics over the user-reported score ledger (160 rows).

Groups submission names by method tokens and reports n / median / max of the
USER-REPORTED values. This is descriptive statistics over the owner's ledger,
not organizer-confirmed data and not causal evidence: tokens co-occur and the
fleet is heavily confounded (same family re-emitted many times).
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TOKENS = {
    "dotted/poisson emission": r"dotted|poisson|pindrop|lattice",
    "off-catalogue gated": r"offcat|off-catalogue|offcatalogue",
    "submodular/coverage": r"submod|cover",
    "continuous ridge surface": r"ridge|surface|continuous",
    "lidar/scarp/dem scarp": r"lidar|scarp|dem10",
    "magnetic euler/tilt/worm": r"euler|tilt|worm|mag",
    "ml model (hgb/gbm/nn/pu)": r"hgb|gbm|unet|pinn|\bpu\b|ml-",
    "zeros outside": r"zeros|allfinite|zero$|-zero",
    "nan outside": r"nan",
    "budget 37-44k in name": r"37654|38854|44090|38k|40k|37k|36k",
    "budget >=80k/100k in name": r"80k|90k|100k|100000|150k|84262",
}


def main() -> int:
    rows = list(csv.DictReader((ROOT / "registry/owner_score_ledger.csv").open()))
    def is_float(s: str) -> bool:
        try:
            float(s); return True
        except ValueError:
            return False
    snapshots = [r for r in rows if r["evidence_class"] == "official-snapshot"]
    scored = [r for r in rows if is_float(r["score"]) and r["evidence_class"] == "user-report"]
    out = {"n_rows": len(rows), "n_scored": len(scored),
           "label": "USER-REPORTED (owner ledger; no organizer receipts)", "tokens": {}}
    for label, pat in TOKENS.items():
        hit = [float(r["score"]) for r in scored if re.search(pat, r["submission"], re.I)]
        miss = [float(r["score"]) for r in scored if not re.search(pat, r["submission"], re.I)]
        if hit:
            out["tokens"][label] = {
                "n": len(hit), "median": float(np.median(hit)), "max": float(np.max(hit)),
                "median_without_token": float(np.median(miss)) if miss else None}
    out["official_leaderboard_snapshots_in_ledger"] = [
        {"as_of": r["as_of_utc"], "what": r["submission"], "value": r["score"]} for r in snapshots]
    top = sorted(scored, key=lambda r: -float(r["score"]))[:15]
    out["top15"] = [{"site": r["site"], "submission": r["submission"],
                     "user_reported": float(r["score"])} for r in top]
    (ROOT / "evidence/fleet_stats.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
