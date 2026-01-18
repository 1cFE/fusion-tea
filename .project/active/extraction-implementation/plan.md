# Implementation Plan: Extraction Implementation (POC Item 2)

**Status:** Complete
**Created:** 2026-01-18 21:24:33 UTC
**Last Updated:** 2026-01-18
**Branch:** visualization

## Source Documents

- **Spec:** `.project/active/extraction-implementation/spec.md`
- **Design:** `.project/active/extraction-implementation/design.md` ← See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
1. **Types first** - Establishes the contract and mapping pattern that everything builds on
2. **Tests second** - Test-first validates infrastructure before writing extraction logic
3. **Core logic third** - With types and tests ready, implement the main functionality
4. **Edge cases last** - Polish once core works

**Overall Validation Approach:**
- Each phase starts with tests (or test infrastructure)
- Each phase has automated + manual validation
- Golden reference comparison is the ultimate validation

---

## Phase 1: Types + Mapping Registries + Golden Reference Update

### Goal

Establish the abstraction layer (types, enums, mapping registries) and update the golden reference to use qualified path IDs. This is first because types define the contract everything else builds on, and the mapping registries are the key maintainability pattern.

### Test Stencil (Write This First)

```python
# proof_of_concept/tests/test_types.py
# Minimal tests for types module - validates imports and basic structure

import pytest

def test_element_category_enum():
    """ElementCategory enum has expected values."""
    from proof_of_concept.extraction.types import ElementCategory

    assert ElementCategory.PART.value == "part"
    assert ElementCategory.ATTRIBUTE.value == "attribute"

def test_edge_category_enum():
    """EdgeCategory enum has expected values."""
    from proof_of_concept.extraction.types import EdgeCategory

    assert EdgeCategory.CONTAINMENT.value == "containment"

def test_element_type_registry_exists():
    """ELEMENT_TYPE_REGISTRY is populated."""
    from proof_of_concept.extraction.types import ELEMENT_TYPE_REGISTRY

    assert len(ELEMENT_TYPE_REGISTRY) >= 1
```

### Changes Required

**See `design.md` for:**
- TypedDict definitions → `design.md#component-1-type-definitions-and-mappings-typepy`
- Enum definitions → `design.md#component-1-type-definitions-and-mappings-typepy`
- Mapping registries → `design.md#component-1-type-definitions-and-mappings-typepy`

**Specific file changes:**

#### 1. Package Init
**File:** `proof_of_concept/extraction/__init__.py` (NEW)
- [ ] Create empty `__init__.py` to make package importable

#### 2. Types Module
**File:** `proof_of_concept/extraction/types.py` (NEW)
- [ ] Create `ElementCategory` enum (see `design.md#component-1`)
- [ ] Create `EdgeCategory` enum
- [ ] Create `StructuralNode` TypedDict
- [ ] Create `ContainmentEdge` TypedDict
- [ ] Create `StructuralViewResult` TypedDict
- [ ] Create `ElementTypeMapping` dataclass
- [ ] Create `ELEMENT_TYPE_REGISTRY` list
- [ ] Create `get_element_category()` function
- [ ] Create `should_include_in_structural()` function
- [ ] Create `EdgeTypeMapping` dataclass
- [ ] Create `EDGE_TYPE_REGISTRY` list
- [ ] Create `get_edge_category()` function

#### 3. Golden Reference Update
**File:** `proof_of_concept/golden_references/coffee_maker_structural.json` (UPDATE)
- [ ] Change node IDs from `n1`, `n2` to qualified paths (see `design.md#id-scheme`)
- [ ] Change edge IDs from `e1`, `e2` to `parent->child` format
- [ ] Update `source`/`target` fields in edges to use qualified paths
- [ ] Update `parent` fields in nodes to use qualified paths

### Validation (How to Verify This Phase)

**Automated:**
- [ ] `uv run python -c "from proof_of_concept.extraction.types import *"` → No import errors
- [ ] `uv run python -c "from proof_of_concept.extraction.types import ELEMENT_TYPE_REGISTRY; print(len(ELEMENT_TYPE_REGISTRY))"` → Prints `3`

**Manual:**
- [ ] Open `coffee_maker_structural.json` and verify IDs are qualified paths
- [ ] Verify first node has `"id": "coffee_maker"` not `"id": "n1"`

**What We Know Works After This Phase:**
- Types module imports without errors
- Mapping registries are populated
- Golden reference has correct ID format for test comparison

---

## Phase 2: Test Infrastructure + Minimal Extraction Skeleton

### Goal

Write failing tests that define success criteria, then create a minimal extraction skeleton that loads the model. This de-risks model loading early - if syside can't load coffee_maker, we find out immediately.

### Test Stencil (Write This First)

```python
# proof_of_concept/tests/test_visualization.py
import json
from pathlib import Path
import pytest

# Paths
GOLDEN_REF = Path(__file__).parent.parent / "golden_references" / "coffee_maker_structural.json"
MODEL_DIR = Path(__file__).parent.parent.parent / "models" / "tests" / "coffee_maker"


@pytest.fixture
def golden_reference():
    """Load golden reference JSON."""
    with open(GOLDEN_REF) as f:
        return json.load(f)


@pytest.fixture
def extracted_result():
    """Run extraction on coffee_maker model."""
    from proof_of_concept.extraction.visualization import extract_structural_view
    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, diagnostics = syside.try_load_model(files)
    assert not diagnostics.contains_errors(), f"Model load failed: {diagnostics}"

    return extract_structural_view(model, root="coffee_maker")


def test_node_count(extracted_result, golden_reference):
    """Extraction produces exactly 10 nodes."""
    assert len(extracted_result["nodes"]) == len(golden_reference["nodes"])


def test_edge_count(extracted_result, golden_reference):
    """Extraction produces exactly 9 edges."""
    assert len(extracted_result["edges"]) == len(golden_reference["edges"])


def test_root_node_exists(extracted_result):
    """Root node is coffee_maker."""
    node_ids = [n["id"] for n in extracted_result["nodes"]]
    assert "coffee_maker" in node_ids


def test_multiplicity_on_heater(extracted_result):
    """Heater has multiplicity [2, 2]."""
    heater = next(n for n in extracted_result["nodes"] if n["name"] == "heater")
    assert heater["multiplicity"] == [2, 2]
```

### Changes Required

**See `design.md` for:**
- Test strategy → `design.md#component-3-test-suite-test_visualizationpy`
- Function signature → `design.md#component-2-extraction-function-visualizationpy`

**Specific file changes:**

#### 1. Add pytest dependency
**File:** `pyproject.toml` (UPDATE)
- [ ] Add `pytest` to dependencies

#### 2. Test Package Init
**File:** `proof_of_concept/tests/__init__.py` (NEW)
- [ ] Create empty `__init__.py`

#### 3. Test Module
**File:** `proof_of_concept/tests/test_visualization.py` (NEW)
- [ ] Create test file with stencil above
- [ ] Implement fixtures: `golden_reference`, `extracted_result`
- [ ] Implement tests: `test_node_count`, `test_edge_count`, `test_root_node_exists`, `test_multiplicity_on_heater`

#### 4. Extraction Skeleton
**File:** `proof_of_concept/extraction/visualization.py` (NEW - skeleton)
- [ ] Create file with `extract_structural_view()` function signature
- [ ] Return empty `StructuralViewResult` (tests will fail, but import works)
- [ ] Add model loading validation (check diagnostics)

### Validation (How to Verify This Phase)

**Automated:**
- [ ] `uv run pytest proof_of_concept/tests/test_visualization.py -v` → Tests run (most fail, but no import/load errors)
- [ ] Model loading succeeds (fixture doesn't crash)

**Manual:**
- [ ] Run: `uv run python -c "import syside; m, d = syside.try_load_model(syside.collect_files_recursively('models/tests/coffee_maker')); print('loaded' if not d.contains_errors() else d)"`
- [ ] Verify: Prints "loaded"

**What We Know Works After This Phase:**
- pytest runs in the project
- syside loads coffee_maker model without errors
- Test infrastructure ready for extraction implementation

---

## Phase 3: Core Extraction Logic

### Goal

Implement the recursive extraction that produces correct nodes and edges. This is the core functionality - walking the model, building qualified paths, following typing relationships, and generating the output structure.

### Test Stencil (Extend Existing)

```python
# Add to test_visualization.py

def test_hierarchy_depth(extracted_result):
    """Maximum depth is 2."""
    max_depth = max(n["depth"] for n in extracted_result["nodes"])
    assert max_depth == 2


def test_qualified_path_ids(extracted_result):
    """Node IDs are qualified paths."""
    node_ids = [n["id"] for n in extracted_result["nodes"]]
    assert "coffee_maker.brewing" in node_ids
    assert "coffee_maker.brewing.heater" in node_ids


def test_containment_edges(extracted_result):
    """Edges connect parents to children."""
    edge_sources = {e["source"] for e in extracted_result["edges"]}
    edge_targets = {e["target"] for e in extracted_result["edges"]}

    # coffee_maker should be a source (has children)
    assert "coffee_maker" in edge_sources
    # brewing.heater should be a target (is a child)
    assert "coffee_maker.brewing.heater" in edge_targets


def test_type_names_extracted(extracted_result):
    """Type names are extracted from definitions."""
    root = next(n for n in extracted_result["nodes"] if n["id"] == "coffee_maker")
    assert root["type_name"] == "Coffee Maker"


def test_structure_matches_golden_reference(extracted_result, golden_reference):
    """Full structural comparison."""
    # Compare node names (order-independent)
    extracted_names = {n["name"] for n in extracted_result["nodes"]}
    golden_names = {n["name"] for n in golden_reference["nodes"]}
    assert extracted_names == golden_names

    # Compare edge count
    assert len(extracted_result["edges"]) == len(golden_reference["edges"])
```

### Changes Required

**See `design.md` for:**
- Data flow → `design.md#data-flow`
- Helper functions → `design.md#component-2-extraction-function-visualizationpy`
- Key patterns from explore_ast.py → `design.md#research-findings`

**Specific file changes:**

#### 1. Complete Extraction Implementation
**File:** `proof_of_concept/extraction/visualization.py` (COMPLETE)
- [ ] Implement `_find_root_part()` - find root PartUsage by name or auto-detect
- [ ] Implement `_build_qualified_path()` - build `parent.child` paths
- [ ] Implement `_build_edge_id()` - build `parent->child` edge IDs
- [ ] Implement `_is_stdlib_element()` - reuse from explore_ast.py:481-487
- [ ] Implement `_get_multiplicity()` - return `[lower, upper]` or None
- [ ] Implement `_extract_node()` - recursive extraction with:
  - Qualified path ID generation
  - Type lookup via `get_element_category()`
  - Depth tracking
  - Edge creation
  - **Critical:** Follow typing to get children from PartDefinitions (explore_ast.py:562-565)
- [ ] Complete `extract_structural_view()` - orchestrate extraction and build result

### Validation (How to Verify This Phase)

**Automated:**
- [ ] `uv run pytest proof_of_concept/tests/test_visualization.py -v` → All tests pass
- [ ] `uv run pytest proof_of_concept/tests/ -v` → Full test suite passes

**Manual:**
- [ ] Run extraction and print result:
  ```bash
  uv run python -c "
  import json
  import syside
  from proof_of_concept.extraction.visualization import extract_structural_view

  files = syside.collect_files_recursively('models/tests/coffee_maker')
  model, _ = syside.try_load_model(files)
  result = extract_structural_view(model, root='coffee_maker')
  print(json.dumps(result, indent=2))
  "
  ```
- [ ] Verify: 10 nodes, 9 edges, heater has `multiplicity: [2, 2]`

**What We Know Works After This Phase:**
- Extraction produces correct structure matching golden reference
- Qualified path IDs work correctly
- Typing relationships followed to get nested parts
- Multiplicity extracted correctly

---

## Phase 4: Edge Cases + Polish

### Goal

Handle edge cases gracefully (warnings not crashes), ensure unmapped types are logged, and verify stdlib filtering works correctly.

### Test Stencil (Edge Case Tests)

```python
# Add to test_visualization.py or create test_edge_cases.py

def test_stdlib_elements_excluded(extracted_result):
    """Standard library elements are not in output."""
    node_names = {n["name"] for n in extracted_result["nodes"]}
    # These are common stdlib elements that should be filtered
    assert "start" not in node_names
    assert "done" not in node_names


def test_all_nodes_have_element_type(extracted_result):
    """Every node has element_type field."""
    for node in extracted_result["nodes"]:
        assert "element_type" in node
        assert node["element_type"] == "part"  # For structural view


def test_metadata_present(extracted_result):
    """Metadata contains expected fields."""
    meta = extracted_result["metadata"]
    assert meta["view"] == "structural"
    assert meta["root"] == "coffee_maker"
    assert meta["total_nodes"] == 10
    assert meta["max_depth"] == 2
```

### Changes Required

**See `design.md` for:**
- Risks and mitigations → `design.md#potential-risks`
- Stdlib filtering → explore_ast.py:481-487

**Specific file changes:**

#### 1. Edge Case Handling
**File:** `proof_of_concept/extraction/visualization.py` (UPDATE)
- [ ] Add logging for unmapped syside types (warning, not error)
- [ ] Handle anonymous elements: use "(anonymous)" as name, log warning
- [ ] Ensure stdlib filtering works via `_is_stdlib_element()`
- [ ] Add metadata generation with correct counts

#### 2. Additional Edge Case Tests
**File:** `proof_of_concept/tests/test_visualization.py` (UPDATE)
- [ ] Add `test_stdlib_elements_excluded`
- [ ] Add `test_all_nodes_have_element_type`
- [ ] Add `test_metadata_present`

### Validation (How to Verify This Phase)

**Automated:**
- [ ] `uv run pytest proof_of_concept/tests/ -v` → All tests pass
- [ ] No warnings about unmapped types for coffee_maker model

**Manual:**
- [ ] Verify metadata in output has correct counts
- [ ] Verify no stdlib elements in output (no "start", "done")

**What We Know Works After This Phase:**
- All acceptance criteria from spec met
- Edge cases handled gracefully
- Ready for Item 3 (CLI and converters)

---

## Environment Setup

**See CLAUDE.md for full environment rules**

**Key commands:**
- Run tests: `uv run pytest proof_of_concept/tests/ -v`
- Run single test: `uv run pytest proof_of_concept/tests/test_visualization.py::test_node_count -v`
- Python REPL: `uv run python`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 2**: Model loading tested in isolation via fixture
- **Phase 3**: Following typing pattern proven in explore_ast.py - adapt carefully
- **Phase 4**: Logging for unmapped types prevents silent failures

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-01-18 ~21:45 UTC
**Actual Changes:**
- Created `proof_of_concept/extraction/__init__.py` with package exports
- Created `proof_of_concept/extraction/types.py` with:
  - `ElementCategory` and `EdgeCategory` enums
  - `StructuralNode`, `ContainmentEdge`, `StructuralViewResult` TypedDicts
  - `ElementTypeMapping` dataclass and `ELEMENT_TYPE_REGISTRY` (3 entries)
  - `EdgeTypeMapping` dataclass and `EDGE_TYPE_REGISTRY` (1 entry)
  - `get_element_category()`, `should_include_in_structural()`, `get_edge_category()` functions
- Updated `coffee_maker_structural.json` with qualified path IDs (e.g., `coffee_maker.brewing.heater`)
- Created `proof_of_concept/tests/__init__.py`
- Created `proof_of_concept/tests/conftest.py` to configure Python path
- Created `proof_of_concept/tests/test_types.py` with 7 tests (all passing)
- Added `pytest>=8.0` to `pyproject.toml` dependencies

**Issues:**
- pytest couldn't find `proof_of_concept` module initially → Fixed by adding `conftest.py` with sys.path configuration

**Deviations:**
- Added `conftest.py` (not in original plan) to fix import path for tests
- Added pytest dependency in Phase 1 instead of Phase 2 (needed to run Phase 1 tests)

### Phase 2 Completion
**Completed:** 2026-01-18 ~21:50 UTC
**Actual Changes:**
- Created `proof_of_concept/tests/test_visualization.py` with:
  - `golden_reference` fixture - loads golden reference JSON
  - `extracted_result` fixture - loads model and runs extraction
  - 4 tests: `test_node_count`, `test_edge_count`, `test_root_node_exists`, `test_multiplicity_on_heater`
- Created `proof_of_concept/extraction/visualization.py` with:
  - `extract_structural_view()` function signature matching spec
  - Stub implementation returning empty `StructuralViewResult`

**Issues:**
- None

**Deviations:**
- pytest dependency was already added in Phase 1
- Test package init already existed from Phase 1

### Phase 3 Completion
**Completed:** 2026-01-18 ~22:00 UTC
**Actual Changes:**
- Implemented full `visualization.py` with:
  - `_ExtractionConfig` dataclass for configuration
  - `_find_root_part()` - finds root PartUsage by name or auto-detect
  - `_build_qualified_path()` - builds `parent.child` path IDs
  - `_build_edge_id()` - builds `parent->child` edge IDs
  - `_is_stdlib_element()` - filters stdlib elements
  - `_get_multiplicity()` - extracts `[lower, upper]` bounds
  - `_get_element_name()` - gets name from declared or redefinitions
  - `_get_type_name()` - gets type definition name
  - `_extract_node()` - recursive extraction following typing relationships
  - `extract_structural_view()` - main orchestration function
- Added 5 new tests to `test_visualization.py`:
  - `test_hierarchy_depth`, `test_qualified_path_ids`, `test_containment_edges`
  - `test_type_names_extracted`, `test_structure_matches_golden_reference`

**Issues:**
- Initial extraction showed `heater.multiplicity = [2, 3]` due to syside bug
  - Root cause: syside `cached_upper_bound` has off-by-one bug (returns value+1)
  - See: `.project/research/20260118-220500_syside-multiplicity-caching-bug.md`
  - Fixed by applying workaround: use `cached_upper_bound - 1` for expression-based multiplicities

**Deviations:**
- Added `_get_element_name()` and `_get_type_name()` helpers (not in original plan but needed)

### Phase 4 Completion
**Completed:** 2026-01-18 ~22:15 UTC
**Actual Changes:**
- Added 3 edge case tests to `test_visualization.py`:
  - `test_stdlib_elements_excluded` - verifies 'start'/'done' not in output
  - `test_all_nodes_have_element_type` - verifies all nodes have element_type='part'
  - `test_metadata_present` - verifies metadata has view, root, total_nodes, max_depth
- Added logging to `visualization.py`:
  - Warning for anonymous elements in `_get_element_name()`
  - Warning for unmapped syside types in `_extract_node()`

**Issues:**
- None

**Deviations:**
- None

---

**Status**: Draft → In Progress → Complete
