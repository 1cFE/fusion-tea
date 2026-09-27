# Study preparation notes

[AGENT] Working choices for the coordinator, pending the accepted model interface and independent scan. This is not an execution release or a sourced uncertainty interval.

## Catalog and controls

Retain all 498 predecessor input maps as development controls after the explicit migration. The original finite catalog has 375 gas offers and 72 steam connector offers; three steam offers share an identical full input map with a gas row. Preserve aliases so deduplication does not remove a technology's candidate. In the repaired predecessor, 14 gas and 21 steam offers pass their original requirements. These counts are historical evidence only; new whole-plant admission and ranking must be calculated again.

For the main study, rerun the complete nominal catalog at 2500, 2800 and 3000 MW supplied source. Each varying branch is paired with a supported fixed anchor of the other branch when one exists. Selection uses new whole-plant LCOE. A source-wide failure stays in the attempted ledger. A permanent source-qualification disclaimer is separate from an equipment failure.

Cost-only scenarios can rerank the nominal physically supported catalog because physical operating inputs stay fixed. Finance and availability also require new lifecycle/outage checks. Performance scenarios can create or remove supported offers, so either rerun their full affected catalog or explicitly report a held-offer response without claiming an optimized technology result. Never silently discard a newly passing offer based on the old verdict.

## Sensitivity questions

- How do conversion prices and efficiencies change the selected equipment and paired whole-plant difference?
- How do common capital scope, indirect/contingency rates and the uncertain primary pipe quote affect the electricity-denominator penalty?
- How do heating efficiency, primary drive efficiency and residual source loads change net export and auxiliary rejection margins?
- How do zero/low/historical-stress tritium prices and the modeled versus source-paper breeding assumptions affect the paired result?
- How do availability, replacement service life, finance and routine service assumptions affect ranking and outage admission?

Record every interval as an engineered sensitivity unless a retained source supports its endpoints. For material unknowns, calculate a supported reversal threshold when one can be bracketed by native evaluations. If there is no crossing in the tested window, say so; never call an arbitrary endpoint a credible uncertainty bound. Threshold interpolation may join native response points; it may not insert a separate physical or LCOE calculation into reporting.

## Proposed finite budget

[AGENT] Limit the main study to 3000 unique complete input maps after aliases are retained. Exact allocation follows the pinned oracle scan. Development controls are separate. A practical allocation is the full nominal catalog; cost/finance/common-demand scenarios over all nominally supported equipment offers; two opposing joint efficiency scenarios over the full affected 2500/2800 MW catalogs; a few held-offer one-at-a-time responses for interpretation; and native-confirmed price/heating thresholds. The 3000 MW source-wide failures need not be repeated under every price scenario because those prices cannot repair the physical failure, but remain in the nominal attempted ledger.

New cryogenic axes are explicitly assumed mean heating 35.5/50/80 W/m³ and extra cold heat 0/10000/13000 W. The 50 value is a reference stress, not an established upper bound; 80 and 13000 retain genuine selected-capacity failures. The same fixed 40/60 kW equipment and quote apply. Nuclear-transport qualification remains zero. The accepted C1 review owns the equations and hot-source versus cold-region accounting distinction.

## Evidence deposits

The final native study needs complete qualified inputs, outputs and verdicts for every unique point; case aliases and scenario membership; all-axis indicators including declined axes; source/account inventory; the old-boundary control comparison; separate power and capital/operating/event contributions; native verification of every new arithmetic channel and predicate; published figures/data; and frozen replay sources. Final coverage must include positive and adverse whole-plant cases and explicit rankability reasons.
