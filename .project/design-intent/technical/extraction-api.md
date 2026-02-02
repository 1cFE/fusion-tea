# View Extraction API

**Date**: 2026-01-18
**Status**: Technical Spike - Design Document

---

## Strategy

**syside already gives us a graph** - the AST is a tree of elements with relationships. Visualization is just **filtering and projecting** that AST into a simpler shape for rendering.

```
SysML text → syside.try_load_model() → syside.Model → extract_*_view() → {nodes, edges}
                                            ↑                ↑
                                       the parsed AST    query parameters
```

**Usage:**
```python
import syside
from agentic_mbse.sysml.visualization import extract_structural_view

# 1. Parse SysML files → get the AST (syside.Model)
model, diagnostics = syside.try_load_model(["library.sysml", "design.sysml"])

# 2. Extract a view from the AST
result = extract_structural_view(model, root="coffee_maker", max_depth=3)
```

We're adding **view extraction functions** to `agentic-mbse/sysml/` that:
1. Take a `syside.Model` (the parsed AST) + query parameters
2. Walk the relevant parts of the AST
3. Return a simple `{nodes, edges}` dict

---

## View Types

| View | What it shows | Primary use |
|------|--------------|-------------|
| **Structural** | Part containment hierarchy | "What's in this system?" |
| **Cost** | Cost attributes + rollup chains | "Where does cost come from?" |
| **Dependency** | Calculation data flow | "What depends on what?" |

Each view is separate. No overlays for now - add only if proven necessary.

---

## API

### Location

`agentic-mbse/src/agentic_mbse/sysml/visualization.py`

### Return Type

All functions return the same shape:

```python
class ViewResult(TypedDict):
    nodes: list[dict]      # Each node has: id, name, type, depth, parent, ...
    edges: list[dict]      # Each edge has: source, target, type, ...
    metadata: dict         # View-specific info: total_nodes, max_depth, etc.
```

---

## 1. Structural View

**Question**: "What's the part hierarchy?"

```python
result = extract_structural_view(
    model=model,
    root="coffee_maker",       # Start here (None = all roots)
    max_depth=3,               # How deep to go
    include_attributes=False,  # Just parts, not attributes
    include_multiplicity=True, # Show [2] annotations
    exclude_stdlib=True,       # Skip 'start', 'done', etc.
)
```

### Output

```json
{
  "nodes": [
    {"id": "n1", "name": "coffee_maker", "type": "Coffee Maker", "depth": 0},
    {"id": "n2", "name": "brewing", "type": "Brewing System", "depth": 1, "parent": "n1"},
    {"id": "n3", "name": "heater", "type": "Heating Element", "depth": 2, "parent": "n2", "multiplicity": [2, 3]},
    {"id": "n4", "name": "pump", "type": "Water Pump", "depth": 2, "parent": "n2"},
    {"id": "n5", "name": "chamber", "type": "Brew Chamber", "depth": 2, "parent": "n2"},
    {"id": "n6", "name": "reservoir", "type": "Water Reservoir", "depth": 1, "parent": "n1"},
    {"id": "n7", "name": "carafe", "type": "Carafe", "depth": 1, "parent": "n1"},
    {"id": "n8", "name": "housing", "type": "Housing", "depth": 1, "parent": "n1"},
    {"id": "n9", "name": "shell", "type": "Outer Shell", "depth": 2, "parent": "n8"},
    {"id": "n10", "name": "panel", "type": "Control Panel", "depth": 2, "parent": "n8"}
  ],
  "edges": [
    {"source": "n1", "target": "n2", "type": "containment"},
    {"source": "n2", "target": "n3", "type": "containment"},
    ...
  ],
  "metadata": {"view": "structural", "root": "coffee_maker", "total_nodes": 10, "max_depth": 2}
}
```

### How to Get Each Field

| Field | Source |
|-------|--------|
| `id` | `str(element.element_id)` |
| `name` | `element.declared_name` |
| `type` | `list(element.types)[0].declared_name` |
| `depth` | Computed during traversal |
| `parent` | Parent element's id |
| `multiplicity` | `[mult.cached_lower_bound, mult.cached_upper_bound]` |

---

## 2. Cost View

**Question**: "What are the costs and how do they roll up?"

```python
result = extract_cost_view(
    model=model,
    root="brewing",
    cost_attributes=["capital_cost", "raw_material_cost"],  # Which costs
    include_formulas=True,   # Show rollup expressions
    include_values=True,     # Include evaluated values
)
```

### Output

```json
{
  "nodes": [
    {
      "id": "n1", "name": "brewing", "type": "Brewing System",
      "costs": {
        "capital_cost": {"formula": "sum(heater.capital_cost) + pump.capital_cost + ...", "value": 55.35},
        "raw_material_cost": {"formula": "sum(heater.raw_material_cost) + ...", "value": 32.34}
      },
      "is_leaf": false
    },
    {
      "id": "n2", "name": "heater", "type": "Heating Element",
      "multiplicity": [2, 3],
      "costs": {
        "capital_cost": {"formula": "cost_model.total_cost", "value": 13.125},
        "raw_material_cost": {"formula": "cost_model.material_cost", "value": 7.50}
      },
      "is_leaf": true
    },
    ...
  ],
  "edges": [
    {"source": "n1", "target": "n2", "type": "rollup", "label": "sum()"},
    {"source": "n1", "target": "n3", "type": "rollup"},
    ...
  ],
  "metadata": {"view": "cost", "cost_attributes": ["capital_cost", "raw_material_cost"]}
}
```

### How to Get Cost Data

```python
def get_cost_formula(part, attr_name: str) -> str | None:
    for feature in part.owned_features:
        if feature.declared_name == attr_name:
            expr = feature.feature_value_expression
            if expr:
                return syside.pprint(expr).strip()
    return None
```

### Cost Attributes

| Attribute | Leaf Formula | Assembly Formula |
|-----------|--------------|------------------|
| `capital_cost` | `cost_model.total_cost` | `sum(child.capital_cost) + ...` |
| `raw_material_cost` | `cost_model.material_cost` | `sum(child.raw_material_cost) + ...` |
| `fabrication_cost` | `cost_model.fab_cost` | `sum(...)` |
| `installation_cost` | `cost_model.install_cost` | `sum(...)` |
| `idiot_index` | `cost_model.idiot_index` | `capital_cost / raw_material_cost` |

---

## 3. Dependency View

**Question**: "What affects this value?"

```python
result = extract_dependency_view(
    model=model,
    target="brewing.capital_cost",  # What to trace
    direction="upstream",           # What feeds into it
    max_hops=3,                     # How far to trace
)
```

### Output

```json
{
  "nodes": [
    {"id": "n1", "name": "brewing.capital_cost", "node_type": "attribute"},
    {"id": "n2", "name": "heater.capital_cost", "node_type": "attribute"},
    {"id": "n3", "name": "heater.cost_model.total_cost", "node_type": "calc_output"},
    {"id": "n4", "name": "heater.power_rating", "node_type": "design_param", "value": 1000.0},
    {"id": "n5", "name": "heater.material_mass", "node_type": "design_param", "value": 0.15},
    ...
  ],
  "edges": [
    {"source": "n2", "target": "n1", "type": "aggregates_to", "operator": "sum"},
    {"source": "n3", "target": "n2", "type": "binds_to"},
    {"source": "n4", "target": "n3", "type": "input_to"},
    ...
  ],
  "metadata": {"view": "dependency", "target": "brewing.capital_cost", "direction": "upstream"}
}
```

---

## Implementation Notes

### Reuse Existing agentic-mbse Code

```python
from agentic_mbse.sysml.syside_adapter import SysideAdapter
from agentic_mbse.sysml.expression import extract_feature_refs
from agentic_mbse.sysml.binding import extract_bindings

# Type checking
SysideAdapter.is_instance(elem, "PartUsage")

# Iteration
for part in SysideAdapter.elements_of_type(model, "PartDefinition"):
    ...

# Expression analysis
refs = extract_feature_refs(expr)
```

### Filtering Standard Library

```python
STDLIB_NAMES = {'start', 'done'}
STDLIB_PREFIXES = ('Base::', 'Occurrences::', 'Parts::', 'Items::')

def is_stdlib(element) -> bool:
    name = element.declared_name or ""
    if name in STDLIB_NAMES:
        return True
    qname = str(element.qualified_name) if element.qualified_name else ""
    return any(qname.startswith(p) for p in STDLIB_PREFIXES)
```

### Walking Containment

```python
def get_child_parts(parent):
    """Get contained PartUsages, including from type definition."""
    children = []
    for f in parent.owned_features:
        if f.isinstance(syside.PartUsage):
            children.append(f)
    # Also check type definition
    types = list(parent.types) if hasattr(parent, 'types') else []
    if types and types[0].isinstance(syside.PartDefinition):
        for f in types[0].owned_features:
            if f.isinstance(syside.PartUsage):
                children.append(f)
    return children
```

---

## Expected Output (Coffee Maker)

### Structural View

```
coffee_maker (Coffee Maker)
├── brewing (Brewing System)
│   ├── heater [2] (Heating Element)
│   ├── pump (Water Pump)
│   └── chamber (Brew Chamber)
├── reservoir (Water Reservoir)
├── carafe (Carafe)
└── housing (Housing)
    ├── shell (Outer Shell)
    └── panel (Control Panel)
```

### Cost View

| Part | Capital | Raw Material | Fabrication | Installation |
|------|---------|--------------|-------------|--------------|
| coffee_maker | 113.96 | 68.44 | 37.03 | 7.53 |
| brewing | 55.35 | 32.34 | 18.45 | 3.60 |
| heater (x2) | 26.25 | 15.00 | 9.00 | 2.25 |
| pump | 17.10 | 9.00 | 7.20 | 0.90 |
| chamber | 7.20 | 4.50 | 2.25 | 0.45 |
| reservoir | 11.25 | 7.50 | 3.00 | 0.75 |
| carafe | 12.96 | 9.60 | 2.88 | 0.48 |
| housing | 34.40 | 19.00 | 12.70 | 2.70 |
| shell | 4.80 | 3.00 | 1.50 | 0.30 |
| panel | 29.60 | 16.00 | 11.20 | 2.40 |
