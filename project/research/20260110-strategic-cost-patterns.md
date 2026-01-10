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

#### Rule R3: No Hybrid Parts (Partial Aggregation + Partial Direct Calculation)

**Anti-pattern to AVOID**:
```sysml
// BAD: Mixes direct calculation with partial aggregation
part def 'Confused Component' :> 'Costed Component' {
    part child_1 : 'Costed Child' { ... }

    // BAD: Does direct calc but also has costed child
    calc cost_model : SomeCostCalc { ... }

    :>> capital_cost = cost_model.total + child_1.capital_cost;  // UNCLEAR
}
```

**Rationale**:
- Clarity for traversal algorithms
- Prevents double-counting
- Matches BOM aggregation patterns (SAP, Oracle)

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

    # Estimation Metadata
    estimation_method: str           # "parametric", "analogous", "engineering"
    confidence_level: float          # 0.0-1.0
    data_source: str                 # "PyFECONS CAS220103"

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
      "confidence_level": 0.75,
      "data_source": "PyFECONS CAS220103",
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
    "by_confidence_band": {"high": 0.452, "medium": 0.421, "low": 0.127}
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
- `project/research/20260107-final-cost-architecture.md` - Nested cost model architecture
- `project/research/20260106-065431_cost-architecture-patterns.md` - Initial patterns
- `project/research/20260110-mbse-cost-modeling-best-practices.md` - Industry survey

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
