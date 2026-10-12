# Brief: spec stage — model-viz

Sent by the orchestrator to `/_my_spec`. Provenance marks follow `claude-pack/rules/capture-fidelity.md`. Owner-grade items are quoted or path-cited; everything else is the orchestrator's call.

## Work item

- Name: `model-viz`. Folder: `.project/active/model-viz/`. Single standard-scale item, not an epic (the concept's decomposition guidance, agent-grade, ratified by the reviewed design).
- Read in this order: `.project/concepts/model-viz.md` (the concept, owner words inside), `.project/concepts/model-viz-design.md` (the reviewed concept design), `.project/concepts/model-viz-design-review.md` § Focused Re-review (the two documentation corrections), `.project/research/20260912-004633_calc-dag-visualization.md` (snapshot field evidence).
- The data: `exploration/stellarator_e2e/stellarator.snapshot.json` (~1 MB, `instance-graph/v3`). Probe it with a read-only `uv run python` JSON script when a count or field shape matters. Do not trust counts from the docs without checking; the review already corrected some.

## What the owner decided (settled; do not relitigate)

- `[OWNER-VERBATIM]` "if we see a block for a calc, being able to expand or open a side panel to see the actual SysML or python representation of the calculation" (concept § Owner's Words).
- `[OWNER]` Data source is the codegen snapshot read as JSON. No syside, no codegen Python import, no re-derivation (concept § Next-Stage Handoff).
- `[OWNER]` v1 is direct one-hop I/O per calc plus the detail panel. Multi-hop path tracing is v2 (concept § Owner's Words).
- `[OWNER]` Code lives at `src/model_viz/` (concept § Next-Stage Handoff). Note the repo has no `src/` directory today; this item creates it.
- `[OWNER]` The structural overlay (calcs drawn inside subsystem containers) is an architecture requirement the viewer supports when the model provides non-root scopes; it is not a v1 visual feature (design § Design Principles 4, provenance note).

## Orchestrator decisions (agent-grade, recorded here so the spec can cite them)

1. **v1 scope is the calc DAG viewer only.** The structural view migration from `proof_of_concept/extraction/` into `src/model_viz/` is a follow-on item, not part of this spec. Reason: it has a different producer (syside) and a different serving model (a Python server), and folding it in doubles scope and forces the serving question the design already answered for the DAG path. The concept's own decomposition guidance allows this. Record it in Non-Goals as a decision with this reason, and note concept success criterion 4 is deferred, not dropped.
2. **Serving model: a standalone HTML page loading the snapshot via a file input.** No server. Settled in the reviewed design (§ Architectural Bets); treat as `[AGENT] (ratified by review 2026-09-13)`.
3. **Concept open questions:** (1) static SVG/PNG export: out of scope for v1. (2) Links to generated Python module files: out of scope; the snapshot carries no such path. (3) Schema version mismatch: fail with a clear error naming expected and found versions (design § Edge Cases).
4. **Calcs with empty `calc_expressions`** show "No formula available." No upstream metadata improvement in this item.
5. **The design's "Settled here" heading mixes grades.** The review asked for it to be renamed. Treat the `[AGENT]` entries under it as proposals ratified by the review, not owner rulings. Do not restate them as `[NEED]`; they are `[INFERRED]`.
6. **Test environment facts:** there is no `node` on this machine. Python Playwright is installed in the project venv (`uv run python -c "import playwright"` works) and `scripts/browser_inspect.py` drives a real browser. Any JS-level acceptance test must run through Playwright from pytest. The spec should state acceptance criteria as observable page behaviour, testable that way; it should not prescribe a JS test runner.
7. A parallel spike is measuring dagre layout quality and the expand-collapse extension on the real snapshot. Its findings feed design, not spec. Do not wait for it.

## What the spec must nail down

- Requirements graded `[HARD]` / `[NEED]` / `[INFERRED]` / `[INHERITED]` per capture-fidelity's absorb mapping. `[NEED]` only for the owner items above.
- The four input edge kinds (producer, node, literal, null-with-default) and how each must appear: producer edges become graph edges; all four appear in the I/O panel; unresolvable producer edges are shown with a warning, never dropped.
- Grouping by full `source_file` path, with `source_group` and `occurrence_id` carried as separate fields; parent derived from the selected mode.
- The proof obligations from the design: collapse round-trip preserves the inter-group edge set; a navigation link to a node inside a collapsed group expands the group, then selects and centres the node.
- Acceptance criteria that are checkable: counts for the stellarator snapshot (verify them yourself: calcs, producer bindings, distinct calc pairs, groups, null-edge inputs, empty-formula calcs), the overlay-readiness synthetic-snapshot test, the schema-mismatch error.
- Keep design-shaped questions (panel proportions, extension version, vendoring of JS libraries, file layout under `src/model_viz/`) out of the spec; list them in the handoff for design.

## Rules of the run

- Do not commit. The orchestrator commits after each stage.
- Write markdown with one line per paragraph, no hard wrapping.
- Plain language. A tired engineer reads this once.
- You cannot ask the owner anything. Where the concept and this brief leave something open, decide, mark it `[INFERRED]`, and record the reason in the spec.
- Finish with `ARTIFACT: .project/active/model-viz/spec.md`.
