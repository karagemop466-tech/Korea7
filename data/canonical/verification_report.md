# Dashboard verification report

Generated: 2026-11-08T23:13:44+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 15 pages generated |
| Every table row has a source link | PASS | 675 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 767 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 71 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 123 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official sources verified directly | PASS | 27 official/manufacturer sources verified 2026-11-07 to 2026-11-08; 68 sources verified overall |

## Counts

- pages: 15
- tables: 23
- rows: 324
- source_ledger_entries: 85
- verified_sources: 68
- official_or_manufacturer_verified: 27
- generated_tbody_rows: 675
- internal_links_checked: 767
- unique_external_links: 71
- published_text_files_scanned: 123

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- Official values were read directly from the issuing site on the date shown for each source
  in the source ledger; CSLB records printed their own "Data current as of" stamp, which is
  transcribed per record in `data/canonical/cslb_records.json`.
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources: https://homeguides.sfgate.com/repair-trip-lever-tub-drain-41958.html, https://inspectandtest.net/guides/bathtub-overflow-drain/ (documented, never linked from a row).
