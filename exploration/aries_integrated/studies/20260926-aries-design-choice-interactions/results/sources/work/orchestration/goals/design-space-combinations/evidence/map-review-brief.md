# Review brief — compatibility map (T-001, fresh reviewer)

You are a fresh reviewer with no prior context. Do not load the goal runbook, the project CLAUDE.md or other goal directories; read only the files named here. Budget: up to 14 tool calls and a 400-word return. Return the exact format at the end.

## The question

Are the interface and operating-range claims in `work/orchestration/goals/design-space-combinations/evidence/compatibility-map.md` § 1 and § 2 true of the code as committed, and does each classification (compatible / incompatible / new behavior; inputs / assembly / none) follow from the line it cites? You are checking claims about code, not judging whether the combinations are physically wise.

## Entry files and the claims to check

1. `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py` lines 16–68: (a) all three branches require positive flow, cp and limit; (b) UA and available heat may be zero; (c) a zero-UA branch yields coefficient 0, capability 0, transferred 0, `state_defined` 0, and passes the secondary temperature through unchanged; (d) the bracket runs from `cold_temperature` to the highest branch limit.
2. `exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py` lines 60–110: (a) the IHX hot approach is `helium_hot_K − 738.15` and the cold approach `helium_suction_K − 543.15`, and a nonpositive approach raises; (b) salt flow is `q_ihx/(1560×195)`; (c) `salt_return_C` is computed from 270 minus a pump-work term. Confirm that no input to this body sets the salt hot temperature.
3. `exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py` lines 160–200 and 73–76: (a) pressures must equal 6.2/0.8 MPa; (b) steam and reheat superheated and ≤ 455 °C; (c) condenser 20–60 °C; (d) salt heat must equal heat available within `max(1e-8, 1e-12·scale)`; (e) the pinch gap is reported, not raised on.
4. `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml` lines 960–990: `salt_hot_C_in` comes from the entry key `mfe_plant_systems_params.stellarator_09__stellaris__heat_transport__salt_hot_C`, while `salt_return_C_in`, `heat_available_MW_in` and the salt flow come from computed equipment channels. This is the basis of map rows H2 and O2 (lowering `salt_hot_C` alone breaks the salt heat join).
5. `models/library/analyses/mfe_power_cycle.sysml` lines 4–50 and `models/designs/stellarator_09/stellarator_plant.sysml` lines 811–830: T2 = T_hot − dT_approach − 273.15 with dT_approach 20 K and the domain [384, 642] °C; outside the domain the value is published and a constraint reads violated (map rows H6, H7).
6. `models/designs/generic_mfe/mfe_plant.sysml` and `mfe_subsystems.sysml`: `grep -n "plasma\." ` — confirm the plant consumes `plasma.p_rad`, `plasma.p_aux_required`, `plasma.p_alpha_heat`, `plasma.n_T0`, `plasma.fuel_volume` besides `plasma.p_fus` (map row P2); and `models/library/analyses/supplied_profile_plasma.sysml` lines 31–52: the ARIES profile calc publishes none of those five (row P2).
7. `models/designs/aries_cs_integrated/plant.sysml` lines 15–26 and 110–140: the source selector reads `plasma.fusion_power_MW`; 'Fuel Cycle Flows' and 'Integrated Heat Source' take fusion power in MW and nothing else from the core (row P1).

## Original evidence

The files above are the original evidence; the map cites nothing outside the repository. `choice-inventory.md` § 1 (same directory) is the map's vocabulary; read its rows S-C1, S-V1, S-V0, A-C1, A-V1, A-P1 only if a claim needs it.

## Expected checks and exclusions

Check each numbered claim against the cited lines and say true / false / not decidable from the cited lines. Then say whether any row of § 2 is misclassified given what you found, naming the row and the reason. Exclusions: do not execute any package; do not assess physical merit or cost; do not review the inventory's mechanical § 2; do not propose new model behavior.

## Return format (≤ 400 words)

```
Verdict: PASS | FINDINGS | OWNER_GATE
Claims: 1a true/false/undecidable — <one line>; 1b …; … 7 …
Misclassified rows: none | <row>: <reason>
Missing evidence: none | <what you could not find>
Notes: <at most three lines>
```
