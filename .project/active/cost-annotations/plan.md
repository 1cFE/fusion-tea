# Implementation Plan: Cost Annotations + Polish

**Status:** Draft
**Created:** 2026-01-19 01:23:56 UTC
**Last Updated:** 2026-01-19 01:23:56 UTC

## Source Documents

- **Spec:** `.project/active/cost-annotations/spec.md`
- **Design:** `.project/active/cost-annotations/design.md` ← See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
1. **Phase 1 (Refactor)** - De-risk by exposing existing evaluation logic as callable function
2. **Phase 2 (Integration)** - Wire cost computation into extraction pipeline
3. **Phase 3 (Golden Ref)** - Lock down expected values before UI work
4. **Phase 4 (UI)** - Pure frontend work with stable backend

**Overall Validation Approach:**
- Each phase starts with tests (where applicable)
- Existing tests must pass throughout
- Manual verification at end of each phase

---

## Phase 1: Refactor generate_costs.py for Reuse

### Goal

Extract cost evaluation logic from `generate_costs.py` into a callable function that visualization code can import. This is the riskiest part - we're modifying working code.

### Test Stencil (Write This First)

```python
# Test stencil for Phase 1 - validate refactored function works
# File: models/tests/coffee_maker/test_generate_costs.py (or inline test)

def test_compute_costs_returns_dict():
    """compute_costs returns dict mapping qualified paths to cost dicts."""
    from generate_costs import compute_costs

    result = compute_costs("models/tests/coffee_maker")

    assert isinstance(result, dict)
    assert "coffee_maker" in result
    assert "capital_cost" in result["coffee_maker"]

def test_compute_costs_values_match_existing():
    """Refactored function produces same values as before."""
    from generate_costs import compute_costs

    result = compute_costs("models/tests/coffee_maker")

    # Known values from existing generate_costs.py output
    assert abs(result["coffee_maker"]["capital_cost"] - 113.96) < 0.01
```

### Changes Required

**See `design.md#value-extraction-approach` for decision rationale.**

**Specific file changes:**

#### 1. Refactor generate_costs.py
**File:** `models/tests/coffee_maker/generate_costs.py`

- [x] Add new function `compute_costs(model_path: str) -> dict[str, dict[str, float]]`
- [x] Function should:
  - Load model
  - Run existing evaluation pipeline
  - Return dict mapping qualified paths (e.g., "coffee_maker.brewing.heater") to cost dicts
- [x] Keep existing `if __name__ == "__main__"` behavior unchanged
- [x] Existing script should still work identically when run directly

### Validation

**Automated:**
- [x] Run existing generate_costs.py script → Same output as before
- [x] Run test stencil above → Passes

**Manual:**
- [x] `uv run python models/tests/coffee_maker/generate_costs.py` → Prints cost table
- [x] Import and call: `from models.tests.coffee_maker.generate_costs import compute_costs; print(compute_costs("models/tests/coffee_maker"))`

**What We Know Works After This Phase:**
- Cost evaluation logic is accessible as a function
- Existing script behavior unchanged

---

## Phase 2: Cost Extraction Integration

### Goal

Wire the `compute_costs()` function into `extract_structural_view()` so nodes include cost data.

### Test Stencil (Write This First)

```python
# Test stencil for Phase 2 - cost extraction integration
# File: proof_of_concept/tests/test_visualization.py

def test_costs_field_present_when_requested(extracted_result_with_costs):
    """Nodes have costs field when cost extraction enabled."""
    for node in extracted_result_with_costs["nodes"]:
        assert "costs" in node

def test_backward_compatible_no_costs():
    """Extraction without cost attributes still works."""
    result = extract_structural_view(model, root="coffee_maker")
    assert len(result["nodes"]) == 10
    # costs field should be None
    assert result["nodes"][0].get("costs") is None
```

### Changes Required

**See `design.md#component-1` through `design.md#component-3` for details.**

**Specific file changes:**

#### 1. Update TypedDict
**File:** `proof_of_concept/extraction/types.py:49-68`

- [x] Add `costs: dict[str, float] | None` field to `StructuralNode`

#### 2. Add Cost Extraction Logic
**File:** `proof_of_concept/extraction/visualization.py`

- [x] Add `include_cost_attributes` parameter to `extract_structural_view()` (see `design.md#component-2`)
- [x] Import and call `compute_costs()` when cost attributes requested
- [x] In `_extract_node()`, look up costs by qualified path and populate `node["costs"]`
- [x] Update `_ExtractionConfig` dataclass to include cost attribute list

#### 3. Update Cytoscape Converter
**File:** `proof_of_concept/extraction/visualization.py:432-461`

- [x] Update `to_cytoscape()` to pass through costs (see `design.md#component-3`)
- [x] Flatten cost fields for Cytoscape `mapData` access

#### 4. Add Tests
**File:** `proof_of_concept/tests/test_visualization.py`

- [x] Add `extracted_result_with_costs` fixture (see `design.md#component-7`)
- [x] Add test stencil tests above
- [x] Add `test_cost_values_are_numeric`
- [x] Add `test_to_cytoscape_includes_costs`

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/` → All tests pass (including new ones)
- [x] Existing 24 tests still pass

**Manual:**
- [x] Python REPL: Extract with costs, inspect a node's `costs` dict

**What We Know Works After This Phase:**
- Extraction returns cost data when requested
- Cytoscape converter passes costs through
- Backward compatibility maintained

---

## Phase 3: Golden Reference + Value Tests

### Goal

Create golden reference with expected cost values; add tests validating extraction matches.

### Test Stencil (Write This First)

```python
# Test stencil for Phase 3 - golden reference comparison
# File: proof_of_concept/tests/test_visualization.py

GOLDEN_REF_COSTS = Path(__file__).parent.parent / "golden_references" / "coffee_maker_with_costs.json"

@pytest.fixture
def golden_reference_with_costs():
    with open(GOLDEN_REF_COSTS) as f:
        return json.load(f)

def test_costs_match_golden_reference(extracted_result_with_costs, golden_reference_with_costs):
    """Extracted costs match golden reference values."""
    for extracted_node in extracted_result_with_costs["nodes"]:
        golden_node = next(n for n in golden_reference_with_costs["nodes"] if n["id"] == extracted_node["id"])

        for attr, value in golden_node["costs"].items():
            assert abs(extracted_node["costs"][attr] - value) < 0.01, f"{extracted_node['id']}.{attr}"
```

### Changes Required

#### 1. Generate Golden Reference
**File:** `proof_of_concept/golden_references/coffee_maker_with_costs.json` (NEW)

- [x] Run `compute_costs()` to get expected values
- [x] Create JSON file matching structure in `design.md#component-6`
- [x] Include all 10 nodes with their cost values

#### 2. Add Golden Reference Tests
**File:** `proof_of_concept/tests/test_visualization.py`

- [x] Add fixture for loading golden reference with costs
- [x] Add `test_costs_match_golden_reference` comparing extracted vs expected

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/` → All pass including golden ref comparison

**Manual:**
- [x] Inspect golden reference JSON - values look reasonable
- [x] Compare a few values manually against generate_costs.py output

**What We Know Works After This Phase:**
- Cost values are correct and locked down
- Any future changes that break costs will be caught

---

## Phase 4: Web UI - Info Panel + Styling

### Goal

Display costs in info panel; add "Color by Cost" toggle with gradient coloring.

### Test Stencil

No automated tests for UI. Manual testing only.

### Changes Required

**See `design.md#component-4` and `design.md#component-5` for details.**

#### 1. Update Server
**File:** `proof_of_concept/web/server.py`

- [x] Add `DEFAULT_COST_ATTRIBUTES` constant (see `design.md#component-4`)
- [x] Pass `include_cost_attributes` to `extract_structural_view()`

#### 2. Update Info Panel
**File:** `proof_of_concept/web/static/index.html`

- [x] Add CSS for `.cost-table`, `.cost-row`, `.cost-name`, `.cost-value` (see `design.md#component-5`)
- [x] Add `formatCostName()` and `formatCostValue()` helper functions
- [x] Update `updateInfoPanel()` to show costs section

#### 3. Add Cost Styling Toggle
**File:** `proof_of_concept/web/static/index.html`

- [x] Add checkbox toggle in control bar (after export button)
- [x] Add `lerpColor()` function for color interpolation
- [x] Add `applyCostStyling(enabled)` function
- [x] Wire up toggle event handler

### Validation

**Automated:**
- [x] `uv run python -m pytest proof_of_concept/tests/` → All tests still pass

**Manual:**
- [x] Start server: `uv run python -m proof_of_concept.web`
- [x] Navigate to `http://localhost:8000`
- [x] Enter `models/tests/coffee_maker` and click Load
- [x] Click `heater` node → Info panel shows all 5 cost attributes
- [x] Click `coffee_maker` root → Info panel shows aggregated costs
- [x] Check "Color by Cost" toggle → Nodes change color (blue→red gradient)
- [x] Uncheck toggle → Colors reset to default blue
- [x] Export PNG with coloring enabled → Colors appear in export
- [x] No console errors in browser dev tools

**What We Know Works After This Phase:**
- Full end-to-end: model → extraction → API → UI with costs
- Info panel displays cost data
- Cost-based coloring works and is toggleable

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Key commands:
- Tests: `uv run python -m pytest proof_of_concept/tests/`
- Server: `uv run python -m proof_of_concept.web`
- Generate costs: `uv run python models/tests/coffee_maker/generate_costs.py`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Run existing script before and after to verify unchanged behavior
- **Phase 2**: Run full test suite after each file change
- **Phase 4**: Test expand/collapse still works after styling changes

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Renamed existing `compute_costs()` to `_compute_part_hierarchy_costs()` (internal function)
- Created new public `compute_costs(model_path: str) -> dict[str, dict[str, float]]` function
- Updated `main()` to call the renamed internal function
- Created `models/tests/coffee_maker/test_generate_costs.py` with 7 test cases

**Issues:**
- None - existing script still passes, all tests pass

**Deviations:**
- None - followed plan exactly

### Phase 2 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Added `costs: dict[str, float] | None` field to `StructuralNode` TypedDict in `types.py`
- Added `cost_data` field to `_ExtractionConfig` dataclass in `visualization.py`
- Added `include_cost_attributes` and `model_path` parameters to `extract_structural_view()`
- Updated `_extract_node()` to populate costs from pre-computed cost data
- Updated `to_cytoscape()` to pass through costs dict and flatten cost attributes
- Added 5 new tests to `test_visualization.py` for cost extraction

**Issues:**
- None - all 32 tests pass

**Deviations:**
- Added `model_path` parameter to `extract_structural_view()` (needed to call `compute_costs()`)

### Phase 3 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Created `proof_of_concept/golden_references/coffee_maker_with_costs.json` with all 10 nodes and their cost values
- Added `golden_reference_with_costs` fixture to `test_visualization.py`
- Added `test_costs_match_golden_reference` test comparing extracted vs expected costs

**Issues:**
- None - all 33 tests pass

**Deviations:**
- None - followed plan exactly

### Phase 4 Completion
**Completed:** 2026-01-19
**Actual Changes:**
- Updated `server.py` to pass `DEFAULT_COST_ATTRIBUTES` and `model_path` to `extract_structural_view()`
- Added CSS styles for cost display (`.cost-table`, `.cost-row`, `.cost-name`, `.cost-value`, `.toggle-label`)
- Added `formatCostName()` and `formatCostValue()` helper functions in `index.html`
- Updated `updateInfoPanel()` to display costs section when present
- Added "Color by Cost" toggle checkbox to control bar
- Added `lerpColor()` and `applyCostStyling()` functions for gradient coloring
- Updated `setButtonsEnabled()` to include cost styling toggle

**Issues:**
- None - all 33 tests pass, API returns costs correctly

**Deviations:**
- None - followed plan exactly

---

**Status**: Complete
