# Brief to /_my_spec — GSTH Item 5: Research-to-Model Round Proof

You are speccing one work item inside a running epic. Write
`.project/active/goal-research-model-proof/spec.md`. Do NOT run git commits — the
orchestrator commits. If you must ask something, ask; otherwise finish with
`ARTIFACT: <path>`.

## The work item (epic text is authoritative)

Read `.project/backlog/epic_goal_strategy_task_harness.md` § Item 5 (line ~364) in full —
objective, scope 1–4, out-of-scope, success criteria, deliverables. That section is the
requirements source; this brief adds owner rulings and orientation, it does not replace it.

One-line objective: exercise a real `model → research → model` sequence under one
unchanged strategy, with a fresh non-author critic between the study reading / proposed
dispositions and any semantic follow-up execution. It is a PROOF item: kept, inspectable
evidence that the native research seam (GSTH Item 2) and the critic checkpoint work in a
live goal round. Honest outcomes are first-class — a `STRATEGY_BLOCKER` close is a valid
result; do not spec the item so only the positive path can succeed.

## Owner rulings at Align (2026-08-27) — settled, do not relitigate

- `[OWNER 2026-08-27]` **The live need is the `p_pump` re-source** — discovery row
  `20260821-power-cycle-ab#3` in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`:
  `p_pump` = 1.0 MW is ~100× below helium-primary circulator figures (DI-008,
  `knowledge/KNOWLEDGE.md`); the row says "re-sourcing is a separate modeling item; item
  not yet minted". A NEW goal is grounded on this need under
  `work/orchestration/goals/` (the only existing goal, `cryo-volume-basis`, is closed).
  Ruled with the conflict surfaced: this takes the `p_pump` re-source off Run-Study
  Item 6 Phase 4's close list.
- `[OWNER 2026-08-27]` **Reserved gates** (owner decides, the run parks and asks):
  (a) the goal question and its "answered when" terms at grounding; (b) any model or
  knowledge mutation beyond the goal directory (WI lands through the modeling PM; go/no-go
  is the owner's); (c) the close ruling if the round ends on a judgment call.
- `[OWNER 2026-08-27]` **In scope**: flipping `work/orchestration/GOAL_RUNBOOK.md`
  § The native seams `research` row from "pending native repair" to native (Item 6 owns
  the `integrate` row).
- `[OWNER]` (epic, § Epic Strategy) **Hardening rule**: no envelopes, ledgers, digests,
  idempotency, reconciliation, or dispatcher machinery unless a recorded run failure
  promotes it. Prose artifacts + native facts only.
- `[OWNER 2026-08-25]` (epic, Success Criteria) a fresh non-author critic reviews the
  reading and proposed dispositions BEFORE any semantic follow-up task executes; the
  author revises until the checkpoint passes or its declared cap produces an
  owner-visible stop. The spec must carry that cap.

## Required reading (per the epic, with resolved paths)

- `work/orchestration/GOAL_RUNBOOK.md` — the operating contract (grounding, rounds,
  task returns, seams, review). The goal round follows it; the spec cites it, never
  restates it.
- Item 1 archive `.project/completed/20260827_goal-harness-contract/`, Item 2 archive
  `.project/completed/20260827_goal-research-seam/` (research seam: `scripts/research_seam.py`,
  `scripts/source_registry.py`, `docs/research_seam_operator_guide.md`, returns
  REGISTERED / OPERATOR_QUEUE / BOUNDED_NEGATIVE / BLOCKER), Item 4 archive
  `.project/completed/20260827_goal-cold-pickup-proof/` (the manual-seam proof this item
  extends).
- `.project/concepts/goal-strategy-task-harness-design.md` § Task-grain invocation,
  Native seams, Round Semantics, Findings and Learning, Review Pattern.
- `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words on critic
  placement; Success Criteria 2, 4–6.
- `.project/research/20260822-120756_research-extraction-harness.md` § the one manual
  trace, patterns P1–P10.
- The prior goal `work/orchestration/goals/cryo-volume-basis/` as the worked example of
  goal.md/trail.md shape (closed; do not reopen it).
- DI-008 in `knowledge/KNOWLEDGE.md` and the power-cycle study record
  `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md` § finding #3 —
  the native evidence behind the live need.

## Boundaries the spec must hold (from the epic)

- Out of scope: research or model writes outside their native workflows; more than the
  one bounded live need; package regeneration, promotion, or study execution (Item 6
  owns those); a critic per native stage (ONE critic checkpoint, placed as ruled).
- The modeling task returns `PREREQUISITE` from its own bounded scope — it must not
  predict the research in a future task list.
- Every touched discovery row gets a joined `<study-id>#<n>` disposition update; the
  study executor stays first-sighting writer.
- No mirroring of modeling-PM state into the goal directory; cite `<path>@<commit-sha>`.

## Provenance discipline

Grade requirements per capture-fidelity: owner rulings above are `[NEED]` with the ruling
cited; epic-inherited items `[INHERITED: epic_goal_strategy_task_harness.md]`; your own
operationalizations `[INFERRED]`. Do not promote inferences to `[NEED]`.
