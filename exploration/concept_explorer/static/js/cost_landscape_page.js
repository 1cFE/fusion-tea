/**
 * cost_landscape_page.js — the Cost landscape page (Theme F).
 *
 * Reuses B1's data core wholesale: the page fetches four endpoints ONCE
 * (manifest + registry + tree for the rows/grouping spine, plus
 * /api/cost-landscape for the LCOE decomposition), left-joins the cost record
 * onto each row by `concept_id`, and keeps only costed concepts. Every re-group
 * is then a pure `matrixData.project()` over the same rows[] — no refetch ever
 * (NFR-1 / I3). Grouping, family color, and identity all come from existing
 * authorities; this module owns only fetch-join-render-and-the-group-control.
 *
 * The render is a Plotly stacked bar per concept: height = headline LCOE,
 * segments = the annualised components that sum to it (Capital / Fixed O&M /
 * Replacement / Fuel, or a single combined-O&M segment when a concept's model
 * never split it). Segment $/MWh is decomposed in JS (D2); colors come from the
 * --cost-* :root tokens (D3, no hex here, I2); the y-axis is a focused linear
 * range with over-cap bars drawn to the cap and their true LCOE annotated (D5).
 */

"use strict";

(function () {
  // ---- View state (the single mutable model; every interaction re-projects) --
  var rows = []; // costed rows (joined + cost attached + _seg decomposed), once
  var tree = null; // /api/taxonomy/tree, for groupBy="tree"
  var totalServed = 0; // manifest concept count, for the honest excluded note
  var viewState = null;
  var clickWired = false; // plotly_click handler attached once (survives re-react)

  // The cost landscape offers a curated subset of the matrix's group options
  // (FR-F6): no-grouping + family tree + four ontology facets. Sort is fixed
  // LCOE-ascending within band (FR-F7), so there is no sort control.
  var WANTED_DIMENSIONS = ["fuel", "driver", "capture", "opMode"];

  // Focused linear y-range cap (D5, user-confirmed). Bars taller than this draw
  // to the cap and carry an "↑ <true LCOE>" annotation; the full bar is still
  // reachable by Plotly zoom. Linear (not log) so the segments stay additive.
  var CAP_LCOE = 400;

  // The stacked segments, bottom→top (Plotly stacks in trace order). capital and
  // fuel are always drawn; the O&M split (fixed_om/replacement) and the combined
  // O&M (om_combined) are mutually exclusive per concept and each only appears as
  // a trace when some concept needs it. Colors trace to :root (D3 / I2).
  var COMPONENTS = [
    { key: "capital", label: "Capital", token: "--cost-capital", always: true },
    { key: "fixed_om", label: "Fixed O&M", token: "--cost-fixed-om", always: false },
    { key: "replacement", label: "Replacement", token: "--cost-replacement", always: false },
    { key: "om_combined", label: "O&M (combined)", token: "--cost-om-combined", always: false },
    { key: "fuel", label: "Fuel", token: "--cost-fuel", always: true },
  ];

  var rootStyle = getComputedStyle(document.documentElement);

  /** Read a :root custom property; warn loudly if missing (no silent ""). */
  function tok(name) {
    var v = rootStyle.getPropertyValue(name).trim();
    if (!v) console.error("[cost-landscape] missing CSS token: " + name);
    return v;
  }

  var PLOTLY_CONFIG = { displayModeBar: false, responsive: true };

  /** Create a DOM element with optional attributes and text (mirrors matrix_page.js). */
  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") node.className = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    if (text != null) node.textContent = text;
    return node;
  }

  /** Resolve a fetch Response to JSON, throwing loudly on a non-2xx status. */
  function okJson(resp) {
    if (!resp.ok) throw new Error("HTTP " + resp.status + " for " + resp.url);
    return resp.json();
  }

  /** The curated group-by options, reusing matrixData's labels for the facets. */
  function groupOptions() {
    var dims = matrixData.GROUP_OPTIONS.filter(function (o) {
      return WANTED_DIMENSIONS.indexOf(o.value) !== -1;
    });
    return [
      { value: "none", label: "No grouping" },
      { value: "tree", label: "Family (tree)" },
    ].concat(dims);
  }

  /**
   * Within-band order: LCOE ascending, concept code as the stable tiebreak
   * (FR-F7). matrixData.makeComparator can't sort by LCOE (it only knows code,
   * name, and ontology facets), so the cost page owns this one comparator.
   */
  function byLcoeAsc(a, b) {
    var la = a.cost.lcoe,
      lb = b.cost.lcoe;
    if (la !== lb) return la - lb;
    return String(a.concept_id) < String(b.concept_id) ? -1 : 1;
  }

  /** The band's accent color: family color for tree bands, value color for dims. */
  function railColor(band) {
    if (band.kind === "tree" && band.family) return ontologyPalette.family[band.family];
    if (band.kind === "dim" && band.color) return band.color;
    return null;
  }

  /** Tree band labels are full paths ("MFE › Stellarator › Modular"); the chart
   *  shows just the leaf so the per-band annotation stays readable. */
  function bandShortLabel(label) {
    var parts = String(label).split("›");
    return parts[parts.length - 1].trim();
  }

  /** Format an LCOE for the over-cap annotation (thousands grouped). */
  function fmtLcoe(v) {
    return v >= 1000 ? Math.round(v).toLocaleString("en-US") : v.toFixed(0);
  }

  /** Translucent rgba() from a palette/token hex (the hex is token-sourced, not
   *  authored here — keeps the A2/I2 single-color-authority intact). */
  function hexToRgba(hex, alpha) {
    var h = String(hex).replace(/^#/, "");
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return "rgba(" + ((n >> 16) & 255) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + alpha + ")";
  }

  /**
   * Decompose a concept's annualised costs into per-segment $/MWh (D2):
   *   segment $/MWh = component_M$ / (capital + om_combined + fuel) × LCOE.
   * When the O&M split is recorded, fixed_om/replacement carry it and the
   * combined bucket is 0; otherwise the combined bucket carries all O&M and the
   * split is 0 (honest degradation — a single O&M segment, never a fake split).
   * The five segment values sum to the headline LCOE (I1).
   */
  function decompose(cost) {
    var c = cost.components;
    var annualised = c.capital + c.om_combined + c.fuel; // cas90 + cas70 + cas80
    var factor = annualised > 0 ? cost.lcoe / annualised : 0;
    var split = c.fixed_om != null && c.replacement != null;
    return {
      capital: c.capital * factor,
      fixed_om: split ? c.fixed_om * factor : 0,
      replacement: split ? c.replacement * factor : 0,
      om_combined: split ? 0 : c.om_combined * factor,
      fuel: c.fuel * factor,
      split: split,
    };
  }

  /** Flatten projected bands into an ordered row list + band spans (for x layout). */
  function flattenBands(bands) {
    var ordered = [];
    var spans = [];
    bands.forEach(function (band) {
      var start = ordered.length;
      band.rows.forEach(function (r) {
        ordered.push(r);
      });
      spans.push({
        label: band.label,
        start: start,
        end: ordered.length - 1,
        color: railColor(band),
      });
    });
    return { ordered: ordered, spans: spans };
  }

  /** One stacked-bar trace per included component (Phase 5 enriches the hover). */
  function buildTraces(ordered) {
    var anySplit = ordered.some(function (r) {
      return r._seg.split;
    });
    var anyCombined = ordered.some(function (r) {
      return !r._seg.split;
    });

    return COMPONENTS.filter(function (comp) {
      if (comp.always) return true;
      if (comp.key === "om_combined") return anyCombined;
      return anySplit; // fixed_om / replacement
    }).map(function (comp) {
      return {
        type: "bar",
        name: comp.label,
        x: ordered.map(function (_, i) {
          return i;
        }),
        y: ordered.map(function (r) {
          return r._seg[comp.key];
        }),
        customdata: ordered.map(function (r) {
          return r.concept_id;
        }),
        marker: { color: tok(comp.token) },
        hovertemplate: "%{hovertext}<extra></extra>",
        hovertext: ordered.map(function (r) {
          return hoverFor(r, comp);
        }),
      };
    });
  }

  /** Truncate a citation/rationale for the hover (full text on the concept page). */
  function truncate(s, n) {
    s = String(s);
    return s.length > n ? s.slice(0, n).trim() + "…" : s;
  }

  /**
   * Which override-component families a rendered segment covers. The combined-O&M
   * segment (drawn when a concept's model never split O&M) carries both the
   * fixed-O&M and replacement override families — analysts author O&M overrides
   * at the combined CAS70 level, which rolls up to `fixed_om`, so without this
   * the combined segment's hover would miss them.
   */
  function coveredComponents(segKey) {
    return segKey === "om_combined" ? ["fixed_om", "replacement"] : [segKey];
  }

  /**
   * Per-segment override summary for the hover (FR-F8 / D6): a "★N adjustments"
   * header plus up to two notes (account + first-sentence rationale, or the
   * source, or an explicit "not recorded"), with a deep-link cue when there are
   * more. The full multi-paragraph rationale lives on the concept page (D6).
   * Returns null when the segment carries no overrides (library default).
   */
  function overrideSummary(cost, segKey) {
    var covered = coveredComponents(segKey);
    var segOv = (cost.overrides || []).filter(function (o) {
      return covered.indexOf(o.component) !== -1;
    });
    if (!segOv.length) return null;

    var enabled = segOv.filter(function (o) {
      return o.enabled;
    });
    var blocked = segOv.filter(function (o) {
      return !o.enabled;
    });

    var lines = [];
    if (enabled.length) {
      var header = "★ " + enabled.length + " adjustment" + (enabled.length === 1 ? "" : "s");
      if (blocked.length) header += " · " + blocked.length + " blocked";
      lines.push(header);
    } else {
      // Only blocked entries: recorded but not applied (the segment is library
      // default) — say so honestly rather than "0 adjustments".
      lines.push(blocked.length + " blocked adjustment" + (blocked.length === 1 ? "" : "s") + " (not applied)");
    }

    enabled.slice(0, 2).forEach(function (o) {
      var note = o.rationale_short || o.source;
      lines.push("· " + o.account + ": " + (note ? truncate(note, 70) : "not recorded"));
    });
    if (enabled.length > 2) {
      lines.push("· …" + (enabled.length - 2) + " more — click for detail");
    }
    return lines.join("<br>");
  }

  /**
   * Per-segment hover: identity + component $/MWh + % of LCOE, the override
   * summary for that segment, and the concept's grounding caveat reason (the
   * same caveat the tick glyph marks). Click navigates to the concept page (D6).
   */
  function hoverFor(row, comp) {
    var seg = row._seg[comp.key];
    var pct = row.cost.lcoe > 0 ? (seg / row.cost.lcoe) * 100 : 0;
    var lines = [
      conceptLabel(row).text,
      comp.label + ": " + seg.toFixed(1) + " $/MWh (" + pct.toFixed(1) + "%)",
    ];
    var ov = overrideSummary(row.cost, comp.key);
    if (ov) lines.push(ov);
    var cav = caveatMarker({ asterisk: row.asterisk_in_comparison, fitGrade: row.fit_grade });
    if (cav.any) lines.push(cav.glyph + " " + cav.title);
    lines.push("<i>click bar → concept page</i>");
    return lines.join("<br>");
  }

  /**
   * Group decorations: a translucent colored background zone per band (so it's
   * obvious which bars belong to which group), a boundary separator, and a
   * staggered band label. The zone color is the band's family/value color; the
   * label rows alternate height to reduce horizontal collisions when bands are
   * narrow (the dense family-tree case). Plus over-cap "↑ true LCOE" markers.
   */
  function buildDecorations(ordered, spans, grouped) {
    var shapes = [];
    var annotations = [];

    if (grouped) {
      spans.forEach(function (span, i) {
        var x0 = span.start - 0.5;
        var x1 = span.end + 0.5;
        var color = span.color;

        // Background zone — the primary "which bars are in this group" cue.
        shapes.push({
          type: "rect",
          xref: "x",
          yref: "paper",
          x0: x0,
          x1: x1,
          y0: 0,
          y1: 1,
          fillcolor: hexToRgba(color || tok("--color-text-muted"), color ? 0.13 : 0.05),
          line: { width: 0 },
          layer: "below",
        });
        // Boundary separator (distinguishes adjacent same-color zones, e.g.
        // sibling tree leaves under one family).
        if (i > 0) {
          shapes.push({
            type: "line",
            xref: "x",
            yref: "paper",
            x0: x0,
            x1: x0,
            y0: 0,
            y1: 1.07,
            line: { color: tok("--color-border"), width: 1 },
          });
        }
        // Label, staggered into two rows so neighbors don't overlap.
        annotations.push({
          xref: "x",
          yref: "paper",
          x: (span.start + span.end) / 2,
          y: i % 2 === 0 ? 1.065 : 1.02,
          yanchor: "bottom",
          xanchor: "center",
          showarrow: false,
          text: truncate(bandShortLabel(span.label), 16),
          font: { color: color || tok("--color-text-secondary"), size: 10 },
        });
      });
    }

    ordered.forEach(function (r, i) {
      if (r.cost.lcoe > CAP_LCOE) {
        annotations.push({
          xref: "x",
          yref: "paper",
          x: i,
          y: 0.98,
          yanchor: "top",
          showarrow: false,
          text: "↑ " + fmtLcoe(r.cost.lcoe),
          font: { color: tok("--color-text-primary"), size: 9 },
          textangle: -90,
        });
      }
    });

    return { shapes: shapes, annotations: annotations };
  }

  /** Render the projected, LCOE-sorted bands as the Plotly stacked-bar chart. */
  function renderChart(bands) {
    var mount = document.getElementById("cost-chart");
    var flat = flattenBands(bands);
    var ordered = flat.ordered;
    if (!ordered.length) {
      Plotly.purge(mount);
      mount.textContent = "No costed concepts to display.";
      return;
    }

    var grouped = viewState.groupBy !== "none";
    var traces = buildTraces(ordered);
    var deco = buildDecorations(ordered, flat.spans, grouped);
    var n = ordered.length;

    var layout = {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      font: { color: tok("--color-text-secondary") },
      hoverlabel: {
        bgcolor: tok("--color-surface-2"),
        bordercolor: tok("--color-border"),
        font: { color: tok("--color-text-primary"), size: 12 },
      },
      barmode: "stack",
      bargap: 0.25,
      height: 560,
      margin: { l: 60, r: 20, t: 64, b: 96 },
      xaxis: {
        tickmode: "array",
        tickvals: ordered.map(function (_, i) {
          return i;
        }),
        ticktext: ordered.map(function (r) {
          // Append the A3 caveat glyph to the #code tick for low-grounding /
          // archetype-fit-None concepts (FR-F5/F10); the reason is in the hover.
          // (Plotly tick labels are plain text, so the glyph rides the string.)
          var cav = caveatMarker({ asterisk: r.asterisk_in_comparison, fitGrade: r.fit_grade });
          return conceptLabel(r).codeText + (cav.any ? " " + cav.glyph : "");
        }),
        tickfont: { color: tok("--color-text-muted"), size: 10 },
        tickangle: -60,
        range: [-0.5, n - 0.5],
        zeroline: false,
        showgrid: false,
      },
      yaxis: {
        title: {
          text: "LCOE contribution ($/MWh)",
          font: { color: tok("--color-text-secondary"), size: 11 },
          standoff: 8,
        },
        range: [0, CAP_LCOE],
        gridcolor: tok("--color-border-subtle"),
        tickfont: { color: tok("--color-text-muted"), size: 11 },
        zeroline: false,
      },
      legend: {
        orientation: "h",
        x: 0,
        y: -0.22,
        xanchor: "left",
        yanchor: "top",
        font: { color: tok("--color-text-secondary"), size: 11 },
        bgcolor: "transparent",
      },
      shapes: deco.shapes,
      annotations: deco.annotations,
      showlegend: true,
    };

    Plotly.react(mount, traces, layout, PLOTLY_CONFIG);

    // Bar click → concept page (FR-F9 / D6). Attached once; the handler reads
    // the clicked point's customdata (concept_id), so it stays correct across
    // re-groups (Plotly.react reuses the same graph div).
    if (!clickWired) {
      mount.on("plotly_click", function (ev) {
        var pt = ev && ev.points && ev.points[0];
        if (pt && pt.customdata != null) {
          window.location.href = "/concept/" + pt.customdata;
        }
      });
      clickWired = true;
    }
  }

  // ---- Controls bar: the group-by select (mirrors matrix_page buildControls) --
  function buildControls() {
    var bar = document.getElementById("cost-controls");
    bar.innerHTML = "";

    var gb = el("label", { class: "matrix-control" });
    gb.appendChild(el("span", { class: "matrix-control__label" }, "Group by"));
    var sel = el("select", { class: "matrix-control__select", id: "cost-groupby" });
    groupOptions().forEach(function (opt) {
      sel.appendChild(el("option", { value: opt.value }, opt.label));
    });
    sel.value = viewState.groupBy;
    sel.addEventListener("change", function () {
      viewState.groupBy = sel.value;
      applyView();
    });
    gb.appendChild(sel);
    bar.appendChild(gb);

    bar.appendChild(el("span", { class: "matrix-controls__summary", id: "cost-summary" }));
  }

  /** Controls-bar summary line. */
  function updateSummary(bands) {
    var visible = bands.reduce(function (n, b) {
      return n + b.rows.length;
    }, 0);
    var opt = groupOptions().find(function (o) {
      return o.value === viewState.groupBy;
    });
    var label = opt ? opt.label : viewState.groupBy;
    var s = document.getElementById("cost-summary");
    if (s) {
      s.textContent =
        visible + " costed concepts · grouped by " + label + " · " + bands.length + " groups";
    }
  }

  /**
   * Honest accounting (I5/FR-F10): concepts not on the chart (served set minus
   * costed rows — none today, all 36 served are costed), plus a note for bars
   * that exceed the axis cap (drawn to the cap with their true LCOE annotated).
   * Both are functions of the fixed row set, so this runs once at load.
   */
  function updateNotes() {
    var note = document.getElementById("cost-excluded");
    var msgs = [];

    var excluded = totalServed - rows.length;
    if (excluded > 0) {
      msgs.push(
        excluded +
          " of " +
          totalServed +
          " concepts not shown (no cost model or non-finite LCOE)."
      );
    }

    var capped = rows.filter(function (r) {
      return r.cost.lcoe > CAP_LCOE;
    }).length;
    if (capped > 0) {
      msgs.push(
        capped +
          " concept" +
          (capped === 1 ? "" : "s") +
          " exceed the " +
          CAP_LCOE +
          " $/MWh axis cap — true LCOE annotated; zoom for the full bar."
      );
    }

    if (msgs.length) {
      note.textContent = msgs.join(" ");
      note.style.display = "";
    } else {
      note.style.display = "none";
    }
  }

  /** The single re-render entry point: project the current viewState, then paint. */
  function applyView() {
    var bands = matrixData.project(rows, viewState, tree);
    // "No grouping" yields a single ungrouped band — give it an honest label.
    if (viewState.groupBy === "none" && bands.length) {
      bands[0].label = "All costed concepts";
    }
    bands.forEach(function (b) {
      b.rows.sort(byLcoeAsc);
    });
    renderChart(bands);
    updateSummary(bands);
  }

  async function init() {
    var loadingEl = document.getElementById("loading-state");
    var contentEl = document.getElementById("cost-landscape-content");
    var errorEl = document.getElementById("error-state");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    var manifest, registry, landscape;
    try {
      var payloads = await Promise.all([
        fetch("/api/manifest").then(okJson),
        fetch("/api/taxonomy/registry").then(okJson),
        fetch("/api/taxonomy/tree").then(okJson),
        fetch("/api/cost-landscape").then(okJson),
      ]);
      manifest = payloads[0];
      registry = payloads[1];
      tree = payloads[2];
      landscape = payloads[3];
    } catch (err) {
      console.error("[cost-landscape] Failed to load data:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    var joined = matrixData.joinConcepts(manifest, registry);
    totalServed = joined.length;

    var costById = {};
    (landscape.concepts || []).forEach(function (c) {
      costById[c.concept_id] = c;
    });
    rows = joined.filter(function (r) {
      return costById[r.concept_id];
    });
    rows.forEach(function (r) {
      r.cost = costById[r.concept_id];
      r._seg = decompose(r.cost);
    });

    // Fixed sort key: matrixData.project sorts within band, but we re-sort by
    // LCOE in applyView, so the project sort key is irrelevant. Filter is off
    // for v1 (the cost page exposes grouping, not the filter panel).
    viewState = { groupBy: "tree", sortKey: "code", sortDir: "asc", filter: null };

    buildControls();
    updateNotes();
    applyView();

    loadingEl.style.display = "none";
    contentEl.style.display = "";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
