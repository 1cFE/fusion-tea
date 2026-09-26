# Steam interface audit

[AGENT] Bounded source/interface audit, 2026-09-26. Scope: the existing steam conversion and helium-to-salt transport definitions, their live handwritten implementations and retained source records. This is evidence for the comparison contract, not approval of that contract or a completed comparative study. No model, package, historical evidence or source file was changed. No external retrieval or holdout access occurred.

## Conclusion

The existing matched steam model can accept the Stellaris-like source through the existing salt transport at its selected temperatures. **The default steam admission is physically consistent:** 465 °C salt supplies 445 °C main steam and reheat; the implemented full-profile minimum gaps are both 20 K. A duty-only comparison at fixed steam, salt and condenser temperatures preserves the steam offered-condition checks. Those checks are not an absolute blocker to a bounded conditional comparison.

The unresolved seams are more specific: the common source return must be enforced in both branches; the inherited aggregate steam-package price needs an explicit matched currency convention and uncertainty treatment; any changed operating temperature requires a supported offered-equipment assumption; and the helium primary pump law must not be transferred to the hotter ARIES divertor without qualification. The current package assumption includes represented steam-generator/reheater children, although their individual prices are unvalidated. A complete steam thermodynamic model is not missing. Detailed machine maps, exchanger hydraulic design and site cooling qualification would be major extensions if the question required that level of prediction.

## 1. What was actually inspected

The starting map calls H1 and H3 compatible, with H3 using a hot divertor stream above the 465 °C salt leg (`work/orchestration/goals/design-space-combinations/evidence/compatibility-map.md:21`, `:24`). WI-093 deferred C-3 because assembling the costed heat-transport and turbine subsystems would copy most of the balance of plant; it did not execute or qualify C-3 (`work/completed/20260926_WI-093_combination-assemblies/design.md:26`). Positive terminal approaches in that map establish only an initial interface opportunity.

Normative bodies inspected:

- `exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py`, abbreviated **cooling body** below.
- `exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py`, abbreviated **steam body** below.
- `exploration/stellarator_e2e/generated/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py`, abbreviated **primary body** below.
- `exploration/stellarator_e2e/generated/handwritten/mfe_viability/steam_offered_conditions_impl.py`, abbreviated **steam conditions** below.

## 2. Thermal joins and return requirements

**Primary helium.** The existing loop takes source duty, blanket inlet temperature and temperature rise as independent quantities. It calculates mass flow, flow-dependent pressure loss, circulator inlet temperature, shaft work and IHX duty. The required IHX outlet is the circulator inlet, not the blanket inlet: `T_comp_in = T_blanket_in / [1 + (pressure_ratio^((gamma−1)/gamma) − 1)/eta_is]`; IHX duty equals source heat plus circulator shaft work (primary body:24–51). The SysML documentation explicitly says this is what the IHX must deliver, not proof that it can (`models/library/analyses/mfe_primary_loop.sysml:34`).

**Helium-to-salt exchanger.** The cooling body assumes salt at 465 °C leaving the IHX and 270 °C entering it. It computes hot and cold approaches as helium-hot minus 738.15 K and helium-return minus 543.15 K; either nonpositive approach refuses evaluation. With both positive, it calculates LMTD and required area using a heat-transfer coefficient anchored at the DEMO reference. Installed area is independently fixed by 14,852 tubes, 19.05 mm diameter and 11.6 m length per exchanger, with one exchanger per selected circuit (cooling body:62–78; normative definition `models/library/analyses/mfe_cooling_equipment.sysml:9`). Required area is checked against that selected geometry. The body does not solve the outlet of an uncontrolled exchanger at full installed UA. Maintaining the prescribed terminals when excess capacity exists therefore remains an operating/control assumption; a claimed control prediction needs an explicit closure.

**Salt loop.** Total salt flow is `Q_IHX × 10^6 / (1560 × 195)`. Salt-pump shaft heat increases the admitted steam-cycle heat, and the pre-pump salt return decreases below 270 °C by exactly that shaft heat divided by salt capacity rate (cooling body:89–106). Consequently, at fixed head and efficiency, `T_return = 270 − g × head/(eta_p × 1560)`, independent of duty. At 40 m and 0.75 efficiency this is 269.6647299145299 °C. Salt supply is 465 °C and heat capacity 1.56 kJ/kg/K in the SysML exposure (`models/library/structure/mfe_plant_systems.sysml:294–300`). The plant binds all five boundary quantities directly into the steam cycle (`models/designs/generic_mfe/mfe_plant.sysml:198–208`).

**Steam side.** The steam body checks both available heat = source heat + selected recovered heat and available heat = salt capacity rate × temperature fall, at arithmetic residual tolerances (steam body:174–180). Main/extraction pressures are restricted to 6.2/0.8 MPa; steam and reheat temperatures are superheated and at most 455 °C; condenser temperature is 20–60 °C (steam body:170–190). It evaluates all piecewise-linear water-enthalpy profile knots, including boiling, against the salt profile. Any minimum gap ≤ 0 yields failed admission and unavailable required UA, not a false passing zero conductance (steam body:129–157, :242–269).

The selected point is 445/445 °C main/reheat and 42 °C condenser, with turbine efficiencies 0.9, pump efficiencies 0.8, pump-motor efficiency 0.95, mechanical efficiency 0.99 and generator efficiency 0.98 (`models/designs/stellarator_09/stellarator_plant.sysml:755–796`). The old fitted-cycle argument is still computed but is not the selected steam state (`models/designs/generic_mfe/mfe_subsystems.sysml:558–560`; WI-073 `design.md:24`).

## 3. Executed diagnostic: default admission and duty-only operation

[AGENT] A focused `.codex-test/run python` diagnostic loaded the live steam body directly by `importlib.util.spec_from_file_location`, supplied the selected states and efficiencies above, and normalized available/source heat to 1000 MW with recovered heat zero. Salt flow was calculated from that heat and the declared salt temperatures. This is a component diagnostic, not a native integrated case or a prediction for a 1000 MW plant.

| Diagnostic output | Result |
|---|---:|
| Main/reheat minimum gap | 20 / 20 K |
| Main/reheat admission | true / true |
| Gross efficiency | 0.3689262426735591 |
| Required main/reheat UA | 12.420851488945114 / 3.3828662172959874 MW/K |
| Feedwater plus condensate pump electricity | 2.9353753202738706 MW |
| Rejection before cooling-water pumping | 634.0091326467146 MW |
| LP moisture fraction, reported without a qualification fence | 0.027190644596582714 |

At fixed states the specific water enthalpies, bleed fraction and salt temperature profile remain fixed; mass flows, shaft/electrical powers and required UA scale with duty (steam body:224–243). **Varying only duty therefore preserves steam offered conditions.** Installed capacities and prices must remain selected inputs. The default main/reheat installed UA are 41.07437838721364/11.18676341684029 MW/K (`stellarator_plant.sysml:757`, `:762`), so reducing duty below their captured point reduces demand without purchasing smaller equipment or qualifying an operating map.

The actual offered-condition code requires state equality within eight floating-point ULPs, not an engineering temperature envelope (steam conditions:10–23). Steam, reheat, condenser, both salt temperatures and both pressures participate. A temperature sweep makes equipment support undefined until a separate supported offer or reviewed performance relationship exists. Changing duty alone does not.

## 4. Which source boundary is genuinely common?

**Preferred starting scope: Stellaris-like supplied helium loop.** The retained C-1 boundary has 3125.93 MW source heat, approximately 3301.21 MW delivered including 175.28 MW of circulator work, 3009.76 kg/s and 773.15 K hot helium (`work/orchestration/goals/design-study-parameters/evidence/starting-configuration.md:9–11`). Its approximately 561.935 K required helium return exceeds the IHX salt inlet by 18.785 K; the hot approach is 35 K. The loop is explicitly a DEMO HCPB transfer, not a demonstrated Stellaris coolant design (`stellarator_plant.sysml:1250–1261`). This conditional starting point has substantially better continuity of assumptions than the hot-divertor transfer.

There are two distinct duty-study contracts:

1. Hold source hot and return temperatures fixed and vary source duty/flow consistently at a supplied conversion-subsystem boundary. This preserves steam temperature support. Common upstream pump power and costs need a stated matched treatment; this boundary is an explicit extension/abstraction of the existing full primary loop.
2. Reuse the full primary-loop calculation unchanged while varying source duty and holding blanket inlet/rise. The required source return then changes because pressure loss changes with flow. A direct diagnostic with unchanged public loop inputs gave required returns 564.164654 K at 2800 MW, 561.935382 K at 3125.93 MW, and 560.641433 K at 3300 MW. All hot temperatures remained 773.15 K. Matching the resulting return within each steam/Brayton pair is possible in principle, but the existing helium point-condition ratings do not provide an envelope across those states (`models/library/structure/mfe_plant_systems.sysml:72–89`). A fixed-return claim cannot be attached to this unchanged duty sweep.

**ARIES divertor alternative.** The integrated model's 374.75 MW literal, 500 kg/s flow and 973.15 K hot bound are visible at `models/designs/aries_cs_integrated/plant.sysml:44`, `:250–253`. Those are not a source-qualified 375 MW operating point. Retained source reconciliation identifies 573→700 °C divertor temperatures, source flow 283 kg/s at 2365 MW fusion, and source divertor pumping 27 MW; 500 kg/s and 10 MW pumping are inherited assumptions (`work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/reference-case-contract.md:31`, `:37`, `:45`; `q1-thermal-cycle-review.md:15`). With 374.75 MW and 500 kg/s, ignoring pump heat, the simple heat balance gives a return of 828.821 K, not the cited 846.15 K. Adding pump heat shifts it again. All of these are hot enough for the salt IHX, but they do not establish one mutually consistent published source point.

Further, the existing primary loop's pressure-loss law assumes the reference density and 300–500 °C window (`models/library/analyses/mfe_primary_loop.sysml:26–32`). Its unchanged reuse at a 700 °C outlet would be an unsupported transport extrapolation. Selecting a supplied divertor heat/temperature/flow boundary with its existing pump account is a smaller extension than pretending the DEMO hydraulics were validated at that state.

## 5. Equipment and complete power accounting

Required steam-branch inventory: helium/salt IHX; salt pumps, piping and purchased salt; any branch-owned helium circulators/piping/inventory; main steam generator and reheater; HP/LP turbines and generator; extraction splitter/open feedwater heater; condensate/feedwater pumps; condenser; cooling-water pumps and heat-rejection equipment. The physical child definitions are in `models/library/structure/mfe_steam_cycle_components.sysml:15–82`; the assembly and state bindings are in `models/designs/generic_mfe/mfe_subsystems.sysml:675–850`. Common upstream equipment must be counted once or excluded consistently from both subsystem boundaries.

The steam gross output includes mechanical and generator losses. Subtract condensate/feedwater pump electricity separately. Subtract primary circulator electricity and salt-pump electricity while admitting their correctly recovered shaft heat. Add cooling-water electricity: that body solves the flow with its own electrical heat included, under a conditional 25→35 °C, 20 m head scenario (`exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/cooling_water_rejection_impl.py:39–58`; WI-073 `design.md:42`). Keep reactor heating and other common plant auxiliaries identical only when the boundary includes them. Existing bindings separate all these channels (`models/library/structure/mfe_plant_systems.sysml:395–400`; `models/designs/generic_mfe/mfe_plant.sysml:378–395`). The Brayton comparator needs equivalent heat-rejection electrical accounting; a thermal rejection rating alone supplies no cooling-pump electricity.

## 6. Modest repairs versus new physical models

| Need | Bounded treatment | Where a major extension starts |
|---|---|---|
| Common source/return closure | Goal-owned source adapter with explicit duty, hot/return states and energy identities; enforce each branch's return and control requirement; retain pre-repair replay | Predicting reactor temperature/duty/flow response or new coolant hydraulics |
| Steam admission | Reuse the existing state and full-profile solver; retain fixed pressure domain and failed gaps | Variable-pressure steam properties/cycle architecture, detailed turbine maps |
| Duty-only steam operation | Keep chosen temperatures, head, efficiencies and equipment fixed; check independently selected UA, flow, power and rejection ceilings at each duty | Claiming experimentally qualified turndown, control stability, or hydraulic/heat-transfer dependence absent from the model |
| IHX operating control | Explicitly state regulated terminal-duty operation or implement/review a narrow return-control relationship with chosen exchanger capacity | Predictive valve/piping distribution, pressure-vessel qualification and broad heat-transfer correlations |
| SG/reheater cost | Retain the explicitly inclusive aggregate offered-package assumption, chosen ratings and fixed price; declare currency treatment and test package-price uncertainty | Predicting individual exchanger prices or marginal prices of changed UA from a new equipment model |
| Cooling system | Reuse conditional water-pumping energy with explicit offered equipment and prices for both cycles | Site heat-sink qualification and a full cooling-system design |

The current accounting scope is explicit: WI-079's selected-package record defines the turbine offer as an “Aggregate turbine conversion account including represented child equipment; child ratings do not add separate capital” (`work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/evidence/selected-packages.json:230–238`). The supplied amount is 247,464,428.83859593 dollars per one-module package, an assumed entering estimate with an inherited nominal dollar convention and no new price-year claim. This includes the represented steam-generator/reheater children as an accounting assumption. The same record includes heat rejection as an aggregate package at 115,939,531.80564217 dollars, with pump ratings adding no separate capital (`:240–249`).

The earlier cycle proposal's unresolved SG/reheater coverage (`work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md:68`) describes the prior coefficient-based estimate. The later inclusive offer resolves the accounting boundary by assumption; it supplies no validated individual SG/reheater prices or marginal price law for changed conductance. That distinction is consistent with the child definition's lack of an individual installed price (`models/library/structure/mfe_steam_cycle_components.sysml:18`) and WI-080's statement that changing ratings at a held amount defines a different hypothetical offer (`work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-implementation.md:11`). A bounded conditional comparison can inherit the inclusive offer and test its price uncertainty. Adding a separate SG/reheater quote would require revising the aggregate scope to avoid counting those children twice. Currency alignment remains an explicit comparison assumption because the retained offer establishes no validated price year.

## 7. MR-7 assessment

### Direct use at a supplied conversion boundary

[AGENT] The proposed 80/90/100% experiment at 773.15 K hot, approximately 561.935 K required return, helium heat capacity 5193 J/kg/K and nominal IHX heat approximately 3301.213 MW is compatible with the cooling and steam equations as a supplied-source experiment. Supply helium flow as `Q/(cp × (T_hot − T_return))` and verify that identity explicitly: the cooling body does not itself enforce this helium energy join. Its relevant calculations use the supplied helium terminal temperatures and duty directly, so instantiating `Cooling Equipment` without `Primary Coolant Loop` avoids introducing the latter's duty-dependent return. At held salt head/efficiencies the salt return stays fixed, steam offered conditions stay fixed, and required UA and machinery demand decrease with duty. The actual selected inventory still needs screening at all three points; this audit has not executed that assembly.

The direct body has an accounting/interface complication, not a missing thermodynamic equation. It also demands positive primary-flow, pressure-loss and primary-power inputs and computes helium circulator/piping/inventory costs (cooling body:30–35, :53–61, :79–88, :125–147). A thin assembly may carry explicitly declared common upstream inputs for those excluded outputs, but must identify them as outside the assessed conversion boundary. Do not use their irrelevant qualification flags to claim the downstream design passed, and do not count their electricity/cost again. Take the IHX, salt pumps/pipes/inventory and associated installation from their disjoint outputs. Replacement and consumables aggregates mix primary and secondary equipment and need a reviewed accounting split or consistent common upstream inclusion; subtracting a guessed fraction is insufficient.

For the steam heat join, supplied source heat is the IHX-boundary heat and selected recovered heat is salt-pump shaft heat only. Primary pump heat is already inside the supplied 3301.213 MW. The steam cycle's cooling-water calculation can be reused for Brayton rejected heat under a declared common water scenario, but its condenser-temperature argument must represent a justified Brayton cooler terminal; steam's 42 °C value is not automatically a valid Brayton rejection temperature. The same body assumes a lumped heat-rejection boundary and its water approach must be checked against the actual cooler/intercooler states. These bindings and accounting selections constitute modest reviewed integration work. They do not require a new steam-cycle model.

| Affected relationship | Roles and evidence | Assessment |
|---|---|---|
| Salt flow/steam flow | Calculated demand from declared heat and fixed states, not installed pump size; cooling body:91; steam body:228 | Compliant within an explicit duty/state contract |
| IHX/steam-generator/reheater capacity | Fixed chosen geometry or supplied UA compared with required area/UA; cooling body:63–78; `mfe_subsystems.sysml:405–428` | Compliant |
| Machine purchases and inventories | Independent selected design-point inputs and purchased fluid masses; cooling body:58, :98–105, :121–137 | Compliant for represented scope |
| Steam package purchase | Independent supplied amount, kept fixed as duty changes; inclusive child scope in WI-079 `evidence/selected-packages.json:230–238` | Compliant; inherited accounting coverage explicit, price accuracy/currency alignment unverified |
| Fixed-duty/state comparison using actual offered ratings | Temperatures unchanged, operating demands checked against held ratings | Candidate compliance supported by equations; native integrated comparison unverified |
| Arbitrary temperature/rating changes or ARIES hydraulic transfer | No supported equipment envelope or transferred pump law established | Unverified; cannot count as passing |
| Automatically setting installed UA/ratings from calculated demand | Would replace an independent design choice with adequacy by construction | Violated if introduced; not performed here |

[AGENT] Recommendation: develop the Stellaris-like conversion-subsystem contract first, with a bounded duty range at fixed source temperatures where justified. Preserve a separate record of primary-loop conditions and control. Carry the inclusive steam offer as an inherited accounting assumption, align currency explicitly, and resolve both branches' cooling-power/cost boundaries before treating results as an economic choice. Test package-price uncertainty and keep individual equipment-price qualification separate from the conditional result.
