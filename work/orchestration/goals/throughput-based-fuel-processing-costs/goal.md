# Goal: Throughput-based fuel-processing costs

## Status

`closed` — 2026-09-19. [OWNER-VERBATIM] “Please close the goal”. Closed on the independently reviewed R10.S2 result, audited model `2a50d3ec` and committed study `2bae7fb7`. See [closure record](trail.md#goal-closure--2026-09-19) and [independent grade](evidence/final-review-and-grade.md). The conditional processing scope and remaining limitations are retained.

## Question

[OWNER] Can we make the cost of the fuel-processing plant follow its calculated processing demand, using applicable cost sources and explicit equipment boundaries?

## Consumer

[OWNER] The project owner needs the existing R10.S2 target met before the ARIES comparison. The answer must explain the represented processes and unpriced scope to an engineer without project background.

## Answered when

[OWNER-VERBATIM] “Processing-plant cost follows computed throughput with source basis.” The unchanged R10.S rubric receives a fresh independent grade tracing verified fuel flows through applicable source relationships to integrated plant capital and electricity cost. The evidence includes an equipment/account boundary map, source applicability assessment, reference reproduction, accounting checks, generated execution, regressions and a focused native study separating throughput effects from price and process assumptions. Aggregate process costing is acceptable for S2. A documented blocker or unsupported number does not close the gap. Full requirements are retained verbatim in evidence/owner-prompt.md.

## Invariants

- [OWNER] Preserve the published r2 archive, historical results, existing rubric and fuel-system requirements; identify new versions and studies separately.
- [OWNER] Keep ARIES sealed under knowledge/holdout/aries-cs/PROTOCOL.md and exclude .project/concepts/stellarator-mbse-demo.md and all barred derivatives.
- [OWNER] Use actual architecture and verified isotope-specific flows. Preserve fuel-loss assumptions; annual availability cannot reduce running equipment capacity. Do not duplicate mass balances or overlap capital, fuel purchases and startup stock.
- [OWNER] Keep S2 scope; detailed process design, breeding-gap repair, facilities sizing and full self-sufficiency are outside scope. Preserve failing plant cases and disclose unsupported terms.
- [OWNER] Native research, modeling, integration and studies use .codex-test/run. Preserve unrelated work; no merge or push.

## Grounding evidence

- [OWNER] evidence/owner-prompt.md (copied from /tmp/run-goal-fuel-processing-costs-prompt.md; unpinned; no native digest).
- [OWNER] .project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d.
- [OWNER] work/analysis/20260918-192403_stellarator-depth-reassessment.md and companion .cells.json (unpinned; no native digest).
- [INHERITED] work/orchestration/goals/plant-closure/ and work/orchestration/goals/pre-reveal-feasible-neighborhood/@86333b0de799e2332c01d489d400f8028bdb6d87.
- [INHERITED] work/orchestration/goals/fuel-inventory-and-startup/answer.md and evidence/throughput-interface.md@86333b0de799e2332c01d489d400f8028bdb6d87 identify the completed upstream producer; study pin 3529f6c8, audited model 956444b5. Confirm implementation before consuming it.

## Limits

[AGENT] Execution defaults from the native runbook:

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional limit |

## Reserved gates

[OWNER] Reveal, replacement of the frozen comparison, major scope or process-technology changes, material scientific decisions and formal goal closure remain owner-held. No merge or push. Existing authority permits research, model implementation, package generation, targeted studies and independent reviews without renewed approval.

## Close rule

[OWNER] Only the owner formally closes the goal after reviewing its independently supported answer.

## Amendments

### Amendment 2026-09-19 — resolves process-adoption gate

[OWNER-VERBATIM] “yes, adopt and continue”. The owner authorizes adopting the reviewed conditional conventional cleanup/cryogenic-separation cost basis and continuing implementation. [AGENT] (ratified by owner, 2026-09-19) The process/feed and four-row pricing assumptions retain their agent provenance and the limitations in evidence/proposed-cost-scope.md; approval does not certify feed purity, recovery, completeness or commercial qualification. All other reserved gates and invariants remain unchanged.

### Amendment 2026-09-19 — owner closes the goal

[OWNER-VERBATIM] “Please close the goal”. The owner exercises the close rule after the delivered answer and independent R10.S2 PASS. The status above records this closure; other reserved decisions remain separate.
