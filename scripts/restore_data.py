#!/usr/bin/env python3
"""Restore all Korea7 inputs from hash-pinned GitHub mirrors (owner's own repos).

These are *mirrors*, not organizer-authenticated downloads: every file is
SHA-256-verified against the values below (which cross-match the manifests in
GEMSDOEkarage3 registry/data_manifest.json and data/restore_receipt.json), but
only a download from the DrivenData data page while logged in authenticates
origin. The original mirror repos (buffedlizard55-lab/GEMSDOE*) return HTTP
404 as of 2026-11-04, and the 419 MB 19-band training_features.tif parts they
hosted are not restoreable from any live repo found today (flagged IR-K7-02);
this lane deliberately uses only the files below.

Requires: gh (authenticated) OR network access to codeload.github.com.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K1 = "9e1cfa8b843c25c5dc8ce2358e0f340f65dad472"    # karagemop466-tech/GEMSDOEkarage1
K3 = "6b0d7cd64b06c7b694eeae70032afc761f869171"    # karagemop466-tech/GEMSDOEkarage3
KAN1 = "60abceb569d385f8d82c7ea2a07fb75617d1bb0f"  # kanlerxz87-cyber/KANLERGEMSDOE1

FILES = [
    # dest, repo, ref, path, sha256
    ("data/sample_submission.tif", "karagemop466-tech/GEMSDOEkarage3", K3, "docs/downloads/sample_submission.tif", "2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc"),
    ("data/labels.tif", "karagemop466-tech/GEMSDOEkarage3", K3, "docs/downloads/labels.tif", "7ba308ccdc4418b31a178f4f1ef21aaa6e152e4028f2f6f64b01f7eb25ae4093"),
    ("data/external/derived_sgmc_faults_100m_u8.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/external/derived_sgmc_faults_100m_u8.tif", "643cbe992ef4ba37588fb469163ed8291e3ceb23d6c1f78a3cfaa462430c2da0"),
    ("data/external/lidar_scarp_features_u8.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/external/lidar_scarp_features_u8.tif", "d580bb8bdcdb941e32fefb8b38044bc5bf04e199bf2e83498c3576e6fc465568"),
    ("data/external/geodawn_rad_u8.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/external/geodawn_rad_u8.tif", "c22420f75999030d7cc65c9e31e50d232ea6158423bca051613a18a8b20ba682"),
    ("data/external/geodawn_extensions_u8.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/external/geodawn_extensions_u8.tif", "a35a9c6d2a14786f4dab85481ee59769213072f5dab5b2535ea82ae4d9bb7d9b"),
    ("data/external/tiger_road_distance_m.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/external/tiger_road_distance_m.tif", "e5350423508968fa2d32b0a6ae0d3fb4ae3ea645e3b8736f0c8e7ad9ff2f2988"),
    ("registry/GEMSDOE24.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE24_gems24-h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan.tif", "68d0e2e4fcc594f9a23f56c44b885fee733d026d39be55e18ad2a07289525310"),
    ("registry/GEMSDOE25.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE25_d28.tif", "3e78737f0da8dd2ca66cc6caac0ce8eeefcd6715707f8d1bd3091845cd9bcc30"),
    ("registry/GEMSDOE27.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE27_gems27-topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan.tif", "33003374335d84bf885f2d8f5e9dd4c57044c8ec58fa6a0d7fa581e8bc41c11d"),
    ("registry/GEMSDOE28.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE28_gems28-h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan.tif", "5556aa1438fd67376b60d5ffc99228ec09dcc11a8408298a743ccb88d6163641"),
    ("registry/GEMSDOE30.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE30_gemsdoe30-d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca.tif", "8cf893ead5667df21d3288a9968c35fd5385c425b029d82ee71d311715b129fd"),
    ("registry/GEMSDOE31.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE31_gemsdoe31-h27-4-solo-d28-20261004-8acb75e1-nan.tif", "07b6db440535404bb41ec8ddc797713e200d308e3da35937393efde5eb84bc40"),
    ("registry/GEMSDOE32.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE32_B2.tif", "c55bafc470054e8271dcb89347a17e07fefe50de6af6e6ba6c4b169ef7ab6fa9"),
    ("registry/GEMSDOE33.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE33_GEMSDOE33-h33d-analog-tip-stepover-r30-20261004-cb490425926e.tif", "87f857d505e23247e991ccfab2cbe9f49a04df4f9c8028dce7ea261554690757"),
    ("registry/GEMSDOE36.tif", "karagemop466-tech/GEMSDOEkarage1", K1, "registry/GEMSDOE36_gemsdoe36-anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros.tif", "e15891020b9c57056ac7fa874a5e506fbd6ed9314a4ea8e73af0753887a3708a"),
    ("registry/LATTICE_WITNESS_r13.tif", "kanlerxz87-cyber/KANLERGEMSDOE1", KAN1, "data/scored/13gems_20261001_r13-lattice-s5_v2_nan-outside.tif", "b4570b406efec198eb2f4d142ad8d0d6184b14b66f2f52b5c4d697f0647dc9b2"),
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch(repo: str, ref: str, path: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    try:
        if shutil.which("gh"):
            with tmp.open("wb") as out:
                subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}?ref={ref}",
                                "-H", "Accept: application/vnd.github.raw"],
                               stdout=out, stderr=subprocess.PIPE, check=True)
        else:
            import tarfile
            import urllib.request
            url = f"https://codeload.github.com/{repo}/tar.gz/{ref}"
            with urllib.request.urlopen(url, timeout=300) as resp, \
                    tarfile.open(fileobj=resp, mode="r|gz") as tf:
                for m in tf:
                    if m.isfile() and "/" in m.name and m.name.split("/", 1)[1] == path:
                        with tmp.open("wb") as out:
                            shutil.copyfileobj(tf.extractfile(m), out, 1 << 20)
                        break
                else:
                    raise FileNotFoundError(path)
        tmp.replace(dest)
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    receipt = []
    for dest, repo, ref, path, want in FILES:
        d = ROOT / dest
        status = "present-verified"
        if not (d.exists() and sha256(d) == want):
            fetch(repo, ref, path, d)
            status = "restored"
            if sha256(d) != want:
                raise SystemExit(f"HASH MISMATCH {dest}: {sha256(d)} != {want}")
        receipt.append({"dest": dest, "repo": repo, "ref": ref, "path": path,
                        "sha256": want, "status": status})
        print(status, dest)
    out = {"verified_utc": "2026-11-04", "authentication": "owner GitHub mirrors, hash-pinned; NOT organizer-authenticated",
           "unavailable": [{"id": "training_features.tif (19-band, 418912844 bytes)",
                            "sha256": "4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5",
                            "reason": "host repos buffedlizard55-lab/* return HTTP 404 on 2026-11-04; no live mirror found. Organizer source: https://www.drivendata.org/competitions/306/competition-doe-gems/data/ (login required)"}],
           "files": receipt}
    (ROOT / "evidence/data_provenance.json").write_text(json.dumps(out, indent=2) + "\n")
    (ROOT / "registry/focus9_manifest.json").write_text(
        json.dumps([r for r in receipt if r["dest"].startswith("registry/")], indent=2) + "\n")
    print(f"{len(receipt)} files verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
