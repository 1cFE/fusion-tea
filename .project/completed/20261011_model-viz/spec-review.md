# Spec Review: Model Visualization — Calc DAG Viewer

**Spec:** `.project/active/model-viz/spec.md`
**Contract:** `~/.claude/commands/_my_spec.md`
**Review File:** `.project/active/model-viz/spec-review.md`
**Date:** 2026-09-13
**Reviewer context:** Fresh session, non-interactive stage run. No owner present. Where a finding would ask the owner, it states the question and a recommended answer for the orchestrator to rule on. All review judgments are `[AGENT]`.

---

## Reality Check

**Sound.** The spec is about the right work item: a read-only calc graph viewer with a detail panel, reading the codegen snapshot in the browser. The Problem section is accurate, and every fixture count I checked is correct (table below). The core requirements follow the owner's words and the reviewed concept design. The problems are in precision, not direction: four success criteria can be argued past as written, one criterion contradicts orchestrator ruling 2, and the owner-quote narrowing is parked as an open question when it has now been ruled on.

### Fixture verification

I ran read-only `uv run python` JSON probes against `exploration/stellarator_e2e/stellarator.snapshot.json`. The SHA-256 matches the spec (`c9f6e2a5…ce393`). Schema is `instance-graph/v3`.

| Spec claim | Probe result |
|---|---|
| 76 calcs at `instance_graph.graph.calcs`, `node_id` a string | 76, string. Confirmed. |
| 17 source-file groups; largest `mfe_account_costs.sysml` with 33; `mfe_plant.sysml` 10, `stellarator_plant.sysml` 1 | Confirmed. 12 of the 17 groups hold a single calc. |
| Inputs: 150 producer, 234 node, 10 literal, 52 null | Confirmed. |
| 140 distinct calc pairs | Confirmed. |
| 35 directed group pairs, 4 bidirectional (the four named) | Confirmed: 35 directed cross-group pairs; bidirectional pairs are account-costs↔mfe_plant, plasma-scaling↔plasma-sustainment, magnet-field↔plasma-scaling, power-balance↔primary-loop. 5 groups also have intra-group edges. |
| 64 of 155 output ports have no calc consumer | Confirmed. Every consumed `(calculation, output)` pair matches a declared output port (0 orphans). `port.calculation` equals the owning calc's `node_id` for all outputs. |
| 150/150 producer targets match a calc; 234/234 node targets match an attr | Confirmed. |
| 11 empty `calc_expressions` lists, no doc comment on those 11 | Confirmed (all 11 have `doc_comment: null`); all 11 have a dict `expression_ir`. |
| 65 lists carry documentation text | Confirmed. |
| All 76 have `source_file` and `source_line` | Confirmed. |
| All 76 scope to root `stellaris`; 13 subsystem occurrences own none | Confirmed: 14 occurrences, `scope.wire` of all 76 equals the root's `occurrence_id`. All 14 `display_segment` values are distinct on the fixture. |
| `fuel_handling`: producer, parameter, literal `ref_power` = 1000.0; `fuel.s_per_fpy_in` default 31536000.0 | Confirmed. |
| No `node` binary; Python Playwright in venv; `scripts/browser_inspect.py` exists; no `src/` today | Confirmed. Playwright 1.58.0 with Chromium installed. |

Extra facts found while probing, used in findings below:

- `calc_expressions` is not verbatim SysML. Codegen rebuilds each line from the parsed expression tree (`../sysml-codegen/src/sysml_codegen/extraction/extractor.py:147-150`) and appends the whole doc comment as the last entry (`extractor.py:175-180`). So on 65 calcs the panel will show the doc comment twice if it shows both sections.
- `source_file` is a snapshot-relative referent. `sources.roots` holds only `{kind: "directory", ordinal: 0}`, with no path. The same relative files exist in two trees on disk: `exploration/stellarator_e2e/models/` and `models/library/` + `models/designs/`. The snapshot records a SHA-256 per file in `sources.files`.
- The 11 formula-less calcs use a tiny expression vocabulary: operator `+` (35 nodes), operator `*` (4), feature references (47), literals (3).
- No hidden calc-to-attribute-to-calc flow on this fixture. All 234 node-edge targets hold static values (none null, none aliases), so drawing only producer edges misses no computation dependency here.

---

## Audit

Severity is marked on every finding. **Must-fix** items go back to the spec author before design. **Should-fix** items should be fixed in the same pass but do not block on their own. **Notes** are for the orchestrator or design and need no spec change unless the orchestrator says so.

### Lens 1 — Faithfulness

**L1-1 · Must-fix · Direct claim:** The owner-quote narrowing is honest but not recorded as a decision. Orchestrator ruling 1 has now settled it (agent-grade): v1 shows formula steps, doc comment, and source location; no verbatim SysML text and no Python view. The spec still carries this as an Open Question "for the owner or spec reviewer to confirm" (spec line 107), and spreads it across three places (Problem, an `[INFERRED]` requirement at line 86, and Open Questions). Non-Goals has a "Generated Python view" entry but no entry for verbatim SysML source text, and its Python reason ("the snapshot carries no path") differs from the ruling's reason (loading the model source tree would be a second data source, which the owner's data-source decision excludes). What needs to be true: the narrowing lives in one home as a decision record, graded `[AGENT]` and attributed to the orchestrator ruling, with the ruling's reason, covering both SysML source text and Python. It should also say plainly what the formula steps are: codegen's reconstruction of the calc's expressions from the parsed model (`extractor.py:147-150`), not the source text, with the doc comment appended as the final entry. Ruling 1's own wording ("the SysML expression text codegen extracted") is close but slightly overstates it; "reconstructed" is the exact word.

**L1-2 · Should-fix · Direct claim:** The `[INFERRED]` requirement at spec line 86 says the source location "is how the modeler reaches the actual SysML." That overstates what the location gives. `source_file` reads `root-0/analyses/mfe_account_costs.sysml`, and the snapshot never says what `root-0` is (`sources.roots` has an ordinal and no path). The same relative path exists in both `exploration/stellarator_e2e/models/` and `models/library/`, which may differ. A modeler following the location can open the wrong copy. What needs to be true: the spec describes the location as a snapshot-relative referent and does not promise it resolves to a file. Whether to show the per-file SHA-256 or a root hint is a design question and belongs in Open Questions.

**L1-3 · Should-fix · Rewrite request:** The `[NEED]` at spec line 84 ("Selecting a calc shows its implementation: its formula steps and documentation") cites the verbatim owner quote as its authority. The quote asks for "the actual SysML or python representation," which is not what the requirement states. The owner-grade source that actually says "formula, docs, and direct I/O" is the concept's Next-Stage Handoff (`[OWNER] v1 includes the detail panel with formula, docs, and direct I/O`). The `[NEED]` grade is right; the citation is wrong, and it makes the requirement look like a faithful restatement of the quote when it is the narrowed form. Point the citation at the handoff line and let L1-1's decision record carry the relationship to the quote.

**L1-4 · Should-fix · Question to the orchestrator:** The concept's owner-grade handoff line reads "Code lives at `src/model_viz/`. The existing structural view migrates in." The spec keeps the first sentence as `[NEED]` and defers the second to "a follow-on item," saying Success Criterion 4 and US-4 are "deferred to that item, not dropped." No such item exists. `.project/backlog/` has nothing for it, and `CURRENT_WORK.md` lists only `model-viz`. An owner-grade intent whose only home is a Non-Goal line in a spec that will be archived is at risk of being dropped in practice. **Question:** where is the structural-migration follow-on recorded? **Recommended answer:** the orchestrator registers it (a backlog line or a `CURRENT_WORK.md` entry naming the concept's Success Criterion 4 and US-4), and the spec's Non-Goal cites that location.

**L1-5 · Note:** The concept's Key Concept 3 described formula steps "rendered as syntax-highlighted math." The spec drops this without a line. That is consistent with the design review's m2 (do not present entries as more than the snapshot's text), and it was agent-grade, so no Non-Goal entry is required. Recorded so nobody reads the omission as an oversight.

**L1-6 · Note:** Provenance structure checks pass apart from L1-3. Every `[NEED]` traces to an `[OWNER]` or `[OWNER-VERBATIM]` item in the concept. The `[INHERITED]` overlay item cites its sources. The quoted owner words appear verbatim in the concept. The overlay grade conflict is surfaced, not resolved, as ruling 3 requires. Nothing is marked settled that is not owner-grade. No prohibition-shaped requirements.

### Lens 2 — Problem & Approach

**L2-1 · Note · Question to the orchestrator:** US-2 and US-3 start from a calc the modeler already has in mind ("the calcs I need to touch"). With groups collapsed and the calc's file unknown, the only way to find `cas22_capital` is to guess its group and expand boxes. Nothing in the concept asks for search, so this is not a dropped requirement. **Question:** should "find a calc by name" be a v1 outcome? **Recommended answer:** no requirement; add it to Open Questions as a usability question for design, since it is cheap to add and the concept's navigation stories lean on it.

**L2-2 · Note for design (feeds ruling 2):** The operator vocabulary of the 11 formula-less calcs is small and flat: only `+` and `*` operators, feature references, and literals. On the fixture that favours ruling 2's printer branch. The spec should not decide this; the evidence is recorded here so design does not re-probe.

**L2-3 · Note for design:** 12 of the 17 source-file groups contain exactly one calc. A collapsed singleton group is a box around one node. This affects how useful the collapsed overview is (the design's "17 labelled boxes" start state), not correctness. It belongs with the layout-quality question already deferred to the spike.

### Lens 3 — Pipeline Risk

**L3-1 · Must-fix · Direct claim:** The success criterion at spec line 46 requires the panel to show "No formula available." for all 11 formula-less calcs, and Open Question 1 (line 106) says "v1 follows the brief." Orchestrator ruling 2 now leaves this to design: if the expression-tree vocabulary is small enough, render a formula derived from the structure, labelled as such; otherwise show "No formula available." Either way the label must say the snapshot has no formula text. As written, the criterion would fail the printer branch, which L2-2's evidence makes the likely one. What needs to be true: the criterion holds under either design branch. It should require that the panel for each of the 11 visibly states the snapshot has no formula text, and that any formula shown is labelled as derived from the expression structure. Open Question 1 should record ruling 2 as the decision and hand the branch choice to design.

**L3-2 · Must-fix · Rewrite request:** The collapse criteria (spec lines 39-40) can be argued past. Three gaps:

- **No rule for mixed states.** The spec pins the edge set in only two states: everything collapsed (35 pairs) and before-and-after a round trip. Real use, and the hidden-target test, runs with some groups collapsed and others open. The expand-collapse extension draws substitute edges in exactly those states, and the design review asked for a check "during" collapse, not only after. What needs to be true: one rule that holds in every collapse state. For example, each producer binding is shown by a visible edge from the nearest visible container of its producer to the nearest visible container of its consumer, in the producer-to-consumer direction. The 35-pair count is then the all-collapsed instance of that rule, not the whole contract. (The concept's own phrase, "calc blocks render in the lowest parent which is viewed," is the same idea.)
- **Which groups, and in what order.** "Collapsing a group" does not say which group. A test on a singleton group with no edges passes trivially. What needs to be true: the round trip covers every group, plus at least one sequence that collapses and re-expands two connected groups in interleaved order, including a bidirectional pair.
- **Where edges are read from.** "Read from the page" is undefined. The graph draws to a canvas, so a test must query the renderer through JavaScript. If it reads the snapshot or the projection output, the round trip is true by construction and proves nothing. What needs to be true: edges are read from the set the renderer is currently displaying.

Two smaller ambiguities in the 35-pair criterion should be closed in the same edit: whether a collapsed group with internal edges may show a self-loop (5 groups have internal edges), and whether a bidirectional pair must be two directed edges or may be one edge with arrowheads at both ends. These are observable facts a test needs to know. Which to choose is the spec author's call; stating none leaves it to argument.

**L3-3 · Must-fix · Rewrite request:** The criterion at spec line 37 says all 150 bindings are "recoverable from the page (drawn or listed in the I/O panel)." The "or" lets the panel alone satisfy it, and it checks only one direction. The design's System Confidence claim 1 is that the forward edge set and the reverse output-consumer index agree. No criterion tests that; the output criterion (line 48) checks only the count of 64 unconsumed ports. What needs to be true: each of the 150 bindings appears in its consumer's panel as a producer input naming the upstream calc and port, and in its producer's panel as a consumer of that exact output port. Separately, every drawn calc-to-calc edge corresponds to at least one binding.

**L3-4 · Should-fix · Rewrite request:** The hidden-target criterion (spec line 50) describes order ("the group expands first, then the calc is selected") that a test cannot observe, and "centred" has no tolerance. It also does not say how the situation arises. What needs to be true: the criterion states the end state after the click. The target's group is expanded, the target is inside the viewport, the target is selected, and the panel shows the target. It should cover both an upstream and a downstream link whose target sits in a collapsed group while the current calc's group is open. The same tolerance point applies to "centres it in view" at line 49.

**L3-5 · Should-fix · Rewrite request:** "The page does not drop entries or present them as more than the snapshot's text" (spec line 45) has an untestable half. What needs to be true: an observable, such as each entry's text appears in the panel verbatim and in snapshot order. Separately, design should know the last entry repeats the doc comment (`extractor.py:175-180`), so showing both sections displays it twice. That belongs in Open Questions, not a requirement.

**L3-6 · Should-fix · Rewrite request:** The unresolvable-producer guard (spec line 54) says "one calc removed" without saying which. Removing a calc whose outputs no other calc consumes makes the test vacuous, because no input points at it. It also does not say that the graph draws no edge to the missing calc and that the rest of the graph still renders. What needs to be true: the removed calc has at least one consumer, every consumer shows the unresolved input with a warning, no edge points at a non-existent node, and the remaining 75 calcs render.

**L3-7 · Should-fix · Rewrite request:** The loading criteria cover a wrong schema version and a JSON file without a version. They do not cover a file that is not JSON at all (a PDF picked by mistake), or loading a second snapshot after a first. What needs to be true: a non-JSON file shows a clear error with no crash, and loading a second snapshot replaces the first rather than merging into it.

**L3-8 · Note:** Success criteria that name mechanisms: "file picker" (line 29), "group expands" for hidden targets (line 50), "centres" (line 49). Each traces to the reviewed concept design and is tagged or cited, so none is a smuggled invention. No criterion names a library, layout engine, or panel form. The "switching the viewer's grouping" step in the overlay criterion needs a switch reachable without editing code; how is correctly deferred (Open Question "Grouping-mode control").

**L3-9 · Note:** The spec never says whether `src/model_viz/` is a Python package. The concept described "a Python package with extractors, a local server, and an interactive frontend," while this spec delivers a static page and tests. The Python-package question falls under the deferred "File layout under `src/model_viz/`"; recorded so design answers it explicitly.

### Lens 4 — Hygiene

**L4-1 · Should-fix:** Related Artifacts says the product lens did not run because the instructions file was unreadable. It is readable in this session, and this review applies the lens (below). The ledger at `.project/active/model-viz/product-lens.md` still holds only the NOT RUN block. The orchestrator should append the block below (append-only) and update the pointer.

### Lens 5 — Reader Comprehension

**L5-1 · Note · Rewrite request:** The `[INHERITED]` overlay item (spec line 79) packs four things into one paragraph: the requirement, a "not a v1 visual feature" limit, the container keying rule, and the grade conflict. A tired reader has to re-read it to find the obligation. Splitting it into the requirement followed by the grade-conflict note would fix it. The rest of the spec reads cleanly.

---

## Product Lens

Applied in this session from `~/.claude/scripts/product-lens.md`. I read the spec before the sources, so this is not a clean oracle-first pass; the point below is derived from the owner's words, not from the spec's framing. Proposed ledger block for the orchestrator to append to `.project/active/model-viz/product-lens.md`:

```
## spec_review — 2026-09-13 — rev .project/active/model-viz/spec.md (uncommitted, on 82cdc9ec)
Point (re-derived): A modeler can see the I/O and behavioral relationships between calcs, and can open a calc block to see its actual SysML or Python representation.   [source: .project/concepts/model-viz.md § Owner's Words, grade: owner/HARD (OWNER-VERBATIM)]
Falsifier: A modeler clicks a calc and cannot see a representation of what it computes; or a real calc-to-calc dependency in the model has no visible edge.
Findings:
- spec_review-F1 [DO] The quote's "actual SysML or python representation" is narrowed to reconstructed expression text, doc comment, and a snapshot-relative location; the 11 formula-less calcs may show none. — concept Owner's Words (owner-verbatim) — disposition: DISPOSED on reviewer reading (see note); orchestrator ruling 1 records the narrowing; spec to record it per spec-review L1-1
- spec_review-F2 [DO] Behavioral relationships: only producer edges are drawn. On the fixture this misses nothing (234 node targets are static values), but a future calc→attribute→calc flow would be invisible. — concept Owner's Words (owner-verbatim) — disposition: no finding on this fixture; noted for design
- spec_review-F3 [can't-find] No durable product promise for the viewer in .project/product/ (INDEX lists only 0001, goal-round operability). — none — disposition: write the point down when the owner states the promise
Gate: DISPOSED (spec_review-F1, spec_review-F3)
```

**Note on F1, surfaced per capture-fidelity Law 4.** The lens rule says an owner-grade contradiction blocks. I do not read F1 as a contradiction. The owner asked for "SysML *or* python," and codegen's reconstructed expression lines are a SysML-syntax representation of the calc body for 65 calcs. The remaining 11 are labelled, and ruling 2 may give them a derived formula. If the orchestrator instead reads "actual" as the verbatim source text, F1 becomes a BLOCK that only the owner can clear. That reading choice is the orchestrator's to make, and the owner should see it at the next touchpoint either way.

---

## Engagement Summary

**Overall take:** The spec points at the right thing, is faithful to the owner's words, and every fixture fact in it is true. It is not yet a contract you could test against. The collapse and binding-coverage criteria each have an escape hatch, and one criterion contradicts ruling 2. The owner-quote narrowing is honest but still sits as an open question rather than a recorded decision.

**Here's what I need you to weigh in on:**

1. **[L3-2]** Require one visible-edge rule that holds in every collapse state, cover every group plus an interleaved two-group sequence in the round trip, and read edges from what the renderer displays. Recommended: send back as must-fix.
2. **[L3-3]** Replace "drawn or listed" with both directions: each binding in its consumer's panel and in its producer's output-consumer list. Recommended: must-fix.
3. **[L3-1, L2-2]** Rewrite the formula-less criterion so it holds under either branch of ruling 2. The fixture evidence favours the printer branch. Recommended: must-fix.
4. **[L1-1, L1-3, spec_review-F1]** Record the SysML/Python narrowing as an agent-grade decision in Non-Goals with ruling 1's reason, say formula lines are reconstructed rather than verbatim, and fix the `[NEED]` citation. Also decide whether you read F1 as narrowing (DISPOSED) or contradiction (BLOCK, owner needed). Recommended: must-fix for the spec edit; read F1 as DISPOSED.
5. **[L1-4]** Register the structural-migration follow-on somewhere durable before this spec's Non-Goal becomes its only home. Recommended: orchestrator registers it.
6. **[L1-2]** Stop calling the source location the route to "the actual SysML"; it is a snapshot-relative path that matches two trees on disk. Recommended: should-fix, with root disambiguation deferred to design.
7. **[L2-1]** Decide whether finding a calc by name belongs in Open Questions. Recommended: yes, as a design usability question, not a requirement.

---

## Resolutions

No owner was present. The orchestrator's rulings supplied with this review are recorded here as given; they are agent-grade.

- **Ruling 1 (owner-quote reach):** v1 shows formula steps, doc comment, and `source_file:source_line`; no verbatim SysML text and no Python view, because the snapshot carries neither and loading the source tree is a second data source. This review judges the narrowing honest but not clearly recorded; see L1-1 and L1-2.
- **Ruling 2 (11 formula-less calcs):** design decides between a labelled derived formula and "No formula available"; the label must say the snapshot has no formula text. The spec currently contradicts this; see L3-1.
- **Ruling 3 (overlay grade conflict):** stays surfaced, not resolved. The spec complies; see L1-6.

Findings awaiting orchestrator rulings: L1-4, L2-1, and the F1 reading.

---

**Verdict:** Revise
**Next Steps:** The orchestrator rules on the summary items and carries the must-fix findings (L1-1, L3-1, L3-2, L3-3) and the should-fix findings back to the spec author, who revises `spec.md`. The reviewer does not edit the spec. Append the product-lens block above to the ledger. After revision, a focused re-check of the four must-fix criteria is enough; a full re-review is not needed.
