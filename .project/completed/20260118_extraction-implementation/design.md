# Design: Extraction Implementation (POC Item 2)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-18 20:49:57 UTC
**Last Updated:** 2026-01-18
**Branch:** visualization
**Commit:** b812d74

---

## Overview

Implement `extract_structural_view()` function that traverses a parsed syside SysML model and produces a `ViewResult` data structure matching the golden reference schema. This validates that we can programmatically extract structural hierarchy from real SysML models.

---

## Related Artifacts

- **Spec:** `.project/active/extraction-implementation/spec.md`
- **Research:** `.project/research/20260118-191541_visualization-poc-sprint-plan.md`
- **Epic:** `.project/backlog/epic_visualization-poc.md`
- **Golden Reference:** `proof_of_concept/golden_references/coffee_maker_structural.json`
- **Test Model:** `models/tests/coffee_maker/`

---

## Research Findings

### Existing Implementation

A working prototype exists at `.project/design-intent/technical/explore_ast.py`:

- **`extract_structural_data()`** (lines 444-478): Entry point that extracts nodes/edges from the model
- **`_extract_parts()`** (lines 490-570): Recursive traversal that follows typing relationships to get children from PartDefinitions
- **`_is_stdlib_element()`** (lines 481-487): Filters standard library elements
- **`_get_multiplicity_str()`** (lines 82-105): Extracts multiplicity bounds

This implementation correctly:
- Walks ownership trees starting from PartUsages
- Follows typing relationships to get nested parts from PartDefinitions (critical for coffee_maker)
- Handles multiplicity extraction with cached bounds
- Filters stdlib elements via qualified name prefix checking

### Syside API Patterns

**Model Loading:**
```python
import syside
files = syside.collect_files_recursively(str(model_dir))
model, diagnostics = syside.try_load_model(files)
```

**Element Iteration:**
```python
for part in model.nodes(syside.PartUsage, include_subtypes=True):
    # Process each part usage
```

**Key Element Properties:**
| Property | Purpose |
|----------|---------|
| `element.declared_name` | Primary name |
| `element.owner` | Parent element |
| `element.owned_elements` | Direct children |
| `element.types` | Type definitions (for usages) |
| `element.owned_features` | Features defined on element |
| `element.declared_multiplicity` | Multiplicity specification |
| `element.qualified_name` | Full qualified path |
| `element.isinstance(syside.PartUsage)` | Type checking |

**Multiplicity Access:**
```python
mult = element.declared_multiplicity
if mult and mult.has_cached_bounds:
    lower = mult.cached_lower_bound  # int
    upper = mult.cached_upper_bound  # int or None
```

### Coffee Maker Model Analysis

The model spans two files with 10 extractable nodes:

**Hierarchy:**
```
coffee_maker (depth=0, design.sysml:16)
├── brewing (depth=1, type: Brewing System)
│   ├── heater (depth=2, multiplicity=[2,2])
│   ├── pump (depth=2)
│   └── chamber (depth=2)
├── reservoir (depth=1)
├── carafe (depth=1)
└── housing (depth=1)
    ├── shell (depth=2)
    └── panel (depth=2)
```

**Key extraction points:**
- Root `coffee_maker` is a PartUsage in design.sysml:16
- Children like `brewing` are PartUsages inside the `Coffee Maker` PartDefinition (library.sysml:470)
- Nested parts (heater, pump, chamber) are found by following the typing relationship to `Brewing System` definition (library.sysml:384)
- Multiplicity `[heater_count]` resolves to `[2,2]` via attribute default (library.sysml:397)

### Differences from Existing Implementation

The prototype in explore_ast.py produces slightly different output than what we need:

| Aspect | explore_ast.py | New Design |
|--------|----------------|------------|
| Node IDs | Python `id()` or `element_id` | Qualified path (e.g., `coffee_maker.brewing.heater`) |
| Type field | Python class name (`PartUsage`) | Mapped category (`"part"`) via explicit registry |
| Type name | `sysml_type` field | `type_name` field |
| Edges | Ad-hoc generation | Mapped edge types via explicit registry |
| Depth | Not tracked | `depth` field required |

### Design Principle: Abstraction Layers for Evolving APIs

Since syside is evolving, we need clean abstraction boundaries between:
1. **SysML/syside layer** - Raw metatypes (`PartUsage`, `AttributeUsage`, etc.)
2. **Visualization layer** - Simplified categories (`"part"`, `"attribute"`, etc.)

This is achieved through **explicit mapping registries** that:
- Centralize the translation logic
- Make it easy to add new mappings as SysML support expands
- Document the mapping decisions
- Enable type-safe access

---

## Proposed Design

### Architecture

```
proof_of_concept/extraction/
├── __init__.py           # Package exports
├── types.py              # TypedDict definitions + mapping registries
└── visualization.py      # extract_structural_view() function

proof_of_concept/tests/
└── test_visualization.py # Golden reference comparison tests

proof_of_concept/golden_references/
└── coffee_maker_structural.json  # UPDATE: use qualified path IDs
```

**Implementation tasks include:**
1. Create `types.py` with TypedDicts and mapping registries
2. Create `visualization.py` with extraction function
3. Update `coffee_maker_structural.json` to use qualified path IDs
4. Create `test_visualization.py` with golden reference comparison

### Component 1: Type Definitions and Mappings (`types.py`)

**Output Data Types:**

```python
from typing import TypedDict, Literal
from dataclasses import dataclass
from enum import Enum

# --- Visualization Categories (renderer-facing) ---

class ElementCategory(str, Enum):
    """Simplified element categories for visualization styling."""
    PART = "part"
    ATTRIBUTE = "attribute"
    CALCULATION = "calculation"
    # Add new categories here as visualization needs expand

class EdgeCategory(str, Enum):
    """Edge categories for visualization styling."""
    CONTAINMENT = "containment"
    # Future: DEPENDENCY = "dependency", FLOW = "flow", etc.

# --- Output TypedDicts ---

class StructuralNode(TypedDict):
    id: str                                      # Qualified path (e.g., "coffee_maker.brewing.heater")
    name: str                                    # Usage name (declared or from redefines)
    type_name: str                               # Definition name (e.g., "Coffee Maker")
    element_type: str                            # ElementCategory value (e.g., "part")
    parent: str | None                           # Parent node ID (qualified path)
    depth: int                                   # Hierarchy depth (0 = root)
    multiplicity: list[int] | None              # [lower, upper] or None

class ContainmentEdge(TypedDict):
    id: str                                      # "parent_path->child_path"
    source: str                                  # Parent node ID
    target: str                                  # Child node ID
    edge_type: str                               # EdgeCategory value (e.g., "containment")

class StructuralViewResult(TypedDict):
    nodes: list[StructuralNode]
    edges: list[ContainmentEdge]
    metadata: dict                               # view, root, total_nodes, max_depth
```

**Mapping Registries:**

```python
import syside

# --- SysML Metatype → Visualization Category Mapping ---

@dataclass(frozen=True)
class ElementTypeMapping:
    """Maps a syside metatype to a visualization category."""
    syside_type: type                # e.g., syside.PartUsage
    category: ElementCategory        # e.g., ElementCategory.PART
    include_in_structural: bool = True  # Whether to include in structural view

# Registry: Add new mappings here as syside/SysML support expands
ELEMENT_TYPE_REGISTRY: list[ElementTypeMapping] = [
    ElementTypeMapping(syside.PartUsage, ElementCategory.PART, include_in_structural=True),
    ElementTypeMapping(syside.AttributeUsage, ElementCategory.ATTRIBUTE, include_in_structural=False),
    ElementTypeMapping(syside.CalculationUsage, ElementCategory.CALCULATION, include_in_structural=False),
    # Future: ItemUsage, ConnectionUsage, etc.
]

def get_element_category(element) -> ElementCategory | None:
    """Look up visualization category for a syside element.

    Returns None if element type is not mapped (should be skipped).
    """
    for mapping in ELEMENT_TYPE_REGISTRY:
        if element.isinstance(mapping.syside_type):
            return mapping.category
    return None

def should_include_in_structural(element) -> bool:
    """Check if element should be included in structural view."""
    for mapping in ELEMENT_TYPE_REGISTRY:
        if element.isinstance(mapping.syside_type):
            return mapping.include_in_structural
    return False

# --- Edge Type Mapping ---

@dataclass(frozen=True)
class EdgeTypeMapping:
    """Maps a relationship type to a visualization edge category."""
    relationship: str                # e.g., "ownership", "dependency"
    category: EdgeCategory

EDGE_TYPE_REGISTRY: list[EdgeTypeMapping] = [
    EdgeTypeMapping("ownership", EdgeCategory.CONTAINMENT),
    # Future: EdgeTypeMapping("dependency", EdgeCategory.DEPENDENCY),
]

def get_edge_category(relationship: str) -> EdgeCategory:
    """Look up edge category for a relationship type."""
    for mapping in EDGE_TYPE_REGISTRY:
        if mapping.relationship == relationship:
            return mapping.category
    # Default fallback
    return EdgeCategory.CONTAINMENT
```

**Why this pattern:**
- **Centralized**: All SysML→Viz mappings in one place
- **Documented**: Each mapping is explicit with its purpose
- **Extensible**: Add new `ElementTypeMapping` entries as syside adds types
- **Type-safe**: Enums prevent typos in category strings
- **Testable**: Can unit test the mappings independently

### Component 2: Extraction Function (`visualization.py`)

**Public API:**
```python
def extract_structural_view(
    model,
    root: str | None = None,
    max_depth: int = 10,
    include_multiplicity: bool = True,
    exclude_stdlib: bool = True
) -> StructuralViewResult:
    """Extract structural (containment) view from SysML model.

    Args:
        model: Parsed syside model object
        root: Name of root part to start from (None = auto-detect)
        max_depth: Maximum hierarchy depth to traverse
        include_multiplicity: Whether to include multiplicity info
        exclude_stdlib: Whether to filter out standard library elements

    Returns:
        StructuralViewResult with nodes, edges, and metadata
    """
```

**Implementation Strategy:**

1. **Find root**: Locate root PartUsage by name, or find first top-level PartUsage in design document
2. **Recursive extraction**: Adapt `_extract_parts()` from explore_ast.py:490-570
3. **ID generation**: Build qualified paths (e.g., `coffee_maker.brewing.heater`)
4. **Type mapping**: Use `get_element_category()` to translate syside types
5. **Depth tracking**: Pass depth parameter through recursion
6. **Edge generation**: Create containment edges with `parent->child` IDs

**Key adaptations from explore_ast.py:**

| explore_ast.py | New implementation |
|----------------|-------------------|
| Lines 490-570: `_extract_parts()` | Adapt with qualified path IDs and mapping lookups |
| Lines 481-487: `_is_stdlib_element()` | Reuse as-is |
| Lines 82-105: `_get_multiplicity_str()` | Adapt to return `[lower, upper]` tuple |
| Lines 562-565: Follow typing | Critical pattern - follow `type_def.owned_features` |

**Helper Functions:**

```python
def _find_root_part(model, root_name: str | None):
    """Find the root PartUsage to start extraction."""

def _build_qualified_path(element_name: str, parent_path: str | None) -> str:
    """Build qualified path ID for an element.

    Examples:
        _build_qualified_path("coffee_maker", None) → "coffee_maker"
        _build_qualified_path("brewing", "coffee_maker") → "coffee_maker.brewing"
    """
    if parent_path:
        return f"{parent_path}.{element_name}"
    return element_name

def _build_edge_id(source_path: str, target_path: str) -> str:
    """Build edge ID from source and target paths.

    Example: "coffee_maker->brewing"
    """
    return f"{source_path}->{target_path}"

def _is_stdlib_element(element) -> bool:
    """Check if element is from SysML standard library."""
    # Reuse from explore_ast.py:481-487

def _get_multiplicity(element) -> list[int] | None:
    """Extract multiplicity as [lower, upper] or None."""

def _extract_node(
    element,
    parent_path: str | None,
    depth: int,
    nodes: list[StructuralNode],
    edges: list[ContainmentEdge],
    visited: set[str],
    config: ExtractionConfig
) -> None:
    """Recursively extract a node and its children.

    Uses mapping registries to translate syside types to visualization categories.
    """
```

### Component 3: Test Suite (`test_visualization.py`)

**Test Strategy:**
1. Load golden reference JSON
2. Load coffee_maker model via syside
3. Run extraction
4. Compare output to golden reference

**Test Cases:**

```python
def test_node_count():
    """Extraction produces exactly 10 nodes."""

def test_edge_count():
    """Extraction produces exactly 9 edges."""

def test_hierarchy_depth():
    """Maximum depth is 2."""

def test_root_node():
    """Root node is coffee_maker with Coffee Maker type."""

def test_multiplicity_extraction():
    """Heater has multiplicity [2, 2]."""

def test_containment_edges():
    """All parent-child relationships have containment edges."""

def test_structure_matches_golden_reference():
    """Full structural comparison to golden reference."""
```

### Data Flow

```
1. Load model
   syside.try_load_model([files])

2. Find root
   model.nodes(PartUsage) → filter for root name or design doc

3. Recursive extraction
   For each element:
     a. Check should_include_in_structural(element) via mapping registry
     b. Build qualified path ID: parent_path + "." + name
     c. Look up element_type via get_element_category(element)
     d. Create node with qualified path as ID
     e. Create containment edge if parent exists (ID: "parent->child")
     f. Follow typing → get type definition
     g. For each PartUsage in type_def.owned_features:
        Recurse (this gets nested parts)

4. Build result
   Return StructuralViewResult with nodes, edges, metadata
```

### ID Scheme

**Node IDs:** Qualified paths provide semantic meaning and stability.

| Node | ID |
|------|-----|
| coffee_maker | `coffee_maker` |
| brewing | `coffee_maker.brewing` |
| heater | `coffee_maker.brewing.heater` |
| shell | `coffee_maker.housing.shell` |

**Edge IDs:** Arrow notation showing relationship direction.

| Edge | ID |
|------|-----|
| coffee_maker contains brewing | `coffee_maker->brewing` |
| brewing contains heater | `coffee_maker.brewing->coffee_maker.brewing.heater` |

**Benefits:**
- Human-readable and debuggable
- Stable across extraction runs (same model = same IDs)
- Self-documenting hierarchy
- Can be used to look up elements in tests

**Golden reference update:** The golden reference (`coffee_maker_structural.json`) will be updated to use qualified paths instead of `n1`, `n2`.

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Multiplicity with expressions (not cached) | Medium | Fallback to pretty-print, log warning |
| Anonymous elements without redefines | Low | Use "(anonymous)" as name, log warning |
| Circular references in model | High | Track visited elements by qualified path |
| Model loading failures | Medium | Check diagnostics, fail gracefully with message |
| New syside metatype not in registry | Low | `get_element_category()` returns None, element skipped with warning |
| syside API changes | Medium | Mapping registry isolates changes to one file |

---

## Integration Strategy

This component is self-contained for the POC:
- Lives in `proof_of_concept/extraction/`
- No integration with existing fusion-tea code
- Item 3 will add CLI and converters on top of this

**Dependencies:**
- `syside` (already in pyproject.toml via sysml-codegen)
- `pytest` (needs to be added for testing)

---

## Validation Approach

### Automated Testing
- pytest tests in `proof_of_concept/tests/test_visualization.py`
- Golden reference comparison for coffee_maker model
- Run with: `uv run pytest proof_of_concept/tests/`

### Manual Verification
1. Run extraction on coffee_maker model
2. Inspect JSON output
3. Verify 10 nodes, 9 edges, max_depth 2
4. Verify heater has multiplicity [2, 2]

### Success Criteria
- [ ] All tests pass
- [ ] Output matches golden reference structure
- [ ] Handles edge cases gracefully (warnings, not crashes)

---

**Next Step:** After approval → `/_my_implement`
