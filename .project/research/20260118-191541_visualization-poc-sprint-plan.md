---
date: 2026-01-18T19:15:41-08:00
researcher: Claude
topic: "Visualization POC Sprint Plan"
tags: [research, visualization, sprint-planning, risk-assessment, architecture]
status: complete
last_updated: 2026-01-18
---

# Research: Visualization POC Sprint Plan

**Date**: 2026-01-18
**Researcher**: Claude
**Research Type**: Architecture / Feasibility / Sprint Planning

## Research Question

Given the UX design concepts in `.project/design-intent/` and risk assessment in `.project/research/20260118-180847_sysmlv2-visualization-strategy.md`, what is the most expedient approach to:
1. Build a proof of concept for user feedback
2. De-risk the technical approach

## Executive Summary

The visualization design is **fundamentally sound** and can be de-risked with a focused 1-week sprint. The key insight—"syside already gives us a graph, we just filter and project"—is correct. The critical risks are:

| Risk | Impact | Mitigation |
|------|--------|------------|
| Expression traversal complexity | High | Start with structural view only; defer dependency view |
| Anonymous element naming | Medium | Handle during golden reference creation |
| Cytoscape.js compound node behavior | Medium | POC validates layout/interaction before full build |
| Cross-file reference handling | Low-Medium | Coffee maker model tests this inherently |

**Recommendation**: Build a vertical slice that proves the full pipeline works: extraction → data model → rendering → export. Use the coffee maker model as the test case.

---

## Part 1: Risk Assessment

### 1.1 Architecture Risks

#### Risk A1: View Extraction Complexity (Medium-High)

**Concern**: The extraction-api.md spec looks clean, but the actual implementation may be complex when handling:
- Anonymous elements needing name derivation
- Cross-file type resolution
- Expression tree reconstruction for dependency views

**Assessment**: Structural view is simpler than cost/dependency views. The ownership hierarchy traversal is well-understood from `explore_ast.py`. Cost view requires understanding rollup formulas. Dependency view requires full expression tree reconstruction.

**Mitigation Strategy**:
1. Start with structural view only
2. Add cost annotations (attributes, not edges) as second step
3. Defer dependency view until structural and cost views work

#### Risk A2: Data Model Stability (Low)

**Concern**: Will the `ViewResult` schema need to change as we add features?

**Assessment**: The proposed schema is minimal and renderer-agnostic:
```python
class ViewResult(TypedDict):
    nodes: list[dict]      # {id, name, type, depth, parent, ...}
    edges: list[dict]      # {source, target, type, ...}
    metadata: dict         # View-specific info
```

This is flexible enough. Node and edge dicts can carry arbitrary properties.

**Mitigation**: Define explicit TypedDicts for node/edge types per view:
```python
class StructuralNode(TypedDict):
    id: str
    name: str
    type_name: str  # SysML type name
    parent: str | None
    depth: int
    multiplicity: tuple[int, int | None] | None

class ContainmentEdge(TypedDict):
    id: str
    source: str
    target: str
    edge_type: Literal["containment"]
```

#### Risk A3: agentic-mbse Integration (Low)

**Concern**: Where does visualization code live?

**Assessment**: Previous research recommends `agentic-mbse/src/agentic_mbse/sysml/visualization.py`. This is correct:
- Keeps SysML analysis co-located
- Can reuse existing utilities (syside_adapter, expression, binding)
- Decouples from frontend

**Mitigation**: None needed. Proceed with this location.

### 1.2 Interface/Data Flow Risks

#### Risk I1: Node/Edge Type Mapping (Medium)

**Concern**: How do SysML element types map to visualization node types?

**Assessment**: The coffee maker model shows these element types need representation:
- `PartDefinition` → not shown (definitions are templates)
- `PartUsage` → "part" node (containment hierarchy)
- `AttributeUsage` → "attribute" node (optional, for cost view)
- `CalculationUsage` → "calculation" node (optional, for dependency view)

Edge types needed:
- Containment (implicit via parent-child) or explicit edges
- Cost rollup (for cost view)
- Dependency (for dependency view)

**Mitigation**: Start with simple mapping:
```
PartUsage → { type: "part", ... }
```
Extend as needed. Cytoscape.js styling uses `node[type="part"]` selectors.

#### Risk I2: Cytoscape.js Data Format (Low)

**Concern**: Does the Cytoscape.js format match our ViewResult?

**Assessment**: Direct match. Our format:
```json
{
  "nodes": [{"id": "n1", "name": "...", "parent": "n2", ...}],
  "edges": [{"source": "n1", "target": "n2", ...}]
}
```

Cytoscape.js format:
```json
{
  "elements": {
    "nodes": [{"data": {"id": "n1", "label": "...", "parent": "n2", ...}}],
    "edges": [{"data": {"source": "n1", "target": "n2", ...}}]
  }
}
```

**Mitigation**: Simple wrapper function:
```python
def to_cytoscape(view_result: ViewResult) -> dict:
    return {
        "elements": {
            "nodes": [{"data": n} for n in view_result["nodes"]],
            "edges": [{"data": e} for e in view_result["edges"]]
        }
    }
```

### 1.3 Tooling Risks

#### Risk T1: Cytoscape.js Compound Node Layout (Medium)

**Concern**: Will dagre layout work well with nested compound nodes?

**Assessment**: Cytoscape.js supports compound nodes via `data.parent`, and dagre layout handles them. However, deeply nested hierarchies (3+ levels) may need layout tuning.

**Mitigation**: POC validates this with coffee maker model (3 levels: coffee_maker → brewing → heater).

#### Risk T2: Interactive Features (Low)

**Concern**: Will expand/collapse, zooming, highlighting work as expected?

**Assessment**: `cytoscape-expand-collapse` extension is mature and well-documented. Standard features like zoom-to-node and neighbor highlighting are straightforward.

**Mitigation**: POC includes basic interactivity to validate.

#### Risk T3: Export Quality (Low)

**Concern**: Will PNG/SVG exports be publication quality?

**Assessment**: Cytoscape.js built-in PNG export supports high resolution (scale factor). SVG export via `cytoscape-svg` extension.

**Mitigation**: POC tests export at 2x resolution.

### 1.4 Usability Risks

#### Risk U1: Layout Aesthetics (Medium)

**Concern**: Will auto-layout produce visually pleasing diagrams?

**Assessment**: Dagre is a reasonable starting point but may need manual adjustment for complex models. ELK is better but heavier.

**Mitigation**:
- Start with dagre
- Document layout parameter tuning
- Consider ELK for v1.1

#### Risk U2: Information Density (Medium)

**Concern**: How to show enough detail without overwhelming?

**Assessment**: The design-intent documents emphasize progressive disclosure:
- Initial view shows major subsystems
- Expand to see children
- Cost annotations optional (toggle layer)

**Mitigation**: POC starts with collapsed view; user expands on demand.

---

## Part 2: Gap Analysis

### 2.1 What Exists

| Component | Location | Status |
|-----------|----------|--------|
| SysML parsing | syside (installed) | Ready |
| Model loading | SysideAdapter | Ready |
| Expression traversal | expression.py | Partial (flat extraction, not tree) |
| Binding analysis | binding.py | Ready |
| Graph algorithms | graph.py | Ready (cycle detection, topo sort) |
| Data types | types.py | Ready (BindingInfo, ExpressionRef) |
| Source location | helpers.py | Ready |
| AST exploration script | explore_ast.py | Reference only |

### 2.2 What's Missing

| Component | Priority | Effort | Notes |
|-----------|----------|--------|-------|
| `extract_structural_view()` | P0 | Medium | Core extraction function |
| `extract_cost_view()` | P1 | Medium | Adds cost attributes to nodes |
| `extract_dependency_view()` | P2 | High | Defer to later sprint |
| Cytoscape.js output conversion | P0 | Low | Simple wrapper |
| DOT output conversion | P0 | Low | For quick validation |
| Web frontend | P1 | Medium | React + Cytoscape.js |
| Agent integration | P2 | High | Defer to later sprint |

### 2.3 Golden Reference Artifact

Before implementing extraction, create a hand-written "golden reference" JSON that represents the expected output for the coffee maker model. This:
- Forces explicit decisions about data shape
- Provides test fixture for extraction code
- Can be fed to Cytoscape.js to validate rendering independent of extraction

**Golden reference deliverables**:
1. `coffee_maker_structural.json` - Structural view nodes/edges
2. `coffee_maker_cost.json` - Structural view with cost annotations

---

## Part 3: 1-Week Sprint Proposal

### Sprint Goal

**De-risk the visualization pipeline by building a working vertical slice from SysML model to interactive web diagram.**

By end of sprint:
- Can load coffee maker model and render interactive structural diagram
- Can export PNG of diagram
- Have golden reference + automated test validating extraction
- Confidence to proceed with full implementation

### Sprint Structure

#### Day 1: Golden Reference + Cytoscape POC

**Objective**: Validate Cytoscape.js can render the diagram we want, independent of extraction.

**Deliverables**:
1. `golden_references/coffee_maker_structural.json` - Hand-written JSON in our ViewResult format
2. `proof_of_concept/cytoscape_demo.html` - Static HTML loading golden reference and rendering with:
   - Dagre layout
   - Compound nodes (part hierarchy)
   - Node type styling (parts vs attributes)
   - Basic expand/collapse
   - Zoom to node
   - PNG export

**Validation**:
- Diagram looks reasonable
- 3-level hierarchy renders correctly
- Expand/collapse works
- Export produces clean PNG

**Risk addressed**: T1 (compound node layout), T2 (interactive features), T3 (export quality)

#### Day 2: Extraction Implementation

**Objective**: Implement `extract_structural_view()` that produces output matching golden reference.

**Deliverables**:
1. `agentic_mbse/sysml/visualization.py` with:
   ```python
   def extract_structural_view(
       model,
       root: str | None = None,
       max_depth: int = 10,
       include_multiplicity: bool = True,
       exclude_stdlib: bool = True
   ) -> ViewResult:
       """Extract structural (containment) view from SysML model."""
   ```
2. Test: `tests/sysml/test_visualization.py` comparing extraction output to golden reference

**Implementation approach**:
- Walk ownership tree starting from root PartUsage
- For each PartUsage, add node with: id, name (from element or redefined_feature), type_name, parent, depth, multiplicity
- Follow typing relationships to get children from PartDefinitions
- Filter stdlib elements

**Validation**:
- `pytest tests/sysml/test_visualization.py` passes
- Extracted JSON matches golden reference structure

**Risk addressed**: A1 (extraction complexity), I1 (type mapping)

#### Day 3: End-to-End Pipeline

**Objective**: Connect extraction to rendering.

**Deliverables**:
1. `agentic_mbse/sysml/visualization.py` additions:
   ```python
   def to_cytoscape(view_result: ViewResult) -> dict:
       """Convert ViewResult to Cytoscape.js elements format."""

   def to_dot(view_result: ViewResult) -> str:
       """Convert ViewResult to DOT format for Graphviz."""
   ```
2. CLI command: `uv run python -m agentic_mbse.sysml.visualization models/tests/coffee_maker`
   - Outputs JSON to stdout (or file with --output)
   - Outputs DOT with --format=dot
3. DOT rendering test: `uv run python -m agentic_mbse.sysml.visualization models/tests/coffee_maker --format=dot | dot -Tpng > test.png`

**Validation**:
- CLI produces valid JSON loadable by Cytoscape POC from Day 1
- DOT output renders correctly in Graphviz
- End-to-end: model → extraction → JSON → Cytoscape → interactive diagram

**Risk addressed**: I2 (data format), pipeline integration

#### Day 4: Web Integration

**Objective**: Create minimal web app that loads model and renders diagram.

**Deliverables**:
1. `proof_of_concept/web/` directory with:
   - `server.py` - FastAPI server with:
     - `GET /api/model/{path}` - Returns Cytoscape.js elements for model at path
     - Static file serving for frontend
   - `index.html` - Web page with:
     - Cytoscape.js rendering
     - Model path input
     - Export button
2. README with setup instructions

**Validation**:
- Navigate to `http://localhost:8000`
- Enter `models/tests/coffee_maker`
- See interactive diagram
- Export PNG works

**Risk addressed**: Backend integration, user workflow

#### Day 5: Cost Annotations + Polish

**Objective**: Add cost data to structural view; polish for demo.

**Deliverables**:
1. Update `extract_structural_view()` with optional cost attributes:
   ```python
   def extract_structural_view(
       ...,
       include_cost_attributes: list[str] | None = None  # e.g., ["capital_cost"]
   ) -> ViewResult:
   ```
2. Update Cytoscape styling to show cost in tooltips or labels
3. `golden_references/coffee_maker_with_costs.json` - Golden reference with cost data
4. Updated tests
5. Demo script/recording showing the workflow

**Validation**:
- Cost values appear on nodes (tooltip or label)
- Golden reference with costs matches extraction
- Demo is ready for stakeholder review

**Risk addressed**: Cost view feasibility, demo readiness

### Sprint Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Extraction works | Tests pass comparing to golden reference |
| Rendering works | Coffee maker hierarchy visible in browser |
| Export works | PNG export produces readable image |
| Pipeline complete | Model file → interactive diagram in browser |
| De-risked | No blocking unknowns for full implementation |

---

## Part 4: Technical Specifications

### 4.1 ViewResult Data Model

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
    # Cost attributes (optional)
    costs: dict[str, float] | None       # e.g., {"capital_cost": 113.96}

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

### 4.2 Golden Reference (Coffee Maker Structural)

```json
{
  "nodes": [
    {"id": "n1", "name": "coffee_maker", "type_name": "Coffee Maker", "element_type": "part", "parent": null, "depth": 0, "multiplicity": null},
    {"id": "n2", "name": "brewing", "type_name": "Brewing System", "element_type": "part", "parent": "n1", "depth": 1, "multiplicity": null},
    {"id": "n3", "name": "heater", "type_name": "Heating Element", "element_type": "part", "parent": "n2", "depth": 2, "multiplicity": [2, 2]},
    {"id": "n4", "name": "pump", "type_name": "Water Pump", "element_type": "part", "parent": "n2", "depth": 2, "multiplicity": null},
    {"id": "n5", "name": "chamber", "type_name": "Brew Chamber", "element_type": "part", "parent": "n2", "depth": 2, "multiplicity": null},
    {"id": "n6", "name": "reservoir", "type_name": "Water Reservoir", "element_type": "part", "parent": "n1", "depth": 1, "multiplicity": null},
    {"id": "n7", "name": "carafe", "type_name": "Carafe", "element_type": "part", "parent": "n1", "depth": 1, "multiplicity": null},
    {"id": "n8", "name": "housing", "type_name": "Housing", "element_type": "part", "parent": "n1", "depth": 1, "multiplicity": null},
    {"id": "n9", "name": "shell", "type_name": "Outer Shell", "element_type": "part", "parent": "n8", "depth": 2, "multiplicity": null},
    {"id": "n10", "name": "panel", "type_name": "Control Panel", "element_type": "part", "parent": "n8", "depth": 2, "multiplicity": null}
  ],
  "edges": [
    {"id": "e1", "source": "n1", "target": "n2", "edge_type": "containment"},
    {"id": "e2", "source": "n2", "target": "n3", "edge_type": "containment"},
    {"id": "e3", "source": "n2", "target": "n4", "edge_type": "containment"},
    {"id": "e4", "source": "n2", "target": "n5", "edge_type": "containment"},
    {"id": "e5", "source": "n1", "target": "n6", "edge_type": "containment"},
    {"id": "e6", "source": "n1", "target": "n7", "edge_type": "containment"},
    {"id": "e7", "source": "n1", "target": "n8", "edge_type": "containment"},
    {"id": "e8", "source": "n8", "target": "n9", "edge_type": "containment"},
    {"id": "e9", "source": "n8", "target": "n10", "edge_type": "containment"}
  ],
  "metadata": {
    "view": "structural",
    "root": "coffee_maker",
    "total_nodes": 10,
    "max_depth": 2
  }
}
```

### 4.3 Cytoscape.js Stylesheet (Recommended)

```javascript
const stylesheet = [
  // Part nodes (compound containers)
  {
    selector: 'node[element_type="part"]',
    style: {
      'shape': 'round-rectangle',
      'background-color': '#e3f2fd',
      'border-color': '#1976d2',
      'border-width': 2,
      'label': 'data(name)',
      'text-valign': 'top',
      'text-margin-y': 8,
      'padding': '20px',
      'font-weight': 'bold'
    }
  },
  // Parts with multiplicity
  {
    selector: 'node[multiplicity]',
    style: {
      'label': function(ele) {
        const m = ele.data('multiplicity');
        const name = ele.data('name');
        if (m && m[0] === m[1]) return `${name} [${m[0]}]`;
        if (m) return `${name} [${m[0]}..${m[1] || '*'}]`;
        return name;
      }
    }
  },
  // Selection state
  {
    selector: ':selected',
    style: {
      'border-width': 4,
      'border-color': '#ff5722'
    }
  },
  // Collapsed indicator
  {
    selector: '.cy-expand-collapse-collapsed-node',
    style: {
      'border-style': 'double',
      'border-width': 4
    }
  }
];
```

### 4.4 File Structure for POC

```
proof_of_concept/
├── golden_references/
│   ├── coffee_maker_structural.json
│   └── coffee_maker_with_costs.json
├── cytoscape_demo.html           # Static demo (Day 1)
├── web/
│   ├── server.py                 # FastAPI backend (Day 4)
│   ├── static/
│   │   ├── index.html
│   │   ├── graph.js
│   │   └── styles.css
│   └── README.md
└── README.md

# In agentic-mbse (separate repo):
src/agentic_mbse/sysml/
├── visualization.py              # NEW: extraction functions
└── ...existing files...

tests/sysml/
├── test_visualization.py         # NEW: extraction tests
└── ...existing tests...
```

---

## Part 5: Deferred Work

### Not in This Sprint

| Item | Reason | When to Address |
|------|--------|-----------------|
| Dependency view | High complexity (expression trees) | Sprint 2 |
| Agent integration | Requires stable extraction API | Sprint 2-3 |
| Real-time model watching | Nice-to-have, not de-risking | Sprint 2 |
| Multiple view types in UI | Start with structural only | Sprint 2 |
| Layout customization | Dagre defaults are acceptable | As needed |
| Fusion model support | Validate with coffee maker first | After POC |

### Known Limitations of POC

1. **No real-time updates** - Manual refresh required
2. **No agent integration** - Static query only
3. **No cost rollup visualization** - Cost shown as attributes, not edges
4. **No dependency tracing** - Structural view only
5. **No layout persistence** - Positions reset on reload

---

## Part 6: Recommendations

### Immediate Actions

1. **Create golden reference files** before any code - forces design decisions
2. **Start with static Cytoscape demo** - validates tool choice before integration
3. **Implement extraction with tests** - ensures correctness before UI
4. **Keep scope minimal** - resist feature creep during de-risking sprint

### Architecture Decisions (Confirmed)

1. **Visualization code in agentic-mbse** - keeps SysML analysis together
2. **ViewResult as intermediate format** - renderer-agnostic
3. **Cytoscape.js as primary renderer** - compound nodes, good layout
4. **Dagre layout initially** - good enough, can upgrade to ELK later

### Questions Resolved

| Question | Decision |
|----------|----------|
| Where does viz code live? | `agentic-mbse/sysml/visualization.py` |
| What renderer? | Cytoscape.js |
| What layout? | Dagre (can upgrade to ELK) |
| How to test extraction? | Golden reference comparison |
| Which model for POC? | Coffee maker |
| How to handle anonymous elements? | Derive name from redefined_feature |

---

## References

### Design Documents
- `.project/design-intent/README.md`
- `.project/design-intent/concepts.md`
- `.project/design-intent/requirements.md`
- `.project/design-intent/technical/extraction-api.md`
- `.project/design-intent/technical/ast-exploration.md`
- `.project/design-intent/technical/tool-research.md`

### Previous Research
- `.project/research/20260118-180847_sysmlv2-visualization-strategy.md`
- `.project/research/20260116-161342_sysml-v2-visualization-tools.md`

### Code Analyzed
- `/home/reid/1cfe/agentic-mbse/src/agentic_mbse/sysml/*.py`
- `models/tests/coffee_maker/library.sysml`
- `models/tests/coffee_maker/design.sysml`
- `.project/design-intent/technical/explore_ast.py`

### External Resources
- [Cytoscape.js Documentation](https://js.cytoscape.org/)
- [cytoscape-dagre](https://github.com/cytoscape/cytoscape.js-dagre)
- [cytoscape-expand-collapse](https://github.com/iVis-at-Bilkent/cytoscape.js-expand-collapse)
