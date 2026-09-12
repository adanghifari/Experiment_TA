# Pre-run Hard Audit: experiment_18 vs experiment_21

Scope: audit sebelum training. `experiment_21` dibuat sebagai folder baru standalone dari parent recipe `experiment_18`; `experiment_20` hanya evidence, bukan runtime parent.

Expected only behavioral differences, satu experimental factor `Side augmentation policy`: `Side rotation 45 -> 30` dan `Side color jitter 0.8 -> 0.6`.

## Class Mapping Verification

`BINARY_LABEL_MAP = {"safe_driving":0,"phone_use":1}`. Side class weight tetap `[2.5,1.0]`, jadi index `0 = safe_driving`, index `1 = phone_use`.

## Verdict

PASS: hanya intentional differences pada side augmentation policy yang ditemukan.

## Audit Table

| Parameter | Experiment 18 | Experiment 21 | Status |
|---|---|---|---|
| seed | 42 | 42 | EXACT MATCH |
| stride | 30 | 30 | EXACT MATCH |
| subject split IDs | {"train":[5,6,7,9,12,13,14,16,18,19,23,24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,43,44,45,46,47,48,49,50],"val":[1,2,3,15,20,22,27,41],"test":[4,8,10,11,17,21,42]} | {"train":[5,6,7,9,12,13,14,16,18,19,23,24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,43,44,45,46,47,48,49,50],"val":[1,2,3,15,20,22,27,41],"test":[4,8,10,11,17,21,42]} | EXACT MATCH |
| sample counts | {"front_train":1084,"front_val":225,"front_test":220,"side_train":1084,"side_val":225,"side_test":220} | {"front_train":1084,"front_val":225,"front_test":220,"side_train":1084,"side_val":225,"side_test":220} | EXACT MATCH |
| image size | 224 | 224 | EXACT MATCH |
| batch size | 32 | 32 | EXACT MATCH |
| max epochs | 30 | 30 | EXACT MATCH |
| backbone | "EfficientNetV2-S" | "EfficientNetV2-S" | EXACT MATCH |
| pretrained | true | true | EXACT MATCH |
| optimizer | "AdamW" | "AdamW" | EXACT MATCH |
| Front LR | 3e-05 | 3e-05 | EXACT MATCH |
| Front WD | 0.0005 | 0.0005 | EXACT MATCH |
| Front dropout | 0.4 | 0.4 | EXACT MATCH |
| Front freeze | 5 | 5 | EXACT MATCH |
| Front label smoothing | 0.0 | 0.0 | EXACT MATCH |
| Front class weight | [2.5,1.0] | [2.5,1.0] | EXACT MATCH |
| Front gamma | 1.0 | 1.0 | EXACT MATCH |
| Front RandomHorizontalFlip | true | true | EXACT MATCH |
| Front rotation | 68 | 68 | EXACT MATCH |
| Front color jitter | 1.2 | 1.2 | EXACT MATCH |
| Front scheduler | "ReduceLROnPlateau" | "ReduceLROnPlateau" | EXACT MATCH |
| Front scheduler factor | 0.5 | 0.5 | EXACT MATCH |
| Front scheduler patience | 1 | 1 | EXACT MATCH |
| Front early stopping | 4 | 4 | EXACT MATCH |
| Front checkpoint monitor | "val_macro_f1" | "val_macro_f1" | EXACT MATCH |
| Side LR | 2e-05 | 2e-05 | EXACT MATCH |
| Side WD | 0.001 | 0.001 | EXACT MATCH |
| Side dropout | 0.4 | 0.4 | EXACT MATCH |
| Side freeze | 4 | 4 | EXACT MATCH |
| Side label smoothing | 0.0 | 0.0 | EXACT MATCH |
| Side class weight | [2.5,1.0] | [2.5,1.0] | EXACT MATCH |
| Side gamma | 1.0 | 1.0 | EXACT MATCH |
| Side RandomHorizontalFlip | true | true | EXACT MATCH |
| Side rotation | 45 | 30 | INTENTIONAL DIFFERENCE |
| Side color jitter | 0.8 | 0.6 | INTENTIONAL DIFFERENCE |
| Side scheduler | "ReduceLROnPlateau" | "ReduceLROnPlateau" | EXACT MATCH |
| Side scheduler factor | 0.5 | 0.5 | EXACT MATCH |
| Side scheduler patience | 2 | 2 | EXACT MATCH |
| Side early stopping | 5 | 5 | EXACT MATCH |
| Side checkpoint monitor | "val_loss" | "val_loss" | EXACT MATCH |
| threshold | 0.5 | 0.5 | EXACT MATCH |
| loss function | "CrossEntropyLoss" | "CrossEntropyLoss" | EXACT MATCH |
| class mapping | {"safe_driving":0,"phone_use":1} | {"safe_driving":0,"phone_use":1} | VERIFIED |
| fusion implementation | "average=0.5*front+0.5*side; adaptive=confidence softmax abs(prob-threshold)" | "same source copied from experiment_18" | EXACT MATCH VERIFIED IN SOURCE FLOW |
| seed runtime mechanism | "random/numpy/torch/torch.cuda seeded before DataLoader/model init" | "same copied source flow" | EXACT MATCH VERIFIED IN SOURCE FLOW |
| output folder reset | "experiment_21 results/checkpoints empty before run except .gitkeep and audit" | "experiment_21 results/checkpoints empty before run except .gitkeep and audit" | VERIFIED |

## Run Command

```powershell
.\run_all.ps1 -From 21 -To 21
```