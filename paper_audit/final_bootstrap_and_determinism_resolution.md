# Final Bootstrap and Determinism Resolution

## Scope and safety

This is a read-only resolution audit scoped to the authoritative final repository `D:\Skripsi\Experiment_TA`. The historical repository was not accessed or used. No retraining, new model inference, checkpoint modification, source modification, manuscript modification, or Git commit was performed.

Only deterministic statistical recomputation from the existing Experiment 18 final prediction CSV was performed. New diagnostic outputs were written under `paper_audit\final_resolution\` and do not overwrite prior artifacts.

## 1. Bootstrap conflict

### Observed conflict

The manuscript and `paper_audit\table_statistics.csv` report:

| Comparison | Manuscript / `table_statistics.csv` |
|---|---:|
| Average − Front | `[-0.03467, 0.14186]` |
| Average − Side | `[0.09749, 0.19156]` |

The later model-selection audit reports:

| Comparison | `model_selection_protocol_deep_audit_tables\within_protocol_bootstrap.csv` |
|---|---:|
| Average − Front | `[-0.03270, 0.13884]` |
| Average − Side | `[0.09801, 0.19127]` |

### Input identity

Both comparisons refer to the same final P1 prediction artifact:

`D:\Skripsi\Experiment_TA\experiment_18\results\predictions\fusion_test_predictions.csv`

- SHA-256: `07fcb5e5cb04c30f5af2d8d26573d3047b72294ec26e1827a89810d1d589ce26`
- Rows: 220
- Unique `(subject_id, activity_id, frame)` samples: 220
- Test subjects: 7
- Subject row counts: subject 10 = 30, 11 = 27, 17 = 35, 21 = 33, 4 = 32, 42 = 25, 8 = 38
- Observed point estimates recomputed from this file: Average − Front = `0.04487475995698731`; Average − Side = `0.13645128171351606`

The equal input hash and equal observed point estimates show that the conflict is not due to different final predictions or a different test set. It is an interval-generation/provenance conflict.

### Surviving canonical implementation

The surviving explicit subject-cluster implementation is present in both:

- `D:\Skripsi\Experiment_TA\paper_audit\generate_standardization_reports.py:65-108`
- `D:\Skripsi\Experiment_TA\paper_audit\deep_model_selection_audit.py:627-665`

The implementation establishes:

1. clusters are the seven test subjects;
2. subject groups use first appearance order from the prediction file;
3. the random generator is `np.random.default_rng(seed)`;
4. the seed is `42`;
5. each replicate samples seven subject indices with replacement;
6. Macro F1 is recomputed from aggregated confusion counts;
7. the 2.5th and 97.5th percentiles use NumPy's default percentile method;
8. the number of replicates is 10,000.

The deterministic reproduction saved at `D:\Skripsi\Experiment_TA\paper_audit\final_resolution\bootstrap_reproduction.json` reproduces the later deep-audit values exactly from the hashed final prediction CSV:

| Comparison | Observed difference | Canonical 95% CI |
|---|---:|---:|
| Average − Front | `0.04487475995698731` | `[-0.032702300061770995, 0.13884389171745493]` |
| Average − Side | `0.13645128171351606` | `[0.09800745235314207, 0.19126612106447805]` |

The current authoritative repository does not contain a surviving source path that generates the older `table_statistics.csv` interval values. `table_statistics.csv` records the high-level method, seven clusters, 10,000 repetitions, and point estimates, but not the RNG implementation, cluster ordering, or executable provenance that would reproduce its exact endpoints. The exact old generating mechanism is therefore not established.

Diagnostic tests of common alternative RNG/order choices were performed only as provenance checks. They did not establish a unique implementation that reproduces both old intervals simultaneously. Their results are saved in `final_resolution\bootstrap_reproduction.json` and `final_resolution\bootstrap_order_search.json`.

### Root cause

**ROOT CAUSE:** statistical-artifact provenance drift: two stored outputs use the same final predictions and the same high-level subject-cluster/bootstrap description but have different exact resampling implementation provenance. The precise historical cause of the older endpoints—such as an unrecorded RNG/order/code-path difference—is **not established from the authoritative artifacts**.

This is not evidence of a changed model, changed prediction input, or changed qualitative conclusion.

### Canonical implementation and manuscript impact

The canonical result for final-lock purposes is the later explicit and exactly reproducible subject-cluster implementation described above. The manuscript's exact numerical limits therefore **need update** if numerical consistency with the surviving canonical implementation is required:

> The primary inferential comparison uses the subject-cluster bootstrap described in Section III. For Average versus Front, the observed Macro F1 difference was +0.04487 with a 95% interval of **[-0.03270, 0.13884]**, which included zero; versus Side, the difference was +0.13645 with interval **[0.09801, 0.19127]**.

No manuscript edit was made. The qualitative conclusion is unchanged: the Average-versus-Front interval includes zero, while the Average-versus-Side interval remains positive.

## 2. cuDNN conflict

### Conflicting artifacts

`D:\Skripsi\Experiment_TA\experiment_18\results\run_metadata.json` records:

```json
"cudnn_deterministic": false,
"cudnn_benchmark": false
```

The training source at `experiment_18\src\train.py:17-18` contains:

```python
def seed_everything(seed=42):
    random.seed(seed); os.environ['PYTHONHASHSEED']=str(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False
```

`experiment_18\src\train.py:68` calls `seed_everything(SPLIT_SEED)` at the start of `run_training` when training seeding is enabled. The same training file writes per-view training summaries with `env_metadata()` at `train.py:128`.

### Process and timestamp evidence

`experiment_18\run_experiment.ps1` launches:

- front training at line 44: `python -m src.train --view front`;
- side training at line 45: `python -m src.train --view side`;
- summary at line 60: `python -m src.summarize --root .`.

These are separate Python subprocess invocations. `src/summarize.py:26` writes `results/run_metadata.json` by calling `env_metadata()` directly. It does not call `seed_everything()` or set cuDNN deterministic mode before taking that environment snapshot.

The timestamps are consistent with this process distinction:

| Artifact | Timestamp | cuDNN deterministic |
|---|---:|---:|
| Front `train_summary.json` | `2026-09-12T04:44:46` | `true` |
| Side `train_summary.json` | `2026-09-12T04:49:51` | `true` |
| Root `run_metadata.json` | `2026-09-12T04:50:53` | `false` |

The root metadata file was therefore generated after both training workers and reflects the summary-process state, not the state captured during the front or side training workers.

### Determinism conclusion

**ACTUAL TRAINING PROCESS CUDNN DETERMINISTIC: TRUE.**

This conclusion is supported by the training source and both per-view training summaries. The root `run_metadata.json` value is not valid evidence that the training workers used `false`; it is a process-context metadata mismatch caused by summary-time capture.

The manuscript wording in `D:\Skripsi\Paper_TA\sections\04_experimental_setup.tex` is restrained: it states that cuDNN deterministic mode is enabled and benchmarking is disabled, while also stating that full bitwise determinism is not assumed. That wording is **SUPPORTED**, with the qualification that `run_metadata.json` should not be cited as the training-worker environment record.

## 3. FACT / INFERENCE / UNKNOWN

### FACT

- The two bootstrap CI pairs use the same final prediction file hash, 220 samples, and seven subject clusters.
- The later stored bootstrap implementation is explicit, uses `default_rng(42)`, 10,000 subject-cluster resamples, aggregated confusion counts, and NumPy percentile endpoints.
- That implementation reproduces `[-0.03270, 0.13884]` and `[0.09801, 0.19127]` exactly before display rounding.
- `table_statistics.csv` and the manuscript contain a different CI pair.
- The surviving repository does not identify the executable provenance that generated the older exact endpoints.
- `train.py` sets `torch.backends.cudnn.deterministic=True` before training and disables benchmarking.
- Front and Side training summaries record `cudnn_deterministic=true`.
- `summarize.py` writes root `run_metadata.json` in a separate summary process without reapplying the training seed/cuDNN settings, and that file records `false`.

### INFERENCE

- The bootstrap conflict is best classified as statistical-artifact provenance drift rather than a model/prediction discrepancy.
- The cuDNN conflict is explained by summary-process environment capture rather than evidence that the training workers used nondeterministic cuDNN.

### UNKNOWN

- The exact old code path, RNG state, cluster ordering, or other implementation detail that produced the older `table_statistics.csv` endpoints.
- Whether any unrecorded environment setting affected the old bootstrap calculation beyond the surviving artifacts.
- Full bitwise identity of all training operations across hardware/software executions; the manuscript does not claim it.

## 4. Final resolution

BOOTSTRAP CONFLICT:
ROOT CAUSE:
Statistical-artifact provenance drift. The same final prediction input and point estimates are paired with two different exact CI outputs. The old endpoint-generating implementation is not preserved in the authoritative repository.
CANONICAL IMPLEMENTATION:
The later explicit subject-cluster implementation in `paper_audit/generate_standardization_reports.py:65-108` and `paper_audit/deep_model_selection_audit.py:627-665`: seven subjects, 10,000 resamples, seed 42, `np.random.default_rng`, first-appearance cluster order, aggregated confusion-count Macro F1, and default NumPy percentiles.
CANONICAL AVERAGE-FRONT CI:
[-0.03270, 0.13884] (full values: [-0.032702300061770995, 0.13884389171745493])
CANONICAL AVERAGE-SIDE CI:
[0.09801, 0.19127] (full values: [0.09800745235314207, 0.19126612106447805])
CURRENT MANUSCRIPT VALUES:
NEED UPDATE
QUALITATIVE CONCLUSION:
UNCHANGED

CUDNN CONFLICT:
ROOT CAUSE:
`run_metadata.json` was captured by the separate summary subprocess through `src/summarize.py:26`, without calling the training seed/cuDNN setup. It records summary-process state, while per-view training summaries capture the actual training-worker state.
ACTUAL TRAINING PROCESS CUDNN DETERMINISTIC:
TRUE
RUN_METADATA STATUS:
Summary-process environment snapshot; not a valid training-worker cuDNN record. It is internally consistent with the post-training summary process but misleading if interpreted as the training configuration.
CURRENT MANUSCRIPT WORDING:
SUPPORTED

FINAL LOCK STATUS:
NUMERICAL CONSISTENCY:
FAIL
METHOD CONSISTENCY:
PASS
HALLUCINATION RISK:
MINOR
MANUSCRIPT CHANGE REQUIRED:
YES
IF YES:
Update only the two exact bootstrap interval values in the Results paragraph: `[-0.03467, 0.14186]` → `[-0.03270, 0.13884]`; `[0.09749, 0.19156]` → `[0.09801, 0.19127]`. No cuDNN wording change is required by this audit.
