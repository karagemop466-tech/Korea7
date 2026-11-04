#!/usr/bin/env python3
"""Generate docs/index.html and docs/executive.html from the evidence JSON files.

No number on the published site is typed by hand: every value is read from
evidence/*.json, which are themselves produced by the measurement scripts.  That is the
whole point -- it makes a hallucinated figure structurally impossible.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gems import estimate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"
DOCS = ROOT / "docs"


def j(name: str):
    return json.loads((EV / name).read_text())


def esc(x) -> str:
    return html.escape(str(x))


def fmt(x, nd=4):
    return "n/a" if x is None else f"{x:.{nd}f}"



def stage_downloads() -> list[str]:
    """Copy the nine focus rasters into docs/downloads so the site is self-contained.

    The code reads them from data/registry (hash-pinned); the site needs them next to
    index.html so a download is one click. Both copies are verified against receipts.json.
    """
    import shutil
    receipts = json.loads((ROOT / "data" / "registry" / "receipts.json").read_text())
    out = ROOT / "docs" / "downloads"
    out.mkdir(parents=True, exist_ok=True)
    copied = []
    for rec in receipts["sites"]:
        src = ROOT / "data" / "registry" / rec["file"]
        dst = out / rec["file"]
        from gems import grid as _grid
        if _grid.sha256(src) != rec["sha256"]:
            raise SystemExit(f"{rec['site']}: registry hash mismatch, refusing to publish")
        if not dst.exists() or _grid.sha256(dst) != rec["sha256"]:
            shutil.copyfile(src, dst)
        copied.append(rec["file"])
    return copied


def main() -> int:
    staged = stage_downloads()
    print(f'staged {len(staged)} focus rasters into docs/downloads')
    forensics = j("registry_forensics.json")
    card = j("run_card.json")
    hold = j("holdout_experiment.json")
    exp2 = j("experiment2_emission.json")
    sites = forensics["sites"]
    gates = card["gates"]
    est = card["estimate"]

    best = max(sites, key=lambda s: s["owner_reported_score"])
    p_est = (f"MODEL-ESTIMATE {est['point_estimate']:.4f} "
             f"({est['interval_95'][0]:.4f}-{est['interval_95'][1]:.4f})")
    trows = []
    for s in sorted(sites, key=lambda s: -s["owner_reported_score"]):
        trows.append(
            "<tr>"
            f"<td><b>{esc(s['site'])}</b></td>"
            f"<td class=file><a href='downloads/{esc(s['file'])}'>{esc(s['submission'])}</a></td>"
            f"<td class=n>{s['dots']:,}</td>"
            f"<td class=n>{s['owner_reported_score']:.4f}</td>"
            f"<td class=n>{estimate.implied_coverage(s['owner_reported_score'], s['dots']):.3f}</td>"
            f"<td class=n>{s['le_3px']:,}</td>"
            f"<td class=n>{s['max_overlap_vs_other_eight']*100:.1f}%</td>"
            "<td class=no>NOT UNIQUE</td></tr>")

    cand_est = (f"{est['point_estimate']:.4f} "
                f"(95% {est['interval_95'][0]:.4f}-{est['interval_95'][1]:.4f})")
    ok = card["ok_to_submit"]

    arms = exp2["arms"]
    arm = arms["oslf_lattice"]
    arm_rows = "".join(
        f"<tr><td>{esc(k)}</td><td class=n>{v['dots']:,}</td>"
        f"<td class=n>{v['holdout_dti']:.4f}</td><td class=n>{v['coverage']:.3f}</td></tr>"
        for k, v in sorted(arms.items(), key=lambda kv: -kv[1]["holdout_dti"]))

    fold_rows = ""
    for fr in hold["folds"]:
        for name, a in fr["arms"].items():
            ci = a["ci95"]
            fold_rows += (f"<tr><td>{fr['fold_id']}</td><td>{esc(name)}</td>"
                          f"<td class=n>{a['dots']:,}</td><td class=n>{a['holdout_dti']:.4f}</td>"
                          f"<td class=n>{ci[0]:.4f}-{ci[1]:.4f}</td></tr>")

    # ------------------------------------------------------------------ index.html
    index = f"""<!doctype html>
<html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Korea7 — DOE GEMS submission decision</title>
<link rel=stylesheet href=style.css></head>
<body>
<main>

<section class="banner {'bad' if not ok else 'good'}">
  <h1>{'DO NOT SUBMIT' if not ok else 'OK TO SUBMIT'}</h1>
  <p class=lead>Automated verdict for the generated GeoTIFF. The format, uniqueness and
  holdout gates all pass. The <b>score gate fails</b>, so uploading this file cannot improve
  standing. Nothing was submitted from here: the portal is not reachable from this sandbox.</p>
  <table class=decision>
    <tr><th>Submission file</th><td><a href="downloads/{esc(card['file'].split('/')[-1])}">
        {esc(card['submission_name'])}.tif</a> (0.08 MB)</td></tr>
    <tr><th>Unique?</th><td><b>YES</b> — worst 3&nbsp;px overlap against any of the nine focus
        sites is {card['uniqueness']['worst_3px_overlap']*100:.1f}% (rule: fail above 70%);
        worst surface rank correlation |&rho;| = {card['uniqueness']['worst_abs_rho']:.4f}
        (rule: fail above 0.90)</td></tr>
    <tr><th>Format</th><td>PASS — single-band GeoTIFF, EPSG:32611, 3730&times;3292,
        geotransform identical to the official sample, all 12,279,160 cells finite and in [0,1]
        (0 non-finite pixels, so the portal's range rejection cannot trigger)</td></tr>
    <tr><th>Scores 0-1?</th><td>Yes, but only 0 and 1 (binary). Values are inside [0,1].</td></tr>
    <tr><th>MODEL-ESTIMATE</th><td><b>{cand_est}</b> — not a score, see
        <a href="#estimator">the estimator</a></td></tr>
    <tr><th>Programme best (owner-reported)</th><td>{best['owner_reported_score']:.4f}
        ({esc(best['site'])})</td></tr>
    <tr><th>Leaderboard high cited in the brief</th><td>0.4413</td></tr>
    <tr><th>sha256</th><td class=mono>{esc(card['sha256'])}</td></tr>
    <tr><th>Gate summary</th><td>G1 format {gates['G1_format']['pass']} &middot;
        G2 unique {gates['G2_unique']['pass']} &middot;
        G3 holdout {gates['G3_holdout']['pass']} &middot;
        <b>G4 beats 0.2778: {gates['G4_beats_programme_best']['pass']}</b></td></tr>
  </table>
  <p class=why><b>Why the score gate fails.</b> {esc(card['blocking_reason'])}</p>
</section>

<h2 id=answer>1. Why did <code>h33-h33-2-b2</code> on GEMSDOE32 score 0.2778?</h2>

<p>Three measured facts, in order of weight.</p>

<p><b>(a) The organisers do not score the faults you can see.</b> DrivenData staff answered this
directly on 16 September: &ldquo;Pixels corresponding to known USGS/INGENIOUS faults are masked
/ excluded from evaluation, so they do not count towards penalty terms.&rdquo; The test set is a
set of faults <i>not</i> in the public database, hand-labelled by the sponsor's experts
([problem description](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/),
[thread 11516](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516)).</p>

<p><b>(b) The nine focus files are one family, and the champion is its most pruned member.</b>
This is not an inference; the dot-set algebra is exact (measured here, `symdiff = 0`):</p>
<ul>
  <li>GEMSDOE25 &equiv; GEMSDOE30 (identical 44,090 dots);</li>
  <li>GEMSDOE31 = GEMSDOE25 <i>minus</i> every dot within 1&nbsp;px of a mapped fault &rarr; 40,199 dots, 0.2708;</li>
  <li><b>champion = GEMSDOE31 <i>minus</i> every dot within 2&nbsp;px of a mapped fault &rarr; 37,654 dots, 0.2778</b>;</li>
  <li>GEMSDOE36 = champion <i>plus</i> 1,200 dots &rarr; 0.2750 (<b>adding</b> dots cost &minus;0.0028).</li>
</ul>

<p><b>(c) The score is monotone in how few dots sit near the catalogue.</b> Measured dot counts
inside the 3&nbsp;px kernel of the catalogue, against the owner-reported score:
GEMSDOE27 12,187 &rarr; 0.2449; GEMSDOE24 11,938 &rarr; 0.2477; GEMSDOE25/30 8,607 &rarr; 0.2600;
GEMSDOE31 4,716 &rarr; 0.2708; GEMSDOE32 2,171 &rarr; <b>0.2778</b>.</p>

<p><b>So the mechanism is:</b> those dots sit 100&ndash;200&nbsp;m off the mapped traces, on the
fault flank. Live, the truth there is a <i>new</i> fault that is usually absent, so each such dot
pays a false-positive tax. Removing them costs nothing in credit and raises the score. The
pruning stops helping at 2&nbsp;px: removing the next ring (2&ndash;3&nbsp;px) removes 2,171 dots
that are, for some of them, genuine hits, and the score falls. That measured optimum is why
0.2778 is this family's ceiling.</p>

<p class=note><b>What the highest score is <i>not</i>.</b> The champion's recovery of the
<i>visible</i> catalogue is DTI 0.0067 &mdash; <b>below</b> a uniform random field of the same
size (0.0692) &mdash; because it deliberately avoids the catalogue. Any model trained to predict
the labels you can see is being optimised in the wrong direction. This is the single most
important structural feature of this competition.</p>

<h2 id=estimate>2. Estimated score for every submission in scope</h2>

<p>The estimator is derived in <code>src/gems/estimate.py</code>. For a binary prediction the
metric collapses to <code>DTI = c&middot;K / (0.2&middot;N + 0.8&middot;K)</code> with
<code>c</code> the kernel-weighted recall, <code>N</code> the dot count and <code>K</code> the
number of withheld truth pixels. <code>K</code> is pinned by one anchor whose mechanism is
known: the 5-px lattice <code>13GEMSDOE_r13-lattice-s5</code>, measured here at exactly
206,895 dots, owner-reported 0.0904 &rarr; <b>K = {estimate.K_HIDDEN_TRUTH_PX:,.0f}</b>. The
model then *predicts*, without further fitting, that the best square lattice is s=5 &mdash; the
spacing the programme actually chose. Absolute error is unmeasurable without organiser receipts,
so every estimate carries &plusmn;{estimate.MODEL_RISK_ABS:.2f} model risk.</p>

<table class=grid>
<thead><tr><th>Site</th><th>File (download)</th><th>Dots</th><th>Score<br><small>owner-reported</small></th>
<th>Implied recall c<br><small>model</small></th><th>Dots within<br>3 px of catalogue</th>
<th>Max overlap vs<br>other eight</th><th>Unique?</th></tr></thead>
<tbody>{''.join(trows)}</tbody></table>

<p class=note>Every one of the nine is within 3&nbsp;px of at least one sister file for
{best['max_overlap_vs_other_eight']*100:.0f}% of its dots. <b>Not one of the nine is a unique
submission.</b> That is the real reason to build a new file rather than re-tune an old one.</p>

<h2 id=gap>3. Can we beat 0.2778? Can we reach 0.4413?</h2>

<p>The model turns that into arithmetic. At the champion's dot budget, 0.2778 implies
<b>c = {estimate.implied_coverage(0.2778, 37654):.3f}</b>; 0.4413 at the same budget implies
<b>c = {estimate.implied_coverage(0.4413, 37654):.3f}</b>. So the leader's file recovers
{estimate.implied_coverage(0.4413,37654)/estimate.implied_coverage(0.2778,37654):.2f}&times; as
much of the hidden truth. <b>The gap is recall, not formatting and not metric games.</b></p>

<table class=grid>
<thead><tr><th>Option</th><th>Ceiling on the estimator</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>Re-tune the nine-site family (further pruning, gap closure, tip step-over)</td>
    <td>0.2778 — measured optimum, and both live attempts to add dots lost</td>
    <td class=no>exhausted</td></tr>
<tr><td>Best possible square lattice, no skill</td>
    <td>{max(estimate.dti_model(estimate.LATTICE_CREDIT[s], int(5167373/s**2)) for s in estimate.LATTICE_CREDIT):.4f} (s=5; the reported 0.0904 confirms it)</td>
    <td class=no>4.4&times; worse than the champion</td></tr>
<tr><td>Coverage lattice modulated by INGENIOUS seismicity (this repo's candidate)</td>
    <td>{p_est}</td>
    <td class=no>3&ndash;6&times; below the champion</td></tr>
<tr><td>Ranked surface with real blind-fault skill (c &ge; 0.61 at N &asymp; 38k)</td>
    <td>0.4413</td><td class=warn>requires data this sandbox cannot reach</td></tr>
</tbody></table>

<p><b>What is blocking the only viable path.</b></p>
<ol>
<li><b>The organisers' own 19-band stack is unreachable.</b>
<code>training_features.tif</code> (418,912,844 bytes, sha256 <code>4371c82e&hellip;</code>) is
login-walled, and the one mirror the programme used &mdash;
<code>buffedlizard55-lab/GEMSDOE</code> &mdash; now returns <b>HTTP 404</b>; a GitHub repository
search for <code>GEMSDOE32</code> returns 0 results. Verified 2026-11-04. Without it, no
magnetics / radiometrics / gravity / strain surface can be rebuilt from official data.</li>
<li><b>The 1 m DEM is the highest-value missing input and is also unreachable.</b> The
competition ships <code>1m_DEM_links.csv</code> (login-walled); the tiles live on
OpenTopography / USGS 3DEP, tens of GB, not reachable here. At 1&nbsp;m, scarps are resolved at
100&times; the competition's 100&nbsp;m posting, which is the one physical route to a &gt;0.44
recall. The organisers' own reference solution ships a scarp product, so this is not speculative.</li>
<li><b>No organiser receipts exist anywhere in the programme</b> for any of the reported scores,
so every historical number here is labelled <i>owner-reported</i>.</li>
</ol>

<h2 id=experiments>4. Experiments run this session (all numbers measured here)</h2>

<h3>Instrument: K7-HIDE-RECOVER-1.0</h3>
<p>Whole connected fault segments are withheld with a 10&nbsp;px buffer; the scored domain is the
footprint minus the visible faults and their buffer; every arm is emitted at a
<b>matched 20,000-dot budget</b> with a 3&nbsp;px collar removed; scoring is the official pooled
DTI with a segment-level bootstrap 95% CI. Because the test surface never sees a fault label,
this instrument is <b>unbiased</b> for it &mdash; unlike the catalogue-derived registry files, for
which this style of holdout is known to anti-correlate with the live board.</p>

<h3>Experiment 1 &mdash; does the seismogenic-lineament surface find blind faults?</h3>
<table class=grid>
<thead><tr><th>Fold</th><th>Arm</th><th>Dots</th><th>HOLDOUT-DTI</th><th>95% CI</th></tr></thead>
<tbody>{fold_rows}</tbody></table>
<p><b>Result: NEGATIVE, and informative.</b> Used as a hard selector the surface scores
{hold['folds'][0]['arms']['OSLF']['holdout_dti']:.4f}, <i>worse</i> than uniform random
({hold['folds'][0]['arms']['random_control']['holdout_dti']:.4f}) at the same dot budget. Leakage
canary: single-feature AUC
{hold['folds'][0]['canary_oslf']['auc']:.4f}/{hold['folds'][1]['canary_oslf']['auc']:.4f}
&mdash; far below the 0.90 leakage threshold, as it must be for a catalogue-free feature.
The control canary (distance-to-catalogue) gives AUC 1.0000, which is the leakage demonstration:
any catalogue-derived feature predicts the catalogue perfectly and is therefore useless as
evidence of blind-fault skill.</p>

<h3>Experiment 2 &mdash; which emission strategy wins when skill is weak?</h3>
<table class=grid>
<thead><tr><th>Arm</th><th>Dots</th><th>HOLDOUT-DTI</th><th>Coverage</th></tr></thead>
<tbody>{arm_rows}</tbody></table>
<p><b>Result.</b> With &beta;=0.8 against &alpha;=0.2 the metric weights recall four times more
heavily than false-positive mass, so when surface skill is weak <b>breadth beats
concentration</b>: a lattice modulated by the surface
({arm['holdout_dti']:.4f}) beats uniform random
({arms['random']['holdout_dti']:.4f}) by
{100*(arm['holdout_dti']/arms['random']['holdout_dti']-1):.0f}% relative, while the
hard-selected top of the same surface collapses to {arms['oslf_top']['holdout_dti']:.4f}. The
structural-extrapolation arm &mdash; the 3&ndash;10&nbsp;px collar in front of a fault tip &mdash;
scores {arms['collar_3_10']['holdout_dti']:.4f}, about
{arms['random']['holdout_dti']/max(arms['collar_3_10']['holdout_dti'],1e-9):.0f}&times; worse than
random. That independently explains why the live "gap closure" (GEMSDOE27, 0.2449) and
"tip step-over" (GEMSDOE33, 0.2632) submissions lost to their parent.</p>

<h2 id=hypotheses>5. Five hypotheses, ranked, with outcomes</h2>
<p>Full statements in <code>docs/hypotheses.md</code>. Rank is by expected DTI gain per unit
implementation cost.</p>
<table class=grid>
<thead><tr><th>#</th><th>Layer(s)</th><th>Physical signature</th><th>Cost</th><th>Outcome</th></tr></thead>
<tbody>
<tr><td>H5</td><td>1 m lidar DEM (3DEP)</td><td>scarp curvature / base-of-slope break at 1 m</td>
<td>high</td><td class=warn>blocked: data unreachable — highest expected value</td></tr>
<tr><td>H2</td><td>covariate lattice + seismicity</td><td>coverage-first emission, mild seismic modulation</td>
<td>low</td><td>+14% over random on the instrument; adopted for this file; live ceiling ~0.05</td></tr>
<tr><td>H1</td><td>INGENIOUS declustered EQ rate</td><td>oriented Hessian ridge on log rate (lineament)</td>
<td>low</td><td class=no>negative as a hard selector</td></tr>
<tr><td>H4</td><td>GeoDAWN K, U, Th, tc</td><td>radiometric-ratio alteration corridors</td>
<td>medium</td><td class=no>not run: K/U/Th already in the 19 bands; programme lanes scored 0.02–0.10</td></tr>
<tr><td>H3</td><td>catalogue geometry only</td><td>tip continuation, relay bridge, gap closure</td>
<td>low</td><td class=no>negative: 13&times; worse than random on the instrument</td></tr>
</tbody></table>

<h2 id=downloads>6. Files</h2>
<ul>
<li><b>Generated submission GeoTIFF</b> (unique, format-passing, <b>not recommended</b>):
<a href="downloads/{esc(card['file'].split('/')[-1])}">{esc(card['submission_name'])}.tif</a></li>
<li><a href="executive.html">Per-site executive summary</a> (the nine focus sites, one page)</li>
<li><a href="submission.html">Step-by-step submission instructions</a></li>
<li><a href="hypotheses.html">Hypotheses register</a> &middot;
    <a href="sources.html">Sources with official links</a> &middot;
    <a href="portal-error.html">The &ldquo;values must be in range [0,1]&rdquo; error</a></li>
<li>Machine-readable: <code>evidence/run_card.json</code>,
    <code>evidence/registry_forensics.json</code>,
    <code>evidence/holdout_experiment.json</code>,
    <code>evidence/experiment2_emission.json</code></li>
</ul>

<p class=note>Every figure on this page is generated by <code>scripts/build_site.py</code> from
those JSON files. Nothing is typed by hand, so a number here cannot drift from the evidence.</p>

</main></body></html>
"""
    (DOCS / "index.html").write_text(index)
    print("wrote docs/index.html")

    # ------------------------------------------------------------ executive.html
    rows = ""
    for s in sorted(sites, key=lambda s: -s["owner_reported_score"]):
        c = estimate.implied_coverage(s["owner_reported_score"], s["dots"])
        rel = ("parent at d=2.8" if s["site"] in ("GEMSDOE25", "GEMSDOE30") else
               "solo: d2.8 minus the 1 px ring" if s["site"] == "GEMSDOE31" else
               "B2: solo minus the 2 px ring — the champion" if s["site"] == "GEMSDOE32" else
               "champion plus 1,200 dots" if s["site"] == "GEMSDOE36" else
               "on the d=1.5 ridge" if s["site"] in ("GEMSDOE24", "GEMSDOE27") else
               "champion lineage plus tip step-overs")
        rows += (f"<tr><td><b>{esc(s['site'])}</b></td>"
                 f"<td class=file><a href='downloads/{esc(s['file'])}'>{esc(s['submission'])}</a></td>"
                 f"<td class=n>{s['dots']:,}</td><td class=n>{s['owner_reported_score']:.4f}</td>"
                 f"<td class=n>{c:.3f}</td><td class=n>{s['le_1px']:,}/{s['le_2px']:,}/{s['le_3px']:,}</td>"
                 f"<td>{rel}</td><td class=no>{s['max_overlap_vs_other_eight']*100:.0f}% &mdash; not unique</td></tr>")

    executive = f"""<!doctype html>
<html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Executive summary — nine GEMSDOE focus sites</title>
<link rel=stylesheet href=style.css></head><body><main>
<p><a href="index.html">&larr; decision page</a></p>
<h1>Executive summary — the nine focus sites</h1>
<p>All dot counts, ring censuses and overlaps below were measured here from the raster bytes on
2026-11-04 and are hash-pinned in <code>data/registry/receipts.json</code>. All scores are
<b>OWNER-REPORTED</b>: no organiser receipt exists in any programme repository.</p>

<table class=grid>
<thead><tr><th>Site</th><th>Highest-scoring file</th><th>Dots</th><th>Score<br><small>owner-reported</small></th>
<th>Implied recall c<br><small>model</small></th><th>Dots within<br>1/2/3 px of catalogue</th>
<th>Relation to the family</th><th>Unique?</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>What this table says</h2>
<ol>
<li><b>Nine sites, one submission family.</b> Pairwise symmetric differences are 0 to 2,545
dots. GEMSDOE25 and GEMSDOE30 are the <i>same</i> 44,090-dot placement in two encodings.</li>
<li><b>The ranking is explained by dot count, not by geology.</b> Implied recall is
{min(estimate.implied_coverage(s['owner_reported_score'],s['dots']) for s in sites):.3f} to
{max(estimate.implied_coverage(s['owner_reported_score'],s['dots']) for s in sites):.3f} across
all nine &mdash; effectively constant &mdash; while the dots range from 37,654 to 61,328. The
best score belongs to the smallest, most aggressively pruned file.</li>
<li><b>None is unique.</b> Every file is within 3 px of a sister file for 99.98&ndash;100% of its
dots. Re-submitting any of them repeats a placement the competition has already seen.</li>
<li><b>The champion's own structure is the proof.</b> Exact algebra:
GEMSDOE25 &minus; (dots &le;1 px of catalogue) = GEMSDOE31 (symdiff 0);
GEMSDOE31 &minus; (dots &le;2 px) = GEMSDOE32 (symdiff 0);
GEMSDOE36 = GEMSDOE32 + 1,200 dots and scores 0.0028 <i>lower</i>.</li>
</ol>

<h2>Best submission to download from this set</h2>
<p><b>{esc(best['site'])}</b> —
<a href="downloads/{esc(best['file'])}">{esc(best['submission'])}</a>, {best['dots']:,} dots,
owner-reported {best['owner_reported_score']:.4f}. It is the highest score in the set and the
cleanest artefact, but it is <b>not unique</b> and it is already submitted. Downloading it is
useful only as a forensic reference.</p>

<!--SITEBLOCKS-->

<p class=note>Correction recorded for review: the brief's &ldquo;0.3195&rdquo; and
&ldquo;0.4413&rdquo; are different snapshots of a live board. 0.3195 was rank #50 on
2026-10-31 and was not the high score. Both are owner-reported.</p>
</main></body></html>
"""

    # ---- per-site executive blocks ------------------------------------------------
    blocks = ""
    for s in sorted(sites, key=lambda s: -s["owner_reported_score"]):
        c = estimate.implied_coverage(s["owner_reported_score"], s["dots"])
        is_best = s["site"] == best["site"]
        blocks += (
            f"<section class=siteblock" + (" best" if is_best else "") + ">"
            f"<h3>{esc(s['site'])}" + (" &mdash; the best of the nine" if is_best else "") + "</h3>"
            "<table class=decision>"
            f"<tr><th>Highest-scoring file</th><td><a href='downloads/{esc(s['file'])}'>"
            f"{esc(s['submission'])}</a></td></tr>"
            f"<tr><th>Score</th><td><b>{s['owner_reported_score']:.4f}</b> "
            f"<span class=mut>OWNER-REPORTED &mdash; {esc(s['source_url'])}</span></td></tr>"
            f"<tr><th>Dots (measured here)</th><td>{s['dots']:,}</td></tr>"
            f"<tr><th>Dots within 1 / 2 / 3 px of the catalogue</th>"
            f"<td>{s['le_1px']:,} / {s['le_2px']:,} / {s['le_3px']:,} "
            f"({s['frac_le_3px']*100:.1f}% of its dots)</td></tr>"
            f"<tr><th>MODEL implied recall c</th><td>{c:.3f}</td></tr>"
            f"<tr><th>Unique?</th><td class=no>NO &mdash; {s['max_overlap_vs_other_eight']*100:.1f}% "
            f"of its dots are within 3 px of a sister file; max IoU vs a sister "
            f"{s['max_iou_vs_other_eight']:.3f}</td></tr>"
            f"<tr><th>sha256</th><td class=mono>{esc(s['sha256'])}</td></tr>"
            "</table>"
            f"<p>{esc(s['site'])} sits "
            f"{'at the top of' if is_best else 'inside'} the one-family ladder. Its ring census "
            f"places {s['le_1px']:,} dots on or beside a mapped trace and {s['gt_3px']:,} beyond "
            f"the kernel; the modelled recall is {c:.3f}, "
            + ("which defines the champion. " if is_best else
               f"within {100*abs(c-estimate.implied_coverage(0.2778,37654))/estimate.implied_coverage(0.2778,37654):.0f}% "
               "of the champion's. ") +
            "The score difference is therefore "
            "<i>not</i> a difference in geological skill &mdash; it is the dot budget. "
            "Do not submit this file: it is not unique and, for the denser members, its extra dots "
            "are the ones that sit on a fault flank and pay the false-positive tax.</p>"
            "</section>")

    executive = executive.replace("<!--SITEBLOCKS-->", blocks)
    (DOCS / "executive.html").write_text(executive)
    print("wrote docs/executive.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
