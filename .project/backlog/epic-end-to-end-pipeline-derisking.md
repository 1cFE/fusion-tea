# Epic: End-to-End Pipeline De-Risking (Solar+Battery)

**Status**: DRAFT
**Priority**: P0 (blocking full cost modeling pipeline)
**Created**: 2026-01-30
**Owner**: Reid

---

## Executive Summary

Prove the full pipeline — SysML model → sysml-codegen → TEAx execution → LCOE output — works end-to-end using a solar+battery toy-plus system. The coffee maker epic (Stages 1–3) proved the SysML cost pattern is valid and evaluable. This epic closes the remaining gap: codegen and TEAx execution.

**End state**: A solar+battery SysML model produces a verified LCOE value ($/MWh) through the automated pipeline, with all intermediate values traceable back to the model.

---

## Context

### What's Been Proven (Coffee Maker Epic)

| Capability | Status | Evidence |
|------------|--------|----------|
| Nested cost pattern compiles | PROVEN | `syside check` passes on coffee maker |
| Pattern is AST-traversable | PROVEN | `validate_ast.py` finds all 7 calcs, bindings, multiplicity |
| Pattern is evaluable | PROVEN | `generate_costs.py` matches expected CSV (7/7 tests) |
| Output format works | PROVEN | 14-column CSV approved, visualization POC uses it (33/33 tests) |

### What's NOT Been Proven

| Capability | Status | Gap |
|------------|--------|-----|
| Codegen handles nested CalcUsages | NOT PROVEN | Codegen finds top-level CalcUsages only; embedded `cost_model` in PartDefs invisible |
| Codegen extracts a CalcUsage DAG (inter-calc dependencies) | PROVEN (Item 2) | 3-calc chain spike: correct extraction, wiring, ordering, and runtime execution |
| Codegen generates correct TEAx modules | NOT PROVEN | Never run on a cost model |
| TEAx executes generated cost pipeline | NOT PROVEN | Battery demo works but no SysML-derived pipeline tested |
| LCOE comes out the other end | NOT PROVEN | No end-to-end test exists |

### Why Solar+Battery?

The coffee maker is useful for cost pattern validation but has no energy production, no LCOE, and no direct mapping to fusion concepts. A solar+battery system:

- **Has LCOE** — the core metric for fusion TEA
- **Has the same cost structure** — component costs → subsystem rollup → total CAPEX → LCOE
- **Has performance modeling** — energy production depends on system parameters
- **Maps to fusion** — solar array ≈ reactor core, battery ≈ energy storage, site infrastructure ≈ balance of plant
- **Has known realistic values** — easy to verify outputs against industry benchmarks

---

## System Design: Solar+Battery Plant

### Hierarchy (3 levels, 9 leaf parts)

```
Solar Battery Plant (assembly, L0) ─── LCOE rollup
├── Solar Array (assembly, L1) ─── cost rollup
│   ├── PV Module [20] (leaf, L2) ─── 400W panels, arrayed
│   ├── String Inverter [4] (leaf, L2) ─── 2kW micro-inverters, arrayed
│   └── Array BOS (leaf, L2) ─── wiring, combiner boxes, fuses
├── Battery System (assembly, L1) ─── cost rollup
│   ├── Battery Pack [8] (leaf, L2) ─── 5kWh LFP packs, arrayed
│   ├── Hybrid Inverter (leaf, L2) ─── 10kW bidirectional
│   └── Battery BOS (leaf, L2) ─── BMS, safety disconnects, wiring
└── Site Infrastructure (assembly, L1) ─── cost rollup
    ├── Racking & Mounting (leaf, L2) ─── ground-mount system
    ├── Electrical Panel (leaf, L2) ─── main panel, disconnects
    └── Permitting & Interconnect (leaf, L2) ─── soft costs
```

### Calculation Definitions (~15 calc defs)

**Component Cost Calcs** (9, nested in PartDefs — Pattern A):

| Calc Def | Key Inputs | Key Outputs |
|----------|-----------|-------------|
| PVModuleCostCalc | wattage, efficiency | material_cost, fab_cost, install_cost, total_cost |
| InverterCostCalc | power_rating | material_cost, fab_cost, install_cost, total_cost |
| ArrayBOSCostCalc | string_count, panel_count | material_cost, fab_cost, install_cost, total_cost |
| BatteryPackCostCalc | capacity_kwh, chemistry_factor | material_cost, fab_cost, install_cost, total_cost |
| HybridInverterCostCalc | power_rating, bidirectional | material_cost, fab_cost, install_cost, total_cost |
| BatteryBOSCostCalc | pack_count | material_cost, fab_cost, install_cost, total_cost |
| RackingCostCalc | panel_count, tilt_angle | material_cost, fab_cost, install_cost, total_cost |
| ElectricalPanelCostCalc | circuit_count | material_cost, fab_cost, install_cost, total_cost |
| PermittingCostCalc | system_capacity_kw | total_cost (soft cost, no material/fab split) |

**Assembly Allocation Calc** (1):

| Calc Def | Purpose |
|----------|---------|
| AllocationCostCalc | Assembly-level minor items (fasteners, labels, conduit) |

**System-Level Calcs** (5, explicit CalcUsages in design — visible to codegen today):

These are aligned with the PyFECONS LCOE structure so that the solar test exercises the same calc def pattern that fusion will use. The solar model is a lightweight instance of the fusion LCOE formula, not a separate formulation.

| Calc Def | PyFECONS Analog | Key Inputs | Key Outputs |
|----------|----------------|-----------|-------------|
| EnergyProductionCalc | LCOE denominator | p_net_mw, n_mod, plant_availability | annual_energy_mwh (= 8760 × p_net × n_mod × availability) |
| AnnualizedOMCalc | CAS70 (C700000) | om_rate_per_kw_year, p_net_kw | annual_om_cost |
| AnnualizedFuelCalc | CAS80 (C800000) | fuel_unit_cost, fuel_consumption | annual_fuel_cost (= 0 for solar; placeholder for pipeline wiring) |
| AnnualizedFinancialCalc | CAS90 (C900000) | total_capex, discount_rate, plant_lifetime | capital_recovery_factor, annualized_capital_cost (= CRF × total_capex) |
| LCOECalc | C1000000 | annualized_capital_cost, annual_om_cost, annual_fuel_cost, yearly_inflation, plant_lifetime, annual_energy_mwh | lcoe_per_mwh (= (C900000 + (C700000 + C800000) × (1+inflation)^lifetime) / annual_energy) |

**Design decision**: The LCOE formula uses the PyFECONS structure rather than a simplified CRF-based formula. For solar, `annual_fuel_cost = 0` and `yearly_inflation` is set to a realistic value (0.0245). This means the solar test exercises the full 3-term numerator with inflation escalation, proving the wiring that fusion will need. The only difference for fusion will be non-zero fuel costs and different parameter sources.

### Target Values

For a residential 8kW solar + 40kWh battery system in a moderate-irradiance location:

| Parameter | Value | Notes |
|-----------|-------|-------|
| p_net | 0.008 MW | 8 kW system capacity |
| n_mod | 1 | Single installation |
| plant_availability | ~0.159 | Effective CF: (4.5 sun-hours / 24) × 0.85 PR |
| plant_lifetime | 25 years | Standard solar warranty period |
| discount_rate | 0.05 | 5% real discount rate |
| yearly_inflation | 0.0245 | BLS long-run average |
| om_rate | 20 $/kW-year | Residential solar O&M |
| fuel_cost | 0 | No fuel for solar (placeholder) |

| Metric | Sanity-Check Range | Notes |
|--------|-------------------|-------|
| Total CAPEX | $35k–$45k | Solar ~$20k, battery ~$16k, site ~$4k |
| Annual energy | 10,000–12,000 kWh | 8760 × 0.008 × 1 × ~0.159 ≈ 11,140 kWh |
| Annual O&M | $150–$200 | 20 $/kW-yr × 8 kW = $160 |
| LCOE | $0.15–$0.35/kWh | Wide range due to battery cost weight |

**Important**: The sanity-check ranges above are for gross-error detection only. The actual verification target is the exact LCOE value hand-calculated from chosen model parameters, verified to **1% tolerance**. Item 1 produces `expected_output.csv` with these exact values.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        End-to-End Pipeline                              │
│                                                                         │
│  1. SysML Model (models/tests/solar_battery/)                          │
│     ├── library.sysml     ─── CalcDefs + PartDefs with nested costs    │
│     └── design.sysml      ─── Design instance + system-level CalcUsages│
│              │                                                          │
│  ┌───────────┼───────────────────────┐                                  │
│  │           │                       │                                  │
│  ▼           ▼                       ▼                                  │
│  3a. generate_costs.py    3b/4. sysml-codegen                          │
│  (component costs)        (system-level calcs)                          │
│       │                        │                                        │
│       │ component_costs.json   │ Generated modules:                     │
│       │ (CAPEX breakdown)      │  ├── energy_production/               │
│       │                        │  ├── annualized_om/                   │
│       │                        │  ├── annualized_fuel/                 │
│       │                        │  ├── annualized_financial/            │
│       │                        │  └── lcoe/                            │
│       │                        │                                        │
│       └────────┬───────────────┘                                        │
│                │                                                        │
│                ▼                                                        │
│  5. TEAx Pipeline (solar_battery_pipeline.yaml)                        │
│     ├── EntryPoint: component_costs.json + design_params.json          │
│     ├── Module: EnergyProductionCalc → annual_energy_mwh               │
│     ├── Module: AnnualizedOMCalc → C700000                             │
│     ├── Module: AnnualizedFuelCalc → C800000 (= 0)                    │
│     ├── Module: AnnualizedFinancialCalc → C900000                      │
│     ├── Module: LCOECalc → lcoe_per_mwh                               │
│     └── ExitPoint: lcoe_result.json, cost_breakdown.json               │
│                │                                                        │
│                ▼                                                        │
│  Verification                                                           │
│     └── lcoe_result.lcoe_per_mwh ≈ expected_lcoe (within 1%)          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Design Decision: Hybrid Pipeline

Component cost calcs (nested in PartDefs) are **not visible to codegen today**. Rather than block on a large codegen enhancement, we use a hybrid approach:

- **Component costs** → evaluated by `generate_costs.py` → output as JSON entry point
- **System-level calcs** → extracted by codegen → generated as TEAx modules
- **TEAx pipeline** → wires entry point data + generated modules → produces LCOE

This proves:
1. The SysML model is complete and correct
2. Codegen works for the calcs it can see
3. TEAx executes correctly end-to-end
4. The LCOE value matches expectations

The codegen gap for nested CalcUsages is documented and scoped as a separate enhancement (Item 6), which when complete would eliminate the generate_costs.py step entirely.

### Key Design Decision: PyFECONS-Aligned LCOE Formula

The solar model uses the PyFECONS LCOE formula structure rather than a simplified CRF-based formula. This is a deliberate choice:

- **Pro**: The pipeline test exercises the exact formula structure fusion will use
- **Pro**: The 3-term numerator with inflation escalation is tested (even though fuel = 0)
- **Pro**: No throwaway calc defs — the solar LCOECalc is an instance of the fusion pattern
- **Con**: Solar LCOE values will differ slightly from typical solar LCOE calculators (which don't use inflation escalation)

The solar model's `annual_fuel_cost = 0` is a realistic value (solar has no fuel), not a hack. It exercises the wiring while producing correct results.

---

## Success Criteria

- [ ] Solar+battery SysML model compiles (`syside check` passes)
- [ ] Model has 3 hierarchy levels, 9 leaf parts, 3 assemblies, ~15 calc defs
- [x] Codegen spike confirms CalcUsage-chain extraction works (Item 2)
- [x] `generate_costs.py` evaluates all component costs correctly (matches expected CSV)
- [ ] `sysml-codegen` generates TEAx modules for system-level calcs (5 modules)
- [ ] Handwritten implementations filled in and passing generated tests
- [ ] TEAx pipeline executes without errors
- [ ] LCOE matches hand-calculated value from model parameters (within 1% tolerance)
- [ ] End-to-end documented: SysML → codegen → TEAx → LCOE

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ~~Codegen can't resolve inter-CalcUsage dependencies (DAG wiring)~~ | ~~Medium~~ | ~~High~~ | **RETIRED** — Item 2 spike confirmed DAG wiring works end-to-end |
| Codegen produces incorrect module structure | Medium | High | Run on solar model early; fix issues iteratively |
| TEAx registry integration unclear | Medium | Medium | Battery demo is reference pattern; follow exactly |
| Pipeline YAML wiring errors | Medium | Low | TEAx validator catches type mismatches |
| generate_costs.py approach doesn't scale | Low | Low | Goal is shared library; this epic is the first consumer |
| SysML model too simple to stress-test | Low | Medium | 9 leaves + 3 assemblies + multiplicity is substantial |

---

## Backlog Items

### Item 1: Solar+Battery SysML Model ✅ COMPLETE

**Type**: Modeling

**Objective**: Create a solar+battery SysML model with nested cost patterns and PyFECONS-aligned system-level LCOE calculations that compiles and is AST-traversable.

**Current State**:
- ✅ Coffee maker model exists as reference pattern
- ✅ `'Costed Component'` interface exists in `models/library/foundation/costing.sysml`
- ✅ Pattern A (nested cost models) proven in coffee maker
- ✅ Solar+battery model complete (library.sysml + design.sysml)
- ✅ validate_ast.py passes all 5 FR checks (FR-13 through FR-17)
- ✅ Expected outputs computed (expected_output.csv + expected_system_outputs.csv)

**Scope**:
1. **`models/tests/solar_battery/library.sysml`** (~550–650 lines):
   - 9 component cost CalcDefs (PVModuleCostCalc, BatteryPackCostCalc, etc.)
   - 1 AllocationCostCalc for assembly-level items
   - 5 system-level CalcDefs aligned with PyFECONS (EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc, AnnualizedFinancialCalc, LCOECalc)
   - 9 leaf PartDefs with embedded `cost_model` calc usages
   - 3 assembly PartDefs with `sum()` rollup
   - 1 top-level `'Solar Battery Plant'` PartDef
2. **`models/tests/solar_battery/design.sysml`** (~100–120 lines):
   - Concrete plant instance with parameter bindings via `:>>`
   - Multiplicity: PV modules [20], inverters [4], battery packs [8]
   - System-level CalcUsages (5 calcs) as explicit top-level usages
   - Operating parameters: plant_lifetime, plant_availability, n_mod, yearly_inflation
   - Financial parameters: discount_rate, om_rate_per_kw_year
   - Fuel parameters: fuel_unit_cost = 0, fuel_consumption = 0
3. **`models/tests/solar_battery/validate_ast.py`** (~300 lines):
   - Discover all 9+1 cost models
   - Trace parameter bindings through redefinition chains
   - Detect multiplicity on arrayed parts
   - Verify system-level calc usages are visible at design level
   - Verify inter-calc dependencies (LCOECalc inputs trace to other calc outputs)
4. **`models/tests/solar_battery/expected_output.csv`**:
   - Hand-calculated cost breakdown for all parts
   - LCOE calculation using PyFECONS formula with exact parameter values
   - **This is the verification target** — all downstream items validate against these exact values

**Out of Scope**:
- Degradation modeling beyond simple annual rate
- Time-of-use or dynamic pricing
- Battery cycling or dispatch optimization

**Success Criteria**:
- [x] `uv run syside check models/tests/solar_battery/` exits 0
- [x] `validate_ast.py` finds all 10 cost models (9 leaf + 1 allocation) and 5 system calcs
- [x] `validate_ast.py` detects multiplicity on 3 arrayed parts
- [x] `expected_output.csv` computed from exact parameters (LCOE $0.289/kWh within sanity range)
- [x] System-level CalcUsages are at design level (not nested in PartDefs)
- [x] LCOECalc uses PyFECONS formula structure with 3-term numerator

**Dependencies**: None (coffee maker and costing interface exist as references)

**Deliverables**:
- `models/tests/solar_battery/library.sysml`
- `models/tests/solar_battery/design.sysml`
- `models/tests/solar_battery/validate_ast.py`
- `models/tests/solar_battery/expected_output.csv`

---

### Item 2: Codegen CalcUsage-Chain Spike ✅ COMPLETE

**Type**: Spike / Risk Reduction

**Objective**: Verify that sysml-codegen correctly extracts a DAG of CalcUsages where one calc's output feeds as input to another calc, and generates correct pipeline YAML with proper module ordering and data wiring.

**Rationale**: The 5 system-level calcs form a dependency chain:

```
EnergyProductionCalc → annual_energy_mwh ──────┐
AnnualizedOMCalc → annual_om_cost ──────────────┤
AnnualizedFuelCalc → annual_fuel_cost ──────────┤
AnnualizedFinancialCalc → annualized_capital ───┤
                                                ▼
                                          LCOECalc → lcoe_per_mwh
```

If codegen can't resolve these inter-calc dependencies — recognizing that LCOECalc's `annual_energy_mwh` input binds to EnergyProductionCalc's output — then Items 4 and 5 will require significant unplanned work. This spike answers that question cheaply before investing in the full model pipeline.

**Current State**:
- ✅ Codegen works for independent top-level CalcUsages
- ✅ Codegen resolves calc-to-calc data flow (3-calc chain verified)
- ✅ Generated pipeline YAML orders modules correctly for a DAG
- ✅ End-to-end pipeline execution produces correct results with zero manual workarounds

**Scope**:
1. **Create minimal test model** (`models/tests/codegen_chain_spike/`):
   - 2–3 CalcDefs where Calc B takes Calc A's output as input
   - Explicit top-level CalcUsages in a design file
   - ~30–50 lines of SysML total
2. **Run codegen on the test model**:
   ```bash
   uv run sysml-codegen generate \
     --models models/tests/codegen_chain_spike \
     --output generated/codegen_chain_spike \
     --package-name chain_spike
   ```
3. **Evaluate results**:
   - Does codegen discover both CalcUsages?
   - Does the pipeline YAML wire Calc A's output to Calc B's input?
   - Is module ordering correct (A before B)?
4. **Document findings**:
   - If it works: note as confirmed, proceed with Items 3–5 as planned
   - If it doesn't: document the gap, estimate fix scope, and decide whether to fix in codegen or work around manually in Item 4

**Out of Scope**:
- Cost patterns or nested CalcUsages (tested separately in Item 6)
- Full solar+battery model (that's Item 1)
- Filling in handwritten implementations (just need codegen output structure)

**Success Criteria**:
- [x] Minimal chain model compiles (`syside check` passes)
- [x] Codegen discovers all CalcUsages in the chain
- [x] Generated pipeline YAML has correct inter-module data wiring
- [x] Go/no-go decision documented for Items 4–5

**Go/No-Go Decision**: **GO.** CalcUsage-chain extraction, pipeline ordering, and end-to-end execution all work. Items 4–5 can proceed as planned.

**Dependencies**: None (uses a standalone minimal model, not the solar+battery model)

**Deliverables**:
- `models/tests/codegen_chain_spike/` — minimal test model
- `generated/codegen_chain_spike/` — codegen output
- Spike findings document (pass/fail + any issues found)

**Issues Encountered & Resolved**:

The initial spike (structural evaluation) passed all 4 stages. However, when attempting to **execute** the generated pipeline at runtime, 3 gaps were discovered:

| Gap | Issue | Root Cause | Fix |
|-----|-------|-----------|-----|
| 1 | `design_params.json` generated empty | Path filter default `"models/designs"` excluded test models | Changed default to `""` (accept all) in `sysml-codegen` |
| 2 | `RootModel[float]` exit point type had no output handler | Exit point types not included in `CUSTOM_SCHEMA_TYPES` | Codegen now generates `primitives.py` with `Float = RootModel[float]` and includes it in `CUSTOM_SCHEMA_TYPES` |
| 3 | Static `FusionParams` template copied into every package | Unconditional `shutil.copy` of hardcoded template | Removed the unconditional copy |

All 3 gaps were fixed in upstream commits:
- `sysml-codegen` commit `61aa907` (Fix three codegen runtime gaps)
- `agentic-mbse` commit `7413072` (L8 extractability validation)

**Verification**: After fixes, `execute_pipeline()` on freshly-regenerated output produced correct results (`area=50.0`, `total_cost=600.0`, `cost_per_area=12.0`) with zero manual workarounds (Attempt 1 in `plan_revisit.md`).

**Reports**:
- `.project/reports/codegen-runtime-gaps-2026-02-01-2047.md` — Gap analysis with root causes and reproduction steps
- `.project/active/gap1-default-value-debug/findings.md` — Deep diagnostic of the path filter root cause (4 scripts, delta-by-delta analysis)
- `.project/active/gap1-default-value-debug/fix-plan.md` — 5-change fix plan with prioritization
- `.project/active/codegen-chain-spike/plan.md` — Original spike plan (structural evaluation)
- `.project/active/codegen-chain-spike/plan_revisit.md` — Fix verification plan (runtime evaluation)

**Operational Notes**:
- Regeneration overwrites handwritten implementations. Use `--preserve-handwritten` flag to avoid this.
- Pipeline filename is now `pipeline.yaml` (not `{package_name}_pipeline.yaml`).
- Package symlink still needed: `ln -sfn codegen_chain_spike generated/chain_spike` for imports.

---

### Item 3: Cost Evaluation & Entry Point Generation ✅ COMPLETE

**Type**: Implementation

**Objective**: Evaluate all component costs from the SysML model and generate the JSON entry point files that TEAx will consume.

**Current State**:
- ✅ `generate_costs.py` pattern proven in coffee maker (1631 lines, 7/7 tests)
- ✅ `compute_costs()` API exists and is importable
- ✅ Solar+battery `generate_costs.py` adapted from coffee maker (10/10 tests)
- ✅ `component_costs.json` and `design_params.json` generated
- ✅ System-level LCOE verification passes ($288.68/MWh within 1%)

**Scope**:
1. **`models/tests/solar_battery/generate_costs.py`**:
   - Reuse patterns from coffee maker's generate_costs.py
   - Goal: extract shared logic into a reusable library where feasible
   - Extract calc defs, resolve bindings, evaluate formulas
   - Handle multiplicity (PV[20], inverter[4], battery[8])
   - Aggregate assembly rollups + allocation
   - Output `actual_output.csv` in same 14-column schema
   - Compare with `expected_output.csv`
2. **`models/tests/solar_battery/component_costs.json`**:
   - Pydantic-compatible JSON with total CAPEX broken down by subsystem
   - Format matches what TEAx EntryPoint expects
3. **`models/tests/solar_battery/design_params.json`**:
   - System-level parameters for PyFECONS-aligned LCOE calcs
   - p_net_mw, n_mod, plant_availability, plant_lifetime
   - discount_rate, yearly_inflation
   - om_rate_per_kw_year, p_net_kw
   - fuel_unit_cost = 0, fuel_consumption = 0
4. **`models/tests/solar_battery/test_generate_costs.py`**:
   - Tests matching coffee maker pattern (8–10 tests)
   - Verify CAPEX total, individual component costs, LCOE

**Out of Scope**:
- Changes to agentic-mbse

**Success Criteria**:
- [x] `generate_costs.py` runs without errors
- [x] `actual_output.csv` matches `expected_output.csv` within tolerance (1e-6)
- [x] `component_costs.json` and `design_params.json` generated
- [x] All tests pass (10/10)
- [x] CAPEX total within sanity-check range ($35k–$45k) — $41,205.00
- [x] Computed LCOE matches `expected_output.csv` value (within 1%) — $288.68/MWh

**Dependencies**: Item 1 (SysML model)

**Deliverables**:
- `models/tests/solar_battery/generate_costs.py`
- `models/tests/solar_battery/test_generate_costs.py`
- `models/tests/solar_battery/actual_output.csv`
- `models/tests/solar_battery/component_costs.json`
- `models/tests/solar_battery/design_params.json`

---

### Item 4: Codegen Pipeline Run — DEPRECATED

**Status**: DEPRECATED — folded into Item 5 (Hybrid Pipeline End-to-End)

**Reason**: The original scope (run codegen, fill implementations, run tests) was incorporated as Phases 1-3 of the revised Item 5. Keeping them as separate items created an artificial boundary — codegen output is only useful once wired into a pipeline, and the pipeline can't be tested without filled implementations. The hybrid pipeline spec (`.project/active/hybrid-pipeline-e2e/spec.md`) subsumes this item's full scope.

**What was delivered (via Item 5)**:
- ✅ Codegen run on solar+battery model (15 modules generated, 5 system-level)
- ✅ 5 handwritten implementations filled with correct formulas
- ✅ All codegen-generated tests pass (15/15)
- ✅ Formula verification tests pass (5/5)

---

### Item 5: Hybrid Pipeline End-to-End ✅ COMPLETE (revised — absorbs Item 4)

**Type**: Implementation / Integration / Validation

**Objective**: Prove the full hybrid pipeline — `generate_costs.py` as a TEAx module + codegen-generated system-level modules — produces a verified LCOE from a single `execute_pipeline()` call. Component costs are computed dynamically, not injected as static JSON.

**Revision Note**: This item was revised to absorb the original Item 4 (codegen pipeline run) and replace the original Item 5 (static entry point injection). The original Items 4-5 had an artificial boundary and the original Item 5's approach of injecting pre-computed `total_capex` as a static entry point was answer injection, not a pipeline test. See `.project/active/hybrid-pipeline-e2e/spec.md` for the full spec.

**Current State**:
- ✅ All phases complete (5/5)
- ✅ All tests pass: 28 pipeline tests + 10 regression tests
- ✅ Verification script confirms all 7 metrics within tolerance
- ✅ Pipeline is reproducible from clean state

**What Was Delivered**:

1. **Codegen on solar+battery** (Phase 1):
   - 15 modules generated (5 system-level + 10 component-level)
   - Namespace: `solarbatterylibrary`
   - AnnualizedFinancialCalc multi-output handled correctly by codegen

2. **ComponentCostEvaluator module** (Phase 2):
   - Hand-written TEAx module wrapping `compute_costs()` via importlib
   - Dynamically computes `total_capex` + reads design params from JSON
   - MultiOutput with 11 `Float` channels

3. **Handwritten implementations** (Phase 3):
   - 5 system-level calc implementations with correct PyFECONS-aligned formulas
   - Formula verification tests against known values

4. **Pipeline integration** (Phase 4):
   - Hand-crafted pipeline YAML wiring cost evaluator → 5 system-level modules → exit point
   - Registry updated with ComponentCostEvaluator + custom schemas
   - Execution script with absolute path resolution

5. **Verification** (Phase 5):
   - Verification script checking all 7 metrics against expected values
   - Handles hash-suffixed output directories and both RootModel serialization formats

**Key Design Decisions**:
- **DD-6 resolution**: CostEvaluatorResult uses MultiOutput (not BaseModel) — pipeline validator rejected single-output BaseModel approach
- **AnnualizedFinancialCalcOutput**: Fields changed from `float` to `Float` (RootModel[float]) for exit point serialization
- **importlib**: Added `sys.modules` registration to fix PEP 563 string annotation resolution

**Success Criteria**:
- [x] Single `execute_pipeline()` call produces LCOE from solar+battery SysML model
- [x] Component costs computed dynamically (not static JSON injection)
- [x] LCOE matches $288.68/MWh within 1% tolerance
- [x] Pipeline reproducible from clean state
- [x] `total_capex` = $41,205.00 (exact)
- [x] All existing tests pass (no regressions)
- [x] Verification script reports PASS

**Dependencies**: Item 1 (SysML model), Item 2 (spike confirms codegen chain handling), Item 3 (generate_costs.py + expected values)

**Deliverables**:
- `generated/solar_battery/` — full pipeline package
- `.project/active/hybrid-pipeline-e2e/` — spec, design, plan documents

**Detailed Docs**: `.project/active/hybrid-pipeline-e2e/spec.md`, `design.md`, `plan.md`

---

### Item 6: Codegen Enhancement — Nested CalcUsage Discovery

**Type**: Code/Implementation

**Objective**: Enhance sysml-codegen to discover CalcUsages embedded in PartDefinitions, synthesize per-PartUsage instances with resolved bindings, and generate TEAx modules for component costs — eliminating the need for the `generate_costs.py` workaround.

**Current State**:
- ✅ Codegen extraction pipeline exists (extractor.py, usage_extractor.py)
- ✅ Binding resolution works for top-level CalcUsages
- ✅ `generate_costs.py` proves the pattern is evaluable (the algorithm exists)
- ❌ `extract_calculation_usages()` only finds top-level CalcUsages
- ❌ No mechanism to discover CalcUsages inside PartDefinitions
- ❌ No per-PartUsage instantiation of embedded CalcUsages
- ❌ No binding resolution through `:>>` redefinition chains in design files

**Scope**:
1. **Enhance extraction** (`usage_extractor.py`):
   - When processing PartUsages, check if their PartDefinition contains CalcUsages
   - For each discovered embedded CalcUsage, create a synthetic `CalcUsageData`
   - Generate unique qualified names: `{PartUsageQN}__{CalcUsageName}`
   - Handle arrayed parts: one synthetic CalcUsage per unique PartUsage (not per array element)
2. **Enhance binding resolution** (`dependency_backtracker.py`):
   - Resolve CalcUsage input bindings that reference parent PartDef attributes
   - Trace `:>>` redefinitions from design file to get concrete values
   - Support binding chain: design `:>>` → part attribute → calc input
3. **Re-run codegen on solar+battery**:
   - Verify all 13 component cost CalcUsages are now discovered
   - Verify generated modules have correct bindings
   - Component costs should now be TEAx modules (not entry point JSON)
4. **Update pipeline YAML**:
   - Component cost modules feed into CAPEX rollup
   - Entry points reduced to design parameters only (no more component_costs.json)
5. **Re-run TEAx pipeline**:
   - Same LCOE output as Item 5 (values must match)
   - But now component costs flow through codegen, not generate_costs.py

**Out of Scope**:
- Generic PartUsage traversal beyond cost patterns
- Nested PartUsage-within-PartUsage discovery (only one level deep)
- Performance optimization of extraction

**Success Criteria**:
- [ ] Codegen discovers all 9 embedded component cost CalcUsages + allocation
- [ ] Synthetic CalcUsageData has correct bindings resolved from design
- [ ] Generated modules produce correct cost values (match generate_costs.py output)
- [ ] TEAx pipeline runs with generated cost modules (no component_costs.json entry point)
- [ ] LCOE output matches Item 5 result within tolerance
- [ ] Existing codegen tests still pass (no regressions)

**Dependencies**: Items 1–5 (working pipeline to validate against)

**Deliverables**:
- Enhanced `usage_extractor.py` with nested CalcUsage discovery
- Enhanced `dependency_backtracker.py` with redefinition binding resolution
- Updated generated code for solar+battery
- Regression tests for new extraction capability
- Before/after comparison document

---

## Effort Summary

| Item | Type | Dependencies |
|------|------|-------------|
| 1. Solar+Battery SysML Model | Modeling | None |
| 2. Codegen CalcUsage-Chain Spike | Spike | None |
| 3. Cost Evaluation & Entry Points | Implementation | Item 1 |
| 4. Codegen Pipeline Run | Code/Integration | Items 1, 2, 3 |
| 5. TEAx End-to-End Execution | Execution/Validation | Items 3, 4 |
| 6. Codegen Enhancement — Nested Discovery | Code/Implementation | Items 1–5 |

Items 1 and 2 can be done **in parallel** (the spike uses a standalone minimal model, not the solar+battery model).

Items 1–5 are the **pragmatic path**: prove the full pipeline works today with a hybrid approach (generate_costs.py + codegen).

Item 6 is the **completeness path**: eliminate the workaround by enhancing codegen to handle the nested pattern natively.

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Coffee maker model (reference pattern) | Ready | Stage 1–3 complete |
| `'Costed Component'` interface | Ready | `costing.sysml` complete (pending commit) |
| sysml-codegen | Ready | Functional for top-level CalcUsages; chain handling confirmed (Item 2). Runtime gaps fixed in `61aa907`. |
| TEAx/teax-simkit | Ready | Battery demo proves framework works |
| agentic-mbse (SysideAdapter) | Ready | Used by all scripts |

---

## References

### Prior Research
- [20260107-final-cost-architecture.md](../research/20260107-final-cost-architecture.md) — Nested cost model architecture
- [20260110-strategic-cost-patterns.md](../research/20260110-strategic-cost-patterns.md) — Standardization decisions
- [epic-cost-patterns-derisking.md](epic-cost-patterns-derisking.md) — Coffee maker de-risking (Stages 1–3)
- [20260126-lcoe-visibility-requirements-analysis.md](../../modeling_pm/research/20260126-lcoe-visibility-requirements-analysis.md) — LCOE gap analysis (PyFECONS formula structure)

### Codebases
- `sysml-codegen` at `/home/reid/1cfe/sysml-codegen` — Code generation pipeline
- `teax-simkit` at `/home/reid/1cfe/teax/packages/teax-simkit` — Pipeline execution framework
- `battery-tea-demo` at `/home/reid/1cfe/teax/packages/battery-tea-demo` — Reference implementation

### Test Models
- `models/tests/coffee_maker/` — Proven cost pattern reference
- `models/tests/solar_battery/` — NEW: This epic's deliverable
- `models/tests/codegen_chain_spike/` — NEW: Item 2 spike model

---

**Last Updated**: 2026-02-02
