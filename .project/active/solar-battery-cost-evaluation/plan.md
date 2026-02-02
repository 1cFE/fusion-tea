# Implementation Plan: Solar+Battery Cost Evaluation & Entry Point Generation

**Status:** Complete
**Created:** 2026-02-02
**Last Updated:** 2026-02-02

## Source Documents
- **Spec:** `.project/active/solar-battery-cost-evaluation/spec.md`
- **Design:** `.project/active/solar-battery-cost-evaluation/design.md` — See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks by proving the coffee maker engine works on the solar battery model — if AST traversal or binding resolution fails, we find out immediately before writing any new code. Phase 2 adds JSON generation (new code, but depends on Phase 1 producing correct cost data). Phase 3 adds LCOE verification (pure Python math, lowest risk, depends on Phase 2's extracted params).

**Overall Validation Approach:**
- Each phase starts with tests
- Each phase has `uv run python -m pytest` validation
- Coffee maker regression check after Phase 1

---

## Phase 1: Copy + Adapt Core Script — Prove CSV Match

### Goal
Get `generate_costs.py` producing correct `actual_output.csv` for the solar battery model. This is the highest-risk phase — it validates the entire evaluation engine (extract, resolve, evaluate, aggregate) works on a model with 9 leaves, 3 assemblies, multiplicity up to [20], and the Permitting soft cost edge case.

### Test Stencil (Write This First)
```python
# test_generate_costs.py — tests 1-7, adapted from coffee maker
MODEL_DIR = Path(__file__).parent

def test_compute_costs_returns_dict():
    from generate_costs import compute_costs
    result = compute_costs(str(MODEL_DIR))
    assert isinstance(result, dict)
    assert "solar_battery_plant" in result

def test_compute_costs_has_all_expected_paths():
    from generate_costs import compute_costs
    result = compute_costs(str(MODEL_DIR))
    assert set(result.keys()) == {
        "solar_battery_plant",
        "solar_battery_plant.solar_array",
        # ... 13 paths total (see design.md#expected-paths)
    }

def test_compute_costs_root_values_match_expected():
    from generate_costs import compute_costs
    result = compute_costs(str(MODEL_DIR))
    root = result["solar_battery_plant"]
    assert abs(root["capital_cost"] - 41205.00) < 0.02
```

### Changes Required

**See `design.md#file-1` for:** Architecture, ROOT_PART_NAME constant, all unchanged sections.

**Specific file changes:**

#### 1. Test File
**File:** `models/tests/solar_battery/test_generate_costs.py` (NEW — write first)
- [x] Create test file with imports and MODEL_DIR
- [x] Implement tests 1-7 (adapted from `models/tests/coffee_maker/test_generate_costs.py`)
- [x] Key adaptations: 13 paths (not 10), root CAPEX $41,205.00 (not $113.96), PV Module spot-check $14,980.00

#### 2. Implementation File
**File:** `models/tests/solar_battery/generate_costs.py` (NEW)
- [x] Copy `models/tests/coffee_maker/generate_costs.py` verbatim
- [x] Add `ROOT_PART_NAME = "solar_battery_plant"` module constant (~line 30)
- [x] Replace hardcoded `"coffee_maker"` in `extract_design_hierarchy()` with `ROOT_PART_NAME` (2 occurrences: the constant and the path arg)
- [x] Replace hardcoded `"coffee_maker"` in `compute_costs()` docstring
- [x] Update module docstring (solar battery, not coffee maker)

### Validation (How to Verify This Phase)

**Automated:**
- [x] `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` — tests 1-7 pass
- [x] `uv run python models/tests/solar_battery/generate_costs.py` — exits 0, prints PASS
- [x] `uv run python -m pytest models/tests/coffee_maker/test_generate_costs.py -v` — no regressions

**Manual:**
- [x] Inspect `models/tests/solar_battery/actual_output.csv` — 14 data rows, header matches expected
- [x] Spot-check: `solar_battery_plant` total_cost = 41205.00
- [x] Spot-check: `solar_battery_plant.site_infra.permitting` material_cost = 0.00, idiot_index = 0.00

**What We Know Works After This Phase:**
The coffee maker evaluation engine correctly evaluates the solar battery model: 9 leaf costs, 3 assembly rollups, 1 allocation, multiplicity handling, Permitting soft cost edge case, and CSV output matching expected values.

---

## Phase 2: JSON Entry Points + Design Param Extraction

### Goal
Add `extract_design_params()`, `write_component_costs_json()`, and `write_design_params_json()` to produce the two JSON entry points TEAx will consume in Items 4-5.

### Test Stencil (Write This First)
```python
def test_write_component_costs_json(tmp_path):
    from generate_costs import compute_costs, write_component_costs_json, CostResult
    # Use internal API to get CostResult list (need to call pipeline directly)
    # ... load model, compute results ...
    output_path = tmp_path / "component_costs.json"
    write_component_costs_json(results, output_path)
    data = json.loads(output_path.read_text())
    assert abs(data["total_capex"] - 41205.00) < 0.02
    assert "solar_array" in data
    assert abs(data["solar_array"]["total_cost"] - 21204.00) < 0.02

def test_write_design_params_json(tmp_path):
    # ... load model, find root_usage, compute total_capex ...
    from generate_costs import extract_design_params, write_design_params_json
    params = extract_design_params(root_usage, total_capex=41205.00)
    output_path = tmp_path / "design_params.json"
    write_design_params_json(params, output_path)
    data = json.loads(output_path.read_text())
    assert len(data) == 11
    assert data["p_net_mw"] == 0.008
    assert data["p_net_kw"] == 8.0
    assert data["total_capex"] == 41205.00
```

### Changes Required

**See `design.md#change-2` through `design.md#change-4` for:** Function signatures, logic, JSON structure.

**Specific file changes:**

#### 1. Test File
**File:** `models/tests/solar_battery/test_generate_costs.py` (MODIFY)
- [x] Add `import json`
- [x] Add test 8: `test_write_component_costs_json` — uses `tmp_path`, verifies JSON structure and values from assembly-level CostResults
- [x] Add test 9: `test_write_design_params_json` — loads model via SysideAdapter, extracts params, verifies 11 keys with correct values

#### 2. Implementation File
**File:** `models/tests/solar_battery/generate_costs.py` (MODIFY)
- [x] Add `import json` to imports
- [x] Add `extract_design_params()` after the design extractor section (~line 510). See `design.md#change-2` for logic.
- [x] Add `write_component_costs_json()` after output generator section. See `design.md#change-3` for logic.
- [x] Add `write_design_params_json()` after `write_component_costs_json()`. See `design.md#change-4`.
- [x] Update `main()`: add root_usage lookup (~3 lines scanning PartUsages for `ROOT_PART_NAME`)
- [x] Update `main()`: add Phase 6 (extract params), Phase 7 (write component JSON), Phase 8 (write design params JSON)

### Validation (How to Verify This Phase)

**Automated:**
- [x] `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` — tests 1-9 pass
- [x] `uv run python models/tests/solar_battery/generate_costs.py` — generates both JSON files

**Manual:**
- [x] Inspect `component_costs.json`: `total_capex` = 41205.00, three subsystem entries
- [x] Inspect `design_params.json`: 11 keys, `p_net_kw` = 8.0 (derived), `total_capex` = 41205.00
- [x] Verify `design_params.json` values match `design.sysml` lines 53-62

**What We Know Works After This Phase:**
Design parameter extraction from SysML AST (including derived `p_net_kw`), component cost JSON generation from CostResult rows, and both entry point files ready for TEAx consumption.

---

## Phase 3: System-Level LCOE Verification

### Goal
Add `verify_system_outputs()` that computes all 6 system-level outputs from design params in pure Python and compares against `expected_system_outputs.csv`. This validates entry point data correctness before Items 4-5 consume it.

### Test Stencil (Write This First)
```python
def test_verify_system_outputs_passes():
    from generate_costs import extract_design_params, verify_system_outputs
    # ... load model, extract params with total_capex=41205.00 ...
    expected_path = MODEL_DIR / "expected_system_outputs.csv"
    passed, diffs = verify_system_outputs(params, expected_path)
    assert passed, f"System output verification failed: {diffs}"
```

### Changes Required

**See `design.md#change-5` for:** Function signature, formulas, comparison logic.

**Specific file changes:**

#### 1. Test File
**File:** `models/tests/solar_battery/test_generate_costs.py` (MODIFY)
- [x] Add test 10: `test_verify_system_outputs_passes` — extracts params, calls verify, asserts pass

#### 2. Implementation File
**File:** `models/tests/solar_battery/generate_costs.py` (MODIFY)
- [x] Add `verify_system_outputs()` function. Formulas from `design.md#change-5`:
  - `annual_energy_mwh = 8760 * p_net_mw * n_mod * plant_availability`
  - `annual_om_cost = om_rate_per_kw_year * p_net_kw`
  - `annual_fuel_cost = fuel_unit_cost * fuel_consumption`
  - `crf = r * (1+r)^n / ((1+r)^n - 1)`
  - `annualized_capital_cost = crf * total_capex`
  - `lcoe_per_mwh = (annualized_capital_cost + (annual_om_cost + annual_fuel_cost) * (1 + yearly_inflation)^plant_lifetime) / annual_energy_mwh`
- [x] Read `expected_system_outputs.csv`, compare each row's `output_value` within 1% relative tolerance
- [x] Return `(passed, diffs)` tuple
- [x] Update `main()`: add Phase 9 (verify system outputs), print PASS/FAIL

### Validation (How to Verify This Phase)

**Automated:**
- [x] `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` — all 10 tests pass
- [x] `uv run python models/tests/solar_battery/generate_costs.py` — prints system verification PASS + CSV comparison PASS

**Manual:**
- [x] Verify LCOE output: $288.68/MWh (within 1% of expected)
- [x] Verify CRF: 0.070952

**What We Know Works After This Phase:**
Complete pipeline: SysML model -> component cost evaluation -> CSV validation -> JSON entry points -> system-level LCOE verification. All acceptance criteria from the spec are met. Items 4-5 can consume the JSON files with confidence.

---

## Environment Setup

**See CLAUDE.md:** All Python commands via `uv run`. Test command: `uv run python -m pytest`.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: If CSV comparison fails, diff output identifies exactly which part/field diverges — debug from there. The `--verbose` flag traces binding resolution step by step.
- **Phase 2**: If `extract_design_params()` misses attributes, the 11-key validation raises `ValueError` immediately with the missing key name.
- **Phase 3**: If LCOE doesn't match, `verify_system_outputs()` reports per-output diffs — identifies which intermediate calc diverges.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-02-02
**Actual Changes:**
- Created `models/tests/solar_battery/test_generate_costs.py` (7 tests adapted from coffee maker)
- Created `models/tests/solar_battery/generate_costs.py` (copied from coffee maker with targeted edits)
- Edits: module-level `ROOT_PART_NAME = "solar_battery_plant"`, removed local `ROOT_PART_NAME` in `extract_design_hierarchy()`, updated `path=` arg to use constant, updated docstrings and comments
- Generated `models/tests/solar_battery/actual_output.csv` — 14 data rows, all match expected
**Issues:** None. Multiplicity warnings (cached_lower_bound != cached_upper_bound) are expected — same behavior as coffee maker.
**Deviations:** Also updated `main()` argparse description and `PartInstance.path` comment (minor, not in plan but consistent with intent).

### Phase 2 Completion
**Completed:** 2026-02-02
**Actual Changes:**
- Added `import json` to `generate_costs.py`
- Added `extract_design_params()` function (~45 lines) — extracts 9 literal params from AST, computes `p_net_kw` derived, adds `total_capex`, validates 11 keys
- Added `write_component_costs_json()` function (~35 lines) — builds dict from root + 3 subsystem CostResults
- Added `write_design_params_json()` function (~5 lines) — simple json.dump wrapper
- Updated `main()` with phases 6-8: root_usage lookup, param extraction, JSON generation
- Added tests 8-9 to `test_generate_costs.py` with `tmp_path` fixtures
**Issues:** Minor floating-point representation in `component_costs.json` (`2743.7999999999997` for battery_system.install_cost) — this is a JSON serialization artifact and within tolerance. Does not affect downstream consumption.
**Deviations:** None.

### Phase 3 Completion
**Completed:** 2026-02-02
**Actual Changes:**
- Added `verify_system_outputs()` function (~70 lines) — computes all 6 system-level outputs in pure Python, reads expected CSV, compares with 1% relative tolerance
- Added Phase 9 to `main()` — verify system outputs before CSV comparison (renumbered CSV comparison to Phase 10)
- Added test 10: `test_verify_system_outputs_passes`
**Issues:** None. All 6 system-level outputs match within tolerance.
**Deviations:** None.

---

**Status**: Complete
