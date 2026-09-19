# Fuel-processing capital now follows operating exhaust flow

**The requested R10.S2 target is met.** The [fresh independent grade](evidence/final-review-and-grade.md) assigns **R10.S = 2** against the unchanged rubric. The adopted conventional estimate follows calculated running D+T exhaust through a source-supported relationship into plant capital and electricity cost. Audited model `2a50d3ec` and frozen study `2bae7fb7` preserve the exact result. Formal goal closure remains owner-held.

## Included processing and capacity

The represented package covers palladium-alloy cleanup/impurity treatment, cryogenic isotope separation, internal transfer pumps and limited purchased secondary containment. It includes the local controls supplied with those source packages. It does not represent a complete fuel plant.

The verified upstream fuel calculation supplies **12.911794 kg D+T per operating day**, including **7.742681 kg T/day**, at the reference point. This is plasma-exhaust inlet before recovery losses, per fusion module. Running flow determines equipment capacity; annual availability determines annual processed mass. Impurities, helium and carrier gas are not included in that isotope-mass number. The accepted process requires source-like minor impurities and cleaned separation feed below 1 ppm noncondensibles; the model declares these conditions rather than calculating purity or qualifying recovery.

[Producer trace](evidence/current-trace.md), [adopted design](../../../../work/active/WI-070_throughput-based-fuel-processing-costs/design.md) and [independent implementation audit](../../../../work/active/WI-070_throughput-based-fuel-processing-costs/audit.md) identify the exact interface. The physical balance comes from audited WI-069 at `956444b5`; WI-070 consumes its output without changing fuel losses or residence assumptions.

## Capacity to price

ORNL's 1988 ETR/ITER systems-code method scales the four historical equipment rows with a common exponent of 0.3, relative to **1.79712 kg D+T/day**. Each row retains its raw capital and direct-installation amounts and expenditure-year assumptions. CPI converts those amounts to 2025 purchasing power; it is not a validated contemporary equipment-price index. Larger original ITER process designs support conventional service above the current demand, but do not empirically validate this economic exponent or year-round reliability. [Source applicability review](evidence/source-review-r2.md), [price review](evidence/proposed-price-review.md).

The calculation applies a separately declared capacity margin, scales each converted row by the capacity ratio to exponent 0.3, applies a separate price multiplier, and sums identical per-module packages. Both margin and multiplier default to one; no standby train is priced.

| Reference result | Old account | Adopted account |
|---|---:|---:|
| Processing equipment and represented installation | $120.746 million | $22.786 million |
| Total plant capital | $18.059 billion | $17.918 billion |
| Headline electricity cost | $273.455/MWh | $271.584/MWh |

The new subtotal consists of **$20.443 million equipment plus $2.343 million direct installation**, before generic project charges. The capital reduction is **$141.271 million** after those charges; the electricity-cost change is **−$1.870/MWh**. These are matched model results, not demonstrated procurement savings. [Exact baseline changes](../../../../work/active/WI-070_throughput-based-fuel-processing-costs/evidence/baseline-delta.json).

## Accounting and remaining omissions

The complete old C220500 allowance is replaced once. Source installation is absent from the generic equipment-installation base and is excluded, with its project contingency, from freight. Other tax, insurance, indirect and finance allowances retain their reviewed meanings. Included local controls belong only to C220500; distinct supervisory/plasma controls belong to retained C220700. That residual controls allowance has not been recalibrated from an itemized historical price. [Account reconciliation](../../../../work/active/WI-070_throughput-based-fuel-processing-costs/evidence/account-reconciliation.md), [controls review](evidence/controls-review.md).

Civil buildings/ventilation and annual fuel purchases remain separate. The startup-fuel allowance still uses its existing power proxy; this change does not price the calculated startup stock. Storage hardware, blanket extraction/conditioning, specialized additional fuel monitoring, broader containment and emergency/effluent systems, fueling hardware, torus vacuum pumps, full design/inspection, operating expense and replacements remain outside the new block. Generic project allowances do not establish detailed coverage of those omissions.

## Verification and study results

Author checks pass 172 source/domain tests, 263 affected tests and 13 model-family tests; these suites overlap. Independent audit passes 176 tests and 6,538 comparisons over seven native cases. The original 25 constraint verdicts are preserved at the matched reference. [Audit](../../../../work/active/WI-070_throughput-based-fuel-processing-costs/audit.md), [integration receipt](evidence/round2/integration/integration_return.json).

Static validation still fails L2 and L6. L2 retains ten issues; L6 adds three instances of the known public-alias dot-reference limitation, with separate generated-execution coverage. Integration did not run its manifest read-set coverage check. These limitations are not reported as passes.

The [focused study report](../../../../exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/report.md) retains 20 native cases, with all **18,680 mapped comparisons and 500 predicate comparisons passing**. Exactly 22 inherited numeric channels remain outside the independent map and are named in the record. None of the cases satisfies every whole-plant screen.

- Changing single-pass burn from 2.5% to 10% changes inlet flow from **26.503 to 6.116 kg D+T/day** and process capital from **$28.273 to $18.210 million**. The report separates the existing annual-fuel effect from the new processing-capital effect.
- Changing physical recovery preserves inlet capacity and its price. Its loss/breeding effect remains separate from the held annual fuel-pricing recovery input.
- Changing unplanned downtime preserves running flow and equipment price while changing annual processing, electricity production and LCOE.
- The independent price stress of 0.5–2 times changes process capital to **$11.393–45.572 million** and reference LCOE to **$271.367–272.019/MWh**. This is an engineered stress range, not a probability interval.
- Capacity margins and actual containment expenditure-year alternatives are separate cases; matched old/new controls retain the same physical outputs and verdicts.

The first attempt admitted 15 active cases and rejected five legacy controls before evaluation because of Boolean input encoding. Its original store and evidence remain. The successful retry used the equivalent accepted numeric encoding in a fresh store, with no case filtering or model change. The immutable study is committed at `2bae7fb7`; cold reproduction passes all 20 cases and 19,120 native scalar comparisons. The independent final review passes the frozen evidence, interpretation and all seven finding dispositions. Its four-case cold check reproduces 3,824 native scalar values and every predicate.

ARIES remains sealed, published r2 and historical studies are preserved, and no merge or push occurred. Formal goal closure remains the owner's decision.
