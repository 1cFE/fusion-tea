---
date: 2026-01-06T06:54:31-08:00
researcher: Claude
topic: "Cost Architecture Patterns for Fusion TEA"
tags: [research, cost-modeling, sysmlv2, agentic-mbse, lcoe, architecture]
status: complete
last_updated: 2026-01-06 (addendum added)
---

# Research: Cost Architecture Patterns for Fusion TEA

**Date**: 2026-01-06 06:54 PST (addendum 08:30 PST)
**Researcher**: Claude
**Research Type**: Architecture Design (SysMLv2 + Tooling Integration)

## Research Question

How should we architect cost modeling in SysMLv2 to address:
1. Single instantiation pattern (avoid redundant calc wiring)
2. Scalable/recursive cost patterns (hierarchy rollup)
3. Enforcement via agentic-mbse (validation rules)
4. Standard cost output schema (cross-concept comparison)
5. Extension to full LCOE (beyond CapEx)

## Summary

- **Single Instantiation**: SysMLv2 does NOT support auto-instantiation of nested calcs. Accept explicit wiring in design files (provides auditability). Future tooling enhancement possible but not recommended initially.
- **Recursive Aggregation**: No built-in `sum()` operations. Use semantic cost calc defs at each hierarchy level with explicit aggregation formulas.
- **Enforcement via agentic-mbse**: Comprehensive 8-level validation framework exists. Add Level 9 for cost modeling with 3 rules: (1) Costed Components have calc defs, (2) Calc inputs match part attributes, (3) Cost-bearing parts have usages.
- **Standard Output Schema**: PyFECONS defines 60+ cost categories. Proposed schema with 25+ required outputs for cross-concept comparison. sysml-codegen and teax-simkit natively support multi-output routing.
- **Full LCOE**: PyFECONS formula fully documented. Requires CAS70 (O&M), CAS80 (fuel), CAS90 (annualized financial), plus plant availability and lifetime.

---

## Detailed Findings

### Q1: Single Instantiation Pattern

**Problem**: Currently, designs must:
1. Instantiate structural parts (`part magnets : 'Magnet System'`)
2. Separately instantiate cost calcs (`calc magnet_cost : MagnetSystemCost`)
3. Wire them together (`in n_coils = magnets.n_coils`)

**Finding**: SysMLv2 does NOT support automatic calculation inclusion via part instantiation.

**Evidence from Testing** (prior research):
```sysml
// This pattern does NOT work as hoped:
part def 'Magnet System' {
    calc cost_model : MagnetCostCalc { ... }  // Only exists in template
}

part magnets : 'Magnet System';  // Does NOT create magnets.cost_model instance
```

syside does NOT instantiate nested calc usages. When a part def containing a calc usage is instantiated:
- sysml-codegen finds the calc usage in the **part definition template**
- It does NOT create a calc usage instance when the part is instantiated

**Analysis Cases & Viewpoints - Limited Help**:
- **Analysis cases** exist for organizing analysis contexts but don't provide auto-wiring
- **Viewpoints/views** are for organizing visualizations, not computational dependencies

**Recommendation**: Accept explicit calc wiring in design files.

**Rationale**:
1. **Auditability**: All calculations visible in one place
2. **Traceability**: Clear which calc produces which cost
3. **Tool Support**: sysml-codegen finds all calc usages automatically
4. **Multi-output**: Pattern exposes all intermediate values

**Pattern**:
```sysml
part catf_plant : 'CATF Fusion Plant' {
    // Structure
    part magnets : 'Magnet System' { :>> field_strength = 12.0; }
    part blanket : 'Blanket System' { ... }

    // Cost calculations (explicit wiring - visible and auditable)
    calc magnet_cost : MagnetSystemCostCalc {
        in field = magnets.field_strength;
        in n_coils = 12;
    }

    calc blanket_cost : BlanketSystemCostCalc {
        in area = blanket.surface_area;
    }

    // EXPOSE all outputs for visibility
    attribute magnet_capital : Real = magnet_cost.total_capital;
    attribute blanket_capital : Real = blanket_cost.total_capital;

    // Top-level LCOE
    calc lcoe : LCOECalculation {
        in cas22_reactor = magnet_capital + blanket_capital;
    }

    attribute lcoe_value : Real = lcoe.lcoe;
    attribute overnight_cost_per_kw : Real = lcoe.overnight_cost_per_kw;
}
```

**Limitations & Workarounds**:
- **Limitation**: Repetitive wiring if many components
- **Workaround**: Use templates/patterns in text editor, or code generation scripts

---

### Q2: Scalable Recursive Cost Patterns

**Problem**: Fusion plants have deep structural hierarchies. Cost must flow up: leaf components → subsystems → systems → plant total.

**Finding**: SysMLv2 does NOT support collection operations like `parts.cost->sum()`.

**What's Supported**:
- Derived attributes with expressions (`attribute x = y + z`)
- Redefinition with values (`:>> attribute = value`)
- Multi-level attribute references

**What's Missing**:
- `parts.cost->sum()` - No collection sum operation
- `collect()` operations on part multiplicities
- Built-in aggregation functions

**Recommendation**: Use semantic cost calc defs at each aggregation level.

**Pattern for Fixed-Count Children**:
```sysml
part magnet_system {
    part tf_coils : 'TF Coil' [12];

    calc rollup : TFCoilArrayCost {
        in unit_cost = tf_coils.capital_cost;
        in quantity = 12;
        out total : Real = unit_cost * quantity;
    }
    attribute total_tf_cost : Real = rollup.total;
}
```

**Pattern for Hierarchical Rollup**:
```sysml
// Leaf component
part def 'TF Coil' :> 'Costed Component' {
    attribute capital_cost : Real;
}

// Subsystem level
part def 'Magnet System' :> 'Costed Component' {
    part tf_coils : 'TF Coil' [12];
    part pf_coils : 'PF Coil' [6];

    calc subsystem_cost : MagnetSystemCostCalc {
        in tf_unit = tf_coils.capital_cost;
        in tf_count = 12;
        in pf_unit = pf_coils.capital_cost;
        in pf_count = 6;
    }

    :>> capital_cost = subsystem_cost.total;
}

// System level
part fusion_plant {
    part magnets : 'Magnet System';
    part blanket : 'Blanket System';

    calc plant_cost : PlantCostRollup {
        in magnet_cost = magnets.capital_cost;
        in blanket_cost = blanket.capital_cost;
    }

    attribute total_capital : Real = plant_cost.total;
}
```

**Key Principle - Semantic Cost Models, Not Generic Math**:

**Wrong approach** (generic math wrappers):
```sysml
// BAD: meaningless abstraction
calc def MultiplyAndAdd {
    in a : Real; in b : Real; in c : Real;
    out result : Real = a * b + c;
}
```

**Correct approach** (semantic cost models):
```sysml
// GOOD: encodes domain knowledge
calc def MagnetSystemCostCalc {
    doc /* Cost model for complete magnet system per PyFECONS CAS220103 */

    in tf_conductor_volume : Real;
    in tf_structure_mass : Real;
    in n_tf_coils : Integer;
    in conductor_cost_per_m3 : Real;

    out tf_material_cost : Real = tf_conductor_volume * conductor_cost_per_m3 * n_tf_coils;
    out manufacturing_cost : Real = tf_material_cost * 1.3;
    out total_capital : Real = tf_material_cost + manufacturing_cost;
    out conductor_fraction : Real = tf_material_cost / total_capital;
}
```

---

### Q3: Enforcement via agentic-mbse

**Finding**: agentic-mbse has a comprehensive 8-level validation pyramid.

**Files**: `/home/reid/1cfe/agentic-mbse/src/agentic_mbse/validation/`

**Existing Levels**:
- Level 1: Syntax Validation
- Level 2: Structural Completeness
- Level 3: Dataflow Integrity
- Level 4: Constraint Satisfaction
- Level 5: Semantic Consistency
- Level 6: Traceability & Documentation
- Level 7: Architectural Integrity
- Level 8: Codegen Readiness

**Framework for Custom Rules**:

All rules follow this pattern:
1. **Function signature**: `check_X(model: Any) -> list[ValidationIssue]`
2. **Element iteration**: Use `SysideAdapter.elements_of_type(model, "TypeName")`
3. **Issue creation**: Instantiate `ValidationIssue` with structured metadata
4. **Return**: List of `ValidationIssue` objects

**Recommendation**: Add Level 9 for Cost Modeling Conventions.

**Three Cost Modeling Rules**:

**Rule 1: Every Costed Component has calc def**
```python
def check_costed_components_have_calcs(model: Any) -> list[ValidationIssue]:
    """Check Rule 1: Every PartDef specializing 'Costed Component'
       must have a corresponding CalculationDefinition"""
    issues = []
    for part_def in SysideAdapter.elements_of_type(model, "PartDefinition"):
        if _specializes_costed_component(part_def):
            expected_calc_name = _derive_calc_def_name(part_def.name)
            if not _calc_def_exists(model, expected_calc_name):
                issues.append(ValidationIssue(
                    level=9, severity=Severity.ERROR,
                    code=ValidationCode.COST_MISSING_CALC_DEF,
                    message=f"Costed component '{part_def.name}' lacks cost calc",
                    suggestion=f"Create calc def: {expected_calc_name}"
                ))
    return issues
```

**Rule 2: Calc def inputs match part attributes**
```python
def check_calc_inputs_match_part_attributes(model: Any) -> list[ValidationIssue]:
    """Check Rule 2: For each cost calc def, verify inputs
       correspond to attributes in associated PartDef"""
    issues = []
    for calc_def in SysideAdapter.elements_of_type(model, "CalculationDefinition"):
        if not _is_cost_calc(calc_def): continue
        associated_part = _find_associated_part_def(model, calc_def)
        if not associated_part: continue

        calc_inputs = _extract_input_features(calc_def)
        part_attrs = _extract_part_attributes(associated_part)

        for input_feat in calc_inputs:
            if input_feat.name not in part_attrs:
                issues.append(ValidationIssue(
                    level=9, severity=Severity.WARNING,
                    code=ValidationCode.COST_INPUT_NOT_IN_PART,
                    message=f"Input '{input_feat.name}' not in part"
                ))
    return issues
```

**Rule 3: Cost-bearing parts have cost usages**
```python
def check_cost_bearing_parts_have_usages(model: Any) -> list[ValidationIssue]:
    """Check Rule 3: Every cost-bearing PartUsage in designs/
       must have at least one CalculationUsage for cost"""
    issues = []
    for part_usage in SysideAdapter.elements_of_type(model, "PartUsage"):
        if "designs/" not in str(part_usage.document.url): continue
        if not _is_cost_bearing(part_usage): continue

        if not _has_cost_calc_usage(part_usage):
            issues.append(ValidationIssue(
                level=9, severity=Severity.ERROR,
                code=ValidationCode.COST_MISSING_USAGE,
                message=f"Part '{part_usage.name}' has no cost calc"
            ))
    return issues
```

**Integration with /audit-models**:
```bash
# Validate only cost modeling
agentic-mbse validate models/ --level 9

# Run all levels including cost modeling
agentic-mbse validate models/ --complete
```

---

### Q4: Standard Cost Output Schema

**Finding**: PyFECONS defines 60+ cost categories following ARPA-E CAS structure.

**PyFECONS CAS Hierarchy** (from `/home/reid/PyFECONS/pyfecons/costing/`):

```
CAS10 - Pre-Construction Costs
CAS20 - Direct Capital Cost
  CAS21 - Buildings & Infrastructure
  CAS22 - Reactor Plant Equipment (~60% of cost)
    CAS220101-220119 - Core reactor equipment
    CAS2202-2207 - Auxiliary systems
  CAS23 - Turbine Plant Equipment
  CAS24 - Electric Plant Equipment
  CAS25 - Miscellaneous Plant Equipment
  CAS26 - Heat Rejection
  CAS27 - Special Materials
  CAS28 - Digital Twin
  CAS29 - Contingency on Direct Costs
CAS30 - Capitalized Indirect Service
CAS40 - Capitalized Owner's Costs
CAS50 - Capitalized Supplementary
CAS60 - Capitalized Financial
CAS70 - Annualized O&M
CAS80 - Annualized Fuel
CAS90 - Annualized Financial Charges
LCOE - Final Output ($/MWh)
```

**Recommendation**: Define standard cost output schema with 25+ required outputs.

**Proposed Schema**:

```sysml
/**
 * Standard Cost Output Schema for Cross-Concept Comparison
 *
 * All fusion designs MUST expose these outputs to enable
 * systematic comparison via pipeline execution.
 */
calc def StandardCostOutputs {
    // === CAPITAL COSTS ===
    out cas10_pre_construction : Real;      // Pre-construction [$M]
    out cas20_direct_total : Real;          // Total direct costs [$M]
    out cas21_buildings : Real;             // Buildings [$M]
    out cas22_reactor_equipment : Real;     // Reactor equipment [$M]
    out cas22_magnets : Real;               // Magnet subsystem [$M]
    out cas22_blanket : Real;               // Blanket subsystem [$M]
    out cas22_divertor : Real;              // Divertor subsystem [$M]
    out cas22_structure : Real;             // Primary structure [$M]
    out cas23_turbine : Real;               // Turbine plant [$M]
    out cas24_electric : Real;              // Electric plant [$M]
    out cas25_misc : Real;                  // Miscellaneous [$M]
    out cas26_heat_rejection : Real;        // Heat rejection [$M]
    out cas27_special_materials : Real;     // Special materials [$M]
    out cas30_indirect : Real;              // Indirect costs [$M]
    out cas40_owners : Real;                // Owner's costs [$M]
    out cas50_supplementary : Real;         // Supplementary costs [$M]
    out cas60_financial : Real;             // Financial costs [$M]

    // === OPERATING COSTS ===
    out cas70_annual_om : Real;             // Annual O&M [$/year]
    out cas80_annual_fuel : Real;           // Annual fuel [$/year]

    // === SUMMARY METRICS ===
    out total_capital_cost : Real;          // C990000 [$M]
    out cas90_annualized : Real;            // Annualized capital [$/year]
    out lcoe : Real;                        // Levelized cost [$/MWh]

    // === BREAKDOWN FRACTIONS ===
    out overnight_cost_per_kw : Real;       // $/kW
    out capital_lcoe_fraction : Real;       // Capital contribution to LCOE
    out om_lcoe_fraction : Real;            // O&M contribution to LCOE
    out fuel_lcoe_fraction : Real;          // Fuel contribution to LCOE
    out magnet_cost_fraction : Real;        // Magnets as % of reactor
    out blanket_cost_fraction : Real;       // Blanket as % of reactor
}
```

**sysml-codegen Support**:

Multi-output detection is automatic:
- `len(output_attributes) >= 2` triggers MultiOutput pattern
- Generates `{CalcName}Output` Pydantic model with all fields
- Each output becomes separate exit point channel

**teax-simkit Support**:

Exit point architecture captures all outputs:
- Each field in MultiOutput becomes separate JSON file
- RunManifest records all produced artifacts
- Field references enable downstream extraction

**Comparison Example**:
```python
# Run multiple designs
catf_result = execute_pipeline("catf/pipeline.yaml", "results/catf/",
    custom_schema_types=[StandardCostOutputs])
stellarator_result = execute_pipeline("stellarator/pipeline.yaml", "results/stellarator/",
    custom_schema_types=[StandardCostOutputs])

# Compare standardized outputs
comparison = {
    "CATF": {
        "lcoe": catf_result.outputs["lcoe"],
        "overnight_cost_per_kw": catf_result.outputs["overnight_cost_per_kw"],
        "magnet_cost_fraction": catf_result.outputs["magnet_cost_fraction"],
    },
    "Stellarator": {
        "lcoe": stellarator_result.outputs["lcoe"],
        "overnight_cost_per_kw": stellarator_result.outputs["overnight_cost_per_kw"],
        "magnet_cost_fraction": stellarator_result.outputs["magnet_cost_fraction"],
    },
}
```

---

### Q5: Extension to Full LCOE

**Finding**: PyFECONS LCOE formula fully documented.

**LCOE Formula** (from `/home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py`):

```python
lcoe.C1000000 = (
    cas90.C900000 +
    (cas70.C700000 + cas80.C800000) * (1 + yearly_inflation) ** plant_lifetime
) / (8760 * p_net * n_mod * plant_availability)
```

**Components**:

1. **CAS90 - Annualized Financial Cost**:
   ```
   C900000 = capital_recovery_factor × C990000
   ```
   - capital_recovery_factor = 0.09 (default, from NETL methodology)
   - C990000 = Total Capital Cost

2. **CAS70 - Annualized O&M**:
   ```
   C700000 = 60 × P_net × 1000  [M$/year]
   ```
   - Fixed cost basis: $60/MW/year

3. **CAS80 - Annualized Fuel (D-T)**:
   ```
   C800000 = (n_mod × P_nrl × 1e6 × 3600 × 8760 × u_D × m_D × availability)
             / (17.58 × 1.6021e-13)
   ```
   - u_D = $2175/kg (Deuterium cost)
   - m_D = 3.342e-27 kg (mass of deuterium atom)
   - 17.58 MeV = DT reaction energy release

4. **Annual Energy Production**:
   ```
   annual_energy = 8760 × p_net × n_mod × plant_availability
   ```

**Lifecycle Costs**:

- **Scheduled Replacement** (CAS220119):
  ```
  C220119 = cas2201_total_cost × primary_structure.replacement_factor
  ```

- **Replacement Interval**: Part def attribute `replacement_interval_years`

**Key Financial Parameters**:

| Parameter | Default | Source |
|-----------|---------|--------|
| capital_recovery_factor | 0.09 | NETL fossil plant methodology |
| plant_lifetime | - | Input (typically 40-60 years) |
| plant_availability | - | Input (typically 0.76-0.90) |
| yearly_inflation | - | Input (typically 0.02-0.03) |
| construction_time | - | Input (typically 6-12 years) |

**Recommendation**: Create `LCOECalculation` calc def with full breakdown.

**Pattern**:
```sysml
calc def LCOECalculation {
    doc /*
    Master LCOE calculation per PyFECONS methodology.
    Exposes all intermediate values for sensitivity analysis.

    **Source**: PyFECONS costing/calculations/lcoe.py
    */

    // === INPUTS ===
    in total_capital : Real;           // C990000 [$M]
    in annual_om : Real;               // CAS70 [$/year]
    in annual_fuel : Real;             // CAS80 [$/year]
    in p_net : Real;                   // Net power [MW]
    in plant_availability : Real;      // Capacity factor [0-1]
    in plant_lifetime : Real;          // Years
    in yearly_inflation : Real;        // Annual rate
    in capital_recovery_factor : Real default := 0.09;

    // === INTERMEDIATE CALCULATIONS ===
    out cas90_annualized : Real = capital_recovery_factor * total_capital * 1e6;

    out inflated_opex : Real =
        (annual_om + annual_fuel) * ((1.0 + yearly_inflation) ** plant_lifetime);

    out annual_energy_mwh : Real = 8760.0 * p_net * plant_availability;

    out total_annual_cost : Real = cas90_annualized + inflated_opex;

    // === FINAL LCOE ===
    out lcoe : Real = total_annual_cost / annual_energy_mwh;

    // === BREAKDOWN METRICS ===
    out capital_lcoe_fraction : Real = cas90_annualized / total_annual_cost;
    out om_lcoe_fraction : Real = annual_om / total_annual_cost;
    out fuel_lcoe_fraction : Real = annual_fuel / total_annual_cost;
    out overnight_cost_per_kw : Real = total_capital * 1000.0 / p_net;
}
```

---

## Implementation Roadmap

### Phase 1: Cost Infrastructure

1. **Create `models/library/definitions/costed_component.sysml`**
   - Define `abstract part def 'Costed Component'`
   - Required attributes: capital_cost, annual_operating_cost, replacement_cost, replacement_interval_years

2. **Update MODELING_GUIDE.md**
   - Document cost interface requirement
   - Add cost calc def naming conventions

3. **Add agentic-mbse Level 9 validation**
   - Implement three cost modeling rules
   - Register in validation runner

### Phase 2: Semantic Cost Calc Defs

4. **Create `models/library/calculations/costing/` directory**
   - `blanket_cost.sysml` - BlanketSystemCostCalc
   - `magnet_cost.sysml` - MagnetSystemCostCalc
   - `structure_cost.sysml` - StructureCostCalc
   - `subsystem_rollup.sysml` - ReactorCostRollup

5. **Create `models/library/calculations/lcoe.sysml`**
   - LCOECalculation with 20+ outputs
   - LifecycleCostCalc for replacement cost NPV

### Phase 3: CATF Design Integration

6. **Update CATF design to wire cost calcs**
   - Wire structural parts to cost calc defs
   - EXPOSE all cost outputs

7. **Test end-to-end pipeline**
   - sysml-codegen generates modules
   - teax-simkit executes pipeline
   - Verify all cost outputs in results

### Phase 4: Comparison Framework

8. **Create comparison visualization scripts**
   - LCOE breakdown bar charts
   - Cost driver Sankey diagrams
   - Sensitivity tornado plots

9. **Document comparison methodology**
   - Standard output naming
   - Units and currency conventions
   - ARIES-ST benchmark comparison

---

## Code/Model References

**SysMLv2 Specifications**:
- `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/SysML_IntroGuide_v2/full_document.md:195-214` - Derived attribute patterns
- `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/Cheatsheet/sysml_textual_notation_cheatsheet.md:134-135` - Specialization syntax

**agentic-mbse Validation**:
- `src/agentic_mbse/validation/runner.py:48-57` - QUALITY_CHECKS registry
- `src/agentic_mbse/validation/adr002.py:28-77` - Rule implementation pattern
- `src/agentic_mbse/sysml/syside_adapter.py:195-214` - Element iteration API

**PyFECONS Cost Structure**:
- `pyfecons/costing/calculations/lcoe.py:11-25` - LCOE formula
- `pyfecons/costing/calculations/cas70_annualized_om.py:6-19` - O&M costs
- `pyfecons/costing/mfe/cas80_annualized_fuel.py:8-41` - Fuel costs
- `pyfecons/costing/calculations/cas90_annualized_financial.py:6-19` - Financial annualization

**sysml-codegen Multi-Output**:
- `src/sysml_codegen/generation/schemas.py:103-113` - Multi-output detection
- `src/sysml_codegen/generation/modules.py:22-31` - Module generation

**teax-simkit Output Routing**:
- `simkit/core/pipeline_executor.py:196-230` - MultiOutput handling
- `simkit/io/output_router.py:250-343` - Schema registration

---

## Success Criteria Checklist

- [x] Pattern defined where explicit wiring provides auditability (Q1)
- [x] Recursive cost rollup pattern documented for any hierarchy depth (Q2)
- [x] Three enforceable rules defined with implementation approach (Q3)
- [x] Standard cost output schema defined with 25+ required outputs (Q4)
- [x] Full LCOE calculation pattern documented with all components (Q5)
- [ ] Minimal prototype validates patterns work with tooling (future)

---

## Open Questions

1. **Cost Uncertainty Modeling**: How to represent uncertainty ranges?
   - Options: (a) min/max attributes, (b) confidence factors, (c) Monte Carlo in simulation layer

2. **Learning Curves**: How to model cost reductions over deployment generations?

3. **Regional Cost Factors**: How to handle location-specific cost multipliers?

4. **Interface Validation Timing**: Should cost interface compliance be checked at parse-time or code-generation time?

---

## Addendum: Nested Calculations in Part Definitions (Empirical Validation)

**Added**: 2026-01-06 (follow-up investigation)

### Background

The original Q1 finding stated that SysMLv2 "does NOT support automatic calculation inclusion via part instantiation." This was based on prior testing of calc *usages* inside part defs. A follow-up investigation explored whether:

1. **Calc defs** can be nested inside part defs (like OOP methods on classes)
2. **Calc usages** inside part defs can have their outputs traced through to concrete values
3. The **redefinition mechanism** connects usage-level values to definition-level bindings

### Test Cases

Two test models were created to investigate these patterns:

**Case 1: Nested calc def inside part def**
`models/tests/case1_calc_def_in_partdef.sysml`

```sysml
part def 'Component' {
    attribute quantity : Integer;
    attribute unit_price : Real;

    // Nested calc DEFINITION
    calc def Cost {
        in n : Integer;
        in price : Real;
        out total : Real = n * price;
    }

    // Use the nested calc def
    calc cost_calc : Cost {
        in n = quantity;
        in price = unit_price;
    }

    // EXPOSE the calc output
    attribute total_cost : Real = cost_calc.total;
}

part my_component : 'Component' {
    :>> quantity = 12;
    :>> unit_price = 100.0;
}

// Use the exposed cost downstream
calc final_cost_with_tax {
    in base_cost = my_component.total_cost;
    in tax_rate : Real = 0.1;
    out final_cost : Real = base_cost * (1.0 + tax_rate);
}

attribute project_cost : Real = final_cost_with_tax.final_cost;
```

**Case 2: Inline calc usage inside part def**
`models/tests/case2_calc_usage_in_partdef.sysml`

```sysml
part def 'Component' {
    attribute quantity : Integer;
    attribute unit_price : Real;

    // Inline calc USAGE (anonymous)
    calc cost_calc {
        in n = quantity;
        in price = unit_price;
        return result : Real = n * price;
    }

    // EXPOSE the calc output
    attribute total_cost : Real = cost_calc.result;
}

part my_component : 'Component' {
    :>> quantity = 12;
    :>> unit_price = 100.0;
}

// Use the exposed cost downstream
calc final_cost_with_tax {
    in base_cost = my_component.total_cost;
    in tax_rate : Real = 0.1;
    out final_cost : Real = base_cost * (1.0 + tax_rate);
}

attribute project_cost : Real = final_cost_with_tax.final_cost;
```

**Result**: Both cases parse successfully with `syside check`.

### Key Findings

#### Finding 1: Nested Definitions Are Valid

syside extracts nested calc defs with proper qualified names:

```
Case 1:
  CalculationDefinition: Cost -> Case1_CalcDefInPartDef::Component::Cost
    owner: Component (PartDefinition)
  CalculationUsage: cost_calc -> Case1_CalcDefInPartDef::Component::cost_calc
    owner: Component (PartDefinition)

Case 2:
  CalculationDefinitions: (none - inline calc has no separate def)
  CalculationUsage: cost_calc -> Case2_CalcUsageInPartDef::Component::cost_calc
    owner: Component (PartDefinition)
```

#### Finding 2: Calc Usages Are Owned by PartDefinition, Not PartUsage

In both cases, the calc usage (`cost_calc`) is owned by the **PartDefinition**, not the **PartUsage**. The `my_component` part usage only contains attribute redefinitions (`quantity`, `unit_price`), not its own calc usage.

#### Finding 3: The Binding Chain Is Fully Traceable

The AST contains complete binding information from downstream calcs back to source values:

```
final_cost_with_tax.base_cost
  → FeatureChainExpression to: Component::total_cost

Component::total_cost
  → FeatureChainExpression to: Component::cost_calc::result

cost_calc.n
  → FeatureReferenceExpression to: Component::quantity

cost_calc.price
  → FeatureReferenceExpression to: Component::unit_price
```

#### Finding 4: Redefinition Connects Usage Values to Definition Bindings

This is the critical finding. When querying `my_component.features`:

```
my_component.owned_members: ['quantity', 'unit_price']  ← only overrides
my_component.features: [..., 'cost_calc', 'total_cost', ...]  ← includes inherited!
```

The `total_cost` feature is **inherited** from the type and accessible via `my_component.total_cost`.

More importantly, the redefinition mechanism provides value resolution:

```
my_component.quantity
  qualified_name: Case2_CalcUsageInPartDef::my_component::quantity
  VALUE: 12
  redefines: Case2_CalcUsageInPartDef::Component::quantity
```

The part usage's `quantity` attribute **redefines** the part definition's `quantity` attribute with value `12`. This means:

- `cost_calc.n` binds to `Component::quantity` (the definition attribute)
- `my_component::quantity` redefines `Component::quantity` with value `12`
- In the context of `my_component`, `Component::quantity` **resolves to `12`**

### Complete Resolution Path

The full traceability chain:

```
project_cost
  → final_cost_with_tax.final_cost
    → base_cost * (1.0 + tax_rate)
      → my_component.total_cost (inherited from Component)
        → cost_calc.result (owned by Component)
          → n * price
            → n = Component::quantity
                  redefined by my_component::quantity = 12
            → price = Component::unit_price
                      redefined by my_component::unit_price = 100.0
          = 12 * 100.0 = 1200
```

### Implications for Architecture

#### SysMLv2 Supports the OOP-Like Pattern

The user's intuition is correct: SysMLv2 **does** support defining calculations as "methods" of part definitions:

1. Part def defines structure + calc + exposed output attribute
2. Part usage instantiates with concrete attribute values
3. The calc output is inherited and accessible via the part usage
4. Redefinition connects usage-level values to definition-level bindings

#### Tooling Gap (Not Language Gap)

The limitation is in **tooling**, not in SysMLv2 semantics:

| Aspect | SysMLv2 Support | sysml-codegen Support |
|--------|-----------------|----------------------|
| Nested calc def in part def | YES | Extracts it |
| Calc usage in part def | YES | Extracts it |
| Binding chain in AST | YES | Follows it |
| Inheritance via `.features` | YES | Unknown |
| Redefinition resolution | YES | **Not implemented** |

sysml-codegen's `_get_parent_part_path()` function (line 407-421) only tracks `PartUsage` parents, not `PartDefinition` parents. It doesn't resolve the redefinition chain to get concrete values from part usages.

#### Recommended Tooling Enhancement

To fully support the nested calc pattern, sysml-codegen would need to:

1. **Detect calc usages owned by PartDefinitions** (not just PartUsages)
2. **Find all PartUsages that instantiate those PartDefinitions**
3. **Follow the redefinition chain**: calc input → part def attribute → part usage override value
4. **Generate pipeline with resolved bindings**

This is a tractable enhancement that aligns with MBSE principles of co-locating structure and analysis.

### Revised Recommendation

The original recommendation ("accept explicit calc wiring in design files") remains valid as a **pragmatic approach** given current tooling. However, the investigation reveals:

**Option A: Explicit Wiring (Current Recommendation)**
- Calc defs in library, calc usages in design files
- Explicit `in param = part.attribute` bindings
- Works today with existing tooling

**Option B: Nested Calc Pattern (Future Enhancement)**
- Calc def/usage inside part def
- Bindings reference parent's attributes directly
- Requires sysml-codegen enhancement to resolve redefinitions
- More aligned with OOP intuition and co-location principles

**Recommendation**: Proceed with Option A for immediate implementation. Consider Option B as a tooling enhancement once the cost modeling infrastructure is validated.

### Test Model Locations

- `models/tests/case1_calc_def_in_partdef.sysml` - Nested calc def pattern
- `models/tests/case2_calc_usage_in_partdef.sysml` - Inline calc usage pattern

Both models demonstrate the binding chain and can be used as reference for future tooling work.

---

**Last Updated**: 2026-01-06
**Related**: `project/research/20260106-050051_cost-modeling-lcoe-strategy.md`
