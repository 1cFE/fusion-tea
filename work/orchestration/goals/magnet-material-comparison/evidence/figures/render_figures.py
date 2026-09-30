#!/usr/bin/env python
"""Render the T-008 results table and figures from the sealed study record.

Reads only ``results/cases.csv`` of record ``20260929-magnet-material-comparison`` (plus
``results/case_aliases.json``, used solely to check that grouping declared cases by
``candidate_id`` reproduces the record's alias list). Writes one CSV per figure under
``data/`` (every row carries its case id), ``data/results-table.csv``, and every figure as
SVG and PNG (150 dpi) next to this script. Deterministic: fixed SVG hash salt, no dates in
the output metadata, no random state.

Run from the repository root:

    .codex-test/run python work/orchestration/goals/magnet-material-comparison/evidence/figures/render_figures.py

Nothing here re-runs the model, the oracle or the study. Values are plotted as recorded;
unit changes are only scale factors (W to kW or MW, m to km, USD to M USD).
"""

from __future__ import annotations

import csv
import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

# --------------------------------------------------------------------------------------
# Paths and record identity
# --------------------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
RECORD_ID = "20260929-magnet-material-comparison"
RECORD_DIR = REPO / "exploration" / "magnet_materials" / "studies" / RECORD_ID
CASES_CSV = RECORD_DIR / "results" / "cases.csv"
ALIASES_JSON = RECORD_DIR / "results" / "case_aliases.json"
DATA_DIR = HERE / "data"

P = "magnet_subsystem__subsystem__"


def ch(material: str, channel: str) -> str:
    """Column name of a per-material channel, e.g. ch('nb3sn', 'area__fit_margin')."""
    return f"{P}{material}__{channel}"


PAIR = {
    "rankable": P + "pair__rankable",
    "cost_difference": P + "pair__cost_difference",
    "be_per_m": P + "pair__breakeven_rebco_price_per_m",
    "be_per_kAm": P + "pair__breakeven_rebco_price_per_kAm",
}

# Nb3Sn / REBCO conductor status codes as stored in cases.csv. The mapping is fixed by the
# record: summary.json § materials.status_by_anchor_field lists D-13T as edge, D-14T as
# law-only and D-16T..D-20T as unsupported, and cases.csv carries codes 2, 3 and 0 there;
# it is asserted below against point_class before anything is plotted.
STATUS = {1: "supported", 2: "edge", 3: "law-only", 0: "unsupported"}

MATERIAL_LABEL = {"nb3sn": "Nb₃Sn", "rebco": "REBCO"}

# --------------------------------------------------------------------------------------
# Palette (dataviz reference palette, light surface) and chart chrome
# --------------------------------------------------------------------------------------

BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
VIOLET = "#4a3aa7"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"
BAND = "#e1e0d9"

MATERIAL_COLOR = {"nb3sn": BLUE, "rebco": ORANGE}
STATUS_MARKER = {"supported": "o", "edge": "^", "law-only": "D", "unsupported": "o"}

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "lines.linewidth": 1.3,
        "lines.markersize": 5,
        "svg.hashsalt": RECORD_ID,
        "svg.fonttype": "path",
        "path.simplify": False,
    }
)

FIELD_TICKS = [8, 9, 10, 11, 12, 13, 14, 16, 18, 20]


# --------------------------------------------------------------------------------------
# Loading and shared helpers
# --------------------------------------------------------------------------------------


def load_cases() -> tuple[pd.DataFrame, dict[str, list[str]]]:
    df = pd.read_csv(CASES_CSV)
    assert len(df) == 2832, f"expected 2832 declared cases, read {len(df)}"
    assert df["candidate_id"].nunique() == 2310, "expected 2310 executed points"

    # Alias groups: declared case ids that share one executed point (same candidate_id).
    groups = df.groupby("candidate_id", sort=False)["case_id"].apply(list)
    aliases_of: dict[str, list[str]] = {}
    for ids in groups:
        for cid in ids:
            aliases_of[cid] = [o for o in ids if o != cid]

    # Cross-check against the record's own alias list (read for the check only).
    record_aliases = json.loads(ALIASES_JSON.read_text())["aliases"]
    for canonical, others in record_aliases.items():
        assert set(aliases_of[canonical]) == set(others), f"alias mismatch at {canonical}"
    # 506 canonical ids plus 522 aliased ids share a point with at least one other declared case.
    assert sum(1 for v in aliases_of.values() if v) == 506 + 522, "alias count"

    # Status-code check against point_class (Nb3Sn on anchor D; REBCO everywhere).
    nb = df[ch("nb3sn", "conductor__status_code")].astype(int)
    assert (nb[(df.anchor == "D") & (df.B_peak == 13.0)] == 2).all()
    assert (nb[(df.anchor == "D") & (df.B_peak == 14.0)] == 3).all()
    assert (nb[(df.anchor == "D") & (df.B_peak >= 16.0)] == 0).all()
    assert (nb[df.B_peak <= 12.0] == 1).all()
    assert (df[ch("rebco", "conductor__status_code")].astype(int) == 1).all()
    return df, aliases_of


def reference_offers(df: pd.DataFrame) -> pd.DataFrame:
    """Reference offers, reference variant, reference rule family, reference refrigerator."""
    m = (
        (df.variant == "none")
        & (df.offer_kind == "reference")
        & (df.refrigerator_kind == "reference")
        & (df.rule_family == "reference")
    )
    return df[m]


def status_of(row: pd.Series, material: str) -> str:
    return STATUS[int(row[ch(material, "conductor__status_code")])]


def construction_of(material: str, pairing: str) -> str:
    """Construction rule the material sits on under a pairing (contract § 4)."""
    if pairing == "common-P":
        return "P"
    if pairing == "common-C":
        return "C"
    return "P" if material == "nb3sn" else "C"  # native: Nb3Sn on P, REBCO on C


def failed_checks(row: pd.Series, material: str) -> list[str]:
    names = ["acceptance", "fit", "copper", "steel", "capacity"]
    return [n for n in names if row[f"{material}.{n}_ok"] == "violated"]


def non_rankable_reason(row: pd.Series) -> str:
    """Why a reference-offer pair carries no ranking, from the recorded verdicts."""
    if int(row[PAIR["rankable"]]) == 1:
        return ""
    parts = []
    for material in ("nb3sn", "rebco"):
        st = status_of(row, material)
        fails = failed_checks(row, material)
        if st == "unsupported":
            parts.append(f"{MATERIAL_LABEL[material]} unsupported")
        elif fails:
            parts.append(f"{MATERIAL_LABEL[material]} {', '.join(fails)}")
    return "; ".join(parts)


def write_csv(name: str, rows: list[dict], columns: list[str]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, "")) for k in columns})
    return path


def fmt(v):
    if isinstance(v, float):
        if np.isnan(v):
            return ""
        return repr(float(v))
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return repr(float(v))
    return v


def field_axis(ax, ticks=FIELD_TICKS):
    ax.set_xticks(ticks)
    ax.set_xlabel("Peak field at the conductor (T)")
    ax.tick_params(length=2.5)


def footer(fig, text: str, y: float = 0.008):
    width = int(fig.get_figwidth() * 16.5)
    body = textwrap.fill(f"Record {RECORD_ID} · {text}", width=width)
    fig.text(0.01, y, body, fontsize=7.2, color=MUTED, ha="left", va="bottom", linespacing=1.4)


def save(fig, stem: str):
    fig.savefig(HERE / f"{stem}.svg", format="svg", metadata={"Date": None, "Creator": None})
    fig.savefig(HERE / f"{stem}.png", format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)


def hline(ax, y, label=None, color=MUTED, ls=(0, (4, 3)), lw=0.8, label_x=0.99, ha="right", va="bottom",
          dy_pt=0.0):
    """Dashed reference line with a label; ``dy_pt`` shifts the label vertically in points."""
    ax.axhline(y, color=color, linestyle=ls, linewidth=lw, zorder=1)
    if label:
        ax.annotate(label, xy=(label_x, y), xycoords=ax.get_yaxis_transform(), xytext=(0, dy_pt),
                    textcoords="offset points", fontsize=7.2, color=INK2, ha=ha, va=va, zorder=6)


def fields_text(fields: list[float], of: list[float] | None = None) -> str:
    """'12–14 T' for a run of consecutive integer fields, '13 T and above' when the fields are every
    evaluated field (``of``) from the first one up, else '12, 13 T'; '' when empty."""
    fs = sorted(set(fields))
    if not fs:
        return ""
    if of is not None and len(fs) > 1 and fs == sorted({f for f in of if f >= fs[0]}):
        return f"{fs[0]:g} T and above"
    if len(fs) > 1 and all(b - a == 1 for a, b in zip(fs, fs[1:])):
        return f"{fs[0]:g}–{fs[-1]:g} T"
    return ", ".join(f"{f:g}" for f in fs) + " T"


def plot_series(ax, x, y, color, ls="-", statuses=None, hollow=None, zorder=3, lw=1.3, ms=5):
    """A line through the points plus one marker per point shaped by status."""
    ax.plot(x, y, color=color, linestyle=ls, linewidth=lw, zorder=zorder)
    statuses = statuses if statuses is not None else ["supported"] * len(x)
    hollow = hollow if hollow is not None else [s == "unsupported" for s in statuses]
    for xi, yi, st, ho in zip(x, y, statuses, hollow):
        ax.plot(
            [xi], [yi], marker=STATUS_MARKER[st], linestyle="none", markersize=ms,
            markerfacecolor="none" if ho else color, markeredgecolor=color, markeredgewidth=1.1,
            zorder=zorder + 1,
        )


def status_legend_handles(include_unsupported=True):
    h = [
        Line2D([], [], marker="o", color=INK2, linestyle="none", markersize=5, label="supported"),
        Line2D([], [], marker="^", color=INK2, linestyle="none", markersize=5, label="edge (Nb₃Sn 12.2–13.5 T)"),
        Line2D([], [], marker="D", color=INK2, linestyle="none", markersize=4.5, label="law-only (Nb₃Sn 13.5–14.5 T)"),
    ]
    if include_unsupported:
        h.append(Line2D([], [], marker="o", color=INK2, markerfacecolor="none", linestyle="none", markersize=5,
                        label="unsupported (no verdict)"))
    return h


def base_row(row: pd.Series, aliases_of) -> dict:
    return {
        "case_id": row["case_id"],
        "candidate_id": row["candidate_id"],
        "aliases": ";".join(aliases_of[row["case_id"]]),
        "anchor": row["anchor"],
        "B_peak_T": float(row["B_peak"]),
        "point_class": row["point_class"],
        "pairing": row["pairing"],
        "rule_family": row["rule_family"],
        "variant": row["variant"],
        "offer_kind": row["offer_kind"],
        "refrigerator_kind": row["refrigerator_kind"],
    }


# --------------------------------------------------------------------------------------
# F1 — fit margin per turn versus field, anchors D and S
# --------------------------------------------------------------------------------------

F1_YMIN_D = -5000.0


def figure_f1(df, aliases_of):
    ref = reference_offers(df)
    panels = {"D": ["common-P", "native", "common-C"], "S": ["common-P", "native", "common-C"]}
    rows = []
    for anchor, pairings in panels.items():
        sub = ref[(ref.anchor == anchor) & (ref.pairing.isin(pairings))].sort_values(["pairing", "B_peak"])
        for _, r in sub.iterrows():
            for material in ("nb3sn", "rebco"):
                fm = float(r[ch(material, "area__fit_margin")])
                clipped = anchor == "D" and fm < F1_YMIN_D
                rows.append({
                    **base_row(r, aliases_of),
                    "panel": f"anchor {anchor}",
                    "material": MATERIAL_LABEL[material],
                    "construction": construction_of(material, r.pairing),
                    "status": status_of(r, material),
                    "fit_margin_mm2": fm,
                    "gross_area_mm2": float(r[ch(material, "area__gross_area")]),
                    "fit_pass": int(r[ch(material, "area__fit_pass")]),
                    "drawn_at_axis_floor": int(clipped),
                })
    cols = list(rows[0].keys())
    write_csv("f1_fit.csv", rows, cols)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.9), gridspec_kw={"width_ratios": [1.25, 1]})
    series_spec = {
        # (material, construction): (label, linestyle)
        ("nb3sn", "P"): ("Nb₃Sn on P (common-P = native)", "-"),
        ("nb3sn", "C"): ("Nb₃Sn on C (common-C)", (0, (5, 2))),
        ("rebco", "P"): ("REBCO on P (common-P)", "-"),
        ("rebco", "C"): ("REBCO on C (native = common-C)", (0, (5, 2))),
    }
    handles = {}
    for ax, (anchor, pairings) in zip(axes, panels.items()):
        sub = [r for r in rows if r["panel"] == f"anchor {anchor}"]
        floor_labels: dict[tuple[float, str, str], float] = {}
        for (material, constr), (label, ls) in series_spec.items():
            pts = [r for r in sub if r["material"] == MATERIAL_LABEL[material] and r["construction"] == constr]
            if not pts:
                continue
            for pairing in pairings:
                pp = sorted([r for r in pts if r["pairing"] == pairing], key=lambda r: r["B_peak_T"])
                if not pp:
                    continue
                x = [r["B_peak_T"] for r in pp]
                y = [max(r["fit_margin_mm2"], F1_YMIN_D) if anchor == "D" else r["fit_margin_mm2"] for r in pp]
                st = [r["status"] for r in pp]
                keep = [not r["drawn_at_axis_floor"] for r in pp]
                ax.plot(x, y, color=MATERIAL_COLOR[material], linestyle=ls, linewidth=1.3, zorder=3)
                plot_series(ax, [xi for xi, k in zip(x, keep) if k], [yi for yi, k in zip(y, keep) if k],
                            MATERIAL_COLOR[material], ls="none", statuses=[s_ for s_, k in zip(st, keep) if k])
                for r in pp:
                    key = (r["B_peak_T"], material, constr)
                    if r["drawn_at_axis_floor"] and key not in floor_labels:
                        ax.plot([r["B_peak_T"]], [F1_YMIN_D], marker="v", linestyle="none", markersize=6,
                                markerfacecolor="none", markeredgecolor=MATERIAL_COLOR[material], zorder=5)
                        floor_labels[key] = r["fit_margin_mm2"]
            handles[label] = Line2D([], [], color=MATERIAL_COLOR[material], linestyle=ls, label=label)
        # Values of the points drawn at the axis floor, stacked per field (most negative lowest).
        base = 0  # rightmost field's stack sits lowest; each field to its left stacks above it
        for x_ in sorted({k[0] for k in floor_labels}, reverse=True):
            here = sorted((v, m, c) for (xx, m, c), v in floor_labels.items() if xx == x_)
            for k, (val, material, constr) in enumerate(here):  # label to the left of the floor marker
                ax.annotate(f"{val:,.0f} ({MATERIAL_LABEL[material]}/{constr})", (x_, F1_YMIN_D),
                            xytext=(-6, 5 + 9 * (base + k)), textcoords="offset points", ha="right", fontsize=6.6,
                            color=INK2)
            base += len(here)
        ax.axhline(0, color=AXIS, linewidth=1.0, zorder=2)
        ax.text(0.99, 0.0, "zero: fits the envelope exactly", transform=ax.get_yaxis_transform(), fontsize=7,
                color=MUTED, ha="right", va="bottom")
        field_axis(ax, FIELD_TICKS if anchor == "D" else [8, 9, 10, 11, 12, 13])
        ax.set_ylabel("Fit margin per turn, envelope − gross area (mm²)")
        if anchor == "D":
            ax.set_ylim(F1_YMIN_D, 3600)
            ax.set_title("Anchor D — EU DEMO TF, envelope 3751.1 mm² per turn", loc="left")
            ax.set_xlim(7.6, 20.6)
        else:
            ax.set_title("Anchor S — Stellaris, envelope 420.8 mm² per turn", loc="left")
    fig.legend(handles=[handles[lab] for lab, _ in series_spec.values()] + status_legend_handles(), loc="lower center", ncol=4,
               bbox_to_anchor=(0.5, 0.055), handlelength=2.4, columnspacing=1.4)
    fig.suptitle("F1 · Winding fit: fit margin per turn versus peak field, reference offers", x=0.01, ha="left",
                 fontsize=11, color=INK)
    footer(fig, "reference offers · reference variant · reference rule family · pairings common-P, native and common-C on both "
                "anchors · anchor D points below −5000 mm² are drawn at the axis floor with their value and construction")
    fig.tight_layout(rect=(0, 0.14, 1, 0.95))
    save(fig, "f1_fit")


# --------------------------------------------------------------------------------------
# Shared selection for F2–F4: anchor D, common-P, reference offers, both materials
# --------------------------------------------------------------------------------------


def d_common_p_rows(df, aliases_of, channels: dict[str, tuple[str, float]]):
    """One row per (case, material) for anchor D common-P reference offers.

    ``channels`` maps output column -> (channel suffix, scale). Nb3Sn rows at unsupported
    fields (16–20 T) are kept with plotted = 0.
    """
    ref = reference_offers(df)
    sub = ref[(ref.anchor == "D") & (ref.pairing == "common-P")].sort_values("B_peak")
    rows = []
    for _, r in sub.iterrows():
        for material in ("nb3sn", "rebco"):
            st = status_of(r, material)
            row = {
                **base_row(r, aliases_of),
                "material": MATERIAL_LABEL[material],
                "construction": "P",
                "status": st,
                "plotted": int(st != "unsupported"),
                "fit_pass": int(r[ch(material, "area__fit_pass")]),
                "fit_margin_mm2": float(r[ch(material, "area__fit_margin")]),
            }
            for out, (suffix, scale) in channels.items():
                row[out] = float(r[ch(material, suffix)]) * scale
            rows.append(row)
    return rows


def plot_d_common_p(ax, rows, ycol, material, step=False):
    """Draw one material's plotted rows; a hollow marker means the supplied winding fails fit."""
    pts = sorted([r for r in rows if r["material"] == MATERIAL_LABEL[material] and r["plotted"]],
                 key=lambda r: r["B_peak_T"])
    x = [r["B_peak_T"] for r in pts]
    y = [r[ycol] for r in pts]
    color = MATERIAL_COLOR[material]
    if step:
        ax.step(x, y, where="mid", color=color, linewidth=1.3, zorder=3)
        plot_series(ax, x, y, color, ls="none", statuses=[r["status"] for r in pts],
                    hollow=[not r["fit_pass"] for r in pts])
    else:
        plot_series(ax, x, y, color, statuses=[r["status"] for r in pts], hollow=[not r["fit_pass"] for r in pts])


def material_handles():
    return [Line2D([], [], color=BLUE, marker="o", label="Nb₃Sn (4.5 K supply, strand)"),
            Line2D([], [], color=ORANGE, marker="o", label="REBCO (20 K supply, tape)"),
            Line2D([], [], marker="o", color=INK2, markerfacecolor="none", linestyle="none", markersize=5,
                   label="hollow: supplied winding does not fit the envelope")]


def fit_fail_note(rows) -> str:
    """Footer clause naming the plotted fields where the supplied winding fails fit."""
    parts = []
    for material in ("nb3sn", "rebco"):
        mine = [r for r in rows if r["material"] == MATERIAL_LABEL[material] and r["plotted"]]
        fs = [r["B_peak_T"] for r in mine if not r["fit_pass"]]
        if fs:
            parts.append(f"{MATERIAL_LABEL[material]} {fields_text(fs, of=[r['B_peak_T'] for r in mine])}")
    return "supplied winding fails fit (hollow markers): " + "; ".join(parts) if parts else "every plotted winding fits"


def f234_footer(rows) -> str:
    return ("anchor D · common-P pairing · reference offers · reference variant · reference rule family · "
            + fit_fail_note(rows)
            + " · Nb₃Sn at 16–20 T is unsupported (no verdict) and is listed in the CSV with plotted = 0")


# --------------------------------------------------------------------------------------
# F2 — inventory
# --------------------------------------------------------------------------------------


def figure_f2(df, aliases_of):
    rows = d_common_p_rows(df, aliases_of, {
        "element_length_km": ("inventory__element_length", 1e-3),
        "sc_cost_MUSD2021": ("inventory__sc_cost", 1e-6),
        "conductor_length_km": ("inventory__conductor_length", 1e-3),
        "element_mass_kg": ("inventory__element_mass", 1.0),
    })
    write_csv("f2_inventory.csv", rows, list(rows[0].keys()))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, ycol, ylabel, title in (
        (axes[0], "element_length_km", "Superconducting element length (km)", "Element length: strands (Nb₃Sn) or tapes (REBCO)"),
        (axes[1], "sc_cost_MUSD2021", "Superconductor purchase cost (M USD2021)", "Superconductor purchase cost at reference prices\n(Nb₃Sn 8 USD/m strand, REBCO 80 USD/m tape)"),
    ):
        for material in ("nb3sn", "rebco"):
            plot_d_common_p(ax, rows, ycol, material)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_ylim(bottom=0)
        field_axis(ax)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    fig.legend(handles=material_handles() + status_legend_handles(include_unsupported=False), loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, 0.085))
    fig.suptitle("F2 · Conductor inventory versus peak field, anchor D common-P reference offers", x=0.01, ha="left",
                 fontsize=11, color=INK)
    footer(fig, f234_footer(rows))
    fig.tight_layout(rect=(0, 0.18, 1, 0.95))
    save(fig, "f2_inventory")


# --------------------------------------------------------------------------------------
# F3 — refrigeration
# --------------------------------------------------------------------------------------


def figure_f3(df, aliases_of):
    rows = d_common_p_rows(df, aliases_of, {
        "q_cold_kW": ("cold_load__q_cold", 1e-3),
        "p_in_cold_MW": ("refrigeration__p_in_cold", 1e-6),
        "p_in_shield_MW": ("refrigeration__p_in_shield", 1e-6),
        "p_in_total_MW": ("refrigeration__p_in_total_MW", 1.0),
        "eta_cold": ("refrigeration__eta_cold", 1.0),
        "green_extrapolated": ("refrigeration__green_extrapolated", 1.0),
        "R_equiv_kW": ("refrigeration__R_equiv_kW", 1.0),
        "capacity_margin_kW": ("refrigeration__capacity_margin", 1e-3),
        "refrigerator_capital_MUSD2021": ("refrigeration__refrigerator_capital", 1e-6),
    })
    for r in rows:
        r["green_extrapolated"] = int(r["green_extrapolated"])
    write_csv("f3_refrigeration.csv", rows, list(rows[0].keys()))

    fig, axes = plt.subplots(2, 2, figsize=(10, 8.3))
    specs = (
        (axes[0, 0], "q_cold_kW", "Cold-stage load (kW)", "Cold-stage load (supply temperature stage)", False),
        (axes[0, 1], "p_in_cold_MW", "Cold-stage electrical input (MW)", "Cold-stage refrigerator electrical input", False),
        (axes[1, 0], "R_equiv_kW", "R_equiv, capital-equivalent rating (kW)",
         "Capital-equivalent rating R_equiv as recorded\n(installed rating is not a cases.csv channel)", True),
        (axes[1, 1], "refrigerator_capital_MUSD2021", "Refrigerator capital (M USD2021)", "Refrigerator capital from R_equiv", True),
    )
    # Fields where the recorded green_extrapolated flag is 1 (rating outside the Green fit range),
    # per material, from the plotted rows; shaded on the efficiency- and capital-related panels.
    green_fields = {m: sorted({r["B_peak_T"] for r in rows if r["material"] == MATERIAL_LABEL[m] and r["plotted"]
                               and r["green_extrapolated"]}) for m in ("nb3sn", "rebco")}
    green_all = sorted(set(green_fields["nb3sn"]) | set(green_fields["rebco"]))
    green_note = "; ".join(
        f"{MATERIAL_LABEL[m]} {fields_text(fs, of=[r['B_peak_T'] for r in rows if r['material'] == MATERIAL_LABEL[m] and r['plotted']])}"
        for m, fs in green_fields.items() if fs)
    for ax, ycol, ylabel, title, step in specs:
        if ycol != "q_cold_kW" and green_all:
            ax.axvspan(min(green_all) - 0.5, max(green_all) + 0.5, color=BAND, alpha=0.55, zorder=0, linewidth=0)
            ax.text(min(green_all) - 0.4, 0.015, "green_extrapolated = 1", transform=ax.get_xaxis_transform(),
                    fontsize=7, color=INK2, ha="left", va="bottom")
        for material in ("nb3sn", "rebco"):
            plot_d_common_p(ax, rows, ycol, material, step=step)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_ylim(0, {"R_equiv_kW": 62, "refrigerator_capital_MUSD2021": 56}.get(ycol))
        field_axis(ax)
    axes[0, 0].set_ylim(0, 46)
    axes[0, 0].text(0.02, 0.97, "77 K intercept stage not shown (common to both)", transform=axes[0, 0].transAxes,
                    fontsize=7.2, color=MUTED, va="top")
    axes[1, 0].text(0.98, 0.62, "4.5 K plant: R_equiv = installed rating;\n20 K plant: R_equiv = rating × 0.2132 (contract § 6)",
                    transform=axes[1, 0].transAxes, fontsize=7.2, color=MUTED, va="top", ha="right")
    green_handle = Patch(facecolor=BAND, alpha=0.55, label="shaded: green_extrapolated = 1 (rating outside Green fit range)")
    fig.legend(handles=material_handles() + status_legend_handles(include_unsupported=False) + [green_handle],
               loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.07))
    fig.suptitle("F3 · Refrigeration versus peak field, anchor D common-P reference offers", x=0.01, ha="left",
                 fontsize=11, color=INK)
    footer(fig, f234_footer(rows) + f" · green_extrapolated = 1 (shaded) at {green_note}: the listed 50 kW rating lies "
                "outside the Green refrigerator fit range 0.01–35 kW, so efficiency and capital there extrapolate the fitted laws")
    fig.tight_layout(rect=(0, 0.14, 1, 0.965))
    save(fig, "f3_refrigeration")


# --------------------------------------------------------------------------------------
# F4 — margins
# --------------------------------------------------------------------------------------

FRACTION_RULE = 0.8  # I <= 0.8 x Ic(B, T_conductor)              (contract § 3)
TEMPERATURE_RULE_K = 1.5  # Tcs >= supply + 0.7 K + 1.5 K, i.e. Tcs - T_conductor >= 1.5 K


def figure_f4(df, aliases_of):
    rows = d_common_p_rows(df, aliases_of, {
        "operating_fraction": ("conductor__operating_fraction", 1.0),
        "T_cs_K": ("conductor__T_cs", 1.0),
        "T_conductor_K": ("conductor__T_conductor", 1.0),
        "temperature_margin_K": ("conductor__temperature_margin", 1.0),
        "temp_rule_margin_K": ("conductor__temp_rule_margin", 1.0),
        "fraction_rule_margin": ("conductor__fraction_rule_margin", 1.0),
        "acceptance_margin": ("conductor__acceptance_margin", 1.0),
    })
    for r in rows:
        r["reference_acceptance_rule"] = "temperature rule (Tcs − T_conductor ≥ 1.5 K)" if r["material"] == MATERIAL_LABEL["nb3sn"] else "fraction rule (I/Ic ≤ 0.8)"
    write_csv("f4_margins.csv", rows, list(rows[0].keys()))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    ax = axes[0]
    for material in ("nb3sn", "rebco"):
        plot_d_common_p(ax, rows, "operating_fraction", material)
    hline(ax, FRACTION_RULE, "fraction rule: I / Ic(B, T_conductor) ≤ 0.8 (REBCO reference rule)", label_x=0.30, ha="left",
          va="top", dy_pt=-7)
    ax.set_ylabel("Operating fraction I / Ic(B, T_conductor) (1)")
    ax.set_title("Operating fraction")
    ax.set_ylim(0.5, 0.9)
    field_axis(ax)

    ax = axes[1]
    for material in ("nb3sn", "rebco"):
        plot_d_common_p(ax, rows, "temperature_margin_K", material)
    hline(ax, TEMPERATURE_RULE_K, "temperature rule: Tcs − T_conductor ≥ 1.5 K (Nb₃Sn reference rule)")
    ax.set_ylabel("Temperature margin Tcs − T_conductor (K)")
    ax.set_title("Temperature margin")
    ax.set_ylim(0, 6)
    field_axis(ax)
    fig.legend(handles=material_handles() + status_legend_handles(include_unsupported=False), loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, 0.095))
    fig.suptitle("F4 · Current margins versus peak field, anchor D common-P reference offers", x=0.01, ha="left",
                 fontsize=11, color=INK)
    footer(fig, f234_footer(rows) + " · each reference offer is the smallest n meeting its material's reference rule")
    fig.tight_layout(rect=(0, 0.19, 1, 0.95))
    save(fig, "f4_margins")


# --------------------------------------------------------------------------------------
# F5 — cost difference and break-even REBCO price
# --------------------------------------------------------------------------------------

# (anchor, pairing, colour, marker, marker size): D common-P and D native lie within 0.5 % of each
# other at every field, so the native marker is drawn smaller on top of the common-P marker.
F5_PAIRS = [("D", "common-P", BLUE, "o", 7.5), ("D", "native", AQUA, "s", 4.0), ("S", "common-C", VIOLET, "^", 6.0)]
F5_MAX_FIELD = 14.0
NB3SN_PRICE_BAND = (5.4, 13.5)  # USD/m, contract § 7
REBCO_PRICE_LINES = [(10, "10 USD/m (volume)"), (30, "30 USD/m (target)"), (80, "80 USD/m (2021 market)")]


def figure_f5(df, aliases_of):
    ref = reference_offers(df)
    rows = []
    for anchor, pairing, _, _, _ in F5_PAIRS:
        sub = ref[(ref.anchor == anchor) & (ref.pairing == pairing)].sort_values("B_peak")
        for _, r in sub.iterrows():
            rankable = int(r[PAIR["rankable"]])
            rows.append({
                **base_row(r, aliases_of),
                "pair": f"{anchor} {pairing}",
                "rankable": rankable,
                "non_rankable_reason": non_rankable_reason(r),
                "nb3sn_status": status_of(r, "nb3sn"),
                "rebco_status": status_of(r, "rebco"),
                "nb3sn_all_pass": int(r[ch("nb3sn", "all_pass__all_pass")]),
                "rebco_all_pass": int(r[ch("rebco", "all_pass__all_pass")]),
                "cost_difference_MUSD_per_yr": float(r[PAIR["cost_difference"]]) * 1e-6,
                "nb3sn_annualized_cost_MUSD_per_yr": float(r[ch("nb3sn", "annualized__annualized_cost")]) * 1e-6,
                "rebco_annualized_cost_MUSD_per_yr": float(r[ch("rebco", "annualized__annualized_cost")]) * 1e-6,
                "breakeven_rebco_price_USD_per_m": float(r[PAIR["be_per_m"]]),
                "breakeven_rebco_price_USD_per_kAm": float(r[PAIR["be_per_kAm"]]),
                "plotted": int(float(r["B_peak"]) <= F5_MAX_FIELD),
            })
    write_csv("f5_cost_breakeven.csv", rows, list(rows[0].keys()))

    fig, axes = plt.subplots(3, 1, figsize=(9.5, 10.8), sharex=True)
    specs = (
        (axes[0], "cost_difference_MUSD_per_yr", "Annualized cost difference,\nREBCO − Nb₃Sn (M USD2021/yr)",
         "Annualized subsystem cost difference (0.08 × capital + refrigeration electricity)"),
        (axes[1], "breakeven_rebco_price_USD_per_m", "Break-even REBCO tape price (USD2021/m)",
         "Break-even REBCO price per metre of tape (Nb₃Sn at 8 USD/m strand)"),
        (axes[2], "breakeven_rebco_price_USD_per_kAm", "Break-even REBCO price (USD2021/kA·m)",
         "Break-even REBCO price per kA·m at the operating point"),
    )
    # How far the anchor D native series sits from common-P over the plotted fields (it is drawn on top).
    by_field = {(r["pair"], r["B_peak_T"]): r for r in rows if r["plotted"]}
    gaps = [(abs(by_field[("D native", b)]["breakeven_rebco_price_USD_per_m"] - by_field[("D common-P", b)]["breakeven_rebco_price_USD_per_m"]),
             abs(by_field[("D native", b)]["cost_difference_MUSD_per_yr"] - by_field[("D common-P", b)]["cost_difference_MUSD_per_yr"]))
            for (pair, b) in by_field if pair == "D native"]
    gap_be, gap_cost = max(g[0] for g in gaps), max(g[1] for g in gaps)
    handles = []
    for anchor, pairing, color, marker, ms in F5_PAIRS:
        label = f"anchor {anchor}, {pairing}"
        if (anchor, pairing) == ("D", "native"):
            label += f" — drawn over common-P (within {gap_be:.2f} USD/m and {gap_cost:.1f} M USD/yr of it)"
        handles.append(Line2D([], [], color=color, marker=marker, markersize=ms, label=label))
    handles.append(Line2D([], [], color=INK2, marker="o", markerfacecolor="none", linestyle="none",
                          label="hollow: not rankable (reasons in the top panel)"))
    for ax, ycol, ylabel, title in specs:
        for i, (anchor, pairing, color, marker, ms) in enumerate(F5_PAIRS):
            pts = sorted([r for r in rows if r["pair"] == f"{anchor} {pairing}" and r["plotted"]], key=lambda r: r["B_peak_T"])
            x = [r["B_peak_T"] for r in pts]
            y = [r[ycol] for r in pts]
            rk = [r["rankable"] for r in pts]
            # Solid line through rankable points only; non-rankable points hollow, joined by a hairline.
            xr = [xi for xi, k in zip(x, rk) if k]
            yr = [yi for yi, k in zip(y, rk) if k]
            ax.plot(x, y, color=color, linewidth=0.6, alpha=0.5, zorder=2)
            ax.plot(xr, yr, color=color, linewidth=1.4, zorder=3)
            for r, xi, yi in zip(pts, x, y):
                ax.plot([xi], [yi], marker=marker, linestyle="none", markersize=ms, markeredgewidth=1.1,
                        markerfacecolor=color if r["rankable"] else "none", markeredgecolor=color, zorder=4 + i)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left")
    # Why the hollow points carry no ranking, grouped by pair and by runs of fields with one reason.
    lines = ["Not rankable (hollow), by pair:"]
    for anchor, pairing, _, _, _ in F5_PAIRS:
        pts = sorted([r for r in rows if r["pair"] == f"{anchor} {pairing}" and r["plotted"] and not r["rankable"]],
                     key=lambda r: r["B_peak_T"])
        if not pts:
            lines.append(f"  {anchor} {pairing}: none")
            continue
        runs: list[list] = []
        for r in pts:
            if runs and runs[-1][0] == r["non_rankable_reason"] and runs[-1][2] == r["B_peak_T"] - 1:
                runs[-1][2] = r["B_peak_T"]
            else:
                runs.append([r["non_rankable_reason"], r["B_peak_T"], r["B_peak_T"]])
        parts = [f"{a:g} T" if a == b else f"{a:g}–{b:g} T" for _, a, b in runs]
        lines.append(f"  {anchor} {pairing}: " + "; ".join(f"{p} {reason}" for p, (reason, _, _) in zip(parts, runs)))
    axes[0].text(0.99, 0.06, "\n".join(lines), transform=axes[0].transAxes, fontsize=7, color=INK2, ha="right", va="bottom",
                 linespacing=1.35)
    axes[0].axhline(0, color=AXIS, linewidth=1.0, zorder=1)
    axes[0].text(0.01, 0.0, "zero: equal annualized cost", transform=axes[0].get_yaxis_transform(), fontsize=7,
                 color=MUTED, ha="left", va="bottom")
    ax = axes[1]
    ax.axhspan(*NB3SN_PRICE_BAND, color=BAND, alpha=0.6, zorder=0, linewidth=0)
    ax.text(0.01, NB3SN_PRICE_BAND[1], "Nb₃Sn strand price range 5.4–13.5 USD/m", fontsize=7, color=INK2,
            ha="left", va="bottom", transform=ax.get_yaxis_transform())
    for y, label in REBCO_PRICE_LINES:
        if y == 10:  # the line lies inside the shaded band: label it just below the band's lower edge
            hline(ax, y)
            ax.annotate("REBCO " + label + ": dashed line inside the band", xy=(0.99, NB3SN_PRICE_BAND[0]),
                        xycoords=ax.get_yaxis_transform(), xytext=(0, -2), textcoords="offset points", fontsize=7.2,
                        color=INK2, ha="right", va="top", zorder=6)
        else:
            hline(ax, y, "REBCO " + label, label_x=0.01, ha="left")
    ax.set_ylim(0, 90)
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    axes[2].set_ylim(bottom=0)
    field_axis(axes[2], [8, 9, 10, 11, 12, 13, 14])
    axes[2].set_xlim(7.7, 14.3)
    handles.append(Patch(facecolor=BAND, alpha=0.6, label="Nb₃Sn strand price range (contract § 7)"))
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.032), columnspacing=1.2)
    fig.suptitle("F5 · Cost difference and break-even REBCO price versus peak field, reference offers", x=0.01,
                 ha="left", fontsize=11, color=INK)
    footer(fig, "reference offers · reference variant · reference rule family · pairs: anchor D common-P, anchor D native, "
                "anchor S common-C · 16–20 T extension points (Nb₃Sn unsupported, no ranking) are in the CSV with plotted = 0")
    fig.tight_layout(rect=(0, 0.085, 1, 0.965))
    save(fig, "f5_cost_breakeven")


# --------------------------------------------------------------------------------------
# F6 — tornado of the break-even REBCO price at anchor D, 10 T, common-P
# --------------------------------------------------------------------------------------

VARIANT_FAMILIES = [
    ("strand grade", ["nb3sn_strand_OST_TFEU9", "nb3sn_strand_BEAS_TFEU10-12", "nb3sn_strand_BEAS_II_Tsui"]),
    ("strain", ["nb3sn_strain_-0.6pct", "nb3sn_strain_-0.6pct_OST_TFEU9", "nb3sn_strain_-0.6pct_BEAS_TFEU10-12"]),
    ("margin rule", ["rule:both-temperature", "rule:both-fraction", "nb3sn_tcs_6.5K"]),
    ("REBCO shape / anchor / T* / degradation", ["rebco_shape_power_law", "rebco_anchor_225A", "rebco_Tstar_17K",
                                                 "rebco_Tstar_33K", "rebco_degradation_0.80", "rebco_degradation_0.95"]),
    ("steel", ["steel_base_layer1_9.3635", "steel_base_layer8_16.24", "steel_no_field_scaling"]),
    ("copper", ["cu_density_common_100", "cu_density_material_93.4_100"]),
    ("efficiency", ["eta_constant_0.24", "eta_input_power_20K"]),
    ("capital", ["capital_capacity_basis_20K", "combined_unfavourable_20K"]),
    ("cold load", ["cold_load_x0.5", "cold_load_x2"]),
    ("price", ["price_nb3sn_5.4", "price_nb3sn_13.5", "price_rebco_30_target", "price_rebco_10_volume"]),
    ("electricity", ["electricity_30", "electricity_120"]),
    ("capital recovery", ["crf_0.05", "crf_0.11"]),
    ("turn length", ["turn_length_D_45m", "turn_length_D_60m"]),
    ("manufacturing", ["manufacturing_nb3sn_only", "manufacturing_both"]),
]


def figure_f6(df, aliases_of):
    sel = df[(df.anchor == "D") & (df.B_peak == 10.0) & (df.pairing == "common-P") & (df.refrigerator_kind == "reference")]
    by_id = sel.set_index("case_id")
    baseline_id = "D-10T-common-P-reference-none-reference-reference"
    base = by_id.loc[baseline_id]
    base_be = float(base[PAIR["be_per_m"]])
    assert int(base[PAIR["rankable"]]) == 1

    rows = []
    for family, variants in VARIANT_FAMILIES:
        for v in variants:
            if v.startswith("rule:"):
                rf = v.split(":", 1)[1]
                used_id = f"D-10T-common-P-{rf}-none-reference-reference"
                used = by_id.loc[used_id]
                basis = "rule-family reference offer (policy offer under that rule family)"
                other_id = ""
            else:
                reeval_id = f"D-10T-common-P-reference-{v}-reference-reference"
                offer_id = f"D-10T-common-P-reference-{v}-variant-offer-reference"
                reeval, offer = by_id.loc[reeval_id], by_id.loc[offer_id]
                if reeval["candidate_id"] == offer["candidate_id"]:
                    used, used_id, other_id = reeval, reeval_id, offer_id
                    basis = "re-evaluated reference offer (variant offer is an alias of it: policy did not re-select)"
                else:
                    used, used_id, other_id = offer, offer_id, reeval_id
                    basis = "variant offer (policy re-selected: distinct executed point from the re-evaluated reference)"
            be = float(used[PAIR["be_per_m"]])
            rows.append({
                "family": family,
                "variant": v,
                "case_id": used_id,
                "candidate_id": used["candidate_id"],
                "aliases": ";".join(aliases_of[used_id]),
                "case_basis": basis,
                "other_case_id": other_id,
                "other_case_candidate_id": by_id.loc[other_id]["candidate_id"] if other_id else "",
                "other_case_rankable": int(by_id.loc[other_id][PAIR["rankable"]]) if other_id else "",
                "rankable": int(used[PAIR["rankable"]]),
                "breakeven_rebco_price_USD_per_m": be,
                "delta_vs_baseline_USD_per_m": be - base_be,
                "cost_difference_MUSD_per_yr": float(used[PAIR["cost_difference"]]) * 1e-6,
                "baseline_case_id": baseline_id,
                "baseline_breakeven_USD_per_m": base_be,
            })
    cols = list(rows[0].keys())
    write_csv("f6_sensitivities.csv", rows, cols)

    order = sorted(rows, key=lambda r: (-abs(r["delta_vs_baseline_USD_per_m"]), r["variant"]))
    n = len(order)
    fig, ax = plt.subplots(figsize=(9.5, 0.27 * n + 2.6))
    ypos = np.arange(n)[::-1]
    for y, r in zip(ypos, order):
        d = r["delta_vs_baseline_USD_per_m"]
        filled = bool(r["rankable"])
        ax.barh(y, d, left=base_be, height=0.62, color=BLUE if filled else "none", edgecolor=BLUE, linewidth=1.0, zorder=3)
        be = r["breakeven_rebco_price_USD_per_m"]
        txt = f"{be:.2f}" + ("" if filled else "  (not rankable)") + ("  (no change)" if abs(d) < 1e-6 else "")
        ax.text(be + (0.12 if d >= 0 else -0.12), y, txt, va="center", ha="left" if d >= 0 else "right", fontsize=7.2, color=INK2)
    ax.axvline(base_be, color=INK2, linewidth=1.0, zorder=2)
    ax.text(base_be + 0.1, n - 0.2, f"baseline {base_be:.2f} USD/m", ha="left", va="bottom", fontsize=7.5, color=INK2)
    ax.set_yticks(ypos)
    short = {"REBCO shape / anchor / T* / degradation": "REBCO"}
    ax.set_yticklabels([f"{short.get(r['family'], r['family'])}: {r['variant'].replace('rule:', 'rule family ')}" for r in order],
                       fontsize=7.6)
    ax.set_xlabel("Break-even REBCO tape price (USD2021/m); bar from the baseline to the variant's value")
    ax.set_xlim(6, 20)
    ax.grid(axis="y", visible=False)
    ax.set_ylim(-0.8, n + 0.6)
    ax.tick_params(axis="y", length=0)
    fig.suptitle("F6 · Sensitivity of the break-even REBCO price, anchor D, 10 T, common-P, reference rule family",
                 x=0.01, ha="left", fontsize=11, color=INK)
    fig.legend(handles=[Patch(facecolor=BLUE, label="variant value (rankable pair)"),
                        Patch(facecolor="none", edgecolor=BLUE, label="not rankable (hollow)")],
               loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.03))
    footer(fig, "anchor D · 10 T · common-P · reference rule family unless the bar names a rule family · one bar per variant: "
                "the variant-offer case where the policy re-selected, else the re-evaluated reference case (data CSV states which)")
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))
    save(fig, "f6_sensitivities")


# --------------------------------------------------------------------------------------
# Results table (data/results-table.csv)
# --------------------------------------------------------------------------------------


def results_table(df, aliases_of):
    ref = reference_offers(df)
    rows = []
    for anchor, pairing in (("D", "common-P"), ("S", "common-C")):
        sub = ref[(ref.anchor == anchor) & (ref.pairing == pairing) & (ref.B_peak <= 13.0)].sort_values("B_peak")
        for _, r in sub.iterrows():
            row = {**base_row(r, aliases_of), "n_elements_per_turn": "not a cases.csv channel"}
            for material in ("nb3sn", "rebco"):
                m = material
                row.update({
                    f"{m}_status": status_of(r, m),
                    f"{m}_all_pass": int(r[ch(m, "all_pass__all_pass")]),
                    f"{m}_acceptance_margin": float(r[ch(m, "conductor__acceptance_margin")]),
                    f"{m}_temp_rule_margin_K": float(r[ch(m, "conductor__temp_rule_margin")]),
                    f"{m}_fraction_rule_margin": float(r[ch(m, "conductor__fraction_rule_margin")]),
                    f"{m}_fit_margin_mm2": float(r[ch(m, "area__fit_margin")]),
                    f"{m}_p_in_cold_MW": float(r[ch(m, "refrigeration__p_in_cold")]) * 1e-6,
                    f"{m}_p_in_total_MW": float(r[ch(m, "refrigeration__p_in_total_MW")]),
                    f"{m}_capital_total_MUSD2021": float(r[ch(m, "annualized__capital_total")]) * 1e-6,
                    f"{m}_annualized_cost_MUSD_per_yr": float(r[ch(m, "annualized__annualized_cost")]) * 1e-6,
                })
            row.update({
                "rankable": int(r[PAIR["rankable"]]),
                "non_rankable_reason": non_rankable_reason(r),
                "cost_difference_MUSD_per_yr": float(r[PAIR["cost_difference"]]) * 1e-6,
                "breakeven_rebco_price_USD_per_m": float(r[PAIR["be_per_m"]]),
                "breakeven_rebco_price_USD_per_kAm": float(r[PAIR["be_per_kAm"]]),
            })
            rows.append(row)
    write_csv("results-table.csv", rows, list(rows[0].keys()))


# --------------------------------------------------------------------------------------


def main():
    df, aliases_of = load_cases()
    results_table(df, aliases_of)
    figure_f1(df, aliases_of)
    figure_f2(df, aliases_of)
    figure_f3(df, aliases_of)
    figure_f4(df, aliases_of)
    figure_f5(df, aliases_of)
    figure_f6(df, aliases_of)
    print("wrote", sorted(p.name for p in DATA_DIR.iterdir()))
    print("wrote", sorted(p.name for p in HERE.iterdir() if p.suffix in (".svg", ".png")))


if __name__ == "__main__":
    main()
