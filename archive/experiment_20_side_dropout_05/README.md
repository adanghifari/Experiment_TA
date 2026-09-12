# experiment_20

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral change versus parent runtime recipe:

- Side dropout: `0.4 -> 0.5`

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 20 -To 20
```

Outputs are written under `experiment_20/results/`; checkpoints are written under `experiment_20/checkpoints/`.
Previous side checkpoint-monitor variant is archived at `archive/experiment_20_side_val_macro_f1/`.
