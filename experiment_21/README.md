# experiment_21

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral factor change versus parent runtime recipe:

- Side augmentation policy: rotation `45 -> 30`, color jitter `0.8 -> 0.6`

Experiment_20 final moderate augmentation is evidence only, not runtime parent.

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 21 -To 21
```

Outputs are written under `experiment_21/results/`; checkpoints are written under `experiment_21/checkpoints/`.
