# Cooling equipment costs: implemented conceptual estimate

The executable now sizes and separately prices helium circulators, intermediate salt pumps, piping and helium-to-salt heat exchangers. Installation, initial spares, coolant inventories and scheduled replacements feed the plant cost accounts and electricity cost. The focused study passes native verification, and the [fresh independent assessment](evidence/round3/final-review-and-grade.md) confirms **R7.S3 is met** against the unchanged rubric.

This is a conceptual equipment estimate with declared construction and price transfers. It is not a quotation, a pressure-qualified equipment selection or a complete installed-plant price. The newly priced scope substantially increases estimated cost.

## Scope and equipment

The owner-approved intermediate coolant is HITEC, a molten-salt mixture, operating at 270–465°C. Primary helium remains at the existing nominal 8 MPa and 300–500°C conditions. The [account-boundary map](evidence/round3/account-boundary-map.md) identifies one owner for every modeled item. The [combined design](../../../active/WI-067_installed-cooling-equipment-costs/combined-design.md) records the quantities, raw source prices and assumptions.

For the retained selected eighteen-circuit design, the generated executable gives:

| Equipment | Quantity and engineered requirement | Sizing or layout basis |
|---|---|---|
| Primary helium circulators | 36 active; each 78.288 kg/s, 11.764 m³/s at suction, 159.303 kPa rise and 2.410 MW shaft power | Two parallel machines per circuit. Existing thermal flow and hydraulic pressure-loss calculation; suction 7.841 MPa at about 294°C. |
| Intermediate salt pumps | 36 active; each 275.213 kg/s, 2,317.752 US gal/min, 40 m developed head and 143.942 kW shaft power | Calculated exchanger duty, salt heat capacity and 195 K temperature rise determine flow. Head and efficiencies are explicit assumptions. Cold-side suction is assumed 0.20 MPa absolute; calculated discharge is about 0.938 MPa. |
| Helium-to-salt exchangers | 18; 3,013.915 MW total, 167.440 MW each; 5,824.089 m² required versus 10,310.691 m² installed area each | Duty includes recovered primary compression work. Thermal approaches and source effective heat-transfer coefficient determine required area. A fixed source-scale exchanger geometry is priced; shell, tube-sheet and tube thicknesses are conceptual construction assumptions. |
| Primary piping and fittings | 6,261.253 tonnes of modeled stainless fabrication | Per circuit: 50 m hot and cold mains, 1.3/1.1 m outside diameters, 65 mm walls; nine hot and nine cold branches with 30 mm walls and assumed routing. Source fitting mass ratio added once. |
| Salt piping and fittings | 462.448 tonnes | Per circuit: 50 m hot plus 50 m cold, 0.40 m inside diameter, 20 mm wall. Calculated straight-pipe head loss is 0.905 m; the remaining 39.095 m is an unallocated allowance, not a solved exchanger/fitting pressure loss. |
| Initial inventory and spares | 21.269 tonnes helium and 2,068.394 tonnes salt, including 10% mass reserve; one uninstalled spare of each machine type | Inventories cover explicitly modeled ex-vessel pipe and exchanger volumes. They exclude unmeasured in-vessel, tank and conversion volumes. |

The starting records confirm eighteen circuits, 36 helium machines and eighteen exchangers; saved r2 controls use fourteen circuits. Eighteen was never established as an optimum. [Retained input extraction](evidence/starting-cases.json), [entering replay](evidence/entering-replay.json), and [native study](../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/record.md) retain the exact input precision and historical/current distinction.

## Purchased and installed costs

The following selected-design figures are million US dollars expressed using a **2025 annual-CPI purchasing-power proxy**. CPI is not an equipment escalation index. The inherited rest of the plant remains on its prior mixed price basis; these are not uniformly rebased 2025 plant costs. Source currency, year, equations and inclusion boundaries remain in the [primary source assessment](evidence/round2/circulator-transfer.md), [exchanger source assessment](evidence/round2/hx-method-check.md), and [secondary methods](evidence/round3/secondary-methods.md).

| Account | Purchased/fabricated supply | Site installation | Account total |
|---|---:|---:|---:|
| Active helium circulator packages | 350.259 | 109.228 | 460.129, including 0.642 one-time supplier design |
| Primary pipes and fittings | 2,549.181 | 1,274.590 | 3,823.771 |
| Heat exchangers | 3,528.947 | 91.753 | 3,620.700 |
| Active salt pump/motor packages | 2.346 | 0.732 | 3.077 |
| Salt pipes and fittings | 188.279 | 94.140 | 282.419 |
| Initial coolant inventories | 5.446 | Not separately estimated | 5.446 |
| Uninstalled spare machines | 9.795 | None at initial purchase | 9.795 |
| **Total** | **6,634.894 including supplier design, inventories and spares** | **1,570.442** | **8,205.337** |

The helium price relation transfers the BNL supplier reference of $550,000 per machine, $110,000 power supply and $130,000 first-design engineering in December 1978 dollars. It responds to suction pressure and shaft duty; transfer to multi-megawatt machines is uncalibrated. The source includes fabrication, testing and delivery. Salt pump/motor prices use the Seider generic liquid-pump and motor equations in the CE500/2006 basis, with explicit material/type factors and operating-range checks. Their transfer to hot-salt construction remains unvalidated.

Pipe and exchanger prices use the ANL $310/kg in 2017 dollars for finished nuclear stainless fabrication and delivery. It is not a raw-steel price. Component steel mass determines the bill. Exchanger installation adds the source 2.4% labor and 0.2% material; piping uses the separately identified NETL field-labor transfer of 50% of the fabricated bill. Pump setting uses the reviewed ORNL installation analogy, with its procurement-inclusive denominator reproduced but no second procurement-services charge. These conceptual transfers dominate uncertainty; the study's alternatives are scenarios, not a calibrated confidence interval.

## Replacement of the old accounts

The Cost Account Structure (CAS) is the hierarchy that totals plant costs. Equipment mode **replaces both old C220200 cooling terms completely**: the primary net-power relation and the intermediate thermal-power relation. It does not add the equipment bill on top of either old allowance. Seven separately calculated child accounts roll into the one existing heat-transport consumer.

In-vessel blanket structures, turbine/power conversion, ultimate heat rejection, magnet cryogenics and buildings retain their separate homes. The cooling boundary ends at the salt supply/return interface to power conversion. The steam generator belongs to Row8/CAS23; its inclusion in the inherited price is **unverified**, not established free or fully paid for.

Fabrication is already included in finished component prices. Delivered initial purchases are removed from the existing shipping base. Procurement and project engineering remain CAS30; supplier first-design work is distinct and charged once. Initial cooling spares are outside the inherited spare fraction's CAS23–28 base. Account identity tests check these boundaries and their effects on contingency, indirects, shipping and total capital. The inherited shipping charge on contingency remains a disclosed approximation.

## Lifecycle treatment

The default 30-year scenario replaces active machines in years 10 and 20, and tube bundles in year 15. Pipes and exchanger vessels have assumed 60-year lives, so no replacement occurs during this horizon. These are assumed service lives, not measured reliability. Replacement purchases, installation and an explicit removal-labor proxy are discounted and annualized into CAS72, the replacement-expense account. Initial spares and first-design fees are not repurchased at every event.

For the selected eighteen-circuit design, the added equivalent annual replacement expense is **$63.243 million/year**. Coolant make-up adds **$5,446/year before existing expense levelization**, assuming annual loss of 0.1% of the priced inventory. Existing CAS71 routine operation and maintenance is assumed to cover service labor. Replacements are assumed to coincide with existing outages, leaving availability unchanged. Extra outages, disposal and dedicated handling are unpriced. The study varies machine/bundle life, make-up, inventory reserve and removal cost explicitly.

## Matched plant results

LCOE means levelized cost of electricity. “Legacy” uses the old cooling allowances and no added salt-pump energy; “cost only” replaces costs and adds lifecycle expense at identical plant performance; “full” also adds salt-pump electricity and recovered shaft heat. Equipment diagnostics run in every mode, but their costs and energy enter plant totals only when selected.

| Retained input case | Mode | Total capital, $billion | Net electricity, MW | LCOE, $/MWh |
|---|---|---:|---:|---:|
| Selected, 18 circuits | Legacy | 9.466 | 1,010.112 | 150.430 |
| Same inputs | Cost only | 20.901 | 1,010.112 | 309.555 |
| Same inputs | Full | 20.903 | 1,006.725 | 310.633 |
| Selected, 14 circuits | Legacy | 9.491 | 975.844 | 156.052 |
| Same inputs | Cost only | 18.426 | 975.844 | 285.388 |
| Same inputs | Full | 18.429 | 972.393 | 286.438 |
| Saved r2 forward, 14 circuits | Legacy | 10.205 | 1,003.739 | 162.871 |
| Same inputs | Full | 19.155 | 1,000.101 | 289.997 |
| Saved r2 Table5 control, 14 circuits | Legacy | 10.214 | 1,003.767 | 162.947 |
| Same inputs | Full | 19.164 | 1,000.139 | 290.047 |

For selected eighteen circuits, the old $205.073 million allowance becomes an $8,205.337 million equipment estimate. The direct increase is $8,000.263 million. Existing plant-level factors turn that into $11,434.850 million additional capital in the cost-only comparison; lifecycle expense also contributes to the $159.125/MWh LCOE increase. Adding salt energy then increases capital by $2.846 million and LCOE by $1.078/MWh. Salt pumps draw 5.455 MW and return 5.182 MW shaft heat to conversion; after the retained efficiency calculation, net electricity falls 3.387 MW. Total primary-plus-salt pumping electricity is 92.231 MW.

Fourteen circuits costs less than eighteen under these assumptions, while requiring more pumping electricity and larger individual salt machines. Its liquid-pump cost applicability checks fail. This is not an optimum or a qualified cheaper design. The full study retains all 34 scenarios, including count, demand, layout, construction and lifecycle sensitivities. Its [report](../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/report.md) provides the complete comparisons.

## Sensitivity and what drives the estimate

Primary pipes and exchangers dominate the new cost. Their fixed representative geometry is purchased once per circuit, so increasing circuit count adds metal and installation even as individual machine flow and pressure rise fall. Heat demand changes flow, required exchanger area and machine prices; this implementation checks the installed exchanger capacity rather than inventing a resized exchanger pressure-loss law.

| One change from selected eighteen-circuit full mode | LCOE, $/MWh | Interpretation |
|---|---:|---|
| Half / twice assumed pipe length | 271.612 / 388.673 | Layout uncertainty dominates; this is an accounting sensitivity, not a recalculated primary hydraulic layout. |
| Exchanger shell wall 0.10 / 0.30 m, versus 0.20 m | 289.968 / 332.743 | Strong construction-mass effect; thinner is not established structurally acceptable. |
| Tube wall 1.0 / 2.0 mm, versus 1.5 mm | 304.520 / 316.376 | Construction and future bundle replacement both change. |
| Machine life 20 / 30 years, versus 10 years | 307.687 / 306.189 | Fewer replacements; the longer lives are assumptions. |
| Bundle life 30 years, versus 15 years | 307.133 | No bundle replacement strictly inside the 30-year horizon. |
| Twelve / sixteen / twenty circuits | 277.964 / 297.757 / 324.443 | Twelve fails loop capacity; lower counts also fail salt-machine price ranges. No optimum follows. |
| Plasma density −2% / +2% | 319.342 / 302.498 | Supported demand change propagates through heat, flow, machine sizing, electricity and cost. |

These are separate one-at-a-time scenarios. They are not joint uncertainty bounds or recommendations to use thinner walls, longer lives or fewer circuits.

## Engineering limits and verification

All current scenarios fail the tritium-breeding acceptance check. The historical selected designs passed their earlier represented checks; that history does not establish current feasibility. The eighteen-circuit case passes exchanger area, salt pump/motor equation ranges and straight-pipe head screens, but still has major declared gaps:

- The inherited efficiency-fit argument is 480°C while salt supply is 465°C. Its physical-interface check fails. Full-mode electricity results retain an explicitly labeled surrogate rather than a thermodynamically solved salt/steam cycle.
- Pressure boundaries, allowable stresses, material life and hot-salt machine construction are not qualified. Thick walls are cost geometry assumptions with sensitivities.
- The assumed primary pipe-plus-exchanger volume is 1.91 times the source reference inventory volume. This is retained as a layout warning, not hidden by an invented residual.
- The salt inventory is below the source industrial-bulk procurement category. Detailed valves, local supports/insulation, expansion/drain tanks, trace heating, nitrogen cover and additional inventory remain unpriced. Their cost significance is not established negligible.

Native integration passes all ten gates at the reviewed pin. All 34 study cases pass software verification: 12,206 scalar comparisons and 680 exact predicate comparisons, with the generic verifier also passing. The separately recorded default baseline passes another 359 scalar and 20 predicate comparisons. An inherited current-margin oracle operation-order discrepancy was corrected without changing any native result, input or threshold; the original failed verification remains retained. Separate original-source reviews establish the conceptual transfer basis; generated/oracle agreement checks software, not physical applicability. Targeted tests include the 98-test batch, later equipment checks, and 258 passing equipment/current-sizing/manufacturing-oracle tests after the exact-boundary correction. The expanded consumer batch has 71 passes and the same six pre-existing stale-contract failures. Static validation retains Level2/6 failures; new diagnostics and their runtime bindings are explicitly dispositioned. The integration seam does not test assertion read-set coverage. This is not a clean full-suite claim. See [verification status](../../../active/WI-067_installed-cooling-equipment-costs/evidence/verification-status.md).

## R7 result and project status

**R7.S = 3, independently assessed PASS.** The exact unchanged target is “Pumps, piping, heat exchangers as separately sized subaccounts,” with appropriate lifecycle logic. The reviewer checked original source scope, actual executable results and account/lifecycle identities. This closes the technical structural-cost gap at S3; it does not award S4, regrade physics or eliminate the stated engineering and price gaps. The complete study is committed at `5b956a82`; the snapshot and all124 artifact hashes are retained. The frozen r2 archive, historical studies and requested rubric revision remain unchanged. ARIES stays sealed. No merge or push occurred. The owner formally closed this goal on 2026-09-18; see the [closure record](trail.md).
