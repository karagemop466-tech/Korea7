# Dashboard verification report

Generated: 2026-11-08T23:23:05+00:00

Offline structural, privacy and direct-read register consistency; no network check

| Check | Result | Detail |
|---|---|---|
| Build output complete | PASS | 13 canonical pages |
| Every table row has a source link | PASS | 440 rendered rows; 0 missing |
| Blank values are flagged UNVERIFIED | PASS | 0 unflagged blanks |
| Internal links resolve | PASS | 391 links; 0 broken |
| Anchor targets resolve | PASS | 0 broken anchors |
| External links are in the source ledger | PASS | 56 unique external links; 0 unknown/dead |
| Navigation consistent | PASS | 0 issues |
| Privacy sweep (internal-only wording) | PASS | 121 published text files; 0 matches |
| No unfilled template markers | PASS | 0 matches |
| Dead sources not linked | PASS | 0 dead-source links |
| Source ledger records prior direct reads | PASS | 29 official/manufacturer; 58 direct-read sources overall (metadata only; no network check) |
| Row source roles and evidence fields | PASS | 0 issues |
| JSON snapshot matches generator | PASS | 0 stale/missing entries |

## Counts

- pages: 13
- tables: 15
- rows: 201
- source_ledger_entries: 68
- verified_sources: 58
- official_or_manufacturer_verified: 29
- generated_tbody_rows: 440
- internal_links_checked: 391
- unique_external_links: 56
- published_text_files_scanned: 121

## Limitations

- Source links were read on 2026-11-08; this verifier performs no network check.
- A source-role/structure PASS does not independently prove every sentence.
- Owner-only amounts remain blank in verified-value cells; original transcriptions are labeled separately.
- Blocked Yelp pages have no verified ratings, counts or exact-job reviews.
- Repository-wide audit and deployment are separate checks; see repo-review.html and COORDINATION.md.
