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
3. Open the corresponding `*_impl.py` file in `solar_battery/handwritten/`
4. Replace `raise NotImplementedError(...)` with actual calculation logic
5. Ensure the function returns correct type (single float or tuple of floats)
6. Test: `python -c "from solar_battery.modules.<module> import <Module>"`

**Complexity Guide**:
- **Low**: Simple arithmetic (1-5 operations)
- **Medium**: Multiple terms, some conditional logic (6-15 operations)
- **High**: Complex logic, loops, or external dependencies (15+ operations)

| Status | Module | Function | SysML Source | Complexity |
|--------|--------|----------|--------------|------------|
| [ ] | PVModuleCostCalc | `run_pvmodulecostcalc` | `models/tests/solar_battery/library.sysml:27` | Medium |
| [ ] | InverterCostCalc | `run_invertercostcalc` | `models/tests/solar_battery/library.sysml:50` | Medium |
| [ ] | ArrayBOSCostCalc | `run_arrayboscostcalc` | `models/tests/solar_battery/library.sysml:72` | High |
| [ ] | BatteryPackCostCalc | `run_batterypackcostcalc` | `models/tests/solar_battery/library.sysml:96` | Medium |
| [ ] | HybridInverterCostCalc | `run_hybridinvertercostcalc` | `models/tests/solar_battery/library.sysml:119` | Medium |
| [ ] | BatteryBOSCostCalc | `run_batteryboscostcalc` | `models/tests/solar_battery/library.sysml:141` | High |
| [ ] | RackingCostCalc | `run_rackingcostcalc` | `models/tests/solar_battery/library.sysml:163` | Medium |
| [ ] | ElectricalPanelCostCalc | `run_electricalpanelcostcalc` | `models/tests/solar_battery/library.sysml:187` | High |
| [ ] | PermittingCostCalc | `run_permittingcostcalc` | `models/tests/solar_battery/library.sysml:210` | Medium |
| [ ] | AllocationCostCalc | `run_allocationcostcalc` | `models/tests/solar_battery/library.sysml:235` | High |
| [ ] | EnergyProductionCalc | `run_energyproductioncalc` | `models/tests/solar_battery/library.sysml:267` | High |
| [ ] | AnnualizedOMCalc | `run_annualizedomcalc` | `models/tests/solar_battery/library.sysml:283` | High |
| [ ] | AnnualizedFuelCalc | `run_annualizedfuelcalc` | `models/tests/solar_battery/library.sysml:298` | High |
| [ ] | AnnualizedFinancialCalc | `run_annualizedfinancialcalc` | `models/tests/solar_battery/library.sysml:314` | High |
| [ ] | LCOECalc | `run_lcoecalc` | `models/tests/solar_battery/library.sysml:335` | High |

---

## Stage 2: Verification

**Objective**: Verify implementations work correctly.

**Instructions**:

### 2.1 Type Checking
Run pyright to catch typing errors:
```bash
pyright solar_battery/
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
1. Create a test pipeline configuration in `solar_battery/pipelines/`
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
