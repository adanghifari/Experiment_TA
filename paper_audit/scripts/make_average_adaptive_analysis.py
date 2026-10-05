"""Create a compact analysis figure for average versus adaptive fusion.

The figure is derived from the verified Exp18 per-sample artifact.  The
adaptive weights and fused probabilities are reconstructed from the locked
formula and checked against the stored columns before plotting.
"""

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


EXPECTED_N = 220
EXPECTED_MEAN_ABS_DIFF = 0.00757458
EXPECTED_MAX_ABS_DIFF = 0.05102784
EXPECTED_WEIGHT_MEAN = 0.51260
EXPECTED_WEIGHT_STD = 0.03914
EXPECTED_DIFF_COUNT = 220
EXPECTED_WEIGHT_045_055 = 173
EXPECTED_WEIGHT_040_060 = 219


def read_and_validate(source_path: Path):
    with source_path.open(newline="", encoding="utf-8-sig") as source_file:
        rows = list(csv.DictReader(source_file))

    if len(rows) != EXPECTED_N:
        raise RuntimeError(f"Expected {EXPECTED_N} rows, found {len(rows)}")

    weights = []
    p_avg_values = []
    p_adapt_values = []
    stored_avg = []
    stored_adapt = []
    average_predictions = []
    adaptive_predictions = []

    for row in rows:
        p_front = float(row["front_prob_phone"])
        p_side = float(row["side_prob_phone"])
        c_front = abs(p_front - 0.5)
        c_side = abs(p_side - 0.5)
        exp_front = math.exp(c_front)
        exp_side = math.exp(c_side)
        w_front = exp_front / (exp_front + exp_side)
        w_side = exp_side / (exp_front + exp_side)
        p_avg = (p_front + p_side) / 2.0
        p_adapt = w_front * p_front + w_side * p_side

        weights.append(w_front)
        p_avg_values.append(p_avg)
        p_adapt_values.append(p_adapt)
        stored_avg.append(float(row["average_prob_phone"]))
        stored_adapt.append(float(row["adaptive_prob_phone"]))
        average_predictions.append(int(row["average_pred"]))
        adaptive_predictions.append(int(row["adaptive_pred"]))

    max_avg_error = max(abs(a - b) for a, b in zip(p_avg_values, stored_avg))
    max_adapt_error = max(abs(a - b) for a, b in zip(p_adapt_values, stored_adapt))
    differences = [abs(a - b) for a, b in zip(p_adapt_values, p_avg_values)]
    mean_abs_diff = sum(differences) / EXPECTED_N
    max_abs_diff = max(differences)
    weight_mean = sum(weights) / EXPECTED_N
    weight_std = math.sqrt(
        sum((weight - weight_mean) ** 2 for weight in weights) / EXPECTED_N
    )
    decision_changes = sum(
        int((p_avg >= 0.5) != (p_adapt >= 0.5))
        for p_avg, p_adapt in zip(p_avg_values, p_adapt_values)
    )

    if max_avg_error != 0.0 or max_adapt_error != 0.0:
        raise RuntimeError("Reconstructed probabilities do not match stored columns")
    if abs(mean_abs_diff - EXPECTED_MEAN_ABS_DIFF) > 1e-7:
        raise RuntimeError("Mean absolute probability difference does not match audit")
    if abs(max_abs_diff - EXPECTED_MAX_ABS_DIFF) > 1e-7:
        raise RuntimeError("Maximum absolute probability difference does not match audit")
    if abs(weight_mean - EXPECTED_WEIGHT_MEAN) > 1e-5:
        raise RuntimeError("Adaptive weight mean does not match audit")
    if abs(weight_std - EXPECTED_WEIGHT_STD) > 1e-5:
        raise RuntimeError("Adaptive weight population standard deviation does not match audit")
    if sum(diff != 0.0 for diff in differences) != EXPECTED_DIFF_COUNT:
        raise RuntimeError("Expected all samples to have different average/adaptive probabilities")
    if sum(0.45 <= weight <= 0.55 for weight in weights) != EXPECTED_WEIGHT_045_055:
        raise RuntimeError("Adaptive weight count in [0.45, 0.55] does not match audit")
    if sum(0.40 <= weight <= 0.60 for weight in weights) != EXPECTED_WEIGHT_040_060:
        raise RuntimeError("Adaptive weight count in [0.40, 0.60] does not match audit")
    if decision_changes != 0:
        raise RuntimeError("Unexpected hard-decision changes at threshold 0.5")
    if average_predictions != adaptive_predictions:
        raise RuntimeError("Stored average and adaptive predictions are not identical")

    delta_p = [p_adapt - p_avg for p_avg, p_adapt in zip(p_avg_values, p_adapt_values)]
    if not any(delta < 0.0 for delta in delta_p) or not any(delta > 0.0 for delta in delta_p):
        raise RuntimeError("Expected both positive and negative probability shifts")
    return weights, delta_p, mean_abs_diff, max_abs_diff, decision_changes


def main() -> None:
    script_path = Path(__file__).resolve()
    audit_dir = script_path.parent.parent
    source_path = audit_dir.parent / "results" / "final_exp18_complementarity_per_sample.csv"
    output_dir = audit_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    weights, delta_p, mean_abs_diff, max_abs_diff, decision_changes = read_and_validate(source_path)

    fig, axes = plt.subplots(1, 2, figsize=(3.45, 2.45))
    fig.subplots_adjust(left=0.15, right=0.98, bottom=0.24, top=0.93, wspace=0.48)

    ax_weight, ax_probability = axes

    ax_weight.hist(
        weights,
        bins=12,
        range=(0.38, 0.62),
        color="#d9d9d9",
        edgecolor="#555555",
        linewidth=0.45,
    )
    ax_weight.axvline(
        0.5, color="#222222", linewidth=0.8, linestyle="--",
        label="Equal weight",
    )
    ax_weight.axvline(
        EXPECTED_WEIGHT_MEAN, color="#222222", linewidth=0.8,
        linestyle="-", label="Mean = 0.513",
    )
    ax_weight.legend(
        loc="upper right", frameon=False, fontsize=5.5,
        handlelength=1.4, borderpad=0.1, labelspacing=0.2,
    )
    ax_weight.set_xlim(0.38, 0.62)
    ax_weight.set_xlabel("Front-view weight", fontsize=6.8, labelpad=2)
    ax_weight.set_ylabel("Count", fontsize=6.8, labelpad=2)
    ax_weight.tick_params(axis="both", labelsize=6.2, length=2, pad=1)
    ax_weight.text(0.0, 1.04, "(a)", transform=ax_weight.transAxes,
                   fontsize=7.5, fontweight="bold", va="bottom")

    histogram = ax_probability.hist(
        delta_p,
        bins=16,
        range=(-max_abs_diff * 1.12, max_abs_diff * 1.12),
        color="#d9d9d9",
        edgecolor="#555555",
        linewidth=0.45,
    )
    if sum(histogram[0]) != EXPECTED_N:
        raise RuntimeError("Delta histogram does not contain all expected samples")
    ax_probability.axvline(0.0, color="#222222", linewidth=0.8)
    ax_probability.text(
        0.97, 0.94,
        f"{EXPECTED_N} / {EXPECTED_N} scores changed\n"
        f"{decision_changes} / {EXPECTED_N} decisions changed",
        transform=ax_probability.transAxes,
        ha="right", va="top", fontsize=5.5,
    )
    ax_probability.set_xlabel(
        "Adaptive − average\nprobability", fontsize=6.2, labelpad=2
    )
    ax_probability.set_ylabel("Count", fontsize=6.8, labelpad=2)
    ax_probability.tick_params(axis="both", labelsize=6.2, length=2, pad=1)
    ax_probability.text(0.0, 1.04, "(b)", transform=ax_probability.transAxes,
                        fontsize=7.5, fontweight="bold", va="bottom")

    for axis in axes:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    fig.savefig(output_dir / "average_adaptive_analysis.pdf",
                bbox_inches="tight", facecolor="white")
    fig.savefig(output_dir / "average_adaptive_analysis.png",
                dpi=600, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # Keep this value exercised so future edits cannot silently remove the audit.
    assert mean_abs_diff > 0


if __name__ == "__main__":
    main()
