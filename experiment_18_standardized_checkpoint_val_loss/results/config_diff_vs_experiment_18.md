# Configuration diff: experiment_18 vs controlled variant

This file records the pre-run configuration audit. It does not report a completed training run.

## Intentional methodological change

| Item | `experiment_18` | Controlled variant |
|---|---|---|
| Front checkpoint monitor | `val_macro_f1` | `val_loss` |
| Front checkpoint mode | maximize | minimize |
| Side checkpoint monitor | `val_loss` | `val_loss` |
| Side checkpoint mode | minimize | minimize |

## Preserved training behavior

| Item | Front | Side |
|---|---:|---:|
| Early-stopping monitor | `val_macro_f1` | `val_loss` |
| Early-stopping mode | maximize | minimize |
| Early-stopping patience | 4 | 5 |
| Scheduler monitor | `val_macro_f1` | `val_macro_f1` |
| Scheduler mode | maximize | maximize |
| Scheduler patience | 1 | 2 |
| Maximum epochs | 30 | 30 |
| Learning rate | `3e-5` | `2e-5` |
| Weight decay | `5e-4` | `1e-3` |
| Freeze stages | 5 | 4 |
| Class weights | `[2.5, 1.0]` | `[2.5, 1.0]` |
| Frame stride | 30 | 30 |
| Seed | 42 | 42 |

## Implementation requirement

The training loop now maintains separate trackers:

- `BestMetric` selects and saves the checkpoint according to the configured checkpoint monitor.
- `EarlyStopping` monitors the unchanged early-stopping metric and controls only when training stops.
- `ReduceLROnPlateau` remains stepped on validation Macro F1 after each validation epoch.

## Output isolation

The pre-existing copied artifacts under `checkpoints/` and `results/` are retained. New outputs, when the run is explicitly authorized, will use:

- `checkpoints/standardized_val_loss/`
- `results/standardized_val_loss/`

## Run status

**Completed.** The runner was executed as `./run_experiment.ps1` after the pre-run audit. The first sandbox attempt stopped before training because its Python launcher was inaccessible; no artifact was created by that attempt. The same runner then completed successfully using the repository virtualenv with PyTorch 2.11.0+cu128 on an NVIDIA GeForce RTX 5060 Laptop GPU.

The completed pipeline ran Front and Side training, train/validation/test evaluation, test fusion, and summary generation. All new artifacts are isolated under `checkpoints/standardized_val_loss/` and `results/standardized_val_loss/`; pre-existing copied artifacts were not overwritten.
