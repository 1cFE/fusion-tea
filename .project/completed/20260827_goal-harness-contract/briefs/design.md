# Brief: design stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25.

**Input spec**: `.project/active/goal-harness-contract/spec.md` — revised through independent review (`spec-review.md`, verdict Revise, all must-fixes applied and orchestrator-verified). Treat the spec as the contract; its provenance grades are load-bearing. Read `align.md` for owner rulings and `product-lens.md` for the capture ledger.

**Epic context**: Item 1 of `.project/backlog/epic_goal_strategy_task_harness.md`. Downstream items 4–6 read your output as their input: a fresh non-builder must be able to ground a goal, resume an interrupted task, and run a full round from the documents and templates you design. Item 2 (research seam) runs NOW in a parallel worktree and wants to file ADRs into the home you create — sequence the ADR home early.

## What design must settle (spec § Open Questions)

1. **ADR home** — location, record form, numbering. Weigh extending `modeling_project/ARCHITECTURE.md`'s `AD-XXX` convention vs a separate orchestration register; say which and why. Decide when the home lands relative to the rest of the item (Item 2 is waiting on it).
2. **Template/instruction form and paths** for `goal.md` / `trail.md` / `learnings.md` and the goal-agent entry surface (skill vs command vs plain instructions) — human and agent must follow the same contract.
3. **Section conventions** for the three prose files: headings, entry format, dated amendments, the write-ahead start line, the six-value task return, the five decision fields.
4. **Default numeric limits** — retry cap, checkpoint revision cap, round limits. The caps' existence and the owner-visible stop are `[NEED]`; only values are yours. Ground values in the referent (`work/orchestration/handshake-lcoe-construction.md`) and the design doc; keep them lean.
5. **Consistency tests** — home, assertions, drift detection across the five amended writer-ownership homes; deliberate coverage of the joined-row shape (the `[HARD]` item on `tests/study/test_records.py:41`). Lightweight-consistency altitude only.
6. **The exact amendment text plan** for the five writer-ownership homes and `CLAUDE.md:73` — leaving room for Item 6's pending findings #6/#10/#11.

## Constraints to hold

- Hardening boundary (spec § Non-Goals) is absolute — no control-plane mechanism. The evidence-citation digest survives per the recorded `[INFERRED]` reconciliation; if you find a genuine collision, surface it and park, don't resolve.
- No fallbacks for missing inputs; no goal-agent executable code.
- Smallest surface that meets the owner's documentation bar — the handshake brief is the `[REFERENT]` prose bar.
- Match repo conventions; don't hard-wrap markdown prose.

Output: `.project/active/goal-harness-contract/design.md`. If a spec requirement can't be met as written, ask me before writing around it — never bury the gap.
