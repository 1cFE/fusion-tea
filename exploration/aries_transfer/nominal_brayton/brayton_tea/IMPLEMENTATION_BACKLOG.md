# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 14 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `brayton_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from brayton_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Ideal_Gas_Compressor | `run_ideal_gas_compressor` | `root-0/ideal_gas_brayton_components.sysml:3` | High |
| [ ] | Fractional_Pressure_Loss | `run_fractional_pressure_loss` | `root-0/ideal_gas_brayton_components.sysml:52` | High |
| [ ] | Ideal_Gas_Expander | `run_ideal_gas_expander` | `root-0/ideal_gas_brayton_components.sysml:16` | High |
| [ ] | Equal_Capacity_Recuperator | `run_equal_capacity_recuperator` | `root-0/ideal_gas_brayton_components.sysml:41` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Fixed_Outlet_Conditioning | `run_fixed_outlet_conditioning` | `root-0/ideal_gas_brayton_components.sysml:29` | High |
| [ ] | Brayton_Cycle_Ledger | `run_brayton_cycle_ledger` | `root-0/ideal_gas_brayton_components.sysml:58` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |
| [ ] | Offered_Capacity_Screen | `run_offered_capacity_screen` | `root-0/mfe_viability.sysml:106` | High |

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright brayton_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 14 implementation functions
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
1. Create a test pipeline configuration in `brayton_tea/pipelines/`
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
- Stage 1: All 14 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
