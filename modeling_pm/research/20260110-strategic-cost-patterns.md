---
date: 2026-01-10T14:30:00-08:00
researcher: Claude
topic: "Strategic Cost Modeling Patterns for Fusion TEA"
tags: [research, cost-modeling, architecture, patterns, principles, idiot-index, bom, synthesis]
status: complete
last_updated: 2026-01-10
---

# Research: Strategic Cost Modeling Patterns for Fusion TEA

**Date**: 2026-01-10
**Researcher**: Claude
**Research Type**: Architecture Synthesis (Multi-Source Integration)

## Research Question

How should we design cost modeling patterns for fusion TEA that:
1. Standardize the "cost calc" reference name across parts?
2. Define clear expectations around recursion?
3. Enable enforcement rules for proper implementation?
4. Produce clean, parseable output (tables, hierarchy, rollup)?
5. Support the "idiot index" (cost/material ratio) metric?
6. Generate BOM-like outputs with material + installation breakdown?

This document synthesizes findings from:
- Fusion-simkit/sysml-codegen traversal capabilities
- PyFECONS cost structure analysis
- MBSE/SysML cost modeling literature
- Commercial costing software patterns
- SysMLv2 official patterns

---

## Executive Summary

Based on comprehensive research across five domains, I recommend the following strategic approach:

### Core Principles

1. **Standardized Cost Interface**: Every costed part MUST expose `capital_cost` via the `'Costed Component'` interface
2. **Standardized Calc Reference**: Every part with embedded cost logic SHOULD have a calc usage named `cost_model`
3. **Recursive Rollup Rule**: Assemblies aggregate child costs; leaf parts compute directly - no middle ground
4. **Multi-Category Outputs**: Every calc exposes `raw_material_cost`, `fabrication_cost`, `installation_cost`, `total_cost`
5. **Idiot Index**: Every material-intensive part tracks `finished_cost / raw_material_cost` ratio

### Design Alternatives Evaluated

| Alternative | Pattern | Complexity | Tooling Gap | Recommended |
|-------------|---------|------------|-------------|-------------|
| **A. Nested Cost Models** | Calc usage inside part def | Medium | YES (sysml-codegen) | ✅ Long-term |
| **B. Explicit Wiring** | Calc usages in design files | Low | None | ✅ Immediate |
| **C. Hybrid Approach** | Nested + explicit where needed | Medium | Partial | ✅ Transition |

---

## Part 1: Standardization Decisions

### Q1: Should we standardize the "cost calc" reference name across parts?

**Recommendation: YES - Use `cost_model` as the standard name**

**Rationale**:

1. **Traversal Simplification**: sysml-codegen's `usage_extractor.py:155` iterates over all `CalculationUsage` elements. A standard name enables pattern-based filtering:
   ```python
   cost_calcs = [u for u in usages if u.instance_name.endswith("cost_model")]
   ```

2. **Industry Precedent**: NASA WBS and PyFECONS both use consistent naming (CAS codes)

3. **Validation Rules**: Enables agentic-mbse Level 9 rules like:
   - "Every `PartUsage` typed by `'Costed Component'` must have a `cost_model` calc usage"

4. **Output Schema**: Predictable channel names for results:
   - `plant.magnets.cost_model.total_cost`
   - `plant.blanket.cost_model.total_cost`

**Standard Pattern**:

```sysml
part def 'Magnet System' :> 'Costed Component' {
    // Design parameters
    attribute field_strength : Real;
    attribute coil_volume : Real;

    // STANDARD NAME: cost_model
    calc cost_model : MagnetSystemCostCalc {
        in field = field_strength;
        in volume = coil_volume;
    }

    // EXPOSE via standard interface
    :>> capital_cost = cost_model.total_cost;
}
```

**Exceptions Allowed**:
- Parts with multiple cost models (e.g., `cost_model_base` + `cost_model_advanced`)
- Analysis-specific calcs (e.g., `mass_calc`, `thermal_calc`) - different purpose

---

### Q2: Should we standardize expectations around recursion?

**Recommendation: YES - Define clear recursion rules**

**Rule Framework**:

#### Rule R1: Leaf Parts MUST Have Direct Cost Calculations

**Definition**: A "leaf part" is a `PartUsage` with no child `PartUsage` members that are `'Costed Component'` types.

**Pattern**:
```sysml
// LEAF: No costed children, direct calculation
part def 'First Wall' :> 'Costed Component' {
    attribute area : Real;
    attribute armor_thickness : Real;
    attribute armor_material : Material;

    calc cost_model : FirstWallCostCalc {
        in area = area;
        in thickness = armor_thickness;
        in material = armor_material;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
}
```

#### Rule R2: Assembly Parts MUST Aggregate Child Costs

**Definition**: An "assembly part" is a `PartUsage` with one or more child `PartUsage` members typed by `'Costed Component'`.

**Pattern**:
```sysml
// ASSEMBLY: Has costed children, aggregates their costs
part def 'Blanket System' :> 'Costed Component' {
    // Child parts (each is a 'Costed Component')
    part first_wall : 'First Wall' { ... }
    part breeding_zone : 'Breeding Zone' { ... }
    part back_structure : 'Back Structure' { ... }

    // Additional assembly-level costs (integration, testing)
    attribute assembly_cost : Real;

    // AGGREGATION: Sum of children plus assembly overhead
    :>> capital_cost =
        first_wall.capital_cost +
        breeding_zone.capital_cost +
        back_structure.capital_cost +
        assembly_cost;

    // AGGREGATION: Material costs from all children
    :>> raw_material_cost =
        first_wall.raw_material_cost +
        breeding_zone.raw_material_cost +
        back_structure.raw_material_cost;
}
```

#### Rule R3: Assembly-Level Allocation Costs (Revised from "No Hybrid Parts")

**Original concern**: Mixing direct calculation with partial aggregation creates ambiguity.

**Practical reality**: Real BOMs include costs that don't decompose neatly:
- Fasteners, seals, gaskets
- Floor stock (consumables)
- Miscellaneous hardware
- Assembly tooling amortization

**Revised Rule R3**: Assembly parts MAY include **allocation costs** for items that:
1. Are **low-value** relative to the assembly (< 5% of assembly cost)
2. Are **standard/commodity** items (not custom-engineered)
3. Do **not warrant** their own part definition or cost model
4. Can be **estimated as a function** of assembly characteristics

**Pattern: Assembly with Allocation Costs**
```sysml
part def 'TF Coil System' :> 'Costed Component' {
    // === MODELED CHILDREN (significant cost items) ===
    part conductor : 'TF Conductor' [12] { ... }
    part structure : 'TF Structure' [12] { ... }
    part feedthroughs : 'Feedthroughs' [12] { ... }

    // === ALLOCATION COSTS (bundled minor items) ===
    // These don't warrant separate part definitions
    calc allocation_model : TFCoilAllocationCost {
        in n_coils = 12;
        in conductor_mass = conductor.total_mass;
        in structure_mass = structure.total_mass;
    }

    // Allocation outputs are CATEGORIZED for traceability
    attribute fastener_allowance : Real = allocation_model.fastener_cost;
    attribute seal_allowance : Real = allocation_model.seal_cost;
    attribute floor_stock_allowance : Real = allocation_model.floor_stock_cost;
    attribute misc_hardware_cost : Real =
        fastener_allowance + seal_allowance + floor_stock_allowance;

    // === COST AGGREGATION ===
    :>> capital_cost =
        // Children (modeled)
        conductor.capital_cost +
        structure.capital_cost +
        feedthroughs.capital_cost +
        // Allocation (bundled)
        misc_hardware_cost +
        // Integration (process-based, see Part 5)
        integration_cost;

    // === MATERIAL TRACKING ===
    // Allocation items contribute to material cost for idiot index
    :>> raw_material_cost =
        conductor.raw_material_cost +
        structure.raw_material_cost +
        feedthroughs.raw_material_cost +
        allocation_model.material_portion;  // ~80% of misc is material
}
```

**Allocation Calc Def Pattern**:
```sysml
calc def TFCoilAllocationCost {
    doc /*
    Bundled allocation costs for TF Coil assembly.
    Covers minor items not modeled as separate parts.

    **Estimation Method**: Engineering judgment + historical data
    **AACE Class**: 4 (study/feasibility level)
    **Typical Range**: 2-5% of major component costs
    */

    in attribute n_coils : Integer;
    in attribute conductor_mass : Real;    // [kg]
    in attribute structure_mass : Real;    // [kg]

    // Fasteners: ~$50/kg of structure (bolts, nuts, washers)
    out attribute fastener_cost : Real = structure_mass * 50.0 / 1.0e6;

    // Seals: ~$20/coil (vacuum seals, thermal barriers)
    out attribute seal_cost : Real = n_coils * 20.0 / 1.0e6;

    // Floor stock: ~1% of conductor mass value
    out attribute floor_stock_cost : Real = conductor_mass * 0.01 * 150.0 / 1.0e6;

    // Total
    out attribute total_allocation : Real =
        fastener_cost + seal_cost + floor_stock_cost;

    // Material vs labor split (for idiot index)
    out attribute material_portion : Real = total_allocation * 0.8;
    out attribute labor_portion : Real = total_allocation * 0.2;
}
```

**Enforcement Rule E3b: Allocation Cost Limits**
```yaml
rule_id: E3b-ALLOCATION-LIMITS
severity: WARNING
description: "Allocation costs should be < 5% of assembly cost"
check:
  for_each: PartUsage where has allocation_model calc
  condition: misc_hardware_cost / capital_cost < 0.05
message: "Assembly '{name}' has high allocation costs ({percent}%) - consider modeling items explicitly"
```

**When to Promote Allocation to Modeled Part**:
- If allocation item exceeds 5% of assembly cost
- If allocation item has significant design uncertainty
- If allocation item affects system performance (not just cost)
- If allocation item needs tracking for maintenance/spares

**Anti-pattern STILL to AVOID**:
```sysml
// BAD: Uses allocation as a "fudge factor" without basis
part def 'Mystery Assembly' :> 'Costed Component' {
    part child_1 : 'Child' { ... }

    // BAD: Unexplained overhead with no calc basis
    attribute mystery_overhead : Real = 500.0;  // Where does this come from?

    :>> capital_cost = child_1.capital_cost + mystery_overhead;
}
```

**Key Distinction**:
- ✅ **Allocation**: Systematic estimate based on assembly characteristics (mass, count, etc.)
- ❌ **Fudge factor**: Arbitrary overhead with no documented basis

#### Rule R4: Assembly Overhead MUST Be Explicit

**Pattern**:
```sysml
part def 'TF Coil System' :> 'Costed Component' {
    part conductor : 'TF Conductor' [12] { ... }  // 12 coils
    part structure : 'TF Structure' [12] { ... }
    part feedthroughs : 'Feedthroughs' [12] { ... }

    // EXPLICIT: Assembly-level costs that aren't in children
    calc assembly_cost_model : TFCoilAssemblyCost {
        in n_coils = 12;
        in conductor_mass = conductor.total_mass;
    }

    :>> capital_cost =
        conductor.capital_cost +
        structure.capital_cost +
        feedthroughs.capital_cost +
        assembly_cost_model.integration_cost +
        assembly_cost_model.testing_cost;
}
```

---

### Q3: What rules could we write to enforce proper implementation?

**Recommendation: Implement agentic-mbse Level 9 validation rules**

#### Enforcement Rule E1: Costed Interface Compliance

```yaml
rule_id: E1-COSTED-INTERFACE
severity: ERROR
description: "Every part specializing 'Costed Component' must expose capital_cost"
check:
  for_each: PartUsage where type :> 'Costed Component'
  condition: attribute 'capital_cost' is bound (not null/unbound)
message: "Part '{name}' missing capital_cost binding"
```

#### Enforcement Rule E2: Cost Model Naming

```yaml
rule_id: E2-COST-MODEL-NAME
severity: WARNING
description: "Cost calc usages should be named 'cost_model'"
check:
  for_each: CalculationUsage where calc_def contains 'Cost'
  condition: instance_name == 'cost_model' OR instance_name ends_with '_cost_model'
message: "Cost calc '{name}' should be named 'cost_model' for consistency"
```

#### Enforcement Rule E3: Leaf Part Direct Calculation

```yaml
rule_id: E3-LEAF-DIRECT-CALC
severity: ERROR
description: "Leaf parts must have direct cost calculation"
check:
  for_each: PartUsage where type :> 'Costed Component' AND has_no_costed_children
  condition: has cost_model calc usage OR capital_cost has expression
message: "Leaf part '{name}' needs cost_model or capital_cost expression"
```

#### Enforcement Rule E4: Assembly Aggregation

```yaml
rule_id: E4-ASSEMBLY-AGGREGATION
severity: ERROR
description: "Assembly parts must aggregate all child costs"
check:
  for_each: PartUsage where type :> 'Costed Component' AND has_costed_children
  condition: capital_cost expression references ALL costed children
message: "Assembly '{name}' capital_cost doesn't include all children"
```

#### Enforcement Rule E5: Material Cost Tracking

```yaml
rule_id: E5-MATERIAL-TRACKING
severity: WARNING
description: "Leaf parts should track raw_material_cost for idiot index"
check:
  for_each: PartUsage where type :> 'Costed Component' AND has_no_costed_children
  condition: attribute 'raw_material_cost' exists AND is bound
message: "Leaf part '{name}' missing raw_material_cost (needed for idiot index)"
```

#### Enforcement Rule E6: Standard Outputs Present

```yaml
rule_id: E6-STANDARD-OUTPUTS
severity: ERROR
description: "Top-level plant must expose StandardCostOutputs"
check:
  for_each: PartUsage where is_top_level_plant
  condition: all_standard_outputs_bound  # 30+ required outputs
message: "Plant missing required standard cost outputs"
```

---

### Q4: Does EVERY part need a cost, or should assemblies cover children?

**Recommendation: Hybrid approach based on part role**

#### Decision Matrix

| Part Type | Has Children? | Cost Calc Location | capital_cost Source |
|-----------|---------------|-------------------|---------------------|
| **Leaf Component** | No | Inside part def | `= cost_model.total_cost` |
| **Simple Assembly** | Yes (few) | None (aggregation only) | `= Σ(child.capital_cost) + overhead` |
| **Complex Assembly** | Yes (many) | Optional assembly calc | `= Σ(child.capital_cost) + assembly_model.cost` |
| **System-Level** | Yes (subsystems) | LCOE calc only | `= Σ(subsystem.capital_cost)` |

#### Example: CAS22 Hierarchy

```
CAS22 Reactor Plant Equipment
├── [ASSEMBLY] CAS220100 First Level Equipment
│   ├── [LEAF] CAS220101 Reactor Equipment (blanket)
│   │   └── cost_model: ReactorEquipmentCost
│   ├── [LEAF] CAS220102 Shield
│   │   └── cost_model: ShieldCost
│   ├── [LEAF] CAS220103 Magnets
│   │   └── cost_model: MagnetCost
│   ├── [LEAF] CAS220108 Divertor
│   │   └── cost_model: DivertorCost
│   └── [AGGREGATE] C220100 = sum of above
├── [LEAF] CAS220200 Coolant System
│   └── cost_model: CoolantSystemCost
├── [LEAF] CAS220300 Auxiliary Cooling
│   └── cost_model: AuxCoolingCost
└── [AGGREGATE] CAS22 = sum of CAS2201xx + CAS220200...
```

**Key Insight**: The CAS structure in PyFECONS already follows this pattern - leaf codes (CAS220101) have direct calculations, parent codes (CAS220100, CAS22) are pure aggregations.

---

## Part 2: Output Structure Design

### Q5: What should the output look like?

**Recommendation: Structured cost object with BOM-like hierarchy**

#### Output Schema Design

```python
@dataclass
class CostLineItem:
    """Single line item in cost output."""
    # Identity
    cas_code: str                    # "CAS220103"
    name: str                        # "TF Coil System"
    qualified_path: str              # "catf.reactor.magnets.tf_coils"

    # Cost Breakdown
    raw_material_cost: float         # $M - materials only
    fabrication_cost: float          # $M - manufacturing labor/overhead
    installation_cost: float         # $M - on-site assembly
    total_cost: float                # $M - sum of above

    # Estimation Metadata (AACE-aligned)
    estimation_method: EstimationMethod  # See enum below
    aace_class: AACEEstimateClass        # Industry standard classification
    data_source: str                     # "PyFECONS CAS220103"
    basis_of_estimate: str               # Documentation reference

    # Efficiency Metrics
    idiot_index: float              # total_cost / raw_material_cost
    cost_per_unit: float            # $M per unit (for arrayed parts)
    quantity: int                   # Number of units

    # Hierarchy
    parent_path: str                # "catf.reactor.magnets"
    children: list[str]             # ["catf.reactor.magnets.tf_coils.conductor", ...]
    level: int                      # 0=plant, 1=system, 2=subsystem, 3=component
    is_leaf: bool                   # True if no costed children

@dataclass
class CostBreakdownReport:
    """Full cost report with hierarchy."""
    # Header
    design_name: str                # "CATF MFE v1.0"
    timestamp: str                  # ISO format

    # Summary
    total_capital_cost: float       # $M
    overnight_cost_per_kw: float    # $/kW
    lcoe: float                     # $/MWh

    # Hierarchical Breakdown
    line_items: list[CostLineItem]  # Flat list, hierarchically ordered

    # Aggregated Views
    by_cas_category: dict[str, float]    # CAS20, CAS21, CAS22, ...
    by_estimation_method: dict[str, float]  # parametric, analogous, ...
    by_confidence_band: dict[str, float]    # high (>0.8), medium, low

    # Efficiency Summary
    idiot_indices: dict[str, float]      # Component → index
    high_idiot_index_flags: list[str]    # Components with index > threshold
```

#### Table Output Format (Human-Readable)

```
COST BREAKDOWN: CATF MFE v1.0
Generated: 2026-01-10T14:30:00-08:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAS CODE  │ NAME                    │ MATERIAL  │ FAB      │ INSTALL  │ TOTAL    │ IDIOT
          │                         │ ($M)      │ ($M)     │ ($M)     │ ($M)     │ INDEX
──────────┼─────────────────────────┼───────────┼──────────┼──────────┼──────────┼───────
CAS20     │ DIRECT CAPITAL          │           │          │          │ 4,521.3  │
├─CAS21   │ Buildings & Site        │    45.2   │   120.4  │    34.2  │   199.8  │  4.4
├─CAS22   │ Reactor Plant Equipment │           │          │          │ 3,247.1  │
│ ├─220101│   Blanket & First Wall  │   142.3   │   285.1  │    42.8  │   470.2  │  3.3
│ ├─220102│   Shield                │    89.1   │   178.2  │    26.7  │   294.0  │  3.3
│ ├─220103│   Magnets               │   412.8   │   619.2  │   185.7  │ 1,217.7  │  2.9 ⚠
│ │ └─TF  │     TF Coil System      │   312.4   │   468.6  │   140.6  │   921.6  │  2.9
│ │ └─PF  │     PF Coil System      │   100.4   │   150.6  │    45.1  │   296.1  │  2.9
│ ├─220104│   Heating Systems       │    78.2   │   117.3  │    35.2  │   230.7  │  2.9
│ ├─220105│   Primary Structure     │    56.7   │   113.4  │    34.0  │   204.1  │  3.6
│ ├─220106│   Vacuum System         │    23.4   │    46.8  │    14.0  │    84.2  │  3.6
│ ├─220107│   Power Supplies        │    45.6   │    91.2  │    27.4  │   164.2  │  3.6
│ ├─220108│   Divertor              │    67.8   │   135.6  │    40.7  │   244.1  │  3.6
│ └─220111│   Installation          │     0.0   │     0.0  │   337.9  │   337.9  │  N/A
├─CAS23   │ Turbine Plant Equipment │   234.5   │   351.7  │   105.5  │   691.7  │  2.9
├─CAS24   │ Electric Plant          │    89.3   │   133.9  │    40.2  │   263.4  │  2.9
└─CAS25-28│ Misc & Special Materials│    56.2   │    84.3  │    25.3  │   165.8  │  2.9
CAS30     │ INDIRECT SERVICE        │           │          │          │   678.2  │
CAS40     │ OWNER'S COST            │           │          │          │   452.1  │
CAS50     │ SUPPLEMENTARY           │           │          │          │   135.6  │
CAS60     │ FINANCIAL               │           │          │          │   339.1  │
──────────┼─────────────────────────┼───────────┼──────────┼──────────┼──────────┼───────
TOTAL     │ CAPITAL COST            │ 1,341.1   │ 2,477.1  │   979.6  │ 6,126.3  │  4.6
          │ $/kW (overnight)        │           │          │          │  6,126   │
          │ LCOE                    │           │          │          │    78.4  │ $/MWh
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTIMATION METHOD BREAKDOWN:
  Parametric:    82.3%  ($5,041.7M) - Physics-based scaling laws
  Analogous:     12.4%  ($759.5M)   - Historical comparison (ITER, SPARC)
  Engineering:    5.3%  ($325.1M)   - Bottom-up build-up

IDIOT INDEX FLAGS (> 5.0):
  ⚠ None detected - all components within reasonable range

CONFIDENCE SUMMARY:
  High (>0.8):   45.2%  - Well-validated parameters
  Medium:        42.1%  - Standard assumptions
  Low (<0.5):    12.7%  - Uncertain parameters
```

#### Estimation Metadata: AACE Classification System

**AACE International** (Association for the Advancement of Cost Engineering) defines a **5-class estimate classification system** that is the industry standard. We adopt this instead of generic "confidence levels."

**AACE Estimate Classes (AACE 18R-97)**:

| Class | Project Definition | Accuracy Range | Primary Use | Typical Methods |
|-------|-------------------|----------------|-------------|-----------------|
| **Class 5** | 0-2% defined | -20% to -50% / +30% to +100% | Concept screening, feasibility | Analogous, capacity-factored |
| **Class 4** | 1-15% defined | -15% to -30% / +20% to +50% | Study, feasibility | Parametric, analogous |
| **Class 3** | 10-40% defined | -10% to -20% / +10% to +30% | Budget authorization, control | Semi-detailed, parametric |
| **Class 2** | 30-75% defined | -5% to -15% / +5% to +20% | Bid/tender, detailed control | Detailed, unit cost |
| **Class 1** | 65-100% defined | -3% to -10% / +3% to +15% | Check estimate, bid validation | Detailed, actual costs |

**Enum Definitions for Output Schema**:

```python
from enum import Enum

class EstimationMethod(str, Enum):
    """Primary method used for cost estimate."""
    ANALOGOUS = "analogous"           # Based on similar historical system
    PARAMETRIC = "parametric"         # Using cost estimating relationships (CERs)
    ENGINEERING = "engineering"       # Detailed bottom-up from engineering data
    EXPERT_JUDGMENT = "expert"        # Subject matter expert opinion
    VENDOR_QUOTE = "vendor"           # Based on supplier quotation
    ACTUAL = "actual"                 # From actual incurred costs

class AACEEstimateClass(int, Enum):
    """AACE 18R-97 estimate classification."""
    CLASS_5 = 5  # Concept screening: -20/-50% to +30/+100%
    CLASS_4 = 4  # Study/feasibility: -15/-30% to +20/+50%
    CLASS_3 = 3  # Budget authorization: -10/-20% to +10/+30%
    CLASS_2 = 2  # Bid/tender: -5/-15% to +5/+20%
    CLASS_1 = 1  # Check estimate: -3/-10% to +3/+15%

    @property
    def accuracy_low(self) -> tuple[float, float]:
        """Return (optimistic%, pessimistic%) for low range."""
        ranges = {5: (-50, -20), 4: (-30, -15), 3: (-20, -10), 2: (-15, -5), 1: (-10, -3)}
        return ranges[self.value]

    @property
    def accuracy_high(self) -> tuple[float, float]:
        """Return (optimistic%, pessimistic%) for high range."""
        ranges = {5: (+30, +100), 4: (+20, +50), 3: (+10, +30), 2: (+5, +20), 1: (+3, +15)}
        return ranges[self.value]
```

**SysML Attribute Definition Pattern**:

```sysml
attribute def 'Estimate Metadata' {
    doc /*
    Metadata for cost estimate traceability.
    Based on AACE 18R-97 classification system.
    */

    // Method used
    attribute estimation_method : String;  // analogous, parametric, engineering, etc.

    // AACE class (1-5, where 1 is most accurate)
    attribute aace_class : Integer;

    // Accuracy range derived from AACE class
    attribute accuracy_low_pct : Real;     // e.g., -15% for Class 4
    attribute accuracy_high_pct : Real;    // e.g., +50% for Class 4

    // Documentation
    attribute data_source : String;        // "PyFECONS CAS220103"
    attribute basis_of_estimate : String;  // Reference to BOE document

    // Timestamps
    attribute estimate_date : String;      // ISO format
    attribute last_updated : String;
}

// Usage in Costed Component
abstract part def 'Costed Component' {
    attribute capital_cost : Real;
    attribute cost_metadata : 'Estimate Metadata';
}
```

**Fusion TEA Guidelines for AACE Class Selection**:

| Cost Element | Typical AACE Class | Rationale |
|--------------|-------------------|-----------|
| **Magnets (TF/PF)** | Class 4 | Parametric from ITER/SPARC data, ~15% defined |
| **Blanket** | Class 4-5 | Novel designs, limited historical data |
| **Divertor** | Class 4 | Some ITER precedent, but design-specific |
| **Buildings** | Class 3 | Good industrial precedent for similar facilities |
| **Turbine/BOP** | Class 3 | Standard industrial equipment |
| **Power supplies** | Class 3-4 | Commercial equipment with scaling |
| **Special materials (tritium)** | Class 5 | High uncertainty, limited precedent |

#### JSON Output Format (Machine-Readable)

```json
{
  "design_name": "CATF MFE v1.0",
  "timestamp": "2026-01-10T14:30:00-08:00",
  "summary": {
    "total_capital_cost_m_usd": 6126.3,
    "overnight_cost_per_kw": 6126,
    "lcoe_per_mwh": 78.4
  },
  "line_items": [
    {
      "cas_code": "CAS220103",
      "name": "Magnets",
      "qualified_path": "catf.reactor.magnets",
      "raw_material_cost": 412.8,
      "fabrication_cost": 619.2,
      "installation_cost": 185.7,
      "total_cost": 1217.7,
      "estimation_method": "parametric",
      "aace_class": 4,
      "accuracy_range": {"low": -30, "high": +50},
      "data_source": "PyFECONS CAS220103",
      "basis_of_estimate": "ARIES-AT magnet scaling + SPARC cost data",
      "idiot_index": 2.9,
      "parent_path": "catf.reactor",
      "children": ["catf.reactor.magnets.tf_coils", "catf.reactor.magnets.pf_coils"],
      "level": 2,
      "is_leaf": false
    }
  ],
  "aggregated": {
    "by_cas_category": {"CAS20": 4521.3, "CAS21": 199.8, "CAS22": 3247.1},
    "by_estimation_method": {"parametric": 5041.7, "analogous": 759.5, "engineering": 325.1},
    "by_aace_class": {"class_3": 1200.4, "class_4": 4125.2, "class_5": 800.7}
  },
  "uncertainty": {
    "p10_total": 4891.0,
    "p50_total": 6126.3,
    "p90_total": 9189.5,
    "notes": "P10/P90 derived from AACE class accuracy ranges via Monte Carlo"
  },
  "efficiency": {
    "idiot_indices": {"magnets": 2.9, "blanket": 3.3, "divertor": 3.6},
    "high_idiot_index_flags": []
  }
}
```

---

### Q6: How to support the "idiot index" (commodity multiple)?

**Recommendation: Track material costs at leaf level, propagate up**

#### Idiot Index Pattern

```sysml
// === Library: Extended Costed Component ===
abstract part def 'Costed Component' {
    // Required
    attribute capital_cost : Real;           // Total finished cost

    // For idiot index (optional but recommended)
    attribute raw_material_cost : Real default := 0.0;

    // Computed efficiency metric
    attribute idiot_index : Real =
        raw_material_cost > 0.0 ? capital_cost / raw_material_cost : 0.0;

    // Breakdown (for BOM-like output)
    attribute fabrication_cost : Real default := 0.0;
    attribute installation_cost : Real default := 0.0;
}

// === Library: Leaf Part Example ===
part def 'TF Conductor' :> 'Costed Component' {
    attribute tape_length : Real;        // [m]
    attribute tape_current_rating : Real; // [kA]
    attribute hts_cost_per_ka_m : Real = 150.0;  // $/kA-m (2025 market)

    calc cost_model : TFConductorCost {
        in length = tape_length;
        in rating = tape_current_rating;
        in unit_cost = hts_cost_per_ka_m;
    }

    // Material cost (direct)
    :>> raw_material_cost = cost_model.material_cost;

    // Fabrication (winding, insulation, testing)
    :>> fabrication_cost = cost_model.fabrication_cost;

    // Installation (on-site connection)
    :>> installation_cost = cost_model.installation_cost;

    // Total
    :>> capital_cost = cost_model.total_cost;

    // Idiot index computed automatically: capital_cost / raw_material_cost
}

// === Library: Assembly Example ===
part def 'TF Coil System' :> 'Costed Component' {
    part conductor : 'TF Conductor' [12] { ... }
    part structure : 'TF Structure' [12] { ... }

    // AGGREGATE material costs from children
    :>> raw_material_cost = conductor.raw_material_cost + structure.raw_material_cost;

    // AGGREGATE fabrication costs
    :>> fabrication_cost = conductor.fabrication_cost + structure.fabrication_cost;

    // Assembly-level installation (integration, testing)
    attribute integration_cost : Real;
    :>> installation_cost =
        conductor.installation_cost +
        structure.installation_cost +
        integration_cost;

    // Total
    :>> capital_cost = raw_material_cost + fabrication_cost + installation_cost;

    // Idiot index = 1217.7 / 412.8 = 2.9 (reasonable for complex system)
}
```

#### Calc Def Pattern for Leaf Parts

```sysml
calc def TFConductorCost {
    doc /*
    TF coil conductor cost with full breakdown.

    **Source**: PyFECONS CAS220103
    **Formula**: Material + Fabrication + Installation
    **Idiot Index Expectation**: 2.5-3.5 for HTS conductors
    */

    in attribute length : Real;           // [m] tape length
    in attribute current_rating : Real;   // [kA] operating current
    in attribute hts_cost_per_ka_m : Real default := 150.0;  // [$/kA-m]

    // === MATERIAL COST ===
    out attribute material_cost : Real =
        length * current_rating * hts_cost_per_ka_m / 1.0e6;  // [$M]

    // === FABRICATION COST ===
    // Winding, insulation, testing (typically 50% of material)
    in attribute fabrication_factor : Real default := 0.5;
    out attribute fabrication_cost : Real = material_cost * fabrication_factor;

    // === INSTALLATION COST ===
    // On-site handling, connection, commissioning (typically 15% of material)
    in attribute installation_factor : Real default := 0.15;
    out attribute installation_cost : Real = material_cost * installation_factor;

    // === TOTAL ===
    out attribute total_cost : Real =
        material_cost + fabrication_cost + installation_cost;

    // === EFFICIENCY METRICS ===
    out attribute idiot_index : Real = total_cost / material_cost;
    out attribute material_fraction : Real = material_cost / total_cost;
    out attribute fabrication_fraction : Real = fabrication_cost / total_cost;
    out attribute installation_fraction : Real = installation_cost / total_cost;
}
```

---

## Part 3: Implementation Strategy

### Algorithm: Recursive Cost Traversal

Based on the fusion-simkit exploration, here's how cost rollup can work:

```python
def build_cost_hierarchy(model) -> dict[str, CostNode]:
    """Build hierarchy from SysML model."""
    nodes = {}

    # 1. Find all parts typed by 'Costed Component'
    for part_usage in model.nodes(PartUsage):
        if is_costed_component(part_usage):
            node = CostNode(
                name=part_usage.name,
                qualified_path=build_path(part_usage),
                parent=get_parent_path(part_usage),
                children=get_costed_children(part_usage),
                is_leaf=len(get_costed_children(part_usage)) == 0
            )
            nodes[node.qualified_path] = node

    return nodes

def execute_cost_rollup(nodes: dict, calc_results: dict) -> dict:
    """Execute costs in topological order (leaves first)."""
    # Topological sort: leaves before parents
    order = topological_sort(nodes)

    results = {}
    for path in order:
        node = nodes[path]

        if node.is_leaf:
            # Get cost from calc usage result
            cost_data = calc_results.get(f"{path}.cost_model")
            results[path] = CostLineItem(
                raw_material_cost=cost_data.material_cost,
                fabrication_cost=cost_data.fabrication_cost,
                installation_cost=cost_data.installation_cost,
                total_cost=cost_data.total_cost,
                idiot_index=cost_data.idiot_index
            )
        else:
            # Aggregate from children
            child_costs = [results[c] for c in node.children]
            results[path] = CostLineItem(
                raw_material_cost=sum(c.raw_material_cost for c in child_costs),
                fabrication_cost=sum(c.fabrication_cost for c in child_costs),
                installation_cost=sum(c.installation_cost for c in child_costs),
                total_cost=sum(c.total_cost for c in child_costs),
                idiot_index=compute_aggregate_idiot_index(child_costs)
            )

    return results
```

### Integration with teax-simkit

The existing pipeline executor already supports this via channel aggregation:

```yaml
# Generated pipeline with cost rollup
modules:
  tf_conductor_cost_model:
    class: TFConductorCostModule
    inputs:
      length: {value: 5000.0}
      current_rating: {value: 70.0}
    outputs: [material_cost, fabrication_cost, installation_cost, total_cost, idiot_index]

  pf_conductor_cost_model:
    class: PFConductorCostModule
    # ...

  # Post-processor for aggregation
  cost_rollup:
    class: CostRollupModule
    inputs:
      tf_cost: module.tf_conductor_cost_model.total_cost
      pf_cost: module.pf_conductor_cost_model.total_cost
      tf_material: module.tf_conductor_cost_model.material_cost
      pf_material: module.pf_conductor_cost_model.material_cost
    outputs: [magnet_total_cost, magnet_material_cost, magnet_idiot_index]

exit_points:
  - {name: cas220103_magnet_cost, channel: cost_rollup.magnet_total_cost}
  - {name: cas220103_material_cost, channel: cost_rollup.magnet_material_cost}
  - {name: cas220103_idiot_index, channel: cost_rollup.magnet_idiot_index}
```

---

## Part 4: Design Alternatives Comparison

### Alternative A: Nested Cost Models (Recommended Long-Term)

**Description**: Cost calc usages inside part definitions

**Pros**:
- Clean design files (just instantiate parts)
- Co-located structure + cost
- Automatic cost when part instantiated
- Matches industry BOM pattern

**Cons**:
- Requires sysml-codegen enhancement
- Tooling gap exists today

**Example**:
```sysml
// Library
part def 'Magnet System' :> 'Costed Component' {
    calc cost_model : MagnetSystemCostCalc { ... }
    :>> capital_cost = cost_model.total_cost;
}

// Design (clean!)
part catf_plant {
    part magnets : 'Magnet System' {
        :>> field_strength = 12.0;  // Just set parameters
    }
    // Cost automatically computed!
}
```

### Alternative B: Explicit Wiring (Recommended Immediate)

**Description**: Cost calc usages in design files, explicit wiring

**Pros**:
- Works with current tooling
- Clear, auditable
- No sysml-codegen changes needed

**Cons**:
- Verbose design files
- Risk of forgetting to wire a part
- Duplicates part-to-calc mapping

**Example**:
```sysml
// Library
part def 'Magnet System' :> 'Costed Component' {
    // No embedded calc
}

// Design (verbose but works)
part catf_plant {
    part magnets : 'Magnet System' {
        :>> field_strength = 12.0;
        :>> coil_volume = 150.0;
    }

    // EXPLICIT wiring
    calc magnet_cost_model : MagnetSystemCostCalc {
        in field = magnets.field_strength;
        in volume = magnets.coil_volume;
    }

    // Manual binding
    :> magnets.capital_cost = magnet_cost_model.total_cost;
}
```

### Alternative C: Hybrid Approach (Recommended Transition)

**Description**: Use explicit wiring now, migrate to nested when tooling ready

**Pros**:
- Works today
- Clear migration path
- Validates patterns before tooling investment

**Cons**:
- Intermediate complexity
- Requires refactoring later

**Implementation Path**:
1. **Now**: Use Alternative B (explicit wiring)
2. **Phase 2**: Implement sysml-codegen enhancements
3. **Phase 3**: Migrate to Alternative A (nested)
4. **Ongoing**: Maintain both patterns during transition

---

## Part 5: Runtime Validation and Sanity Checks

### Where in the Pipeline Can We Enforce Checks?

Our cost modeling pipeline has three validation layers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   LAYER 1: Model Structure (agentic-mbse)                                   │
│   ├─ SysML parsing (syside check)                                           │
│   ├─ Level 9 rules (E1-E6) - interface compliance                           │
│   └─ Calc def input/output validation                                       │
│                                                                              │
│   LAYER 2: Design-Time Constraints (SysML constraint defs)                  │
│   ├─ Physical bounds (cost > 0, mass > 0)                                   │
│   ├─ High-level parametric cross-checks                                     │
│   └─ Ratio sanity checks (idiot index bounds)                              │
│                                                                              │
│   LAYER 3: Runtime Validation (teax-simkit post-execution)                  │
│   ├─ Rollup consistency (sum of children == parent)                         │
│   ├─ Part count verification                                                │
│   ├─ Cross-check against high-level parametrics                             │
│   └─ Historical comparison bounds                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Layer 2: Design-Time Constraints (SysML `constraint def`)

**Purpose**: Catch obvious errors before execution

#### Pattern: Physical Bound Constraints

```sysml
constraint def PositiveCost {
    doc /* All cost values must be positive */
    in attribute cost : Real;
    cost > 0.0
}

constraint def ReasonableIdiotIndex {
    doc /* Idiot index should be 1.0 < index < 20.0 for most components */
    in attribute idiot_index : Real;
    idiot_index > 1.0 and idiot_index < 20.0
}

constraint def MaterialFractionBounds {
    doc /* Material cost should be 20-80% of total for manufactured items */
    in attribute material_cost : Real;
    in attribute total_cost : Real;
    attribute material_fraction : Real = material_cost / total_cost;
    material_fraction > 0.2 and material_fraction < 0.8
}
```

**Usage in Part Definition**:
```sysml
part def 'TF Conductor' :> 'Costed Component' {
    attribute capital_cost : Real;
    attribute raw_material_cost : Real;

    // Apply constraints
    assert constraint cost_positive : PositiveCost {
        in cost = capital_cost;
    }

    assert constraint idiot_reasonable : ReasonableIdiotIndex {
        in idiot_index = capital_cost / raw_material_cost;
    }
}
```

#### Pattern: High-Level Parametric Cross-Checks

Cross-check detailed bottom-up costs against simple parametrics:

```sysml
constraint def MagnetCostCrossCheck {
    doc /*
    Magnet system cost cross-check against high-level parametric.

    Parametric: Cost ~ 0.05 × B^4 × V_coil [$M]
    Where B = field strength [T], V = coil volume [m³]

    Bottom-up should be within ±50% of parametric (AACE Class 4)
    */

    in attribute bottom_up_cost : Real;      // [$M] from detailed calcs
    in attribute field_strength : Real;       // [T]
    in attribute coil_volume : Real;          // [m³]

    // High-level parametric estimate
    attribute parametric_cost : Real = 0.05 * field_strength ** 4 * coil_volume;

    // Bottom-up should be within 50% of parametric
    attribute ratio : Real = bottom_up_cost / parametric_cost;
    ratio > 0.5 and ratio < 2.0
}

// Usage in design
part catf_plant {
    part magnets : 'Magnet System' {
        :>> field_strength = 12.0;
        :>> coil_volume = 150.0;
    }

    // Cross-check constraint
    assert constraint magnet_sanity : MagnetCostCrossCheck {
        in bottom_up_cost = magnets.capital_cost;
        in field_strength = magnets.field_strength;
        in coil_volume = magnets.coil_volume;
    }
}
```

#### Pattern: Rollup Consistency Constraint

```sysml
constraint def RollupConsistency {
    doc /*
    Verify that parent cost equals sum of children.
    Catches missing children or double-counting.
    */

    in attribute parent_cost : Real;
    in attribute child_costs : Real[*];      // Array of child costs
    in attribute overhead : Real default := 0.0;
    in attribute tolerance_pct : Real default := 0.01;  // 1%

    attribute child_sum : Real = child_costs->sum();
    attribute expected : Real = child_sum + overhead;

    // Within tolerance
    (parent_cost - expected).abs() / expected < tolerance_pct
}
```

### Layer 3: Runtime Validation (teax-simkit)

**Purpose**: Validate computed results after execution

#### Implementation: Post-Execution Validator Module

```python
from dataclasses import dataclass
from simkit.core.module import SimkitModule, Input, Output

@dataclass
class CostValidationResult:
    passed: bool
    checks: list[dict]
    warnings: list[str]
    errors: list[str]

class CostSanityValidator(SimkitModule):
    """Post-execution validation for cost outputs."""

    # === INPUTS: All computed costs ===
    cas22_reactor: Input[float]
    cas22_magnets: Input[float]
    cas22_blanket: Input[float]
    cas22_divertor: Input[float]
    # ... more CAS categories

    total_capital: Input[float]
    lcoe: Input[float]

    # === REFERENCE DATA ===
    p_fusion: Input[float]  # For scaling checks
    p_net: Input[float]

    # === OUTPUT ===
    validation_result: Output[CostValidationResult]

    def run(self) -> CostValidationResult:
        checks = []
        warnings = []
        errors = []

        # Check 1: Rollup consistency
        cas22_sum = (
            self.cas22_magnets.value +
            self.cas22_blanket.value +
            self.cas22_divertor.value +
            # ... other components
        )
        rollup_error = abs(self.cas22_reactor.value - cas22_sum) / cas22_sum
        checks.append({
            "name": "CAS22 Rollup",
            "expected": cas22_sum,
            "actual": self.cas22_reactor.value,
            "error_pct": rollup_error * 100,
            "passed": rollup_error < 0.01
        })
        if rollup_error >= 0.01:
            errors.append(f"CAS22 rollup error: {rollup_error:.1%}")

        # Check 2: Overnight cost per kW bounds
        overnight_per_kw = self.total_capital.value * 1000 / self.p_net.value
        checks.append({
            "name": "Overnight $/kW bounds",
            "value": overnight_per_kw,
            "expected_range": [3000, 15000],
            "passed": 3000 < overnight_per_kw < 15000
        })
        if overnight_per_kw < 3000:
            warnings.append(f"Overnight cost ${overnight_per_kw:.0f}/kW suspiciously low")
        if overnight_per_kw > 15000:
            warnings.append(f"Overnight cost ${overnight_per_kw:.0f}/kW very high")

        # Check 3: LCOE bounds
        checks.append({
            "name": "LCOE bounds",
            "value": self.lcoe.value,
            "expected_range": [30, 200],
            "passed": 30 < self.lcoe.value < 200
        })

        # Check 4: CAS22 as fraction of total
        cas22_fraction = self.cas22_reactor.value / self.total_capital.value
        checks.append({
            "name": "CAS22 fraction of total",
            "value": cas22_fraction,
            "expected_range": [0.3, 0.7],
            "passed": 0.3 < cas22_fraction < 0.7
        })

        passed = len(errors) == 0
        return CostValidationResult(
            passed=passed,
            checks=checks,
            warnings=warnings,
            errors=errors
        )
```

#### Implementation: Part Count Tracking

Track quantities through the rollup process:

```python
@dataclass
class PartCountSummary:
    """Track part quantities for BOM verification."""
    part_path: str
    part_type: str
    quantity: int
    unit_cost: float
    total_cost: float
    children: list["PartCountSummary"]

class PartCountTracker(SimkitModule):
    """Track and verify part counts through cost rollup."""

    # Inputs from model (populated by sysml-codegen)
    tf_coil_count: Input[int]      # Expected: 12-18 for tokamak
    pf_coil_count: Input[int]      # Expected: 6-10
    blanket_module_count: Input[int]  # Expected: 16-48
    divertor_cassette_count: Input[int]  # Expected: 48-64

    # Costs
    tf_coil_unit_cost: Input[float]
    pf_coil_unit_cost: Input[float]
    blanket_module_unit_cost: Input[float]

    # Outputs
    part_count_report: Output[dict]
    total_major_components: Output[int]

    def run(self) -> dict:
        report = {
            "tf_coils": {
                "count": self.tf_coil_count.value,
                "unit_cost": self.tf_coil_unit_cost.value,
                "total_cost": self.tf_coil_count.value * self.tf_coil_unit_cost.value,
                "expected_range": [12, 18],
                "in_range": 12 <= self.tf_coil_count.value <= 18
            },
            "pf_coils": {
                "count": self.pf_coil_count.value,
                # ...
            },
            "blanket_modules": {
                "count": self.blanket_module_count.value,
                # ...
            },
        }

        total = sum(item["count"] for item in report.values())

        return {
            "report": report,
            "total_major_components": total,
            "all_counts_valid": all(item["in_range"] for item in report.values())
        }
```

#### Pipeline Integration

Add validation modules to generated pipeline:

```yaml
# Generated pipeline with validation
modules:
  # ... cost calculation modules ...

  # POST-EXECUTION VALIDATION
  cost_validator:
    class: CostSanityValidator
    inputs:
      cas22_reactor: module.cas22_rollup.total
      cas22_magnets: module.magnet_cost_model.total_cost
      cas22_blanket: module.blanket_cost_model.total_cost
      total_capital: module.lcoe_calc.total_capital
      lcoe: module.lcoe_calc.lcoe
      p_net: entry_point.p_net
    outputs: [validation_result]

  part_count_tracker:
    class: PartCountTracker
    inputs:
      tf_coil_count: entry_point.n_tf_coils
      pf_coil_count: entry_point.n_pf_coils
      blanket_module_count: entry_point.n_blanket_modules
      tf_coil_unit_cost: module.tf_coil_cost_model.cost_per_coil
    outputs: [part_count_report, total_major_components]

exit_points:
  - {name: validation_result, channel: cost_validator.validation_result}
  - {name: part_counts, channel: part_count_tracker.part_count_report}
```

### Enforcement Rule Summary for Runtime Checks

| Check Type | Layer | Mechanism | When Triggered |
|------------|-------|-----------|----------------|
| Positive costs | 2 | `constraint def` | Model parsing |
| Idiot index bounds | 2 | `constraint def` | Model parsing |
| Material fraction | 2 | `constraint def` | Model parsing |
| Parametric cross-check | 2 | `constraint def` | Model parsing |
| Rollup consistency | 3 | Validator module | Post-execution |
| Historical bounds | 3 | Validator module | Post-execution |
| Part count verification | 3 | Tracker module | Post-execution |

---

## Part 6: Modeling Process Costs (Installation & Manufacturing)

### The Challenge

Your question highlights an important distinction:
- **Structural cost**: Cost of the physical artifact (materials + fabrication)
- **Process cost**: Cost of performing an activity (installation, manufacturing steps)

Our current pattern (`capital_cost = material + fabrication + installation`) bundles these together. For detailed analysis, we may want to model processes explicitly.

### SysMLv2 Pattern: Action Definitions for Processes

SysMLv2 uses `action def` for behaviors/processes. We can extend this for cost modeling:

```sysml
// === PROCESS DEFINITION ===
action def 'Install TF Coil' {
    doc /*
    Installation process for a single TF coil.
    Covers transport, positioning, connection, and testing.
    */

    // Process inputs (from structural parts)
    in item coil : 'TF Coil';
    in item support_structure : 'TF Support Structure';

    // Process parameters
    attribute crane_hours : Real;           // Heavy lift crane time
    attribute technician_hours : Real;      // Skilled labor
    attribute connection_count : Integer;   // Electrical + coolant connections

    // Sub-actions (sequential steps)
    action transport : 'Transport to Bay' {
        in item = coil;
        out duration : Real;
    }

    action position : 'Position on Support' {
        in item = coil;
        in support = support_structure;
        out duration : Real;
    }

    action connect : 'Make Connections' {
        in count = connection_count;
        out duration : Real;
    }

    action test : 'Functional Test' {
        out duration : Real;
    }

    // Total duration
    attribute total_duration : Real =
        transport.duration + position.duration + connect.duration + test.duration;
}
```

### Pattern: Process Cost Calculation

```sysml
calc def InstallationProcessCost {
    doc /*
    Calculate cost of an installation process.
    Based on duration, labor rates, and equipment costs.

    **Source**: Industrial installation standards
    **AACE Class**: 3-4 (well-understood processes)
    */

    // Process characteristics
    in attribute duration_hours : Real;
    in attribute technician_count : Integer;
    in attribute crane_required : Boolean;
    in attribute crane_hours : Real default := 0.0;

    // Cost rates
    in attribute technician_rate : Real default := 150.0;   // $/hour (loaded)
    in attribute crane_rate : Real default := 5000.0;       // $/hour
    in attribute overhead_factor : Real default := 1.25;    // 25% overhead

    // Cost calculation
    out attribute labor_cost : Real =
        duration_hours * technician_count * technician_rate / 1.0e6;

    out attribute equipment_cost : Real =
        crane_hours * crane_rate / 1.0e6;

    out attribute subtotal : Real = labor_cost + equipment_cost;

    out attribute total_cost : Real = subtotal * overhead_factor;

    // Metrics
    out attribute cost_per_hour : Real = total_cost / duration_hours;
}
```

### Integration with Structural Parts

**Option A: Process as Child of Assembly (Embedded)**

```sysml
part def 'TF Coil System' :> 'Costed Component' {
    // Structural children
    part conductor : 'TF Conductor' [12] { ... }
    part structure : 'TF Structure' [12] { ... }

    // Installation process (one per coil)
    perform action install_coil : 'Install TF Coil' [12] {
        in coil = conductor;
        in support_structure = structure;
        :>> crane_hours = 8.0;
        :>> technician_hours = 40.0;
        :>> connection_count = 24;
    }

    // Process cost calculation
    calc installation_cost_model : InstallationProcessCost {
        in duration_hours = install_coil.total_duration * 12;  // All coils
        in technician_count = 6;
        in crane_required = true;
        in crane_hours = install_coil.crane_hours * 12;
    }

    // Cost aggregation (structural + process)
    :>> capital_cost =
        conductor.capital_cost +
        structure.capital_cost +
        installation_cost_model.total_cost;

    // Separate tracking for analysis
    attribute structural_cost : Real = conductor.capital_cost + structure.capital_cost;
    :>> installation_cost = installation_cost_model.total_cost;
}
```

**Option B: Process as Separate CAS Category (PyFECONS Pattern)**

PyFECONS separates installation into CAS220111:

```sysml
package 'CATF Cost Analysis' {
    // Structural parts (CAS220101-220108)
    part reactor_equipment : 'Reactor Equipment' { ... }

    // Separate installation cost (CAS220111)
    calc cas220111_installation : PlantInstallationCost {
        doc /*
        CAS220111: Installation costs for reactor equipment.
        Calculated as % of equipment cost + specific process costs.
        */

        in equipment_cost = reactor_equipment.capital_cost;
        in equipment_mass = reactor_equipment.total_mass;

        // Installation factor (typically 15-25% for fusion)
        in installation_factor : Real default := 0.20;
    }

    // CAS22.1 total
    attribute cas220100 : Real =
        reactor_equipment.capital_cost +
        cas220111_installation.total_cost;
}
```

### Pattern: Manufacturing Process Cost

For specialized component manufacturing (e.g., HTS tape production):

```sysml
action def 'Manufacture HTS Conductor' {
    doc /*
    Manufacturing process for HTS tape conductor.
    Multi-step process with yield considerations.
    */

    // Process steps
    action deposit_buffer : 'IBAD Buffer Deposition' {
        attribute yield_rate : Real = 0.95;
        attribute throughput : Real;  // m/hour
    }

    action deposit_superconductor : 'MOCVD REBCO Deposition' {
        attribute yield_rate : Real = 0.90;
        attribute throughput : Real;
    }

    action slit_and_test : 'Slit and Test' {
        attribute yield_rate : Real = 0.98;
        attribute throughput : Real;
    }

    // Overall yield
    attribute cumulative_yield : Real =
        deposit_buffer.yield_rate *
        deposit_superconductor.yield_rate *
        slit_and_test.yield_rate;  // ~0.84
}

calc def ManufacturingProcessCost {
    doc /*
    Manufacturing cost based on process parameters.
    Accounts for yield losses and equipment amortization.
    */

    in attribute target_length : Real;           // [m] output needed
    in attribute cumulative_yield : Real;        // Process yield
    in attribute raw_material_cost : Real;       // $/m of substrate
    in attribute equipment_depreciation : Real;  // $/m amortized
    in attribute labor_cost_per_m : Real;        // $/m
    in attribute energy_cost_per_m : Real;       // $/m

    // Account for yield losses
    attribute gross_length : Real = target_length / cumulative_yield;

    out attribute material_cost : Real = gross_length * raw_material_cost / 1.0e6;
    out attribute equipment_cost : Real = gross_length * equipment_depreciation / 1.0e6;
    out attribute labor_cost : Real = gross_length * labor_cost_per_m / 1.0e6;
    out attribute energy_cost : Real = gross_length * energy_cost_per_m / 1.0e6;

    out attribute total_cost : Real =
        material_cost + equipment_cost + labor_cost + energy_cost;

    // Effective cost per meter of good output
    out attribute effective_cost_per_m : Real = total_cost * 1.0e6 / target_length;
}
```

### When to Use Process Modeling

| Scenario | Recommended Pattern | Rationale |
|----------|---------------------|-----------|
| Standard installation | Factor-based (15-25%) | Well-understood, low uncertainty |
| Complex installation | Process calc def | Many steps, equipment-intensive |
| Commodity manufacturing | Material multiplier (`m` factor) | PyFECONS pattern, simple |
| Specialized manufacturing | Process action + calc | Need yield tracking, step visibility |
| Construction sequence analysis | Action decomposition | Schedule-driven analysis |
| Labor learning curves | Process with iteration | N-th unit costs less than first |

### Summary: Process Cost Integration

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     COST STRUCTURE OPTIONS                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   SIMPLE (Current Pattern):                                                 │
│   capital_cost = raw_material + fabrication + installation                  │
│   ├─ raw_material: Volume × density × $/kg                                 │
│   ├─ fabrication: material × fab_factor                                    │
│   └─ installation: material × install_factor                               │
│                                                                             │
│   DETAILED (Process Modeling):                                              │
│   capital_cost = structural_cost + process_costs                           │
│   ├─ structural_cost:                                                      │
│   │   └─ Σ(child.capital_cost) for physical parts                         │
│   └─ process_costs:                                                        │
│       ├─ manufacturing_cost: action-based with yield                       │
│       └─ installation_cost: action-based with duration                     │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

**Recommendation**: Start with simple factor-based approach (Option B / PyFECONS pattern). Add detailed process modeling selectively for:
- High-uncertainty processes (novel manufacturing)
- Schedule-critical paths (installation sequence)
- Learning curve analysis (N-th-of-a-kind production)

---

## Summary: Recommended Principles

### Principle 1: Standardized Cost Interface
```
Every 'Costed Component' exposes:
- capital_cost (required)
- raw_material_cost (recommended)
- fabrication_cost (recommended)
- installation_cost (recommended)
- idiot_index (derived)
```

### Principle 2: Standardized Calc Naming
```
Cost calc usages SHOULD be named 'cost_model'
Enables pattern-based tooling and validation
```

### Principle 3: Clear Recursion Rules
```
LEAF parts: Direct cost calculation
ASSEMBLY parts: Pure aggregation of children + explicit overhead
NO hybrid parts mixing calculation and aggregation
```

### Principle 4: Enforcement via Validation
```
agentic-mbse Level 9 rules enforce:
- E1: Costed interface compliance
- E2: Cost model naming
- E3: Leaf direct calculation
- E4: Assembly aggregation
- E5: Material cost tracking
- E6: Standard outputs present
```

### Principle 5: Structured Output
```
Outputs include:
- Hierarchical breakdown (CAS-aligned)
- Per-line-item: material, fabrication, installation, total
- Efficiency metrics: idiot_index per component
- Estimation metadata: method, confidence, source
- Aggregated views: by category, by method, by confidence
```

### Principle 6: Idiot Index Tracking
```
For every material-intensive leaf part:
idiot_index = capital_cost / raw_material_cost

Flags when > 5.0 (indicates cost reduction opportunity)
Typical range: 2.5-4.0 for complex engineered systems
```

---

## References

### Prior Research (This Project)
- `modeling_pm/research/20260107-final-cost-architecture.md` - Nested cost model architecture
- `modeling_pm/research/20260106-065431_cost-architecture-patterns.md` - Initial patterns
- `modeling_pm/research/20260110-mbse-cost-modeling-best-practices.md` - Industry survey

### External Sources
- PyFECONS `/home/reid/PyFECONS` - CAS structure, cost formulas
- MIL-STD-881F - Work Breakdown Structure standard
- NASA WBS Handbook - Cost/WBS integration
- SpaceX "Idiot Index" - Manufacturing cost efficiency
- COSYSMO - Parametric cost modeling for MBSE

### Tooling
- sysml-codegen `usage_extractor.py` - Calc usage extraction
- sysml-codegen `dependency_backtracker.py` - Binding resolution
- teax-simkit `pipeline_executor.py` - Execution and channels

---

**Last Updated**: 2026-01-10
