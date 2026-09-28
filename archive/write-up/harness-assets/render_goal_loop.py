"""Render the goal-loop figure for the Part 3 harness write-up.

Run: uv run python archive/write-up/harness-assets/render_goal_loop.py
Writes goal-loop.png and goal-loop.svg next to this script.

The figure follows section 2's walk of the outer loop: the goal is written first; a round
opens with an approach, runs tasks one at a time, pins the model at most once and then
runs studies against the pin; the round's record is checked; the owner closes the goal or
the next round opens. Shape: work/orchestration/GOAL_RUNBOOK.md (§ Opening and closing a
round, § Running one task, § The fresh review).
"""
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = Path(__file__).parent
# Palette shared with the Part 2 figures (../sysml-codegen-assets/render_figures.py).
INK = "#152b40"; MUTED = "#52677a"; FAINT = "#b9c5cf"
BLUE = "#2463a5"; TINT = "#edf3fa"; FIXED = "#eef0f2"; TEAL = "#087e83"; GOLD = "#b75f1c"; BG = "#f7f9fc"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "svg.fonttype": "none"})

# Geometry, in inches: the axes span the whole figure, one unit per inch.
FW, FH = 11.6, 6.45
XL = 0.35                                  # the next-round path runs up this line
X0, XE = 0.75, 11.3                        # content band
GOAL_H = 0.6; GOAL_Y = FH - 0.2 - GOAL_H
PAN_H = 2.45; PAN_Y = GOAL_Y - 0.55 - PAN_H
GATE_H = 0.95; GATE_Y = PAN_Y - 0.6 - GATE_H
END_Y = GATE_Y - 0.55                    # where the "goal closed" arrow ends
IN_H = 1.75; IN_Y = PAN_Y + 0.22          # the row of parts inside the round
AP = (X0 + 0.2, 1.65)                      # approach: x, width
TK = (AP[0] + AP[1] + 0.4, 6.1)            # task area, split by the pin
PIN_X = TK[0] + 3.6                        # the pin line, inside the task area
RC = (TK[0] + TK[1] + 0.4, XE - 0.2 - (TK[0] + TK[1] + 0.4))  # round record
OWN = (5.2, 2.3)                           # owner box: x, width

fig = plt.figure(figsize=(FW, FH), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set(xlim=(0, FW), ylim=(0, FH)); ax.axis("off")


def box(x, y, w, h, color, fill="white", lw=1.5, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=fill, ec=color, lw=lw, zorder=z))


def refresh(cx, cy, r, color, lw=2.0):
    """Two clockwise arcs with arrowheads: the task loop inside a round."""
    for start, end in ((165, 25), (345, 205)):
        t = np.radians(np.linspace(start, end, 40))
        xs, ys = cx + r * np.cos(t), cy + r * np.sin(t)
        ax.plot(xs[:-3], ys[:-3], color=color, lw=lw, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch((xs[-6], ys[-6]), (xs[-1], ys[-1]), arrowstyle="-|>",
                                     mutation_scale=11, lw=lw, color=color, shrinkA=0, shrinkB=0))


def arrow(p, q, color=MUTED, lw=1.7):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=17, lw=lw, color=color,
                                 shrinkA=0, shrinkB=0))


def path(points, color, lw=1.7):
    """A polyline whose last segment carries the arrowhead."""
    xs, ys = zip(*points[:-1])
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt")
    arrow(points[-2], points[-1], color, lw)


def titled(x, y, w, h, color, title, body, size=12.5):
    box(x, y, w, h, color)
    ax.text(x + 0.18, y + h - 0.27, title, fontsize=size, weight="bold", color=color, va="center")
    ax.text(x + 0.18, y + h - 0.5, body, fontsize=10.2, color=MUTED, va="top", linespacing=1.4)


def chip(x, y, w, label):
    box(x, y, w, 0.38, BLUE, lw=1.2)
    ax.text(x + w / 2, y + 0.19, label, fontsize=11, ha="center", va="center")


# The goal: written first, fixed while it runs
box(X0, GOAL_Y, XE - X0, GOAL_H, INK)
ax.text(X0 + 0.22, GOAL_Y + GOAL_H / 2, "Goal", fontsize=13.5, weight="bold", va="center")
ax.text(X0 + 0.95, GOAL_Y + GOAL_H / 2, "a question, and what would count as answering it", fontsize=11.5,
        va="center")
ax.text(XE - 0.22, GOAL_Y + GOAL_H / 2, "written first, not changed while it runs", fontsize=11,
        color=MUTED, style="italic", ha="right", va="center")

# One round, drawn from the inside; the cards behind it say that rounds repeat
for k in (2, 1):
    box(X0 + 0.09 * k, PAN_Y + 0.09 * k, XE - X0, PAN_H, FAINT, lw=1.2)
box(X0, PAN_Y, XE - X0, PAN_H, BLUE, lw=1.8)
ax.text(X0 + 0.2, PAN_Y + PAN_H - 0.23, "Round", fontsize=13.5, weight="bold", color=BLUE, va="center")
ax.text(XE - 0.2, PAN_Y + PAN_H - 0.23, "one bounded attempt by the AI", fontsize=11,
        color=MUTED, style="italic", ha="right", va="center")
arrow((AP[0] + AP[1] / 2, GOAL_Y), (AP[0] + AP[1] / 2, IN_Y + IN_H), INK)

titled(AP[0], IN_Y, AP[1], IN_H, BLUE, "Approach", "a bet on how to\nanswer the\nquestion.\nNo task list.")

# Task area: one set of tasks, split by the pin. Before it the model can change; after it
# the model is fixed and studies run against it.
top = IN_Y + IN_H
TX1 = TK[0] + TK[1]
box(TK[0], IN_Y, TK[1], IN_H, TINT, fill=TINT, lw=0)
box(PIN_X, IN_Y, TX1 - PIN_X, IN_H, FIXED, fill=FIXED, lw=0)
ax.add_patch(Rectangle((PIN_X, IN_Y), 0.15, IN_H, fc=FIXED, ec="none"))
box(TK[0], IN_Y, TK[1], IN_H, BLUE, fill="none", lw=1.2)
refresh(TK[0] + 0.4, top - 0.4, 0.2, BLUE)
ax.text(TK[0] + 0.78, top - 0.27, "Tasks, one at a time", fontsize=12.5, weight="bold", color=BLUE, va="center")
ax.text(TK[0] + 0.78, top - 0.52, "each result decides the next task", fontsize=10, color=BLUE,
        style="italic", va="center")
ax.plot([PIN_X, PIN_X], [IN_Y, top], color=INK, lw=1.6)
ax.text(TK[0] + 0.35, IN_Y + 0.74, "research\nmodel changes", fontsize=11.5, va="center", linespacing=1.7)
ax.text(PIN_X + 0.95, IN_Y + 0.74, "studies", fontsize=11.5, va="center")
PW = 1.4
box(PIN_X - PW / 2, IN_Y + 0.5, PW, 0.52, MUTED, lw=1.0, z=3)
ax.text(PIN_X, IN_Y + 0.86, "pin the model", fontsize=10.5, ha="center", va="center", zorder=4)
ax.text(PIN_X, IN_Y + 0.64, "at most once", fontsize=8.8, color=MUTED, ha="center", va="center", zorder=4)
ax.text(TK[0] + 0.18, IN_Y + 0.17, "the model can change", fontsize=10, color=MUTED, va="center")
ax.text(PIN_X + 0.18, IN_Y + 0.17, "the model is fixed", fontsize=10, color=MUTED, va="center")

titled(RC[0], IN_Y, RC[1], IN_H, BLUE, "Record", "what was tried,\nwhat was found,\nwhy it stopped")
mid = IN_Y + IN_H - 0.4                   # the round's flow line, clear of the task chips
arrow((AP[0] + AP[1], mid), (TK[0], mid), BLUE)
arrow((TK[0] + TK[1], mid), (RC[0], mid), BLUE)

# Nothing builds on a round until someone who did not do the work has reviewed it
gm = GATE_Y + GATE_H / 2
box(RC[0], GATE_Y, RC[1], GATE_H, TEAL)
ax.text(RC[0] + RC[1] / 2, GATE_Y + GATE_H - 0.27, "Review", fontsize=12.5, weight="bold",
        color=TEAL, ha="center", va="center")
ax.text(RC[0] + RC[1] / 2, GATE_Y + 0.32, "by someone who did\nnot do the work", fontsize=9.8,
        color=MUTED, ha="center", va="center", linespacing=1.3)
arrow((RC[0] + RC[1] / 2, IN_Y), (RC[0] + RC[1] / 2, GATE_Y + GATE_H))

box(OWN[0], GATE_Y, OWN[1], GATE_H, GOLD)
ax.text(OWN[0] + OWN[1] / 2, GATE_Y + GATE_H - 0.27, "Owner", fontsize=12.5, weight="bold", color=GOLD,
        ha="center", va="center")
ax.text(OWN[0] + OWN[1] / 2, GATE_Y + 0.3, "is the goal answered?", fontsize=10, color=MUTED,
        ha="center", va="center")
arrow((RC[0], gm), (OWN[0] + OWN[1], gm))

# Not yet: the next round, with a revised approach. Yes: the goal closes.
path([(OWN[0], gm), (XL, gm), (XL, mid), (AP[0], mid)], BLUE)
ax.text((XL + OWN[0]) / 2, gm + 0.08, "not yet: next round,\nrevised approach",
        fontsize=10, color=BLUE, style="italic", ha="center", va="bottom", linespacing=1.3)
arrow((OWN[0] + OWN[1] / 2, GATE_Y), (OWN[0] + OWN[1] / 2, END_Y), INK)
ax.text(OWN[0] + OWN[1] / 2 + 0.12, (GATE_Y + END_Y) / 2, "yes", fontsize=10, color=INK, style="italic", va="center")
ax.text(OWN[0] + OWN[1] / 2, END_Y - 0.22, "Goal closed", fontsize=12.5, weight="bold", ha="center", va="center")

fig.savefig(OUT / "goal-loop.png", dpi=170, facecolor=BG)
fig.savefig(OUT / "goal-loop.svg", facecolor=BG)
