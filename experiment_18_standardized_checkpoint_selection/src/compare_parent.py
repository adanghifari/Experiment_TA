"""Build a reproducible comparison report against experiment_18."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARENT = ROOT.parent / "experiment_18"
RESULTS = ROOT / "results"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def view_report(view):
    parent_summary = read_json(PARENT / "results" / view / "train_summary.json")
    variant_summary = read_json(RESULTS / view / "train_summary.json")
    parent_test = read_json(PARENT / "results" / view / "test_eval_metrics.json")
    variant_test = read_json(RESULTS / view / "test_eval_metrics.json")
    return {
        "parent": {
            "checkpoint_selection": parent_summary["checkpoint_selection"],
            "best_epoch": parent_summary["best_epoch"],
            "test_macro_f1": parent_test["f1_macro"],
            "test_accuracy": parent_test["accuracy"],
        },
        "variant": {
            "checkpoint_selection": variant_summary["checkpoint_selection"],
            "early_stopping": variant_summary["early_stopping"],
            "best_epoch": variant_summary["best_epoch"],
            "test_macro_f1": variant_test["f1_macro"],
            "test_accuracy": variant_test["accuracy"],
        },
        "delta_variant_minus_parent": {
            "test_macro_f1": round(variant_test["f1_macro"] - parent_test["f1_macro"], 6),
            "test_accuracy": round(variant_test["accuracy"] - parent_test["accuracy"], 6),
        },
    }


def fusion_report():
    parent = read_json(PARENT / "results" / "fusion" / "fusion_metrics.json")
    variant = read_json(RESULTS / "fusion" / "fusion_metrics.json")
    return {
        name: {
            "parent_macro_f1": parent[name]["f1_macro"],
            "variant_macro_f1": variant[name]["f1_macro"],
            "delta_variant_minus_parent": round(variant[name]["f1_macro"] - parent[name]["f1_macro"], 6),
            "parent_accuracy": parent[name]["accuracy"],
            "variant_accuracy": variant[name]["accuracy"],
        }
        for name in ("average_fusion", "adaptive_fusion")
    }


def config_checks():
    parent = {
        view: read_json(PARENT / "results" / view / "train_summary.json")["resolved_config"]
        for view in ("front", "side")
    }
    variant = {
        view: read_json(RESULTS / view / "train_summary.json")["resolved_config"]
        for view in ("front", "side")
    }
    common_equal = {}
    for view in ("front", "side"):
        keys = sorted(set(parent[view]) & set(variant[view]))
        if view == "side":
            keys = [key for key in keys if key not in {"checkpoint_monitor", "checkpoint_monitor_mode"}]
        different = {
            key: {"parent": parent[view][key], "variant": variant[view][key]}
            for key in keys
            if parent[view][key] != variant[view][key]
        }
        common_equal[view] = {"all_common_fields_equal": not different, "different_common_fields": different}
    side = variant["side"]
    return {
        "front_common_config_equal": common_equal["front"]["all_common_fields_equal"],
        "side_common_config_equal_except_checkpoint_monitor": common_equal["side"]["all_common_fields_equal"],
        "front": common_equal["front"],
        "side": common_equal["side"],
        "expected_monitor_change": {
            "parent_side_checkpoint": parent["side"].get("checkpoint_monitor"),
            "variant_side_checkpoint": side.get("checkpoint_monitor"),
            "variant_side_checkpoint_mode": side.get("checkpoint_monitor_mode"),
            "variant_side_early_stopping": side.get("early_stopping_monitor"),
            "variant_side_early_stopping_mode": side.get("early_stopping_mode"),
            "variant_side_early_stopping_patience": side.get("early_stopping_patience"),
            "variant_side_scheduler_monitor": side.get("scheduler_monitor"),
            "variant_side_scheduler_patience": side.get("lr_scheduler_patience"),
        },
    }


def file_checks():
    checks = {}
    for name in ("dataset.py", "model.py", "evaluate.py", "fusion.py", "metrics.py"):
        parent = PARENT / "src" / name
        variant = ROOT / "src" / name
        checks["src/" + name] = {"parent_sha256": sha256(parent), "same_in_variant": sha256(parent) == sha256(variant)}
    checks["manifest_split.csv"] = {"sha256": sha256(ROOT.parent / "data" / "manifest_split.csv")}
    checks["manifest_paired.csv"] = {"sha256": sha256(ROOT.parent / "data" / "manifest_paired.csv")}
    parent_pred = PARENT / "results" / "predictions" / "front_test_predictions.csv"
    variant_pred = RESULTS / "predictions" / "front_test_predictions.csv"
    checks["front_test_predictions.csv"] = {
        "parent_sha256": sha256(parent_pred),
        "variant_sha256": sha256(variant_pred),
        "same": sha256(parent_pred) == sha256(variant_pred),
    }
    return checks


def main():
    front = view_report("front")
    side = view_report("side")
    report = {
        "variant": ROOT.name,
        "parent": PARENT.name,
        "scope": "Side checkpoint-selection criterion only; no Paper_TA changes.",
        "front": front,
        "side": side,
        "fusion": fusion_report(),
        "configuration_checks": config_checks(),
        "file_identity_checks": file_checks(),
    }
    (RESULTS / "comparison_to_experiment_18.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    avg = report["fusion"]["average_fusion"]
    adaptive = report["fusion"]["adaptive_fusion"]
    lines = [
        f"# Comparison: {ROOT.name} vs experiment_18",
        "",
        "This report tests Side checkpoint-selection standardization. Paper_TA was not edited.",
        "",
        "## Protocol",
        "",
        "- Front checkpoint: val_macro_f1/max (unchanged).",
        "- Side checkpoint: val_macro_f1/max (changed from val_loss/min).",
        "- Side early stopping: val_loss/min, patience 5 (kept from experiment_18).",
        "- Side scheduler: val_macro_f1, patience 2 (same effective experiment_18 training metadata).",
        "- Other data, split, seed, augmentation, class weights, loss, optimizer, stride, and model settings: unchanged.",
        "",
        "## Test metrics",
        "",
        "| Metric | experiment_18 | Standardized variant | Delta |",
        "|---|---:|---:|---:|",
        f"| Front Macro F1 | {front['parent']['test_macro_f1']:.5f} | {front['variant']['test_macro_f1']:.5f} | {front['delta_variant_minus_parent']['test_macro_f1']:+.5f} |",
        f"| Side Macro F1 | {side['parent']['test_macro_f1']:.5f} | {side['variant']['test_macro_f1']:.5f} | {side['delta_variant_minus_parent']['test_macro_f1']:+.5f} |",
        f"| Average Fusion Macro F1 | {avg['parent_macro_f1']:.5f} | {avg['variant_macro_f1']:.5f} | {avg['delta_variant_minus_parent']:+.5f} |",
        f"| Adaptive Fusion Macro F1 | {adaptive['parent_macro_f1']:.5f} | {adaptive['variant_macro_f1']:.5f} | {adaptive['delta_variant_minus_parent']:+.5f} |",
        "",
        "## Checkpoint and stopping evidence",
        "",
        f"- Side checkpoint: epoch {side['variant']['best_epoch']}, selected by val_macro_f1/max.",
        f"- Side early stopping: val_loss/min, patience {side['variant']['early_stopping']['patience']}; run completed at epoch {side['variant']['early_stopping']['stopped_after_epoch']}.",
        f"- Front best epoch: {front['variant']['best_epoch']}.",
        f"- Front common configuration equal to parent: {report['configuration_checks']['front_common_config_equal']}.",
        f"- Side common configuration equal apart from intended checkpoint monitor fields: {report['configuration_checks']['side_common_config_equal_except_checkpoint_monitor']}.",
        "",
        "The JSON file contains the full comparison, hashes, and audit checks.",
    ]
    (RESULTS / "comparison_to_experiment_18.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("comparison report written")


if __name__ == "__main__":
    main()
