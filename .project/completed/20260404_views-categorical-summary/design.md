# Design: Categorical & Summary Views

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 20:07 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 3a

## Overview

Implement two new view types for the comparison page — Categorical (taxonomy attribute table) and Summary (headline economics comparison) — that register on the existing `VIEW_REGISTRY` in `comparison.js`. Each view renders in both Integrated (shared panel, all concepts) and Landscape (per-concept card) modes. Includes a reusable axis synchronization utility for Landscape mode.

## Related Artifacts

- **Spec:** `.project/active/views-categorical-summary/spec.md`
- **Concept:** `.project/active/explorer-ux-v2/concept.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 3a)
- **Shell design:** `.project/active/compare-shell/design.md`
- **Shell code:** `exploration/concept_explorer/static/js/comparison.js`

## Research Findings

### Files Analyzed

| File | Key Takeaways |
|------|--------------|
| `comparison.js` (:54-62) | `VIEW_REGISTRY` exposed as `window.VIEW_REGISTRY`. Render dispatch at :476-495. `renderViewContent()` calls `view.renderIntegrated(container, concepts)` for integrated or `view.renderLandscape(container, concept, syncContext)` for landscape. `syncContext` shape: `{allConcepts, sharedScales}` — currently passes `sharedScales: {}`. |
| `comparison.js` (:460-470) | `getConceptDataArray()` builds `{concept_id, name, confinement_family, data: ConceptData}` from `conceptCache`. The `data` field is the full `/api/concepts/{id}` response. |
| `taxonomy_card.js` (:22-32) | `ATTR_DISPLAY` array defines 9 cross-cutting fields with display labels. Null → "—" with `.taxonomy-card__value--na`; "TBD"/"Unknown" → as-is with `.taxonomy-card__value--tbd`. |
| `concept_page.js` (:121-141) | Headline card uses `.headline-grid` + `.headline-metric` pattern. Each metric: label (xs, uppercase) → value (mono, xl) → unit (sm). |
| `explorer.css` (:710-763) | Headline metric CSS: `.headline-grid` is `grid-template-columns: repeat(auto-fit, minmax(120px, 1fr))`. `.headline-metric` has surface-2 bg, border, padding. |
| `explorer.css` (:851-877) | Table styling: `.comparison-table th` uppercase + letter-spacing. `.comparison-table td` with mono font. Row classes: `.match`, `.diff`. |
| `tornado.js` (:67-207) | Plotly dark theme: `paper_bgcolor/plot_bgcolor: "transparent"`, text color `#8b949e`, grid `#21262d`, hover bg `#21262d`. `config: { displayModeBar: false, responsive: true }`. |
| `cas_breakdown.js` (:25-48) | `CAS_COLORS` map for 17 accounts. Family color CSS vars: `--color-badge-mfe: #3b82f6`, `--color-badge-ife: #a855f7`, `--color-badge-mif: #f59e0b`, `--color-badge-nonstandard: #6b7280`. |
| `models.py` (:337-351) | `ConceptData` has `confinement_family` but NO other taxonomy fields. Taxonomy data is only in `/api/taxonomy/registry` → `ConceptRegistry`. |
| `taxonomy_models.py` (:185-217) | `ConceptTaxonomy` has all 20 taxonomy fields. Hierarchical validation: MFE must have `mfe_topology`, non-MFE must not; same for IFE/`ife_driver`, etc. |
| `server.py` (:600) | `/api/taxonomy/registry` → `ConceptRegistry` (all concepts with full taxonomy). |

### Key Data Flow Insight

The comparison shell fetches concept data via `/api/concepts/{id}`, which returns `ConceptData` — economics but no taxonomy beyond `confinement_family`. The Categorical view needs taxonomy data from `/api/taxonomy/registry`, which returns the full `ConceptRegistry` with all 20 fields per concept.

**Design implication:** The Categorical view must fetch taxonomy data independently via `/api/taxonomy/registry` and build a lookup by `concept_id`. This fetch is done once and cached.

### Reusable Patterns

- **DOM helpers:** `el(tag, cls, text)`, `append(parent, ...children)` — used across all JS modules
- **Family badges:** `FAMILY_META` lookup → `<span class="${cls}">${label}</span>` — carried over in `comparison.js` (:33-42)
- **Table styling:** Existing `.comparison-table` CSS in `explorer.css` (:851-877) — reusable for Categorical
- **Metric display:** `.headline-metric` pattern in `explorer.css` (:710-763) — reusable for Summary metrics
- **Plotly config:** Dark theme constants from `tornado.js` — reusable for Summary chart

## Proposed Design

### Architecture Overview

```
compare.html.j2
  └─ <script src="/static/js/comparison.js">    (existing shell)
  └─ <script src="/static/js/view_categorical.js"> (NEW — registers on VIEW_REGISTRY)
  └─ <script src="/static/js/view_summary.js">     (NEW — registers on VIEW_REGISTRY)

view_categorical.js
  ├─ Fetches /api/taxonomy/registry (once, cached)
  ├─ TAXONOMY_FIELDS array (field → label, 20 entries)
  ├─ renderIntegrated(container, concepts) → comparison table
  └─ renderLandscape(container, concept, ctx) → attribute card

view_summary.js
  ├─ HEADLINE_METRICS array (field → label → unit → format)
  ├─ computeSharedScales(concepts) → {min, max} per metric
  ├─ renderIntegrated(container, concepts) → grouped bar chart + metrics table
  ├─ renderLandscape(container, concept, ctx) → single bar chart + metrics
  └─ Axis sync: computeSharedScales exported for Item 3b reuse
```

### Component 1: Categorical View (`view_categorical.js`)

**Purpose:** Compare taxonomy attributes across selected concepts in table (Integrated) or card (Landscape) format.

**Data source:** `/api/taxonomy/registry` — fetched once on first render, cached in module scope.

#### Taxonomy Field Definition

```javascript
const TAXONOMY_FIELDS = [
  // Hierarchical
  { field: "confinement_family", label: "Confinement" },
  { field: "mfe_topology",      label: "MFE Topology",    applicableTo: "MFE" },
  { field: "tokamak_shape",     label: "Tokamak Shape",   applicableTo: "MFE" },
  { field: "stellarator_type",  label: "Stellarator Type", applicableTo: "MFE" },
  { field: "ife_driver",        label: "IFE Driver",      applicableTo: "IFE" },
  { field: "laser_approach",    label: "Laser Approach",   applicableTo: "IFE" },
  { field: "mif_method",        label: "MIF Method",      applicableTo: "MIF" },
  { field: "non_standard_mechanism", label: "Mechanism",   applicableTo: "NONSTANDARD" },
  // Cross-cutting
  { field: "fuel",              label: "Fuel" },
  { field: "primary_heating",   label: "Primary Heating" },
  { field: "energy_capture",    label: "Energy Capture" },
  { field: "plasma_state",      label: "Plasma State" },
  { field: "magnet_type",       label: "Magnet Type" },
  { field: "tritium_breeding",  label: "Tritium Breeding" },
  { field: "neutron_management", label: "Neutron Mgmt" },
  { field: "operation_mode",    label: "Operation Mode" },
  { field: "repetition_rate",   label: "Rep Rate" },
  { field: "driver_technology", label: "Driver Tech" },
  // Metadata
  { field: "confidence",        label: "Confidence" },
];
```

The `applicableTo` property enables FR-5 (inapplicable vs. unknown distinction). When a field has `applicableTo` and the concept's `confinement_family` doesn't match, the cell renders "—" (not applicable). When the family matches but the value is null, the cell renders "N/A" (applicable but unknown). Fields without `applicableTo` always apply.

#### Row Visibility

Not all fields are interesting for every comparison. Hierarchical sub-type fields (`tokamak_shape`, `stellarator_type`, `laser_approach`, `mif_method`, `non_standard_mechanism`) are only relevant when at least one selected concept has that family. Rather than always showing 20 rows with many "—" cells:

- **Filter rule:** A hierarchical field row is shown only when at least one concept in the comparison has a matching `confinement_family` for that field's `applicableTo`.
- **Cross-cutting fields** (no `applicableTo`): always shown.
- This reduces visual noise while preserving completeness — all applicable fields are visible.

#### Integrated Mode — Comparison Table

Renders a `<table class="comparison-table">` (reusing the existing CSS class from `explorer.css` :1040-1066, which already provides `.diff`, `.match`, `.attr-label` styling) with:
- **Header row:** first cell is "Attribute", then one cell per concept (name + family badge)
- **Body rows:** one per visible `TAXONOMY_FIELDS` entry
  - First cell: field label (`.attr-label`)
  - Concept cells: field value with styling based on state:
    - Value present → plain text
    - `null` on applicable field → "N/A" with `.taxonomy-card__value--tbd` class
    - "TBD" or "Unknown" string → as-is with `.taxonomy-card__value--tbd` class  
    - Not applicable (family mismatch on hierarchical field) → "—" with `.taxonomy-card__value--na` class
  - **Row highlighting:** When values differ across concepts, add `.diff` class to `<tr>` for subtle background tint (existing CSS: `rgba(248, 113, 113, 0.06)`). When all match, add `.match` class. This directly supports the business goal: "correlate descriptive differences to economic differences."

#### Landscape Mode — Attribute Cards

Renders a single `.card` inside the landscape cell container with:
- **Field list:** rows of label → value pairs, same styling as taxonomy_card.js attribute rows
- Reuses `.taxonomy-card__attr`, `.taxonomy-card__label`, `.taxonomy-card__value` CSS classes
- Same null/TBD/inapplicable handling as integrated mode
- Filters out inapplicable hierarchical fields (don't show `mfe_topology` row on an IFE concept's card)

#### Data Fetch & Cache

```javascript
let _taxonomyCache = null; // concept_id → ConceptTaxonomy object

async function ensureTaxonomy() {
  if (_taxonomyCache) return _taxonomyCache;
  const resp = await fetch("/api/taxonomy/registry");
  if (!resp.ok) throw new Error("Failed to fetch taxonomy registry");
  const data = await resp.json();
  _taxonomyCache = {};
  for (const c of data.concepts) {
    _taxonomyCache[c.concept_id] = c;
  }
  return _taxonomyCache;
}
```

Both `renderIntegrated` and `renderLandscape` call `ensureTaxonomy()` (async, but cached after first call). Since the shell's `renderViewContent()` calls the render function synchronously, the view function must handle the async fetch internally — clear container, show a brief loading state, then render when data arrives.

**Loading pattern:** The taxonomy fetch is fast (JSON already in server memory, ~38 concepts), so a simple inline "Loading..." text that's replaced on completion is sufficient. No shimmer animation needed.

### Component 2: Summary View (`view_summary.js`)

**Purpose:** Compare headline economics across selected concepts via chart + metrics table.

**Data source:** `concept.data.cost_model.headline` from the concept data already fetched by the shell (in `conceptCache`). No additional API calls needed.

#### Metric Definitions

```javascript
const HEADLINE_METRICS = [
  { field: "lcoe_per_mwh",        label: "LCOE",           unit: "$/MWh", format: v => v.toFixed(1) },
  { field: "overnight_cost_per_kw", label: "Overnight Cost", unit: "$/kW",  format: v => v.toFixed(0) },
  { field: "p_net_mw",            label: "Net Power",       unit: "MW",    format: v => v.toFixed(0) },
  { field: "q_eng",               label: "Q_eng",           unit: "",      format: v => v.toFixed(2) },
  { field: "capacity_factor",     label: "Capacity Factor", unit: "",      format: v => (v * 100).toFixed(1) + "%" },
];

const CAS_ACCOUNT_KEYS = [
  "cas10", "cas21", "cas22", "cas23", "cas24", "cas25", "cas26", "cas27",
  "cas28", "cas29", "cas30", "cas40", "cas50", "cas60", "cas70", "cas80", "cas90"
];
```

#### Integrated Mode — Grouped Bar Chart + Metrics Table

**Chart (Plotly):** A grouped bar chart comparing the 5 headline metrics across concepts. Each concept is one trace; metrics are categories on the x-axis.

**Problem:** The 5 metrics have wildly different scales (LCOE ~50-200, overnight cost ~2000-10000, P_net ~200-2000, Q_eng ~1-30, capacity factor ~0.5-0.9). A single shared y-axis would be meaningless.

**Solution — Small multiples within a single Plotly figure using subplots:**
- 5 side-by-side subplots (one per metric), each with its own y-axis
- Each subplot shows one grouped bar per concept
- Concepts distinguished by color (family color from `FAMILY_COLORS`)
- Shared legend at the bottom

This is the standard approach for comparing values on different scales — it works naturally with Plotly's `make_subplots` equivalent (manual `xaxis`/`xaxis2`/... domain specification in layout).

**Family Colors for Traces:**
```javascript
const FAMILY_COLORS = {
  MFE: "#3b82f6",
  IFE: "#a855f7",
  MIF: "#f59e0b",
  NONSTANDARD: "#6b7280",
};
```

When multiple concepts share a family (e.g., two MFE concepts), differentiate by opacity stepping or lighter/darker shade. For v1 with max 3 concepts in Integrated mode, a simple approach: use family color as base, apply opacity 1.0 for first concept of that family, 0.7 for second, 0.5 for third.

**Metrics Table:** Below the chart, a compact comparison table:
- Header: "Metric" + one column per concept (name + family badge)
- Rows: one per `HEADLINE_METRICS` entry — label, then formatted values with units
- **Top CAS driver row** (FR-8): Last row shows the largest CAS account per concept (name + % of total). Computed by iterating `CAS_ACCOUNT_KEYS`, summing `cost_m_usd`, finding the max. Helpful hint toward the CapEx view.
- Uses `<table class="comparison-table comparison-table--summary">` — base class provides standard table styling, modifier adds right-aligned mono values

**No-cost-model handling (FR-11, FR-12):** Concepts without `data.cost_model` are excluded from the chart traces but shown in the metrics table with "—" in every value cell and a subtle "No cost model" note. This keeps the table complete (all selected concepts visible) while the chart only shows meaningful data.

#### Landscape Mode — Per-Concept Panels

Each landscape cell gets:

1. **Bar chart:** Horizontal bar chart of the 5 metrics for that single concept. Uses the same Plotly dark theme. Axis ranges synchronized via `syncContext.sharedScales`.

2. **Metrics list:** Below the chart, a compact vertical list of label → value → unit, using `.headline-metric` pattern from existing CSS.

3. **Top CAS driver:** Single line at the bottom: "Top CAS: {name} ({pct}%)"

4. **No-cost-model:** If the concept has no cost model, the entire cell shows a centered placeholder: "No cost model available" with muted text, matching the existing `.compare-placeholder` style but without the dashed border (since the landscape cell already has a solid border).

#### Axis Synchronization

For Landscape mode, bar charts must use consistent scales so visual comparison is meaningful. The shell passes `syncContext = { allConcepts, sharedScales: {} }` — currently empty. The Summary view computes its own shared scales internally rather than relying on the shell to pre-compute them (since scale computation is view-specific).

```javascript
function computeSharedScales(concepts) {
  const scales = {};
  for (const metric of HEADLINE_METRICS) {
    let min = Infinity, max = -Infinity;
    for (const c of concepts) {
      if (!c.data.cost_model) continue;
      const val = c.data.cost_model.headline[metric.field];
      if (val < min) min = val;
      if (val > max) max = val;
    }
    if (min === Infinity) { min = 0; max = 1; } // No data — fallback
    // Pad by 10% for visual breathing room
    const pad = (max - min) * 0.1 || max * 0.1 || 1;
    scales[metric.field] = { min: Math.max(0, min - pad), max: max + pad };
  }
  return scales;
}
```

**Reusability for Item 3b:** This function is internal to `view_summary.js` but establishes the pattern. Item 3b views (CapEx, Sensitivity) will implement analogous scale computation for their own data. No shared utility module is needed — the pattern is simple enough to replicate, and each view's scale logic differs (Summary: 5 scalar metrics; CapEx: 17 CAS account costs; Sensitivity: elasticity ranges). A premature shared abstraction would add complexity without benefit.

### Component 3: Script Loading & Registration

#### Template Change (`compare.html.j2`)

Add two script tags after `comparison.js`:

```html
{% block scripts %}
<script src="/static/js/comparison.js"></script>
<script src="/static/js/view_categorical.js"></script>
<script src="/static/js/view_summary.js"></script>
{% endblock %}
```

Order matters: `comparison.js` defines `window.VIEW_REGISTRY`; view scripts register on it.

#### Registration Pattern

Each view file immediately registers its render functions (no DOMContentLoaded wait needed — the shell only calls render functions after init, which happens on DOMContentLoaded).

**Convention:** Each view file defines its own local `el(tag, cls, text)` and `append(parent, ...children)` DOM helpers, matching the pattern used in `comparison.js` (:89-101), `taxonomy_card.js`, and other modules. These are module-local (inside the IIFE), not shared globals.

```javascript
// view_categorical.js
"use strict";
(function () {
  // Local DOM helpers (same pattern as comparison.js:89-101)
  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }
  function append(parent, ...children) {
    for (const c of children) { if (c != null) parent.appendChild(c); }
    return parent;
  }

  // ... module internals ...

  window.VIEW_REGISTRY.categorical.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.categorical.renderLandscape = renderLandscape;
})();
```

This matches the shell's dispatch logic at `comparison.js:476-495` — it checks `view.renderIntegrated` / `view.renderLandscape` for truthiness before calling.

### CSS Additions to `explorer.css`

Minimal new CSS. The Categorical view reuses `.comparison-table` (existing in `explorer.css` :1040-1066) which already provides `th` uppercase styling, `.diff` / `.match` row backgrounds, `.attr-label`, and `td` padding/borders. Only view-specific sub-classes are added:

```css
/* Categorical view — sub-classes for .comparison-table */
.comparison-table .val--na {
  color: var(--color-text-muted);
  font-style: italic;
}
.comparison-table .val--tbd {
  color: var(--color-text-muted);
}

/* Summary view — metrics comparison table (extends .comparison-table too) */
.comparison-table--summary td {
  text-align: right;
  font-family: var(--font-mono);
}
.comparison-table--summary td:first-child,
.comparison-table--summary th:first-child {
  text-align: left;
  font-family: var(--font-sans);
}
.comparison-table--summary .unit {
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
  margin-left: var(--space-1);
}
.comparison-table--summary .no-data {
  color: var(--color-text-muted);
  font-style: italic;
  font-family: var(--font-sans);
}

/* Summary landscape — compact metric list */
.summary-metric-row {
  display: flex;
  justify-content: space-between;
  padding: var(--space-1) 0;
  font-size: var(--font-size-sm);
  border-bottom: 1px solid var(--color-border-subtle);
}
.summary-metric-row:last-child {
  border-bottom: none;
}
.summary-metric-row__label {
  color: var(--color-text-muted);
}
.summary-metric-row__value {
  font-family: var(--font-mono);
  font-weight: 600;
}

/* No-cost-model placeholder (inline, within view area) */
.view-no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  font-style: italic;
}
```

### File Changes Summary

| File | Action | Description |
|------|--------|-------------|
| `view_categorical.js` | **New** | Categorical view: taxonomy comparison table/cards, registers on VIEW_REGISTRY |
| `view_summary.js` | **New** | Summary view: headline economics chart + metrics table, registers on VIEW_REGISTRY |
| `compare.html.j2` | **Edit** | Add two `<script>` tags for view files |
| `explorer.css` | **Append** | CSS for categorical table, summary metrics, no-data placeholder |

No changes to `comparison.js`, `server.py`, or any existing JS files.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Plotly subplot layout for 5 different-scale metrics may be visually awkward in narrow panels | Med | Test with real data; fall back to metrics-table-only if chart adds more confusion than clarity |
| Taxonomy registry fetch adds latency on first Categorical render | Low | Registry is small (~38 concepts), cached after first fetch. Brief "Loading..." text during fetch. |
| Family color collisions when multiple concepts share a family | Low | Opacity stepping (1.0 / 0.7 / 0.5) differentiates. Max 3 concepts in Integrated mode limits collision count. |
| Async render inside synchronous dispatch contract | Low | Shell clears container before calling render function. View clears again and shows loading, then replaces on data arrival. No race condition — each render call owns its container. |

## Integration Strategy

**With comparison shell (Item 2):** Zero-touch integration. Views register render functions on `window.VIEW_REGISTRY`; shell dispatches to them. No shell code changes needed.

**With Item 3b (CapEx, Sensitivity):** Item 3b follows the same registration pattern. The axis sync approach (view-internal `computeSharedScales`) is replicated, not shared — each view has different scale semantics. Item 3b views add their own `<script>` tags to the template.

**With existing pages:** No impact. New JS files are only loaded on the compare page via `compare.html.j2`.

## Validation Approach

**Manual testing checklist:**

1. **Categorical Integrated:** Select 2-3 concepts → Categorical view shows comparison table with all taxonomy fields, diff rows highlighted, inapplicable fields show "—"
2. **Categorical Landscape:** Switch to Landscape → each concept card shows its own attribute list, inapplicable fields omitted
3. **Summary Integrated:** Select Summary → grouped subplot chart + metrics table with correct values and units
4. **Summary Landscape:** Switch to Landscape → per-concept charts with synced axes, metrics below
5. **No cost model:** Add a concept without a cost model → Summary shows "No cost model available" placeholder, no JS errors
6. **Mixed selection:** 2 concepts with cost models + 1 without → Summary chart shows 2, table shows all 3 with "—" for missing
7. **View switching:** Rapidly toggle between Categorical ↔ Summary in both modes — containers clear properly, no stale DOM
8. **URL persistence:** Select Summary in right panel → refresh page → Summary still selected in right panel
9. **Regression:** Concept profile page, index grid, taxonomy views all work unchanged

---

**Next Step:** After approval → `/_my_plan`
