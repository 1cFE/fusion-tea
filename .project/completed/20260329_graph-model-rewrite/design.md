# Design: Neighborhood Graph — Proper Graph Model

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29
**Updated:** 2026-03-29
**Branch:** ralph/concept-explorer
**Base Commit:** d904f0a

---

## Overview

Replace the procedural graph construction (build center+neighbors, then bolt on bridges as position-locked overlays) with a model-view architecture: a **GraphModel** data structure built once from the full similarity report, a **GraphView** that renders the complete graph via Cytoscape and toggles visibility for state transitions, and a diversity-aware bridge selection algorithm on the server. All nodes participate in the initial force layout. State transitions are visibility changes, not DOM mutations.

## Related Artifacts

- **Spec:** `.project/active/graph-model-rewrite/spec.md`
- **Prior design work:** `.project/active/taxonomy-viz-redesign/` (visual polish, separate concern)
- **Current graph:** `exploration/concept_explorer/static/js/neighborhood_graph.js` (647 lines, rewritten entirely)
- **Orchestrator:** `exploration/concept_explorer/static/js/taxonomy.js` (347 lines, modified)
- **Bridge selection:** `exploration/concept_explorer/static/js/taxonomy_card.js:168` (`selectBridges()`, removed)
- **Similarity engine:** `exploration/concept_explorer/similarity.py:231` (`explain_difference()`, modified)
- **Server endpoint:** `exploration/concept_explorer/server.py:422` (similarity API, modified)
- **Template:** `exploration/concept_explorer/templates/taxonomy.html.j2` (neighbor count control added)
- **Tests:** `exploration/concept_explorer/tests/test_similarity.py` (new tests added)

## Research Findings

### Current Architecture Problems

The existing `neighborhood_graph.js` has three structural defects that all stem from one design mistake: the graph is treated as a rendering surface rather than a data structure.

**1. Bridge nodes are position-locked overlays (lines 524-538)**

`showBridges()` computes geometric positions perpendicular to the center-neighbor line (angle offsets at 1.4x the center-neighbor distance), then inserts new nodes with `locked: true`. These nodes don't participate in the force simulation. They sit at computed coordinates and feel artificial.

**2. Duplicate nodes for the same concept (line 521)**

Bridge node IDs include an index suffix: `"b-" + bridge.bridge_concept_id + "-" + i`. If concept X bridges two mismatched fields for the same neighbor, it gets two nodes (`b-X-0`, `b-X-1`) at two different positions.

**3. Bridge selection lacks diversity (similarity.py:251-263)**

`explain_difference()` independently selects the best bridge per mismatched field. If concept X has the highest overall similarity and matches the query on fields A, B, and C, it wins all three — producing three identical bridge nodes. The client-side `selectBridges()` (`taxonomy_card.js:168-187`) deduplicates by field but not by concept.

**4. State transitions are DOM mutations (lines 486-584)**

`showBridges()` calls `_cy.add()` to insert new elements. `clearBridges()` calls `.remove()`. Switching neighbors means: remove all bridge DOM, recompute positions, insert new DOM, animate opacity. This is expensive, fragile, and prevents the graph from knowing about its full topology.

### Existing Patterns Worth Preserving

- **IIFE module pattern**: All JS modules use `var X = (function() { ... return { ... }; })()`. Stay consistent.
- **Cytoscape COSE layout**: The force-directed configuration (repulsion 8000, edge length 180, gravity 0.25, 200 iterations) produces good results for center+neighbor topology. Needs re-tuning with bridge nodes added.
- **Tooltip system**: `showTooltip()/hideTooltip()` with smart edge-of-screen repositioning works well.
- **Double-click debounce**: 300ms timer distinguishing single-click (compare) from double-click (focus). Reuse as-is.
- **Stylesheet structure**: The Cytoscape CSS rules for node types, edge types, and interaction states (`.comparing`, `.highlighted`) are well-organized.
- **State machine in taxonomy.js**: The OVERVIEW/FOCUSED/COMPARING state machine (lines 6-17) is correct. The new graph doesn't change the state machine — it changes how COMPARING is implemented.

### API Response Structure

The similarity API (`/api/taxonomy/similarity/{id}`) returns everything needed to build the complete graph in one response:

```json
{
  "query_concept_id": "...",
  "nearest": [
    {
      "concept_id": "...",
      "comparison": { "overall_score": 0.75, ... },
      "bridges": [
        {
          "dimension": "engineering",
          "mismatched_field": "magnet_type",
          "query_value": "HTS (wound)",
          "similar_value": "Self-confined",
          "bridge_concept_id": "...",
          "bridge_concept_name": "...",
          "bridge_overall_similarity": 0.65
        }
      ]
    }
  ]
}
```

Each neighbor already carries its bridge data. The current code ignores this until `handleCompare()` — the new design uses it immediately at construction time.

### Server-Side Bridge Selection (similarity.py:231-278)

`explain_difference()` iterates all mismatched fields and for each field, scans the entire registry for the best matching candidate (highest overall similarity). Each field's selection is independent — no cross-field coordination. This is where diversity must be enforced.

### Precomputed vs. Dynamic Similarity (server.py:274-282)

Similarity reports are precomputed at startup with `top_n=5` hardcoded. To support configurable neighbor count (FR-7/FR-8), this needs to change: either precompute with a generous max and slice, or compute on-demand.

Given 38 concepts and trivial `compare_pair()` cost, precomputing with `top_n=15` and slicing to the requested count is both fast and avoids per-request computation.

---

## Proposed Design

### Architecture Overview

Three layers, each with a single responsibility:

```
                +-----------------------+
                |   taxonomy.js         |  CONTROLLER
                |   State machine       |  Owns app state, delegates to model+view
                |   Event routing       |
                +-----------+-----------+
                            |
              +-------------+-------------+
              |                           |
  +-----------v-----------+   +-----------v-----------+
  |   GraphModel          |   |   GraphView           |  MODEL / VIEW
  |   Pure data structure  |   |   Cytoscape wrapper   |
  |   Node/edge registry  |   |   Visibility toggling  |
  |   Deduplication       |   |   Event handlers       |
  |   Multi-field merging |   |   Tooltips             |
  +-----------------------+   +-----------------------+
```

- **GraphModel**: Built once from the similarity report. Contains all nodes (center, neighbors, bridges — deduplicated) and all edges (similarity, bridge — with multi-field labels merged). Pure data, no Cytoscape dependency. Queryable: "give me bridges for neighbor X."
- **GraphView**: Owns the Cytoscape instance. Renders all elements from the model. After initial layout settles, hides bridge elements. Exposes `compare(neighborId)` → show bridges, `clearComparison()` → hide bridges. Handles interaction events (click, tooltip, drag).
- **taxonomy.js**: Unchanged state machine (OVERVIEW/FOCUSED/COMPARING). Calls `NeighborhoodGraph.render(container, concept, report, registry, callbacks)` once, then `NeighborhoodGraph.compare(neighborId)` and `NeighborhoodGraph.clearComparison()` for state transitions. Also manages the neighbor count control.

### Component 1: Server — Diversity-Aware Bridge Selection

**File:** `exploration/concept_explorer/similarity.py`
**Function:** `explain_difference()` (lines 231-278)

**Change:** Replace independent per-field best-bridge selection with greedy diverse selection.

**Algorithm:**

```
1. For each mismatched field:
     Collect ALL candidates that match the query on that field
     Sort by overall similarity (descending)
   → candidates_by_field: { field: [(score, concept), ...] }

2. Greedy selection (iterate fields in dimension order):
   used_concept_ids = set()

   For each field:
     For each candidate in candidates_by_field[field]:
       If candidate.concept_id NOT in used_concept_ids:
         Select this candidate as bridge
         Add to used_concept_ids
         Break
     Else (all candidates already used):
       Select the highest-scoring candidate anyway (fallback)
```

**Why greedy works:** Fields typically have 5-15 matching candidates each. The greedy pass produces diverse bridges in the common case. Only when the pool is genuinely exhausted (rare — 38 concepts) does it fall back to reuse.

**Data model unchanged:** The `DifferenceBridge` Pydantic model stays the same. The change is internal to the selection algorithm.

**Performance:** Trivially fast. 38 concepts, ~5 fields, `compare_pair()` is attribute comparison. The extra work (collecting all candidates instead of tracking just the best) is negligible.

### Component 2: Server — Configurable `top_n`

**File:** `exploration/concept_explorer/server.py`

**Changes:**

1. **Precompute with generous max** (line 277): Change `top_n=5` to `top_n=15` in `_load_taxonomy()`. This precomputes bridges for the top 15 neighbors of each concept.

2. **Add query parameter** to similarity endpoint (line 422):
   ```python
   def api_taxonomy_similarity(
       concept_id: str,
       top_n: int = 5,
       state: _State = Depends(get_state),
   ) -> ConceptSimilarityReport:
       report = state.similarity_reports.get(concept_id)
       if report is None:
           raise HTTPException(status_code=404, ...)
       # Slice to requested count
       sliced = ConceptSimilarityReport(
           query_concept_id=report.query_concept_id,
           query_concept_name=report.query_concept_name,
           nearest=report.nearest[:top_n],
       )
       return sliced
   ```

3. **Clamp `top_n`**: Validate that `1 <= top_n <= 15` (or the precomputed max). Return 422 for out-of-range values.

**Why precompute+slice over on-demand:** Zero per-request computation cost. The startup cost increase is ~3x (15 vs 5 neighbors, each with `explain_difference()`), but for 38 concepts this is still under a second.

### Component 3: GraphModel — Pure Data Structure

**File:** `exploration/concept_explorer/static/js/neighborhood_graph.js` (new, complete rewrite)

The GraphModel holds the complete topology of the neighborhood graph. It is built once from the similarity report and never mutated.

**Implementation note:** All pseudocode in this design uses constructor/prototype syntax for clarity. The actual implementation MUST use the IIFE+closure pattern consistent with every other JS module in this codebase (e.g., `var NeighborhoodGraph = (function() { ... return { render: render, ... }; })();`). GraphModel and GraphView are internal concerns — closured functions, not exported constructors.

**Data structures:**

```javascript
// NodeData — one per unique concept in the graph
{
  id: string,            // concept_id (unique key)
  type: "center" | "neighbor" | "bridge",
  label: string,         // concept name
  family: string,        // confinement_family
  concept: object,       // full concept from registry (for tooltips)
  score: number | null,  // overall_score (neighbors only)
  bridgeForNeighbors: string[]  // neighbor IDs this node bridges for (bridges only)
}

// EdgeData — one per unique relationship
{
  id: string,            // "sim:{targetId}" or "br:{neighborId}:{bridgeId}"
  type: "similarity" | "bridge",
  source: string,        // concept_id
  target: string,        // concept_id
  // Similarity edges:
  score: number,
  matches: number,
  comparable: number,
  // Bridge edges:
  neighborId: string,    // which neighbor comparison this edge belongs to
  fields: string[],      // ["magnet_type"] or ["primary_heating", "magnet_type"]
  dimension: string,     // primary dimension (for edge color — see note below)
  queryValue: string     // shared value (for tooltip)
}
```

**Construction: `GraphModel.build(focusedConcept, report, registry)`**

The build process has three stages:

**Stage 1 — Add center + neighbors:**
```
For each neighbor in report.nearest:
  Add neighbor node (type: "neighbor", score from comparison)
  Add similarity edge (center → neighbor)
```

**Stage 2 — Add bridge nodes + edges with deduplication:**
```
For each neighbor in report.nearest:
  For each bridge in neighbor.bridges:
    bridgeConceptId = bridge.bridge_concept_id

    IF node already exists for bridgeConceptId:
      // Concept is already a neighbor or a bridge for another neighbor
      // Don't create a second node
      IF existing node is type "bridge":
        Append this neighborId to existing node.bridgeForNeighbors
    ELSE:
      Create bridge node (type: "bridge", bridgeForNeighbors: [neighborId])

    edgeKey = "br:" + neighborId + ":" + bridgeConceptId
    IF edge already exists for edgeKey:
      // Same concept bridges multiple fields for the same neighbor
      Append field to existing edge.fields  (→ SC-3: multi-field labels)
    ELSE:
      Create bridge edge (center → bridgeConceptId, neighborId, fields: [field])
```

**Stage 3 — Build lookup indices:**
```
bridgesByNeighbor: { neighborId → [{ bridgeNode, bridgeEdge, fields, ... }] }
```

This lookup allows `getBridgesForNeighbor(neighborId)` to return bridge information for the comparison panel without re-scanning the edge list.

**Key invariants:**
- Exactly one node per concept_id (SC-2)
- If a concept is both a neighbor and a bridge, it exists as one node with type "neighbor" (always visible) and has additional bridge edges (visible when comparing)
- Multi-field bridge edges carry combined labels: `fields.map(f => FIELD_LABELS[f]).join(" + ")` (SC-3)
- When a bridge edge spans fields from different dimensions (e.g., `primary_heating` from `plasma_physics` and `magnet_type` from `engineering`), the edge color uses the **first field's dimension** — fields iterate in dimension order during the greedy selection, so the first field is from the highest-priority dimension
- A bridge node that serves multiple neighbors has all neighbor IDs in `bridgeForNeighbors`

**Public interface:**

```javascript
GraphModel.build(focusedConcept, report, registry) → GraphModel

model.centerConceptId        // string
model.nodes                  // { conceptId: NodeData }
model.edges                  // { edgeKey: EdgeData }
model.getNeighborIds()       // string[] — all neighbor concept IDs
model.getBridgesForNeighbor(neighborId) → [BridgeInfo]
  // Returns: [{ conceptId, conceptName, fields, dimension, queryValue, similarValue }]
  // Used by the comparison panel to render bridge references
model.getBridgeNodeIdsForNeighbor(neighborId) → string[]
  // Returns concept IDs of bridge nodes that should be visible when comparing this neighbor
model.getBridgeEdgeIdsForNeighbor(neighborId) → string[]
  // Returns edge keys that should be visible when comparing this neighbor
```

### Component 4: GraphView — Cytoscape Rendering + Visibility

**File:** `exploration/concept_explorer/static/js/neighborhood_graph.js` (same file as GraphModel)

The GraphView owns the Cytoscape instance and translates model data into Cytoscape elements. It manages visibility state (which bridges are shown) and interaction events.

**Initialization sequence:**

```
1. Convert GraphModel nodes → Cytoscape node elements
   - Center node at (0,0)
   - Neighbors in circle (radius 200px, evenly distributed)
   - Bridge nodes at computed initial positions (see below)

2. Convert GraphModel edges → Cytoscape edge elements
   - Similarity edges: visible, styled by score
   - Bridge edges: start with opacity: 0 (from stylesheet)

3. Create Cytoscape instance with COSE layout on ALL elements
   - Bridge nodes participate in the force simulation
   - They find natural positions based on their connections to center

4. After layout stops (layout 'stop' event):
   - Hide all bridge nodes and edges: cy.elements('.bridge').hide()
   - Bridge positions are now force-computed and remembered by Cytoscape

5. Register event handlers (tap, mouseover, etc.)
```

**Why include bridges in the initial layout (FR-3, SC-1):**

The current code positions bridges geometrically (angular offsets perpendicular to center-neighbor line). This produces artificial positions. By including bridges in the COSE force simulation:
- Bridge nodes find natural positions based on their topology (connected to center)
- They are influenced by node repulsion from neighbors and other bridges
- The result looks organic rather than computed

Since bridges start with `opacity: 0` in the stylesheet (carried over from the current design), users see only center + neighbors during the layout animation. Bridges are invisible but being positioned by physics.

**Bridge initial positions:**

For the COSE layout, bridge nodes need initial positions (COSE uses them as starting points for the simulation, `randomize: false`). Use the angular offset strategy from the current code:

```javascript
// Position bridge nodes initially between center and the midpoint of their associated neighbors
// This gives COSE a good starting position to converge from
var neighborPositions = getAverageNeighborPosition(node.bridgeForNeighbors);
var angle = Math.atan2(neighborPositions.y, neighborPositions.x);
var distance = 160; // slightly inside the neighbor ring
position = { x: distance * Math.cos(angle), y: distance * Math.sin(angle) };
```

**Layout tuning:**

Adding ~10-15 bridge nodes to the 6 existing nodes requires re-tuning:

```javascript
layout: {
  name: "cose",
  animate: true,
  animationDuration: 500,
  fit: true,
  padding: 50,
  nodeRepulsion: function(node) {
    // Lower repulsion for bridge nodes so they don't push neighbors out
    return node.hasClass("bridge") ? 4000 : 8000;
  },
  idealEdgeLength: function(edge) {
    // Bridge edges slightly shorter — bridges sit closer to center than neighbors
    return edge.hasClass("bridge") ? 140 : 180;
  },
  edgeElasticity: function() { return 100; },
  gravity: 0.25,
  numIter: 200,
  initialTemp: 200,
  coolingFactor: 0.95,
  randomize: false
}
```

Bridge nodes get lower repulsion (4000 vs 8000) so they cluster closer to center without pushing neighbors outward. Bridge edges get shorter ideal length (140 vs 180) to keep bridges inside the neighbor ring.

**Visibility toggling — `compare(neighborId)`:**

```javascript
GraphView.prototype.compare = function(neighborId) {
  var cy = this._cy;

  // 1. Hide any previously visible bridges (instant, no animation)
  cy.elements(".bridge").hide().style("opacity", 0);
  cy.nodes(".comparing").removeClass("comparing");

  // 2. Highlight the compared neighbor
  cy.getElementById(neighborId).addClass("comparing");

  // 3. Show bridge elements for this neighbor
  var bridgeNodeIds = this._model.getBridgeNodeIdsForNeighbor(neighborId);
  var bridgeEdgeIds = this._model.getBridgeEdgeIdsForNeighbor(neighborId);

  for (var i = 0; i < bridgeNodeIds.length; i++) {
    var node = cy.getElementById(bridgeNodeIds[i]);
    if (!node.empty()) {
      node.show();
      node.animate({ style: { opacity: 1 } }, { duration: 250 });
    }
  }
  for (var i = 0; i < bridgeEdgeIds.length; i++) {
    var edge = cy.getElementById(bridgeEdgeIds[i]);
    if (!edge.empty()) {
      edge.show();
      edge.animate({ style: { opacity: 1 } }, { duration: 250 });
    }
  }

  this._activeNeighborId = neighborId;
};
```

**Visibility toggling — `clearComparison()`:**

```javascript
GraphView.prototype.clearComparison = function() {
  if (!this._activeNeighborId) return;
  var cy = this._cy;

  cy.nodes(".comparing").removeClass("comparing");

  // Fade out, then hide
  var bridges = cy.elements(".bridge").filter(":visible");
  bridges.animate(
    { style: { opacity: 0 } },
    { duration: 200, complete: function() { bridges.hide(); } }
  );

  this._activeNeighborId = null;
};
```

**Bridge highlight — `highlightBridge(conceptId)`:**

Preserved from the current API. Called from the comparison panel's bridge-ref clicks (via `taxonomy.js:handleBridgeHighlight()`). Adds a `"highlighted"` class to the bridge node, which triggers the existing stylesheet rule (3px white border + overlay glow), then removes the class after 1500ms.

```javascript
function highlightBridge(conceptId) {
  if (!_cy) return;
  var node = _cy.getElementById(conceptId);
  if (node.empty()) return;
  node.addClass("highlighted");
  setTimeout(function() { node.removeClass("highlighted"); }, 1500);
}
```

With deduplicated node IDs (concept_id directly), this is simpler than the current code which has to filter by `data("conceptId")` across multiple index-suffixed bridge nodes.

**Node ID scheme:**

All nodes use the concept_id directly as their Cytoscape node ID. This is the key deduplication mechanism — a concept that is both a neighbor and a bridge is one Cytoscape node.

**Breaking change from current code:** The center node ID changes from the string `"center"` to the focused concept's `concept_id`. This is necessary for deduplication (a bridge could theoretically share an ID with a hardcoded string, and the uniform scheme is cleaner). The implementer must replace all `_cy.getElementById("center")` references with `_cy.getElementById(model.centerConceptId)` — there are at least 2 in the current `showBridges()` (lines 497-498).

```
Center:    concept_id                    (e.g., "hts-compact-tokamak")
Neighbor:  concept_id                    (e.g., "qi-stellarator-hts")
Bridge:    concept_id                    (e.g., "large-scale-stellarator")
```

Edge IDs:
```
Similarity: "sim:" + neighborConceptId   (e.g., "sim:qi-stellarator-hts")
Bridge:     "br:" + neighborId + ":" + bridgeConceptId
            (e.g., "br:qi-stellarator-hts:large-scale-stellarator")
```

**Stylesheet changes:**

The stylesheet structure stays the same (center/neighbor/bridge node styles, similarity/bridge edge styles). One change: bridge nodes no longer need `locked: true` positioning logic — they participate in the layout. The `opacity: 0` initial style for bridges is preserved.

**Tooltip changes:**

Bridge tooltips need updating for multi-field edges. Currently: "Shares {field}: {value}". New: "Shares {field1} + {field2}: {value1}, {value2}" or similar.

**Event handlers:**

Unchanged from the current code: single-click neighbor → `callbacks.onCompare()`, double-click → `callbacks.onFocus()`, background click → `callbacks.onDeselect()`, bridge double-click → `callbacks.onFocus()`. The 300ms debounce pattern is preserved.

### Component 5: Orchestrator Changes (taxonomy.js)

**File:** `exploration/concept_explorer/static/js/taxonomy.js`

**Changes are minimal** — the state machine is unchanged. Only the calls to NeighborhoodGraph change:

**`switchToNeighborhood()` (line 189):**

```diff
- NeighborhoodGraph.render(neighborhoodContainer, concept, neighbors, _registry, {
+ NeighborhoodGraph.render(neighborhoodContainer, concept, report, _registry, {
    onCompare: handleCompare,
    onFocus: handleFocus,
    onDeselect: handleDeselect
  });
```

Pass the full `report` instead of just `neighbors`. The GraphModel needs bridge data from `report.nearest[i].bridges`.

**`handleCompare()` (line 281):**

```diff
  // Select bridges (up to 3, one per field, by similarity)
- var bridges = TaxonomyCards.selectBridges(result.bridges);
-
- // Update graph: show bridge nodes + highlight neighbor
- NeighborhoodGraph.showBridges(neighborId, bridges);
+ // Show bridge nodes for this neighbor (visibility toggle)
+ NeighborhoodGraph.compare(neighborId);
+
+ // Get bridge data from the graph model for the comparison panel
+ var bridges = NeighborhoodGraph.getBridgesForNeighbor(neighborId);

  // Update detail panel: comparison table
  TaxonomyCards.renderComparison(
    comparisonContainer, focused, neighbor, result,
    bridges, report.nearest, handleBridgeHighlight, handleCompare
  );
```

**`handleDeselect()` (line 325):**

```diff
- NeighborhoodGraph.clearBridges();
+ NeighborhoodGraph.clearComparison();
```

**`fetchSimilarity()` (line 218):**

Add `top_n` parameter to the API call:

```javascript
function fetchSimilarity(conceptId) {
  var cacheKey = conceptId + ":" + _neighborCount;
  if (_similarityCache[cacheKey]) {
    return Promise.resolve(_similarityCache[cacheKey]);
  }
  var url = "/api/taxonomy/similarity/" + encodeURIComponent(conceptId)
    + "?top_n=" + _neighborCount;
  return fetch(url)
    .then(function (resp) { ... })
    .then(function (report) {
      _similarityCache[cacheKey] = report;
      return report;
    });
}
```

**New state variable:**

```javascript
var _neighborCount = 5;  // default, user-configurable
```

**Neighbor count change handler:**

```javascript
function handleNeighborCountChange(newCount) {
  _neighborCount = newCount;
  // Re-focus triggers fetchSimilarity with new cache key (conceptId:topN)
  // so no manual invalidation needed — cache naturally separates by count
  if (_focusedId) {
    handleFocus(_focusedId);  // re-fetch (if not cached at this count) + rebuild graph
  }
}
```

### Component 6: taxonomy_card.js Changes

**File:** `exploration/concept_explorer/static/js/taxonomy_card.js`

**Remove `selectBridges()`** — bridge selection and deduplication is now handled by the GraphModel at construction time. The orchestrator calls `NeighborhoodGraph.getBridgesForNeighbor()` instead.

**Adapt `renderComparison()`** — the `selectedBridges` parameter now comes from the GraphModel's bridge info (which already has multi-field merging done). The comparison table shows the combined field labels.

**Bridge panel rendering change:** When a bridge covers multiple fields, the comparison table shows the bridge once with combined field label rather than once per field. This matches what the graph shows (one node, one multi-label edge).

### Component 7: Neighbor Count UI Control

**File:** `exploration/concept_explorer/templates/taxonomy.html.j2`

Add a control in the graph header bar (line 28-38), visible only in neighborhood mode:

```html
<div class="graph-header" id="graph-header">
  <button class="graph-header__back" id="back-to-overview" ...>...</button>
  <span class="graph-header__title" id="graph-title">...</span>
  <span class="graph-header__subtitle" id="graph-subtitle">...</span>
  <label class="neighbor-count" id="neighbor-count-control" style="display:none">
    <span class="neighbor-count__label">Neighbors</span>
    <select class="neighbor-count__select" id="neighbor-count-select">
      <option value="3">3</option>
      <option value="5" selected>5</option>
      <option value="7">7</option>
      <option value="10">10</option>
    </select>
  </label>
</div>
```

The control is a `<select>` dropdown — minimal, doesn't command attention, always accessible. Shown when in neighborhood mode, hidden in overview.

**Wired up in taxonomy.js:**

```javascript
// In init():
var neighborCountSelect = document.getElementById("neighbor-count-select");
neighborCountSelect.addEventListener("change", function() {
  handleNeighborCountChange(parseInt(this.value, 10));
});

// In switchToNeighborhood():
document.getElementById("neighbor-count-control").style.display = "";

// In switchToOverview():
document.getElementById("neighbor-count-control").style.display = "none";
```

### Component 8: CSS additions

**File:** `exploration/concept_explorer/static/css/explorer.css`

Minimal additions for the neighbor count control:

```css
.neighbor-count {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  margin-left: auto;  /* push to right of header */
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
.neighbor-count__select {
  background: var(--color-surface-2);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 2px var(--space-1);
  font-size: var(--font-size-sm);
}
```

---

## Potential Risks

### R-1: Layout Density with Bridge Nodes

Adding ~10-15 bridge nodes to a 6-node graph changes the force layout dynamics. The mitigations (lower bridge repulsion, shorter bridge edge length) should keep bridges inside the neighbor ring, but the exact tuning values may need iteration once the code is running. This is a visual tuning exercise, not an architectural risk.

### R-2: Cache Invalidation on Neighbor Count Change

When the user changes the neighbor count, cached similarity reports for other `top_n` values become stale. **Decision:** Key the cache on `conceptId + ":" + topN`. Different counts produce different cache entries. Memory cost is negligible (a few KB per entry). This avoids unnecessary re-fetches when toggling between previously visited concepts at different neighbor counts.

### R-3: Bridge Node Visibility When Also a Neighbor

If concept X is both a neighbor and a bridge for another neighbor, its node is always visible (it's a neighbor). When comparing, bridge edges to X appear — but X doesn't "pop in" because it was already there. This might be slightly confusing visually (a neighbor suddenly sprouts a dashed bridge edge). Mitigation: the bridge edge animates in with opacity fade, making it clear that the new connection appeared.

### R-4: `explain_difference()` Performance with Diversity

The diversity algorithm collects ALL candidates per field before selecting, rather than tracking just the best. This means every candidate for every field gets scored. With 38 concepts and ~5 fields, that's ~190 `compare_pair()` calls per neighbor comparison. Currently it's the same count (the loop doesn't short-circuit). No performance impact.

### R-5: Precomputing `top_n=15` at Startup

Currently precomputing with `top_n=5`: 38 concepts x 5 neighbors x `explain_difference()` each. With `top_n=15`: 38 x 15 = 570 `explain_difference()` calls. Each call scans ~38 candidates per ~5 fields = ~190 `compare_pair()` calls. Total: ~108K pair comparisons. `compare_pair()` is attribute string comparison — this is still well under a second on any hardware.

---

## Integration Strategy

### Execution Order

Changes can be implemented in this sequence (each builds on the previous):

1. **Server: diversity-aware `explain_difference()`** — Python change, testable independently
2. **Server: `top_n` parameterization** — Python change, backward-compatible (default=5)
3. **JS: GraphModel + GraphView** — Complete rewrite of `neighborhood_graph.js`
4. **JS: taxonomy.js orchestrator** — Adapt calls to new NeighborhoodGraph API
5. **JS: taxonomy_card.js** — Remove `selectBridges()`, adapt bridge data format
6. **HTML/CSS: neighbor count control** — Template + styling

Steps 1-2 are independent of steps 3-6. Steps 3-5 form one atomic change (the old API and new API are incompatible). Step 6 is a small addition after the JS changes.

### What Gets Replaced vs. Modified

| File | Change Type | Scope |
|------|-------------|-------|
| `similarity.py` | Modify | `explain_difference()` only (~50 lines) |
| `server.py` | Modify | Similarity endpoint + precompute (~15 lines) |
| `neighborhood_graph.js` | **Full rewrite** | 647 lines → ~550-650 lines |
| `taxonomy.js` | Modify | ~30 lines changed (API calls, new state var, event binding) |
| `taxonomy_card.js` | Modify | Remove `selectBridges()`, minor adapt (~20 lines) |
| `taxonomy.html.j2` | Modify | Add neighbor count control (~8 lines) |
| `explorer.css` | Modify | Add neighbor count styles (~15 lines) |
| `test_similarity.py` | Add tests | New test class for bridge diversity (~30 lines) |

---

## Validation Approach

### Automated

- All 141 existing tests must pass (especially `test_similarity.py` bridge tests)
- New tests for `explain_difference()` diversity:
  - Bridge concepts are distinct when alternatives exist
  - Falls back to reuse when no alternative exists for a field
  - `top_n` parameter slicing returns correct count
  - `top_n=1` and `top_n=15` edge cases work

### Manual Verification

- **SC-1**: All nodes draggable. Force layout settles naturally. No position-locked nodes.
- **SC-2**: Open browser dev tools, run `document.querySelectorAll('[data-id]')` or inspect Cytoscape nodes — verify each concept_id appears exactly once.
- **SC-3**: Compare a neighbor that differs on 2+ fields, both bridged by the same concept → verify single node with combined edge label.
- **SC-4**: Compare neighbors across different concepts — verify bridge concepts vary when alternatives exist.
- **SC-5**: Change neighbor count slider → verify graph rebuilds with correct count, edges and bridges recalculate.
- **SC-6**: Compare neighbor A → compare neighbor B → deselect → verify no DOM add/remove (check Cytoscape element count stays constant, only visibility changes).

### Regression Checks

- Tree sidebar collapse/expand still triggers `NeighborhoodGraph.resize()`
- Overview → focused → comparing → overview cycle works
- Constellation double-click → focus transition
- Escape key returns to overview
- Similarity cache works (re-focusing same concept doesn't re-fetch)

---

**Next Step:** After approval → `/_my_plan` to break this into implementation phases, then `/_my_implement`.
