# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 134 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `whole_plant_conversion_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from whole_plant_conversion_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Supplied_Purchase_Cost | `run_supplied_purchase_cost` | `root-0/mfe_account_costs.sysml:17` | High |
| [ ] | Primary_Coolant_Loop | `run_primary_coolant_loop` | `root-0/mfe_primary_loop.sysml:4` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Exchanger_Area_Conductance | `run_exchanger_area_conductance` | `root-0/integrated_equipment_costs.sysml:16` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Supplied_Source_Basis | `run_supplied_source_basis` | `root-0/whole_plant_conversion_accounts.sysml:141` | High |
| [ ] | Fuel_Inventory | `run_fuel_inventory` | `root-0/mfe_fuel_cycle.sysml:93` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Captured_Reactor_Offer | `run_captured_reactor_offer` | `root-0/whole_plant_conversion_accounts.sysml:14` | High |
| [ ] | Finite_Water_Cooler | `run_finite_water_cooler` | `root-0/component_alternatives_thermal.sysml:84` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Conditional_Cryogenic_Demand | `run_conditional_cryogenic_demand` | `root-0/whole_plant_conversion_accounts.sysml:56` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Cooling_Equipment_With_Selected_Salt_Pump_Count | `run_cooling_equipment_with_selected_salt_pump_count` | `root-0/cooling_equipment_selected_pumps.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Primary_Bypass_Control | `run_primary_bypass_control` | `root-0/loop_return_control.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Recuperator_Installed_Capability | `run_recuperator_installed_capability` | `root-0/component_alternatives_thermal.sysml:116` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Supplied_Primary_Capacity | `run_supplied_primary_capacity` | `root-0/whole_plant_conversion_accounts.sysml:127` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Eight_Amount_Sum | `run_eight_amount_sum` | `root-0/integrated_equipment_costs.sysml:80` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Scaled_Amount | `run_scaled_amount` | `root-0/integrated_equipment_costs.sysml:92` | High |
| [ ] | Fractional_Pressure_Loss | `run_fractional_pressure_loss` | `root-0/ideal_gas_brayton_components.sysml:52` | High |
| [ ] | Network_Heat_Driven_Closure | `run_network_heat_driven_closure` | `root-0/integrated_heat_electricity.sysml:112` | High |
| [ ] | Primary_Bypass_Control | `run_primary_bypass_control` | `root-0/loop_return_control.sysml:3` | High |
| [ ] | Controlled_Conversion_Boundary | `run_controlled_conversion_boundary` | `root-0/component_alternatives_thermal.sysml:124` | High |
| [ ] | Ideal_Gas_Expander | `run_ideal_gas_expander` | `root-0/ideal_gas_brayton_components.sysml:16` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Passive_Recuperator | `run_passive_recuperator` | `root-0/integrated_heat_electricity.sysml:185` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Finite_Water_Cooler | `run_finite_water_cooler` | `root-0/component_alternatives_thermal.sysml:84` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Actual_Exchanger_Approaches | `run_actual_exchanger_approaches` | `root-0/whole_plant_conversion_accounts.sysml:5` | High |
| [ ] | Finite_Water_Cooler | `run_finite_water_cooler` | `root-0/component_alternatives_thermal.sysml:84` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Controlled_Conversion_Boundary | `run_controlled_conversion_boundary` | `root-0/component_alternatives_thermal.sysml:124` | High |
| [ ] | Steam_Offered_Conditions | `run_steam_offered_conditions` | `root-0/mfe_viability.sysml:38` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Matched_Steam_Cycle | `run_matched_steam_cycle` | `root-0/mfe_matched_steam_cycle.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Controlled_Conversion_Boundary | `run_controlled_conversion_boundary` | `root-0/component_alternatives_thermal.sysml:124` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Pump_Pressure_Rise | `run_pump_pressure_rise` | `root-0/mfe_viability.sysml:92` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Temperature_Kelvin | `run_temperature_kelvin` | `root-0/whole_plant_conversion_accounts.sysml:173` | High |
| [ ] | Actual_Exchanger_Approaches | `run_actual_exchanger_approaches` | `root-0/whole_plant_conversion_accounts.sysml:5` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Cooling_Water_Rejection | `run_cooling_water_rejection` | `root-0/mfe_matched_steam_cycle.sysml:105` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Pump_Pressure_Rise | `run_pump_pressure_rise` | `root-0/mfe_viability.sysml:92` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Eight_Amount_Sum | `run_eight_amount_sum` | `root-0/integrated_equipment_costs.sysml:80` | High |
| [ ] | Eight_Amount_Sum | `run_eight_amount_sum` | `root-0/integrated_equipment_costs.sysml:80` | High |
| [ ] | Conversion_Subsystem_Ledger | `run_conversion_subsystem_ledger` | `root-0/component_alternatives_thermal.sysml:3` | High |
| [ ] | Whole_Plant_Operating_Ledger | `run_whole_plant_operating_ledger` | `root-0/whole_plant_conversion_accounts.sysml:321` | High |
| [ ] | Plant_Electrical_Balance | `run_plant_electrical_balance` | `root-0/integrated_heat_electricity.sysml:197` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Controlled_Conversion_Boundary | `run_controlled_conversion_boundary` | `root-0/component_alternatives_thermal.sysml:124` | High |
| [ ] | Cooling_Water_Rejection | `run_cooling_water_rejection` | `root-0/mfe_matched_steam_cycle.sysml:105` | High |
| [ ] | Conversion_Subsystem_Ledger | `run_conversion_subsystem_ledger` | `root-0/component_alternatives_thermal.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Whole_Plant_Operating_Ledger | `run_whole_plant_operating_ledger` | `root-0/whole_plant_conversion_accounts.sysml:321` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Fuel_Supply_Accounts | `run_fuel_supply_accounts` | `root-0/whole_plant_conversion_accounts.sysml:83` | High |
| [ ] | Whole_Plant_Capital_Accounts | `run_whole_plant_capital_accounts` | `root-0/whole_plant_conversion_accounts.sysml:178` | High |
| [ ] | Whole_Plant_Lifecycle_Ledger | `run_whole_plant_lifecycle_ledger` | `root-0/whole_plant_conversion_accounts.sysml:255` | High |
| [ ] | Whole_Plant_Capital_Accounts | `run_whole_plant_capital_accounts` | `root-0/whole_plant_conversion_accounts.sysml:178` | High |
| [ ] | Whole_Plant_Lifecycle_Ledger | `run_whole_plant_lifecycle_ledger` | `root-0/whole_plant_conversion_accounts.sysml:255` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright whole_plant_conversion_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 134 implementation functions
- Each function tested for: imports, signature, return type
- Tests tolerate NotImplementedError (pass before implementation)
- Tests verify return types (pass after implementation)

**Checklist**:
- [ ] Pyright passes (0 errors)
- [ ] Verification tests pass
- [ ] All implementations return correct types

**Note**: Import validation and ruff linting performed separately by maintainers.

---

## Stage 3: Integration Testing

**Objective**: Verify the full pipeline works end-to-end.

**Instructions**:
1. Create a test pipeline configuration in `whole_plant_conversion_tea/pipelines/`
2. Run the pipeline with sample inputs
3. Verify outputs match expected values from SysML models
4. Document any discrepancies and resolve

**Checklist**:
- [ ] Test pipeline created
- [ ] Pipeline runs without errors
- [ ] Outputs validated against SysML models
- [ ] All discrepancies resolved

---

## Completion Criteria

The implementation is complete when:
- Stage 1: All 134 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
