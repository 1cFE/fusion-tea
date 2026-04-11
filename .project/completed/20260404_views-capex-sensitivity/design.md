# Design: CapEx & Sensitivity Views

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 22:25 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 3b

## Overview

Implement two new comparison view types — CapEx (CAS cost structure drill-down) and Sensitivity (parameter elasticity tornado) — as `view_capex.js` and `view_sensitivity.js`. Both register on the existing `window.VIEW_REGISTRY` and follow the same IIFE + registration pattern established by `view_categorical.js` and `view_summary.js` in Item 3a.

## Related Artifacts

- **Spec:** `.project/active/views-capex-sensitivity/spec.md`
- **Item 3a design:** `.project/active/views-categorical-summary/design.md` (pattern reference)
- **Item 3a code:** `view_categorical.js`, `view_summary.js` (contract reference)
- **Existing charts:** `cas_breakdown.js`, `tornado.js` (reusable logic and constants)
- **Shell:** `comparison.js` (VIEW_REGISTRY, render dispatch, concept data shape)
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 3b)

## Research Findings

### Files Analyzed

| File | Key Takeaways |
|------|--------------|
| `comparison.js` (:54-62) | `VIEW_REGISTRY.capex` and `VIEW_REGISTRY.sensitivity` have null render functions. Shell dispatches at :476-495. |
| `comparison.js` (:460-470) | `getConceptDataArray()` → `{concept_id, name, confinement_family, data}`. The `data` field is full ConceptData from `/api/concepts/{id}`. |
| `comparison.js` (:486-491) | Landscape mode passes `syncContext = { allConcepts: [...], sharedScales: {} }`. Each concept rendered individually. |
| `cas_breakdown.js` (:16-20) | `CAS_ORDER` — 17 CAS keys in display order. |
| `cas_breakdown.js` (:23-27) | `CAS22_ORDER` — 14 sub-account keys in display order. |
| `cas_breakdown.js` (:30-48) | `CAS_COLORS` — 17-color palette keyed by CAS code. |
| `cas_breakdown.js` (:51-56) | `CAS22_COLORS` — 14 green shades for sub-accounts. |
| `cas_breakdown.js` (:58-94) | `CAS_NAMES`, `CAS22_NAMES` — human-readable labels. |
| `cas_breakdown.js` (:391-425) | `_buildSegmentMarker()` for overridden hatch + `_hexToRgba()` utility. |
| `tornado.js` (:16-45) | `TORNADO_CATEGORY_COLORS`, `TORNADO_CATEGORY_LABELS`, `TORNADO_CATEGORY_ORDER`, `TORNADO_CONFIDENCE_OPACITY`. |
| `tornado.js` (:86-104) | Merge engineering + financial into flat map, sort by |elasticity|, take top-N. |
| `tornado.js` (:113-118) | Display name resolution: `parameterMetadata[name]?.display_name || name`. |
| `view_summary.js` (:14-77) | IIFE pattern: local `el()`, `append()`, `FAMILY_META`, `FAMILY_COLORS`, `PLOTLY_THEME`, `PLOTLY_CONFIG`. |
| `view_summary.js` (:123-133) | `assignColors()` — family-based color with opacity stepping [1.0, 0.7, 0.5, ...]. |
| `view_summary.js` (:138-143) | `rgba()` hex-to-rgba converter (duplicated from tornado.js). |
| `view_summary.js` (:149-174) | `computeSharedScales()` — per-metric min/max with 10% padding, skip concepts without data. |
| `view_summary.js` (:444-449) | `purgeCharts()` — Plotly cleanup before re-render. |
| `explorer.css` (:2276-2340) | Item 3a CSS: `.val--na`, `.val--tbd`, `.view-no-data`, `.comparison-table--summary`, `.summary-metric-row`. |
| `compare.html.j2` (:87-89) | Scripts loaded: `comparison.js`, `view_categorical.js`, `view_summary.js`. |
| Data files (`04.json`, `05.json`, `06.json`, `08.json`) | All 4 concepts have full CAS + sensitivity data. Engineering sensitivities vary in param count (10-25 params). Financial group has 1-3 params. |

### Key Design Observations

1. **Existing `cas_breakdown.js` and `tornado.js` are global-scope modules** — their constants (`CAS_ORDER`, `CAS_COLORS`, `CAS_NAMES`, etc.) are globally available. The new view files can reference them directly without duplication.

2. **The Item 3a views are self-contained IIFEs** that duplicate helpers (`el`, `append`, `FAMILY_META`, `FAMILY_COLORS`, `rgba`). This is intentional — module-local scope, no cross-file dependencies. New views follow the same pattern.

3. **`cas_breakdown.js` already has a `sharedScale` option** (:109-112, :136-149) — designed for exactly this use case. But the existing function renders a single stacked bar, not a grouped comparison. The CapEx view needs a fundamentally different chart layout (grouped horizontal bars with CAS as categories).

4. **Landscape mode's `syncContext.sharedScales`** is passed as `{}` by the shell (:489). Each view computes its own scales internally from `syncContext.allConcepts`, matching the pattern in `view_summary.js:484-485`.

5. **Sensitivity parameter overlap**: With 4 concepts and top-N=8, the union set could be up to 32 parameters (worst case, no overlap). In practice, many engineering params are shared (e.g., `construction_time_yr`, `eta_th`, `p_net`), so the union will be smaller. Sorting shared-first makes the chart scannable.

## Proposed Design

### Architecture Overview

```
compare.html.j2
  └─ <script src="/static/js/cas_breakdown.js">       (existing — constants reused)
  └─ <script src="/static/js/tornado.js">              (existing — constants reused)
  └─ <script src="/static/js/comparison.js">           (existing shell)
  └─ <script src="/static/js/view_categorical.js">     (existing — Item 3a)
  └─ <script src="/static/js/view_summary.js">         (existing — Item 3a)
  └─ <script src="/static/js/view_capex.js">           (NEW)
  └─ <script src="/static/js/view_sensitivity.js">     (NEW)

view_capex.js
  ├─ Reads CAS_ORDER, CAS22_ORDER, CAS_COLORS, CAS22_COLORS,
  │  CAS_NAMES, CAS22_NAMES from global scope (cas_breakdown.js)
  ├─ computeSharedMaxCost(concepts) → number
  ├─ renderIntegrated(container, concepts) → grouped horizontal bar chart
  ├─ renderLandscape(container, concept, syncContext) → single horizontal bar + synced axis
  └─ CAS22 expand/collapse toggle (mutable flag, re-renders chart)

view_sensitivity.js
  ├─ Reads TORNADO_CATEGORY_COLORS, TORNADO_CONFIDENCE_OPACITY,
  │  _hexToRgba from global scope (tornado.js)
  ├─ mergeAndRank(sensitivities, topN) → sorted [{paramName, elasticity, group}]
  ├─ buildUnionParams(concepts, topN) → { params, sharedSet }
  ├─ computeSharedElasticityRange(concepts) → number (symmetric max)
  ├─ renderIntegrated(container, concepts) → grouped tornado chart
  └─ renderLandscape(container, concept, syncContext) → single tornado + synced axis
```

### Component 1: CapEx View (`view_capex.js`)

**Purpose:** Compare CAS cost structure across concepts with CAS22 drill-down.

**Data source:** `concept.data.cost_model.cas{10..90}` and `concept.data.cost_model.cas22_detail` — already in `conceptCache`, no additional fetches.

#### Global Constant Reuse

`cas_breakdown.js` declares at module scope (not inside an IIFE):
- `CAS_ORDER` (:16-20) — 17-element array
- `CAS22_ORDER` (:23-27) — 14-element array
- `CAS_COLORS` (:30-48) — color map
- `CAS22_COLORS` (:51-56) — green shades
- `CAS_NAMES` (:58-77) — human labels
- `CAS22_NAMES` (:79-94) — sub-account labels

These are already global. The CapEx view references them directly — no duplication. **Requirement**: `cas_breakdown.js` must be loaded before `view_capex.js` in the template. This is a new dependency — currently `cas_breakdown.js` is only loaded on the concept profile page, not the compare page.

#### CAS22 Expand/Collapse

A mutable `showSubAccounts` flag (module-scoped) tracks whether CAS22 is expanded. When toggled, the entire chart re-renders. Both Integrated and Landscape modes share this flag — expanding CAS22 in one mode applies to the other. This matches the existing `cas_breakdown.js` pattern (:128-129).

**Toggle mechanism:** A button/link below the chart: "▸ Expand CAS22 Detail" / "▾ Collapse CAS22 Detail". Not a click on the bar itself (unlike the concept profile page) because in grouped mode, clicking a specific concept's CAS22 bar is ambiguous about whether to expand all or just that concept. A dedicated toggle is clearer.

#### Integrated Mode — Grouped Horizontal Bars

Renders a single Plotly grouped bar chart:

- **Y-axis**: CAS account names as categories (17 accounts, or 17 - 1 + 14 = 30 when CAS22 expanded)
- **X-axis**: Cost in M$ (shared across all concepts)
- **Traces**: One trace per concept, grouped side-by-side per CAS account
- **Concept colors**: `assignColors(concepts)` — family-based with opacity stepping (same as `view_summary.js:123-133`)
- **Layout**: `barmode: "group"`, horizontal orientation

```javascript
// Pseudocode for trace construction
for (const concept of conceptsWithData) {
  const color = colors[ci];
  const yLabels = [];  // CAS account names in display order
  const xValues = [];  // Cost values
  const hoverTexts = [];

  for (const casKey of CAS_ORDER) {
    if (casKey === "cas22" && showSubAccounts) {
      // Insert sub-accounts instead of aggregate
      for (const subKey of CAS22_ORDER) {
        const sub = costModel.cas22_detail[subKey];
        if (sub) {
          yLabels.push(CAS22_NAMES[subKey]);
          xValues.push(sub.cost_m_usd);
          // hover includes overridden flag + % of total
        }
      }
    } else {
      const account = costModel[casKey];
      yLabels.push(CAS_NAMES[casKey]);
      xValues.push(account ? account.cost_m_usd : 0);
    }
  }

  traces.push({
    type: "bar", orientation: "h",
    y: yLabels, x: xValues,
    name: concept.name,
    marker: { color: rgba(color.base, color.opacity) },
    // ...
  });
}
```

**Y-axis ordering:** Plotly `categoryorder: "array"`, `categoryarray` set to the reversed CAS display order (Plotly renders bottom-to-top). CAS10 at top, CAS90 at bottom. When expanded, CAS22 sub-accounts appear between CAS21 and CAS23 in the natural position.

**Overridden annotations:** In the hover text only (not as separate Plotly annotations) — the star annotation pattern from `cas_breakdown.js` works for a single stacked bar but would be visually noisy on a grouped chart with multiple concepts. Hover text includes "★ overridden" suffix when `account.overridden === true`.

**Total cost label:** Not shown per-bar (too cluttered with grouped layout). Instead, a compact summary line below the chart: "Total: Concept A = 2,733 M$ | Concept B = 4,102 M$". This replaces the annotation-above-bar approach from `cas_breakdown.js` which only works for single-bar stacked charts.

**Chart height:** Dynamic: `Math.min(900, Math.max(400, numCategories * 28 + 120))` — scales with the number of CAS rows. Capped at 900px; if content exceeds this (e.g., CAS22 expanded with 3 concepts), the container scrolls via `overflow-y: auto`.

#### Landscape Mode — Per-Concept Bars

Each landscape cell gets a horizontal bar chart of CAS accounts for that single concept:

- **Y-axis**: CAS account names (same expand/collapse state)
- **X-axis**: Cost in M$, synced across all panels
- **Single trace**: All bars in the concept's family color (full opacity)
- **Bar colors**: Can use `CAS_COLORS` per account (same as concept profile) since there's no grouping ambiguity in single-concept mode
- **Overridden accounts**: Star annotation (matching `cas_breakdown.js` pattern) — works fine for single-concept charts

**Axis synchronization** — max single-account cost (not total, since bars represent individual accounts):

```javascript
function computeSharedMaxAccount(concepts) {
  let max = 0;
  for (const c of concepts) {
    if (!c.data.cost_model) continue;
    for (const key of CAS_ORDER) {
      const acct = c.data.cost_model[key];
      if (acct && acct.cost_m_usd > max) max = acct.cost_m_usd;
    }
    // Also check CAS22 sub-accounts if expanded
    if (showSubAccounts && c.data.cost_model.cas22_detail) {
      for (const sub of Object.values(c.data.cost_model.cas22_detail)) {
        if (sub.cost_m_usd > max) max = sub.cost_m_usd;
      }
    }
  }
  return max > 0 ? max * 1.1 : 1; // 10% padding
}
```

Applied to Plotly layout: `xaxis.range = [0, sharedMax]`.

#### Landscape — Design Choice: CAS-Colored vs Family-Colored Bars

For Landscape mode (single concept per panel), two options:

- **CAS-colored** (each bar colored by its CAS account using `CAS_COLORS`): Matches the concept profile page. Good for seeing cost distribution within one concept.
- **Family-colored** (all bars one color): Consistent with Integrated mode. Visually monotone.

**Decision: CAS-colored.** Landscape panels already have a header with the concept name + family badge, so identity is clear. CAS coloring adds information density — the same color legend works as a visual key when scanning across panels.

#### No-Cost-Model Handling

```javascript
if (!concept.data.cost_model) {
  container.appendChild(el("div", "view-no-data", "No cost model available"));
  return;
}
```

In Integrated mode: filter to concepts with cost models for chart rendering. If none have cost models, show single placeholder.

### Component 2: Sensitivity View (`view_sensitivity.js`)

**Purpose:** Compare parameter sensitivities across concepts via tornado charts.

**Data source:** `concept.data.cost_model.sensitivities` (engineering + financial) and `concept.data.parameter_metadata` — already in `conceptCache`.

#### Global Constant Reuse

`tornado.js` declares at module scope (not inside an IIFE):
- `TORNADO_CATEGORY_COLORS` (:16-22)
- `TORNADO_CATEGORY_LABELS` (:24-30)
- `TORNADO_CATEGORY_ORDER` (:32-38)
- `TORNADO_CONFIDENCE_OPACITY` (:41-45)
- `_hexToRgba()` (:405-410)

These are already global. The Sensitivity view references them directly.

**Requirement:** `tornado.js` must be loaded before `view_sensitivity.js` in the template.

#### Core Data Processing

```javascript
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
```

#### Integrated Mode — Grouped Tornado

**Parameter set construction (union of top-8):**

```javascript
const TOP_N = 8;

function buildUnionParams(concepts) {
  // Step 1: Get each concept's top-8
  const perConcept = new Map(); // conceptId → Set<paramName>
  const allParams = new Map();  // paramName → { appearances: number, maxAbsElasticity: number }

  for (const c of concepts) {
    if (!c.data.cost_model?.sensitivities) continue;
    const ranked = mergeAndRank(c.data.cost_model.sensitivities, TOP_N);
    const paramSet = new Set();
    for (const entry of ranked) {
      paramSet.add(entry.paramName);
      const existing = allParams.get(entry.paramName) || { appearances: 0, maxAbsElasticity: 0 };
      existing.appearances++;
      existing.maxAbsElasticity = Math.max(existing.maxAbsElasticity, Math.abs(entry.elasticity));
      allParams.set(entry.paramName, existing);
    }
    perConcept.set(c.concept_id, paramSet);
  }

  // Step 2: Union of all top-8 sets
  const unionParams = [...allParams.keys()];

  // Step 3: Sort — shared params first (by appearance count desc), then unique (by max |elasticity| desc)
  const conceptCount = perConcept.size;
  unionParams.sort((a, b) => {
    const aInfo = allParams.get(a);
    const bInfo = allParams.get(b);
    const aShared = aInfo.appearances > 1 ? 1 : 0;
    const bShared = bInfo.appearances > 1 ? 1 : 0;
    if (aShared !== bShared) return bShared - aShared; // shared first
    return bInfo.maxAbsElasticity - aInfo.maxAbsElasticity; // then by magnitude
  });

  const sharedSet = new Set(
    unionParams.filter((p) => allParams.get(p).appearances > 1)
  );

  return { params: unionParams, sharedSet };
}
```

**Chart layout:**

- **Y-axis**: Parameter display names as categories, ordered per `unionParams` (shared at top)
- **X-axis**: Elasticity (dimensionless), symmetric around zero
- **Traces**: One trace per concept, grouped side-by-side per parameter
- **Concept colors**: `assignColors(concepts)` — family-based with opacity stepping
- **Barmode**: `"group"`

For each concept, build a trace with all union parameters. If a parameter is not in a concept's sensitivity data, the value is 0 (zero-width bar — parameter exists in the union but this concept doesn't have it).

```javascript
for (const concept of conceptsWithData) {
  const sensitivities = concept.data.cost_model.sensitivities;
  const allSens = {
    ...(sensitivities.engineering || {}),
    ...(sensitivities.financial || {}),
  };
  
  const yLabels = unionParams.map((p) => displayName(p, concept.data.parameter_metadata));
  const xValues = unionParams.map((p) => allSens[p] ? allSens[p].elasticity : 0);

  traces.push({
    type: "bar", orientation: "h",
    y: yLabels, x: xValues,
    name: concept.name,
    marker: { color: rgba(color.base, color.opacity) },
    // hover shows actual elasticity, baseline, param name
  });
}
```

**Shared parameter visual emphasis:** The sort order (shared first) is the primary emphasis. Additionally, a subtle visual separator between shared and unique sections — a Plotly shape (horizontal line) or an annotation dividing the two zones. Simple approach: add a dotted line annotation at the y-position between the last shared param and first unique param.

```javascript
if (sharedSet.size > 0 && sharedSet.size < unionParams.length) {
  // Add subtle divider between shared and unique sections
  const dividerIdx = sharedSet.size - 0.5; // between last shared and first unique
  layout.shapes = [{
    type: "line",
    x0: 0, x1: 1, xref: "paper",
    y0: dividerIdx, y1: dividerIdx, yref: "y",
    line: { color: "#30363d", width: 1, dash: "dot" },
  }];
}
```

**Display name resolution:** Uses `parameter_metadata[paramName]?.display_name || paramName`. When multiple concepts have different metadata for the same param (shouldn't happen, but defensive), use the first non-null display name found.

```javascript
function displayName(paramName, ...metadataSources) {
  for (const meta of metadataSources) {
    if (meta && meta[paramName]?.display_name) {
      return meta[paramName].display_name;
    }
  }
  return paramName;
}
```

For Integrated mode, build a combined metadata lookup from all concepts before rendering.

**Confidence encoding:** In Integrated mode, confidence encoding (opacity/hatch from the existing `tornado.js`) is NOT applied. Reason: the per-concept color + opacity stepping already uses the opacity channel for concept differentiation. Adding confidence opacity on top would create a confusing 2D opacity matrix. Confidence is shown in hover text only.

**Chart height:** `Math.max(300, unionParams.length * 28 + 120)`.

#### Landscape Mode — Per-Concept Tornado

Each landscape cell gets a per-concept tornado chart showing that concept's own top-8:

- **Y-axis**: Parameter display names, sorted by |elasticity| descending
- **X-axis**: Elasticity, synced across all panels (symmetric range)
- **Single concept**: Can use confidence encoding (opacity + hatch) since no concept-color conflict
- **Category colors**: Optional — use `TORNADO_CATEGORY_COLORS` when `parameter_metadata` has category info, fall back to family color otherwise

**Axis synchronization:**
```javascript
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
  return maxAbs > 0 ? maxAbs * 1.1 : 1; // 10% padding
}
```

Applied to Plotly layout: `xaxis.range = [-sharedMax, sharedMax]`.

**Landscape confidence encoding:** Since each panel shows a single concept, the full confidence encoding from `tornado.js` is appropriate:
- High confidence: full opacity
- Medium confidence: 0.8 opacity
- Low confidence: 0.6 opacity + diagonal hatch fill

This directly reuses the pattern from `tornado.js:318-395` (`_buildSolidTrace` / `_buildHatchedTrace`), adapted for the simpler single-concept case.

#### No-Data Handling

```javascript
// No sensitivities at all
if (!concept.data.cost_model?.sensitivities) {
  container.appendChild(el("div", "view-no-data", "No sensitivity data available"));
  return;
}
// Has sensitivities but all zero
const ranked = mergeAndRank(sensitivities, TOP_N);
if (ranked.length === 0) {
  container.appendChild(el("div", "view-no-data", "No sensitivity parameters found"));
  return;
}
```

### Component 3: Script Loading

#### Template Change (`compare.html.j2`)

Add dependency scripts and view scripts:

```html
{% block scripts %}
<script src="/static/js/cas_breakdown.js"></script>
<script src="/static/js/tornado.js"></script>
<script src="/static/js/comparison.js"></script>
<script src="/static/js/view_categorical.js"></script>
<script src="/static/js/view_summary.js"></script>
<script src="/static/js/view_capex.js"></script>
<script src="/static/js/view_sensitivity.js"></script>
{% endblock %}
```

Order: `cas_breakdown.js` and `tornado.js` first (provide global constants) → `comparison.js` (defines `VIEW_REGISTRY`) → view scripts (register renderers).

**Note:** `cas_breakdown.js` and `tornado.js` are currently only loaded on the concept profile page template. Loading them on the compare page adds ~35KB (Plotly is already loaded). They have no side effects — they just declare globals and functions.

#### Registration Pattern

Same IIFE pattern as Item 3a views:

```javascript
// view_capex.js
"use strict";
(function () {
  // Local helpers: el(), append(), FAMILY_COLORS, assignColors(), rgba(), purgeCharts()
  // (duplicated from view_summary.js — module-local scope)

  // Module state
  let showSubAccounts = false;

  // ... render functions ...

  window.VIEW_REGISTRY.capex.renderIntegrated = renderIntegrated;
  window.VIEW_REGISTRY.capex.renderLandscape = renderLandscape;
})();
```

### CSS Additions to `explorer.css`

Minimal additions — most styling comes from Plotly charts and existing `.view-no-data` / `.comparison-table` classes.

```css
/* CapEx view — total cost summary below chart */
.capex-totals {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  font-size: var(--font-size-sm);
}
.capex-totals__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
.capex-totals__value {
  font-family: var(--font-mono);
  font-weight: 600;
}

/* CAS22 expand/collapse toggle */
.capex-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2);
  margin-top: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  background: none;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: color 0.12s, border-color 0.12s;
}
.capex-toggle:hover {
  color: var(--color-text-primary);
  border-color: var(--color-border);
}

/* Sensitivity view — shared/unique section label */
.sensitivity-divider {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  padding: var(--space-1) 0;
}
```

### File Changes Summary

| File | Action | Description |
|------|--------|-------------|
| `view_capex.js` | **New** | CapEx view: grouped CAS bars + CAS22 drill-down, registers on VIEW_REGISTRY |
| `view_sensitivity.js` | **New** | Sensitivity view: tornado charts with union top-8, registers on VIEW_REGISTRY |
| `compare.html.j2` | **Edit** | Add 4 `<script>` tags: `cas_breakdown.js`, `tornado.js`, `view_capex.js`, `view_sensitivity.js` |
| `explorer.css` | **Append** | CSS for capex totals, CAS22 toggle, sensitivity divider |

No changes to `comparison.js`, `cas_breakdown.js`, `tornado.js`, `server.py`, or any existing view files.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Grouped horizontal bar chart with 30 categories (CAS22 expanded) × 3 concepts = very tall chart | Med | Chart height capped at 900px with `overflow-y: auto`. CAS22 expanded is opt-in, so user controls when the chart grows. |
| Union of top-8 across 3 concepts could yield 24 parameters — visually dense tornado | Med | 8 is already conservative (down from tornado.js default of 15). Sort by shared-first keeps most informative params at top. |
| Global constants from `cas_breakdown.js` / `tornado.js` loaded on compare page even when CapEx/Sensitivity not selected | Low | ~35KB combined, no runtime cost until charts render. Already loading Plotly (~1.2MB). |
| `_hexToRgba` naming collision between `cas_breakdown.js` and `tornado.js` (both define global `_hexToRgba`) | Med | Both implementations are identical. Second declaration silently overwrites first — no bug, but worth noting. The view files use their own local `rgba()` inside the IIFE. |
| Plotly memory leaks from rapid view switching | Low | `purgeCharts()` called at start of each render (same pattern as `view_summary.js:444-449`). |

## Integration Strategy

**With comparison shell (Item 2):** Zero-touch. Views register on `VIEW_REGISTRY`; shell dispatches to them.

**With existing charts:** `cas_breakdown.js` and `tornado.js` are loaded for their global constants only. Their render functions (`renderCASBreakdown`, `renderTornado`) are not called — the view files implement their own rendering for comparison mode.

**With Item 3a views:** No interaction. Each view is self-contained.

**With concept profile page:** No impact. `cas_breakdown.js` and `tornado.js` continue to work as before on the concept page. The new view files are only loaded on the compare page.

## Validation Approach

**Manual testing checklist:**

1. **CapEx Integrated:** Select 2-3 concepts → grouped horizontal bars, one group per CAS account, concepts side-by-side
2. **CapEx Landscape:** Switch to Landscape → per-concept bar charts with synced x-axis scale
3. **CapEx CAS22 toggle:** Click "Expand CAS22 Detail" → 14 sub-accounts replace CAS22 aggregate in both modes
4. **CapEx overridden:** Verify hover text shows "★ overridden" for overridden accounts
5. **CapEx no cost model:** Include concept without cost model → placeholder, no JS errors
6. **Sensitivity Integrated:** Select 2-3 concepts → grouped tornado, shared params at top, divider, unique below
7. **Sensitivity Landscape:** Switch to Landscape → per-concept top-8 tornado with synced axis, confidence encoding
8. **Sensitivity no data:** Include concept without sensitivities → placeholder, no JS errors
9. **Sensitivity mixed:** 2 concepts with sensitivities + 1 without → renders what's available
10. **View switching:** Rapidly toggle CapEx ↔ Sensitivity ↔ Summary ↔ Categorical — no stale DOM, no Plotly leaks
11. **URL persistence:** Select CapEx in left panel → refresh → CapEx still selected
12. **Regression:** Concept profile page CAS chart + tornado → unchanged behavior

---

**Next Step:** After approval → `/_my_plan`
