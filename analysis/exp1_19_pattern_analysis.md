# Experiment 1-19 Hyperparameter Pattern Analysis

Analisis ini hanya ekstraksi pola deskriptif. Tidak ada retraining, tidak ada perubahan checkpoint/config, dan tidak ada klaim sebab-akibat.

Semua metrik hasil berasal dari artifact repo baru. Angka historical repo lama tidak dipakai sebagai hasil; hanya kolom mapping historis yang dipakai sebagai identitas.

Catatan protokol penting: eksperimen memakai stride/sample count berbeda. Stride 15, 20, dan 30 tidak digabung sebagai protokol identik; setiap ringkasan grup menampilkan stride/sample count yang hadir.

## LR vs Performance/Stability

LR dibaca deskriptif per-view. Nilai ini sering berubah bersama WD, freeze, dropout, augmentasi, dan stride.

### Front LR

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 5e-05 | 4 | 0.83327 | 0.87074 | 0.12806 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.0001 | 2 | 0.82587 | 0.83402 | 0.11823 | stride 15 test front=419;side=419 | experiment_2 |
| 3e-05 | 10 | 0.7812 | 0.81113 | 0.05428 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |
| 1e-05 | 3 | 0.66393 | 0.79023 | 0.07326 | stride 15 test front=419;side=419 | experiment_5 |

### Side LR

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 2e-05 | 11 | 0.7899 | 0.87074 | 0.06663 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| 5e-05 | 2 | 0.83813 | 0.85253 | 0.14495 | stride 15 test front=419;side=419 | experiment_4 |
| 0.0001 | 2 | 0.82587 | 0.83402 | 0.11823 | stride 15 test front=419;side=419 | experiment_2 |
| 1e-05 | 3 | 0.66393 | 0.79023 | 0.07326 | stride 15 test front=419;side=419 | experiment_5 |
| 3e-05 | 1 | 0.77992 | 0.77992 | 0.03227 | stride 30 test front=220;side=220 | experiment_15 |

## WD vs Performance/Stability

Weight decay dibaca sebagai pola grup, bukan efek tunggal.

### Front Weight Decay

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0005 | 8 | 0.80965 | 0.87074 | 0.08501 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| 0.0001 | 2 | 0.82887 | 0.83402 | 0.12656 | stride 15 test front=419;side=419 | experiment_2 |
| 0.0 | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| 0.002 | 3 | 0.77083 | 0.78412 | 0.05093 | stride 30 test front=220;side=220 | experiment_13 |
| 0.0003 | 2 | 0.78025 | 0.78059 | 0.04338 | stride 30 test front=220;side=220 | experiment_14 |
| 0.01 | 2 | 0.67667 | 0.76142 | 0.05608 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_12 |
| 0.001 | 1 | 0.60963 | 0.60963 | 0.09839 | stride 15 test front=419;side=419 | experiment_6 |

### Side Weight Decay

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0005 | 6 | 0.8119 | 0.87074 | 0.09102 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| 0.0001 | 3 | 0.81255 | 0.83402 | 0.09513 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_2 |
| 0.0 | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| 0.001 | 3 | 0.73849 | 0.81113 | 0.07744 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_18 |
| 0.002 | 4 | 0.77327 | 0.78412 | 0.05182 | stride 30 test front=220;side=220 | experiment_13 |
| 0.01 | 2 | 0.67667 | 0.76142 | 0.05608 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_12 |

## Dropout vs Performance/Stability

Dropout tinggi/rendah ikut bercampur dengan freeze dan augmentasi.

### Front Dropout

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 8 | 0.79669 | 0.87074 | 0.07542 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.3 | 3 | 0.82516 | 0.83402 | 0.12705 | stride 15 test front=419;side=419 | experiment_2 |
| 0.4 | 6 | 0.78969 | 0.81113 | 0.05885 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |
| 0.6 | 2 | 0.60078 | 0.60963 | 0.08682 | stride 15 test front=419;side=419 | experiment_6 |

### Side Dropout

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 5 | 0.81331 | 0.87074 | 0.09051 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.3 | 11 | 0.79177 | 0.83402 | 0.07436 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_2 |
| 0.4 | 1 | 0.81113 | 0.81113 | 0.06714 | stride 30 test front=220;side=220 | experiment_18 |
| 0.6 | 2 | 0.60078 | 0.60963 | 0.08682 | stride 15 test front=419;side=419 | experiment_6 |

## Freeze Stage vs Performance/Stability

Freeze stage menunjukkan derajat fine-tuning per-view.

### Front Freeze stage

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 5 | 0.82672 | 0.87074 | 0.10442 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 2 | 1 | 0.82372 | 0.82372 | 0.14468 | stride 15 test front=419;side=419 | experiment_3 |
| 0 | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| 5 | 12 | 0.75113 | 0.81113 | 0.05971 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |

### Side Freeze stage

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 0.74959 | 0.87074 | 0.09919 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 4 | 13 | 0.79145 | 0.85253 | 0.06482 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_4 |
| 2 | 1 | 0.82372 | 0.82372 | 0.14468 | stride 15 test front=419;side=419 | experiment_3 |
| 0 | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| 5 | 1 | 0.60963 | 0.60963 | 0.09839 | stride 15 test front=419;side=419 | experiment_6 |

## Label Smoothing vs Performance/Stability

Label smoothing pada banyak eksperimen sama antar view, tetapi tetap diringkas per-view.

### Front Label smoothing

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 3 | 0.74959 | 0.87074 | 0.09919 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.0 | 13 | 0.78847 | 0.85253 | 0.08488 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_4 |
| 0.12 | 3 | 0.76326 | 0.76694 | 0.03678 | stride 30 test front=220;side=220 | experiment_10 |

### Side Label smoothing

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 3 | 0.74959 | 0.87074 | 0.09919 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.0 | 13 | 0.78847 | 0.85253 | 0.08488 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_4 |
| 0.12 | 3 | 0.76326 | 0.76694 | 0.03678 | stride 30 test front=220;side=220 | experiment_10 |

## Class Weight/Gamma vs Performance/Stability

Class weight/gamma ditampilkan sesuai resolved artifact repo baru, termasuk Exp15 yang view-specific.

### Front Class weight

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| [2.5,1.0] | 12 | 0.78907 | 0.87074 | 0.06376 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| [3.1036036036036037,0.5960207612456747] | 5 | 0.78203 | 0.85253 | 0.10857 | stride 15 test front=419;side=419 | experiment_4 |
| NA | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| [5.15,1.0] | 1 | 0.59192 | 0.59192 | 0.07525 | stride 15 test front=419;side=419 | experiment_7 |

### Front Class weight gamma

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 19 | 0.77835 | 0.87074 | 0.07954 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |

### Side Class weight

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| [2.5,1.0] | 11 | 0.7899 | 0.87074 | 0.06663 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| [3.1036036036036037,0.5960207612456747] | 5 | 0.78203 | 0.85253 | 0.10857 | stride 15 test front=419;side=419 | experiment_4 |
| NA | 1 | 0.81773 | 0.81773 | 0.12804 | stride 15 test front=419;side=419 | experiment_1 |
| [1.7548633720450872,0.7726035850029893] | 1 | 0.77992 | 0.77992 | 0.03227 | stride 30 test front=220;side=220 | experiment_15 |
| [5.15,1.0] | 1 | 0.59192 | 0.59192 | 0.07525 | stride 15 test front=419;side=419 | experiment_7 |

### Side Class weight gamma

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 18 | 0.77826 | 0.87074 | 0.08217 | stride 15 test front=419;side=419; stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_8 |
| 0.5 | 1 | 0.77992 | 0.77992 | 0.03227 | stride 30 test front=220;side=220 | experiment_15 |

## Augmentation Strength vs Performance/Stability

Rotation dan color jitter dipakai sebagai proxy kekuatan augmentasi.

### Front Rotation

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 4 | 0.7146 | 0.87074 | 0.09899 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 15 | 2 | 0.82138 | 0.85253 | 0.09568 | stride 15 test front=419;side=419 | experiment_4 |
| 10 | 3 | 0.82516 | 0.83402 | 0.12705 | stride 15 test front=419;side=419 | experiment_2 |
| 68 | 6 | 0.78969 | 0.81113 | 0.05885 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |
| 45 | 4 | 0.76848 | 0.78412 | 0.04743 | stride 30 test front=220;side=220 | experiment_13 |

### Front Color jitter

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.4 | 4 | 0.7146 | 0.87074 | 0.09899 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.3 | 2 | 0.82138 | 0.85253 | 0.09568 | stride 15 test front=419;side=419 | experiment_4 |
| 0.2 | 3 | 0.82516 | 0.83402 | 0.12705 | stride 15 test front=419;side=419 | experiment_2 |
| 1.2 | 6 | 0.78969 | 0.81113 | 0.05885 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |
| 0.8 | 3 | 0.76899 | 0.78412 | 0.05029 | stride 30 test front=220;side=220 | experiment_13 |
| 0.6 | 1 | 0.76694 | 0.76694 | 0.03884 | stride 30 test front=220;side=220 | experiment_10 |

### Side Rotation

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 4 | 0.7146 | 0.87074 | 0.09899 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 15 | 2 | 0.82138 | 0.85253 | 0.09568 | stride 15 test front=419;side=419 | experiment_4 |
| 10 | 3 | 0.82516 | 0.83402 | 0.12705 | stride 15 test front=419;side=419 | experiment_2 |
| 45 | 10 | 0.7812 | 0.81113 | 0.05428 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |

### Side Color jitter

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 0.4 | 4 | 0.7146 | 0.87074 | 0.09899 | stride 15 test front=419;side=419; stride 30 test front=220;side=220 | experiment_8 |
| 0.3 | 2 | 0.82138 | 0.85253 | 0.09568 | stride 15 test front=419;side=419 | experiment_4 |
| 0.2 | 3 | 0.82516 | 0.83402 | 0.12705 | stride 15 test front=419;side=419 | experiment_2 |
| 0.8 | 9 | 0.78279 | 0.81113 | 0.056 | stride 20 test front=322;side=322; stride 30 test front=220;side=220 | experiment_18 |
| 0.6 | 1 | 0.76694 | 0.76694 | 0.03884 | stride 30 test front=220;side=220 | experiment_10 |

## Stride vs Performance/Stability

Stride mengubah sample count/protokol, jadi pola lintas stride harus dibaca dengan batasan ini.

### Stride

| Parameter value | n | Avg fusion F1 mean | Avg fusion F1 max | Mean abs gap mean | Stride/sample counts present | Best experiment in group |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 8 | 0.77382 | 0.87074 | 0.10691 | stride 15 test front=419;side=419 | experiment_8 |
| 30 | 9 | 0.78071 | 0.81113 | 0.05817 | stride 30 test front=220;side=220 | experiment_18 |
| 20 | 2 | 0.78589 | 0.78589 | 0.06622 | stride 20 test front=322;side=322 | experiment_16 |

## Candidate Directions for Experiment 20

- Parameter yang terlihat promising untuk dinaikkan/diturunkan: sekitar LR front `5e-05` dan side `2e-05` muncul pada parent kuat Exp8; WD sekitar `0.0005` muncul pada grup dengan hasil maksimum tertinggi; augmentasi rotation `20` dan color jitter `0.4` muncul pada Exp8; side gamma `0.5` pada Exp15/18 memberi sinyal menarik pada stride 30, namun protokol/sample count berbeda perlu ditandai.
- Parameter yang terlihat berisiko: LR sangat rendah `5e-06`, dropout `0.6`, WD `0.01`, dan freeze stage sangat tinggi pada beberapa recipe tampil bersama fusion yang lebih rendah atau stabilitas yang tidak otomatis membaik.
- Eksperimen yang paling layak dijadikan parent: Exp8 untuk performa fusion tertinggi; Exp4 sebagai parent kuat stride 15 dengan label smoothing `0`; Exp18/Exp19 sebagai parent stride 30 bila prioritasnya eksplorasi protocol stride 30; Exp15 bila prioritasnya metadata/config view-specific class weighting yang bersih dan gap train-val kecil.
- Opsi controlled change 1: parent Exp8, ubah hanya label smoothing `0.1 -> 0.0` sambil menjaga LR/WD/dropout/freeze/augmentasi tetap.
- Opsi controlled change 2: parent Exp8, ubah hanya side class weight gamma `1.0 -> 0.5` sambil menjaga front static `[2.5,1.0]`.
- Opsi controlled change 3: parent Exp4 atau Exp8, ubah satu parameter regularisasi saja, misalnya dropout front/side `0.5 -> 0.4`, tanpa mengubah stride.