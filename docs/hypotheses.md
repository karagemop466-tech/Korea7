# Candidate geological hypotheses — Korea7 lane selection (2026-11-04)

Written **before** experiment code, per the brief. Layers actually obtainable in
this sandbox (hash-verified owner mirrors, see `evidence/data_provenance.json`):
1 m-DEM-derived lidar-scarp stack (12 u8 bands), GeoDAWN radiometrics
(K, Th, U, TC), radiometric ratios + upward-continued magnetics
(ThK, UK, UTh, TMI_up150), TIGER road distance, GDR well/spring points.
The 19-band `training_features.tif` mirror is **not** obtainable today
(source repos return HTTP 404; verified 2026-11-04), so any hypothesis needing
strain/conductivity/gravity bands is *not viable in this session* and is excluded
rather than proposed as viable.

Evaluation for ranking: shared `GEMSDOE32-SGMC-CAL-v3.0` HOLDOUT-DTI
(off-catalogue SGMC faults as blind-fault proxy; among the nine focus winners it
rank-agrees with the user-reported leaderboard, Spearman ρ = 0.95, n = 9 per
GEMSDOEkarage3 2026-10-31 — a consistency check, not proof) and
`GEMSDOE32-HIDE-RECOVER-v3.0` (buffered whole-segment catalogue recovery,
reported secondarily because it is known to rank *against* the leaderboard for
off-catalogue emitters). Gate to beat: SGMC-CAL best of the nine =
GEMSDOE36 0.0644 [0.0571, 0.0720] (reproduced protocol; champion GEMSDOE32 =
0.0641 [0.0567, 0.0716], reproduced exactly in this repo).

| Rank | Hypothesis | Layer(s) + physical signature | Why it should catch catalogue-missing faults | Non-fault mimic | Difference from nine-site family / this repo | Expected DTI gain vs cost |
|---|---|---|---|---|---|---|
| 1 (LANE) | **Scarp × radiometric-concordance blind-fault emission** | Lidar `step_max`+`coh100` (a coherent topographic step) AND-gated (geometric mean) with radiometric-ratio gradient magnitude (ThK/UK/UTh edges = lithologic/alteration contrast), emitted only >2 px from catalogue | A young fault under thin cover can show a subtle scarp *and* displace/alter near-surface material; either signal alone is common, their colocation is the rarer, structural case. The >2 px gate copies the champion's measured winning geometry (scored GT is off-catalogue) | Lithologic contacts with erosional scarps; roads/terraces mimicking steps (controlled in E3 via TIGER road distance) | Nine winners all emit one shared 19-band ridge surface (h19-5 family; exact subset chain measured). This surface is built only from the external lidar+radiometric stacks and AND-gates two independent physics; emission is greedy 300 m-kernel coverage, not d1.5/d2.8 Poisson thinning | Highest / medium — all inputs in hand, evaluator 11 s |
| 2 | **Deep basement edge under cover** | `TMI_up150` horizontal-gradient ridge (upward continuation suppresses shallow sources) × lidar coherence | Blind basement faults beneath alluvium lack scarps but offset magnetic basement; catalogue mapping from surface geology misses them preferentially in basins | Intrusive/lithologic magnetic contacts | Fleet tilt/worm/euler lanes used full-resolution magnetics from the 19-band stack; the u8 upward-continued band + coherence gate is a different, deeper-source filter | Medium / medium (E2 adds this as third concordance term) |
| 3 | **Road-mimic-controlled emission** (control variant, not standalone geology) | Winner of E1/E2 minus pixels within 100 m of a TIGER road, budget refilled by the same greedy rule | Removes the largest named non-fault mimic class for scarp detectors without touching geologic signal elsewhere | Real faults can follow valleys/roads — exclusion could remove true dots; measured as A/B | No nine-site winner documents a road-distance exclusion; their surface is unavailable for one | Unknown / low (E3) |
| 4 | **Geothermal discharge alignment** | GDR well/spring points: oriented local density anisotropy intersecting lidar lineaments | Permeable unmapped faults leak; aligned springs can trace them | Drilling/sampling bias along roads and known fields; points are sparse | Tried in spirit by fleet spring lanes (karage1 KP1 unscored in brief); our point file is in hand but bias correction is not — not run this session | Low–unknown / high |
| 5 | **Catalogue tip/stepover geometry only** | Labels geometry: extend segment tips, fill stepovers at r≈30 px | New faults often continue known systems | n/a (geometric) | **Already a nine-site winner (GEMSDOE33 h33d, 0.2632 user-reported)** — excluded as non-novel for this lane | Not run |

## Predeclared experiments (budget: 3, then stop)

- **E1** — H1 surface, greedy triangular-kernel coverage emission, budget
  37,654 dots (= champion), catalogue distance > 2 px, footprint only.
- **E2** — E1 surface × TMI_up150-gradient concordance term (H2), same emission.
- **E3** — better of E1/E2 on SGMC-CAL, with road-distance mimic control (H3).

Promotion rule (separate selector step, per protocol): a candidate is
*promotable for the owner's selector decision* only if SGMC-CAL HOLDOUT-DTI
beats 0.0644 with bootstrap CI reported, no leakage canary AUC > 0.90,
≤70 % of dots within 3 px of every nine-site winner and surface rank-ρ ≤ 0.90,
and the saved GeoTIFF passes the strict all-pixel [0,1] validator.
Anything else is a **negative** deliverable and the site must say DO NOT SUBMIT.
