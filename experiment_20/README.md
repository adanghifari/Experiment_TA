# experiment_20

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral factor change versus parent runtime recipe:

- Side augmentation policy: rotation `45 -> 20`, color jitter `0.8 -> 0.4`

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 20 -To 20
```

Outputs are written under `experiment_20/results/`; checkpoints are written under `experiment_20/checkpoints/`.
Previous side LR 1.5e-5 variant is archived at `archive/experiment_20_side_lr_15e5/`.
