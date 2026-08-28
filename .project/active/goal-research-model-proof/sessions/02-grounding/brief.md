# Operator resume turn — the owner's answers, grounding turn 2

This is a resume turn of the grounding session that wrote
`work/orchestration/goals/p-pump-basis/goal.md` and left five numbered questions in its
final message. The answers are below, numbered against yours.

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

## Provenance — read this before you write a word

Two registers, and they must not blur.

**Answers 1 and 2 below are the owner's own sentences, approved verbatim.** They carry
`[OWNER 2026-08-28]`. Quote them; do not paraphrase them into your own wording.

**Answers 3, 4 and 5 are the operator's**, given under authority the owner delegated and
consistent with the charter the owner approved. They carry `[AGENT]` — *not* `[OWNER]`.
You were right to refuse to write an owner's rule from a precedent; these are the
operator answering, and they are graded as such.

## Answer 1 — § Question. `[OWNER 2026-08-28]`, verbatim

> Is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and if
> not, what sourced value should the model carry?

This settles your question 1. The two halves are deliberately joined by "and if not":
the second clause is conditional on the first. Put this sentence in § Question as the
owner's, with its grade.

## Answer 2 — § Answered when. `[OWNER 2026-08-28]`, verbatim

> A written, sourced answer either way — a better number, or "keep 1.0 MW, here's why" —
> with any model change coming back to the owner first.

Three things this settles, and you should make each explicit in § Answered when:

- **Both directions end the goal.** A reasoned "keep 1.0 MW, with the optimism disclosed"
  is a complete answer, not a failure. So is a better sourced number.
- **The answer must be written and sourced.** An unsourced opinion does not end it.
- **A trail-only answer is complete.** The goal does not have to land a model change to be
  answered. Any model change comes back to the owner first — that is the existing reserved
  gate, and this sentence confirms it rather than adding to it.

## Answer 3 — the DI-008 band discrepancy. `[AGENT]`, operator, 2026-08-28

The goal works against **DI-008 as written**. The 60–190 vs 30–190 MW discrepancy you
found is **logged for the owner, not reconciled inside this goal**. Record it in the goal
file as an open item pointing at the owner, and leave it there. Amending a DI stays a
reserved gate, as you already have it.

Finding this was good work. It was not recorded anywhere before you looked.

## Answer 4 — the shape of the answer. `[AGENT]`, operator, 2026-08-28

**The answer contract does not fix the shape.** A re-based scalar in MW and a fraction of
computed `p_th` are both admissible answers to § Question, and choosing between them is
the work, not a premise of it.

Two bounds on that work, both of which you already have right in § Invariants and
§ Reserved gates and which should stay exactly as you wrote them: the follow-up work item
is what proposes the shape, and **retiring `p_pump` as a settable input is explicitly gate
material** under `STUDY_POLICY.md` § 2 rule 3.

## Answer 5 — § Close rule. `[AGENT]`, operator, 2026-08-28

The fresh round review hands the owner a recommendation; **the owner's ruling closes the
goal.** This is the `cryo-volume-basis` pattern. Write it as the operator's answer with
its `[AGENT]` grade, noting that the owner holds the close itself.

## What to do

Take `goal.md` to `Status: grounded`, per `GOAL_RUNBOOK.md` § Grounding a goal, with all
five field classes non-hollow.

Fill § Question, § Answered when and § Close rule from the answers above, at the grade each
one carries. Everything else you already grounded stays as you wrote it — § Invariants,
§ Grounding evidence, § Limits and § Reserved gates were filled and are not reopened here.
The goal is not yet grounded, so this is still grounding rather than an amendment; from the
moment it reaches `grounded`, nothing is edited in place and corrections go to § Amendments.

Two specific things to preserve, because they are the parts most easily damaged by a second
pass:

- § Invariants must still state the channel and the equal-input/unequal-effect distinction
  and **stop there**, with no conclusion about whether comparison meaning survives.
- § Limits must still restate all four numbers explicitly, with no invented time limit.

If anything in the answers above conflicts with something already in the file, say so in
your final message rather than resolving it silently.

Do not run `git commit` — the operator owns commits. Do not open a round and do not start
any task: grounding is still the only work of this exchange.
