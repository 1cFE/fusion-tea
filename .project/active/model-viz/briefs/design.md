# Brief: design stage — model-viz

Sent by the orchestrator to `/_my_design`. Fresh session.

## Item

- Spec (the contract): `.project/active/model-viz/spec.md`, revised after review. Its review: `spec-review.md` (§ Notes for design carries points the reviewer wrote for you).
- Spike findings on layout and the expand-collapse extension, measured on the real snapshot: `.project/active/model-viz/spike-layout-findings.md`, with throwaway code and screenshots under `spike/`. Read the findings before choosing libraries or layout direction; look at the screenshots.
- Upstream shaping, for intent only: `.project/concepts/model-viz.md`, `.project/concepts/model-viz-design.md` (a concept-level design; this stage produces the technical design for implementation, and may depart from it where the spec or the spike evidence says so, recording why).
- Fixture: `exploration/stellarator_e2e/stellarator.snapshot.json`. Probe with `uv run python` when a field shape matters.
- Existing reference code, not reused as a data source: `proof_of_concept/cytoscape_demo.html` (an earlier Cytoscape shell with compound nodes, expand-collapse and an info panel), `proof_of_concept/web/`, `proof_of_concept/tests/test_web.py` (how the earlier POC tested a page from pytest).

## Provenance

Owner-grade items are the `[NEED]` lines in the spec. Everything else in the spec is `[INFERRED]` or `[HARD]`, and every ruling in `briefs/spec.md`, `briefs/spec_review.md` and `briefs/spec_revise.md` is orchestrator judgment, agent-grade. Design may challenge an agent-grade item by re-deriving against its recorded reason; it may not challenge a `[NEED]` line.

## Orchestrator constraints for the design (agent-grade, with reasons)

1. **Engineering bar.** This is the first code under `src/model_viz/`; it sets the pattern. Small pure projection functions with no DOM access, separated from rendering and from the page shell, so the projection is testable from `page.evaluate` without clicking through the UI. No framework, no build step. Vanilla JS in a few files, not one 2,000-line HTML page.
2. **Vendor the JS libraries** (Cytoscape, dagre, cytoscape-dagre, cytoscape-expand-collapse) under `src/model_viz/viewer/vendor/` with pinned versions and a short `VENDOR.md` listing version, source URL, and licence. Reason: the viewer must work offline and the Playwright tests must be deterministic; the spike will say whether unpkg is even reachable here. Use the versions the spike proved load together.
3. **Tests are Python Playwright under pytest**, in `tests/model_viz/`. The page is opened as a `file://` URL; the snapshot is delivered through the file input with Playwright's `set_input_files`. Synthetic fixtures (schema mismatch, removed-calc, unrenderable-tree, overlay occurrences) are generated from the real snapshot by a small fixture module at test time, not checked in as 1 MB copies. Follow `feedback_test_strategy`: test the seams (load → project → render → panel → navigate), not isolated happy paths.
4. **The 11 formula-less calcs**: a tiny printer for `expression_ir` covering `+`, `*`, attribute references and literals, with a "cannot render" fallback for anything else, labelled as the spec says. Probe the IR shape on the fixture first and put the shape in the design.
5. **Grouping-mode control**: implement mode switching as a projection parameter plus a small UI control (a select or toggle). It is degenerate on today's model; that is fine. The overlay test drives it through the UI, not through a hidden hook.
6. **Duplicate doc comment** at the end of every formula list: show the formula entries in full and show the doc comment once in its own section; if the last formula entry is byte-identical to `doc_comment`, render it in the formula section with a note that it repeats the documentation rather than dropping it. Spec requires no entry lost.
7. **Search by calc name**: include a simple filter box that selects and centres a calc by name match (expanding its group). It is cheap and the navigation stories lean on it. Keep it to name matching.
8. Decide and record: parallel edges or merged per calc pair (spec allows either; the spike may inform), layout direction, initial collapse state, panel proportions, group label shortening, how design-file groups are distinguished.

## What the design must contain

- The file layout under `src/model_viz/` and `tests/model_viz/`, and what each file owns.
- The projection's output shape (node and edge data fields, including `source_group` and `occurrence_id` carried separately) and the visible-edge rule from the spec mapped onto the expand-collapse extension's actual behaviour as the spike measured it. If the extension does not implement the spec's rule natively, say how the design achieves it.
- The reverse index for output consumers and how unresolved producers are represented.
- The interaction contract for navigation: expand-then-select-then-centre, including the timing the spike found (same tick or callback).
- The test plan at the level of which criteria each test file covers, and how edges are read from the renderer rather than the snapshot.
- Alternatives considered where you were genuinely unsure, with the choice and reason.

## Rules of the run

- No owner is present. Decide and record; do not stop to ask unless a decision would make the work useless if wrong. If you must stop, put every question in one batch as your whole final message.
- Do not commit. One line per paragraph, no hard wrapping, plain language. Main body about 300 lines; appendices allowed.
- Finish with `ARTIFACT: .project/active/model-viz/design.md`.

## Spike-derived rulings (added after the spike landed; agent-grade)

- **Edge endpoints.** The expand-collapse extension repoints crossing edges at the collapsed group box and restores them on expand (`data('originalEnds')`). The projection therefore keeps its own copy of every edge's calc endpoints and ports, and the detail panel and the reverse index read only projection data, never live renderer edge data. The spec's round-trip criteria are read from the renderer as required; the invariant "original endpoints not mutated" in the concept design is superseded by "the projection's endpoint record is the truth".
- **Bundling.** The all-collapsed view must be bundled (119 raw lines is a hairball; 31 bundled lines is readable). The extension's `collapseAllEdges()` merges a two-way pair into one line tagged `directionType: 'bidirection'`, which breaks the spec's two-edges rule. Design must produce one visible edge per directed group pair (35 with everything collapsed). Either bundle per direction in the projection layer, or use the extension's bundling and split the `bidirection` bundles; pick one and record why.
- **Layout.** Dagre `rankDir: 'LR'`. Groups start collapsed. Fit-to-view after an expand.
- **Navigation timing.** `api.expand(node)` is synchronous and `cy.center()` works on the same tick; `cy.animate` needs its `complete` callback. A calc inside a collapsed group is absent from `cy`, so navigation resolves the target's group from the projection first.
- **Versions.** Cytoscape 3.28.1, dagre 0.8.5, cytoscape-dagre 2.5.0, cytoscape-expand-collapse 4.1.0 load together with no console errors. Vendor these exact versions; do not upgrade in this item.
- **Lookup key.** `node_id` is already a JSON-encoded string; producer targets match it raw. The research doc's `json.dumps` recipe is wrong; ignore it.
