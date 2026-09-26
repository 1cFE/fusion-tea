# Design review brief — WI-093 combination assemblies (fresh reviewer, before implementation)

You are a fresh reviewer with no prior context. Read only the files named here; do not load the goal runbook, CLAUDE.md or other goal directories. Budget: up to 16 tool calls and a 450-word return. Do not execute anything; do not edit any file. Return the exact format at the end.

## The question

Is the design at `work/active/WI-093_combination-assemblies/design.md` implementable from existing definitions exactly as written, and does it preserve design choices (MR-7: no calculation or binding silently sets an installed quantity from a required performance; every chosen quantity stays chosen)? Answer the four review questions in the design's § 10.

## Entry files and what to check in each

1. `work/active/WI-093_combination-assemblies/design.md` — the whole file (§ 1–10). `spec.md` § Requirements R1–R7 for the contract.
2. `models/library/analyses/mfe_primary_loop.sysml` lines 78–137: confirm every input named for `loop` in design § 2 is a formal of 'Primary Coolant Loop' (names end in `_in` in the definition; the design lists them without the suffix) and that `mdot`, `T_out`, `q_ihx`, `p_elec`, `q_recovered_total` are outputs; confirm the units the doc states (K, Pa, kg/s, MW).
3. `models/library/analyses/integrated_heat_electricity.sysml` lines 46–110 and 180–235, and `models/designs/aries_cs_integrated/plant.sysml` lines 244–331 and 377–424: confirm the closure's per-branch formals (available, flow, cp, ua, limit) and the electrical balance formals match design § 2 and § 3; confirm `he_limit` is a temperature in K in the ARIES assembly (729.15).
4. `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py` lines 16–40: confirm the idle-stage dummies in design § 2 (flow 1.0, cp 1.0, limit 308.15, UA 0, available 0) pass every `require` and yield a stage that transfers nothing; say whether limit 308.15 K interacts with the bracket at lines 85–86 (`hi = max(lo, limits)`).
5. `models/library/structure/mfe_plasma.sysml` lines 7–149: confirm the 'Plasma' part def's attributes the design binds with `:>>` exist (R, a, kappa, f_shape, n_e, sigma_v, E_fus, T_i0, alpha_n, alpha_T, n_e0, iota_23, f_ren, f_alpha_fast, tau_ratio_ash, f_suppr_ash, Z_eff_core, f_W_core, Ti_over_Te, B) and that `p_fus` is exposed; note whether `B` is declared as a plain attribute (bindable in a flat assembly) and whether the part def's ports need connections to generate.
6. `models/designs/stellarator_09/stellarator_plant.sysml` lines 895–1030 and 1226–1321, and `work/analysis/model-evaluation-diagnostics/baseline.json` (grep the channel names): spot-check at least six inherited values in design § 2, § 3 and § 5 (e.g. n_e0 5.06e20, T_i0 14.63, eta_is 0.772797, dp_loop_ref 329187.19, q_source 3125.932, helium_design_shaft_MW 6.26003, primary_circulators_cost 442174444.749, B_axis 9.0).
7. `models/library/analyses/mfe_power_cycle.sysml` lines 4–80 and `models/library/analyses/mfe_viability.sysml` lines 106–125 and 520–533: confirm design § 4's bindings and the 'Cycle Fit Domain' formal; confirm 'Offered Capacity Screen' and 'Offered Equipment Capacity' formals used in § 2, § 3, § 5.
8. `models/library/analyses/integrated_equipment_costs.sysml` lines 3–15 and `models/library/structure/integrated_equipment_parts.sysml`: confirm 'Selected Inventory Purchase' formals and that 'Selected Equipment' can carry `capital_cost` as § 5 binds it.
9. `modeling_project/REQUIREMENTS.md`, section MR-7 only: apply its application bullets to design § 6.

## Exclusions

Do not assess whether the combinations are physically sensible; do not review the goal's other evidence; do not propose new definitions; do not check codegen behaviour beyond what the cited files show.

## Return format (≤ 450 words)

```
Verdict: PASS | FINDINGS | OWNER_GATE
Q1 bindings/units: <per assembly: ok | <formal or unit problem, file:line>>
Q2 MR-7: <compliant | violated: <which quantity, why> | unverified: <what>>
Q3 inherited values: <each spot-checked value: confirmed / mismatch with the cited value>
Q4 new relationship in disguise: <none | <which>>
Idle-stage dummies: <pass every require: yes/no; bracket note>
Findings: none | <numbered, one line each, blocking or note>
Missing evidence: none | <what>
```
