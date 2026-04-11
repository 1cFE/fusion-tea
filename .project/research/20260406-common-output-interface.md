# Research: Common Output Interface for Concept Analysis Scripts

**Date**: 2026-04-06
**Context**: The concept explorer needs structured data from both costingfe-backed and freeform model_setup.py scripts. This document investigates the exact data structures on both sides and evaluates options for a common interface.

**Related**: `.project/research/20260406-model-setup-extraction-interface-gap.md` (the gap analysis that motivated this)

---

## 1. Current State

### 1.1 ForwardResult Shape (costingfe)

**Source**: `/home/reid/1cfe/1costingfe/src/costingfe/types.py` lines 139-147

```python
@dataclass
class ForwardResult:
    power_table: PowerTable
    costs: CostResult
    params: dict              # All input params (for sensitivity analysis)
    overridden: list[str]     # Keys that were overridden (CAS account names)
    cas22_detail: dict[str, float]  # CAS22 sub-accounts (C220101-C220700)
    plasma_state: object      # PlasmaState when 0D model is active (optional)
```

**PowerTable** (`types.py` lines 79-106): 22 power flow fields, all `float`:

| Field | Type | Description |
|-------|------|-------------|
| `p_fus` | float | Fusion power [MW] |
| `p_ash` | float | Charged fusion product power [MW] |
| `p_neutron` | float | Neutron power [MW] |
| `p_rad` | float | Plasma radiation power [MW] |
| `p_wall` | float | Ash thermal on walls [MW] |
| `p_dee` | float | Direct energy extracted electric [MW] |
| `p_dec_waste` | float | DEC waste heat [MW] |
| `p_th` | float | Total thermal power [MW] |
| `p_the` | float | Thermal electric power [MW] |
| `p_et` | float | Gross electric power [MW] |
| `p_loss` | float | Lost power [MW] |
| `p_net` | float | Net electric power [MW] |
| `p_pump` | float | Pumping power [MW] |
| `p_sub` | float | Subsystem power [MW] |
| `p_aux` | float | Auxiliary power [MW] |
| `p_input` | float | Effective heating power [MW] |
| `p_coils` | float | Coil power [MW] (MFE) |
| `p_cool` | float | Cooling power [MW] (MFE) |
| `p_cryo` | float | Cryogenic system power [MW] |
| `p_target` | float | Target factory power [MW] (IFE/MIF) |
| `q_sci` | float | Scientific Q |
| `q_eng` | float | Engineering Q |
| `rec_frac` | float | Recirculating power fraction |

**CostResult** (`types.py` lines 110-136): 22 cost fields, all `float`, in M$:

| Field | Type | Description |
|-------|------|-------------|
| `cas10`-`cas29` | float | Individual CAS accounts [M$] |
| `cas20` | float | Total direct costs (CAS21-29 sum) [M$] |
| `cas30`-`cas90` | float | Indirect, owner, supplementary, IDC, O&M, fuel, financial [M$] |
| `cas71`, `cas72` | float | O&M and scheduled replacement sub-accounts [M$] |
| `total_capital` | float | CAS10-60 sum [M$] |
| `lcoe` | float | Levelized cost of electricity [$/MWh] |
| `overnight_cost` | float | Overnight capital cost [$/kW] |

**cas22_detail** keys: `C220101`, `C220102`, ..., `C220112` (per-module), `C220200`, `C220300`, ..., `C220700` (plant-wide), `C220000` (total). All values in M$.

**params**: A flat dict of all input parameters merged from engineering defaults + user overrides + named args. Includes both engineering params (eta_th, p_input, etc.) and plant-level params (net_electric_mw, availability, lifetime_yr, n_mod, etc.). All values are numeric or enum.

### 1.2 CostModel.forward() Signature

**Source**: `/home/reid/1cfe/1costingfe/src/costingfe/model.py` lines 344-356

```python
def forward(
    self,
    net_electric_mw: float,
    availability: float,
    lifetime_yr: float,
    n_mod: int = 1,
    construction_time_yr: float = 6.0,
    interest_rate: float = 0.07,
    inflation_rate: float = 0.02,
    noak: bool = True,
    cost_overrides: dict[str, float] | None = None,
    **overrides,
) -> ForwardResult:
```

Named args are plant-level requirements. `**overrides` captures engineering parameter overrides (eta_th, p_input, etc.). `cost_overrides` are CAS-account-level cost substitutions (e.g., `{"CAS22": 500.0}`).

### 1.3 CostModel.sensitivity() Return Shape

**Source**: `/home/reid/1cfe/1costingfe/src/costingfe/model.py` lines 779-814

```python
def sensitivity(self, params: dict, cost_overrides=None) -> dict[str, dict[str, float]]:
```

Returns:
```python
{
    "engineering": {"eta_th": 0.45, "p_input": -0.12, ...},  # elasticity values
    "financial": {"interest_rate": 0.31, "inflation_rate": 0.05}
}
```

Each value is a dimensionless elasticity: `(dLCOE/dp) * (p/LCOE)`. Uses JAX autodiff (`jax.grad`) for exact gradients. The `params` argument is typically `result.params` from a previous `forward()` call.

### 1.4 What the Explorer Consumes

**Source**: `exploration/concept_explorer/models.py` and `exploration/concept_explorer/extract_explorer_data.py`

#### CostModelData (Pydantic model, `models.py` lines 111-298)

The explorer's canonical cost model representation. Constructed via `CostModelData.from_forward_result()` which takes `dataclasses.asdict(forward_result)`.

Fields consumed from ForwardResult:

| Explorer field | ForwardResult source | Notes |
|----------------|---------------------|-------|
| `cas10`-`cas90` (CASAccount) | `costs.cas10`-`costs.cas90` | Each wrapped in `CASAccount(name=..., cost_m_usd=..., overridden=...)` |
| `cas22_detail` | `cas22_detail` dict | 18 sub-accounts (C220101-C220112, C220200-C220700), wrapped in CASAccount |
| `headline.lcoe_per_mwh` | `costs.lcoe` | |
| `headline.overnight_cost_per_kw` | `costs.overnight_cost` | |
| `headline.p_net_mw` | `power_table.p_net` | |
| `headline.q_eng` | `power_table.q_eng` | |
| `headline.capacity_factor` | `power_table.availability` (injected) | Fallback: `power_table.capacity_factor` |
| `sensitivities` | Built from `model.sensitivity(result.params)` | `SensitivityAnalysis` with engineering/financial dicts |
| `params` | `result.params` filtered to numeric | Flat dict of `{str: float}` |

#### `from_forward_result()` input contract (`models.py` lines 186-298)

Expects a dict shaped like `dataclasses.asdict(ForwardResult)`:
```python
{
    "costs": {"cas10": float, "cas21": float, ..., "lcoe": float, "overnight_cost": float},
    "power_table": {"p_net": float, "q_eng": float, "availability": float, ...},
    "cas22_detail": {"C220101": float, ...},
    "overridden": ["C220103", ...],
    "params": {"net_electric_mw": float, ...},
}
```

Missing keys default to 0.0. Missing CAS22 sub-accounts default to 0.0. This is already tolerant of partial data.

#### SensitivityAnalysis (`models.py` lines 97-108)

```python
class SensitivityAnalysis(BaseModel):
    engineering: dict[str, SensitivityEntry]  # {param_name: {elasticity, baseline}}
    financial: dict[str, SensitivityEntry]
```

Built by `build_sensitivity_analysis()` in `extract_explorer_data.py` (lines 132-153), which calls `model.sensitivity(result.params)` and wraps results.

### 1.5 Server Live Recomputation Path

**Source**: `exploration/concept_explorer/server.py`

The server's `/api/compute` endpoint (`_compute_cached()`, lines 534-571) loads the module, grabs `model` and `result`, then calls:

```python
_forward_with_overrides(model, result.params, dict(overrides))
```

This calls `model.forward()` with the original params updated by slider overrides. It then runs `CostModelData.from_forward_result()` on the new result.

**Key requirement**: The server needs a callable `model.forward()` and a baseline `result.params` dict. Without these, live slider recomputation is impossible.

### 1.6 What Freeform Scripts Produce

Surveyed: concepts 02 (Acoustic ICF), 12 (Levitated Dipole), 15 (Z-Pinch), 22 (Projectile ICF).

#### Common architecture

All freeform scripts follow the same 5-layer pattern from the prompt template:

1. A `@dataclass` with all plant parameters (e.g., `LevitatedDipolePlantParams`)
2. Five methods: `_compute_power()`, `_compute_geometry()`, `_compute_cas22()`, `_compute_costs()`, `_compute_economics()`
3. Each method returns a `dict[str, float]` (plain dict, not dataclass)
4. A `compute()` method merges all five dicts into a nested result
5. `print_results()` prints formatted output to stdout
6. `sensitivity_sweep()` does brute-force single-parameter sweeps
7. `main()` creates the dataclass, calls `compute()`, prints results, runs sweeps

#### Data structures (all are plain dicts)

**power dict** (from `_compute_power()`):
```python
{
    "p_fus": float,         # Fusion power [MW]
    "p_neutron": float,     # Neutron power [MW]
    "p_alpha": float,       # Alpha/charged particle power [MW]
    "p_th": float,          # Total thermal power [MW]
    "p_et": float,          # Gross electric [MW]
    "p_net": float,         # Net electric [MW]
    "p_recirc_MW": float,   # Recirculating power [MW]
    "recirc_fraction": float,  # Recirculating fraction
    "capacity_factor": float,  # Plant capacity factor [0-1]
    "annual_energy_MWh": float,
    "Qsci": float,         # Scientific Q
    "Qeng_approx": float,  # Engineering Q (approximate)
    # ... concept-specific keys (p_icrh_wallplug_MW, p_driver_avg_MW, etc.)
}
```

**cas22 dict** (from `_compute_cas22()`):
```python
{
    "C220101": float,  # First Wall & Blanket [M$]
    "C220102": float,  # Shield [M$]
    "C220103": float,  # Magnets/Coils [M$]
    "C220104": float,  # Heating/Driver [M$]
    "C220105": float,  # Primary Structure [M$]
    "C220106": float,  # Vacuum System [M$]
    "C220107": float,  # Power Conditioning [M$]
    "C220108": float,  # Target Factory [M$]
    "C220109": float,  # Direct Energy Converter [M$]
    "C220110": float,  # Remote Handling [M$]
    "C220111": float,  # Installation Labor [M$]
    "C220112": float,  # Isotope Separation [M$]
    "C220200": float,  # Main & Secondary Coolant [M$]
    "C220300": float,  # Auxiliary Cooling & Cryoplant [M$]
    "C220400": float,  # Radioactive Waste Management [M$]
    "C220500": float,  # Fuel Handling [M$]
    "C220600": float,  # Other Reactor Plant Equipment [M$]
    "C220700": float,  # Instrumentation & Control [M$]
    "CAS22": float,    # Total CAS22 [M$]
    "CAS22_per_module": float,
    "CAS22_plant_wide": float,
}
```

**costs dict** (from `_compute_costs()`):
```python
{
    "CAS10": float,  # Pre-construction [M$]
    "CAS21": float,  # Buildings [M$]
    "CAS22": float,  # Reactor Plant Equipment [M$]
    "CAS23": float,  # Turbine Plant [M$]
    "CAS24": float,  # Electric Plant [M$]
    "CAS25": float,  # Misc Plant [M$]
    "CAS26": float,  # Heat Rejection [M$]
    "CAS27": float,  # Special Materials [M$]
    "CAS28": float,  # Digital Twin [M$]
    "CAS29": float,  # Contingency [M$]
    "CAS20": float,  # Total Direct Costs [M$]
    "CAS30": float,  # Indirect Costs [M$]
    "CAS40": float,  # Owner's Costs [M$]
    "CAS50": float,  # Supplementary Costs [M$]
    "CAS60": float,  # IDC [M$]
    "overnight_capital": float,  # CAS10-50 sum [M$]
    "total_capital": float,      # CAS10-60 sum [M$]
    "specific_capital_USD_per_kWe": float,  # $/kW
}
```

**economics dict** (from `_compute_economics()`):
```python
{
    "CAS70": float,   # Total O&M [M$/yr]
    "CAS71": float,   # O&M base [M$/yr]
    "CAS72": float,   # Scheduled replacement [M$/yr]
    "CAS80": float,   # Fuel [M$/yr]
    "CAS90": float,   # Capital charge [M$/yr]
    "lcoe_USD_per_MWh": float,
    "lcoe_cents_per_kWh": float,
    # ... concept-specific breakdown keys
}
```

#### Key observation: Freeform CAS structure is nearly identical to CostResult

The freeform scripts compute every CAS account that CostResult has, using the same account numbering. The differences are:

1. **Naming**: Freeform uses `"CAS10"`, `"CAS21"`, etc. (uppercase). CostResult uses `cas10`, `cas21` (lowercase attributes).
2. **Structure**: Freeform uses nested plain dicts (`results["costs"]["CAS10"]`). CostResult is a flat dataclass with typed attributes.
3. **Key naming**: Freeform `costs["overnight_capital"]` vs CostResult `overnight_cost` ($/kW, not M$). Freeform `economics["lcoe_USD_per_MWh"]` vs CostResult `lcoe`.
4. **Power table**: Freeform `power["p_net"]` and `power["Qeng_approx"]` vs PowerTable `p_net` and `q_eng`. Field set differs (freeform has fewer standard fields, more concept-specific ones).
5. **CAS22 detail**: Freeform uses identical keys (C220101-C220700) with identical semantics. Structurally compatible.

#### What freeform scripts DON'T produce

- No `ForwardResult` dataclass (no costingfe import)
- No `model` (CostModel instance) at module level
- No `result` at module level
- No `params` dict (parameters live as `@dataclass` fields)
- No `overridden` list
- No standardized sensitivity output (brute-force sweeps, not elasticities)
- Everything runs inside `main()` -- no module-level artifacts to extract

#### Sensitivity analysis in freeform scripts

**Source**: e.g., `12-levitated-dipole/model_setup.py` lines 1013-1025

```python
def sensitivity_sweep(base_params, param_name, values, label=""):
    results_list = []
    for val in values:
        p = LevitatedDipolePlantParams(**{**base_params.__dict__, param_name: val})
        r = p.compute()
        results_list.append({
            "param_value": float(val),
            "lcoe_cents_kWh": r["lcoe_cents_per_kWh"],
            "net_electric_MW": r["net_electric_MW"],
        })
    return results_list
```

This is a brute-force sweep over discrete values. It computes LCOE at N points per parameter and reports the raw values. There is no elasticity computation, no JAX autodiff.

### 1.7 Current Prompt Templates

**costingfe template** (`model_setup_costingfe.md`):
- Tells the LLM to create a `CostModel`, call `.forward()`, print results, call `.sensitivity()`
- Does NOT mandate that `result` be a module-level variable
- Does NOT mention the explorer or extraction

**freeform template** (`model_setup_freeform.md`):
- Tells the LLM to write a self-contained script with `@dataclass`, five `_compute_*()` methods, `print_results()`, `sensitivity_sweep()`, and `main()`
- Prescribes CAS-structured accounting following the MagLIF exemplar
- Does NOT mention any export function, `to_explorer_dict()`, or module-level variables
- Does NOT mention the explorer or extraction

---

## 2. Target State

For cross-concept comparison, the explorer needs from every concept:

1. **Headline economics**: LCOE ($/MWh), overnight cost ($/kW), p_net (MW), Q_eng, capacity factor
2. **CAS cost breakdown**: CAS10-CAS90, each as M$ with a human-readable name
3. **CAS22 detail**: C220101-C220700, each as M$ with a human-readable name
4. **Sensitivity data**: Elasticity of LCOE to each tunable parameter (dimensionless, same scale across concepts)
5. **Parameter baselines**: The numeric value of each parameter at which the model was evaluated
6. **Recomputation capability** (nice-to-have): Ability to re-evaluate the model with modified parameters for slider interaction

Items 1-3 are needed for cost comparison charts, waterfall diagrams, and CAS breakdown views.
Item 4 is needed for tornado charts and cross-concept parameter comparison.
Item 5 is needed for displaying what a parameter "means" alongside its sensitivity.
Item 6 enables interactive what-if exploration.

---

## 3. Gap Analysis

### Field-by-field comparison

| Data needed | costingfe ForwardResult | Freeform scripts | Gap |
|------------|------------------------|------------------|-----|
| LCOE ($/MWh) | `costs.lcoe` | `economics["lcoe_USD_per_MWh"]` | Key naming only |
| Overnight cost ($/kW) | `costs.overnight_cost` | `costs["specific_capital_USD_per_kWe"]` | Key naming only |
| p_net (MW) | `power_table.p_net` | `power["p_net"]` | None |
| Q_eng | `power_table.q_eng` | `power["Qeng_approx"]` | Key naming only |
| Capacity factor | Injected from `params["availability"]` | `power["capacity_factor"]` | None |
| CAS10-CAS90 (M$) | `costs.cas10`-`costs.cas90` | `costs["CAS10"]`-`costs["CAS29"]` + `economics["CAS70"]`-`economics["CAS90"]` | Split across two dicts; key case; CAS70-90 in "economics" not "costs" |
| CAS22 detail | `cas22_detail` dict (C220101-C220700 keys) | `cas22` dict (same keys) | None (structurally identical) |
| CAS71, CAS72 | `costs.cas71`, `costs.cas72` | `economics["CAS71"]`, `economics["CAS72"]` | Split across dicts, key case |
| total_capital (M$) | `costs.total_capital` | `costs["total_capital"]` | None |
| Overridden accounts | `overridden` list | Not tracked | Missing entirely |
| params dict | `params` (flat dict of all inputs) | Encoded as `@dataclass` fields, no dict | Must extract from dataclass `__dict__` |
| Sensitivity elasticities | `model.sensitivity(params)` returns `{eng: {k: float}, fin: {k: float}}` | `sensitivity_sweep()` returns `[{param_value, lcoe}]` per sweep | Fundamentally different format; no elasticities computed |
| Recomputation | `model.forward(**overrides)` | `ParamsDataclass(**{**base.__dict__, k: v}).compute()` | Different API but same capability |

### Summary of gaps

1. **Trivial naming gaps** (LCOE, overnight cost, Q_eng key names): Solved by a mapping dict in the adapter.

2. **Structural gap** (nested dicts vs flat dataclass): Freeform results are spread across `power`, `costs`, `economics`, `cas22` sub-dicts. CostResult is a flat dataclass. A thin adapter can flatten/rename.

3. **Missing `overridden` list**: Freeform scripts don't track which CAS accounts were overridden vs computed from defaults. This could be added to the dataclass (list the parameter names that were set to non-default values) or omitted (set to empty list).

4. **No `params` dict**: Freeform parameters live as `@dataclass` fields. Easily extracted via `dataclasses.asdict(params_instance)` or `params_instance.__dict__`.

5. **Sensitivity format mismatch** (the biggest gap): costingfe provides JAX-based exact elasticities. Freeform scripts do brute-force sweeps returning raw LCOE values at discrete points. Converting sweeps to elasticities requires finite-difference computation: `elasticity_i = (LCOE(p_i+dp) - LCOE(p_i-dp)) / (2*dp) * p_i / LCOE_base`. This is approximatable from sweep data but not identical to autodiff.

6. **No module-level artifacts**: Freeform scripts have no module-level `model` or `result`. Everything lives inside `main()`. The extraction interface gap spec addresses this routing problem separately.

---

## 4. Options with Tradeoffs

### Option A: Make freeform scripts import and populate a ForwardResult directly

**Concept**: Freeform scripts compute physics their own way but pack final results into `costingfe.types.ForwardResult`, `costingfe.types.CostResult`, and `costingfe.types.PowerTable` dataclasses.

**What changes**:

- **Prompt template** (`model_setup_freeform.md`): Major rewrite. Must instruct the LLM to import `from costingfe.types import ForwardResult, CostResult, PowerTable` and construct these at the end of `compute()`. Must document all PowerTable fields (22 fields) and CostResult fields (22 fields) and explain which ones to set to 0.0 when not applicable.

- **Freeform scripts**: Each script's `compute()` method gains a final section that maps its dict outputs to ForwardResult fields. Roughly 40 lines of boilerplate per script.

- **Extractor**: Minimal change. The existing `extract_costingfe()` pathway works if `result` is a ForwardResult at module level. The extractor routing still needs to detect that the module has ForwardResult but no CostModel.

- **Server**: Cannot do live recomputation without a CostModel. Would need a lightweight adapter that wraps the freeform dataclass's `compute()` method in a forward()-like API. Significant work.

- **Existing costingfe concepts**: No change.

**Pros**:
- Exact structural compatibility with explorer extraction
- CAS22 detail "just works"
- Sensitivity analysis could use the existing `build_sensitivity_analysis()` path IF we also provide a CostModel-like wrapper (but this defeats the purpose)

**Cons**:
- Adds costingfe as a dependency for "dependency-free" freeform scripts (contradicts the freeform template's design principle)
- 22 PowerTable fields is a lot of boilerplate for concepts that only compute 6-8 power values
- Many PowerTable fields are MFE-specific (p_coils, p_cool, p_dec_waste) and meaningless for exotic concepts
- Sensitivity still can't use `model.sensitivity()` because there's no CostModel
- Prompt is much more complex; LLM error rate will increase

**Verdict**: Poor fit. The dependency-free principle of freeform scripts exists for a reason (exotic concepts that don't map to costingfe's physics layers). Forcing ForwardResult compliance adds friction without solving the sensitivity problem.

### Option B: Define a lighter-weight output protocol

**Concept**: Define a `ConceptResult` dict schema (or simple dataclass) that both costingfe ForwardResult and freeform scripts can produce. The extractor consumes this instead of ForwardResult directly.

**Proposed protocol** (a `to_explorer_dict()` function):

```python
def to_explorer_dict() -> dict:
    """Return structured data for the concept explorer.
    
    All monetary values in M$ (millions USD).
    All power values in MW.
    """
    return {
        "costs": {
            "cas10": float, "cas21": float, ..., "cas90": float,
            "cas71": float, "cas72": float,  # O&M sub-accounts
            "total_capital": float,  # M$
            "lcoe": float,          # $/MWh
            "overnight_cost": float, # $/kW
        },
        "power": {
            "p_fus": float,     # Fusion power [MW]
            "p_th": float,      # Total thermal [MW]
            "p_et": float,      # Gross electric [MW]
            "p_net": float,     # Net electric [MW]
            "q_sci": float,     # Scientific Q
            "q_eng": float,     # Engineering Q
            "capacity_factor": float,  # [0-1]
            "rec_frac": float,  # Recirculating fraction
        },
        "cas22_detail": {
            "C220101": float, ..., "C220700": float,
        },
        "params": {str: float},     # All tunable parameters
        "overridden": [str],        # CAS accounts with manual overrides
        "sensitivities": {          # Optional; null if not computed
            "engineering": {str: {"elasticity": float, "baseline": float}},
            "financial": {str: {"elasticity": float, "baseline": float}},
        },
    }
```

**What changes**:

- **Prompt template** (`model_setup_freeform.md`): Add a section requiring a `to_explorer_dict()` function at module level. Document the dict schema. The function maps the script's internal dicts to the protocol. ~30 lines of boilerplate per script (less than Option A because the power section is smaller).

- **Freeform scripts**: Add `to_explorer_dict()` that maps `compute()` output to the protocol. Also add module-level `params = MyDataclass()` and `results = params.compute()` so the function has data to work with.

- **Extractor**: `extract_standalone()` already looks for `to_explorer_dict()` (line 264). It calls it and validates via `CostModelData.model_validate(raw_dict)`. The `from_forward_result()` method already handles the dict shape tolerantly (missing keys → 0.0). Minimal additional work: just ensure the dict keys match what `from_forward_result()` expects, or add a second constructor `from_explorer_dict()` with the protocol's key names.

- **Server**: Live recomputation for freeform concepts requires a different approach. The server could look for a `recompute(overrides: dict) -> dict` function in the module instead of `model.forward()`. The freeform script would implement this as: create modified dataclass, call `.compute()`, return `to_explorer_dict()`. This is feasible but adds a second entry point to the module.

- **Existing costingfe concepts**: Add `to_explorer_dict()` as a thin wrapper around `dataclasses.asdict(result)` + renaming. Or keep the existing `extract_costingfe()` path and only use the protocol for standalone concepts.

**Pros**:
- No costingfe dependency in freeform scripts
- Protocol is small (8 power fields vs 22 in PowerTable)
- Existing standalone extraction path already supports `to_explorer_dict()`
- Sensitivity can be computed inside the freeform script using finite-difference and returned in the same format
- Costingfe concepts don't need to change (keep existing extraction path)

**Cons**:
- Two extraction paths remain (costingfe direct vs protocol dict)
- Protocol must be documented carefully so LLM generates it correctly
- Live recomputation needs a `recompute()` function (additional module-level API)
- Sensitivity computation in freeform scripts is approximate (finite-difference vs autodiff)

### Option C: Make freeform scripts wrap results in a costingfe CostModel

**Concept**: Create a `GenericCostModel` subclass or adapter in costingfe that accepts pre-computed CAS values instead of computing them from physics.

**Assessment**: This inverts the architecture. CostModel's value is its physics layers (power balance, geometry, cost scaling). A freeform script that already computes everything would be wrapping results in a CostModel just to get the output format. The CostModel's `forward()` would be a no-op that returns pre-populated values.

**Verdict**: Architecturally wrong. CostModel is a computation engine, not an output container. Rejected.

### Option D: Dual-path with shared output type (recommended hybrid)

**Concept**: Keep two extraction paths but have both produce the same `CostModelData` Pydantic model. For costingfe, continue using `from_forward_result()`. For freeform, use a new `from_freeform_result()` class method or the existing `to_explorer_dict()` protocol.

**What changes**:

- **Prompt template** (`model_setup_freeform.md`): Add requirement for:
  1. Module-level `params` and `results` variables (so extraction can access them)
  2. A `to_explorer_dict()` function that maps `compute()` output to a dict matching the `from_forward_result()` expected shape (lowercase cas keys, `"costs"` / `"power_table"` / `"cas22_detail"` structure)
  3. A `compute_sensitivity()` function that returns finite-difference elasticities in the `{"engineering": {...}, "financial": {...}}` format

- **Freeform scripts**: Add ~40-50 lines of boilerplate: `to_explorer_dict()` + `compute_sensitivity()` + module-level variables. The `compute_sensitivity()` function would:
  ```python
  def compute_sensitivity(params, base_results, sweep_params):
      base_lcoe = base_results["economics"]["lcoe_USD_per_MWh"]
      elasticities = {}
      for name in sweep_params:
          base_val = getattr(params, name)
          dp = base_val * 0.01  # 1% perturbation
          p_up = MyDataclass(**{**params.__dict__, name: base_val + dp})
          p_dn = MyDataclass(**{**params.__dict__, name: base_val - dp})
          lcoe_up = p_up.compute()["economics"]["lcoe_USD_per_MWh"]
          lcoe_dn = p_dn.compute()["economics"]["lcoe_USD_per_MWh"]
          dlcoe_dp = (lcoe_up - lcoe_dn) / (2 * dp)
          elasticities[name] = dlcoe_dp * base_val / base_lcoe
      return {"engineering": elasticities, "financial": {}}
  ```

- **Extractor**: The existing `extract_standalone()` already handles `to_explorer_dict()`. Add sensitivity extraction: if the module has `compute_sensitivity()`, call it and build a `SensitivityAnalysis`. Update `has_sensitivities=True`.

- **Server**: For live recomputation, look for a `recompute(overrides: dict) -> dict` function. Freeform scripts implement this as:
  ```python
  def recompute(overrides: dict) -> dict:
      p = MyDataclass(**{**params.__dict__, **overrides})
      return p.to_explorer_dict()  # or inline the mapping
  ```
  The server's `_compute_cached()` detects freeform modules and calls `recompute()` instead of `model.forward()`.

- **Existing costingfe concepts**: Zero changes. The costingfe extraction path is untouched.

**Pros**:
- Zero changes to existing costingfe concepts
- Freeform concepts get full explorer integration (cost breakdown, sensitivities, live recomputation)
- `to_explorer_dict()` protocol is already supported by the standalone pathway
- Sensitivity computation uses the same dimensionless elasticity format
- Clean separation: costingfe does its thing, freeform does its thing, explorer consumes one format

**Cons**:
- ~50 lines of boilerplate per freeform script
- Sensitivity is finite-difference (approximate), not autodiff (exact) -- but for first-pass models this is fine
- Need to update 4 existing freeform scripts to add the protocol functions
- Need to update prompt template for future freeform concepts
- Two code paths in the server (model.forward vs recompute)

---

## 5. Sensitivity Analysis

### Current state

| | costingfe | Freeform |
|---|----------|----------|
| Method | JAX autodiff (`jax.grad`) | Brute-force sweep at N discrete points |
| Output | Exact elasticities (dict of floats) | Raw LCOE values at each sweep point |
| Format | `{"engineering": {k: elast}, "financial": {k: elast}}` | `[{param_value, lcoe_cents_kWh, net_electric_MW}]` |
| Scope | All continuous params automatically | Manually selected 5-7 params |
| Speed | Single `jax.grad` call (~2x forward pass) | N forward passes per param (typically 5-7 points x 5-7 params = 25-49 evaluations) |

### Standardization approach

The explorer's `SensitivityAnalysis` model expects `{engineering: {k: SensitivityEntry}, financial: {k: SensitivityEntry}}` where each `SensitivityEntry` has `elasticity` (dimensionless) and `baseline` (parameter value).

For freeform scripts, central-difference elasticity is:

```
elasticity = (LCOE(p + dp) - LCOE(p - dp)) / (2 * dp) * (p / LCOE_base)
```

With `dp = 0.01 * p` (1% perturbation), this gives a numerical derivative accurate to ~O(dp^2) relative error. For parameters where the LCOE response is roughly linear over a few percent (which it is for most engineering parameters), this is indistinguishable from the autodiff result.

The sensitivity computation should:
1. Be implemented as a standalone function in the freeform script (not requiring costingfe)
2. Iterate over all numeric `@dataclass` fields (not just hand-picked sweep parameters)
3. Skip fields with value 0.0 or boolean/string type
4. Return the `{"engineering": {...}, "financial": {...}}` format directly
5. Classify `interest_rate` and `inflation_rate` as "financial"; everything else as "engineering"

### Parameter coverage

costingfe's `_engineering_keys()` returns a curated list of ~25-35 parameters per concept family. Freeform scripts have ~20-40 `@dataclass` fields. The sets overlap substantially (both include eta_th, p_cryo, availability, etc.) but freeform scripts have concept-specific parameters (e.g., `hts_coil_system_cost_M_USD`, `driver_rep_rate_Hz`) that don't exist in costingfe's parameter space. This is expected and desirable -- the explorer should show these concept-unique sensitivities.

### Accuracy comparison

For a typical freeform model with ~30 parameters:
- Finite-difference at 1% perturbation: 60 forward evaluations
- Each evaluation: ~1ms (simple Python arithmetic)
- Total: ~60ms per concept

This is fast enough to compute at extraction time. The elasticity values will differ from hypothetical JAX autodiff values by < 0.1% for smooth models, which is well within the uncertainty of the underlying physics parameters.

### Proposed `compute_sensitivity()` template

```python
def compute_sensitivity(
    params_instance,          # The @dataclass instance
    params_cls,               # The @dataclass class (for creating modified instances)
    lcoe_key: str = "lcoe_USD_per_MWh",
    financial_keys: set[str] = {"interest_rate", "inflation_rate"},
    dp_fraction: float = 0.01,
) -> dict:
    """Compute LCOE elasticities for all numeric parameters via central difference."""
    import dataclasses
    base = params_instance.compute()
    base_lcoe = base["economics"][lcoe_key]
    if base_lcoe <= 0:
        return {"engineering": {}, "financial": {}}
    
    engineering = {}
    financial = {}
    
    for f in dataclasses.fields(params_instance):
        val = getattr(params_instance, f.name)
        if not isinstance(val, (int, float)) or val == 0.0:
            continue
        
        dp = abs(val) * dp_fraction
        p_up = params_cls(**{**dataclasses.asdict(params_instance), f.name: val + dp})
        p_dn = params_cls(**{**dataclasses.asdict(params_instance), f.name: val - dp})
        lcoe_up = p_up.compute()["economics"][lcoe_key]
        lcoe_dn = p_dn.compute()["economics"][lcoe_key]
        
        dlcoe_dp = (lcoe_up - lcoe_dn) / (2 * dp)
        elasticity = dlcoe_dp * val / base_lcoe
        
        target = financial if f.name in financial_keys else engineering
        target[f.name] = {"elasticity": elasticity, "baseline": val}
    
    return {"engineering": engineering, "financial": financial}
```

This function is concept-agnostic and can be included in the freeform template as a utility. Each freeform script calls it with its own `@dataclass` class and instance.

---

## 6. Recommendation

**Option D (dual-path with shared output type)** is the recommended approach, implemented in two phases:

### Phase 1: Extraction routing fix (immediate)

Fix the extractor's branching logic so freeform scripts route to `extract_standalone()`. This unblocks extraction for concepts 12, 15, 22 with `cost_model=None`. No changes to freeform scripts needed.

### Phase 2: Freeform output protocol (this work item)

1. Update `model_setup_freeform.md` to prescribe `to_explorer_dict()`, `compute_sensitivity()`, and module-level `params`/`results` variables.
2. Update the 4 existing freeform scripts (02, 12, 15, 22) to add these functions.
3. Update `extract_standalone()` to call `compute_sensitivity()` if available and populate `SensitivityAnalysis`.
4. Update the server to support `recompute(overrides)` for freeform concepts.

Phase 1 is a P0 prerequisite (already specced). Phase 2 enables full cross-concept comparison including freeform concepts.

### Key file paths referenced

| File | Role |
|------|------|
| `/home/reid/1cfe/1costingfe/src/costingfe/types.py` (lines 79-147) | ForwardResult, PowerTable, CostResult definitions |
| `/home/reid/1cfe/1costingfe/src/costingfe/model.py` (lines 344-356, 779-814) | CostModel.forward() and .sensitivity() |
| `exploration/concept_explorer/models.py` (lines 111-298) | CostModelData, from_forward_result(), HeadlineEconomics |
| `exploration/concept_explorer/extract_explorer_data.py` (lines 132-219, 227-308) | extract_costingfe(), extract_standalone(), build_sensitivity_analysis() |
| `exploration/concept_explorer/server.py` (lines 75-163, 534-582) | _forward_with_overrides(), _compute_cached() |
| `exploration/concept_analysis/prompt_templates/model_setup_freeform.md` | Freeform prompt template |
| `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` | Costingfe prompt template |
| `exploration/concept_analysis/analyses/12-levitated-dipole/model_setup.py` | Freeform exemplar (levitated dipole) |
| `exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/iter-3/model_setup.py` | Freeform exemplar (z-pinch) |
| `exploration/concept_analysis/analyses/22-projectile-icf/iter-4/model_setup.py` | Freeform exemplar (projectile ICF) |
| `exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/model_setup.py` | Freeform exemplar (sonofusion) |
