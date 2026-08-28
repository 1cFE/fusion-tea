# Brief to /_my_design_review — GSTH Item 5 design

Review `.project/active/goal-research-model-proof/design.md` (Draft 2026-08-27) against
the contract `.project/active/goal-research-model-proof/spec.md` (revised same day).
You are a fresh, non-author reviewer. Do NOT edit the design, do NOT run git commits.
Classify findings must-fix vs advisory; finish with `ARTIFACT: <path>`.

Context: align.md (owner rulings, settled), spec-review.md (spec's review, applied),
epic § Item 5, `work/orchestration/GOAL_RUNBOOK.md` (operating contract),
`docs/research_seam_operator_guide.md` (seam contract),
`.project/completed/20260827_goal-cold-pickup-proof/` (Item 4, the pattern reference).

## Review priorities beyond your command's checklist

1. **Requirement coverage** — every spec R-* lands somewhere in the design; flag any
   silently dropped or weakened (especially R-A2a, R-C3a, R-G4, R-H4).
2. **D8's class→outcome mapping** — is `OPERATOR_QUEUE → PREREQUISITE` and
   `BLOCKER → MECHANICAL_FAILURE` legal against the runbook's task-return vocabulary
   and R-D3's no-re-grade rule? Check the runbook's actual return classes.
3. **D5, the stale-row override** — a committed brief overrides the shipped runbook.
   Is it phrased as an operator decision with provenance (capture-fidelity) rather than
   an instruction that stages the errand? Does its timing (post-checkpoint) actually
   protect Invariant 3, given the brief text will name the seam scripts?
   Cross-check Invariant 3's wording: it fences briefs committed BEFORE T-001's return —
   is that the right fence line for the T-002 brief?
4. **Invariant 2 vs the brief-delivery mechanism** — sessions may not read the item
   dir, but briefs live at `sessions/NN-<role>/brief.md` in the item dir. How does the
   brief reach the session without breaching Invariant 2? Item 4's mechanism is the
   reference; the design must not leave this contradictory.
5. **Auditability** — can each of Invariants 1–10 actually be checked by the stated
   command shapes? Any that are unverifiable as written?
6. **Session choreography legality** — resumed session 03 across turns 05/06/07 vs the
   runbook's session-boundary rules; critic and reviewer freshness (R-C5, R-F4).
7. **Budget realism** — 8–10 sessions against 8h execute; is the floor path (queue +
   gate park) actually inside budget?
8. **Hardening rule** — do covering-branches.md / freshness-record.md / meta.md stay
   prose artifacts (Item 4 precedent) or does anything cross into R-H1's banned list?
