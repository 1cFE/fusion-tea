# Brief — design stage — GSTH Item 4 (goal-cold-pickup-proof)

Design the proof runs for `.project/active/goal-cold-pickup-proof/spec.md` (Approved after
review; review at `spec-review.md`, dispositions in `briefs/spec_fix.md`). The spec is the
contract — every criterion is disk-checkable and ordering-carried by git ancestry. Epic:
`.project/backlog/epic_goal_strategy_task_harness.md` § Item 4. Align: `align.md`.

## What the design must settle

The spec defers seven items to design; three are load-bearing on proof validity and the spec
requires them settled before anything runs:

1. **How a cold session is obtained and captured.** The orchestrator runs headless stage
   sessions (`~/.claude/scripts/orchestrate-stage.sh run <stage>` with the brief on stdin;
   fresh session per `run`, resumable by id). Design the freshness evidence: each cold session
   gets exactly one committed input brief (committed before the session runs), its full output
   is kept in the item directory, and the freshness record enumerates every session with its
   complete kept input and closes the enumeration. Decide which stage command each cold role
   uses (the run-goal skill exists: `.claude/skills/run-goal/`; a generic session pointed at
   GOAL_RUNBOOK.md is also viable) and what the session may read.
2. **Which native target the interruption uses.** Constraint interplay to respect: Item 2/3
   seams are out of scope (manual patterns allowed); the goal's reserved gates say any model
   or knowledge mutation beyond the goal directory needs owner sign-off; the epic bars solving
   the finding; yet the task must land a genuine, observable, completed native artifact before
   the stop. Candidates worth weighing: a manual research note under the research pipeline's
   documented pattern, a `work/` analysis artifact, or another native surface — pick one that
   is honest native work toward the goal's question without crossing a reserved gate, and
   state why. If every honest candidate crosses a gate, that is a design finding to surface,
   not to paper over.
3. **How the drift is planted.** Exactly one plausible scope or comparison-meaning drift,
   seeded in the round's written material by the orchestrator-controlled round path, seed
   record committed first (identity + expected detection), post-review disclosure amendment
   per the spec.

Also settle the remaining deferred items (see spec § Open questions / deferred list), the
task grain (how many tasks the round runs; the spec's criteria reference T-001 scope and a
T-00N interruption), the exact sequence of commits that carries the ordering predicates, and
the verification record's shape (who checks each criterion, against which paths).

## Constraints

- The proof exercises Item 1's contract as shipped — the design must not extend or repair
  GOAL_RUNBOOK.md, templates, or ADRs (repairs are Item 1's; measured shortfalls are
  evidence under the owner's hardening rule, spec § A predicted prose failure).
- The grounding-gate probe measures **per field class** (five classes); the enforcer is a
  separate fresh runbook-following session (spec decision, do not reopen).
- The round closes on an unresolved owner gate or declared limit only (spec § A close
  trigger the epic names does not exist — do not reopen the trigger vocabulary).
- No hardening machinery, no dispatch, no concurrency (ADR-003 barred premises).
- Provenance discipline: operator-side content in the proof goal is orchestrator-
  operationalized `[AGENT]` unless it traces to `align.md` owner lines.
- The owner wants operator-notes from the orchestrator's side of the grounding exchange —
  design where they live and what they must cover.

## Deliverable

`.project/active/goal-cold-pickup-proof/design.md`. A design_review follows as a fresh
session. End with `ARTIFACT: <path>`.
