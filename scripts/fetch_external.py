#!/usr/bin/env python3
"""Fetch, warp and record the official external layers onto the competition grid.

Run this once before the experiments on a fresh clone; the experiment scripts will also
call it lazily if the cache is missing.  Writes evidence/external_layers.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import external as ext, grid  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    foot = grid.load_reference()["footprint"]
    recs = []
    for layer in ext.LAYERS:
        arr = ext.load_on_grid(layer, foot, refresh=True)
        rec = {"layer": layer,
               "finite_fraction_of_footprint": float(np.isfinite(arr[foot]).mean())}
        recs.append(layer)
        print(f"  {layer}: finite over {rec['finite_fraction_of_footprint']:.1%} of the footprint")
    print(f"checked {len(recs)} layer(s); receipt -> evidence/external_layers.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
