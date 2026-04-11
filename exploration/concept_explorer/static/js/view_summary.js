/**
 * view_summary.js — Summary comparison view.
 *
 * Compares headline economics across selected concepts.
 *   - Integrated mode: 5-metric small-multiples bar chart + metrics table
 *   - Landscape mode: per-concept horizontal bar chart + metric rows (synced axes)
 *
 * Data source: concept.data.cost_model.headline (already in conceptCache).
 * Registers on window.VIEW_REGISTRY.summary.
 */

"use strict";

(function () {
  // ---------------------------------------------------------------------------
  // DOM helpers (same pattern as comparison.js:89-101)
  // ---------------------------------------------------------------------------

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function append(parent, ...children) {
    for (const c of children) {
      if (c != null) parent.appendChild(c);
    }
    return parent;
  }

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const FAMILY_META = {
    MFE: { label: "MFE", cls: "badge badge-mfe" },
    IFE: { label: "IFE", cls: "badge badge-ife" },
    MIF: { label: "MIF", cls: "badge badge-mif" },
    NONSTANDARD: { label: "Non-std", cls: "badge badge-nonstandard" },
  };

  const FAMILY_COLORS = {
    MFE: "#3b82f6",
    IFE: "#a855f7",
    MIF: "#f59e0b",
    NONSTANDARD: "#6b7280",
  };

  const HEADLINE_METRICS = [
    { field: "lcoe_per_mwh",         label: "LCOE",           unit: "$/MWh", format: (v) => v.toFixed(1) },
    { field: "overnight_cost_per_kw", label: "Overnight Cost", unit: "$/kW",  format: (v) => v.toFixed(0) },
    { field: "p_net_mw",             label: "Net Power",      unit: "MW",    format: (v) => v.toFixed(0) },
    { field: "q_eng",                label: "Q_eng",          unit: "",      format: (v) => v.toFixed(2) },
    { field: "capacity_factor",      label: "Capacity Factor", unit: "",      format: (v) => (v * 100).toFixed(1) + "%" },
  ];

  const CAS_ACCOUNT_KEYS = [
    "cas10", "cas21", "cas22", "cas23", "cas24", "cas25", "cas26", "cas27",
    "cas28", "cas29", "cas30", "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
  ];

  /** Plotly dark theme — matches tornado.js conventions */
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

  /**
   * Get headline data for a concept, or null if no cost model.
   */
  function getHeadline(concept) {
    return concept.data.cost_model ? concept.data.cost_model.headline : null;
  }

  /**
   * Find the largest CAS account for a concept's cost model.
   * Returns { name, pct } or null.
   */
  function getTopCasDriver(costModel) {
    if (!costModel) return null;
    let maxKey = null;
    let maxCost = -1;
    let total = 0;

    for (const key of CAS_ACCOUNT_KEYS) {
      const account = costModel[key];
      if (!account) continue;
      total += account.cost_m_usd;
      if (account.cost_m_usd > maxCost) {
        maxCost = account.cost_m_usd;
        maxKey = key;
      }
    }

    if (!maxKey || total <= 0) return null;
    const account = costModel[maxKey];
    return {
      name: account.name,
      pct: ((maxCost / total) * 100).toFixed(1),
    };
  }

  /**
   * Assign a color to each concept. Uses family color with opacity stepping
   * when multiple concepts share a family.
   */
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

  /**
   * Convert hex + opacity to rgba string.
   */
  function rgba(hex, opacity) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${opacity})`;
  }

  /**
   * Compute shared axis scales across all concepts that have cost models.
   * Returns { [metricField]: { min, max } }.
   */
  function computeSharedScales(concepts) {
    const scales = {};
    for (const metric of HEADLINE_METRICS) {
      let min = Infinity;
      let max = -Infinity;
      for (const c of concepts) {
        const h = getHeadline(c);
        if (!h) continue;
        const val = h[metric.field];
        if (val != null) {
          if (val < min) min = val;
          if (val > max) max = val;
        }
      }
      if (min === Infinity) {
        min = 0;
        max = 1;
      }
      const pad = (max - min) * 0.1 || max * 0.1 || 1;
      scales[metric.field] = {
        min: Math.max(0, min - pad),
        max: max + pad,
      };
    }
    return scales;
  }

  // ---------------------------------------------------------------------------
  // Integrated mode — subplot chart + metrics table
  // ---------------------------------------------------------------------------

  /**
   * Render the 5-subplot small-multiples chart into container.
   */
  function renderIntegratedChart(container, concepts) {
    const conceptsWithData = concepts.filter((c) => getHeadline(c));
    if (conceptsWithData.length === 0) return;

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    const colors = assignColors(concepts);
    const traces = [];
    const nMetrics = HEADLINE_METRICS.length;

    // Build one trace per concept across all subplots
    for (let ci = 0; ci < concepts.length; ci++) {
      const c = concepts[ci];
      const h = getHeadline(c);
      if (!h) continue;

      const color = colors[ci];

      for (let mi = 0; mi < nMetrics; mi++) {
        const metric = HEADLINE_METRICS[mi];
        const val = h[metric.field];
        const xAxisKey = mi === 0 ? "x" : `x${mi + 1}`;
        const yAxisKey = mi === 0 ? "y" : `y${mi + 1}`;

        traces.push({
          type: "bar",
          x: [val],
          y: [c.name],
          orientation: "h",
          name: c.name,
          legendgroup: c.concept_id,
          showlegend: false,
          marker: { color: rgba(color.base, color.opacity) },
          hovertemplate: `${c.name}<br>${metric.label}: %{x}${metric.unit ? " " + metric.unit : ""}<extra></extra>`,
          xaxis: xAxisKey,
          yaxis: yAxisKey,
        });
      }
    }

    // Layout with 5 side-by-side subplots
    const gap = 0.06;
    const subWidth = (1 - gap * (nMetrics - 1)) / nMetrics;
    const layout = {
      paper_bgcolor: PLOTLY_THEME.paper_bgcolor,
      plot_bgcolor: PLOTLY_THEME.plot_bgcolor,
      font: PLOTLY_THEME.font,
      hoverlabel: PLOTLY_THEME.hoverlabel,
      margin: { l: 10, r: 20, t: 10, b: 30 },
      height: Math.max(160, conceptsWithData.length * 50 + 80),
      barmode: "group",
      showlegend: false,
    };

    for (let mi = 0; mi < nMetrics; mi++) {
      const metric = HEADLINE_METRICS[mi];
      const xStart = mi * (subWidth + gap);
      const xEnd = xStart + subWidth;
      const xKey = mi === 0 ? "xaxis" : `xaxis${mi + 1}`;
      const yKey = mi === 0 ? "yaxis" : `yaxis${mi + 1}`;

      layout[xKey] = {
        domain: [xStart, xEnd],
        title: { text: metric.unit ? `${metric.label} (${metric.unit})` : metric.label, font: { size: 10, color: "#8b949e" }, standoff: 4 },
        gridcolor: PLOTLY_THEME.gridcolor,
        tickfont: { color: "#6e7681", size: 9 },
        nticks: 4,
        zeroline: false,
      };
      layout[yKey] = {
        anchor: mi === 0 ? "x" : `x${mi + 1}`,
        automargin: true,
        tickfont: mi === 0 ? { color: "#8b949e", size: 11 } : { color: "transparent", size: 1 },
        showticklabels: mi === 0,
      };
    }

    Plotly.newPlot(chartDiv, traces, layout, PLOTLY_CONFIG);
  }

  /**
   * Render the metrics comparison table.
   */
  function renderMetricsTable(container, concepts) {
    const table = el("table", "comparison-table comparison-table--summary");

    // Header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headerRow.appendChild(el("th", null, "Metric"));

    for (const c of concepts) {
      const th = document.createElement("th");
      const familyInfo = FAMILY_META[c.confinement_family] ?? {
        label: c.confinement_family,
        cls: "badge badge-nonstandard",
      };
      append(th, el("span", null, c.name + " "), el("span", familyInfo.cls, familyInfo.label));
      headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body — one row per metric
    const tbody = document.createElement("tbody");

    for (const metric of HEADLINE_METRICS) {
      const tr = document.createElement("tr");

      // Label cell
      const labelTd = el("td", null, metric.label);
      if (metric.unit) {
        append(labelTd, el("span", "unit", metric.unit));
      }
      tr.appendChild(labelTd);

      // Value cells
      for (const c of concepts) {
        const h = getHeadline(c);
        if (!h) {
          tr.appendChild(el("td", "no-data", "\u2014"));
          continue;
        }
        const val = h[metric.field];
        tr.appendChild(el("td", null, val != null ? metric.format(val) : "\u2014"));
      }

      tbody.appendChild(tr);
    }

    // Top CAS driver row
    const casTr = document.createElement("tr");
    casTr.appendChild(el("td", null, "Top CAS Driver"));

    for (const c of concepts) {
      if (!c.data.cost_model) {
        casTr.appendChild(el("td", "no-data", "\u2014"));
        continue;
      }
      const driver = getTopCasDriver(c.data.cost_model);
      if (driver) {
        casTr.appendChild(el("td", null, `${driver.name} (${driver.pct}%)`));
      } else {
        casTr.appendChild(el("td", "no-data", "\u2014"));
      }
    }
    tbody.appendChild(casTr);

    table.appendChild(tbody);
    container.appendChild(table);
  }

  // ---------------------------------------------------------------------------
  // Landscape mode — per-concept panel
  // ---------------------------------------------------------------------------

  /**
   * Render a single-concept horizontal bar chart with synced axes.
   */
  function renderLandscapeChart(container, concept, scales) {
    const h = getHeadline(concept);
    if (!h) return;

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    const color = FAMILY_COLORS[concept.confinement_family] || FAMILY_COLORS.NONSTANDARD;

    const yLabels = HEADLINE_METRICS.map((m) => m.label).reverse();

    // Normalize values to 0-1 range using shared scales so bars are visually comparable
    const xNorm = HEADLINE_METRICS.map((m) => {
      const s = scales[m.field];
      const val = h[m.field];
      if (!s || s.max === s.min) return val ? 1 : 0;
      return (val - s.min) / (s.max - s.min);
    }).reverse();

    const hoverText = HEADLINE_METRICS.map((m) => {
      const val = h[m.field];
      return `${m.label}: ${m.format(val)}${m.unit ? " " + m.unit : ""}`;
    }).reverse();

    const trace = {
      type: "bar",
      y: yLabels,
      x: xNorm,
      orientation: "h",
      marker: { color: color },
      hovertext: hoverText,
      hoverinfo: "text",
      showlegend: false,
    };

    const layout = {
      paper_bgcolor: PLOTLY_THEME.paper_bgcolor,
      plot_bgcolor: PLOTLY_THEME.plot_bgcolor,
      font: PLOTLY_THEME.font,
      hoverlabel: PLOTLY_THEME.hoverlabel,
      margin: { l: 10, r: 10, t: 5, b: 5 },
      height: 160,
      xaxis: {
        range: [0, 1],
        showticklabels: false,
        gridcolor: PLOTLY_THEME.gridcolor,
        zeroline: false,
      },
      yaxis: {
        automargin: true,
        tickfont: { color: "#8b949e", size: 10 },
      },
      bargap: 0.3,
    };

    Plotly.newPlot(chartDiv, [trace], layout, PLOTLY_CONFIG);
  }

  /**
   * Render compact metric rows below the landscape chart.
   */
  function renderLandscapeMetrics(container, concept) {
    const h = getHeadline(concept);
    if (!h) return;

    const list = el("div");
    list.style.marginTop = "var(--space-3)";

    for (const metric of HEADLINE_METRICS) {
      const row = el("div", "summary-metric-row");
      row.appendChild(el("span", "summary-metric-row__label", metric.label));

      const valText = h[metric.field] != null ? metric.format(h[metric.field]) : "\u2014";
      const unitText = metric.unit ? ` ${metric.unit}` : "";
      row.appendChild(el("span", "summary-metric-row__value", valText + unitText));

      list.appendChild(row);
    }

    // Top CAS driver
    const driver = getTopCasDriver(concept.data.cost_model);
    if (driver) {
      const driverRow = el("div", "summary-metric-row");
      driverRow.appendChild(el("span", "summary-metric-row__label", "Top CAS"));
      driverRow.appendChild(el("span", "summary-metric-row__value", `${driver.name} (${driver.pct}%)`));
      list.appendChild(driverRow);
    }

    container.appendChild(list);
  }

  // ---------------------------------------------------------------------------
  // Helpers — Plotly cleanup
  // ---------------------------------------------------------------------------

  /**
   * Purge any Plotly charts inside a container before clearing it.
   * Prevents memory leaks from orphaned Plotly internals.
   */
  function purgeCharts(container) {
    const charts = container.querySelectorAll(".js-plotly-plot");
    for (const chart of charts) {
      Plotly.purge(chart);
    }
  }

  // ---------------------------------------------------------------------------
  // Render entry points
  // ---------------------------------------------------------------------------

  function renderIntegrated(container, concepts) {
    purgeCharts(container);
    container.innerHTML = "";

    const anyData = concepts.some((c) => getHeadline(c));
    if (!anyData) {
      container.appendChild(el("div", "view-no-data", "No cost model data available for selected concepts"));
      return;
    }

    renderIntegratedChart(container, concepts);

    const spacer = el("div");
    spacer.style.height = "var(--space-4)";
    container.appendChild(spacer);

    renderMetricsTable(container, concepts);
  }

  function renderLandscape(container, concept, syncContext) {
    purgeCharts(container);
    container.innerHTML = "";

    if (!concept.data.cost_model) {
      container.appendChild(el("div", "view-no-data", "No cost model available"));
      return;
    }

    // Compute shared scales from all concepts in the comparison
    const allConcepts = syncContext && syncContext.allConcepts ? syncContext.allConcepts : [concept];
    const scales = computeSharedScales(allConcepts);

    renderLandscapeChart(container, concept, scales);
    renderLandscapeMetrics(container, concept);
  }

  // ---------------------------------------------------------------------------
  // Register on VIEW_REGISTRY
  // ---------------------------------------------------------------------------

  window.VIEW_REGISTRY.summary.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.summary.renderLandscape = renderLandscape;
})();
