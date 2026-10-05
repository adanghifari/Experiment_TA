# Model-selection protocol comparison

Scope: authoritative repository `D:\Skripsi\Experiment_TA` only. No historical repository or manuscript edits were used.

## Protocols compared

1. Original mixed `experiment_18`.
2. Existing checkpoint-only Macro-F1 variant.
3. Existing checkpoint-only validation-loss variant.
4. New full standardized Macro-F1 variant.
5. New full standardized validation-loss variant.

The two new variants were fully run: Front and Side training, train/validation/test evaluation, fusion, and summary. The earlier two variants are compared only from their existing stored artifacts.

## Protocol and selected checkpoint table

| protocol | Front criterion | Side criterion | Front epoch | Side epoch | Front test Macro F1 | Side test Macro F1 | Average fusion Macro F1 | Adaptive fusion Macro F1 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 18_original_mixed_reference | val_macro_f1/max | val_loss/min | 9 | 26 | 0.76626 | 0.67468 | 0.81113 | 0.81113 |
| 18_checkpoint_val_macro_f1 | val_macro_f1/max | val_macro_f1/max | 9 | 15 | 0.76626 | 0.63045 | 0.76827 | 0.76827 |
| 18_checkpoint_val_loss | val_loss/min | val_loss/min | 12 | 26 | 0.77256 | 0.67468 | 0.76751 | 0.76751 |
| 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | val_macro_f1/max | val_macro_f1/max | 9 | 15 | 0.76626 | 0.63045 | 0.76827 | 0.76827 |
| 18_checkpoint_val_loss_and_earlystopping_val_loss | val_loss/min | val_loss/min | 21 | 26 | 0.73358 | 0.67468 | 0.75045 | 0.75045 |

## Training-health observations for the new variants

| variant | view | executed epochs | selected epoch | min-loss epoch | max-F1 epoch | selected val loss | selected val Macro F1 | final loss gap |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | front | 13 | 9 | 12 | 9 | 0.51736 | 0.72581 | 0.13310 |
| 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | side | 20 | 15 | 20 | 15 | 0.53991 | 0.75724 | 0.08578 |
| 18_checkpoint_val_loss_and_earlystopping_val_loss | front | 25 | 21 | 21 | 21 | 0.49745 | 0.74624 | 0.10580 |
| 18_checkpoint_val_loss_and_earlystopping_val_loss | side | 30 | 26 | 26 | 15 | 0.50217 | 0.68238 | 0.10480 |

## Fusion, complementarity, adaptive diagnostics, and bootstrap

Each variant's detailed summary contains ROC-AUC, PR-AUC, ECE, Brier, per-class results, confusion matrices, complementarity counts, adaptive-weight diagnostics, and subject-cluster bootstrap intervals. The stored prediction CSVs are the common evidence layer for the post-run comparisons.

| protocol | avg-vs-Front observed ΔF1 [95% CI] | avg-vs-Side observed ΔF1 [95% CI] | Front weight mean | avg rescue/break |
|---|---:|---:|---:|---:|
| 18_original_mixed_reference | 0.04487 [-0.03270, 0.13884] | 0.13645 [0.09801, 0.19127] | 0.51260 | 13/6 |
| 18_checkpoint_val_macro_f1 | 0.00202 [-0.07058, 0.07734] | 0.13782 [0.08525, 0.20421] | 0.51929 | 10/6 |
| 18_checkpoint_val_loss | -0.00505 [-0.02949, 0.04107] | 0.09283 [0.01168, 0.15940] | 0.51890 | 8/8 |
| 18_checkpoint_val_macro_f1_and_earlystopping_val_macro | 0.00202 [-0.07058, 0.07734] | 0.13782 [0.08525, 0.20421] | 0.51929 | 10/6 |
| 18_checkpoint_val_loss_and_earlystopping_val_loss | 0.01686 [-0.01373, 0.05963] | 0.07577 [-0.01765, 0.15696] | 0.52593 | 10/7 |

## FACT

- The new full Macro-F1 variant has both views using checkpoint and early-stopping `val_macro_f1/max`.
- The new full validation-loss variant has both views using checkpoint and early-stopping `val_loss/min`.
- Scheduler monitor/logic was kept as `val_macro_f1/max`; it is not part of the controlled selection-criterion change.
- Both new variants have physical checkpoints, per-epoch histories, evaluation outputs, fusion outputs, and SHA-256 records.

## OBSERVED DIFFERENCE

- The tables show what changed in these stored runs. A result difference is not by itself evidence that a criterion is generally better or that the criterion was selected because of test performance.

## INTERPRETATION

- Full standardization changes early stopping as well as checkpoint selection relative to the original mixed protocol. Therefore the new full variants are distinct training trajectories, not mere relabeling of old checkpoints.
- The checkpoint-only variants are not interchangeable with the new full variants because their early-stopping protocols were not simultaneously standardized.

## LIMITATION

- One configured training seed was used for each new variant; cuDNN deterministic mode was false in the recorded environment.
- Subject-cluster bootstrap uses 7 test subjects, 10,000 repetitions, percentile 95% CI, and analysis seed 42. It measures resampling uncertainty, not training-seed uncertainty.
- This comparison does not use the test set as a model-selection signal.

## Detailed reports

- [Full standardized Macro F1 summary](../experiment_18_full_standardized_macro_f1/results/full_standardized_macro_f1_summary.md)
- [Full standardized validation-loss summary](../experiment_18_full_standardized_val_loss/results/full_standardized_val_loss_summary.md)
