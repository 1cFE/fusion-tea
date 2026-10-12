# Implementation Plan: Model Visualization — Calc DAG Viewer

**Status:** Complete (implementation; audit next)
**Created:** 2026-09-13
**Last Updated:** 2026-09-13
**Branch:** feat/model-viz

## Source Documents

- **Spec (acceptance contract):** `.project/active/model-viz/spec.md`
- **Design (technical contract):** `.project/active/model-viz/design.md` ← component details, data shapes, the visible-edge rule, navigation contract, DOM hooks, missing-field policy (Appendix C)
- **Design review:** `.project/active/model-viz/design-review.md` (Revise, approach approved; revision applied in `design.md`, commit 1a550d42)
- **Briefs (provenance):** `briefs/spec.md`, `briefs/spec_review.md`, `briefs/spec_revise.md`, `briefs/design.md`, `briefs/design_review.md`, `briefs/design_revise.md`, `briefs/plan.md`
- **Spike (crib patterns, not files):** `spike/page_template.html` (projection + Cytoscape setup), `spike/rebuild_check.py` (batch rebuild + dagre + select/zoom/centre), `spike/run_spike.py` (Playwright driver with console and page-error capture)
- **Fixture:** `exploration/stellarator_e2e/stellarator.snapshot.json`, SHA-256 `c9f6e2a52ea69cf95dcee015496f906f705d1130bce1a529bde510299a5ce393`

## The Point

The stellarator model computes LCOE through 76 calcs wired by 150 producer bindings, and nobody can see that wiring. The only existing viewer (`proof_of_concept/extraction/`) draws part containment, which is filing, not computation. To learn what one calc does, a modeler reads SysML across about 16 files by hand. The owner asked, `[OWNER-VERBATIM]`: "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation."

The owner-grade obligations (`[NEED]`) this plan must deliver:

- The data comes from the codegen snapshot read as JSON. No syside, no codegen Python, no re-derived bindings.
- The code lives at `src/model_viz/`.
- Selecting a calc shows its formula, its documentation and its direct I/O.
- The I/O is one hop: what feeds each input and which calcs consume each output.

v1 narrows "actual SysML or python" to codegen's reconstructed formula lines, the doc comment and the recorded source location (`[AGENT]`, orchestrator ruling 1, spec § Non-Goals).

Why it matters: goal rounds keep asking "which calcs are affected, what feeds them, what do they feed." The viewer answers that by sight, and a wrong picture is worse than none. So the first duty, and the thing the tests guard hardest, is that every drawn edge is a real binding and every binding is findable, in every collapse state.

## Implementation Strategy

**Phasing rationale.** The design's architecture is a pure pipeline (read → model → view) with thin drawing shells. The risky seams are all in the first slice: classic scripts on `file://`, the file picker driven by Playwright, vendored libraries with no network, and the independent Python edge oracle agreeing with the view function on the rendered graph. Phase 1 proves those seams and the edge rule in every collapse state before any panel code exists. The panel (Phase 2) then builds on a proven model. Interaction (Phase 3) needs the panel's links. Guards and error loads (Phase 4) need synthetic snapshot builders and the mode switch, which nothing earlier depends on. Phase 5 is docs, the manual walk and the regression diff.

**Deviation from the brief's order, recorded.** The brief puts "all-collapsed/all-expanded edge counts" in the first phase and does not name the round-trip tests. This plan puts the per-group round trip and the interleaved sequence in Phase 1 too, as its second half. They use the same oracle and the same `toggleContainer` call, they test the design's first duty, and a bug there would change `view.js`, which every later phase reads. A checkpoint splits Phase 1 so a session can stop after the counts.

**Critical path.** Baseline capture → vendor libraries → pure layer + page shell + graph shell → conftest + oracle → counts green → round trips green → panel → navigation → guards → docs, manual walk, suite diff.

**First proof point.** `test_graph_edges.py::test_all_collapsed_edges` and `::test_all_expanded_edges` pass: the page loads the fixture through the real file input on `file://`, makes no network request, and the edges read from `window.modelVizApp.cy` equal the Python oracle's list (35 and 140). If that passes, the architecture is proven end to end.

**Overall validation approach.**

- Each phase writes its tests first, runs them to see them fail for the right reason (missing element or function, not an import error in the harness), then writes code until green.
- Each phase's gate is `uv run python -m pytest tests/model_viz -q` all green, plus the phase's manual check.
- The full suite runs twice only: once before Phase 1 (baseline) and once in Phase 5 (diff). The gate is "no new failures," not "all green," because `tests/` has long-standing unrelated failures.

## Decisions Made in This Plan

The design left three things open for the plan (§ Next-Stage Handoff), and planning surfaced four more. No owner was present; these are agent-grade and recorded here.

- **PD1. Colours and edge width.** Analysis group: solid border `#4a78b5`, fill `#eaf1fb`. Design group (D8): dashed border `#b5793a`, fill `#fbf1e6`. Ungrouped / unscoped container: dotted border `#888`, fill `#f3f3f3`. Calc node: fill `#ffffff`, border `#666`. Selected calc: border `#d9480f`, 3 px. Edges: `#999`; highlighted edges and neighbour borders `#d9480f`. Edge width is `min(1 + 0.75 × (bindings − 1), 5)` px. Warning labels: text `#8a4b00` on `#fff4e0`. These are cosmetic; the implementer may adjust for legibility and records the change.
- **PD2. `test_panel.py` shares one loaded page per module** for the read-only 76-calc sweeps (a module-scoped fixture in `conftest.py`). The synthetic unrenderable-tree test in the same file uses its own per-test page. Loading once cuts about 76 page loads out of the run.
- **PD3. Panel wording beyond the spec's labels** uses the strings already in design § Implementation Notes and Appendix C verbatim. New strings the implementer needs are short and plain, and are listed in the Phase 2 implementation notes when added.
- **PD4. A missing Playwright or Chromium fails the model_viz tests, not the whole run.** The design says the default run "fails loudly, never skips." A `conftest.py` that raises at import would abort collection of the entire `tests/` tree and hide every other suite's result. So the import is guarded, and the session-scoped browser fixture calls `pytest.fail` with the exact commands `uv sync --extra e2e` and `uv run playwright install chromium`. Every model_viz test then fails loudly with that message; other suites still run. This keeps the design's rule (a green run always means the viewer was exercised) without the collateral damage.
- **PD5. The fixture's hash is checked.** A session fixture computes the fixture's SHA-256 and fails with both hashes if it differs from the spec's. The spec's counts are facts about that exact file; a regenerated snapshot must fail loudly, not produce confusing count mismatches.
- **PD6. Two DOM hooks added to the design's list,** needed for the verbatim and both-directions checks without reading projection data. The panel root carries `data-calc-node-id` (the calc's raw `node_id`). Each formula entry `li[data-formula-index]` holds its verbatim text in a child `.formula-text` element, and the "repeats the documentation below" note in a separate `.formula-note` child, so the verbatim `textContent` check (I7) is not polluted by the note. Literal and default input rows carry `data-value` with the raw value as `String(value)`.
- **PD7. The page's console must stay clean.** Handled load errors show in the banner and do not call `console.error`. The per-test page fixture fails the test on any page error, any `console.error`, or any `http:`/`https:` request. This makes "the page does not crash" and "no network" checks global rather than per test.

## Spec Criterion → Test Map

Every success criterion has a test task. Test file names follow design § Validation Approach.

| # | Spec criterion (short) | Test | Phase |
|---|---|---|---|
| L1 | Pick the fixture through the file picker, graph renders, no server | `test_loading.py::test_fixture_loads_via_picker` (plus global no-network check, PD7) | 1 |
| L2 | Wrong `schema_version` names expected and found | `test_loading.py::test_wrong_version_rejected` | 4 |
| L3 | JSON with no `schema_version` gives a clear error | `test_loading.py::test_not_a_snapshot_rejected` | 4 |
| L4 | Non-JSON file gives a clear error, no crash | `test_loading.py::test_non_json_rejected` | 4 |
| L5 | Second load replaces the first (and a bad second load leaves no remnant, I6) | `test_loading.py::test_second_load_replaces_first`, `::test_bad_load_after_good_clears` | 4 |
| G1 | 76 calc nodes | `test_graph_edges.py::test_calc_nodes` | 1 |
| G2 | 17 groups, largest 33, two design-file groups | `test_graph_edges.py::test_source_groups` | 1 |
| G3 | All expanded: 140 distinct directed pairs, producer → consumer | `test_graph_edges.py::test_all_expanded_edges` | 1 |
| G4 | `node`, `literal`, `null` inputs make no edge | `test_graph_edges.py::test_only_producer_inputs_make_edges` | 1 |
| G5 | All collapsed: 35, four two-way pairs both directions, no self-loops | `test_graph_edges.py::test_all_collapsed_edges` | 1 |
| G6 | Round trip, every group | `test_graph_edges.py::test_round_trip_every_group` | 1 |
| G7 | Round trip, interleaved account-costs / generic plant | `test_graph_edges.py::test_round_trip_interleaved` | 1 |
| P1 | Clicking a calc node opens its panel with formula, doc, location, inputs, outputs | `test_panel.py::test_panel_sections` (via `showCalc`) and `test_navigation.py::test_canvas_gestures` (real click) | 2, 3 |
| P2 | 65 formula lists verbatim, in order; doc shown at least once | `test_panel.py::test_formula_entries_verbatim` | 2 |
| P3 | 11 derived formulas with label; doc-absence label; unrenderable tree shows "No formula available" | `test_panel.py::test_derived_formulas`, `::test_unrenderable_tree_synthetic` | 2, 4 |
| P4 | Four input kinds labelled; `fuel_handling` and `fuel` examples; totals 150/234/10/52 | `test_panel.py::test_input_kinds_and_totals` | 2 |
| P5 | Each of 150 bindings appears in both panels | `test_panel.py::test_bindings_both_directions` | 2 |
| P6 | Outputs list consumers; 64 of 155 have none | `test_panel.py::test_output_consumers` | 2 |
| N1 | Clicking a panel link selects, centres inside the pane, panel follows | `test_navigation.py::test_panel_link_navigation` | 3 |
| N2 | Hidden target, one upstream and one downstream link | `test_navigation.py::test_hidden_target_upstream`, `::test_hidden_target_downstream` | 3 |
| U1 | Unresolvable producer (removed calc) | `test_guards.py::test_unresolvable_producer` | 4 |
| U2 | Overlay readiness (occurrence grouping) | `test_guards.py::test_overlay_occurrence_grouping` | 4 |

Supporting tests, not a spec criterion on their own: `test_pure_layer.py` (printer edge cases, `endsWithDoc`, view rule on a hand-built model; Phase 1 and 2), `test_navigation.py::test_search_box` (Phase 3), `test_panel.py::test_calendar_note` (Phase 2).

---

## Phase 0: Capture the Test Baseline

### Goal

Record which tests already fail before any model_viz code exists, so Phase 5 can prove "no new failures."

### Assumption Under Test

The existing suite's failures are stable enough to diff by test id.

### Steps

- [x] Check `.project/active/model-viz/evidence/pytest_baseline_before_phase1.txt`. On 2026-09-13 it exists and is empty (0 bytes). If it is still empty, capture the baseline below and overwrite it. If it already has content, keep it and note that in Implementation Notes.
- [x] Confirm no other pytest or study battery is running (`ps -ef | grep "[p]ytest"`). Two runs share `.integration_workspace` and produce phantom errors (auto-memory, "one battery at a time").
- [x] Run the full suite once, detached, writing to a file: `uv run python -m pytest -q -rfE -p no:cacheprovider > .project/active/model-viz/evidence/pytest_full_before.log 2>&1`. It collects about 1,215 tests; allow it to run to completion.
- [x] Extract the failing ids: `grep -E '^(FAILED|ERROR) ' .project/active/model-viz/evidence/pytest_full_before.log | sed -E 's/ - .*//' | sort -u > .project/active/model-viz/evidence/pytest_baseline_before_phase1.txt`.
- [x] Record the summary line (passed / failed / errors) in Implementation Notes.

### Validation

- [x] The baseline file lists one test id per line and its count matches the log's failed + error count.

---

## Phase 1: Seams and the Edge Rule

### Goal

Vendor the three libraries, build the pure layer, a page shell that loads a snapshot through the file input, and a graph shell that draws what the view function returns. Prove with the Python oracle that the drawn edges follow the visible-edge rule all collapsed, all expanded, and through every collapse round trip.

### Assumption Under Test

- Classic scripts plus vendored Cytoscape/dagre run from `file://` in headless Chromium 145 with no network (design D3).
- Playwright's `set_input_files` drives the real file input and the page reports completion through `data-load-state` / `data-load-seq`.
- The view function (design § The visible-edge rule) and an independently written Python oracle agree on the rendered edges in every state the spec names, and the literal anchors (35, 140, the four two-way pairs) hold. If they disagree, one of the two misreads the rule; resolve against spec § Known Requirements › Graph, not by editing the oracle to match.

### Test Stencil (Write This First)

```python
# tests/model_viz/test_graph_edges.py
from edge_oracle import expected_edges, load_fixture, displayed_edges, group_paths

def test_all_collapsed_edges(fixture_page):
    snap = load_fixture()
    fixture_page.click("[data-action=collapse-all]")
    got = displayed_edges(fixture_page)                      # sorted list of (src_identity, tgt_identity), read from cy.edges()
    want = expected_edges(snap, collapsed_paths=set(group_paths(snap)))
    assert got == want and len(got) == 35
    assert all(s != t for s, t in got)                       # no self-loops
    for a, b in TWO_WAY_PAIRS:                               # four named pairs, by group path
        assert (f"group:{a}", f"group:{b}") in got and (f"group:{b}", f"group:{a}") in got
    assert_unique_edge_ids(fixture_page)
```

```python
def test_round_trip_every_group(fixture_page):
    snap = load_fixture(); fixture_page.click("[data-action=expand-all]")
    start = displayed_edges(fixture_page)
    for path in group_paths(snap):
        toggle_group(fixture_page, path)                     # maps path→container id via cy, calls modelVizApp.toggleContainer
        assert displayed_edges(fixture_page) == expected_edges(snap, collapsed_paths={path})
        toggle_group(fixture_page, path)
        assert displayed_edges(fixture_page) == start
```

### Changes Required

**See `design.md` for:** architecture and file roles → § Architecture, § Component Overview; model and element shapes → § Model shape, § Cytoscape element data; the rule → § The visible-edge rule, as the view function applies it; containers → § Containers per grouping mode; invariants I1–I8 → § Required Invariants; script order, `cy.batch`, tap bubbling, file input reset, load errors → § Implementation Notes; oracle comparison rules → § Validation Approach; layout options → D4; start state → D5; app handle → D13.

#### 1. Vendor the libraries (first, so nothing else touches the network)

- [x] `mkdir -p src/model_viz/viewer/vendor` and download with `curl -fsSL -o`:
  - `https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js` → `cytoscape-3.28.1.min.js`
  - `https://unpkg.com/dagre@0.8.5/dist/dagre.min.js` → `dagre-0.8.5.min.js`
  - `https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js` → `cytoscape-dagre-2.5.0.js`
- [x] Confirm each licence from the package's `package.json` on unpkg (`https://unpkg.com/<pkg>@<ver>/package.json`, field `license`). The design expects MIT for all three; if any differs, stop and record it.
- [x] Write `src/model_viz/viewer/vendor/VENDOR.md`: one table row per file with package, version, source URL, licence, SHA-256 (`sha256sum`), download date. Add one line saying the expand-collapse extension is deliberately not vendored (design D1).

#### 2. Test harness (write before viewer code)

**File:** `tests/model_viz/conftest.py` (NEW). No `__init__.py` anywhere under `tests/model_viz/` (namespace tree, `pyproject.toml` testpaths).

- [x] Guarded `playwright.sync_api` import; session `browser` fixture that `pytest.fail`s with the two install commands on import or launch failure (PD4).
- [x] Session `fixture_path` fixture that checks the SHA-256 (PD5).
- [x] Per-test `viewer_page` fixture: new page at viewport 1600×1000, `goto` the `file://` URI of `src/model_viz/viewer/index.html`, record page errors, `console.error` messages and any `http:`/`https:` request; at teardown fail on any of them (PD7). Close the page.
- [x] `load_snapshot(page, path)` helper: read `document.body.dataset.loadSeq`, `set_input_files` on the file input, wait until `loadSeq` increments, return `dataset.loadState`.
- [x] `fixture_page` fixture = `viewer_page` with the fixture loaded and state asserted `ready`.
- [x] Module-scoped `loaded_fixture_page` for PD2 (its own error and request capture, checked at module teardown). Can be added in Phase 2 if preferred.

**File:** `tests/model_viz/edge_oracle.py` (NEW). Reads the raw snapshot JSON in Python and shares no code or data with the viewer.

- [x] `load_fixture()`, `group_paths(snap)`, `producer_bindings(snap)` (list of `(consumer node_id, input name, producer node_id, output id)`, resolved only).
- [x] `expected_edges(snap, collapsed_paths)` for source-file mode: representative of a calc is `group:<path>` when its path is collapsed, else its `node_id`; drop equal ends; return the sorted list of distinct `(source, target)` pairs.
- [x] `displayed_edges(page)`: `page.evaluate` over `modelVizApp.cy.edges()`, mapping each endpoint to `node_id` for calc nodes and `group:<group_path>` for containers; return the sorted list with one tuple per drawn edge (no dedupe). `assert_unique_edge_ids(page)`.
- [x] `toggle_group(page, path)`: find the container id in `cy` by `group_path`, call `modelVizApp.toggleContainer(id)`. The test keeps its own `collapsed_paths`; the oracle never reads the page (design § Validation Approach, DR-M2).

**File:** `tests/model_viz/test_pure_layer.py` (NEW)

- [x] `ModelViz.formula.printExpression`: `+` chain, `*` with a `+` operand gets parentheses, dotted `feature_ref`, `9400.0` prints `9400`, `/` operator → `null`, one-operand operator → `null`, null literal value → `null`, empty `source_name` → `null`.
- [x] `ModelViz.formula.endsWithDoc`: true when the entry ends with a non-empty doc; false for empty doc or no match.
- [x] `ModelViz.view.visibleElements` on a small hand-built snapshot passed through `ModelViz.model.buildModel` (a Python dict handed to `page.evaluate`): self-loop dropped when both ends share a collapsed group; a two-way pair gives two edges; in occurrence mode, a nested collapse maps a calc to the outermost collapsed ancestor; I2 and I3 hold (every edge's `bindings` non-empty, each binding on exactly one edge or none).
- [x] `ModelViz.model.readSnapshot` refuses a wrong version with both version strings in the message (cheap here; the UI check is Phase 4).

**File:** `tests/model_viz/test_loading.py` (NEW)

- [x] `test_fixture_loads_via_picker`: `load_snapshot` returns `ready`; 76 calc nodes exist in `cy`; the file input is a real `<input type=file>`.

**File:** `tests/model_viz/test_graph_edges.py` (NEW)

- [x] `test_calc_nodes` (G1): 76 calc nodes after Expand all; their `node_id` set equals the snapshot's.
- [x] `test_source_groups` (G2): 17 containers after load; `member_count` 33 for `root-0/analyses/mfe_account_costs.sysml`; `container_kind` `design` for exactly `mfe_plant.sysml` (10) and `stellarator_plant.sysml` (1).
- [x] `test_all_expanded_edges` (G3): list equals oracle with no collapsed paths; length 140; every edge's source is a producer and target a consumer per `producer_bindings`.
- [x] `test_only_producer_inputs_make_edges` (G4): the drawn calc pairs equal the pairs from producer inputs alone; no endpoint is an `attrs` `node_id`; recompute pairs including `node`/`literal`/`null` inputs in Python and assert the drawn list excludes anything only they would add.
- [x] `test_all_collapsed_edges` (G5): stencil above. The four two-way pairs by full path: `mfe_account_costs.sysml` ↔ `designs/generic_mfe/mfe_plant.sysml`, `mfe_plasma_scaling` ↔ `mfe_plasma_sustainment`, `mfe_magnet_field` ↔ `mfe_plasma_scaling`, `mfe_power_balance` ↔ `mfe_primary_loop`. Take the exact paths from the snapshot, and assert these are exactly the two-way pairs the oracle finds (so the anchor cannot drift from the fixture).
- [x] **Checkpoint:** the tests above green before starting the round trips.
- [x] `test_round_trip_every_group` (G6): stencil above, all 17 groups.
- [x] `test_round_trip_interleaved` (G7): steps collapse account-costs, collapse generic plant, expand account-costs, expand generic plant; after each, equal to the oracle for the test's own `collapsed_paths`; after the last, equal to the start.

Run `uv run python -m pytest tests/model_viz -q` now and confirm each test fails because the page or function is missing, not because the harness is broken.

#### 3. Viewer code

**Files:** `src/model_viz/viewer/index.html`, `viewer.css`, `js/model.js`, `js/formula.js`, `js/view.js`, `js/graph.js`, `js/app.js` (all NEW). `js/panel.js` gets a stub that renders the "select a calc" placeholder only.

- [x] `index.html`: toolbar (file input, Expand all / Collapse all / Fit buttons with `data-action`, an empty mode select and search box placeholders for later phases), graph pane, always-present 420 px panel (D9), error banner, script tags in the design's order. `body` starts `data-load-state="empty"`, `data-load-seq="0"`.
- [x] `model.js`: `readSnapshot(text)` with the load errors in § Implementation Notes and Appendix C; `buildModel(snap)` per § Model shape, one pass for bindings and `consumersOf`, unresolved bindings kept with `producer: null`.
- [x] `formula.js`: `printExpression(ir)` per § Formula printer; `endsWithDoc(entry, doc)` per D7.
- [x] `view.js`: `containerTree(model, mode)` for both modes (occurrence mode is needed by `test_pure_layer.py` now and by the UI in Phase 4); `visibleElements(model, tree, collapsed)` per the four-step rule, D2 edge ids `e:<s>><t>` with a `bindings` list.
- [x] `graph.js`: Cytoscape instance on the graph pane, stylesheet with `curve-style: bezier`, `target-arrow-shape: triangle` and PD1 colours, `render(elements)` as `cy.batch(remove; add)` then dagre per D4, `cy.resize()` on window resize, tap handlers per D10 with the `evt.target` guard.
- [x] `app.js`: state object, file input handler (I6 clear first, then read, set `input.value = ""`, bump `data-load-seq`), start collapsed (D5), toolbar actions, `window.modelVizApp` with `cy`, `model`, state, `toggleContainer`, `expandAll`, `collapseAll` (and stubs for `showCalc`, `navigateTo` filled in later phases).

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/model_viz -q` → all Phase 1 tests pass.
- [x] `uv run ruff check tests/model_viz` → clean.
- [x] `grep -nE "document|cy\." src/model_viz/viewer/js/{model,formula,view}.js` → no hits (I8; the `window.ModelViz = window.ModelViz || {}` line is the only `window` use).

**Manual:**
- [x] `sha256sum src/model_viz/viewer/vendor/*.js` matches `VENDOR.md`.
- [x] Record the wall time of the `tests/model_viz` run in Implementation Notes (the spike's 3-minute run was blamed on unpkg and screenshots; this run should be well under that).

**What we know works after this phase:** the page loads a snapshot offline from `file://`, and every edge it draws in every source-mode collapse state the spec names matches an independent oracle, with the literal fixture anchors holding.

---

## Phase 2: The Detail Panel

### Goal

Render one calc's header, location, formula, documentation, inputs and outputs from the model, with every DOM hook the tests need.

### Assumption Under Test

The model built in Phase 1 carries everything the panel needs (bindings both directions through `consumersOf`, attr values, defaults, file hashes), so the panel is a pure read of the model with no second pass over the snapshot. The IR printer renders all 11 fixture trees.

### Test Stencil (Write This First)

```python
# tests/model_viz/test_panel.py
def test_bindings_both_directions(loaded_fixture_page):
    snap = load_fixture(); page = loaded_fixture_page
    want = Counter(producer_bindings(snap))                  # (consumer, input, producer, output), 150
    as_consumer, as_producer = Counter(), Counter()
    for calc in snap["instance_graph"]["graph"]["calcs"]:
        show_calc(page, calc["node_id"])                     # modelVizApp.showCalc(key for node_id)
        me = page.get_attribute("[data-panel]", "data-calc-node-id")
        for row in page.query_selector_all("[data-input-kind=producer]"):
            as_consumer[(me, row.get_attribute("data-input-name"), row.get_attribute("data-producer-node-id"), row.get_attribute("data-output-id"))] += 1
        for link in page.query_selector_all("[data-output-id] [data-consumer-node-id]"):
            as_producer[(link.get_attribute("data-consumer-node-id"), link.get_attribute("data-input-name"), me, output_id_of(link))] += 1
    assert as_consumer == want and as_producer == want       # multisets, not sets (DR-N5)
```

### Changes Required

**See `design.md` for:** panel sections and layout → D9; formula section and the doc repeat → D7 and § Formula printer; source location and hash → D11; parameter, default, unresolved and undeclared-output display → § Implementation Notes, § Reverse index and unresolved producers, Appendix C; DOM hooks → § Component Overview, "Panel DOM hooks for tests" (plus PD6 here); verbatim rendering → I7 and § Implementation Notes (`textContent`, `pre-wrap`).

#### 1. Tests first

**File:** `tests/model_viz/test_panel.py` (NEW), using `loaded_fixture_page` (PD2) and a `show_calc(page, node_id)` helper in `conftest.py`.

- [x] `test_panel_sections` (P1): for a sample calc, each of `location`, `formula`, `doc`, `inputs`, `outputs` sections exists and is non-empty; header shows the calc name; `data-calc-node-id` matches.
- [x] `test_formula_entries_verbatim` (P2): for all 65 calcs with non-empty `calc_expressions`, the `.formula-text` elements under `li[data-formula-index]` have `textContent` equal to the snapshot entries, same count, same order; the `doc` section's text contains `doc_comment`; the last entry carries `data-doc-repeat`.
- [x] `test_calendar_note`: `calendar`'s single entry carries `data-doc-repeat` and the formula section shows the "no formula lines recorded for this calc" note (D7).
- [x] `test_derived_formulas` (P3, fixture part): for the 11 calcs with empty `calc_expressions`, the formula section contains the exact label "derived from expression structure; the snapshot has no formula text for this calc.", does not contain "No formula available", starts with `<output name> = `, and contains every `feature_ref` `source_name` from the IR in left-to-right order (walked in Python). The doc section carries `data-doc-absent`. Location and inputs/outputs sections are still present.
- [x] `test_input_kinds_and_totals` (P4): across all 76 panels, `data-input-kind` counts are producer 150, parameter 234, literal 10, default 52, and each input row's kind matches the snapshot input's edge kind. `fuel_handling` shows a producer row with an upstream calc link and port, a parameter row with attribute name and value, and a literal row `ref_power` with `float(data-value) == 1000.0`. `fuel` shows a default row `s_per_fpy_in` with `float(data-value) == 31536000.0`.
- [x] `test_bindings_both_directions` (P5): stencil above.
- [x] `test_output_consumers` (P6): 155 output rows in total; 64 carry `data-no-consumer`; every other output's consumer links match the snapshot's producer targets for that `(calculation, output)`.
- [x] `test_location_and_hash` (supports P1, D11): each panel's location reads `source_file:source_line` and shows the first 12 hex digits of the matching `sources.files` hash.

#### 2. Code

- [x] `js/panel.js`: `renderPanel(model, key)` building sections with `textContent` only; PD6 hooks; calc links carry `data-calc-key` and call a callback supplied by `app.js`.
- [x] `js/app.js`: `showCalc(key)` renders the panel, selects the node in `cy` if visible, applies the highlight class to its visible edges and their other ends (D10).
- [x] `viewer.css`: section styles, `pre-wrap` on `.formula-text` and the doc, warning-label style (PD1).

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/model_viz -q` → Phase 1 and Phase 2 tests pass.

**Manual:**
- [x] Open `src/model_viz/viewer/index.html` in headless Chromium with a short throwaway script (or the implementer's own browser if one is available), load the fixture, show `total_capital` and `fuel_handling`, take one screenshot of the panel to `/tmp/`, and look at it: sections readable, warnings styled, no raw HTML showing. Not kept as evidence; the Phase 5 walk is.

**What we know works after this phase:** every calc's panel shows its formula (verbatim or derived, honestly labelled), its doc or a labelled absence, its location, and every binding from both ends.

---

## Phase 3: Navigation, Search and Canvas Gestures

### Goal

Make the panel links, the search box and the three canvas gestures work, including navigation to a calc hidden inside a collapsed group.

### Assumption Under Test

- The navigation contract (expand the chain from `containerTree`, rebuild, select, zoom to at least 1.0, centre, all on one tick; D6) leaves the target fully inside the graph pane after a real click, as the rebuild check suggested.
- Real `page.mouse.click` at a point from `renderedBoundingBox` plus the graph pane's page offset reaches Cytoscape's tap handlers, and the `evt.target` guard stops a calc tap from collapsing its parent.

### Test Stencil (Write This First)

```python
# tests/model_viz/test_navigation.py
def test_hidden_target_upstream(fixture_page):
    snap = load_fixture()
    consumer, producer = cross_group_binding(snap)           # first binding (snapshot order) whose ends are in different groups
    page = fixture_page
    page.click("[data-action=collapse-all]"); toggle_group(page, path_of(snap, consumer))
    click_calc_on_canvas(page, consumer)
    page.click(f"[data-input-kind=producer][data-producer-node-id='{css_str(producer)}'] [data-calc-key]")
    assert page.get_attribute("[data-panel]", "data-calc-node-id") == producer
    assert selected_node_ids(page) == [producer]
    assert group_expanded(page, path_of(snap, producer))
    assert fully_inside_pane(page, producer)                  # renderedBoundingBox within [0, cy.width()] x [0, cy.height()]
```

### Changes Required

**See `design.md` for:** the navigation contract → § Navigation contract and D6; gestures → D10 and § Implementation Notes (tap bubbling); search box behaviour → § Implementation Notes; the canvas-gesture test recipe → § Validation Approach, `test_navigation.py` row.

#### 1. Tests first

**File:** `tests/model_viz/test_navigation.py` (NEW). Helpers (`click_calc_on_canvas`, `fully_inside_pane`, `selected_node_ids`, `cross_group_binding`) live in this file or in `edge_oracle.py`; any new helper module needs a name unique across `tests/`.

- [x] `test_panel_link_navigation` (N1): Expand all, show a calc, real-click one upstream link; target selected, fully inside the pane, panel shows it. Then real-click a downstream consumer link from the new panel and assert the same.
- [x] `test_hidden_target_upstream` (N2): stencil above. Pick the pair from the snapshot in Python, never hardcoded.
- [x] `test_hidden_target_downstream` (N2): same, starting from a producer whose consumer is in a different, collapsed group; click the consumer link in its Outputs section.
- [x] `test_canvas_gestures` (P1 real click, DR-M1, DR-N7): from all collapsed, (1) click a collapsed container's centre → expanded; (2) click a calc node's centre inside it → panel shows that calc, node selected, container still expanded and the calc still in `cy`; (3) click inside the expanded container at a point the test first checks is outside every child's bounding box → collapsed. Pick a container with at least 5 calcs so there is background to click (`mfe_magnet_cost` or larger).
- [x] `test_search_box`: from all collapsed, fill the search input with `cas22_capital` and press Enter → same end state as N2 (group expanded, selected, inside pane, panel). Also: a name with no match shows "no calc matches"; a substring with several matches shows the count and navigates nowhere.
- [x] `test_navigate_unknown_key`: `modelVizApp.navigateTo("nope")` shows the panel-level warning and does not throw.

#### 2. Code

- [x] `js/app.js`: `navigateTo(key)` per the contract; re-select after other rebuilds; search box with `<datalist>` and the match rules.
- [x] `js/graph.js`: finish the three tap gestures if Phase 1 left any unwired; selection highlight.
- [x] `js/panel.js`: link callbacks call `navigateTo`.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/model_viz -q` → Phases 1–3 pass.
- [x] Run `test_navigation.py` three times in a row (`--count` is not installed; loop in the shell) → no flaky failures. Canvas clicks after a layout are the likeliest flake; if one appears, wait for the layout's `layoutstop` before reading bounding boxes rather than adding sleeps.

**Manual:**
- [x] None beyond the Phase 5 walk.

**What we know works after this phase:** a modeler can click from any calc to its neighbours, find a calc by name, and open, select and close groups on the canvas, and navigation never silently does nothing.

---

## Phase 4: Guards, Error Loads and Synthetic Snapshots

### Goal

Build the synthetic snapshot builders and prove the error loads, the replace-on-reload rule, the unresolved-producer guard, the unrenderable-tree fallback, and occurrence grouping.

### Assumption Under Test

- The load path clears everything before validating (I6), so a failed or second load leaves no remnant.
- Occurrence mode needs no viewer code change beyond the mode select: containers keyed by `occurrence_id`, nested by `parent_id` (design § Containers per grouping mode).
- An unresolved producer shows in the consumer panel and never reaches an edge.

### Test Stencil (Write This First)

```python
# tests/model_viz/test_guards.py
def test_unresolvable_producer(viewer_page, tmp_path):
    snap, removed = viewer_snapshots.remove_most_consumed_calc(load_fixture())   # on the fixture: pb, 27 consumers
    path = viewer_snapshots.write(snap, tmp_path / "removed.json")
    assert load_snapshot(viewer_page, path) == "ready"
    viewer_page.click("[data-action=expand-all]")
    assert calc_node_count(viewer_page) == 75
    assert every_edge_endpoint_exists(viewer_page)
    for consumer, input_name in consumers_of(load_fixture(), removed):
        show_calc(viewer_page, consumer)
        row = viewer_page.query_selector(f"[data-input-name='{input_name}'][data-unresolved]")
        assert row and row.get_attribute("data-producer-node-id") == removed
```

### Changes Required

**See `design.md` for:** synthetic snapshot list → § Validation Approach, "Synthetic snapshots"; load error texts → § Implementation Notes and Appendix C; unresolved producers → § Reverse index and unresolved producers; occurrence containers → § Containers per grouping mode; mode select behaviour → § Implementation Notes and D5; `test_loading.py` and `test_guards.py` rows → § Validation Approach table.

#### 1. Tests first

**File:** `tests/model_viz/viewer_snapshots.py` (NEW). Every builder deep-copies the fixture dict; `write(snap, path)` writes JSON to `tmp_path`. Nothing is checked in and the fixture file is never modified.

- [x] `wrong_version(snap)` (sets `instance-graph/v2`), `no_version(snap)`, `non_json_bytes()` (PDF-like bytes starting `%PDF-1.7`), `renamed(snap)` (every calc `display_name` prefixed `renamed_`), `remove_most_consumed_calc(snap)` (returns the removed `node_id`; ties broken by snapshot order), `unrenderable_tree(snap)` (first of the 11 IR calcs, its root operator set to `/`), `overlay(snap)`.
- [x] `overlay(snap)`: add one occurrence under the root and two children under it with the same `display_segment` and distinct `occurrence_id`s; re-scope the calcs of one multi-calc source file (for example `mfe_magnet_cost.sysml`, 5 calcs) so they split across the two children; leave every other calc on the root. Return the snapshot and the expected `node_id → occurrence_id` assignment.

**File:** `tests/model_viz/test_loading.py` (extend)

- [x] `test_wrong_version_rejected` (L2): state `error`; banner contains `instance-graph/v3` and `instance-graph/v2`; zero nodes in `cy`.
- [x] `test_not_a_snapshot_rejected` (L3): state `error`; banner says "not a codegen snapshot"; zero nodes.
- [x] `test_non_json_rejected` (L4): state `error`; banner says "not a JSON file"; zero nodes. PD7 teardown proves no page error.
- [x] `test_second_load_replaces_first` (L5): load the fixture, show a calc, then load `renamed`; every calc label in `cy` starts `renamed_`; no original `display_name` remains in `cy` labels or the panel text; the panel shows the placeholder or a renamed calc.
- [x] `test_bad_load_after_good_clears` (L5, I6): load the fixture, then `non_json_bytes`; zero nodes, panel shows no calc, state `error`.
- [x] `test_same_file_repick_reloads` (DR-N6): load the fixture twice from the same path; `data-load-seq` increments both times.

**File:** `tests/model_viz/test_panel.py` (extend)

- [x] `test_unrenderable_tree_synthetic` (P3, synthetic part): per-test page; load `unrenderable_tree`; that calc's formula section shows "No formula available" and the same derived-formula label; no page error; its location and I/O still show.

**File:** `tests/model_viz/test_guards.py` (NEW)

- [x] `test_unresolvable_producer` (U1): stencil above; also assert the unresolved row has a visible warning element.
- [x] `test_overlay_occurrence_grouping` (U2): load `overlay`, `select_option` the mode select to `Occurrence`, click Expand all; for every calc, walk its `parent` chain in `cy` and assert the container `occurrence_id`s equal the expected occurrence and its ancestors, ending at the root; the two same-segment siblings are two distinct container nodes; the split source file's calcs sit under both. Also assert every calc node still carries `source_group` and `occurrence_id` (I5), and that switching back to `Source file` restores 17 collapsed groups.

#### 2. Code

- [x] `js/model.js`: finish Appendix C field checks if Phase 1 left gaps (calc and input index in messages).
- [x] `js/app.js`: mode select (`Source file` / `Occurrence`), rebuild tree, collapse all, keep selection (§ Implementation Notes).
- [x] `js/panel.js`: unresolved row with warning and raw target; undeclared-output rows; "unknown input kind" row (Appendix C).

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/model_viz -q` → Phases 1–4 pass.
- [x] `git status --short exploration/stellarator_e2e/stellarator.snapshot.json` → no change (fixture untouched).

**What we know works after this phase:** bad input fails loudly and cleanly, reloading never mixes snapshots, a missing producer is visible rather than dropped, and the viewer groups calcs by occurrence with no code change.

---

## Phase 5: Documentation, Manual Walk and Quality Pass

### Goal

Write the README, do the manual layout walk and record its evidence, and prove no regressions in the wider suite.

### Assumption Under Test

- Bets B3 (collapsed start orients), B4 (compound overlap is cosmetic) and B5 (full re-layout per toggle does not disorient) hold on the fixture when looked at, not just counted.
- The new tests add no failures elsewhere under the default `testpaths = ["tests"]` run.

### Steps

#### 1. README

**File:** `src/model_viz/README.md` (NEW)

- [x] How to open the viewer: open `src/model_viz/viewer/index.html` in a browser, pick a codegen snapshot (for example `exploration/stellarator_e2e/stellarator.snapshot.json`); no server, no network.
- [x] What it reads: an `instance-graph/v3` codegen snapshot, and only that; what it shows (calcs, producer bindings as edges, the panel); what it does not (verbatim SysML, Python, attributes, multi-hop), pointing to `.project/active/model-viz/spec.md` § Non-Goals.
- [x] How to run the tests: `uv run python -m pytest tests/model_viz`; prerequisites `uv sync --extra e2e` and `uv run playwright install chromium`; the fixture hash check (PD5) and what to do when codegen regenerates the fixture (the spec's counts must be re-probed, not edited to pass).
- [x] Where the libraries come from: `viewer/vendor/VENDOR.md`.
- [x] File map: one line per file under `viewer/js/` with its role (pure vs shell).

#### 2. Manual layout walk (design § Validation Approach, "Manual check")

- [x] Write `.project/active/model-viz/evidence/manual_walk.py`, a short Playwright script (viewport 1600×1000) that loads the fixture through the file input and screenshots each step: `01_all_collapsed.png`, `02_account_costs_expanded.png`, `03_cost_calc_selected.png` (for example `cas22_capital`), `04_after_upstream_link.png`, `05_all_expanded.png`. Screenshots go to `.project/active/model-viz/evidence/`.
- [x] Run it and look at every screenshot (Read tool). Compare `02` with `.project/active/model-viz/spike/out/LR_2_account_costs_expanded.png`.
- [x] Write `.project/active/model-viz/evidence/manual_walk.md`: one short section per screenshot answering, in plain words, whether labels are legible, whether the two-way edges show as two curves with arrowheads, whether the selected calc and its neighbours stand out, and whether the step's result is where the eye expects it. Then one line each for B3, B4 and B5: held, or did not hold, with what was seen. If a bet did not hold, record it as a finding for the owner and do not change the architecture in this item (design names the fallbacks).

#### 3. Quality pass

- [x] `uv run ruff check tests/model_viz` and `uv run ruff format --check tests/model_viz` → clean.
- [x] Pure-layer check (I8): the `grep` from Phase 1 still has no hits.
- [x] Size check: `wc -l src/model_viz/viewer/js/*.js`. Any file over about 400 lines gets a note explaining why, or is split along the design's roles.
- [x] No `innerHTML` in `src/model_viz/viewer/js/` (`grep -n innerHTML` → no hits, or only on elements with no snapshot text, noted).
- [x] No network URL in the viewer: `grep -rnE "https?://" src/model_viz/viewer --include=*.html --include=*.js --include=*.css | grep -v vendor/` → no hits.
- [x] Every checkbox in the Spec Criterion → Test Map has a passing test; tick them in `spec.md` only if the orchestrator's close stage asks for it (do not edit the spec here).

#### 4. Regression diff

- [x] Confirm no other test battery is running.
- [x] Run the full suite once, detached: `uv run python -m pytest -q -rfE -p no:cacheprovider > .project/active/model-viz/evidence/pytest_full_after.log 2>&1`.
- [x] Extract failing ids the same way as Phase 0 into `evidence/pytest_failures_after.txt`, then `comm -13 evidence/pytest_baseline_before_phase1.txt evidence/pytest_failures_after.txt > evidence/pytest_new_failures.txt`.
- [x] Gate: `pytest_new_failures.txt` is empty, and no `tests/model_viz` id appears in the after-list. If a pre-existing test newly fails, check whether model_viz caused it (for example a conftest or namespace-name collision) before calling it unrelated; record the evidence either way.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/model_viz -q` → all green.
- [x] `evidence/pytest_new_failures.txt` is empty.

**Manual:**
- [x] `evidence/manual_walk.md` exists with five screenshots referenced and B3/B4/B5 lines filled.
- [x] A fresh reader can follow `src/model_viz/README.md` to open the viewer and run the tests.

**What we know works after this phase:** the viewer is documented, looked at, and adds no regressions; the item is ready for `/_my_audit`.

---

## Environment Setup

**See CLAUDE.md for the full environment rules.** Item-specific facts, verified by the orchestrator on 2026-09-13:

- Always `uv run python ...`. No `node` on this machine.
- Python Playwright 1.58.0 is in the `e2e` extra and launches Chromium 145. `pytest-playwright` is not installed; use `playwright.sync_api` directly.
- unpkg is reachable, so vendoring is `curl` plus a hash record. After Phase 1 nothing needs the network.
- `tests/` is a namespace tree: no `__init__.py` under `tests/model_viz/`, and helper module names must be unique across `tests/`.
- Run one test battery at a time; do not start the full suite while `tests/model_viz` or a study run is going.
- Do not commit (orchestrator rule for this run). The orchestrator commits.

## Risk Management

**See `design.md` § Potential Risks and § Key Bets** for the design-level risks.

**Phase-specific mitigations:**

- **Phase 1, oracle and view disagree.** Both could be wrong. Settle each disagreement against the spec's rule text and the literal anchors (35, 140, four two-way pairs), and write the resolution in Implementation Notes. Never adjust the oracle only to match the page.
- **Phase 1, Cytoscape selectors with quoted `node_id`s.** Short keys (`c0…`) avoid this in the page. In tests, match `node_id`s by reading `data()` in `page.evaluate`, not by building CSS selectors from raw ids; where a panel selector must use a raw id, escape it (`css_str` helper using `JSON.stringify`-style quoting or `CSS.escape` in the page).
- **Phase 1, harness failure hides as "everything fails."** Run the tests once before writing viewer code and confirm the failures name missing elements, not import or launch errors.
- **Phase 3, canvas-click flakiness after layout.** Read bounding boxes only after the layout's `layoutstop`; D6 keeps navigation synchronous, so no animation waits are needed.
- **Phase 4, overlay builder produces an invalid occurrence tree.** Assert the builder's own output in Python first (each new occurrence's `parent_id` exists; the two siblings share a segment and differ in id) before loading it.
- **Phase 5, full suite is slow or noisy.** It runs twice in the whole item, detached, with output to files; diff by test id, not by counts.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION — leave empty now]

### Phase 0 Completion
**Completed:** 2026-09-13. The orchestrator captured the baseline at launch, detached; the implement stage did not start a second run (brief, Phase 0 note).
**Baseline summary line:** `132 failed, 913 passed, 151 skipped, 20 errors in 406.14s (0:06:46)`, then `exit 1`.
**Issues:**
- The orchestrator's command differs from the plan's step: `set -a; source ~/1cfe/agentic-mbse/.env; set +a; timeout 3000 uv run python -m pytest tests -q -p no:cacheprovider --no-header -rf | grep -E "^FAILED|^ERROR|passed|failed"`. There is no separate `pytest_full_before.log`; the baseline file holds the filtered lines directly.
- Because of `-rf` (not `-rfE`), the file lists the 132 `FAILED` ids but none of the 20 `ERROR` ids. The validation "count matches failed + error" therefore holds for failures only. Phase 5 must run the same command with `-rfE`, diff the `FAILED` ids against this file, and compare the error count (20) as a number; any new `ERROR` id then needs a manual look.
- The file also carries the summary line and the `exit 1` line, so the Phase 5 diff must filter to `^FAILED` lines before `comm`.

### Phase 1 Completion
**Completed:** 2026-09-13
**Actual Changes:**
- `src/model_viz/viewer/vendor/` — `cytoscape-3.28.1.min.js`, `dagre-0.8.5.min.js`, `cytoscape-dagre-2.5.0.js`, `VENDOR.md` (URL, licence, SHA-256, date; expand-collapse deliberately not vendored).
- `src/model_viz/viewer/index.html` — toolbar (file input, mode select, Expand all / Collapse all / Fit, search input with datalist, search status), error banner, graph pane, always-present panel, scripts in design order. Body starts `data-load-state="empty"`, `data-load-seq="0"`.
- `src/model_viz/viewer/viewer.css` — D9 layout (flex column; graph pane `flex: 1`; panel 420 px, own scroll), banner, panel section and warning styles.
- `js/model.js` — `readSnapshot(text)` (non-JSON, no version, wrong version naming both, no calcs list) throwing `SnapshotError`; `buildModel(snap)` per design § Model shape with Appendix C field checks, one pass for `bindings` + `consumersOf`, unresolved bindings kept with `producer: null`.
- `js/formula.js` — `printExpression(ir)`, `endsWithDoc(entry, doc)`.
- `js/view.js` — `containerTree(model, mode)` for source and occurrence modes, `containerChain(tree, key)`, `visibleElements(model, tree, collapsed)` (the four-step rule; edge id `e:<s>><t>`, `bindings` list, `weight`).
- `js/graph.js` — Cytoscape instance, PD1 stylesheet, `render(elements)` as `cy.batch(remove; add)` then dagre (D4), one core-level tap handler dispatching on `evt.target` (bubbling guard), container tooltip via the pane's `title`, `cy.resize()` on window resize, `selectCalc(key)`, `focusCalc(key)`, `fit()`.
- `js/panel.js` — `renderPlaceholder(panelElement)` only (panel body comes in Phase 2).
- `js/app.js` — the state object, file input handler (I6 clear first, `input.value = ""`, load state and seq), start collapsed (D5), toolbar buttons, `window.modelVizApp` with `cy`, `model`, `state`, `toggleContainer`, `expandAll`, `collapseAll`.
- `tests/model_viz/conftest.py` — session `browser` (PD4 fail-loud), session `fixture_path` (PD5 hash), per-test `viewer_page` with PD7 teardown, `fixture_page`, module `loaded_fixture_page` (PD2).
- `tests/model_viz/viewer_harness.py` — page helpers (`open_viewer`, `load_snapshot`, `show_calc`, `toggle_group`, `selected_node_ids`, `css_str`, …) and `PageProblems`.
- `tests/model_viz/edge_oracle.py` — `load_fixture`, `group_paths`, `producer_bindings`, `expected_edges`, `two_way_group_pairs`, `displayed_edges`, `assert_unique_edge_ids`.
- `tests/model_viz/test_pure_layer.py` (printer cases, `endsWithDoc`, `readSnapshot` version refusal, view rule on a 4-calc / 2-file / 3-level-occurrence snapshot incl. every collapse subset for I2/I3), `test_loading.py::test_fixture_loads_via_picker`, `test_graph_edges.py` (G1–G7).
**Vendor hashes and licences confirmed:** all three MIT per `package.json` on unpkg; `sha256sum -c` against `VENDOR.md` → OK for all three.
**`tests/model_viz` wall time:** 34 passed in 17.5 s.
**Oracle/view disagreements and resolutions:** none. The literal anchors hold: 35 all collapsed, 140 all expanded, and the oracle's two-way pairs equal exactly the spec's four.
**Issues:**
- All tests passed on the first run, so "see them fail for the right reason" was not observed. To prove the tests can fail, two deliberate mutations of `view.js` were run and reverted: dropping the self-loop skip failed 3 of 7 edge tests (all collapsed, both round trips); swapping edge direction failed 5 of 7. `view.js` was restored byte-identical (checked with `git diff --no-index`).
- The first model_viz run may have overlapped the tail of the orchestrator's baseline run. model_viz does not touch `.integration_workspace` and did not exist when the baseline collected, so the baseline is unaffected.
**Deviations:**
- **Order of work:** the viewer code was written before the tests in this phase rather than strictly after (mutation check above stands in for the red run).
- **New helper module `tests/model_viz/viewer_harness.py`** (not in design § Component Overview). `tests/` has five other `conftest.py` files, so tests cannot `from conftest import …` unambiguously; page helpers live in a uniquely named module and `conftest.py` holds fixtures only.
- **Model shape additions:** `Calc.hasExpressionIr` (D7's "no `expression_ir`" branch needs presence, separate from `derivedFormula === null` for an unprintable tree); `Calc.undeclaredOutputIds` (so the producer's panel can list undeclared-output rows without a second pass); `Binding.outputDeclared`; `Model.bindingById`; `Input.kind` may be `"unknown"` with `rawKind` (Appendix C last row); literal/default/parameter inputs carry `hasValue`.
- **Appendix C gaps decided here:** a duplicate calc `node_id` is a load error (keys would collide); an occurrence whose `parent_id` names a missing occurrence, or a parent cycle, is a load error (containers cannot nest); `occurrence_id` missing is a load error, a missing `display_segment` is labelled "segment not recorded"; a present `calc_expressions` that is not a list of strings is a load error (it cannot render verbatim); `source_line` that is not an integer is labelled "not recorded".
- **Selection mechanism:** every element is added with `selectable: false`; `graph.selectCalc` briefly `selectify`s, selects, then `unselectify`s. This keeps Cytoscape's own tap and background-tap handling from changing the selection behind `app.js`, while `cy.nodes(':selected')` still reports the app's selection.
- **`member_count`** counts all calcs beneath a container (in occurrence mode, descendants included), so a collapsed ancestor's label shows everything it hides.

### Phase 2 Completion
**Completed:** 2026-09-13
**Actual Changes:**
- `js/panel.js` — `renderPanel(panelElement, model, key, onCalcLink)` builds header (name, full group path), Location (`source_file:source_line`, first 12 hex of the file SHA-256 with the full hash as `title`), Formula (D7 list with `.formula-text` / `.formula-note` children; derived block with the spec label), Documentation (or `data-doc-absent` label), Inputs (one row renderer per kind, plus `unknown`), Outputs (declared outputs with consumer links, then undeclared-output rows). `textContent` only, through one small `el()` helper that refuses unknown properties. `renderPlaceholder`, `renderMissingCalc` (panel-level warning for an unknown key, used by Phase 3).
- `js/app.js` — `showCalc(key)` (sets `selected`, selects and highlights in `cy` when drawn, renders the panel; throws on a key not in the model). `navigateTo(key)` was written here too because panel links call it; its tests are Phase 3.
- `js/graph.js` — `clearSelection()` split out of `selectCalc`.
- `viewer.css` — link underline offset so underscores in calc names stay visible.
- `tests/model_viz/panel_dom.py` (NEW) — `panel_dump(page)` reads the rendered panel's DOM hooks and `textContent` into plain data in one `page.evaluate`.
- `tests/model_viz/test_panel.py` (NEW) — module fixture `panels` shows all 76 calcs once on `loaded_fixture_page` (PD2) and dumps each; `test_panel_sections`, `test_formula_entries_verbatim`, `test_calendar_note`, `test_derived_formulas` (exact string against an independent Python printer, plus reference order), `test_input_kinds_and_totals`, `test_bindings_both_directions` (multisets), `test_output_consumers`, `test_location_and_hash`.
- Result: `tests/model_viz` 42 passed in 19.5 s. Red run first: every panel test errored with `showCalc is not a function`. Mutation check: rendering only the first consumer of each port failed `test_bindings_both_directions` and `test_output_consumers`; reverted, `cmp` identical.
- Manual check: screenshots of `total_capital` and `fuel_handling` panels (`/tmp/mv_panel_*.png`, not kept). Sections readable, warnings styled, no raw HTML; the derived formula and the doc repeat both read correctly.
**New panel strings added (PD3):** section titles `Location`, `Formula`, `Documentation`, `Inputs (n)`, `Outputs (n)`; `file SHA-256 <12 hex>`; `source location not recorded`, `line not recorded`, `no source file recorded`; `No formula lines recorded for this calc.` (D7 wording, capitalised as a sentence); `repeats the documentation below`; `unresolved: the producer calc is not in this snapshot`; `undeclared output <id>`; `undeclared output: bound by a consumer but not declared on this calc`; `attribute name not recorded`; `no calc consumes this output`; placeholder `Select a calc in the graph to see its formula, documentation, inputs and outputs.`; missing key `No calc <key> in this snapshot; nothing to show.`
**Issues:**
- One test bug fixed: `test_calendar_note` compared calcs by identity across two separate fixture parses; it now compares `node_id`.
**Deviations:**
- `renderPanel` takes the panel element and the link callback as arguments (`renderPanel(panelElement, model, key, onCalcLink)`) instead of design's `renderPanel(model, key)`, so the shell holds no state of its own.
- The panel root hook is `[data-role=panel]` with `data-calc-node-id` (PD6); the plan's stencil wrote `[data-panel]`.
- Extra DOM hooks beyond the design and PD6: `[data-role=calc-name]`, `[data-role=location-text]`, `[data-role=file-hash]`, `[data-role=derived-formula]`, `data-output-name` on output rows, `data-attr-node-id` and `data-value` on parameter rows, `data-undeclared-output` on undeclared-output rows.
- The "repeats the documentation below" note renders before the entry's text (still a separate `.formula-note` child), so it is visible without scrolling past a long entry.
- When every formula entry is a doc repeat and an `expression_ir` exists, the derived block is shown above the list as well (D7 names only the no-IR case; showing the derived text here loses nothing). Not reached on the fixture.

### Phase 3 Completion
**Completed:** 2026-09-13
**Actual Changes:**
- `js/app.js` — `navigateTo(key)` per the navigation contract (chain from `containerTree`, open collapsed ones, rebuild only if something opened, `showCalc`, then `graph.focusCalc`: zoom `max(zoom, 1.0)` and centre, same tick); an unknown key clears the selection and shows `panel.renderMissingCalc`. Search box: `matchCalcs(model, query)` (exact case-insensitive first, else substring) and `runSearch()` on Enter and `change`; one match navigates, zero shows `no calc matches`, several show `N calcs match`. The `<datalist>` is filled with calc names on load and emptied on clear. Toolbar controls (buttons, search, mode select) are disabled until a snapshot loads and on every clear, so no button can call into an empty app.
- `tests/model_viz/test_navigation.py` (NEW) — `test_panel_link_navigation` (N1, real link clicks upstream then downstream from `total_capital`), `test_hidden_target_upstream`, `test_hidden_target_downstream` (N2; real canvas click on the start calc, real link click), `test_canvas_gestures` (three real `page.mouse.click`s: collapsed container centre expands; calc centre selects, shows the panel and leaves the container expanded; a container background point clear of every child's bounding box, and confirmed as hitting only the container, collapses it), `test_search_box`, `test_navigate_unknown_key`.
- Result: `tests/model_viz` 48 passed in 23.0 s; `test_navigation.py` run three times in a row: 6 passed each time (4.3–4.4 s).
**Pairs picked for hidden-target tests:** chosen in Python from the snapshot, not hardcoded. Upstream: the first cross-file binding in snapshot order, consumer `cas90_1cfe_calc` (`mfe_account_costs.sysml`, input `overnight_cost`) ← producer `overnight_capital` (`designs/generic_mfe/mfe_plant.sysml`). Downstream: the last cross-file binding, producer `supplementary` (`mfe_account_costs.sysml`) → consumer `total_capital` (`mfe_plant.sysml`, input `supplementary_capital`). Canvas gestures use `mfe_magnet_field.sysml` (7 calcs).
**Issues:**
- `navigateTo` and the link callbacks came with Phase 2 code, so only the search test was red before its code (`panel_node_id` was `None` after Enter).
- Tap-bubbling mutation check. A first mutation (a delegated `cy.on("tap", "node[kind='container']", …)` handler) was not caught, and a probe showed why: in Cytoscape 3.28.1 a delegated selector handler does not fire for a bubbled calc tap, so that mutation is not the bug. The real bug shape is a handler bound on the container elements themselves, which does receive the calc's tap (probe: `direct-on-container` fired with target `c3`). Mutating `render` to bind that way failed `test_canvas_gestures` and `test_hidden_target_upstream`; `graph.js` restored, `cmp` identical.
- The background-point search in `test_canvas_gestures` calls `cy.renderer().findNearestElements`, an undocumented renderer method in the vendored 3.28.1, to confirm the chosen point hits the container and not an edge crossing it. The test asserts it finds a point, so a library change fails loudly rather than skipping.
**Deviations:**
- None to the navigation contract. The design does not mention disabling toolbar controls before a load; added so the buttons cannot throw into the console with no snapshot.

### Phase 4 Completion
**Completed:** 2026-09-13
**Actual Changes:**
- `js/app.js` — `setMode(mode)` (rebuild the tree for the mode, collapse all per D5, keep selection and panel) wired to the mode select's `change`; exposed on `modelVizApp`. The initial `state.mode` reads the select's value.
- `js/model.js`, `js/panel.js` — no change needed: the Appendix C checks (with calc and input indices), unresolved rows, undeclared-output rows and the unknown-kind row were built in Phases 1–2 and are now under test.
- `tests/model_viz/viewer_snapshots.py` (NEW) — `write`, `write_bytes`, `wrong_version`, `no_version`, `no_calcs_list`, `calc_without_node_id`, `non_json_bytes`, `renamed`, `consumers_of`, `remove_most_consumed_calc`, `unrenderable_tree`, `undeclared_output_and_unknown_kind`, `overlay` (with its own structural asserts before returning), `occurrence_chain`.
- `tests/model_viz/test_loading.py` — added `test_wrong_version_rejected` (L2), `test_not_a_snapshot_rejected` (L3), `test_non_json_rejected` (L4), `test_second_load_replaces_first` (L5: labels, datalist and panel links all `renamed_`; panel starts empty), `test_bad_load_after_good_clears` (L5, I6), `test_same_file_repick_reloads` (seq 1 then 2), plus `test_v3_without_calcs_rejected` and `test_missing_calc_field_names_itself` (Appendix C).
- `tests/model_viz/test_panel.py` — added `test_unrenderable_tree_synthetic` (P3 synthetic part, per-test page).
- `tests/model_viz/test_guards.py` (NEW) — `test_unresolvable_producer` (U1: 75 calc nodes; drawn edges equal the oracle on the reduced snapshot; every consumer row marked unresolved with a visible warning and the raw target), `test_overlay_occurrence_grouping` (U2: select `Occurrence` → only the root box; Expand all → every calc's `parent` chain in `cy` equals its occurrence and ancestors from the snapshot; one container per `occurrence_id`; the two `twin` siblings are distinct containers; the split file lands in both; I5 fields on every calc node; back to `Source file` → 17 collapsed groups), and `test_undeclared_output_and_unknown_input_kind`.
- Result: `tests/model_viz` 60 passed in 28.8 s. Fixture unchanged (`git status` clean for the file; SHA-256 still `c9f6e2a5…ce393`).
- Synthetic picks on the fixture: removed calc `pb` (24 distinct consumer calcs, 27 bindings); unrenderable tree `reactor_equipment_subtotal`; undeclared output on `cas90_1cfe_calc.crf` ← `cas71_calc`; unknown kind on `fuel_handling.ref_power`; overlay splits `mfe_magnet_cost.sysml` 3 / 2 across the twins.
**Issues:**
- Only the overlay test was red before its code (`setMode` missing: 17 source boxes instead of one root). The error-load, replace-on-reload and guard tests passed on first run because their code landed in Phases 1–2. Mutation checks stand in for red runs: skipping `clearLoaded()` at the start of a load failed `test_second_load_replaces_first` and `test_bad_load_after_good_clears`; giving the two `twin` occurrences one container id failed `test_overlay_occurrence_grouping`. Both reverted, `cmp` identical.
**Deviations:**
- Tests added beyond the plan: `test_v3_without_calcs_rejected`, `test_missing_calc_field_names_itself`, `test_undeclared_output_and_unknown_input_kind`, so the Appendix C paths and the undeclared-output and unknown-kind panel rows are not untested code.
- The plan says the removed calc has "the most consumers"; the builder counts distinct consumer calcs (24 for `pb`), which on the fixture picks the same calc as counting bindings (27).

### Phase 5 Completion
**Completed:** 2026-09-13
**Actual Changes:**
- `src/model_viz/README.md` (NEW) — how to open the viewer, how to use it, what it reads and does not show (pointing to spec § Non-Goals), file map (pure vs shell), test prerequisites (`uv sync --extra e2e`, `uv run playwright install chromium`), the fixture hash check and what to do when codegen regenerates the fixture.
- `.project/active/model-viz/evidence/manual_walk.py`, `manual_walk.md`, and screenshots `01_all_collapsed.png` … `05_all_expanded.png`.
- `.project/active/model-viz/evidence/pytest_full_after.log`, `pytest_failures_after.txt`, `pytest_errors_after.txt`, `pytest_new_failures.txt` (empty).
- Removed three unused exports (`ModelViz.model.EXPECTED_VERSION`, `ModelViz.panel.DERIVED_LABEL`, `ModelViz.view.MODES`); `tests/model_viz` re-run: 60 passed in 31.0 s.
**Manual walk findings (B3/B4/B5):** details in `evidence/manual_walk.md`.
- B3 held: the 17 collapsed boxes and 35 edges read at a glance; thick edges and the four two-way pairs (two curves, two arrowheads) are visible without zooming.
- B4 held: no group boxes overlap on this fixture (checked by bounding box in `cy`), but the all-expanded view has oversized sparse groups (`mfe_power_balance` holds 2 calcs in a large box) and many edges crossing boxes; calc labels are unreadable at the fit zoom. The edge tests pass in every collapse state, so the cost is readability only.
- B5 held with a caveat for the owner: after opening a group or navigating, every box moves, but the opened group or the centred, highlighted target anchors the eye. After a plain toggle there is no highlight, so several toggles in a row mean re-finding one's place each time. No architecture change in this item.
- Cosmetic, not fixed: in `04` the collapsed `mfe_primary_loop (1)` box sits on the `mfe_power_balance` group label; small group labels (`mfe_fuel_cycle`, `mfe_divertor_heat`) nearly touch in the expanded view.
**Regression diff result:** after-run `132 failed, 973 passed, 151 skipped, 20 errors in 407.46s`, `exit 1`; baseline `132 failed, 913 passed, 151 skipped, 20 errors`. The 60 extra passes are the model_viz tests. `FAILED` ids: after-list equals the baseline list exactly (`comm`: 0 new, 0 gone); `pytest_new_failures.txt` is empty. `ERROR` ids could not be diffed by id because the baseline was captured with `-rf` (Phase 0 note); the count is unchanged at 20, all in `tests/test_codegen_teax_acceptance.py` (6) and `tests/test_occurrence_mutation_teax.py` (14), which model_viz does not touch. No `tests/model_viz` id appears in either after-list. Same invocation as the baseline (`.env` sourced, `timeout 3000`, `-q -p no:cacheprovider --no-header`), with `-rfE` added.
**Quality pass:** `ruff check` and `ruff format --check` clean on `tests/model_viz` and `manual_walk.py`. I8 grep: the only hits in `model.js`, `formula.js`, `view.js` are the `window.ModelViz = window.ModelViz || {}` lines. No `innerHTML` in `viewer/js/`. No `http(s)://` in the viewer outside `vendor/`. No `TODO`, `FIXME`, `skip` or `xfail` in `src/model_viz` or `tests/model_viz` outside the vendored dagre file. Line counts: `model.js` 298, `panel.js` 233, `app.js` 194, `view.js` 171, `graph.js` 148, `formula.js` 45; all under 400. Every row of the Spec Criterion → Test Map has a passing test; `spec.md` was not edited (plan instruction).
**Issues:**
- The first after-run was started with a plain background Bash and did not survive: the wrapper was reported complete while its pytest child kept running with stdout on a deleted file, leaving a 97-byte log. That child was stopped by PID and the suite was relaunched with `setsid nohup` and polled in short foreground loops (auto-memory gotcha "one battery at a time"). Only the relaunched run is recorded. Before both runs, the one other pytest seen on the machine belonged to a different checkout (`fusion-tea-codex-test`); `.integration_workspace` is per checkout (`tests/study/conftest.py:309`), and none was running when the relaunch started.
- The walk used `fuel_handling` instead of the plan's example `cas22_capital`, because `cas22_capital` sits in `mfe_plant.sysml`, which is still collapsed at that step and cannot be clicked on the canvas. The script now refuses to click an element that is not drawn.
**Deviations:**
- `.project/CURRENT_WORK.md` and `spec.md` status were not updated. `CURRENT_WORK.md` already has uncommitted owner-side changes and the orchestrator commits per phase; the plan says not to edit the spec here. The orchestrator's close stage owns both.

### Post-audit fixes
**Completed:** 2026-09-13, from `audit.md` (certified, four non-blocking findings) and the resume brief. Only `src/model_viz/`, `tests/model_viz/`, this plan and the spec's metadata were touched.

1. **Null calc entry crashed the load** (`audit.md` § Code integrity). `buildModel` now checks that every `graph.calcs` entry is an object before any pass reads a field, and throws the `SnapshotError` "Calc entry N is not an object." (`src/model_viz/viewer/js/model.js`, start of `buildModel`); the later per-calc record check it made redundant was removed. Test: `test_loading.py::test_null_calc_entry_rejected` (a `null` at `calcs[5]`; banner names it; nothing drawn). Mutation: removing the check makes the load throw a `TypeError`, the seq never bumps, and the test fails with the page error, which is the failure the audit described.
2. **Doc-repeat note on every matching entry** (audit-F3, D7). `panel.js` `formulaSection` now tests only the last entry; the `calendar` case becomes "exactly one entry, and it repeats". Tests: `test_formula_entries_verbatim` now also asserts no earlier entry carries the note on the 65 fixture calcs; new `test_panel.py::test_doc_repeat_note_on_last_entry_only` on a synthetic copy (`viewer_snapshots.earlier_entry_ends_with_doc`) where entry 0 of the first multi-entry calc also ends with the doc comment: every entry verbatim, notes `[False, …, True]`, no "No formula lines recorded" note. Mutation: the old every-entry rule fails the new test.
3. **I2/I3 pure-layer test overclaimed.** `test_pure_layer.py::test_view_every_binding_on_exactly_one_edge_or_none` now compares, for every collapse subset in both modes, the drawn edge map `{(source, target): bindings}` with a map computed in Python from `SMALL` (`small_representative`, `small_expected_edges`; container ids written out by hand). Bindings are identified by `(consumer, input name)`, so two bindings between the same calcs cannot merge. Equality gives I3 (every binding with distinct representatives is on exactly one edge, others on none) and I2 (every edge's bindings map back to its ends); it also asserts no duplicate edge ends, no empty binding list, no binding listed twice. Mutation: dropping one binding in `view.js` fails it.
   - **Occurrence mode under the UI oracle, added** (it was cheap): `edge_oracle.expected_occurrence_edges(snap, collapsed_occurrences)` and `test_guards.py::test_overlay_occurrence_edges_under_collapse`. On the overlay snapshot, occurrence mode, all expanded, it steps collapse twin_a → collapse twin_b → collapse plant (twins still collapsed underneath) → expand plant → expand twin_a → expand twin_b → collapse root → expand root, and after each step the edges read from `cy` equal the oracle for the test's own collapsed set; the end equals the start. Mutation: taking the innermost instead of the outermost collapsed container fails it.
4. **Tidy-ups** (`graph.js`). The `selectCalc` comment moved from above `clearSelection` to `selectCalc`, reworded to what the function does; `selectCalc` no longer returns a value (no caller used it).
5. **Lens addition audit-F1.** The Formula section now opens with a muted line, `data-role=formula-provenance`: "Lines reconstructed by codegen from the parsed model; not verbatim source text." `test_panel_sections` asserts that exact text on all 76 panels (`panel_dom.py` reads it).
6. **Lens addition audit-F2.** Decidable from the snapshot: an attribute fed by a calc is recorded as an alias (`is_alias: true`) whose `alias_target` is `{kind: "producer", target: {calculation, output}}`. The fixture has 69 such attributes, and all 234 parameter inputs target non-alias attributes (219 `occurrence_override`, 15 `definition_default`, all with values). New `test_graph_edges.py::test_no_calc_output_reaches_a_calc_through_an_attribute` asserts this against the raw snapshot, with a docstring explaining why the viewer would draw no edge for such a link (the consumer's input is a `node` edge to the attribute, not a `producer` edge). It depends on `fixture_path`, so the hash check runs first. `src/model_viz/README.md` gains a "Re-probe these premises too" list naming this check.

**Spec metadata:** `spec.md` Status now reads "Certified 2026-09-13 (audit.md)"; Related Artifacts' design link no longer says "to be created", and the audit is linked.

**Result:** `uv run python -m pytest tests/model_viz -q` → 64 passed in 31.3 s (60 before; +4: null calc entry, last-entry-only note, occurrence edges under collapse, attribute premise). `ruff check` and `ruff format --check` clean. Every mutation above was reverted and the source file compared byte-identical with `cmp`.

**Deviations:** none from the design. The two helpers added for item 3 (`expected_occurrence_edges` in `edge_oracle.py`, `toggle_occurrence` in `test_guards.py`) keep the rule that the oracle's collapse state comes from the test; `cy` is read only to find a container id.

---

**Status:** Draft → In Progress → Complete
**Next step:** `/_my_implement` from Phase 0; `/_my_audit` after Phase 5.
