# Fuel-processing cost basis: adopted; implementation underway

The goal has a technically reviewed conditional cost basis, but it has not yet met R10.S2. The [fresh current-state grade](evidence/current-r10s-grade.md) remains **R10.S1** because the executed model still prices fuel handling from net electric power. The production model and generated package are unchanged so far; the new study record is in preparation.

## Adopted scenario

[AGENT] Adopt conventional palladium-alloy cleanup followed by cryogenic isotope separation as a conditional costing scenario for the represented plasma-exhaust processor. The [fresh source review](evidence/source-review-r2.md) accepts the engineering transfer at conceptual-estimate depth and recommends this choice. It identifies adoption as an owner-held scientific decision because a previously unspecified technology and an unverified feed-conditioning assumption would determine plant capital.

The scenario assumes near-equimolar D/T, source-like minor impurities and cleanup to the separation reference's less-than 1 ppm noncondensibles. The model calculates isotope flow; it does not verify those feed conditions. Existing 99% recovery and all other fuel-loss assumptions stay unchanged. The scenario does not certify recovery, actual feed purity, year-round reliability or commercial equipment performance.

[OWNER-VERBATIM] “yes, adopt and continue”. The owner adopted this conditional scenario on 2026-09-19. Acceptance authorizes the modeling assumption; it does not by itself earn S2 or formally close the goal. The [trail](trail.md) records the ruling and Round 2 implementation.

## What determines capacity

The existing verified fuel calculation produces **12.911794 kg D+T per operating day**, including **7.742681 kg T/day**, at the reference point. This is inlet flow before recovery losses, per modeled fusion module. Annual availability changes annual processed mass, not running equipment capacity. Total isotope mass does not include helium, carrier gases or impurities.

The producer is the audited WI-069 model at `956444b5`, with its frozen study at `3529f6c8`. Producer files remain unchanged. Fresh targeted fuel-domain and independent-oracle tests pass **144 tests** with 13 serialization warnings. The [current trace](evidence/current-trace.md), [interface review](evidence/interface-review.md) and [identity evidence](evidence/entering-evidence.json) establish the exact consumption interface and accounting path.

## How the source prices that capacity

ORNL's 1988 ETR/ITER systems-code method provides a flow relationship with exponent 0.3, referenced to 1.79712 kg D+T/day. It is a published reactor-oriented conceptual engineering method. Original TSTA expenditure data supply its historical equipment basis. Later primary ITER designs specify conventional cleanup and cryogenic separation above the present demand, including a 320 molecular-mol/hour plasma stream corresponding to approximately 36.48 kg D+T/day in the source's equal-D/T case. This larger process-design evidence resolves the initial small-facility scale concern; it does not empirically validate the economic exponent.

The [first research report](../../../../knowledge/research/pending/20260919-091411_throughput-based-fuel-processing-cost-applicability.md) records source prices, inclusion boundaries and rejected alternatives. The [targeted transfer report](../../../../knowledge/research/pending/20260919-092112_conventional-reactor-fuel-processing-transfer.md) supplies the larger process-design basis. Both native acquisition records are committed at `66548f14`. Eighteen bounded searches were used across two different questions. A challenge-page registration is explicitly rejected as evidence; original papers supply the actual basis.

## Reviewable price example

The [proposed scope](evidence/proposed-cost-scope.md) and [reproducible example](evidence/proposed-price-example.json) price four source rows at the actual running isotope flow. Raw expenditure years are preserved separately and converted using the registered annual CPI series to 2025 purchasing power. CPI is a general monetary proxy, not proof of modern tritium-equipment prices. Installation dates use the source capital-expenditure year as an explicit proxy; containment's 1978–1982 range uses 1980 centrally.

| Included amount | 2025 purchasing-power example|
|---|---:|
| Purchased/fabricated equipment |$20.443 million|
| Source direct installation |$2.343 million|
| **Four-row total** |**$22.786 million**|

The rows cover cleanup, cryogenic separation, internal transfer pumps and limited purchased secondary containment. Some local instrumentation/control is included in those packages. The source supplied some containment boxes free; the estimate does not buy complete plant-area containment. Moving only the containment expenditure year across its source range changes the total to $22.568–23.181 million. That narrow range is a date sensitivity, not total cost uncertainty. No standby train or extra capacity margin is priced.

The [independent price review](evidence/proposed-price-review.md) reproduces the arithmetic and identifies no civil/vacuum duplication in the proposed four-row boundary. Its scope wording corrections are incorporated. The example is not an integrated plant estimate or a claim of total installed/EPC completeness.

## What would be replaced and what remains unpriced

The new block would replace the full existing C220500 processing/containment allowance once through its current CAS22 consumer. That account currently evaluates to $120.746 million using net electric power. Its historical price basis is not established here; the difference from the proposed example is not a demonstrated procurement saving.

Existing civil buildings/ventilation, recurring fuel purchases and the separate startup-stock purchase allowance remain separate. The startup allowance still follows a power proxy despite the computed startup quantity; this is disclosed rather than duplicated in processing capital. Blanket extraction remains a separate function. Its tritium mass flow is not a specification of PbLi circulation, carrier gas or extraction hardware.

The [controls review](evidence/controls-review.md) proposes single ownership: source-included local controls in C220500 and distinct supervisory/plasma controls in retained C220700. Its inherited coefficient remains an uncalibrated residual allowance, not a source-proven numerical deduction. Storage equipment, additional specialized fuel analysis/monitoring, effluent and emergency systems, blanket extraction/conditioning, further safety/service scope, complete design/inspection work, OPEX and replacement schedules remain unpriced by the four-row block. Detailed fueling hardware and torus vacuum pumping are not bought by its internal-transfer-pump row. Omissions are not assumed physically unnecessary.

## Remaining work and current result

The owner decision is resolved. Native WI-070 design and independent accounting review are underway. The production change still needs native model requirements/design, final project-charge reconciliation, implementation, generated execution, integration verification, a focused native study and a fresh R10.S grade tracing cost through plant total and LCOE. The current plant and electricity costs are unchanged; no new LCOE effect or whole-plant feasibility claim is made.

ARIES remains sealed, the published r2 archive is preserved, and unrelated work is untouched. Round 2 is executing the adopted scenario; the goal remains open. No merge or push was performed.
