# Architecture Decision Index

Repository, orchestration, and tooling decisions. Model-architecture decisions (`AD-XXX`) live in `modeling_project/ARCHITECTURE.md`. See `README.md` for the record form, the grade vocabulary, and how to file.

| Id | Decision | Status | Grade | Date |
|---|---|---|---|---|
| `001` | [A goal round authorizes one bounded task at a time, under one revisable strategy](001-strategy-and-task.md) | accepted | `[AGENT]` ratified by owner | 2026-08-25 |
| `002` | [One agent pursues one strategy for a round; a fresh agent reviews it and authors the next](002-round-boundary.md) | accepted | `[OWNER]` purpose; `[AGENT]` mechanism | 2026-08-25 |
| `003` | [Begin with prose files and native facts; harden only on an observed failure](003-lean-first-persistence.md) | accepted | `[OWNER]` 2026-08-23; `[AGENT]` mechanism | 2026-08-25 |
| `004` | [A goal round dispositions every discovery row its evidence touched, by appending a joined row](004-finding-disposition.md) | accepted | `[OWNER]` 2026-08-23 | 2026-08-25 |
| `005` | [One fresh round critic, plus one pre-execution disposition checkpoint](005-review-topology.md) | accepted | `[AGENT]`; owner may override | 2026-08-25 |
| `006` | [Goal artifacts may cite `.project/` by path and digest](006-goal-evidence-seam.md) | accepted | `[OWNER]` 2026-08-23 | 2026-08-25 |
| `007` | [The task is the authority unit; the finding stays the traceability unit](007-supersession.md) | accepted | `[AGENT]` half; `[OWNER]` 2026-08-23 half | 2026-08-25 |

## Prior art, outside the register

`exploration/phase_1a/ADR-001_csv-source-of-truth.md` — CSV is the source of truth for the concept ontology (2026-05-17). Written before this register existed, in its own style, and it already owns the id `ADR-001`. It is not renumbered and not moved: it has inbound citations, and breaking them for tidiness is not worth it. Register ids are scoped to this directory, so the `001` above and that file are different ids. New decisions go here.
