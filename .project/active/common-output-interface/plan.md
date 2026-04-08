# Implementation Plan: Common Output Interface

**Status:** Draft
**Created:** 2026-04-06
**Last Updated:** 2026-04-06

## Source Documents
- **Spec:** `.project/active/common-output-interface/spec.md`
- **Design:** `.project/active/common-output-interface/design.md` ← See here for component details, detection logic, schema examples

## Implementation Strategy

**Phasing Rationale:**
Phase 1 (extractor routing) fixes the root cause blocking 5/11 concepts and proves the import-based detection pattern. Phase 2 (run_model validation) reuses that pattern for pipeline-time warnings. Phase 3 (templates + checklist) is pure content with no code dependencies and only affects future pipeline runs.

---

## Phase 1: Extractor Routing Fix

### Goal
Fix `extract_explorer_data.py` so freeform `model_setup.py` scripts route to the standalone pathway instead of the costingfe pathway. Also add `compute_sensitivity()` extraction support and prefer `model_setup.py` in standalone file discovery.

### Test Stencil (Write This First)
```python
# test_extraction.py — new tests for routing fix

class TestRoutingDetection:
    def test_freeform_model_setup_routes_to_standalone(self, tmp_path):
        """model_setup.py without costingfe import → standalone pathway."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False)
        (concept_dir / "model_setup.py").write_text(
            "# freeform\nparams = None\n"
            "def to_explorer_dict(): return {}\n"
        )
        # Patch load_module, call run_extraction, assert standalone path taken

    def test_costingfe_model_setup_routes_to_costingfe(self, tmp_path):
        """model_setup.py with CostModel import → costingfe pathway."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False)
        (concept_dir / "model_setup.py").write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel(...)\nresult = model.forward(...)\n"
        )
        # Assert costingfe path taken

    def test_standalone_prefers_model_setup_py(self, tmp_path):
        """When model_setup.py exists alongside other .py, it's loaded first."""
        # Create both aaa_script.py and model_setup.py
        # Assert model_setup.py is the one loaded

    def test_compute_sensitivity_populates_sensitivities(self, tmp_path):
        """Standalone module with compute_sensitivity() → has_sensitivities=True."""
        # Mock module with to_explorer_dict + compute_sensitivity
        # Assert sensitivities populated
```

### Changes Required

**See `design.md#component-3` for:** routing logic, detection code, standalone pathway enhancement, sensitivity extraction helper.

**Specific file changes:**

#### 1. Test File
**File:** `exploration/concept_explorer/tests/test_extraction.py` (MODIFY — write first)
- [x] Add `TestRoutingDetection` class with 4 tests above
- [x] Add test for `compute_sensitivity()` extraction into `SensitivityAnalysis`
- [x] Add test: costingfe-constants-only import (has `import costingfe` but no `CostModel`) → standalone

#### 2. Extractor Routing
**File:** `exploration/concept_explorer/extract_explorer_data.py`
- [x] Change routing logic at line ~554: replace filename check with import-based detection (`"CostModel" in source and ("from costingfe" in source or "import costingfe" in source)`)
- [x] Add comment noting parallel with `run_model()` detection (Component 2)
- [x] In `extract_standalone()`: prefer `model_setup.py` over alphabetical first `.py` file (lines ~246-249)
- [x] In `extract_standalone()`: after `to_explorer_dict()` call, check for `compute_sensitivity()` and build `SensitivityAnalysis`
- [x] Add `_build_sensitivity_from_dict()` helper — wraps `{eng: {k: elast}, fin: {k: elast}}` into `SensitivityAnalysis` with `SensitivityEntry` objects

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_extraction.py -v` → all pass (old + new) — 44 passed
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -v` → full explorer test suite passes — 153 passed, 2 skipped

**Manual:**
- [ ] Run extraction on a known freeform concept: `uv run python exploration/concept_explorer/extract_explorer_data.py --concept 12 --skip-narrative` → should route to standalone (no `ExtractionError`)
- [ ] Run extraction on a known costingfe concept: `--concept 01 --skip-narrative` → should still work via costingfe pathway

**What We Know Works After This Phase:**
Freeform scripts (02, 12, 15, 22) route to standalone extraction. Costingfe scripts unaffected. Sensitivity extraction from `compute_sensitivity()` works.

---

## Phase 2: Post-Generation Validation in `run_model()`

### Goal
Add interface conformance warnings to `run_model()` so the pipeline flags non-conforming scripts at generation time. Warnings only — no return type change, no caller changes.

### Test Stencil (Write This First)
```python
# test_claude.py — new tests for interface validation

class TestRunModelInterfaceValidation:
    def test_conforming_costingfe_no_warnings(self, tmp_path, capsys):
        """Script with 'from costingfe...' and 'result = ...' → no warnings."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel(...)\nresult = model.forward(...)\n"
            "print('LCOE: 75.0 $/MWh')\n"
        )
        # Mock subprocess, check no stderr warnings

    def test_missing_result_warns(self, tmp_path, capsys):
        """costingfe script without module-level result → warning on stderr."""
        # Script with CostModel import but no 'result = '

    def test_freeform_missing_to_explorer_dict_warns(self, tmp_path, capsys):
        """Freeform script without to_explorer_dict → warning on stderr."""

    def test_freeform_with_to_explorer_dict_no_warnings(self, tmp_path, capsys):
        """Freeform script with to_explorer_dict → no warnings."""
```

### Changes Required

**See `design.md#component-2` for:** detection logic, source scanning approach, FR-4 deviation rationale.

**Specific file changes:**

#### 1. Test File
**File:** `exploration/concept_analysis/scripts/test_claude.py` (MODIFY — write first)
- [x] Add `TestCheckInterface` class with 5 tests (conforming costingfe, missing result, freeform missing to_explorer_dict, freeform with to_explorer_dict, indented result)
- [x] Tests use capsys to check stderr for warnings (direct _check_interface calls, no subprocess mocking needed)

#### 2. Validation Logic
**File:** `exploration/concept_analysis/scripts/lib/claude.py`
- [x] Add `_check_interface(model_path: Path) -> None` helper after `run_model()` — reads source, detects type, prints warnings to stderr
- [x] Call `_check_interface(model_path)` at end of `run_model()` after successful execution (after `output_path.write_text(...)`)
- [x] Add comment noting detection logic parallels `extract_explorer_data.py` routing

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_claude.py -v` → all pass — 22 passed
- [x] Existing `test_claude.py` tests still pass (no return type change)

**Manual:**
- [ ] Temporarily run `run_model()` against a known non-conforming script (e.g., concept 12's freeform `model_setup.py`) → should see warning on stderr

**What We Know Works After This Phase:**
Pipeline warns on non-conforming scripts. Existing callers unaffected (return type unchanged).

---

## Phase 3: Prompt Templates + Assessment Checklist

### Goal
Update generation templates so future scripts conform to the output interface, and add a data model integrity check to the assessment checklist.

### Test Stencil
No automated tests — these are prompt template content changes. Validation is by reading.

### Changes Required

**See `design.md#component-1` for:** exact template additions (costingfe output interface section, freeform output interface section with schema and `compute_sensitivity()` template).
**See `design.md#component-4` for:** assessment checklist addition.

**Specific file changes:**

#### 1. costingfe Template
**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- [x] Add "### Output Interface (CRITICAL)" section after Structure item 4 — require `result = model.forward(...)` at module level, multi-scenario aliasing convention

#### 2. Freeform Template
**File:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`
- [x] Add "## Output Interface (CRITICAL)" section after "## Sensitivity Analysis" — require module-level `params`/`results`, `to_explorer_dict()` with target schema, `compute_sensitivity()` with central-difference template

#### 3. Assessment Checklist
**File:** `exploration/concept_analysis/prompt_templates/config/assessment_checklist.md`
- [x] Add "## Modeling (Data Model Integrity)" section after "## Risk Identification (Goal 5)" — 3 checklist items per `design.md#component-4`

### Validation

**Manual:**
- [ ] Read each modified template — verify output interface section is present and correctly placed
- [ ] Verify assessment checklist has the new section with 3 items
- [ ] Verify no existing template content was altered

**What We Know Works After This Phase:**
Future pipeline runs will instruct the LLM to produce conforming scripts. The assessor will catch data model quality issues and route findings to the model-setup pass.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Run extraction against real concept dirs after tests pass to validate detection in the wild
- **Phase 2**: Interface check is a pure addition after the success return path — cannot break existing behavior
- **Phase 3**: Template changes are additive sections — no existing content modified

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `extract_explorer_data.py:554-563` — replaced `is_costingfe = (concept_dir / "model_setup.py").exists()` with import-based detection checking for `CostModel` + `from costingfe`/`import costingfe` in source
- `extract_explorer_data.py:244-252` — standalone pathway now prefers `model_setup.py` over alphabetical first `.py` file
- `extract_explorer_data.py:266-278` — standalone pathway now extracts `compute_sensitivity()` if present, building `SensitivityAnalysis` via new `_build_sensitivity_from_dict()` helper
- `extract_explorer_data.py:155-182` — added `_build_sensitivity_from_dict()` helper (parallel to `build_sensitivity_analysis` for costingfe)
- `tests/test_extraction.py` — added `TestRoutingDetection` class with 5 tests (freeform routing, costingfe routing, constants-only routing, model_setup.py preference, compute_sensitivity extraction)
**Issues:** None
**Deviations:** Added a `has_sensitivities` local variable to `extract_standalone()` to track sensitivity state (design implied it but didn't specify the variable)

### Phase 2 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `lib/claude.py` — added `import re`, added `_check_interface(model_path)` function that reads source, detects costingfe vs freeform via import-based detection, prints warnings to stderr
- `lib/claude.py` — call `_check_interface(model_path)` at end of `run_model()` after `output_path.write_text()`
- `test_claude.py` — added `TestCheckInterface` class with 5 tests
**Issues:** None
**Deviations:** Tests call `_check_interface` directly rather than mocking subprocess through `run_model()` — cleaner and more focused. Added an extra test for indented `result =` (not at module level) which the plan didn't specify but is an important edge case.

### Phase 3 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `model_setup_costingfe.md` — added "### Output Interface (CRITICAL)" section (8 lines) after Structure item 4, before Traceability
- `model_setup_freeform.md` — added "## Output Interface (CRITICAL)" section (~60 lines) after Sensitivity Analysis, before Anti-Hallucination, with module-level vars, `to_explorer_dict()` schema, and `compute_sensitivity()` template
- `assessment_checklist.md` — added "## Modeling (Data Model Integrity)" section (3 checklist items) after Risk Identification
**Issues:** None
**Deviations:** None

---

**Status**: Complete
