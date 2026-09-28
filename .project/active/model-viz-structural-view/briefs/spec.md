# Brief: spec stage — model-viz-structural-view

Sent by the orchestrator to `/_my_spec`. Provenance marks follow `claude-pack/rules/capture-fidelity.md`. Owner-grade items are quoted or path-cited; everything else is the orchestrator's call, recorded here so the spec can cite it.

## Work item

- Name: `model-viz-structural-view`. Folder: `.project/active/model-viz-structural-view/` (new; never touch `.project/active/model-viz/`, the closed v1 calc-graph item). Single standard-scale item, not an epic.
- Purpose: finish v1 of the model visualization concept. Concept Success Criterion 4 and User Story US-4 were deferred out of the calc-graph item and this item delivers them: the structural (part containment) view lives in `src/model_viz/` beside the calc graph view, and a modeler switches between "where numbers are filed" and "how numbers are computed" in one tool.
- Read in this order: `.project/concepts/model-viz.md` (owner words), `.project/concepts/model-viz-design.md` (reviewed concept design; § Goals bullet 4, § Switching to the structural view, § Next-Stage Handoff), `.project/active/model-viz/spec.md` § Non-Goals (the deferral record), `.project/active/model-viz/design.md` (the v1 viewer architecture you build on: § Architecture, D1, D12, D13, § Integration Strategy), `src/model_viz/README.md`, `proof_of_concept/README.md` and `proof_of_concept/extraction/types.py` (what the old view showed).
- Branch: `feat/integrated`. The v1 viewer is at `src/model_viz/viewer/` (six classic scripts on `window.ModelViz`, tests under `tests/model_viz/`, run with `uv run python -m pytest tests/model_viz -q`).
- The data: `exploration/stellarator_e2e/stellarator.snapshot.json` (`instance-graph/v3`; graph under `instance_graph.graph` with `occurrences`, `attrs`, `calcs`, `constraints`, `constraint_usages`). Probe it with a read-only `uv run python` JSON script when a count or field shape matters. Verify every count you state.

## What the owner decided (settled; do not relitigate)

- `[OWNER]` "Code lives at `src/model_viz/`. The existing structural view migrates in." (concept § Next-Stage Handoff). Success Criterion 4: the structural view "is served alongside the calc DAG view". US-4: "I can switch between the structural view (part containment) and the calc DAG view in the same tool."
- `[OWNER]` Data source for the calc graph is the codegen snapshot read as JSON. No syside, no codegen Python import (concept § Next-Stage Handoff).
- `[OWNER-VERBATIM]` "can you explain to me why we don't have any organization or structure of the models?" (concept § Owner's Words). The structural view is the answer to that question: it shows the part containment tree.
- `[OWNER]` Multi-hop path tracing is v2. `[OWNER]` The structural overlay (calcs inside subsystem containers) is an architecture requirement, not a v1 visual feature; v1 already ships it as the calc graph's "Occurrence" grouping mode.

## Orchestrator rulings (agent-grade; cite them as `[INFERRED]` with this brief as the source)

1. **Producer for the structural view is the snapshot, not syside. The FastAPI server and the syside extractor are not migrated; they stay in `proof_of_concept/` as reference.** The concept's literal words name the syside extractor (`src/model_viz/extractors/structural.py`), but that wording predates the finding that the snapshot carries the containment tree. Verified by the orchestrator on 2026-09-13: `occurrences` holds 23 records with `occurrence_id`, `parent_id`, `display_segment`, `containment_slot`, `effective_usage_id`, `effective_type_ids`, `occurrence_index`, `package_display`; tree is root `stellaris` → 18 subsystems → `blanket/first_wall`, `magnet/casing`, `magnet/coil`, `magnet/winding_pack`. Each attribute record carries `owner_qualified_name` (for example `mfe_radial_build_parts::'First Wall'`) and `scope.wire`, so a part's type name is recoverable from any attribute it owns, and per-part attribute values are in the file. `effective_type_ids` resolve to nothing in the snapshot. Multiplicity is not recorded anywhere and every `occurrence_index` is null (no multi-instance parts in this model). Tradeoff: keeping syside would buy multiplicity, which this model does not use, at the cost of a Python server, a second data source and a second serving model in one page. One data source, one page, no server is the cleaner design. The owner reaffirmed on 2026-09-13 that this is the orchestrator's call. Record this in the spec as a decision with the reason, and record "multiplicity is shown only if the snapshot ever records it" as a consequence, not a compensating requirement.
2. **Serving model is the v1 viewer's: one static page, snapshot picked through the file input, no server.** Same page shell, same file load, same detail panel pattern (v1 design § Integration Strategy says the structural view "can reuse `graph.js` and the panel pattern").
3. **The structural view is a second view in the same page, switched by a control.** Both views read the one loaded snapshot. Switching does not reload the file. How the switch looks is a design question.
4. **What the structural view must show that the calc graph's Occurrence mode does not** (the item's substance; the spec must state these as requirements): every part occurrence including those that own no calcs (verified: `magnet/casing`, `magnet/coil`, `magnet/winding_pack` own zero calcs and are absent from Occurrence mode); the containment tree as nested boxes or as parent→child edges; each part's type name where recoverable and "not recorded" where not; each part's attributes with values, units where recorded, and source location in a detail panel on part click. Calc nodes do not appear in the structural view (the POC excluded `ElementCategory.CALCULATION` too); the count of calcs a part owns may be shown as a number.
5. **Per-part costs:** the POC's `costs` field came from a separate `generate_costs` import that no longer applies. Cost attributes are ordinary attributes in the snapshot; the panel shows them with the rest. No special cost extraction.
6. **Expand and collapse in the structural view use the v1 mechanism** (v1 design D1: a pure function over a collapsed-id set, Cytoscape rebuilt from its output). The `cytoscape-expand-collapse` extension that `proof_of_concept/cytoscape_demo.html` uses stays rejected.
7. **Retirement of the POC:** `proof_of_concept/` stays in the repo for reference and is marked superseded in its README by this item. Its tests are not run by the project suite today; leave them as they are. Design decides whether anything from `proof_of_concept/extraction/types.py` is worth carrying as vocabulary.
8. **Package question (v1 design D12):** `src/model_viz/` stays without Python because this item adds none. State it as a consequence.
9. **Non-goals with reasons:** layout stability on toggle (backlog P3, separate); the occurrence-mode start state and the 33 root-level cost calcs (a modeling question owned by the structural-decomposition goal; belongs to a v2 concept revision); multiplicity (not in the snapshot); multi-hop tracing (owner, v2); constraint nodes; model editing; a server or syside path.
10. **Test environment facts:** no `node` on the machine; Python Playwright drives Chromium from the venv; tests run as `uv run python -m pytest tests/model_viz -q` (about 30 s); Chrome refuses ES modules on `file://`, so the viewer uses classic scripts on `window.ModelViz` with `window.modelVizApp` as the test handle. State acceptance criteria as observable page behaviour testable that way.

## What the spec must nail down

- Requirements graded `[HARD]` / `[NEED]` / `[INFERRED]` / `[INHERITED]` per capture-fidelity's absorb mapping. `[NEED]` only for the owner items above.
- The structural node and edge content (ruling 4), with counts for the stellarator snapshot verified by you: occurrences, depth per level, attrs per part, parts with no attrs (if any; those have no recoverable type name), parts with no calcs.
- The view switch: both views available after one file load; the switch preserves the loaded snapshot; what state (selection, collapse) survives a switch is a design call, but the spec must say the switch is not a reload.
- The part detail panel content: name, type name or "not recorded", containment path, attributes with values and units and source location, calc count.
- Proof obligations: the structural view renders every occurrence (23 on the fixture) including the four nested parts and the three calc-less magnet parts; collapse round-trip preserves the visible tree; a part's panel lists exactly the attributes scoped to it (`blanket` alone holds 18 per the handoff; verify); the schema-mismatch error still applies.
- Acceptance criteria checkable by Playwright from pytest, plus a Playwright screenshot of each view on the stellarator snapshot as evidence.
- Keep design-shaped questions (toggle widget, tree vs nested boxes, panel layout, file layout, how much of `graph.js`/`panel.js` is shared) out of the spec; list them in the handoff for design.

## Rules of the run

- Do not commit. The orchestrator commits after each stage.
- Do not edit anything under `.project/active/model-viz/`, `proof_of_concept/`, or `src/` in this stage. The spec is the only artifact.
- End with `ARTIFACT: .project/active/model-viz-structural-view/spec.md`.
