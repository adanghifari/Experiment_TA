# Experiment 22

FINAL recipe exploration. Parent recipe: experiment_18.

Intentional behavioral change only: Side augmentation strength
- side rotation: 45 -> 35
- side color jitter: 0.8 -> 0.7

Front is exact experiment_18. Side is exact experiment_18 except the Side augmentation strength factor above. Train standalone from ImageNet pretrained; do not load checkpoints, predictions, or results from previous experiments.

Run command:
```powershell
.\run_all.ps1 -From 22 -To 22
```
