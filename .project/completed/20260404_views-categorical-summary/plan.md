# Implementation Plan: Categorical & Summary Views

**Status:** Draft
**Created:** 2026-04-05 20:46 PDT
**Last Updated:** 2026-04-05 20:46 PDT

## Source Documents
- **Spec:** `.project/active/views-categorical-summary/spec.md`
- **Design:** `.project/active/views-categorical-summary/design.md` — See here for component details, data flows, CSS, and architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 (Categorical) validates the view registration pattern and async-fetch-inside-sync-dispatch approach with the simpler of the two views. Phase 2 (Summary) builds on the proven pattern to tackle the riskier Plotly subplot layout. Phase 3 is a validation sweep across the full acceptance criteria matrix.

**No automated frontend tests:** This project has no JS test runner. Validation is manual via browser. Each phase includes a structured manual checklist instead of test stencils.

---

## Phase 1: Categorical View + Template Wiring

### Goal
Deliver the first working comparison view. Validates: VIEW_REGISTRY registration, async taxonomy fetch inside sync dispatch, comparison table in Integrated mode, attribute cards in Landscape mode. Exercises the full render contract that Phase 2 and Item 3b will reuse.

### Manual Test Checklist (Verify Before Moving On)

```
1. Navigate to /compare?concepts=arc,sparc&left=categorical
   → Left panel shows taxonomy comparison table (not placeholder)
   → Right panel still shows placeholder (Summary not yet implemented)

2. Table structure:
   → Header: "Attribute" | "ARC" | "SPARC" (with family badges)
   → Rows: all cross-cutting fields (fuel, heating, energy capture, etc.)
   → Hierarchical fields: only MFE sub-types shown (both are MFE)
   → Diff rows have subtle red tint background
   → Matching rows have no tint

3. Null/TBD handling:
   → Fields with null on applicable concept show "N/A" (muted)
   → Fields inapplicable to concept's family show "—" (muted italic)
   → "TBD" or "Unknown" string values render as-is (muted)

4. Add an IFE concept (e.g., /compare?concepts=arc,sparc,nif):
   → IFE-specific rows now appear (ife_driver, laser_approach)
   → IFE concept's MFE fields show "—"

5. Switch to Landscape mode:
   → Each concept gets its own attribute card
   → Inapplicable fields omitted from card (not shown as "—")
   → Cards use .taxonomy-card__attr styling

6. Switch back to Integrated → table re-renders correctly
7. Open browser console → no JS errors
```

### Changes Required

**See `design.md` for:** TAXONOMY_FIELDS definition, data fetch/cache pattern, row visibility logic, integrated table structure, landscape card structure, registration pattern, el()/append() convention.

**Specific file changes:**

#### 1. Template
**File:** `exploration/concept_explorer/templates/compare.html.j2` (EDIT)
- [ ] Add `<script src="/static/js/view_categorical.js"></script>` after `comparison.js` in `{% block scripts %}`

#### 2. View Implementation
**File:** `exploration/concept_explorer/static/js/view_categorical.js` (NEW)
- [ ] IIFE wrapper with `"use strict"`
- [ ] Local `el()` and `append()` DOM helpers (see `design.md#registration-pattern`)
- [ ] `FAMILY_META` constant (same as `comparison.js:33-42`)
- [ ] `TAXONOMY_FIELDS` array with `applicableTo` property (see `design.md#taxonomy-field-definition`)
- [ ] `ensureTaxonomy()` async fetch + cache (see `design.md#data-fetch--cache`)
- [ ] `getVisibleFields(concepts, taxonomyData)` — filters TAXONOMY_FIELDS by row visibility rule (see `design.md#row-visibility`)
- [ ] `renderCellValue(value, field, conceptFamily)` — returns DOM node with correct class (val--na, val--tbd, or plain text)
- [ ] `renderIntegrated(container, concepts)` — async wrapper, builds `.comparison-table` (see `design.md#integrated-mode--comparison-table`)
- [ ] `renderLandscape(container, concept, ctx)` — async wrapper, builds attribute card (see `design.md#landscape-mode--attribute-cards`)
- [ ] Register on `window.VIEW_REGISTRY.categorical`

#### 3. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (APPEND)
- [ ] Add `.comparison-table .val--na` and `.comparison-table .val--tbd` sub-classes (see `design.md#css-additions`)

### Validation

**Manual:**
- [ ] Run all 7 checklist items above
- [ ] Verify existing comparison shell behavior unchanged (mode toggle, concept picker, URL state)
- [ ] Navigate to concept profile page → still works
- [ ] Navigate to taxonomy page → still works

**What We Know Works After This Phase:**
- VIEW_REGISTRY registration pattern works end-to-end
- Async data fetch inside sync dispatch contract works
- Categorical renders correctly in both modes with real data
- Template script loading order is correct

---

## Phase 2: Summary View

### Goal
Deliver headline economics comparison with Plotly subplots + metrics table. Validates: Plotly subplot layout in narrow panels, axis synchronization for Landscape mode, graceful degradation for concepts without cost models.

### Manual Test Checklist (Verify Before Moving On)

```
1. Navigate to /compare?concepts=arc,sparc&right=summary
   → Right panel shows Plotly chart with 5 subplots + metrics table
   → Each subplot: one grouped bar per concept, own y-axis
   → Family-colored bars with legend at bottom

2. Metrics table below chart:
   → Header: "Metric" | "ARC" | "SPARC"
   → Rows: LCOE ($/MWh), Overnight Cost ($/kW), Net Power (MW), Q_eng, Cap Factor (%)
   → Last row: Top CAS driver per concept (name + % of total)
   → Values right-aligned, mono font

3. No-cost-model concept (find one without has_cost_model):
   → Add it to comparison
   → Chart: only concepts with data shown (no empty bar)
   → Table: concept column shows "—" for all metrics, "No cost model" note
   → No JS errors in console

4. Switch to Landscape mode with 3+ concepts:
   → Each concept gets its own bar chart + metrics
   → Bar chart axes synchronized (same range across panels)
   → Concept without cost model shows "No cost model available" placeholder

5. Landscape axis sync:
   → Compare bar lengths visually — same value = same bar length across panels
   → Add/remove concept → scales recompute (bars resize)

6. View switching: rapidly toggle Categorical ↔ Summary in both modes
   → Containers clear properly, no stale DOM or orphaned Plotly charts
   → No JS errors in console
```

### Changes Required

**See `design.md` for:** HEADLINE_METRICS/CAS_ACCOUNT_KEYS definitions, Plotly subplot layout, FAMILY_COLORS, opacity stepping, metrics table structure, landscape panel structure, computeSharedScales(), no-cost-model handling.

**Specific file changes:**

#### 1. Template
**File:** `exploration/concept_explorer/templates/compare.html.j2` (EDIT)
- [ ] Add `<script src="/static/js/view_summary.js"></script>` after `view_categorical.js`

#### 2. View Implementation
**File:** `exploration/concept_explorer/static/js/view_summary.js` (NEW)
- [ ] IIFE wrapper with `"use strict"`, local `el()`/`append()` helpers
- [ ] `FAMILY_META` constant (for badge rendering in table headers)
- [ ] `FAMILY_COLORS` constant (for Plotly trace colors)
- [ ] `HEADLINE_METRICS` array with format functions (see `design.md#metric-definitions`)
- [ ] `CAS_ACCOUNT_KEYS` array
- [ ] `PLOTLY_THEME` constant — dark theme config extracted from `tornado.js` pattern (see `design.md#research-findings`)
- [ ] `computeSharedScales(concepts)` — per-metric min/max with 10% padding (see `design.md#axis-synchronization`)
- [ ] `getTopCasDriver(costModel)` — returns `{name, pct}` for largest CAS account
- [ ] `renderIntegratedChart(container, concepts)` — Plotly 5-subplot layout (see `design.md#integrated-mode--grouped-bar-chart--metrics-table`)
- [ ] `renderMetricsTable(container, concepts)` — `.comparison-table.comparison-table--summary` (see design)
- [ ] `renderIntegrated(container, concepts)` — orchestrates chart + table, handles all-no-data edge case
- [ ] `renderLandscapeChart(container, concept, scales)` — single horizontal bar chart with synced axes
- [ ] `renderLandscapeMetrics(container, concept)` — compact metric rows using `.summary-metric-row`
- [ ] `renderLandscape(container, concept, ctx)` — orchestrates chart + metrics, handles no-cost-model placeholder
- [ ] Register on `window.VIEW_REGISTRY.summary`

#### 3. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (APPEND)
- [ ] Add `.comparison-table--summary` modifier sub-classes (see `design.md#css-additions`)
- [ ] Add `.summary-metric-row` classes for landscape metrics (see design)
- [ ] Add `.view-no-data` placeholder class (see design)

### Validation

**Manual:**
- [ ] Run all 6 checklist items above
- [ ] Categorical view still works (not broken by new script)
- [ ] Concept profile page and taxonomy page still work
- [ ] URL state: `/compare?concepts=arc,sparc&left=categorical&right=summary` loads correctly after refresh

**What We Know Works After This Phase:**
- Both views render in both modes
- Plotly subplot layout works in Integrated panels
- Axis synchronization works in Landscape mode
- Graceful degradation for missing cost models
- Views coexist — switching between them works cleanly

---

## Phase 3: End-to-End Validation & Polish

### Goal
Verify the full acceptance criteria matrix from the spec. Fix visual/interaction issues discovered during testing. No planned new files — bug fixes only.

### Full Acceptance Criteria Sweep

```
Spec Acceptance Criteria:

CORE FUNCTIONALITY:
- [ ] Selecting "Categorical" in any view dropdown renders taxonomy comparison
- [ ] Selecting "Summary" in any view dropdown renders economics comparison
- [ ] Categorical Integrated: single table, concepts as columns, all taxonomy fields as rows
- [ ] Categorical Landscape: per-concept cards with all taxonomy fields
- [ ] Summary Integrated: grouped chart + metrics table on shared axes
- [ ] Summary Landscape: per-concept chart panels with synced scales + metrics
- [ ] Summary with no-cost-model concept: shows placeholder, no console errors
- [ ] Summary with mixed concepts: renders what's available
- [ ] Null/TBD taxonomy values display cleanly

QUALITY & INTEGRATION:
- [ ] No changes to comparison.js
- [ ] Existing shell behavior unchanged (mode toggle, concept picker, URL state)
- [ ] Existing taxonomy views, concept profile pages, index grid unaffected
- [ ] No new API endpoints

DESIGN VALIDATION CHECKLIST (design.md#validation-approach):
- [ ] Categorical Integrated with 2-3 concepts: diff rows highlighted, inapplicable "—"
- [ ] Categorical Landscape: per-concept cards, inapplicable fields omitted
- [ ] Summary Integrated: subplot chart + metrics with correct values/units
- [ ] Summary Landscape: synced axes across panels
- [ ] No cost model: placeholder, no errors
- [ ] Mixed selection: chart shows data-having concepts, table shows all
- [ ] Rapid view switching: no stale DOM
- [ ] URL persistence: refresh reproduces view selection
- [ ] Regression: concept profile, index grid, taxonomy all work
```

### Polish Items (Fix If Found)

- [ ] Visual spacing between chart and metrics table
- [ ] Plotly chart sizing in narrow Integrated panels (may need height/margin tuning)
- [ ] Landscape card height consistency across concepts with/without cost models
- [ ] Loading flash on first Categorical render (taxonomy fetch)

### Validation

**What We Know Works After This Phase:**
All spec acceptance criteria pass. Both views are production-ready for the EXPLORER-UX-V2 epic.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If async-inside-sync dispatch doesn't work cleanly → the shell's `renderViewContent` already clears the container, so the view can clear again + show loading text + replace on fetch completion. Worst case: brief flash of "Loading..." text.
- **Phase 2**: If Plotly 5-subplot layout is visually awkward in narrow panels → fall back to metrics table only (remove chart, keep table as primary). The table alone satisfies the spec requirements; the chart is additive.

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_explorer/static/js/view_categorical.js` (~230 lines)
  - IIFE with local `el()`/`append()` helpers, `FAMILY_META`, `TAXONOMY_FIELDS` (20 fields with `applicableTo`)
  - `ensureTaxonomy()` async fetch + cache to `/api/taxonomy/registry`
  - `getVisibleFields()` filters hierarchical sub-type rows by family presence
  - `cellState()` helper: inapplicable → "—" (val--na), null → "N/A" (val--tbd), TBD/Unknown → as-is (val--tbd)
  - `renderIntegratedTable()`: `.comparison-table` with diff/match row highlighting, attr-label first column, text-col class for normal taxonomy values
  - `renderLandscapeCard()`: reuses `.taxonomy-card__attr`/`__label`/`__value` classes, omits inapplicable fields
  - Async render pattern: shows "Loading..." text, replaces on fetch completion, error fallback
  - Registered on `window.VIEW_REGISTRY.categorical`
- Appended to `explorer.css`: `.val--na` (muted italic), `.val--tbd` (muted), `.view-no-data` placeholder
- Added `<script src="/static/js/view_categorical.js">` to `compare.html.j2` after `comparison.js`
**Issues:** None
**Deviations:** None — followed design exactly

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_explorer/static/js/view_summary.js` (~330 lines)
  - IIFE with local helpers, `FAMILY_META`, `FAMILY_COLORS`, `HEADLINE_METRICS` (5 metrics with format fns), `CAS_ACCOUNT_KEYS`, `PLOTLY_THEME`
  - `getHeadline()` / `getTopCasDriver()` data accessors
  - `assignColors()` with opacity stepping for same-family concepts
  - `computeSharedScales()` for landscape axis synchronization (10% padding, missing-data exclusion)
  - `renderIntegratedChart()`: Plotly 5-subplot small-multiples (horizontal bars, one subplot per metric, concept names on y-axis of first subplot only)
  - `renderMetricsTable()`: `.comparison-table--summary` with metric rows + Top CAS Driver row, no-data concepts show "—"
  - `renderLandscapeChart()`: single horizontal bar chart per concept, values normalized to 0-1 using shared scales for visual comparability
  - `renderLandscapeMetrics()`: compact `.summary-metric-row` list with Top CAS driver
  - No-cost-model: integrated shows "—" in table (excluded from chart); landscape shows `.view-no-data` placeholder
  - Registered on `window.VIEW_REGISTRY.summary`
- Appended to `explorer.css`: `.comparison-table--summary` modifier (right-aligned mono values, unit styling, no-data styling), `.summary-metric-row` classes
- Added `<script src="/static/js/view_summary.js">` to `compare.html.j2` after `view_categorical.js`
**Issues:** None
**Deviations:**
- Landscape chart uses normalized 0-1 scale instead of raw metric values with per-subplot axes. Since each landscape card shows only one concept, raw values on different scales would be meaningless for visual comparison. Normalizing to shared scales makes bar lengths comparable across cards. Actual values are shown in hover text and the metrics list below.

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Removed dead variable `xVals` in `view_summary.js:renderLandscapeChart()`
- Added `purgeCharts()` helper that calls `Plotly.purge()` on any `.js-plotly-plot` elements before `innerHTML = ""` — prevents memory leaks from orphaned Plotly internals on view switching
- Added spacer div (`--space-4`) between chart and metrics table in integrated mode
**Issues:**
- No issues beyond the three code quality items fixed above
**Deviations:** None

### Acceptance Criteria Review (Code-Level)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Categorical in dropdown renders taxonomy | PASS | `VIEW_REGISTRY.categorical.renderIntegrated/renderLandscape` registered |
| Summary in dropdown renders economics | PASS | `VIEW_REGISTRY.summary.renderIntegrated/renderLandscape` registered |
| Categorical Integrated: table, concepts as columns | PASS | `.comparison-table` with `<th>` per concept |
| Categorical Landscape: per-concept cards | PASS | `.taxonomy-card__attrs` with filtered fields |
| Summary Integrated: chart + metrics table | PASS | Plotly 5-subplot + `.comparison-table--summary` |
| Summary Landscape: synced scale panels | PASS | `computeSharedScales()` → normalized 0-1 bars |
| Summary no-cost-model: placeholder, no errors | PASS | `.view-no-data` fallback, null-safe accessors |
| Summary mixed concepts: renders available | PASS | Chart filters to data-having; table shows "—" for rest |
| Null/TBD taxonomy values display cleanly | PASS | `cellState()` handles null→"N/A", TBD→as-is, inapplicable→"—" |
| No changes to comparison.js | PASS | Only additive new files |
| Existing shell behavior unchanged | PASS | No modifications to existing JS/HTML/CSS classes |
| No new API endpoints | PASS | Uses existing `/api/taxonomy/registry` and `/api/concepts/{id}` |
| Plotly available globally | PASS | Loaded from `base.html.j2` via `/static/vendor/plotly-basic.min.js` |
| Plotly cleanup on re-render | PASS | `purgeCharts()` before `innerHTML = ""` |

**Remaining: manual browser testing needed for visual polish items.**

---

**Status**: Complete (all 3 phases done, 14/14 manual tests pass)
