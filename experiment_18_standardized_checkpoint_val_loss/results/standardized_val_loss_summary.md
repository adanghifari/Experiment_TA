# Controlled variant run summary

Experiment: `experiment_18_standardized_checkpoint_val_loss`

Status: **completed**

## Protocol

- Front checkpoint selection: `val_loss`, minimize.
- Side checkpoint selection: `val_loss`, minimize.
- Front early stopping: `val_macro_f1`, maximize, patience 4.
- Side early stopping: `val_loss`, minimize, patience 5.
- Scheduler: `ReduceLROnPlateau`, monitor `val_macro_f1`, mode maximize.
- Scheduler patience: Front 1, Side 2.
- Maximum epochs: 30.
- Seed: 42.
- Frame stride: 30.
- Class weights: `[2.5, 1.0]`.

The checkpoint tracker and early-stopping tracker are separate in `src/train.py`. The scheduler remains stepped after validation Macro F1.

## Execution record

Command: `./run_experiment.ps1`

The first attempt stopped before training because the sandbox could not start the virtualenv's Python launcher. It created no new artifact. The rerun completed successfully with the repository virtualenv, PyTorch `2.11.0+cu128`, CUDA 12.8, and NVIDIA GeForce RTX 5060 Laptop GPU.

The completed pipeline included:

- Front training and Side training.
- Evaluation on train, validation, and test splits for both views.
- Test average fusion and adaptive fusion.
- Summary metadata and figures.

## Checkpoint results

| View | Selected epoch | Selection metric | Mode | Early-stopping monitor | Epochs executed | SHA-256 |
|---|---:|---|---|---|---:|---|
| Front | 12 | `val_loss = 0.50961` | min | `val_macro_f1`, max, patience 4 | 13 | `16d0f46c6e75a295c5ca18f3a2d8258420ce99f1ee359d5392e58e63efd2181b` |
| Side | 26 | `val_loss = 0.50217` | min | `val_loss`, min, patience 5 | 30 | `a3494d74bdfac0ca2de936b5b1dfb7197312fc0bd4891b56166235f34421f7a9` |

Checkpoint paths:

- `checkpoints/standardized_val_loss/front/best.pt`
- `checkpoints/standardized_val_loss/side/best.pt`

## Selected-epoch validation metrics

| View | Train loss | Validation loss | Validation Macro F1 | Validation accuracy | Learning rate |
|---|---:|---:|---:|---:|---:|
| Front, epoch 12 | 0.41722 | 0.50961 | 0.71892 | 0.84889 | `1.5e-5` |
| Side, epoch 26 | 0.39480 | 0.50217 | 0.68238 | 0.80889 | `1.25e-6` |

## Test metrics

| Model | Accuracy | Macro F1 | ROC-AUC | PR-AUC | ECE | Brier |
|---|---:|---:|---:|---:|---:|---:|
| Front | 0.87273 | 0.77256 | 0.88958 | 0.97330 | 0.09754 | 0.10548 |
| Side | 0.80455 | 0.67468 | 0.75444 | 0.92515 | 0.16761 | 0.15333 |
| Average fusion | 0.87273 | 0.76751 | 0.86917 | 0.96417 | 0.14479 | 0.11834 |
| Adaptive fusion | 0.87273 | 0.76751 | 0.87069 | 0.96519 | 0.14369 | 0.11489 |

Fusion complementarity on 220 paired test samples:

- Both correct: 166
- Both wrong: 17
- Front correct / Side wrong: 26
- Front wrong / Side correct: 11
- Average fusion fixed Front errors: 8
- Average fusion broke Front-correct cases: 8
- Adaptive fusion fixed Front errors: 8
- Adaptive fusion broke Front-correct cases: 8

## Artifact index

- `config/resolved_config.json`
- `results/standardized_val_loss/front/history.json` and `.csv`
- `results/standardized_val_loss/side/history.json` and `.csv`
- `results/standardized_val_loss/front/train_summary.json`
- `results/standardized_val_loss/side/train_summary.json`
- `results/standardized_val_loss/front/{train,val,test}_eval_metrics.json`
- `results/standardized_val_loss/side/{train,val,test}_eval_metrics.json`
- `results/standardized_val_loss/fusion/fusion_metrics.json`
- `results/standardized_val_loss/predictions/`
- `results/standardized_val_loss/run_metadata.json`
- `results/standardized_val_loss/best_checkpoint_metadata.json`
- `results/standardized_val_loss/confusion_matrices.json`
- `results/standardized_val_loss/figures/`

No manuscript was edited, no historical repository was used, and no Git commit was created.
