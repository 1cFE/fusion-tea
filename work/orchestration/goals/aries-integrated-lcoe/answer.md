# Conditional integrated ARIES LCOE

[AGENT] **The positive integration goal is met under declared assumptions.** [Independent final review](evidence/final-review.md) passes. The generated native package produces complete conditional lifecycle prices and the sealed 64-point study passes all-point verification. The owner authorized formal closure on 2026-09-22; the goal and WI-091 are closed.

## Delivered boundary and interpretation

The evolving native assembly is `models/designs/aries_cs_integrated/plant.sysml`, package `exploration/aries_integrated/aries_integrated/`. The 423.106794 MW case remains the **assumed integrated baseline**. Equipment choices are supplied independently of demand; scientific magnet, breeding, deposition, hydraulics, materials and machine-map qualifications remain unsupported.

The financial convention uses constant USD2004, an assumed 5% real rate, six-year construction represented by midpoint spending, 40 calendar operating years and 85% availability. The generated graph charges overnight capital with construction financing once; annual O&M, fuel, consumables and imports; dated blanket replacements; an explicit other-equipment overhaul allowance; and terminal decommissioning/disposal less declared salvage. Availability includes downtime. The alternative replacement reserve is excluded. See [assumptions and ownership](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/design.md).

“No breeding credit” means no credit for new usable tritium supply. Internal exhaust recycling remains in the modeled fuel loop. The inherited recovery input represents NEW usable T feed outside that loop, after extraction losses, in kg per calendar year. It must never include exhaust that was already credited through the permanent-loss calculation. The named 100 kg/year scenario includes a separate assumed 30 million USD2004/year supply-service charge. That charge and feed are independent scenario assumptions; they do not qualify breeding or define a recovery-equipment performance/cost law. They are not optimization controls.

## Baseline accounting

| Native contribution, USD2004/MWh | No breeding credit | Assumed new feed: 100 kg/year, 30 million USD/year charge |
|---|---:|---:|
| Financed initial capital | 93.155988 | 93.155988 |
| Routine O&M | 22.219026 | 22.219026 |
| External tritium purchases | 996.691911 | 44.447958 |
| New-feed service | 0 | 9.522440 |
| Deuterium and consumables | 1.609134 | 1.609134 |
| Dated blanket replacements | 3.301126 | 3.301126 |
| Other-equipment overhaul | 1.516446 | 1.516446 |
| Gross terminal decommissioning/disposal | 1.143065 | 1.143065 |
| Salvage credit | −0.228613 | −0.228613 |
| Imported electricity | 0 | 0 |
| **Complete conditional LCOE** | **1119.408083** | **176.686569** |

These values come from the generated native outputs retained in WI-091 development-cases.json and independently checked in [implementation-review.md](evidence/implementation-review.md). Combined deuterium/consumables is a presentation sum of two native contribution channels. Annual net electricity is 3,150,453.189 MWh; discounted energy at commissioning is 54,058,898.323 MWh. Gross annual T makeup is 104.667707 kg, composed of burn, permanent exhaust loss after recycling, and calendar-time decay of maintained stock. The 100 kg/year feed leaves 4.667707 kg/year external purchases. Initial stock is purchased once in capital.

Overnight capital is 4,350,208,470 USD2004. One midpoint construction adjustment adds 685,701,610.084 USD2004, giving 5,035,910,080.084 at commissioning. Six blanket/divertor/LiPb replacements occur strictly before retirement; their discounted expense is 178,455,255.937 USD2004. A separately declared 217,510,423.5 USD2004 equipment overhaul occurs in year 20. Gross terminal cost is 435,020,847 USD2004 and salvage is 87,004,169.4 USD2004, both at year 40. Terminal scope includes dismantling, radiological handling, final blanket/LiPb/fuel disposition and site restoration. The source’s 0.5 USD1992/MWh terminal allowance is not added to this event or silently converted.

## Declared supply scenarios and sensitivities

All following native cases hold the same assumed physical baseline. “New feed” is additional usable tritium outside the exhaust-recycling loop; its charge is an independent scenario input, not a fitted equipment-cost law.

| New feed, kg/calendar year | Annual incremental supply charge, USD2004 | Complete LCOE, USD2004/MWh |
|---:|---:|---:|
| 0, no breeding credit | 0 | 1119.408083 |
| 50 | 30 million | 652.808546 |
| 100 | 30 million | 176.686569 |
| 110 | 30 million | 132.238612 |

The 110 kg/year case exceeds the baseline makeup requirement; external purchases clip at zero, excess feed is curtailed and no resale credit is granted. Holding the charge fixed while varying supplied feed tests an unsupported supply assumption. It is not a free equipment upgrade or an optimum. The finite values depend strongly on the assumed 30 million USD2004/kg external T price and the unqualified new-feed boundary.

The 64-point native study verifies every point over 364 scalar channels and 14 predicates. Four completed points retain engineering failures: the three inherited source controls and undersized helium exchanger. Separate stock-native refusal receipts and isolated native diagnostics retain nonpositive-energy and unsupported-financial cases; none is silently removed from the finite study set after execution.

| Assumption window, other inputs held as declared | No-credit LCOE endpoints | 100 kg/year feed, 30 million/year charge endpoints |
|---|---:|---:|
| Real rate 0–10% | 1062.967–1212.769 | 120.246–270.048 |
| Construction duration 0–10 years | 1106.724–1128.957 | 164.002–186.235 |
| Calendar operating life 20–60 years | 1155.321–1110.088 | 212.600–167.367 |
| Availability 0.60–0.95 | 1171.116–1106.382 | 185.683–262.895 |

These are unequal engineered windows, not probabilities. At fixed 100 kg/calendar-year feed, the availability response changes direction around the external-purchase floor; the 0.75 case is 149.291 USD2004/MWh. This is a supplied-feed scenario effect, not a reliability optimum. Fixed-hardware density cases likewise change electricity and purchased fuel consistently: the tested lower/higher density endpoints give 398.980 and 221.325 USD2004/MWh with the same 100 kg/year feed and charge. Increasing assumed external T price from 10 to 100 million USD2004/kg changes no-credit LCOE from 448.399 to 3467.940.

Selected exchanger area supports a limited hardware comparison because the model connects purchased area, capital, conductance and heat removal. Density is an operating-input check with fixed hardware. Rates, life, availability, prices, terminal allowances and supplied T are assumption sensitivities. Their missing qualification or cost-response relations cannot support an engineering optimum.

## Source comparison


Source values and their original page references are retained in [the retained source-boundary review](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/source-evidence/source-boundary.md) and its reviewed page images. The source-conditioned branch uses already-financed capital and supplied 1000 MW with zero second IDC. It retains the integrated case's fuel throughput, rather than reconstructing source fusion/fuel physics. It holds each selected case's recurring expenses and blanket events; terminal/salvage/overhaul fractions stay fixed, so their absolute capital-based amounts change. It does not reconstruct the source financial convention.

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

## Package and evidence identity

| Item | Identity |
|---|---|
| Implemented package checkpoint | `e44a0ded` |
| Independently accepted implementation | `54cce30b` |
| Native CANDIDATE, all ten gates | `f4ea4795`, [integration receipt](evidence/integration-attempt1/integration_return.json) |
| Executable fingerprint | `d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b` |
| Semantic fingerprint | `419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131` |
| Sealed study commit | `3f521955` |
| Snapshot SHA256 | `6f51f7ad251cdec581c556a6c9ab6655e7132142918efe012af52cd2523742c6` |
| TEAx revision | `8d877460ac4f6f264561d916e40c1708adb13397` |

[Exact financial interface](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/evidence/interface-handoff.json) names public inputs and native outputs. The source-inclusive capital branch consumes a native exact-zero construction-duration guard; attempted second financing refuses rather than silently changing the source boundary.

## Verification and remaining limits

The [sealed study report](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/report.md) retains 64 complete native input/output maps, each executed once, with 546 numeric outputs. Independent verification covers 364 scalar channels and 14 predicates per point: 23,296 scalar and 896 predicate comparisons. All comparisons pass; four engineering-failed points remain visible. The [record integrity receipt](evidence/study-record-integrity.json) verifies all 281 frozen artifact hashes, full proposal/result map identity and 27 finding joins. Original persistent evidence hashes remained unchanged during export.

Eleven actual stock-runtime refusal attempts are retained separately from the 64 completed cases. The explicitly separate diagnostic runtime preserves upstream outputs and all 14 predicate records for nonpositive-energy, negative-rate and second-source-financing controls. At −571.893206 MW integrated net output, 505 upstream numeric outputs remain while integrated LCOE is blocked by its dependency; the independent supplied-power comparison branch can remain defined. No refused case receives a sentinel price. Diagnostic baseline parity covers all 546 numeric outputs. See the study diagnostics and [implementation review](evidence/implementation-review.md).

The final non-author reviewer also compared all 34,944 exported scalar values and 896 predicate statuses directly with the original native store, confirming exact equality, unique first attempts and unchanged store bytes. This transport check is distinct from independent numerical derivation; see [final review](evidence/final-review.md).

The complete validator reports four levels passed and two failed, not an overall pass. Level 2 retains 105 literal warnings (103 inherited and two explicit finance zeros); Level 6 retains 493 EXPOSE static findings (407 inherited and 86 additive). No unbound, undefined, self-reference or orphan defects were reported. The native relationship-scoped validation entry SV-135 passes. Detailed limits remain in the [WI-091 report](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/report.md).

Preservation checks confirm all 9,104 protected files unchanged. The separate isolated Stellaris regression matches 1,352 numeric outputs and 68 responses exactly. The native CANDIDATE also passes all ten promotion gates, including regeneration, source-family regression, baseline verification and lineage. These establish implementation and preservation evidence, not whole-plant scientific qualification.

## Replay and prompt-04 handoff

Start with the [sealed study record](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/record.md) at `3f521955`, its snapshot and sealed package, then follow [exact replay instructions](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/replay.md) in an isolated copy. Execution used `f4ea479506cae17d2a9aafe0f914346c555193e7` and the package fingerprints above; the freeze adds evidence without changing that package. The replay document gives native execution, all-point verification and reporting-only commands. Never execute into the frozen record.

Prompt 04 can consume this complete conditional plant/financial boundary through the [native interface handoff](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/evidence/interface-handoff.json). Preserve both supply scenarios, their charges, already-accounted internal recycling, event-only replacement costs and the single-financing invariant. Retain the three source failures, insufficient exchanger case, separate undefined financial outcomes and scientific support flags. The [design assumption register and reuse/change account](../../../completed/20260922_WI-091_aries-integrated-lifecycle-cost/design.md) identify replacement conditions and owners.

Selected exchanger area supports a bounded purchased-hardware tradeoff; density supports an operating propagation test with fixed equipment. The declared finance, cost, lifetime, availability and new-feed axes support assumption sensitivity only. A capability/cost model for usable breeder extraction, source-consistent life and replacement timing, dated supply/terminal cost evidence, and missing scientific qualifications remain future engineering work. Neither finite LCOE nor the source-conditioned numerical proximity closes that broader model effort.
