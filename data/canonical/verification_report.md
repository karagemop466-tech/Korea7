# Dashboard verification report

Generated: 2026-11-10T05:55:24+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 20 pages generated |
| Every table row has a source link | PASS | 1687 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 1784 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 410 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 147 files scanned, 0 matches |
| Archived microsites privacy sweep (scheduling context) | PASS | 40 archived files in bathtub-overflow, sf-overflow-audit, docs/bath scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 66 official/manufacturer sources marked verified (read dates 2026-11-07 to 2026-11-10); 129 sources marked verified overall (metadata only; no network check) |

## Counts

- pages: 20
- tables: 37
- rows: 818
- source_ledger_entries: 147
- verified_sources: 129
- official_or_manufacturer_verified: 66
- generated_tbody_rows: 1687
- internal_links_checked: 1784
- unique_external_links: 410
- published_text_files_scanned: 147

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- The ledger records source-specific check dates; this automated check does not re-fetch sources.
  Each CSLB record's own "Data current as of" stamp is transcribed in
  `data/canonical/cslb_records.json` (2026-11-08 reads printed 11/8/2026).
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
