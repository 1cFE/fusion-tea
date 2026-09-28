---
name: run-study
description: >
  Run a parameter study against a generated model package, or read a finished study's
  record and synthesize it. Use when asked to sweep, search, or explore a design space;
  to test how an objective or a constraint responds to a parameter; to find where a
  feasible region ends; or to pick up someone else's finished study and say what it
  found. Triggers: "run a study", "sweep R and a", "design search", "explore the design
  space", "how sensitive is LCOE to", "where does the constraint bind", "find the
  feasible region", "study whatever you can find in this package", "what did this study
  find", "synthesize this study", "pick up the results in exploration/.../studies/",
  "administer this record", any request to sweep a model or interpret a study record.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Run Study

A study runs a model package over a set of parameter points and records what the model's
own objective and constraints did at each one. What makes it a study rather than a sweep
is the record: one directory that a second agent, with no memory of the run, can read and
recover what was asked, what was assumed, what came out, and what none of it supports.

This file is the entry point and nothing else. It captures intake, picks the mode, names
the record path, and points onward. The steps live in `runbook.md`; the rules live in the
policy.

## Three roles

- **User** — sets the intent, and rules on any axis the model turns out not to resist.
  That ruling happens before any point runs.
- **Executor** — works through the applicable runbook obligations and commits the record. May write an executor synthesis grounded only in the committed record; label its authorship honestly.
- **Administrator** — optional separate reader of a committed record, used when the owner requests a cold-record reading or independent coverage needs it. Reads only the record directory and reports missing facts instead of recovering them elsewhere.

The main agent may execute and synthesize directly. A separate administrator is not an automatic step. A claimed independent reading requires a fresh non-author session with no inherited conversation. Both kinds of synthesis cite only the committed record and preserve its evidence. Review scope follows `work/orchestration/GOAL_RUNBOOK.md` § Review scope and evidence reuse: original evidence, bounded briefs, and no duplicate assurance.

## Pick the mode

- **execute** — there is an intent and no record yet. Ends with a committed record.
- **administer** — there is a committed record and no synthesis. Ends with `synthesis.md`.

Infer the mode from the request and existing record. Ask only when genuine ambiguity would change the work. Executing and then synthesizing in the same session is allowed; a separate session is needed only for an independent reading.

## Capture the intake

In execute mode, get the goal and the scope in the user's own words and keep them
verbatim — they are the first thing the record carries.

Intake is collaborative and flexible. "Study whatever you can find in this package" is a
complete intake and so is a named subsystem with a specific parameter list, and so is
everything between. There is no questionnaire to fill in. Work with what the user gives,
ask about what is genuinely unclear, and write down what you added yourself as yours
rather than blending it into their words.

## Name the record path

- **execute** — the record path is `exploration/<pkg>/studies/<study-id>/`. Mint the
  `<study-id>` here, before the runbook starts, using the convention in
  `runbook.md § Naming`, and tell the user where the record will land.
- **administer** — the user gives you the record path. Confirm it is a record directory
  before reading it as one.

## Then go here

- **`runbook.md`** — the ordered obligations, what each deposits in the record, and the
  administer sequence. Both modes continue there.
- **`record-template.md`** — the record contract: the seventeen sections, the
  values/arguments split, and the `snapshot.json` field list.
- **`modeling_project/STUDY_POLICY.md`** — the rulebook. It
  says what a legitimate axis is and what a study may claim; this skill does not restate
  it.
- **`scripts/study/`** — the tools. Runbook steps call them; this skill never does.
