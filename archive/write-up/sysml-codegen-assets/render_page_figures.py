"""Render the figures that the HTML page adds or redraws, and inline them into the page.

Run from the repository root:
  uv run python archive/write-up/sysml-codegen-assets/render_page_figures.py

Writes, next to this script (all new files; the markdown's figures are untouched):
  page-calculation-graph.svg      Figure 5, the magnet graph from graph-evidence.json, in the page's fonts
  page-winding-pack-fit.svg       Figure 4, what the fit calculation compares (mfe_winding_pack_fit.sysml equations)
  page-fit-case-*.svg             Figure 10, each recorded case's required envelope against its clear cavity
  page-breeding-response.svg      Figure 7, the five stored transport results and the interpolated response
  page-feasibility-cost.svg       Figure 11, the 17 September map, one SVG group per evaluated case, with text
                                  labels where each limit bites
  page-feasibility-cost-stacked.svg  the same map with the panels stacked, for narrow screens
  page-map-data.json              the map's cases, as the page's readout needs them

Then, if the published page docs/exploratory-modeling/part-2-model-execution.html exists, replaces the content between its
<!-- inline:NAME --> and <!-- /inline:NAME --> markers with the file NAME, so the page embeds
the SVG text and the browser draws it with the page's own fonts.

Facts come from the retained evidence only: graph-evidence.json, feasibility-cost-map.csv,
magnet-sizing-comparison.csv, the study report's fit margins, breeding_response.json (through the
handwritten function's embedded table) and the normative equations documented in
models/library/analyses/mfe_winding_pack_fit.sysml. No model is executed here.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRITEUP = HERE.parent
ROOT = WRITEUP.parents[1]
sys.path.insert(0, str(WRITEUP))
import figure_style as fs  # noqa: E402

PAGE = ROOT / "docs/exploratory-modeling/part-2-model-execution.html"
SANS = f"{fs.SANS}, 'Helvetica Neue', Arial, sans-serif"
MONO = f"'{fs.MONO}', ui-monospace, Menlo, Consolas, monospace"

# Colors beyond figure_style, all taken from write-up.css.
ACCENT_SOFT = "#d5e6f3"
SURFACE_2 = "#eae6e0"
FAINT = "#6e6961"
CODE_BG = "#e6e2dc"
# The three failing-check classes of the map, validated as an all-pairs categorical set on the plate
# (dataviz validator: CVD dE 8.4, normal dE 17.2, contrast >= 3:1). Passing marks keep the data role's teal
# and differ by shape.
CLASS_FIELD = fs.ROLE_CALC      # peak_field_ok fails
CLASS_DIVERTOR = fs.ROLE_CHECK  # divertor_heat_ok fails alone
CLASS_DIV_HEAT = "#8a2a6b"      # divertor_heat_ok and sustainment_ok fail


# ----------------------------------------------------------------------------------------------
# Small SVG builder for the hand-drawn figures
# ----------------------------------------------------------------------------------------------

class Svg:
    def __init__(self, w: float, h: float, title: str, desc: str, cls: str = ""):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{esc(title)}" class="{cls}" font-family="{esc(SANS)}" font-size="14">',
            f"<title>{esc(title)}</title><desc>{esc(desc)}</desc>",
        ]

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1.0, dash=None, rx=0, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        r = f' rx="{rx}"' if rx else ""
        self.parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{sw}"{d}{r}{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=fs.EDGE, sw=1.0, dash=None, marker=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-start="url(#{marker})" marker-end="url(#{marker})"' if marker else ""
        self.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" '
                          f'stroke-width="{sw}"{d}{m}/>')

    def text(self, x, y, s, size=14, fill=fs.INK, anchor="start", weight=None, mono=False, extra=""):
        w = f' font-weight="{weight}"' if weight else ""
        f = f' font-family="{esc(MONO)}"' if mono else ""
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                          f'text-anchor="{anchor}"{w}{f}{extra}>{esc(s)}</text>')

    def raw(self, s):
        self.parts.append(s)

    def dims_marker(self, name="dim", color=fs.MUTED):
        self.raw(f'<defs><marker id="{name}" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" '
                 f'markerHeight="6" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9" fill="none" '
                 f'stroke="{color}" stroke-width="1.5"/></marker></defs>')

    def dim_h(self, x1, x2, y, label, color=fs.MUTED, size=12, marker="dim", above=True):
        self.line(x1, y, x2, y, stroke=color, sw=1, marker=marker)
        self.text((x1 + x2) / 2, y - 5 if above else y + 14, label, size=size, fill=color, anchor="middle")

    def dim_v(self, x, y1, y2, label, color=fs.MUTED, size=12, marker="dim"):
        self.line(x, y1, x, y2, stroke=color, sw=1, marker=marker)
        self.text(x + 6, (y1 + y2) / 2 + 4, label, size=size, fill=color)

    def write(self, path: Path):
        path.write_text("\n".join(self.parts + ["</svg>"]) + "\n")


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ----------------------------------------------------------------------------------------------
# Figure 5: the magnet calculation graph (Graphviz, page fonts and colors)
# ----------------------------------------------------------------------------------------------

LABELS = {
    "radial_build": "Radial build\nCoil position", "field_calc": "Axis field",
    "coil_length": "Coil length", "peak_field_calc": "Peak conductor\nfield",
    "current_sizing": "Current-driven\npack sizing", "wp_sizing": "Winding-pack\nside length",
    "wp_fit": "Pack / casing\nfit margins", "wp_volume": "Winding-pack\nvolume",
    "material_inventory": "Material\ninventory", "winding_procurement": "Winding quantities\nand cost",
    "conductor_current": "Conductor\ncurrent margin", "peak_field_ok": "CHECK\nField limit",
    "reference_conductor_current_ok": "CHECK\nCurrent margin", "wp_fit_ok": "CHECK\nPack fits casing",
}


def calculation_graph():
    data = json.loads((HERE / "graph-evidence.json").read_text())
    lines = [
        "digraph G {",
        f'graph [rankdir=TB, bgcolor="transparent", pad="0.15", nodesep="0.5", ranksep="0.48", splines=polyline, '
        f'fontname="{fs.SANS}", fontsize=14, fontcolor="{fs.INK}", labelloc=t, '
        f'label="How magnet calculations depend on one another\\n "];',
        f'node [shape=box, style="rounded,filled", fillcolor="{fs.ROLE_CALC_FILL}", color="{fs.ROLE_CALC}", '
        f'fontcolor="{fs.INK}", fontname="{fs.SANS}", fontsize=11.5, margin="0.18,0.1", penwidth=1.1];',
        f'edge [color="{fs.EDGE}", arrowsize=0.7, penwidth=1.1];',
    ]
    for n in data["nodes"]:
        if n["kind"] == "constraint":
            color, fill = fs.ROLE_CHECK, fs.ROLE_CHECK_FILL
        elif n["id"] == "winding_procurement":
            color, fill = fs.ROLE_DATA, fs.ROLE_DATA_FILL
        else:
            color, fill = fs.ROLE_CALC, fs.ROLE_CALC_FILL
        lines.append(f'{n["id"]} [label={json.dumps(LABELS[n["id"]])},color="{color}",fillcolor="{fill}"];')
    pairs = set()
    for e in data["edges"]:
        assert e["collapsed"] is False
        pair = (e["source"], e["target"])
        if pair in pairs:
            continue
        attrs = (f' [label="Tape + conductor lengths", fontname="{fs.SANS}", fontsize=10.5, '
                 f'fontcolor="{fs.MUTED}"]') if pair == ("winding_procurement", "conductor_current") else ""
        lines.append(f"{pair[0]} -> {pair[1]}{attrs};")
        pairs.add(pair)
    lines += [
        "{rank=same; radial_build; field_calc;}",
        "{rank=same; wp_fit; wp_volume;}",
        "}",
    ]
    dot = HERE / "page-calculation-graph.dot"
    dot.write_text("\n".join(lines) + "\n")
    out = subprocess.run(["dot", "-Tsvg", str(dot)], check=True, capture_output=True, text=True,
                         env=fs.graphviz_env()).stdout
    svg = out[out.index("<svg"):]
    svg = re.sub(r"<!--.*?-->\n?", "", svg, flags=re.S)
    svg = svg.replace("<svg ", '<svg role="img" aria-label="Actual magnet calculation dependencies: field feeds '
                      'sizing; pack dimensions feed fit and material costs; separate checks assess field, current, '
                      'and fit." ', 1)
    (HERE / "page-calculation-graph.svg").write_text(svg)


# ----------------------------------------------------------------------------------------------
# Figure 4: what the fit calculation compares (generic proportions, names only)
# ----------------------------------------------------------------------------------------------

def fit_schematic():
    # Generic dimensions in metres, exaggerated so every layer is visible. No values are printed.
    wall, ins, clr = 0.05, 0.035, 0.025
    pack_x, pack_y = 0.42, 0.50
    cav_x, cav_y = 0.62, 0.72
    req_x, req_y = pack_x + 2 * (ins + clr), pack_y + 2 * (ins + clr)
    S = 380  # px per metre
    W, H = 980, 438
    ox, oy = 292, 104  # exterior top-left
    ext_x, ext_y = cav_x + 2 * wall, cav_y + 2 * wall
    svg = Svg(W, H, "What the fit calculation compares",
              "Cross-section of a magnet coil: the casing wall encloses a cavity; inside it, centred, the winding "
              "pack is wrapped in ground insulation and an assembly clearance on every face. The required envelope "
              "is the pack plus those allowances. The radial margin is the cavity's radial width minus the "
              "required radial width; the transverse margin is the same in the transverse direction. The check "
              "reads the smaller of the two.", cls="fig-fit")
    svg.dims_marker()
    ex, ey = ox, oy
    cx, cy = ox + wall * S, oy + wall * S
    rx, ry = cx + (cav_x - req_x) / 2 * S, cy + (cav_y - req_y) / 2 * S
    ix, iy = rx + clr * S, ry + clr * S
    px, py = ix + ins * S, iy + ins * S
    # casing and cavity
    svg.rect(ex, ey, ext_x * S, ext_y * S, fill=SURFACE_2, stroke=fs.EDGE, sw=1.2, rx=3)
    svg.rect(cx, cy, cav_x * S, cav_y * S, fill=fs.PLATE, stroke=fs.RULE, sw=1)
    # margin band: the cavity area outside the required envelope
    svg.raw(f'<path d="M{cx:.1f},{cy:.1f}h{cav_x*S:.1f}v{cav_y*S:.1f}h{-cav_x*S:.1f}z '
            f'M{rx:.1f},{ry:.1f}v{req_y*S:.1f}h{req_x*S:.1f}v{-req_y*S:.1f}z" fill="{fs.ROLE_CHECK_FILL}" '
            f'fill-rule="evenodd" opacity="0.8"/>')
    # required envelope, clearance, insulation, pack
    svg.rect(rx, ry, req_x * S, req_y * S, fill="none", stroke=fs.ROLE_CHECK, sw=1.6, dash="6 4")
    svg.rect(ix, iy, (pack_x + 2 * ins) * S, (pack_y + 2 * ins) * S, fill="#f1ede6", stroke=fs.EDGE, sw=0.8)
    svg.rect(px, py, pack_x * S, pack_y * S, fill=ACCENT_SOFT, stroke=fs.ROLE_CALC, sw=1.4)
    svg.text(px + pack_x * S / 2, py + pack_y * S / 2 - 4, "winding pack", size=15, anchor="middle", weight=600)
    svg.text(px + pack_x * S / 2, py + pack_y * S / 2 + 16, "nominal + internal build", size=14, fill=fs.MUTED,
             anchor="middle")
    svg.text(cx + cav_x * S / 2, ry - 8, "margin, split over both sides", size=14, fill=fs.ROLE_CHECK, anchor="middle")
    # dimension lines: widths above, heights at right, with the vertical labels along their lines
    top = ey - 14
    svg.dim_h(cx, cx + cav_x * S, top - 26, "cavity_x  =  radial_allocation − 2 × wall_thickness", size=14)
    svg.dim_h(rx, rx + req_x * S, top, "required_x", color=fs.ROLE_CHECK, size=14)
    right = ex + ext_x * S + 18
    svg.line(right, cy, right, cy + cav_y * S, stroke=fs.MUTED, sw=1, marker="dim")
    svg.text(right + 15, cy + cav_y * S / 2, "cavity_y  =  interior_y", size=14, fill=fs.MUTED, anchor="middle",
             extra=f' transform="rotate(-90 {right + 15:.1f} {cy + cav_y * S / 2:.1f})"')
    r2 = right + 40
    svg.line(r2, ry, r2, ry + req_y * S, stroke=fs.ROLE_CHECK, sw=1, marker="dim")
    svg.text(r2 + 15, ry + req_y * S / 2, "required_y", size=14, fill=fs.ROLE_CHECK, anchor="middle",
             extra=f' transform="rotate(-90 {r2 + 15:.1f} {ry + req_y * S / 2:.1f})"')
    # leader labels on the left, staggered so none collide
    lx = ex - 16
    targets = [
        (ex + wall * S / 2, "casing wall", "wall_thickness, each radial side"),
        (rx + clr * S / 2, "assembly clearance", "assembly_clearance, each face"),
        (ix + ins * S / 2, "ground insulation", "ground_insulation, each face"),
    ]
    for k, (tx, label, sub) in enumerate(targets):
        y = cy + 40 + k * 70
        svg.text(lx, y, label, size=14, anchor="end", weight=600)
        svg.text(lx, y + 18, sub, size=14, fill=fs.MUTED, anchor="end")
        svg.line(lx + 6, y - 4, tx, y - 4, stroke=fs.EDGE, sw=0.8)
        svg.raw(f'<circle cx="{tx:.1f}" cy="{y - 4:.1f}" r="2.2" fill="{fs.EDGE}"/>')
    # the margins, spelled out to the right
    bx = r2 + 46
    by = cy + 24
    svg.rect(bx - 10, by - 22, W - bx - 2, 134, fill=fs.PLATE, stroke=fs.RULE, sw=1, rx=4)
    svg.text(bx, by, "What the check reads", size=14, fill=FAINT, weight=600)
    svg.text(bx, by + 28, "margin_x = cavity_x − required_x", size=14, mono=True)
    svg.text(bx, by + 52, "margin_y = cavity_y − required_y", size=14, mono=True)
    svg.text(bx, by + 76, "minimum_margin =", size=14, mono=True)
    svg.text(bx + 18, by + 98, "min(margin_x, margin_y)", size=14, mono=True)
    svg.text(bx, cy + cav_y * S - 40, "x is radial, toward the plasma", size=14, fill=fs.MUTED)
    svg.text(bx, cy + cav_y * S - 20, "face; y is transverse. Both are", size=14, fill=fs.MUTED)
    svg.text(bx, cy + cav_y * S, "normal to the conductor.", size=14, fill=fs.MUTED)
    svg.write(HERE / "page-winding-pack-fit.svg")


# ----------------------------------------------------------------------------------------------
# Figure 10: each recorded case's required envelope against its clear cavity, to one scale
# ----------------------------------------------------------------------------------------------

def fit_cases():
    rows = list(csv.DictReader((HERE / "magnet-sizing-comparison.csv").open()))
    assert [r["report_alias"] for r in rows] == ["reference", "reference-sized", "reference-accommodated"]
    wall = 0.025  # m, casing wall on each radial side (study evidence)
    S = 300       # px per metre, shared by the three drawings
    W, H = 260, 236
    for r in rows:
        cav_x = float(r["radial_exterior_m"]) - 2 * wall
        cav_y = float(r["transverse_cavity_m"])
        req_x, req_y = float(r["required_cavity_x_m"]), float(r["required_cavity_y_m"])
        mx, my = cav_x - req_x, cav_y - req_y
        fits = r["fit_status"] == "satisfied"
        assert fits == (min(mx, my) >= 0)
        alias = r["report_alias"]
        desc = (f"Clear cavity {cav_x:.3f} by {cav_y:.3f} m; required envelope {req_x:.3f} by {req_y:.3f} m; "
                f"radial margin {mx:+.3f} m, transverse margin {my:+.3f} m; the pack "
                f"{'fits' if fits else 'does not fit'}.")
        svg = Svg(W, H, f"Required envelope against clear cavity, {alias}", desc, cls="fig-case")
        svg.dims_marker(name=f"dim-{alias}")
        # centre both rectangles on the same point so the overflow shows on both sides
        ccx, ccy = 130, 132
        ex_w, ex_h = (cav_x + 2 * wall) * S, (cav_y + 2 * wall) * S
        svg.rect(ccx - ex_w / 2, ccy - ex_h / 2, ex_w, ex_h, fill=SURFACE_2, stroke=fs.EDGE, sw=1, rx=2)
        svg.rect(ccx - cav_x * S / 2, ccy - cav_y * S / 2, cav_x * S, cav_y * S, fill=fs.PLATE, stroke=fs.RULE)
        color = fs.ROLE_DATA if fits else fs.ROLE_CHECK
        svg.rect(ccx - req_x * S / 2, ccy - req_y * S / 2, req_x * S, req_y * S,
                 fill=ACCENT_SOFT if fits else "none", stroke=color, sw=1.8, dash=None if fits else "5 3",
                 extra=' fill-opacity="0.55"')
        # Words only; the card's check row carries the two margins as numbers.
        svg.text(ccx, ccy + 7, "required", size=20, fill=color, anchor="middle", weight=600)
        svg.text(10, 24, "clear cavity", size=20, fill=fs.MUTED)
        svg.text(W - 10, 24, "fits" if fits else "does not fit", size=20, fill=color, anchor="end", weight=700)
        svg.write(HERE / f"page-fit-case-{alias}.svg")


# ----------------------------------------------------------------------------------------------
# Figure 7: the breeding response table and its interpolation (matplotlib, fixed layout)
# ----------------------------------------------------------------------------------------------

def breeding_chart():
    fs.use_matplotlib()
    import matplotlib.pyplot as plt

    src = ROOT / "exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py"
    text = src.read_text()
    table = eval(re.search(r"^TABLE = (\{.*?\})\n", text, re.S | re.M).group(1))  # a literal dict in the source
    nodes = table["nodes"]
    xs = [n["thickness_m"] for n in nodes]
    ys = [n["tbr_li6"] + n["tbr_li7"] for n in nodes]
    xlim, ylim = (0.5, 1.1), (1.05, 1.29)
    fw, fh = fs.WIDE_IN, 4.2
    rect = (0.08, 0.16, 0.90, 0.71)
    plt.rcParams.update({"xtick.labelsize": fs.TEXT_PT, "ytick.labelsize": fs.TEXT_PT})
    fig = plt.figure(figsize=(fw, fh))
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.axvspan(xs[0], xs[-1], color="#eef3f8", zorder=0)
    ax.grid(True, color="#e4e0da", lw=0.7); ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.plot(xs, ys, color=fs.ROLE_CALC, lw=2, zorder=2, solid_capstyle="round")
    ax.scatter(xs, ys, s=64, color=fs.ROLE_CALC, edgecolor="white", linewidth=1.5, zorder=3)
    ax.annotate(f"{ys[0]:.3f}", (xs[0], ys[0]), xytext=(-8, 8), textcoords="offset points", ha="right",
                fontsize=fs.TEXT_PT, color=fs.INK)
    ax.annotate(f"{ys[-1]:.3f}", (xs[-1], ys[-1]), xytext=(8, -12), textcoords="offset points", ha="left",
                fontsize=fs.TEXT_PT, color=fs.INK)
    ax.text((xs[0] + xs[-1]) / 2, ylim[1] - 0.012, "defined: five stored results, 0.60 to 1.00 m",
            ha="center", va="top", fontsize=fs.TEXT_PT, color=fs.MUTED)
    for x, ha in ((xlim[0] + 0.01, "left"), (xlim[1] - 0.01, "right")):
        ax.text(x, ylim[1] - 0.012, "undefined", ha=ha, va="top", fontsize=fs.TEXT_PT, color=fs.MUTED)
    ax.set_xlabel("Blanket thickness (m)")
    ax.set_ylabel("Tritium breeding ratio (Li-6 + Li-7)")
    ax.set_title("Stored transport results and the interpolated response", loc="left", pad=10)
    out = HERE / "page-breeding-response.svg"
    fig.savefig(out, format="svg")
    plt.close(fig)
    # Record the data-to-SVG transform so the page can place the live marker. The SVG is in points, origin top-left.
    W, H = fw * 72, fh * 72
    px0, px1 = rect[0] * W, (rect[0] + rect[2]) * W
    py0, py1 = H - rect[1] * H, H - (rect[1] + rect[3]) * H   # y for ylim[0], ylim[1]
    attrs = (f'data-x0="{xlim[0]}" data-x1="{xlim[1]}" data-px0="{px0:.3f}" data-px1="{px1:.3f}" '
             f'data-y0="{ylim[0]}" data-y1="{ylim[1]}" data-py0="{py0:.3f}" data-py1="{py1:.3f}"')
    _finish_mpl_svg(out, 'role="img" aria-label="Five stored breeding results between 0.60 and 1.00 m blanket '
                         'thickness, joined by straight segments; outside that range the response is undefined." '
                    + attrs, prefix="br")
    (HERE / "page-breeding-nodes.json").write_text(json.dumps({
        "nodes": [{"thickness_m": n["thickness_m"], "tbr_li6": n["tbr_li6"], "tbr_li7": n["tbr_li7"],
                   "std_error": n["std_error"]} for n in nodes],
        "interpolation_allowance": table["interpolation_allowance"],
        "statistical_multiplier": table["statistical_multiplier"],
        "source": str(src.relative_to(ROOT)),
    }, indent=1))


def _finish_mpl_svg(path: Path, root_attrs: str, prefix: str):
    """Strip the XML prolog so the SVG can be inlined, add attributes to the root element, and prefix
    matplotlib's generic ids (figure_1, marker and clip-path hashes) so two charts can share one page.
    Ids the page addresses by name (map-a-000 and so on) are left alone."""
    svg = path.read_text()
    svg = svg[svg.index("<svg"):]
    svg = re.sub(r"<metadata>.*?</metadata>\n?", "", svg, flags=re.S)
    svg = svg.replace("<svg ", f"<svg {root_attrs} ", 1)
    svg = re.sub(r'id="(?!maps?-)([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', svg)
    svg = re.sub(r"url\(#(?!maps?-)([^)]+)\)", lambda m: f"url(#{prefix}-{m.group(1)})", svg)
    svg = re.sub(r'xlink:href="#(?!maps?-)([^"]+)"', lambda m: f'xlink:href="#{prefix}-{m.group(1)}"', svg)
    path.write_text(svg)


# ----------------------------------------------------------------------------------------------
# Figure 11: the 17 September radius-current map, one group per case so the page can read each mark
# ----------------------------------------------------------------------------------------------

CHECK_NAMES = {
    "peak_field_ok": "field limit",
    "divertor_heat_ok": "divertor heat-load limit",
    "sustainment_ok": "installed-heating limit",
    "burn_hold_ok": "burn hold",
}


def feasibility_map():
    """Two renderings of the same 256 cases: side by side for the wide column, stacked for narrow screens."""
    fs.use_matplotlib()
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    from matplotlib.lines import Line2D

    rows = list(csv.DictReader((HERE / "feasibility-cost-map.csv").open()))
    assert len(rows) == 256
    cls = [r["classification"] for r in rows]
    assert (cls.count("pass"), cls.count("fail"), cls.count("invalid-account")) == (44, 210, 2)
    plt.rcParams.update({"xtick.labelsize": fs.TEXT_PT, "ytick.labelsize": fs.TEXT_PT, "legend.fontsize": fs.TEXT_PT})
    # One hue, light to dark, for conditional cost.
    cmap = LinearSegmentedColormap.from_list("cost", ["#b9d4ec", "#6b9fd0", "#2f6fae", "#0f3e6e"])
    norm = Normalize(vmin=149, vmax=160)
    handles = [Line2D([], [], marker="o", color="none", markerfacecolor=fs.ROLE_DATA, markeredgecolor="white",
                      markersize=7, label="44 pass all screens"),
               Line2D([], [], marker="x", color="#a39d94", linestyle="none", markersize=6, markeredgewidth=1.2,
                      label="210 fail at least one screen"),
               Line2D([], [], marker="D", color=fs.INK, markerfacecolor="none", linestyle="none", markersize=6,
                      label="2 invalid power accounts")]

    def panels(ax1, ax2):
        for ax in (ax1, ax2):
            ax.set_facecolor("white")
            ax.grid(True, color="#e4e0da", lw=0.7); ax.set_axisbelow(True)
            ax.spines[["top", "right"]].set_visible(False)
            ax.set_xlim(10.43, 12.23); ax.set_ylim(11.945, 13.25)
        ax1.set_title("Feasibility under the 20 modeled screens", loc="left", pad=10)
        ax2.set_title("Cost of electricity at the same points", loc="left", pad=10)

    def marks(ax1, ax2, prefix):
        # Every mark, the hollow diamonds included, gets a face color so that matplotlib writes it as a <use>
        # element with x and y attributes; the page reads those to place its hit targets and rings.
        for i, r in enumerate(rows):
            x, y, c = float(r["R_m"]), float(r["current_MAturn"]), r["classification"]
            lcoe = float(r["LCOE_dollars_MWh"])
            if c == "pass":
                a = ax1.scatter([x], [y], s=46, c=fs.ROLE_DATA, edgecolors="white", linewidths=0.9, zorder=3)
                b = ax2.scatter([x], [y], s=50, c=[cmap(norm(lcoe))], edgecolors=fs.INK, linewidths=0.7, zorder=3)
            elif c == "fail":
                a = ax1.scatter([x], [y], s=34, c="#a39d94", marker="x", linewidths=1.2, zorder=2)
                b = ax2.scatter([x], [y], s=36, c=[cmap(norm(lcoe))], marker="x", linewidths=1.5, zorder=2)
            else:
                a = ax1.scatter([x], [y], s=70, c="white", edgecolors=fs.INK, marker="D", linewidths=1.4, zorder=4)
                b = ax2.scatter([x], [y], s=70, c="white", edgecolors=fs.INK, marker="D", linewidths=1.4, zorder=4)
            a.set_gid(f"{prefix}-a-{i:03d}"); b.set_gid(f"{prefix}-b-{i:03d}")

    def edge_labels(fig, ax, items, prefix):
        """Plain text naming where each limit bites, set above the feasibility panel so that no label covers a
        mark. Along the top row (13.2 MA-turn) the three classes the page's toggle colors read left to right:
        field-limit failures, the passing band, then divertor or installed-heating failures. Each label sits in
        its own tier over that stretch of the top edge, with a bracket down to the edge and a leader up to the
        text. Nothing is shaded, because no region was interpolated. Returns the height used above the axes,
        in points, so the panel title can clear it."""
        from matplotlib import transforms
        blended = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        ax_h = fig.get_figheight() * 72 * ax.get_position().height
        up = lambda pt: 1.0 + pt / ax_h          # points above the top edge, in axes fraction
        style = dict(color=fs.INK, lw=0.9, transform=blended, clip_on=False, solid_capstyle="butt")
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        top = 0.0
        for k, (text, x0, x1, label_x, ha, rise) in enumerate(items):
            xc = (x0 + x1) / 2
            a, b = x0 - 0.045, x1 + 0.045
            ax.plot([a, a, b, b], [up(1.5), up(5), up(5), up(1.5)], **style)[0].set_gid(f"maplabel-{prefix}-bracket-{k}")
            ax.plot([xc, xc], [up(5), up(rise - 2)], **style)[0].set_gid(f"maplabel-{prefix}-leader-{k}")
            t = ax.text(label_x, up(rise), text, transform=blended, ha=ha, va="bottom", fontsize=fs.TEXT_PT,
                        color=fs.INK, linespacing=1.15, clip_on=False)
            t.set_gid(f"maplabel-{prefix}-{k}")
            ext = t.get_window_extent(renderer)
            top = max(top, rise + ext.height * 72 / fig.dpi)
            span = ax.transData.inverted().transform([[ext.x0, 0], [ext.x1, 0]])[:, 0]
            assert span[0] <= xc <= span[1], (text, span, xc)   # the leader lands under its own label
        return top

    def colorbar(cax, orientation):
        sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
        cb = plt.colorbar(sm, cax=cax, orientation=orientation)
        cb.set_label("Conditional LCOE ($/MWh)", labelpad=8); cb.outline.set_visible(False)
        cb.solids.set_rasterized(False)  # keep the ramp as vector rectangles, not an embedded bitmap
        return cb

    label = ('role="img" aria-label="Stellarator radius–ampere-turn map showing 44 passing samples, '
             '210 failing samples, two invalid power accounts, and the conditional electricity cost at valid points."')

    # Wide: the two panels side by side, at the width of the page's wide column.
    H = 83.5 + 275.6 + 118            # bottom margin, axes height and the room above them, in points
    fig = plt.figure(figsize=(fs.WIDE_IN, H / 72))
    b, h = 83.5 / H, 275.6 / H
    ax1 = fig.add_axes([0.065, b, 0.385, h])
    ax2 = fig.add_axes([0.505, b, 0.385, h])
    cax = fig.add_axes([0.905, b, 0.012, h])
    panels(ax1, ax2)
    for ax in (ax1, ax2): ax.set_xlabel("Major radius (m)", labelpad=8)
    ax1.set_ylabel("Coil ampere-turns (MA-turn)", labelpad=8)
    ax2.tick_params(labelleft=False)
    marks(ax1, ax2, "map")
    used = edge_labels(fig, ax1, [
        ("Smaller radius: field limit fails", 10.62, 11.68, 11.15, "center", 12),
        ("Passing band", 11.80, 11.92, 11.80, "center", 33),
        ("Larger radius: divertor heat or\ninstalled-heating limits fail", 12.03, 12.15, 12.22, "right", 54),
    ], "w")
    for ax in (ax1, ax2):
        ax.set_title(ax.get_title(loc="left"), loc="left", pad=used + 14)
    colorbar(cax, "vertical")
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.055, 0.01), ncol=3, columnspacing=1.6,
               handletextpad=0.4)
    out = HERE / "page-feasibility-cost.svg"
    fig.savefig(out, format="svg"); plt.close(fig)
    _strip_marker_colors(out)
    _finish_mpl_svg(out, label + ' data-marks="map"', prefix="fc")

    # Stacked: one panel above the other, drawn at a phone's width so its text keeps its size there.
    H = 712.8 + 104                   # the earlier layout plus room for the labels above the top panel, in points
    fig = plt.figure(figsize=(3.5, H / 72))
    ax1 = fig.add_axes([0.19, 438.4 / H, 0.78, 235.2 / H])
    ax2 = fig.add_axes([0.19, 174.6 / H, 0.78, 235.2 / H])
    cax = fig.add_axes([0.19, 117.6 / H, 0.78, 8.6 / H])
    panels(ax1, ax2)
    ax1.set_title("Feasibility, 20 modeled screens", loc="left", pad=8)
    ax2.set_title("Cost of electricity, same points", loc="left", pad=8)
    ax1.tick_params(labelbottom=False)
    ax2.set_xlabel("Major radius (m)", labelpad=6)
    for ax in (ax1, ax2): ax.set_ylabel("Coil ampere-turns (MA-turn)", labelpad=6)
    marks(ax1, ax2, "maps")
    used = edge_labels(fig, ax1, [
        ("Smaller radius:\nfield limit fails", 10.62, 11.68, 11.15, "center", 12),
        ("Passing band", 11.80, 11.92, 11.74, "center", 50),
        ("Larger radius: divertor heat\nor installed-heating\nlimits fail", 12.03, 12.15, 12.22, "right", 71),
    ], "s")
    ax1.set_title("Feasibility, 20 modeled screens", loc="left", pad=used + 16)
    cb = colorbar(cax, "horizontal")
    cb.set_label("Conditional LCOE ($/MWh)", labelpad=4)
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.12, 67.7 / H), ncol=1, handletextpad=0.4,
               labelspacing=0.25)
    out = HERE / "page-feasibility-cost-stacked.svg"
    fig.savefig(out, format="svg"); plt.close(fig)
    _strip_marker_colors(out)
    _finish_mpl_svg(out, label + ' data-marks="maps"', prefix="fcs")

    # The page's readout data. Failed checks are the study's predicate ids, in the CSV's order.
    data = []
    for i, r in enumerate(rows):
        data.append({
            "i": i, "R": round(float(r["R_m"]), 4), "I": round(float(r["current_MAturn"]), 4),
            "c": {"pass": "pass", "fail": "fail", "invalid-account": "invalid"}[r["classification"]],
            "lcoe": round(float(r["LCOE_dollars_MWh"]), 2),
            "v": [v for v in r["violated"].split(";") if v],
            "fm": round(float(r["field_margin_T"]), 3),
            "dm": round(float(r["divertor_margin_MW_m2"]), 3),
            "hm": round(float(r["auxiliary_window_margin_MW"]), 2),
            "net": round(float(r["net_electric_MW"]), 1),
            "id": r["candidate_id"],
        })
    (HERE / "page-map-data.json").write_text(json.dumps({
        "study": "20260917-pre-reveal-feasible-neighborhood", "checks": CHECK_NAMES, "cases": data}, separators=(",", ":")))


def _strip_marker_colors(path: Path):
    """Marker definitions are shared between marks of one color; each <use> repeats fill and stroke in its own
    style. Drop the colors from the shared definitions so a mark's <use> style is what colors it, which lets
    the page recolor one mark without touching the others."""
    svg = path.read_text()
    svg = re.sub(r'(<path id="m[0-9a-f]+" d="[^"]*" style=")([^"]*)(")',
                 lambda m: m.group(1) + re.sub(r"(fill|stroke): #[0-9a-f]{6};?\s*", "", m.group(2)).strip("; ") + m.group(3),
                 svg)
    path.write_text(svg)


# ----------------------------------------------------------------------------------------------
# Inline the rendered files into the page
# ----------------------------------------------------------------------------------------------

def inline_into_page():
    if not PAGE.exists():
        print(f"(no page at {PAGE}; nothing inlined)")
        return
    html = PAGE.read_text()
    names = set(re.findall(r"<!-- inline:([\w.\-]+) -->", html))
    for name in sorted(names):
        body = (HERE / name).read_text().strip()
        pattern = re.compile(rf"(<!-- inline:{re.escape(name)} -->)(.*?)(<!-- /inline:{re.escape(name)} -->)", re.S)
        html, n = pattern.subn(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", html)
        assert n == 1, name
        print(f"inlined {name} ({len(body)} bytes)")
    PAGE.write_text(html)


if __name__ == "__main__":
    calculation_graph()
    fit_schematic()
    fit_cases()
    breeding_chart()
    feasibility_map()
    inline_into_page()
