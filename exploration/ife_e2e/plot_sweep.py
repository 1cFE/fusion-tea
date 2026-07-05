"""WI-015 feasible-region figures from the sweep CSV.

Figure 1 (ife_viability_eta_gain.png): eta-G plane at f=5 Hz. LCOE contours
over the power-positive region, the eta*G=10 viability knee (DI-001), the
P_net=0 boundary, and the $100/MWh overlay.

Figure 2 (ife_viability_by_freq.png): the same classification map as small
multiples over rep rate f — shows the feasible region growing with f.

Run:  uv run python exploration/ife_e2e/plot_sweep.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).parent.parent.parent
OUT = REPO / "data/ife_sweep"

df = pd.read_csv(OUT / "sweep_results.csv")
ETA = np.sort(df["eta"].unique())
G = np.sort(df["gain"].unique())
FREQS = np.sort(df["frequency_hz"].unique())

ETA_TH, M = 0.40, 1.2  # baseline thermal efficiency, blanket multiple


def grids(f_hz: float):
    sub = df[df["frequency_hz"] == f_hz].sort_values(["eta", "gain"])
    lcoe = sub.pivot(index="gain", columns="eta", values="lcoe_per_mwh").values
    return lcoe  # shape (len(G), len(ETA))


def draw_boundaries(ax, label=True):
    eta_line = np.linspace(ETA.min(), ETA.max(), 400)
    ax.plot(eta_line, 10.0 / eta_line, "k-", lw=2,
            label=r"$\eta G = 10$ viability knee (DI-001)" if label else None)
    ax.plot(eta_line, 2.0 / (ETA_TH * M * eta_line), "k--", lw=1.5,
            label=r"$P_{net} = 0$" if label else None)
    ax.set_ylim(G.min(), G.max())
    ax.set_xlim(ETA.min(), ETA.max())


# --- Figure 1: f = 5 Hz ----------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6.5))
lcoe = grids(5.0)
levels = [40, 60, 80, 100, 150, 250, 500, 1000]
cf = ax.contourf(ETA, G, lcoe, levels=levels, cmap="viridis_r", extend="both")
c100 = ax.contour(ETA, G, lcoe, levels=[100.0], colors="crimson", linewidths=2)
ax.clabel(c100, fmt="$%.0f/MWh")
draw_boundaries(ax)

# hatch the non-viable region (eta*G <= 10)
EE, GG = np.meshgrid(ETA, G)
ax.contourf(ETA, G, (EE * GG <= 10).astype(float), levels=[0.5, 1.5],
            colors="none", hatches=["///"])

# anchor B marker
ax.plot(0.25, 100, "w*", ms=16, mec="black", label="Anchor B: $68.69/MWh")

ax.set_xlabel(r"Driver efficiency $\eta$")
ax.set_ylabel("Target gain $G$")
ax.set_title("IFE viability map at f = 5 Hz (generated pipeline, Hawker LCOE)\n"
             "hatched: non-viable ($\\eta G \\leq 10$); red: \\$100/MWh overlay")
fig.colorbar(cf, ax=ax, label="LCOE [$/MWh]")
ax.legend(loc="upper right", framealpha=0.9)
fig.tight_layout()
fig.savefig(OUT / "ife_viability_eta_gain.png", dpi=150)
print("wrote", OUT / "ife_viability_eta_gain.png")

# --- Figure 2: small multiples over f ---------------------------------------
fig2, axes = plt.subplots(1, len(FREQS), figsize=(4 * len(FREQS), 4.2),
                          sharey=True)
for ax, f_hz in zip(axes, FREQS):
    lcoe = grids(f_hz)
    cf = ax.contourf(ETA, G, lcoe, levels=levels, cmap="viridis_r",
                     extend="both")
    ax.contour(ETA, G, lcoe, levels=[100.0], colors="crimson", linewidths=1.5)
    ax.contourf(ETA, G, (EE * GG <= 10).astype(float), levels=[0.5, 1.5],
                colors="none", hatches=["///"])
    draw_boundaries(ax, label=False)
    sub = df[df["frequency_hz"] == f_hz]
    pct = 100 * sub["attractive"].sum() / len(sub)
    ax.set_title(f"f = {f_hz:g} Hz\nattractive: {pct:.0f}%")
    ax.set_xlabel(r"$\eta$")
axes[0].set_ylabel("Target gain $G$")
fig2.suptitle("Feasible region vs rep rate (hatched: $\\eta G \\leq 10$; "
              "red: \\$100/MWh)", y=1.02)
fig2.colorbar(cf, ax=axes, label="LCOE [$/MWh]", fraction=0.02)
fig2.savefig(OUT / "ife_viability_by_freq.png", dpi=150, bbox_inches="tight")
print("wrote", OUT / "ife_viability_by_freq.png")
