# Dashboard verification report

Generated: 2026-11-07T20:42:15+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 382 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 425 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 48 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 104 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official sources verified directly | PASS | 14 official/manufacturer sources verified 2026-11-07; 44 sources verified overall |

## Counts

- pages: 13
- tables: 14
- rows: 179
- source_ledger_entries: 55
- verified_sources: 44
- official_or_manufacturer_verified: 14
- generated_tbody_rows: 382
- internal_links_checked: 425
- unique_external_links: 48
- published_text_files_scanned: 104

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- Official values were read directly from the issuing site on 2026-11-07; CSLB records printed
  "Data current as of 11/7/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
