# Cost Modeling Guide

**Status**: Final
**Last Updated**: 2026-01-12
**Validated By**: Coffee Maker Test Model (`models/tests/coffee_maker/`)

---

## 1. Introduction

This guide codifies the validated cost modeling patterns for fusion plant techno-economic analysis (TEA). All fusion designs in this project should follow these patterns to ensure:

- Consistent cost rollup from components to system-level LCOE
- Multi-category cost visibility (material, fabrication, installation)
- Automatic aggregation across part multiplicities
- Comparable output across different fusion concepts

### Pattern A: Nested Cost Models

The validated approach is **Pattern A: Nested Cost Models**, where:

1. Parts specialize an abstract `'Costed Component'` interface
2. Leaf parts contain embedded `cost_model` calc usages that compute costs from parameters
3. Assembly parts aggregate child costs using `sum()` from the standard library
4. Design files bind concrete parameter values via redefinition (`:>>`)

This pattern co-locates structure with cost analysis, making design files clean and cost rollup automatic.

---

## 2. The Costed Component Interface

Every cost-bearing part must specialize the abstract `'Costed Component'` interface:

```sysml
abstract part def 'Costed Component' {
    // Required cost attributes
    attribute capital_cost : Real;
    attribute raw_material_cost : Real;
    attribute fabrication_cost : Real;
    attribute installation_cost : Real;

    // Derived efficiency metric
    attribute idiot_index : Real;
}
```

**Reference**: `models/tests/coffee_maker/library.sysml:19-37`

### Why This Interface?

| Attribute | Purpose |
|-----------|---------|
| `capital_cost` | Total cost for LCOE calculation |
| `raw_material_cost` | Material portion for cost driver analysis |
| `fabrication_cost` | Manufacturing labor/overhead |
| `installation_cost` | On-site assembly and integration |
| `idiot_index` | `capital_cost / raw_material_cost` - manufacturing overhead ratio |

The **idiot index** (term from SpaceX) indicates manufacturing complexity. Values of 2-4 are typical for complex engineered systems; values >5 suggest cost reduction opportunities.

### Specialization Semantics

When a part specializes `'Costed Component'`:

- It **inherits** all five attributes (they exist but are unbound)
- It **must** redefine (`:>>`) each attribute to provide values
- Failure to bind leaves the attribute unbound (no parse error, but evaluation fails)

---

## 3. Calculation Definitions

Calc definitions encapsulate cost formulas with typed inputs and outputs.

### Structure

```sysml
calc def HeatingElementCostCalc {
    // Inputs (some with defaults)
    in attribute power : Real;
    in attribute mass : Real;
    in attribute material_cost_per_kg : Real default := 50.0;
    in attribute fab_factor : Real default := 0.6;
    in attribute install_factor : Real default := 0.15;

    // Outputs (with formulas)
    out attribute material_cost : Real = mass * material_cost_per_kg;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**Reference**: `models/tests/coffee_maker/library.sysml:43-71`

### Key Principles

1. **Inputs with defaults**: Cost factors (e.g., `fab_factor = 0.6`) should have defaults based on domain knowledge. Design-specific parameters (e.g., `mass`) typically don't.

2. **Multi-category outputs**: Always provide `material_cost`, `fab_cost`, `install_cost`, and `total_cost` for downstream visibility.

3. **Idiot index**: Include as output for efficiency tracking.

4. **Topological dependencies**: Outputs can reference other outputs. Evaluation order must respect dependencies (material_cost before fab_cost before total_cost).

5. **Simple arithmetic only**: Formulas should use `+`, `-`, `*`, `/`. No conditionals or complex logic.

---

## 4. Part Definition Patterns

### 4.1 Leaf Parts (Direct Calculation)

Leaf parts compute their own cost via an embedded `cost_model` calc usage:

```sysml
part def 'Heating Element' :> 'Costed Component' {
    // Design parameters (set by usage)
    attribute power_rating : Real;
    attribute material_mass : Real;

    // Embedded cost model
    calc cost_model : HeatingElementCostCalc {
        in power = power_rating;
        in mass = material_mass;
        // Defaults not overridden - uses calc def defaults
    }

    // Expose cost outputs via redefinition
    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**Reference**: `models/tests/coffee_maker/library.sysml:226-252`

### 4.2 Assembly Parts (Aggregation)

Assembly parts aggregate costs from their children:

```sysml
part def 'Brewing System' :> 'Costed Component' {
    // Child parts
    attribute heater_count : Integer default := 2;
    part heater : 'Heating Element' [heater_count];
    part pump : 'Water Pump';
    part chamber : 'Brew Chamber';

    // Allocation model for minor items
    calc allocation_model : AllocationCostCalc {
        in child_count = 4.0;
        in total_child_mass = 0.8;
    }

    attribute misc_hardware_cost : Real = allocation_model.total_allocation;

    // AUTOMATIC aggregation using sum()
    :>> capital_cost =
        sum(heater.capital_cost) +
        pump.capital_cost +
        chamber.capital_cost +
        misc_hardware_cost;

    :>> raw_material_cost =
        sum(heater.raw_material_cost) +
        pump.raw_material_cost +
        chamber.raw_material_cost +
        allocation_model.material_portion;

    :>> fabrication_cost =
        sum(heater.fabrication_cost) +
        pump.fabrication_cost +
        chamber.fabrication_cost;

    :>> installation_cost =
        sum(heater.installation_cost) +
        pump.installation_cost +
        chamber.installation_cost;

    :>> idiot_index = capital_cost / raw_material_cost;
}
```

**Reference**: `models/tests/coffee_maker/library.sysml:384-438`

### 4.3 Allocation Costs (Rule R3)

**When to use**: Assembly-level minor items that don't warrant separate part definitions:
- Fasteners, seals, gaskets
- Wiring harnesses
- Floor stock / consumables
- Items <5% of assembly cost

```sysml
calc def AllocationCostCalc {
    in attribute child_count : Real;
    in attribute total_child_mass : Real;

    in attribute fastener_cost_per_child : Real default := 0.50;
    in attribute seal_cost_per_child : Real default := 0.30;
    in attribute wiring_cost_per_kg : Real default := 2.0;

    out attribute fastener_cost : Real = child_count * fastener_cost_per_child;
    out attribute seal_cost : Real = child_count * seal_cost_per_child;
    out attribute wiring_cost : Real = total_child_mass * wiring_cost_per_kg;
    out attribute total_allocation : Real = fastener_cost + seal_cost + wiring_cost;

    // Material portion for idiot index (80% of allocation is material)
    out attribute material_portion : Real = total_allocation * 0.8;
}
```

**Reference**: `models/tests/coffee_maker/library.sysml:195-220`

**Output treatment**: Allocation costs appear as a **separate row** in cost output with `cost_type = "allocation"`, enabling visibility into assembly overhead.

---

## 5. Multiplicity Handling

### Required Import

```sysml
private import NumericalFunctions::sum;
```

This import is **mandatory** for any model with arrayed parts. Without it, `sum()` is undefined.

### Array Declaration

```sysml
// Fixed multiplicity
part heater : 'Heating Element' [2];

// Parameterized multiplicity
attribute heater_count : Integer default := 2;
part heater : 'Heating Element' [heater_count];
```

### Aggregation

The `sum()` function automatically aggregates over all array elements:

```sysml
:>> capital_cost = sum(heater.capital_cost) + pump.capital_cost;
```

This works regardless of the array size - whether `[2]`, `[12]`, or `[heater_count]`.

### Output Schema

For arrayed parts, the output includes:
- `quantity`: Array size (e.g., 2)
- `unit_*_cost`: Per-instance cost
- `total_*_cost`: `quantity × unit_*_cost`

---

## 6. Design Instance Patterns

Design files bind concrete parameter values to part attributes.

### Dot Notation Binding

```sysml
part coffee_maker : 'Coffee Maker' {
    part redefines brewing {
        :>> heater.power_rating = 1000.0;
        :>> heater.material_mass = 0.15;
        :>> pump.flow_rate = 0.5;
        :>> chamber.volume = 0.3;
    }

    part redefines housing {
        :>> shell.surface_area = 0.15;
        :>> panel.button_count = 3.0;
    }
}
```

**Reference**: `models/tests/coffee_maker/design.sysml:15-54`

### Binding Resolution Order

When evaluating a calc input, resolution follows this precedence (highest wins):

1. **Design redefinition**: `:>> heater.power_rating = 1000.0` in design file
2. **Calc usage binding**: `in power = power_rating` in part def
3. **Calc def default**: `in attribute power : Real default := 100.0` in calc def

### Alternative: Part Redefines with Nested Bindings

```sysml
part redefines brewing {
    part redefines heater {
        :>> power_rating = 1000.0;
        :>> material_mass = 0.15;
    }
}
```

Both patterns work; dot notation is more concise for simple bindings.

---

## 7. Use Cases

### 7.1 Standard Leaf Part

A component with parameters that directly drive cost:

```sysml
part def 'TF Conductor' :> 'Costed Component' {
    attribute tape_length : Real;
    attribute current_rating : Real;

    calc cost_model : TFConductorCostCalc {
        in length = tape_length;
        in rating = current_rating;
    }

    :>> capital_cost = cost_model.total_cost;
    // ... other bindings
}
```

### 7.2 Assembly with Children

A sub-system aggregating multiple components:

```sysml
part def 'TF Coil System' :> 'Costed Component' {
    part conductor : 'TF Conductor' [12];
    part structure : 'TF Structure' [12];

    :>> capital_cost = sum(conductor.capital_cost) + sum(structure.capital_cost);
    // ... other aggregations
}
```

### 7.3 Multiplicity (Arrayed Parts)

Same pattern as 7.2 - use `sum()` for any array size.

### 7.4 Allocation Costs

See Section 4.3. Add `allocation_model` calc usage for assembly-level minor items.

### 7.5 System-Level Costing Without Sub-Component Costs

**Scenario**: You need to decompose a system for physics calculations, but only have system-level cost data from literature.

**Pattern**: Only the system specializes `'Costed Component'`; sub-components do **not**.

```sysml
// Sub-components for physics - NOT costed
part def 'TF Coil Structure' {
    // Physics-relevant attributes
    attribute n_coils : Integer;
    attribute field_strength : Real;
    attribute coil_volume : Real;
    // NO cost attributes - cost handled at system level
}

part def 'PF Coil Structure' {
    attribute n_coils : Integer;
    // ... physics attributes only
}

// System-level with cost from literature
part def 'Magnet System' :> 'Costed Component' {
    // Sub-components for physics (not costed)
    part tf_coils : 'TF Coil Structure';
    part pf_coils : 'PF Coil Structure';

    // System-level cost from research paper
    calc cost_model : MagnetSystemCostCalc {
        in B_field = tf_coils.field_strength;
        in coil_volume = tf_coils.coil_volume;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    // ... other bindings
}
```

**When to use**:
- Cost data only available at system level (AACE Class 4-5 estimates)
- Sub-component decomposition needed for physics/performance analysis
- Will refactor later when detailed cost data becomes available

**Documentation**: Add doc comment explaining the pattern:
```sysml
part def 'TF Coil Structure' {
    doc /*
    Structural definition for physics calculations.
    Cost handled at Magnet System level (no decomposed cost data available).
    */
}
```

---

## 8. Required Imports

Every cost-bearing model file should include:

```sysml
// Required for cost aggregation over multiplicities
private import NumericalFunctions::sum;

// Required for numeric types
private import ScalarValues::Real;
private import ScalarValues::Integer;
```

---

## 9. Anti-Patterns

### 9.1 Hardcoded Aggregate Values

**Wrong**:
```sysml
// BAD: Hardcoded value that drifts when components change
:>> capital_cost = 26.25;
```

**Correct**:
```sysml
// GOOD: Automatic aggregation
:>> capital_cost = sum(heater.capital_cost) + pump.capital_cost;
```

### 9.2 Missing NumericalFunctions Import

**Wrong**:
```sysml
// BAD: sum() without import
:>> capital_cost = sum(heater.capital_cost);  // Error: "No Type named 'sum' found"
```

**Correct**:
```sysml
private import NumericalFunctions::sum;
// ... now sum() works
```

### 9.3 Re-Declaring Parts in Usages

**Wrong** (causes shadowing warning):
```sysml
part brewing : 'Brewing System' {
    part heater : 'Heating Element' [2] {  // Re-declaration - BAD
        :>> power_rating = 1000.0;
    }
}
```

**Correct**:
```sysml
part brewing : 'Brewing System' {
    :>> heater.power_rating = 1000.0;  // Dot notation - GOOD
}
// OR
part brewing : 'Brewing System' {
    part redefines heater {  // Explicit redefines - GOOD
        :>> power_rating = 1000.0;
    }
}
```

### 9.4 Hybrid Parts (Direct Calc + Aggregation)

**Wrong**:
```sysml
// BAD: Mixing direct calculation with partial aggregation
part def 'Confused Assembly' :> 'Costed Component' {
    part child : 'Child Component';

    calc cost_model : SomeCalc { ... }  // Direct calculation

    :>> capital_cost = child.capital_cost + cost_model.extra_cost;  // Confusing!
}
```

**Correct**: Choose one pattern:
- **Leaf**: Direct calculation only (no costed children)
- **Assembly**: Aggregation only (+ optional allocation for minor items)

---

## 10. Validation Checklist

Before committing a cost model:

- [ ] `uv run syside check` passes with no errors
- [ ] No "member name shadows" warnings
- [ ] All leaf parts have exactly one `cost_model` calc usage
- [ ] All assemblies aggregate all costed children
- [ ] All five `'Costed Component'` attributes are bound (`:>>`)
- [ ] `NumericalFunctions::sum` is imported if arrays are used
- [ ] Cost values are reasonable (spot-check against expected)

---

## 11. References

### Test Model
- `models/tests/coffee_maker/library.sysml` - Calc defs, part defs with nested cost models
- `models/tests/coffee_maker/design.sysml` - Design instance with parameter bindings
- `models/tests/coffee_maker/expected_output.csv` - Expected cost output (14 columns)
- `models/tests/coffee_maker/generate_costs.py` - Reference evaluation script

### Research Documents
- `project/research/20260107-final-cost-architecture.md` - Architecture rationale
- `project/research/20260110-strategic-cost-patterns.md` - Standardization decisions (Rules R1-R4)
- `project/research/20260112-055807_multiplicity-cost-rollup-gap.md` - NumericalFunctions::sum solution

### Standard Library
- `NumericalFunctions.kerml` - `sum`, `product`, `abs`, `max`, `min`
- `ScalarValues.kerml` - `Real`, `Integer`, `Boolean`
