# Spec: Model Visualization — Calc DAG Viewer

**Status:** Certified 2026-09-13 (audit.md)
**Owner:** Reid W
**Created:** 2026-09-13
**Complexity:** MEDIUM
**Branch:** feat/model-viz

---

## Problem

The stellarator model computes its answer through 76 calculations wired together by 150 producer bindings. That wiring decides how a change to an input reaches LCOE. Nobody can see it today.

- **The only viewer shows filing, not computation.** `proof_of_concept/extraction/` draws part containment: 14 subsystem boxes under a plant root. It excludes calculations entirely.
- **Inspecting one calc means reading SysML by hand.** To learn what a calc does, a modeler finds the `.sysml` file, locates the calc, and traces its bindings across about 16 source files.
- **The data already exists.** The codegen snapshot (`exploration/stellarator_e2e/stellarator.snapshot.json`, schema `instance-graph/v3`) carries every calc, its resolved input bindings, formula steps reconstructed by codegen, doc comment, and recorded source location. No surface shows it.

The owner's ask, `[OWNER-VERBATIM]` (concept § Owner's Words): "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation."

This item builds a read-only viewer that turns a snapshot into an interactive calc graph with a detail panel. It is the first code under `src/model_viz/`.

## Success Criteria

Every criterion below is observable in a real browser and checkable from pytest through Python Playwright. Counts are for the stellarator fixture at SHA-256 `c9f6e2a52ea69cf95dcee015496f906f705d1130bce1a529bde510299a5ce393`, verified by read-only JSON probes on 2026-09-13. They are fixture facts, not constants the viewer may hardcode.

**Where edges are read from.** Every edge criterion reads the edges the renderer is currently displaying, queried from the live page. Reading the snapshot or the projection output instead would make the check true by construction, and does not satisfy the criterion.

**Loading**

- [x] A modeler opens the viewer page, picks the stellarator snapshot through the page's file picker, and the graph renders with no server, no command line, and no Python step.
- [x] Loading a snapshot whose `instance_graph.schema_version` is not `instance-graph/v3` shows an error that names both the expected version and the version found. No graph renders.
- [x] Loading a JSON file that is not a codegen snapshot (no `instance_graph.schema_version`) shows a clear error. No graph renders and the page does not crash.
- [x] Loading a file that is not JSON at all (for example a PDF picked by mistake) shows a clear error. No graph renders and the page does not crash.
- [x] Loading a second snapshot after a first replaces the first. Nothing from the first snapshot remains in the graph or the panel.

**The graph (stellarator fixture)**

- [x] 76 calc nodes exist, one per entry in `instance_graph.graph.calcs`.
- [x] 17 source-file groups exist, one per distinct full `source_file` path. The largest, `root-0/analyses/mfe_account_costs.sysml`, holds 33 calcs. Two groups come from design files (`mfe_plant.sysml` with 10 calcs, `stellarator_plant.sysml` with 1).
- [x] With all groups expanded, the displayed calc-to-calc edges cover exactly 140 distinct (upstream calc, downstream calc) pairs, all pointing from producer to consumer. Every displayed edge corresponds to at least one producer binding.
- [x] No input record of kind `node`, `literal`, or `null` produces a graph edge.
- [x] **All collapsed.** With every group collapsed, the displayed edges follow the visible-edge rule (Known Requirements § Graph): exactly 35 directed group-to-group pairs. The 4 group pairs that depend on each other both ways (account-costs ↔ generic plant, plasma-scaling ↔ plasma-sustainment, magnet-field ↔ plasma-scaling, power-balance ↔ primary-loop) each show as two directed edges. No collapsed group shows a self-loop, including the 5 groups with internal edges.
- [x] **Collapse round-trip, every group.** Starting from all groups expanded, for each of the 17 groups in turn: collapse it, then re-expand it. While it is collapsed, the displayed edge set matches the visible-edge rule for that state. After re-expanding, the displayed edge set is identical to the set before collapsing. No edge is dropped, duplicated, or reversed.
- [x] **Collapse round-trip, interleaved.** For the two-way pair account-costs and generic plant, starting from all expanded: collapse account-costs, collapse generic plant, expand account-costs, expand generic plant. After every step the displayed edge set matches the visible-edge rule for that mixed state, and after the last step it is identical to the starting set.

**The detail panel**

- [x] Clicking a calc node opens a panel for that calc showing: its formula, its doc comment, its recorded source location (`source_file:source_line`), its inputs, and its outputs.
- [x] For each of the 65 calcs with a non-empty `calc_expressions` list, every formula entry appears in the panel verbatim and in snapshot order; no entry is lost. The doc comment text appears in the panel at least once.
- [x] For each of the 11 calcs with an empty `calc_expressions` list (for example `total_capital`, `cas22_capital`), the panel shows formula text derived from the calc's `expression_ir` tree, labelled "derived from expression structure; the snapshot has no formula text for this calc." On the fixture all 11 trees render. In a synthetic copy where one of those trees contains an operator outside the renderable set, that calc's panel shows "No formula available" instead, with the same no-formula-text label and no crash. These 11 also have no doc comment; the panel labels that absence and still shows source location and I/O.
- [x] The inputs list shows all four input kinds, each labelled by kind. On the fixture: `fuel_handling` shows a producer input (linked upstream calc and port), a parameter input (attribute name and value), and a literal input (`ref_power` = 1000.0); `fuel` shows a defaulted input (`s_per_fpy_in`, default 31536000.0). Across the fixture the inputs total 150 producer, 234 parameter, 10 literal, and 52 defaulted.
- [x] **Bindings, both directions.** Each of the 150 producer bindings appears twice: in its consumer's panel as a producer input naming the upstream calc and output port, and in its producer's panel as a consumer of that exact output port.
- [x] Each output lists the calcs that consume it. An output with no calc consumer says so. On the fixture, 64 of the 155 output ports have no calc consumer.
- [x] **Navigation.** After clicking an upstream or downstream calc link in the panel, the linked calc is selected, lies fully inside the viewport, and the panel shows that calc.
- [x] **Hidden-target navigation.** With the current calc's group expanded and the link target's group collapsed, clicking the link ends with: the target's group expanded, the target selected and fully inside the viewport, and the panel showing the target. The test covers both an upstream link and a downstream link. The click is never silently ignored.

**Guards (synthetic snapshots derived from the fixture)**

- [x] **Unresolvable producer.** In a copy of the fixture with one calc removed, where that calc has at least one consumer: every consumer's panel shows each input that pointed at the removed calc, marked unresolved with a visible warning; no displayed edge points at a node that does not exist; and the remaining 75 calcs render.
- [x] **Overlay readiness.** In a synthetic snapshot where calcs scope to different non-root occurrences, switching the viewer's grouping to occurrence containment places each calc inside a container for its occurrence, nested under that occurrence's ancestors, with no change to viewer code. The test covers two sibling occurrences that share a `display_segment` and proves they stay separate containers, and covers calcs from one source file landing in different occurrences.

## Known Requirements

**Data source and boundary**

- **[NEED]** The viewer's data comes from a codegen snapshot read as JSON. It does not use syside, does not import codegen Python, and does not re-derive bindings. (Concept § Next-Stage Handoff.)
- **[NEED]** The code lives at `src/model_viz/`. The repo has no `src/` directory today; this item creates it. (Concept § Next-Stage Handoff.)
- **[INFERRED]** The viewer is a standalone HTML page that loads the snapshot through a file picker, with no server. Proposed in the concept design § Architectural Bets and ratified by the 2026-09-13 review. Browsers block `fetch` of `file://` paths, so a picker is the serverless route.
- **[INFERRED]** The page checks `instance_graph.schema_version` before reading anything else and refuses any version other than `instance-graph/v3`. There is no best-effort degradation; wrong data shown silently is worse than a clear error. (Brief decision 3; design § Edge Cases.)

**Snapshot shapes the viewer must honour** — verified against the fixture:

- **[HARD]** Calcs live at `instance_graph.graph.calcs`. Each calc's identity is its `node_id`, a string.
- **[HARD]** Each input is a record with `name`, `port`, `metadata`, and `edge`. `edge` takes one of four shapes: `{kind: "producer", target: {calculation: <calc node_id string>, output: <output id>}}`; `{kind: "node", target: <attribute node_id string>}`; `{kind: "literal", value: <number>}`; or `null`, with the default in `metadata.default_value`. On the fixture, producer targets match a calc `node_id` exactly (150 of 150) and node targets match an attribute `node_id` in `instance_graph.graph.attrs` (234 of 234).
- **[HARD]** Each output carries `name`, `declaration`, and `port.{calculation, output}`. Consumers of an output are found by matching a producer target's `(calculation, output)` pair against it.
- **[HARD]** Each calc's `scope.wire` names an occurrence. Occurrences live at `instance_graph.graph.occurrences`, each with `occurrence_id`, `parent_id` (null at the root), and `display_segment`. On the fixture, all 76 calcs scope to the root occurrence `stellaris`, and the 13 subsystem occurrences own no calcs.
- **[HARD]** `calc_expressions` is not source text. Codegen rebuilds each line from the parsed expression tree and appends the whole doc comment as the final entry (`../sysml-codegen/src/sysml_codegen/extraction/extractor.py:147-150`, `:175-180`). On the fixture, the final entry of all 65 non-empty lists contains the calc's doc comment.
- **[HARD]** `source_file` is relative to a snapshot root the snapshot does not name (`root-0/...`; `sources.roots` carries an ordinal and no path). The same relative files exist in more than one tree on disk (`exploration/stellarator_e2e/models/` and `models/library/` + `models/designs/`).

**Graph**

- **[INFERRED]** Only producer inputs become graph edges. Parameter, literal, and defaulted inputs appear only in the detail panel. (Design § Required Invariants, ratified by review.)
- **[INFERRED]** A producer input whose target calc is not in the snapshot is shown in the panel as unresolved, with a warning. It is never dropped, and no edge is drawn to a node that does not exist. (Design § Edge Resolution.)
- **[INFERRED]** A calc's group identity is its full `source_file` path, so two files with the same base name never merge. A shortened label is display only. A calc with no `source_file` goes into an "ungrouped" group. (Design § Grouping and Containment.)
- **[INFERRED]** Each calc carries its source-file group and its occurrence as two separate fields. The container a calc is drawn inside is derived from whichever grouping mode is active; switching modes loses neither field. (Design § Design Principles 4; review M2.)
- **[INHERITED: concept § Next-Stage Handoff; design § Design Principles 4]** The viewer supports drawing calcs inside subsystem containers when the model scopes calcs to non-root occurrences. It is an architecture requirement, not a v1 visual feature. Occurrence containers are keyed by `occurrence_id`, not `display_segment`, and include ancestors.
    - Grade conflict, surfaced not resolved: the concept's Owner's Words records overlay readiness as `[AGENT]` inference, while its handoff and the design's provenance note record it as `[OWNER]`. The 2026-09-13 review leaves it pending owner resolution. The obligation is the same under either grade; only whether it may be challenged without asking the owner differs.
- **[INFERRED]** **The visible-edge rule.** In every collapse state, each producer binding is shown by an edge from the nearest visible ancestor of its producer calc to the nearest visible ancestor of its consumer calc, pointing producer to consumer. A calc that is itself visible is its own nearest visible ancestor. When both endpoints map to the same collapsed container, the binding is hidden, not drawn as a self-loop. A pair of containers that feed each other shows as two directed edges, one each way, and is not flagged as a cycle. This matches the concept's phrase "calc blocks render in the lowest parent which is viewed." (Design § Collapse and Navigation; spec review L3-2.)

**Detail panel**

- **[NEED]** Selecting a calc shows its formula, its documentation, and its direct I/O. (Concept § Next-Stage Handoff: "v1 includes the detail panel with formula, docs, and direct I/O.")
- **[NEED]** The I/O is one hop only: what feeds each input and which calcs consume each output. (Concept § Owner's Words: one-hop I/O is v1.)
- **[INFERRED]** The panel shows the calc's source location as recorded in the snapshot (`source_file:source_line`). It is display only: a `root-0/`-relative referent, not an openable path. All 76 fixture calcs have both fields, including the 11 with no formula text.
- **[INFERRED]** For a calc with empty `calc_expressions`, the panel renders its `expression_ir` tree as derived formula text, labelled "derived from expression structure; the snapshot has no formula text for this calc." The renderable set is `+`, `*`, attribute references, and literals, which covers every operator the 11 fixture trees use (35 `+`, 4 `*`, 47 references, 3 literals). A tree containing anything else shows "No formula available" with the same label. (Orchestrator ruling 2, 2026-09-13.)
- **[INFERRED]** Missing metadata is labelled, never hidden. A missing doc comment is labelled as missing. A parameter input whose attribute has no value is labelled as such. (Brief decision 4; design § Design Principles 3.)
- **[INFERRED]** Formula entries render as the snapshot's text, in order. The page does not try to separate formula lines from documentation fragments inside them, because the snapshot does not mark the difference. (Design § Detail Panel; review m2.)
- **[INFERRED]** Every input shows its kind: producer (linked upstream calc and output port), parameter (attribute name and value), literal (value), or default (default value).

**Testing**

- **[HARD]** There is no `node` on this machine. Browser-level tests run through Python Playwright from pytest (`uv run python -m pytest`). Python Playwright is installed in the project venv, and `scripts/browser_inspect.py` already drives a real browser.

## Non-Goals

- **Verbatim SysML source text and Python views.** `[AGENT]` (orchestrator ruling 1, 2026-09-13.) The owner asked for "the actual SysML or python representation." v1 shows the formula lines codegen reconstructed from the parsed model (a SysML-syntax representation of the calc body, not verbatim source), the doc comment, and the recorded source location. It does not show the source text itself or any Python, including `generated/modules/.../*.py`. Reason: the snapshot carries neither verbatim SysML nor Python, and loading the model source tree would be a second data source, which the owner's snapshot-only data-source decision excludes for now.
- **Structural view migration.** Moving the syside part-containment extractor from `proof_of_concept/extraction/` into `src/model_viz/` is a follow-on item, registered at `.project/backlog/BACKLOG.md` § Flagged — don't lose ("Structural view migration into `src/model_viz/`"). It has a different producer (syside) and a different serving model (a Python server); folding it in doubles scope and reopens the serving question this item settles for the calc graph. Concept Success Criterion 4 and User Story US-4 are deferred to that item, not dropped. (Orchestrator decision; the concept's decomposition guidance allows it.)
- **Multi-hop path tracing** ("show me everything between R and LCOE") is v2. (`[OWNER]`, concept § Owner's Words.)
- **Static SVG or PNG export** is out of scope for v1.
- **Upstream metadata improvements** to add formula text or doc comments for the 11 computed calcs are out of scope.
- **Attribute nodes, constraint nodes, model editing, and auto-refresh** are out of scope. The viewer is read-only and shows calcs; the user reloads after a codegen run. (Concept § Non-Goals, agent-grade.)

## Open Questions / Deferred to design

- **The doc comment appears twice in the data.** The final `calc_expressions` entry repeats the doc comment. Design decides whether the panel shows it once or twice; the success criteria require only that no formula entry is lost and the doc comment is shown at least once.
- **Find a calc by name.** With groups collapsed, reaching a known calc such as `cas22_capital` means guessing its group. Whether v1 offers a way to find a calc by name is a usability question for design, not a requirement.
- **Source location context.** Whether to show a root hint or the per-file SHA-256 from `sources.files`, so a modeler can tell which on-disk tree the location matches.
- **One edge per binding or one per calc pair.** On the fixture, some calc pairs are joined by more than one binding (150 bindings over 140 pairs). Design picks whether to draw parallel edges or merge them. The success criteria count distinct pairs and hold either way.
- **Initial state and emphasis.** Whether groups start collapsed, and how a selected calc's one-hop neighbours are highlighted. 12 of the 17 groups hold one calc, which affects how useful a collapsed overview is.
- **Panel layout.** Proportions, scrolling, tabs versus sections, and how selection animates.
- **Grouping-mode control.** Whether occurrence grouping is a visible toggle in v1 or reachable only from tests, given that it is degenerate on today's model. The overlay test needs a switch reachable without editing code.
- **Libraries.** Renderer, layout engine, expand-collapse extension and version, and whether JS libraries are vendored or loaded from a CDN (a CDN load needs network access; a vendored copy does not).
- **File layout under `src/model_viz/`**, whether it is a Python package, and where the Playwright tests and synthetic snapshot fixtures live.
- **Group labels.** How a full path is shortened for display, and how the design-file groups are distinguished from analysis-module groups.
- **Layout quality.** Whether the 33-calc account-costs group is readable. A parallel spike is measuring this; its findings feed design.

---

## Related Artifacts

- **Concept:** `.project/concepts/model-viz.md`
- **Concept design:** `.project/concepts/model-viz-design.md`
- **Concept design review:** `.project/concepts/model-viz-design-review.md` (§ Focused Re-review)
- **Research:** `.project/research/20260912-004633_calc-dag-visualization.md`
- **Spec review:** `.project/active/model-viz/spec-review.md` (verdict Revise; findings applied in this revision)
- **Follow-on:** `.project/backlog/BACKLOG.md` § Flagged — don't lose, "Structural view migration into `src/model_viz/`"
- **Fixture:** `exploration/stellarator_e2e/stellarator.snapshot.json`
- **Existing viewer (reference, not reused as a data source):** `proof_of_concept/cytoscape_demo.html`, `proof_of_concept/extraction/`
- **Product lens:** `.project/active/model-viz/product-lens.md` (spec_review pass 2026-09-13, gate DISPOSED)
- **Design:** `.project/active/model-viz/design.md`
- **Audit:** `.project/active/model-viz/audit.md` (certified 2026-09-13)

---

**Next Steps:** Focused re-check of the four must-fix criteria (L1-1, L3-1, L3-2, L3-3), then `/_my_design`.
