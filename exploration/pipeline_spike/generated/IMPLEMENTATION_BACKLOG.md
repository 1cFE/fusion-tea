# Implementation Backlog

This document tracks the implementation of SysML calculation definitions.
Complete all stages in order for a production-ready system.

---

## Stage 1: Implement Calculation Functions

**Objective**: Implement each calculation definition in its handwritten file.

**Total**: 15 functions to implement

**Instructions for each function**:
1. Open the SysML source file at the line number shown below
2. Review the calculation expressions and constraints in SysML
3. Open the corresponding `*_impl.py` file in `solar_battery_tea/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from solar_battery_tea.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | EnergyProductionCalc | `run_energyproductioncalc` | `library.sysml:267` | High |
| [ ] | AnnualizedFuelCalc | `run_annualizedfuelcalc` | `library.sysml:298` | High |
| [ ] | PVModuleCostCalc | `run_pvmodulecostcalc` | `library.sysml:27` | Medium |
| [ ] | InverterCostCalc | `run_invertercostcalc` | `library.sysml:50` | Medium |
| [ ] | ArrayBOSCostCalc | `run_arrayboscostcalc` | `library.sysml:72` | High |
| [ ] | BatteryPackCostCalc | `run_batterypackcostcalc` | `library.sysml:96` | Medium |
| [ ] | HybridInverterCostCalc | `run_hybridinvertercostcalc` | `library.sysml:119` | Medium |
| [ ] | BatteryBOSCostCalc | `run_batteryboscostcalc` | `library.sysml:141` | High |
| [ ] | RackingCostCalc | `run_rackingcostcalc` | `library.sysml:163` | Medium |
| [ ] | ElectricalPanelCostCalc | `run_electricalpanelcostcalc` | `library.sysml:187` | High |
| [ ] | PermittingCostCalc | `run_permittingcostcalc` | `library.sysml:210` | Medium |
| [ ] | AllocationCostCalc | `run_allocationcostcalc` | `library.sysml:235` | High |
| [ ] | AnnualizedOMCalc | `run_annualizedomcalc` | `library.sysml:283` | High |
| [ ] | AnnualizedFinancialCalc | `run_annualizedfinancialcalc` | `library.sysml:314` | High |
| [ ] | LCOECalc | `run_lcoecalc` | `library.sysml:335` | High |

**1 computed attribute module(s) auto-implemented** (not included in manual count above).

**20 aggregation module(s) auto-implemented** (not included in manual count above).

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright solar_battery_tea/
```
Expected: 0 errors (should stay clean during implementation)

### 2.2 Implementation Tests
Run verification tests:
```bash
pytest tests/test_implementations_runnable.py -v
```
All tests should pass (or pytest.skip for NotImplementedError stubs)

**Test Coverage**:
- 15 implementation functions
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
1. Create a test pipeline configuration in `solar_battery_tea/pipelines/`
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
- Stage 1: All 15 functions implemented
- Stage 2: All validations pass
- Stage 3: Integration tests pass

**Next Steps**: Deploy to production environment or integrate with larger system.
