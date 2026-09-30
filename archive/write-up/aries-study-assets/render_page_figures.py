"""Render the charts of the HTML page for the ARIES write-up, in the page's fonts, and inline them into the page.

Run from the repository root: uv run python archive/write-up/aries-study-assets/render_page_figures.py

Writes page-*.svg next to this script, then refreshes each copy inside ../aries-model-transfer-outline.html between
its <!-- inline:NAME --> and <!-- /inline:NAME --> markers. Every value is read from a committed study or goal record
(named per figure below); nothing is evaluated here and no point is interpolated. The markdown's own figures
(parameter-*.png, architecture-nominal-pair.png, render_parameters.py, render_architecture.py) are left untouched.
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAGE = HERE.parent / "aries-model-transfer-outline.html"
sys.path.insert(0, str(HERE.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

import figure_style as fs  # noqa: E402

fs.use_matplotlib()
plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.9,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "xtick.labelsize": fs.TEXT_PT,
    "ytick.labelsize": fs.TEXT_PT,
    "legend.fontsize": fs.TEXT_PT,
    "text.parse_math": False,   # labels carry dollar signs
    "axes.facecolor": fs.PLATE,
})

T = fs.TEXT_PT
L = fs.LABEL_PT
GRID = "#e4e0da"
# Series colors. Blue, orange and green were checked together with the dataviz palette validator (adjacent CVD
# separation >= 18, normal-vision >= 32 on the plate); orange sits below 3:1 against the plate, so every orange mark
# carries a visible label or legend entry. Red for a failing point passes against blue (CVD 17).
BLUE = fs.ROLE_CALC
ORANGE = "#f08c30"
GREEN = "#276b2c"
VIOLET = "#9a7fd0"
RED = "#c0392b"
GREY = fs.EDGE

REC = {
    "field": ROOT / ".project/active/aries-comparison-preparation/post-reveal-investigation/field-audit/receipt.json",
    "economics": ROOT / "exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/attribution.json",
    "economics_cases": ROOT / "exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/cases.json",
    "parameters": HERE / "parameter-figure-data.json",
    "conversion": ROOT / "exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/results/presentation/matched-account-table.csv",
    "ranking": ROOT / "exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/results/presentation/native-ranking.csv",
    "architecture": HERE / "architecture-figure-data.json",
}


def save(fig, name, salt):
    plt.rcParams["svg.hashsalt"] = salt
    fig.savefig(HERE / f"{name}.svg", facecolor=fs.PLATE, metadata={"Date": None, "Creator": None})
    plt.close(fig)


def thousands(ax, which="x"):
    """Tick labels with thousands separators, matching the prose (1,000 rather than 1000)."""
    from matplotlib.ticker import FuncFormatter
    fmt = FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.xaxis if which == "x" else ax.yaxis).set_major_formatter(fmt)


def style_axis(ax, grid_axis="x"):
    ax.grid(True, axis=grid_axis, color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    ax.spines["left"].set_color(fs.RULE)
    ax.spines["bottom"].set_color(fs.RULE)


# --- Figure 3: the field at the coils, against the conductor model's range --------------------------------------
# Our run: the reconstructed arithmetic of the failed post-reveal run (field-audit receipt, F-004 in findings.md).
# ARIES: 5.70 T on axis and 15.08 T maximum on the coils, as the post-reveal source review records them (F-003 in
# .project/active/aries-comparison-preparation/post-reveal-investigation/findings.md); the page states "about 15.1".
def field_range():
    r = json.loads(REC["field"].read_text())["intermediates"]
    ours_axis, ours_peak = r["B_axis_T"], r["B_peak_T"]
    aries_axis, aries_peak = 5.70, 15.08
    fig = plt.figure(figsize=(fs.WIDE_IN, 2.55))
    ax = fig.add_axes([0.215, 0.23, 0.765, 0.72])
    ax.set(xlim=(0, 60), ylim=(-0.55, 1.55))
    for s in ("left", "top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(fs.RULE)
    ax.set_yticks([])
    ax.set_xticks(range(0, 61, 10))
    ax.set_xlabel("Magnetic field (tesla)", fontsize=T, color=fs.INK)
    for y in (0, 1):
        ax.plot([0, 60], [y, y], color=GRID, lw=0.8, zorder=0)
    ax.add_patch(Rectangle((20, -0.36), 12, 0.72, fc=fs.ROLE_CHECK_FILL, ec=fs.ROLE_CHECK, lw=1.0, zorder=1))
    ax.text(26, 0.44, "conductor model's range, 20–32 T", ha="center", va="bottom", fontsize=T, color=fs.ROLE_CHECK)
    ax.text(-1.2, 1, "On the plasma axis", ha="right", va="center", fontsize=T, weight="semibold", color=fs.INK)
    ax.text(-1.2, 0, "At the coils", ha="right", va="center", fontsize=T, weight="semibold", color=fs.INK)

    def mark(x, y, color, marker, label, above):
        ax.plot([x], [y], marker=marker, ms=9, color=color, mec=fs.PLATE, mew=1.3, zorder=4, ls="none")
        ax.text(x, y + (0.2 if above else -0.2), label, ha="center", va="bottom" if above else "top", fontsize=T,
                color=color)

    mark(aries_axis, 1, fs.INK, "s", f"ARIES {aries_axis:.1f}", True)
    mark(ours_axis, 1, BLUE, "o", f"our run {ours_axis:.1f}", True)
    mark(aries_peak, 0, fs.INK, "s", f"ARIES {aries_peak:.1f}", False)
    mark(ours_peak, 0, BLUE, "o", f"our run {ours_peak:.1f}", True)
    save(fig, "page-field-range", "field-range")


# --- Figure 5: how close the extended model came -----------------------------------------------------------------
# Both panels use the costed 891 MW configuration of aries-reconciled-alternative-economics (attribution.json,
# scenario alt-canonical-no-credit, and the aligned L7/L8 diagnostics) and the published values that record carries.
def how_close():
    d = json.loads(REC["economics"].read_text())
    pub = d["published"]
    alt = d["scenarios"]["alt-canonical-no-credit"]
    contrib = alt["contributions"]
    steps = {s["case"]: s["lcoe_ours"] for s in d["ladder"]["steps"]}
    aligned = [(0, steps["diag-L8-aligned-discount-0.00"]), (3, steps["diag-L8-aligned-discount-0.03"]),
               (5, steps["diag-L7-aligned-combined-at-our-net"]), (8, steps["diag-L8-aligned-discount-0.08"]),
               (10, steps["diag-L8-aligned-discount-0.10"])]
    cases = json.loads(REC["economics_cases"].read_text())["cases"]
    tin_K = next(c for c in cases if c["case"] == "alt-canonical-no-credit")["outputs"][
        "aries_integrated_plant__heat_exchangers__evaluate__turbine_temperature"]
    tin_ours, tin_aries = tin_K - 273.15, 708.0  # ARIES: 708 °C (Lyon Table IV, as the reconciliation answer cites it)

    fig = plt.figure(figsize=(fs.WIDE_IN, 5.5))
    a = fig.add_axes([0.155, 0.64, 0.3, 0.27])
    b = fig.add_axes([0.64, 0.64, 0.335, 0.27])
    c = fig.add_axes([0.155, 0.1, 0.52, 0.34])

    # Power: net electricity from the same fusion power.
    ys = [1, 0]
    a.barh(ys[0], alt["net"], height=0.52, color=BLUE)
    a.barh(ys[1], pub["net"], height=0.52, color=GREY)
    a.set(xlim=(0, 1250), ylim=(-0.6, 1.6))
    a.set_yticks(ys, ["Our model", "ARIES, published"])
    a.text(alt["net"] + 15, ys[0], f"{alt['net']:,.0f} MW", va="center", fontsize=T, color=fs.INK)
    a.text(pub["net"] + 15, ys[1], f"{pub['net']:,.0f} MW", va="center", fontsize=T, color=fs.INK)
    a.text(18, ys[0], f"turbine inlet {tin_ours:.0f} °C", va="center", fontsize=T, color="white")
    a.text(18, ys[1], f"turbine inlet {tin_aries:.0f} °C", va="center", fontsize=T, color="white")
    a.set_xlabel("Net electricity (MW)", fontsize=T)
    a.set_title("Power from 2,436 MW of fusion", loc="left", pad=10)
    thousands(a, "x")
    style_axis(a)

    # Cost as modeled: purchased tritium first, then everything else, so each label sits on its own segment.
    tritium = contrib["tritium"]
    rest = alt["lcoe"] - tritium
    b.barh(1, tritium, height=0.52, color=ORANGE)
    b.barh(1, rest, left=tritium, height=0.52, color=BLUE)
    b.text(tritium / 2, 1, f"purchased tritium ${tritium:,.0f}", ha="center", va="center", fontsize=T, color=fs.INK)
    b.text(alt["lcoe"] + 14, 1.02, f"+ everything else ${rest:,.0f}", va="bottom", fontsize=T, color=fs.INK)
    b.text(alt["lcoe"] + 14, 0.98, f"= ${alt['lcoe']:,.0f} in all", va="top", fontsize=T, color=fs.INK)
    b.barh(0, pub["lcoe"], height=0.52, color=GREY)
    b.text(pub["lcoe"] + 14, 0, f"${pub['lcoe']:.1f}", va="center", fontsize=T)
    b.set(xlim=(0, 1100), ylim=(-0.6, 1.6))
    b.set_xticks([0, 250, 500, 750, 1000])
    b.set_yticks([1, 0], ["Our model", "ARIES, published"])
    b.set_xlabel("2004 $ per MWh", fontsize=T)
    b.set_title("Cost of electricity, our model buying all its tritium", loc="left", pad=10)
    thousands(b, "x")
    style_axis(b)

    # Cost on ARIES's basis: its tritium assumption and accounting conventions, at each stored discount rate.
    xs = [r for r, _ in aligned]
    vs = [v for _, v in aligned]
    c.axhline(pub["lcoe"], color=GREY, ls=(0, (4, 3)), lw=1.3, zorder=1)
    c.plot(xs, vs, color=BLUE, lw=1.4, zorder=2)
    c.scatter(xs, vs, s=[80 if r == 5 else 46 for r in xs], color=BLUE, edgecolors=fs.PLATE, linewidths=1.2,
              zorder=3)
    for r, v in aligned:  # labels below the points under ARIES's line, above the points over it, clear of the line
        above = v > pub["lcoe"]
        c.text(r, v + (6 if above else -6), f"${v:,.0f}", ha="center", va="bottom" if above else "top", fontsize=T,
               weight="semibold" if r == 5 else "normal", color=fs.INK)
    c.text(10.35, pub["lcoe"], f"ARIES, published: ${pub['lcoe']:.1f}", va="bottom", fontsize=T, color=fs.INK,
           clip_on=False)
    c.text(10.35, pub["lcoe"] - 2, "historical ARIES costing uses 4.35%", va="top", fontsize=L, color=fs.MUTED,
           clip_on=False)
    c.set(xlim=(-0.4, 10.4), ylim=(0, 128))
    c.set_xticks(xs, [f"{r}%" for r in xs])
    c.set_xlabel("Real discount rate", fontsize=T)
    c.set_ylabel("2004 $ per MWh", fontsize=T)
    c.set_title("Our model with ARIES's tritium assumption and accounting conventions", loc="left", pad=10)
    style_axis(c, "y")
    save(fig, "page-how-close", "how-close")


# --- Figure 7: net electricity and unremoved heat near the exchanger limit ---------------------------------------
# parameter-figure-data.json (written by render_parameters.py from the sealed study's readout.json): the seven
# stored cases at 2,500 kg/s with ratio <= 1.45. Each point is its own SVG group, pr-a-N (top) and pr-b-N (bottom),
# so the page's explore panel can find it.
def pressure_ratio():
    d = json.loads(REC["parameters"].read_text())
    cases = sorted(d["pressure_ratio_cases"], key=lambda r: r["ratio"])
    limit = next(r for r in cases if r["case"] == "ir-boundary-f2500")["ratio"]
    fig = plt.figure(figsize=(fs.WIDE_IN, 4.9))
    a = fig.add_axes([0.1, 0.53, 0.88, 0.43])
    b = fig.add_axes([0.1, 0.11, 0.88, 0.3], sharex=a)
    x0, x1 = 1.4245, 1.4505
    for ax in (a, b):
        ax.axvspan(x0, limit, color="#f7e3e0", lw=0, zorder=0)
        ax.axvline(limit, color=fs.MUTED, ls=(0, (4, 3)), lw=1)
        style_axis(ax, "both")
        ax.set_xlim(x0, x1)
    xs = [r["ratio"] for r in cases]
    a.plot(xs, [r["net"] for r in cases], color=GREY, lw=1.2, zorder=2)
    b.plot(xs, [r["unmet"] for r in cases], color=GREY, lw=1.2, zorder=2)
    for k, r in enumerate(cases):
        ok = r["passing"]
        kw = dict(s=70, zorder=4, color=BLUE if ok else RED, marker="o" if ok else "X",
                  edgecolors=fs.PLATE, linewidths=1.2)
        a.scatter([r["ratio"]], [r["net"]], gid=f"pr-a-{k}", **kw)
        b.scatter([r["ratio"]], [r["unmet"]], gid=f"pr-b-{k}", **kw)
    a.set_ylim(570, 640)
    a.set_ylabel("Net electricity (MW)")
    b.set_ylim(-0.8, 10)
    b.set_ylabel("Unremoved heat (MW)")
    b.set_xlabel("Pressure ratio per compressor stage (lower ratio ←)")
    plt.setp(a.get_xticklabels(), visible=False)
    peak = next(r for r in cases if r["case"] == "ir-boundary-f2500")
    fail = next(r for r in cases if not r["passing"])
    a.annotate(f"{peak['net']:.0f} MW at the exchanger limit", xy=(limit, peak["net"]), xytext=(1.4318, 631),
               fontsize=T, arrowprops=dict(arrowstyle="-", color=fs.MUTED, lw=0.9))
    b.annotate(f"{fail['unmet']:.1f} MW of reactor heat cannot be removed", xy=(fail["ratio"], fail["unmet"]),
               xytext=(1.4318, 7.2), fontsize=T, arrowprops=dict(arrowstyle="-", color=fs.MUTED, lw=0.9))
    a.text(limit - 0.00025, 573, "past the limit", ha="right", va="bottom", fontsize=L, color=RED)
    a.text(limit + 0.00025, 573, f"exchanger limit, ratio {limit:.4f}", ha="left", va="bottom", fontsize=L,
           color=fs.MUTED)
    save(fig, "page-pressure-ratio", "pressure-ratio")


# --- Figure 8: the limiting ratio and its output at each cycle flow ----------------------------------------------
def flow_boundary():
    d = json.loads(REC["parameters"].read_text())
    pts = sorted(d["boundary_cases"], key=lambda r: r["flow"])
    fig = plt.figure(figsize=(fs.WIDE_IN, 3.2))
    a = fig.add_axes([0.075, 0.17, 0.39, 0.66])
    b = fig.add_axes([0.585, 0.17, 0.395, 0.66])
    f = [r["flow"] for r in pts]
    best = {2500.0, 2750.0}
    for ax, key, title in ((a, "ratio", "Pressure ratio at the exchanger limit"),
                           (b, "net", "Net electricity at that limit (MW)")):
        ax.plot(f, [r[key] for r in pts], color=GREY, lw=1.2, zorder=2)
        ax.scatter(f, [r[key] for r in pts], s=[80 if r["flow"] in best else 42 for r in pts],
                   color=[BLUE if r["flow"] in best else "#7fa3c4" for r in pts], edgecolors=fs.PLATE,
                   linewidths=1.2, zorder=3)
        ax.set_title(title, loc="left", pad=10)
        ax.set_xlabel("Cycle helium flow (kg/s)")
        ax.set_xticks(f, [f"{v:,.0f}" for v in f])
        style_axis(ax, "both")
    for r in pts:
        if r["flow"] in best:
            b.text(r["flow"], r["net"] + 5, f"{r['net']:.1f}", ha="center", va="bottom", fontsize=T, color=fs.INK)
    b.set_ylim(520, 640)
    a.set_ylim(1.2, 1.7)
    save(fig, "page-flow-boundary", "flow-boundary")


def conversion_rows():
    rows = [r for r in csv.DictReader(REC["conversion"].open()) if r["scenario"] == "nominal"
            and r["status"] == "supported_catalog_minimum"]
    order = [("2500.0", "steam"), ("2500.0", "gas"), ("2800.0", "steam"), ("2800.0", "gas")]
    by = {(r["source_MW"], r["branch"]): r for r in rows}
    return [(f"{float(q):,.0f} MW · {b}", by[(q, b)]) for q, b in order]


# --- Figure 9: where each plant's electricity goes ---------------------------------------------------------------
# matched-account-table.csv of the sealed whole-plant conversion study: gross electricity, the conversion
# equipment's own electrical load, the upstream electrical load and net export, for the four supported nominal plants.
def power_budget():
    rows = conversion_rows()
    fig = plt.figure(figsize=(fs.WIDE_IN, 3.25))
    ax = fig.add_axes([0.14, 0.15, 0.84, 0.66])
    y = list(range(len(rows)))[::-1]
    for yi, (label, r) in zip(y, rows):
        exp = float(r["power.net_export_MW"])
        conv = float(r["conversion.electrical_load"])
        up = float(r["power.upstream_electric_MW"])
        gross = float(r["conversion.gross_electric"])
        ax.barh(yi, exp, height=0.6, color=BLUE)
        ax.barh(yi, conv, left=exp, height=0.6, color=ORANGE)
        ax.barh(yi, up, left=exp + conv, height=0.6, color=GREEN)
        ax.text(12, yi, f"{exp:,.0f} for sale", va="center", fontsize=T, color="white")
        ax.text(exp + conv + up / 2, yi, f"{up:,.0f}", ha="center", va="center", fontsize=T, color="white")
        ax.text(gross + 10, yi, f"{gross:,.0f} generated", va="center", fontsize=T, color=fs.INK)
    ax.set_yticks(y, [lab for lab, _ in rows])
    ax.set(xlim=(0, 1250), ylim=(-0.6, len(rows) - 0.4))
    ax.set_xlabel("Electricity (MW)")
    thousands(ax, "x")
    style_axis(ax)
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, ORANGE, GREEN)]
    fig.legend(handles, ["For sale", "Conversion equipment's own use",
                         "Reactor circulation, heating, refrigeration and services"],
               loc="upper left", bbox_to_anchor=(0.14, 0.995), ncol=3, frameon=False, handlelength=1.1,
               columnspacing=1.6)
    save(fig, "page-power-budget", "power-budget")


# --- Figure 10: whole-plant LCOE by where the money goes ---------------------------------------------------------
# Present value of each account divided by the present value of exported energy, as the study's own figure does;
# the four groups sum to its published LCOE.
def cost_contributions():
    rows = conversion_rows()
    groups = [
        ("Initial financed capital", BLUE, ["whole.initial_financed_capital"]),
        ("Annual service, fuel, makeup and imports", ORANGE, ["whole.annual_expense_pv"]),
        ("Blanket, magnet, primary and conversion replacements", GREEN,
         ["whole.blanket_replacement_pv", "whole.magnet_replacement_pv", "whole.primary_replacement_pv",
          "whole.conversion_replacement_pv"]),
        ("Overhaul and terminal cost", VIOLET, ["whole.overhaul_pv", "whole.terminal_pv"]),
    ]
    fig = plt.figure(figsize=(fs.WIDE_IN, 3.35))
    ax = fig.add_axes([0.14, 0.15, 0.84, 0.62])
    y = list(range(len(rows)))[::-1]
    for yi, (label, r) in zip(y, rows):
        energy = float(r["whole.energy_pv"])
        left = 0.0
        for name, color, keys in groups:
            v = sum(float(r[k]) for k in keys) / energy
            ax.barh(yi, v, left=left, height=0.6, color=color)
            if name.startswith("Initial"):
                ax.text(12, yi, f"${v:,.0f}", va="center", fontsize=T, color="white")
            left += v
        lcoe = float(r["whole.lcoe_USD2025_MWh"])
        assert abs(left - lcoe) < 1e-3 * lcoe, (label, left, lcoe)
        ax.text(lcoe + 12, yi, f"${lcoe:,.0f} per MWh", va="center", fontsize=T, color=fs.INK)
    ax.set_yticks(y, [lab for lab, _ in rows])
    ax.set(xlim=(0, 1450), ylim=(-0.6, len(rows) - 0.4))
    ax.set_xlabel("Whole-plant LCOE (2025 $ per MWh)")
    thousands(ax, "x")
    style_axis(ax)
    handles = [Rectangle((0, 0), 1, 1, color=c) for _, c, _ in groups]
    fig.legend(handles, [n for n, _, _ in groups], loc="upper left", bbox_to_anchor=(0.14, 1.0), ncol=2,
               frameon=False, handlelength=1.1, columnspacing=1.6)
    save(fig, "page-cost-contributions", "cost-contributions")


# --- Figure 11: every tested change, as Brayton's LCOE over steam's ---------------------------------------------
# native-ranking.csv of the same study: the supported catalog minimum of each branch in every scenario. The
# reporting-band and economic-bracket rows are threshold diagnostics, not tested changes, and are left out; so are
# scenarios where neither branch is supported (listed on the page).
FAMILIES = [
    ("nominal_catalog", "Nominal assumptions"),
    ("fuel", "Breeding ratio and tritium price"),
    ("finance", "Discount rate 0 or 10%"),
    ("availability", "Availability 65%"),
    ("common_capital", "Common plant quotes ×0.5 or ×1.5"),
    ("overheads", "Contingency and overhead rates"),
    ("source_installation", "Reactor installation cost"),
    ("primary_piping", "Primary piping quote ×0.5 or ×1.5"),
    ("replacement", "Magnet life 8 or 12 years"),
    ("conversion_price_service", "Conversion quotes and service costs"),
    ("auxiliary_rejection", "Auxiliary heat-rejection quote"),
    ("service", "Routine service allocation"),
    ("imports", "Import electricity price"),
    ("source_load", "Heating, pumping and other loads"),
    ("cryogenic_heat", "Cryogenic and nuclear heating loads"),
    ("joint_efficiency", "Combined machine efficiencies"),
    ("joint_performance_price", "Combined efficiencies and quotes"),
]


def conversion_sensitivity():
    rows = list(csv.DictReader(REC["ranking"].open()))
    pairs = {}
    for r in rows:
        if r["status"] != "supported_catalog_minimum":
            continue
        pairs.setdefault((r["scenario"], r["source_MW"], r["family"]), {})[r["branch"]] = float(
            r["native_lcoe_USD2025_MWh"])
    fam_y = {fam: len(FAMILIES) - 1 - i for i, (fam, _) in enumerate(FAMILIES)}
    # Shown inside an evidence panel, whose plate is about 7.5 in wide, so it is drawn at that width.
    fig = plt.figure(figsize=(7.5, 5.9))
    axes = [fig.add_axes([0.335, 0.125, 0.3, 0.81]), fig.add_axes([0.685, 0.125, 0.3, 0.81])]
    for ax, load in zip(axes, ("2500.0", "2800.0")):
        ax.set_xscale("log")
        ax.set(xlim=(0.8, 12), ylim=(-0.7, len(FAMILIES) - 0.3))
        ax.axvspan(0.8, 1.0, color="#f7e3e0", lw=0, zorder=0)
        ax.axvline(1.0, color=fs.MUTED, lw=1)
        ax.set_xticks([1, 2, 4, 8], ["1×", "2×", "4×", "8×"])
        ax.minorticks_off()
        style_axis(ax, "x")
        for y in range(len(FAMILIES)):
            ax.axhline(y, color=GRID, lw=0.6, zorder=0)
        ax.set_title(f"{float(load):,.0f} MW of reactor heat", loc="left", pad=8)
        for (scen, q, fam), v in pairs.items():
            if q != load or fam not in fam_y or "gas" not in v or "steam" not in v:
                continue
            ratio = v["gas"] / v["steam"]
            reversed_ = ratio < 1
            ax.plot([ratio], [fam_y[fam]], marker="D" if fam == "nominal_catalog" else "o",
                    ms=7 if fam == "nominal_catalog" else 5.5, ls="none",
                    color=RED if reversed_ else (fs.INK if fam == "nominal_catalog" else BLUE),
                    mec=fs.PLATE, mew=0.8, alpha=1 if reversed_ or fam == "nominal_catalog" else 0.8, zorder=3)
            if reversed_:
                ax.text(ratio * 1.12, fam_y[fam], f"Brayton ${v['gas']:.0f}, steam ${v['steam']:.0f}",
                        va="center", fontsize=T, color=RED)
        ax.set_yticks(range(len(FAMILIES)))
        ax.set_yticklabels([lab for _, lab in FAMILIES][::-1] if ax is axes[0] else [])
        ax.tick_params(axis="y", length=0)
    fig.text(0.335, 0.008, "Brayton's LCOE as a multiple of steam's, on a log scale.\nRight of 1×, steam is cheaper; "
             "in the shaded band, Brayton is.", ha="left", va="bottom", fontsize=T, color=fs.INK, linespacing=1.4)
    save(fig, "page-conversion-sensitivity", "conversion-sensitivity")


# --- Figure 13: the nominal architecture pair -------------------------------------------------------------------
# architecture-figure-data.json (written by render_architecture.py from the goal's reporting.json): the matched
# offer-B pair at 1,835.45 MW of supplied fusion power; both layouts pass every check.
def architecture_pair():
    p = json.loads(REC["architecture"].read_text())["pair"]
    assert p["series_pass"] and p["network_pass"]
    fig = plt.figure(figsize=(fs.WIDE_IN, 2.75))
    panels = [("Cycle helium flow (kg/s)", "series_flow_kg_s", "network_flow_kg_s", "{:,.0f}"),
              ("Net electricity (MW)", "series_net_MW", "network_net_MW", "{:,.1f}"),
              ("Cost excluding fuel (2004 $/MWh)", "series_nonfuel_lcoe", "network_nonfuel_lcoe", "${:,.2f}")]
    for i, (title, ks, kn, fmt) in enumerate(panels):
        ax = fig.add_axes([0.115 + i * 0.3, 0.14, 0.2, 0.66])
        vals = [p[ks], p[kn]]
        ax.barh([1, 0], vals, height=0.56, color=[GREY, BLUE])
        for yv, v in zip([1, 0], vals):
            ax.text(v * 1.02, yv, fmt.format(v), va="center", fontsize=T)
        ax.set_xlim(0, max(vals) * 1.42)
        ax.set_ylim(-0.6, 1.6)
        ax.set_yticks([1, 0], ["Series", "Split"] if i == 0 else ["", ""])
        ax.set_title(title, loc="left", pad=8, fontsize=T)
        ax.tick_params(axis="x", labelsize=L)
        thousands(ax, "x")
        style_axis(ax)
        if i:
            ax.tick_params(axis="y", length=0)
    save(fig, "page-architecture-pair", "architecture-pair")


# --- Inlining -----------------------------------------------------------------------------------------------------
# Each entry: marker name -> (id prefix, accessible label, extra attributes on the <svg>).
INLINE = {
    "page-field-range": ("fr", "Magnetic field in tesla on one axis. On the plasma axis: ARIES 5.7, our run 14.7. "
                         "At the coils: ARIES 15.1, our run 56.6. The conductor model covers 20 to 32 tesla at the "
                         "coils; both coil values fall outside it, ARIES's below and ours above.", ""),
    "page-how-close": ("hc", "Three panels. Net electricity from 2,436 MW of fusion: our model 891 MW with a 628 °C "
                       "turbine inlet, ARIES 1,000 MW with 708 °C. Cost of electricity in 2004 dollars per MWh with "
                       "all tritium bought: our model 686, of which 627 is purchased tritium and 58 everything else, "
                       "against ARIES's published 77.6. Our model with ARIES's tritium assumption and accounting "
                       "conventions, at real discount rates of 0, 3, 5, 8 and 10%: 32, 46, 59, 85 and 105, against "
                       "ARIES's published 77.6. Historical ARIES costing uses a 4.35% discount rate, with other "
                       "financial assumptions that differ.", ""),
    "page-pressure-ratio": ("pr", "Net electricity rises as compressor pressure ratio falls, until the exchanger can "
                            "no longer remove all reactor heat", ' data-marks="pr"'),
    "page-flow-boundary": ("fb", "Pressure ratio and net electricity at the exchanger limit across seven cycle flows",
                           ""),
    "page-power-budget": ("pb", "Electricity exported and consumed internally by the steam and helium Brayton plants",
                          ""),
    "page-cost-contributions": ("cc", "Whole-plant LCOE contributions for steam and helium Brayton at both supported "
                                "heat loads", ""),
    "page-conversion-sensitivity": ("cs", "For each group of tested changes, Brayton's LCOE divided by steam's at "
                                    "2,500 and 2,800 MW of reactor heat. Every point lies above 1, meaning steam is "
                                    "cheaper, except one: combined gas-favourable efficiencies with halved Brayton "
                                    "and 50% dearer steam quotes at 2,800 MW, where Brayton costs $397 and steam $427 "
                                    "per MWh.", ""),
    "page-architecture-pair": ("ap", "Nominal architecture comparison: the split network needs less cycle flow, "
                               "produces more electricity and reduces the cost excluding fuel", ""),
}


def inline_svg(name):
    prefix, label, extra = INLINE[name]
    s = (HERE / f"{name}.svg").read_text()
    s = s[s.index("<svg"):]
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    for i in sorted(ids, key=len, reverse=True):
        s = s.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f"url(#{i})", f"url(#{prefix}-{i})") \
             .replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    # The explore panel looks points up by their plain gids (pr-a-N); keep those unprefixed.
    s = re.sub(rf'id="{prefix}-(pr-[ab]-\d+)"', r'id="\1"', s)
    label = label.replace("&", "&amp;").replace('"', "&quot;")
    s = s.replace("<svg ", f'<svg role="img" aria-label="{label}"{extra} ', 1)
    s = "\n".join(line.rstrip() for line in s.strip().splitlines())
    return s


# The explore panel of Figure 6 reads each stored point from this JSON; the table is the same data for readers
# without scripts (the panel hides it once it runs). Both come from parameter-figure-data.json.
CHECK_NAMES = {"checks__heat_removal_ok": "heat removal", "checks__return_condition_ok": "return temperature"}


def pressure_ratio_points():
    d = json.loads(REC["parameters"].read_text())
    cases = sorted(d["pressure_ratio_cases"], key=lambda r: r["ratio"])
    pts = [{"k": k, "case": r["case"], "ratio": round(r["ratio"], 6), "net": round(r["net"], 3),
            "unmet": round(r["unmet"], 3), "bypass": round(r["bypass_fraction"], 6),
            "heater_C": round(r["heater_inlet_K"] - 273.15, 2), "nonfuel": round(r["nonfuel_lcoe"], 2),
            "pass": bool(r["passing"]), "failed": [CHECK_NAMES.get(c, c) for c in r["failed_checks"]]}
           for k, r in enumerate(cases)]
    (HERE / "page-pressure-ratio-points.json").write_text(json.dumps(pts, indent=1) + "\n")
    rows = []
    for q in reversed(pts):
        verdict = "passes every check" if q["pass"] else "fails " + " and ".join(q["failed"])
        rows.append(f'<tr><td class="r">{q["ratio"]:.4f}</td><td class="r">{q["net"]:.1f}</td>'
                    f'<td class="r">{q["unmet"]:.1f}</td><td class="r">{100 * q["bypass"]:.1f}%</td>'
                    f'<td class="r">{q["heater_C"]:.0f}</td><td class="r">{q["nonfuel"]:.2f}</td><td>{verdict}</td></tr>')
    return json.dumps(pts, separators=(",", ":")), "\n".join(rows)


def refresh_page():
    html = PAGE.read_text()
    data, table = pressure_ratio_points()
    for name, body in (("pr-points", data), ("pr-table", table)):
        start, end = f"<!-- inline:{name} -->", f"<!-- /inline:{name} -->"
        if start in html:
            a = html.index(start) + len(start)
            html = html[:a] + "\n" + body + "\n" + html[html.index(end):]
    for name in INLINE:
        start, end = f"<!-- inline:{name} -->", f"<!-- /inline:{name} -->"
        if start not in html:
            print(f"page has no marker for {name}; skipped")
            continue
        a = html.index(start) + len(start)
        b = html.index(end)
        html = html[:a] + "\n" + inline_svg(name) + "\n" + html[b:]
    PAGE.write_text(html)


if __name__ == "__main__":
    field_range()
    how_close()
    pressure_ratio()
    flow_boundary()
    power_budget()
    cost_contributions()
    conversion_sensitivity()
    architecture_pair()
    for svg in HERE.glob("page-*.svg"):
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    if PAGE.exists():
        refresh_page()
