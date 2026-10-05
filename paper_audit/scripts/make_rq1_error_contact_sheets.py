"""Create factual RQ1 error/complementarity contact sheets from Exp18 CSV data.

This script performs validation before writing any output. It does not infer
visual causes of errors and does not modify prediction artifacts.
"""

from __future__ import annotations

import csv
import math
import os
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image


REPO_ROOT = Path(r"D:\Skripsi\Experiment_TA")
SOURCE_CSV = REPO_ROOT / "results" / "final_exp18_complementarity_per_sample.csv"
OUTPUT_DIR = REPO_ROOT / "paper_audit" / "rq1_error_analysis"
SUMMARY_CSV = OUTPUT_DIR / "rq1_error_candidates.csv"

EXPECTED_TOTAL = 220
EXPECTED_COUNTS = {
    # CSV names are retained where they describe the correctness relation.
    "side_only_correct": 13,  # front wrong / side correct
    "front_only_correct": 26,  # front correct / side wrong
    "both_wrong": 17,
}

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

CATEGORY_TITLES = {
    "side_only_correct": "Front wrong / Side correct",
    "front_only_correct": "Front correct / Side wrong",
    "both_wrong": "Both wrong",
}

SUMMARY_FIELDS = [
    "category",
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
    "front_margin",
    "side_margin",
    "confidence_difference",
]


def label_text(value: str) -> str:
    return "Phone Use" if int(value) == 1 else "Safe"


def prediction_text(value: str) -> str:
    return "Phone Use" if int(value) == 1 else "Safe"


def validate_rows(rows: list[dict[str, str]]) -> None:
    if len(rows) != EXPECTED_TOTAL:
        raise RuntimeError(f"Expected N={EXPECTED_TOTAL}, found {len(rows)} rows")

    missing_columns = REQUIRED_COLUMNS - set(rows[0]) if rows else REQUIRED_COLUMNS
    if missing_columns:
        raise RuntimeError(f"Missing required columns: {sorted(missing_columns)}")

    row_indices = [row["row_index"] for row in rows]
    if len(row_indices) != len(set(row_indices)):
        raise RuntimeError("Duplicate row_index detected")

    counts = Counter(row["error_type"] for row in rows)
    all_expected = {"both_correct": 164, **EXPECTED_COUNTS}
    for category, expected in all_expected.items():
        if counts[category] != expected:
            raise RuntimeError(
                f"Category mismatch for {category}: expected {expected}, found {counts[category]}"
            )

    if sum(counts.values()) != EXPECTED_TOTAL:
        raise RuntimeError(f"Category counts do not sum to N={EXPECTED_TOTAL}: {counts}")

    for row in rows:
        front_correct = int(row["front_pred"]) == int(row["label"])
        side_correct = int(row["side_pred"]) == int(row["label"])
        expected_type = (
            "both_correct"
            if front_correct and side_correct
            else "front_only_correct"
            if front_correct
            else "side_only_correct"
            if side_correct
            else "both_wrong"
        )
        if row["error_type"] != expected_type:
            raise RuntimeError(
                f"Prediction/category mismatch at row_index={row['row_index']}: "
                f"CSV={row['error_type']}, derived={expected_type}"
            )

        for key in ("front_prob_phone", "side_prob_phone"):
            probability = float(row[key])
            if not 0.0 <= probability <= 1.0:
                raise RuntimeError(f"Probability out of range in {key}: {probability}")

        for key in ("filepath_front", "filepath_side"):
            if not Path(row[key]).is_file():
                raise RuntimeError(f"Missing image path: {row[key]}")


def sort_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        rows,
        key=lambda row: (
            int(row["subject_id"]),
            int(row["activity_id"]),
            int(row["frame"]),
        ),
    )


def write_summary(rows: list[dict[str, str]]) -> None:
    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        for row in rows:
            front_margin = abs(float(row["front_prob_phone"]) - 0.5)
            side_margin = abs(float(row["side_prob_phone"]) - 0.5)
            output = {field: row.get(field, "") for field in SUMMARY_FIELDS}
            output["category"] = CATEGORY_TITLES[row["error_type"]]
            output["front_margin"] = f"{front_margin:.8f}"
            output["side_margin"] = f"{side_margin:.8f}"
            output["confidence_difference"] = f"{side_margin - front_margin:.8f}"
            writer.writerow(output)


def render_category(category: str, rows: list[dict[str, str]]) -> Path:
    output_pdf = OUTPUT_DIR / {
        "side_only_correct": "front_wrong_side_correct.pdf",
        "front_only_correct": "front_correct_side_wrong.pdf",
        "both_wrong": "both_wrong.pdf",
    }[category]

    per_page = 4
    page_count = math.ceil(len(rows) / per_page)
    with PdfPages(output_pdf) as pdf:
        for page_number in range(page_count):
            page_rows = rows[page_number * per_page : (page_number + 1) * per_page]
            fig = plt.figure(figsize=(8.5, 11.0), facecolor="white")
            fig.subplots_adjust(left=0.07, right=0.93, top=0.875, bottom=0.06)
            fig.suptitle(
                CATEGORY_TITLES[category],
                fontsize=13,
                fontweight="bold",
                y=0.965,
            )
            fig.text(
                0.5,
                0.925,
                f"RQ1 qualitative error audit | all candidates shown | "
                f"page {page_number + 1} of {page_count}",
                ha="center",
                va="top",
                fontsize=8.5,
                color="0.25",
            )

            grid = fig.add_gridspec(
                nrows=4,
                ncols=2,
                hspace=0.83,
                wspace=0.06,
                height_ratios=[1, 1, 1, 1],
            )

            for row_number, row in enumerate(page_rows):
                front_ax = fig.add_subplot(grid[row_number, 0])
                side_ax = fig.add_subplot(grid[row_number, 1])
                front_image = Image.open(row["filepath_front"]).convert("RGB")
                side_image = Image.open(row["filepath_side"]).convert("RGB")
                front_ax.imshow(front_image, aspect="equal")
                side_ax.imshow(side_image, aspect="equal")
                front_ax.set_title(
                    f"Front view\nPred: {prediction_text(row['front_pred'])} | "
                    f"p(phone): {float(row['front_prob_phone']):.3f}",
                    fontsize=8.5,
                    pad=4,
                )
                side_ax.set_title(
                    f"Side view\nPred: {prediction_text(row['side_pred'])} | "
                    f"p(phone): {float(row['side_prob_phone']):.3f}",
                    fontsize=8.5,
                    pad=4,
                )
                for axis in (front_ax, side_ax):
                    axis.set_xticks([])
                    axis.set_yticks([])
                    for spine in axis.spines.values():
                        spine.set_color("0.72")
                        spine.set_linewidth(0.7)

                position = front_ax.get_position()
                side_position = side_ax.get_position()
                metadata = (
                    f"Subject {row['subject_id']} | Activity {row['activity_id']} | "
                    f"Frame {row['frame']} | GT: {label_text(row['label'])}"
                )
                fig.text(
                    (position.x0 + side_position.x1) / 2,
                    min(position.y0, side_position.y0) - 0.038,
                    metadata,
                    ha="center",
                    va="top",
                    fontsize=9,
                    color="0.05",
                )

            pdf.savefig(fig, facecolor="white")
            plt.close(fig)

    return output_pdf


def main() -> None:
    with SOURCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    validate_rows(rows)
    rows = sort_rows(rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    candidate_rows = [row for row in rows if row["error_type"] in EXPECTED_COUNTS]
    if len(candidate_rows) != sum(EXPECTED_COUNTS.values()):
        raise RuntimeError(
            f"Candidate count mismatch: expected {sum(EXPECTED_COUNTS.values())}, "
            f"found {len(candidate_rows)}"
        )
    write_summary(candidate_rows)
    for category in EXPECTED_COUNTS:
        category_rows = [row for row in rows if row["error_type"] == category]
        render_category(category, category_rows)

    print(f"Validated N={len(rows)} rows")
    print("Validated counts:", dict(Counter(row["error_type"] for row in rows)))
    print(f"Wrote summary: {SUMMARY_CSV}")
    for category in EXPECTED_COUNTS:
        output_name = {
            "side_only_correct": "front_wrong_side_correct.pdf",
            "front_only_correct": "front_correct_side_wrong.pdf",
            "both_wrong": "both_wrong.pdf",
        }[category]
        print(f"Wrote PDF: {OUTPUT_DIR / output_name}")


if __name__ == "__main__":
    main()
