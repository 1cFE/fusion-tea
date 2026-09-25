# Record: 20260925-aries-reference-heat-electricity-reconciliation

## 1. Study header

- **Study id:** `20260925-aries-reference-heat-electricity-reconciliation`
- **Package:** `aries_integrated`
- **Date executed:** `2026-09-25`
- **Executor:** Claude coordinator of goal `aries-reference-heat-electricity-reconciliation` (round 1, T-004); executor reporting, not an independent administrator reading.
- **Mode:** execute
- **Arms:** single arm, `arm-diagnostic`

## 2. Intake

[OWNER-VERBATIM] From `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-brief.md`:

> Use controlled cases to quantify causes. Change one justified assumption or model feature at a time where meaningful, then run the combined corrected case. Attribution in a nonlinear model can depend on change order: identify that order, measure consequential interactions and ensure the final ledger accounts for the combined difference. Do not simply add unrelated sensitivity effects.

> I authorize explicitly labeled assumption-sensitivity studies without modeled constraint response. Record that absence before execution. This does not authorize optimizing those assumptions or treating an endpoint as an engineering optimum.

[AGENT] Executor additions: this study runs on the unchanged entry package (no model change). It supplies the published Lyon fusion power (2436 MW, producer mode 0) and isolates, one at a time from the original failing case and in combination, the inherited inputs that the reference-case contract identifies as unsupported: recuperator effectiveness, cycle flow, divertor primary flow, deposition partition, auxiliary-load accounting and, as a labelled diagnostic only, tenfold exchanger conductance. Reverse one-at-a-time cases from the combined case and a cycle-flow bracket measure interactions. The four canonical controls are copied verbatim. Nothing is tuned to the published output; the study's purpose is attribution, not agreement.

## 3. Objective and result

- **Objective channels:** `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `__gross_electric` (MW); `aries_integrated_plant__heat_exchangers__evaluate__unmet_heat`, `__he_unmet`, `__pbli_unmet`, `__divertor_unmet`, `__accepted_heat`, `__turbine_temperature`; `aries_integrated_plant__plant_ledger__evaluate__thermal_efficiency`. The package's LCOE channel `aries_integrated_plant__lifecycle_price__evaluate__lcoe` remains the manifest headline for the baseline gate but is not this study's objective.
- **Result:** the original source-conditioned case (`nominal-source-assumed`) gives net 796.005 MW, gross 1028.659 MW and 158.726 MW unremoved heat, all of it in the PbLi stage, against the reference 1000 / 1253 / 0. Every input-level correction combined on this package (`combined-c3-partition`: source recuperation 0.95, cycle flow 1600 kg/s, divertor flow 283 kg/s, Lyon auxiliary itemisation, source-informed partition) gives net 842.732 MW, gross 1094.742 MW, thermal efficiency 0.3945 and still 151.002 MW unremoved in the PbLi stage. The only source-conditioned cases that remove all heat and pass every evaluated check run at 1600 kg/s with the inherited 0.8 recuperation (`oat-cycle-flow-1600` net 773.518 MW, gross 1006.172; `c2-minus-recuperator` and `c3-minus-recuperator` net 759.886 MW, gross 1011.896). At the source's 0.95 recuperation, full heat removal appears only at 1800 kg/s (`c2-cycle-flow-1800`, `c3-cycle-flow-1800`: net 803.563 MW), where the assumed 1600 MW compressor rating is exceeded.

Over the studied space the reference gross (1253 MW) is never approached: the largest gross is 1128.379 MW (`c2-cycle-flow-1700`, 16.283 MW unremoved, compressor rating exceeded). Net responses are strongly interacting: the forward one-at-a-time net deltas from the original sum to −45.065 MW while the combined C3 delta is +46.727 MW, because raising recuperation only helps when cycle flow is high enough to accept the heat (`results/attribution.json`, `results/attribution.md`).

## 4. Constraint outcomes

Every generated constraint identity appears below; there are no indeterminate statuses. "Satisfied" means the evaluated scalar check passes, not scientific feasibility.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied / violated | Violated in the six cases at cycle flow ≥ 1700 kg/s (`oat-cycle-flow-1700`, `c2-cycle-flow-1700/1800/2000`, `c3-cycle-flow-1700/1800`): compressor shaft demand scales with cycle flow past the assumed 1600 MW offered rating (A6). |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied / violated | Violated only in `literal-Raffray-accounting` (retained −182.03 MW source-energy mismatch). |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated in 19 of 27 cases: every source-conditioned case except those at cycle flow 1600 kg/s with recuperation 0.8 and those at ≥ 1800 kg/s. |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | All 27. |

Four cases satisfy every evaluated check: `nominal-calculated`, `oat-cycle-flow-1600`, `c2-minus-recuperator`, `c3-minus-recuperator`. Exact predicates and operand provenance are in `results/constraint_catalog.json`.

## 5. Framing

**As proposed at intake.** [AGENT] Every axis is sensitivity-framed: the study measures response to declared input changes; it searches for no boundary and no optimum.

| Axis | Framing proposed | Why |
|---|---|---|
| `recuperator_effectiveness` | sensitivity | assumed input; No purchased recuperator geometry, area or pressure-loss relation resists the effectiveness. |
| `cycle_flow` | sensitivity | operating input; No machine map, purchased flow capability or cycle pressure-loss law responds to cycle flow; compressor rating screen is the only reachable check. |
| `divertor_primary_flow` | sensitivity | operating input; Divertor hydraulics and MHD are unqualified; the cubic pump proxy is bypassed by the fixed-power mode in every case that changes this flow. |
| `he_u` | sensitivity | assumed input; U has no geometry or pressure-drop qualification. |
| `pbli_u` | sensitivity | assumed input; Same as he_u. |
| `divertor_u` | sensitivity | assumed input; Same as he_u. |
| `deposited_auxiliary_heat` | sensitivity | accounting input; No plasma sustainment model resists this supplied heat. |
| `cryo_load` | sensitivity | accounting input; No cryoplant demand model. |
| `control_load` | sensitivity | accounting input; No subsystem demand model. |
| `other_load` | sensitivity | accounting input; No subsystem demand model. |
| `fuel_base_load` | sensitivity | accounting input; No fuel-processing demand model. |
| `fuel_coefficient` | sensitivity | accounting input; Same as fuel_base_load. |
| `he_pump_mode` | sensitivity | accounting input; Mode switch only. |
| `he_pump_fixed_power` | sensitivity | accounting input; No hydraulic law. |
| `divertor_pump_mode` | sensitivity | accounting input; Mode switch only. |
| `divertor_pump_fixed_power` | sensitivity | accounting input; No hydraulic law. |
| `radiation_fraction` | sensitivity | assumed input; No radiation, scrape-off-layer or neutron transport model resists the partition. |
| `exchange_fraction` | sensitivity | assumed input; No insert-conductance model resists the exchange. |

**As judged after the run.** [AGENT]

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `recuperator_effectiveness` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `cycle_flow` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `divertor_primary_flow` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `he_u` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `pbli_u` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `divertor_u` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `deposited_auxiliary_heat` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `cryo_load` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `control_load` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `other_load` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `fuel_base_load` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `fuel_coefficient` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `he_pump_mode` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `he_pump_fixed_power` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `divertor_pump_mode` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `divertor_pump_fixed_power` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `radiation_fraction` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |
| `exchange_fraction` | sensitivity | no | Monotone or single-setting response observed; heat-removal and compressor-rating violations are located in § 4 and § 6, and no boundary or optimum is claimed. |

## 6. Per-axis account

#### `recuperator_effectiveness` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `recuperator_effectiveness` — observed response (sensitivity framing)

**Applies:** yes.

From the original case, 0.8 → 0.95 raises net by 11.011 MW and thermal efficiency from 0.3728 to 0.4127, but raises the heater inlet from 556.28 K to 593.65 K and unremoved heat from 158.726 to 398.909 MW (helium stage 169.870, PbLi 229.039). From C3, dropping back to 0.8 removes all unmet heat and costs 82.846 MW net. Heat-removal violations occur at 0.95 for every cycle flow below 1800 kg/s. No boundary claim is made.

#### `cycle_flow` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `cycle_flow` — observed response (sensitivity framing)

**Applies:** yes.

From the original case at 0.8 recuperation, 1500 kg/s leaves 32.840 MW unremoved and gains 22.239 MW net; 1600 kg/s removes all heat (turbine inlet 877.34 K) at -22.487 MW net; 1700 kg/s costs 90.848 MW and exceeds the compressor rating. At C2 (0.95 recuperation) unremoved heat falls from 265.969 MW (1500) through 132.350 (1600) and 16.283 (1700) to 0 at 1800 kg/s, while net peaks near 1700 kg/s (876.369 MW) and falls to 628.683 MW at 2000 kg/s. The compressor-rating violation is located at ≥ 1700 kg/s in every family. No boundary claim is made.

#### `divertor_primary_flow` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `divertor_primary_flow` — observed response (sensitivity framing)

**Applies:** yes.

500 → 283 kg/s with pump power held at 10 MW changes net by -1.605 MW from the original and by -2.288 MW at C2; the divertor stage becomes slightly capacity-rate limited (12.479 MW divertor unmet from the original, 12.747 MW at C2). A second-order effect. No boundary claim is made.

#### `he_u` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_u` — observed response (sensitivity framing)

**Applies:** yes.

Tenfold conductance on all three exchangers changes net by only 8.552 MW from the original and 5.495 MW from C3, and leaves 144.887 MW unremoved at C3: conductance is not the limit; the temperature bounds and the PbLi capacity rate are. Labelled diagnostic, not a reference reproduction. No boundary claim is made.

#### `pbli_u` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_u` — observed response (sensitivity framing)

**Applies:** yes.

Swept only together with `he_u` in the tenfold-conductance diagnostic; see `he_u`. No boundary claim is made.

#### `divertor_u` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `divertor_u` — observed response (sensitivity framing)

**Applies:** yes.

Swept only together with `he_u` in the tenfold-conductance diagnostic; see `he_u`. No boundary claim is made.

#### `deposited_auxiliary_heat` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `deposited_auxiliary_heat` — observed response (sensitivity framing)

**Applies:** yes.

Part of the Lyon accounting alignment (`oat-lyon-auxiliaries`): the ten accounting axes together change net by -18.334 MW from the original (auxiliary electricity 232.653 → 252.010 MW, matching Lyon's itemised 252 MW) and gross by 1.023 MW (through 178 MW of returned pumping heat instead of 150). Removing the 20 MW deposited heating lowers divertor deposition; the net effect on unmet heat is 6.532 MW. No boundary claim is made.

#### `cryo_load` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `cryo_load` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `control_load` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `control_load` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `other_load` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `other_load` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `fuel_base_load` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `fuel_base_load` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `fuel_coefficient` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `fuel_coefficient` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `he_pump_mode` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_pump_mode` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `he_pump_fixed_power` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_pump_fixed_power` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `divertor_pump_mode` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `divertor_pump_mode` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `divertor_pump_fixed_power` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `divertor_pump_fixed_power` — observed response (sensitivity framing)

**Applies:** yes.

Swept only as part of the Lyon accounting alignment (or, for the divertor pump keys, to hold pump power fixed when divertor flow changes); see `deposited_auxiliary_heat` and `divertor_primary_flow`. No boundary claim is made.

#### `radiation_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `radiation_fraction` — observed response (sensitivity framing)

**Applies:** yes.

With `exchange_fraction`, the source-informed partition (0.25 → 0.657; 0.04 → 0.0469) moves ≈ 198 MW from the divertor circuit to the blanket circuits: net changes by -13.650 MW from the original and by -16.762 MW from C2; unremoved PbLi heat rises to 177.693 MW and 151.002 MW respectively. The correction is source-supported and adverse, as the contract predicted. No boundary claim is made.

#### `exchange_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `exchange_fraction` — observed response (sensitivity framing)

**Applies:** yes.

Swept only together with `radiation_fraction`; see `radiation_fraction`. No boundary claim is made.

## 7. Axis groups

Every axis is one qualified entry key (`fan_out`); no ties are declared. The four preflight sibling warnings name the PbLi pump mode/fixed-power keys, which are deliberately left at their canonical values (PbLi pumping is 0.01 MW in both sources).

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `recuperator_effectiveness` | `aries_integrated_plant__cycle__recuperator_effectiveness` | fan_out | Raffray Table III prints 0. |
| `cycle_flow` | `aries_integrated_plant__cycle__selected_flow` | fan_out | Inherited 1400 kg/s is agent assumption A3; 1600 is derived from Lyon 2916 MW over Raffray Fig. |
| `divertor_primary_flow` | `aries_integrated_plant__heat_exchangers__divertor_flow` | fan_out | Raffray Table V prints 283 kg/s; inherited 500 kg/s is agent assumption A4. |
| `he_u` | `aries_integrated_plant__he_hx__assumed_u` | fan_out | Diagnostic tenfold conductance (UA 50 to 500 MW/K) to separate conductance limits from temperature and capacity-rate limits; labelled resized diagnostic, never reference reproduction. |
| `pbli_u` | `aries_integrated_plant__pbli_hx__assumed_u` | fan_out | Same diagnostic as he_u. |
| `divertor_u` | `aries_integrated_plant__divertor_hx__assumed_u` | fan_out | Same diagnostic as he_u. |
| `deposited_auxiliary_heat` | `aries_integrated_plant__deposition__auxiliary_heat` | fan_out | Lyon reference is an ignited plasma (P_input = 0, p707); inherited 20 MW is assumption A1. |
| `cryo_load` | `aries_integrated_plant__generator_auxiliaries__cryo` | fan_out | Lyon p717 itemises 5 MW cryogenic; inherited 10 MW is assumption A5. |
| `control_load` | `aries_integrated_plant__generator_auxiliaries__control` | fan_out | Lyon itemises no control load; folded into the 50 MW balance of plant. |
| `other_load` | `aries_integrated_plant__generator_auxiliaries__other_electric` | fan_out | Lyon p717: 50 MW balance of plant. |
| `fuel_base_load` | `aries_integrated_plant__generator_auxiliaries__fuel_base` | fan_out | Lyon itemises no fuel-processing load; folded into balance of plant. |
| `fuel_coefficient` | `aries_integrated_plant__generator_auxiliaries__fuel_coefficient` | fan_out | Same as fuel_base_load. |
| `he_pump_mode` | `aries_integrated_plant__he_pump__pump_mode` | fan_out | Mode 1 supplies a fixed pump power instead of the cubic proxy; used to hold or set pump power explicitly. |
| `he_pump_fixed_power` | `aries_integrated_plant__he_pump__fixed_power` | fan_out | Lyon p708: 170 MW blanket helium pumping; Raffray Table II: 156 MW. |
| `divertor_pump_mode` | `aries_integrated_plant__divertor_pump__pump_mode` | fan_out | Mode 1 supplies a fixed pump power instead of the cubic proxy. |
| `divertor_pump_fixed_power` | `aries_integrated_plant__divertor_pump__fixed_power` | fan_out | Lyon p708 and Raffray Table V: 27 MW divertor helium pumping; inherited 10 MW is assumption A2. |
| `radiation_fraction` | `aries_integrated_plant__deposition__radiation_fraction` | fan_out | Model meaning: fraction of charged power deposited in the blanket circuits, remainder to the divertor. |
| `exchange_fraction` | `aries_integrated_plant__deposition__exchange_fraction` | fan_out | Raffray Table II: 111 MW conducted from PbLi to He at 2365 MW fusion, 0. |

**Declared designs** (`proposed-points.json`; base is a canonical native map or an earlier design; values are axis settings):

| Case | Base | Axis values | Classification |
|---|---|---|---|
| `nominal-calculated` | manifest-baseline | — | assumed integrated baseline, calculated plasma (control) |
| `nominal-source-assumed` | nominal-source-assumed | — | original failing source-conditioned case (control) |
| `literal-Lyon-source-input` | literal-Lyon-source-input | — | canonical literal source-input variant (control) |
| `literal-Raffray-accounting` | literal-Raffray-accounting | — | canonical literal Raffray accounting (control) |
| `oat-recuperator-0.95` | nominal-source-assumed | {"recuperator_effectiveness": 0.95} | one change: source recuperator effectiveness |
| `oat-cycle-flow-1500` | nominal-source-assumed | {"cycle_flow": 1500.0} | one change: cycle flow bracket |
| `oat-cycle-flow-1600` | nominal-source-assumed | {"cycle_flow": 1600.0} | one change: source-informed cycle flow |
| `oat-cycle-flow-1700` | nominal-source-assumed | {"cycle_flow": 1700.0} | one change: cycle flow bracket |
| `oat-divertor-flow-283` | nominal-source-assumed | {"divertor_primary_flow": 283.0, "divertor_pump_mode": 1.0, "divertor_pump_fixed_power": 10.0} | one thermal change: source divertor flow with inherited 10 MW pump power held fixed |
| `oat-ua-x10` | nominal-source-assumed | {"he_u": 10000.0, "pbli_u": 10000.0, "divertor_u": 10000.0} | diagnostic resized conductance; not a reference reproduction |
| `oat-lyon-auxiliaries` | nominal-source-assumed | {"deposited_auxiliary_heat": 0.0, "cryo_load": 5.0, "control_load": 0.0, "other_load": 50.0, "fuel_base_load": 0.0, "fuel_coefficient": 0.0, "he_pump_mode": 1.0, "he_pump_fixed_power": 170.0, "divertor_pump_mode": 1.0, "divertor_pump_fixed_power": 27.0} | accounting alignment to Lyon auxiliary definitions |
| `combined-source-thermal` | nominal-source-assumed | {"recuperator_effectiveness": 0.95, "cycle_flow": 1600.0, "divertor_primary_flow": 283.0, "divertor_pump_mode": 1.0, "divertor_pump_fixed_power": 10.0} | combined source-informed thermal inputs |
| `combined-source-thermal-lyon-aux` | combined-source-thermal | {"deposited_auxiliary_heat": 0.0, "cryo_load": 5.0, "control_load": 0.0, "other_load": 50.0, "fuel_base_load": 0.0, "fuel_coefficient": 0.0, "he_pump_mode": 1.0, "he_pump_fixed_power": 170.0, "divertor_pump_mode": 1.0, "divertor_pump_fixed_power": 27.0} | combined thermal inputs plus Lyon auxiliary accounting (C2) |
| `combined-plus-ua-x10` | combined-source-thermal-lyon-aux | {"he_u": 10000.0, "pbli_u": 10000.0, "divertor_u": 10000.0} | C2 plus diagnostic conductance |
| `c2-minus-recuperator` | combined-source-thermal-lyon-aux | {"recuperator_effectiveness": 0.8} | reverse one-at-a-time from C2 |
| `c2-minus-cycle-flow` | combined-source-thermal-lyon-aux | {"cycle_flow": 1400.0} | reverse one-at-a-time from C2 |
| `c2-minus-divertor-flow` | combined-source-thermal-lyon-aux | {"divertor_primary_flow": 500.0} | reverse one-at-a-time from C2 |
| `c2-cycle-flow-1500` | combined-source-thermal-lyon-aux | {"cycle_flow": 1500.0} | cycle-flow bracket at C2 |
| `c2-cycle-flow-1700` | combined-source-thermal-lyon-aux | {"cycle_flow": 1700.0} | cycle-flow bracket at C2 |
| `c2-cycle-flow-1800` | combined-source-thermal-lyon-aux | {"cycle_flow": 1800.0} | cycle-flow bracket at C2 |
| `c2-cycle-flow-2000` | combined-source-thermal-lyon-aux | {"cycle_flow": 2000.0} | cycle-flow bracket at C2 |
| `oat-source-partition` | nominal-source-assumed | {"radiation_fraction": 0.657, "exchange_fraction": 0.0469} | one change: source-informed deposition partition |
| `combined-c3-partition` | combined-source-thermal-lyon-aux | {"radiation_fraction": 0.657, "exchange_fraction": 0.0469} | C2 plus source-informed partition (C3) |
| `c3-plus-ua-x10` | combined-c3-partition | {"he_u": 10000.0, "pbli_u": 10000.0, "divertor_u": 10000.0} | C3 plus diagnostic conductance |
| `c3-cycle-flow-1700` | combined-c3-partition | {"cycle_flow": 1700.0} | cycle-flow bracket at C3 |
| `c3-cycle-flow-1800` | combined-c3-partition | {"cycle_flow": 1800.0} | cycle-flow bracket at C3 |
| `c3-minus-recuperator` | combined-c3-partition | {"recuperator_effectiveness": 0.8} | reverse one-at-a-time from C3 |

## 8. Indicators and rulings

`indicators.json` reports every declared axis as `constraints_reachable` (at least 5 of 14 executing constraints and at least 110 of 364 objective channels on a possible path). No axis is `no_constraint_response`, so no user ruling is required before execution. The owner's authorisation of explicitly labelled assumption-sensitivity studies without modelled constraint response (owner brief § Studies and engineering discipline) is nevertheless recorded here because reachability is a possible path, never a claim that the axis is physically resisted.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `recuperator_effectiveness` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `cycle_flow` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `divertor_primary_flow` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `he_u` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `pbli_u` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `divertor_u` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `deposited_auxiliary_heat` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `cryo_load` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `control_load` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `other_load` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `fuel_base_load` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `fuel_coefficient` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `he_pump_mode` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `he_pump_fixed_power` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `divertor_pump_mode` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; engineered window |
| `divertor_pump_fixed_power` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `radiation_fraction` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |
| `exchange_fraction` | constraints_reachable | not required: constraints reachable; owner-authorised diagnostic sensitivity applies to unresisted meaning | swept in the declared designs; sourced window |

**Not derivable, disclosed:** monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds.

**Model-development findings.** Recorded for every axis because the reachable constraints are scalar screens and the ledger/heat-removal predicates, not physical resistance to the input itself.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `recuperator_effectiveness` | No purchased recuperator geometry, area or pressure-loss relation resists the effectiveness. | `20260925-aries-reference-heat-electricity-reconciliation#1` |
| `cycle_flow` | No machine map, purchased flow capability or cycle pressure-loss law responds to cycle flow; compressor rating screen is the only reachable check. | `20260925-aries-reference-heat-electricity-reconciliation#2` |
| `divertor_primary_flow` | Divertor hydraulics and MHD are unqualified; the cubic pump proxy is bypassed by the fixed-power mode in every case that changes this flow. | `20260925-aries-reference-heat-electricity-reconciliation#3` |
| `he_u` | U has no geometry or pressure-drop qualification. | `20260925-aries-reference-heat-electricity-reconciliation#4` |
| `pbli_u` | Same as he_u. | `20260925-aries-reference-heat-electricity-reconciliation#4` |
| `divertor_u` | Same as he_u. | `20260925-aries-reference-heat-electricity-reconciliation#4` |
| `deposited_auxiliary_heat` | No plasma sustainment model resists this supplied heat. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `cryo_load` | No cryoplant demand model. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `control_load` | No subsystem demand model. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `other_load` | No subsystem demand model. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `fuel_base_load` | No fuel-processing demand model. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `fuel_coefficient` | Same as fuel_base_load. | `20260925-aries-reference-heat-electricity-reconciliation#5` |
| `he_pump_mode` | Mode switch only. | `20260925-aries-reference-heat-electricity-reconciliation#3` |
| `he_pump_fixed_power` | No hydraulic law. | `20260925-aries-reference-heat-electricity-reconciliation#3` |
| `divertor_pump_mode` | Mode switch only. | `20260925-aries-reference-heat-electricity-reconciliation#3` |
| `divertor_pump_fixed_power` | No hydraulic law. | `20260925-aries-reference-heat-electricity-reconciliation#3` |
| `radiation_fraction` | No radiation, scrape-off-layer or neutron transport model resists the partition. | `20260925-aries-reference-heat-electricity-reconciliation#6` |
| `exchange_fraction` | No insert-conductance model resists the exchange. | `20260925-aries-reference-heat-electricity-reconciliation#6` |

## 9. Preflight results

From `preparation/preflight_results.json` (run after the final axis declaration; the native baseline point in `preparation/baseline_result.json` was executed once, before the axis set was extended, and was not rerun because the manifest and package are unchanged).

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 18 declared keys across 18 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass, warnings 4 | `pbli_pump__pump_mode` and `pbli_pump__fixed_power` are undeclared siblings of the declared He/divertor pump keys; deliberate |
| Baseline gate against the pinned headline | pass | `aries_integrated_plant__lifecycle_price__evaluate__lcoe` reproduces at relative deviation 0; 2/2 pinned verdicts match (`preparation/baseline_result.json`) |
| Manifest / package fingerprint match | pass | both recorded fingerprints match the package on disk (`preparation/package_identity.json`) |
| Package cleanliness | pass | package tree byte-untouched |

## 10. Execution route and why

- **Route:** study-local direct-API (stock `StudyRunner` with `PreparedListStrategy` over complete declared input maps, through `reconciliation_support.py` and the retained predecessor executor `20260922-aries-integrated-lcoe/execute_study.py`).
- **Why this route:** the declared cases are named full maps composed on canonical bases and on each other, not a Cartesian grid; the strict loader, fingerprints, store lease and full-map exporter are reused unchanged.

**Glue disclosure.** glue ledger: none. No adapter on this route, so nothing is harness-supplied.

## 11. Study definition and window provenance

The candidate range was scanned with the package-owned independent oracle (`oracle-window-scan.json`, 27 of 27 evaluated, none refused). Windows are declared per axis in `axis-plan.json`: sourced values (0.95 recuperation; 283 kg/s divertor flow; Lyon auxiliary itemisation; partition 0.657 / 0.0469) and engineered values (cycle flow 1500–2000 kg/s around the derived 1595; tenfold conductance as a labelled diagnostic). Engineered windows cost the claim of a boundary; none is made.

## 12. Cross-fingerprint correlation and what it means

single fingerprint — no cross-arm correlation needed.

## 13. Verification

All 27 stored cases were verified against the package-owned independent oracle (`scripts/study/verify.py`, sample size 27, stratified over the five observed verdict combinations): 364 numeric channels per case at relative 1e-9 or the two declared absolute tolerances, and all 14 predicates re-derived exactly. Outcome `pass`. The worst relative deviation (2.73e4) is on `plant_ledger__evaluate__residual_magnitude` at a value of 6.2e-9 MW in case c0017, inside the reviewed 1e-7 MW absolute allowance for the near-zero ledger residual; no engineering channel relaxed. Each case publishes 546 numeric outputs; 182 are not in the oracle catalog and are not independently verified. The oracle shares the reviewed equations' authority: it verifies numerical translation of the assumptions, not their scientific validity, and the three canonical controls' inputs are identical by construction on both sides.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Source readings and source-informed inputs (fresh non-author reviewer, `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/source-check-review.md` r1–r3) | r1 FINDINGS none blocking; r2 FINDINGS one correct-before-use; r3 PASS | Contract and budget corrected before execution; the study inputs 0.95, 283 kg/s, partition 0.657/0.0469 and Lyon itemisation confirmed against page images; 1600 kg/s graded as a cross-source derived convention and bracketed. |
| Pre-execution framing and no-response rulings | coordinator check | Every axis `constraints_reachable`; owner authorisation of labelled assumption sensitivity recorded in § 8; no separate critic commissioned because no new equation, interface or shared definition is introduced. |
| Mechanical gates and all-point verification | tool outcomes | Preflight six gates pass (§ 9); verification pass (§ 13). |
| Study reading and dispositions | pending goal round review | The executor reading in `synthesis.md` and the goal trail's dispositions are submitted to the round's fresh review; this record makes no claim beyond its results. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260925-aries-reference-heat-electricity-reconciliation#1` | model | No purchased recuperator geometry, area or pressure-loss relation resists recuperator effectiveness; 0.8 and 0.95 are supplied constants. | declared seam; sensitivity-only under owner authorisation | documented seam (WI-089 design A3) |
| `20260925-aries-reference-heat-electricity-reconciliation#2` | model | No machine map or cycle pressure-loss law responds to cycle flow; only the offered compressor rating (assumed 1600 MW, A6) screens it, and it trips at ≥ 1700 kg/s. | declared seam; flow ≥ 1700 kg/s cases retained as adverse | documented seam (WI-090 design E3/E5) |
| `20260925-aries-reference-heat-electricity-reconciliation#3` | model | Divertor and blanket hydraulics/MHD are unqualified; the cubic pump proxy was bypassed by fixed-power mode wherever flow changed. | declared seam | documented seam (WI-090 design E3) |
| `20260925-aries-reference-heat-electricity-reconciliation#4` | model | Assumed U has no geometry or pressure-drop qualification; tenfold conductance changes unremoved heat by only ≈ 6–12 MW, so conductance is not the limiting mechanism. | declared seam; diagnostic only | documented seam (WI-090 design E2) |
| `20260925-aries-reference-heat-electricity-reconciliation#5` | model | Auxiliary loads (cryogenic, control, other, fuel processing) and deposited heating have no subsystem demand models; the Lyon itemisation is an accounting alignment, not a demand calculation. | declared seam; accounting difference quantified (≈ −18 MW net) | documented seam (WI-089 design A5) |
| `20260925-aries-reference-heat-electricity-reconciliation#6` | model | The deposition partition has no transport model and no divertor nuclear-heating term; the source-informed setting carries 68.8 MW of nuclear heat as charged power. | declared seam; source-informed setting recorded in the contract | documented seam (WI-089 design A1; contract § 8) |
| `20260925-aries-reference-heat-electricity-reconciliation#7` | model | After every input-level correction, 151 MW remains unremoved in the PbLi stage: the series helium → divertor → PbLi closure heats the cycle helium through the divertor stage before the PbLi stage, and the PbLi capacity rate (5.10 MW/K) is below the cycle's, so the PbLi cannot be cooled below ≈ 475 °C against the published 451 °C. Raffray Fig. 12 places the PbLi and divertor stages in parallel. | routed: model increment in the next goal round (topology alternative) after design review | modeling item (to be opened under goal `aries-reference-heat-electricity-reconciliation`) |
| `20260925-aries-reference-heat-electricity-reconciliation#8` | model | At the source's 0.95 recuperation, full heat removal on this package needs cycle flow between 1700 and 1800 kg/s, above the assumed compressor rating; the only all-checks-satisfied source-conditioned cases use 0.8 recuperation at 1600 kg/s (net 760–774 MW, efficiency ≈ 0.345). | bounded result carried into the goal ledger | goal `answer.md` discrepancy ledger |
| `20260925-aries-reference-heat-electricity-reconciliation#9` | process | The native baseline point in `preparation/` was executed before the axis set was extended from 16 to 18 axes; manifest and package were unchanged, indicators and preflight were rerun, and the baseline was not re-executed. | recorded; no rerun needed | this record § 9 |
| `20260925-aries-reference-heat-electricity-reconciliation#10` | model | The published chain 2916 MW → 43% → 1253 → −253 → 1000 is a systems-code constant applied to all thermal power; the contract's Q1 (independently checked) shows the published temperatures, duties and series-first arrangement cannot all hold, so the model's unmet heat and lower efficiency are partly a property of the published design description, not only of the model. | routed: goal answer and learnings; owner-visible premise surprise | goal `answer.md`; `learnings.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `dae3a4652ea16cbba42914e3d7174b27a9d112359a3c88307a316d1a573dba78`
- **Schema version:** `1`

No snapshot content is restated here.

## 17. What this record does not contain

- The native baseline work store (`preparation/_work`) executed for the baseline gate was not retained, as in the predecessor records; `preparation/baseline_result.json` names its case id and store id.
- No administrator (cold-record) synthesis: `synthesis.md` is the executor's reading and says so.
- No plots: the attribution ledger (`results/attribution.json`, `results/attribution.md`) and `results/cases.csv` carry the presentation numbers; PNG/PDF plots belong to the goal answer if needed.
- No topology alternative: the series helium → divertor → PbLi closure is the only network this package can evaluate; finding #7 routes the parallel-stage alternative to a later goal round.
- No source reconstruction of the Lyon case's per-circuit heat split at 2436 MW: the per-circuit comparison values in the goal ledger use the stated scaling rule from Raffray's 2365 MW case and are not in this record.
- The TEAx revision is reported as `unrecorded` by the verifier and resolved through `results/integration_return_used.json`, as in the predecessor records.
- The goal-level attribution and discrepancy ledger (original → revised → cause) live in the goal directory, not here; this record holds the native cases and the presentation arithmetic only.
