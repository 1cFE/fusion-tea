# Brief: design_review stage — model-viz

Sent by the orchestrator to `/_my_design_review`. Fresh session; you did not write the design.

## Item

- Design under review: `.project/active/model-viz/design.md`. Write the review to `.project/active/model-viz/design-review.md`.
- The contract it must satisfy: `.project/active/model-viz/spec.md` (revised after review). Its review, for the reviewer's notes to design: `spec-review.md`.
- What the design stage was told: `.project/active/model-viz/briefs/design.md`, including the spike-derived rulings at the end. Those rulings are orchestrator judgment, agent-grade; challenge them with evidence, but do not treat them as the design author's inventions.
- Evidence the design leans on: `.project/active/model-viz/spike-layout-findings.md` with `spike/results.json` and screenshots. The spike page `spike/dag_spike.html` and `spike/run_spike.py` can be re-run with `uv run python` if you want to check a claim about the extension's behaviour.
- Fixture: `exploration/stellarator_e2e/stellarator.snapshot.json`. Probe field shapes yourself when the design asserts one.

## What to attack

- **Spec coverage.** Walk every success criterion and requirement in the spec and find the design element that satisfies it. Anything uncovered, or covered by hand-waving, is a must-fix.
- **The visible-edge rule.** The spec states one rule for mixed collapse states and requires one edge per directed group pair when collapsed. The extension bundles two-way pairs into one line. Does the design's mechanism actually produce the spec's edge set, and can the tests read it from the renderer without the test passing by construction?
- **Endpoint truth.** The extension repoints edges on collapse. Does anything in the design read endpoints from live renderer data where it should read the projection's record?
- **Navigation.** Expand, select, centre for a target absent from the renderer while its group is collapsed. Is the sequencing and timing concrete?
- **Testability under the environment's constraints.** No node. Python Playwright, `file://` page, `set_input_files`. Are synthetic fixtures generated, not checked in? Is any criterion untestable as designed?
- **Engineering quality.** Pure projection separated from rendering and shell; vendored pinned libraries; no framework, no build step. Flag anything that smells like a 2,000-line page or DOM access inside the projection.
- **The IR printer** for the 11 formula-less calcs: is the IR shape verified on the fixture, is the operator set exactly the one found, and is the fallback honest?

## Rules of the run

- You never edit the design. Findings in the review doc with IDs; must-fix versus should-fix versus note. The orchestrator carries must-fix items back to the design author.
- No owner is present. Where a finding needs a ruling, state the question and your recommended answer.
- Do not commit. One line per paragraph, no hard wrapping, plain language.
- Finish with `ARTIFACT: .project/active/model-viz/design-review.md`.
