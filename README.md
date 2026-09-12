# Eksperimen Tugas Akhir

Repository ini berisi 19 eksperimen utama untuk klasifikasi perilaku pengemudi menggunakan EfficientNetV2-S dan decision-level fusion.

Dataset raw tidak disalin ke repository ini. Path default dataset:

```powershell
D:\Skripsi\Experiment_TA\data\raw
```

Struktur setiap eksperimen:

```text
experiment_X/
  checkpoints/
  config/
  notebooks/
  results/
  src/
  run_experiment.ps1
```

Setiap folder eksperimen berdiri sendiri dan memiliki konfigurasi, source code, checkpoint, serta hasil masing-masing.

## Setup

```powershell
cd D:\Skripsi\Experiment_TA
.\.venv\Scripts\Activate.ps1
pip install -r requirements-training.txt
```

## Menjalankan Eksperimen

Satu eksperimen:

```powershell
cd D:\Skripsi\Experiment_TA
.\run_all.ps1 -From 1 -To 1
```

Rentang eksperimen:

```powershell
cd D:\Skripsi\Experiment_TA
.\run_all.ps1 -From 1 -To 19
```

Output utama tersimpan di folder `results/` masing-masing eksperimen, termasuk history training, evaluasi train/validation/test, fusion metrics, prediksi, grafik, metadata run, dan SHA256 checkpoint.

## Catatan

Semua eksperimen menggunakan seed 42 untuk menjaga konsistensi hasil antar eksekusi.

