/**
 * view_capex.js — CapEx comparison view.
 *
 * Compares CAS cost structure across selected concepts.
 *   - Integrated mode: grouped horizontal bar chart, all concepts on shared axes
 *   - Landscape mode: per-concept horizontal bar chart with CAS-colored bars, synced x-axis
 *   - CAS22 expand/collapse: dedicated toggle button replaces CAS22 aggregate with 14 sub-accounts
 *
 * Depends on globals from cas_breakdown.js:
 *   CAS_ORDER, CAS22_ORDER, CAS_COLORS, CAS22_COLORS, CAS_NAMES, CAS22_NAMES, _hexToRgba
 *
 * Data source: concept.data.cost_model.cas{10..90} and concept.data.cost_model.cas22_detail
 * Registers on window.VIEW_REGISTRY.capex.
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

  function append(parent, ...children) {
    for (const c of children) {
      if (c != null) parent.appendChild(c);
    }
    return parent;
  }

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const FAMILY_COLORS = {
    MFE: "#3b82f6",
    IFE: "#a855f7",
    MIF: "#f59e0b",
    NONSTANDARD: "#6b7280",
  };

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
  // Module state
  // ---------------------------------------------------------------------------

  let showSubAccounts = false;

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

  /**
   * Build the y-axis category order for CAS accounts.
   * Returns array in display order (CAS10 first, CAS90 last).
   * When showSubAccounts is true, CAS22 is replaced by its 14 sub-accounts.
   */
  function buildCategoryOrder() {
    const categories = [];
    for (const casKey of CAS_ORDER) {
      if (casKey === "cas22" && showSubAccounts) {
        for (const subKey of CAS22_ORDER) {
          categories.push(CAS22_NAMES[subKey] || subKey);
        }
      } else {
        categories.push(CAS_NAMES[casKey] || casKey);
      }
    }
    return categories;
  }

  /**
   * Compute total capital cost for a concept's cost model.
   */
  function totalCost(costModel) {
    let sum = 0;
    for (const key of CAS_ORDER) {
      const acct = costModel[key];
      if (acct) sum += acct.cost_m_usd || 0;
    }
    return sum;
  }

  /**
   * Compute the maximum single-account cost across all concepts.
   * Used for Landscape mode axis sync. Includes CAS22 sub-accounts when expanded.
   */
  function computeSharedMaxAccount(concepts) {
    let max = 0;
    for (const c of concepts) {
      if (!c.data.cost_model) continue;
      const cm = c.data.cost_model;
      for (const key of CAS_ORDER) {
        if (key === "cas22" && showSubAccounts) {
          if (cm.cas22_detail) {
            for (const sub of Object.values(cm.cas22_detail)) {
              if (sub && sub.cost_m_usd > max) max = sub.cost_m_usd;
            }
          }
        } else {
          const acct = cm[key];
          if (acct && acct.cost_m_usd > max) max = acct.cost_m_usd;
        }
      }
    }
    return max > 0 ? max * 1.1 : 1;
  }

  /**
   * Format a number with comma thousands separator.
   */
  function fmtCost(val) {
    return val.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  // ---------------------------------------------------------------------------
  // Integrated mode — grouped horizontal bars
  // ---------------------------------------------------------------------------

  function renderIntegrated(container, concepts) {
    purgeCharts(container);
    container.innerHTML = "";

    const conceptsWithData = concepts.filter((c) => c.data.cost_model);
    if (conceptsWithData.length === 0) {
      container.appendChild(
        el("div", "view-no-data", "No cost model data available for selected concepts")
      );
      return;
    }

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    const colors = assignColors(concepts);
    const categories = buildCategoryOrder();
    // Plotly renders bottom-to-top, so reverse for top-down display
    const categoryArray = [...categories].reverse();
    const numCategories = categories.length;

    const traces = [];

    for (let ci = 0; ci < concepts.length; ci++) {
      const concept = concepts[ci];
      const cm = concept.data.cost_model;
      if (!cm) continue;

      const color = colors[ci];
      const total = totalCost(cm);
      const yLabels = [];
      const xValues = [];
      const hoverTexts = [];

      for (const casKey of CAS_ORDER) {
        if (casKey === "cas22" && showSubAccounts) {
          for (const subKey of CAS22_ORDER) {
            const sub = cm.cas22_detail ? cm.cas22_detail[subKey] : null;
            const name = CAS22_NAMES[subKey] || subKey;
            const cost = sub ? sub.cost_m_usd || 0 : 0;
            const pct = total > 0 ? ((cost / total) * 100).toFixed(1) : "0.0";
            const overrideTag = sub && sub.overridden ? " ★ overridden" : "";
            yLabels.push(name);
            xValues.push(cost);
            hoverTexts.push(
              `<b>${name}</b> (CAS22)<br>` +
              `${concept.name}<br>` +
              `Cost: ${cost.toFixed(1)} M$ (${pct}%)${overrideTag}`
            );
          }
        } else {
          const acct = cm[casKey];
          const name = CAS_NAMES[casKey] || casKey;
          const cost = acct ? acct.cost_m_usd || 0 : 0;
          const pct = total > 0 ? ((cost / total) * 100).toFixed(1) : "0.0";
          const overrideTag = acct && acct.overridden ? " ★ overridden" : "";
          yLabels.push(name);
          xValues.push(cost);
          hoverTexts.push(
            `<b>${name}</b><br>` +
            `${concept.name}<br>` +
            `Cost: ${cost.toFixed(1)} M$ (${pct}%)${overrideTag}`
          );
        }
      }

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

    const chartHeight = Math.min(900, Math.max(400, numCategories * 28 + 120));

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
          text: "Cost (M$)",
          font: { color: "#8b949e", size: 11 },
          standoff: 6,
        },
        gridcolor: PLOTLY_THEME.gridcolor,
        tickfont: PLOTLY_THEME.tickfont,
        zeroline: false,
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
      showlegend: true,
    };

    Plotly.newPlot(chartDiv, traces, layout, PLOTLY_CONFIG);

    // Total cost summary line
    const totalsDiv = el("div", "capex-totals");
    for (const concept of conceptsWithData) {
      const total = totalCost(concept.data.cost_model);
      const item = el("div", "capex-totals__item");
      append(
        item,
        el("span", null, concept.name + ":"),
        el("span", "capex-totals__value", fmtCost(total) + " M$")
      );
      totalsDiv.appendChild(item);
    }
    container.appendChild(totalsDiv);

    // CAS22 toggle button
    const toggleBtn = el(
      "button",
      "capex-toggle",
      showSubAccounts ? "▾ Collapse CAS22 Detail" : "▸ Expand CAS22 Detail"
    );
    toggleBtn.addEventListener("click", () => {
      showSubAccounts = !showSubAccounts;
      renderIntegrated(container, concepts);
    });
    container.appendChild(toggleBtn);
  }

  // ---------------------------------------------------------------------------
  // Landscape mode — per-concept CAS-colored bars
  // ---------------------------------------------------------------------------

  function renderLandscape(container, concept, syncContext) {
    purgeCharts(container);
    container.innerHTML = "";

    if (!concept.data.cost_model) {
      container.appendChild(el("div", "view-no-data", "No cost model available"));
      return;
    }

    const cm = concept.data.cost_model;
    const total = totalCost(cm);
    const allConcepts =
      syncContext && syncContext.allConcepts ? syncContext.allConcepts : [concept];
    const sharedMax = computeSharedMaxAccount(allConcepts);

    const categories = buildCategoryOrder();
    const categoryArray = [...categories].reverse();

    const chartDiv = el("div");
    chartDiv.style.width = "100%";
    container.appendChild(chartDiv);

    const yLabels = [];
    const xValues = [];
    const barColors = [];
    const hoverTexts = [];
    const annotations = [];

    for (const casKey of CAS_ORDER) {
      if (casKey === "cas22" && showSubAccounts) {
        for (let si = 0; si < CAS22_ORDER.length; si++) {
          const subKey = CAS22_ORDER[si];
          const sub = cm.cas22_detail ? cm.cas22_detail[subKey] : null;
          const name = CAS22_NAMES[subKey] || subKey;
          const cost = sub ? sub.cost_m_usd || 0 : 0;
          const pct = total > 0 ? ((cost / total) * 100).toFixed(1) : "0.0";
          const overrideTag = sub && sub.overridden ? " ★ overridden" : "";
          yLabels.push(name);
          xValues.push(cost);
          barColors.push(CAS22_COLORS[si % CAS22_COLORS.length]);
          hoverTexts.push(
            `<b>${name}</b> (CAS22)<br>` +
            `Cost: ${cost.toFixed(1)} M$ (${pct}%)${overrideTag}`
          );
          if (sub && sub.overridden) {
            annotations.push({
              x: cost,
              y: name,
              text: " ★",
              font: { color: "#FCD34D", size: 10 },
              showarrow: false,
              xanchor: "left",
              xref: "x",
              yref: "y",
            });
          }
        }
      } else {
        const acct = cm[casKey];
        const name = CAS_NAMES[casKey] || casKey;
        const cost = acct ? acct.cost_m_usd || 0 : 0;
        const pct = total > 0 ? ((cost / total) * 100).toFixed(1) : "0.0";
        const overrideTag = acct && acct.overridden ? " ★ overridden" : "";
        yLabels.push(name);
        xValues.push(cost);
        barColors.push(CAS_COLORS[casKey] || "#6B7280");
        hoverTexts.push(
          `<b>${name}</b><br>` +
          `Cost: ${cost.toFixed(1)} M$ (${pct}%)${overrideTag}`
        );
        if (acct && acct.overridden) {
          annotations.push({
            x: cost,
            y: name,
            text: " ★",
            font: { color: "#FCD34D", size: 10 },
            showarrow: false,
            xanchor: "left",
            xref: "x",
            yref: "y",
          });
        }
      }
    }

    const numCategories = categories.length;
    const chartHeight = Math.min(600, Math.max(300, numCategories * 22 + 80));

    const trace = {
      type: "bar",
      orientation: "h",
      y: yLabels,
      x: xValues,
      marker: { color: barColors },
      hovertemplate: "%{hovertext}<extra></extra>",
      hovertext: hoverTexts,
      showlegend: false,
    };

    const layout = {
      paper_bgcolor: PLOTLY_THEME.paper_bgcolor,
      plot_bgcolor: PLOTLY_THEME.plot_bgcolor,
      font: PLOTLY_THEME.font,
      hoverlabel: PLOTLY_THEME.hoverlabel,
      margin: { l: 10, r: 30, t: 5, b: 25 },
      height: chartHeight,
      xaxis: {
        range: [0, sharedMax],
        title: {
          text: "Cost (M$)",
          font: { color: "#8b949e", size: 10 },
          standoff: 4,
        },
        gridcolor: PLOTLY_THEME.gridcolor,
        tickfont: { color: "#6e7681", size: 10 },
        zeroline: false,
      },
      yaxis: {
        automargin: true,
        tickfont: { color: "#8b949e", size: 10 },
        categoryorder: "array",
        categoryarray: categoryArray,
      },
      annotations: annotations,
    };

    Plotly.newPlot(chartDiv, [trace], layout, PLOTLY_CONFIG);

    // Total cost below chart
    const totalLine = el("div", "capex-totals");
    const item = el("div", "capex-totals__item");
    append(
      item,
      el("span", null, "Total:"),
      el("span", "capex-totals__value", fmtCost(total) + " M$")
    );
    totalLine.appendChild(item);
    container.appendChild(totalLine);

    // CAS22 toggle
    const toggleBtn = el(
      "button",
      "capex-toggle",
      showSubAccounts ? "▾ Collapse CAS22 Detail" : "▸ Expand CAS22 Detail"
    );
    toggleBtn.addEventListener("click", () => {
      showSubAccounts = !showSubAccounts;
      renderLandscape(container, concept, syncContext);
    });
    container.appendChild(toggleBtn);
  }

  // ---------------------------------------------------------------------------
  // Register on VIEW_REGISTRY
  // ---------------------------------------------------------------------------

  window.VIEW_REGISTRY.capex.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.capex.renderLandscape = renderLandscape;
})();
