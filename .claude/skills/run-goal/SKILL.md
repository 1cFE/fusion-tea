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

## Dispatch patterns

The runbook prescribes obligations (fresh critics, bounded scope, one task at a time) but not dispatch mechanisms. These patterns have proven effective across eleven completed goals.

### Model changes

For a single work item, drive it inline through the modeling PM stages: read `.claude/commands/spec-model.md`, `design-model.md`, `plan-model.md`, `implement-model.md` in sequence and follow each procedure directly. Use `uv run agentic-mbse pm add-item` to register the work item, `uv run syside check` for model validation, and `uv run python scripts/integrate.py` for integration proofs.

For multiple independent work items, fork each one as a parallel `Agent` (`subagent_type: "fork"`). Each fork inherits the goal context and drives its own item through the modeling PM stages. Designs and prototypes may run in parallel; integration is always sequential and runs in the main session after all forks return. Write a basis packet (`evidence/`) before forking to fix the shared interface — channel names, file ownership, integration order — so the forks don't collide.

### Research

Start with internal sources: `knowledge/SOURCE_INDEX.md` (registered sources), `knowledge/KNOWLEDGE.md` (domain insights), and `knowledge/research/` (prior research). Use `docs/research_seam_operator_guide.md` for the full protocol.

When external sources are needed, form request files (`knowledge/research/requests/REQ-*.json`) and dispatch each as a parallel `Agent` (`subagent_type: "general-purpose"`) carrying the `/research-acquire` protocol. Each subagent runs the search-triage-register cycle independently: `scripts/research_seam.py` for run bookkeeping, `scripts/source_registry.py register` for ingestion. Deposit the spawn prompt at `evidence/` before spawning. Every search subagent must carry the clean-room screen (`knowledge/holdout/aries-cs/PROTOCOL.md`) in its instructions before any fetch.

### Fresh critics

When the runbook requires a fresh non-author session (disposition checkpoint, round review, study administrator), spawn an `Agent` (`subagent_type: "general-purpose"`) with a deposited prompt — commit the prompt to `evidence/` before spawning. The session must inherit no execution context. If a fresh session cannot be obtained, write the handoff stop per `GOAL_RUNBOOK.md` § What "fresh" means and halt.

## Then go here

- **`work/orchestration/GOAL_RUNBOOK.md`** — the procedure, stage by stage. Read the section for your mode before writing anything.
- **`work/orchestration/goal-templates/`** — the three copyable files.
- **`.project/adr/`** — why the layer is shaped this way. Records 001–007, indexed in `INDEX.md`.
