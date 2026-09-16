# Goal: Magnet manufacturing-cost completeness

[AGENT] Prepared 2026-09-15 from the native goal template. Owner-confirmed slug: `magnet-manufacturing-cost-completeness`. Owner requirements below come from the initiating request in this session; inherited evidence and execution choices retain their own provenance.

## Status

`grounded` — owner confirmed the proposed slug and instructed “proceed” on 2026-09-15. The initiating request supplies the objective and authorization to pursue it.

## Question

[OWNER] What do the modeled magnet procurement and manufacturing charges cover, which overlaps can be demonstrated and removed, and which missing costs can be estimated or made explicit using admissible evidence and current conductor/pack geometry?

## Consumer

[OWNER] The model owner needs an economically coherent component estimate with traceable quantities, rates and account boundaries. The objective is neither a factory quotation nor a cheaper design.

## Answered when

- [OWNER] Every affected cost term has a clear quantity basis and account boundary. An account map identifies quantities, unit rates, included operations, exclusions, price years and evidence.
- [OWNER] The account map distinguishes complete composite tape and its constituent materials; external conductor/cable materials; electrical insulation, impregnation and assembly allowances; winding operations; coil casing and other electromagnetic supports; and nonmagnet infrastructure.
- [OWNER] Demonstrated overlaps are removed without silently deleting required scope. Uncertain boundaries remain identified as uncertain.
- [OWNER] Quantified insulation or cable additions follow the modeled construction and avoid counting tape constituents twice. Remaining costs appear as explicit assumptions or unresolved quantities.
- [OWNER] Winding-operation changes have a stated evidence basis and applicability. Unsupported effort remains visible as an unresolved term or clearly labeled sensitivity model.
- [OWNER] Material, fabrication and total-cost subtotals reconcile. Material quantities remain separate from unit-price uncertainty. Price years are normalized where defensible; unresolved bases remain disclosed.
- [AGENT] Deliver a source-linked answer, native implementation/validation evidence for any changed calculations, and independent coverage of new source interpretations, equations and account interfaces. If evidence supports only a bounded negative for an addition or effort driver, report that limit and its effect on completeness explicitly.

## Invariants

- [AGENT] Package: record the entering implementation at `10fd10a059c48d5a3781d7e2c28c16570deaa2fe` and use exact native package identities for any comparison. Prior frozen studies remain historical evidence; attributed cost deltas use matched current physical inputs.
- [OWNER] Comparison: completeness and coherent accounting define improvement. Lower cost is not the objective.
- [OWNER] Use the current physical conductor and pack geometry consistently. Geometric clearance does not automatically represent purchased insulation volume.
- [OWNER] Composite tape procurement includes its constituent materials. External cable additions must have a distinct boundary.
- [OWNER] Do not assume material prices include fabrication or add fabrication to an all-in rate. Distinguish demonstrated double counting from uncertain boundaries.
- [OWNER] The existing nonmagnet structural budget is an explicit allowance, not a measured partition of the old aggregate.
- [OWNER] Investigate winding effort against conductor size, turns, joints, geometry and other supported drivers. Implement the simplest defensible response; do not invent a cross-section multiplier merely to make cost rise.
- [OWNER] Keep quantity uncertainty separate from unit-price uncertainty. Mixed-year arithmetic is not a reconciled common-year estimate without a defensible conversion.
- [INHERITED: current geometry/current answers] Preserve the existing fit and current-margin definitions and their adverse nominal results unless a separately justified physical change is explicitly recorded. An accounting correction does not establish buildability.
- [INHERITED: `knowledge/holdout/aries-cs/PROTOCOL.md`] Preserve source quarantine and screen admissibility before external acquisition. No barred or sealed design/cost data may inform this goal.

## Grounding evidence

All paths below are tracked entering evidence at `10fd10a059c48d5a3781d7e2c28c16570deaa2fe`; that commit identifies the cited revision, not the date each result was generated.

- [INHERITED] `work/orchestration/goals/absolute-conductor-current-margin/answer.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: physical tape/conductor inventory joins, current qualification limits and twenty-predicate baseline.
- [INHERITED] `work/orchestration/goals/winding-pack-casing-fit/answer.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: conditional geometry, clearance and adverse nominal fit.
- [INHERITED] `work/orchestration/goals/tape-procurement-consistency/answer.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: complete composite-tape procurement by physical metres, separate external materials and winding operations.
- [INHERITED] `work/orchestration/goals/magnet-coil-realism/answer.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: total electromagnetic support pricing and explicitly assumed nonmagnet infrastructure budget.
- [INHERITED] `work/orchestration/goals/magnet-design-transfer/transfer-claim.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: manufacturing scope gaps and transfer limits.
- [INHERITED] `work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/accounting-research.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: PROCESS conductor-length winding basis, historical price year, CPI proxy, omitted fixed cable expense and uncertain process coverage.
- [INHERITED] `work/completed/20260914_WI-040_winding-pack-mass-cost/design.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe` and `work/completed/20260914_WI-040_winding-pack-mass-cost/audit.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: native design and audit entry points for account reconstruction.
- [INHERITED] `work/active/WI-059_coil-thermal-and-total-support-inventory/design.md@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: total support versus casing-floor boundary, inherited steel-rate scenario and nonmagnet allowance semantics.
- [INHERITED] `models/library/analyses/mfe_winding_pack_cost.sysml@10fd10a059c48d5a3781d7e2c28c16570deaa2fe`: live material and procurement equations, exclusions and additive winding term.

## Limits

[AGENT] Use the native runbook defaults. These are execution bounds, not owner-originated scientific requirements.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional wall-clock limit; each research task declares source/search limits before execution |

[INHERITED: runbook] At most one promoted package pin and one committed study per round. Research tasks return useful evidence or a bounded negative. A source gap does not justify invented coefficients.

## Reserved gates

- [INHERITED: run-goal skill] Confirm the goal slug before creating its directory.
- [INHERITED: runbook] The owner retains goal closure, item closure/archive, merge and push.
- [INHERITED: quarantine protocol] Source-quarantine exceptions or reveal remain owner-held.
- [AGENT] Changes to the stated economic objective, comparison meaning or owner constraints require an owner ruling. Evidence-backed accounting, research and modeling choices within the request proceed under the authorized scope and required independent review.
- [INHERITED: runbook] An unresolved interpretation that changes scientific meaning is surfaced to the owner; independent review cannot substitute for that ruling.

## Close rule

[INHERITED: runbook] The owner closes the goal after the answer contract is assessed against native evidence and required review coverage. The coordinator may recommend closure on a conditional estimate that explicitly exposes unsupported quantities; it must not present missing costs as zero or claim a fully qualified manufacturing quotation.

## Amendments

None.
