"""Uniqueness screening against the nine GEMSDOE registry rasters.

Two tests, both required by the run protocol:

* **rank correlation** of the candidate's pre-placement surface against each
  registry surface (Spearman rho).  Above 0.90 means the *method* has drifted
  into another lane's logic, even if the dots differ.
* **dot overlap**: the share of the candidate's positive cells lying within
  3 Euclidean pixels of a registry raster's positives.  Above 0.70 means the
  *output* is a copy.

A missing or incomplete manifest is not evidence of uniqueness: the verdict is
``UNKNOWN`` and the submission is blocked.  Hashes are recorded so a later run
can prove which file was screened.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import rankdata

REQUIRED_SITES = ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28",
                  "GEMSDOE30", "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36")
RHO_LIMIT = 0.90
OVERLAP_LIMIT = 0.70
OVERLAP_PX = 3.0


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def spearman(a, b):
    x, y = rankdata(a), rankdata(b)
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        raise ValueError("rank correlation undefined for a constant surface")
    return float(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy))


def _read(path, grid=None):
    with rasterio.open(path) as s:
        if s.count != 1:
            raise ValueError(f"{path}: expected one band, found {s.count}")
        spec = (s.crs.to_epsg() if s.crs else None, s.width, s.height,
                tuple(s.transform)[:6])
        if grid is not None and spec != grid:
            raise ValueError(f"{path}: CRS/shape/transform does not match the candidate")
        return s.read(1).astype(np.float32), spec


def screen(candidate, surface=None, manifest=None):
    """Screen a candidate against the registry manifest.

    Returns a report with status PASS (unique enough), BLOCKED (threshold
    breach) or UNKNOWN (no usable manifest).  Never returns 'approved'.
    """
    rep = {"candidate": str(candidate), "status": "UNKNOWN", "comparisons": [],
           "limits": {"rho": RHO_LIMIT, "overlap": OVERLAP_LIMIT,
                      "overlap_px": OVERLAP_PX},
           "errors": [],
           "notice": ("Uniqueness against the supplied registry only. Registry "
                      "completeness cannot be proven here.")}
    try:
        rep["candidate_sha256"] = sha256(candidate)
        cand, grid = _read(candidate)
        if not np.isin(cand, [0.0, 1.0]).all():
            raise ValueError("candidate is not binary; dot overlap is undefined")
        dots = cand == 1
        if not dots.any():
            raise ValueError("candidate has no positive cells")
        surf = cand if surface is None else _read(surface, grid)[0]
        if not np.isfinite(surf).all() or np.ptp(surf) == 0:
            raise ValueError("candidate surface is non-finite or constant")
        if manifest is None:
            rep["errors"].append("no registry manifest supplied: uniqueness is UNKNOWN")
            return rep
        items = json.loads(Path(manifest).read_text())
        if not isinstance(items, list) or not items:
            raise ValueError("manifest must be a non-empty JSON array")
        sites = {i.get("site") for i in items}
        missing = [s for s in REQUIRED_SITES if s not in sites]
        base = Path(manifest).resolve().parent
        worst = {"rho": 0.0, "overlap": 0.0}
        for item in items:
            sp, dp = base / item["surface"], base / item["dots"]
            if sha256(sp) != item["surface_sha256"] or sha256(dp) != item["dots_sha256"]:
                raise ValueError(f"{item['site']}: registry hash mismatch")
            rs = _read(sp, grid)[0]
            rd = _read(dp, grid)[0]
            refd = rd == 1
            if not refd.any():
                raise ValueError(f"{item['site']}: registry dots are empty")
            rho = spearman(surf, rs)
            overlap = float((distance_transform_edt(~refd)[dots] <= OVERLAP_PX).mean())
            worst["rho"] = max(worst["rho"], abs(rho))
            worst["overlap"] = max(worst["overlap"], overlap)
            rep["comparisons"].append({"site": item["site"], "spearman_rho": round(rho, 4),
                                       "dot_overlap_3px": round(overlap, 4),
                                       "duplicate": bool(abs(rho) > RHO_LIMIT
                                                         or overlap > OVERLAP_LIMIT)})
        rep["missing_sites"] = missing
        if any(c["duplicate"] for c in rep["comparisons"]):
            rep["status"] = "BLOCKED"
            rep["errors"].append("duplicate/lane-drift threshold exceeded")
        elif missing:
            rep["status"] = "UNKNOWN"
            rep["errors"].append(f"registry incomplete: missing {missing}")
        else:
            rep["status"] = "PASS"
        rep["worst"] = worst
    except Exception as exc:                      # noqa: BLE001
        rep["errors"].append(f"{type(exc).__name__}: {exc}")
        rep["status"] = "BLOCKED"
    return rep


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Screen a candidate against the GEMSDOE registry")
    p.add_argument("--candidate", required=True)
    p.add_argument("--surface", help="pre-placement score surface (defaults to candidate)")
    p.add_argument("--manifest", help="JSON array of registry entries")
    p.add_argument("--out")
    args = p.parse_args(argv)
    rep = screen(args.candidate, args.surface, args.manifest)
    text = json.dumps(rep, indent=2, allow_nan=False, default=str)
    if args.out:
        Path(args.out).write_text(text)
    print(text)
    return 0 if rep["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
