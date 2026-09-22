# Integrated ARIES equipment and costs

[AGENT] Status: **the positive integration goal is met under the declared assumptions.** Native equipment/cost integration, thermal-first sensitivity and both frozen studies pass independent review. The [final review](evidence/cost-study-review.md) accepts the conditional answer and financial handoff. Formal item/goal closure remains owner-held.

## Executable case

The evolving assembly is `models/designs/aries_cs_integrated/plant.sysml`; its generated package is `exploration/aries_integrated/aries_integrated/`. The canonical `nominal-calculated` case is the **assumed integrated baseline**, as required by the owner. It produces 423.106794 MW net and 2240.389047 MW accepted heat, with zero unmet heat and all 14 represented scalar checks satisfied. These scalar checks do not qualify magnet/conductor, breeding, materials, deposition, hydraulics or machine maps; their scientific support outputs remain 0.

The native graph owns selected aggregate magnet/structure, blanket/divertor, shield/manifold, vessel/cryostat, support, LiPb and fuel inventories; selected exchanger areas, pump capacities and machine ratings; and disjoint capital, annual-operation and replacement accounts. Missing VF-coil mass and conductor takeoff remain explicitly unavailable. Supplied hardware choices are independent of calculated operating demand. Existing fuel, capacity, supplied-purchase, account-sum, annual-cost and allowance machinery is reused; ten additive generic calculations and one costed-component specialization complete the accepted boundary. [Implementation report](../../../active/WI-090_aries-integrated-equipment-and-costs/report.md) and [exact financial owner map](../../../active/WI-090_aries-integrated-equipment-and-costs/evidence/financial-handoff.md) identify the native interfaces and limitations.

| Identity | Value |
|---|---|
| Reviewed package checkpoint | `36cb6aedcde8367461ba466b8e0ff229db11e12b` |
| Executable fingerprint | `01f8f89c42a98621ff4c6868156d9b7938b7c80102f1c8321b35504ffcc7a021` |
| Semantic fingerprint | `10ea8ab0c94ef4bd126465b2bf664a86bc3a38fa892b39591aa3057069f13a6f` |
| TEAx revision | `8d877460ac4f6f264561d916e40c1708adb13397` |
| Native CANDIDATE | `e8f9cc1d`, [all ten integration gates](evidence/integration-attempt1/integration_return.json) |
| Thermal/equipment study | `494c329e`, `exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs/` |
| Cost study | `8d322312`, `exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/`; executed at `bd9b9aec` |

## Thermal assumptions precede economic interpretation

The 64-point native study covers 25 principal thermal axes, four recuperator/PbLi-temperature interaction points, fixed-hardware plasma-demand changes and selected exchanger/pump alternatives. Every point completed and was independently checked: 17,792 scalar comparisons and 896 exact predicates pass. Eleven engineering-failure cases remain in the record. [Thermal reading](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs/thermal-results.md) and [independent review](evidence/thermal-study-review.md) carry the detailed evidence.

| Declared thermal variation | Net output at endpoints | Meaning |
|---|---|---|
| Cycle flow 1000–1800 kg/s |596.773–149.663 MW| Both endpoints fail: low flow leaves 138.638 MW heat unremoved; high flow exceeds compressor capacity. Neither is a usable alternative. |
| Neutron multiplier 1–1.25 |254.022–518.217 MW| Strong conditional response; deposition/neutronics remains unsupported. |
| Recuperator effectiveness 0.6–0.95 |310.053–557.114 MW| Strong conditional response without a purchased-geometry/performance law. |
| He operating flow 1630.5–4891.5 kg/s |470.814–293.616 MW| Cubic pump-demand proxy responds; high flow exceeds purchased pump capacity. |

These unequal finite windows do not define probabilities or an optimum. Nominal U, bulk-temperature, partition and PbLi-heat-capacity endpoints retain enough modeled heat-removal capability and show no meaningful net-power change. That local nonresponse does not establish irrelevance outside the tested windows.

All 56 thermal/plasma-demand points retain every upfront purchase account and the same overnight capital. Density changes fuel throughput and annual expense. Buying 5000 m² He exchanger area lowers cost but leaves 47.119 MW heat unremoved; its linear price is flagged outside the local comparison range. Buying 75000 m² clears heat removal but gives no nominal power gain. Buying 1630.5 versus 4891.5 kg/s pump capacity changes cost and flow margin while operating draw stays fixed at unchanged operating flow. No demand-triggered resizing or invented efficiency benefit occurs.

| Preserved source-conditioned case | Unmet heat | Interpretation |
|---|---:|---|
| Nominal source-assumed |158.725848 MW| Fails full heat removal. |
| Literal Lyon |398.908524 MW| Fails full heat removal. |
| Literal Raffray accounting |502.134202 MW| Also retains the −182.03 MW energy mismatch. |

Their electrical outputs describe only the represented removable-heat subset, not complete steady source plants. They remain adverse preservation controls in later financial work.

## Declared capital and operating boundary

All amounts are **USD2004**, with no conversion or market-price claim. Source-package amounts are provisionally treated as installed-direct estimates under the explicit disjoint scope map. Initial LiPb and tritium inventory belong to initial capital once; fuel throughput, calendar-time stock decay and recurring makeup have separate owners.

| Assumed baseline native amount | USD2004 |
|---|---:|
| Provisional direct capital |2,919,603,000|
| Provisional overnight capital |4,350,208,470|
| Separate source direct comparison |2,619,572,000|
| Separate source inclusive comparison |5,055,773,960|
| Annual operating cost, no T-recovery credit |3,215,100,712.857/year|
| Scheduled replacement event |72,231,350/event|
| Undiscounted scheduled replacements |433,388,100 over 40 years|
| Alternative replacement reserve |12,279,329.5/year|

Overnight capital includes 20% indirect, 20% contingency on direct plus indirect, and 5% owner/commissioning allowance. It excludes financing/escalation; the source 1.93 inclusive multiplier remains a separate comparison. The 300,031,000 direct difference is 300 million initial T stock plus the retained 31,000 core mismatch.

Annual operating cost includes fixed O&M, consumables, external T, deuterium and any modeled grid imports. Positive-operation auxiliary demand already reduces net export. The no-credit baseline assumes 104.667707 kg/year purchased T at 30 million/kg; it is deliberately pessimistic supply accounting, not a prediction of zero breeding. Replacement uses selected 5 full-power-year life, 0.85 availability and 40 calendar years: six events strictly before retirement. The annual reserve is an alternative representation and must not be added to event cashflows. Decommissioning and end-of-life disposal are outside this declared boundary, not zero-cost claims.

### Cost uncertainty

The 113-point second study varies all 38 purchase-price factors plus stock/fuel, annual allowances, capital fractions, availability, replacement assumptions and explicit supplied-recovery scenarios. It verifies every point against 278 independent numeric channels and 14 predicates: 31,414 scalar and 1,582 predicate comparisons pass. All 110 assumed-baseline-family points retain 423.106794 MW net and satisfy the represented checks; the three source controls retain their failures. No scientific support flag is upgraded.

| Conditional native scenario | Overnight capital | Annual operating cost | Undiscounted lifetime replacements |
|---|---:|---:|---:|
| Baseline, no recovery credit |$4.350 billion|$3.215 billion/year|$433.388 million|
| Same baseline, supplied 100 kg/year recovery |$4.350 billion|$215.101 million/year|$433.388 million|
| Combined lower-cost assumptions, no credit |$1.623 billion|$893.907 million/year|$48.499 million|
| Combined higher-cost assumptions, no credit |$13.332 billion|$11.960 billion/year|$5.126 billion|
| Same combined lower/higher assumptions, 100 kg/year recovery |$1.623–13.332 billion|$36.006 million–1.960 billion/year|$48.499 million–5.126 billion|

The [cost report](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/report.md) and exact native cases supply these values. All entries are USD2004. The combined cases simultaneously vary explicitly declared engineering bounds, including availability and replacement life; they are scenario corners, not confidence intervals or independently predicted plant costs. Full inputs are retained. Their annual export also changes with availability, so a smaller expense is not a demonstrated better economic outcome.

Over the declared one-factor windows, the largest overnight changes are tritium unit price (+$1.043 billion at the high endpoint), selected T stock (+$894 million) and contingency (+$700.705 million). Annual cost is dominated by tritium price and the independent recovery boundary; availability follows among the tested continuous annual-cost assumptions. Replacement life and event-price factor dominate the tested lifetime replacement changes. These are finite effects over unequal assumption windows, not a probability ranking or equipment recommendation.

At nominal assumptions, 100 kg/year supplied recovery leaves 4.667707 kg/year external T purchase; 200 kg/year reduces modeled purchase to zero and annual operating cost to $75.070 million. Recovery is an independently supplied boundary, with no incremental recovery-cost or qualification law at fixed installed scope. These lower expenses do not establish breeding sufficiency, free recovery equipment or an optimum.

Buying the adequate 75000 m² He exchanger changes overnight capital to $4.393661 billion in selected-quantity mode, while fixed-budget mode leaves it at $4.350208 billion. Both retain the same calculated thermal result. That explicit nonresponse prevents treating the fixed-budget placeholder as a credible hardware-cost law. The separate source direct/inclusive channels remain unchanged comparisons, not substitutes silently added to these costs.

## Source reconciliation and remaining response limits

The graph calculates the source reactor 28.396 million unallocated difference, core 0.031 million excess, coil 5.287 million excess and fuel 0.001 million difference. These are unresolved source discrepancies, not installation estimates. Known listed mass including cryostat exceeds printed dry-core mass by 1,333,700 kg and lacks known VF mass; this is not an authenticated matching-scope reconciliation. Selected total LiPb is 8,830,000 kg, counted once; its 17.1/kg comparison differs from the source budget by 334,000. The source replacement comparison preserves 975 million from 75 million×13 versus 966 million printed. [Original-source review](evidence/source-review.md) and native study results retain all differences.

Selected-quantity prices are local linear scenarios; fixed source-package alternatives do not respond credibly to hardware changes. Assumed U, temperature limits, efficiencies and recuperation lack qualified geometry/performance-price relations. Pump hydraulics uses a declared cubic proxy, and replacement life is selected rather than derived from damage. Aggregate source inventories do not qualify field/conductor, breeding or materials. Those limits carry into prompt 03 and subsequent design studies.

## Verification and preservation

The 66-case development receipt retains 54 evaluated cases and 12 expected domain refusals. Exact generated-code/SysML-body and canonical-output parity covers the final citation-only package rebuild. Independent source, design and implementation reviews accepted the affected MR-7 ownership and disjointness. Complete model validation remains four levels passing and two failing: reviewed L2 literal-binding warnings and L6 static EXPOSE/reference limitations are retained; there is no complete-validator pass claim.

All 8752 protected original and frozen-predecessor files remain unchanged through both rounds. The separate isolated Stellaris replay matches 1352 numeric outputs and 68 responses exactly. [Preservation](evidence/round2-preservation.json) and [behavioral regression](evidence/stellaris-regression.md) are distinct evidence. No original Stellaris definition, input, package, completion or frozen result was changed.

## Replay and prompt 03 handoff

Use the licensed runtime documented in `.project/codex-test-setup.md`, the pinned TEAx revision and a fresh checkout/output location. Do not run replay commands into frozen record directories. The thermal study's [replay instructions](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs/replay.md) give exact native execution and all-point verification commands; its snapshot, sealed package, source copies and complete maps are committed at 494c329e.

The [financial handoff](../../../active/WI-090_aries-integrated-equipment-and-costs/evidence/financial-handoff.md) lists 99 exact public input keys and 114 native output IDs, including the separate source-inclusive, overnight, annual-export and scheduled-event boundaries. Prompt 03 must choose its declared supply/cost scenarios and financing treatment without treating this assumed plant as scientifically qualified. The [cost-study replay](../../../../exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/replay.md) identifies execution checkpoint `bd9b9aec`, frozen record `8d322312`, all 113-point verification and the retained export-only recovery. Native evaluation ran once per point; exact full maps and original evidence remain intact. The final independent review passes; the delivered model and financial handoff are ready for prompt 03 under these declared limits.
