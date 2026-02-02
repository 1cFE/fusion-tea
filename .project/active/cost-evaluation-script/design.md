# Design: Cost Evaluation Script

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-12 14:53:24 UTC
**Branch:** costing-patterns
**Commit:** a103596

---

## Overview

Python script that evaluates the coffee maker SysML model's cost calculations, producing `actual_output.csv` to validate against `expected_output.csv`. This proves the cost modeling pattern (Pattern A: nested cost models) is evaluable before investing in sysml-codegen tooling upgrades.

## Related Artifacts

- **Spec:** `.project/active/cost-evaluation-script/spec.md`
- **Epic:** `.project/backlog/epic-cost-patterns-derisking.md` (Stage 2b)
- **Test Model:** `models/tests/coffee_maker/` (library.sysml, design.sysml)
- **Expected Output:** `models/tests/coffee_maker/expected_output.csv`
- **AST Validation:** `models/tests/coffee_maker/validate_ast.py`

---

## Research Findings

### Existing Codebase Analysis

#### validate_ast.py (models/tests/coffee_maker/validate_ast.py)

This script provides reusable patterns for the evaluation script:

| Function | Purpose | Reusability |
|----------|---------|-------------|
| `find_cost_models()` (line 83) | Discovers cost_model/allocation_model calc usages in part definitions | **Reuse directly** - returns CostModelInfo with calc_def_name, owning_part_def |
| `find_part_usages_with_multiplicity()` (line 217) | Finds part usages with array counts | **Reuse directly** - returns PartInfo with multiplicity, part_def_name |
| `_extract_multiplicity_bound()` (line 283) | Extracts array size from multiplicity AST | **Reuse directly** - handles LiteralInteger and LiteralInfinity |
| `_get_calc_def_name()` (line 140) | Extracts calc definition name from calc usage | **Reuse directly** |

#### agentic_mbse.sysml.expression (expression.py)

| Function | Purpose | Applicability |
|----------|---------|---------------|
| `evaluate_true_static_expression()` (line 374) | Evaluates literal math expressions | **Cannot use directly** - raises ValueError on feature refs. Cost formulas contain feature refs like `mass * material_cost_per_kg` |
| `extract_feature_refs()` (line 119) | Extracts attribute references from expressions | **Useful** - identifies what parameters an expression depends on |
| `is_true_static_expression()` (line 478) | Checks if expression has no design refs | **Useful** - can check if expression is evaluable after substitution |

**Key insight**: The existing `evaluate_true_static_expression()` is designed for ADR-002 compliance checking (detecting illegal refs), not for evaluating formulas with bound parameters. We need a different approach.

#### agentic_mbse.sysml.binding (binding.py)

| Function | Purpose | Applicability |
|----------|---------|---------------|
| `extract_bindings()` (line 65) | Extracts parameter bindings from CalculationUsage | **Useful** - gets calc usage inputs with their binding types |
| `classify_binding()` (line 13) | Classifies binding type (LITERAL, CHAIN, EXPRESSION, etc.) | **Useful** - identifies how each input is bound |

**Gap**: `extract_bindings()` works on calc usages, but we need to trace `:>>` bindings at the part usage level (e.g., `part redefines brewing { :>> heater.power_rating = 1000.0 }`).

#### agentic_mbse.sysml.syside_adapter (syside_adapter.py)

| Method | Purpose |
|--------|---------|
| `SysideAdapter.load_model()` (line 161) | Load SysML model files |
| `SysideAdapter.elements_of_type()` (line 195) | Iterate elements by type name |
| `SysideAdapter.is_instance()` (line 230) | Type checking with mock support |

#### validation.common (common.py)

| Function | Purpose |
|----------|---------|
| `get_qualified_name()` (line 157) | Get element's qualified name for paths |
| `get_element_location()` (line 169) | Get file:line location for debugging |

### Model Structure Analysis

From reading `library.sysml` and `design.sysml`:

**Calc Definition Pattern** (library.sysml lines 43-71):
```sysml
calc def HeatingElementCostCalc {
    in attribute power : Real;
    in attribute mass : Real;
    in attribute material_cost_per_kg : Real default := 50.0;  // Has default
    in attribute fab_factor : Real default := 0.6;

    out attribute material_cost : Real = mass * material_cost_per_kg;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
}
```

**Calc Usage Pattern** (library.sysml lines 241-244):
```sysml
calc cost_model : HeatingElementCostCalc {
    in power = power_rating;      // Bound to part attribute
    in mass = material_mass;      // Bound to part attribute
    // Defaults not overridden    // Uses default values
}
```

**Design Binding Pattern** (design.sysml lines 26-27):
```sysml
part redefines brewing {
    :>> heater.power_rating = 1000.0;   // Binds part attribute
    :>> heater.material_mass = 0.15;
}
```

### Output Schema (expected_output.csv)

The expected output has 13 columns:
- `path`, `part_def`, `quantity` - Identification
- `unit_material_cost`, `unit_fab_cost`, `unit_install_cost`, `unit_total_cost` - Per-unit (leaf only)
- `total_material_cost`, `total_fab_cost`, `total_install_cost`, `total_cost` - Totals
- `idiot_index` - Efficiency metric
- `cost_type` - "leaf", "assembly", or "allocation"
- `calc_def` - Calc definition name (leaf only)

### Key Evaluation Challenges

1. **Calc def formula extraction**: Need to extract output expressions from calc definitions (e.g., `material_cost = mass * material_cost_per_kg`)

2. **Default value handling**: Calc defs have default parameter values that must be used when not overridden in calc usage

3. **Parameter binding resolution**: Must trace through:
   - Calc usage input bindings (e.g., `in mass = material_mass`)
   - Part definition attributes (e.g., `attribute material_mass : Real`)
   - Design redefinitions (e.g., `:>> heater.material_mass = 0.15`)

4. **Multiplicity handling**: heater[2] means:
   - `quantity = 2`
   - `unit_*` costs are per-instance
   - `total_*` costs are `quantity × unit_*`

5. **Assembly rollup**: Uses `sum(heater.capital_cost)` which aggregates over all array instances

---

## Proposed Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       generate_costs.py                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Model Loading (SysideAdapter)                               │
│     └─ Load library.sysml + design.sysml                        │
│                                                                 │
│  2. Extraction Phase                                            │
│     ├─ Extract calc definitions with formulas + defaults        │
│     ├─ Extract part definitions with cost_model mappings        │
│     ├─ Extract design instance with parameter bindings          │
│     └─ Build part hierarchy tree                                │
│                                                                 │
│  3. Evaluation Phase                                            │
│     ├─ For each leaf part: evaluate cost_model with bound params│
│     ├─ Handle multiplicity (unit × quantity)                    │
│     └─ For each assembly: aggregate children + allocation       │
│                                                                 │
│  4. Output Phase                                                │
│     ├─ Generate actual_output.csv                               │
│     └─ Compare with expected_output.csv                         │
└─────────────────────────────────────────────────────────────────┘
```

### Data Structures

```python
@dataclass
class CalcDefInfo:
    """Extracted information from a calc definition."""
    name: str                           # "HeatingElementCostCalc"
    inputs: dict[str, InputParam]       # param_name -> InputParam
    outputs: dict[str, OutputFormula]   # output_name -> OutputFormula

@dataclass
class InputParam:
    """Input parameter from calc def."""
    name: str
    default_value: float | None         # None if no default

@dataclass
class OutputFormula:
    """Output formula from calc def."""
    name: str                           # "material_cost"
    expression_ast: Any                 # Raw AST for evaluation
    dependencies: list[str]             # ["mass", "material_cost_per_kg"]
    # Dependencies used for topological sort: material_cost must be
    # computed before fab_cost (which references material_cost)

@dataclass
class AllocationInfo:
    """Information about an allocation_model in an assembly."""
    calc_def_name: str                  # "AllocationCostCalc"
    display_name: str                   # "Brewing System Allocation"
    bound_params: dict[str, float]      # Resolved input parameters

@dataclass
class PartInstance:
    """A concrete part in the design hierarchy."""
    path: str                           # "coffee_maker.brewing.heater"
    part_def_name: str                  # "Heating Element"
    quantity: int                       # 2 for heater[2]
    cost_type: str                      # "leaf" or "assembly"
    calc_def_name: str | None           # "HeatingElementCostCalc" for leaves
    bound_params: dict[str, float]      # Resolved parameter values
    children: list[PartInstance]        # For assemblies
    allocation: AllocationInfo | None   # For assemblies with allocation_model

@dataclass
class CostResult:
    """Computed costs for a part instance."""
    path: str
    part_def: str
    quantity: int
    unit_material_cost: float | None
    unit_fab_cost: float | None
    unit_install_cost: float | None
    unit_total_cost: float | None
    total_material_cost: float
    total_fab_cost: float
    total_install_cost: float
    total_cost: float
    idiot_index: float
    cost_type: str
    calc_def: str | None
```

### Component Details

#### 1. CalcDefExtractor

**Purpose**: Extract calc definitions with their formulas and default values.

**Location**: `generate_costs.py` (inline class or functions)

**Key Functions**:

```python
def extract_calc_defs(model) -> dict[str, CalcDefInfo]:
    """Extract all calc definitions from the model.

    Returns:
        Mapping of calc def name -> CalcDefInfo
    """
```

**Implementation Notes**:
- Iterate `SysideAdapter.elements_of_type(model, "CalculationDefinition")`
- For each calc def, iterate `owned_members` to find AttributeUsage
- Distinguish inputs (`in attribute`) from outputs (`out attribute`)
- Extract default values from `feature_value_expression` on inputs
- Extract formulas from `feature_value_expression` on outputs
- Use `extract_feature_refs()` to find formula dependencies

**AST Access Pattern** (from library.sysml structure):
```python
for calc_def in elements_of_type(model, "CalculationDefinition"):
    for member in calc_def.owned_members:
        if is_instance(member, "AttributeUsage"):
            # Check direction: in/out
            direction = getattr(member, "direction", None)
            # Get value expression
            expr = getattr(member, "feature_value_expression", None)
```

#### 2. PartDefMapper

**Purpose**: Map part definitions to their cost_model calc usages.

**Location**: `generate_costs.py`

**Key Functions**:

```python
def map_part_defs_to_calcs(model) -> dict[str, str]:
    """Map part definition names to their cost_model calc def names.

    Returns:
        Mapping of part_def_name -> calc_def_name
        e.g., {"Heating Element": "HeatingElementCostCalc"}
    """
```

**Implementation Notes**:
- Reuse `find_cost_models()` from validate_ast.py
- Build mapping from `owning_part_def` -> `calc_def_name`

#### 3. DesignExtractor

**Purpose**: Extract the design hierarchy with resolved parameter bindings.

**Location**: `generate_costs.py`

**Key Functions**:

```python
def extract_design_hierarchy(model) -> PartInstance:
    """Extract the design hierarchy starting from coffee_maker.

    Returns:
        Root PartInstance with children populated recursively.
    """

def resolve_parameter_bindings(part_usage, part_def, parent_bindings) -> dict[str, float]:
    """Resolve all parameter values for a part instance.

    Traces through:
    1. Default values from calc def
    2. Calc usage bindings (in power = power_rating)
    3. Part definition attributes
    4. Design redefinitions (:>> heater.power_rating = 1000.0)

    Returns:
        Mapping of calc input param name -> resolved float value
    """
```

**Implementation Notes**:
- Find `coffee_maker` PartUsage in `CoffeeMakerDesign` package
- Recursively build hierarchy by iterating `owned_members` for child PartUsages
- Use `_extract_multiplicity_bound()` from validate_ast.py for array sizes
- Extract allocation_model from assembly part definitions (same pattern as cost_model)

**Dot Notation Binding Extraction**:

The design file uses `part redefines brewing { :>> heater.power_rating = 1000.0 }` to bind parameters. The extraction approach:

1. **Find redefining parts**: Iterate `owned_members` of design instance, look for PartUsages with `owned_redefinitions`
2. **Collect bindings by context**: For each `part redefines X` block:
   - The redefining part establishes context (e.g., `brewing`)
   - Iterate its `owned_members` for redefinition expressions
3. **Parse dot paths**: For `:>> heater.power_rating = 1000.0`:
   - `redefined_feature` gives the target: `heater.power_rating`
   - Parse as path segments: `["heater", "power_rating"]`
   - First segment identifies child part, remainder identifies attribute
4. **Build binding map**: Create nested structure:
   ```python
   bindings = {
       "brewing": {
           "heater": {"power_rating": 1000.0, "material_mass": 0.15},
           "pump": {"flow_rate": 0.5},
           "chamber": {"volume": 0.3}
       },
       "housing": {
           "shell": {"surface_area": 0.15},
           "panel": {"button_count": 3.0}
       }
   }
   ```
5. **Extract literal values**: Use `feature_value_expression` on the redefinition, evaluate as literal

**Binding Resolution Order** (most specific wins):
1. Check design redefinitions for explicit `:>>` bindings (from binding map above)
2. Fall back to calc usage input bindings (from part def's cost_model)
3. Fall back to calc def default values

#### 4. FormulaEvaluator

**Purpose**: Evaluate calc def formulas with bound parameter values.

**Location**: `generate_costs.py`

**Key Functions**:

```python
def evaluate_formula(
    formula_ast: Any,
    param_values: dict[str, float],
    calc_def_info: CalcDefInfo
) -> float:
    """Evaluate a formula AST with the given parameter values.

    Args:
        formula_ast: The expression AST from calc def output
        param_values: Mapping of param name -> value (inputs + computed outputs)
        calc_def_info: The calc def for resolving references

    Returns:
        Computed float value
    """
```

**Implementation Notes**:
- Cannot use `evaluate_true_static_expression()` directly (it rejects feature refs)
- Implement custom evaluation that:
  1. Traverses expression AST
  2. For OperatorExpression: recursively evaluate operands, apply operator
  3. For FeatureReferenceExpression: look up value in `param_values`
  4. For LiteralRational/LiteralInteger: return numeric value

**Topological Sort for Evaluation Order**:

Output formulas must be evaluated in dependency order. Example from HeatingElementCostCalc:
- `material_cost = mass * material_cost_per_kg` (depends on inputs only)
- `fab_cost = material_cost * fab_factor` (depends on material_cost)
- `total_cost = material_cost + fab_cost + install_cost` (depends on all above)

```python
def evaluate_all_outputs(calc_def: CalcDefInfo, input_values: dict[str, float]) -> dict[str, float]:
    """Evaluate all outputs in topological order."""
    values = dict(input_values)  # Start with inputs

    # Sort outputs by dependencies (simple case: iterate in definition order,
    # since calc defs are typically written in dependency order)
    sorted_outputs = topological_sort(calc_def.outputs)

    for output in sorted_outputs:
        # At this point, all dependencies are in `values`
        values[output.name] = evaluate_formula(output.expression_ast, values)

    return values

def topological_sort(outputs: dict[str, OutputFormula]) -> list[OutputFormula]:
    """Sort outputs so dependencies come before dependents.

    Uses OutputFormula.dependencies to determine order.
    For simple calc defs, definition order usually works.
    """
```

**Supported Operators**: `+`, `-`, `*`, `/` (same as expression.py:328)

#### 5. CostAggregator

**Purpose**: Aggregate costs for assemblies from their children.

**Location**: `generate_costs.py`

**Key Functions**:

```python
def compute_costs(root: PartInstance, calc_defs: dict[str, CalcDefInfo]) -> list[CostResult]:
    """Compute costs for all parts in hierarchy.

    For leaves: Evaluate cost_model with bound params
    For assemblies: Sum children costs + allocation
    For allocations: Evaluate allocation_model, emit separate row

    Returns:
        List of CostResult in PRE-ORDER for output (parent, children, allocation)
        matching expected_output.csv row ordering.
    """
```

**Computation vs Output Order**:

The expected_output.csv uses **pre-order** for display (parent before children):
```
coffee_maker              <- assembly first
coffee_maker.brewing      <- child assembly
coffee_maker.brewing.heater   <- grandchild leaf
coffee_maker.brewing.pump
coffee_maker.brewing.chamber
coffee_maker.brewing.allocation  <- allocation AFTER leaf children
...
```

The implementation uses **post-order** for computation (children before parents, so totals are available), but **pre-order** for output generation:

```python
def compute_costs(root: PartInstance, calc_defs: dict) -> list[CostResult]:
    # Internal: compute in post-order (recursive, children first)
    computed: dict[str, CostResult] = {}
    _compute_recursive(root, calc_defs, computed)

    # Output: emit in pre-order (parent, children, allocation)
    results: list[CostResult] = []
    _emit_preorder(root, computed, results)
    return results

def _emit_preorder(part: PartInstance, computed: dict, results: list):
    """Emit results in pre-order: parent, then children, then allocation."""
    results.append(computed[part.path])
    for child in part.children:
        _emit_preorder(child, computed, results)
    if part.allocation:
        # Allocation row emitted AFTER all children
        results.append(computed[part.path + ".allocation"])
```

**Allocation Row Generation**:

Assemblies with `allocation_model` get a **separate CostResult row** in the output:

```python
# For assembly with allocation (e.g., brewing):
if part.allocation:
    # 1. Evaluate allocation_model to get its costs
    alloc_costs = evaluate_calc(part.allocation.calc_def_name,
                                part.allocation.bound_params,
                                calc_defs)

    # 2. Create allocation CostResult
    alloc_result = CostResult(
        path=f"{part.path}.allocation",         # "coffee_maker.brewing.allocation"
        part_def=part.allocation.display_name,  # "Brewing System Allocation"
        quantity=1,
        unit_material_cost=alloc_costs["material_portion"],
        unit_fab_cost=0.0,
        unit_install_cost=0.0,
        unit_total_cost=alloc_costs["total_allocation"],
        total_material_cost=alloc_costs["material_portion"],
        total_fab_cost=0.0,
        total_install_cost=0.0,
        total_cost=alloc_costs["total_allocation"],
        idiot_index=alloc_costs["total_allocation"] / alloc_costs["material_portion"],
        cost_type="allocation",
        calc_def=part.allocation.calc_def_name
    )

    # 3. Include allocation in assembly's rollup totals
    assembly_result.total_material_cost += alloc_costs["material_portion"]
    assembly_result.total_cost += alloc_costs["total_allocation"]
```

**Implementation Notes**:
- **Post-order computation**: Children computed before parents so totals are available for rollup
- **Pre-order output**: Results emitted parent-first to match expected_output.csv
- **Allocation after children**: Allocation row inserted after all leaf children of an assembly
- For leaf parts:
  - Get calc_def by name
  - Evaluate formulas in topological order (using OutputFormula.dependencies)
  - Multiply by quantity for totals
- For assemblies:
  - Sum `total_*` costs from children (including their allocations)
  - Add own allocation costs if present
  - Compute idiot_index = total_cost / total_material_cost

#### 6. OutputGenerator

**Purpose**: Generate CSV output and compare with expected.

**Location**: `generate_costs.py`

**Key Functions**:

```python
def write_csv(results: list[CostResult], output_path: Path) -> None:
    """Write results to CSV file in expected schema."""

def compare_outputs(actual_path: Path, expected_path: Path) -> tuple[bool, list[str]]:
    """Compare actual vs expected CSV with tolerance.

    Returns:
        (passed, list of diff messages)
    """
```

**Implementation Notes**:
- Use csv module for writing
- Match column order from expected_output.csv
- Comparison tolerance: ~1e-6 for floating point
- Report which rows/columns differ

### File Structure

```
models/tests/coffee_maker/
├── library.sysml          # Input: calc defs, part defs
├── design.sysml           # Input: design instance
├── validate_ast.py        # Existing: AST validation
├── expected_output.csv    # Input: hand-calculated expected values
├── generate_costs.py      # NEW: cost evaluation script
└── actual_output.csv      # Output: generated costs
```

### Dependencies

**External packages**: None beyond agentic-mbse (per spec requirement)

**Internal modules**:
- `agentic_mbse.sysml.syside_adapter.SysideAdapter`
- `agentic_mbse.sysml.expression.extract_feature_refs`
- `agentic_mbse.validation.common.get_qualified_name`, `get_element_location`

**Reused from validate_ast.py**:
- `find_cost_models()` (import or inline)
- `find_part_usages_with_multiplicity()` (import or inline)
- `_extract_multiplicity_bound()` (import or inline)
- `_get_calc_def_name()` (import or inline)

### Data Flow

```
                    library.sysml
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
CalcDefExtractor    PartDefMapper      (validates)
    │                    │
    │ CalcDefInfo        │ part_def→calc_def
    ▼                    ▼
    └────────┬───────────┘
             │
             ▼                    design.sysml
      DesignExtractor  ◄──────────────┘
             │
             │ PartInstance tree
             ▼
      FormulaEvaluator
             │
             │ Unit costs computed
             ▼
      CostAggregator
             │
             │ List[CostResult]
             ▼
      OutputGenerator ──────► actual_output.csv
             │
             │ compare
             ▼
      expected_output.csv ──► PASS/FAIL report
```

### Error Handling

| Scenario | Handling |
|----------|----------|
| Model fails to load | Print error message, exit 1 |
| Calc def not found for part | Print warning, skip part (shouldn't happen in valid model) |
| Parameter not bound (no default) | Print error with location, exit 1 |
| Division by zero | Print error with formula context, exit 1 |
| Output mismatch | Print diff details, exit 1 |

### Usage Example

```bash
cd models/tests/coffee_maker
python generate_costs.py
# Outputs:
#   Writing actual_output.csv...
#   Comparing with expected_output.csv...
#   PASS: All 12 rows match within tolerance
```

Or with verbose output:

```bash
python generate_costs.py --verbose
# Shows each calculation step
```

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| AST structure differs from expected | Medium | Validate assumptions against actual AST early; use validate_ast.py patterns |
| Formula evaluation complexity | Low | Start with simple arithmetic; coffee maker uses only +, -, *, / |
| Binding resolution edge cases | Medium | Document resolution order; dot notation parsing fully specified |
| Dot path parsing errors | Medium | Test with design.sysml bindings; handle nested paths carefully |

---

## Integration Strategy

**Complements**: This script works alongside `validate_ast.py`:
- `validate_ast.py` validates structure (7 calcs found, bindings traced)
- `generate_costs.py` validates computation (values match expected)

**Does not replace**: Any existing tooling. This is a standalone validation script.

**Future**: Patterns from this script will inform sysml-codegen implementation (Stage 4).

---

## Validation Approach

### Testing Strategy

1. **Unit validation**: Each component's output can be spot-checked against model/expected
2. **Integration validation**: Final CSV comparison against expected_output.csv

### Success Criteria

- [ ] Script loads model without errors
- [ ] All 7 leaf cost calculations evaluated
- [ ] Multiplicity handling correct (heater quantity=2, totals doubled)
- [ ] Assembly rollups aggregate correctly
- [ ] Allocation costs appear as separate row and included in assembly totals
- [ ] Output row ordering matches expected (pre-order: parent, children, allocation)
- [ ] `actual_output.csv` matches `expected_output.csv` within tolerance (~1e-6)

### Manual Verification

Spot-check one leaf calculation (HeatingElement):
- Input: mass=0.15, material_cost_per_kg=50.0 (default)
- Expected material_cost = 0.15 × 50.0 = 7.50
- Verify this appears in actual_output.csv

Spot-check allocation row (Brewing System):
- Path: `coffee_maker.brewing.allocation`
- Expected total_allocation = 4 × 0.50 + 4 × 0.30 + 0.8 × 2.0 = 4.80
- Verify row exists with cost_type="allocation"

---

**Next Steps:** After approval → `/_my_implement`
