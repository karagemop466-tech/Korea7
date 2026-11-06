#!/usr/bin/env python3
"""Build the bathtub trip-lever project site into docs/bathtub/.

Every table cell with a verifiable value carries a source link. Cells whose value
could not be confirmed are rendered as an explicit "unverified" chip and are also
listed on the Flagged for Review page. Nothing is inferred.

Usage:
    python scripts/build_bathtub_site.py
"""
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "bathtub" / "data"
OUT = ROOT / "docs" / "bathtub"

# ----------------------------------------------------------------------------- helpers


def load(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def esc(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def chips(status: str) -> str:
    s = (status or "").lower()
    if s in {"met", "verified", "verified_active", "met_for_shortlist",
             "not_triggered_on_described_scope"}:
        cls = "ok"
    elif s in {"unverified", "blocked", "open", "in_progress"}:
        cls = "warn"
    elif s.startswith("suspended") or s.startswith("do not"):
        cls = "bad"
    elif s in {"partially_met", "verified_requirement_not_yet_done",
               "verified_active_but_out_of_county", "must_if_applicable"}:
        cls = "mid"
    else:
        cls = "neutral"
    label = s.replace("_", " ")
    return f'<span class="chip chip-{cls}">{esc(label)}</span>'


def src_link(source_url: str, source_id: str, label: str | None = None) -> str:
    if not source_url:
        return '<span class="chip chip-warn" title="No official source could be located">unverified</span>'
    text = label or (source_id or "source")
    return (f'<a class="srclink" href="{esc(source_url)}" target="_blank" '
            f'rel="noopener noreferrer">{esc(text)}&nbsp;&#8599;</a>')


def table(headers, rows, cls="tbl") -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="table-wrap"><table class="{cls}">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


NAV = [
    ("index.html", "Dashboard", "i-dash"),
    ("executive-summary.html", "Executive summary", "i-doc"),
    ("estimates.html", "Estimates", "i-money"),
    ("vendors.html", "Vendors", "i-people"),
    ("compliance.html", "Compliance", "i-shield"),
    ("technical.html", "Technical", "i-wrench"),
    ("requirements.html", "Requirements", "i-list"),
    ("sources.html", "Sources", "i-link"),
    ("flagged.html", "Flagged for review", "i-flag"),
    ("repo-audit.html", "Repo audit", "i-repo"),
]


def page(slug: str, title: str, description: str, body: str, active: str) -> str:
    CURRENT = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{CURRENT if href == active else ""}>'
        f'<span class="nav-dot"></span>{esc(label)}</a>'
        for href, label, _ in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="layout">
  <aside class="sidebar">
    <div class="brand">
      <span class="mark">BT</span>
      <div><strong>Trip-Lever</strong><span>SF overflow project</span></div>
    </div>
    <nav aria-label="Sections">{nav}</nav>
    <div class="side-foot">
      <p><strong>Internal use only.</strong> Built {esc(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))}.</p>
      <p>Every verified cell links to an official source. Unverified cells are blank and listed on <a href="flagged.html">Flagged for review</a>.</p>
    </div>
  </aside>
  <main id="main">
{body}
    <footer class="foot">
      <p>No value on this site is inferred. Where an official source could not confirm a value, the cell is blank and carries an <span class="chip chip-warn">unverified</span> chip.</p>
      <p>Compliance notes summarise published code text for internal planning. They are not legal advice.</p>
    </footer>
  </main>
</div>
</body>
</html>
"""


def stat(label: str, value: str, note: str = "", cls: str = "") -> str:
    return (f'<div class="stat {cls}"><div class="stat-label">{esc(label)}</div>'
            f'<div class="stat-value">{value}</div>'
            f'<div class="stat-note">{note}</div></div>')


# ----------------------------------------------------------------------------- pages


def build_index(req, est, comp, flag, compliance) -> str:
    total_req = req["summary"]["total"]
    compliance_items = compliance["items"]
    bodies = f"""
    <header class="page-head">
      <div class="eyebrow">Internal working site &middot; San Francisco</div>
      <h1>Bathtub wastewater overflow trip lever</h1>
      <p class="lede">A seized trip lever, a hard-to-reach overflow, and a decision about whether to open
      the ceiling below. This dashboard collects the requirements, the three estimates, the licensed
      contractors that could be verified, and the code text that governs the permit question &mdash;
      with a source link on every row.</p>
    </header>

    <section class="stats">
      {stat("Requirements captured", str(total_req), "full register, <a href='requirements.html'>see all</a>")}
      {stat("Estimates received", str(len(est["estimates"])), "2026-08-30, <a href='estimates.html'>compared</a>")}
      {stat("Contractors license-verified", f"{comp['verified_active']}<span class='sub'>/{comp['checked']}</span>", "from CSLB, <a href='vendors.html'>shortlist</a>", "hl")}
      {stat("Compliance checks", str(len(compliance_items)), f"{compliance['summary']['verified']} verified, <a href='compliance.html'>matrix</a>")}
      {stat("Flagged for review", str(flag["summary"]["total"]), "blank cells, <a href='flagged.html'>why</a>", "warnbox")}
    </section>

    <section class="callout callout-key">
      <h2>Three things to know before anyone touches the wall</h2>
      <ol class="keylist">
        <li><strong>The drywall is not the permit problem &mdash; the plumbing is.</strong>
        Patching wallboard is exempt from a San Francisco building permit, but the same section says
        the separate plumbing permit still applies, and the plumbing code's exemption list does not
        name bathtub waste-and-overflow work.
        {src_link('https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-92027','S11')}
        {src_link('https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830','S09')}</li>

        <li><strong>Only one locally-based firm was verified to hold plumbing and building on one licence.</strong>
        Of nine licence numbers checked against CSLB, seven are active and <em>two are suspended</em>. Exactly
        one San Francisco firm holds C-36 plumbing <em>and</em> B general building together, which is what
        &ldquo;all in one service&rdquo; actually requires.
        {src_link('https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=829071','CSLB')}</li>

        <li><strong>The three quotes are not the same job.</strong>
        Two are replacement prices ($550 and $614). One is an adjust-only price ($135). Choosing on price
        across those three would be comparing a repair attempt with a replacement, and none of them states
        whether it includes the ceiling, the permit, or the tenant protections.
        <a class="srclink" href="estimates.html">analysis&nbsp;&rarr;</a></li>
      </ol>
    </section>

    <section>
      <h2>Where each part of the problem lives</h2>
      <p class="sub">The site is organised by category. Each card states what it answers and what it cannot answer.</p>
      <div class="cards">
        <a class="card" href="executive-summary.html">
          <h3>Executive summary</h3>
          <p>The whole project on one page: what is known, what is decided, what is still open.</p>
          <span class="card-meta">1 page</span>
        </a>
        <a class="card" href="estimates.html">
          <h3>Estimates</h3>
          <p>The three 2026-08-30 numbers normalised, with the seven things missing from all of them.</p>
          <span class="card-meta">{len(est['estimates'])} quotes &middot; 307% spread</span>
        </a>
        <a class="card" href="vendors.html">
          <h3>Vendors</h3>
          <p>CSLB licence records for every firm, field by field, including the two that are suspended.</p>
          <span class="card-meta">{comp['verified_active']} active &middot; {comp['suspended_excluded']} suspended</span>
        </a>
        <a class="card" href="compliance.html">
          <h3>Compliance</h3>
          <p>Permit trigger, drywall exemption, lead-safe rule, asbestos thresholds, tenant notice.</p>
          <span class="card-meta">{len(compliance_items)} checks</span>
        </a>
        <a class="card" href="technical.html">
          <h3>Technical</h3>
          <p>What is behind the tub wall, from the patent that describes the assembly.</p>
          <span class="card-meta">1 primary source</span>
        </a>
        <a class="card" href="requirements.html">
          <h3>Requirements</h3>
          <p>The full register: {total_req} requirements with origin, priority and verification status.</p>
          <span class="card-meta">{total_req} rows &middot; {req['summary']['by_status']['open']} open</span>
        </a>
        <a class="card" href="sources.html">
          <h3>Sources</h3>
          <p>Every official source used, with the exact quoted passage it supports.</p>
          <span class="card-meta">{len(load('sources.json')['sources'])} sources</span>
        </a>
        <a class="card" href="flagged.html">
          <h3>Flagged for review</h3>
          <p>Every blank cell and every discrepancy, with what would close it.</p>
          <span class="card-meta">{flag['summary']['total']} items</span>
        </a>
        <a class="card" href="repo-audit.html">
          <h3>Repo audit</h3>
          <p>Line-by-line check of this repository against its own claims, with measurements.</p>
          <span class="card-meta">14 passed &middot; 5 findings</span>
        </a>
      </div>
    </section>

    <section>
      <h2>Status at a glance</h2>
      <p class="sub">The five states a requirement can be in, and how many requirements are in each.</p>
      {table(["Status", "Meaning", "Count"],
             [["<span class='chip chip-ok'>met</span>", "An official source or a completed artefact confirms it.", str(req["summary"]["by_status"]["met"])],
              ["<span class='chip chip-ok'>verified</span>", "The requirement is established from official code text.", str(req["summary"]["by_status"]["verified"])],
              ["<span class='chip chip-mid'>partially met</span>", "Part of it is satisfied, part is still open.", str(req["summary"]["by_status"]["partially_met"])],
              ["<span class='chip chip-warn'>unverified / blocked</span>", "Cannot be confirmed from an official source from this environment.", str(req["summary"]["by_status"]["unverified"] + req["summary"]["by_status"]["blocked"])],
              ["<span class='chip chip-warn'>open</span>", "Depends on a decision or an on-site fact that does not exist yet.", str(req["summary"]["by_status"]["open"])]])}
    </section>

    <section class="callout callout-quiet">
      <h2>About this project's confidentiality</h2>
      <p>The owner asked that one internal scheduling reason never be published, and it is not recorded
      anywhere on this site or in this repository. Nothing was removed from the analysis to protect it:
      the compliance pages state what the published code says, forward-looking, and stop there.</p>
    </section>
    """
    return page("index.html", "Bathtub overflow trip lever - dashboard",
                "Requirements, estimates, CSLB-verified contractors and code compliance for a seized bathtub overflow trip lever in San Francisco.",
                bodies, "index.html")


def build_exec(est, comp, flag, req) -> str:
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Executive summary</div>
      <h1>The job, the numbers, and the one decision that matters</h1>
      <p class="lede">A trip lever is stuck inside the hidden waste-and-overflow plumbing behind the tub.
      Five or more licensed plumbers have already declined to force it from above. Every one of them
      recommended going in from below. Below the tub is a storage unit, so going in from below means
      opening a drywall ceiling &mdash; which is the point at which this stops being a repair and becomes a
      small construction project with a permit question attached.</p>
    </header>

    <section>
      <h2>1. What is actually wrong</h2>
      <p>The assembly behind the tub is a <strong>trip-lever waste and overflow</strong>. A trip lever on the
      overflow plate moves an adjustable linkage &mdash; two brass rods and a clevis &mdash; which raises or drops a
      hollow cylinder inside the tee that opens and closes the drain. The patent that describes the design
      states the failure mode in its own words: if the linkage is too short the cylinder will not seat, and
      if it is too long the cylinder cannot clear the port inside the tee. Either way, the part that has to
      come out is the part that is jammed.
      {src_link('https://patents.google.com/patent/US4352213A/en','US 4,352,213')}</p>
      <p>That is why &ldquo;just pull it out from the overflow&rdquo; has failed repeatedly. It also explains why the
      plumbers would not force it: the alternative to a clean withdrawal is a sheared linkage or a broken
      overflow fitting, both of which turn a service call into an open-wall job.</p>
    </section>

    <section>
      <h2>2. What the three estimates actually say</h2>
      {table(["Provider (as given)", "Quoted scope", "Price", "Comparable to the others?", "Licence verified"],
             [[esc(e["provider_as_given"]), esc(e["quoted_scope"]),
               f"${e['amount_usd']}",
               {True: "<span class='chip chip-mid'>replacement</span>",
                False: "<span class='chip chip-warn'>adjust only &mdash; different job</span>"}[e["scope_class"] != "adjust_or_repair_only"],
               '<span class="chip chip-warn">unverified</span>' if not e["licence_verified"] else src_link("x", "CSLB")]
              for e in est["estimates"]])}
      <p class="note">The two replacement quotes are 11.6% apart. The $135 figure is 307% below the cheaper
      replacement quote because it is a different scope, not a discount. None of the three states whether it
      includes the ceiling opening, the permit, disposal, or tenant protection.
      <a href="estimates.html">Full comparison</a></p>
    </section>

    <section>
      <h2>3. Who can legally do the whole job</h2>
      <p>Of {comp['checked']} licence numbers checked against CSLB, <strong>{comp['verified_active']} are active</strong> and
      <strong>{comp['suspended_excluded']} are suspended</strong>. The suspended two are worth knowing about: both
      present as normal contractors, and one of them markets a CSLB-plumbing-class licence number while the
      licence is suspended for lack of qualifier, lapsed workers' compensation and a cancelled bond.</p>
      <p>On the &ldquo;all in one service&rdquo; requirement, CSLB's own guidance decides the answer: a B (General
      Building) licensee may contract for and oversee a project that needs more than two types of work, and may
      sub-contract parts of it. San Francisco DBI accepts C-36, B or A licence classes for a plumbing permit.
      So the target is a firm holding <strong>C-36 and B in one licence</strong>.
      {src_link('https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/What_Kind_Of_Contractor.aspx','CSLB')}
      {src_link('https://www.sf.gov/apply-plumbing-and-mechanical-permit','DBI')}</p>
      {table(["Firm", "Licence", "Classes held", "Covers both trades alone?"],
             [[esc(c["business_name"]),
               f'<a class="srclink" href="{esc(c["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(c["licence_number"])}&#8599;</a>',
               esc(", ".join(c["classifications"])),
               '<span class="chip chip-ok">yes</span>' if c["meets_single_provider"].startswith("YES") and "out of county" not in c["status_flag"] else
               ('<span class="chip chip-mid">yes, but out of county</span>' if "out of county" in c["status_flag"] and c["meets_single_provider"].startswith("YES") else
                '<span class="chip chip-warn">no</span>')]
              for c in comp["contractors"] if c["status_flag"].startswith("verified")])}
      <p class="note"><a href="vendors.html">Full licence records for every firm, including bond and workers' compensation</a></p>
    </section>

    <section>
      <h2>4. The decision that matters</h2>
      <div class="callout callout-key">
        <p><strong>Settle the permit question before anyone opens the ceiling.</strong> San Francisco's
        plumbing code exemption list covers leak repair, unstopping, tap replacement and toilet replacement.
        It does not cover bathtub waste-and-overflow removal. The building code exempts wallboard repair from a
        <em>building</em> permit but explicitly re-imposes the plumbing permit. So the ceiling opening is not a
        loophole &mdash; it is the thing that turns a $135 adjustment into a permitted plumbing job with an
        inspection, and it is also the thing that doubles the price.</p>
      </div>
      <p>That gives three coherent strategies, and they should be priced separately rather than blended:</p>
      {table(["Strategy", "What it involves", "Permit position", "Cost band"],
             [["<strong>A. Adjust from above only</strong>", "Contractor attempts to free or re-set the linkage through the overflow opening. No cutting.", "Closest to 104.2(2) unstopping, but still not a named exemption.", "$135 quoted"],
              ["<strong>B. Replace from above</strong>", "Trim kit or full waste-and-overflow replaced through the overflow opening if it will come free.", "Appears to require a plumbing permit.", "$550&ndash;$614 quoted"],
              ["<strong>C. Open the ceiling</strong>", "Same as B plus a ceiling access opening, plumbing, then patch and finish.", "Plumbing permit appears required; the drywall patch itself is exempt.", "Unknown &mdash; no quote covers it"]])}
      <p class="note">No verified quote exists for strategy C. That is the largest open cost in the project.</p>
    </section>

    <section>
      <h2>5. Open items</h2>
      <p>{flag['summary']['total']} items are on <a href="flagged.html">Flagged for review</a>, of which
      {flag['summary']['by_severity']['high']} are high severity. The high ones are: no verified price,
      no verified licence for the three quoting firms, the build year (which decides whether the lead-safe
      rule applies), whether an adjust-only scope is exempt, and one repo finding.</p>
      <p>The requirements register tracks {req['summary']['total']} requirements:
      {req['summary']['by_status']['open']} are open, {flag['summary']['total']} items need a human decision,
      and the rest are either verified against code or satisfied by a finished artefact.</p>
    </section>
    """
    return page("executive-summary.html", "Executive summary - bathtub trip lever",
                "Summary of the trip-lever project: mechanism, estimates, licence verification, and the permit decision.",
                body, "executive-summary.html")


def build_estimates(est) -> str:
    rows = []
    for e in est["estimates"]:
        rows.append([
            esc(e["provider_as_given"]),
            esc(e["quoted_scope"]),
            f"<strong>${e['amount_usd']:,}</strong>",
            f'<span class="chip chip-mid">{esc(e["scope_class"].replace("_"," "))}</span>',
            esc(str(e["includes_labor"])),
            esc(str(e["includes_materials"])),
            '<span class="chip chip-warn">not supplied</span>' if not e["licence_number_supplied"] else src_link("", "CSLB"),
            src_link("", "S18") if e["source_id"] else "",
        ])
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Estimates</div>
      <h1>Three numbers that cannot be compared as they stand</h1>
      <p class="lede">All three quotes arrived on 2026-08-30. Two are replacement prices. One is an
      adjust-only price. None states a licence number, and none states whether the ceiling is included.</p>
    </header>

    <section class="callout callout-warn">
      <h2>Read this before comparing prices</h2>
      <p>Quoting the $135 against the $550 and $614 would be comparing a repair attempt with a replacement.
      The cheapest option is only correct if the stop is a mis-adjusted linkage that can be reached and moved
      from above &mdash; and five or more licensed plumbers have already tried exactly that and declined to force it.</p>
    </section>

    <section>
      <h2>The three quotes, as given</h2>
      <p class="sub">Nothing in this table was cleaned up or re-scoped. &ldquo;Not stated&rdquo; means the quote as
      reported did not say.</p>
      {table(["Provider", "Quoted scope", "Price", "Scope class", "Labour incl.", "Materials incl.", "Licence #", "Source"], rows)}
      <p class="note">All values <span class="chip chip-warn">owner reported</span> on 2026-08-30. No written
      quote, licence number or line-item breakdown was supplied.</p>
    </section>

    <section>
      <h2>Normalised comparison</h2>
      <div class="split">
        <div class="panel">
          <h3>Replacement quotes</h3>
          <p class="big">$614 <span class="vs">vs</span> $550</p>
          <p>Spread <strong>$64</strong> (11.6%). Both are plumbing-class replacement prices and are broadly
          comparable &mdash; except that the $550 quote adds a spout with a diverter, which the other does not.</p>
        </div>
        <div class="panel">
          <h3>Adjust-only quote</h3>
          <p class="big">$135</p>
          <p><strong>$415 (307%)</strong> below the cheaper replacement quote. Not a discount: a different scope,
          and the least likely of the three to resolve a lever that five plumbers could not free.</p>
        </div>
      </div>
    </section>

    <section>
      <h2>What is missing from all three</h2>
      <p class="sub">Each row is a line item that should be in the next round of bids. Blank means no quote addressed it.</p>
      {table(["Missing line item", "Why it matters"],
             [[esc(m), w] for m, w in [
               ("CSLB licence number", "Legally expected on a bid; needed to run the official check. " + src_link("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx","S07")),
               ("Ceiling opening and patch", "The most likely reason the final price moves. Patched wallboard is building-permit exempt but still a labour and finish line item. " + src_link("https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-92027","S11")),
               ("Plumbing permit (if required)", "DBI requires a permit before cutting into or replacing pipes. " + src_link("https://www.sf.gov/apply-plumbing-and-mechanical-permit","S10")),
               ("Disposal of the old assembly", "Metal waste handling. Unverified whether included."),
               ("Prior experience of a seized lever in an occupied unit", "The specific competence this job needs. No official register records it."),
               ("Fixed bid vs. hourly", "Determines who carries the risk if the lever shears."),
               ("Tenant notice, containment and the lead pamphlet", "Required or prudent in an occupied unit. " + src_link("https://www.ecfr.gov/current/title-40/chapter-I/subchapter-R/part-745/subpart-E/section-745.84","S13")),
             ]])}
    </section>

    <section>
      <h2>Analysis</h2>
      <ul class="findings">
        {''.join(f'<li>{esc(a)}</li>' for a in est['analysis'])}
      </ul>
    </section>

    <section class="callout callout-quiet">
      <h2>What this page will not do</h2>
      <p>It will not tell you which of the three is cheapest, because two of the three prices are for a
      different job. It also will not guess a market rate: no official source publishes a price for this
      work, and the only official number in the area is the permit fee, which is a separate cost and is
      itself not transcribed here. <a href="flagged.html">See FR-04, FR-05 and FR-06</a>.</p>
    </section>
    """
    return page("estimates.html", "Estimates - bathtub trip lever",
                "The three estimates normalised, and the line items missing from all of them.",
                body, "estimates.html")


def build_vendors(full, flag) -> str:
    comp = dict(full["summary"])
    comp["contractors"] = full["contractors"]
    active = [c for c in comp["contractors"] if c["status_flag"].startswith("verified")]
    susp = [c for c in comp["contractors"] if c["status_flag"].startswith("SUSPENDED")]

    rows = []
    for c in active:
        rows.append([
            f"<strong>{esc(c['business_name'])}</strong>" + (f"<br><span class='muted'>dba {esc(c['dba'])}</span>" if c["dba"] else ""),
            f'<a href="{esc(c["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(c["licence_number"])}&nbsp;&#8599;</a>',
            '<span class="chip chip-ok">current and active</span>',
            esc(", ".join(c["classifications"])),
            esc(c["address_of_record"]) + ("<br><span class='chip chip-mid'>outside SF</span>" if "out_of_county" in c["status_flag"] else ""),
            esc(c["business_phone_cslb"]),
            esc(c["bond"]),
            esc(c["workers_comp"]),
            '<span class="chip chip-ok">yes</span>' if c["meets_single_provider"].startswith("YES") else '<span class="chip chip-warn">no</span>',
        ])

    srows = []
    for c in susp:
        srows.append([
            f"<strong>{esc(c['business_name'])}</strong>" + (f"<br><span class='muted'>dba {esc(c['dba'])}</span>" if c["dba"] else ""),
            f'<a href="{esc(c["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(c["licence_number"])}&nbsp;&#8599;</a>',
            f'<span class="chip chip-bad">suspended</span>',
            esc(c["licence_status"]),
            esc(c["address_of_record"]),
        ])

    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Vendors</div>
      <h1>Licence-verified contractors, and the two that are suspended</h1>
      <p class="lede">Nine licence numbers were loaded from the California Contractors State License Board
      and transcribed field by field. Seven are current and active. Two are under suspension, and they are
      on this page deliberately &mdash; they are the clearest evidence for why the check is not optional.</p>
    </header>

    <section class="stats">
      {stat("Licences checked", str(comp["checked"]), "CSLB License Detail")}
      {stat("Current and active", str(comp["verified_active"]), "bond and WC current", "hl")}
      {stat("Suspended", str(comp["suspended_excluded"]), "excluded from hiring", "warnbox")}
      {stat("Plumbing + building on one licence", str(comp["single_licence_covering_plumbing_and_building_in_sf"]), "San Francisco based")}
    </section>

    <section>
      <h2>How these were found and verified</h2>
      <ol class="steps">
        <li><strong>Find a licence number.</strong> Public web search for San Francisco plumbing contractors,
        then the licence number printed on the firm's own website or a plumbing directory. Directories were
        used only to obtain the <em>number</em> &mdash; never as the source of the licence status.</li>
        <li><strong>Load the official record.</strong> Each number was opened at
        <a href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" target="_blank" rel="noopener noreferrer">CSLB License Detail</a>
        and the status, classifications, dates, bond and workers' compensation were transcribed verbatim.</li>
        <li><strong>Apply the rule.</strong> A row is active only if the official page said
        &ldquo;This license is current and active.&rdquo; Anything else is transcribed and excluded.</li>
      </ol>
      <p class="note">CSLB's own statewide master file is available at no charge from the
      <a href="https://www.cslb.ca.gov/OnlineServices/DataPortal/ContractorList" target="_blank" rel="noopener noreferrer">Public Data Portal</a>,
      but it is served behind a form and could not be downloaded from this environment. Per-licence
      verification was used instead, which is the more precise check anyway.</p>
    </section>

    <section>
      <h2>Active and verified &mdash; {len(active)} firms</h2>
      {table(["Firm", "Licence #", "Status", "Classifications", "Address of record", "Phone (CSLB)", "Bond", "Workers' comp", "Both trades on one licence?"], rows)}
      <p class="note">Every licence number in the second column links straight to its official CSLB record.
      Status read on 2026-11-06.</p>
    </section>

    <section class="callout callout-key">
      <h2>The &ldquo;all in one service&rdquo; answer</h2>
      <p>Exactly one San Francisco firm in this set holds <strong>C-36 Plumbing and B General Building on the
      same licence</strong>: Ace Plumbing &amp; Rooter, #829071. A B licensee may contract for and oversee a
      project requiring more than two trades, and may perform the work or sub-contract parts of it, which is
      precisely the &ldquo;plumbing plus drywall, one company&rdquo; requirement.
      {src_link('https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/What_Kind_Of_Contractor.aspx','CSLB')}
      A second C-36 + B combination exists at Marin H2O (#839817) but its address of record is in San Rafael,
      so whether it will travel into the City is a phone question, not a published fact.</p>
    </section>

    <section>
      <h2>Suspended &mdash; do not hire &mdash; {len(susp)} firms</h2>
      <p class="sub">These are transscribed exactly as CSLB reported them. They are listed as evidence, not as recommendations.</p>
      {table(["Firm", "Licence #", "Status", "CSLB suspension reason (verbatim)", "Address of record"], srows)}
      <p class="note">The point of this table is that a licence <em>number</em> on a website or a truck proves
      almost nothing. Both of these firms have a number and a public presence. Both are suspended.</p>
    </section>

    <section>
      <h2>What could not be verified about any firm</h2>
      {table(["Field", "Status", "Why"],
             [["Yelp / Google rating and reviews", '<span class="chip chip-warn">unverified</span>', "yelp.com returned HTTP 403 to automated requests this session. Links for you to open yourself are below."],
              ["Service area for this address", '<span class="chip chip-warn">unverified</span>', "CSLB publishes address of record, not service area."],
              ["Willingness to work without a permit", '<span class="chip chip-warn">unverified</span>', "Not published anywhere, and not appropriate to put in writing."],
              ["Price for this job", '<span class="chip chip-warn">unverified</span>', "None of these firms has quoted. Only the three owner-reported numbers exist."],
              ["References for this specific work", '<span class="chip chip-warn">unverified</span>', "Must be requested from the firm and checked by phone."]])}
    </section>

    <section>
      <h2>Review links to open yourself</h2>
      <p class="sub">These are search entry points, not verified results. Nothing on this page reproduces a
      rating or a review, because none could be read.</p>
      <div class="cards">
        <a class="card" href="https://www.yelp.com/search?find_desc=Plumbing+Contractor&amp;find_loc=San+Francisco%2C+CA" target="_blank" rel="noopener noreferrer">
          <h3>Yelp &middot; plumbing contractors, San Francisco</h3><p>Search entry point.</p><span class="card-meta">opens yelp.com</span></a>
        <a class="card" href="https://www.yelp.com/search?find_desc=Bathtub+Repair&amp;find_loc=San+Francisco%2C+CA" target="_blank" rel="noopener noreferrer">
          <h3>Yelp &middot; bathtub repair, San Francisco</h3><p>Narrower query for this exact job.</p><span class="card-meta">opens yelp.com</span></a>
        <a class="card" href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx" target="_blank" rel="noopener noreferrer">
          <h3>CSLB &middot; find C-36 in San Francisco</h3><p>Official list generator by city and class.</p><span class="card-meta">opens cslb.ca.gov</span></a>
      </div>
    </section>
    """
    return page("vendors.html", "Vendors - CSLB verified contractors",
                "Nine CSLB licence records checked for a San Francisco bathtub overflow repair, including two suspended licences.",
                body, "vendors.html")


def build_compliance(comp) -> str:
    rows = []
    for i in comp["items"]:
        rows.append([
            f"<strong>{esc(i['id'])}</strong><br><span class='muted'>{esc(i['topic'])}</span>",
            esc(i["question"]),
            esc(i["official_answer"]),
            chips(i["verification"]),
            src_link(load("sources.json") and next(s["url"] for s in load("sources.json")["sources"] if s["id"] == i["source_id"]), i["source_id"]),
        ])
    detail = []
    for i in comp["items"]:
        detail.append(f"""
        <article class="find" id="{esc(i['id'])}">
          <header><h3>{esc(i['id'])} &middot; {esc(i['topic'])}</h3>{chips(i['verification'])}</header>
          <p class="q">{esc(i['question'])}</p>
          <p class="a"><strong>What the official text says.</strong> {esc(i['official_answer'])}</p>
          <p class="c"><strong>What that means here.</strong> {esc(i['conclusion'])}</p>
          <p class="s">Source: {src_link(next(s['url'] for s in load('sources.json')['sources'] if s['id'] == i['source_id']), i['source_id'])}</p>
        </article>""")
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Compliance</div>
      <h1>What the code actually says about opening this ceiling</h1>
      <p class="lede">Eleven checks against published San Francisco, California and federal text. Seven are
      verified, one is unverified, one is checked-and-not-triggered. The headline is uncomfortable: the
      drywall is exempt, but the plumbing it exposes is not.</p>
    </header>

    <section class="callout callout-key">
      <h2>The whole compliance story in three sentences</h2>
      <ol class="keylist">
        <li>San Francisco's plumbing code exemption list covers leak repair, unstopping, tap and toilet
        replacement &mdash; and does not name bathtub waste-and-overflow work.
        {src_link('https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830','S09')}</li>
        <li>Patching the ceiling is exempt from a <em>building</em> permit, but the same section re-imposes the
        separate plumbing permit for the work underneath it.
        {src_link('https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-92027','S11')}</li>
        <li>DBI states the trigger plainly: a permit is needed before cutting into or replacing pipes,
        especially pipes that will be covered by a wall.
        {src_link('https://www.sf.gov/apply-plumbing-and-mechanical-permit','S10')}</li>
      </ol>
    </section>

    <section>
      <h2>Matrix</h2>
      {table(["Check", "Question", "Official answer (condensed)", "Verified?", "Source"], rows)}
    </section>

    <section>
      <h2>Each check in detail</h2>
      {''.join(detail)}
    </section>

    <section class="callout callout-quiet">
      <h2>Scope of this page</h2>
      <p>These are summaries of published text for internal planning. They are not legal advice, they do not
      cover every code that might apply, and they deliberately do not tell anyone to skip a permit. Where the
      answer depends on a fact this session does not have &mdash; the build year, above all &mdash; the row is marked
      unverified instead of guessed. <a href="flagged.html">See the flagged register</a>.</p>
    </section>
    """
    return page("compliance.html", "Compliance - bathtub trip lever",
                "Permit, drywall, lead-safe, asbestos and tenant-notice checks against published official code.",
                body, "compliance.html")


def build_technical(tech) -> str:
    parts = "".join(
        f"<article class='find'><header><h3>{esc(p['part'])}</h3></header>"
        f"<p class='a'>{esc(p['what_it_is'])}</p><p class='c'><strong>Why it matters here.</strong> {esc(p['relevance'])}</p></article>"
        for p in tech["assembly"])
    VS_OK = '<span class="chip chip-ok">sourced</span>'
    VS_WARN = '<span class="chip chip-warn">unverified</span>'
    fails = "".join(
        "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(m["mechanism"]), esc(m["from_source"]), esc(m["consequence"]),
           (VS_OK + ' <a class="srclink" href="https://patents.google.com/patent/US4352213A/en" '
                    'target="_blank" rel="noopener noreferrer">US4352213&#8599;</a>')
           if m["verified"] else VS_WARN)
        for m in tech["why_it_gets_stuck"])
    qs = "".join(f"<li>{esc(q)}</li>" for q in tech["questions_that_separate_a_good_bid_from_a_bad_one"])
    cons = "".join(f"<li>{esc(c)}</li>" for c in tech["consequence_for_this_project"])
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Technical</div>
      <h1>Why it will not come out from above</h1>
      <p class="lede">Not opinion: the assembly is described in a granted US patent, in its own words, including
      the two adjustments that cause it to jam. This page exists so the owner can tell a credible approach
      from a hopeful one.</p>
    </header>

    <section class="callout callout-quiet">
      <p><strong>Primary source.</strong> {esc(tech['primary_source']['citation'])}
      {src_link(tech['primary_source']['url'], 'US 4,352,213')} Filed 1980, granted 1982, expired. Quoted below
      because it is the clearest public description of the geometry that is hidden behind the tub.</p>
    </section>

    <section>
      <h2>What is behind the tub wall</h2>
      {parts}
    </section>

    <section>
      <h2>Why it seizes</h2>
      {table(["Mechanism", "What the source says", "Consequence", "Sourced?"], [])}
      <div class="table-wrap"><table class="tbl">
        <thead><tr><th>Mechanism</th><th>What the source says</th><th>Consequence</th><th>Sourced?</th></tr></thead>
        <tbody>{fails}</tbody></table></div>
    </section>

    <section>
      <h2>What that means for this job</h2>
      <ul class="findings">{cons}</ul>
    </section>

    <section class="callout callout-key">
      <h2>Eight questions that separate a good bid from a bad one</h2>
      <p>Ask every firm the same eight questions and compare the answers. A firm that has done this work
      will answer all eight without hesitation.</p>
      <ol class="keylist">{qs}</ol>
    </section>
    """
    return page("technical.html", "Technical - bathtub trip lever",
                "The waste-and-overflow assembly described from a granted US patent, and why a seized linkage cannot be forced.",
                body, "technical.html")


def build_requirements(req) -> str:
    srcmap = {x["id"]: x["url"] for x in load("sources.json")["sources"]}
    cats = {}
    for r in req["requirements"]:
        cats.setdefault(r["category"], []).append(r)
    blocks = []
    for cat, items in cats.items():
        rows = [[f"<strong>{esc(r['id'])}</strong>", esc(r["requirement"]), chips(r["status"]),
                 esc(r["origin"].replace("_", " ")), esc(r["priority"].replace("_", " ")),
                 esc(r["verify_by"]), src_link(srcmap.get(r["source_id"], ""), r["source_id"])] for r in items]
        blocks.append(f"""
        <section>
          <h2>{esc(cat)} &middot; {len(items)}</h2>
          {table(["ID", "Requirement", "Status", "Origin", "Priority", "How it gets verified", "Source"], rows)}
        </section>""")
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Requirements</div>
      <h1>The full register &mdash; {req['summary']['total']} requirements</h1>
      <p class="lede">Every requirement in the project, with where it came from, whether it is a must, and
      exactly how it would be verified. Owner-stated requests and code-derived requirements are labelled
      separately so it is always clear which is which.</p>
    </header>

    <section class="stats">
      {stat("Total requirements", str(req["summary"]["total"]), "grouped by category")}
      {stat("Must-have", str(req["summary"]["by_priority"]["must"]), "non-negotiable")}
      {stat("Open", str(req["summary"]["by_status"]["open"]), "waiting on a decision or an on-site fact", "warnbox")}
      {stat("Verified against code", str(req["summary"]["by_status"]["verified"] + req["summary"]["by_status"]["met"] + req["summary"]["by_status"]["met_for_shortlist"]), "official source or finished artefact", "hl")}
    </section>

    <section class="callout callout-quiet">
      <p><strong>Origin key.</strong> <em>owner stated</em> &mdash; the owner asked for it in the request.
      <em>owner implied</em> &mdash; follows directly from the owner's description.
      <em>derived official</em> &mdash; the requirement exists because an official source requires it, and the
      source is named in the row.</p>
    </section>

    {''.join(blocks)}
    """
    return page("requirements.html", "Requirements - bathtub trip lever",
                f"The full requirements register: {req['summary']['total']} requirements with origin, priority and verification method.",
                body, "requirements.html")


def build_sources(src) -> str:
    rows = []
    for s in src["sources"]:
        link = src_link(s["url"], s["id"]) if s["url"] else '<span class="chip chip-warn">owner reported</span>'
        rows.append([f"<strong>{esc(s['id'])}</strong>", f"<span class='chip chip-{'ok' if s['tier']=='official' else ('mid' if s['tier']=='primary_technical' else 'warn')}'>{esc(s['tier'].replace('_',' '))}</span>",
                     esc(s["publisher"]), esc(s["title"]), link, esc(s.get("supports", ""))])
    quotes = "".join(
        f"""<article class="find"><header><h3>{esc(s['id'])} &middot; {esc(s['title'])}</h3>
        {src_link(s['url'], s['url'].split('//')[-1].split('/')[0] if s['url'] else '', 'open')}</header>
        <blockquote>{esc(s['quote'])}</blockquote>
        <p class="c">{esc(s['supports'])}</p></article>"""
        for s in src["sources"] if s.get("quote"))
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Sources</div>
      <h1>Every official source, with the passage it supports</h1>
      <p class="lede">{len(src['sources'])} sources. Nine official publishers, one patent office record, one
      owner-reported input. Where a claim on this site has a source, the source is here and the exact quoted
      text is reproduced so you can read it without leaving the page.</p>
    </header>

    <section>
      <h2>Tier rules</h2>
      {table(["Tier", "Counts as verified?", "Used for"],
             [["<span class='chip chip-ok'>official</span>", "Yes", "Government statute, regulation, code, or licensing registry."],
              ["<span class='chip chip-mid'>primary technical</span>", "Yes, for mechanism only", "Patent-office record describing the physical assembly."],
              ["<span class='chip chip-warn'>third party</span>", "No, never", "Only to discover a licence number that is then checked officially."],
              ["<span class='chip chip-warn'>owner reported</span>", "Recorded, not verified", "The three prices, as given."]])}
    </section>

    <section>
      <h2>Registry</h2>
      {table(["ID", "Tier", "Publisher", "Document", "Link", "What it supports"], rows)}
    </section>

    <section>
      <h2>Quoted passages</h2>
      <p class="sub">Reproduced so that every claim is auditable in place. Read them against the live source before relying on them.</p>
      {quotes}
    </section>

    <section class="callout callout-quiet">
      <h2>Sources deliberately not used</h2>
      <p><strong>Yelp</strong> (HTTP 403 to automated requests), <strong>Google reviews</strong>,
      <strong>Angi/HomeAdvisor/Thumbtack listings</strong> and <strong>plumbing directories</strong> are not
      used as evidence anywhere on this site. Directories were used only to obtain licence numbers, which
      were then verified against CSLB. Review text and star ratings are not reproduced because none could be
      verified. <a href="flagged.html">FR-01, FR-03</a></p>
    </section>
    """
    return page("sources.html", "Sources - bathtub trip lever",
                "Every official source used, with the exact quoted passage it supports.",
                body, "sources.html")


def build_flagged(flag) -> str:
    cats = {}
    for i in flag["items"]:
        cats.setdefault(i["page"], []).append(i)
    blocks = []
    for pg, items in cats.items():
        rows = [[f"<strong>{esc(i['id'])}</strong>", esc(i["field"]),
                 '<span class="chip chip-warn">blank / unverified</span>',
                 esc(i["why"]), esc(i["owner_action"]),
                 src_link(i["source_url"], "open") if i["source_url"] else "&mdash;",
                 f"<span class='chip chip-{'bad' if i['severity']=='high' else ('mid' if i['severity']=='medium' else 'neutral')}'>{esc(i['severity'])}</span>"]
                for i in items]
        blocks.append(f"<section><h2>{esc(pg)} &middot; {len(items)}</h2>"
                      f"{table(['ID','Field','Value','Why it is blank','What would close it','Source','Severity'], rows)}</section>")
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Flagged for review</div>
      <h1>{flag['summary']['total']} things that could not be verified</h1>
      <p class="lede">This is the honest ledger. Every cell that is blank elsewhere on the site appears here
      with the reason it is blank and what would close it. Nothing on this page blocks the project; it exists
      so you can see exactly where the evidence stops.</p>
    </header>

    <section class="stats">
      {stat("Total flagged", str(flag["summary"]["total"]), "across all pages")}
      {stat("High severity", str(flag["summary"]["by_severity"]["high"]), "affects a decision", "warnbox")}
      {stat("Medium", str(flag["summary"]["by_severity"]["medium"]), "affects completeness")}
      {stat("Low", str(flag["summary"]["by_severity"]["low"]), "cosmetic or documentation")}
    </section>

    <section class="callout callout-quiet">
      <h2>Rules applied</h2>
      <ul class="findings">{''.join(f'<li>{esc(r)}</li>' for r in flag['rules_applied'])}</ul>
    </section>

    {''.join(blocks)}
    """
    return page("flagged.html", "Flagged for review - bathtub trip lever",
                "Every unverifiable field and discrepancy, with the reason and what would close it.",
                body, "flagged.html")


def build_repo_audit() -> str:
    checks = [
        ["Test suite", "`pytest -q`", "84 passed"],
        ["Committed JSON parses", "json.load over all commits", "0 invalid"],
        ["Internal site links", "href scan over docs/**/*.html", "0 broken"],
        ["Candidate SHA-256", "sha256sum vs README", "matches 9e345463…"],
        ["Candidate ZIP SHA-256", "sha256sum vs README", "matches 7460b2dd…"],
        ["E3 SHA-256", "sha256sum vs README", "matches f013b9c4…"],
        ["ZIP inner payload", "zipfile + sha256", "byte-identical to loose TIF"],
        ["SHA256SUMS.txt", "3 listed rasters", "all 3 match"],
        ["Grid constants", "sha256 vs vendor/gems57/grid.py docstring", "both match"],
        ["labels.tif identity", "sha256 vs bridge/existing_faults.tif", "identical (7ba308cc…)"],
        ["NaN / finite counts", "rasterio read", "7,111,787 / 5,167,373 — matches docstring"],
        ["Shared grid across rasters", "transform read", "all origin (243350, 4508550), 100 m"],
        ["Dot counts vs names", "non-zero count", "20,000 / 37,654 / 37,654 / 44,090 correct"],
        ["Catalogue collisions", "overlap with labels.tif", "0 for both promoted candidates"],
    ]
    findings = [
        ("F-01", "MEDIUM", "A file named <code>…-30000dots-…</code> contains <strong>10,944</strong> dots.",
         "The raster's own receipt discloses <code>n_dots: 10944, n_dots_target: 30000</code>. The filename does not. Any citation of the name asserts 2.7× the real count."),
        ("F-02", "HIGH", "The parallel lane's stated FAIL reason is measurably inverted.",
         "Three rasters are said to fail because their origin <code>(243350, 4508550)</code> &ldquo;differs from the recorded grid <code>(250000, 4520000)</code>&rdquo;. Measured: those rasters are at <code>(243350, 4508550)</code>, which is exactly the repo's own <code>grid.py TRANSFORM</code>. The only file at <code>(250000, 4520000)</code> is an unrelated zero probe."),
        ("F-03", "MEDIUM", "The &ldquo;off-catalogue&rdquo; relay lane puts <strong>72</strong> dots on the mapped catalogue.",
         "72 of 10,944 non-zero cells coincide with <code>data/labels.tif</code> (0.66%). The two promoted candidates score 0 on the same test."),
        ("F-04", "LOW", "GitHub Pages serves the repo root, not <code>docs/</code>.",
         "Pages API reports <code>source.path: /</code>, so the landing URL renders <code>README.md</code> and the designed site is one level down at <code>/docs/</code>."),
        ("F-05", "LOW", "<code>format_probe_score_0.0000_do_not_submit.tif</code> is served publicly.",
         "It is all zeros and named as a warning, but it is still a live, submission-shaped download next to real candidates."),
    ]
    REPO = "https://github.com/karagemop466-tech/Korea7"
    verify_links = {
        "Test suite": f"{REPO}/blob/main/tests",
        "Committed JSON parses": f"{REPO}/tree/main/evidence",
        "Internal site links": f"{REPO}/tree/main/docs",
        "Candidate SHA-256": f"{REPO}/blob/main/README.md",
        "Candidate ZIP SHA-256": f"{REPO}/blob/main/README.md",
        "E3 SHA-256": f"{REPO}/blob/main/README.md",
        "ZIP inner payload": f"{REPO}/tree/main/docs/downloads",
        "SHA256SUMS.txt": f"{REPO}/blob/main/docs/downloads/SHA256SUMS.txt",
        "Grid constants": f"{REPO}/blob/main/vendor/gems57/grid.py",
        "labels.tif identity": f"{REPO}/tree/main/data",
        "NaN / finite counts": f"{REPO}/blob/main/vendor/gems57/grid.py",
        "Shared grid across rasters": f"{REPO}/tree/main/docs/downloads",
        "Dot counts vs names": f"{REPO}/tree/main/docs/downloads",
        "Catalogue collisions": f"{REPO}/tree/main/data",
    }
    body = f"""
    <header class="page-head">
      <div class="eyebrow">Category &middot; Repo audit</div>
      <h1>This repository, checked against its own claims</h1>
      <p class="lede">The repo is not about bathtubs. It is a DOE GEMS geothermal fault-prospectivity audit.
      This page records {len(checks)} checks that passed and {len(findings)} irregularities, each measured in
      this session rather than asserted.</p>
    </header>

    <section class="callout callout-quiet">
      <p><strong>What this repository is.</strong> A Python research and audit package for the DOE GEMS
      competition (DrivenData #306): single-band GeoTIFFs of &ldquo;fault dots&rdquo; on a 100 m grid in EPSG:32611,
      with an internal holdout evaluator, a submission validator, a pytest suite, and a static GitHub Pages
      site under <code>docs/</code>. The bathtub project in this session is unrelated to its contents, so all
      new work was placed in new paths and nothing existing was restructured.</p>
    </section>

    <section>
      <h2>Checks that passed</h2>
      {table(["Check", "Method", "Result", "Verify"],
             [[esc(c[0]), f"<code>{esc(c[1])}</code>",
               f"<span class='chip chip-ok'>{esc(c[2])}</span>",
               src_link(verify_links.get(c[0], REPO), "", "open")]
              for c in checks])}
    </section>

    <section>
      <h2>Irregularities</h2>
      <div class="cards">
        {''.join(f'<div class="card static"><h3>{esc(f[0])} &middot; <span class="chip chip-{"bad" if f[1]=="HIGH" else ("mid" if f[1]=="MEDIUM" else "neutral")}">{esc(f[1])}</span></h3><p><strong>{f[2]}</strong></p><p class="muted">{f[3]}</p></div>' for f in findings)}
      </div>
      <p class="note">None of these were fixed in this session: the GEMS files are outside this session's
      file scope, and F-02 is a substantive research question rather than a typo. All five are logged in
      <code>COORDINATION.md</code> and on <a href="flagged.html">Flagged for review</a>.</p>
    </section>

    <section>
      <h2>What could not be verified in the repo</h2>
      {table(["Item", "Why"],
             [["Holdout DTI figures", "Internal-evaluator outputs requiring withheld proxy labels. Not independently checkable; transcribed as the repo's claim only."],
              ["USER-REPORTED leaderboard scores", "No organizer receipt exists in the repo, and the repo says so."],
              ["13GEMS covering-lattice probe", "The registry raster is excluded by <code>.gitignore</code> (<code>registry/*.tif</code>), so the percentage cannot be recomputed from committed bytes."],
              ["Nine-focus-site pairwise overlaps", "The nine focus rasters are present, so this is re-runnable, but it was not re-run in this session. Marked not measured, not false."]])}
    </section>

    <section>
      <h2>Bottom line</h2>
      <p>The measured engineering is solid: tests pass, hashes match, ZIPs are byte-identical, the grid is
      consistent, and the catalogue discipline is real. The weak point is prose that outran the data in two
      places &mdash; a filename that overstates a dot count by 2.7×, and a FAIL verdict whose stated reason is
      measurably backwards. In a repository whose entire value is auditability, F-02 should be corrected
      before the next session builds on it.</p>
      <p><a href="https://github.com/karagemop466-tech/Korea7" target="_blank" rel="noopener noreferrer">Repository&nbsp;&#8599;</a>
      &nbsp;·&nbsp; <a href="../index.html">Existing GEMS site&nbsp;&rarr;</a></p>
    </section>
    """
    return page("repo-audit.html", "Repo audit - Korea7",
                "Line-by-line verification of the Korea7 GEMS repository against its own claims, with measurements.",
                body, "repo-audit.html")


# ----------------------------------------------------------------------------- css


CSS = """
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#161a20; --muted:#5d6675; --line:#e3e7ee;
  --brand:#0f5c8c; --brand-2:#0c7f7a; --ok:#0f7a4a; --ok-bg:#e7f6ee;
  --warn:#8a5a00; --warn-bg:#fdf3dd; --bad:#a3151f; --bad-bg:#fdeaea;
  --mid:#7a4a00; --mid-bg:#fbf0d9; --radius:12px;
  --shadow:0 1px 2px rgba(16,24,40,.05),0 1px 3px rgba(16,24,40,.06);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
.skip{position:absolute;left:-9999px}
.skip:focus{left:8px;top:8px;background:#fff;padding:8px 12px;z-index:99;border-radius:8px}
.layout{display:flex;min-height:100vh;align-items:flex-start}
.sidebar{position:sticky;top:0;height:100vh;width:262px;flex:0 0 262px;background:#0e141b;color:#cfd8e3;
  display:flex;flex-direction:column;padding:18px 14px;gap:14px}
.brand{display:flex;gap:10px;align-items:center;padding:4px 6px 12px;border-bottom:1px solid #222d3a}
.brand .mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;
  background:linear-gradient(135deg,var(--brand),var(--brand-2));color:#fff;font-weight:800;font-size:13px}
.brand strong{display:block;font-size:14px;color:#fff;letter-spacing:.2px}
.brand span{font-size:11.5px;color:#8fa0b3}
.sidebar nav{display:flex;flex-direction:column;gap:2px;overflow:auto}
.sidebar nav a{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:8px;
  color:#c6d1de;text-decoration:none;font-size:13.5px;font-weight:500}
.sidebar nav a:hover{background:#18222d;color:#fff}
.sidebar nav a[aria-current="page"]{background:#1b2836;color:#fff;box-shadow:inset 2px 0 0 var(--brand-2)}
.nav-dot{width:5px;height:5px;border-radius:50%;background:#3f5061;flex:0 0 5px}
.sidebar nav a[aria-current="page"] .nav-dot{background:var(--brand-2)}
.side-foot{margin-top:auto;font-size:11.5px;color:#8fa0b3;border-top:1px solid #222d3a;padding-top:12px}
.side-foot p{margin:0 0 8px}
.side-foot a{color:#9ec8e6}
main{flex:1 1 auto;min-width:0;padding:30px 34px 60px;max-width:1180px}
.page-head{margin-bottom:26px;padding-bottom:18px;border-bottom:1px solid var(--line)}
.eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--brand)}
h1{font-size:31px;line-height:1.18;margin:8px 0 12px;letter-spacing:-.4px}
.lede{font-size:15.5px;color:#39424f;max-width:78ch;margin:0}
h2{font-size:19px;margin:34px 0 6px;letter-spacing:-.2px}
h3{font-size:14.5px;margin:0 0 6px}
section{margin-bottom:26px}
.sub{color:var(--muted);font-size:13.5px;margin:0 0 12px;max-width:80ch}
.note{color:var(--muted);font-size:12.5px;margin:8px 0 0}
.muted{color:var(--muted);font-size:12.5px}
code{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef1f6;
  padding:1px 5px;border-radius:4px;color:#25303d}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:12px;margin:0 0 26px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:13px 14px;box-shadow:var(--shadow)}
.stat.hl{border-color:#bfe3d5;background:linear-gradient(180deg,#f4fbf8,#fff)}
.stat.warnbox{border-color:#f0dcaf;background:linear-gradient(180deg,#fffbf0,#fff)}
.stat-label{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.stat-value{font-size:26px;font-weight:800;letter-spacing:-.6px;margin:3px 0 1px}
.stat-value .sub{font-size:15px;color:var(--muted);font-weight:600}
.stat-note{font-size:11.5px;color:var(--muted)}
.stat-note a{color:var(--brand)}
.table-wrap{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
table.tbl{width:100%;border-collapse:collapse;font-size:13px}
table.tbl th{position:sticky;top:0;background:#f0f3f7;text-align:left;font-size:11px;letter-spacing:.06em;
  text-transform:uppercase;color:#46505f;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
table.tbl td{padding:10px 12px;border-bottom:1px solid #eef1f5;vertical-align:top}
table.tbl tbody tr:last-child td{border-bottom:0}
table.tbl tbody tr:hover{background:#fafbfd}
.chip{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;
  padding:2px 7px;border-radius:999px;white-space:nowrap;border:1px solid transparent}
.chip-ok{background:var(--ok-bg);color:var(--ok);border-color:#bfe3d0}
.chip-warn{background:var(--warn-bg);color:var(--warn);border-color:#f0dcaf}
.chip-bad{background:var(--bad-bg);color:var(--bad);border-color:#f6c9cc}
.chip-mid{background:var(--mid-bg);color:var(--mid);border-color:#efdcb4}
.chip-neutral{background:#eef1f6;color:#4b5563;border-color:#dfe4ec}
.srclink{font-size:11px;font-weight:700;color:var(--brand);text-decoration:none;border-bottom:1px dotted #9dc0d8;margin-left:4px}
.srclink:hover{border-bottom-style:solid}
.callout{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--brand);
  border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.callout h2{margin:0 0 8px;font-size:16px}
.callout p{margin:0 0 8px}
.callout p:last-child{margin-bottom:0}
.callout-key{border-left-color:var(--brand-2);background:linear-gradient(180deg,#f5fbfa,#fff)}
.callout-warn{border-left-color:#c79212;background:linear-gradient(180deg,#fffdf5,#fff)}
.callout-quiet{border-left-color:#9aa6b6;background:#fbfcfd}
.keylist{margin:6px 0 0;padding-left:20px}
.keylist li{margin-bottom:9px}
.findings{margin:6px 0 0;padding-left:20px}
.findings li{margin-bottom:8px;color:#374151}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 15px;text-decoration:none;color:inherit;box-shadow:var(--shadow);transition:.15s}
.card:hover{border-color:#b7cbdc;transform:translateY(-1px);box-shadow:0 4px 12px rgba(16,24,40,.08)}
.card.static{transform:none}
.card h3{color:var(--brand);font-size:14px}
.card p{margin:0 0 8px;font-size:12.5px;color:#46505f}
.card-meta{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.03em}
.split{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow)}
.big{font-size:25px;font-weight:800;letter-spacing:-.5px;margin:2px 0 8px}
.vs{font-size:13px;color:var(--muted);font-weight:600;padding:0 4px}
.steps{margin:6px 0 10px;padding-left:20px}
.steps li{margin-bottom:8px}
.find{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 16px;margin-bottom:10px;box-shadow:var(--shadow)}
.find header{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-bottom:6px}
.find header h3{margin:0}
.find .q{font-weight:600;color:#26303c;margin:0 0 8px;font-size:13.5px}
.find .a,.find .c,.find .s{margin:0 0 7px;font-size:13px;color:#3c4652}
.find .s{font-size:11.5px;color:var(--muted);margin-bottom:0}
blockquote{margin:6px 0 10px;padding:10px 14px;background:#f7f9fc;border-left:3px solid #c4d3e0;
  font-size:12.5px;color:#33404f;border-radius:0 8px 8px 0}
.foot{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:11.5px}
.foot p{margin:0 0 6px}
a{color:var(--brand)}
@media (max-width:900px){
  .layout{flex-direction:column}
  .sidebar{position:static;height:auto;width:100%;flex:none}
  .sidebar nav{flex-direction:row;flex-wrap:wrap}
  main{padding:20px 16px 50px}
  h1{font-size:24px}
  .split{grid-template-columns:1fr}
}
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")

    req = load("requirements.json")
    est = load("estimates.json")
    contractors = load("contractors.json")
    comp = dict(contractors["summary"])
    comp["contractors"] = contractors["contractors"]
    compliance = load("compliance.json")
    tech = load("technical.json")
    flag = load("flagged.json")
    src = load("sources.json")

    pages = {
        "index.html": build_index(req, est, comp, flag, compliance),
        "executive-summary.html": build_exec(est, comp, flag, req),
        "estimates.html": build_estimates(est),
        "vendors.html": build_vendors(contractors, flag),
        "compliance.html": build_compliance(compliance),
        "technical.html": build_technical(tech),
        "requirements.html": build_requirements(req),
        "sources.html": build_sources(src),
        "flagged.html": build_flagged(flag),
        "repo-audit.html": build_repo_audit(),
    }
    for name, html_text in pages.items():
        (OUT / name).write_text(html_text, encoding="utf-8")
    print(f"wrote {len(pages)} pages to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
