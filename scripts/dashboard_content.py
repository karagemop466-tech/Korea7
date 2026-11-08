"""Canonical content for the bathtub-overflow trip-lever dashboard.

Single source of truth: data/review-2026-11-08/research.json. Every table row
cites source ids. Values that cannot be confirmed from an official government or
manufacturer source are blank in verified-value cells and flagged UNVERIFIED.
Owner-provided figures and third-party review snapshots are labeled separately.
Ranking is an evidence-based interview order, not a performance guarantee.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PATH = ROOT / "data" / "review-2026-11-08" / "research.json"
DATA = json.loads(RESEARCH_PATH.read_text(encoding="utf-8"))

META = DATA["meta"]
SOURCES = DATA["sources"]
CONTRACTORS = DATA["contractors"]
ESTIMATES = DATA["estimates"]
BENCHMARKS = DATA["benchmarks"]
TECHNICAL = DATA["technical"]
REQUIREMENTS = DATA["requirements"]
FLAGS = DATA["flags"]
CRITERIA = DATA["decision_criteria"]

NAV = [
    {"group": "Overview", "links": [
        ("index.html", "Dashboard"),
        ("summary.html", "Executive summary"),
        ("requirements.html", "Requirements"),
    ]},
    {"group": "Decision", "links": [
        ("contractors.html", "Contractors & ranking"),
        ("estimates.html", "Estimates & costs"),
        ("findings.html", "Findings & analysis"),
    ]},
    {"group": "Reference", "links": [
        ("technical.html", "Technical background"),
        ("permits.html", "Permits & licensing"),
        ("brief.html", "Project brief"),
        ("sources.html", "Source ledger"),
    ]},
    {"group": "Audit", "links": [
        ("verification.html", "Verification"),
        ("repo-review.html", "Repo review"),
        ("flagged.html", "Flagged for review"),
    ]},
]


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def pill(text: str, tone: str = "info") -> str:
    return '<span class="pill %s">%s</span>' % (tone, esc(text))


def slink(sid: str, label: str | None = None) -> str:
    s = SOURCES[sid]
    text = label or s["label"]
    url = s["url"]
    if url.startswith("http"):
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (esc(url), esc(text))
    return '<a href="%s">%s</a>' % (esc(url), esc(text))


BLANK = '<span class="blank" aria-label="blank — unverified"></span>'
UNVERIFIED = pill("UNVERIFIED", "warn")
BF = BLANK + " " + UNVERIFIED
OWNER_STATUS = UNVERIFIED + "<br><small>owner-provided — no official source exists</small>"


def blank_if_empty(value: str) -> str:
    return esc(value) if value else BF


def table(title: str, columns: list[str], rows: list[dict], caption: str) -> dict:
    return {"title": title, "columns": columns + ["Source"], "rows": rows, "caption": caption}


def row(cells: list[str], src: list[str]) -> dict:
    return {"cells": cells, "src": src}


TABLES: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# Problem / brief
# ---------------------------------------------------------------------------
problem_items = [
    ("Failed component", "Bathtub wastewater overflow trip lever stuck inside concealed plumbing behind the wall.", "S14"),
    ("Access problem", "Hard-to-reach overflow; owner reports 5+ licensed plumbers declined above-removal because of concern for hidden plumbing damage.", "S56"),
    ("Reported fallback", "Work from below; a storage unit is underneath and the drywall ceiling may need to be opened.", "S14"),
    ("Service requirement", "One provider for plumbing and drywall restoration; delicate work in a tenant-occupied unit.", "S54"),
    ("Preference", "Removal from above is preferred if it can be done safely.", "S56"),
    ("Location", "San Francisco, California.", "S01"),
    ("Pictures", "Owner said reference pictures might be provided; none were supplied to this session.", "S56"),
]
TABLES["problem"] = table(
    "Problem snapshot — owner-provided, not independently verified",
    ["Item", "Detail as provided", "Verified value", "Provenance"],
    [row([esc(item), esc(detail), BF, pill("owner-provided", "info")], ["S57", ctx])
     for item, detail, ctx in problem_items],
    "These facts come from the " + slink("S57", "project brief") + ". Context links describe the component or rule; they do not confirm the installed condition. Verified value cells are blank and flagged.",
)

TABLES["brief_quotes"] = table(
    "Brief transcription — quoted amounts (NOT verified)",
    ["#", "Company", "Quoted scope (transcription)", "Amount as stated in brief", "Date heading", "Status", "Record type"],
    [row([str(i), esc(e["company"]), esc(e["scope"]), "<strong>%s</strong>" % esc(e["reported_amount"]),
          esc(e["date_heading"]), OWNER_STATUS, pill("primary record only", "mute")],
         ["S57", e["cslb"]]) for i, e in enumerate(ESTIMATES, 1)],
    "Transcription of the owner's brief, not a verification table. The date is the brief heading, not an independently verified quote date. Source: " + slink("S57", "project brief") + ".",
)

# ---------------------------------------------------------------------------
# Estimates and costs
# ---------------------------------------------------------------------------
estimate_contractor = {"expert": "expert", "bay": "bay-area", "fast": "fast-response"}
estimate_rows = []
for i, e in enumerate(ESTIMATES, 1):
    c = next(c for c in CONTRACTORS if c["id"] == estimate_contractor[e["id"]])
    estimate_rows.append(row([str(i),
          "<strong>%s</strong><br>%s · %s" % (esc(e["company"]), slink(c["site"], "official site"), slink(c["cslb"], "CSLB #" + c["license"])),
          esc(e["scope"]),
          "<strong>%s</strong> %s" % (esc(e["reported_amount"]), pill("reported", "mute")),
          BF, esc(e["date_heading"]), OWNER_STATUS],
         ["S57", c["cslb"], c["site"]]))
TABLES["estimates"] = table(
    "Estimates received — brief heading 2026-08-30",
    ["#", "Company", "Scope as reported", "Reported amount (unverified)", "Verified amount", "Date heading in brief", "Verification"],
    estimate_rows,
    "Reported amounts are separated from verified amounts. No official public source confirms these private quotes, so verified amount cells are blank. Company identity/license is verified on CSLB; quote contents are not.",
)

TABLES["estimate_analysis"] = table(
    "Why the three reported amounts are not comparable",
    ["Company", "Reported amount", "What the wording may cover", "What is not confirmed", "Cost reasoning"],
    [row([esc(e["company"]), esc(e["reported_amount"]) + " " + pill("unverified", "warn"),
          esc(e["scope"]), esc(e["includes"]), esc(e["analysis"])],
         ["S57", e["cslb"], "S55"]) for e in ESTIMATES],
    "CSLB guidance says to compare written bids on identical scope and not automatically accept the lowest bid. " + slink("S55", "CSLB hiring guidance") + ".",
)

TABLES["benchmarks"] = table(
    "Publisher cost benchmarks — context only, not official quotes",
    ["Benchmark", "Publisher-stated value (not an official quote)", "Official/project quote", "Publisher date", "Scope caveat"],
    [row([esc(b["label"]), esc(b["value"]), BF, esc(b["date"]), esc(b["caveat"])],
         [b["src"], "S55"]) for b in BENCHMARKS],
    "These are national publisher cost guides, not official tariffs, San Francisco bids or prices for this concealed-access job. The official/project quote column is blank and flagged. Compare local written bids on identical scope: " + slink("S55", "CSLB") + ".",
)

# ---------------------------------------------------------------------------
# Contractors
# ---------------------------------------------------------------------------
def company_links(c: dict) -> str:
    parts = ["<strong>%s</strong>" % esc(c["name"])]
    if c["site"]:
        parts.append(slink(c["site"], "official site"))
    if c["yelp"]:
        parts.append(slink(c["yelp"], "Yelp"))
    return "<br>".join(parts)


def phone_cell(c: dict) -> str:
    parts = []
    if c["phone_cslb"]:
        parts.append("CSLB: " + esc(c["phone_cslb"]))
    if c["phone_site"] and c["phone_site"] != c["phone_cslb"]:
        parts.append("Site: " + esc(c["phone_site"]))
    return "<br>".join(parts) if parts else BF


license_rows = []
for c in CONTRACTORS:
    if c["license"]:
        lic = slink(c["cslb"], "#" + c["license"])
        classes = esc(c["classes"])
        status = esc(c["status"]) + "<br>expires " + esc(c["expiry"])
        if c["id"] == "sugar-bear":
            status += " " + pill("entity match unverified", "warn")
        bond_wc = esc(c["bond"]) + "<br>" + pill(c["wc"], c["wc_tone"])
        address = esc(c["address"])
        src = [c["cslb"], "S04", "S05"]
        if c["site"]:
            src.append(c["site"])
        if c["yelp"]:
            src.append(c["yelp"])
    else:
        lic = BF
        classes = BF
        status = BF
        bond_wc = BF
        address = BF
        src = ["S04", "S33", "S63"]
    license_rows.append(row([company_links(c), lic, classes, status, phone_cell(c), bond_wc, address], src))

TABLES["contractors"] = table(
    "Contractor records — CSLB re-read 2026-11-08",
    ["Company", "CSLB license", "Classifications", "Status / expiry", "Phone (source-labeled)", "Bond / workers' compensation", "Address on record"],
    license_rows,
    "License facts were read directly from CSLB records stamped 11/8/2026. Company phone numbers are labeled by source. Blank cells are unverified. A license class is not proof of job-specific skill, drywall inclusion or availability. Recheck on the hire date: " + slink("S04", "CSLB Check a License") + ".",
)

ranked = sorted([c for c in CONTRACTORS if c["rank"]], key=lambda c: c["rank"])
decision_rows = []
for c in ranked:
    drywall = (esc(c["drywall"]) + "<br>" + slink(c["drywall_src"], "company page")) if c["drywall_src"] else BF
    occupied = (esc(c["occupied"]) + "<br>" + pill("self-published / platform lead", "mute") + " " + slink(c["occupied_src"], "source")) if c["occupied_src"] else BF
    reasoning = esc(c["rationale"]) + "<br><strong>Cost:</strong> " + esc(c["cost"]) + "<br><strong>Caution:</strong> " + esc(c["caution"])
    src = [c["cslb"], c["site"], "S54", "S05", "S55"] + c["extra"]
    if c["quote"]:
        src.append("S57")
    decision_rows.append(row([str(c["rank"]), "<strong>%s</strong><br>%s" % (esc(c["name"]), slink(c["cslb"], "CSLB #" + c["license"])),
                              esc(c["classes"]) + "<br>" + pill(c["group"], "ok" if "B + C-36" in c["group"] else "info"),
                              drywall, occupied, BF, reasoning], src))

TABLES["decision"] = table(
    "Ranked interview order — decision analysis, not a hire guarantee",
    ["Rank", "Company", "Verified license fit", "Published combined-scope evidence", "Occupied-unit evidence", "Verified combined price", "Reasoning, cost note and caution"],
    decision_rows,
    "Rank is this project's evidence-based interview order: license fit first, then published combined scope, occupied-unit/insurance evidence and quote clarity. It is not an official rating, performance guarantee or job acceptance. Verified combined price is blank for every candidate because no all-in quote was confirmed. No provider has been contacted and no provider has confirmed this job.",
)

additional = [c for c in CONTRACTORS if not c["rank"]]
TABLES["additional_leads"] = table(
    "Additional leads — not ranked",
    ["Lead", "CSLB / entity", "Why it is not ranked", "Evidence limit", "Next step"],
    [row([company_links(c),
          (slink(c["cslb"], "#" + c["license"]) + "<br>" + esc(c["entity"])) if c["license"] else BF,
          esc(c["rationale"]), esc(c["caution"]), esc(c["cost"]) or BF],
         ([c["cslb"], c["site"], "S04"] if c["cslb"] else ["S04", "S33", "S63"]) + c["extra"])
     for c in additional],
    "These leads are retained for review but are not part of the ranked interview order until entity, license and single-contract scope questions are resolved.",
)

TABLES["reviews"] = table(
    "Review-platform evidence — discovery only",
    ["Platform", "What was reviewed", "Usable evidence", "Verified rating/count", "Limitation"],
    [
        row(["Yelp", "San Francisco bathtub-drain and drywall searches plus candidate business pages",
             "Discovery links and indexed category/project captions; no numeric rating used", BF,
             "Direct fetches returned HTTP 403. Ratings/counts are blank and not used in ranking."],
            ["S22", "S23", "S27", "S28", "S04"]),
        row(["Angi", "SF bathtub restoration directory and Sugar Bear profile",
             "Indexed Aug 2018 review describes tenant-occupied SF three-unit plumbing plus ceiling/drywall below a bathtub; July 2026 review mentions wall patching", BF,
             "Customer statements, not official capability findings; older review captured from search index."],
            ["S17", "S53", "S04"]),
        row(["BuildZoom", "SF plumbers and drywall/plaster directories",
             "Separate trade directories with reviews/projects; useful for cross-checking the drywall half", BF,
             "Platform scores/badges are not CSLB verification."],
            ["S18", "S19", "S04"]),
        row(["Thumbtack", "SF bathtub services",
             "Bathtub-service listings and reviews; many results are refinishing rather than concealed waste-and-overflow repair", BF,
             "Platform license badges are not CSLB verification."],
            ["S20", "S04"]),
        row(["BBB", "Expert Plumbing Solutions profile",
             "Not accredited; not currently rated; no BBB complaints in last 3 years; license number on record", BF,
             "BBB does not verify third-party information or endorse businesses."],
            ["S21", "S06"]),
    ],
    "Every row includes the official CSLB lookup for credential checking. Platform ratings/counts are left blank because they are volatile third-party values, not official license or job-capability verification.",
)

# ---------------------------------------------------------------------------
# Technical / permits / requirements / flags
# ---------------------------------------------------------------------------
TABLES["technical"] = table(
    "Technical background — manufacturer facts vs job-specific unknowns",
    ["Topic", "Manufacturer/official fact", "Job-specific determination", "Status"],
    [row([esc(t["topic"]), esc(t["verified"]), BF,
          pill("job-specific unverified", "warn") + ("<br><small>" + esc(t["job"]) + "</small>" if t["job"] else "")],
         t["src"]) for t in TECHNICAL],
    "Manufacturer guidance describes documented products, not the installed assembly. Do not force a seized linkage or cut framing based on this page; the contractor must identify the model and assess access.",
)

permit_items = [
    ("Covered pipe cutting/replacement", "SF.gov: a permit is needed before cutting into or replacing pipes, particularly pipes covered by a wall or buried in the ground.", ["S01", "S03"]),
    ("Limited plumbing exemptions", "SF Plumbing Code §104.2 exempts leak repair and unstopping only when no cutting into or removal of piping/traps is required.", ["S03", "S01"]),
    ("Interior wallboard finish", "SF.gov lists minor repairs to existing interior plaster or wallboard as exempt unless required for fire protection.", ["S02"]),
    ("License classes for a plumbing permit", "SF.gov lists A, B after scope approval, C-4/C-36 for plumbing, C-16 sprinkler, C-20 mechanical and C-54 shower-pan-only scopes.", ["S01", "S54", "S05"]),
    ("Inspection before covering", "SF.gov says to have plumbing/mechanical work inspected before covering pipes; Oatey describes a fill-and-inspect replacement test.", ["S01", "S14"]),
    ("Small-job licensing exemption", "BPC §7048 requires aggregate price under $1,000, casual/minor/inconsequential work, and no building permit; anti-evasion and advertising/employee limits apply.", ["S13", "S55"]),
]
TABLES["permits"] = table(
    "Permits and licensing — neutral official references",
    ["Topic", "Official rule", "Job-specific determination"],
    [row([esc(topic), esc(rule), BF], src) for topic, rule, src in permit_items],
    "No job-specific permit determination is made here. The actual scope, ceiling fire-rating and access method are unknown; the licensed contractor and DBI should determine applicability before work.",
)

TABLES["requirements"] = table(
    "Full requirements register",
    ["ID", "Requirement", "Status", "Verified evidence / value"],
    [row([esc(r["id"]), esc(r["requirement"]),
          pill(r["status"], "ok" if r["status"].startswith("Delivered") else ("warn" if "unverified" in r["status"].lower() or "Pending" in r["status"] else "info")),
          esc(r["evidence"]) if r["evidence"] else BF],
         r["src"]) for r in REQUIREMENTS],
    "Owner-provided facts have blank verified-value cells and are flagged. Process deliverables cite the project's own primary records. No value is inferred.",
)

flag_tone = {"Unverified": "warn", "Scope ambiguity": "warn", "Access limitation": "info", "Insurance follow-up": "warn",
             "Disclosure": "warn", "Source conflict": "warn", "Policy expiry": "warn", "Data irregularity": "info",
             "Contact difference": "info", "Service-area follow-up": "info", "Entity / review limitation": "warn",
             "Scope-dependent compliance": "info", "Repository irregularity": "info", "Coordination": "info",
             "Legacy link irregularity": "info", "Legacy artifact irregularity": "info", "Cost limitation": "info",
             "Review limitation": "info", "Outreach boundary": "info"}
TABLES["flags"] = table(
    "Flagged for Review — non-blocking",
    ["ID", "Type", "Item", "Finding", "Suggested review", "Status"],
    [row([esc(f["id"]), pill(f["severity"], flag_tone.get(f["severity"], "info")), esc(f["item"]),
          esc(f["detail"]), esc(f["action"]), pill("needs review — non-blocking", "warn")], f["src"])
     for f in FLAGS],
    "These items are published for review and do not block the site or merge. Unverified values remain blank in verified-value cells; suggested actions are not claims that the issue has been resolved.",
)

repo_flag_ids = {"F18", "F19", "F20", "F21", "F22"}
TABLES["repo_flags"] = table(
    "Repository irregularities",
    ["ID", "Item", "Finding"],
    [row([esc(f["id"]), esc(f["item"]), esc(f["detail"])], f["src"]) for f in FLAGS if f["id"] in repo_flag_ids],
    "Full line-by-line inventory and hash/link results: " + slink("S72", "repository audit report") + ". Legacy GEMS science was preserved, not revalidated.",
)

TABLES["criteria"] = table(
    "Decision criteria",
    ["Criterion", "Rule applied"],
    [row([esc(c["criterion"]), esc(c["rule"])], c["src"]) for c in CRITERIA],
    "Criteria are applied as an interview order. Unknown job-specific capability is not scored as zero competence; it is left blank and flagged.",
)

TABLES["checklist"] = table(
    "Occupied-unit written-scope checklist",
    ["Checklist item", "What to require in writing"],
    [
        row(["Identify the assembly", "Manufacturer/model if visible, whether the seized part is linkage, drop cylinder/barrel, overflow elbow or another stopper type, and the planned above-access limit."], ["S56", "S14"]),
        row(["Access plan", "Whether a ceiling opening is needed, its proposed location/size, and how concealed joints will be protected before any forcing or cutting."], ["S56", "S14", "S57"]),
        row(["Tenant and storage protection", "Contents protection, dust containment, cleanup, water-shutoff windows and tenant access coordination."], ["S55", "S57"]),
        row(["Testing before close", "Fill/drain and overflow test plan, visual inspection of connections behind the tub, and any required official inspection before covering."], ["S14", "S01"]),
        row(["Restoration", "Ceiling patch, tape, texture, paint, and any fire-rated assembly requirement; who performs each trade."], ["S02", "S38", "S41", "S54"]),
        row(["One contract and price", "Single written scope covering plumbing, access, restoration, protection, testing and permit/inspection responsibilities; change-order process."], ["S55", "S57"]),
        row(["Credentials and insurance", "Hire-date CSLB check, disclosure review, attending-crew workers' compensation and general liability evidence."], ["S04", "S55", "S12"]),
    ],
    "This is a procurement checklist derived from official manufacturer, CSLB and SF guidance plus the owner brief. It is not a quote or a permit determination.",
)

TABLES["source_ledger"] = {
    "title": "Source ledger",
    "columns": ["ID", "Source", "Publisher / tier", "Status", "What it supports / note", "Source"],
    "rows": [],
    "caption": "Official = government issuer; manufacturer = product maker; company = self-published business page; platform = review/discovery directory; publisher = cost/technical article; primary = project record. A source link supports only what its note says.",
}

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def prose(title: str, body: str) -> dict:
    return {"type": "prose", "title": title, "html": body}


def callout(tone: str, body: str) -> dict:
    return {"type": "callout", "tone": tone, "html": body}


def t(ref: str, title: str | None = None) -> dict:
    b = {"type": "table", "ref": ref}
    if title:
        b["title"] = title
    return b


quick_items = [
    {"href": "summary.html", "t": "Executive summary", "d": "Recommendation, verified facts, unknowns and next steps."},
    {"href": "requirements.html", "t": "Requirements", "d": "Full brief and deliverable register, line by line."},
    {"href": "contractors.html", "t": "Contractors & ranking", "d": "CSLB records, ranked interview order, phones and review links."},
    {"href": "estimates.html", "t": "Estimates & costs", "d": "Three reported quotes, blank verified cells and cost context."},
    {"href": "findings.html", "t": "Findings & analysis", "d": "Decision criteria, access options and occupied-unit checklist."},
    {"href": "technical.html", "t": "Technical background", "d": "Manufacturer facts separated from job-specific unknowns."},
    {"href": "permits.html", "t": "Permits & licensing", "d": "Neutral official SF/CSLB/state-law references."},
    {"href": "brief.html", "t": "Project brief", "d": "Owner-provided primary record, clearly unverified."},
    {"href": "sources.html", "t": "Source ledger", "d": "Every source, tier, status and retrieval date."},
    {"href": "verification.html", "t": "Verification", "d": "Row-level source audit, link checks and build results."},
    {"href": "repo-review.html", "t": "Repo review", "d": "Inventory, irregularities and archived material."},
    {"href": "flagged.html", "t": "Flagged for review", "d": "Unverified values and irregularities, non-blocking."},
]

PAGES = {
    "index.html": {
        "title": "Dashboard", "eyebrow": "Repair research · San Francisco · updated " + META["updated"],
        "h1": "Bathtub wastewater overflow trip lever",
        "lede": "A stuck trip lever in concealed plumbing behind the wall. Above-removal is preferred but reportedly unsuccessful; the fallback may require opening a storage-unit ceiling. This dashboard organizes the requirements, estimates, contractor evidence, ranking, official rules and every item still needing review.",
        "sections": [
            {"type": "cards", "items": [
                {"k": "Reported estimates", "v": "3", "s": "Brief heading 2026-08-30 · amounts unverified", "tone": "warn"},
                {"k": "Ranked candidates", "v": "9", "s": "Interview order · no job acceptance confirmed", "tone": "info"},
                {"k": "Official / manufacturer sources", "v": "AUTO_OFFICIAL", "s": "Read " + META["updated"], "tone": "ok"},
                {"k": "Flagged for review", "v": str(len(FLAGS)), "s": "Non-blocking · <a href=\"flagged.html\">review</a>", "tone": "warn"},
            ]},
            t("problem"),
            {"type": "quick", "title": "Browse by category", "items": quick_items},
            callout("ok", "<strong>Source-linked tables.</strong> License facts come from CSLB records stamped 11/8/2026; permit rules from SF.gov and California Legislative Information; technical facts from Oatey/Watco. Company and platform statements are labeled as such."),
            callout("warn", "<strong>Blank means unconfirmed.</strong> Verified-value cells are blank and marked UNVERIFIED when no official source confirms the value. Owner-provided amounts appear only in clearly labeled reported/transcription columns. Nothing is inferred."),
            callout("info", "<strong>Canonical site.</strong> Earlier microsites and the unrelated GEMS project are preserved as archive; see <a href=\"repo-review.html\">Repo review</a>. Shared board: " + slink("S58", "COORDINATION.md") + "."),
        ],
    },
    "summary.html": {
        "title": "Executive summary", "eyebrow": "Overview · updated " + META["updated"],
        "h1": "Executive summary",
        "lede": "Decision-ready summary of the access problem, estimate limits, contractor evidence and next steps.",
        "sections": [
            prose("Recommendation", "<p>Start with <strong>General SF</strong> (" + slink("S09", "CSLB #959843") + ") and <strong>Handyman Heroes</strong> (" + slink("S10", "CSLB #1003394") + ") because they have the clearest reviewed official pages advertising both plumbing and sheetrock/wall repair under a B + C-36 license. Then interview <strong>Ace Plumbing & Rooter</strong> (" + slink("S11", "CSLB #829071") + ") for its broad license set, current workers' compensation record and property-manager workflow. This is an interview order, not a guarantee; no provider has been contacted or accepted the job.</p>"),
            prose("What is verified", "<p>Ten CSLB records were re-read on 2026-11-08: nine ranked candidates plus Sugar Bear Plumbing Inc. Six ranked candidates carry both B General Building and C-36 Plumbing on one record. SF.gov requires a permit before cutting/replacing covered pipes; the Plumbing Code exemptions are limited to work not requiring cutting/removal; minor wallboard repair exemption does not apply when required for fire protection. Oatey and Watco describe the trip-lever mechanism and post-replacement fill-and-inspect test.</p>"),
            prose("What is not verified", "<p>The installed model, seized component, pipe material, ceiling fire-rating, need/size of a ceiling opening, job-specific occupied-unit experience, single-contract drywall inclusion, availability and all-in price remain blank/unverified. The three owner-reported amounts ($614, $550, $135) are not official quotes and describe different scopes. Yelp direct fetches were blocked; numeric ratings are not used.</p>"),
            prose("Cost decision", "<p>Do not choose by the lowest reported amount. The $135 figure is an adjustment scope, $550 mentions a spout/diverter that may be a different mechanism, and $614 mentions waste-and-overflow replacement. None confirms ceiling opening, patch/texture/paint, tenant protection, testing or permit/inspection responsibilities. Require identical written scopes; national Angi ranges are context only. See <a href=\"estimates.html\">Estimates & costs</a>.</p>"),
            prose("Next steps", "<ol><li>Use the <a href=\"contractors.html\">ranked interview order</a> and official phone links.</li><li>Require one written scope using the <a href=\"findings.html\">occupied-unit checklist</a>.</li><li>Recheck CSLB status/disclosures and attending-crew insurance on the hire date.</li><li>Have the contractor and DBI determine permit/inspection applicability for the exact scope.</li><li>Review <a href=\"flagged.html\">Flagged for Review</a> before hiring.</li></ol>"),
            callout("warn", "<strong>Privacy and compliance.</strong> Owner-only context is omitted. Permit content is neutral and official-source-based; no job-specific permit outcome or avoidance instruction is published."),
        ],
    },
    "requirements.html": {
        "title": "Requirements", "eyebrow": "Overview · line-by-line register",
        "h1": "Full requirements register",
        "lede": "Every requirement from the brief and project instructions, with status and source links. Owner-provided facts have blank verified values.",
        "sections": [t("requirements")],
    },
    "estimates.html": {
        "title": "Estimates & costs", "eyebrow": "Decision · reported vs verified",
        "h1": "Estimates and cost analysis",
        "lede": "Three owner-reported estimates are transcribed separately from verified values. No all-in project price is confirmed.",
        "sections": [
            t("estimates"),
            t("estimate_analysis"),
            t("benchmarks"),
            callout("warn", "<strong>No invented total.</strong> Access, ceiling restoration, tenant protection, testing and permit/inspection costs are not confirmed in any reported quote. Do not sum or infer a project total from unlike scopes."),
        ],
    },
    "contractors.html": {
        "title": "Contractors & ranking", "eyebrow": "Decision · CSLB re-read " + META["updated"],
        "h1": "Contractors, contacts and ranked interview order",
        "lede": "Official license records, source-labeled phones, published scope evidence and review discovery links. Ranking is analysis, not an official rating.",
        "sections": [
            callout("info", "<strong>No provider has been contacted</strong> and no provider <strong>has confirmed this job</strong>. Third-party review data is unverified for hiring; use CSLB and written contract/insurance evidence."),
            t("decision"),
            t("contractors"),
            t("additional_leads"),
            t("reviews"),
        ],
    },
    "findings.html": {
        "title": "Findings & analysis", "eyebrow": "Decision · method and checklist",
        "h1": "Findings and decision analysis",
        "lede": "How the interview order was built, what the access options mean, and what to require in writing for an occupied unit.",
        "sections": [
            t("criteria"),
            prose("Access findings", "<p>Manufacturer instructions show plate/linkage service through the overflow opening on documented models, while the overflow elbow/gasket sit behind the tub. That supports trying above-access first <em>only after the contractor identifies the assembly</em>; it does not prove this seized unit can be freed from above. Oatey's replacement test requires inspecting connections behind the tub, so if a ceiling is opened the test/inspection should happen before it is closed. Framing must not be cut without building-official approval.</p>"),
            prose("All-in-one finding", "<p>A B + C-36 record is a licensing fit for a single prime contract, but it is not proof the company will include or self-perform drywall. General SF and Handyman Heroes have the clearest reviewed official combined-service pages. Ace, Genteel, Rapid Flow and Manny's need written confirmation of ceiling restoration. The three quoting plumbers are C-36 only on CSLB, so a single plumbing-plus-drywall contract is not established.</p>"),
            t("checklist"),
            callout("warn", "<strong>Review evidence is a lead, not a guarantee.</strong> The most specific occupied-unit ceiling review found is an old Angi customer statement about Sugar Bear, whose current marketing entity/phone differ from the CSLB corporation; it is kept unranked pending confirmation."),
        ],
    },
    "technical.html": {
        "title": "Technical background", "eyebrow": "Reference · manufacturer sources",
        "h1": "Technical background",
        "lede": "What the manufacturers document, separated from what is unknown about this installed assembly.",
        "sections": [
            t("technical"),
            callout("warn", "<strong>Do not force or improvise.</strong> The installed manufacturer/model is unknown. A licensed contractor should identify the mechanism and assess whether above-removal risks damaging concealed joints before any ceiling cut."),
        ],
    },
    "permits.html": {
        "title": "Permits & licensing", "eyebrow": "Reference · neutral official guidance",
        "h1": "Permits and licensing",
        "lede": "Official San Francisco, CSLB and California statutory references. No job-specific determination is made.",
        "sections": [
            t("permits"),
            callout("info", "<strong>Scope-dependent.</strong> The actual work, ceiling fire-rating and access method are unknown. The licensed contractor and DBI should determine applicability before work. This page does not publish owner-only context or instructions either way."),
        ],
    },
    "brief.html": {
        "title": "Project brief", "eyebrow": "Reference · owner-provided primary record",
        "h1": "Project brief — primary record only",
        "lede": "Transcription of the owner's problem statement and estimate scopes. These are not independently verified facts.",
        "sections": [
            t("problem"),
            t("brief_quotes"),
            callout("warn", "<strong>Primary record, not official verification.</strong> No public source confirms the physical conditions or private quote amounts. Verified-value cells are blank and flagged. Owner-only context is omitted."),
        ],
    },
    "sources.html": {
        "title": "Source ledger", "eyebrow": "Reference · provenance",
        "h1": "Source ledger",
        "lede": "Every source used by the canonical dashboard, with publisher, tier, status, retrieval date and the exact claim it supports.",
        "sections": [
            prose("How to read tiers", "<p><strong>Official</strong> sources are government issuers (CSLB, SF.gov, California Legislative Information). <strong>Manufacturer</strong> sources are product makers (Oatey, Watco). <strong>Company</strong> sources are self-published business pages. <strong>Platform</strong> sources are review/discovery directories. <strong>Publisher</strong> sources are cost/technical articles. <strong>Primary</strong> sources are this project's own records. A link supports only what its note says; it does not verify unrelated owner facts.</p>"),
            t("source_ledger"),
        ],
    },
    "verification.html": {
        "title": "Verification", "eyebrow": "Audit · generated checks",
        "h1": "Verification and line-by-line row audit",
        "lede": "Automated build/link/privacy checks plus a row-level source audit. Source presence is not the same as value verification.",
        "sections": [
            {"type": "verification_summary"},
            {"type": "row_audit"},
            prose("Verification boundaries", "<p>Official license and permit values were read directly from issuing sites on 2026-11-08. Manufacturer facts were read from Oatey/Watco. Company pages verify only what the company publishes. Yelp direct fetches were blocked; numeric ratings are blank. Owner-provided amounts and physical conditions remain unverified. Legacy GEMS science and archived microsites were inventoried, not revalidated. See <a href=\"data/review-2026-11-08/REPO-AUDIT.md\">repository audit</a> and <a href=\"data/canonical/verification_report.json\">machine-readable report</a>.</p>"),
        ],
    },
    "repo-review.html": {
        "title": "Repo review", "eyebrow": "Audit · repository inventory",
        "h1": "Repository review",
        "lede": "What is in this repository, what was checked line by line, and what remains flagged as legacy or irregular.",
        "sections": [
            prose("Scope", "<p>The canonical plumbing dashboard lives at the repository root. The repo also contains an unrelated legacy GEMS geothermal audit and several archived overflow microsites from parallel sessions. This session inventoried tracked files, hashed bytes, parsed JSON/Python, scanned HTML links and re-read official plumbing sources. It did not edit or revalidate legacy GEMS science or archived microsites.</p>"),
            t("repo_flags"),
            prose("Audit artifacts", "<p>Line-by-line inventory and hashes: <a href=\"data/review-2026-11-08/repo_inventory.json\">repo_inventory.json</a>. Findings: <a href=\"data/review-2026-11-08/repo_findings.json\">repo_findings.json</a>. Report: <a href=\"data/review-2026-11-08/REPO-AUDIT.md\">REPO-AUDIT.md</a>. Current research dataset: <a href=\"data/review-2026-11-08/research.json\">research.json</a>.</p>"),
            prose("Archived material", "<p>Preserved unchanged: " + slink("S66", "bathtub-overflow/") + ", " + slink("S67", "docs/bath/") + ", " + slink("S68", "docs overflow dashboard") + ", " + slink("S64", "parallel SF overflow audit") + ", " + slink("S69", "earlier shortlist") + ", " + slink("S70", "prior verification log") + ", and the unrelated " + slink("S65", "legacy GEMS site") + ". Canonical root pages control for this project.</p>"),
        ],
    },
    "flagged.html": {
        "title": "Flagged for review", "eyebrow": "Audit · non-blocking",
        "h1": "Flagged for Review",
        "lede": "Unverified values, source conflicts, access limitations and repository irregularities. These items are published for review and do not block the site or merge.",
        "sections": [
            t("flags"),
            callout("info", "<strong>Needs review does not block.</strong> Each item has source links and a suggested review action. Unverified values remain blank in verified-value cells; no irregularity is silently resolved."),
        ],
    },
}
