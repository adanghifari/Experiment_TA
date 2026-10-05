# Model-Selection Standardization Impact Audit

Audit read-only untuk standardisasi kriteria pemilihan model Side menjadi validation Macro F1 dengan mode maximize.

## Scope and restrictions

Authoritative training/evaluation evidence was read only from:

D:\Skripsi\Experiment_TA

Paper evidence was read only from:

D:\Skripsi\Paper_TA

The historical repository was not accessed or used. No retraining, new inference, source modification, manuscript modification, checkpoint overwrite, or Git commit was performed.

## Executive conclusion

The current final Side run uses validation loss for both checkpoint selection and early stopping. Therefore, changing the configuration to validation Macro F1 would not be checkpoint-only: it would also change the early-stopping score and mode.

For the current final Side history:

- minimum validation loss: epoch 26;
- maximum validation Macro F1: epoch 15;
- the old validation-loss run reached its maximum configured 30 epochs and did not early-stop before epoch 30;
- replaying the exact EarlyStopping implementation with validation Macro F1 and patience 5 over this history gives a theoretical stop at epoch 20.

A physically existing authoritative-repository candidate was found:

D:\Skripsi\Experiment_TA\archive\experiment_20_side_val_macro_f1\checkpoints\side\best.pt

Its accompanying metadata records:

- checkpoint criterion: val_macro_f1;
- mode: max;
- best epoch: 15;
- SHA-256: 0e8b30bff8773d2696a63378104a3d7701671b8a2647d7a553424def64a9fda6;
- early-stopping patience: 5;
- scheduler monitor: val_macro_f1;
- Side hyperparameters matching the final Side recipe;
- complete validation history through the theoretical stop;
- Side test predictions and fusion predictions/metrics.

The candidate is therefore sufficient to avoid retraining the main final Side model, subject to the provenance caveat described below: several embedded metadata paths point to a different current directory, so the physical archive path and SHA-256 must be treated as authoritative identity.

The candidate also means the main fusion results can be updated from existing prediction/evaluation artifacts without new inference. Robustness and augmentation-sensitivity runs are different: only the seed-42 baseline candidate exists under the standardized criterion. Seed 43, seed 44, and the three altered augmentation settings remain validation-loss runs without corresponding validated Macro-F1 checkpoints.

## 1. Current Side training behavior

### 1.1 Source-code evidence

File:

D:\Skripsi\Experiment_TA\experiment_18\src\train.py

~~~python
# lines 68-82
checkpoint_monitor = checkpoint_monitor or (
    CHECKPOINT_MONITOR_FRONT if view == 'front' else CHECKPOINT_MONITOR_SIDE
)
weights = resolve_class_weights(...)
mode = 'min' if checkpoint_monitor == 'val_loss' else 'max'
~~~

~~~python
# lines 52-58
class EarlyStopping:
    def __init__(self, patience, mode='max'):
        self.patience=patience; self.mode=mode
        self.best=-float('inf') if mode=='max' else float('inf')
        self.counter=0; self.should_stop=False

    def step(self, score):
        ok=score>self.best if self.mode=='max' else score<self.best
        if ok:
            self.best=score; self.counter=0; return True
        self.counter+=1
        self.should_stop=self.counter>=self.patience
        return False
~~~

~~~python
# lines 120-127
va_loss,va=validate(...)
sch.step(va['macro_f1'])
...
score=row[checkpoint_monitor]
is_best=early.step(score)
...
if early.should_stop:
    break
~~~

The exact implementation shows:

- the selected checkpoint score is the same score passed to EarlyStopping;
- mode is max except when the monitor is val_loss;
- the scheduler is stepped separately using validation Macro F1;
- stopping is checked after checkpoint update and after scheduler stepping.

### 1.2 Final Side settings

File:

D:\Skripsi\Experiment_TA\experiment_18\results\side\train_summary.json

Recorded effective settings:

| Setting | Current final Side value |
|---|---|
| checkpoint monitor | val_loss |
| checkpoint mode | min |
| early-stopping monitor | val_loss |
| early-stopping mode | min |
| early-stopping patience | 5 |
| LR scheduler | ReduceLROnPlateau |
| scheduler monitor | val_macro_f1 |
| scheduler mode | max |
| scheduler patience | 2 |
| maximum epochs | 30 |
| optimizer | AdamW |
| learning rate | 2e-5 |
| weight decay | 1e-3 |
| seed | 42 |

The source configuration confirms:

D:\Skripsi\Experiment_TA\experiment_18\src\config.py

~~~python
# lines 133-152
LEARNING_RATE_SIDE = 0.00002
EARLY_STOPPING_PATIENCE_SIDE = 5
MAX_EPOCHS = 30
WEIGHT_DECAY_SIDE = 0.001
NUM_STAGES_TO_FREEZE_SIDE = 4
LR_SCHEDULER_PATIENCE_SIDE = 2
~~~

The root-level resolved configuration contains scheduler_patience_side = 1, but the per-run Side summary, checkpoint metadata, source configuration, and actual scheduler construction all record/use 2. The per-run source and summary are the relevant evidence for the final Side training behavior.

### 1.3 Direct answers about behavior change

Would changing Side checkpoint monitor from val_loss to val_macro_f1 also change early stopping?

**YES.**

Reason: train.py derives mode from checkpoint_monitor and passes the same monitor score and mode into EarlyStopping. Changing the Side monitor changes:

- the score passed to early.step;
- the comparison direction;
- the epochs at which patience is reset;
- the epoch at which training stops.

Would the change affect optimizer or scheduler trajectory?

**It does not change gradient calculation or the scheduler metric for epochs that are actually executed, but it can change the total trajectory by stopping at a different epoch.**

Facts from source:

- gradient updates use train_one_epoch, optimizer.zero_grad, loss.backward, and optimizer.step;
- the loss function, data loader, augmentation, and optimizer are created independently of checkpoint_monitor;
- ReduceLROnPlateau always receives va['macro_f1'];
- checkpoint_monitor is used for EarlyStopping and checkpoint saving.

Therefore:

- optimizer updates within common executed epochs are not selected by val_loss versus val_macro_f1;
- scheduler stepping within common executed epochs still uses validation Macro F1;
- if the alternative criterion stops earlier, later optimizer updates and scheduler steps do not occur;
- the saved best checkpoint changes because the saved epoch changes;
- full bitwise identity is not claimed because the repository itself does not assume full bitwise determinism.

The relevant randomness and data behavior are implemented in:

D:\Skripsi\Experiment_TA\experiment_18\src\train.py, lines 17-18, and

D:\Skripsi\Experiment_TA\experiment_18\src\dataset.py, lines 19-44.

The final run uses fixed seeds, deterministic cuDNN settings, shuffled training data, and stochastic training augmentation. The monitor itself does not alter those functions, but a different stopping epoch changes how long they are executed.

## 2. Final Side validation-history audit

Source history:

D:\Skripsi\Experiment_TA\experiment_18\results\side\history.csv

Improvement means strict improvement exactly as implemented:

- validation loss: current value < previous best;
- validation Macro F1: current value > previous best;
- equality is not counted as improvement.

| Epoch | Train loss | Val loss | Val Macro F1 | Learning rate | Improves val loss | Improves val Macro F1 |
|---:|---:|---:|---:|---:|:---:|:---:|
| 1 | 0.68783 | 0.61984 | 0.45783 | 2e-5 | yes | yes |
| 2 | 0.66351 | 0.61456 | 0.45122 | 2e-5 | yes | no |
| 3 | 0.62094 | 0.61117 | 0.47671 | 2e-5 | yes | yes |
| 4 | 0.61543 | 0.60593 | 0.45255 | 2e-5 | yes | no |
| 5 | 0.60473 | 0.59085 | 0.45783 | 2e-5 | yes | no |
| 6 | 0.57667 | 0.58139 | 0.45652 | 1e-5 | yes | no |
| 7 | 0.56428 | 0.57795 | 0.58836 | 1e-5 | yes | yes |
| 8 | 0.56642 | 0.57338 | 0.53354 | 1e-5 | yes | no |
| 9 | 0.54957 | 0.56865 | 0.62212 | 1e-5 | yes | yes |
| 10 | 0.54512 | 0.56729 | 0.71715 | 1e-5 | yes | yes |
| 11 | 0.50576 | 0.56054 | 0.71447 | 1e-5 | yes | no |
| 12 | 0.53423 | 0.54875 | 0.74270 | 1e-5 | yes | yes |
| 13 | 0.49931 | 0.55967 | 0.71241 | 1e-5 | no | no |
| 14 | 0.51615 | 0.53427 | 0.73666 | 1e-5 | yes | no |
| 15 | 0.48501 | 0.53991 | 0.75724 | 1e-5 | no | yes |
| 16 | 0.48325 | 0.53097 | 0.72282 | 1e-5 | yes | no |
| 17 | 0.46293 | 0.52459 | 0.73468 | 1e-5 | yes | no |
| 18 | 0.43267 | 0.51556 | 0.74572 | 5e-6 | yes | no |
| 19 | 0.44828 | 0.51429 | 0.70533 | 5e-6 | yes | no |
| 20 | 0.42200 | 0.50778 | 0.72282 | 5e-6 | yes | no |
| 21 | 0.42589 | 0.50681 | 0.68983 | 2.5e-6 | yes | no |
| 22 | 0.40914 | 0.51567 | 0.67799 | 2.5e-6 | no | no |
| 23 | 0.41379 | 0.51441 | 0.68684 | 2.5e-6 | no | no |
| 24 | 0.40627 | 0.51341 | 0.67510 | 1.25e-6 | no | no |
| 25 | 0.40850 | 0.50241 | 0.68684 | 1.25e-6 | yes | no |
| 26 | 0.39480 | 0.50217 | 0.68238 | 1.25e-6 | yes | no |
| 27 | 0.42705 | 0.50756 | 0.67086 | 6.25e-7 | no | no |
| 28 | 0.41742 | 0.50466 | 0.68983 | 6.25e-7 | no | no |
| 29 | 0.40019 | 0.51380 | 0.66667 | 6.25e-7 | no | no |
| 30 | 0.39814 | 0.50294 | 0.70060 | 3.125e-7 | no | no |

History conclusions:

A. Minimum validation loss:

- epoch 26;
- val_loss = 0.50217.

B. Maximum validation Macro F1:

- epoch 15;
- val_macro_f1 = 0.75724.

C. Did maximum validation Macro F1 occur before the old training stopped?

**YES.**

The old run contains 30 epochs. With val_loss and patience 5, the minimum occurs at epoch 26 and only four subsequent epochs are present without a lower loss. Thus the old run reached the maximum configured 30 epochs rather than triggering Side early stopping before epoch 30.

D. Theoretical early stopping with validation Macro F1 and patience 5:

- best F1 is reached at epoch 15;
- epochs 16, 17, 18, 19, and 20 do not improve on 0.75724;
- the exact implementation sets should_stop at epoch 20;
- theoretical stop epoch: **20**.

The existing candidate standardized run also contains 20 Side history rows, consistent with this counterfactual stop calculation.

## 3. Side Macro-F1 checkpoint availability

### 3.1 Current final Side checkpoint

Current paper-aligned final checkpoint:

D:\Skripsi\Experiment_TA\experiment_18\checkpoints\side\best.pt

Metadata:

- selected metric: val_loss;
- mode: min;
- best epoch: 26;
- SHA-256: a37aedc2a5f5c3a02877a370ac67964663a409789134b949966d6c52802023fc.

This file is not the desired Macro-F1-selected checkpoint.

### 3.2 Existing standardized candidate

A separate physical checkpoint is available:

D:\Skripsi\Experiment_TA\archive\experiment_20_side_val_macro_f1\checkpoints\side\best.pt

Physical file:

- file size: 228,679,217 bytes;
- SHA-256: 0e8b30bff8773d2696a63378104a3d7701671b8a2647d7a553424def64a9fda6.

Supporting authoritative artifacts:

- archive\experiment_20_side_val_macro_f1\src\config.py, lines 33-34:
  CHECKPOINT_MONITOR_FRONT = 'val_macro_f1'
  CHECKPOINT_MONITOR_SIDE = 'val_macro_f1'
- archive\experiment_20_side_val_macro_f1\config\resolved_config.json:
  Side monitor val_macro_f1, max; Side early-stopping patience 5; Side scheduler patience 2.
- archive\experiment_20_side_val_macro_f1\results\side\train_summary.json:
  best_epoch 15; val_macro_f1; mode max; SHA-256 above.
- archive\experiment_20_side_val_macro_f1\results\side\test_eval_metrics.json:
  same checkpoint SHA, best_epoch 15, and Macro-F1 selection metadata.
- archive\experiment_20_side_val_macro_f1\results\side\history.csv:
  20 epochs, with maximum validation Macro F1 0.75724 at epoch 15.
- archived Side and fusion prediction files are present.

The standardized candidate’s training and validation metrics and learning rates match the first 20 epochs of the final Side val_loss history exactly when excluding epoch runtime duration. This supports that the candidate is a legitimate run of the same effective recipe through the alternative stopping point.

### 3.3 Provenance caveat

Some embedded candidate metadata paths point to:

D:\Skripsi\Experiment_TA\experiment_20\checkpoints\side\best.pt

That current root file has a different SHA-256 because it belongs to an augmentation-sensitivity setting. The embedded path is therefore stale or non-unique.

The archive candidate remains identifiable by:

- its physical file path;
- its physical SHA-256;
- matching SHA values in its train summary and test evaluation metadata;
- its own resolved configuration;
- its own source configuration;
- its complete history and predictions.

The audit does not use the stale embedded path as identity evidence.

### 3.4 Availability status

SIDE MAX-F1 CHECKPOINT: **AVAILABLE**

Qualification: available and metadata-verified in the authoritative repository; physical path and SHA must be used instead of the stale embedded path.

No model state was reconstructed from validation numbers, and no new inference was run.

## 4. Reusability of the old training trajectory

### FACT

- checkpoint_monitor is used for EarlyStopping score and mode;
- scheduler.step always receives validation Macro F1;
- optimizer updates do not use checkpoint_monitor;
- loss calculation does not use checkpoint_monitor;
- DataLoader sampling and training augmentation do not use checkpoint_monitor;
- the final Side val_loss history and standardized candidate history have identical metric and learning-rate fields through epoch 20;
- a Macro-F1-selected checkpoint and prediction artifacts exist for the seed-42 baseline.

### INFERENCE

Under the same initialization, data order, stochastic transforms, and runtime conditions, the checkpoint-monitor change alone does not alter optimizer or scheduler updates before the first different stopping decision. The standardized candidate’s matching first-20 history is direct supporting evidence for the actual available run.

The criterion does alter:

- which state is saved as best;
- when early stopping occurs;
- how many later optimizer and scheduler steps are executed.

### UNKNOWN

- Full bitwise identity of every parameter and optimizer tensor between a hypothetical rerun and the candidate is not independently established.
- The candidate run metadata records cudnn_deterministic=false, whereas the final Side run metadata records deterministic cuDNN settings. This is an environment/provenance caveat, not evidence that the candidate is unusable.
- The exact low-level relation between the stale embedded path and the archived physical file is not reconstructed; SHA-256 identity is used instead.

## 5. Retraining decision

Under the strict criterion specified by the audit request, NO RETRAIN REQUIRED for the main final Side model because:

1. a physically existing checkpoint selected by val_macro_f1/max is available;
2. its source/config metadata records the new criterion;
3. its effective Side training recipe matches the final Side recipe;
4. its best epoch is 15;
5. the checkpoint SHA is recorded consistently in the candidate summary and evaluation metadata;
6. its validation history, test predictions, and evaluation artifacts are present.

This conclusion is not based on validation scores alone.

If the archived candidate is rejected because the metadata path/environment caveat is considered unacceptable, then the fallback decision would be retraining required. The authoritative repository itself, however, contains enough artifacts to classify the candidate as available and metadata-verified.

## 6. Which artifacts need changes under standardization

| Artifact or result | Classification | Reason |
|---|---|---|
| Front final model | UNAFFECTED | Front already uses val_macro_f1/max; its checkpoint and predictions do not depend on Side selection. |
| Main Side final model | RE-EVALUATE ONLY | A valid standardized Side checkpoint and existing evaluation artifacts are available. |
| Average fusion | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side test predictions and archived fusion artifacts exist; current paper values use the old Side checkpoint. |
| Adaptive fusion | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side probabilities and adaptive fusion artifacts exist; current adaptive metrics use the old Side checkpoint. |
| Side confusion matrix | RECOMPUTE FROM EXISTING PREDICTIONS | The candidate Side test evaluation contains a different confusion matrix. |
| Fusion confusion matrices | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate fusion artifacts contain new average/adaptive matrices. |
| Side per-class recall | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side test metrics contain new safe-driving and phone-use recalls. |
| Fusion per-class recall | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate fusion metrics contain new class recalls. |
| Side ROC-AUC | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side probabilities and metric file exist. |
| Side PR-AUC | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side probabilities and metric file exist. |
| Side ECE | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side probabilities and metric file exist. |
| Side Brier score | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate Side probabilities and metric file exist. |
| Fusion ROC-AUC, PR-AUC, ECE, Brier | RECOMPUTE FROM EXISTING PREDICTIONS | Candidate fusion metrics are already stored. |
| Front/Side correctness overlap | RECOMPUTE FROM EXISTING PREDICTIONS | Side correctness changes; candidate paired predictions exist. |
| Fusion-rescued and fusion-broken cases | RECOMPUTE FROM EXISTING PREDICTIONS | These depend on paired Front and Side predictions; candidate complementarity artifacts exist. |
| Qualitative error examples / Fig. 3 | RECOMPUTE FROM EXISTING PREDICTIONS | Error-category membership can change; existing candidate predictions allow re-audit, but the currently selected examples are not automatically valid. |
| Adaptive-weight analysis / Fig. 4 | RECOMPUTE FROM EXISTING PREDICTIONS | Adaptive weights use Side probabilities; candidate prediction files exist. |
| Subject-cluster bootstrap | RECOMPUTE FROM EXISTING PREDICTIONS | Current intervals use old predictions. No standardized candidate bootstrap output was found, but candidate test predictions contain the inputs needed for recomputation. |
| Dataset and split facts | UNAFFECTED | No model-selection checkpoint affects counts, subjects, or stride. |
| Architecture and fusion equations | UNAFFECTED | The model and fusion definitions do not change. |
| Training hyperparameters other than monitor | UNAFFECTED | The standardized candidate keeps the same effective Side recipe. |
| Main training-configuration monitor statement | RE-EVALUATE ONLY | The Side cell would change from validation loss to validation Macro F1 if the candidate is adopted. |

### Existing standardized candidate values

These are reported only as artifact impact evidence, not as a new inference result.

Candidate Side test evaluation:

- Macro F1: 0.63045;
- accuracy: 0.80455;
- safe-driving recall: 0.32500;
- phone-use recall: 0.91111;
- confusion matrix: [[13, 27], [16, 164]];
- ROC-AUC: 0.71014;
- PR-AUC: 0.90842;
- ECE: 0.16615;
- Brier score: 0.15905.

Candidate Average Fusion:

- Macro F1: 0.76827;
- accuracy: 0.88182;
- confusion matrix: [[20, 20], [6, 174]];
- ROC-AUC: 0.86556;
- PR-AUC: 0.96264;
- ECE: 0.17850;
- Brier score: 0.12707.

Candidate Adaptive Fusion:

- Macro F1: 0.76827;
- accuracy: 0.88182;
- same hard confusion matrix as Average Fusion;
- ROC-AUC: 0.86806;
- PR-AUC: 0.96415;
- ECE: 0.17141;
- Brier score: 0.12402.

Candidate complementarity:

- both correct: 163;
- both wrong: 16;
- Front correct / Side wrong: 27;
- Front wrong / Side correct: 14;
- side-only correct: 14;
- fusion fixed Front error: 10;
- fusion broke Front correct: 6.

## 7. Robustness runs

Robustness artifacts are under:

D:\Skripsi\Experiment_TA\experiment_23

The robustness source and per-seed summaries record Side checkpoint selection as val_loss/min.

| Seed | Side criterion | Side history | Max-F1 epoch in history | Existing max-F1 checkpoint | Current Side checkpoint |
|---:|---|---|---:|---|---|
| 42 | val_loss/min in the final run | yes, 30 epochs | 15 | yes, archived standardized candidate | final run best.pt is val_loss epoch 26 |
| 43 | val_loss/min | yes, 19 epochs | 13 | no corresponding max-F1 checkpoint found | best.pt is val_loss epoch 14 |
| 44 | val_loss/min | yes, 18 epochs | 13 | no corresponding max-F1 checkpoint found | best.pt is val_loss epoch 13 |

Theoretical Macro-F1 early-stopping replay with patience 5 over the existing histories:

- seed 42: stop at epoch 20;
- seed 43: stop at epoch 7;
- seed 44: stop at epoch 18.

These are counterfactual replay results over existing histories, not retraining results. In particular, seed 43 would theoretically stop before the later validation-F1 maximum at epoch 13, so the old seed-43 trajectory cannot be treated as the standardized run’s actual future trajectory.

Robustness decision:

**PARTIAL rerun required if the robustness table must use the standardized criterion for all seeds.**

- Seed 42 can reuse the existing standardized candidate.
- Seed 43 requires Side retraining under val_macro_f1/max.
- Seed 44 requires Side retraining under val_macro_f1/max.
- After new Side checkpoints exist for seeds 43 and 44, their Side and fusion test metrics must be recomputed.
- The aggregate robustness table and paper discussion must then be recomputed.

## 8. Side augmentation sensitivity analysis

The four settings represented in the authoritative repository are:

| Setting | Side rotation | Side jitter | Current Side criterion | Max-F1 checkpoint under this setting |
|---|---:|---:|---|---|
| Baseline | 45 degrees | 0.8 | val_loss/min | available in archived standardized candidate |
| Variant 1 | 35 degrees | 0.7 | val_loss/min | not found |
| Variant 2 | 30 degrees | 0.6 | val_loss/min | not found |
| Variant 3 | 20 degrees | 0.4 | val_loss/min | not found |

Evidence:

- baseline: experiment_18 plus the archived standardized candidate;
- 35/0.7: experiment_22;
- 30/0.6: experiment_21;
- 20/0.4: experiment_20.

The three variant Side summaries all record val_loss/min. Their checkpoint directories contain best.pt but no per-epoch checkpoint set or corresponding Macro-F1-selected checkpoint was found.

Sensitivity decision:

**PARTIAL rerun required if the sensitivity analysis is required to follow the standardized protocol.**

- Baseline can reuse the existing standardized candidate.
- The three altered augmentation settings require retraining under val_macro_f1/max.
- Their current val_loss-selected results may remain as a separate explicitly labeled analysis of the old protocol, but they cannot be presented as results produced under the newly standardized criterion.
- Their fusion results also depend on the new Side checkpoints and must be recomputed after those retrains.

## 9. Paper impact map

Current paper examined:

D:\Skripsi\Paper_TA\main.tex

and included sections under:

D:\Skripsi\Paper_TA\sections

### UNCHANGED

The following remain valid regardless of Side checkpoint reselection:

- dataset definition and label mapping;
- subject-independent split;
- stride-30 sampling;
- post-stride sample counts;
- image preprocessing and augmentation definitions;
- EfficientNetV2-S architecture;
- probability-level average and adaptive fusion equations;
- Front checkpoint and Front test predictions;
- Front-only metrics;
- class weights and loss formulation;
- threshold definition;
- the fact that Macro F1 is the primary metric;
- figure of the model architecture;
- citation list and scientific references;
- conclusions about task scope, daytime RGB, fixed subject split, and single-backbone limitation.

### POTENTIALLY CHANGED

#### Abstract

Affected claims:

- Side Macro F1 0.67468;
- fusion Macro F1 0.81113;
- fusion-versus-Side comparison;
- fusion-versus-Front observed difference;
- bootstrap interpretation;
- statement that fusion is the strongest observed configuration.

Front-only values in the abstract remain unchanged, but the Side and fusion values must be replaced if the standardized candidate is adopted. The current paper’s bootstrap statement cannot be retained unchanged without recomputation.

#### Methodology / Section III

Affected statement:

- the Side checkpoint monitor currently says validation loss.

If standardization is adopted, this should describe validation Macro F1 for both Front and Side, with the same max direction. This is an impact only; the manuscript was not edited.

The optimizer, loss, scheduler monitor, augmentation, and other training configuration statements are otherwise unchanged. The source implementation does mean that the standardized Side protocol also uses Macro F1 for early stopping.

#### Training-configuration table

File:

D:\Skripsi\Paper_TA\tables\training_configuration.tex

Affected row:

- Checkpoint monitor: Side currently validation loss; standardized version would be validation Macro F1.

#### Main results table

File:

D:\Skripsi\Paper_TA\tables\main_results.tex

Affected rows:

- Side;
- Average Fusion;
- Adaptive Fusion.

Front row is unchanged. The archived standardized candidate contains replacement Side and fusion metrics, so this is an update from existing artifacts rather than a requirement for new inference.

#### RQ1 / single-view and complementarity discussion

File:

D:\Skripsi\Paper_TA\sections\05_results.tex

Potentially changed:

- Side performance comparison;
- Side per-class recall;
- confusion matrices;
- Front/Side correctness overlap;
- side-only-correct counts;
- qualitative error category membership;
- fusion-rescued and fusion-broken counts.

The current candidate complementarity artifact already shows different counts from the current paper.

#### Fig. 2

The view-overlap figure depends on paired predictions. Its underlying categories must be recomputed from the candidate predictions. The figure may need replacement if the selected examples or counts change.

#### Fig. 3

The qualitative error figure is tied to model-prediction categories. Existing image content is not automatically invalid, but each example must be rechecked against the standardized Side predictions.

#### RQ2 / fusion discussion

Potentially changed:

- Average and adaptive hard metrics;
- confusion matrix;
- observed differences versus Front and Side;
- complementarity counts;
- fusion-rescued and fusion-broken cases.

Existing standardized candidate fusion artifacts are available.

#### RQ3 / adaptive analysis

Potentially changed:

- adaptive probability metrics;
- ECE and Brier score;
- adaptive weight summaries;
- statement that hard decisions are identical;
- Fig. 4 numerical annotations.

The candidate adaptive artifact reports the same hard decisions as its candidate Average Fusion, but the probability-level values differ from the current paper and must be mapped before any manuscript update.

#### Robustness

File:

D:\Skripsi\Paper_TA\tables\robustness.tex

The current robustness table uses Side and fusion predictions from the val_loss protocol for all seeds. A standardized robustness table requires Side retraining for seeds 43 and 44 and subsequent recomputation. Seed 42 can use the existing standardized candidate.

#### Bootstrap

The current paper reports a subject-cluster bootstrap comparison. No standardized candidate bootstrap output was found in the inspected authoritative artifacts. The intervals must be recomputed from standardized candidate predictions and the same subject-cluster configuration before retaining any inferential claim.

#### Conclusion

The general methodological conclusion may remain directionally relevant, but numerical and inferential claims about Side, fusion, complementarity, and uncertainty are potentially changed. The conclusion must not retain old numeric claims after switching the Side checkpoint unless the candidate artifacts are adopted and the dependent analysis is updated.

### MUST BE RECOMPUTED before a standardized paper claim

- Side test metrics;
- Average Fusion metrics;
- Adaptive Fusion metrics;
- all Side/fusion confusion matrices;
- per-class recalls that use Side or fusion;
- ROC-AUC, PR-AUC, ECE, and Brier values involving Side or fusion;
- correctness-overlap counts;
- fusion-rescued and fusion-broken counts;
- adaptive-weight summaries;
- bootstrap intervals;
- qualitative example category verification;
- robustness aggregate after seeds 43 and 44 are standardized;
- sensitivity rows for the three altered augmentation settings if they are retained as part of the standardized protocol.

Existing candidate artifacts cover the baseline Side model and main seed-42 fusion outputs, but they do not cover standardized seed 43, seed 44, or the three altered sensitivity settings.

## 10. Decision summary

CURRENT FRONT CRITERION:
validation Macro F1, maximize; early stopping also uses validation Macro F1 with patience 4.

CURRENT SIDE CRITERION:
validation loss, minimize; early stopping also uses validation loss with patience 5.

SIDE MAX VALIDATION MACRO-F1 EPOCH:
epoch 15, validation Macro F1 0.75724 in the final Side history.

SIDE MAX-F1 CHECKPOINT AVAILABLE:
YES

Exact physical path:

D:\Skripsi\Experiment_TA\archive\experiment_20_side_val_macro_f1\checkpoints\side\best.pt

Epoch: 15

SHA-256:
0e8b30bff8773d2696a63378104a3d7701671b8a2647d7a553424def64a9fda6

WOULD MACRO-F1 EARLY STOPPING CHANGE STOP EPOCH:
YES

explanation: With the exact EarlyStopping implementation and final patience 5, the final Side history would stop at epoch 20 after five consecutive epochs without improvement following epoch 15. The old val_loss run reached the maximum 30 epochs.

FINAL SIDE RETRAIN REQUIRED:
NO

reason: An authoritative-repository candidate checkpoint already exists with val_macro_f1/max selection, best epoch 15, matching effective Side recipe, matching metadata SHA, complete history, and prediction/evaluation artifacts. This is not a decision based on validation numbers alone. The embedded checkpoint path is stale; use the physical archive path and SHA.

FRONT RETRAIN REQUIRED:
NO

reason: Front already uses validation Macro F1/max and its checkpoint and predictions are unaffected.

MAIN FUSION RECOMPUTATION REQUIRED:
CONDITIONAL

reason: If the existing standardized candidate and its archived Side/fusion predictions are accepted, no new inference is required; the candidate fusion metrics are already available. If that candidate is rejected, a new Side checkpoint would require new Side inference and fusion recomputation.

ROBUSTNESS RERUN REQUIRED:
PARTIAL

reason: Seed 42 has the standardized candidate. Seeds 43 and 44 have only val_loss-selected Side checkpoints and require Side retraining plus dependent evaluation/fusion recomputation.

SENSITIVITY RERUN REQUIRED:
PARTIAL

reason: The baseline has the standardized candidate. The three altered augmentation settings have only val_loss-selected Side checkpoints and require retraining if they must follow the standardized protocol.

DO ALL PREVIOUS EXPERIMENTS NEED TO BE RERUN:
NO

reason: Front and fixed methodology artifacts are unaffected. The main seed-42 Side and fusion artifacts already exist under the standardized criterion. Only dependent analyses without valid standardized artifacts need updating; for robustness and sensitivity this is partial, not all.

PAPER SECTIONS AFFECTED:
Abstract; Section III training/model-selection description; training-configuration table; main-results table; RQ1 single-view and complementarity discussion; Fig. 2 overlap; Fig. 3 qualitative error categories; RQ2 fusion discussion; RQ3 adaptive analysis and Fig. 4; robustness table/discussion; bootstrap statement; sensitivity discussion; conclusion.

FACT:
- Current Side uses val_loss/min for checkpoint and early stopping.
- The Side scheduler uses val_macro_f1/max with patience 2.
- Final Side history has 30 epochs.
- Final Side minimum validation loss is epoch 26.
- Final Side maximum validation Macro F1 is epoch 15.
- Exact alternative early stopping over the final history stops at epoch 20.
- An authoritative archived val_macro_f1/max Side checkpoint exists at epoch 15.
- Its physical SHA-256 is recorded consistently in candidate artifacts.
- Its first 20 metric and learning-rate history fields match the final Side run.
- Candidate Side and fusion predictions/evaluation artifacts exist.
- Seed 43 and seed 44 robustness Side runs remain val_loss-selected.
- Three altered augmentation sensitivity Side runs remain val_loss-selected.
- No standardized candidate bootstrap output was found.

INFERENCE:
- The monitor change is not checkpoint-only because the implementation reuses checkpoint_monitor for EarlyStopping.
- Existing standardized seed-42 candidate artifacts can be used without retraining or new inference for the main Side/fusion baseline.
- Side-dependent paper results cannot be assumed unchanged merely because the training recipe is otherwise fixed.

UNKNOWN:
- Full bitwise identity between the archived candidate and a hypothetical fresh run under the current final runtime environment.
- Whether the stale embedded paths were intended as provenance paths or are simply copied metadata.
- Whether the paper should adopt the archived standardized candidate or require a new clean rerun for administrative reproducibility.
- The standardized bootstrap interval until it is recomputed from candidate predictions.
- Whether the existing qualitative examples remain the preferred examples after prediction-category re-audit.

No source modification.
No retraining.
No new inference.
No manuscript modification.
No Git commit.
