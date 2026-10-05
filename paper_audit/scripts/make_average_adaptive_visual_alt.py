"""Create an alternative compact visualization for Exp18 fusion behavior.

The plot uses only the verified per-sample artifact. Adaptive weights and
probability shifts are reconstructed from the locked Exp18 formula and
validated against the saved probability columns before plotting.
"""

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


EXPECTED_N = 220
EXPECTED_WEIGHT_MEAN = 0.51260
EXPECTED_WEIGHT_STD = 0.03914
EXPECTED_MEAN_ABS_DIFF = 0.00757458
EXPECTED_MAX_ABS_DIFF = 0.05102784


def validate_and_reconstruct(source_path: Path):
    with source_path.open(newline="", encoding="utf-8-sig") as source_file:
        rows = list(csv.DictReader(source_file))

    if len(rows) != EXPECTED_N:
        raise RuntimeError(f"Expected {EXPECTED_N} rows, found {len(rows)}")

    weights = []
    delta_p = []
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

        if p_avg != float(row["average_prob_phone"]):
            raise RuntimeError("Reconstructed p_avg does not match stored p_avg")
        if p_adapt != float(row["adaptive_prob_phone"]):
            raise RuntimeError("Reconstructed p_adapt does not match stored p_adapt")

        weights.append(w_front)
        delta_p.append(p_adapt - p_avg)
        average_predictions.append(int(row["average_pred"]))
        adaptive_predictions.append(int(row["adaptive_pred"]))

    weight_mean = sum(weights) / EXPECTED_N
    weight_std = math.sqrt(
        sum((weight - weight_mean) ** 2 for weight in weights) / EXPECTED_N
    )
    abs_delta = [abs(delta) for delta in delta_p]
    mean_abs_delta = sum(abs_delta) / EXPECTED_N
    max_abs_delta = max(abs_delta)
    score_changes = sum(delta != 0.0 for delta in delta_p)
    decision_changes = sum(
        average != adaptive
        for average, adaptive in zip(average_predictions, adaptive_predictions)
    )

    if abs(weight_mean - EXPECTED_WEIGHT_MEAN) > 1e-5:
        raise RuntimeError("Adaptive front-weight mean does not match locked fact")
    if abs(weight_std - EXPECTED_WEIGHT_STD) > 1e-5:
        raise RuntimeError("Adaptive front-weight population std does not match locked fact")
    if abs(mean_abs_delta - EXPECTED_MEAN_ABS_DIFF) > 1e-7:
        raise RuntimeError("Mean absolute probability shift does not match locked fact")
    if abs(max_abs_delta - EXPECTED_MAX_ABS_DIFF) > 1e-7:
        raise RuntimeError("Maximum probability shift does not match locked fact")
    if score_changes != EXPECTED_N:
        raise RuntimeError("Expected p_avg and p_adapt to differ for all samples")
    if decision_changes != 0:
        raise RuntimeError("Unexpected hard-decision changes")
    if not any(delta < 0.0 for delta in delta_p) or not any(delta > 0.0 for delta in delta_p):
        raise RuntimeError("Expected both positive and negative probability shifts")

    return weights, delta_p, weight_mean, weight_std, mean_abs_delta, max_abs_delta


def deterministic_jitter(count: int, amplitude: float = 0.055):
    """Return repeatable vertical offsets without introducing random state."""
    return [amplitude * (((index * 7) % 17) / 16.0 * 2.0 - 1.0) for index in range(count)]


def main() -> None:
    script_path = Path(__file__).resolve()
    audit_dir = script_path.parent.parent
    source_path = audit_dir.parent / "results" / "final_exp18_complementarity_per_sample.csv"
    output_dir = audit_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    weights, delta_p, weight_mean, weight_std, mean_abs_delta, max_abs_delta = (
        validate_and_reconstruct(source_path)
    )

    fig, axes = plt.subplots(1, 2, figsize=(3.55, 2.15))
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.29, top=0.88, wspace=0.48)
    ax_weight, ax_delta = axes

    # (a) Sample-dependent adaptive front-view weights.
    ax_weight.axvline(
        0.5, color="#555555", linewidth=0.75, linestyle="--",
        label="Equal weight",
    )
    ax_weight.axvline(
        weight_mean, color="#222222", linewidth=0.75, linestyle="-",
        label="Mean = 0.513",
    )
    ax_weight.axhline(0.0, color="#bbbbbb", linewidth=0.5)
    ax_weight.scatter(
        weights,
        deterministic_jitter(len(weights)),
        s=6,
        color="#555555",
        alpha=0.40,
        linewidths=0,
    )
    ax_weight.plot(
        [weight_mean], [0.0], marker="D", markersize=3.4,
        color="#111111", linestyle="None",
    )
    ax_weight.set_xlim(min(weights) - 0.012, max(weights) + 0.012)
    ax_weight.set_ylim(-0.16, 0.16)
    ax_weight.set_yticks([])
    ax_weight.set_xlabel("Front-view weight", fontsize=6.6, labelpad=2)
    ax_weight.tick_params(axis="x", labelsize=6.0, length=2, pad=1)
    ax_weight.text(0.0, 1.04, "(a)", transform=ax_weight.transAxes,
                   fontsize=6.3, fontweight="bold", va="bottom")
    ax_weight.legend(
        loc="upper right", frameon=False, fontsize=5.0,
        handlelength=1.3, borderpad=0.1, labelspacing=0.2,
    )

    # (b) Direct view of the probability shift relative to average fusion.
    delta_limit = max_abs_delta * 1.16
    ax_delta.axvline(0.0, color="#222222", linewidth=0.8)
    ax_delta.axhline(0.0, color="#bbbbbb", linewidth=0.5)
    ax_delta.scatter(
        delta_p,
        deterministic_jitter(len(delta_p)),
        s=7,
        color="#555555",
        alpha=0.45,
        linewidths=0,
    )
    ax_delta.set_xlim(-delta_limit, delta_limit)
    ax_delta.set_ylim(-0.16, 0.16)
    ax_delta.set_yticks([])
    ax_delta.set_xlabel("Adaptive − average\nprobability", fontsize=6.3, labelpad=2)
    ax_delta.set_xlabel(
        "Probability shift\n$p_{\\mathrm{adapt}} - p_{\\mathrm{avg}}$",
        fontsize=6.1, labelpad=2,
    )
    ax_delta.tick_params(axis="x", labelsize=6.0, length=2, pad=1)
    ax_delta.text(0.0, 1.04, "(b)", transform=ax_delta.transAxes,
                  fontsize=6.3, fontweight="bold", va="bottom")
    ax_delta.text(
        0.98, 0.96,
        "220 / 220 scores changed\n0 / 220 decisions changed\n"
        f"mean |Δp| = {mean_abs_delta:.4f}\nmax |Δp| = {max_abs_delta:.4f}",
        transform=ax_delta.transAxes, ha="right", va="top", fontsize=0,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.8),
    )
    ax_delta.text(
        0.98, 0.96,
        f"Scores changed: {EXPECTED_N}/{EXPECTED_N}\n"
        f"Decision changes: 0/{EXPECTED_N}\n"
        f"|Δp| mean/max: {mean_abs_delta:.4f} / {max_abs_delta:.4f}",
        transform=ax_delta.transAxes, ha="right", va="top", fontsize=4.7,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.8),
    )

    for axis in axes:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_visible(False)

    fig.savefig(output_dir / "average_adaptive_visual_alt.pdf",
                bbox_inches="tight", facecolor="white")
    fig.savefig(output_dir / "average_adaptive_visual_alt.png",
                dpi=600, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
