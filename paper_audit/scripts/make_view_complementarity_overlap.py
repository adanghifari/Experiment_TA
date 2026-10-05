"""Create a correctness-overlap matrix for the two camera views.

This artifact uses the locked, audited aggregate counts for the full subset.
It does not read or modify experiment artifacts.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


N = 220
COUNTS = (
    (164, 26),  # Front correct: side correct, side wrong
    (13, 17),   # Front wrong: side correct, side wrong
)


def main() -> None:
    audit_dir = Path(__file__).resolve().parent.parent
    output_dir = audit_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(3.35, 2.50))
    fig.subplots_adjust(left=0.21, right=0.98, bottom=0.27, top=0.96)

    colors = (("#dce7ec", "#f2f2f2"), ("#f2f2f2", "#d9d9d9"))
    labels = (
        ("Both correct", 164),
        ("Front only", 26),
        ("Side only", 13),
        ("Both wrong", 17),
    )

    for row in range(2):
        for col in range(2):
            x = col - 0.5
            y = 0.5 - row
            ax.add_patch(
                Rectangle(
                    (x, y), 1, 1,
                    facecolor=colors[row][col],
                    edgecolor="#777777",
                    linewidth=0.6,
                )
            )
            label, count = labels[row * 2 + col]
            ax.text(col, y + 0.60, label, ha="center", va="center",
                    fontsize=6.8, color="#222222")
            ax.text(col, y + 0.30, str(count), ha="center", va="center",
                    fontsize=12, fontweight="bold", color="#111111")

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xticks([0, 1], labels=["Correct", "Wrong"])
    ax.set_yticks([1, 0], labels=["Correct", "Wrong"])
    ax.tick_params(axis="both", length=0, labelsize=8)
    for tick_label in ax.get_yticklabels():
        tick_label.set_rotation(90)
        tick_label.set_va("center")
        tick_label.set_ha("center")
    ax.set_xlabel("Side View", fontsize=8, labelpad=3)
    ax.set_ylabel("Front View", fontsize=8, labelpad=3)
    ax.text(0.5, -0.24, f"N = {N}", transform=ax.transAxes,
            ha="center", va="top", fontsize=7.5, color="#333333")
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.savefig(output_dir / "view_complementarity_overlap.pdf",
                bbox_inches="tight")
    fig.savefig(output_dir / "view_complementarity_overlap.png",
                dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
