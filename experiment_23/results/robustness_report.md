# Experiment 23 Robustness Report

## Pre-Run Audit

PASS: no unintended behavioral mismatch found. Seed43/44 vary only by `TRAINING_SEED`; recipe remains exact experiment_18. Seed42 uses existing experiment_18 artifacts without retrain.

## Exact Split Verification

- train: 35 subjects [5, 6, 7, 9, 12, 13, 14, 16, 18, 19, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48, 49, 50]; stride30 samples front=1084, side=1084
- val: 8 subjects [1, 2, 3, 15, 20, 22, 27, 41]; stride30 samples front=225, side=225
- test: 7 subjects [4, 8, 10, 11, 17, 21, 42]; stride30 samples front=220, side=220

## TABLE A - Per-Seed Main Performance
| Model | Seed42 | Seed43 | Seed44 | Mean +/- Std |
|---|---|---|---|---|
| Front Macro F1 | 0.76626 | 0.72049 | 0.75940 | 0.74872 +/- 0.02468 |
| Side Macro F1 | 0.67468 | 0.66353 | 0.70213 | 0.68011 +/- 0.01987 |
| Average Fusion Macro F1 | 0.81113 | 0.74028 | 0.76626 | 0.77256 +/- 0.03584 |
| Adaptive Fusion Macro F1 | 0.81113 | 0.74028 | 0.76626 | 0.77256 +/- 0.03584 |

## TABLE B - Per-Class Recall
| Model / Metric | Seed42 | Seed43 | Seed44 | Mean +/- Std |
|---|---|---|---|---|
| Front Safe Recall | 0.60000 | 0.65000 | 0.65000 | 0.63333 +/- 0.02887 |
| Front Phone Recall | 0.92222 | 0.85000 | 0.89444 | 0.88889 +/- 0.03643 |
| Side Safe Recall | 0.47500 | 0.60000 | 0.60000 | 0.55833 +/- 0.07217 |
| Side Phone Recall | 0.87778 | 0.80000 | 0.85000 | 0.84259 +/- 0.03942 |
| Fusion Safe Recall | 0.62500 | 0.57500 | 0.60000 | 0.60000 +/- 0.02500 |
| Fusion Phone Recall | 0.95556 | 0.90556 | 0.92222 | 0.92778 +/- 0.02546 |

## TABLE C - Probability / Calibration
| Metric | Seed42 | Seed43 | Seed44 | Mean +/- Std |
|---|---|---|---|---|
| Fusion ROC-AUC | 0.86500 | 0.84042 | 0.84833 | 0.85125 +/- 0.01255 |
| Fusion PR-AUC | 0.96329 | 0.95434 | 0.95745 | 0.95836 +/- 0.00454 |
| Fusion ECE | 0.17159 | 0.18907 | 0.13498 | 0.16521 +/- 0.02760 |
| Fusion Brier | 0.12028 | 0.14679 | 0.11934 | 0.12880 +/- 0.01558 |

## TABLE D - Confusion Matrices
| Seed | Front CM | Side CM | Average Fusion CM | Adaptive Fusion CM |
|---|---|---|---|---|
| 42 | [[24,16],[14,166]] | [[19,21],[22,158]] | [[25,15],[8,172]] | [[25,15],[8,172]] |
| 43 | [[26,14],[27,153]] | [[24,16],[36,144]] | [[23,17],[17,163]] | [[23,17],[17,163]] |
| 44 | [[26,14],[19,161]] | [[24,16],[27,153]] | [[24,16],[14,166]] | [[24,16],[14,166]] |

## TABLE E - Complementarity
| Metric | Seed42 | Seed43 | Seed44 |
|---|---|---|---|
| both_correct | 164 | 146 | 162 |
| front_correct_side_wrong | 26 | 33 | 25 |
| front_wrong_side_correct | 13 | 22 | 15 |
| both_wrong | 17 | 19 | 18 |
| fusion_fixed_front_error | 13 | 14 | 9 |
| fusion_broke_front_correct | 6 | 7 | 6 |
| fusion_correct_when_side_wrong | 20 | 26 | 19 |
| fusion_wrong_when_side_correct | 0 | 8 | 6 |

## TABLE F - Adaptive Weights
| Metric | Seed42 | Seed43 | Seed44 |
|---|---|---|---|
| mean_front_weight | 0.51260 | 0.51439 | 0.50368 |
| mean_side_weight | 0.48740 | 0.48561 | 0.49632 |
| std_front_weight | 0.03914 | 0.03382 | 0.03877 |
| std_side_weight | 0.03914 | 0.03382 | 0.03877 |
| min_front_weight | 0.41105 | 0.41015 | 0.40256 |
| max_front_weight | 0.61037 | 0.59623 | 0.60711 |
| min_side_weight | 0.38963 | 0.40377 | 0.39289 |
| max_side_weight | 0.58895 | 0.58985 | 0.59744 |
| adaptive_vs_average_prediction_diff_count | 0 | 0 | 0 |
| adaptive_vs_average_prediction_diff_pct | 0.00000 | 0.00000 | 0.00000 |
| front_weight_gt_side_count | 139 | 143 | 120 |
| side_weight_gt_front_count | 81 | 77 | 100 |
| both_weights_near_0_5_count | 173 | 181 | 174 |

## Key Robustness Questions

1. Average Fusion Macro F1 > Front Macro F1 for all seeds: True.
2. Average Fusion Macro F1 > Side Macro F1 for all seeds: True.
3. Fusion consistently best model per seed: True.
4. Ranking Fusion > Front > Side stable: True.
5. Average and Adaptive decisions identical across all seeds: True.
6. Std of Average Fusion Macro F1: 0.03584.
7. Safe Recall stability: variable across seeds; see TABLE B.
8. Phone Recall stability: comparatively high but still varies; see TABLE B.
9. Calibration stability: ECE/Brier vary across seeds; see TABLE C.
10. Obvious outlier: seed43 is the weakest fusion run.

## Robustness Verdict

moderate seed sensitivity. Experiment_18 remains the selected recipe; Exp23 measures stochastic robustness and does not replace the selected seed with a better/worse seed.

## Compact Reproducibility Summary

Experiment_23 FINAL ROBUSTNESS VALIDATION for main recipe experiment_18. Seed42 uses existing experiment_18 artifacts; seed43 and seed44 are standalone retrains from ImageNet pretrained. SPLIT_SEED=42 fixed; TRAINING_SEED varies: 42, 43, 44. Subject split is fixed from manifest_split.csv and not regenerated.
train: 35 subjects IDs=[5, 6, 7, 9, 12, 13, 14, 16, 18, 19, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48, 49, 50]; stride30 samples per view: front=1084, side=1084.
val: 8 subjects IDs=[1, 2, 3, 15, 20, 22, 27, 41]; stride30 samples per view: front=225, side=225.
test: 7 subjects IDs=[4, 8, 10, 11, 17, 21, 42]; stride30 samples per view: front=220, side=220.
Seed 42: Front Macro F1=0.76626, Side Macro F1=0.67468, Average Fusion Macro F1=0.81113, Adaptive Fusion Macro F1=0.81113.
Seed 42 recalls: Front safe=0.60000, front phone=0.92222, Side safe=0.47500, side phone=0.87778, Fusion safe=0.62500, fusion phone=0.95556.
Seed 42 CM: Front=[[24,16],[14,166]], Side=[[19,21],[22,158]], Average Fusion=[[25,15],[8,172]], Adaptive Fusion=[[25,15],[8,172]].
Seed 42 adaptive fusion calibration/probability: ROC-AUC=0.86500, PR-AUC=0.96329, ECE=0.17159, Brier=0.12028.
Seed 43: Front Macro F1=0.72049, Side Macro F1=0.66353, Average Fusion Macro F1=0.74028, Adaptive Fusion Macro F1=0.74028.
Seed 43 recalls: Front safe=0.65000, front phone=0.85000, Side safe=0.60000, side phone=0.80000, Fusion safe=0.57500, fusion phone=0.90556.
Seed 43 CM: Front=[[26,14],[27,153]], Side=[[24,16],[36,144]], Average Fusion=[[23,17],[17,163]], Adaptive Fusion=[[23,17],[17,163]].
Seed 43 adaptive fusion calibration/probability: ROC-AUC=0.84042, PR-AUC=0.95434, ECE=0.18907, Brier=0.14679.
Seed 44: Front Macro F1=0.75940, Side Macro F1=0.70213, Average Fusion Macro F1=0.76626, Adaptive Fusion Macro F1=0.76626.
Seed 44 recalls: Front safe=0.65000, front phone=0.89444, Side safe=0.60000, side phone=0.85000, Fusion safe=0.60000, fusion phone=0.92222.
Seed 44 CM: Front=[[26,14],[19,161]], Side=[[24,16],[27,153]], Average Fusion=[[24,16],[14,166]], Adaptive Fusion=[[24,16],[14,166]].
Seed 44 adaptive fusion calibration/probability: ROC-AUC=0.84833, PR-AUC=0.95745, ECE=0.13498, Brier=0.11934.
Aggregate Front Test Macro F1: seed42=0.76626, seed43=0.72049, seed44=0.75940, mean=0.74872, std=0.02468, min=0.72049, max=0.76626.
Aggregate Front Safe Recall: seed42=0.60000, seed43=0.65000, seed44=0.65000, mean=0.63333, std=0.02887, min=0.60000, max=0.65000.
Aggregate Front Phone Recall: seed42=0.92222, seed43=0.85000, seed44=0.89444, mean=0.88889, std=0.03643, min=0.85000, max=0.92222.
Aggregate Front ROC-AUC: seed42=0.88014, seed43=0.84347, seed44=0.82486, mean=0.84949, std=0.02813, min=0.82486, max=0.88014.
Aggregate Front PR-AUC: seed42=0.97075, seed43=0.95876, seed44=0.94716, mean=0.95889, std=0.01180, min=0.94716, max=0.97075.
Aggregate Front ECE: seed42=0.12513, seed43=0.16235, seed44=0.12890, mean=0.13879, std=0.02049, min=0.12513, max=0.16235.
Aggregate Front Brier: seed42=0.11311, seed43=0.13921, seed44=0.12365, mean=0.12532, std=0.01313, min=0.11311, max=0.13921.
Aggregate Side Test Macro F1: seed42=0.67468, seed43=0.66353, seed44=0.70213, mean=0.68011, std=0.01987, min=0.66353, max=0.70213.
Aggregate Side Safe Recall: seed42=0.47500, seed43=0.60000, seed44=0.60000, mean=0.55833, std=0.07217, min=0.47500, max=0.60000.
Aggregate Side Phone Recall: seed42=0.87778, seed43=0.80000, seed44=0.85000, mean=0.84259, std=0.03942, min=0.80000, max=0.87778.
Aggregate Side ROC-AUC: seed42=0.75444, seed43=0.73778, seed44=0.80014, mean=0.76412, std=0.03229, min=0.73778, max=0.80014.
Aggregate Side PR-AUC: seed42=0.92515, seed43=0.91933, seed44=0.94644, mean=0.93031, std=0.01427, min=0.91933, max=0.94644.
Aggregate Side ECE: seed42=0.16761, seed43=0.20334, seed44=0.12627, mean=0.16574, std=0.03857, min=0.12627, max=0.20334.
Aggregate Side Brier: seed42=0.15333, seed43=0.17770, seed44=0.13970, mean=0.15691, std=0.01925, min=0.13970, max=0.17770.
Aggregate Average Fusion Test Macro F1: seed42=0.81113, seed43=0.74028, seed44=0.76626, mean=0.77256, std=0.03584, min=0.74028, max=0.81113.
Aggregate Average Fusion Safe Recall: seed42=0.62500, seed43=0.57500, seed44=0.60000, mean=0.60000, std=0.02500, min=0.57500, max=0.62500.
Aggregate Average Fusion Phone Recall: seed42=0.95556, seed43=0.90556, seed44=0.92222, mean=0.92778, std=0.02546, min=0.90556, max=0.95556.
Aggregate Average Fusion ROC-AUC: seed42=0.86292, seed43=0.83736, seed44=0.84736, mean=0.84921, std=0.01288, min=0.83736, max=0.86292.
Aggregate Average Fusion PR-AUC: seed42=0.96236, seed43=0.95286, seed44=0.95702, mean=0.95741, std=0.00476, min=0.95286, max=0.96236.
Aggregate Average Fusion ECE: seed42=0.17916, seed43=0.19494, seed44=0.14072, mean=0.17161, std=0.02789, min=0.14072, max=0.19494.
Aggregate Average Fusion Brier: seed42=0.12341, seed43=0.14978, seed44=0.12131, mean=0.13150, std=0.01587, min=0.12131, max=0.14978.
Aggregate Adaptive Fusion Test Macro F1: seed42=0.81113, seed43=0.74028, seed44=0.76626, mean=0.77256, std=0.03584, min=0.74028, max=0.81113.
Aggregate Adaptive Fusion Safe Recall: seed42=0.62500, seed43=0.57500, seed44=0.60000, mean=0.60000, std=0.02500, min=0.57500, max=0.62500.
Aggregate Adaptive Fusion Phone Recall: seed42=0.95556, seed43=0.90556, seed44=0.92222, mean=0.92778, std=0.02546, min=0.90556, max=0.95556.
Aggregate Adaptive Fusion ROC-AUC: seed42=0.86500, seed43=0.84042, seed44=0.84833, mean=0.85125, std=0.01255, min=0.84042, max=0.86500.
Aggregate Adaptive Fusion PR-AUC: seed42=0.96329, seed43=0.95434, seed44=0.95745, mean=0.95836, std=0.00454, min=0.95434, max=0.96329.
Aggregate Adaptive Fusion ECE: seed42=0.17159, seed43=0.18907, seed44=0.13498, mean=0.16521, std=0.02760, min=0.13498, max=0.18907.
Aggregate Adaptive Fusion Brier: seed42=0.12028, seed43=0.14679, seed44=0.11934, mean=0.12880, std=0.01558, min=0.11934, max=0.14679.
Aggregate Front Train-Val F1 Gap: seed42=-0.02652, seed43=0.05985, seed44=0.10581, mean=0.04638, std=0.06719, min=-0.02652, max=0.10581.
Aggregate Side Train-Val F1 Gap: seed42=0.10775, seed43=-0.02259, seed44=0.00733, mean=0.03083, std=0.06827, min=-0.02259, max=0.10775.
Complementarity seed 42: both_correct=164, front_correct_side_wrong=26, front_wrong_side_correct=13, both_wrong=17, fusion_fixed_front_error=13, fusion_broke_front_correct=6, fusion_correct_when_side_wrong=20, fusion_wrong_when_side_correct=0, side_only_correct=13, fusion_correct_when_both_wrong=0, fusion_wrong_when_both_single_view_correct=0.
Complementarity seed 43: both_correct=146, front_correct_side_wrong=33, front_wrong_side_correct=22, both_wrong=19, fusion_fixed_front_error=14, fusion_broke_front_correct=7, fusion_correct_when_side_wrong=26, fusion_wrong_when_side_correct=8, side_only_correct=22, fusion_correct_when_both_wrong=0, fusion_wrong_when_both_single_view_correct=0.
Complementarity seed 44: both_correct=162, front_correct_side_wrong=25, front_wrong_side_correct=15, both_wrong=18, fusion_fixed_front_error=9, fusion_broke_front_correct=6, fusion_correct_when_side_wrong=19, fusion_wrong_when_side_correct=6, side_only_correct=15, fusion_correct_when_both_wrong=0, fusion_wrong_when_both_single_view_correct=0.
Adaptive weights seed 42: mean_front_weight=0.51260, mean_side_weight=0.48740, std_front_weight=0.03914, std_side_weight=0.03914, min_front_weight=0.41105, max_front_weight=0.61037, min_side_weight=0.38963, max_side_weight=0.58895, adaptive_vs_average_prediction_diff_count=0, adaptive_vs_average_prediction_diff_pct=0.00000, front_weight_gt_side_count=139, side_weight_gt_front_count=81, both_weights_near_0_5_count=173.
Adaptive weights seed 43: mean_front_weight=0.51439, mean_side_weight=0.48561, std_front_weight=0.03382, std_side_weight=0.03382, min_front_weight=0.41015, max_front_weight=0.59623, min_side_weight=0.40377, max_side_weight=0.58985, adaptive_vs_average_prediction_diff_count=0, adaptive_vs_average_prediction_diff_pct=0.00000, front_weight_gt_side_count=143, side_weight_gt_front_count=77, both_weights_near_0_5_count=181.
Adaptive weights seed 44: mean_front_weight=0.50368, mean_side_weight=0.49632, std_front_weight=0.03877, std_side_weight=0.03877, min_front_weight=0.40256, max_front_weight=0.60711, min_side_weight=0.39289, max_side_weight=0.59744, adaptive_vs_average_prediction_diff_count=0, adaptive_vs_average_prediction_diff_pct=0.00000, front_weight_gt_side_count=120, side_weight_gt_front_count=100, both_weights_near_0_5_count=174.
Final robustness verdict: moderate seed sensitivity. No seed cherry-picking; experiment_18 remains selected recipe.


