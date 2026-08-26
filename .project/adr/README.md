# Architecture Decision Register

This directory holds the repository's architecture decision records. A record exists so that a decision is challengeable at its root: anyone can read what was decided, why, who decided it, what it affects, and what was rejected — without having read the review it came out of.

## What belongs here, and what does not

`.project/adr/` owns **repository, orchestration, and tooling decisions** — how work is organized, how the coding and modeling PMs relate, how the goal layer operates, how scripts and skills are shaped. Records are numbered `ADR-NNN` and live one per file.

`modeling_project/ARCHITECTURE.md` owns **model-architecture decisions** — how the SysML model packages decompose, what a library definition may contain, how designs bind to library elements. Those are numbered `AD-XXX` and stay in that file.

The split is deliberate and follows CLAUDE.md's two-system rule: modeling decisions belong to the modeling PM, everything else to the coding PM. If a decision is about the shape of the model, it is an `AD-XXX`. If it is about the shape of the repository or the way work runs through it, it is an `ADR-NNN`.

## Record form

One decision, one file, named `NNN-<slug>.md`. Every record opens with frontmatter and then carries six sections in order.

```yaml
---
status: accepted            # accepted | superseded
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] 2026-08-23"  # capture-fidelity grade, copied from the source
supersedes: none             # or NNN
amends: CLAUDE.md:73         # or none — a live surface this record changes
---
```

- **Context** — the situation that forced the decision, and where it was decided.
- **Decision** — what was decided, stated so it can be followed.
- **Rationale** — why, at the depth needed to challenge it.
- **Rejected alternatives** — what else was on the table and why it lost. One line each is enough.
- **Affected seams** — the files, procedures, or surfaces that must agree with this record.
- **Consequences** — what is now true, including what this record obliges someone to do.

## Grades

`grade` carries the capture-fidelity provenance of the decision, copied verbatim from wherever it was recorded. It is never re-derived when filing.

| Grade | Meaning | How it is challenged |
|---|---|---|
| `[OWNER]` | The owner decided it, with the date | Ask the owner |
| `[AGENT]` | An agent decided it; "ratified by owner" means the owner approved an agent recommendation | Re-derive it against the recorded reasoning |
| `[INHERITED: src]` | Carried in from a named source | Re-derive against that source |

A record may carry a split grade when the purpose and the mechanism were decided by different people — for example `[OWNER] purpose; [AGENT] mechanism`. Write the split; do not round it to the stronger half.

Only owner-*originated* decisions are settled. An approved agent recommendation stays agent-grade and is challenged by re-deriving it, not by re-asking.

## Filing a record

```bash
.project/scripts/adr.sh list                 # print the index
.project/scripts/adr.sh new <slug>           # mint the next id from the template, add the index row
.project/scripts/adr.sh supersede <old> <new>  # mark old superseded, cross-link both
```

`new` copies `template.md`, fills the id and slug, and appends a row to `INDEX.md`. Fill in the frontmatter and the six sections by hand — the script mints, it does not write.

Superseding never deletes. The old record stays, flipped to `status: superseded` with a pointer to its successor, and the successor names what it supersedes.

Ids are register-scoped. `tests/orchestration/test_goal_contract.py::test_register_is_coherent` asserts that every register id resolves to exactly one file, every file appears in `INDEX.md`, every record carries a grade, and every non-`none` `amends` path exists.
