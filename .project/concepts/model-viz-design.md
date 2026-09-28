# Design: Model Visualization Tool

**Status:** Proposed
**Owner:** Reid
**Created:** 2026-09-12

---

## Overview

The model's computational structure — a directed graph of 76 calculations wired through 150 producer edges (140 distinct calc pairs) — is the thing that determines how an input change propagates to a cost answer. There is no way to see it. The only existing visualization shows part containment (14 flat subsystem boxes), which answers "where are numbers filed?" not "how are numbers computed?"

This design describes a standalone HTML page that loads the codegen snapshot directly in the browser and renders the calc dependency graph as an interactive diagram. The core insight: the snapshot already carries the fully resolved DAG with metadata (formulas, doc comments, source citations, typed I/O). The visualization is a browser-side projection of that artifact, not a re-derivation or a conversion to an intermediate format.

---

## Problem

The model's most important dimension is invisible. Answering "how does major radius affect LCOE?" requires reading SysML source files across ~16 analysis modules and mentally tracing bindings. The computation chain that carries that signal — plasma scaling to magnet sizing to power balance to cost accounts to LCOE — exists only in the modeler's head.

The existing structural view doesn't help. It shows ownership: which subsystem contains which sub-parts. That's the filing structure, not the computation structure. The calcs are where the physics lives, and the edges between them are where the model's logic lives. Neither appears in the structural view.

Understanding what a single calc does is also harder than it needs to be. The codegen process already computed the formula steps, resolved the source citations, and typed every input and output. That metadata is serialized in the snapshot but has no surface — the modeler goes back to the SysML source and re-derives what the toolchain already knows.

---

## Goals

- Show the computation graph as an interactive diagram so a modeler can see how calcs connect without reading source files.
- Let the modeler click a calc and see its formula, documentation, and direct I/O — what feeds it, what it feeds — without opening a file.
- Provide spatial context for model changes: before a goal round, the modeler can see which analysis modules contain the relevant calcs and how they connect to the rest of the graph.
- Serve both the calc DAG and the structural view from one tool, so the modeler can switch between "how numbers are computed" and "where numbers are filed."

## Non-Goals

- **[OWNER]** Multi-hop path tracing ("show me everything between R and LCOE"). v2 candidate.
- **[AGENT]** Attribute nodes in the graph. The 292 attributes make the graph too dense — better as detail in the I/O panel.
- **[AGENT]** Editing the model from the visualization. This is a read-only tool.
- **[AGENT]** Constraint nodes, live auto-refresh, or generated Python rendering. Later additions if needed.

---

## Design Principles

### 1. Read the artifact, don't re-derive it

The codegen snapshot carries the fully resolved DAG — every calc-to-calc edge, doc comments, source citations, and formula steps for most calcs (65 of 76; 11 computed aggregation nodes have empty formula lists). The browser loads that JSON file directly and projects it to a graph. No Python conversion step, no syside parsing, no codegen import. This keeps the tool simple, fast, and decoupled from the model toolchain.

### 2. Group by computation, not by containment

The calcs cluster naturally by the source file they come from (17 groups — 15 analysis modules like magnet cost and power balance, plus 2 design files). Each group represents a physics or engineering domain. This is the computation's real structure — it's how the modeler thinks about the model. The containment hierarchy (which subsystem owns what) is a separate view for a separate question.

### 3. The detail panel is the differentiator

A graph diagram alone is just a picture. What makes this a navigation tool is the detail panel: click a calc, see its available formula steps, its documentation with source citations, and its direct inputs and outputs with links to their upstream/downstream calcs. The metadata is already in the snapshot — the panel surfaces it. Where metadata is absent (11 calcs have no formula text, 65 expression lists include documentation fragments alongside formulas), the panel shows what exists and labels what is missing — it never fabricates or omits silently.

### 4. Architecture-ready for structural overlay

Today all calcs scope to the plant root, so a structural overlay (calcs rendered inside subsystem containers) is degenerate. But the viewer should handle a non-root scope when the model eventually reorganizes calcs under subsystem parts. This means the data model carries source-file group identity and occurrence identity as separate fields, and the viewer derives the active Cytoscape `parent` from whichever mode is selected — source-file grouping in v1, occurrence containment when available. The two containment schemes cannot share a single field.

**Provenance:** Owner confirmed overlay readiness is `[OWNER]` — the viewer should support this when the model provides it.

## Architectural Bets

- **Snapshot as sole data source.** The browser loads the ~1 MB snapshot directly and projects it to Cytoscape elements in memory. No Python step, no intermediate format. A bet that the `instance-graph/v3` schema is stable enough to read directly. The metadata is not complete (11 calcs lack formula text, 52 inputs have null edges with defaults) but the design handles these explicitly. If the schema changes frequently, the alternative is an upstream `--emit-graph` flag. The existing structural extractor uses syside (a different data source); both paths coexist, not competing.
- **Cytoscape.js with dagre layout.** Compound graph support for grouped layout, dagre for automatic positioning. 76 nodes in 17 groups with cross-group edges. If dagre can't handle it, ELK.js is the upgrade path.
- **Browser-direct loading via file input.** No server, no fetch from a local path (browser CORS blocks `file://` fetch). Simpler than FastAPI and appropriate because this tool has no live queries — its data is a single static file.
- **`[AGENT]` Structural view migration is a follow-on, not v1.** The structural view already works in `proof_of_concept/`. The calc DAG is the new capability and should ship first. Source concept explicitly allows this sequencing.

---

## ADR Candidates

None — no decision crosses the ADR density bar. The snapshot-as-data-source decision is settled in the concept doc with owner attribution, and syside re-derivation is high-risk per Jan 2026 research.

## Core Model

### Projection Function

A JavaScript function that takes the raw snapshot JSON and produces Cytoscape elements. Runs in the browser — no Python step, no intermediate file. Navigates `snap.instance_graph.graph.calcs` to build calc nodes and edges.

For each calc, captures: `display_name`, `source_file`, `source_line`, `calc_expressions`, `doc_comment`, `inputs`, `outputs`, `scope`. Builds a `node_id` → calc lookup for edge resolution.

**Input edge classification.** Each calc input has one of four edge shapes:

| `edge` value | Kind | Count in stellarator | Graph edge? | Detail panel display |
|---|---|---|---|---|
| `{kind: "producer", target: {calculation, output}}` | Upstream calc output | 150 | Yes | Linked calc name + port |
| `{kind: "node", target: "<NodeId>"}` | Model parameter | 234 | No | Parameter name + value |
| `{kind: "literal", value: <number>}` | Inline constant | 10 | No | Literal value |
| `null` | Declared default | 52 | No | Default value from `metadata.default_value` |

Only producer edges become graph edges. All four kinds appear in the I/O panel.

**Edge resolution.** Producer edges carry `target.calculation` as a JSON-encoded `NodeId` string. The projection matches this against the `node_id` lookup. It also builds a reverse map from `(calc_node_id, output_port_id)` → downstream consumer calcs for the detail panel's output section.

**Grouping.** Groups calcs by full `source_file` path (avoiding basename collisions). Display label strips the prefix and extension — e.g., `root-0/analyses/mfe_magnet_cost.sysml` → `mfe_magnet_cost`. Each group becomes a Cytoscape compound node.

**Containment fields.** Each calc carries two identity fields: `source_group` (source file) and `occurrence_id` (resolved from `scope.wire` against the occurrence tree). The active Cytoscape `parent` is derived from whichever mode is selected — `source_group` in v1, `occurrence_id` when occurrence containment becomes meaningful.

### Viewer

A single HTML page. The user selects a snapshot file via a file input; the page reads it with `FileReader`, runs the projection function, and renders the graph using Cytoscape.js with dagre layout. Groups are compound nodes — expandable and collapsible via the `cytoscape.js-expand-collapse` extension. Clicking a calc node updates the detail panel.

**Collapse correctness.** The collapsed group graph has bidirectional edges (e.g., account-costs and generic-plant groups have edges both ways). The expand-collapse extension projects edges to visible container boundaries, retaining original endpoints. When a navigation action (I/O link click) targets a node inside a collapsed group, the viewer expands that group first, then selects and centers the target node.

### Detail Panel

A side panel with three sections:

1. **Formula** — the `calc_expressions` list, rendered as readable steps. Where expressions include documentation fragments (65 of 76 calcs), render all entries faithfully without distinguishing formula from documentation — the snapshot doesn't make that distinction. For the 11 calcs with empty `calc_expressions`, show "No formula available" rather than an empty section.
2. **Documentation** — the `doc_comment` text, preserving Source/Ref/Basis citations.
3. **I/O** — a table of inputs (name, edge kind, source — upstream calc link / parameter name / literal value / default value) and outputs (name, downstream consumer calcs as clickable links). Consumer calcs are resolved via the reverse output-port index.

### Structural Overlay (architecture-ready, `[OWNER]`)

Each calc carries an `occurrence_id` resolved from `scope.wire`. Today all calcs resolve to the plant root occurrence, so occurrence-based grouping is degenerate. When the model reorganizes calcs under subsystem parts, the occurrence IDs will point to different subsystem occurrences. Switching the viewer's parent derivation from `source_group` to `occurrence_id` enables the overlay. The occurrence tree carries `display_segment` for labels and `parent_id` for nesting — both are needed to emit correct container nodes and their ancestors. A test with a synthetic snapshot containing calcs scoped to different occurrences verifies this path.

---

## Prior Art

None relevant — index checked (10 entries). No entry concerns visualization architecture, data source selection, or the structural/DAG view split.

## Required Invariants

### Data Source

- The viewer runs entirely in the browser. It never requires Python, syside, sysml-codegen, or a server. The projection function takes raw snapshot JSON as input.
- The projection tolerates missing optional fields gracefully (e.g., a calc with no `doc_comment` renders with an empty documentation section, not a crash; a calc with empty `calc_expressions` shows "No formula available").

### Edge Resolution

- Every `"kind": "producer"` input edge resolves to exactly one upstream calc node via the `node_id` lookup. An unresolvable edge (target calc not in the snapshot) is rendered as a dangling input in the I/O panel with a warning — not silently dropped. (Currently zero unresolved in the stellarator snapshot; this is a guard, not an expected case.)
- Null edges (52 inputs with `edge: null` and a `metadata.default_value`) appear in the I/O panel as defaulted inputs. They are not graph edges and are not silently omitted.
- `"kind": "node"` and `"kind": "literal"` edges appear only in the I/O panel, never as graph edges.
- Output consumers are resolved via a reverse index from `(calc_node_id, output_port_id)` → downstream calc list. A port with no consumers shows as a terminal output.

### Grouping and Containment

- Every calc belongs to exactly one source-file group, derived from the full `source_file` path (not just the basename, to avoid collisions). A calc with no `source_file` is placed in an "ungrouped" fallback.
- Source-file group identity and occurrence identity are carried as separate fields on each calc node. The active Cytoscape `parent` is derived from whichever mode is selected. Switching modes does not lose either identity.
- Groups are stable across viewer sessions for the same snapshot.

### Collapse and Navigation

- Expanding and collapsing a group preserves all original edge endpoints. The expand-collapse extension projects edges to visible container boundaries; the original source/target data is not mutated.
- When a navigation action targets a node inside a collapsed group, the group is expanded before the node is selected. A hidden target is never silently ignored.
- Bidirectional edges between collapsed groups are rendered faithfully — they represent real computation dependencies in both directions, not cycles within a single group.

## How It Works

### Opening the viewer

The modeler opens the HTML page and selects a codegen snapshot via the file input. The page reads the file with `FileReader`, runs the projection function, and renders the graph. No server, no conversion step, no command line.

### Navigating the graph

The graph renders with source-file groups as labeled compound nodes. All groups start collapsed — the modeler sees 17 labeled boxes with inter-group edges (some bidirectional — this is expected, not a cycle). Clicking a group expands it to show its member calcs with intra-group and inter-group edges. The dagre layout re-flows on expand/collapse.

### Inspecting a calc

Clicking a calc node highlights it and its direct edges (one hop upstream, one hop downstream). The detail panel updates to show the formula steps, documentation, and I/O table. Clicking an upstream or downstream calc name in the I/O table selects that node, re-centers the view, and updates the panel — enabling one-hop-at-a-time graph traversal.

### Switching to the structural view

When the structural view is migrated (follow-on), a toggle switches between the calc DAG and the structural containment view. Both views share the same page shell and detail panel pattern, but display different graph data — one from the snapshot projection, one from the structural extractor.

## Edge Cases and Failure Modes

- **Snapshot schema change.** The projection targets `instance-graph/v3`. If the schema version doesn't match, the page shows a clear error naming the expected and found versions. No graceful degradation — a schema mismatch means the field structure may be different, and silent wrong data is worse than a clear error.
- **Large group (33 calcs in `mfe_account_costs`).** The cost accounts group is 3x larger than any other. Expanding it produces a dense subgraph. Mitigation: dagre handles this size, and the group starts collapsed. If it's still unwieldy, a future pass could split it by CAS tier (CAS10–CAS90), but that's a heuristic the v1 doesn't need.
- **Unresolvable producer edge.** If a calc input has `"kind": "producer"` but its target `node_id` isn't in the snapshot's calc list, the projection marks the input as "unresolved" in the I/O panel with a visual warning. Currently zero unresolved in the stellarator snapshot.
- **Calcs with no formula text.** 11 calcs (aggregation nodes like `total_capital`, `cas22_capital`) have empty `calc_expressions`. The detail panel shows "No formula available" and still displays the doc comment and I/O sections. This is an honest gap in the snapshot's metadata, not a viewer bug.
- **Defaulted inputs with null edges.** 52 inputs have `edge: null` with a `metadata.default_value`. These are declared defaults — the calc uses the default because no upstream binding exists. The I/O panel shows the input name and default value, labeled as "default." They are not graph edges.
- **Hidden navigation target.** Clicking an I/O link that targets a calc inside a collapsed group. The viewer expands the target's group, then selects and centers the target node. Without this, the link silently fails.
- **No snapshot available.** The page shows a file-load prompt; the tool's scope starts after codegen.
- **Browser performance.** 76 nodes is well within Cytoscape.js + dagre's comfortable range. Collapsed default shows 17 nodes.

## Vocabulary

- **Calc node**: A calculation usage instance in the snapshot — one of the 76 calcs. Identified by `node_id`, displayed by `display_name`.
- **Producer edge**: A data-flow edge where one calc's output feeds another calc's input. The `"kind": "producer"` discriminator in the snapshot's input edge structure. 150 in the stellarator snapshot, covering 140 distinct calc pairs.
- **Source-file group**: A cluster of calcs that share the same `source_file` value. 17 groups in the stellarator snapshot — 15 from analysis files (e.g., `mfe_magnet_cost.sysml`), 2 from design files.
- **Null edge / defaulted input**: An input with `edge: null` and a non-null `metadata.default_value`. The calc uses a declared default because no upstream binding exists. 52 in the stellarator snapshot.
- **Projection function**: The JavaScript function that takes raw snapshot JSON and produces Cytoscape elements in memory. No intermediate file.
- **Structural overlay**: Rendering calcs inside their owning subsystem container, using `occurrence_id` (resolved from `scope.wire`) as the Cytoscape parent. Degenerate today (all calcs scope to plant root).
- **Detail panel**: The side panel that shows a selected calc's formula (or "No formula available"), documentation, and I/O.

## System Confidence

Three claims must hold for the system to work:

1. **Edge resolution is complete and the reverse index is consistent.** Every `"producer"` edge resolves to a calc in the projection's node set. The reverse output-port index agrees with the forward edge set — if calc A's input points at calc B's output, then calc B's output consumers include calc A. The projection builds both from the same calc list, so inconsistency requires a snapshot-internal defect.

2. **Collapse preserves edge semantics.** Expanding a group, navigating within it, and collapsing it again produces the same inter-group edge set as before. The expand-collapse extension's meta-edge projection must not drop, duplicate, or reverse edges. This is testable by comparing the edge set before collapse, during collapse, and after re-expand.

3. **Navigation reveals hidden targets.** Every I/O link click that targets a node in a collapsed group results in the target being visible and selected. This is an interaction contract on the viewer, not on the layout engine.

Layout quality (whether dagre produces a readable arrangement for the 33-node cost accounts group) affects usability, not correctness — fixed by tuning, not architecture changes.

## Validation Strategy

- **Edge resolution and reverse index**: Zero unresolved producers for stellarator; reverse index matches forward edge set.
- **Input completeness**: All four edge kinds (producer, node, literal, null) appear in the I/O panel for a calc that has each.
- **Count match**: 76 calcs and 150 producer edges from the stellarator snapshot.
- **Collapse round-trip**: Inter-group edge set identical before collapse and after re-expand.
- **Hidden-target navigation**: I/O link targeting a collapsed node results in expansion + selection.
- **Overlay readiness**: Synthetic snapshot with two calcs in different occurrences → correct parent assignments.
- **Layout**: Manual inspection of the stellarator graph. Judgment call, not automated.

## Next-Stage Handoff

**Decisions and proposals** (`[OWNER]` entries are settled; `[AGENT]` entries are proposals ratified by the 2026-09-13 review, not owner rulings):
- **`[OWNER]`** Data source is the codegen snapshot, read as JSON — no syside, no codegen import.
- **`[OWNER]`** v1 includes the detail panel with formula, docs, and direct I/O. Multi-hop path tracing is v2.
- **`[AGENT]`** Browser-direct loading via file input — no Python conversion step, no server, no intermediate format.
- **`[AGENT]`** Grouping is by `source_file`, not by subsystem containment. Source-file and occurrence identity are separate fields.
- **`[AGENT]`** Detail panel shows available formula, documentation, and I/O with clickable cross-references. Absent metadata is labeled, not hidden.
- **`[OWNER]`** Structural overlay is architecture-ready via separate `occurrence_id` field, verified by test, not a v1 visual feature.
- **`[AGENT]`** Structural view migration is a follow-on, not v1. Source concept explicitly allows this sequencing.

**Spec/design detail still needed next:**
- Detail panel layout — proportions, scroll behavior, how I/O links animate the graph selection.
- Expand-collapse extension integration — which extension version, how meta-edges are styled, how bidirectional inter-group edges render when collapsed.
- How the 11 calcs with empty formula text should present — just "No formula available," or should the spec pursue an upstream metadata improvement?

**First risk to de-risk** (spiked 2026-09-13: `.project/active/model-viz/spike-layout-findings.md` — bet confirmed with conditions on edge-endpoint mutation, bundling, and bidirectional rendering):
- The dagre layout quality with 76 nodes in 17 groups, especially the 33-node `mfe_account_costs` group. A `/_my_spike` with a hardcoded Cytoscape.js page and the real snapshot data would confirm whether the layout is navigable before building the full tool.

**Proof obligations:**
- Collapse round-trip: the inter-group edge set before collapse = after re-expand.
- Hidden-target navigation: an I/O link click targeting a collapsed node results in expansion + selection.

## Summary

The model's computation graph is invisible today. The codegen snapshot carries the fully resolved DAG with most of the metadata needed — 150 producer edges across 140 calc pairs, formula text for 65 of 76 calcs, doc comments with source citations. This design loads that artifact directly in the browser, projects it to a grouped interactive diagram with a detail panel, and stays decoupled from the model toolchain. Where metadata is incomplete, the viewer shows what exists and labels what is missing. Source-file grouping and occurrence identity are carried separately to support a future structural overlay without overloading the renderer's parent mechanism.
