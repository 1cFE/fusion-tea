# Brief: spec_review stage — model-viz-structural-view

Sent by the orchestrator to `/_my_spec_review`, in a fresh session. Review `.project/active/model-viz-structural-view/spec.md`.

## Context

- The item finishes v1 of the model visualization concept: the structural (part containment) view beside the calc graph view, in one page. Concept: `.project/concepts/model-viz.md`; concept design: `.project/concepts/model-viz-design.md`; the closed calc-graph item's artifacts: `.project/active/model-viz/` (spec, design, audit). The v1 viewer is at `src/model_viz/viewer/`.
- What the spec stage was told: `.project/active/model-viz-structural-view/briefs/spec.md`. Its ruling 1 (snapshot as producer, not syside) is the orchestrator's decision, reaffirmed by the owner on 2026-09-13 as the orchestrator's call to make. Do not relitigate that decision; do check that the spec grades it honestly and states its consequences.
- The fixture: `exploration/stellarator_e2e/stellarator.snapshot.json`. Re-verify any count you doubt with a read-only `uv run python` probe.

## Where to press

1. The three premise corrections (spec § Problem). Are they right? In particular, is there really no way to name a part's direct type from the snapshot? Check `effective_type_ids` ordering, `effective_usage_id`, `declaration_qn` on attrs and calcs, `calc_def_qualified_name`, and `constraint_usages` for anything that names an occurrence's definition. If you find one, that is a must-fix.
2. Does the spec name what the structural view adds beyond the calc graph's Occurrence grouping mode, concretely enough that an implementer cannot ship a relabelled Occurrence mode and call it done?
3. Are the acceptance criteria checkable through Playwright from pytest as observable page behaviour, with verified fixture counts? Is any criterion untestable or design-shaped?
4. Provenance: `[NEED]` only where the owner said it; `[INFERRED]` cites the brief or the v1 design; nothing settled without an owner source.
5. Non-goals: each has a reason; none is phrased as a prohibition anchored on a rejected suggestion.

## Output

Write the review to `.project/active/model-viz-structural-view/spec-review.md` with must-fix items separated from advisories. Do not edit the spec. Do not commit. End with `ARTIFACT: .project/active/model-viz-structural-view/spec-review.md`.
