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
- **Executor** — works through the runbook and commits the record. Writes everything in
  the record directory except the synthesis.
- **Administrator** — reads a committed record and writes the synthesis. Reads nothing
  outside the record directory, and reports a missing fact as missing rather than
  recovering it from elsewhere.

One session takes one role at a time. The record is the only seam between them.

## Pick the mode — ask, do not guess

- **execute** — there is an intent and no record yet. Ends with a committed record.
- **administer** — there is a committed record and no synthesis. Ends with `synthesis.md`.

If the request does not make the mode obvious, ask which one before doing anything else.
A study executed when a synthesis was wanted wastes a run; a synthesis attempted on a
directory that is not a record produces a confident account of nothing.

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
