# Factual Audit: Checkpoint Selection and Class-Weight Provenance

Tanggal audit: 2026-09-18  
Repository authoritative: D:\Skripsi\Experiment_TA  
Paper: D:\Skripsi\Paper_TA\main.tex dan D:\Skripsi\Paper_TA\sections\  
Historical fallback: D:\Skripsi\Experiment

Audit ini read-only terhadap paper, source code, checkpoint, log, konfigurasi, dan artefak historis. Tidak ada retraining, inference baru, perubahan manuscript/source code, perubahan checkpoint, atau Git commit.

## 1. Executive summary

### Resolver final artifact

Final model yang dipakai paper dapat di-resolve ke experiment_18 berdasarkan kecocokan artefak, bukan nama folder:

- D:\Skripsi\Experiment_TA\experiment_index.csv:19 memetakan experiment_18 ke Exp 21D, stride 30, Front test Macro F1 0.76626, Side test Macro F1 0.67468, status artifact_aligned.
- D:\Skripsi\Experiment_TA\master_experiment_summary.md:22 mencatat monitor Front val_macro_f1, monitor Side val_loss, Front best epoch 9, Side best epoch 26, serta nilai test yang sama dengan paper.
- experiment_16 tidak dipakai sebagai final paper artifact: Side test Macro F1-nya 0.75905, bukan 0.67468.

### Audit A

Implementasi authoritative membuktikan bahwa kriteria berbeda dan bagaimana kriteria itu diterapkan:

- Front: maksimum val_macro_f1.
- Side: minimum val_loss.
- Early stopping memakai metric dan arah yang sama dengan best-checkpoint selection.
- LR scheduler tidak memakai metric yang sama: scheduler selalu menerima val_macro_f1 dengan mode max, termasuk untuk Side.

Dokumentasi historical fallback secara eksplisit menghubungkan keputusan Side val_loss dengan stabilisasi probabilitas fusion dan pengujian overfit/loss gap. Jadi, dengan historical fallback yang diwajibkan bila authoritative repository tidak cukup, terdapat evidence kuat untuk alasan perbedaan kriteria. Namun, authoritative repository sendiri tidak memuat catatan contemporaneous yang membuktikan kapan alasan tersebut pertama kali ditetapkan atau bahwa keputusan itu telah dipra-registrasi.

**Checkpoint audit verdict: STATUS A — Strong evidence exists for why the criteria differ.**

### Audit B

[2.5, 1.0] terbukti sebagai fixed literal yang dipakai oleh CrossEntropyLoss dalam urutan class index [safe_driving=0, phone_use=1]. Final authoritative artifacts tidak memuat formula pembangkit atau log validasi yang memilih angka tersebut. Historical source menelusurinya ke konfigurasi Exp8 dan menyebutnya sebagai bobot moderat untuk safe_driving.

Perbandingan matematis dengan distribusi 176/908 menunjukkan bahwa [2.5,1.0] bukan inverse-frequency standar, bukan sklearn balanced weight, dan bukan rescaling langsung dari rasio frekuensi.

**Class-weight provenance classification: 4. inherited configuration.**  
Confidence: **Medium** — implementasinya High-confidence; alasan numerik awalnya tidak tercatat sebagai formula atau eksperimen seleksi final yang lengkap.

## 2. Audit A — checkpoint criterion

### A1. Final configuration evidence

File: D:\Skripsi\Experiment_TA\experiment_18\src\config.py:33-34

~~~
CHECKPOINT_MONITOR_FRONT = 'val_macro_f1'
CHECKPOINT_MONITOR_SIDE = 'val_loss'
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\config\resolved_config.json:24-25

~~~
"checkpoint_monitor_front": "val_macro_f1",
"checkpoint_monitor_side": "val_loss",
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\config\resolved_config.json:2-6,16-17

~~~
"frame_stride": 30,
"learning_rate_front": 3e-05,
"learning_rate_side": 2e-05,
"weight_decay_front": 0.0005,
"weight_decay_side": 0.001,
"freeze_front": 5,
"freeze_side": 4,
~~~

Catatan: root resolved_config.json mencatat scheduler_patience_side=1, sementara source config.py:152, per-view train_summary.json, dan training-resolved metadata mencatat Side scheduler patience 2. Perbedaan metadata ini tidak mengubah metric scheduler: metric-nya tetap val_macro_f1.

### A2. Exact implementation evidence

#### Metric and optimization direction

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:78-82

~~~
checkpoint_monitor = checkpoint_monitor or (CHECKPOINT_MONITOR_FRONT if view == 'front' else CHECKPOINT_MONITOR_SIDE)
class_weight_gamma = class_weight_gamma if class_weight_gamma is not None else (CLASS_WEIGHT_GAMMA_FRONT if view == 'front' else CLASS_WEIGHT_GAMMA_SIDE)
ls = LABEL_SMOOTHING
weights = resolve_class_weights(view, exp_config, class_weight_gamma)
mode = 'min' if checkpoint_monitor == 'val_loss' else 'max'
~~~

Artinya:

- Front val_macro_f1 memakai mode max.
- Side val_loss memakai mode min.

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:52-58

~~~
class EarlyStopping:
    def __init__(self, patience, mode='max'):
        self.patience=patience; self.mode=mode; self.best=-float('inf') if mode=='max' else float('inf'); self.counter=0; self.should_stop=False
    def step(self, score):
        ok=score>self.best if self.mode=='max' else score<self.best
        if ok: self.best=score; self.counter=0; return True
        self.counter+=1; self.should_stop=self.counter>=self.patience; return False
~~~

#### Loss, scheduler, early stopping, dan best-checkpoint save

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:110

~~~
model=build_model(PRETRAINED,freeze,dropout).to(device); criterion=nn.CrossEntropyLoss(weight=torch.tensor(weights,dtype=torch.float).to(device),label_smoothing=ls); opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=wd); sch=torch.optim.lr_scheduler.ReduceLROnPlateau(opt,mode='max',factor=LR_SCHEDULER_FACTOR,patience=sched_pat); early=EarlyStopping(patience,mode)
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:115

~~~
resolved={... 'checkpoint_monitor':checkpoint_monitor,'checkpoint_monitor_mode':mode,... 'scheduler':'ReduceLROnPlateau','scheduler_monitor':'val_macro_f1','scheduler_step_timing':'after_validation', ...}
~~~

Field scheduler_monitor yang tersimpan adalah persis val_macro_f1.

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:120-124

~~~
va_loss,va=validate(model,loaders['val'],criterion,device,epoch); sch.step(va['macro_f1'])
row={'epoch':epoch, ... 'val_loss':round(va_loss,5), ... 'val_macro_f1':round(va['macro_f1'],5), ...}
rows.append(row); score=row[checkpoint_monitor]; is_best=early.step(score)
if is_best:
    best_epoch=epoch; torch.save({...,'checkpoint_selection':{'monitored_metric':checkpoint_monitor,'mode':mode,'best_epoch':epoch,'reason':f'Best validation {checkpoint_monitor} so far.'}},ckpt)
~~~

Konsekuensi implementasi yang dapat dibuktikan:

1. score=row[checkpoint_monitor], sehingga metric best checkpoint mengikuti view-specific checkpoint_monitor.
2. early.step(score) memakai score yang sama, sehingga best checkpoint dan early-stopping monitor adalah criterion yang sama.
3. sch.step(va['macro_f1']) tidak mengikuti checkpoint_monitor; scheduler selalu memonitor validation Macro F1.
4. Scheduler mode selalu max, termasuk Side.
5. Checkpoint menyimpan monitored_metric, mode, dan best_epoch di metadata.

#### Ringkasan implementation behavior

| View | Best checkpoint | Direction | Early stopping | LR scheduler | Sama dengan checkpoint criterion? |
|---|---|---|---|---|---|
| Front | val_macro_f1 | max | val_macro_f1 / max | val_macro_f1 / max | Yes |
| Side | val_loss | min | val_loss / min | val_macro_f1 / max | No |

### A3. Checkpoint yang benar-benar dipakai paper

D:\Skripsi\Experiment_TA\experiment_18\results\front\train_summary.json mencatat:

~~~
"best_epoch": 9,
"checkpoint_selection": {
  "monitored_metric": "val_macro_f1",
  "mode": "max",
  "reason": "Selected by validation val_macro_f1."
}
~~~

D:\Skripsi\Experiment_TA\experiment_18\results\side\train_summary.json mencatat:

~~~
"best_epoch": 26,
"checkpoint_selection": {
  "monitored_metric": "val_loss",
  "mode": "min",
  "reason": "Selected by validation val_loss."
}
~~~

Kecocokan checkpoint final diverifikasi dari path dan SHA256 pada train summary, validation evaluation, dan test evaluation:

| View | Checkpoint | SHA256 | Best epoch | Test Macro F1 | Evidence |
|---|---|---|---:|---:|---|
| Front | experiment_18/checkpoints/front/best.pt | 1e8036ddb330649d7e51a7dc56cc697c915fb44a7e9873abb7dd440062b6ba35 | 9 | 0.76626 | results/front/test_eval_metrics.json |
| Side | experiment_18/checkpoints/side/best.pt | a37aedc2a5f5c3a02877a370ac67964663a409789134b949966d6c52802023fc | 26 | 0.67468 | results/side/test_eval_metrics.json |

Jadi checkpoint yang dipakai paper konsisten dengan implementasi dan dengan nilai test paper.

### A4. Validation-history evidence

Sumber history:

- D:\Skripsi\Experiment_TA\experiment_18\results\front\history.csv
- D:\Skripsi\Experiment_TA\experiment_18\results\side\history.csv

Kolom train_macro_f1 tidak direkonstruksi atau digunakan dalam tabel berikut; hanya field yang diminta dan tersedia di log yang dilaporkan.

#### Front history

| epoch | train_loss | val_loss | val_macro_f1 | val_accuracy | learning_rate | checkpoint selected? |
|---:|---:|---:|---:|---:|---:|:---:|
| 1 | 0.68932 | 0.63331 | 0.57331 | 0.8 | 3e-05 | no |
| 2 | 0.62853 | 0.61716 | 0.60011 | 0.81778 | 3e-05 | no |
| 3 | 0.59312 | 0.61332 | 0.64747 | 0.8 | 3e-05 | no |
| 4 | 0.54896 | 0.59023 | 0.64845 | 0.80889 | 3e-05 | no |
| 5 | 0.52988 | 0.55668 | 0.65328 | 0.84889 | 3e-05 | no |
| 6 | 0.50284 | 0.54337 | 0.69549 | 0.84 | 3e-05 | no |
| 7 | 0.50961 | 0.52457 | 0.71596 | 0.83556 | 3e-05 | no |
| 8 | 0.48857 | 0.52586 | 0.70060 | 0.82667 | 3e-05 | no |
| 9 | 0.47353 | 0.51736 | 0.72581 | 0.84444 | 3e-05 | yes |
| 10 | 0.44571 | 0.53340 | 0.68375 | 0.80444 | 3e-05 | no |
| 11 | 0.41193 | 0.51456 | 0.72000 | 0.84444 | 1.5e-05 | no |
| 12 | 0.41722 | 0.50961 | 0.71892 | 0.84889 | 1.5e-05 | no |
| 13 | 0.38726 | 0.52036 | 0.71666 | 0.83111 | 7.5e-06 | no |

Front:

- Best validation Macro F1: epoch 9, 0.72581.
- Minimum validation loss: epoch 12, 0.50961.
- Same epoch? **No**.
- Checkpoint actually used: epoch 9, selected by val_macro_f1.

#### Side history

| epoch | train_loss | val_loss | val_macro_f1 | val_accuracy | learning_rate | checkpoint selected? |
|---:|---:|---:|---:|---:|---:|:---:|
| 1 | 0.68783 | 0.61984 | 0.45783 | 0.84444 | 2e-05 | no |
| 2 | 0.66351 | 0.61456 | 0.45122 | 0.82222 | 2e-05 | no |
| 3 | 0.62094 | 0.61117 | 0.47671 | 0.82667 | 2e-05 | no |
| 4 | 0.61543 | 0.60593 | 0.45255 | 0.82667 | 2e-05 | no |
| 5 | 0.60473 | 0.59085 | 0.45783 | 0.84444 | 2e-05 | no |
| 6 | 0.57667 | 0.58139 | 0.45652 | 0.84 | 1e-05 | no |
| 7 | 0.56428 | 0.57795 | 0.58836 | 0.84889 | 1e-05 | no |
| 8 | 0.56642 | 0.57338 | 0.53354 | 0.84889 | 1e-05 | no |
| 9 | 0.54957 | 0.56865 | 0.62212 | 0.85333 | 1e-05 | no |
| 10 | 0.54512 | 0.56729 | 0.71715 | 0.87111 | 1e-05 | no |
| 11 | 0.50576 | 0.56054 | 0.71447 | 0.87556 | 1e-05 | no |
| 12 | 0.53423 | 0.54875 | 0.74270 | 0.88444 | 1e-05 | no |
| 13 | 0.49931 | 0.55967 | 0.71241 | 0.84889 | 1e-05 | no |
| 14 | 0.51615 | 0.53427 | 0.73666 | 0.88 | 1e-05 | no |
| 15 | 0.48501 | 0.53991 | 0.75724 | 0.88 | 1e-05 | no |
| 16 | 0.48325 | 0.53097 | 0.72282 | 0.85778 | 1e-05 | no |
| 17 | 0.46293 | 0.52459 | 0.73468 | 0.86222 | 1e-05 | no |
| 18 | 0.43267 | 0.51556 | 0.74572 | 0.87111 | 5e-06 | no |
| 19 | 0.44828 | 0.51429 | 0.70533 | 0.83111 | 5e-06 | no |
| 20 | 0.42200 | 0.50778 | 0.72282 | 0.85778 | 5e-06 | no |
| 21 | 0.42589 | 0.50681 | 0.68983 | 0.82222 | 2.5e-06 | no |
| 22 | 0.40914 | 0.51567 | 0.67799 | 0.80444 | 2.5e-06 | no |
| 23 | 0.41379 | 0.51441 | 0.68684 | 0.81333 | 2.5e-06 | no |
| 24 | 0.40627 | 0.51341 | 0.67510 | 0.79556 | 1.25e-06 | no |
| 25 | 0.40850 | 0.50241 | 0.68684 | 0.81333 | 1.25e-06 | no |
| 26 | 0.39480 | 0.50217 | 0.68238 | 0.80889 | 1.25e-06 | yes |
| 27 | 0.42705 | 0.50756 | 0.67086 | 0.79111 | 6.25e-07 | no |
| 28 | 0.41742 | 0.50466 | 0.68983 | 0.82222 | 6.25e-07 | no |
| 29 | 0.40019 | 0.51380 | 0.66667 | 0.78667 | 6.25e-07 | no |
| 30 | 0.39814 | 0.50294 | 0.70060 | 0.82667 | 3.125e-07 | no |

Side:

- Best validation Macro F1: epoch 15, 0.75724.
- Minimum validation loss: epoch 26, 0.50217.
- Same epoch? **No**.
- Checkpoint actually used: epoch 26, selected by val_loss.

Perbedaan epoch ini adalah fakta dari validation history. Ia tidak, dengan sendirinya, membuktikan alasan historis pemilihan metric.

### A5. Explicit-rationale evidence

#### Authoritative repository

Search pada D:\Skripsi\Experiment_TA menemukan implementasi, metadata, dan kalimat generik seperti Selected by validation val_loss, tetapi tidak menemukan catatan contemporaneous yang menyatakan alasan awal pemilihan Side val_loss atau membuktikan bahwa Front val_macro_f1 telah dipra-registrasi.

Karena itu, dari authoritative repository saja, kesimpulan yang aman adalah: **implementation proves the criteria differ, but no authoritative artifact establishes why they were chosen**.

#### HISTORICAL SOURCE — not the authoritative final experiment repository

Fallback dilakukan karena provenance alasan tidak cukup di Experiment_TA.

File: D:\Skripsi\Experiment\experiment_21C_notes.md:19-21

> Checkpoint side yang dipilih berdasarkan validation loss dapat menghasilkan probabilitas yang lebih stabil untuk fusion dibanding checkpoint yang dipilih berdasarkan validation Macro F1. Dengan freeze stage 4 dan patience 6, side diharapkan menjadi lebih tidak agresif terhadap kelas phone_use.

File: D:\Skripsi\Experiment\experiment_21C_notes.md:96-100

> Side checkpoint terpilih pada epoch 15 berdasarkan validation loss 0.38643. Validation Macro F1 pada checkpoint tersebut adalah 0.76723. Train-validation loss gap side adalah 0.15835, sehingga status generalisasi berbasis gap dikategorikan OVERFIT.

File: D:\Skripsi\Experiment\experiment_21D_notes.md:31-39

> Exp21 stride30-best side memiliki train-validation loss gap 0.22406 pada best validation-loss checkpoint. Pola history menunjukkan side tetap membantu fusion, tetapi gap mulai melebar setelah epoch menengah. Karena itu, perubahan dibuat konservatif: ... Monitor tetap validation loss karena target utama adalah menguji overfit/gap.

File: D:\Skripsi\Experiment\experiment_21_notes.md:101-105

> Front berstatus OK dengan train-validation loss gap 0.04383. Side berstatus OVERFIT dengan train-validation loss gap 0.22406, tetapi side tetap meningkatkan performa test dan membantu fusion naik dari 0.78059 menjadi 0.82504. Eksplorasi berikutnya boleh fokus ke side overfit ...

Provenance mapping final:

- D:\Skripsi\Experiment_TA\experiment_index.csv:19 memetakan final artifact experiment_18 ke Exp 21D.
- Catatan 21D menyebut Front dikunci dari resep front stabilization dengan monitor validation Macro F1 dan Side diretrain dengan monitor validation loss.

#### Classification of A–F possibilities

| Candidate explanation | Audit result |
|---|---|
| A. Direncanakan sejak awal / pre-registered | **NOT ESTABLISHED FROM AVAILABLE ARTIFACTS.** Configuration exists, but no pre-registration or contemporaneous design record was found. |
| B. Berasal dari script/config training | **FACT.** The final implementation and resolved metadata enforce the difference. |
| C. Dipilih karena observed validation behavior | **SUPPORTED at historical documentation level, not independently proven as the original timestamped decision.** Historical notes discuss observed side gap/probability behavior. |
| D. Keputusan setelah membandingkan checkpoint | **NOT ESTABLISHED FROM AVAILABLE ARTIFACTS.** Different best epochs are not evidence of a post-hoc comparison. |
| E. Warisan dari eksperimen sebelumnya | **SUPPORTED.** The final artifact is indexed to Exp21D; historical notes state the Front/Side recipes were inherited from the Exp21B/Exp21C stabilization line. |
| F. Provenance tidak dapat dibuktikan | **Not the overall conclusion after historical fallback**, but this remains true for pre-registration/timing and exact first-decision provenance. |

### A6. Checkpoint verdict

**STATUS A: Strong evidence exists for why the criteria differ.**

This status is based on the combination of:

1. authoritative implementation and final checkpoint metadata, and
2. explicit historical notes that link Side val_loss to probability stabilization and overfit/loss-gap diagnosis.

It does **not** mean that the repository proves pre-registration, nor that a better test result retroactively justifies the validation criterion.

#### FACT

- Front final checkpoint is epoch 9 selected by maximum validation Macro F1.
- Side final checkpoint is epoch 26 selected by minimum validation loss.
- Early stopping uses the same criterion as checkpoint selection.
- LR scheduler uses validation Macro F1 for both views; Side therefore has a different scheduler monitor from its checkpoint monitor.
- Front best validation Macro F1 and minimum validation loss are different epochs; Side best validation Macro F1 and minimum validation loss are different epochs.
- Final checkpoint paths and SHA256 values are consistent across train summaries and evaluation metrics.
- Historical notes explicitly document Side probability-stability and overfit/loss-gap motivations and the inheritance from the stabilization experiments.

#### INFERENCE

- The difference was a view-specific design choice carried through the Exp21 stabilization lineage.
- Side val_loss was used to support a loss-gap/probability-stability objective, not because its test performance later happened to be better.

#### UNKNOWN

- Whether Front val_macro_f1 was chosen before inspecting any validation history.
- The exact timestamped first decision that changed or introduced Side val_loss.
- Whether any unrecorded checkpoint comparison was performed before the historical notes were written.

### A7. Paper-safe wording

#### Version 1 — if the historical rationale is accepted as evidence

> Checkpoint selection was view-specific. The Front checkpoint was selected at the epoch with maximum validation Macro F1. For the Side model, validation loss was used instead; the documented experimental rationale was to stabilize Side probabilities for fusion and to monitor the side-view overfit/loss-gap behavior. The LR scheduler still monitored validation Macro F1 for both views.

This wording should be accompanied by an internal provenance note that the rationale is documented in the historical repository, not in the authoritative final repository itself.

#### Version 2 — if only authoritative final artifacts may be cited

> Model selection used validation metrics. The Front checkpoint was selected by maximum validation Macro F1, whereas the Side checkpoint was selected by minimum validation loss. The available authoritative artifacts do not establish the original rationale for using different criteria.

## 3. Audit B — class-weight provenance

### B1. Exact implementation evidence

#### Fixed literal and class order

File: D:\Skripsi\Experiment_TA\experiment_18\src\config.py:99-102

~~~
BINARY_LABEL_MAP = {
    "safe_driving": 0,
    "phone_use": 1,
}
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\src\config.py:149

~~~
CLASS_WEIGHTS = [2.5, 1.0]
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:20-28

~~~
def resolve_class_weights(view, exp_config=None, gamma=1.0):
    if exp_config:
        raw = exp_config['class_weights']
    else:
        per_view_name = 'CLASS_WEIGHTS_FRONT' if view == 'front' else 'CLASS_WEIGHTS_SIDE'
        raw = globals().get(per_view_name, CLASS_WEIGHTS)
    if raw!='balanced': return raw
    df=load_split_dataframe(view,'train'); counts={v:int((df['binary_label']==k).sum()) for k,v in BINARY_LABEL_MAP.items()}; total=sum(counts.values())
    return [float((total/(len(counts)*counts[i]))**gamma) for i in range(len(counts))]
~~~

File: D:\Skripsi\Experiment_TA\experiment_18\src\train.py:110

~~~
criterion=nn.CrossEntropyLoss(weight=torch.tensor(weights,dtype=torch.float).to(device),label_smoothing=ls)
~~~

Factual meaning:

- The final default is a fixed list, so resolve_class_weights returns [2.5,1.0] directly; it does not enter the raw == 'balanced' formula branch.
- The list is passed directly as PyTorch class-index weights.
- Given BINARY_LABEL_MAP, class index 0 is safe_driving and class index 1 is phone_use.
- Both Front and Side final summaries store [2.5,1.0] with class_weight_gamma=1.0.

Files confirming final resolved values:

- D:\Skripsi\Experiment_TA\experiment_18\config\resolved_config.json:10-15
- D:\Skripsi\Experiment_TA\experiment_18\results\front\train_summary.json under resolved_config.class_weights
- D:\Skripsi\Experiment_TA\experiment_18\results\side\train_summary.json under resolved_config.class_weights
- D:\Skripsi\Experiment_TA\experiment_18\results\front\test_eval_metrics.json and side\test_eval_metrics.json under hyperparameters.class_weights

### B2. Training-count verification

The post-stride training counts were independently checked from:

- D:\Skripsi\Experiment_TA\data\manifest_split.csv
- D:\Skripsi\Experiment_TA\experiment_18\src\dataset.py:26-30, which filters the selected view/split and applies (frame - 1) % frame_stride == 0.
- D:\Skripsi\Experiment_TA\experiment_18\src\config.py:171, where FRAME_STRIDE = 30.

After filtering split=train, one view contains:

| class | count |
|---|---:|
| safe_driving | 176 |
| phone_use | 908 |
| total | 1084 |

The manifest contains both views, so the combined filtered count is 2168, with 1084 per view.

### B3. Mathematical formula comparison

Let n_safe=176, n_phone=908, N=1084, K=2.

| Formula | safe weight | phone weight | Resulting ratio safe/phone | Matches [2.5,1.0]? |
|---|---:|---:|---:|---|
| Raw inverse frequency 1/n | 0.0056818182 | 0.0011013216 | 5.1590909 | No |
| Inverse frequency normalized to sum 1 | 0.8376384 | 0.1623616 | 5.1590909 | No |
| Inverse frequency normalized to mean 1 | 1.6752768 | 0.3247232 | 5.1590909 | No |
| sklearn-style balanced N/(K*n) | 3.0795455 | 0.5969163 | 5.1590909 | No |
| Balanced weights rescaled so phone weight = 1 | 5.1590909 | 1.0 | 5.1590909 | No |
| Fixed artifact value | 2.5 | 1.0 | 2.5 | Reference only |

The standard balanced values are approximately [3.0795, 0.5969], not [2.5,1.0]. Therefore:

> **[2.5, 1.0] is not directly explained by the tested standard frequency-based formulas.**

This calculation rules formulas in or out only. It does not prove why the fixed value was chosen.

### B4. Historical/configuration evidence and provenance table

| weight setting | where found | Front/Side | validation/test context | explicit reason or provenance |
|---|---|---|---|---|
| [2.5,1.0] | Experiment_TA/experiment_18/src/config.py:149; experiment_18/config/resolved_config.json:10-12 | Both | Final stride-30 run; test Front 0.76626, Side 0.67468 | Hard-coded fixed literal; no formula in final authoritative artifact. |
| [2.5,1.0] | Experiment_TA/experiment_8/config/resolved_config.json:10-12; repeated in experiments 9–14 and 16–19 | Both in the listed shared configurations | Earlier experiments and final candidate line | Historical source comment traces this setting to Exp8. |
| [3.1036036036036037,0.5960207612456747] | Experiment_TA/experiment_2, _3, _4, _5, _6 resolved configs and analysis matrix | Both | Earlier balanced configurations | Generated by the raw == 'balanced' branch; frequency-derived, not the final fixed value. |
| [5.15,1.0] | Experiment_TA/experiment_7/config/resolved_config.json:10-12 | Both | Earlier exploratory experiment | Hard-coded alternative; no exact selection rationale found in authoritative report. |
| [1.7548633720450872,0.7726035850029893] | Experiment_TA/experiment_15/config/resolved_config.json:10-17; analysis matrix | Front fixed; Side | Side gamma 0.5 class-weight experiment | Historical Experiment_19_notes.md:408-415 documents validation-based gamma selection; this is not the final [2.5,1.0] origin. |
| [3.0795,0.5969] | Experiment_19_notes.md:84-87,434 | Historical Side gamma 1.0 | Full balanced comparison | Explicitly the balanced baseline; formula-derived from class distribution. |

Historical source quote:

File: D:\Skripsi\Experiment\src\config.py:126

~~~
CLASS_WEIGHTS = [2.5, 1.0]      # [v5/Exp8] bobot kelas moderat untuk safe_driving
~~~

This is the strongest provenance clue for the fixed value: it documents an inherited Exp8 configuration and describes the safe-driving weight as moderate. It does not provide an equation producing 2.5, nor a complete validation sweep that selected exactly 2.5.

#### What is and is not established

- **Established:** [2.5,1.0] is hard-coded and used for both final views.
- **Established:** the order is compatible with class indices [safe_driving=0, phone_use=1].
- **Established:** a historical configuration comment traces the fixed value to Exp8 and calls it a moderate safe-driving weight.
- **Not established:** an exact formula producing 2.5.
- **Not established:** that [2.5,1.0] was selected by validation tuning.
- **Not established:** that test performance was used to select this main final weight.
- **Not established:** that the value was recomputed from the final post-stride counts 176/908.

### B5. Class-weight verdict

#### Implementation evidence

CrossEntropyLoss receives a literal tensor made from [2.5,1.0]; the final resolver does not calculate it from counts. Both final view artifacts record it.

#### Mathematical comparison

The final distribution implies standard balanced weights approximately [3.0795,0.5969] and a class-imbalance ratio 5.1591:1. The artifact value has ratio 2.5:1, so it is not a direct standard frequency formula.

#### Documentary evidence

The authoritative final repository documents the value as configuration only. The historical repository documents [2.5,1.0] as [v5/Exp8] and a moderate safe-driving weight. No artifact gives the exact numeric derivation or a complete selection protocol for 2.5.

#### Provenance classification

**4. inherited configuration.**

The historical comment directly links the fixed value to Exp8, while subsequent final configs inherit it. Its intended role as a moderate safe-driving imbalance-handling heuristic is documented, but the exact numeric origin remains unresolved.

#### Confidence

**Medium.** High confidence for implementation and class order; medium confidence for historical origin; low confidence for any stronger claim about exact numeric selection rationale.

#### FACT

- Final weights are [2.5,1.0] for both Front and Side.
- They are applied in CrossEntropyLoss.
- Class index order is safe-driving then phone-use.
- The final list is fixed and bypasses the balanced-count formula.
- Alternative balanced and gamma-based settings exist in other experiments.
- Historical configuration identifies [2.5,1.0] with Exp8 and describes it as moderate for safe-driving.

#### INFERENCE

- The final value was carried forward as an inherited moderate imbalance-handling heuristic.

#### UNKNOWN

- Who first selected exactly 2.5 for safe-driving.
- Whether 2.5 came from a manual rule, a small unrecorded pilot, or a comparison not preserved in the repositories.
- Whether any validation result was used in the original Exp8 decision.

### B6. Paper-safe wording

> Training used weighted cross-entropy with fixed class weights [2.5,1.0] in the order [safe-driving, phone-use], assigning the larger penalty to the safe-driving class. The final artifacts do not establish a frequency-derived formula or validation-selection procedure for the exact value 2.5; historical configuration notes trace it to the inherited Exp8 recipe.

If the historical note is excluded from the paper, use the narrower wording:

> Training used weighted cross-entropy with fixed class weights [2.5,1.0] in the order [safe-driving, phone-use]. The available artifacts do not establish the numeric derivation or selection rationale for these fixed weights.

## 4. Current paper consistency check

| Paper statement | Location | Audit status | Evidence |
|---|---|---|---|
| Both models use class weights [2.5,1.0] in order [safe driving, phone-use]. | D:\Skripsi\Paper_TA\sections\04_experimental_setup.tex:14 | **SUPPORTED** | Final config, class-index mapping, train summaries, and evaluation metadata agree. |
| Checkpoint monitor is view-specific. | D:\Skripsi\Paper_TA\sections\04_experimental_setup.tex:18 | **SUPPORTED** | experiment_18/src/config.py:33-34, resolved config, and saved checkpoint metadata. |
| Front selected by validation Macro F1; Side selected by validation loss. | D:\Skripsi\Paper_TA\sections\04_experimental_setup.tex:21 | **SUPPORTED** | Source logic, history, summaries, SHA256-linked evaluation artifacts, and paper-matching test values. |
| Macro F1 is primary because the task is imbalanced. | D:\Skripsi\Paper_TA\sections\03_methodology.tex:20, 01_introduction.tex:11, and 04_experimental_setup.tex:24 | **SUPPORTED** as a motivation for the metric | The paper’s pre-stride distribution and the post-stride manifest both show class imbalance. This does not establish the numeric origin of [2.5,1.0]. |
| Front/Side paper test results 0.76626/0.67468. | D:\Skripsi\Paper_TA\sections\05_results.tex:6 and main.tex:41 | **SUPPORTED** | experiment_18 test artifacts and experiment index. |
| Any explicit rationale that the exact Side criterion was pre-registered or chosen from a formal checkpoint comparison. | Not stated in current paper | **NOT CLAIMED** | No such paper statement was found; available artifacts do not establish it. |

No current paper statement was found that claims [2.5,1.0] is inverse-frequency-derived or validation-tuned. Such claims should not be added without new evidence.

## 5. Recommended paper-safe wording

### Checkpoint selection

Safest factual form:

> Model selection used validation metrics. The Front checkpoint was selected by maximum validation Macro F1, while the Side checkpoint was selected by minimum validation loss. In the training implementation, early stopping used the same view-specific criterion as checkpoint saving, whereas the ReduceLROnPlateau scheduler monitored validation Macro F1 for both views.

If the historical rationale is accepted and explicitly documented:

> The view-specific criteria were retained from the stabilization experiments: Front used validation Macro F1, while Side used validation loss to target side-view loss-gap/overfit behavior and probability stability for fusion. These criteria were applied only on the validation set; test performance was not used in the checkpoint-selection rule.

### Class weights

> Weighted cross-entropy used fixed class weights [2.5,1.0] in the order [safe-driving, phone-use]. The larger safe-driving weight reflects the fixed imbalance-handling configuration used in the experiment; the available final artifacts do not establish an inverse-frequency formula or validation-selection procedure for the exact numeric value.

## 6. Remaining unresolved questions

1. Was Front val_macro_f1 selected before any validation history was observed, or inherited from an earlier recipe?
2. What is the timestamped first record that introduced Side val_loss as the checkpoint criterion?
3. Was any side checkpoint comparison conducted before the historical 21C/21D notes were written?
4. Who selected the exact fixed value 2.5 for safe-driving, and was it a manual pilot, a rule-of-thumb, or an unpreserved experiment?
5. Why does the root experiment_18/config/resolved_config.json report Side scheduler patience 1 while source/per-view training metadata report 2?

CHECKPOINT RATIONALE: SUPPORTED

CLASS-WEIGHT RATIONALE: PARTIALLY SUPPORTED
