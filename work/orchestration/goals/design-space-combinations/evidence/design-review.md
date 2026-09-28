# Fresh design review — WI-093 combination assemblies

Reviewer: fresh non-author session (Claude Code `Agent`, general-purpose), dispatched 2026-09-26 with `evidence/design-review-brief.md`. Return deposited verbatim by the coordinator; the coordinator's dispositions follow the return.

## Return (verbatim)

Verdict: FINDINGS

Q1 bindings/units: C-1 ok — all 16 loop inputs are `*_in` formals, outputs mdot/T_out/q_ihx/p_elec/q_recovered_total exist, MW/K/Pa/kg/s as stated (mfe_primary_loop.sysml:78-136); 'Network Heat Driven Closure' formals match (integrated_heat_electricity.sysml:114-138); 'Plant Electrical Balance' formals match (200-215); he_limit = loop.T_out is K like ARIES 729.15 (plant.sysml:249). C-2 ok — every `:>>` attribute exists in 'Plasma', B is a plain attribute, p_fus exposed (mfe_plasma.sysml:23-84); 'Fusion Source Selector' formals calculated_power_in/reference_power_in/mode_in (plant.sysml:20-23). C-4 ok — ten 'Power Cycle Efficiency' formals, domain_product → 'Cycle Fit Domain' (mfe_power_cycle.sysml:52-79; mfe_viability.sysml:532). C-5 ok — 'Selected Inventory Purchase' formals (integrated_equipment_costs.sysml:5-9); capital_cost/cas_code come from 'Costed Component' (costed_component.sysml:17-18), bound as ARIES he_hx (plant.sysml:725,740).

Q2 MR-7: compliant. No binding derives a rating, area, flow capacity or ratio from demand; loop mdot direction disclosed; C-5 capital follows selected_rating. Disclosure gaps in findings 3-4.

Q3 inherited values: confirmed — n_e0 5.06e20, T_i0 14.63 and all other plasma values (stellarator_plant.sysml:898-1016); T_in 573.15, dT 200, cp 5193, gamma 5/3, p 8e6, n_loops 14, mdot_loop_ref 225.0778, dp_loop_ref 329187.1857, eta_is 0.7727966, eta_drive 1, loop_live 1 (1226-1321); mdot_loop_rated 225.0778 (1171); Kovari fit values and cycle_live/eta_th_direct/delta_eta (811-834); baseline q_source 3125.9322770825056, helium_design_shaft_MW = circulator_shaft_MW 6.26003337158886, primary_circulators_cost 442174444.749, p_fus 2652.56; B_axis 8.999999999999998 (9.0 is rounding). ARIES cycle values, ratio, area/U, auxiliary_heat 20, reference 2436, limits 729.15/973.15/1011.15, ratings 1600/3500/1800/2500/1500 → compressor/turbine/generator/rejection/he (plant.sysml:144-257, 551-691). Mismatches: "tolerance 1e-6 [INHERITED: ARIES energy_tolerance]" — ARIES binds no 1e-6; energy_tolerance is a ledger output (plant.sysml:514). Source mode 1 graded [INHERITED: ARIES] but ARIES producer_mode is 0 (plant.sysml:18).

Q4 new relationship in disguise: none blocking. C-1 replaces two ledger outputs with assembly expressions: rejection demand = precooler + intercoolers (ARIES reads plant_ledger.cycle_rejection) and a literal tolerance; state them as such.

Idle-stage dummies: pass every require: yes. UA 0 → ntu 0 → effectiveness 0 → coefficient 0 → cap 0, q 0, defined False, secondary passes through (impl:41-63). Bracket: hi = max(lo, 773.15, 308.15, 308.15); lo is compressor_3 outlet > 308.15, so 308.15 never sets it; hi becomes loop.T_out.

Findings:

1. note — § 1 puts 'Heat Removal Adequate' in mfe_viability; it is integrated_heat_electricity.sysml:343 (formals unmet_in, tolerance_in).
2. note — energy_tolerance 1e-6 is not an ARIES-bound value; regrade [ASSUMED] or cite the ledger body.
3. note — re-selected ratings 3200/7000/3600/5000/3500 and ratio 1.35 carry [ASSUMED] without the R4 reason; he 3500 sits just above q_ihx ≈ 3301 MW, so state it is an analyst re-selection informed by the screen.
4. note — C-1 turns ARIES's chosen he_flow (plant.sysml:246) into calculated loop.mdot; MR-7 asks that this role change be called out. The loop's mdot_loop_rated ceiling (capacity_margin) has no screen in C-1's checks.
5. note — C-2 staging must include mfe_interfaces (port types, mfe_plasma.sysml:3), mfe_plasma_scaling and mfe_plasma_sustainment; whether codegen needs the four ports connected is not determinable from the entry files.
6. note — C-5 pairs a per-circulator shaft channel with a total cost (circulator_count 28 in the same channel family); state the basis.

Missing evidence: 'Net Power Positive' formal names (mfe_viability.sysml:141, doc block only); whether 'Plant Electrical Balance' adds pump_recovered_in to heat (body outside entry files), which decides if he_available = q_ihx plus pump_recovered = q_recovered_total double-counts.

## Coordinator dispositions — 2026-09-26

Verdict accepted: FINDINGS, none blocking, no owner gate. Every note applied to `work/active/WI-093_combination-assemblies/design.md` (Updated 2026-09-26). Q1 (bindings and units) and Q4 (no new relationship in disguise) PASS as returned; Q2 MR-7 compliant with the two disclosure gaps closed below; Q3 two grade mismatches corrected.

| # | Note | Disposition |
|---|---|---|
| 1 | 'Heat Removal Adequate' lives in `integrated_heat_electricity.sysml:343`, not `mfe_viability` | Corrected in § 1 (both C-1 and C-2 rows). |
| 2 | energy_tolerance 1e-6 is not an ARIES-bound value | Regraded `[ASSUMED]`: the floor of the ledger body's rule `max(1e-6, 1e-9 × supplied heat)` (`integrated_plant_ledger_impl.py:43`); ARIES reads the ledger output (`plant.sysml:514`), which C-1 does not assemble; the closure's own residual contract is 1e-6 MW (`network_heat_driven_closure_impl.py:99`). § 2 checks row. |
| 3 | re-selected ratings and ratio carry `[ASSUMED]` without the R4 reason | Reasons added in § 2 (cycle, ratio and ratings rows) and § 6: analyst re-selection informed by the round-1 screen's demands at 2,500 kg/s; each a case input chosen so installed equipment covers the observed demand; the 3,500 MW helium rating sits just above q_ihx ≈ 3,301 MW; none computed from a demand inside the model. |
| 4 | C-1 turns ARIES's chosen he_flow into calculated loop.mdot; no screen on the loop's rated-flow ceiling | Role change called out in § 2 (loop row) and § 6. `loop_capacity_ok : 'Loop Capacity'` (`mfe_viability.sysml:499-518`, asserted by the generic plant at `mfe_plant.sysml:884`) added to C-1's checks on mdot_loop against mdot_loop_rated; § 1 table, § 7 count (23) and § 8 identity updated. |
| 5 | C-2 staging must include `mfe_interfaces`, `mfe_plasma_scaling`, `mfe_plasma_sustainment`; port connection need undeterminable from the entry files | Staged list written out in § 1 (all three present in the build's LIBRARY list). Ports resolved: they are declarative (WI-057); the generic plant binds only `B` on its plasma part and connects ports at plant level (`generic_mfe/mfe_plant.sysml:81-84`, `:270-272`); the generated Stellaris package carries no port artefact (grep of `exploration/stellarator_e2e/generated/stellarator_tea/modules` for "port": none), so an unconnected `part plasma : 'Plasma'` is a shape the generator already accepts. |
| 6 | C-5 pairs a per-circulator shaft channel with a 28-machine total cost | Basis stated in § 5: the Stellaris body reports shaft per machine (primary shaft ÷ (2 × n_loops), `cooling_equipment_impl.py:55, 61`) and the cost as the 28-machine total whose size argument is the per-machine design shaft (`:58-61`); C-5's linear law scales the fleet cost with the per-machine rating at fixed count 28; the Stellaris law's 0.28 exponent makes the two differ off the reference point, reported as a finding of the cases. |

Q4 assembly expressions stated as such in § 2 (ratings row): the rejection demand `-(intercooler_1 + intercooler_2 + precooler heat_into_fluid)` reproduces the ledger's cycle_rejection formula (`integrated_plant_ledger_impl.py:31`) at part level with a named fallback (drop the screen with reason if the generator refuses the expression); the tolerance literal as in note 2.

Missing evidence resolved by the coordinator against the bodies:

- 'Net Power Positive' has one formal, `net_electric` (`mfe_viability.sysml:153`); the design's binding `net_electric = electrical.net_electric` is right.
- 'Plant Electrical Balance' does not add pump_recovered to any heat: it guards `pump_recovered <= pump_electric` and reports `pump_loss = pump_electric − pump_recovered` (`plant_electrical_balance_impl.py:11, 25`). The loop's friction heat enters the cycle once through q_ihx = q_source + w_fluid (`primary_coolant_loop_impl.py:51`), so he_available = q_ihx with pump_recovered = q_recovered_total does not double-count. Recorded in § 8.

Residual uncertainty for the implementation review: whether the stock generator accepts the three-term part-level sum for the rejection demand (fallback named); whether the multi-package staged tree generates one pipeline (a strategy assumption).
