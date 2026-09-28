# T-001 upstream reactor, loads and account evidence

[AGENT] Bounded retained-evidence investigation, 2026-09-27. This is a proposed comparison boundary and account map, not certification of an operating Stellaris plant. No models or frozen studies were changed, no external sources fetched, no quarantined source read. Exact numerical inventory below comes from the retained WI-080 native baseline, not stale headline prose in the design file.

## Recommendation and material limits

[AGENT] Use the current **Stellaris helium-primary modeled alternative** as one fixed installed reactor inventory. Supply source heat and derive compatible fusion/fuel demand under an explicit auxiliary-heating scenario. This is the strongest compatible existing inventory because it already has separately supplied magnet, fuel-processing, cooling and facility purchases, plus traceable disjoint CAS accounts. It is not the paper's water-cooled PbLi blanket with separate helium first-wall circuit; the generic radial build and transferred neutron multiplier remain assumptions. Do not take the complete ARIES reactor capital as its replacement.

[AGENT] A conditional costed reactor inventory is possible now. A demonstrated physically adequate core at these conditions is not established. The retained baseline has material winding-pack fit and conductor-current failures independent of the source-load reduction, plus a 10 FPY coil-life limitation. Carry these visibly as unresolved reactor qualifications, put explicit incremental inventory/service allowances around them, and test whether the conversion preference survives. If the headline requires full current-core physical adequacy, this evidence does not supply it. The owner permits a supplied-source component-isolation study; that permission must not become a claim that failed reactor checks passed.

[AGENT] At 3000 MW source with the predecessor's loss factor 1.1, the retained primary pressure-rise offer is also inadequate: required 304270.726 Pa exceeds supplied 300319.896 Pa. The 2500/2800 MW conditions lie below that pressure-rise rating. Any changed primary offer must be selected and priced explicitly, and held common between the paired branches.

## Evidence identity and provenance

- [INHERITED] Numerical receipt: `work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json`, SHA256 `195f8eb4bbc8889175b726b8ed8eb08d502d12aaa78b6f35b7016cec0e60358c`, 1352 numeric outputs and 68 response entries. It is a retained executed baseline; this task did not rerun it. All abbreviated receipt keys below begin `stellarator_09__stellaris__`.
- [INHERITED] Inventory inputs and source comments: `models/designs/stellarator_09/stellarator_plant.sysml`; assembled ownership: `models/designs/generic_mfe/mfe_plant.sysml` and `models/library/structure/mfe_plant_systems.sysml`. WI-075–080 records establish supplied inventory/cost/capability roles.
- [INHERITED] Cooling equations and money: `models/library/analyses/mfe_cooling_equipment.sysml`; active purchase selection is `heat_transport__cooling_selection__cost`, not dormant `heat_transport__coolant__cost`.
- [INHERITED] Fuel and facilities: WI-069, WI-070 and WI-068 designs cited in the model. Active fuel processing is `fuel_cycle__processing_cost__cost`; active facilities are `buildings__facility_accounts__cost`.
- [AGENT verified] Inspected retained Table 2 image `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_002_table_0.png`: R 12.7 m, a 1.3 m, B-axis 9 T, peak conductor 24.9 T, 48 coils, 15.4 MA peak coil current, 50 MW plasma-coupled ECRH, approximately 2700 MW fusion, 3150 MW thermal, 1000 MW electric and 4.05 MW/m² peak neutron wall load. That particular table image prints 428 m³; model prose says 425 m³. Do not use a rounded volume citation to silently replace the model's selected geometry or claim a reconciled source volume.

## One installed plant and operating/source roles

[INHERITED] Held inventory: R=12.7 m, a=1.3 m, kappa=1; 0.8 m blanket, 0.2 m reflector, 0.2 m high-temperature shield, 0.15 m structure, 0.1 m vessel, 0.1 m vacuum gap, 0.05 m first wall; 48 coils, 308 reference turns, 50 kA effective turn current, 25 m reference winding circumference, 11,615,604.483 kg supplied electromagnetic support. Native radial-build volumes are blanket 1013.406045 m³, shield 517.043901 m³, structure 204.937401 m³ and vessel 147.905892 m³. The model's older inline approximate volumes are superseded by this receipt.

[INHERITED] Primary selection: 14 circuits, two active circulators per circuit and one initial spare; selected per-machine pumping duty 6.260033372 MW, selected suction 7699680.104 Pa; per-circuit flow ceiling 225.077778 kg/s. Helium purchased stock 16607.698111 kg. Primary pipe geometry uses 1.3/1.1 m OD mains, 65 mm walls and 50 m each leg, plus the represented branches; native represented pipe mass 4,869,863.200 kg. This selected inventory stays fixed when source heat changes. It is a conditional EU-DEMO-derived hydraulic/layout transfer, not a complete new reactor routing design.

[INHERITED] `component_alternatives/plant.sysml:19` defines the predecessor's `blanket_source.q_source` as heat delivered to the primary loop **before** recovered circulator work. `mfe_power_balance.sysml` defines `Q_source=mn*P_neutron+P_alpha+H`, where `P_alpha=(3.52/17.58)*P_fusion`, `P_neutron=P_fusion-P_alpha`. The primary loop then produces `Q_IHX=Q_source+W_fluid` and independently consumes `P_primary=W_fluid/eta_drive`. Source heat 2500/2800/3000 MW is neither fusion power nor IHX duty.

[AGENT proposed] Hold coupled heating at the paper's 50 MW installed scenario, with 50% source efficiency and unity coupling: 100 MW wall-plug. Then `P_fusion=(Q_source-50)/(1.2*(1-3.52/17.58)+3.52/17.58)`. This is a conditional source conversion, not plasma sustainment reconstruction. Alternative H=0/25/50 MW can test the assumption, but 0 MW means an assumed ignited condition, not demonstrated ignition. The existing 50 MW heating purchase remains installed at all loads.

| Supplied Qsource MW | Derived fusion MW at H=50 | Primary fluid/electric MW at eta_drive=1 | Per-circuit flow kg/s | Primary pressure rise Pa |
|---:|---:|---:|---:|---:|
| 2500 | 2112.151824 | 98.423698 | 171.934747 | 211299.115 |
| 2800 | 2370.782660 | 138.452713 | 192.566917 | 265053.610 |
| 3000 | 2543.203217 | 170.448431 | 206.321697 | 304270.726 |

[AGENT calculated illustration] Table above directly evaluates the existing primary-loop equations at predecessor f_loss=1.1, 573.15 K inlet, 200 K rise, cp5193 J/kg/K, gamma5/3, 8 MPa, eta_is0.772796639536644. It is evidence arithmetic, not a substitute for native generated calculation in the final study. eta_drive=1 is a documented lower bound on electrical draw. Holding primary work at a fixed percentage of heat would discard the existing flow/loss relationship.

## Power ownership

| Item | Retained value or rule | Proposed whole-plant owner |
|---|---|---|
| Primary circulators | Native predecessor primary_loop p_elec; table above | Subtract once from each branch's subsystem net. Recover W_fluid in Q_IHX once; motor losses are not automatically recovered there. |
| Coupled ECRH / wall-plug | Retained operating point 49.0796008/98.1592016 MW; installed50/100 MW | Supply common H scenario, calculate wall-plug H/(eta_source*eta_couple), compare with supplied heating capability. |
| Coil lead/joint drive | 0.0502673272 MW | Separate electrical load; do not add another steady 111 MW (111 is stored GJ). |
| Cold/intercept refrigeration | 1.5353731658 + 0.6023889434 = 2.1377621092 MW | One combined refrigeration draw. |
| TF cooling | 15 MW; PF cooling0 | Separate inherited cooling-system allowance, hold common and include sensitivity because auxiliary-cooling scope is coarse. |
| Tritium processing | 10 MW | Common processing allowance; vacuum pumping has represented gas throughput but no independent electrical producer, so explicitly assign vacuum electricity to this allowance or an extra supplied load and disclose. |
| Housekeeping | 4 MW | Common house/service load. |
| Subsystem/control power | f_sub=0.03 times gross electric in old balance | Potential duplicate: predecessor conversion ledgers already own controls/auxiliaries. Select an explicitly disjoint reactor control allowance or carve overlapping branch controls before applying any gross fraction. Never blindly add old3% to the full predecessor. |
| Steam salt, feed/condensate, cooling-water pumps | Predecessor steam ledger owns | Retain once; do not use baseline primary-plus-salt `p_pump_total` to subtract salt again. |
| Brayton compressors | Already subtracted as shaft work before generated net | Never subtract compressor work a second time as electric load. Existing gas rejection/cooling/services stay branch-owned. |
| Imported electricity | max(-whole_plant_net,0) times annual hours | Lifecycle import expense only when appropriate; nonpositive net cannot receive export LCOE. |

[AGENT proposed] The nonheating fixed upstream subtotal excluding primary and unresolved control/vacuum increment is 31.1880294364 MW = 0.0502673272+2.1377621092+15+10+4. At H50, add100 MW ECRH. These are existing assumptions, not new qualified measurements.

## Disjoint fixed account map

[INHERITED] The following exact receipt values are model dollars with the money distinctions below. They should enter model-owned supplied purchase leaves and native sums. Holding them fixed is an explicit fixed-inventory scenario, not reapplying historical power-scaled purchasing as demand changes.

| Account | Retained amount $ | Exact receipt suffix | Treatment |
|---|---:|---|---|
| CAS10 land/preconstruction | 16901536.908759248 | `facility_preconstruction__cost` | Retain; active facility footprint basis |
| CAS21 facilities | 799758795.940320015 | `buildings__facility_accounts__cost` | Retain chosen existing buildings and declared common envelope; conversion-specific expansion is extra |
| CAS22 magnet | 1707443242.259755135 | `magnet__magnet_capital_rollup__capital_cost` | Retain conditional inventory; excludes legacy comparison magnet costs |
| CAS22 heating | 264145000.000000000 | `heating__heating_cost__cost` | Retain installed 50 MW coupled package |
| CAS22 divertor | 109109123.155930519 | `divertor__divertor_cost__cost` | Retain selected package; source-dependent thermal check needed |
| CAS22 blanket/first wall | 719155016.196642518 | `blanket__blanket_cost__cost` | Retain selected geometry |
| CAS22 shield | 452529516.994486034 | `shield__shield_cost__cost` | Retain selected geometry |
| CAS22 nonmagnet structure | 32373952.820015125 | `structure__structure_cost__cost` | Retain residual; magnetic supports already in magnet |
| CAS22 vessel | 113317730.127626330 | `vessel__vessel_cost__cost` | Retain selected geometry |
| CAS22 power supplies | 86013482.741806164 | `power_supplies__power_supplies_cost__cost` | Retain selected package |
| CAS22 remote handling | 157969959.252817959 | `remote_handling__cost` | Retain fixed procurement class |
| CAS22 reactor installation | 509887983.296871185 | `installation__cost` | Retain; original base is core plus remote handling, excluding cooling |
| CAS22 primary circulators | 442174444.749116242 | `heat_transport__equipment__primary_circulators_cost` | Retain includes active vendor+design+installation; spare separate |
| CAS22 primary piping | 2974043934.375750542 | `heat_transport__equipment__primary_piping_cost` | Retain installed fabrication+field labor |
| Primary initial spare | 12020446.033021579 | `heat_transport__equipment__primary_spare` | Retain once |
| Primary helium initial fill | 1409367.527367595 | `heat_transport__equipment__helium_inventory_cost` | Retain; explicitly priced represented subset |
| CAS22 auxiliary cooling+cryo | 35116270.129820704 | `cryoplant__aux_cooling__cost` | Retain includes31.478692M cryoplant plus3.637578M auxiliary allowance |
| CAS22 waste | 6481502.633743829 | `waste__cost` | Retain fixed thermal procurement class |
| CAS22 fuel processing | 22811717.720117148 | `fuel_cycle__processing_cost__cost` | Retain active processing quote; check capacity at held stock/throughput |
| CAS22 other reactor equipment | 10098565.144581091 | `other_rpe__cost` | Retain; explicitly assign vacuum equipment here if no separately priced package |
| CAS22 reactor I&C | 81921417.185930178 | `inc_cost__cost` | Retain plasma/central supervisory controls, exclude package-local controls |
| CAS24 electric plant | 105407841.903247327 | `electric_plant__electric_cost__cost` | Retain shared grid/switchgear distribution only; predecessor generator and local motor drives remain branch-owned |
| CAS26 misc plant | 64159703.769580752 | `misc_plant__misc_cost__cost` | Retain shared residual; specify scope |
| CAS27 PbLi initial fill | 23815042.059888843 | `special_materials_capital__special_materials_capital` | Retain selected volume; replace/refurbish fraction at blanket events explicitly |
| CAS40 owner | 37985982.203505553 | `owner__cost` | Retain fixed owner preparation class |
| Annual routine O&M | 50617243.276030459 | `om_cost__annual_om` | Retain staffing allowance before inflation; determine conversion O&M overlap explicitly |
| CAS28 digital twin | 5000000 | instance `cas28_capital` | Retain central digital-twin scope once |

[AGENT] Account values above exclude new conversion purchases, financing, terminal events, stock-purchase replacement and explicit missing-scope allowances. They are an inventory, not an already complete overnight total.

## Exclusions and exact double-count traps

[AGENT] Remove the old full cooling purchase `heat_transport__cooling_selection__cost=6471347145.807992` from a new whole-plant rollup, then add only the primary-owned pieces above and the new branch-owned conversion pieces. Its old HX2816099940.869176, secondary piping219659254.513647, salt pumps3025188.849982, salt spare82358.851186 and salt fill2832210.038747 are replaced by the predecessor's selected steam branch equipment, not common reactor purchases. The existing primary-only pieces sum3429648192.685253 dollars. The generic older `coolant__cost=180463075.174766` is a dormant comparison, never another account.

[AGENT] Remove old CAS23 turbine247464428.838596 and CAS25 rejection115939531.805642 before inserting either predecessor branch's conversion purchases. Keep CAS24 electric plant only under a declared shared-grid/switchgear scope, since the branch generator and local drives are already priced. CAS26 misc remains shared only with an explicit residual scope. The fixed existing turbine/cooling halls may be held common as an assumed reusable envelope; branch-specific expansion costs need a differential allowance because a complete layout fit has not been checked.

[AGENT] Do not copy baseline CAS20/29/30/50 or overnight17751261591.194653 wholesale. Those totals include the removed cooling/conversion amounts. Recompute indirect/contingency/owner terms from the new disjoint base using one declared convention. Generic MFE uses10% contingency then20% indirect adjusted by construction time; ARIES uses20% indirect then20% contingency and5% owner. Either is an assumption, not an interchangeable source fact. CAS50 includes shipping/taxes/insurance, spares, startup fuel and a decommissioning provision; split those explicitly before reuse. Installed cooling already includes direct installation/delivery exclusions. Startup T stock must replace the generic startup fuel allowance; a dated terminal event must replace the PV decommissioning provision. No second financing charge is permitted.

[INHERITED] Active replacements and O&M must also be disaggregated: baseline cooling replacement annual55673507.794149 includes primary machines, salt machines and exchanger bundles. Keep a primary-only event cost, and let branch machinery/bundle events own the remainder. The whole generic replacement annual193999912.574855 must not be added to new dated events.

## Fuel balance and service assumptions

[INHERITED] Existing fixed-source-compatible conservation definitions are `Fuel Cycle Flows` and `Fuel Inventory` in `models/library/analyses/mfe_fuel_cycle.sysml`, and `Annual Selected Fuel` / `Selected Stock Atoms` in `integrated_equipment_costs.sysml`. Existing Stellaris inputs include per-reaction17.58 MeV, MeV conversion1.602176634e-13 J, T mass5.008267663228036e-27 kg, burn fraction0.05, internal exhaust recycle0.99, extraction1.0, decay1.782785958230312e-9/s. These are inherited assumptions, not experimental qualification. Existing processing inventory and capability is independently supplied; preserve it and calculate demand from fusion.

[INHERITED] Retained computed blanket yield: mean1.1980739195540366, lower1.1861455810023918, Li6 part1.1947266274106922 and Li7 part0.0033472921433443455. Required baseline TBR1.1916699222592924. The mean balances fuel, but the lower supported estimate misses by0.0055243412569006. Existing `tbr_ok` is therefore violated; do not claim demonstrated fuel self-sufficiency. Transfer of this transport surrogate and neutron multiplier to the helium-primary scenario remains conditional.

[AGENT proposed] Keep the blanket geometry fixed and use the retained mean/lower yield as explicit **conditional breeding-yield scenarios**. Model usable new feed as `eta_extract*TBR*burn` times operating hours, separate from internal recycle. External annual makeup is `max(annual_burn+annual_permanent_loss+calendar_stock_decay-usable_new_feed,0)`, no sales credit for excess. This avoids a fixed100kg/year headline and allows fuel cost to track source heat. Show a no-credit external-supply stress case and a conditional self-sufficient supply case with a separately declared service charge; neither establishes breeding capability. Sweep T price down to zero as a ranking diagnostic, then use a transparent retained-price scenario and thresholds.

[INHERITED] Baseline fuel stock4.41795274454kg; startup-conservative requirement4.40012421570kg; processing D+T flow12.9117940450kg/day. Annual baseline burn134.280046970kg, permanent recycle loss25.513208924kg, calendar decay0.248385865kg, extracted new feed160.877422191kg at availability0.902777778. Those depend on the original2652.56MW fusion point; recalculate for supplied heat rather than copying annual amounts. Holding selected4.418kg stock is a legitimate chosen-inventory test if the demand/capacity check remains explicit. Initial purchase uses the selected startup stock once, not the sum of nominal compartments plus startup requirement.

[INHERITED] Legacy Stellaris `DT Fuel Cost` uses a feedstock-price factor and is not the same financial meaning as explicit external tritium shortfall. Its annual550716.18149 must not be added to an explicit T/D purchase ledger without determining its scope. ARIES integrated economics used30MUSD2004/kg T as an assumed price, and10–100MUSD2004/kg as stress prices; these are neither current supplier quotes nor established uncertainty bounds. The predecessor's documented321.9/188.9 CPI conversion can map that assumption to USD2025, clearly labelled purchasing power. Fuel-zero/low-price cases are required to show whether the result is driven by that assumption.

## Lifecycle completion

| Item | Retained evidence | Proposed treatment and unresolved assumption |
|---|---|---|
| Blanket/divertor event |828264139.352573 dollars; first-wall fluence18MWyr/m²; baseline physical life4.523926FPY | Derive wall loading from conditional fusion at fixed geometry, or supply a declared5FPY service life. Use dated events strictly before retirement. Include declared PbLi refurbishment/replacement fraction; the old event includes blanket+divertor only. |
| Planned replacement outage |7/12year estimate; source maintenance paragraph cited at stellarator_plant.sysml:2065 | Use one availability/calendar convention for all cost, burn and annual energy. Do not add outages again to already selected net availability. |
| Coil service |10FPY source estimate; baseline27.083333FPY productive life, margin−17.083333FPY | Thirty-year operation needs explicit magnet/coil service assumptions. A conservative scenario can replace the full selected magnet purchase at10FPY intervals plus supplied removal/installation allowance and outage; it is not a sourced replacement method. A long-life alternative is a sensitivity, not silent nominal adequacy. |
| Primary machines |10calendar-year life selected in cooling model | Active primary event purchase336572488.924604 plus installation104960130.671138 plus removal multiplier×104960130.671138; initial spare already counted once. At removal multiplier1, event546492750.266880 dollars. |
| Primary piping |Retained installed purchase; no modeled scheduled replacement | Supply explicit plant-life piping assumption; pressure/material qualification remains unverified. |
| Conversion services |Predecessor owns branch replacements and service costs | Preserve its events and complete omissions through declared package allowances, with no overlap with plant routine O&M. |
| General O&M |50617243.2760305 dollars/year staffing assumption at fixed procurement class | Use raw annual amount in constant-money DCF; do not import the generic2% escalated CAS71 output into a real-price convention. Bound any unresolved routine maintenance overlap. |
| Coolant makeup |Primary helium1409.367527 dollars/year at0.1% selected-stock makeup | Keep primary portion; salt/conversion stock makeup is branch-owned. Missing in-vessel primary stock is an explicit allowance. |
| Terminal / salvage |Generic CAS50 old provision; integrated lifecycle explicit terminal10% and salvage2% assumptions | Use one declared dated terminal cost, remove old provision, and scope it to dismantling/radiological disposal/site restoration. Fractions are agent assumptions and should be tested. |
| Finance |Stellaris7%,8construction years,30calendar years; predecessor has its own declared common convention | Hold one constant-money convention across branches. Reuse predecessor for direct replay comparability if desired, explicitly changing upstream historical assumptions. Financing once at commissioning; report overnight and financed separately. |

[AGENT] Existing `Lifecycle Cashflow Accounts` in `integrated_lifecycle_costs.sysml` has a hard-coded USD2004 output in its implementation. Reusing it for USD2025 requires an isolated variant or explicitly parameterized currency output; inspect the implementation instead of simply relabelling its report. It supports one periodic replacement stream plus overhaul/terminal; multiple blanket/magnet/primary/conversion streams must be summed natively through reviewed extra event producers, not postprocessed into an external LCOE formula. Event cashflows and annual replacement reserves are alternative representations, never additive.

## Money year and uncertainty basis

- [INHERITED] Primary cooling purchases and fabrication are USD2025 annual-CPI proxies. `mfe_cooling_equipment.sysml:15` declares CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271,2024=313.7,2025=321.9. Finished stainless fabrication nominal310USD2017/kg; retained source-family240/360 alternatives can test that rate, with fixed selected mass. These are analogy/source-rate variations, not validated reactor-pipe quote bounds. Primary piping dominates the common inventory at2.974B and deserves a separate axis.
- [INHERITED] Facilities civil/ventilation are explicit2025 purchasing-power conversions; source proof is `work/orchestration/goals/layout-based-facilities/evidence/cost-source-basis.md`. The85M site-improvement remainder is inherited and must stay labelled. Fuel processing uses the reviewed WI-0702025 CPI assumptions, including assumed1980 containment date.
- [INHERITED] Magnet is mixed: tape20dollars/m is an independent illustrative price with no established year; copper11 and steel6dollars/kg are2026-era assumptions; solder64.441119/kg is a2026 retail proxy; helium and winding use estimated2026 CPI334.4. Winding alone is750415091.660291 and tape731571428.571429 dollars. Source: stellarator_plant.sysml:375–429 and WI-060 design. Proposed2025 treatment: explicitly re-quote assumed tape/material prices in USD2025, replace estimated2026 winding escalation334.4/130.7 with321.9/130.7, and normalize genuinely2026 money by321.9/334.4 only as an explicitly estimated CPI proxy. The old whole magnet amount cannot be called already USD2025.
- [INHERITED] Legacy reactor unit rates/allowances were retained from1costingFE with mixed/unspecified date metadata in model comments. Existing monetary investigation establishes source-declared2025 for CAS23–26 coefficients only (`design-study-component-alternatives/evidence/monetary-basis.md`), not every CAS22 account. Proposed treatment is an explicitly assumed USD2025 inherited account quote with independent multiplier, not a claimed historical escalation. Do not fabricate a money-year conversion where no origin year is known.
- [AGENT proposed] Put uncertain common prices into component groups: magnet procurement/service; primary pipe/fittings and omitted valves/supports/insulation; reactor blanket/shield/vessel; civil/facilities and controls; routine O&M; terminal. Use source-supported rate alternatives where available, plus clearly hypothetical0.5/1/1.5 or similar scenarios and exact preference thresholds. Those factors are stress tests, not credible confidence intervals. Positive omitted scope should receive an explicit allowance, varied to a material reversal threshold; do not omit it merely because common.

## Actual retained defects and safe scope

| Retained failed response or limit | Magnitude / consequence | Relation to matched source study |
|---|---|---|
| facility_occupancy_ok |−4.547e−13m² | Numerical equality defect. Exact intended dimensions/capacity can be retained after a declared arithmetic repair/recheck; no need to buy a materially larger building based on this residual. |
| water_electric_capacity_ok |−3.553e−15MW | Numerical equality defect in replaced conversion equipment; predecessor repair evidence governs its new branch. |
| divertor_heat_ok |10.517841546 vs10MW/m² | Under retained absorbed-alpha0.95,90% total radiation and fixed-R proxy, H50 yields8.583543/9.518262/10.141408 at Q2500/2800/3000. First two pass proxy;3000 remains inadequate. These are analytical checks, not full plasma/divertor qualification. |
| tbr_ok |Lower yield1.186145581 vs required1.191669922 | Conditional mean/lower scenarios and explicit external supply retain uncertainty. A low positive external purchase is not proof that a violated breeding requirement passed. |
| reference_conductor_current_ok |Selected50kA versus allowable23.717404kA; margin−26.282596kA | Material, independent of lower source duty at held field/current. Absolute conductor transfer is already field-extrapolated. Need explicit conditional upgraded conductor/greater inventory allowance and scientific support flag0; do not manufacture a pass by dropping this row. |
| wp_fit_ok |Required x0.37m versus cavity0.25m, margin−0.12m | Material geometry incompatibility; changing it physically affects casing/radial build and cost. A fixed conceptual core offer with an explicit fit/capability assumption and cost range is possible, but is a changed supplied scenario. No claim of native fit can follow until modeled. |
| coil service margin |10FPY source life versus27.0833FPY original productive horizon | Explicit replacement/life assumption needed in full lifecycle, as above. |
| primary pressure rise at Q3000 |304270.726Pa vs300319.896Pa | Fails unchanged offer at predecessor f_loss1.1; do not rank that source point as supported whole plant unless selected offer is changed and priced or another supported operating scenario meets it. |

[AGENT] The cleanest initial comparison is2500MW (and potentially2800MW), with the full selected inventory described as a conditional core offer and unresolved conductor/fit qualifications explicitly retained. The whole-plant question can still be answered conditionally if component choice is isolated and common-core uncertainty does not reverse the conclusion; the result must never be called a fully feasible Stellaris design. At3000MW there are additional directly evaluated upstream equipment limits, so this point needs a reviewed offered-capability alternative or remains unsupported. An assumption about unknown reactor qualification cannot erase a known check without naming that change of scenario.

## Implementation entry points and review conditions

[AGENT] Extend an isolated copy of `models/designs/component_alternatives/plant.sysml`. It already owns source heat, primary-loop work/flow, conversion states, return controls, selected equipment and subsystem electricity/cost. Add upstream supplied-inventory parts and account sums, a source/fusion conversion calculation, existing fuel conservation definitions, explicit upstream electrical ledger, and whole-plant finance. Copy/instantiate reviewed definitions with recorded identity rather than reproducing physics in reporting scripts. Avoid assembling the entire original plasma solver when the study contract supplies source heat.

[AGENT] Variable-role table for design: Qsource/H are supplied operating assumptions; Pfusion, primary flow/loss/work, fuel burn/loss/shortfall and net export are calculated; core geometry/magnet inventory/primary count/ratings/stock/account quotes are supplied choices; flow/pressure/current/fit/heating/fuel-processing limits are requirements or offered capacities; blanket/coil life, replacement scope, availability, price year and finance are explicit service/economic assumptions. No demand-derived value may become a purchased rating or amount automatically. At least one insufficient/sufficient primary offer test and a fixed-hardware load-change test are needed, with exact cost invariance where intended.

[AGENT] Independent review must check active vs dormant output selection, treatment of magnet/fit deficiencies, common source definition, explicit primary ratings at each source, possible controls/vacuum/TF-cooling overlap, CAS24/shared-electric scope, primary-only cooling split, complete startup/replacement/terminal accounting, money-year declarations, and no double financing. Numerical native evidence and scientific-support statements must remain separate.


## T-002 follow-up: explicit alternate magnet offer candidate

[AGENT proposed, not executed] A bounded supplied-inventory probe can test a larger **transversely wider** winding pack while preserving R12.7, a1.3, coil radial allocation0.30m, coil-centre radius3.15m,308 turns and50kA. Exact chosen changes: `magnet__winding_pack__wp_side=0.54`m; `magnet__winding_pack__fit_aspect_ratio=0.19`; `magnet__casing__interior_y=1.30`m. Hold ground insulation0.003m, wall0.025m, clearance0.002m and internal build fractions0/.025. These are deliberately supplied scenario values, not model-sized results or recovered source construction.

[AGENT analytical screen] Existing local-fit equations give required x0.245380543m against0.25m cavity and required y1.279816087m against1.30m cavity. Existing current law at unchanged field gives allowable current53364.158577A against50000A, since tape volume/parallel count grows by2.25. All three values must be checked through native execution before reporting a passed design. This proposal does not change field extrapolation status:24.9T remains above the empirical24T boundary and is supported only under the existing declared extrapolation switch.

[INHERITED code relationships] `mfe_power_core.sysml:188–338` binds these supplied choices into winding-state density, material/tape volume, purchased tape length, insulation inventory, cold volume, stress/strain and fit. At fixed reference turns and circumference, conductor length and winding-operation cost stay constant, while tape and non-tape stock increase2.25×. Winding-pack stress falls with larger supplied section. Cryogenic nuclear heat rises with cold volume; radiation/support-area proxies and cryoplant capability must be re-evaluated. Geometry-owned costs, selected cryoplant capacity/quote and magnetic support mass are not automatically enlarged. `mfe_winding_pack_fit.sysml` explicitly says casing dimensions do not reprice wall mass or resize supports. Wider transverse casing therefore needs a separate chosen casing/support/civil allowance or reviewed inventory update; current model does not prove manufactured global fit.

[AGENT assessment] This is a small set of input changes and a valid candidate for a **conditional modeled offer**, but a substantial cross-section redesign: transverse cavity grows0.4→1.3m. It is not a minor sourced Stellaris correction. It avoids changing coil radial thickness because increasing `coil_t` shifts coil centre, changes winding length and peak field, and can exceed the fixed24.9T ceiling. It also avoids invented material-performance improvement. Recommend one native probe of this explicit offer, with full downstream conductor/fit/strain/cryo/facility checks retained and separately priced extra casing/support scope. Reject or leave unsupported if other capacities fail; do not tune flags or automatically select larger equipment. If the study instead holds the original inventory, its known current/fit failures remain a material prerequisite rather than a certified reactor configuration.
