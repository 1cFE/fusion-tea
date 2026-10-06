---
Status: complete
Updated: '2026-10-06'
---

# WI-098 implementation plan

[AGENT] Persistent native checklist. Scope and acceptance are in spec.md; implementation waits for the independent design gate.

- [x] Establish exact configuration, disjoint account mapping, monetary convention and variable-role/binding design from T-001 evidence.
- [x] Obtain independent source/math/interface review; resolve findings within the declared revision cap.
- [x] Implement additive SysML and native package; retain existing model/package bytes.
- [x] Exercise prior controls, new power/fuel/cost balances, insufficient/sufficient hardware, unsupported and nonpositive-net cases; independently verify outputs and predicates.
- [x] Obtain substantive integration review; prepare generated fixed point, source/body census, validation dispositions and native study interface.
- [x] Deposit report and exact replay commands; hand off for native integration and whole-plant study.

## Implementation notes

2026-09-27: Registered WI-098 through native pm add-item. Spec captures owner endpoint. Existing source and conversion inventories are under bounded investigation; no production edits yet.

2026-09-27: R2 design gate PASS at 81423599; boundary-review-r2.md records MR-7 design compliance. Exact 48 kA capture and isolated implementation released. Gas transport overhead wording clarified per nonblocking review note.

2026-09-27 implementation: exact 48 kA capture retained with all full-plasma failures. Focused cryogenic demand/sink and selected-offer corrections passed independent review. Isolated package 6915694e…/bb284160… passes two-pass fixed point with 16 sources/39 body receipts. Final 35 native cases independently checked:32 evaluated × 1192 scalars and 125 predicates; 3 expected refusals; 88 behavior checks. All 498 legacy controls passed under the frozen package: [comparison](evidence/conversion-controls/comparison.json) records exact equality for 872 inherited channels and 84 predicates per case; [independent summary](evidence/independent-verification/controls-summary.json) records all 498 cases passing the 1192-channel and 125-predicate check. Six-level validation retains 72 L2 and 1174 L6 diagnostics; [per-identity disposition](evidence/validation-detail.json) records zero unresolved items.

2026-09-27 integration: independent implementation-integration-review.md passed the complete boundary and executed MR-7 checks. Native integration returned CANDIDATE with all ten gates passing at 3deafc4e. Report and study replay instructions were deposited. The first main study is preserved as blocked at verification, commit 275ba13c; goal Round 2 now independently adjudicates oracle root precision and cryogenic diagnostic spacing. Formal item closure remains owner-held.
