"""Static PNG figures for the main Substack post.

Run: uv run python docs/write-up/main-post-assets/render_figures.py

- model-growth.png: calculations, checks and parts after each goal, read from the data embedded in
  ../stellaris-evolution.html (the evolution viewer).
- steam-vs-brayton.png: the 2,500 MW pair from
  work/orchestration/goals/design-study-whole-plant-conversion/answer.md (Nominal results table and
  "Why the choice changes at plant scale").
"""
import base64
import gzip
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import figure_style as fs  # noqa: E402

fs.use_matplotlib()
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DPI = 220
FIG_W = 7.2  # inches; Substack shows images about 728 px wide


def viewer_frames():
    html = (HERE.parent / "stellaris-evolution.html").read_text()
    blob = re.search(r'<script[^>]*id="evo-data"[^>]*>(.*?)</script>', html, re.S).group(1)
    return json.loads(gzip.decompress(base64.b64decode(blob.strip())))["frames"]


def style_axes(ax):
    ax.set_facecolor(fs.PLATE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color=fs.RULE, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def model_growth():
    frames = viewer_frames()
    goals = list(range(len(frames)))  # 0 is the starting model; 1..28 are goals
    panels = [("calcs", "Calculations"), ("checks", "Engineering checks"), ("parts", "Parts")]
    fig, axes = plt.subplots(1, 3, figsize=(FIG_W, 2.9), sharey=True, layout="constrained")
    for ax, (key, label) in zip(axes, panels):
        values = [f["metrics"][key] for f in frames]
        ax.step(goals, values, where="post", color=fs.ROLE_CALC, linewidth=2)
        ax.plot([goals[0], goals[-1]], [values[0], values[-1]], "o", color=fs.ROLE_CALC, markersize=4.5)
        ax.annotate(f"{values[0]}", (goals[0], values[0]), xytext=(0, 7), textcoords="offset points",
                    ha="left", color=fs.INK, fontsize=fs.LABEL_PT)
        ax.annotate(f"{values[-1]}", (goals[-1], values[-1]), xytext=(0, 7), textcoords="offset points",
                    ha="right", color=fs.INK, fontsize=fs.LABEL_PT, fontweight="semibold")
        ax.set_title(label, loc="left")
        ax.set_xlim(-0.5, goals[-1] + 0.5)
        ax.set_xticks([0, 7, 14, 21, 28])
        ax.set_ylim(0, 225)
        style_axes(ax)
    axes[1].set_xlabel("Goals completed", color=fs.MUTED, fontsize=fs.LABEL_PT)
    fig.suptitle("The Stellaris model over 28 goals", x=0.01, ha="left",
                 fontsize=fs.TITLE_PT, fontweight="semibold")
    fig.savefig(HERE / "model-growth.png", dpi=DPI)
    plt.close(fig)


def steam_vs_brayton():
    # 2,500 MW of reactor heat, USD2025 (answer.md: Nominal results; Why the choice changes at plant scale).
    options = ["Steam", "Helium\nBrayton"]
    colors = [fs.ROLE_CALC, fs.ROLE_CHECK]
    panels = [
        ("Conversion equipment", [2.55, 1.54], "${:.2f}B"),
        ("Electricity sold", [663.97, 285.88], "{:.0f} MW"),
        ("Cost of electricity", [408.16, 875.31], "${:.0f}/MWh"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(FIG_W, 2.9), layout="constrained")
    for ax, (label, values, fmt) in zip(axes, panels):
        bars = ax.bar(options, values, color=colors, width=0.62)
        ax.bar_label(bars, labels=[fmt.format(v) for v in values], padding=3,
                     color=fs.INK, fontsize=fs.LABEL_PT)
        ax.set_title(label, loc="left")
        ax.set_ylim(0, max(values) * 1.22)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        style_axes(ax)
        ax.grid(False)
        ax.tick_params(axis="x", colors=fs.INK, labelsize=fs.LABEL_PT)
    fig.suptitle("Cheaper equipment, more expensive electricity", x=0.01, ha="left",
                 fontsize=fs.TITLE_PT, fontweight="semibold")
    fig.text(0.01, -0.02, "Proof-of-concept model. Same Stellaris-derived reactor at 2,500 MW of heat; 2025 dollars. "
             "Read the direction, not the numbers.", ha="left", va="top", color=fs.MUTED, fontsize=fs.LABEL_PT)
    fig.savefig(HERE / "steam-vs-brayton.png", dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


if __name__ == "__main__":
    model_growth()
    steam_vs_brayton()
