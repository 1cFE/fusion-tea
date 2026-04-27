/**
 * cas_breakdown.js — CAS cost breakdown widget.
 *
 * Tabbed widget with two views: Table (default, composition stripe + ranked rows)
 * and Treemap (proportional tiles, drill into CAS22 sub-accounts). View, expand,
 * and drill-in state persist across re-renders so slider drags don't snap the
 * user out of their view.
 *
 * Pure DOM + SVG — no Plotly.
 */

"use strict";

const CAS_ORDER = [
  "cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
  "cas26", "cas27", "cas28", "cas29", "cas30",
  "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
];

const CAS22_ORDER = [
  "C220101", "C220102", "C220103", "C220104", "C220105", "C220106",
  "C220107", "C220108", "C220109", "C220110", "C220111", "C220112",
  "C220200", "C220300", "C220400", "C220500", "C220600", "C220700",
];

const CAS_COLORS = {
  cas10: "#6B7280", cas21: "#3B82F6", cas22: "#10B981", cas23: "#F59E0B",
  cas24: "#8B5CF6", cas25: "#EC4899", cas26: "#06B6D4", cas27: "#F97316",
  cas28: "#84CC16", cas29: "#EF4444", cas30: "#64748B", cas40: "#78716C",
  cas50: "#A78BFA", cas60: "#FB7185", cas70: "#34D399", cas80: "#FCD34D",
  cas90: "#94A3B8",
};

const CAS22_COLORS = [
  "#059669", "#047857", "#065F46", "#064E3B",
  "#10B981", "#34D399", "#6EE7B7", "#A7F3D0",
  "#52A8A8", "#3D8B8B", "#2E7070", "#1F5555",
  "#0F3D3D", "#062A2A",
];

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

const SVG_NS = "http://www.w3.org/2000/svg";

// Per-container UI state survives re-render (slider drag).
// WeakMap so state is GC'd with the container element.
const _stateByContainer = new WeakMap();

function _getState(container) {
  let s = _stateByContainer.get(container);
  if (!s) {
    s = { activeView: "table", cas22Expanded: false, drilledInto: null };
    _stateByContainer.set(container, s);
  }
  return s;
}

function _fmtMoney(v) {
  if (v >= 1000) return v.toLocaleString(undefined, { maximumFractionDigits: 0 }) + " M$";
  if (v >= 10) return v.toFixed(0) + " M$";
  return v.toFixed(1) + " M$";
}

function _pct(part, total) {
  return total ? ((part / total) * 100).toFixed(1) + "%" : "0.0%";
}

/**
 * Render the CAS cost breakdown widget.
 *
 * @param {HTMLElement} container - Target element. Cleared and rebuilt.
 * @param {Object} options
 * @param {Object} options.cas - { casXX: { name, cost_m_usd, overridden } }.
 * @param {Object} [options.cas22_detail={}] - { CXXXXXX: { name, cost_m_usd, overridden } }.
 * @param {Function} [options.onAccountClick=null] - Fires on click of a non-CAS22 row.
 *   Signature: (casCode, accountData) => void. CAS22 click is internal (expand or drill).
 */
function renderCASBreakdown(container, options) {
  const {
    cas,
    cas22_detail = {},
    onAccountClick = null,
  } = options;

  const state = _getState(container);
  const ctx = { container, cas, cas22_detail, onAccountClick, state };

  _buildShell(ctx);
  _renderActiveView(ctx);
}

function _buildShell(ctx) {
  const { container, state } = ctx;
  container.innerHTML = "";
  container.classList.add("cas-widget");

  const header = document.createElement("div");
  header.className = "cas-widget__header";

  const tabs = document.createElement("div");
  tabs.className = "cas-widget__tabs";
  tabs.setAttribute("role", "tablist");

  const btnTable = document.createElement("button");
  btnTable.type = "button";
  btnTable.textContent = "Table";
  btnTable.className = "cas-widget__tab" + (state.activeView === "table" ? " is-active" : "");
  btnTable.addEventListener("click", () => _setView(ctx, "table"));

  const btnTreemap = document.createElement("button");
  btnTreemap.type = "button";
  btnTreemap.textContent = "Treemap";
  btnTreemap.className = "cas-widget__tab" + (state.activeView === "treemap" ? " is-active" : "");
  btnTreemap.addEventListener("click", () => _setView(ctx, "treemap"));

  tabs.appendChild(btnTable);
  tabs.appendChild(btnTreemap);
  header.appendChild(tabs);
  container.appendChild(header);

  const totalLine = document.createElement("div");
  totalLine.className = "cas-widget__total-line";
  totalLine.innerHTML =
    `<span>Total capital + annualized:</span>` +
    `<b class="cas-widget__total"></b>`;
  container.appendChild(totalLine);

  const viewMount = document.createElement("div");
  viewMount.className = "cas-widget__view";
  container.appendChild(viewMount);

  ctx.tabs = { table: btnTable, treemap: btnTreemap };
  ctx.totalEl = totalLine.querySelector(".cas-widget__total");
  ctx.viewMount = viewMount;
}

function _setView(ctx, name) {
  ctx.state.activeView = name;
  ctx.tabs.table.classList.toggle("is-active", name === "table");
  ctx.tabs.treemap.classList.toggle("is-active", name === "treemap");
  _renderActiveView(ctx);
}

function _renderActiveView(ctx) {
  ctx.viewMount.innerHTML = "";
  if (ctx.state.activeView === "table") {
    _renderTable(ctx);
  } else {
    _renderTreemap(ctx);
  }
}

function _topLevelRows(cas) {
  return CAS_ORDER
    .filter((k) => cas[k] && cas[k].cost_m_usd > 0)
    .map((k) => [k, cas[k]])
    .sort((a, b) => b[1].cost_m_usd - a[1].cost_m_usd);
}

function _hasCAS22Detail(cas22_detail) {
  return Object.values(cas22_detail).some((s) => s && s.cost_m_usd > 0);
}

function _cas22SubRows(cas22_detail) {
  // Maintain CAS22_ORDER index for stable color assignment, then sort by cost.
  return CAS22_ORDER
    .map((key, idx) => ({ key, idx, account: cas22_detail[key] }))
    .filter((r) => r.account && r.account.cost_m_usd > 0)
    .sort((a, b) => b.account.cost_m_usd - a.account.cost_m_usd);
}

// =============== TABLE VIEW ===============
function _renderTable(ctx) {
  const { cas, cas22_detail, viewMount, totalEl } = ctx;
  const rows = _topLevelRows(cas);
  const total = rows.reduce((s, [, a]) => s + a.cost_m_usd, 0);
  const hasSubs = _hasCAS22Detail(cas22_detail);

  totalEl.textContent = _fmtMoney(total);

  // Composition stripe
  const stripeWrap = document.createElement("div");
  stripeWrap.className = "cas-widget__stripe-wrap";

  const stripe = document.createElement("div");
  stripe.className = "cas-widget__stripe";
  for (const [casKey, a] of rows) {
    const seg = document.createElement("div");
    seg.className = "cas-widget__stripe-seg" + (a.overridden ? " is-overridden" : "");
    seg.style.flex = `${a.cost_m_usd} 0 0`;
    seg.style.background = CAS_COLORS[casKey] || "#6B7280";
    seg.title =
      `${a.name}${a.overridden ? " ★" : ""}\n` +
      `${_fmtMoney(a.cost_m_usd)} · ${_pct(a.cost_m_usd, total)}`;
    stripe.appendChild(seg);
  }
  stripeWrap.appendChild(stripe);

  const caption = document.createElement("div");
  caption.className = "cas-widget__stripe-caption";
  const largest = rows[0]
    ? `${rows[0][1].name} (${_pct(rows[0][1].cost_m_usd, total)})`
    : "—";
  caption.innerHTML =
    `<span>Composition (hover for detail) →</span>` +
    `<span>Largest segment: <b>${_escapeHTML(largest)}</b></span>`;
  stripeWrap.appendChild(caption);
  viewMount.appendChild(stripeWrap);

  // Table
  const table = document.createElement("table");
  table.className = "cas-widget__table";
  table.innerHTML =
    `<thead><tr>` +
    `<th>CAS Account</th>` +
    `<th class="num">Cost</th>` +
    `<th class="num">% of total</th>` +
    `</tr></thead>`;
  const tbody = document.createElement("tbody");
  table.appendChild(tbody);

  for (const [casKey, a] of rows) {
    const isCAS22 = casKey === "cas22" && hasSubs;
    const tr = document.createElement("tr");
    if (isCAS22) {
      tr.className = "is-expandable";
      tr.addEventListener("click", () => {
        ctx.state.cas22Expanded = !ctx.state.cas22Expanded;
        _renderActiveView(ctx);
      });
    } else if (ctx.onAccountClick) {
      tr.classList.add("is-clickable");
      tr.addEventListener("click", () => ctx.onAccountClick(casKey, a));
    }

    const chev = isCAS22 ? (ctx.state.cas22Expanded ? "▾" : "▸") : "";
    const swatchOver = a.overridden ? " is-overridden" : "";
    const star = a.overridden ? '<span class="cas-widget__star" title="Overridden">★</span>' : "";
    tr.innerHTML =
      `<td class="cas-widget__name">` +
      `<span class="cas-widget__chev">${chev}</span>` +
      `<span class="cas-widget__swatch${swatchOver}" style="background-color:${CAS_COLORS[casKey] || "#6B7280"};"></span>` +
      `${_escapeHTML(a.name)}${star}` +
      `</td>` +
      `<td class="num">${_fmtMoney(a.cost_m_usd)}</td>` +
      `<td class="num cas-widget__pct"><b>${_pct(a.cost_m_usd, total)}</b></td>`;
    tbody.appendChild(tr);

    if (isCAS22 && ctx.state.cas22Expanded) {
      for (const { idx, account } of _cas22SubRows(cas22_detail)) {
        const subColor = CAS22_COLORS[idx % CAS22_COLORS.length];
        const subTr = document.createElement("tr");
        subTr.className = "is-sub";
        const subSwatchOver = account.overridden ? " is-overridden" : "";
        const subStar = account.overridden ? '<span class="cas-widget__star" title="Overridden">★</span>' : "";
        subTr.innerHTML =
          `<td class="cas-widget__name cas-widget__name--sub">` +
          `<span class="cas-widget__swatch${subSwatchOver}" style="background-color:${subColor};"></span>` +
          `${_escapeHTML(account.name)}${subStar}` +
          `</td>` +
          `<td class="num">${_fmtMoney(account.cost_m_usd)}</td>` +
          `<td class="num cas-widget__pct"><b>${_pct(account.cost_m_usd, total)}</b></td>`;
        tbody.appendChild(subTr);
      }
    }
  }

  viewMount.appendChild(table);
}

// =============== TREEMAP VIEW ===============
function _renderTreemap(ctx) {
  const { cas, cas22_detail, viewMount } = ctx;
  const totalAll = CAS_ORDER.reduce(
    (s, k) => s + (cas[k] ? cas[k].cost_m_usd || 0 : 0),
    0
  );

  // Reset drill-in if CAS22 has no detail (data shape changed).
  if (ctx.state.drilledInto === "cas22" && !_hasCAS22Detail(cas22_detail)) {
    ctx.state.drilledInto = null;
  }

  const breadcrumb = document.createElement("div");
  breadcrumb.className = "cas-widget__breadcrumb";

  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("class", "cas-widget__treemap");
  const W = 1392, H = 600;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("preserveAspectRatio", "none");

  let values, headerLabel;
  if (ctx.state.drilledInto === "cas22") {
    values = _cas22SubRows(cas22_detail).map(({ key, idx, account }) => ({
      id: key,
      name: account.name,
      value: account.cost_m_usd,
      color: CAS22_COLORS[idx % CAS22_COLORS.length],
      overridden: !!account.overridden,
      drillable: false,
    }));
    headerLabel =
      `CAS22 — Reactor Plant Equipment ` +
      `(${_fmtMoney(cas.cas22.cost_m_usd)} · ${_pct(cas.cas22.cost_m_usd, totalAll)} of total)`;
  } else {
    values = _topLevelRows(cas).map(([key, a]) => ({
      id: key,
      name: a.name,
      value: a.cost_m_usd,
      color: CAS_COLORS[key] || "#6B7280",
      overridden: !!a.overridden,
      drillable: key === "cas22" && _hasCAS22Detail(cas22_detail),
      account: a,
    }));
  }

  if (ctx.state.drilledInto === "cas22") {
    const back = document.createElement("a");
    back.className = "cas-widget__breadcrumb-link";
    back.textContent = "← All CAS";
    back.addEventListener("click", () => {
      ctx.state.drilledInto = null;
      _renderActiveView(ctx);
    });
    breadcrumb.appendChild(back);
    breadcrumb.appendChild(document.createTextNode(`  /  ${headerLabel}`));
  } else {
    breadcrumb.textContent =
      "Click a tile to inspect; CAS22 (Reactor Plant Equipment) drills into sub-accounts.";
  }

  viewMount.appendChild(breadcrumb);
  viewMount.appendChild(svg);

  // Hatch pattern for overridden tiles
  const defs = document.createElementNS(SVG_NS, "defs");
  defs.innerHTML =
    `<pattern id="cas-widget-hatch" patternUnits="userSpaceOnUse" ` +
    `width="6" height="6" patternTransform="rotate(45)">` +
    `<line x1="0" y1="0" x2="0" y2="6" stroke="rgba(252,211,77,0.5)" stroke-width="2"/>` +
    `</pattern>`;
  svg.appendChild(defs);

  const tiles = _squarify(values, 0, 0, W, H);

  for (const t of tiles) {
    const g = document.createElementNS(SVG_NS, "g");
    g.setAttribute("class", "cas-widget__tile" + (t.drillable ? " is-drillable" : ""));

    if (t.drillable) {
      g.addEventListener("click", () => {
        ctx.state.drilledInto = t.id;
        _renderActiveView(ctx);
      });
    } else if (ctx.onAccountClick && ctx.state.drilledInto === null && t.account) {
      g.classList.add("is-clickable");
      g.addEventListener("click", () => ctx.onAccountClick(t.id, t.account));
    }

    const rect = document.createElementNS(SVG_NS, "rect");
    rect.setAttribute("class", "cas-widget__tile-bg");
    rect.setAttribute("x", t.x);
    rect.setAttribute("y", t.y);
    rect.setAttribute("width", t.w);
    rect.setAttribute("height", t.h);
    rect.setAttribute("fill", t.color);
    g.appendChild(rect);

    if (t.overridden) {
      const ov = document.createElementNS(SVG_NS, "rect");
      ov.setAttribute("x", t.x);
      ov.setAttribute("y", t.y);
      ov.setAttribute("width", t.w);
      ov.setAttribute("height", t.h);
      ov.setAttribute("fill", "url(#cas-widget-hatch)");
      ov.setAttribute("pointer-events", "none");
      g.appendChild(ov);
    }

    if (t.w > 70 && t.h > 28) {
      const lbl = document.createElementNS(SVG_NS, "text");
      lbl.setAttribute("class", "cas-widget__tile-label");
      lbl.setAttribute("x", t.x + 8);
      lbl.setAttribute("y", t.y + 18);
      lbl.textContent =
        (t.overridden ? "★ " : "") + t.name + (t.drillable ? "  ▸" : "");
      g.appendChild(lbl);

      const sub = document.createElementNS(SVG_NS, "text");
      sub.setAttribute("class", "cas-widget__tile-sub");
      sub.setAttribute("x", t.x + 8);
      sub.setAttribute("y", t.y + 34);
      sub.textContent = `${_fmtMoney(t.value)} · ${_pct(t.value, totalAll)}`;
      g.appendChild(sub);
    } else if (t.w > 30 && t.h > 16) {
      const lbl = document.createElementNS(SVG_NS, "text");
      lbl.setAttribute("class", "cas-widget__tile-sub");
      lbl.setAttribute("x", t.x + 4);
      lbl.setAttribute("y", t.y + 12);
      lbl.textContent = _fmtMoney(t.value);
      g.appendChild(lbl);
    }

    const title = document.createElementNS(SVG_NS, "title");
    title.textContent =
      `${t.name}${t.overridden ? " (overridden)" : ""}\n` +
      `${_fmtMoney(t.value)} · ${_pct(t.value, totalAll)} of total`;
    g.appendChild(title);

    svg.appendChild(g);
  }
}

// Squarified treemap layout. Returns tiles {x, y, w, h, ...originalFields}.
function _squarify(values, x, y, w, h) {
  const total = values.reduce((s, v) => s + v.value, 0);
  const tiles = [];
  if (total <= 0 || values.length === 0) return tiles;
  const scale = (w * h) / total;
  let remaining = values.map((v) => ({ ...v, area: v.value * scale }));
  let curX = x, curY = y, curW = w, curH = h;

  while (remaining.length > 0) {
    const shorter = Math.min(curW, curH);
    const row = [];
    let rowSum = 0;
    let bestRatio = Infinity;

    for (let i = 0; i < remaining.length; i++) {
      const candSum = rowSum + remaining[i].area;
      const candRow = row.concat(remaining[i]);
      const candRatio = _worstRatio(candRow, candSum, shorter);
      if (candRatio < bestRatio) {
        row.push(remaining[i]);
        rowSum = candSum;
        bestRatio = candRatio;
      } else {
        break;
      }
    }

    const stripThickness = rowSum / shorter;
    let pos = 0;
    for (const tile of row) {
      const tileLen = (tile.area / rowSum) * shorter;
      if (curW >= curH) {
        tiles.push({ ...tile, x: curX, y: curY + pos, w: stripThickness, h: tileLen });
      } else {
        tiles.push({ ...tile, x: curX + pos, y: curY, w: tileLen, h: stripThickness });
      }
      pos += tileLen;
    }
    if (curW >= curH) { curX += stripThickness; curW -= stripThickness; }
    else              { curY += stripThickness; curH -= stripThickness; }
    remaining = remaining.slice(row.length);
  }
  return tiles;
}

function _worstRatio(row, rowSum, shorter) {
  if (rowSum <= 0) return Infinity;
  const stripThickness = rowSum / shorter;
  let worst = 0;
  for (const t of row) {
    const tileLen = (t.area / rowSum) * shorter;
    const r = Math.max(stripThickness / tileLen, tileLen / stripThickness);
    if (r > worst) worst = r;
  }
  return worst;
}

function _escapeHTML(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
