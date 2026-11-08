# Dashboard verification report

Generated: 2026-11-08T23:17:01+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 1115 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 1081 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 362 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 127 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 22 official/manufacturer sources marked verified; 53 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 13
- tables: 19
- rows: 540
- source_ledger_entries: 78
- verified_sources: 53
- official_or_manufacturer_verified: 22
- generated_tbody_rows: 1115
- internal_links_checked: 1081
- unique_external_links: 362
- published_text_files_scanned: 127

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources.
  Current ranking sources were read directly on 2026-11-08; CSLB records printed "Data current as of 11/8/2026".
  Historical sources are labeled and excluded from the current ranking.
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
