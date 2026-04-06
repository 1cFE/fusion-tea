# Design: Selection Tray & Taxonomy Integration

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05 17:24
**Updated:** 2026-04-05 17:24
**Branch:** ralph/concept-explorer
**Commit:** d4ceb34

---

## Overview

A persistent bottom bar on the taxonomy page that accumulates concept selections via Ctrl/Cmd+click across tree, constellation, and neighborhood graph views. Selections display as family-colored chips with action buttons to launch Integrated or Landscape comparison modes.

## Related Artifacts

- **Spec:** `.project/active/selection-tray/spec.md`
- **Concept:** `.project/active/explorer-ux-v2/concept.md`
- **Epic:** `.project/backlog/epic_explorer_ux_v2.md` (Item 1)

---

## Research Findings

### Existing Click Handlers

Each taxonomy view uses a distinct click-handling pattern. Ctrl+click detection must be injected into each one differently:

| View | Handler Location | Click Pattern | Modifier Key Access |
|------|-----------------|---------------|-------------------|
| **Tree** | `tree_view.js:109` — `leaf.addEventListener("click", fn)` | Direct DOM click, calls `onConceptClick(conceptId)` | Native `e.ctrlKey`, `e.metaKey` |
| **Constellation** | `constellation.js:118` — `container.on("plotly_click", fn)` | Plotly event wrapper, 300ms debounce for double-click | `eventData.event.ctrlKey`, `eventData.event.metaKey` (Plotly exposes native event as `.event`) |
| **Neighborhood** | `neighborhood_graph.js:624` — `_cy.on("tap", "node.neighbor", fn)` | Cytoscape event, 300ms debounce for double-click | `evt.originalEvent.ctrlKey`, `evt.originalEvent.metaKey` |

**Key insight**: All three handlers have access to the native browser event's modifier key state. The Ctrl+click check can be a simple guard at the top of each existing handler — no restructuring needed.

### State Machine Integration

The taxonomy page has three states (`taxonomy.js:6-17`):
- **OVERVIEW**: Constellation visible, no concept focused
- **FOCUSED**: Neighborhood graph visible, taxonomy card shown
- **COMPARING**: Focused + neighbor selected, comparison table visible

Selection tray state is **orthogonal** to the taxonomy state machine — concepts can be added/removed in any state. The tray doesn't trigger state transitions and state transitions don't affect the tray.

### Data Available at Click Time

When a concept is clicked in any view, `_registry[conceptId]` (`taxonomy.js:28`) provides the full `ConceptTaxonomy` object with:
- `concept_id`, `name`, `confinement_family` — needed for chip rendering
- `analysis_id` — presence indicates a cost model exists (used in popover indicator, FR-14)

The registry is loaded at init and available throughout the page lifecycle.

### CSS Patterns

- Family badge colors: `--color-badge-mfe`, `--color-badge-ife`, `--color-badge-mif`, `--color-badge-nonstandard` (`explorer.css:38-42`)
- Badge component: `.badge.badge-{family}` classes (`explorer.css:363-398`) — inline-flex, padding, uppercase, 15% opacity background
- Spacing scale: `--space-1` through `--space-12` (`explorer.css:44-53`)
- Surface colors: `--color-surface-1` through `--color-surface-3` for layered UI (`explorer.css:12-14`)
- Footer height: Simple text footer at `explorer.css:98-100`, ~48px

### Existing Selection Chip Pattern

`comparison.js:180-215` renders concept chips in the compare page's selector. Pattern: chip div with name span + remove button. We'll follow this pattern but add family-colored badges.

### Graph Node Types

`neighborhood_graph.js` uses Cytoscape classes to distinguish node types:
- `.center` — the focused concept (line 624 has no tap handler for center — we'll add one)
- `.neighbor` — similar concepts (line 624 tap handler)
- `.bridge` — intermediate concepts shown during comparison (should NOT be selectable per FR-27)

### Module Loading

All JS is loaded via `<script>` tags (`taxonomy.html:104-109`). Modules use the revealing module pattern (IIFE returning public API). The new `selection_tray.js` script will follow this pattern and must be loaded before `taxonomy.js` (which wires everything together).

---

## Proposed Design

### Architecture

```
                         ┌──────────────────────┐
                         │   SelectionTray       │
                         │  (selection_tray.js)  │
                         │                       │
                         │ State: Set<concept_id>│
                         │ UI: bottom bar + chips│
                         │ Popover: anchored     │
                         │ URL: ?selected=...    │
                         └──────────┬────────────┘
                                    │
                         onChange callback
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
   ┌──────────▼──────┐  ┌──────────▼──────┐  ┌──────────▼──────┐
   │   TreeView       │  │  Constellation   │  │ NeighborhoodGraph│
   │ Ctrl+click guard │  │ Ctrl+click guard │  │ Ctrl+click guard │
   │ .tree-leaf--tray │  │ ring restyle     │  │ .in-tray class   │
   └─────────────────┘  └─────────────────┘  └──────────────────┘
```

**`taxonomy.js`** wires everything: passes the `SelectionTray` reference to each view's click handler callbacks, and registers a `SelectionTray.onChange` listener that calls each view's visual update method.

### Component: SelectionTray (`selection_tray.js`)

**Location**: `exploration/concept_explorer/static/js/selection_tray.js`

**Constants** (top of file, tunable):
```javascript
var MIN_INTEGRATED = 1;
var MAX_INTEGRATED = 3;
var MIN_LANDSCAPE = 1;
var MAX_LANDSCAPE = 6;
```

**Module state**:
```javascript
var _selected = new Map();      // concept_id → { concept_id, name, confinement_family, analysis_id }
var _registry = null;            // concept_id → ConceptTaxonomy (for URL restore)
var _changeListeners = [];       // Array<Function(selectedIds: string[])>
var _trayEl = null;              // .selection-tray root element
var _chipsEl = null;             // .selection-tray__chips container
var _popoverEl = null;           // .selection-popover element (reused, repositioned)
```

**Public API**:

| Method | Purpose |
|--------|---------|
| `init(containerParent, registry)` | Creates tray DOM, appends to containerParent, stores registry for URL restore, reads URL params |
| `add(concept)` | Adds concept to selection, updates UI, syncs URL. No hard cap — buttons disable beyond max but adding is unrestricted. |
| `remove(conceptId)` | Removes concept, updates UI, syncs URL |
| `toggle(concept)` | If already selected → removes it, returns `"removed"`. If not selected → returns `"pending"` (caller should show popover). |
| `has(conceptId)` | Returns boolean |
| `getIds()` | Returns array of selected concept_ids |
| `showPopover(concept, anchorRect)` | Dismisses any existing popover first (FR-17: only one popover at a time), then shows anchored popover for add confirmation |
| `hidePopover()` | Dismisses popover |
| `onChange(callback)` | Registers change listener |

**Popover flow**:
1. Ctrl+click detected in view handler → calls `SelectionTray.toggle(concept)`
2. If concept was selected → `toggle` removes it, returns `"removed"` (done, no popover)
3. If concept was NOT selected → `toggle` returns `"pending"`, caller then calls `showPopover(concept, anchorRect)`
4. `showPopover` dismisses any existing popover first, then shows the new one
5. Popover shows "Add [Name] to comparison?" + count + confirm button
6. Popover info line (FR-14): If concept lacks `analysis_id`, shows "No cost model — Categorical view only". If concept has `analysis_id`, the info line is omitted (cost model availability is the default/expected case).
7. User clicks "Add" → `SelectionTray.add(concept)` → popover dismisses
8. Popover dismisses on: confirm click, click outside, Escape key

**URL sync**:
- On selection change: `history.replaceState(null, "", "?" + params.toString())` where `params` includes `selected=id1,id2,id3`
- On init: parse `new URLSearchParams(window.location.search).get("selected")`, split by comma, look up each in registry, add to selection
- Preserves any existing query params (future-proof for other URL state)

**Tray DOM structure**:
```html
<div class="selection-tray">
  <button class="selection-tray__clear" disabled>Clear All</button>
  <div class="selection-tray__chips">
    <!-- When empty: -->
    <span class="selection-tray__empty">Ctrl+click concepts to compare</span>
    <!-- When populated: -->
    <div class="selection-tray__chip" data-concept-id="04">
      <span class="selection-tray__chip-badge badge-mfe"></span>
      <span class="selection-tray__chip-name">ARC</span>
      <button class="selection-tray__chip-remove" aria-label="Remove ARC">×</button>
    </div>
    <!-- ... more chips ... -->
  </div>
  <div class="selection-tray__actions">
    <button class="selection-tray__action" data-mode="integrated" disabled>
      Integrated (0)
    </button>
    <button class="selection-tray__action" data-mode="landscape" disabled>
      Landscape (0)
    </button>
  </div>
</div>
```

**Popover DOM structure**:
```html
<div class="selection-popover" style="position:fixed; left:...; top:...;">
  <div class="selection-popover__header">Add to comparison?</div>
  <div class="selection-popover__name">
    <span class="badge badge-mfe">MFE</span> ARC
  </div>
  <div class="selection-popover__info">No cost model — Categorical view only</div>
  <div class="selection-popover__count">2 of 6 selected</div>
  <button class="selection-popover__confirm">Add</button>
</div>
```

**Popover positioning**: Fixed position using `anchorRect` (from `getBoundingClientRect()` or Cytoscape/Plotly event coordinates). Viewport-aware: if popover would overflow right/bottom, flip to left/top of anchor. Reuses a single DOM element (moved and repopulated each time).

### Integration: Tree View

**File**: `tree_view.js` — modify `buildLeaf` function (line 106-111)

**Change**: The `select` function (line 106) and the click handler (line 109) need to check for modifier keys. However, `buildLeaf` only receives `onConceptClick` — it doesn't know about the selection tray.

**Approach**: Add a second callback parameter `onCtrlClick` to the tree rendering chain:

1. `renderTreeView(container, treeData, onConceptClick, onCtrlClick)` — new 4th param
2. In `buildLeaf`, the click handler checks `e.metaKey || e.ctrlKey`:
   - If modifier held → call `onCtrlClick(conceptId, e)` (passes event for popover positioning via `leaf.getBoundingClientRect()`)
   - If no modifier → call `onConceptClick(conceptId)` (existing behavior, unchanged)
3. Keyboard handler (Enter/Space) unchanged — no modifier check (FR-26)

**Visual indicator**: New CSS class `.tree-leaf--in-tray` applied via a new `updateTrayIndicators(selectedIds)` method on `TreeView`:
- Iterates all `.tree-leaf` elements, toggles `.tree-leaf--in-tray` based on `data-concept-id` membership in `selectedIds`
- Called by taxonomy.js when `SelectionTray.onChange` fires

### Integration: Constellation

**File**: `constellation.js` — modify click handler (line 118-142)

**Change**: The `plotly_click` handler needs a modifier check before the debounce logic.

**Approach**: Add `onCtrlClick` as a 5th parameter to `Constellation.render()`:

1. `render(container, data, onConceptClick, onDoubleClick, onCtrlClick)` — new 5th param
2. At the top of the `plotly_click` handler (before line 125), add:
   ```javascript
   var nativeEvent = eventData.event;
   if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
     if (onCtrlClick) onCtrlClick(conceptId, nativeEvent);
     return; // Don't proceed to single/double-click logic
   }
   ```
3. This short-circuits the debounce entirely for Ctrl+click — no 300ms delay.

**Visual indicator**: New method `Constellation.updateTrayIndicators(selectedIds)`:
- Uses `Plotly.restyle` to set per-point `marker.line.width` and `marker.line.color` arrays
- Selected points: `marker.line.width: 3`, `marker.line.color: "#e6edf3"` (white ring)
- Unselected points: `marker.line.width: 1`, `marker.line.color: "rgba(255,255,255,0.2)"` (existing default)
- Iterates traces by family (same pattern as `highlight()`), builds arrays per trace
- Called by taxonomy.js when `SelectionTray.onChange` fires

**Anchor rect for popover**: Plotly click events don't give a direct element rect. Use `nativeEvent.clientX/clientY` to create a synthetic anchor rect `{ left: clientX, top: clientY, width: 0, height: 0 }`. The popover positions itself relative to this point.

### Integration: Neighborhood Graph

**File**: `neighborhood_graph.js` — modify tap handlers (lines 624-660)

**Change**: Modifier check in the `tap node.neighbor` handler and add a new `tap node.center` handler for Ctrl+click on the focused concept.

**Approach**: Add `onCtrlClick` to the `callbacks` object passed to `render()`:

1. In the `tap node.neighbor` handler (line 624), add modifier check:
   ```javascript
   _cy.on("tap", "node.neighbor", function (evt) {
     var conceptId = evt.target.id();
     var nativeEvent = evt.originalEvent;
     if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
       if (callbacks.onCtrlClick) callbacks.onCtrlClick(conceptId, nativeEvent);
       return;
     }
     // ... existing debounce logic unchanged ...
   });
   ```

2. Add new handler for center node Ctrl+click:
   ```javascript
   _cy.on("tap", "node.center", function (evt) {
     var conceptId = evt.target.id();
     var nativeEvent = evt.originalEvent;
     if (nativeEvent && (nativeEvent.metaKey || nativeEvent.ctrlKey)) {
       if (callbacks.onCtrlClick) callbacks.onCtrlClick(conceptId, nativeEvent);
     }
     // No other action — center node has no existing click behavior
   });
   ```

3. Bridge nodes: No handler change — `.bridge` nodes remain unselectable (FR-27). The existing bridge tap handler (line 644) stays as-is.

**Visual indicator**: New method `NeighborhoodGraph.updateTrayIndicators(selectedIds)`:
- Adds/removes `.in-tray` Cytoscape class on neighbor and center nodes
- Cytoscape stylesheet entry for `.in-tray`: thicker border or ring overlay
- Called by taxonomy.js when `SelectionTray.onChange` fires

**Anchor rect for popover**: Use `evt.originalEvent.clientX/clientY` (same as constellation).

### Integration: taxonomy.js (Orchestrator)

**File**: `taxonomy.js` — wire everything together in `init()`

**Changes**:

1. **Import and init tray** (after data fetch, before view rendering):
   ```javascript
   // Init selection tray, reading URL params
   SelectionTray.init(document.querySelector("main"), _registry);
   ```
   The tray appends itself inside `<main>`, positioned fixed at bottom.

2. **Wire tree Ctrl+click** (line 113):
   ```javascript
   TreeView.renderTreeView(treeContainer, treeData, handleFocus, function onCtrlClick(conceptId, event) {
     var concept = _registry[conceptId];
     if (!concept) return;
     handleTrayToggle(concept, event.target.getBoundingClientRect());
   });
   ```

3. **Wire constellation Ctrl+click** (line 117):
   ```javascript
   Constellation.render(constellationContainer, constellationData,
     function onSingleClick(conceptId) { Constellation.highlight(conceptId); },
     function onDoubleClick(conceptId) { handleFocus(conceptId); },
     function onCtrlClick(conceptId, nativeEvent) {
       var concept = _registry[conceptId];
       if (!concept) return;
       handleTrayToggle(concept, { left: nativeEvent.clientX, top: nativeEvent.clientY, width: 0, height: 0 });
     }
   );
   ```

4. **Wire neighborhood Ctrl+click** (line 220, in `switchToNeighborhood`):
   Add `onCtrlClick` to the callbacks object:
   ```javascript
   NeighborhoodGraph.render(neighborhoodContainer, concept, report, _registry, {
     onCompare: handleCompare,
     onFocus: handleFocus,
     onDeselect: handleDeselect,
     onCtrlClick: function (conceptId, nativeEvent) {
       var c = _registry[conceptId];
       if (!c) return;
       handleTrayToggle(c, { left: nativeEvent.clientX, top: nativeEvent.clientY, width: 0, height: 0 });
     }
   });
   ```

5. **New helper in taxonomy.js**:
   ```javascript
   function handleTrayToggle(concept, anchorRect) {
     var result = SelectionTray.toggle(concept);
     if (result === "pending") {
       SelectionTray.showPopover(concept, anchorRect);
     }
   }
   ```

6. **Register change listener** for visual indicators:
   ```javascript
   SelectionTray.onChange(function (selectedIds) {
     TreeView.updateTrayIndicators(selectedIds);
     Constellation.updateTrayIndicators(selectedIds);
     if (_viewMode === "neighborhood") {
       NeighborhoodGraph.updateTrayIndicators(selectedIds);
     }
   });
   ```

### CSS Additions (`explorer.css`)

New sections appended to `explorer.css`:

**Selection Tray**:
```css
.selection-tray {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  background: var(--color-surface-1);
  border-top: 1px solid var(--color-border);
  min-height: 48px;
}
```

- `main` gets `padding-bottom: 56px` to prevent tray from obscuring content (NFR-1)
- Clear All button: ghost style, disabled when empty
- Chips area: `flex: 1; overflow-x: auto; display: flex; gap: var(--space-2);`
- Each chip: inline-flex with family-colored left border or small circle badge, name text, × button
- Chips for concepts WITHOUT `analysis_id`: slightly dimmed opacity (FR-20)
- Action buttons: primary style, disabled state with muted color + cursor

**Selection Popover**:
```css
.selection-popover {
  position: fixed;
  z-index: 200;
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  box-shadow: 0 4px 16px rgba(0,0,0,0.4);
  min-width: 200px;
  max-width: 280px;
}
```

**Tree leaf tray indicator**: A neutral-colored dot signals "this concept is in the tray." Family color is unnecessary here — the tree doesn't know each leaf's family, and the family color already shows in the tray chip.
```css
.tree-leaf--in-tray::after {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-muted);
  margin-left: auto;
  flex-shrink: 0;
}
```

**Neighborhood graph tray indicator** (Cytoscape stylesheet addition in `neighborhood_graph.js`):
```javascript
{
  selector: "node.in-tray",
  style: {
    "border-width": 3,
    "border-color": "#e6edf3",  // --color-text-primary
    "border-style": "double"
  }
}
```

### Navigation to Compare Page (FR-10)

Action buttons construct a URL and navigate:
```javascript
window.location.href = "/compare?mode=" + mode + "&concepts=" + ids.join(",");
```

The URL format is owned by Item 2 (Compare Shell). For now, we construct this URL shape. If Item 2 changes the format, only the navigation line needs updating.

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Plotly `plotly_click` may not expose `event` in all versions | High — no modifier detection in constellation | Verify with vendored Plotly version. Fallback: listen for native `click` on Plotly container and correlate with `plotly_click` timing |
| Ctrl+click triggers context menu on macOS | Medium — interference with selection | Spec already handles this: detect `metaKey` (Cmd on Mac). Users use Cmd+click on macOS, Ctrl+click on Windows/Linux. Both work via `e.metaKey \|\| e.ctrlKey` |
| `history.replaceState` URL updates cause Plotly resize or Cytoscape reset | Low — but possible | `replaceState` doesn't trigger `popstate` or page navigation. Verify no side effects |
| Popover positioning near viewport edges | Low — poor UX if clipped | Viewport-aware flip logic in `showPopover` (check if anchor + popover dimensions exceed `window.innerWidth`/`innerHeight`) |

---

## Integration Strategy

### File Changes Summary

| File | Change Type | Description |
|------|------------|-------------|
| `selection_tray.js` | **New** | Selection state, tray UI, popover, URL sync |
| `taxonomy.js` | Modify | Init tray, wire Ctrl+click callbacks, register onChange listener |
| `tree_view.js` | Modify | Add `onCtrlClick` param, modifier guard in click handler, `updateTrayIndicators` method |
| `constellation.js` | Modify | Add `onCtrlClick` param, modifier guard in plotly_click, `updateTrayIndicators` method |
| `neighborhood_graph.js` | Modify | Modifier guard in neighbor tap, new center tap handler, `.in-tray` stylesheet, `updateTrayIndicators` method |
| `taxonomy.html` | Modify | Add `<script>` for `selection_tray.js` (before `taxonomy.js`) |
| `explorer.css` | Modify | Add tray, chip, popover, and indicator styles |

### Script Load Order

```html
<script src="/static/js/selection_tray.js"></script>  <!-- NEW -->
<script src="/static/js/tree_view.js"></script>
<script src="/static/js/constellation.js"></script>
<script src="/static/js/taxonomy_card.js"></script>
<script src="/static/js/neighborhood_graph.js"></script>
<script src="/static/js/taxonomy.js"></script>
```

`selection_tray.js` loads first (no dependencies on other modules). `taxonomy.js` loads last (depends on all others).

### What This Complements/Replaces

- **Complements**: All existing taxonomy interactions — Ctrl+click is additive, no existing behavior changes
- **Does NOT replace**: The compare page's concept picker (`comparison.js:165-274`) — that stays until Item 2 replaces it
- **Prepares for**: Item 2 (Compare Shell) which will consume the URL format this item produces

---

## Validation Approach

### Manual Testing Checklist

1. **Ctrl+click on tree leaf** → popover appears anchored to leaf → confirm → chip appears in tray
2. **Ctrl+click on constellation dot** → popover appears near dot → confirm → chip in tray
3. **Ctrl+click on graph neighbor** → popover appears near node → confirm → chip in tray
4. **Ctrl+click on graph center** → same behavior as neighbor
5. **Ctrl+click on already-selected concept** → concept removed from tray (no popover)
6. **× on chip** → concept removed from tray
7. **Clear All** → all chips removed
8. **Switch taxonomy tabs** (overview ↔ neighborhood) → tray persists
9. **Visual indicators** update in current view when selection changes
10. **URL updates** on each selection change → copy URL → open in new tab → tray populated
11. **Action buttons** → enabled/disabled based on count → click navigates to `/compare?mode=...&concepts=...`
12. **Popover dismissal** → click outside, Escape, or confirm all dismiss
13. **macOS** → Cmd+click works (test `metaKey`)

### Non-Regression

14. **Tree single-click** (no Ctrl) → still focuses concept as before
15. **Constellation double-click** → still focuses concept
16. **Graph neighbor single-click** → still shows bridges
17. **Graph neighbor double-click** → still re-centers
18. **Keyboard Enter/Space on tree leaf** → still focuses concept
19. **Graph bridge node Ctrl+click** → nothing happens (not selectable)

---

Next Step: After approval → `/_my_plan` for phased implementation
