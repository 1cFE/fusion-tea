# Spec: Cost Evaluation Script

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-12 14:51:33 UTC
**Complexity:** MEDIUM
**Branch:** costing-patterns

---

## Business Goals

### Why This Matters

Before investing in sysml-codegen tooling upgrades (Stage 4), we need to prove that the cost modeling pattern (Pattern A: nested cost models) is not just parseable but *evaluable*. Stage 2's `expected_output.csv` is hand-calculated - without automated evaluation, we can't validate that the model structure actually supports cost computation.

This script serves as a prototype for what sysml-codegen needs to do, proving the approach works before building production tooling.

### Success Criteria

- [ ] Script produces `actual_output.csv` matching `expected_output.csv` within floating-point tolerance
- [ ] All 7 leaf cost calculations are evaluated correctly
- [ ] Multiplicity handling works (heater[2] → 2 × unit cost in totals)
- [ ] Assembly rollups aggregate correctly (children + allocation)
- [ ] Comparison logic reports pass/fail with diff details

### Priority

P0 - Blocking Stage 3 (iteration) and Stage 4 (sysml-codegen implementation).

---

## Problem Statement

### Current State

- `validate_ast.py` proves the model is *traversable* (finds calc usages, bindings, hierarchy)
- `expected_output.csv` contains hand-calculated cost values
- No automated way to verify the model produces correct cost values
- No validation that formulas, bindings, and multiplicity work together

### Desired Outcome

A Python script that:
1. Loads the coffee maker SysML model
2. Extracts all necessary information from the AST
3. Evaluates cost calculations with bound parameters
4. Produces output matching the expected CSV
5. Reports comparison results

---

## Scope

### In Scope

- **Parameter extraction**: Resolve `:>>` bindings in design.sysml to get concrete values
- **Formula extraction**: Parse calc def output expressions from library.sysml
- **Calculation evaluation**: Evaluate formulas with bound inputs
- **Multiplicity handling**: Multiply unit costs by array size for arrayed parts
- **Assembly aggregation**: Compute rollup costs from children + allocation
- **CSV generation**: Output `actual_output.csv` in expected schema
- **Comparison**: Diff actual vs expected with tolerance reporting

### Out of Scope

- Changes to sysml-codegen (deferred to Stage 4)
- Changes to SysML models (library.sysml, design.sysml are inputs)
- Generic/reusable framework (this is a one-off validation script)
- Support for models other than coffee maker test case

### Edge Cases & Considerations

- **Default values**: Calc defs have default parameter values (e.g., `material_cost_per_kg : Real default := 50.0`) that must be used when not overridden
- **Nested redefinitions**: Design uses `part redefines brewing { :>> heater.power_rating = 1000.0 }` - must trace through redefinition chain
- **sum() aggregation**: Library uses `sum(heater.capital_cost)` for multiplicity rollup - must handle this pattern
- **Allocation costs**: Assembly-level allocation_model contributes to rollup but is categorized separately

---

## Requirements

### Functional Requirements

> Requirements below are from epic Stage 2b specification

1. **FR-1**: Extract parameter bindings from PartUsages (`:>> power_rating = 1000.0`)
2. **FR-2**: Extract calc def formulas and default values from library
3. **FR-3**: Evaluate calculations with bound parameters
4. **FR-4**: Handle multiplicity (heater[2] → quantity=2, total = 2 × unit cost)
5. **FR-5**: Aggregate assembly rollups (children + allocation at each level)
6. **FR-6**: Output `actual_output.csv` in same schema as `expected_output.csv`
7. **FR-7**: Compare actual vs expected and report pass/fail with diff details

### Output Schema

Per `expected_output.csv`, columns are:
- `path` - Qualified path (e.g., `coffee_maker.brewing.heater`)
- `part_def` - Part definition name
- `quantity` - Part count (e.g., 2 for arrayed parts)
- `unit_material_cost`, `unit_fab_cost`, `unit_install_cost`, `unit_total_cost` - Per-unit costs (leaf only)
- `total_material_cost`, `total_fab_cost`, `total_install_cost`, `total_cost` - Totals (quantity × unit for leaves, sum for assemblies)
- `idiot_index` - total_cost / total_material_cost
- `cost_type` - "leaf", "assembly", or "allocation"
- `calc_def` - Calc definition name (leaf only)

---

## Acceptance Criteria

### Core Functionality

- [ ] Script loads model via `SysideAdapter.load_model()`
- [ ] Extracts all 7 leaf part parameter values from design.sysml
- [ ] Extracts all calc def formulas from library.sysml
- [ ] Evaluates each leaf cost_model with correct bound values
- [ ] Computes correct unit costs for each leaf part
- [ ] Handles heater[2] multiplicity (quantity=2, totals = 2 × unit)
- [ ] Computes assembly rollups including allocation costs
- [ ] Writes `actual_output.csv` to `models/tests/coffee_maker/`
- [ ] Comparison passes with floating-point tolerance (~1e-6)

### Quality & Integration

- [ ] Script runs successfully: `python generate_costs.py`
- [ ] No additional dependencies beyond agentic-mbse
- [ ] Clear error messages if model fails to load or parse

---

## Technical Notes

### Available Infrastructure

From `agentic_mbse.sysml`:
- `SysideAdapter` - Model loading and element iteration
- `expression.py` - `evaluate_true_static_expression()` for literal math, `extract_feature_refs()` for reference extraction
- `binding.py` - `extract_bindings()` for calc usage parameters

From `validate_ast.py`:
- `find_cost_models()` - Discovers cost_model calc usages in part definitions
- `find_part_usages_with_multiplicity()` - Discovers part usages with array counts
- `_extract_multiplicity_bound()` - Extracts multiplicity from AST

### Key AST Patterns

1. **Calc def output expressions**: `calc_def.owned_members` contains output attributes with `feature_value_expression`
2. **Part usage redefinitions**: `part_usage.owned_redefinitions` contains `:>>` bindings
3. **Multiplicity**: `part_usage.multiplicity.upper_bound` contains count (LiteralInteger or attribute ref)

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-cost-patterns-derisking.md` (Stage 2b)
- **Test Model:** `models/tests/coffee_maker/` (library.sysml, design.sysml)
- **Expected Output:** `models/tests/coffee_maker/expected_output.csv`
- **AST Validation:** `models/tests/coffee_maker/validate_ast.py`
- **Design:** `.project/active/cost-evaluation-script/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
