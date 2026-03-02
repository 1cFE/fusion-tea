# Spec: Extraction Implementation (POC Item 2)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-18 20:47:13 UTC
**Complexity:** MEDIUM
**Branch:** visualization

---

## Business Goals

### Why This Matters

This is the core extraction logic that transforms a parsed SysML model into a renderer-agnostic data structure (`ViewResult`). It de-risks the most uncertain part of the visualization pipeline - whether we can reliably extract the structural hierarchy from syside's AST.

Item 1 validated that Cytoscape.js can render what we want. This item validates that we can programmatically extract that data from real SysML models.

### Success Criteria

- [x] `pytest` passes for extraction tests (19/19 pass)
- [x] Extracted JSON matches golden reference structure for coffee_maker model
- [x] Extraction handles: naming (declared vs redefined), multiplicity, depth tracking, stdlib filtering

### Priority

P0 (Critical) - Blocking dependency for Items 3-5. Item 1 is complete.

---

## Problem Statement

### Current State

- Golden reference exists: `proof_of_concept/golden_references/coffee_maker_structural.json`
- Cytoscape demo validates the data format works for rendering
- No extraction code exists to produce this data from actual SysML models

### Desired Outcome

A function `extract_structural_view()` that:
- Takes a parsed syside model
- Returns a `ViewResult` dict matching the golden reference schema
- Can be validated against the golden reference via automated tests

---

## Scope

### In Scope

1. **`extract_structural_view()` function** with signature:
   ```python
   def extract_structural_view(
       model,
       root: str | None = None,
       max_depth: int = 10,
       include_multiplicity: bool = True,
       exclude_stdlib: bool = True
   ) -> ViewResult:
   ```

2. **ViewResult data types** (TypedDict definitions):
   - `StructuralNode`: id, name, type_name, element_type, parent, depth, multiplicity
   - `ContainmentEdge`: id, source, target, edge_type
   - `StructuralViewResult`: nodes, edges, metadata

3. **Test suite** comparing extraction output to golden reference

4. **Coffee maker model** as the test case

### Out of Scope

- Cost view extraction (Item 5)
- Dependency view extraction (Sprint 2)
- CLI interface (Item 3)
- `to_cytoscape()` converter (Item 3)
- `to_dot()` converter (Item 3)
- Web integration (Item 4)

### Edge Cases & Considerations

- **Anonymous elements**: Derive name from `redefined_feature` when declared name is absent
- **Cross-file references**: Coffee maker model uses multiple files; extraction must follow type references
- **Stdlib filtering**: Exclude elements from SysML standard library
- **Multiplicity parsing**: Handle `[n]`, `[n..m]`, `[n..*]` formats

---

## Requirements

### Functional Requirements

> Requirements below are from sprint plan (research document lines 281-309)

1. **FR-1**: Walk ownership tree starting from root PartUsage
2. **FR-2**: For each PartUsage, extract: id, name, type_name, parent, depth, multiplicity
3. **FR-3**: Follow typing relationships to get children from PartDefinitions
4. **FR-4**: Filter stdlib elements when `exclude_stdlib=True`
5. **FR-5**: Derive name from `redefined_feature` when element has no declared name
6. **FR-6**: Generate containment edges for parent-child relationships
7. **FR-7**: Return `ViewResult` dict matching the golden reference schema

### Non-Functional Requirements

- **NFR-1**: Code lives in `fusion-tea` for POC phase (not agentic-mbse)

---

## Acceptance Criteria

### Core Functionality

- [x] `extract_structural_view()` accepts a syside model object
- [x] Output matches `StructuralViewResult` TypedDict schema
- [x] Extracted nodes include: id, name, type_name, element_type, parent, depth, multiplicity
- [x] Extracted edges include: id, source, target, edge_type
- [x] Metadata includes: view type, root element, total_nodes, max_depth

### Test Validation

- [x] Test loads `models/tests/coffee_maker` via syside
- [x] Test compares extracted output to `proof_of_concept/golden_references/coffee_maker_structural.json`
- [x] Test validates node count matches (10 nodes)
- [x] Test validates edge count matches (9 edges)
- [x] Test validates hierarchy depth (max_depth: 2)
- [x] Test validates multiplicity is captured (heater [2,2])

### Quality & Integration

- [x] Existing tests continue to pass
- [x] Code uses syside API correctly (via existing patterns in project)

---

## Technical Notes

### ViewResult Schema (from research Part 4.1)

```python
from typing import TypedDict, Literal

class StructuralNode(TypedDict):
    id: str                              # Element ID from syside
    name: str                            # Derived name (declared or from redefines)
    type_name: str                       # SysML type name (e.g., "Coffee Maker")
    element_type: Literal["part", "attribute", "calculation"]
    parent: str | None                   # Parent node ID (for containment)
    depth: int                           # Depth in hierarchy (0 = root)
    multiplicity: tuple[int, int | None] | None  # (lower, upper) or None

class ContainmentEdge(TypedDict):
    id: str                              # Generated edge ID
    source: str                          # Parent node ID
    target: str                          # Child node ID
    edge_type: Literal["containment"]

class StructuralViewResult(TypedDict):
    nodes: list[StructuralNode]
    edges: list[ContainmentEdge]
    metadata: dict  # {"view": "structural", "root": ..., "max_depth": ...}
```

### Implementation Approach (from research Part 3, Day 2)

1. Load model via syside
2. Find root PartUsage (by name if specified, otherwise first top-level part)
3. Recursively walk owned members
4. For each PartUsage:
   - Generate stable ID
   - Get name (declared_name or from redefined_feature)
   - Get type_name from typing relationship
   - Track parent and depth
   - Parse multiplicity from multiplicity feature
5. Build edges from parent-child relationships
6. Filter stdlib elements

### File Locations

```
proof_of_concept/
├── extraction/
│   ├── __init__.py
│   ├── visualization.py      # extract_structural_view()
│   └── types.py              # TypedDict definitions
├── tests/
│   └── test_visualization.py # Golden reference comparison tests
└── golden_references/
    └── coffee_maker_structural.json  # (exists)
```

---

## Related Artifacts

- **Research:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md`
- **Golden Reference:** `proof_of_concept/golden_references/coffee_maker_structural.json`
- **Test Model:** `models/tests/coffee_maker/`
- **Design:** `.project/active/extraction-implementation/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
