# Design: Comparison Page Shell — Routing, Modes & Layout

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 18:56 PDT
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer
**Epic:** EXPLORER-UX-V2, Item 2

## Overview

Rewrite the `/compare` page to support two comparison modes (Integrated and Landscape) with URL-driven state, a lightweight concept picker, and a view rendering contract that Items 3a/3b plug into. The existing `comparison.js` is replaced; `fetchManifest`, `fetchConcept`, and `conceptCache` carry over.

## Related Artifacts

- **Spec:** `.project/active/compare-shell/spec.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 2)
- **Selection tray:** `exploration/concept_explorer/static/js/selection_tray.js`
- **Current comparison.js:** `exploration/concept_explorer/static/js/comparison.js`
- **Current template:** `exploration/concept_explorer/templates/compare.html.j2`

## Research Findings

### Files Analyzed

| File | Key Takeaways |
|------|--------------|
| `comparison.js` (832 lines) | `fetchManifest()` (:110), `fetchConcept()` (:120), `conceptCache` (:28) — reusable. `FAMILY_META` (:45) for badge rendering. Picker, tabs, and render functions — replaced. |
| `selection_tray.js` (360 lines) | Navigates via `window.location.href = "/compare?mode={mode}&concepts=id1,id2,..."` (:328). Constants: `MAX_INTEGRATED=3`, `MAX_LANDSCAPE=6` (:24-27). Chip rendering pattern reusable for concept bar. |
| `compare.html.j2` | Current DOM: `#selector-area` → `#tabs-section` with 3 tab panels. Scripts load `tornado.js`, `cas_breakdown.js`, `comparison.js`. |
| `base.html.j2` | Nav has `/compare` link with `active_nav` class toggle. Plotly vendored globally. Page content in `{% block body %}`. |
| `explorer.css` | Design tokens (:1-30), `.comparison-chip` (:959), `.comparison-add-btn` (:986), `.tabs/.tab-btn` (:1002-1037), `.card` (:221), `.btn/.btn--primary/.btn--ghost` (:1072-1113). All reusable. |
| `taxonomy.js` | Initializes tray with `SelectionTray.init(document.querySelector("main"), _registry)` (:112). `onChange` callback pattern (:114-121). |
| `server.py` | `/compare` route (:481-482) serves pre-rendered HTML from `dist/`. `/api/manifest` (:355), `/api/concepts/{id}` (:359). No route changes needed — just template swap. |

### Reusable Patterns

- **Family badge rendering**: `FAMILY_META` lookup → `<span class="badge badge-{family}">` — used everywhere, carry over
- **Concept chip**: `.comparison-chip` with `.comparison-chip__remove` — reuse CSS class for concept bar
- **Button styles**: `.btn`, `.btn--primary`, `.btn--ghost` — use for mode toggle and picker
- **Card container**: `.card` class — use for panels
- **Fetch + cache**: `fetchManifest()` / `fetchConcept()` / `conceptCache` pattern — carry over verbatim
- **Server state sync**: `postState()` (:97-108) POSTs `ExplorerState` with `comparison_set` to `/api/state`. The concept profile page reads `ExplorerState` for slider overrides. Keep `postState()` and call it on concept add/remove to maintain `comparison_set` parity. Other fields (`current_concept_id`, `slider_overrides`) passed as-is (empty/null from compare page).

### Selection Tray URL Contract

The tray (Item 1) navigates to `/compare` with this exact format:
```
/compare?mode=integrated&concepts=arc,sparc,iter
/compare?mode=landscape&concepts=arc,sparc,iter,demo,cfr,aries
```
The comparison page must parse this format. The `mode` param may be absent (auto-select). The `concepts` param is a comma-separated list of concept IDs.

## Design Decision: View State in URL

**Context:** The spec flagged whether URL should encode selected views (e.g., `&left=summary&right=capex`) for shareability.

**Decision: Yes — encode view selections in URL.**

Rationale:
- Adds 2 params (`left`, `right` for Integrated; `view` for Landscape) — trivial complexity
- Makes shared URLs reproduce exactly what the sender was looking at
- Without it, every shared link opens to defaults (Categorical + Summary) regardless of what the sender had selected
- Consistent with the existing `?selected=...` URL sync pattern on taxonomy

**URL format (complete):**
```
# Integrated
/compare?mode=integrated&concepts=arc,sparc&left=categorical&right=summary

# Landscape  
/compare?mode=landscape&concepts=arc,sparc,iter,demo&view=categorical

# Minimal (defaults applied)
/compare?concepts=arc,sparc
```

Valid view values: `categorical`, `summary`, `capex`, `sensitivity`

## Proposed Design

### Architecture Overview

```
compare.html.j2 (template)
  ├─ Header: title + concept bar (chips + picker toggle)
  ├─ Mode toggle bar
  ├─ #compare-integrated (two-panel layout)
  │   ├─ Panel Left: view selector + content area
  │   └─ Panel Right: view selector + content area
  └─ #compare-landscape (grid layout)
      ├─ View selector (single)
      └─ Concept grid (responsive)

comparison.js (rewritten controller)
  ├─ State: concepts[], mode, viewLeft, viewRight, viewLandscape
  ├─ URL ↔ State sync (parse on load, replaceState on change)
  ├─ Data: fetchManifest(), fetchConcept(), conceptCache (carried over)
  ├─ Concept picker (add/remove on compare page)
  ├─ Mode toggle logic (auto-select, manual, constraints)
  ├─ Layout rendering (integrated vs landscape)
  └─ View dispatch → VIEW_REGISTRY[viewName].render*(container, concepts)

VIEW_REGISTRY (rendering contract for Items 3a/3b)
  ├─ categorical: { renderIntegrated, renderLandscape }
  ├─ summary:     { renderIntegrated, renderLandscape }
  ├─ capex:       { renderIntegrated, renderLandscape }
  └─ sensitivity: { renderIntegrated, renderLandscape }
```

### Component 1: URL State Manager

Centralized URL ↔ state synchronization. All state changes flow through this.

**JS convention:** The rewrite uses `const` for constants and never-reassigned bindings, `let` for mutable state. No `var`. This matches the `let`/`const` style in the existing `comparison.js` (lines 25-37) and `selection_tray.js`.

**State shape:**
```javascript
let _state = {
    concepts: [],          // Ordered concept IDs (validated against manifest)
    mode: "integrated",    // "integrated" | "landscape"
    left: "categorical",   // View for integrated left panel
    right: "summary",      // View for integrated right panel
    view: "categorical"    // View for landscape mode
};
```

**Functions:**

`parseUrl()` → Reads `URLSearchParams` from `window.location.search`. Returns state object with defaults applied:
- `concepts`: split on comma, filter empty strings
- `mode`: if present and valid, use it; else auto-select per FR-4
- `left`/`right`/`view`: if present and valid view name, use it; else defaults (categorical/summary/categorical)

`syncUrl(state)` → Builds query string from state, calls `history.replaceState`. Only includes non-default values to keep URLs clean:
- Always includes `concepts` (if any)
- Always includes `mode`  
- Includes `left`/`right` only if not the defaults (categorical/summary)
- Includes `view` only if not the default (categorical)

`validateAndCorrect(state, manifest)` → Applies FR-5/FR-6 corrections:
- Filter `concepts` to those present in manifest (skip invalid, collect warnings)
- If `mode === "integrated"` and `concepts.length > MAX_INTEGRATED`: correct to `"landscape"`
- Returns `{ state, warnings }` where warnings is an array of strings

**popstate listener:** On browser back/forward, call `parseUrl()` → `validateAndCorrect()` → `render()`.

### Component 2: Concept Bar & Picker (FR-20–22)

Replaces the current `#selector-area` with a concept bar that shows selected concepts as chips and provides inline add/remove.

**Concept bar** (always visible in page header):
- Renders one `.comparison-chip` per selected concept (reuses existing CSS)
- Each chip: family badge + concept name + `×` remove button
- `+` button at the end opens the picker
- Remove updates state → `syncUrl()` → `postState()` → re-evaluates mode → re-renders

**Concept picker** (toggleable inline panel, same pattern as current):
- Opens below concept bar as a `.card` dropdown
- Lists all manifest concepts not currently selected
- Each row: concept name, family badge, company info (same as current `renderPickerList`)
- Click adds concept → state update → URL sync → `postState()` → re-render
- Click-outside or Esc closes
- Shows count: "N of 6 selected". Picker disables adding when count reaches `MAX_LANDSCAPE` (6) — hides the `+` button and shows "Maximum concepts selected" in picker if opened via keyboard

**Mode re-evaluation on add/remove:**
- After adding: if count > MAX_INTEGRATED and mode is integrated → auto-switch to landscape
- After removing: if count ≤ MAX_INTEGRATED → keep current mode (don't force switch back)
- Update mode toggle button states

### Component 3: Mode Toggle (FR-4–6)

Two-button toggle bar below the concept bar. Uses `.btn` styling.

```
[ Integrated (2) ]  [ Landscape (2) ]
     ↑ active           ↑ available
```

**Behavior:**
- Active mode gets `.btn--primary` styling; other gets `.btn--ghost`
- Integrated button: disabled (`.btn[disabled]`) when `concepts.length > MAX_INTEGRATED`
- Landscape button: always enabled (when concepts exist)
- Both disabled when 0 concepts
- Click on available mode: update `_state.mode` → `syncUrl()` → re-render layout
- Label shows concept count in parentheses for context

### Component 4: Integrated Layout (FR-7–10)

Two side-by-side panels using CSS Grid.

**CSS:**
```css
.compare-integrated {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
}
```

**Each panel** (`.compare-panel`):
- Header: view selector `<select>` dropdown
- Content area: `<div class="compare-panel__content">` — rendering target

**View selector dropdowns:**
- Four `<option>` values: Categorical, Summary, CapEx, Sensitivity
- Left panel defaults to `categorical`, right to `summary`
- **Mutual exclusion (FR-8):** When left changes, disable that option in right's dropdown (and vice versa). Implementation: on change, set `disabled` attribute on the matching `<option>` in the sibling dropdown. The previously-disabled option becomes enabled.
- On change: update `_state.left` or `_state.right` → `syncUrl()` → re-render that panel only

**Placeholder rendering** (until Items 3a/3b):
- Each panel shows a `.card` with: view name as heading, list of concept names with family badges
- Confirms correct data routing per FR-16

### Component 5: Landscape Layout (FR-11–13)

Single view selector at top, responsive concept grid below.

**View selector:** Same `<select>` dropdown as integrated panels, but single instance. No mutual exclusion needed. Defaults to `categorical`.

**Grid CSS:**
```css
.compare-landscape-grid {
    display: grid;
    gap: var(--space-4);
}
.compare-landscape-grid--1up {
    grid-template-columns: 1fr;
    max-width: 50%;
}
.compare-landscape-grid--2up {
    grid-template-columns: repeat(2, 1fr);
}
.compare-landscape-grid--3up {
    grid-template-columns: repeat(3, 1fr);
}
```

Grid class selection: `concepts.length <= 3` → `--2up`, else `--3up` (FR-12).

**Edge case — 1 concept in Landscape:** A single card in a 2-column grid looks odd. When `concepts.length === 1`, use `--1up` (single full-width column). This can happen when a user manually toggles to Landscape with 1 concept, or removes concepts down to 1 while in Landscape mode.

**Each concept cell** (`.compare-landscape-cell`):
- Header: concept name + family badge
- Content area: `<div class="compare-landscape-cell__content">` — rendering target

**Placeholder rendering:** Each cell shows concept name, ID, and selected view name in a `.card`.

### Component 6: View Rendering Contract

This is the integration point for Items 3a/3b. The shell defines the contract; placeholder implementations satisfy it now.

**Registry pattern:**
```javascript
const VIEW_REGISTRY = {
    categorical: { label: "Categorical", renderIntegrated: null, renderLandscape: null },
    summary:     { label: "Summary",     renderIntegrated: null, renderLandscape: null },
    capex:       { label: "CapEx",       renderIntegrated: null, renderLandscape: null },
    sensitivity: { label: "Sensitivity", renderIntegrated: null, renderLandscape: null }
};
```

**Render function signatures:**
```javascript
// Integrated: renders into one panel with all selected concepts
renderIntegrated(container, conceptDataArray)
// container: DOM element (.compare-panel__content)
// conceptDataArray: Array of {concept_id, name, confinement_family, data: ConceptData}

// Landscape: renders into one cell for one concept  
renderLandscape(container, conceptData, syncContext)
// container: DOM element (.compare-landscape-cell__content)
// conceptData: {concept_id, name, confinement_family, data: ConceptData}
// syncContext: {allConcepts, sharedScales} for axis synchronization
```

**Registration by Items 3a/3b:**
```javascript
// In view_categorical.js:
VIEW_REGISTRY.categorical.renderIntegrated = function(container, concepts) { ... };
VIEW_REGISTRY.categorical.renderLandscape = function(container, concept, ctx) { ... };
```

**Shell dispatch logic:**
```javascript
function renderPanel(container, viewName, concepts) {
    container.innerHTML = "";
    var view = VIEW_REGISTRY[viewName];
    if (view.renderIntegrated) {
        view.renderIntegrated(container, concepts);
    } else {
        renderPlaceholder(container, viewName, concepts);
    }
}
```

Items 3a/3b just set the function references on `VIEW_REGISTRY` — no changes to the shell needed.

### Component 7: Page Lifecycle

**`init()` sequence:**
1. Show loading state
2. `fetchManifest()` — if fails, show error state
3. Parse URL → `validateAndCorrect()` against manifest
4. If warnings (invalid IDs, mode correction): show transient warning banner
5. Fetch concept data for all valid IDs (parallel `Promise.all`)
6. `syncUrl()` (writes corrected state back to URL)
7. `postState()` (sync `comparison_set` to server — fire-and-forget)
8. Render concept bar, mode toggle, active layout
9. Hide loading state

**Re-render triggers** (all partial — only affected areas update):
- Concept added/removed → re-render concept bar + mode toggle + active layout
- Mode changed → re-render mode toggle + swap layout (integrated ↔ landscape)
- View selector changed → re-render affected panel(s) only

### Template Structure (`compare.html.j2`)

```html
{% extends "base.html.j2" %}
{% block body %}
<div id="app" class="page-content page-content--wide">

  <div id="loading-state" class="loading-state">Loading comparison...</div>
  <div id="error-state" class="error-state" style="display:none"></div>
  <div id="warning-banner" class="warning-banner" style="display:none"></div>

  <div id="compare-content" style="display:none">
    <!-- Header -->
    <header class="compare-header">
      <h1>Compare Concepts</h1>
    </header>

    <!-- Concept bar -->
    <div id="concept-bar" class="comparison-selector"></div>

    <!-- Concept picker dropdown -->
    <div id="concept-picker" class="card" style="display:none" role="listbox">
      <div class="picker-header">
        <span>Select a concept to add</span>
        <button id="close-picker" class="btn btn--ghost">×</button>
      </div>
      <div id="picker-list" class="picker-list"></div>
    </div>

    <!-- Empty state -->
    <div id="empty-state" class="compare-empty" style="display:none">
      <p>Select concepts on the <a href="/taxonomy">Taxonomy</a> page,
         or use the <strong>+ Add concept</strong> button above.</p>
    </div>

    <!-- Mode toggle -->
    <div id="mode-toggle" class="mode-toggle" style="display:none">
      <button id="mode-integrated" class="btn btn--primary" data-mode="integrated">
        Integrated
      </button>
      <button id="mode-landscape" class="btn btn--ghost" data-mode="landscape">
        Landscape
      </button>
    </div>

    <!-- Integrated layout -->
    <div id="compare-integrated" class="compare-integrated" style="display:none">
      <div class="compare-panel" id="panel-left">
        <div class="compare-panel__header">
          <select id="select-left" class="compare-view-select"></select>
        </div>
        <div class="compare-panel__content" id="content-left"></div>
      </div>
      <div class="compare-panel" id="panel-right">
        <div class="compare-panel__header">
          <select id="select-right" class="compare-view-select"></select>
        </div>
        <div class="compare-panel__content" id="content-right"></div>
      </div>
    </div>

    <!-- Landscape layout -->
    <div id="compare-landscape" style="display:none">
      <div class="compare-landscape__header">
        <select id="select-landscape" class="compare-view-select"></select>
      </div>
      <div id="landscape-grid" class="compare-landscape-grid"></div>
    </div>

  </div>
</div>
{% endblock %}

{% block scripts %}
<script src="/static/js/comparison.js"></script>
{% endblock %}
```

Note: `tornado.js` and `cas_breakdown.js` are no longer loaded on the compare page. Items 3a/3b will add their own script tags when ready.

### CSS Additions to `explorer.css`

```css
/* Mode toggle */
.mode-toggle {
    display: flex;
    gap: var(--space-2);
    margin-bottom: var(--space-6);
}

/* Integrated: two-panel grid */
.compare-integrated {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
}

/* Panel */
.compare-panel {
    display: flex;
    flex-direction: column;
    min-height: 400px;
}
.compare-panel__header {
    display: flex;
    align-items: center;
    margin-bottom: var(--space-3);
}
.compare-panel__content {
    flex: 1;
}

/* View selector dropdown */
.compare-view-select {
    padding: var(--space-1) var(--space-3);
    background-color: var(--color-surface-2);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    color: var(--color-text-primary);
    font-size: var(--font-size-sm);
    font-family: var(--font-sans);
    cursor: pointer;
}
.compare-view-select option:disabled {
    color: var(--color-text-muted);
}

/* Landscape: header + grid */
.compare-landscape__header {
    margin-bottom: var(--space-4);
}
.compare-landscape-grid {
    display: grid;
    gap: var(--space-4);
}
.compare-landscape-grid--1up {
    grid-template-columns: 1fr;
    max-width: 50%;
}
.compare-landscape-grid--2up {
    grid-template-columns: repeat(2, 1fr);
}
.compare-landscape-grid--3up {
    grid-template-columns: repeat(3, 1fr);
}

/* Landscape cell */
.compare-landscape-cell {
    background-color: var(--color-surface-1);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-4);
}
.compare-landscape-cell__header {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    margin-bottom: var(--space-3);
    font-size: var(--font-size-md);
    font-weight: 600;
}
.compare-landscape-cell__content {
    min-height: 200px;
}

/* Warning banner */
.warning-banner {
    background-color: rgba(234, 179, 8, 0.1);
    border: 1px solid rgba(234, 179, 8, 0.3);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-4);
    margin-bottom: var(--space-4);
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
}

/* Empty state */
.compare-empty {
    text-align: center;
    padding: var(--space-12) var(--space-6);
    color: var(--color-text-muted);
}
.compare-empty a {
    color: var(--color-well-established);
}

/* Placeholder card (temporary until Items 3a/3b) */
.compare-placeholder {
    background-color: var(--color-surface-2);
    border: 1px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-6);
    text-align: center;
    color: var(--color-text-muted);
    font-size: var(--font-size-sm);
    min-height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-3);
}
```

### Existing CSS Retained

The following existing classes carry over unchanged:
- `.comparison-chip`, `.comparison-chip__remove` — for concept bar chips
- `.comparison-selector` — for concept bar container (flex, wrap, gap)
- `.comparison-add-btn` — for the `+` button
- `.btn`, `.btn--primary`, `.btn--ghost` — for mode toggle buttons
- `.card` — for picker dropdown
- `.badge`, `.badge-mfe`, `.badge-ife`, etc. — for family badges
- `.loading-state`, `.error-state` — for page states

### File Changes Summary

| File | Action | Description |
|------|--------|-------------|
| `comparison.js` | **Rewrite** | New page controller with URL state, mode toggle, layouts, view registry |
| `compare.html.j2` | **Rewrite** | New template with mode toggle, dual-panel, grid layout, picker |
| `explorer.css` | **Append** | New classes for mode toggle, integrated/landscape layouts, view selectors, placeholders |
| `server.py` | **No change** | `/compare` route already serves pre-rendered template |

No new files created. No files deleted (old comparison.js is overwritten).

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| `VIEW_REGISTRY` global pattern fragile if scripts load out of order | Low | View scripts are loaded after comparison.js; registration is additive (null → function) |
| Mutual exclusion dropdown UX may feel clunky with `<option disabled>` | Low | Standard HTML behavior; worst case, replace with custom dropdown in polish pass |
| Picker click-outside detection conflicts with mode toggle area | Low | Same pattern as current comparison.js (:814-822) — exclude known interactive regions |
| `history.replaceState` on every view selector change may feel heavy | Low | replaceState is synchronous and lightweight — no navigation or network |

## Integration Strategy

**With Selection Tray (Item 1):**
- Tray navigates to `/compare?mode=...&concepts=...` — this page parses that exact format
- No shared state between tray and compare page (tray uses `?selected=`, compare uses `?concepts=`)
- No code dependency between `selection_tray.js` and the new `comparison.js`

**With Items 3a/3b (View Renderers):**
- Items 3a/3b register render functions on the global `VIEW_REGISTRY` object
- Shell dispatches to registered functions or falls back to placeholder
- Contract: `renderIntegrated(container, conceptDataArray)` and `renderLandscape(container, conceptData, syncContext)`
- Items 3a/3b add their own `<script>` tags to the template

**With Existing Pages:**
- No changes to concept profile, index grid, or taxonomy pages
- Only `compare.html.j2` and `comparison.js` are modified (plus CSS additions)

## Validation Approach

**Manual testing checklist:**

1. **URL parsing**: Navigate directly to URLs with various param combinations:
   - `/compare` (empty state)
   - `/compare?concepts=arc,sparc` (auto-select integrated, default views)
   - `/compare?mode=landscape&concepts=arc,sparc,iter,demo` (landscape, 2x2 grid)
   - `/compare?mode=integrated&concepts=a,b,c,d,e` (auto-correct to landscape)
   - `/compare?concepts=arc,INVALID,sparc` (skip invalid, show warning)
   - `/compare?mode=integrated&concepts=arc,sparc&left=capex&right=sensitivity` (custom views)

2. **Mode toggle**: Switch between modes, verify Integrated disables at >3

3. **Concept picker**: Add/remove concepts, verify URL updates and mode re-evaluation

4. **View selectors**: Change views in integrated panels, verify mutual exclusion. Change landscape view, verify all cells update.

5. **Browser navigation**: Use back/forward, verify layout updates without reload

6. **Tray integration**: Select concepts on taxonomy → launch comparison → verify correct mode and concepts load

7. **Regression**: Concept profile pages, index grid, taxonomy views all unchanged

---

**Next Step:** After approval → `/_my_plan`
