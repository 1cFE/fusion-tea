# Trail: magnet-closure

What happened, and what was decided. Append-only, newest entry last, ISO dates; no entry is ever edited in place — corrections are `### Amendment` entries. This file logs judgment, not routine stage motion; native workflows keep their own stage records and are cited, never restated. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

Goal grounded 2026-08-30 (`goal.md`, owner-present session). No round open.

## Round 1 — derive-field-and-limit

### Strategy revision — 2026-08-30

- **Approach:** make the magnet system forward-derived in three linked moves: (1) compute the field path from coil geometry and current — the existing Ampère's-law conductor quantity (`mfe_magnet_cost.sysml`) already runs geometry→kA·m *from* a held B; invert the direction so B_axis/B_peak follow from coil current and bore geometry; (2) add one executable structural limit (winding-pack stress or critical-current-density margin) whose operand is computed, so coil sizing and field choice have something pushing back; (3) split the 5.87 markup into separately sized winding-pack / structure / cryoplant sub-accounts. Sources: admissible in-repo material only — Stellaris design details (REBCO HTS, 20 K, winding-pack data already cited in the instance), 1costingFE (pinned `0254385`), general engineering practice.
- **Assumptions:** the in-repo admissible sources carry enough winding-pack data for a defensible limit basis; the radial build supplies the coil-bore geometry; P3 is reachable without confinement coupling (the Row-3 anchor asks the limit to push on coil sizing/field, not on the operating point).
- **Abandonment conditions:** a defensible limit basis turns out to need new ingestion the owner declines, or an owner-gated reopening (Rung C, held p_pump); or the P3 anchor proves unreachable without confinement closure — that is a rubric-anchor contest and goes to the owner, not around them.
- **Intended model increment:** magnet subsystem calc defs (field from coil geometry/current; stress or J-margin), one new viability constraint asserted in the instance, decomposed magnet cost accounts in library + `stellarator_09` rebinds.
- **Intended study question:** where does the new structural fence bind in (R, a, B) space, and do feasibility and the constrained optimum move once field is derived rather than cited?

### T-001 scope

- **Objective:** register the modeling work item and produce its spec for the magnet-closure model increment.
- **Why now:** the goal is grounded at `goal.md@11fa3e3d`; a standard-scale modeling change enters the native modeling PM at `/spec-model`, and the spec's owner checkpoint is the first place the increment's outcome-level shape gets ruled on.
- **Scope:** authorized — `pm add-item` under the modeling PM and `work/active/WI-XXX_*/spec.md`; excluded — design/plan/implement stages, any `models/` edit, any source ingestion.
- **Inputs:** `goal.md@11fa3e3d` (no narrower constraint).
- **Done when:** the spec exists and is presented at the owner checkpoint (outcomes, not mechanisms — per the standing spec-stage feedback).
- **Stop when:** owner gate (the checkpoint), a discovered prerequisite, or a strategy blocker.
