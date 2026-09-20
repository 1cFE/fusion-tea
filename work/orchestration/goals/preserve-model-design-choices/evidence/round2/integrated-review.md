---
Verdict: concerns
Created: 2026-09-20
Related Artifacts:
  Architecture: ./architecture-review.md
  Thermal Contract: ../../../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json
---

# Round 2 independent integrated review

**PENDING final native evidence.** The inspected source and seed implementation follow the released MR-7 architecture. No material source-binding defect was found. The auxiliary-cost output-order correction and incremental native acceptance are now reviewed below. Final package identity and broad validation evidence remain pending.

## Source and interface assessment

- **Chosen procurement survives evaluation.** Five equipment accounts consume independently supplied package amounts. Material accounts and broad allowances consume guarded supplied classes. Electric capacity and its linear price share the same supplied gross-MWe owner. Legacy facility/cooling/fuel/preconstruction paths also use supplied classes. Blanket/divertor replacement unit cost still reads their selected capital amounts; operating replacement timing remains separate. Checked the actual account usages in `mfe_subsystems.sysml`, `mfe_plant.sysml`, `mfe_plant_systems.sysml` and `mfe_power_core.sysml`, rather than relying on their names.
- **Capability checks use actual demands.** An independent scripted source comparison found no discrepancy across all 32 screen definitions' five bindings or their native assertion operands against the declared contract. Inspected ownership and units for turbine children, water rejection, cryogenic stages and helium/salt machines. The IHX assertion consumes the existing per-exchanger area margin. None of these comparisons increases offered equipment to meet demand.
- **Conditions and definedness remain explicit.** The seeds implement finite point-state comparison with fixed eight-ULP numerical identity, primary/secondary mode applicability, strict unsnapped capacity margins and unavailable-UA/intercept guards. Fixed-purpose conversion definitions replace editable scale/offset controls. Forty generated Boolean controls can withhold credit only; the independent oracle carries the same administrative masks separately from physical offers. Inactive/unsupported results are distinguishable through outputs even when the aggregate predicate reports violation.
- **Physical propagation is retained in source.** Operating heating remains distinct from installed heating. The blanket-to-primary-to-steam-to-rejection bindings, breeding requirement operands and divertor heat-flux comparison were not replaced by the new procurement inputs. This establishes wiring, not the outstanding executed propagation evidence.
- **Interface changes are explicit.** The ledger declares 118 additions and 11 removals from 597 inputs, yielding 704. It declares 203 added numeric outputs and 33 added predicates, yielding 1352 and 67. Retired fields are price-estimate inputs; operating channels remain. Reviewed oracle procurement formulas, screen mapping and the regression adapter's declared cost-descendant treatment. Exact regenerated membership and full regressions remain acceptance evidence.

The corrected auxiliary-cost seed maps named amounts through the generated schema field order. That addresses the observed auxiliary/total swap in principle; its regenerated runtime result must establish the fix. Package records label captured amounts and ratings as assumptions, not vendor quotations or qualified machinery. Multi-module package evaluation is expressly rejected.

## Incremental native acceptance reviewed

The [six-case propagation record](../../../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/propagation-acceptance.json) and its [test](../../../../../../tests/models/test_supplied_equipment_propagation.py) close the earlier demand-propagation gaps. Density perturbations change primary flow/work, IHX requirement, salt flow/work, steam flow/power/UA and rejection flow/work while installed area, selected package costs, cooling spares and replacement purchase provision stay fixed. Heating, breeding and divertor operands and verdicts are compared independently. Shifted helium point conditions remain unsupported; supported salt/steam/water screens can fail as loads rise.

Increased support heat changes cold/intercept loads and produces negative margins at fixed refrigeration purchase price. Separate cold and shield operating-COP perturbations increase electricity without changing thermal demand, capacity margins or price. These are actual native scenarios, not inference from declarations.

Reviewed the native residual-cost tests covering turbine replacement offers, divertor price propagation into replacement unit cost/PV without rescheduling, the actual auxiliary module's three named outputs, and simultaneous legacy facilities/cooling/fuel routes under changed density. The coordinator reports 38 passing cost tests; final evidence must bind that result to the accepted package.

The [numerical-identity record](../../../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/numerical-identity.md) is consistent with inspected native and independent cooling-water equations. Independent shaft-work division now follows the native equation's operation order. Baseline water-electric margin remains `-3.552713678800501e-15` and fails in both implementations; neither rating nor capacity predicate was changed. The eight-ULP rule remains confined to state identity.

## Consumer migration assessment

The adapter composes explicit sequential interface ledgers, not observed generated membership. Its 54 changed existing channels and 59 local names are restricted to documented procurement descendants; the extra five names are aliases. Exact partition membership and unchanged historical values remain asserted. Changed/new native values are compared with independently computed current equations at the same replay inputs. Frozen artifacts remain the baseline for unchanged physics.

The coil-thermal replay test replaces only declared changed economic expectations with native values and compares them to the independent oracle's result under identical replay controls. This is a cross-implementation check, not a comparison of native output with itself. The migration does not independently validate empirical price laws, and the review claims no such validation. Boolean masks are explicit administrative inputs; exact Boolean interface membership remains a contract check.

The previously noted turbine behavioral comment is corrected. No material implementation finding remains from these incremental checks.

## Current interface coverage and residual dispositions

Independently recomputed every direct input-to-consumer edge from the current pipeline: all 704 unique input rows match their declared 1,121 edges, with no discrepancy. All seven source hashes in the [coverage record](../../../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/current-interface-coverage.json) match the inspected files. Its 118 additions and 11 retirements exactly match the reviewed interface ledger, leaving 586 retained inputs. The role split is 49 physical offer fields, 27 procurement fields, 40 administrative masks and two restricted single-module formals.

The [current residual dispositions](../../../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/residual-dispositions.md) correctly distinguish consumed inputs from scientific validity. Revised R09–R12/R14 meanings identify supplied prices, conditional capacity screens and retained operating dependencies. Vacuum equipment, maintained fuel-stock policy, source-domain limits and missing equipment qualification remain explicit. The prior WI-074 record retains its contents with a historical/current pointer; no inherited conclusion becomes owner-originated authority.

The current oracle IHX predicate map now names `margin_m2_in`, matching the actual native formal. The coordinator reports agreement for all 67 baseline predicates. Stock-route stale-name/census repairs and broad-suite completion still require their final receipts below.

## Remaining final gate

Provide the final package/checkpoint identity, completed native offer/state tests, broad regression results, stock study-route results and required integration evidence. Confirm the deposited acceptance records apply to that package. Until then, final native/integration MR-7 compliance remains **unverified**. This reviewer did not rerun full tests or open reference material/comparisons.
