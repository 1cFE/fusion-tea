# Brief — spec stage — GSTH Item 4 (goal-cold-pickup-proof)

You are speccing **Item 4 of the Goal Strategy and Task Harness epic**:
`.project/backlog/epic_goal_strategy_task_harness.md` § "Item 4: Goal Grounding, Cold-Pickup
Resume, and Round-Review Proof". Read that section in full — its Scope, Out of Scope, Success
Criteria, and Deliverables are the item contract. Work item directory:
`.project/active/goal-cold-pickup-proof/` (Align record already there: `align.md`).

## What this item is

A **proof item, not a build item**. Item 1 (goal-harness-contract) shipped the lean goal
contract: `work/orchestration/GOAL_RUNBOOK.md`, templates at `work/orchestration/goal-templates/`,
ADRs in `.project/adr/`. Item 4 proves that contract works **cold**, with kept evidence:

1. **Cold grounding** — a fresh non-builder session, given only an operator question and the
   repository (no prewritten goal), co-develops a valid `goal.md`; a deliberately ungrounded
   draft must be rejected before any task starts, with the missing fields named.
2. **Interrupted resume** — one bounded task with a write-ahead start is invoked far enough to
   leave an observable native artifact, then intentionally ended with no task return; a
   *different* fresh session must resolve it from the goal directory + native facts alone,
   appending the correct return/stop without duplicating the completed native effect.
3. **Bounded closure + fresh review** — the round closes with **no promoted pin and no
   committed study** (legitimate bounded-negative, owner gate, or declared limit); one scope
   or comparison-meaning drift is seeded; a fresh `RoundReview` must catch it, account for
   every touched discovery row, and accept or correct the learning delta.
4. **Evidence** — goal files, cold-agent inputs/outputs, native refs, a concise proof report.

The proof records any prose failure; **no hardening mechanism is promoted without that
recorded evidence** (owner rule, epic § Hardening rule).

## Settled at Align (provenance marked — do not reopen)

- `[OWNER 2026-08-26]` The operator question is delegated to the orchestrator, who picked
  `[AGENT]`: ground the proof goal on discovery row `20260823-magnet-technology-ab#2`
  (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`) — should `vol_cold_cryo` be
  computed from ampere-turns + DI-010's J_eng instead of held? Grounding chain: the study
  record, DI-010 (`knowledge/KNOWLEDGE.md`), WI-031 approved research.
- `[OWNER 2026-08-26]` The orchestrator plays the operator in the co-development. The owner
  additionally wants the orchestrator's **notes on how the exchange works** — include an
  operator-notes artifact in the deliverables.
- `[OWNER 2026-08-26]` Work stays on branch `feat/goal-integration-seam`, no child branch.
- `[OWNER 2026-08-26, ratifying AGENT default]` Reserved gates for the proof goal: merge,
  push, item close, archive owner-held per the runbook; any model or knowledge mutation
  beyond the goal directory needs owner sign-off.

## Constraints and boundaries

- **Out of scope** (epic): using Item 2/3's native seams (documented manual patterns remain
  allowed); solving the chosen finding; unattended dispatch; promoting hardening machinery;
  treating a clean-boundary handoff as proof of interruption recovery — the interruption must
  be a genuine mid-task stop after write-ahead, before task return.
- The goal layer **cites, never restates** native state (runbook § What this is). The proof
  goal must obey the same writer-ownership rules as a real goal, including joined
  `<study-id>#<n>` disposition rows in the discovery log for touched rows.
- "Fresh" is a **session** boundary (runbook § What "fresh" means, owner's rule). The spec
  should require the evidence to show each cold session's inputs so freshness is auditable.
- Effort target: ~1 day total (spec 1h). Keep the spec lean and testable — success criteria
  from the epic, made concrete.

## Required reading (from the epic)

Item 1's spec/design/runbook/templates/ADRs; the two concept docs' cited sections
(`goal-driven-model-development-harness.md` § Owner's Words + SC 1, 3, 6–8;
`goal-strategy-task-harness-design.md` § Goal and strategy, Task-grain invocation, Review
Pattern, Validation and Handoff); design-review § Resolutions C1/P2;
`work/orchestration/handshake-lcoe-construction.md` (cold prose referent);
`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`.

## Deliverable

`.project/active/goal-cold-pickup-proof/spec.md`. End with `ARTIFACT: <path>`.
