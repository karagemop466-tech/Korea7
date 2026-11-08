"""Canonical, source-first content for the overflow repair dashboard.

Run scripts/build_dashboard.py to render HTML and the JSON snapshot. Official
license facts, business self-descriptions and owner statements are deliberately
separate. A source link is not proof of an unrelated claim. No provider acceptance,
exact-job competence, availability or combined price is inferred.
"""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = json.loads((ROOT / "data/canonical/source_evidence.json").read_text())
CHECKED = "2026-11-08"
META = {
    "updated": CHECKED, "session": "arena/3a4a1788-korea7",
    "title": "Bathtub overflow trip lever — repair decision dashboard",
    "pages_url": "https://karagemop466-tech.github.io/Korea7/",
    "repo_url": "https://github.com/karagemop466-tech/Korea7",
}

def esc(value):
    return html.escape(str(value), quote=True)

def pill(text, tone="info"):
    return '<span class="pill %s">%s</span>' % (tone, esc(text))

UNVERIFIED = pill("UNVERIFIED", "warn")
BLANK = '<span class="blank" aria-label="blank — unverified"></span>'
UNKNOWN = BLANK + " " + UNVERIFIED

def source(sid, label, url, tier, supports, note="", status="verified"):
    return {"label": label, "publisher": tier, "url": url, "tier": tier,
            "status": status, "checked": CHECKED, "supports": supports, "note": note}

SOURCES = {}
def add(sid, label, url, tier, supports, note="", status="verified"):
    SOURCES[sid] = source(sid, label, url, tier, supports, note, status)

def slink(sid, label=None):
    s = SOURCES[sid]
    attrs = ' target="_blank" rel="noopener noreferrer"' if s["url"].startswith("http") else ""
    return '<a href="%s"%s>%s</a>' % (esc(s["url"]), attrs, esc(label or s["label"]))

def source_links(ids):
    labels = {"official":"official", "company":"business", "manufacturer":"manufacturer",
              "platform":"blocked platform", "owner":"owner statement", "project":"project record"}
    return " · ".join(slink(sid, sid + " · " + labels[SOURCES[sid]["tier"]]) for sid in ids)

add("S01", "SF DBI — plumbing and mechanical permits", "https://www.sf.gov/apply-plumbing-and-mechanical-permit", "official", "Pipe replacement guidance, license scope and inspection before covering permitted work")
add("S02", "SF DBI — work that does not need a permit", "https://www.sf.gov/information--check-if-your-construction-project-needs-permit", "official", "Minor interior wallboard repairs, with a fire-protection exception")
add("S04", "CSLB — Check a License", "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx", "official", "Official license lookup and its limitations")
add("S05", "CSLB — C-36 plumbing classification", "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C36", "official", "Plumbing classification includes fluid-waste disposal and maintenance/replacement")
add("S12", "CSLB — Handyman Heroes complaint disclosure", "https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394", "official", "Citation 2 2020 001045, dated 2020-07-12, disclosure-only status")
add("S13", "California BPC §7048", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7048", "official", "Current small-project licensing exemption and restrictions; effective 2026-01-01")
add("S14", "Oatey — Dearborn trip-lever bath waste", "https://www.oatey.com/products/P_041193058379/dearborn-plastic-tubular-triplever-bath-waste", "manufacturer", "A9226/P9226 product identities; not established as the installed model")
for lic in EVIDENCE["licenses"]:
    add(lic["source"], "CSLB #%s — %s" % (lic["number"], lic["name"]),
        "https://www2.cslb.ca.gov/onlineservices/checklicenseII/LicenseDetail.aspx?LicNum=" + lic["number"],
        "official", "Name, phone, address, classifications, status, expiry, bond and workers' compensation",
        "Direct read; record stamp %s. A disclosed-link absence is not a claim of no complaints." % lic["stamp"])
add("S38", "Expert Plumbing Solutions — business website", "https://www.eplumbingsolutions.com/", "company", "Business phone, SF service area and plumbing services", "Self-description; not exact-job evidence")
add("S39", "Bay Area Plumbing — business website", "https://www.bayareaplumbingsf.com/", "company", "Business phone, SF service area and plumbing/remodeling services", "Self-description; ceiling scope not established")
add("S40", "Fast Response — business website", "https://www.fastresponseplumbingsf.com/", "company", "Business phone, SF houses/apartments/HOAs and plumbing services", "Self-description; review aggregates are not independently verified")
add("S41", "General SF — business website", "https://generalsf.com/", "company", "Business phone, Bay Area service and license identity", "Self-description; license facts checked separately at CSLB")
add("S42", "Handyman Heroes — business website", "https://www.handymanhero.es/", "company", "Plumbing/construction services and C-10 advertising claim", "C-10 claim differs from the reviewed CSLB record; see U08")
add("S43", "Ace Plumbing & Rooter — business website", "https://www.aceplumbingandrooter.com/", "company", "Business phone, SF service, HOA/property-manager services and license identity", "No drywall commitment established on reviewed pages")
add("S44", "Owner-provided project brief", "brief.html", "owner", "Problem description and three quoted scopes/amounts", "Primary transcription only; not independent or official verification")
add("S45", "Shared coordination and delivery record", META["repo_url"] + "/blob/main/COORDINATION.md", "official", "Repository claims, handoffs, tests and deployment records", "Official repository record; not a contractor source")
add("S46", "GitHub Pages landing page", META["pages_url"], "project", "Published site location", "Live deployment is checked after merge, not inferred from this link")
add("S47", "Repository README", META["repo_url"] + "/blob/main/README.md", "official", "Repository documentation and legacy-project scope")
for sid, label, url in [
    ("S48", "Legacy GEMS site", "docs/index.html"),
    ("S49", "Earlier bathtub-overflow pages", "bathtub-overflow/executive-summary.html"),
    ("S50", "Earlier docs/bath dashboard", "docs/bath/index.html"),
    ("S51", "Earlier docs overflow dashboard", "docs/plumbing-index.html"),
    ("S55", "Canonical source ledger", "sources.html"),
    ("S58", "Historical ranked shortlist", "shortlist.html"),
    ("S59", "Earlier verification log", "verification-log.html"),
    ("S60", "Parallel SF overflow audit", "sf-overflow-audit/index.html"),
    ("S63", "Archived overflow verification", "docs/overflow-verification.html"),
]:
    add(sid, label, url, "project", label + "; retained for manual review", "Historical content is not the canonical factual record")
add("S52", "Older open pull request #32", META["repo_url"] + "/pull/32", "official", "Parallel-session delivery irregularity", "Not merged or closed by this session")
add("S61", "Fast Response — repair and replacement", "https://www.fastresponseplumbingsf.com/plumbing-repair-replacement", "company", "Bathtubs (waste & overflow), coordination with a general contractor, business phone and mailing address", "Company self-description; not proof of exact stuck-mechanism experience")
add("S62", "California BPC §7059", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=7059.&lawCode=BPC", "official", "Incidental and supplemental work by specialty contractors", "Applicability to this ceiling repair is not established")
add("S64", "CSLB — B general building classification", "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=B", "official", "BPC 7057 trade conditions and appropriately licensed subcontractors")
add("S66", "General SF — building services", "https://generalsf.com/building", "company", "Sheetrock/tape and texture, finish plumbing and painting advertised", "Not a combined quote or confirmed ceiling scope")
add("S67", "General SF — plumbing services", "https://generalsf.com/plumbing", "company", "Tub/shower and shower-valve replacement advertised", "Exact trip-lever extraction experience not established")
add("S68", "CSLB — C-9 drywall classification", "https://www2.cslb.ca.gov/About_Us/Library/Licensing_Classifications/Licensing_Classifications_Detail.aspx?Class=C-9", "official", "Wallboard installation, taping and texturing scope")
add("S71", "Handyman Heroes — sheetrock and wall repairs", "https://www.handymanhero.es/handyman-services/sheetrock-and-wall-repairs/", "company", "Drywall replacement, patching, texture matching, optional painting and cleanup", "Ceiling scope and price require a proposal")
add("S72", "Handyman Heroes — San Francisco services", "https://www.handymanhero.es/city/san-francisco-ca/", "company", "SF plumbing for homes/condos/apartments and drywall patching", "Company statement; exact occupied-unit references unverified")
add("S73", "Rapid Flow — business website", "https://www.rapidflowbayarea.com/", "company", "SF address, license identity and 844-BAY-FLOW contact", "Vanity phone differs from CSLB phone; see U25")
add("S74", "Rapid Flow — services", "https://www.rapidflowbayarea.com/services", "company", "Tub installation, drywall repair/installation and subcontractor coordination in SF", "Self-description; not job acceptance")
add("S75", "Genteel Plumbers — business website", "https://www.genteelplumbers.com/", "company", "SF service, phone, published dispatch fee and Financial District exclusion", "Dispatch fee is not a repair quote; phone differs from CSLB")
add("S76", "Manny's Plumbing & Rooters — business website", "https://www.mannysplumbingandremodeling.com/", "company", "License identity, SF/San Mateo counties, tub installation and remodeling", "No drywall inclusion established")
add("S77", "Watco — trip-lever installation instructions", "https://www.watcomfg.com/watco/Instructions/500-501-600TL_Instructions_Bath_Waste_Sheet.pdf", "manufacturer", "Overflow plate/drop-cylinder adjustment and assembly examples", "Not instructions to force this unidentified assembly")
add("S78", "Watco — 501/502 trip-lever parts specification", "https://www.watcomfg.com/Spec_Sheets/tubular_brass/Watco_Trip_Lever_501-502-551-552_Series_Bath_Waste_Sheet.pdf", "manufacturer", "Linkage, drop cylinder, overflow elbow and retainer plate examples", "Installed model/parts unknown")
add("S79", "Oatey — bath waste and overflow FAQ", "https://www.oatey.com/products/bath-waste-overflow/bath-waste-overflow", "manufacturer", "Trip-lever mechanism, replacement draining test and framing caution", "Product-specific guidance; not a diagnosis")
add("S80", "GitHub Docs — custom Pages workflows", "https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages", "official", "Build/artifact/deploy workflow and required permissions")
for sid, url, label in [
    ("S29", "https://www.yelp.com/search?find_desc=Drywall+Installation+%26+Repair&find_loc=San+Francisco%2C+CA", "Yelp — SF drywall search"),
    ("S32", "https://www.yelp.com/biz/expert-plumbing-solutions-san-francisco", "Yelp — Expert Plumbing Solutions"),
    ("S33", "https://www.yelp.com/biz/bay-area-plumbing-san-francisco", "Yelp — Bay Area Plumbing"),
    ("S34", "https://www.yelp.com/biz/fast-response-plumbing-and-rooter-san-francisco-3", "Yelp — Fast Response"),
    ("S35", "https://www.yelp.com/biz/general-sf-san-francisco-2", "Yelp — General SF"),
    ("S36", "https://www.yelp.com/biz/handyman-heroes-san-francisco-5", "Yelp — Handyman Heroes"),
    ("S81", "https://www.yelp.com/biz/ace-plumbing-and-rooter-san-francisco", "Yelp — Ace Plumbing"),
    ("S82", "https://www.yelp.com/biz/genteel-plumbers-san-francisco-7", "Yelp — Genteel Plumbers"),
    ("S83", "https://www.yelp.com/biz/mannys-plumbing-and-rooter-daly-city", "Yelp — Manny's Plumbing"),
    ("S84", "https://www.yelp.com/search?find_desc=Rapid+Flow+Plumbing&find_loc=San+Francisco%2C+CA", "Yelp — Rapid Flow search"),
]:
    add(sid, label, url, "platform", "Discovery link only; current review values not verified", "Direct fetch returned HTTP 403 on 2026-11-08; ratings/counts left blank", "blocked-403")
add("S85", "Direct-source evidence register", "data/canonical/source_evidence.json", "project", "Source-specific excerpts, record stamps and limitations")
add("S86", "Repository audit report", "data/canonical/repo_audit.json", "project", "Inventory, syntax, hash, link and test checks")
add("S87", "Repository line inventory", "data/canonical/repo_line_inventory.json", "project", "Per-file line counts and SHA-256 inventory")
add("S88", "CSLB — hiring guidance", "https://www2.cslb.ca.gov/Consumers/Hire_A_Contractor/", "official", "License, contractor selection, permit and contract guidance")

NAV = [
    {"group": "Overview", "links": [("index.html", "Dashboard"), ("summary.html", "Executive summary"), ("requirements.html", "Requirements")]},
    {"group": "Decision", "links": [("contractors.html", "Contractor ranking"), ("estimates.html", "Estimates & costs"), ("findings.html", "Access & hiring plan")]},
    {"group": "Reference", "links": [("technical.html", "Technical context"), ("permits.html", "Official rules"), ("brief.html", "Owner brief"), ("sources.html", "Source ledger")]},
    {"group": "Audit", "links": [("verification.html", "Verification"), ("repo-review.html", "Repo review"), ("flagged.html", "Flagged for review")]},
]

# Structured candidate records. Null means no verified value, never a negative finding.
CANDIDATES = [
    {"key":"general", "rank":1, "name":"General SF", "lic":"959843", "sid":"S09", "site":"S41", "yelp":"S35", "extra":["S66","S67"], "drywall":"Advertises sheetrock/tape and texture", "fit":"Strongest documented combined-service match: SF plumbing plus sheetrock/tape/texture on its own service pages; B + C-36 on CSLB.", "risk":"Workers' compensation exemption: confirm who attends and their coverage. Exact extraction and ceiling scope unconfirmed.", "quote":None},
    {"key":"heroes", "rank":2, "name":"Handyman Heroes", "lic":"1003394", "sid":"S10", "site":"S42", "yelp":"S36", "extra":["S71","S72","S12"], "drywall":"Advertises replacement, patching, texture and optional paint", "fit":"Documented SF plumbing and drywall restoration, B + C-36, and a workers' compensation policy on CSLB.", "risk":"Official citation disclosure requires review; website C-10 claim is not on the reviewed license. Priming/painting is optional, not automatically included.", "quote":None},
    {"key":"rapid", "rank":3, "name":"Rapid Flow Plumbing & Rooter", "lic":"1115649", "sid":"S56", "site":"S73", "yelp":"S84", "extra":["S74"], "drywall":"Advertises drywall and subcontractor coordination", "fit":"Documented SF tub plumbing, drywall and project coordination; B + C-36 on CSLB.", "risk":"Workers' compensation exemption and different website/CSLB phone numbers. No verified exact-job reference or combined price.", "quote":None},
    {"key":"ace", "rank":4, "name":"Ace Plumbing & Rooter", "lic":"829071", "sid":"S11", "site":"S43", "yelp":"S81", "extra":[], "drywall":None, "fit":"SF plumbing, B + C-36, workers' compensation policy and documented HOA/property-manager service.", "risk":"Drywall service is not established on the reviewed pages. Ask for the responsible drywall trade and one coordinated proposal.", "quote":None},
    {"key":"genteel", "rank":5, "name":"Genteel Plumbers", "lic":"1025814", "sid":"S65", "site":"S75", "yelp":"S82", "extra":[], "drywall":None, "fit":"SF plumbing, B + C-36 and a workers' compensation policy on CSLB.", "risk":"Drywall not established; website excludes Financial District service and differs from CSLB phone. Published dispatch fee is not a repair quote.", "quote":None},
    {"key":"manny", "rank":6, "name":"Manny's Plumbing & Rooters", "lic":"841229", "sid":"S57", "site":"S76", "yelp":"S83", "extra":[], "drywall":None, "fit":"B + C-36; business advertises tub installation/remodeling and surrounding areas of San Francisco County.", "risk":"Daly City mailing address, workers' compensation exemption and no documented drywall inclusion. Confirm the exact SF address is served.", "quote":None},
    {"key":"expert", "rank":7, "name":"Expert Plumbing Solutions", "lic":"977638", "sid":"S06", "site":"S38", "yelp":"S32", "extra":[], "drywall":None, "fit":"Closest owner-reported plumbing scope: waste-and-overflow replacement; active C-36 and workers' compensation policy.", "risk":"No B or C-9 on this record and no verified drywall scope. Owner amount is not an all-in price; incidental-work rules do not prove coverage.", "quote":614},
    {"key":"bay", "rank":8, "name":"Bay Area Plumbing", "lic":"757796", "sid":"S07", "site":"S39", "yelp":"S33", "extra":[], "drywall":None, "fit":"Active SF C-36 plumber with an owner-reported lever/plug/spout quote.", "risk":"A tub spout diverter is not necessarily the overflow trip lever. Clarify the component and access plan; drywall and workers' compensation coverage unconfirmed.", "quote":550},
    {"key":"fast", "rank":9, "name":"Fast Response Plumbing & Rooter", "lic":"1024971", "sid":"S08", "site":"S40", "yelp":"S34", "extra":["S61"], "drywall":None, "fit":"Official business page explicitly lists bathtubs (waste & overflow), SF apartments/HOAs and working alongside a general contractor.", "risk":"Owner quote is for repair/adjustment, not verified concealed replacement. C-36 only on this record; address discrepancy and workers' compensation renewal require review.", "quote":135},
]
LICENSES = {x["number"]: x for x in EVIDENCE["licenses"]}

def license_link(number):
    return slink(LICENSES[number]["source"], "#" + number)

def candidate_name(c):
    return "<strong>%s</strong><br>%s · %s" % (esc(c["name"]), slink(c["site"], "Business site"), license_link(c["lic"]))

def table(title, columns, rows, caption):
    return {"title":title, "columns":columns + ["Source"], "rows":rows, "caption":caption}

def row(cells, src):
    return {"cells":cells, "src":src}

TABLES = {}
TABLES["problem"] = table("Project at a glance", ["Item", "Owner-reported detail", "Independent verification", "Status"], [
    row(["Problem", "Trip lever stuck in concealed bathtub waste/overflow plumbing", UNKNOWN, "Site conditions not inspected"], ["S44","S79"]),
    row(["Preferred access", "Remove from above if safe", UNKNOWN, "No safe extraction method confirmed"], ["S44","S77"]),
    row(["Reported attempts", "More than five licensed plumbers expressed concern about concealed-plumbing damage", UNKNOWN, "Identities, findings and licenses not supplied"], ["S44","S04"]),
    row(["Fallback access", "From below; storage space beneath may require a ceiling opening", UNKNOWN, "Opening size, framing and fire rating unknown"], ["S44","S79"]),
    row(["Service model", "One coordinated plumbing + drywall service", "Business services and license classes checked; acceptance is not", pill("Conditional shortlist", "warn")], ["S44","S66","S71","S74"]),
    row(["Occupancy", "Tenants occupy the affected unit", UNKNOWN, "Schedule, protection plan and references unconfirmed"], ["S44","S72"]),
    row(["Reference images", "No photographs attached to this session's brief", "No installed model or cause of seizure established", pill("Unverified site details", "warn")], ["S44","S78"]),
], "Owner statements are preserved as statements, not converted into verified facts. Official links provide technical/licensing context only.")

TABLES["estimates"] = table("Three owner-reported estimates — 2026-08-30", ["Business / official identity", "Scope transcribed from owner", "Verified amount", "Drywall inclusion", "Comparison"], [
    row([candidate_name(c), scope, UNKNOWN, UNKNOWN, note], [c["sid"],c["site"],"S44"])
    for c, scope, note in [
        (CANDIDATES[6], "Replacing waste and overflow; remove bathtub wastewater overflow trip lever", "Closest stated match to concealed waste-and-overflow work; not a verified extraction plan."),
        (CANDIDATES[7], "Replace lever for bathtub plug and spout with diverter; labor and materials", "Component mismatch possible: a spout diverter is not the same as a trip-lever stopper."),
        (CANDIDATES[8], "Repair or adjust bathtub wastewater plunger handle", "Adjustment attempt only as described; cannot be treated as full replacement pricing."),
    ]
], "Amounts are intentionally blank in the verified-value column. The original figures are retained only in the labeled owner transcription below and on Flagged for Review. Date is owner-provided. No official job quote was available.")
TABLES["brief_quotes"] = table("Owner transcription — NOT verified prices", ["Business", "Amount stated by owner", "Date stated by owner", "Record status"], [
    row([esc(c["name"]), "$%d" % c["quote"], "2026-08-30", pill("owner-provided — no official source exists", "warn")], ["S44",c["sid"]])
    for c in CANDIDATES if c["quote"] is not None
], "These are transcriptions, not confirmed values, current offers or comparable all-in bids. No total or savings calculation is presented.")
TABLES["costs"] = table("Published cost information and missing scope", ["Item", "Published value", "What it does not establish", "Status"], [
    row(["Genteel dispatch fee", "$149, applied to the cost of services (business website)", "Not a trip-lever repair quote; no ceiling or drywall price", pill("Business-published", "info")], ["S75","S65"]),
    row(["Combined plumbing + drywall quote", UNKNOWN, "No provider has supplied an accepted combined scope", UNVERIFIED], ["S44","S66","S71","S09","S10"]),
    row(["Diagnostic / above-access attempt fee", UNKNOWN, "No job-specific amount verified", UNVERIFIED], ["S44","S61","S08"]),
    row(["Ceiling opening, patch, texture, paint and protection", UNKNOWN, "No dimensions, finish level or job-specific price verified", UNVERIFIED], ["S44","S71","S10"]),
    row(["Permit / inspection fees, if applicable", "Depend on the scope of work (SF DBI)", "No applicability determination or project fee verified", pill("Official guidance", "info")], ["S01"]),
], "National publisher ranges from earlier pages are not used to price this San Francisco job. They remain in the labeled archives, not in the canonical decision data.")

TABLES["ranking"] = table("Conditional hiring order — best documented fit first", ["Rank", "Business / phone", "Drywall evidence", "Why this position", "Cost for this job", "Before hiring"], [
    row([str(c["rank"]), candidate_name(c) + "<br><strong>" + esc(LICENSES[c["lic"]]["phone"]) + "</strong>",
         esc(c["drywall"]) if c["drywall"] else UNKNOWN, esc(c["fit"]), UNKNOWN, esc(c["risk"])],
        [c["sid"],c["site"],"S44"] + c["extra"])
    for c in CANDIDATES
], "Desk-research ranking, not a hire commitment. Order favors documented combined services, then license/insurance evidence and disclosed risks. No reviews or exact-job competence were inferred. All-in costs remain blank; owner-only figures are on Estimates. Phone numbers are CSLB-listed; website differences are flagged.")
TABLES["contractors"] = table("Official license register — checked 2026-11-08", ["Business", "License", "Classes", "Status / expiry", "Workers' compensation", "Bond", "CSLB phone / address"], [
    row([esc(l["name"]), license_link(l["number"]), esc(" · ".join(l["classes"])),
         pill(l["status"], "warn" if l["number"] in {"1003394","1009195"} else "ok") + "<br>Expires " + l["expires"],
         esc(l["wc"]) + ("<br>Policy expires " + l["wc_expires"] if l["wc_expires"] else ""),
         "$%s" % format(l["bond"], ","), esc(l["phone"]) + "<br><small>" + esc(l["address"]) + "</small>"], [l["source"]])
    for l in EVIDENCE["licenses"]
], "Direct CSLB reads; exact record stamps are in the evidence register. License status is not a quality rating. Bond is not general-liability insurance. Workers' compensation exemption is not proof that an attending worker is covered. Recheck before signing.")
TABLES["support"] = table("Additional options and unverified lead", ["Business", "Role", "Verified identity / phone", "Limitation"], [
    row(["Bernal Hill Drywall", "Drywall coordination option — not all-in-one plumbing", license_link("995163") + "<br>(415) 533-8274", "C-9 + B, no C-36 on this record. Coordinate with the chosen plumber; acceptance and price unverified."], ["S69","S68"]),
    row(["Advanced Plumbing and Drain", "Not prioritized; official additional-status warning", license_link("1009195") + "<br>(415) 744-4944", "Currently active C-36, but CSLB displays a potential future-suspension liability warning. Review before considering."], ["S70"]),
    row(["Szeto Plumbing and Handyman", "Historical lead only", UNKNOWN, "No license number supplied or matching record independently verified in this session. No phone, price or capability filled in."], ["S04","S58","S45"]),
], "These entries preserve earlier research without presenting an unsupported lead as a licensed recommendation.")
TABLES["reviews"] = table("Review discovery — current values intentionally blank", ["Business", "Review link", "Current rating / count", "Exact concealed trip-lever review", "Use in ranking"], [
    row([esc(c["name"]), slink(c["yelp"], "Yelp listing/search") + " · " + license_link(c["lic"]), UNKNOWN, UNKNOWN, "Not used; direct review fetch blocked (403)"], [c["yelp"],c["sid"]])
    for c in CANDIDATES
], "Yelp was searched and direct listings attempted. Search snippets and old snapshots are not current verified review data. Business-site testimonials are self-published. No star rating, review count or 'verified license' badge substitutes for CSLB.")

REQ = [
 ("R01","Collect, organize and analyze the full requirements","Requirements register and traceable sources","S04"),
 ("R02","Create an executive summary","Summary with decision, costs and limitations","S45"),
 ("R03","Hard-to-access bathtub overflow; drywall may need opening","Owner statement; no site inspection","S79"),
 ("R04","Remove the wastewater overflow trip lever","Installed model and safe method unverified","S77"),
 ("R05","Expert Plumbing Solutions estimate dated 8/30/26","Owner transcription; verified amount blank","S06"),
 ("R06","Bay Area Plumbing estimate dated 8/30/26","Owner transcription; component scope needs clarification","S07"),
 ("R07","Fast Response estimate dated 8/30/26","Owner transcription; adjustment scope only","S08"),
 ("R08","Find a provider able to perform the needed work","Conditional candidates; no acceptance established","S04"),
 ("R09","Prefer removal from above","Manufacturer examples do not establish feasibility here","S77"),
 ("R10","More than five plumbers reportedly could not remove it safely from above","Owner statement; identities and reports not supplied","S04"),
 ("R11","Below access may require opening a storage-area ceiling","No dimensions, framing or fire-rating verification","S79"),
 ("R12","One coordinated drywall and plumbing service","Three business sites document both services; scope unconfirmed","S66"),
 ("R13","Search Yelp and other review services for this work in SF","Yelp attempted; current values blank when blocked","S04"),
 ("R14","Prefer a licensed plumber or contractor","Eleven official license records checked; one lead unverified","S04"),
 ("R15","Provider must service the San Francisco area","Business statements and CSLB addresses kept separate","S41"),
 ("R16","Delicate work in a sensitive tenant-occupied environment","Exact-job references and protection plan unverified","S72"),
 ("R17","Use pictures if supplied; otherwise use the description","No images attached; no model inferred","S78"),
 ("R18","Complete the work without requesting manual input","Desk research, build and publication executed autonomously","S45"),
 ("R19","Review the repository and flag irregularities with links","Repository audit and line inventory published","S47"),
 ("R20","Create a clean GitHub Pages dashboard with category pages","Static landing page and category navigation","S80"),
 ("R21","Every table row has an official-source link; unknown values blank and flagged","Source-role audit distinguishes context from proof","S04"),
 ("R22","Coordinate concurrent sessions through the shared board","Claims, handoffs and conflict resolutions recorded","S45"),
 ("R23","Publish a clearly labeled Flagged for Review page","Non-blocking flags with sources and review actions","S47"),
 ("R24","Create and merge a PR; confirm deployment and record results","Delivery record appended after live verification","S80"),
 ("R25","Rank contractors with reasons, costs, official links and phones","Conditional ranking; unknown costs blank","S04"),
 ("R26","Do not infer or hallucinate unavailable values","Blank cells, explicit provenance and source-specific limitations","S04"),
]
TABLES["requirements"] = table("Requirements traceability", ["ID", "Requirement / input", "Officially verified value", "Implementation / limitation", "Context source"], [
    row([rid, esc(req), UNKNOWN if rid not in {"R14","R21"} else ("See official license register" if rid=="R14" else "Structural check enforced; see Verification"), esc(note), slink(sid,"Official reference")], ["S44",sid,"S45"])
    for rid,req,note,sid in REQ
], "The brief is the source of requested work, not official confirmation of property facts. Context links do not prove owner statements. Delivery status is recorded in the repository.")

TABLES["technical"] = table("Technical context — not a diagnosis", ["Topic", "What the official source establishes", "Application to this project", "Status"], [
    row(["Trip-lever assembly", "Watco examples include a faceplate, linkage, drop cylinder, overflow elbow and retainer plate", "Identify the installed assembly before selecting parts or an extraction method", pill("Manufacturer example", "info")], ["S77","S78"]),
    row(["Above access", "Watco Step 7 describes removing the overflow plate/drop cylinder to readjust", "Does not establish that this seized assembly can be safely extracted from above", UNVERIFIED], ["S77","S44"]),
    row(["Stopper types", "Oatey distinguishes trip-lever linkage, Uni-Lift, Toe-Touch and cable-drive systems", "A tub spout/diverter quote may not address the same component", pill("Manufacturer distinction", "info")], ["S79","S44"]),
    row(["Replacement test", "Oatey describes filling until overflow flow begins, shutting off water and inspecting connections behind the tub", "Ask the contractor to specify the test and keep required access available until completed", pill("Manufacturer guidance", "info")], ["S79"]),
    row(["Framing", "Oatey warns against cutting framing without local building-official approval", "No opening size or structural alteration is recommended here", pill("Manufacturer caution", "warn")], ["S79"]),
    row(["Replacement compatibility", "Oatey publishes A9226/P9226 trip-lever kits", "No compatibility with the installed tub is established", UNVERIFIED], ["S14","S44"]),
    row(["Cause of seizure / hidden damage", UNKNOWN, "No photos, model, inspection report or disassembly evidence supplied", UNVERIFIED], ["S44","S78"]),
], "No forcing technique, chemical treatment, diagnosis or guaranteed access route is recommended. The contractor must assess the actual assembly.")
TABLES["plan"] = table("Recommended scope to request — not a provider promise", ["Stage", "Requested deliverable", "Decision gate", "Evidence / status"], [
    row(["1. Diagnose", "Identify the stopper mechanism and explain a conservative above-access attempt with a stop-work limit", "Do not authorize blind force or assume the linkage is free", "Manufacturer context; exact method " + UNVERIFIED], ["S44","S77","S78"]),
    row(["2. Contingent access", "Separate line items for below access, storage protection, ceiling opening and plumbing repair/replacement", "Agree location, size, responsible trades and any required inspections before cutting", "Site dimensions and requirements " + UNVERIFIED], ["S44","S01","S79"]),
    row(["3. Occupied-unit plan", "Scheduled tenant coordination, dust containment, floor/storage protection and cleanup", "Confirm who enters each unit and how belongings are protected", "Business statements are not job references; " + UNVERIFIED], ["S44","S71","S72"]),
    row(["4. Test", "Contractor-specified drain/overflow test and documented inspection of exposed joints", "Complete required testing/inspection before closure", pill("Official/manufacturer context", "info")], ["S01","S79"]),
    row(["5. Restore", "Patch, tape, texture and explicitly agreed primer/paint scope; debris removal", "Do not assume optional painting is included", "Business service description; price " + UNVERIFIED], ["S71","S66"]),
    row(["6. Close out", "One written scope, named responsible trades, insurance evidence, photos, test result and warranty", "Recheck license and coverage before signing", pill("Hiring control", "info")], ["S04","S88"]),
], "This is a procurement checklist based on the owner's requirements and cited guidance, not engineering advice or a confirmed contractor proposal.")
TABLES["permits"] = table("Neutral official rules — applicability is scope-specific", ["Topic", "Official text / rule", "Limit for this project"], [
    row(["Concealed pipe work", "SF DBI: permit required before cutting into or replacing pipes, particularly pipes covered by a wall; see §104.2 exemptions", "No exemption or permit determination is made here"], ["S01"]),
    row(["Wallboard repairs", "SF DBI lists minor interior plaster/wallboard repairs, unless required for fire protection", "Does not decide the plumbing scope or establish the ceiling rating"], ["S02"]),
    row(["Inspection", "SF DBI requires inspection before covering pipes after a permit is issued", "Conditional on the permitted scope"], ["S01"]),
    row(["Plumbing classification", "C-36 covers proper fluid-waste disposal and maintenance/replacement", "License class does not prove exact-job skill"], ["S05"]),
    row(["General building", "B classification is subject to BPC 7057 trade conditions and appropriate specialty licensing/subcontracts", "B + C-36 is a screening signal, not automatic acceptance or proof of drywall expertise"], ["S64","S62"]),
    row(["Incidental work", "BPC §7059 allows qualifying incidental and supplemental work by specialty contractors", "Whether this ceiling work qualifies is not established; no categorical second-trade requirement is asserted"], ["S62"]),
    row(["Small-project licensing exemption", "BPC §7048: aggregate labor/materials/all items under $1,000, casual/minor work, no building permit required; additional restrictions apply", "Not a permit exemption and not a reason to split a project; current text effective 2026-01-01"], ["S13"]),
], "Information only, not legal advice. Confirm the actual scope with the responsible licensed professional and SF DBI. No property-specific compliance status is published.")

FLAGS = [
 ("U01","Three owner-reported amounts lack official quotes","Verified amount cells are blank; original figures are labeled owner transcriptions","Obtain current written quotes for the same scope",["S44","S06","S07","S08"]),
 ("U02","Physical problem and prior plumber attempts are owner statements","No inspection, photos, plumber reports or installed model supplied","Have the chosen contractor document the actual condition",["S44","S78"]),
 ("U03","Yelp direct access blocked","Listings/search returned HTTP 403; current ratings/counts and exact-job reviews are blank","Open the linked listings manually; do not rely on old counts",["S29","S32","S35","S36","S81","S04"]),
 ("U04","Drywall inclusion was not stated in the three estimates","Inclusion cells are blank, not assumed excluded or included","Request explicit opening, patch, texture, paint and cleanup line items",["S44","S71"]),
 ("U05","Bay Area quote may describe a different component","Tub spout/diverter wording is not a verified trip-lever overflow scope","Clarify the exact part and access plan before comparing price",["S44","S79","S07"]),
 ("U06","Four exemptions: #757796, #959843, #1115649, #841229","Each certified no employees at the record check; this does not establish coverage for attending workers","Confirm attending workers and appropriate coverage before entry",["S07","S09","S56","S57"]),
 ("U07","Handyman Heroes has an official citation disclosure","Citation 2 2020 001045, 2020-07-12, disclosure-only status; underlying merits not inferred","Read the official disclosure before hiring",["S12","S10"]),
 ("U08","Handyman Heroes website advertises C-10","Reviewed CSLB #1003394 lists B and C-36, not C-10","Ask which entity/license covers any electrical work",["S42","S10"]),
 ("U09","Fast Response aggregates reviews on its own site","Combined Yelp/Google claim is not independently verified and is not used in ranking","Check each platform separately; leave current values blank here",["S40","S34"]),
 ("U10","Szeto lead has no verified matching license in this session","License, phone, price and capability remain blank","Do not hire from the historical lead without an official matching record",["S04","S58"]),
 ("U11","Earlier dead technical sources are not canonical evidence","Historical SFGate/InspectAndTest citations are superseded by live manufacturer sources","Use Watco/Oatey links in the canonical ledger",["S77","S79","S59"]),
 ("U12","Repository contains unrelated scientific work and multiple historical dashboards","Legacy files are preserved; root is the canonical repair dashboard","Review archives as historical, not current recommendations",["S47","S48","S49","S50","S51","S60"]),
 ("U13","Older conflicting PR #32 remains open","Not merged or closed by this session","Owner/session may reconcile or close it separately",["S52","S45"]),
 ("U14","No accepted combined plumbing/drywall proposal","No availability, acceptance, schedule or all-in price established","Use the staged scope checklist for comparable proposals",["S44","S66","S71","S74"]),
 ("U15","Exact delicate-repair and occupied-unit experience is unverified","License classes and general service statements do not establish this capability","Request relevant references and a conservative access plan",["S04","S72","S43"]),
 ("U16","Review-platform badges are not regulator verification","Only CSLB records are used for license status/classes","Recheck the official license before signing",["S04","S36"]),
 ("U17","Fast Response address differs across official sources","CSLB: 236 W POTRAL AVE #459; business mailing address: 236 W Portal Ave #259","Confirm the correct business/service address; do not silently normalize",["S08","S61"]),
 ("U18","Older $500 licensing references are superseded","Current BPC §7048 uses under $1,000 plus other conditions, effective 2026-01-01","Use the current statute, not archived threshold language",["S13","S63"]),
 ("U19","Historical pages contain superseded claims and ranking language","Preserved for coordination integrity; canonical pages supersede them","Use the root dashboard and current source ledger",["S58","S59","S63","S45"]),
 ("U20","No provider has been contacted and no provider has confirmed this job","This is desk research; owner reported prior estimates are not new outreach","Confirm acceptance, scope and availability before hiring",["S44","S45"]),
 ("U21","Source-link presence is not claim verification","Company and project links are not government sources; a generic official link cannot prove unrelated owner facts","Read the source-role and evidence columns; canonical rows identify the supporting source",["S04","S45","S85"]),
 ("U22","License classes do not establish the only possible repair arrangement","BPC §7059 permits qualifying incidental and supplemental work; specific job coverage unverified","Obtain a written scope and responsible-trade confirmation",["S62","S58","S63"]),
 ("U23","Fast Response workers' compensation policy expires 2026-12-18","Policy is listed on the current record; future coverage is not established","Request renewal evidence if work occurs after expiry",["S08"]),
 ("U24","Genteel phone/service-area differences","CSLB (833) 436-8335; website 415-465-5853; website excludes Financial District","Confirm exact neighborhood and contact; drywall scope remains blank",["S65","S75"]),
 ("U25","Rapid Flow phone differs across official sources","CSLB (415) 866-8401; website 844-BAY-FLOW (844-229-3569)","Both are attributed; confirm the service number before hiring",["S56","S73"]),
 ("U26","Advanced Plumbing has an official future-suspension warning","Currently active, but outstanding-liability warning is displayed; not prioritized", "Review the CSLB additional status before considering",["S70"]),
 ("U27","Legacy directory link may not render as a browsable page","docs/results/ contains JSON but no index.html; file existence is not a directory landing page","Historical file preserved; use explicit file links in canonical navigation",["S47","S86"]),
 ("U28","GitHub Pages has had intermittent deployment failures","A reachable site can be an older successful deployment; latest run must be checked separately","Record the delivery PR, successful run and live content after merge",["S45","S80"]),
 ("U29","No permit applicability or code-compliance determination","Official guidance is scope-specific; site framing, fire rating and plumbing scope unknown","Responsible professionals must assess the actual work",["S01","S02","S79"]),
]
TABLES["flagged"] = table("Flagged for review — non-blocking", ["ID", "Issue", "Finding / unverified value", "Review action", "Status"], [
    row([fid,esc(title),esc(detail),esc(action),pill("needs review", "warn")], src)
    for fid,title,detail,action,src in FLAGS
], "These flags do not block publication. They prevent missing evidence from being presented as certainty. Historical flag IDs are retained; current findings supersede older wording.")
TABLES["repo_review"] = table("Repository review and integration decisions", ["Area", "Finding", "Action / evidence"], [
    row(["Mixed repository scope", "Legacy DOE GEMS code/data coexist with several overflow research sets", "Preserved; canonical root dashboard identified. " + slink("S47","README")], ["S47","S48","S86"]),
    row(["Line-by-line inventory", "Tracked text decoded and inventoried; JSON parsed, Python AST-parsed, HTML links/anchors checked", "Per-file counts/hashes: " + slink("S87","line inventory") + "; results: " + slink("S86","audit")], ["S86","S87","S45"]),
    row(["Scientific artifacts", "Unrelated to this repair; pinned download hashes recomputed, full test suite run", "No scientific prediction or leaderboard result is certified by this repair dashboard"], ["S47","S86"]),
    row(["Run-card drift", "Hyphen/underscore filenames and different schemas coexist", "Flagged, not silently rewritten; outside repair scope"], ["S47","S86"]),
    row(["Concurrent sessions", "Multiple append-only claims and overlapping historical dashboards", "Incoming work and regression tests preserved; conflicts logged in " + slink("S45","board")], ["S45","S58","S59","S60"]),
    row(["Source policy", "Older structural checks accepted any link and could label contextual links as proof", "Canonical verifier now checks official/business/manufacturer source roles and evidence-backed license fields"], ["S85","S86","S45"]),
    row(["Historical shortlist", "Earlier ranking and vetting script retained", slink("S58","Open historical shortlist") + "; current order and caveats: <a href='contractors.html'>Contractor ranking</a>"], ["S58","S04"]),
    row(["Deployment", "Pages serves main at repository root; previous runs include both failures and recoveries", "Validate before merge; confirm the new deployment and live pages afterward"], ["S45","S80"]),
], "Audit is non-destructive. A syntax/link/hash pass is not scientific peer review or proof of every historical external claim.")
TABLES["source_ledger"] = {"title":"Source ledger", "columns":["ID","Source / official link","Role","Read status", "Supports / limitation"], "rows":[
    row([sid, slink(sid), pill(s["tier"], "ok" if s["tier"]=="official" else "info"),
         pill(s["status"], "warn" if s["status"] != "verified" else "ok") + "<br>" + s["checked"],
         esc(s["supports"]) + "<br><small>" + esc(s["note"]) + "</small>"], [sid] if s["tier"] in {"official","manufacturer","company"} else [sid,"S45"])
    for sid,s in SOURCES.items()
], "columns":["ID","Source / official link","Role","Read status", "Supports / limitation","Source"], "caption":"Direct reads occurred on 2026-11-08. Blocked review links are labeled and carry no verified values. Project/owner entries also link the official repository record (S45), which documents the entry but does not independently verify its subject. The verifier checks recorded evidence and structure; it does not re-fetch the web."}

# Keep the earlier standalone shortlist reachable without presenting it as current.
HISTORICAL_SHORTLIST = (ROOT / "shortlist.html").read_text()

def prose(title, body):
    return {"type":"prose","title":title,"html":body}
def tab(ref, title=None):
    return {"type":"table","ref":ref, **({"title":title} if title else {})}
def callout(body, tone="info"):
    return {"type":"callout","tone":tone,"html":body}

PAGES = {
 "index.html": {"title":"Dashboard","eyebrow":"San Francisco · Repair decision workspace","h1":"Bathtub overflow trip lever","lede":"A clear hiring plan for a stuck concealed mechanism: compare the scopes, review licensed candidates, and keep every unknown visible.","sections":[
    {"type":"cards","items":[
        {"k":"Owner estimates","v":"3","s":"Different scopes · not comparable all-in bids","tone":"warn"},
        {"k":"Ranked candidates","v":"9","s":"Conditional desk-research order","tone":"info"},
        {"k":"Official license records","v":"11","s":"Direct CSLB reads · 2026-11-08","tone":"ok"},
        {"k":"Confirmed job acceptances","v":"0","s":"No outreach or site inspection","tone":"warn"}]},
    callout("<strong>Best documented starting point: General SF.</strong> Its business pages advertise both plumbing and sheetrock/tape/texture, and CSLB lists B + C-36. This is a conditional first inquiry, not a confirmed hire: crew coverage, exact extraction ability and a combined price remain unverified. <a href='contractors.html'>Compare all nine candidates →</a>", "ok"),
    tab("problem"),
    {"type":"quick","title":"Browse by category","items":[
        {"href":"summary.html","t":"Executive summary","d":"Decision, key risks and next steps"},
        {"href":"contractors.html","t":"Contractor ranking","d":"Reasons, official links, phones and costs"},
        {"href":"estimates.html","t":"Estimates & costs","d":"Scope comparison and blank verified values"},
        {"href":"requirements.html","t":"Requirements","d":"Full input-to-deliverable traceability"},
        {"href":"findings.html","t":"Access & hiring plan","d":"Staged scope and decision gates"},
        {"href":"flagged.html","t":"Flagged for review","d":"Unknowns and irregularities with sources"}]},
    callout("Blank cells mean <strong>unverified</strong>, not zero or no. Business websites are official sources for their own statements; CSLB is the authority for license facts. Owner estimates are transcribed separately. <a href='verification.html'>See exactly what was checked.</a>"),
 ]},
 "summary.html": {"title":"Executive summary","eyebrow":"Overview · Decision and limitations","h1":"Executive summary","lede":"What is known, what is not, and the most defensible next hiring decision.","sections":[
    prose("Decision", "<p>Start with <strong>General SF</strong>, then <strong>Handyman Heroes</strong> and <strong>Rapid Flow</strong>: each advertises plumbing and drywall-related services and has B + C-36 on its CSLB record. General SF has the clearest sheetrock/tape/texture wording; Handyman Heroes adds documented patch/texture/cleanup services and a workers' compensation policy, but also an official citation disclosure. This order is conditional on a satisfactory site-specific proposal, not evidence that any firm can extract this particular mechanism.</p>"),
    tab("ranking","Hiring order and reasons"),
    prose("Cost conclusion", "<p>The owner reports <strong>$614</strong> for Expert Plumbing Solutions' waste-and-overflow replacement, <strong>$550</strong> for Bay Area Plumbing's lever/plug/spout-with-diverter work, and <strong>$135</strong> for Fast Response's repair/adjustment. These are owner-provided figures, not verified prices. They describe different scopes; drywall inclusion was not stated. No all-in total, cheapest-option claim or savings estimate is justified. Verified amount cells remain blank.</p>"),
    prose("Access and occupied-unit plan", "<p>Preserve the preference for a conservative above-access assessment, but do not assume it is feasible. Watco documents plate/linkage adjustment on example products; Oatey describes inspecting concealed joints during a replacement test. The installed model, cause of seizure, framing and ceiling rating are unknown. Request one coordinated proposal with separate diagnostic, contingent below-access, plumbing, protection, testing and restoration items. Confirm tenant scheduling, dust containment and cleanup before authorizing work.</p>"),
    prose("Important cautions", "<p>Four shortlisted records show workers' compensation exemptions. Handyman Heroes has a disclosure and a website C-10 claim not on its reviewed license. Fast Response has an address discrepancy and a policy expiring in December 2026. Yelp direct fetches were blocked, so current ratings/counts play no role in the ranking. No provider has been contacted or accepted the work.</p>"),
    tab("plan","What a complete proposal should contain"),
    prose("Official rules and evidence", "<p>SF DBI requires a permit before cutting/replacing pipes subject to code exemptions; minor wallboard repair guidance does not decide the plumbing scope. License classifications and incidental-work rules do not establish this job's coverage. See <a href='permits.html'>Official rules</a>, <a href='sources.html'>Source ledger</a> and <a href='flagged.html'>Flagged for review</a>. This dashboard is procurement analysis, not a code determination or engineering instruction.</p>"),
 ]},
 "requirements.html": {"title":"Requirements","eyebrow":"Overview · Complete input register","h1":"Requirements, line by line","lede":"Every requested deliverable and site constraint, with implementation status and explicit evidence limits.","sections":[tab("requirements")]},
 "estimates.html": {"title":"Estimates & costs","eyebrow":"Decision · Scope before price","h1":"Estimates and cost analysis","lede":"Three different scopes cannot be compared as equivalent all-in bids. Unknown prices stay blank.","sections":[tab("estimates"),tab("brief_quotes"),tab("costs"),callout("Do not add the three quotes together or choose the lowest as the best repair. First normalize the component, access method, testing, ceiling restoration, protection and finish scope.","warn")]},
 "contractors.html": {"title":"Contractor ranking","eyebrow":"Decision · Evidence before reputation","h1":"Contractors, ranking and reviews","lede":"Official business links and phone numbers, transparent reasons, and a separate regulator-checked license register.","sections":[callout("<strong>No provider has been contacted and no provider has confirmed this job.</strong> Ranking is a conditional screening order. Exact repair skill, occupied-unit references, availability and all-in cost are unverified for every candidate. third-party review values are not used.","warn"),tab("ranking"),tab("contractors"),tab("support"),tab("reviews")]},
 "findings.html": {"title":"Access & hiring plan","eyebrow":"Decision · Protect the property and occupants","h1":"Access strategy and hiring controls","lede":"A staged, contingent scope that preserves the above-access preference without promising it is safe.","sections":[tab("plan"),prose("How the order was decided", "<p>First priority: documented plumbing plus drywall services in SF. Next: official license classes and workers' compensation evidence, then disclosed irregularities. The three owner-quoted plumbers remain useful plumbing options but have less verified combined-service evidence. No numerical score is fabricated from blocked reviews, and a broader license list is not treated as proof of better workmanship.</p>"),prose("Historical research", "<p>The earlier <a href='shortlist.html'>ranked shortlist and call script</a> and <a href='sf-overflow-audit/index.html'>parallel audit</a> are preserved. Their historical claims do not override the current source ledger or flags.</p>")]},
 "technical.html": {"title":"Technical context","eyebrow":"Reference · Manufacturer evidence","h1":"What the mechanism sources establish","lede":"Manufacturer examples explain the assembly, not the condition of your bathtub.","sections":[tab("technical"),callout("No photographs or installed model were supplied. Do not infer a brand, part number, cause of seizure or safe extraction force from these examples.","warn")]},
 "permits.html": {"title":"Official rules","eyebrow":"Reference · Neutral regulatory context","h1":"Permits, licensing and scope","lede":"Official guidance only. The actual work scope determines applicability.","sections":[tab("permits")]},
 "brief.html": {"title":"Owner brief","eyebrow":"Reference · Primary transcription","h1":"Owner-provided project record","lede":"This page preserves the supplied facts and estimates without labeling them independently verified.","sections":[tab("problem"),tab("brief_quotes"),callout("Source roles: the owner is the source of these statements; business identity and license status were checked separately. No reference photographs were attached.","warn")]},
 "sources.html": {"title":"Source ledger","eyebrow":"Reference · Manual-review links","h1":"Sources and evidence","lede":"Follow the original source for each claim. Read dates and limitations are part of the record.","sections":[tab("source_ledger"),prose("Evidence register", "<p><a href='data/canonical/source_evidence.json'>Direct-source excerpts and CSLB record stamps</a> document what was read. Company statements are not independent performance evidence. Review pages blocked to automated retrieval have no verified ratings or counts.</p>")]},
 "verification.html": {"title":"Verification","eyebrow":"Audit · Reproducible checks","h1":"Verification and publication checks","lede":"Structural checks, source-role checks and direct-read evidence are reported separately.","sections":[{"type":"verification_summary"},{"type":"row_audit"},prose("Method and limits", "<p>The build validates source IDs, cell counts, blank flags, source roles, license-field agreement with the direct-read register, navigation, internal links/anchors and privacy wording. The source ledger records direct reads on 2026-11-08; the automated verifier performs <strong>no network check</strong>. A contextual official link does not verify an owner statement. Repository-wide inventory and tests are linked on <a href='repo-review.html'>Repo review</a>. Deployment is confirmed separately after merge.</p>")]},
 "repo-review.html": {"title":"Repo review","eyebrow":"Audit · Preserve and distinguish","h1":"Repository review","lede":"What was inspected, what was preserved, and what remains outside this repair project's evidence.","sections":[tab("repo_review"),{"type":"quick","title":"Audit artifacts and preserved research","items":[
    {"href":"data/canonical/repo_audit.json","t":"Repository audit JSON","d":"Syntax, inventory, hashes and checks"},
    {"href":"data/canonical/repo_line_inventory.json","t":"Per-file line inventory","d":"Line counts and SHA-256 digests"},
    {"href":"data/canonical/verification_report.json","t":"Site verification JSON","d":"Machine-readable structural checks"},
    {"href":"shortlist.html","t":"Historical shortlist","d":"Earlier ranking and vetting script"},
    {"href":"verification-log.html","t":"Earlier verification log","d":"Preserved concurrent-session work"},
    {"href":"sf-overflow-audit/index.html","t":"Parallel audit","d":"Separate research set, not canonical data"}]}]},
 "flagged.html": {"title":"Flagged for review","eyebrow":"Audit · Visible unknowns","h1":"Flagged for review","lede":"Unverified values and irregularities, with original-source links. These items do not block publication.","sections":[tab("flagged"),callout("Use the item ID when requesting a correction. Blank means unverified. Historical pages remain available for review, but the canonical dashboard and current evidence register control this decision analysis.","warn")]},
}
