"""Content-integrity repairs found by a line-by-line sweep of the published pages.

Session ``arena/33f7b0ca-korea7``, 2026-11-11. This module makes **no new factual
claims** and reads **no new sources**. It repairs three defects that a line-by-line
review of the rendered site found, and it publishes one flag recording the repairs:

1. ``findings`` carried two rows with the identifier ``F10``. The later, appended
   workers'-compensation finding is renumbered **F20**, and the U46 cross-reference
   that pointed at it is updated.
2. Three live strings still described an **eight-record** candidate pool after the
   pool grew to sixteen: the Contractors page lede, requirement **R09** and
   requirement **R15**. A fourth occurrence in finding **F04** is corrected in the
   same pass.
3. ``shortlist.html`` — a static page still linked from the navigation but no longer
   produced by the generator — published "Eight named candidates … verified for 8 of
   9" beside the current sixteen-record dataset, with no date banner. It is repaired
   in place (see the commit) with a dated snapshot note and current counts.

The 2026-11-11 licence re-read itself is owned by a concurrent session's module
(``scripts/reread_1111.py``, page ``reread-1111.html``, artifact
``data/canonical/reread-2026-11-11.json``); this module deliberately does not
duplicate it.
"""
from __future__ import annotations

import re

FLAG_TEXT = (
    "A line-by-line sweep of the published pages found a duplicated finding identifier and three "
    "stale candidate counts"
)


def _sub(text, old, new, sink):
    if isinstance(text, str) and old in text:
        sink.append(old)
        return text.replace(old, new)
    return text


def _repair_counts(c, changed):
    c.PAGES["contractors.html"]["lede"] = _sub(
        c.PAGES["contractors.html"]["lede"],
        "Eight candidates had active CSLB license records on 2026-11-07",
        "Sixteen candidates had active CSLB license records re-read on 2026-11-08",
        changed,
    )
    for row in c.TABLES["requirements"]["rows"]:
        if row["cells"][0] == "R09":
            row["cells"][3] = _sub(row["cells"][3], "Eight licensed candidates researched",
                                   "Sixteen licensed candidates researched", changed)
        if row["cells"][0] == "R15":
            row["cells"][3] = _sub(row["cells"][3], "CSLB records checked for eight candidates",
                                   "CSLB records checked for sixteen candidates", changed)
    for row in c.TABLES["findings"]["rows"]:
        if row["cells"][0] == "F04":
            row["cells"][1] = _sub(row["cells"][1], "All eight verified candidates",
                                   "All sixteen verified candidates", changed)
            row["cells"][2] = _sub(row["cells"][2], "Eight official License Detail pages each print",
                                   "Sixteen official License Detail pages each print", changed)


def _repair_duplicate_finding_id(c):
    rows = c.TABLES["findings"]["rows"]
    duplicates = [r for r in rows
                  if str(r["cells"][0]) == "F10" and "workers'-compensation" in str(r["cells"][1])]
    if not duplicates:
        return False
    row = duplicates[0]
    rows.remove(row)
    row["cells"][0] = "F20"
    rows.append(row)
    for flagged in c.TABLES["flagged"]["rows"]:
        if str(flagged["cells"][0]) == "U46":
            flagged["cells"][2] = str(flagged["cells"][2]).replace("see F10", "see F20")
    return True


def integrate(c):
    changed = []
    _repair_counts(c, changed)
    renumbered = _repair_duplicate_finding_id(c)

    next_id = max(int(str(r["cells"][0])[1:]) for r in c.TABLES["flagged"]["rows"]
                  if str(r["cells"][0])[1:].isdigit()) + 1
    flag_id = "U%d" % next_id
    c.TABLES["flagged"]["rows"].append({
        "cells": [
            flag_id,
            FLAG_TEXT,
            ("The findings table published two rows identified as F10, and the Contractors page lede, "
             "requirements R09/R15 and finding F04 still said “eight” candidates after the scored pool "
             "grew to sixteen. Repaired in this pass: the appended workers'-compensation finding is F20 "
             "and the counts read sixteen. No score, source, price or licence value was changed, and the "
             "separately published 2026-11-11 licence re-read is unaffected."),
            "No action needed — corrected and re-published; re-read each CSLB record on the hire date",
            c.pill("resolved / documented", "ok"),
        ],
        "src": ["S04", "S120"],
    })

    # Keep the published counts/range consistent with the new flag, as the other modules do.
    _max = max(int(str(r["cells"][0])[1:]) for r in c.TABLES["flagged"]["rows"]
               if str(r["cells"][0])[1:].isdigit())
    for page in c.PAGES.values():
        for block in page["sections"]:
            for key, value in list(block.items()):
                if isinstance(value, str):
                    value = re.sub(r"U01–U\d+", "U01–U%d" % _max, value)
                    value = re.sub(r"\b\d+ flagged items\b",
                                   "%d flagged items" % len(c.TABLES["flagged"]["rows"]), value)
                    block[key] = value
    for block in c.PAGES["index.html"]["sections"]:
        if block["type"] == "cards":
            for card in block["items"]:
                if card.get("k") == "Flagged for review":
                    card["v"] = str(len(c.TABLES["flagged"]["rows"]))

    return {"flag_id": flag_id, "strings_fixed": changed, "finding_renumbered": renumbered}
