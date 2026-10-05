# Configuration diff — experiment_18_full_standardized_macro_f1 vs `experiment_18`

## Status

- Pre-run gate: PASS.
- Run status: COMPLETED; both views trained, evaluated, fused, and summarized.
- Output namespace: `full_standardized_macro_f1`.

## Intended controlled change

| field | experiment_18 effective protocol | controlled variant |
|---|---|---|
| Front checkpoint | `val_macro_f1/max` | `val_macro_f1/max` |
| Side checkpoint | `val_loss/min` | `val_macro_f1/max` |
| Front early stopping | `val_macro_f1/max`, patience 4 | `val_macro_f1/max`, patience 4 |
| Side early stopping | `val_loss/min`, patience 5 | `val_macro_f1/max`, patience 5 |
| Scheduler | unchanged; effective patience Front=1, Side=2; monitor `val_macro_f1/max` | unchanged |
| All other hyperparameters/data/split/augmentation | locked | locked |

## Verification after run

- Front selected epoch: 9; Side selected epoch: 15.
- Front checkpoint SHA-256: `3b87de7c597ddaf7cf51022dfe47c0d5c325316d8d207e743e19e1286061b8b8`.
- Side checkpoint SHA-256: `92afbec084192fa08c157174528c0bb49a5af40f2ae8b89209ac540b9c6c4645`.
- No output is written to the original `experiment_18` namespace by this controlled variant.

## Metadata note

- The baseline root `experiment_18/config/resolved_config.json` records Side scheduler patience as 1, while the baseline source/per-view training metadata records the effective Side value as 2. This variant preserves the effective source behavior (Side=2) and does not treat the stale root metadata value as a protocol change.
