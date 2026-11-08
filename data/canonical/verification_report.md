# Dashboard verification report

Generated: 2026-11-08T22:59:16+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 417 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 500 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 51 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 121 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official source ledger entries | PASS | 17 official/manufacturer sources marked verified in the ledger; 51 sources marked verified overall (not live checks) |

## Counts

- pages: 13
- tables: 14
- rows: 195
- source_ledger_entries: 62
- verified_sources: 51
- official_or_manufacturer_verified: 17
- generated_tbody_rows: 417
- internal_links_checked: 500
- unique_external_links: 51
- published_text_files_scanned: 121

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources. Prior CSLB checks printed
  "Data current as of 11/7/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
