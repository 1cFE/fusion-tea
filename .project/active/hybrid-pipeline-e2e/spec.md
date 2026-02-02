# Spec: Hybrid Pipeline End-to-End (Solar+Battery)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-02T05:55:03Z
**Complexity:** MEDIUM
**Branch:** visualization
**Epic:** End-to-End Pipeline De-Risking (replaces Items 4+5)

---

## Business Goals

### Why This Matters

The end-to-end pipeline de-risking epic has proven individual pieces work in isolation:
- Item 1: SysML model compiles and is AST-traversable
- Item 2: Codegen handles CalcUsage chains and TEAx executes them
- Item 3: `generate_costs.py` evaluates all component costs correctly

Nobody has proven these pieces work **together as an integrated pipeline**. The retired Items 4-5 would have injected pre-computed `total_capex` as a static entry point — that's not a pipeline test, it's answer injection. This item proves the real thing: `generate_costs.py` runs as a TEAx module, its output feeds codegen-generated system-level modules, and a verified LCOE comes out the other end.

### Success Criteria

- [ ] A single `execute_pipeline()` call produces LCOE from the solar+battery SysML model
- [ ] Component costs are computed dynamically (not static JSON injection)
- [ ] LCOE matches reference value ($288.68/MWh) within 1% tolerance
- [ ] The pipeline is reproducible: clone repo, run script, get LCOE

### Priority

P0 — only remaining item before the epic can close (Item 6 is a follow-on enhancement, not a blocker).

---

## Problem Statement

### Current State

- `generate_costs.py` computes component costs from SysML → outputs JSON
- Codegen generates TEAx modules from top-level CalcUsages → but never run on solar+battery
- TEAx executes pipelines → but no solar/fusion pipeline exists
- These three capabilities have never been wired together

### Desired Outcome

A working TEAx pipeline where:
1. A TEAx module wraps `compute_costs()` and dynamically evaluates component costs from the SysML model
2. Codegen-generated modules compute system-level LCOE calcs (energy production, O&M, fuel, financial, LCOE)
3. The pipeline wires them together: component costs → total_capex → system-level calcs → LCOE
4. Output is a verified LCOE value

---

## Scope

### In Scope

1. **Run codegen on solar+battery model** — generate system-level TEAx modules
2. **Fill in handwritten implementations** — 5 system-level calc implementations
3. **Create `ComponentCostEvaluator` TEAx module** — wraps `compute_costs()`
4. **Create pipeline YAML** — wires cost evaluator + system-level modules
5. **Create execution script** — runs the full pipeline
6. **Create verification script** — compares output against expected values
7. **Retire Item 4** from the epic (folded into this item)

### Out of Scope

- Enhancing codegen for nested CalcUsage discovery (Item 6)
- Extracting `generate_costs.py` into a reusable library
- Changes to the SysML model
- Changes to TEAx/simkit framework
- Changes to sysml-codegen itself
- CI/CD integration
- Multi-design comparison

### Edge Cases & Considerations

- Codegen may produce warnings about nested CalcUsages it can't see — this is expected and should be documented, not fixed
- `compute_costs()` loads the SysML model internally via `SysideAdapter` — the TEAx module needs the model path as input
- Pipeline YAML must wire `total_capex` from cost evaluator output to `AnnualizedFinancialCalc` input — this is the critical data flow
- The 5 handwritten implementations must match the PyFECONS formula structure (CRF-based LCOE with inflation escalation)

---

## Requirements

### Functional Requirements

> Requirements below are from user's request and epic context unless marked [INFERRED].

1. **FR-1**: Run `sysml-codegen generate` on `models/tests/solar_battery/` and produce TEAx modules for the 5 system-level CalcUsages (EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc, AnnualizedFinancialCalc, LCOECalc)

2. **FR-2**: Fill in handwritten implementations for all 5 generated module stencils with correct formulas:
   - `energy_production_impl.py`: `annual_energy_mwh = 8760 * p_net_mw * n_mod * plant_availability`
   - `annualized_om_impl.py`: `annual_om_cost = om_rate_per_kw_year * p_net_kw`
   - `annualized_fuel_impl.py`: `annual_fuel_cost = fuel_unit_cost * fuel_consumption`
   - `annualized_financial_impl.py`: CRF = `r*(1+r)^n / ((1+r)^n - 1)`; `annualized_capital_cost = CRF * total_capex`
   - `lcoe_impl.py`: `lcoe = (C900000 + (C700000 + C800000) * (1+inflation)^lifetime) / annual_energy_mwh`

3. **FR-3**: Create a `ComponentCostEvaluator` TEAx module (`ModuleBase` subclass) that:
   - Takes SysML model path as input (from entry point or configuration)
   - Internally calls `compute_costs()` from `generate_costs.py`
   - Outputs `total_capex` and per-subsystem cost breakdown as Pydantic model
   - Outputs design parameters (`p_net_mw`, `plant_availability`, `discount_rate`, etc.)

4. **FR-4**: Create a pipeline YAML that wires:
   - Entry point → ComponentCostEvaluator → system-level modules → exit point
   - `total_capex` from cost evaluator feeds into `AnnualizedFinancialCalc`
   - Design parameters from cost evaluator feed into all system-level modules
   - Inter-module chaining: LCOECalc consumes outputs from the other 4 system-level calcs
   - Exit point captures `lcoe_per_mwh` and cost breakdown

5. **FR-5**: Create an execution script that runs the full pipeline with a single command

6. **FR-6**: Create a verification script that compares pipeline output against `expected_system_outputs.csv` values (within 1% tolerance)

7. **FR-7**: [INFERRED] Generated codegen tests MUST pass before pipeline execution

### Non-Functional Requirements

- Pipeline execution MUST be reproducible from a clean state (no manual steps beyond running the script)
- All new code MUST use `uv run` for Python execution per project conventions

---

## Acceptance Criteria

### Core Functionality

- [ ] `sysml-codegen generate` completes without errors on solar+battery model
- [ ] 5 system-level modules generated with correct structure
- [ ] 5 handwritten implementations filled in with correct formulas
- [ ] `ComponentCostEvaluator` module wraps `compute_costs()` and produces correct output
- [ ] Pipeline YAML correctly wires cost evaluator → system-level modules → LCOE
- [ ] `execute_pipeline()` completes without errors
- [ ] LCOE output matches $288.68/MWh within 1% tolerance
- [ ] `total_capex` in pipeline matches $41,205.00 from `generate_costs.py`
- [ ] Verification script reports PASS

### Quality & Integration

- [ ] Existing tests continue to pass (`generate_costs.py` tests, codegen tests)
- [ ] Generated codegen tests pass
- [ ] Pipeline is runnable from a single script invocation
- [ ] Failure modes produce clear error messages (not silent wrong answers)

---

## Key Design Decisions (for design phase)

These decisions should be resolved during `/_my_design`:

1. **How does the cost evaluator module receive the SysML model path?**
   - Option A: Entry point JSON with model path
   - Option B: Environment variable or configuration
   - Option C: Hardcoded relative path (simplest for test)

2. **How are design parameters passed to system-level modules?**
   - Option A: Cost evaluator outputs them alongside total_capex (single source)
   - Option B: Separate entry point JSON for design params (codegen-generated `design_params.json`)
   - Option C: Cost evaluator outputs total_capex; design params come from codegen's entry point extraction

3. **Where does the generated code live?**
   - Option A: `generated/solar_battery/` (alongside chain spike)
   - Option B: Under `models/tests/solar_battery/generated/`

4. **How to handle codegen's pipeline YAML vs the actual pipeline YAML?**
   - Codegen generates a pipeline YAML for the 5 system-level calcs it can see
   - The actual pipeline needs the cost evaluator module added
   - Option A: Post-process codegen's YAML to add cost evaluator
   - Option B: Write the pipeline YAML manually (it's ~30 lines)
   - Option C: Generate base YAML, then merge/extend

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Items 4+5, revised)
- **Research:** `.project/research/20260202-055244_hybrid-vs-native-codegen-feasibility.md`
- **SysML Model:** `models/tests/solar_battery/library.sysml`, `design.sysml`
- **Reference Implementation:** `models/tests/solar_battery/generate_costs.py`
- **Expected Values:** `models/tests/solar_battery/expected_system_outputs.csv`
- **Chain Spike Reference:** `generated/codegen_chain_spike/` (proven codegen → TEAx pattern)
- **Design:** `.project/active/hybrid-pipeline-e2e/design.md` (to be created)

---

## Verification Values

From `expected_system_outputs.csv` and `generate_costs.py` output:

| Metric | Expected Value | Tolerance |
|--------|---------------|-----------|
| total_capex | $41,205.00 | exact (from generate_costs.py) |
| annual_energy_mwh | 11.14272 MWh | 1% |
| annual_om_cost | $160.00 | 1% |
| annual_fuel_cost | $0.00 | exact |
| capital_recovery_factor | 0.070952 | 1% |
| annualized_capital_cost | $2,923.60 | 1% |
| lcoe_per_mwh | $288.68/MWh | 1% |

---

**Next Steps:** After approval, proceed to `/_my_design`
