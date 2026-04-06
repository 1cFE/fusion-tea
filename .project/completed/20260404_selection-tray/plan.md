# Implementation Plan: Selection Tray & Taxonomy Integration

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/selection-tray/spec.md`
- **Design:** `.project/active/selection-tray/design.md` — See here for component details, API signatures, DOM structures, CSS specs, and integration patterns

## Implementation Strategy

**Phasing Rationale:**
Foundation first (tray module), then integrate one view at a time in ascending complexity (tree → constellation → graph), finish with cross-cutting concerns. Plotly `event` access is de-risked in Phase 1 before any constellation code is written.

**Overall Validation Approach:**
- No automated test framework — all validation is manual browser testing
- Each phase has specific manual checks that can be performed immediately
- Non-regression checks run at each phase to catch interaction breakage early

---

## Phase 1: SelectionTray Module + CSS Foundation

### Goal
Create the standalone tray module with full state management, chip rendering, popover, and URL sync. Add all CSS. Verify Plotly `event` access. After this phase, the tray renders on the taxonomy page and can be exercised from the browser console.

### Plotly Event De-Risk (Do First)
Before writing any code, verify the vendored Plotly exposes native event:
```javascript
// In browser console on /taxonomy:
// Temporarily attach a test handler
document.getElementById("constellation-container").on("plotly_click", function(d) {
  console.log("event prop:", d.event, "ctrlKey:", d.event && d.event.ctrlKey);
});
// Ctrl+click a dot — check console output
```
If `d.event` is undefined, the fallback approach (native `click` listener) is needed — flag before proceeding to Phase 3.

### Changes Required

**See `design.md` for:**
- Module state and public API → `design.md#component-selectiontray`
- Tray DOM structure → `design.md#component-selectiontray` (Tray DOM structure)
- Popover DOM structure and positioning → `design.md#component-selectiontray` (Popover DOM structure)
- URL sync approach → `design.md#component-selectiontray` (URL sync)
- All CSS specs → `design.md#css-additions`

**Specific file changes:**

#### 1. `exploration/concept_explorer/static/js/selection_tray.js` (NEW)
- [x] Create file using revealing module pattern (IIFE)
- [x] Tunable constants: `MIN_INTEGRATED`, `MAX_INTEGRATED`, `MIN_LANDSCAPE`, `MAX_LANDSCAPE`
- [x] Module state: `_selected` Map, `_registry`, `_changeListeners`, `_trayEl`, `_chipsEl`, `_popoverEl`
- [x] `init(containerParent, registry)`: Create tray DOM, append to parent, store registry, call `_restoreFromUrl()`
- [x] `add(concept)`: Add to `_selected`, call `_renderChips()`, `_syncUrl()`, `_notifyListeners()`
- [x] `remove(conceptId)`: Remove from `_selected`, call `_renderChips()`, `_syncUrl()`, `_notifyListeners()`
- [x] `toggle(concept)`: If `has()` → `remove()`, return `"removed"`. Else return `"pending"`.
- [x] `has(conceptId)`: Check `_selected.has()`
- [x] `getIds()`: Return `Array.from(_selected.keys())`
- [x] `showPopover(concept, anchorRect)`: Dismiss existing first (FR-17), create/reposition popover, populate with concept info + count + FR-14 cost model line, wire confirm button
- [x] `hidePopover()`: Hide and detach event listeners
- [x] `onChange(callback)`: Push to `_changeListeners`
- [x] `_renderChips()`: Clear chips container, render chip per selected concept (family badge, name, × button), show empty state text when none selected, update action button labels + enabled state
- [x] `_syncUrl()`: Build `URLSearchParams`, set `selected` param, `history.replaceState`
- [x] `_restoreFromUrl()`: Parse `?selected=`, split, look up each in `_registry`, call `add()` for each valid ID
- [x] `_updateActionButtons()`: Enable/disable based on count vs min/max constants, update count in label
- [x] Popover dismiss listeners: click-outside (document click), Escape key

#### 2. `exploration/concept_explorer/static/css/explorer.css` (MODIFY)
- [x] Add `padding-bottom: 56px` to taxonomy page `main` (NFR-1)
- [x] Add `.selection-tray` styles (fixed bottom bar per design)
- [x] Add `.selection-tray__clear` (ghost button, disabled state)
- [x] Add `.selection-tray__chips` (flex, overflow-x auto, gap)
- [x] Add `.selection-tray__empty` (muted hint text)
- [x] Add `.selection-tray__chip` (inline-flex, family border/badge, name, remove button)
- [x] Add `.selection-tray__chip--no-model` (dimmed opacity for concepts without `analysis_id`, FR-20)
- [x] Add `.selection-tray__action` (primary button, disabled state)
- [x] Add `.selection-popover` styles (fixed, z-200, surface-2 bg, shadow, radius)
- [x] Add `.selection-popover__header`, `__name`, `__info`, `__count`, `__confirm` styles

#### 3. `exploration/concept_explorer/dist/taxonomy.html` (MODIFY — line 104)
- [x] Add `<script src="/static/js/selection_tray.js"></script>` before existing scripts

#### 4. `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY — partial, init only)
- [x] After registry is built (~line 97), call `SelectionTray.init(document.querySelector("main"), _registry)`
- [x] Register empty `onChange` listener (views wired in later phases)

### Validation

**Manual:**
- [ ] Open `/taxonomy` → empty tray bar visible at bottom with hint text "Ctrl+click concepts to compare"
- [ ] Action buttons visible, both disabled
- [ ] Browser console: `SelectionTray.add({concept_id:"04", name:"ARC", confinement_family:"MFE", analysis_id:"04"})` → chip appears with blue badge
- [ ] Console: `SelectionTray.add({concept_id:"11", name:"NIF", confinement_family:"IFE"})` → second chip, purple badge, dimmed (no analysis_id)
- [ ] Click × on ARC chip → removed
- [ ] Click Clear All → all chips gone
- [ ] Add 2 concepts → Integrated button enabled, Landscape button enabled. Add 4th → Integrated disabled
- [ ] Check URL bar contains `?selected=04,11` after adding
- [ ] Copy URL, open in new tab → tray populated with same concepts
- [ ] Console: `SelectionTray.showPopover({concept_id:"04", name:"ARC", confinement_family:"MFE", analysis_id:"04"}, {left:400, top:300, width:0, height:0})` → popover appears near (400,300)
- [ ] Popover shows "Add to comparison?", concept name with badge, count. No cost model line (has analysis_id).
- [ ] Press Escape → popover dismissed
- [ ] Show popover for concept WITHOUT analysis_id → "No cost model — Categorical view only" line present
- [ ] Plotly event check: Ctrl+click constellation dot, verify `d.event` exists in console

**Non-Regression:**
- [ ] All existing taxonomy interactions work (tree click, constellation click/double-click, etc.)
- [ ] Tray does not obscure taxonomy content (padding-bottom applied)

**What We Know Works After This Phase:**
Tray module is fully functional as a standalone component. URL sync round-trips. Popover renders and dismisses. CSS is complete. Plotly event access confirmed.

---

## Phase 2: Tree View Integration

### Goal
First end-to-end Ctrl+click flow through the simplest handler (direct DOM, no debounce). Proves the full loop: modifier detect → toggle → popover → confirm → chip + visual indicator.

### Changes Required

**See `design.md` for:**
- Tree integration approach → `design.md#integration-tree-view`
- Orchestrator wiring → `design.md#integration-taxonomyjs` (items 2, 5, 6)
- Tree indicator CSS → `design.md#css-additions` (Tree leaf tray indicator)

**Specific file changes:**

#### 1. `exploration/concept_explorer/static/js/tree_view.js` (MODIFY)
- [x] Add `onCtrlClick` as 4th param to `renderTreeView()` (line 177), pass through to `buildBranch` → `buildLeaf`
- [x] In `buildLeaf` click handler (line 109): add modifier guard — if `e.metaKey || e.ctrlKey`, call `onCtrlClick(conceptId, e)` and return. Else existing `select()` call.
- [x] Add `updateTrayIndicators(selectedIds)` method: iterate `.tree-leaf` elements, toggle `.tree-leaf--in-tray` class based on `data-concept-id` membership
- [x] Export `updateTrayIndicators` in return object

#### 2. `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY)
- [x] Update `TreeView.renderTreeView` call (line 113): pass 4th arg `onCtrlClick` callback that calls `handleTrayToggle(concept, event.target.getBoundingClientRect())`
- [x] Add `handleTrayToggle(concept, anchorRect)` helper per design
- [x] In `SelectionTray.onChange` listener: call `TreeView.updateTrayIndicators(selectedIds)`

#### 3. `exploration/concept_explorer/static/css/explorer.css` (MODIFY)
- [x] Add `.tree-leaf--in-tray::after` styles (neutral dot indicator per design)

### Validation

**Manual:**
- [ ] Ctrl+click tree leaf → popover anchored near leaf, shows concept name + badge + count
- [ ] Click "Add" in popover → chip appears in tray, dot indicator appears on leaf
- [ ] Ctrl+click same leaf again → concept removed from tray (no popover), dot disappears
- [ ] Ctrl+click leaf for concept without cost model → popover shows "No cost model" info line
- [ ] Popover: click outside → dismissed. Escape → dismissed.
- [ ] Only one popover at a time: Ctrl+click leaf A → popover for A. Ctrl+click leaf B → popover for A dismissed, popover for B shown.

**Non-Regression:**
- [ ] Single-click tree leaf (no Ctrl) → still focuses concept in constellation/graph
- [ ] Keyboard Enter/Space on tree leaf → still focuses concept
- [ ] Branch expand/collapse → unchanged

**What We Know Works After This Phase:**
Full Ctrl+click → popover → chip → indicator → toggle loop works end-to-end. Tree interactions preserved.

---

## Phase 3: Constellation Integration

### Goal
Ctrl+click on Plotly scatter dots. Modifier check short-circuits the 300ms debounce. Visual ring indicator on selected dots via `marker.line` restyle.

### Changes Required

**See `design.md` for:**
- Constellation integration approach → `design.md#integration-constellation`
- Orchestrator wiring → `design.md#integration-taxonomyjs` (item 3)

**Specific file changes:**

#### 1. `exploration/concept_explorer/static/js/constellation.js` (MODIFY)
- [x] Add `onCtrlClick` as 5th param to `render()` (line 37)
- [x] In `plotly_click` handler (line 118), before debounce logic (line 125): check `eventData.event.metaKey || eventData.event.ctrlKey`. If true, call `onCtrlClick(conceptId, eventData.event)` and `return`.
- [x] Add `updateTrayIndicators(selectedIds)` method: iterate traces by family (same pattern as `highlight()`), build per-point `marker.line.width` and `marker.line.color` arrays, call `Plotly.restyle`
- [x] Export `updateTrayIndicators` in return object

#### 2. `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY)
- [x] Update `Constellation.render` call (line 117): pass 5th arg `onCtrlClick` callback using synthetic anchor rect from `nativeEvent.clientX/clientY`
- [x] In `SelectionTray.onChange` listener: call `Constellation.updateTrayIndicators(selectedIds)`

### Validation

**Manual:**
- [ ] Ctrl+click constellation dot → popover near cursor → confirm → chip in tray + white ring on dot
- [ ] Ctrl+click already-selected dot → removed from tray, ring disappears
- [ ] Add concept via tree, verify constellation ring also appears (onChange propagates)
- [ ] Remove concept via chip ×, verify constellation ring disappears

**Non-Regression:**
- [ ] Single-click constellation dot (no Ctrl) → dot highlights as before
- [ ] Double-click constellation dot → focuses concept, switches to neighborhood view
- [ ] Constellation legend and zoom/pan → unchanged

**What We Know Works After This Phase:**
Two views integrated. Cross-view indicator sync works (add in tree → ring in constellation). Debounce short-circuit pattern validated.

---

## Phase 4: Neighborhood Graph Integration

### Goal
Ctrl+click on neighbor and center nodes. Bridge exclusion (FR-27). Cytoscape `.in-tray` style. Handle graph re-render (destroyed/rebuilt on each focus) — indicators must refresh after render.

### Changes Required

**See `design.md` for:**
- Graph integration approach → `design.md#integration-neighborhood-graph`
- Orchestrator wiring → `design.md#integration-taxonomyjs` (item 4)
- Cytoscape stylesheet → `design.md#css-additions` (Neighborhood graph tray indicator)

**Specific file changes:**

#### 1. `exploration/concept_explorer/static/js/neighborhood_graph.js` (MODIFY)
- [x] In Cytoscape stylesheet array: add `{ selector: "node.in-tray", style: { "border-width": 3, "border-color": "#e6edf3", "border-style": "double" } }`
- [x] In `tap node.neighbor` handler (line 624): add modifier guard at top �� if `evt.originalEvent.metaKey || evt.originalEvent.ctrlKey`, call `callbacks.onCtrlClick(conceptId, evt.originalEvent)` and `return`
- [x] Add `tap node.center` handler: only fires on modifier click, calls `callbacks.onCtrlClick`
- [x] Add `updateTrayIndicators(selectedIds)` method: iterate `_cy.nodes(".neighbor, .center")`, add/remove `.in-tray` class based on ID membership
- [x] Export `updateTrayIndicators` in return object

#### 2. `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY)
- [x] In `switchToNeighborhood` (line 220), add `onCtrlClick` to callbacks object per design
- [x] In `SelectionTray.onChange` listener: call `NeighborhoodGraph.updateTrayIndicators(selectedIds)` when `_viewMode === "neighborhood"`
- [x] After `NeighborhoodGraph.render()` completes (inside the setTimeout at line 211): call `NeighborhoodGraph.updateTrayIndicators(SelectionTray.getIds())` to refresh indicators on re-render

### Validation

**Manual:**
- [ ] Focus a concept (double-click constellation) → switch to neighborhood view
- [ ] Ctrl+click a neighbor node → popover → confirm → chip + double-border on node
- [ ] Ctrl+click center node → popover → confirm → chip + double-border on center
- [ ] Ctrl+click a bridge node → nothing happens (bridge not selectable)
- [ ] Ctrl+click already-selected neighbor → removed, border reverts
- [ ] Focus a different concept (double-click neighbor) → graph re-renders → previously selected concepts still show `.in-tray` border if they appear as neighbors in new graph

**Non-Regression:**
- [ ] Single-click neighbor (no Ctrl) → shows bridge comparison as before
- [ ] Double-click neighbor → re-centers graph on that concept
- [ ] Background click → deselects comparison
- [ ] Tooltips on hover → unchanged

**What We Know Works After This Phase:**
All three views integrated. Ctrl+click works everywhere. Visual indicators propagate across views. Bridge exclusion enforced. Graph re-render preserves indicators.

---

## Phase 5: Action Buttons, Cross-View Persistence, Final Validation

### Goal
Wire action buttons to navigate to compare page. Verify selection persists across all taxonomy state transitions. Full non-regression pass.

### Changes Required

#### 1. `exploration/concept_explorer/static/js/selection_tray.js` (MODIFY)
- [x] In `init()` or `_renderChips()`: wire click handlers on action buttons — on click, build URL `/compare?mode={integrated|landscape}&concepts={ids}` and `window.location.href = url`
- [x] Verify action buttons show count in label (e.g., "Integrated (2)")

#### 2. `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY — minor)
- [x] Verify `switchToOverview()` does NOT clear selection tray (it shouldn't — tray state is orthogonal)
- [x] Verify `handleFocus()` does NOT clear selection tray

### Validation

**Full End-to-End Flow:**
- [ ] Start on `/taxonomy` overview
- [ ] Ctrl+click 2 tree leaves → 2 chips in tray
- [ ] Double-click constellation dot → switches to neighborhood view → tray still has 2 chips
- [ ] Ctrl+click a neighbor → 3 chips now
- [ ] Press Escape (back to overview) → tray still has 3 chips
- [ ] Ctrl+click constellation dot for 4th concept → tray has 4 chips
- [ ] Integrated button disabled (>3), Landscape button enabled
- [ ] Click "Landscape" → navigates to `/compare?mode=landscape&concepts=id1,id2,id3,id4`
- [ ] Browser back → tray restored from URL with 4 chips

**URL Restore:**
- [ ] Navigate to `/taxonomy?selected=04,05,17b` → tray populated with 3 concepts on load
- [ ] Invalid IDs in URL silently ignored (no JS errors)

**Full Non-Regression (all from `design.md#validation-approach`):**
- [ ] Tree single-click (no Ctrl) → focuses concept
- [ ] Constellation single-click → highlights dot
- [ ] Constellation double-click → focuses concept
- [ ] Graph neighbor single-click → shows bridges
- [ ] Graph neighbor double-click → re-centers
- [ ] Keyboard Enter/Space on tree leaf → focuses concept
- [ ] Graph bridge node Ctrl+click → nothing
- [ ] Escape key → back to overview
- [ ] Sidebar toggle → works, graph resizes

**What We Know Works After This Phase:**
Complete feature. Selection persists across all state transitions. Action buttons navigate correctly. URL is shareable. No regressions.

---

## Environment Setup

**See CLAUDE.md for full environment rules (use `uv run` for all Python commands)**

Server: `uv run python -m exploration.concept_explorer.server` (or however the dev server runs)
Browser: Open `http://localhost:PORT/taxonomy`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Plotly event verification done before any code depends on it. If `d.event` is undefined, Phase 3 switches to native click listener fallback.
- **Phase 4**: Graph re-render indicator refresh — call `updateTrayIndicators` after `NeighborhoodGraph.render()` completes, not just on selection change.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_explorer/static/js/selection_tray.js` — full IIFE module with state (Map), chip rendering, popover with viewport-aware positioning, URL sync via `history.replaceState`, and complete public API
- Modified `exploration/concept_explorer/static/css/explorer.css` — appended ~160 lines: tray bar (fixed bottom), chip styles with family-colored dot badges, no-model dimming, ghost clear button, primary action buttons with disabled state, popover with shadow/border, `main` padding-bottom: 56px
- Modified `exploration/concept_explorer/dist/taxonomy.html` — added `selection_tray.js` script tag before `tree_view.js`
- Modified `exploration/concept_explorer/static/js/taxonomy.js` — added `SelectionTray.init()` call after registry build, registered placeholder `onChange` listener for later phases
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Modified `tree_view.js`: threaded `onCtrlClick` through `renderTreeView` → `buildBranch` → `buildLeaf`; added modifier guard (`e.metaKey || e.ctrlKey`) in leaf click handler; added `updateTrayIndicators(selectedIds)` method using classList.toggle; exported in return object
- Modified `taxonomy.js`: added `handleTrayToggle(concept, anchorRect)` helper; passed `onCtrlClick` callback to `TreeView.renderTreeView`; wired `TreeView.updateTrayIndicators` in `onChange` listener
- Modified `explorer.css`: added `.tree-leaf--in-tray::after` neutral dot indicator (no redundant flex declarations since `.tree-leaf` already uses flex)
**Issues:** None
**Deviations:** Removed redundant `display:flex; align-items:center` from `.tree-leaf--in-tray` since `.tree-leaf` base class already declares these

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Modified `constellation.js`: added `onCtrlClick` as 5th param to `render()`; added modifier guard (`nativeEvent.metaKey || nativeEvent.ctrlKey`) before debounce logic in `plotly_click` handler — short-circuits entirely for Ctrl+click; added `updateTrayIndicators(selectedIds)` using `Plotly.restyle` on `marker.line.width`/`marker.line.color` arrays per trace; exported in return object
- Modified `taxonomy.js`: passed `onCtrlClick` callback to `Constellation.render` using synthetic anchor rect from `nativeEvent.clientX/clientY`; wired `Constellation.updateTrayIndicators` in `onChange` listener
**Issues:** None
**Deviations:** None

### Phase 4 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Modified `neighborhood_graph.js`: added `node.in-tray` Cytoscape stylesheet entry (double border, white); added modifier guard in `tap node.neighbor` handler; added new `tap node.center` handler (Ctrl+click only); added `updateTrayIndicators(selectedIds)` method using Cytoscape `addClass`/`removeClass`; exported in return object
- Modified `taxonomy.js`: added `onCtrlClick` callback to `switchToNeighborhood` callbacks object; called `NeighborhoodGraph.updateTrayIndicators(SelectionTray.getIds())` after render completes; wired `NeighborhoodGraph.updateTrayIndicators` in `onChange` listener (guarded by `_viewMode === "neighborhood"`)
**Issues:** None
**Deviations:** None

### Phase 5 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Action button wiring was already in place from Phase 1 (`_navigateToCompare` called from button click listeners in `init()`, count labels updated in `_updateActionButtons()`)
- Verified `switchToOverview()` and `handleFocus()` do not touch selection tray state
- Added `Constellation.updateTrayIndicators(SelectionTray.getIds())` call in `switchToOverview()` after constellation is re-shown — ensures rings are refreshed if selection changed while constellation was hidden during neighborhood view
**Issues:** None
**Deviations:** Added constellation indicator refresh in `switchToOverview()` — not in original plan but needed to handle the case where selection changes during neighborhood view while constellation is `display:none`

---

**Status**: Complete
