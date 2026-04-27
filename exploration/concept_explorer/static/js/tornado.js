/**
 * tornado.js — Integrated sensitivity grid component.
 *
 * Each row: [ name+elasticity | bar | slider | value ].
 *
 * Owns slider lifecycle (override map, debounced onSliderChange callback,
 * reset()) so concept_page.js only routes the callback to /api/compute and
 * to the sticky headline. Standalone concepts (sensitivities === null) render
 * a placeholder.
 *
 * Public API (stable; do not break view_sensitivity.js comparison view):
 *   renderTornado(container, options) → { reset } | undefined
 *   TORNADO_CATEGORY_COLORS, TORNADO_CATEGORY_LABELS, TORNADO_CATEGORY_ORDER
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

const SLIDER_DEBOUNCE_MS = 200;
const ROW_GRID_TEMPLATE = "220px minmax(180px, 1fr) minmax(200px, 1fr) 90px";
const LABEL_COL_WIDTH_PX = 220;

/**
 * Render the integrated sensitivity grid.
 *
 * @param {HTMLElement} container — cleared and replaced
 * @param {Object} options
 * @param {Object|null} options.sensitivities — { engineering: {...}, financial: {...} } or null
 * @param {Object} options.parameterMetadata — { paramKey → ParameterMetadata }
 * @param {Object} [options.populationContext=null]
 * @param {number} [options.topN=15]
 * @param {Function} [options.onParameterClick=null] — (paramName, meta) => void
 * @param {Function} [options.onSliderChange=null]   — (overrides) => void, debounced
 * @returns {{ reset: Function } | undefined}
 *   `reset()` returns sliders to baselines and fires one final onSliderChange({}).
 *   Returns undefined for standalone concepts (no sliders to reset).
 */
function renderTornado(container, options) {
  const {
    sensitivities,
    parameterMetadata,
    populationContext = null,
    topN = 15,
    onParameterClick = null,
    onSliderChange = null,
  } = options;

  // Standalone concept: placeholder, no sliders, no reset handle
  if (sensitivities === null) {
    container.innerHTML =
      '<p class="text-muted" style="padding: 24px 0; font-style: italic; font-size: 13px;">' +
      "No sensitivity data available \u2014 this concept uses a standalone cost model" +
      "</p>";
    return undefined;
  }

  // Merge engineering + financial into one flat map (carries `group` for color dot)
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

  // Top-N by |elasticity|
  const sorted = Object.entries(merged)
    .sort((a, b) => Math.abs(b[1].elasticity) - Math.abs(a[1].elasticity))
    .slice(0, topN);

  if (sorted.length === 0) {
    container.innerHTML =
      '<p class="text-muted" style="padding: 24px 0; font-size: 13px;">No sensitivity parameters found.</p>';
    return undefined;
  }

  // Per-render slider state, owned by this render call
  const baselines = {}; // paramName → baseline value
  const overrides = {}; // paramName → current value (always populated; equals baseline at start)
  const sliderInputs = {}; // paramName → <input type=range>
  const valueCells = {}; // paramName → <div> showing current value
  let debounceTimer = null;

  // Compute x-axis extent for bar scaling (include population whisker extents)
  const allElasticities = sorted.map(([, e]) => e.elasticity);
  let maxAbs = Math.max(...allElasticities.map(Math.abs));
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
  maxAbs *= 1.1;
  if (maxAbs === 0) maxAbs = 1;

  // Build DOM
  container.innerHTML = "";

  const wrapper = document.createElement("div");
  wrapper.className = "tornado-chart";
  wrapper.style.cssText = "width: 100%; font-family: inherit;";

  // --- Column header row ---
  wrapper.appendChild(_buildHeaderRow());

  // --- Parameter rows ---
  for (const [paramName, entry] of sorted) {
    const meta = parameterMetadata[paramName] || {};
    const row = _buildRow({
      paramName,
      entry,
      meta,
      maxAbs,
      populationContext,
      onParameterClick,
      // Slider integration
      onInput: (newVal) => {
        overrides[paramName] = newVal;
        valueCells[paramName].textContent = _formatValue(newVal, meta);
        _updateValueClass(valueCells[paramName], newVal, baselines[paramName], entry.elasticity);
        _scheduleFire();
      },
      registerSlider: (input, valueCell, baseline) => {
        baselines[paramName] = baseline;
        overrides[paramName] = baseline;
        sliderInputs[paramName] = input;
        valueCells[paramName] = valueCell;
      },
    });
    wrapper.appendChild(row);
  }

  // --- X-axis label ---
  const axisLabel = document.createElement("div");
  axisLabel.style.cssText = `
    text-align: center;
    font-size: 11px;
    color: #8b949e;
    padding: 8px 0 4px;
    margin-left: ${LABEL_COL_WIDTH_PX}px;
    margin-right: 290px; /* slider+value col widths approximated */
  `;
  axisLabel.textContent = "Elasticity (\u0394LCOE% / \u0394param%)";
  wrapper.appendChild(axisLabel);

  // --- Legend ---
  wrapper.appendChild(_buildLegend(sorted, parameterMetadata, populationContext));

  container.appendChild(wrapper);

  // --- Slider firing (debounced) + reset handle ---
  function _scheduleFire() {
    if (!onSliderChange) return;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      onSliderChange({ ...overrides });
    }, SLIDER_DEBOUNCE_MS);
  }

  function reset() {
    // Clear slider UI state only. The caller is responsible for any
    // result-state updates (sticky headline, CAS breakdown) — going through
    // /api/compute on Reset is unnecessary work AND triggers a real bug:
    // the compute API returns un-scaled `result` values that don't match the
    // extraction-time `result_1gw`-scaled headline, so a Reset round-trip
    // would appear as a phantom "▼ improvement" delta.
    for (const [paramName, input] of Object.entries(sliderInputs)) {
      const baseline = baselines[paramName];
      input.value = String(baseline);
      overrides[paramName] = baseline;
      const meta = parameterMetadata[paramName] || {};
      valueCells[paramName].textContent = _formatValue(baseline, meta);
      _updateValueClass(valueCells[paramName], baseline, baseline, 0);
    }
    clearTimeout(debounceTimer);
  }

  // Expose reset on the container for callers that don't capture the return value
  // (and as a return value for callers that do).
  container._tornadoReset = reset;
  return { reset };
}

// ---------------------------------------------------------------------------
// Internal builders
// ---------------------------------------------------------------------------

function _buildHeaderRow() {
  const header = document.createElement("div");
  header.className = "tornado-row tornado-row--header";
  header.style.cssText = `
    display: grid;
    grid-template-columns: ${ROW_GRID_TEMPLATE};
    gap: 0 12px;
    align-items: center;
    height: 24px;
    border-bottom: 1px solid #30363d;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6e7681;
    padding-bottom: 4px;
  `;
  const cols = [
    { text: "Parameter", align: "left" },
    { text: "Elasticity", align: "center" },
    { text: "What-if", align: "left" },
    { text: "Value", align: "right" },
  ];
  for (const c of cols) {
    const cell = document.createElement("div");
    cell.style.textAlign = c.align;
    cell.textContent = c.text;
    header.appendChild(cell);
  }
  return header;
}

function _buildRow({
  paramName, entry, meta, maxAbs, populationContext,
  onParameterClick, onInput, registerSlider,
}) {
  const category = meta.category || "unclassified";
  const confidence = meta.confidence || "unknown";
  const color = TORNADO_CATEGORY_COLORS[category] || TORNADO_CATEGORY_COLORS["unclassified"];
  const opacity = TORNADO_CONFIDENCE_OPACITY[confidence] ?? 0.8;
  const isLowConfidence = confidence === "low";
  const elasticity = entry.elasticity;
  const displayName = meta.display_name || paramName;

  const row = document.createElement("div");
  row.className = "tornado-row";
  row.dataset.paramName = paramName;
  row.style.cssText = `
    display: grid;
    grid-template-columns: ${ROW_GRID_TEMPLATE};
    gap: 0 12px;
    align-items: center;
    height: 36px;
    border-bottom: 1px solid rgba(48, 54, 61, 0.5);
  `;
  row.title =
    `${displayName}\n` +
    `Elasticity: ${elasticity.toFixed(3)}\n` +
    `Category: ${TORNADO_CATEGORY_LABELS[category] || category}\n` +
    `Confidence: ${confidence}`;

  // --- Label cell (dot · name · elasticity badge) ---
  const labelCell = document.createElement("div");
  labelCell.style.cssText = `
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12.5px;
    color: #e6edf3;
    overflow: hidden;
    cursor: ${onParameterClick ? "pointer" : "default"};
  `;

  const dot = document.createElement("span");
  dot.style.cssText = `
    flex-shrink: 0;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: ${color};
  `;
  labelCell.appendChild(dot);

  const nameSpan = document.createElement("span");
  nameSpan.style.cssText = `
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1 1 auto;
    min-width: 0;
  `;
  nameSpan.textContent = displayName;
  labelCell.appendChild(nameSpan);

  const elastBadge = document.createElement("span");
  elastBadge.style.cssText = `
    flex-shrink: 0;
    font-family: ui-monospace, monospace;
    font-size: 11px;
    color: #6e7681;
    font-variant-numeric: tabular-nums;
  `;
  const sign = elasticity > 0 ? "+" : "";
  elastBadge.textContent = sign + elasticity.toFixed(2);
  labelCell.appendChild(elastBadge);

  if (onParameterClick) {
    labelCell.addEventListener("click", () => onParameterClick(paramName, meta));
  }

  // --- Bar cell (zero line, whisker behind, elasticity bar) ---
  const barCell = document.createElement("div");
  barCell.style.cssText = `
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    cursor: ${onParameterClick ? "pointer" : "default"};
  `;

  const zeroLine = document.createElement("div");
  zeroLine.style.cssText = `
    position: absolute;
    left: 50%;
    top: 8px; bottom: 8px;
    width: 1px;
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
    height: 18px;
    background: ${barBg};
    border: 1px solid ${_hexToRgba(color, 0.5)};
    border-radius: 2px;
    z-index: 2;
    transition: filter 0.15s;
  `;
  bar.addEventListener("mouseenter", () => { bar.style.filter = "brightness(1.2)"; });
  bar.addEventListener("mouseleave", () => { bar.style.filter = ""; });
  barCell.appendChild(bar);

  if (onParameterClick) {
    barCell.addEventListener("click", () => onParameterClick(paramName, meta));
  }

  // --- Slider cell ---
  const sliderCell = document.createElement("div");
  sliderCell.style.cssText = "display: flex; align-items: center;";

  // --- Value cell ---
  const valueCell = document.createElement("div");
  valueCell.style.cssText = `
    text-align: right;
    font-family: ui-monospace, monospace;
    font-size: 12px;
    color: #e6edf3;
    font-variant-numeric: tabular-nums;
  `;

  // Build slider only when range is available and finite
  const range = meta.range;
  const hasRange =
    Array.isArray(range)
    && range.length === 2
    && Number.isFinite(range[0])
    && Number.isFinite(range[1])
    && range[1] > range[0];

  if (hasRange) {
    const baseline = Number.isFinite(meta.baseline) ? meta.baseline : range[0];
    const input = document.createElement("input");
    input.type = "range";
    input.id = `slider-${_safeId(paramName)}`;
    input.min = String(range[0]);
    input.max = String(range[1]);
    input.step = String((range[1] - range[0]) / 200);
    input.value = String(baseline);
    input.dataset.paramName = paramName;
    input.setAttribute("aria-label", displayName);
    input.style.cssText = `
      -webkit-appearance: none; appearance: none;
      width: 100%; height: 4px;
      background: #30363d;
      border-radius: 2px;
      outline: none;
      cursor: pointer;
    `;
    input.addEventListener("input", (e) => {
      const v = parseFloat(e.target.value);
      if (Number.isFinite(v)) onInput(v);
    });
    sliderCell.appendChild(input);

    valueCell.textContent = _formatValue(baseline, meta);
    registerSlider(input, valueCell, baseline);
  } else {
    // Show baseline value if available; otherwise dash
    const baseline = Number.isFinite(meta.baseline) ? meta.baseline : null;
    valueCell.textContent = baseline === null ? "—" : _formatValue(baseline, meta);
    valueCell.title = "No slider range available for this parameter";
  }

  row.appendChild(labelCell);
  row.appendChild(barCell);
  row.appendChild(sliderCell);
  row.appendChild(valueCell);
  return row;
}

function _buildLegend(sorted, parameterMetadata, populationContext) {
  const categoriesPresent = new Set(
    sorted.map(([pn]) => (parameterMetadata[pn]?.category || "unclassified"))
  );

  const legend = document.createElement("div");
  legend.style.cssText = `
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 0 4px ${LABEL_COL_WIDTH_PX}px;
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

  return legend;
}

// ---------------------------------------------------------------------------
// Formatting helpers
// ---------------------------------------------------------------------------

function _formatValue(rawValue, meta) {
  const multiplier = Number.isFinite(meta.display_multiplier) ? meta.display_multiplier : 1;
  const unit = meta.display_unit || "";
  const v = rawValue * multiplier;
  let body;
  if (unit === "%") {
    body = v.toFixed(1) + "%";
  } else if (Math.abs(v) >= 100) {
    body = v.toFixed(0) + (unit ? " " + unit : "");
  } else if (Math.abs(v) >= 10) {
    body = v.toFixed(1) + (unit ? " " + unit : "");
  } else {
    body = v.toFixed(3) + (unit ? " " + unit : "");
  }
  return body;
}

function _updateValueClass(cell, currentValue, baseline, elasticity) {
  cell.style.color = "#e6edf3";
  if (!Number.isFinite(baseline) || baseline === 0) return;
  if (Math.abs(currentValue - baseline) < 1e-9) return;
  const dPct = (currentValue - baseline) / baseline;
  const lcoeDir = elasticity * dPct;
  // Green when LCOE goes down, orange when LCOE goes up
  cell.style.color = lcoeDir < 0 ? "#10B981" : "#F59E0B";
}

function _hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha.toFixed(2)})`;
}

function _safeId(name) {
  return String(name).replace(/[^A-Za-z0-9_-]/g, "_");
}
