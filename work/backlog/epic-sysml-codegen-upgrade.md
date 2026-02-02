# sysml-codegen Upgrade: Cost Model Processing

**Status**: Ready for Implementation
**Priority**: P0 (Blocks Phase 4 - Cost Calculations)
**Created**: 2026-01-12
**Epic**: Cost Patterns De-Risking (Stage 4)

---

## 1. Executive Summary

### Goal

Enable sysml-codegen to process **Pattern A (Nested Cost Models)** - where calc usages are embedded inside part definitions and must be instantiated per part usage.

### Current Gap

sysml-codegen finds `cost_model` calc usages in PartDefinitions but treats them as templates. It does **not**:
- Create calc instances per PartUsage
- Resolve parameter bindings through the redefinition chain
- Handle multiplicity aggregation with `sum()`

### Success Criteria

Generate output matching `models/tests/coffee_maker/expected_output.csv` within 1e-6 tolerance.

### Reference Implementation

A working Python implementation exists at `models/tests/coffee_maker/generate_costs.py` (1550 lines). This document specifies what sysml-codegen needs to replicate.

---

## 2. Goals & Requirements

| ID | Goal | Description |
|----|------|-------------|
| G1 | Discover cost models | Find all `cost_model` calc usages in PartDefinitions |
| G2 | Resolve bindings | Trace parameter values through design redefinitions |
| G3 | Evaluate formulas | Compute calc outputs with bound parameter values |
| G4 | Handle multiplicity | Process `[N]` arrays with `sum()` aggregation |
| G5 | Aggregate assemblies | Roll up child costs to parent assemblies |
| G6 | Generate output | Produce CSV in the 14-column schema |

---

## 3. Output Schema

### Reference File

`models/tests/coffee_maker/expected_output.csv`

### Column Definitions (14 columns)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `path` | string | Qualified dot-notation path | `coffee_maker.brewing.heater` |
| `part_def` | string | Part definition name | `Heating Element` |
| `quantity` | int | Multiplicity (1 for singles, N for arrays) | `2` |
| `unit_material_cost` | float? | Per-unit material cost (leaf only) | `7.50` |
| `unit_fab_cost` | float? | Per-unit fabrication cost (leaf only) | `4.50` |
| `unit_install_cost` | float? | Per-unit installation cost (leaf only) | `1.125` |
| `unit_total_cost` | float? | Per-unit total cost (leaf only) | `13.125` |
| `total_material_cost` | float | Aggregated material cost | `15.00` |
| `total_fab_cost` | float | Aggregated fabrication cost | `9.00` |
| `total_install_cost` | float | Aggregated installation cost | `2.25` |
| `total_cost` | float | Total cost | `26.25` |
| `idiot_index` | float | `total_cost / total_material_cost` | `1.75` |
| `cost_type` | enum | `"leaf"`, `"assembly"`, or `"allocation"` | `leaf` |
| `calc_def` | string? | Calc definition name (leaf/allocation only) | `HeatingElementCostCalc` |

### Row Types

1. **Leaf**: Direct calculation from parameters
   - `unit_*` columns populated
   - `total_* = quantity × unit_*`
   - `calc_def` populated

2. **Assembly**: Aggregation from children
   - `unit_*` columns empty
   - `total_*` = sum of children
   - `calc_def` empty

3. **Allocation**: Assembly-level minor items
   - Separate row for visibility
   - `calc_def` = allocation calc name
   - Included in parent assembly's totals

### Row Ordering

**Pre-order traversal**: parent → children → allocation

```
coffee_maker              (assembly)
coffee_maker.brewing      (assembly)
coffee_maker.brewing.heater    (leaf)
coffee_maker.brewing.pump      (leaf)
coffee_maker.brewing.chamber   (leaf)
coffee_maker.brewing.allocation (allocation)
coffee_maker.reservoir    (leaf)
coffee_maker.carafe       (leaf)
coffee_maker.housing      (assembly)
coffee_maker.housing.shell     (leaf)
coffee_maker.housing.panel     (leaf)
```

---

## 4. Modeling Patterns (How SysML Looks)

### 4.1 Calc Definition Pattern

**Reference**: `models/tests/coffee_maker/library.sysml:43-71`

```sysml
calc def HeatingElementCostCalc {
    // Inputs (some with defaults)
    in attribute power : Real;
    in attribute mass : Real;
    in attribute material_cost_per_kg : Real default := 50.0;
    in attribute fab_factor : Real default := 0.6;
    in attribute install_factor : Real default := 0.15;

    // Outputs (with formulas referencing inputs and other outputs)
    out attribute material_cost : Real = mass * material_cost_per_kg;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**Key extraction points**:
- `in attribute` with optional `default :=` value
- `out attribute` with `=` formula expression
- Output dependencies (fab_cost depends on material_cost)

### 4.2 Leaf Part Pattern

**Reference**: `models/tests/coffee_maker/library.sysml:226-252`

```sysml
part def 'Heating Element' :> 'Costed Component' {
    // Design parameters
    attribute power_rating : Real;
    attribute material_mass : Real;

    // Embedded cost model (THIS IS THE KEY PATTERN)
    calc cost_model : HeatingElementCostCalc {
        in power = power_rating;
        in mass = material_mass;
        // Defaults not overridden
    }

    // Expose calc outputs as part attributes
    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**Key extraction points**:
- `calc cost_model` inside PartDefinition (not PartUsage)
- Input bindings: `in power = power_rating` maps calc param to part attribute
- Output bindings: `:>> capital_cost = cost_model.total_cost`

### 4.3 Assembly Pattern with sum()

**Reference**: `models/tests/coffee_maker/library.sysml:384-438`

```sysml
part def 'Brewing System' :> 'Costed Component' {
    // Parameterized multiplicity
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

    // Aggregation using sum() for arrays
    :>> capital_cost =
        sum(heater.capital_cost) +
        pump.capital_cost +
        chamber.capital_cost +
        misc_hardware_cost;
    // ... similar for other cost categories
}
```

**Key extraction points**:
- `part heater [heater_count]` - parameterized multiplicity
- `sum(heater.capital_cost)` - aggregation over array
- `allocation_model` - separate calc for minor items

### 4.4 Design Binding Pattern

**Reference**: `models/tests/coffee_maker/design.sysml:20-37`

```sysml
part coffee_maker : 'Coffee Maker' {
    part redefines brewing {
        // Dot notation bindings apply to child attributes
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

**Key extraction points**:
- `part redefines X` establishes context
- `:>> child.attr = value` binds nested attribute
- Dot path: first segment = child name, remainder = attribute path

---

## 5. Current Parsing Mechanisms

### 5.1 Reference Implementation: generate_costs.py

**File**: `models/tests/coffee_maker/generate_costs.py` (1550 lines)

#### Phase 1: Calc Definition Extraction

**Function**: `extract_calc_defs()` (lines 107-160)

```python
def extract_calc_defs(model) -> dict[str, CalcDefInfo]:
    """Extract all calc definitions from the model."""
    calc_defs = {}
    for calc_def in adapter.elements_of_type(model, "CalculationDefinition"):
        name = calc_def.name
        inputs, outputs = {}, {}

        for member in getattr(calc_def, "owned_members", []):
            if not adapter.is_instance(member, "AttributeUsage"):
                continue

            direction = getattr(member, "direction", None)
            attr_name = member.name

            if direction and direction.name == "In":
                default = _extract_default_value(member)
                inputs[attr_name] = InputParam(name=attr_name, default_value=default)
            elif direction and direction.name == "Out":
                expr_ast = getattr(member, "feature_value_expression", None)
                deps = _extract_dependencies(expr_ast)
                outputs[attr_name] = OutputFormula(
                    name=attr_name, expression_ast=expr_ast, dependencies=deps
                )

        calc_defs[name] = CalcDefInfo(name=name, inputs=inputs, outputs=outputs)
    return calc_defs
```

**Key patterns**:
- `adapter.elements_of_type(model, "CalculationDefinition")` for discovery
- `direction.name == "In"` vs `"Out"` for input/output distinction
- `feature_value_expression` for formula AST

#### Phase 2: Part-to-Calc Mapping

**Function**: `map_part_defs_to_calcs()` (lines 248-277)

```python
def map_part_defs_to_calcs(model) -> dict[str, str]:
    """Map part definition names to their cost_model calc def names."""
    mapping = {}
    for calc_usage in adapter.elements_of_type(model, "CalculationUsage"):
        if calc_usage.name not in ("cost_model", "allocation_model"):
            continue

        # Find owning part definition
        owner = _get_owning_part_def(calc_usage)
        if owner:
            calc_def_name = _get_calc_def_name(calc_usage)
            mapping[owner.name] = calc_def_name

    return mapping
```

**Key patterns**:
- Filter by calc usage name (`cost_model`, `allocation_model`)
- Traverse ownership to find containing PartDefinition

#### Phase 3: Design Hierarchy Extraction

**Function**: `extract_design_hierarchy()` (lines 312-359)

**Binding Extraction**: `_extract_design_bindings()` (lines 362-469)

```python
def _extract_design_bindings(design_part) -> dict[str, dict[str, dict[str, float]]]:
    """Extract bindings from design redefinitions.

    Returns: {context: {child: {attr: value}}}
    Example: {"brewing": {"heater": {"power_rating": 1000.0}}}
    """
    bindings = {}

    for member in getattr(design_part, "owned_members", []):
        if not adapter.is_instance(member, "PartUsage"):
            continue

        # Check for redefines pattern
        redefinitions = getattr(member, "owned_redefinitions", [])
        if not redefinitions:
            continue

        context_name = _get_redefined_name(redefinitions[0])
        context_bindings = {}

        # Extract :>> bindings from the redefining part
        for nested in getattr(member, "owned_members", []):
            if _is_redefinition_expression(nested):
                path, value = _extract_binding(nested)
                # Parse dot path: heater.power_rating -> ("heater", "power_rating")
                parts = path.split(".")
                if len(parts) == 2:
                    child, attr = parts
                    if child not in context_bindings:
                        context_bindings[child] = {}
                    context_bindings[child][attr] = value

        bindings[context_name] = context_bindings

    return bindings
```

**Key patterns**:
- `owned_redefinitions` to find `part redefines X` blocks
- `chaining_features` to extract dot-notation paths
- Nested dict structure: `{context: {child: {attr: value}}}`

#### Phase 4: Formula Evaluation

**Function**: `evaluate_calc()` (lines 909-939)

```python
def evaluate_calc(calc_def: CalcDefInfo, bound_params: dict[str, float]) -> dict[str, float]:
    """Evaluate all outputs in topological order."""
    values = dict(bound_params)

    sorted_outputs = _topological_sort_outputs(calc_def.outputs)

    for output in sorted_outputs:
        values[output.name] = _evaluate_expression(output.expression_ast, values)

    return values
```

**Expression Evaluation**: `_evaluate_expression()` (lines 992-1058)

```python
def _evaluate_expression(expr, values: dict[str, float]) -> float:
    """Recursively evaluate an expression AST."""
    type_name = type(expr).__name__

    if type_name in ("LiteralRational", "LiteralReal"):
        return float(expr.value)
    elif type_name == "LiteralInteger":
        return float(expr.value)
    elif type_name in ("FeatureReferenceExpression", "FeatureChainExpression"):
        ref_name = _get_reference_name(expr)
        if ref_name not in values:
            raise ValueError(f"Unbound reference: {ref_name}")
        return values[ref_name]
    elif type_name == "OperatorExpression":
        op = _get_operator(expr)
        operands = list(expr.operands)
        left = _evaluate_expression(operands[0], values)
        right = _evaluate_expression(operands[1], values)

        if op in ("+", "Plus"): return left + right
        elif op in ("-", "Minus"): return left - right
        elif op in ("*", "Times"): return left * right
        elif op in ("/", "Divide"): return left / right
        else:
            raise ValueError(f"Unsupported operator: {op}")
    else:
        raise ValueError(f"Unsupported expression type: {type_name}")
```

**Key patterns**:
- Type checking via `type(expr).__name__` (avoids import coupling)
- Recursive operand evaluation
- Operator as both string (`"+"`) and enum name (`"Plus"`)

#### Phase 5: Cost Aggregation

**Function**: `compute_costs()` (lines 1066-1280)

```python
def compute_costs(root: PartInstance, calc_defs: dict) -> list[CostResult]:
    """Compute costs in post-order, emit in pre-order."""
    computed = {}

    def _compute_recursive(part):
        # Compute children first (post-order)
        for child in part.children:
            _compute_recursive(child)

        if part.cost_type == "leaf":
            # Evaluate calc with bound params
            outputs = evaluate_calc(calc_defs[part.calc_def_name], part.bound_params)
            computed[part.path] = _make_leaf_result(part, outputs)
        else:
            # Aggregate children
            child_results = [computed[c.path] for c in part.children]
            computed[part.path] = _make_assembly_result(part, child_results)

            # Handle allocation if present
            if part.allocation:
                alloc_outputs = evaluate_calc(
                    calc_defs[part.allocation.calc_def_name],
                    part.allocation.bound_params
                )
                computed[part.path + ".allocation"] = _make_allocation_result(
                    part, alloc_outputs
                )

    _compute_recursive(root)

    # Emit in pre-order
    results = []
    def _emit_preorder(part):
        results.append(computed[part.path])
        for child in part.children:
            _emit_preorder(child)
        if part.allocation:
            results.append(computed[part.path + ".allocation"])

    _emit_preorder(root)
    return results
```

**Key patterns**:
- Post-order computation (children before parents)
- Pre-order emission (parents before children in output)
- Allocation rows emitted after all children of their assembly

### 5.2 From validate_ast.py

**File**: `models/tests/coffee_maker/validate_ast.py` (556 lines)

| Function | Purpose | Lines |
|----------|---------|-------|
| `find_cost_models()` | Discovers `cost_model`/`allocation_model` calc usages | 83-137 |
| `find_part_usages_with_multiplicity()` | Finds arrayed parts | 217-280 |
| `_extract_multiplicity_bound()` | Gets array size from AST | 283-331 |
| `_get_calc_def_name()` | Extracts calc def from usage | 140-164 |

### 5.3 Key AST Navigation Patterns

| Task | Pattern |
|------|---------|
| Element discovery | `adapter.elements_of_type(model, "TypeName")` |
| Ownership | `getattr(elem, "owner", None)` |
| Children | `getattr(elem, "owned_members", [])` |
| Redefinitions | `getattr(elem, "owned_redefinitions", [])` |
| Type info | `getattr(rel, "type", None)` for FeatureTyping |
| Expression value | `getattr(elem, "feature_value_expression", None)` |
| Default value | `getattr(elem, "feature_value", None)` |
| Multiplicity | `getattr(elem, "multiplicity", None)` then `upper_bound` |

---

## 6. Data Structures

### CalcDefInfo

```python
@dataclass
class CalcDefInfo:
    name: str                           # "HeatingElementCostCalc"
    inputs: dict[str, InputParam]       # param_name -> InputParam
    outputs: dict[str, OutputFormula]   # output_name -> OutputFormula

@dataclass
class InputParam:
    name: str                           # "power"
    default_value: float | None         # 50.0 or None

@dataclass
class OutputFormula:
    name: str                           # "material_cost"
    expression_ast: Any                 # Raw AST for evaluation
    dependencies: list[str]             # ["mass", "material_cost_per_kg"]
```

### PartInstance

```python
@dataclass
class PartInstance:
    path: str                           # "coffee_maker.brewing.heater"
    part_def_name: str                  # "Heating Element"
    quantity: int                       # 2 for heater[2]
    cost_type: str                      # "leaf" or "assembly"
    calc_def_name: str | None           # "HeatingElementCostCalc" for leaves
    bound_params: dict[str, float]      # {"power": 1000.0, "mass": 0.15}
    children: list[PartInstance]        # Recursive children
    allocation: AllocationInfo | None   # For assemblies with allocation_model

@dataclass
class AllocationInfo:
    calc_def_name: str                  # "AllocationCostCalc"
    display_name: str                   # "Brewing System Allocation"
    bound_params: dict[str, float]      # {"child_count": 4.0}
```

### CostResult

```python
@dataclass
class CostResult:
    path: str                           # Qualified path
    part_def: str                       # Part definition name
    quantity: int                       # Count
    unit_material_cost: float | None    # Per-unit (leaf only)
    unit_fab_cost: float | None
    unit_install_cost: float | None
    unit_total_cost: float | None
    total_material_cost: float          # Aggregated
    total_fab_cost: float
    total_install_cost: float
    total_cost: float
    idiot_index: float
    cost_type: str                      # "leaf", "assembly", "allocation"
    calc_def: str | None                # For leaves/allocations only
```

---

## 7. Implementation Phases

| Phase | Priority | Task | Dependency |
|-------|----------|------|------------|
| P1 | P0 | Calc definition extraction | None |
| P2 | P0 | Cost model discovery + binding resolution | P1 |
| P3 | P0 | Formula evaluation | P1, P2 |
| P4 | P1 | Multiplicity handling | P3 |
| P5 | P0 | Output generation | P3, P4 |

### Phase 1: Calc Definition Extraction

- Iterate `CalculationDefinition` elements
- Extract inputs with defaults, outputs with formulas
- Build dependency graph for topological sort
- **Test**: Extract 8 calc defs from library.sysml

### Phase 2: Cost Model Discovery + Binding Resolution

- Find `cost_model` calc usages in PartDefinitions
- Build part instance hierarchy from design
- Resolve parameter bindings through redefinition chain
- **Test**: heater bound params = {power: 1000.0, mass: 0.15}

### Phase 3: Formula Evaluation

- Topologically sort outputs by dependencies
- Recursively evaluate expression AST
- Handle operators: +, -, *, /
- **Test**: HeatingElement unit_total_cost = 13.125

### Phase 4: Multiplicity Handling

- Detect array multiplicity from PartUsage
- Track unit costs per instance
- Handle `sum()` aggregation in assembly formulas
- **Test**: heater[2] → quantity=2, total=26.25

### Phase 5: Output Generation

- Generate CSV in 14-column schema
- Pre-order row emission
- Integration with sysml-codegen pipeline
- **Test**: Full CSV matches expected_output.csv

---

## 8. Test Cases

### Unit Test: Calc Definition Extraction

**Input**: `library.sysml`

**Assertions**:
- 8 calc defs found
- `HeatingElementCostCalc` has 5 inputs (power, mass, 3 with defaults)
- `HeatingElementCostCalc` has 5 outputs
- Defaults: `material_cost_per_kg=50.0`, `fab_factor=0.6`, `install_factor=0.15`
- Dependencies: `fab_cost` depends on `material_cost`

### Unit Test: Parameter Binding Resolution

**Input**: `design.sysml` + `library.sysml`

**Setup**: Extract BrewingSystem with heater array

**Assertions**:
- `heater.power_rating = 1000.0` (from design)
- `heater.material_mass = 0.15` (from design)
- `pump.flow_rate = 0.5` (from design)
- Binding precedence: design overrides default

### Integration Test: Cost Evaluation

**Input**: Full coffee maker model

**Assertions**:
- HeatingElement: `unit_total_cost = 13.125`
  - material = 0.15 × 50 = 7.5
  - fab = 7.5 × 0.6 = 4.5
  - install = 7.5 × 0.15 = 1.125
  - total = 7.5 + 4.5 + 1.125 = 13.125
- heater[2]: total = 2 × 13.125 = 26.25
- Allocation: total = 4.80

### Integration Test: Output Format

**Assertions**:
- 14 columns
- 12 rows (including allocation)
- Pre-order: coffee_maker → brewing → heater → ... → allocation → ...
- Float precision: match within 1e-6

---

## 9. Appendix

### A. Complete Calculation Walkthrough: Heating Element

```
Input parameters (from design.sysml):
  power_rating = 1000.0
  material_mass = 0.15

Calc def defaults (from library.sysml):
  material_cost_per_kg = 50.0
  fab_factor = 0.6
  install_factor = 0.15

Bound parameters:
  power = 1000.0  (from power_rating)
  mass = 0.15     (from material_mass)
  material_cost_per_kg = 50.0  (default)
  fab_factor = 0.6  (default)
  install_factor = 0.15  (default)

Formula evaluation (topological order):
  1. material_cost = mass × material_cost_per_kg
                   = 0.15 × 50.0 = 7.50

  2. fab_cost = material_cost × fab_factor
              = 7.50 × 0.6 = 4.50

  3. install_cost = material_cost × install_factor
                  = 7.50 × 0.15 = 1.125

  4. total_cost = material_cost + fab_cost + install_cost
                = 7.50 + 4.50 + 1.125 = 13.125

  5. idiot_index = total_cost / material_cost
                 = 13.125 / 7.50 = 1.75

Output row:
  path: coffee_maker.brewing.heater
  part_def: Heating Element
  quantity: 2
  unit_material_cost: 7.50
  unit_fab_cost: 4.50
  unit_install_cost: 1.125
  unit_total_cost: 13.125
  total_material_cost: 15.00  (= 2 × 7.50)
  total_fab_cost: 9.00  (= 2 × 4.50)
  total_install_cost: 2.25  (= 2 × 1.125)
  total_cost: 26.25  (= 2 × 13.125)
  idiot_index: 1.75
  cost_type: leaf
  calc_def: HeatingElementCostCalc
```

### B. File References

| File | Purpose |
|------|---------|
| `models/tests/coffee_maker/library.sysml` | Calc defs, part defs |
| `models/tests/coffee_maker/design.sysml` | Design bindings |
| `models/tests/coffee_maker/expected_output.csv` | Expected results |
| `models/tests/coffee_maker/generate_costs.py` | Reference implementation |
| `models/tests/coffee_maker/validate_ast.py` | AST validation patterns |
| `modeling_pm/docs/COST_MODELING.md` | Modeling guide |
| `modeling_pm/research/20260107-final-cost-architecture.md` | Architecture rationale |

### C. Research Documents

- `modeling_pm/research/20260107-final-cost-architecture.md` - Why nested cost models
- `modeling_pm/research/20260110-strategic-cost-patterns.md` - Standardization rules
- `modeling_pm/research/20260112-055807_multiplicity-cost-rollup-gap.md` - sum() solution
