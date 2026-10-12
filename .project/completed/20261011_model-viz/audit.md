# Audit: Model Visualization — Calc DAG Viewer

**Verdict:** Certify
**Audited:** 2026-09-13
**Branch:** feat/model-viz
**Commit:** 90cb8333 (working tree clean for `src/model_viz/` and `tests/model_viz/`)

---

## The Point

The stellarator model computes LCOE through 76 calcs wired together by 150 producer bindings. That wiring decides how a change to an input reaches LCOE, and nobody could see it. The only existing viewer (`proof_of_concept/extraction/`) draws part containment, which is filing, not computation. To learn what one calc does, a modeler had to find it in SysML and trace its bindings across about 16 files by hand.

The owner asked, `[OWNER-VERBATIM]` (concept § Owner's Words): "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation."

The owner-grade obligations (`[NEED]`, spec § Known Requirements):

- The data comes from the codegen snapshot read as JSON: no syside, no codegen Python, no re-derived bindings.
- The code lives at `src/model_viz/`.
- Selecting a calc shows its formula, its documentation and its direct I/O.
- The I/O is one hop: what feeds each input and which calcs consume each output.

v1 narrows "actual SysML or python" to codegen's reconstructed formula lines, the doc comment and the recorded source location (`[AGENT]`, orchestrator ruling 1, spec § Non-Goals). Goal rounds keep asking "which calcs are affected, what feeds them, what do they feed", and a wrong picture is worse than none. So the first duty is that every drawn edge is a real binding and every binding is findable, in every collapse state.

## Summary

The viewer delivers the point. I ran the 60 viewer tests myself (60 passed in 28.9 s), read every source and test file, and loaded the page in headless Chromium: no network requests, no console or page errors. Every spec success criterion has a test that drives the real page, and every edge assertion compares live Cytoscape edges with an independent Python oracle, never with the viewer's own projection. The findings are small: one malformed-input path crashes instead of showing the error banner, the doc-repeat note deviates from the orchestrator's "last entry only" ruling, one pure-layer test claims more than it checks, and one comment is misplaced.

## Product Judgment

**Is this the right piece of work? Yes.** A modeler can open the page from `file://`, pick a snapshot, see the calc graph grouped by source file, click any calc, and read its formula, doc, location and one-hop I/O with links to neighbours. The screenshots `evidence/audit_total_capital_derived.png` and `evidence/audit_fuel_handling_panel.png` (taken in this audit) show both panel shapes: a derived formula with its label and doc-absence warning, and a verbatim formula list with the doc repeat noted.

**Ledger gate: DISPOSED.** Every block in `product-lens.md` was scanned. The spec-stage NOT RUN entry is superseded by the spec_review pass. spec_review (F1–F3), design_review (F1–F3 and the fired DR-M3 smell) and this audit pass (F1–F3) are all dispositioned. No unresolved `BLOCK`. The item has no parent epic.

**Lens findings from this pass and their disposition:**

- **audit-F1** (panel heading says "Formula" without saying the lines are reconstructed). The narrowing is recorded under ruling 1 and the README states it (`src/model_viz/README.md:31`). Not blocking. Optional follow-up: a one-line muted note under the Formula heading, "reconstructed by codegen from the parsed model; not verbatim source."
- **audit-F2** (nothing guards the "no attribute-routed dependencies" premise after a fixture regeneration). The design records it as a Non-Goal (`design.md:218`), so v1 is honest on today's model. Not blocking. Recommended: add "every parameter input's attribute is a static value, not fed by a calc" to the re-probe list at `src/model_viz/README.md:60`, and assert it in `tests/model_viz/test_graph_edges.py:88`.
- **audit-F3** (doc-repeat note applies to every entry, not only the last). Recorded below as a design-conformance finding.

**Structural smells.** One fired, low: the doc-repeat note depends on codegen's internal habit of appending the doc comment into `calc_expressions` (`src/model_viz/viewer/js/formula.js:38-42`). I resolve it here, not just escalate it: the dependency touches only an annotation, never which entries render; the check does not depend on codegen's prefix wording; the upstream defect is filed as Finding 12 (`exploration/stellarator_e2e/CODEGEN_FINDINGS.md:68`); and when codegen is fixed the note simply never fires. No other smell fired. In particular, no test passes by construction: panel sweeps use `modelVizApp.showCalc`, which is the same function the canvas tap calls (`src/model_viz/viewer/js/graph.js:82-87`, `app.js:21`), and the real-click paths are covered separately.

## Findings

### Plan completion

All phases verified. Every plan checkbox was already ticked by the implementer; I checked each phase's deliverables against the code and the evidence, not against the notes.

- **Phase 0 validation is only half true.** The baseline was captured with `-rf`, so it lists the 132 `FAILED` ids and none of the 20 `ERROR` ids (`plan.md:530`). The checkbox "count matches failed + error" holds for failures only. Consequence: an `ERROR` id that changed while the count stayed at 20 would go unnoticed. I re-ran the diff: 132 failed ids before, 132 after, zero difference; `evidence/pytest_errors_after.txt` has 20 errors, all in `tests/test_codegen_teax_acceptance.py` and `tests/test_occurrence_mutation_teax.py`, none in `tests/model_viz`. I accept the residual risk as low.
- **Test-first was not followed in Phases 1, 2 (partly) and 4 (partly).** Code landed before or with its tests (`plan.md:553-556`, `:592`, `:610`). The implementer substituted mutation checks, which I could not re-run without editing code. Those checks cover the self-loop skip, edge direction, rendering only one consumer per port, tap bubbling, `clearLoaded`, and twin occurrence ids. They do not cover the verbatim formula comparison or the inside-the-pane check. Reading those tests, both compare against the raw snapshot and the pane geometry, so they can fail; I found no pass-by-construction path.
- **No placeholder code, TODOs, stubs, skips or xfails** in `src/model_viz/` or `tests/model_viz/` (grep; the vendored dagre file excluded). No spike scaffolding copied: nothing under `src/` or `tests/` references `spike/`.

### Spec conformance

**Loading**

- Picker load, no server: verified. `tests/model_viz/test_loading.py:20` loads through the real `<input type=file>` on a `file://` page; the per-page fixture fails any test that makes an `http(s)` request or logs an error (`tests/model_viz/viewer_harness.py:25-46`). My own load recorded zero non-`file:` requests.
- Wrong version names both: verified. `app.js:136-144` → `model.js:37-40`; `test_loading.py:32`.
- JSON with no version: verified. `model.js:32-35`; `test_loading.py:40`.
- Non-JSON: verified. `model.js:22-29`; `test_loading.py:47` with PDF bytes.
- Second load replaces first: verified. `app.js:119-129` clears model, graph, panel, banner, datalist and search before validating (I6); `test_loading.py:68` and `:98`.

**The graph**

- 76 calc nodes: verified. `test_graph_edges.py:53` compares the drawn `node_id` set with the snapshot.
- 17 groups, 33 in account costs, two design groups: verified. `model.js:95-117`; `test_graph_edges.py:62`.
- 140 pairs all expanded, producer to consumer: verified. `test_graph_edges.py:77` (sorted list equality with the oracle, length 140, unique ids, each pair a real binding).
- Non-producer inputs make no edge: verified. `view.js:154-158` iterates bindings only; `model.js:268`; `test_graph_edges.py:88`.
- All collapsed, 35 edges, four two-way pairs, no self-loops: verified. `view.js:158`; `test_graph_edges.py:113`, which also asserts the oracle's two-way pairs are exactly the spec's four.
- Round trip, every group: verified. `test_graph_edges.py:128`, all 17 groups, oracle equality while collapsed, list equality with the start after.
- Round trip, interleaved: verified. `test_graph_edges.py:141`; the test keeps its own collapsed set and never reads it from the page.

**The detail panel**

- Clicking a calc opens its panel with all five sections: verified. Real canvas click in `test_navigation.py:151` (step 2); sections for all 76 calcs in `test_panel.py:54`.
- 65 formula lists verbatim, in order; doc shown: verified. `panel.js:77` sets `textContent`; `test_panel.py:64` compares `.formula-text` with the snapshot entries.
- 11 derived formulas, label, doc-absence label, unrenderable fallback: verified. `formula.js:13-36`, `panel.js:56-65`; `test_panel.py:93` checks the exact string against an independent Python printer; `test_panel.py:212` covers the `/` synthetic copy.
- Four input kinds, the `fuel_handling` and `fuel` examples, totals 150/234/10/52: verified. `panel.js:149-159`; `test_panel.py:115`.
- Bindings both directions: verified. `test_panel.py:159` matches multisets, so a missing duplicate row fails.
- Outputs list consumers; 64 of 155 have none: verified. `panel.js:174-184`; `test_panel.py:178`.
- Navigation: verified. `app.js:45-60`, `graph.js:133-138`; `test_navigation.py:73` real-clicks an upstream link then a downstream link.
- Hidden-target navigation, both directions: verified. `test_navigation.py:93` and `:110`; start calc chosen by real canvas click, target group collapsed first, link clicked for real.

**Guards**

- Unresolvable producer: verified. `model.js:269-282` keeps the binding with `producer: null`; `panel.js:108-111` marks it; `test_guards.py:9` (75 calcs, oracle equality on the reduced snapshot, every consumer row unresolved with a visible warning).
- Overlay readiness: verified. `view.js:28-76` keys containers by `occurrence_id` and nests by `parent_id`; `test_guards.py:85` switches mode through the real select, checks every calc's parent chain, the same-segment twins, and the split file.

**Tagged requirements**

- `[NEED]` snapshot-only data: met. No fetch, no Python step; the page reads only the picked file.
- `[NEED]` code at `src/model_viz/`: met.
- `[NEED]` formula, docs, direct I/O: met (above).
- `[NEED]` one-hop I/O: met. The panel lists direct producers and direct consumers only.
- `[HARD]` snapshot shapes: honoured in `model.js:186-221`.
- `[HARD]` Playwright from pytest, no node: met.
- `[INFERRED]` items (standalone page, strict version check, producer-only edges, unresolved shown, full-path group identity, two grouping fields on every node, visible-edge rule, source location, derived-formula label, labelled absences, entries as text, input kinds): met. `view.js:122-136` carries `source_group` and `occurrence_id` on every calc node in both modes.
- `[INHERITED]` overlay readiness: met. The grade conflict the spec surfaced (owner vs agent grade) is still open; it does not change the obligation.

**Non-goals respected.** No verbatim SysML, no Python view, no multi-hop tracing, no export, no attribute or constraint nodes, no editing, no auto-refresh. The structural-view migration is not built and stays registered at `.project/backlog/BACKLOG.md:22`.

### Design conformance

Implementation follows the design, with these deviations. The first is undocumented; the rest are recorded in the plan's notes.

- **D7 note applies to every entry, not only the last (undocumented; lens audit-F3).** Design D7 and orchestrator ruling 1 on the design review (`briefs/design_revise.md:7`) say the note fires when *the last* entry ends with the doc comment. `src/model_viz/viewer/js/panel.js:70` tests every entry, and `:78` notes each one that matches. `tests/model_viz/test_panel.py:73` asserts only the last entry. Consequence: an earlier formula line that happened to end with the doc text would be labelled "repeats the documentation below" and no test would fail. Nothing on the fixture triggers it, and no entry is hidden either way. Fix: compute the flag for the last index only (the `calendar` all-repeats check then becomes "one entry, and it repeats"), and assert in `test_panel.py:64` that every earlier entry has `repeat` false.
- **Derived block also shown when every entry is a repeat and an IR exists** (`panel.js:72`, `plan.md:582`). D7 names only the no-IR case. Adds information, not reached on the fixture. Accept.
- **`renderPanel(panelElement, model, key, onCalcLink)`** instead of `renderPanel(model, key)` (`plan.md:578`). Keeps the shell stateless, which is what the design wanted. Accept.
- **New helper modules `viewer_harness.py` and `panel_dom.py`** not in the component list (`plan.md:557`, `:570`). Needed because `tests/` has several `conftest.py` files; names are unique across the tree. Accept.
- **Model and DOM additions** (`hasExpressionIr`, `undeclaredOutputIds`, `outputDeclared`, `bindingById`, `unknown` input kind; extra `data-role` hooks) and **Appendix C gaps decided in code** (duplicate `node_id`, missing or cyclic occurrence parents are load errors) (`plan.md:558-559`, `:580`). All consistent with Appendix C's principle "load error if the calc cannot be placed; label otherwise." Accept.
- **Selection by `selectify` / `unselectify`** around each select (`graph.js:108-130`, `plan.md:560`). Keeps Cytoscape's own tap handling from changing the selection behind the app. Accept.
- **Toolbar disabled until a snapshot loads** (`app.js:114-116`). Not in the design; prevents calls into an empty app. Accept.

**Invariants.**

- I1 (model immutable, no reading bindings back from live edges): holds. Nothing in `app.js` or `panel.js` reads edge data from `cy`.
- I2 and I3 (each edge's bindings non-empty and consistent; each binding on exactly one edge or none): hold by construction in `view.js:153-166`. UI-level completeness is proven by the oracle comparisons. See the test finding below.
- I4 (only producer inputs become bindings): holds, `model.js:268`.
- I5 (both grouping fields on every calc node): holds, `view.js:122-136`; asserted in `test_guards.py:100`.
- I6 (load clears first): holds, `app.js:137`.
- I7 (verbatim `textContent`, in order): holds, `panel.js:77`; the note is a separate element so the text stays clean. No `innerHTML` anywhere in `viewer/js/`.
- I8 (pure layer has no DOM or Cytoscape access): holds. The only `window` reference in `model.js`, `formula.js` and `view.js` is the namespace line. `model.js:253` calls `ModelViz.formula.printExpression`, which is another pure function.

**Engineering bar.** File layout matches design § Component Overview. Shells are thin (`graph.js` 148 lines, `panel.js` 233, `app.js` 194). The three vendored files match `VENDOR.md` hashes (`sha256sum`, run in this audit). The expand-collapse extension is not vendored, per D1. `ruff check` and `ruff format --check` on `tests/model_viz` are clean.

### Code integrity

- **A `null` entry in `graph.calcs` crashes the load instead of showing the banner.** `src/model_viz/viewer/js/model.js:226` calls `buildGroups`, which reads `raw.source_file` at `:99` before the per-calc record check at `:236` runs. Probed in this audit: `calcs: [null]` throws `TypeError: Cannot read properties of null`. `app.js:141` re-throws anything that is not a `SnapshotError`, so the change handler rejects: the page is already cleared, no banner appears, and `data-load-state` / `data-load-seq` do not update. Appendix C promises a named load error for a calc that is not a record. Codegen does not write such files, so the real-world risk is low, but it is a malformed-input path that fails silently to the modeler. Fix: validate that every `calcs[i]` is a record before `buildGroups` (or move the record check into `buildGroups`), and add the case to `tests/model_viz/test_loading.py` beside `test_missing_calc_field_names_itself`.
- **`test_view_every_binding_on_exactly_one_edge_or_none` checks less than its docstring claims.** `tests/model_viz/test_pure_layer.py:196-206` asserts that edges have bindings, that no binding is listed twice, and no self-loops. It does not assert that every binding with distinct representatives is listed (the "exactly one" half of I3), nor that a listed binding's representatives equal the edge's ends (the second half of I2). Bindings are also identified by (producer name, consumer name), so two bindings between the same calcs would merge. Consequence: in occurrence mode, where no UI oracle runs, a view bug that dropped a binding under some collapse state would pass. Fix: compute representatives in Python for each subset of the small snapshot and assert the edge map equals them, or rename the test to what it checks.
- **Misplaced comment and unused return value.** `src/model_viz/viewer/js/graph.js:106-107` describes `selectCalc` ("Mark one calc selected … Returns false when the calc is not on screen") but sits above `clearSelection`. The return value of `selectCalc` (`:129`) is never used by `app.js`. Fix: move the comment to `:116` and drop the return, or use it.
- **Canvas-gesture test uses an undocumented Cytoscape renderer method** (`tests/model_viz/test_navigation.py:138`, `cy.renderer().findNearestElements`). Recorded by the implementer (`plan.md:594`). It fails loudly if the library changes, so it is brittle, not dishonest. No change needed while the vendored version is pinned.

No god functions, parameter sprawl, policy in utilities, broad excepts, compatibility shims or optional parameters papering over data. `readSnapshot` catches only `SyntaxError` (`model.js:25`), and `loadText` catches only `SnapshotError` (`app.js:141`).

**Owner questions (no owner present; recommendations stated).**

1. **Readability caveats from the manual walk.** B4 held on correctness but calc labels are unreadable at the all-expanded fit zoom, and B5 held with a caveat: after a plain toggle, every box moves and nothing is highlighted, so repeated toggles mean re-finding one's place (`evidence/manual_walk.md`; `plan.md:624-626`). Question: accept this for v1, or treat position-preserving layout as a v1 need? Recommendation: accept for v1 and register "position-preserving layout (dagre seeded from prior positions or ELK)" beside the structural-view item in `.project/backlog/BACKLOG.md`. Correctness is proven; the design names this exact fallback, and it changes only `graph.render`.
2. **Overlay-readiness grade.** The spec's surfaced conflict (`spec.md:88`: `[OWNER]` in the handoff, `[AGENT]` in Owner's Words) is still open. Recommendation: owner confirms the grade at close; the delivered behaviour is the same either way.

---

## Certification

**Checked:**

- Ran `uv run python -m pytest tests/model_viz -q`: 60 passed in 28.9 s.
- Read every file in `src/model_viz/viewer/js/`, `index.html`, `viewer.css`, `README.md`, `VENDOR.md`, and every file in `tests/model_viz/`.
- Recomputed vendor SHA-256s: all three match `VENDOR.md`.
- Grepped the pure layer for `document`, `window` and `cy` (I8), the viewer for `innerHTML`, network URLs, TODOs and console calls, and the tests for skips.
- Loaded the fixture in headless Chromium through the picker: zero non-`file:` requests, zero console or page errors; two panel screenshots saved to `evidence/`.
- Probed the `calcs: [null]` case directly.
- Re-diffed the `FAILED` ids between the baseline and the after-run: 132 and 132, no difference.
- Ran `ruff check` and `ruff format --check` on `tests/model_viz`.
- Ran the product-lens as an independent subagent and scanned every ledger block.

**Marked:** all 22 success criteria in `spec.md` ticked. Plan checkboxes were already all ticked; left as they are, with the Phase 0 caveat above. `CURRENT_WORK.md` updated to "certified". No epic.

**Recommended before close (none blocks certification):** the `null`-calc load crash (`model.js:226`), the D7 last-entry deviation and its test (`panel.js:70`, `test_panel.py:73`), the I2/I3 test gap (`test_pure_layer.py:196`), the misplaced comment (`graph.js:106`), and audit-F2's re-probe guard (`README.md:60`). Stale spec metadata should also be refreshed at close: the status line still reads "Draft — revised after spec review" (`spec.md:3`), and Related Artifacts says the design is "to be created" (`spec.md:141`).

**Not checked:**

- I did not run the full `tests/` suite. I relied on the implementer's after-run log and re-diffed its `FAILED` ids. `ERROR` ids could not be diffed by id because the baseline has none.
- I did not re-run the implementer's mutation checks (that would mean editing code).
- Occurrence-mode edges under partial collapse are not compared with an independent oracle anywhere at UI level. The spec does not require it, and the pure-layer test only partly covers it (see Code integrity).
- Browsers other than headless Chromium 145, and opening the page by double-click in a desktop browser.
- Snapshots other than the stellarator fixture and its synthetic copies, and layout performance on models larger than 76 calcs (bet B1).
- Visual legibility beyond the two panel screenshots taken here; layout quality relies on the implementer's `evidence/manual_walk.md` and its five screenshots, which I did not re-review one by one.
- Keyboard accessibility and the tooltip text on container hover.
