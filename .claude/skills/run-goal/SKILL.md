---
name: run-goal
description: >
  Operate the goal layer: ground a goal, open or run a round, review a study reading's
  proposed dispositions before follow-up work executes, or review a closed round as a
  fresh agent. Use when asked to pursue a grounded question across rounds of modeling
  and studies, to pick up an interrupted goal run, or to check someone else's round.
  Triggers: "run the next goal round", "ground a goal", "open a round", "what should
  this goal do next", "resume the goal run", "review this round", "check these
  dispositions", "close the round", "the goal trail says", any request to work under
  work/orchestration/goals/.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Run Goal

A goal is a grounded question pursued in rounds. A round is one agent's bounded attempt at one strategy, running one task at a time through the *native* workflows, ending in a mandatory written result and a review by a fresh agent who did not do the work.

This file is the entry point and nothing else. It names the roles, picks the mode, names the goal directory, and points onward. The procedure lives in `work/orchestration/GOAL_RUNBOOK.md`; the decisions behind it live in `.project/adr/`. Nothing is restated here — a human operator and an agent follow the same document, and a second copy of a rule is a rule that will disagree with itself.

## Three roles

- **Operator** — sets the question and holds the gates. Grounds the goal, rules on reserved gates, and closes.
- **Round agent** — pursues one strategy, scopes and runs one task at a time, writes the result.
- **Fresh reviewer** — a session that did not do the work. Reads a study's proposed dispositions before follow-up executes, or reviews the closed round and writes the next strategy.

Which role you are in decides which section you read. `GOAL_RUNBOOK.md` § What
"fresh" means defines the boundary, says who obtains the reviewer on each path, and
gives the agent its move when it cannot start a session — read it before either
review mode.

## Pick the mode

| Mode | When | Go to |
|---|---|---|
| `ground` | No `goal.md`, or it is still `draft` | `GOAL_RUNBOOK.md` § Grounding a goal |
| `round` | A grounded goal, and either no open round or an open round with work left | § Opening and closing a round, then § Running one task |
| `checkpoint` | A study reading with proposed dispositions, before any semantic follow-up | § The pre-execution disposition checkpoint |
| `review` | A round result is written | § The fresh review |

If `trail.md` shows a `T-00N start` with no return and no stop, the run was interrupted: go to § Resuming an interruption before anything else.

To tell whether a round is open, read `trail.md`'s headings — `GOAL_RUNBOOK.md` § Opening and closing a round gives the rule.

## Name the goal directory

`work/orchestration/goals/<goal-slug>/`, holding `goal.md`, `trail.md`, and `learnings.md`. Confirm the slug with the operator before creating it. Templates are at `work/orchestration/goal-templates/`; copy them rather than writing the files from scratch.

## Then go here

- **`work/orchestration/GOAL_RUNBOOK.md`** — the procedure, stage by stage. Read the section for your mode before writing anything.
- **`work/orchestration/goal-templates/`** — the three copyable files.
- **`.project/adr/`** — why the layer is shaped this way. Records 001–007, indexed in `INDEX.md`.
