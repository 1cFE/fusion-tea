# Model viz: calc graph viewer

A read-only page that shows how a model's calcs feed each other. Each box is a calc; each arrow runs from the calc that produces a value to the calc that consumes it. Selecting a calc opens a panel with its formula, documentation, source location, inputs and outputs.

## Open the viewer

1. Run codegen so a snapshot exists, for example `exploration/stellarator_e2e/stellarator.snapshot.json`.
2. Open `src/model_viz/viewer/index.html` in a browser (double-click it, or `file://` in the address bar).
3. Click **Snapshot** and pick the `.snapshot.json` file.

No server, no command line and no network. The three libraries are vendored under `viewer/vendor/` (versions, sources and SHA-256 in `viewer/vendor/VENDOR.md`). After a new codegen run, pick the file again; the page does not refresh on its own.

## Using it

- Every source-file group starts collapsed. A collapsed box shows its calc count, for example `mfe_lcoe_dcf (1)`. Dashed warm boxes are design files; solid blue boxes are analysis files.
- Click a collapsed box to open it. Click the empty background of an open box to close it. **Expand all**, **Collapse all** and **Fit** are in the toolbar.
- Click a calc to open its panel. The calc and its drawn arrows are highlighted.
- In the panel, calc names are links. Clicking one opens that calc's group if needed, selects it and centres it.
- **Find calc** takes a name: an exact name (any case) goes straight to the calc; otherwise one partial match goes to it, and several show how many matched.
- **Group by → Occurrence** draws calcs inside the occurrences they are scoped to, nested by parent. On today's stellarator model every calc sits on the root occurrence, so this shows one box.

When groups are collapsed, an arrow between two boxes stands for every binding between calcs inside them. Bindings inside one collapsed box are not drawn. Two boxes that feed each other show two arrows, one each way.

## What it reads

Only an `instance-graph/v3` codegen snapshot. Any other version, a JSON file that is not a snapshot, or a non-JSON file shows an error banner and draws nothing. A snapshot missing a field the viewer needs to place a calc (for example a calc `node_id`) is refused with the field named; fields the panel can do without are shown as "not recorded" labels, never guessed.

What it shows:

- Calcs, and producer bindings as arrows. Parameter, literal and defaulted inputs appear only in the panel.
- The formula lines codegen reconstructed (`calc_expressions`), verbatim and in order. When a calc has none, a formula printed from its `expression_ir`, labelled as derived.
- The doc comment, the recorded `source_file:source_line`, and the start of that file's SHA-256 from the snapshot.
- A producer input whose calc is not in the snapshot, marked unresolved in the consumer's panel. No arrow is drawn for it.

What it does not show: verbatim SysML source, any Python, attribute or constraint nodes, or paths longer than one hop. See `.project/active/model-viz/spec.md` § Non-Goals.

## Files

- `viewer/index.html` — page shell: toolbar, graph pane, panel, script tags in load order.
- `viewer/viewer.css` — layout and panel styles.
- `viewer/js/model.js` — pure: `readSnapshot(text)` checks the file; `buildModel(snap)` builds calcs, bindings and the consumer index.
- `viewer/js/formula.js` — pure: `printExpression(ir)` and `endsWithDoc(entry, doc)`.
- `viewer/js/view.js` — pure: `containerTree(model, mode)` and `visibleElements(model, tree, collapsed)`, which applies the visible-edge rule.
- `viewer/js/graph.js` — shell: the Cytoscape instance, stylesheet, layout, tap handling, selection highlight.
- `viewer/js/panel.js` — shell: renders one calc's panel with `textContent` only.
- `viewer/js/app.js` — the one state object, page events, and `window.modelVizApp` for tests.

The pure files never touch the page or Cytoscape. The design is `.project/active/model-viz/design.md`.

## Tests

```bash
uv sync --extra e2e
uv run playwright install chromium
uv run python -m pytest tests/model_viz
```

The tests drive the real page in headless Chromium through Python Playwright. They compare what the page draws with a Python oracle computed from the raw snapshot (`tests/model_viz/edge_oracle.py`). If Playwright or Chromium is missing, every viewer test fails with the two install commands above; none are skipped.

The tests check the fixture's SHA-256 first. The counts they assert (76 calcs, 140 calc pairs, 35 collapsed group pairs and so on) are facts about that exact file. If codegen regenerates `exploration/stellarator_e2e/stellarator.snapshot.json`, the hash check fails: re-probe the new file's facts and update the spec and the tests from the probe, never by editing counts until the tests pass.

Re-probe these premises too, not just the counts:

- No calc output reaches another calc through an attribute. The viewer draws only producer bindings, so a calc output that feeds an attribute (recorded as an alias attribute whose `alias_target` is a producer binding) which another calc reads as a parameter would be a real dependency with no edge. `tests/model_viz/test_graph_edges.py::test_no_calc_output_reaches_a_calc_through_an_attribute` checks that no parameter input targets an alias attribute. If that fails, register a follow-on item rather than changing the edge rule quietly.
