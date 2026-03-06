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
| SV-001 | All 14 Hawker parameters present with metadata | rollup | model | 14 attributes, each with unit + range + default + sensitivity | exact count | WI-006 spec MR-WI006-1 | model inspection | passing |
| SV-002 | CAS hierarchy covers IFE-relevant level 2 accounts | rollup | model | CAS20-27, 91-99 present with classification | all accounts | WI-006 spec MR-WI006-2 | model inspection | passing |
| SV-003 | LCOE calc dimensional consistency | physical | model | Output units resolve to $/MWh | dimensional | WI-006 spec MR-WI006-3 | model inspection | passing |
| SV-004 | Fusion cycle gain constraint evaluable | physical | model | eta*G threshold expressed as constraint | present | WI-006 spec MR-WI006-4 | model inspection | passing |
| SV-005 | Library files parse cleanly | baseline | model | `syside check` returns 0 errors | 0 errors | WI-006 spec MR-WI006-9 | `uv run syside check` | passing |
| SV-006 | Generic IFE plant has all required subsystems | rollup | model | Driver, target factory, chamber subsystems present with CAS mapping | all subsystems | WI-007 spec MR-WI007-1 | model inspection | passing |
| SV-007 | CAS22 level 3 sub-accounts present for IFE | rollup | model | 22.1.1, 22.1.2, 22.1.3, 22.1.5, 22.1.8 present with scope | all accounts | WI-007 spec MR-WI007-5 | model inspection | passing |
| SV-008 | LCOE with realistic parameters within Hawker range | reasonableness | test | $25–120/MWh with HIF design point params | order of magnitude | WI-007 spec MR-WI007-7 | `scripts/verify_ife_lcoe.py` | passing |
| SV-009 | Driver interface is abstract with 4 required parameters | baseline | model | eta, gamma, E_d, N_d as typed attributes | exact count | WI-007 spec MR-WI007-2 | model inspection | passing |
| SV-010 | Design files parse cleanly | baseline | model | `syside check` returns 0 errors | 0 errors | WI-007 spec MR-WI007-13 | `uv run syside check` | passing |
| SV-011 | HIF Driver concrete with 4 params set from sources | baseline | model | HIF Driver specializes IFE Driver, all 4 attributes have values with citations | exact | WI-008 spec MR-WI008-1 | model inspection | passing |
| SV-012 | Meier driver cost formula produces expected output | baseline | test | C_dd ≈ $1.0B at E_d=5 MJ, N_c=1, v=5 Hz | ±10% | WI-008 spec MR-WI008-2 | `scripts/verify_hif_costs.py` | passing |
| SV-013 | Hawker LCOE with HIF params is finite and positive | reasonableness | test | Positive LCOE value with HIF design point parameters | finite positive | WI-008 spec MR-WI008-4 | `scripts/verify_hif_costs.py` | passing |
| SV-014 | Meier COE at reference case matches published value | baseline | test | COE ≈ 5.0 cents/kWh at 1.0 GWe (Meier 1986, 1988$) | ±15% | WI-008 spec MR-WI008-3 | `scripts/verify_hif_costs.py` | passing |
| SV-015 | HIF design files parse cleanly | baseline | model | `syside check` returns 0 errors | 0 errors | WI-008 spec MR-WI008-11 | `uv run syside check` | passing |
