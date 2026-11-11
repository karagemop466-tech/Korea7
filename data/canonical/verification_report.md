# Dashboard verification report

Generated: 2026-11-11T02:27:27+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 21 pages generated |
| Every table row has a source link | PASS | 1968 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 1937 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 431 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 151 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 86 official/manufacturer sources marked verified (read dates 2026-11-07 to 2026-11-11); 156 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 21
- tables: 45
- rows: 959
- source_ledger_entries: 179
- verified_sources: 156
- official_or_manufacturer_verified: 86
- generated_tbody_rows: 1968
- internal_links_checked: 1937
- unique_external_links: 431
- published_text_files_scanned: 151

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources.
  Each CSLB record's own "Data current as of" stamp is transcribed in
  `data/canonical/cslb_records.json` (2026-11-08 reads printed 11/8/2026).
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/, https://www.plumbing1builders.com/ (documented, never linked from a row).
