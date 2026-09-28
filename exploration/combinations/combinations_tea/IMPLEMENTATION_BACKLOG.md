# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 59 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `combinations_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from combinations_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/mfe_power_cycle.sysml:4` | High |
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/mfe_power_cycle.sysml:4` | High |
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/mfe_power_cycle.sysml:4` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Selected_Inventory_Purchase | `run_selected_inventory_purchase` | `root-0/integrated_equipment_costs.sysml:3` | High |
| [ ] | Selected_Stock_Atoms | `run_selected_stock_atoms` | `root-0/integrated_equipment_costs.sysml:37` | High |
| [ ] | Exchanger_Area_Conductance | `run_exchanger_area_conductance` | `root-0/integrated_equipment_costs.sysml:16` | High |
| [ ] | Selected_Flow_Pump | `run_selected_flow_pump` | `root-0/integrated_equipment_costs.sysml:23` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Selected_Flow_Pump | `run_selected_flow_pump` | `root-0/integrated_equipment_costs.sysml:23` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Exchanger_Area_Conductance | `run_exchanger_area_conductance` | `root-0/integrated_equipment_costs.sysml:16` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Plasma_Sustainment | `run_plasma_sustainment` | `root-0/mfe_plasma_sustainment.sysml:4` | High |
| [ ] | DT_Fusion_Power | `run_dt_fusion_power` | `root-0/mfe_plasma_scaling.sysml:148` | High |
| [ ] | Fusion_Source_Selector | `run_fusion_source_selector` | `root-0/integrated_heat_electricity.sysml:3` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fractional_Pressure_Loss | `run_fractional_pressure_loss` | `root-0/ideal_gas_brayton_components.sysml:52` | High |
| [ ] | Exchanger_Area_Conductance | `run_exchanger_area_conductance` | `root-0/integrated_equipment_costs.sysml:16` | High |
| [ ] | Selected_Flow_Pump | `run_selected_flow_pump` | `root-0/integrated_equipment_costs.sysml:23` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Integrated_Heat_Source | `run_integrated_heat_source` | `root-0/integrated_heat_electricity.sysml:11` | High |
| [ ] | Coolant_Branch_Heat | `run_coolant_branch_heat` | `root-0/dual_circuit_heat_accounting.sysml:4` | High |
| [ ] | Coolant_Branch_Heat | `run_coolant_branch_heat` | `root-0/dual_circuit_heat_accounting.sysml:4` | High |
| [ ] | Coolant_Branch_Heat | `run_coolant_branch_heat` | `root-0/dual_circuit_heat_accounting.sysml:4` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Network_Heat_Driven_Closure | `run_network_heat_driven_closure` | `root-0/integrated_heat_electricity.sysml:112` | High |
| [ ] | Ideal_Gas_Expander | `run_ideal_gas_expander` | `root-0/ideal_gas_brayton_components.sysml:16` | High |
| [ ] | Plant_Electrical_Balance | `run_plant_electrical_balance` | `root-0/integrated_heat_electricity.sysml:197` | High |
| [ ] | Passive_Recuperator | `run_passive_recuperator` | `root-0/integrated_heat_electricity.sysml:185` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Exchanger_Area_Conductance | `run_exchanger_area_conductance` | `root-0/integrated_equipment_costs.sysml:16` | High |
| [ ] | Primary_Coolant_Loop | `run_primary_coolant_loop` | `root-0/mfe_primary_loop.sysml:4` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fractional_Pressure_Loss | `run_fractional_pressure_loss` | `root-0/ideal_gas_brayton_components.sysml:52` | High |
| [ ] | Network_Heat_Driven_Closure | `run_network_heat_driven_closure` | `root-0/integrated_heat_electricity.sysml:112` | High |
| [ ] | Ideal_Gas_Expander | `run_ideal_gas_expander` | `root-0/ideal_gas_brayton_components.sysml:16` | High |
| [ ] | Passive_Recuperator | `run_passive_recuperator` | `root-0/integrated_heat_electricity.sysml:185` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Plant_Electrical_Balance | `run_plant_electrical_balance` | `root-0/integrated_heat_electricity.sysml:197` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |

**2 computed attribute module(s) auto-implemented** (not included in manual count above).

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright combinations_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 59 implementation functions
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
1. Create a test pipeline configuration in `combinations_tea/pipelines/`
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
- Stage 1: All 59 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
