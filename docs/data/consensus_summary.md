# Korea7 consensus run card

**File:** `docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif`  
**SHA-256:** `9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c`  
**Dots:** 20000.0  
**Geometry:** far >15 px = 0.857; near <=2 px = 0.000; median distance = 34.1 px  
**PROJECTED leaderboard value:** 0.3382 (95% bootstrap 0.3277–0.3525) — **not a score**  
**HOLDOUT-DTI:** 0.0000 (95% CI 0.0000–0.0000); random control 0.0320  
**Unique vs nine focus:** 0% forward 3-px overlap by construction; max |surface Spearman| = 0.0068  
**13GEMS lattice forward 3-px overlap:** 0.9996 (literal rule fails; covering-grid probe)  
**Validator:** PASS  
**Verdict:** NEGATIVE — research artifact, NOT CLEARED for a weekly slot.

## Why the projection and holdout disagree

The holdout truth is the mapped catalogue; the candidate is off-catalogue by design, so it cannot recover withheld catalogue segments. The organizer masks known faults, so the holdout is a conservative proxy for catalogue recovery, not a direct estimate of the hidden new-fault score. The projection is an OLS extrapolation from nine USER-REPORTED scores and cannot see surface quality. Neither number is an organizer score.

## Run card JSON

```json
{
  "schema": "korea7-consensus-run-card-v1",
  "date_utc": "2026-11-04T20:25:38Z",
  "session": "arena/e868a66c-korea7",
  "lane": "density-weighted multi-method off-catalogue consensus (new lane; not an exact copy of any prior submission)",
  "hypothesis": "Blind geothermal faults missing from the USGS/INGENIOUS catalogue are co-detected by independent off-catalogue geophysical, geothermal-conduit, habitat-suitability and corridor-prior methods; a density-weighted consensus of their local support concentrates the highest-confidence off-catalogue structures while avoiding the mapped catalogue and the nine focus-site halos.",
  "mechanism": "Each of four reference rasters is converted to a 3-px local-density surface; the densities are weighted by each method's measured far-catalogue fraction and summed. The surface is masked to >5 px from the catalogue and outside the closed 3-px halo of every focus-site raster, then the top 20,000 cells are selected by greedy 3-px NMS. The candidate is written with the shared gems57.submission_writer and validated on disk.",
  "named_non_fault_mimic": "Pluvial shoreline berms, road/rail embankments, conductive playas, alluvial-fan toes and basin-margin gravity steps can produce linear conductivity/curvature/gravity anomalies in novel territory; the consensus requires agreement across independent methods, but does not prove a fault.",
  "holdout": {
    "evidence_class": "HOLDOUT-DTI",
    "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
    "pooled_dti": 0.0,
    "pooled_coverage": 0.0,
    "ci95": [
      0.0,
      0.0
    ],
    "withheld_positive_pixels": 45260,
    "n_cells": 16,
    "folds": {
      "draw20_foldNW_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 7687.0,
        "fn": 1925.0,
        "n_truth": 1925.0,
        "n_emitted": 7687.0
      },
      "draw20_foldNW_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 7687.0,
        "fn": 1919.0,
        "n_truth": 1919.0,
        "n_emitted": 7687.0
      },
      "draw20_foldNE_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 2526.0,
        "fn": 2360.0,
        "n_truth": 2360.0,
        "n_emitted": 2526.0
      },
      "draw20_foldNE_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 2526.0,
        "fn": 2361.0,
        "n_truth": 2361.0,
        "n_emitted": 2526.0
      },
      "draw20_foldSW_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 5546.0,
        "fn": 3780.0,
        "n_truth": 3780.0,
        "n_emitted": 5546.0
      },
      "draw20_foldSW_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 5546.0,
        "fn": 3778.0,
        "n_truth": 3778.0,
        "n_emitted": 5546.0
      },
      "draw20_foldSE_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 3265.0,
        "fn": 3253.0,
        "n_truth": 3253.0,
        "n_emitted": 3265.0
      },
      "draw20_foldSE_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 3265.0,
        "fn": 3249.0,
        "n_truth": 3249.0,
        "n_emitted": 3265.0
      },
      "draw21_foldNW_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 7687.0,
        "fn": 1919.0,
        "n_truth": 1919.0,
        "n_emitted": 7687.0
      },
      "draw21_foldNW_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 7687.0,
        "fn": 1924.0,
        "n_truth": 1924.0,
        "n_emitted": 7687.0
      },
      "draw21_foldNE_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 2526.0,
        "fn": 2365.0,
        "n_truth": 2365.0,
        "n_emitted": 2526.0
      },
      "draw21_foldNE_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 2526.0,
        "fn": 2358.0,
        "n_truth": 2358.0,
        "n_emitted": 2526.0
      },
      "draw21_foldSW_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 5546.0,
        "fn": 3786.0,
        "n_truth": 3786.0,
        "n_emitted": 5546.0
      },
      "draw21_foldSW_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 5546.0,
        "fn": 3781.0,
        "n_truth": 3781.0,
        "n_emitted": 5546.0
      },
      "draw21_foldSE_all": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 3265.0,
        "fn": 3253.0,
        "n_truth": 3253.0,
        "n_emitted": 3265.0
      },
      "draw21_foldSE_detached": {
        "dti": 0.0,
        "coverage": 0.0,
        "tp": 0.0,
        "fp": 3265.0,
        "fn": 3249.0,
        "n_truth": 3249.0,
        "n_emitted": 3265.0
      }
    }
  },
  "random_control_holdout": {
    "evidence_class": "HOLDOUT-DTI",
    "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
    "pooled_dti": 0.03195774890885529,
    "pooled_coverage": 0.03629625355722053,
    "ci95": [
      0.029612533040742177,
      0.034560317447077896
    ],
    "withheld_positive_pixels": 45260,
    "n_cells": 16,
    "folds": {
      "draw20_foldNW_all": {
        "dti": 0.03869823872195799,
        "coverage": 0.04825932366544738,
        "tp": 92.8991980559862,
        "fp": 4210.12744140625,
        "fn": 1832.1008019440137,
        "n_truth": 1925.0,
        "n_emitted": 4251.0
      },
      "draw20_foldNW_detached": {
        "dti": 0.034175237533199086,
        "coverage": 0.04264978084157545,
        "tp": 81.8449294349833,
        "fp": 4216.4580078125,
        "fn": 1837.1550705650168,
        "n_truth": 1919.0,
        "n_emitted": 4253.0
      },
      "draw20_foldNE_all": {
        "dti": 0.024925003875740606,
        "coverage": 0.030929023588760825,
        "tp": 72.99249566947555,
        "fp": 5129.431640625,
        "fn": 2287.0075043305246,
        "n_truth": 2360.0,
        "n_emitted": 5160.0
      },
      "draw20_foldNE_detached": {
        "dti": 0.025163110231490895,
        "coverage": 0.031214643737882564,
        "tp": 73.69777386514073,
        "fp": 5126.3134765625,
        "fn": 2287.302226134859,
        "n_truth": 2361.0,
        "n_emitted": 5158.0
      },
      "draw20_foldSW_all": {
        "dti": 0.02808318451385806,
        "coverage": 0.030289518372301438,
        "tp": 114.49437944729944,
        "fp": 5150.36962890625,
        "fn": 3665.5056205527007,
        "n_truth": 3780.0,
        "n_emitted": 5201.0
      },
      "draw20_foldSW_detached": {
        "dti": 0.029280636530249923,
        "coverage": 0.03159516446311956,
        "tp": 119.36653134166569,
        "fp": 5151.8193359375,
        "fn": 3658.633468658334,
        "n_truth": 3778.0,
        "n_emitted": 5202.0
      },
      "draw20_foldSE_all": {
        "dti": 0.03267701416508892,
        "coverage": 0.034603678029297466,
        "tp": 112.56576462930465,
        "fp": 4099.43212890625,
        "fn": 3140.434235370695,
        "n_truth": 3253.0,
        "n_emitted": 4151.0
      },
      "draw20_foldSE_detached": {
        "dti": 0.03544168025636149,
        "coverage": 0.03756739815768068,
        "tp": 122.05647661430453,
        "fp": 4101.28466796875,
        "fn": 3126.9435233856957,
        "n_truth": 3249.0,
        "n_emitted": 4153.0
      },
      "draw21_foldNW_all": {
        "dti": 0.029006117973488774,
        "coverage": 0.03616740477480495,
        "tp": 69.4052497628507,
        "fp": 4218.4931640625,
        "fn": 1849.5947502371494,
        "n_truth": 1919.0,
        "n_emitted": 4248.0
      },
      "draw21_foldNW_detached": {
        "dti": 0.03504256270103209,
        "coverage": 0.043682590863555346,
        "tp": 84.04530482148049,
        "fp": 4211.84375,
        "fn": 1839.9546951785196,
        "n_truth": 1924.0,
        "n_emitted": 4249.0
      },
      "draw21_foldNE_all": {
        "dti": 0.028187977658418347,
        "coverage": 0.03495592033507577,
        "tp": 82.6707515924542,
        "fp": 5121.515625,
        "fn": 2282.329248407546,
        "n_truth": 2365.0,
        "n_emitted": 5157.0
      },
      "draw21_foldNE_detached": {
        "dti": 0.02692191273149145,
        "coverage": 0.03341556281684312,
        "tp": 78.79389712211606,
        "fp": 5122.9912109375,
        "fn": 2279.206102877884,
        "n_truth": 2358.0,
        "n_emitted": 5158.0
      },
      "draw21_foldSW_all": {
        "dti": 0.03132672666189227,
        "coverage": 0.0337837444818248,
        "tp": 127.9052566081887,
        "fp": 5142.8125,
        "fn": 3658.0947433918113,
        "n_truth": 3786.0,
        "n_emitted": 5198.0
      },
      "draw21_foldSW_detached": {
        "dti": 0.03084646366244737,
        "coverage": 0.033278538275135314,
        "tp": 125.82615321828662,
        "fp": 5145.7294921875,
        "fn": 3655.1738467817136,
        "n_truth": 3781.0,
        "n_emitted": 5199.0
      },
      "draw21_foldSE_all": {
        "dti": 0.039542283439141554,
        "coverage": 0.04192155439721784,
        "tp": 136.37081645414963,
        "fp": 4095.299072265625,
        "fn": 3116.6291835458505,
        "n_truth": 3253.0,
        "n_emitted": 4155.0
      },
      "draw21_foldSE_detached": {
        "dti": 0.04287744556639141,
        "coverage": 0.04550121802465826,
        "tp": 147.83345736211467,
        "fp": 4095.236572265625,
        "fn": 3101.1665426378854,
        "n_truth": 3249.0,
        "n_emitted": 4159.0
      }
    }
  },
  "focus_holdout": {
    "GEMSDOE24": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.09750418428986357,
      "pooled_coverage": 0.17608877861568148,
      "ci95": [
        0.08696517873964764,
        0.10772321122291265
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.08437883373624601,
          "coverage": 0.18364348613009956,
          "tp": 353.5137108004417,
          "fp": 12894.4951171875,
          "fn": 1571.4862891995583,
          "n_truth": 1925.0,
          "n_emitted": 13112.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.09108579071219135,
          "coverage": 0.19870451628702704,
          "tp": 381.3139667548049,
          "fp": 12874.26953125,
          "fn": 1537.6860332451952,
          "n_truth": 1919.0,
          "n_emitted": 13112.0
        },
        "draw20_foldNE_all": {
          "dti": 0.11422960957191232,
          "coverage": 0.24351130099139737,
          "tp": 574.6866703396978,
          "fp": 15140.2041015625,
          "fn": 1785.3133296603023,
          "n_truth": 2360.0,
          "n_emitted": 15489.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.10419061642673015,
          "coverage": 0.2218589018036254,
          "tp": 523.8088671583596,
          "fp": 15169.2373046875,
          "fn": 1837.1911328416404,
          "n_truth": 2361.0,
          "n_emitted": 15489.0
        },
        "draw20_foldSW_all": {
          "dti": 0.07529596019046828,
          "coverage": 0.12308173478707457,
          "tp": 465.2489574951419,
          "fp": 15309.43359375,
          "fn": 3314.751042504858,
          "n_truth": 3780.0,
          "n_emitted": 15584.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.07147406997224873,
          "coverage": 0.11680868785514177,
          "tp": 441.3032227167256,
          "fp": 15318.2578125,
          "fn": 3336.6967772832745,
          "n_truth": 3778.0,
          "n_emitted": 15584.0
        },
        "draw20_foldSE_all": {
          "dti": 0.12404620034264012,
          "coverage": 0.19217431574219027,
          "tp": 625.1430491093449,
          "fp": 11560.849609375,
          "fn": 2627.856950890655,
          "n_truth": 3253.0,
          "n_emitted": 11944.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.13097595573085072,
          "coverage": 0.20318085443761782,
          "tp": 660.1345960678203,
          "fp": 11544.4677734375,
          "fn": 2588.8654039321796,
          "n_truth": 3249.0,
          "n_emitted": 11944.0
        },
        "draw21_foldNW_all": {
          "dti": 0.08994611857187458,
          "coverage": 0.19629760088216247,
          "tp": 376.6950960928698,
          "fp": 12887.3466796875,
          "fn": 1542.3049039071302,
          "n_truth": 1919.0,
          "n_emitted": 13112.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.0786280689744093,
          "coverage": 0.17109942813174897,
          "tp": 329.19529972548503,
          "fp": 12908.505859375,
          "fn": 1594.804700274515,
          "n_truth": 1924.0,
          "n_emitted": 13112.0
        },
        "draw21_foldNE_all": {
          "dti": 0.10274127580983666,
          "coverage": 0.21848438458556882,
          "tp": 516.7155695448703,
          "fp": 15169.7294921875,
          "fn": 1848.2844304551297,
          "n_truth": 2365.0,
          "n_emitted": 15489.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.11334159157954475,
          "coverage": 0.2416910497409932,
          "tp": 569.907495289262,
          "fp": 15139.23828125,
          "fn": 1788.092504710738,
          "n_truth": 2358.0,
          "n_emitted": 15489.0
        },
        "draw21_foldSW_all": {
          "dti": 0.07075554392821778,
          "coverage": 0.11551187643716718,
          "tp": 437.3279641911149,
          "fp": 15322.8203125,
          "fn": 3348.672035808885,
          "n_truth": 3786.0,
          "n_emitted": 15584.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.07600501155213892,
          "coverage": 0.12418510795473396,
          "tp": 469.5438931768491,
          "fp": 15295.46484375,
          "fn": 3311.456106823151,
          "n_truth": 3781.0,
          "n_emitted": 15584.0
        },
        "draw21_foldSE_all": {
          "dti": 0.1191397108324257,
          "coverage": 0.1845488049341753,
          "tp": 600.3372624508722,
          "fp": 11582.337890625,
          "fn": 2652.662737549128,
          "n_truth": 3253.0,
          "n_emitted": 11944.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.12793908985219254,
          "coverage": 0.19849261287537207,
          "tp": 644.9024992320839,
          "fp": 11562.5947265625,
          "fn": 2604.0975007679162,
          "n_truth": 3249.0,
          "n_emitted": 11944.0
        }
      }
    },
    "GEMSDOE25": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.10226689004897589,
      "pooled_coverage": 0.15790587663450967,
      "ci95": [
        0.09093150254145185,
        0.11327390531714962
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.0889482474631701,
          "coverage": 0.1618330543685191,
          "tp": 311.52862965939926,
          "fp": 9500.2626953125,
          "fn": 1613.4713703406007,
          "n_truth": 1925.0,
          "n_emitted": 9655.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.10032826281191845,
          "coverage": 0.18301497659411178,
          "tp": 351.2057400841005,
          "fp": 9475.6259765625,
          "fn": 1567.7942599158996,
          "n_truth": 1919.0,
          "n_emitted": 9655.0
        },
        "draw20_foldNE_all": {
          "dti": 0.12281886118868907,
          "coverage": 0.21823203880903488,
          "tp": 515.0276115893223,
          "fp": 11011.931640625,
          "fn": 1844.9723884106777,
          "n_truth": 2360.0,
          "n_emitted": 11261.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.11167923029964794,
          "coverage": 0.19810985814661916,
          "tp": 467.73737508416787,
          "fp": 11029.37109375,
          "fn": 1893.262624915832,
          "n_truth": 2361.0,
          "n_emitted": 11261.0
        },
        "draw20_foldSW_all": {
          "dti": 0.07689800003328057,
          "coverage": 0.10919982853780076,
          "tp": 412.77535187288686,
          "fp": 11306.3720703125,
          "fn": 3367.224648127113,
          "n_truth": 3780.0,
          "n_emitted": 11507.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.07241230494894021,
          "coverage": 0.1027864538270643,
          "tp": 388.32722255864894,
          "fp": 11313.2939453125,
          "fn": 3389.672777441351,
          "n_truth": 3778.0,
          "n_emitted": 11507.0
        },
        "draw20_foldSE_all": {
          "dti": 0.12705192585475872,
          "coverage": 0.1723236525452728,
          "tp": 560.5688417297724,
          "fp": 8488.05078125,
          "fn": 2692.4311582702276,
          "n_truth": 3253.0,
          "n_emitted": 8771.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.13548205867379007,
          "coverage": 0.18406327076878912,
          "tp": 598.0215667277959,
          "fp": 8476.1171875,
          "fn": 2650.9784332722043,
          "n_truth": 3249.0,
          "n_emitted": 8771.0
        },
        "draw21_foldNW_all": {
          "dti": 0.09516442277797395,
          "coverage": 0.17356716545281856,
          "tp": 333.07539050395883,
          "fp": 9490.919921875,
          "fn": 1585.9246094960413,
          "n_truth": 1919.0,
          "n_emitted": 9655.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.08439323193485096,
          "coverage": 0.15349983445127036,
          "tp": 295.33368148424415,
          "fp": 9506.140625,
          "fn": 1628.6663185157558,
          "n_truth": 1924.0,
          "n_emitted": 9655.0
        },
        "draw21_foldNE_all": {
          "dti": 0.11125174150980213,
          "coverage": 0.19709808894667438,
          "tp": 466.1369803588849,
          "fp": 11023.51171875,
          "fn": 1898.863019641115,
          "n_truth": 2365.0,
          "n_emitted": 11261.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.12130433936471481,
          "coverage": 0.2155390722625354,
          "tp": 508.2411323950585,
          "fp": 11008.767578125,
          "fn": 1849.7588676049415,
          "n_truth": 2358.0,
          "n_emitted": 11261.0
        },
        "draw21_foldSW_all": {
          "dti": 0.07153545040061975,
          "coverage": 0.10144037889232942,
          "tp": 384.05327448635916,
          "fp": 11315.509765625,
          "fn": 3401.946725513641,
          "n_truth": 3786.0,
          "n_emitted": 11507.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.07783388901821672,
          "coverage": 0.11049332234317341,
          "tp": 417.7752517795387,
          "fp": 11295.84375,
          "fn": 3363.224748220461,
          "n_truth": 3781.0,
          "n_emitted": 11507.0
        },
        "draw21_foldSE_all": {
          "dti": 0.12439624914749467,
          "coverage": 0.1687373457509239,
          "tp": 548.9025857277554,
          "fp": 8501.763671875,
          "fn": 2704.0974142722444,
          "n_truth": 3253.0,
          "n_emitted": 8771.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.13321411171699157,
          "coverage": 0.18101241626223885,
          "tp": 588.109340436014,
          "fp": 8489.728515625,
          "fn": 2660.890659563986,
          "n_truth": 3249.0,
          "n_emitted": 8771.0
        }
      }
    },
    "GEMSDOE27": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.09719107195151397,
      "pooled_coverage": 0.17755366328786862,
      "ci95": [
        0.08670182110635657,
        0.10730083482964382
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.08413555165621614,
          "coverage": 0.18431379085659447,
          "tp": 354.80404739894436,
          "fp": 13030.458984375,
          "fn": 1570.1959526010555,
          "n_truth": 1925.0,
          "n_emitted": 13249.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.09071323998484583,
          "coverage": 0.19918461564823953,
          "tp": 382.23527742897164,
          "fp": 13010.09375,
          "fn": 1536.7647225710284,
          "n_truth": 1919.0,
          "n_emitted": 13249.0
        },
        "draw20_foldNE_all": {
          "dti": 0.11421537465284642,
          "coverage": 0.24648943168935272,
          "tp": 581.7150587868724,
          "fp": 15443.9921875,
          "fn": 1778.2849412131277,
          "n_truth": 2360.0,
          "n_emitted": 15798.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.10420927303928203,
          "coverage": 0.22463102404250843,
          "tp": 530.3538477643624,
          "fp": 15472.22265625,
          "fn": 1830.6461522356376,
          "n_truth": 2361.0,
          "n_emitted": 15798.0
        },
        "draw20_foldSW_all": {
          "dti": 0.07469317648049563,
          "coverage": 0.12380039972920594,
          "tp": 467.96551097639843,
          "fp": 15737.888671875,
          "fn": 3312.0344890236015,
          "n_truth": 3780.0,
          "n_emitted": 16015.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.07183467228409872,
          "coverage": 0.11904394272881942,
          "tp": 449.74801562947977,
          "fp": 15742.634765625,
          "fn": 3328.2519843705204,
          "n_truth": 3778.0,
          "n_emitted": 16015.0
        },
        "draw20_foldSE_all": {
          "dti": 0.12371353790923559,
          "coverage": 0.19396881562159754,
          "tp": 630.9805572170568,
          "fp": 11858.697265625,
          "fn": 2622.0194427829433,
          "n_truth": 3253.0,
          "n_emitted": 12246.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.1298955410760974,
          "coverage": 0.20392166989423374,
          "tp": 662.5415054863654,
          "fp": 11844.31640625,
          "fn": 2586.458494513635,
          "n_truth": 3249.0,
          "n_emitted": 12246.0
        },
        "draw21_foldNW_all": {
          "dti": 0.08936255274720065,
          "coverage": 0.19629760088216247,
          "tp": 376.6950960928698,
          "fp": 13024.091796875,
          "fn": 1542.3049039071302,
          "n_truth": 1919.0,
          "n_emitted": 13249.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.07817820827022705,
          "coverage": 0.17123177948699853,
          "tp": 329.44994373298516,
          "fp": 13044.99609375,
          "fn": 1594.550056267015,
          "n_truth": 1924.0,
          "n_emitted": 13249.0
        },
        "draw21_foldNE_all": {
          "dti": 0.10214174640309368,
          "coverage": 0.21987564741791668,
          "tp": 520.005906143373,
          "fp": 15475.10546875,
          "fn": 1844.994093856627,
          "n_truth": 2365.0,
          "n_emitted": 15798.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.11321849640457167,
          "coverage": 0.24440504688887998,
          "tp": 576.307100563979,
          "fp": 15442.794921875,
          "fn": 1781.692899436021,
          "n_truth": 2358.0,
          "n_emitted": 15798.0
        },
        "draw21_foldSW_all": {
          "dti": 0.07049275148599866,
          "coverage": 0.11669156245939893,
          "tp": 441.7942554712844,
          "fp": 15750.353515625,
          "fn": 3344.2057445287155,
          "n_truth": 3786.0,
          "n_emitted": 16015.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.07579083767581911,
          "coverage": 0.12556666061092286,
          "tp": 474.7675437698993,
          "fp": 15722.138671875,
          "fn": 3306.2324562301005,
          "n_truth": 3781.0,
          "n_emitted": 16015.0
        },
        "draw21_foldSE_all": {
          "dti": 0.11920935058772489,
          "coverage": 0.18688487908941834,
          "tp": 607.9365116778779,
          "fp": 11878.755859375,
          "fn": 2645.063488322122,
          "n_truth": 3253.0,
          "n_emitted": 12246.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.12717822274241175,
          "coverage": 0.19968563320043503,
          "tp": 648.7786222682134,
          "fp": 11861.892578125,
          "fn": 2600.2213777317866,
          "n_truth": 3249.0,
          "n_emitted": 12246.0
        }
      }
    },
    "GEMSDOE28": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.03153527520816375,
      "pooled_coverage": 0.0450537909912627,
      "ci95": [
        0.028246829013356536,
        0.034722489803931694
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.027112981774524814,
          "coverage": 0.04550513381079303,
          "tp": 87.59738258577659,
          "fp": 8366.54296875,
          "fn": 1837.4026174142234,
          "n_truth": 1925.0,
          "n_emitted": 8413.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.0348763868309147,
          "coverage": 0.05867247869825252,
          "tp": 112.59248662194658,
          "fp": 8353.0576171875,
          "fn": 1806.4075133780534,
          "n_truth": 1919.0,
          "n_emitted": 8413.0
        },
        "draw20_foldNE_all": {
          "dti": 0.0348161155300985,
          "coverage": 0.056513413082010196,
          "tp": 133.37165487354406,
          "fp": 9580.3525390625,
          "fn": 2226.6283451264558,
          "n_truth": 2360.0,
          "n_emitted": 9654.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.037084498064641945,
          "coverage": 0.060198826027316216,
          "tp": 142.1294282504936,
          "fp": 9576.787109375,
          "fn": 2218.8705717495063,
          "n_truth": 2361.0,
          "n_emitted": 9654.0
        },
        "draw20_foldSW_all": {
          "dti": 0.021902482307251184,
          "coverage": 0.0292342454358085,
          "tp": 110.50544774735613,
          "fp": 9996.189453125,
          "fn": 3669.494552252644,
          "n_truth": 3780.0,
          "n_emitted": 10057.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.023805468894934442,
          "coverage": 0.031789086730987674,
          "tp": 120.09916966967143,
          "fp": 9993.0224609375,
          "fn": 3657.9008303303285,
          "n_truth": 3778.0,
          "n_emitted": 10057.0
        },
        "draw20_foldSE_all": {
          "dti": 0.03796766360956578,
          "coverage": 0.04737012042441771,
          "tp": 154.0950017406308,
          "fp": 7126.83154296875,
          "fn": 3098.904998259369,
          "n_truth": 3253.0,
          "n_emitted": 7207.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.04108605852308797,
          "coverage": 0.05129736155335002,
          "tp": 166.6651276868342,
          "fp": 7119.77783203125,
          "fn": 3082.3348723131658,
          "n_truth": 3249.0,
          "n_emitted": 7207.0
        },
        "draw21_foldNW_all": {
          "dti": 0.02828148801079263,
          "coverage": 0.04754480971765181,
          "tp": 91.23848984817383,
          "fp": 8363.1875,
          "fn": 1827.761510151826,
          "n_truth": 1919.0,
          "n_emitted": 8413.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.02639848014011466,
          "coverage": 0.04430616380372878,
          "tp": 85.24505915837418,
          "fp": 8364.58203125,
          "fn": 1838.7549408416257,
          "n_truth": 1924.0,
          "n_emitted": 8413.0
        },
        "draw21_foldNE_all": {
          "dti": 0.03469224044981949,
          "coverage": 0.05625281643786937,
          "tp": 133.03791087556107,
          "fp": 9580.9775390625,
          "fn": 2231.962089124439,
          "n_truth": 2365.0,
          "n_emitted": 9654.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.03561433412489003,
          "coverage": 0.05783392125010714,
          "tp": 136.37238630775263,
          "fp": 9577.34375,
          "fn": 2221.6276136922475,
          "n_truth": 2358.0,
          "n_emitted": 9654.0
        },
        "draw21_foldSW_all": {
          "dti": 0.023121745881435597,
          "coverage": 0.03084464951297887,
          "tp": 116.777843056138,
          "fp": 9992.0390625,
          "fn": 3669.222156943862,
          "n_truth": 3786.0,
          "n_emitted": 10057.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.026320835331053605,
          "coverage": 0.03514254327290556,
          "tp": 132.8739561148559,
          "fp": 9984.337890625,
          "fn": 3648.126043885144,
          "n_truth": 3781.0,
          "n_emitted": 10057.0
        },
        "draw21_foldSE_all": {
          "dti": 0.037253554981413986,
          "coverage": 0.04648420760042454,
          "tp": 151.21312732418104,
          "fp": 7131.9140625,
          "fn": 3101.786872675819,
          "n_truth": 3253.0,
          "n_emitted": 7207.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.04074866660849402,
          "coverage": 0.05088338208779927,
          "tp": 165.32010840325984,
          "fp": 7124.01953125,
          "fn": 3083.67989159674,
          "n_truth": 3249.0,
          "n_emitted": 7207.0
        }
      }
    },
    "GEMSDOE30": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.10226689004897589,
      "pooled_coverage": 0.15790587663450967,
      "ci95": [
        0.09093150254145185,
        0.11327390531714962
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.0889482474631701,
          "coverage": 0.1618330543685191,
          "tp": 311.52862965939926,
          "fp": 9500.2626953125,
          "fn": 1613.4713703406007,
          "n_truth": 1925.0,
          "n_emitted": 9655.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.10032826281191845,
          "coverage": 0.18301497659411178,
          "tp": 351.2057400841005,
          "fp": 9475.6259765625,
          "fn": 1567.7942599158996,
          "n_truth": 1919.0,
          "n_emitted": 9655.0
        },
        "draw20_foldNE_all": {
          "dti": 0.12281886118868907,
          "coverage": 0.21823203880903488,
          "tp": 515.0276115893223,
          "fp": 11011.931640625,
          "fn": 1844.9723884106777,
          "n_truth": 2360.0,
          "n_emitted": 11261.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.11167923029964794,
          "coverage": 0.19810985814661916,
          "tp": 467.73737508416787,
          "fp": 11029.37109375,
          "fn": 1893.262624915832,
          "n_truth": 2361.0,
          "n_emitted": 11261.0
        },
        "draw20_foldSW_all": {
          "dti": 0.07689800003328057,
          "coverage": 0.10919982853780076,
          "tp": 412.77535187288686,
          "fp": 11306.3720703125,
          "fn": 3367.224648127113,
          "n_truth": 3780.0,
          "n_emitted": 11507.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.07241230494894021,
          "coverage": 0.1027864538270643,
          "tp": 388.32722255864894,
          "fp": 11313.2939453125,
          "fn": 3389.672777441351,
          "n_truth": 3778.0,
          "n_emitted": 11507.0
        },
        "draw20_foldSE_all": {
          "dti": 0.12705192585475872,
          "coverage": 0.1723236525452728,
          "tp": 560.5688417297724,
          "fp": 8488.05078125,
          "fn": 2692.4311582702276,
          "n_truth": 3253.0,
          "n_emitted": 8771.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.13548205867379007,
          "coverage": 0.18406327076878912,
          "tp": 598.0215667277959,
          "fp": 8476.1171875,
          "fn": 2650.9784332722043,
          "n_truth": 3249.0,
          "n_emitted": 8771.0
        },
        "draw21_foldNW_all": {
          "dti": 0.09516442277797395,
          "coverage": 0.17356716545281856,
          "tp": 333.07539050395883,
          "fp": 9490.919921875,
          "fn": 1585.9246094960413,
          "n_truth": 1919.0,
          "n_emitted": 9655.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.08439323193485096,
          "coverage": 0.15349983445127036,
          "tp": 295.33368148424415,
          "fp": 9506.140625,
          "fn": 1628.6663185157558,
          "n_truth": 1924.0,
          "n_emitted": 9655.0
        },
        "draw21_foldNE_all": {
          "dti": 0.11125174150980213,
          "coverage": 0.19709808894667438,
          "tp": 466.1369803588849,
          "fp": 11023.51171875,
          "fn": 1898.863019641115,
          "n_truth": 2365.0,
          "n_emitted": 11261.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.12130433936471481,
          "coverage": 0.2155390722625354,
          "tp": 508.2411323950585,
          "fp": 11008.767578125,
          "fn": 1849.7588676049415,
          "n_truth": 2358.0,
          "n_emitted": 11261.0
        },
        "draw21_foldSW_all": {
          "dti": 0.07153545040061975,
          "coverage": 0.10144037889232942,
          "tp": 384.05327448635916,
          "fp": 11315.509765625,
          "fn": 3401.946725513641,
          "n_truth": 3786.0,
          "n_emitted": 11507.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.07783388901821672,
          "coverage": 0.11049332234317341,
          "tp": 417.7752517795387,
          "fp": 11295.84375,
          "fn": 3363.224748220461,
          "n_truth": 3781.0,
          "n_emitted": 11507.0
        },
        "draw21_foldSE_all": {
          "dti": 0.12439624914749467,
          "coverage": 0.1687373457509239,
          "tp": 548.9025857277554,
          "fp": 8501.763671875,
          "fn": 2704.0974142722444,
          "n_truth": 3253.0,
          "n_emitted": 8771.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.13321411171699157,
          "coverage": 0.18101241626223885,
          "tp": 588.109340436014,
          "fp": 8489.728515625,
          "fn": 2660.890659563986,
          "n_truth": 3249.0,
          "n_emitted": 8771.0
        }
      }
    },
    "GEMSDOE31": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.03273307810048334,
      "pooled_coverage": 0.04813685189059694,
      "ci95": [
        0.02957482267862288,
        0.03586370319043169
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.028043791808403735,
          "coverage": 0.04860060399484863,
          "tp": 93.55616269008362,
          "fp": 8886.8134765625,
          "fn": 1831.4438373099165,
          "n_truth": 1925.0,
          "n_emitted": 8938.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.033786336934554156,
          "coverage": 0.05868384698254385,
          "tp": 112.61430235950165,
          "fp": 8877.04296875,
          "fn": 1806.3856976404984,
          "n_truth": 1919.0,
          "n_emitted": 8938.0
        },
        "draw20_foldNE_all": {
          "dti": 0.03401169316631823,
          "coverage": 0.05706029891642684,
          "tp": 134.66230544276735,
          "fp": 10221.8095703125,
          "fn": 2225.3376945572327,
          "n_truth": 2360.0,
          "n_emitted": 10295.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.03787876886756651,
          "coverage": 0.06355725303233745,
          "tp": 150.05867440934873,
          "fp": 10213.6962890625,
          "fn": 2210.941325590651,
          "n_truth": 2361.0,
          "n_emitted": 10295.0
        },
        "draw20_foldSW_all": {
          "dti": 0.022275854138322365,
          "coverage": 0.030550535355319205,
          "tp": 115.4810236431066,
          "fp": 10685.19140625,
          "fn": 3664.5189763568933,
          "n_truth": 3780.0,
          "n_emitted": 10748.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.026285543139116553,
          "coverage": 0.036074654105425034,
          "tp": 136.29004321029578,
          "fp": 10676.615234375,
          "fn": 3641.7099567897044,
          "n_truth": 3778.0,
          "n_emitted": 10748.0
        },
        "draw20_foldSE_all": {
          "dti": 0.040065589994997916,
          "coverage": 0.051233835910801176,
          "tp": 166.66366821783623,
          "fp": 7620.18994140625,
          "fn": 3086.3363317821636,
          "n_truth": 3253.0,
          "n_emitted": 7706.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.04269817420782068,
          "coverage": 0.054634901335825437,
          "tp": 177.50879444009684,
          "fp": 7612.953125,
          "fn": 3071.4912055599034,
          "n_truth": 3249.0,
          "n_emitted": 7706.0
        },
        "draw21_foldNW_all": {
          "dti": 0.029138197407019353,
          "coverage": 0.050586762874354214,
          "tp": 97.07599795588574,
          "fp": 8884.783203125,
          "fn": 1821.9240020441143,
          "n_truth": 1919.0,
          "n_emitted": 8938.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.027285042672463213,
          "coverage": 0.04728813907112137,
          "tp": 90.98237957283752,
          "fp": 8885.591796875,
          "fn": 1833.0176204271625,
          "n_truth": 1924.0,
          "n_emitted": 8938.0
        },
        "draw21_foldNE_all": {
          "dti": 0.037873964183133144,
          "coverage": 0.06348792938329555,
          "tp": 150.14895299149396,
          "fp": 10212.037109375,
          "fn": 2214.851047008506,
          "n_truth": 2365.0,
          "n_emitted": 10295.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.037909275478992636,
          "coverage": 0.06364599111108137,
          "tp": 150.07724703992986,
          "fp": 10212.1875,
          "fn": 2207.9227529600703,
          "n_truth": 2358.0,
          "n_emitted": 10295.0
        },
        "draw21_foldSW_all": {
          "dti": 0.02426327500882346,
          "coverage": 0.033257331503579755,
          "tp": 125.91225707255296,
          "fp": 10677.173828125,
          "fn": 3660.087742927447,
          "n_truth": 3786.0,
          "n_emitted": 10748.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.02885870736201061,
          "coverage": 0.03959631095645469,
          "tp": 149.71365172635518,
          "fp": 10665.3642578125,
          "fn": 3631.2863482736448,
          "n_truth": 3781.0,
          "n_emitted": 10748.0
        },
        "draw21_foldSE_all": {
          "dti": 0.037841564658878106,
          "coverage": 0.04837748707188611,
          "tp": 157.37196544484553,
          "fp": 7624.1611328125,
          "fn": 3095.6280345551545,
          "n_truth": 3253.0,
          "n_emitted": 7706.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.04102637952291722,
          "coverage": 0.05249507243812872,
          "tp": 170.5564903514802,
          "fp": 7619.6416015625,
          "fn": 3078.44350964852,
          "n_truth": 3249.0,
          "n_emitted": 7706.0
        }
      }
    },
    "GEMSDOE32": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.004729038412082699,
      "pooled_coverage": 0.006739156493901159,
      "ci95": [
        0.004318925433915449,
        0.005168440926990719
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.005119234300348168,
          "coverage": 0.00859620922427085,
          "tp": 16.54770275672139,
          "fp": 8445.7353515625,
          "fn": 1908.4522972432785,
          "n_truth": 1925.0,
          "n_emitted": 8458.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.005014688193299874,
          "coverage": 0.008433615134521486,
          "tp": 16.184107443146733,
          "fp": 8444.51953125,
          "fn": 1902.8158925568532,
          "n_truth": 1919.0,
          "n_emitted": 8458.0
        },
        "draw20_foldNE_all": {
          "dti": 0.005721849025628992,
          "coverage": 0.0092493422094324,
          "tp": 21.82844761426046,
          "fp": 9612.81640625,
          "fn": 2338.1715523857397,
          "n_truth": 2360.0,
          "n_emitted": 9629.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.004978923243562035,
          "coverage": 0.0080457656701271,
          "tp": 18.996052747170083,
          "fp": 9613.470703125,
          "fn": 2342.00394725283,
          "n_truth": 2361.0,
          "n_emitted": 9629.0
        },
        "draw20_foldSW_all": {
          "dti": 0.0036614968254688987,
          "coverage": 0.00490293504472627,
          "tp": 18.5330944690653,
          "fp": 10169.5517578125,
          "fn": 3761.4669055309346,
          "n_truth": 3780.0,
          "n_emitted": 10184.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.004205780460762832,
          "coverage": 0.0056332499216276925,
          "tp": 21.282418203909423,
          "fp": 10168.107421875,
          "fn": 3756.7175817960906,
          "n_truth": 3778.0,
          "n_emitted": 10184.0
        },
        "draw20_foldSE_all": {
          "dti": 0.0034797123829621137,
          "coverage": 0.0042978214321099445,
          "tp": 13.98081311865365,
          "fp": 7063.0546875,
          "fn": 3239.0191868813463,
          "n_truth": 3253.0,
          "n_emitted": 7074.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.005083238459760853,
          "coverage": 0.00628178974310084,
          "tp": 20.40953487533463,
          "fp": 7058.91748046875,
          "fn": 3228.5904651246656,
          "n_truth": 3249.0,
          "n_emitted": 7074.0
        },
        "draw21_foldNW_all": {
          "dti": 0.0031000233064623294,
          "coverage": 0.0052134440245985075,
          "tp": 10.004599083204536,
          "fp": 8450.32421875,
          "fn": 1908.9954009167955,
          "n_truth": 1919.0,
          "n_emitted": 8458.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.005410020062761232,
          "coverage": 0.009086906265319859,
          "tp": 17.483207654475407,
          "fp": 8444.689453125,
          "fn": 1906.5167923455247,
          "n_truth": 1924.0,
          "n_emitted": 8458.0
        },
        "draw21_foldNE_all": {
          "dti": 0.0058060526566376,
          "coverage": 0.009374880915335343,
          "tp": 22.171593364768086,
          "fp": 9611.345703125,
          "fn": 2342.828406635232,
          "n_truth": 2365.0,
          "n_emitted": 9629.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.006190248529220478,
          "coverage": 0.010010824875317926,
          "tp": 23.605525055999667,
          "fp": 9611.0966796875,
          "fn": 2334.394474944,
          "n_truth": 2358.0,
          "n_emitted": 9629.0
        },
        "draw21_foldSW_all": {
          "dti": 0.004172962032270323,
          "coverage": 0.005584299026213742,
          "tp": 21.14215611324523,
          "fp": 10167.1708984375,
          "fn": 3764.857843886755,
          "n_truth": 3786.0,
          "n_emitted": 10184.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.005495714256245373,
          "coverage": 0.0073593022685602425,
          "tp": 27.825521877426276,
          "fp": 10163.830078125,
          "fn": 3753.174478122574,
          "n_truth": 3781.0,
          "n_emitted": 10184.0
        },
        "draw21_foldSE_all": {
          "dti": 0.004289063617143429,
          "coverage": 0.005297877115812058,
          "tp": 17.233994257736626,
          "fp": 7061.3916015625,
          "fn": 3235.7660057422636,
          "n_truth": 3253.0,
          "n_emitted": 7074.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.004430084565265658,
          "coverage": 0.00547413181866696,
          "tp": 17.785454278848952,
          "fp": 7059.70751953125,
          "fn": 3231.214545721151,
          "n_truth": 3249.0,
          "n_emitted": 7074.0
        }
      }
    },
    "GEMSDOE33": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.05534030951426988,
      "pooled_coverage": 0.08306250239400044,
      "ci95": [
        0.050436013269554575,
        0.0601929105665239
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.056609966253549235,
          "coverage": 0.10078346132609703,
          "tp": 194.0081630527368,
          "fp": 9241.5048828125,
          "fn": 1730.9918369472632,
          "n_truth": 1925.0,
          "n_emitted": 9343.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.06294407217800989,
          "coverage": 0.11232022048641357,
          "tp": 215.54250311342764,
          "fp": 9230.205078125,
          "fn": 1703.4574968865722,
          "n_truth": 1919.0,
          "n_emitted": 9343.0
        },
        "draw20_foldNE_all": {
          "dti": 0.05991638225647834,
          "coverage": 0.10276831294251965,
          "tp": 242.53321854434637,
          "fp": 10556.7744140625,
          "fn": 2117.4667814556537,
          "n_truth": 2360.0,
          "n_emitted": 10685.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.05563680289529395,
          "coverage": 0.09536323734167658,
          "tp": 225.1526033636984,
          "fp": 10564.990234375,
          "fn": 2135.8473966363017,
          "n_truth": 2361.0,
          "n_emitted": 10685.0
        },
        "draw20_foldSW_all": {
          "dti": 0.041491499453608804,
          "coverage": 0.05777613528588837,
          "tp": 218.39379138065803,
          "fp": 10979.501953125,
          "fn": 3561.606208619342,
          "n_truth": 3780.0,
          "n_emitted": 11093.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.042253867776999396,
          "coverage": 0.05885487299746006,
          "tp": 222.35371018440412,
          "fp": 10977.2861328125,
          "fn": 3555.646289815596,
          "n_truth": 3778.0,
          "n_emitted": 11093.0
        },
        "draw20_foldSE_all": {
          "dti": 0.06644996046892039,
          "coverage": 0.08676496533190897,
          "tp": 282.2464322246999,
          "fp": 7943.2705078125,
          "fn": 2970.7535677753003,
          "n_truth": 3253.0,
          "n_emitted": 8092.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.06996061275429466,
          "coverage": 0.09141805408629686,
          "tp": 297.0172577263785,
          "fp": 7934.4453125,
          "fn": 2951.9827422736216,
          "n_truth": 3249.0,
          "n_emitted": 8092.0
        },
        "draw21_foldNW_all": {
          "dti": 0.05198741862995496,
          "coverage": 0.09266464031174777,
          "tp": 177.82344475824397,
          "fp": 9248.72265625,
          "fn": 1741.176555241756,
          "n_truth": 1919.0,
          "n_emitted": 9343.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.05130039247927934,
          "coverage": 0.09129401298325554,
          "tp": 175.64968097978365,
          "fp": 9248.0712890625,
          "fn": 1748.3503190202164,
          "n_truth": 1924.0,
          "n_emitted": 9343.0
        },
        "draw21_foldNE_all": {
          "dti": 0.06210502226756952,
          "coverage": 0.10641907211348729,
          "tp": 251.68110554839745,
          "fp": 10550.859375,
          "fn": 2113.3188944516023,
          "n_truth": 2365.0,
          "n_emitted": 10685.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.05808651084399496,
          "coverage": 0.09963830141500411,
          "tp": 234.9471147365797,
          "fp": 10556.94921875,
          "fn": 2123.05288526342,
          "n_truth": 2358.0,
          "n_emitted": 10685.0
        },
        "draw21_foldSW_all": {
          "dti": 0.04121161654994534,
          "coverage": 0.057336616246711485,
          "tp": 217.07642911004967,
          "fp": 10975.724609375,
          "fn": 3568.9235708899505,
          "n_truth": 3786.0,
          "n_emitted": 11093.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.045509549476016875,
          "coverage": 0.06337494617376503,
          "tp": 239.6206714830056,
          "fp": 10962.7958984375,
          "fn": 3541.3793285169945,
          "n_truth": 3781.0,
          "n_emitted": 11093.0
        },
        "draw21_foldSE_all": {
          "dti": 0.06355714562453772,
          "coverage": 0.08296945468859142,
          "tp": 269.8996361019879,
          "fp": 7950.93212890625,
          "fn": 2983.100363898012,
          "n_truth": 3253.0,
          "n_emitted": 8092.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.06957698892549523,
          "coverage": 0.09093970330688267,
          "tp": 295.4630960440618,
          "fp": 7941.35400390625,
          "fn": 2953.536903955938,
          "n_truth": 3249.0,
          "n_emitted": 8092.0
        }
      }
    },
    "GEMSDOE36": {
      "evidence_class": "HOLDOUT-DTI",
      "evaluator_version": "gems57-holdout-v1 (shared hide-and-recover; alpha=0.2, beta=0.8, 3 px triangular kernel)",
      "pooled_dti": 0.004871196530481981,
      "pooled_coverage": 0.007039091222115184,
      "ci95": [
        0.004470203528666086,
        0.005303463315415316
      ],
      "withheld_positive_pixels": 45260,
      "n_cells": 16,
      "folds": {
        "draw20_foldNW_all": {
          "dti": 0.005245474377186883,
          "coverage": 0.008890484015656864,
          "tp": 17.114181730139464,
          "fp": 8596.1689453125,
          "fn": 1907.8858182698605,
          "n_truth": 1925.0,
          "n_emitted": 8609.0
        },
        "draw20_foldNW_detached": {
          "dti": 0.0051420778715181754,
          "coverage": 0.008728810013843047,
          "tp": 16.750586416564808,
          "fp": 8595.009765625,
          "fn": 1902.2494135834352,
          "n_truth": 1919.0,
          "n_emitted": 8609.0
        },
        "draw20_foldNE_all": {
          "dti": 0.0057149579912320015,
          "coverage": 0.0092493422094324,
          "tp": 21.82844761426046,
          "fp": 9635.81640625,
          "fn": 2338.1715523857397,
          "n_truth": 2360.0,
          "n_emitted": 9652.0
        },
        "draw20_foldNE_detached": {
          "dti": 0.004972927514148975,
          "coverage": 0.0080457656701271,
          "tp": 18.996052747170083,
          "fp": 9636.470703125,
          "fn": 2342.00394725283,
          "n_truth": 2361.0,
          "n_emitted": 9652.0
        },
        "draw20_foldSW_all": {
          "dti": 0.0038464995120444483,
          "coverage": 0.005330545041553776,
          "tp": 20.149460257073272,
          "fp": 11051.794921875,
          "fn": 3759.8505397429267,
          "n_truth": 3780.0,
          "n_emitted": 11068.0
        },
        "draw20_foldSW_detached": {
          "dti": 0.0047344493355413,
          "coverage": 0.006563174685350385,
          "tp": 24.795673961253755,
          "fp": 11049.6435546875,
          "fn": 3753.2043260387463,
          "n_truth": 3778.0,
          "n_emitted": 11068.0
        },
        "draw20_foldSE_all": {
          "dti": 0.003530438030907228,
          "coverage": 0.004376101176192352,
          "tp": 14.23545712615372,
          "fp": 7134.7998046875,
          "fn": 3238.7645428738465,
          "n_truth": 3253.0,
          "n_emitted": 7146.0
        },
        "draw20_foldSE_detached": {
          "dti": 0.0051282680355614315,
          "coverage": 0.00636016586113718,
          "tp": 20.664178882834698,
          "fp": 7130.6630859375,
          "fn": 3228.3358211171653,
          "n_truth": 3249.0,
          "n_emitted": 7146.0
        },
        "draw21_foldNW_all": {
          "dti": 0.0032627301157620477,
          "coverage": 0.00553844138355422,
          "tp": 10.62826901504055,
          "fp": 8600.7578125,
          "fn": 1908.3717309849594,
          "n_truth": 1919.0,
          "n_emitted": 8609.0
        },
        "draw21_foldNW_detached": {
          "dti": 0.005473045732736709,
          "coverage": 0.00927870768129488,
          "tp": 17.85223357881135,
          "fp": 8595.37890625,
          "fn": 1906.1477664211886,
          "n_truth": 1924.0,
          "n_emitted": 8609.0
        },
        "draw21_foldNE_all": {
          "dti": 0.005799067115859878,
          "coverage": 0.009374880915335343,
          "tp": 22.171593364768086,
          "fp": 9634.345703125,
          "fn": 2342.828406635232,
          "n_truth": 2365.0,
          "n_emitted": 9652.0
        },
        "draw21_foldNE_detached": {
          "dti": 0.0061827902821171435,
          "coverage": 0.010010824875317926,
          "tp": 23.605525055999667,
          "fp": 9634.0966796875,
          "fn": 2334.394474944,
          "n_truth": 2358.0,
          "n_emitted": 9652.0
        },
        "draw21_foldSW_all": {
          "dti": 0.004432674231494943,
          "coverage": 0.006138914353519548,
          "tp": 23.24192974242501,
          "fp": 11049.3583984375,
          "fn": 3762.758070257575,
          "n_truth": 3786.0,
          "n_emitted": 11068.0
        },
        "draw21_foldSW_detached": {
          "dti": 0.005969562777644659,
          "coverage": 0.008273363310328663,
          "tp": 31.28158667635267,
          "fp": 11045.62109375,
          "fn": 3749.7184133236474,
          "n_truth": 3781.0,
          "n_emitted": 11068.0
        },
        "draw21_foldSE_all": {
          "dti": 0.00427374752753165,
          "coverage": 0.005297877115812058,
          "tp": 17.233994257736626,
          "fp": 7133.3916015625,
          "fn": 3235.7660057422636,
          "n_truth": 3253.0,
          "n_emitted": 7146.0
        },
        "draw21_foldSE_detached": {
          "dti": 0.004477452620890986,
          "coverage": 0.0055525079367033,
          "tp": 18.04009828634902,
          "fp": 7131.453125,
          "fn": 3230.959901713651,
          "n_truth": 3249.0,
          "n_emitted": 7146.0
        }
      }
    }
  },
  "projection": {
    "evidence_class": "PROJECTED \u2014 not a score, not a measurement",
    "projected_value": 0.3381805960516634,
    "bootstrap_95_interval": [
      0.32770294049755905,
      0.3525366710930341
    ],
    "loo_interval": [
      0.33549224074798645,
      0.34086895135534034
    ],
    "delta_vs_B2_projection": 0.061243385478501056,
    "candidate_position": {
      "log_dots": 9.903487552536127,
      "far_fraction": 0.857
    }
  },
  "geometry": {
    "dots": 20000,
    "far_fraction": 0.857,
    "near2_fraction": 0.0,
    "median_distance_px": 34.058772731852805,
    "on_catalogue": 0
  },
  "uniqueness_vs_focus": {
    "GEMSDOE24": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.006760075156218131
    },
    "GEMSDOE25": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005782532123991141
    },
    "GEMSDOE27": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.00683139283241379
    },
    "GEMSDOE28": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005340916666160865
    },
    "GEMSDOE30": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005782532123991141
    },
    "GEMSDOE31": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005519386086007269
    },
    "GEMSDOE32": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005340488067901635
    },
    "GEMSDOE33": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005633512569643698
    },
    "GEMSDOE36": {
      "forward_3px_overlap": 0.0,
      "reverse_3px_overlap": 0.0,
      "exact_mask_equal": false,
      "surface_spearman": -0.005425553636824374
    },
    "13GEMSDOE_lattice": {
      "forward_3px_overlap": 0.9996,
      "reverse_3px_overlap": 0.0763382392034607,
      "surface_spearman": -0.0003143608750861239,
      "note": "covering-grid probe; every dotted raster on this grid exceeds the literal 70% rule"
    }
  },
  "raster": {
    "file": "docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif",
    "sha256": "9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c",
    "bytes": 102331,
    "zip": "korea7-consensus-offcat-20k-20261104-zeros.zip",
    "zip_sha256": "7460b2dd99ba2cd44d412b3d021fa1c30fb0a25b071b6e5f66a0c661a0d2a6a5",
    "dots": 20000,
    "encoding": "zeros (float32, 0.0 off-dot, 1.0 on-dot; single band; tiled deflate; sample grid)"
  },
  "validator_output": {
    "file": "/home/user/Korea7/docs/downloads/korea7-consensus-offcat-20k-20261104-zeros.tif",
    "bytes": 102331,
    "sha256": "9e3454636697248a9fa547ecf96f7611f671ca05fdd11352b890f7069a68999c",
    "meta": {
      "crs": "EPSG:32611",
      "shape": [
        3730,
        3292
      ],
      "dtype": "float32",
      "count": 1,
      "nodata": null,
      "transform": [
        100.0,
        0.0,
        243350.0,
        0.0,
        -100.0,
        4508550.0
      ],
      "profile_compress": "deflate"
    },
    "band_description": [
      null
    ],
    "n_finite": 12279160,
    "n_nan": 0,
    "n_infinite": 0,
    "min": 0.0,
    "max": 1.0,
    "mean": 0.0016287759644910693,
    "emitted_positive_pixels": 20000,
    "checks": {
      "single_band": true,
      "dtype_float32": true,
      "dimensions_3730x3292": true,
      "crs_epsg_32611": true,
      "transform_matches_sample_submission": true,
      "no_nan_anywhere": true,
      "no_inf_anywhere": true,
      "no_sentinel_values": true,
      "range_0_1_guaranteed": true,
      "min_ge_0": true,
      "max_le_1": true,
      "in_footprint_all_finite": true,
      "in_footprint_range_0_1": true,
      "outside_footprint_zero": true,
      "zero_dots_on_mapped_catalogue": true
    },
    "all_checks_passed": true,
    "validation_class": "local format/range preflight; not organizer acceptance or uniqueness clearance",
    "on_catalogue_positive_pixels": 0,
    "in_footprint_positive_pixels": 20000,
    "footprint_fraction": 0.0038704386155208846
  },
  "zip_check": {
    "member_names": [
      "korea7-consensus-offcat-20k-20261104-zeros.tif"
    ],
    "single_tiff": true,
    "bytes_match": true
  },
  "name": "korea7-consensus-offcat-20k-20261104-zeros",
  "note": "Korea7 4-method off-catalogue consensus, 20k dots, 85% far from catalogue; unique vs nine focus sites; research only.",
  "note_chars": 117,
  "ok_to_submit": false,
  "download_available": "research artifact; NOT CLEARED for a weekly slot",
  "slot_selected_or_spent": false,
  "experiments_used": 1,
  "experiments_budget": 3,
  "verdict": "negative",
  "verdict_reason": "The candidate is format-valid and unique by construction versus the nine focus-site rasters (0% forward 3-px overlap), and its PROJECTED leaderboard value is above the B2 projection. However, its HOLDOUT-DTI is 0.000 (below the random control) because the method is off-catalogue by design, and it fails the literal 13GEMS covering-lattice probe. Under the parallel-run protocol a candidate that has not beaten the holdout best is not promoted to a weekly slot. This is a research artifact, not an organizer-cleared submission.",
  "owner_decision_required": "Decide whether the off-catalogue projection or the catalogue hide-and-recover holdout governs promotion. The two instruments disagree by construction: the organizer masks known faults, while the holdout truth is the catalogue.",
  "known_deviations": [
    "The shared gems57.holdout evaluator (gems57-holdout-v1) is used for the holdout; the prior nine-site table used gems57-pooled-hide-v2. The two evaluators are not interchangeable.",
    "The projection is an OLS extrapolation from nine USER-REPORTED scores; it is not a score and cannot see surface quality.",
    "The 13GEMS lattice probe is a covering grid; the literal 70% rule is saturated and every dotted raster on this grid fails it. This is flagged as an owner decision, not waived.",
    "The reference candidates are research artifacts from the same project family, not organizer-cleared submissions. The consensus is a new method, not an exact copy."
  ]
}
```
