# Exact reviewed 48 kA native capture

The selected local magnet and cryoplant checks pass at the independently supplied35.5 W/m³ winding heating. This is conditional transport, not a demonstrated heating bound for the enlarged geometry. Source, transport and global construction qualification remain zero in the whole-plant model. The native record is preserved unchanged.

Executed `capture.py` through the strict full-system study route: one original control and one reviewed48kA offer. The complete overrides, all values/predicates, evidence digest and package identity are in `declared-cases.json`, `offer-inputs.json`, `native-cases.json` and `package-identity.json`. Protected-file hashes are in `preservation.json`.

Selected geometry: packside.54m,aspect.19,cavity1.30m,48kA,308turns; existing source geometry and48coils held. Cryoplant independently selected40/60kW at USD2025 62957384.24217385. Winding procurement escalation is321.9/130.7; helium rate is converted321.9/334.4; remaining retained material/insulation rates are explicitly requoted USD2025. Field extrapolation is disabled and calculated flag0.

Magnet initial cost2614323601.574602USD2025; fit margin.004619457049m; current margin6687.355927A; peak23.904T; stress399.36MPa; strain.0013312. Cold27730.308885W,intercept41189.504335W,refrigeration2.537567042MW,coil drive.048556634134MW. Cold/intercept capacity margins12269.691115/18810.495665W. Exact component mappings are in `selected-fields.json`.

The altered full-plasma model calculates2748.353598704MW fusion and3258.804490684MW hot source. Its operating point differs from the independently supplied2500/2800MW comparison. New full-plasma sustainment/wall/fuel/primary/conversion failures are retained below. No hardware was tuned to remove them. The whole-plant assembly recalculates source-dependent fuel/primary/divertor/conversion behavior at its chosen source; it does not claim these full-model failures have passed.

The native nuclear heating input has no fusion operand. The chosen fusion ceiling2652.5632625175904MW is a study-domain condition only. Original source35.5W/m³ is a mean for its detailed2700MW neutronics geometry. The reviewed correction adds native same-hardware35.5/50/80W/m³ and extra-cold-watt scenarios, with finite nonnegative domain checks and unchanged40/60kW capacities/quote.50 is a reference stress, not an uncertainty bound. Cold/refri/sink/power/economics respond; source/fuel inversion does not, because the effective1.2 hot-source multiplier excludes cryogenic deposition.

## Retained failed predicates

- `stellarator_09__stellaris__condensate_electric_capacity_ok__a5ca7c5129553d1f` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__condensate_flow_capacity_ok__252eeccf9b929ade` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__condenser_rejection_capacity_ok__b5d2e6443913eb29` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` (also failed in control)
- `stellarator_09__stellaris__electric_gross_capacity_ok__80f1c3ed362e90b1` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__facility_occupancy_ok__2c505953d2466dad` (also failed in control)
- `stellarator_09__stellaris__feedwater_electric_capacity_ok__2274a605654bb912` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__feedwater_flow_capacity_ok__3065124bba3fb314` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__fuel_processing_capacity_ok__ddb8525b2bda8f0a` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__helium_electric_capacity_ok__842a956a27b809da` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__helium_flow_capacity_ok__de4eed99bc4bea72` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__helium_pressure_rise_capacity_ok__7d12d01bc94dde7a` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__helium_pumping_capacity_ok__9e3c5d06ca11e640` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__hp_flow_capacity_ok__f0b30eeb1c674ce4` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__hp_shaft_capacity_ok__a19eda5dff14e4c2` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__lp_flow_capacity_ok__3e0e231ed626fd7d` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__lp_shaft_capacity_ok__70b40123e64ccdf5` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__main_UA_capacity_ok__86518fe643367961` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__reheat_UA_capacity_ok__e377a2da71f404d0` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__salt_electric_capacity_ok__d353ed9e85c5a75b` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__salt_flow_capacity_ok__76ca6d6f7320b2d1` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__salt_shaft_capacity_ok__9a14c3c81e97c1d0` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` (also failed in control)
- `stellarator_09__stellaris__turbine_gross_capacity_ok__1668a7a2950bf2c4` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__water_electric_capacity_ok__da93435fdb1e0e2d` (also failed in control)
- `stellarator_09__stellaris__water_flow_capacity_ok__a2c7af45d6a66edb` (new at altered full-plasma operating point)
- `stellarator_09__stellaris__water_rejection_capacity_ok__c6f88b0bf20410d2` (new at altered full-plasma operating point)
