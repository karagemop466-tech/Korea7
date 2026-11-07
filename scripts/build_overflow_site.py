#!/usr/bin/env python3
"""Build the canonical Bathtub Overflow Trip Lever site at the repository root.

Reads the verified data in data/overflow/*.json and renders a static, no-JS
dashboard: eight pages, every table row either citing an external source link or
explicitly labelled owner-provided. Output is deterministic: same data in, same
HTML out (the capture date comes from the data files, not from the clock).

Run:  python3 scripts/build_overflow_site.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "overflow"

PAGES = [
    ("index.html", "Dashboard"),
    ("summary.html", "Executive summary"),
    ("estimates.html", "Estimates"),
    ("contractors.html", "Contractors"),
    ("findings.html", "Analysis"),
    ("plan.html", "Hiring plan"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
]


# --------------------------------------------------------------------------- helpers
def e(value) -> str:
    """Escape text for safe HTML output."""
    return html.escape(str(value), quote=True)


def load(name: str):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def link(url: str, label: str, cls: str = "") -> str:
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<a href="{e(url)}"{cls_attr}>{e(label)}</a>'


def ext(url: str, label: str) -> str:
    return f'<a href="{e(url)}" rel="noopener">{e(label)}</a>'


def pill(text: str, kind: str = "mute") -> str:
    return f'<span class="pill {kind}">{e(text)}</span>'


def table(headers, rows, caption=None, num_cols=(), caption_html=None) -> str:
    head = []
    for i, h in enumerate(headers):
        cls = ' class="num"' if i in num_cols else ""
        head.append(f"<th{cls} scope=\"col\">{h}</th>")
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cls = ' class="num"' if i in num_cols else ""
            cells.append(f"<td{cls}>{cell}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    cap = ""
    if caption or caption_html:
        cap = f"<caption>{caption_html or e(caption)}</caption>"
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + "".join(head)
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody>"
        + cap
        + "</table></div>"
    )


def nav(active: str) -> str:
    items = []
    for href, label in PAGES:
        current = ' aria-current="page"' if href == active else ""
        cls = ' class="flag-link"' if href == "flagged.html" else ""
        items.append(f'<a href="{href}"{cls}{current}>{e(label)}</a>')
    return "".join(items)


def page(filename: str, title: str, description: str, body: str, project: dict) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap nav">
    <a class="brand" href="index.html"><span class="mark">TL</span> {e(project["short_title"])} <span class="muted">/ San Francisco</span></a>
    <nav aria-label="Primary">{nav(filename)}</nav>
  </div>
</header>

<main id="main" class="wrap">
{body}
</main>

<footer class="site">
  <div class="wrap">
    <span>Internal research dashboard · {e(project["title"])} · San Francisco · verified {e(project["updated"])}</span>
    <span>Licences re-checkable at {ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "cslb.ca.gov")} · session 7e5f723c</span>
  </div>
</footer>
</body>
</html>
"""


def callout(text_html: str, kind: str = "") -> str:
    cls = f"callout {kind}".strip()
    return f'<div class="{cls}"><p>{text_html}</p></div>'


def section(title: str, body_html: str, sub: str = "") -> str:
    sub_html = f'<p class="sub">{e(sub)}</p>' if sub else ""
    return f'<section class="section"><h2>{e(title)}</h2>{sub_html}{body_html}</section>'


# --------------------------------------------------------------------------- data views
def contractor_lookup(contractors: dict) -> dict:
    return {c["id"]: c for c in contractors["records"]}


def licence_cell(c: dict) -> str:
    if not c["license"]:
        return pill("no licence found", "warn") + "<br><small>" + ext(
            c["cslb_url"], "CSLB name search"
        ) + " — blank rather than guessed</small>"
    classes = "<br>".join(e(x) for x in c["classes"])
    return (
        f'<strong>{ext(c["cslb_url"], "#" + c["license"])}</strong><br>'
        f'<small>{e(c["entity_type"])} · issued {e(c["issued"])} · expires {e(c["expires"])}<br>{classes}</small>'
    )


def status_cell(c: dict) -> str:
    if not c["license"]:
        return pill("unverified", "warn") + "<br><small>Licence number not found — see flagged item F14</small>"
    parts = [pill(c["cslb_status"], "ok")]
    bits = [e(c["bond"]), e(c["workers_comp"])]
    parts.append("<small>" + "<br>".join(bits) + "</small>")
    return "<br>".join(parts)


def yelp_cell(c: dict) -> str:
    if not c["yelp_rating"]:
        return pill("not checked", "mute")
    return (
        f'<strong>{e(c["yelp_rating"])} ★</strong> <small>({e(c["yelp_count"])} reviews)</small><br>'
        f'<small>{ext(c["yelp_url"], "Yelp listing")} · captured {e("2026-11-07")}</small>'
    )


def company_cell(c: dict) -> str:
    bits = [f'<strong>{e(c["name"])}</strong>']
    if c["legal_entity"] and c["legal_entity"] != c["name"].upper():
        bits.append(f'<small>CSLB: {e(c["legal_entity"])}</small>')
    links = []
    if c["website"]:
        links.append(ext(c["website"], "website"))
    if c["yelp_url"]:
        links.append(ext(c["yelp_url"], "Yelp"))
    if c["license"]:
        links.append(ext(c["cslb_url"], "CSLB"))
    if links:
        bits.append("<small>" + " · ".join(links) + "</small>")
    return "<br>".join(bits)


def contact_cell(c: dict) -> str:
    bits = []
    if c["phone"]:
        bits.append(e(c["phone"]))
    if c["address_cslb"]:
        bits.append(f'<small>{e(c["address_cslb"])}</small>')
    return "<br>".join(bits) if bits else "—"


# --------------------------------------------------------------------------- pages
def build_index(project, contractors, estimates, flags, plan) -> str:
    cl = contractor_lookup(contractors)
    licensed = [c for c in contractors["records"] if c["license"]]
    all_in_one = [c for c in contractors["records"] if c["all_in_one"]]

    stats = f"""<div class="grid cols-4">
  <div class="card stat"><div class="k">Quotes received</div><div class="v">3</div>
    <div class="s">$135 · $550 · $614 as stated 8/30/26 {pill("owner-provided", "warn")}</div></div>
  <div class="card stat"><div class="k">Candidates checked</div><div class="v">{len(contractors["records"])}</div>
    <div class="s">{len(all_in_one)} can hold drywall and plumbing on one licence</div></div>
  <div class="card stat"><div class="k">Licences active on CSLB</div><div class="v ok">{len(licensed)} / {len(contractors["records"])}</div>
    <div class="s">Read on cslb.ca.gov, data current {e(project["cslb_data_current"])}</div></div>
  <div class="card stat"><div class="k">Flagged for your review</div><div class="v warn">{len(flags["flags"])}</div>
    <div class="s">Unverified values and source disagreements — none blocks use of the site</div></div>
</div>"""

    problem_rows = [
        [f'<strong>{e(f["item"])}</strong>', e(f["detail"]), pill(f["status"], "info")]
        for f in project["problem_facts"]
    ]
    problem_tbl = table(
        ["Item", "Detail", "Provenance"],
        problem_rows,
        caption_html="Source: the owner's project brief. No public record of a private building's plumbing exists, so these rows are marked owner-provided rather than linked.",
    )

    est_rows = []
    for est in estimates["estimates"]:
        c = cl[est["company_id"]]
        est_rows.append(
            [
                f'<strong>{e(est["company"])}</strong><br><small>'
                + ext(est["source_url"], "CSLB #" + c["license"])
                + "</small>",
                e(est["scope"]),
                f'<strong>${est["amount"]:,}</strong><br>' + pill("owner-provided", "warn"),
                f'<span class="muted">—</span><br><small>no official source exists</small>',
            ]
        )
    est_tbl = table(
        ["Company", "Scope as quoted", "Amount", "Official confirmation"],
        est_rows,
        caption_html=f'Amounts are as stated in the owner\'s brief dated {e(estimates["quote_date_as_stated"])}. The CSLB links verify the company and licence only; they do not confirm any price. Full detail: <a href="estimates.html">Estimates</a>.',
        num_cols=(2,),
    )

    short_rows = []
    for c in all_in_one:
        short_rows.append(
            [
                company_cell(c),
                f'<small>{esc_classes(c)}</small>',
                contact_cell(c),
                yelp_cell(c),
                pill("B + C-36", "ok"),
            ]
        )
    short_tbl = table(
        ["Company", "Classifications on the CSLB record", "Contact", "Reviews (snapshot)", "Single-contract fit"],
        short_rows,
        caption_html="Official licence records read 2026-11-07. Yelp values are third-party snapshots (flags F12, F13) — the link is the source; the number is dated.",
    )

    quick = [
        ("summary.html", "Executive summary", "One page: what is known, what is verified, what to do next."),
        ("estimates.html", "Estimates & benchmarks", "The three 2026-08-30 quotes against 2026 national cost data, and what none of them includes."),
        ("contractors.html", "Contractors", f"{len(contractors['records'])} San Francisco candidates with CSLB verification, reviews and contact details."),
        ("findings.html", "Analysis & findings", "Access route, licence scope, quote comparison, drywall budget and occupied-unit planning."),
        ("plan.html", "Hiring plan", "Shortlist order, the questions to ask, the scope checklist and the contract terms."),
        ("sources.html", "Sources", "Every source, what it supports, and when it was read."),
        ("flagged.html", "Flagged for review", f"{len(flags['flags'])} items: unverified values, source disagreements and repository irregularities."),
    ]
    quick_cards = "".join(
        f'<a href="{h}"><div class="t">{e(t)}</div><div class="d">{e(d)}</div></a>' for h, t, d in quick
    )

    steps_brief = "".join(
        f'<li><strong>{e(s["title"])}</strong> — {e(s["body"].split(". ")[0])}.</li>' for s in plan["steps"][:3]
    )

    c_licences = callout(
        "<strong>Licences come from the authority.</strong> Status, classification, bond and workers'-compensation entries were read on the California Contractors State License Board record for each licence number on "
        + e(project["updated"])
        + ". Each record is linked in place, and the link can be re-checked in seconds.",
        "ok",
    )
    c_blank = callout(
        '<strong>If a value cannot be confirmed, it is left blank and flagged.</strong> The three quote amounts are owner-provided: they are shown exactly as supplied, tagged, and the official-confirmation column stays empty. One candidate has no licence number at all, so that cell is blank rather than guessed. See <a href="flagged.html">Flagged for review</a>.'
    )
    c_reviews = callout(
        "<strong>Reviews are snapshots, not evidence.</strong> Star ratings and review counts were captured on "
        + e(project["yelp_captured"])
        + " and drift daily; Yelp also blocks automated reads, so the number is a dated snapshot of the linked page. Licence status, not popularity, decides whether a firm may take the job.",
        "info",
    )

    body = f"""
<section class="hero">
  <div class="eyebrow">Internal research · {e(project["location"])} · verified {e(project["updated"])}</div>
  <h1>{e(project["title"])}</h1>
  <p>{e(project["intro"])}</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="summary.html">Read the executive summary</a>
    <a class="btn btn-ghost" href="contractors.html">Contractors &amp; licence checks</a>
    <a class="btn btn-ghost" href="plan.html">Hiring plan</a>
    <a class="btn btn-ghost" href="flagged.html">{len(flags["flags"])} flagged items</a>
  </div>
</section>

{stats}

<section class="section">
  <h2>The problem, as reported</h2>
  <p class="sub">These are the owner's facts. They are the reason the site exists, and they cannot be confirmed from a public source.</p>
  {problem_tbl}
</section>

<section class="section">
  <h2>The three quotes at a glance</h2>
  <p class="sub">{e(estimates["rule"])}</p>
  {est_tbl}
</section>

<section class="section">
  <h2>If you want one contract for drywall and plumbing, start with these</h2>
  <p class="sub">These four firms hold General Building (B) and Plumbing (C-36) on the same CSLB licence, so one contract can cover opening the ceiling, the repair and the patch.</p>
  {short_tbl}
{callout('A firm holding only C-36 can still do the plumbing — but the drywall portion needs a licensed building contractor. The three original quoters are all C-36 only. See <a href="contractors.html">Contractors</a> for all eleven candidates and <a href="findings.html">Analysis</a> for the licence reasoning.', "info")}
</section>

<section class="section">
  <h2>Next three moves</h2>
  <ol class="tight">{steps_brief}</ol>
  <p class="src">Full sequence with contract terms and a scope checklist: <a href="plan.html">Hiring plan</a>.</p>
</section>

<section class="section">
  <h2>Browse by category</h2>
  <p class="sub">Every table row on this site either carries a source link to an official or publisher page, or is explicitly marked owner-provided.</p>
  <div class="quick">{quick_cards}</div>
</section>

<section class="section">
  <h2>How verification works here</h2>
  {c_licences}
  {c_blank}
  {c_reviews}
</section>
"""
    return page(
        "index.html",
        "Bathtub Overflow Trip Lever — Repair Dashboard · San Francisco",
        "Internal dashboard for a seized bathtub overflow trip lever in San Francisco: three quotes, ten contractor candidates with CSLB licence checks, cost benchmarks, hiring plan and flagged items.",
        body,
        project,
    )


def esc_classes(c: dict) -> str:
    return " · ".join(x.split(" ")[0] for x in c["classes"])


def build_summary(project, contractors, estimates, flags, plan) -> str:
    licensed = [c for c in contractors["records"] if c["license"]]
    all_in_one = [c for c in contractors["records"] if c["all_in_one"]]
    amounts = [x["amount"] for x in estimates["estimates"]]

    verified_rows = [
        [
            "Licences of all candidate firms",
            f"{len(licensed)} of {len(contractors['records'])} candidates hold a licence that reads “current and active” on CSLB; one candidate has no matching record.",
            ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB — Check a licence"),
        ],
        [
            "Single-contract capability",
            f"{len(all_in_one)} firms hold B General Building together with C-36 Plumbing on one licence: "
            + ", ".join(c["name"] for c in all_in_one)
            + ".",
            ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7057", "BPC §7057"),
        ],
        [
            "Below-tub access is standard practice when above fails",
            "“For stubborn drains, you may need to access the plumbing from below the tub”; in extreme cases the old drain is cut out from below.",
            ext("https://www.thisoldhouse.com/plumbing/replacing-bath-tub-drain", "This Old House"),
        ],
        [
            "What a drain replacement normally costs",
            "$500–$1,020 nationally in 2026, average $700 — the band the $550 and $614 quotes sit inside.",
            ext("https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm", "Angi (2026-09-18)"),
        ],
        [
            "What drywall adds",
            "About $2,100 for new drywall where a wall is opened; $300–$930 for patching after a leak. None of the three quotes includes this.",
            ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "Angi (2026-10-28)"),
        ],
        [
            "The licensing threshold",
            "The licensing law does not apply below $1,000 aggregate contract price and only where the work does not require a building permit (BPC §7048, amended effective 1 Jan 2026).",
            ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048", "BPC §7048"),
        ],
    ]
    verified_tbl = table(
        ["What is established", "What the source says", "Source"],
        verified_rows,
        caption_html="Rows above were re-read on 2026-11-07. Anything that could not be confirmed is on the Flagged for review page instead of being asserted here.",
    )

    owner_rows = [
        ["The trip lever is seized inside concealed plumbing behind the wall", pill("owner-provided", "info")],
        ["More than five licensed plumbers declined to remove it from above", pill("owner-provided", "info")],
        ["The storage unit below may require the ceiling to be opened", pill("owner-provided", "info")],
        ["The unit is occupied by tenants during the work", pill("owner-provided", "info")],
        [f"The quotes were $135, $550 and $614, dated {estimates['quote_date_as_stated']}", pill("owner-provided", "warn")],
        [
            'Fast Response = Fast Response Plumbing &amp; Rooter, '
            + ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971", "CSLB #1024971"),
            pill("assumed match", "warn"),
        ],
    ]
    owner_tbl = table(
        ["Owner-supplied fact", "Status"],
        owner_rows,
        caption_html="No public source exists for these; they are the premises of the project, not findings. See <a href=\"flagged.html\">flagged items F1–F3</a>.",
    )

    recs = [
        ("Send one identical written scope to the four B + C-36 firms.", "Use the scope checklist on the Hiring plan page. Identical scope is what makes the bids comparable; CSLB recommends at least three written bids."),
        ("Ask each firm how it will get at the assembly before discussing price.", "A firm that has done this work will describe the access route unprompted. Make the route, the cut location and the cut size part of the quote."),
        ("Price the drywall as its own line on the same contract.", "Published 2026 figures put drywall at roughly $2,100 when a wall is opened, and $300–$930 for patching — a material addition, not a rounding error."),
        ("Verify the licence number on the written bid on CSLB, and read the complaint disclosure if there is one.", "Do this for whichever firm you choose, even the one recommended by someone you trust."),
        ("Keep the payment inside the legal limit.", "CSLB: no more than 10% of the contract price or $1,000, whichever is less, as a down payment unless a blanket performance and payment bond is on file."),
    ]
    rec_html = "".join(
        f"<li><strong>{e(t)}</strong><br>{e(d)}</li>" for t, d in recs
    )

    risk_rows = [
        ["Hidden damage behind the wall", "Water-damage repair runs $1,350–$6,100 in 2026 national data; a leak involving hidden pipes can reach $4,000.", ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "Angi (2026-10-28)")],
        ["Scope creep between trades", "The plumbing and the patch are separate trades; if they are not on one written scope, nobody owns the finish.", ext("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx", "CSLB — hire a contractor")],
        ["Insurance gaps", "Two candidates show a workers'-compensation exemption (“no employees”) on CSLB; ask who is on site and how they are covered.", ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796", "CSLB #757796")],
        ["One candidate has a complaint disclosure", "Handyman Heroes' CSLB record carries a live complaint-disclosure link; read it before hiring.", ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394", "CSLB disclosure #1003394")],
        ["Unverified experience claims", "No register records experience with seized trip levers in occupied units; test it by phone and by references.", '<a href="flagged.html#F16">Flagged item F16</a>'],
        ["Review values are volatile", "Ratings and counts moved during capture and Yelp blocks automated reads; treat them as dated snapshots.", '<a href="flagged.html#F12">Flagged items F12–F13</a>'],
    ]
    risk_tbl = table(
        ["Risk", "Why it matters", "Evidence"],
        risk_rows,
        caption_html="Each risk is either backed by the linked source or explicitly flagged as unverifiable.",
    )

    c_amounts = callout(
        'The amounts are owner-provided and cannot be confirmed from any official source. They are reproduced exactly as supplied and tagged. <a href="flagged.html">Flagged item F2</a>.'
    )

    body = f"""
<div class="page-head">
  <h1>Executive summary</h1>
  <p>What is established, what is assumed, and what to do next — in one page. Verified {e(project["updated"])}.</p>
</div>

<section class="section">
  <h2>The situation</h2>
  <p>The trip lever on the bathtub overflow is seized inside the concealed waste-and-overflow plumbing. Access from above has already failed: the owner reports more than five licensed plumbers declined to force it for fear of destroying the hidden assembly. The reported fallback is access from below, through the ceiling of the storage unit, which means opening and later patching drywall in a building with tenants in place.</p>
  <p>Three quotes were received on {e(estimates["quote_date_as_stated"])}: <strong>${amounts[2]:,}</strong> to repair or adjust the plunger handle, <strong>${amounts[1]:,}</strong> to replace the lever, plug and spout with a diverter, and <strong>${amounts[0]:,}</strong> to replace the waste and overflow. All three companies are licensed and active on CSLB. <strong>None of the three quotes includes the drywall work</strong>, and none is a combined plumbing-plus-drywall price.</p>
  {c_amounts}
</section>

<section class="section">
  <h2>What is established</h2>
  <p class="sub">Each row cites the page that supports it, re-read on 2026-11-07.</p>
  {verified_tbl}
</section>

<section class="section">
  <h2>What is owner-supplied</h2>
  <p class="sub">The premises of the project. No public source exists, and none is invented.</p>
  {owner_tbl}
</section>

<section class="section">
  <h2>Recommendation</h2>
  <ol class="tight">{rec_html}</ol>
</section>

<section class="section">
  <h2>Risks and open items</h2>
  {risk_tbl}
  <p class="src">Every unverified value, source disagreement and repository irregularity is listed with its link on <a href="flagged.html">Flagged for review</a> ({len(flags["flags"])} items).</p>
</section>

<section class="section">
  <h2>Where the numbers land</h2>
  <div class="grid cols-3">
    <div class="card stat"><div class="k">Quotes as stated</div><div class="v">$135–$614</div><div class="s">Three different scopes — not three prices for one job</div></div>
    <div class="card stat"><div class="k">Benchmark: drain replacement</div><div class="v">$500–$1,020</div><div class="s">2026 national average $700 · Angi</div></div>
    <div class="card stat"><div class="k">Benchmark: drywall when a wall opens</div><div class="v">≈ $2,100</div><div class="s">Plus $300–$930 for patching · Angi</div></div>
  </div>
  <p class="src">Benchmarks are national and are not quotes for this job. Sources: <a href="sources.html">Sources</a>.</p>
</section>
"""
    return page(
        "summary.html",
        "Executive summary · Bathtub Overflow Trip Lever",
        "One-page executive summary: established facts with official source links, owner-supplied premises, recommendation, risks, and where the numbers land.",
        body,
        project,
    )


def build_estimates(project, contractors, estimates, benchmarks, flags) -> str:
    cl = contractor_lookup(contractors)
    rows = []
    for est in estimates["estimates"]:
        c = cl[est["company_id"]]
        rows.append(
            [
                f'<strong>{e(est["company"])}</strong><br><small>'
                + ext(c["cslb_url"], "CSLB #" + c["license"])
                + "<br>"
                + ext(c["yelp_url"], "Yelp listing")
                + "</small>",
                e(est["scope"]),
                f'<strong>${est["amount"]:,}</strong><br>' + pill("owner-provided", "warn"),
                '<span class="muted">—</span><br><small>blank: no official confirmation exists</small>',
                ext(est["source_url"], "CSLB #" + c["license"]),
            ]
        )
    est_tbl = table(
        ["Company", "Scope as quoted", "Amount as stated", "Official confirmation", "Source (company/licence only)"],
        rows,
        caption_html=f'Quote date as stated: {e(estimates["quote_date_as_stated"])}. The source column verifies who the company is and that its licence is active; it does not verify any price. Rule: <em>{e(estimates["rule"])}</em>',
        num_cols=(2,),
    )

    bench_rows = []
    for b in benchmarks["benchmarks"]:
        bench_rows.append(
            [e(b["item"]), f'<strong>{e(b["value"])}</strong>', ext(b["url"], b["publisher"]), e(b["page_note"])]
        )
    bench_tbl = table(
        ["Benchmark item", "2026 figure", "Publisher", "Page updated"],
        bench_rows,
        caption_html="National cost data from the named publisher, re-read 2026-11-07. These are not San Francisco quotes and do not price this job.",
    )

    comp_rows = [
        [
            "$135 — repair or adjust the plunger handle",
            "Small-job call-out $50–$200; leak repair $150–$600",
            "In line with an adjustment attempt. It does not remove or replace the concealed assembly.",
            ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "Angi (2026-10-28)"),
        ],
        [
            "$550 — lever, plug and spout with diverter",
            "Drain replacement $500–$1,020, average $700",
            "Inside the national replacement band, though the stated scope is trim rather than the concealed waste-and-overflow.",
            ext("https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm", "Angi (2026-09-18)"),
        ],
        [
            "$614 — replacing waste and overflow",
            "Drain replacement $500–$1,020, average $700",
            "Inside the band and the only quote described as replacing the assembly.",
            ext("https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm", "Angi (2026-09-18)"),
        ],
        [
            "Drywall: not quoted by anyone",
            "≈$2,100 to install drywall where a wall is opened; $300–$930 for patching after a leak",
            "The largest unpriced line. If the ceiling is opened, this is a separate cost on top of every quote above.",
            ext("https://www.angi.com/articles/whats-potential-cost-plumbing-leak.htm", "Angi (2026-10-28)"),
        ],
        [
            "Hidden damage: unknown",
            "Water-damage repair $1,350–$6,100",
            "The main upside risk once the assembly is exposed. Build in a stop-and-report point.",
            ext("https://www.angi.com/articles/how-much-does-it-cost-repair-bathtub-drain-leak.htm", "Angi (2026-09-18)"),
        ],
    ]
    comp_tbl = table(
        ["Quote or line item", "Benchmark", "Reading", "Source"],
        comp_rows,
        caption_html="Reading is analytical; the benchmark and the quote amounts are sourced as shown. The quote amounts themselves remain owner-provided (flag F2).",
    )

    body = f"""
<div class="page-head">
  <h1>Estimates &amp; cost benchmarks</h1>
  <p>The three quotes exactly as stated, the 2026 independent benchmarks that give them context, and the line nobody has priced.</p>
</div>

<section class="section">
  <h2>The three quotes</h2>
  <p class="sub">{e(estimates["rule"])}</p>
  {est_tbl}
</section>

<section class="section">
  <h2>Independent 2026 benchmarks</h2>
  <p class="sub">Re-read on {e(project["updated"])} from the publishers' own pages. Different job, different scope — context, not a price.</p>
  {bench_tbl}
</section>

<section class="section">
  <h2>How the quotes compare</h2>
  {comp_tbl}
</section>

<section class="section">
  <h2>What none of the quotes includes</h2>
  <ul class="tight">
    <li><strong>Opening the ceiling.</strong> No quote prices the access cut in the storage-unit ceiling.</li>
    <li><strong>Patching and finishing the ceiling.</strong> Drywall, tape, sand and paint to a matched finish.</li>
    <li><strong>Protection of an occupied building.</strong> Dust barrier, floor coverings, notice to the tenant, daily clean-up.</li>
    <li><strong>Contingency for hidden damage.</strong> Corrosion, a previous repair, or water damage behind the wall.</li>
    <li><strong>Disposal.</strong> Removal of old material from the premises.</li>
  </ul>
  {callout('Ask each firm to price those five lines on the same quote. Until that exists, the three figures above are not comparable to one another. The scope checklist is on the <a href="plan.html">Hiring plan</a> page.', "info")}
</section>
"""
    return page(
        "estimates.html",
        "Estimates & cost benchmarks · Bathtub Overflow Trip Lever",
        "The three 2026-08-30 quotes exactly as stated, 2026 national cost benchmarks from Angi, and the unpriced drywall line.",
        body,
        project,
    )


def build_contractors(project, contractors, flags) -> str:
    groups = {g["id"]: g for g in contractors["groups"]}

    def rows_for(group_id, slim=False):
        out = []
        for c in contractors["records"]:
            if c["group"] != group_id:
                continue
            if slim:
                out.append(
                    [
                        company_cell(c),
                        contact_cell(c),
                        licence_cell(c),
                        status_cell(c),
                        yelp_cell(c),
                    ]
                )
            else:
                out.append(
                    [
                        company_cell(c),
                        contact_cell(c),
                        licence_cell(c),
                        status_cell(c),
                        yelp_cell(c),
                        f'<strong>${c["quote"]:,}</strong><br>'
                        + pill("owner-provided", "warn")
                        + f'<br><small>{e(c["quote_scope"])}</small>',
                    ]
                )
        return out

    t1 = table(
        ["Company", "Contact", "CSLB licence", "Status, bond, insurance", "Reviews (snapshot 2026-11-07)", "Quote as stated"],
        rows_for("quoter"),
        caption_html=f'Official licence records read {e(project["updated"])} (each record prints “data current as of {e(project["cslb_data_current"])}”). Yelp values are dated snapshots — flags F12/F13. Quote amounts are owner-provided — flag F2.',
        num_cols=(5,),
    )

    t2 = table(
        ["Company", "Contact", "CSLB licence", "Status, bond, insurance", "Reviews (snapshot 2026-11-07)"],
        rows_for("all_in_one", slim=True),
        caption_html="These four hold B General Building and C-36 Plumbing on the same record — the single-contract fit for drywall plus plumbing. Read the notes below the table before choosing.",
    )

    t3 = table(
        ["Company", "Contact", "CSLB licence", "Status, bond, insurance", "Reviews (snapshot 2026-11-07)"],
        rows_for("plumbing", slim=True),
        caption_html="C-36 plumbing candidates without a B General Building classification. The drywall portion would need a licensed building contractor, subcontracted or separate.",
    )

    notes = []
    for c in contractors["records"]:
        if not c["notes"]:
            continue
        flag_links = ""
        if c["flags"]:
            flag_links = (
                ' <small class="src">refs '
                + ", ".join(f'<a href="flagged.html#{f}">{f}</a>' for f in c["flags"])
                + "</small>"
            )
        notes.append(
            f'<li><strong>{e(c["name"])}</strong> — {e(c["notes"])}{flag_links}</li>'
        )
    notes_html = '<ul class="tight">' + "".join(notes) + "</ul>"

    discovery = [
        ("https://www.yelp.com/search?find_desc=Bathtub+Repair&find_loc=San+Francisco%2C+CA", "Bathtub repair in San Francisco"),
        ("https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA", "Plumbers in San Francisco"),
        ("https://www.yelp.com/search?find_desc=Handyman+Plumbing&find_loc=San+Francisco%2C+CA", "Handyman plumbing in San Francisco"),
        ("https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA", "Drywall installation & repair in San Francisco"),
    ]
    discovery_html = '<ul class="tight">' + "".join(
        f"<li>{ext(u, t)}</li>" for u, t in discovery
    ) + (
        '<li>'
        + ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx", "CSLB — Find a licensed contractor by ZIP code (official register)")
        + " — the only list on this page where every entry is a licensed contractor.</li>"
    ) + "</ul>"

    c_contact = callout(
        "<strong>No provider has been contacted.</strong> None of these firms has confirmed this job's scope, availability or experience with this specific assembly — a licence record establishes licence status, a company site establishes what the company says about itself, and neither has confirmed this job.",
        "info",
    )

    c_szeto = callout(
        "One candidate — Szeto Plumbing and Handyman — appears on Yelp with plumbing and drywall services but has no matching CSLB record. Its licence fields are deliberately blank rather than guessed: "
        '<a href="flagged.html#F14">flag F14</a>.',
        "bad",
    )

    body = f"""
<div class="page-head">
  <h1>Contractors — San Francisco</h1>
  <p>Eleven candidates found through review-platform searches and the original quotes, then checked line by line against the official CSLB licence database on {e(project["updated"])}. Review values are dated snapshots; licences are official.</p>
</div>
{c_contact}

<section class="section">
  <h2>{e(groups["quoter"]["title"])}</h2>
  <p class="sub">{e(groups["quoter"]["sub"])}</p>
  {t1}
</section>

<section class="section">
  <h2>{e(groups["all_in_one"]["title"])}</h2>
  <p class="sub">{e(groups["all_in_one"]["sub"])}</p>
  {t2}
  {callout('<strong>Which one first?</strong> Ace Plumbing &amp; Rooter holds the broadest licence set and an established HOA / property-manager practice; Genteel Plumbers is smaller with B + C-36 only; Handyman Heroes adds an explicit handyman/drywall line but carries a complaint disclosure; General SF describes commercial and institutional clients, so ask about small residential work. The ranked shortlist is on the <a href="plan.html">Hiring plan</a> page.', "info")}
</section>

<section class="section">
  <h2>{e(groups["plumbing"]["title"])}</h2>
  <p class="sub">{e(groups["plumbing"]["sub"])}</p>
  {t3}
</section>

<section class="section">
  <h2>Notes, discrepancies and what to ask about</h2>
  {notes_html}
</section>

<section class="section">
  <h2>Re-verify any licence yourself in 30 seconds</h2>
  <ol class="tight">
    <li>Open {ext("https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB — Check a License")}.</li>
    <li>Enter the licence number from the table above (or the business name).</li>
    <li>Confirm the status is “current and active”, that the classification matches the work, that a contractor's bond is on file, and note the workers'-compensation entry — insured or exempt.</li>
    <li>If the record shows complaint-disclosure information, open it and read it.</li>
  </ol>
  <p class="src">CSLB guidance on what to check and why: {ext("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx", "Finding the right contractor")}.</p>
</section>

<section class="section">
  <h2>Keep searching — live review lists for this exact work</h2>
  <p class="sub">These are live search results, so the businesses and review counts change. Use them to widen the field, then verify any licence on CSLB.</p>
  {discovery_html}
</section>

{c_szeto}
"""
    return page(
        "contractors.html",
        "Contractors · CSLB-verified · Bathtub Overflow Trip Lever",
        "Ten San Francisco contractor candidates for a seized bathtub overflow trip lever, with CSLB licence verification, bond and insurance status, Yelp snapshots and contact details.",
        body,
        project,
    )


def build_findings(project, findings, flags) -> str:
    blocks = []
    for i, f in enumerate(findings["findings"], start=1):
        rows = [
            [e(r["claim"]), ext(r["source_url"], r["source_label"])] for r in f["rows"]
        ]
        tbl = table(["What the source says", "Source"], rows)
        blocks.append(
            f"""<section class="section">
  <h2>{i}. {e(f["title"])}</h2>
  <p>{e(f["body"])}</p>
  {tbl}
  {callout("<strong>What to do with this:</strong> " + e(f["takeaway"]), "ok")}
</section>"""
        )
    body = f"""
<div class="page-head">
  <h1>Analysis &amp; findings</h1>
  <p>Seven readings of the evidence: the access route, what the licence classifications actually allow, what the quotes do and do not cover, the drywall budget, the hidden-damage risk, occupied-unit planning, and the licensing threshold.</p>
</div>

<section class="section">
  <h2>How to read this page</h2>
  <p>Each finding separates three things: what the source says (quoted or closely paraphrased, with a link), what it means for this job (analysis), and what to do about it. Where the evidence stops, the page says so instead of filling the gap — every gap is listed on <a href="flagged.html">Flagged for review</a> ({len(flags["flags"])} items).</p>
</section>
{''.join(blocks)}
<section class="section">
  <h2>What the analysis does not establish</h2>
  <ul class="tight">
    <li>Whether this specific assembly can be freed from above. Only an on-site inspection can answer that.</li>
    <li>Whether the wall or ceiling construction in this building matches the general descriptions quoted here.</li>
    <li>The price of this job in San Francisco. The benchmarks are national and the quotes are owner-provided.</li>
    <li>Whether any firm has previously worked in this building, or on this exact failure mode.</li>
  </ul>
</section>
"""
    return page(
        "findings.html",
        "Analysis & findings · Bathtub Overflow Trip Lever",
        "Access-route evidence, licence-classification analysis, quote comparison, drywall and hidden-damage budgets, occupied-unit planning, and licensing thresholds — each with its source.",
        body,
        project,
    )


def build_plan(project, plan, flags) -> str:
    rank_rows = [
        [f'<strong>{r["rank"]}</strong>', f'<strong>{e(r["who"])}</strong>', e(r["why"]), ext(r["source_url"], r["source_label"])]
        for r in plan["shortlist_order"]
    ]
    rank_tbl = table(["Order", "Who", "Why", "Source"], rank_rows)

    steps_html = "".join(
        f"""<div class="step">
  <div class="step-n">{e(s["n"])}</div>
  <div class="step-body">
    <h3>{e(s["title"])}</h3>
    <p>{e(s["body"])}</p>
    <p class="src">Source: {ext(s["source_url"], s["source_label"])}</p>
  </div>
</div>"""
        for s in plan["steps"]
    )

    questions = "".join(f"<li>{e(q)}</li>" for q in plan["questions"])
    checklist = "".join(f"<li>{e(x)}</li>" for x in plan["scope_checklist"])

    c_open = callout(
        'Still open before you book: which entity quoted you, whether the Yelp listing matches the licence, and which firm has actually done concealed-access work in an occupied unit. Those are the <a href="flagged.html">flagged items</a>.'
    )

    body = f"""
<div class="page-head">
  <h1>Hiring plan</h1>
  <p>{e(plan["intro"])}</p>
</div>

<section class="section">
  <h2>Who to call, in order</h2>
  <p class="sub">Ranked by fit with the one-contract requirement, then by verifiable record. Rankings are recommendations, not endorsements.</p>
  {rank_tbl}
</section>

<section class="section">
  <h2>The seven steps</h2>
  <div class="steps">{steps_html}</div>
</section>

<section class="section">
  <h2>Five questions to ask on the phone</h2>
  <ol class="tight">{questions}</ol>
  {callout("A firm that has done this work will answer the first question with an access plan, not a caveat. If the answer is “we will see when we get there”, that is the answer.", "info")}
</section>

<section class="section">
  <h2>Scope checklist — send this with the request</h2>
  <p class="sub">Ten lines. Every one of them should appear, priced or explicitly excluded, in the written quote.</p>
  <ul class="tight">{checklist}</ul>
</section>

<section class="section">
  <h2>Contract and payment terms</h2>
  <ul class="tight">
    <li>A licensed contractor must provide a written contract on a home improvement project, and the licence number must appear on the contract and on all advertising. {ext("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx", "CSLB guidance")}</li>
    <li>Down payment: no more than 10% of the contract price or $1,000, whichever is less, unless the contractor has a blanket performance and payment bond on file with CSLB. {ext("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx", "CSLB — down-payment limit")}</li>
    <li>The contract must describe both workers'-compensation and liability insurance. Ask for the certificates and check the named entity matches the licence. {ext("https://www.cslb.ca.gov/Consumers/Hire_A_Contractor/Finding_The_Right_Contractor.aspx", "CSLB — insurance")}</li>
    <li>Licensing threshold: the law does not apply below $1,000 aggregate contract price and only where the work does not require a building permit (BPC §7048). {ext("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048", "BPC §7048")}</li>
  </ul>
</section>

{c_open}
"""
    return page(
        "plan.html",
        "Hiring plan · Bathtub Overflow Trip Lever",
        "Ranked shortlist, seven hiring steps, the questions to ask, a ten-line scope checklist, and the CSLB contract and payment rules.",
        body,
        project,
    )


def build_sources(project, sources, contractors) -> str:
    official = [s for s in sources["sources"] if s["type"].startswith("Official")]
    rows = []
    for s in sources["sources"]:
        rows.append(
            [
                e(s["publisher"]),
                f'<small>{e(s["type"])}</small>',
                ext(s["url"], s["title"]),
                e(s["supports"]),
                f'<small>{e(s["read"])}</small>',
            ]
        )
    tbl = table(
        ["Publisher", "Type", "Source", "What it supports on this site", "When it was read"],
        rows,
        caption_html=f'All {len(sources["sources"])} sources cited anywhere on this site, including those linked only as contact points. “Read {e(project["updated"])}” means the page was opened directly in this session.',
    )

    body = f"""
<div class="page-head">
  <h1>Sources</h1>
  <p>{e(sources["rule"])}</p>
</div>

<div class="grid cols-3">
  <div class="card stat"><div class="k">Sources listed</div><div class="v">{len(sources["sources"])}</div><div class="s">Official records, statutes, publishers, company sites, review platforms</div></div>
  <div class="card stat"><div class="k">Official sources</div><div class="v ok">{len(official)}</div><div class="s">CSLB licence records and lookups, CSLB guidance and classifications, California statutes</div></div>
  <div class="card stat"><div class="k">Licences verified</div><div class="v">9</div><div class="s">Read on cslb.ca.gov, data current {e(project["cslb_data_current"])}</div></div>
</div>

<section class="section">
  <h2>Every source, in one place</h2>
  <p class="sub">Official records first, then statutes, industry publishers, company sites and review platforms.</p>
  {tbl}
</section>

<section class="section">
  <h2>What is not cited, and why</h2>
  <ul class="tight">
    <li><strong>Anything not re-read on {e(project["updated"])} is not used to support a claim.</strong> Earlier drafts cited additional publishers; those claims were dropped rather than carried forward on trust (flag F18).</li>
    <li><strong>Yelp pages are linked but cannot be read by this environment</strong> (HTTP 403 to automated requests). Ratings therefore come from search-engine snapshots of the same pages, captured and dated in place (flag F13).</li>
    <li><strong>Aggregator and directory profiles</strong> (BBB, BuildZoom, Expertise.com and similar) are not used as evidence of licence status — only the CSLB record is.</li>
    <li><strong>Photos and building records</strong> were not supplied, so nothing about the condition of the assembly is asserted.</li>
  </ul>
</section>
"""
    return page(
        "sources.html",
        "Sources · Bathtub Overflow Trip Lever",
        "Every source used on this site with its URL, publisher, what it supports and the date it was read.",
        body,
        project,
    )


def build_flagged(project, flags, contractors) -> str:
    counts = {}
    for f in flags["flags"]:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    rows = []
    for f in flags["flags"]:
        sev = {"unverified": "warn", "caution": "info", "info": "mute"}.get(f["severity"], "mute")
        source = ext(f["source_url"], f["source_label"]) if f["source_url"].startswith("http") else (
            f'<a href="{e(f["source_url"])}">{e(f["source_label"])}</a>'
        )
        rows.append(
            [
                f'<a id="{e(f["id"])}"></a><strong>{e(f["id"])}</strong>',
                pill(f["severity"], sev),
                f'<strong>{e(f["title"])}</strong><br><small>{e(f["detail"])}</small>',
                source,
                f'<small>{e(f["action"])}</small>',
            ]
        )
    tbl = table(
        ["ID", "Type", "Item", "Source", "Suggested action"],
        rows,
        caption_html="Flags do not block use of this site or the hiring decision. They mark where a value is unverified, where two sources disagree, or where the repository itself is irregular.",
    )

    blank_rows = [
        ["Amount in the “Official confirmation” column", "Blank — no public record of a private quote exists", '<a href="flagged.html#F2">F2</a>'],
        ["Licence number for Szeto Plumbing and Handyman", "Blank — no matching CSLB record found on 2026-11-07", '<a href="flagged.html#F14">F14</a>'],
        ["Job-specific experience in occupied units", "Blank — not recorded by any official register", '<a href="flagged.html#F16">F16</a>'],
        ["Promise that the overflow can be freed from above", "Blank — only an on-site inspection can answer it", '<a href="flagged.html#F1">F1</a>'],
        ["Whether the Yelp listing for Discount Plumbing matches CSLB #1140843", "Blank — address of record is in Burlingame", '<a href="flagged.html#F15">F15</a>'],
    ]
    blank_tbl = table(
        ["Value", "How it is shown", "Flag"],
        blank_rows,
        caption_html="The rule in practice: when an official source cannot confirm a value, the cell stays empty and the gap is named here.",
    )

    body = f"""
<div class="page-head">
  <h1>Flagged for review</h1>
  <p>{e(flags["intro"])}</p>
</div>

<div class="grid cols-3">
  <div class="card stat"><div class="k">Unverified values</div><div class="v warn">{counts.get("unverified", 0)}</div><div class="s">No official source can confirm them</div></div>
  <div class="card stat"><div class="k">Cautions</div><div class="v">{counts.get("caution", 0)}</div><div class="s">Source disagreements or items to ask about</div></div>
  <div class="card stat"><div class="k">Informational</div><div class="v">{counts.get("info", 0)}</div><div class="s">Snapshots, method notes, repository irregularities</div></div>
</div>

<section class="section">
  <h2>All {len(flags["flags"])} items</h2>
  <p class="sub">Each row links to the page or record that shows the problem.</p>
  {tbl}
</section>

<section class="section">
  <h2>Values deliberately left blank</h2>
  {blank_tbl}
</section>

<section class="section">
  <h2>Repository irregularities</h2>
  <ul class="tight">
    <li><strong>The repository contains an unrelated project.</strong> The root of this repository was originally a geothermal fault-prospectivity analysis for a DOE competition; its pages remain under <code>docs/</code> and are unrelated to this repair project. They were left untouched.</li>
    <li><strong>Four overflow page-sets coexist.</strong> Earlier sessions built separate dashboards for this same bathroom job (<code>docs/bath/</code>, <code>docs/overflow-*.html</code>, <code>docs/plumbing-index.html</code>, <code>bathtub-overflow/</code>). None were deleted; all are superseded by the pages at the repository root, which are the only ones maintained.</li>
    <li><strong>One legacy page has a broken internal link.</strong> The unrelated geothermal project under <code>docs/</code> links to a git-ignored results folder from <code>docs/parallel-index.html</code>. It is outside this project and was left untouched; recorded here so the audit trail is complete.</li>
    <li><strong>One shared coordination board, several appended sections.</strong> <code>COORDINATION.md</code> carries the task board and handoff log for each session, preserved verbatim. See <a href="https://github.com/karagemop466-tech/Korea7/blob/main/COORDINATION.md">COORDINATION.md</a>.</li>
    <li><strong>This session's verification trail</strong> is recorded in <code>COORDINATION.md</code> and in the site's own data files under <code>data/overflow/</code>.</li>
  </ul>
</section>
"""
    return page(
        "flagged.html",
        "Flagged for review · Bathtub Overflow Trip Lever",
        f"{len(flags['flags'])} flagged items: unverified values, source disagreements, cautions and repository irregularities, each with its source link.",
        body,
        project,
    )


# --------------------------------------------------------------------------- main
def main() -> None:
    project = load("project.json")
    contractors = load("contractors.json")
    estimates = load("estimates.json")
    benchmarks = load("benchmarks.json")
    findings = load("findings.json")
    plan = load("plan.json")
    sources = load("sources.json")
    flags = load("flags.json")

    pages = {
        "index.html": build_index(project, contractors, estimates, flags, plan),
        "summary.html": build_summary(project, contractors, estimates, flags, plan),
        "estimates.html": build_estimates(project, contractors, estimates, benchmarks, flags),
        "contractors.html": build_contractors(project, contractors, flags),
        "findings.html": build_findings(project, findings, flags),
        "plan.html": build_plan(project, plan, flags),
        "sources.html": build_sources(project, sources, contractors),
        "flagged.html": build_flagged(project, flags, contractors),
    }
    for name, html_text in pages.items():
        (ROOT / name).write_text(html_text, encoding="utf-8")
        print(f"wrote {name} ({len(html_text):,} bytes)")


if __name__ == "__main__":
    main()
