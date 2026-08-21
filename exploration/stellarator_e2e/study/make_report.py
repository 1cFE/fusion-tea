"""Render the design-search proof-of-life report (study/report.html) from the
committed study CSVs. Pure render step: reads design_search_R_a.csv,
availability_sweep.csv, verification_summary.json; writes report.html.
Regeneration path: uv run python study/make_report.py  (from stellarator_e2e/).

Charts are inline SVG. Palette: validated reference dataviz palette
(sequential blue ramp for LCOE magnitude; chrome/ink tokens for both themes).
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- data -------------------------------------------------------------------
ROWS = list(csv.DictReader((HERE / "design_search_R_a.csv").open()))
AV = list(csv.DictReader((HERE / "availability_sweep.csv").open()))
VER = json.loads((HERE / "verification_summary.json").read_text())

# Grid axis values are the 0.5-step R columns; the appended baseline point
# (R = 12.7) is off-grid and is drawn as a marker, not a cell column.
R_VALUES = sorted(v for v in {float(r["R"]) for r in ROWS}
                  if abs(v * 2 - round(v * 2)) < 1e-9)
A_VALUES = sorted({float(r["a"]) for r in ROWS})
BY_RA = {(float(r["R"]), float(r["a"])): r for r in ROWS}
BASELINE = BY_RA[(12.7, 1.3)]
FEAS = [r for r in ROWS if r["feasible"] == "True"]
BEST = min(FEAS, key=lambda r: float(r["lcoe"]))
CHEAPEST_ANY = min(ROWS, key=lambda r: float(r["lcoe"]))
VIOL = Counter()
for r in ROWS:
    for v in ("net_positive", "recirc_ok", "wall_load_ok", "beta_ok", "tbr_ok"):
        if r[v] != "satisfied":
            VIOL[v] += 1

# --- palette (reference dataviz instance) -----------------------------------
RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
        "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
ACCENT = "#2a78d6"

LC_MIN = min(float(r["lcoe"]) for r in ROWS)
LC_MAX = max(float(r["lcoe"]) for r in ROWS)


def lcoe_color(lcoe: float) -> str:
    t = (math.log(lcoe) - math.log(LC_MIN)) / (math.log(LC_MAX) - math.log(LC_MIN))
    return RAMP[min(int(t * len(RAMP)), len(RAMP) - 1)]


def fmt_money(v: float) -> str:
    return f"${v/1e9:.2f}B"


# --- heatmap ----------------------------------------------------------------
CELL, GAP = 17, 1
ML, MT, MR, MB = 46, 8, 8, 40  # margins: left/top/right/bottom
W = ML + len(R_VALUES) * CELL + MR
H = MT + len(A_VALUES) * CELL + MB


def cell_xy(R: float, a: float) -> tuple[float, float]:
    ix = R_VALUES.index(R)
    iy = A_VALUES.index(a)
    x = ML + ix * CELL
    y = MT + (len(A_VALUES) - 1 - iy) * CELL
    return x, y


def heatmap_svg() -> str:
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="LCOE heatmap over major radius R and minor radius a">']
    parts.append(
        '<defs><pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" '
        'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" '
        'stroke="var(--hatch)" stroke-width="1.4"/></pattern></defs>')
    for r in ROWS:
        R, a = float(r["R"]), float(r["a"])
        if R not in R_VALUES or a not in A_VALUES:
            continue  # the appended off-grid baseline point is drawn as a marker
        x, y = cell_xy(R, a)
        lcoe = float(r["lcoe"])
        fill = lcoe_color(lcoe)
        feasible = r["feasible"] == "True"
        fails = [v for v in ("wall_load_ok", "recirc_ok", "net_positive")
                 if r[v] != "satisfied"]
        tip = (f"R = {R:g} m, a = {a:g} m&#10;LCOE ${lcoe:,.1f}/MWh&#10;"
               f"fusion {float(r['p_fus']):,.0f} MW · wall {float(r['wall_load']):.2f} MW/m²&#10;"
               f"capital {fmt_money(float(r['total_capital']))}&#10;"
               + ("feasible (5/5 satisfied)" if feasible else "INFEASIBLE: " + ", ".join(fails)))
        parts.append(
            f'<rect class="c" x="{x}" y="{y}" width="{CELL-GAP}" height="{CELL-GAP}" '
            f'fill="{fill}" data-tip="{tip}"/>')
        if not feasible:
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL-GAP}" height="{CELL-GAP}" '
                f'fill="url(#hatch)" pointer-events="none"/>')
    # geometric exclusion (self-intersecting torus): dotted outline over gap
    for R in R_VALUES:
        for a in A_VALUES:
            if (R, a) not in BY_RA:
                x, y = cell_xy(R, a)
                parts.append(
                    f'<rect x="{x+3}" y="{y+3}" width="{CELL-GAP-6}" height="{CELL-GAP-6}" '
                    f'fill="none" stroke="var(--muted)" stroke-width="1" '
                    f'stroke-dasharray="2 2" opacity="0.5"/>')
    # markers: baseline + best feasible
    for row, label, dy in ((BASELINE, "Stellaris baseline", -8), (BEST, "best feasible", -8)):
        R, a = float(row["R"]), float(row["a"])
        ix = ML + (R - R_VALUES[0]) / (R_VALUES[-1] - R_VALUES[0]) * (len(R_VALUES) - 1) * CELL + CELL / 2
        iy = MT + (len(A_VALUES) - 1 - (a - A_VALUES[0]) / (A_VALUES[-1] - A_VALUES[0]) * (len(A_VALUES) - 1)) * CELL + CELL / 2
        parts.append(f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="5.5" fill="none" '
                     f'stroke="var(--ink)" stroke-width="2"/>')
        parts.append(f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="7.5" fill="none" '
                     f'stroke="var(--surface)" stroke-width="2"/>')
        anchor = "start" if label == "best feasible" else "end"
        lx = ix + (10 if anchor == "start" else -10)
        parts.append(f'<text x="{lx:.1f}" y="{iy+dy:.1f}" text-anchor="{anchor}" '
                     f'class="lbl">{label}</text>')
    # axes
    for R in R_VALUES:
        if R % 2 == 0:
            x, _ = cell_xy(R, A_VALUES[0])
            parts.append(f'<text x="{x + CELL/2}" y="{H-MB+16}" text-anchor="middle" '
                         f'class="tick">{R:g}</text>')
    parts.append(f'<text x="{ML + (W-ML-MR)/2}" y="{H-6}" text-anchor="middle" class="axis">'
                 f'major radius R (m)</text>')
    for a in A_VALUES:
        if round(a * 100) % 20 == 0:
            _, y = cell_xy(R_VALUES[0], a)
            parts.append(f'<text x="{ML-8}" y="{y + CELL/2 + 4}" text-anchor="end" '
                         f'class="tick">{a:g}</text>')
    parts.append(f'<text transform="translate(12 {MT + (H-MT-MB)/2}) rotate(-90)" '
                 f'text-anchor="middle" class="axis">minor radius a (m)</text>')
    parts.append("</svg>")
    return "".join(parts)


def colorbar_svg() -> str:
    w, h, sw = 420, 46, 420 / len(RAMP)
    parts = [f'<svg viewBox="0 0 {w+60} {h}" role="img" aria-label="LCOE color scale">']
    for i, c in enumerate(RAMP):
        parts.append(f'<rect x="{30 + i*sw:.1f}" y="8" width="{sw-1:.1f}" height="14" fill="{c}"/>')
    for val in (175, 250, 400, 700, 1500, 3000, 6000):
        t = (math.log(val) - math.log(LC_MIN)) / (math.log(LC_MAX) - math.log(LC_MIN))
        if 0 <= t <= 1:
            x = 30 + t * 420
            parts.append(f'<line x1="{x:.1f}" y1="22" x2="{x:.1f}" y2="27" stroke="var(--muted)"/>')
            parts.append(f'<text x="{x:.1f}" y="40" text-anchor="middle" class="tick">{val:,}</text>')
    parts.append(f'<text x="30" y="40" text-anchor="end" class="tick"></text>')
    parts.append("</svg>")
    return "".join(parts)


def minimap_svg(verdict: str, title: str) -> str:
    c, m = 8, 30
    w = m + len(R_VALUES) * c + 6
    h = 22 + len(A_VALUES) * c + 18
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{title}">']
    parts.append(f'<text x="{m}" y="14" class="lbl">{title}</text>')
    for r in ROWS:
        R, a = float(r["R"]), float(r["a"])
        if R not in R_VALUES or a not in A_VALUES:
            continue
        x = m + R_VALUES.index(R) * c
        y = 22 + (len(A_VALUES) - 1 - A_VALUES.index(a)) * c
        bad = r[verdict] != "satisfied"
        fill = ACCENT if bad else "var(--cell-ok)"
        parts.append(f'<rect x="{x}" y="{y}" width="{c-1}" height="{c-1}" fill="{fill}"/>')
    parts.append(f'<text x="{m}" y="{h-4}" class="tick">R 4→20 m · a 0.8→2.2 m</text>')
    parts.append("</svg>")
    return "".join(parts)


def availability_svg() -> str:
    w, h, ml, mt, mr, mb = 640, 300, 56, 16, 16, 44
    xs = [float(r["availability"]) for r in AV]
    ys = [float(r["lcoe"]) for r in AV]
    x0, x1 = min(xs), max(xs)
    y0, y1 = 220, 480
    def X(v): return ml + (v - x0) / (x1 - x0) * (w - ml - mr)
    def Y(v): return mt + (y1 - v) / (y1 - y0) * (h - mt - mb)
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" '
             f'aria-label="LCOE versus availability at baseline geometry">']
    for gv in range(250, 500, 50):
        parts.append(f'<line x1="{ml}" y1="{Y(gv):.1f}" x2="{w-mr}" y2="{Y(gv):.1f}" '
                     f'stroke="var(--grid)" stroke-width="1"/>')
        parts.append(f'<text x="{ml-8}" y="{Y(gv)+4:.1f}" text-anchor="end" class="tick">{gv}</text>')
    pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in zip(xs, ys))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="{ACCENT}" '
                 f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for x, y, r in zip(xs, ys, AV):
        tip = (f"availability {x:g}&#10;LCOE ${y:,.2f}/MWh&#10;"
               + ("feasible" if r["feasible"] == "True" else "infeasible"))
        parts.append(f'<circle class="c" cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" fill="{ACCENT}" '
                     f'stroke="var(--surface)" stroke-width="2" data-tip="{tip}"/>')
    bx, by = X(0.85), Y(float(BASELINE["lcoe"]))
    parts.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="7" fill="none" '
                 f'stroke="var(--ink)" stroke-width="2"/>')
    parts.append(f'<text x="{bx:.1f}" y="{by-14:.1f}" text-anchor="middle" class="lbl">'
                 f'baseline 0.85 → $275.26</text>')
    for xv in (0.5, 0.6, 0.7, 0.8, 0.9):
        parts.append(f'<text x="{X(xv):.1f}" y="{h-mb+18}" text-anchor="middle" '
                     f'class="tick">{xv:g}</text>')
    parts.append(f'<text x="{ml + (w-ml-mr)/2}" y="{h-6}" text-anchor="middle" class="axis">'
                 f'availability (capacity factor lever)</text>')
    parts.append(f'<text transform="translate(14 {mt + (h-mt-mb)/2}) rotate(-90)" '
                 f'text-anchor="middle" class="axis">LCOE ($/MWh)</text>')
    parts.append("</svg>")
    return "".join(parts)


# --- assemble ---------------------------------------------------------------
def stat(label: str, value: str, note: str) -> str:
    return (f'<div class="stat"><div class="stat-label">{label}</div>'
            f'<div class="stat-value">{value}</div><div class="stat-note">{note}</div></div>')


best_R, best_a = float(BEST["R"]), float(BEST["a"])
best_lcoe = float(BEST["lcoe"])
bl_lcoe = float(BASELINE["lcoe"])
delta_pct = 100 * (best_lcoe - bl_lcoe) / bl_lcoe
cheap_lcoe = float(CHEAPEST_ANY["lcoe"])

HTML = f"""<title>Stellarator design search — proof of life</title>
<style>
:root {{
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --hairline: rgba(11,11,11,0.10);
  --accent: {ACCENT}; --cell-ok: #eceae4; --hatch: rgba(11,11,11,0.45);
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) {{
    --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink2: #c3c2b7;
    --muted: #898781; --grid: #2c2c2a; --hairline: rgba(255,255,255,0.10);
    --accent: #3987e5; --cell-ok: #262624; --hatch: rgba(255,255,255,0.55);
  }}
}}
:root[data-theme="dark"] {{
  --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink2: #c3c2b7;
  --muted: #898781; --grid: #2c2c2a; --hairline: rgba(255,255,255,0.10);
  --accent: #3987e5; --cell-ok: #262624; --hatch: rgba(255,255,255,0.55);
}}
body {{ background: var(--page); color: var(--ink);
  font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; margin: 0; }}
main {{ max-width: 880px; margin: 0 auto; padding: 40px 24px 80px; }}
h1 {{ font-size: 28px; line-height: 1.2; margin: 0 0 4px; text-wrap: balance; }}
h2 {{ font-size: 19px; margin: 44px 0 10px; }}
p, li {{ max-width: 72ch; color: var(--ink); }}
.eyebrow {{ font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--ink2); margin: 0 0 10px; }}
.sub {{ color: var(--ink2); margin: 0 0 28px; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px; margin: 24px 0 8px; }}
.stat {{ background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 6px; padding: 14px 16px; }}
.stat-label {{ font-size: 12.5px; color: var(--ink2); }}
.stat-value {{ font-size: 24px; font-weight: 600; margin: 2px 0; }}
.stat-note {{ font-size: 12.5px; color: var(--muted); }}
figure {{ margin: 18px 0; background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 6px; padding: 16px; overflow-x: auto; }}
figcaption {{ font-size: 13px; color: var(--ink2); margin-top: 8px; max-width: 72ch; }}
svg {{ display: block; max-width: 100%; height: auto; }}
svg .tick {{ font: 11px system-ui, sans-serif; fill: var(--muted);
  font-variant-numeric: tabular-nums; }}
svg .axis {{ font: 12.5px system-ui, sans-serif; fill: var(--ink2); }}
svg .lbl {{ font: 600 12px system-ui, sans-serif; fill: var(--ink);
  paint-order: stroke; stroke: var(--surface); stroke-width: 3px;
  stroke-linejoin: round; }}
.minimaps {{ display: flex; gap: 16px; flex-wrap: wrap; }}
.minimaps figure {{ flex: 1 1 260px; margin: 0; }}
table {{ border-collapse: collapse; font-size: 14.5px; margin: 12px 0;
  font-variant-numeric: tabular-nums; }}
th, td {{ text-align: left; padding: 7px 14px 7px 0; border-bottom: 1px solid var(--grid); }}
th {{ font-size: 12.5px; color: var(--ink2); font-weight: 600; }}
code, .mono {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 0.92em; }}
pre {{ background: var(--surface); border: 1px solid var(--hairline); border-radius: 6px;
  padding: 12px 16px; overflow-x: auto; font-size: 13.5px; }}
.caveat li {{ margin-bottom: 10px; }}
#tt {{ position: fixed; display: none; background: var(--ink); color: var(--page);
  padding: 8px 11px; border-radius: 5px; font-size: 12.5px; line-height: 1.45;
  pointer-events: none; white-space: pre; z-index: 10; max-width: 320px;
  font-variant-numeric: tabular-nums; }}
.legend {{ display: flex; gap: 22px; flex-wrap: wrap; font-size: 13px;
  color: var(--ink2); margin: 6px 0 0; align-items: center; }}
.legend .sw {{ display: inline-block; width: 14px; height: 14px; border-radius: 3px;
  vertical-align: -2px; margin-right: 6px; }}
a {{ color: var(--accent); }}
</style>
<main>
<p class="eyebrow">Fusion TEA · stellarator MBSE demo · 2026-08-16</p>
<h1>Stellarator design search — proof of life</h1>
<p class="sub">{len(ROWS) + len(AV)} plant designs evaluated end-to-end through the
generated SysML pipeline and the stock teax study layer, classified by the model's
own viability constraints, and verified against an independent oracle.</p>

<div class="stats">
{stat("Design points evaluated", f"{len(ROWS) + len(AV)}", f"{len(ROWS)-1}-cell (R, a) grid + baseline + 19-point availability sweep")}
{stat("Baseline reproduced", "$275.264220", "pinned WI-029 headline LCOE, exact")}
{stat("Best feasible point found", f"${best_lcoe:,.2f}/MWh", f"{delta_pct:+.0f}% vs baseline, at R = {best_R:g} m, a = {best_a:g} m")}
{stat("Worst oracle deviation", f"{VER['worst_channel_rel_dev']:.1e}", f"{2*VER['sampled_rows_per_study']} sampled points, 5 channels, tolerance 1e-9")}
</div>

<h2>What this is</h2>
<p>The demo asks one thing of the toolchain: author a fusion power plant as a SysML&nbsp;v2
model, generate executable code from it, and then <em>search the design space</em> —
vary design levers, and get back cost and feasibility for every candidate. Cost here
is the levelized cost of electricity (LCOE, $/MWh — lifetime cost per delivered
megawatt-hour). This report is the first end-to-end run of that loop on the
stellarator (Stellaris, concept-09).</p>
<p>Three layers did the work — none of the study machinery was hand-rolled
(the small documented glue harness is itemized in the caveats):</p>
<ul>
<li>The <strong>SysML model</strong> owns the meaning: plasma geometry, profile-integrated
fusion power, power balance, the full cost-account stack (CAS — the standard fusion
cost breakdown), LCOE, and five viability constraints (beta limit, wall load,
tritium breeding, recirculation, net power).</li>
<li>The <strong>generated package</strong> (sysml-codegen, sealed July build) owns evaluation —
the same package that reproduces the pinned $275.26/MWh headline bit-exact.</li>
<li>The <strong>study layer of teax</strong> (the evaluation toolkit) owns exploration,
pinned to the package's era (see caveats): stock
<span class="mono">PreparedListStrategy → StudyRunner → StudyStore → StudyQuery</span>,
with every swept SysML attribute expanded to its complete set of generated input keys.</li>
</ul>
<p>Every point carries the model's own verdict for all five constraints, plus recorded
outputs (LCOE, fusion power, wall load, capital). Nothing here is tuned to a result:
the two study axes are causal design levers (the machine's major and minor radius),
and the constraint set is exactly what the model already asserted.</p>

<h2>The design map</h2>
<p>Each cell is one plant design at that (R, a); everything else is held at the
Stellaris baseline. Color is LCOE (log scale — dark is expensive). Hatched cells are
designs the model itself rejects; the dotted corner is geometrically impossible
(the radial build no longer fits inside the major radius).</p>
<figure>
{heatmap_svg()}
{colorbar_svg()}
<div class="legend">
<span>LCOE $/MWh, log scale</span>
<span><span class="sw" style="background:repeating-linear-gradient(45deg, var(--surface), var(--surface) 2px, var(--hatch) 2px, var(--hatch) 3px); border:1px solid var(--hairline)"></span>infeasible (model verdict)</span>
<span><span class="sw" style="border:1.5px dashed var(--muted)"></span>geometry impossible</span>
</div>
<figcaption>LCOE over the (R, a) window, {len(ROWS)} evaluated designs,
{len(FEAS)} feasible ({100*len(FEAS)/len(ROWS):.0f}%). Hover any cell for its numbers.</figcaption>
</figure>

<p>Three things the search found:</p>
<ul>
<li><strong>The wall-load limit is the active fence.</strong> {VIOL['wall_load_ok']} of
{sum(VIOL.values())} constraint violations are the neutron wall load exceeding the
sourced 4.05&nbsp;MW/m² limit. LCOE keeps falling as the plasma gets fatter: the
cheapest point in the window is ${cheap_lcoe:,.0f}/MWh at
R&nbsp;=&nbsp;{float(CHEAPEST_ANY['R']):g}, a&nbsp;=&nbsp;{float(CHEAPEST_ANY['a']):g},
at wall load {float(CHEAPEST_ANY['wall_load']):.2f} — and the model correctly fences
that whole region off.</li>
<li><strong>The best feasible design sits on the boundary.</strong>
R&nbsp;=&nbsp;{best_R:g}&nbsp;m, a&nbsp;=&nbsp;{best_a:g}&nbsp;m gives
${best_lcoe:,.2f}/MWh ({delta_pct:+.0f}% vs the authored baseline) at wall load
{float(BEST['wall_load']):.3f} of 4.05 — the classic signature of a constrained
optimum, found by the model's own verdicts, not by a hand rule.</li>
<li><strong>Recirculation kills the small-machine corner.</strong> {VIOL['recirc_ok']}
small-R·a designs fail the economic recirculation threshold — Q<sub>eng</sub>, the
plant's engineering gain (gross electric over recirculated power), must be at least 2 —
before net power even goes negative. Net-positive never fires in this window, and
the beta and TBR verdicts cannot move on these axes (they are bound design inputs;
see caveats).</li>
</ul>

<div class="minimaps">
<figure>{minimap_svg("wall_load_ok", "Where the wall-load limit fails")}</figure>
<figure>{minimap_svg("recirc_ok", "Where recirculation fails (Q_eng < 2)")}</figure>
</div>

<h2>The availability sweep</h2>
<p>A second study exercises a non-geometry lever: availability. The package carries
this one attribute as four separate input keys (fuel throughput, scheduled
replacement, both LCOE forms) — the known duplicated-input defect, where mutating
one copy leaves the rest stale. The study layer moves all four together, closing
the defect at the study surface (see caveats for what remains untied).</p>
<figure>
{availability_svg()}
<figcaption>LCOE at baseline geometry, availability 0.50 → 0.95:
${float(AV[0]['lcoe']):,.0f} → ${float(AV[-1]['lcoe']):,.0f}/MWh. The 0.85 point
is the Stellaris baseline and reproduces the pinned headline to all recorded digits.
The slope kink near 0.775 is the scheduled-replacement count stepping (a ceiling
function in the model) — real model behavior, not noise.</figcaption>
</figure>

<h2>Verification</h2>
<table>
<tr><th>Check</th><th>Result</th></tr>
<tr><td>Baseline point vs the pinned headline from the July certification run (WI-029)</td>
<td>LCOE $275.264220042 — matches to all recorded digits; 5/5 verdicts satisfied</td></tr>
<tr><td>{2*VER['sampled_rows_per_study']} randomly sampled points (12 per study,
stratified so every observed verdict outcome is covered) vs the independent oracle
(<span class="mono">verify_stellaris.py</span>), 5 channels each</td>
<td>worst relative deviation {VER['worst_channel_rel_dev']:.1e} (tolerance 1e-9)</td></tr>
<tr><td>All 5 verdicts re-derived from oracle operands and the package's bound limits</td>
<td>match the package's ConstraintReport at every sample</td></tr>
<tr><td>Committed generated package after all runs</td>
<td>byte-untouched (git-clean gate)</td></tr>
<tr><td>Study machinery</td>
<td>stock teax study layer; zero hand-rolled sweep loops</td></tr>
</table>
<p>The oracle is a line-by-line pure-Python mirror of the SysML calc definitions,
written independently of the generated code. Channels checked: LCOE, fusion power,
magnet capital, total capital, wall load. One ingredient sits outside this check's
independence: the CAS27 special-materials cost is supplied by the same formula on
both sides (see caveats).</p>

<h2>What this does not prove (read before quoting)</h2>
<ul class="caveat">
<li><strong>The package runs at its own era, behind a scoped seal exception.</strong>
Current teax refuses this July package's v1.0.0 seal (a deliberate fail-closed
version gate). The studies ran on a read-only teax worktree pinned to the era that
built and certified this package, through a small harness-side wrapper around the
era's loader (GlueAwareLoader, <span class="mono">study/run_design_search.py</span>).
Two files differ from their sealed hashes — exactly the two the documented harness
glue edits; the loader verifies every other artifact and refuses anything beyond
those two. Regenerating the package on the current toolchain is known upstream work,
currently parked (unowned, behind a July hold): the current code generator refuses
the canonical stellarator models — at least 114 uses of a modeling pattern it no
longer accepts (self-binding), counting only the first diagnostic class.</li>
<li><strong>Three values are harness-supplied per point (glue), not model-computed:</strong>
the CAS27 special-materials cost (recomputed per point from the blanket volume — the
package cannot wire it cross-part, so the oracle check does not independently verify
this one ingredient), the CAS28 digital-twin constant, and a replacement-schedule
module count. All inherited from the documented glue ledger of the July build items
(WI-018/028/029).</li>
<li><strong>Only the three declared axes are safe to sweep.</strong> R, a, and
availability carry complete attribute→entry-key expansion maps; the package's
remaining duplicated input keys (interest rate ×4, operational years ×4, and others)
are untied, so sweeping anything else would silently leave stale siblings. The
expansion completeness check is name-based; <span class="mono">magnet__R0</span>
rides with R as a hand-declared physical-identity tie (the magnet-cost current runs
on the major radius), and known semantic duplicates under different names are held
fixed (installed heating power appears twice; one fraction appears at two
precisions).</li>
<li><strong>Interest rate is deliberately not swept.</strong> The model's
levelization calc lacks a guard for the degenerate case where interest rate
approaches the inflation rate — a known library gap that only a regenerated package
can fix.</li>
<li><strong>This is a power-balance-and-cost feasibility map under an assumed plasma.</strong>
Density and temperature profiles, heating power, cryo loads, and the magnet shape
factor are held at Stellaris baseline values at every point; no confinement-scaling
constraint (e.g. ISS04) exists in the model yet, so nothing asks whether the assumed
plasma is achievable at each geometry. Beta and TBR are bound design inputs — their
verdicts cannot flip on these axes.</li>
<li><strong>The sweep window is engineered.</strong> Ranges were chosen by oracle
pre-scan so the constraint boundaries sit in frame; the feasible fraction (59%) is a
property of the window, not a finding about stellarators.</li>
<li><strong>The study store records only single-number outputs</strong> at this
toolchain version: net electric power and Q<sub>eng</sub> reach the record through
their verdicts, not as stored numbers.</li>
<li><strong>This is a first cut of the demo epic's design-search items, not their
close-out.</strong> The instance-swap (A/B) study, the formal review and
policy-ratification step, and the search-process animation remain open.</li>
</ul>

<h2>Reproduce</h2>
<p>Prerequisite: a read-only teax worktree at commit <span class="mono">fa0e06a</span>
at <span class="mono">/home/reid/1cfe/teax-v1-era</span> (the era pin — see the
script docstring). On a machine without it, create one with
<span class="mono">git worktree add ../teax-v1-era fa0e06a</span> from the teax repo.</p>
<pre>cd exploration/stellarator_e2e
uv run python study/run_design_search.py run     # both studies + gates (~2 min)
uv run python study/run_design_search.py verify  # oracle spot-checks
uv run python study/make_report.py               # this report</pre>
<p class="sub">Committed artifacts: <span class="mono">study/design_search_R_a.csv</span>,
<span class="mono">study/availability_sweep.csv</span>,
<span class="mono">study/verification_summary.json</span>. Study definitions carry the
package's executable fingerprint and the model-contract fingerprint.</p>
</main>
<div id="tt"></div>
<script>
const tt = document.getElementById("tt");
document.querySelectorAll("[data-tip]").forEach(el => {{
  el.addEventListener("mousemove", e => {{
    tt.textContent = el.dataset.tip;
    tt.style.display = "block";
    const x = Math.min(e.clientX + 14, window.innerWidth - tt.offsetWidth - 8);
    const y = Math.min(e.clientY + 14, window.innerHeight - tt.offsetHeight - 8);
    tt.style.left = x + "px"; tt.style.top = y + "px";
  }});
  el.addEventListener("mouseleave", () => tt.style.display = "none");
}});
</script>
"""

(HERE / "report.html").write_text(HTML)
print(f"wrote {HERE/'report.html'} ({len(HTML):,} bytes)")
