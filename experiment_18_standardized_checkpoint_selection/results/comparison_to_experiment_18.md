# Comparison: experiment_18_standardized_checkpoint_selection vs experiment_18

This report tests Side checkpoint-selection standardization. Paper_TA was not edited.

## Protocol

- Front checkpoint: val_macro_f1/max (unchanged).
- Side checkpoint: val_macro_f1/max (changed from val_loss/min).
- Side early stopping: val_loss/min, patience 5 (kept from experiment_18).
- Side scheduler: val_macro_f1, patience 2 (same effective experiment_18 training metadata).
- Other data, split, seed, augmentation, class weights, loss, optimizer, stride, and model settings: unchanged.

## Test metrics

| Metric | experiment_18 | Standardized variant | Delta |
|---|---:|---:|---:|
| Front Macro F1 | 0.76626 | 0.76626 | +0.00000 |
| Side Macro F1 | 0.67468 | 0.63045 | -0.04423 |
| Average Fusion Macro F1 | 0.81113 | 0.76827 | -0.04286 |
| Adaptive Fusion Macro F1 | 0.81113 | 0.76827 | -0.04286 |

## Checkpoint and stopping evidence

- Side checkpoint: epoch 15, selected by val_macro_f1/max.
- Side early stopping: val_loss/min, patience 5; run completed at epoch 30.
- Front best epoch: 9.
- Front common configuration equal to parent: True.
- Side common configuration equal apart from intended checkpoint monitor fields: True.

The JSON file contains the full comparison, hashes, and audit checks.
