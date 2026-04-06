/**
 * cas_breakdown.js — CAS cost breakdown chart component.
 *
 * Renders a stacked horizontal bar chart with one segment per CAS account (CAS10–CAS90).
 * CAS22 expands inline to sub-account detail on click, collapses on second click.
 * Overridden segments carry both a hatched fill and an asterisk annotation so
 * reviewers can always distinguish real vs. overridden costs.
 *
 * Depends on: Plotly.js at /static/vendor/plotly-basic.min.js (loaded globally as window.Plotly)
 */

"use strict";

// Top-level CAS account keys in ascending display order.
// Mirrors models.py CAS_NAMES ordering — never reorder.
const CAS_ORDER = [
  "cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
  "cas26", "cas27", "cas28", "cas29", "cas30",
  "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
];

// CAS22 sub-account keys in ascending display order
const CAS22_ORDER = [
  "C220101", "C220102", "C220103", "C220104", "C220105", "C220106",
  "C220107", "C220108", "C220200", "C220300", "C220400", "C220500",
  "C220600", "C220700",
];

// Distinct color per CAS account slot — chosen to be readable on dark background
const CAS_COLORS = {
  cas10: "#6B7280",  // gray — preconstruction
  cas21: "#3B82F6",  // blue — buildings
  cas22: "#10B981",  // green — reactor plant (expandable)
  cas23: "#F59E0B",  // amber — turbine
  cas24: "#8B5CF6",  // purple — electrical
  cas25: "#EC4899",  // pink — misc
  cas26: "#06B6D4",  // cyan — heat rejection
  cas27: "#F97316",  // orange — special materials
  cas28: "#84CC16",  // lime — digital twin
  cas29: "#EF4444",  // red — contingency
  cas30: "#64748B",  // slate — indirect
  cas40: "#78716C",  // stone — owner
  cas50: "#A78BFA",  // violet — supplementary
  cas60: "#FB7185",  // rose — IDC
  cas70: "#34D399",  // emerald — O&M
  cas80: "#FCD34D",  // yellow — fuel
  cas90: "#94A3B8",  // cool gray — financial
};

// CAS22 sub-account colors — green shades to signal they belong under CAS22
const CAS22_COLORS = [
  "#059669", "#047857", "#065F46", "#064E3B",
  "#10B981", "#34D399", "#6EE7B7", "#A7F3D0",
  "#52A8A8", "#3D8B8B", "#2E7070", "#1F5555",
  "#0F3D3D", "#062A2A",
];

// Human-readable names — mirrors models.py CAS_NAMES / CAS22_NAMES exactly
const CAS_NAMES = {
  cas10: "Preconstruction",
  cas21: "Buildings & Structures",
  cas22: "Reactor Plant Equipment",
  cas23: "Turbine Plant Equipment",
  cas24: "Electrical Plant Equipment",
  cas25: "Miscellaneous Plant Equipment",
  cas26: "Heat Rejection Systems",
  cas27: "Special Materials",
  cas28: "Digital Twin & Simulation",
  cas29: "Contingency",
  cas30: "Indirect Costs",
  cas40: "Owner's Costs",
  cas50: "Supplementary Costs",
  cas60: "Interest During Construction",
  cas70: "O&M Costs (annualised)",
  cas80: "Fuel Costs (annualised)",
  cas90: "Financial Costs",
};

const CAS22_NAMES = {
  C220101: "First Wall & Blanket",
  C220102: "Radiation Shield",
  C220103: "Magnets / Coils",
  C220104: "Heating & Driver Systems",
  C220105: "Primary Structure & Support",
  C220106: "Vacuum System",
  C220107: "Power Conditioning & Energy Storage",
  C220108: "Divertor / Target Factory",
  C220109: "Direct Energy Converter",
  C220110: "Remote Handling & Maintenance Equipment",
  C220111: "Installation Labor",
  C220112: "Isotope Separation Plant",
  C220200: "Main & Secondary Coolant",
  C220300: "Auxiliary Cooling & Cryoplant",
  C220400: "Radioactive Waste Management",
  C220500: "Fuel Handling & Storage",
  C220600: "Other Reactor Plant Equipment",
  C220700: "Instrumentation & Control",
};

/**
 * Render a CAS cost breakdown as a stacked horizontal bar chart.
 *
 * @param {HTMLElement} container - Target DOM element (cleared and replaced on each render)
 * @param {Object} options
 * @param {Object} options.cas
 *   Top-level CAS account data: Record<string, {name: string, cost_m_usd: number, overridden: boolean}>
 *   Zero-cost accounts are skipped automatically.
 * @param {Object} [options.cas22_detail={}]
 *   CAS22 sub-account data: Record<string, {name: string, cost_m_usd: number, overridden: boolean}>
 *   If all values are zero or the object is empty, CAS22 click does nothing (no drill-down).
 * @param {boolean} [options.showSubAccounts=false]
 *   Initial expand state for CAS22 sub-accounts.
 * @param {number} [options.sharedScale=null]
 *   When set, pin x-axis max to this value so multiple charts share the same scale.
 *   Use max total capital cost across the comparison set.
 * @param {Function} [options.onAccountClick=null]
 *   Fired when the user clicks a non-CAS22 segment (or CAS22 when detail is empty):
 *   onAccountClick(casCode: string, accountData: CASAccount)
 *   CAS22 expand/collapse is handled internally and does NOT fire this callback.
 */
function renderCASBreakdown(container, options) {
  const {
    cas,
    cas22_detail = {},
    showSubAccounts: initialShowSubs = false,
    sharedScale = null,
    onAccountClick = null,
  } = options;

  // Mutable expand flag closed over by both render() and the click handler.
  // Why: re-render on click without external state management or full page reload.
  let showSubAccounts = initialShowSubs;

  function render() {
    const { traces, total, annotations } = _buildCASTraces(
      cas, cas22_detail, showSubAccounts
    );

    // Build xaxis — only include range when sharedScale is explicitly provided
    const xaxis = {
      title: {
        text: "Cost (M$)",
        font: { color: "#8b949e", size: 11 },
        standoff: 6,
      },
      tickfont: { color: "#6e7681", size: 11 },
      gridcolor: "#21262d",
      zeroline: false,
    };
    if (sharedScale != null) {
      // 5% padding so the rightmost bar doesn't touch the axis edge
      xaxis.range = [0, sharedScale * 1.05];
    }

    const layout = {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      margin: { l: 10, r: 60, t: 36, b: 36 },
      height: 120,
      barmode: "stack",
      xaxis,
      yaxis: {
        visible: false,
        range: [-0.5, 0.5],
      },
      annotations: [
        // Total cost label positioned just above the right edge of the bar
        {
          x: total,
          y: 0.52,
          xanchor: "left",
          yanchor: "bottom",
          text: `<b>${total.toFixed(0)} M$</b>`,
          font: { color: "#e6edf3", size: 11 },
          showarrow: false,
          xref: "x",
          yref: "y",
        },
        ...annotations,
      ],
      legend: {
        font: { color: "#8b949e", size: 10 },
        bgcolor: "transparent",
        bordercolor: "#30363d",
        borderwidth: 1,
        orientation: "h",
        x: 0,
        y: -0.38,
        xanchor: "left",
        yanchor: "top",
        traceorder: "normal",
      },
      hoverlabel: {
        bgcolor: "#21262d",
        bordercolor: "#30363d",
        font: { color: "#e6edf3", size: 12 },
        align: "left",
      },
    };

    const config = {
      displayModeBar: false,
      responsive: true,
    };

    Plotly.newPlot(container, traces, layout, config);

    // Wire click handler after each newPlot call
    container.on("plotly_click", (eventData) => {
      if (!eventData || !eventData.points || eventData.points.length === 0) return;
      const point = eventData.points[0];
      const cd = point.customdata;
      if (!cd) return;

      const { casCode, accountData } = cd;

      // CAS22: toggle sub-account view when detail has non-zero entries
      if (casCode === "cas22") {
        const hasSubs = Object.values(cas22_detail).some((a) => a.cost_m_usd > 0);
        if (hasSubs) {
          showSubAccounts = !showSubAccounts;
          render();
          // Return without firing onAccountClick — expand/collapse is internal
          return;
        }
        // Fall through when detail is empty: no drill-down, fire external callback
      }

      if (onAccountClick) {
        onAccountClick(casCode, accountData);
      }
    });
  }

  render();
}

/**
 * Build the Plotly traces and override annotations for the CAS stacked bar.
 *
 * When showSubAccounts is true, the CAS22 aggregate segment is replaced inline
 * by its sub-account traces. The total annotation always reflects top-level totals.
 *
 * @param {Object} cas - Top-level account data
 * @param {Object} cas22_detail - CAS22 sub-account data
 * @param {boolean} showSubAccounts - Whether to expand CAS22
 * @returns {{ traces: Array, total: number, annotations: Array }}
 */
function _buildCASTraces(cas, cas22_detail, showSubAccounts) {
  const traces = [];
  const annotations = [];

  // Total across all top-level accounts (used for % and the total annotation).
  // Computed upfront so percentages are consistent whether CAS22 is expanded or not.
  const total = CAS_ORDER.reduce((sum, key) => {
    const a = cas[key];
    return sum + (a ? a.cost_m_usd || 0 : 0);
  }, 0);

  // x-offset tracks the right edge of the last rendered segment.
  // Why: asterisk override annotations must be placed at the center of their segment,
  // which Plotly doesn't expose directly for stacked bar charts — we track it manually.
  let xOffset = 0;

  for (const casKey of CAS_ORDER) {
    const account = cas[casKey];
    if (!account || account.cost_m_usd <= 0) continue;

    if (casKey === "cas22" && showSubAccounts) {
      // Swap CAS22 aggregate for sub-account breakdown
      const { subTraces, subAnnotations, subWidth } = _buildCAS22SubTraces(
        cas22_detail, total, xOffset
      );
      traces.push(...subTraces);
      annotations.push(...subAnnotations);
      xOffset += subWidth;
    } else {
      const color = CAS_COLORS[casKey] || "#6B7280";
      const name = CAS_NAMES[casKey] || casKey;
      const pct = total > 0 ? ((account.cost_m_usd / total) * 100).toFixed(1) : "0.0";

      // Show expand indicator on CAS22 label when sub-accounts exist
      const hasSubs = casKey === "cas22" && Object.values(cas22_detail).some((a) => a.cost_m_usd > 0);
      const legendLabel = hasSubs ? `${name} ▾` : name;

      const overrideText = account.overridden ? " ★ overridden" : "";
      const hovertext =
        `<b>${name}${account.overridden ? " ★" : ""}</b><br>` +
        `Cost: ${account.cost_m_usd.toFixed(1)} M$<br>` +
        `Share: ${pct}%${overrideText}`;

      // Asterisk annotation centered on this segment — visible even when bar is narrow
      if (account.overridden) {
        annotations.push({
          x: xOffset + account.cost_m_usd / 2,
          y: 0.55,
          text: "★",
          font: { color: "#FCD34D", size: 9 },
          showarrow: false,
          xref: "x",
          yref: "y",
        });
      }

      traces.push({
        type: "bar",
        orientation: "h",
        x: [account.cost_m_usd],
        y: [""],
        name: legendLabel,
        marker: _buildSegmentMarker(color, account.overridden),
        hovertemplate: `${hovertext}<extra></extra>`,
        // customdata carries identity so the click handler can route correctly
        customdata: [{ casCode: casKey, accountData: account }],
        legendgroup: casKey,
        showlegend: true,
      });

      xOffset += account.cost_m_usd;
    }
  }

  return { traces, total, annotations };
}

/**
 * Build bar traces for CAS22 sub-accounts (expanded state).
 *
 * @param {Object} cas22_detail - Sub-account data keyed by C220XXX
 * @param {number} totalCost - Top-level total (for percentage calculations)
 * @param {number} startOffset - x position where CAS22 sub-accounts begin
 * @returns {{ subTraces: Array, subAnnotations: Array, subWidth: number }}
 */
function _buildCAS22SubTraces(cas22_detail, totalCost, startOffset) {
  const subTraces = [];
  const subAnnotations = [];
  let xOffset = startOffset;

  const activeSubs = CAS22_ORDER.filter(
    (key) => cas22_detail[key] && cas22_detail[key].cost_m_usd > 0
  );

  activeSubs.forEach((key, idx) => {
    const account = cas22_detail[key];
    const color = CAS22_COLORS[idx % CAS22_COLORS.length];
    const name = CAS22_NAMES[key] || key;
    const pct = totalCost > 0 ? ((account.cost_m_usd / totalCost) * 100).toFixed(1) : "0.0";

    const overrideText = account.overridden ? " ★ overridden" : "";
    const hovertext =
      `<b>${name}${account.overridden ? " ★" : ""}</b> <span style="color:#6e7681">(CAS22)</span><br>` +
      `Cost: ${account.cost_m_usd.toFixed(1)} M$<br>` +
      `Share of total: ${pct}%${overrideText}`;

    if (account.overridden) {
      subAnnotations.push({
        x: xOffset + account.cost_m_usd / 2,
        y: 0.55,
        text: "★",
        font: { color: "#FCD34D", size: 9 },
        showarrow: false,
        xref: "x",
        yref: "y",
      });
    }

    subTraces.push({
      type: "bar",
      orientation: "h",
      x: [account.cost_m_usd],
      y: [""],
      name,
      marker: _buildSegmentMarker(color, account.overridden),
      hovertemplate: `${hovertext}<extra></extra>`,
      customdata: [{ casCode: key, accountData: account }],
      legendgroup: key,
      showlegend: true,
    });

    xOffset += account.cost_m_usd;
  });

  return { subTraces, subAnnotations, subWidth: xOffset - startOffset };
}

/**
 * Build a Plotly marker config for a CAS segment.
 * Overridden segments get a diagonal hatch on top of the base color.
 * Why: reviewers must be able to distinguish real vs. overridden costs at a glance.
 *
 * @param {string} color - Hex color for this segment
 * @param {boolean} overridden - Whether the account value was manually overridden
 * @returns {Object} Plotly marker configuration
 */
function _buildSegmentMarker(color, overridden) {
  const base = {
    color,
    line: { color: _hexToRgba(color, 0.7), width: 1 },
  };
  if (overridden) {
    return {
      ...base,
      opacity: 0.85,
      pattern: {
        shape: "\\",
        bgcolor: color,
        fgcolor: _hexToRgba("#FCD34D", 0.45),
        size: 6,
        solidity: 0.25,
      },
    };
  }
  return base;
}

/**
 * Convert a 6-digit hex color + alpha to "rgba(r, g, b, a)" string.
 * Why: mirrors tornado.js — Plotly marker.color accepts rgba() for per-segment opacity.
 *
 * @param {string} hex - e.g. "#3B82F6"
 * @param {number} alpha - 0–1
 * @returns {string}
 */
function _hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha.toFixed(2)})`;
}
