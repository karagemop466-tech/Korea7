# Dashboard verification report

Generated: 2026-11-08T23:01:20+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 421 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 501 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 52 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 121 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 17 official/manufacturer sources marked verified; 52 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 13
- tables: 14
- rows: 197
- source_ledger_entries: 63
- verified_sources: 52
- official_or_manufacturer_verified: 17
- generated_tbody_rows: 421
- internal_links_checked: 501
- unique_external_links: 52
- published_text_files_scanned: 121

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources. Prior CSLB checks printed
  "Data current as of 11/7/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
