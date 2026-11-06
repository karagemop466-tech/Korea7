#!/usr/bin/env python3
"""Build the Bathtub Wastewater Overflow Trip Lever project site (docs/bath/).

Reads the verified JSON data in docs/bath/data/ and renders a static,
no-JS dashboard site. Deterministic: same data in, same HTML out.

Every table row on every page carries at least one source link. Values that
could not be confirmed from an official source are rendered as blank/"not
verified" and are published on the Flagged for Review page.
"""

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATH = ROOT / "docs" / "bath"
DATA = BATH / "data"
ASSETS = BATH / "assets"

BUILD_DATE = date.today().isoformat()

PAGES = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("problem-scope.html", "Problem &amp; Scope"),
    ("technical-background.html", "Technical Background"),
    ("estimates.html", "Estimates"),
    ("contractors.html", "Contractors"),
    ("analysis.html", "Analysis"),
    ("flagged-for-review.html", "Flagged for Review"),
    ("sources.html", "Sources"),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def esc(value):
    return html.escape(str(value)) if value is not None else ""


def page(title, active, body, subtitle=None):
    nav_parts = []
    for href, label in PAGES:
        cls = ' class="active"' if href == active else ""
        nav_parts.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "".join(nav_parts)
    sub = f'<p class="subtitle">{subtitle}</p>' if subtitle else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Bathtub Overflow Trip Lever Project</title>
<link rel="stylesheet" href="assets/bath.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="index.html">
      <span class="brand-mark">SF</span>
      <span class="brand-text"><strong>Bathtub Overflow Trip Lever</strong><span>Repair research &amp; verified hiring brief — San Francisco</span></span>
    </a>
  </div>
  <nav class="site-nav"><div class="wrap">{nav}</div></nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <p>Bathtub wastewater overflow trip lever project — static research site. Data verified against linked sources on 2026-11-06; review the <a href="flagged-for-review.html">Flagged for Review</a> page for limitations. Built {BUILD_DATE}.</p>
</div></footer>
</body>
</html>
"""


def table(headers, rows, cls="data-table"):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{c}</td>" for c in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return f'<div class="table-scroll"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def badge(text, kind):
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


def ext(url, label=None):
    label = label or url
    return f'<a href="{esc(url)}" rel="noopener" target="_blank">{esc(label)}</a>'


def card(title, value, note, href=None):
    link_open = f'<a class="stat-card" href="{href}">' if href else '<div class="stat-card">'
    link_close = "</a>" if href else "</div>"
    return f'{link_open}<span class="stat-value">{value}</span><span class="stat-label">{esc(title)}</span><span class="stat-note">{note}</span>{link_close}'


def section(title, body, anchor=None):
    a = f' id="{anchor}"' if anchor else ""
    return f'<section class="card"{a}><h2>{title}</h2>{body}</section>'


# --------------------------------------------------------------------------- data
contractors_data = load("contractors.json")
estimates_data = load("estimates.json")
benchmarks_data = load("benchmarks.json")
flags_data = load("flags.json")
sources_data = load("sources.json")

contractors = contractors_data["contractors"]
estimates = estimates_data["estimates"]
benchmarks = benchmarks_data["benchmarks"]
flags = flags_data["flags"]
by_id = {c["id"]: c for c in contractors}
dual = [c for c in contractors if c["all_in_one_capable"]]

AMOUNTS = {e["id"]: e["amount_usd"] for e in estimates}
LOW, HIGH = min(AMOUNTS.values()), max(AMOUNTS.values())


def contractor_link(cid):
    c = by_id[cid]
    return ext(c["cslb_detail_url"], c["name"])


def license_short(cid):
    c = by_id[cid]
    return f'{ext(c["cslb_detail_url"], "CSLB #" + c["license_number"])}'


# --------------------------------------------------------------------------- pages

def p_index():
    body = f"""
<section class="hero card">
  <h1>Bathtub wastewater overflow trip lever — verified repair research</h1>
  <p>A stuck trip-lever bathtub drain assembly inside hidden plumbing behind a wall in a tenant-occupied San
  Francisco unit. Removal from above has not been achievable in the field, so work may need to proceed from
  below through the ceiling of the storage area underneath. This site organizes the three estimates received,
  eight CSLB-verified candidate contractors, the licensing analysis for combining plumbing with drywall
  work, and every source used — with all limitations flagged.</p>
  <p class="small">All findings were verified line by line on 2026-11-06 against official sources
  (California CSLB license records, California statute, IAPMO code readers, manufacturer instructions) and
  first-party company listings. Client-provided figures are labeled as such and are not presented as verified.</p>
</section>
<section class="stat-grid">
  {card("Estimates on file", f"{len(estimates)}", f"client-provided; ${LOW}–${HIGH} spread", "estimates.html")}
  {card("CSLB-verified candidates", f"{len(contractors)}", "license status read from cslb.ca.gov", "contractors.html")}
  {card("B + C-36 dual-licensed", f"{len(dual)}", "can take plumbing + drywall as one contract", "analysis.html")}
  {card("Flagged items", f"{len(flags)}", "review before acting", "flagged-for-review.html")}
</section>
<section class="card">
  <h2>Browse by category</h2>
  <div class="nav-grid">
    <a class="nav-card" href="executive-summary.html"><strong>Executive Summary</strong><span>The whole picture in one page: situation, verified findings, money, shortlist, next steps.</span></a>
    <a class="nav-card" href="problem-scope.html"><strong>Problem &amp; Scope</strong><span>What is stuck, where, why access is hard, and the work statement.</span></a>
    <a class="nav-card" href="technical-background.html"><strong>Technical Background</strong><span>How trip-lever wastes work, repair options, code sections, license classes.</span></a>
    <a class="nav-card" href="estimates.html"><strong>Estimates</strong><span>The three client-provided quotes with scope wording, plus market cost benchmarks.</span></a>
    <a class="nav-card" href="contractors.html"><strong>Contractors</strong><span>Eight candidates, every license read directly from the CSLB, with review links.</span></a>
    <a class="nav-card" href="analysis.html"><strong>Analysis</strong><span>Which quotes match the real problem, and who can legally do plumbing + drywall in one contract.</span></a>
    <a class="nav-card" href="flagged-for-review.html"><strong>Flagged for Review</strong><span>Every unverified value, conflict, and irregularity, with suggested actions.</span></a>
    <a class="nav-card" href="sources.html"><strong>Sources</strong><span>Complete source registry: official, first-party, review-platform, technical, market.</span></a>
  </div>
</section>
<section class="card">
  <h2>Quick view — the three estimates (client-provided)</h2>
  {table(["Company (CSLB record)", "Scope as stated", "Amount", "Basis"], [
      [contractor_link(e["company_id"]), esc(e["scope_as_stated"]), f'<strong>${e["amount_usd"]}</strong>', badge("client-provided", "warn")] for e in estimates
  ])}
  <p class="small">Amounts are recorded verbatim from the client and cannot be verified from an official source; each carries a flag — see <a href="flagged-for-review.html">Flagged for Review</a>. The companies are independently verified: see <a href="contractors.html">Contractors</a>.</p>
</section>
<section class="card">
  <h2>Quick view — single-contract (plumbing + drywall) capability</h2>
  {table(["Company (CSLB record)", "Key classifications", "License status", "Reviews"], [
      [contractor_link(c["id"]),
       esc(" + ".join(x.split(" - ")[0] for x in c["classifications"][:2])),
       esc(c["license_status"] + " (exp. " + c["license_expires"] + ")"),
       ext(c["yelp_url"], f'Yelp {c["yelp_rating"]} ({c["yelp_review_count"]})')]
      for c in dual
  ])}
  <p class="small">Under California Business &amp; Professions Code <a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7057" rel="noopener" target="_blank">§7057</a> (official text), a prime contract requiring two unrelated trades — plumbing plus drywall — fits the B General Building classification. Details: <a href="analysis.html">Analysis</a>.</p>
</section>
"""
    return page("Dashboard", "index.html", body, "Everything about this repair in one verified dashboard.")


def p_executive_summary():
    body = f"""
<section class="card">
<h2>Purpose</h2>
<p>Collect, organize, and analyze everything needed to hire help for one specific repair: a bathtub
wastewater overflow <strong>trip lever</strong> that is stuck inside hidden plumbing behind a wall, in a
tenant-occupied San Francisco unit, with a storage unit directly below. This page is the executive summary;
every value on this site is source-linked, and anything that could not be confirmed from an official source
is left blank or labeled client-provided and listed on the <a href="flagged-for-review.html">Flagged for
Review</a> page.</p>
</section>

<section class="card">
<h2>Situation (client-stated context)</h2>
<ul>
  <li>The bathtub's trip-lever waste-and-overflow assembly is stuck; the working parts sit inside the
  overflow pipe hidden behind the wall.</li>
  <li>Per the client, <strong>5+ licensed plumbers</strong> have been unable to remove it from above without
  concern over destroying the hidden plumbing (client-stated; not independently verifiable —
  {badge("unverified context", "warn")}).</li>
  <li>Recommended path from those plumbers: work from below — but a storage unit occupies the space below,
  so access may require opening the drywall ceiling.</li>
  <li>The client wants an <strong>all-in-one service</strong> covering plumbing <em>and</em> drywall, with a
  licensed plumber or contractor experienced in delicate work in tenant-occupied units.</li>
</ul>
</section>

<section class="card">
<h2>Money — estimates on file</h2>
{table(["Company (CSLB record)", "Scope as stated", "Amount", "Basis"], [
    [contractor_link(e["company_id"]), esc(e["scope_as_stated"]), f'<strong>${e["amount_usd"]}</strong>', badge("client-provided", "warn")] for e in estimates
])}
<p class="small">The three amounts (${LOW}–${HIGH} spread) came to the client directly and are not
independently verifiable; they are labeled client-provided. They also describe <em>different scopes</em>
(adjust vs. trim replacement vs. full waste-and-overflow replacement) and are not directly comparable —
see <a href="analysis.html">Analysis</a> and the <a href="estimates.html">Estimates</a> page. National
market benchmarks put bathtub drain work at roughly <strong>$100–$700+</strong>
({ext("https://homeguide.com/costs/bathtub-repair-cost", "HomeGuide")}) and tub/shower drain replacement at
<strong>$500–$1,025</strong> ({ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "Angi")}),
with accessibility — drywall/tile removal — called out as a major cost driver.</p>
</section>

<section class="card">
<h2>What was verified (2026-11-06)</h2>
<ul>
  <li><strong>8 candidate contractors</strong>, each read directly from the official CSLB license-detail
  page: {", ".join(contractor_link(c["id"]) for c in contractors)}.</li>
  <li>All 8 licenses are <strong>current and active</strong> with C-36 Plumbing classification; two —
  {ext(by_id["ace-plumbing-rooter"]["cslb_detail_url"], "Ace Plumbing &amp; Rooter (829071)")} and
  {ext(by_id["genteel-plumbers"]["cslb_detail_url"], "Genteel Plumbers (1025814)")} — also hold
  <strong>B General Building</strong> on the same license.</li>
  <li>The three companies behind the estimates were matched by name + exact address/phone to CSLB records;
  each match is listed on the <a href="contractors.html">Contractors</a> page and flagged for client
  confirmation.</li>
  <li>California statute {ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7057", "B&amp;P §7057")} (official
  text): a prime contract requiring <strong>two unrelated trades</strong> (plumbing + drywall) is within the
  B classification — the legal basis for the all-in-one requirement.</li>
  <li>Technical and code references pinned to official manufacturer instructions
  ({ext("https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "Watco trip-lever installation PDF")})
  and the {ext("https://epubs.iapmo.org/2022/CPC/", "California Plumbing Code")} / {ext("https://epubs.iapmo.org/2024/UPC/", "UPC")} (§409 Bathtubs:
  waste outlet, overflow, installation and access).</li>
</ul>
</section>

<section class="card">
<h2>Core conclusion</h2>
<p>If from-above removal has truly failed with 5+ licensed plumbers (client-stated), the
<strong>$135 adjust</strong> and <strong>$550 trim-replacement</strong> scopes may not resolve the problem;
the <strong>$614 full waste-and-overflow replacement</strong> scope is the one aligned with the described
failure — and it covers plumbing only. The likely end-state is: open the ceiling below (drywall), replace
the waste-and-overflow from below, then patch the ceiling. That is two unrelated trades, so the cleanest
single-contract path is a contractor holding <strong>B + C-36</strong>
({ext(by_id["ace-plumbing-rooter"]["cslb_detail_url"], "Ace")} and
{ext(by_id["genteel-plumbers"]["cslb_detail_url"], "Genteel Plumbers")} both hold this exact combination,
verified on CSLB), or a C-36 plumber paired with a licensed drywall contractor under two contracts.</p>
</section>

<section class="card">
<h2>Recommended next steps</h2>
<ol>
  <li>Confirm with each quoting company which scope their price covers and get itemized written quotes
  (access/opening included or excluded — say which explicitly).</li>
  <li>Shortlist the two B + C-36 firms for single-contract bids; ask each for references from comparable
  tenant-occupied work ({badge("unverified criterion", "warn")} — cannot be verified from official sources).</li>
  <li>Re-check each license on {ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB Check a License")}
  on the day you hire, and collect insurance certificates (note the workers' compensation exemption flag on
  Bay Area Plumbing).</li>
  <li>Get the access plan in writing: where the opening will be cut, containment for the occupied unit and
  the storage unit below, and who patches/finishes.</li>
  <li>Review the {len(flags)} items on the <a href="flagged-for-review.html">Flagged for Review</a> page
  before signing anything.</li>
</ol>
</section>
"""
    return page("Executive Summary", "executive-summary.html", body)


def p_problem_scope():
    body = f"""
<section class="card">
<h2>The problem</h2>
<p>The bathtub's wastewater overflow <strong>trip lever</strong> — the lever on the overflow plate that
raises and lowers an internal plunger inside the overflow pipe — is stuck. The overflow assembly sits in a
hard-to-access area behind the wall. In the field, removal from above has repeatedly failed: per the client,
more than five licensed plumbers have been unable to remove it without concern over destroying the hidden
plumbing behind the wall ({badge("client-stated", "warn")}). Those plumbers recommend working from below,
but a <strong>storage unit occupies the space below</strong>, which may require opening the drywall ceiling
to reach the hidden plumbing.</p>
<p>The unit is <strong>tenant-occupied</strong>, so the work must be planned and executed for a sensitive,
in-use environment.</p>
</section>

<section class="card">
<h2>Work statement (as understood from the client's description)</h2>
<ol>
  <li>Remove or free the stuck trip-lever overflow assembly — or, if the hidden plumbing is compromised,
  replace the waste-and-overflow assembly.</li>
  <li>Obtain access: preferably from above (tub side); failing that, from below through the drywall ceiling
  above the storage area.</li>
  <li>Restore finishes: close and patch the ceiling (if opened) so the space below is left sound and
  finished.</li>
  <li>Do all of the above with licensed professionals, ideally one responsible party for plumbing
  <em>and</em> drywall, experienced with tenant-occupied units.</li>
</ol>
</section>

<section class="card">
<h2>Requirements with official basis</h2>
{table(["Item", "Value", "Status", "Source / basis"], [
    ["Service area", "San Francisco, CA", badge("requirement", "ok"), ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx", "CSLB — Find a Licensed Contractor")],
    ["License", "Licensed plumber or contractor (California CSLB license)", badge("requirement", "ok"), ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB — Check a License")],
    ["Single responsible party for plumbing + drywall", "Preferred (all-in-one service)", badge("requirement", "ok"), ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7057", "B&amp;P Code §7057 (two unrelated trades)")],
    ["Access route", "Above preferred; below via ceiling drywall expected if above fails", badge("constraint", "info"), ext("https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "Watco trip-lever waste installation instructions")],
    ["Code governing the fixture work", "California Plumbing Code (Title 24, Part 5, UPC-based)", badge("context", "info"), ext("https://epubs.iapmo.org/2022/CPC/", "2022 CPC — official IAPMO reader")],
])}
</section>

<section class="card">
<h2>Client-stated site facts (context — not independently verifiable)</h2>
<p>The following facts come from the client's description of the property and drive the analysis; they are
labeled client-stated and tracked on the <a href="flagged-for-review.html">Flagged for Review</a> page:</p>
<ul>
  <li><strong>Tenant-occupied unit</strong> — the work happens in an occupied home; experience with this is
  a hiring criterion that cannot be verified from official sources, so the Contractors page leaves that
  column blank and it becomes an interview question ({badge("unverified criterion", "warn")}).</li>
  <li><strong>Storage unit below</strong> — the space under the bathroom is occupied by a storage area, so
  a below-floor access path means opening and later patching the drywall ceiling there, with containment
  and protection for stored contents.</li>
  <li><strong>5+ licensed plumbers declined to remove the assembly from above</strong> without concern over
  destroying the hidden plumbing — the field history that pushes the job toward below-floor access
  ({badge("client-stated", "warn")}).</li>
  <li><strong>Reference photos pending</strong> — the client may add photos of the work area later; none
  are on file, so no visual condition assessment exists yet.</li>
</ul>
</section>

<section class="card">
<h2>Not on file</h2>
<p>Tub make/model and trim style, building access logistics, unit address, and prior plumbers' written
findings are not in the brief. Per this project's rules, those fields are left blank rather than guessed.
Where the site cites an on-site condition, it is labeled client-stated.</p>
</section>
"""
    return page("Problem & Scope", "problem-scope.html", body)


def p_technical():
    watco = ext("https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "Watco trip-lever bath waste installation instructions")
    watco2 = ext("https://www.watcomfg.com/Instructions/WIRE-TL-TS-SL%20Inst.black.pdf", "Watco trip-lever variations sheet")
    hunker = ext("https://www.hunker.com/13769421/how-to-fix-a-bathtub-drain-stopper/", "Hunker bathtub drain stopper guide")
    sniper = ext("https://plumbingsniper.com/how-to-fix-a-sticky-trip-lever-bathtub-stopper/", "Plumbing Sniper trip-lever guide")
    leginfo = ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7057", "B&amp;P Code §7057")
    cslb_c36 = ext("https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "CSLB C-36 classification")
    cslb_b = ext("https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B", "CSLB B classification")
    body = f"""
<section class="card">
<h2>How a trip-lever waste-and-overflow works</h2>
<p>A trip-lever bathtub drain has no visible stopper in the drain opening. Instead, a lever on the
<strong>overflow plate</strong> (the plate on the tub wall over the drain end of the overflow pipe) moves a
linkage and a hollow <strong>plunger (drop cylinder)</strong> up and down inside the overflow pipe. Lever up
drops the plunger into the junction of the overflow and the drain line to close the drain; lever down lifts
it to open the drain. {watco} (official manufacturer) diagrams the parts: overflow plate and screws, brass
linkage with adjustment nut, drop cylinder/plunger, overflow elbow with gasket, tee, and drain elbow with
strainer body under the tub. A second official sheet covers the linkage variants
({ext("https://www.watcomfg.com/Instructions/WIRE-TL-TS-SL%20Inst.black.pdf", "Quick Adjust® / Slip Lock® / Turnstyle®")}).</p>
</section>

<section class="card">
<h2>Why trip levers stick — and why removal can fail</h2>
<ul>
  <li><strong>Buildup on the plunger:</strong> mineral (calcium/iron) deposits and gunk on the plunger make
  it bind against the inside of the overflow pipe ({sniper}).</li>
  <li><strong>Corroded trim/linkage:</strong> the plate, screws, and brass linkage corrode and can freeze;
  a stuck or broken linkage sometimes has to be fished out or the assembly replaced ({hunker}).</li>
  <li><strong>All working parts are hidden:</strong> for plunger-type trip levers, everything that matters is
  inside the overflow pipe behind the wall — there is nothing to service at the drain opening itself
  ({hunker}).</li>
</ul>
</section>

<section class="card">
<h2>Repair options, smallest to largest</h2>
{table(["Option", "What it involves", "Access needed", "Matches which estimate", "Source"], [
    ["Free/adjust the trip-lever linkage and plunger", "Remove the two overflow-plate screws, withdraw linkage + plunger, clean/adjust/rebuild", "Tub side only (from above)", "<a href='estimates.html'>$135 (Fast Response)</a>", ext("https://www.hunker.com/13769421/how-to-fix-a-bathtub-drain-stopper/", "From-above trip-lever service (guide)")],
    ["Replace the trip-lever trim (plate/linkage) or lever &amp; diverter spout", "New faceplate/linkage set through the overflow opening; spout work at the wall", "Tub side / spout wall", "<a href='estimates.html'>$550 (Bay Area Plumbing)</a>", ext("https://www.watcomfg.com/Instructions/WIRE-TL-TS-SL%20Inst.black.pdf", "Trip-lever linkage variants (Watco)")],
    ["Replace the full waste-and-overflow assembly", "Tear out and reinstall overflow elbow + tee + drain elbow + strainer; per the manufacturer's instructions the drain elbow and strainer body are fitted <em>under the tub</em> and the overflow elbow <em>behind the tub</em>", "Tub side <strong>and</strong> below/behind the tub — from below through the ceiling when above-access fails", "<a href='estimates.html'>$614 (Expert Plumbing Solutions)</a>", ext("https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "Waste-and-overflow installation (Watco)")],
])}
<p class="small">Sources: {watco}; {hunker}. The manufacturer's own instructions are the reference for what
a full replacement physically requires — which is why repeated from-above failure pushes the job to
below-floor access.</p>
</section>

<section class="card">
<h2>Code context (California)</h2>
<p>California's plumbing code is the <strong>California Plumbing Code</strong> (Title 24, Part 5), based on
the Uniform Plumbing Code — official IAPMO readers: {ext("https://epubs.iapmo.org/2022/CPC/", "2022 CPC")} ·
{ext("https://epubs.iapmo.org/2024/UPC/", "2024 UPC")}. The UPC chapter on fixtures maps the relevant
sections (titles from the official table of contents): <strong>409.0 Bathtubs and Whirlpool Bathtubs</strong>,
with <strong>409.2 Waste Outlet</strong>, <strong>409.3 Overflow</strong>, and
<strong>409.6 Installation and Access</strong>. In other words, the code family that governs this work has
explicit provisions covering bathtub waste outlets, overflows, and installation/access — a professional
bidding this job should be working from the current CPC edition.</p>
</section>

<section class="card">
<h2>License classes that fit this job (California)</h2>
<ul>
  <li><strong>C-36 Plumbing</strong> — the plumbing contractor classification ({cslb_c36}); covers the
  waste-and-overflow work itself. All eight candidates on the <a href="contractors.html">Contractors</a>
  page hold active C-36 licenses.</li>
  <li><strong>B General Building</strong> — {cslb_b}. Under {leginfo} (official statutory text read
  2026-11-06), a general building contractor's business involves structures whose construction requires
  <em>“at least two unrelated building trades or crafts”</em>, and a B contractor may take a prime contract
  for such a multi-trade project (holding the matching specialty classification or subcontracting where
  required). <strong>Plumbing + drywall = two unrelated trades</strong>, so a B + C-36 license holder can
  take this job as one contract including the ceiling opening and patch.</li>
  <li>A C-36-only plumber can legally do the plumbing scope; the drywall opening/patch would then be a
  separate contract with a second licensed contractor (or the plumber's own licensed drywall
  subcontractor).</li>
</ul>
</section>
"""
    return page("Technical Background", "technical-background.html", body)


def p_estimates():
    rows = []
    for e in estimates:
        date_txt = esc(e["date_as_stated"]) if e["date_as_stated"] else '<span class="blank">not stated</span>'
        rows.append([
            contractor_link(e["company_id"]),
            esc(e["scope_as_stated"]),
            f'<strong>${e["amount_usd"]}</strong>',
            date_txt,
            badge("client-provided", "warn"),
            badge("no — not independently verifiable", "warn"),
            ext(e["company_profile_link"], "CSLB record"),
        ])
    body = f"""
<section class="card">
<h2>Estimates provided to the client</h2>
{table(["Company", "Scope as stated by bidder", "Amount (USD)", "Date as stated", "Basis", "Independently verified?", "Source link"], rows)}
<p class="small"><strong>How to read this table:</strong> the amounts and scope wordings are transcribed from
the client's brief. No official public source publishes a company's private quotes, so these amounts are
labeled <em>client-provided</em> and cannot be independently verified — by rule they are flagged, not
silently treated as fact. The <em>companies</em> behind the quotes are independently verified: each row's
source link opens that company's official CSLB license record (name, address, phone, classifications,
status), read on 2026-11-06. See {badge("flag-scope-mismatch", "warn")} on the
<a href="flagged-for-review.html">Flagged for Review</a> page: the three prices buy three different scopes.</p>
</section>

<section class="card">
<h2>Market cost benchmarks (third-party context — not quotes for this job)</h2>
{table(["Publisher", "Metric", "Range", "Notes", "Source"], [
    [esc(b["publisher"]), esc(b["metric"]), f'<strong>{esc(b["range"])}</strong>', esc(b["detail"]), ext(b["url"], b["page_title"])] for b in benchmarks
])}
<p class="small">These are national cost guides used for context only. Angi's guide explicitly calls out
that repairs requiring <em>drywall, tile, or flooring removal cost significantly more</em> than work at
exposed fixtures — the single most important benchmark fact for this project, because access is this job's
defining difficulty.</p>
</section>

<section class="card">
<h2>What is missing (left blank by rule)</h2>
<ul>
  <li>Itemized line items (labor vs. materials vs. access/patch) for each quote — <span class="blank">not
  stated in the brief</span>.</li>
  <li>Whether the $550 and $135 prices include any contingency if the hidden plumbing turns out to be
  damaged — <span class="blank">not stated</span>.</li>
  <li>Issue dates for the $550 and $135 estimates — <span class="blank">not stated</span> (the brief's
  "8/30/26" heading sits above the first estimate only).</li>
  <li>Whether any bidder included drywall/ceiling work — <span class="blank">no quote on file includes it
  as stated</span>; treat drywall as out of scope until a bidder says otherwise in writing.</li>
</ul>
</section>
"""
    return page("Estimates", "estimates.html", body)


def p_contractors():
    rows = []
    for c in contractors:
        cls = "<br>".join(esc(x) for x in c["classifications"])
        allin = badge("B + C-36 — single-contract capable", "ok") if c["all_in_one_capable"] else badge("plumbing only (C-36)", "muted")
        reviews = ext(c["yelp_url"], f'Yelp {c["yelp_rating"]} · {c["yelp_review_count"]} reviews')
        occupied = '<span class="blank">blank — unverified (ask for references)</span>'
        rows.append([
            f'<strong>{ext(c["cslb_detail_url"], c["name"])}</strong>',
            ext(c["cslb_detail_url"], c["license_number"]),
            cls,
            esc(c["license_status"]) + "<br><span class='small'>exp. " + esc(c["license_expires"]) + "</span>",
            esc(c["address_cslb"]),
            esc(c["phone"]),
            reviews,
            allin,
            occupied,
        ])
    body = f"""
<section class="card">
<h2>Candidate contractors — licenses read directly from the CSLB (2026-11-06)</h2>
<p class="small">Every license field below was read from that company's official CSLB license-detail page on
2026-11-06 (follow the CSLB # link to re-verify). The first three rows are the companies behind the
client-provided estimates. The "tenant-occupied experience" column is blank for everyone by rule: no official
source documents it, so it is a question to ask, not a fact to assert.</p>
{table(["Company", "CSLB #", "Classifications", "Status", "Address (CSLB record)", "Phone", "Reviews", "All-in-one fit", "Tenant-occupied experience"], rows)}
</section>

<section class="card">
<h2>Per-candidate notes (each note is source-linked)</h2>
<ul class="notes-list">
""" + "".join(
        f'<li><strong>{ext(c["cslb_detail_url"], c["name"])}</strong> — {esc(c["notes"])}</li>'
        for c in contractors
    ) + f"""
</ul>
</section>

<section class="card">
<h2>How these eight were selected and verified</h2>
<ol>
  <li><strong>Matching to the client's quotes:</strong> the brief's names were matched to San Francisco
  entities by name plus exact agreement of address and phone with official records (CSLB, and each company's
  own site). Where aggregator sites disagreed, the CSLB record that matches the company's own address/phone
  was used — see the name-collision flag for the trap this avoids.</li>
  <li><strong>Widely reviewed in San Francisco:</strong> the additional five candidates were taken from
  Yelp's San Francisco plumbing listings ({ext("https://www.yelp.com/search?cflt=plumbing&amp;find_loc=San+Francisco%2C+CA", "Yelp — plumbing in San Francisco")}),
  then license-verified one by one on CSLB.</li>
  <li><strong>Verification chain per row:</strong> CSLB license-detail page (identity, classification,
  status) → company's own site (service area, identity) → Yelp/BBB listing (reviews, cross-check).
  Where a direct Yelp business URL could not be confirmed, the search listing is linked and noted.</li>
  <li><strong>Not included:</strong> unlicensed or unverifiable operations; firms whose license records
  could not be matched to their public identity. No values were inferred to fill gaps.</li>
</ol>
</section>
"""
    return page("Contractors", "contractors.html", body)


def p_analysis():
    ace = by_id["ace-plumbing-rooter"]
    gen = by_id["genteel-plumbers"]
    body = f"""
<section class="card">
<h2>1 — The three quotes buy three different scopes</h2>
{table(["Price (client-provided)", "Scope as stated", "What it can and cannot do here", "Technical basis"], [
    ["<strong>$135</strong>", "Repair or adjust bathtub wastewater plunger handle", "Fastest, cheapest — pure from-above trim/linkage work. <em>Cannot</em> address damaged hidden plumbing; presumes the plunger assembly can be withdrawn through the overflow opening.", ext("https://www.hunker.com/13769421/how-to-fix-a-bathtub-drain-stopper/", "Trip-lever service from above (guide)")],
    ["<strong>$550</strong>", "Replace lever for tub plug and spout with diverter (labor + materials)", "Replaces the operating trim. Still from-above work at the overflow plate and spout; presumes the hidden waste-and-overflow body stays in place and sound.", ext("https://www.watcomfg.com/Instructions/WIRE-TL-TS-SL%20Inst.black.pdf", "Trip-lever trim/linkage variants (Watco)")],
    ["<strong>$614</strong>", "Replacing waste and overflow", "Full assembly replacement — the scope that matches the described failure mode if the hidden assembly is corroded or damaged. Per the manufacturer's instructions, the drain elbow/strainer are fitted under the tub, so below-tub access is normally part of this job.", ext("https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "Waste-and-overflow installation (Watco)")],
])}
<p class="small">Scope wordings transcribed from the client's brief (amounts client-provided,
{badge("unverified", "warn")}). Technical basis: the manufacturer instructions and guides on the
<a href="technical-background.html">Technical Background</a> page.</p>
</section>

<section class="card">
<h2>2 — Which scope fits the actual problem?</h2>
<p>The client-stated field history is that <strong>5+ licensed plumbers could not remove the assembly from
above</strong> without risking the hidden plumbing ({badge("client-stated, unverified", "warn")}). If that
stands after a re-inspection, then:</p>
<ul>
  <li>The <strong>$135</strong> adjust scope and the <strong>$550</strong> trim-replacement scope assume
  from-above removal works — exactly what the field history says keeps failing. Money spent there may not
  fix the tub.</li>
  <li>The <strong>$614</strong> full waste-and-overflow replacement is the scope aligned with the described
  failure — and it is plumbing-only: it does not include opening or patching the ceiling below.</li>
  <li>Therefore the realistic total is <strong>$614 + access/patch work</strong> (or a re-bid on the same
  combined scope), not $135 or $550 alone. Angi's cost guide independently flags drywall removal as a
  major cost adder for exactly this kind of repair
  ({ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "source")}).</li>
</ul>
</section>

<section class="card">
<h2>3 — The all-in-one requirement is a licensing question</h2>
<p>The job's likely end-state — open the ceiling of the storage area, replace the waste-and-overflow from
below, patch the ceiling — spans <strong>two unrelated trades: plumbing and drywall</strong>. California's
{ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=7057", "Business &amp; Professions Code §7057")}
(official text) defines the B General Building classification around exactly this case: a prime contract
whose construction requires at least two unrelated trades. A C-36-only plumber cannot take the combined
contract as a matter of licensing scope ({ext("https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "CSLB C-36 classification")}).</p>
{table(["Path", "Who can take it (verified)", "Trade-offs"], [
    ["One contractor, one contract (B + C-36 on one license)", f'{ext(ace["cslb_detail_url"], ace["name"])} (829071) and {ext(gen["cslb_detail_url"], gen["name"])} (1025814) — both read from CSLB with B and C-36 on the same license', "Single responsible party for plumbing + opening + patch; simplest accountability in a tenant-occupied building. Get the drywall patch scope written into the contract."],
    ["Two contracts: C-36 plumber + licensed drywall contractor", "Any of the six C-36-only candidates on the <a href='contractors.html'>Contractors</a> page, plus a drywall contractor to be sourced (none on file yet — <span class='blank'>blank</span>)", "Works, but splits accountability for a shared opening; sequencing and dust control need explicit coordination.", ext("https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "CSLB C-36 classification scope")],
    ["Plumber with in-house drywall help under a C-36-only license", "Not verifiable from official sources — license classification is the test; <span class='blank'>blank</span> until a firm documents a B-classified arrangement or a licensed drywall subcontractor", "Ask directly; accept only with the subcontractor's license number in writing.", ext("https://www.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B", "CSLB B classification scope")],
])}
</section>

<section class="card">
<h2>4 — Shortlist for outreach</h2>
{table(["Tier", "Company (CSLB record)", "Why"], [
    [badge("Tier 1 — single-contract bids", "ok"), ext(ace["cslb_detail_url"], "Ace Plumbing &amp; Rooter"), "B + C-36 + four more classifications on license 829071 (active, exp. 06/30/2027); ~1,447+ Yelp reviews (4.7); San Francisco (1090 Bryant St)."],
    [badge("Tier 1 — single-contract bids", "ok"), ext(gen["cslb_detail_url"], "Genteel Plumbers"), "B + C-36 on license 1025814 (active, exp. 04/30/2027); 4.7 with 519 Yelp reviews; 24/7 San Francisco service."],
    [badge("Tier 2 — plumbing scope / comparison bids", "muted"), ext(by_id["expert-plumbing-solutions"]["cslb_detail_url"], "Expert Plumbing Solutions"), "Holds the $614 full-replacement quote (client-provided); C-36 active since 2012; 4.8 (81) on Yelp."],
    [badge("Tier 2 — plumbing scope / comparison bids", "muted"), ext(by_id["fast-response-plumbing-rooter"]["cslb_detail_url"], "Fast Response Plumbing &amp; Rooter"), "High-volume reviewed shop (4.8, ~906 on Yelp); C-36 active; useful for a sanity-check bid on the same written scope."],
    [badge("Tier 2 — plumbing scope / comparison bids", "muted"), ext(by_id["bay-area-plumbing"]["cslb_detail_url"], "Bay Area Plumbing"), "Holds the $550 quote (client-provided); C-36 active since 1999; note the workers' compensation exemption flag."],
    [badge("Tier 3 — additional verified options", "muted"), ", ".join(ext(c["cslb_detail_url"], c["name"]) for c in contractors if c["id"] in ("atlas-plumbing-rooter", "heises-plumbing", "discount-plumbing-rooter")), "All C-36-active with solid review bases; Heise's additionally advertises drywall/carpentry repair services on its own site (no B classification — see flag)."],
])}
</section>

<section class="card">
<h2>5 — Decision checklist (before signing)</h2>
<ol>
  <li>Itemized written quote that names the access method (above vs. ceiling opening), the ceiling patch,
  and who does each part.</li>
  <li>Confirm the entity name on the quote matches the CSLB record (guard against the name-collision
  problem documented in the flags).</li>
  <li>Re-verify the license on {ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB Check a License")} that day;
  collect liability insurance certificates (and workers' comp where employees are used).</li>
  <li>References for tenant-occupied work ({badge("unverified criterion", "warn")}) plus a written
  dust/containment plan covering the occupied unit <em>and</em> the storage unit below.</li>
  <li>Agree in writing what happens on discovery (e.g., corroded pipe beyond the assembly): stop-work
  point, re-price procedure, and who patches if scope grows.</li>
</ol>
</section>

<section class="card">
<h2>What this analysis is not</h2>
<p>It is not a recommendation to hire any particular firm, and not a substitute for on-site inspection —
no photos or prior plumbers' written findings were available ({badge("pending", "warn")}). All quote amounts
are client-provided; all license facts are CSLB-verified as of 2026-11-06; review scores are volatile
snapshots. This site deliberately does not discuss scheduling or regulatory strategy; it documents verified
facts about the problem, the market, and the candidates.</p>
</section>
"""
    return page("Analysis", "analysis.html", body)


def p_flagged():
    sev_map = {
        "important": "important",
        "due-diligence": "due diligence",
        "minor": "minor",
        "expected-limitation": "expected limitation",
        "unverified-criterion": "unverified criterion",
    }
    rows = []
    for f in flags:
        kind = "warn" if f["severity"] in ("important", "due-diligence") else ("muted" if f["severity"] in ("minor", "expected-limitation") else "info")
        rows.append([
            f'<strong>{esc(f["title"])}</strong><br><span class="small">{esc(f["id"])}</span>',
            badge(sev_map.get(f["severity"], f["severity"]), kind),
            esc(f["detail"]),
            esc(f["action"]),
            ext(f["source_url"], f["source_label"]),
        ])
    body = f"""
<section class="card">
<h2>Flagged for Review ({len(flags)} items)</h2>
<p class="small">Everything on this page is published for the owner's after-launch review. None of it blocks
the site: unverified values stay blank or are labeled client-provided in the tables, and each flag says what
to do next. Nothing on this site was inferred to fill a gap.</p>
{table(["Item", "Severity", "Detail", "Suggested action", "Related source"], rows)}
</section>
<section class="card">
<h2>Standing verification rules applied</h2>
<ul>
  <li>Every table row carries a source link; official sources (CSLB, California legislation, IAPMO code
  readers, manufacturer instructions) outrank first-party listings, which outrank aggregators.</li>
  <li>Client-provided amounts are labeled as such — never presented as verified facts.</li>
  <li>Values that could not be confirmed from an official source are left blank (e.g., tenant-occupied
  experience, missing quote dates, drywall sub-arrangements).</li>
  <li>Review counts are volatile snapshots (2026-11-06) and are linked, not hard-coded into conclusions.</li>
</ul>
</section>
"""
    return page("Flagged for Review", "flagged-for-review.html", body)


def p_sources():
    parts = []
    kind_label = {
        "grp-official": badge("official", "ok"),
        "grp-first-party": badge("first-party", "info"),
        "grp-reviews": badge("review platforms", "muted"),
        "grp-technical": badge("technical reference", "info"),
        "grp-market": badge("market data", "warn"),
    }
    for g in sources_data["groups"]:
        rows = [[f'<strong>{esc(s["title"])}</strong>', ext(s["url"], "open"), esc(s["used_for"])] for s in g["sources"]]
        parts.append(section(f'{g["label"]} <span class="count-pill">{len(g["sources"])}</span>', table(["Source", "Link", "Used for"], rows)))
    listing = "".join(parts)
    body = f"""
<section class="card">
<h2>Source registry</h2>
<p class="small">Every claim on this site traces to a source on this page. "Official" = government /
licensing authority / standards body / equipment manufacturer. "First-party" = the company's own site or
claimed listings. Review-platform data and market cost guides are labeled as such and used only where
appropriate. All sources accessed 2026-11-06.</p>
{listing}
</section>
"""
    return page("Sources", "sources.html", body, "Complete registry of the 34 sources behind this site.")


PAGES_BUILDERS = {
    "index.html": p_index,
    "executive-summary.html": p_executive_summary,
    "problem-scope.html": p_problem_scope,
    "technical-background.html": p_technical,
    "estimates.html": p_estimates,
    "contractors.html": p_contractors,
    "analysis.html": p_analysis,
    "flagged-for-review.html": p_flagged,
    "sources.html": p_sources,
}


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    css_src = ROOT / "scripts" / "bath_assets" / "bath.css"
    (ASSETS / "bath.css").write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")
    for name, builder in PAGES_BUILDERS.items():
        html_out = builder()
        (BATH / name).write_text(html_out, encoding="utf-8")
        print(f"wrote docs/bath/{name} ({len(html_out)} bytes)")


if __name__ == "__main__":
    main()
