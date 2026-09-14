# Trail: magnet-design-transfer

Append-only judgment record. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

## Round 1 — price-the-sized-winding-pack

### Strategy revision — 2026-09-13

- **Approach:** [AGENT] Connect the existing winding-pack sizing to material quantities and component costs through WI-040, then use the resulting evidence to determine the next bounded task. [OWNER] WI-040 precedes WI-038.
- **Assumptions:** The existing sizing chain supplies meaningful material quantities, and admissible sources can establish material prices without duplicating conductor or casing costs. These premises require inspection against the current model.
- **Abandonment conditions:** A material/accounting premise is contradicted, the needed source basis is unavailable within scope, an owner gate binds, or a declared limit is reached.
- **Intended model increment:** Audited winding-pack steel, insulation, copper and helium mass costs connected to the existing magnet cost account.
- **Intended study question:** Over a documented geometry/current-density range, does increased winding-pack size produce consistent changes in material quantities, magnet cost and the existing operating checks?

### T-001 scope

- **Objective:** Implement and independently audit WI-040's winding-pack mass cost account.
- **Why now:** The approved goal requires this before conductor-grade pricing; the epic records unpriced non-conductor pack material.
- **Scope:** WI-040 source basis, native specification/design/plan, model and coherent generated consumers, validation and independent audit. WI-038 and separate geometry/configuration capabilities are excluded from this task.
- **Inputs:** `goal.md`; `work/backlog/epic-mfe-cost-modeling.md@0b5de53407443f386b2efd2a120fa4837a928690`; `work/completed/20260903_WI-036_winding-pack-sizing/design.md@f937be2c04b43d3ebf00317ec300f4e35aaea93c`; current model and native state inspected before implementation.
- **Done when:** An independently audited WI-040 demonstrates coherent material accounting and affected-consumer behavior, or native evidence establishes a bounded blocker.
- **Stop when:** Prerequisite, strategy blocker, unresolved owner gate, or declared limit.

### T-001 start — 2026-09-13

WI-040 · `work/active/WI-040_winding-pack-mass-cost/` · native specification through independent audit, or a named blocker.
