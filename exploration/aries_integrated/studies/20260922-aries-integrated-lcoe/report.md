# Conditional lifecycle study results

[AGENT executor reading] All 64 declared points completed in one native attempt each at execution commit `f4ea479506cae17d2a9aafe0f914346c555193e7`. Independent all-point verification passes 23,296 scalar and 896 predicate comparisons. Four completed cases retain engineering violations; 60 satisfy all 14 represented checks. Financial definedness does not qualify unsupported physics or supply capability. All report values below are read from `results/cases.json`; derived differences are reporting arithmetic.

## Named supply cases

The assumed integrated baseline produces 423.106794 MW net. Internal exhaust recycling is already accounted for. New feed is net usable extracted breeder supply entering after extraction losses, in kg per calendar year. Its service allowance is additional to existing installed fuel/blanket capital and O&M; it is not a third-party purchase or a demonstrated breeding capability.

| Native case | New feed kg/y | Service million USD2004/y | External T kg/y | Curtailed feed kg/y | Integrated USD2004/MWh | Source-conditioned USD2004/MWh |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| no-breeding-credit | 0 | 0 | 104.667707 | 0.000000 | 1119.408083 | 473.951454 |
| new-feed-50.0 | 50 | 30 | 54.667707 | 0.000000 | 652.808546 | 276.530020 |
| assumed-new-tritium-feed-100 | 100 | 30 | 4.667707 | 0.000000 | 176.686569 | 75.079576 |
| new-feed-110.0 | 110 | 30 | 0.000000 | 5.332293 | 132.238612 | 56.273343 |
| supply-service-10000000.0 | 100 | 10 | 4.667707 | 0.000000 | 170.338276 | 72.393571 |
| supply-service-100000000.0 | 100 | 100 | 4.667707 | 0.000000 | 198.905595 | 84.480597 |

Baseline gross new-tritium need is 104.667707 kg/calendar year. Assumed feed of 110 kg/year crosses the zero-purchase floor and curtails the excess without sales revenue. No point establishes that this extraction capability exists or that increasing it has the declared service cost.

## Complete baseline contributions

| Contribution USD2004/MWh | No credit | Feed100 / service30m | Source-conditioned feed100 |
| --- | ---: | ---: | ---: |
| Financed capital | 93.155987937 | 93.155987937 | 39.570401512 |
| Routine O&M | 22.219025582 | 22.219025582 | 9.401020682 |
| External tritium | 996.691911412 | 44.447957897 | 18.806232970 |
| Deuterium | 0.022061004 | 0.022061004 | 0.009334161 |
| Consumables | 1.587073256 | 1.587073256 | 0.671501477 |
| Grid imports | 0.000000000 | 0.000000000 | 0.000000000 |
| New-feed service | 0.000000000 | 9.522439535 | 4.029008864 |
| Blanket/divertor/LiPb events | 3.301126391 | 3.301126391 | 1.396729004 |
| Other major overhaul | 1.516445832 | 1.516445832 | 0.745683408 |
| Gross terminal disposal/decommissioning | 1.143064971 | 1.143064971 | 0.562080468 |
| Salvage credit | -0.228612994 | -0.228612994 | -0.112416094 |
| Total | 1119.408083391 | 176.686569410 | 75.079576454 |

Constant USD2004, real discount 5%, 40 calendar operating years and availability .85 define these baseline values. Overnight capital receives midpoint construction financing once over six years. Operating energy and recurring charges fall at each year end; dated replacement events exclude an event exactly at terminal life. The annual replacement reserve is published but excluded from LCOE. A separate 5%-of-capital overhaul at year 20 covers non-blanket scheduled refurbishment. Terminal gross liability is 10% of capital and salvage 2%, both at year 40; availability already includes downtime. No additional replacement outage penalty is charged.

| Native baseline account | Value |
| --- | ---: |
| cost_ledger.overnight (USD2004) | 4350208470.000000000 |
| lifecycle_accounts.financed_capital (USD2004) | 5035910080.083750725 |
| lifecycle_accounts.idc (USD2004) | 685701610.083750725 |
| lifecycle_accounts.annual_energy (MWh/y) | 3150453.188937971 |
| lifecycle_accounts.pv_energy (discounted MWh) | 54058898.323203810 |
| replacement.event_count (events) | 6.000000000 |
| replacement.event_cost (USD2004/event) | 72231350.000000000 |
| lifecycle_accounts.pv_replacement (USD2004) | 178455255.937462449 |
| lifecycle_accounts.gross_terminal (USD2004) | 435020847.000000000 |
| lifecycle_accounts.salvage (USD2004) | 87004169.400000006 |

## Financial sensitivity

The following ranges include the matching baseline and the declared changed points. Windows differ between axes; spans are neither probabilities nor a ranking independent of chosen bounds. All amounts are conditional USD2004/MWh.

| Axis | Supply scenario | Observed minimum | Observed maximum |
| --- | --- | ---: | ---: |
| discount | no-credit | 1062.967327 | 1212.769362 |
| discount | named-feed | 120.245813 | 270.047848 |
| construction | no-credit | 1106.723740 | 1128.956572 |
| construction | named-feed | 164.002226 | 186.235058 |
| terminal | no-credit | 1118.836551 | 1120.551148 |
| salvage | no-credit | 1119.065164 | 1119.636696 |
| overhaul_fraction | no-credit | 1117.891638 | 1120.924529 |
| overhaul_date | no-credit | 1118.822604 | 1119.827049 |
| life | no-credit | 1110.088437 | 1155.321083 |
| life | named-feed | 167.366923 | 212.599569 |
| availability | no-credit | 1106.382473 | 1171.115875 |
| availability | named-feed | 149.290942 | 262.894802 |
| magnet_inventory_price | no-credit | 1116.065230 | 1122.750936 |
| unallocated_source_scope_price | no-credit | 1118.943245 | 1120.337760 |
| tritium_price | no-credit | 448.398872 | 3467.940324 |
| routine_om | no-credit | 1108.298571 | 1141.627109 |
| consumables | no-credit | 1118.138425 | 1122.582230 |
| replacement_life | no-credit | 1118.034303 | 1125.340663 |
| replacement_factor | no-credit | 1117.757520 | 1122.709210 |
| new_feed | named-feed | 132.238612 | 652.808546 |
| supply_service | named-feed | 170.338276 | 198.905595 |
| density_amplitude | named-feed | 176.686569 | 398.980272 |
| he_hx_area | no-credit | 1119.408083 | 1215.075689 |

External tritium price dominates the selected no-credit window: its 10–100 million USD2004/kg endpoints produce 448.398872–3467.940324 USD2004/MWh. This is a broad assumed supply-price range, not a dated market forecast. Zero real discount is supported; the zero-discount and tiny-rate cases approach the same dated-cashflow limit. At zero discount, construction duration produces no financing increment. Terminal, salvage, overhaul and replacement contributions remain charged explicitly through the chosen convention.

## Fixed supply under availability and demand changes

| Native case | Availability | Density amplitude m^-3 | Fixed feed kg/y | Net MW | External T kg/y | Curtailed kg/y | USD2004/MWh |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| availability-0.6-feed | 0.60 | 5e+20 | 100 | 423.106794 | 0.000000 | 25.951554 | 185.683378 |
| availability-0.75-feed | 0.75 | 5e+20 | 100 | 423.106794 | 0.000000 | 7.579997 | 149.290942 |
| assumed-new-tritium-feed-100 | 0.85 | 5e+20 | 100 | 423.106794 | 4.667707 | 0.000000 | 176.686569 |
| availability-0.95-feed | 0.95 | 5e+20 | 100 | 423.106794 | 16.915411 | 0.000000 | 262.894802 |
| density-4.5e+20-fixed-feed | 0.85 | 4.5e+20 | 100 | 140.230696 | 0.000000 | 15.112336 | 398.980272 |
| density-5.5e+20-fixed-feed | 0.85 | 5.5e+20 | 100 | 735.759323 | 26.529859 | 0.000000 | 221.325165 |

Each of these points fixes independently supplied feed at 100 kg/calendar year and service at 30 million USD2004/year; neither is multiplied by availability again. Hardware, capacities and purchase choices remain fixed. Lower availability/demand can eliminate external purchases, while higher operation crosses the purchase floor and incurs expensive supplemental tritium. The non-monotone LCOE response is therefore conditional fuel-boundary arithmetic, not a reliability or plasma optimum. The density changes also alter net electricity, which reaches the native denominator.

## Preserved engineering failures and refusals

| Completed adverse case | Net MW | USD2004/MWh | Failed qualified constraints |
| --- | ---: | ---: | --- |
| nominal-source-assumed | 796.005288 | 767.420931 | `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07`=violated |
| literal-Lyon-source-input | 807.016660 | 756.949825 | `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07`=violated |
| literal-Raffray-accounting | 805.910865 | 737.855370 | `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535`=violated; `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07`=violated |
| he-area-5000.0 | 389.195517 | 1215.075689 | `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07`=violated |

The 5000 m2 helium exchanger case retains its heat-removal failure while producing finite financial output. The explicitly purchased 75000 m2 case passes all represented checks and changes capital through the selected-area price law. The three inherited source cases remain distinct, with their actual thermal failures; no source electricity is substituted into their integrated headline.

Eleven author stock-runtime financial refusal attempts are retained separately in diagnostic-refusals.json. The additional isolated diagnostic route retains full upstream outputs for nonpositive energy, negative rate and source double-financing controls, plus a baseline parity case. It has its own copied runtime/provenance, not a stock StudyRunner completion claim. At nonpositive energy, native calculated power is -571.893206 MW; 505 numeric outputs and 14 predicate records remain, while integrated LCOE is blocked by its dependency. The supplied source-comparison branch can remain defined independently. The negative-rate control blocks both financial branches; the nonzero source-construction guard blocks only the source-financing branch. No refused case is assigned a sentinel price or included in the 64 finite rows.

## Source comparison

Source values and their original page references are retained in source-evidence/source-boundary.md and its reviewed page images. The source-conditioned branch uses already-financed capital and supplied 1000 MW with zero second IDC. It retains the integrated case's fuel throughput, rather than reconstructing source fusion/fuel physics. It holds each selected case's recurring expenses and blanket events; terminal/salvage/overhaul fractions stay fixed, so their absolute capital-based amounts change. It does not reconstruct the source financial convention.

| Quantity | Published source | Native integrated feed100 | Native source-conditioned feed100 | Difference / comparability | Units / price year / status |
| --- | ---: | ---: | ---: | --- | --- |
| Complete LCOE | 77.6 | 176.686569 | 75.079576 | Integrated +99.086569; source-conditioned -2.520424; boundaries differ | USD2004/MWh; source reported, model calculated |
| Net power | 1000 | 423.106794 | 1000 | Integrated -576.893206; source branch supplied | MW; source reported / integrated calculated / comparison supplied |
| Annual energy | 7446000 | 3150453.188938 | 7446000.000000 | Integrated denominator differs; source denominator assumes source85% availability | MWh/year; source-derived and native calculated |
| Capital boundary | 5055773960 inclusive | 4350208470.00 overnight; 5035910080.08 financed | 5055773960.00 already financed | Different capital scope and financing convention; not one comparable overnight estimate | USD2004; source-derived inclusive vs native provisional cost |
| Life | 40 full-power years, ambiguous printed availability treatment | 40 calendar years | 40 calendar years | Unmatched time convention | Years; source reported / model assumed |
| Terminal | 0.5 | Gross terminal and salvage shown below | Gross terminal and salvage shown below | Unmatched: source USD1992 per energy versus new USD2004 dated capital fractions | Source USD1992/MWh; model USD2004 event |
| Annual external T purchases | Not established by inspected source (source fuel description identifies D) | Charged remaining shortfall | Same recurring amount held | Scope difference, no zero-source-expense claim | USD2004/year; calculated under assumed supply |
| Annual O&M | 80,893,344 reverse-derived | 70000000.00 | 70000000.00 held | Source amount is77.6×14%×7,446,000; target-derived, not independently reported | USD2004/year; source target-derived / model supplied allowance |
| Operating replacement total | 966,000,000 printed; rounded75m×13=975m | 433388100.00 across 6 events | 433388100.00 held | Unmatched FPY/calendar life and dated event scope; source lifetime figure is not discounted PV | USD2004; source reported / native selected schedule |

| Capital-scaled allowance at same fractions | Integrated USD2004 | Source-conditioned USD2004 |
| --- | ---: | ---: |
| gross_terminal | 435020847.000000 | 505577396.000000 |
| salvage | 87004169.400000 | 101115479.200000 |
| other_overhaul_cost | 217510423.500000 | 252788698.000000 |

The source-conditioned 75.079576 USD2004/MWh is 2.520424 below 77.6, but that proximity does not identify the source's rate, calendar convention, supply assumption or expense schedule. The no-credit source-conditioned value is 473.951454 USD2004/MWh. WI-088 partial budget allocations remain partial and are not competing full LCOEs.

## Verification and limits

The frozen native evidence supplies every advertised production quantity. Independent checks cover 364 of 546 numeric outputs per point and rederive all 14 predicates; unchanged constants/pass-through values are not scientific validation. The residual-magnitude and IDC-only absolute tolerances are declared before study execution. Tiny-rate IDC tolerance covers cancellation at the capital scale; other financial channels retain the standard relative comparison. Initial oracle binding/schema preparation corrections are preserved and did not change the model or study inputs.

All finance/cost/feed assumptions are sensitivity-only. The area cases support bounded purchased-equipment accounting/capability comparisons; density cases support fixed-hardware operating propagation. Neither establishes geometry/hydraulic qualification, actual breeding/extraction capability, a market supply path or an optimized plant. Whole-plant scientific qualification remains unsupported. Exact replay and identities are retained in replay.md and results/execution-context.json.
