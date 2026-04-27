/**
 * tornado.js — Tornado chart component for parameter sensitivity visualization.
 *
 * DOM-based implementation (replaces Plotly) rendering an HTML/CSS grid with:
 * - Category color encoding (design system colors from explorer.css)
 * - Confidence opacity (1.0 / 0.8 / 0.6) + hatched fill for low-confidence bars
 * - Population whiskers: [min, max] elasticity range across concepts
 * - Click handler for parameter detail popover
 * - Tooltip on hover with parameter name, elasticity, category, confidence
 *
 * No external dependencies — pure DOM.
 */

"use strict";

// Category → hex color (matches --color-* custom properties in explorer.css)
const TORNADO_CATEGORY_COLORS = {
  "shared-baseline": "#6B7280",
  "well-established": "#3B82F6",
  "key-innovation": "#10B981",
  "concept-unique": "#F59E0B",
  "high-risk": "#EF4444",
  "unclassified": "#6B7280",
};

const TORNADO_CATEGORY_LABELS = {
  "shared-baseline": "Shared Baseline",
  "well-established": "Well Established",
  "key-innovation": "Key Innovation",
  "concept-unique": "Concept Unique",
  "high-risk": "High Risk",
  "unclassified": "Unclassified",
};

// Display order for categories in legend
const TORNADO_CATEGORY_ORDER = [
  "shared-baseline",
  "well-established",
  "key-innovation",
  "concept-unique",
  "high-risk",
  "unclassified",
];

const TORNADO_CONFIDENCE_OPACITY = {
  high: 1.0,
  medium: 0.8,
  low: 0.6,
  unknown: 0.8,
};

/**
 * Render a tornado chart of sensitivity elasticities into a DOM element.
 *
 * @param {HTMLElement} container - Target DOM element (will be cleared and replaced)
 * @param {Object} options
 * @param {Object|null} options.sensitivities
 * @param {Object} options.parameterMetadata
 * @param {Object} [options.populationContext=null]
 * @param {number} [options.topN=15]
 * @param {Function} [options.onParameterClick=null]
 */
function renderTornado(container, options) {
  const {
    sensitivities,
    parameterMetadata,
    populationContext = null,
    topN = 15,
    onParameterClick = null,
  } = options;

  // Standalone concept: show placeholder
  if (sensitivities === null) {
    container.innerHTML =
      '<p class="text-muted" style="padding: 24px 0; font-style: italic; font-size: 13px;">' +
      "No sensitivity data available \u2014 this concept uses a standalone cost model" +
      "</p>";
    return;
  }

  // Merge engineering + financial into one flat map
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

  // Resolve display names
  const displayName = (paramName) =>
    parameterMetadata[paramName]?.display_name || paramName;

  // Compute x-axis extent for scaling
  const allElasticities = sorted.map(([, e]) => e.elasticity);
  let maxAbs = Math.max(...allElasticities.map(Math.abs));

  // Include population whisker extents
  if (populationContext?.parameters) {
    for (const [paramName] of sorted) {
      const ie = populationContext.parameters[paramName];
      if (ie?.concepts?.length >= 2) {
        for (const c of ie.concepts) {
          maxAbs = Math.max(maxAbs, Math.abs(c.elasticity));
        }
      }
    }
  }
  // Add 10% padding
  maxAbs *= 1.1;
  if (maxAbs === 0) maxAbs = 1;

  // Build DOM
  container.innerHTML = "";

  const wrapper = document.createElement("div");
  wrapper.className = "tornado-chart";
  wrapper.style.cssText = "width: 100%; font-family: inherit;";

  // --- Rows ---
  for (const [paramName, entry] of sorted) {
    const meta = parameterMetadata[paramName] || {};
    const category = meta.category || "unclassified";
    const confidence = meta.confidence || "unknown";
    const color = TORNADO_CATEGORY_COLORS[category] || TORNADO_CATEGORY_COLORS["unclassified"];
    const opacity = TORNADO_CONFIDENCE_OPACITY[confidence] ?? 0.8;
    const isLowConfidence = confidence === "low";
    const elasticity = entry.elasticity;

    const row = document.createElement("div");
    row.className = "tornado-row";
    row.style.cssText = `
      display: grid;
      grid-template-columns: 180px 1fr 60px;
      align-items: center;
      height: 32px;
      cursor: pointer;
      border-bottom: 1px solid rgba(48, 54, 61, 0.5);
    `;
    row.title =
      `${displayName(paramName)}\n` +
      `Elasticity: ${elasticity.toFixed(3)}\n` +
      `Category: ${TORNADO_CATEGORY_LABELS[category] || category}\n` +
      `Confidence: ${confidence}`;

    // Click handler
    if (onParameterClick) {
      row.addEventListener("click", () => onParameterClick(paramName, meta));
      row.style.cursor = "pointer";
    }

    // --- Label cell ---
    const labelCell = document.createElement("div");
    labelCell.style.cssText = `
      font-size: 12px;
      color: #8b949e;
      text-align: right;
      padding-right: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    `;
    // Category dot
    const dot = document.createElement("span");
    dot.style.cssText = `
      display: inline-block;
      width: 8px; height: 8px;
      border-radius: 50%;
      background: ${color};
      margin-right: 6px;
      vertical-align: middle;
    `;
    labelCell.appendChild(dot);
    labelCell.appendChild(document.createTextNode(displayName(paramName)));

    // --- Bar cell (contains the dual-direction bar + whisker) ---
    const barCell = document.createElement("div");
    barCell.style.cssText = `
      position: relative;
      height: 100%;
      display: flex;
      align-items: center;
    `;

    // Zero line
    const zeroLine = document.createElement("div");
    zeroLine.style.cssText = `
      position: absolute;
      left: 50%;
      top: 0; bottom: 0;
      width: 2px;
      background: #30363d;
      z-index: 1;
    `;
    barCell.appendChild(zeroLine);

    // Population whisker (behind bar)
    if (populationContext?.parameters) {
      const ie = populationContext.parameters[paramName];
      if (ie?.concepts?.length >= 2) {
        const elasticities = ie.concepts.map((c) => c.elasticity);
        const minE = Math.min(...elasticities);
        const maxE = Math.max(...elasticities);

        const whiskerLeft = 50 + (minE / maxAbs) * 50;
        const whiskerRight = 50 + (maxE / maxAbs) * 50;

        const whisker = document.createElement("div");
        whisker.style.cssText = `
          position: absolute;
          left: ${whiskerLeft}%;
          width: ${whiskerRight - whiskerLeft}%;
          height: 2px;
          background: rgba(139, 148, 158, 0.35);
          z-index: 0;
        `;
        barCell.appendChild(whisker);

        // Whisker end caps
        for (const pos of [whiskerLeft, whiskerRight]) {
          const cap = document.createElement("div");
          cap.style.cssText = `
            position: absolute;
            left: ${pos}%;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 1px;
            height: 10px;
            background: rgba(139, 148, 158, 0.35);
            z-index: 0;
          `;
          barCell.appendChild(cap);
        }
      }
    }

    // Elasticity bar
    const barWidthPct = Math.abs(elasticity) / maxAbs * 50;
    const barLeftPct = elasticity >= 0 ? 50 : 50 - barWidthPct;

    const bar = document.createElement("div");
    const barBg = isLowConfidence
      ? `repeating-linear-gradient(
           45deg,
           ${_hexToRgba(color, opacity)},
           ${_hexToRgba(color, opacity)} 3px,
           transparent 3px,
           transparent 6px
         )`
      : _hexToRgba(color, opacity);
    bar.style.cssText = `
      position: absolute;
      left: ${barLeftPct}%;
      width: ${barWidthPct}%;
      height: 20px;
      background: ${barBg};
      border: 1px solid ${_hexToRgba(color, 0.5)};
      border-radius: 2px;
      z-index: 2;
      transition: filter 0.15s;
    `;
    bar.addEventListener("mouseenter", () => { bar.style.filter = "brightness(1.2)"; });
    bar.addEventListener("mouseleave", () => { bar.style.filter = ""; });
    barCell.appendChild(bar);

    // --- Value cell ---
    const valueCell = document.createElement("div");
    valueCell.style.cssText = `
      font-size: 11px;
      color: #6e7681;
      text-align: right;
      padding-left: 8px;
      font-variant-numeric: tabular-nums;
    `;
    valueCell.textContent = elasticity.toFixed(3);

    row.appendChild(labelCell);
    row.appendChild(barCell);
    row.appendChild(valueCell);
    wrapper.appendChild(row);
  }

  // --- X-axis label ---
  const axisLabel = document.createElement("div");
  axisLabel.style.cssText = `
    text-align: center;
    font-size: 11px;
    color: #8b949e;
    padding: 8px 0 4px;
    margin-left: 180px;
  `;
  axisLabel.textContent = "Elasticity (\u0394LCOE% / \u0394param%)";
  wrapper.appendChild(axisLabel);

  // --- Legend ---
  const categoriesPresent = new Set(
    sorted.map(([pn]) => (parameterMetadata[pn]?.category || "unclassified"))
  );

  const legend = document.createElement("div");
  legend.style.cssText = `
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 0 4px 180px;
    font-size: 11px;
    color: #8b949e;
    border-top: 1px solid #21262d;
  `;

  for (const cat of TORNADO_CATEGORY_ORDER) {
    if (!categoriesPresent.has(cat)) continue;
    const item = document.createElement("span");
    item.style.cssText = "display: flex; align-items: center; gap: 4px;";
    const swatch = document.createElement("span");
    swatch.style.cssText = `
      display: inline-block;
      width: 10px; height: 10px;
      border-radius: 2px;
      background: ${TORNADO_CATEGORY_COLORS[cat]};
    `;
    item.appendChild(swatch);
    item.appendChild(document.createTextNode(TORNADO_CATEGORY_LABELS[cat] || cat));
    legend.appendChild(item);
  }

  // Population range legend item
  if (populationContext?.parameters) {
    const hasWhisker = sorted.some(([pn]) => {
      const ie = populationContext.parameters[pn];
      return ie?.concepts?.length >= 2;
    });
    if (hasWhisker) {
      const item = document.createElement("span");
      item.style.cssText = "display: flex; align-items: center; gap: 4px;";
      const line = document.createElement("span");
      line.style.cssText = `
        display: inline-block;
        width: 16px; height: 2px;
        background: rgba(139, 148, 158, 0.35);
      `;
      item.appendChild(line);
      item.appendChild(document.createTextNode("Population range"));
      legend.appendChild(item);
    }
  }

  wrapper.appendChild(legend);
  container.appendChild(wrapper);
}

/**
 * Convert a 6-digit hex color + alpha to "rgba(r, g, b, a)" string.
 */
function _hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha.toFixed(2)})`;
}
