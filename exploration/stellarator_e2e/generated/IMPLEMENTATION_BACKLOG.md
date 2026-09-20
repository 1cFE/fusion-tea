# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 57 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `stellarator_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from stellarator_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | Blanket_Tritium_Breeding | `run_blanket_tritium_breeding` | `root-0/analyses/mfe_tritium_breeding.sysml:4` | High |
| [ ] | Winding_Pack_Casing_Fit | `run_winding_pack_casing_fit` | `root-0/analyses/mfe_winding_pack_fit.sysml:3` | High |
| [ ] | Winding_Operating_State | `run_winding_operating_state` | `root-0/analyses/mfe_magnet_field.sysml:4` | High |
| [ ] | Plasma_Sustainment | `run_plasma_sustainment` | `root-0/analyses/mfe_plasma_sustainment.sysml:4` | High |
| [ ] | DT_Fusion_Power | `run_dt_fusion_power` | `root-0/analyses/mfe_plasma_scaling.sysml:148` | High |
| [ ] | Cooling_Scenario_Guard | `run_cooling_scenario_guard` | `root-0/analyses/mfe_cooling_accounts.sysml:4` | Medium |
| [ ] | Divertor_Heat_Ledger | `run_divertor_heat_ledger` | `root-0/analyses/mfe_divertor_heat.sysml:4` | High |
| [ ] | Primary_Coolant_Loop | `run_primary_coolant_loop` | `root-0/analyses/mfe_primary_loop.sysml:4` | High |
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/analyses/mfe_power_cycle.sysml:4` | High |
| [ ] | Cooling_Equipment | `run_cooling_equipment` | `root-0/analyses/mfe_cooling_equipment.sysml:3` | High |
| [ ] | Matched_Steam_Cycle | `run_matched_steam_cycle` | `root-0/analyses/mfe_matched_steam_cycle.sysml:3` | High |
| [ ] | Cycle_Mode_Selection | `run_cycle_mode_selection` | `root-0/analyses/mfe_matched_steam_cycle.sysml:130` | High |
| [ ] | Cooling_Water_Rejection | `run_cooling_water_rejection` | `root-0/analyses/mfe_matched_steam_cycle.sysml:105` | High |
| [ ] | Coil_Thermal_Inventory | `run_coil_thermal_inventory` | `root-0/analyses/mfe_cryo_inventory.sysml:3` | High |
| [ ] | Intercept_Electrical_Power | `run_intercept_electrical_power` | `root-0/analyses/mfe_cryo_inventory.sysml:89` | High |
| [ ] | Cryoplant_Electrical_Power | `run_cryoplant_electrical_power` | `root-0/analyses/mfe_cryo_plant.sysml:4` | High |
| [ ] | Winding_Pack_Material_Inventory | `run_winding_pack_material_inventory` | `root-0/analyses/mfe_winding_pack_cost.sysml:4` | High |
| [ ] | Winding_Pack_Procurement_Cost | `run_winding_pack_procurement_cost` | `root-0/analyses/mfe_winding_pack_cost.sysml:42` | High |
| [ ] | Conductor_Peak_Field | `run_conductor_peak_field` | `root-0/analyses/mfe_plasma_scaling.sysml:420` | High |
| [ ] | REBCO_Conductor_Current | `run_rebco_conductor_current` | `root-0/analyses/mfe_conductor_current.sysml:3` | High |
| [ ] | Winding_Pack_Insulation_Inventory | `run_winding_pack_insulation_inventory` | `root-0/analyses/mfe_winding_pack_cost.sysml:70` | High |
| [ ] | Winding_Pack_Stress | `run_winding_pack_stress` | `root-0/analyses/mfe_magnet_field.sysml:60` | High |
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
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:694` | High |
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:694` | High |
| [ ] | Facility_Shipping_Scope | `run_facility_shipping_scope` | `root-0/analyses/mfe_facilities.sysml:690` | Medium |
| [ ] | IDC_Closed_Form_Cost | `run_idc_closed_form_cost` | `root-0/analyses/mfe_account_costs.sysml:659` | High |
| [ ] | LCOE_DCF | `run_lcoe_dcf` | `root-0/analyses/mfe_lcoe_dcf.sysml:4` | High |

**15 computed attribute module(s) auto-implemented** (not included in manual count above).

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright stellarator_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 57 implementation functions
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
1. Create a test pipeline configuration in `stellarator_tea/pipelines/`
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
- Stage 1: All 57 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
