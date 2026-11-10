# Dashboard verification report

Generated: 2026-11-10T01:00:02+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 17 pages generated |
| Every table row has a source link | PASS | 1489 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 1558 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 395 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 140 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 55 official/manufacturer sources marked verified (read dates 2026-11-07 to 2026-11-10); 112 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 17
- tables: 29
- rows: 731
- source_ledger_entries: 130
- verified_sources: 112
- official_or_manufacturer_verified: 55
- generated_tbody_rows: 1489
- internal_links_checked: 1558
- unique_external_links: 395
- published_text_files_scanned: 140

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources.
  Each CSLB record's own "Data current as of" stamp is transcribed in
  `data/canonical/cslb_records.json` (2026-11-08 reads printed 11/8/2026).
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
