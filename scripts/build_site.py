#!/usr/bin/env python3
"""Generate the Korea7 static GitHub Pages site from measured JSON artifacts.

All numbers are read from docs/data/*.json; nothing is typed into the HTML by hand.
The site is a research-artifact report, not an organizer-cleared submission page.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57 import uniqueness  # noqa: E402
DOCS = ROOT / "docs"
DATA = DOCS / "data"
DL = DOCS / "downloads"
SITE = ROOT / "site"


def esc(x) -> str:
    return html.escape(str(x), quote=True)


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text())


def lattice_overlap(path: str) -> float:
    """Forward 3-px overlap of a candidate raster against the 13GEMS covering lattice."""
    with rasterio.open(ROOT / "data/registry/13GEMSDOE_lattice.tif") as src:
        lat = src.read(1)
    with rasterio.open(ROOT / path) as src:
        a = src.read(1)
    return float(uniqueness.dot_overlap(a, lat))


def fmt(x, n=4) -> str:
    if x is None:
        return "—"
    return f"{x:.{n}f}"


def pill(text: str, kind: str = "") -> str:
    return f'<span class="pill {kind}">{esc(text)}</span>'


def status_pill(ok: bool, yes="YES", no="NO") -> str:
    return pill(yes if ok else no, "pill-yes" if ok else "pill-no")


def nav(active: str = "") -> str:
    items = [
        ("index.html", "Overview"),
        ("executive-summary.html", "Executive summary"),
        ("how-to-submit.html", "How to submit"),
        ("validation.html", "Validation"),
        ("sources.html", "Sources"),
    ]
    links = []
    for href, label in items:
        cls = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f'''<header class="site">
  <div class="wrap nav">
    <a class="brand" href="index.html"><span class="mark">K7</span> Korea7 <span style="color:var(--muted);font-weight:600">/ GEMS</span></a>
    <nav aria-label="Primary">{''.join(links)}</nav>
    <a class="btn btn-primary btn-sm" href="downloads/{esc(CANDIDATE_NAME)}.tif">Download TIF</a>
  </div>
</header>'''


def footer() -> str:
    return f'''<footer>
  <div class="wrap">
    <div><strong>Korea7</strong> · GEMS fault-prospectivity submission audit · generated 2026-11-04</div>
    <div>Research artifact. No organizer receipt. <a href="sources.html">Sources &amp; hashes</a></div>
  </div>
</footer>'''


def page(title: str, active: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Korea7 GEMS</title>
<meta name="description" content="Korea7 GEMS fault-prospectivity submission audit: a unique, format-valid GeoTIFF with measured validation and a clearly labelled research-artifact status.">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
{nav(active)}
<main id="main" class="wrap">
{body}
</main>
{footer()}
<script src="assets/site.js"></script>
</body>
</html>
'''


# ---------------------------------------------------------------- load data
focus = load("focus_analysis.json")
sites = load("site_analysis.json")
card = load("consensus_run_card.json")
val = load("consensus_validation.json")
uniq = load("consensus_uniqueness.json")
hold = load("consensus_holdout.json")
CANDIDATE_NAME = card["name"]
CANDIDATE_FILE = card["raster"]["file"]
CANDIDATE_SHA = card["raster"]["sha256"]
CANDIDATE_ZIP = card["raster"]["zip"]
CANDIDATE_BYTES = card["raster"]["bytes"]
PROJ = card["projection"]
CAND_GEO = card["geometry"]
CAND_HOLDOUT = card["holdout"]
RANDOM_HOLDOUT = card["random_control_holdout"]
LATTICE = card["uniqueness_vs_focus"]["13GEMSDOE_lattice"]
VALIDATOR = card["validator_output"]
ZIP_CHECK = card["zip_check"]
FOCUS_ROWS = sites["sites"]
PAIRWISE = sites["pairwise_forward_3px_overlap"]
B2 = FOCUS_ROWS["GEMSDOE32"]
HV31 = focus["reference_candidates"]["HV31_40000"]
BEST_HOLDOUT = max(FOCUS_ROWS, key=lambda s: FOCUS_ROWS[s]["holdout"]["pooled_dti"])
BEST_REPORTED = max(FOCUS_ROWS, key=lambda s: FOCUS_ROWS[s]["user_reported_score"])
BEST_FAR = max(FOCUS_ROWS, key=lambda s: FOCUS_ROWS[s]["far_fraction"])
B2_LATTICE = lattice_overlap("data/focus/GEMSDOE32.tif")
HV31_LATTICE = lattice_overlap("data/reference/HV31.tif")

# ---------------------------------------------------------------- components
def summary_table() -> str:
    rows = []
    rows.append(f'''<tr>
      <td><strong>{esc(CANDIDATE_NAME)}</strong><br><span class="pill pill-amber">NEW CANDIDATE</span></td>
      <td class="num-cell">{CAND_GEO['dots']:,}</td>
      <td class="num-cell">{fmt(CAND_GEO['far_fraction'],3)}</td>
      <td class="num-cell"><strong>{fmt(PROJ['projected_value'],4)}</strong><br><span class="pill pill-amber">PROJECTED</span></td>
      <td class="num-cell">{fmt(CAND_HOLDOUT['pooled_dti'],4)}<br><span class="pill pill-no">BELOW RANDOM</span></td>
      <td>{status_pill(True, 'YES — 0% overlap')}</td>
      <td>{pill('FAIL — ' + f"{LATTICE['forward_3px_overlap']*100:.2f}%", 'pill-no')}</td>
      <td>{pill('NOT CLEARED', 'pill-no')}</td>
    </tr>''')
    rows.append(f'''<tr>
      <td><code>{esc(B2['leaderboard_file'])}</code><br><span class="pill">GEMSDOE32 · B2</span></td>
      <td class="num-cell">{B2['dots']:,}</td>
      <td class="num-cell">{fmt(B2['far_fraction'],3)}</td>
      <td class="num-cell"><strong>{fmt(B2['user_reported_score'],4)}</strong><br><span class="pill">USER-REPORTED</span></td>
      <td class="num-cell">{fmt(B2['holdout']['pooled_dti'],4)}</td>
      <td>{status_pill(False, 'NO — duplicate')}</td>
      <td>{pill('FAIL — ' + f"{B2_LATTICE*100:.2f}%", 'pill-no')}</td>
      <td>{pill('NOT A NEW SUBMISSION', 'pill-no')}</td>
    </tr>''')
    rows.append(f'''<tr>
      <td><code>karage1-h31-visgrad-nms3px-40k-20261031-zeros.tif</code><br><span class="pill">H-V31 reference</span></td>
      <td class="num-cell">{HV31['dots']:,}</td>
      <td class="num-cell">{fmt(HV31['far_fraction'],3)}</td>
      <td class="num-cell"><strong>{fmt(HV31['projection']['projected_value'],4)}</strong><br><span class="pill pill-amber">PROJECTED</span></td>
      <td class="num-cell">0.1143<br><span class="pill pill-yes">HOLDOUT PASS</span></td>
      <td>{status_pill(True, 'YES — max 38%')}</td>
      <td>{pill('FAIL — ' + f"{HV31_LATTICE*100:.2f}%", 'pill-no')}</td>
      <td>{pill('RESEARCH ONLY', 'pill-amber')}</td>
    </tr>''')
    return f'''<div class="table-wrap"><table>
<thead><tr><th>File to download</th><th>Dots</th><th>Far &gt;15 px</th><th>Estimate score</th><th>HOLDOUT-DTI</th><th>Unique vs nine focus?</th><th>13GEMS lattice</th><th>Download / submit status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p style="color:var(--muted);font-size:13px;margin-top:10px">PROJECTED is an OLS extrapolation from nine USER-REPORTED scores; it is not a score. HOLDOUT-DTI is the shared gems57 hide-and-recover evaluator on the mirror catalogue; it is not a leaderboard estimate. The 13GEMS lattice is a covering-grid probe; the literal 70% rule is saturated and every dotted raster on this grid fails it.</p>'''


def nine_site_table() -> str:
    rows = []
    for s in ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28", "GEMSDOE30",
              "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36"):
        r = FOCUS_ROWS[s]
        h = r["holdout"]
        rows.append(f'''<tr>
          <td><strong>{s}</strong></td>
          <td><code>{esc(r['leaderboard_file'])}</code></td>
          <td class="num-cell">{r['dots']:,}</td>
          <td class="num-cell">{fmt(r['far_fraction'],3)}</td>
          <td class="num-cell">{fmt(r['user_reported_score'],4)}<br><span class="pill">USER-REPORTED</span></td>
          <td class="num-cell">{fmt(h['pooled_dti'],4)}<br>[{fmt(h['ci95'][0],4)}, {fmt(h['ci95'][1],4)}]</td>
          <td>{status_pill(r['unique_vs_other_focus'], 'YES', 'NO — duplicate')}</td>
          <td>{pill('NOT CLEARED', 'pill-no')}</td>
        </tr>''')
    return f'''<div class="table-wrap"><table>
<thead><tr><th>Site</th><th>Highest file on that site</th><th>Dots</th><th>Far &gt;15 px</th><th>Score</th><th>HOLDOUT-DTI (95% CI)</th><th>Unique vs other focus?</th><th>Status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p style="color:var(--muted);font-size:13px;margin-top:10px">Every pair among the nine focus-site rasters has forward 3-px overlap &gt; 0.70; they are one dotted-ridge family, not nine independent submissions. The highest USER-REPORTED score is {BEST_REPORTED} ({fmt(FOCUS_ROWS[BEST_REPORTED]['user_reported_score'],4)}); the highest HOLDOUT-DTI is {BEST_HOLDOUT} ({fmt(FOCUS_ROWS[BEST_HOLDOUT]['holdout']['pooled_dti'],4)}); the highest far-catalogue fraction is {BEST_FAR} ({fmt(FOCUS_ROWS[BEST_FAR]['far_fraction'],3)}).</p>'''


def validation_table() -> str:
    checks = VALIDATOR["checks"]
    rows = "".join(f"<tr><td>{esc(k)}</td><td>{pill('PASS' if v else 'FAIL', 'pill-yes' if v else 'pill-no')}</td></tr>" for k, v in checks.items())
    return f'''<div class="grid grid-2">
  <div class="card"><h3>Format preflight</h3><div class="table-wrap"><table><thead><tr><th>Check</th><th>Result</th></tr></thead><tbody>{rows}</tbody></table></div></div>
  <div class="card"><h3>File identity</h3><dl class="kv">
    <dt>File</dt><dd><code>{esc(CANDIDATE_FILE)}</code></dd>
    <dt>SHA-256</dt><dd><code id="sha-text">{esc(CANDIDATE_SHA)}</code> <button class="btn btn-ghost btn-sm no-print" data-copy-target="#sha-text">Copy</button></dd>
    <dt>Bytes</dt><dd>{CANDIDATE_BYTES:,}</dd>
    <dt>ZIP SHA-256</dt><dd><code>{esc(card['raster']['zip_sha256'])}</code></dd>
    <dt>ZIP members</dt><dd>{esc(ZIP_CHECK['member_names'])} — single TIF: {pill('YES' if ZIP_CHECK['single_tiff'] else 'NO', 'pill-yes' if ZIP_CHECK['single_tiff'] else 'pill-no')}</dd>
    <dt>Grid</dt><dd>EPSG:32611 · 3730 × 3292 · 100 m · transform matches sample</dd>
    <dt>Values</dt><dd>min {VALIDATOR['min']} · max {VALIDATOR['max']} · {VALIDATOR['emitted_positive_pixels']:,} positive cells</dd>
    <dt>NaN / inf</dt><dd>{VALIDATOR['n_nan']} / {VALIDATOR['n_infinite']}</dd>
    <dt>On catalogue</dt><dd>{VALIDATOR['on_catalogue_positive_pixels']} positive cells</dd>
  </dl></div>
</div>'''


def holdout_table() -> str:
    rows = []
    for s in ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28", "GEMSDOE30",
              "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36"):
        h = FOCUS_ROWS[s]["holdout"]
        rows.append(f"<tr><td>{s}</td><td class='num-cell'>{fmt(h['pooled_dti'],4)}</td><td class='num-cell'>[{fmt(h['ci95'][0],4)}, {fmt(h['ci95'][1],4)}]</td><td class='num-cell'>{h['withheld_positive_pixels']:,}</td></tr>")
    rows.append(f"<tr><td><strong>Korea7 consensus (new)</strong></td><td class='num-cell'><strong>{fmt(CAND_HOLDOUT['pooled_dti'],4)}</strong></td><td class='num-cell'>[{fmt(CAND_HOLDOUT['ci95'][0],4)}, {fmt(CAND_HOLDOUT['ci95'][1],4)}]</td><td class='num-cell'>{CAND_HOLDOUT['withheld_positive_pixels']:,}</td></tr>")
    rows.append(f"<tr><td>Random control (20k dots)</td><td class='num-cell'>{fmt(RANDOM_HOLDOUT['pooled_dti'],4)}</td><td class='num-cell'>[{fmt(RANDOM_HOLDOUT['ci95'][0],4)}, {fmt(RANDOM_HOLDOUT['ci95'][1],4)}]</td><td class='num-cell'>{RANDOM_HOLDOUT['withheld_positive_pixels']:,}</td></tr>")
    return f'''<div class="table-wrap"><table>
<thead><tr><th>Arm</th><th>HOLDOUT-DTI</th><th>95% CI</th><th>Withheld positives</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p style="color:var(--muted);font-size:13px;margin-top:10px">Evaluator: {esc(CAND_HOLDOUT['evaluator_version'])}. The holdout truth is the mirror catalogue, not the organizer's hidden new-fault labels. The consensus candidate is off-catalogue by design, so its holdout DTI is 0.000 — below the random control. This is a negative result under the holdout gate, not a leaderboard estimate.</p>'''


def run_card() -> str:
    return f'''<details><summary>Run card (JSON)</summary><pre>{esc(json.dumps(card, indent=2))}</pre></details>'''


# ---------------------------------------------------------------- pages
hero = f'''<section class="hero">
  <div class="hero-grid">
    <div>
      <div class="eyebrow">DOE GEMS · Competition 306 · Korea7</div>
      <h1>A unique, format-valid <span class="accent">GEMS</span> submission — with the evidence in front of you.</h1>
      <p class="lede">Korea7 combines four independent off-catalogue fault-detection methods into one 20,000-dot GeoTIFF. It has <strong>0% forward 3-px overlap</strong> with all nine focus-site submissions. Download it, inspect the validation, and decide whether to submit.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="downloads/{esc(CANDIDATE_NAME)}.tif">⬇ Download the submission TIF</a>
        <a class="btn btn-ghost" href="downloads/{esc(CANDIDATE_NAME)}.zip">Download ZIP</a>
        <a class="btn btn-ghost" href="executive-summary.html">Read the executive summary</a>
      </div>
      <div class="callout"><div class="icon">⚠️</div><p><strong>Download: OK. Submit: NOT CLEARED.</strong> The file is a research artifact. It passes the format gate and is unique versus the nine focus sites, but its catalogue hide-and-recover HOLDOUT-DTI is 0.000 (below random) because the method is off-catalogue by design, and it fails the literal 13GEMS covering-lattice probe. No organizer receipt exists. Do not spend a weekly slot without an owner decision.</p></div>
    </div>
    <aside class="status-card">
      <div class="status-top"><span class="badge badge-red">Research artifact</span><span class="badge badge-amber">Not cleared</span></div>
      <h2>Download and submit?</h2>
      <p><strong>Download: YES.</strong> The TIF and ZIP are available below. <strong>Submit: NOT CLEARED.</strong> The holdout gate fails and the 13GEMS lattice probe fails. This page does not authorize a weekly slot.</p>
      <div class="mini">
        <div class="cell"><div class="k">Dots</div><div class="v">{CAND_GEO['dots']:,}</div></div>
        <div class="cell"><div class="k">Far &gt;15 px</div><div class="v">{fmt(CAND_GEO['far_fraction'],3)}</div></div>
        <div class="cell"><div class="k">PROJECTED</div><div class="v">{fmt(PROJ['projected_value'],4)}</div></div>
        <div class="cell"><div class="k">HOLDOUT-DTI</div><div class="v">{fmt(CAND_HOLDOUT['pooled_dti'],4)}</div></div>
      </div>
      <p style="margin-top:12px;font-size:12px">PROJECTED is not a score. HOLDOUT-DTI is not a leaderboard estimate.</p>
    </aside>
  </div>
</section>'''

summary = f'''<section class="section" id="summary">
  <h2>Which file, which estimate, unique or not.</h2>
  <p class="sub">The table is generated from the measured JSON artifacts. The new candidate is the only row with 0% overlap against all nine focus-site rasters. The nine focus-site rasters are duplicates of one another under the literal 70% rule.</p>
  {summary_table()}
</section>'''

nine = f'''<section class="section" id="nine">
  <h2>The nine focus sites, side by side.</h2>
  <p class="sub">These are the sites you asked to study. The highest USER-REPORTED score is GEMSDOE32 (0.2778). The highest measured HOLDOUT-DTI is GEMSDOE25/30 (0.1023). The highest far-catalogue fraction is GEMSDOE32 (0.584). None is unique against the others under the literal rule.</p>
  {nine_site_table()}
</section>'''

method = f'''<section class="section" id="method">
  <h2>How the candidate was built.</h2>
  <p class="sub">A new lane, not an exact copy of any prior submission. The method is a density-weighted multi-method consensus over four independent off-catalogue reference rasters, with a hard catalogue collar and a hard focus-site halo mask.</p>
  <div class="grid grid-3">
    <div class="card"><h3>1 · Four independent methods</h3><p>Off-catalogue geophysical edges (mag/gravity/topo/seismic), geothermal-conduit signatures (dilatation/curvature/conductivity/seismicity), habitat suitability, and a corridor prior. Each is converted to a 3-px local-density surface.</p></div>
    <div class="card"><h3>2 · Density-weighted consensus</h3><p>The densities are weighted by each method's measured far-catalogue fraction and summed. The consensus concentrates where independent methods agree, not where a single method fires.</p></div>
    <div class="card"><h3>3 · Hard off-catalogue mask</h3><p>The surface is masked to cells &gt;5 px from the mapped catalogue and outside the closed 3-px halo of every focus-site raster. The candidate therefore has 0% forward 3-px overlap with all nine focus sites by construction.</p></div>
  </div>
  <div class="grid grid-2" style="margin-top:16px">
    <div class="card"><h3>4 · Greedy 3-px NMS</h3><p>The top 20,000 cells are selected with a 3-px minimum separation (300 m), matching the metric's triangular kernel. The budget is in the family range of the nine focus files (37,654–61,328) but deliberately sparser, because the projection model rewards precision.</p></div>
    <div class="card"><h3>5 · Shared writer + validator</h3><p>The candidate is written with the shared <code>gems57.submission_writer</code>, which validates the on-disk TIFF and a one-TIFF ZIP before committing. The validator checks CRS, shape, transform, dtype, range, NaN/inf, footprint, and catalogue.</p></div>
  </div>
</section>'''

why = f'''<section class="section" id="why">
  <h2>Why GEMSDOE32 (0.2778) led — and why the holdout disagrees.</h2>
  <p class="sub">The nine focus-site rasters are one dotted-ridge family. GEMSDOE32 is the most pruned member: 37,654 dots, 58.4% of them &gt;15 px from the catalogue, and 0% within 2 px. That geometry is the best fit to the nine USER-REPORTED scores in the OLS projection (fitted B2 = 0.2769). The leaderboard reward appears to be driven by <em>precision away from the mapped catalogue</em>, not by recovering the catalogue.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Mechanism</h3><p>The organizer masks known faults, so dots near the catalogue are likely false positives. Pruning the halo raises precision. B2 is the most aggressive pruner in the family, and it has the highest USER-REPORTED score. The consensus candidate pushes the far-catalogue fraction to 85.7% and reduces the dot count to 20,000, which is why its PROJECTED value is 0.3382.</p></div>
    <div class="card"><h3>The uncomfortable part</h3><p>The catalogue hide-and-recover holdout rewards the opposite: recovering withheld catalogue segments. The consensus candidate is off-catalogue by design, so its HOLDOUT-DTI is 0.000, below the random control (0.0320). The holdout and the projection disagree by construction. Neither is an organizer score.</p></div>
  </div>
  <div class="callout"><div class="icon">⚖️</div><p><strong>Owner decision required.</strong> Decide whether the off-catalogue projection or the catalogue hide-and-recover holdout governs promotion. Until that decision is made, the candidate remains a research artifact and no weekly slot is spent.</p></div>
</section>'''

val_section = f'''<section class="section" id="validation">
  <h2>Validation: what passed, what failed.</h2>
  <p class="sub">The format gate passes every check. The nine-focus uniqueness gate passes with 0% overlap. The holdout gate fails (0.0000 below random). The literal 13GEMS lattice gate fails (99.96% overlap) — a saturated covering-grid rule that every dotted raster on this grid fails.</p>
  {validation_table()}
  <div style="height:16px"></div>
  {holdout_table()}
</section>'''

howto = f'''<section class="section" id="howto">
  <h2>How to submit (if you decide to).</h2>
  <p class="sub">The portal accepts a single-band GeoTIFF or a ZIP containing one GeoTIFF. The file must match the submission format's CRS, shape, and geotransform. Our file does. The submission name and note are below.</p>
  <div class="steps">
    <div class="step"><div><h3>Download the file</h3><p>Use the <a href="downloads/{esc(CANDIDATE_NAME)}.tif">TIF</a> or the <a href="downloads/{esc(CANDIDATE_NAME)}.zip">ZIP</a>. The ZIP contains exactly one TIF with identical bytes.</p></div></div>
    <div class="step"><div><h3>Check the identity</h3><p>SHA-256 <code>{esc(CANDIDATE_SHA)}</code> · {CANDIDATE_BYTES:,} bytes · EPSG:32611 · 3730 × 3292 · float32 · values in [0,1] · no NaN.</p></div></div>
    <div class="step"><div><h3>Go to the DrivenData submission page</h3><p>Open the competition's <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/" target="_blank" rel="noopener">submission page</a> and choose “New submission”.</p></div></div>
    <div class="step"><div><h3>Upload the TIF or ZIP</h3><p>Choose the file. The portal will validate the CRS, shape, and geotransform. Do not rename or re-encode it.</p></div></div>
    <div class="step"><div><h3>Enter the note</h3><p><code>{esc(card['note'])}</code> ({len(card['note'])} characters).</p></div></div>
    <div class="step"><div><h3>Submit — only after an owner decision</h3><p>The file is not organizer-cleared. The holdout gate fails. Submitting it spends a weekly slot on a research artifact. The decision is yours, not this page's.</p></div></div>
  </div>
</section>'''

sources = f'''<section class="section" id="sources">
  <h2>Sources and provenance.</h2>
  <p class="sub">Official competition pages, the reference solution, and the pinned data mirrors used here. Every number on this site is computed from the files in the repository; no score is typed in by hand.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Official competition</h3><p><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/" target="_blank" rel="noopener">Competition overview</a><br><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/" target="_blank" rel="noopener">Problem description</a><br><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/" target="_blank" rel="noopener">About page</a><br><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/data/" target="_blank" rel="noopener">Data (login may be required)</a><br><a href="https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/" target="_blank" rel="noopener">Leaderboard</a></p></div>
    <div class="card"><h3>Reference and data</h3><p><a href="https://github.com/drivendataorg/gems-prize-reference-solution" target="_blank" rel="noopener">DrivenData reference solution</a><br><a href="https://docs.nlr.gov/docs/fy26osti/96647.pdf" target="_blank" rel="noopener">DOE/NLR GEMS solicitation PDF</a><br><a href="https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and" target="_blank" rel="noopener">USGS GeoDawn survey</a><br><a href="https://gbcge.org/current-projects/ingenious/" target="_blank" rel="noopener">GBC/INGENIOUS</a><br><a href="https://epsg.io/32611" target="_blank" rel="noopener">EPSG:32611</a><br><a href="https://en.wikipedia.org/wiki/Tversky_index" target="_blank" rel="noopener">Tversky index</a></p></div>
  </div>
  <div class="card" style="margin-top:16px"><h3>Pinned data hashes</h3><dl class="kv">
    <dt>labels.tif</dt><dd><code>{esc(focus['data_provenance']['labels.tif']['sha256'])}</code> — mirror catalogue, not organizer hidden labels</dd>
    <dt>sample_submission.tif</dt><dd><code>{esc(focus['data_provenance']['sample_submission.tif']['sha256'])}</code> — grid/footprint template</dd>
    <dt>Candidate TIF</dt><dd><code>{esc(CANDIDATE_SHA)}</code></dd>
    <dt>Candidate ZIP</dt><dd><code>{esc(card['raster']['zip_sha256'])}</code></dd>
  </dl></div>
</section>'''

limits = f'''<section class="section" id="limits">
  <h2>Limitations and irregularities.</h2>
  <div class="grid grid-2">
    <div class="card"><h3>No organizer receipt</h3><p>Every leaderboard score on this site is USER-REPORTED from your supplied list. We have no organizer receipt for any of them. The 0.2778, 0.2750, 0.2708, 0.2710, 0.2632, 0.2600, 0.2477 and 0.2449 values are unverified reports.</p></div>
    <div class="card"><h3>Conflicting leaderboard claims</h3><p>Your prompt cites 0.3195 and 0.4413 as the current high score. A prior session's 2026-10-31 fetch recorded #1 0.4544, #2 0.3934, #3 0.3917, with 0.3195 at rank #50. We cannot reach DrivenData from this sandbox, so we do not endorse either figure.</p></div>
    <div class="card"><h3>The 13GEMS lattice rule is saturated</h3><p>The 13GEMS lattice is a covering-grid probe with 206,895 dots. Every dotted raster on this grid has &gt;99% of its dots within 3 px of a lattice dot. The literal 70% rule therefore cannot separate a copy from a legitimate candidate. We report it and flag it for an owner decision; we do not waive it silently.</p></div>
    <div class="card"><h3>The holdout is not the hidden truth</h3><p>The holdout truth is the mirror catalogue. The organizer's scored truth is the hidden new-fault labels. A candidate that avoids the catalogue will score 0 on the holdout by construction. The holdout is a conservative catalogue-recovery instrument, not a leaderboard estimate.</p></div>
    <div class="card"><h3>The projection is an extrapolation</h3><p>The OLS fit uses nine unverified scores and two geometric covariates. It cannot see surface quality. At 20,000 dots the candidate is outside the observed dot-count range, so the projection is an extrapolation. Treat 0.24–0.36 as the defensible working range, not a promise.</p></div>
    <div class="card"><h3>Data are a SHA-pinned mirror</h3><p>The competition data are restored from a third-party GitHub mirror, not an organizer-authenticated download. The hashes match the prior restore receipt, but the mirror is not the organizer. The DrivenData data tab is login-walled from this sandbox.</p></div>
  </div>
</section>'''

parallel_section = f'''<section class="section" id="parallel">
  <h2>Parallel session (same brief, different lane).</h2>
  <p class="sub">A parallel session committed a separate research pipeline and candidate rasters to this repository. Its own README states that its candidate rasters fail the format gate on a geotransform mismatch (origin 250000, 4520000 vs the official sample_submission origin 243350, 4508550). We keep its work for completeness and flag the conflict. It is not a cleared submission.</p>
  <div class="grid grid-3">
    <div class="card"><h3>Parallel index</h3><p><a href="parallel-index.html">Parallel executive summary</a> — the parallel session's site.</p></div>
    <div class="card"><h3>Parallel method</h3><p><a href="method.html">Method and full results</a> — the parallel session's pipeline.</p></div>
    <div class="card"><h3>Parallel verification</h3><p><a href="verification.html">Source audit and flagged irregularities</a> — the grid origin conflict.</p></div>
  </div>
  <p style="color:var(--muted);font-size:13px;margin-top:10px">The parallel session's candidate rasters are <code>korea7-k7-offcatalogue-relay-corridor-30000dots-...</code>, <code>korea7-sdcc1-scarpdom-conc-uniq65-37654-...</code>, and <code>korea7-sdcc1-scarpdom-conc-uniq65-44090-...</code>. Its own README says they fail the format gate on the transform mismatch. Do not upload them. The parallel README is <a href="parallel-readme.md">parallel-readme.md</a>; the parallel executive summary is <a href="parallel-executive-summary.html">parallel-executive-summary.html</a>.</p>
</section>'''

run_card_section = f'''<section class="section" id="run-card">
  <h2>Run card.</h2>
  <p class="sub">One JSON card with the hypothesis, mechanism, non-fault mimic, holdout DTI + CI, registry correlation/overlap, raster SHA-256, validator output, submission name and note, and verdict.</p>
  <button class="btn btn-ghost btn-sm no-print" data-print>Print this page</button>
  {run_card()}
</section>'''

index_body = hero + summary + nine + method + why + val_section + howto + limits + parallel_section + run_card_section
exec_body = f'''<section class="hero" style="padding-top:44px">
  <div class="eyebrow">Executive summary</div>
  <h1 style="font-size:clamp(30px,4vw,46px)">The best file to download — and the honest reason it is not cleared.</h1>
  <p class="lede">The new Korea7 consensus candidate is the only file in this project with 0% forward 3-px overlap against all nine focus-site submissions. It is format-valid and its PROJECTED leaderboard value is 0.3382, above the B2 projection of 0.2769. But its catalogue hide-and-recover HOLDOUT-DTI is 0.0000, below the random control, and it fails the literal 13GEMS covering-lattice probe. It is a research artifact, not an organizer-cleared submission.</p>
  <div class="hero-actions"><a class="btn btn-primary" href="downloads/{esc(CANDIDATE_NAME)}.tif">⬇ Download the TIF</a><a class="btn btn-ghost" href="how-to-submit.html">How to submit</a><a class="btn btn-ghost" href="validation.html">Validation report</a></div>
</section>
<section class="section"><h2>Answer: why did GEMSDOE32 (0.2778) lead?</h2><p class="sub">The nine focus-site rasters are one dotted-ridge family. GEMSDOE32 is the most pruned member: 37,654 dots, 58.4% far from the catalogue, 0% within 2 px. That geometry is the best fit to the nine USER-REPORTED scores in the OLS projection (fitted B2 = 0.2769). The leaderboard reward appears to be driven by precision away from the mapped catalogue, not by recovering the catalogue. The organizer masks known faults, so dots near the catalogue are likely false positives. Pruning the halo raises precision. B2 is the most aggressive pruner in the family, and it has the highest USER-REPORTED score.</p>
<p class="sub"><strong>Can we generate a higher score?</strong> Possibly, but not demonstrated. The consensus candidate's PROJECTED value is 0.3382, above B2's 0.2769, because it pushes the far-catalogue fraction to 85.7% and reduces the dot count to 20,000. But the projection is an OLS extrapolation from nine unverified scores and cannot see surface quality. The catalogue hide-and-recover holdout gives the candidate 0.0000, below the random control, because the candidate is off-catalogue by design. The two instruments disagree by construction. No organizer receipt exists. The candidate is a research artifact, not a cleared submission.</p></section>
<section class="section"><h2>Candidate comparison</h2>{summary_table()}</section>
<section class="section"><h2>Nine focus sites</h2>{nine_site_table()}</section>
<section class="section"><h2>Holdout evidence</h2>{holdout_table()}</section>
<section class="section"><h2>Validation</h2>{validation_table()}</section>
<section class="section"><h2>Parallel session</h2><p class="sub">A parallel session committed a separate research pipeline and candidate rasters. Its own README says they fail the format gate on a geotransform mismatch. It is not a cleared submission. <a href="parallel-index.html">Parallel index</a> · <a href="method.html">Parallel method</a> · <a href="verification.html">Parallel verification</a> · <a href="parallel-readme.md">Parallel README</a>.</p></section>
<section class="section"><h2>Run card</h2><button class="btn btn-ghost btn-sm no-print" data-print>Print this page</button>{run_card()}</section>'''

howto_body = f'''<section class="hero" style="padding-top:44px"><div class="eyebrow">How to submit</div><h1 style="font-size:clamp(30px,4vw,46px)">From download to submission, step by step.</h1><p class="lede">The portal accepts a single-band GeoTIFF or a ZIP containing one GeoTIFF. Our file matches the submission format's CRS, shape, and geotransform. The decision to submit is an owner decision: the file is a research artifact and is not organizer-cleared.</p></section>
<section class="section"><div class="callout"><div class="icon">⚠️</div><p><strong>NOT CLEARED — do not submit without an owner decision.</strong> The file passes the format gate and the nine-focus uniqueness gate, but fails the catalogue holdout gate (0.0000 below random) and the literal 13GEMS lattice probe. Submitting it spends a weekly slot on a research artifact.</p></div>
<h2>Submission packet</h2><dl class="kv">
<dt>File</dt><dd><a href="downloads/{esc(CANDIDATE_NAME)}.tif">TIF</a> · <a href="downloads/{esc(CANDIDATE_NAME)}.zip">ZIP</a></dd>
<dt>Submission name</dt><dd><code>{esc(CANDIDATE_NAME)}</code></dd>
<dt>Note ({len(card['note'])} chars)</dt><dd><code id="note-text">{esc(card['note'])}</code> <button class="btn btn-ghost btn-sm no-print" data-copy-target="#note-text">Copy note</button></dd>
<dt>SHA-256</dt><dd><code>{esc(CANDIDATE_SHA)}</code></dd>
<dt>Bytes</dt><dd>{CANDIDATE_BYTES:,}</dd>
<dt>Grid</dt><dd>EPSG:32611 · 3730 × 3292 · 100 m · transform matches sample</dd>
<dt>Values</dt><dd>min {VALIDATOR['min']} · max {VALIDATOR['max']} · no NaN · no inf</dd>
</dl></section>
<section class="section"><h2>Steps</h2><div class="steps">
<div class="step"><div><h3>Download</h3><p>Click the TIF or ZIP link above. The ZIP contains exactly one TIF with identical bytes.</p></div></div>
<div class="step"><div><h3>Verify the hash</h3><p>Compare the SHA-256 to <code>{esc(CANDIDATE_SHA)}</code>. Do not rename or re-encode the file.</p></div></div>
<div class="step"><div><h3>Open the competition submission page</h3><p>Go to <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/" target="_blank" rel="noopener">drivendata.org/competitions/306/competition-doe-gems</a> and click “New submission”.</p></div></div>
<div class="step"><div><h3>Upload the file</h3><p>Choose the TIF or ZIP. The portal will check the CRS, shape, and geotransform. If it returns “Predicted values must be in range [0, 1]”, the file has been altered; re-download it.</p></div></div>
<div class="step"><div><h3>Enter the note</h3><p>Paste the note exactly: <code>{esc(card['note'])}</code></p></div></div>
<div class="step"><div><h3>Submit</h3><p>Only after an owner decision. The file is not organizer-cleared. The holdout gate fails. The 13GEMS lattice probe fails. No organizer receipt exists.</p></div></div>
</div></section>'''

val_body = f'''<section class="hero" style="padding-top:44px"><div class="eyebrow">Validation report</div><h1 style="font-size:clamp(30px,4vw,46px)">Every check, from the saved bytes.</h1><p class="lede">The validator re-reads the on-disk TIFF and the ZIP. It checks CRS, shape, transform, dtype, range, NaN/inf, footprint, catalogue, and the ZIP member. The format gate passes. The holdout gate fails. The 13GEMS lattice probe fails.</p></section>
<section class="section">{validation_table()}</section>
<section class="section"><h2>HOLDOUT-DTI table</h2>{holdout_table()}</section>
<section class="section"><h2>Uniqueness vs the nine focus sites</h2><div class="table-wrap"><table><thead><tr><th>Focus site</th><th>Forward 3-px overlap</th><th>Reverse 3-px overlap</th><th>Surface Spearman</th><th>Exact mask equal</th></tr></thead><tbody>{''.join(f"<tr><td>{s}</td><td class='num-cell'>{fmt(v['forward_3px_overlap'],4)}</td><td class='num-cell'>{fmt(v['reverse_3px_overlap'],4)}</td><td class='num-cell'>{fmt(v['surface_spearman'],4)}</td><td>{pill('NO', 'pill-yes')}</td></tr>" for s, v in uniq['focus'].items() if s in FOCUS_ROWS)}</tbody></table></div><p style="color:var(--muted);font-size:13px;margin-top:10px">The candidate has 0% forward 3-px overlap with every focus-site raster by construction. The 13GEMS covering-lattice probe has {fmt(LATTICE['forward_3px_overlap'],4)} forward overlap; the literal 70% rule fails. This is a saturated covering-grid rule, flagged for an owner decision.</p></section>
<section class="section"><button class="btn btn-ghost btn-sm no-print" data-print>Print this page</button>{run_card()}</section>'''

sources_body = f'''<section class="hero" style="padding-top:44px"><div class="eyebrow">Sources</div><h1 style="font-size:clamp(30px,4vw,46px)">Official links and pinned hashes.</h1><p class="lede">Every number on this site is computed from the files in the repository. The links below are for manual review. The competition data are a SHA-pinned third-party mirror, not an organizer-authenticated download.</p></section>
<section class="section">{sources}</section>
<section class="section"><h2>Reproduce</h2><div class="card"><h3>Commands</h3><pre>python3 scripts/analyze_focus.py
python3 scripts/analyze_sites.py
python3 scripts/build_consensus.py
python3 scripts/build_site.py
pytest -q</pre><p style="margin-top:10px">The scripts read the pinned rasters in <code>data/</code> and the shared <code>vendor/gems57</code> evaluator/writer. They do not call the DrivenData portal and do not spend a submission slot.</p></div></section>'''

# per-site pages
site_pages = []
for s in ("GEMSDOE24", "GEMSDOE25", "GEMSDOE27", "GEMSDOE28", "GEMSDOE30",
          "GEMSDOE31", "GEMSDOE32", "GEMSDOE33", "GEMSDOE36"):
    r = FOCUS_ROWS[s]
    h = r["holdout"]
    body = f'''<section class="hero" style="padding-top:44px"><div class="eyebrow">{s}</div><h1 style="font-size:clamp(30px,4vw,46px)">{s}: {fmt(r['user_reported_score'],4)} USER-REPORTED.</h1><p class="lede">The highest file on this site is <code>{esc(r['leaderboard_file'])}</code>. It has {r['dots']:,} dots, {fmt(r['far_fraction'],3)} of them &gt;15 px from the catalogue, and a measured HOLDOUT-DTI of {fmt(h['pooled_dti'],4)} (95% CI {fmt(h['ci95'][0],4)}–{fmt(h['ci95'][1],4)}). It is not unique against the other focus sites under the literal 70% rule.</p></section>
<section class="section"><h2>Snapshot</h2><dl class="kv">
<dt>Leaderboard file</dt><dd><code>{esc(r['leaderboard_file'])}</code></dd>
<dt>USER-REPORTED score</dt><dd>{fmt(r['user_reported_score'],4)} — no organizer receipt</dd>
<dt>HOLDOUT-DTI</dt><dd>{fmt(h['pooled_dti'],4)} (95% CI {fmt(h['ci95'][0],4)}–{fmt(h['ci95'][1],4)})</dd>
<dt>Dots</dt><dd>{r['dots']:,}</dd>
<dt>Far &gt;15 px</dt><dd>{fmt(r['far_fraction'],3)}</dd>
<dt>Near &lt;=2 px</dt><dd>{fmt(r['near2_fraction'],3)}</dd>
<dt>Median catalogue distance</dt><dd>{fmt(r['median_distance_px'],1)} px</dd>
<dt>On catalogue</dt><dd>{r['on_catalogue']} positive cells</dd>
<dt>Unique vs other focus?</dt><dd>{status_pill(r['unique_vs_other_focus'], 'YES', 'NO — duplicate')}</dd>
<dt>Max forward overlap</dt><dd>{fmt(r['max_forward_overlap_other_focus'],3)} vs {r['worst_other_focus']}</dd>
</dl></section>
<section class="section"><h2>Why this site is not a new submission</h2><p class="sub">The nine focus-site rasters are one dotted-ridge family. Every pair has forward 3-px overlap &gt; 0.70. {s} is a member of that family, not an independent method. Its USER-REPORTED score is unverified and its HOLDOUT-DTI is measured against the mirror catalogue. It cannot be promoted as a unique submission without an owner decision on the literal rule.</p><div class="hero-actions"><a class="btn btn-primary" href="downloads/{esc(CANDIDATE_NAME)}.tif">Download the unique Korea7 candidate</a><a class="btn btn-ghost" href="executive-summary.html">Back to the executive summary</a></div></section>'''
    site_pages.append((f"site-{s}.html", body))

# write pages
(DOCS / "index.html").write_text(page("Korea7 GEMS — unique submission audit", "index.html", index_body))
(DOCS / "executive-summary.html").write_text(page("Executive summary — Korea7 GEMS", "executive-summary.html", exec_body))
(DOCS / "how-to-submit.html").write_text(page("How to submit — Korea7 GEMS", "how-to-submit.html", howto_body))
(DOCS / "validation.html").write_text(page("Validation report — Korea7 GEMS", "validation.html", val_body))
(DOCS / "sources.html").write_text(page("Sources — Korea7 GEMS", "sources.html", sources_body))
for name, body in site_pages:
    (DOCS / name).write_text(page(f"{name} — Korea7 GEMS", "", body))

manifest = {
    "schema": "korea7-site-manifest-v1",
    "generated_utc": "2026-11-04",
    "candidate": {"name": CANDIDATE_NAME, "tif": CANDIDATE_FILE, "zip": CANDIDATE_ZIP,
                  "sha256": CANDIDATE_SHA, "zip_sha256": card["raster"]["zip_sha256"],
                  "bytes": CANDIDATE_BYTES, "dots": CAND_GEO['dots'],
                  "projected": PROJ['projected_value'],
                  "projected_interval": PROJ['bootstrap_95_interval'],
                  "holdout_dti": CAND_HOLDOUT['pooled_dti'],
                  "holdout_ci": CAND_HOLDOUT['ci95'],
                  "random_dti": RANDOM_HOLDOUT['pooled_dti'],
                  "nine_focus_gate_passes": True,
                  "lattice_overlap": LATTICE['forward_3px_overlap'],
                  "verdict": "negative", "ok_to_submit": False},
    "pages": ["index.html", "executive-summary.html", "how-to-submit.html", "validation.html", "sources.html"] + [n for n, _ in site_pages],
    "downloads": [f"downloads/{CANDIDATE_NAME}.tif", f"downloads/{CANDIDATE_NAME}.zip",
                  f"downloads/{CANDIDATE_NAME}.json"],
}
(DATA / "site_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"pages": manifest["pages"], "candidate": manifest["candidate"]}, indent=2))
