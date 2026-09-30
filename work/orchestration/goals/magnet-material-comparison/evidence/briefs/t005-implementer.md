# T-005 implementer brief — WI-099 magnet conductor alternatives

You are the implementing modeler for work item WI-099 in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). Another fresh agent is writing an independent oracle and the study's offer policy in parallel from the same design; you must not read their files, and they will not read your handwritten bodies. The coordinator owns the goal records, the WI `spec.md`, the integration seam and the study.

## Authority and inputs (read these)

- Released comparison contract: `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (r3).
- Reviewed model design: `work/active/WI-099_magnet-conductor-alternatives/design.md` (the equations, calc definitions, interface names and bindings you implement; follow it exactly, including § 6 names).
- Requirements: `modeling_project/REQUIREMENTS.md` MR-3, MR-4 and MR-7; `modeling_project/MODELING_PROCESS.md` § Technical Patterns (read the referenced pattern files in `.agentic-mbse/patterns/` at the point of use: `adr002-calculations.md`, `plant-idiom.md` binding rule, `expose-pattern.md`, `semantic-operators.md`, `constraints.md`).
- Working example of a new isolated package with handwritten bodies: `exploration/component_alternatives/` (`build.py`, `bodies/`, `studies/study_route.py`, `studies/interface_data.py`, `studies/prepare_interface.py`) and its sources `models/library/analyses/component_alternatives_thermal.sysml`, `models/designs/component_alternatives/plant.sysml`.
- Source citations for MR-4: the evidence notes in `work/orchestration/goals/magnet-material-comparison/evidence/sources/` and `evidence/check-*.md` name each source path and page; cite repository paths (`knowledge/sources/<slug>/...`) in SysML doc comments with Source/Reference/Basis, marking agent choices `[AGENT]` and bounded assumptions as such.
- Clean room: never open `knowledge/holdout/**` or ARIES-CS material.

## Deliverables (you own exactly these new paths)

1. `models/library/analyses/magnet_conductor_alternatives.sysml` — the calc and constraint definitions of design § 2, concept-agnostic defaults, doc comments with citations and a pointer to each body.
2. `models/designs/magnet_materials/magnet_subsystem.sysml` — design § 3 with the reference case defaults (anchor D, 10 T; the design lists them or the coordinator supplies them in `work/active/WI-099_magnet-conductor-alternatives/reference-case.json`).
3. `exploration/magnet_materials/bodies/magnet_conductor_alternatives/*_impl.py` — one handwritten body per calc (`AUTO_IMPLEMENTED = False`, `calculate(dict) -> dict`, finite-input and domain checks; domain violations produce status outputs, not exceptions, wherever the design says “unsupported”).
4. `exploration/magnet_materials/build.py` — stage exactly the two SysML sources, generate `magnet_materials_tea` with `sysml-codegen`, install bodies with typed adapters, prove a fixed point, write the snapshot, census and build-hash receipt (follow the component-alternatives build). Build evidence goes under `work/active/WI-099_magnet-conductor-alternatives/build/`.
5. `exploration/magnet_materials/studies/` — `study_route.py` (`execute_baseline`, `run_points` through stock TEAx APIs as in component alternatives), `interface_data.py` mapping every design § 6 attribute to its entry key(s) plus output channels and constraint verdict ids, `manifest.json`, and a baseline result.
6. Tests `tests/models/test_magnet_materials.py` running through the generated package: the MR-7 acceptance tests and source-data tests in contract § 5 (with the tolerances there), including insufficient/sufficient pairs for acceptance, fit, copper, steel and capacity; field varied with hardware fixed; one unsupported case per conductor with no ranking; anchor reproduction of EU DEMO layer 1 and Stellaris Table 7.
7. `work/active/WI-099_magnet-conductor-alternatives/implementation-notes.md` — what you built, commands run, results, deviations and anything unverified.

## Rules

- Run Python and tools only as `.codex-test/run python ...` or `.codex-test/run sysml-codegen ...` / `.codex-test/run syside ...` from the repository root.
- Validate with `syside check` on both SysML files, the build's fixed-point proof, the baseline execution and your tests.
- Do not modify any existing file. `git status` at the end must show only new paths you own (plus whatever others own). Do not commit.
- MR-7: no calculation writes a supplied quantity; no output is bound back as an input; nothing sets an offer, area or rating from demand.
- If a design statement is ambiguous or cannot be expressed through the toolchain, stop that part and report it; do not invent a different equation.

## Return

At most 400 words: what exists, validation results with numbers, test results, any deviation from the design, and anything unverified.
