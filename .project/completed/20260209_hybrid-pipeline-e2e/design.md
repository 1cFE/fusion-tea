# Design: Hybrid Pipeline End-to-End (Solar+Battery)

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-02T06:10:49Z
**Updated:** 2026-02-02T06:35:00Z
**Complexity:** MEDIUM
**Branch:** visualization
**Commit:** 0c65513

---

## Overview

Wire `generate_costs.py`'s `compute_costs()` into a TEAx pipeline alongside codegen-generated system-level modules, producing a verified LCOE from a single `execute_pipeline()` call.

## Related Artifacts

- **Spec:** `.project/active/hybrid-pipeline-e2e/spec.md`
- **Research:** `.project/research/20260202-055244_hybrid-vs-native-codegen-feasibility.md`
- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md`
- **Chain spike reference:** `generated/codegen_chain_spike/`
- **SysML model:** `models/tests/solar_battery/library.sysml`, `design.sysml`
- **Reference implementation:** `models/tests/solar_battery/generate_costs.py`
- **Expected values:** `models/tests/solar_battery/expected_system_outputs.csv`

---

## Research Findings

### Existing Patterns (from chain spike)

The chain spike at `generated/codegen_chain_spike/` demonstrates the complete codegen → TEAx pattern:

- **Module structure:** `ModuleBase[InputModel, OutputModel]` subclass in `modules/<namespace>/<calc>.py` delegates to `handwritten/<namespace>/<calc>_impl.py`
- **Pipeline YAML:** EntryPoint loads JSON → modules consume inputs from entry or upstream → ExitPoint writes JSON outputs
- **Registry:** `__init__.py` exports `create_<pkg>_registry()` and `CUSTOM_SCHEMA_TYPES`
- **Inter-module wiring:** `channel_name.root` for `RootModel[T]` outputs, `channel_name.field` for multi-output models
- **Single outputs:** Use `RootModel[float]` (aliased as `Float` in `primitives.py`)
- **Multi-outputs:** Use `MultiOutput` subclass (from `simkit.config.schema`)
- **Package symlink:** `generated/chain_spike -> codegen_chain_spike` — required because `--package-name chain_spike` produces imports from `chain_spike.*` but the output directory is `codegen_chain_spike`

### TEAx Framework Key Facts

- `execute_pipeline()` at `simkit/core/pipeline.py:71-212` — takes `spec_path`, `output_dir`, `registry`, `custom_schema_types`
- `ModuleBase` at `simkit/core/base.py:19-29` — requires `validate_and_fill_default()` and `run()` methods
- `ModuleResult[T]` wraps output with `data: T` and optional `notes: str`
- Entry points are **static JSON only** — cannot run Python code
- Modules can run **arbitrary Python** via `run()` — this is the integration point for `compute_costs()`
- `MultiOutput` subclass (`simkit/config/schema.py:53-99`) supports multiple named output channels via `to_channel_dict()`
- Multi-output executor flow (`pipeline_executor.py:199-211`): checks `isinstance(data, MultiOutput)`, extracts fields, routes to channels
- Field reference resolution (`pipeline_executor.py:355-395`): `getattr(value, binding.field_path)` — works on any object with the named attribute
- **YAML type names use `__name__`**: `Float = RootModel[float]` has `__name__ == "RootModel[float]"` (confirmed: `simkit/tests/test_toy_pipeline.py:37`). The chain spike YAML uses `RootModel[float]`, not `Float`, as the type string.
- `RunResult.outputs` (`pipeline_executor.py:58-65`): `Mapping[str, Any]` keyed by ExitPoint **field names** (from YAML `outputs:` keys), values are channel contents
- Schema type registry (`pipeline_executor.py:404-497`): maps `type.__name__` → type class. Custom types registered via `CUSTOM_SCHEMA_TYPES` list.

### compute_costs() API

- Location: `models/tests/solar_battery/generate_costs.py:1308-1381`
- Signature: `compute_costs(model_path: str, verbose: bool = False) -> dict[str, dict[str, float]]`
- Returns: `{qualified_path: {capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index}}`
- Total capex is at key `"solar_battery_plant"`, field `"capital_cost"` → value `41205.0`

### extract_design_params() API

- Location: `models/tests/solar_battery/generate_costs.py:1521-1567`
- Signature: `extract_design_params(root_usage: Any, total_capex: float) -> dict[str, float]`
- **Requires a syside `root_usage` object**, not just a model path. Getting root_usage requires:
  ```python
  model, _ = SysideAdapter.load_model([model_dir])
  root_usage = None
  for part_usage in SysideAdapter.elements_of_type(model, "PartUsage"):
      if getattr(part_usage, "name", None) == ROOT_PART_NAME:
          root_usage = part_usage
          break
  ```
  (From `generate_costs.py` main(), lines 1821-1836)

### Pre-generated JSON files

`generate_costs.py` main() already writes exactly the files we need:
- `design_params.json` — 11 design parameters including `total_capex` (written at line 1847)
- `component_costs.json` — subsystem cost breakdown (written at line 1842)

These are committed to the repo and kept in sync by `generate_costs.py` test runs.

### Design Parameters Available

From `design_params.json` (produced by `extract_design_params()` at `generate_costs.py:1521`):
```json
{
  "p_net_mw": 0.008, "n_mod": 1.0, "plant_availability": 0.159,
  "plant_lifetime": 25.0, "yearly_inflation": 0.0245, "discount_rate": 0.05,
  "om_rate_per_kw_year": 20.0, "fuel_unit_cost": 0.0, "fuel_consumption": 0.0,
  "p_net_kw": 8.0, "total_capex": 41205.0
}
```

### System-Level CalcUsages (from design.sysml:68-97)

Codegen will discover these 5 CalcUsages at the top level of `solar_battery_plant`:

| CalcUsage | CalcDef | Inputs (bound from) | Outputs |
|-----------|---------|---------------------|---------|
| `energy_production` | `EnergyProductionCalc` | p_net_mw, n_mod, plant_availability (design attrs) | annual_energy_mwh |
| `annualized_om` | `AnnualizedOMCalc` | om_rate_per_kw_year, p_net_kw (design attrs) | annual_om_cost |
| `annualized_fuel` | `AnnualizedFuelCalc` | fuel_unit_cost, fuel_consumption (design attrs) | annual_fuel_cost |
| `annualized_financial` | `AnnualizedFinancialCalc` | total_capex (from `capital_cost`), discount_rate, plant_lifetime | capital_recovery_factor, annualized_capital_cost |
| `lcoe` | `LCOECalc` | annualized_capital_cost (chained), annual_om_cost (chained), annual_fuel_cost (chained), yearly_inflation, plant_lifetime, annual_energy_mwh (chained) | lcoe_per_mwh |

**Critical observation:** `annualized_financial.total_capex` binds to `capital_cost` — the plant's aggregated total. Codegen will see this as an unresolved design attribute (it can't compute component costs). The `ComponentCostEvaluator` module provides this value.

---

## Design Decisions

### DD-1: How does the cost evaluator receive the SysML model path?

**Decision:** Entry point JSON with model path (Option A from spec).

**Rationale:** The entry point JSON already contains design parameters. Adding `model_path` as a string field is the simplest approach and follows the pattern established by the chain spike. The cost evaluator module reads it from its input schema. Hardcoded paths would break reproducibility; environment variables add unnecessary complexity.

### DD-2: How are design parameters passed to system-level modules?

**Decision:** Cost evaluator outputs them alongside total_capex (Option A from spec — single source).

**Rationale:** The cost evaluator module is the single source of truth — it outputs total_capex, per-subsystem costs, AND all design parameters. Codegen-generated modules consume these from the cost evaluator's output channels rather than from the entry point.

**Why not separate entry point JSON?** Codegen's entry point extraction would create a `design_params.json` with the 5 system-level calc parameters, but it wouldn't know about `total_capex` (which comes from component cost computation). Having two sources of truth creates a consistency risk.

### DD-3: Where does the generated code live?

**Decision:** `generated/solar_battery/` (alongside chain spike, Option A from spec).

**Rationale:** Follows the existing convention where `generated/codegen_chain_spike/` lives at the top level. The `generated/` directory is the designated location for codegen output. Putting it under `models/tests/` would mix generated code with the SysML model source.

**Symlink requirement:** If codegen's `--output` directory name differs from `--package-name`, a symlink is needed (as with chain spike: `generated/chain_spike -> codegen_chain_spike`). Since we use `--output generated/solar_battery` and `--package-name solar_battery`, the directory name matches the package name — no symlink needed. If codegen produces a different directory name, add a symlink at that point.

### DD-4: How to handle codegen's pipeline YAML vs actual pipeline YAML?

**Decision:** Write the pipeline YAML manually (Option B from spec).

**Rationale:** The actual pipeline needs the cost evaluator module prepended before the 5 system-level modules, and the wiring is different from what codegen would produce:
- Codegen would wire `total_capex` to a design_params entry point field (it doesn't know about the cost evaluator)
- The actual pipeline wires `total_capex` from the cost evaluator's output
- The YAML is ~50 lines — simpler to write manually than to post-process codegen output

We still run codegen to generate the module wrappers, handwritten stencils, schemas, and tests. We just replace the pipeline YAML with a hand-crafted version that includes the cost evaluator.

### DD-5: How does the cost evaluator get total_capex and design parameters?

**Decision:** Read pre-generated JSON files from disk, with `compute_costs()` called first to ensure they exist and are current.

**Context:** `extract_design_params()` requires a syside `root_usage` object (not just a model path). Getting `root_usage` requires ~15 lines of model loading and element traversal that duplicates `generate_costs.py` main() lines 1821-1836. Three approaches were considered:

- **Option A (load model twice):** Call `compute_costs()` for total_capex, then load model again, find root_usage, call `extract_design_params()`. Duplicates ~20 lines of model-loading logic inside the module.
- **Option B (lower-level flow):** Load model once, compute costs and extract params together. Duplicates `compute_costs()` internals.
- **Option C (read pre-generated JSON):** The cost evaluator calls `compute_costs()` to dynamically compute total_capex and verify it. Then reads `design_params.json` (already written by `generate_costs.py` CI/test runs) for the design parameters. Overrides `total_capex` in the dict with the freshly computed value.

**Chosen: Option C** — pragmatic and avoids duplicating any model-loading logic. The `design_params.json` file is already committed, kept in sync by tests, and contains exactly the 11 parameters we need. The module dynamically computes `total_capex` via `compute_costs()` to prove the pipeline isn't just reading static values, then reads the pre-existing JSON for design params.

**Tradeoff:** If `design_params.json` is stale (e.g., SysML model changed but `generate_costs.py` wasn't re-run), non-capex design params could be wrong. Mitigation: the execution script runs `generate_costs.py` as a pre-step before pipeline execution to ensure JSON files are current. This also produces `component_costs.json` for verification.

### DD-6: Cost evaluator output pattern

**Decision:** Use `MultiOutput` subclass with `RootModel[float]` fields.

**Context:** The cost evaluator needs to output 11 values (total_capex + 10 design params) to separate pipeline channels. Two approaches:

- **Option A (MultiOutput with 11 Float fields):** Each field becomes a separate channel. Downstream modules reference `component_costs__p_net_mw.root`. Proven by `MultiOutput.to_channel_dict()` at `simkit/config/schema.py:84-99`, though only tested with 2 fields (AlphaNeutronSplit).
- **Option B (single BaseModel output + field access):** Output one `CostEvaluatorResult(BaseModel)` with 11 plain float fields. Downstream modules reference `component_costs.p_net_mw`. Simpler — no `.root` unwrapping needed, one channel instead of 11.

**Chosen: Option B** — single-output BaseModel with field access. The executor's `_resolve_input()` at `pipeline_executor.py:382-384` uses `getattr(value, binding.field_path)` to extract fields — this works on any object with named attributes, including plain `BaseModel` instances. This avoids the untested 11-channel MultiOutput pattern and is simpler to write and debug.

The module returns `ModuleResult[CostEvaluatorResult]` where `CostEvaluatorResult` is a `BaseModel` (not `MultiOutput`) with plain `float` fields. In the YAML, the module has a single output channel, and downstream modules use `component_costs.total_capex`, `component_costs.p_net_mw`, etc.

**Risk:** The pipeline validator may not validate field references on non-MultiOutput single-channel outputs the same way. If validation fails, fall back to Option A. The executor itself will work either way — validation is the concern.

---

## Proposed Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Pipeline YAML (hand-crafted)                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  EntryPoint ─── model_path (string) ──→ ComponentCostEvaluator     │
│                                              │                      │
│                    ┌─────────────────────────┘                      │
│                    │ (single BaseModel with all fields)              │
│                    │ .total_capex, .p_net_mw, .n_mod, etc.          │
│                    ▼                                                │
│  ┌─────────────────────────────────────────────┐                   │
│  │  Codegen-generated modules (5)               │                   │
│  │  EnergyProductionCalc ──→ annual_energy_mwh  │                   │
│  │  AnnualizedOMCalc     ──→ annual_om_cost     │                   │
│  │  AnnualizedFuelCalc   ──→ annual_fuel_cost   │                   │
│  │  AnnualizedFinancialCalc ──→ CRF, ann_capex  │                   │
│  │  LCOECalc ──→ lcoe_per_mwh                   │                   │
│  └───────────────────────────────────────────────┘                  │
│                    │                                                │
│                    ▼                                                │
│  ExitPoint ─── lcoe_per_mwh, total_capex, cost breakdown           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Component 1: Run Codegen on Solar+Battery Model

**Purpose:** Generate TEAx module wrappers, handwritten stencils, schemas, and tests for the 5 system-level CalcUsages.

**Initial codegen run (one-time, to get stencils):**
```bash
uv run sysml-codegen generate \
  --models models/tests/solar_battery \
  --output generated/solar_battery \
  --package-name solar_battery \
  --pipeline-name pipeline \
  --overwrite
```

**Subsequent re-runs (after filling in implementations):**
```bash
uv run sysml-codegen generate \
  --models models/tests/solar_battery \
  --output generated/solar_battery \
  --package-name solar_battery \
  --pipeline-name pipeline \
  --preserve-handwritten
```

**Workflow:** Run `--overwrite` once to produce initial stencils. Fill in implementations (Component 2). For any subsequent regeneration (if SysML model changes), use `--preserve-handwritten` to keep the filled-in implementations.

**Verify directory/package alignment:** After running codegen, confirm the output directory name matches `--package-name`. If codegen produces `generated/solar_battery/` and package imports use `solar_battery.*`, no symlink is needed. If they diverge, create a symlink (as chain spike does: `ln -sfn <actual_dir> generated/solar_battery`).

**Expected output structure:**
```
generated/solar_battery/
├── __init__.py                          # Registry + CUSTOM_SCHEMA_TYPES
├── primitives.py                        # Float = RootModel[float]
├── IMPLEMENTATION_BACKLOG.md
├── modules/
│   └── <ns>/                            # namespace from codegen
│       ├── __init__.py
│       ├── energyproductioncalc.py      # ModuleBase[..., RootModel[float]]
│       ├── annualizedomcalc.py          # ModuleBase[..., RootModel[float]]
│       ├── annualizedfuelcalc.py        # ModuleBase[..., RootModel[float]]
│       ├── annualizedfinancialcalc.py   # ModuleBase[..., ???] (see Risk 5)
│       └── lcoecalc.py                  # ModuleBase[..., RootModel[float]]
├── handwritten/
│   └── <ns>/
│       ├── __init__.py
│       ├── energyproductioncalc_impl.py
│       ├── annualizedomcalc_impl.py
│       ├── annualizedfuelcalc_impl.py
│       ├── annualizedfinancialcalc_impl.py
│       └── lcoecalc_impl.py
├── schemas/
│   ├── design_params.py                 # Entry point schema (from codegen)
│   └── (possible multi-output schema for AnnualizedFinancialCalc)
├── pipelines/
│   └── pipeline.yaml                    # Will be replaced with hand-crafted version
├── inputs/
│   └── design_params.json               # Will be replaced
└── tests/
    └── test_implementations_runnable.py
```

**Note:** The exact namespace (e.g., `solarbatterylibrary` vs `solarbatterydesign`) depends on codegen's package name extraction from the SysML model. We adapt to whatever codegen produces.

### Component 2: Fill in 5 Handwritten Implementations

**Purpose:** Provide the actual calculation logic for each system-level CalcUsage.

Each implementation file follows the pattern from `generated/codegen_chain_spike/handwritten/chainspikelibrary/areacalc_impl.py`:

**File: `handwritten/<ns>/energyproductioncalc_impl.py`**
```python
def run_energyproductioncalc(inputs):
    return 8760.0 * inputs.p_net_mw * inputs.n_mod * inputs.plant_availability
```

**File: `handwritten/<ns>/annualizedomcalc_impl.py`**
```python
def run_annualizedomcalc(inputs):
    return inputs.om_rate_per_kw_year * inputs.p_net_kw
```

**File: `handwritten/<ns>/annualizedfuelcalc_impl.py`**
```python
def run_annualizedfuelcalc(inputs):
    return inputs.fuel_unit_cost * inputs.fuel_consumption
```

**File: `handwritten/<ns>/annualizedfinancialcalc_impl.py`**
```python
def run_annualizedfinancialcalc(inputs):
    r = inputs.discount_rate
    n = inputs.plant_lifetime
    crf = r * (1 + r) ** n / ((1 + r) ** n - 1)
    annualized_capital_cost = crf * inputs.total_capex
    return crf, annualized_capital_cost
```
Note: `AnnualizedFinancialCalc` has two outputs (`capital_recovery_factor`, `annualized_capital_cost`). The return pattern (tuple vs dict vs named fields) depends on what codegen generates for the module wrapper — see Risk 5.

**File: `handwritten/<ns>/lcoecalc_impl.py`**
```python
def run_lcoecalc(inputs):
    return (
        inputs.annualized_capital_cost
        + (inputs.annual_om_cost + inputs.annual_fuel_cost)
        * (1.0 + inputs.yearly_inflation) ** inputs.plant_lifetime
    ) / inputs.annual_energy_mwh
```

### Component 3: ComponentCostEvaluator TEAx Module

**Purpose:** Wraps `compute_costs()` as a TEAx module. This is a hand-written module (not codegen-generated) that bridges component-level cost computation into the pipeline.

**Location:** `generated/solar_battery/modules/component_cost_evaluator.py`

**Input Schema:**
```python
from pydantic import BaseModel, Field

class CostEvaluatorInput(BaseModel):
    """Input for ComponentCostEvaluator module."""
    model_path: str = Field(..., description="Path to SysML model directory")
```

**Output Schema (single BaseModel, not MultiOutput):**
```python
from pydantic import BaseModel

class CostEvaluatorResult(BaseModel):
    """Output from ComponentCostEvaluator module.

    Single object containing total_capex and all design parameters.
    Downstream modules access fields via dot notation in YAML
    (e.g., component_costs.total_capex).
    """
    total_capex: float
    p_net_mw: float
    n_mod: float
    plant_availability: float
    plant_lifetime: float
    yearly_inflation: float
    discount_rate: float
    om_rate_per_kw_year: float
    fuel_unit_cost: float
    fuel_consumption: float
    p_net_kw: float
```

**Module class:**
```python
import json
from pathlib import Path

from simkit.core.base import ModuleBase, ModuleResult

class ComponentCostEvaluator(ModuleBase[CostEvaluatorInput, CostEvaluatorResult]):
    name: str = "ComponentCostEvaluator"
    version: str = "v0.1"

    def validate_and_fill_default(self, model_path: str) -> CostEvaluatorInput:
        return CostEvaluatorInput(model_path=model_path)

    def run(self, model_path: str) -> ModuleResult[CostEvaluatorResult]:
        validated = self.validate_and_fill_default(model_path)
        model_dir = Path(validated.model_path)

        # 1. Dynamically compute total_capex via compute_costs()
        compute_costs = self._import_compute_costs(model_dir)
        costs = compute_costs(str(model_dir))
        total_capex = costs["solar_battery_plant"]["capital_cost"]

        # 2. Read design parameters from pre-generated JSON
        design_params_path = model_dir / "design_params.json"
        with open(design_params_path) as f:
            params = json.load(f)

        # 3. Override total_capex with dynamically computed value
        params["total_capex"] = total_capex

        return ModuleResult(data=CostEvaluatorResult(**params))

    @staticmethod
    def _import_compute_costs(model_dir: Path):
        """Import compute_costs from generate_costs.py using importlib."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_costs",
            model_dir / "generate_costs.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.compute_costs
```

**Key design choices:**
- Uses `importlib.util.spec_from_file_location()` instead of `sys.path` manipulation — avoids polluting global interpreter state (addresses Issue 7)
- Reads `design_params.json` for design params instead of duplicating the `extract_design_params()` flow that requires `root_usage` (addresses Issue 1)
- Dynamically computes `total_capex` via `compute_costs()` to prove the pipeline isn't just reading static values
- Returns single `CostEvaluatorResult(BaseModel)` — downstream modules use field access (addresses Issue 2)

### Component 4: Pipeline YAML (Hand-Crafted)

**Location:** `generated/solar_battery/pipelines/pipeline.yaml`

This replaces the codegen-generated pipeline YAML. It wires the cost evaluator output into the system-level modules.

**YAML type name convention:** Use `RootModel[float]` (not `Float`) to match the proven chain spike pattern. `Float = RootModel[float]` and `RootModel[float].__name__ == "RootModel[float]"`, so the schema registry resolves `RootModel[float]` correctly. The chain spike YAML exclusively uses `RootModel[float]` as the type string.

```yaml
metadata:
  run_description: "Solar+Battery LCOE Pipeline (hybrid: generate_costs.py + codegen)"
  output_folder: "solar_battery_results"

modules:
  # Entry point: just the model path
  entry_point:
    module_type: EntryPoint
    inputs:
      config: PipelineConfig ../inputs/pipeline_config.json

  # Component cost evaluator (wraps generate_costs.py)
  # Single-output module: returns CostEvaluatorResult BaseModel
  # Downstream modules access fields via dot notation
  component_costs:
    module_type: ComponentCostEvaluator
    inputs:
      model_path: str config.model_path
    outputs:
      root: CostEvaluatorResult component_costs

  # System-level modules (codegen-generated wrappers, handwritten impls)
  energy_production:
    module_type: <ns>.EnergyProductionCalcModule
    inputs:
      p_net_mw: float component_costs.p_net_mw
      n_mod: float component_costs.n_mod
      plant_availability: float component_costs.plant_availability
    outputs:
      root: RootModel[float] energy_production__annual_energy_mwh

  annualized_om:
    module_type: <ns>.AnnualizedOMCalcModule
    inputs:
      om_rate_per_kw_year: float component_costs.om_rate_per_kw_year
      p_net_kw: float component_costs.p_net_kw
    outputs:
      root: RootModel[float] annualized_om__annual_om_cost

  annualized_fuel:
    module_type: <ns>.AnnualizedFuelCalcModule
    inputs:
      fuel_unit_cost: float component_costs.fuel_unit_cost
      fuel_consumption: float component_costs.fuel_consumption
    outputs:
      root: RootModel[float] annualized_fuel__annual_fuel_cost

  annualized_financial:
    module_type: <ns>.AnnualizedFinancialCalcModule
    inputs:
      total_capex: float component_costs.total_capex
      discount_rate: float component_costs.discount_rate
      plant_lifetime: float component_costs.plant_lifetime
    outputs:
      capital_recovery_factor: RootModel[float] annualized_financial__capital_recovery_factor
      annualized_capital_cost: RootModel[float] annualized_financial__annualized_capital_cost

  lcoe:
    module_type: <ns>.LCOECalcModule
    inputs:
      annualized_capital_cost: float annualized_financial__annualized_capital_cost.root
      annual_om_cost: float annualized_om__annual_om_cost.root
      annual_fuel_cost: float annualized_fuel__annual_fuel_cost.root
      yearly_inflation: float component_costs.yearly_inflation
      plant_lifetime: float component_costs.plant_lifetime
      annual_energy_mwh: float energy_production__annual_energy_mwh.root
    outputs:
      root: RootModel[float] lcoe__lcoe_per_mwh

  # Exit point
  exit_point:
    module_type: ExitPoint
    outputs:
      total_capex: RootModel[float] component_costs__total_capex.json
      annual_energy_mwh: RootModel[float] energy_production__annual_energy_mwh.json
      annual_om_cost: RootModel[float] annualized_om__annual_om_cost.json
      annual_fuel_cost: RootModel[float] annualized_fuel__annual_fuel_cost.json
      capital_recovery_factor: RootModel[float] annualized_financial__capital_recovery_factor.json
      annualized_capital_cost: RootModel[float] annualized_financial__annualized_capital_cost.json
      lcoe_per_mwh: RootModel[float] lcoe__lcoe_per_mwh.json
```

**Notes:**
- `<ns>` is a placeholder for the actual namespace codegen produces. The exact module_type names (e.g., `solarbatterylibrary.EnergyProductionCalcModule`) will be determined after running codegen.
- The cost evaluator uses `CostEvaluatorResult` as the YAML output type (must be in `CUSTOM_SCHEMA_TYPES`).
- Single-output codegen modules use `root: RootModel[float]` — downstream `.root` extraction gets the float value.
- `annualized_financial` has 2 outputs — if codegen generates a `MultiOutput`, the YAML output section has 2 fields. If codegen doesn't support multi-output, see Risk 5 for fallback.
- The exit point needs `RootModel[float]` values, but `component_costs` is a `CostEvaluatorResult` (BaseModel, not RootModel). The exit point for `total_capex` references channel `component_costs__total_capex` — this requires the cost evaluator or a separate extraction step to put a `RootModel[float]` value in that channel. **Simplification:** The exit point can reference any channel that exists. We need to ensure the channels referenced in the exit point actually exist. The system-level module outputs (e.g., `energy_production__annual_energy_mwh`) are `RootModel[float]`. For `total_capex`, we can either: (a) add a passthrough in the exit point from `component_costs.total_capex`, or (b) capture it from the `annualized_financial` module's input. This is a YAML wiring detail to resolve during implementation.

### Component 5: Pipeline Config and Entry Point

**Location:** `generated/solar_battery/inputs/pipeline_config.json`

```json
{
  "model_path": "models/tests/solar_battery"
}
```

**Schema:** `generated/solar_battery/schemas/pipeline_config.py`

```python
from pydantic import BaseModel, Field

class PipelineConfig(BaseModel):
    model_path: str = Field(..., description="Path to SysML model directory")
    model_config = {"frozen": True, "extra": "forbid"}
```

**Path resolution:** The execution script (Component 7) resolves `model_path` to an absolute path before pipeline execution, ensuring it works regardless of working directory.

### Component 6: Registry Updates

**Location:** `generated/solar_battery/__init__.py`

The codegen-generated `__init__.py` will register the 5 system-level modules. We modify it to also register `ComponentCostEvaluator` and the custom schemas:

```python
from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

# Codegen-generated modules (exact imports depend on codegen output)
from solar_battery.modules.<ns>.energyproductioncalc import EnergyProductionCalcModule
# ... etc for all 5 modules

# Hand-written module
from solar_battery.modules.component_cost_evaluator import (
    ComponentCostEvaluator,
    CostEvaluatorResult,
)

# Schemas
from solar_battery.schemas.pipeline_config import PipelineConfig
from solar_battery.primitives import Float  # = RootModel[float]

def create_solar_battery_registry() -> PipelineModuleRegistry:
    return create_registry(
        [
            ComponentCostEvaluator,
            EnergyProductionCalcModule,
            # ... etc for all 5 codegen modules
        ],
        module_type_override={
            ComponentCostEvaluator: "ComponentCostEvaluator",
            # ... codegen module type overrides (namespace.ClassName pattern)
        },
    )

CUSTOM_SCHEMA_TYPES = [PipelineConfig, CostEvaluatorResult, Float]
```

### Component 7: Execution Script

**Location:** `generated/solar_battery/run_pipeline.py`

```python
#!/usr/bin/env python3
"""Execute the solar+battery LCOE pipeline.

Usage:
    uv run python generated/solar_battery/run_pipeline.py
"""
import json
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery import create_solar_battery_registry, CUSTOM_SCHEMA_TYPES


def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    pipeline_dir = Path(__file__).resolve().parent

    # Resolve model path to absolute (ensures working directory independence)
    config_path = pipeline_dir / "inputs" / "pipeline_config.json"
    with open(config_path) as f:
        config = json.load(f)
    model_path = (project_root / config["model_path"]).resolve()

    # Write resolved config for pipeline execution
    resolved_config = pipeline_dir / "inputs" / "pipeline_config_resolved.json"
    with open(resolved_config, "w") as f:
        json.dump({"model_path": str(model_path)}, f, indent=2)

    # Execute pipeline
    pipeline_path = pipeline_dir / "pipelines" / "pipeline.yaml"
    output_dir = pipeline_dir / "outputs"
    registry = create_solar_battery_registry()

    result = execute_pipeline(
        spec_path=str(pipeline_path),
        output_dir=str(output_dir),
        registry=registry,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )

    # Print results — result.outputs is keyed by ExitPoint field names
    print("Pipeline completed successfully!")
    for name, value in result.outputs.items():
        # RootModel[float] values have a .root attribute
        val = getattr(value, "root", value)
        print(f"  {name}: {val}")

    return result


if __name__ == "__main__":
    main()
```

**Note on result access:** `result.outputs` is `Mapping[str, Any]` keyed by ExitPoint YAML field names (`pipeline_executor.py:132-138`). Values are the channel contents — for `RootModel[float]` channels, access `.root` to get the float. The script uses `getattr(value, "root", value)` defensively.

### Component 8: Verification Script

**Location:** `generated/solar_battery/verify_pipeline.py`

Compares pipeline output against expected values:

```python
#!/usr/bin/env python3
"""Verify pipeline output against expected values.

Usage:
    uv run python generated/solar_battery/verify_pipeline.py
"""
import json
import sys
from pathlib import Path

EXPECTED_VALUES = {
    "total_capex": (41205.0, 0.0),          # exact match
    "annual_energy_mwh": (11.14272, 0.01),   # 1% tolerance
    "annual_om_cost": (160.0, 0.01),
    "annual_fuel_cost": (0.0, 0.0),          # exact
    "capital_recovery_factor": (0.070952, 0.01),
    "annualized_capital_cost": (2923.60, 0.01),
    "lcoe_per_mwh": (288.68, 0.01),
}


def verify(output_dir: Path) -> bool:
    all_pass = True
    for name, (expected, tolerance) in EXPECTED_VALUES.items():
        output_file = output_dir / f"{name}.json"
        if not output_file.exists():
            print(f"  FAIL {name}: output file not found")
            all_pass = False
            continue

        with open(output_file) as f:
            actual = json.load(f)

        # RootModel[float] serializes as just the float value
        if isinstance(actual, dict) and "root" in actual:
            actual = actual["root"]

        if expected == 0.0:
            passed = actual == 0.0
        elif tolerance == 0.0:
            passed = abs(actual - expected) < 0.01  # exact within rounding
        else:
            passed = abs(actual - expected) / abs(expected) <= tolerance

        status = "PASS" if passed else "FAIL"
        print(f"  {status} {name}: expected={expected}, actual={actual}")
        if not passed:
            all_pass = False

    return all_pass


def main():
    output_dir = Path(__file__).resolve().parent / "outputs" / "solar_battery_results"
    print("Verifying pipeline output...")
    success = verify(output_dir)
    print(f"\nOverall: {'PASS' if success else 'FAIL'}")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Potential Risks

### Risk 1: Codegen namespace mismatch
**Issue:** Codegen's namespace for the solar+battery model may differ from what we expect (e.g., `solarbatterydesign` vs `solarbatterylibrary`).
**Mitigation:** Run codegen first, inspect output, then adapt the pipeline YAML and registry accordingly. The design above uses `<ns>` as a placeholder intentionally.

### Risk 2: Package name vs directory name misalignment
**Issue:** If codegen output directory name doesn't match `--package-name`, Python imports will fail.
**Mitigation:** Verify after codegen run. If misaligned, create a symlink: `ln -sfn <actual_dir_name> generated/solar_battery` (same pattern as chain spike: `generated/chain_spike -> codegen_chain_spike`).

### Risk 3: Model path resolution across working directories
**Issue:** Pipeline runs from different working directories could break relative model paths.
**Mitigation:** The execution script resolves the model path to absolute before pipeline execution. Writes a `pipeline_config_resolved.json` with the absolute path.

### Risk 4: design_params.json staleness
**Issue:** If SysML model changes but `generate_costs.py` isn't re-run, design parameters could be stale.
**Mitigation:** The execution script should run `generate_costs.py` as a pre-step (or verify JSON timestamps). The cost evaluator dynamically computes `total_capex` via `compute_costs()`, so the most critical value is always fresh. The other 10 design parameters are literal values from `design.sysml` that rarely change independently.

### Risk 5: AnnualizedFinancialCalc multi-output codegen support
**Issue:** This calc has 2 outputs (`capital_recovery_factor`, `annualized_capital_cost`). The chain spike has only single-output calcs, so codegen's multi-output module generation is unverified. Codegen may not generate a `MultiOutput` wrapper, or may generate it incorrectly.
**Mitigation:** After running codegen, inspect the generated `annualizedfinancialcalc.py`. Three possible outcomes:
1. **Codegen generates MultiOutput correctly** → use as-is
2. **Codegen generates single-output (picks one output)** → hand-write the module wrapper with MultiOutput pattern
3. **Codegen fails** → hand-write both the module wrapper and the output schema

In cases 2 or 3, hand-write `modules/<ns>/annualizedfinancialcalc.py` following the `MultiOutput` pattern from `simkit/config/schema.py:53-99`. This is ~40 lines of straightforward code.

### Risk 6: CostEvaluatorResult field access in pipeline validator
**Issue:** The pipeline validator may not resolve field references on non-MultiOutput single-channel outputs. The executor itself will work (`_resolve_input` uses plain `getattr`), but validation could reject the YAML.
**Mitigation:** If validator rejects `component_costs.total_capex` references, fall back to the MultiOutput pattern (DD-6 Option A: 11 separate `RootModel[float]` channels). This is more verbose in the YAML but avoids validator concerns.

### Risk 7: compute_costs() import from non-package directory
**Issue:** `generate_costs.py` lives in `models/tests/solar_battery/` which is not a Python package.
**Mitigation:** Use `importlib.util.spec_from_file_location()` for clean dynamic import without `sys.path` pollution. This is a standard Python pattern for importing from arbitrary file paths.

---

## Integration Strategy

### How it fits into existing workflows
- **Builds on proven pieces:** `generate_costs.py` (Item 3), codegen (Item 2), TEAx framework
- **Adds one new module type:** `ComponentCostEvaluator` — the bridge between component costs and system-level calcs
- **Uses standard TEAx patterns:** Same registry, pipeline YAML, and execution approach as chain spike
- **Does not modify:** SysML models, codegen source, TEAx framework, or `generate_costs.py`

### What it replaces
- Retires Item 4 from the epic (codegen on solar+battery + fill implementations) — folded into this item
- Replaces the abandoned "static entry point injection" approach (old Items 4-5) with a dynamic pipeline

---

## Validation Approach

### Unit validation
1. Run codegen → verify 5 modules generated without errors
2. Run codegen-generated tests → verify implementations match expected signatures
3. Run existing `generate_costs.py` tests → verify no regressions

### Integration validation
1. Execute pipeline → verify no runtime errors
2. Compare each output against `expected_system_outputs.csv`:
   - `total_capex` = $41,205.00 (exact)
   - `annual_energy_mwh` = 11.14272 MWh (±1%)
   - `annual_om_cost` = $160.00 (±1%)
   - `annual_fuel_cost` = $0.00 (exact)
   - `capital_recovery_factor` = 0.070952 (±1%)
   - `annualized_capital_cost` = $2,923.60 (±1%)
   - `lcoe_per_mwh` = $288.68 (±1%)

### Reproducibility validation
1. Run `uv run python generated/solar_battery/run_pipeline.py` from project root
2. Run `uv run python generated/solar_battery/verify_pipeline.py` → PASS

---

**Next Step:** After approval → `/_my_plan` to break into implementation phases, or `/_my_implement` to proceed directly.
