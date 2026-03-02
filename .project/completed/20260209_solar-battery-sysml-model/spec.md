# Spec: Solar+Battery SysML Model

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-31 23:12 UTC
**Complexity:** HIGH
**Branch:** visualization
**Epic:** End-to-End Pipeline De-Risking (Item 1)

---

## Business Goals

### Why This Matters

The coffee maker epic proved that the nested cost pattern (Pattern A) compiles, is AST-traversable, and is evaluable. But the coffee maker has no energy production, no LCOE, and no mapping to the PyFECONS formula structure that fusion will use. A solar+battery model closes this gap: it exercises the full LCOE pipeline — component costs through subsystem rollup through system-level calculations to a final $/MWh value — using realistic economics that can be verified against industry benchmarks.

This model is the foundation for all downstream pipeline items (codegen spike, cost evaluation, TEAx execution). Every subsequent item validates against the expected outputs produced here.

### Success Criteria

- [ ] A complete SysML model that compiles and represents a solar+battery plant with nested cost patterns and PyFECONS-aligned LCOE calculations
- [ ] AST validation script confirms all cost models, bindings, multiplicity, and system-level calc structure
- [ ] Hand-calculated expected outputs serve as the single verification target for all downstream items
- [ ] The model uses the production foundation `Costing` package (not a local copy), making the test representative of production patterns

### Priority

P0 — blocking the full cost modeling pipeline. Items 2–6 of the epic depend on this model existing.

---

## Problem Statement

### Current State

- The coffee maker model exists as a proven reference for Pattern A (nested cost models)
- The foundation `Costing` package exists with `'Costed Component'`, `CASCategory` enum, and `cas_category` attribute
- No test model exercises energy production or LCOE calculations
- No test model uses the PyFECONS formula structure (CAS70/80/90 → LCOE)
- No expected output exists for pipeline verification

### Desired Outcome

A solar+battery SysML model that:
1. Follows the coffee maker's proven nested cost pattern (9 leaf parts with embedded cost calc usages)
2. Adds PyFECONS-aligned system-level calculations (energy production, O&M, fuel, financial, LCOE)
3. Produces hand-calculable expected outputs that downstream items validate against
4. Uses the production `Costing` package to ensure test fidelity

---

## Scope

### In Scope

- `library.sysml` — CalcDefs, leaf PartDefs, assembly PartDefs, top-level PartDef
- `design.sysml` — Concrete instance with parameter bindings, multiplicity, system-level CalcUsages
- `validate_ast.py` — AST validation script using syside
- `expected_output.csv` — Hand-calculated verification target

### Out of Scope

- Degradation modeling beyond simple annual rate
- Time-of-use or dynamic pricing
- Battery cycling or dispatch optimization
- `generate_costs.py` (Item 3)
- Codegen execution (Item 2)
- TEAx pipeline wiring (Items 4–5)
- Changes to the foundation `Costing` package or agentic-mbse

### Edge Cases & Considerations

- The foundation `Costing` package requires `cas_category` on every `'Costed Component'`. The solar model will need to assign CAS categories to each part, even though this is a test model. Use reasonable mappings (solar array → CAS22 analog, etc.)
- The `sum()` function for multiplicity rollup is proven in the coffee maker but hasn't been used with the foundation package's `cas_category` attribute — verify no interaction issues
- The PyFECONS LCOE formula uses inflation escalation, which means the solar LCOE will differ from typical solar LCOE calculators. This is intentional — the model tests the fusion formula structure, not solar industry conventions
- `annual_fuel_cost = 0` for solar is a realistic value, not a hack. It exercises the wiring while producing correct results

---

## Requirements

### Functional Requirements

> Requirements below are from the user's epic description and clarifications unless marked [INFERRED].

#### library.sysml

1. **FR-1**: MUST define 9 component cost CalcDefs, each with inputs specific to the component and outputs: `material_cost`, `fab_cost`, `install_cost`, `total_cost`, `idiot_index`. CalcDefs: PVModuleCostCalc, InverterCostCalc, ArrayBOSCostCalc, BatteryPackCostCalc, HybridInverterCostCalc, BatteryBOSCostCalc, RackingCostCalc, ElectricalPanelCostCalc, PermittingCostCalc.

2. **FR-2**: MUST define 1 AllocationCostCalc for assembly-level minor items (fasteners, labels, conduit), following the coffee maker's allocation pattern.

3. **FR-3**: MUST define 5 system-level CalcDefs aligned with the PyFECONS LCOE structure:
   - **EnergyProductionCalc**: `annual_energy_mwh = 8760 * p_net_mw * n_mod * plant_availability`
   - **AnnualizedOMCalc**: `annual_om_cost = om_rate_per_kw_year * p_net_kw`
   - **AnnualizedFuelCalc**: `annual_fuel_cost = fuel_unit_cost * fuel_consumption`
   - **AnnualizedFinancialCalc**: `capital_recovery_factor = r*(1+r)^n / ((1+r)^n - 1)`; `annualized_capital_cost = CRF * total_capex`
   - **LCOECalc**: `lcoe_per_mwh = (C900000 + (C700000 + C800000) * (1 + yearly_inflation)^plant_lifetime) / annual_energy_mwh`

4. **FR-4**: MUST define 9 leaf PartDefs, each specializing `Costing::'Costed Component'` from the foundation package (NOT a local copy). Each leaf MUST have an embedded `cost_model` CalcUsage that binds component parameters to calc inputs and exposes cost outputs via `:>>` redefinition.

5. **FR-5**: MUST define 3 assembly PartDefs (Solar Array, Battery System, Site Infrastructure), each specializing `'Costed Component'`. Assemblies MUST aggregate child costs using `sum()` for arrayed parts. Assemblies do NOT have cost calc usages — they use summation expressions only.

6. **FR-6**: MUST define 1 top-level `'Solar Battery Plant'` PartDef that aggregates the 3 assembly costs.

7. **FR-7**: PermittingCostCalc SHOULD output only `total_cost` (soft cost, no material/fab split), per the epic's specification.

8. **FR-8**: [INFERRED] Each PartDef MUST assign an appropriate `cas_category` value from the `CASCategory` enum, as required by the foundation `'Costed Component'` interface.

#### design.sysml

9. **FR-9**: MUST create a concrete plant instance with parameter bindings via `:>>`.

10. **FR-10**: MUST use multiplicity: PV modules [20], string inverters [4], battery packs [8].

11. **FR-11**: MUST include 5 system-level CalcUsages as explicit top-level usages (visible to codegen), NOT nested inside PartDefs. These wire together the system-level calcs defined in the library.

12. **FR-12**: MUST bind all operating, financial, and fuel parameters to specific values consistent with the target values in the epic:
    - `p_net_mw = 0.008`, `n_mod = 1`, `plant_availability ≈ 0.159`
    - `plant_lifetime = 25`, `discount_rate = 0.05`, `yearly_inflation = 0.0245`
    - `om_rate_per_kw_year = 20`, `fuel_unit_cost = 0`, `fuel_consumption = 0`

#### validate_ast.py

13. **FR-13**: MUST discover 10 cost calc usages (9 leaf + 1 allocation) and 5 system-level CalcUsages.

14. **FR-14**: MUST detect multiplicity on the 3 arrayed parts (PV modules, inverters, battery packs).

15. **FR-15**: MUST verify system-level CalcUsages are at design level (not nested in PartDefs).

16. **FR-16**: MUST verify inter-calc dependencies — LCOECalc inputs trace to other calc outputs.

17. **FR-17**: MUST verify 3 assembly parts exist with `sum()` rollup (cost attribute aggregation, not calc usages).

#### expected_output.csv

18. **FR-18**: MUST contain hand-calculated cost breakdown for all 9 leaf parts, 3 assemblies, and the top-level plant, using exact parameter values from the design.

19. **FR-19**: MUST contain the LCOE value calculated using the PyFECONS formula structure with the exact parameter values. This is the verification target — all downstream items validate against it.

20. **FR-20**: MUST use the same 14-column CSV schema proven in the coffee maker.

21. **FR-21**: MUST produce values within sanity-check ranges: Total CAPEX $35k–$45k, annual energy 10,000–12,000 kWh, LCOE $0.15–$0.35/kWh.

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv run syside check models/tests/solar_battery/` exits 0
- [ ] `validate_ast.py` finds 10 cost calc usages (9 leaf + 1 allocation)
- [ ] `validate_ast.py` finds 5 system-level CalcUsages at design level
- [ ] `validate_ast.py` detects multiplicity on 3 arrayed parts
- [ ] `validate_ast.py` verifies 3 assembly parts with sum() rollup
- [ ] `validate_ast.py` verifies LCOECalc inter-calc dependencies
- [ ] `expected_output.csv` computed from exact parameters, LCOE within sanity-check range
- [ ] LCOECalc uses PyFECONS formula structure with 3-term numerator and inflation escalation

### Quality & Integration

- [ ] Model imports from foundation `Costing` package (not a local interface copy)
- [ ] All leaf PartDefs assign `cas_category`
- [ ] Coffee maker model and tests continue to work (no regressions)
- [ ] System-level CalcDefs are reusable — not solar-specific in their definition, only in their parameterization

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 1)
- **Research:** `modeling_pm/research/20260126-lcoe-visibility-requirements-analysis.md`
- **Reference Pattern:** `models/tests/coffee_maker/` (library.sysml, design.sysml)
- **Foundation Package:** `models/library/foundation/costing.sysml`
- **Design:** `.project/active/solar-battery-sysml-model/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
