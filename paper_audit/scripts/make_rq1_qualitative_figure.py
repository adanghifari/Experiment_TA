"""Render the locked representative paired examples for RQ1.

The script is deterministic and validates every selected row against the
authoritative per-sample CSV before rendering. It does not modify the CSV or
the source images.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


REPO_ROOT = Path(r"D:\Skripsi\Experiment_TA")
SOURCE_CSV = REPO_ROOT / "results" / "final_exp18_complementarity_per_sample.csv"
OUTPUT_DIR = REPO_ROOT / "paper_audit" / "figures"
OUTPUT_PDF = OUTPUT_DIR / "rq1_qualitative_examples.pdf"
OUTPUT_PNG = OUTPUT_DIR / "rq1_qualitative_examples.png"

REQUIRED_COLUMNS = {
    "row_index",
    "subject_id",
    "activity_id",
    "frame",
    "label",
    "front_pred",
    "side_pred",
    "front_prob_phone",
    "side_prob_phone",
    "filepath_front",
    "filepath_side",
    "error_type",
}

# The probabilities supplied by the audit brief are display-rounded values.
# The CSV remains authoritative; validation compares the CSV values rounded to
# three decimals with these audit values and uses the full CSV values to draw.
LOCKED_CASES = (
    {
        "case": "A",
        "row_label": "(a) Side helps",
        "subject_id": 17,
        "activity_id": 8,
        "frame": 91,
        "label": 1,
        "front_pred": 0,
        "side_pred": 1,
        "front_prob_phone": 0.390,
        "side_prob_phone": 0.716,
        "error_type": "side_only_correct",
    },
    {
        "case": "B",
        "row_label": "(b) Front helps",
        "subject_id": 42,
        "activity_id": 9,
        "frame": 61,
        "label": 1,
        "front_pred": 1,
        "side_pred": 0,
        "front_prob_phone": 0.956,
        "side_prob_phone": 0.493,
        "error_type": "front_only_correct",
    },
    {
        "case": "C",
        "row_label": "(c) Both fail",
        "subject_id": 11,
        "activity_id": 1,
        "frame": 91,
        "label": 0,
        "front_pred": 1,
        "side_pred": 1,
        "front_prob_phone": 0.822,
        "side_prob_phone": 0.718,
        "error_type": "both_wrong",
    },
)


def class_name(value: str | int) -> str:
    return "Phone Use" if int(value) == 1 else "Safe"


def read_and_validate() -> list[dict[str, str]]:
    with SOURCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise RuntimeError(f"CSV is empty: {SOURCE_CSV}")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise RuntimeError(f"Missing required CSV columns: {sorted(missing)}")

    selected: list[dict[str, str]] = []
    for expected in LOCKED_CASES:
        matches = [
            row
            for row in rows
            if int(row["subject_id"]) == expected["subject_id"]
            and int(row["activity_id"]) == expected["activity_id"]
            and int(row["frame"]) == expected["frame"]
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"Case {expected['case']} key is not unique: "
                f"expected 1 match, found {len(matches)}"
            )
        row = matches[0]

        for key in ("label", "front_pred", "side_pred"):
            actual = int(row[key])
            if actual != expected[key]:
                raise RuntimeError(
                    f"Case {expected['case']} mismatch for {key}: "
                    f"CSV={actual}, expected={expected[key]}"
                )
        for key in ("front_prob_phone", "side_prob_phone"):
            actual = float(row[key])
            if f"{actual:.3f}" != f"{expected[key]:.3f}":
                raise RuntimeError(
                    f"Case {expected['case']} mismatch for {key}: "
                    f"CSV={actual:.9f}, expected_display={expected[key]:.3f}"
                )
        if row["error_type"] != expected["error_type"]:
            raise RuntimeError(
                f"Case {expected['case']} mismatch for error_type: "
                f"CSV={row['error_type']}, expected={expected['error_type']}"
            )
        for key in ("filepath_front", "filepath_side"):
            image_path = Path(row[key])
            if not image_path.is_file():
                raise RuntimeError(
                    f"Case {expected['case']} image does not exist: {image_path}"
                )
            try:
                with Image.open(image_path) as image:
                    if image.width <= 0 or image.height <= 0:
                        raise RuntimeError(f"Invalid image dimensions: {image_path}")
            except Exception as exc:
                raise RuntimeError(f"Cannot read image {image_path}: {exc}") from exc

        selected.append({**row, "case": expected["case"], "row_label": expected["row_label"]})

    return selected


def render(selected: list[dict[str, str]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Approximately IEEE single-column width. Each case occupies one column;
    # Front and Side are arranged as the two image rows. The source images
    # retain their 4:3 aspect ratio.
    fig = plt.figure(figsize=(3.40, 2.75), dpi=600, facecolor="white")
    grid = fig.add_gridspec(
        nrows=3,
        ncols=3,
        left=0.105,
        right=0.995,
        top=0.900,
        bottom=0.105,
        height_ratios=[0.38, 1, 1],
        hspace=0.36,
        wspace=0.085,
    )

    # Case labels and one GT label per column.
    for column, (case, expected) in enumerate(zip(selected, LOCKED_CASES)):
        header_ax = fig.add_subplot(grid[0, column])
        header_ax.axis("off")
        header_ax.text(
            0.5,
            0.5,
            f"{expected['row_label']}\nGT: {class_name(case['label'])}",
            ha="center",
            va="center",
            fontsize=6.0,
            color="0.08",
            linespacing=1.12,
        )

    # Each view is a row; the row labels make the orientation explicit.
    front_axes = []
    side_axes = []
    for column, case in enumerate(selected):
        for row_number, path_key, pred_key, prob_key, axes_list in (
            (1, "filepath_front", "front_pred", "front_prob_phone", front_axes),
            (2, "filepath_side", "side_pred", "side_prob_phone", side_axes),
        ):
            ax = fig.add_subplot(grid[row_number, column])
            axes_list.append(ax)
            with Image.open(case[path_key]) as image:
                ax.imshow(image.convert("RGB"), aspect="equal")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("0.55")
                spine.set_linewidth(0.55)
            ax.text(
                0.5,
                -0.085,
                f"Pred: {class_name(case[pred_key])}\n"
                f"p(phone)={float(case[prob_key]):.3f}",
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontsize=5.25,
                color="0.08",
                linespacing=1.08,
            )

    front_position = front_axes[0].get_position()
    side_position = side_axes[0].get_position()
    fig.text(
        0.055,
        (front_position.y0 + front_position.y1) / 2,
        "Front view",
        ha="center",
        va="center",
        fontsize=5.8,
        color="0.08",
        rotation=90,
    )
    fig.text(
        0.055,
        (side_position.y0 + side_position.y1) / 2,
        "Side view",
        ha="center",
        va="center",
        fontsize=5.8,
        color="0.08",
        rotation=90,
    )

    fig.savefig(
        OUTPUT_PDF,
        format="pdf",
        facecolor="white",
        metadata={
            "Creator": "make_rq1_qualitative_figure.py",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(OUTPUT_PNG, format="png", dpi=600, facecolor="white")
    plt.close(fig)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    selected = read_and_validate()
    render(selected)
    print(f"Validated source CSV: {SOURCE_CSV}")
    for case, row in zip(LOCKED_CASES, selected):
        print(
            f"Case {case['case']}: row_index={row['row_index']}; "
            f"subject={row['subject_id']}; activity={row['activity_id']}; frame={row['frame']}; "
            f"label={class_name(row['label'])}; front_pred={class_name(row['front_pred'])}; "
            f"side_pred={class_name(row['side_pred'])}; "
            f"front_prob_phone={float(row['front_prob_phone']):.9f}; "
            f"side_prob_phone={float(row['side_prob_phone']):.9f}; "
            f"error_type={row['error_type']}"
        )
        print(f"  filepath_front={row['filepath_front']}")
        print(f"  filepath_side={row['filepath_side']}")
    print(f"Wrote PDF: {OUTPUT_PDF}")
    print(f"Wrote PNG: {OUTPUT_PNG}")
    print(f"PNG SHA256: {sha256(OUTPUT_PNG)}")
    print(f"PDF SHA256: {sha256(OUTPUT_PDF)}")


if __name__ == "__main__":
    main()
