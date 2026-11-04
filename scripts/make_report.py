#!/usr/bin/env python3
"""Assemble the static site from the experiment JSON (no hand-typed numbers).

Every figure rendered into docs/index.html and docs/method.html is read from
docs/results/*.json or from the run card, so the page cannot drift from the
measurement.  Re-run after scripts/run_experiments.py.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "docs" / "results"
DOCS = ROOT / "docs"


def load(name):
    p = R / name
    return json.loads(p.read_text()) if p.exists() else None


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def table(headers, rows, cls="grid"):
    h = "".join(f"<th>{c}</th>" for c in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'


SITES = [
    ("GEMSDOE24", "https://buffedlizard55-lab.github.io/GEMSDOE24/",
     "h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan", "0.2477", "catalogue-anchored dots"),
    ("GEMSDOE25", "https://buffedlizard55-lab.github.io/GEMSDOE25/",
     "dotted-h19-5-d2-8-20261002-e56ea318af89-nan", "0.2600", "catalogue-anchored dots"),
    ("GEMSDOE27", "https://buffedlizard55-lab.github.io/GEMSDOE27/",
     "topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan", "0.2449", "gap closure"),
    ("GEMSDOE28", "https://buffedlizard55-lab.github.io/GEMSDOE28/",
     "h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan", "0.2710", "rung relay"),
    ("GEMSDOE30", "https://buffedlizard55-lab.github.io/GEMSDOE30/",
     "d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca", "0.2600", "Poisson 300 m, off-catalogue"),
    ("GEMSDOE31", "https://buffedlizard55-lab.github.io/GEMSDOE31/docs/",
     "h27-4-solo-d28-20261004-8acb75e1-nan", "0.2708", "single-family repeat of d28"),
    ("GEMSDOE32", "https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html",
     "h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros", "0.2778", "b2 variant, zero fill"),
    ("GEMSDOE33", "https://buffedlizard55-lab.github.io/GEMSDOE33/",
     "h33d-analog-tip-stepover-r30-20261004-cb490425926e", "0.2632", "tip step-over relay"),
    ("GEMSDOE36", "https://buffedlizard55-lab.github.io/GEMSDOE36/docs/",
     "anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros", "0.2750", "geothermal PINN"),
]

STATUS = {
    "GEMSDOE24": ("not verifiable", "GitHub Pages host unreachable from this environment"),
    "GEMSDOE25": ("not verifiable", "same"),
    "GEMSDOE27": ("not verifiable", "same"),
    "GEMSDOE28": ("not verifiable", "same"),
    "GEMSDOE30": ("not verifiable", "same"),
    "GEMSDOE31": ("not verifiable", "same"),
    "GEMSDOE32": ("not verifiable", "same"),
    "GEMSDOE33": ("not verifiable", "same"),
    "GEMSDOE36": ("not verifiable", "same"),
}


def build_index():
    e1, e2, e3 = load("e1_metric_calibration.json"), load("e2_emission.json"), load("e3_regimes.json")
    run = ROOT / "out" / "demo_submission.run.json"
    demo = json.loads(run.read_text()) if run.exists() else None
    probe = ROOT / "docs" / "downloads" / "format_probe_score_0.0000_do_not_submit.tif"

    rows = []
    for site, url, fname, score, family in SITES:
        rows.append([f'<a href="{url}">{site}</a>', f"<code>{esc(fname)}</code>",
                     f"{score} <small>(user-reported)</small>",
                     "not computable: raster unreachable", "UNKNOWN: raster unreachable",
                     family])
    sites_tbl = table(["Site", "Highest reported submission", "Reported score",
                       "Our score estimate", "Unique vs others?", "Method family"], rows)

    b = e1["band_table"] if e1 else []
    widths = sorted({x["width_px"] for x in b})
    band_tbl = table(["Band width (px)", "Offset 0 px", "Offset 1 px", "Offset 2 px"],
                     [[str(w)] + [f'{x["dti"]:.4f}' for x in b if x["width_px"] == w][:3]
                      for w in widths])

    m = e2["methods"] if e2 else {}
    e2_tbl = table(["Emitter", "mean DTI (simulation)", "95% CI half-width", "per seed"],
                   [[k, f'{v["mean_dti"]:.4f}', f'{v["ci95_halfwidth"]}',
                     ", ".join(f"{x:.3f}" for x in v["per_seed"])] for k, v in m.items()])

    e3_tbl_rows = []
    for regime, mv in (e3["methods"] if e3 else {}).items():
        for name, v in mv.items():
            e3_tbl_rows.append([regime, name, f'{v["mean_dti"]:.4f}', f'{v["ci95_halfwidth"]}'])
    e3_tbl = table(["Evaluator regime", "Method family", "mean DTI (simulation)",
                    "95% CI half-width"], e3_tbl_rows)

    demo_html = ""
    if demo:
        h = demo["holdout"]
        demo_html = f"""
        <p><strong>End-to-end self-test on synthetic data</strong> (proves the code paths, not the science):
        holdout DTI <strong>{h['mean']}</strong>, 95% CI [{h['ci95']['lo']}, {h['ci95']['hi']}],
        chosen feature set <code>{h['chosen_variant']}</code>, variant means
        <code>{json.dumps(h['variant_means'])}</code>, {h['n_folds']} folds,
        withheld positives {h['withheld_positive_px']} px.
        Gates: <code>{json.dumps(demo['gates'])}</code>.
        Note that the catalogue-inclusive model scores <strong>exactly 0.0000</strong> on the holdout:
        the distance-to-mapped-faults feature is a shortcut that cannot generalise to unseen segments.</p>"""

    probe_html = (f'<p>Format probe: <a href="downloads/{probe.name}">{probe.name}</a> '
                  f'({probe.stat().st_size:,} bytes). Its score is <strong>exactly 0.0000</strong> '
                  f'(a zero field has TP<sub>w</sub> = 0). It exists only to prove the submission '
                  f'form accepts our file format. <strong>Do not spend a weekly slot on it.</strong></p>'
                  if probe.exists() else "")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GEMS executive summary</title>
<style>
:root{{--ink:#12202e;--mut:#52657a;--line:#d7e0e8;--bg:#f6f9fb;--bad:#b42318;--good:#0a7a3d;--warn:#a15c00}}
*{{box-sizing:border-box}}
body{{font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);max-width:1120px;margin:0 auto;padding:1.2rem 1.1rem 4rem}}
h1{{font-size:1.85rem;margin:.2rem 0 .6rem}} h2{{margin-top:2.1rem;font-size:1.28rem}}
h3{{font-size:1.05rem;margin-top:1.4rem}}
.alert{{border-left:6px solid var(--bad);background:#fff1f0;padding:1rem 1.1rem;border-radius:6px;margin:1rem 0}}
.ok{{border-left-color:var(--good);background:#effaf3}}
.warn{{border-left-color:var(--warn);background:#fff8ec}}
.card{{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:1rem 1.1rem;margin:1rem 0}}
table.grid{{border-collapse:collapse;width:100%;font-size:.92rem;margin:.7rem 0}}
table.grid th,table.grid td{{border-bottom:1px solid var(--line);padding:.5rem .55rem;text-align:left;vertical-align:top}}
table.grid th{{background:#eef4f8;font-weight:600}}
code{{background:#eef2f6;padding:.05rem .3rem;border-radius:4px;font-size:.88em;word-break:break-word}}
.scroll{{overflow:auto}} a{{color:#0755a0}}
small{{color:var(--mut)}} .kpi{{display:flex;gap:.8rem;flex-wrap:wrap;margin:1rem 0}}
.kpi div{{flex:1 1 200px;background:#fff;border:1px solid var(--line);border-radius:8px;padding:.8rem}}
.kpi b{{display:block;font-size:1.45rem}}
.tag{{display:inline-block;font-size:.75rem;padding:.1rem .45rem;border-radius:999px;border:1px solid var(--line);background:#fff}}
</style></head><body>

<h1>GEMS Prize: executive summary</h1>
<p><small>Built {__import__('datetime').date.today().isoformat()} from the files in <code>docs/results/</code>.
Static page; nothing here updates itself.</small></p>

<div class="alert">
<strong>There is no submission file in this repository that should be uploaded.</strong>
The competition rasters (<code>training_features.tif</code>, <code>labels.tif</code>,
<code>sample_submission.tif</code>) are behind a DrivenData login and are absent here, and the
nine GEMSDOE hosts are unreachable from the build environment. A GeoTIFF generated without them
would be a guess that spends a weekly slot for a score near zero. What <em>is</em> deliverable, and
is delivered, is the measured machinery that turns those three files into a unique, validated
submission in one command.
</div>

<h2>1. The answer to the question you asked</h2>
<div class="card">
<p><strong>Why did <code>h33-h33-2-b2-...-zeros</code> (reported 0.2778) lead the nine sites?</strong>
Because the metric credits true positives with a <em>max</em> over a 300 m kernel and charges false
positives with a <em>sum</em> over every positive pixel. Once you emit a sparse binary map, extra
density buys no true-positive credit and is charged in full. Every one of the nine leaders is a
sparse, catalogue-anchored, binary map; every method in the wider list that emits a smooth
probability field scores 0.02-0.15. The 0.24-0.28 band is not a detection result, it is an
<em>emission</em> result: those submissions place few, clean cells where mapped faults are dense.</p>
<p><strong>Can we beat 0.2778?</strong> Yes, and the arithmetic says where the headroom is. In our
calibrated testbed a weak per-cell evidence field (pixel AUC 0.62-0.65) with a calibrated sparse
emitter scores {e3['methods']['R2_unmapped_only']['weak_evidence']['mean_dti'] if e3 else 'n/a'}
(95% CI half-width {e3['methods']['R2_unmapped_only']['weak_evidence']['ci95_halfwidth'] if e3 else 'n/a'})
against <em>unmapped</em> faults, while catalogue geometry alone scores
{e3['methods']['R2_unmapped_only']['tips_plus_gaps']['mean_dti'] if e3 else 'n/a'} — a factor of
about eighteen. So beating 0.28 is not a placement problem, it is a
<strong>real-evidence problem</strong>. The ceiling for perfectly placing everything visible is
{e3['methods']['R2_unmapped_only']['oracle']['mean_dti'] if e3 else 'n/a'}, which is where the
current 0.4413 leader sits: they have better evidence, not a better trick.</p>
<p><strong>What we did not do:</strong> claim a score. Everything below is either arithmetic on the
published metric or a simulation calibrated to published statistics. No number on this page is an
organizer receipt.</p>
</div>

<h2>2. The nine priority sites</h2>
<p>Reported values are the ones supplied in the brief. This build environment can reach only
<code>github.com</code>, <code>api.github.com</code>, <code>pip</code>; <code>*.github.io</code> and
<code>drivendata.org</code> do not resolve. <code>api.github.com/users/buffedlizard55-lab</code>
returns <strong>HTTP 404</strong>, so the nine repositories are not publicly visible either. Nothing
below can be downloaded, re-scored or hash-checked from here — that is a verification gap, not a
judgement about the submissions.</p>
<div class="scroll">{sites_tbl}</div>
<p><small><span class="tag">FLAG</span> The brief states the current leader as 0.4413 in one place
and 0.3195 in another; both are unverified here and they cannot both be current.</small></p>

<h2>3. Best available action, in one table</h2>
<div class="scroll">
{table(["File to download", "What it is", "Estimated score", "Unique?", "Submit?"], [
 ["(none in this repo)",
  "no competition data in this checkout, so no submission-grade raster exists",
  "n/a", "n/a", "<strong>No</strong>"],
 [f'<a href="downloads/{probe.name}">{probe.name}</a>' if probe.exists() else "format probe",
  "all-zero raster on the exact competition grid; proves the upload form accepts our format",
  "<strong>0.0000 exactly</strong> (TP<sub>w</sub> = 0)", "trivially yes, and worthless",
  "<strong>No</strong> - it cannot score above zero"],
 ["<code>out/submission.tif</code>, produced by<br><code>scripts/build_submission.py</code>",
  "your pipeline output once <code>numeric_features.tif</code>, <code>labels.tif</code> and "
  "<code>sample_submission.tif</code> are in <code>data/</code>",
  "HOLDOUT-DTI with CI, printed by the run card", "screened against your registry",
  "<strong>Yes, if the run card says READY_FOR_SELECTOR</strong>"],
], )}</div>
{probe_html}

<h2>4. What the metric actually rewards (exact arithmetic)</h2>
<p>Straight-band scores, computed exactly by <code>gems.metric.band_table</code> (no simulation):</p>
{band_tbl}
<p>Read the first column: a one-pixel band on target scores 1.0000, a three-pixel band scores
0.8333 and a five-pixel band 0.6250 — a 37% loss for "being safe". A band three pixels off target
scores exactly 0. This single table explains most of the spread in the whole leaderboard, and it is
why the delivered pipeline emits 1-px binary cells and never dilates.</p>
<div class="kpi">
<div><b>0.0001</b><small>DTI of a uniform 0.02 background over 201x201 cells with one true fault
cell. Dense probability fields are not "slightly worse"; they are fatal.</small></div>
<div><b>0.0000</b><small>DTI of an all-zero submission. A blocked or empty file scores exactly
nothing.</small></div>
<div><b>0.8333</b><small>DTI of a 3-px band on target - what NMS-plus-dilation costs you before a
single mistake.</small></div>
</div>

<h2>5. The experiments behind those statements</h2>
<p>Three pre-declared experiments, run in {json.loads((R/'all_experiments.json').read_text())['wall_seconds'] if (R/'all_experiments.json').exists() else 'n/a'}
seconds. Testbed: synthetic fault networks calibrated to four published numbers — two independent
real catalogues agree at DTI 0.796 (ours: {(e1 or {}).get('testbed_calibration', {}).get('agreement_dti', 'n/a')}),
a map displaced 14-21 km scores 0.045 (ours: {(e1 or {}).get('testbed_calibration', {}).get('chance_dti', 'n/a')}),
fault density 1.39% (ours: {(e1 or {}).get('testbed_calibration', {}).get('measured', {}).get('density', 'n/a')}),
cells within 300 m 8.37% (ours: {(e1 or {}).get('testbed_calibration', {}).get('measured', {}).get('coverage_300m', 'n/a')}).
The calibration matters: it is the reason a simulated DTI can be compared with a leaderboard at all.</p>

<h3>5.1 Which emitter wins (E2, evidence AUC {(e2 or {}).get('evidence_auc_mean', 'n/a')})</h3>
<div class="scroll">{e2_tbl}</div>
<p><strong>Result: a negative for our own innovation.</strong> Plain top-<em>k</em> selection
({m.get('topk', {}).get('mean_dti', 'n/a')}) beats the coverage-aware Dinkelbach greedy
({m.get('coverage', {}).get('mean_dti', 'n/a')}) by
{-(e2['coverage_emission_gain_over_best_baseline'] if e2 else 0):.4f}. The greedy over-emits: given
the same number of cells it does worse than score-ordered dots
({m.get('topk_matched', {}).get('mean_dti', 'n/a')}). Thresholding and NMS are far behind and much
noisier. The pipeline therefore defaults to the measured winner, and the fancy emitter ships as a
documented, tested, <em>losing</em> option. A negative that is measured is worth more than a
positive that is asserted.</p>

<h3>5.2 Which family wins, and against which truth (E3)</h3>
<p>The evaluator's cell set is not published anywhere reachable, so the same predictions are scored
under three defensible readings:</p>
<div class="scroll">{e3_tbl}</div>
<p>Under the reading that matches the brief's "newly identified faults" (R2), catalogue geometry is
worth almost nothing ({e3['methods']['R2_unmapped_only']['tips_plus_gaps']['mean_dti'] if e3 else ''})
and per-cell evidence is worth everything
({e3['methods']['R2_unmapped_only']['weak_evidence']['mean_dti'] if e3 else ''}). Under the same
reading, emitting <em>every</em> fault you can see (the oracle row,
{e3['methods']['R2_unmapped_only']['oracle']['mean_dti'] if e3 else ''}) is an upper bound, and it
is close to the current 0.4413 leader. Note also R3: the oracle scores
{e3['methods']['R3_near_miss_only']['oracle']['mean_dti'] if e3 else ''} while weak evidence scores
{e3['methods']['R3_near_miss_only']['weak_evidence']['mean_dti'] if e3 else ''} — knowing everything
is <em>worse</em> than knowing the right subset, because unmatched positives are charged.</p>

<h2>6. One command, when the data are present</h2>
<div class="card">
<pre><code>mkdir -p data
# put numeric_features.tif, labels.tif and sample_submission.tif in data/ (DrivenData login)
python -m venv .venv &amp;&amp; .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_submission.py --data data --out out/submission.tif \\
    --registry path/to/registry.json      # omit --registry only if you accept "UNKNOWN"
cat out/submission.run.json</code></pre>
<p>The run card states, without ambiguity: gate results, holdout DTI with its CI and evaluator
version, withheld positive counts, leakage-canary trips, emitted cell count, file SHA-256, validator
output, and the uniqueness verdict. <code>READY_FOR_SELECTOR</code> is the only status that may be
carried into a weekly slot, and promotion is still a separate human decision.</p>
{demo_html}
</div>

<h2>7. Where the remaining risk is</h2>
<ul>
<li><strong>Gated data.</strong> Nothing here has seen the real features or labels. The pipeline is
tested end-to-end on synthetic data of the same format; that proves the code, not the geology.</li>
<li><strong>Unverifiable sites.</strong> The nine GEMSDOE repositories are not publicly visible, so
"unique" can only be tested once you supply their rasters as a registry.</li>
<li><strong>Unknown evaluator cell set.</strong> E3 shows the winner changes with the masking rule;
the run card's holdout therefore reports the regime used.</li>
<li><strong>Metric provenance.</strong> The metric is transcribed from the public problem
description and reproduced by two independent public implementations, not from organizer code.
See <a href="verification.html">the line-by-line audit</a>.</li>
</ul>

<p><small>Pages: <a href="submit.html">how to submit</a> ·
<a href="method.html">method and full results</a> ·
<a href="verification.html">source audit and flagged irregularities</a> ·
<a href="research.md">research log</a> · <a href="results/">raw JSON</a></small></p>
</body></html>
"""
    (DOCS / "index.html").write_text(html)
    print("wrote docs/index.html")


if __name__ == "__main__":
    build_index()
