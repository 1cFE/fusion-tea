# Brief — /design-model — WI-027 Demo Constraint Execution (STELLARATOR-DEMO Item 2)

Design the mechanism for WI-027. Spec: `work/active/WI-027_demo-constraint-execution/spec.md` (MR-1…MR-8, all outcome-level — the mechanism is yours). Write `work/active/WI-027_demo-constraint-execution/design.md`.

## Required reading, in order

1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute.
2. `work/active/WI-027_demo-constraint-execution/spec.md` — the outcomes you are designing for.
3. `work/orchestration/demo-constraint-execution.md` — Align rulings, graded inputs, standing bars, the premise flag you must discharge.
4. The proven in-repo precedent: the IFE constraint-execution acceptance in the primary checkout — `~/1cfe/fusion-tea/exploration/ife_e2e/` (study/, generated_bridged/, pkg_bridged/, outputs). This is the working example of constraint lowering + verdict reporting + study-layer execution against a fusion model in this codebase. Study how it generated, sealed, and executed before designing our path.
5. `exploration/stellarator_e2e/` — the current staged demo chain this item modifies (bridge script, staged copies with the strip sites, runner, oracle, handshake).

## Design must settle (mechanism decisions, each with rationale and rejected alternative where real)

1. **Generation path**: how the stellarator staged package regenerates with constraint lowering — same snapshot+bridge chain as today (`bridge_v11_generate.py`, `preserve_handwritten=True`) with constraints no longer stripped, vs adopting the IFE acceptance's bridged-generation path. Whichever you pick must preserve the WI-022 handwritten-impl hash and the regen-stability bars (MR-5).
2. **Verdict surface (MR-1/MR-4)**: where verdicts appear — the report aggregator module the toolchain generates, how `run_stellaris.py` (or a successor runner step) captures them into the run report, and the exact report shape SV-033 will record. Violated-never-raises semantics per the toolchain contract.
3. **Oracle treatment**: the pure-Python oracle mirrors executed channels at rel 1e-9 — decide whether the oracle asserts verdicts too (recommended if cheap: verdicts are data) or verdict parity is checked by a dedicated assertion in the runner; either way MR-5's bit-exactness on numeric channels is untouched.
4. **Pin + defect register (MR-6/MR-7)**: record the sysml-codegen commit you generate with; reconcile with what the IFE acceptance ran; walk the remediation epic's defect register (`~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md` + its research doc) against our five predicates and the constructs the generation path exercises (occurrence expansion, snapshot replay, path portability are among the Mediums). Record each as hit/not-hit with a one-line reason. A hit → stop and surface to the orchestrator (premise flag), do not design around it silently.
5. **Staged-twin discipline**: the staged `mfe_plant.sysml` / `stellarator_plant.sysml` twins have known DEMO NOTE divergences (per-edit-region identity, orchestration brief §inherited). Define the twin diff-bar for this item's edits (strip sites retire; what else may differ: nothing).
6. **Validation design**: SV-033's executed record shape; which existing SVs re-verify (SV-025/026 handshake byte-identity under the original bar, SV-023 IFE anchors); the L1–L6 expectation (offender list = the 6 pre-existing, zero new).

## Constraints

- Barred paths per PROTOCOL §3.
- Prototype-before-commit per the design-model methodology where a construct is unproven — but note the constraint-exec constructs are proven by the IFE acceptance; reuse its evidence rather than re-spiking what it already proved. New-to-stellarator seams (handwritten-impl coexistence with constraint modules, the V11 bridge vs constraint sections) are the ones worth a cheap prototype if uncertainty remains after reading the IFE artifacts.
- No design work on out-of-scope surfaces (new constraints, studies, account changes — spec Out of Scope).
- Python via `uv run` only. `SYSIDE_LICENSE_KEY` via `.env` if you run syside.

End with ARTIFACT: <path to design.md>.
