# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 130 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `stellarator_materials_nb3sn_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from stellarator_materials_nb3sn_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Blanket_Tritium_Breeding | `run_blanket_tritium_breeding` | `root-0/analyses/mfe_tritium_breeding.sysml:4` | High |
| [ ] | Supplied_Purchase_Cost | `run_supplied_purchase_cost` | `root-0/analyses/mfe_account_costs.sysml:17` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Purchase_Cost | `run_supplied_purchase_cost` | `root-0/analyses/mfe_account_costs.sysml:17` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Cryogenic_Offered_Conditions | `run_cryogenic_offered_conditions` | `root-0/analyses/mfe_viability.sysml:74` | High |
| [ ] | Supplied_Purchase_Cost | `run_supplied_purchase_cost` | `root-0/analyses/mfe_account_costs.sysml:17` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Winding_Pack_Casing_Fit | `run_winding_pack_casing_fit` | `root-0/analyses/mfe_winding_pack_fit.sysml:3` | High |
| [ ] | Winding_Operating_State | `run_winding_operating_state` | `root-0/analyses/mfe_magnet_field.sysml:4` | High |
| [ ] | Plasma_Sustainment | `run_plasma_sustainment` | `root-0/analyses/mfe_plasma_sustainment.sysml:4` | High |
| [ ] | DT_Fusion_Power | `run_dt_fusion_power` | `root-0/analyses/mfe_plasma_scaling.sysml:148` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Cooling_Scenario_Guard | `run_cooling_scenario_guard` | `root-0/analyses/mfe_cooling_accounts.sysml:4` | Medium |
| [ ] | Supplied_Purchase_Cost | `run_supplied_purchase_cost` | `root-0/analyses/mfe_account_costs.sysml:17` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Divertor_Heat_Ledger | `run_divertor_heat_ledger` | `root-0/analyses/mfe_divertor_heat.sysml:4` | High |
| [ ] | Primary_Coolant_Loop | `run_primary_coolant_loop` | `root-0/analyses/mfe_primary_loop.sysml:4` | High |
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/analyses/mfe_power_cycle.sysml:4` | High |
| [ ] | Cooling_Equipment | `run_cooling_equipment` | `root-0/analyses/mfe_cooling_equipment.sysml:3` | High |
| [ ] | Salt_Offered_Conditions | `run_salt_offered_conditions` | `root-0/analyses/mfe_viability.sysml:24` | High |
| [ ] | Salt_Machine_Electric | `run_salt_machine_electric` | `root-0/analyses/mfe_viability.sysml:99` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Matched_Steam_Cycle | `run_matched_steam_cycle` | `root-0/analyses/mfe_matched_steam_cycle.sysml:3` | High |
| [ ] | Pump_Pressure_Rise | `run_pump_pressure_rise` | `root-0/analyses/mfe_viability.sysml:92` | High |
| [ ] | Pump_Pressure_Rise | `run_pump_pressure_rise` | `root-0/analyses/mfe_viability.sysml:92` | High |
| [ ] | Steam_Offered_Conditions | `run_steam_offered_conditions` | `root-0/analyses/mfe_viability.sysml:38` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Cycle_Mode_Selection | `run_cycle_mode_selection` | `root-0/analyses/mfe_matched_steam_cycle.sysml:130` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Cooling_Water_Rejection | `run_cooling_water_rejection` | `root-0/analyses/mfe_matched_steam_cycle.sysml:105` | High |
| [ ] | Water_Offered_Conditions | `run_water_offered_conditions` | `root-0/analyses/mfe_viability.sysml:61` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Helium_Offered_Conditions | `run_helium_offered_conditions` | `root-0/analyses/mfe_viability.sysml:4` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Coil_Thermal_Inventory | `run_coil_thermal_inventory` | `root-0/analyses/mfe_cryo_inventory.sysml:3` | High |
| [ ] | Intercept_Electrical_Power | `run_intercept_electrical_power` | `root-0/analyses/mfe_cryo_inventory.sysml:89` | High |
| [ ] | Cryoplant_Electrical_Power | `run_cryoplant_electrical_power` | `root-0/analyses/mfe_cryo_plant.sysml:4` | High |
| [ ] | Magnet_Cold_Stage_Load | `run_magnet_cold_stage_load` | `root-0/analyses/magnet_conductor_alternatives.sysml:166` | High |
| [ ] | Staged_Refrigeration_Screen | `run_staged_refrigeration_screen` | `root-0/analyses/magnet_conductor_alternatives.sysml:203` | High |
| [ ] | Supplied_Auxiliary_Cooling_Cost | `run_supplied_auxiliary_cooling_cost` | `root-0/analyses/mfe_account_costs.sysml:33` | High |
| [ ] | Cold_Load_Watts | `run_cold_load_watts` | `root-0/analyses/mfe_viability.sysml:87` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Winding_Pack_Material_Inventory | `run_winding_pack_material_inventory` | `root-0/analyses/mfe_winding_pack_cost.sysml:4` | High |
| [ ] | Winding_Pack_Procurement_Cost | `run_winding_pack_procurement_cost` | `root-0/analyses/mfe_winding_pack_cost.sysml:42` | High |
| [ ] | Conductor_Peak_Field | `run_conductor_peak_field` | `root-0/analyses/mfe_plasma_scaling.sysml:420` | High |
| [ ] | Nb3Sn_Cable_Critical_Surface | `run_nb3sn_cable_critical_surface` | `root-0/analyses/magnet_conductor_alternatives.sysml:5` | High |
| [ ] | Winding_Inventory_and_Cost | `run_winding_inventory_and_cost` | `root-0/analyses/magnet_conductor_alternatives.sysml:132` | High |
| [ ] | REBCO_Conductor_Current | `run_rebco_conductor_current` | `root-0/analyses/mfe_conductor_current.sysml:3` | High |
| [ ] | Winding_Pack_Insulation_Inventory | `run_winding_pack_insulation_inventory` | `root-0/analyses/mfe_winding_pack_cost.sysml:70` | High |
| [ ] | Winding_Turn_Area_Screen | `run_winding_turn_area_screen` | `root-0/analyses/magnet_conductor_alternatives.sysml:97` | High |
| [ ] | Winding_Pack_Stress | `run_winding_pack_stress` | `root-0/analyses/mfe_magnet_field.sysml:60` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/analyses/mfe_viability.sysml:106` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Supplied_Cost_Class | `run_supplied_cost_class` | `root-0/analyses/mfe_account_costs.sysml:4` | High |
| [ ] | Lifecycle_Calendar | `run_lifecycle_calendar` | `root-0/analyses/mfe_lifecycle.sysml:4` | High |
| [ ] | Fuel_Inventory | `run_fuel_inventory` | `root-0/analyses/mfe_fuel_cycle.sysml:93` | High |
| [ ] | Fuel_Processing_Cost | `run_fuel_processing_cost` | `root-0/analyses/mfe_fuel_cycle.sysml:258` | High |
| [ ] | Facility_Layout | `run_facility_layout` | `root-0/analyses/mfe_facilities.sysml:3` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Facility_Civil_Cost | `run_facility_civil_cost` | `root-0/analyses/mfe_facilities.sysml:667` | Medium |
| [ ] | Tritium_Breeding_Adequacy | `run_tritium_breeding_adequacy` | `root-0/analyses/mfe_tritium_breeding.sysml:30` | High |
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:747` | High |
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:747` | High |
| [ ] | Facility_Shipping_Scope | `run_facility_shipping_scope` | `root-0/analyses/mfe_facilities.sysml:690` | Medium |
| [ ] | IDC_Closed_Form_Cost | `run_idc_closed_form_cost` | `root-0/analyses/mfe_account_costs.sysml:712` | High |
| [ ] | LCOE_DCF | `run_lcoe_dcf` | `root-0/analyses/mfe_lcoe_dcf.sysml:4` | High |

**20 computed attribute module(s) auto-implemented** (not included in manual count above).

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright stellarator_materials_nb3sn_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 130 implementation functions
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
1. Create a test pipeline configuration in `stellarator_materials_nb3sn_tea/pipelines/`
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
- Stage 1: All 130 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
