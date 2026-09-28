# Goal: Conditional integrated ARIES design studies

## Status

`closed` — 2026-09-22. [OWNER] Closure authorized after the independent final PASS at `aa162cd4`. Grounding and execution were authorized by the retained owner brief.

## Question

Within the integrated model's declared domains and assumptions, which selected design changes improve conditional LCOE, what limits them, and how sensitive are those conclusions to missing physics and cost assumptions?

## Consumer

[OWNER] The project owner needs reproducible comparisons and engineering findings for the integrated ARIES model and write-up.

## Answered when

[INHERITED: evidence/owner-brief.md] Baseline replay and dependency audit support a small set of justified axes; successive local-response, coupled-design and assumption-robustness studies deliver complete attempted cases, plots, exact parameters, price/capability propagation, adverse outcomes and independent selected-case replay. A bounded conclusion of no supported improvement is acceptable. The final answer identifies reused machinery, actual adaptations, scientific limits, unmatched source comparisons and replay commands.

[OWNER-VERBATIM] “Keep both tritium-supply scenarios visible. For every candidate, report net electricity, gross tritium requirement, assumed breeder feed, external purchases and LCOE contributions. Separate improvements in physical performance or purchased equipment from improvements caused by crossing the assumed fuel-supply threshold. Do not optimize supplied breeder output, its service charge or unsupported efficiency assumptions.”

## Invariants

- [INHERITED] Preserve Stellaris models, shared definitions, packages, inputs and frozen evidence; entry digest manifest and isolated behavioral regression are separate obligations. Preserve the two unrelated untracked files recorded at entry.
- [INHERITED] Use the reviewed native integrated assembly and exact generated package. Baseline remains the **423.106794 MW assumed integrated baseline**, with original source-case failures retained. No silent retuning. No caller-side plant model or hidden equipment sizing.
- [INHERITED] MR-1–MR-7 and applicable process requirements govern any refinement. Selected equipment stays independent of demand; inventory, purchase costs and operating demand must trace to actual native bindings. Analysis-specific variable roles and unsupported domains are explicit. No design-role change is authorized by existing code alone.
- [OWNER] Every physical candidate retains no-breeding-credit (new feed 0, incremental service 0) and assumed new breeder feed (100 kg/calendar year, 30 million USD2004/year service) scenarios. Exhaust recycling is already accounted for; gross makeup and external purchases remain distinct. Feed/service are fixed scenarios, never optimization levers. Unsupported efficiencies may only receive declared sensitivity treatment.
- [INHERITED] Constant USD2004 lifecycle boundary, one construction-financing adjustment, dated replacement cashflows excluding the reserve, complete terminal expenses and salvage. Physical/equipment changes and fuel-threshold effects are reported separately. No point is called feasible while material qualification is unverified; use passes evaluated checks.
- [INHERITED] Post-reveal development; retained primary evidence permitted. Preserve historical hold-out evidence and source policy. No arbitrary reuse percentage or global-optimum claim.

## Grounding evidence

- `work/orchestration/aries-transfer-experiment/report.md`, `change-register.md`, `log.md`, `scientific-prerequisites.md`, `evidence/integrated-review.md` @ `16c3c3ebb4266fd83a9e90ddc76762cebeed3572`: original transfer architecture and unqualified boundaries.
- `work/orchestration/goals/aries-integrated-lcoe/answer.md` @ `289083b4592c8b9897716e0c926ebb4f3ad5f8ca`: reviewed lifecycle package, scenario accounting and source mismatches.
- `work/completed/20260922_WI-091_aries-integrated-lifecycle-cost/evidence/interface-handoff.json` and `design.md` @ `289083b4592c8b9897716e0c926ebb4f3ad5f8ca`: actual interfaces, assumption register and reuse account.
- `exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/record.md` @ `3f521955`: sealed 64-point predecessor study and immutable snapshot; accepted thermal/equipment predecessors remain linked there.
- `evidence/owner-brief.md` and `evidence/owner-supplement.md`: retained present authorization, initially unpinned; no native digest until grounding commit.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) per failed task |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional wall-clock cap; at most one promoted package and one committed study per round |

## Reserved gates

[OWNER] Changes to stated modeling intent, Stellaris changes, external messages, push/merge and formal goal/item closure. Routine transparent assumptions and local commits are authorized. Scientific qualification cannot be inferred from implementation checks. Execution caps cannot be silently extended.

## Close rule

Owner-held after the answer contract and applicable independent review are satisfied. Completion recommendation does not close or archive the goal/item.

## Amendments

None.
