# experiment_20

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral change versus parent runtime recipe:

- Side checkpoint monitor: `val_loss -> val_macro_f1`

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 20 -To 20
```

Outputs are written under `experiment_20/results/`; checkpoints are written under `experiment_20/checkpoints/`.
Previous experiment_20 front-freeze4 artifacts are archived at `archive/experiment_20_front_freeze4/`.
