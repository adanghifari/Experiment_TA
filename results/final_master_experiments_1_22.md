# Final Master Summary Experiments 1-22

Source of truth: artifact repo baru only. Experiment_23 excluded from recipe table because it is robustness validation.

## Data Quality / Artifact Issues

- No duplicate experiment rows detected.
- Metrics were read from repo-new artifacts under `experiment_1` through `experiment_22`.
- Experiment_23 is excluded from main recipe table and reported separately as robustness validation.
- No missing required core metrics detected.

## TABLE A - Main Performance
| Exp | Stride | Front F1 | Side F1 | Average Fusion F1 | Adaptive Fusion F1 | Fusion Safe Recall | Fusion Phone Recall |
|---|---|---|---|---|---|---|---|
| Exp1 | 15 | 0.83759 | 0.61415 | 0.81773 | 0.81773 | 0.55263 | 0.98834 |
| Exp2 | 15 | 0.78267 | 0.78792 | 0.83402 | 0.83402 | 0.60526 | 0.98251 |
| Exp3 | 15 | 0.75341 | 0.81679 | 0.82372 | 0.82372 | 0.56579 | 0.98834 |
| Exp4 | 15 | 0.82133 | 0.81210 | 0.85253 | 0.85253 | 0.68421 | 0.97085 |
| Exp5 | 15 | 0.78785 | 0.54586 | 0.79023 | 0.79023 | 0.67105 | 0.91837 |
| Exp6 | 15 | 0.55558 | 0.57932 | 0.60963 | 0.60963 | 0.31579 | 0.88921 |
| Exp7 | 15 | 0.55968 | 0.51949 | 0.59192 | 0.59192 | 0.40789 | 0.80175 |
| Exp8 | 15 | 0.85931 | 0.78012 | 0.87074 | 0.87074 | 0.75000 | 0.96501 |
| Exp9 | 30 | 0.82130 | 0.57174 | 0.78610 | 0.78610 | 0.52500 | 0.97222 |
| Exp10 | 30 | 0.74014 | 0.63333 | 0.76694 | 0.76694 | 0.57500 | 0.93333 |
| Exp11 | 30 | 0.73985 | 0.62625 | 0.76142 | 0.76142 | 0.57500 | 0.92778 |
| Exp12 | 30 | 0.73985 | 0.62625 | 0.76142 | 0.76142 | 0.57500 | 0.92778 |
| Exp13 | 30 | 0.77399 | 0.62023 | 0.78412 | 0.78412 | 0.57500 | 0.95000 |
| Exp14 | 30 | 0.76626 | 0.62023 | 0.78059 | 0.78059 | 0.50000 | 0.97778 |
| Exp15 | 30 | 0.76626 | 0.64349 | 0.77992 | 0.77992 | 0.52500 | 0.96667 |
| Exp16 | 20 | 0.78797 | 0.75905 | 0.78589 | 0.78589 | 0.64407 | 0.92395 |
| Exp17 | 20 | 0.78797 | 0.75905 | 0.78589 | 0.78589 | 0.64407 | 0.92395 |
| Exp18 | 30 | 0.76626 | 0.67468 | 0.81113 | 0.81113 | 0.62500 | 0.95556 |
| Exp19 | 30 | 0.76626 | 0.68372 | 0.79471 | 0.79471 | 0.60000 | 0.95000 |
| Exp20 | 30 | 0.76626 | 0.76019 | 0.77327 | 0.77327 | 0.55000 | 0.95000 |
| Exp21 | 30 | 0.76626 | 0.75067 | 0.79614 | 0.79614 | 0.57500 | 0.96111 |
| Exp22 | 30 | 0.76626 | 0.69915 | 0.80686 | 0.80686 | 0.60000 | 0.96111 |

## TABLE B - Training Stability
| Exp | Front Train F1 | Front Val F1 | Front Gap | Side Train F1 | Side Val F1 | Side Gap |
|---|---|---|---|---|---|---|
| Exp1 | 0.98541 | 0.88682 | 0.09859 | 0.60001 | 0.75748 | -0.15748 |
| Exp2 | 0.99910 | 0.88748 | 0.11162 | 0.96582 | 0.86057 | 0.10524 |
| Exp3 | 0.98037 | 0.84723 | 0.13314 | 0.95571 | 0.79949 | 0.15622 |
| Exp4 | 0.94402 | 0.80977 | 0.13425 | 0.99370 | 0.83752 | 0.15619 |
| Exp5 | 0.83815 | 0.77469 | 0.06346 | 0.56073 | 0.58956 | -0.02883 |
| Exp6 | 0.52106 | 0.63648 | -0.11541 | 0.53961 | 0.62099 | -0.08138 |
| Exp7 | 0.49662 | 0.59678 | -0.10016 | 0.50386 | 0.55419 | -0.05033 |
| Exp8 | 0.91425 | 0.81451 | 0.09973 | 0.93404 | 0.81547 | 0.11857 |
| Exp9 | 0.92316 | 0.78603 | 0.13713 | 0.60526 | 0.69447 | -0.08922 |
| Exp10 | 0.75542 | 0.72688 | 0.02854 | 0.64533 | 0.69447 | -0.04915 |
| Exp11 | 0.74123 | 0.72222 | 0.01901 | 0.65715 | 0.70735 | -0.05020 |
| Exp12 | 0.74123 | 0.71762 | 0.02361 | 0.65715 | 0.70735 | -0.05020 |
| Exp13 | 0.83188 | 0.75562 | 0.07625 | 0.66754 | 0.75000 | -0.08246 |
| Exp14 | 0.69929 | 0.72581 | -0.02652 | 0.66754 | 0.75000 | -0.08246 |
| Exp15 | 0.69929 | 0.72581 | -0.02652 | 0.70212 | 0.74014 | -0.03802 |
| Exp16 | 0.73751 | 0.71443 | 0.02308 | 0.84743 | 0.73807 | 0.10936 |
| Exp17 | 0.73751 | 0.71443 | 0.02308 | 0.84743 | 0.73807 | 0.10936 |
| Exp18 | 0.69929 | 0.72581 | -0.02652 | 0.79013 | 0.68238 | 0.10775 |
| Exp19 | 0.69929 | 0.72581 | -0.02652 | 0.78942 | 0.68238 | 0.10703 |
| Exp20 | 0.69929 | 0.72581 | -0.02652 | 0.92848 | 0.77926 | 0.14922 |
| Exp21 | 0.69929 | 0.72581 | -0.02652 | 0.85309 | 0.71014 | 0.14294 |
| Exp22 | 0.69929 | 0.72581 | -0.02652 | 0.80186 | 0.69447 | 0.10738 |

## TABLE C - Calibration / Ranking Metrics
| Exp | Avg Fusion ROC-AUC | Avg Fusion PR-AUC | Avg Fusion ECE | Avg Fusion Brier | Adaptive ROC-AUC | Adaptive PR-AUC | Adaptive ECE | Adaptive Brier |
|---|---|---|---|---|---|---|---|---|
| Exp1 | 0.92401 | 0.97919 | 0.06113 | 0.07684 | 0.92424 | 0.97927 | 0.05217 | 0.07602 |
| Exp2 | 0.90463 | 0.96989 | 0.06527 | 0.07758 | 0.90483 | 0.96993 | 0.06046 | 0.07723 |
| Exp3 | 0.91399 | 0.97534 | 0.04809 | 0.07273 | 0.91511 | 0.97567 | 0.04270 | 0.07176 |
| Exp4 | 0.92389 | 0.97905 | 0.04259 | 0.06783 | 0.92370 | 0.97903 | 0.03684 | 0.06655 |
| Exp5 | 0.88837 | 0.95848 | 0.23716 | 0.14552 | 0.88994 | 0.95980 | 0.21873 | 0.13960 |
| Exp6 | 0.70619 | 0.89716 | 0.23299 | 0.19265 | 0.70880 | 0.89964 | 0.23044 | 0.19101 |
| Exp7 | 0.65859 | 0.87439 | 0.26734 | 0.21450 | 0.66135 | 0.87666 | 0.26626 | 0.21328 |
| Exp8 | 0.93532 | 0.98248 | 0.15563 | 0.08617 | 0.93356 | 0.98196 | 0.14862 | 0.08390 |
| Exp9 | 0.91736 | 0.97641 | 0.20309 | 0.12405 | 0.92153 | 0.97862 | 0.19102 | 0.11842 |
| Exp10 | 0.87472 | 0.96600 | 0.21822 | 0.14369 | 0.88028 | 0.96818 | 0.21238 | 0.14011 |
| Exp11 | 0.86625 | 0.96173 | 0.20229 | 0.14237 | 0.87097 | 0.96376 | 0.20126 | 0.13936 |
| Exp12 | 0.86681 | 0.96199 | 0.20238 | 0.14240 | 0.87125 | 0.96384 | 0.20135 | 0.13938 |
| Exp13 | 0.89819 | 0.97231 | 0.16611 | 0.11552 | 0.90486 | 0.97553 | 0.15513 | 0.11071 |
| Exp14 | 0.86556 | 0.96293 | 0.19662 | 0.12980 | 0.87056 | 0.96530 | 0.18907 | 0.12646 |
| Exp15 | 0.86986 | 0.96449 | 0.16435 | 0.11971 | 0.87208 | 0.96549 | 0.15824 | 0.11725 |
| Exp16 | 0.88013 | 0.96387 | 0.13519 | 0.10988 | 0.87414 | 0.96152 | 0.13074 | 0.10814 |
| Exp17 | 0.88013 | 0.96387 | 0.13519 | 0.10988 | 0.87414 | 0.96152 | 0.13074 | 0.10814 |
| Exp18 | 0.86292 | 0.96236 | 0.17916 | 0.12341 | 0.86500 | 0.96329 | 0.17159 | 0.12028 |
| Exp19 | 0.86306 | 0.96256 | 0.16697 | 0.12193 | 0.86514 | 0.96332 | 0.15947 | 0.11893 |
| Exp20 | 0.88569 | 0.97100 | 0.10761 | 0.09905 | 0.88625 | 0.97124 | 0.09990 | 0.09672 |
| Exp21 | 0.86847 | 0.96489 | 0.13403 | 0.10924 | 0.86972 | 0.96557 | 0.12580 | 0.10692 |
| Exp22 | 0.86333 | 0.96301 | 0.15619 | 0.11569 | 0.86639 | 0.96415 | 0.14869 | 0.11296 |

## TABLE D - Recipe Overview
| Exp | Stride | Front LR | Front WD | Front Dropout | Front Freeze | Front Rotation | Front Jitter | Side LR | Side WD | Side Dropout | Side Freeze | Side Rotation | Side Jitter | Side Monitor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exp1 | 15 | 0.00010 | 0.00000 | 0.30000 | 0 | NA | NA | 0.00010 | 0.00000 | 0.30000 | 0 | NA | NA | val_macro_f1 |
| Exp2 | 15 | 0.00010 | 0.00010 | 0.30000 | 4 | 10 | 0.20000 | 0.00010 | 0.00010 | 0.30000 | 4 | 10 | 0.20000 | val_macro_f1 |
| Exp3 | 15 | 0.00005 | 0.00010 | 0.30000 | 2 | 10 | 0.20000 | 0.00005 | 0.00010 | 0.30000 | 2 | 10 | 0.20000 | val_macro_f1 |
| Exp4 | 15 | 0.00005 | 0.00050 | 0.50000 | 4 | 15 | 0.30000 | 0.00005 | 0.00050 | 0.50000 | 4 | 15 | 0.30000 | val_macro_f1 |
| Exp5 | 15 | 0.00001 | 0.00050 | 0.50000 | 4 | 15 | 0.30000 | 0.00001 | 0.00050 | 0.50000 | 4 | 15 | 0.30000 | val_macro_f1 |
| Exp6 | 15 | 0.00001 | 0.00100 | 0.60000 | 5 | 20 | 0.40000 | 0.00001 | 0.00100 | 0.60000 | 5 | 20 | 0.40000 | val_macro_f1 |
| Exp7 | 15 | 0.00001 | 0.01000 | 0.60000 | 5 | 20 | 0.40000 | 0.00001 | 0.01000 | 0.60000 | 3 | 20 | 0.40000 | val_macro_f1 |
| Exp8 | 15 | 0.00005 | 0.00050 | 0.50000 | 4 | 20 | 0.40000 | 0.00002 | 0.00050 | 0.50000 | 3 | 20 | 0.40000 | val_macro_f1 |
| Exp9 | 30 | 0.00005 | 0.00050 | 0.50000 | 4 | 20 | 0.40000 | 0.00002 | 0.00050 | 0.50000 | 3 | 20 | 0.40000 | val_macro_f1 |
| Exp10 | 30 | 0.00003 | 0.00200 | 0.50000 | 5 | 45 | 0.60000 | 0.00002 | 0.00200 | 0.50000 | 4 | 45 | 0.60000 | val_macro_f1 |
| Exp11 | 30 | 0.00003 | 0.00200 | 0.50000 | 5 | 45 | 0.80000 | 0.00002 | 0.00200 | 0.30000 | 4 | 45 | 0.80000 | val_macro_f1 |
| Exp12 | 30 | 0.00003 | 0.01000 | 0.50000 | 5 | 45 | 0.80000 | 0.00002 | 0.01000 | 0.30000 | 4 | 45 | 0.80000 | val_macro_f1 |
| Exp13 | 30 | 0.00003 | 0.00200 | 0.50000 | 5 | 45 | 0.80000 | 0.00002 | 0.00200 | 0.30000 | 4 | 45 | 0.80000 | val_macro_f1 |
| Exp14 | 30 | 0.00003 | 0.00030 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00200 | 0.30000 | 4 | 45 | 0.80000 | val_macro_f1 |
| Exp15 | 30 | 0.00003 | 0.00030 | 0.40000 | 5 | 68 | 1.20000 | 0.00003 | 0.00010 | 0.30000 | 4 | 45 | 0.80000 | val_macro_f1 |
| Exp16 | 20 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00050 | 0.30000 | 4 | 45 | 0.80000 | val_loss |
| Exp17 | 20 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00050 | 0.30000 | 4 | 45 | 0.80000 | val_loss |
| Exp18 | 30 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00100 | 0.40000 | 4 | 45 | 0.80000 | val_loss |
| Exp19 | 30 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00100 | 0.30000 | 4 | 45 | 0.80000 | val_loss |
| Exp20 | 30 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00100 | 0.40000 | 4 | 20 | 0.40000 | val_loss |
| Exp21 | 30 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00100 | 0.40000 | 4 | 30 | 0.60000 | val_loss |
| Exp22 | 30 | 0.00003 | 0.00050 | 0.40000 | 5 | 68 | 1.20000 | 0.00002 | 0.00100 | 0.40000 | 4 | 35 | 0.70000 | val_loss |

## Rankings

Warning: cross-stride rankings compare different sample counts/protocol sizes, so absolute comparisons are not fully apples-to-apples.

### A. Best Average Fusion Macro F1

| Rank | Exp | Stride | Average Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.87074 |
| 2 | Exp4 | 15 | 0.85253 |
| 3 | Exp2 | 15 | 0.83402 |
| 4 | Exp3 | 15 | 0.82372 |
| 5 | Exp1 | 15 | 0.81773 |
| 6 | Exp18 | 30 | 0.81113 |
| 7 | Exp22 | 30 | 0.80686 |
| 8 | Exp21 | 30 | 0.79614 |
| 9 | Exp19 | 30 | 0.79471 |
| 10 | Exp5 | 15 | 0.79023 |

### B. Best Adaptive Fusion Macro F1

| Rank | Exp | Stride | Adaptive Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.87074 |
| 2 | Exp4 | 15 | 0.85253 |
| 3 | Exp2 | 15 | 0.83402 |
| 4 | Exp3 | 15 | 0.82372 |
| 5 | Exp1 | 15 | 0.81773 |
| 6 | Exp18 | 30 | 0.81113 |
| 7 | Exp22 | 30 | 0.80686 |
| 8 | Exp21 | 30 | 0.79614 |
| 9 | Exp19 | 30 | 0.79471 |
| 10 | Exp5 | 15 | 0.79023 |

### C. Best Front Macro F1

| Rank | Exp | Stride | Front Test macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.85931 |
| 2 | Exp1 | 15 | 0.83759 |
| 3 | Exp4 | 15 | 0.82133 |
| 4 | Exp9 | 30 | 0.82130 |
| 5 | Exp16 | 20 | 0.78797 |
| 6 | Exp17 | 20 | 0.78797 |
| 7 | Exp5 | 15 | 0.78785 |
| 8 | Exp2 | 15 | 0.78267 |
| 9 | Exp13 | 30 | 0.77399 |
| 10 | Exp14 | 30 | 0.76626 |

### D. Best Side Macro F1

| Rank | Exp | Stride | Side Test macro_f1 |
|---|---|---|---|
| 1 | Exp3 | 15 | 0.81679 |
| 2 | Exp4 | 15 | 0.81210 |
| 3 | Exp2 | 15 | 0.78792 |
| 4 | Exp8 | 15 | 0.78012 |
| 5 | Exp20 | 30 | 0.76019 |
| 6 | Exp16 | 20 | 0.75905 |
| 7 | Exp17 | 20 | 0.75905 |
| 8 | Exp21 | 30 | 0.75067 |
| 9 | Exp22 | 30 | 0.69915 |
| 10 | Exp19 | 30 | 0.68372 |

### E. Best Fusion Safe Recall

| Rank | Exp | Stride | Average Fusion safe_recall |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.75000 |
| 2 | Exp4 | 15 | 0.68421 |
| 3 | Exp5 | 15 | 0.67105 |
| 4 | Exp16 | 20 | 0.64407 |
| 5 | Exp17 | 20 | 0.64407 |
| 6 | Exp18 | 30 | 0.62500 |
| 7 | Exp2 | 15 | 0.60526 |
| 8 | Exp19 | 30 | 0.60000 |
| 9 | Exp22 | 30 | 0.60000 |
| 10 | Exp10 | 30 | 0.57500 |

### F. Best Fusion Phone Recall

| Rank | Exp | Stride | Average Fusion phone_recall |
|---|---|---|---|
| 1 | Exp1 | 15 | 0.98834 |
| 2 | Exp3 | 15 | 0.98834 |
| 3 | Exp2 | 15 | 0.98251 |
| 4 | Exp14 | 30 | 0.97778 |
| 5 | Exp9 | 30 | 0.97222 |
| 6 | Exp4 | 15 | 0.97085 |
| 7 | Exp15 | 30 | 0.96667 |
| 8 | Exp8 | 15 | 0.96501 |
| 9 | Exp21 | 30 | 0.96111 |
| 10 | Exp22 | 30 | 0.96111 |

### G. Best ROC-AUC

| Rank | Exp | Stride | Average Fusion roc_auc |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.93532 |
| 2 | Exp1 | 15 | 0.92401 |
| 3 | Exp4 | 15 | 0.92389 |
| 4 | Exp9 | 30 | 0.91736 |
| 5 | Exp3 | 15 | 0.91399 |
| 6 | Exp2 | 15 | 0.90463 |
| 7 | Exp13 | 30 | 0.89819 |
| 8 | Exp5 | 15 | 0.88837 |
| 9 | Exp20 | 30 | 0.88569 |
| 10 | Exp16 | 20 | 0.88013 |

### H. Best PR-AUC

| Rank | Exp | Stride | Average Fusion pr_auc |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.98248 |
| 2 | Exp1 | 15 | 0.97919 |
| 3 | Exp4 | 15 | 0.97905 |
| 4 | Exp9 | 30 | 0.97641 |
| 5 | Exp3 | 15 | 0.97534 |
| 6 | Exp13 | 30 | 0.97231 |
| 7 | Exp20 | 30 | 0.97100 |
| 8 | Exp2 | 15 | 0.96989 |
| 9 | Exp10 | 30 | 0.96600 |
| 10 | Exp21 | 30 | 0.96489 |

### I. Lowest ECE

| Rank | Exp | Stride | Average Fusion ece |
|---|---|---|---|
| 1 | Exp4 | 15 | 0.04259 |
| 2 | Exp3 | 15 | 0.04809 |
| 3 | Exp1 | 15 | 0.06113 |
| 4 | Exp2 | 15 | 0.06527 |
| 5 | Exp20 | 30 | 0.10761 |
| 6 | Exp21 | 30 | 0.13403 |
| 7 | Exp16 | 20 | 0.13519 |
| 8 | Exp17 | 20 | 0.13519 |
| 9 | Exp8 | 15 | 0.15563 |
| 10 | Exp22 | 30 | 0.15619 |

### J. Lowest Brier

| Rank | Exp | Stride | Average Fusion brier |
|---|---|---|---|
| 1 | Exp4 | 15 | 0.06783 |
| 2 | Exp3 | 15 | 0.07273 |
| 3 | Exp1 | 15 | 0.07684 |
| 4 | Exp2 | 15 | 0.07758 |
| 5 | Exp8 | 15 | 0.08617 |
| 6 | Exp20 | 30 | 0.09905 |
| 7 | Exp21 | 30 | 0.10924 |
| 8 | Exp16 | 20 | 0.10988 |
| 9 | Exp17 | 20 | 0.10988 |
| 10 | Exp13 | 30 | 0.11552 |

## Stride-Specific Rankings

### Stride 15

### Best Average Fusion F1

| Rank | Exp | Stride | Average Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.87074 |
| 2 | Exp4 | 15 | 0.85253 |
| 3 | Exp2 | 15 | 0.83402 |
| 4 | Exp3 | 15 | 0.82372 |
| 5 | Exp1 | 15 | 0.81773 |

### Best Adaptive Fusion F1

| Rank | Exp | Stride | Adaptive Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.87074 |
| 2 | Exp4 | 15 | 0.85253 |
| 3 | Exp2 | 15 | 0.83402 |
| 4 | Exp3 | 15 | 0.82372 |
| 5 | Exp1 | 15 | 0.81773 |

### Best Front F1

| Rank | Exp | Stride | Front Test macro_f1 |
|---|---|---|---|
| 1 | Exp8 | 15 | 0.85931 |
| 2 | Exp1 | 15 | 0.83759 |
| 3 | Exp4 | 15 | 0.82133 |
| 4 | Exp5 | 15 | 0.78785 |
| 5 | Exp2 | 15 | 0.78267 |

### Best Side F1

| Rank | Exp | Stride | Side Test macro_f1 |
|---|---|---|---|
| 1 | Exp3 | 15 | 0.81679 |
| 2 | Exp4 | 15 | 0.81210 |
| 3 | Exp2 | 15 | 0.78792 |
| 4 | Exp8 | 15 | 0.78012 |
| 5 | Exp1 | 15 | 0.61415 |

### Stride 20

### Best Average Fusion F1

| Rank | Exp | Stride | Average Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp16 | 20 | 0.78589 |
| 2 | Exp17 | 20 | 0.78589 |

### Best Adaptive Fusion F1

| Rank | Exp | Stride | Adaptive Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp16 | 20 | 0.78589 |
| 2 | Exp17 | 20 | 0.78589 |

### Best Front F1

| Rank | Exp | Stride | Front Test macro_f1 |
|---|---|---|---|
| 1 | Exp16 | 20 | 0.78797 |
| 2 | Exp17 | 20 | 0.78797 |

### Best Side F1

| Rank | Exp | Stride | Side Test macro_f1 |
|---|---|---|---|
| 1 | Exp16 | 20 | 0.75905 |
| 2 | Exp17 | 20 | 0.75905 |

### Stride 30

### Best Average Fusion F1

| Rank | Exp | Stride | Average Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp18 | 30 | 0.81113 |
| 2 | Exp22 | 30 | 0.80686 |
| 3 | Exp21 | 30 | 0.79614 |
| 4 | Exp19 | 30 | 0.79471 |
| 5 | Exp9 | 30 | 0.78610 |

### Best Adaptive Fusion F1

| Rank | Exp | Stride | Adaptive Fusion macro_f1 |
|---|---|---|---|
| 1 | Exp18 | 30 | 0.81113 |
| 2 | Exp22 | 30 | 0.80686 |
| 3 | Exp21 | 30 | 0.79614 |
| 4 | Exp19 | 30 | 0.79471 |
| 5 | Exp9 | 30 | 0.78610 |

### Best Front F1

| Rank | Exp | Stride | Front Test macro_f1 |
|---|---|---|---|
| 1 | Exp9 | 30 | 0.82130 |
| 2 | Exp13 | 30 | 0.77399 |
| 3 | Exp14 | 30 | 0.76626 |
| 4 | Exp15 | 30 | 0.76626 |
| 5 | Exp18 | 30 | 0.76626 |

### Best Side F1

| Rank | Exp | Stride | Side Test macro_f1 |
|---|---|---|---|
| 1 | Exp20 | 30 | 0.76019 |
| 2 | Exp21 | 30 | 0.75067 |
| 3 | Exp22 | 30 | 0.69915 |
| 4 | Exp19 | 30 | 0.68372 |
| 5 | Exp18 | 30 | 0.67468 |

## Final Stride-30 Table

| Exp | Front F1 | Side F1 | Average Fusion F1 | Adaptive Fusion F1 | Fusion Safe Recall | Fusion Phone Recall | ROC-AUC | PR-AUC | ECE | Brier | Front Gap | Side Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exp9 | 0.82130 | 0.57174 | 0.78610 | 0.78610 | 0.52500 | 0.97222 | 0.91736 | 0.97641 | 0.20309 | 0.12405 | 0.13713 | -0.08922 |
| Exp10 | 0.74014 | 0.63333 | 0.76694 | 0.76694 | 0.57500 | 0.93333 | 0.87472 | 0.96600 | 0.21822 | 0.14369 | 0.02854 | -0.04915 |
| Exp11 | 0.73985 | 0.62625 | 0.76142 | 0.76142 | 0.57500 | 0.92778 | 0.86625 | 0.96173 | 0.20229 | 0.14237 | 0.01901 | -0.05020 |
| Exp12 | 0.73985 | 0.62625 | 0.76142 | 0.76142 | 0.57500 | 0.92778 | 0.86681 | 0.96199 | 0.20238 | 0.14240 | 0.02361 | -0.05020 |
| Exp13 | 0.77399 | 0.62023 | 0.78412 | 0.78412 | 0.57500 | 0.95000 | 0.89819 | 0.97231 | 0.16611 | 0.11552 | 0.07625 | -0.08246 |
| Exp14 | 0.76626 | 0.62023 | 0.78059 | 0.78059 | 0.50000 | 0.97778 | 0.86556 | 0.96293 | 0.19662 | 0.12980 | -0.02652 | -0.08246 |
| Exp15 | 0.76626 | 0.64349 | 0.77992 | 0.77992 | 0.52500 | 0.96667 | 0.86986 | 0.96449 | 0.16435 | 0.11971 | -0.02652 | -0.03802 |
| Exp18 | 0.76626 | 0.67468 | 0.81113 | 0.81113 | 0.62500 | 0.95556 | 0.86292 | 0.96236 | 0.17916 | 0.12341 | -0.02652 | 0.10775 |
| Exp19 | 0.76626 | 0.68372 | 0.79471 | 0.79471 | 0.60000 | 0.95000 | 0.86306 | 0.96256 | 0.16697 | 0.12193 | -0.02652 | 0.10703 |
| Exp20 | 0.76626 | 0.76019 | 0.77327 | 0.77327 | 0.55000 | 0.95000 | 0.88569 | 0.97100 | 0.10761 | 0.09905 | -0.02652 | 0.14922 |
| Exp21 | 0.76626 | 0.75067 | 0.79614 | 0.79614 | 0.57500 | 0.96111 | 0.86847 | 0.96489 | 0.13403 | 0.10924 | -0.02652 | 0.14294 |
| Exp22 | 0.76626 | 0.69915 | 0.80686 | 0.80686 | 0.60000 | 0.96111 | 0.86333 | 0.96301 | 0.15619 | 0.11569 | -0.02652 | 0.10738 |
- Stride-30 best Front: Exp9 (0.82130).
- Stride-30 best Side: Exp20 (0.76019).
- Stride-30 best Fusion: Exp18 (0.81113).

## Exp18 / Exp20 / Exp21 / Exp22 Ablation

| Metric | Exp18 | Exp22 | Exp21 | Exp20 Final |
|---|---|---|---|---|
| Side augmentation rotation | 45 | 35 | 30 | 20 |
| Side color jitter | 0.80000 | 0.70000 | 0.60000 | 0.40000 |
| Side Train F1 | 0.79013 | 0.80186 | 0.85309 | 0.92848 |
| Side Val F1 | 0.68238 | 0.69447 | 0.71014 | 0.77926 |
| Side gap | 0.10775 | 0.10738 | 0.14294 | 0.14922 |
| Side Test F1 | 0.67468 | 0.69915 | 0.75067 | 0.76019 |
| Side Safe Recall | 0.47500 | 0.50000 | 0.57500 | 0.62500 |
| Side Phone Recall | 0.87778 | 0.89444 | 0.91667 | 0.90556 |
| Average Fusion F1 | 0.81113 | 0.80686 | 0.79614 | 0.77327 |
| Adaptive Fusion F1 | 0.81113 | 0.80686 | 0.79614 | 0.77327 |
| Fusion Safe Recall | 0.62500 | 0.60000 | 0.57500 | 0.55000 |
| Fusion Phone Recall | 0.95556 | 0.96111 | 0.96111 | 0.95000 |
| ROC-AUC | 0.86292 | 0.86333 | 0.86847 | 0.88569 |
| PR-AUC | 0.96236 | 0.96301 | 0.96489 | 0.97100 |
| ECE | 0.17916 | 0.15619 | 0.13403 | 0.10761 |
| Brier | 0.12341 | 0.11569 | 0.10924 | 0.09905 |

Descriptive note: lighter Side augmentation improved Side standalone metrics in Exp20/Exp21, but fusion Macro F1 remained strongest in Exp18. Exp22 moved closer to Exp18 fusion behavior but did not surpass Exp18.

## Exp23 Robustness Note

Selected recipe: experiment_18. Exp23 seed43/44 are robustness repeats, not new recipe experiments.
- Front Macro F1: seed42=0.76626, seed43=0.72049, seed44=0.75940, mean=0.74872, std=0.02468.
- Side Macro F1: seed42=0.67468, seed43=0.66353, seed44=0.70213, mean=0.68011, std=0.01987.
- Average Fusion Macro F1: seed42=0.81113, seed43=0.74028, seed44=0.76626, mean=0.77256, std=0.03584.
- Adaptive Fusion Macro F1: seed42=0.81113, seed43=0.74028, seed44=0.76626, mean=0.77256, std=0.03584.
- Ranking Fusion > Front > Side remained consistent across all three seeds, but absolute performance showed moderate seed sensitivity.

## Compact Reproducibility Summary

Exp1: stride=15, Front F1=0.83759, Side F1=0.61415, Avg Fusion F1=0.81773, Adaptive Fusion F1=0.81773, Fusion Safe Recall=0.55263, Fusion Phone Recall=0.98834, Front Gap=0.09859, Side Gap=-0.15748, ROC-AUC=0.92401, PR-AUC=0.97919, ECE=0.06113, Brier=0.07684.
Exp2: stride=15, Front F1=0.78267, Side F1=0.78792, Avg Fusion F1=0.83402, Adaptive Fusion F1=0.83402, Fusion Safe Recall=0.60526, Fusion Phone Recall=0.98251, Front Gap=0.11162, Side Gap=0.10524, ROC-AUC=0.90463, PR-AUC=0.96989, ECE=0.06527, Brier=0.07758.
Exp3: stride=15, Front F1=0.75341, Side F1=0.81679, Avg Fusion F1=0.82372, Adaptive Fusion F1=0.82372, Fusion Safe Recall=0.56579, Fusion Phone Recall=0.98834, Front Gap=0.13314, Side Gap=0.15622, ROC-AUC=0.91399, PR-AUC=0.97534, ECE=0.04809, Brier=0.07273.
Exp4: stride=15, Front F1=0.82133, Side F1=0.81210, Avg Fusion F1=0.85253, Adaptive Fusion F1=0.85253, Fusion Safe Recall=0.68421, Fusion Phone Recall=0.97085, Front Gap=0.13425, Side Gap=0.15619, ROC-AUC=0.92389, PR-AUC=0.97905, ECE=0.04259, Brier=0.06783.
Exp5: stride=15, Front F1=0.78785, Side F1=0.54586, Avg Fusion F1=0.79023, Adaptive Fusion F1=0.79023, Fusion Safe Recall=0.67105, Fusion Phone Recall=0.91837, Front Gap=0.06346, Side Gap=-0.02883, ROC-AUC=0.88837, PR-AUC=0.95848, ECE=0.23716, Brier=0.14552.
Exp6: stride=15, Front F1=0.55558, Side F1=0.57932, Avg Fusion F1=0.60963, Adaptive Fusion F1=0.60963, Fusion Safe Recall=0.31579, Fusion Phone Recall=0.88921, Front Gap=-0.11541, Side Gap=-0.08138, ROC-AUC=0.70619, PR-AUC=0.89716, ECE=0.23299, Brier=0.19265.
Exp7: stride=15, Front F1=0.55968, Side F1=0.51949, Avg Fusion F1=0.59192, Adaptive Fusion F1=0.59192, Fusion Safe Recall=0.40789, Fusion Phone Recall=0.80175, Front Gap=-0.10016, Side Gap=-0.05033, ROC-AUC=0.65859, PR-AUC=0.87439, ECE=0.26734, Brier=0.21450.
Exp8: stride=15, Front F1=0.85931, Side F1=0.78012, Avg Fusion F1=0.87074, Adaptive Fusion F1=0.87074, Fusion Safe Recall=0.75000, Fusion Phone Recall=0.96501, Front Gap=0.09973, Side Gap=0.11857, ROC-AUC=0.93532, PR-AUC=0.98248, ECE=0.15563, Brier=0.08617.
Exp9: stride=30, Front F1=0.82130, Side F1=0.57174, Avg Fusion F1=0.78610, Adaptive Fusion F1=0.78610, Fusion Safe Recall=0.52500, Fusion Phone Recall=0.97222, Front Gap=0.13713, Side Gap=-0.08922, ROC-AUC=0.91736, PR-AUC=0.97641, ECE=0.20309, Brier=0.12405.
Exp10: stride=30, Front F1=0.74014, Side F1=0.63333, Avg Fusion F1=0.76694, Adaptive Fusion F1=0.76694, Fusion Safe Recall=0.57500, Fusion Phone Recall=0.93333, Front Gap=0.02854, Side Gap=-0.04915, ROC-AUC=0.87472, PR-AUC=0.96600, ECE=0.21822, Brier=0.14369.
Exp11: stride=30, Front F1=0.73985, Side F1=0.62625, Avg Fusion F1=0.76142, Adaptive Fusion F1=0.76142, Fusion Safe Recall=0.57500, Fusion Phone Recall=0.92778, Front Gap=0.01901, Side Gap=-0.05020, ROC-AUC=0.86625, PR-AUC=0.96173, ECE=0.20229, Brier=0.14237.
Exp12: stride=30, Front F1=0.73985, Side F1=0.62625, Avg Fusion F1=0.76142, Adaptive Fusion F1=0.76142, Fusion Safe Recall=0.57500, Fusion Phone Recall=0.92778, Front Gap=0.02361, Side Gap=-0.05020, ROC-AUC=0.86681, PR-AUC=0.96199, ECE=0.20238, Brier=0.14240.
Exp13: stride=30, Front F1=0.77399, Side F1=0.62023, Avg Fusion F1=0.78412, Adaptive Fusion F1=0.78412, Fusion Safe Recall=0.57500, Fusion Phone Recall=0.95000, Front Gap=0.07625, Side Gap=-0.08246, ROC-AUC=0.89819, PR-AUC=0.97231, ECE=0.16611, Brier=0.11552.
Exp14: stride=30, Front F1=0.76626, Side F1=0.62023, Avg Fusion F1=0.78059, Adaptive Fusion F1=0.78059, Fusion Safe Recall=0.50000, Fusion Phone Recall=0.97778, Front Gap=-0.02652, Side Gap=-0.08246, ROC-AUC=0.86556, PR-AUC=0.96293, ECE=0.19662, Brier=0.12980.
Exp15: stride=30, Front F1=0.76626, Side F1=0.64349, Avg Fusion F1=0.77992, Adaptive Fusion F1=0.77992, Fusion Safe Recall=0.52500, Fusion Phone Recall=0.96667, Front Gap=-0.02652, Side Gap=-0.03802, ROC-AUC=0.86986, PR-AUC=0.96449, ECE=0.16435, Brier=0.11971.
Exp16: stride=20, Front F1=0.78797, Side F1=0.75905, Avg Fusion F1=0.78589, Adaptive Fusion F1=0.78589, Fusion Safe Recall=0.64407, Fusion Phone Recall=0.92395, Front Gap=0.02308, Side Gap=0.10936, ROC-AUC=0.88013, PR-AUC=0.96387, ECE=0.13519, Brier=0.10988.
Exp17: stride=20, Front F1=0.78797, Side F1=0.75905, Avg Fusion F1=0.78589, Adaptive Fusion F1=0.78589, Fusion Safe Recall=0.64407, Fusion Phone Recall=0.92395, Front Gap=0.02308, Side Gap=0.10936, ROC-AUC=0.88013, PR-AUC=0.96387, ECE=0.13519, Brier=0.10988.
Exp18: stride=30, Front F1=0.76626, Side F1=0.67468, Avg Fusion F1=0.81113, Adaptive Fusion F1=0.81113, Fusion Safe Recall=0.62500, Fusion Phone Recall=0.95556, Front Gap=-0.02652, Side Gap=0.10775, ROC-AUC=0.86292, PR-AUC=0.96236, ECE=0.17916, Brier=0.12341.
Exp19: stride=30, Front F1=0.76626, Side F1=0.68372, Avg Fusion F1=0.79471, Adaptive Fusion F1=0.79471, Fusion Safe Recall=0.60000, Fusion Phone Recall=0.95000, Front Gap=-0.02652, Side Gap=0.10703, ROC-AUC=0.86306, PR-AUC=0.96256, ECE=0.16697, Brier=0.12193.
Exp20: stride=30, Front F1=0.76626, Side F1=0.76019, Avg Fusion F1=0.77327, Adaptive Fusion F1=0.77327, Fusion Safe Recall=0.55000, Fusion Phone Recall=0.95000, Front Gap=-0.02652, Side Gap=0.14922, ROC-AUC=0.88569, PR-AUC=0.97100, ECE=0.10761, Brier=0.09905.
Exp21: stride=30, Front F1=0.76626, Side F1=0.75067, Avg Fusion F1=0.79614, Adaptive Fusion F1=0.79614, Fusion Safe Recall=0.57500, Fusion Phone Recall=0.96111, Front Gap=-0.02652, Side Gap=0.14294, ROC-AUC=0.86847, PR-AUC=0.96489, ECE=0.13403, Brier=0.10924.
Exp22: stride=30, Front F1=0.76626, Side F1=0.69915, Avg Fusion F1=0.80686, Adaptive Fusion F1=0.80686, Fusion Safe Recall=0.60000, Fusion Phone Recall=0.96111, Front Gap=-0.02652, Side Gap=0.10738, ROC-AUC=0.86333, PR-AUC=0.96301, ECE=0.15619, Brier=0.11569.
Best stride-15 by Average Fusion Macro F1: Exp8 = 0.87074.
Best stride-20 by Average Fusion Macro F1: Exp16 = 0.78589.
Best stride-30 by Average Fusion Macro F1: Exp18 = 0.81113.
Overall max by Average Fusion Macro F1: Exp8 stride=15 value=0.87074; caveat: cross-stride sample counts differ, so not fully apples-to-apples.
Exp18/20/21/22 ablation summary: Exp18 fusion F1=0.81113 remains strongest; Exp22 fusion F1=0.80686 is closest among later Side augmentation refinements; Exp21 fusion F1=0.79614; Exp20 final fusion F1=0.77327. Side standalone improves under lighter augmentation but fusion complementarity can drop.
Exp23 robustness summary: Average Fusion seed42=0.81113, seed43=0.74028, seed44=0.76626, mean=0.77256, std=0.03584; Front mean=0.74872 +/- 0.02468; Side mean=0.68011 +/- 0.01987; verdict=moderate seed sensitivity with stable Fusion > Front > Side ranking.

