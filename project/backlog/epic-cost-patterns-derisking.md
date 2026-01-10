# Epic: Cost Modeling Patterns De-Risking

**Status**: READY
**Priority**: P0 (blocking Phase 4 - Cost Calculations)
**Created**: 2026-01-10
**Owner**: Reid

---

## Context

### Problem Statement

Our current modeling pipeline (SysML → sysml-codegen → teax-simkit) produces outputs that are not useful for humans. The results are just energy balance values and final LCOE numbers — no visibility into cost drivers, no hierarchical breakdown, no efficiency metrics.

Before implementing full cost calculations (Phase 4), we need to:
1. Define and validate the **modeling patterns** for cost rollup
2. Define and validate the **output format** that meets user needs
3. Prove the approach works before investing in tooling upgrades

### Background Research

This epic synthesizes findings from several research efforts:

| Document | Key Findings |
|----------|--------------|
| [20260107-final-cost-architecture.md](../research/20260107-final-cost-architecture.md) | **Nested cost models are the correct pattern**: Parts contain their own cost calc usages, co-locating structure with analysis. SysMLv2 fully supports this via redefinition semantics. |
| [20260110-strategic-cost-patterns.md](../research/20260110-strategic-cost-patterns.md) | **Standardization decisions**: `cost_model` naming convention, leaf vs assembly recursion rules, idiot index tracking, AACE estimation metadata, multi-category outputs (material/fab/install). |
| sysml-codegen exploration | **Tooling gap identified**: sysml-codegen extracts calc usages from PartDefinitions but does NOT instantiate them per PartUsage. This is the specific gap blocking Pattern A. |

### The Pattern We're Validating

**Pattern A: Nested Cost Models**

```sysml
// Library: Part definition with embedded cost model
part def 'Heating Element' :> 'Costed Component' {
    attribute power_rating : Real;
    attribute material_mass : Real;

    calc cost_model : HeatingElementCostCalc {
        in power = power_rating;
        in mass = material_mass;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
}

// Design: Clean instantiation (cost computed automatically)
part coffee_maker {
    part heater : 'Heating Element' {
        :>> power_rating = 1000.0;  // Watts
        :>> material_mass = 0.15;   // kg
    }

    // Cost "just works" via redefinition propagation
    attribute heater_cost : Real = heater.capital_cost;
}
```

**Why This Pattern**:
- Co-locates structure with cost analysis
- Design files are clean (just set parameters)
- Recursive rollup via `capital_cost` aggregation
- Multi-output visibility (material, fab, install, idiot index)

### Tooling Gap

**sysml-codegen current behavior**:
- Finds `cost_model` calc usage in `'Heating Element'` PartDefinition
- Treats it as a template owned by the definition
- Does NOT create `heater.cost_model` module instance

**Required behavior**:
- Detect calc usages owned by PartDefinitions (templates)
- Find all PartUsages that instantiate those definitions
- Create virtual calc usage per instantiation with resolved bindings
- Handle redefinition chain (`:>> power_rating = 1000.0` → literal binding)

---

## Goals

### Primary Goal

**De-risk the cost modeling pattern before building tooling.**

Validate that:
1. The SysML pattern is syntactically valid and parseable
2. The pattern is traversable (we can find calcs, bindings, hierarchy via AST walking)
3. The output format meets user needs for cost analysis

### Success Criteria

| Criterion | Validation Method |
|-----------|-------------------|
| Model compiles | `syside check` passes |
| Pattern is traversable | Custom AST script finds all calcs, traces bindings through redefinitions, builds hierarchy |
| Output format is useful | Hand-written CSV reviewed and approved by stakeholder |
| Rollup math is correct | Manual calculation matches expected totals |

---

## Scope

### In Scope

- **Demo model**: Coffee maker with 3-4 hierarchy levels
- **AST validation script**: Prove the pattern is traversable
- **Expected output format**: Hand-written CSV showing ideal cost breakdown
- **Iteration**: Refine model and output until both are right

### Out of Scope (Deferred to Implementation)

- sysml-codegen feature implementation
- agentic-mbse enforcement rules
- teax-simkit execution
- Full fusion plant model

---

## Plan

### Stage 1: Demo Model

**Goal**: Create a coffee maker model using Pattern A that compiles and is traversable.

**Deliverables**:
1. `models/tests/coffee_maker/` directory with:
   - `library.sysml` — Costed Component interface, calc defs
   - `design.sysml` — Coffee maker instantiation with nested parts
2. `syside check` passes
3. Custom AST script that outputs:
   - All calc usages found (with owning part path)
   - Bindings traced through redefinitions
   - Hierarchy structure (parent → children)

**Hierarchy target** (3-4 levels):
```
CoffeeMaker (assembly)
├── BrewingSystem (assembly + allocation costs)
│   ├── HeatingElement [2] (leaf, arrayed)  ← tests multiplicity
│   ├── WaterPump (leaf)
│   └── BrewChamber (leaf)
│   └── [allocation: fasteners, seals, wiring harness]
├── WaterReservoir (leaf)
├── Carafe (leaf)
└── Housing (assembly)
    ├── OuterShell (leaf)
    └── ControlPanel (leaf)
```

**Key patterns validated**:
| Pattern | Example | What It Tests |
|---------|---------|---------------|
| Leaf cost calc | `HeatingElement.cost_model` | Direct calculation |
| Assembly rollup | `BrewingSystem.capital_cost = Σ children` | Aggregation |
| **Part multiplicity** | `HeatingElement [2]` | Per-unit vs total cost, rollup math |
| **Allocation costs** | `BrewingSystem.misc_hardware_cost` | Assembly-level minor items (Rule R3) |

**Exit criteria**: AST script can find all 7 leaf cost_models, trace bindings (including through multiplicity), and identify allocation costs at assembly level.

### Stage 2: Expected Output Format

**Goal**: Define the ideal CSV output by hand.

**Deliverables**:
1. `models/tests/coffee_maker/expected_output.csv` with columns:
   - `path` — Qualified path (e.g., `coffee_maker.brewing_system.heater`)
   - `quantity` — Part count (e.g., 2 for `HeatingElement [2]`)
   - `unit_cost` — Cost per unit (for arrayed parts)
   - `raw_material_cost` — Material cost (total for all units)
   - `fabrication_cost` — Manufacturing cost
   - `installation_cost` — Assembly cost
   - `total_cost` — Sum
   - `idiot_index` — total / material ratio
   - `cost_type` — "direct" (leaf calc), "rollup" (assembly sum), or "allocation" (minor items)
2. Rollup rows for assemblies showing aggregated child costs + allocation
3. Summary row with totals

**Deferred to v2**: AACE class, estimation method, confidence bands, data source references.

**Exit criteria**: Stakeholder approves output format as "useful for cost analysis."

### Stage 3: Iteration

**Goal**: Iterate on model and output until aligned.

**Activities**:
- Adjust model structure if hierarchy doesn't support needed outputs
- Adjust output columns if missing key information
- Validate rollup math manually (especially multiplicity: 2 * unit_cost)
- Validate allocation costs appear correctly in rollup

**Exit criteria**: Model and expected output are stable; ready for implementation.

### Stage 4: Implementation Specification

**Goal**: Document what sysml-codegen needs to produce the expected output.

**Deliverables**:
1. Detailed spec for sysml-codegen changes (reference [20260107-final-cost-architecture.md](../research/20260107-final-cost-architecture.md) Section: "Tooling Upgrade Specification")
2. Test cases: Given demo model, expected extraction results
3. Handoff to sysml-codegen implementation

**Exit criteria**: Spec is clear enough to implement without ambiguity.

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| SysIDE available | Ready | Used for `syside check` |
| Pattern A research complete | Ready | [20260107-final-cost-architecture.md](../research/20260107-final-cost-architecture.md) |
| Output schema research complete | Ready | [20260110-strategic-cost-patterns.md](../research/20260110-strategic-cost-patterns.md) |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Pattern doesn't compile | Low | High | SysIDE tests already pass for similar patterns |
| AST traversal more complex than expected | Medium | Medium | Start simple, iterate; we have working extraction code to reference |
| Output format needs significant revision | Medium | Low | Cheap to iterate on CSV before building tooling |
| Scope creep into tooling | Medium | Medium | Strict Stage gates; don't start Stage 4 until Stage 3 exit criteria met |

---

## References

### Research Documents
- [20260107-final-cost-architecture.md](../research/20260107-final-cost-architecture.md) — Nested cost model architecture, tooling spec
- [20260110-strategic-cost-patterns.md](../research/20260110-strategic-cost-patterns.md) — Standardization decisions, output schema, enforcement rules

### External Codebases
- `sysml-codegen` at `/home/reid/1cfe/sysml-codegen` — Extraction logic to be enhanced
- `teax-simkit` at `/home/reid/1cfe/teax-simkit` — Execution pipeline (not in scope for this epic)
- `agentic-mbse` at `/home/reid/1cfe/agentic-mbse` — Enforcement rules (deferred)

### Test Models
- `models/tests/case1_calc_def_in_partdef.sysml` — Existing pattern test
- `models/tests/case2_calc_usage_in_partdef.sysml` — Inline calc usage test

---

**Last Updated**: 2026-01-10
