# T-007 postexecution interpretation and disposition review

## Verdict

**PASS for the numerical interpretation, answer and all six proposed dispositions.** The coordinator may append the reviewed dispositions and freeze the study record. Final snapshot/record checks and the full study test battery remain coordinator-owned completion gates. This review does not claim those pending checks have passed.

Reviewed by the independent non-author `/root/round1_review` on 2026-09-15 under `T-007_postexecution_brief.md`. Reused the valid T-005 source/math, T-006 implementation/integration and study preexecution reviews. No model edits, source reacquisition or execution battery was repeated. This is a bounded correctness/disposition review of the draft record, not a cold reading of a committed snapshot.

## Checked evidence and conclusions

- The actual `results/points.csv` contains 183 arm rows and 180 distinct candidates: 30 minor-radius transect, 21 major-radius transect, 108 matched-window and 24 assumption rows. Counts of satisfied and violated outcomes for all eighteen predicate columns match the record.
- Independently minimizing nominal fully feasible CSV rows, excluding the assumption arm, returns the reported cheap anchors at R = 12.7 m and a = 1.7 m. Their LCOEs are $135.512/MWh and $141.764/MWh for the 100 MW and 220 MW installed-heating cases. The design anchor costs $146.309/MWh and fails the divertor predicate. Unrestricted low-price transect points are not presented as feasible optima.
- Refrigeration share uses total stage refrigeration divided by gross electrical generation minus net electrical output. The design row gives 2.137762 MW / 345.367436 MW = 0.618982%; both cheap anchors give 2.125444 MW / 266.651132 MW = 0.797088%. Direct coil supply remains a separate load. The claim below 1% is explicitly limited to nominal anchors.
- Baseline support mass and cost are 11,615,604.483 kg and $209.081M; total magnet capital is $1,779.451M. Cheap-anchor support mass and cost are 10,746,149.734 kg and $193.431M; total magnet capital is $1,687.402M. These quantities support the answer's distinction between support cost, winding procurement and total magnet capital. Design winding procurement rises 28.571% between a = 1.3 m and a = 2.2 m; total magnet capital rises to $2,328.489M.
- The nuclear-proxy rows increase refrigeration to 5.745859 MW at the design anchor and 5.463467 MW at the cheap anchors. Zero nonmagnet-budget and zero cooling-budget rows change price without establishing physical adequacy. The interpretation correctly retains zero nominal structure deposition, unqualified thermal hardware, inferred mass-fit transfer and inherited fabrication-price assumptions. The 35.5 W/m³ proxy is not an upper bound.
- Direct joins to the entering-Round-1 CSV verify every before/after LCOE and all eighteen verdicts for 159 comparison rows, with zero flips. Direct joins to the preserved older matched-window cases and current CSV verify all 108 historical before/after prices and verdict comparisons, with zero defects. The two plant-closure reference prices are $191.758/MWh and $198.003/MWh. Those older references span earlier increments; the answer attributes the new inventory increment to the immediately entering Round-1 comparison.
- `results/oracle-all-points.json` reports 7,320 scalar and 3,294 predicate comparisons over all 183 arm rows, no failures and maximum scalar relative deviation 6.19e-16. Generic verification reports 30 sampled candidates across 26 verdict strata, 25 channels and all eighteen predicates, with no mismatches. Circumference and cold-volume identity checks are explicitly distinguished from independently published oracle channels.

Evidence homes: `exploration/stellarator_e2e/studies/20260915-coil-inventory/record.md`, its `results/points.csv`, `analysis.json`, `verification_summary.json`, `oracle-all-points.json`, all three `comparison-*.json` artifacts and the preserved entering/historical preparation data. The answer reviewed is `work/orchestration/goals/magnet-coil-realism/answer.md`.

## Dispositions approved

All six rows in `T-007_proposed_dispositions.md` are approved with their stated scope:

| Finding | Approved disposition | Boundary of the approval |
|---|---|---|
| `20260915-coil-inventory#1` | Declared seam; open | Cost sensitivities do not establish procurement qualification or a sized infrastructure floor. |
| `20260915-coil-inventory#2` | Declared seam; open | Retain actual geometry, deposition, structural fit and fabrication qualification limits. |
| `20260914-magnet-coil-realism#3` | Model fix; closed for the named inventory omission | Explicit lead, shield and support heat plus stage/direct-supply accounting repair the omission. Qualification continues in the new seam. |
| `20260907-minor-radius#2` | Declared seam; remains open | Pricing responds to bore; admissible geometry and local conductor/fit margins remain unqualified. |
| `20260913-magnet-design-transfer#3` | Declared seam; remains open | Total-support pricing repairs the casing-floor basis. The five historical passes retain their extrapolated-envelope limitations. |
| `20260904-wall-and-heating#3` | Closed; re-sighting only | Additional bore-price evidence does not reopen the repaired constant-price defect. |

When landing these rows, preserve each finding's responsible actor and concrete evidence home in the discovery register. The reviewed agent-selected scenario values remain agent decisions under owner delegation.

## Accepted learnings

- **L-004 accepted.** Explicit lead, radiation and support heat raises nominal refrigeration from 0.864 MW to 2.138 MW. It remains below 1% of recirculating demand at the design and sampled cheap anchors under the declared nominal scenario. Evidence: anchor and nuclear-proxy CSV rows plus the reviewed stage accounting. Implication: refrigeration is small in these nominal plant budgets; this does not bound unqualified structure deposition or hardware heat loads. Supersedes: none.
- **L-005 accepted.** The Eq. 56 total-support scenario raises baseline support cost from $54.4M to $209.1M at the inherited $18/kg rate. It raises the cheap-point price while leaving the sampled nominal geometry unchanged. Zero predicate flips applies to the 159 immediate-entering comparison rows; assumption rows have no corresponding before rows. Evidence: entering comparison, support costs and independently checked nominal feasible minima. Implication: this sampled window supports a cost increment without a changed nominal feasible choice; it does not establish invariance elsewhere. Supersedes: none.

Accepted by independent reviewer `/root/round1_review`, 2026-09-15. No additional numerical round is required by these results.

## Record landing and remaining assurance

The latest preparation inventory retains the ten native input groups, final manifest/model contract, implemented design and both source bases. Record §14 currently locates the postexecution review under `reviews`; before freezing, copy this review there or amend that citation to its actual goal evidence home. This is a citation repair, not a numerical finding.

The coordinator must finish freezing, record validation and the pending full study tests before claiming final technical completion. A focused recheck of their outcomes can discharge those remaining gates without repeating this source, model or interpretation review.
