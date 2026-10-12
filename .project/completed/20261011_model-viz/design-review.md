# Design Review: Model Visualization — Calc DAG Viewer

**Design:** `.project/active/model-viz/design.md` (committed at 022b0be4)
**Spec:** `.project/active/model-viz/spec.md` (revised after review)
**Review File:** `.project/active/model-viz/design-review.md`
**Date:** 2026-09-13
**Reviewer:** design_review stage subagent (fresh session, non-interactive; no owner present)

---

## The Point

The stellarator model computes LCOE through 76 calcs joined by 150 producer bindings, and nobody can see that wiring. The only existing viewer shows part containment, which is filing, not computation. The owner asked, `[OWNER-VERBATIM]`: "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation." The owner-grade `[NEED]` obligations: the data comes from the codegen snapshot read as JSON; the code lives at `src/model_viz/`; selecting a calc shows its formula, documentation and direct I/O; the I/O is one hop. v1 narrows "actual SysML or python" to codegen's reconstructed formula lines, the doc comment and the recorded source location (`[AGENT]`, orchestrator ruling 1, spec § Non-Goals).

The viewer serves goal rounds that ask "which calcs are affected, what feeds them, what do they feed." A wrong picture is worse than none. So every drawn edge must be a real binding, and every binding must be findable, in every collapse state.

## Fundamental Assessment

**Sound.** This is the right piece of work and the approach is simpler than the one the brief pointed at.

- **Right work.** The design delivers the owner's ask inside the recorded narrowing. It does not drift into the structural view, Python views or multi-hop tracing. The product lens (appended to `product-lens.md`, summarised in § Product Lens below) is carried into this judgment.
- **Right approach.** The brief listed the expand-collapse extension for vendoring and asked design to either split its two-way bundles or bundle per direction. The design instead drops the extension and computes the visible graph from collapse state with a pure function, then rebuilds Cytoscape (D1). I re-ran `spike/rebuild_check.py` today and got the design's numbers: 17 nodes / 35 edges all collapsed (39 ms), 50 / 103 with one group open, 93 / 140 all expanded (253 ms), and a hidden target present and centred after the rebuild, with no console errors. The extension's only remaining job would have been hiding children, and it mutates live edges, which is the source of both spike problems. Dropping it removes a library, three layers of hidden state and the endpoint-truth question in one move. I endorse the departure from brief constraint 2; its reason (offline, deterministic libraries) still holds for the three libraries kept.
- **Abstractions earn their place.** Three pure files (`model.js`, `formula.js`, `view.js`), two shells (`graph.js`, `panel.js`) and one app file. Each has a job a test can reach. None is a speculative layer.
- **Structural smell: "consumer compensates for a producer" — FIRED, low severity, escalated here.** Codegen's data model says `calc_expressions` holds "SysML calc expressions (preserved as-is)" (`../sysml-codegen/src/sysml_codegen/extraction/data_models.py:80`), yet the extractor appends the doc comment into that list (`extractor.py:175-180`). D7 detects the repeat by matching codegen's two private wording forms, `"\nDocumentation:\n"` and `"See documentation:\n"`. That is the viewer absorbing a producer defect, and the design calls it "refining brief constraint 6" instead of naming the defect. The damage is contained: every entry still renders verbatim, and a missed match only loses the "repeats the documentation" note. So it does not touch the architecture, and I do not recommend Rework. It becomes must-fix **DR-M3**: name the codegen defect, register it upstream, and stop coupling to codegen's wording. (Deviation recorded: the review command says a fired smell forces Rework. I judge that rule aimed at foundation-level smells; this one is confined to one cosmetic annotation. The orchestrator can overrule.)
- **Structural smell: "changes who owns an invariant without saying so" — not fired.** The visible-edge rule moves from the extension to the view function, and D1, I1–I3 and the ADR candidate all say so out loud.

The problems are in the test plan, one decision that leans on codegen's wording, and a few unstated rendering rules, not the architecture. Three must-fix items: two close test holes where a spec criterion could pass while the behaviour is wrong, and one escalates the fired smell.

---

## Dimensional Review

### 1. Spec Compliance

**Assessment:** Concerns

I walked every success criterion and requirement. All have a design element. Coverage table, abbreviated to the items with a gap:

| Spec item | Design element | Gap |
|---|---|---|
| Panel: "Clicking a calc node opens a panel" | D10, `graph.js` tap handler, `test_panel.py` | No test clicks a calc node. See **DR-M1**. |
| Round-trip, every group / interleaved: "no edge dropped, duplicated, or reversed" | D1, view rule, `test_graph_edges.py` | Set comparison cannot see a duplicate; oracle state source unstated. See **DR-M2**. |
| 11 formula-less calcs: "These 11 also have no doc comment; the panel labels that absence" | Test table only | No rendering rule for the missing-doc label. See **DR-S2**. |
| 65 non-empty lists, "every formula entry appears" | D7, I7 | `calendar` has one entry and it is only the doc repeat; the panel would show no formula line and no label saying so. See **DR-S3**. |
| Missing metadata is labelled, never hidden | Impl notes (parameter values), Risks (B2) | Which missing fields are load errors and which are labelled is contradictory. See **DR-S1**. |
| Navigation: target "lies fully inside the viewport" | Navigation contract steps 1–4 | Holds only if the graph pane's size is fixed before centring. See **DR-S4**. |

Everything else is covered concretely:

- **Loading (5 criteria).** Version check before any other read, four error texts, I6 clear-before-validate, `data-load-seq` for sequencing, no-network assertion.
- **Graph counts.** 76 nodes, 17 groups with design-file kinds (D8), 140 pairs all expanded, 35 all collapsed with the four two-way pairs as `A>B` and `B>A` keys, self-loops dropped at step 3 of the rule.
- **Visible-edge rule.** The view function's four steps are the spec's rule, including nested containers ("outermost collapsed container" is the nearest visible ancestor). It produces one edge per directed pair by construction of the key, so the brief's bundling problem does not arise.
- **Endpoint truth.** No live edge is ever mutated, and I1 forbids reading bindings back from `cy`. The panel and reverse index read the model only.
- **Panel.** Four input kinds with DOM hooks, bindings both directions through `data-producer-node-id` / `data-output-id` and `data-consumer-node-id` / `data-input-name`, 64 unconsumed outputs through `data-no-consumer`.
- **Hidden-target navigation.** The chain comes from `containerTree`, never `cy`; expand, rebuild, select, zoom, centre on one tick. The rebuild check reproduces this (`c65` absent before, selected and centred after).
- **Guards.** Removed-calc copy (most-consumed calc; on the fixture that is `pb`, 27 consumers) and overlay copy driven through the real `<select>`.
- **IR printer.** See Dimension 5; verified against the fixture.

Capture fidelity: the design carries the spec's grades. It challenges two agent-grade brief items (constraint 2's vendor list, constraint 6's byte-identical test) with recorded evidence, which is allowed. It does not harden any `[INFERRED]` item into something the owner never asked for. The owner quote is carried verbatim in The Point.

### 2. Pattern Consistency

**Assessment:** Pass

- Tests use `playwright.sync_api` directly, matching `scripts/browser_inspect.py` and the spike. Playwright 1.58.0 and Chromium are installed here.
- The namespace-package note (unique helper module names) matches `pyproject.toml` and the existing `tests/` tree.
- `src/model_viz/` is new, so there is no local pattern to break. D12 (not a Python package yet) is the right minimum.
- One convention question is open: whether a missing Playwright should fail the default `pytest` run. See **DR-S5**.

### 3. Abstraction Quality

**Assessment:** Pass, with one note

- The pure / shell / app split is the right cut, and I8 makes it checkable.
- `window.modelViz` (D13) is a test seam that also serves the UI. It is justified: 34 canvas-coordinate toggles would be slow and brittle.
- **Note DR-N1.** Two globals differ only by case: `window.ModelViz` (the namespace of pure functions, used by `test_pure_layer.py`) and `window.modelViz` (the app handle). A reader and a test author will confuse them. Rename one, for example `ModelViz` for the namespace and `modelVizApp` for the handle.
- **Note DR-N2.** D13's handle includes `showCalc`, which lets `test_panel.py` skip the canvas. That is fine for the 76-calc sweep, but it is why DR-M1 slipped through: every panel-opening path the tests exercise bypasses the calc tap.

### 4. Duplication Avoidance

**Assessment:** Pass

- Forward bindings and `consumersOf` are built in one pass from the same records, so they cannot drift.
- The Python oracle deliberately reimplements the visible-edge rule. That is intended independence, not duplication. Its one risk is a shared misreading of the rule in both languages; the literal fixture counts (35, 140, the four named two-way pairs, no self-loops) anchor against that, and the test table already names them. Keep those literal assertions alongside oracle equality.

### 5. Data Structure Clarity

**Assessment:** Concerns

The model and element shapes are explicit and typed. I probed the fixture for every shape the design asserts:

- **Confirmed.** 76 calcs with unique `display_name`. `scope.wire` matches an `occurrence_id` for all 76. 150 producer targets all match a declared `(port.calculation, port.output)`. `sources.files[]` carries `referent` and `sha256`. `default_value` present on all 52 defaulted inputs.
- **IR confirmed exactly.** `expression_ir` is null on all 65 calcs with a non-empty list and present on the 11 without. Nodes: 39 `operator` (35 `+`, 4 `*`, every one with exactly 2 operands), 47 `feature_ref` (none with an empty `source_name`; chains are already dotted, e.g. `magnet.capital_cost` with `chain_segments: ["magnet","capital_cost"]`), 3 `literal` (all `LiteralRational`: 0.5, 9400.0, 5.0). No other kind. The operator set in the design is exactly the one found.
- **Precedence case exists.** One `+` sits directly under a `*`, so the parenthesis rule is exercised on the fixture, not hypothetical. Good.
- **Doc repeat forms confirmed.** 64 lists end with `"\nDocumentation:\n" + doc`, 1 (`calendar`) is exactly `"See documentation:\n" + doc`, 0 byte-identical. The design's refinement of brief constraint 6 is correct.

Concerns:

- **DR-S1 — Missing-field policy is contradictory.** B2 says a missing field should become a load error "rather than guess." Potential Risks says the builder "labels anything unexpected in the panel instead of dropping it; schema drift beyond that is a load error." Neither names fields. Recommendation: list the fields whose absence is a load error (for example `node_id`, `display_name`, `inputs`, `outputs` on a calc; `graph.occurrences` when present-but-not-a-list) and the fields that are labelled when absent (`doc_comment`, `calc_expressions`, `expression_ir`, `source_file`, `source_line`, `scope`, attr `value`). One short table in Implementation Notes.
- **DR-N3 — Printer edge cases.** `String(literal.value)` prints `9400.0` as `9400` and would print a null value as `"null"`. The first is honest; state it. The second should return `null` for the tree. Also state that an operator with fewer than two operands returns `null`.
- **DR-N4 — Wording.** "The root occurrence is `stellaris`" names the `display_segment`. The `occurrence_id` is `[["c1525587-…",null]]`. A reader implementing keys from that sentence would key on the wrong field.
- **DR-N5 — One output feeds one consumer twice.** On the fixture, one `(consumer, producer, output)` triple occurs on two inputs. The DOM hooks handle it (`data-input-name` distinguishes the rows), but the panel test must match rows as a multiset, not a set, or it will pass with one row missing.

### 6. Route Safety

**Assessment:** Pass (not applicable in the usual sense)

No server and no routes. The equivalent surfaces are safe:

- Verbatim text renders through `textContent` with `pre-wrap`, never `innerHTML`. The doc comments contain `<` and `*`, so this matters.
- The page makes no network request, and a test asserts it.
- Navigation to a key not in the model shows a warning instead of doing nothing.
- **DR-N6 — Same-file reload.** A file input does not fire `change` when the same path is picked again. A modeler who reruns codegen and re-picks `stellarator.snapshot.json` sees nothing happen. Reset `input.value = ""` after reading. The spec's replace criterion uses a different file, so no test catches this.

### 7. Bets & Decisions Integrity

**Assessment:** Concerns (minor)

- **Stated bets are genuine.** B1 (rebuild speed) is measured and I reproduced it. B3 (collapsed start orients) and B4 (compound overlap is cosmetic) are claims about reality with named failure costs. B2 is honest but its "if false" conflicts with the Risks section (DR-S1).
- **Decisions name alternatives.** D1, D2, D4–D7, D10 and D13 each record what was rejected and why.
- **Hidden bets surfaced:**
  - **HB1. Cytoscape's `bezier` curve style draws `A>B` and `B>A` as two visibly separate curves.** The design asserts it; the rebuild check counted edges but did not look. The spike's unbundled screenshot supports it (arrowheads at both boxes), and the spike stylesheet sets `curve-style: bezier`. The design's own stylesheet section does not state the curve style, and Cytoscape's default is `haystack`, which draws no arrowheads. State `curve-style: bezier` in `graph.js`'s stylesheet as a fixed decision. Folded into **DR-S4**.
  - **HB2. A full re-layout with `fit: true` on every toggle does not disorient.** Every expand moves every box. The extension route would have done the same, so this is not a reason to change course, but it is a usability bet worth one line under Key Bets, with the manual check as its test.
  - **HB3. The panel is always laid out at 420 px.** If the panel appears only on selection, the graph pane changes width after Cytoscape measured it, and `cy.center` centres on a stale size. See **DR-S4**.

### 8. Reader Comprehension

**Assessment:** Pass

The Core Concept states the mental model before the mechanism: read, model, view, draw, and "collapse is just state." The visible-edge rule is four numbered plain steps. Decisions lead with the choice. A tired engineer can skim it once and know what to build. The only blocking wording is DR-N1 and DR-N4.

---

## Product Lens

The lens ran as a separate subagent against the design, with the repo's product statements and the concept's owner-verbatim text as sources. Its verdict block is appended to `.project/active/model-viz/product-lens.md`. Summary and disposition:

- **Point (re-derived by the lens).** A modeler sees the real I/O relationships between calcs and can open a calc to see its representation; data from the snapshot, no re-derived bindings, one-hop I/O. It matches the design's Point.
- **Falsifier.** In some collapse state, a drawn edge matches no producer binding, or a binding with distinct visible ends has no edge; or a click on a calc or on a link to a hidden calc gives no formula, doc and I/O view. DR-M1 and DR-M2 exist because the test plan could miss exactly this.
- **design_review-F1 [DO] — calc → attribute → calc flow is unaddressed.** The spec review left this for design (spec_review-F2). Only producer inputs become edges (I4). If a calc output ever reached another calc through an attribute, that dependency would be invisible. The fixture has no such case (the lens checked the 292 attrs' value sites). The design records nothing. Disposition: should-fix **DR-S6**.
- **design_review-F2 [DO] — the representation narrowing.** Already disposed as spec_review-F1 (orchestrator ruling 1); the design restates it. Nothing new.
- **design_review-F3 [can't-find] — no durable product promise for the viewer.** Carried from spec_review-F3. Disposition: record when the owner states the promise; not a design issue.
- **Smells.** "Consumer compensates for a producer" fired (D7), escalated as DR-M3. "Invariant owner changes silently" did not fire.
- **Gate:** DISPOSED, with DR-M3 and DR-S6 carrying the two open dispositions.

---

## Issues by Severity

Must-fix items go back to the design author. Should-fix items should be addressed in the same revision; each is small. Notes are the author's call.

### Critical (must-fix)

- **DR-M1 — No test clicks a calc node, and the design names the exact bug that would slip.** The spec's first panel criterion is "Clicking a calc node opens a panel." `test_panel.py` uses `modelViz.showCalc`, `test_navigation.py` clicks panel links, and the one canvas click in `test_graph_edges.py` is on a collapsed container. Implementation Notes warn that a calc tap bubbles to its compound parent and, unguarded, collapses the group. No test would catch that. **Fix:** add one test that expands a group, clicks a calc node at its rendered position (from `renderedBoundingBox` plus the pane's page offset), and asserts the panel shows that calc, the calc is selected, and its group is still expanded. (Dimension 1)
- **DR-M2 — The round-trip tests, as described, can pass while the behaviour is wrong.** Two holes. (a) "Displayed set equals the oracle" compares sets, so a duplicated edge is invisible, but the spec says "no edge dropped, duplicated, or reversed." (b) The design does not say where the oracle gets the collapse state. If the test reads each container's `collapsed` flag back from `cy` to feed the oracle, a toggle that collapses the wrong group passes, because the oracle follows the page. **Fix:** state in Validation Approach that (a) edge comparisons use sorted lists of `(source identity, target identity)` and assert the list length equals the number of distinct pairs, and (b) the oracle's collapse state comes from the test's own step list, keyed by group path, never from page data. Mapping a group path to a container id for the `toggleContainer` call may read `cy`; the oracle state may not. (Dimension 1, brief attack "test passing by construction")

- **DR-M3 — D7 couples the viewer to codegen's private wording to work around a codegen defect (fired smell).** Codegen promises `calc_expressions` "preserved as-is" (`data_models.py:80`) but appends the doc comment into it (`extractor.py:175-180`). D7 matches the two exact prefixes. If codegen changes a word, the note silently disappears, and nobody upstream learns the list is polluted. **Fix, in three parts:** (a) in D7, name this as a codegen defect, not a refinement of the brief; (b) have the orchestrator register an upstream follow-on (a separate doc field, or no doc in the list) in the coding backlog, and cite it from D7; (c) replace the prefix match with a wording-independent test, for example "the last entry ends with `doc_comment`" (the spec's `[HARD]` fact is that the final entry contains the doc comment), or drop the note entirely. Either option keeps every entry verbatim, so no spec criterion moves. I recommend the ends-with test: it keeps the helpful note and depends only on a fact the spec already records. (Stage 0 smell)

### Major (should-fix)

- **DR-S6 — Record the calc → attribute → calc gap (lens design_review-F1).** Add one line: either a Non-Goal ("dependencies routed through an attribute are not drawn; none exist on the fixture") or a Key Bet with its if-false. The spec review asked design to take this up and the design is silent. (Product lens)

- **DR-S1 — Missing-field policy.** Replace the B2 / Risks contradiction with one table: load-error fields versus labelled-when-absent fields. (Dimension 5)
- **DR-S2 — Missing-doc label has no rendering rule.** The spec requires the 11 calcs' absent doc comment to be labelled. Add the label text and where it renders (the Documentation section) to Implementation Notes, next to the parameter-value labels. (Dimension 1)
- **DR-S3 — `calendar` shows no formula and no reason.** Its only `calc_expressions` entry is the doc repeat, and `expression_ir` is null, because codegen filters expressions it cannot reconstruct (`extractor.py:147-155`). Under D7 the Formula section shows one entry marked "repeats the documentation below" and nothing else. Add a rule: when every entry is a doc repeat and there is no IR, the Formula section also says "no formula lines recorded for this calc" (wording is the author's). The entry still renders, so no spec criterion is lost. (Dimension 1)
- **DR-S4 — Pin the rendering facts that navigation and two-way edges depend on.** State in D9 or Implementation Notes that the panel is always laid out, empty until a selection, so the graph pane never changes size after Cytoscape starts; or call `cy.resize()` whenever it does. State `curve-style: bezier` in the stylesheet (HB1). Add HB2 as a Key Bet. (Dimension 7)
- **DR-S5 — Default test run without Playwright.** `tests/model_viz/` joins the default `pytest` run, but Playwright is an optional `e2e` extra, and a plain `uv sync` removes extras. The design fails with an install message rather than skipping. **Ruling needed.** Question: should a machine without the `e2e` extra get a failing default test run? Recommended answer: yes, keep the loud failure (a silent skip lets a green run hide an unexercised viewer), and have the README and the failure message both give the exact command, `uv sync --extra e2e && uv run playwright install chromium`. The alternative, moving Playwright into the `dev` dependency group, is also acceptable and removes the trap; the design author should pick one and record it. (Dimension 2)

### Minor (notes)

- **DR-N1 — `ModelViz` versus `modelViz`.** Rename one global. (Dimension 3)
- **DR-N2 — `showCalc` bypasses the canvas.** Keep it for the sweep; DR-M1 covers the gap. (Dimension 3)
- **DR-N3 — Printer edge cases.** A null literal value and an operator with fewer than two operands return `null`; note that `9400.0` prints as `9400`. (Dimension 5)
- **DR-N4 — "Root occurrence is `stellaris`."** Say `display_segment`; the id is the wire string. (Dimension 5)
- **DR-N5 — Multiset row matching in the panel test.** One output feeds one consumer on two inputs. (Dimension 5)
- **DR-N6 — Same-file re-pick does nothing.** Reset the file input's value after each read. (Dimension 6)
- **DR-N7 — Expanded-container click-to-collapse is untested.** D10's second gesture has no test. Low risk; one assertion could ride along with DR-M1's test.
- **DR-N8 — Brief constraint 2 and the version ruling are now partly moot.** `cytoscape-expand-collapse` 4.1.0 is not vendored. The orchestrator should treat D1 as superseding that line of the brief and the "Versions" ruling's fourth library, not as a violation.

---

## Recommendations

1. Add the calc-node canvas click test (DR-M1).
2. Rewrite the round-trip test description so duplicates are visible and the oracle's collapse state is independent of the page (DR-M2).
3. Name the codegen doc-append defect, register it upstream, and replace the prefix match with a wording-independent test (DR-M3).
4. Add one table for missing fields, and the two missing labels: absent doc comment and the `calendar` case (DR-S1, DR-S2, DR-S3).
5. Pin the always-present panel, `curve-style: bezier`, and the re-layout bet (DR-S4).
6. Record the Playwright-availability choice and the attribute-routed dependency gap (DR-S5, DR-S6).

---

## Resolutions

No owner was present. Open questions and recommended answers, for the orchestrator:

- **DR-S5.** Should the default test run fail without the `e2e` extra? Recommended: yes, fail loudly with the exact install command; or move Playwright to the `dev` group. Design author records the pick.
- **DR-M3 / fired smell.** Does a low-severity fired smell confined to one annotation force Rework, as the review command's rule reads? Recommended: no; Revise with DR-M3, and the orchestrator registers the upstream codegen follow-on.
- **DR-M3 (c).** Ends-with-doc test, or drop the note? Recommended: ends-with test.
- **DR-N8.** Does D1 supersede brief constraint 2's vendoring of the expand-collapse extension? Recommended: yes; the constraint's reason holds for the libraries kept, and the extension's behaviour is what the spike found wrong.

---

**Overall:** Revise (three small must-fix items: two test-plan holes and one escalated smell; architecture approved)
**Next Steps:** The orchestrator carries DR-M1 to DR-M3, plus the should-fix items, back to the design author, and registers the upstream codegen follow-on for DR-M3 (b). After the revision, a focused check of the three must-fix items is enough; a full re-review is not needed. Then `/_my_plan`. The reviewer does not edit the design.
