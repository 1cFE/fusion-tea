# Operator brief — grounding, turn 1

You are a fresh session working with an operator to ground a goal under the repository's
goal layer. You did not build that layer and you need nothing beyond what is on disk.

## What you may read

The goal directory `work/orchestration/goals/cryo-volume-basis/`;
`work/orchestration/GOAL_RUNBOOK.md`; `work/orchestration/goal-templates/`;
`.claude/skills/run-goal/`; `.project/adr/`; and the native repository — `models/`,
`knowledge/`, `work/`, `exploration/`, `modeling_project/`, `docs/`, `scripts/`.

You may **not** read `.project/active/goal-cold-pickup-proof/`, any `.orchestrate-logs/`
directory anywhere, or anything under `~/goal-proof-logs/`. These are orchestration
surfaces, not goal material.

## The operator's question

> Should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus
> DI-010's `J_eng`, instead of held?

The question comes from discovery row `20260823-magnet-technology-ab#2`
(`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`).

## What to do

Ground this question into `work/orchestration/goals/cryo-volume-basis/goal.md`, per
`work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal. The three template copies are
already in the goal directory as your starting point. Walk the repository for the grounding
evidence yourself; the operator will not hand you paths beyond the discovery row above.

This is a headless exchange: you cannot pause to ask. Fill what you can ground from the
repository and the runbook. Where a field genuinely needs the operator — their intent, their
gates, their limits — write the goal file as far as honesty allows, and put your questions
for the operator, numbered and specific, in your final message. The operator's answers
arrive as your next turn.

Provenance: the operator is an agent acting under authority the owner delegated. Mark
operator-supplied content `[AGENT]`, never `[OWNER]`.

Do not run `git commit` — the operator owns commits. Do not start any task: grounding is
the only work of this exchange.
