# Spec: Taxonomy Graph Spacing & Label Fix

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-12 17:53 PDT
**Complexity:** LOW
**Branch:** taxonomy-fix

---

## Business Goals

### Why This Matters
The neighborhood graph is the primary tool for exploring concept relationships in the taxonomy explorer. Currently nodes are too cramped and labels too large, making the graph hard to read.

### Success Criteria
- [ ] Graph nodes are ~3x more spread out than current layout
- [ ] Labels are readable but don't dominate the visual space
- [ ] No interaction regressions

---

## Problem Statement

### Current State
- Nodes are packed too closely together, making relationships hard to distinguish
- Label font sizes (14/13/12/10px) are disproportionately large relative to the graph area
- Node sizes (64/44/36px) contribute to visual crowding

### Desired Outcome
A well-spaced neighborhood graph where nodes, labels, and edges are clearly distinguishable without zooming.

---

## Scope

### In Scope
- Layout parameters in `neighborhood_graph.js`: radius, nodeRepulsion, idealEdgeLength, padding
- Font sizes for all node types and edges
- Node dimensions (width/height)

### Out of Scope
- Constellation view (Plotly scatter)
- New features or interaction changes
- Backend / data layer changes

---

## Requirements

### Functional Requirements

1. **FR-1**: Triple the effective node spacing — increase layout radius (~200→600), nodeRepulsion, and idealEdgeLength proportionally
2. **FR-2**: Reduce label font sizes — center, neighbor, bridge, and edge labels all smaller
3. **FR-3**: Reduce node sizes proportionally so they don't appear oversized in the larger layout

### Acceptance Criteria

- [ ] Nodes visually ~3x more spread out than current layout
- [ ] Labels readable but not dominating
- [ ] Bridge nodes still appear correctly on comparison
- [ ] Click, double-click, and tooltip interactions unchanged

---

## Related Artifacts

- **File:** `exploration/concept_explorer/static/js/neighborhood_graph.js`
- **Design:** `.project/active/taxonomy-graph-spacing/design.md` (to be created)

---

**Next Steps:** After approval, proceed to implementation (LOW complexity — design phase optional)
