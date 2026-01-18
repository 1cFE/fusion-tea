# Spec: Golden Reference + Cytoscape POC

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-18 19:46:29 UTC
**Complexity:** LOW
**Branch:** visualization

---

## Business Goals

### Why This Matters

This is the first task in the Visualization POC Sprint (EPIC-001). By creating a hand-written golden reference JSON and static Cytoscape.js demo, we:
1. Force explicit decisions about the data shape before writing extraction code
2. Validate that Cytoscape.js can render compound node hierarchies as expected
3. De-risk the rendering technology choice independently of extraction complexity

This task unblocks all subsequent sprint items (extraction, pipeline, web integration, cost annotations).

### Success Criteria

- [ ] Golden reference JSON accurately represents the coffee maker structural hierarchy
- [ ] Cytoscape demo renders 3-level hierarchy correctly (coffee_maker → brewing → heater)
- [ ] Expand/collapse works on compound nodes
- [ ] PNG export produces a clean, readable image
- [ ] Diagram looks reasonable without manual layout adjustment

### Priority

P0 - Critical path for the sprint. Blocks Items 2-5.

---

## Problem Statement

### Current State

We have designed a visualization approach (see `.project/design-intent/`) and researched the technical stack (see `.project/research/20260118-180847_sysmlv2-visualization-strategy.md`), but have not validated that:
- The proposed ViewResult data format is sufficient
- Cytoscape.js can render nested compound nodes with dagre layout
- Interactive features (expand/collapse, zoom, export) work as expected

### Desired Outcome

A working static demo that proves the rendering pipeline works, providing confidence to proceed with extraction implementation.

---

## Scope

### In Scope

**Golden Reference JSON** (`proof_of_concept/golden_references/coffee_maker_structural.json`):
- Nodes for all 10 PartUsages in the coffee maker model
- Node properties: id, name, type_name, element_type, parent, depth, multiplicity
- Containment edges (parent → child relationships)
- Metadata about the view (view type, root, node count, max depth)

**Cytoscape Demo** (`proof_of_concept/cytoscape_demo.html`):
- Static HTML page (single file or minimal file set)
- Loads golden reference JSON
- Dagre layout for hierarchical arrangement
- Compound nodes showing containment hierarchy
- Node styling by type (parts)
- Expand/collapse functionality via cytoscape-expand-collapse extension
- Zoom-to-node on click/double-click
- PNG export button with 2x resolution

### Out of Scope

- Backend/server integration (Item 4)
- Dynamic model loading or CLI (Item 3)
- Cost attributes on nodes (Item 5)
- Extraction code from SysML models (Item 2)
- Dependency view or cost rollup edges (future sprints)
- Layout persistence or customization
- Multiple view types

### Edge Cases & Considerations

- **Multiplicity representation**: The `heater` part has multiplicity `[2]`. How this appears in the golden reference (single node with multiplicity vs. multiple nodes) should be verified against actual syside extraction behavior during design phase.
- **Anonymous elements**: Not present in coffee maker model, but worth noting for future reference creation.

---

## Requirements

### Functional Requirements

> Requirements below are from the epic/sprint plan.

1. **FR-1**: Golden reference JSON MUST follow the ViewResult schema from sprint plan Part 4.1-4.2
2. **FR-2**: Golden reference MUST include all 10 PartUsages from the coffee maker model hierarchy
3. **FR-3**: Each node MUST have: id, name, type_name, element_type, parent, depth, multiplicity
4. **FR-4**: Containment edges MUST connect parent nodes to child nodes
5. **FR-5**: Cytoscape demo MUST use dagre layout algorithm
6. **FR-6**: Cytoscape demo MUST render compound nodes (nested parts)
7. **FR-7**: Cytoscape demo MUST support expand/collapse of compound nodes
8. **FR-8**: Cytoscape demo MUST support zoom-to-node functionality
9. **FR-9**: Cytoscape demo MUST include PNG export at 2x resolution
10. **FR-10**: [INFERRED] Demo SHOULD be self-contained (minimal external dependencies via CDN)

### Non-Functional Requirements

- **NFR-1**: Demo should load and render in under 2 seconds (small dataset)
- **NFR-2**: Exported PNG should be readable at standard screen resolution

---

## Acceptance Criteria

### Core Functionality

- [ ] `proof_of_concept/golden_references/coffee_maker_structural.json` exists and is valid JSON
- [ ] JSON contains 10 nodes matching coffee maker hierarchy
- [ ] JSON contains 9 containment edges
- [ ] `proof_of_concept/cytoscape_demo.html` opens in browser without errors
- [ ] Diagram displays with 3-level nesting visible
- [ ] Clicking expand/collapse toggles child visibility
- [ ] Double-clicking a node zooms to fit it
- [ ] Export button produces a PNG file
- [ ] PNG shows the diagram clearly at 2x resolution

### Quality & Integration

- [ ] No console errors in browser developer tools
- [ ] Diagram layout is automatically computed (no manual positioning)

---

## Deliverables

| Deliverable | Path |
|-------------|------|
| Golden reference JSON | `proof_of_concept/golden_references/coffee_maker_structural.json` |
| Cytoscape demo | `proof_of_concept/cytoscape_demo.html` |
| Supporting files (if needed) | `proof_of_concept/` |

---

## Technical References

### Data Model

From sprint plan Part 4.1:
```python
class StructuralNode(TypedDict):
    id: str                              # Element ID (simple: "n1", "n2", etc.)
    name: str                            # Derived name (e.g., "brewing")
    type_name: str                       # SysML type name (e.g., "Brewing System")
    element_type: Literal["part"]        # Node type for styling
    parent: str | None                   # Parent node ID
    depth: int                           # Depth in hierarchy (0 = root)
    multiplicity: tuple[int, int | None] | None  # (lower, upper) or None
```

### Coffee Maker Structure

From `models/tests/coffee_maker/`:
```
coffee_maker : 'Coffee Maker' (depth 0)
├── brewing : 'Brewing System' (depth 1)
│   ├── heater : 'Heating Element' [2] (depth 2)
│   ├── pump : 'Water Pump' (depth 2)
│   └── chamber : 'Brew Chamber' (depth 2)
├── reservoir : 'Water Reservoir' (depth 1)
├── carafe : 'Carafe' (depth 1)
└── housing : 'Housing' (depth 1)
    ├── shell : 'Outer Shell' (depth 2)
    └── panel : 'Control Panel' (depth 2)
```

### Cytoscape.js Extensions Required

- `cytoscape-dagre` - Hierarchical layout
- `cytoscape-expand-collapse` - Expand/collapse compound nodes

### Stylesheet Reference

See sprint plan Part 4.3 for recommended Cytoscape.js stylesheet.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_visualization-poc.md`
- **Sprint Plan:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Design Intent:** `.project/design-intent/`
- **Test Model:** `models/tests/coffee_maker/`

---

## Open Questions for Design Phase

1. **Multiplicity representation**: Verify against syside how `heater[2]` should appear - single node with `[2,2]` multiplicity, or expanded to 2 nodes?

---

**Next Steps:** After approval, proceed to `/_my_design`
