#!/usr/bin/env python3
"""Build the canonical, source-linked bathtub trip-lever repair dashboard.

Stdlib only. Deterministic: no timestamps, network calls, or random values are
introduced at build time. Unconfirmed values are rendered as blank cells with an
explicit link to the relevant Flagged for Review item.
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "repair"
REPO_URL = "https://github.com/karagemop466-tech/Korea7"
SITE_URL = "https://karagemop466-tech.github.io/Korea7/"
PRE_INTEGRATION_SHA = "d93299c3647a94ba2d1c4762ddc48e6f0429fdab"
LAST_PARALLEL_SHA = "408e90c"  # updated during final integration if main advances

PAGES = [
    ("index.html", "Overview"),
    ("summary.html", "Executive summary"),
    ("requirements.html", "Requirements"),
    ("estimates.html", "Estimates"),
    ("contractors.html", "Contractors"),
    ("reviews.html", "Reviews"),
    ("findings.html", "Findings"),
    ("access-plan.html", "Access plan"),
    ("compliance.html", "Compliance"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
    ("verification.html", "Verification"),
    ("archive.html", "Archive"),
]

CSS = """
:root{--bg:#f6f8fb;--panel:#fff;--ink:#172033;--muted:#5b6475;--line:#d9e0ea;--accent:#1d4ed8;--accent-soft:#e8efff;--warn:#9a3412;--warn-soft:#fff4e5;--ok:#166534;--ok-soft:#e9f7ee;--radius:14px;--shadow:0 1px 2px rgba(16,24,40,.06),0 8px 24px rgba(16,24,40,.05)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,summary:focus-visible{outline:3px solid #93c5fd;outline-offset:2px}.skip-link{position:absolute;left:-9999px;top:0;background:#fff;padding:.6rem 1rem;z-index:10}.skip-link:focus{left:0}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}header.site{background:linear-gradient(135deg,#102044,#1d4ed8);color:#fff;padding:26px 0 18px}header.site h1{margin:0 0 6px;font-size:clamp(1.35rem,3vw,2rem);line-height:1.2}header.site p{margin:0;color:#dbe7ff;max-width:80ch}.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.pill{display:inline-block;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:3px 10px;font-size:.8rem;color:#fff}nav.site{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5;box-shadow:0 1px 2px rgba(16,24,40,.04)}nav.site .wrap{display:flex;flex-wrap:wrap;gap:4px;padding-top:8px;padding-bottom:8px}nav.site a{padding:6px 10px;border-radius:8px;font-size:.9rem;color:#334155}nav.site a[aria-current=page]{background:var(--accent-soft);color:var(--accent);font-weight:650}main{padding:26px 0 48px}h2{font-size:1.35rem;margin:28px 0 10px}h3{font-size:1.08rem;margin:20px 0 8px}p{max-width:95ch}.lede{font-size:1.05rem;color:#334155}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:18px 0}.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px;box-shadow:var(--shadow)}.card .num{font-size:1.9rem;font-weight:750;color:var(--accent);line-height:1.1}.card .label{font-size:.9rem;color:var(--muted);margin-top:4px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:18px;margin:16px 0;box-shadow:var(--shadow)}.callout{border-left:5px solid var(--accent);background:var(--accent-soft);border-radius:10px;padding:12px 14px;margin:14px 0}.callout.warn{border-color:var(--warn);background:var(--warn-soft)}.callout.ok{border-color:var(--ok);background:var(--ok-soft)}.table-wrap{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);margin:12px 0}table{border-collapse:collapse;width:100%;min-width:760px;font-size:.92rem}caption{text-align:left;padding:12px 14px;font-weight:650;color:#334155;background:#fbfcfe}th,td{border-top:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}thead th{background:#f1f5f9;color:#334155;font-size:.82rem;text-transform:uppercase;letter-spacing:.03em}tbody tr:nth-child(even){background:#fbfcfe}td ul{margin:0;padding-left:18px}td li{margin:2px 0}.badge{display:inline-block;border-radius:999px;padding:2px 8px;font-size:.75rem;font-weight:650;border:1px solid transparent;white-space:nowrap}.badge.ok{background:var(--ok-soft);color:var(--ok);border-color:#bbe7c8}.badge.warn{background:var(--warn-soft);color:var(--warn);border-color:#fed7aa}.badge.info{background:var(--accent-soft);color:var(--accent);border-color:#c7d7fe}.badge.muted{background:#eef2f7;color:#475569;border-color:#d9e0ea}.blank{display:inline-block;min-width:2.2em;min-height:1em;border-bottom:1px dashed #94a3b8}.flag-link{font-size:.78rem;color:var(--warn);margin-left:6px}.src{font-size:.82rem}.muted{color:var(--muted)}.small{font-size:.85rem}.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}details{background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0}summary{cursor:pointer;font-weight:650}footer.site{border-top:1px solid var(--line);background:#fff;color:var(--muted);padding:20px 0;font-size:.85rem}code{background:#eef2f7;border-radius:5px;padding:1px 5px;font-size:.88em}.steps{padding-left:22px}.steps li{margin:8px 0}.tagrow{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}@media(max-width:640px){.wrap{padding:0 14px}table{font-size:.85rem}th,td{padding:8px}nav.site{position:static}}@media print{nav.site,.skip-link{display:none}body{background:#fff}.panel,.card,.table-wrap{box-shadow:none;break-inside:avoid}a{color:#000;text-decoration:underline}}
"""


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def e(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def a(url: str, label: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    if url.startswith("http"):
        return f'<a href="{e(url)}"{c} rel="noopener noreferrer" target="_blank">{e(label)}</a>'
    return f'<a href="{e(url)}"{c}>{e(label)}</a>'


def blank(flag_id: str = "exact-fit-unconfirmed", label: str = "Unverified") -> str:
    return f'<span class="blank" role="img" aria-label="Value intentionally blank because unverified"></span> {a(f"flagged.html#{flag_id}", label, "flag-link")}'


def badge(text: str, kind: str = "info") -> str:
    return f'<span class="badge {kind}">{e(text)}</span>'


def table(caption: str, headers: list[str], rows: list[list[str]], min_width: int | None = None) -> str:
    style = f' style="min-width:{min_width}px"' if min_width else ""
    head = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table{style}><caption>{e(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def page(filename: str, title: str, subtitle: str, body: str, checked: str) -> str:
    nav_parts = []
    for href, label in PAGES:
        current = ' aria-current="page"' if href == filename else ""
        nav_parts.append(f'<a href="{e(href)}"{current}>{e(label)}</a>')
    nav = "".join(nav_parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(subtitle)}">
<title>{e(title)} · SF Bathtub Trip-Lever Repair</title>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<h1>San Francisco bathtub overflow / trip-lever repair</h1>
<p>{e(subtitle)}</p>
<div class="meta"><span class="pill">Evidence checked {e(checked)}</span><span class="pill">Source-linked rows</span><span class="pill">Unconfirmed values blank</span><span class="pill">No provider contacted or booked</span></div>
</div></header>
<nav class="site" aria-label="Dashboard sections"><div class="wrap">{nav}</div></nav>
<main id="main" class="wrap">
{body}
</main>
<footer class="site"><div class="wrap">
<p>Canonical repair dashboard for this repository. Earlier page sets and the unrelated legacy GEMS project remain preserved in Git; see {a('archive.html', 'Archive')} and {a('flagged.html', 'Flagged for review')}. This site is public; it contains no tenant identifiers or private scheduling context.</p>
<p>{a(REPO_URL, 'Repository')} · {a(SITE_URL, 'Live site')} · Evidence date {e(checked)}. License status must be rechecked on the day of hiring.</p>
</div></footer>
</body>
</html>
"""


def provider_by_id(providers):
    return {p["id"]: p for p in providers}


def source_registry(providers, guidance, reviews) -> list[dict]:
    sources = []
    seen = set()

    def add(url, title, kind, method):
        if not url or url in seen:
            return
        seen.add(url)
        sources.append({"url": url, "title": title, "type": kind, "method": method})

    for g in guidance["sources"]:
        add(g["url"], g["title"], g["type"], g["method"])
    for p in providers:
        if p.get("license"):
            add(p["cslb_url"], f"CSLB #{p['license']} — {p['legal_name']}", "Government regulator record", "Read directly 2026-11-07")
        else:
            add(p["cslb_url"], "CSLB official license lookup", "Government regulator lookup", "Official lookup entry point")
        if p.get("website"):
            add(p["website"], f"{p['name']} — company website", "Business self-description", "Company-published; not independent performance proof")
        for u in p.get("service_pages", []):
            add(u, f"{p['name']} — service page", "Business self-description", "Read directly; company-published scope")
        add(p.get("yelp_url"), f"{p['name']} — Yelp review/discovery link", "Review platform", "Direct fetch restricted (HTTP 403); no current numeric values asserted")
    for b in reviews["bbb"]:
        add(b["url"], f"{b['provider']} — BBB profile", "Review/complaint platform", "Read directly 2026-11-07; platform statements only")
    add(f"{REPO_URL}/blob/main/COORDINATION.md", "Repository coordination board", "Repository", "Session history and verification protocol")
    add(REPO_URL, "Repository", "Repository", "Canonical source and preserved history")
    return sources


def build(output: Path) -> None:
    providers_doc = load("providers.json")
    providers = providers_doc["providers"]
    by_id = provider_by_id(providers)
    estimates = load("estimates.json")
    requirements = load("requirements.json")
    guidance = load("guidance.json")
    findings = load("findings.json")
    flags = load("flags.json")
    reviews = load("reviews.json")
    checked = providers_doc["checked_on"]
    verified = [p for p in providers if p.get("license")]
    discovery = [p for p in providers if not p.get("license")]
    combined = [p for p in providers if p["group"] == "combined"]
    sources = source_registry(providers, guidance, reviews)
    flag_ids = {f["id"] for f in flags["flags"]}

    output.mkdir(parents=True, exist_ok=True)
    (output / "assets").mkdir(exist_ok=True)
    (output / "assets" / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    out_data = output / "data" / "repair"
    out_data.mkdir(parents=True, exist_ok=True)
    for name in ["providers.json", "estimates.json", "requirements.json", "guidance.json", "findings.json", "flags.json", "reviews.json"]:
        shutil.copyfile(DATA / name, out_data / name)
    (out_data / "sources.json").write_text(json.dumps({"checked_on": checked, "sources": sources}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "data" / "validation.json").write_text(json.dumps({"status": "pending", "note": "Run scripts/verify_repair_dashboard.py to replace this placeholder before publication."}, indent=2) + "\n", encoding="utf-8")

    def write(name, title, subtitle, body):
        (output / name).write_text(page(name, title, subtitle, body, checked), encoding="utf-8")

    # Overview
    cards = f"""
<div class="cards">
<div class="card"><div class="num">{len(verified)}</div><div class="label">CSLB records read directly</div></div>
<div class="card"><div class="num">{len(combined)}</div><div class="label">Combined-service leads to screen first</div></div>
<div class="card"><div class="num">{len(estimates['estimates'])}</div><div class="label">Owner-reported estimates; amounts unverified</div></div>
<div class="card"><div class="num">{len(discovery)}</div><div class="label">Discovery-only leads; licenses blank</div></div>
<div class="card"><div class="num">{len(flags['flags'])}</div><div class="label">Flagged review items</div></div>
</div>"""
    body = f"""
<h2>Overview</h2>
<p class="lede">Research and publication dashboard for a seized bathtub wastewater overflow trip-lever/plunger mechanism in concealed plumbing in San Francisco. The owner prefers a safe from-above approach; if that is not feasible, the discussed alternative is controlled access from below through a storage-unit ceiling, with plumbing and drywall restoration coordinated by one responsible service.</p>
<div class="callout warn"><strong>Not a booking or a permit determination.</strong> No provider was contacted, confirmed, or booked. Exact job fit, access method, availability, total price, and job-specific permit classification remain unconfirmed. Official guidance is linked on {a('compliance.html', 'Compliance')}.</div>
{cards}
<div class="grid2">
<div class="panel"><h3>Start here</h3><ol class="steps">
<li>{a('summary.html', 'Executive summary')} — decision-ready findings and screening order.</li>
<li>{a('requirements.html', 'Requirements')} — owner requests and proposed acceptance checks.</li>
<li>{a('contractors.html', 'Contractors')} — evidence-separated provider tables.</li>
<li>{a('access-plan.html', 'Access plan')} — above-first / below-alternative questions.</li>
</ol></div>
<div class="panel"><h3>Evidence and irregularities</h3><ol class="steps">
<li>{a('estimates.html', 'Estimates')} — scopes retained; unverified amounts blank.</li>
<li>{a('reviews.html', 'Reviews')} — Yelp restricted; BBB platform statements separated.</li>
<li>{a('findings.html', 'Findings')} and {a('flagged.html', 'Flagged for review')}.</li>
<li>{a('sources.html', 'Sources')} and {a('verification.html', 'Verification method')}.</li>
</ol></div>
</div>
<h2>Screening order, not an endorsement</h2>
<p>Based only on published service scope and checked license records: {a('contractors.html#general-sf', 'General SF')} first (explicit sheetrock/tape/texture plus plumbing); {a('contractors.html#heises-plumbing', "Heise's Plumbing")} second (explicit rental/tenant scheduling and drywall patching, with ceiling-scope questions); {a('contractors.html#handyman-heroes', 'Handyman Heroes')} third (wall repair plus plumbing, with CSLB disclosure and classification questions). Every candidate still needs a site-specific written proposal.</p>
"""
    write("index.html", "Overview", "Canonical, source-linked research dashboard. Unconfirmed values are blank and flagged.", body)

    # Executive summary
    summary_rows = []
    for p in combined:
        license_label = f"CSLB #{p['license']}"
        summary_rows.append([
            f'<strong>{e(p["name"])}</strong><br>{a(p["cslb_url"], license_label, "src")}',
            e(p["plumbing_evidence"]),
            e(p["drywall_evidence"]) if p["drywall_evidence"] else blank("drywall-unconfirmed"),
            e(p["occupied_evidence"]) if p["occupied_evidence"] else blank("exact-fit-unconfirmed"),
            e(p["note"]),
        ])
    body = f"""
<h2>Executive summary</h2>
<p class="lede">The repository now has one canonical dashboard built from a source-linked dataset. Fourteen contractor license records were read directly from CSLB on {e(checked)}; seven earlier discovery leads are retained with blank license fields. Three owner-reported estimate scopes are preserved, but amounts and per-estimate dates are not published as verified values.</p>
<div class="callout"><strong>Best documented combined-service screen:</strong> General SF has the clearest explicitly published plumbing + sheetrock/tape/texture scope. Heise's explicitly addresses rental units, tenant schedules, and drywall patching. Handyman Heroes publishes wall repair plus plumbing but has a CSLB disclosure and a C-10 advertising discrepancy to review. None is confirmed for this exact seized assembly.</div>
{table('Combined-service leads (company-published scope; regulator identity separate)', ['Provider / license', 'Plumbing evidence', 'Drywall evidence', 'Occupied-unit evidence', 'Caveat'], summary_rows, 980)}
<h3>What the evidence does not establish</h3>
<ul>
<li>No provider has confirmed availability, willingness to take this job, exact repair method, combined price, or tenant-protection protocol.</li>
<li>A B or C-36 license does not prove a company offers drywall restoration or has experience with this mechanism.</li>
<li>The installed manufacturer/model is unknown; manufacturer instructions are general context, not a diagnosis.</li>
<li>Yelp direct fetches were restricted; current Yelp ratings/counts are blank. BBB statements are platform evidence only.</li>
<li>Permit/inspection requirements depend on the actual scope; no exemption is asserted here.</li>
</ul>
<h3>Recommended next action</h3>
<p>Use {a('requirements.html', 'the requirements checklist')} and {a('access-plan.html', 'the access-plan questions')} to request identical written scopes from the three combined-service leads, then compare itemized proposals under {a('compliance.html', 'official compliance guidance')}. Recheck CSLB status and insurance on the day of hiring.</p>
"""
    write("summary.html", "Executive summary", "Decision-ready summary with evidence limits and screening order.", body)

    # Requirements
    req_rows = []
    for r in requirements["requirements"]:
        req_rows.append([
            f'<strong>{e(r["id"])}</strong><br>{badge(r["category"], "muted")}',
            e(r["requirement"]),
            e(r["origin"]),
            blank("owner-facts") if r["confirmed_site_fact"] is None else e(r["confirmed_site_fact"]),
            e(r["acceptance"]),
            a(r["context_source"], r["context_label"], "src"),
        ])
    body = f"""
<h2>Requirements</h2>
<p>{e(requirements['note'])}</p>
{table('Full requirements and proposed acceptance checks', ['ID / category', 'Requirement', 'Origin', 'Confirmed site fact', 'Acceptance check', 'Official context source'], req_rows, 1100)}
"""
    write("requirements.html", "Requirements", "Owner requests and proposed acceptance checks, separated from official context.", body)

    # Estimates
    est_rows = []
    for q in estimates["estimates"]:
        est_rows.append([
            f'<strong>{e(q["id"])}</strong>',
            f'{e(q["provider"])}<br>{a(q["identity_source"], "CSLB identity context", "src")}',
            e(q["scope_owner_reported"]),
            blank("quotes"),
            e(q["labor_materials"]) if q["labor_materials"] else blank("quotes"),
            blank("quotes"),
            badge(q["status"], "warn"),
        ])
    body = f"""
<h2>Estimates</h2>
<div class="callout warn"><strong>Amounts are intentionally blank.</strong> {e(estimates['amount_policy'])}</div>
<p><strong>Date heading as supplied:</strong> <code>{e(estimates['date_heading_as_supplied'])}</code>. {e(estimates['date_note'])}</p>
{table('Owner-reported estimate scopes (not verified contractor commitments)', ['ID', 'Provider / identity context', 'Scope as owner reported', 'Official-confirmed amount', 'Labor/materials', 'Drywall included?', 'Status'], est_rows, 1050)}
<div class="panel"><h3>Combined plumbing + access + drywall quote</h3><p>{blank('quotes')} {e(estimates['combined_quote']['status'])}</p></div>
<h3>How to compare</h3>
<p>CSLB recommends comparing at least three written bids on identical scope. Ask each provider to separate diagnosis/adjustment, replacement parts, access opening, drywall restoration, testing, cleanup, and contingencies. See {a('requirements.html', 'R15–R16')} and {a('sources.html', 'CSLB hiring guidance')}.</p>
"""
    write("estimates.html", "Estimates", "Owner-reported scopes retained; unverified amounts and inclusions blank.", body)

    # Contractors
    def provider_rows(group):
        rows = []
        for p in providers:
            if p["group"] != group:
                continue
            lic = a(p["cslb_url"], f'#{p["license"]}', "src") + f'<br>{e(p["status"])}<br><span class="muted small">Exp. {e(p["expires"])}</span>' if p.get("license") else blank("discovery-license")
            classes = "<ul>" + "".join(f"<li>{e(c)}</li>" for c in p["classifications"]) + "</ul>" if p["classifications"] else blank("discovery-license")
            drywall = e(p["drywall_evidence"]) if p["drywall_evidence"] else blank("drywall-unconfirmed" if p.get("license") else "discovery-license")
            occupied = e(p["occupied_evidence"]) if p["occupied_evidence"] else blank("exact-fit-unconfirmed")
            review_links = a(p["yelp_url"], "Yelp (manual)", "src")
            bbb = next((b for b in reviews["bbb"] if b["provider_id"] == p["id"]), None)
            if bbb:
                review_links += "<br>" + a(bbb["url"], "BBB profile", "src")
            flag_links = " ".join(a(f"flagged.html#{fid}", fid, "flag-link") for fid in p["flags"] if fid in flag_ids)
            rows.append([
                f'<span id="{e(p["id"])}"></span><strong>{e(p["name"])}</strong><br><span class="muted small">{e(p["legal_name"]) if p.get("legal_name") else "Legal name unconfirmed"}</span><details><summary>Record details</summary><p class="small">{e(p["note"])}</p><p class="small"><strong>CSLB phone:</strong> {e(p["phone_cslb"]) if p.get("phone_cslb") else "—"}<br><strong>CSLB address:</strong> {e(p["address_cslb"]) if p.get("address_cslb") else "—"}<br><strong>Bond:</strong> {("$" + format(p["bond_usd"], ",")) if p.get("bond_usd") is not None else "—"}<br><strong>Workers’ comp:</strong> {e(p["workers_comp"]) if p.get("workers_comp") else "—"}</p><p class="small">{a(p["website"], "Company website", "src") if p.get("website") else ""}</p></details>',
                lic,
                classes,
                e(p["plumbing_evidence"]) if p["plumbing_evidence"] else blank("discovery-license"),
                drywall,
                occupied,
                review_links + "<br>" + flag_links,
            ])
        return rows

    headers = ["Provider", "CSLB license / status", "Classifications", "Plumbing evidence (company)", "Drywall evidence (company)", "Occupied-unit evidence", "Reviews / flags"]
    body = f"""
<h2>Contractors</h2>
<p>{e(providers_doc['policy'])}</p>
<div class="callout"><strong>Screening order:</strong> General SF → Heise's → Handyman Heroes for explicitly published combined/rental-repair scope. This is not a ranking by stars, license count, or confirmed ability to do this job.</div>
<h3 id="combined">Combined-service leads</h3>
{table('Explicitly published plumbing + wall/drywall or rental-repair scope', headers, provider_rows('combined'), 1250)}
<h3 id="quoters">Providers named in owner-reported estimates</h3>
{table('Existing estimate leads; amounts remain unverified', headers, provider_rows('quoter'), 1250)}
<h3 id="plumbing">Additional verified plumbing / general-building leads</h3>
{table('License verified; drywall or exact job fit may be unconfirmed', headers, provider_rows('plumbing'), 1250)}
<h3 id="discovery">Discovery-only leads</h3>
{table('Retained from earlier research; license and most fields blank until officially confirmed', headers, provider_rows('discovery'), 1250)}
<h3>Questions before selection</h3>
<ol class="steps">
<li>Can you diagnose and service this exact seized overflow trip-lever/plunger assembly without forcing it? What comparable concealed-work references can you share?</li>
<li>Is safe from-above/overflow-opening access feasible? If not, what controlled below-ceiling opening and protection plan do you propose?</li>
<li>Who is responsible for plumbing, drywall opening, patch/tape/texture/paint, testing, cleanup, and any required inspections under one written scope?</li>
<li>How do you coordinate tenant access and protect storage contents and occupied areas?</li>
<li>What is itemized, what is excluded, and what triggers a written change order?</li>
</ol>
"""
    write("contractors.html", "Contractors", "Evidence-separated provider tables: regulator records, company scope, reviews, and flags.", body)

    # Reviews
    yelp_rows = []
    for p in providers:
        yelp_rows.append([
            e(p["name"]),
            a(p["yelp_url"], "Yelp link", "src"),
            blank("reviews"),
            blank("reviews"),
            e(p["review_status"]),
        ])
    bbb_rows = []
    for b in reviews["bbb"]:
        bbb_rows.append([
            e(b["provider"]),
            a(b["url"], "BBB profile", "src"),
            e(b["rating_as_platform_states"]),
            e(b["accreditation"]),
            e(b["complaints_last_3_years_as_platform_states"]),
            blank("reviews"),
            e(b["status"]),
        ])
    body = f"""
<h2>Reviews</h2>
<p>{e(reviews['note'])}</p>
<h3>Yelp — manual review links only</h3>
{table('Yelp links; current ratings and counts blank because direct fetch was restricted', ['Provider', 'Review link', 'Rating', 'Review count', 'Access / verification status'], yelp_rows, 900)}
<h3>BBB — platform statements read directly</h3>
{table('BBB profile fields as stated by BBB; not government licensing or job-fit proof', ['Provider', 'Source', 'BBB rating statement', 'Accreditation', 'Complaints in last 3 years (BBB statement)', 'Customer review count', 'Check status'], bbb_rows, 1000)}
<div class="callout warn">BBB says its profiles assist judgment and do not verify third-party accuracy. A platform rating or complaint count is not a CSLB record, a reference for this exact repair, or proof of occupied-unit procedures.</div>
"""
    write("reviews.html", "Reviews", "Review-platform evidence separated from official licensing and job-fit verification.", body)

    # Findings
    finding_rows = []
    for f in findings["findings"]:
        finding_rows.append([
            f'<strong>{e(f["id"])}</strong>',
            f'<strong>{e(f["title"])}</strong><br>{e(f["finding"])}',
            e(f["basis"]),
            a(f["source"], f["source_label"], "src"),
            badge(f["status"], "warn" if "unconfirmed" in f["status"].lower() or "restricted" in f["status"].lower() or "pending" in f["status"].lower() else "info"),
        ])
    body = f"""
<h2>Findings</h2>
<p>Findings separate repository observations, owner testimony, regulator records, company-published scope, and review-platform evidence. Interpretation is labeled; no finding confirms a booking or exact job capability.</p>
{table('Findings and analysis', ['ID', 'Finding', 'Evidence basis', 'Source', 'Status'], finding_rows, 1000)}
"""
    write("findings.html", "Findings", "Evidence-separated findings, corrections, and open verification gaps.", body)

    # Access plan
    body = f"""
<h2>Access plan</h2>
<p class="lede">Owner preference: attempt a safe from-above / overflow-opening approach first. If the contractor determines that risks damaging concealed plumbing, plan controlled access from below through the storage-unit ceiling. The actual installed mechanism and building assembly are not identified in the supplied evidence.</p>
<div class="callout warn">This is a screening checklist, not an instruction to force a seized mechanism or open a ceiling. A licensed contractor must diagnose the assembly and determine the safe access method.</div>
<h3>Above-first questions</h3>
<ol class="steps">
<li>Identify manufacturer/model and photograph the overflow plate, linkage, and accessible connections before disassembly.</li>
<li>Can the linkage be retrieved/adjusted through the overflow opening without forcing it? What stop-work threshold applies?</li>
<li>Which compatible parts are needed only if replacement is actually required?</li>
<li>What hidden connections must remain intact, and how will damage risk be controlled?</li>
</ol>
<h3>Below-access alternative</h3>
<ol class="steps">
<li>Locate the ceiling opening relative to the tub drain/overflow and protect storage contents below.</li>
<li>Define opening size, dust containment, water control, and temporary protection for the occupied unit.</li>
<li>Keep access open for functional and leak checks before any ceiling closure.</li>
<li>Specify drywall patch, tape, texture, paint match, and any required fire-rated assembly or access-panel option.</li>
<li>Name one responsible prime or written subcontracting plan for plumbing and restoration.</li>
</ol>
<h3>Acceptance before closure</h3>
<ul>
<li>Stopper/drain operates correctly; overflow/drain connections checked for leaks with access open.</li>
<li>Required inspections completed before covering pipes, if applicable.</li>
<li>Before/during/after documentation retained without publishing tenant identifiers.</li>
<li>Restoration scope, cleanup, warranty, and change-order process are written.</li>
</ul>
<p>Technical context: {a('https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf', 'Watco trip-lever instructions (model-specific example)')}. Requirements: {a('requirements.html', 'R01–R14')}.</p>
"""
    write("access-plan.html", "Access plan", "Above-first preference and controlled below-access alternative, with acceptance checks.", body)

    # Compliance
    guidance_rows = [[e(g["title"]), e(g["supports"]), a(g["url"], "Official source", "src"), e(g["method"])] for g in guidance["sources"] if g["type"].startswith("Government")]
    body = f"""
<h2>Compliance</h2>
<div class="callout warn"><strong>No job-specific exemption is asserted.</strong> {e(guidance['neutral_compliance_note'])}</div>
{table('Official guidance and code context', ['Source', 'What it supports', 'Link', 'Method'], guidance_rows, 950)}
<h3>Before work</h3>
<ul>
<li>Have the contractor and San Francisco DBI classify the actual proposed scope, including any pipe cutting/replacement, ceiling opening, and restoration.</li>
<li>Confirm required permits and inspections; do not cover pipes before required inspections.</li>
<li>Verify the contracting entity, license, bond, workers' compensation for the actual crew, and liability insurance.</li>
<li>Use a written contract with complete scope, price, schedule, cleanup, special instructions, and written change orders.</li>
</ul>
"""
    write("compliance.html", "Compliance", "Neutral official permit, licensing, insurance, and contract guidance; no job-specific exemption assumed.", body)

    # Sources
    def source_rows(kind_filter):
        return [[e(s["title"]), e(s["type"]), a(s["url"], "Open source", "src"), e(s["method"])] for s in sources if kind_filter(s)]
    body = f"""
<h2>Sources</h2>
<p>Every published data row links a source. Source type matters: a regulator record verifies license fields; a company page verifies only what the company publishes; a review platform verifies only its own displayed statements; owner testimony is not independently verified.</p>
<h3>Government, code, manufacturer, and platform documentation</h3>
{table('Primary guidance and technical context', ['Title', 'Type', 'Link', 'Method / limit'], source_rows(lambda s: s['type'] in {'Government', 'Government code publisher', 'Manufacturer', 'Official platform documentation'}), 900)}
<h3>CSLB contractor records</h3>
{table('Regulator records read directly', ['Title', 'Type', 'Link', 'Method / limit'], source_rows(lambda s: s['type'] == 'Government regulator record' or s['type'] == 'Government regulator lookup'), 900)}
<h3>Company-published service pages</h3>
{table('Business self-description, not independent performance proof', ['Title', 'Type', 'Link', 'Method / limit'], source_rows(lambda s: s['type'] == 'Business self-description'), 900)}
<h3>Review and complaint platforms</h3>
{table('Platform evidence only', ['Title', 'Type', 'Link', 'Method / limit'], source_rows(lambda s: s['type'] in {'Review platform', 'Review/complaint platform'}), 900)}
<h3>Repository provenance</h3>
{table('Repository and coordination sources', ['Title', 'Type', 'Link', 'Method / limit'], source_rows(lambda s: s['type'] == 'Repository'), 900)}
"""
    write("sources.html", "Sources", "Source register separated by evidence type, with access methods and limits.", body)

    # Flagged
    flag_rows = []
    for f in flags["flags"]:
        flag_rows.append([
            f'<span id="{e(f["id"])}"></span><strong>{e(f["title"])}</strong>',
            e(f["detail"]),
            e(f["action"]),
            a(f["source"], f["source_label"], "src"),
            badge("Value blank" if f["blank"] else "Review item", "warn" if f["blank"] else "info"),
        ])
    body = f"""
<h2>Flagged for review</h2>
<p>Unverified and irregular items are published here rather than hidden or guessed. Flagged items do not block publication of the dashboard, but they do block treating a value or provider as confirmed.</p>
{table('Open verification items and irregularities', ['Item', 'Detail', 'Required action', 'Source / context', 'Type'], flag_rows, 1050)}
"""
    write("flagged.html", "Flagged for review", "Unverified values, discrepancies, disclosures, and open verification actions.", body)

    # Verification
    lic_rows = []
    for p in verified:
        lic_rows.append([
            e(p["name"]),
            a(p["cslb_url"], f'#{p["license"]}', "src"),
            e(p["status"]),
            e(p["expires"]),
            "<ul>" + "".join(f"<li>{e(c)}</li>" for c in p["classifications"]) + "</ul>",
            f'${p["bond_usd"]:,}',
            e(p["workers_comp"]),
        ])
    body = f"""
<h2>Verification</h2>
<p>Evidence checked {e(checked)}. License status is a snapshot and must be rechecked on the day of hiring. Automated build/link/blank-value checks are recorded in {a('data/validation.json', 'the validation report')} after verification runs.</p>
<h3>Evidence hierarchy</h3>
<ol class="steps">
<li><strong>Government regulator/code:</strong> CSLB license fields, SF DBI/code guidance.</li>
<li><strong>Manufacturer:</strong> model-specific technical instructions; not a diagnosis of an unknown installed model.</li>
<li><strong>Business self-description:</strong> what a company publishes about its services; not independent proof of performance.</li>
<li><strong>Review platform:</strong> what Yelp/BBB display; not licensing or exact job-fit proof.</li>
<li><strong>Owner testimony:</strong> site conditions and estimate scopes; unconfirmed values remain blank.</li>
</ol>
{table('CSLB records read directly', ['Provider', 'License', 'Status', 'Expires', 'Classifications', 'Bond', 'Workers’ compensation record'], lic_rows, 1100)}
<h3>Automated checks</h3>
<p>The build is deterministic and stdlib-only. Verification checks internal links/anchors, table-row source links, blank unconfirmed values, HTML structure, privacy wording, and canonical data consistency. See {a(f'{REPO_URL}/blob/main/scripts/verify_repair_dashboard.py', 'verifier script')} and {a(f'{REPO_URL}/blob/main/tests/test_repair_dashboard.py', 'regression tests')}.</p>
"""
    write("verification.html", "Verification", "Method, evidence hierarchy, regulator snapshot, and automated validation links.", body)

    # Archive
    archive_rows = [
        ["Pre-integration repository snapshot", a(f"{REPO_URL}/tree/{PRE_INTEGRATION_SHA}", "Immutable tree", "src"), "Starting point before the parallel dashboard sessions; preserved in Git."],
        ["Last parallel-session main snapshot", a(f"{REPO_URL}/tree/{LAST_PARALLEL_SHA}", "Tree at last parallel merge", "src"), "Root and historical page sets before this canonical consolidation."],
        ["Earlier bath microsite", a(f"{REPO_URL}/tree/{PRE_INTEGRATION_SHA}/docs/bath", "docs/bath snapshot", "src"), "Alternate generated site preserved in history; not the canonical live site."],
        ["Earlier overflow dashboard", a(f"{REPO_URL}/blob/{PRE_INTEGRATION_SHA}/docs/plumbing-index.html", "docs/plumbing-index.html snapshot", "src"), "Earlier page set preserved in history."],
        ["Earlier bathtub-overflow microsite", a(f"{REPO_URL}/tree/{PRE_INTEGRATION_SHA}/bathtub-overflow", "bathtub-overflow snapshot", "src"), "Earlier page set preserved in history."],
        ["Legacy GEMS project", a(f"{REPO_URL}/tree/{PRE_INTEGRATION_SHA}/docs", "docs snapshot", "src"), "Unrelated scientific project preserved in the repository; excluded from the canonical published artifact and not reverified for this repair."],
    ]
    body = f"""
<h2>Archive and legacy separation</h2>
<p>This integration publishes one canonical repair dashboard. Earlier bathtub/overflow/bath page sets and the unrelated legacy GEMS project remain preserved in Git. Old project entry URLs redirect to the canonical dashboard or this archive so readers are not left on conflicting live versions.</p>
{table('Immutable historical references', ['Item', 'Link', 'Note'], archive_rows, 850)}
<div class="callout">Historical files may contain earlier unverified values or superseded conclusions. Use the canonical pages and {a('flagged.html', 'Flagged for review')} for current evidence limits.</div>
"""
    write("archive.html", "Archive", "Immutable historical snapshots and legacy GEMS separation.", body)

    # Compatibility redirects for old project entry points. These are not data pages.
    redirects = {
        "bathtub-overflow/index.html": "index.html",
        "docs/plumbing-index.html": "index.html",
        "docs/bath/index.html": "index.html",
        "docs/index.html": "archive.html",
    }
    for old in ["docs/overflow-analysis.html", "docs/overflow-contractors.html", "docs/overflow-estimates.html", "docs/overflow-executive-summary.html", "docs/overflow-flagged-review.html", "docs/overflow-permits.html", "docs/overflow-sources.html", "docs/overflow-verification-flags.html", "docs/overflow-verification-permits.html"]:
        redirects[old] = "archive.html"
    for old, target in redirects.items():
        path = output / old
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../../{e(target)}"><title>Redirecting</title></head><body><p>This historical project page is preserved in Git. Continue to the <a href="../../{e(target)}">canonical repair dashboard</a>.</p></body></html>\n""", encoding="utf-8")
    # Fix relative redirect depth per path.
    for old, target in redirects.items():
        path = output / old
        depth = len(Path(old).parts) - 1
        rel = "../" * depth + target
        path.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={e(rel)}"><title>Redirecting</title></head><body><p>This historical project page is preserved in Git. Continue to the <a href="{e(rel)}">canonical repair dashboard</a>.</p></body></html>\n""", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=REPO, help="Output directory (default: repository root for canonical pages)")
    args = ap.parse_args()
    build(args.output.resolve())
    print(f"Built canonical repair dashboard in {args.output.resolve()}")


if __name__ == "__main__":
    main()
