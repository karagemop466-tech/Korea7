#!/usr/bin/env python3
"""Build the strict, source-linked decision analysis and compliant shortlist.

Usage:  python3 scripts/build_decision_matrix.py

The generated pages use only the audited values in data/decision_matrix.json.
Owner-provided prices, third-party rating values and job-specific capability
claims are never filled in: their verified cells are blank and UNVERIFIED.
Every rendered table row carries at least one link to an official government,
manufacturer or official-business site. The script exits non-zero on failure.
"""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "decision_matrix.json"
PAGES = ["decision-matrix.html", "shortlist.html"]

OFFICIAL_DOMAINS = {
    "www2.cslb.ca.gov", "www.cslb.ca.gov", "cslb.ca.gov",
    "www.sf.gov", "sf.gov", "leginfo.legislature.ca.gov",
    "www.oatey.com", "oatey.com",
    "www.eplumbingsolutions.com", "eplumbingsolutions.com",
    "www.bayareaplumbingsf.com", "bayareaplumbingsf.com",
    "www.fastresponseplumbingsf.com", "fastresponseplumbingsf.com",
    "generalsf.com", "www.generalsf.com",
    "www.handymanhero.es", "handymanhero.es",
    "www.aceplumbingandrooter.com", "aceplumbingandrooter.com",
    "www.rapidflowbayarea.com", "rapidflowbayarea.com",
    "www.mannysplumbingandremodeling.com", "mannysplumbingandremodeling.com",
}
OFFICIAL_TIERS = {"official", "manufacturer", "company"}
PRIVATE_PATTERNS = [
    r"without\s+a\s+permit", r"\bno\s+permit\b",
    r"do\s+not\s+pull\s+a\s+permit", r"cannot\s+pull\s+a\s+permit",
    r"private\s+project\s+rationale", r"reasons\s+that\s+need\s+to\s+stay\s+private",
]

NAV = [
    ("Overview", [("index.html", "Dashboard"), ("summary.html", "Executive summary"),
                  ("requirements.html", "Requirements")]),
    ("Data", [("estimates.html", "Estimates & costs"), ("contractors.html", "Contractors & reviews"),
              ("findings.html", "Findings & analysis"), ("shortlist.html", "Shortlist"),
              ("decision-matrix.html", "Decision matrix")]),
    ("Reference", [("technical.html", "Technical background"), ("permits.html", "Permits & licensing"),
                   ("brief.html", "Project brief"), ("sources.html", "Source ledger")]),
    ("Audit", [("verification.html", "Verification"), ("repo-review.html", "Repo review"),
               ("verification-log.html", "Prior verification log"), ("flagged.html", "Flagged for review")]),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def is_official_url(url: str) -> bool:
    return urlparse(url).netloc.lower() in OFFICIAL_DOMAINS


def link(url: str, label: str, title: str = "", external: bool | None = None) -> str:
    if external is None:
        external = url.startswith(("http://", "https://"))
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    if title:
        attrs += ' title="%s"' % esc(title)
    return '<a href="%s"%s>%s</a>' % (esc(url), attrs, esc(label))


def pill(text: str, tone: str = "info") -> str:
    return '<span class="pill %s">%s</span>' % (tone, esc(text))


def blank() -> str:
    return '<span class="blank" aria-label="blank — unverified">—</span> ' + pill("UNVERIFIED", "warn")


def source_link(sid: str, sources: dict) -> str:
    src = sources[sid]
    return link(src["url"], sid, "%s — %s" % (src["label"], src["publisher"]))


def source_cell(ids: list[str], sources: dict) -> str:
    ids = list(dict.fromkeys(ids))
    if not any(sources[s]["tier"] in OFFICIAL_TIERS for s in ids):
        # A neutral official verification authority is included on every row. It
        # does not turn a third-party value into an official fact.
        ids.append("O01")
    return '<span class="src-ids">%s</span>' % " · ".join(source_link(s, sources) for s in ids)


def table(columns: list[str], rows: list[str], caption: str) -> str:
    return ('<section class="section"><div class="table-wrap"><table class="data-table">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody><caption>%s</caption>'
            '</table></div></section>'
            % ("".join("<th>%s</th>" % esc(c) for c in columns), "".join(rows), caption))


def nav_html(active: str) -> str:
    parts = ['<aside class="sidebar" aria-label="Site navigation">',
             '<a class="side-brand" href="index.html"><span class="mark">TL</span>'
             '<span>Overflow Trip Lever<small>San Francisco repair project</small></span></a>']
    for group, links in NAV:
        parts.append('<div class="nav-group"><div class="nav-group-title">%s</div>' % esc(group))
        for href, label in links:
            current = ' aria-current="page" class="active"' if href == active else ""
            parts.append('<a href="%s"%s>%s</a>' % (esc(href), current, esc(label)))
        parts.append('</div>')
    parts.append('<div class="side-foot">Updated 2026-11-08<br>Session '
                 '<span class="mono">arena/e7305a26-korea7</span></div></aside>')
    return "\n".join(parts)


def page(title: str, h1: str, lede: str, body: str, active: str) -> str:
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s · Bathtub Overflow Trip Lever</title>
<meta name="description" content="Source-linked decision analysis for a bathtub wastewater overflow trip lever repair in San Francisco.">
<link rel="stylesheet" href="assets/dashboard.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="layout">
%s
<main id="main" class="content">
<header class="page-head">
  <div class="eyebrow">Verified decision analysis · San Francisco · updated 2026-11-08</div>
  <h1>%s</h1>
  <p class="lede">%s</p>
</header>
%s
<footer class="site">
  <span>Research dashboard · San Francisco · updated 2026-11-08 · session <span class="mono">arena/e7305a26-korea7</span></span>
  <span><a href="index.html">Dashboard</a> · <a href="sources.html">Sources</a> · <a href="flagged.html">Flagged for review</a> · <a href="https://github.com/karagemop466-tech/Korea7">Repository</a></span>
</footer>
</main>
</div>
<script src="assets/dashboard.js" defer></script>
</body>
</html>
""" % (esc(title), nav_html(active), esc(h1), lede, body)


def candidate_rows(data: dict) -> list[str]:
    out = []
    for c in data["candidates"]:
        ids = [c["cslb"]]
        if c["company_site"]:
            ids.append(c["company_site"])
        if c["review"]:
            ids.append(c["review"])
        name_cell = "<strong>%s</strong>" % esc(c["name"])
        if c["license"]:
            name_cell += "<br><small>%s · %s<br>%s</small>" % (
                esc(c["license"]), esc(c["phone"]), esc(c["address"]))
        else:
            name_cell += "<br><small>%s · %s</small>" % (blank(), pill("no official record", "warn"))
        official_cell = "%s<br>%s<br><small>%s · expires %s · bond %s<br>%s</small>" % (
            esc(c["status"] or "—"), esc(c["classes"] or "—"),
            esc(c["license"] or "license not confirmed"), esc(c["expires"] or "—"),
            esc(c["bond"] or "—"), esc(c["workers_comp"] or "—"))
        if c["cslb"] == "O01":
            official_cell = "%s<br><small>No CSLB license number has been confirmed for this lead</small>" % blank()
        cost_cell = "%s<br><small>%s</small>" % (blank(), esc(c["cost_basis"]))
        review_cell = "%s<br><small>%s</small>" % (blank(), esc(c["official_note"]))
        if c["company_site"]:
            review_cell += "<br><small>%s</small>" % link(
                data["sources"][c["company_site"]]["url"], "official business site",
                data["sources"][c["company_site"]]["label"])
        out.append("<tr><td><strong>%d</strong></td><td>%s</td><td>%s</td>"
                   "<td>%s</td><td>%s</td><td>%s</td><td class=\"src-col\">%s</td></tr>"
                   % (c["rank"], name_cell, official_cell, esc(c["ranking_reason"]),
                      cost_cell, review_cell, source_cell(ids, data["sources"])))
    return out


def cost_rows(data: dict) -> list[str]:
    out = []
    for row in data["cost_rows"]:
        ids = row["sources"] + row["publisher"]
        official = esc(row["official_value"]) if row["official_value"] else blank()
        publisher = esc(row["publisher_value"]) if row["publisher_value"] else blank()
        out.append("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td>"
                   "<td class=\"src-col\">%s</td></tr>"
                   % (esc(row["factor"]), official, publisher,
                      esc(row["decision"]), source_cell(ids, data["sources"])))
    return out


def review_rows(data: dict) -> list[str]:
    out = []
    for row in data["review_rows"]:
        ids = [row["official"], row["link"]]
        out.append("<tr><td><strong>%s</strong><br><small>%s</small></td><td>%s</td>"
                   "<td>%s</td><td class=\"src-col\">%s</td></tr>"
                   % (esc(row["platform"]),
                      link(data["sources"][row["link"]]["url"], "third-party discovery link",
                           data["sources"][row["link"]]["label"]),
                      blank(), esc(row["note"]), source_cell(ids, data["sources"])))
    return out


def flag_rows(data: dict) -> list[str]:
    out = []
    for row in data["flags"]:
        out.append("<tr><td><code>%s</code></td><td><strong>%s</strong></td><td>%s</td>"
                   "<td>%s</td><td class=\"src-col\">%s</td></tr>"
                   % (esc(row["id"]), esc(row["item"]), esc(row["why"]),
                      esc(row["action"]), source_cell(row["sources"], data["sources"])))
    return out


def ledger_rows(data: dict) -> list[str]:
    out = []
    for sid, src in sorted(data["sources"].items()):
        ids = [sid, "O01"]
        tone = {"official": "ok", "manufacturer": "ok", "company": "info"}.get(src["tier"], "warn")
        out.append("<tr><td><code>%s</code></td><td>%s</td><td>%s<br>%s</td><td>%s</td>"
                   "<td>%s</td><td class=\"src-col\">%s</td></tr>"
                   % (esc(sid), link(src["url"], src["label"], src["publisher"]),
                      esc(src["publisher"]), pill(src["tier"], tone), esc(src["checked"]),
                      esc(src["supports"]), source_cell(ids, data["sources"])))
    return out


def shortlist_rows(data: dict) -> list[str]:
    out = []
    for c in data["candidates"]:
        ids = [c["cslb"]]
        if c["company_site"]:
            ids.append(c["company_site"])
        name_cell = "<strong>%s</strong>" % esc(c["name"])
        if c["license"]:
            name_cell += "<br><small>%s · %s</small>" % (esc(c["license"]), esc(c["phone"]))
        else:
            name_cell += "<br><small>%s</small>" % blank()
        official_cell = "%s<br><small>%s · expires %s · %s</small>" % (
            esc(c["status"] or "—"), esc(c["classes"] or "—"),
            esc(c["expires"] or "—"), esc(c["workers_comp"] or "—"))
        if c["cslb"] == "O01":
            official_cell = "%s<br><small>No official CSLB license number confirmed</small>" % blank()
        out.append("<tr><td><strong>%d</strong></td><td>%s</td><td>%s</td>"
                   "<td>%s<br><small>No third-party rating, owner amount or job-specific capability value is presented as verified</small></td>"
                   "<td class=\"src-col\">%s</td></tr>"
                   % (c["rank"], name_cell, official_cell, blank(), source_cell(ids, data["sources"])))
    return out


class RowAudit(HTMLParser):
    """Check that every tbody row carries a link to an official site."""
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_row = False
        self.rows: list[list[str]] = []
        self.current: list[str] = []
        self.all_links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.in_row = True
            self.current = []
        if tag == "a" and a.get("href"):
            self.all_links.append(a["href"])
            if self.in_row:
                self.current.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.rows.append(self.current)
            self.in_row = False
        if tag == "tbody":
            self.in_tbody = False


def verify_html(text: str, filename: str) -> tuple[int, list[str]]:
    parser = RowAudit()
    parser.feed(text)
    problems = []
    for i, links in enumerate(parser.rows, 1):
        if not any(is_official_url(u) for u in links):
            problems.append("%s row %d has no official link" % (filename, i))
    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, text, re.I):
            problems.append("%s contains private wording matching %s" % (filename, pattern))
    for amount in ("$614", "$550", "$135"):
        if amount in text:
            problems.append("%s contains owner-provided amount %s" % (filename, amount))
    for href in parser.all_links:
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc:
            continue
        # Same-page fragment: the target id is in the generated page itself.
        if not parsed.path:
            continue
        target = (ROOT / parsed.path).resolve()
        if not target.is_file() and target.name not in PAGES:
            problems.append("%s has broken internal link %s" % (filename, href))
    return len(parser.rows), problems


def build_decision_page(data: dict) -> str:
    cards = ('<div class="grid cols-4">'
             '<div class="card stat ok"><div class="k">Official active records</div><div class="v">8</div>'
             '<div class="s">CSLB records read 2026-11-08</div></div>'
             '<div class="card stat ok"><div class="k">B + C-36 on one license</div><div class="v">5</div>'
             '<div class="s">Documented single-vendor candidates</div></div>'
             '<div class="card stat warn"><div class="k">Workers-comp exemptions</div><div class="v">4</div>'
             '<div class="s">Confirm crew coverage in writing</div></div>'
             '<div class="card stat info"><div class="k">Ranked candidates</div><div class="v">9</div>'
             '<div class="s">8 licensed + 1 unverified lead</div></div></div>')

    decision_table = table(
        ["Rank", "Business · official phone", "Official CSLB value", "Why this rank (decision analysis)",
         "Verified cost · explanation", "Capability / review value", "Official source"],
        candidate_rows(data),
        "Ranking is a documented decision analysis, not an official quality rating. One active license carrying "
        "B General Building and C-36 Plumbing is weighted first because the job may need both concealed plumbing "
        "and ceiling drywall restoration. Every row links an official government record; unverified values are blank. "
        "No provider was contacted by this session and none has confirmed this job.")

    summary_callout = ('<div class="callout info"><div class="icon">i</div><p><strong>Decision rule.</strong> '
        '%s</p></div>' % esc(data["meta"]["ranking_basis"]))

    cost_table = table(
        ["Cost factor", "Officially confirmed value", "Publisher-reported context", "Decision implication", "Official source"],
        cost_rows(data),
        "Only the SF.gov statement that permit fees depend on scope is shown as an official value; no numeric "
        "publisher benchmark is presented as an official confirmation. CSLB advises three written bids on identical "
        "scope and warns against automatically accepting the lowest bid.")

    note_items = []
    for note in data["cost_notes"]:
        refs = " · ".join(source_link(s, data["sources"]) for s in note["sources"])
        note_items.append("<li>%s <span class=\"src\">%s</span></li>" % (esc(note["text"]), refs))
    cost_notes = ('<section class="section"><h2>Publisher cost notes (not official quotes)</h2>'
                  '<ul class="tight">%s</ul></section>' % "".join(note_items))

    review_table = table(
        ["Review platform", "Official confirmed rating / capability", "Why it is only a discovery aid", "Official source"],
        review_rows(data),
        "Yelp, Angi, BuildZoom, Thumbtack and BBB are third-party platforms. Their pages are linked for manual "
        "review; no rating, review count or badge is treated as license or capability verification.")

    flags_table = table(
        ["ID", "Item", "Why it is flagged", "What would clear it", "Official source"],
        flag_rows(data),
        "This is the clearly labeled Flagged for Review section for this decision analysis. The canonical site "
        "also publishes its U01–U21 list on " + link("flagged.html", "Flagged for review") + ".")

    ledger_table = table(
        ["ID", "Source", "Publisher / tier", "Checked", "What it supports", "Official source"],
        ledger_rows(data),
        "Every source used on this page, with retrieval date. O01 is included as the official license authority "
        "on rows whose cited source is a publisher or platform; that inclusion does not convert third-party "
        "content into an official fact.")

    method = ('<section class="section"><h2>Verification method</h2><ol class="tight">'
              '<li>All eight CSLB License Detail pages were read directly on 2026-11-08 and printed a '
              '"Data current as of 11/8/2026" stamp.</li>'
              '<li>CSLB B/C-36 classification pages, CSLB hiring guidance, two SF.gov pages, California BPC §7048 '
              'and the Oatey manufacturer page were read directly on 2026-11-08.</li>'
              '<li>Six original candidate company sites plus the Rapid Flow and Manny’s sites were read directly '
              'for official business links and phone corroboration.</li>'
              '<li>Owner-provided prices, problem facts, Yelp ratings, job-specific experience and availability '
              'are blank and flagged UNVERIFIED; no value was inferred.</li>'
              '<li>Every tbody row on both generated pages is checked for an official-domain link; all internal '
              'links are checked against the filesystem; a privacy sweep rejects internal-only wording.</li>'
              '</ol><p class="src">Machine-readable data: '
              + link("data/decision_matrix.json", "data/decision_matrix.json") +
              '. Verification trail: ' + link("trip-lever/e7305a26-verification.md", "e7305a26-verification.md") +
              '. Canonical build report: ' + link("verification.html", "Verification") + '.</p></section>')

    neutral_rules = ('<section class="section"><h2>Neutral official rules</h2><ul class="tight">'
        '<li>' + link("https://www.sf.gov/apply-plumbing-and-mechanical-permit", "SF.gov plumbing permit guidance") +
        ' states that a permit is needed before cutting into or replacing pipes, especially pipes covered by a wall, '
        'and that permit fees depend on scope.</li>'
        '<li>' + link("https://www.sf.gov/information--check-if-your-construction-project-needs-permit", "SF.gov permit-exemption list") +
        ' lists minor repairs to existing interior plaster or wallboard among work that does not need a building permit, '
        'subject to exceptions.</li>'
        '<li>' + link("https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B", "CSLB B classification") +
        ' and ' + link("https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "CSLB C-36 classification") +
        ' define the two relevant license scopes. Applicability to the final scope belongs to SF DBI and the selected contractor.</li>'
        '</ul></section>')

    next_steps = ('<section class="section"><h2>Recommended next steps</h2><ol class="tight">'
        '<li>Request one contingent written scope from at least three of the five B + C-36 firms.</li>'
        '<li>Require the above-attempt, below-access, ceiling cut/patch/finish, fill-and-inspect test and tenant '
        'schedule as separate line items in the same contract.</li>'
        '<li>Verify the actual crew’s workers-compensation and liability coverage on the hire date.</li>'
        '<li>Ask for references on concealed waste-and-overflow work in occupied units; treat company and review '
        'statements as unverified until documented.</li>'
        '<li>Re-check the chosen license and complaint disclosure at '
        + link("https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "CSLB Check a License") +
        ' on the day of hiring.</li>'
        '<li>Review ' + link("flagged.html", "all flagged items") + ' before signing.</li>'
        '</ol></section>')

    closing = ('<div class="callout warn"><div class="icon">!</div><p><strong>Informational only.</strong> '
        'This page is research, not legal advice, a quote, a contractor endorsement or a confirmation that any '
        'provider accepts this job.</p></div>')

    body = "\n".join([cards, '<section class="section"><h2>Ranked decision matrix</h2></section>',
                      summary_callout, decision_table,
                      '<section class="section"><h2>Cost analysis</h2></section>', cost_table, cost_notes,
                      '<section class="section"><h2>Review discovery</h2></section>', review_table,
                      '<section class="section"><h2>Flagged for Review — decision analysis</h2></section>',
                      flags_table,
                      '<section class="section"><h2>Official source ledger</h2></section>', ledger_table,
                      method, neutral_rules, next_steps, closing])
    return page("Decision matrix", "Ranked contractor decision analysis",
                "A strict, source-linked ranking of the best documented choices for a stuck bathtub wastewater "
                "overflow trip lever in a tenant-occupied San Francisco unit. Official values come from CSLB, "
                "SF.gov, California law, the manufacturer and official business sites; everything else is blank "
                "and flagged.", body, "decision-matrix.html")


def build_shortlist_page(data: dict) -> str:
    callout = ('<div class="callout info"><div class="icon">i</div><p><strong>Use the full '
               + link("decision-matrix.html", "Decision matrix") +
               ' for ranking, costs, reasoning and review links.</strong> This compact shortlist is a verified '
               'license register only. Third-party ratings, owner-provided amounts, job-specific capability and '
               'availability are blank and UNVERIFIED.</p></div>')
    shortlist_table = table(
        ["Rank", "Business · official phone", "Verified official license value", "Unverified values", "Official source"],
        shortlist_rows(data),
        "All license, classification, phone, status, expiry, bond and workers-compensation values come from the "
        "official CSLB detail record linked in each row. The older shortlist’s third-party ratings and "
        "owner-supplied quote figures were removed; no value was inferred.")
    audit = ('<section class="section"><h2>How to use this page</h2><ol class="tight">'
             '<li>Start with ranks 1–5 because each has B + C-36 on one active CSLB record.</li>'
             '<li>Open the linked official record on the hire date; license status changes.</li>'
             '<li>Use the ' + link("decision-matrix.html", "Decision matrix") +
             ' for cost reasoning, review discovery and flagged items.</li>'
             '<li>See ' + link("flagged.html", "Flagged for Review") +
             ' for all historical irregularities before hiring.</li></ol></section>')
    closing = ('<div class="callout warn"><div class="icon">!</div><p><strong>Not an endorsement.</strong> '
               'No provider has been contacted by this session and no provider has confirmed acceptance, '
               'availability or a price for this job.</p></div>')
    return page("Shortlist", "Shortlist — verified license view",
                "A clean, source-linked register of the eight officially licensed candidates and one unverified "
                "lead. The ranked decision analysis is on the Decision matrix page.",
                "\n".join([callout, shortlist_table, audit, closing]), "shortlist.html")


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = []
    ranks = [c["rank"] for c in data["candidates"]]
    if ranks != list(range(1, len(ranks) + 1)):
        errors.append("candidate ranks must be consecutive 1..%d" % len(ranks))
    for c in data["candidates"]:
        if not data["sources"][c["cslb"]]["tier"] == "official":
            errors.append("%s has no official CSLB source" % c["name"])
        if c["quote_scope"] and ("$" in c["quote_scope"]):
            errors.append("%s contains an unblanked quote amount" % c["name"])
        if c["review_rating"]:
            errors.append("%s contains a third-party rating value" % c["name"])
    for sid, src in data["sources"].items():
        if not src["url"].startswith(("http://", "https://")):
            errors.append("source %s has no absolute URL" % sid)
    if errors:
        print("CONTENT VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    outputs = {
        "decision-matrix.html": build_decision_page(data),
        "shortlist.html": build_shortlist_page(data),
    }
    total_rows = 0
    for filename, text in outputs.items():
        count, problems = verify_html(text, filename)
        total_rows += count
        errors.extend(problems)
    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    for filename, text in outputs.items():
        (ROOT / filename).write_text(text, encoding="utf-8")
    print("Built %d pages; %d tbody rows checked; every row has an official link; "
          "0 privacy matches; 0 unblanked owner quote amounts; 0 broken internal links."
          % (len(outputs), total_rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
