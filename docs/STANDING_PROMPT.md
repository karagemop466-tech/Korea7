# STANDING REFERENCE PROMPT (verbatim, owner-supplied 2026-11-04)

> Read this at the start of every session, per the owner's instruction. Transcribed verbatim from the session 36cfbc6a brief.

Review the repo.

I want to focus on the highest scoring submissions from the following sites, GEMSDOE24, GEMSDOE25, GEMSDOE27, GEMSDOE28, GEMSDOE30, GEMSDOE31, GEMSDOE32, GEMSDOE33, GEMSDOE36. I want an executive summary on every site that is clear and obvious which is the best submission to submit to obtain a high score on the leaderboard. It should also be unique and not an exact duplicate of any previous submission that is the same as below. Keep iterating and testing until we have the highest scoring submission to download and submit.

We should be able to estimate the score for a submission. I want a table in the executive summary that clearly lists what file to download, what the estimate score is, and whether it is a unique submission unlike any of the other GEMDOE sites listed below.

THE FOLLOWING IS THE HIGHEST URGENCY AND MUST BE FOLLOWED!

MUST GENERATE A UNIQUE TIF SUBMISSION FOR THE COMPETITION. DO NOT COPY A PREVIOUS SUBMISSION UNLESS IT'S FOR LEARNING AND EDUCATION. BUT WE MUST GENERATE A UNIQUE TIF SUBMISSION. IT MUST BE OBVIOUS WHETHER IT IS OK TO DOWNLOAD AND SUBMIT THE GENERATED TIF SUBMISSION.

There should be an easy to download submission tif file as described by the prompt. Read the entire prompt. A lot of sites mention inspection only and a human inspector, but the inspection needs to be done through the project and needs to be validated for submission without human intervention.

PARALLEL-RUN PROTOCOL — read first. This session is one of several running from this same prompt.

1. LANE. Your lane is the single method paragraph below. Stay inside it. If your raster's rank-correlation with any registry raster exceeds [0.90], or more than [70%] of your dots fall within 3 px of one registry raster's dots, you have drifted into another lane: log it as a duplicate and stop. Check this on the surface before placement AND on the final dots.

2. REUSE, DON'T REBUILD. Use the template's cached feature stack, evaluate_holdout.py and submission_writer.py. Holdout = hide-and-recover: withhold whole fault segments with a buffer, derive every catalogue-based feature only from the visible faults, mask visible faults pixel-exactly, score pooled DTI (alpha 0.2, beta 0.8, 300 m triangular kernel). If a shared tool is wrong, fix it once in the template and report it; never keep a private fork.

3. LABEL EVERY NUMBER as HOLDOUT-DTI (evaluator version, number of withheld positives, 95% CI) or ORGANIZER-CONFIRMED (copied from a submission-page receipt). A projection is never written as a score.

4. LEAKAGE CANARY. Test each feature alone on the holdout before trusting any result. AUC above [0.90] means leakage until proven otherwise.

5. RUN CARD. End with one JSON card: hypothesis; mechanism; the named non-fault process that could mimic it; holdout DTI + CI; correlation/overlap vs registry; raster sha256; validator output (no NaN inside the footprint, values in [0,1], CRS/shape/transform match); submission name + note of at most 140 characters; verdict promote / negative. Negative results are deliverables.

6. BUDGET. Stop after [3] experiments or [2] hours. Do not pick submissions: promotion to a real slot is a separate selector step, within the weekly cap shown on the submission page.

The following sites should serve as a starting point for understanding how to generate TIF submissions. These websites are researched, and tested and have generated TIF submissions. But we need to generate high scoring submissions.

Here are the results from submissions into the competition, separated by ....:

WE NEED TO STUDY, ANALYZE, AND UNDERSTAND THE HIGHEST SCORE FROM THE GEMDOE SITE WHERE THE SUBMISSION TIF IS DOWNLOADED FROM WHICH IS THE FOLLOWING:

https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html — h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778

Why and how did this get the highest score and are we able to generate a submission that scores higher than 0.2778?

Answer the question using Phd level experience, knowledge, and judgement. Then use the answer to generate a unique TIF submission into the competition. Must be unique submission unlike any within the GEMSDOE sites above. Verify working line by line no hallucinations.

Current competition leaderboard GEMSDOE high score: 0.4413

(The brief repeats the GEMSDOE32 study paragraph a second time, verbatim.)

## Reported results by site (separated by "...." in the original)

- GEMSDOE: gems-submission-20260925T001403Z-7f00890a: 0.1563
- 6GEMSDOE: gems6_hgb88-topk03_33cec71ff0: 0.0286
- GEMSDOE3: pindrop-v4-nodes-20260925T152420Z-f347b70daa: 0.1193 · pindrop-v4-discovery-20260925T152423Z-37f9d5b855: 0.0830 · pindrop-v4-ridge-20260925T152422Z-4e03fc9705: 0.1152
- GEMSDOE2: gemsdoe2-dual-family-union-20260925T160406Z-f68e590f: 0.1560
- GEMSDOE4: gems-submission-20260926T163915Z-237f0063: 0.0343
- 5GEMSDOE: gems-submission-20260926T175114Z-7f00890a: 0.1563
- 7GEMSDOE: lidarscarp-ridge-top2pct-36c3a3f341c8: 0.1461
- 8GEMSDOE: Hedge-v2_submission: 0.1563
- GEMSDOE9: 2314b599: 0.0107
- 11GEMSDOE: gems-structural-area06-v1: 0.0202
- 12GEMSDOE: r7-nms3-dem10-scarp_0c9199f14e62: 0.1294 · r7-nms3-dem10-scarp_0c9199f14e62_allfinite: 0.1294
- 15GEMSDOE: gems-tso1-20260929T005627Z-conj_alteration_mag: 0.0782
- 14GEMSDOE: GEMS_r5-geom-horse-ensemble_20260929T154852Z_ccbe1de0_site_e96e942f: 0.0020
- 17GEMSDOE: 17GEMSDOE_F-ensemble-2pct_20260930T050626Z: 0.0187
- 18GEMSDOE: H19-C_20260930T212401Z_c11e495e: 0.0297
- 19GEMSDOE: h19-4-multiline-corroborated-openness-thermal-pop-20260930-691e4dfa-nan: 0.1894 · h19-5-powerlaw-budget-multiline-corroborated-20260930-e27054cf-nan: 0.1922
- GEMSDOE10: h16-continuation: 0.0461 · h20-dem10-scarp-thin: 0.0921 · H25-ctx-ridge: 0.1280 · h28-dotted-ridge: 0.1839
- 13GEMSDOE: 20261001_r13-lattice-s5_v2_nan-outside: 0.0904
- 16GEMSDOE: h16-1-topo-geophys-baseline-ridges: 0.1855 · h18-3a-topo-geophys-x-complexity-prior: 0.0976 · h18-4-usgs-geologic-map-faults-gap: 0.0360
- GEMSDOE21: h19-4-reference-20260930-691e4dfa: 0.1894
- 20GEMSDOE: h20-1-sarnnpu-powerlaw-pi0363-tilt-wingcrack: 0.1890 · h20-5-continuous-pu-proxy-unverified: 0.1859
- GEMSDOE22: h23-a-dti-optimal-emission-6pct: 0.1002 · h23-b-dti-optimal-emission-10pct: 0.0748
- GEMSDOE23: h30-arrangement-matched-habitat: 0.1352
- GEMSDOE24: h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan: 0.2477 · gems24-gvc1-negative-geothermal-lineament-submod: 0.0859
- GEMSDOE25: dotted-h19-5-d2-8-20261002-e56ea318af89-nan: 0.2600 · gems25-h66-mgd-flank-sapd3-0-k3p5: 0.0742
- GEMSDOE26: dilcond-oof-v1: 0.1223
- GEMSDOE27: topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan: 0.2449 · gems27-h29-hydrothermal-piedmont-celf: 0.2190 · gems27-h31-drcg-wl-celf28: 0.2250
- GEMSDOE28: h27-4-r1-solo-d2-8: 0.2708 · h32-1-prethin-tip-euler-d2-8: 0.2649 · h36-1-rung30-blind-r1: 0.2710 · h38-1-hf-euler-r30-r1: 0.2707 · gems28-s18-mxtp: 0.0217 · gems28-s21-puhgb: 0.0206
- GEMSDOE29: efd28-repro: 0.2600 · repo-c0-habitat-emission: 0.0041 · sgmc-off-catalogue-44k: 0.0512 · wormrank-d28: 0.2560 · wormsurv-filter: 0.0532 · xfit-c0-habitat: 0.0439 · xfit-h41-union-qfaults: 0.0356
- GEMSDOE30: d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca: 0.2600 · gems30-MSDB1-edge44090: 0.1462
- GEMSDOE31: h27-4-solo-d28-20261004-8acb75e1-nan: 0.2708
- GEMSDOE32: h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778
- GEMSDOE33: h33d-analog-tip-stepover-r30-20261004-cb490425926e: 0.2632 · gemsdoe33-s33-seisdil-strain-seismicity: 0.0963
- GEMSDOE34: h34-scatter-q50-arr-matched: 0.0778
- GEMSDOE35: h35-06-aaa86efb25-candidate: 0.0418
- GEMSDOE36: anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros: 0.2750 · gemsdoe36-kpl36-exp3: 0.1647
- GEMSDOE37: h6-physics-dotted-80k: 0.1193
- GEMSDOE38: D-step-3p0-07pct-tipProt: 0.0763
- GEMSDOE42: xscale-worm-persistence: 0.0581
- GEMSDOE43: sup01-hgb21-sep40-n40000: 0.0424
- GEMSDOE45: h51-km-faultzone: 0.0106
- GEMSDOE49: gate_ortho_w0.25-40k: 0.2376
- GEMSDOE46: r11f-scarp-radiometric-fusion: 0.1589 · r12-scarp-rad-concordance: 0.0843
- GEMSDOE39: h40-e-disc-h40e-30k-zeros: 0.0339
- GEMSDOE40: h8-euler-lineament-depthcluster: 0.0355 / -hard: 0.0397 · h45-eulerdepthreadcluster: 0.0984
- GEMSDOE41: h42-submission-primary: 0.0245
- GEMSDOE44: h46-twostageAB: 0.0715
- GEMSDOE47: h60-lidarscarp-s2p0: 0.0430
- GEMSDOE48: h59-cover-ds-belief-b2xh33d: 0.2296
- GEMSDOE50: h59-sharpened-scarp-scatter-90k: 0.0764
- GEMSDOE51: h53-twostage: 0.1047
- GEMSDOE52: h97b-candidate: 0.0856
- GEMSDOE53: h8-tiprelay-ridgeconcord-pr2-n80000: 0.0159
- GEMSDOE54: h54c-manifest-edge: 0.0449
- 55GEMSDOE: tensor_full-n16000-sep3: 0.0290
- 56GEMSDOE: h56-final-dotted-ridge-d2p8: 0.0658
- 57GEMSDOE: h57r-joint-strata-38000: 0.0254
- 58GEMSDOE: ml-binary-ridge: 0.0180
- 59GEMSDOE: h59j-coherence-consensus-dotted: 0.0499
- 60GEMSDOE: h73-chi-coherent-corridor-12000: 0.0351
- 61GEMSDOE: h61a-basement-step-20000dots: 0.0009 · h61o-vardepth-none-40000dots: 0.0751
- 62GEMSDOE: datum-lahontan-strain-gauge-defensible-440dots-zeros: 0.0000
- GEMSDOE63: cvarlw-thin-s3p17-54864: 0.2303
- GEMSDOE64: h64-lidar-scarp-cv: 0.0383
- GEMSDOE65: sar-em-propensity-half: 0.0431
- GEMSDOE66: gems66-lidar03-cvretrain-reliefdecile-37654dots: 0.1152
- GEMSDOE67: h67a-orientip-lane-29447dots: 0.0356 · ovtr-ml-cover-tau3p0: 0.1426
- GEMSDOE68: gems68-autoctx-s3-strands-35000dots (nan & zeros): 0.0437
- GEMSDOE69: h69-joint-relayramp-pullapart-38669: 0.0053
- GEMSDOE70: gems70-p5-dual-submod300-oof38k: 0.2478
- GEMSDOE71: gems71-hydro-conduit-38800: 0.0558
- GEMSDOE72: gemsdoe72-h72-1-sgmc-offcatalogue: 0.0492
- GEMSDOE73: gems73-h73-mcsc-seamfree-blakely-37654dots: 0.1917
- GEMSDOE74: gemsdoe74-triregime-radon-piedmont-37654: 0.0669
- GEMSDOE75: gems75-trlt-radon-loco-ridge: 0.1627
- GEMSDOE76: gems76_h76_3_geotherm_tilt_axial_submod: 0.1555 · gems76-ptcf-tiltworm-submod39k: 0.2343
- GEMSDOE77: gems85-h85-edti-collar35-skel-r33: 0.0964
- GEMSDOE78: gems78-h78sigx-fuse-b5-44090dots: 0.1564
- GEMSDOE79: gems79-tilt-ring-100000dots: 0.0005
- GEMSDOE80: gemsdoe80-h80g-choquet-tworegime: 0.0943
- GEMSDOE81: gems81-cont-poisson44090-buf2: 0.0041
- GEMSDOE82: gemsdoe82-h82-submodular-punoisyor: 0.1886
- GEMSDOE83: gems83-h83-gvcd-dink300-37654dots: 0.0573
- GEMSDOE84: gems84-h84-kthm-tworegime-58000px: 0.0132
- GEMSDOE85: gemsdoe85-hjcd-ventbridge-submod-zeros: 0.1110
- GEMSDOE86 / GEMSDOE88: (no results listed)
- GEMSDOE87: h87-h87-cmgep: 0.0500
- GEMSDOE89: gemsdoe89-bh-rtp-habc: 0.0301
- GEMSDOE90: gems90-cnc-35000dots: 0.0749
- GEMSDOE91: cwpc-e3: 0.1367 · lftg: 0.1823 · S18-UNIQUE-curvtilt: 0.0435 · s22-omtj-e1: 0.0298 · s91-alm-alteration-halo / s28-vsd-e3: (unscored)
- GEMSDOE92: listricdip-updip50: 0.0255 · lbmc1-35801dots: (unscored)
- KANLERGEMSDOE3: cadg-submod-exp-k3-3-oof8f-37654: (unscored)
- KANLERGEMSDOE2: kanlergems2-htcads-exp-2-37654dots: 0.1218
- WBGGEMSDOE3: wbg3-h3pack-34k: 0.0443 · skarpline-union: 0.0443 · invdesign-anchor-20k: 0.1362
- WBGGEMSDOE2: wbg2-offcatalogue-density-36k: 0.0262 · wbg4-triphysics-ridge-38k: (unscored)
- WBGGEMSDOE1: wbg6-qmh-kdisjoint-30000: 0.0576
- GEMSDOEkarage3: h-k3c-csst-bghf-24cell-d31-b37654: 0.1978
- GEMSDOEkarage2: hk3-edgecentrality-apron3: 0.1591 · halo39-b44090-sep2: (unscored)
- GEMSDOEkarage1: hmas-sinter-dualcover-sep29 / kp1-ttca-springalter-far-conduit-32000: (unscored)
- ApartGEMSDOE3: cfkc-dhc-37654: (unscored) · h2-cshd-dual97-axial362-37654: 0.1633
- ApartGEMSDOE1: udth-submod-e3: 0.0525 · maw-gsi-e3: (unscored)
- GEMSDOESASS3: lwst-geoconduit-dual37654: 0.1339 · lbinv-84262: (unscored)
- GEMSDOESASS2: xghf-dualhorizon-aniso-b2-37654: (unscored) · hvfd-exp3-hydrocollinear-37654: 0.1881 · sparse-blind-conduit-22163: 0.0056 · strainridge-offcat-37654d: (unscored)
- GEMSDOESASS1: swgb-hrv2-44090dots: 0.0558 · hvtgb-thermal-anchored-37654-b6: (unscored)
- wbg-corridor-band3to12-s24-sep4 / wbg8-mridge-pois300-offcat3-37654 / wbg5-sgmc-topo-poisson150k: (unscored)
- EUGGEMSDOE1/2/3, GINNYGEMSDOE1/2/3, ApartGEMSDOE2, KANLERGEMSDOE1: (no results listed)

I think it makes sense that in order for a submission to be validated that it needs to pass certain high scoring validation gates before confirming whether a file is unique and can be submitted for scoring.

The following is the leaderboard for the competition: https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/

See below for more links and information related to the competition: https://github.com/drivendataorg/gems-prize-reference-solution · https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and · https://gbcge.org/current-projects/ingenious/ · https://epsg.io/32611 · https://en.wikipedia.org/wiki/Tversky_index

We need to quickly look at the results and results from the GEMSDOE websites above.

Before implementing, generate 3–5 candidate geological hypotheses we haven't tried yet, each naming: the specific layer(s) involved, the physical signature being targeted (e.g., an edge-detection or curvature transform), why it should catch a fault missing from the USGS/INGENIOUS catalogue rather than one already in it, and how it differs from anything already implemented in this repo. Rank them by expected DTI improvement and implementation cost. Validate the top candidate on our spatially-blocked holdout set before touching a weekly submission slot — do not spend a submission slot on an idea that hasn't beaten the current holdout best. If a candidate can't be validated without new external data, name the specific free, official source needed and check it's obtainable before proposing the idea as viable.

Work line by line verifying from official verified trusted sources, provide links for manual review. There should be no manual input, work on your own to complete tasks. Flag any irregularities for review. No hallucinations. Verify no hallucinations.

The goal of this project is to get a full list that follow our requirements. No hallucinations. Verify line by line.

We have a good understanding of how our hypothesis, methodology, calculations, analysis are done so we should be able to figure out a way to score higher on the leaderboard using previous results and scoring that we have across the sites listed above. We need to come up with distinct and unique strategies to score higher in this competition leaderboard. We need to start doing heavy and deep research into the part of the project that matters the most, which is the scientific discovery of geothermal vents. We should store all of our information and knowledge that we can gather from official verified sources. This will serve as a starting point for other projects as well. We need to think outside the box but still be grounded in proper scientific research, we are ultimately aiming for a top prize that many others are competing for. So it's important to be contrarian but be smart about it. We need to find sources of data that others are over looking or areas of the project when it comes to geothermal vents. We need to do deep research and critical thinking and come up with new hypothesis to test.

0.3195 is the highest score right now so we need to design a new strategy, research, testing, analyzing, and generating submission system than the current website. It should be unique, take unique approaches to generating a submission that can score higher than 0.3195.

Put this prompt into the repo readme and read it everytime we work on the project as a starting point to make sure we are building what we are aiming for and have a strong base to continue building and improving on making something useful for everyday use. It should solve the problem of having to manually check everything ourselves and having an up to date current feed.

Review the repo.

The following is taken from the Arena AI team and I think it makes a good point on building a successful project, so let's keep the Core Values and Own the Outcome as a focal point when building, developing, researching, suggesting upgrades, and implementing the work.

Our Core Values — Maximize P(Win): "Maximize the Probability of Winning": our decision making framework. In every decision, we weigh tradeoffs, assess risk, and choose the path that maximizes the probability that Arena succeeds. We set aside our emotions and make tough decisions in order to maximize P(Win). "Maximize P(Win)" frees us from constraints and clarifies that we must put Arena first.

Own the Outcome: We own results end to end — not just our individual slice of the work. When problems arise and we have the means to act, we do so without waiting for permission or assignment. We treat failure and success as signals and use them to improve. At Arena, we stay accountable to the final outcome.

Work line by line verifying from official verified trusted sources, provide links for manual review. There should be no manual input, work on your own to complete tasks. Flag any irregularities for review. No hallucinations. Verify no hallucinations. The goal of this project is to get a full list that follow our requirements. No hallucinations. Verify line by line.

We need to focus on being able to generate a submission into the competition.

The site should be able to generate a TIF file that is required for submission. It should be as easy as download to click a File to submit into the competition. This needs to be in the executive summary or the very beginning of the site. it should be obvious when you visit the site.

I tried to submit the document that i downloaded from the site but it returned this error on the submission form: "Predicted values must be in range [0, 1]"

Also we need to give it a unique name and A short comment to help you or your team tell submissions apart later e.g. clustering with k=25

Here is the submission page when i click submit file — New submission — File to submit: No file chosen — You can submit a single-band GeoTIFF (.tif) file, or a .zip file containing a single GeoTIFF, with your predictions. It must match the submission format's CRS, shape, and geotransform. You may wish to review the competition rules first. Note (optional): A short comment to help you or your team tell submissions apart later e.g. clustering with k=25

Create a executive summary subpage that explains exactly how to make a submission into the contest.

Work on the next steps from the previous sessions first.

The goal of this project is to place top of the leaderboard in this competition. The following is the competition: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/

We need to create a project that can compete and place top of the leaderboard. We need to understand the problem, collect all the data and organize it into a clean easily auditable table with official verified links for manual verification.

This is the guidelines we need to follow: https://www.drivendata.org/competitions/306/competition-doe-gems/ — Get familiar with the problem through the overview and problem description (https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/). You might also want to reference additional resources available on the about page (https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/). Download the data from the data tab (https://www.drivendata.org/competitions/306/competition-doe-gems/data/). Create and train your own model. This reference solution (https://github.com/drivendataorg/gems-prize-reference-solution) implements a simple approach. Use your model to generate predictions that match the submission format.

Tell me what are you limitations and what you need access to during this project. We will need to find free publicly available sources and data from official and verified sources if we are to use 3rd party or external data.

this pdf outlines how submissions must be entered into the competition: https://docs.nlr.gov/docs/fy26osti/96647.pdf

You must be able to do your own research, deep research, scientific literature research and organize the knowledge so that we can critically think through the problem and generate a solution through scientific and free publicly available information. this must be done autonomously and must be constantly reviewed and improved upon. Provide suggestions and improvements and implement them.

❌ No DrivenData auth → cannot auto-download training_features.tif, labels.tif, sample_submission.tif, 1m_DEM_links.csv from https://www.drivendata.org/competitions/306/competition-doe-gems/data/ (verified redirect to login). See below for links from the above site. See attached files for links from the above site. https://gdr.openei.org/submissions/1391

Download competition data from https://www.drivendata.org/competitions/306/competition-doe-gems/data/ (requires login) to data/. See links below for competition data (Dropbox mirrors): GEMS_96647.pdf · example_submission.tif · existing_faults.tif · gems-geodawn-numerical-features.tif · Digital-elevation-model-links-JSON.pdf

Work line by line verifying from official verified trusted sources, provide links for manual review. There should be no manual input, work on your own to complete tasks. Flag any irregularities for review. No hallucinations. Verify no hallucinations. The goal of this project is to get a full list that follow our requirements. No hallucinations. Verify line by line.

Site creation: Create a github page for this repo that has clean ui, user friendly, simple and easy to use. It should be organized and clean. It should include all relevant information in an easy to read format with official verified links as sources for review. Work line by line verify everything no hallucinations.

**The single remaining blocker to training is data placement**: run `bash scripts/download_competition_data.sh` on any unrestricted machine into `data/`, then `python scripts/prepare_data.py` — after that the full train→inference→validate pipeline is ready to run (GPU needed for training; metric/losses/validation all verified working here on CPU).

you need to complete the above task by yourself. Work line by line verifying from official verified trusted sources, provide links for manual review. There should be no manual input, work on your own to complete tasks. Flag any irregularities for review. No hallucinations. Verify no hallucinations. The goal of this project is to get a full list that follow our requirements. No hallucinations. Verify line by line.

Run this task through multiple passes. Pass 1: Implement the task completely and verify the result. Pass 2: Review your work for bugs, missing requirements, incorrect assumptions, and edge cases. Fix everything you find. Pass 3: Re-check the entire implementation against the original request. Improve accuracy, reliability, completeness, and code quality. Fix any remaining issues. Do not stop after the first pass. Each pass must build on the previous one. Before finishing, verify that the final result fully satisfies the original request. Work line by line verify everything no hallucinations.

Go ahead and create a pull request and then merge the pull request onto the main. Make suggestions for what work still needs to be done and any limitations that is in the way of a successful project. It should be worked on in this next session or the next session. Work line by line verify everything no hallucinations.
