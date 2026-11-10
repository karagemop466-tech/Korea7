#!/usr/bin/env python3
"""Independent live re-verification of the canonical CSLB records.

Reads every CSLB License Detail page cited by the site's canonical dataset,
parses the selected official fields, and diffs them against
data/canonical/cslb_records.json.  Writes data/canonical/live-audit-<date>.json.

This is a *live reachability + field* check.  It only checks the fields it
parses; anything it cannot parse is reported as unparsed, never inferred.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data/canonical/cslb_records.json"
UA = "Mozilla/5.0 (compatible; Korea7-audit/1.0; +https://karagemop466-tech.github.io/Korea7/)"


def fetch(url: str, timeout: int = 45) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 - report, never infer
        return -1, f"__ERROR__ {type(e).__name__}: {e}"


def text_of(html: str) -> str:
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</(td|th|tr|div|p|li|h\d)>", "\n", html, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = (txt.replace("&nbsp;", " ").replace("&amp;", "&")
              .replace("&quot;", '"').replace("&#39;", "'").replace("&lt;", "<")
              .replace("&gt;", ">"))
    return re.sub(r"[ \t]+", " ", txt)


def parse(html: str) -> dict:
    t = text_of(html)
    out: dict = {}

    m = re.search(r"License Detail for License\s*#?\s*([0-9A-Za-z\-]+)", t)
    out["license_on_page"] = m.group(1).strip() if m else None

    m = re.search(r"Data current as of\s*([0-9/]+[^\n]*)", t)
    out["record_stamp"] = m.group(1).strip() if m else None

    m = re.search(r"Business Phone Number:\s*(\([0-9]{3}\)\s*[0-9]{3}-[0-9]{4}|[0-9\- ]{7,})", t)
    out["phone_on_record"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None

    m = re.search(r"Expire Date\s*\n?\s*([0-9]{2}/[0-9]{2}/[0-9]{4})", t)
    out["expire_date"] = m.group(1) if m else None

    if re.search(r"This license is current and active", t):
        out["status"] = "current and active"
    elif re.search(r"license is (?:expired|suspended|revoked|cancelled)", t, re.I):
        m = re.search(r"This license is ([^.\n]+)", t)
        out["status"] = m.group(1).strip() if m else "other"
    else:
        out["status"] = None

    classes = re.findall(r"\n\s*([A-C][0-9]{0,2}(?:-[0-9]{1,2})?)\s*-\s*([A-Z][A-Z ,/&\-]+)", t)
    seen, cls = set(), []
    for code, _name in classes:
        code = code.strip()
        if code not in seen and code not in {"A", "B", "C"} or (
            code in {"A", "B", "C"} and code not in seen
        ):
            if re.match(r"^(A|B|C-?[0-9]{1,2}|C[0-9]{1,2})$", code):
                seen.add(code)
                cls.append(code)
    out["classifications"] = cls
    return out


def norm_date(d: str | None) -> str | None:
    if not d:
        return None
    mm, dd, yy = d.split("/")
    return f"{yy}-{mm.zfill(2)}-{dd.zfill(2)}"


def norm_class(c: str) -> str:
    c = c.upper().replace("-", "")
    return {"C36": "C36", "C10": "C10", "C9": "C9", "C4": "C4", "C16": "C16", "C20": "C20"}.get(c, c)


def main() -> int:
    data = json.loads(DATASET.read_text())
    today = dt.date.today().isoformat()
    results, mismatches, errors = [], [], []

    for rec in data["records"]:
        lic = rec["license"]
        url = rec["source_url"]
        code, html = fetch(url)
        row = {
            "license": lic,
            "name_in_dataset": rec["name_on_record"],
            "url": url,
            "http_status": code,
            "live": None,
            "comparison": {},
            "mismatches": [],
        }
        if code != 200 or html.startswith("__ERROR__") or "License Detail" not in html:
            row["error"] = (html[:200] if html.startswith("__ERROR__") else f"HTTP {code}")
            errors.append(lic)
            results.append(row)
            time.sleep(1.0)
            continue

        live = parse(html)
        row["live"] = live

        checks = {
            "license": (rec["license"], live.get("license_on_page")),
            "expire_date": (rec["expire_date"], norm_date(live.get("expire_date"))),
            "phone_on_record": (re.sub(r"[^0-9]", "", rec["phone_on_record"] or ""),
                                re.sub(r"[^0-9]", "", live.get("phone_on_record") or "")),
            "status": (rec["status"], live.get("status")),
            "classifications": (sorted({norm_class(c) for c in rec["classifications"]}),
                                sorted({norm_class(c) for c in (live.get("classifications") or [])})),
        }
        for field, (stored, seen) in checks.items():
            row["comparison"][field] = {"dataset": stored, "live": seen,
                                        "match": stored == seen if seen is not None else None}
            if seen is None:
                row["mismatches"].append(f"{field}: NOT PARSED from live page (not inferred)")
            elif stored != seen:
                row["mismatches"].append(f"{field}: dataset={stored!r} live={seen!r}")
        if row["mismatches"]:
            mismatches.append(lic)
        results.append(row)
        time.sleep(1.0)

    report = {
        "session": "arena/33211fbf-korea7",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "method": "Each CSLB License Detail page fetched live with urllib and parsed field-by-field; "
                  "unparsed fields are reported as such and never inferred.",
        "records_checked": len(results),
        "records_reachable": len(results) - len(errors),
        "records_with_mismatch": len(mismatches),
        "unreachable": errors,
        "mismatch_licenses": mismatches,
        "results": results,
    }
    out = ROOT / f"data/canonical/live-audit-{today}.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"checked {len(results)} records: {len(results)-len(errors)} reachable, "
          f"{len(errors)} unreachable, {len(mismatches)} with a mismatch")
    for m in mismatches:
        print("  MISMATCH", m)
    for e in errors:
        print("  UNREACHABLE", e)
    print("wrote", out.relative_to(ROOT))
    return 0 if not errors and not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
