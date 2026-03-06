---
date: 2026-01-07T09:30:00-08:00
researcher: Claude
topic: "Final Cost Architecture for Fusion TEA"
tags: [research, cost-modeling, sysmlv2, architecture, lcoe, synthesis, tooling]
status: complete
last_updated: 2026-01-07
---

# Research: Final Cost Architecture for Fusion TEA

**Date**: 2026-01-07 09:30 PST (updated 10:15 PST)
**Researcher**: Claude
**Research Type**: Architecture Synthesis (SysMLv2 + Tooling + Domain)

## Research Question

How should we architect cost modeling in SysMLv2 to enable:
1. Nested cost models where parts "know" their own cost
2. Recursive parametric rollups (e.g., bike cost = frame + 2*wheels + assembly)
3. Full LCOE calculation with visibility into cost drivers
4. Cross-concept comparison of different fusion designs

This synthesizes all prior research and provides the **final recommended architecture**.

---

## Summary

- **Nested cost models are the correct pattern**: Parts should contain their own cost calc usages, co-locating structure with analysis. This is cleaner, scales better, and reduces error risk.
- **SysMLv2 fully supports this pattern**: Redefinition (`:>>`) correctly propagates values from part usages through calculation bindings. Test models validate parsing.
- **Tooling upgrade required**: sysml-codegen needs enhancement to instantiate calc usages per PartUsage when they're defined in PartDefinitions. This is tractable.
- **Recursive rollups work via attribute propagation**: Each part exposes `capital_cost`, parent parts sum child costs, propagation is automatic.
- **Multi-output is fully supported**: sysml-codegen and teax-simkit natively support 20+ outputs per calc, enabling full LCOE breakdown visibility.

---

## The Bike Example - Validating Your Intuition

Your example of nested cost models is exactly right. Here's how it works in SysMLv2:

### Pattern: Hierarchical Cost Rollup

```sysml
// === LIBRARY DEFINITIONS ===

abstract part def 'Costed Component' {
    attribute capital_cost : Real;
}

part def Hub :> 'Costed Component' {
    attribute mass : Real;
    attribute cost_per_kg : Real = 5.0;
    :>> capital_cost = mass * cost_per_kg;
}

part def Tire :> 'Costed Component' {
    attribute diameter : Real;
    attribute cost_per_cm : Real = 0.10;
    :>> capital_cost = diameter * cost_per_cm;
}

part def Wheel :> 'Costed Component' {
    attribute hub_mass : Real;
    attribute tire_diameter : Real;

    // Child parts with derived costs
    part hub : Hub { :>> mass = hub_mass; }
    part tire : Tire { :>> diameter = tire_diameter; }

    // Wheel cost = sum of child costs (automatic via propagation)
    :>> capital_cost = hub.capital_cost + tire.capital_cost;
}

part def Frame :> 'Costed Component' {
    attribute length : Real;
    attribute material_cost_per_m : Real = 50.0;
    :>> capital_cost = length * material_cost_per_m;
}

part def Bike :> 'Costed Component' {
    // Design parameters
    attribute frame_length : Real;
    attribute wheel_hub_mass : Real;
    attribute wheel_tire_diameter : Real;
    attribute assembly_cost : Real = 20.0;

    // Child parts
    part frame : Frame { :>> length = frame_length; }
    part front_wheel : Wheel {
        :>> hub_mass = wheel_hub_mass;
        :>> tire_diameter = wheel_tire_diameter;
    }
    part rear_wheel : Wheel {
        :>> hub_mass = wheel_hub_mass;
        :>> tire_diameter = wheel_tire_diameter;
    }

    // Bike cost = frame + 2*wheels + assembly
    :>> capital_cost =
        frame.capital_cost +
        front_wheel.capital_cost +
        rear_wheel.capital_cost +
        assembly_cost;
}

// === DESIGN USAGE ===
part my_bike : Bike {
    :>> frame_length = 1.5;        // meters
    :>> wheel_hub_mass = 0.3;      // kg
    :>> wheel_tire_diameter = 60.0; // cm
    :>> assembly_cost = 25.0;      // dollars
}
// Result: my_bike.capital_cost = (1.5*50) + 2*(0.3*5 + 60*0.10) + 25
//                              = 75 + 2*(1.5 + 6.0) + 25
//                              = 75 + 15 + 25 = 115
```

**Key insight**: The cost rollup is "automatic" via SysMLv2's attribute propagation. When `my_bike.frame_length = 1.5`, this propagates through:
1. `frame.length = 1.5`
2. `frame.capital_cost = 1.5 * 50.0 = 75.0`
3. `my_bike.capital_cost` includes `frame.capital_cost` in its sum

### Why This Works

SysMLv2's **redefinition semantics** propagate values through the hierarchy:
- `:>> attribute = value` creates a binding that follows the value chain
- Derived attributes recalculate when their inputs change
- The pattern is truly recursive - works at any depth

---

## Why Nested Cost Models Are Better

### Pattern Comparison

**Pattern A: Nested Cost Model (Recommended)**
```sysml
// === LIBRARY ===
part def 'Magnet System' :> 'Costed Component' {
    attribute field_strength : Real;
    attribute coil_volume : Real;

    // Cost model CO-LOCATED with structure
    calc cost_model : MagnetSystemCostCalc {
        in field = field_strength;
        in volume = coil_volume;
    }

    :>> capital_cost = cost_model.total;
}

// === DESIGN (clean!) ===
part catf_plant {
    part magnets : 'Magnet System' {
        :>> field_strength = 12.0;
        :>> coil_volume = 150.0;
    }

    // Cost "just works" - no wiring needed
    attribute total_cost : Real = magnets.capital_cost;
}
```

**Pattern B: Explicit Wiring (Not Recommended)**
```sysml
// === LIBRARY ===
part def 'Magnet System' :> 'Costed Component' {
    attribute field_strength : Real;
    attribute coil_volume : Real;
    // No cost model - structure only
}

// === DESIGN (verbose, error-prone) ===
part catf_plant {
    part magnets : 'Magnet System' {
        :>> field_strength = 12.0;
        :>> coil_volume = 150.0;
    }

    // MANUAL WIRING - must repeat for every part!
    calc magnet_cost_calc : MagnetSystemCostCalc {
        in field = magnets.field_strength;
        in volume = magnets.coil_volume;
    }

    attribute cost_magnets : Real = magnet_cost_calc.total;
}
```

### Comparison Table

| Aspect | Nested (A) | Explicit Wiring (B) |
|--------|------------|---------------------|
| Lines in design file | ~15 | ~30 |
| Add new subsystem | Just instantiate | Instantiate + wire calc + expose |
| Knowledge duplication | None | Calc-to-part mapping repeated |
| Error risk | Low | High (forget to wire a part) |
| Co-location | Structure + cost together | Separated |
| Scalability | Excellent | Poor (50 parts = 50 wiring blocks) |

**Conclusion**: Nested cost models are cleaner. We should upgrade tooling to support them.

---

## Current Tooling Gap

### What sysml-codegen Does Today

Based on direct analysis of `usage_extractor.py`:

```python
# Line 155: Extracts ALL calc usages in the model
for elem in SysideAdapter.elements_of_type(model, "CalculationUsage"):
    usage_data = _extract_single_usage(elem, known_calc_defs, warnings, calc_def_map)

# Line 417: Parent path only tracks PartUsage, not PartDefinition
if SysideAdapter.is_instance(owning_elem, "PartUsage"):
    parts.insert(0, owning_elem.name)
```

**Current Behavior**:
1. sysml-codegen DOES find calc usages inside part definitions
2. It treats them as owned by the definition template
3. It does NOT create a new module instance per part usage

**Example of the Gap**:
```sysml
part def 'Wheel' {
    calc cost_calc { ... }  // Found as 'Wheel'::cost_calc
}

part front_wheel : 'Wheel';  // Does NOT create front_wheel.cost_calc module
part rear_wheel : 'Wheel';   // Does NOT create rear_wheel.cost_calc module
```

**What We Need**: When `'Wheel'` is instantiated as `front_wheel` and `rear_wheel`, sysml-codegen should create two module instances:
- `front_wheel.cost_calc` with bindings resolved through `front_wheel`'s redefinitions
- `rear_wheel.cost_calc` with bindings resolved through `rear_wheel`'s redefinitions

---

## Tooling Upgrade Specification

### Behavioral Requirements

#### BR-1: Detect Calc Usages in PartDefinitions

**Current**: All calc usages extracted with their direct owner context.

**Required**: Distinguish between:
- Calc usages owned by `PartUsage` → extract as today (concrete instance)
- Calc usages owned by `PartDefinition` → mark as "template" for instantiation

#### BR-2: Find All Instantiations of a PartDefinition

**Current**: Not done.

**Required**: For each PartDefinition containing calc usages, find all PartUsages that instantiate it (directly or through specialization chain).

#### BR-3: Create Virtual Calc Usages Per Instantiation

**Current**: One CalcUsageData per CalculationUsage element.

**Required**: For template calc usages, create N CalcUsageData instances where N = number of PartUsages instantiating the PartDefinition.

Each virtual calc usage should have:
- `qualified_name`: Based on PartUsage path (e.g., `catf_plant.magnets.cost_model`)
- `instance_name`: Combines part usage name and calc name (e.g., `magnets__cost_model`)
- `bindings`: Resolved through redefinition chain

#### BR-4: Resolve Bindings Through Redefinition Chain

**Current**: Bindings extracted as-is from calc usage element.

**Required**: For each binding in a template calc usage:
1. Identify the target attribute in the PartDefinition
2. Check if the PartUsage redefines that attribute
3. If redefined with a literal → binding becomes LITERAL
4. If redefined with an expression → binding follows the new expression
5. If not redefined → binding remains to definition attribute (may be unbound/entry point)

**Example Resolution**:
```
Template: cost_model.field → binds to 'Magnet System'::field_strength

PartUsage: magnets { :>> field_strength = 12.0 }

Resolved: magnets.cost_model.field → LITERAL 12.0
```

```
Template: cost_model.field → binds to 'Magnet System'::field_strength

PartUsage: magnets { :>> field_strength = power_balance.field_requirement }

Resolved: magnets.cost_model.field → CHAIN power_balance.field_requirement
```

#### BR-5: Handle Nested Part Hierarchies

**Current**: Parent path only tracks immediate PartUsage parents.

**Required**: Full path through nested PartUsages.

**Example**:
```sysml
part plant {
    part reactor {
        part magnets : 'Magnet System' { ... }
    }
}
```

Should produce: `plant.reactor.magnets.cost_model`

#### BR-6: Handle Multiple Levels of Definition Nesting

**Current**: Not supported.

**Required**: If a PartDefinition contains a PartUsage which itself has calc usages, the instantiation should recurse.

**Example**:
```sysml
part def 'Reactor' {
    part magnets : 'Magnet System';  // 'Magnet System' has cost_model
}

part my_reactor : 'Reactor';
```

Should produce: `my_reactor.magnets.cost_model`

---

### Code Changes Required

#### File 1: `sysml_codegen/extraction/usage_extractor.py`

**Change 1.1: Add owner type detection**

```python
# NEW FUNCTION (after line 420)
def _get_owning_type_info(elem: Any) -> tuple[str | None, Any | None]:
    """Get the owning type (PartDefinition or PartUsage) of an element.

    Returns:
        Tuple of (owner_type, owner_element) where owner_type is
        "PartDefinition", "PartUsage", or None.
    """
    current = elem
    while hasattr(current, "owner") and current.owner:
        owner = current.owner
        if hasattr(owner, "owning_related_element"):
            owning_elem = owner.owning_related_element
            if owning_elem:
                if SysideAdapter.is_instance(owning_elem, "PartDefinition"):
                    return ("PartDefinition", owning_elem)
                elif SysideAdapter.is_instance(owning_elem, "PartUsage"):
                    return ("PartUsage", owning_elem)
        current = owner
    return (None, None)
```

**Change 1.2: Add function to find PartUsages of a PartDefinition**

```python
# NEW FUNCTION
def _find_part_usages_of_definition(
    model: Any,
    part_def: Any,
) -> list[tuple[Any, str]]:
    """Find all PartUsages that instantiate a given PartDefinition.

    Args:
        model: The parsed SysML model
        part_def: The PartDefinition element

    Returns:
        List of (PartUsage element, full qualified path) tuples
    """
    usages = []
    part_def_name = getattr(part_def, 'name', None)

    for elem in SysideAdapter.elements_of_type(model, "PartUsage"):
        # Check if this usage's type matches the definition
        if _usage_instantiates_definition(elem, part_def, part_def_name):
            path = _build_full_part_path(elem)
            usages.append((elem, path))

    return usages


def _usage_instantiates_definition(
    usage: Any,
    part_def: Any,
    part_def_name: str | None,
) -> bool:
    """Check if a PartUsage instantiates a given PartDefinition."""
    if not hasattr(usage, "type") or not usage.type:
        return False

    for type_ref in usage.type:
        # Direct match
        if type_ref == part_def:
            return True
        # Name match (for cross-file references)
        if part_def_name and getattr(type_ref, 'name', None) == part_def_name:
            return True
        # Check specialization chain
        if _is_specialization_of(type_ref, part_def, part_def_name):
            return True

    return False


def _build_full_part_path(elem: Any) -> str:
    """Build full dot-separated path from root to this element."""
    parts = []
    current = elem

    while current:
        if hasattr(current, "name") and current.name:
            if SysideAdapter.is_instance(current, "PartUsage"):
                parts.insert(0, current.name)

        # Navigate up
        if hasattr(current, "owner") and current.owner:
            owner = current.owner
            if hasattr(owner, "owning_related_element"):
                current = owner.owning_related_element
            else:
                break
        else:
            break

    return ".".join(parts)
```

**Change 1.3: Add binding resolution through redefinition**

```python
# NEW FUNCTION
def _resolve_binding_through_redefinition(
    original_binding: BindingInfo,
    part_usage: Any,
    part_def: Any,
) -> BindingInfo:
    """Resolve a binding through a PartUsage's redefinitions.

    Args:
        original_binding: The binding from the template calc usage
        part_usage: The PartUsage that may redefine attributes
        part_def: The PartDefinition containing the original attribute

    Returns:
        New BindingInfo with resolved source path
    """
    # Find the target attribute in the part definition
    target_attr_name = original_binding.source_attribute_name
    if not target_attr_name:
        return original_binding

    # Check if part_usage redefines this attribute
    for member in getattr(part_usage, 'owned_members', []):
        member_name = getattr(member, 'name', None)

        # Check if this member redefines the target attribute
        if member_name == target_attr_name or _redefines_attribute(member, target_attr_name):
            # Extract the new binding source
            new_binding = _extract_single_binding(
                usage_elem=part_usage,
                param_elem=member,
                param_name=original_binding.param_name,
            )
            return new_binding

    # No redefinition found - binding remains unresolved (entry point)
    return BindingInfo(
        param_name=original_binding.param_name,
        source_path=None,
        binding_type=BindingType.UNBOUND,
        raw_expression=f"Unresolved: {target_attr_name} not redefined in {part_usage.name}",
    )


def _redefines_attribute(member: Any, attr_name: str) -> bool:
    """Check if a member redefines a specific attribute by name."""
    if not hasattr(member, 'owned_redefinitions'):
        return False

    for redef in member.owned_redefinitions:
        redefined = getattr(redef, 'redefined_feature', None)
        if redefined and getattr(redefined, 'name', None) == attr_name:
            return True

    return False
```

**Change 1.4: Add instantiation expansion function**

```python
# NEW FUNCTION
def _instantiate_template_calc_usages(
    model: Any,
    calc_usages: list[CalcUsageData],
    warnings: list[str],
) -> list[CalcUsageData]:
    """Expand calc usages in PartDefinitions to per-PartUsage instances.

    Args:
        model: The parsed SysML model
        calc_usages: List of extracted calc usages (may include templates)
        warnings: List to append warnings to

    Returns:
        Expanded list with template usages replaced by concrete instances
    """
    expanded = []

    for usage in calc_usages:
        owner_type, owner_elem = _get_owning_type_info(usage.raw_element)

        if owner_type == "PartDefinition":
            # This is a template - find all instantiations
            part_usages = _find_part_usages_of_definition(model, owner_elem)

            if not part_usages:
                warnings.append(
                    f"Calc usage '{usage.instance_name}' in PartDefinition "
                    f"'{owner_elem.name}' has no instantiations"
                )
                continue

            for part_usage, part_path in part_usages:
                # Create virtual calc usage for this instantiation
                virtual = _create_virtual_calc_usage(
                    template=usage,
                    part_usage=part_usage,
                    part_def=owner_elem,
                    part_path=part_path,
                )
                expanded.append(virtual)
        else:
            # Concrete usage - keep as-is
            expanded.append(usage)

    return expanded


def _create_virtual_calc_usage(
    template: CalcUsageData,
    part_usage: Any,
    part_def: Any,
    part_path: str,
) -> CalcUsageData:
    """Create a virtual calc usage for a specific PartUsage instantiation.

    Args:
        template: The template CalcUsageData from the PartDefinition
        part_usage: The PartUsage instantiating the PartDefinition
        part_def: The PartDefinition containing the template
        part_path: Full dot-separated path to the PartUsage

    Returns:
        New CalcUsageData with resolved bindings and updated paths
    """
    # Resolve bindings through redefinition chain
    resolved_bindings = []
    resolved_unbound = []

    for binding in template.bindings:
        resolved = _resolve_binding_through_redefinition(
            original_binding=binding,
            part_usage=part_usage,
            part_def=part_def,
        )
        if resolved.binding_type == BindingType.UNBOUND:
            resolved_unbound.append(resolved.param_name)
        else:
            resolved_bindings.append(resolved)

    # Build qualified name: part_path.calc_name
    qualified_name = f"{part_path}.{template.instance_name}"

    # Build instance name: flatten path with __
    instance_name = qualified_name.replace(".", "__")

    return CalcUsageData(
        instance_name=instance_name,
        calc_def_name=template.calc_def_name,
        calc_def_qualified_name=template.calc_def_qualified_name,
        module_type=template.module_type,
        bindings=resolved_bindings,
        unbound_params=resolved_unbound + template.unbound_params,
        source_file=template.source_file,
        source_line=template.source_line,
        parent_part_path=part_path,
        qualified_name=qualified_name,
    )
```

**Change 1.5: Modify main extraction function**

```python
# MODIFY extract_calculation_usages (around line 133)
def extract_calculation_usages(
    model: Any,
    known_calc_defs: set[str] | None = None,
    calc_defs: list | None = None,
    expand_templates: bool = True,  # NEW PARAMETER
) -> tuple[list[CalcUsageData], ExtractionReport]:
    """Extract all calculation usages from a SysML model.

    Args:
        model: Parsed SysIDE model
        known_calc_defs: Set of known calc def names for validation (optional)
        calc_defs: List of CalculationDefinitionData for detecting algorithm params
        expand_templates: If True, expand calc usages in PartDefinitions to
                         per-PartUsage instances (default True)

    Returns:
        Tuple of (list of CalcUsageData, ExtractionReport with statistics)
    """
    usages: list[CalcUsageData] = []
    warnings: list[str] = []

    # ... existing extraction code ...

    # NEW: Expand template calc usages
    if expand_templates:
        usages = _instantiate_template_calc_usages(model, usages, warnings)

    # ... rest of function ...
```

#### File 2: `sysml_codegen/extraction/usage_extractor.py` - Data Classes

**Change 2.1: Add raw_element to CalcUsageData**

```python
# MODIFY CalcUsageData dataclass (around line 84)
@dataclass
class CalcUsageData:
    # ... existing fields ...

    # NEW FIELD: Store raw AST element for template detection
    raw_element: Any = None
```

**Change 2.2: Store raw element during extraction**

```python
# MODIFY _extract_single_usage (around line 223)
    return CalcUsageData(
        instance_name=instance_name,
        # ... existing fields ...
        raw_element=elem,  # NEW: Store for template detection
    )
```

#### File 3: `sysml_codegen/generation/pipeline.py`

**No changes required** if extraction is correct. The pipeline generator consumes `CalcUsageData` and should work with the expanded virtual usages.

**Verification needed**: Ensure module naming handles the `__` separator in instance names.

#### File 4: Tests

**New test file: `tests/extraction/test_template_instantiation.py`**

```python
"""Tests for calc usage template instantiation."""

import pytest
from sysml_codegen.extraction.usage_extractor import extract_calculation_usages

# Test fixtures would use the models/tests/case*.sysml files

def test_calc_in_part_def_single_usage():
    """Calc in PartDef with one PartUsage creates one module."""
    model = load_model("models/tests/case1_calc_def_in_partdef.sysml")
    usages, report = extract_calculation_usages(model, expand_templates=True)

    # Should have one concrete calc usage for my_component.cost_calc
    assert len(usages) == 2  # cost_calc + final_cost_with_tax

    cost_calc = next(u for u in usages if "cost_calc" in u.instance_name)
    assert cost_calc.parent_part_path == "my_component"
    assert cost_calc.qualified_name == "my_component.cost_calc"


def test_calc_in_part_def_multiple_usages():
    """Calc in PartDef with multiple PartUsages creates multiple modules."""
    model = load_model("models/tests/wheel_multiple_instances.sysml")
    usages, report = extract_calculation_usages(model, expand_templates=True)

    # front_wheel.cost_calc and rear_wheel.cost_calc
    wheel_calcs = [u for u in usages if "cost_calc" in u.instance_name]
    assert len(wheel_calcs) == 2

    paths = {u.parent_part_path for u in wheel_calcs}
    assert paths == {"front_wheel", "rear_wheel"}


def test_binding_resolution_literal():
    """Literal redefinition resolves to LITERAL binding."""
    model = load_model("models/tests/case1_calc_def_in_partdef.sysml")
    usages, _ = extract_calculation_usages(model, expand_templates=True)

    cost_calc = next(u for u in usages if "cost_calc" in u.instance_name)

    # quantity was redefined to 12
    quantity_binding = next(b for b in cost_calc.bindings if b.param_name == "n")
    assert quantity_binding.binding_type == BindingType.LITERAL
    assert quantity_binding.literal_value == 12


def test_nested_part_hierarchy():
    """Deeply nested parts produce correct qualified names."""
    model = load_model("models/tests/nested_hierarchy.sysml")
    usages, _ = extract_calculation_usages(model, expand_templates=True)

    # plant.reactor.magnets.cost_model
    magnet_calc = next(u for u in usages if "cost_model" in u.instance_name)
    assert magnet_calc.qualified_name == "plant.reactor.magnets.cost_model"
```

---

### Implementation Order

1. **Phase 1: Detection** (BR-1, BR-2)
   - Add `_get_owning_type_info()`
   - Add `_find_part_usages_of_definition()`
   - Add `_build_full_part_path()`
   - Add tests for detection

2. **Phase 2: Resolution** (BR-4)
   - Add `_resolve_binding_through_redefinition()`
   - Add `_redefines_attribute()`
   - Add tests for literal and chain resolution

3. **Phase 3: Instantiation** (BR-3)
   - Add `raw_element` to `CalcUsageData`
   - Add `_instantiate_template_calc_usages()`
   - Add `_create_virtual_calc_usage()`
   - Modify `extract_calculation_usages()` with `expand_templates` param

4. **Phase 4: Nesting** (BR-5, BR-6)
   - Enhance path building for deep hierarchies
   - Handle recursive definition nesting
   - Add integration tests

5. **Phase 5: Pipeline Verification**
   - Verify generated pipeline YAML is correct
   - Verify teax-simkit executes correctly
   - End-to-end test with cost model

---

## Recommended Architecture (With Tooling Upgrade)

### Layer 1: Costed Component Interface

```sysml
// models/library/definitions/costed_component.sysml
abstract part def 'Costed Component' {
    doc /*
    Base interface for all cost-bearing components.
    Every subsystem must specialize this and define capital_cost.

    **Pattern Source**: PyFECONS cost_calculator.py
    */

    // Required for ALL costed components
    attribute capital_cost : Real;

    // Optional lifecycle attributes
    attribute annual_operating_cost : Real default := 0.0;
    attribute replacement_cost : Real default := 0.0;
    attribute replacement_interval_years : Real default := 40.0;
}
```

### Layer 2: Semantic Cost Calc Defs (NOT Generic Math)

**CRITICAL**: Do NOT create calc defs like `MultiplyAndAdd`. Each calc def encodes domain knowledge:

```sysml
// models/library/calculations/costing/magnet_cost.sysml
calc def MagnetSystemCostCalc {
    doc /*
    Magnet system cost per PyFECONS CAS220103.
    Encodes quadratic scaling with field strength.

    **Source**: PyFECONS
    **Reference**: pyfecons/costing/calculations/cas22/cas220103_coils.py
    */

    in attribute field_strength : Real;        // [Tesla]
    in attribute coil_volume : Real;           // [m^3]
    in attribute n_tf_coils : Integer;

    // Cost factors (with defaults from PyFECONS)
    in attribute hts_cost_per_m3 : Real default := 150.0e6;    // [$/m^3]
    in attribute structural_factor : Real default := 0.3;      // 30% for structure
    in attribute integration_factor : Real default := 0.25;    // 25% for integration

    // Intermediate outputs (for visibility)
    out attribute conductor_cost : Real;       // [$M]
    out attribute structural_cost : Real;      // [$M]
    out attribute integration_cost : Real;     // [$M]

    // Final outputs
    out attribute total_capital : Real;        // [$M]
    out attribute cost_per_coil : Real;        // [$M/coil]
    out attribute conductor_fraction : Real;   // [fraction]
}
```

### Layer 3: Part Definitions with Embedded Cost Models

**This is the key pattern**: Each part definition contains its own cost calc usage, co-locating structure with analysis.

```sysml
// models/library/definitions/magnet_system.sysml
part def 'Magnet System' :> 'Costed Component' {
    doc /*
    Magnet system with embedded cost model.
    Cost is automatically calculated when part is instantiated.
    */

    // === STRUCTURAL PARAMETERS (set by design) ===
    attribute field_strength : Real;
    attribute coil_volume : Real;
    attribute n_tf_coils : Integer;

    // === EMBEDDED COST MODEL ===
    calc cost_model : MagnetSystemCostCalc {
        in field_strength = field_strength;
        in coil_volume = coil_volume;
        in n_tf_coils = n_tf_coils;
    }

    // === EXPOSE COST INTERFACE ===
    :>> capital_cost = cost_model.total_capital;

    // === EXPOSE INTERMEDIATE VALUES (for visibility) ===
    attribute conductor_cost : Real = cost_model.conductor_cost;
    attribute structural_cost : Real = cost_model.structural_cost;
    attribute conductor_fraction : Real = cost_model.conductor_fraction;
}

// models/library/definitions/blanket_system.sysml
part def 'Blanket System' :> 'Costed Component' {
    attribute surface_area : Real;
    attribute thickness : Real;
    attribute breeding_ratio : Real;

    calc cost_model : BlanketSystemCostCalc {
        in area = surface_area;
        in thickness = thickness;
        in tbr = breeding_ratio;
    }

    :>> capital_cost = cost_model.total_capital;
    attribute material_cost : Real = cost_model.material_cost;
}
```

### Layer 4: Clean Design Files (No Manual Wiring!)

```sysml
// models/designs/catf/system.sysml
package 'CATF Design' {
    private import 'FusionTEA::Library::Definitions'::*;
    private import 'FusionTEA::Library::Calculations'::LCOECalculation;

    part catf_plant {
        // Instantiate subsystems - costs are AUTOMATIC
        part magnets : 'Magnet System' {
            :>> field_strength = 12.0;      // Tesla
            :>> coil_volume = 150.0;        // m^3
            :>> n_tf_coils = 12;
        }

        part blanket : 'Blanket System' {
            :>> surface_area = 800.0;       // m^2
            :>> thickness = 0.5;            // m
            :>> breeding_ratio = 1.15;
        }

        part divertor : 'Divertor System' {
            :>> heat_load = 10.0;           // MW/m^2
            :>> surface_area = 50.0;        // m^2
        }

        // Costs "just work" - no manual wiring needed!
        attribute cas22_reactor : Real =
            magnets.capital_cost +
            blanket.capital_cost +
            divertor.capital_cost;

        // Top-level LCOE (only one calc wiring needed)
        calc lcoe_calc : LCOECalculation {
            in cas22_reactor = cas22_reactor;
            in p_net = power_balance.p_net;
            in availability = 0.85;
        }

        attribute lcoe : Real = lcoe_calc.lcoe;
        attribute overnight_cost_per_kw : Real = lcoe_calc.overnight_cost_per_kw;

        // All intermediate values accessible for comparison
        attribute magnet_cost : Real = magnets.capital_cost;
        attribute magnet_conductor_fraction : Real = magnets.conductor_fraction;
        attribute blanket_cost : Real = blanket.capital_cost;
    }
}
```

### Layer 5: Generated Pipeline (After Tooling Upgrade)

With the tooling upgrade, sysml-codegen will automatically instantiate calc modules per PartUsage:

```yaml
# Generated by sysml-codegen (AFTER tooling upgrade)
modules:
  # Automatically created from magnets : 'Magnet System'
  catf_plant__magnets__cost_model:
    class: MagnetSystemCostCalcModule
    inputs:
      field_strength: {value: 12.0}      # Resolved from redefinition
      coil_volume: {value: 150.0}        # Resolved from redefinition
      n_tf_coils: {value: 12}            # Resolved from redefinition
    outputs: [conductor_cost, structural_cost, integration_cost, total_capital, cost_per_coil, conductor_fraction]

  # Automatically created from blanket : 'Blanket System'
  catf_plant__blanket__cost_model:
    class: BlanketSystemCostCalcModule
    inputs:
      area: {value: 800.0}
      thickness: {value: 0.5}
      tbr: {value: 1.15}
    outputs: [material_cost, total_capital]

  # Automatically created from divertor : 'Divertor System'
  catf_plant__divertor__cost_model:
    class: DivertorSystemCostCalcModule
    # ...

  # Explicit calc in design file
  catf_plant__lcoe_calc:
    class: LCOECalculationModule
    inputs:
      cas22_reactor: module.catf_plant__magnets__cost_model.total_capital + ...
      # ...

exit_points:
  - { name: lcoe, channel: catf_plant__lcoe_calc.lcoe }
  - { name: magnet_cost, channel: catf_plant__magnets__cost_model.total_capital }
  - { name: magnet_conductor_fraction, channel: catf_plant__magnets__cost_model.conductor_fraction }
  - { name: blanket_cost, channel: catf_plant__blanket__cost_model.total_capital }
  # ... 50+ output channels for full visibility
```

---

## Addressing Your Original Questions

### Q1: Do nested cost models work?

**YES**, with caveats:
- SysMLv2 semantics support it (redefinition propagates values)
- sysml-codegen finds calc usages in part defs but doesn't instantiate per usage
- Practical approach: explicit wiring in design files

### Q2: Can we recursively define parametric rollups?

**YES**, via the hierarchical pattern:
1. Each part exposes `capital_cost` attribute
2. Parent parts sum child costs via explicit formula
3. Propagation happens automatically through redefinition

### Q3: Is there a "standard cost model" we can enforce?

**YES**, via the `'Costed Component'` abstract part def:
- All cost-bearing parts specialize it
- Required attribute: `capital_cost`
- Optional: `annual_operating_cost`, `replacement_cost`, `replacement_interval_years`
- Enforcement via agentic-mbse validation (Level 9)

### Q4: How do we get visibility for comparison?

**Multi-output calc defs**:
- Every calc def exposes 5-20+ output attributes
- sysml-codegen generates `{CalcName}Output` with all fields
- teax-simkit routes each output to separate channel
- Results include full breakdown, not just final LCOE

---

## Full LCOE Calculation Pattern

Based on PyFECONS methodology:

```sysml
calc def LCOECalculation {
    doc /*
    Master LCOE calculation per PyFECONS methodology.

    Formula:
      LCOE = [CAS90 + (CAS70 + CAS80)*(1+inflation)^lifetime] / [8760*P_net*availability]

    **Source**: PyFECONS costing/calculations/lcoe.py
    */

    // === CAPITAL COST INPUTS (by CAS category) ===
    in attribute cas21_buildings : Real;
    in attribute cas22_reactor : Real;
    in attribute cas23_turbine : Real;
    in attribute cas24_electric : Real;
    in attribute cas25_misc : Real;
    in attribute cas26_heat_rejection : Real;
    in attribute cas27_special_materials : Real;

    // === INDIRECT FACTORS ===
    in attribute indirect_factor : Real default := 0.20;
    in attribute owners_factor : Real default := 0.10;
    in attribute financial_factor : Real default := 0.15;

    // === OPERATING COSTS ===
    in attribute annual_om : Real;
    in attribute annual_fuel : Real;

    // === FINANCIAL PARAMETERS ===
    in attribute capital_recovery_factor : Real default := 0.09;
    in attribute plant_lifetime : Real default := 40.0;
    in attribute inflation_rate : Real default := 0.02;

    // === POWER OUTPUT ===
    in attribute p_net : Real;
    in attribute availability : Real;

    // === INTERMEDIATE OUTPUTS ===
    out attribute cas20_direct : Real =
        cas21_buildings + cas22_reactor + cas23_turbine +
        cas24_electric + cas25_misc + cas26_heat_rejection +
        cas27_special_materials;

    out attribute cas30_indirect : Real = cas20_direct * indirect_factor;
    out attribute cas40_owners : Real = cas20_direct * owners_factor;
    out attribute cas50_financial : Real = cas20_direct * financial_factor;

    out attribute total_capital : Real =
        cas20_direct + cas30_indirect + cas40_owners + cas50_financial;

    out attribute cas90_annualized : Real =
        capital_recovery_factor * total_capital * 1.0e6;  // Convert $M to $

    out attribute inflated_opex : Real =
        (annual_om + annual_fuel) * ((1.0 + inflation_rate) ** plant_lifetime);

    out attribute total_annual : Real = cas90_annualized + inflated_opex;

    out attribute annual_energy_mwh : Real = 8760.0 * p_net * availability;

    // === FINAL LCOE ===
    out attribute lcoe : Real = total_annual / annual_energy_mwh;

    // === BREAKDOWN FRACTIONS ===
    out attribute capital_lcoe_fraction : Real = cas90_annualized / total_annual;
    out attribute om_lcoe_fraction : Real = annual_om / total_annual;
    out attribute fuel_lcoe_fraction : Real = annual_fuel / total_annual;

    // === NORMALIZED METRICS ===
    out attribute overnight_cost_per_kw : Real = total_capital * 1000.0 / p_net;
}
```

---

## Implementation Roadmap

### Phase 1: Cost Infrastructure (Immediate)

1. Create `models/library/definitions/costed_component.sysml`
   - Abstract `'Costed Component'` definition
   - Required and optional cost attributes

2. Create `models/library/calculations/costing/` directory:
   - `lcoe.sysml` - Master LCOE calc def
   - `subsystem_rollup.sysml` - CAS22 aggregation
   - `magnet_cost.sysml` - Example subsystem calc

3. Update `MODELING_GUIDE.md`:
   - Document cost modeling patterns
   - Enforce semantic calc defs (not generic math)
   - Require all parts specialize `'Costed Component'`

### Phase 2: CATF Design Integration

4. Create `models/designs/catf/cost_analysis.sysml`:
   - Wire structural parts to cost calcs
   - EXPOSE all intermediate values
   - Master LCOE calculation

5. Test end-to-end pipeline:
   - Run sysml-codegen to generate modules
   - Execute with teax-simkit
   - Verify all 50+ outputs visible

### Phase 3: Validation and Comparison

6. Add agentic-mbse Level 9 validation:
   - Rule: Every costed component has cost calc def
   - Rule: Cost calc inputs match part attributes
   - Rule: All cost-bearing parts wired to calcs

7. Create comparison framework:
   - Standard output schema (25+ required outputs)
   - Visualization scripts (bar charts, Sankey, tornado)

---

## Summary Table

| Concern | Pattern | Implementation |
|---------|---------|----------------|
| **Interface enforcement** | `'Costed Component'` abstract part def | All subsystems specialize it |
| **Cost calculations** | Semantic calc defs in library | `MagnetSystemCostCalc`, `BlanketCostCalc`, etc. |
| **Cost model location** | **Embedded in part definitions** | Calc usage inside part def, binds to own attributes |
| **Design files** | Clean instantiation only | Just set parameters, costs computed automatically |
| **Recursive rollup** | Parent sums child `capital_cost` | `total = child1.capital_cost + child2.capital_cost` |
| **Visibility** | Multi-output calc defs | 20+ outputs per calc, all exposed via part attributes |
| **Comparison** | Standard output schema | 25+ required outputs across all designs |
| **Tooling requirement** | sysml-codegen upgrade | Instantiate template calcs per PartUsage |

---

## References

**Prior Research**:
- `modeling_pm/research/20260106-050051_cost-modeling-lcoe-strategy.md`
- `modeling_pm/research/20260106-065431_cost-architecture-patterns.md`
- `modeling_pm/research/NEXT_cost-architecture-patterns.md`

**Test Models**:
- `models/tests/case1_calc_def_in_partdef.sysml` - Nested calc def pattern
- `models/tests/case2_calc_usage_in_partdef.sysml` - Inline calc usage pattern

**Tooling**:
- `sysml-codegen/src/sysml_codegen/extraction/usage_extractor.py:155` - Calc extraction
- `sysml-codegen/src/sysml_codegen/extraction/usage_extractor.py:407-421` - Parent path logic

**PyFECONS**:
- `pyfecons/costing/calculations/lcoe.py` - Master LCOE formula
- `pyfecons/costing/calculations/cas22/` - CAS220xxx detailed calcs

---

**Last Updated**: 2026-01-07
