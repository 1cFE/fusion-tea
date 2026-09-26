# Fresh feasibility review

[AGENT] **FINDINGS — proceed with the bounded native screen and a narrow integration design. The matched main study is not yet released.** Reviewed 2026-09-26 as a fresh non-author session against the [brief](feasibility-review-brief.md), [owner direction](owner-brief.md), [contract](../comparison-contract.md), and all three audits. Original definitions, bodies and bindings were inspected. No model execution or modification occurred in this review.

## 1. Supplied source: a modest supported interface change

The proposed fixed hot/return boundary is a legitimate conditional conversion experiment. Declare duty and temperatures as supplied, flow as the operating balance, and pump capacity as independently installed. It is not unchanged primary-loop behavior: that loop changes required return with duty. Add an explicit helium energy join; Cooling Equipment does not enforce it. Bind steam heat to supplied IHX duty plus salt-pump shaft heat, which the existing body already accounts for ([cooling body](../../../../../exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py), lines 67–106).

Exclude common upstream circulation consistently or include its electricity, hardware and replacements once. Cooling Equipment mixes primary/secondary replacement costs; split its actual terms rather than subtract an assumed fraction. The steam IHX checks required area against installed geometry; excess capacity does not demonstrate controlled source return. State and review the operating/control assumption before claiming an exactly maintained boundary.

## 2. Coolers: missing checks, not evidence that major physics is required

The [conditioning body](../../../../../exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten/ideal_gas_brayton_components/fixed_outlet_conditioning_impl.py), lines 16–27, imposes the outlet. The [water body](../../../../../exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/cooling_water_rejection_impl.py), lines 23–58, supplies circulation and pumping, not gas-cooler capacity.

Its condenser gap cannot represent a counterflow gas cooler: helium outlet 35 °C and water 25→35 °C give a zero surrogate gap, while the actual cold-terminal gap is approximately 10 K before pump heating. Check both actual terminal gaps and pump-heat location. Add required conductance from the temperature profile/LMTD and compare it with independently offered installed conductance and duty. This is a small extension of the existing exchanger relationships, subject to equation/design review. Positive approaches alone are insufficient; arbitrary capacity labels do not establish applicability. Site qualification remains absent.

Keep recuperator effectiveness conditional or relate it to independently supplied conductance using the existing equal-capacity exchanger relation. State its operating envelope and price ownership. Include generator losses in rejection accounting; the inherited Brayton rejection expression sums only three cooler heats.

## 3. Costs: scope can be disjoint; a common monetary basis remains unresolved

The early SG/reheater omission reading is superseded by [WI-079 selected packages](../../../../active/WI-079_supplied-equipment-design-bases-for-residual-costs/evidence/selected-packages.json), lines 235–247: the aggregate turbine account includes represented child equipment. Preserve that inherited accounting assumption; separate SG/reheater purchases would duplicate it. The same record explicitly makes no price-year claim.

Brayton services can own recuperator/conditioning under an explicit assumed allocation; [WI-090 E4](../../../../completed/20260922_WI-090_aries-integrated-equipment-and-costs/design.md) supports allocation sensitivities, not procurement qualification. Resolve installation, fluids, remaining auxiliaries, operating expense and replacements without overlap. A missing historical steam currency basis cannot be repaired by relabeling dollars. If unresolved, report cost corrections/break-even thresholds with symbolic conversion factors and economic completion unmet.

## 4. Minimum next work and MR-7

1. Execute the contract's unchanged-package diagnostic screen, including steam duty-only cases and the original/matched Brayton controls. Retain native identities, exceptions, capacity/condition verdicts, heat/return residuals and unimplemented checks. These controls establish neither matched performance nor economics.
2. Write the small native design for the source join, cooler checks, recuperator applicability, disjoint electricity/cost ledger and explicit offered inventory. Review its actual bindings before implementation. Exercise insufficient/sufficient hardware and fixed-hardware demand changes.
3. Release matched performance execution after that evidence passes. Release complete economic ranking only with justified common-currency offers and complete scoped recurring costs; otherwise execute a clearly partial threshold analysis.

**MR-7: compliant for inspected existing choices.** Steam installed UA feeds capacity screens independently of demand (`models/designs/generic_mfe/mfe_subsystems.sysml:405`); Brayton selected area feeds both conductance and purchase (`models/designs/costed_loop_brayton/costed_loop_brayton.sysml:181`). **Unverified for the proposed assembly**, which has no implemented bindings or acceptance evidence. Demand-derived installed capacities would be **violated**. No owner gate or categorical physical blocker is established by this review.
