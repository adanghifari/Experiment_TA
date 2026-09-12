# experiment_20

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral change versus parent runtime recipe:

- Side learning rate: `2e-5 -> 1.5e-5`

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 20 -To 20
```

Outputs are written under `experiment_20/results/`; checkpoints are written under `experiment_20/checkpoints/`.
Previous side classweight 2.25 variant is archived at `archive/experiment_20_side_classweight_225/`.
