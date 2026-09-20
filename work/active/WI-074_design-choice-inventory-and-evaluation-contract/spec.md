---
Status: active
Scale: standard
Owner: codex
Created: 2026-09-20
Updated: 2026-09-20
---

# Design-choice inventory and evaluation contract

[NEED] Inventory the stellarator model and shared dependencies, then define supported design-variable choices and review actual bindings before production changes. Authority: work/orchestration/goals/preserve-model-design-choices/evidence/owner-prompt.md. MR-7 and its provenance govern this work.

[NEED] Cover physical relationships, units, current and intended roles, policy assumptions, public/generated interfaces, study routes and cost consumers. Use whole-model traversal plus source inspection. Preserve empirical limits and historical evidence. No reference material may inform equations or defaults.

[INFERRED] This item delivers the inventory and independently reviewed evaluation contract; downstream repair items will be scoped from its findings. It cannot certify technical remediation itself.

## Acceptance and execution

- [x] Whole-model parsed traversal and complete generated-interface/binding census retained with source hashes.
- [x] Every relevant subsystem disposition has explicit evidence and unresolved coverage is named.
- [x] Supported calculation directions and selection-policy boundary are explicit, including actual proposed bindings and behavior tests.
- [x] Fresh non-author design review covers MR-7 and original owner intent before production implementation.

Subsystem investigations write the goal's evidence/magnet-inventory.md, cooling-inventory.md and facilities-fuel-inventory.md. Coordinator owns whole-model traversal, native PM, merged contract and reviewer dispatch. Disjoint evidence writes are independent; conclusions are integrated before dependent work. No production changes are authorized by an inventory author alone.

## Current evidence and review boundary

[AGENT] `residual-dispositions.md` and the updated public-parameter coverage CSV cover all entering/current controls with explicit bounded meanings and actual consumers. Final generated census: 597 current, 609 union, 12 retired, 98 introduced, zero unconsumed. Source binding reviews precede WI-075–078 implementation. Residual row dispositions are independently approved; final integrated acceptance remains open; completing the inventory is not self-certification of remediation.
