# Configuration diff — experiment_18_full_standardized_val_loss vs `experiment_18`

## Status

- Pre-run gate: PASS.
- Run status: COMPLETED; both views trained, evaluated, fused, and summarized.
- Output namespace: `full_standardized_val_loss`.

## Intended controlled change

| field | experiment_18 effective protocol | controlled variant |
|---|---|---|
| Front checkpoint | `val_macro_f1/max` | `val_loss/min` |
| Side checkpoint | `val_loss/min` | `val_loss/min` |
| Front early stopping | `val_macro_f1/max`, patience 4 | `val_loss/min`, patience 4 |
| Side early stopping | `val_loss/min`, patience 5 | `val_loss/min`, patience 5 |
| Scheduler | unchanged; effective patience Front=1, Side=2; monitor `val_macro_f1/max` | unchanged |
| All other hyperparameters/data/split/augmentation | locked | locked |

## Verification after run

- Front selected epoch: 21; Side selected epoch: 26.
- Front checkpoint SHA-256: `9b3435c45ceddf974d644063239eedb9784be2b7d92294d3bde11d834e8eeadc`.
- Side checkpoint SHA-256: `6799d279f536f9f9d5949f04ed553084f67749f9d8b8c31a2141ff3b2ea3136e`.
- No output is written to the original `experiment_18` namespace by this controlled variant.

## Metadata note

- The baseline root `experiment_18/config/resolved_config.json` records Side scheduler patience as 1, while the baseline source/per-view training metadata records the effective Side value as 2. This variant preserves the effective source behavior (Side=2) and does not treat the stale root metadata value as a protocol change.
