from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score


ROOT = Path(r"D:\Skripsi\Experiment_TA")
AUDIT = ROOT / "paper_audit"
BOOT_REPS = 10_000
BOOT_SEED = 42


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fmt(x, digits=5):
    if x is None:
        return "—"
    if isinstance(x, (float, np.floating)):
        return f"{float(x):.{digits}f}"
    return str(x)


def history_health(history_path: Path, summary_path: Path):
    rows = load_json(history_path)
    summary = load_json(summary_path)
    df = pd.DataFrame(rows)
    min_loss = df.loc[df["val_loss"].idxmin()]
    max_f1 = df.loc[df["val_macro_f1"].idxmax()]
    last = df.iloc[-1]
    health = {
        "best_epoch": summary.get("best_epoch"),
        "executed_epochs": int(len(df)),
        "checkpoint": summary.get("checkpoint_selection", {}),
        "early_stopping": summary.get("early_stopping", {}),
        "best_epoch_metrics": summary.get("best_epoch_metrics", {}),
        "min_val_loss_epoch": int(min_loss["epoch"]),
        "min_val_loss": float(min_loss["val_loss"]),
        "max_val_macro_f1_epoch": int(max_f1["epoch"]),
        "max_val_macro_f1": float(max_f1["val_macro_f1"]),
        "last_epoch": int(last["epoch"]),
        "last_loss_gap": float(last.get("loss_gap", np.nan)),
        "last_f1_gap": float(last.get("f1_gap", np.nan)),
        "mean_loss_gap": float(df["loss_gap"].mean()) if "loss_gap" in df else None,
        "max_loss_gap": float(df["loss_gap"].max()) if "loss_gap" in df else None,
        "history": df.to_dict(orient="records"),
    }
    return health


def bootstrap_subject_cluster(df: pd.DataFrame, pred_a: str, pred_b: str):
    subjects = list(df["subject_id"].drop_duplicates())
    groups = [df.loc[df["subject_id"] == s] for s in subjects]
    y = df["label"].to_numpy(dtype=int)
    observed = f1_score(y, df[pred_a], average="macro") - f1_score(y, df[pred_b], average="macro")

    def counts(group, pred):
        gy = group["label"].to_numpy(dtype=int)
        gp = group[pred].to_numpy(dtype=int)
        return np.array(
            [
                ((gy == 0) & (gp == 0)).sum(),
                ((gy != 0) & (gp == 0)).sum(),
                ((gy == 0) & (gp != 0)).sum(),
                ((gy == 1) & (gp == 1)).sum(),
                ((gy != 1) & (gp == 1)).sum(),
                ((gy == 1) & (gp != 1)).sum(),
            ],
            dtype=np.int64,
        )

    def macro_f1_from_counts(c):
        f0 = (2.0 * c[:, 0]) / np.maximum(2.0 * c[:, 0] + c[:, 1] + c[:, 2], 1.0)
        f1 = (2.0 * c[:, 3]) / np.maximum(2.0 * c[:, 3] + c[:, 4] + c[:, 5], 1.0)
        return (f0 + f1) / 2.0

    counts_a = np.stack([counts(g, pred_a) for g in groups])
    counts_b = np.stack([counts(g, pred_b) for g in groups])
    rng = np.random.default_rng(BOOT_SEED)
    choices = rng.integers(0, len(groups), size=(BOOT_REPS, len(groups)))
    sampled_a = counts_a[choices].sum(axis=1)
    sampled_b = counts_b[choices].sum(axis=1)
    diffs = macro_f1_from_counts(sampled_a) - macro_f1_from_counts(sampled_b)
    return {
        "comparison": f"{pred_a}_vs_{pred_b}",
        "metric": "macro_f1",
        "method": "subject_cluster_bootstrap_test_subjects",
        "n_clusters": len(subjects),
        "n_boot": BOOT_REPS,
        "confidence_level": 0.95,
        "seed": BOOT_SEED,
        "observed_diff": float(observed),
        "ci95_low": float(np.percentile(diffs, 2.5)),
        "ci95_high": float(np.percentile(diffs, 97.5)),
        "subjects": [str(s) for s in subjects],
    }


def adaptive_diagnostics(pred_path: Path):
    df = pd.read_csv(pred_path)
    front_conf = np.abs(df["front_prob_phone"].to_numpy(dtype=float) - 0.5)
    side_conf = np.abs(df["side_prob_phone"].to_numpy(dtype=float) - 0.5)
    front_exp = np.exp(front_conf)
    side_exp = np.exp(side_conf)
    wf = front_exp / (front_exp + side_exp)
    ws = 1.0 - wf
    delta = df["adaptive_prob_phone"].to_numpy(dtype=float) - df["average_prob_phone"].to_numpy(dtype=float)
    return {
        "weight_front_mean": float(wf.mean()),
        "weight_front_std": float(wf.std()),
        "weight_front_min": float(wf.min()),
        "weight_front_max": float(wf.max()),
        "weight_side_mean": float(ws.mean()),
        "count_weight_front_045_055": int(((wf >= 0.45) & (wf <= 0.55)).sum()),
        "count_weight_front_040_060": int(((wf >= 0.40) & (wf <= 0.60)).sum()),
        "mean_delta_adaptive_minus_average": float(delta.mean()),
        "mean_abs_delta": float(np.abs(delta).mean()),
        "max_abs_delta": float(np.abs(delta).max()),
        "probability_changed_count": int((np.abs(delta) > 1e-12).sum()),
        "hard_decision_changed_count": int(
            (df["adaptive_pred"].to_numpy(dtype=int) != df["average_pred"].to_numpy(dtype=int)).sum()
        ),
    }


def complementarity(df: pd.DataFrame):
    y = df["label"].to_numpy(dtype=int)
    f = df["front_pred"].to_numpy(dtype=int)
    s = df["side_pred"].to_numpy(dtype=int)
    a = df["average_pred"].to_numpy(dtype=int)
    ad = df["adaptive_pred"].to_numpy(dtype=int)
    fc = f == y
    sc = s == y
    out = {
        "support": int(len(df)),
        "both_correct": int((fc & sc).sum()),
        "both_wrong": int((~fc & ~sc).sum()),
        "front_correct_side_wrong": int((fc & ~sc).sum()),
        "front_wrong_side_correct": int((~fc & sc).sum()),
        "average_fixed_front_error": int((~fc & (a == y)).sum()),
        "average_broke_front_correct": int((fc & (a != y)).sum()),
        "adaptive_fixed_front_error": int((~fc & (ad == y)).sum()),
        "adaptive_broke_front_correct": int((fc & (ad != y)).sum()),
    }
    categories = {
        "average_rescued": df.loc[(~fc) & (a == y), ["subject_id", "activity_id", "frame"]].to_dict("records"),
        "average_broken": df.loc[fc & (a != y), ["subject_id", "activity_id", "frame"]].to_dict("records"),
        "adaptive_rescued": df.loc[(~fc) & (ad == y), ["subject_id", "activity_id", "frame"]].to_dict("records"),
        "adaptive_broken": df.loc[fc & (ad != y), ["subject_id", "activity_id", "frame"]].to_dict("records"),
    }
    return out, categories


VARIANTS = {
    "original_experiment_18": {
        "label": "18_original_mixed_reference",
        "root": ROOT / "experiment_18",
        "result": ROOT / "experiment_18" / "results",
        "pred": ROOT / "experiment_18" / "results" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18" / "results" / "fusion" / "fusion_metrics.json",
        "protocol": "Front val_macro_f1/max; Side val_loss/min; early stopping tied to each checkpoint criterion in original implementation.",
        "new": False,
    },
    "checkpoint_only_macro_f1": {
        "label": "18_checkpoint_val_macro_f1",
        "root": ROOT / "experiment_18_standardized_checkpoint_selection",
        "result": ROOT / "experiment_18_standardized_checkpoint_selection" / "results",
        "pred": ROOT / "experiment_18_standardized_checkpoint_selection" / "results" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_standardized_checkpoint_selection" / "results" / "fusion" / "fusion_metrics.json",
        "protocol": "Front/Side checkpoint val_macro_f1/max; Side early stopping remained val_loss/min in this checkpoint-only variant.",
        "new": False,
    },
    "checkpoint_only_val_loss": {
        "label": "18_checkpoint_val_loss",
        "root": ROOT / "experiment_18_standardized_checkpoint_val_loss",
        "result": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss",
        "pred": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss" / "fusion" / "fusion_metrics.json",
        "protocol": "Front/Side checkpoint val_loss/min; Front early stopping remained Macro F1 in this checkpoint-only variant.",
        "new": False,
    },
    "full_standardized_macro_f1": {
        "label": "18_checkpoint_val_macro_f1_and_earlystopping_val_macro",
        "root": ROOT / "experiment_18_full_standardized_macro_f1",
        "result": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1",
        "pred": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1" / "fusion" / "fusion_metrics.json",
        "protocol": "Front/Side checkpoint and early stopping val_macro_f1/max; patience Front=4, Side=5; scheduler unchanged.",
        "new": True,
    },
    "full_standardized_val_loss": {
        "label": "18_checkpoint_val_loss_and_earlystopping_val_loss",
        "root": ROOT / "experiment_18_full_standardized_val_loss",
        "result": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss",
        "pred": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss" / "fusion" / "fusion_metrics.json",
        "protocol": "Front/Side checkpoint and early stopping val_loss/min; patience Front=4, Side=5; scheduler unchanged.",
        "new": True,
    },
}


def locate_variant_health(v):
    health = {}
    for view in ("front", "side"):
        h = v["result"] / view / "history.json"
        s = v["result"] / view / "train_summary.json"
        if h.exists() and s.exists():
            health[view] = history_health(h, s)
    return health


def collect_variant(key, v):
    f = load_json(v["fusion"])
    p = pd.read_csv(v["pred"])
    comp, cats = complementarity(p)
    boot = {}
    for a in ("average_pred", "adaptive_pred"):
        for b in ("front_pred", "side_pred"):
            boot[f"{a}_vs_{b}"] = bootstrap_subject_cluster(p, a, b)
    out = {
        "key": key,
        "label": v["label"],
        "protocol": v["protocol"],
        "health": locate_variant_health(v),
        "fusion_metrics": f,
        "complementarity_recomputed": comp,
        "adaptive_diagnostics": adaptive_diagnostics(v["pred"]),
        "bootstrap": boot,
        "prediction_file": str(v["pred"]),
        "prediction_sha256": sha256(v["pred"]),
        "n_samples": int(len(p)),
        "n_subjects": int(p["subject_id"].nunique()),
        "categories": cats,
    }
    return out


def metric_row(result):
    f = result["fusion_metrics"]
    h = result["health"]
    return {
        "label": result["label"],
        "front_epoch": h.get("front", {}).get("best_epoch"),
        "side_epoch": h.get("side", {}).get("best_epoch"),
        "front_test_f1": f.get("single_front", {}).get("f1_macro"),
        "side_test_f1": f.get("single_side", {}).get("f1_macro"),
        "average_fusion_f1": f.get("average_fusion", {}).get("f1_macro"),
        "adaptive_fusion_f1": f.get("adaptive_fusion", {}).get("f1_macro"),
        "average_fusion_acc": f.get("average_fusion", {}).get("accuracy"),
        "adaptive_fusion_acc": f.get("adaptive_fusion", {}).get("accuracy"),
        "bootstrap_avg_vs_front": result["bootstrap"]["average_pred_vs_front_pred"],
        "bootstrap_avg_vs_side": result["bootstrap"]["average_pred_vs_side_pred"],
    }


def write_variant_report(result):
    key = result["key"]
    v = VARIANTS[key]
    out_path = v["root"] / "results" / (
        "full_standardized_macro_f1_summary.md" if key == "full_standardized_macro_f1" else "full_standardized_val_loss_summary.md"
    )
    h = result["health"]
    f = result["fusion_metrics"]
    ad = result["adaptive_diagnostics"]
    lines = [
        f"# {result['label']}",
        "",
        "## Protocol and execution status",
        "",
        f"- Protocol: {result['protocol']}",
        f"- Completed full run: YES; training, train/val/test evaluation, fusion, and summary were executed.",
        f"- Test prediction rows: {result['n_samples']}; test subjects: {result['n_subjects']}.",
        f"- Prediction CSV SHA-256: `{result['prediction_sha256']}`.",
        "- The original `experiment_18` directory and `Paper_TA` were not modified by this run.",
        "",
        "## Training health",
        "",
        "| view | selected epoch | executed epochs | checkpoint | early stopping | min val loss epoch | max val Macro F1 epoch | selected val loss | selected val Macro F1 | final loss gap | max loss gap |",
        "|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for view in ("front", "side"):
        x = h[view]
        bm = x["best_epoch_metrics"]
        lines.append(
            f"| {view} | {x['best_epoch']} | {x['executed_epochs']} | "
            f"{x['checkpoint'].get('monitored_metric')}/{x['checkpoint'].get('mode')} | "
            f"{x['early_stopping'].get('monitored_metric')}/{x['early_stopping'].get('mode')}, "
            f"patience {x['early_stopping'].get('patience')} | {x['min_val_loss_epoch']} | "
            f"{x['max_val_macro_f1_epoch']} | {fmt(bm.get('val_loss'))} | {fmt(bm.get('val_macro_f1'))} | "
            f"{fmt(x['last_loss_gap'])} | {fmt(x['max_loss_gap'])} |"
        )
    lines += [
        "",
        "Per-epoch histories remain in the run namespace: `results/<namespace>/front/history.json` and `side/history.json`.",
        "The selected checkpoint is the physical `best.pt` written by the corresponding training process; its SHA-256 is recorded in `train_summary.json`.",
        "",
        "## Test metrics",
        "",
        "| model | accuracy | Macro Precision | Macro Recall | Macro F1 | ROC-AUC | PR-AUC | ECE | Brier |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, label in (("single_front", "Front"), ("single_side", "Side"), ("average_fusion", "Average fusion"), ("adaptive_fusion", "Adaptive fusion")):
        m = f[name]
        lines.append(
            f"| {label} | {fmt(m.get('accuracy'))} | {fmt(m.get('precision_macro'))} | {fmt(m.get('recall_macro'))} | "
            f"{fmt(m.get('f1_macro'))} | {fmt(m.get('roc_auc'))} | {fmt(m.get('pr_auc'))} | {fmt(m.get('ece_binary'))} | {fmt(m.get('brier_score'))} |"
        )
    lines += [
        "",
        "## Complementarity and adaptive diagnostics",
        "",
        f"- Both correct: {result['complementarity_recomputed']['both_correct']}; both wrong: {result['complementarity_recomputed']['both_wrong']}; Front-correct/Side-wrong: {result['complementarity_recomputed']['front_correct_side_wrong']}; Front-wrong/Side-correct: {result['complementarity_recomputed']['front_wrong_side_correct']}.",
        f"- Average fusion rescued Front errors: {result['complementarity_recomputed']['average_fixed_front_error']}; broke Front-correct cases: {result['complementarity_recomputed']['average_broke_front_correct']}.",
        f"- Adaptive fusion rescued Front errors: {result['complementarity_recomputed']['adaptive_fixed_front_error']}; broke Front-correct cases: {result['complementarity_recomputed']['adaptive_broke_front_correct']}.",
        f"- Mean Front adaptive weight: {fmt(ad['weight_front_mean'])}; SD: {fmt(ad['weight_front_std'])}; range: [{fmt(ad['weight_front_min'])}, {fmt(ad['weight_front_max'])}].",
        f"- Front weight in [0.45, 0.55]: {ad['count_weight_front_045_055']}; in [0.40, 0.60]: {ad['count_weight_front_040_060']}.",
        f"- Mean adaptive-minus-average probability: {fmt(ad['mean_delta_adaptive_minus_average'])}; mean absolute difference: {fmt(ad['mean_abs_delta'])}; hard decisions changed: {ad['hard_decision_changed_count']}.",
        "",
        "## Subject-cluster bootstrap",
        "",
        f"The audit uses the documented test-subject cluster protocol: {result['n_subjects']} subjects, {BOOT_REPS:,} resamples, percentile 95% CI. The post-run audit seed is {BOOT_SEED}; this is analysis of stored predictions and is not a new model inference.",
        "",
        "| comparison | observed Macro-F1 difference | 95% CI |",
        "|---|---:|---:|",
    ]
    for k in ("average_pred_vs_front_pred", "average_pred_vs_side_pred", "adaptive_pred_vs_front_pred", "adaptive_pred_vs_side_pred"):
        b = result["bootstrap"][k]
        lines.append(f"| {k} | {fmt(b['observed_diff'])} | [{fmt(b['ci95_low'])}, {fmt(b['ci95_high'])}] |")
    lines += [
        "",
        "## FACT / OBSERVED DIFFERENCE / INTERPRETATION / LIMITATION",
        "",
        "### FACT",
        "",
        "- The two views were retrained under the stated full protocol; checkpoint and early-stopping monitors are explicit and recorded separately in the resolved configuration and training summaries.",
        "- All reported test metrics above are read from stored evaluation/fusion artifacts generated by this run.",
        "- Adaptive fusion is a deterministic post-processing operation over stored Front/Side probabilities; no additional model training was performed for it.",
        "",
        "### OBSERVED DIFFERENCE",
        "",
        "- The selected epoch, validation trajectory, single-view test metrics, fusion metrics, complementarity counts, and bootstrap intervals are the values in this run and are not claims about an unrun counterfactual.",
        "",
        "### INTERPRETATION",
        "",
        "- Any comparison across protocols is an observed comparison of independently run artifacts with the same locked non-selection configuration. It does not establish that one criterion is universally superior.",
        "",
        "### LIMITATION",
        "",
        "- The experiment uses one configured training seed and deterministic split seed 42, while the environment metadata records cuDNN deterministic mode as false. The bootstrap quantifies test-subject resampling uncertainty, not training-seed uncertainty.",
        "- A separate audit script is used because the original repository does not expose the bootstrap implementation as a reusable source module; the method, cluster count, repetition count, confidence level, and seed are recorded here.",
        "",
        "## Artifact pointers",
        "",
        "- `config/resolved_config.json`",
        "- `results/<namespace>/front/train_summary.json` and `side/train_summary.json`",
        "- `results/<namespace>/front/history.json` and `side/history.json`",
        "- `results/<namespace>/fusion/fusion_metrics.json`",
        "- `results/<namespace>/predictions/fusion_test_predictions.csv`",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def write_config_diff(key, result):
    v = VARIANTS[key]
    cfg = load_json(v["root"] / "config" / "resolved_config.json")
    namespace = v["result"].name
    p = v["root"] / "results" / "config_diff_vs_experiment_18.md"
    lines = [
        f"# Configuration diff — {cfg['experiment']} vs `experiment_18`",
        "",
        "## Status",
        "",
        "- Pre-run gate: PASS.",
        "- Run status: COMPLETED; both views trained, evaluated, fused, and summarized.",
        "- Output namespace: `" + namespace + "`.",
        "",
        "## Intended controlled change",
        "",
        "| field | experiment_18 effective protocol | controlled variant |",
        "|---|---|---|",
    ]
    if key == "full_standardized_macro_f1":
        lines += [
            "| Front checkpoint | `val_macro_f1/max` | `val_macro_f1/max` |",
            "| Side checkpoint | `val_loss/min` | `val_macro_f1/max` |",
            "| Front early stopping | `val_macro_f1/max`, patience 4 | `val_macro_f1/max`, patience 4 |",
            "| Side early stopping | `val_loss/min`, patience 5 | `val_macro_f1/max`, patience 5 |",
        ]
    else:
        lines += [
            "| Front checkpoint | `val_macro_f1/max` | `val_loss/min` |",
            "| Side checkpoint | `val_loss/min` | `val_loss/min` |",
            "| Front early stopping | `val_macro_f1/max`, patience 4 | `val_loss/min`, patience 4 |",
            "| Side early stopping | `val_loss/min`, patience 5 | `val_loss/min`, patience 5 |",
        ]
    lines += [
        "| Scheduler | unchanged; effective patience Front=1, Side=2; monitor `val_macro_f1/max` | unchanged |",
        "| All other hyperparameters/data/split/augmentation | locked | locked |",
        "",
        "## Verification after run",
        "",
        f"- Front selected epoch: {result['health']['front']['best_epoch']}; Side selected epoch: {result['health']['side']['best_epoch']}.",
        f"- Front checkpoint SHA-256: `{load_json(v['result'] / 'front' / 'train_summary.json')['checkpoint_sha256']}`.",
        f"- Side checkpoint SHA-256: `{load_json(v['result'] / 'side' / 'train_summary.json')['checkpoint_sha256']}`.",
        "- No output is written to the original `experiment_18` namespace by this controlled variant.",
        "",
        "## Metadata note",
        "",
        "- The baseline root `experiment_18/config/resolved_config.json` records Side scheduler patience as 1, while the baseline source/per-view training metadata records the effective Side value as 2. This variant preserves the effective source behavior (Side=2) and does not treat the stale root metadata value as a protocol change.",
    ]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def write_master(results):
    p = AUDIT / "model_selection_protocol_comparison.md"
    lines = [
        "# Model-selection protocol comparison",
        "",
        "Scope: authoritative repository `D:\\Skripsi\\Experiment_TA` only. No historical repository or manuscript edits were used.",
        "",
        "## Protocols compared",
        "",
        "1. Original mixed `experiment_18`.",
        "2. Existing checkpoint-only Macro-F1 variant.",
        "3. Existing checkpoint-only validation-loss variant.",
        "4. New full standardized Macro-F1 variant.",
        "5. New full standardized validation-loss variant.",
        "",
        "The two new variants were fully run: Front and Side training, train/validation/test evaluation, fusion, and summary. The earlier two variants are compared only from their existing stored artifacts.",
        "",
        "## Protocol and selected checkpoint table",
        "",
        "| protocol | Front criterion | Side criterion | Front epoch | Side epoch | Front test Macro F1 | Side test Macro F1 | Average fusion Macro F1 | Adaptive fusion Macro F1 |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key in VARIANTS:
        r = results[key]
        h = r["health"]
        f = r["fusion_metrics"]
        fc = h.get("front", {}).get("checkpoint", {})
        sc = h.get("side", {}).get("checkpoint", {})
        lines.append(
            f"| {r['label']} | {fc.get('monitored_metric','—')}/{fc.get('mode','—')} | {sc.get('monitored_metric','—')}/{sc.get('mode','—')} | "
            f"{h.get('front',{}).get('best_epoch','—')} | {h.get('side',{}).get('best_epoch','—')} | "
            f"{fmt(f.get('single_front',{}).get('f1_macro'))} | {fmt(f.get('single_side',{}).get('f1_macro'))} | "
            f"{fmt(f.get('average_fusion',{}).get('f1_macro'))} | {fmt(f.get('adaptive_fusion',{}).get('f1_macro'))} |"
        )
    lines += [
        "",
        "## Training-health observations for the new variants",
        "",
        "| variant | view | executed epochs | selected epoch | min-loss epoch | max-F1 epoch | selected val loss | selected val Macro F1 | final loss gap |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for key in ("full_standardized_macro_f1", "full_standardized_val_loss"):
        r = results[key]
        for view in ("front", "side"):
            x = r["health"][view]
            bm = x["best_epoch_metrics"]
            lines.append(
                f"| {r['label']} | {view} | {x['executed_epochs']} | {x['best_epoch']} | {x['min_val_loss_epoch']} | {x['max_val_macro_f1_epoch']} | {fmt(bm.get('val_loss'))} | {fmt(bm.get('val_macro_f1'))} | {fmt(x['last_loss_gap'])} |"
            )
    lines += [
        "",
        "## Fusion, complementarity, adaptive diagnostics, and bootstrap",
        "",
        "Each variant's detailed summary contains ROC-AUC, PR-AUC, ECE, Brier, per-class results, confusion matrices, complementarity counts, adaptive-weight diagnostics, and subject-cluster bootstrap intervals. The stored prediction CSVs are the common evidence layer for the post-run comparisons.",
        "",
        "| protocol | avg-vs-Front observed ΔF1 [95% CI] | avg-vs-Side observed ΔF1 [95% CI] | Front weight mean | avg rescue/break |",
        "|---|---:|---:|---:|---:|",
    ]
    for key in VARIANTS:
        r = results[key]
        b1 = r["bootstrap"]["average_pred_vs_front_pred"]
        b2 = r["bootstrap"]["average_pred_vs_side_pred"]
        ad = r["adaptive_diagnostics"]
        c = r["complementarity_recomputed"]
        lines.append(
            f"| {r['label']} | {fmt(b1['observed_diff'])} [{fmt(b1['ci95_low'])}, {fmt(b1['ci95_high'])}] | {fmt(b2['observed_diff'])} [{fmt(b2['ci95_low'])}, {fmt(b2['ci95_high'])}] | {fmt(ad['weight_front_mean'])} | {c['average_fixed_front_error']}/{c['average_broke_front_correct']} |"
        )
    lines += [
        "",
        "## FACT",
        "",
        "- The new full Macro-F1 variant has both views using checkpoint and early-stopping `val_macro_f1/max`.",
        "- The new full validation-loss variant has both views using checkpoint and early-stopping `val_loss/min`.",
        "- Scheduler monitor/logic was kept as `val_macro_f1/max`; it is not part of the controlled selection-criterion change.",
        "- Both new variants have physical checkpoints, per-epoch histories, evaluation outputs, fusion outputs, and SHA-256 records.",
        "",
        "## OBSERVED DIFFERENCE",
        "",
        "- The tables show what changed in these stored runs. A result difference is not by itself evidence that a criterion is generally better or that the criterion was selected because of test performance.",
        "",
        "## INTERPRETATION",
        "",
        "- Full standardization changes early stopping as well as checkpoint selection relative to the original mixed protocol. Therefore the new full variants are distinct training trajectories, not mere relabeling of old checkpoints.",
        "- The checkpoint-only variants are not interchangeable with the new full variants because their early-stopping protocols were not simultaneously standardized.",
        "",
        "## LIMITATION",
        "",
        "- One configured training seed was used for each new variant; cuDNN deterministic mode was false in the recorded environment.",
        "- Subject-cluster bootstrap uses 7 test subjects, 10,000 repetitions, percentile 95% CI, and analysis seed 42. It measures resampling uncertainty, not training-seed uncertainty.",
        "- This comparison does not use the test set as a model-selection signal.",
        "",
        "## Detailed reports",
        "",
        "- [Full standardized Macro F1 summary](../experiment_18_full_standardized_macro_f1/results/full_standardized_macro_f1_summary.md)",
        "- [Full standardized validation-loss summary](../experiment_18_full_standardized_val_loss/results/full_standardized_val_loss_summary.md)",
    ]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def main():
    results = {key: collect_variant(key, v) for key, v in VARIANTS.items()}
    for key in ("full_standardized_macro_f1", "full_standardized_val_loss"):
        write_variant_report(results[key])
        write_config_diff(key, results[key])
        # Keep detailed post-run audit data alongside each new variant.
        out = VARIANTS[key]["result"] / "postrun_standardization_audit.json"
        out.write_text(json.dumps(results[key], indent=2, default=str) + "\n", encoding="utf-8")
    write_master(results)
    compact = {key: metric_row(results[key]) for key in results}
    (AUDIT / "model_selection_protocol_comparison.json").write_text(json.dumps(compact, indent=2, default=str) + "\n", encoding="utf-8")
    print("REPORTS_WRITTEN")


if __name__ == "__main__":
    main()
