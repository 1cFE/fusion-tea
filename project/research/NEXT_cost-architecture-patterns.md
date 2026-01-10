# Follow-Up Research: Cost Architecture Patterns for Fusion TEA

**Status**: PENDING
**Priority**: High
**Depends On**: `20260106-050051_cost-modeling-lcoe-strategy.md`

## Context

Previous research established:
1. sysml-codegen extracts calc defs from library and calc usages from designs
2. Calc usages inside part defs are NOT instantiated when the part def is used
3. "Semantic cost models" (calc defs that encode domain knowledge) are preferred over "dumb math abstractions"
4. The pattern of pairing part defs with corresponding cost calc defs is viable

However, several critical architecture questions remain unanswered.

---

## Research Questions

### Q1: Single Instantiation Pattern

**Problem**: In the current pattern, a design must:
1. Instantiate structural parts (`part magnets : 'Magnet System'`)
2. Separately instantiate cost calcs (`calc magnet_cost : MagnetSystemCost`)
3. Wire them together (`in n_coils = magnets.n_coils`)

This is redundant and error-prone. If someone adds a subsystem but forgets to wire its cost calc, the cost is silently missing.

**Research Goal**: Find a pattern where instantiating ONE top-level part (e.g., `part catf_plant : 'CATF Fusion Plant'`) automatically includes all cost calculations.

**Questions to Investigate**:
- Can SysMLv2 constraint blocks or analysis cases help here?
- Is there a way to define a "cost view" that automatically wires to structure?
- Could sysml-codegen be enhanced to auto-generate cost calc usages based on conventions?
- What patterns exist in traditional MBSE for this problem?

**Consult**:
- SysMLv2 spec for analysis cases, viewpoints, and constraint blocks
- `agentic-mbse/docs/sysmlv2/` for relevant patterns
- PyFECONS structure for how it handles this in Python

---

### Q2: Scalable and Recursive Cost Patterns

**Problem**: Fusion plants have deep structural hierarchies:
```
Fusion Plant
├── Fusion Island (CAS22)
│   ├── Magnet System
│   │   ├── TF Coils
│   │   │   ├── Conductor
│   │   │   └── Structure
│   │   ├── PF Coils
│   │   └── CS Coil
│   ├── Blanket System
│   │   ├── Breeding Zone
│   │   └── First Wall
│   └── ...
├── Balance of Plant (CAS23-26)
└── ...
```

Cost must flow up this hierarchy: leaf components → subsystems → systems → plant total.

**Research Goal**: Define patterns that are:
- **Scalable**: Adding a new component at any level automatically includes its cost
- **Recursive**: The same pattern works at every level of hierarchy
- **Auditable**: Can trace any cost back to its source

**Questions to Investigate**:
- Should every part def expose a standard `total_cost` attribute?
- How do rollup calc defs reference child part costs generically?
- Can we use SysMLv2 collection operations (e.g., `parts.cost->sum()`)?
- What's the pattern for handling variable-count children (e.g., 12 TF coils)?

**Consult**:
- SysMLv2 spec for collection operations and derived attributes
- PyFECONS CAS account structure for hierarchical cost aggregation
- `fusion_modeling` models for existing patterns

---

### Q3: Enforcement via agentic-mbse

**Problem**: Conventions are only useful if they can be checked. Without enforcement:
- Someone might create a part def without a cost calc def
- Cost calc inputs might not match part def attributes
- Designs might forget to wire cost calcs

**Research Goal**: Define checking rules that can be implemented in `agentic-mbse` validation scripts.

**Questions to Investigate**:
- What validation hooks exist in `agentic-mbse`?
- Can we check that every part def specializing `'Costed Component'` has a corresponding calc def?
- Can we validate that calc def inputs are a subset of part def attributes?
- Can we check that all cost-bearing parts in a design have cost calc usages?
- How would these checks integrate with `/audit-models`?

**Consult**:
- `agentic-mbse` validation framework
- Existing checking scripts in `agentic-mbse/scripts/` or similar
- SysIDE/syside API for model introspection

---

### Q4: Standard Cost Output Schema

**Problem**: For designs to be comparable, they must produce the same output structure. If CATF outputs `total_cost` and stellarator outputs `capital_cost`, comparison is impossible.

**Research Goal**: Define a standard cost output schema that all designs must produce.

**Questions to Investigate**:
- What should the standard schema include? (Propose based on PyFECONS CAS structure)
- How can we enforce that all designs expose these outputs?
- Can we define a `CostOutputInterface` that top-level cost calcs must satisfy?
- How does this relate to teax-simkit's output routing?

**Proposed Schema Structure** (validate/refine during research):
```
Standard Cost Outputs:
├── Capital Costs
│   ├── cas20_direct_total
│   ├── cas21_buildings
│   ├── cas22_reactor_equipment
│   │   ├── cas22_magnets
│   │   ├── cas22_blanket
│   │   ├── cas22_divertor
│   │   └── ...
│   ├── cas23_turbine
│   ├── cas24_electric
│   ├── cas25_heat_rejection
│   ├── cas26_misc
│   └── cas27_special_materials
├── Indirect Costs
│   ├── cas30_indirect
│   ├── cas40_owners
│   └── cas50_financial
├── Operating Costs
│   ├── cas70_annual_om
│   ├── cas80_annual_fuel
│   └── cas90_annualized_capital
├── Summary Metrics
│   ├── total_capital_cost
│   ├── overnight_cost_per_kw
│   ├── lcoe
│   ├── lcoe_capital_fraction
│   ├── lcoe_om_fraction
│   └── lcoe_fuel_fraction
└── Breakdown Fractions
    ├── magnet_cost_fraction
    ├── blanket_cost_fraction
    └── ...
```

**Consult**:
- PyFECONS output structure
- teax-simkit output routing and schema capabilities
- sysml-codegen multi-output generation

---

### Q5: Extension to Full LCOE

**Problem**: Current focus has been on CapEx. Full LCOE requires:
- **OpEx**: Annual O&M costs (staff, maintenance, consumables)
- **Fuel**: Tritium costs, breeding economics
- **Lifecycle**: Replacement schedules, decommissioning
- **Financial**: Discount rates, construction period, financing costs
- **Energy Production**: Net power, availability, capacity factor

**Research Goal**: Extend the cost architecture to cover all LCOE components.

**Questions to Investigate**:
- What calc defs are needed for each LCOE component?
- How do lifecycle costs (replacements) integrate with CapEx?
- How do time-varying costs (inflation, learning curves) factor in?
- What attributes must part defs expose for lifecycle cost (e.g., `replacement_interval`)?
- How does availability modeling connect to LCOE?

**Consult**:
- PyFECONS LCOE calculation methodology
- `fusion_modeling` power balance models
- Industry LCOE calculation standards (IEA, NREL)

---

## Deliverables

1. **Pattern Definitions**: Concrete SysMLv2 patterns for each question, with examples
2. **Enforcement Rules**: Specific rules that can be implemented as agentic-mbse checks
3. **Schema Definition**: Standard cost output schema as SysMLv2 attribute def or interface
4. **Implementation Roadmap**: Ordered steps to implement the patterns
5. **Test Cases**: Minimal examples demonstrating each pattern works with sysml-codegen

---

## Research Approach

1. **SysMLv2 Patterns Research**: Use sysmlv2-doc-analyzer agent to find relevant spec patterns for:
   - Collection operations on part children
   - Derived attributes that aggregate child values
   - Interface/abstract patterns for enforcing structure
   - Analysis cases and viewpoints

2. **Tooling Investigation**: Examine sysml-codegen and agentic-mbse for:
   - Existing validation hooks
   - Extension points for new checks
   - How to add convention-based auto-generation

3. **PyFECONS Analysis**: Deep dive into PyFECONS for:
   - Complete LCOE calculation flow
   - All cost categories and their drivers
   - How lifecycle costs are annualized

4. **Prototype and Test**: Create minimal working examples to validate patterns work end-to-end with sysml-codegen and teax-simkit.

---

## Success Criteria

- [ ] Pattern defined where single design instantiation includes all costs
- [ ] Recursive cost rollup pattern works at any hierarchy depth
- [ ] At least 3 enforceable rules defined with implementation approach
- [ ] Standard cost output schema defined with 20+ required outputs
- [ ] Full LCOE calculation pattern documented with all components
- [ ] Minimal prototype validates patterns work with tooling

---

**Created**: 2026-01-06
**Related**: `project/research/20260106-050051_cost-modeling-lcoe-strategy.md`
