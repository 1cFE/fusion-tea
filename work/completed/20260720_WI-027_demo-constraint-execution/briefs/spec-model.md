# Brief — /spec-model — WI-027 Demo Constraint Execution (STELLARATOR-DEMO Item 2)

Spec the modeling work item WI-027 "Demo Constraint Execution (STELLARATOR-DEMO Item 2)", already registered in `work/BACKLOG.md` (standalone, standard, P0). Write `work/active/WI-027_demo-constraint-execution/spec.md`.

## Required reading, in order

1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute for this session.
2. `work/orchestration/demo-constraint-execution.md` — the orchestration brief: Align rulings, graded inputs, standing bars. Everything there is load-bearing; do not re-derive or contradict it.
3. `.project/backlog/epic_stellarator_mbse_demo.md` Item 2 — the item's scope as the epic decomposed it.
4. `.project/concepts/stellarator-mbse-demo.md` criterion 2 — the governing bar, verbatim.
5. `exploration/stellarator_e2e/CODEGEN_FINDINGS.md` finding #9 — why the staged copies stripped the asserts.
6. The staged strip site: the comment at the staged `stellarator_plant.sysml:741` (under `exploration/stellarator_e2e/`).

## Outcomes to spec (spec captures outcomes; mechanism belongs to design — standing [OWNER-VERBATIM] feedback: "spec should capture the outcomes — how the model is built should be done with the expertise of SysML modeling")

1. **Criterion 2 met at the Stellaris design point**: every already-modeled assert (`net_positive`, `recirc_ok` in `mfe_plant.sysml`; the beta / wall-load / TBR asserts in the concept-09 instance) executes in the generated pipeline; verdicts (`satisfied | violated | indeterminate`) appear as data in the run report. Expected verdicts at the design point: all satisfied (the canonical model's viability currently passes — wall load 3.13 < 4.05 etc.); a violated/indeterminate verdict at the design point is a finding to surface, not to tune away.
2. **No hand-coded viability anywhere in the demo pipeline** — grep-provable absence.
3. **The staged strip retires**: the constraint-stripping comment/edit in the staged copies is gone; staged copies carry the asserts through codegen.
4. **All standing bars hold** (orchestration brief §inherited): oracle bit-exact rel 1e-9 on every executed channel; **handshake untouched under the ORIGINAL successor bar** (refinement-type item: `handshake_comparison.json` diff empty, injection-map-only edits if any); IFE anchors unchanged; offender list = the 6 pre-existing; WI-022 handwritten-impl hash survives regen; pytest tally 11/18/14/0.
5. **SV-033** registered: constraint verdicts at the design point as an executed-record validation entry.
6. **Toolchain pin recorded**: the sysml-codegen commit this item generates with, verified against what the in-repo IFE acceptance ran; the defect-register check (orchestration brief premise flag) is a named design-stage requirement.
7. **Out of scope**: new constraints (ISS04 etc. — [OWNER] 2026-07-19 Align ruling 3); study definitions (epic Item 5); any account/cost change; touching canonical `models/` semantics (regeneration consumes them as-is unless design surfaces a blocking incompatibility — which is a surface-to-orchestrator event, not a silent edit).

## Constraints

- Barred paths per PROTOCOL §3 — do not read them.
- The [OWNER] rulings in the orchestration brief are settled; carry their grades. The spec proceeds to design without an owner checkpoint (waived 2026-07-19) — so the spec must be complete enough that design needs no scope clarification.
- Python via `uv run` only.

End with ARTIFACT: <path to spec.md>.
