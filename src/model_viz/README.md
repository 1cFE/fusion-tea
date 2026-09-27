# Model viz: calc graph and structure viewer

A read-only page that shows how a model's calcs feed each other. Each box is a calc; each arrow runs from the calc that produces a value to the calc that consumes it. Selecting a calc opens a panel with its formula, documentation, source location, inputs and outputs.

The same page has a second view of the same snapshot, the structure view. It shows where numbers are filed: every part in its place in the containment tree, and for a selected part its type, its calcs and every attribute it owns.

## Open the viewer

1. Run codegen so a snapshot exists, for example `exploration/stellarator_e2e/stellarator.snapshot.json`.
2. Open `src/model_viz/viewer/index.html` in a browser (double-click it, or `file://` in the address bar).
3. Click **Snapshot** and pick the `.snapshot.json` file.

No server, no command line and no network. The three libraries are vendored under `viewer/vendor/` (versions, sources and SHA-256 in `viewer/vendor/VENDOR.md`). After a new codegen run, pick the file again; the page does not refresh on its own.

## Share a model

To send someone a model, export it to one HTML file:

```bash
uv run python src/model_viz/export.py exploration/stellarator_e2e/stellarator.snapshot.json -o stellarator.html
```

The file holds everything: the stylesheet, the eight viewer scripts, the three vendored libraries and the snapshot itself. It references no other file and no host. The reader double-clicks it and the calc graph draws with the snapshot already loaded; the View select, the panels and the **Snapshot** picker work as in the live page. The stellarator export is about 2 MB.

The page title is the model name (`stellarator`), and the toolbar ends with a note saying which snapshot file it was exported from, on which date, and the first 12 characters of the snapshot's `instance_graph.fingerprint`. The file is a copy: re-export after a new codegen run.

`--viewer v2` exports the structural view instead of the calc graph. Everything else is the same, and the default (`--viewer v1`, or no flag) writes exactly the bytes it always did:

```bash
uv run python src/model_viz/export.py --viewer v2 exploration/stellarator_e2e/stellarator.snapshot.json -o stellarator_v2.html
```

Several snapshots go into one file. Name them all before `-o`:

```bash
uv run python src/model_viz/export.py --viewer v2 a.snapshot.json b.snapshot.json -o two_models.html
```

The toolbar then gains a **Model** select, after the **Snapshot** picker, listing each embedded file by its model name (the file stem without `.snapshot`). The page opens on the first one; choosing another loads it in place, and the title and the export note follow the choice. Every snapshot is checked before anything is written, so one unreadable file in the set means no output file at all.

The exporter refuses, and writes nothing, when the input is not JSON or is not a codegen snapshot (no `format`, `instance_graph` or `instance_graph.fingerprint`). Anything else the viewer checks on load, as it does for a picked file.

## Using it

- Every source-file group starts collapsed. A collapsed box shows its calc count, for example `mfe_lcoe_dcf (1)`. Dashed warm boxes are design files; solid blue boxes are analysis files.
- Click a collapsed box to open it. Click the empty background of an open box to close it. **Expand all**, **Collapse all** and **Fit** are in the toolbar.
- Click a calc to open its panel. The calc and its drawn arrows are highlighted.
- In the panel, calc names are links. Clicking one opens that calc's group if needed, selects it and centres it.
- **Find calc** takes a name: an exact name (any case) goes straight to the calc; otherwise one partial match goes to it, and several show how many matched.
- **Group by → Occurrence** draws calcs inside the occurrences they are scoped to, nested by parent. On the stellarator fixture it starts as one collapsed box, `stellaris (77)`. Occurrences that hold no calc and have none below them are not drawn in this mode (on the fixture, the three parts inside `magnet`); the structure view draws every part.

When groups are collapsed, an arrow between two boxes stands for every binding between calcs inside them. Bindings inside one collapsed box are not drawn. Two boxes that feed each other show two arrows, one each way.

## Switching views

The **View** select in the toolbar switches between **Calc graph** and **Structure**. Both views read the one loaded snapshot; switching never re-reads the file. Each view keeps its own open and closed boxes and its own selection, so switching back returns you to where you were.

The toolbar acts on the active view. **Expand all**, **Collapse all**, **Fit** and the search box work in both. **Group by** applies to the calc graph only and is disabled in the structure view. A switch clears the search box.

Links cross views: a calc name or a calc binding in a part panel opens the calc graph on that calc.

## The structure view

- Every part is a box, and a part's children sit inside it. No calcs and no arrows are drawn. The second line of each label is the number of calcs the part owns directly (`13 calcs`, `1 calc`, `0 calcs`). The root's name line includes its package, for example `stellarator_09::stellaris`.
- On load, the top level is open and every deeper part with children is closed. On the stellarator fixture that shows 19 boxes, with `blanket` and `magnet` closed. **Expand all** shows every part; **Collapse all** leaves only the root.
- A closed part is dashed and its name line counts the parts hidden inside it: `magnet (3 parts)`. This is a different count from the calc graph's Occurrence mode, where a closed `magnet (13)` counts the calcs inside it.
- Click a part to select it and open its panel. Clicking a closed part also opens it. Clicking an open part never closes it, so reading a part never hides anything.
- To close or open a single part, use the **Collapse** or **Expand** button in its panel header. The button shows only on parts with children.
- **Find part** takes a containment path or a part name, any case: an exact path wins, then an exact name, then a partial match of the path. One match opens the parts above it and selects it; several show how many matched.
- Hovering a part shows its containment path.

### The part panel

From top to bottom:

- **Header:** the part's name, its containment path from the root (`stellaris/magnet/coil`), its type, and its calc count.
- **Calcs:** the calcs the part owns directly, in snapshot order, each a link into the calc graph.
- **Attributes:** every attribute scoped to this part and no other, grouped by declaring owner in the order owners first appear. Each row shows the name, the value and the recorded `source_file:source_line`. When an owner is the part's own usage (on the root, `stellarator_09::stellaris`), its heading says "declared on this part".

**The type name is shown when the snapshot leaves no doubt; otherwise it reads "type not recorded", with the reason.** The snapshot does not record a part's type by name. It records the type and all its supertypes as bare ids. When there is exactly one id and the part's attributes come from exactly one declaring owner (not counting the part's own usage), that owner is the type. On the stellarator fixture this names 10 parts. The other 13 list 4 or 5 type ids, and nothing says which is the part's own type.

Each attribute's value is one of five kinds:

- **A recorded number**, shown as recorded.
- **A recorded string**, shown as recorded.
- **Bound to a calc output:** "bound to `<calc>.<output>`", with the calc as a link into the calc graph.
- **Bound to another attribute:** "bound to `<part path>.<attribute>`", as a link that selects that part and scrolls to the row.
- **No value in the snapshot:** a non-alias attribute whose value is null, labelled as such.

A binding whose target is missing from the snapshot is shown as a warning with the raw ids, never as a value. The snapshot carries no computed values, so a bound attribute names where its value comes from rather than a number.

What the structure view does not show: multiplicity (the snapshot does not record it), units (no attribute records one), calc nodes (they live in the calc graph), and a part's bare type ids or occurrence id.

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
- `viewer/js/structure.js` — pure: `structuralTree(model)`, `structureElements` and `structureLayout` (the row-packed preset layout), `typeName`, `partDetail` (every attribute row's value kind), `matchParts`. It uses `view.js`'s `visibleContainers(tree, collapsed)`, the one visibility rule both views share.
- `viewer/js/graph.js` — shell: the Cytoscape instance, stylesheet, layout, tap handling, selection highlight.
- `viewer/js/panel.js` — shell: renders one calc's panel with `textContent` only.
- `viewer/js/part_panel.js` — shell: renders one part's panel with `textContent` only, using `panel.js`'s helpers.
- `viewer/js/app.js` — the one state object, page events, and `window.modelVizApp` for tests and the export loader.
- `viewer2/` — the v2 page: one picture of parts and calcs together, with reach and tracing. It loads v1's `model.js`, `formula.js`, `view.js`, `structure.js`, `panel.js` and `part_panel.js` from `../viewer/js/` rather than copying them.
- `export.py` — stdlib script that writes one self-contained HTML file for one or more snapshots, from either viewer.

The pure files never touch the page or Cytoscape. The design is `.project/active/model-viz/design.md`; the structure view's is `.project/active/model-viz-structural-view/design.md`.

v2 composes v1's `panel.js` and `part_panel.js` DOM rather than re-rendering it, so their `data-*` hooks are a contract between the two viewers: `tests/model_viz_v2/test_panels_v2.py` checks it differentially against v1's own page, and changing a hook breaks v2.

## Tests

```bash
uv sync --extra e2e
uv run playwright install chromium
uv run python -m pytest tests/model_viz
```

The tests drive the real page in headless Chromium through Python Playwright. They compare what the page draws with a Python oracle computed from the raw snapshot (`tests/model_viz/edge_oracle.py` for the calc graph, `tests/model_viz/structure_oracle.py` for parts, attributes and type names). If Playwright or Chromium is missing, every viewer test fails with the two install commands above; none are skipped.

The tests check the fixture's SHA-256 first. The counts they assert (76 calcs, 140 calc pairs, 35 collapsed group pairs and so on) are facts about that exact file. If codegen regenerates `exploration/stellarator_e2e/stellarator.snapshot.json`, the hash check fails: re-probe the new file's facts and update the spec and the tests from the probe, never by editing counts until the tests pass.

Re-probe these premises too, not just the counts:

- No calc output reaches another calc through an attribute. The viewer draws only producer bindings, so a calc output that feeds an attribute (recorded as an alias attribute whose `alias_target` is a producer binding) which another calc reads as a parameter would be a real dependency with no edge. `tests/model_viz/test_graph_edges.py::test_no_calc_output_reaches_a_calc_through_an_attribute` checks that no parameter input targets an alias attribute. If that fails, register a follow-on item rather than changing the edge rule quietly.
- A part's `effective_type_ids` is its own type plus the closure of its supertypes, as codegen builds it today. The type-name rule relies on this: a one-id list is the part's own type. If codegen changes how the list is built, the rule could name a supertype as the type. `tests/model_viz/test_part_panel.py::test_type_names_exact` asserts the fixture's 10 names; re-probe the premise at the next re-pin, not just the names.
