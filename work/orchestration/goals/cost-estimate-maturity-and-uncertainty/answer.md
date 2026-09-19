# Cost-estimate maturity and uncertainty

The integrated reference has meaningful functional cost detail and a defensible **provisional Class 5 conceptual estimate** assessment. Its nominal overnight capital is **$17.918 billion** and headline levelized cost of electricity (LCOE) is **$271.584/MWh**. The new calculation quantifies selected source-price and source-interpretation uncertainty. It does not establish a confidence interval for the complete plant. **Fresh independent review assigns R12.S = 3 — PASS** against the unchanged criterion. No required S3 element is missing; see the [independent grade](evidence/final-review-and-grade.md).

## Which estimate this describes

This is the fourteen-circuit reference after the completed cooling, facilities and fuel-processing work. Audited model commit **`fe720553`** adds one shared stainless fabrication-price input through WI-071. Its nominal value preserves all 956 retained baseline outputs and all 25 engineering predicates exactly. The [entering account review](evidence/account-review.md) describes WI-070; its nominal amounts and disjoint account map remain valid here through that preservation check. Historical eighteen-circuit and published r2 results are different estimates.

| Identity | Assessed candidate |
|---|---|
| Semantic fingerprint | `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a` |
| Executable fingerprint | `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236` |
| Integration candidate pin | `e48d5218b6e3be2775a94269a461dccd259fccc5fc41fed7c135dc1336bfe284` |
| Frozen study commit | `82bf78f8` |
| Native study | [20260919-cost-estimate-maturity-and-uncertainty](../../../../exploration/stellarator_e2e/studies/20260919-cost-estimate-maturity-and-uncertainty/record.md) |

Exact inputs are retained in the study preparation files and [account extraction](evidence/accounts/fixed-inputs.json). The reference has one module, major/minor plasma radii of 12.7/1.3 m, 48 coils, fixed reference magnet sizing, fourteen cooling circuits, layout-based facilities and the adopted conventional fuel-processing package. It retains 30 years of operation, eight years of construction, 7% interest, 2% annual expense escalation, 10% direct contingency and zero supplementary contingency. Replacement scheduling gives availability 0.902778; no additional unplanned downtime is assumed in the reference.

## What costs are represented

The [functional account map](evidence/accounts/functional-accounts.csv) contains 23 disjoint direct-account rows with native producer references. Cooling, magnets and facilities together represent **73.478% of the $12.219 billion direct subtotal**. Their children price distinct equipment, material quantities or manufacturing operations.

| Family | Direct cost | Share | Actual functional detail |
|---|---:|---:|---|
| Cooling | $6.471 billion | 52.960% | Machines, primary piping, exchangers, secondary piping, inventories and spares; primary piping is $2.974 billion and exchangers $2.816 billion. |
| Magnets | $1.707 billion | 13.973% | Complete tape, winding operations, external materials, additional insulation sheet and electromagnetic supports. |
| Facilities and site | $0.800 billion | 6.545% | Twenty-five measured civil occurrences, ventilation and site improvements. |

The account codes sometimes exceed three digits. The relevant rubric evidence is the functional depth beneath the broad totals, not the character count. No lump was relabeled or split by arbitrary percentages. Large indirect costs remain an explicit project-level factor, with their lower maturity disclosed.

| Cost or production quantity | Nominal result |
|---|---:|
| Direct accounts before contingency | $12.219310 billion |
| Direct contingency | $1.221931 billion |
| Project indirect costs | $3.584331 billion |
| Overnight capital, including contingency and other capital accounts | $17.918171 billion |
| Separate construction-interest diagnostic | $5.061441 billion |
| Raw routine operations and maintenance | $55.143720 million/year |
| Levelized routine operations and maintenance plus coolant makeup | $79.360459 million/year |
| Scheduled replacement annual equivalent | $193.999913 million/year |
| All levelized annual noncapital expense, including fuel | $274.152877 million/year |
| Net electricity capacity | 1,008.898406 MW |
| Annual electricity | 7,978,704.890196 MWh |
| Headline LCOE | $271.584320/MWh |
| Separate comparison-form LCOE | $266.458931/MWh |

LCOE expresses modeled lifetime expense as cost per unit of electricity. The headline annual capital charge uses overnight capital multiplied by `(1.07)^4` and the capital-recovery factor `0.0805864035111112`. The comparison form instead adds the separate construction-interest amount to overnight capital before applying that factor. The two financing treatments are not added together. The [account review](evidence/account-review.md#capital-contingency-and-financing) reconciles the remaining capital accounts and annual expenses.

All amounts are USD on **mixed monetary bases**. Cooling, civil and fuel-processing sources use inherited CPI conversions to 2025 purchasing power; winding and helium include estimated 2026 bases; several inherited rates have unresolved years. CPI is an approximate purchasing-power proxy, not equipment escalation. Neither these totals nor the uncertainty endpoints are a normalized “2025 plant estimate.” The frozen comparison conventions remain unchanged.

## How mature the estimate is

[AGENT] The [maturity assessment](evidence/method-research.md#maturity-assessment) applies generic AACE 17R-97 guidance, using the official 2020 public sample and the original generic classification matrix reproduced in DOE's 2018 cost-estimating guide. The reproduced matrix is the historical 2011 version; full conformity with an unseen current matrix is not claimed. The [independent method review](evidence/method-review.md) accepts **provisional Class 5**. This is an engineering assessment, not AACE certification or a measured completion percentage.

Cooling has calculated duties, counts and conceptual masses, but lacks qualified pressure/material designs and procurement packages. Facilities have an explicit conceptual layout, but lack site, structural and shielding design. Magnets have material and winding estimates, but lack a complete manufacturing route, supplier scope and yield evidence. Fuel processing has throughput and historical equipment rows, but incomplete process and safety scope. Residual plant and project costs rely more heavily on coefficients and allowances. Those differences remain visible; software completion does not raise their engineering maturity.

No generic Class 5 accuracy percentage is applied. The process-industry classification excludes power generation, and the nuclear-specific classification excludes fusion. The generic framework therefore supplies the maturity basis; it does not supply a probability distribution.

## What the uncertainty calculation means

The [26-entry uncertainty register](uncertainty-register.md) distinguishes source errors, engineering quantities, deliberate designs, future scenarios, financial conventions and missing equipment. Four entries have numerical treatments in this study:

- A single fabrication rate of **240, 310 or 360 USD2017/kg** changes initial exchangers, primary and secondary piping, and future exchanger-bundle replacement together. The endpoints follow an ANL source judgment that stainless fabrication costs two to three times a fixed 120 USD/kg carbon-steel reference. This is conditional on that reference and the adopted equipment analogy; it does not bound actual helium/salt equipment procurement.
- One civil-source ton interpretation applies **907.18474 or 1,000 kg/TN** jointly to all affected building occurrences, with physical quantities fixed.
- One containment expenditure-date interpretation uses the retained **1978, 1980 or 1982 CPI** for both equipment and its direct installation.
- Additional insulation sheet is either separately charged or included in the retained winding charge. Both cases contain the same physical insulation. The zero additional charge does not mean free or absent equipment.

The full combination of these alternatives gives **36 cases** with existing 10% contingency. Another **36 matched cases** set contingency to zero as a financial diagnostic. Two separate stresses apply 5% and 10% additional unplanned downtime at nominal prices. These 74 cases are a finite enumeration, without probabilities, statistical independence assumptions, random seeds or sampling-convergence claims.

Existing contingency remains a deterministic allowance. The input alternatives are propagated once through actual accounts, dependent installation, replacement expense, indirect costs and financing; no second uncertainty uplift is added. Zero-contingency results expose the allowance's effect and do not replace financial policy. Missing scope is not presumed covered by contingency.

## Results and verification

The [native study summary](../../../../exploration/stellarator_e2e/studies/20260919-cost-estimate-maturity-and-uncertainty/results/summary.json) retains all three populations separately. No cases were removed.

| Population | Cases | Overnight capital | Headline LCOE |
|---|---:|---:|---:|
| Selected source/interpretation alternatives, existing 10% contingency | 36 | **$15.948–19.304 billion** | **$244.882–290.376/MWh** |
| Matched zero-contingency diagnostic | 36 | $14.528–17.577 billion | $226.085–267.504/MWh |
| Nominal prices, 5% additional unplanned downtime | 1 | $17.918 billion | $285.201/MWh |
| Nominal prices, 10% additional unplanned downtime | 1 | $17.918 billion | $300.292/MWh |

The first row is the **conditional partial uncertainty envelope**. It includes only register entries U01–U04, at the retained design and financial conventions. It is neither a confidence interval nor a full-plant accuracy range. Direct costs span $10.841–13.189 billion; annual noncapital expense spans $269.259–277.649 million, including scheduled replacements of $189.106–197.496 million/year. The separate construction-interest diagnostic spans $4.505–5.453 billion. Annual electricity remains exactly 7,978,704.890196 MWh in all 72 cost cases. The comparison-form LCOE spans $240.320–284.854/MWh in the source population.

Fabrication price dominates the **quantified** variation: its isolated low-to-high LCOE difference is $45.082/MWh with other assumptions nominal. The corresponding differences are $0.391/MWh for the civil ton interpretation, $0.01169/MWh for the containment date and $0.00916/MWh for additional sheet inclusion. These are deterministic contrasts, not shares of statistical variance or a ranking of the unbounded uncertainties. The combined minimum uses 240 USD/kg, metric tonnes, the 1982 containment date and included sheet stock; the maximum uses 360 USD/kg, short tons, the 1978 date and separate sheet stock.

The downtime stresses reduce annual electricity to 95% and 90% of its reference value through the existing availability producer. They also change annual fuel expense and the in-vessel replacement calendar. Their effect is therefore propagated through the model, not calculated by simply dividing the baseline LCOE by availability. No reliability evidence supports treating these two stresses as uncertainty endpoints.

**All 74 cases completed; none passes every plant constraint.** Each retains four failed predicates: divertor heat handling, tritium breeding, reference conductor current and winding-pack fit. There were no execution rejections, failed calculations or undefined breeding cases. Separate applicability diagnostics, including the unresolved salt-to-power-cycle temperature interface, remain adverse. Cost verification does not establish a feasible plant.

Independent implementation audit and all ten integration gates pass. Native verification passes **69,116 mapped scalar comparisons and 1,850 predicate comparisons** across the 74 cases. The 2,887 account/dependency checks independently reproduce source endpoints, common-rate purchases, initial and replacement cost response, unchanged unrelated quantities and nominal preservation. The independent map covers 934 unique channels; **22 numeric channels remain unmapped**. Static validation retains the same ten level-2 and 1,082 level-6 issues, and integration did not run manifest read-set coverage. These limits remain part of the result. See [implementation audit](../../../active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/audit.md) and [integration receipt](evidence/integration/integration_return.json).

The frozen study snapshot is `75fcaad1c0b01659235973d323d0e01871ce1c8949bbf10515f07419453bb0dd`. All 565 listed artifact hashes were checked before commit. Replaying its retained producer package reproduces all 74 cases, 70,744 native output values and every constraint verdict; see [reproduction receipt](evidence/frozen-reproduction/reproduction.json). All three native record checks pass. A missing CSV arm label was corrected before commit with all original data preserved; [repair evidence](evidence/precommit-record-repair/repair-receipt.json) shows exact equality of every existing cell and no other result-file change.

The fresh reviewer independently verified all 565 artifacts against committed blobs and checked all 74 cases and 36 contingency pairs. Its 71,442 numerical equalities include native/export agreement, account sums, shared fabrication and replacement response, and financial/electricity arithmetic. These checks overlap prior verification; they do not independently validate the physical assumptions. The [review receipt](evidence/final-review/checks.json) records the scope.

## What remains outside the range

The major exclusions are fabrication-analogy transfer, pressure/material qualification, routing and equipment quantities; conductor purchase and winding/support price uncertainty; qualified pump costs; reliability, replacement procedures and outages; operating expenses; and financial/schedule uncertainty. Missing or coverage-unresolved scope includes magnet manufacturing and testing, cooling valves/supports/tanks/trace heating, steam generation, facility handling equipment and services, and wider fuel storage/extraction/containment/fueling/vacuum systems. These have no supported numerical bounds in the inspected evidence. The register gives each a concrete next evidence request and relevant engineering discipline.

The largest useful next step is scope-matched exchanger and piping fabrication evidence, followed by qualified geometry and pressure/material design. Magnet procurement/manufacturing quotations and reliability evidence would address other major gaps. These are follow-up needs, not amounts hidden inside the conditional interval.

[OWNER-VERBATIM] “great. please close the goal”. **Formally closed on 2026-09-19** on the independently reviewed R12.S = 3, PASS result. The limitations above remain part of that result. ARIES remains sealed, the published r2 comparison is preserved, and no merge or push is authorized by this closure.
