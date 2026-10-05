# Final Manuscript-to-Experiment Consistency Audit

Audit type: read-only final consistency audit.

Audit date: 2026-09-22.

## Scope and safety

The current manuscript was audited from:

- `D:\Skripsi\Paper_TA\main.tex`
- all included section files and table files under `D:\Skripsi\Paper_TA`
- compiled PDF: `D:\Skripsi\Paper_TA\main.pdf`

The primary final experiment source was:

- `D:\Skripsi\Experiment_TA\experiment_18`

The supporting audit/fact source was:

- `D:\Skripsi\Experiment_TA\paper_audit`

The historical repository was not accessed directly. The two approved historical audit files were used only for the already-audited rationale questions:

- `paper_audit\historical_checkpoint_criterion_audit.md`
- `paper_audit\historical_class_weight_provenance_audit.md`

No manuscript, source code, checkpoint, experiment artifact, or Git state was modified. No retraining and no new model inference were performed.

## 1. Current manuscript structure

The compiled manuscript currently renders:

1. Introduction
2. Related Work
3. Methodology
   - Problem Formulation
   - Dataset and Binary Label Mapping
   - Single-View EfficientNetV2-S Models
   - Decision-Level Fusion
   - Average Fusion
   - Adaptive Fusion
   - Subject-Based Data Split
   - Frame Sampling and Preprocessing
   - Training Configuration
   - Reproducibility and Model Selection
   - Evaluation Protocol
   - Statistical Analysis
   - Error and Failure Analysis
   - Robustness and Additional Analyses
4. Results and Discussion
   - Single-View Performance and View Complementarity
   - Multi-View and Fusion Strategy
   - Exploratory Analysis, Robustness, and Uncertainty
5. Conclusion
6. References

Rendered tables: Table I, Table II, and Table III. Rendered figures: Fig. 1--Fig. 4.

The standalone `sections/06_discussion.tex`, `tables/ablation.tex`, `tables/robustness.tex`, and `tables/training_gap.tex` are not included by the current `main.tex`; their values are discussed or used only where the current manuscript explicitly reports them.

## 2. Artifact verification

### Final Experiment 18

Status: VERIFIED for the main Experiment 18 results.

- Front history, summary, evaluation metrics, predictions, checkpoint, and checkpoint hash are present.
- Side history, summary, evaluation metrics, predictions, checkpoint, and checkpoint hash are present.
- Fusion metrics, complementarity metrics, and paired fusion predictions are present.
- The final fusion prediction artifact contains 220 unique paired samples and the seven test subjects `[4, 8, 10, 11, 17, 21, 42]`.
- Front checkpoint: epoch 9, SHA-256 `1e8036ddb330649d7e51a7dc56cc697c915fb44a7e9873abb7dd440062b6ba35`.
- Side checkpoint: epoch 26, SHA-256 `a37aedc2a5f5c3a02877a370ac67964663a409789134b949966d6c52802023fc`.

The SHA-256 values in `results/run_metadata.json`, `results/best_checkpoint_metadata.json`, and the per-view summaries agree with the physical checkpoint files.

### Supporting audit artifacts

Status: VERIFIED for the stored audit tables and deterministic recomputations, with one bootstrap-value conflict documented below.

The approved audit artifacts include dataset/split checks, metric definitions, complementarity counts, adaptive-fusion diagnostics, robustness summaries, sensitivity summaries, qualitative-example validation, and the model-selection protocol audit.

## 3. Dataset, labels, and split

| Manuscript claim | Status | Evidence and result |
|---|---|---|
| Daytime RGB subset of 3MDAD | SUPPORTED | `experiment_18/src/config.py`; final manifest/audit facts |
| RGB1 = Side and RGB2 = Front | SUPPORTED | `src/config.py:46-51` |
| A1 = safe driving; A5--A9 = phone-use | SUPPORTED | `src/config.py:56-81` |
| safe = 0 and phone-use = 1; phone-use positive | SUPPORTED | `src/config.py:99-101`; prediction columns and paper methodology |
| 41,595 synchronized pairs before stride | SUPPORTED | `paper_audit/table_split.csv`, manifest facts |
| 6,761 safe and 34,834 phone-use pairs before stride | SUPPORTED | `paper_audit/table_dataset.csv` and manifest facts |
| RGB1/S31 AC9--AC10 correction applied at manifest level | SUPPORTED WITH QUALIFICATION | `src/config.py:86-96`; implementation is present, but a separate visual-proof artifact is not present |
| 35/8/7 train/validation/test subjects | SUPPORTED | `paper_audit/table_split.csv` |
| nominal 70/15/15 ratios and split seed 42 | SUPPORTED | `src/config.py:118-120`; manuscript wording is nominal, not an exact sample ratio claim |
| no subject overlap; same assignments for both views | SUPPORTED | `paper_audit/dataset_integrity.csv` and `table_split.csv` |
| post-stride counts 176/908/1084, 34/191/225, 40/180/220 | SUPPORTED | `paper_audit/table_split.csv`; paper Table I matches row-by-row |

## 4. Sampling, preprocessing, and architecture

The manuscript claims are supported by `experiment_18/src/config.py`, `dataset.py`, and `model.py`:

- stride 30 with `(frame-1) % 30 == 0`: supported (`dataset.py:26-30`, `config.py:165-171`);
- RGB loading, resize to 224 x 224, tensor conversion, and ImageNet normalization: supported (`dataset.py:23-24`, `config.py:125-127`);
- training horizontal flip, rotation, and ColorJitter: supported (`dataset.py:21-24`);
- Front rotation 68 degrees and jitter 1.2; Side rotation 45 degrees and jitter 0.8: supported (`config.py:155-161`);
- default hue 0: supported by the exact `ColorJitter` call, which specifies brightness, contrast, and saturation but no hue;
- deterministic validation/test preprocessing: supported (`dataset.py:24`);
- `timm` identifier `tf_efficientnetv2_s`, pretrained initialization, feature extraction with `num_classes=0`, Dropout, and a two-logit Linear head: supported (`config.py:129-130`, `model.py:69-77`);
- logits go to CrossEntropyLoss, while softmax class-1 probabilities are used during inference/fusion: supported (`train.py:110`, `train.py:46`, `fusion.py:38`);
- class index 1 is phone-use: supported (`config.py:99-101`, `model.py:74`).

No incorrect architectural statement was found. Omitted implementation trivia, such as the exact pooled feature dimension, was not treated as an error.

## 5. Training configuration and model selection

### Table II and training prose

All displayed Table II cells match the final resolved metadata:

| Setting | Front | Side | Status |
|---|---:|---:|---|
| Learning rate | 3e-5 | 2e-5 | SUPPORTED |
| Weight decay | 5e-4 | 1e-3 | SUPPORTED |
| Dropout | 0.4 | 0.4 | SUPPORTED |
| Freeze-stage setting | 5 | 4 | SUPPORTED |
| Rotation | 68 degrees | 45 degrees | SUPPORTED |
| Color jitter | 1.2 | 0.8 | SUPPORTED |
| Checkpoint monitor | validation Macro F1 | validation loss | SUPPORTED |

The shared training claims are also supported: AdamW, batch size 32, maximum 30 epochs, image size 224, stride 30, dropout 0.4, label smoothing 0.0, and weighted CrossEntropyLoss.

### Exact final checkpoint evidence

The final checkpoints used by the paper are:

- Front: `experiment_18/checkpoints/front/best.pt`, selected epoch 9, `val_macro_f1` / max.
- Side: `experiment_18/checkpoints/side/best.pt`, selected epoch 26, `val_loss` / min.

The final evaluation files reference those same paths and hashes. This supports the paper's implementation statement and final-model provenance.

### Source behavior

The source confirms the relevant logic:

- `src/train.py:78-82`: the checkpoint monitor is view-specific and mode is `max` for `val_macro_f1` and `min` for `val_loss`;
- `src/train.py:110`: `ReduceLROnPlateau` is constructed with `mode='max'`, while `EarlyStopping` receives the checkpoint-derived mode;
- `src/train.py:120`: the scheduler is stepped on validation Macro F1;
- `src/train.py:122-127`: the same selected score is passed to early stopping and the loop stops after the configured patience;
- `src/train.py:124`: the physical checkpoint is saved when that score improves.

The paper does not claim a scheduler monitor in Table II or prose, so the scheduler implementation does not contradict a manuscript statement.

### Side model-selection rationale

Status: SUPPORTED WITH QUALIFICATION.

The current final repository proves the implementation but does not independently contain the historical decision record. The approved `historical_checkpoint_criterion_audit.md` records contemporaneous evidence that Side validation-loss selection was introduced to test stabilization of Side probability outputs for fusion after unsatisfactory Side/fusion behavior. The same approved audit explicitly states that the rationale is only partial: the criterion change was accompanied by other configuration changes, and the artifacts do not establish that validation Macro F1 alone was rejected as too noisy.

The manuscript wording is therefore acceptable as a qualified rationale, but it should not be read as criterion-only causal evidence.

### Class-weight implementation and rationale

Status: implementation SUPPORTED; exact numeric rationale UNSUPPORTED/NOT ESTABLISHED.

The final metadata and source confirm fixed weights `[2.5, 1.0]`, ordered `[safe_driving, phone_use]`, for both views, passed to weighted CrossEntropyLoss. The paper only states the direct effect that the minority safe-driving class receives a larger loss contribution; it does not claim inverse-frequency derivation or validation/test selection. That wording is supported.

The approved `historical_class_weight_provenance_audit.md` states that the exact numeric origin of 2.5 is not documented and that standard frequency formulas do not produce `[2.5, 1.0]`. No overclaim was found in the manuscript.

## 6. Reproducibility audit

The source sets Python random, `PYTHONHASHSEED`, NumPy, PyTorch CPU/CUDA seeds, `cudnn.deterministic=True`, and `cudnn.benchmark=False` (`src/train.py:17-18`). The paper explicitly says that these settings control stochasticity but does not claim full bitwise determinism. This is SUPPORTED WITH QUALIFICATION.

An artifact-level discrepancy remains: `results/run_metadata.json` records `cudnn_deterministic: false`, while both per-view checkpoint metadata environments and the training source record `true`. The manuscript's restrained wording is supported by source and per-view metadata, but the run-level metadata conflict should be resolved or documented before claiming an entirely unambiguous run configuration.

The audit also found no `DataLoader` generator, `worker_init_fn`, or `torch.use_deterministic_algorithms` in Experiment 18. The paper does not claim those controls or bitwise determinism.

## 7. Fusion equations and metric definitions

The manuscript equations match `src/fusion.py`:

- average: `p_avg = 0.5*p_front + 0.5*p_side` (`fusion.py:31`);
- confidence: `c_k = abs(p_k - 0.5)` (`fusion.py:32`);
- adaptive weights: softmax over those confidence scores (`fusion.py:32`);
- adaptive probability: weighted sum of the two probabilities (`fusion.py:32`);
- threshold: 0.5, with `>=` assigned to phone-use (`fusion.py:44`, `fusion.py:56`);
- no calibration step before fusion: supported by source and `paper_facts.md`.

The manuscript also correctly states that the confidence heuristic is not assumed equivalent to correctness. Metric definitions match `src/metrics.py`, including Macro F1, ROC-AUC, PR-AUC, ten-bin ECE, Brier score, and confusion-matrix convention.

## 8. Main test results and confusion matrices

All Table III values match the final JSON metrics and recomputation from the final fusion prediction CSV:

| Method | Macro F1 | Accuracy | Macro Precision | Macro Recall | Safe Recall | Phone Recall | Confusion matrix |
|---|---:|---:|---:|---:|---:|---:|---|
| Front | 0.76626 | 0.86364 | 0.77183 | 0.76111 | 0.60000 | 0.92222 | `[[24,16],[14,166]]` |
| Side | 0.67468 | 0.80455 | 0.67305 | 0.67639 | 0.47500 | 0.87778 | `[[19,21],[22,158]]` |
| Average Fusion | 0.81113 | 0.89545 | 0.83868 | 0.79028 | 0.62500 | 0.95556 | `[[25,15],[8,172]]` |
| Adaptive Fusion | 0.81113 | 0.89545 | 0.83868 | 0.79028 | 0.62500 | 0.95556 | `[[25,15],[8,172]]` |

Rows are true labels and columns are predicted labels in the order `[safe driving, phone-use]`. All confusion-matrix entries agree with the prediction artifact.

Per-class decomposition also matches:

- Front: safe F1 0.61538; phone-use F1 0.91713.
- Side: safe F1 0.46914; phone-use F1 0.88022.
- Average and Adaptive: safe F1 0.68493; phone-use F1 0.93733.

## 9. Complementarity and Fig. 2

Status: SUPPORTED.

The final paired prediction artifact gives:

- both correct: 164;
- Front only correct: 26;
- Side only correct: 13;
- both wrong: 17;
- total: 220.

The reported fusion behavior also matches: average fusion fixed 13 Front errors and broke 6 Front-correct cases. The Fig. 2 PDF in the paper has the same SHA-256 as the audited source figure. The surrounding text is descriptive and does not claim that viewpoint caused the errors.

## 10. Qualitative examples and Fig. 3

Status: SUPPORTED.

The audited figure-generation script validates each displayed row against `D:\Skripsi\Experiment_TA\results\final_exp18_complementarity_per_sample.csv` before rendering. The three displayed cases are:

| Panel | Subject/activity/frame | Ground truth | Front | Side | Front p(phone) | Side p(phone) |
|---|---|---|---|---|---:|---:|
| (a) Side helps | 17 / 8 / 91 | Phone-use | Safe | Phone-use | 0.390 | 0.716 |
| (b) Front helps | 42 / 9 / 61 | Phone-use | Phone-use | Safe | 0.956 | 0.493 |
| (c) Both fail | 11 / 1 / 91 | Safe | Phone-use | Phone-use | 0.822 | 0.718 |

The full file paths in the paired prediction artifact have matching subject, activity, and frame keys across Front and Side. The paper figure is byte-identical to the audited source figure. The wording `appears to provide a more informative perspective` is appropriately limited to a representative example; no visual cause is presented as ground truth.

## 11. Average/adaptive fusion and Fig. 4

Status: SUPPORTED.

The paper's hard-decision and probability-level claims match the stored metrics:

- identical hard predictions: 220/220;
- probability scores changed: 220/220;
- decision changes: 0/220;
- mean front weight: 0.51260;
- population standard deviation of front weight: 0.03914;
- front weights in [0.45, 0.55]: 173/220;
- front weights in [0.40, 0.60]: 219/220;
- mean absolute probability shift: 0.00757;
- maximum absolute probability shift: 0.05103;
- Average: ROC-AUC 0.86292, PR-AUC 0.96236, ECE 0.17916, Brier 0.12341;
- Adaptive: ROC-AUC 0.86500, PR-AUC 0.96329, ECE 0.17159, Brier 0.12028.

The manuscript correctly separates hard-decision quality from probability-level metrics and does not claim that adaptive fusion improves the hard-decision metric.

## 12. Sensitivity and robustness

The sensitivity wording is SUPPORTED WITH QUALIFICATION. The stored audit table contains four settings, keeps Front fixed, changes Side rotation/jitter, and records Side Macro F1 range 0.67468--0.76019 and fusion Macro F1 range 0.77327--0.81113. The paper explicitly calls the analysis descriptive, exploratory, test-informed, and not fully test-blind or pre-registered. It does not make a causal claim.

The robustness values and ordering are SUPPORTED:

- seeds: 42, 43, 44;
- Front: 0.76626, 0.72049, 0.75940; reported mean +/- sample std 0.74872 +/- 0.02468;
- Side: 0.67468, 0.66353, 0.70213; reported mean +/- sample std 0.68011 +/- 0.01987;
- Average and Adaptive: 0.81113, 0.74028, 0.76626; reported mean +/- sample std 0.77256 +/- 0.03584;
- Fusion > Front > Side holds for each listed seed.

The paper does not label the reported standard deviations as population standard deviations; the values match sample standard deviation (`ddof=1`) in the stored aggregate.

## 13. Bootstrap audit

The manuscript correctly states the design-level facts: subject-cluster resampling, 7 test subjects, 10,000 repetitions, and 95% intervals. It also correctly interprets the Front comparison as crossing zero and the Side comparison as positive.

However, exact interval values are not uniquely consistent across the available audit artifacts:

| Comparison | Manuscript | `paper_audit/table_statistics.csv` | Later deterministic deep-audit artifact |
|---|---:|---:|---:|
| Average - Front | `[-0.03467, 0.14186]` | `[-0.03467, 0.14186]` | `[-0.03270, 0.13884]` |
| Average - Side | `[0.09749, 0.19156]` | `[0.09749, 0.19156]` | `[0.09801, 0.19127]` |

The later artifact is `paper_audit/model_selection_protocol_deep_audit_tables/within_protocol_bootstrap.csv`, generated by the stored audit implementation in `paper_audit/deep_model_selection_audit.py:627-665`. The manuscript values therefore match one existing audit table, but not the later deterministic recomputation from the same P1 prediction artifact. The qualitative conclusions remain the same, but the exact numerical provenance is unresolved.

Classification: **UNCERTAIN**, severity **MAJOR for numerical final-lock**, because the exact reported confidence limits cannot be uniquely selected from the conflicting stored audit outputs. This is not evidence that the bootstrap conclusion changes; it is an artifact-consistency issue that should be resolved before claiming numerical PASS.

## 14. Literature-claim boundary

Literature claims are not treated as experiment claims. Structural checks pass:

- citations are present and resolve in the compiled PDF;
- the two new EfficientNetV2 references are described only as transfer-learning applications to MRI and histopathological image classification;
- neither is described as a driver-monitoring study.

The literature claims are therefore `NOT AUDITABLE FROM EXPERIMENT ARTIFACTS` in the strict experimental sense, but no structural citation or scope error was found.

## 15. Dangerous-wording review

The manuscript contains terms such as `best`, `strongest observed`, `support`, `stabilize`, `confidence`, and `robustness`. Context review found:

- `best single-view` is used for the highest observed single-view Macro F1 and is numerically supported;
- `strongest observed` is explicitly qualified as observed and is not presented as universal superiority;
- `support` is used with the bootstrap limitation and does not claim significance against Front;
- `stabilize` is tied to the approved historical rationale and remains qualified by the absence of criterion-only causal evidence;
- `confidence` is defined as distance from the 0.5 boundary and is explicitly not equated with correctness;
- `robustness` is used for the named seed analysis and not as a generalization guarantee.

No dangerous overclaim requiring automatic removal was found. The bootstrap exact-value conflict remains the only major numerical issue.

## 16. Figure and table placement review

The six-page compiled PDF was rendered and inspected page-by-page.

- Fig. 1 is placed adjacent to the methodology text that introduces the pipeline.
- Table I appears with the split/preprocessing discussion.
- Table II appears with training configuration and model-selection prose.
- Table III appears before the main result discussion.
- Fig. 2 and Fig. 3 appear near their first textual references in the RQ1 subsection.
- Fig. 4 appears near the adaptive-fusion discussion.
- Labels, captions, and axes are readable; no clipping, overlap, or misleading float placement was observed.
- The final PDF has 6 pages.

Layout status: PASS.

## 17. Numerical consistency cross-check summary

The detailed cross-check is saved as `paper_audit/final_manuscript_numeric_crosscheck.csv`.

Results:

- Main dataset counts, split counts, preprocessing values, training configuration, class weights, checkpoint criteria, model metrics, confusion matrices, complementarity counts, qualitative examples, adaptive diagnostics, sensitivity ranges, and robustness values: MATCH.
- Bootstrap exact confidence limits: CONFLICTING AUTHORITATIVE AUDIT ARTIFACTS; unresolved.
- Run-level cuDNN metadata: CONFLICTING METADATA; source/per-view summaries support the paper wording, but run-level record differs.

## 18. Final claim audit table

| Section | Claim | Status | Severity | Evidence | Recommended action |
|---|---|---|---|---|---|
| Abstract | Dataset, views, model family, split, and primary metric | SUPPORTED | NONE | config, manifests, paper text | KEEP |
| Abstract | Front/Side/Fusion Macro F1 values | SUPPORTED | NONE | final metrics and predictions | KEEP |
| Abstract | Adaptive has identical hard decisions but changes probability-level metrics | SUPPORTED | NONE | adaptive metrics and diagnostics | KEEP |
| Abstract | Bootstrap interval against Front crosses zero; Side interval positive | SUPPORTED WITH QUALIFICATION | MAJOR | two audit bootstrap versions agree qualitatively but differ numerically | INVESTIGATE |
| Methodology | Dataset and binary label mapping | SUPPORTED | NONE | config and manifests | KEEP |
| Methodology | S31 correction applied at manifest level | SUPPORTED WITH QUALIFICATION | MINOR | config/manifest implementation; no separate visual-proof file | KEEP |
| Methodology | Preprocessing and augmentation | SUPPORTED | NONE | dataset.py and config.py | KEEP |
| Methodology | EfficientNetV2-S, pretrained, two logits, softmax only at inference | SUPPORTED | NONE | model.py, train.py, fusion.py | KEEP |
| Methodology | Fixed class weights [2.5, 1.0] and minority-class effect | SUPPORTED | NONE | config, checkpoint metadata, train.py | KEEP |
| Methodology | Exact numeric origin of 2.5 | NOT CLAIMED; rationale not established | NONE | approved class-weight audit | KEEP |
| Methodology/Table II | View-specific training configuration | SUPPORTED | NONE | resolved config and checkpoint metadata | KEEP |
| Methodology | Front val Macro F1/max and Side val loss/min | SUPPORTED | NONE | source, summaries, checkpoints | KEEP |
| Methodology | Side rationale for probability stabilization | SUPPORTED WITH QUALIFICATION | MINOR | approved checkpoint-criterion audit | KEEP WITH QUALIFICATION |
| Methodology | Reproducibility controls without bitwise determinism | SUPPORTED WITH QUALIFICATION | MINOR | source/per-view metadata versus run_metadata discrepancy | INVESTIGATE |
| Methodology | Fusion equations and threshold | SUPPORTED | NONE | fusion.py | KEEP |
| Results/Table III | Main metrics and confusion matrices | SUPPORTED | NONE | final metrics and predictions | KEEP |
| Results/RQ1 | Complementarity counts and Front-error rescue/break counts | SUPPORTED | NONE | complementarity artifact | KEEP |
| Results/Fig. 3 | Representative sample identities, labels, predictions, and probabilities | SUPPORTED | NONE | locked qualitative validation script and CSV | KEEP |
| Results/RQ2/RQ3 | Average/adaptive hard and probability-level behavior | SUPPORTED | NONE | fusion metrics and adaptive audit | KEEP |
| Results | Sensitivity wording as exploratory/test-informed | SUPPORTED | NONE | sensitivity table and audit | KEEP |
| Results | Robustness seed values and ordering | SUPPORTED | NONE | robustness artifacts | KEEP |
| Results/Conclusion | Exact bootstrap intervals | SUPPORTED WITH QUALIFICATION | MAJOR | manuscript matches older table, not later recomputation | INVESTIGATE |
| Related Work | EfficientNetV2 MRI/histopathology scope | NOT AUDITABLE FROM EXPERIMENT ARTIFACTS | NONE | bibliography and wording structurally match | KEEP |

## 19. Hallucination check

### A. Does the manuscript contain any number not traceable to an authoritative experiment artifact?

**UNCERTAIN.** Nearly all numbers trace directly to final artifacts. The exact bootstrap limits have conflicting audit versions, so their unique provenance is not established.

### B. Does the manuscript contain any methodological statement contradicted by the final implementation?

**NO**, with the run-level cuDNN metadata discrepancy recorded as an artifact conflict rather than a source contradiction.

### C. Does any figure display probabilities or counts that do not match final predictions?

**NO.** Fig. 2, Fig. 3, and Fig. 4 match the stored final prediction/audit artifacts; the paper copies of the three audited PDFs are byte-identical to the audit sources.

### D. Does the manuscript attribute causality where only descriptive evidence exists?

**NO.** The RQ1 paragraph explicitly says observations are descriptive rather than causal, and sensitivity limitations are stated.

### E. Does the manuscript claim an experimental rationale unsupported by final artifacts or approved historical audits?

**NO**, subject to the qualification that the Side rationale is only partially supported and is not criterion-only causal evidence.

### F. Does the manuscript mix historical exploratory experiments into the final Experiment 18 narrative?

**NO.** The final numerical narrative uses Experiment 18 and the approved audit summaries; no historical experiment IDs appear in the manuscript.

### G. Does any paper statement appear invented solely to make the method sound stronger?

**NO evidence found.** The strongest claims are qualified as observed, descriptive, exploratory, or uncertainty-limited.

## 20. FACT / INTERPRETATION / UNKNOWN

### FACT

- The main Experiment 18 metrics, configurations, checkpoints, predictions, confusion matrices, complementarity counts, qualitative examples, adaptive diagnostics, sensitivity ranges, and robustness values are traceable and match the manuscript.
- Front uses validation Macro F1/max; Side uses validation loss/min.
- Class weights are fixed `[2.5, 1.0]` in `[safe_driving, phone_use]` order for both views.
- Average and adaptive fusion have identical hard predictions on the 220-sample test set.
- The current PDF is six pages and has no observed clipping or overlap.

### INTERPRETATION

- The Side rationale can be described as a historically documented probability-stabilization motivation, but not as proof that criterion alone caused any later outcome.
- The side view provides descriptive complementary evidence for a subset of samples.
- The fusion result is the strongest observed point estimate, not an unconditional claim of superiority.

### UNKNOWN

- Which of the two stored subject-cluster bootstrap implementations is the canonical source for the exact intervals printed in the paper.
- Why `run_metadata.json` records cuDNN deterministic mode false while the source and per-view checkpoint metadata record true.
- The exact numerical origin/selection process for the fixed value 2.5; the manuscript does not claim one.

## 21. Final verdict

The manuscript is substantively consistent with the final Experiment 18 implementation and prediction artifacts. No broad manuscript rewrite is indicated. However, a final-lock decision should not be marked fully numerical PASS until the bootstrap artifact conflict is resolved and the cuDNN metadata discrepancy is explained.

FINAL MANUSCRIPT CONSISTENCY:

NUMERICAL CONSISTENCY:
UNCERTAIN

METHOD CONSISTENCY:
PASS

FIGURE CONSISTENCY:
PASS

MODEL-SELECTION RATIONALE:
PARTIALLY SUPPORTED

CLASS-WEIGHT RATIONALE:
PARTIALLY SUPPORTED

CAUSAL-CLAIM SAFETY:
PASS

HALLUCINATION RISK:
MINOR

CRITICAL ISSUES:
None found.

MAJOR ISSUES:
The exact bootstrap confidence limits printed in the paper match `paper_audit/table_statistics.csv` but differ from the later deterministic deep-audit recomputation from the same P1 prediction artifact. Resolve the canonical bootstrap artifact before final lock.

MINOR ISSUES:
`run_metadata.json` records `cudnn_deterministic=false`, while source/per-view checkpoint metadata record true. The manuscript wording is restrained, but the metadata discrepancy should be explained.

UNSUPPORTED CLAIMS:
No unsupported experimental claim requiring removal was found. The exact numeric origin of class weight 2.5 is not established, but the manuscript does not claim a derivation.

CONTRADICTED CLAIMS:
None found.

VALUES NOT TRACEABLE TO ARTIFACT:
No unique provenance for the exact bootstrap limits; two stored audit outputs disagree.

RECOMMENDATION:
INVESTIGATION REQUIRED

The required investigation is limited to reconciling the existing bootstrap outputs and run metadata. No retraining, inference, or manuscript edit is recommended as part of this audit.
