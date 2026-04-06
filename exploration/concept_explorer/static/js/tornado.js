/**
 * tornado.js — Tornado chart component for parameter sensitivity visualization.
 *
 * Renders a horizontal bar chart showing parameter elasticities with:
 * - Category color encoding (design system colors from explorer.css)
 * - Confidence opacity (1.0 / 0.8 / 0.6) + hatched fill for low-confidence bars
 * - Population whiskers: [min, max] elasticity range across concepts in the parameter index
 * - Click handler for parameter detail popover
 *
 * Depends on: Plotly.js at /static/vendor/plotly-basic.min.js (loaded globally as window.Plotly)
 */

"use strict";

// Category → hex color (matches --color-* custom properties in explorer.css)
const TORNADO_CATEGORY_COLORS = {
  "shared-baseline": "#6B7280",
  "well-established": "#3B82F6",
  "key-innovation": "#10B981",
  "concept-unique": "#F59E0B",
  "high-risk": "#EF4444",
};

const TORNADO_CATEGORY_LABELS = {
  "shared-baseline": "Shared Baseline",
  "well-established": "Well Established",
  "key-innovation": "Key Innovation",
  "concept-unique": "Concept Unique",
  "high-risk": "High Risk",
};

// Display order for categories in legend
const TORNADO_CATEGORY_ORDER = [
  "shared-baseline",
  "well-established",
  "key-innovation",
  "concept-unique",
  "high-risk",
];

const TORNADO_CONFIDENCE_OPACITY = {
  high: 1.0,
  medium: 0.8,
  low: 0.6,
};

/**
 * Render a tornado chart of sensitivity elasticities into a DOM element.
 *
 * @param {HTMLElement} container - Target DOM element (will be cleared and replaced)
 * @param {Object} options
 * @param {Object|null} options.sensitivities
 *   Sensitivity data: { engineering: Record<string, {elasticity, baseline}>,
 *                       financial:   Record<string, {elasticity, baseline}> }
 *   Pass null for standalone concepts — renders informative placeholder instead.
 * @param {Object} options.parameterMetadata
 *   Map of paramName → ParameterMetadata (display_name, category, confidence, range, ...)
 * @param {Object} [options.populationContext=null]
 *   ParameterIndex object ({ parameters: { [paramName]: { concepts: [{concept_id, name, elasticity}] } } })
 *   Used to compute [min, max] whisker ranges. Pass null to omit whiskers.
 *   NOTE: The spec interface types this as ConceptManifest, but ParameterIndex is the correct type
 *   because only ParameterIndex carries per-parameter cross-concept elasticities.
 * @param {number} [options.topN=15] - Maximum number of bars to display (sorted by |elasticity|)
 * @param {Function} [options.onParameterClick=null]
 *   Callback fired when a bar is clicked: onParameterClick(paramName, metadata)
 */
function renderTornado(container, options) {
  const {
    sensitivities,
    parameterMetadata,
    populationContext = null,
    topN = 15,
    onParameterClick = null,
  } = options;

  // Standalone concept: show placeholder instead of empty chart
  if (sensitivities === null) {
    container.innerHTML =
      '<p class="text-muted" style="padding: 24px 0; font-style: italic; font-size: 13px;">' +
      "No sensitivity data available \u2014 this concept uses a standalone cost model" +
      "</p>";
    return;
  }

  // Merge engineering + financial into one flat map
  // Warn per missing metadata key so callers notice incomplete metadata files
  const merged = {};
  for (const [key, entry] of Object.entries(sensitivities.engineering || {})) {
    merged[key] = { ...entry, group: "engineering" };
    if (!parameterMetadata[key]) {
      console.warn(`[tornado] Missing parameterMetadata for engineering key: ${key}`);
    }
  }
  for (const [key, entry] of Object.entries(sensitivities.financial || {})) {
    merged[key] = { ...entry, group: "financial" };
    if (!parameterMetadata[key]) {
      console.warn(`[tornado] Missing parameterMetadata for financial key: ${key}`);
    }
  }

  // Sort by |elasticity| descending, take top N
  const sorted = Object.entries(merged)
    .sort((a, b) => Math.abs(b[1].elasticity) - Math.abs(a[1].elasticity))
    .slice(0, topN);

  if (sorted.length === 0) {
    container.innerHTML =
      '<p class="text-muted" style="padding: 24px 0; font-size: 13px;">No sensitivity parameters found.</p>';
    return;
  }

  // Resolve display names (fallback to param key if metadata absent)
  const displayName = (paramName) =>
    parameterMetadata[paramName]?.display_name || paramName;

  // Build global y-axis ordering: highest |elasticity| at top.
  // Plotly renders category axis bottom→top, so the LAST entry in categoryarray is at the TOP.
  // We want highest |elasticity| (first in `sorted`) at the top → reverse for categoryarray.
  const yLabels = sorted.map(([paramName]) => displayName(paramName));
  const categoryArray = [...yLabels].reverse();

  // --- Whisker trace (population range, rendered behind bars) ---
  // For each parameter present in populationContext with ≥2 concepts, show [min, max] as an
  // error-bar scatter trace. Absent for concept-unique parameters (only 1 concept in index).
  const whiskerTrace = _buildWhiskerTrace(sorted, parameterMetadata, populationContext, displayName);

  // --- Primary bar traces (one per category, solid + hatched variants) ---
  // Group sorted params by category
  const byCategory = {};
  for (const [paramName, entry] of sorted) {
    const meta = parameterMetadata[paramName];
    const category = meta ? meta.category : "shared-baseline";
    if (!byCategory[category]) byCategory[category] = [];
    byCategory[category].push({ paramName, entry, meta });
  }

  const barTraces = _buildBarTraces(byCategory, displayName);

  const traces = [];
  if (whiskerTrace) traces.push(whiskerTrace);
  traces.push(...barTraces);

  const layout = {
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { l: 10, r: 30, t: 10, b: 30 },
    height: Math.max(300, sorted.length * 28 + 120),
    xaxis: {
      title: {
        text: "Elasticity (\u0394LCOE% / \u0394param%)",
        font: { color: "#8b949e", size: 11 },
        standoff: 8,
      },
      zeroline: true,
      zerolinecolor: "#30363d",
      zerolinewidth: 2,
      gridcolor: "#21262d",
      tickfont: { color: "#6e7681", size: 11 },
      tickformat: ".2f",
    },
    yaxis: {
      tickfont: { color: "#8b949e", size: 11 },
      automargin: true,
      categoryorder: "array",
      categoryarray: categoryArray,
    },
    barmode: "overlay",
    legend: {
      font: { color: "#8b949e", size: 11 },
      bgcolor: "transparent",
      bordercolor: "#30363d",
      borderwidth: 1,
      orientation: "h",
      x: 0,
      y: -0.12,
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

  // Wire click handler — Plotly fires plotly_click on the container element
  if (onParameterClick) {
    container.on("plotly_click", (eventData) => {
      if (!eventData || !eventData.points || eventData.points.length === 0) return;
      const point = eventData.points[0];
      // customdata is set per-point on bar traces
      const cd = point.customdata;
      if (cd && cd.paramName) {
        onParameterClick(cd.paramName, cd.meta || null);
      }
    });
  }
}

/**
 * Build the whisker scatter trace showing [min, max] elasticity range across concepts.
 * Returns null if populationContext is absent or no parameters have population data.
 *
 * Why: visually secondary (low opacity) error-bar scatter placed before bar traces so bars
 * render on top. Using error_x centered at midpoint of [min, max] range per parameter.
 *
 * @param {Array} sorted - [[paramName, entry], ...] sorted by |elasticity|
 * @param {Object} parameterMetadata
 * @param {Object|null} populationContext - ParameterIndex or null
 * @param {Function} displayName - paramName → string
 * @returns {Object|null} Plotly trace or null
 */
function _buildWhiskerTrace(sorted, parameterMetadata, populationContext, displayName) {
  if (!populationContext || !populationContext.parameters) return null;

  const x = [];
  const y = [];
  const errorMinus = [];
  const errorPlus = [];

  for (const [paramName] of sorted) {
    const indexEntry = populationContext.parameters[paramName];
    // Absent (concept-unique) → no whisker
    if (!indexEntry || !indexEntry.concepts || indexEntry.concepts.length < 2) continue;

    const elasticities = indexEntry.concepts.map((c) => c.elasticity);
    const minE = Math.min(...elasticities);
    const maxE = Math.max(...elasticities);
    const center = (minE + maxE) / 2;

    x.push(center);
    y.push(displayName(paramName));
    // Asymmetric error bars from center to each edge
    errorPlus.push(maxE - center);
    errorMinus.push(center - minE);
  }

  if (x.length === 0) return null;

  return {
    type: "scatter",
    x,
    y,
    mode: "markers",
    name: "Population range",
    marker: {
      color: "rgba(139, 148, 158, 0.25)",
      size: 4,
      symbol: "line-ns-open",
      line: { width: 2, color: "rgba(139, 148, 158, 0.35)" },
    },
    error_x: {
      type: "data",
      symmetric: false,
      array: errorPlus,
      arrayminus: errorMinus,
      visible: true,
      color: "rgba(139, 148, 158, 0.35)",
      thickness: 1.5,
      width: 5,
    },
    hoverinfo: "skip",
    showlegend: true,
    legendrank: 1000,
  };
}

/**
 * Build bar traces grouped by category (solid confidence levels) and hatched (low confidence).
 * One trace per category for the legend; low-confidence bars get a separate hatched trace
 * so Plotly's fillpattern applies consistently within each trace.
 *
 * @param {Object} byCategory - { category: [{paramName, entry, meta}] }
 * @param {Function} displayName - paramName → string
 * @returns {Array} Array of Plotly bar trace objects
 */
function _buildBarTraces(byCategory, displayName) {
  const traces = [];

  for (const category of TORNADO_CATEGORY_ORDER) {
    const params = byCategory[category];
    if (!params || params.length === 0) continue;

    const color = TORNADO_CATEGORY_COLORS[category] || "#6B7280";
    const label = TORNADO_CATEGORY_LABELS[category] || category;

    // Separate solid (high/medium) from hatched (low confidence)
    const solid = params.filter((p) => !p.meta || p.meta.confidence !== "low");
    const hatched = params.filter((p) => p.meta && p.meta.confidence === "low");

    if (solid.length > 0) {
      traces.push(_buildSolidTrace(solid, color, label, category, displayName));
    }

    if (hatched.length > 0) {
      // Show hatched trace in legend only if no solid trace exists for this category
      // (avoids duplicate legend entries for the same category)
      const showInLegend = solid.length === 0;
      traces.push(_buildHatchedTrace(hatched, color, label, category, showInLegend, displayName));
    }
  }

  return traces;
}

/**
 * Build a solid bar trace for one category.
 * Opacity encodes confidence: high=1.0, medium=0.8.
 */
function _buildSolidTrace(params, color, label, category, displayName) {
  const x = params.map((p) => p.entry.elasticity);
  const y = params.map((p) => displayName(p.paramName));
  const markerColors = params.map((p) => {
    const opacity = TORNADO_CONFIDENCE_OPACITY[p.meta?.confidence] ?? 1.0;
    return _hexToRgba(color, opacity);
  });
  const hovertext = params.map(
    (p) =>
      `<b>${displayName(p.paramName)}</b><br>` +
      `Elasticity: ${p.entry.elasticity.toFixed(3)}<br>` +
      `Category: ${label}<br>` +
      `Confidence: ${p.meta?.confidence || "unknown"}`
  );
  const customdata = params.map((p) => ({ paramName: p.paramName, meta: p.meta }));

  return {
    type: "bar",
    orientation: "h",
    x,
    y,
    name: label,
    marker: {
      color: markerColors,
      line: { color: _hexToRgba(color, 0.5), width: 1 },
    },
    hovertemplate: "%{hovertext}<extra></extra>",
    hovertext,
    customdata,
    legendgroup: category,
    showlegend: true,
    legendrank: TORNADO_CATEGORY_ORDER.indexOf(category),
  };
}

/**
 * Build a hatched bar trace for low-confidence bars in one category.
 * Uses Plotly fillpattern for hatch texture; opacity is 0.6 per design system.
 */
function _buildHatchedTrace(params, color, label, category, showlegend, displayName) {
  const x = params.map((p) => p.entry.elasticity);
  const y = params.map((p) => displayName(p.paramName));
  const hovertext = params.map(
    (p) =>
      `<b>${displayName(p.paramName)}</b> (?)<br>` +
      `Elasticity: ${p.entry.elasticity.toFixed(3)}<br>` +
      `Category: ${label}<br>` +
      `Confidence: low`
  );
  const customdata = params.map((p) => ({ paramName: p.paramName, meta: p.meta }));

  return {
    type: "bar",
    orientation: "h",
    x,
    y,
    name: showlegend ? label : `${label} (low confidence)`,
    marker: {
      color: _hexToRgba(color, TORNADO_CONFIDENCE_OPACITY.low),
      pattern: {
        shape: "/",
        bgcolor: "transparent",
        fgcolor: _hexToRgba(color, 0.9),
        size: 6,
        solidity: 0.3,
      },
      line: { color: _hexToRgba(color, 0.5), width: 1 },
    },
    hovertemplate: "%{hovertext}<extra></extra>",
    hovertext,
    customdata,
    legendgroup: category,
    // Hide in legend when a solid trace already represents this category (avoid duplicate entries)
    showlegend: showlegend,
    legendrank: TORNADO_CATEGORY_ORDER.indexOf(category),
  };
}

/**
 * Convert a 6-digit hex color + alpha to "rgba(r, g, b, a)" string.
 * Why: Plotly marker.color accepts rgba() strings for per-point opacity control.
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
