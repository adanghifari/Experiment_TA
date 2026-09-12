# Final Candidate Analysis

## Guardrails

- Metrics are extracted from repo-new experiment artifacts only.
- Repo-old is represented only by historical mapping from experiment_index.csv.
- Existing checkpoints and experiment artifacts were not modified.
- NA means the artifact/field was not available.
- Conflict notes mark disagreement between per-experiment artifacts and summary/index files.

## Headline Winners

- Best overall fusion: experiment_8 (0.87074)
- Best front: experiment_8 (0.85931)
- Best side: experiment_3 (0.81679)
- Best phone_use recall by average fusion: experiment_1 (0.98834)
- Best safe recall by average fusion: experiment_8 (0.75)
- Most stable by mean abs train-val F1 gap: experiment_15 (0.03227)

## Candidate Shortlist

| Experiment | Historical Source Mapping | Scenario | Mean Val Macro F1 | Front Test Macro F1 | Side Test Macro F1 | Best Overall Fusion | Average Fusion Safe Recall | Average Fusion Phone Recall | Front Train-Val F1 Gap | Side Train-Val F1 Gap | Tradeoff Score | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| experiment_8 | Exp 8 | Golden Balance | 0.81499 | 0.85931 | 0.78012 | 0.87074 | 0.75 | 0.96501 | 0.09973 | 0.11857 | 0.85366 | conflict experiment_index front_macro_f1=0.86314 vs artifact=0.85931; conflict experiment_index side_macro_f1=0.77124 vs artifact=0.78012; conflict experiment_index average_fusion_macro_f1=0.87494 vs artifact=0.87074; conflict experiment_index adaptive_fusion_macro_f1=0.87494 vs artifact=0.87074 |
| experiment_4 | Exp 4 | Regularisasi dan stride 5 | 0.82364 | 0.82133 | 0.8121 | 0.85253 | 0.68421 | 0.97085 | 0.13425 | 0.15619 | 0.81413 | conflict experiment_index front_macro_f1=0.88252 vs artifact=0.82133; conflict experiment_index side_macro_f1=0.80318 vs artifact=0.8121; conflict experiment_index average_fusion_macro_f1=0.84434 vs artifact=0.85253; conflict experiment_index adaptive_fusion_macro_f1=0.84434 vs artifact=0.85253 |
| experiment_2 | Exp 2 | Perbaikan pipeline awal | 0.87403 | 0.78267 | 0.78792 | 0.83402 | 0.60526 | 0.98251 | 0.11162 | 0.10524 | 0.81007 | conflict experiment_index front_macro_f1=0.80925 vs artifact=0.78267; conflict experiment_index side_macro_f1=0.76181 vs artifact=0.78792; conflict experiment_index average_fusion_macro_f1=0.79197 vs artifact=0.83402; conflict experiment_index adaptive_fusion_macro_f1=0.79197 vs artifact=0.83402 |
| experiment_18 | Exp 21D | Regularisasi side stride 30 | 0.70409 | 0.76626 | 0.67468 | 0.81113 | 0.625 | 0.95556 | -0.02652 | 0.10775 | 0.80881 | conflict experiment_index side_macro_f1=0.73985 vs artifact=0.67468 |
| experiment_5 | Exp 5 | LR rendah dengan regularisasi v4 | 0.68212 | 0.78785 | 0.54586 | 0.79023 | 0.67105 | 0.91837 | 0.06346 | -0.02883 | 0.80071 | conflict experiment_index front_macro_f1=0.8375 vs artifact=0.78785; conflict experiment_index side_macro_f1=0.73806 vs artifact=0.54586; conflict experiment_index average_fusion_macro_f1=0.79897 vs artifact=0.79023; conflict experiment_index adaptive_fusion_macro_f1=0.79897 vs artifact=0.79023 |
| experiment_19 | Exp 21E / Final v2 | Light regularized side stride 30 / Final v2 | 0.70409 | 0.76626 | 0.68372 | 0.79471 | 0.6 | 0.95 | -0.02652 | 0.10703 | 0.79132 | conflict experiment_index side_macro_f1=0.7159 vs artifact=0.68372; conflict experiment_index average_fusion_macro_f1=0.82504 vs artifact=0.79471; conflict experiment_index adaptive_fusion_macro_f1=0.82504 vs artifact=0.79471 |
| experiment_15 | Exp 19 Final Valid | Gamma 0.50 validation-selected | 0.73297 | 0.76626 | 0.64349 | 0.77992 | 0.525 | 0.96667 | -0.02652 | -0.03802 | 0.79003 | conflict experiment_index average_fusion_macro_f1=0.7799 vs artifact=0.77992 |

## Interpretation Notes

- Do not select solely by test Macro F1; compare validation behavior, train-val gaps, recall balance, and fusion gain.
- Average and adaptive fusion often have identical class decisions in these artifacts; when F1 ties, calibration metrics such as ROC-AUC, PR-AUC, ECE, and Brier can still differ.
- Statistical test artifacts were not found in this repo-new extraction pass, so inferential claims should wait until those are added or computed in a separate analysis step.

## Conflicts Found

- experiment_1: conflict experiment_index front_macro_f1=0.82245 vs artifact=0.83759
- experiment_1: conflict experiment_index side_macro_f1=0.83697 vs artifact=0.61415
- experiment_1: conflict experiment_index average_fusion_macro_f1=0.84097 vs artifact=0.81773
- experiment_1: conflict experiment_index adaptive_fusion_macro_f1=0.84097 vs artifact=0.81773
- experiment_2: conflict experiment_index front_macro_f1=0.80925 vs artifact=0.78267
- experiment_2: conflict experiment_index side_macro_f1=0.76181 vs artifact=0.78792
- experiment_2: conflict experiment_index average_fusion_macro_f1=0.79197 vs artifact=0.83402
- experiment_2: conflict experiment_index adaptive_fusion_macro_f1=0.79197 vs artifact=0.83402
- experiment_3: conflict experiment_index front_macro_f1=0.82124 vs artifact=0.75341
- experiment_3: conflict experiment_index side_macro_f1=0.83443 vs artifact=0.81679
- experiment_3: conflict experiment_index average_fusion_macro_f1=0.83915 vs artifact=0.82372
- experiment_3: conflict experiment_index adaptive_fusion_macro_f1=0.83915 vs artifact=0.82372
- experiment_4: conflict experiment_index front_macro_f1=0.88252 vs artifact=0.82133
- experiment_4: conflict experiment_index side_macro_f1=0.80318 vs artifact=0.8121
- experiment_4: conflict experiment_index average_fusion_macro_f1=0.84434 vs artifact=0.85253
- experiment_4: conflict experiment_index adaptive_fusion_macro_f1=0.84434 vs artifact=0.85253
- experiment_5: conflict experiment_index front_macro_f1=0.8375 vs artifact=0.78785
- experiment_5: conflict experiment_index side_macro_f1=0.73806 vs artifact=0.54586
- experiment_5: conflict experiment_index average_fusion_macro_f1=0.79897 vs artifact=0.79023
- experiment_5: conflict experiment_index adaptive_fusion_macro_f1=0.79897 vs artifact=0.79023
- experiment_6: conflict experiment_index front_macro_f1=0.82925 vs artifact=0.55558
- experiment_6: conflict experiment_index side_macro_f1=0.73263 vs artifact=0.57932
- experiment_6: conflict experiment_index average_fusion_macro_f1=0.82873 vs artifact=0.60963
- experiment_6: conflict experiment_index adaptive_fusion_macro_f1=0.82873 vs artifact=0.60963
- experiment_7: conflict experiment_index front_macro_f1=0.8074 vs artifact=0.55968
- experiment_7: conflict experiment_index side_macro_f1=0.73011 vs artifact=0.51949
- experiment_7: conflict experiment_index average_fusion_macro_f1=0.83282 vs artifact=0.59192
- experiment_7: conflict experiment_index adaptive_fusion_macro_f1=0.83282 vs artifact=0.59192
- experiment_8: conflict experiment_index front_macro_f1=0.86314 vs artifact=0.85931
- experiment_8: conflict experiment_index side_macro_f1=0.77124 vs artifact=0.78012
- experiment_8: conflict experiment_index average_fusion_macro_f1=0.87494 vs artifact=0.87074
- experiment_8: conflict experiment_index adaptive_fusion_macro_f1=0.87494 vs artifact=0.87074
- experiment_9: conflict experiment_index front_macro_f1=0.78495 vs artifact=0.8213
- experiment_9: conflict experiment_index side_macro_f1=0.75077 vs artifact=0.57174
- experiment_9: conflict experiment_index average_fusion_macro_f1=0.80444 vs artifact=0.7861
- experiment_9: conflict experiment_index adaptive_fusion_macro_f1=0.80444 vs artifact=0.7861
- experiment_12: conflict experiment_index front_macro_f1=0.7206 vs artifact=0.73985
- experiment_12: conflict experiment_index average_fusion_macro_f1=0.7773 vs artifact=0.76142
- experiment_15: conflict experiment_index average_fusion_macro_f1=0.7799 vs artifact=0.77992
- experiment_16: conflict experiment_index side_macro_f1=0.66044 vs artifact=0.75905
- experiment_16: conflict experiment_index average_fusion_macro_f1=0.7588 vs artifact=0.78589
- experiment_16: conflict experiment_index adaptive_fusion_macro_f1=0.7588 vs artifact=0.78589
- experiment_17: conflict experiment_index side_macro_f1=0.76085 vs artifact=0.75905
- experiment_17: conflict experiment_index average_fusion_macro_f1=0.81626 vs artifact=0.78589
- experiment_17: conflict experiment_index adaptive_fusion_macro_f1=0.81626 vs artifact=0.78589
- experiment_18: conflict experiment_index side_macro_f1=0.73985 vs artifact=0.67468
- experiment_19: conflict experiment_index side_macro_f1=0.7159 vs artifact=0.68372
- experiment_19: conflict experiment_index average_fusion_macro_f1=0.82504 vs artifact=0.79471
- experiment_19: conflict experiment_index adaptive_fusion_macro_f1=0.82504 vs artifact=0.79471
