# WI-073 exact interface contract

[AGENT; independently reviewed implementation contract] Names below are canonical SysML scalar names before generator sanitization. All module inputs use the suffix `_in`; listed outputs do not. `Real` means finite real unless inactive as specified. Units are explicit even where existing code generation represents them as `Real`. No state output is a free input. The component and module names fix ownership; the generated entry-point inventory will verify bindings rather than guess flattened names.

## Matched Steam Cycle

Place the new manual `calc def 'Matched Steam Cycle'` in `models/library/analyses/mfe_matched_steam_cycle.sysml`; occurrence `turbine.matched_cycle`. Fixed one-heater/one-reheat topology. No production no-reheat selector; that remains a retained diagnostic reference.

| Input name without `_in` | Unit | Owner/binding |
| --- | --- | --- |
| enabled | 0 or 1 Real | `turbine.matched_cycle_enabled`, generic 0/current stellarator 1 |
| source_heat_MW | MW | `heat_transport.q_source`, existing reactor source producer |
| selected_recovered_MW | MW | `heat_transport.q_recovered_total`, mode-selected primary/secondary recovered heat |
| heat_available_MW | MW | `heat_transport.conversion_heat_MW`, pure alias of `equipment.conversion_heat_MW` |
| salt_flow_per_circuit | kg/s | `heat_transport.salt_flow_per_circuit`, alias of `equipment.salt_flow` |
| salt_circuit_count | count | `heat_transport.salt_circuit_count`, alias of `equipment.ihx_count` = n active circuits; `salt_pump_count` = 2n is deliberately not this quantity |
| salt_hot_C | °C | `heat_transport.salt_hot_C`, the existing equipment's 465°C fixed scenario, exposed as a named fact |
| salt_return_C | °C | `heat_transport.salt_return_C`, alias of `equipment.salt_return_C` before pumping |
| salt_cp_kJ_kgK | kJ/(kg K) | `heat_transport.salt_cp_kJ_kgK`, existing equipment's 1.560 fixed scenario |
| main_pressure_MPa | MPa | main SG component fact, fixed 6.2 |
| extraction_pressure_MPa | MPa | heater component fact, fixed 0.8 |
| steam_temperature_C | °C | main SG component fact, current 445 |
| reheat_temperature_C | °C | reheater component fact, current 445 |
| condenser_temperature_C | °C | condenser component fact, current 42 |
| eta_hp | 1 | HP turbine fact, current 0.90 |
| eta_lp | 1 | LP turbine fact, current 0.90 |
| eta_condensate_pump | 1 | condensate pump fact, current 0.80 |
| eta_feedwater_pump | 1 | feedwater pump fact, current 0.80 |
| eta_pump_motor | 1 | water pump motor fact, current 0.95 |
| eta_mechanical | 1 | generator shaft boundary fact, current 0.99 |
| eta_generator | 1 | generator fact, current 0.98 |

[AGENT] Existing handwritten cooling implementation line 93 publishes `salt_flow=loopflow`, `ihx_count=n`, `salt_pump_count=2*n` and `salt_pump_flow=loopflow/2`. Thus 14 active circuits and 28 installed duty pumps give the existing total salt flow by `salt_flow*ihx_count`, not by pump count. Test this identity at baseline and a nondefault loop count. All fixed/current values are model facts with sources or assumption comments, not hidden handwritten defaults.

Scalar state outputs are exactly `p_<state>_MPa`, `h_<state>_kJ_kg`, `mdot_<state>_kg_s` for each state in `{feed, main, hp, reheat, lp, condensate, condensate_pumped, heater}`. Additional `t_<state>_C` and `s_<state>_kJ_kgK` exist for all of those states EXCEPT `condensate_pumped`. Its pressure, enthalpy, mass flow and pump work are supported by the incompressible model; its compressed temperature and entropy are deliberately not declared. This prevents the 40°C missing benchmark from becoming invented zero properties. The feed-pump outlet does lie in the 6.2 MPa liquid table and has temperature/entropy outputs. `mdot_hp_kg_s` denotes full flow before splitting; `mdot_reheat_kg_s` denotes unextracted flow. Separate `mdot_bleed_kg_s` carries the heater extraction flow.

Other Real outputs are exactly: `bleed_fraction`, `mdot_bleed_kg_s`, `salt_flow_total_kg_s`, `salt_main_flow_kg_s`, `salt_reheat_flow_kg_s`, `q_main_MW`, `q_reheat_MW`, `q_condenser_MW`, `p_hp_shaft_MW`, `p_lp_shaft_MW`, `p_condensate_shaft_MW`, `p_feedwater_shaft_MW`, `p_condensate_electric_MW`, `p_feedwater_electric_MW`, `p_cycle_pumps_MW`, `p_gross_MW`, `eta_gross`, `p_cycle_net_before_cooling_MW`, `q_mechanical_loss_MW`, `q_generator_loss_MW`, `q_pump_motor_loss_MW`, `q_rejection_before_cooling_MW`, `lp_quality`, `lp_moisture_fraction`, `main_min_gap_K`, `reheat_min_gap_K`, `main_UA_MW_K`, `reheat_UA_MW_K`, `salt_heat_residual_MW`, `heater_mass_residual_kg_s`, `heater_energy_residual_MW`, `cycle_shaft_residual_MW`, `cycle_electric_residual_MW`.

Boolean outputs are exactly: `active`, `main_UA_available`, `reheat_UA_available`, `main_admission_ok`, `reheat_admission_ok`, `turbine_equipment_qualified`, `installed_sg_capacity_qualified`. The two qualification outputs remain false, including when the bounded state calculation succeeds. They are limitations, not newly failing numerical checks. No moisture acceptance predicate exists. Admission tests are strictly `min_gap > 0`; retain the raw margin. The 20 K nominal approach is a selected state consequence, not an added global threshold. Undefined UA at nonpositive gaps uses value 0 with availability false, never a claimed zero conductance. Disabled mode returns all numeric outputs 0, all Booleans false, and `active=false`; these are inactive schema placeholders, not physical predictions or passing checks.

## Cooling Water Rejection

New manual `calc def 'Cooling Water Rejection'` in the same library file; occurrence `heat_rejection.cooling_water`. Inputs (suffix `_in`) are exactly `enabled` [0/1], `cycle_active` [0/1], `q_rejection_before_cooling_MW` [MW], `condenser_temperature_C` [°C], `water_inlet_C` [°C], `water_outlet_C` [°C], `head_m` [m], `eta_pump` [1], `eta_motor` [1]. Current selected reference scenario is 1, 25°C, 35°C, 20 m, 0.80, 0.95; generic enable is 0. `cycle_active` binds to an explicit numeric mode alias, not an implicit Boolean-to-Real coercion. Enabling cooling while the matched cycle is disabled is a mode refusal.

Real outputs are exactly `water_flow_kg_s`, `p_cooling_pump_shaft_MW`, `p_cooling_pump_electric_MW`, `q_cooling_motor_loss_MW`, `q_total_rejection_MW`, `water_pump_rise_K`, `condenser_water_gap_K`, `water_energy_residual_MW`, `denominator_kJ_kg`. Boolean outputs are `active`, `reference_scenario`, `site_qualified`, `cooling_approach_ok`. A selected valid calculation reports `reference_scenario=true` and `site_qualified=false`. A nonpositive approach remains a raw negative/zero diagnostic and `cooling_approach_ok=false`; nonpositive denominator or nonfinite/nonpositive flow is an explicit numerical/domain refusal. No fictitious finite flow is substituted. Inactive module returns zero numerics/false Booleans before property access. Both pump shaft work and motor loss enter the water heat balance. `water_pump_rise_K` is the diagnostic `(1000*p_cooling_pump_electric_MW/water_flow_kg_s) / ((h_water_out-h_water_in)/(water_outlet_C-water_inlet_C))`: apparent rise using the mean liquid heat capacity over the selected span, not a separate exact local pump-outlet state.

## Cycle Mode Selection and power balance

New manual `calc def 'Cycle Mode Selection'` in the same file; occurrence `turbine.cycle_selection`. Inputs are `matched_enabled_in`, `legacy_eta_in`, `matched_eta_in`, `legacy_domain_product_in`. Outputs: `eta_selected` [Real], `legacy_domain_applicable` [Boolean], `matched_domain_applicable` [Boolean]. There is no new green substitute for the legacy raw domain product. `turbine.eta_th` aliases `eta_selected`. `turbine.domain_product` and `turbine.cycle_argument` remain raw old-calculation aliases with legacy applicability attached in diagnostics. Legacy `cycle_live` and `eta_th_direct` retain their existing exact formula and meaning.

`MFE Power Balance Calc` adds exactly `p_cycle_pumps_in` and `p_cooling_water_in` [MW, generic defaults 0]. Recirculating power adds both once. Keep `p_the=eta_th_in*p_th` and independently verify `p_the=matched_cycle.p_gross_MW` using equal admitted-heat bases in matched mode. Preserve zero-demand legacy arithmetic with an explicit zero-addition branch if needed for the historical floating comparison policy; do not rewrite old anchors. No new cycle-net efficiency enters this channel.

## Component and port bindings

Add `mfe_steam_cycle_components.sysml` under `models/library/structure/`. Reuse definitions for turbines and pumps. Occurrences remain under the existing CAS23 `turbine`: `main_steam_generator`, `hp_turbine`, `reheater`, `lp_turbine`, `open_feedwater_heater`, `condenser`, `condensate_pump`, `feedwater_pump`, `generator`. Each has actual state/flow/work/duty aliases from the above outputs. Full state mapping: SG feed→main; HP main→hp with separate bleed flow; reheater hp→reheat with unextracted flow; LP reheat→lp; condenser lp→condensate; condensate pump condensate→condensate_pumped; open heater condensate_pumped plus hp bleed→heater; feedwater pump heater→feed. Generator consumes the two turbine shaft outputs and exposes gross output and separate mechanical/generator losses. Heat rejection owns `circulating_water_pump` with flow and shaft/electric work, and the environmental heat output.

Water ports carry only always-supported pressure [MPa], specific enthalpy [kJ/kg] and mass flow [kg/s]. Temperature and entropy remain named component-state properties where supported, rather than universally promised port fields. Extend existing interfaces with a heat-duty port [MW] and shaft-power port [MW]; reuse Electric Port. Connect salt supply/return through explicit split/join ports on the matched assembly to SG/reheater, with each branch flow bound above. Connect turbine shafts to generator, condenser plus conversion-loss heat to rejection, and electric-plant recirculating supply to both cycle pump input and heat-rejection pump input. Physical ports are declarative; scalar bindings execute. No component result feeds back as a separate solver input.

[AGENT; fresh-review released correction] Active matched mode requires admitted equipment heat to equal `source_heat_MW + selected_recovered_MW` under the existing arithmetic closure tolerance before property work. This prevents mixed historical/current heat modes from producing contradictory gross electricity. Inactive mode returns before reading these facts. No new entry-point facts, output channels or engineering acceptance bands are added. Native adversarial evidence and critic ruling are in the goal Round2 record.

## Signed closure diagnostics — reviewed clarification, 2026-09-20

[AGENT; independent critic approved] These six diagnostics measure arithmetic conservation residuals. Their signed definitions are explicit so independent implementations compare the same quantity. They are not additional engineering acceptance bands.

- `salt_heat_residual_MW`: admitted heat minus salt mass flow times heat capacity times the hot-to-return temperature difference.
- `heater_mass_residual_kg_s`: condensate inlet flow plus extraction inlet flow minus mixed outlet flow. The independent reference previously used the opposite sign; that interface error is corrected with compensated summation while preserving the raw prior receipt.
- `heater_energy_residual_MW`: inlet condensate and extraction enthalpy flows minus mixed outlet enthalpy flow.
- `cycle_shaft_residual_MW`: admitted heat plus pump shaft work minus turbine shaft work and condenser heat.
- `cycle_electric_residual_MW`: admitted heat plus cycle pump electricity minus gross electricity and total cycle rejection before cooling-water pumping.
- `water_energy_residual_MW`: cooling-water enthalpy rise minus total rejected heat including cooling-water pump electricity.

[AGENT; independently reviewed numerical policy] The finance regression's six new near-zero diagnostics use relative tolerance1e-9 and absolute tolerance1e-9 in their stated MW or kg/s units. The general released scalar policy already permits absolute1e-6; this scoped finance comparison is stricter. All pre-existing finance channels retain their original relative-only comparison, rate invariance stays exact and engineering predicates stay strict. Production closure guards are unchanged. Independent operation order may leave small signed roundoff; no value is clipped to zero.
