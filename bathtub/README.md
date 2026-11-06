# Bathtub overflow trip-lever project

Internal working folder for the San Francisco bathtub wastewater overflow trip-lever repair.
Published site: **<https://karagemop466-tech.github.io/Korea7/docs/bathtub/>**

> This folder is unrelated to the DOE GEMS geothermal audit that makes up the rest of this
> repository. It lives here because the session's repository is Korea7. Nothing in the GEMS
> audit was changed except one navigation link.

## Start here

| Document | What it answers |
|---|---|
| [`EXECUTIVE-BRIEF.md`](EXECUTIVE-BRIEF.md) | The whole project on one page: situation, numbers, headline finding, next steps, unknowns. |
| [`../reports/repo-audit-2026-11-06.md`](../reports/repo-audit-2026-11-06.md) | Line-by-line verification of this repository against its own claims. |

## Data (single source of truth for the site)

Everything the site renders comes from these files. Edit a file, re-run the generator, and the
site changes — nothing is hand-written into the HTML.

| File | Contents |
|---|---|
| `data/requirements.json` | 29 requirements with origin, priority and verification status |
| `data/sources.json` | 19 sources with the exact quoted passage each one supports |
| `data/estimates.json` | The three 2026-08-30 quotes, normalised, plus what is missing from all three |
| `data/contractors.json` | 9 CSLB licence records, transcribed field by field |
| `data/compliance.json` | 11 permit / drywall / lead-safe / asbestos / tenancy checks |
| `data/technical.json` | The assembly, from a granted US patent, and why it seizes |
| `data/flagged.json` | 17 fields that could not be verified, with what would close each one |

## Rebuild and verify

```bash
python scripts/build_bathtub_site.py     # regenerate docs/bathtub/
python scripts/check_bathtub_site.py     # fail-closed checks; exit 1 on any failure
```

The checker enforces, among other things: every internal link resolves, every external host is an
official source (or a documented exception), every external URL in the data actually renders on the
site, no placeholder text, no secrets, and no verified-looking chip in a table row without a source
link beside it.

## The rules this project follows

1. **A row is only "verified" if an official site confirms it.** Directory listings, reviews and
   aggregators are used only to discover a licence *number*, which is then checked against CSLB.
2. **A value that cannot be confirmed is left blank and flagged.** It is never inferred, averaged,
   or copied from a similar job.
3. **Owner-supplied facts are labelled `owner_reported`** and are never presented as verified.
4. **Confidentiality is honoured by omission, not by falsification.** One internal scheduling reason
   is not recorded anywhere. Nothing in the analysis was softened to protect it.

## Known limits of this project

- **No price is verified.** The three quotes have no licence numbers attached, so the firms could not
  be checked.
- **Yelp could not be read.** `yelp.com` returned HTTP 403 to automated requests all session. The
  site ships deep links instead and reproduces no rating.
- **The CSLB bulk master file could not be downloaded** (served behind a form). Per-licence
  verification was used instead, which is more precise but narrower than a full C-36 sweep of the
  city. A complete list is available to a human at CSLB's *Find A Licensed Contractor* by city and
  classification.
- **The build year of the unit is unknown**, which is the single fact that decides whether the
  federal lead-safe rule applies to the ceiling opening.
