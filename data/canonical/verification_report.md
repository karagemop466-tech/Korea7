# Dashboard verification report

Generated: 2026-11-08T23:41:22+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 628 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 570 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 77 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 121 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official sources verified directly | PASS | 26 official/manufacturer sources verified (25 checked 2026-11-08); 75 sources verified overall |

## Counts

- pages: 13
- tables: 19
- rows: 289
- source_ledger_entries: 90
- verified_sources: 75
- official_or_manufacturer_verified: 26
- generated_tbody_rows: 628
- internal_links_checked: 570
- unique_external_links: 77
- published_text_files_scanned: 121

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- Official values were read directly from the issuing site on 2026-11-08; CSLB records printed
  "Data current as of 11/8/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
