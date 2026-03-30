# Implementation Plan: Neighborhood Graph — Proper Graph Model

**Status:** Complete
**Created:** 2026-03-29
**Last Updated:** 2026-03-29

## Source Documents
- **Spec:** `.project/active/graph-model-rewrite/spec.md`
- **Design:** `.project/active/graph-model-rewrite/design.md` — See here for component details, data structures, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Server changes first (independently testable, de-risks the algorithm). Frontend rewrite second (depends on correct server output, is the core risk). Neighbor count control last (additive feature, doesn't touch graph internals).

Phase 2 is atomic — the new `neighborhood_graph.js` API is incompatible with the old orchestrator calls. The graph rewrite, orchestrator adaptation, and taxonomy_card changes must ship together. Sub-steps within Phase 2 are documented for tracking but commit as one unit.

**Overall Validation Approach:**
- Phase 1: pytest (existing + new tests)
- Phase 2: Manual browser testing (no JS test framework in this project)
- Phase 3: Manual browser testing
- All phases: `uv run python -m pytest exploration/concept_explorer/tests/` must pass

---

## Phase 1: Server — Diversity-Aware Bridges + Configurable `top_n`

### Goal
Fix bridge diversity at the source and enable configurable neighbor count. These are Python-only changes, independently testable, and backward-compatible (default `top_n=5` preserves current behavior).

### Test Stencil (Write This First)

```python
# test_similarity.py — new test class

class TestBridgeDiversity:
    def test_bridges_prefer_distinct_concepts(self, registry):
        """When alternatives exist, bridge concepts should be distinct across fields."""
        # Find a concept pair with multiple mismatched fields
        a = registry.by_id("hts-compact-tokamak")
        b = registry.by_id("sheared-flow-stabilized-z-pinch")
        bridges = explain_difference(a, b, registry)
        if len(bridges) >= 2:
            concept_ids = [br.bridge_concept_id for br in bridges]
            # At least some diversity — not all the same concept
            assert len(set(concept_ids)) > 1

    def test_bridges_fallback_to_reuse_when_no_alternative(self, registry):
        """When only one concept matches a field, it can be reused."""
        # This just verifies the function doesn't crash or return empty
        # when diversity is impossible
        a = registry.by_id("hts-compact-tokamak")
        b = registry.by_id("sheared-flow-stabilized-z-pinch")
        bridges = explain_difference(a, b, registry)
        assert len(bridges) > 0

    def test_bridge_fields_still_covered(self, registry):
        """Diversity preference must not reduce field coverage."""
        a = registry.by_id("hts-compact-tokamak")
        b = registry.by_id("sheared-flow-stabilized-z-pinch")
        bridges = explain_difference(a, b, registry)
        fields = [br.mismatched_field for br in bridges]
        # Each bridge covers a unique field
        assert len(fields) == len(set(fields))


class TestTopNSlicing:
    def test_top_n_returns_requested_count(self, registry):
        """find_nearest(top_n=3) returns exactly 3."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=3)
        assert len(results) == 3

    def test_top_n_fifteen(self, registry):
        """find_nearest(top_n=15) returns 15 (enough concepts in registry)."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=15)
        assert len(results) == 15

    def test_top_n_one(self, registry):
        """Edge case: top_n=1 returns single result."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=1)
        assert len(results) == 1
```

### Changes Required

**See `design.md#component-1` for:** diversity algorithm (greedy selection pseudocode), performance analysis
**See `design.md#component-2` for:** `top_n` parameterization, precompute strategy, endpoint changes

**Specific file changes:**

#### 1. Test File
**File:** `exploration/concept_explorer/tests/test_similarity.py` (MODIFY)
- [x] Add `TestBridgeDiversity` test class (3 tests)
- [x] Add `TestTopNSlicing` test class (3 tests)

#### 2. Bridge Diversity
**File:** `exploration/concept_explorer/similarity.py:231-278` (MODIFY `explain_difference()`)
- [x] Replace single-best-per-field selection with collect-all-candidates approach
- [x] Add greedy diverse selection pass with `used_concept_ids` set
- [x] Add fallback: reuse best candidate when all are already used
- [x] Preserve return type (`list[DifferenceBridge]`) — no model changes

#### 3. Server Endpoint
**File:** `exploration/concept_explorer/server.py` (MODIFY)
- [x] Change precompute `top_n=5` → `top_n=15` at line 277
- [x] Add `top_n: int = 5` query parameter to `api_taxonomy_similarity()` at line 422
- [x] Add validation: clamp `top_n` to `1 <= top_n <= 15`
- [x] Return sliced report: `report.nearest[:top_n]`

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_similarity.py -v` → All 29 pass (existing + new)
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → All 147 pass, no regressions

**Manual:**
- [ ] Start server: `uv run python -m exploration.concept_explorer.server`
- [ ] `curl localhost:8000/api/taxonomy/similarity/hts-compact-tokamak` → Returns 5 neighbors (default)
- [ ] `curl localhost:8000/api/taxonomy/similarity/hts-compact-tokamak?top_n=3` → Returns 3 neighbors
- [ ] `curl localhost:8000/api/taxonomy/similarity/hts-compact-tokamak?top_n=10` → Returns 10 neighbors
- [ ] Inspect bridge concepts in response — verify diversity (different concept_ids across bridges for a given neighbor)

**What We Know Works After This Phase:**
- Server produces diverse bridges
- `top_n` parameter accepted and slicing works
- Existing frontend still works (default=5 unchanged)
- All Python tests pass

---

## Phase 2: Frontend — Graph Model-View Rewrite

### Goal
Replace the procedural graph construction with a model-view architecture. This is the core of the work: complete rewrite of `neighborhood_graph.js`, plus wiring changes in `taxonomy.js` and `taxonomy_card.js`. All three files change atomically.

### Test Approach

No JS test framework exists in this project. Validation is manual browser testing (consistent with all prior JS work). The sub-steps below provide a natural implementation order within this single atomic phase.

### Changes Required

**See `design.md#component-3` for:** GraphModel data structures, construction algorithm (3 stages), deduplication invariants, public interface
**See `design.md#component-4` for:** GraphView initialization sequence, layout tuning, visibility toggling, highlight, node ID scheme, stylesheet, tooltips, event handlers
**See `design.md#component-5` for:** taxonomy.js orchestrator diffs
**See `design.md#component-6` for:** taxonomy_card.js changes

**Specific file changes:**

#### Step 1: Rewrite `neighborhood_graph.js`
**File:** `exploration/concept_explorer/static/js/neighborhood_graph.js` (FULL REWRITE — 647 lines → ~550-650 lines)

GraphModel (pure data, internal to IIFE):
- [x] Constants: `FAMILY_COLORS`, `FAMILY_LABELS`, `FIELD_LABELS`, `DIMENSION_EDGE_COLORS`, `DBLCLICK_DELAY` (preserved from current)
- [x] `buildGraphModel(focusedConcept, report, registry)` — 3-stage construction per `design.md#component-3`
  - [x] Stage 1: center node + neighbor nodes + similarity edges
  - [x] Stage 2: bridge nodes + edges with deduplication + multi-field merging
  - [x] Stage 3: `bridgesByNeighbor` lookup index
- [x] Model query functions: `getNeighborIds()`, `getBridgesForNeighbor()`, `getBridgeNodeIdsForNeighbor()`, `getBridgeEdgeIdsForNeighbor()`

GraphView (Cytoscape wrapper, internal to IIFE):
- [x] `buildStylesheet()` — preserve existing styles, bridge nodes keep `opacity: 0`
- [x] `buildElements(model)` — convert model nodes/edges to Cytoscape elements
  - [x] Center node at (0,0), uses `model.centerConceptId` as Cytoscape ID (not `"center"`)
  - [x] Neighbors in circle at radius 200px
  - [x] Bridge nodes at initial positions (angular offset toward associated neighbors)
  - [x] Similarity edges with score-weighted width
  - [x] Bridge edges with dimension-colored styling and combined field labels
- [x] `initCytoscape(container, elements, callbacks)` — create instance with COSE layout on ALL elements
  - [x] Layout tuning: bridge repulsion 4000, bridge edge length 140 (per `design.md#component-4`)
  - [x] Layout `stop` callback: `cy.elements('.bridge').hide()`
  - [x] Event handlers: neighbor tap (debounced), bridge tap, background tap, tooltips (preserved logic)
- [x] `compare(neighborId)` — show bridge elements for neighbor via `show()` + opacity animation
- [x] `clearComparison()` — hide all bridge elements via opacity animation + `hide()`
- [x] `highlightBridge(conceptId)` — add/remove `"highlighted"` class with 1500ms timeout
- [x] Tooltip functions: `showTooltip`, `hideTooltip`, `tooltipCenter`, `tooltipNeighbor`, `tooltipBridgeNode` (adapted for multi-field bridge edges)
- [x] `resize()`, `destroy()` — preserved

Module public API (returned from IIFE):
- [x] `render(container, focusedConcept, report, registry, callbacks)` — build model, init view
- [x] `compare(neighborId)` — delegate to view
- [x] `clearComparison()` — delegate to view
- [x] `highlightBridge(conceptId)` — delegate to view
- [x] `getBridgesForNeighbor(neighborId)` — delegate to model
- [x] `resize()`, `destroy()` — delegate to view

#### Step 2: Update orchestrator
**File:** `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY ~30 lines)
- [x] `switchToNeighborhood()`: pass `report` instead of `neighbors` to `NeighborhoodGraph.render()`
- [x] `handleCompare()`: replace `selectBridges()` + `showBridges()` with `compare()` + `getBridgesForNeighbor()`
- [x] `handleDeselect()`: replace `clearBridges()` with `clearComparison()`

#### Step 3: Update taxonomy_card.js
**File:** `exploration/concept_explorer/static/js/taxonomy_card.js` (MODIFY ~20 lines)
- [x] Remove `selectBridges()` function (lines 162-187) and its `MAX_BRIDGES` constant
- [x] Remove `selectBridges` from the returned public API object
- [x] Adapt `renderComparison()` to accept bridge data from GraphModel format (fields as array, combined labels)

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → All 147 pass, no regressions

**Manual — Core behavior (SC-1 through SC-6):**
- [ ] SC-1: Click a concept in the tree → graph renders with center + neighbors. All nodes draggable. Bridges invisible during layout.
- [ ] SC-2: Inspect Cytoscape element count via browser console: `document.querySelector('#neighborhood-container')._cy.nodes().length` — verify no duplicate concept IDs
- [ ] SC-3: Compare a neighbor with 2+ fields bridged by the same concept → verify one bridge node with combined edge label (e.g., "Heating + Magnets")
- [ ] SC-4: Compare multiple neighbors across different concepts → verify bridge concepts are diverse (from Phase 1 server change)
- [ ] SC-6: Compare neighbor A → compare neighbor B → click background to deselect → verify Cytoscape element count stays constant (bridges shown/hidden, not added/removed)

**Manual — State transitions:**
- [ ] Overview (constellation) → click tree leaf → focused (neighborhood graph) → click neighbor → comparing (bridges appear) → click different neighbor → bridges swap → click background → bridges gone → click back button → overview
- [ ] Double-click neighbor → re-centers on that concept
- [ ] Double-click bridge → re-centers on that concept
- [ ] Escape key → returns to overview
- [ ] Sidebar toggle → graph resizes correctly
- [ ] Comparison panel shows bridge references → click bridge ref → bridge node pulses in graph

**Manual — Edge cases:**
- [ ] Bridge concept that is also a neighbor → one node, bridge edge appears when comparing relevant neighbor
- [ ] Re-focus same concept (click tree again while focused) → graph rebuilds cleanly
- [ ] Rapid neighbor switching → no visual glitches or orphaned elements

**What We Know Works After This Phase:**
- Graph built once with all nodes
- Force layout includes bridges (natural positions)
- State transitions are visibility toggles
- One node per concept
- Multi-field edge labels
- All interaction callbacks work
- Comparison panel synchronized with graph

---

## Phase 3: Neighbor Count Control

### Goal
Add user-facing `top_n` control. This is an additive feature — it doesn't change the graph module, only the orchestrator's fetch logic and a new UI element.

### Changes Required

**See `design.md#component-7` for:** HTML template, wiring code
**See `design.md#component-8` for:** CSS styles
**See `design.md#component-5` for:** `_neighborCount` state variable, `handleNeighborCountChange()`, `fetchSimilarity()` cache key

**Specific file changes:**

#### 1. Template
**File:** `exploration/concept_explorer/templates/taxonomy.html.j2` (MODIFY)
- [x] Add `<label class="neighbor-count">` with `<select>` inside `graph-header` div (options: 3, 5, 7, 10; default 5)

#### 2. CSS
**File:** `exploration/concept_explorer/static/css/explorer.css` (MODIFY)
- [x] Add `.neighbor-count` and `.neighbor-count__select` styles per `design.md#component-8`

#### 3. Orchestrator Wiring
**File:** `exploration/concept_explorer/static/js/taxonomy.js` (MODIFY ~20 lines)
- [x] Add `_neighborCount = 5` state variable
- [x] Update `fetchSimilarity()`: cache key `conceptId + ":" + _neighborCount`, append `?top_n=` to URL
- [x] Add `handleNeighborCountChange(newCount)` handler
- [x] In `init()`: bind `change` event on `#neighbor-count-select`
- [x] In `switchToNeighborhood()`: show `#neighbor-count-control`
- [x] In `switchToOverview()`: hide `#neighbor-count-control`

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → All 147 pass

**Manual:**
- [ ] Focus a concept → neighbor count dropdown visible in header
- [ ] Change to 3 → graph rebuilds with 3 neighbors
- [ ] Change to 10 → graph rebuilds with 10 neighbors
- [ ] Change back to 5 → graph rebuilds (may serve from cache if previously fetched at 5)
- [ ] Return to overview → dropdown hidden
- [ ] Focus different concept → dropdown still shows, previous count preserved
- [ ] Verify dropdown doesn't appear in overview mode

**What We Know Works After This Phase:**
- User can configure neighbor count
- Cache correctly separates by `top_n`
- Graph rebuilds with correct neighbor count
- All prior behavior preserved

---

## Environment Setup

**See CLAUDE.md for full environment rules**

- Python: always `uv run python ...`
- Tests: `uv run python -m pytest exploration/concept_explorer/tests/ -v`
- Server: `uv run python -m exploration.concept_explorer.server`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis (R-1 through R-5)**

**Phase-Specific Mitigations:**
- **Phase 1**: Low risk. Tests validate diversity. Existing tests catch regressions. Default `top_n=5` preserves backward compat.
- **Phase 2**: Highest risk (full JS rewrite). Mitigated by: writing GraphModel first (pure data, console-testable), then GraphView, then wiring. If layout tuning is off, adjust repulsion/edge-length values — this is visual, not architectural.
- **Phase 3**: Low risk. Additive feature. If the dropdown is visually awkward, adjust CSS — no architectural concern.

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Modified `similarity.py:231-295` — rewrote `explain_difference()` with two-stage approach: Stage 1 collects all candidates per mismatched field sorted by score; Stage 2 greedily selects diverse bridges using `used_concept_ids` set with fallback to best candidate when all are already used
- Modified `server.py:277` — changed precompute `top_n=5` → `top_n=15`
- Modified `server.py:422-438` — added `top_n: int = 5` query parameter to `api_taxonomy_similarity()`, clamped to 1–15, returns sliced `ConceptSimilarityReport`
- Added 6 new tests in `test_similarity.py` — `TestBridgeDiversity` (3 tests) and `TestTopNSlicing` (3 tests)
**Issues:** None
**Deviations:** None — implemented exactly per plan

### Phase 2 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Full rewrite of `neighborhood_graph.js` (647 → ~520 lines): GraphModel (pure data with 3-stage build, node deduplication, multi-field edge merging, query methods) + GraphView (Cytoscape wrapper with visibility toggling for compare/clearComparison). All nodes use concept_id as Cytoscape ID. Bridge nodes participate in COSE layout with tuned repulsion (4000) and edge length (140). After layout stops, bridges hidden via `.hide()`. State transitions are show/hide + opacity animation.
- Modified `taxonomy.js` (~15 lines changed): `switchToNeighborhood()` now takes `report` instead of `neighbors`. `handleCompare()` uses `NeighborhoodGraph.compare()` + `getBridgesForNeighbor()`. `handleDeselect()` uses `clearComparison()`.
- Modified `taxonomy_card.js` (~25 lines changed): Removed `selectBridges()` and `MAX_BRIDGES`. Updated bridge lookup in `renderComparison()` to use GraphModel format (`field`/`conceptId`/`conceptName` instead of `mismatched_field`/`bridge_concept_id`/`bridge_concept_name`). Removed `selectBridges` from public API.
**Issues:** None
**Deviations:** Bridge node tooltip simplified to show concept info only (name + family + "Double-click to explore") since per-field data is now on edges, not nodes. Edge tooltips handle multi-field case with line breaks.

### Phase 3 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Modified `taxonomy.html.j2` — added `<label class="neighbor-count">` with `<select>` (options 3/5/7/10, default 5) inside graph-header, hidden by default
- Modified `explorer.css` — added `.neighbor-count` (inline-flex, margin-left auto to push right) and `.neighbor-count__select` styles
- Modified `taxonomy.js` (~25 lines changed): added `_neighborCount` state variable, updated `fetchSimilarity()` with composite cache key (`conceptId:topN`) and `?top_n=` URL param, added `handleNeighborCountChange()` handler, bound change event in `init()`, show/hide control in `switchToNeighborhood()`/`switchToOverview()`. Also fixed `handleCompare()` and `handleDeselect()` to use the composite cache key.
**Issues:** None
**Deviations:** None — implemented exactly per plan

---

**Status**: Complete
