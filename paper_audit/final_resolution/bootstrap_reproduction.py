from pathlib import Path
import hashlib
import itertools
import json
import numpy as np
import pandas as pd

ROOT = Path(r"D:\Skripsi\Experiment_TA")
PRED = ROOT / "experiment_18" / "results" / "predictions" / "fusion_test_predictions.csv"
OUT = ROOT / "paper_audit" / "final_resolution"
OUT.mkdir(parents=True, exist_ok=True)

REPS = 10_000
SEED = 42


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def counts(group, pred):
    y = group["label"].to_numpy(dtype=int)
    p = group[pred].to_numpy(dtype=int)
    return np.array([
        np.sum((y == 0) & (p == 0)),
        np.sum((y == 0) & (p == 1)),
        np.sum((y == 1) & (p == 0)),
        np.sum((y == 1) & (p == 1)),
    ], dtype=float)


def macro_f1_from_counts(c):
    c = np.asarray(c, dtype=float)
    tn, fp, fn, tp = c[..., 0], c[..., 1], c[..., 2], c[..., 3]
    f0 = 2 * tn / np.maximum(2 * tn + fp + fn, 1)
    f1 = 2 * tp / np.maximum(2 * tp + fn + fp, 1)
    return (f0 + f1) / 2


def run(df, pred_a, pred_b, order_name, rng_name, draw_name):
    subjects = list(df["subject_id"].drop_duplicates())
    if order_name == "sorted":
        subjects = sorted(subjects)
    groups = [df.loc[df["subject_id"] == s] for s in subjects]
    observed = float(macro_f1_from_counts(counts(df, pred_a)) - macro_f1_from_counts(counts(df, pred_b)))
    ca = np.stack([counts(g, pred_a) for g in groups])
    cb = np.stack([counts(g, pred_b) for g in groups])
    if rng_name == "default_rng":
        rng = np.random.default_rng(SEED)
        if draw_name == "integers":
            choices = rng.integers(0, len(groups), size=(REPS, len(groups)))
        else:
            choices = rng.choice(len(groups), size=(REPS, len(groups)), replace=True)
    else:
        rng = np.random.RandomState(SEED)
        if draw_name == "randint":
            choices = rng.randint(0, len(groups), size=(REPS, len(groups)))
        else:
            choices = rng.choice(len(groups), size=(REPS, len(groups)), replace=True)
    diffs = macro_f1_from_counts(ca[choices].sum(axis=1)) - macro_f1_from_counts(cb[choices].sum(axis=1))
    return {
        "order": order_name,
        "rng": rng_name,
        "draw": draw_name,
        "observed_diff": observed,
        "ci95_low": float(np.percentile(diffs, 2.5)),
        "ci95_high": float(np.percentile(diffs, 97.5)),
        "n_clusters": len(subjects),
        "subjects": [int(s) for s in subjects],
    }


df = pd.read_csv(PRED)
results = []
for order in ("first_appearance", "sorted"):
    for rng, draw in (("default_rng", "integers"), ("default_rng", "choice"), ("RandomState", "randint"), ("RandomState", "choice")):
        for a, b, label in (("average_pred", "front_pred", "average_vs_front"), ("average_pred", "side_pred", "average_vs_side")):
            item = run(df, a, b, order, rng, draw)
            item["comparison"] = label
            results.append(item)

report = {
    "prediction_path": str(PRED),
    "prediction_sha256": sha256(PRED),
    "rows": int(len(df)),
    "unique_samples": int(df[["subject_id", "activity_id", "frame"]].drop_duplicates().shape[0]),
    "subjects_in_file_order": [int(s) for s in df["subject_id"].drop_duplicates()],
    "subject_row_counts": {str(int(s)): int(n) for s, n in df.groupby("subject_id", sort=False).size().items()},
    "repetitions": REPS,
    "seed": SEED,
    "numpy_version": np.__version__,
    "results": results,
    "target_manuscript": {
        "average_vs_front": [-0.03467, 0.14186],
        "average_vs_side": [0.09749, 0.19156],
    },
    "target_deep_audit": {
        "average_vs_front": [-0.032702300061770995, 0.13884389171745493],
        "average_vs_side": [0.09800745235314207, 0.19126612106447805],
    },
}
(OUT / "bootstrap_reproduction.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# Search only the possible subject-order effect under the stored deep-audit
# generator. This is a provenance diagnostic, not a replacement result.
subjects = list(df["subject_id"].drop_duplicates())
base_groups = [df.loc[df["subject_id"] == s] for s in subjects]
ca = np.stack([counts(g, "average_pred") for g in base_groups])
cf = np.stack([counts(g, "front_pred") for g in base_groups])
cs = np.stack([counts(g, "side_pred") for g in base_groups])
choices = np.random.default_rng(SEED).integers(0, len(subjects), size=(REPS, len(subjects)))
targets = {"average_vs_front": (-0.03467, 0.14186), "average_vs_side": (0.09749, 0.19156)}
order_matches = []
for perm in itertools.permutations(range(len(subjects))):
    pa = ca[list(perm)][choices].sum(axis=1)
    pf = cf[list(perm)][choices].sum(axis=1)
    ps = cs[list(perm)][choices].sum(axis=1)
    front_diff = macro_f1_from_counts(pa) - macro_f1_from_counts(pf)
    side_diff = macro_f1_from_counts(pa) - macro_f1_from_counts(ps)
    front_ci = (float(np.percentile(front_diff, 2.5)), float(np.percentile(front_diff, 97.5)))
    side_ci = (float(np.percentile(side_diff, 2.5)), float(np.percentile(side_diff, 97.5)))
    if (round(front_ci[0], 5), round(front_ci[1], 5)) == targets["average_vs_front"] or (round(side_ci[0], 5), round(side_ci[1], 5)) == targets["average_vs_side"]:
        order_matches.append({"subject_order": [int(subjects[i]) for i in perm], "average_vs_front": front_ci, "average_vs_side": side_ci})
(OUT / "bootstrap_order_search.json").write_text(json.dumps({"matches": order_matches, "tested_permutations": 5040, "generator": "default_rng(42).integers", "target_rounded": targets}, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
