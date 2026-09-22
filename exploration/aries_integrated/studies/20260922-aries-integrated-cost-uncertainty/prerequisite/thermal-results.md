# Thermal sensitivity reading

[AGENT] Executor interpretation from stored native results. Read this before the equipment/cost discussion. Every number below is a named low/high case in results/cases.json; results/analysis.json retains the full mapping. Net output from a case with a violated engineering check is a diagnostic value, not a usable plant alternative.

| Axis | Low/high input | Units | Low/high net MW | Low/high unmet MW | Violations |
|---|---|---|---|---|---|
| cycle_flow | 1000 / 1800 | kg/s | 596.773 / 149.663 | 138.638 / 0.000 | cycle_flow-low: plant_ledger.heat_removal_ok; cycle_flow-high: compressor_capacity.capacity_ok |
| neutron_multiplier | 1 / 1.25 | dimensionless | 254.022 / 518.217 | 0.000 / 0.000 | none |
| recuperator_effectiveness | 0.6 / 0.95 | dimensionless | 310.053 / 557.114 | 0.000 / 0.000 | none |
| he_operating_flow | 1630.5 / 4891.5 | kg/s | 470.814 / 293.616 | 0.000 / 0.000 | he_operating_flow-high: he_pump.capacity_ok |
| common_compressor_efficiency | 0.84 / 0.92 | dimensionless | 346.945 / 464.830 | 0.000 / 0.000 | none |
| pbli_operating_flow | 13430 / 40290 | kg/s | 367.082 / 423.083 | 77.857 / 0.000 | pbli_operating_flow-low: plant_ledger.heat_removal_ok; pbli_operating_flow-high: pbli_pump.capacity_ok |
| turbine_efficiency | 0.88 / 0.95 | dimensionless | 377.289 / 440.633 | 0.000 / 0.000 | none |
| common_cold_sink | 298.15 / 318.15 | K | 454.165 / 392.049 | 0.000 / 0.000 | none |
| pressure_loss | 0.02 / 0.08 | dimensionless | 436.654 / 402.802 | 0.000 / 0.000 | none |
| he_pump_efficiency | 0.6 / 0.9 | dimensionless | 404.933 / 429.165 | 0.000 / 0.000 | none |
| heating_efficiency | 0.4 / 0.7 | dimensionless | 413.107 / 434.535 | 0.000 / 0.000 | none |
| divertor_operating_flow | 250 / 750 | kg/s | 426.189 / 414.740 | 0.000 / 0.000 | divertor_operating_flow-high: divertor_pump.capacity_ok |
| cryo_load | 5 / 15 | MW | 428.107 / 418.107 | 0.000 / 0.000 | none |
| control_load | 2.5 / 7.5 | MW | 425.607 / 420.607 | 0.000 / 0.000 | none |
| other_electric_load | 2.5 / 7.5 | MW | 425.607 / 420.607 | 0.000 / 0.000 | none |
| pbli_hot_limit | 961.15 / 1061.15 | K | 423.107 / 423.107 | 0.000 / 0.000 | none |
| divertor_hot_limit | 923.15 / 1023.15 | K | 423.107 / 423.107 | 0.000 / 0.000 | none |
| he_hot_limit | 679.15 / 779.15 | K | 423.107 / 423.107 | 0.000 / 0.000 | none |
| he_u | 500 / 1500 | W/(m2 K) | 423.107 / 423.107 | 0.000 / 0.000 | none |
| pbli_u | 500 / 1500 | W/(m2 K) | 423.107 / 423.107 | 0.000 / 0.000 | none |
| divertor_u | 500 / 1500 | W/(m2 K) | 423.107 / 423.107 | 0.000 / 0.000 | none |
| helium_partition | 0.3 / 0.46 | dimensionless | 423.107 / 423.107 | 0.000 / 0.000 | none |
| radiation_partition | 0.1 / 0.4 | dimensionless | 423.107 / 423.107 | 0.000 / 0.000 | none |
| intercoolant_exchange | 0.02 / 0.06 | dimensionless | 423.107 / 423.107 | 0.000 / 0.000 | none |
| pbli_cp | 170 / 220 | J/(kg K) | 423.107 / 423.107 | 0.000 / 0.000 | none |

[AGENT] Rows are ordered by maximum absolute net change from the assumed423.106794MW baseline over these engineered endpoints. The windows differ in physical meaning and width, so this is a finite-perturbation comparison, not a probability-based uncertainty ranking. Cycle flow, neutron multiplier, recuperation and helium circulation deserve attention within this approximation. Heat removal and installed capacities must be considered together with net output.

[AGENT] Net-flat thermal axes are not all disconnected. U changes calculated UA while inventory remains fixed; branch flow/cp and bulk bounds enter the finite exchanger calculation. In these particular nominal windows, all available source heat is still accepted. Partition changes redistribute branch duty but leave the total accepted heat unchanged. These results cannot establish global nonresponse. Four recuperator/PbLi-hot-limit corners likewise show no additional hot-limit effect within their sampled window.

[AGENT] All54 thermal points preserve the complete upfront purchase-account set and overnight total exactly. Pump electrical demand responds to operating flow/efficiency through the disclosed proxy. Recuperator/material/machine-quality and auxiliary assumptions lack the corresponding qualified performance/purchase coupling. No endpoint is promoted to an optimized design.
