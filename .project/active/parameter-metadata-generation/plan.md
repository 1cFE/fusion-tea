# Implementation Plan: Parameter Metadata Generation

**Status:** Draft
**Created:** 2026-04-26
**Last Updated:** 2026-04-26

## Source Documents
- **Spec:** `.project/active/parameter-metadata-generation/spec.md`
- **Design:** `.project/active/parameter-metadata-generation/design.md` ← See here for component details, architecture, key bets

## Implementation Strategy

**Phasing Rationale:**
Function first, wiring second. Phase 1 proves the derivation logic works in isolation. Phase 2 connects it to the extraction pipeline and verifies the full loop (extraction → JSON → server → sliders).

**Critical Path:**
`generate_parameter_metadata()` → wire into `extract_costingfe()` → re-extract → sliders render

**First Proof Point:**
Phase 1 test: given the existing mock sensitivity data (`_make_mock_model()` in `test_extraction.py`), the function produces valid `ParameterMetadata` entries with correct ranges and display names.

---

## Phase 1: The Function + Unit Tests

### Goal
Write `generate_parameter_metadata()` and prove it works in isolation against known inputs.

### Assumption Under Test
Can we derive valid `ParameterMetadata` entries from a `SensitivityAnalysis` alone — correct ranges, no Pydantic validation failures, proper fractional clamping?

### Test Stencil (Write This First)
```python
def test_generate_parameter_metadata_basic():
    sens = SensitivityAnalysis(
        engineering={
            "availability": SensitivityEntry(elasticity=0.75, baseline=0.85),
            "R0": SensitivityEntry(elasticity=-0.3, baseline=5.0),
        },
        financial={
            "interest_rate": SensitivityEntry(elasticity=0.85, baseline=0.07),
        },
    )
    meta = generate_parameter_metadata(sens)
    assert set(meta.keys()) == {"availability", "R0", "interest_rate"}
    # Fractional param clamped to [0, 1]
    assert meta["availability"].range[1] <= 1.0
    assert meta["availability"].range[0] >= 0
    # Non-fractional: baseline ± 30%
    assert meta["R0"].range == pytest.approx((3.5, 6.5))
    # All entries are valid ParameterMetadata (Pydantic didn't reject)
    assert meta["R0"].display_name == "R0"
```

### Changes Required

**See `design.md` for:**
- Function signature and field derivation → `design.md#component-overview`
- Range strategy and fractional heuristic → `design.md#component-overview` (Fractional parameter identification)
- Required invariants → `design.md#required-invariants`

**Specific file changes:**

#### 1. Test file
**File:** `exploration/concept_explorer/tests/test_extraction.py`
- [x] Import `generate_parameter_metadata` (add to existing import block, line 20-34)
- [x] Import `ParameterMetadata`, `ParameterCategory`, `Confidence` from models (add to line 35-46)
- [x] Add `test_generate_parameter_metadata_basic` — happy path with engineering + financial params
- [x] Add `test_generate_parameter_metadata_fractional_clamping` — verify efficiency/availability params clamp to [0, 1]
- [x] Add `test_generate_parameter_metadata_zero_baseline` — verify fallback range for zero-baseline edge case
- [x] Add `test_generate_parameter_metadata_empty` — empty sensitivities → empty dict

#### 2. Implementation
**File:** `exploration/concept_explorer/extract_explorer_data.py`
- [x] Add `generate_parameter_metadata(sensitivities: SensitivityAnalysis) -> dict[str, ParameterMetadata]` — place it right after `build_sensitivity_analysis()` (after line 153)
- [x] Fractional detection: inline predicate, not a separate function (see `design.md#implementation-notes`)

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_extraction.py -v -k generate` → new tests pass
- [x] `uv run python -m pytest exploration/concept_explorer/tests/` → no regressions

**What We Know Works After This Phase:**
The derivation function produces valid `ParameterMetadata` for all parameter types — fractional, non-fractional, financial, zero-baseline edge case.

---

## Phase 2: Wire Into Extraction + End-to-End Verification

### Goal
Connect `generate_parameter_metadata()` into `extract_costingfe()`, re-extract all concepts, and verify sliders appear in the browser.

### Assumption Under Test
Does the existing frontend actually render sliders and trigger `POST /api/compute` when given populated `parameter_metadata`?

### Test Stencil (Write This First)
```python
def test_extract_costingfe_generates_metadata(tmp_path):
    """extract_costingfe() produces non-empty parameter_metadata."""
    concept_dir = _make_concept_dir(tmp_path)
    with patch("...load_module_from_path") as mock_load:
        mock_load.return_value = _make_module(model=_make_mock_model(), result=_make_forward_result())
        concept = extract_costingfe(concept_dir, "04", frontmatter, analysis_path, None, {})
    assert len(concept.parameter_metadata) > 0
    assert "availability" in concept.parameter_metadata
```

### Changes Required

**Specific file changes:**

#### 1. Test file
**File:** `exploration/concept_explorer/tests/test_extraction.py`
- [ ] Add `test_extract_costingfe_generates_metadata` — verify extraction produces non-empty metadata
- [ ] Add `test_extract_costingfe_yaml_overrides_win` — verify yaml metadata replaces generated entries

#### 2. Glue code
**File:** `exploration/concept_explorer/extract_explorer_data.py:205-239` (in `extract_costingfe()`)
- [ ] After `sensitivities = build_sensitivity_analysis(...)` (line 205): add `generated_meta = generate_parameter_metadata(sensitivities)`
- [ ] Before `ConceptData(...)` (line 239): merge `merged_meta = {**generated_meta, **param_metadata}`
- [ ] Pass `merged_meta` instead of `param_metadata` to `ConceptData`

#### 3. Re-extract
- [ ] Run `uv run python exploration/concept_explorer/extract_explorer_data.py` to regenerate all concept JSONs
- [ ] Spot-check `exploration/concept_explorer/data/01.json` — `parameter_metadata` should be non-empty

#### 4. Manual browser verification
- [ ] Start server: `uv run python exploration/concept_explorer/server.py`
- [ ] Open a costingfe concept profile page
- [ ] Verify: "Parameter What-If" section visible with sliders
- [ ] Drag a slider → headline economics update (POST /api/compute fires)
- [ ] Verify: tornado chart still renders correctly (no regression)

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` → all pass (including new tests)

**Manual:**
- [ ] Sliders visible on concept profile page
- [ ] Slider drag updates headline card
- [ ] No console errors in browser dev tools

**What We Know Works After This Phase:**
Full pipeline: extraction generates metadata → JSON has it → frontend renders sliders → compute endpoint recomputes on drag. Spec acceptance criteria met.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Zero-baseline edge case tested explicitly. Pydantic validation covered by all tests constructing `ParameterMetadata`.
- **Phase 2**: If frontend doesn't render despite populated metadata, check browser console — the gating conditions are in `concept_page.js:458-510`.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-04-26

**Actual Changes:**
- Added `generate_parameter_metadata()` to `exploration/concept_explorer/extract_explorer_data.py:156-209` with module-level constants `_FRACTIONAL_NAME_TOKENS` and `_FRACTIONAL_NAME_EXACT`.
- Added `TestGenerateParameterMetadata` class to `exploration/concept_explorer/tests/test_extraction.py:823-908` with 5 tests (basic, fractional clamping, zero baseline, empty, sub-unit non-fractional). All pass.
- Added `Confidence`, `ParameterCategory`, `ParameterMetadata` imports to test file.

**Issues:**
- None. All 49 extraction tests pass; the 39 errors in `test_views_manual.py` are pre-existing missing-`page`-fixture errors from `pytest-playwright` not being installed — unrelated to this work.

**Deviations:**
- Added a 5th test (`test_non_fractional_with_subunit_baseline`) to lock in that `interest_rate`-style params with sub-unit baselines do not get the [0, 1] clamp. Plan called for 4 tests; this catches a heuristic regression risk specifically called out in design.md (Risk 2).
- Inlined the fractional predicate inside the function but kept the token list and exact-name set as module-level constants — keeps the predicate one expression while making the patterns greppable.

### Phase 2 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
