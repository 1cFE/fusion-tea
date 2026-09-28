---
Verdict: pass
Created: 2026-09-20
Related Artifacts:
  Cost: ./cost-contract-proposal.md
  Thermal: ./thermal-contract-proposal.md
  Refinement: ./package-contract-refinement.md
  Propagation: ./propagation-contract.md
  Brief: ./review-brief.md
---

# Round 2 independent architecture review

**PASS for implementation of the resolved contract below.** The initial disconnected-price finding is resolved by the [package refinement](package-contract-refinement.md) and the [cost proposal's selected-amount mechanism](cost-contract-proposal.md#selected-package-amounts-where-the-cost-law-does-not-price-the-specification). These supersede conflicting live-class pricing alternatives in the earlier proposal sections. No OWNER_GATE is necessary for this conditional evaluation architecture. Implementation and numerical defaults remain unverified.

## Released contract

- **Selected packages:** turbine, heat rejection, cryoplant, power supplies and divertor own their offered specification, declared conditions and `selected_package_cost`. Capital consumes the supplied dollar amount. Turbine and heat-rejection totals multiply the per-module amount by `n_mod` once; other accounts preserve their existing aggregation scope. Cryogenic auxiliary-cooling allowance stays separate. Replacement unit costs and downstream rollups consume the selected amount wherever applicable. A versioned package record supplies scope, currency convention, checkpoint and assumption/quote provenance. A captured estimate is an assumption, never a vendor quotation.
- **Retained formulas:** electric plant may retain its linear supplied gross-MWe rating law because that matches its single represented capacity dimension. Geometry-priced blanket/shield/structure/vessel and explicitly limited budget accounts may retain independent procurement-class formulas. Legacy facilities, cooling, preconstruction and fuel paths receive independent cost classes too. No operating-power fallback is permitted. Existing helium/salt purchase laws remain accepted; added offered specifications do not imply a newly predicted marginal price.
- **Estimate helpers:** package correlations may estimate amounts outside evaluation on declared independent design inputs. Neither cost nor ratings may be regenerated from demand. The cryogenic stage-to-electric equation matches existing Carnot arithmetic but is only an optional conditional estimate helper. Heat-rejection total-MWth coefficients cannot price rejected MW, and gross-MWe coefficients cannot price converter MW. All price-model source limits survive.
- **Physical screens:** implement the thermal proposal's producer/consumer table, preserving per-machine/per-IHX units and actual balances. Compare every applicable supplied dimension with its demand and expose signed margins. Check declared conditions from actual operating inputs; a caller-supplied success flag is insufficient. Point ratings apply only at their declared state unless an explicit assumed envelope is supplied. Unsupported or inactive cases retain separate applicability/definedness and cannot receive affirmative physical adequacy. Existing qualification flags remain false.

## Findings closed and remaining acceptance

Disconnected class/capacity knobs become a declared offered package, including its price. Rating-only changes at fixed price are hypothetical offers, not evidence of free upgrades. Test replacement offers with changed supplied amounts and verify account/rollup propagation. Separately vary demand with every package field fixed. Preserve operating consumption and load-dependent replacement timing.

The omitted IHX native verdict is approved for promotion from the [existing area calculation](../../../../../../exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py:63), retaining its U/temperature assumptions and invalid-state rejection. Test insufficient/sufficient supplied assemblies and fixed assembly under changed heat.

Native acceptance must cover every new dimension, equality, invalid ratings, legacy/disabled modes, condition mismatch, public input preservation and full assertion inventory. Verify captured defaults against exact native outputs and document retired price-helper inputs. Keep existing module-count inconsistencies explicit rather than silently repairing them.

## Evidence and limits

Inspected MR-7, review process, owner extension, both specs, all four proposals, current account and thermal bindings, cooling executable, cryogenic equations, native verdict inventory and original pre-reveal costing functions. Verified heating propagation, blanket-to-conversion/rejection bindings, breeding operands and divertor flux comparison. No new empirical physics is approved. Broad allowances and omitted equipment remain limited claims; their disclosure does not establish adequacy. No runtime tests or numeric capture verification performed; no quarantined material opened. MR-7 design contract is compliant; implemented/native compliance remains **unverified** until acceptance.

## Implementation correction review — 2026-09-20

**PASS for the proposed corrections; implementation verification remains pending.** Inspected current viability definitions and owning bindings, the capability seed record, oracle contract, existing loop/secondary energy selection, and the initial scratch handwritten modules under `/tmp/mr7-seed-drift-70f_qi8f/generated`. This is not certification of that scratch package; its generic conversion still contained a stub at inspection.

- Replace public generic conversion knobs with dedicated cold-MW-to-W, pump pressure-rise and per-machine electric-demand definitions. Encode `1e6` in the equation; bind subtraction operands to actual inlet/outlet pressures and division to actual assembly pump count. Those are physical producer dependencies, not independently supplied scale/offset/divisor controls. Acceptance must inspect the regenerated public manifest, since source literals alone did not prevent exposure.
- Helium applicability must require enabled equipment and the active primary-loop route (`loop_live=1`). Salt applicability must additionally reflect the selected secondary energy route (`secondary_energy_mode=1`), rather than crediting equipment calculated but omitted from the energy balance. Preserve existing selector validation; inactive or unsupported routes cannot receive affirmative capacity credit. Each relevant demand conversion and downstream screen must use the same applicability. Test active equipment with each energy route disabled separately.
- A fixed numerical identity rule for finite point-state values is approved: `a == b or abs(a-b) <= 8 * max(math.ulp(a), math.ulp(b))`. Hard-code the multiplier; expose no tolerance input and use no absolute floor or default `isclose` tolerance. Eight ULP admits only nearby binary representations: about `9.1e-13 K` near 562 K and `7.45e-9 Pa` near 8 MPa. This is an explicit numerical identity policy, not a derived error bound for every upstream calculation or an engineering operating envelope. Retain actual/rated raw values. Investigate discrepancies exceeding eight ULP instead of widening this rule to recover a passing case.

Apply the same identity rule to native and independent state guards, and amend their exact-equality documentation. Capacity demand, supplied capacity, raw signed margin and `margin >= 0` remain strict and unsnapped. Acceptance must include adjacent and beyond-boundary state values, nonfinite rejection, a materially changed state, and a next-representable insufficient capacity. No tests were rerun in this review; the actual independent/native state discrepancies and completed correction remain to be evidenced.
