#!/usr/bin/env python3
"""Measure the nine focus-site rasters: ring census, lineage algebra, pairwise overlap.

Everything printed here is computed from the raster bytes in ``data/registry``.
Owner-reported scores are read from ``receipts.json`` and are labelled as such.
Writes ``evidence/registry_forensics.json``.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import grid, registry  # noqa: E402

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"


def main() -> int:
    ref = grid.load_reference()
    foot, cat = ref["footprint"], ref["catalogue"]
    files = registry.registry_files()
    receipts = {r["site"]: r for r in registry.load_receipts()["sites"]}

    dist = registry.distance_to_catalogue(cat)
    masks, rows = {}, []
    for site in registry.SITES:
        m = registry.dots(files[site], foot)
        masks[site] = m
        rec = receipts[site]
        row = {
            "site": site,
            "file": rec["file"],
            "sha256": rec["sha256"],
            "submission": rec["submission"],
            "owner_reported_score": rec["owner_reported_score"],
            "score_evidence_class": "owner-report",
            "source_url": rec["source_url"],
            **registry.catalogue_ring_census(m, dist),
        }
        row.update(registry.implied_coverage(rec["owner_reported_score"], row["dots"]))
        rows.append(row)
        print(f"{site}  dots={row['dots']:6d}  <=1px={row['le_1px']:6d}  <=2px={row['le_2px']:6d}  "
              f"<=3px={row['le_3px']:6d}  >3px={row['gt_3px']:6d}  score={rec['owner_reported_score']}")

    print("\n--- lineage algebra (exact dot-set relations) ---")
    pairs = registry.pairwise(masks)
    for key, v in pairs.items():
        if v["a_subset_of_b"] or v["b_subset_of_a"] or v["symmetric_difference"] == 0:
            print(f"  {key:22s} iou={v['iou']:.4f} symdiff={v['symmetric_difference']:6d} "
                  f"subset(a in b)={v['a_subset_of_b']} subset(b in a)={v['b_subset_of_a']}")

    # Does the champion equal the parent minus the <=2 px ring?
    cham, solo = masks["GEMSDOE32"], masks["GEMSDOE31"]
    predicted = solo & (dist > 2)
    print(f"\n  champion == GEMSDOE31 minus (dist<=2px)?  "
          f"symdiff={int((cham ^ predicted).sum())} (champion={int(cham.sum())}, rule={int(predicted.sum())})")
    d28 = masks["GEMSDOE25"]
    b1 = d28 & (dist > 1)
    print(f"  GEMSDOE31 == GEMSDOE25 minus (dist<=1px)?  "
          f"symdiff={int((solo ^ b1).sum())} ({int(solo.sum())} vs {int(b1.sum())})")
    pinn = masks["GEMSDOE36"]
    print(f"  GEMSDOE36 superset of champion?           "
          f"missing={int((cham & ~pinn).sum())} extra={int((pinn & ~cham).sum())}")

    print("\n--- worst-case pairwise overlap (lane gate is >70% within 3 px) ---")
    worst = max(pairs.items(), key=lambda kv: max(kv[1]["frac_a_within_3px_of_b"],
                                                  kv[1]["frac_b_within_3px_of_a"]))
    print(f"  max pairwise 3px overlap = {max(worst[1]['frac_a_within_3px_of_b'], worst[1]['frac_b_within_3px_of_a']):.4f} ({worst[0]})")

    print("\n--- metric algebra at the programme best ---")
    bar = registry.marginal_bar(0.2778)
    print(json.dumps(bar, indent=2))

    out = {
        "generated_utc": "2026-11-04",
        "grid": {
            "crs": grid.EXPECTED_CRS,
            "shape": [grid.EXPECTED_HEIGHT, grid.EXPECTED_WIDTH],
            "transform": list(grid.EXPECTED_TRANSFORM),
            "footprint_pixels": int(foot.sum()),
            "catalogue_pixels": int(cat.sum()),
        },
        "sites": rows,
        "pairwise": pairs,
        "lineage_checks": {
            "champion_equals_solo_minus_le2px_symdiff": int((cham ^ predicted).sum()),
            "champion_dots": int(cham.sum()),
            "solo_equals_d28_minus_le1px_symdiff": int((solo ^ b1).sum()),
            "pinn_minus_champion_dots": int((pinn & ~cham).sum()),
            "pinn_missing_champion_dots": int((cham & ~pinn).sum()),
        },
        "marginal_bar_at_0.2778": bar,
        "note": ("Owner-reported scores are not organiser-confirmed. Ring census uses Euclidean pixel "
                 "distance to the nearest catalogue fault pixel, 1 px = 100 m."),
    }
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "registry_forensics.json").write_text(json.dumps(out, indent=2) + "\n")
    print("\nwrote evidence/registry_forensics.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
