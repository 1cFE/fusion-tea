# Spec: Neighborhood Graph — Proper Graph Model

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29
**Complexity:** MEDIUM
**Branch:** ralph/concept-explorer

---

## Business Goals

### Why This Matters

The neighborhood graph uses the wrong mental model. It procedurally assembles different views — center + neighbors as a "base", then bolts bridge concepts on as position-locked overlays that are added/removed from the DOM. This produces three concrete defects:

1. Bridge nodes are static — locked in place, not part of the force simulation, feel artificial
2. The same concept can render as multiple nodes (once per mismatched field it bridges)
3. Bridge selection doesn't prefer diversity — the same high-similarity concept wins every field

The fundamental issue: the graph should be a **data structure** where state transitions are visibility changes, not a **rendering** that gets surgically reconstructed on each interaction.

### Success Criteria

- [ ] SC-1: All nodes (center, neighbors, bridges) participate in the same force-directed layout — all draggable, all physics-settled
- [ ] SC-2: Each concept appears as exactly one node in the graph, regardless of how many relationships it has
- [ ] SC-3: When a concept bridges multiple mismatched fields, those fields are combined into the edge label (e.g. "Heating + Magnets"), not rendered as separate nodes
- [ ] SC-4: Bridge selection prefers diverse concepts — a concept that already bridges one field SHOULD NOT bridge another if alternatives exist
- [ ] SC-5: User can configure how many neighbors to show (default 5) via a control on the taxonomy page
- [ ] SC-6: State transitions (focused → comparing → different neighbor) are visibility toggles on an already-built graph, not add/remove operations

### Priority

High — the current bridge behavior undermines the usefulness of the graph as an exploration tool.

---

## Problem Statement

### Current State

The graph is built in stages that don't compose:

1. `render()` creates center + neighbor nodes with force layout
2. `showBridges()` computes geometric positions and adds new locked nodes + edges to the existing graph
3. `clearBridges()` removes those nodes from the DOM
4. Switching neighbors means: remove all bridge nodes → recompute positions → add new locked nodes

Bridge concepts that appear for multiple mismatched fields get separate node IDs (`b-{id}-0`, `b-{id}-1`) and render as separate diamonds at separate positions.

The server pre-computes bridge recommendations in `similarity.py explain_difference()` — one per mismatched field, independently, with no diversity preference. By the time the client sees the data, alternatives have already been discarded.

### Desired Outcome

A single graph built once from the full similarity report. All nodes — center, neighbors, and bridge concepts — exist in the graph from the start and participate in the force layout. State transitions change which nodes/edges are visible, not which nodes exist. Each concept is one node. Bridge edges carry combined field labels when one concept bridges multiple fields. The graph naturally settles with bridges integrated into the topology rather than floating as disconnected overlays.

The neighbor count is user-configurable with a simple UI control.

---

## Scope

### In Scope

1. **Graph architecture rewrite** — `neighborhood_graph.js` builds the complete graph (center + neighbors + all bridge concepts) upfront; state transitions toggle visibility
2. **Node deduplication** — one node per concept ID, enforced at graph construction
3. **Multi-field edge labels** — when the same concept bridges multiple fields, combine into a single edge with combined label
4. **Bridge diversity preference** — bridge selection SHOULD prefer different concepts across fields; only reuse a concept when no alternative exists for that field
5. **Configurable neighbor count** — UI control on the taxonomy page, propagated to the API, default 5
6. **API parameter** — the similarity endpoint MUST accept a `top_n` query parameter (it's already parameterized in `similarity.py`, just hardcoded to 5 in `server.py`)

### Out of Scope

- Other pages (concept detail, index, compare)
- Changes to the similarity scoring algorithm itself
- Mobile/responsive design beyond what was already done
- New API endpoints or data model changes (beyond parameterizing `top_n`)

### Edge Cases & Considerations

- A bridge concept that is also a neighbor — it already has a node as a neighbor; the bridge relationship adds an edge, not a second node
- A neighbor that bridges a field for another neighbor — same principle, one node, multiple edges
- Neighbor count of 0 or 1 — degenerate but should not crash
- All mismatched fields bridge to the same concept — that concept gets one node with one multi-label edge

---

## Requirements

### Functional Requirements

1. **FR-1**: The graph MUST be built as a single data structure containing all nodes (center, neighbors, bridge concepts) and all edges (similarity, bridge) at construction time. State transitions MUST NOT add or remove nodes.
2. **FR-2**: Each concept MUST appear as exactly one node. If a concept is both a neighbor and a bridge, it is one node with edges for both relationships. If a concept bridges multiple fields, it is one node with edge label(s) reflecting all bridged fields.
3. **FR-3**: All nodes MUST participate in the force-directed layout. No node MUST be position-locked. All nodes MUST be draggable.
4. **FR-4**: State transitions (focused → comparing neighbor A → comparing neighbor B → back to focused) MUST be implemented as visibility changes (show/hide nodes and edges, add/remove CSS classes) on the existing graph. The layout MAY re-settle when hidden nodes become visible.
5. **FR-5**: When a single concept bridges multiple mismatched fields, the bridge edge label MUST combine the field names (e.g. "Heating + Magnets"). The edge MUST NOT be duplicated.
6. **FR-6**: Bridge selection SHOULD prefer diverse concepts across fields. When multiple fields need bridges, a concept that already bridges one field SHOULD be skipped for subsequent fields if another candidate exists. Only when no alternative exists for a field SHOULD a concept bridge multiple fields.
7. **FR-7**: The taxonomy page MUST provide a user-facing control to set the number of neighbors displayed. The default MUST be 5. The control MUST trigger a new similarity fetch and graph rebuild.
8. **FR-8**: The `/api/taxonomy/similarity/{concept_id}` endpoint MUST accept an optional `top_n` query parameter. The default MUST remain 5.
9. **FR-9**: [INFERRED] The comparison table and neighbor list in the detail panel MUST remain synchronized with the graph state — selecting a neighbor in the graph updates the panel, and vice versa.

### Non-Functional Requirements

- All existing 141 tests MUST continue to pass
- Cytoscape.js loaded only on the taxonomy page (already the case)
- No changes to the similarity scoring algorithm

---

## Acceptance Criteria

### Core Functionality
- [ ] Clicking a concept in the tree builds a graph with center + neighbors + all bridge concepts in one pass
- [ ] Every node in the graph is draggable and settles via force simulation
- [ ] Clicking a neighbor reveals its bridge edges/nodes (via visibility toggle, not DOM add)
- [ ] Clicking a different neighbor hides the previous bridges and reveals the new ones
- [ ] No concept ever appears as two nodes in the graph
- [ ] A concept bridging 2 fields shows one edge with both field names
- [ ] Bridge concepts are different from each other when possible
- [ ] Neighbor count control changes the number of neighbors and rebuilds the graph

### Regression
- [ ] All 141 existing tests pass
- [ ] Tree sidebar collapse/expand still works
- [ ] Overview → focused → comparing state transitions unchanged
- [ ] Constellation double-click, neighbor click, bridge highlight all still work

---

## Related Artifacts

- **Prior work:** `.project/active/taxonomy-viz-polish/` — the visual polish spec (separate, not superseded)
- **Cytoscape.js:** `static/vendor/cytoscape.min.js` (v3.31.0, already vendored)
- **Current graph:** `static/js/neighborhood_graph.js` (Cytoscape, but wrong mental model)
- **Similarity API:** `server.py` line 422-431, `similarity.py` `explain_difference()` + `find_nearest()`
- **Bridge selection:** `taxonomy_card.js` `selectBridges()` — currently client-side, per-field, no diversity

---

**Next Steps:** After approval, proceed to `/_my_design`
