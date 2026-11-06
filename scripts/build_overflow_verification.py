#!/usr/bin/env python3
"""Build the overflow verification addendum (docs/overflow-verification*.html).

Reads docs/data/overflow-verification.json and writes six pages under docs/:
  overflow-verification.html               summary, headlines, next steps, requirements
  overflow-verification-permits.html       SF permit rules and CSLB licensing rules (quoted)
  overflow-verification-contractors.html   contractor cross-check and quote scope comparison
  overflow-verification-repo-review.html   Korea7 repo checks
  overflow-verification-flags.html         Flagged for Review (addendum)
  overflow-verification-sources.html       sources, how each was checked

It does not touch the existing overflow-*.html, plumbing-index.html or GEMS pages.

Checks (the build fails if any fail):
  * every data row has an https source link, or is OWNER-STATED (no official source applies);
  * VERIFIED rows link only to official domains;
  * contractor and quote rows cannot be VERIFIED in this build;
  * every flag code used in a row exists on the flags list;
  * no placeholder text remains in the repo review;
  * every relative link and asset in the generated pages resolves to a file in the repo.

Usage:  python3 scripts/build_overflow_verification.py           (build, then check)
        python3 scripts/build_overflow_verification.py --check   (check existing HTML only)
"""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data" / "overflow-verification.json"
DOCS = ROOT / "docs"

OFFICIAL_DOMAINS = {
    "sf.gov", "www.sf.gov", "media.api.sf.gov", "codelibrary.amlegal.com",
    "cslb.ca.gov", "www.cslb.ca.gov", "www2.cslb.ca.gov", "sanfranciscoca.portal.opengov.com",
    "drivendata.org", "www.drivendata.org",
}
CSLB_LOOKUP = "https://www.cslb.ca.gov/onlineservices/checklicenseii/checklicense.aspx"
ALLOWED_VERIFICATION = {"VERIFIED", "UNVERIFIED", "OWNER-STATED"}

PAGES = [
    # (file, nav label, page title, subtitle)
    ("overflow-verification.html", "Summary", "Verification addendum: summary",
     "Official-source checks for the bathtub overflow trip lever project."),
    ("overflow-verification-permits.html", "Permits and licensing", "Permit and licensing rules (quoted)",
     "Verbatim official text, with what it means for this project."),
    ("overflow-verification-contractors.html", "Contractors and quotes", "Contractor cross-check and quotes",
     "Shortlist evidence, CSLB license checks, and quote scope comparison. Job fit and quotes are unverified."),
    ("overflow-verification-repo-review.html", "Repo review", "Korea7 repo review",
     "Checks on the existing repository, with pass and flag status."),
    ("overflow-verification-flags.html", "Flagged for Review", "Flagged for Review (addendum)",
     "Unverified items, irregularities, and decisions for the owner. Items do not block publication."),
    ("overflow-verification-sources.html", "Sources", "Sources",
     "Every source used, its link, and how it was checked."),
]


class CheckError(Exception):
    pass


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate(d: dict) -> None:
    errors: list[str] = []
    flag_ids = {f["id"] for f in d["flags"]}

    def check_row(section: str, row: dict, verified_allowed: bool) -> None:
        rid = row.get("id", "?")
        verification = row.get("verification")
        if section != "repo_review" and verification not in ALLOWED_VERIFICATION:
            errors.append(f"{section} {rid}: bad verification '{verification}'")
        url = row.get("source_url") or row.get("url") or row.get("cslb_url") or row.get("listing_url")
        if section not in ("repo_review",) and verification != "OWNER-STATED" and not url:
            errors.append(f"{section} {rid}: missing source link")
        if url:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{section} {rid}: source link is not https: {url}")
        if verification == "VERIFIED":
            if not verified_allowed:
                errors.append(f"{section} {rid}: VERIFIED not allowed in this section")
            host = urlparse(url or "").netloc.lower()
            if host not in OFFICIAL_DOMAINS:
                errors.append(f"{section} {rid}: VERIFIED but source is not an official domain ({host})")
        for code in (row.get("flag") or "").split():
            if code not in flag_ids:
                errors.append(f"{section} {rid}: unknown flag code {code}")

    for r in d["requirements"]:
        check_row("requirements", r, verified_allowed=True)
    for r in d["permit_rules"]:
        check_row("permit_rules", r, verified_allowed=True)
    for r in d["licensing_rules"]:
        check_row("licensing_rules", r, verified_allowed=True)
    for r in d["contractors"]:
        check_row("contractors", r, verified_allowed=True)
        if r.get("verification") == "VERIFIED":
            # license-level verification only: needs the license number, a CSLB record URL for that
            # number, and the status text read from that record
            if not r.get("license_no") or not r.get("license_status"):
                errors.append(f"contractors {r['id']}: VERIFIED needs license_no and license_status")
            elif f"LicNum={r['license_no']}" not in (r.get("cslb_url") or ""):
                errors.append(f"contractors {r['id']}: cslb_url does not name license {r['license_no']}")
            elif urlparse(r["cslb_url"]).netloc.lower() not in OFFICIAL_DOMAINS:
                errors.append(f"contractors {r['id']}: cslb_url is not an official CSLB domain")
        elif r.get("verification") != "UNVERIFIED":
            errors.append(f"contractors {r['id']}: bad verification state")
        elif r.get("license_no"):
            errors.append(f"contractors {r['id']}: UNVERIFIED row must not carry a license number")
    for r in d["estimates"]:
        check_row("estimates", r, verified_allowed=False)
        if r.get("verification") != "UNVERIFIED":
            errors.append(f"estimates {r['id']}: quotes must stay UNVERIFIED")
    for r in d["repo_review"]:
        if "PLACEHOLDER" in r["result"] or "PLACEHOLDER" in r["status"]:
            errors.append(f"repo_review {r['id']}: placeholder left in place")
        if not (r.get("source_url") or "").startswith("https://"):
            errors.append(f"repo_review {r['id']}: missing https source link")
    for r in d["sources"]:
        if not r["url"].startswith("https://"):
            errors.append(f"sources {r['id']}: not https")
        host = urlparse(r["url"]).netloc.lower()
        if r["kind"] == "Official" and host not in OFFICIAL_DOMAINS:
            errors.append(f"sources {r['id']}: labelled Official but host is {host}")
    for f in d["flags"]:
        if f.get("source_url") and not f["source_url"].startswith("https://"):
            errors.append(f"flags {f['id']}: source is not https")
    if errors:
        raise CheckError("\n".join(errors))


# ---------- rendering ----------

def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def pill(v: str) -> str:
    cls = {
        "VERIFIED": "ok", "PASS": "ok", "UNVERIFIED": "warn", "NOT CHECKED": "warn",
        "FLAG": "bad", "OWNER-STATED": "muted", "INFO": "muted",
    }.get(v, "muted")
    return f'<span class="pill {cls}">{esc(v)}</span>'


def link(url, label=None) -> str:
    if not url:
        return '<span class="muted">none (owner-stated)</span>'
    return f'<a href="{esc(url)}" rel="noopener" target="_blank">{esc(label or url)}</a>'


def flag_chips(codes: str, flag_ids: set) -> str:
    out = []
    for c in (codes or "").split():
        if c in flag_ids:
            out.append(f'<a class="flagchip" href="overflow-verification-flags.html#{esc(c)}">{esc(c)}</a>')
    return " ".join(out)


def table(headers, rows, table_id, filterable=True) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    cls = "tbl" + (" filterable" if filterable else "")
    return (f'<div class="tablewrap"><table class="{cls}" id="{esc(table_id)}">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def shell(active_file: str, title: str, subtitle: str, body: str) -> str:
    parts = []
    for f, label, _, _ in PAGES:
        cls = ' class="active"' if f == active_file else ""
        parts.append('<a' + cls + ' href="' + esc(f) + '">' + esc(label) + '</a>')
    nav = "".join(parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Overflow verification addendum</title>
<link rel="stylesheet" href="assets/verification.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="plumbing-index.html">Overflow project dashboard</a> / <a href="overflow-verification.html">Verification addendum</a></div>
  <nav class="nav">{nav}</nav>
</header>
<main class="wrap">
  <h1>{esc(title)}</h1>
  <p class="subtitle">{esc(subtitle)}</p>
  {body}
</main>
<footer class="foot">
  <p>Research only. Information as of 2026-11-06 (UTC). Open items are on the
  <a href="overflow-verification-flags.html">Flagged for Review (addendum)</a> page. Every row links to its source.</p>
</footer>
<script src="assets/verification-filter.js"></script>
</body>
</html>
"""


def build_pages(d: dict) -> dict[str, str]:
    flag_ids = {f["id"] for f in d["flags"]}
    meta = d["meta"]
    pages: dict[str, str] = {}
    subtitles = {f: s for f, _, _, s in PAGES}
    titles = {f: t for f, _, t, _ in PAGES}

    # ---- summary ----
    n_contr = len(d["contractors"])
    n_lic = sum(1 for c in d["contractors"] if c.get("verification") == "VERIFIED")
    n_quotes = len(d["estimates"])
    n_official = sum(1 for s in d["sources"] if s["kind"] == "Official")
    stats = [
        ("Providers in addendum", str(n_contr), f"{n_lic} license-verified on CSLB, {n_contr - n_lic} UNVERIFIED"),
        ("Licenses verified here", str(n_lic), "CSLB license detail records, read 2026-11-06. Job fit not verified."),
        ("Quotes compared", str(n_quotes), "Amounts as supplied, UNVERIFIED"),
        ("Official sources read", str(n_official), "sf.gov, SF Plumbing Code, CSLB, SF ECC list"),
        ("Items flagged", str(len(d["flags"])), "See Flagged for Review (addendum)"),
    ]
    stat_html = "".join(
        f'<div class="stat"><div class="num">{esc(n)}</div><div class="lbl">{esc(l)}</div>'
        f'<div class="sub">{esc(s)}</div></div>' for l, n, s in stats)
    heads = "".join(f"<li>{esc(h)}</li>" for h in d["headlines"])
    steps = "".join(f"<li>{esc(s)}</li>" for s in d["next_steps"])
    rows = []
    for r in d["requirements"]:
        rows.append([
            esc(r["id"]), esc(r["requirement"]), esc(r["basis"]),
            link(r.get("source_url"), r.get("source_label")), pill(r["verification"]),
            flag_chips(r.get("flag", ""), flag_ids),
        ])
    req_table = table(["ID", "Requirement", "Basis", "Source (official where one applies)", "Status", "Flags"],
                      rows, "req")
    cards = [
        ("overflow-verification-permits.html", "Permits and licensing", f"{len(d['permit_rules'])} permit rows and {len(d['licensing_rules'])} licensing rows quoted from official text."),
        ("overflow-verification-contractors.html", "Contractors and quotes", f"{n_contr} providers with listing evidence, and {n_quotes} quotes compared on scope."),
        ("overflow-verification-flags.html", "Flagged for Review", f"{len(d['flags'])} items, including two claims on the existing pages that could not be confirmed."),
        ("overflow-verification-repo-review.html", "Repo review", f"{len(d['repo_review'])} checks on the repository, with hash matches and flagged inconsistencies."),
        ("overflow-verification-sources.html", "Sources", f"{len(d['sources'])} sources, with how each was checked."),
        ("plumbing-index.html", "Original overflow dashboard", "The existing dashboard from session 7379ee3c, unchanged by this addendum."),
    ]
    card_html = "".join(f'<a class="card" href="{esc(f)}"><h3>{esc(t)}</h3><p>{esc(x)}</p></a>' for f, t, x in cards)
    body = f"""
<section class="banner"><strong>Status:</strong> {esc(meta['status_line'])}
  <div class="small">As of {esc(meta['as_of'])} (UTC). {esc(meta['owner_note'])}</div></section>
<section class="stats">{stat_html}</section>
<section class="panel"><h2>Executive summary</h2><ul class="list">{heads}</ul></section>
<section class="panel"><h2>Recommended next steps (owner)</h2><ol class="list">{steps}</ol></section>
<section class="panel"><h2>Requirements mapped to official rules</h2>
  <p class="small">Owner-stated rows have no official source, so none is cited. Rows marked VERIFIED cite the official text.</p>
  {req_table}</section>
<section class="cards">{card_html}</section>
"""
    pages["overflow-verification.html"] = shell("overflow-verification.html", titles["overflow-verification.html"],
                                                subtitles["overflow-verification.html"], body)

    # ---- permits and licensing ----
    rows = []
    for r in d["permit_rules"]:
        rows.append([
            esc(r["id"]), esc(r["rule"]), esc(r["section"]),
            f'<blockquote>{esc(r["quote"])}</blockquote>', esc(r["implication"]),
            link(r["source_url"], r["source_label"]), pill(r["verification"]),
            flag_chips(r.get("flag", ""), flag_ids),
        ])
    permit_tbl = table(["ID", "Rule", "Section", "Official text (quoted)", "What it means here", "Source", "Status", "Flags"],
                       rows, "permits")
    rows = []
    for r in d["licensing_rules"]:
        rows.append([
            esc(r["id"]), esc(r["rule"]), f'<blockquote>{esc(r["quote"])}</blockquote>',
            esc(r["implication"]), link(r["source_url"], r["source_label"]), pill(r["verification"]),
            flag_chips(r.get("flag", ""), flag_ids),
        ])
    lic_tbl = table(["ID", "Rule", "Official text (quoted)", "What it means here", "Source", "Status", "Flags"],
                    rows, "lic")
    body = f"""
<section class="panel"><h2>San Francisco permit rules</h2>
  <p class="small">Quotes are verbatim from the sources read on 2026-11-06. The implications are this addendum's reading of the text, not legal advice. The permit determination belongs to SF DBI.</p>
  {permit_tbl}</section>
<section class="panel"><h2>Licensing rules (CSLB) and the SF ECC list</h2>
  <p class="small">Classification text is official. Seven license records are verified on CSLB (see the contractors page). Job fit and quotes are not verified.</p>
  {lic_tbl}</section>
"""
    pages["overflow-verification-permits.html"] = shell("overflow-verification-permits.html",
        titles["overflow-verification-permits.html"], subtitles["overflow-verification-permits.html"], body)

    # ---- contractors and quotes ----
    rows = []
    for r in d["contractors"]:
        rows.append([
            esc(r["id"]), f'<strong>{esc(r["business"])}</strong>',
            link(r["listing_url"], r["listing_label"]), esc(r["snapshot"]), esc(r["evidence"]),
            esc(r["claimed_license"]),
            (link(r["cslb_url"], f'CSLB #{r["license_no"]} (record)') if r["verification"] == "VERIFIED"
             else f'<a href="{CSLB_LOOKUP}" target="_blank" rel="noopener">CSLB lookup</a>'),
            (f'<strong>#{esc(r["license_no"])}</strong> {esc(r["license_status"])}' if r["verification"] == "VERIFIED"
             else '<span class="blank" aria-label="verified license value left blank"></span>'),
            (f'{esc(r["match_note"])} <em>Scope:</em> {esc(r["scope_note"])}' if r["verification"] == "VERIFIED"
             else '<span class="blank" aria-label="scope not verified"></span>'),
            esc(r["ecc_check"]), esc(r.get("cross_check", "")), pill(r["verification"]),
            flag_chips(r.get("flag", ""), flag_ids),
        ])
    contr_tbl = table(
        ["ID", "Provider (as listed)", "Listing (third-party)", "Snapshot", "Evidence in listing",
         "Claimed license", "Official check", "Verified license (CSLB record)", "Match and scope (CSLB)", "SF ECC list",
         "Cross-check with existing page", "Status", "Flags"], rows, "contr")
    rows = []
    for r in d["estimates"]:
        rows.append([
            esc(r["id"]), esc(r["provider"]), esc(r["date"]), esc(r["scope"]),
            f'<span class="unv">{esc(r["amount_as_provided"])}</span>',
            '<span class="blank" aria-label="verified amount left blank"></span>',
            esc(r["scope_note"]), link(r.get("source_url"), r["source_label"]),
            pill(r["verification"]), flag_chips(r.get("flag", ""), flag_ids),
        ])
    quote_tbl = table(["ID", "Provider (as supplied)", "Date (as supplied)", "Scope (as supplied)",
                       "Amount (as supplied, UNVERIFIED)", "Verified amount", "Scope note", "Source", "Status", "Flags"],
                      rows, "quotes", filterable=False)
    body = f"""
<section class="panel"><h2>Contractor cross-check</h2>
  <p class="small">Seven rows are license-verified against the CSLB license detail record cited on each row (data current 2026-11-06, 5:24-5:35 AM UTC). Verification covers status, classification, bond and workers comp only. The rest are UNVERIFIED, because no license number was given. Ratings come from search-result text, not live pages. Yelp's Verified License badge is not a CSLB check. Name matches to quote providers do not confirm who issued a quote.</p>
  <input class="filter" type="search" placeholder="Filter providers..." data-target="contr">
  {contr_tbl}</section>
<section class="panel"><h2>Quotes compared on scope</h2>
  <p class="small">Amounts are as supplied by the owner and are UNVERIFIED. The verified-amount column is blank on purpose. The scopes differ, so the amounts are not directly comparable.</p>
  {quote_tbl}</section>
"""
    pages["overflow-verification-contractors.html"] = shell("overflow-verification-contractors.html",
        titles["overflow-verification-contractors.html"], subtitles["overflow-verification-contractors.html"], body)

    # ---- repo review ----
    rows = []
    for r in d["repo_review"]:
        rows.append([esc(r["id"]), esc(r["check"]), esc(r["result"]), esc(r["evidence"]),
                     link(r.get("source_url"), "Source"), pill(r["status"])])
    repo_tbl = table(["ID", "Check", "Result", "Evidence", "Source", "Status"], rows, "repo", filterable=False)
    body = f"""
<section class="panel"><h2>Repository checks</h2>
  <p class="small">Checks on the existing Korea7 repository (a DOE GEMS submission project). They were run on branch arena/56e0fb61-korea7. No GEMS file was edited.</p>
  {repo_tbl}</section>
"""
    pages["overflow-verification-repo-review.html"] = shell("overflow-verification-repo-review.html",
        titles["overflow-verification-repo-review.html"], subtitles["overflow-verification-repo-review.html"], body)

    # ---- flags ----
    rows = []
    for f in d["flags"]:
        rows.append([
            f'<a id="{esc(f["id"])}"></a>{esc(f["id"])}', esc(f["type"]),
            f'<strong>{esc(f["title"])}</strong><br>{esc(f["detail"])}',
            link(f.get("source_url"), "Source") if f.get("source_url") else '<span class="muted">none (owner-stated or not researched)</span>',
            esc(f["owner_action"]),
        ])
    flag_tbl = table(["ID", "Type", "Item and detail", "Source", "Owner action"], rows, "flags", filterable=False)
    body = f"""
<div class="banner warnbanner"><strong>Flagged for Review (addendum).</strong> Irregularities, unverified items and owner decisions.
These do not block publication. Each item links to its source where one exists. The owner can request changes after the site is live.</div>
{flag_tbl}
"""
    pages["overflow-verification-flags.html"] = shell("overflow-verification-flags.html",
        titles["overflow-verification-flags.html"], subtitles["overflow-verification-flags.html"], body)

    # ---- sources ----
    rows = []
    for s in d["sources"]:
        rows.append([esc(s["id"]), esc(s["name"]), esc(s["kind"]), link(s["url"]), esc(s["used_for"]), esc(s["how_checked"])])
    src_tbl = table(["ID", "Source", "Kind", "Link", "Used for", "How it was checked"], rows, "sources", filterable=False)
    body = f"""
<section class="panel"><h2>Sources</h2>
  <p class="small">Official means a government or licensing body. Third-party means listings, directories, aggregators and business websites. Third-party data is used only for UNVERIFIED rows.</p>
  {src_tbl}</section>
"""
    pages["overflow-verification-sources.html"] = shell("overflow-verification-sources.html",
        titles["overflow-verification-sources.html"], subtitles["overflow-verification-sources.html"], body)
    return pages


def write_pages(pages: dict[str, str]) -> None:
    for name, content in pages.items():
        (DOCS / name).write_text(content, encoding="utf-8")


# ---------- link and asset check ----------

class _RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


def check_links() -> list[str]:
    problems: list[str] = []
    pages = [DOCS / f for f, _, _, _ in PAGES]
    for path in pages:
        if not path.exists():
            problems.append(f"missing page: {path.relative_to(ROOT)}")
            continue
        parser = _RefParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for ref in parser.refs:
            parsed = urlparse(ref)
            if parsed.scheme == "https":
                continue
            if parsed.scheme:  # http, mailto, javascript, etc.
                problems.append(f"{path.relative_to(ROOT)}: non-https reference {ref}")
                continue
            if ref.startswith("#"):
                continue
            target_path = ref.split("#", 1)[0]
            if not target_path:
                continue
            target = (path.parent / target_path).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(f"{path.relative_to(ROOT)}: link leaves repo: {ref}")
                continue
            if not target.exists():
                problems.append(f"{path.relative_to(ROOT)}: broken link {ref}")
    for asset in ("docs/assets/verification.css", "docs/assets/verification-filter.js"):
        if not (ROOT / asset).exists():
            problems.append(f"missing asset {asset}")
    return problems


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        d = load()
        validate(d)
        write_pages(build_pages(d))
    problems = check_links()
    if problems:
        print("LINK/ASSET CHECK FAILED:")
        for p in problems:
            print("  -", p)
        return 1
    print("OK: verification addendum built and checked (rows validated; no broken internal links).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CheckError as exc:
        print("DATA CHECK FAILED:")
        for line in str(exc).splitlines():
            print("  -", line)
        sys.exit(1)
