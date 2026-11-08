# Dashboard verification report

Generated: 2026-11-08T23:17:48+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 14 pages generated |
| Every table row has a source link | PASS | 551 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 559 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 68 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 122 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 22 official/manufacturer sources marked verified (18 of them with a 2026-11-08 read date); 64 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 14
- tables: 18
- rows: 262
- source_ledger_entries: 79
- verified_sources: 64
- official_or_manufacturer_verified: 22
- generated_tbody_rows: 551
- internal_links_checked: 559
- unique_external_links: 68
- published_text_files_scanned: 122

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources. Prior CSLB checks printed
  "Data current as of 11/7/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
