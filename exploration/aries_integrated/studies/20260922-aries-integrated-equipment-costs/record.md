## 1. Study header

Study id: `20260922-aries-integrated-equipment-costs`. Package: `aries_integrated`. Date executed: 2026-09-22. Executor: equipment_study agent, T-006. Mode: execute. Single arm: `arm-declared-sensitivity`, containing canonical, thermal, demand and selected-equipment point families. All 64 exact proposals executed once and completed at commit `e8f9cc1d59a0583fb1b2b2ca4eaa51d87b891c2f`. Exact commands and execution authority are in `results/execution-context.json`. The coordinator owns final snapshot/archive creation and commitment.

## 2. Intake

[OWNER-VERBATIM: supplemental owner message captured in the goal]

> Before ranking equipment or economic alternatives, test sensitivity to the principal thermal assumptions and connect each varied equipment capability to its selected inventory, purchase cost and applicable operating demand. Preserve the source-case failures and label the 423.1 MW case as the assumed integrated baseline.

[OWNER-VERBATIM: retained owner brief]

> For this prompt, I authorize explicitly labeled diagnostic/sensitivity-only sweeps of declared assumptions even when no modeled constraint resists them. Record the missing constraint response and development finding before execution. This does not authorize optimizing an unresisted parameter or calling its endpoint an engineering optimum. Do not invent physical pushback.

[AGENT] One dependency question joins the point families: how do thermal assumptions and explicitly purchased choices alter operating demands, adequacy and cost while preserving independent inventory? The coordinator approved four canonical cases, 50 endpoints across 25 thermal axes, four recuperator/PbLi-temperature interactions, two density-demand perturbations and four purchased-capability probes. Price uncertainty belongs to the next round. Initial wider endpoint suggestions were narrowed to the accepted design where applicable; the declared engineered windows and units are in `axis-plan.json`.

## 3. Objective and result

LCOE objective/result: not applicable; this package produces thermal, inventory and cost inputs for a later financial analysis. The thermal headline is `aries_integrated_plant__plant_ledger__evaluate__net_electric`, MW. The assumed integrated baseline remains 423.106794 MW net with zero unmet heat and all 14 represented checks satisfied. Scientific qualification flags remain unsupported. Across the 64 points, 53 satisfy every represented check and 11 retain violations; no runtime point refused. `results/cases.json` preserves every native output and verdict; `results/analysis.json` joins them to named cases.

Thermal sensitivity was interpreted before equipment or cost comparisons. Cycle-flow changes have the largest net effect over the declared windows, but both endpoints fail a represented check: 1,000 kg/s reports 596.773 MW with 138.638 MW unremoved heat; 1,800 kg/s reports 149.663 MW while exceeding compressor capacity. Those numbers describe constraint-failing operating cases, not usable generation alternatives. Neutron multiplication, recuperator effectiveness and He operating flow also materially change net output. The net-flat U, bulk-limit, partition and PbLi-cp tests all retain zero unmet heat at these selected points; this identifies spare modeled capability near this nominal, not general irrelevance.

All 56 thermal/demand points retain every upfront purchase account and the 4.350208470 billion USD2004 overnight total exactly. Density changes alter fuel throughput/annual cost at fixed purchases. Selected He HX area and pump rating change their purchase accounts and meaningful adequacy outcomes. They demonstrate dependencies, not an economic optimum. `thermal-results.md` and `results/analysis.json` contain the full thermal reading; `report.md` presents the conditional cost boundary after that reading.

## 4. Constraint outcomes

Every executing constraint is listed by exact identity below. Status counts cover all 64 points; the complete case memberships are in `results/analysis.json` under constraint_outcomes. A satisfied scalar screen is not evidence of scientific qualification. The canonical source cases remain constraint-failing.

| constraint_id | source_local_identity | Satisfied | Violated | Violation cases |
| --- | --- | --- | --- | --- |
| aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab | capacity_ok | 63 | 1 | cycle_flow-high |
| aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c | capacity_ok | 63 | 1 | divertor_operating_flow-high |
| aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64 | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0 | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161 | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180 | capacity_ok | 62 | 2 | he_operating_flow-high, he_pump_capacity-low |
| aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395 | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb | capacity_ok | 63 | 1 | pbli_operating_flow-high |
| aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535 | balances_ok | 63 | 1 | literal-Raffray-accounting |
| aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07 | heat_removal_ok | 58 | 6 | nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting, cycle_flow-low, pbli_operating_flow-low, he_hx_area-low |
| aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608 | capacity_ok | 64 | 0 | none |
| aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1 | capacity_ok | 64 | 0 | none |

## 5. Framing

As proposed: all 28 axes are sensitivity, including the two purchased-capability probes and fixed-hardware density demand. As judged: sensitivity remains appropriate for every axis; no framing changed. Finite endpoints show responses or observed failures, not a feasible-region boundary or optimum. Ranking the size of net changes across different engineered windows is not a probability-weighted uncertainty ranking or an intrinsic parameter-importance ranking.

## 6. Per-axis account

#### recuperator_effectiveness — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### recuperator_effectiveness — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.6/0.95 dimensionless give net 310.052702/557.114222 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Purchased recuperator geometry, pressure loss and effectiveness relation absent. Exact case outputs are in `results/cases.json`.

#### he_hot_limit — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_hot_limit — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 679.15/779.15 K give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Bulk limit is not a qualified material temperature. Exact case outputs are in `results/cases.json`.

#### pbli_hot_limit — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### pbli_hot_limit — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 961.15/1061.15 K give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Bulk limit is not a qualified material temperature. Exact case outputs are in `results/cases.json`.

#### divertor_hot_limit — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### divertor_hot_limit — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 923.15/1023.15 K give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Bulk limit is not a qualified material temperature. Exact case outputs are in `results/cases.json`.

#### cycle_flow — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### cycle_flow — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 1000/1800 kg/s give net 596.772776/149.662843 MW and unmet heat 138.638214/0.000000 MW. cycle_flow-low: plant_ledger.heat_removal_ok; cycle_flow-high: compressor_capacity.capacity_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Machine maps and flow-specific purchased capability absent. Exact case outputs are in `results/cases.json`.

#### he_operating_flow — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_operating_flow — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 1630.5/4891.5 kg/s give net 470.813765/293.616445 MW and unmet heat 0.000000/0.000000 MW. he_operating_flow-high: he_pump.capacity_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Cubic fixed-path pump proxy does not qualify gas or MHD hydraulics. Exact case outputs are in `results/cases.json`.

#### pbli_operating_flow — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### pbli_operating_flow — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 13430/40290 kg/s give net 367.082072/423.083044 MW and unmet heat 77.856670/0.000000 MW. pbli_operating_flow-low: plant_ledger.heat_removal_ok; pbli_operating_flow-high: pbli_pump.capacity_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Cubic fixed-path pump proxy does not qualify gas or MHD hydraulics. Exact case outputs are in `results/cases.json`.

#### divertor_operating_flow — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### divertor_operating_flow — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 250/750 kg/s give net 426.189154/414.740389 MW and unmet heat 0.000000/0.000000 MW. divertor_operating_flow-high: divertor_pump.capacity_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Cubic fixed-path pump proxy does not qualify gas or MHD hydraulics. Exact case outputs are in `results/cases.json`.

#### he_u — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_u — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 500/1500 W/(m2 K) give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Fixed-area U uncertainty lacks geometry, pressure-drop and real-fluid qualification. Exact case outputs are in `results/cases.json`.

#### pbli_u — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### pbli_u — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 500/1500 W/(m2 K) give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Fixed-area U uncertainty lacks geometry, pressure-drop and real-fluid qualification. Exact case outputs are in `results/cases.json`.

#### divertor_u — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### divertor_u — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 500/1500 W/(m2 K) give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Fixed-area U uncertainty lacks geometry, pressure-drop and real-fluid qualification. Exact case outputs are in `results/cases.json`.

#### neutron_multiplier — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### neutron_multiplier — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 1/1.25 dimensionless give net 254.022006/518.216988 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: No qualified neutron, radiation or inter-coolant transport response. Exact case outputs are in `results/cases.json`.

#### helium_partition — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### helium_partition — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.3/0.46 dimensionless give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: No qualified neutron, radiation or inter-coolant transport response. Exact case outputs are in `results/cases.json`.

#### radiation_partition — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### radiation_partition — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.1/0.4 dimensionless give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: No qualified neutron, radiation or inter-coolant transport response. Exact case outputs are in `results/cases.json`.

#### intercoolant_exchange — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### intercoolant_exchange — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.02/0.06 dimensionless give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: No qualified neutron, radiation or inter-coolant transport response. Exact case outputs are in `results/cases.json`.

#### pbli_cp — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### pbli_cp — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 170/220 J/(kg K) give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Constant-property sensitivity lacks real-fluid qualification. Exact case outputs are in `results/cases.json`.

#### common_cold_sink — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### common_cold_sink — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 298.15/318.15 K give net 454.164845/392.048743 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Common operating sink is an executor-declared tie; weather and sink equipment response absent. Exact case outputs are in `results/cases.json`.

#### pressure_loss — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### pressure_loss — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.02/0.08 dimensionless give net 436.653670/402.801735 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Pressure loss is not derived from selected geometry. Exact case outputs are in `results/cases.json`.

#### turbine_efficiency — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### turbine_efficiency — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.88/0.95 dimensionless give net 377.289256/440.633478 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Machine-map and purchased quality response absent. Exact case outputs are in `results/cases.json`.

#### common_compressor_efficiency — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### common_compressor_efficiency — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.84/0.92 dimensionless give net 346.944621/464.830419 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Common assumed efficiency is an executor-declared tie; machine-map and purchase-quality response absent. Exact case outputs are in `results/cases.json`.

#### he_pump_efficiency — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_pump_efficiency — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.6/0.9 dimensionless give net 404.932710/429.164822 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Efficiency is assumed at fixed installed flow capacity; qualification and price premium absent. Exact case outputs are in `results/cases.json`.

#### heating_efficiency — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### heating_efficiency — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 0.4/0.7 dimensionless give net 413.106794/434.535366 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Heating efficiency has no purchased equipment or performance-map response. Exact case outputs are in `results/cases.json`.

#### cryo_load — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### cryo_load — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 5/15 MW give net 428.106794/418.106794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Supplied auxiliary demand lacks subsystem physics. Exact case outputs are in `results/cases.json`.

#### control_load — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### control_load — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 2.5/7.5 MW give net 425.606794/420.606794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Supplied auxiliary demand lacks subsystem physics. Exact case outputs are in `results/cases.json`.

#### other_electric_load — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### other_electric_load — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 2.5/7.5 MW give net 425.606794/420.606794 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Supplied auxiliary demand lacks subsystem physics. Exact case outputs are in `results/cases.json`.

#### density_amplitude — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### density_amplitude — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 4.5e+20/5.5e+20 m^-3 give net 140.230696/735.759323 MW and unmet heat 0.000000/0.000000 MW. Neither endpoint violates a represented check. Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Calculated source sensitivity does not qualify confinement. Exact case outputs are in `results/cases.json`.

#### he_hx_area — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_hx_area — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 5000/75000 m2 give net 389.195517/423.106794 MW and unmet heat 47.118607/0.000000 MW. he_hx_area-low: plant_ledger.heat_removal_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Low-area point is a flagged linear-price extrapolation allowed by E2. Exact case outputs are in `results/cases.json`.

#### he_pump_capacity — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### he_pump_capacity — observed response (sensitivity framing)

**Applies:** yes. Low/high inputs 1630.5/4891.5 kg/s give net 423.106794/423.106794 MW and unmet heat 0.000000/0.000000 MW. he_pump_capacity-low: he_pump.capacity_ok Failed-case net is not a usable power alternative. No boundary claim is made. Missing response: Offered scalar flow capacity is not hydraulic qualification. Exact case outputs are in `results/cases.json`.

The four interaction cases combine recuperator effectiveness 0.60/0.95 with PbLi hot limit 961.15/1061.15 K. They all satisfy the represented checks; net remains approximately 310.052702 MW at 0.60 and 557.114222 MW at 0.95, without a meaningful PbLi-limit interaction in this window. This does not establish behavior outside the tested corners.

## 7. Axis groups

Every case carries all 411 generated entry fields. The 28 axes cover 32 declared keys. Only the common sink and common compressor-efficiency groups use ties, declared by the executor as common operating/assumption choices. Different coolant owners and plasma/deposition fractions remain independent. The complete maps in proposed-points.json equal the stored inputs exactly.

| Axis | Entry key | Provenance | Tie authority |
| --- | --- | --- | --- |
| recuperator_effectiveness | aries_integrated_plant__cycle__recuperator_effectiveness | fan_out | Single source owner; native internal fan-out |
| he_hot_limit | aries_integrated_plant__heat_exchangers__he_limit | fan_out | Single source owner; native internal fan-out |
| pbli_hot_limit | aries_integrated_plant__heat_exchangers__pbli_limit | fan_out | Single source owner; native internal fan-out |
| divertor_hot_limit | aries_integrated_plant__heat_exchangers__divertor_limit | fan_out | Single source owner; native internal fan-out |
| cycle_flow | aries_integrated_plant__cycle__selected_flow | fan_out | Single source owner; native internal fan-out |
| he_operating_flow | aries_integrated_plant__heat_exchangers__he_flow | fan_out | Single source owner; native internal fan-out |
| pbli_operating_flow | aries_integrated_plant__heat_exchangers__pbli_flow | fan_out | Single source owner; native internal fan-out |
| divertor_operating_flow | aries_integrated_plant__heat_exchangers__divertor_flow | fan_out | Single source owner; native internal fan-out |
| he_u | aries_integrated_plant__he_hx__assumed_u | fan_out | Single source owner; native internal fan-out |
| pbli_u | aries_integrated_plant__pbli_hx__assumed_u | fan_out | Single source owner; native internal fan-out |
| divertor_u | aries_integrated_plant__divertor_hx__assumed_u | fan_out | Single source owner; native internal fan-out |
| neutron_multiplier | aries_integrated_plant__deposition__neutron_multiplier | fan_out | Single source owner; native internal fan-out |
| helium_partition | aries_integrated_plant__deposition__helium_fraction | fan_out | Single source owner; native internal fan-out |
| radiation_partition | aries_integrated_plant__deposition__radiation_fraction | fan_out | Single source owner; native internal fan-out |
| intercoolant_exchange | aries_integrated_plant__deposition__exchange_fraction | fan_out | Single source owner; native internal fan-out |
| pbli_cp | aries_integrated_plant__heat_exchangers__pbli_cp | fan_out | Single source owner; native internal fan-out |
| common_cold_sink | aries_integrated_plant__cycle__low_temperature | fan_out | Single source owner; native internal fan-out |
| common_cold_sink | aries_integrated_plant__intercooler_1__target_temperature | tie | Executor-declared common assumption |
| common_cold_sink | aries_integrated_plant__intercooler_2__target_temperature | tie | Executor-declared common assumption |
| pressure_loss | aries_integrated_plant__pressure_loss__loss_fraction | fan_out | Single source owner; native internal fan-out |
| turbine_efficiency | aries_integrated_plant__cycle__turbine_efficiency | fan_out | Single source owner; native internal fan-out |
| common_compressor_efficiency | aries_integrated_plant__compressor_1__efficiency | fan_out | Single source owner; native internal fan-out |
| common_compressor_efficiency | aries_integrated_plant__compressor_2__efficiency | tie | Executor-declared common assumption |
| common_compressor_efficiency | aries_integrated_plant__compressor_3__efficiency | tie | Executor-declared common assumption |
| he_pump_efficiency | aries_integrated_plant__he_pump__efficiency | fan_out | Single source owner; native internal fan-out |
| heating_efficiency | aries_integrated_plant__generator_auxiliaries__heating_efficiency | fan_out | Single source owner; native internal fan-out |
| cryo_load | aries_integrated_plant__generator_auxiliaries__cryo | fan_out | Single source owner; native internal fan-out |
| control_load | aries_integrated_plant__generator_auxiliaries__control | fan_out | Single source owner; native internal fan-out |
| other_electric_load | aries_integrated_plant__generator_auxiliaries__other_electric | fan_out | Single source owner; native internal fan-out |
| density_amplitude | aries_cs_plasma_integration__plasma__amplitude | fan_out | Single source owner; native internal fan-out |
| he_hx_area | aries_integrated_plant__he_hx__selected_area | fan_out | Single source owner; native internal fan-out |
| he_pump_capacity | aries_integrated_plant__he_pump__selected_flow_capacity | fan_out | Single source owner; native internal fan-out |

Area and assumed U replace the old free UA keys. Pump flow/efficiency or explicit literal fixed-power mode replace independent nominal pump electrical inputs. Selected tritium kg is the shared stock authority; the old dormant-atoms input retires. No dependent demand chooses installed area, rating or stock. Historical records remain unchanged; prior preparation receipts are preserved separately in goal evidence.

## 8. Indicators and rulings

All 28 groups report constraints_reachable in `indicators.json`; none reports no_constraint_response. This is a possible module path, not measured physical pushback. The top-level indicator warning list is empty; the native suffix scan separately emits nine advisory sibling warnings, disposed in §9. The owner’s quoted sensitivity-only authorization covers unresisted assumptions; known missing physical responses were recorded before execution as findings #1–#3 and in axis-plan.json.

Not derivable from indicators: monotonicity of a channel in an axis; identity of the same physical quantity across different names; intra-module operand dependency. Unresisted is the executor’s judgment, not a tool output. Fixed-budget recuperator quality, qualified materials/transport, machine maps, hydraulic/MHD detail, auxiliary subsystem physics and demand-derived replacement life remain absent despite reachable aggregate predicates.

## 9. Preflight results

Native integration CANDIDATE passed all ten gates before release. Its six mechanical study preflight gates are retained in `results/integration/preflight_results.json`; identity and baseline documents are `results/package_identity.json` and `results/baseline_result.json`. The baseline gate pins two unique local predicates; the repeated capacity local name is certified separately through all exact stored IDs and all-point numerical rederivation.

| Gate | Outcome | Detail |
| --- | --- | --- |
| declared_keys | pass | 32 declared keys across 28 groups, all package inputs |
| sibling_scan | pass | warnings: 9 |
| identity | pass | kind sealed, digest 01f8f89c42a98621ff4c6868156d9b7938b7c80102f1c8321b35504ffcc7a021 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | aries_integrated_plant__plant_ledger__evaluate__net_electric reproduces at relative deviation 0.000e+00; 2/2 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The nine suffix advisories do not identify missing ties. Plasma helium fraction and deposited-heat helium fraction represent different physics. Compressor efficiency is not the same assumption as either other primary-pump efficiency. The three pumps and exchangers have independently selected efficiency, area and flow-capacity owners. The He-only hardware probes hold the other branches fixed deliberately. The warnings are preserved, not suppressed or converted into invented equalities.

## 10. Execution route and why

Route: study-local direct API using the delivered strict package loader, PreparedEvaluator, PreparedListStrategy, StudyRunner and SQLite store lifecycle. Complete coordinated points and explicit ties motivated the prepared-list route. The candidate reproduced the pinned baseline and the single stored invocation completed all 64 proposals. Glue ledger: none; no runtime physical adapter or caller-side plant arithmetic supplied an output. The record-local analysis reads native outputs and computes only comparisons/counts. Exact execution, all-point verification and analysis commands are in results/execution-context.json.

## 11. Study definition and window provenance

Windows are engineered from the accepted thermal/equipment design, not sourced applicability envelopes. The corrected package’s independent oracle evaluated all 64 proposed maps with no domain refusal before native execution; oracle-window-scan.json retains the scan. He HX area endpoints bracket heat removal and He pump capacity endpoints bracket a scalar flow margin; these were used to retain useful diagnostic points, not to claim a boundary. The low-area price is explicitly extrapolated. After a citation-only executable reseal, exact canonical inputs/outputs were preserved and preparation was repeated under the final identity; prior receipts remain preserved outside this unfinished record.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint across every stored case; no cross-arm correlation is needed. The prior frozen WI-089 study and earlier preparation checkpoints are historical evidence, not additional stored arms. The source-conditioned configurations retain their own full maps and failed thermal outcomes. The new selected 10 kg stock intentionally changes required-breeding and fuel-cost diagnostics without changing inherited thermal results; breeding support stays unsupported.

## 13. Verification

PASS: all 64 stored rows were independently checked, covering all seven observed verdict-combination strata. Each row compares 278 numeric channels and rederives all 14 exact predicate statuses: 17,792 scalar and 896 predicate comparisons, zero mismatches. The standard relative tolerance is 1e-9, with only the inherited residual-magnitude channel allowed 1e-7 MW absolute error. No monetary tolerance was relaxed. The reported large worst relative deviation is a near-zero residual comparison covered by that dimensional tolerance, not a failed physical result. `results/verification_summary.json` retains sampling, channel identities, predicates and the actual outcome.

The oracle independently integrates plasma profiles, solves thermal closure with Brent’s method, calculates selected-area/pump/stock/account/schedule arithmetic, and reconstructs source comparisons. It imports no generated physical arithmetic. Numerical agreement checks implementation and wiring under shared equation authority; it does not independently validate the source tables or qualify the scientific approximations. Copied supplied amounts/year/support flags are transport checks, not independent science. Broad published outputs outside the 278-channel catalog remain unverified numerically. The checker-local variable-shadowing failure from preparation is retained, followed by passing correction; it changed no package or stored result.

## 14. Review outcomes

The coordinator released T-006 only after accepted source/design/implementation review and native CANDIDATE at execution commit e8f9cc1d. The coordinator freeze copied source-review.md, design-review.md and implementation-review.md under results/sources/ with their original paths and hashes. These reviews cover model semantics and preservation; the executor does not label its own numerical interpretation an independent review. Coordinator checks cover the exact stored/proposed maps, all-point verifier receipt, retained adverse outcomes and thermal-first reporting. Independent interpretation/disposition review follows the committed record and will be recorded outside its frozen evidence. No new source interpretation or model equation was introduced during execution.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| 20260922-aries-integrated-equipment-costs#1 | model | Recuperator effectiveness and material/transport/machine assumptions lack qualified geometry or scientific response despite graph reachability. | Sensitivity only under owner authorization; no endpoint optimum or qualified-performance claim. | work/active/WI-090_aries-integrated-equipment-and-costs/design.md |
| 20260922-aries-integrated-equipment-costs#2 | model | Primary flow uses a cubic pump proxy; hydraulic/MHD qualification, machine maps and demand-derived replacement life remain absent. | Preserve independent installed ratings and selected replacement schedules; carry proxy limits. | work/active/WI-090_aries-integrated-equipment-and-costs/design.md |
| 20260922-aries-integrated-equipment-costs#3 | model | Low He HX area is0.1 times reference, outside the0.5–1.5 local linear purchase comparison range although E2 permits the capability diagnostic. | Retain extrapolated flag and adverse heat-removal outcome; no qualified low-price alternative claim. | work/active/WI-090_aries-integrated-equipment-and-costs/design.md |
| 20260922-aries-integrated-equipment-costs#4 | model | Cycle flow produces the largest net change over declared thermal endpoints; low flow fails heat removal and high flow fails compressor capacity. | Report constraint-failing net separately; do not select an operating optimum from this finite sweep. | record.md §6; results/analysis.json |
| 20260922-aries-integrated-equipment-costs#5 | model | Nominal U/hot-limit/partition/PbLi-cp sweeps and the four tested recuperator/PbLi-limit corners retain enough modeled heat-transfer capability. | Retain local nonresponse; do not generalize beyond the engineered windows or confuse it with missing graph connections. | thermal-results.md |
| 20260922-aries-integrated-equipment-costs#6 | model | All56 thermal/demand cases preserve every upfront purchase account and overnight total; density changes fuel throughput and annual costs. | Accept bounded MR-7 evidence; preserve declared operating-versus-purchase roles. | results/analysis.json |
| 20260922-aries-integrated-equipment-costs#7 | model | Selected He area changes cost/capability, and selected pump capacity changes purchase cost/margin at fixed operating demand. | Accept explicit inadequate/adequate purchase probes; no hidden sizing or economic optimum. | report.md; results/cases.json |
| 20260922-aries-integrated-equipment-costs#8 | model | All three source-conditioned canonical cases retain heat-removal failures; literal Raffray also fails the energy-balance screen. | Carry adverse source outcomes forward unchanged; no usable published-plant power claim. | results/cases.json |
| 20260922-aries-integrated-equipment-costs#9 | model | The no-recovery-credit baseline prices104.667707kg/y external T and makes assumed tritium supply dominate annual cost. | Pursue the separately authorized cost-uncertainty/supply scenarios next round; this is not a breeding prediction. | work/orchestration/goals/aries-integrated-equipment-costs/goal.md |
| 20260922-aries-integrated-equipment-costs#10 | model | Native source-account, known-mass, LiPb-rate and replacement comparisons retain nonzero mismatches and VF mass unavailability. | Preserve disjoint source/provisional boundaries; do not normalize mismatches or infer missing mass as zero. | report.md; results/cases.json |

## 16. Snapshot

The coordinator captured snapshot.json and sealed-package.tar.gz after execution and verification. Snapshot SHA256 is `894a81ddc6142bc983c95a783a3ff32783ac6b9f4b58a5d1a727269a3b8f4fcc`; it resolves the package, complete manifest, tools, store compatibility tuple and138 retained artifact digests. One arm contains the declared point families. This record freezes when committed; later corrections are addenda.

## 17. What this record does not contain

No full price-uncertainty range, assumed-recovery100kg/year scenario, LCOE, financial cashflow treatment, global optimum or scientific qualification is present. No negative-export study point occurred, so its tariff branch is not exercised by this study. The record provides a conditional operating/equipment dependency result and a declared baseline cost boundary. Independent interpretation/disposition acceptance is a subsequent goal review, outside this executor record.
