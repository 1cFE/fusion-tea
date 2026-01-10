---
date: 2026-01-06T05:00:51-08:00
researcher: Claude
topic: "Cost Modeling and LCOE Strategy for Fusion TEA"
tags: [research, strategy, cost-modeling, lcoe, sysml-codegen, teax-simkit]
status: complete
last_updated: 2026-01-06
---

# Research: Cost Modeling and LCOE Strategy for Fusion TEA

**Date**: 2026-01-06 05:00 PST
**Researcher**: Claude
**Research Type**: Strategic Integration (Codebase + Architecture + Domain)

## Research Question

How should we structure cost modeling in SysMLv2 to enable:
1. Projecting long-range LCOE floors (<1c/kWh potential)
2. Reliable cost estimation across fusion concepts
3. Lifecycle/replacement cost modeling
4. Transparent LCOE breakdowns for design comparison
5. Integration with sysml-codegen and teax-simkit for execution

## Summary

- **Cost rollups require structured patterns**: Use hierarchical calc defs with explicit aggregation, not implicit summation
- **Multi-output is native in sysml-codegen**: The framework supports 2+ output attributes per calc def, generating `MultiOutput` containers
- **teax-simkit captures all exit points**: Every output channel becomes visible in results, enabling breakdown analysis
- **Three strategic approaches identified**: (1) Hierarchical rollup calcs, (2) Cost interface pattern, (3) Category-based tagging
- **Key insight**: Structure models to expose intermediate values, not just final LCOE, for sensitivity and comparison

---

## Detailed Findings

### 1. PyFECONS Cost Architecture (Reference Baseline)

**Source**: `/home/reid/PyFECONS/pyfecons/`

PyFECONS implements a hierarchical Cost Account Structure (CAS) following ARPA-E standards:

```
CAS10 - Pre-Construction Costs
CAS20 - Direct Capital Cost (aggregates CAS21-29)
  CAS21 - Buildings & Infrastructure
  CAS22 - Reactor Plant Equipment (~60% of cost)
    CAS220101 - Reactor Equipment (vessel, blanket)
    CAS220102 - Shield
    CAS220103 - Magnets (TF, CS, PF)
    CAS220104-220119 - Supporting systems, scheduled replacement
  CAS23-29 - Other Plant Systems
CAS30-60 - Indirect, Owner's, Financial Costs
CAS70 - Annualized O&M
CAS80 - Annualized Fuel (Tritium)
CAS90 - Annualized Financial Charges
LCOE - Final Output ($/MWh)
```

**LCOE Formula**:
```
LCOE = [C90 + (C70+C80)*(1+inflation)^lifetime] / [8760*p_net*availability]
```

**Key Observation**: PyFECONS maintains visibility to ALL intermediate cost accounts. This is critical for sensitivity analysis and design comparison.

### 2. sysml-codegen Multi-Output Architecture

**Source**: `/home/reid/1cfe/sysml-codegen/src/sysml_codegen/generation/`

The code generator natively supports multi-output calculations:

**modules.py:22-31** - Multi-output detection:
```python
def is_multioutput(calc_def: CalculationDefinitionData) -> bool:
    """Determine if calc def has multiple outputs."""
    return len(calc_def.output_attributes) >= 2
```

**schemas.py:103-113** - Multi-output model generation:
```python
def should_use_multioutput(calc_def: CalculationDefinitionData) -> bool:
    output_attrs = calc_def.output_attributes
    return len(output_attrs) >= 2
```

**Generated Output**: For a calc def with 2+ outputs, generates:
1. `{CalcName}Output` Pydantic model with all output fields
2. `{CalcName}Module` that returns the multi-output container
3. Pipeline YAML with separate channels for each output

**Example**: A PowerBalanceCalc with 16 outputs becomes:
- `PowerBalanceCalcOutput` with `p_alpha`, `p_neutron`, `p_net`, `q_eng`, etc.
- Each output is a separate channel in the pipeline
- All 16 values visible in results

### 3. teax-simkit Exit Point Architecture

**Source**: `/home/reid/1cfe/teax/packages/teax-simkit/simkit/core/`

**pipeline_executor.py:196-230** - Multi-output handling:
```python
# Check if module returned MultiOutput container (new pattern)
if isinstance(data, MultiOutput):
    # Multi-output mode - extract fields from MultiOutput container
    channel_dict = data.to_channel_dict()
    for field, binding in outputs.items():
        context.set_channel(binding.channel_name, channel_dict[field])
```

**pipeline.py:196-227** - Exit point captures ALL outputs:
```python
def _build_exit_points(modules: list[PipelineModule]) -> list[dict]:
    """Build exit point context for template.
    Exit points capture all module outputs for pipeline results."""
    exit_points = []
    for module in modules:
        for out in module.outputs:
            exit_points.append({
                "name": out.channel_name,
                "type": output_type,
            })
    return exit_points
```

**Key Insight**: Every output attribute from every calc becomes a visible channel in the final results. This is exactly what we need for LCOE breakdown visibility.

### 4. SysMLv2 Patterns for Cost Modeling

Based on project conventions (MODELING_GUIDE.md) and SysMLv2 patterns research:

#### Pattern A: Hierarchical Rollup Calculations

**Library Definition** (`models/library/calculations/costing.sysml`):
```sysml
calc def SubsystemCostRollup {
    doc /*
    Aggregates component costs to subsystem level
    **Source**: PyFECONS costing pattern
    */

    // Individual component costs
    in attribute blanket_cost : Real;
    in attribute shield_cost : Real;
    in attribute magnet_cost : Real;
    in attribute divertor_cost : Real;

    // Subtotals (exposed for visibility)
    out attribute reactor_equipment_cost : Real =
        blanket_cost + shield_cost + magnet_cost + divertor_cost;

    // Category breakdown (for comparison)
    out attribute structural_fraction : Real =
        (blanket_cost + shield_cost) / reactor_equipment_cost;
    out attribute magnet_fraction : Real =
        magnet_cost / reactor_equipment_cost;
}
```

**Design Usage** (`models/designs/catf/cost_analysis.sysml`):
```sysml
calc subsystem_costs : SubsystemCostRollup {
    in blanket_cost = blanket_system.cost;
    in shield_cost = shield_system.cost;
    in magnet_cost = magnet_system.cost;
    in divertor_cost = divertor_system.cost;
}

// EXPOSE all outputs for pipeline visibility
attribute cas22_cost : Real = subsystem_costs.reactor_equipment_cost;
attribute structural_fraction : Real = subsystem_costs.structural_fraction;
attribute magnet_fraction : Real = subsystem_costs.magnet_fraction;
```

#### Pattern B: Cost Interface (Cross-Cutting Concern)

**Library Definition** (`models/library/definitions/costed_component.sysml`):
```sysml
abstract part def 'Costed Component' {
    doc /*
    Base definition for cost-bearing components.
    All major subsystems should specialize this.
    */

    // Every costed component exposes these
    attribute capital_cost : Real;
    attribute annual_operating_cost : Real;
    attribute replacement_interval_years : Real;
    attribute replacement_cost : Real;
}
```

**Specialization**:
```sysml
part def 'First Wall' :> 'Costed Component' {
    doc /*
    First wall with frequent replacement
    **Source**: PyFECONS CAS220119
    */

    // Override with specific values in design
    :>> replacement_interval_years = 5.0;
}
```

#### Pattern C: Lifecycle Cost Calculation

**Library Definition** (`models/library/calculations/lifecycle.sysml`):
```sysml
calc def LifecycleCostCalc {
    doc /*
    Calculates total lifecycle cost including replacements
    **Source**: PyFECONS annualized cost methodology
    */

    in attribute capital_cost : Real;           // Initial cost [$M]
    in attribute annual_opex : Real;            // $/year
    in attribute replacement_cost : Real;       // Per replacement [$M]
    in attribute replacement_interval : Real;   // Years
    in attribute plant_lifetime : Real;         // Years
    in attribute discount_rate : Real;          // Annual rate

    // Intermediate values (exposed for visibility)
    out attribute num_replacements : Real =
        (plant_lifetime / replacement_interval) - 1.0;

    out attribute total_replacement_cost : Real =
        replacement_cost * num_replacements;

    out attribute total_opex : Real =
        annual_opex * plant_lifetime;

    // NPV calculation (simplified)
    out attribute lifecycle_npv : Real =
        capital_cost + total_replacement_cost + total_opex;
}
```

#### Pattern D: LCOE Master Calculation with Full Breakdown

**Library Definition** (`models/library/calculations/lcoe.sysml`):
```sysml
calc def LCOECalculation {
    doc /*
    Master LCOE calculation with full breakdown visibility

    Exposes all intermediate values for:
    - Sensitivity analysis
    - Design comparison
    - Cost driver identification

    **Source**: PyFECONS LCOE methodology
    */

    // === CAPITAL COST INPUTS (by CAS category) ===
    in attribute cas21_buildings : Real;
    in attribute cas22_reactor : Real;
    in attribute cas23_turbine : Real;
    in attribute cas24_electric : Real;
    in attribute cas25_heat_rejection : Real;
    in attribute cas26_misc : Real;
    in attribute cas27_special_materials : Real;

    // === INDIRECT COSTS ===
    in attribute cas30_indirect_factor : Real;
    in attribute cas40_owners_factor : Real;
    in attribute cas50_financial_factor : Real;

    // === OPERATING COSTS ===
    in attribute annual_om : Real;       // CAS70
    in attribute annual_fuel : Real;     // CAS80

    // === FINANCIAL PARAMETERS ===
    in attribute discount_rate : Real;
    in attribute plant_lifetime : Real;
    in attribute inflation_rate : Real;

    // === POWER OUTPUT ===
    in attribute p_net : Real;           // MW
    in attribute availability : Real;    // Capacity factor

    // === INTERMEDIATE OUTPUTS (for visibility) ===

    // Direct capital subtotal
    out attribute cas20_direct : Real =
        cas21_buildings + cas22_reactor + cas23_turbine +
        cas24_electric + cas25_heat_rejection + cas26_misc +
        cas27_special_materials;

    // Indirect costs
    out attribute cas30_indirect : Real = cas20_direct * cas30_indirect_factor;
    out attribute cas40_owners : Real = cas20_direct * cas40_owners_factor;
    out attribute cas50_financial : Real = cas20_direct * cas50_financial_factor;

    // Total capital
    out attribute total_capital : Real =
        cas20_direct + cas30_indirect + cas40_owners + cas50_financial;

    // Annualized financial (CAS90)
    out attribute cas90_annualized : Real =
        total_capital * discount_rate /
        (1.0 - (1.0 / ((1.0 + discount_rate) ** plant_lifetime)));

    // Total annual cost
    out attribute total_annual : Real =
        cas90_annualized + annual_om + annual_fuel;

    // Annual energy production
    out attribute annual_energy_mwh : Real =
        p_net * 8760.0 * availability;

    // === FINAL LCOE ===
    out attribute lcoe : Real =
        total_annual / annual_energy_mwh;

    // === BREAKDOWN METRICS (for comparison) ===
    out attribute capital_lcoe_fraction : Real =
        cas90_annualized / total_annual;
    out attribute om_lcoe_fraction : Real =
        annual_om / total_annual;
    out attribute fuel_lcoe_fraction : Real =
        annual_fuel / total_annual;

    // Cost per kW (for comparison across scales)
    out attribute overnight_cost_per_kw : Real =
        total_capital * 1000.0 / p_net;
}
```

### 5. Strategic Recommendations

#### Recommendation 1: Expose ALL Intermediate Cost Values

**Rationale**: sysml-codegen and teax-simkit natively support multi-output. Every `out attribute` becomes a visible channel in results. Leverage this for full transparency.

**Implementation**:
- Define calc defs with 10-20 outputs each (inputs, subtotals, breakdowns)
- Never aggregate to single LCOE without exposing components
- Use descriptive names: `cas22_reactor_cost`, `magnet_fraction`, `overnight_cost_per_kw`

**Generated Pipeline Example**:
```yaml
exit_point:
  outputs:
    - name: lcoe
      channel: lcoe_calc.lcoe
    - name: capital_lcoe_fraction
      channel: lcoe_calc.capital_lcoe_fraction
    - name: overnight_cost_per_kw
      channel: lcoe_calc.overnight_cost_per_kw
    - name: cas22_reactor_cost
      channel: subsystem_costs.reactor_equipment_cost
    # ... all 30+ cost metrics visible
```

#### Recommendation 2: Enforce Cost Interface Pattern

**Rationale**: Consistent cost attributes across all components enables automated rollup and comparison.

**Implementation**:
```sysml
// Every cost-bearing component implements this interface
abstract part def 'Costed Component' {
    attribute capital_cost : Real;
    attribute annual_opex : Real;
    attribute replacement_cost : Real;
    attribute replacement_years : Real;
}
```

**Enforcement**: Document in MODELING_GUIDE that all subsystem part defs MUST specialize `'Costed Component'`.

#### Recommendation 3: Category-Based Cost Aggregation

**Rationale**: Enable comparison across concepts by consistent categories.

**Implementation**: Create standard calc defs for each CAS category:
- `CAS21BuildingsCostCalc`
- `CAS22ReactorCostCalc`
- `CAS23TurbineCostCalc`
- etc.

Each calc def follows same pattern: inputs → subtotals → fractions → total.

#### Recommendation 4: Lifecycle Cost as First-Class Concern

**Rationale**: OpEx drivers (replacement, maintenance) significantly impact LCOE.

**Implementation**:
```sysml
calc def ComponentLifecycleCost {
    in capital_cost : Real;
    in replacement_cost : Real;
    in replacement_interval : Real;
    in plant_lifetime : Real;
    in discount_rate : Real;

    // NPV of all replacements
    out npv_replacements : Real;

    // Annualized replacement cost
    out annualized_replacement : Real;
}
```

Apply to high-replacement components: first wall, divertor, blanket modules.

#### Recommendation 5: Design Comparison Framework

**Rationale**: Goal is comparing fusion concepts, not just single LCOE numbers.

**Implementation**: Structure designs to produce standardized comparison outputs:

```sysml
// Every design exposes these standard metrics
part fusion_plant {
    // Core LCOE
    attribute lcoe : Real;

    // Breakdown by category (for stacked bar charts)
    attribute lcoe_capital : Real;
    attribute lcoe_om : Real;
    attribute lcoe_fuel : Real;

    // Breakdown by subsystem (for Sankey diagrams)
    attribute cost_magnets : Real;
    attribute cost_blanket : Real;
    attribute cost_structure : Real;
    attribute cost_bop : Real;

    // Scalability metrics
    attribute overnight_cost_per_kw : Real;
    attribute specific_power_mw_per_m3 : Real;

    // Risk/uncertainty
    attribute cost_confidence : Real;
}
```

### 6. Integration Architecture

#### Data Flow: SysML → Code → Results

```
SysMLv2 Models (models/)
    │
    ├── library/calculations/
    │   ├── power_balance.sysml      → PowerBalanceCalcDT (16 outputs)
    │   ├── geometry.sysml           → RadialBuildCalc (10 outputs)
    │   ├── costing/
    │   │   ├── blanket.sysml        → BlanketCostCalc (5 outputs)
    │   │   ├── magnets.sysml        → MagnetCostCalc (8 outputs)
    │   │   └── lcoe.sysml           → LCOECalculation (20 outputs)
    │   └── lifecycle.sysml          → LifecycleCostCalc (6 outputs)
    │
    └── designs/catf/
        └── plant.sysml              → Wire all calcs, EXPOSE outputs
            │
            ▼
    sysml-codegen --models models/ --output generated/ --package-name fusion_tea
            │
            ├── generated/modules/
            │   ├── power_balance_calc_dt_module.py
            │   ├── lcoe_calculation_module.py
            │   └── ... (20+ modules)
            │
            ├── generated/schemas/
            │   ├── power_balance_calc_dt_output.py  (16 fields)
            │   ├── lcoe_calculation_output.py       (20 fields)
            │   └── ... (multi-output schemas)
            │
            └── generated/pipeline.yaml
                │
                ▼
    teax-simkit execute_pipeline(
        "generated/pipeline.yaml",
        "results/catf_run1/",
        registry=fusion_tea.create_registry(),
        custom_schema_types=[LCOECalculationOutput, ...]
    )
                │
                ▼
    results/catf_run1/
        ├── lcoe.json                    # Final LCOE: 4.2 c/kWh
        ├── lcoe_capital_fraction.json   # Capital: 65%
        ├── overnight_cost_per_kw.json   # $3,200/kW
        ├── cas22_reactor_cost.json      # $1.8B
        └── ... (50+ output channels)
```

#### Comparison Workflow

```python
# Run multiple designs
catf_results = execute_pipeline("catf/pipeline.yaml", "results/catf/")
stellarator_results = execute_pipeline("stellarator/pipeline.yaml", "results/stellarator/")
mirror_results = execute_pipeline("mirror/pipeline.yaml", "results/mirror/")

# Compare standardized outputs
comparison = {
    "CATF": {
        "lcoe": catf_results.outputs["lcoe"],
        "capital_fraction": catf_results.outputs["lcoe_capital_fraction"],
        "magnet_cost": catf_results.outputs["cost_magnets"],
    },
    "Stellarator": { ... },
    "Mirror": { ... },
}

# Generate comparison visualizations
plot_lcoe_breakdown(comparison)
plot_cost_sankey(comparison)
plot_sensitivity_tornado(catf_results, ["p_net", "availability", "magnet_cost"])
```

### 7. Answering the Original Questions

#### Q1: How to ensure "cost" is modeled reliably across the system?

**Answer**: Use the **Costed Component Interface Pattern**:
1. Define `abstract part def 'Costed Component'` with standard cost attributes
2. All cost-bearing components specialize this definition
3. Calc defs for rollup explicitly bind to these standard attributes
4. Enforce via MODELING_GUIDE documentation and audit

#### Q2: Do we require all models have a capital cost? Do we enforce rules?

**Answer**: Yes, enforce via convention:
- All subsystem part defs MUST specialize `'Costed Component'`
- MODELING_GUIDE documents required attributes
- `/audit-models` validates interface compliance
- Missing costs generate validation warnings

#### Q3: How to model lifecycle/replacement rate?

**Answer**: Use **Lifecycle Cost Calc Pattern**:
1. Each component has `replacement_interval` and `replacement_cost` attributes
2. `LifecycleCostCalc` computes NPV and annualized replacement
3. High-replacement components (first wall, divertor) explicitly modeled
4. Results include `annualized_replacement_cost` output for visibility

#### Q4: How does this translate to top-level LCOE with visibility?

**Answer**: **Multi-output calc defs** naturally provide visibility:
1. `LCOECalculation` has 20+ outputs (all intermediate values)
2. sysml-codegen generates `LCOECalculationOutput` with all fields
3. teax-simkit exposes every output as separate channel
4. Results include full breakdown: `lcoe`, `capital_fraction`, `overnight_cost_per_kw`, etc.

#### Q5: How to COMPARE different designs?

**Answer**: **Standardized output interface** across all designs:
1. Every design exposes same set of comparison metrics
2. Run each design through same pipeline structure
3. Results are directly comparable (same field names, same units)
4. Visualizations: stacked bars, Sankey diagrams, tornado plots

---

## Implementation Roadmap

### Phase 1: Cost Infrastructure (Immediate)

1. Create `models/library/definitions/costed_component.sysml`
   - Define `abstract part def 'Costed Component'`
   - Document in MODELING_GUIDE

2. Create `models/library/calculations/costing/` directory:
   - `subsystem_rollup.sysml` - Aggregation calcs
   - `lifecycle.sysml` - Lifecycle cost calcs

### Phase 2: LCOE Calculation (After Cost Infrastructure)

1. Create `models/library/calculations/lcoe.sysml`
   - Full breakdown with 15-20 outputs
   - All intermediate values exposed

2. Update CATF design to wire cost calcs

### Phase 3: Comparison Framework (After LCOE Working)

1. Define standard comparison output interface
2. Create visualization tooling (Python scripts)
3. Document comparison methodology

### Phase 4: Additional Concepts (After Framework Validated)

1. Apply patterns to stellarator, mirror, IFE designs
2. Validate cross-concept comparison
3. Sensitivity analysis tooling

---

## Code/Model References

**sysml-codegen**:
- `src/sysml_codegen/generation/modules.py:22-31` - Multi-output detection
- `src/sysml_codegen/generation/schemas.py:103-113` - Multi-output model generation
- `src/sysml_codegen/generation/pipeline.py:196-227` - Exit point generation

**teax-simkit**:
- `simkit/core/pipeline_executor.py:196-230` - Multi-output handling
- `simkit/core/pipeline.py:71-213` - Pipeline execution

**PyFECONS** (reference):
- `pyfecons/costing/mfe/PowerBalance.py` - Power balance calculation
- `pyfecons/costing/categories/` - Cost account structure

**FusionTEA Current State**:
- `models/library/foundation.sysml` - Package structure, enums
- `models/library/calculations/power_balance.sysml` - PowerBalanceCalc (16 outputs already)

---

## Open Questions

1. **Cost uncertainty modeling**: How to represent uncertainty ranges? Options: (a) min/max attributes, (b) confidence factors, (c) Monte Carlo in simulation layer
2. **Learning curves**: How to model cost reductions over deployment generations?
3. **Regional cost factors**: How to handle location-specific cost multipliers?

---

## Addendum: Architectural Tension - Calc Location vs. Structure Co-location

**Added**: 2026-01-06 (follow-up discussion)

### The Core Problem

The patterns in Section 4 are **complementary layers**, not alternatives:

| Pattern | Role | When Used |
|---------|------|-----------|
| **B: Cost Interface** | Foundation | Define once in library. All cost-bearing parts specialize it. |
| **A: Hierarchical Rollup** | Aggregation | Multiple calc defs that sum component costs → subsystem → system |
| **C: Lifecycle Cost** | Time-aware | Applied to high-replacement components (first wall, divertor) |
| **D: LCOE Master** | Top-level | One calc def that takes all inputs and produces final LCOE + breakdown |

However, a fundamental architectural tension exists between:

1. **Structural composition** (naturally defined in design files)
2. **Cost calculations** (must be calc defs, currently required in library)

### The Tension Illustrated

```
┌─────────────────────────────────────────────────────────────┐
│  STRUCTURAL COMPOSITION    ←→    COST COMPUTATION           │
│  (naturally in design)           (must be calc def in lib)  │
│                                                             │
│  Design knows: "12 TF coils"     Library knows: "formula"   │
│  Design knows: "this assembly"   Library knows: "how to sum"│
│                                                             │
│  These SHOULD be co-located for auditability                │
│  But our rules force them apart                             │
└─────────────────────────────────────────────────────────────┘
```

**Key insight from discussion**: The natural place for cost rollup is wherever the structure is defined. If an assembly of 5 parts is defined in a particular location, the cost rollup for that assembly should be co-located - not scattered in a separate file.

### Hierarchical Cost Responsibility

**Recommendation**: Each part captures only its OWN costs (materials, manufacturing), and rollup is done explicitly:

```sysml
// Each part knows its own cost, NOT its children's costs
part def 'TF Coil' :> 'Costed Component' {
    // Cost of ONE coil (conductor, winding, structure)
    attribute capital_cost : Real;
}

// Assembly explicitly calculates rollup
part magnet_system {
    part tf_coils : 'TF Coil' [12];
    attribute assembly_cost : Real = 50.0;  // Integration labor

    // Rollup is EXPLICIT
    calc tf_cost_calc : MultiplyAndAdd {
        in unit_cost = tf_coils.capital_cost;
        in quantity = 12;
        in adder = assembly_cost;
    }
    attribute capital_cost : Real = tf_cost_calc.total;
}
```

**Why incremental (not rollup) at part level?**
- Avoids double-counting
- Clear traceability (where did this cost come from?)
- Flexible (different designs can compose differently)

### Proposed Alternative: Part Defs Own Their Cost Models

**Alternative A** (most aligned with MBSE practice): Each part def in library includes both its structure AND its cost calculation:

```sysml
// Library: part def with embedded cost model
part def 'Magnet System' :> 'Costed Component' {
    // === STRUCTURAL PARAMETERS (set by design) ===
    attribute num_tf_coils : Integer;
    attribute num_pf_coils : Integer;

    // === CHILD PARTS ===
    part tf_coils : 'TF Coil' [num_tf_coils];
    part pf_coils : 'PF Coil' [num_pf_coils];

    // === COST CALCULATION (co-located with structure) ===
    calc cost_model : MagnetSystemCostCalc {
        in tf_count = num_tf_coils;
        in tf_unit_cost = tf_coils.capital_cost;
        in pf_count = num_pf_coils;
        in pf_unit_cost = pf_coils.capital_cost;
    }

    // === INTERFACE COMPLIANCE ===
    :>> capital_cost = cost_model.total_cost;
}
```

**Benefits**:
- Cost and structure co-located (auditable!)
- Design is clean - just parameter values
- Each part def is self-documenting for cost

### Open Question: Does sysml-codegen Support This?

**The key question**: When sysml-codegen extracts calculation usages, does it find calc usages that are:
1. Inside part usages in design files? → **YES** (confirmed by prior work)
2. Inside part definitions in library files? → **UNKNOWN**

**Extraction process** (`usage_extractor.py:155`):
```python
for elem in SysideAdapter.elements_of_type(model, "CalculationUsage"):
```

This traverses the entire AST. The question is whether syside instantiates nested calc usages when a part def containing them is instantiated as a part usage.

**Two possibilities**:

1. **If syside instantiates nested elements**: When `part magnets : 'Magnet System'` is parsed, syside creates a `CalculationUsage` for `magnets.cost_model`. sysml-codegen would find it automatically. **No tooling changes needed.**

2. **If syside only references the definition**: The AST only contains the `CalculationUsage` in the part def template, not in instances. sysml-codegen would generate a module for the template, not instances. **Tooling enhancement needed** to resolve definition→usage relationships.

### Test Required

A minimal test case should determine the actual behavior:

```sysml
// Library: models/tests/lib_calc_in_partdef.sysml
package TestLibrary {
    calc def SimpleCalc {
        in attribute x : Real;
        out attribute y : Real = x * 2.0;
    }

    part def PartWithEmbeddedCalc {
        attribute input_value : Real;
        calc embedded : SimpleCalc {
            in x = input_value;
        }
        attribute output_value : Real = embedded.y;
    }
}

// Design: models/tests/design_uses_partdef.sysml
package TestDesign {
    import TestLibrary::*;

    part test_instance : PartWithEmbeddedCalc {
        :>> input_value = 5.0;
    }
}
```

Run sysml-codegen and check if it discovers a `CalculationUsage` for `test_instance.embedded`.

### Implications for Implementation

**If syside DOES instantiate nested calcs** (optimistic case):
- Alternative A works as-is
- Part defs can embed their cost calcs
- Clean architecture with co-located structure and cost

**If syside does NOT instantiate** (pessimistic case):
- Need tooling enhancement to sysml-codegen
- Or accept separation of structure (design) and calcs (design, but separate)
- Or use template-based approach where library defines standard assemblies

### Prior Art Reference

The existing `fusion_modeling` project uses calc usages inside part usages (not part defs):

**`fusion_modeling/models/designs/catf_mfe/system.sysml:199-204`**:
```sysml
part catf_mfe_plant {
    // Calc usage inside a part USAGE (in design file)
    calc auxiliary_load : AuxiliarySystemsPower {
        in gross_electric = 1546.72;
    }
    attribute auxiliary_power : Real = auxiliary_load.auxiliary_power;
}
```

This works because `catf_mfe_plant` is a part usage (instance), not a part definition (template).

---

## Addendum 2: Semantic Cost Models (Final Resolution)

**Added**: 2026-01-06 (follow-up discussion)

### Key Insight: "Dumb Math" vs. "Semantic Cost Models"

The earlier discussion about `MultiplyAndAdd` revealed the real issue: **abstraction granularity**.

**Wrong approach** - Generic math wrappers:
```sysml
// BAD: meaningless abstraction
calc def MultiplyAndAdd {
    in a : Real; in b : Real; in c : Real;
    out result : Real = a * b + c;
}
```

**Correct approach** - Semantic cost models:
```sysml
// GOOD: encodes domain knowledge
calc def TFCoilSystemCost {
    doc /* Cost model for TF coil system per PyFECONS */

    in conductor_volume : Real;
    in structure_volume : Real;
    in n_coils : Integer;
    in conductor_cost_per_m3 : Real;
    in structure_cost_per_m3 : Real;
    in manufacturing_complexity : Real = 3.5;

    out material_cost : Real = ...;
    out manufacturing_cost : Real = ...;
    out total_cost : Real = ...;
    out material_fraction : Real = ...;
}
```

### Resolved Pattern

1. **Library contains paired definitions**:
   - Part def (structure): `'TF Coil System'` with attributes
   - Cost calc def (model): `TFCoilSystemCost` with matching inputs

2. **Part defs expose cost-relevant attributes** that the corresponding calc def needs

3. **Designs wire part instances to cost calc instances** - acceptable because:
   - Wiring is mechanical (name-matching)
   - Cost model logic stays in library
   - Calc def is semantically meaningful

### Test Result: syside Behavior Confirmed

**Test executed**: `models/tests/lib_calc_in_partdef.sysml` + `design_uses_partdef.sysml`

**Finding**: syside does NOT instantiate nested calc usages. When a part def containing a calc usage is instantiated:
- sysml-codegen finds the calc usage in the **part definition template**
- It does NOT create a new calc usage for the **part instance**

**Implication**: Calc usages must be explicit in design files. The pattern of "part def owns its cost model via embedded calc usage" requires tooling enhancement.

### Open Questions for Follow-Up Research

The semantic cost model pattern resolves the "dumb math" problem but raises new questions:

1. **Single instantiation**: Can we design patterns where instantiating ONE top-level part guarantees all costs are calculated? (Avoid redundant calc wiring in design)

2. **Scalable/recursive patterns**: What patterns ensure cost calculations scale with structural hierarchy? (If I add a sub-component, does cost automatically include it?)

3. **Enforcement via tooling**: Can `agentic-mbse` checking scripts validate that:
   - Every part def has a corresponding cost calc def?
   - Cost calc inputs match part def attributes?
   - All cost-bearing parts are wired to cost calcs?

4. **Output structure for comparability**: Can we enforce a standard cost output schema so different fusion designs produce directly comparable results?

5. **Beyond CapEx**: How does this pattern extend to:
   - OpEx (O&M costs)
   - Lifecycle costs (replacements, decommissioning)
   - Full LCOE calculation
   - Sensitivity metrics

**Recommendation**: Conduct follow-up research to address these questions before implementing cost modeling infrastructure.

---

**Last Updated**: 2026-01-06
