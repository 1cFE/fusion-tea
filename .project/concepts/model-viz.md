# Concept: Model Visualization Tool

**Created:** 2026-09-12
**Status:** Draft

---

## Problem Statement

The stellarator model's computational structure is a directed graph of 76 calc usages wired through ~178 data-flow edges — plasma geometry feeds radial build, which feeds fusion power, which feeds power balance, which feeds LCOE. This is the model's actual skeleton: the thing that determines how an input change propagates to a cost answer.

There is no way to see it. The only visualization tool (`proof_of_concept/extraction/`) shows part containment — 14 flat subsystem boxes under a plant root. That view shows where numbers are *filed* (which CAS account a cost belongs to), not how they are *computed* (which calcs feed which). For this model, the containment tree is the least interesting dimension.

This matters in three concrete ways:

1. **Navigation.** Answering "how does major radius affect LCOE?" requires reading SysML source files and mentally tracing bindings across ~16 library analysis modules. The calc chain that carries that signal is invisible.

2. **Inspection.** Understanding what a calc does means finding the right `.sysml` file, locating the calc def, and parsing the syntax. The codegen snapshot already carries the formula steps and doc comments with source citations — but no surface exposes them.

3. **Development direction.** The demo maturation goals (burn-control, minor-radius, plant-closure) drive model changes. Each goal's scope question is "which calcs are affected, what feeds them, what do they feed." That is a graph question with no visual tool.

## Owner's Words

- **[OWNER-VERBATIM]** "it only shows structure? No I/O or behavioral relationships?"
- **[OWNER-VERBATIM]** "can you explain to me why we don't have any organization or structure of the models?"
- **[OWNER-VERBATIM]** "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation"
- **[AGENT]** The structural overlay (calcs rendered inside subsystem containers) should be architecturally supportable for when the model eventually organizes calcs under subsystem parts. The owner asked about overlay feasibility and confirmed it's not a v1 requirement — the architectural readiness is an agent inference from that conversation.
- **[OWNER]** Direct I/O (one-hop upstream/downstream per calc) is v1. Multi-hop path tracing ("show me everything between R and LCOE") is v2.

## Success Criteria

When this work is complete:

1. **The calc dependency graph is visible as an interactive diagram.** All 76 calcs render as nodes with directed edges showing data flow. Calcs are grouped by analysis module (the `source_file` field — e.g. all `mfe_magnet_cost` calcs together). Groups are expandable and collapsible.
2. **Clicking a calc node shows its implementation.** A detail panel displays: (a) the formula steps from `calc_expressions`, (b) the doc comment with source citations, (c) direct inputs with their source (upstream calc, model parameter, or literal) and direct outputs with their downstream consumers.
3. **The data comes from the codegen snapshot.** The viewer reads `stellarator.snapshot.json` (or any codegen snapshot). No syside parsing, no model loading, no binding resolution at visualization time.
4. **The existing structural view migrates into the same package.** The syside-based part-containment extractor from `proof_of_concept/extraction/` moves to `src/model_viz/extractors/` and is served alongside the calc DAG view.
5. **The structural overlay is demonstrably supportable.** Given a synthetic or future snapshot where calcs have non-root scopes, the viewer renders them inside subsystem containers without viewer code changes — only a different `parent` value from the extractor. Verified by a test with a modified snapshot.

---

## Why This Shape

- **Key bet:** The codegen snapshot is the right data source. It carries the fully resolved DAG with metadata (formulas, doc comments, source locations, I/O) — the same data that sysml-codegen already computed during elaboration. Reading it is ~100 lines of JSON traversal. Re-extracting from syside would duplicate the binding resolution that the Jan 2026 research flagged as "Risk 1: High Impact."
- **Why this shape is promising:** The snapshot exists for every generated package, is regenerated on every codegen run, and is fingerprinted and validated. The visualization is downstream of codegen, not parallel to it — no new parsing infrastructure to maintain.
- **Constraint to preserve downstream:** The viewer must not depend on sysml-codegen as a Python import. It reads the snapshot as JSON. This keeps the visualization installable and runnable without the codegen toolchain.

---

## User Stories

### Navigation

**US-1: See the computation graph.**
As a modeler, I can open the model visualization and see how calcs connect — which feeds which, where the path from plasma geometry to LCOE runs through — so that I understand the model's structure without reading SysML source.

**US-2: Find a calc's context.**
As a modeler, I can click a calc node and see its formula steps, its documentation with source citations, and its direct I/O (what feeds it, what it feeds), so that I can understand what the calc does and where it sits in the chain without opening a file.

### Development

**US-3: Orient before a model change.**
As a modeler planning a goal round, I can look at the graph and see which analysis modules contain the calcs I need to touch, what their direct inputs and outputs are, and which other modules they connect to, so that I have spatial context for the change before opening any files.

**US-4: Inspect both views.**
As a modeler, I can switch between the structural view (part containment) and the calc DAG view in the same tool, so that I can see both how numbers are organized and how they are computed.

---

## Key Concepts

### 1. Calc DAG Extractor

Reads a codegen snapshot JSON and produces a graph data structure: calc nodes (with display name, formula steps, doc comment, source file/line, I/O ports) and directed edges (producer refs resolved to upstream calc names). Groups calcs by analysis module using the `source_file` field.

### 2. Analysis Module Groups

The 76 calcs cluster naturally by the library analysis file they come from (~16 groups: `mfe_magnet_cost`, `mfe_power_balance`, `mfe_plasma_scaling`, etc.). Each group represents a physics/engineering domain. These groups are expandable containers that show their member calcs when opened and collapse to a single labeled box when closed.

### 3. Detail Panel

A side panel that updates on calc-node click. Three sections: (a) formula steps (the `calc_expressions` from the snapshot, rendered as syntax-highlighted math), (b) documentation (the `doc_comment` with Source/Ref/Basis citations), (c) I/O table (each input's source and each output's consumers, with links to the upstream/downstream calc nodes in the graph).

### 4. Structural Overlay (architecture-ready)

Each calc node carries an optional `parent` field. Today all calcs scope to the plant root, so no overlay is possible. When the model reorganizes calcs under subsystem parts, the extractor populates `parent` with the subsystem occurrence's `display_segment`, and the viewer renders calcs inside their owning subsystem container — expand/collapse handles "calc blocks render in the lowest parent which is viewed" natively. The grouping switches from analysis-module to subsystem with no viewer changes.

---

## Scope of Behavior Changes

### New artifacts to create
- `src/model_viz/` — Python package with extractors, a local server, and an interactive frontend
- A snapshot reader that produces graph data (calc nodes, directed edges, metadata for the detail panel)
- An interactive graph viewer with grouped layout, expand/collapse, and a detail panel

### Existing artifacts to modify
- `proof_of_concept/extraction/` — code migrates to `src/model_viz/extractors/structural.py`; the `proof_of_concept/` directory remains for reference but is no longer the live code

### Behavior changes by workflow stage
- **Model development:** After a codegen run, the snapshot is viewable as an interactive calc DAG. This is a new capability — today the snapshot is only machine-consumed.
- **Goal planning:** The calc DAG provides visual context for scoping which calcs a goal round will touch.

---

## Non-Goals / Out of Scope

- **[OWNER]** Multi-hop path tracing (v2 candidate — "show me everything between R and LCOE")
- **[AGENT]** Attribute nodes in the graph. The 292 attrs make the graph too dense. Better as hover-detail on edges or in the I/O panel.
- **[AGENT]** Editing or modifying the model from the visualization. This is a read-only tool.
- **[AGENT]** Constraint nodes. The 14 constraints could be a later addition but are not needed for the core navigation and inspection use cases.
- **[AGENT]** Live model watching / auto-refresh on model changes. The viewer reads a snapshot file; the user reloads after a codegen run.

---

## Assumptions & Prerequisites

- A codegen snapshot exists for the model being visualized. For the stellarator, this is `exploration/stellarator_e2e/stellarator.snapshot.json`.
- The snapshot schema (`instance-graph/v3`) is stable enough to read directly as JSON. If it changes frequently, an upstream `--emit-graph` flag on sysml-codegen would provide a more stable interface.
- Cytoscape.js with dagre layout handles 76 nodes in ~16 groups with cross-group edges at interactive frame rates.

## Open Questions

1. Should the tool also serve pre-rendered static output (SVG/PNG) for embedding in documents, or is interactive-only sufficient for v1?
2. Should the detail panel link out to the generated Python module files (e.g. `generated/modules/mfe_lcoe_dcf/lcoe_dcf.py`)? The snapshot carries `source_file` for the SysML source but not the generated Python path — that would require a convention-based path derivation.
3. How should the viewer handle a snapshot with a different schema version than expected? Fail with a clear message, or degrade gracefully?

---

## Next-Stage Handoff

**Settled here:**
- **[OWNER]** Data source is the codegen snapshot, read as JSON. Not syside, not pipeline YAML, not a codegen Python import.
- **[OWNER]** v1 includes the detail panel with formula, docs, and direct I/O. Multi-hop path tracing is v2.
- **[OWNER]** Code lives at `src/model_viz/`. The existing structural view migrates in.
- **[OWNER]** Structural overlay is an architecture requirement (the viewer supports it when the model provides it), not a v1 feature.

**Needs spec next:**
- The extractor's output schema — what fields per node, what fields per edge, what metadata for the detail panel
- Detail panel layout and interaction — tabs vs sections, how I/O links navigate the graph
- How the structural view and calc DAG view coexist in the UI (tabs, toggle, side-by-side)
- Serving model — local server (like concept explorer) vs standalone HTML loading a JSON file (simpler, no server dependency)
- Migration plan for `proof_of_concept/extraction/` code — whether it ships with v1 or follows

**Decomposition guidance:**
- This is a single standard-scale work item. The extractor and viewer are tightly coupled and should ship together. The structural view migration could be a follow-on if it adds scope risk.

---

## Appendix: Research Reference

Full research at `.project/research/20260912-004633_calc-dag-visualization.md`. Key data points:

- Snapshot carries `calc_expressions`, `doc_comment`, `source_file`, `source_line`, `inputs` (with resolved producer refs), `outputs` per calc
- Edge resolution verified: `fusion.V <- geom`, `fusion.n_T0_in <- sustain`, etc.
- All 76 calcs scope to the plant root occurrence (`c1525587-...`). Subsystem occurrences exist but own zero calcs.
- The existing `types.py` already defines `ElementCategory.CALCULATION` (excluded) and stubs `EdgeCategory.DEPENDENCY`
- Jan 2026 visualization research planned three views (structural, cost, dependency) sharing one `ViewResult` shape
