# Map review — fresh reviewer return (T-001)

[AGENT: fresh reviewer, no inherited context] Brief: `map-review-brief.md`. Twelve tool calls. Returned 2026-09-26, verbatim below; the coordinator's application follows.

```
Verdict: FINDINGS
Claims:
1a true — closure_impl.py:33-35 require flow, cp, limit > 0 for each of BRANCHES = ('he','divertor','pbli') (line 14).
1b true — line 36: ua ≥ 0 and available ≥ 0.
1c true — UA 0 gives ntu 0, effectiveness 0, coefficient 0 (38-45); stage() then gives cap 0, q 0, defined False, state_defined 0.0, secondary_out = secondary + 0/cs (49-58).
1d true, but outside the cited 16-68: lo = cold_temperature, hi = max(lo, branch limits) at 85-86; bisection 87-97. The map's ":57-68" cite for the root solve is off.
2a true — cooling_equipment_impl.py:72-73.
2b true — line 91.
2c true — line 106. No input names a salt hot temperature anywhere in the file (grep salt_hot: none); 465 is a literal at 90, 91, 148 (148 compares input sourcefitargument_C against 465; it does not set it).
3a true — 170-171.
3b true — 185-188; the reheat lower bound is the extraction saturation liquid endpoint's temperature.
3c true — 189-190.
3d true — 174-180 with balance() at 73-76; salt_flow = per_circuit × circuit_count (174).
3e true — heat_profile returns (minimum, 0., False) on a nonpositive gap (145-146), written to main_min_gap_K / main_admission_ok (261, 269); none of the 23 raises (48-272) keys on the gap.
4 true — pipeline.yaml:977 salt_hot_C from mfe_plant_systems_params; 967 salt_return_C, 969 ihx_count, 973 conversion_heat_MW, 976 salt_flow from the equipment module. salt_cp_kJ_kgK (982) is also an entry key. H2/O2 basis follows: salt flow is fixed for a 195 K rise, so lowering salt_hot_C alone leaves a residual far above tolerance.
5 partly undecidable — T2 formula mfe_power_cycle.sysml:9; dT_approach 20 at stellarator_plant.sysml:817; T2_min 384 at 827; T2_max 642 at 831 (outside cited 811-830). Values published: calc outputs margin_low/high and domain_product (76-78); doc says eta_fit is never clamped (26-28). "Constraint reads violated": undecidable — no constraint def or usage named 'Cycle Fit Domain' (or on domain_product) exists in either named file; only the doc comment at 26-27 asserts it.
6 true — mfe_plant.sysml reads plasma.fuel_volume (115), n_T0 (116), p_alpha_heat (155), p_aux_required (156), p_rad (159), plus alpha_n (117), R, a, kappa; mfe_subsystems.sysml has comments only. supplied_profile_plasma.sysml:45-52 publishes none of the five. The map's "14 references" does not match the grep (21 lines).
7 true — plant.sysml:20 is the file's only plasma. read; 'Integrated Heat Source' (45-59+) and 'Fuel Cycle Flows' (122-135) take source.selected_power plus literals/fuel_inventory. The map's cite ":122-135" covers only the fuel block.
Misclassified rows: none. H7's classification (T2 680/718 > 642) follows from the cited values; its stated mechanism ("the domain constraint reads violated") is unevidenced in the named files (see 5). Same for § 1's S-V0 bullet.
Missing evidence: a 'Cycle Fit Domain' constraint definition and its binding on the Stellaris instance — absent from mfe_power_cycle.sysml and stellarator_plant.sysml.
Notes: Line cites drift in 1d, 5 and 7 without changing substance. The fixed salt window is consistent with code: conversion_heat = q_ihx + shaftsalt equals salt_heat only at hot 465 °C with cp 1.56 kJ/kgK. A-P1 also omits alpha_n, which the plant reads (117); this strengthens P2.
```

## Coordinator application

- No row is misclassified; the map's classifications stand.
- Line cites corrected in `compatibility-map.md`: closure bracket and bisection at `network_heat_driven_closure_impl.py:85-97`; T2_max at `stellarator_plant.sysml:831`; the ARIES source read at `plant.sysml:20` and 'Integrated Heat Source' at `:45-59`; the plant's plasma reads counted as 21 grep lines with the five consumed quantities named.
- The 'Cycle Fit Domain' constraint: located by the coordinator outside the reviewer's named files (see the correction note in the map); the S-V0 bullet and row H7 now cite the actual constraint or, where none is bound, say that only the calc outputs (`margin_low`, `margin_high`, `domain_product`) carry the domain and no verdict reads them.
- P2 strengthened: A-P1 also omits `alpha_n`, which the plant reads at `mfe_plant.sysml:117`.
