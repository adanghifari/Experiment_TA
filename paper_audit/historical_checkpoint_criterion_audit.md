# Historical Checkpoint-Criterion Audit: Front vs Side

Tanggal audit: 2026-09-18  
Repository historis utama: `D:\Skripsi\Experiment`  
Repository final: `D:\Skripsi\Experiment_TA` — dibaca hanya untuk referensi konfigurasi final.

## Scope and method

Audit ini bersifat read-only. Tidak ada training, retraining, inference baru, perubahan source code, perubahan checkpoint, perubahan manuscript, atau Git commit.

Sumber bukti utama:

- commit history lokal dan branch lokal pada repository historis;
- notes Markdown, konfigurasi Python, JSON summary/metadata, CSV, dan epoch histories;
- test metrics hanya sebagai rekonstruksi sejarah, bukan sebagai dasar untuk mengklaim checkpoint dipilih dengan melihat test set;
- konfigurasi final pada `Experiment_TA` hanya sebagai referensi bahwa asymmetry criterion dipertahankan.

Beberapa artefak seperti `side_retrain_v3` berada sebagai working-tree artifacts pada repository historis. Artefak tersebut diperlakukan sebagai bukti sekunder; titik transisi ditentukan dari commit dan artefak yang commit-verifiable.

## Executive conclusion

Hipotesis audit:

Side awalnya menggunakan validation Macro F1 seperti Front, tetapi hasil/perilaku Side kurang baik sehingga model selection Side kemudian diganti menggunakan validation loss.

**Verdict: PARTIALLY SUPPORTED.**

Yang didukung langsung:

1. Side memang menggunakan validation Macro F1 untuk checkpoint/model selection pada run awal dan baseline final-v1.
2. Side pada Experiment 21 awal memiliki hasil/fusion behavior yang kurang baik: test Macro F1 Side `0.66044`, fusion `0.76597`, dan `safe_driving -> phone_use` sebanyak `39`.
3. Catatan kontemporer Experiment 21C secara eksplisit menyatakan bahwa Side perlu distabilkan dan menguji checkpoint berbasis validation loss agar probabilitas Side lebih stabil untuk fusion.
4. Implementasi pertama yang eksplisit menggunakan `val_loss` adalah Experiment 21C, commit `d060b4271`.

Yang tidak terbukti penuh:

- bahwa validation Macro F1 itu sendiri terbukti terlalu buruk/fluktuatif dan menjadi satu-satunya alasan;
- bahwa perubahan criterion saja menyebabkan perbaikan, karena freeze stage, early-stopping patience, dan scheduler patience juga berubah.

## 1. Criterion history

### 1.1 Earliest verified Side run

Commit `9f7f77270` (2026-07-05, `First commit and first try in This Experiment`) sudah memiliki `results/side_history.json`, `results/side_test_metrics.json`, dan source training yang menyatakan early stopping berdasarkan validation Macro F1.

- View: Side
- Backbone: EfficientNetV2-S
- Training seed: konfigurasi split seed `42`; training seed khusus tidak tercatat terpisah pada artefak awal
- Split/stride: subject split; stride tidak tercatat sebagai subsampling pada konfigurasi awal
- Learning rate: `1e-4`
- Weight decay: tidak tercatat
- Freeze-stage: tidak tercatat eksplisit pada summary awal
- Augmentation train: horizontal flip, rotation `10°`, ColorJitter `0.2`; val/test tanpa augmentation
- Class weights: tidak tercatat
- Checkpoint monitor/mode: validation Macro F1 / maximize; source memakai `step(val_f1)`
- Early stopping monitor/patience: validation Macro F1 / patience `5`
- Best epoch: `3`
- Best validation Macro F1: `0.90022`
- Minimum validation loss: `0.13644`, juga pada epoch `3`
- Test Macro F1: `0.83697`
- Status: exploratory initial run

Run ini adalah bukti tertua bahwa Side telah memakai validation Macro F1. Pada run ini epoch max-F1 dan min-loss kebetulan sama.

### 1.2 Baseline Side13 and Front14A / final-v1

Artefak `experiment_notes.md`, `results/experiment_14A_front_metrics.json`, `results/final_v1/*`, dan `summary.md` menunjukkan baseline berikut:

| Run | View | LR | WD | Freeze | Augmentation train | Class weights | Checkpoint / early-stop | Patience | Best epoch | Best val Macro F1 | Val loss at selected epoch | Test Macro F1 | Status |
|---|---|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|---|
| Side13 / final-v1 Side | Side | `2e-5` | `2e-3` | 4 | flip, rotation `45°`, jitter `0.8` | `[2.5,1.0]` | `val_macro_f1` / max | 7 | 11 | `0.75000` | `0.56022` | `0.62023` | final-v1 baseline |
| Front14A revised / final-v1 Front | Front | `3e-5` | `3e-4` | 5 | flip, rotation `68°`, jitter `1.2` | `[2.5,1.0]` | `val_macro_f1` / max | 4 | 9 | `0.72581` | `0.51736` | `0.76626` | final-v1 baseline |

Both views therefore used validation Macro F1/max in this baseline. `experiment_notes.md` explicitly says Front14A's best model was selected by validation Macro F1, while Side13 remained the control Side model.

### 1.3 Experiment 19 Side sweep

Experiment 19 changed Side class weighting, not checkpoint criterion. The gamma summaries record `metric_for_best_model: "validation Macro F1"`, early-stopping patience `5`, EfficientNetV2-S, AdamW, LR `3e-5`, WD `1e-4`, dropout `0.3`, freeze stage `4`, with class weights varying by gamma.

Representative verified rows:

| Run | Class-weight setting | Best epoch | Best val Macro F1 | Val loss at selected epoch | Test Macro F1 | Status |
|---|---|---:|---:|---:|---:|---|
| Exp19 gamma 0.93 | gamma `0.93` | 5 | `0.62232` | `0.63709` | `0.57397` | exploratory |
| Exp19 gamma 0.96 | gamma `0.96` | 14 | `0.61595` | `0.58362` | `0.58393` | exploratory |
| Exp19 gamma 0.98 | gamma `0.98` | 8 | `0.58997` | `0.61342` | `0.56113` | exploratory |
| Exp19 validation-selected gamma | gamma `0.50` | 8 | selected by validation Macro F1 | recorded in selection artifact | `0.64349` Side; `0.77992` fusion | exploratory, not final replacement |

The explicit protocol in `experiment_19_notes.md` and `results/gamma_selection_exp19_summary.json` is validation-based selection. No transition to `val_loss` occurs in Experiment 19.

### 1.4 Experiment 21 initial Side: last Macro-F1-selected Side before transition

The original Experiment 21 artifact is preserved in commit `23efbc314` (`Add Experiment 21 results`, 2026-08-03 09:47 WIB).

- View: Side; backbone EfficientNetV2-S
- Training/split seed: `42`
- Split: same subject-based split used by final pipeline
- Frame stride: `20`
- LR/WD/dropout: `2e-5` / `5e-4` / `0.3`
- Freeze stage: `3`; label smoothing `0.0`
- Augmentation: inherited Side pipeline, flip, rotation `45°`, jitter `0.8`
- Class weights: `[2.5,1.0]`
- Checkpoint monitor/mode: `val_macro_f1` / max
- Early-stopping monitor/patience: validation Macro F1 / `7`
- Best epoch: `21`
- Best validation Macro F1: `0.74767`
- Validation loss at selected epoch: `0.47662`
- Test Macro F1: `0.66044`
- Test confusion: `[[20,39],[16,247]]`
- Fusion Macro F1: `0.76597`
- Status: not adopted as final; follow-up Side stabilization was initiated

The contemporaneous Experiment 21B notes call this model “Side Exp21A” and record that it was kept as a locked reference, while also documenting Side bias and the fusion trade-off.

### 1.5 First verified val_loss Side run: Experiment 21C

The first explicit criterion transition is commit `d060b4271` (`Add Experiment 21C side stabilization pipeline`, 2026-08-03 10:30 WIB). The first result artifact is commit `df6ddaac0` (10:50 WIB).

- View: Side; backbone EfficientNetV2-S
- Training/split seed: `42`
- Split: same subject-based split
- Frame stride: `20`
- LR/WD/dropout: `2e-5` / `5e-4` / `0.3`
- Freeze stage: `4`; label smoothing `0.0`
- Augmentation: inherited Side pipeline, flip, rotation `45°`, jitter `0.8`
- Class weights: `[2.5,1.0]`
- Checkpoint monitor/mode: `val_loss` / min
- Early-stopping monitor/patience: validation loss / `6`
- Scheduler: ReduceLROnPlateau on validation loss, patience `2`
- Best epoch by selected criterion: `15`
- Minimum validation loss: `0.38643`
- Validation Macro F1 at selected epoch: `0.76723`
- Test Macro F1: `0.76085`
- Test confusion: `[[37,22],[25,238]]`
- Fusion Macro F1: `0.81626`
- Status: candidate/accepted as the best Experiment 21C fusion direction; recipe then used in stride-30 run

The source implementation is explicit: `MinEarlyStopping.step(val_loss)`, `best_idx = min(... val_loss ...)`, `metric_for_best_model: "validation loss"`, and `checkpoint_monitor: "val_loss"`.

### 1.6 Post-transition Side runs

| Run | Stride | LR | WD | Dropout | Freeze | Patience | Monitor/mode | Best epoch | Val loss | Val Macro F1 at selected epoch | Test Macro F1 | Status |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|
| Exp21 stride-30 best / final-v2 Side | 30 | `2e-5` | `5e-4` | `0.3` | 4 | 6 | `val_loss` / min | 25 | `0.42690` | `0.73653` | `0.71590` | main final-v2 recipe |
| Exp21D Side | 30 | `2e-5` | `1e-3` | `0.4` | 4 | 5 | `val_loss` / min | 26 | `0.41766` | `0.75752` | `0.73985` | diagnostic regularization |
| Exp21E Side | 30 | `2e-5` | `1e-3` | `0.3` | 4 | 6 | `val_loss` / min | 25 | `0.42690` | `0.73653` | `0.71590` | diagnostic follow-up |

Stride-30 main configuration:

- Front: `val_macro_f1` / max, patience `4`, LR `3e-5`, WD `5e-4`, dropout `0.4`, freeze `5`.
- Side: `val_loss` / min, patience `6`, LR `2e-5`, WD `5e-4`, dropout `0.3`, freeze `4`.

### 1.7 Later exploratory reversion

The later `side_retrain_v3_protocol.md` returns to validation Macro F1 for exploratory multi-seed selection, constrained by validation phone recall and train-validation loss gap. It does not replace final-v2.

- Seeds: `42,43,44,45,46`
- Selection base: validation Macro F1
- Constraints: validation phone recall floor and loss gap `<= 0.10`
- Selected candidate: seed `42`, epoch `14`, val Macro F1 `0.75000`, gap `0.03276`
- Test Side Macro F1: `0.64349`
- Status: exploratory candidate, not main final-v2

This shows that the change was not a universal rule for every later Side experiment; it was the rule adopted for the 21C/stride-30/final-v2 line.

## 2. Direct historical evidence

### Direct evidence Side originally used validation Macro F1

- Earliest source `9f7f77270`: `EarlyStopping.step(val_f1)`; Side test artifact contains `best_epoch` and `val_macro_f1`.
- `experiment_notes.md`: Front14A best model selected by validation Macro F1; Side remained Exp13 control.
- `results/final_v1/side_train_summary_final_v1.json`: `metric_for_best_model: "validation Macro F1"`.
- `results/side_summary_exp19_gamma*.json`: `metric_for_best_model: "validation Macro F1"`.
- `23efbc314:results/experiment_21/side_train_summary_exp21.json`: `metric_for_best_model: "validation Macro F1"`, best epoch `21`.

### Direct evidence of first switch to validation loss

- Commit order identifies `d060b4271` as the first explicit introduction of `checkpoint_monitor`.
- `experiment_21C_notes.md` says Side checkpoint is selected using validation loss and frames this as probability stabilization for fusion.
- `src/experiment_21C/config_experiment_21C.py` sets `checkpoint_monitor: "val_loss"`.
- `src/experiment_21C/train_experiment_21C.py` uses lower-is-better `MinEarlyStopping`, calls `step(val_loss)`, selects `min(val_loss)`, and writes `metric_for_best_model: "validation loss"`.
- `results/experiment_21C/side_train_summary_exp21C.json` records `checkpoint_monitor: "val_loss"`, epoch `15`, and loss `0.38643`.

### Direct contemporaneous rationale

`experiment_21C_notes.md` documents this sequence:

1. Front 21B was already strong.
2. Side Exp21A had Macro F1 `0.66044`, was biased toward `phone_use`, and contributed to fusion `safe->phone` rising from `16` on Front to `26`.
3. The next experiment focused on Side probability stabilization rather than changing the fusion formula.
4. The hypothesis was that validation-loss checkpoint selection could yield more stable probabilities than validation-Macro-F1 selection.

This is contemporaneous rationale, not merely a later interpretation of curves.

## 3. Validation-behavior analysis

All calculations below use existing complete histories only.

### 3.1 Initial Side 21

History: `23efbc314:results/experiment_21/side_history_exp21.json`.

- Max validation Macro F1: epoch `21`, F1 `0.74767`, loss `0.47662`, gap `0.05569`.
- Min validation loss: epoch `28`, loss `0.46727`, F1 `0.74043`, gap `0.05489`.
- Difference: `7` epochs.
- This proves criterion disagreement in the history, not that the disagreement caused the later decision.

### 3.2 Experiment 21C

History: `results/experiment_21C/side_history_exp21C.json`.

- Min validation loss: epoch `15`, loss `0.38643`, F1 `0.76723`, gap `0.15835`.
- Max validation Macro F1: epoch `20`, F1 `0.78224`, loss `0.40720`, gap `0.23643`.
- Difference: `5` epochs.
- The loss-selected epoch has lower loss and lower observed loss gap than the later max-F1 epoch.
- This is consistent with stabilization, but the notes—not this calculation—are the historical rationale.

### 3.3 Stride-30 main and follow-ups

- Main stride-30 Side: min loss epoch `25` (`0.42690`), F1 `0.73653`; max validation F1 epoch `26` (`0.76316`), loss `0.43759`.
- Exp21D: min loss and max F1 both epoch `26` (`0.41766`), `0.75752`.
- Exp21E: min loss epoch `25`; max F1 epoch `26`.

Criterion disagreement is therefore run-dependent. The evidence does not support a universal claim that validation loss is always smoother or superior.

## 4. Comparable runs and controlled-comparison assessment

Closest pre/post pair:

- **A — Exp21 initial Side / 21A:** `val_macro_f1`/max, stride `20`, seed `42`, LR `2e-5`, WD `5e-4`, dropout `0.3`, class weights `[2.5,1.0]`, same broad Side augmentation pipeline.
- **B — Exp21C Side:** `val_loss`/min, stride `20`, seed `42`, LR `2e-5`, WD `5e-4`, dropout `0.3`, class weights `[2.5,1.0]`, same broad pipeline.

Not criterion-only:

- freeze stage changed `3 -> 4`;
- early-stopping patience changed `7 -> 6`;
- scheduler patience changed `1 -> 2`;
- front checkpoint was revised/locked in the surrounding fusion line.

Observed outcome:

- Side test Macro F1: `0.66044 -> 0.76085`;
- fusion Macro F1: `0.76597 -> 0.81626`;
- Side `safe->phone`: `39 -> 22`;
- selected epoch: `21` under Macro F1 versus `15` under validation loss.

Therefore controlled comparison is **partial**, not criterion-only causal evidence. The stride-30 run is not controlled against 21C because stride changes; 21D/E also change regularization and patience.

## 5. Test-performance caution

Historical test outcomes:

- Exp21A Side: `0.66044`; fusion `0.76597`.
- Exp21C Side: `0.76085`; fusion `0.81626`.
- Exp21 stride-30/final-v2 Side: `0.71590`; fusion `0.82504`.

No artifact says that the within-run checkpoint was selected by looking at test set results. The 21C notes use prior Side/fusion behavior to motivate a new experiment, but the checkpoint monitor itself is validation loss. These test metrics are outcomes, not proof that `val_loss` was selected because it gave the best test result.

## 6. Transition-point reconstruction

| Time/order | Artifact | Side criterion | What it shows |
|---|---|---|---|
| 2026-07-05 | `9f7f77270`, initial source/results | `val_macro_f1` / max | Earliest verified Side Macro-F1 selection |
| 2026-07-16 to 2026-07-19 | Exp14A/final-v1/Exp19 | `val_macro_f1` / max | Baseline and class-weight sweep remain Macro-F1-selected |
| 2026-08-03 09:18 | `7f59caea4`, Exp21 pipeline | Macro F1 | Both views initially use same selection family |
| 2026-08-03 09:47 | `23efbc314`, Exp21 results | `val_macro_f1` / max | Last pre-transition Side: F1 `0.66044`, fusion `0.76597` |
| 2026-08-03 10:05–10:17 | Exp21B pipeline/results | Side locked from 21A | Front changed; Side still inherited Macro F1 |
| **2026-08-03 10:30** | **`d060b4271`, Exp21C pipeline** | **`val_loss` / min** | **First verified explicit Side switch** |
| 2026-08-03 10:50 | `df6ddaac0`, Exp21C results | `val_loss` / min | First result under new criterion |
| 2026-08-03 11:19 onward | `85804dcd1`, stride-30 recipe | `val_loss` / min | 21C recipe promoted to stride-30 line |
| 2026-08-03 13:23 onward | final-v2 pipeline/results | `val_loss` / min | Asymmetry carried into final-v2 |

Experiment immediately before: Exp21B/locked Exp21A Side.  
Experiment immediately after: Exp21C Side stabilization.  
Criterion-only change: No.  
Documented rationale: Yes, probability stabilization after poor Side/fusion behavior; not isolated proof that Macro F1 validation behavior alone caused the switch.

## 7. Historical fact vs rationale vs retrospective interpretation

### Historical fact

- Side used validation Macro F1/max in the initial pipeline, Side13/final-v1, Exp19, and initial Exp21.
- Side first used validation loss/min in Exp21C, then in the stride-30 main/final-v2 line.
- Front remained validation Macro F1/max in the relevant Front14A, Exp21B, stride-30, and final-v2 configurations.
- The Side criterion switch was implemented together with other Side recipe changes.
- Selected epochs can differ: initial Exp21 `21` vs `28`; Exp21C `15` vs `20`; stride-30 main `25` vs `26`.

### Historical rationale

- The contemporaneous 21C note attributes the next step to Side bias toward `phone_use` and the resulting fusion error trade-off.
- The stated hypothesis was that validation-loss selection could stabilize Side probabilities for fusion.
- Notes do not explicitly say: “validation Macro F1 was too noisy, therefore it was discarded.”

### Retrospective interpretation

- Histories show criterion disagreement and, in 21C, a lower-loss checkpoint before the later maximum-F1 epoch.
- The selected 21C checkpoint has a lower loss gap than its later max-F1 epoch.
- These patterns are consistent with stabilization, but are not themselves the historical reason.
- Improvement after 21C is a result of a multi-parameter experiment, not evidence that criterion alone caused it.

## 8. Verdict components

### DIRECT EVIDENCE

- Explicit pre-transition `metric_for_best_model: "validation Macro F1"` for Side.
- Explicit `checkpoint_monitor: "val_loss"` and `metric_for_best_model: "validation loss"` in 21C and final-v2 Side configs.
- Commit order identifies 21C as first switch.
- Contemporaneous 21C notes connect the change to Side probability stabilization after poor Side/fusion behavior.

### INDIRECT SUPPORT

- Initial Exp21 Side had lower standalone and fusion Macro F1, with `39` safe-to-phone errors.
- Initial history selected max F1 at epoch `21`, while min loss occurred at epoch `28`.
- 21C loss selection chose epoch `15`, while max validation F1 occurred at epoch `20` with a larger loss gap.
- 21C and promoted stride-30 recipe improved documented Side/fusion outcomes, although multiple parameters changed.

### CONTRADICTING EVIDENCE

- Initial Side Exp21 was labeled generalization status `OK`; the documented problem was bias/fusion behavior, not unambiguous validation-loss failure.
- Later Side retrain v3 returned to validation Macro F1 with constraints.
- Exp21D has min loss and max Macro F1 at the same epoch.
- No criterion-only experiment proves `val_loss`, rather than freeze/patience/other changes, caused improvement.

### MISSING EVIDENCE

- No contemporaneous note explicitly says validation Macro F1 was rejected because it was too noisy.
- No paired same-seed, same-recipe, criterion-only Side retrain is present.
- No complete paired checkpoint set selected once by Macro F1 and once by loss is present for every transition run.
- No evidence says test performance was used to choose `val_loss`.

## 9. Answer to the specific hypothesis

**PARTIALLY SUPPORTED.**

The broad narrative is supported: Side began with validation Macro F1, Side/fusion behavior was unsatisfactory in the relevant 21A/21B context, and 21C explicitly changed Side selection to validation loss to test probability stabilization. The stronger causal narrative is not fully established because the transition also changed freeze stage, early-stopping patience, and scheduler patience, and notes do not state that validation Macro F1 fluctuation itself was decisive.

## 10. Wording for adviser

### A. SAFE SHORT ANSWER

“Pada eksperimen awal, Front dan Side sama-sama memilih checkpoint berdasarkan validation Macro F1. Setelah Side menunjukkan bias/error yang kurang baik untuk fusion, Experiment 21C menguji pemilihan berdasarkan validation loss untuk menstabilkan probabilitas Side; perubahan ini dilakukan bersama beberapa perubahan konfigurasi lain, jadi evidence tidak cukup untuk mengklaim bahwa criterion saja yang menyebabkan perbaikan.”

### B. FULL TECHNICAL ANSWER

“Secara historis, Front dan Side awalnya memakai validation Macro F1 sebagai monitor checkpoint dengan mode maximize. Pada hasil Side Exp21A, Macro F1 standalone adalah 0.66044 dan fusion menjadi 0.76597; catatan eksperimen menyoroti bias Side ke kelas `phone_use` dan kenaikan error `safe_driving -> phone_use` pada fusion. Karena itu pada Experiment 21C dibuat eksperimen stabilisasi Side: checkpoint dan early stopping diubah menjadi validation loss/min, dengan hipotesis bahwa probabilitas Side akan lebih stabil untuk fusion. Ini adalah alasan yang tercatat pada notes kontemporer. Namun perubahan tersebut tidak hanya mengganti monitor: freeze stage berubah dari 3 menjadi 4, patience early stopping dari 7 menjadi 6, dan scheduler patience juga berubah. Karena itu hasil setelahnya harus dibaca sebagai hasil paket perubahan konfigurasi, bukan bukti criterion-only.” 

## Required final fields

HYPOTHESIS:  
Side val_macro_f1 performed poorly / behaved poorly, therefore Side checkpoint criterion was changed to val_loss.

VERDICT:  
PARTIALLY SUPPORTED

FIRST VERIFIED SIDE VAL_MACRO_F1 RUN:  
Commit `9f7f77270`, initial run (`results/side_history.json`, `results/side_test_metrics.json`); validation Macro F1/max, best epoch `3`, val Macro F1 `0.90022`, test Macro F1 `0.83697`.

FIRST VERIFIED SIDE VAL_LOSS RUN:  
Experiment 21C, commit `d060b4271` (pipeline) with result commit `df6ddaac0`; validation loss/min, best epoch `15`, val loss `0.38643`, val Macro F1 at selected epoch `0.76723`.

CONTROLLED COMPARISON EXISTS:  
PARTIAL

DIRECT HISTORICAL RATIONALE EXISTS:  
YES

SAFE ANSWER TO ADVISER:  
Pada eksperimen awal, Front dan Side sama-sama memilih checkpoint berdasarkan validation Macro F1. Setelah Side menunjukkan bias/error yang kurang baik untuk fusion, Experiment 21C menguji validation loss untuk menstabilkan probabilitas Side; karena freeze dan patience juga berubah, evidence tidak membuktikan bahwa criterion saja yang menyebabkan hasil lebih baik.

FACT:  
Side awal menggunakan `val_macro_f1`/max; Side pertama yang secara eksplisit menggunakan `val_loss`/min adalah Experiment 21C; notes 21C mencatat tujuan stabilisasi probabilitas Side untuk fusion.

INFERENCE:  
Perbedaan epoch dan gap pada history konsisten dengan interpretasi bahwa loss memberi checkpoint yang lebih konservatif/stabil pada beberapa run.

UNKNOWN:  
Apakah validation Macro F1 secara khusus dianggap terlalu fluktuatif oleh peneliti saat keputusan dibuat, dan seberapa besar perbaikan setelah 21C berasal dari criterion versus perubahan freeze/patience, tidak dapat dipisahkan dari artifacts yang tersedia.
