# Feedback — spec revision — from spec-review.md (verdict Revise)

Fix all five must-fix and the five should-fix findings in
`.project/active/goal-cold-pickup-proof/spec-review.md`. Orchestrator dispositions on the
points that needed a call:

1. **L1-1 (bounded-negative is not a close trigger)** — surface, don't copy. Add a short
   surfaced-premise-conflict note: the epic's "legitimate bounded-negative" wording predates
   Item 1's shipped contract; the runbook's six close triggers (`GOAL_RUNBOOK.md:84-91`) are
   authoritative. Map the epic's intent: the round's last semantic outcome may be a task-level
   `BOUNDED_NEGATIVE`, and the round then closes on one of the six — for this proof, an owner
   gate or a declared limit. Criteria must use the runbook's trigger vocabulary. Mark this
   resolution `[AGENT]`; it is flagged to the owner in the orchestrator's run summary.
2. **L2-1 (gate enforcer)** — decide it in the spec `[AGENT]`: the enforcer in the proof is a
   separate fresh runbook-following session handed the deliberately ungrounded draft and asked
   to proceed to a task per the runbook. The contract holds only if that session refuses task
   start and names the missing field classes unprompted. The orchestrator-as-operator never
   plays the refusing role.
3. **L3-1 (clean-boundary teeth)** — Criterion 4 must require, on disk: the write-ahead trail
   entry, the completed observable native artifact, and no task return, all present *before*
   the resumer session starts; and the resumer must not re-produce the native effect (native
   artifact hash unchanged, no second invocation evidence). An interruption with no landed
   native effect fails the criterion.
4. **L3-2 (orderings)** — make every ordering claim a git predicate: the seed record, the
   write-ahead state, and cold-session input briefs are committed before the dependent session
   runs, so commit ancestry is the auditable order. State this as the spec's verification
   mechanism for orderings.
5. **L1-2 (provenance)** — retag spec:56/spec:58 as `[AGENT] (ratified by owner 2026-08-26)`
   per `align.md`; they are not owner-originated and must not be settled/do-not-relitigate.

Should-fix: L1-3 restore the owner's hardening list to its five items and cite ADR-003 for
the barred premises; L3-3 scope "byte-identical" to the completed native artifact only — the
discovery log legitimately gains joined rows; L3-4 retitle Criterion 2 honestly; L3-5 require
the freshness record to be complete-and-closed (every session enumerated with its full kept
input, and a statement that no other input existed); L4-1 fix the count.

Reviewer's open questions, disposed by orchestrator: L2-2 — the grounding-gate shortfall does
not halt on Item 1's close; it reaches the owner in the run summary with this item's measured
evidence `[AGENT]`. L2-3 — yes: after the fresh review completes, append a dated amendment to
the kept `trail.md` disclosing the seeded drift and citing this item's verification record;
disclosure is post-review only, so it cannot spoil the test. Put both in the spec.

Update the spec in place, keep product-lens current if a finding touches it, end with
`ARTIFACT: <path>`.
