# experiment_18_standardized_checkpoint_val_loss

Controlled variant dari `experiment_18` untuk menyamakan checkpoint selection:

- Front: `val_loss`, minimize
- Side: `val_loss`, minimize
- Front early stopping: `val_macro_f1`, maximize, patience 4
- Side early stopping: `val_loss`, minimize, patience 5
- Scheduler: `val_macro_f1`, maximize; patience Front 1 dan Side 2

Checkpoint selection dan early stopping dipisahkan di `src/train.py`. Artefak salinan lama yang sudah ada di `checkpoints/` dan `results/` tidak digunakan atau ditimpa; output variant ditulis ke namespace `checkpoints/standardized_val_loss/` dan `results/standardized_val_loss/`.

Jalankan dari folder variant setelah pre-run audit selesai:

```powershell
.\run_experiment.ps1
```

Audit konfigurasi dan perbedaan terhadap baseline tercatat di `results/config_diff_vs_experiment_18.md`. Hasil run terdokumentasi di `results/standardized_val_loss_summary.md`.
