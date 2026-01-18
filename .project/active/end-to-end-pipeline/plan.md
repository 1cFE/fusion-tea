# Implementation Plan: End-to-End Pipeline (POC Item 3)

**Status:** Complete
**Created:** 2026-01-18
**Last Updated:** 2026-01-18

## Source Documents
- **Spec:** `.project/active/end-to-end-pipeline/spec.md`
- **Design:** `.project/active/end-to-end-pipeline/design.md` ← See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 builds the core converters first since they're the actual functionality - the CLI is just a thin wrapper. Phase 2 adds the CLI and model loading helper. Phase 3 is manual validation to confirm the business goal (end-to-end pipeline works).

**Overall Validation Approach:**
- Each phase starts with tests
- Automated tests via `uv run pytest proof_of_concept/tests/`
- Manual validation confirms integration with Cytoscape demo and Graphviz

---

## Phase 1: Format Converters + Tests

### Goal
Implement `to_cytoscape()` and `to_dot()` converters with full test coverage. This is the core functionality - everything else wraps these.

### Test Stencil (Write This First)
```python
# Add to proof_of_concept/tests/test_visualization.py

def test_to_cytoscape_format(extracted_result):
    """to_cytoscape returns correct structure."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result)

    assert "elements" in result
    assert len(result["elements"]) == 10  # 10 nodes
    assert all("data" in el for el in result["elements"])

def test_to_cytoscape_labels(extracted_result):
    """Labels include multiplicity notation."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result)
    labels = {el["data"]["label"] for el in result["elements"]}

    assert "heater [2]" in labels  # Has multiplicity
    assert "pump" in labels        # No multiplicity

def test_to_dot_contains_structure(extracted_result):
    """DOT output has expected keywords."""
    from proof_of_concept.extraction.visualization import to_dot

    result = to_dot(extracted_result)

    assert "digraph" in result
    assert "subgraph cluster_" in result
    assert "coffee_maker" in result
```

### Changes Required

**See `design.md` for:**
- `to_cytoscape()` signature and logic → `design.md#component-1-to_cytoscape-function`
- `to_dot()` signature and logic → `design.md#component-2-to_dot-function`
- Label formatting helper → `design.md#component-1-to_cytoscape-function`

**Specific file changes:**

#### 1. Test File (write first)
**File:** `proof_of_concept/tests/test_visualization.py` (MODIFY)
- [x] Add `test_to_cytoscape_format`
- [x] Add `test_to_cytoscape_labels`
- [x] Add `test_to_dot_contains_structure`

#### 2. Implementation
**File:** `proof_of_concept/extraction/visualization.py` (MODIFY - add at end)
- [x] Add `_format_label()` helper (see `design.md#component-1`)
- [x] Add `to_cytoscape()` function
- [x] Add `_escape_dot_id()` helper for DOT ID escaping
- [x] Add `_build_dot_label()` helper for DOT node label formatting
- [x] Add `to_dot()` function with recursive `emit_node_or_cluster()` inner function

### Validation

**Automated:**
- [x] `uv run pytest proof_of_concept/tests/test_visualization.py -v` → All pass (including new tests)
- [x] `uv run pytest proof_of_concept/tests/` → No regressions (22/22 passed)

**Manual:**
- [ ] Import and call `to_cytoscape()` in Python REPL, inspect output structure

**What We Know Works After This Phase:**
- Converters produce correctly formatted output
- Label formatting handles multiplicity correctly
- DOT output has proper structure

---

## Phase 2: Model Loading Helper + CLI

### Goal
Add `load_model()` helper and CLI entry point so the full pipeline can be invoked from command line.

### Test Stencil (Write This First)
```python
# Add to proof_of_concept/tests/test_visualization.py

def test_load_model_valid_path():
    """load_model loads coffee_maker model."""
    from proof_of_concept.extraction.visualization import load_model

    model = load_model(MODEL_DIR)

    assert model is not None

def test_load_model_invalid_path():
    """load_model raises ValueError for bad path."""
    from proof_of_concept.extraction.visualization import load_model
    import pytest

    with pytest.raises(ValueError, match="not found"):
        load_model("/nonexistent/path")
```

### Changes Required

**See `design.md` for:**
- `load_model()` signature and logic → `design.md#component-4-model-loading-helper`
- CLI structure and args → `design.md#component-3-cli-entry-point`
- Error handling → `design.md#component-3-cli-entry-point`

**Specific file changes:**

#### 1. Test File (write first)
**File:** `proof_of_concept/tests/test_visualization.py` (MODIFY)
- [x] Add `test_load_model_valid_path`
- [x] Add `test_load_model_invalid_path`

#### 2. Model Loading Helper
**File:** `proof_of_concept/extraction/visualization.py` (MODIFY)
- [x] Add `load_model()` function (see `design.md#component-4`)

#### 3. CLI Entry Point
**File:** `proof_of_concept/extraction/__main__.py` (NEW)
- [x] Create file with `main()` function per `design.md#component-3`
- [x] Add argparse setup for: `model_path`, `--format`, `--output`, `--root`
- [x] Add error handling for invalid paths and model errors

#### 4. Exports
**File:** `proof_of_concept/extraction/__init__.py` (MODIFY)
- [x] Add exports: `load_model`, `to_cytoscape`, `to_dot`, `extract_structural_view`

### Validation

**Automated:**
- [x] `uv run pytest proof_of_concept/tests/` → All pass (24/24)

**Manual:**
- [x] `uv run python -m proof_of_concept.extraction models/tests/coffee_maker` → JSON output
- [x] `uv run python -m proof_of_concept.extraction models/tests/coffee_maker --format=dot` → DOT output
- [x] `uv run python -m proof_of_concept.extraction /bad/path` → Error message

**What We Know Works After This Phase:**
- Model loading works for directories
- CLI produces JSON and DOT output
- Error handling provides clear messages

---

## Phase 3: Integration Validation

### Goal
Verify the end-to-end pipeline works with downstream tools (Cytoscape demo, Graphviz).

### Changes Required
No code changes - validation only.

### Validation

**Cytoscape Integration:**
- [x] Run: `uv run python -m proof_of_concept.extraction models/tests/coffee_maker`
- [x] Validated JSON structure matches Cytoscape demo format (10 elements, all required fields, correct parent/label/multiplicity)
- [ ] Manual: Copy JSON output, paste into `cytoscape_demo.html` replacing `goldenReference`, verify renders

**Graphviz Integration:**
- [x] Generated DOT file: `uv run python -m proof_of_concept.extraction models/tests/coffee_maker --format=dot -o /tmp/coffee_maker.dot`
- [x] Validated DOT syntax (3 clusters, 7 leaf nodes, balanced braces, correct labels)
- [ ] Manual (requires Graphviz install): `dot -Tpng /tmp/coffee_maker.dot -o /tmp/coffee_maker.png`

**What We Know Works After This Phase:**
- Full pipeline: model file → extraction → JSON → Cytoscape diagram
- Full pipeline: model file → extraction → DOT → Graphviz PNG
- Business goal achieved

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Key commands:
- Run tests: `uv run pytest proof_of_concept/tests/ -v`
- Run CLI: `uv run python -m proof_of_concept.extraction.visualization <path>`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: DOT nesting complexity → Use recursive helper, test with 3-level hierarchy
- **Phase 2**: No additional risks

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-01-18
**Changes Made:**
- Added 3 tests to `proof_of_concept/tests/test_visualization.py:134-164`:
  - `test_to_cytoscape_format` - validates elements structure and count
  - `test_to_cytoscape_labels` - validates multiplicity notation in labels
  - `test_to_dot_contains_structure` - validates DOT keywords
- Added functions to `proof_of_concept/extraction/visualization.py:369-518`:
  - `_format_label()` - formats name with multiplicity notation
  - `to_cytoscape()` - converts StructuralViewResult to Cytoscape.js format
  - `_escape_dot_id()` - escapes dots in IDs for DOT format
  - `_build_dot_label()` - formats DOT labels with name, multiplicity, type
  - `to_dot()` - converts StructuralViewResult to DOT with nested clusters

**Issues Encountered:**
- None

**Deviations from Plan:**
- Plan listed `_build_dot_node()` and `_build_dot_subgraph()` as separate helpers
- Implementation uses `_escape_dot_id()`, `_build_dot_label()`, and an inner function `emit_node_or_cluster()` instead
- This approach is cleaner: single recursive function handles both leaf and cluster nodes

### Phase 2 Completion
**Completed:** 2026-01-18
**Changes Made:**
- Added 2 tests to `proof_of_concept/tests/test_visualization.py:172-186`:
  - `test_load_model_valid_path` - validates model loading works
  - `test_load_model_invalid_path` - validates ValueError on bad path
- Added `load_model()` function to `proof_of_concept/extraction/visualization.py:378-405`
- Created `proof_of_concept/extraction/__main__.py` with CLI entry point
- Updated `proof_of_concept/extraction/__init__.py` with new exports

**Issues Encountered:**
- Type hint `str | "Path"` caused TypeError; fixed by adding `from __future__ import annotations`

**Deviations from Plan:**
- CLI invocation is `python -m proof_of_concept.extraction` (not `.visualization`)
- Plan had inconsistent paths; using package `__main__.py` is cleaner separation of concerns

### Phase 3 Completion
**Completed:** 2026-01-18
**Changes Made:**
- No code changes (validation only)

**Validation Results:**
- JSON output: 10 elements with correct structure (id, label, name, type_name, element_type, parent, depth, multiplicity)
- JSON labels: Correctly include multiplicity notation (e.g., "heater [2]")
- DOT output: Valid syntax with 3 nested clusters (coffee_maker, brewing, housing) and 7 leaf nodes
- DOT labels: Include name, multiplicity, and type (e.g., "heater [2] : Heating Element")

**Issues Encountered:**
- Graphviz (`dot` command) not installed on system; validated DOT syntax programmatically instead

**Manual Steps Remaining (for user):**
1. Copy JSON output into `cytoscape_demo.html` to visually verify rendering
2. Install Graphviz and run `dot -Tpng /tmp/coffee_maker.dot -o /tmp/coffee_maker.png` to verify PNG output

---

**Status**: Draft → In Progress → Complete
