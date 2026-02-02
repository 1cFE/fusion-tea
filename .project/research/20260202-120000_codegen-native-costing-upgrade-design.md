---
date: 2026-02-02T12:00:00-06:00
researcher: Claude
topic: "sysml-codegen native costing upgrade design"
tags: [research, codegen, architecture, nested-calcusage, costing]
status: complete
last_updated: 2026-02-02
---

# Research: Upgrading sysml-codegen for Native Nested CalcUsage Costing

**Date**: 2026-02-02T12:00:00-06:00
**Researcher**: Claude
**Research Type**: Architecture / Feasibility / Design

## Research Question

How should sysml-codegen be upgraded to handle component-level costing natively — discovering CalcUsages embedded in PartDefinitions, resolving bindings through `:>>` redefinition chains, handling multiplicity, and generating correct TEAx modules — thereby eliminating the `generate_costs.py` workaround?

## Summary

- **The root limitation is NOT CalcUsage discovery** — codegen already finds all 15 CalcUsages (including 10 component-level ones). The actual gap is a cluster of 4 interrelated problems: (1) binding resolution through `:>>` redefinition chains, (2) multiplicity-aware cost computation, (3) assembly cost rollup/aggregation, and (4) part-usage-context awareness for per-instance parameter variation.
- **The hybrid pipeline worked** because `generate_costs.py` implements a full 4-phase algorithm (extract → map → resolve hierarchy → evaluate) that traverses the model at runtime using syside's reflection APIs, while codegen uses a static extraction pipeline that loses the hierarchical context.
- **sysml-codegen has a clean 7-step layered architecture** (extract → analyze → resolve → generate) with strong single-sources-of-truth at each layer. The enhancement would primarily affect Steps 3-5 (usage extraction, design attribute extraction, dependency backtracking) plus a new aggregation concept in the resolution layer.
- **Four viable approaches exist**: (A) Enhance codegen's extraction+analysis layers to understand part hierarchies natively, (B) Generate a runtime evaluator module that mirrors `generate_costs.py`'s algorithm, (C) Formalize `generate_costs.py` as a codegen plugin/extension, or (D) Expression compilation with generated tree evaluator. Each has different complexity/payoff tradeoffs.
- **UPDATE: A fifth option exists — "Approach E: Codegen-Compatible Modeling Style."** Analysis of the first CATF model at `/home/reid/fusion_modeling/models/` reveals a set of SysML modeling patterns that deliberately avoid codegen's limitations while remaining semantically correct. This is not a codegen enhancement but a modeling discipline that makes the problem disappear at the source. See Section 5 for details.
- **UPDATE: The nested CalcUsage + multiplicity + aggregation pattern is NOT costing-specific.** PyFECONS uses the same pattern for magnet physics (TF coils ×12, PF coils ×8, each with field/stress/cooling calcs, then aggregated). The fusion backlog (WI-007, WI-008, WI-009) plans this for geometry, magnetics, and thermal domains. This strengthens the case for Approaches A/D and weakens the "over-engineering" concern about Approach A.

## Detailed Findings

### 1. The Actual Root Cause (Not What the Epic Says)

The epic states: "Codegen finds top-level CalcUsages only; embedded `cost_model` in PartDefs invisible." This is **incorrect**. Evidence:

- Phase 1 of the hybrid pipeline (plan.md:396) confirms: "**15 modules generated** (not 5): Codegen discovered all CalcUsages including 10 component-level cost calcs."
- `SysideAdapter.elements_of_type(model, "CalculationUsage")` returns **all** CalculationUsage elements in the model, regardless of nesting depth (`syside_adapter.py:214`: `model.elements(type_map[type_name])`).
- Both `generate_costs.py:261` and `usage_extractor.py:155` call the same API and get the same elements.

**The real gap is a 4-part problem:**

#### Gap 1: Binding Resolution Through `:>>` Redefinition Chains

When a design file uses `:>>` to bind parameter values through a part hierarchy:

```sysml
// design.sysml
part solar_battery_plant : 'Solar Battery Plant' {
    :>> solar_array {
        :>> pv_module {
            :>> wattage = 400;  // overrides library default
        }
    }
}
```

Codegen's `DependencyBacktracker` (`dependency_backtracker.py`) resolves bindings using 5 strategies:
1. Exact match in output_catalog
2. Direct instance match (same-file)
3. Transitive design attribute resolution
4. Cross-file attribute matching
5. Bare instance name lookup

None of these handle the `:>>` redefinition chain pattern where a design-level attribute override flows through a PartUsage hierarchy to reach a CalcUsage's input. The backtracker sees the component CalcUsage's input params (e.g., `wattage`) but can't trace them back to the design-level `:>>` overrides because that chain goes: design `:>> pv_module.wattage` → PartUsage attribute → PartDef attribute → CalcUsage input binding.

**Evidence**: `library_params.json` shows codegen extracted default values from the library definitions (e.g., `cost_per_watt: 1.07`) but couldn't find the design-level overrides. These became entry points rather than resolved bindings.

#### Gap 2: Multiplicity-Unaware Cost Computation

Codegen generates one module per CalcUsage. For `PVModuleCostCalc`, it generates a module that computes cost for a single PV module. But the design specifies `pv_module[20]` — there are 20 instances. The total cost must be `single_cost * 20`.

Codegen has no concept of multiplicity in its pipeline. The `CalcUsageData` dataclass has no multiplicity field. The `PipelineModule` resolution model has no way to express "run this N times" or "multiply output by N".

`generate_costs.py` handles this at `_build_part_instance()` by extracting multiplicity from `part_usage.multiplicity.upper_bound` and storing it on each `PartInstance`, then applying it during cost aggregation.

#### Gap 3: Assembly Cost Rollup / Aggregation

The costing pattern uses a 3-level hierarchy: Plant → Assembly → Leaf. Assemblies (Solar Array, Battery System, Site Infrastructure) sum their children's `total_cost` values plus an optional allocation model. The plant sums assembly costs.

Codegen has no aggregation concept. It models a flat DAG of CalcUsages where outputs feed inputs. There's no mechanism to express "sum the total_cost outputs of all child CalcUsages."

`generate_costs.py` handles this via post-order tree traversal in `_compute_part_hierarchy_costs()`: compute leaves first, then aggregate at assembly level, then aggregate at plant level.

#### Gap 4: Part-Usage-Context for Per-Instance Variation

Each CalcUsage is defined once in a PartDefinition (e.g., `PVModuleCostCalc` in `PV_Module`), but instantiated multiple times via PartUsages in the design. Each instance could have different parameter values (e.g., different wattages for different PV modules, though in this model they're uniform).

Codegen generates one module per CalcDefinition. It would need to generate per-PartUsage instances with resolved bindings specific to each usage context.

`generate_costs.py` handles this by building a `PartInstance` tree where each node carries its own resolved `bound_params` dict.

### 2. Why the Hybrid Pipeline Worked

The hybrid pipeline split the problem along a natural boundary:

| Concern | Handled By | Why It Works |
|---------|-----------|--------------|
| Discover nested CalcUsages | `generate_costs.py` | Runtime AST traversal via syside reflection |
| Resolve `:>>` bindings | `generate_costs.py` | `_extract_design_bindings()` traces redefinition chains at runtime |
| Handle multiplicity | `generate_costs.py` | `_extract_multiplicity()` reads part usage cardinality |
| Aggregate assembly costs | `generate_costs.py` | `_compute_part_hierarchy_costs()` post-order traversal |
| Compute system-level LCOE | codegen → TEAx | Top-level CalcUsages with direct design attribute bindings |
| Wire everything together | TEAx pipeline YAML | `ComponentCostEvaluator` bridges the two worlds |

The key insight: **component costing requires hierarchical tree evaluation**, while system-level LCOE requires **flat DAG evaluation**. Codegen is built for the latter. The hybrid pipeline respects this boundary.

### 3. sysml-codegen Architecture Deep Dive

**Location**: `/home/reid/1cfe/sysml-codegen/src/sysml_codegen/`

**7-Step Pipeline** (in `generation/initialization.py: build_pipeline_context()`):

```
Step 1: Load SysML models via SysideAdapter
Step 2: extract_calculation_definitions() → list[CalculationDefinitionData]
Step 3: extract_calculation_usages() → list[CalcUsageData]
Step 4: extract_design_attributes() → dict[Path, list[DesignAttributeData]]
Step 5: ParameterGroupDeriver(design_attrs, usages, calc_defs)
Step 6: DependencyBacktracker.find_required_modules() → BacktrackingResult
Step 7: build_computation_graph() → ComputationGraph
```

**Layer Architecture**:

| Layer | Directory | Purpose | Key Data Type |
|-------|-----------|---------|---------------|
| Extraction | `extraction/` | Parse SysML → structured data | `CalculationDefinitionData`, `CalcUsageData` |
| Analysis | `analysis/` | Dependency tracing, entry point classification | `BacktrackingResult`, `BindingResolution` |
| Resolution | `resolution/` | Build pipeline graph (SSOT) | `ComputationGraph`, `PipelineModule` |
| Generation | `generation/` | Jinja2 templates → Python/YAML | Generated code files |

**Key Design Decisions**:
- `ComputationGraph` is the SSOT for all downstream generation
- Binding resolution happens once in the backtracker, stored as a dict
- Topological sort for execution ordering
- Entry points classified into parameter groups (→ JSON files)
- `__` (double underscore) separator for Python-safe qualified names

### 4. generate_costs.py Algorithm (The Reference Implementation)

**4-Phase Pipeline** (`generate_costs.py`):

```
Phase 1: extract_calc_defs()
  - adapter.elements_of_type(model, "CalculationDefinition")
  - For each: extract inputs, outputs, formulas, dependencies

Phase 2: map_part_defs_to_calcs()
  - adapter.elements_of_type(model, "CalculationUsage")
  - Filter by name == "cost_model"
  - Map: part_def_name → calc_def_name

Phase 3: extract_design_hierarchy()
  - _extract_design_bindings(root_usage) → nested dict of :>> overrides
  - _build_part_instance(part_usage, ...) → recursive tree
  - _resolve_bindings() → 3-level priority: design :>> > calc usage binding > calc def default

Phase 4: _compute_part_hierarchy_costs()
  - Post-order traversal: leaves first
  - evaluate_calc() → topological sort of outputs, recursive expression evaluation
  - Assembly: sum children + allocation
```

**Key syside APIs used**:
- `model.elements(type)` — all elements of a type
- `part_usage.part_definitions[0]` — definition for a usage
- `part_usage.multiplicity.upper_bound` — cardinality
- `elem.owned_members` — child elements
- `elem.owned_redefinitions` — `:>>` redefinition links
- `feature.chaining_features` — dot-path resolution
- `feature.feature_value_expression` — value/formula AST

## Architecture Insights

### What Makes This Hard

The fundamental tension is between **static code generation** and **runtime model evaluation**:

- **Codegen's model**: Extract everything at generation time → emit fixed Python code → run that code with parameter values from JSON. The generated code doesn't need the SysML model at runtime.
- **generate_costs.py's model**: Load the SysML model at runtime → traverse it reflectively → evaluate formulas dynamically. The algorithm IS the model traversal.

For component costing, the model structure is the computation — the hierarchy, multiplicity, and aggregation patterns are embedded in the part/usage/redefinition relationships. Flattening this into a static DAG of independent modules loses critical information.

### The Part Hierarchy Problem

The core issue is that SysML v2's part hierarchy encodes computation semantics:

```
Solar Battery Plant                    ← sum children
├── Solar Array                        ← sum children + allocation
│   ├── PV Module [20]                 ← compute × 20
│   ├── String Inverter [4]            ← compute × 4
│   └── Array BOS                      ← compute × 1
├── Battery System                     ← sum children
│   ├── Battery Pack [8]               ← compute × 8
│   ├── Hybrid Inverter                ← compute × 1
│   └── Battery BOS                    ← compute × 1
└── Site Infrastructure                ← sum children
    ├── Racking & Mounting             ← compute × 1
    ├── Electrical Panel               ← compute × 1
    └── Permitting & Interconnect      ← compute × 1
```

This is a TREE, not a DAG. Codegen's `ComputationGraph` models DAGs. Costing requires tree evaluation with:
- Leaf-first computation
- Per-node multiplicity scaling
- Bottom-up aggregation at intermediate nodes
- Context-dependent parameter binding (same CalcDef, different params per instance)

## Feasibility Assessment

### Approach A: Enhance Codegen's Core Extraction+Analysis (Full Native)

**What changes:**

1. **Step 3 Enhancement** — `extract_calculation_usages()` gains a `PartUsageContext`:
   - After finding CalcUsages, check each one's `owner`/`owning_type`
   - If owned by a PartDefinition (not a package), record the owning PartDef
   - Create `ContextualCalcUsageData` with: CalcUsageData + owning_part_def + multiplicity (from design)
   - For each PartUsage in the design that uses this PartDef, create a synthetic per-instance CalcUsage

2. **Step 4 Enhancement** — `extract_design_attributes()` understands `:>>` chains:
   - Currently extracts flat design attributes with `feature_value_expression`
   - Add: traverse `:>>` redefinitions recursively
   - Build a `RedefinitionChain` that maps `design.part.attr` → resolved value
   - Expose as part of `DesignAttributeData`

3. **Step 6 Enhancement** — `DependencyBacktracker` gains a new resolution case:
   - Case 6: Redefinition chain binding — when a CalcUsage input is bound to a PartDef attribute that's overridden via `:>>` in the design

4. **New Step: Aggregation Graph** — Add a `HierarchyAggregator` that:
   - Builds the part-usage tree from the design
   - Tags each node with: CalcUsage (if leaf), multiplicity, aggregation function (sum)
   - Generates synthetic "rollup" CalcUsages for assembly nodes
   - Flattens to additional `PipelineModule` entries in the `ComputationGraph`

5. **Step 7 Enhancement** — `ComputationGraph` gains `multiplicity_factor` on `PipelineModule`:
   - Each module carries a `multiplicity: int = 1`
   - Generated code multiplies output by this factor
   - OR: generates a `MultiplyModule` wrapper

**Complexity**: HIGH (4-6 weeks). Touches every layer. Risk of regressions in existing DAG-based pipeline generation.

**Pros:**
- Cleanest long-term solution
- All costing flows through codegen → uniform pipeline
- No runtime model dependency
- Enables codegen to handle any nested CalcUsage pattern (not just costing)

**Cons:**
- Large change surface across extraction, analysis, and resolution layers
- Tree-to-DAG flattening is conceptually tricky (synthetic rollup modules)
- `:>>` redefinition chain resolution is complex (arbitrary depth, multiple override levels)
- ~~May over-engineer codegen for a pattern that's specific to costing~~ **UPDATE: RETRACTED** — see Section 5. The pattern is pervasive across physics domains (magnets, blankets, thermal), not costing-specific.

### Approach B: Generate a Runtime Evaluator Module

**What changes:**

Instead of making codegen understand the full hierarchy, generate a single TEAx module that evaluates component costs at runtime by traversing the SysML model — essentially a generated version of `generate_costs.py`.

1. **New Generator** — `generate_cost_evaluator()`:
   - At codegen time: analyze the model to identify the part hierarchy and costing pattern
   - Generate a Python module that hardcodes the hierarchy structure but evaluates formulas dynamically
   - The generated code embeds: part tree structure, multiplicity values, calc-def-to-part-def mappings
   - At runtime: reads parameter values from JSON entry points, evaluates formulas, aggregates

2. **codegen Enhancement (minimal)** — Just detect the pattern:
   - In Step 3: identify CalcUsages whose `owner` is a PartDefinition (not package-level)
   - Tag these as "embedded" vs "top-level"
   - For embedded CalcUsages: don't generate individual modules; instead delegate to the cost evaluator

3. **Pipeline YAML** — Cost evaluator replaces all component-cost modules:
   - `CostEvaluator` module: inputs = param JSONs → outputs = total_capex + breakdown
   - System-level modules stay as-is (codegen-generated)

**Complexity**: MEDIUM (2-3 weeks). Mostly new code, minimal changes to existing layers.

**Pros:**
- Low risk to existing codegen behavior
- The generated evaluator is self-contained — no runtime syside dependency
- Can be incrementally developed and tested against `generate_costs.py` output
- Handles the tree evaluation naturally (generated code IS tree evaluation code)

**Cons:**
- Generated code is complex (expression evaluator, tree traversal)
- Doesn't generalize to non-costing nested CalcUsage patterns
- Conceptual duplication: codegen generates an evaluator that does what `generate_costs.py` does
- Testing the generator requires testing generated code (meta-testing)

### Approach C: Formalize generate_costs.py as a Codegen Plugin

**What changes:**

Rather than enhancing codegen, formalize the pattern where codegen generates the system-level pipeline and a plugin/extension generates the component-cost evaluator module.

1. **Plugin API for codegen** — Allow registration of external module generators:
   - Codegen emits a manifest of discovered CalcUsages (including embedded ones)
   - A plugin reads the manifest and generates its own TEAx modules
   - Codegen's pipeline YAML generator accepts "external modules" from plugins

2. **Cost Evaluator Plugin** — Wraps `generate_costs.py` logic:
   - Takes the CalcUsage manifest + SysML model paths as input
   - Generates `ComponentCostEvaluator` module (like the current hand-written one)
   - Generates entry point JSON with component cost parameters
   - Outputs module registration info for codegen's pipeline YAML

3. **Codegen Enhancement (minimal)** — Plugin interface:
   - In `build_pipeline_context()`: emit CalcUsage manifest
   - In pipeline YAML generation: accept `external_modules` list
   - In registry generation: accept `external_registrations` list

**Complexity**: LOW-MEDIUM (1-2 weeks). Mostly interface work + formalization of existing pattern.

**Pros:**
- Least disruption to codegen core
- Validates plugin architecture that could serve other extension points
- `generate_costs.py` already works — just needs a thin adapter
- Clean separation of concerns: codegen handles DAG patterns, plugins handle tree patterns

**Cons:**
- Still requires `generate_costs.py` (or equivalent) at generation time
- Runtime model dependency remains (the evaluator still loads syside)
- Doesn't advance codegen's own capabilities
- "Plugin" framing may be over-engineering for one use case

### Approach D: Expression Compilation (Hybrid Static+Runtime)

**What changes:**

Compile the SysML calc expressions into standalone Python functions at codegen time, but handle the hierarchy/multiplicity/aggregation as a generated tree evaluator.

1. **Expression Compiler** — New codegen component:
   - Parse each CalcDef's expression AST (already extracted in Step 2)
   - Generate Python function: `def pv_module_cost(wattage, cost_per_watt, ...): return wattage * cost_per_watt`
   - These are type-safe, testable, no runtime AST evaluation needed

2. **Tree Evaluator Generator** — Separate from expression compiler:
   - At codegen time: extract part hierarchy, multiplicity, aggregation patterns
   - Generate a `CostTreeEvaluator` class that hardcodes the tree structure
   - The evaluator calls the compiled expression functions for leaf nodes
   - Aggregation logic is generated as simple sum-of-children patterns

3. **Parameter Resolution** — At codegen time:
   - Extract `:>>` redefinition chains and resolve to parameter sources
   - Generate parameter mapping: `{(part_usage, param_name): source}` where source is either a literal value or a JSON entry point field

**Complexity**: MEDIUM-HIGH (3-4 weeks). New expression compiler + tree evaluator generator.

**Pros:**
- No runtime syside dependency (all compiled to Python)
- Expression functions are individually testable
- Clean separation: expressions are compiled, hierarchy is generated
- Generalizable: expression compiler useful for ANY calc pattern

**Cons:**
- Expression compilation is non-trivial (handle all AST node types)
- Must handle formula dependencies (topological sort within a CalcDef)
- Two new components to build and maintain

### Approach E: Codegen-Compatible Modeling Style (Workaround)

**UPDATE**: Added after analysis of the CATF model at `/home/reid/fusion_modeling/models/`.

**What changes:**

No codegen changes. Instead, adopt a modeling discipline that keeps all calculations within codegen's existing capabilities. The first CATF model already demonstrates this approach across physics, geometry, and thermal domains.

**The five rules:**

1. **Multiplicity is a parameter, not a SysML array.**
   ```sysml
   // DO:
   part catf_tf_system {
       attribute n_coils : Real = 12;
   }
   // DON'T:
   part tf_coil[12] : 'TF Coil' { ... }
   ```
   CalcDefs accept `n_coils` as an input and multiply internally. No per-element iteration.

2. **Nested CalcUsages EXPOSE all outputs as sibling attributes.**
   ```sysml
   part blanket {
       calc volume_calc : TorusVolume { ... }
       attribute volume : Real = volume_calc.volume;  // EXPOSE
   }
   ```
   External code references `blanket.volume` (attribute path), never `blanket.volume_calc.volume` (calc output path). Codegen resolves attribute references without needing to trace into nested calc structures.

3. **Aggregation is an explicit CalcDef, not automatic tree traversal.**
   ```sysml
   calc def NetElectricPower {
       in p_coils; in p_heating; in p_pumps; ...
       out p_parasitic_total = p_coils + p_heating + p_pumps + ...;
   }
   ```
   Every aggregation point is a CalcDef with all inputs listed explicitly. Codegen sees this as a normal flat DAG node.

4. **Non-uniform arrays become separate named instances.**
   ```sysml
   part catf_pf1 { attribute coil_count = 2; attribute r_centre = 0.67; ... }
   part catf_pf2 { attribute coil_count = 2; attribute r_centre = 0.67; ... }
   // ... 8 separate PF coils with per-instance parameters
   ```

5. **Cross-file references use EXPOSE'd attributes, never calc output paths.**
   ```sysml
   // physics.sysml
   in p_coils = catf_tf_system.cooling_power;  // attribute, not calc path
   ```

**Evidence from CATF model:**

The CATF model at `/home/reid/fusion_modeling/models/` uses all five patterns successfully:

| File | Pattern Used | What It Avoids |
|------|-------------|----------------|
| `magnets.sysml:48` | `n_coils : Real = 12` (Rule 1) | SysML array multiplicity |
| `magnets.sysml:96` | `cooling_power : Real = cryo_load.cooling_power` (Rule 2) | Nested calc path traversal |
| `physics.sysml:84-96` | `NetElectricPower` takes 7 explicit parasitic inputs (Rule 3) | Automatic tree aggregation |
| `magnets.sysml:103-329` | 8 separate `catf_pf1`..`catf_pf8` parts (Rule 4) | Array with per-element variation |
| `physics.sysml:89` | `catf_tf_system.cooling_power` (Rule 5) | Calc output path reference |
| `radial_build.sysml:96-110` | Nested `minor_calc` + `volume_calc` with EXPOSE (Rule 2) | Hidden nested outputs |

**Complexity**: ZERO (codegen changes). MEDIUM (modeling discipline + documentation).

**Pros:**
- No codegen changes needed — works today
- The CATF model proves it's viable for real fusion modeling (physics + geometry + thermal)
- Produces correct results — the pattern is semantically equivalent
- Immediate: no development delay before fusion modeling can proceed
- Forces explicit data flow documentation (every aggregation is visible in the CalcDef)

**Cons:**
- **Verbosity**: 14 repeated `minor_calc` + `volume_calc` blocks in `radial_build.sysml` (vs 1 CalcDef-in-PartDef with the nested pattern). Each radial build layer duplicates ~10 lines of calc usage boilerplate.
- **Fragile aggregation**: Adding a new subsystem (e.g., a 9th PF coil) requires updating every aggregation CalcDef that sums over PF coils. With tree aggregation, you'd just add the child and `sum()` picks it up automatically.
- **No structural enforcement**: Nothing prevents a modeler from forgetting to add a new subsystem to an aggregation CalcDef. The model will silently produce wrong results.
- **Duplicated instances for non-uniform arrays**: 8 PF coil parts with largely duplicated structure. For fusion's ~30 subsystems, this could mean 100+ named parts.
- **Loses SysML's compositional semantics**: The "part has its own cost model" pattern (CalcUsage-in-PartDef) is idiomatic SysML v2. Flattening everything to top-level calcs works but doesn't leverage the language's design intent for hierarchical modeling.

**Scalability assessment:**

| Metric | Solar+Battery (current) | CATF Fusion (planned) | Concern Level |
|--------|------------------------|----------------------|---------------|
| Leaf parts | 9 | ~30-50 | Manageable |
| Hierarchy levels | 3 | 4-6 | Aggregation CalcDefs get large |
| Aggregation CalcDefs | ~3 | ~10-15 | Each with 5-15 explicit inputs |
| Repeated calc blocks | ~0 | ~14 (radial build) | Annoyance, not blocker |
| Non-uniform array instances | 0 | 8 (PF coils) + more | Gets verbose but works |

For fusion at the CATF scale (~50 CalcDefs, ~30 subsystems), the workaround is **viable but increasingly awkward**. The aggregation CalcDefs would have 50+ explicit inputs for the full CAS hierarchy. Maintainability becomes the main concern.

---

## Recommendations

**UPDATE: Revised after CATF model analysis and domain pattern evaluation.**

### Decision Matrix

| Approach | Codegen Changes | Modeling Effort | Scalability | Runtime syside? | Closes "GAP" | Domain Generality |
|----------|----------------|-----------------|-------------|-----------------|--------------|-------------------|
| **A: Full Native** | HIGH | None | Excellent | No | Yes | All domains |
| **B: Runtime Evaluator** | MEDIUM | None | Good | No | Partial | Costing only |
| **C: Plugin** | LOW | None | Good | Yes | No | Costing only |
| **D: Expression Compiler** | MEDIUM-HIGH | None | Excellent | No | Yes | All domains |
| **E: Modeling Workaround** | None | MEDIUM | Adequate | No | No | All domains (via discipline) |

### Recommended: Approach E (Modeling Workaround) for Immediate Term

Use the codegen-compatible modeling style to unblock fusion modeling now:

1. Document the 5 rules as a formal ADR in `modeling_project/ARCHITECTURE.md`
2. Use the CATF model's proven patterns as the reference
3. Fusion modeling can proceed immediately with no tooling delays
4. Accept the verbosity tradeoff at current scale (~30-50 subsystems)

### Recommended: Approach D (Expression Compilation) for Long-Term

This remains the architecturally cleanest solution and advances codegen's capabilities most broadly:

1. **Expression compiler** is independently useful — enables codegen to generate actual computation logic (currently marked as "GAP: Code generator does NOT implement calc logic")
2. **Tree evaluator** cleanly separates hierarchy concerns from computation concerns
3. **No runtime model dependency** — all compilation happens at codegen time
4. Positions codegen for fusion LCOE where the same pattern (nested costs + system-level calcs) will be more complex

**UPDATE**: The case for Approach D is stronger than originally stated. The nested CalcUsage + multiplicity + aggregation pattern is NOT costing-specific — PyFECONS uses it for magnet physics (`cas220103_coils.py:42-66`: per-magnet property computation → `sum()` aggregation), and the fusion backlog plans it for geometry (WI-008), magnetics (WI-009), and thermal (WI-013). The expression compiler + tree evaluator would serve all these domains.

### Revised Assessment: Approach A (Full Native Enhancement)

**UPDATE**: Originally "Not Recommended." Now **worth considering** given the domain evidence:

- The "over-engineering for costing" concern is retracted — the pattern is pervasive across physics domains
- The complexity is still HIGH, but the payoff is also higher than originally assessed
- The DAG-vs-tree concern remains valid, but could be addressed by generating synthetic "flattened" modules from the tree rather than changing the ComputationGraph structure
- If Approach E's verbosity becomes a bottleneck at scale, Approach A becomes the right long-term investment

### Recommended: Approach C (Plugin) for Short-Term (if E is insufficient)

If the goal is to eliminate the hand-written `ComponentCostEvaluator` module quickly:

1. Formalize the existing `generate_costs.py` as a codegen extension
2. Add minimal plugin interface to codegen (manifest + external module registration)
3. This can be done in 1-2 weeks and validates the architecture before investing in Approach D

### Revised Phased Roadmap

```
Phase 0 (Immediate): Approach E — Codegen-Compatible Modeling Style
  - Document 5 modeling rules as ADR
  - Apply to fusion-tea models (costing + physics + geometry)
  - Unblocks all current backlog items (WI-007 through WI-013)
  - No tooling changes required

Phase 1 (Short-term, if needed): Approach C — Plugin Interface
  - Formalize generate_costs.py as codegen extension
  - Only needed if solar_battery-style models (with :>> and array multiplicity)
    must coexist alongside CATF-style flat models
  - Validates plugin architecture

Phase 2 (Medium-term): Expression Compiler (Approach D, Phase 1)
  - Compile CalcDef expressions → Python functions
  - Close the "GAP: does NOT implement calc logic" across ALL generated modules
  - Independently testable and useful
  - Benefits ALL domains, not just costing

Phase 3 (Long-term): Tree Evaluator Generator (Approach D, Phase 2)
  - Generate hierarchy-aware evaluators from part structure
  - Uses expression compiler outputs for leaf computation
  - Full native costing with no runtime model dependency
  - Enables transition from Approach E (flat) back to idiomatic SysML (nested)
  - Trigger: when Approach E's verbosity measurably impedes productivity
```

### When to Escalate from Phase 0

Approach E (modeling workaround) should be revisited when any of these become true:

1. **Aggregation CalcDefs exceed ~15 explicit inputs** — signals that manual wiring is fragile
2. **A modeler forgets to add a subsystem to an aggregation CalcDef** — the silent-failure risk materializes
3. **Non-uniform array instances exceed ~15** — verbosity becomes a maintenance burden
4. **Multiple modelers are working simultaneously** — the implicit "you must update aggregation calcs" convention doesn't scale across a team
5. **Model reuse across fusion concepts** — the flat pattern is specific to one design; nested CalcUsages in PartDefs are reusable across CATF/stellarator/mirror

### 5. Domain Generality: The Pattern Is NOT Costing-Specific

**UPDATE**: Added after analysis of PyFECONS calculation patterns and the fusion-tea backlog.

#### PyFECONS Evidence

The strongest evidence comes from `PyFECONS/pyfecons/costing/mfe/cas22/cas220103_coils.py`. The magnet costing module uses exactly the nested-calc + multiplicity + aggregation pattern — but the nested calculations are **physics**, not costing:

```python
# Per-magnet PHYSICS computation (field, stress, cooling) — lines 42-45
magnet_properties = [
    compute_magnet_properties(coils, magnet, radial_build, power_table)
    for magnet in coils.magnets   # TF(×12), CS(×1), PF(×4+)
]

# Per-type AGGREGATION — lines 48-66
C22010301 = sum([mag.magnet_total_cost for mag in cas220103.tf_coils])
C22010305 = sum([mag.magnet_struct_cost for mag in cas220103.magnet_properties])
C22010306 = sum([mag.cooling_cost for mag in cas220103.magnet_properties])
```

Inside `compute_magnet_properties()`, the per-coil calculations include:
- Cross-sectional area and turn count geometry
- Tape length and current density (electromagnetic physics)
- Material volumes and masses (structural analysis)
- Hoop stress (mechanical analysis)
- Nuclear heating and cooling load (thermal analysis)
- Cost is derived FROM these physics results, not independent of them

#### Fusion Domain Examples

| System | Multiplicity | Per-Unit Physics Calc | Aggregation | PyFECONS Source |
|--------|-------------|----------------------|-------------|-----------------|
| **TF Coils** | ×12 | Field strength, hoop stress, stored energy, cooling load | `sum(stored_energy)`, `max(stress)`, `sum(cooling)` | `cas220103_coils.py` |
| **PF Coils** | ×6-8 (non-uniform) | Per-coil current, field contribution | `sum(cooling)`, field control authority | `cas220103_coils.py` |
| **Blanket Modules** | ×20-40 zones | Neutron multiplication, TBR per module, thermal power | `sum(tbr)` → tritium self-sufficiency, `sum(thermal_power)` → p_th | `blanket.py` inputs |
| **Heat Exchangers** | ×2-4 loops | Q = ṁ·Cp·ΔT per loop, pressure drop | `sum(duty)` → total thermal rejection | `thermal.py` |
| **Radial Build Layers** | ×12-14 concentric | Volume, mass, neutron attenuation per layer | Cumulative shielding → dose rate at magnets | `volume.py` |

#### Planned Backlog Items Using This Pattern

- **WI-007 (Power Core)**: Blanket modules with per-module TBR and thermal calcs
- **WI-008 (Geometry)**: Radial build layers with per-layer volume/area calcs (already demonstrated in CATF model)
- **WI-009 (Magnets)**: TF/PF/CS coils with per-coil field/stress/cooling calcs
- **WI-012 (Heating)**: Multiple beamlines with per-line power deposition calcs
- **WI-013 (Balance of Plant)**: Multiple heat exchangers with per-loop thermal duty calcs

#### Implication for Approach Selection

This finding changes the calculus significantly:

- **Approach A**: No longer "over-engineering" — it's building infrastructure that physics, thermal, structural, and costing domains all need
- **Approach D**: The expression compiler serves all domains; the tree evaluator is needed for any domain with hierarchical aggregation
- **Approach C**: Would need to be duplicated per domain (costing plugin, magnetics plugin, thermal plugin...) — doesn't scale
- **Approach E**: Works for all domains via modeling discipline, but the verbosity compounds across 5+ physics domains

---

## Code References

### sysml-codegen
- `src/sysml_codegen/extraction/usage_extractor.py:155` — `elements_of_type(model, "CalculationUsage")` finds ALL usages (not just top-level)
- `src/sysml_codegen/extraction/usage_extractor.py:171` — `_extract_single_usage()` processes each usage
- `src/sysml_codegen/analysis/dependency_backtracker.py` — 5 binding resolution strategies (none handle `:>>` chains)
- `src/sysml_codegen/resolution/graph_builder.py` — `build_computation_graph()` builds flat DAG
- `src/sysml_codegen/resolution/models.py` — `ComputationGraph`, `PipelineModule` (no multiplicity, no tree)
- `src/sysml_codegen/generation/initialization.py` — 7-step `build_pipeline_context()`

### generate_costs.py (reference algorithm)
- `models/tests/solar_battery/generate_costs.py:253` — `map_part_defs_to_calcs()` maps PartDefs to CalcDefs
- `models/tests/solar_battery/generate_costs.py:261` — Same `elements_of_type` call as codegen
- Phase 3 hierarchy extraction: `_extract_design_bindings()`, `_build_part_instance()`, `_resolve_bindings()`
- Phase 4 evaluation: `_compute_part_hierarchy_costs()`, `evaluate_calc()`

### agentic-mbse
- `src/agentic_mbse/sysml/syside_adapter.py:214` — `model.elements(type)` returns ALL elements

### Hybrid pipeline artifacts
- `.project/active/hybrid-pipeline-e2e/plan.md:396` — Confirms 15 modules generated (not 5)
- `generated/solar_battery/inputs/library_params.json` — Codegen's extracted component params (as entry points)
- `generated/solar_battery/inputs/design_params.json` — Codegen's extracted system-level params
- `generated/solar_battery/modules/solarbatterylibrary/pvmodulecostcalc.py` — Generated component module (structurally correct, missing context)

### CATF model (Approach E reference patterns)
- `/home/reid/fusion_modeling/models/designs/catf_mfe/magnets.sysml:48` — `n_coils : Real = 12` (multiplicity as parameter)
- `/home/reid/fusion_modeling/models/designs/catf_mfe/magnets.sysml:86-96` — Nested `cryo_load` CalcUsage + EXPOSE as `cooling_power` attribute
- `/home/reid/fusion_modeling/models/designs/catf_mfe/magnets.sysml:103-329` — 8 separate PF coil instances (non-uniform array as named parts)
- `/home/reid/fusion_modeling/models/designs/catf_mfe/physics.sysml:63-96` — Flat CalcUsage chain with explicit cross-file aggregation inputs
- `/home/reid/fusion_modeling/models/designs/catf_mfe/radial_build.sysml:96-110` — Nested calc + EXPOSE pattern (14 layers, each with geometry calcs)

### PyFECONS (domain pattern evidence)
- `/home/reid/PyFECONS/pyfecons/costing/mfe/cas22/cas220103_coils.py:42-66` — Per-magnet physics computation + aggregation
- `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py` — Power balance chain (sequential flat pattern)
- `/home/reid/PyFECONS/pyfecons/data.py:56-195` — CAS hierarchy (11-level cost structure)

## Open Questions

1. **Should codegen generate expression implementations at all?** Currently all calc logic is marked as "GAP" and deferred to handwritten implementations. The expression compiler (Approach D Phase 2) would close this gap globally but is a significant feature.

2. ~~**How generalizable is the part hierarchy pattern?** Is costing the only use case for nested CalcUsages + aggregation, or will fusion models have other tree-evaluation patterns (e.g., neutronics, thermal analysis)?~~ **UPDATE: ANSWERED — YES, the pattern is pervasive.** See Section 5. PyFECONS uses it for magnet physics (field, stress, cooling per coil → aggregated totals). The fusion backlog plans it for geometry (WI-008), magnetics (WI-009), thermal (WI-012, WI-013). This is not costing-specific.

3. **Runtime model dependency tradeoff**: Approaches C and the current hybrid both require syside at runtime. Is eliminating this dependency a hard requirement (favoring D) or a nice-to-have?

4. ~~**What's the fusion model scale?**~~ **UPDATE: PARTIALLY ANSWERED.** The CATF model has ~30-50 subsystems, 4-6 hierarchy levels, ~50 CalcDefs planned. The full CAS hierarchy has ~25 leaf cost accounts. Approach E (modeling workaround) is viable at this scale but aggregation CalcDefs would have 50+ explicit inputs for the full CAS hierarchy. The "when to escalate" triggers in the Recommendations section provide concrete thresholds.

5. **Should codegen's plugin API be general-purpose?** Or should it be specific to the costing pattern? A general plugin API has more design overhead but enables other extensions. **UPDATE**: Less relevant if Approach E (modeling workaround) is adopted as the immediate path — no plugin needed.

6. **NEW: Is the Approach E verbosity acceptable for team modeling?** The CATF model was built by a single modeler. If multiple modelers work on the fusion model simultaneously, the implicit convention "you must update aggregation CalcDefs when adding subsystems" becomes a coordination problem. This is the strongest argument for eventually investing in Approach A or D.

7. **NEW: Can Approach E and nested CalcUsages coexist?** The solar_battery model uses nested CalcUsages (idiomatic SysML), while the CATF model uses the flat workaround. If both styles are present in a project, codegen handles the flat ones natively and needs `generate_costs.py` for the nested ones. Is a mixed-style codebase acceptable, or must one pattern win?

8. **NEW: What's the modeling reuse story?** Approach E's flat style is design-specific — the aggregation CalcDefs for CATF list CATF's specific subsystems. A stellarator with different subsystems needs different aggregation CalcDefs. Nested CalcUsages in PartDefs (idiomatic SysML) are reusable across designs: the same `'TF Coil'` PartDef with its embedded physics calcs works in any tokamak variant. If cross-concept comparison is a project goal, this favors eventually moving to Approaches A/D.
