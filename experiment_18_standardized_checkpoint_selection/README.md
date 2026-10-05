# experiment_18_standardized_checkpoint_selection

Varian terisolasi dari `experiment_18` untuk menguji standardisasi pemilihan checkpoint.

Perubahan tunggal yang diuji: checkpoint Side dipilih berdasarkan `val_macro_f1/max`.
Early stopping Side tetap terpisah dan menggunakan `val_loss/min` dengan patience yang
sama seperti `experiment_18`; scheduler tetap memonitor `val_macro_f1`.

Front menggunakan checkpoint `val_macro_f1/max` seperti semula. Seluruh parameter data,
split, seed, augmentasi, class weights, loss, optimizer, stride, dan hyperparameter lain
dipertahankan dari `experiment_18`. Folder induk tidak ditimpa.

Hasil dan audit perbandingan tersedia di `results/comparison_to_experiment_18.md` dan
`results/comparison_to_experiment_18.json`.
