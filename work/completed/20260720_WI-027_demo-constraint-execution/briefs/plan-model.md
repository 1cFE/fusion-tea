# Brief — /plan-model — WI-027 Demo Constraint Execution (STELLARATOR-DEMO Item 2)

Plan the implementation of WI-027. Spec + design are complete and settled — plan phases, order, and validation checkpoints; do not reopen mechanism decisions. Write `work/active/WI-027_demo-constraint-execution/plan.md`.

## Required reading, in order

1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute.
2. `work/active/WI-027_demo-constraint-execution/spec.md` (MR-1…8) and `design.md` (the six settled decisions D1–D6).
3. `work/orchestration/demo-constraint-execution.md` — standing bars and rulings.

## Planning guidance

- **Phase the work so every phase ends at a mechanically checkable state**, with the standing bars run at the checkpoints the design names. A sensible spine (adjust with your judgment, record deviations): (1) un-strip staged twins + twin diff-bar check; (2) snapshot recapture at the pinned commit + bridge regen + WI-022 hash + regen-stability checks; (3) runner CONSTRAINT-EXEC adapters + verdict harvest + oracle-side verdict assertion; (4) full validation sweep — oracle rel 1e-9 on all channels, handshake empty-diff (original successor bar), IFE anchors, L1–L6 offender list = 6 pre-existing, pytest tally 11/18/14/0, MR-2 grep; (5) SV-033 executed record + VALIDATION_MATRIX update + docs/annotations.
- Include the **rollback posture** per phase (regen is snapshot-driven — a failed phase reverts to the committed snapshot state).
- The plan carries the design's exact pin (`512786c`) and the recapture procedure; the implement stage must not improvise either.
- Validation levels per the modeling-PM 6-level methodology where applicable; the item's real gates are the design's §6 list.
- Out of scope unchanged (no new constraints, no studies, no account changes, canonical models untouched except as design D1 specifies).

End with ARTIFACT: <path to plan.md>.
