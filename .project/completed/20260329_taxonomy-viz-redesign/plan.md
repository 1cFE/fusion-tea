# Implementation Plan: Taxonomy Visualization Redesign

**Status:** Draft
**Created:** 2026-03-29 17:15 PDT
**Last Updated:** 2026-03-29 17:15 PDT

## Source Documents
- **Spec:** `.project/active/taxonomy-viz-redesign/spec.md`
- **Design:** `.project/active/taxonomy-viz-redesign/design.md` — See here for component details, SVG structure, CSS classes, state machine, interaction handlers

## Implementation Strategy

**Phasing Rationale:**
Server change first because it's tiny and unblocks bridge prioritization. Layout next because it's the container for everything — all subsequent phases render into it. The SVG graph (Phase 2) is the highest-risk new component and needs early validation. The comparison panel (Phase 3) is a parallel concern that can be built independently. The orchestrator (Phase 4) is the integration glue that wires everything together and must come last.

**Overall Validation Approach:**
- Phase 1 has automated tests (server-side bridge field)
- Phases 2-4 are frontend JS with no test infrastructure — validation is manual
- Test command: `uv run python -m pytest exploration/concept_explorer/tests/ -v`
- Server command: `uv run python exploration/concept_explorer/server.py`

---

## Phase 1: Server Change + Layout Foundation

### Goal
Add `bridge_overall_similarity` field to the API response, restructure the taxonomy page template to a 3-column layout, reorder nav tabs, and write all CSS upfront (layout, graph, comparison, tooltip classes). After this phase, the page loads with the new structure and all styling is in place for subsequent JS work.

### Test Stencil (Write This First)
```python
# In tests/test_similarity.py — update existing bridge tests

def test_bridge_has_overall_similarity(registry):
    """Bridge data includes overall similarity to query concept."""
    a = registry.by_id("hts-compact-tokamak")
    nearest = find_nearest(a, registry, top_n=1)[0]
    for bridge in nearest.bridges:
        assert hasattr(bridge, "bridge_overall_similarity")
        assert 0.0 <= bridge.bridge_overall_similarity <= 1.0
```

### Changes Required

**See `design.md` for:**
- Template structure → `design.md#component-1`
- CSS layout classes → `design.md#component-10`
- Nav reordering → `design.md#component-1` (Nav Reordering)
- Bridge field → `design.md#component-5` (Server-side change)

**Specific file changes:**

#### 1. Bridge Similarity Field
**File:** `exploration/concept_explorer/similarity.py`
- [x] Add `bridge_overall_similarity: float` field to `DifferenceBridge` model
- [x] In `explain_difference()`, look up overall similarity from precomputed matrix and pass to `DifferenceBridge` constructor

#### 2. Tests
**File:** `exploration/concept_explorer/tests/test_similarity.py`
- [x] Add test for `bridge_overall_similarity` field presence and range
- [x] Update any existing bridge assertions if field shape changes (none needed — additive field)

#### 3. Template Restructure
**File:** `exploration/concept_explorer/templates/taxonomy.html.j2` (REWRITE)
- [x] Three-column layout: sidebar with tree, toggle button, graph area (constellation + neighborhood containers), detail panel
- [x] Graph header with back button, title, subtitle
- [x] Loading/error/content state divs (keep existing pattern)
- [x] Script includes: add `neighborhood_graph.js` (will be created in Phase 2)

#### 4. Nav Reordering
**File:** `exploration/concept_explorer/templates/base.html.j2`
- [x] Move Taxonomy link to first position in nav

#### 5. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css`
- [x] Replace `.taxonomy-layout` 2-column grid with 4-column grid (see `design.md#component-1`)
- [x] Add `.taxonomy-layout--collapsed` modifier
- [x] Add `.taxonomy-detail` right panel (overflow-y, max-height, border)
- [x] Add `.sidebar-toggle` button styling
- [x] Add `.graph-header`, `__back`, `__title`, `__subtitle` classes
- [x] Add all `.ng-node`, `.ng-edge` SVG graph classes (see `design.md#component-2`)
- [x] Add `.ng-node--highlighted` pulse animation keyframes
- [x] Add `.neighbor-list`, `.neighbor-entry` classes
- [x] Add `.comparison-panel`, `.comparison-section`, `.comparison-row` classes (see `design.md#component-4`)
- [x] Add `.bridge-ref` styling
- [x] Add bridge edge dimension colors (see `design.md#component-10`)
- [x] Update `.tooltip` with `transition: opacity 0.15s`
- [x] Add container fade transition: `#constellation-container, #neighborhood-container { transition: opacity 0.3s; }`

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_similarity.py -v` → 23 passed
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → 141 passed, no regressions

**Manual:**
- [ ] Start server, navigate to `/taxonomy` → page loads with 3-column layout
- [ ] Taxonomy is the first nav tab
- [ ] Tree sidebar visible on left, constellation in center, detail panel on right (empty for now)
- [ ] Existing pages (All Concepts, Compare) still work
- [ ] `curl .../api/taxonomy/similarity/hts-compact-tokamak` → bridge objects have `bridge_overall_similarity` field

**What We Know Works After This Phase:**
The page structure is ready, all CSS is written, the API returns bridge similarity scores. Subsequent phases just add JS behavior into the existing containers.

---

## Phase 2: SVG Neighborhood Graph

### Goal
Build the complete graph renderer as a new JS module: SVG helper, radial layout computation, center/neighbor/bridge node rendering, similarity/bridge edge rendering, all interaction handlers (click, dblclick, hover), tooltip system, and bridge show/clear/highlight lifecycle. After this phase, the graph can be rendered with test data and all node interactions work.

### Test Stencil
No automated tests (no frontend test infrastructure). Validation is manual using the browser console to call the graph API directly.

```javascript
// Manual console test after Phase 2:
// Render a graph into the neighborhood container with mock data
var container = document.getElementById("neighborhood-container");
container.style.display = "";
var concept = { concept_id: "test", name: "Test Concept", confinement_family: "MFE" };
var neighbors = [
  { concept_id: "n1", concept_name: "Neighbor 1", confinement_family: "MFE",
    comparison: { overall_score: 0.75, overall_matches: 6, overall_comparable: 8, dimensions: [] },
    bridges: [] },
  // ... more neighbors
];
NeighborhoodGraph.render(container, concept, neighbors, {test: concept, n1: neighbors[0]}, {
  onCompare: function(id) { console.log("compare", id); },
  onFocus: function(id) { console.log("focus", id); },
  onDeselect: function() { console.log("deselect"); }
});
```

### Changes Required

**See `design.md` for:**
- SVG helper → `design.md#component-2` (SVG Helper)
- Layout computation → `design.md#component-2` (Layout Computation)
- SVG structure → `design.md#component-2` (SVG Structure)
- Node/edge shapes → `design.md#component-2` (Node shapes, Edge styles)
- Interaction handlers → `design.md#component-2` (Interaction Handlers)
- Tooltip system → `design.md#component-6`
- Bridge highlight → `design.md#component-2` (highlightBridge)

**Specific file changes:**

#### 1. Neighborhood Graph Module
**File:** `exploration/concept_explorer/static/js/neighborhood_graph.js` (NEW)
- [x] IIFE module pattern exporting `NeighborhoodGraph` object
- [x] `svgEl(tag, attrs)` helper using `createElementNS`
- [x] `el(tag, cls, text)` DOM helper (following codebase pattern)
- [x] `computeLayout(width, height, neighborCount)` — radial positions
- [x] `computeBridgePositions(layout, neighborIndex, bridgeCount)` — angular offsets from neighbor
- [x] Family color map constant (MFE blue, IFE purple, MIF amber, Non-Standard gray)
- [x] `FIELD_LABELS` constant — human-readable field names
- [x] `render(container, focusedConcept, neighbors, registry, callbacks)` — builds full SVG
  - [x] Center node (circle, r=32, family color)
  - [x] Neighbor nodes (circle, r=22, family color, name + score labels)
  - [x] Similarity edges (solid lines, width proportional to score)
  - [x] Text label truncation (~25 chars + ellipsis)
  - [x] Click/dblclick handlers on all nodes
  - [x] Hover handlers for tooltips on all nodes and edges
- [x] `showBridges(neighborId, bridges)` — add bridge nodes + edges, fade in
  - [x] Bridge nodes (rotated rect/diamond, family color, dashed stroke)
  - [x] Bridge edges (dashed, dimension-colored)
  - [x] Highlight the compared neighbor (`.ng-node--comparing` class)
- [x] `clearBridges()` — fade out and remove bridge elements, clear neighbor highlight
- [x] `highlightBridge(conceptId)` — pulse animation on a bridge node
- [x] `destroy()` — clean up SVG and tooltip element
- [x] Tooltip system: `showTooltip(event, html)`, `hideTooltip()`, viewport overflow handling
- [x] Tooltip content builders for each node/edge type (see `design.md#component-6`)

### Validation

**Manual:**
- [ ] Open `/taxonomy`, open browser console, run manual render test (see stencil above)
- [ ] SVG appears with center node and neighbor ring
- [ ] Hover nodes → tooltips appear with correct content, don't overflow viewport
- [ ] Click a neighbor → console logs "compare"
- [ ] Double-click a neighbor → console logs "focus"
- [ ] Click SVG background → console logs "deselect"
- [ ] Call `NeighborhoodGraph.showBridges(...)` → bridge nodes + edges fade in
- [ ] Call `NeighborhoodGraph.clearBridges()` → bridges fade out
- [ ] Call `NeighborhoodGraph.highlightBridge(...)` → bridge node pulses
- [ ] Node labels truncated for long names, full name in tooltip

**What We Know Works After This Phase:**
The SVG graph renders correctly, all node types display with proper shapes and colors, interactions fire callbacks, tooltips show contextual information, bridge lifecycle (show/clear/highlight) works. Ready to be wired by the orchestrator.

---

## Phase 3: Comparison Panel

### Goal
Rewrite the similarity card into two rendering modes: a compact neighbor list (FOCUSED state) and a field-by-field comparison table (COMPARING state). Implement the bridge selection algorithm and inline bridge references. After this phase, both panel modes render correctly with real data.

### Test Stencil
No automated tests. Manual validation with real API data in the browser console.

```javascript
// Manual console test after Phase 3:
// Fetch real similarity data, render comparison panel
fetch("/api/taxonomy/similarity/hts-compact-tokamak")
  .then(r => r.json())
  .then(function(report) {
    var container = document.getElementById("comparison-container");

    // Test neighbor list
    TaxonomyCards.renderNeighborList(container, report.nearest, function(id) {
      console.log("compare", id);
    });

    // Test comparison table (click first neighbor)
    var focused = /* from registry */;
    var neighbor = /* from registry */;
    TaxonomyCards.renderComparison(container, focused, neighbor, report.nearest[0],
      function(id) { console.log("highlight-bridge", id); },
      function(id) { console.log("compare", id); });
  });
```

### Changes Required

**See `design.md` for:**
- Neighbor list HTML → `design.md#component-4` (Neighbor List)
- Comparison table HTML → `design.md#component-4` (Comparison Table)
- Field label mapping → `design.md#component-4` (Field Label Mapping)
- Comparison builder → `design.md#component-4` (Building the Comparison)
- Bridge selection → `design.md#component-5`

**Specific file changes:**

#### 1. Taxonomy Card Module
**File:** `exploration/concept_explorer/static/js/taxonomy_card.js` (MODIFY)
- [x] Keep `renderTaxonomyCard()` intact
- [x] Remove `renderSimilarityCard()` and `buildSimilarityEntry()` (replaced entirely)
- [x] Add `FIELD_LABELS` constant and `TBD_VALUES` sentinel set
- [x] Add `selectBridges(bridges)` — max 3, unique fields, sorted by `bridge_overall_similarity`
- [x] Add `buildComparison(focused, neighbor, similarityResult)` — returns row objects
- [x] Add `renderNeighborList(container, nearest, onCompare, activeId)` — compact list with name, family badge, score
- [x] Add `renderComparison(container, focused, neighbor, result, selectedBridges, allNearest, onBridgeHighlight, onCompare)`:
  - [x] Header with neighbor name + score
  - [x] Differences section (prominent): field label, both values with "vs", bridge reference if exists
  - [x] Matches section (de-emphasized): field label, shared value, checkmark
  - [x] Other neighbors list (compact, below comparison)
  - [x] Click handlers: bridge refs call `onBridgeHighlight`, neighbor entries call `onCompare`
- [x] Add `setRegistry(registry)` for bridge family badge lookups in comparison panel

### Validation

**Manual:**
- [ ] Open `/taxonomy`, run console test (see stencil above)
- [ ] Neighbor list shows 5 entries with family badges and percentages
- [ ] Click a neighbor entry → console logs concept ID
- [ ] Comparison table shows differences first (prominent), matches below (muted)
- [ ] Differences show actual values ("Hybrid (thermal + direct)" vs "Thermal (unspecified)")
- [ ] Field labels are human-readable ("Energy Capture" not "energy_capture")
- [ ] Bridge references appear for mismatched fields with family badge
- [ ] At most 3 bridges shown, each for a different field
- [ ] Bridge ref click → console logs bridge concept ID
- [ ] N/A and TBD fields excluded from comparison rows

**What We Know Works After This Phase:**
The comparison panel renders both modes correctly with real data. Bridge selection produces sensible results. All interactive elements fire callbacks. Ready to be wired by the orchestrator.

---

## Phase 4: Orchestrator + Integration

### Goal
Rewrite the taxonomy.js orchestrator with the full state machine (OVERVIEW → FOCUSED → COMPARING), view mode switching (constellation ↔ graph with crossfade), constellation double-click handler, sidebar collapse toggle, Escape/back button, and wire all components together. After this phase, the full interaction flow works end-to-end.

### Test Stencil
No automated tests. Full manual walkthrough.

### Changes Required

**See `design.md` for:**
- State machine → `design.md#interaction-state-machine`
- View switching → `design.md#component-3`
- Orchestrator state + handlers → `design.md#component-8`
- Sidebar toggle → `design.md#component-9`
- Constellation double-click → `design.md#component-7`

**Specific file changes:**

#### 1. Orchestrator Rewrite
**File:** `exploration/concept_explorer/static/js/taxonomy.js` (REWRITE)
- [x] State variables: `_viewMode`, `_focusedId`, `_comparingId`, `_registry`, `_similarityCache`, `_sidebarCollapsed`
- [x] `init()` — parallel fetch tree/constellation/registry (keep existing pattern), render tree + constellation, set up sidebar toggle + back button + Escape key
- [x] `handleFocus(conceptId)` — fetch similarity, switch to neighborhood view, render taxonomy card + neighbor list, sync tree highlight
- [x] `handleCompare(neighborId)` — select bridges, call `NeighborhoodGraph.showBridges()`, render comparison table
- [x] `handleBridgeHighlight(conceptId)` — call `NeighborhoodGraph.highlightBridge()`
- [x] `handleDeselect()` — clear bridges, restore neighbor list
- [x] `switchToOverview()` — crossfade graph→constellation, update header, hide back button
- [x] `switchToNeighborhood(concept, neighbors)` — crossfade constellation→graph, update header, show back button
- [x] `fetchSimilarity(conceptId)` — fetch with cache (keep existing pattern)
- [x] Sidebar toggle handler (see `design.md#component-9`)
- [x] Escape key handler → `switchToOverview()` when in neighborhood mode
- [x] Wire `handleFocus` as tree's `onConceptClick` callback

#### 2. Constellation Double-Click
**File:** `exploration/concept_explorer/static/js/constellation.js` (MODIFY)
- [x] Add debounced double-click detection: on `plotly_click`, start 300ms timer; if second click on same point within window, treat as double-click and call `onDoubleClick` callback; otherwise fire single-click (existing highlight behavior)
- [x] Accept `onDoubleClick` callback in `render()` signature (additive — existing `onConceptClick` stays for single-click)
- [x] Add caption subtitle to Plotly layout as annotation below chart

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → 141 passed, no regressions

**Manual (full walkthrough — covers all spec acceptance criteria):**
- [ ] Page loads with constellation (overview mode). Title: "Design Space Overview". Subtitle visible. No back button.
- [ ] Taxonomy is first nav tab. Other pages still work.
- [ ] Sidebar toggle: click → tree collapses, graph expands. Click again → tree returns.
- [ ] Double-click a concept in constellation → crossfade to neighborhood graph. Center node, 5 neighbors in ring. Header: "Neighborhood of {name}". Back button visible.
- [ ] Single-click a tree leaf → same focus behavior. Tree highlights leaf.
- [ ] Single-click a neighbor in graph → neighbor glows, comparison table appears in detail panel. Differences first with actual values. Matches below (muted). Up to 3 bridge nodes fade into graph.
- [ ] Bridge nodes are diamond-shaped, family-colored. Bridge edges are dashed, dimension-colored.
- [ ] Hover bridge node → tooltip: concept name, family, shared attribute.
- [ ] Hover bridge edge → tooltip: "Both use {value} for {field}".
- [ ] Click bridge ref in comparison panel → bridge node pulses in graph.
- [ ] Single-click a different neighbor → old bridges fade out, new bridges fade in. Comparison updates.
- [ ] Click graph background → deselect neighbor. Bridges clear. Neighbor list restores.
- [ ] Double-click a neighbor → graph re-centers on that concept. New neighborhood loads.
- [ ] Double-click a bridge → graph re-centers on bridge concept. New neighborhood loads.
- [ ] Click "← Overview" → crossfade back to constellation. Header restores. Back button hides.
- [ ] Press Escape → same as back button.
- [ ] Detail panel scrolls independently — graph stays in view.
- [ ] Domain sanity: HTS Compact Tokamak neighbors are mostly tokamaks. Click one → differences show actual values (e.g., different magnet type). Bridge shows a non-tokamak with same magnet type.

**What We Know Works After This Phase:**
The full taxonomy page redesign is functional. All interaction states work (overview, focused, comparing). Navigation across the design space via bridge concepts works. Sidebar collapses. Detail panel scrolls independently. Tooltips explain what the user is looking at.

---

## Environment Setup

See `CLAUDE.md` for full environment rules. Key commands:
- Run tests: `uv run python -m pytest exploration/concept_explorer/tests/ -v`
- Start server: `uv run python exploration/concept_explorer/server.py`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Layout might break existing taxonomy functionality — verify constellation still renders in the new container
- **Phase 2**: SVG text overflow for long concept names — implement truncation from the start, not as a fixup
- **Phase 3**: Bridge selection with missing `bridge_overall_similarity` — fallback to insertion order is acceptable during development (R-4)
- **Phase 4**: Plotly double-click conflict (R-1) — implement debounced click pattern; if fragile, fall back to explicit "Explore" button on hover

---

## Implementation Notes

_TO BE FILLED DURING IMPLEMENTATION_

### Phase 1 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- `similarity.py:62-70` — Added `bridge_overall_similarity: float` field to `DifferenceBridge` model
- `similarity.py:265-276` — Passed `best_bridge[0]` (the already-computed score) as `bridge_overall_similarity` in `explain_difference()`
- `tests/test_similarity.py:197-204` — Added `test_bridge_has_overall_similarity` test
- `templates/base.html.j2:16-30` — Moved Taxonomy nav link to first position
- `templates/taxonomy.html.j2` — Full rewrite: 3-column layout (sidebar + toggle + graph area + detail panel), graph header with back button, constellation + neighborhood containers, script include for neighborhood_graph.js
- `static/css/explorer.css:1205+` — Replaced 2-col `.taxonomy-layout` with 4-col grid, added `.taxonomy-layout--collapsed`, `.taxonomy-sidebar__header`, `.sidebar-toggle`, `.taxonomy-graph`, `.graph-header` + sub-classes, `.taxonomy-detail`, view container transitions
- `static/css/explorer.css` (appended) — All SVG graph classes (`.ng-node`, `.ng-edge`, dimension colors, bridge-pulse keyframes), neighbor list classes, comparison panel classes, bridge-ref styling
- `static/js/neighborhood_graph.js` — Created stub module (no-op exports) so template script tag doesn't 404
**Issues:** None
**Deviations:** None — followed plan exactly

### Phase 2 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- `static/js/neighborhood_graph.js` — Full implementation replacing stub. IIFE module with: SVG helpers (svgEl, el, truncate, esc), layout computation (computeLayout, computeBridgePositions), tooltip system (showTooltip/hideTooltip with viewport overflow, content builders for center/neighbor/bridge nodes and similarity/bridge edges), render() with center node (r=32, drop shadow filter), neighbor ring (r=22, click/dblclick/hover), similarity edges (width proportional to score, invisible hit areas for hover), showBridges/clearBridges/highlightBridge lifecycle with requestAnimationFrame fade-in and 350ms fade-out removal.
**Issues:** None
**Deviations:** Added invisible wider hit areas (stroke-width: 12, transparent) on edges for hover tooltip targeting — not in design but necessary for usability since 1.5-3px lines are too thin to hover reliably.

### Phase 3 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- `static/js/taxonomy_card.js` — Removed `buildSimilarityEntry()` and `renderSimilarityCard()`. Added: `FIELD_LABELS` constant, `TBD_VALUES` sentinel set, `selectBridges()` (FR-10 bridge selection: max 3, unique fields, sorted by bridge_overall_similarity), `buildComparison()` (row builder from dimensions data with N/A/TBD filtering), `renderNeighborList()` (compact list with family badges, scores, active highlight), `renderComparison()` (field-by-field table with differences prominent + bridge refs + matches muted + other neighbors list), `setRegistry()` for bridge family badge lookups. Updated public API.
**Issues:** None
**Deviations:**
- Added `setRegistry()` method — design had the comparison panel looking up registry concepts for bridge family badges, but the IIFE doesn't have access to the orchestrator's `_registry`. Added a setter that the orchestrator will call during init.
- `renderComparison` takes `selectedBridges` as a parameter instead of calling `selectBridges` internally — cleaner separation since the orchestrator needs the selected bridges for both the graph and the panel.
- Added `activeId` parameter to `renderNeighborList` for highlighting the currently-compared neighbor.

### Phase 4 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- `static/js/taxonomy.js` — Full rewrite. IIFE with state machine (OVERVIEW/FOCUSED/COMPARING). State: `_viewMode`, `_focusedId`, `_comparingId`, `_registry`, `_similarityCache`, `_sidebarCollapsed`. DOM references cached in init(). Parallel data fetch (tree/constellation/registry), shares registry with TaxonomyCards via `setRegistry()`. `handleFocus()` fetches similarity, calls `switchToNeighborhood()`, renders taxonomy card + neighbor list. `handleCompare()` calls `TaxonomyCards.selectBridges()` then `NeighborhoodGraph.showBridges()` + `TaxonomyCards.renderComparison()`. `handleDeselect()` clears bridges, restores neighbor list. `switchToOverview()`/`switchToNeighborhood()` implement crossfade with 300ms CSS transition + setTimeout display swap. Sidebar toggle with CSS class toggle + Plotly resize. Back button + Escape key both call `switchToOverview()`. Tree wired with `handleFocus` directly (single-click focuses).
- `static/js/constellation.js` — Added `onDoubleClick` callback parameter to `render()`. Debounced double-click detection via 300ms timer on `plotly_click`: second click on same point within window fires `onDoubleClick`, otherwise fires `onConceptClick` after delay. Added `doubleClick: false` to Plotly config to disable built-in zoom reset. Added caption as Plotly annotation below chart.
**Issues:** None
**Deviations:**
- Constellation single-click in overview mode only highlights the dot (no focus). This matches DD-4 (constellation requires double-click to focus). The design's `onConceptClick` was ambiguous — clarified as highlight-only for constellation single-click.
- Added `void container.offsetHeight` reflow trick before setting opacity in view switches — ensures CSS transition triggers after display change.
- `handleFocus` does not guard against re-focus on same concept (removed `if (conceptId === _focusedId) return`). This allows re-centering when user clicks tree after comparing, which feels more natural.

---

**Status**: Complete — all 4 phases implemented
