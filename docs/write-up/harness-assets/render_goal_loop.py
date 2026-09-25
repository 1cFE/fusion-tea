"""Render the goal-loop figure for the Part 3 harness write-up.

Run: uv run python docs/write-up/harness-assets/render_goal_loop.py
Writes goal-loop.png and goal-loop.svg next to this script.

The figure carries only the section 2 mental model: a fixed question at the top,
one round drawn from the inside in the middle, and the check and owner decision
every round passes through before the next one opens. Shape:
work/orchestration/GOAL_RUNBOOK.md (§ Opening and closing a round, § Running one
task, § The fresh review). The example line cites the two rounds of
work/orchestration/goals/stored-energy-basis/trail.md.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent
# Palette shared with the Part 2 figures (../sysml-codegen-assets/render_figures.py).
INK = "#152b40"; MUTED = "#52677a"; FAINT = "#b9c5cf"
BLUE = "#2463a5"; TINT = "#edf3fa"; TEAL = "#087e83"; GOLD = "#b75f1c"; BG = "#f7f9fc"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "svg.fonttype": "none"})

# Geometry, in inches: the axes span the whole figure, one unit per inch.
FW, FH = 12.2, 7.7
X0, XE = 2.85, 11.95                     # content band, right of the tier labels
XL = 2.5                                 # the return path runs down this line
GOAL_H = 0.85; GOAL_Y = FH - 0.8 - GOAL_H
PAN_H = 2.55; PAN_Y = GOAL_Y - 0.55 - PAN_H
GATE_H = 0.9; GATE_Y = PAN_Y - 0.55 - GATE_H
END_H = 0.6; END_Y = GATE_Y - 0.5 - END_H
IN_H = 1.5; IN_Y = PAN_Y + 0.5          # the three parts inside the round
AP = (X0 + 0.25, 2.3)                    # approach box: x, width
TK = (AP[0] + AP[1] + 0.35, 3.75)        # tasks area
RC = (TK[0] + TK[1] + 0.35, XE - 0.25 - (TK[0] + TK[1] + 0.35))  # round record
OWN = (6.2, 2.4)                         # owner box: x, width

fig = plt.figure(figsize=(FW, FH), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set(xlim=(0, FW), ylim=(0, FH)); ax.axis("off")


def box(x, y, w, h, color, fill="white", lw=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.09",
                                fc=fill, ec=color, lw=lw))


def arrow(p, q, color=MUTED, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=17, lw=1.7, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def path(points, color):
    """A polyline whose last segment carries the arrowhead."""
    xs, ys = zip(*points[:-1])
    ax.plot(xs, ys, color=color, lw=1.7, solid_capstyle="butt")
    arrow(points[-2], points[-1], color)


def titled(x, y, w, h, color, title, body, fill="white"):
    box(x, y, w, h, color, fill)
    ax.text(x + 0.2, y + h - 0.27, title, fontsize=13, weight="bold", color=color, va="center")
    ax.text(x + 0.2, y + h - 0.52, body, fontsize=10.3, color=MUTED, va="top", linespacing=1.4)


def tier(top, name, note):
    """Tier label in the left gutter, aligned with the header line of its boxes."""
    ax.text(0.3, top - 0.27, name, fontsize=14, weight="bold", va="center")
    ax.text(0.3, top - 0.5, note, fontsize=10.5, color=MUTED, va="top", linespacing=1.4)


ax.text(0.3, FH - 0.4, "One question, pursued in checked rounds", fontsize=21, weight="bold", va="center")

tier(GOAL_Y + GOAL_H, "QUESTION", "fixed for the\nwhole goal")
tier(PAN_Y + PAN_H, "ROUNDS", "bounded attempts\nby the AI: at most\none model change\nand one study each")
tier(GATE_Y + GATE_H, "CHECKS", "nothing builds on\na round until it\nhas been checked")

# The goal
box(X0, GOAL_Y, XE - X0, GOAL_H, INK)
ax.text(X0 + 0.25, GOAL_Y + GOAL_H - 0.28, "The goal: a question with a defined answer",
        fontsize=14, weight="bold", va="center")
ax.text(X0 + 0.25, GOAL_Y + 0.25,
        "What we want to know, what counts as answered, the effort allowed, and the calls the owner keeps.",
        fontsize=11, color=MUTED, va="center")

# One round, drawn from the inside; the cards behind it say that rounds repeat
for k in (2, 1):
    box(X0 + 0.09 * k, PAN_Y + 0.09 * k, XE - X0, PAN_H, FAINT, lw=1.2)
box(X0, PAN_Y, XE - X0, PAN_H, BLUE, lw=1.8)
ax.text(X0 + 0.25, PAN_Y + PAN_H - 0.25, "Round N", fontsize=14, weight="bold", color=BLUE, va="center")
arrow((AP[0] + AP[1] / 2 + 0.3, GOAL_Y), (AP[0] + AP[1] / 2 + 0.3, IN_Y + IN_H), INK)

titled(AP[0], IN_Y, AP[1], IN_H, BLUE, "Approach",
       "a bet on how to answer:\nwhat we'll try, what we\nassume, what would make\nus drop it. No task list.")

box(TK[0], IN_Y, TK[1], IN_H, TINT, fill=TINT)
tx = TK[0] + 0.2
ax.text(tx, IN_Y + IN_H - 0.27, "Tasks, one at a time", fontsize=13, weight="bold", color=BLUE, va="center")
chips = [("research", 0.98), ("model change", 1.3), ("study", 0.72)]
CG = 0.12
cy, ch = IN_Y + IN_H - 0.85, 0.36
x = TK[0] + (TK[1] - sum(w for _, w in chips) - CG * (len(chips) - 1)) / 2
centers = []
for label, w in chips:
    box(x, cy, w, ch, BLUE, lw=1.2)
    ax.text(x + w / 2, cy + ch / 2, label, fontsize=11, ha="center", va="center")
    centers.append(x + w / 2)
    x += w + CG
loop_y = cy - 0.2
path([(centers[-1], cy), (centers[-1], loop_y), (centers[0], loop_y), (centers[0], cy)], BLUE)
ax.text(TK[0] + TK[1] / 2, IN_Y + 0.17, "the next task depends on what the last one found", fontsize=9.8,
        color=BLUE, style="italic", ha="center", va="center")

titled(RC[0], IN_Y, RC[1], IN_H, BLUE, "Round record",
       "what was tried, what\nwas found, and why\nthe round stopped")

mid = IN_Y + IN_H / 2
arrow((AP[0] + AP[1], mid), (TK[0], mid), BLUE)
arrow((TK[0] + TK[1], mid), (RC[0], mid), BLUE)
ax.text(X0 + 0.25, PAN_Y + 0.24,
        "In section 4, round 1 ran one research task. Round 2 made one model change, then ran one study.",
        fontsize=9.8, color=MUTED, style="italic", va="center")

# Checks: the record goes to a fresh review, then to the owner
gm = GATE_Y + GATE_H / 2
box(RC[0], GATE_Y, RC[1], GATE_H, TEAL)
ax.text(RC[0] + RC[1] / 2, GATE_Y + GATE_H - 0.27, "✓ Fresh review", fontsize=12.5, weight="bold",
        color=TEAL, ha="center", va="center")
ax.text(RC[0] + RC[1] / 2, GATE_Y + 0.3, "by someone who did\nnot do the work", fontsize=10, color=MUTED,
        ha="center", va="center", linespacing=1.3)
arrow((RC[0] + RC[1] / 2, PAN_Y), (RC[0] + RC[1] / 2, GATE_Y + GATE_H))

box(OWN[0], GATE_Y, OWN[1], GATE_H, GOLD)
ax.text(OWN[0] + OWN[1] / 2, GATE_Y + GATE_H - 0.27, "Owner", fontsize=12.5, weight="bold", color=GOLD,
        ha="center", va="center")
ax.text(OWN[0] + OWN[1] / 2, GATE_Y + 0.28, "is the goal answered?", fontsize=10, color=MUTED,
        ha="center", va="center")
arrow((RC[0], gm), (OWN[0] + OWN[1], gm))

# Not yet: back to a revised approach. Answered: the goal closes.
path([(OWN[0], gm), (XL, gm), (XL, mid), (AP[0], mid)], BLUE)
ax.text((XL + OWN[0]) / 2 + 0.1, gm + 0.08, "not yet: next round,\nwith a revised approach", fontsize=10,
        color=BLUE, style="italic", ha="center", va="bottom", linespacing=1.3)
box(OWN[0], END_Y, OWN[1], END_H, INK, fill="#eef2f6")
ax.text(OWN[0] + OWN[1] / 2, END_Y + END_H / 2, "Goal closed", fontsize=12.5, weight="bold",
        ha="center", va="center")
arrow((OWN[0] + OWN[1] / 2, GATE_Y), (OWN[0] + OWN[1] / 2, END_Y + END_H), INK)
ax.text(OWN[0] + OWN[1] / 2 + 0.12, (GATE_Y + END_Y + END_H) / 2, "yes", fontsize=10, color=INK,
        style="italic", va="center")

fig.savefig(OUT / "goal-loop.png", dpi=170, facecolor=BG)
fig.savefig(OUT / "goal-loop.svg", facecolor=BG)
