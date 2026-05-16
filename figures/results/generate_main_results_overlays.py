# pyright: reportMissingImports=false
"""Generate the dynamic Main Results plot overlays.

Run from the repository root with:
uv run --with matplotlib --with SciencePlots python figures/results/generate_main_results_overlays.py
"""

from pathlib import Path

import matplotlib  # type: ignore[import-not-found]

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # type: ignore[import-not-found]
import scienceplots  # type: ignore[import-not-found] # noqa: F401 - registers SciencePlots styles


DAYS = list(range(14))

# Values reconstructed from the vector data in the paper figure
# daily_results_alternatives.pdf. The original figure is kept untouched.
ORACLE = [0.990, 0.940, 0.943, 0.936, 0.998, 0.937, 0.949, 0.930, 0.957, 0.956, 0.956, 0.979, 0.975, 0.967]
OVERALL = [0.979, 0.796, 0.814, 0.725, 0.978, 0.778, 0.588, 0.452, 0.727, 0.927, 0.888, 0.798, 0.807, 0.069]
DEFAULT = [0.974, 0.819, 0.860, 0.764, 0.996, 0.764, 0.694, 0.666, 0.733, 0.821, 0.817, 0.914, 0.907, 0.076]
SAMPLE = [0.496, 0.483, 0.536, 0.468, 0.885, 0.639, 0.653, 0.437, 0.837, 0.901, 0.850, 0.863, 0.896, 0.340]
AGGREGATE_SCORE = 0.95

COLORS = {
    "oracle": "#d64a6b",
    "overall": "#2ca02c",
    "default": "#e68613",
    "sample": "#1f77b4",
    "muted": "#8a8f98",
    "risk": "#c0392b",
}

SERIES = {
    "overall": (OVERALL, "Overall", "s", COLORS["overall"]),
    "default": (DEFAULT, "Default", "X", COLORS["default"]),
    "sample": (SAMPLE, "10% sample", "^", COLORS["sample"]),
}

STAGE_TITLES = {
    1: "Reference: daily BO oracle stays high",
    2: "One-size configuration: high aggregate, unstable days",
    3: "Default settings: good only on a few easy days",
    4: "10% sample BO: cheaper, but still unstable",
    5: "Deployment view: day-level failures are visible",
}


def setup_style() -> None:
    plt.style.use(["science", "no-latex", "bright"])
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 13,
            "axes.labelsize": 15,
            "axes.titlesize": 16,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "lines.linewidth": 3.0,
            "lines.markersize": 7.0,
            "axes.linewidth": 1.1,
            "grid.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.bbox": "standard",
            "savefig.pad_inches": 0.0,
        }
    )


def draw_series(ax, values, marker, color, *, muted=False):
    ax.plot(
        DAYS,
        values,
        color=COLORS["muted"] if muted else color,
        marker=marker,
        linewidth=1.8 if muted else 3.0,
        markersize=5.0 if muted else 7.5,
        alpha=0.28 if muted else 1.0,
        zorder=2 if muted else 4,
    )


def label_box(ax, x, y, text, color, *, ha="left"):
    ax.text(
        x,
        y,
        text,
        color=color,
        fontsize=11,
        fontweight="bold",
        ha=ha,
        va="center",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": color, "alpha": 0.92},
        zorder=10,
    )


def mark_risky_days(ax) -> None:
    for day in [0, 1, 2, 3, 7, 13]:
        ax.axvspan(day - 0.34, day + 0.34, color=COLORS["risk"], alpha=0.08, lw=0, zorder=0)
    ax.text(
        0.18,
        0.13,
        "risk days",
        color=COLORS["risk"],
        fontsize=11,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=8,
    )


def annotate(ax, text, xy, xytext, color) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        color=color,
        fontsize=12,
        fontweight="bold",
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.8},
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": color, "alpha": 0.9},
    )


def make_overlay(stage: int, output_path: Path) -> None:
    setup_style()
    fig, ax = plt.subplots(figsize=(8.8, 4.7))

    ax.set_facecolor("#fbfbfb")
    ax.set_xlim(-0.45, 13.65)
    ax.set_ylim(0.0, 1.04)
    ax.set_xticks(DAYS)
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 0.95, 1.0])
    ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "0.95", "1.0"])
    ax.set_xlabel("Day")
    ax.set_ylabel("Robustness score")
    ax.grid(True, axis="y", color="#d4d4d4", alpha=0.9)
    ax.grid(True, axis="x", color="#ececec", alpha=0.8)

    if stage == 5:
        mark_risky_days(ax)

    ax.axhline(
        AGGREGATE_SCORE,
        color="black",
        linestyle=(0, (6, 4)),
        linewidth=2.2,
        alpha=0.88,
        zorder=1,
    )
    ax.text(
        5.15,
        0.865,
        "aggregate 0.95",
        color="black",
        fontsize=10.5,
        fontweight="bold",
        ha="left",
        va="center",
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "black", "alpha": 0.86},
        zorder=9,
    )

    draw_series(ax, ORACLE, "o", COLORS["oracle"], muted=False)
    label_box(ax, 13.48, 1.015, "Daily BO oracle", COLORS["oracle"], ha="right")

    if stage >= 2:
        draw_series(ax, OVERALL, "s", COLORS["overall"], muted=False)
        label_box(ax, 13.48, 0.815, "Overall", COLORS["overall"], ha="right")

    if stage >= 3:
        draw_series(ax, DEFAULT, "X", COLORS["default"], muted=False)
        label_box(ax, 13.48, 0.715, "Default", COLORS["default"], ha="right")

    if stage >= 4:
        draw_series(ax, SAMPLE, "^", COLORS["sample"], muted=False)
        label_box(ax, 13.48, 0.555, "10% sample", COLORS["sample"], ha="right")

    if stage == 2:
        annotate(
            ax,
            "daily losses hidden\nby the aggregate",
            xy=(7, OVERALL[7]),
            xytext=(4.15, 0.28),
            color=COLORS["overall"],
        )
    elif stage == 3:
        annotate(
            ax,
            "near-zero on D13",
            xy=(13, DEFAULT[13]),
            xytext=(8.7, 0.23),
            color=COLORS["default"],
        )
    elif stage == 4:
        annotate(
            ax,
            "low on D0-D3, D7, D13",
            xy=(2, SAMPLE[2]),
            xytext=(0.7, 0.28),
            color=COLORS["sample"],
        )
    elif stage == 5:
        annotate(
            ax,
            "same days, different costs",
            xy=(7, 0.46),
            xytext=(3.9, 0.18),
            color=COLORS["risk"],
        )

    ax.text(
        0.01,
        1.035,
        STAGE_TITLES[stage],
        transform=ax.transAxes,
        color="#1f2933",
        fontsize=15,
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    fig.subplots_adjust(left=0.095, right=0.985, bottom=0.145, top=0.87)
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    output_dir = Path(__file__).resolve().with_name("main_results_overlays")
    output_dir.mkdir(parents=True, exist_ok=True)
    for stage in range(1, 6):
        make_overlay(stage, output_dir / f"main_results_overlay_{stage}.pdf")


if __name__ == "__main__":
    main()
