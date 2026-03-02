# Validation Matrix

Verification criteria for the integrated system — checks that go beyond individual work items. Each entry defines what to verify, how to verify it, and what constitutes success.

## Verification Types

| Type | What it checks |
|------|---------------|
| reasonableness | Output is in expected ballpark (order-of-magnitude sanity) |
| baseline | Output matches a reference implementation or known-good value |
| physical | Conservation laws or physical constraints hold |
| relationship | Input/output vary in expected direction (sensitivity) |
| rollup | Aggregations are internally consistent |

## Verification Mechanisms

| Mechanism | How the check runs |
|-----------|--------------------|
| model | Verifiable by model inspection or `agentic-mbse validate` |
| test | Verifiable by pytest (may include codegen + simulation) |
| manual | Requires human judgment |

## Verification Registry

| ID | Description | Type | Mechanism | Expected | Tolerance | Source | Test | Status |
|----|-------------|------|-----------|----------|-----------|--------|------|--------|
| SV-001 | Foundation types parse without errors | baseline | test | 0 parse errors | exact | Level 1 validation | test_foundation_types_parse_without_errors | passing |
| SV-002 | Foundation units parse without errors | baseline | test | 0 parse errors | exact | Level 1 validation | test_foundation_units_parse_without_errors | passing |
| SV-003 | Foundation materials parse without errors | baseline | test | 0 parse errors | exact | Level 1 validation | test_foundation_materials_parse_without_errors | passing |
| SV-004 | All foundation files parse together | baseline | test | 0 parse errors | exact | Level 2 integration | test_all_foundation_files_parse_together | passing |
| SV-005 | Library (foundation + calculations) parses | baseline | test | 0 parse errors | exact | Level 1 validation | test_library_parses_without_errors (power_balance) | passing |
| SV-006 | Power balance files parse with dependencies | baseline | test | 0 parse errors | exact | PowerBalance.py | test_power_balance_parses_without_errors | passing |
| SV-007 | Full model (library + designs) parses | baseline | test | 0 parse errors | exact | Level 1 validation | test_full_model_parses_without_errors | passing |
| SV-008 | Design references resolve to library defs | baseline | test | 0 unresolved refs | exact | Level 2 validation | test_design_references_resolve | passing |
| SV-009 | Enum definitions count meets minimum | baseline | test | >= 13 enums | minimum | PR-004 | test_enum_definitions_count | passing |
| SV-010 | ReactorType enum has MFE, IFE, MIF | baseline | test | {MFE, IFE, MIF} | exact set | PyFECONS, DI-010 | test_reactor_type_variants | passing |
| SV-011 | ConfinementType has sufficient variants | baseline | test | >= 12 variants | minimum | PyFECONS | test_confinement_type_variants_count | passing |
| SV-012 | All 13 expected enums exist | baseline | test | 13 named enums | exact set | PR-004 | test_all_expected_enums_exist | passing |
| SV-013 | Custom economic units defined | baseline | test | {M_USD, USD_KG, USD_M3, USD_W, Percent, Ratio} | exact set | PR-005 | test_custom_units_defined | passing |
| SV-014 | Material definitions count meets minimum | baseline | test | >= 10 part defs | minimum | PR-005 | test_materials_exist | passing |
| SV-015 | Materials have required attributes | baseline | test | density, thermal_conductivity, unit_cost | exact set per part | PR-005 | test_all_materials_have_required_attributes | passing |
| SV-016 | Foundation element counts meet minimums | baseline | test | >= 13 enums, >= 6 attrs, >= 12 parts | minimums | Level 2 validation | test_foundation_element_counts | passing |
| SV-017 | Power balance SysML files exist | baseline | test | Files present | exact | PowerBalance.py | test_power_balance_sysml_exists, test_mfe_power_balance_sysml_exists | passing |
| SV-018 | Alpha Power Calc definition exists | baseline | test | Calc def present | exact | PowerBalance.py | test_alpha_power_calc_exists | passing |
| SV-019 | Power Balance Calc definition exists | baseline | test | Calc def present | exact | PowerBalance.py | test_power_balance_calc_exists | passing |
| SV-020 | MFE Power Balance Calc definition exists | baseline | test | Calc def present | exact | PowerBalance.py | test_mfe_power_balance_calc_exists | passing |
| SV-021 | Alpha Power Calc has p_nrl input | baseline | test | Input present | exact | PowerBalance.py:98 | test_has_p_nrl_input | passing |
| SV-022 | Alpha Power Calc has fuel_type input | baseline | test | Input present | exact | PowerBalance.py:98 | test_has_fuel_type_input | passing |
| SV-023 | Alpha Power Calc has p_alpha output | baseline | test | Output present | exact | PowerBalance.py:98 | test_has_p_alpha_output | passing |
| SV-024 | MFE Power Balance Calc has 16 required inputs | baseline | test | All 16 inputs | exact set | PowerBalance.py | test_has_all_required_inputs | passing |
| SV-025 | MFE Power Balance Calc has p_net output | baseline | test | Output present | exact | PowerBalance.py:50 | test_has_p_net_output | passing |
| SV-026 | MFE Calc has intermediate outputs | baseline | test | p_net accessible | exact | PowerBalance.py:15-48 | test_has_intermediate_outputs | passing |
| SV-027 | Alpha Power Calc has documentation | baseline | model | Doc present | non-empty | PR-002 | test_alpha_power_calc_has_doc | passing |
| SV-028 | MFE Power Balance Calc has documentation | baseline | model | Doc present | non-empty | PR-002 | test_mfe_power_balance_calc_has_doc | passing |
| SV-029 | Alpha power for DT fuel | baseline | test | ~520.4 MW (coefficient ±0.001) | < 0.5 MW | PowerBalance.py:98 | test_alpha_power_dt_fuel | passing |
| SV-030 | Alpha power for DD fuel | baseline | test | Coefficient ~0.5006 | ±0.001 | PowerBalance.py:100 | test_alpha_power_dd_fuel | passing |
| SV-031 | Alpha power for DHe3 fuel | baseline | test | Coefficient ~0.8033 | ±0.001 | PowerBalance.py:102 | test_alpha_power_dhe3_fuel | passing |
| SV-032 | Alpha power for PB11 fuel (aneutronic) | baseline | test | Coefficient = 1.0 | ±0.001 | PowerBalance.py:104 | test_alpha_power_pb11_fuel | passing |
| SV-033 | Neutron power calculation | baseline | test | ~2079.6 MW | < 0.5 MW | PowerBalance.py:11 | test_neutron_power | passing |
| SV-034 | Scientific Q-factor | baseline | test | 52.0 | ±0.01 | PowerBalance.py:28 | test_scientific_q | passing |
| SV-035 | Thermal power from neutrons | reasonableness | test | 2300-2500 MW | range | PowerBalance.py:15-21 | test_thermal_power | passing |
| SV-036 | Thermal-electric power conversion | reasonableness | test | 1000-1200 MW | range | PowerBalance.py:22 | test_thermal_electric_power | passing |
| SV-037 | Engineering Q-factor components | reasonableness | test | 4-6 (simplified) | range | PowerBalance.py:29-48 | test_engineering_q_components | passing |
| SV-038 | Net electric power output | reasonableness | test | 800-950 MW (simplified) | range | PowerBalance.py:50 | test_net_electric_power | passing |
| SV-039 | Total capital cost ballpark | reasonableness | test | $3B-$15B | range | Engineering judgment | — | pending |
| SV-040 | Energy balance conservation | physical | test | Sum of parts = total | ±0.1% | Physics | — | pending |
| SV-041 | LCOE within expected bounds | reasonableness | test | 30-200 $/MWh | range | DI-012 | — | pending |
| SV-042 | CAS22 fraction of total cost | reasonableness | test | 30-70% | range | DI-012 | — | pending |
