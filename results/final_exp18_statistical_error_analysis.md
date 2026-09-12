# Final Exp18 Statistical And Error Analysis

Source: repo-new artifacts only, selected recipe `experiment_18`, test split, no retraining. Seed42 Exp18 is the selected model; Exp23 remains robustness validation.

## Metric Sanity Check

| Model | Macro F1 | Accuracy | Safe Recall | Phone Recall | ROC-AUC | PR-AUC | ECE | Brier | CM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| front | 0.76626 | 0.86364 | 0.60000 | 0.92222 | 0.88014 | 0.97075 | 0.12513 | 0.11311 | [[24,16],[14,166]] |
| side | 0.67468 | 0.80455 | 0.47500 | 0.87778 | 0.75444 | 0.92515 | 0.16761 | 0.15333 | [[19,21],[22,158]] |
| average | 0.81113 | 0.89545 | 0.62500 | 0.95556 | 0.86292 | 0.96236 | 0.17916 | 0.12341 | [[25,15],[8,172]] |
| adaptive | 0.81113 | 0.89545 | 0.62500 | 0.95556 | 0.86500 | 0.96329 | 0.17159 | 0.12028 | [[25,15],[8,172]] |

## Paired Bootstrap Tests

Bootstrap estimates use 10,000 paired resamples of the same 220 test samples. Positive difference means the first model is higher.

| Comparison | Metric | Mean Difference | 95% CI Low | 95% CI High | Bootstrap p(two-sided) |
|---|---|---:|---:|---:|---:|
| average_vs_front | macro_f1 | 0.04485 | -0.02015 | 0.11081 | 0.17640 |
| average_vs_side | macro_f1 | 0.13689 | 0.08269 | 0.19714 | 0.00000 |
| adaptive_vs_front | macro_f1 | 0.04485 | -0.02015 | 0.11081 | 0.17640 |
| adaptive_vs_side | macro_f1 | 0.13689 | 0.08269 | 0.19714 | 0.00000 |
| average_vs_adaptive | macro_f1 | 0.00000 | 0.00000 | 0.00000 | 1.00000 |
| average_vs_front | roc_auc | -0.01721 | -0.05438 | 0.01804 | 0.35460 |
| average_vs_side | roc_auc | 0.10864 | 0.05827 | 0.16432 | 0.00000 |
| adaptive_vs_front | roc_auc | -0.01510 | -0.05374 | 0.02111 | 0.42840 |
| adaptive_vs_side | roc_auc | 0.11075 | 0.06234 | 0.16371 | 0.00000 |
| average_vs_adaptive | roc_auc | -0.00212 | -0.00933 | 0.00444 | 0.53340 |
| average_vs_front | pr_auc | -0.00826 | -0.02097 | 0.00227 | 0.13700 |
| average_vs_side | pr_auc | 0.03691 | 0.01606 | 0.06314 | 0.00000 |
| adaptive_vs_front | pr_auc | -0.00734 | -0.02000 | 0.00318 | 0.19080 |
| adaptive_vs_side | pr_auc | 0.03784 | 0.01730 | 0.06323 | 0.00000 |
| average_vs_adaptive | pr_auc | -0.00093 | -0.00329 | 0.00105 | 0.36960 |

## McNemar Tests

Exact McNemar tests compare paired correctness on the same test samples.

| Comparison | A correct B wrong | A wrong B correct | Discordant n | Exact p(two-sided) | Continuity Chi2 |
|---|---:|---:|---:|---:|---:|
| average_vs_front | 13 | 6 | 19 | 0.16707 | 1.89474 |
| average_vs_side | 20 | 0 | 20 | 0.00000 | 18.05000 |
| adaptive_vs_front | 13 | 6 | 19 | 0.16707 | 1.89474 |
| adaptive_vs_side | 20 | 0 | 20 | 0.00000 | 18.05000 |
| average_vs_adaptive | 0 | 0 | 0 | 1.00000 | 0.00000 |

## Complementarity Summary

- both_correct: 164
- front_correct_side_wrong: 26
- front_wrong_side_correct: 13
- both_wrong: 17
- fusion_fixed_front_error: 13
- fusion_broke_front_correct: 6
- fusion_fixed_side_error: 20
- fusion_broke_side_correct: 0
- average_adaptive_prediction_diff: 0

## Failure Cases

Total average/adaptive fusion wrong samples: 23. Full list is saved in `results/final_exp18_failure_cases.csv`. Top 10 most confident wrong fusion samples:

| subject | activity | frame | label | front_pred | side_pred | fusion_pred | front_prob | side_prob | avg_prob |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 1 | 61 | 0 | 1 | 1 | 1 | 0.74634 | 0.88879 | 0.81756 |
| 10 | 1 | 61 | 0 | 1 | 1 | 1 | 0.77354 | 0.80114 | 0.78734 |
| 8 | 1 | 211 | 0 | 1 | 1 | 1 | 0.77936 | 0.76987 | 0.77461 |
| 11 | 1 | 91 | 0 | 1 | 1 | 1 | 0.82237 | 0.71842 | 0.77040 |
| 11 | 1 | 151 | 0 | 1 | 1 | 1 | 0.67496 | 0.64328 | 0.65912 |
| 10 | 1 | 91 | 0 | 0 | 1 | 1 | 0.44539 | 0.86911 | 0.65725 |
| 8 | 1 | 121 | 0 | 1 | 1 | 1 | 0.68585 | 0.62605 | 0.65595 |
| 4 | 1 | 1 | 0 | 1 | 1 | 1 | 0.74456 | 0.56644 | 0.65550 |
| 17 | 1 | 1 | 0 | 0 | 1 | 1 | 0.47906 | 0.82962 | 0.65434 |
| 11 | 1 | 31 | 0 | 1 | 1 | 1 | 0.67278 | 0.63195 | 0.65237 |

## Paper-Safe Interpretation

- Fusion improvement over Front/Side is evaluated with paired tests on identical test samples.
- Average and Adaptive fusion have identical hard predictions on Exp18 test set; adaptive changes probabilities/calibration slightly, not classification decisions.
- Complementarity exists because there are samples where Side fixes Front errors and samples where Front fixes Side errors.
- This analysis supports reporting overfit/generalization using train-validation Macro F1 gap, while statistical tests support paired test-set comparison.
