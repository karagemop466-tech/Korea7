# Dashboard verification report

Generated: 2026-11-08T23:15:05+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 432 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 510 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 62 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 121 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official sources verified directly | PASS | 21 official/manufacturer sources recorded verified 2026-11-08; 60 sources verified overall |

## Counts

- pages: 13
- tables: 17
- rows: 207
- source_ledger_entries: 72
- verified_sources: 60
- official_or_manufacturer_verified: 21
- generated_tbody_rows: 432
- internal_links_checked: 510
- unique_external_links: 62
- published_text_files_scanned: 121

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- Official values were read directly from the issuing site on 2026-11-08; CSLB records printed
  "Data current as of 11/8/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources:  (documented, never linked from a row).
