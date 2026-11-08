# Dashboard verification report

Generated: 2026-11-08T23:20:34+00:00

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 pages generated |
| Every table row has a source link | PASS | 444 tbody rows checked, 0 missing links |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blank rows |
| Internal links resolve | PASS | 518 internal links checked, 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 64 unique external links, 0 unknown/dead |
| Navigation consistent | PASS | 0 nav issues |
| Privacy sweep (internal-only wording) | PASS | 121 files scanned, 0 matches |
| No unfilled template markers | PASS | 0 template-marker matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Official sources recorded verified (metadata) | PASS | 22 official/manufacturer sources recorded verified 2026-11-08; 63 sources verified overall. This is ledger metadata; no network check of every URL is performed by this script. |

## Counts

- pages: 13
- tables: 17
- rows: 213
- source_ledger_entries: 75
- verified_sources: 63
- official_or_manufacturer_verified: 22
- generated_tbody_rows: 444
- internal_links_checked: 518
- unique_external_links: 64
- published_text_files_scanned: 121

## Notes

- Every table row is emitted with a Source column from `data/canonical/site_data.json`.
- Unverified values are blank in verified cells and published on `flagged.html`.
- Official values were read directly from the issuing site on 2026-11-08; CSLB records printed
  "Data current as of 11/8/2026".
- Yelp URLs return HTTP 403 to automated access and are flagged as platform snapshots.
- Dead sources:  (documented, never linked from a row).
