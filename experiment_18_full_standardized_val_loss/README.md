# experiment_18_full_standardized_val_loss

Full standardized model-selection protocol derived from `experiment_18`.

- Front checkpoint: `val_loss`, minimize
- Side checkpoint: `val_loss`, minimize
- Front early stopping: `val_loss`, minimize, original patience 4
- Side early stopping: `val_loss`, minimize, original patience 5
- Scheduler remains `val_macro_f1`, maximize, with original patience Front 1 and Side 2

Checkpoint selection and early stopping are explicit independent fields in `src/train.py`. All other data, preprocessing, augmentation, model, loss, optimizer, hyperparameters, split, seed, and fusion behavior are inherited from `experiment_18`.

The copied baseline artifacts in `checkpoints/` and `results/` are retained. New outputs use `checkpoints/full_standardized_val_loss/` and `results/full_standardized_val_loss/`.
