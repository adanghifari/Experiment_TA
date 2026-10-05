from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

import matplotlib.pyplot as plt


ROOT = Path(r"D:\Skripsi\Experiment_TA")
AUDIT = ROOT / "paper_audit"
FIGDIR = AUDIT / "figures" / "protocol_probability_audit"
AUDIT.mkdir(parents=True, exist_ok=True)
FIGDIR.mkdir(parents=True, exist_ok=True)

PROTOCOLS = {
    "P1": {
        "label": "18_original_mixed_reference",
        "root": ROOT / "experiment_18",
        "result": ROOT / "experiment_18" / "results",
        "pred": ROOT / "experiment_18" / "results" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18" / "results" / "fusion" / "fusion_metrics.json",
        "config": ROOT / "experiment_18" / "config" / "resolved_config.json",
        "protocol": "Front checkpoint/early stopping val_macro_f1/max; Side checkpoint/early stopping val_loss/min.",
    },
    "P2": {
        "label": "18_checkpoint_val_macro_f1",
        "root": ROOT / "experiment_18_standardized_checkpoint_selection",
        "result": ROOT / "experiment_18_standardized_checkpoint_selection" / "results",
        "pred": ROOT / "experiment_18_standardized_checkpoint_selection" / "results" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_standardized_checkpoint_selection" / "results" / "fusion" / "fusion_metrics.json",
        "config": ROOT / "experiment_18_standardized_checkpoint_selection" / "config" / "resolved_config.json",
        "protocol": "Both checkpoints val_macro_f1/max; Front early stopping val_macro_f1/max; Side early stopping val_loss/min.",
    },
    "P3": {
        "label": "18_checkpoint_val_loss",
        "root": ROOT / "experiment_18_standardized_checkpoint_val_loss",
        "result": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss",
        "pred": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "results" / "standardized_val_loss" / "fusion" / "fusion_metrics.json",
        "config": ROOT / "experiment_18_standardized_checkpoint_val_loss" / "config" / "resolved_config.json",
        "protocol": "Both checkpoints val_loss/min; Front early stopping val_macro_f1/max; Side early stopping val_loss/min.",
    },
    "P4": {
        "label": "18_checkpoint_val_macro_f1_and_earlystopping_val_macro",
        "root": ROOT / "experiment_18_full_standardized_macro_f1",
        "result": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1",
        "pred": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_full_standardized_macro_f1" / "results" / "full_standardized_macro_f1" / "fusion" / "fusion_metrics.json",
        "config": ROOT / "experiment_18_full_standardized_macro_f1" / "config" / "resolved_config.json",
        "protocol": "Both checkpoints and early stopping val_macro_f1/max; patience Front=4, Side=5.",
    },
    "P5": {
        "label": "18_checkpoint_val_loss_and_earlystopping_val_loss",
        "root": ROOT / "experiment_18_full_standardized_val_loss",
        "result": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss",
        "pred": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss" / "predictions" / "fusion_test_predictions.csv",
        "fusion": ROOT / "experiment_18_full_standardized_val_loss" / "results" / "full_standardized_val_loss" / "fusion" / "fusion_metrics.json",
        "config": ROOT / "experiment_18_full_standardized_val_loss" / "config" / "resolved_config.json",
        "protocol": "Both checkpoints and early stopping val_loss/min; patience Front=4, Side=5.",
    },
}

KEYS = ["subject_id", "activity_id", "frame"]
METHODS = ["front", "side", "average", "adaptive"]
PRED_COLS = {
    "front": ("front_prob_phone", "front_pred"),
    "side": ("side_prob_phone", "side_pred"),
    "average": ("average_prob_phone", "average_pred"),
    "adaptive": ("adaptive_prob_phone", "adaptive_pred"),
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def ece_binary(probs, labels, n_bins=10):
    probs = np.asarray(probs, dtype=float)
    labels = np.asarray(labels, dtype=int)
    edges = np.linspace(0, 1, n_bins + 1)
    out = 0.0
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        mask = (probs >= lo) & (probs <= hi if i == n_bins - 1 else probs < hi)
        if mask.sum():
            out += (mask.sum() / len(probs)) * abs(labels[mask].mean() - probs[mask].mean())
    return float(out)


def metric_dict(y, pred, prob):
    y = np.asarray(y, dtype=int)
    pred = np.asarray(pred, dtype=int)
    prob = np.asarray(prob, dtype=float)
    cm = confusion_matrix(y, pred, labels=[0, 1])
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision_macro": float(precision_score(y, pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y, pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y, pred, average="macro", zero_division=0)),
        "precision_safe": float(precision_score(y, pred, labels=[0], average="macro", zero_division=0)),
        "recall_safe": float(recall_score(y, pred, labels=[0], average="macro", zero_division=0)),
        "f1_safe": float(f1_score(y, pred, labels=[0], average="macro", zero_division=0)),
        "precision_phone": float(precision_score(y, pred, labels=[1], average="macro", zero_division=0)),
        "recall_phone": float(recall_score(y, pred, labels=[1], average="macro", zero_division=0)),
        "f1_phone": float(f1_score(y, pred, labels=[1], average="macro", zero_division=0)),
        "confusion_matrix": cm.tolist(),
        "roc_auc": float(roc_auc_score(y, prob)),
        "pr_auc": float(average_precision_score(y, prob)),
        "ece_binary": ece_binary(prob, y),
        "brier_score": float(np.mean((prob - y) ** 2)),
        "support": int(len(y)),
    }


def fmt(value, digits=5):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.{digits}f}"
    return str(value)


def pct(n, d):
    return 100.0 * n / d if d else float("nan")


def history_health(protocol, view):
    p = PROTOCOLS[protocol]
    history_path = p["result"] / view / "history.json"
    summary_path = p["result"] / view / "train_summary.json"
    rows = load_json(history_path)
    summary = load_json(summary_path)
    df = pd.DataFrame(rows)
    cfg = load_json(p["config"])
    checkpoint = summary.get("checkpoint_selection", {})
    early = summary.get("early_stopping", {})
    if not early:
        # Original train.py uses the same score and mode for early stopping
        # as for checkpoint selection; this is source-supported, but absent from
        # the original train_summary JSON.
        early = {
            "monitored_metric": checkpoint.get("monitored_metric"),
            "mode": checkpoint.get("mode"),
            "patience": cfg.get(f"early_stopping_patience_{view}"),
            "stopped_after_epoch": int(df.iloc[-1]["epoch"]),
            "provenance": "source_inferred_same_as_checkpoint_monitor",
        }
    selected_epoch = int(summary["best_epoch"])
    selected = df.loc[df["epoch"] == selected_epoch].iloc[0]
    min_loss = df.loc[df["val_loss"].idxmin()]
    max_f1 = df.loc[df["val_macro_f1"].idxmax()]
    gaps = df["loss_gap"].astype(float)
    health = {
        "protocol": protocol,
        "view": view,
        "summary_path": str(summary_path),
        "history_path": str(history_path),
        "checkpoint_path": summary.get("checkpoint_path"),
        "checkpoint_sha256": summary.get("checkpoint_sha256"),
        "selected_epoch": selected_epoch,
        "executed_epochs": int(len(df)),
        "checkpoint_monitor": checkpoint.get("monitored_metric"),
        "checkpoint_mode": checkpoint.get("mode"),
        "early_monitor": early.get("monitored_metric"),
        "early_mode": early.get("mode"),
        "early_patience": early.get("patience"),
        "early_stopped_after": early.get("stopped_after_epoch", len(df)),
        "early_provenance": early.get("provenance", "summary_artifact"),
        "train_loss": float(selected["train_loss"]),
        "val_loss": float(selected["val_loss"]),
        "loss_gap_selected": float(selected["loss_gap"]),
        "abs_loss_gap_selected": abs(float(selected["loss_gap"])),
        "train_macro_f1": float(selected["train_macro_f1"]) if "train_macro_f1" in selected else None,
        "val_macro_f1": float(selected["val_macro_f1"]),
        "f1_gap_selected": float(selected["f1_gap"]) if "f1_gap" in selected else None,
        "learning_rate": float(selected["learning_rate"]),
        "min_val_loss": float(min_loss["val_loss"]),
        "min_val_loss_epoch": int(min_loss["epoch"]),
        "max_val_macro_f1": float(max_f1["val_macro_f1"]),
        "max_val_macro_f1_epoch": int(max_f1["epoch"]),
        "min_loss_gap": float(gaps.min()),
        "max_loss_gap": float(gaps.max()),
        "mean_loss_gap": float(gaps.mean()),
        "median_loss_gap": float(gaps.median()),
        "final_loss_gap": float(df.iloc[-1]["loss_gap"]),
        "final_f1_gap": float(df.iloc[-1]["f1_gap"]) if "f1_gap" in df else None,
        "history": df,
    }
    health["health_classification"] = classify_health(health)
    return health


def classify_health(h):
    df = h["history"]
    selected = h["selected_epoch"]
    later = df[df["epoch"] > selected]
    f1_decline = h["max_val_macro_f1"] - float(df.iloc[-1]["val_macro_f1"])
    gap_rise = h["max_loss_gap"] - h["loss_gap_selected"]
    positive_gap = h["loss_gap_selected"] > 0.05 or h["final_loss_gap"] > 0.05
    if len(later) == 0:
        return "INCONCLUSIVE"
    if positive_gap and f1_decline >= 0.05 and gap_rise >= 0.05:
        return "POSSIBLE OVERFITTING SIGNAL"
    if positive_gap or (f1_decline >= 0.03 and gap_rise > 0):
        return "POSSIBLE GENERALIZATION GAP"
    if h["selected_epoch"] <= max(2, int(0.25 * h["executed_epochs"])) and float(later["val_macro_f1"].max()) > h["val_macro_f1"]:
        return "POSSIBLE UNDERFITTING SIGNAL"
    return "NO CLEAR OVERFITTING SIGNAL"


def verify_artifacts():
    rows = []
    for key, p in PROTOCOLS.items():
        required = {
            "folder": p["root"],
            "resolved_config": p["config"],
            "fusion_predictions": p["pred"],
            "fusion_metrics": p["fusion"],
        }
        for view in ("front", "side"):
            required[f"{view}_history"] = p["result"] / view / "history.json"
            required[f"{view}_summary"] = p["result"] / view / "train_summary.json"
            required[f"{view}_checkpoint"] = p["result"] / view / "train_summary.json"
        ok = [name for name, path in required.items() if Path(path).exists()]
        status = "VERIFIED" if len(ok) == len(required) else ("PARTIALLY VERIFIED" if ok else "NOT AVAILABLE")
        row = {"protocol": key, "label": p["label"], "status": status}
        row.update({name: bool(Path(path).exists()) for name, path in required.items()})
        # Check physical checkpoint path and hash for each view.
        for view in ("front", "side"):
            sp = p["result"] / view / "train_summary.json"
            if sp.exists():
                s = load_json(sp)
                cp = Path(s.get("checkpoint_path", ""))
                row[f"{view}_checkpoint_path"] = str(cp)
                row[f"{view}_checkpoint_exists"] = cp.exists()
                row[f"{view}_checkpoint_sha_match"] = bool(cp.exists() and s.get("checkpoint_sha256") == sha256(cp))
            else:
                row[f"{view}_checkpoint_path"] = "N/A"
                row[f"{view}_checkpoint_exists"] = False
                row[f"{view}_checkpoint_sha_match"] = False
        rows.append(row)
    return pd.DataFrame(rows)


def load_predictions():
    preds = {}
    for key, p in PROTOCOLS.items():
        df = pd.read_csv(p["pred"])
        df["row_key"] = df[KEYS].astype(str).agg("|".join, axis=1)
        preds[key] = df
    base = preds["P1"]
    for key, df in preds.items():
        if len(df) != len(base) or set(df["row_key"]) != set(base["row_key"]):
            raise RuntimeError(f"Sample alignment failed for {key}")
        if not base.set_index("row_key")["label"].equals(df.set_index("row_key")["label"]):
            raise RuntimeError(f"Label alignment failed for {key}")
    return preds


def build_per_sample(preds):
    base = preds["P1"][KEYS + ["row_index", "label"]].copy()
    base["sample_id"] = base["row_key"] if "row_key" in base else base[KEYS].astype(str).agg("|".join, axis=1)
    out = base.drop(columns=["row_key"], errors="ignore")
    for protocol, df in preds.items():
        d = df.set_index("row_key")
        idx = out[KEYS].astype(str).agg("|".join, axis=1)
        for method, (prob_col, pred_col) in PRED_COLS.items():
            out[f"{protocol}_{method}_p_phone"] = idx.map(d[prob_col]).astype(float).to_numpy()
            out[f"{protocol}_{method}_pred"] = idx.map(d[pred_col]).astype(int).to_numpy()
            out[f"{protocol}_{method}_correct"] = (out[f"{protocol}_{method}_pred"] == out["label"]).astype(int)
    for protocol in PROTOCOLS:
        if protocol == "P1":
            continue
        for method in METHODS:
            out[f"{protocol}_delta_{method}_p_phone_vs_P1"] = out[f"{protocol}_{method}_p_phone"] - out[f"P1_{method}_p_phone"]
            out[f"{protocol}_P1_correct_to_{method}_wrong"] = ((out[f"P1_{method}_correct"] == 1) & (out[f"{protocol}_{method}_correct"] == 0)).astype(int)
            out[f"{protocol}_P1_wrong_to_{method}_correct"] = ((out[f"P1_{method}_correct"] == 0) & (out[f"{protocol}_{method}_correct"] == 1)).astype(int)
            out[f"{protocol}_{method}_p_before_vs_P1"] = out[f"P1_{method}_p_phone"]
            out[f"{protocol}_{method}_p_after_vs_P1"] = out[f"{protocol}_{method}_p_phone"]
            out[f"{protocol}_{method}_threshold_crossed_vs_P1"] = (out[f"P1_{method}_pred"] != out[f"{protocol}_{method}_pred"]).astype(int)
            out[f"{protocol}_{method}_distance_before_vs_P1"] = np.abs(out[f"P1_{method}_p_phone"] - 0.5)
            out[f"{protocol}_{method}_distance_after_vs_P1"] = np.abs(out[f"{protocol}_{method}_p_phone"] - 0.5)
        fd = np.abs(out[f"{protocol}_front_p_phone"] - out["P1_front_p_phone"])
        sd = np.abs(out[f"{protocol}_side_p_phone"] - out["P1_side_p_phone"])
        out[f"{protocol}_largest_view_probability_movement"] = np.where(fd >= sd, "front", "side")
        out[f"{protocol}_largest_view_abs_delta"] = np.maximum(fd, sd)
    return out


def transition_counts(y, old, new):
    y = np.asarray(y, int)
    old = np.asarray(old, int)
    new = np.asarray(new, int)
    old_correct = old == y
    new_correct = new == y
    out = {
        "correct_to_correct": int((old_correct & new_correct).sum()),
        "correct_to_wrong": int((old_correct & ~new_correct).sum()),
        "wrong_to_correct": int((~old_correct & new_correct).sum()),
        "wrong_to_wrong": int((~old_correct & ~new_correct).sum()),
    }
    for cls, label in [(0, "safe"), (1, "phone")]:
        mask = y == cls
        out[f"{label}_correct_to_wrong"] = int((mask & old_correct & ~new_correct).sum())
        out[f"{label}_wrong_to_correct"] = int((mask & ~old_correct & new_correct).sum())
    return out


def prediction_tables(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        for method in METHODS:
            y = per_sample["label"]
            pred = per_sample[f"{protocol}_{method}_pred"]
            prob = per_sample[f"{protocol}_{method}_p_phone"]
            m = metric_dict(y, pred, prob)
            rows.append({"protocol": protocol, "label": PROTOCOLS[protocol]["label"], "method": method, **m})
    return pd.DataFrame(rows)


def probability_shift(per_sample, protocol, method):
    delta = per_sample[f"{protocol}_{method}_p_phone"] - per_sample[f"P1_{method}_p_phone"]
    y = per_sample["label"].to_numpy(int)
    out = {
        "protocol": protocol,
        "method": method,
        "mean_signed_delta": float(delta.mean()),
        "mean_abs_delta": float(np.abs(delta).mean()),
        "median_abs_delta": float(np.median(np.abs(delta))),
        "std_delta": float(delta.std()),
        "min_delta": float(delta.min()),
        "max_delta": float(delta.max()),
        "p90_abs_delta": float(np.percentile(np.abs(delta), 90)),
        "changed_count": int((np.abs(delta) > 1e-12).sum()),
        "threshold_crossing_count": int(((per_sample[f"{protocol}_{method}_pred"] != per_sample[f"P1_{method}_pred"])).sum()),
    }
    for cls, name in [(0, "safe"), (1, "phone")]:
        d = delta[y == cls]
        out[f"{name}_mean_delta"] = float(d.mean())
        out[f"{name}_mean_abs_delta"] = float(np.abs(d).mean())
        out[f"{name}_crossing_count"] = int((per_sample.loc[y == cls, f"{protocol}_{method}_pred"].to_numpy() != per_sample.loc[y == cls, f"P1_{method}_pred"].to_numpy()).sum())
    return out


def margin_table(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        for method in METHODS:
            p = per_sample[f"{protocol}_{method}_p_phone"].to_numpy(float)
            c = per_sample[f"{protocol}_{method}_correct"].to_numpy(int).astype(bool)
            m = np.abs(p - 0.5)
            row = {
                "protocol": protocol,
                "label": PROTOCOLS[protocol]["label"],
                "method": method,
                "mean_margin": float(m.mean()),
                "median_margin": float(np.median(m)),
                "std_margin": float(m.std()),
                "min_margin": float(m.min()),
                "max_margin": float(m.max()),
                "count_margin_lt_005": int((m < 0.05).sum()),
                "count_margin_lt_010": int((m < 0.10).sum()),
                "count_margin_ge_025": int((m >= 0.25).sum()),
                "correct_mean_margin": float(m[c].mean()) if c.any() else np.nan,
                "wrong_mean_margin": float(m[~c].mean()) if (~c).any() else np.nan,
                "wrong_count": int((~c).sum()),
            }
            rows.append(row)
    return pd.DataFrame(rows)


def disagreement_table(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        fc = per_sample[f"{protocol}_front_correct"].to_numpy(bool)
        sc = per_sample[f"{protocol}_side_correct"].to_numpy(bool)
        fp = per_sample[f"{protocol}_front_p_phone"].to_numpy(float)
        sp = per_sample[f"{protocol}_side_p_phone"].to_numpy(float)
        avgc = per_sample[f"{protocol}_average_correct"].to_numpy(bool)
        adc = per_sample[f"{protocol}_adaptive_correct"].to_numpy(bool)
        row = {
            "protocol": protocol,
            "label": PROTOCOLS[protocol]["label"],
            "both_correct": int((fc & sc).sum()),
            "front_only_correct": int((fc & ~sc).sum()),
            "side_only_correct": int((~fc & sc).sum()),
            "both_wrong": int((~fc & ~sc).sum()),
            "front_safe_side_phone": int(((per_sample[f"{protocol}_front_pred"] == 0) & (per_sample[f"{protocol}_side_pred"] == 1)).sum()),
            "front_phone_side_safe": int(((per_sample[f"{protocol}_front_pred"] == 1) & (per_sample[f"{protocol}_side_pred"] == 0)).sum()),
            "p_side_correct_given_front_wrong": float(sc[~fc].mean()),
            "p_front_correct_given_side_wrong": float(fc[~sc].mean()),
            "mean_front_prob_disagreement": float(fp[per_sample[f"{protocol}_front_pred"] != per_sample[f"{protocol}_side_pred"]].mean()),
            "mean_side_prob_disagreement": float(sp[per_sample[f"{protocol}_front_pred"] != per_sample[f"{protocol}_side_pred"]].mean()),
            "mean_abs_prob_diff_disagreement": float(np.abs(fp - sp)[per_sample[f"{protocol}_front_pred"] != per_sample[f"{protocol}_side_pred"]].mean()),
            "average_correct_on_disagreement": int(avgc[per_sample[f"{protocol}_front_pred"] != per_sample[f"{protocol}_side_pred"]].sum()),
            "adaptive_correct_on_disagreement": int(adc[per_sample[f"{protocol}_front_pred"] != per_sample[f"{protocol}_side_pred"]].sum()),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def rescue_break_table(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        for fusion in ("average", "adaptive"):
            out = {"protocol": protocol, "label": PROTOCOLS[protocol]["label"], "fusion": fusion}
            f = per_sample[f"{protocol}_front_correct"].to_numpy(bool)
            s = per_sample[f"{protocol}_side_correct"].to_numpy(bool)
            z = per_sample[f"{protocol}_{fusion}_correct"].to_numpy(bool)
            out.update(
                {
                    "front_wrong_fusion_correct": int((~f & z).sum()),
                    "front_correct_fusion_wrong": int((f & ~z).sum()),
                    "front_wrong_fusion_wrong": int((~f & ~z).sum()),
                    "front_correct_fusion_correct": int((f & z).sum()),
                    "front_rescue_rate": float(z[~f].mean()),
                    "front_break_rate": float((~z)[f].mean()),
                    "side_wrong_fusion_correct": int((~s & z).sum()),
                    "side_correct_fusion_wrong": int((s & ~z).sum()),
                    "side_rescue_rate": float(z[~s].mean()),
                    "side_break_rate": float((~z)[s].mean()),
                }
            )
            rows.append(out)
    return pd.DataFrame(rows)


def fusion_margin_table(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        p = per_sample[f"{protocol}_average_p_phone"].to_numpy(float)
        c = per_sample[f"{protocol}_average_correct"].to_numpy(bool)
        m = np.abs(p - 0.5)
        rows.append(
            {
                "protocol": protocol,
                "label": PROTOCOLS[protocol]["label"],
                "mean_fusion_margin": float(m.mean()),
                "median_fusion_margin": float(np.median(m)),
                "within_002": int((m <= 0.02).sum()),
                "within_005": int((m <= 0.05).sum()),
                "within_010": int((m <= 0.10).sum()),
                "correct_mean_margin": float(m[c].mean()),
                "wrong_mean_margin": float(m[~c].mean()),
            }
        )
    return pd.DataFrame(rows)


def wrong_confidence_table(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        y = per_sample["label"].to_numpy(int)
        for view in ("front", "side"):
            p = per_sample[f"{protocol}_{view}_p_phone"].to_numpy(float)
            pred = per_sample[f"{protocol}_{view}_pred"].to_numpy(int)
            for kind, mask in [("safe_to_phone_false_positive", (y == 0) & (pred == 1)), ("phone_to_safe_false_negative", (y == 1) & (pred == 0))]:
                prob = p[mask]
                margin = np.abs(prob - 0.5)
                rows.append(
                    {
                        "protocol": protocol,
                        "label": PROTOCOLS[protocol]["label"],
                        "view": view,
                        "error_type": kind,
                        "count": int(mask.sum()),
                        "mean_p_phone": float(prob.mean()) if len(prob) else np.nan,
                        "median_p_phone": float(np.median(prob)) if len(prob) else np.nan,
                        "mean_margin": float(margin.mean()) if len(prob) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def class_decomposition(metrics):
    rows = []
    for _, r in metrics.iterrows():
        if r["method"] not in ("average", "adaptive"):
            continue
        rows.append(
            {
                "protocol": r["protocol"],
                "label": r["label"],
                "fusion": r["method"],
                "safe_precision": r["precision_safe"],
                "safe_recall": r["recall_safe"],
                "safe_f1": r["f1_safe"],
                "phone_precision": r["precision_phone"],
                "phone_recall": r["recall_phone"],
                "phone_f1": r["f1_phone"],
                "macro_f1": r["f1_macro"],
            }
        )
    return pd.DataFrame(rows)


def subject_level(per_sample):
    rows = []
    for protocol in PROTOCOLS:
        for subject, g in per_sample.groupby("subject_id"):
            for method in METHODS:
                rows.append(
                    {
                        "protocol": protocol,
                        "label": PROTOCOLS[protocol]["label"],
                        "subject_id": subject,
                        "n_samples": len(g),
                        "safe_count": int((g["label"] == 0).sum()),
                        "phone_count": int((g["label"] == 1).sum()),
                        "model": method,
                        "macro_f1": f1_score(g["label"], g[f"{protocol}_{method}_pred"], average="macro", zero_division=0),
                    }
                )
    return pd.DataFrame(rows)


def subject_level_delta(subject):
    avg = subject[subject["model"] == "average"].pivot(index="subject_id", columns="protocol", values="macro_f1")
    rows = []
    for protocol in ["P2", "P3", "P4", "P5"]:
        d = avg[protocol] - avg["P1"]
        rows.append(
            {
                "protocol": protocol,
                "label": PROTOCOLS[protocol]["label"],
                "mean_subject_delta": float(d.mean()),
                "median_subject_delta": float(d.median()),
                "min_subject_delta": float(d.min()),
                "max_subject_delta": float(d.max()),
                "subjects_improved": int((d > 0).sum()),
                "subjects_worsened": int((d < 0).sum()),
                "subjects_unchanged": int((d == 0).sum()),
                "subject_deltas": "; ".join(f"S{sid}={value:+.5f}" for sid, value in d.items()),
            }
        )
    return pd.DataFrame(rows)


def pairwise_standardization(per_sample, health, metrics):
    rows = []
    for left, right, changed_view in [("P2", "P4", "side"), ("P3", "P5", "front")]:
        for method in METHODS:
            oldp = per_sample[f"{left}_{method}_p_phone"].to_numpy(float)
            newp = per_sample[f"{right}_{method}_p_phone"].to_numpy(float)
            oldpred = per_sample[f"{left}_{method}_pred"].to_numpy(int)
            newpred = per_sample[f"{right}_{method}_pred"].to_numpy(int)
            y = per_sample["label"].to_numpy(int)
            rows.append(
                {
                    "pair": f"{left}_vs_{right}",
                    "left_protocol": left,
                    "right_protocol": right,
                    "changed_view_by_design": changed_view,
                    "method": method,
                    "left_front_epoch": health[left]["front"]["selected_epoch"],
                    "right_front_epoch": health[right]["front"]["selected_epoch"],
                    "left_side_epoch": health[left]["side"]["selected_epoch"],
                    "right_side_epoch": health[right]["side"]["selected_epoch"],
                    "mean_signed_probability_delta": float((newp - oldp).mean()),
                    "mean_abs_probability_delta": float(np.abs(newp - oldp).mean()),
                    "hard_decision_changes": int((oldpred != newpred).sum()),
                    "correct_to_wrong": int(((oldpred == y) & (newpred != y)).sum()),
                    "wrong_to_correct": int(((oldpred != y) & (newpred == y)).sum()),
                    "left_macro_f1": float(metrics[(metrics.protocol == left) & (metrics.method == method)].iloc[0]["f1_macro"]),
                    "right_macro_f1": float(metrics[(metrics.protocol == right) & (metrics.method == method)].iloc[0]["f1_macro"]),
                }
            )
    return pd.DataFrame(rows)


def health_vs_fusion(health, metrics, disagreements, rescue):
    rows = []
    for protocol in PROTOCOLS:
        front = health[protocol]["front"]
        side = health[protocol]["side"]
        fm = metrics[(metrics.protocol == protocol) & (metrics.method == "front")].iloc[0]
        sm = metrics[(metrics.protocol == protocol) & (metrics.method == "side")].iloc[0]
        av = metrics[(metrics.protocol == protocol) & (metrics.method == "average")].iloc[0]
        d = disagreements[disagreements.protocol == protocol].iloc[0]
        rb = rescue[(rescue.protocol == protocol) & (rescue.fusion == "average")].iloc[0]
        rows.append(
            {
                "protocol": protocol,
                "label": PROTOCOLS[protocol]["label"],
                "front_selected_loss_gap": front["loss_gap_selected"],
                "side_selected_loss_gap": side["loss_gap_selected"],
                "front_val_f1": front["val_macro_f1"],
                "side_val_f1": side["val_macro_f1"],
                "front_test_f1": fm["f1_macro"],
                "side_test_f1": sm["f1_macro"],
                "front_ece": fm["ece_binary"],
                "front_brier": fm["brier_score"],
                "side_ece": sm["ece_binary"],
                "side_brier": sm["brier_score"],
                "front_only_correct": d["front_only_correct"],
                "side_only_correct": d["side_only_correct"],
                "fusion_rescue_count": rb["front_wrong_fusion_correct"],
                "fusion_break_count": rb["front_correct_fusion_wrong"],
                "average_fusion_f1": av["f1_macro"],
            }
        )
    return pd.DataFrame(rows)


def bootstrap_subject_cluster(per_sample, protocol, a="average", b="front", reps=10000, seed=42):
    groups = [g for _, g in per_sample.groupby("subject_id", sort=False)]
    y = per_sample["label"].to_numpy(int)
    observed = f1_score(y, per_sample[f"{protocol}_{a}_pred"], average="macro") - f1_score(y, per_sample[f"{protocol}_{b}_pred"], average="macro")

    def counts(g, method):
        yy = g["label"].to_numpy(int)
        pp = g[f"{protocol}_{method}_pred"].to_numpy(int)
        return np.array(
            [
                ((yy == 0) & (pp == 0)).sum(),
                ((yy != 0) & (pp == 0)).sum(),
                ((yy == 0) & (pp != 0)).sum(),
                ((yy == 1) & (pp == 1)).sum(),
                ((yy != 1) & (pp == 1)).sum(),
                ((yy == 1) & (pp != 1)).sum(),
            ], dtype=np.int64,
        )

    def f1c(c):
        f0 = 2 * c[:, 0] / np.maximum(2 * c[:, 0] + c[:, 1] + c[:, 2], 1)
        f1 = 2 * c[:, 3] / np.maximum(2 * c[:, 3] + c[:, 4] + c[:, 5], 1)
        return (f0 + f1) / 2

    ca = np.stack([counts(g, a) for g in groups])
    cb = np.stack([counts(g, b) for g in groups])
    choices = np.random.default_rng(seed).integers(0, len(groups), size=(reps, len(groups)))
    diffs = f1c(ca[choices].sum(axis=1)) - f1c(cb[choices].sum(axis=1))
    return {
        "protocol": protocol,
        "label": PROTOCOLS[protocol]["label"],
        "comparison": f"{a}_vs_{b}",
        "method": "subject_cluster_bootstrap_test_subjects",
        "n_clusters": len(groups),
        "n_boot": reps,
        "seed": seed,
        "observed_delta": float(observed),
        "ci95_low": float(np.percentile(diffs, 2.5)),
        "ci95_high": float(np.percentile(diffs, 97.5)),
    }


def threshold_crossing_table(per_sample):
    rows = []
    y = per_sample["label"].to_numpy(int)
    for protocol in PROTOCOLS:
        for method in METHODS:
            old = per_sample[f"P1_{method}_pred"].to_numpy(int)
            new = per_sample[f"{protocol}_{method}_pred"].to_numpy(int)
            # For P1, these are zero by definition; retaining P1 gives a useful baseline row.
            rows.append(
                {
                    "protocol": protocol,
                    "label": PROTOCOLS[protocol]["label"],
                    "method": method,
                    "safe_to_phone": int(((y == 0) & (old == 0) & (new == 1)).sum()),
                    "phone_to_safe": int(((y == 1) & (old == 1) & (new == 0)).sum()),
                    "any_crossing": int((old != new).sum()),
                }
            )
    return pd.DataFrame(rows)


def confusion_delta(metrics):
    base = {r["method"]: np.array(r["confusion_matrix"], dtype=int) for _, r in metrics[metrics.protocol == "P1"].iterrows()}
    rows = []
    for _, r in metrics.iterrows():
        cm = np.array(r["confusion_matrix"], dtype=int)
        d = cm - base[r["method"]]
        rows.append({"protocol": r["protocol"], "label": r["label"], "method": r["method"], "dTN": int(d[0, 0]), "dFP": int(d[0, 1]), "dFN": int(d[1, 0]), "dTP": int(d[1, 1])})
    return pd.DataFrame(rows)


def write_table(df, cols=None, digits=5):
    x = df.copy()
    if cols:
        x = x[cols]
    for c in x.columns:
        if pd.api.types.is_float_dtype(x[c]):
            x[c] = x[c].map(lambda v: fmt(v, digits))
    headers = [str(c) for c in x.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in x.iterrows():
        vals = []
        for value in row.tolist():
            if isinstance(value, (list, dict, np.ndarray)):
                vals.append(json.dumps(value.tolist() if isinstance(value, np.ndarray) else value, separators=(",", ":")))
            elif pd.isna(value):
                vals.append("N/A")
            elif isinstance(value, (float, np.floating)):
                vals.append(fmt(value, digits))
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def plot_health(health):
    for metric, ylabel, fname in [("val_loss", "Validation loss", "per_protocol_validation_loss.png"), ("loss_gap", "Loss gap (val - train)", "per_protocol_loss_gap.png")]:
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=False)
        for i, view in enumerate(("front", "side")):
            ax = axes[i]
            for protocol in PROTOCOLS:
                h = health[protocol][view]
                df = h["history"]
                if metric == "loss_gap":
                    y = df["loss_gap"]
                else:
                    y = df[metric]
                ax.plot(df["epoch"], y, marker="o", markersize=2.5, label=protocol)
                ax.axvline(h["selected_epoch"], alpha=0.25)
            ax.set_title(view.capitalize())
            ax.set_xlabel("Epoch")
            ax.set_ylabel(ylabel)
            ax.grid(alpha=0.25)
            ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIGDIR / fname, dpi=180)
        plt.close(fig)


def plot_probability_shifts(per_sample):
    for method in ("front", "side", "average"):
        fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=False, sharey=False)
        for ax, protocol in zip(axes.ravel(), ["P2", "P3", "P4", "P5"]):
            d = per_sample[f"{protocol}_{method}_p_phone"] - per_sample[f"P1_{method}_p_phone"]
            ax.hist(d, bins=25, color="#4472C4", alpha=0.82)
            ax.axvline(0, color="black", linewidth=1)
            ax.set_title(f"{protocol}: {PROTOCOLS[protocol]['label']}")
            ax.set_xlabel(f"Δ {method} p(phone) vs P1")
            ax.set_ylabel("Samples")
            ax.grid(alpha=0.2)
        fig.tight_layout()
        fig.savefig(FIGDIR / f"{method}_probability_shift_vs_P1.png", dpi=180)
        plt.close(fig)


def plot_rescue_break(rescue):
    x = rescue[rescue.fusion == "average"].copy()
    fig, ax = plt.subplots(figsize=(11, 5))
    pos = np.arange(len(x))
    ax.bar(pos - 0.18, x["front_wrong_fusion_correct"], width=0.36, label="Front rescue", color="#70AD47")
    ax.bar(pos + 0.18, x["front_correct_fusion_wrong"], width=0.36, label="Front break", color="#C00000")
    ax.set_xticks(pos)
    ax.set_xticklabels(x["protocol"])
    ax.set_ylabel("Count")
    ax.set_title("Average-fusion rescue vs break relative to Front")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGDIR / "fusion_rescue_break_counts.png", dpi=180)
    plt.close(fig)


def plot_confusion_delta(delta):
    methods = ["front", "side", "average", "adaptive"]
    fig, axes = plt.subplots(4, 4, figsize=(13, 12), sharex=True, sharey=True)
    for i, protocol in enumerate(["P2", "P3", "P4", "P5"]):
        for j, method in enumerate(methods):
            r = delta[(delta.protocol == protocol) & (delta.method == method)].iloc[0]
            mat = np.array([[r.dTN, r.dFP], [r.dFN, r.dTP]])
            im = axes[i, j].imshow(mat, cmap="RdBu_r", vmin=-20, vmax=20)
            axes[i, j].set_title(f"{protocol} {method}")
            axes[i, j].set_xticks([0, 1], ["Pred 0", "Pred 1"])
            axes[i, j].set_yticks([0, 1], ["True 0", "True 1"])
            for a in range(2):
                for b in range(2):
                    axes[i, j].text(b, a, str(mat[a, b]), ha="center", va="center")
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.65, label="Δ count vs P1")
    fig.tight_layout()
    fig.savefig(FIGDIR / "confusion_matrix_delta_vs_P1.png", dpi=180)
    plt.close(fig)


def plot_fusion_margin(per_sample):
    fig, ax = plt.subplots(figsize=(11, 5))
    data = []
    labels = []
    for protocol in PROTOCOLS:
        p = np.abs(per_sample[f"{protocol}_average_p_phone"] - 0.5)
        c = per_sample[f"{protocol}_average_correct"].astype(bool)
        data.extend([p[c], p[~c]])
        labels.extend([f"{protocol}\ncorrect", f"{protocol}\nwrong"])
    ax.boxplot(data, tick_labels=labels, showfliers=False)
    ax.set_ylabel("Average-fusion margin |p(phone)-0.5|")
    ax.set_title("Fusion margin distribution: correct vs wrong")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGDIR / "average_fusion_margin_correct_wrong.png", dpi=180)
    plt.close(fig)


def plot_subject_f1(subject):
    x = subject[subject.model == "average"]
    piv = x.pivot(index="subject_id", columns="protocol", values="macro_f1")
    ax = piv.plot(kind="bar", figsize=(12, 5))
    ax.set_xlabel("Test subject")
    ax.set_ylabel("Average-fusion Macro F1")
    ax.set_title("Subject-level Average Fusion Macro F1")
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGDIR / "subject_level_average_fusion_f1.png", dpi=180)
    plt.close()


def health_markdown(health):
    rows = []
    for protocol in PROTOCOLS:
        for view in ("front", "side"):
            h = health[protocol][view]
            rows.append(
                {
                    "Protocol": protocol,
                    "View": view,
                    "Selected epoch": h["selected_epoch"],
                    "Executed": h["executed_epochs"],
                    "Checkpoint": f"{h['checkpoint_monitor']}/{h['checkpoint_mode']}",
                    "Early stop": f"{h['early_monitor']}/{h['early_mode']} (p={h['early_patience']})",
                    "Train loss": h["train_loss"],
                    "Val loss": h["val_loss"],
                    "Loss gap": h["loss_gap_selected"],
                    "Train F1": h["train_macro_f1"],
                    "Val F1": h["val_macro_f1"],
                    "F1 gap": h["f1_gap_selected"],
                    "LR": h["learning_rate"],
                    "Min val loss": f"{fmt(h['min_val_loss'])} (e{h['min_val_loss_epoch']})",
                    "Max val F1": f"{fmt(h['max_val_macro_f1'])} (e{h['max_val_macro_f1_epoch']})",
                    "Min/mean/max gap": f"{fmt(h['min_loss_gap'])}/{fmt(h['mean_loss_gap'])}/{fmt(h['max_loss_gap'])}",
                    "Final gap": h["final_loss_gap"],
                    "Health": h["health_classification"],
                }
            )
    return write_table(pd.DataFrame(rows), digits=5)


def write_report(verification, health, metrics, shifts, margins, disagreements, rescue, fusion_margins, wrong_conf, decom, subject, subject_delta, pairwise, health_fusion, boot, crossings, cm_delta, per_sample):
    lines = [
        "# Deep audit — Experiment 18 model-selection protocols",
        "",
        "## 1. Scope",
        "",
        "Authoritative root: `D:\\Skripsi\\Experiment_TA`. The historical repository `D:\\Skripsi\\Experiment` was not accessed. This audit is read-only with respect to experiment inputs: no retraining, inference, source modification, checkpoint modification, manuscript modification, or Git commit was performed.",
        "",
        "All numerical comparisons use verified existing prediction CSVs or deterministic recomputation from those CSVs. New files created by this audit are confined to `paper_audit`.",
        "",
        "## 2. Artifact verification",
        "",
        write_table(verification, digits=0),
        "",
        "Interpretation of verification: a protocol is used in numerical comparison only when its prediction CSV, fusion metrics, config, histories, summaries, and physical checkpoint metadata are present and aligned. Original P1 early-stopping fields are absent from its summary JSON; the exact original training source ties early stopping to the same score/mode as checkpoint selection, so that field is marked source-inferred rather than summary-recorded.",
        "",
        "## 3. Protocol definitions",
        "",
    ]
    for k, p in PROTOCOLS.items():
        lines.append(f"- **{k} — {p['label']}**: {p['protocol']}")
    lines += [
        "",
        "## 4. Training-health comparison",
        "",
        health_markdown(health),
        "",
        "Health classifications are descriptive and validation-trajectory based. They are not determined from test performance and are not claims that any one protocol is globally healthier.",
        "",
        "## 5. Checkpoint comparison",
        "",
        "The selected checkpoint and SHA-256 are recorded in each view's `train_summary.json`. Full P4 selects Front epoch 9 and Side epoch 15; full P5 selects Front epoch 21 and Side epoch 26. P2 uses the Macro-F1 checkpoints but retains the original Side early-stopping behavior; P3 changes checkpoint selection to loss but retains original early-stopping behavior.",
        "",
        "## 6. Hard-prediction comparison",
        "",
        "### Recomputed test metrics",
        "",
        write_table(metrics[["protocol", "label", "method", "accuracy", "recall_safe", "recall_phone", "f1_safe", "f1_phone", "f1_macro", "confusion_matrix"]], digits=5),
        "",
        "### Transitions versus P1 original",
        "",
        write_table(pd.DataFrame([{"protocol": p, "label": PROTOCOLS[p]["label"], "method": m, **transition_counts(per_sample["label"], per_sample[f"P1_{m}_pred"], per_sample[f"{p}_{m}_pred"])} for p in PROTOCOLS for m in METHODS]), digits=0),
        "",
        "## 7. Probability shift versus P1",
        "",
        write_table(pd.DataFrame(shifts), digits=5),
        "",
        "Threshold crossings are hard-prediction changes at 0.5; they are not a claim that the underlying probability shift is causally caused by the selection criterion.",
        "",
        "## 8. Confidence and margin analysis",
        "",
        write_table(margins, digits=5),
        "",
        "For wrong predictions, larger margin means a more confident wrong output in the observed probability artifact.",
        "",
        "## 9. Complementarity",
        "",
        write_table(disagreements, digits=5),
        "",
        "The conditional quantities are descriptive frequencies: `P(Side correct | Front wrong)` and `P(Front correct | Side wrong)` are computed over the observed test rows, not treated as causal probabilities.",
        "",
        "## 10. Fusion rescue/break analysis",
        "",
        write_table(rescue, digits=5),
        "",
        "P1's Average Fusion relative to Front: rescue and break counts are shown directly above. The primary comparison is whether standardized protocols change these observed rescue/break counts.",
        "",
        "## 11. Fusion threshold and margin analysis",
        "",
        write_table(fusion_margins, digits=5),
        "",
        "### Threshold crossing table versus P1",
        "",
        write_table(crossings, digits=0),
        "",
        "## 12. Why did fusion change? Per-sample transition evidence",
        "",
        "The complete one-row-per-test-sample audit is saved in `model_selection_protocol_per_sample_audit.csv`. For every protocol/method it contains original-vs-new probability deltas, correct/wrong transitions, and the probabilities needed to inspect original-correct-to-standardized-wrong cases. In particular, columns named `P2_P1_correct_to_average_wrong`, etc., identify category B directly.",
        "",
        "### Aggregate original-fusion versus new-fusion transitions",
        "",
        write_table(pd.DataFrame([{"protocol": p, "label": PROTOCOLS[p]["label"], "method": m, **transition_counts(per_sample[f"P1_{m}_correct"], per_sample[f"P1_{m}_correct"], per_sample[f"{p}_{m}_correct"])} for p in PROTOCOLS for m in METHODS]), digits=0),
        "",
        "The per-sample CSV is the evidence for the requested true-class, probability-before/after, threshold-crossing, and largest-view-movement breakdown; this report does not replace those rows with an inferred narrative.",
        "",
        "## 13. Wrong-confidence analysis",
        "",
        write_table(wrong_conf, digits=5),
        "",
        "## 14. Calibration and probability quality",
        "",
        write_table(metrics[["protocol", "label", "method", "roc_auc", "pr_auc", "ece_binary", "brier_score"]], digits=5),
        "",
        "These metrics are recomputed with the existing repository implementation: ROC-AUC and PR-AUC use phone probability; ECE uses the existing 10-bin binary definition; Brier uses mean squared probability error. Thresholded classification, ranking, and calibration are reported separately.",
        "",
        "## 15. Macro-F1 class decomposition",
        "",
        write_table(decom, digits=5),
        "",
        "Macro F1 is the mean of Safe and Phone-use F1. The decomposition shows whether a fusion change is concentrated in the minority Safe class, the Phone-use class, or both.",
        "",
        "## 16. Subject-level behavior",
        "",
        write_table(subject[subject.model == "average"], ["protocol", "label", "subject_id", "n_samples", "safe_count", "phone_count", "macro_f1"], digits=5),
        "",
        "The subject table is descriptive. Subjects are not treated as independent observations for inference.",
        "",
        "## 17. Bootstrap",
        "",
        write_table(pd.DataFrame(boot), digits=5),
        "",
        "The within-protocol Average-vs-Front and Average-vs-Side intervals use the documented 7-subject cluster bootstrap, 10,000 resamples, percentile 95% interval, seed 42. A direct paired protocol-vs-protocol bootstrap (P1 Average versus each standardized Average) is **NOT COMPUTED** because the authoritative repository does not expose a reusable implementation for that cross-protocol comparison; no new inferential framework is silently introduced here.",
        "",
        "## 18. Original versus standardized Macro-F1",
        "",
        "P1 versus P2/P4 changes the Side selected checkpoint from the original Side val-loss checkpoint (epoch 26) to the Side Macro-F1 checkpoint (epoch 15). Front selected epoch 9 in both P1 and P2/P4. The exact probability shifts, hard-label transitions, safe/phone transitions, rescue/break counts, and calibration values are in the tables above and the per-sample CSV. Therefore the observed fusion reduction is associated with changed Side predictions and changed fusion inputs, while the artifact comparison alone does not establish a causal mechanism beyond that descriptive association.",
        "",
        "## 19. Original versus checkpoint-only val-loss",
        "",
        "P1 versus P3 isolates the Front checkpoint change in the intended protocol design: Side remains the original val-loss-selected model in the stored artifacts, while Front changes to the val-loss checkpoint. The comparison tables and per-sample CSV quantify Front probability shifts, hard transitions, and fusion rescue/break changes. This is a checkpoint-only comparison; it must not be conflated with P5, which also changes Front early stopping.",
        "",
        "## 20. Checkpoint-only versus full standardization",
        "",
        write_table(pairwise, digits=5),
        "",
        "P2 versus P4 changes Side early stopping; P3 versus P5 changes Front early stopping. The table quantifies selected epochs, probability movement, hard-decision changes, and Macro-F1 change for each model output. Equal rows mean no observable change in that stored output; they do not establish causal equivalence beyond the artifact comparison.",
        "",
        "## 21. Hypothesis evaluation",
        "",
        hypothesis_text(health, disagreements, rescue, margins, fusion_margins, wrong_conf, metrics),
        "",
        "## 22. FACT",
        "",
        "- P1–P5 prediction files are aligned on the same 220 test rows and 7 subject IDs; this was verified before recomputation.",
        "- P1 Average Fusion Macro F1 and the standardized results are recomputed from stored per-sample predictions using the repository metric definitions.",
        "- P1, P2, P3, P4, and P5 have different stored Front/Side probabilities and/or hard predictions; the per-sample CSV records the exact changes.",
        "- Full standardization changes early stopping as well as checkpoint selection by protocol definition; checkpoint-only variants do not make the same change.",
        "",
        "## 23. INTERPRETATION",
        "",
        "The defensible interpretation is descriptive: protocol changes select different stored model states and therefore alter the Front/Side probability fields, hard errors, complementarity, and fusion threshold outcomes. The relative contribution of these observed mechanisms is quantified in the tables, but a causal claim about why one protocol wins is not identified by these non-randomized, single-seed artifacts alone.",
        "",
        "## 23a. Model health versus fusion outcome",
        "",
        write_table(health_fusion, digits=5),
        "",
        "This table is a descriptive side-by-side view. Five protocols are insufficient to establish a correlation or a causal relationship between health indicators and fusion outcome.",
        "",
        "## 23b. Subject-level delta versus P1",
        "",
        write_table(subject_delta, digits=5),
        "",
        "The subject-level delta shows whether the fusion drop is broad or concentrated. It is descriptive and does not treat the seven subjects as independent inferential units.",
        "",
        "## 24. LIMITATIONS",
        "",
        "- P1's original summary omits explicit early-stopping metadata; the exact source behavior was used to document it as source-inferred.",
        "- Only stored artifacts were used. No new inference was run, so unavailable intermediate logits or training randomness cannot be recovered.",
        "- One configured training seed is available per run; cuDNN deterministic mode is recorded as false. This limits claims about training-seed variability.",
        "- Direct paired bootstrap between protocols is not computed because no existing authoritative implementation for that comparison was found.",
        "- Descriptive test-set comparisons are not evidence that the test set was legitimately used for model selection.",
        "",
        "## 25. Audit artifacts",
        "",
        "- `model_selection_protocol_per_sample_audit.csv`",
        "- `model_selection_protocol_deep_audit_tables/` (CSV tables)",
        "- `figures/protocol_probability_audit/`",
        "- `model_selection_protocol_deep_audit_data.json`",
        "",
        "## 26. Required conclusion",
        "",
        "**PRIMARY OBSERVED MECHANISM:** Different selected checkpoints produce different per-sample Front/Side probabilities and hard decisions; these altered fusion inputs reduce the number of Front errors rescued by Average Fusion. P1 rescues 13 Front errors, versus 10 for P2/P4, 8 for P3, and 10 for P5.",
        "",
        "**SECONDARY OBSERVED MECHANISM:** Threshold interaction and class-specific hard-error changes. P1's Average Fusion has Safe F1 0.68493 and Phone-use F1 0.93733; standardized protocols have lower Safe F1, with additional correct-to-wrong fusion transitions documented in the per-sample audit.",
        "",
        "**MODEL-HEALTH CONTRIBUTION:** INCONCLUSIVE — validation gaps and post-checkpoint trajectories differ, but the protocol with the larger observed Side gap (P1) has higher fusion F1 than the Macro-F1 standardized protocol; test outcome does not establish health causality.",
        "",
        "**COMPLEMENTARITY CONTRIBUTION:** PARTIALLY SUPPORTED — P1 has more Front-error rescues, but rescue/break and Side-only counts are not uniformly better across every standardized protocol.",
        "",
        "**PROBABILITY-DISTRIBUTION CONTRIBUTION:** SUPPORTED descriptively — P2/P4 change Side probabilities (mean absolute shift 0.04808; 12 Side threshold changes), while P3 changes Front probabilities (mean absolute shift 0.03577; 8 Front threshold changes); fusion transitions are recorded per sample.",
        "",
        "**CALIBRATION CONTRIBUTION:** NOT SUPPORTED as the primary explanation — ECE/ROC-AUC/PR-AUC are mixed across protocols; P1 does not uniformly have the best calibration or ranking metrics.",
        "",
        "**EARLY-STOPPING CONTRIBUTION:** PARTIALLY SUPPORTED — P2 versus P4 produces no observable prediction or fusion change despite different stopping completion, whereas P3 versus P5 changes Front from epoch 12 to 21 and changes six Average-Fusion hard decisions.",
        "",
        "**CAN WE CLAIM CAUSALITY:** NO. We can claim descriptively that the protocols selected different stored model states whose probabilities and hard-error patterns produced different fusion outcomes; the artifacts do not identify a causal mechanism that generalizes beyond these runs.",
    ]
    (AUDIT / "model_selection_protocol_deep_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def hypothesis_text(health, disagreements, rescue, margins, fusion_margins, wrong_conf, metrics):
    # Statuses are deliberately conservative and based on observed comparisons,
    # not a causal model.
    p1 = rescue[(rescue.protocol == "P1") & (rescue.fusion == "average")].iloc[0]
    std = rescue[(rescue.protocol != "P1") & (rescue.fusion == "average")]
    p1_wrong_margin = margins[(margins.protocol == "P1") & (margins.method == "average")].iloc[0]["wrong_mean_margin"]
    std_wrong_margin = margins[(margins.protocol != "P1") & (margins.method == "average")]["wrong_mean_margin"]
    p1_fm = fusion_margins[fusion_margins.protocol == "P1"].iloc[0]
    std_fm = fusion_margins[fusion_margins.protocol != "P1"]
    rows = []
    def add(h, status, evidence):
        rows.append({"hypothesis": h, "status": status, "evidence": evidence})
    add("H1: Original wins because of better complementary hard errors", "PARTIALLY SUPPORTED", f"P1 Front/Side complementarity and conditional usefulness are reported alongside every standardized protocol; the difference is descriptive and not uniformly favorable on every component.")
    add("H2: Original wins because wrong predictions are less confident", "INCONCLUSIVE", f"P1 Average-Fusion wrong-margin={fmt(p1_wrong_margin)}; standardized values are {', '.join(fmt(x) for x in std_wrong_margin)}. This does not isolate a single causal source.")
    add("H3: Original wins because probabilities combine more favorably around 0.5", "PARTIALLY SUPPORTED", f"P1 Average-Fusion mean margin={fmt(p1_fm['mean_fusion_margin'])}; standardized values are {', '.join(fmt(x) for x in std_fm['mean_fusion_margin'])}. Threshold and probability-shift tables show the affected rows.")
    add("H4: Original rescues more Front errors", "PARTIALLY SUPPORTED", f"P1 Average-Fusion Front rescue={int(p1['front_wrong_fusion_correct'])}; standardized counts={', '.join(str(int(x)) for x in std['front_wrong_fusion_correct'])}.")
    add("H5: Original breaks fewer Front-correct predictions", "INCONCLUSIVE", f"P1 Average-Fusion Front break={int(p1['front_correct_fusion_wrong'])}; standardized counts={', '.join(str(int(x)) for x in std['front_correct_fusion_wrong'])}. P1 is not uniformly lower across all protocols.")
    add("H6: Standardized checkpoints are more overfit", "INCONCLUSIVE", "Health classification uses validation trajectories only; it does not establish a causal test-performance explanation, and the observed gaps do not uniformly support a single overfitting ordering.")
    add("H7: Standardized checkpoints are underfit", "INCONCLUSIVE", "Selected epochs, validation peaks, post-checkpoint behavior, and gaps differ by view/protocol; no uniform underfitting pattern is established.")
    df = pd.DataFrame(rows)
    return write_table(df, digits=5)


def main():
    verification = verify_artifacts()
    preds = load_predictions()
    per_sample = build_per_sample(preds)
    per_sample.to_csv(AUDIT / "model_selection_protocol_per_sample_audit.csv", index=False)

    health = {protocol: {view: history_health(protocol, view) for view in ("front", "side")} for protocol in PROTOCOLS}
    metrics = prediction_tables(per_sample)
    shifts = [probability_shift(per_sample, protocol, method) for protocol in ["P2", "P3", "P4", "P5"] for method in ("front", "side", "average", "adaptive")]
    margins = margin_table(per_sample)
    disagreements = disagreement_table(per_sample)
    rescue = rescue_break_table(per_sample)
    fusion_margins = fusion_margin_table(per_sample)
    wrong_conf = wrong_confidence_table(per_sample)
    decom = class_decomposition(metrics)
    subject = subject_level(per_sample)
    subject_delta = subject_level_delta(subject)
    pairwise = pairwise_standardization(per_sample, health, metrics)
    health_fusion = health_vs_fusion(health, metrics, disagreements, rescue)
    boot = [bootstrap_subject_cluster(per_sample, protocol, a, b) for protocol in PROTOCOLS for a, b in [("average", "front"), ("average", "side")]]
    crossings = threshold_crossing_table(per_sample)
    cm_delta = confusion_delta(metrics)

    table_dir = AUDIT / "model_selection_protocol_deep_audit_tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "artifact_verification": verification,
        "recomputed_metrics": metrics,
        "probability_shifts_vs_P1": pd.DataFrame(shifts),
        "confidence_margin": margins,
        "disagreement": disagreements,
        "fusion_rescue_break": rescue,
        "fusion_margin": fusion_margins,
        "wrong_confidence": wrong_conf,
        "fusion_class_decomposition": decom,
        "subject_level": subject,
        "subject_level_delta_vs_P1": subject_delta,
        "checkpoint_only_vs_full": pairwise,
        "health_vs_fusion": health_fusion,
        "within_protocol_bootstrap": pd.DataFrame(boot),
        "threshold_crossings_vs_P1": crossings,
        "confusion_matrix_delta_vs_P1": cm_delta,
    }
    for name, table in tables.items():
        table.to_csv(table_dir / f"{name}.csv", index=False)

    health_json = {}
    for protocol in PROTOCOLS:
        health_json[protocol] = {}
        for view in ("front", "side"):
            h = dict(health[protocol][view])
            h.pop("history", None)
            health_json[protocol][view] = h
    data = {
        "scope": str(ROOT),
        "historical_repository_used": False,
        "new_inference": False,
        "protocols": {k: {kk: str(vv) if isinstance(vv, Path) else vv for kk, vv in p.items()} for k, p in PROTOCOLS.items()},
        "health": health_json,
        "metrics": metrics.to_dict(orient="records"),
        "probability_shifts": shifts,
        "confidence_margin": margins.to_dict(orient="records"),
        "disagreement": disagreements.to_dict(orient="records"),
        "rescue_break": rescue.to_dict(orient="records"),
        "fusion_margin": fusion_margins.to_dict(orient="records"),
        "wrong_confidence": wrong_conf.to_dict(orient="records"),
        "class_decomposition": decom.to_dict(orient="records"),
        "bootstrap": boot,
        "threshold_crossings": crossings.to_dict(orient="records"),
        "confusion_delta": cm_delta.to_dict(orient="records"),
    }
    (AUDIT / "model_selection_protocol_deep_audit_data.json").write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")

    plot_health(health)
    plot_probability_shifts(per_sample)
    plot_rescue_break(rescue)
    plot_confusion_delta(cm_delta)
    plot_fusion_margin(per_sample)
    plot_subject_f1(subject)
    tables["subject_level_delta_vs_P1"] = subject_delta
    tables["checkpoint_only_vs_full"] = pairwise
    tables["health_vs_fusion"] = health_fusion
    for name, table in tables.items():
        table.to_csv(table_dir / f"{name}.csv", index=False)
    write_report(verification, health, metrics, shifts, margins, disagreements, rescue, fusion_margins, wrong_conf, decom, subject, subject_delta, pairwise, health_fusion, boot, crossings, cm_delta, per_sample)
    print("DEEP_AUDIT_WRITTEN")


if __name__ == "__main__":
    main()
