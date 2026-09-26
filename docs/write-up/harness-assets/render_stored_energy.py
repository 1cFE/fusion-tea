"""Render the stored-energy figure for the HTML page of the Part 3 harness write-up.

Run: uv run python docs/write-up/harness-assets/render_stored_energy.py
Writes stored-energy.svg and stored-energy.png next to this script. The page embeds the SVG inline.

The figure puts the stored-energy values of the stored-energy-basis goal on one axis: the paper's above
the line, the model's below it. Every value is stated in ../harness.md section 4; the records behind them
are in work/orchestration/goals/stored-energy-basis/trail.md:
  504.65 MJ  printed in the Stellaris paper (Table 5)
  518.3 MJ   the paper's own rules on its printed peaks (T-001 return, round 1)
  527-575 MJ readings of the paper's plotted profiles and printed peaks; 567 MJ implied by its printed beta
             (Grounding, 2026-09-04)
  551 MJ     the model before WI-042 (Grounding; 551.4 at the pin in ../harness.md section 6)
  519.9 MJ   the model after WI-042 (T-002 return, round 2: 519.914)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

import figure_style as fs  # noqa: E402

fs.use_matplotlib()
plt.rcParams["svg.hashsalt"] = "stored-energy"

# Drawn at the plate's full width, so the page shows it at its drawn size; on a narrow screen the page keeps
# it at a readable minimum width and scrolls it sideways instead of shrinking it.
W_IN, H_IN = fs.WIDE_IN, 2.7
X0, X1 = 489.0, 583.0          # data range; the row names sit just left of the axis, which starts at AX0
AX0 = 497.5
BAND = "#e5e1db"               # --band in write-up.css
T = fs.TEXT_PT                 # one text size throughout, so nothing drops below it when the page scrolls it

fig = plt.figure(figsize=(W_IN, H_IN))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set(xlim=(X0, X1), ylim=(-1.3, 1.75))
ax.axis("off")

# The axis: stored energy in MJ. Ticks every 10 MJ; only the ends are numbered, because every value carries its
# own label and the model's stems would cross numbered ticks at 520 and 550.
ax.plot([AX0, X1 - 0.5], [0, 0], color=fs.EDGE, lw=1.1, solid_capstyle="butt")
for v in range(500, 590, 10):
    ax.plot([v, v], [-0.07, 0.07], color=fs.EDGE, lw=1.0)
for v in (500, 580):
    ax.text(v, -0.2, f"{v} MJ", ha="center", va="top", fontsize=T, color=fs.MUTED)

# Row names, beside their rows: the paper's values above the axis, the model's below.
ax.text(X0 + 0.3, 0.73, "The paper", ha="left", va="center", fontsize=T, weight="semibold", color=fs.INK)
ax.text(X0 + 0.3, -0.84, "The model", ha="left", va="center", fontsize=T, weight="semibold", color=fs.ROLE_CALC)


def paper_point(v, label, dy=0.55):
    ax.plot([v, v], [0, dy - 0.12], color=fs.INK, lw=1.2)
    ax.plot([v], [0], marker="o", ms=5.5, color=fs.INK, zorder=3)
    ax.text(v, dy, label, ha="center", va="bottom", fontsize=T, color=fs.INK, linespacing=1.25)


# The paper's values, above the line.
paper_point(504.65, "printed\n504.65")
paper_point(518.3, "its own rules\n518.3")
paper_point(567.0, "implied by\nits beta, 567")
ax.add_patch(Rectangle((527, 1.22), 575 - 527, 0.16, fc=BAND, ec=fs.EDGE, lw=0.9))
ax.text((527 + 575) / 2, 1.45, "readings of its plotted profiles and printed peaks, 527–575", ha="center",
        va="bottom", fontsize=T, color=fs.INK)

# The model's values, below the line, with the fix as an arrow from before to after.
for v, label, filled in ((551.0, "before the fix\n551", False), (519.9, "after the fix\n519.9", True)):
    ax.plot([v, v], [0, -0.52], color=fs.ROLE_CALC, lw=1.2)
    ax.plot([v], [0], marker="o", ms=6, mew=1.4, color=fs.ROLE_CALC,
            mfc=fs.ROLE_CALC if filled else fs.PLATE, zorder=4)
    ax.text(v, -0.62, label, ha="center", va="top", fontsize=T, color=fs.ROLE_CALC, linespacing=1.25)
ax.add_patch(FancyArrowPatch((548.0, -0.93), (523.6, -0.93), arrowstyle="-|>", mutation_scale=12, lw=1.2,
                             color=fs.ROLE_CALC, shrinkA=0, shrinkB=0))

meta = {"Date": None, "Creator": None}
fig.savefig(HERE / "stored-energy.svg", facecolor=fs.PLATE, metadata=meta)
fig.savefig(HERE / "stored-energy.png", dpi=170, facecolor=fs.PLATE)
