# Brief — plan stage — GSTH Item 4 (goal-cold-pickup-proof)

Write `.project/active/goal-cold-pickup-proof/plan.md` from the approved `spec.md` and
`design.md` (design revised after `design-review.md`; all findings incorporated). Epic:
`.project/backlog/epic_goal_strategy_task_harness.md` § Item 4.

## Who executes this plan — write for that reader

The executor is the **orchestrator itself, acting as operator** (Align: the owner told the
orchestrator to play operator and wants its notes). The plan is an operator checklist, not a
subagent work order: exact commands, poll conditions, commit points, and abort rules, in
execution order. Cold sessions are launched with
`~/.claude/scripts/orchestrate-stage.sh run <stage>` / `resume <id>` with the brief on
stdin, `--log-dir` outside the repository per design § The freshness fence. The repository
convention `uv run python ...` applies to any Python.

## Shape

Phase 0 must be the design's three de-risk mechanism checks (transcript survival under
process-group kill; the kill actually terminating the `claude` child; `--log-dir` outside
the tree + worktree cwd pickup), each with a pass condition, before any brief is committed.
Then follow the design's commit-sequence table (design § The commit sequence, phases 0–8)
as the plan's phase spine — one plan phase per commit-sequence phase is a sensible default,
with checkboxes per step and the produced evidence path named on each. Carry the design's
abort rules and contingencies (probe worktree teardown, the three kill-window misses, the
restrictive-`:234`-reading refusal, continuation hand-back) into the phases where they can
fire, so the executor doesn't improvise under pressure.

## Hold these lines

- Ordering predicates are commitments: each phase says what must already be an ancestor
  before its first run starts.
- Every run — kept, aborted, or discarded — lands in the freshness record enumeration.
- No repair of Item 1's contract anywhere; measured shortfalls go to the named records.
- The reviewer/resumer/continuation/reader session boundaries are exactly the design's.
- Validation phase at the end: walk the spec's nine criteria against the produced evidence
  and draft `verification_record.md`; the item then goes to `/_my_audit` as a fresh session.

Deliverable: `.project/active/goal-cold-pickup-proof/plan.md`. End with `ARTIFACT: <path>`.
