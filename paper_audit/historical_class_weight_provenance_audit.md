# Historical Class-Weight Provenance Audit

Audit type: read-only historical provenance audit

Date: 2026-09-22

Authoritative final repository: D:/Skripsi/Experiment_TA

Historical repository: D:/Skripsi/Experiment

## Scope and safety

This audit uses the authoritative final repository and the historical repository only to trace the provenance of the fixed vector [2.5, 1.0]. No retraining, new inference, source modification, checkpoint modification, manuscript modification, artifact overwrite, or Git commit was performed.

The historical repository is used here because the explicit purpose is provenance tracing. Historical results are not substituted for the final Experiment 18 results.

## 1. Final implementation verification

### 1.1 Final vector and class order

The resolved Experiment 18 configuration contains:

    "class_weights": [
      2.5,
      1.0
    ]

Evidence: D:/Skripsi/Experiment_TA/experiment_18/config/resolved_config.json, lines 10--13.

The final class mapping is:

    BINARY_LABEL_MAP = {
        "safe_driving": 0,
        "phone_use": 1,
    }

Evidence: D:/Skripsi/Experiment_TA/experiment_18/src/config.py, lines 99--101.

Therefore the final vector order is:

    [safe_driving, phone_use] = [2.5, 1.0]

### 1.2 Loss implementation

The final Experiment 18 training code resolves the configured value as follows:

    def resolve_class_weights(view, exp_config=None, gamma=1.0):
        if exp_config:
            raw = exp_config['class_weights']
        else:
            per_view_name = 'CLASS_WEIGHTS_FRONT' if view == 'front' else 'CLASS_WEIGHTS_SIDE'
            raw = globals().get(per_view_name, CLASS_WEIGHTS)
        if raw!='balanced': return raw

Evidence: D:/Skripsi/Experiment_TA/experiment_18/src/train.py, lines 20--26.

The final literal [2.5, 1.0] therefore passes through unchanged. The code does contain a balanced branch, but that branch is not used by the resolved final configuration because the resolved value is a numeric list, not the string balanced.

The vector is passed to the loss as:

    criterion=nn.CrossEntropyLoss(
        weight=torch.tensor(weights,dtype=torch.float).to(device),
        label_smoothing=ls
    )

Evidence: D:/Skripsi/Experiment_TA/experiment_18/src/train.py, line 110.

The same shared class-weight configuration is used when the runner trains both views:

    python -m src.train --view front
    python -m src.train --view side

Evidence: D:/Skripsi/Experiment_TA/experiment_18/run_experiment.ps1, training block.

The final checkpoint metadata confirms [2.5, 1.0] for both Front and Side:

- D:/Skripsi/Experiment_TA/experiment_18/results/best_checkpoint_metadata.json, Front resolved_config.class_weights.
- D:/Skripsi/Experiment_TA/experiment_18/results/best_checkpoint_metadata.json, Side resolved_config.class_weights.

### 1.3 Final training counts, stride, and split

The authoritative audit artifact records the post-stride-30 training counts as:

| split | train subjects | stride | safe_driving | phone_use | total |
|---|---:|---:|---:|---:|---:|
| train | 35 | 30 | 176 | 908 | 1084 |

Evidence: D:/Skripsi/Experiment_TA/paper_audit/table_split.csv, row beginning train,35,...,30,176,908,1084.

The final configuration also records FRAME_STRIDE = 30 in D:/Skripsi/Experiment_TA/experiment_18/src/config.py, line 171, and the resolved configuration records frame_stride: 30.

## 2. Historical trace of the vector

### 2.1 First verified occurrence

The first verified occurrence found in the historical Git history is:

| item | evidence |
|---|---|
| First verified commit | 4e1299efe69359e84d32a9441c048a715b60599f |
| Date | 2026-07-08 08:07:08 +0700 |
| Commit message | experiment_8 |
| File | D:/Skripsi/Experiment/src/config.py at that commit |
| Exact setting | CLASS_WEIGHTS = [2.5, 1.0] |
| Exact comment | [v5/Exp8] bobot kelas moderat untuk safe_driving |
| View scope | Shared configuration for the Front and Side training code |

The commit diff shows the preceding configuration used:

    CLASS_WEIGHTS = [5.15, 1.0]      # [v5/Exp7] bobot kelas statis (safe_driving=5.15, phone_use=1.0)

and Experiment 8 changed it to:

    CLASS_WEIGHTS = [2.5, 1.0]      # [v5/Exp8] bobot kelas moderat untuk safe_driving

Evidence: commit diff 4e1299... for src/config.py.

No formula, numeric derivation, validation table, or contemporaneous comparison for the exact value 2.5 appears in that first occurrence or in the commit message.

NO EXPLICIT RATIONALE IN FIRST OCCURRENCE.

### 2.2 Earlier class-weight history

The preceding Experiment 7 commit, ca41e3f207545fe4d534341c71f1d98092171314 (2026-07-08 07:10:42 +0700), introduced a static [5.15, 1.0] setting. Its training code replaced an earlier dynamic balanced-weight calculation:

    w_0 = total_train / (2.0 * count_0) if count_0 > 0 else 1.0
    w_1 = total_train / (2.0 * count_1) if count_1 > 0 else 1.0
    class_weights = torch.tensor([w_0, w_1], dtype=torch.float).to(device)

with a static configuration value:

    class_weights = torch.tensor(CLASS_WEIGHTS, dtype=torch.float).to(device)

Evidence: D:/Skripsi/Experiment/src/train.py and the ca41e3f... commit diff.

The historical Experiment 6 notebook output records the dynamic balanced calculation for a train distribution of 963 safe-driving and 5013 phone-use samples as approximately [3.1028, 0.5961]. This is not [2.5, 1.0].

Thus, the available history shows a transition from dynamic/balanced weights to a static [5.15, 1.0] setting in Experiment 7, followed by a change to static [2.5, 1.0] in Experiment 8. It does not show a documented numeric derivation of the second change.

### 2.3 Historical documentation about motivation

The Experiment 8 notebook describes its broad target as improving recall for the minority safe_driving class in the Side view. It also describes the experiment as using static class weights. The relevant wording is:

> Target utama eksperimen ini adalah meningkatkan Recall pada kelas minoritas (safe_driving) khusus untuk model Side View.

and, in the configuration comparison, the class-weight rationale is written as:

> Fokus pada peningkatan Recall kelas safe_driving (minoritas)

Evidence: D:/Skripsi/Experiment/notebooks/experiment_8.ipynb, markdown and configuration-comparison cells.

However, the comparison cell explicitly shows the [5.15, 1.0] Experiment 7 row, not a validation comparison of candidate values for the exact Experiment 8 vector [2.5, 1.0]. The notebook summary later reports [2.5, 1.0], but does not document how the numeric value 2.5 was selected.

This supports a broad minority-class motivation, but not an exact numeric provenance.

### 2.4 Later configurations and weighting experiments

Later historical configurations retain [2.5, 1.0] as the default or copy it into final-view configurations. This is inheritance of a pre-existing configuration, not a new independent derivation.

The later Experiment 19 weighting work is separate and should not be confused with the origin of [2.5, 1.0]:

- Full balanced weighting is explicitly computed using total / (n_classes * count).
- For the final stride-30 counts 176 and 908, it produces [3.0795, 0.5969].
- Mild weighting uses weight_balanced ** gamma.
- The validation-selected gamma is 0.50, producing approximately [1.7549, 0.7726].
- The exploratory test-best gamma is 0.95, producing approximately [2.9111, 0.6125].

Neither the validation sweep nor the test-informed exploratory sweep contains the exact fixed vector [2.5, 1.0] as a candidate.

Evidence:

- D:/Skripsi/Experiment/experiment_19_notes.md, lines 26--87 and the gamma sections.
- D:/Skripsi/Experiment/results/gamma_selection_exp19_validation.csv.
- D:/Skripsi/Experiment/results/gamma_selection_exp19_summary.json.
- D:/Skripsi/Experiment/src/train.py, lines 75--99.

The historical notes explicitly distinguish validation-selected gamma from the test-best exploratory gamma. That fact belongs to the later gamma sweep; it does not establish that the original 2.5 value was selected from test data.

## 3. Formula check

The following calculations use only the final post-stride training counts safe_driving = 176, phone_use = 908, N = 1084. They are comparison calculations, not provenance evidence.

| method | calculation | result | match [2.5, 1.0]? |
|---|---|---:|---|
| Raw inverse frequency | [1/176, 1/908] | [0.005681818, 0.001101322] | No |
| Inverse frequency normalized to sum 1 | divide raw inverse values by their sum | [0.837638376, 0.162361624] | No |
| Inverse frequency normalized to mean 1 | divide raw inverse values by their mean | [1.675276753, 0.324723247] | No |
| sklearn-style balanced | N / (2*n_c) | [3.079545455, 0.596916300] | No |
| Majority/minority ratio, scaled phone weight to 1 | [908/176, 1] | [5.159090909, 1.0] | No |

The historical source implements the balanced formula as:

    weights_balanced = [total / (n_classes * counts[i]) for i in range(n_classes)]
    weights = [float(w ** class_weight_gamma) for w in weights_balanced]

Evidence: D:/Skripsi/Experiment/src/train.py, lines 91--92.

The final Experiment 18 does not activate this formula because its configured value is the literal numeric list [2.5, 1.0].

Formula conclusion: [2.5, 1.0] is not directly explained by the tested standard frequency-based formulas. Mathematical mismatch rules formulas out; it does not prove a historical selection rationale.

## 4. Historical class-count check

The historical manifest was checked at the recorded stride settings. Because the manifest contains both views, the counts below are shown per view after dividing the paired total equally:

| stride | safe_driving per view | phone_use per view | balanced weight per view | phone/safe ratio |
|---:|---:|---:|---:|---:|
| 1 | 4748 | 24696 | [3.1007, 0.5961] | 5.2013 |
| 5 | 963 | 5013 | [3.1028, 0.5961] | 5.2056 |
| 15 | 333 | 1734 | [3.1036, 0.5960] | 5.2072 |
| 30 | 176 | 908 | [3.0795, 0.5969] | 5.1591 |

None of these recorded distributions yields [2.5, 1.0] under the tested standard formulas. No historical count artifact was found that supplies a documented calculation producing exactly 2.5.

## 5. Controlled validation/tuning assessment

The available historical artifacts do show later class-weight experimentation, but not a controlled validation comparison in which [2.5, 1.0] is a candidate and is selected over alternatives.

The later Experiment 19 gamma sweep changed class weights and evaluated validation results, but its tested numeric vectors were generated from the balanced baseline and gamma values. The exact vector [2.5, 1.0] was not one of those candidates. Some later exploratory gamma selection used test performance, and the notes explicitly label that as test-informed and not final; this does not establish the origin of the original 2.5 value.

Was [2.5, 1.0] chosen through a controlled validation-based comparison?

UNKNOWN / NOT ESTABLISHED. The repository contains no direct comparison record for the exact vector. It is not valid to claim validation selection from the later gamma sweep.

## 6. Front versus Side use

The first verified Experiment 8 configuration uses one shared CLASS_WEIGHTS constant while the training runner selects the view-specific model settings. The same vector is therefore used for both Front and Side in the available Experiment 8/final pipeline evidence.

The final Experiment 18 resolved metadata independently records [2.5, 1.0] for both Front and Side. The vector is a training-loss setting; the final metadata states that class-weight gamma scope is training loss only and not fusion.

## 7. FACT versus historical rationale versus retrospective interpretation

### A. HISTORICAL FACT

1. The final Experiment 18 uses fixed class weights [2.5, 1.0].
2. Class index 0 is safe_driving; class index 1 is phone_use.
3. The vector is passed to CrossEntropyLoss for both views.
4. The final post-stride-30 training counts are 176 safe-driving and 908 phone-use samples.
5. The first verified occurrence of [2.5, 1.0] is the Experiment 8 commit 4e1299... on 2026-07-08.
6. The first-occurrence comment calls it a “moderate” weight for safe_driving.
7. The preceding Experiment 7 configuration used [5.15, 1.0].
8. No exact numeric derivation for 2.5 is stored in the first occurrence.
9. Later balanced/gamma experiments use different numeric vectors and do not establish the origin of 2.5.

### B. HISTORICAL RATIONALE

The strongest contemporaneous rationale available is broad rather than numeric: the Experiment 8 documentation focuses on improving recall for the minority safe_driving class, and the first code comment describes [2.5, 1.0] as a moderate weight for safe_driving.

The repository does not document whether the exact value 2.5 was calculated, manually selected, validation-selected, or copied from an unrecorded comparison.

### C. RETROSPECTIVE INTERPRETATION

The vector gives class 0 a 2.5-times larger loss multiplier than class 1, which is directionally consistent with giving greater penalty to safe-driving errors. The final data are imbalanced toward phone_use, but the vector does not equal the standard inverse-frequency, balanced, or class-ratio values computed from those counts.

This is an interpretation of the implemented effect and data distribution, not proof of the original numerical decision process.

## 8. Evaluation of possible claims

| claim | verdict | evidence-based reason |
|---|---|---|
| 1. [2.5,1.0] was chosen because safe-driving was the minority class. | PARTIALLY SUPPORTED | The Experiment 8 documentation explicitly focuses on minority safe-driving recall, but it does not connect that motivation to a documented derivation of the exact value 2.5. |
| 2. [2.5,1.0] was calculated directly from class proportions. | NOT SUPPORTED | The final counts produce different standard weights, and no formula is recorded for the first [2.5,1.0] occurrence. |
| 3. [2.5,1.0] is an inverse-frequency class weight. | NOT SUPPORTED | Raw, normalized, balanced, and ratio comparisons do not match. |
| 4. [2.5,1.0] was selected through validation experiments. | INCONCLUSIVE | Later validation weighting experiments exist, but the exact vector is not a recorded candidate in those comparisons. |
| 5. [2.5,1.0] was chosen to penalize safe-driving errors more strongly. | PARTIALLY SUPPORTED | The vector demonstrably assigns the larger loss weight to class 0, and the historical notes focus on safe-driving recall; exact selection rationale remains undocumented. |
| 6. [2.5,1.0] was inherited from an earlier experiment. | PARTIALLY SUPPORTED | It was inherited by later configurations, but the first exact occurrence is a change from the earlier [5.15,1.0] setting rather than an inherited exact vector. |
| 7. The exact value 2.5 has a documented numeric derivation. | NOT SUPPORTED | No documented formula or numeric selection record was found. |

## 9. Paper-safe wording

### A. Minimal safe wording

> To account for the class imbalance, the training loss used fixed class weights [2.5, 1.0] in the order [safe driving, phone use], assigning a larger loss contribution to the safe-driving class.

This wording describes the documented configuration and its direct implementation effect. It does not claim that 2.5 came from inverse frequency, balanced weighting, validation tuning, or test tuning.

### B. Stronger wording

No stronger wording about the exact numerical origin is supported by the available artifacts. In particular, the paper should not state that 2.5 was calculated from the final class proportions or selected by a validation sweep.

### C. Wording to avoid

Avoid the following unsupported claims:

- “The weights were calculated using inverse frequency.”
- “The weights are sklearn balanced class weights.”
- “The ratio 2.5:1 follows directly from the class distribution.”
- “The value 2.5 was selected as the best validation setting.”
- “The value 2.5 was selected because it produced the best test result.”
- “The exact value 2.5 is mathematically derived from the final 176/908 counts.”

## 10. Short answer for adviser

Safe-driving merupakan kelas minoritas pada data training, sehingga loss diberi bobot lebih besar untuk kelas tersebut. Konfigurasi final menggunakan fixed class weights [2.5, 1.0] dengan urutan [safe_driving, phone_use], sehingga kesalahan pada safe-driving berkontribusi lebih besar terhadap loss. Namun, angka 2.5 tidak tercatat sebagai hasil perhitungan formula tertentu atau sweep validasi khusus.

## 11. Required final summary

FINAL CLASS WEIGHT:
[2.5, 1.0]

CLASS ORDER:
[safe_driving, phone_use], with safe_driving = 0 and phone_use = 1.

FINAL TRAIN COUNTS:
safe_driving: 176
phone_use: 908

FIRST VERIFIED [2.5,1.0] OCCURRENCE:
Experiment 8, commit 4e1299efe69359e84d32a9441c048a715b60599f, dated 2026-07-08 08:07:08 +0700, in D:/Skripsi/Experiment/src/config.py.

FIRST VERIFIED RATIONALE:
The first-occurrence comment says “bobot kelas moderat untuk safe_driving”; no explicit numeric derivation or selection record is present.

IS 2.5 DIRECTLY DERIVED FROM FINAL CLASS PROPORTION:
NO

IS 2.5 A STANDARD BALANCED WEIGHT:
NO

WAS 2.5 VALIDATION-SELECTED:
UNKNOWN

WAS 2.5 TEST-INFORMED:
UNKNOWN

WAS 2.5 INHERITED:
PARTIAL — inherited by later configurations, but the first exact occurrence is a change from [5.15, 1.0].

DOCUMENTED NUMERIC DERIVATION EXISTS:
NO

MAIN HISTORICAL MOTIVATION:
The available documentation supports a broad minority-safe-driving recall motivation and describes the setting as a moderate static safe-driving weight. It does not establish why the exact numeric value 2.5 was selected.

CLAIM:
“[2.5,1.0] was used to address class imbalance and give greater penalty to safe-driving errors.”

VERDICT:
PARTIALLY SUPPORTED

PAPER-SAFE WORDING:
“To account for the class imbalance, the training loss used fixed class weights [2.5, 1.0] in the order [safe driving, phone use], assigning a larger loss contribution to the safe-driving class.”

SAFE ANSWER TO ADVISER:
Safe-driving adalah kelas minoritas, sehingga diberi bobot loss lebih besar. Konfigurasi finalnya adalah [2.5,1.0] untuk [safe_driving, phone_use]; nilai 2.5 sendiri tidak tercatat sebagai hasil formula atau sweep validasi tertentu.

FACT:
The final implementation, class order, loss usage, final counts, first verified historical occurrence, and later inherited use are established by artifacts.

HISTORICAL RATIONALE:
The available contemporaneous rationale is minority safe-driving recall / a moderate static safe-driving weight. The exact numeric selection reason is not documented.

RETROSPECTIVE INTERPRETATION:
The larger class-0 multiplier is directionally consistent with penalizing safe-driving errors more strongly, but this does not establish the original selection rationale.

UNKNOWN:
Whether 2.5 was manually chosen, selected from an unrecorded validation comparison, informed by an unrecorded experiment, or derived using an undocumented heuristic.

No retraining.
No inference.
No source modification.
No manuscript modification.
No Git commit.
