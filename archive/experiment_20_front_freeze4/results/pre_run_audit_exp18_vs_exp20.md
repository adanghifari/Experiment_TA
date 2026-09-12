# Pre-run Hard Audit: experiment_18 vs experiment_20

Scope: audit sebelum training. Tidak ada checkpoint/result lama yang disalin. Training belum dijalankan.

Expected difference: `Front freeze` berubah `5 -> 4`. Semua parameter lain harus match.

## Verdict

PASS: hanya intentional difference yang ditemukan.

## Audit Table

| Parameter | Experiment 18 | Experiment 20 | Status |
|---|---|---|---|
| seed | 42 | 42 | EXACT MATCH |
| stride | 30 | 30 | EXACT MATCH |
| image_size | 224 | 224 | EXACT MATCH |
| batch_size | 32 | 32 | EXACT MATCH |
| max_epochs | 30 | 30 | EXACT MATCH |
| architecture | EfficientNetV2-S | EfficientNetV2-S | EXACT MATCH |
| pretrained | True | True | EXACT MATCH |
| optimizer | AdamW | AdamW | EXACT MATCH |
| label_smoothing | 0.0 | 0.0 | EXACT MATCH |
| class_weights | [2.5,1.0] | [2.5,1.0] | EXACT MATCH |
| threshold | 0.5 | 0.5 | EXACT MATCH |
| fusion_implementation | average=0.5*front+0.5*side; adaptive=confidence softmax abs(prob-threshold) | average=0.5*front+0.5*side; adaptive=confidence softmax abs(prob-threshold) | EXACT MATCH |
| loss | CrossEntropyLoss | CrossEntropyLoss | EXACT MATCH |
| Front lr | 3e-05 | 3e-05 | EXACT MATCH |
| Front weight_decay | 0.0005 | 0.0005 | EXACT MATCH |
| Front dropout | 0.4 | 0.4 | EXACT MATCH |
| Front freeze | 5 | 4 | INTENTIONAL DIFFERENCE |
| Front gamma | 1.0 | 1.0 | EXACT MATCH |
| Front augmentation | {"random_horizontal_flip_p":0.5,"random_rotation_degree":68,"color_jitter_factor":1.2} | {"random_horizontal_flip_p":0.5,"random_rotation_degree":68,"color_jitter_factor":1.2} | EXACT MATCH |
| Front scheduler | ReduceLROnPlateau | ReduceLROnPlateau | EXACT MATCH |
| Front scheduler_factor | 0.5 | 0.5 | EXACT MATCH |
| Front scheduler_patience | 1 | 1 | EXACT MATCH |
| Front early_stopping | 4 | 4 | EXACT MATCH |
| Front checkpoint_monitor | val_macro_f1 | val_macro_f1 | EXACT MATCH |
| Side lr | 2e-05 | 2e-05 | EXACT MATCH |
| Side weight_decay | 0.001 | 0.001 | EXACT MATCH |
| Side dropout | 0.4 | 0.4 | EXACT MATCH |
| Side freeze | 4 | 4 | EXACT MATCH |
| Side gamma | 1.0 | 1.0 | EXACT MATCH |
| Side augmentation | {"random_horizontal_flip_p":0.5,"random_rotation_degree":45,"color_jitter_factor":0.8} | {"random_horizontal_flip_p":0.5,"random_rotation_degree":45,"color_jitter_factor":0.8} | EXACT MATCH |
| Side scheduler | ReduceLROnPlateau | ReduceLROnPlateau | EXACT MATCH |
| Side scheduler_factor | 0.5 | 0.5 | EXACT MATCH |
| Side scheduler_patience | 2 | 2 | EXACT MATCH |
| Side early_stopping | 5 | 5 | EXACT MATCH |
| Side checkpoint_monitor | val_loss | val_loss | EXACT MATCH |
| subject split IDs | {"train":["5","6","7","9","12","13","14","16","18","19","23","24","25","26","28","29","30","31","32","33","34","35","36","37","38","39","40","43","44","45","46","47","48","49","50"],"val":["1","2","3","15","20","22","27","41"],"test":["4","8","10","11","17","21","42"]} | {"train":["5","6","7","9","12","13","14","16","18","19","23","24","25","26","28","29","30","31","32","33","34","35","36","37","38","39","40","43","44","45","46","47","48","49","50"],"val":["1","2","3","15","20","22","27","41"],"test":["4","8","10","11","17","21","42"]} | EXACT MATCH |
| sample counts stride 30 | {"front_train":1084,"front_val":225,"front_test":220,"side_train":1084,"side_val":225,"side_test":220} | {"front_train":1084,"front_val":225,"front_test":220,"side_train":1084,"side_val":225,"side_test":220} | EXACT MATCH |
| seed runtime mechanism | random/numpy/torch/torch.cuda before DataLoader construction and model initialization | same source copied from experiment_18; seed_everything(SPLIT_SEED) before get_all_dataloaders and build_model | EXACT MATCH VERIFIED IN SOURCE FLOW |

## Run Command

```powershell
.\run_all.ps1 -From 20 -To 20
```

Optional raw data override:

```powershell
.\run_all.ps1 -From 20 -To 20 -RawDataDir "D:\Skripsi\Experiment_TA\data\raw"
```