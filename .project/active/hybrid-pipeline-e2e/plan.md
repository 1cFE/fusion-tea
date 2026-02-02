# Implementation Plan: Hybrid Pipeline End-to-End (Solar+Battery)

**Status:** Complete
**Created:** 2026-02-02T06:45:00Z
**Last Updated:** 2026-02-02T06:45:00Z

## Source Documents
- **Spec:** `.project/active/hybrid-pipeline-e2e/spec.md`
- **Design:** `.project/active/hybrid-pipeline-e2e/design.md` ← See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
De-risk from the outside in. Phase 1 runs codegen to eliminate the biggest unknowns (namespace, multi-output support, directory structure). Phase 2 builds and tests the only hand-written module in isolation. Phase 3 fills in trivial formulas. Phase 4 wires everything together. Phase 5 verifies outputs. Each phase produces a testable artifact before moving on.

**Overall Validation Approach:**
- Each phase has concrete pass/fail criteria
- Phases 1-3 validate components in isolation
- Phase 4 is the integration gate
- Phase 5 is acceptance testing against known-good values

---

## Phase 1: Run Codegen + Resolve Unknowns

### Goal
Run `sysml-codegen generate` on the solar+battery model. Discover the actual namespace, directory structure, and whether multi-output is supported for AnnualizedFinancialCalc. Resolves design Risks 1, 2, and 5 before any code is written.

### Test Stencil (Write This First)
```python
# No test file yet — this phase is exploratory.
# Validation is manual inspection of codegen output.
# The codegen-generated test file (tests/test_implementations_runnable.py)
# will be used in Phase 3.
```

### Changes Required

**See `design.md#component-1` for codegen command and expected output structure.**

#### 1. Run codegen
- [x] Run initial codegen command with `--overwrite` (see `design.md#component-1` for exact command)
- [x] Record actual namespace produced (e.g., `solarbatterylibrary` vs `solarbatterydesign`)

#### 2. Inspect output and resolve unknowns
- [x] Verify directory structure matches `design.md#component-1` expected output
- [x] Check package name vs directory name alignment — create symlink if needed (`design.md#dd-3`)
- [x] Inspect `modules/<ns>/annualizedfinancialcalc.py` — does it use `MultiOutput` for 2 outputs? Record which of the 3 outcomes from `design.md#risk-5` applies
- [x] Inspect `__init__.py` — note registry function name and module imports
- [x] Inspect `pipelines/pipeline.yaml` — note how codegen wired `total_capex` (should be an entry point param since codegen can't see component costs)
- [x] Inspect `inputs/design_params.json` — note what parameters codegen extracted

#### 3. Document findings
- [x] Record actual namespace in Implementation Notes below
- [x] Record AnnualizedFinancialCalc multi-output status
- [x] Record any codegen warnings (expected: warnings about nested CalcUsages it can't see)

### Validation

**Automated:**
- [x] `sysml-codegen generate` exits 0

**Manual:**
- [x] `generated/solar_battery/` directory exists with expected structure
- [x] 15 module files exist in `modules/solarbatterylibrary/` (5 system-level + 10 component-level)
- [x] 15 handwritten stencil files exist in `handwritten/solarbatterylibrary/`
- [x] `primitives.py`, `__init__.py`, `pipelines/pipeline.yaml` all exist
- [x] Python imports work: `PYTHONPATH=generated uv run python -c "from solar_battery import *"` (may fail on missing impls — that's OK, just verify the import path resolves)

**What We Know Works After This Phase:**
Codegen runs on solar+battery model. We know the exact namespace, file layout, and whether multi-output needs manual intervention.

---

## Phase 2: ComponentCostEvaluator Module + Unit Test

### Goal
Build the hand-written `ComponentCostEvaluator` module and test it in isolation. This is the riskiest custom code: importlib dynamic import, JSON file reading, BaseModel output construction. Proving it works before pipeline integration eliminates Risk 7 and partially validates DD-5.

### Test Stencil (Write This First)
```python
# generated/solar_battery/tests/test_cost_evaluator.py
import pytest
from pathlib import Path

from solar_battery.modules.component_cost_evaluator import (
    ComponentCostEvaluator,
    CostEvaluatorResult,
    CostEvaluatorInput,
)


class TestComponentCostEvaluator:
    """Test cost evaluator module in isolation (no pipeline)."""

    MODEL_PATH = str(Path(__file__).resolve().parents[3] / "models" / "tests" / "solar_battery")

    def test_run_produces_result(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert isinstance(result.data, CostEvaluatorResult)

    def test_total_capex_matches_expected(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert result.data.total_capex == pytest.approx(41205.0, abs=0.01)

    def test_design_params_present(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert result.data.p_net_mw == pytest.approx(0.008)
        assert result.data.plant_lifetime == pytest.approx(25.0)
        assert result.data.discount_rate == pytest.approx(0.05)

    def test_validate_and_fill_default(self):
        module = ComponentCostEvaluator()
        validated = module.validate_and_fill_default(model_path="/some/path")
        assert isinstance(validated, CostEvaluatorInput)
        assert validated.model_path == "/some/path"
```

### Changes Required

**See `design.md#component-3` for full module code, `design.md#component-5` for config schema.**

#### 1. Test file (write first)
**File:** `generated/solar_battery/tests/test_cost_evaluator.py` (NEW)
- [x] Create test file with stencil above
- [x] Verify tests fail before implementation (test-first)

#### 2. Pipeline config schema
**File:** `generated/solar_battery/schemas/pipeline_config.py` (NEW)
- [x] Create `PipelineConfig` schema per `design.md#component-5`

#### 3. Cost evaluator module
**File:** `generated/solar_battery/modules/component_cost_evaluator.py` (NEW)
- [x] Create `CostEvaluatorInput`, `CostEvaluatorResult`, `ComponentCostEvaluator` per `design.md#component-3`
- [x] Use `importlib.util.spec_from_file_location()` for dynamic import
- [x] Read `design_params.json`, override `total_capex` with computed value

#### 4. Run tests
- [x] Run unit tests → all 4 pass

### Validation

**Automated:**
- [x] `PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/test_cost_evaluator.py -v` → 4 pass

**Manual:**
- [ ] Instantiate module in REPL: `ComponentCostEvaluator().run(model_path="models/tests/solar_battery")` → returns `ModuleResult` with correct `total_capex`

**What We Know Works After This Phase:**
The cost evaluator module correctly wraps `compute_costs()`, reads `design_params.json`, and produces a `CostEvaluatorResult` with all 11 fields. importlib dynamic import works.

---

## Phase 3: Fill Handwritten Implementations + Codegen Tests

### Goal
Fill in the 5 handwritten calc implementations with correct formulas. Adapt AnnualizedFinancialCalc module wrapper if codegen didn't generate multi-output correctly. Verify codegen-generated tests pass.

### Test Stencil (Write This First)
```python
# Codegen already generated tests/test_implementations_runnable.py.
# Additionally, add formula verification tests:

# generated/solar_battery/tests/test_formulas.py
import pytest

# Import paths depend on actual namespace discovered in Phase 1
# from solar_battery.handwritten.<ns>.energyproductioncalc_impl import run_energyproductioncalc

def test_energy_production_formula():
    """8760 * 0.008 * 1.0 * 0.159 = 11.14272"""
    # Use a mock input with the known design params
    result = run_energyproductioncalc(mock_input)
    assert result == pytest.approx(11.14272, rel=0.001)

def test_lcoe_formula():
    """(2923.60 + (160 + 0) * 1.8315) / 11.14272 = 288.68"""
    result = run_lcoecalc(mock_input)
    assert result == pytest.approx(288.68, rel=0.01)
```

### Changes Required

**See `design.md#component-2` for all 5 formulas.**

#### 1. Formula verification tests (write first)
**File:** `generated/solar_battery/tests/test_formulas.py` (NEW)
- [x] Create test file with formula verification for all 5 calcs
- [x] Import from actual namespace (discovered in Phase 1)
- [x] Use mock inputs matching `design_params.json` values
- [x] Expected values from `expected_system_outputs.csv`

#### 2. Fill handwritten implementations
**Files:** 5 files in `generated/solar_battery/handwritten/<ns>/` (EDIT — fill stencils)
- [x] `energyproductioncalc_impl.py` — `8760 * p_net_mw * n_mod * plant_availability`
- [x] `annualizedomcalc_impl.py` — `om_rate_per_kw_year * p_net_kw`
- [x] `annualizedfuelcalc_impl.py` — `fuel_unit_cost * fuel_consumption`
- [x] `annualizedfinancialcalc_impl.py` — CRF formula + `crf * total_capex` (returns tuple)
- [x] `lcoecalc_impl.py` — LCOE with inflation escalation

#### 3. AnnualizedFinancialCalc multi-output (conditional)
**File:** `generated/solar_battery/modules/<ns>/annualizedfinancialcalc.py` (EDIT or REWRITE)
- [x] Phase 1 found codegen generated multi-output correctly → no changes needed
- N/A — codegen handled it correctly
- N/A — codegen handled it correctly

#### 4. Run tests
- [x] Run codegen-generated tests — 15/15 pass
- [x] Run formula verification tests — 5/5 pass
- [x] Run existing `generate_costs.py` tests (no regressions) — 10/10 pass

### Validation

**Automated:**
- [x] `PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/test_implementations_runnable.py -v` → 15 pass
- [x] `PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/test_formulas.py -v` → 5 pass
- [x] `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` → 10 pass (no regressions)

**What We Know Works After This Phase:**
All 5 system-level calc implementations are correct and match expected values. AnnualizedFinancialCalc multi-output is handled. No regressions in existing tests.

---

## Phase 4: Pipeline YAML + Registry + Integration

### Goal
Wire everything together: hand-craft the pipeline YAML, update the registry, create execution script and entry point config. Execute the pipeline end-to-end.

### Test Stencil (Write This First)
```python
# generated/solar_battery/tests/test_pipeline_integration.py
import pytest
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery import create_solar_battery_registry, CUSTOM_SCHEMA_TYPES


class TestPipelineIntegration:
    """Integration test: full pipeline execution."""

    def test_pipeline_executes_without_error(self):
        pipeline_dir = Path(__file__).resolve().parents[1]
        result = execute_pipeline(
            spec_path=str(pipeline_dir / "pipelines" / "pipeline.yaml"),
            output_dir=str(pipeline_dir / "outputs"),
            registry=create_solar_battery_registry(),
            custom_schema_types=CUSTOM_SCHEMA_TYPES,
        )
        assert result is not None
        assert "lcoe_per_mwh" in result.outputs

    def test_lcoe_within_tolerance(self):
        # ... same setup ...
        lcoe = getattr(result.outputs["lcoe_per_mwh"], "root", result.outputs["lcoe_per_mwh"])
        assert lcoe == pytest.approx(288.68, rel=0.01)
```

### Changes Required

**See `design.md#component-4` for YAML, `design.md#component-6` for registry, `design.md#component-7` for execution script.**

#### 1. Integration test (write first)
**File:** `generated/solar_battery/tests/test_pipeline_integration.py` (NEW)
- [x] Create integration test with stencil above
- [x] Test pipeline executes without error
- [x] Test LCOE output is within tolerance

#### 2. Pipeline config JSON
**File:** `generated/solar_battery/inputs/pipeline_config.json` (NEW)
- [x] Create with `model_path` per `design.md#component-5`

#### 3. Pipeline YAML (hand-crafted, replaces codegen version)
**File:** `generated/solar_battery/pipelines/pipeline.yaml` (REWRITE)
- [x] Write pipeline YAML per `design.md#component-4`
- [x] Replace `<ns>` placeholders with actual namespace from Phase 1
- [x] Use `RootModel[float]` (not `Float`) for type names
- [x] Handle exit point `total_capex` channel wiring (see `design.md#component-4` notes)

#### 4. Registry update
**File:** `generated/solar_battery/__init__.py` (EDIT — add cost evaluator)
- [x] Add `ComponentCostEvaluator` import and registration per `design.md#component-6`
- [x] Add `CostEvaluatorResult` and `PipelineConfig` to `CUSTOM_SCHEMA_TYPES`
- [x] Verify `module_type_override` includes `ComponentCostEvaluator`

#### 5. Execution script
**File:** `generated/solar_battery/run_pipeline.py` (NEW)
- [x] Create per `design.md#component-7`
- [x] Resolve model path to absolute
- [x] Print results on completion

#### 6. Run integration test
- [x] Run integration test → pipeline executes, LCOE correct

### Validation

**Automated:**
- [x] `uv run python -m pytest generated/solar_battery/tests/test_pipeline_integration.py -v` → 4 pass
- [ ] `uv run python generated/solar_battery/run_pipeline.py` → prints LCOE ≈ $288.68/MWh

**Manual:**
- [ ] Inspect `generated/solar_battery/outputs/solar_battery_results/` → JSON files exist for all 7 metrics
- [ ] Spot-check `lcoe_per_mwh.json` → value ≈ 288.68

**If CostEvaluatorResult field access fails (Risk 6):**
- [x] Fall back to MultiOutput pattern per `design.md#dd-6`
- [x] Update YAML to use `component_costs__<field>.root` pattern
- [x] Re-run integration test

**What We Know Works After This Phase:**
The complete pipeline executes end-to-end. `execute_pipeline()` produces LCOE from the solar+battery SysML model. Component costs are computed dynamically. This is the core success criterion from the spec.

---

## Phase 5: Verification Script + Reproducibility

### Goal
Create the verification script. Confirm all 7 metrics match expected values within tolerance. Ensure the pipeline is reproducible from a single command.

### Test Stencil (Write This First)
```python
# The verification script IS the test for this phase.
# We verify that verify_pipeline.py itself returns exit code 0.
# No separate test file needed — the script is self-testing.
```

### Changes Required

**See `design.md#component-8` for verification script.**

#### 1. Verification script
**File:** `generated/solar_battery/verify_pipeline.py` (NEW)
- [x] Create per `design.md#component-8`
- [x] Verify all 7 metrics from `spec.md#verification-values`
- [x] Handle both `RootModel[float]` serialization formats (`{"root": value}` and bare `value`)

#### 2. Reproducibility test
- [x] Run pipeline from clean state (delete `outputs/` dir first)
- [x] Run verification script → PASS

#### 3. Document any deviations
- [x] Update Implementation Notes with any changes from the design
- [x] Note any codegen warnings that should be documented

### Validation

**Automated:**
- [x] `uv run python generated/solar_battery/run_pipeline.py` → completes
- [x] `uv run python generated/solar_battery/verify_pipeline.py` → exit code 0, all PASS
- [x] All existing tests still pass: `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` → 10 pass

**Manual:**
- [x] Delete `generated/solar_battery/outputs/` and re-run pipeline + verify → still PASS (reproducibility)
- [x] Verify `total_capex` = $41,205.00 (exact)
- [x] Verify `lcoe_per_mwh` ≈ $288.68/MWh (±1%)

**What We Know Works After This Phase:**
All acceptance criteria from `spec.md` are met. Pipeline is reproducible. Verification script confirms correctness. Epic Item 5 (revised) is complete.

---

## Environment Setup

**See CLAUDE.md for full environment rules. Key points:**
- All Python via `uv run`
- Codegen via `uv run sysml-codegen generate`
- Tests via `uv run python -m pytest`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Risks 1, 2, 5 resolved by inspection. If codegen fails entirely, stop and diagnose before proceeding.
- **Phase 2**: Risk 7 resolved by unit testing importlib approach. If it fails, fall back to `sys.path` manipulation.
- **Phase 3**: Risk 5 mitigation applied — hand-write AnnualizedFinancialCalc if codegen doesn't handle multi-output.
- **Phase 4**: Risk 6 is the main concern. If validator rejects field access, fall back to MultiOutput pattern. Have the fallback YAML ready.

---

## Implementation Notes

*[TO BE FILLED DURING IMPLEMENTATION]*

### Phase 1 Completion
**Completed:** 2026-02-02
**Actual namespace:** `solarbatterylibrary`
**Multi-output status (AnnualizedFinancialCalc):** Codegen generated MultiOutput correctly — `AnnualizedFinancialCalcOutput(MultiOutput)` with `capital_recovery_factor` and `annualized_capital_cost` fields. Module wrapper unpacks tuple from impl. **Risk 5 outcome: #1 (codegen handles it correctly).**
**Symlink needed:** Yes — `costing.sysml` symlinked from `models/library/foundation/costing.sysml` into `models/tests/solar_battery/` to resolve `Costing::*` import. No package name symlink needed (directory name matches package name).
**Codegen warnings:** None (clean run after symlink fix).
**15 modules generated** (not 5): Codegen discovered all CalcUsages including 10 component-level cost calcs. Only the 5 system-level modules are needed for the hybrid pipeline; the component-level ones are handled by `compute_costs()`.
**Issues:**
- `library_params.py` had `&` in field names (`Racking_&_Mounting`, `Permitting_&_Interconnect`) causing SyntaxError. Fixed by replacing `&` with `and`. This schema is not used in the hybrid pipeline.
- `design_params.json` uses fully-qualified names (e.g., `SolarBatteryDesign__solar_battery_plant__energy_production__p_net_mw`) — different from the simple names in `models/tests/solar_battery/design_params.json`. Our pipeline uses the ComponentCostEvaluator to read the model's `design_params.json`, not codegen's version.
- `total_capex` not in codegen's `design_params.json` (as expected — codegen can't compute it). The `annualized_financial` module gets it from `design_params` entry point which has no value for it. Our pipeline replaces this with ComponentCostEvaluator output.
- Pipeline YAML uses `float` (not `RootModel[float]`) for multi-output module output types — the `annualized_financial` outputs use plain `float`. This differs from the design's assumption.
**Deviations:** None significant. Plan's assumption of 5 modules was correct for system-level calcs. The 10 extra component-level modules are irrelevant to our hybrid pipeline.

### Phase 2 Completion
**Completed:** 2026-02-02
**Changes Made:**
- Created `generated/solar_battery/tests/test_cost_evaluator.py` — 4 unit tests
- Created `generated/solar_battery/schemas/pipeline_config.py` — PipelineConfig schema
- Created `generated/solar_battery/modules/component_cost_evaluator.py` — CostEvaluatorInput, CostEvaluatorResult, ComponentCostEvaluator
**Issues:**
- `importlib.util.spec_from_file_location()` + `exec_module()` failed because `generate_costs.py` uses `@dataclass` with string annotations (PEP 563). Python's `dataclasses` module tries to resolve annotations via `sys.modules[cls.__module__]`, which returns `None` when the module isn't registered. **Fix:** Added `sys.modules["generate_costs"] = module` before `exec_module()`. This is a known importlib gotcha.
**Deviations:**
- Added `sys.modules` registration — not in the design but necessary for correctness. No impact on the broader design.

### Phase 3 Completion
**Completed:** 2026-02-02
**Changes Made:**
- Filled 5 handwritten implementations in `handwritten/solarbatterylibrary/`
- Created `tests/test_formulas.py` — 5 formula verification tests with known values
**AnnualizedFinancialCalc handling:** Codegen generated MultiOutput correctly (Risk 5 outcome #1). No changes needed to module wrapper. Impl returns tuple `(crf, annualized_capital_cost)` as codegen expects.
**Issues:** None.
**Deviations:** None. All formulas match design.md exactly.

### Phase 4 Completion
**Completed:** 2026-02-02
**Field access or MultiOutput fallback:** DD-6 Option A (MultiOutput) required. Validator rejected BaseModel single-output approach because registry introspected 11 fields as 11 expected outputs, but YAML declared only `root`. Changed `CostEvaluatorResult` from `BaseModel` to `MultiOutput` with `Float` fields. Each field becomes a `component_costs__<field>` channel.
**Exit point total_capex resolution:** ExitPoint uses field key (left side) as channel name, right side as filename. So `component_costs__total_capex: RootModel[float] total_capex.json` maps channel `component_costs__total_capex` to file `total_capex.json`.
**AnnualizedFinancialCalcOutput change:** Changed fields from `float` to `Float` (RootModel[float]) so exit point can serialize them via `.model_dump()`. Updated module wrapper to wrap values in `Float()`.
**Issues:**
- Pipeline validator rejected initial BaseModel approach (Risk 6 materialized). MultiOutput fallback worked.
- Exit point format: field key IS the channel name, not an alias. Required `component_costs__total_capex` as key, not `total_capex`.
- `AnnualizedFinancialCalcOutput` had `float` fields which caused exit point `write_json_model()` to fail (plain floats lack `.model_dump()`). Changed to `Float` (RootModel[float]).
**Deviations:**
- CostEvaluatorResult uses MultiOutput (DD-6 Option A) instead of BaseModel (DD-6 Option B). All 11 fields exposed as individual channels.
- AnnualizedFinancialCalcOutput fields changed from `float` to `Float` — codegen's original output didn't work with exit point serialization.
- Test accesses total_capex via `result.outputs["component_costs__total_capex"]` (channel name includes prefix).

### Phase 5 Completion
**Completed:** 2026-02-02
**All metrics PASS:** Yes — all 7 metrics within tolerance. total_capex=41205.0 (exact), lcoe_per_mwh=288.68 (within 1%).
**Reproducibility confirmed:** Yes — deleted outputs/, re-ran pipeline + verify → all PASS.
**Issues:** None.
**Deviations:**
- Verification script adapted for hash-suffixed output directories (e.g., `solar-battery-results-de4ef3c2`). Uses `find_latest_output_dir()` to locate most recent run.
- Output files contain bare floats, not `{"root": value}`. Script handles both formats defensively.

---

**Status**: ~~Draft~~ → ~~In Progress~~ → **Complete**
