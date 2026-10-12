# Brief: spec_review stage — model-viz

Sent by the orchestrator to `/_my_spec_review`. Fresh session; you did not write the spec.

## Item

- Spec: `.project/active/model-viz/spec.md`. Write the review to `.project/active/model-viz/spec-review.md`.
- Upstream, in reading order: `.project/concepts/model-viz.md` (owner words inside), `.project/concepts/model-viz-design.md`, `.project/concepts/model-viz-design-review.md` § Focused Re-review, `.project/research/20260912-004633_calc-dag-visualization.md`.
- What the spec stage was told: `.project/active/model-viz/briefs/spec.md`. Its decisions are orchestrator calls, agent-grade. Challenge them if the evidence warrants, but they are not the spec author's inventions.
- The fixture: `exploration/stellarator_e2e/stellarator.snapshot.json`. Check counts and field shapes yourself with a read-only `uv run python` probe; do not take the spec's word.
- The product-lens check did not run at spec stage (path permission). If you can read `~/.claude/scripts/product-lens.md`, apply that lens as part of your review and say so; if you cannot, say so.

## Orchestrator rulings on the spec's open questions (agent-grade; record, do not reopen unless evidence says otherwise)

1. **"Actual SysML or python representation."** v1 answers it with the snapshot's formula steps (the `calc_expressions` text, which is the SysML expression text codegen extracted), the doc comment, and the `source_file:source_line` location. No verbatim SysML text and no Python view in v1. Reason: the snapshot carries neither, and loading the model source tree into the browser is a second data source the owner's data-source decision excludes for now. Judge whether this narrowing is honest and clearly stated, not whether it should be reversed.
2. **The 11 calcs with `expression_ir` but no formula text.** Design decides: if the operator vocabulary used by those 11 trees on the fixture is small and flat enough for a short printer with a "cannot render" fallback, render it labelled as derived from the expression structure; otherwise show "No formula available." Either way the label must say the snapshot has no formula text.
3. **The overlay grade conflict** stays surfaced, not resolved. Do not ask the spec to pick a grade.

## What to attack

- Faithfulness to the owner's words and the reviewed design. Are the `[NEED]` items genuinely owner-stated?
- Whether the success criteria are checkable through Python Playwright as stated, and whether any one of them smuggles in a design choice (library, layout, panel form).
- Whether the collapse round-trip and hidden-target criteria are precise enough to be tests, or vague enough to be argued past.
- Whether anything the concept asked for was dropped silently rather than deferred with a reason.
- Fixture facts: verify at least the group-pair count (35 directed, 4 bidirectional) and the 64-of-155 terminal outputs claim.

## Rules of the run

- You never edit the spec. Findings go in the review doc with IDs; must-fix versus should-fix versus note, clearly separated. The orchestrator carries must-fix items back to the spec author.
- No owner is present. Where a finding would normally ask the owner, state the question and your recommended answer; the orchestrator will rule.
- Do not commit. One line per paragraph, no hard wrapping, plain language.
- Finish with `ARTIFACT: .project/active/model-viz/spec-review.md`.
