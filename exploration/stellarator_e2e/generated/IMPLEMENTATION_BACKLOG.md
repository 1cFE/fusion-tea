# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 12 functions to implement

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
| [ ] | Winding_Pack_Sizing | `run_winding_pack_sizing` | `root-0/analyses/mfe_magnet_field.sysml:91` | High |
| [ ] | Conductor_Peak_Field | `run_conductor_peak_field` | `root-0/analyses/mfe_plasma_scaling.sysml:419` | High |
| [ ] | Winding_Pack_Stress | `run_winding_pack_stress` | `root-0/analyses/mfe_magnet_field.sysml:48` | High |
| [ ] | Plasma_Sustainment | `run_plasma_sustainment` | `root-0/analyses/mfe_plasma_sustainment.sysml:4` | High |
| [ ] | DT_Fusion_Power | `run_dt_fusion_power` | `root-0/analyses/mfe_plasma_scaling.sysml:147` | High |
| [ ] | Cryoplant_Electrical_Power | `run_cryoplant_electrical_power` | `root-0/analyses/mfe_cryo_plant.sysml:4` | High |
| [ ] | Power_Cycle_Efficiency | `run_power_cycle_efficiency` | `root-0/analyses/mfe_power_cycle.sysml:4` | High |
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:680` | High |
| [ ] | Lifecycle_Calendar | `run_lifecycle_calendar` | `root-0/analyses/mfe_lifecycle.sysml:4` | High |
| [ ] | Levelized_Annual_Cost | `run_levelized_annual_cost` | `root-0/analyses/mfe_account_costs.sysml:680` | High |
| [ ] | IDC_Closed_Form_Cost | `run_idc_closed_form_cost` | `root-0/analyses/mfe_account_costs.sysml:645` | High |
| [ ] | LCOE_DCF | `run_lcoe_dcf` | `root-0/analyses/mfe_lcoe_dcf.sysml:4` | High |

**11 computed attribute module(s) auto-implemented** (not included in manual count above).

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
- 12 implementation functions
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
- Stage 1: All 12 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
