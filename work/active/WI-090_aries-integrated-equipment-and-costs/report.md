# WI-090 native implementation report

[AGENT] The integrated equipment/cost graph executes, with the assumed integrated baseline unchanged at 423.106794 MW net. The canonical cases retain their source-conditioned thermal failures. Development verification passes 66 cases: 54 evaluated and 12 expected domain refusals. Independent integration review and the goal's thermal/cost studies remain separate acceptance work; this report does not close the item or goal.

## Delivered graph and identity

The original `models/designs/aries_cs_integrated/plant.sysml` now owns selected material/package inventories, exchanger area, purchased ratings, pump operating/capacity interfaces, selected fuel stock, disjoint cost leaves and scalar replacement schedules. Ten additive generic calculation definitions and one costed-component specialization implement the extension. Existing source, heat, cycle, capacity, fuel-flow, annual deuterium pricing, annual O&M, indirect/contingency, supplied-purchase and disjoint-budget machinery is reused where its interface fits. New selected-stock arithmetic copies the productive-time/calendar-decay convention; it is not unchanged reuse of the residence-derived inventory calculation.

The final package is `exploration/aries_integrated/aries_integrated`, executable fingerprint `01f8f89c42a98621ff4c6868156d9b7938b7c80102f1c8321b35504ffcc7a021`, semantic fingerprint `10ea8ab0c94ef4bd126465b2bf664a86bc3a38fa892b39591aa3057069f13a6f`. Its census contains 411 entry parameters and canonical execution retains 475 output records. Fifteen canonical source files are staged unchanged into `exploration/aries_integrated/input_models`; build receipts record source/staging hashes, reused completion bodies, typed adapters and a successful smart-regeneration fixed point. All new evidence writes target this WI-090 directory.

The four full canonical maps are in [baseline-execution.json](evidence/baseline-execution.json). [input-migration.json](evidence/input-migration.json) records removed/added keys, retained inputs and changed inherited numeric diagnostics. UA entries become selected area times assumed U; literal pump modes preserve supplied source powers; selected 10 kg stock replaces the dormant zero-stock entry and feeds both required breeding and annual decay. Required-breeding changes are intentional inventory consequences, not changes in burn/exhaust or thermal output. The source parent inputs now have shared owners used by the source total and child comparisons.

## Conditional amounts

All amounts below are USD2004. The installed-direct and overnight figures are declared provisional accounting scenarios, not a sourced installation decomposition or procurement quote.

| Native baseline result | Value | Boundary |
|---|---:|---|
| Net electricity |423.106794 MW| Assumed integrated baseline; scientific qualifications remain unsupported. |
| Source direct budget |2619.572M| Eight printed source parents only. |
| Source inclusive capital |5055.77396M| Source 1.93 factor includes financing/escalation and is not overnight. |
| Provisional direct capital |2919.603M| Source-based selected inventory plus 300M initial T stock; includes 0.031M declared core reconciliation excess. |
| Provisional overnight capital |4350.20847M| Direct plus 20% indirect, 20% contingency on direct+indirect and 5% owner/commissioning; excludes IDC/escalation. |
| Annual operating cost, no T recovery credit |3215.100713M/y| Deliberately pessimistic supplied boundary, dominated by 104.667707 kg/y external T at assumed 30M/kg. Not a breeding prediction. |
| Replacement event cost |72.23135M| Selected blanket/divertor plus 5% LiPb makeup; no permanent magnets/shield or initial-stock duplicate. |
| Replacement interval/count |5.882353 calendar years / 6 events| Selected 5 full-power-year life, availability .85, 40 calendar-year horizon; terminal event excluded. |
| Undiscounted replacement total |433.3881M| Separate from initial capital and annual operations. |
| Replacement reserve |12.2793295M/y| Alternative financial representation; do not add it to event cashflows. |

An independently selected 100 kg/year delivered T-recovery scenario is exercised in development evidence. It lowers purchased fuel without changing breeding support 0. Annual no-credit cost is an assumption-sensitive boundary, not a recommended financial case. An assumption-ranked range and equipment/economic interpretation await the native studies; no economic ranking is made here.

## Native source reconciliation

Source comparisons remain separate from expenses. The graph calculates reactor parent-minus-children 28.396M, core children-minus-parent 0.031M, coil children-minus-parent 5.287M and fuel parent-minus-children 0.001M. Perturbing the source reactor parent changes its comparison gap while leaving selected equipment costs unchanged.

The known selected dry-mass sum including cryostat exceeds printed dry-core mass by 1,333,700 kg. VF-coil mass availability remains 0; this is a partial listed-mass comparison, not an authenticated dry-core reconciliation. Selected total LiPb 8,830,000 kg at 17.1/kg gives 150.993M,334000 below its 151.327M source budget. The source replacement comparison retains 75M/event, 13 events, 842,000 kg/event, 966M printed lifetime cost, 975M rounded product and 9M discrepancy. None of these source-reference products is added again to initial capital or the nominal replacement schedule.

## Verification and limits

[verification.json](evidence/verification.json) and [development-tests.log](evidence/development-tests.log) retain 66 native cases on executable `524c13a905320a5ca35664bdb035043f3588fca22a772503e8383e88f51a0734`. The final citation-only rebuild is covered by [citation-repair-parity.json](evidence/citation-repair-parity.json): all 151 generated/handwritten Python ASTs are unchanged after removing docstrings, both changed SysML bodies are unchanged after removing doc comments, and every input group and output matches exactly across all four canonical cases. The semantic fingerprint is unchanged; the 66-case result is reused with this bounded identity evidence. They check independent energy/state identities, source failures, insufficient/sufficient equipment, purchased quantity/cost response, fixed-hardware density perturbations, separate area/U effects, cubic pump operating response, low/high selected fuel-stock adequacy, shared stock decay/required breeding, source-parent arithmetic, schedule endpoints and negative-electric-export import accounting. Every failed domain case is retained. The zero-heat ledger check is a direct component diagnostic with undefined efficiency and a nonclosing boundary; it is not represented as an acceptable operating point.

The complete validator passes L1 syntax, L3 dataflow, L4 constraints and L5 documentation. L2 reports 103 literal-binding warnings, with zero unbound/undefined/self-named/orphan findings. These literals include sum padding, source reference amounts and conditional scalar-screen flags; they are declared inputs, not unknown costs. L6 reports 407 static-expression/readiness findings (401 unsupported dot-operator diagnostics on EXPOSE attributes and six direct producer forwards) despite successful exact-route generation and native execution. [validation-complete.log](evidence/validation-complete.log) preserves the failing aggregate exit; [validation-diagnostics.json](evidence/validation-diagnostics.json) records individual diagnostics for independent review. This is not a complete-validator pass. The static design-path filter does not inspect all staged files as canonical `designs/` paths; generated exact-route evidence and independent binding review remain necessary.

The first checkpoint's four canonical cases and 63-case verification remain under [checkpoint-a24f9080](evidence/checkpoint-a24f9080/). Initial completion-helper refusals are retained in `initial-execution-refusals.json` and `schema-execution-refusals.json`. They were output-schema/scalar-return interface errors, corrected before successful execution. Later development stops involved expected-error wording after an upstream guard rejected negative inputs; they did not require physical equation changes.

Scientific magnet/conductor, breeding, materials, hydraulic and machine-map qualification stays unsupported. Scalar adequacy and assumed source supply do not upgrade those flags. Fixed package budgets do not respond to demand, and the provisional linear purchase laws are local scenarios. Original Stellaris preservation and isolated behavioral replay are coordinator-owned evidence, separate from this native test result.

## Replay

Use a fresh evidence location when replaying so accepted receipts remain immutable. `execute_case` accepts an explicit output root; the stock command-line runner targets the current WI-090 development directory.

```bash
.codex-test/run bash -c '
  export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
  python work/active/WI-090_aries-integrated-equipment-and-costs/evidence/replay.py
'
```

Independent review should consume the accepted design/source reviews, exact generated binding paths, final 66-case receipt, full validator diagnostics and the retained earlier checkpoint. Native promotion and thermal sensitivity interpretation remain coordinator/study tasks. Formal closure remains owner-held.

## Delivered study evidence — 2026-09-22

[AGENT coordinator] Independent implementation review passes; native CANDIDATE at e8f9cc1d passes all ten gates. The thermal-first study is frozen at494c329e:64points and all17,792scalar/896predicate comparisons, with11adverse cases retained and independent interpretation accepted. The cost-uncertainty study is frozen at8d322312:113points and all31,414scalar/1,582predicate comparisons, with the three source controls still adverse. Every native point ran once. Two bounded export recoveries addressed numeric representation and transient SQLite files without changing proposals, physics or original durable evidence; the complete record retains both failures and the successful copy-query proof.

[AGENT coordinator] The goal answer and `evidence/financial-handoff.md` provide exact selected inventory/cost interfaces, source reconciliation, conditional ranges and replay. Conditional overnight corners span1.623–13.332billion USD2004. Baseline annual operation is3.215billion under no T-recovery credit or215.101million with independently supplied100kg/year recovery, which lacks an incremental recovery-cost/qualification law. These are assumptions, not validated breeding/economic performance.8752protected files remain unchanged and isolated Stellaris behavior matches1352outputs/68responses. Final independent cost/goal interpretation review remains pending; no formal closure is recorded.
