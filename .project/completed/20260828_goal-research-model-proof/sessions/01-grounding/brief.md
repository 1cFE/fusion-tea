# Operator brief — grounding, turn 1

You are a fresh session working with an operator to ground a goal under the repository's
goal layer. You did not build that layer and you need nothing beyond what is on disk.

## What you may read

The goal directory `work/orchestration/goals/p-pump-basis/`;
`work/orchestration/GOAL_RUNBOOK.md`; `work/orchestration/goal-templates/`;
`.claude/skills/run-goal/`; `.project/adr/`; and the native repository — `models/`,
`knowledge/`, `work/`, `exploration/`, `modeling_project/`.

You may **not** read `.project/active/goal-research-model-proof/`, any `.orchestrate-logs/`
directory anywhere in the tree, anything under `~/goal-proof-logs-item5/`, or
`.project/backlog/epic_goal_strategy_task_harness.md`. These are orchestration surfaces,
not goal material. Anything not on the "may read" list above is out of scope for this
exchange.

## The operator's question

> Is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and what
> sourced value should the model carry?

## The grounding evidence the operator can point at

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a`, row `20260821-power-cycle-ab#3`
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` § 15
- `knowledge/KNOWLEDGE.md@ffa5c54c`, DI-008

Walk these yourself, and walk whatever else in the native repository they lead you to. The
operator will not hand you paths beyond these three.

## The consumer

Discovery row `20260821-power-cycle-ab#3`. What is waiting on the answer is that open
finding in the committed A/B study. There is no work item for this.

## The channel this value travels, and the distinction that goes with it

`p_pump` → the plant thermal balance and the recirculating sum → `rec_frac` and `p_net` →
the `recirc_ok` and `net_positive` verdicts and LCOE
(`models/library/analyses/mfe_power_balance.sysml:119,135`).

- **The input shift is equal across arms.** `p_pump` is cycle-independent (DI-007) and is
  held at 1.0 MW in all four arms, so a re-based value adds the same megawatts to every
  arm's recirculating sum.
- **The effect is not equal.** `rec_frac` is the recirculating sum over `p_et`, and `p_et`
  differs by arm by construction (η 0.333 → 0.47). The arms already sit at different
  recirculating fractions at the same grid corner — 0.94 / 0.79 / 0.68 by arm
  (`record.md@881d4448:208`) — and the `recirc_ok` fence already sits at different radii:
  violated at R ≤ 8.0 m (paper), ≤ 6.5 m (upstream), ≤ 5.5 m (both η 0.47 arms), at
  a = 0.8 m against threshold 0.5 (`record.md@881d4448:56`).

State this channel and this distinction in § Invariants and **stop there**. Whether
comparison meaning survives a re-based value is not settled at grounding — that is a
judgment for a round to make on evidence it has in hand, under the checkpoint and the fresh
review. A goal that hands a round the conclusion has not grounded anything.

## The reserved gates the owner keeps

- Any model or knowledge mutation beyond this goal directory. Anything landing in `work/`,
  `models/`, or `knowledge/` is the owner's go/no-go.
- The close ruling, if the round ends on a judgment call.
- Merge, push, work-item close, and archive.

## The limits

Restate every one explicitly in `goal.md` with its number; nothing is inherited silently.
The `GOAL_RUNBOOK.md` § Limits defaults are: retry cap 2 retries (3 attempts); checkpoint
revision cap 2 revisions (3 submissions); round limit 6 rounds; tasks per round: none. The
runbook has no time-limit row — do not invent one.

## What to do

Ground this question into `work/orchestration/goals/p-pump-basis/goal.md`, per
`GOAL_RUNBOOK.md` § Grounding a goal. The three template copies are already in the goal
directory as your starting point.

This is a headless exchange: you cannot pause to ask. Fill what you can ground from the
repository and the runbook. Where a field genuinely needs the owner — the exact wording of
§ Question, the § Answered when condition, § Close rule — write the goal file as far as
honesty allows, and put your questions for the owner, numbered and specific, in your final
message. The answers arrive as your next turn.

Provenance: the operator is an agent acting under authority the owner delegated. Mark
operator-supplied content `[AGENT]`, never `[OWNER]`.

Do not run `git commit` — the operator owns commits. Do not open a round and do not start
any task: grounding is the only work of this exchange.
