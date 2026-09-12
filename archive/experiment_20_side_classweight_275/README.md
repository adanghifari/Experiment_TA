# experiment_20

Controlled experiment from `experiment_18` / historical Exp 21D.

Only intentional behavioral change versus parent runtime recipe:

- Side class weight: `[2.5, 1.0] -> [2.75, 1.0]`

Class index order verified from source: index `0 = safe_driving`, index `1 = phone_use`.

Run from repository root when ready:

```powershell
.\run_all.ps1 -From 20 -To 20
```

Outputs are written under `experiment_20/results/`; checkpoints are written under `experiment_20/checkpoints/`.
Previous side dropout 0.5 variant is archived at `archive/experiment_20_side_dropout_05/`.
