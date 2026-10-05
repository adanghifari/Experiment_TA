# Deep audit — Experiment 18 model-selection protocols

## 1. Scope

Authoritative root: `D:\Skripsi\Experiment_TA`. The historical repository `D:\Skripsi\Experiment` was not accessed. This audit is read-only with respect to experiment inputs: no retraining, inference, source modification, checkpoint modification, manuscript modification, or Git commit was performed.

All numerical comparisons use verified existing prediction CSVs or deterministic recomputation from those CSVs. New files created by this audit are confined to `paper_audit`.

## 2. Artifact verification

| protocol | label | status | folder | resolved_config | fusion_predictions | fusion_metrics | front_history | front_summary | front_checkpoint | side_history | side_summary | side_checkpoint | front_checkpoint_path | front_checkpoint_exists | front_checkpoint_sha_match | side_checkpoint_path | side_checkpoint_exists | side_checkpoint_sha_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | VERIFIED | True | True | True | True | True | True | True | True | True | True | D:\Skripsi\Experiment_TA\experiment_18\checkpoints\front\best.pt | True | True | D:\Skripsi\Experiment_TA\experiment_18\checkpoints\side\best.pt | True | True |
| P2 | 18_checkpoint_val_macro_f1 | VERIFIED | True | True | True | True | True | True | True | True | True | True | D:\Skripsi\Experiment_TA\experiment_18_standardized_checkpoint_selection\checkpoints\front\best.pt | True | True | D:\Skripsi\Experiment_TA\experiment_18_standardized_checkpoint_selection\checkpoints\side\best.pt | True | True |
| P3 | 18_checkpoint_val_loss | VERIFIED | True | True | True | True | True | True | True | True | True | True | D:\Skripsi\Experiment_TA\experiment_18_standardized_checkpoint_val_loss\checkpoints\standardized_val_loss\front\best.pt | True | True | D:\Skripsi\Experiment_TA\experiment_18_standardized_checkpoint_val_loss\checkpoints\standardized_val_loss\side\best.pt | True | True |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | VERIFIED | True | True | True | True | True | True | True | True | True | True | D:\Skripsi\Experiment_TA\experiment_18_full_standardized_macro_f1\checkpoints\full_standardized_macro_f1\front\best.pt | True | True | D:\Skripsi\Experiment_TA\experiment_18_full_standardized_macro_f1\checkpoints\full_standardized_macro_f1\side\best.pt | True | True |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | VERIFIED | True | True | True | True | True | True | True | True | True | True | D:\Skripsi\Experiment_TA\experiment_18_full_standardized_val_loss\checkpoints\full_standardized_val_loss\front\best.pt | True | True | D:\Skripsi\Experiment_TA\experiment_18_full_standardized_val_loss\checkpoints\full_standardized_val_loss\side\best.pt | True | True |

Interpretation of verification: a protocol is used in numerical comparison only when its prediction CSV, fusion metrics, config, histories, summaries, and physical checkpoint metadata are present and aligned. Original P1 early-stopping fields are absent from its summary JSON; the exact original training source ties early stopping to the same score/mode as checkpoint selection, so that field is marked source-inferred rather than summary-recorded.

## 3. Protocol definitions

- **P1 — 18_original_mixed_reference**: Front checkpoint/early stopping val_macro_f1/max; Side checkpoint/early stopping val_loss/min.
- **P2 — 18_checkpoint_val_macro_f1**: Both checkpoints val_macro_f1/max; Front early stopping val_macro_f1/max; Side early stopping val_loss/min.
- **P3 — 18_checkpoint_val_loss**: Both checkpoints val_loss/min; Front early stopping val_macro_f1/max; Side early stopping val_loss/min.
- **P4 — 18_checkpoint_val_macro_f1_and_earlystopping_val_macro**: Both checkpoints and early stopping val_macro_f1/max; patience Front=4, Side=5.
- **P5 — 18_checkpoint_val_loss_and_earlystopping_val_loss**: Both checkpoints and early stopping val_loss/min; patience Front=4, Side=5.

## 4. Training-health comparison

| Protocol | View | Selected epoch | Executed | Checkpoint | Early stop | Train loss | Val loss | Loss gap | Train F1 | Val F1 | F1 gap | LR | Min val loss | Max val F1 | Min/mean/max gap | Final gap | Health |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | front | 9 | 13 | val_macro_f1/max | val_macro_f1/max (p=4) | 0.47353 | 0.51736 | 0.04383 | 0.69929 | 0.72581 | -0.02652 | 0.00003 | 0.50961 (e12) | 0.72581 (e9) | -0.05602/0.04410/0.13310 | 0.13310 | POSSIBLE GENERALIZATION GAP |
| P1 | side | 26 | 30 | val_loss/min | val_loss/min (p=5) | 0.39480 | 0.50217 | 0.10738 | 0.79013 | 0.68238 | 0.10775 | 0.00000 | 0.50217 (e26) | 0.75724 (e15) | -0.06799/0.04820/0.11361 | 0.10480 | POSSIBLE GENERALIZATION GAP |
| P2 | front | 9 | 13 | val_macro_f1/max | val_macro_f1/max (p=4) | 0.47353 | 0.51736 | 0.04383 | 0.69929 | 0.72581 | -0.02652 | 0.00003 | 0.50961 (e12) | 0.72581 (e9) | -0.05602/0.04410/0.13310 | 0.13310 | POSSIBLE GENERALIZATION GAP |
| P2 | side | 15 | 30 | val_macro_f1/max | val_loss/min (p=5) | 0.48501 | 0.53991 | 0.05490 | 0.70578 | 0.75724 | -0.05147 | 0.00001 | 0.50217 (e26) | 0.75724 (e15) | -0.06799/0.04820/0.11361 | 0.10480 | POSSIBLE OVERFITTING SIGNAL |
| P3 | front | 12 | 13 | val_loss/min | val_macro_f1/max (p=4) | 0.41722 | 0.50961 | 0.09239 | 0.76318 | 0.71892 | 0.04427 | 0.00002 | 0.50961 (e12) | 0.72581 (e9) | -0.05602/0.04410/0.13310 | 0.13310 | POSSIBLE GENERALIZATION GAP |
| P3 | side | 26 | 30 | val_loss/min | val_loss/min (p=5) | 0.39480 | 0.50217 | 0.10738 | 0.79013 | 0.68238 | 0.10775 | 0.00000 | 0.50217 (e26) | 0.75724 (e15) | -0.06799/0.04820/0.11361 | 0.10480 | POSSIBLE GENERALIZATION GAP |
| P4 | front | 9 | 13 | val_macro_f1/max | val_macro_f1/max (p=4) | 0.47353 | 0.51736 | 0.04383 | 0.69929 | 0.72581 | -0.02652 | 0.00003 | 0.50961 (e12) | 0.72581 (e9) | -0.05602/0.04410/0.13310 | 0.13310 | POSSIBLE GENERALIZATION GAP |
| P4 | side | 15 | 20 | val_macro_f1/max | val_macro_f1/max (p=5) | 0.48501 | 0.53991 | 0.05490 | 0.70578 | 0.75724 | -0.05147 | 0.00001 | 0.50778 (e20) | 0.75724 (e15) | -0.06799/0.02316/0.08578 | 0.08578 | POSSIBLE GENERALIZATION GAP |
| P5 | front | 21 | 25 | val_loss/min | val_loss/min (p=4) | 0.38805 | 0.49745 | 0.10941 | 0.77081 | 0.74624 | 0.02457 | 0.00000 | 0.49745 (e21) | 0.74624 (e21) | -0.05602/0.07889/0.14124 | 0.10580 | POSSIBLE GENERALIZATION GAP |
| P5 | side | 26 | 30 | val_loss/min | val_loss/min (p=5) | 0.39480 | 0.50217 | 0.10738 | 0.79013 | 0.68238 | 0.10775 | 0.00000 | 0.50217 (e26) | 0.75724 (e15) | -0.06799/0.04820/0.11361 | 0.10480 | POSSIBLE GENERALIZATION GAP |

Health classifications are descriptive and validation-trajectory based. They are not determined from test performance and are not claims that any one protocol is globally healthier.

## 5. Checkpoint comparison

The selected checkpoint and SHA-256 are recorded in each view's `train_summary.json`. Full P4 selects Front epoch 9 and Side epoch 15; full P5 selects Front epoch 21 and Side epoch 26. P2 uses the Macro-F1 checkpoints but retains the original Side early-stopping behavior; P3 changes checkpoint selection to loss but retains original early-stopping behavior.

## 6. Hard-prediction comparison

### Recomputed test metrics

| protocol | label | method | accuracy | recall_safe | recall_phone | f1_safe | f1_phone | f1_macro | confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 0.86364 | 0.60000 | 0.92222 | 0.61538 | 0.91713 | 0.76626 | [[24,16],[14,166]] |
| P1 | 18_original_mixed_reference | side | 0.80455 | 0.47500 | 0.87778 | 0.46914 | 0.88022 | 0.67468 | [[19,21],[22,158]] |
| P1 | 18_original_mixed_reference | average | 0.89545 | 0.62500 | 0.95556 | 0.68493 | 0.93733 | 0.81113 | [[25,15],[8,172]] |
| P1 | 18_original_mixed_reference | adaptive | 0.89545 | 0.62500 | 0.95556 | 0.68493 | 0.93733 | 0.81113 | [[25,15],[8,172]] |
| P2 | 18_checkpoint_val_macro_f1 | front | 0.86364 | 0.60000 | 0.92222 | 0.61538 | 0.91713 | 0.76626 | [[24,16],[14,166]] |
| P2 | 18_checkpoint_val_macro_f1 | side | 0.80455 | 0.32500 | 0.91111 | 0.37681 | 0.88410 | 0.63045 | [[13,27],[16,164]] |
| P2 | 18_checkpoint_val_macro_f1 | average | 0.88182 | 0.50000 | 0.96667 | 0.60606 | 0.93048 | 0.76827 | [[20,20],[6,174]] |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 0.88182 | 0.50000 | 0.96667 | 0.60606 | 0.93048 | 0.76827 | [[20,20],[6,174]] |
| P3 | 18_checkpoint_val_loss | front | 0.87273 | 0.57500 | 0.93889 | 0.62162 | 0.92350 | 0.77256 | [[23,17],[11,169]] |
| P3 | 18_checkpoint_val_loss | side | 0.80455 | 0.47500 | 0.87778 | 0.46914 | 0.88022 | 0.67468 | [[19,21],[22,158]] |
| P3 | 18_checkpoint_val_loss | average | 0.87273 | 0.55000 | 0.94444 | 0.61111 | 0.92391 | 0.76751 | [[22,18],[10,170]] |
| P3 | 18_checkpoint_val_loss | adaptive | 0.87273 | 0.55000 | 0.94444 | 0.61111 | 0.92391 | 0.76751 | [[22,18],[10,170]] |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 0.86364 | 0.60000 | 0.92222 | 0.61538 | 0.91713 | 0.76626 | [[24,16],[14,166]] |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 0.80455 | 0.32500 | 0.91111 | 0.37681 | 0.88410 | 0.63045 | [[13,27],[16,164]] |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 0.88182 | 0.50000 | 0.96667 | 0.60606 | 0.93048 | 0.76827 | [[20,20],[6,174]] |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 0.88182 | 0.50000 | 0.96667 | 0.60606 | 0.93048 | 0.76827 | [[20,20],[6,174]] |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 0.85909 | 0.47500 | 0.94444 | 0.55072 | 0.91644 | 0.73358 | [[19,21],[10,170]] |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 0.80455 | 0.47500 | 0.87778 | 0.46914 | 0.88022 | 0.67468 | [[19,21],[22,158]] |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 0.87273 | 0.47500 | 0.96111 | 0.57576 | 0.92513 | 0.75045 | [[19,21],[7,173]] |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 0.87273 | 0.47500 | 0.96111 | 0.57576 | 0.92513 | 0.75045 | [[19,21],[7,173]] |

### Transitions versus P1 original

| protocol | label | method | correct_to_correct | correct_to_wrong | wrong_to_correct | wrong_to_wrong | safe_correct_to_wrong | safe_wrong_to_correct | phone_correct_to_wrong | phone_wrong_to_correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 190 | 0 | 0 | 30 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | side | 177 | 0 | 0 | 43 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | average | 197 | 0 | 0 | 23 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | adaptive | 197 | 0 | 0 | 23 | 0 | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | front | 190 | 0 | 0 | 30 | 0 | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | side | 171 | 6 | 6 | 37 | 6 | 0 | 0 | 6 |
| P2 | 18_checkpoint_val_macro_f1 | average | 192 | 5 | 2 | 21 | 5 | 0 | 0 | 2 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 192 | 5 | 2 | 21 | 5 | 0 | 0 | 2 |
| P3 | 18_checkpoint_val_loss | front | 187 | 3 | 5 | 25 | 2 | 1 | 1 | 4 |
| P3 | 18_checkpoint_val_loss | side | 177 | 0 | 0 | 43 | 0 | 0 | 0 | 0 |
| P3 | 18_checkpoint_val_loss | average | 192 | 5 | 0 | 23 | 3 | 0 | 2 | 0 |
| P3 | 18_checkpoint_val_loss | adaptive | 192 | 5 | 0 | 23 | 3 | 0 | 2 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 190 | 0 | 0 | 30 | 0 | 0 | 0 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 171 | 6 | 6 | 37 | 6 | 0 | 0 | 6 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 192 | 5 | 2 | 21 | 5 | 0 | 0 | 2 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 192 | 5 | 2 | 21 | 5 | 0 | 0 | 2 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 183 | 7 | 6 | 24 | 6 | 1 | 1 | 5 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 177 | 0 | 0 | 43 | 0 | 0 | 0 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 191 | 6 | 1 | 22 | 6 | 0 | 0 | 1 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 191 | 6 | 1 | 22 | 6 | 0 | 0 | 1 |

## 7. Probability shift versus P1

| protocol | method | mean_signed_delta | mean_abs_delta | median_abs_delta | std_delta | min_delta | max_delta | p90_abs_delta | changed_count | threshold_crossing_count | safe_mean_delta | safe_mean_abs_delta | safe_crossing_count | phone_mean_delta | phone_mean_abs_delta | phone_crossing_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2 | front | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0 | 0 | 0.00000 | 0.00000 | 0 | 0.00000 | 0.00000 | 0 |
| P2 | side | -0.00501 | 0.04808 | 0.04689 | 0.05632 | -0.12915 | 0.11885 | 0.08803 | 220 | 12 | 0.04705 | 0.06184 | 6 | -0.01657 | 0.04503 | 6 |
| P2 | average | -0.00250 | 0.02404 | 0.02345 | 0.02816 | -0.06457 | 0.05942 | 0.04401 | 220 | 7 | 0.02352 | 0.03092 | 5 | -0.00829 | 0.02251 | 2 |
| P2 | adaptive | -0.00258 | 0.02367 | 0.02286 | 0.02822 | -0.07264 | 0.06306 | 0.04590 | 220 | 7 | 0.02374 | 0.03258 | 5 | -0.00842 | 0.02169 | 2 |
| P3 | front | 0.01603 | 0.03577 | 0.02913 | 0.04160 | -0.10864 | 0.11581 | 0.07163 | 220 | 8 | -0.01702 | 0.04253 | 3 | 0.02337 | 0.03427 | 5 |
| P3 | side | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0 | 0 | 0.00000 | 0.00000 | 0 | 0.00000 | 0.00000 | 0 |
| P3 | average | 0.00801 | 0.01788 | 0.01456 | 0.02080 | -0.05432 | 0.05790 | 0.03581 | 220 | 5 | -0.00851 | 0.02127 | 3 | 0.01169 | 0.01713 | 2 |
| P3 | adaptive | 0.00874 | 0.01910 | 0.01589 | 0.02189 | -0.06372 | 0.05555 | 0.04021 | 220 | 5 | -0.00907 | 0.02217 | 3 | 0.01270 | 0.01842 | 2 |
| P4 | front | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0 | 0 | 0.00000 | 0.00000 | 0 | 0.00000 | 0.00000 | 0 |
| P4 | side | -0.00501 | 0.04808 | 0.04689 | 0.05632 | -0.12915 | 0.11885 | 0.08803 | 220 | 12 | 0.04705 | 0.06184 | 6 | -0.01657 | 0.04503 | 6 |
| P4 | average | -0.00250 | 0.02404 | 0.02345 | 0.02816 | -0.06457 | 0.05942 | 0.04401 | 220 | 7 | 0.02352 | 0.03092 | 5 | -0.00829 | 0.02251 | 2 |
| P4 | adaptive | -0.00258 | 0.02367 | 0.02286 | 0.02822 | -0.07264 | 0.06306 | 0.04590 | 220 | 7 | 0.02374 | 0.03258 | 5 | -0.00842 | 0.02169 | 2 |
| P5 | front | 0.04874 | 0.06246 | 0.05664 | 0.05445 | -0.14788 | 0.17036 | 0.11540 | 220 | 13 | 0.00607 | 0.06610 | 7 | 0.05822 | 0.06164 | 6 |
| P5 | side | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0 | 0 | 0.00000 | 0.00000 | 0 | 0.00000 | 0.00000 | 0 |
| P5 | average | 0.02437 | 0.03123 | 0.02832 | 0.02723 | -0.07394 | 0.08518 | 0.05770 | 220 | 7 | 0.00303 | 0.03305 | 6 | 0.02911 | 0.03082 | 1 |
| P5 | adaptive | 0.02678 | 0.03389 | 0.03068 | 0.02910 | -0.08323 | 0.09320 | 0.06211 | 220 | 7 | 0.00334 | 0.03459 | 6 | 0.03199 | 0.03374 | 1 |

Threshold crossings are hard-prediction changes at 0.5; they are not a claim that the underlying probability shift is causally caused by the selection criterion.

## 8. Confidence and margin analysis

| protocol | label | method | mean_margin | median_margin | std_margin | min_margin | max_margin | count_margin_lt_005 | count_margin_lt_010 | count_margin_ge_025 | correct_mean_margin | wrong_mean_margin | wrong_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 0.25448 | 0.26718 | 0.13358 | 0.00483 | 0.48062 | 19 | 39 | 120 | 0.27441 | 0.12830 | 30 |
| P1 | 18_original_mixed_reference | side | 0.20374 | 0.19106 | 0.13585 | 0.00442 | 0.47365 | 34 | 64 | 78 | 0.22397 | 0.12051 | 43 |
| P1 | 18_original_mixed_reference | average | 0.21629 | 0.20078 | 0.12119 | 0.00330 | 0.46110 | 17 | 46 | 84 | 0.22578 | 0.13501 | 23 |
| P1 | 18_original_mixed_reference | adaptive | 0.22387 | 0.21727 | 0.12037 | 0.00335 | 0.46133 | 14 | 44 | 90 | 0.23351 | 0.14131 | 23 |
| P2 | 18_checkpoint_val_macro_f1 | front | 0.25448 | 0.26718 | 0.13358 | 0.00483 | 0.48062 | 19 | 39 | 120 | 0.27441 | 0.12830 | 30 |
| P2 | 18_checkpoint_val_macro_f1 | side | 0.17688 | 0.15531 | 0.11082 | 0.00278 | 0.42835 | 33 | 62 | 63 | 0.19353 | 0.10837 | 43 |
| P2 | 18_checkpoint_val_macro_f1 | average | 0.20331 | 0.19878 | 0.11286 | 0.00104 | 0.43904 | 26 | 46 | 81 | 0.21565 | 0.11130 | 26 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 0.21040 | 0.21167 | 0.11342 | 0.00122 | 0.44042 | 25 | 42 | 87 | 0.22313 | 0.11545 | 26 |
| P3 | 18_checkpoint_val_loss | front | 0.27985 | 0.30391 | 0.13739 | 0.00190 | 0.48836 | 18 | 30 | 133 | 0.29881 | 0.14984 | 28 |
| P3 | 18_checkpoint_val_loss | side | 0.20374 | 0.19106 | 0.13585 | 0.00442 | 0.47365 | 34 | 64 | 78 | 0.22397 | 0.12051 | 43 |
| P3 | 18_checkpoint_val_loss | average | 0.22794 | 0.21892 | 0.12472 | 0.00320 | 0.46809 | 22 | 40 | 94 | 0.24470 | 0.11302 | 28 |
| P3 | 18_checkpoint_val_loss | adaptive | 0.23644 | 0.23807 | 0.12387 | 0.00325 | 0.46809 | 20 | 36 | 102 | 0.25369 | 0.11820 | 28 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 0.25448 | 0.26718 | 0.13358 | 0.00483 | 0.48062 | 19 | 39 | 120 | 0.27441 | 0.12830 | 30 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 0.17688 | 0.15531 | 0.11082 | 0.00278 | 0.42835 | 33 | 62 | 63 | 0.19353 | 0.10837 | 43 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 0.20331 | 0.19878 | 0.11286 | 0.00104 | 0.43904 | 26 | 46 | 81 | 0.21565 | 0.11130 | 26 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 0.21040 | 0.21167 | 0.11342 | 0.00122 | 0.44042 | 25 | 42 | 87 | 0.22313 | 0.11545 | 26 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 0.30823 | 0.34435 | 0.13747 | 0.00232 | 0.49459 | 8 | 25 | 146 | 0.33422 | 0.14977 | 31 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 0.20374 | 0.19106 | 0.13585 | 0.00442 | 0.47365 | 34 | 64 | 78 | 0.22397 | 0.12051 | 43 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 0.24129 | 0.23519 | 0.12620 | 0.00060 | 0.47525 | 19 | 36 | 102 | 0.25931 | 0.11769 | 28 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 0.25130 | 0.25933 | 0.12519 | 0.00070 | 0.47530 | 16 | 32 | 117 | 0.26995 | 0.12341 | 28 |

For wrong predictions, larger margin means a more confident wrong output in the observed probability artifact.

## 9. Complementarity

| protocol | label | both_correct | front_only_correct | side_only_correct | both_wrong | front_safe_side_phone | front_phone_side_safe | p_side_correct_given_front_wrong | p_front_correct_given_side_wrong | mean_front_prob_disagreement | mean_side_prob_disagreement | mean_abs_prob_diff_disagreement | average_correct_on_disagreement | adaptive_correct_on_disagreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | 164 | 26 | 13 | 17 | 18 | 21 | 0.43333 | 0.60465 | 0.56895 | 0.54785 | 0.30699 | 33 | 33 |
| P2 | 18_checkpoint_val_macro_f1 | 163 | 27 | 14 | 16 | 25 | 16 | 0.46667 | 0.62791 | 0.50918 | 0.58165 | 0.27014 | 31 | 31 |
| P3 | 18_checkpoint_val_loss | 166 | 26 | 11 | 17 | 15 | 22 | 0.39286 | 0.60465 | 0.57715 | 0.52004 | 0.31904 | 26 | 26 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 163 | 27 | 14 | 16 | 25 | 16 | 0.46667 | 0.62791 | 0.50918 | 0.58165 | 0.27014 | 31 | 31 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 163 | 26 | 14 | 17 | 14 | 26 | 0.45161 | 0.60465 | 0.60534 | 0.50841 | 0.31861 | 29 | 29 |

The conditional quantities are descriptive frequencies: `P(Side correct | Front wrong)` and `P(Front correct | Side wrong)` are computed over the observed test rows, not treated as causal probabilities.

## 10. Fusion rescue/break analysis

| protocol | label | fusion | front_wrong_fusion_correct | front_correct_fusion_wrong | front_wrong_fusion_wrong | front_correct_fusion_correct | front_rescue_rate | front_break_rate | side_wrong_fusion_correct | side_correct_fusion_wrong | side_rescue_rate | side_break_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | average | 13 | 6 | 17 | 184 | 0.43333 | 0.03158 | 20 | 0 | 0.46512 | 0.00000 |
| P1 | 18_original_mixed_reference | adaptive | 13 | 6 | 17 | 184 | 0.43333 | 0.03158 | 20 | 0 | 0.46512 | 0.00000 |
| P2 | 18_checkpoint_val_macro_f1 | average | 10 | 6 | 20 | 184 | 0.33333 | 0.03158 | 21 | 4 | 0.48837 | 0.02260 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 10 | 6 | 20 | 184 | 0.33333 | 0.03158 | 21 | 4 | 0.48837 | 0.02260 |
| P3 | 18_checkpoint_val_loss | average | 8 | 8 | 20 | 184 | 0.28571 | 0.04167 | 18 | 3 | 0.41860 | 0.01695 |
| P3 | 18_checkpoint_val_loss | adaptive | 8 | 8 | 20 | 184 | 0.28571 | 0.04167 | 18 | 3 | 0.41860 | 0.01695 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 10 | 6 | 20 | 184 | 0.33333 | 0.03158 | 21 | 4 | 0.48837 | 0.02260 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 10 | 6 | 20 | 184 | 0.33333 | 0.03158 | 21 | 4 | 0.48837 | 0.02260 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 10 | 7 | 21 | 182 | 0.32258 | 0.03704 | 19 | 4 | 0.44186 | 0.02260 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 10 | 7 | 21 | 182 | 0.32258 | 0.03704 | 19 | 4 | 0.44186 | 0.02260 |

P1's Average Fusion relative to Front: rescue and break counts are shown directly above. The primary comparison is whether standardized protocols change these observed rescue/break counts.

## 11. Fusion threshold and margin analysis

| protocol | label | mean_fusion_margin | median_fusion_margin | within_002 | within_005 | within_010 | correct_mean_margin | wrong_mean_margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | 0.21629 | 0.20078 | 10 | 17 | 46 | 0.22578 | 0.13501 |
| P2 | 18_checkpoint_val_macro_f1 | 0.20331 | 0.19878 | 13 | 26 | 46 | 0.21565 | 0.11130 |
| P3 | 18_checkpoint_val_loss | 0.22794 | 0.21892 | 8 | 22 | 40 | 0.24470 | 0.11302 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 0.20331 | 0.19878 | 13 | 26 | 46 | 0.21565 | 0.11130 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 0.24129 | 0.23519 | 13 | 19 | 36 | 0.25931 | 0.11769 |

### Threshold crossing table versus P1

| protocol | label | method | safe_to_phone | phone_to_safe | any_crossing |
| --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | side | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | average | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | adaptive | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | front | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | side | 6 | 0 | 12 |
| P2 | 18_checkpoint_val_macro_f1 | average | 5 | 0 | 7 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 5 | 0 | 7 |
| P3 | 18_checkpoint_val_loss | front | 2 | 1 | 8 |
| P3 | 18_checkpoint_val_loss | side | 0 | 0 | 0 |
| P3 | 18_checkpoint_val_loss | average | 3 | 2 | 5 |
| P3 | 18_checkpoint_val_loss | adaptive | 3 | 2 | 5 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 0 | 0 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 6 | 0 | 12 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 5 | 0 | 7 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 5 | 0 | 7 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 6 | 1 | 13 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 0 | 0 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 6 | 0 | 7 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 6 | 0 | 7 |

## 12. Why did fusion change? Per-sample transition evidence

The complete one-row-per-test-sample audit is saved in `model_selection_protocol_per_sample_audit.csv`. For every protocol/method it contains original-vs-new probability deltas, correct/wrong transitions, and the probabilities needed to inspect original-correct-to-standardized-wrong cases. In particular, columns named `P2_P1_correct_to_average_wrong`, etc., identify category B directly.

### Aggregate original-fusion versus new-fusion transitions

| protocol | label | method | correct_to_correct | correct_to_wrong | wrong_to_correct | wrong_to_wrong | safe_correct_to_wrong | safe_wrong_to_correct | phone_correct_to_wrong | phone_wrong_to_correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | side | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | average | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P1 | 18_original_mixed_reference | adaptive | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | front | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | side | 208 | 12 | 0 | 0 | 6 | 0 | 6 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | average | 213 | 7 | 0 | 0 | 2 | 0 | 5 | 0 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 213 | 7 | 0 | 0 | 2 | 0 | 5 | 0 |
| P3 | 18_checkpoint_val_loss | front | 212 | 8 | 0 | 0 | 5 | 0 | 3 | 0 |
| P3 | 18_checkpoint_val_loss | side | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P3 | 18_checkpoint_val_loss | average | 215 | 5 | 0 | 0 | 0 | 0 | 5 | 0 |
| P3 | 18_checkpoint_val_loss | adaptive | 215 | 5 | 0 | 0 | 0 | 0 | 5 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 208 | 12 | 0 | 0 | 6 | 0 | 6 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 213 | 7 | 0 | 0 | 2 | 0 | 5 | 0 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 213 | 7 | 0 | 0 | 2 | 0 | 5 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 207 | 13 | 0 | 0 | 6 | 0 | 7 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 213 | 7 | 0 | 0 | 1 | 0 | 6 | 0 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 213 | 7 | 0 | 0 | 1 | 0 | 6 | 0 |

The per-sample CSV is the evidence for the requested true-class, probability-before/after, threshold-crossing, and largest-view-movement breakdown; this report does not replace those rows with an inferred narrative.

## 13. Wrong-confidence analysis

| protocol | label | view | error_type | count | mean_p_phone | median_p_phone | mean_margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | safe_to_phone_false_positive | 16 | 0.66780 | 0.67387 | 0.16780 |
| P1 | 18_original_mixed_reference | front | phone_to_safe_false_negative | 14 | 0.41684 | 0.42430 | 0.08316 |
| P1 | 18_original_mixed_reference | side | safe_to_phone_false_positive | 21 | 0.66599 | 0.63195 | 0.16599 |
| P1 | 18_original_mixed_reference | side | phone_to_safe_false_negative | 22 | 0.42290 | 0.42347 | 0.07710 |
| P2 | 18_checkpoint_val_macro_f1 | front | safe_to_phone_false_positive | 16 | 0.66780 | 0.67387 | 0.16780 |
| P2 | 18_checkpoint_val_macro_f1 | front | phone_to_safe_false_negative | 14 | 0.41684 | 0.42430 | 0.08316 |
| P2 | 18_checkpoint_val_macro_f1 | side | safe_to_phone_false_positive | 27 | 0.64928 | 0.62696 | 0.14928 |
| P2 | 18_checkpoint_val_macro_f1 | side | phone_to_safe_false_negative | 16 | 0.46065 | 0.46535 | 0.03935 |
| P3 | 18_checkpoint_val_loss | front | safe_to_phone_false_positive | 17 | 0.66610 | 0.65005 | 0.16610 |
| P3 | 18_checkpoint_val_loss | front | phone_to_safe_false_negative | 11 | 0.37529 | 0.39125 | 0.12471 |
| P3 | 18_checkpoint_val_loss | side | safe_to_phone_false_positive | 21 | 0.66599 | 0.63195 | 0.16599 |
| P3 | 18_checkpoint_val_loss | side | phone_to_safe_false_negative | 22 | 0.42290 | 0.42347 | 0.07710 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | safe_to_phone_false_positive | 16 | 0.66780 | 0.67387 | 0.16780 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | phone_to_safe_false_negative | 14 | 0.41684 | 0.42430 | 0.08316 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | safe_to_phone_false_positive | 27 | 0.64928 | 0.62696 | 0.14928 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | phone_to_safe_false_negative | 16 | 0.46065 | 0.46535 | 0.03935 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | safe_to_phone_false_positive | 21 | 0.67424 | 0.67322 | 0.17424 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | phone_to_safe_false_negative | 10 | 0.40163 | 0.40527 | 0.09837 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | safe_to_phone_false_positive | 21 | 0.66599 | 0.63195 | 0.16599 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | phone_to_safe_false_negative | 22 | 0.42290 | 0.42347 | 0.07710 |

## 14. Calibration and probability quality

| protocol | label | method | roc_auc | pr_auc | ece_binary | brier_score |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | front | 0.88014 | 0.97075 | 0.12513 | 0.11311 |
| P1 | 18_original_mixed_reference | side | 0.75444 | 0.92515 | 0.16761 | 0.15333 |
| P1 | 18_original_mixed_reference | average | 0.86292 | 0.96236 | 0.17916 | 0.12341 |
| P1 | 18_original_mixed_reference | adaptive | 0.86500 | 0.96329 | 0.17159 | 0.12028 |
| P2 | 18_checkpoint_val_macro_f1 | front | 0.88014 | 0.97075 | 0.12513 | 0.11311 |
| P2 | 18_checkpoint_val_macro_f1 | side | 0.71014 | 0.90842 | 0.16615 | 0.15905 |
| P2 | 18_checkpoint_val_macro_f1 | average | 0.86556 | 0.96264 | 0.17850 | 0.12707 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 0.86806 | 0.96415 | 0.17141 | 0.12402 |
| P3 | 18_checkpoint_val_loss | front | 0.88958 | 0.97330 | 0.09754 | 0.10548 |
| P3 | 18_checkpoint_val_loss | side | 0.75444 | 0.92515 | 0.16761 | 0.15333 |
| P3 | 18_checkpoint_val_loss | average | 0.86917 | 0.96417 | 0.14479 | 0.11834 |
| P3 | 18_checkpoint_val_loss | adaptive | 0.87069 | 0.96519 | 0.14369 | 0.11489 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 0.88014 | 0.97075 | 0.12513 | 0.11311 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 0.71014 | 0.90842 | 0.16615 | 0.15905 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 0.86556 | 0.96264 | 0.17850 | 0.12707 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 0.86806 | 0.96415 | 0.17141 | 0.12402 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 0.89389 | 0.97429 | 0.06823 | 0.09788 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 0.75444 | 0.92515 | 0.16761 | 0.15333 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 0.87264 | 0.96460 | 0.13144 | 0.11282 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 0.87750 | 0.96644 | 0.12142 | 0.10894 |

These metrics are recomputed with the existing repository implementation: ROC-AUC and PR-AUC use phone probability; ECE uses the existing 10-bin binary definition; Brier uses mean squared probability error. Thresholded classification, ranking, and calibration are reported separately.

## 15. Macro-F1 class decomposition

| protocol | label | fusion | safe_precision | safe_recall | safe_f1 | phone_precision | phone_recall | phone_f1 | macro_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | average | 0.75758 | 0.62500 | 0.68493 | 0.91979 | 0.95556 | 0.93733 | 0.81113 |
| P1 | 18_original_mixed_reference | adaptive | 0.75758 | 0.62500 | 0.68493 | 0.91979 | 0.95556 | 0.93733 | 0.81113 |
| P2 | 18_checkpoint_val_macro_f1 | average | 0.76923 | 0.50000 | 0.60606 | 0.89691 | 0.96667 | 0.93048 | 0.76827 |
| P2 | 18_checkpoint_val_macro_f1 | adaptive | 0.76923 | 0.50000 | 0.60606 | 0.89691 | 0.96667 | 0.93048 | 0.76827 |
| P3 | 18_checkpoint_val_loss | average | 0.68750 | 0.55000 | 0.61111 | 0.90426 | 0.94444 | 0.92391 | 0.76751 |
| P3 | 18_checkpoint_val_loss | adaptive | 0.68750 | 0.55000 | 0.61111 | 0.90426 | 0.94444 | 0.92391 | 0.76751 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average | 0.76923 | 0.50000 | 0.60606 | 0.89691 | 0.96667 | 0.93048 | 0.76827 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | adaptive | 0.76923 | 0.50000 | 0.60606 | 0.89691 | 0.96667 | 0.93048 | 0.76827 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average | 0.73077 | 0.47500 | 0.57576 | 0.89175 | 0.96111 | 0.92513 | 0.75045 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | adaptive | 0.73077 | 0.47500 | 0.57576 | 0.89175 | 0.96111 | 0.92513 | 0.75045 |

Macro F1 is the mean of Safe and Phone-use F1. The decomposition shows whether a fusion change is concentrated in the minority Safe class, the Phone-use class, or both.

## 16. Subject-level behavior

| protocol | label | subject_id | n_samples | safe_count | phone_count | macro_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | 4 | 32 | 6 | 26 | 0.89744 |
| P1 | 18_original_mixed_reference | 8 | 38 | 8 | 30 | 0.70929 |
| P1 | 18_original_mixed_reference | 10 | 30 | 5 | 25 | 0.75741 |
| P1 | 18_original_mixed_reference | 11 | 27 | 6 | 21 | 0.58967 |
| P1 | 18_original_mixed_reference | 17 | 35 | 6 | 29 | 0.83821 |
| P1 | 18_original_mixed_reference | 21 | 33 | 5 | 28 | 0.94545 |
| P1 | 18_original_mixed_reference | 42 | 25 | 4 | 21 | 0.87500 |
| P2 | 18_checkpoint_val_macro_f1 | 4 | 32 | 6 | 26 | 0.76296 |
| P2 | 18_checkpoint_val_macro_f1 | 8 | 38 | 8 | 30 | 0.67521 |
| P2 | 18_checkpoint_val_macro_f1 | 10 | 30 | 5 | 25 | 0.75741 |
| P2 | 18_checkpoint_val_macro_f1 | 11 | 27 | 6 | 21 | 0.58967 |
| P2 | 18_checkpoint_val_macro_f1 | 17 | 35 | 6 | 29 | 0.76667 |
| P2 | 18_checkpoint_val_macro_f1 | 21 | 33 | 5 | 28 | 0.94545 |
| P2 | 18_checkpoint_val_macro_f1 | 42 | 25 | 4 | 21 | 0.85119 |
| P3 | 18_checkpoint_val_loss | 4 | 32 | 6 | 26 | 0.67677 |
| P3 | 18_checkpoint_val_loss | 8 | 38 | 8 | 30 | 0.70929 |
| P3 | 18_checkpoint_val_loss | 10 | 30 | 5 | 25 | 0.75741 |
| P3 | 18_checkpoint_val_loss | 11 | 27 | 6 | 21 | 0.55978 |
| P3 | 18_checkpoint_val_loss | 17 | 35 | 6 | 29 | 0.83821 |
| P3 | 18_checkpoint_val_loss | 21 | 33 | 5 | 28 | 0.94545 |
| P3 | 18_checkpoint_val_loss | 42 | 25 | 4 | 21 | 0.82517 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 4 | 32 | 6 | 26 | 0.76296 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 8 | 38 | 8 | 30 | 0.67521 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 10 | 30 | 5 | 25 | 0.75741 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 11 | 27 | 6 | 21 | 0.58967 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 17 | 35 | 6 | 29 | 0.76667 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 21 | 33 | 5 | 28 | 0.94545 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 42 | 25 | 4 | 21 | 0.85119 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 4 | 32 | 6 | 26 | 0.67677 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 8 | 38 | 8 | 30 | 0.70929 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 10 | 30 | 5 | 25 | 0.75741 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 11 | 27 | 6 | 21 | 0.58967 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 17 | 35 | 6 | 29 | 0.68124 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 21 | 33 | 5 | 28 | 1.00000 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 42 | 25 | 4 | 21 | 0.79675 |

The subject table is descriptive. Subjects are not treated as independent observations for inference.

## 17. Bootstrap

| protocol | label | comparison | method | n_clusters | n_boot | seed | observed_delta | ci95_low | ci95_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | average_vs_front | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.04487 | -0.03270 | 0.13884 |
| P1 | 18_original_mixed_reference | average_vs_side | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.13645 | 0.09801 | 0.19127 |
| P2 | 18_checkpoint_val_macro_f1 | average_vs_front | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.00202 | -0.07058 | 0.07734 |
| P2 | 18_checkpoint_val_macro_f1 | average_vs_side | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.13782 | 0.08525 | 0.20421 |
| P3 | 18_checkpoint_val_loss | average_vs_front | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | -0.00505 | -0.02949 | 0.04107 |
| P3 | 18_checkpoint_val_loss | average_vs_side | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.09283 | 0.01168 | 0.15940 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average_vs_front | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.00202 | -0.07058 | 0.07734 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | average_vs_side | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.13782 | 0.08525 | 0.20421 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average_vs_front | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.01686 | -0.01373 | 0.05963 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | average_vs_side | subject_cluster_bootstrap_test_subjects | 7 | 10000 | 42 | 0.07577 | -0.01765 | 0.15696 |

The within-protocol Average-vs-Front and Average-vs-Side intervals use the documented 7-subject cluster bootstrap, 10,000 resamples, percentile 95% interval, seed 42. A direct paired protocol-vs-protocol bootstrap (P1 Average versus each standardized Average) is **NOT COMPUTED** because the authoritative repository does not expose a reusable implementation for that cross-protocol comparison; no new inferential framework is silently introduced here.

## 18. Original versus standardized Macro-F1

P1 versus P2/P4 changes the Side selected checkpoint from the original Side val-loss checkpoint (epoch 26) to the Side Macro-F1 checkpoint (epoch 15). Front selected epoch 9 in both P1 and P2/P4. The exact probability shifts, hard-label transitions, safe/phone transitions, rescue/break counts, and calibration values are in the tables above and the per-sample CSV. Therefore the observed fusion reduction is associated with changed Side predictions and changed fusion inputs, while the artifact comparison alone does not establish a causal mechanism beyond that descriptive association.

## 19. Original versus checkpoint-only val-loss

P1 versus P3 isolates the Front checkpoint change in the intended protocol design: Side remains the original val-loss-selected model in the stored artifacts, while Front changes to the val-loss checkpoint. The comparison tables and per-sample CSV quantify Front probability shifts, hard transitions, and fusion rescue/break changes. This is a checkpoint-only comparison; it must not be conflated with P5, which also changes Front early stopping.

## 20. Checkpoint-only versus full standardization

| pair | left_protocol | right_protocol | changed_view_by_design | method | left_front_epoch | right_front_epoch | left_side_epoch | right_side_epoch | mean_signed_probability_delta | mean_abs_probability_delta | hard_decision_changes | correct_to_wrong | wrong_to_correct | left_macro_f1 | right_macro_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2_vs_P4 | P2 | P4 | side | front | 9 | 9 | 15 | 15 | 0.00000 | 0.00000 | 0 | 0 | 0 | 0.76626 | 0.76626 |
| P2_vs_P4 | P2 | P4 | side | side | 9 | 9 | 15 | 15 | 0.00000 | 0.00000 | 0 | 0 | 0 | 0.63045 | 0.63045 |
| P2_vs_P4 | P2 | P4 | side | average | 9 | 9 | 15 | 15 | 0.00000 | 0.00000 | 0 | 0 | 0 | 0.76827 | 0.76827 |
| P2_vs_P4 | P2 | P4 | side | adaptive | 9 | 9 | 15 | 15 | 0.00000 | 0.00000 | 0 | 0 | 0 | 0.76827 | 0.76827 |
| P3_vs_P5 | P3 | P5 | front | front | 12 | 21 | 26 | 26 | 0.03271 | 0.03501 | 7 | 5 | 2 | 0.77256 | 0.73358 |
| P3_vs_P5 | P3 | P5 | front | side | 12 | 21 | 26 | 26 | 0.00000 | 0.00000 | 0 | 0 | 0 | 0.67468 | 0.67468 |
| P3_vs_P5 | P3 | P5 | front | average | 12 | 21 | 26 | 26 | 0.01636 | 0.01751 | 6 | 3 | 3 | 0.76751 | 0.75045 |
| P3_vs_P5 | P3 | P5 | front | adaptive | 12 | 21 | 26 | 26 | 0.01804 | 0.01924 | 6 | 3 | 3 | 0.76751 | 0.75045 |

P2 versus P4 changes Side early stopping; P3 versus P5 changes Front early stopping. The table quantifies selected epochs, probability movement, hard-decision changes, and Macro-F1 change for each model output. Equal rows mean no observable change in that stored output; they do not establish causal equivalence beyond the artifact comparison.

## 21. Hypothesis evaluation

| hypothesis | status | evidence |
| --- | --- | --- |
| H1: Original wins because of better complementary hard errors | PARTIALLY SUPPORTED | P1 Front/Side complementarity and conditional usefulness are reported alongside every standardized protocol; the difference is descriptive and not uniformly favorable on every component. |
| H2: Original wins because wrong predictions are less confident | INCONCLUSIVE | P1 Average-Fusion wrong-margin=0.13501; standardized values are 0.11130, 0.11302, 0.11130, 0.11769. This does not isolate a single causal source. |
| H3: Original wins because probabilities combine more favorably around 0.5 | PARTIALLY SUPPORTED | P1 Average-Fusion mean margin=0.21629; standardized values are 0.20331, 0.22794, 0.20331, 0.24129. Threshold and probability-shift tables show the affected rows. |
| H4: Original rescues more Front errors | PARTIALLY SUPPORTED | P1 Average-Fusion Front rescue=13; standardized counts=10, 8, 10, 10. |
| H5: Original breaks fewer Front-correct predictions | INCONCLUSIVE | P1 Average-Fusion Front break=6; standardized counts=6, 8, 6, 7. P1 is not uniformly lower across all protocols. |
| H6: Standardized checkpoints are more overfit | INCONCLUSIVE | Health classification uses validation trajectories only; it does not establish a causal test-performance explanation, and the observed gaps do not uniformly support a single overfitting ordering. |
| H7: Standardized checkpoints are underfit | INCONCLUSIVE | Selected epochs, validation peaks, post-checkpoint behavior, and gaps differ by view/protocol; no uniform underfitting pattern is established. |

## 22. FACT

- P1–P5 prediction files are aligned on the same 220 test rows and 7 subject IDs; this was verified before recomputation.
- P1 Average Fusion Macro F1 and the standardized results are recomputed from stored per-sample predictions using the repository metric definitions.
- P1, P2, P3, P4, and P5 have different stored Front/Side probabilities and/or hard predictions; the per-sample CSV records the exact changes.
- Full standardization changes early stopping as well as checkpoint selection by protocol definition; checkpoint-only variants do not make the same change.

## 23. INTERPRETATION

The defensible interpretation is descriptive: protocol changes select different stored model states and therefore alter the Front/Side probability fields, hard errors, complementarity, and fusion threshold outcomes. The relative contribution of these observed mechanisms is quantified in the tables, but a causal claim about why one protocol wins is not identified by these non-randomized, single-seed artifacts alone.

## 23a. Model health versus fusion outcome

| protocol | label | front_selected_loss_gap | side_selected_loss_gap | front_val_f1 | side_val_f1 | front_test_f1 | side_test_f1 | front_ece | front_brier | side_ece | side_brier | front_only_correct | side_only_correct | fusion_rescue_count | fusion_break_count | average_fusion_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 18_original_mixed_reference | 0.04383 | 0.10738 | 0.72581 | 0.68238 | 0.76626 | 0.67468 | 0.12513 | 0.11311 | 0.16761 | 0.15333 | 26 | 13 | 13 | 6 | 0.81113 |
| P2 | 18_checkpoint_val_macro_f1 | 0.04383 | 0.05490 | 0.72581 | 0.75724 | 0.76626 | 0.63045 | 0.12513 | 0.11311 | 0.16615 | 0.15905 | 27 | 14 | 10 | 6 | 0.76827 |
| P3 | 18_checkpoint_val_loss | 0.09239 | 0.10738 | 0.71892 | 0.68238 | 0.77256 | 0.67468 | 0.09754 | 0.10548 | 0.16761 | 0.15333 | 26 | 11 | 8 | 8 | 0.76751 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 0.04383 | 0.05490 | 0.72581 | 0.75724 | 0.76626 | 0.63045 | 0.12513 | 0.11311 | 0.16615 | 0.15905 | 27 | 14 | 10 | 6 | 0.76827 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | 0.10941 | 0.10738 | 0.74624 | 0.68238 | 0.73358 | 0.67468 | 0.06823 | 0.09788 | 0.16761 | 0.15333 | 26 | 14 | 10 | 7 | 0.75045 |

This table is a descriptive side-by-side view. Five protocols are insufficient to establish a correlation or a causal relationship between health indicators and fusion outcome.

## 23b. Subject-level delta versus P1

| protocol | label | mean_subject_delta | median_subject_delta | min_subject_delta | max_subject_delta | subjects_improved | subjects_worsened | subjects_unchanged | subject_deltas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2 | 18_checkpoint_val_macro_f1 | -0.03770 | -0.02381 | -0.13447 | 0.00000 | 0 | 4 | 3 | S4=-0.13447; S8=-0.03408; S10=+0.00000; S11=+0.00000; S17=-0.07155; S21=+0.00000; S42=-0.02381 |
| P3 | 18_checkpoint_val_loss | -0.04291 | 0.00000 | -0.22067 | 0.00000 | 0 | 3 | 4 | S4=-0.22067; S8=+0.00000; S10=+0.00000; S11=-0.02988; S17=+0.00000; S21=+0.00000; S42=-0.04983 |
| P4 | 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | -0.03770 | -0.02381 | -0.13447 | 0.00000 | 0 | 4 | 3 | S4=-0.13447; S8=-0.03408; S10=+0.00000; S11=+0.00000; S17=-0.07155; S21=+0.00000; S42=-0.02381 |
| P5 | 18_checkpoint_val_loss_and_earlystopping_val_loss | -0.05734 | 0.00000 | -0.22067 | 0.05455 | 1 | 3 | 3 | S4=-0.22067; S8=+0.00000; S10=+0.00000; S11=+0.00000; S17=-0.15697; S21=+0.05455; S42=-0.07825 |

The subject-level delta shows whether the fusion drop is broad or concentrated. It is descriptive and does not treat the seven subjects as independent inferential units.

## 24. LIMITATIONS

- P1's original summary omits explicit early-stopping metadata; the exact source behavior was used to document it as source-inferred.
- Only stored artifacts were used. No new inference was run, so unavailable intermediate logits or training randomness cannot be recovered.
- One configured training seed is available per run; cuDNN deterministic mode is recorded as false. This limits claims about training-seed variability.
- Direct paired bootstrap between protocols is not computed because no existing authoritative implementation for that comparison was found.
- Descriptive test-set comparisons are not evidence that the test set was legitimately used for model selection.

## 25. Audit artifacts

- `model_selection_protocol_per_sample_audit.csv`
- `model_selection_protocol_deep_audit_tables/` (CSV tables)
- `figures/protocol_probability_audit/`
- `model_selection_protocol_deep_audit_data.json`

## 26. Required conclusion

**PRIMARY OBSERVED MECHANISM:** Different selected checkpoints produce different per-sample Front/Side probabilities and hard decisions; these altered fusion inputs reduce the number of Front errors rescued by Average Fusion. P1 rescues 13 Front errors, versus 10 for P2/P4, 8 for P3, and 10 for P5.

**SECONDARY OBSERVED MECHANISM:** Threshold interaction and class-specific hard-error changes. P1's Average Fusion has Safe F1 0.68493 and Phone-use F1 0.93733; standardized protocols have lower Safe F1, with additional correct-to-wrong fusion transitions documented in the per-sample audit.

**MODEL-HEALTH CONTRIBUTION:** INCONCLUSIVE — validation gaps and post-checkpoint trajectories differ, but the protocol with the larger observed Side gap (P1) has higher fusion F1 than the Macro-F1 standardized protocol; test outcome does not establish health causality.

**COMPLEMENTARITY CONTRIBUTION:** PARTIALLY SUPPORTED — P1 has more Front-error rescues, but rescue/break and Side-only counts are not uniformly better across every standardized protocol.

**PROBABILITY-DISTRIBUTION CONTRIBUTION:** SUPPORTED descriptively — P2/P4 change Side probabilities (mean absolute shift 0.04808; 12 Side threshold changes), while P3 changes Front probabilities (mean absolute shift 0.03577; 8 Front threshold changes); fusion transitions are recorded per sample.

**CALIBRATION CONTRIBUTION:** NOT SUPPORTED as the primary explanation — ECE/ROC-AUC/PR-AUC are mixed across protocols; P1 does not uniformly have the best calibration or ranking metrics.

**EARLY-STOPPING CONTRIBUTION:** PARTIALLY SUPPORTED — P2 versus P4 produces no observable prediction or fusion change despite different stopping completion, whereas P3 versus P5 changes Front from epoch 12 to 21 and changes six Average-Fusion hard decisions.

**CAN WE CLAIM CAUSALITY:** NO. We can claim descriptively that the protocols selected different stored model states whose probabilities and hard-error patterns produced different fusion outcomes; the artifacts do not identify a causal mechanism that generalizes beyond these runs.
