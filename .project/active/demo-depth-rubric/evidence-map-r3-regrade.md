# Evidence map — Row 3 re-grade (pointers only)

**Author:** the WI-035 author (goal `magnet-closure` round 2, T-001), 2026-08-30. Per the grading protocol § 2 this map carries pointers and no proposed scores; the grader cites what it actually read. The v1 map (`evidence-map.md`) still covers the other rows; this file adds the post-WI-035 Row-3 surfaces.

## The yardstick

- `rubric.md@dc0f0b6d` § Row 3 (anchors; the P2/P3 and S2/S3 tests) and § Grading protocol.
- Prior cells for the delta: `grading.md` § Row 3 (`R3.P`, `R3.S`) and grader notes G5/G6; author dispositions.

## Declared structure (canonical models/)

- `models/library/analyses/mfe_magnet_field.sysml` — 'Coil Set Axis Field' (field from n_coils, I_coil, k_link, R0), 'Winding Pack Stress' (the computed operand).
- `models/library/analyses/mfe_viability.sysml` — 'Winding Pack Stress Limit' (the new constraint def, at the end of the file).
- `models/library/analyses/mfe_magnet_cost.sysml` — 'Winding Pack Cost', 'Magnet Structure Cost', 'Magnet Capital' (rollup), and the retained 'Magnet Coil Cost' with its comparison-channel doc.
- `models/library/analyses/mfe_cryo_plant.sysml` — the computed cryo chain (unchanged; grader note G5 context).
- `models/library/analyses/mfe_account_costs.sysml` — 'Aux Cooling Cost' split outs (`aux_cost`/`cryo_cost`); 'Power Supplies Cost'.
- `models/library/cost_structure/mfe_power_core.sysml` — 'Magnet System' attribute set (the twelve WI-035 parameters).
- `models/designs/generic_mfe/mfe_plant.sysml` — `field_calc`, the `:>> B = field_calc.B_axis` EXPOSE in the magnet part, `wp_stress`, `assert wp_stress_ok`, the decomposed cost calcs and `magnet_capital_rollup`, exposures `magnet_capital_1cfe` and `cryoplant_capital`.
- `models/designs/stellarator_09/stellarator_plant.sysml` — the retired `B` binding note and the twelve literal bindings with image-cited docs (search "WI-035 coil-set current").

## Runtime and executed behavior

- Package identity: `work/orchestration/goals/magnet-closure/evidence/T-004_integration_return.json` (CANDIDATE, ten gates) — semantic `819a5a05…`, executable `75f90a24…`.
- Baseline: `exploration/stellarator_e2e/studies/20260830-stress-fence/results/baseline_result.json` — channels (`field_calc__B_axis`, `peak_field_calc__B_peak`, `wp_stress__sigma_wp`, `winding_pack_cost__cost`, `magnet_structure_cost__cost`, `magnet_capital_rollup__capital_cost`, `magnet_cost__capital_cost`) and seven verdicts.
- Entry-point census: `tests/models/data/mfe_census.json` (`magnet__B` absent; the twelve levers present).

## Load-bearing study evidence

- `exploration/stellarator_e2e/studies/20260830-stress-fence/record.md` §§ 3, 4, 6, 13 and Addendum; `synthesis.md` (independent recount); `results/points.csv` (per-point verdicts).
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — rows `20260830-stress-fence#1`/`#2` (what is still held) and the `20260823-magnet-technology-ab#3`/`#4` dispositions of 2026-08-30.

## Item record and validation

- `work/active/WI-035_magnet-closure/` — spec (checkpoint ruling), design (D1–D8, esp. D2 field path, D3 limit, D4–D7 decomposition), plan § Implementation record.
- `modeling_project/VALIDATION_MATRIX.md` — SV-038/039/040 rows and status; the Round 1 review's caveat on SV-040's cryoplant conjunct (trail, "Not findings, but worth carrying").
- Goal context: `work/orchestration/goals/magnet-closure/goal.md` § Answered when; `learnings.md` § Round 1.
