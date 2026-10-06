# Probe P5 — per-case time for three plant instances

Design § 7 P5 (K21). Run 2026-09-30 on scratch packages with the 51 stellarator_e2e manual bodies (prefix-rewritten), their `financial_factors.py` helper, and draft bodies B1 and B2 installed, then regenerated with `--smart-regen --preserve-handwritten` (stencils: 0 new, all preserved).

## What was run

`sources/p5_timing.py` loads a package through the stock strict loader (`exploration/stellarator_e2e/studies/study_route.py:207-247`) and runs 20 proposals (turn current 50 kA to 50.95 kA) through the stock `StudyRunner` into a fresh store, timing preparation and the run.

| Package | Instance | Cases | Prepare | Per case (runner, store included) | States |
|---|---|---|---|---|---|
| hunked reference `stellarator_materials_reference_tea` | `stellaris` | 20 | 1.34 s | 1.51 s | all completed |
| single material probe `stellarator_materials_tea` | `probe_a` (both retypes) | 20 | 1.38 s | 1.49 s | all completed |

Raw: `evidence/p5_reference_instance_timing.json`, `evidence/p5_material_instance_timing.json`.

## Result

About 1.5 s per plant evaluation. A three-instance case would have cost about 4.5 s, so contract § 5's order 10⁴ policy evaluations would take about 12.5 h of evaluation against about 4.2 h with one material instance per case.

P2 found that the three-instance package cannot be generated at all, so the K21 fallback (per-instance packages from the same staged tree) is taken for that reason (see P2). With it, a case evaluates exactly one plant, at about 1.5 s.
