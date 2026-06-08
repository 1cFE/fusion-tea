/**
 * view_sensitivity.js — Sensitivity comparison view.
 *
 * Compares parameter elasticities across selected concepts via tornado charts.
 *   - Integrated mode: grouped tornado chart with union of top-N parameters,
 *     shared parameters sorted to top with a dotted divider
 *   - Landscape mode: per-concept top-N tornado with confidence encoding
 *     (opacity + hatch for low-confidence), synced symmetric x-axis
 *
 * Depends on globals from tornado.js:
 *   TORNADO_CATEGORY_COLORS, TORNADO_CATEGORY_LABELS, TORNADO_CATEGORY_ORDER,
 *   TORNADO_CONFIDENCE_OPACITY, _hexToRgba
 *
 * Data source: concept.data.cost_model.sensitivities (engineering + financial)
 *              concept.data.parameter_metadata
 * Registers on window.VIEW_REGISTRY.sensitivity.
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // DOM helpers (same pattern as view_summary.js)
  // ---------------------------------------------------------------------------

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const TOP_N = 8;

  // Family colors from the one authority (ontology_palette.js → CSS :root).
  const FAMILY_COLORS = ontologyPalette.family;

  const PLOTLY_THEME = {
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: { color: "#8b949e" },
    gridcolor: "#21262d",
    tickfont: { color: "#6e7681", size: 11 },
    hoverlabel: {
      bgcolor: "#21262d",
      bordercolor: "#30363d",
      font: { color: "#e6edf3", size: 12 },
    },
  };

  const PLOTLY_CONFIG = { displayModeBar: false, responsive: true };

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function assignColors(concepts) {
    const familyCount = {};
    return concepts.map((c) => {
      const fam = c.confinement_family;
      const base = FAMILY_COLORS[fam] || FAMILY_COLORS.NONSTANDARD;
      const idx = familyCount[fam] || 0;
      familyCount[fam] = idx + 1;
      const opacity = [1.0, 0.7, 0.5, 0.4, 0.35, 0.3][idx] || 0.3;
      return { base, opacity };
    });
  }

  function rgba(hex, opacity) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${opacity})`;
  }

  function purgeCharts(container) {
    const charts = container.querySelectorAll(".js-plotly-plot");
    for (const chart of charts) {
      Plotly.purge(chart);
    }
  }

  // ---------------------------------------------------------------------------
  // Core data processing
  // ---------------------------------------------------------------------------

  /**
   * Merge engineering + financial sensitivities, sort by |elasticity|, take top-N.
   * Returns [{paramName, elasticity, baseline, group}, ...] sorted desc by |elasticity|.
   */
  function mergeAndRank(sensitivities, topN) {
    if (!sensitivities) return [];
    const merged = {};
    for (const [key, entry] of Object.entries(sensitivities.engineering || {})) {
      merged[key] = { ...entry, group: "engineering" };
    }
    for (const [key, entry] of Object.entries(sensitivities.financial || {})) {
      merged[key] = { ...entry, group: "financial" };
    }
    return Object.entries(merged)
      .map(([paramName, entry]) => ({ paramName, ...entry }))
      .sort((a, b) => Math.abs(b.elasticity) - Math.abs(a.elasticity))
      .slice(0, topN);
  }

  /**
   * Build the union of top-N parameters across all concepts.
   * Returns { params: string[], sharedSet: Set<string> } with shared-first sorting.
   */
  function buildUnionParams(concepts) {
    const allParams = new Map(); // paramName → { appearances, maxAbsElasticity }

    for (const c of concepts) {
      if (!c.data.cost_model?.sensitivities) continue;
      const ranked = mergeAndRank(c.data.cost_model.sensitivities, TOP_N);
      for (const entry of ranked) {
        const existing = allParams.get(entry.paramName) || {
          appearances: 0,
          maxAbsElasticity: 0,
        };
        existing.appearances++;
        existing.maxAbsElasticity = Math.max(
          existing.maxAbsElasticity,
          Math.abs(entry.elasticity)
        );
        allParams.set(entry.paramName, existing);
      }
    }

    const unionParams = [...allParams.keys()];

    // Sort: shared params first (by appearance desc), then unique (by max |elasticity| desc)
    unionParams.sort((a, b) => {
      const aInfo = allParams.get(a);
      const bInfo = allParams.get(b);
      const aShared = aInfo.appearances > 1 ? 1 : 0;
      const bShared = bInfo.appearances > 1 ? 1 : 0;
      if (aShared !== bShared) return bShared - aShared;
      return bInfo.maxAbsElasticity - aInfo.maxAbsElasticity;
    });

    const sharedSet = new Set(
      unionParams.filter((p) => allParams.get(p).appearances > 1)
    );

    return { params: unionParams, sharedSet };
  }

  /**
   * Compute the maximum absolute elasticity across all concepts.
   * Used for Landscape mode symmetric axis sync.
   */
  function computeSharedElasticityRange(concepts) {
    let maxAbs = 0;
    for (const c of concepts) {
      const sens = c.data.cost_model?.sensitivities;
      if (!sens) continue;
      for (const group of [sens.engineering, sens.financial]) {
        if (!group) continue;
        for (const entry of Object.values(group)) {
          const abs = Math.abs(entry.elasticity);
          if (abs > maxAbs) maxAbs = abs;
        }
      }
    }
    return maxAbs > 0 ? maxAbs * 1.1 : 1;
  }

  /**
   * Resolve display name from parameter_metadata sources.
   * Tries each source in order, falls back to raw param name.
   */
  function displayName(paramName, ...metadataSources) {
    for (const meta of metadataSources) {
      if (meta && meta[paramName]?.display_name) {
        return meta[paramName].display_name;
      }
    }
    return paramName;
  }

  /**
   * Build a combined metadata map from all concepts' parameter_metadata.
   */
  function buildCombinedMetadata(concepts) {
    const combined = {};
    for (const c of concepts) {
      const meta = c.data.parameter_metadata;
      if (!meta) continue;
      for (const [key, val] of Object.entries(meta)) {
        if (!combined[key]) combined[key] = val;
      }
    }
    return combined;
  }

  // ---------------------------------------------------------------------------
  // Integrated mode — grouped tornado
  // ---------------------------------------------------------------------------

  function renderIntegrated(container, concepts) {
    purgeCharts(container);
    container.innerHTML = "";

    const conceptsWithData = concepts.filter(
      (c) => c.data.cost_model?.sensitivities
    );
    if (conceptsWithData.length === 0) {
      container.appendChild(
        el(
          "div",
          "view-no-data",
          "No sensitivity data available for selected concepts"
        )
      );
      return;
    }

    const { params: unionParams, sharedSet } = buildUnionParams(concepts);
    if (unionParams.length === 0) {
      container.appendChild(
        el("div", "view-no-data", "No sensitivity parameters found")
      );
      return;
    }

    const combinedMeta = buildCombinedMetadata(concepts);
    const colors = assignColors(concepts);

    // Plotly renders bottom-to-top; reverse so first param appears at top
    const yOrder = unionParams.map((p) => displayName(p, combinedMeta));
    const categoryArray = [...yOrder].reverse();

    const traces = [];

    for (let ci = 0; ci < concepts.length; ci++) {
      const concept = concepts[ci];
      const sens = concept.data.cost_model?.sensitivities;
      if (!sens) continue;

      const color = colors[ci];
      const allSens = {
        ...(sens.engineering || {}),
        ...(sens.financial || {}),
      };

      const yLabels = unionParams.map((p) => displayName(p, combinedMeta));
      const xValues = unionParams.map((p) =>
        allSens[p] ? allSens[p].elasticity : 0
      );
      const hoverTexts = unionParams.map((p) => {
        const entry = allSens[p];
        if (!entry) return `${displayName(p, combinedMeta)}<br>${concept.name}: N/A`;
        const conf = combinedMeta[p]?.confidence || "unknown";
        return (
          `<b>${displayName(p, combinedMeta)}</b><br>` +
          `${concept.name}<br>` +
          `Elasticity: ${entry.elasticity.toFixed(3)}<br>` +
          `Baseline: ${entry.baseline}<br>` +
          `Confidence: ${conf}`
        );
      });

      traces.push({
        type: "bar",
        orientation: "h",
        y: yLabels,
        x: xValues,
        name: concept.name,
        marker: { color: rgba(color.base, color.opacity) },
        hovertemplate: "%{hovertext}<extra></extra>",
        hovertext: hoverTexts,
        legendgroup: concept.concept_id,
        showlegend: true,
      });
    }

    const chartHeight = Math.max(300, unionParams.length * 28 + 120);

    // Build shapes for divider between shared and unique sections
    const shapes = [];
    if (sharedSet.size > 0 && sharedSet.size < unionParams.length) {
      // Divider between last shared and first unique param
      // In the reversed category array, shared params are at the end (top of chart)
      // The divider goes at y-position = (total - sharedSet.size) - 0.5 in category index space
      const dividerIdx = unionParams.length - sharedSet.size - 0.5;
      shapes.push({
        type: "line",
        x0: 0,
        x1: 1,
        xref: "paper",
        y0: dividerIdx,
        y1: dividerIdx,
        yref: "y",
        line: { color: "#30363d", width: 1, dash: "dot" },
      });
    }

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    const layout = {
      paper_bgcolor: PLOTLY_THEME.paper_bgcolor,
      plot_bgcolor: PLOTLY_THEME.plot_bgcolor,
      font: PLOTLY_THEME.font,
      hoverlabel: PLOTLY_THEME.hoverlabel,
      margin: { l: 10, r: 30, t: 10, b: 30 },
      height: chartHeight,
      barmode: "group",
      xaxis: {
        title: {
          text: "Elasticity (\u0394LCOE% / \u0394param%)",
          font: { color: "#8b949e", size: 11 },
          standoff: 6,
        },
        zeroline: true,
        zerolinecolor: "#30363d",
        zerolinewidth: 2,
        gridcolor: PLOTLY_THEME.gridcolor,
        tickfont: PLOTLY_THEME.tickfont,
        tickformat: ".2f",
      },
      yaxis: {
        automargin: true,
        tickfont: { color: "#8b949e", size: 11 },
        categoryorder: "array",
        categoryarray: categoryArray,
      },
      legend: {
        font: { color: "#8b949e", size: 11 },
        bgcolor: "transparent",
        bordercolor: "#30363d",
        borderwidth: 1,
        orientation: "h",
        x: 0,
        y: -0.06,
        xanchor: "left",
        yanchor: "top",
      },
      shapes: shapes,
      showlegend: true,
    };

    Plotly.newPlot(chartDiv, traces, layout, PLOTLY_CONFIG);
  }

  // ---------------------------------------------------------------------------
  // Landscape mode — per-concept tornado with confidence encoding
  // ---------------------------------------------------------------------------

  function renderLandscape(container, concept, syncContext) {
    purgeCharts(container);
    container.innerHTML = "";

    const sens = concept.data.cost_model?.sensitivities;
    if (!sens) {
      container.appendChild(
        el("div", "view-no-data", "No sensitivity data available")
      );
      return;
    }

    const ranked = mergeAndRank(sens, TOP_N);
    if (ranked.length === 0) {
      container.appendChild(
        el("div", "view-no-data", "No sensitivity parameters found")
      );
      return;
    }

    const allConcepts =
      syncContext && syncContext.allConcepts ? syncContext.allConcepts : [concept];
    const sharedMax = computeSharedElasticityRange(allConcepts);
    const meta = concept.data.parameter_metadata || {};

    // Sort by |elasticity| descending — already sorted by mergeAndRank
    // Plotly bottom-to-top, so reverse for top-down
    const yLabels = ranked.map((e) => displayName(e.paramName, meta));
    const categoryArray = [...yLabels].reverse();

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    // Build traces with confidence encoding
    // Separate solid (high/medium) from hatched (low)
    const solid = ranked.filter(
      (e) => !meta[e.paramName] || meta[e.paramName].confidence !== "low"
    );
    const hatched = ranked.filter(
      (e) => meta[e.paramName] && meta[e.paramName].confidence === "low"
    );

    const traces = [];

    if (solid.length > 0) {
      const x = solid.map((e) => e.elasticity);
      const y = solid.map((e) => displayName(e.paramName, meta));
      const markerColors = solid.map((e) => {
        const pm = meta[e.paramName];
        const category = pm ? pm.category : "shared-baseline";
        const color =
          TORNADO_CATEGORY_COLORS[category] || TORNADO_CATEGORY_COLORS["shared-baseline"];
        const confidence = pm?.confidence || "high";
        const opacity = TORNADO_CONFIDENCE_OPACITY[confidence] ?? 1.0;
        return _hexToRgba(color, opacity);
      });
      const hoverTexts = solid.map((e) => {
        const pm = meta[e.paramName];
        const catLabel =
          TORNADO_CATEGORY_LABELS[pm?.category] || pm?.category || "Unknown";
        return (
          `<b>${displayName(e.paramName, meta)}</b><br>` +
          `Elasticity: ${e.elasticity.toFixed(3)}<br>` +
          `Baseline: ${e.baseline}<br>` +
          `Category: ${catLabel}<br>` +
          `Confidence: ${pm?.confidence || "unknown"}`
        );
      });

      traces.push({
        type: "bar",
        orientation: "h",
        x: x,
        y: y,
        marker: {
          color: markerColors,
          line: { color: "rgba(139,148,158,0.3)", width: 1 },
        },
        hovertemplate: "%{hovertext}<extra></extra>",
        hovertext: hoverTexts,
        showlegend: false,
      });
    }

    if (hatched.length > 0) {
      const x = hatched.map((e) => e.elasticity);
      const y = hatched.map((e) => displayName(e.paramName, meta));
      const barColors = hatched.map((e) => {
        const pm = meta[e.paramName];
        const category = pm ? pm.category : "shared-baseline";
        const color =
          TORNADO_CATEGORY_COLORS[category] || TORNADO_CATEGORY_COLORS["shared-baseline"];
        return _hexToRgba(color, TORNADO_CONFIDENCE_OPACITY.low);
      });
      const fgColors = hatched.map((e) => {
        const pm = meta[e.paramName];
        const category = pm ? pm.category : "shared-baseline";
        const color =
          TORNADO_CATEGORY_COLORS[category] || TORNADO_CATEGORY_COLORS["shared-baseline"];
        return _hexToRgba(color, 0.9);
      });
      const hoverTexts = hatched.map((e) => {
        const pm = meta[e.paramName];
        const catLabel =
          TORNADO_CATEGORY_LABELS[pm?.category] || pm?.category || "Unknown";
        return (
          `<b>${displayName(e.paramName, meta)}</b> (?)<br>` +
          `Elasticity: ${e.elasticity.toFixed(3)}<br>` +
          `Baseline: ${e.baseline}<br>` +
          `Category: ${catLabel}<br>` +
          `Confidence: low`
        );
      });

      traces.push({
        type: "bar",
        orientation: "h",
        x: x,
        y: y,
        marker: {
          color: barColors,
          pattern: {
            shape: "/",
            bgcolor: "transparent",
            fgcolor: fgColors,
            size: 6,
            solidity: 0.3,
          },
          line: { color: "rgba(139,148,158,0.3)", width: 1 },
        },
        hovertemplate: "%{hovertext}<extra></extra>",
        hovertext: hoverTexts,
        showlegend: false,
      });
    }

    const chartHeight = Math.max(250, ranked.length * 28 + 80);

    const layout = {
      paper_bgcolor: PLOTLY_THEME.paper_bgcolor,
      plot_bgcolor: PLOTLY_THEME.plot_bgcolor,
      font: PLOTLY_THEME.font,
      hoverlabel: PLOTLY_THEME.hoverlabel,
      margin: { l: 10, r: 20, t: 5, b: 25 },
      height: chartHeight,
      barmode: "overlay",
      xaxis: {
        range: [-sharedMax, sharedMax],
        title: {
          text: "Elasticity",
          font: { color: "#8b949e", size: 10 },
          standoff: 4,
        },
        zeroline: true,
        zerolinecolor: "#30363d",
        zerolinewidth: 2,
        gridcolor: PLOTLY_THEME.gridcolor,
        tickfont: { color: "#6e7681", size: 10 },
        tickformat: ".2f",
      },
      yaxis: {
        automargin: true,
        tickfont: { color: "#8b949e", size: 10 },
        categoryorder: "array",
        categoryarray: categoryArray,
      },
    };

    Plotly.newPlot(chartDiv, traces, layout, PLOTLY_CONFIG);
  }

  // ---------------------------------------------------------------------------
  // Register on VIEW_REGISTRY
  // ---------------------------------------------------------------------------

  window.VIEW_REGISTRY.sensitivity.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.sensitivity.renderLandscape = renderLandscape;
})();
