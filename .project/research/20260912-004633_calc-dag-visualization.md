---
date: 2026-09-11T17:46:00-07:00
researcher: Claude
topic: "Calc dependency graph visualization — data sources, integration path, UX"
tags: [research, visualization, sysml-codegen, instance-graph, calc-dag, ux]
status: complete
last_updated: 2026-09-11
---

# Research: Calc DAG Visualization

**Date**: 2026-09-11
**Researcher**: Claude
**Research Type**: Architecture / Integration / Feasibility

## Research Question

How to visualize the SysML v2 model's calc dependency graph, leveraging existing parsing in agentic-mbse and sysml-codegen. Clean integration path. Overlay with structural containment. UX for inspecting calc implementation (SysML source and/or generated Python).

## Summary

- **The calc DAG already exists as serialized JSON** in the codegen snapshot (`stellarator.snapshot.json`): 76 calcs, 292 attrs, 14 constraints, with full I/O edge structure. Every calc-to-calc dependency is a `"kind": "producer"` edge. No new parsing needed.
- **All 76 calcs are scoped to the plant root, not to individual subsystems.** The occurrence tree carries subsystem parts (magnet, blanket, etc.) but every calc's `scope` points to `stellaris` itself. This is a modeling decision, not a tooling limitation — the calcs live in `'MFE Power Plant'` directly. An overlay with structural containment needs either a heuristic mapping or a model reorganization.
- **The snapshot carries everything needed for a detail panel:** `calc_expressions` (the human-readable formula steps), `doc_comment` (the docstring with source citations), `source_file` and `source_line` (pointer into the SysML source), and `inputs`/`outputs` with resolved edge targets.
- **The generated Python modules** exist in `generated/modules/{analysis_name}/{calc_name}.py` with full docstrings including the "Calculation Specification" (the formula steps) and the handwritten implementation path.
- **Recommended path:** read the snapshot JSON directly (~100 lines). Don't re-extract from syside (duplicates binding resolution, the highest-risk piece per Jan 2026 research). Don't parse pipeline YAML (loses containment context and metadata).

## Data Sources

### Source 1: Instance Graph Snapshot (recommended)

**Location**: `exploration/stellarator_e2e/stellarator.snapshot.json` (~1 MB)

The `InstanceGraph` (`sysml_codegen/elaboration/graph.py:364-371`) contains four populations:

| Population | Count | What it holds |
|---|---|---|
| `calcs` | 76 | display name, calc def, typed inputs/outputs, expression IR, source file:line, doc comment |
| `attrs` | 292 | display path, value, value site (definition default / occurrence override) |
| `constraints` | 14 | predicate IR, eligibility, input edges |
| `occurrences` | 14 | subsystem instances with containment slots and display segments |

**Edge structure.** Each calc input is a `{port, edge, name}` triple. The edge discriminates three kinds:
- `"kind": "producer"` — points at another calc's output port. This is the DAG edge.
- `"kind": "node"` — points at an `AttrNode` (a parameter value from the model).
- `"kind": "literal"` — an inline constant.

Resolving edges: `edge.target.calculation` is a `NodeId` (JSON-serialized UUID wire). Build a `calc_by_id` lookup from `json.dumps(c['node_id'])` to recover upstream calc names. Verified working:

```
fusion.n_T0_in  <- sustain
fusion.V        <- geom
fusion.n_D0_in  <- sustain
```

**Calc metadata available for detail panel:**
- `calc_expressions`: list of human-readable formula steps, e.g. `["discount_pow_n = (1.0 + discount_rate_in) ** operational_years_in", "crf = discount_rate_in * discount_pow_n / (discount_pow_n - 1.0)", ...]`
- `doc_comment`: full docstring with source citations (Source/Ref/Basis)
- `source_file` + `source_line`: e.g. `root-0/analyses/mfe_lcoe_dcf.sysml:4`
- `inputs[].name`, `outputs[].name`: port names

**Scope issue.** Every calc's `scope.wire` resolves to the root stellaris occurrence (`c1525587-...`). The 14 subsystem occurrences (magnet, blanket, etc.) are children of the root but own zero calcs. This means a naive overlay (calc inside its owning part container) puts all 76 calcs in one giant stellaris box.

### Source 2: Pipeline YAML (simpler but less rich)

**Location**: `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml`

93 modules in topological order. Each module lists inputs with `source_type: "module_output"` and `producer_channel` naming the upstream output. Parseable in ~50 lines.

**Disadvantages:** No occurrence tree (can't overlay). No metadata (expressions, doc comments, source locations). Module names are codegen-qualified (`stellarator_09__stellaris__geom`), not the modeler's SysML names.

### Source 3: syside API (highest effort)

`syside.CalculationUsage` gives calc names, inputs, outputs with direction. But binding resolution (which input binds to which upstream calc's output) lives in the owning part def's `owned_members` → `feature_value_expression`, not on the calc itself. `agentic_mbse/sysml/binding.py:extract_bindings()` can do this, but it re-derives what codegen already computes. The Jan 2026 research flagged binding resolution as "Risk 1: High Impact."

### Source 4: Generated Python modules

Each calc has a generated Python wrapper at `generated/modules/{analysis_name}/{calc_name}.py` with:
- Full docstring including "Calculation Specification" (the formula steps in Python syntax)
- Input/output Pydantic models with field descriptions
- Source citations (Source/Ref/Basis)
- Path to the handwritten implementation

These exist for every calc and are human-readable — good candidates for a "view Python" tab in the detail panel.

## The Overlay Problem

The structural view (subsystem parts as containers) and the calc DAG (calc-to-calc data flow) share a natural join key — in principle. The snapshot's occurrence tree IS the containment hierarchy, and each calc's `scope` places it inside that tree.

**In practice, the join is degenerate.** All calcs are owned by the plant, not by subsystems. The model architecture puts calcs in `'MFE Power Plant'` directly and uses redefinition bindings (`:>> capital_cost = blanket_cost.cost`) to push results into subsystem attributes.

Two paths forward:

1. **Heuristic mapping.** Assign calcs to subsystems by naming convention (`magnet_cost` → magnet, `blanket_cost` → blanket) or by which subsystem's attributes they write to via redefinition bindings. Fragile but immediate.

2. **Model reorganization.** Move calcs under subsystem parts in the SysML model. This would make the overlay trivial (syside gives containment directly) and would also improve model readability and validation structure. This is a modeling decision with implications beyond visualization.

**Recommendation for now:** start without the overlay. Show the calc DAG as a standalone view — 76 nodes in a directed graph, grouped by analysis file (which is a natural clustering: `mfe_magnet_cost` calcs together, `mfe_power_balance` calcs together, etc.). The `source_file` field gives this grouping for free. Add the structural overlay later if/when the model reorganizes calcs under subsystems.

## UX: Expanding Calc Nodes

The user wants to click a calc node and see its actual implementation. Three representation layers are available:

### Layer 1: SysML expressions (from snapshot `calc_expressions`)

```
discount_pow_n = (1.0 + discount_rate_in) ** operational_years_in
crf = discount_rate_in * discount_pow_n / (discount_pow_n - 1.0)
idc_factor = (1.0 + discount_rate_in) ** (construction_years_in / 2.0)
annual_capital = total_capital_in * idc_factor * crf
annual_energy_mwh = 8760.0 * net_electric_mw * availability_in
lcoe = (annual_capital + annual_om_in) / annual_energy_mwh
```

Already in the snapshot as `calc_expressions[]`. Human-readable, compact, shows the math. This is the best default for a detail panel.

### Layer 2: Doc comment with source citations (from snapshot `doc_comment`)

```
Generic discounted-cash-flow LCOE core [$/MWh]. Concept-agnostic: it
takes an already-rolled-up total capital and annual O&M...

  CRF        = d*(1+d)^N / ((1+d)^N - 1)      (capital recovery factor)
  IDC factor = (1+d)^(Yc/2)                    (interest during construction)
  ...

*Source**: economics.py
*Ref**: economics.py:6-10 (compute_crf)
*Basis**: Standard DCF LCOE
```

Also in the snapshot. Gives the engineering context, the authoritative source, and the mathematical notation. Good for a "Documentation" tab.

### Layer 3: Generated Python (from generated module files)

The full Pydantic module wrapper with input/output models, docstrings, and the handwritten implementation path. Available at `generated/modules/{analysis_name}/{calc_name}.py`. Would need to be read from disk at serve time (or bundled into the snapshot reader's output).

### Recommended UX

A side panel (not inline expand — 76 nodes would make inline expansion unwieldy) with three tabs:

1. **Formula** — the `calc_expressions` steps, syntax-highlighted as Python-like math
2. **Documentation** — the `doc_comment` with source citations
3. **I/O** — input ports (with upstream calc or parameter source) and output ports (with downstream consumers)

The panel updates on click. For the "view Python" use case, a link or button that opens the generated module file path — the viewer is in a code editor context, so a file path is actionable.

## Integration Path

### Step 1: Snapshot reader (`calc_dag_extractor.py`)

~100 lines of Python. Reads the snapshot JSON, builds:
- A node list (76 calc nodes + optionally 292 attr nodes) with display names, metadata
- An edge list (producer refs resolved to upstream calc names)
- Grouping by `source_file` (which analysis module the calc comes from)

Outputs either:
- Cytoscape JSON (for the interactive viewer)
- DOT (for static rendering)
- A combined format that carries the metadata for the detail panel

### Step 2: Interactive viewer

An HTML artifact (or served via the existing FastAPI endpoint) that renders the graph with:
- Nodes colored/grouped by analysis module
- Directed edges showing data flow
- Click-to-select with a side panel showing formula, docs, I/O
- Filter/collapse by analysis group (e.g. show only magnet chain, or only the path to LCOE)

Cytoscape.js from cdnjs with the dagre layout handles the graph rendering. The grouping by analysis file gives natural compound nodes (all `mfe_magnet_cost` calcs in one container, etc.).

### Step 3: Structural overlay (later)

When/if the model reorganizes calcs under subsystem parts, the snapshot's `scope` field will point to subsystem occurrences instead of the plant root. At that point, the overlay is a configuration change in the Cytoscape layout — calc nodes get `parent: "stellaris.magnet"` etc., and the viewer renders them inside the subsystem containers.

## Feasibility Assessment

The standalone calc DAG viewer (steps 1-2) is **straightforward** — ~0.5 day for the extractor, ~0.5 day for the viewer. The data is all there, pre-resolved, in a committed artifact. The main design work is the layout — 76 nodes with cross-group edges needs filtering and progressive disclosure.

The structural overlay (step 3) depends on a **modeling decision** about where calcs live. It's not a tooling blocker — it's a question about the right model architecture.

## Recommendations

1. **Start with the snapshot reader + standalone viewer.** Group calcs by `source_file` (analysis module), not by subsystem. This is the true organizational structure of the calc library.

2. **Include the detail panel from day one.** The snapshot has all the metadata — `calc_expressions`, `doc_comment`, I/O with resolved upstream names. The panel is the UX differentiator that makes this a navigation tool, not just a diagram.

3. **Don't build the structural overlay yet.** All calcs scope to the plant root. A heuristic mapping would be fragile and misleading. Wait for a modeling decision about calc organization.

4. **Consider filing `--emit-graph` upstream on sysml-codegen.** One line (`graph.model_dump_json()`) would make the typed `ComputationGraph` available as JSON alongside `pipeline.yaml`. Cleaner than parsing the snapshot's wire format long-term.

## Code References

- `sysml_codegen/elaboration/graph.py:162-189` — `CalcNode` (inputs, outputs, scope, display_name)
- `sysml_codegen/elaboration/graph.py:364-371` — `InstanceGraph` (calcs, attrs, occurrences, constraints)
- `sysml_codegen/elaboration/graph.py:131` — `OccurrenceRecord` (parent_id, containment_slot)
- `sysml_codegen/snapshot/instance_graph.py:1033-1050` — `encode/decode_instance_graph()`
- `proof_of_concept/extraction/types.py:33,37` — `ElementCategory.CALCULATION`, `EdgeCategory` stub
- `proof_of_concept/extraction/visualization.py:292-303` — structural view recursion (PartUsage only)
- `proof_of_concept/web/server.py:26-56` — FastAPI endpoint
- `exploration/stellarator_e2e/stellarator.snapshot.json` — live snapshot
- `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml` — pipeline YAML (93 modules)
- `exploration/stellarator_e2e/generated/modules/mfe_lcoe_dcf/lcoe_dcf.py` — example generated Python module
- `.project/research/20260118-180847_sysmlv2-visualization-strategy.md` — Jan 2026 visualization strategy (three views, Cytoscape MVP, Risk 1: binding resolution)

## Open Questions

1. **Should the viewer live in fusion-tea or sysml-codegen?** The snapshot reader is generic (any codegen snapshot); the grouping heuristics and detail panel content may be project-specific.
2. **Attr nodes:** The 292 attrs are the bound parameter values. Including them shows the full data flow (param → calc → param → calc) but makes the graph very dense. Better as hover-detail on edges than as rendered nodes.
3. **Path highlighting:** "Show me the path from R (major radius) to LCOE" would be the killer feature — trace the dependency chain through the graph, highlighting which calcs and which intermediate values carry the signal. The topological sort and edge structure support this; the UX is the design question.
4. **Model reorganization:** Should calcs move under subsystem parts? This has modeling implications beyond visualization (validation scoping, reuse patterns, codegen module grouping). Worth a separate discussion.
