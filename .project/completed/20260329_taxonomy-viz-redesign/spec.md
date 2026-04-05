# Spec: Taxonomy Visualization Redesign

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-29 16:45 PDT
**Complexity:** HIGH
**Branch:** ralph/concept-explorer

---

## Business Goals

### Why This Matters

The taxonomy page was built to let users explore the fusion concept design space and understand relationships between 38 concepts. The current implementation fails at this: the constellation plot is a static scatter with meaningless axes that shows proximity without explaining *why*. The similarity card uses abstract dimension bars ("plasma_physics: 2/3") that hide the actual attribute values. And the bridge concept feature — which answers the most analytically interesting question ("where else in the design space does someone make this same unusual choice?") — is buried in a cryptic one-liner that no one can parse without already knowing the data model.

The core problem is that the UI shows summaries of data instead of the data itself, and hides the most valuable feature behind the worst presentation.

### Success Criteria

- [ ] SC-1: A user can focus on any concept and immediately see its nearest neighbors in a spatial layout that communicates similarity through proximity
- [ ] SC-2: Clicking a neighbor shows a field-by-field comparison with actual attribute values — the user can see *exactly* where two concepts match and where they diverge without reading documentation
- [ ] SC-3: When a comparison reveals differences, the user can see which other concepts (potentially from different confinement families) share the focused concept's unusual choices — and can navigate to those concepts to continue exploring
- [ ] SC-4: The visualization is self-explanatory — tooltips, labels, and visual language communicate what the user is looking at without requiring prior knowledge of the data model
- [ ] SC-5: The graph is a navigation tool, not just a display — users can traverse the design space by following cross-cutting attribute connections

### Priority

Active redesign of just-completed feature on `ralph/concept-explorer`. High priority — the current UI is confusing enough that it undermines the value of the underlying data and computation.

---

## Problem Statement

### Current State

- **Constellation plot** is a 2D MDS projection with abstract axes (48% variance explained). It shows clustering but communicates no relationship information. Fixed layout — no interaction beyond click-to-select.
- **Similarity card** shows dimension bars (plasma_physics, engineering, fuel_cycle, operations) with match ratios (e.g., "2/3"). The user cannot see which fields matched, what the values are, or why the ratio is what it is without reading source code.
- **Bridge concepts** appear as single-line callouts ("Differs on energy_capture -> Nanostructured Target") with no explanation of what this means, why it matters, or what the actual values are. The most valuable analytical feature has the worst UX.
- **Layout issues**: The tree sidebar is always visible and takes significant horizontal space. The similar concepts section scrolls with the page, so scrolling through neighbors loses the graph from view. Taxonomy is the last nav tab despite being the primary exploration surface.

### Desired Outcome

An interactive graph-based visualization where the user explores relationships through direct manipulation: focusing on concepts, comparing neighbors with real attribute values, and navigating across the design space by following cross-cutting connections that emerge as bridge nodes in the graph. The visualization should be self-documenting through tooltips and visual language.

---

## Scope

### In Scope

1. **Neighborhood graph component** — SVG-based, radial layout, replaces constellation on concept focus
2. **Three-layer interaction model** — focus (double-click) → compare (single-click) → navigate (double-click bridge)
3. **Field-by-field comparison panel** — replaces abstract dimension bars with actual attribute values
4. **Bridge concepts as graph nodes** — visually distinct, family-colored, labeled with shared attribute
5. **Constellation as toggleable overview** — default view on page load, transitions to neighborhood graph on focus
6. **Layout restructuring** — collapsible tree sidebar, independently scrollable similar-concepts panel, taxonomy as first nav tab
7. **Tooltips and explanatory UI** — hover tips on non-obvious elements explaining what the user is looking at

### Out of Scope

- Mobile/responsive design (explicitly excluded by user)
- Changes to existing pages (All Concepts, Compare, individual concept profiles)
- New API endpoints or changes to similarity computation logic (existing APIs already return all needed data)
- Changes to taxonomy data models, seed script, or similarity engine
- Changes to the tree view's internal rendering (just wrapping it in a collapsible container)

### Edge Cases & Considerations

- **Bridge node clutter**: A neighbor can have 3+ differences, each potentially producing a bridge. Without filtering, the graph becomes cluttered. Bridge selection MUST be limited and prioritized (see FR-10).
- **Concept with no bridges**: Some neighbor comparisons may have zero mismatched fields (100% match) or no bridge concepts found. The graph should handle this gracefully — no bridge nodes appear, comparison table shows all matches.
- **Re-centering loops**: If user double-clicks bridge A from concept X, then a bridge back to X appears from A's neighborhood. This is expected and useful — it shows the bidirectional connection.
- **Constellation-to-graph transition**: If animation proves unstable (layout jitter, timing issues), a clean fade transition is acceptable. Stability over visual polish.
- **Plotly coexistence**: The constellation uses Plotly; the neighborhood graph uses SVG. Both render in the same container area. Mode switching must cleanly tear down one and build the other.

---

## Requirements

### Functional Requirements — Graph Visualization

> Requirements below are from user's request unless marked [INFERRED].

1. **FR-1**: The system MUST provide a neighborhood graph that displays a focused concept at the center with its nearest neighbors arranged radially around it. The number of neighbors MUST default to 5 and SHOULD be easily configurable (single constant).

2. **FR-2**: The system MUST use a radial layout computed deterministically (not force-directed physics simulation). Neighbor nodes MUST be positioned at a fixed radius from center. Edge weight (line thickness or opacity) MUST encode similarity score.

3. **FR-3**: Graph nodes MUST be color-coded by confinement family using the existing color palette (MFE blue, IFE purple, MIF amber, Non-Standard gray).

4. **FR-4**: Double-clicking a concept (in the graph, tree, or constellation) MUST focus the graph on that concept — it becomes the center node with its neighbors in the ring. Double-clicking a bridge node MUST re-center the graph on that bridge concept, loading its neighborhood.

5. **FR-5**: Single-clicking a neighbor node MUST trigger two simultaneous effects: (a) the field-by-field comparison appears in the detail panel, and (b) bridge concept nodes appear in the graph.

6. **FR-6**: Bridge concept nodes MUST be visually distinct from neighbor nodes — different shape (diamond or hexagon), different size, or different border style — so the user can tell relationship types apart at a glance without reading labels.

7. **FR-7**: Bridge nodes MUST be connected to the center (focused) concept by distinctly-styled edges (e.g., dashed, different color) labeled with the shared attribute value. Bridge edges MUST be visually distinguishable from similarity edges.

8. **FR-8**: Bridge nodes MUST display the concept name and a family badge. The family color immediately communicates whether this is a cross-family connection (the interesting case) or a same-family one.

9. **FR-9**: When a different neighbor is single-clicked, the previous set of bridge nodes MUST fade out and the new set MUST fade in. Neighbor node positions MUST remain stable.

10. **FR-10**: Bridge concept selection MUST be limited to at most 3 bridge nodes per neighbor comparison. Selection MUST prioritize by similarity score to the focused concept (most similar bridge first), with the constraint that each bridge concept MUST contribute a *different* mismatched field than previously selected bridges. This ensures diversity — one bridge per difference dimension rather than three bridges for the same field.

### Functional Requirements — Comparison Panel

11. **FR-11**: The system MUST provide a field-by-field comparison table showing actual attribute values for both the focused concept and the selected neighbor. Each row MUST show: field label, focused concept's value, match/mismatch indicator, neighbor's value.

12. **FR-12**: Matched fields MUST be visually de-emphasized (muted text, smaller, or collapsed). Mismatched fields MUST be visually prominent (full contrast, possibly highlighted). The comparison MUST lead with or emphasize differences — the interesting information.

13. **FR-13**: For each mismatched field, if a bridge concept was found, the comparison table MUST reference it inline — e.g., "Also uses [value]: [Bridge Concept Name] [family badge]". Clicking the bridge reference in the table MUST highlight the corresponding bridge node in the graph.

14. **FR-14**: N/A and TBD fields MUST be excluded from the comparison (consistent with existing similarity computation). They SHOULD NOT appear in the comparison table at all — only fields where both concepts have actual values.

### Functional Requirements — Constellation Overview

15. **FR-15**: The constellation (existing Plotly MDS scatter) MUST remain as the default view on page load. It serves as the global overview of the design space.

16. **FR-16**: Focusing a concept (double-click) MUST transition from constellation to neighborhood graph. The transition SHOULD animate (constellation nodes moving to radial positions) if stable; otherwise a clean fade transition is acceptable.

17. **FR-17**: A clearly visible control MUST allow the user to return from the neighborhood graph to the constellation overview. [INFERRED] This could be a button, an Escape key binding, or both.

### Functional Requirements — Layout

18. **FR-18**: The tree sidebar MUST be collapsible/hideable. When collapsed, the graph area MUST expand to fill the available width. A toggle control (button or icon) MUST be always accessible to show/hide the sidebar.

19. **FR-19**: The similar-concepts / comparison panel MUST scroll independently from the graph viewport. Scrolling through neighbor comparisons MUST NOT cause the graph to scroll out of view. [INFERRED] This implies the panel is a fixed-height scrollable container, not part of the page flow.

20. **FR-20**: The Taxonomy nav link MUST be the first tab in the navigation bar (currently third after "All Concepts" and "Compare").

### Functional Requirements — Tooltips & Explanatory UI

21. **FR-21**: The constellation plot MUST display a title or caption explaining what it shows (e.g., "Design Space Overview — concepts positioned by attribute similarity"). Axis labels SHOULD be hidden or replaced with a note that axes represent abstract similarity dimensions.

22. **FR-22**: The neighborhood graph MUST display contextual guidance when first shown — either a title (e.g., "Neighborhood of [Concept Name]") or brief instructional text explaining the interaction model (single-click to compare, double-click to navigate).

23. **FR-23**: Graph nodes MUST show a tooltip on hover with at minimum: concept name, confinement family, and (for bridge nodes) the shared attribute and its value.

24. **FR-24**: Bridge edges MUST show a tooltip on hover explaining the relationship — e.g., "Both use [value] for [field]".

25. **FR-25**: The comparison panel MUST have a header or label explaining what is being compared. [INFERRED] Field labels in the comparison table SHOULD use human-readable names (e.g., "Primary Heating" not "primary_heating").

26. **FR-26**: [INFERRED] Non-obvious UI controls (the sidebar collapse toggle, the "back to overview" button, the view mode indicator) MUST have tooltips or labels explaining their function.

---

## Acceptance Criteria

### Graph Interaction
- [ ] Double-click a concept in the tree → neighborhood graph appears with concept at center, 5 neighbors in a ring
- [ ] Double-click a concept in the constellation → same behavior, constellation transitions to graph
- [ ] Single-click a neighbor → comparison panel shows field-by-field values, bridge nodes appear in graph
- [ ] Single-click a different neighbor → old bridges fade out, new bridges fade in, neighbor positions stable
- [ ] Double-click a bridge node → graph re-centers on that concept with its own neighborhood
- [ ] Bridge nodes are visually distinct from neighbor nodes (different shape/style)
- [ ] Bridge edges are visually distinct from similarity edges (different line style)
- [ ] At most 3 bridge nodes per comparison, each for a different mismatched field

### Comparison Panel
- [ ] Shows actual attribute values for both concepts (not just field names or ratios)
- [ ] Differences are visually prominent; matches are de-emphasized
- [ ] Mismatched fields reference bridge concepts inline with family badge
- [ ] Clicking a bridge reference in the panel highlights the node in the graph
- [ ] Panel scrolls independently — graph stays in view while scrolling comparisons

### Layout & Navigation
- [ ] Taxonomy is the first nav tab
- [ ] Tree sidebar collapses via toggle; graph expands to fill space
- [ ] "Back to overview" control returns to constellation from neighborhood graph
- [ ] Existing pages (All Concepts, Compare) still work and are unaffected

### Tooltips & Self-Documentation
- [ ] Constellation has a title/caption explaining what it shows
- [ ] Neighborhood graph has a contextual header with the focused concept name
- [ ] Hover over any graph node → tooltip with concept name, family, and (for bridges) shared attribute
- [ ] Hover over bridge edge → tooltip explaining the relationship
- [ ] Human-readable field labels throughout (not snake_case identifiers)

### Quality & Integration
- [ ] All existing tests pass (140 tests)
- [ ] No new JS dependencies required (SVG + CSS transitions, Plotly already vendored)
- [ ] Existing API endpoints used unchanged

---

## Related Artifacts

- **Prior spec:** `.project/active/concept-taxonomy-and-similarity/spec.md` (original feature — completed)
- **Prior design:** `.project/active/concept-taxonomy-and-similarity/design.md` (current implementation details)
- **Current implementation:** `exploration/concept_explorer/static/js/constellation.js`, `taxonomy.js`, `taxonomy_card.js`, `tree_view.js`
- **Existing API:** `/api/taxonomy/similarity/{id}` returns neighbors + bridges with field values — no changes needed
- **Design:** `.project/active/taxonomy-viz-redesign/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
