# Design: Model Visualization — Calc DAG Viewer

**Status:** Revised after design review 2026-09-13
**Owner:** Reid W
**Created:** 2026-09-13
**Updated:** 2026-09-13
**Branch:** feat/model-viz
**Commit:** 1b0a5def

---

## Overview

A static HTML page under `src/model_viz/viewer/` that reads a codegen snapshot through a file picker, projects it into a grouped calc graph, and shows a detail panel for the selected calc. The collapse state and the visible-edge rule are computed by pure functions, and the renderer only draws what they return.

## Related Artifacts

- **Spec (the contract):** `.project/active/model-viz/spec.md`
- **Spec review:** `.project/active/model-viz/spec-review.md` (§ Notes for design: L2-2, L2-3, L3-9)
- **Design review:** `.project/active/model-viz/design-review.md` (verdict Revise, approach approved; applied in this revision)
- **Upstream defect:** `exploration/stellarator_e2e/CODEGEN_FINDINGS.md` § Finding 12 (doc comment appended into `calc_expressions`)
- **Spike:** `.project/active/model-viz/spike-layout-findings.md`, code and screenshots in `spike/`
- **Concept and concept design (intent only):** `.project/concepts/model-viz.md`, `.project/concepts/model-viz-design.md`
- **Design brief:** `.project/active/model-viz/briefs/design.md`
- **Fixture:** `exploration/stellarator_e2e/stellarator.snapshot.json` (SHA-256 `c9f6e2a5…ce393`)
- **Reference code, not reused:** `proof_of_concept/cytoscape_demo.html`, `.project/active/model-viz/spike/page_template.html`

## The Point

The stellarator model computes LCOE through 76 calcs wired by 150 producer bindings, and nobody can see that wiring. The only existing viewer shows part containment, which is filing, not computation. The owner asked, `[OWNER-VERBATIM]`: "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation." The owner-grade obligations are `[NEED]`: the data comes from the snapshot read as JSON, the code lives at `src/model_viz/`, selecting a calc shows its formula, documentation and direct I/O, and the I/O is one hop. v1 narrows "actual SysML or python" to codegen's reconstructed formula lines, the doc comment and the recorded source location (`[AGENT]`, orchestrator ruling 1, spec § Non-Goals).

This serves the demo-maturation goals: each goal round asks "which calcs are affected, what feeds them, what do they feed." The viewer answers that by sight, and a wrong answer is worse than none. So the design's first duty is that every edge shown is a real binding and every binding is findable, in every collapse state.

## Research Findings

**Fixture shapes, probed with `uv run python` on 2026-09-13** (details in Appendix A):

- Calcs carry `node_id`, `display_name`, `source_file`, `source_line`, `scope.wire`, `calc_expressions`, `doc_comment`, `expression_ir`, `inputs[]`, `outputs[]`. `display_name` is unique across the 76.
- `scope.wire` equals an `occurrence_id` string exactly. The root occurrence has `parent_id: null` and `display_segment` `stellaris`; its `occurrence_id` is the wire string `[["c1525587-…",null]]`. Containers key on the id, never the segment.
- A parameter input's `edge.target` matches an `attrs[].node_id`. The attr carries `display_name` and `value`.
- `expression_ir` is null on the 65 calcs with formula text and an operator tree on the 11 without. Node kinds: `operator` (`operator`, `operands[]`), `feature_ref` (`reference.source_name`, already dotted for chains, e.g. `magnet.capital_cost`), `literal` (`literal.value`). All 11 have exactly one output.
- **Codegen appends the doc comment into `calc_expressions`,** although its data model documents the list as "preserved as-is" (`../sysml-codegen/src/sysml_codegen/extraction/data_models.py:80`, `extractor.py:175-180`). This is a codegen defect, filed as Finding 12 in `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`. On the fixture the last entry ends with the doc comment on all 65 non-empty lists; it is never byte-identical to it. One calc, `calendar`, has only that entry (see D7).
- `sources.files[]` carries `referent` (matching `source_file`) and `sha256` per file.

**Spike** (`spike-layout-findings.md`): Cytoscape 3.28.1 + dagre 0.8.5 + cytoscape-dagre 2.5.0 load cleanly. LR beats TB. The expand-collapse extension rewrites edge endpoints, draws one edge per binding when collapsed (119 lines, a hairball), and its bundling merges two-way pairs into one `bidirection` edge (31 lines, breaks the spec's two-edges rule). A calc inside a collapsed group is absent from `cy`.

**Rebuild check, run for this design** (`spike/rebuild_check.py` against `spike/dag_spike.html`, Appendix B): replacing all elements with a computed set per collapse state and running dagre works with no console errors. All collapsed: 17 nodes, 35 edges, 44 ms. One large group open: 50 nodes, 103 edges, 88 ms. All expanded: 93 nodes, 140 edges, 256 ms. After a rebuild that opens a target's group, `select` then `zoom` then `center` on the same tick put the target inside the viewport.

**Codebase conventions:**

- Tests live under `tests/` as a namespace tree with no `__init__.py` in subdirectories (`pyproject.toml:51-58`). Helper modules therefore need names unique across the tree.
- `pytest-playwright` is not installed. The spike driver and `scripts/browser_inspect.py` use `playwright.sync_api` directly. Playwright sits in the `e2e` extra (`pyproject.toml:29`).
- Chrome refuses `<script type="module">` from `file://` pages (origin `null` fails the module CORS check). The page must use classic scripts.
- `proof_of_concept/cytoscape_demo.html:357` wires the expand-collapse extension the same way the spike did. Nothing there is reusable beyond styling ideas.
- ADR index (`.project/adr/INDEX.md`): no entry touches visualization. None cited.

## Core Concept

The viewer is a pipeline of plain data transforms with a thin drawing shell at the end.

1. **Read.** The file's text is parsed and version-checked. Anything wrong stops here with a message.
2. **Model.** The snapshot becomes a model: calcs keyed by short ids, every producer binding as its own record (resolved or not), a reverse index from output port to consuming bindings, and each calc's source group and occurrence as two separate fields. The model never changes after load.
3. **View.** Given the model, a grouping mode, and the set of collapsed containers, a pure function returns exactly the nodes and edges that should be on screen. It applies the spec's visible-edge rule directly: each binding maps to the nearest visible thing at each end, same-end bindings vanish, and bindings with the same visible ends merge into one directed edge.
4. **Draw.** The graph shell removes everything from Cytoscape, adds the view's elements, runs dagre, and fits. The panel shell renders one calc from the model.

The key insight is that collapse is just state, and the visible graph is a function of that state. The expand-collapse extension does the same job by mutating live edges, which is why it breaks the two-edges rule and why its edge data cannot be trusted. Once the view function exists, the extension has nothing left to do, so the design drops it. A full rebuild costs under 0.3 s on this graph, and dagre re-lays out on every expand anyway.

This makes every correctness claim checkable at two levels. The view function can be called from `page.evaluate` with any collapse state. The renderer's displayed edges can be read from `cy` and compared against a Python oracle computed straight from the snapshot, which shares no code with the viewer.

## Key Bets

- **B1. A full element rebuild plus dagre layout per collapse change is fast and stable enough for interactive use on graphs of this size.** Measured: 44–256 ms on 76 calcs. *If false → toggling feels sluggish on larger models, and the design must move to incremental add/remove, which re-introduces endpoint bookkeeping.*
- **B2. The `instance-graph/v3` fields probed on the fixture are the ones every v3 snapshot carries.** Appendix C splits them into fields whose absence is a load error and fields whose absence is labelled in the panel. *If false → another model's snapshot either fails to load with a named field, or shows more "not recorded" labels; neither shows wrong data, but the split may need revisiting.*
- **B3. A modeler can orient from 17 collapsed source-file boxes with 35 directed edges, then open one group at a time.** Supported by the spike's bundled screenshot (`spike/out/LR_1c_collapsed_edges_bundled.png`). *If false → the start state is unhelpful and the design needs a different entry view (for example, singletons expanded), not a different architecture.*
- **B4. Dagre's compound overlap in the all-expanded view (spike Q3; seen again in the rebuild check, where the `mfe_plant` and `mfe_account_costs` boxes overlap) is a readability cost, not a correctness one.** *If false → modelers misread which group a calc belongs to, and ELK.js becomes a v1 need rather than a follow-on.*
- **B5. A full re-layout with fit-to-view on every expand or collapse does not disorient a modeler, even though every box moves.** The extension route would have moved boxes the same way. Tested by the manual walk in Validation Approach. *If false → the viewer needs position-preserving layout (dagre seeded from prior positions, or ELK's interactive mode), which changes `graph.render` but not the view function.*

## Key Decisions

- **D1. The view function computes visible elements; the graph shell rebuilds Cytoscape from them. The expand-collapse extension is not used or vendored.** *Rejected: extension with per-direction bundling via `collapseEdges` on each directed pair (three layers of extension state — meta-edges, bundles, `originalEnds` — and the spike never exercised a single-group expand with bundles present). Rejected: extension for nodes only, with edges removed before each extension call and re-added after (it works, but the extension's remaining job is hiding children, which a rebuild does in one line, and two sources of collapse state can drift).* This departs from brief constraint 2's vendor list. The constraint's reason was offline, deterministic delivery of the libraries the viewer uses; it still holds for the three libraries kept. The ruling "the projection's endpoint record is the truth" holds trivially, since no live edge is ever mutated. **D1 supersedes the brief's instruction to vendor `cytoscape-expand-collapse` 4.1.0** (orchestrator ruling 3 on the design review).
- **D2. One drawn edge per directed pair of visible endpoints, carrying the list of bindings it stands for.** With all groups expanded this is one edge per calc pair (140), with a width that grows with the binding count. *Rejected: parallel edges per binding (spike's unbundled view is a hairball, and the two cases would need different rules).* One rule then covers every state: calc pairs, calc-to-group, group-to-group.
- **D3. Classic `<script>` files attaching to one global `ModelViz` namespace, loaded in dependency order.** *Rejected: ES modules (blocked on `file://` in Chrome); one inline HTML file (fails the engineering bar).*
- **D4. Layout LR, dagre `nodeSep 20, rankSep 60, edgeSep 5, padding 20`, `fit: true` after every rebuild.** From the spike. *Rejected: TB (label collisions in the 21-calc cost column).*
- **D5. Every container starts collapsed on load and on a grouping-mode switch.** "Expand all", "Collapse all" and "Fit" buttons sit in the toolbar. Collapsed boxes show the member count, e.g. `mfe_lcoe_dcf (1)`, which softens the 12 singleton boxes (L2-3). *Rejected: remembering collapse state across a mode switch (container ids differ between modes, so there is nothing to carry).*
- **D6. Navigation is instant, not animated.** Expand the target's collapsed ancestors, rebuild, select, set zoom to at least 1.0, centre, all on one tick. *Rejected: `cy.animate` with a `complete` callback (works per spike Q5, but adds an async seam to every navigation test for no correctness gain; can be added later if follow-ups chain on `complete`).*
- **D7. The formula section lists every `calc_expressions` entry verbatim. When the last entry ends with `doc_comment` (and `doc_comment` is non-empty), that entry gets a note, "repeats the documentation below," and stays in the list.** The doc comment itself renders once in its own section. When every entry is such a repeat and there is no `expression_ir`, the section also says "no formula lines recorded for this calc" above the list (the `calendar` case; codegen drops expressions it cannot reconstruct, `extractor.py:147-155`). **This note is a compensation for codegen Finding 12**, not a contract: the test depends only on the spec's `[HARD]` fact that the final entry contains the doc comment, not on codegen's prefix wording. When the upstream fix lands, the note never fires and nothing else changes. *Rejected: matching codegen's two prefixes `"\nDocumentation:\n"` and `"See documentation:\n"` (couples the viewer to private wording; a changed word silently removes the note). Rejected: hiding the repeat (loses an entry the spec says must appear).*
- **D8. Group labels are the file's base name without `.sysml`.** When two groups share a base name, both labels gain their parent directory (`generic_mfe/mfe_plant`). Design-file groups (path contains a `designs/` segment) get a dashed border and a warm fill; analysis groups keep the solid blue style. The full path shows in the node tooltip and as the panel's group line. *Rejected: labelling by full path (unreadable in boxes).*
- **D9. Page layout: a toolbar across the top, the graph pane on the left filling the remaining width, a detail panel on the right at 420 px, scrolling on its own.** The panel uses stacked sections (header, Location, Formula, Documentation, Inputs, Outputs), not tabs, so everything for a calc is one scroll away. The Cytoscape container is the graph pane only, so "inside the viewport" means inside that pane. The panel is always laid out, showing a "select a calc" placeholder until a selection, so the pane never changes width after Cytoscape measures it. `graph.js` calls `cy.resize()` on window resize.
- **D10. Clicking a collapsed container expands it; clicking the background of an expanded container collapses it; clicking a calc selects it and shows its panel.** The selected calc's visible edges and their other ends get a highlight class. *Rejected: double-click toggling (less discoverable; kept as the fallback if accidental collapses show up in use).*
- **D11. Source location shows `source_file:source_line` plus the first 12 hex digits of the file's SHA-256 from `sources.files`, with the full hash in a tooltip.** This lets a modeler tell which on-disk tree matches (spec open question). If the referent has no entry, the hash line says so.
- **D12. `src/model_viz/` is not a Python package in this item.** It holds the static viewer and a short README. The structural-view migration adds Python later and can make it a package then (answers L3-9).
- **D13. The page exposes `window.modelVizApp`, a read-mostly handle with `cy`, `model`, the current view state, and the same functions the UI events call (`toggleContainer`, `expandAll`, `collapseAll`, `showCalc`, `navigateTo`).** Tests drive bulk sequences through it and click real UI for the wiring. *Rejected: tests clicking canvas coordinates for all 34 round-trip toggles (slow and brittle; real canvas clicks prove the three gestures once each, see Validation Approach).* The pure functions live under the separate `window.ModelViz` namespace (D3); the two names differ by more than case on purpose.

## Architecture

```
file input ──text──▶ readSnapshot ──snap──▶ buildModel ──Model──┐
                        │ error                                  │
                        ▼                                        ▼
                  error banner          app state {model, mode, collapsed:Set, selected}
                                                 │
                         ┌───────────────────────┼──────────────────────┐
                         ▼                       ▼                      ▼
             containerTree(model,mode)    renderPanel(model,key)   search box
                         ▼
          visibleElements(model,tree,collapsed) ──▶ graph.render(elements) ──▶ Cytoscape + dagre
```

- **Pure layer** (`model.js`, `formula.js`, `view.js`): no DOM, no Cytoscape. Inputs and outputs are plain objects. Callable from `page.evaluate`.
- **Shells** (`graph.js`, `panel.js`): the only code that touches Cytoscape or the DOM. They read the model and the view output; they hold no state of their own beyond the Cytoscape instance.
- **App** (`app.js`): owns the one mutable state object, wires events to state changes, and re-runs view then draw after each change.

### Model shape

```
Model   = { calcs: Calc[], byKey: Map<key,Calc>, keyByNodeId: Map<node_id,key>,
            bindings: Binding[], consumersOf: Map<"key|outputId", bindingId[]>,
            groups: Map<gid,Group>, occurrences: Map<occurrence_id,Occ>, attrs: Map<node_id,Attr>,
            fileHashes: Map<referent,sha256> }
Calc    = { key:"c12", nodeId, name, sourceGroup:gid, occurrenceId|null, sourceFile|null, sourceLine|null,
            formulas:string[], derivedFormula:string|null, doc|null, inputs:Input[], outputs:Output[] }
Input   = { name, kind:"producer"|"parameter"|"literal"|"default", bindingId?, attrNodeId?, value?, unit? }
Binding = { id:"b7", consumer:key, inputName, producerNodeId, producer:key|null, outputId, resolved:bool }
Group   = { gid, path|null, label, kind:"analysis"|"design"|"ungrouped" }
```

Keys `c0…` follow snapshot order; binding ids follow input order. Short keys keep Cytoscape selectors free of the quotes inside `node_id` strings (spike step 3). `node_id` is used raw as the lookup key (spike ruling; no re-encoding).

### Cytoscape element data

- **Calc node:** `{id: key, kind: "calc", label, node_id, source_group, occurrence_id, parent: containerId}`. Both grouping fields ride on every calc node in every mode; only `parent` depends on the mode.
- **Container node:** `{id, kind: "container", mode, label, container_kind, member_count, collapsed, group_path | occurrence_id, parent?}`. Ids are `g0…` for source groups and `o0…` for occurrences, plus `g-ungrouped` and `o-unscoped`.
- **Edge:** `{id: "e:" + source + ">" + target, source, target, bindings: [bindingId…]}`.

### Containers per grouping mode

`containerTree(model, mode)` returns containers with parent links and each calc's direct container.

- **Source mode:** one flat container per distinct full `source_file`. A calc with no `source_file` goes to `g-ungrouped`.
- **Occurrence mode:** one container per occurrence that holds a calc or is an ancestor of one, keyed by `occurrence_id`, nested by `parent_id`, labelled by `display_segment`. Siblings with the same segment stay separate because the key is the id. A calc whose `scope.wire` matches no occurrence goes to `o-unscoped`.

### The visible-edge rule, as the view function applies it

For a collapse state `collapsed` (a set of container ids):

1. A container is visible when none of its ancestors is collapsed. A calc is visible when none of its containers is collapsed.
2. The representative of a calc is the outermost collapsed container on its ancestor chain, or the calc itself if there is none. This is the spec's "nearest visible ancestor."
3. For each resolved binding: `s = rep(producer)`, `t = rep(consumer)`. If `s === t`, skip it (no self-loop). Otherwise add the binding id to the edge keyed `s>t`.
4. Visible containers become compound parents when expanded and plain boxes when collapsed. Visible calcs keep their container as `parent`.

A two-way pair produces keys `A>B` and `B>A`, so it draws as two directed edges. The stylesheet fixes `curve-style: bezier` with `target-arrow-shape: triangle`: bezier offsets opposite edges so both curves and arrowheads show, while Cytoscape's default `haystack` draws no arrowheads. On the fixture this yields 35 edges all collapsed and 140 all expanded (rebuild check). Unresolved bindings never reach step 3.

### Reverse index and unresolved producers

- `consumersOf` maps `producerKey|outputId` to binding ids. It is built in the same pass as the bindings, from the same records, so forward and reverse cannot disagree unless the snapshot does.
- **Unresolved producer** (target `node_id` not among the calcs): the binding stays in `bindings` with `producer: null, resolved: false`, keeps the raw `producerNodeId` and `outputId`, and is excluded from edges and from `consumersOf`. The consumer's panel shows it in the Inputs section with a warning and the raw target.
- **Resolved calc, undeclared output id** (0 on the fixture): the edge is drawn, since the calc dependency is real. The consumer's panel marks the port as undeclared, and the producer's Outputs section lists it under an "undeclared output" row so the binding is still findable from both ends.

### Formula printer

`printExpression(ir)` returns a string or `null`. `operator` with `+` or `*` joins its printed operands with ` + ` or ` * `; a `+` operand inside `*` gets parentheses. `feature_ref` prints `reference.source_name`. `literal` prints `String(literal.value)`, so `9400.0` prints as `9400`. Any other kind or operator, an operator with fewer than two operands, a null or non-numeric literal value, an empty `source_name`, or any missing field returns `null` for the whole tree. The panel shows `<output name> = <expr>` when the calc has one output, and the bare expression otherwise. Both outcomes carry the spec's label, "derived from expression structure; the snapshot has no formula text for this calc."; `null` shows "No formula available" under the same label.

### Navigation contract

`navigateTo(key)` is what panel links and the search box call.

1. Look up the target's container chain in the current `containerTree`, never in `cy` (a hidden calc is absent from `cy`).
2. Remove every collapsed container on that chain from `collapsed`. If any was removed, rebuild and lay out (synchronous, `fit: true`).
3. Set `selected = key`, select the node in `cy`, apply the highlight, render the panel.
4. Set zoom to `max(cy.zoom(), 1.0)`, then `cy.center(node)`. Same tick; no animation (D6).

The click is never ignored: a key not in the model shows a panel-level warning instead. After any other rebuild (toggle, expand all), the selected calc is re-selected if visible; the panel keeps showing it either way.

## Required Invariants

- **I1.** The model is built once per load and never mutated. Nothing reads endpoint data back from live Cytoscape edges to answer a question about bindings.
- **I2.** Every drawn edge's `bindings` list is non-empty, and every listed binding's representatives equal the edge's `source` and `target`.
- **I3.** Every resolved binding whose two representatives differ is listed on exactly one drawn edge. Bindings with equal representatives are on none.
- **I4.** Only producer inputs become bindings. Parameter, literal and default inputs appear only in the panel.
- **I5.** Every calc node carries both `source_group` and `occurrence_id` regardless of mode.
- **I6.** A load attempt clears the previous model, graph, panel, selection and collapse state before validating, so a failed second load shows no remnant of the first.
- **I7.** Every `calc_expressions` entry is rendered with its exact text as the element's `textContent`, in snapshot order.
- **I8.** The pure layer never touches `document`, `window` state, or `cy`.

## Component Overview

```
src/model_viz/
  README.md                  how to open the viewer; what it reads
  viewer/
    index.html               page shell: toolbar, graph pane, panel, script tags in order
    viewer.css               layout (D9), panel sections, warning and label styles
    js/model.js              readSnapshot(text), buildModel(snap)          — pure
    js/formula.js            printExpression(ir), endsWithDoc(entry, doc)   — pure
    js/view.js               containerTree(model, mode), visibleElements(model, tree, collapsed) — pure
    js/graph.js              Cytoscape instance, stylesheet, render(elements), selection highlight, event hooks
    js/panel.js              renderPanel(model, key) into the panel element; link clicks call back
    js/app.js                state, file input, mode select, search, toolbar buttons, window.modelVizApp
    vendor/
      cytoscape-3.28.1.min.js, dagre-0.8.5.min.js, cytoscape-dagre-2.5.0.js
      VENDOR.md              version, source URL, licence (all MIT), SHA-256 of each file
tests/model_viz/
  conftest.py                session browser, per-test page on file:// index.html, console/pageerror capture, load helper
  viewer_snapshots.py        synthetic snapshot builders from the real fixture, written to tmp_path
  edge_oracle.py             Python oracle: bindings, groups, expected visible edge list for a collapse state given as group paths
  test_loading.py  test_graph_edges.py  test_panel.py  test_navigation.py  test_guards.py  test_pure_layer.py
```

**Panel DOM hooks for tests.** Sections carry `data-section` (`location`, `formula`, `doc`, `inputs`, `outputs`). Formula entries are `li[data-formula-index]`; a repeat entry adds `data-doc-repeat`. The Documentation section carries `data-doc-absent` when there is no doc comment. Input rows carry `data-input-kind` and `data-input-name`; producer rows add `data-producer-node-id` and `data-output-id`, unresolved rows add `data-unresolved`. Output rows carry `data-output-id`, consumer links carry `data-consumer-node-id` and `data-input-name`, and an output with none carries `data-no-consumer`. Calc links carry `data-calc-key`. The body carries `data-load-state` (`empty|ready|error`) and an incrementing `data-load-seq`.

## Non-Goals

- Verbatim SysML source text and any Python view (spec § Non-Goals, ruling 1).
- The structural view and its migration (registered follow-on).
- Multi-hop tracing, export, attribute and constraint nodes, editing, auto-refresh.
- Edge routing around group boxes and fixing dagre compound overlap (B4; ELK.js is the recorded upgrade path).
- Search beyond calc-name matching.
- Dependencies routed through an attribute (a calc output feeding an attribute that another calc reads) are not drawn; only producer bindings are edges (I4). None exist on the fixture: all 234 parameter targets hold static values (spec review, lens finding design_review-F1). A model that introduces one needs a follow-on item, not a silent change here.

## Implementation Notes

- **Script order in `index.html`:** vendor (cytoscape, dagre, cytoscape-dagre), then `model.js`, `formula.js`, `view.js`, `graph.js`, `panel.js`, `app.js`. Each file starts `window.ModelViz = window.ModelViz || {}` and attaches one sub-object.
- **Render verbatim text with `textContent` and `white-space: pre-wrap`,** never `innerHTML`. Doc comments contain `*`, `<` and newlines.
- **`graph.render` wraps remove-and-add in `cy.batch`,** then runs the layout outside the batch (rebuild check pattern, Appendix B).
- **Cytoscape tap events bubble from a child calc to its compound parent.** The container toggle handler must act only when `evt.target` is the container itself, or every calc click would also collapse its group.
- **Search box:** `<input list>` with a `<datalist>` of calc names. On Enter or `change`: exact case-insensitive match first, else substring matches; exactly one match navigates, zero shows "no calc matches", several shows the count and leaves the list open.
- **Mode select** (`Source file` / `Occurrence`): on change, rebuild the tree, collapse all (D5), keep the selection and panel.
- **Absent doc comment:** the Documentation section shows "No documentation in the snapshot for this calc." in the warning-label style. It renders for the 11 formula-less calcs on the fixture.
- **Missing fields:** follow Appendix C. A load-error field names itself in the error banner; a labelled field shows a "not recorded" label where the value would be. Nothing is filled in with a guessed value.
- **File input:** set `input.value = ""` after each read, so re-picking the same file after a codegen run fires `change` again.
- **Parameter input display:** attr `display_name` and `value`; a null value is labelled "no value in snapshot"; an attr missing from `graph.attrs` is labelled "attribute not in snapshot". Show `metadata.unit` when present.
- **Load errors:** non-JSON ("not a JSON file"), no `instance_graph.schema_version` ("not a codegen snapshot"), wrong version (names expected `instance-graph/v3` and the found value), and v3 without a `graph.calcs` array ("v3 snapshot without a calcs list").
- **Test helper module names** must be unique across `tests/` (namespace tree, default import mode). Hence `viewer_snapshots.py` and `edge_oracle.py`, not `fixtures.py`.
- **Vendoring:** download the three files from unpkg at the spike's exact versions; record URL, licence and SHA-256 in `VENDOR.md`. The page must make no network request; a test asserts it (below).

## Potential Risks

- **Canvas click on an expanded container's background collapses it by accident** when a modeler misses a calc. Mitigation: D10 fallback to double-click; the wiring is one line in `graph.js`.
- **The 3-minute spike wall time recurs in tests.** It was attributed to unpkg loading and screenshots, which vendoring and no screenshots remove. Mitigation: one browser per session; the page fixture reloads rather than relaunching.
- **Playwright or Chromium is missing on a machine.** Playwright stays in the `e2e` extra (orchestrator ruling 2), so a plain `uv sync` removes it. `conftest.py` fails loudly, never skips, with the exact commands `uv sync --extra e2e` and `uv run playwright install chromium`; `src/model_viz/README.md` gives the same two commands. A green run always means the viewer was exercised.
- **Another model's snapshot lacks a field the fixture always had** (B2). Mitigation: Appendix C decides per field; an input with an edge kind outside the four known kinds shows as an "unknown input kind" row and is not drawn.

## Integration Strategy

The viewer is new and stands alone. It reads only the snapshot codegen already writes, so it adds nothing to codegen or the modeling PM. A modeler opens `src/model_viz/viewer/index.html` in a browser after a codegen run. The tests join the default `uv run python -m pytest` run through `testpaths = ["tests"]`. The structural-view follow-on will add a second view beside this one and can reuse `graph.js` and the panel pattern.

## Validation Approach

Every edge assertion reads `cy.edges()` through `window.modelVizApp.cy` and maps each endpoint to an identity: a calc node's `node_id`, or `group:<path>` / `occ:<occurrence_id>` for a container. The expected edges come from `edge_oracle.py`, which computes representatives and pairs from the raw snapshot JSON in Python. No test compares the page with the page's own projection.

**Edge comparison rules (no pass by construction):**

- **Lists, not sets.** The page's edges become a sorted list of `(source identity, target identity)` tuples, one per drawn edge. The oracle returns the sorted list of distinct directed pairs. The test asserts the two lists are equal, so a duplicated edge fails on length and a reversed edge fails on order. It also asserts drawn edge ids are unique.
- **The oracle's collapse state comes from the test.** Each round-trip and interleaved test keeps its own `collapsed_paths` set, updated from its scripted step list ("collapse `root-0/analyses/mfe_account_costs.sysml`"), and passes it to the oracle. Mapping a group path to a container id for the `toggleContainer` call may read `cy`; the oracle's state never does. A toggle that hits the wrong group therefore fails.
- **Literal fixture anchors stay beside oracle equality:** 35 edges all collapsed with the four named two-way pairs present in both directions, 140 all expanded, no self-loops. They guard against the oracle and the viewer sharing one misreading of the rule.

| File | Spec criteria covered | How |
|---|---|---|
| `test_loading.py` | All five Loading criteria | `set_input_files` with the fixture, a wrong-version copy, a no-version JSON, PDF-like bytes, then two loads in sequence (fixture, then the renamed copy), and a good load followed by a bad one; asserts `data-load-state`, error text, zero nodes, no page errors, no first-snapshot name left in `cy` or panel. Also asserts the page makes no `http(s)` request. |
| `test_graph_edges.py` | 76 nodes, 17 groups (sizes, design-file kinds), 140 pairs, non-producer kinds make no edge, all-collapsed 35 with the four two-way pairs and no self-loops, round trip for every group, interleaved sequence | Expand all and collapse all via toolbar clicks. The 34 per-group toggles and the interleaved steps use `modelVizApp.toggleContainer`; after each step the displayed edge list equals the oracle's list for the test's own collapse state, and the final list equals the start. |
| `test_panel.py` | Panel sections, 65 formula lists verbatim and ordered with doc shown, 11 derived formulas with label and doc-absence label, input kinds and totals (150/234/10/52), `fuel_handling` and `fuel` examples, bindings both directions, 64 unconsumed outputs | Calls `modelVizApp.showCalc` for each of the 76 and reads DOM hooks; compares against the snapshot in Python. Binding rows are matched as multisets keyed by `(consumer, input name, producer, output)`: on the fixture one output feeds one consumer through two inputs, and a set match would pass with a row missing. Also asserts the `calendar` note and the doc-absent label. |
| `test_navigation.py` | Navigation, hidden-target (one upstream link, one downstream link) | Real clicks on panel links; asserts selection, panel name, group expanded, rendered bounding box inside the graph pane. Also the search box: typing `cas22_capital` from all collapsed reaches the same end state. **Canvas gestures** (spec: "Clicking a calc node opens a panel"), each a Playwright `page.mouse.click` at a point from `renderedBoundingBox` plus the graph pane's page offset: (1) click a collapsed container's centre → it expands; (2) click a calc node's centre inside it → the panel shows that calc, the node is selected, and its container is still expanded with the calc present in `cy` (catches the tap-bubbling bug); (3) click inside the expanded container at a point no child's bounding box contains (the test checks this before clicking) → it collapses. |
| `test_guards.py` | Unresolvable producer, overlay readiness | Removed-calc copy: every consumer panel shows the unresolved row, no edge endpoint is missing from `cy`, 75 calcs render. Overlay copy: choose `Occurrence` with `select_option`, click Expand all, walk each calc's `parent` chain in `cy` and compare with the synthetic assignment; two same-segment siblings are distinct containers; one source file's calcs land in two containers. |
| `test_pure_layer.py` | Supports the unrenderable-tree criterion and the rule's edge cases | `page.evaluate` on `ModelViz.formula.printExpression` (precedence, chains, unsupported operator, single operand and null literal → null) and `endsWithDoc`, and `ModelViz.view.visibleElements` on a small hand-built model (nested collapse, self-loop drop, two-way pair). The UI-level unrenderable-tree check lives in `test_panel.py` with the synthetic copy. |

**Synthetic snapshots** (`viewer_snapshots.py`), each a deep copy of the fixture written to `tmp_path`: wrong version; version removed; non-JSON bytes; renamed (every `display_name` prefixed, for the replace-on-reload check); one calc removed, chosen as the calc with the most consumers; one of the 11 trees with an operator changed to `/`; overlay, which adds a parent occurrence with two children sharing a `display_segment` and re-scopes calcs so one source file spans both.

**Manual check:** open the page on the fixture, walk collapsed → `mfe_account_costs` expanded → a cost calc → an upstream link, and compare against `spike/out/LR_2_account_costs_expanded.png` for layout sanity.

## Next-Stage Handoff

- **Fixed:** D1 (rebuild, no extension), D2 (one edge per directed visible pair), D3 (classic scripts), the model and element data shapes, the navigation contract, the DOM hooks, the oracle-based edge testing.
- **Open for the plan:** exact colours and edge-width scale; whether `test_panel.py` shares one loaded page across its tests; panel wording beyond the spec-mandated labels.
- **De-risk first:** vendor the three libraries and get `index.html` loading the fixture with the pure layer under `test_pure_layer.py` and `test_graph_edges.py`'s all-collapsed and all-expanded counts. That proves the file-picker, classic-script and oracle seams before the panel is built.
- **ADR candidate after approval:** "The viewer derives visible graph elements from collapse state; no library mutates edges." It passes the density bar if the structural-view follow-on would otherwise reach for the expand-collapse extension again.

---

## Appendix A — Fixture probes (2026-09-13)

- `expression_ir` operator node: `{kind: "operator", operator: "+", operands: [..2], operand_type, schema_version: "expression-ir/v1"}`. Across the 11 trees: 35 `+`, 4 `*`, 47 `feature_ref`, 3 `literal`.
- `feature_ref`: `reference.source_name` (`"magnet.capital_cost"` when `chain_segments` is `["magnet", "capital_cost"]`), `reference.target.{kind, name, qualified_name}`.
- `literal`: `literal: {kind: "LiteralRational", result_type, value: 0.5}`.
- Doc repeat among the 65 non-empty lists: last entry ends with `doc_comment` 65, byte-identical 0. Codegen's current prefixes are `"\nDocumentation:\n"` (64) and `"See documentation:\n"` (1, `calendar`); the viewer does not rely on them (D7).
- Output: `{name, declaration, metadata, port: {calculation, output}}`. Multi-output calcs exist (`sustain` 17, `primary_loop` 13).
- Occurrence: `{occurrence_id, parent_id, display_segment, containment_slot, …}`; 14 occurrences, all segments distinct; the root has `parent_id: null` and `display_segment` `stellaris`.
- Attr: `{node_id, display_name, value, value_site, source_file, source_line, …}`; 292 attrs.
- Source groups: `root-0/analyses/mfe_account_costs.sysml` 33, `root-0/designs/generic_mfe/mfe_plant.sysml` 10, `mfe_plasma_scaling` 8, `mfe_magnet_field` 7, `mfe_magnet_cost` 5, `mfe_power_balance` 2, eleven more with 1 (including `root-0/designs/stellarator_09/stellarator_plant.sysml`).

## Appendix B — Rebuild check (2026-09-13)

Script `spike/rebuild_check.py` (run from the repo root; needs unpkg) loaded `spike/dag_spike.html` (unpkg libraries, fixture inlined), then per state did `cy.batch(remove all; add computed elements)` followed by dagre LR with the D4 options. Console and page errors: none.

| State | Nodes | Edges | Rebuild + layout (ms) |
|---|---|---|---|
| All collapsed | 17 | 35 | 44 |
| `mfe_account_costs` expanded | 50 | 103 | 88 |
| All expanded | 93 | 140 | 256 |
| `mfe_account_costs` and `mfe_plant` expanded | 60 | 120 | 126 |

Navigation: target `c65` absent from `cy` before its group opened; after the rebuild, `select`, `zoom(1.5)`, `center` gave a rendered bounding box of x 711–889, y 478–522 in a 1600×1000 pane, and the selection was `["c65"]`.


## Appendix C — Missing-field policy

A field is a load error when the viewer cannot place the calc or its bindings without it. It is labelled when the calc can still be shown truthfully without it. No field is ever filled with a guessed value.

| Field | Absent or wrong type | Shown as |
|---|---|---|
| `instance_graph.schema_version` | Load error | "not a codegen snapshot" |
| `graph.calcs` (array) | Load error | "v3 snapshot without a calcs list" |
| calc `node_id` (string), `display_name` (string), `inputs` (array), `outputs` (array) | Load error | names the field and the calc's index |
| input `name`; producer edge `target.calculation`, `target.output` | Load error | names the field, calc and input index |
| output `name`, `port.output` | Load error | names the field, calc and output index |
| `graph.occurrences`, `graph.attrs` | Absent: treated as empty. Present but not an array: load error | Occurrence mode puts calcs in `o-unscoped`; parameter rows say "attribute not in snapshot" |
| `doc_comment` | Labelled | "No documentation in the snapshot for this calc." |
| `calc_expressions` | Labelled (treated as empty list) | derived-formula path, with the spec's label |
| `expression_ir` | Labelled | "No formula available" with the same label |
| `source_file` / `source_line` | Labelled | calc goes to `g-ungrouped`; location says "not recorded" |
| `scope.wire` | Labelled | calc goes to `o-unscoped` |
| attr `value`, input `metadata.default_value` | Labelled | "no value in snapshot", "no default recorded" |
| `sources.files` entry for the referent | Labelled | hash line says "no file hash recorded" |
| input `edge.kind` outside the four known kinds | Labelled | "unknown input kind: <kind>" row; no edge |

---

**Next Step:** focused re-check of DR-M1 to DR-M3, then `/_my_plan`.
