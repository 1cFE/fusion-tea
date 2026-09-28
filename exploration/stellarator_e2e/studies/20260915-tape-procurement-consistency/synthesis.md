# Executor synthesis — tape procurement consistency

Reader: `/root/study_author`, the executor; this is not an independent review. Date: 2026-09-15. Evidence commit: `f7015074`. Snapshot SHA256: `3af45aa58d511cc28a373c952d5eff52c3e07ededac0cf65092643e72bcb4a3e`. This reading uses only the committed record directory.

## What the study set out to do

Test whether tape procurement follows the same physical inventory as density, selected envelope, current and coil length vary. Compare the correction against its entering package, and report the consequences of explicit tape-price assumptions. The study executed 64 unique native cases, represented by 65 reporting rows because the baseline duplicates one matched point. [Intake and scope](record.md); [resolved proposals](preparation/proposals.json).

## What it found

**The bounded correction is numerically consistent.** Tape length equals tape volume divided by full composite cross-section, and tape cost equals purchased length times dollars per metre. Density and envelope scale tape and non-tape inventory together. Composite-conductor length and winding operations keep their separate current/circumference basis. All 11,456 mapped scalar comparisons and 1,152 independently derived predicate comparisons pass. [Independent comparisons](results/oracle-all-points.json); [combined identities](results/combined-response-checks.json).

At the baseline, 36.58 million tape-metres cost $731.57 million at the assumed $20/m. This replaces the entering $804 million tape account and reduces LCOE from $146.31 to $144.74/MWh. The baseline remains infeasible because divertor heat exceeds its existing limit. The entering evidence is a captured oracle comparison, not a native historical execution. Sixty matched cases preserve 9,600 shared scalar values and all 1,080 predicate verdicts; changed channels are tape procurement and economic descendants. [Baseline](results/analysis.json); [entering attribution](results/comparison-entering.json).

At fixed current, geometry and envelope, density ratios 0.8/1/1.2 give inventory ratios 1.25/1/0.833333. Winding operations do not change. The quantity response already existed physically in the entering model; this correction makes procurement follow it. [Grouped responses](results/axis-responses.json); [matched evidence](results/comparison-entering.json).

At $10/$20/$40 per metre, baseline LCOE is $136.81/$144.74/$160.60/MWh. Quantities, physical outputs and verdicts remain unchanged. These are scenario prices for the assumed construction, not vendor quotes. [Price response](results/axis-responses.json); [price isolation checks](results/combined-response-checks.json).

## Framing verdict per axis

| Axis | Executor reading |
|---|---|
| Reference pack density | Sensitivity remains appropriate. Lower density adds the same tape; higher density consumes unknown current margin. |
| Selected envelope | Sensitivity remains appropriate. The quantity factor enters once; the explored upper envelope is conditional extrapolation. |
| Minor radius | Sensitivity remains appropriate. Bore-based coil length changes both inventory and winding work while plant physics also changes. |
| Major radius | Sensitivity remains appropriate. At fixed minor radius, tape inventory and winding work stay fixed while other plant outputs respond. |
| Coil current | Sensitivity remains appropriate. Inventory and winding work scale together under the held set factors. |
| Tape price | Assumption sensitivity remains appropriate. The model has no supplier performance/price tradeoff, so no procurement optimum is established. |

These judgments agree with the executor’s proposed and observed framing. Exact coordinates, including sampled violations and edge readings, remain available. [Axis accounts](record.md); [indicators](indicators.json); [edge scan](results/edge-scan.json).

## Constraint structure

Three of 64 unique samples satisfy all eighteen existing predicates. They share a = 1.3 m, R = 12.7 m, 17 MA and a 30 T selected envelope. Their LCOEs are $151.92, $146.78 and $143.35/MWh for density ratios 0.8, 1 and 1.2. **All three are conditional extrapolations beyond the approximately 24 T measured extent.** The higher-density sample does not establish adequate absolute current margin. These are sampled passes, not qualified designs or optima. [Feasible cases](results/analysis.json); [source/engineering limits](preparation/implemented-design.md).

All eighteen predicate identities, their satisfied/violated counts and complete definitions are retained. None was indeterminate. The predicate catalog is exactly equal to the entering catalog, with no matched-case feasibility flips. Generic verification covers all thirteen observed verdict combinations. [Constraint table](record.md); [predicate definitions](results/predicate-catalog.json); [stratified verification](results/verification_summary.json).

## Findings carried forward

- **#1 — open declared seam:** supplier performance versus price is absent. Continue treating price as an explicit sensitivity; the delegated ruling does not resolve the missing relationship.
- **#2 — correction complete:** the bounded tape quantity/pricing inconsistency is repaired and verified. No further quantity correction is proposed by this study.
- **#3 — open declared seam:** full-composite construction transfer, fixed ungraded composition, continuous tape inventory, envelope extrapolation, absolute current margin, local fit and manufacturing qualification remain conditional.

The finding identities and homes are recorded in [record.md §15](record.md). This synthesis proposes no scope expansion.

## What the record does not support

The evidence does not support a global optimum, a continuous feasible boundary, a vendor-qualified tape price, perfect-grading discounts, absolute conductor margin, integer tape-count qualification, pack/casing fit or complete factory cost. Reference-coil loading and set-effective loading differ by the retained f_set/f_wp_vol factor. The 56 μm full-composite construction transferred to 6 mm tape remains an assumption. [Source review](reviews/design-review.md); [loading identities](results/inventory-identities.json).

Sixteen native numeric channels are retained without independent oracle coverage. Held inputs are common assumptions, so numerical parity does not validate their physical values. The record does not contain native execution of the entering package or the complete generated implementation/runtime installation. Those limits are explicit; no additional missing historical fact was needed for this reading. [Coverage list](results/oracle-all-points.json); [record limits](record.md).

Final independent study review remains coordinator-provided. The reused independent source and implementation reviews and the executor’s 62 passing record/template/provenance checks establish their stated scopes only. [Review coverage](reviews/validation.md).
