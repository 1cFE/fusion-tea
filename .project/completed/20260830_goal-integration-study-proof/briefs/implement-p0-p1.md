# Brief — implement stage — GSTH Item 6, Phases 0–1 only

You are the **round agent** for goal `p-pump-fence`, round 1. Your session IS the goal-agent
route whose kept evidence Phase 6 later compares against a hand operator — so operate strictly
by `work/orchestration/GOAL_RUNBOOK.md`, and write the goal artifacts (goal.md, trail.md
entries, task scopes/returns) yourself, in your own session.

## Instruction source

`.project/active/goal-integration-study-proof/plan.md` — execute **Phase 0 and Phase 1 only**
(0, 1a, 1b, 1c, 1d), every checkbox, in order. Read it and
`.project/active/goal-integration-study-proof/spec.md` first. The plan's § Decisions D1–D3 and
§ Two standing constraints bind you. Check off plan checkboxes as you complete them and fill
the Phase 0/1 completion notes.

## The owner's grounding wording (reserved gate, now supplied — carry in verbatim)

Goal slug: `p-pump-fence`. Grade both sentences: agent-drafted, **adopted verbatim by owner
ruling 2026-08-29 ("use your drafts")** — record that grading honestly in goal.md; do not
mark them owner-originated prose.

§ Question:
> With `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE?

§ Answered when:
> A committed, verified study on the regenerated, pinned package that locates the `recirc_ok`
> fence and quantifies the LCOE shift at the baseline point relative to the 1.0 MW record —
> with an adverse or inconclusive reading counting as an answer.

## Hard rules

- **Do NOT git commit, push, or touch git state beyond reads/diff/status.** Stage all writes in
  the working tree; the orchestrator commits at the plan's marked commit points. List every
  file you created/modified in your final message, grouped by the plan's two Phase-1 commit
  points plus the Phase-0 one.
- Stop and report (do not improvise) if: the 1a blocker is anything but gate 2
  `package-not-integrated`; the seam exits 2 (read seam_traceback.txt, quote it, stop); any
  grounding field class is hollow; or you hit any reserved gate (spec § Align ruling 4).
- `uv run` for everything; env per plan § Environment Setup.
- Cite-don't-mirror in all goal artifacts (`<path>@<sha>` + meaning).
- Do not proceed into Phase 2 — it opens with an owner framing gate the orchestrator carries.

End with either the stop report above, or: the T-001/T-002 return classes, the CANDIDATE pin +
both fingerprints, the tests/study result, and the grouped file list.
ARTIFACT: (your final message; no single artifact path required)
