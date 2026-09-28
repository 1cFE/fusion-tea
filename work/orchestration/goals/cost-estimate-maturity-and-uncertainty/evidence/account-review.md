# Current estimate and functional account review

[AGENT] Author investigation, 2026-09-19. This is an account map and arithmetic review, not the independent R12.S grade. No model or historical study changed. No uncertainty study was run. All dollar amounts below are USD; tables use millions unless stated otherwise. The available prices have mixed years and scope, so “USD 2025 plant cost” would be an unsupported label.

## Finding

The current estimate is $12,219.310 million of direct accounts, $17,918.171 million overnight capital, and $271.584320/MWh headline levelized electricity cost. Cooling contributes 52.960% of the direct subtotal. Magnets contribute 13.973% and facilities/site 6.545%. Together those three account families contribute 73.478% and already have functional producers beneath their broad totals. The cooling pipe and exchanger accounts alone contribute 47.385% of direct cost. They price engineered quantities rather than arbitrary portions of a lump.

[AGENT] The functional-detail component of the existing S3 criterion is supportable from the implemented hierarchy. The inherited codes use longer account identifiers, but the depth is functional: heat transport separates machines, primary piping, exchangers, secondary piping, inventories and spares; magnet procurement, winding and supports have separate producers; facilities have 25 separately measured civil occurrences plus ventilation and site allowance. Requiring a new three-character label or mechanically dividing blanket and shield prices would not improve this evidence. Blanket/first wall and shielding are already separate functions below reactor power-core capital, although their price methods remain coarse. The consequential engineering and procurement gaps below belong in maturity and uncertainty assessment. The complete S3 grade remains open until those components and independent review are delivered.

## Exact estimate identity

| Item | Identity |
|---|---|
| Audited model | `2a50d3ec40e587af25beadaa9bd26c305b9ac11d`, WI-070 |
| Frozen study | `exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/`, committed `2bae7fb7` |
| Package name | `stellarator_tea` |
| Preserved producer package | That study's `preparation/producer-package/` |
| Semantic fingerprint | `37ca31ff0412f56a67301fa4e714b1dba2e74df6788348ce97dd5ee64d98d62f` |
| Executable fingerprint | `3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f` |
| Candidate/indicator pin | `50c9d4b9b3bf16fdb00e5c726011f2b434bfa0ba8970569795372a12364c312b` |
| Evaluated reference | Frozen `results/baseline_result.json`, native case `stellarator-baseline-point-v1:c0000` |
| Baseline result SHA256 | Recorded in [account-extraction.json](accounts/account-extraction.json) |

The current generated package matches all 370 retained producer-package files byte for byte, excluding Python caches. The tracked canonical/staged model trees have no differences against the audited model revision. The [reproducible extraction](accounts/inspect_accounts.py) records each compared package file and its SHA256. This is a file comparison and reuse of previously verified execution, not a new cold execution. Prior final independent verification remains in `work/orchestration/goals/throughput-based-fuel-processing-costs/evidence/final-review-and-grade.md`.

This reference integrates all three completed upstream goals: installed cooling, layout-based facilities and throughput-based processing. The earlier cooling answer's selected eighteen-circuit result and historical r2 fourteen-circuit controls are different input sets. Their totals must not be mixed into this estimate. Likewise the magnet answer's prior plant LCOE is historical; the magnet component amount alone remains applicable at the present reference.

## Fixed plant and financial assumptions

All effective inputs, including frozen defaults and the baseline override, are retained in [fixed-inputs.json](accounts/fixed-inputs.json). This avoids rounding design coordinates or silently adopting later defaults.

| Assumption | Current reference |
|---|---|
| Plant modules | 1 |
| Major/minor plasma radii | 12.7 / 1.3 m |
| Central density and ion temperature | 5.06×10²⁰ m⁻³; 14.63 keV |
| Cooling circuit count | 14; active equipment-cost and secondary-energy modes |
| Facility selectors | Layout costs and capacity mode enabled |
| Magnet sizing | Fixed reference pack, sizing mode 0; 48 coils |
| Fuel processing | Adopted conventional mode enabled; 5% single-pass burn; capacity margin and price multiplier both 1 |
| Operating period | 30 years |
| Construction duration | 8 years |
| Discount/interest rate | 7% |
| Annual operating-cost escalation | 2% |
| Direct contingency | 10% |
| Indirect fraction | 20% of post-contingency direct subtotal, multiplied by construction duration / 6 years |
| Routine replacement outage | 0.5833333333333334 years per event |
| Additional unplanned downtime | 0 |
| Availability | Live lifecycle calendar; 0.9027777777777779 |
| Peak-wall fluence life | 4.5239260339489915 full-power years; five bundled blanket/divertor replacement events |
| Cooling service lives | Machines 10 years, tube bundles 15 years; two machine events and one bundle event within the horizon |

This is a priced reference design with retained engineering failures. The native baseline has 21 satisfied and four violated predicates: divertor heat, reference conductor current, tritium-breeding adequacy and winding-pack fit. Package diagnostic applicability limits also remain; a count of authored predicates does not cover all equipment qualification questions. No feasible-design claim or filtering follows from this account review.

## Disjoint direct functional map

Each row enters the direct subtotal once. The [CSV](accounts/functional-accounts.csv) contains exact numbers, direct-cost fractions and active channel names. Prefix native channel names with `stellarator_09__stellaris__` to resolve them in the frozen output. Model bindings are in `models/designs/generic_mfe/mfe_plant.sysml:437` through the direct rollup at line 520. Instance prices and selected modes are in `models/designs/stellarator_09/stellarator_plant.sysml`.

| Account | Function and active producer | USD million | Direct share |
|---|---|---:|---:|
| C220200 | Cooling equipment → `heat_transport.cooling_selection.cost` | 6,471.347146 | 52.960% |
| C220103 | Magnet procurement/winding/supports → `magnet.magnet_capital_rollup.capital_cost` | 1,707.443242 | 13.973% |
| CAS21 | Facilities/site → `buildings.facility_accounts.cost` | 799.758796 | 6.545% |
| C220101 | Blanket and first wall → `blanket.blanket_cost.cost` | 719.155016 | 5.885% |
| C220111 | Reactor equipment installation → `installation.cost` | 513.403040 | 4.202% |
| C220102 | In-reactor shield → `shield.shield_cost.cost` | 452.529517 | 3.703% |
| CAS23 | Turbine plant → `turbine.turbine_cost.cost` | 275.925383 | 2.258% |
| C220104 | Heating plant → `heating.heating_cost.cost` | 264.145000 | 2.162% |
| C220110 | Remote-handling equipment allowance → `remote_handling.cost` | 166.806873 | 1.365% |
| C220106 | Vessel shell → `vessel.vessel_cost.cost` | 120.966521 | 0.990% |
| CAS24 | Electrical plant → `electric_plant.electric_cost.cost` | 117.530828 | 0.962% |
| CAS25 | Ultimate heat rejection → `heat_rejection.heat_rejection_cost.cost` | 115.939532 | 0.949% |
| C220108 | Divertor → `divertor.divertor_cost.cost` | 109.109123 | 0.893% |
| C220107 | Power supplies → `power_supplies.power_supplies_cost.cost` | 92.824313 | 0.760% |
| C220700 | Central/supervisory controls → `inc_cost.cost` | 81.921417 | 0.670% |
| CAS26 | Miscellaneous plant → `misc_plant.misc_cost.cost` | 71.538729 | 0.585% |
| C220300 | Cryoplant and auxiliary cooling → `cryoplant.aux_cooling.cost` | 35.116270 | 0.287% |
| C220105 | Nonmagnet structural allowance → `structure.structure_cost.cost` | 34.184967 | 0.280% |
| CAS27 | Special-material inventory → `special_materials_capital` | 23.815042 | 0.195% |
| C220500 | Fuel-process equipment and installation → `fuel_cycle.processing_cost.cost` | 22.786229 | 0.186% |
| C220600 | Other reactor equipment → `other_rpe.cost` | 11.581793 | 0.095% |
| C220400 | Waste-handling allowance → `waste.cost` | 6.481503 | 0.053% |
| CAS28 | Digital-twin allowance → input `cas28_capital` | 5.000000 | 0.041% |
| **Direct total** | **CAS21 + CAS22 + CAS23–28** | **12,219.310281** | **100%** |

The current nonmagnet structure allowance is $34.184967 million; the older magnet ledger's $34.155617 million belongs to its older power point. Exported legacy prices are diagnostics: old cooling $206.829 million, old fuel handling $120.746 million, old buildings $652.635 million, and the old aggregate magnet price $6,323.470 million do not enter the current direct sum. Summing every output whose name includes “cost” would double count these and nested subtotals.

### Where the largest accounts get their detail

| Cooling child | USD million | Quantity/source character |
|---|---:|---|
| Primary pipe and fittings | 2,974.043934 | Modeled pipe/fitting stainless mass; finished nuclear fabrication/delivery rate; field installation separately added |
| Exchangers | 2,816.099941 | Fourteen source-scale exchanger constructions; tube/shell/tube-sheet mass; separate site labor/material |
| Primary helium circulators | 442.174445 | Pressure and shaft-duty transfer, active machine count, one supplier-design fee, setting labor |
| Secondary piping | 219.659255 | Explicit length/diameter/wall/material; separate installation |
| Uninstalled spares | 12.102805 | One spare machine of each type; no initial installation |
| Initial inventories | 4.241578 | Helium and salt quantity × separate commodity prices |
| Secondary pumps/motors | 3.025189 | Flow/head and motor-power price relations; material/type factors and installation |
| **Cooling total** | **6,471.347146** | **Supply 5,229.736988 + site installation 1,241.610158** |

Native child names and sums are in `account-extraction.json.children.C220200`. Engineering/source scope comes from `work/orchestration/goals/installed-cooling-equipment-costs/answer.md` and its `evidence/round3/account-boundary-map.md`. Primary piping and exchanger steel share the same finished-fabrication source and CPI transfer. Their price uncertainty cannot reasonably be sampled independently without evidence for that separation.

The magnet's $1,707.443242 million comprises complete tape $731.571429 million; winding operations $750.415092 million; external copper/solder/steel/helium $15.954709 million; conditional additional sheet stock $0.421132 million; and electromagnetic supports $209.080881 million. These are separate physical/procurement or operation producers. Supports are one all-in charge: adding a casing-floor price or fabricating an unsupported raw-material/labor split would break the boundary. Tape constituents are already purchased in the complete tape. See `work/orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md` and the native `children.C220103` extraction.

Facilities comprise civil $614.376866 million, ventilation $100.381930 million and site improvements $85 million. Civil quantities are separately costed for 25 actual building/link occurrences. Four maintenance wings each cost $94.671892 million; the reactor hall costs $73.273944 million, and the cooling annex $66.903908 million. Every civil occurrence, including substructure/superstructure diagnostics, remains in the frozen baseline; `children.CAS21` retains the disjoint final civil amounts. Buildings exclude cooling equipment, in-reactor shielding and the separate handling/waste equipment allowances. See `work/orchestration/goals/layout-based-facilities/answer.md` and `evidence/inventory.md`.

Fuel processing further separates cleanup, distillation, transfer pumps and limited containment. Native capital $20.443420 million plus installation $2.342810 million equals $22.786229 million. Their local controls stay in this account; central/plasma controls stay in C220700. The whole old allowance is replaced once. See `work/orchestration/goals/throughput-based-fuel-processing-costs/answer.md` and WI-070's `evidence/account-reconciliation.md`.

## Capital, contingency and financing

| Capital layer | USD million | Inclusion |
|---|---:|---|
| Direct accounts before contingency | 12,219.310281 | Disjoint table above |
| CAS29 contingency | 1,221.931028 | Exactly 10% of direct accounts |
| CAS20, including contingency | 13,441.241309 | Direct + CAS29 |
| CAS10 preconstruction | 16.901537 | $16 million fixed plus parcel land; outside CAS29 and CAS30 bases |
| CAS30 indirect | 3,584.331016 | 0.20 × CAS20 × 8/6; broad project engineering/procurement/construction-services allowance |
| CAS40 owner | 41.382901 | Existing net-power relation |
| CAS50 supplementary | 834.314251 | Freight, spares, tax, insurance, startup fuel and decommissioning allowance |
| **Overnight capital / native total_capital** | **17,918.171014** | **CAS10 + CAS20 + CAS30 + CAS40 + CAS50** |
| CAS60 uniform-spend construction interest | 5,061.441111 | Separate diagnostic/comparison line; excluded from native total_capital |
| Comparison-form financed capital | 22,979.612125 | Overnight + CAS60; used only in comparison-form annual charge |

CAS50 applies freight at 1.5%, spares at 3% of CAS23–28, tax at 1% of CAS20, insurance at 1.5% of CAS20+CAS30, and the power-scaled $40 million startup and $272 million decommissioning bases. Its own contingency parameter is zero. The extraction re-derives the six source formula terms and their sum. It does not call them independently priced equipment.

Freight's $7,429.964364 million base excludes delivered initial cooling purchases, installed facilities with associated project contingency, and fuel direct installation with associated contingency. Generic reactor installation is 14% of power-core plus remote handling, excluding the new cooling/fuel installation. Facilities already include construction labor. These selected boundaries prevent the known additive duplicates; they do not establish that ambiguous source packages cover every task.

The $3,584 million indirect account is 20.004% of overnight cost. Its size warrants separate maturity/uncertainty disclosure. It is a transparent project-level factor tied to construction duration, not a measured engineering-hours or procurement-service estimate. Subdividing this factor into percentages with new labels would add no evidence. The same construction-duration input changes indirects, both financing formulas, and operating-cost escalation; those dependencies must remain shared.

CAS29 is a deterministic allowance, not a source-calibrated uncertainty distribution. Any new ranges should state whether contingency is retained. “Raw direct” means before this allowance; “overnight” here includes it and the resulting indirect/supplementary consequences. A second independent contingency uplift would overlap its existing purpose. Removing or redefining it would be a financial-policy decision; this investigation leaves it intact. Mixed source years preclude calling existing escalation a whole-plant constant-dollar normalization.

## Annual expense and electricity cost

| Quantity | Current result |
|---|---:|
| Routine raw O&M | $55.143720 million/year |
| Added raw coolant makeup | $0.004242 million/year |
| CAS71 levelized routine O&M plus makeup | $79.360459 million/year |
| In-vessel scheduled replacement annual equivalent | $138.326405 million/year |
| Cooling replacement annual equivalent | $55.673508 million/year |
| CAS72 total replacement annual equivalent | $193.999913 million/year |
| CAS70 = CAS71 + CAS72 | $273.360371 million/year |
| Raw / levelized fuel purchases | $0.550716 / $0.792506 million/year |
| All levelized annual noncapital expense | $274.152877 million/year |
| Net electrical power | 1,008.898406 MW |
| Annual-energy denominator | 7,978,704.890196 MWh/year |
| Headline annual capital charge | $1,892.738264 million/year |
| Headline LCOE | **$271.584320/MWh** |
| Comparison-form annual capital / LCOE | $1,851.844295 million/year / **$266.458931/MWh** |

LCOE is the estimated levelized cost per unit of lifetime electricity. The headline uses overnight capital × `(1.07)^4` × capital-recovery factor `0.0805864035111112`, then adds the annual expense and divides by `8760 × net MW × availability`. It does not add CAS60 first. The separate comparison uses `(overnight + CAS60) × capital-recovery factor`. Both retain inherited conventions; their difference is financing treatment, not physical design. Implementations: `models/library/analyses/mfe_lcoe_dcf.sysml:4`, `models/designs/generic_mfe/mfe_plant.sysml:632` and `:745`.

The calendar couples replacement dates, replacement expense and electricity availability. Cooling replacements are assumed to coincide with existing outages. That assumption gives no extra outage penalty; it is not observed reliability. Magnet life, component qualification and unplanned failures remain limitations. A quantified change to availability should use the common producer, not separately perturb electricity and replacement costs as independent variables.

## Monetary basis and scope still missing

| Family | Existing monetary evidence | Material unresolved scope or limitation |
|---|---|---|
| Cooling | 1978 BNL helium-machine basis; 2017 ANL finished nuclear stainless basis; Seider CE500/2006 liquid pump basis; commodity bases; CPI transfer to 2025 purchasing power | Pressure-boundary/material qualification, scalable exchanger geometry, source-to-plant pump applicability, routing, valves/supports/insulation, tanks, trace heating, cover gas, additional inventory, field replacement outages and disposal |
| Magnet | Illustrative $20/tape-m; winding 1990 coefficient to estimated 2026 CPI; helium 2024 to estimated 2026; nominal catalog and inherited mixed-year rates | Ground insulation, free resin/adhesive, cable manufacture, joints, assembly, tests, waste/yield/rework/spares, all-in support coverage, stock/winding overlap |
| Facilities | Civil TIMCAT USD2018 and historical PROCESS ventilation USD1990, each transferred to 2025 CPI proxy; site allowance inherited | Qualified envelopes/load/radiation shielding, cranes/carriers/doors/rails and other services, original source ton-unit ambiguity, installed supplier quotations |
| Fuel processing | Historical ORNL rows with raw capital/installation and individual chronology, transferred to 2025 CPI | Storage, blanket extraction/conditioning, wider containment/effluent/emergency systems, fueling hardware, torus vacuum pumping, full inspection/design, recurring process expense/replacements; feed-purity and reliability conditions |
| Blanket/shield/vessel and conventional accounts | Existing volume/power coefficients and account structure | Inherited mixed or unresolved price years; no uniform vendor-quote support; blanket/first-wall fabrication and detailed conventional scope not established |
| Project indirect, owner and supplementary | Fractions and power-scaled allowances | Detailed engineering procurement plan, schedule, labor and vendor scopes; startup-fuel price still follows power rather than the computed startup inventory |

Sources for the table are the four upstream answers and ledgers cited above, plus the current account definitions. No barred source was opened. C220107 retains the protocol's already-disclosed ARIES-lineage library exception; this investigation neither imports original barred facts nor makes a new calibration claim. The published r2 monetary rules and archive remain untouched.

Steam generation at the salt/power-conversion interface has unverified inclusion in CAS23. Broad turbine and handling allowances are not evidence that all omitted equipment is priced. Missing scope is outside any numerical range until a supported quantity/rate is supplied; it is not a zero-cost random variable. Fixed-design source-interpretation alternatives will leave these omissions unresolved.

## Supported interpretation controls for the next method review

[AGENT] These existing controls can represent discrete ambiguities at fixed physical design. They do not establish an all-in uncertainty range. Full native parameter keys use prefix `stellarator_09__stellaris__`.

| Native suffix | Baseline and documentary alternatives | Dependency and boundary |
|---|---|---|
| `buildings__tonne_interpretation_kg` | 907.18474 baseline; 1000 alternative | Source TN interpreted as short ton or metric tonne. Applies jointly to the source rebar pricing for all 25 civil occurrences; physical quantities remain fixed. See facilities `evidence/civil-cost-basis.md`, model instance line 1643. |
| `fuel_cycle__processing_containment_cpi` | 82.4 baseline; 65.2 / 96.5 alternatives | 1980 / 1978 / 1982 expenditure-date CPI choices from the already-reviewed chronology. One input changes both containment capital and its direct installation; the package's throughput ratio and common 0.3 exponent remain fixed. Frozen study `execution/proposals.py:43`, model instance line 1454. |
| `magnet__winding_pack__insulation_sheet_price` | 61.67720668774671 USD/m² baseline; zero additional charge if included in winding | Same physical sheet inventory in both cases. Zero represents an alternative account boundary, not free or absent insulation. Existing winding charge remains. See magnet account ledger, model instance line 468. |

All three propagate through their shared native account rollups, contingency, indirects, supplementary bases and annual capital charge. They should not acquire independent random draws for different occurrences. No new source-price error bars or probabilities are inferred from their finite alternatives.

## Verification and conclusion boundaries

Run `.codex-test/run python work/orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/accounts/inspect_accounts.py`. It reads retained native results, writes only this account evidence directory, and checks twelve identities: disjoint direct sum, four child-family sums, CAS20, overnight, CAS50, CAS70, annual expenses, headline LCOE and comparison LCOE. All pass within 0.0001 in their respective output units. Package-file comparison reports zero mismatches. The full exact inputs, all 25 verdicts, native channel mappings, source hash and arithmetic residuals are preserved.

The underlying study's verification is inherited: 18,680 mapped scalar and 500 predicate comparisons across twenty cases, with twenty-two numeric channels outside its independent map. Static L2/L6 failures and omitted integration read-set coverage remain disclosed in the upstream final review. This extraction neither erases those limits nor certifies source applicability. It supplies the functional/account baseline for the separate maturity method, uncertainty treatment and fresh independent R12.S assessment.
