# Korea7 — Novel geological hypotheses for the GEMS Prize (DrivenData #306)

Parallel-run protocol rule 5: propose and rank 3–5 novel geological hypotheses, each naming
(a) the specific layer(s) involved, (b) the physical signature targeted, (c) why it should catch
a fault MISSING from the USGS/INGENIOUS catalogue rather than one already in it, and (d) how it
differs from anything already implemented in this repo (this repo starts empty; all GEMSDOE site
artifacts are catalogue-derived surface dots/scarps/ridges).

All five target free, official, publicly obtainable data — no login-gated competition data is
required to generate the candidate raster; holdout DTI validation still requires the login-gated
training_features.tif / existing_faults.tif / labels.tif / sample_submission.tif.

Ranking key: DTI = expected distance-weighted Tversky improvement vs the GEMSDOE32 baseline
(claimed 0.2778); Cost = implementation effort (1=low, 5=high).

| Rank | Hypothesis | Layers involved | Physical signature targeted | Why it catches catalogue-missing faults | Differs from repo / GEMSDOE sites | Est. DTI | Cost | Free official source (obtainable?) |
|---|---|---|---|---|---|---|---|---|
| 1 | Deep-crustal conductivity-edge | Crustal magnetotelluric (MT) resistivity/depth-band conductivity (USGS ScienceBase, DOI 10.5066/P9TWT2LU) | Gradient / edge of high-conductivity (geothermal fluid) zones | Blind faults act as deep fluid conduits but leave no surface trace; the conductivity edge marks the subsurface fault zone absent from surface catalogues | GEMSDOE sites used surface faults/scarps/ridges only. No repo code computes MT edges. | High | 3 | Yes — USGS ScienceBase public GeoTIFFs |
| 2 | Hydrothermal alteration radiometric halo | Radiometric (eTh, eK, eU, total count) + aeromagnetics (USGS GeoDAWN release) | Edge/halo of potassium-thorium alteration and magnetic lows around concealed faults | Alteration halos envelop blind/hidden faults not mapped at the surface; the halo extends beyond catalogue traces | GEMSDOE used topography/scarp/lineaments, not radiometric alteration chemistry. No repo code uses radiometrics. | High | 3 | Yes — USGS GeoDAWN public |
| 3 | Sub-scarp LiDAR curvature & relief | 3DEP / GeoDAWN LiDAR DEM (1 m–5 m) | Profile & plan curvature + relative relief highlighting micro-scarps below catalogue mapping threshold | Catalogue faults are the ones mappers saw; subtle active scarps below the mapping threshold are missing, yet still conduct geothermal fluids | GEMSDOE "lidarscarp" used coarse ridge/top-n; no fine-scale curvature/relief transform in repo. | Medium | 2 | Yes — 3DEP LiDAR public |
| 4 | Spring/well 2 m probe temperature anomaly | DOE GDR INGENIOUS well/spring temperatures (gdr.openei.org/submissions/1391) | Localized warm anomalies (hydrothermal upflow points) | Blind faults focus warm water to the surface at points with no mapped surface fault; point temperatures reveal the concealed conduit | GEMSDOE used areal structural dots, not point temperature observations. No repo code ingests GDR well temps. | Medium | 2 | Yes — GDR public submission 1391 |
| 5 | Aeromagnetic lineament-intersection (relay-ramp) density | Aeromagnetics (USGS GeoDAWN) | Density of intersecting magnetic lineaments = relay ramps / stepovers | Relay ramps and stepovers connect mapped segments but are rarely catalogued as faults themselves; they are prime off-catalogue geothermal conduits | GEMSDOE32 used dots near catalogue traces; this targets intersections of lineaments (relay geometry), a different structure. No repo code computes lineament-intersection density. | Medium | 3 | Yes — USGS GeoDAWN public |

Recommended first experiment: Hypothesis 1 (MT conductivity edge) — highest expected DTI, free public data,
single well-defined transform (edge detection), and clearly distinct from every GEMSDOE artifact.
Holdout DTI must be measured on the spatially blocked holdout before any submission slot is used; the
competition data tab is login-gated in this environment, so that measurement is blocked pending data access.
