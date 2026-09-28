# Cost uncertainty study preparation

## 1. Study header

Study id: `20260922-aries-integrated-cost-uncertainty`. Package: `aries_integrated`. Executor: study worker, 2026-09-22. Single arm answering conditional accounting uncertainty. Executed at `bd9b9aec5fabda5e9a14d53df84f108d52f7f183`: 113 proposed points, 113 completed native attempts. Execution, all-point verification and coordinator snapshot/archive capture are complete. Independent interpretation review follows this immutable commit.

## 2. Intake

[OWNER-VERBATIM, captured in prerequisite/goal.md]

> Before ranking equipment or economic alternatives, test sensitivity to the principal thermal assumptions and connect each varied equipment capability to its selected inventory, purchase cost and applicable operating demand. Preserve the source-case failures and label the 423.1 MW case as the assumed integrated baseline.

[AGENT, coordinator-authorized scope] The accepted thermal reading is the prerequisite for this accounting round. Quantify finite sensitivity of initial capital, annual operating costs and scheduled replacement costs to accepted assumptions on the same thermal baseline. Preserve source failures and separate no-credit from independently supplied recovery. `prerequisite/cost-study-brief.md` supplies the bounded execution contract.

## 3. Objective and result

No LCOE channel or optimization objective is requested. Native overnight capital spans USD2004 1,623,355,845–13,331,716,800 among the sampled assumed-baseline scenarios. Combined no-credit annual operating expense is USD2004 893,907,253.092–11,959,761,809.990/year; the separate supplied-100 kg/year corners give 36,005,723.707–1,959,761,809.990/year. These are engineered scenario corners, not calibrated bounds or a probability envelope. Initial, annual and replacement amounts are separate. See `report.md`, `cost-results.md` and `results/cost-analysis.json` for contribution tables, finite changes and exact stored outputs.

## 4. Constraint outcomes

Every exact predicate is retained. All 110 conditional baseline-family points satisfy every scoped check. Only the three inherited source controls fail: all three heat-removal checks; literal Raffray also fails the balance check. Their net outputs are incomplete/constraint-failing diagnostics, not usable power alternatives.

| Constraint id | Local identity | Status counts |
| --- | --- | --- |
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | balances_ok | {'satisfied': 112, 'violated': 1} |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | heat_removal_ok | {'satisfied': 110, 'violated': 3} |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | capacity_ok | {'satisfied': 113} |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | capacity_ok | {'satisfied': 113} |

## 5. Framing

All 53 axes were proposed as sensitivity and remain sensitivity after execution; none changed framing. The 48 no-constraint-response groups retain their pre-execution owner-authorized rulings and missing-response findings. Observed accounting movement, equal net output or a satisfied scalar check supplies no scientific qualification, probability bound or optimum.

## 6. Per-axis account

#### auxiliary_cooling_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### auxiliary_cooling_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| auxiliary_cooling_price-low | -2782575 | 0 | 0 |
| auxiliary_cooling_price-high | 2782575 | 0 | 0 |

#### blanket_inventory_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### blanket_inventory_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| blanket_inventory_price-low | -44213515 | 0 | -178041000 |
| blanket_inventory_price-high | 44213515 | 0 | 178041000 |

#### compressor_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### compressor_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| compressor_equipment_price-low | -58586427.5 | 0 | 0 |
| compressor_equipment_price-high | 58586427.5 | 0 | 0 |

#### conversion_services_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### conversion_services_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| conversion_services_price-low | -46869142 | 0 | 0 |
| conversion_services_price-high | 46869142 | 0 | 0 |

#### divertor_duty_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### divertor_duty_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| divertor_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| divertor_duty_equipment_price-high | 24140359.1667 | 0 | 0 |

#### divertor_hx_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### divertor_hx_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| divertor_hx_price-low | -43452646.5 | 0 | 0 |
| divertor_hx_price-high | 43452646.5 | 0 | 0 |

#### divertor_inventory_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### divertor_inventory_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| divertor_inventory_price-low | -3961910 | 0 | -15954000 |
| divertor_inventory_price-high | 3961910 | 0 | 15954000 |

#### divertor_pump_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### divertor_pump_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| divertor_pump_price-low | -14484215.5 | 0 | 0 |
| divertor_pump_price-high | 14484215.5 | 0 | 0 |

#### electrical_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### electrical_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| electrical_equipment_price-low | -103379180 | 0 | 0 |
| electrical_equipment_price-high | 103379180 | 0 | 0 |

#### facilities_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### facilities_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| facilities_price-low | -250419085 | 0 | 0 |
| facilities_price-high | 250419085 | 0 | 0 |

#### fuel_processing_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fuel_processing_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fuel_processing_equipment_price-low | -12359550 | 0 | 0 |
| fuel_processing_equipment_price-high | 12359550 | 0 | 0 |

#### fuel_services_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fuel_services_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fuel_services_price-low | -28823305 | 0 | 0 |
| fuel_services_price-high | 28823305 | 0 | 0 |

#### generator_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### generator_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| generator_equipment_price-low | -35151856.5 | 0 | 0 |
| generator_equipment_price-high | 35151856.5 | 0 | 0 |

#### he_duty_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### he_duty_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| he_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| he_duty_equipment_price-high | 24140359.1667 | 0 | 0 |

#### he_hx_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### he_hx_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| he_hx_price-low | -43452646.5 | 0 | 0 |
| he_hx_price-high | 43452646.5 | 0 | 0 |

#### he_pump_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### he_pump_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| he_pump_price-low | -14484215.5 | 0 | 0 |
| he_pump_price-high | 14484215.5 | 0 | 0 |

#### heat_rejection_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### heat_rejection_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| heat_rejection_equipment_price-low | -41784070 | 0 | 0 |
| heat_rejection_equipment_price-high | 41784070 | 0 | 0 |

#### heating_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### heating_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| heating_equipment_price-low | -49488115 | 0 | 0 |
| heating_equipment_price-high | 49488115 | 0 | 0 |

#### impurity_control_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### impurity_control_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| impurity_control_price-low | -4887945 | 0 | 0 |
| impurity_control_price-high | 4887945 | 0 | 0 |

#### instrumentation_control_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### instrumentation_control_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| instrumentation_control_price-low | -33195710 | 0 | 0 |
| instrumentation_control_price-high | 33195710 | 0 | 0 |

#### lipb_inventory_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### lipb_inventory_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| lipb_inventory_price-low | -112738615 | 0 | -22699050 |
| lipb_inventory_price-high | 112738615 | 0 | 22699050 |

#### magnet_inventory_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### magnet_inventory_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| magnet_inventory_price-low | -152134960 | 0 | 0 |
| magnet_inventory_price-high | 152134960 | 0 | 0 |

#### magnet_power_supplies_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### magnet_power_supplies_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| magnet_power_supplies_price-low | -52614880 | 0 | 0 |
| magnet_power_supplies_price-high | 52614880 | 0 | 0 |

#### miscellaneous_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### miscellaneous_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| miscellaneous_equipment_price-low | -52863710 | 0 | 0 |
| miscellaneous_equipment_price-high | 52863710 | 0 | 0 |

#### other_reactor_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### other_reactor_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| other_reactor_equipment_price-low | -45238635 | 0 | 0 |
| other_reactor_equipment_price-high | 45238635 | 0 | 0 |

#### pbli_duty_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pbli_duty_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| pbli_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| pbli_duty_equipment_price-high | 24140359.1667 | 0 | 0 |

#### pbli_hx_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pbli_hx_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| pbli_hx_price-low | -43452646.5 | 0 | 0 |
| pbli_hx_price-high | 43452646.5 | 0 | 0 |

#### pbli_pump_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pbli_pump_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| pbli_pump_price-low | -14484215.5 | 0 | 0 |
| pbli_pump_price-high | 14484215.5 | 0 | 0 |

#### primary_piping_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### primary_piping_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| primary_piping_price-low | -43452646.5 | 0 | 0 |
| primary_piping_price-high | 43452646.5 | 0 | 0 |

#### primary_support_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### primary_support_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| primary_support_price-low | -54478870 | 0 | 0 |
| primary_support_price-high | 54478870 | 0 | 0 |

#### secondary_transport_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### secondary_transport_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| secondary_transport_price-low | -64020085 | 0 | 0 |
| secondary_transport_price-high | 64020085 | 0 | 0 |

#### shield_inventory_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### shield_inventory_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| shield_inventory_price-low | -170327115 | 0 | 0 |
| shield_inventory_price-high | 170327115 | 0 | 0 |

#### site_land_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### site_land_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| site_land_price-low | -9632105 | 0 | 0 |
| site_land_price-high | 9632105 | 0 | 0 |

#### turbine_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### turbine_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| turbine_equipment_price-low | -93738284 | 0 | 0 |
| turbine_equipment_price-high | 93738284 | 0 | 0 |

#### unallocated_source_scope_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### unallocated_source_scope_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| unallocated_source_scope_price-low | -21155020 | 0 | 0 |
| unallocated_source_scope_price-high | 42310040 | 0 | 0 |

#### vacuum_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### vacuum_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| vacuum_equipment_price-low | -102165575 | 0 | 0 |
| vacuum_equipment_price-high | 102165575 | 0 | 0 |

#### vf_coils_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### vf_coils_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| vf_coils_price-low | -9951710 | 0 | 0 |
| vf_coils_price-high | 9951710 | 0 | 0 |

#### waste_equipment_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### waste_equipment_price — observed response (sensitivity framing)

**Applies:** yes. Supplied price uncertainty has no market calibration or purchased quality response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| waste_equipment_price-low | -4957975 | 0 | 0 |
| waste_equipment_price-high | 4957975 | 0 | 0 |

#### fuel_inventory_tritium_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fuel_inventory_tritium_price — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fuel_inventory_tritium_price-low | -298000000 | -2093354140.46 | 0 |
| fuel_inventory_tritium_price-high | 1043000000 | 7326739491.63 | 0 |

#### fuel_inventory_selected_tritium_kg — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fuel_inventory_selected_tritium_kg — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fuel_inventory_selected_tritium_kg-low | -402300000 | -15179923.2543 | 0 |
| fuel_inventory_selected_tritium_kg-high | 894000000 | 33733162.7873 | 0 |

#### fuel_inventory_deuterium_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fuel_inventory_deuterium_price — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fuel_inventory_deuterium_price-low | 0 | -62551.9437575 | 0 |
| fuel_inventory_deuterium_price-high | 0 | 625519.437574 | 0 |

#### annual_om_selected_amount — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### annual_om_selected_amount — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| annual_om_selected_amount-low | 0 | -35000000 | 0 |
| annual_om_selected_amount-high | 0 | 70000000 | 0 |

#### cost_ledger_consumables — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### cost_ledger_consumables — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| cost_ledger_consumables-low | 0 | -4000000 | 0 |
| cost_ledger_consumables-high | 0 | 10000000 | 0 |

#### indirect_cost_fraction — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### indirect_cost_fraction — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| indirect_cost_fraction-low | -350352360 | 0 | 0 |
| indirect_cost_fraction-high | 350352360 | 0 | 0 |

#### contingency_fraction — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### contingency_fraction — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| contingency_fraction-low | -350352360 | 0 | 0 |
| contingency_fraction-high | 700704720 | 0 | 0 |

#### owner_commissioning_fraction — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### owner_commissioning_fraction — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| owner_commissioning_fraction-low | -87588090 | 0 | 0 |
| owner_commissioning_fraction-high | 145980150 | 0 | 0 |

#### cost_schedule_replacement_life_fpy — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### cost_schedule_replacement_life_fpy — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| cost_schedule_replacement_life_fpy-low | 0 | 0 | 722313500 |
| cost_schedule_replacement_life_fpy-high | 0 | 0 | -144462700 |

#### cost_schedule_replacement_factor — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### cost_schedule_replacement_factor — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| cost_schedule_replacement_factor-low | 0 | 0 | -216694050 |
| cost_schedule_replacement_factor-high | 0 | 0 | 433388100 |

#### cost_schedule_lipb_makeup_fraction — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### cost_schedule_lipb_makeup_fraction — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| cost_schedule_lipb_makeup_fraction-low | 0 | 0 | -45398100 |
| cost_schedule_lipb_makeup_fraction-high | 0 | 0 | 136194300 |

#### cost_schedule_availability — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### cost_schedule_availability — observed response (sensitivity framing)

**Applies:** yes. Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| cost_schedule_availability-low | 0 | -551158964.376 | -72231350 |
| cost_schedule_availability-high | 0 | 367439309.584 | 72231350 |

#### supplied_recovery — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### supplied_recovery — observed response (sensitivity framing)

**Applies:** yes. Independently supplied recovery is not a calculated breeding capability; support remains zero. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope; it is a boundary scenario, not purchased-capability optimization. The declared window is 0–200 kg/year; baseline supplies the zero endpoint and 100 is an explicit midpoint.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| recovery-100 | 0 | -3000000000 | 0 |
| recovery-200 | 0 | -3140031210.7 | 0 |

#### purchase_mode — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### purchase_mode — observed response (sensitivity framing)

**Applies:** yes. Fixed budget mode deliberately suppresses selected quantity price response. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| fixed-budget-nominal | 0 | 0 | 0 |
| adequate-area-mode-0 | 43452646.5 | 0 | 0 |
| adequate-area-mode-1 | 0 | 0 | 0 |

#### adequate_he_area — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### adequate_he_area — observed response (sensitivity framing)

**Applies:** yes. Previously tested adequate area is not geometry or hydraulic qualification. No boundary or optimum claim is made. Every listed case satisfies all scoped checks; net power remains 423.10679410931664 MW.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacement USD2004 |
| --- | ---: | ---: | ---: |
| adequate-area-mode-0 | 43452646.5 | 0 | 0 |
| adequate-area-mode-1 | 0 | 0 | 0 |

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
| --- | --- | --- | --- |
| auxiliary_cooling_price | `aries_integrated_plant__auxiliary_cooling__price_factor` | fan_out | One public owner; dimensionless. |
| blanket_inventory_price | `aries_integrated_plant__blanket_inventory__price_factor` | fan_out | One public owner; dimensionless. |
| compressor_equipment_price | `aries_integrated_plant__compressor_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| conversion_services_price | `aries_integrated_plant__conversion_services__price_factor` | fan_out | One public owner; dimensionless. |
| divertor_duty_equipment_price | `aries_integrated_plant__divertor_duty_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| divertor_hx_price | `aries_integrated_plant__divertor_hx__price_factor` | fan_out | One public owner; dimensionless. |
| divertor_inventory_price | `aries_integrated_plant__divertor_inventory__price_factor` | fan_out | One public owner; dimensionless. |
| divertor_pump_price | `aries_integrated_plant__divertor_pump__price_factor` | fan_out | One public owner; dimensionless. |
| electrical_equipment_price | `aries_integrated_plant__electrical_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| facilities_price | `aries_integrated_plant__facilities__price_factor` | fan_out | One public owner; dimensionless. |
| fuel_processing_equipment_price | `aries_integrated_plant__fuel_processing_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| fuel_services_price | `aries_integrated_plant__fuel_services__price_factor` | fan_out | One public owner; dimensionless. |
| generator_equipment_price | `aries_integrated_plant__generator_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| he_duty_equipment_price | `aries_integrated_plant__he_duty_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| he_hx_price | `aries_integrated_plant__he_hx__price_factor` | fan_out | One public owner; dimensionless. |
| he_pump_price | `aries_integrated_plant__he_pump__price_factor` | fan_out | One public owner; dimensionless. |
| heat_rejection_equipment_price | `aries_integrated_plant__heat_rejection_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| heating_equipment_price | `aries_integrated_plant__heating_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| impurity_control_price | `aries_integrated_plant__impurity_control__price_factor` | fan_out | One public owner; dimensionless. |
| instrumentation_control_price | `aries_integrated_plant__instrumentation_control__price_factor` | fan_out | One public owner; dimensionless. |
| lipb_inventory_price | `aries_integrated_plant__lipb_inventory__price_factor` | fan_out | One public owner; dimensionless. |
| magnet_inventory_price | `aries_integrated_plant__magnet_inventory__price_factor` | fan_out | One public owner; dimensionless. |
| magnet_power_supplies_price | `aries_integrated_plant__magnet_power_supplies__price_factor` | fan_out | One public owner; dimensionless. |
| miscellaneous_equipment_price | `aries_integrated_plant__miscellaneous_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| other_reactor_equipment_price | `aries_integrated_plant__other_reactor_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| pbli_duty_equipment_price | `aries_integrated_plant__pbli_duty_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| pbli_hx_price | `aries_integrated_plant__pbli_hx__price_factor` | fan_out | One public owner; dimensionless. |
| pbli_pump_price | `aries_integrated_plant__pbli_pump__price_factor` | fan_out | One public owner; dimensionless. |
| primary_piping_price | `aries_integrated_plant__primary_piping__price_factor` | fan_out | One public owner; dimensionless. |
| primary_support_price | `aries_integrated_plant__primary_support__price_factor` | fan_out | One public owner; dimensionless. |
| secondary_transport_price | `aries_integrated_plant__secondary_transport__price_factor` | fan_out | One public owner; dimensionless. |
| shield_inventory_price | `aries_integrated_plant__shield_inventory__price_factor` | fan_out | One public owner; dimensionless. |
| site_land_price | `aries_integrated_plant__site_land__price_factor` | fan_out | One public owner; dimensionless. |
| turbine_equipment_price | `aries_integrated_plant__turbine_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| unallocated_source_scope_price | `aries_integrated_plant__unallocated_source_scope__price_factor` | fan_out | One public owner; dimensionless. |
| vacuum_equipment_price | `aries_integrated_plant__vacuum_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| vf_coils_price | `aries_integrated_plant__vf_coils__price_factor` | fan_out | One public owner; dimensionless. |
| waste_equipment_price | `aries_integrated_plant__waste_equipment__price_factor` | fan_out | One public owner; dimensionless. |
| fuel_inventory_tritium_price | `aries_integrated_plant__fuel_inventory__tritium_price` | fan_out | One public owner; USD2004/kg. |
| fuel_inventory_selected_tritium_kg | `aries_integrated_plant__fuel_inventory__selected_tritium_kg` | fan_out | One public owner; kg. |
| fuel_inventory_deuterium_price | `aries_integrated_plant__fuel_inventory__deuterium_price` | fan_out | One public owner; USD2004/kg. |
| annual_om_selected_amount | `aries_integrated_plant__annual_om__selected_amount` | fan_out | One public owner; USD2004/year. |
| cost_ledger_consumables | `aries_integrated_plant__cost_ledger__consumables` | fan_out | One public owner; USD2004/year. |
| indirect_cost_fraction | `aries_integrated_plant__indirect_cost__fraction` | fan_out | One public owner; dimensionless. |
| contingency_fraction | `aries_integrated_plant__contingency__fraction` | fan_out | One public owner; dimensionless. |
| owner_commissioning_fraction | `aries_integrated_plant__owner_commissioning__fraction` | fan_out | One public owner; dimensionless. |
| cost_schedule_replacement_life_fpy | `aries_integrated_plant__cost_schedule__replacement_life_fpy` | fan_out | One public owner; full-power years. |
| cost_schedule_replacement_factor | `aries_integrated_plant__cost_schedule__replacement_factor` | fan_out | One public owner; dimensionless. |
| cost_schedule_lipb_makeup_fraction | `aries_integrated_plant__cost_schedule__lipb_makeup_fraction` | fan_out | One public owner; dimensionless. |
| cost_schedule_availability | `aries_integrated_plant__cost_schedule__availability` | fan_out | One public owner; dimensionless. |
| supplied_recovery | `aries_integrated_plant__fuel_inventory__annual_recovery_kg` | fan_out | One public owner; kg/year. |
| purchase_mode | `aries_integrated_plant__cost_accounts__estimate_mode` | fan_out | One public owner; enumeration. |
| adequate_he_area | `aries_integrated_plant__he_hx__selected_area` | fan_out | One public owner; m2. |

Combined economic corners explicitly co-vary the first 50 axes in `axis-plan.json`; replacement life uses eight years at the lower-cost corner and two at the higher-cost corner. Each corner has independent supplied recovery fixed at zero or 100 kg/year. Adequate-area cases jointly select area and purchase mode. These scenario ties are coordinated assignments in the full maps, not equality identities. There are no manifest equality ties.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Finding |
| --- | --- | --- | --- |
| auxiliary_cooling_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#1 |
| blanket_inventory_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#2 |
| compressor_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#3 |
| conversion_services_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#4 |
| divertor_duty_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#5 |
| divertor_hx_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#6 |
| divertor_inventory_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#7 |
| divertor_pump_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#8 |
| electrical_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#9 |
| facilities_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#10 |
| fuel_processing_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#11 |
| fuel_services_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#12 |
| generator_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#13 |
| he_duty_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#14 |
| he_hx_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#15 |
| he_pump_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#16 |
| heat_rejection_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#17 |
| heating_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#18 |
| impurity_control_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#19 |
| instrumentation_control_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#20 |
| lipb_inventory_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#21 |
| magnet_inventory_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#22 |
| magnet_power_supplies_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#23 |
| miscellaneous_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#24 |
| other_reactor_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#25 |
| pbli_duty_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#26 |
| pbli_hx_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#27 |
| pbli_pump_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#28 |
| primary_piping_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#29 |
| primary_support_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#30 |
| secondary_transport_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#31 |
| shield_inventory_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#32 |
| site_land_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#33 |
| turbine_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#34 |
| unallocated_source_scope_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#35 |
| vacuum_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#36 |
| vf_coils_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#37 |
| waste_equipment_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#38 |
| fuel_inventory_tritium_price | constraints_reachable | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#39 |
| fuel_inventory_selected_tritium_kg | constraints_reachable | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#40 |
| fuel_inventory_deuterium_price | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#41 |
| annual_om_selected_amount | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#42 |
| cost_ledger_consumables | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#43 |
| indirect_cost_fraction | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#44 |
| contingency_fraction | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#45 |
| owner_commissioning_fraction | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#46 |
| cost_schedule_replacement_life_fpy | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#47 |
| cost_schedule_replacement_factor | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#48 |
| cost_schedule_lipb_makeup_fraction | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#49 |
| cost_schedule_availability | constraints_reachable | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#50 |
| supplied_recovery | constraints_reachable | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#51 |
| purchase_mode | no_constraint_response | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#52 |
| adequate_he_area | constraints_reachable | Owner-authorized sensitivity; retain missing coupling | 20260922-aries-integrated-cost-uncertainty#53 |

48 groups have no reachable constraint. Each carries its own pre-execution model-development finding in `preparation-findings.json`, with the missing coupling also stated in §6. Existing owner authorization is captured in `prerequisite/goal.md` and the coordinator brief; no new permission is inferred. Zero top-level indicator warnings. Reachability is a possible graph path, not demonstrated response. Monotonicity, physical identity across different keys and intra-module operand dependency are not derivable from indicators.

## 9. Preflight results

All six native gates pass in `preparation/preflight_results.json`: declared keys, sibling scan, sealed identity, manifest currency, baseline headline/verdicts and package cleanliness. The gate reads `preparation/package_identity.json` and `preparation/baseline_result.json`. Two suffix advisories name the independent PbLi and divertor exchanger area owners. They remain held constant, so no equality tie is warranted.

## 10. Execution route and why

The unchanged study-local direct-API route uses the native loader, prepared evaluator, prepared-list strategy, StudyRunner, store lease and query lifecycle. Glue ledger: none; the harness supplies no physical or cost arithmetic. The new baseline/preflight remains under `preparation/` and is copied to `results/integration/`; reused CANDIDATE files have separate provenance.

The native runner completed all 113 points once. The wrapper then rejected three numerically identical mode inputs because it compared JSON strings after the existing float-normalization contract. First export recovery stopped on a transient SQLite sidecar hash check. The second, final mechanical recovery read a disposable copy through native StudyQuery, matched every full map numerically without tolerance, and exported original evidence. It checked original persistent database/artifact hashes unchanged. No evaluator reran, no proposal changed, and no global route, oracle or package changed. Two mechanical recoveries were counted conservatively against the retry cap. `results/export-failures.txt`, diagnosis, pre-recovery content check and recovery proof preserve the evidence. Historical byte parity before the first recovery is not claimed because no such prior digest was saved; content/evidence checks are retained. See `replay.md` for the safe replay path.

## 11. Study definition and window provenance

113 complete maps comprise four canonical controls, 76 price-factor endpoints, 24 other economic endpoints, two recovery cases, three mode/area cases and four combined economic corners. Every map has all 411 public inputs. The 53 axes carry exact keys, units, bounds and engineered provenance in `axis-plan.json`. The 38 price factors vary independently over accepted bounds; no parent comparison account is added as a cost. All fixed-package counts remain one.

The accepted E1–E10 windows are assumption sensitivities, not calibrated probabilities. Combined corners are explicit scenario choices, not guaranteed lower/upper cost bounds. The 40-year horizon, processing residence and import tariff are held. Positive-export cases leave the import-price branch unexercised. Recovery is independently supplied over the declared 0–200 kg/year window, with the explicit 100 kg/year midpoint retained. The baseline and zero-credit corners use 0; no point map changed in this metadata correction. Recovery is never calculated from demand. T stock is selected once for initial cost and shared fuel diagnostics. All scientific support limits remain inherited.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint and single arm; cross-fingerprint correlation is not applicable. Accepted executable and semantic identities are retained in the prepared manifest and baseline receipt. The thermal prerequisite at commit494c329e and its exact snapshot hash are retained in `prerequisite/provenance.json`.

## 13. Verification

Native verification passed ALL 113 rows with 278 scalar channels and 14 exact predicates each: 31,414 scalar comparisons and 1,582 predicate comparisons. No verdict mismatches. The inherited relative 1e-9 rule and explicit 1e-7 MW residual tolerance remain unchanged. The displayed worst relative residual ratio is near-zero denominator behavior, accepted only through the declared dimensional absolute tolerance; no monetary tolerance was relaxed. See `results/verification_summary.json`.

Exact proposal coverage, 113 completed attempts, per-row native evidence digests and export normalization are retained in the recovery proof. Only the three mode scenario integers changed JSON representation to typed floats; numerical values and the 411-field maps are unchanged. The prior frozen thermal record and generated package remain untouched.

## 14. Review outcomes

Independent Round1 PASS is copied in `prerequisite/thermal-study-review.md`. Coordinator accepted and committed this preparation at bd9b9aec, then released T008. Coordinator authorized the two recorded mechanical export recoveries; no evaluation retry occurred. Coordinator checks cover declared windows, exact maps, retained recovery evidence, all-point verification and conditional reporting. The snapshot/archive are captured. Independent cost-study interpretation and goal assessment follow this commit and are recorded in the goal evidence; this executor account does not claim that verdict in advance.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| 20260922-aries-integrated-cost-uncertainty#1 | model | auxiliary_cooling_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#2 | model | blanket_inventory_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#3 | model | compressor_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#4 | model | conversion_services_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#5 | model | divertor_duty_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#6 | model | divertor_hx_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#7 | model | divertor_inventory_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#8 | model | divertor_pump_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#9 | model | electrical_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#10 | model | facilities_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#11 | model | fuel_processing_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#12 | model | fuel_services_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#13 | model | generator_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#14 | model | he_duty_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#15 | model | he_hx_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#16 | model | he_pump_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#17 | model | heat_rejection_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#18 | model | heating_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#19 | model | impurity_control_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#20 | model | instrumentation_control_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#21 | model | lipb_inventory_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#22 | model | magnet_inventory_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#23 | model | magnet_power_supplies_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#24 | model | miscellaneous_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#25 | model | other_reactor_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#26 | model | pbli_duty_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#27 | model | pbli_hx_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#28 | model | pbli_pump_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#29 | model | primary_piping_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#30 | model | primary_support_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#31 | model | secondary_transport_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#32 | model | shield_inventory_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#33 | model | site_land_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#34 | model | turbine_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#35 | model | unallocated_source_scope_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#36 | model | vacuum_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#37 | model | vf_coils_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#38 | model | waste_equipment_price: Supplied price uncertainty has no market calibration or purchased quality response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#39 | model | fuel_inventory_tritium_price: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#40 | model | fuel_inventory_selected_tritium_kg: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#41 | model | fuel_inventory_deuterium_price: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#42 | model | annual_om_selected_amount: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#43 | model | cost_ledger_consumables: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#44 | model | indirect_cost_fraction: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#45 | model | contingency_fraction: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#46 | model | owner_commissioning_fraction: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#47 | model | cost_schedule_replacement_life_fpy: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#48 | model | cost_schedule_replacement_factor: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#49 | model | cost_schedule_lipb_makeup_fraction: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#50 | model | cost_schedule_availability: Accounting sensitivity lacks qualified supply, reliability, lifetime or estimation evidence; selected stock retains its scalar diagnostic only. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#51 | model | supplied_recovery: Independently supplied recovery is not a calculated breeding capability; support remains zero. Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope; it is a boundary scenario, not purchased-capability optimization. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#52 | model | purchase_mode: Fixed budget mode deliberately suppresses selected quantity price response. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#53 | model | adequate_he_area: Previously tested adequate area is not geometry or hydraulic qualification. | Retain sensitivity-only; no optimum or qualification claim. | axis-plan.json |
| 20260922-aries-integrated-cost-uncertainty#54 | model | T price and selected stock dominate the tested one-factor overnight changes; price factors and capital fractions retain finite assumed-window meaning. | Retain assumption ranking; no market-calibrated range. | cost-results.md |
| 20260922-aries-integrated-cost-uncertainty#55 | model | No-credit annual expense is dominated by supplied T price and throughput; independent100kg/year recovery changes baseline annual expense from3.215100713B to0.215100713B USD2004/year. | Carry separate supply boundaries and missing incremental recovery-cost/qualification law. | report.md |
| 20260922-aries-integrated-cost-uncertainty#56 | model | Adequate He area75000m2 gives UA75MW/K in either mode; selected pricing raises overnight43.4526465M while fixed-budget pricing gives no capital response. | Expose fixed-budget nonresponse; no purchased-capability optimum. | cost-results.md |
| 20260922-aries-integrated-cost-uncertainty#57 | model | Replacement assumptions change discrete event counts and separate event/lifetime costs; reserve is an alternative convention. | Keep scheduled replacements separate from annual operations and reserve. | report.md |
| 20260922-aries-integrated-cost-uncertainty#58 | process | Original wrapper export used JSON string equality across integer-to-float mode normalization; two mechanical export recoveries retained original113 native evaluations. | Preserve original evidence and disposable-copy export proof; no global route modification in this study. | results/export-recovery-proof.json |
| 20260922-aries-integrated-cost-uncertainty#59 | model | All110 conditional cases preserve423.106794MW and pass scoped checks; three source controls retain failures and scientific support remainszero. | Preserve thermal prerequisite and scientific limits in financial handoff. | report.md |

## 16. Snapshot

The coordinator captured snapshot.json and sealed-package.tar.gz. Snapshot SHA256 is `3d44612d68a513246f18b8184c9022d5ed3dcd93e9002b13497a8460a7dc4041`; it resolves the exact package, complete manifest, tools, store compatibility tuple and210artifact digests. One arm contains the declared scenario families. Evidence freezes with this commit; later corrections are addenda.

## 17. What this record does not contain

No market calibration, inflation conversion, financing/discounting, LCOE, sales-price scenario or economic optimum is supplied. The ranges cover discrete engineered assumptions only. Recovery lacks an incremental cost/qualification law at fixed installed scope. Positive export leaves the import-tariff branch unexercised. Scientific field/conductor, breeding, deposition, hydraulics, materials and machine-map qualification remain unsupported. Source-conditioned failing net outputs are not usable alternatives. Independent completed-study interpretation and final goal assessment are subsequent goal-review work, outside this executor record.

## Addendum 2026-09-22 — loader links

The committed `preparation/_work/pkg_link/aries_integrated` and `results/native/pkg_link/aries_integrated` symlinks are transient loader conveniences pointing at the working package. They are excluded from snapshot artifact hashes and are not retained model evidence. The immutable executable content is `sealed-package.tar.gz`, with its digest in snapshot.json. Replay creates a fresh loader link against the restored, identity-checked package; no claim in this record depends on either old symlink target. Frozen results, snapshot and archive are unchanged.
