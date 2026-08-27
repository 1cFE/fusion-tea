# Brief: spec_review stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25. Fresh session — you did not author the spec.

**Review target**: `.project/active/goal-harness-contract/spec.md`

## Context

This is Item 1 of epic GSTH (`.project/backlog/epic_goal_strategy_task_harness.md`) — the lean goal contract and operator runbook. The spec was authored against:

- The epic's Item 1 section (requirements source; its success criteria are used verbatim)
- `.project/concepts/goal-strategy-task-harness-design.md` — approved concept-design, primary authority
- Review resolutions in `...-design-review.md` and `...-design-review-2.md`
- Owner Align rulings 2026-08-25 in `.project/active/goal-harness-contract/align.md`
- Product-lens ledger `.project/active/goal-harness-contract/product-lens.md` (gate CLEAR after spec-F1/spec-F2)

## What to check hardest

1. **Fidelity to owner rulings.** Every `[NEED]`/`[OWNER]` item should trace to a real owner statement — verify the cites (review resolutions C1, P2/M4, P5; epic product-lens F1/F2 dispositions; Align rulings). Flag any inferred item wearing an owner grade, or any owner ruling dropped or softened.
2. **The hardening boundary.** Nothing in scope should smuggle in a control-plane mechanism (envelopes, ledgers, authority digests, idempotency, reconciliation, concurrency, dispatch). Also check the inverse: the evidence-citation digest is owner-required and must NOT be trimmed as hardening.
3. **Checkpoint vs RoundReview separation** — distinct timing and responsibility must be unambiguous (an epic-level success criterion).
4. **Completeness vs epic Item 1 scope** — all four scope groups (architecture records, lean artifact contract, writer ownership, operating surface) and all six success criteria covered; nothing the epic asks for silently omitted.
5. **Spec/design boundary** — the spec should not pre-decide mechanisms (ADR path, template form, test shape, numeric caps). Flag any mechanism decision hiding in a requirement.

Return must-fix findings vs. nits, each with the source you checked. Do not edit the spec yourself.
