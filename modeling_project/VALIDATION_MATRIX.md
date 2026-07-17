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
| SV-016 | MFE power balance produces net electric, engineering Q, and recirc fraction at a reference design point | reasonableness | test | net electric > 0, Q_eng in ~10-40 for a reference MFE point | order of magnitude | WI-009 spec MR-WI009-1 | model inspection / verify script | pending |
| SV-017 | Fusion power scaling increases with B and R | relationship | test | d(P_fus)/dB > 0 and d(P_fus)/dR > 0 | monotonic direction | WI-009 spec MR-WI009-2 | verify script | pending |
| SV-018 | Magnet cost scaling increases with B and R | relationship | test | d(cost)/dB > 0 and d(cost)/dR > 0 | monotonic direction | WI-009 spec MR-WI009-3 | verify script | pending |
| SV-019 | MFE viability constraint evaluable (net electric > 0 / Q_eng > 1) | physical | model | constraint evaluates true/false correctly | present | WI-009 spec MR-WI009-5 | model inspection | passing |
| SV-020 | CAS Scope has mfe_divergent member and IFE models still parse | baseline | model | 3 enum members; IFE library+design parse clean | 0 errors | WI-009 spec MR-WI009-6 | uv run syside check | passing |
| SV-021 | MFE library files parse cleanly | baseline | model | syside check returns 0 errors | 0 errors | WI-009 spec MR-WI009-11 | uv run syside check | passing |
| SV-022 | Magnet System specialization chain resolves to Costed Component via CAS22.1.3 | baseline | model | Magnet System -> CAS22.1.3 -> CAS22 Power Core -> CAS Account -> Costed Component | exact | WI-009 spec MR-WI009-4 | model inspection | passing |
| SV-023 | Generated IFE pipeline (live syside extraction -> sysml-codegen -> teax executor) reproduces the verified Hawker LCOE anchors: $252.30/MWh at Hawker defaults, $68.69/MWh at the realistic HIF point (f=5 Hz, eta=0.25), $270.12/MWh at the Osiris hif_plant point, plus Meier gamma $68.247/J and Meier COE 4.74 c/kWh. Oracle: scripts/verify_ife_lcoe.py; harness: exploration/ife_e2e/run_anchors.py | reasonableness | model | LCOE 252.30 / 68.69 / 270.12 $/MWh at the three WI-015 anchor points | relative 1e-6 (flat float arithmetic; observed exact to 9 decimals) |  |  | passing |
| SV-024 | MFE plant wiring constructs validate and survive extraction: cross-calc usage binding (in x = calc.ret), part-level assert constraint, and subsystem capital_cost redefinition from a calc output | baseline | model | L6_INVALID_BINDING_FORMAT=0, L6_CONSTRAINT_INELIGIBLE=0, L6_ATTR_REDEF_EXPR_DROPPED=0 | exact |  |  | passing |
| SV-025 | Faithful MFE power balance reproduces the 1costingFE power table at the Anchor A handshake point when fed 1costingFE's own inputs (formula isolation): p_th 2819.07, p_the/p_et 1127.63, p_net 1000.0 MW, q_eng 8.835 | baseline | test | all six power channels match 1costingFE | relative 1e-5 (reference table is JAX float32, ~1e-7 floor) | WI-019 spec MR-WI019-1/2/3 | exploration/stellarator_e2e/handshake_1costingfe.py | passing |
| SV-026 | End-to-end handshake gap collapses after the power-balance fix: every power-scaled account (C220101/102/105/106/107/108, CAS23/24/25/26) deviation shrinks from −8.6…−16.4% to ≤0.1%, leaving only documented structural gaps | baseline | test | power-scaled account rel dev ≤ 0.1% end-to-end | 0.1% relative | WI-019 spec success criterion 2 | exploration/stellarator_e2e/handshake_1costingfe.py | passing |
