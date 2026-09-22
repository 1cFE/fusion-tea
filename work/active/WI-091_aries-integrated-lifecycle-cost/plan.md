---
Status: active
Created: 2026-09-22
Updated: 2026-09-22
---

# Persistent lifecycle implementation plan

Related Artifacts: spec.md; design.md; goal evidence/author-brief.md. Owner: lifecycle author for the files below; coordinator for registration, source-set changes, integration and studies. Preserve concurrent edits. Implementation was released after independent design PASS; current evidence is in report.md.

- [x] Inspect accepted plant/fuel/cost bindings and existing generic finance; capture spec, design, assumption register and reuse decisions.
- [x] Resolve independent source/design findings and obtain coordinator release for the reviewed equation/binding scope. Design PASS and focused source construction guard accepted. Literal-zero experiment produced mutable entry keys; native guard enforces supported domain exactly {0} for source financing.
- [x] Add `models/library/analyses/integrated_lifecycle_costs.sysml`, assembly finance parts and isolated typed completions in `exploration/aries_integrated/native_completions/lifecycle/`; reuse existing DCF and levelization unchanged. Keep selected parameters and predecessor input keys.
- [x] Coordinator registers additive source family; inspect actual CLI help and supported generation route, regenerate only the existing integrated package, populate handwritten adapters and verify fixed point. Use `.codex-test/run` for all Python/modeling commands.
- [x] Record exact generated output IDs, entry-key groups and canonical no-credit/new-feed/source-conditioned cases. Verify source comparison holds recurring and blanket replacement amounts fixed while terminal/overhaul/salvage amounts scale with substituted capital at unchanged fractions and timing; disclose those changed amounts. Run focused tests and preserve adverse outcomes in WI-091 evidence.
- [ ] Run applicable integrated validation and independent behavior review; coordinator checks protected digest manifest and isolated Stellaris replay. Record known inherited validator exceptions with their identities, not a blanket pass.
- [ ] Hand reviewed coherent package and evidence to coordinator for native integration and one-study-per-round execution. Goal studies own financial sensitivity and fixed-hardware dependency evidence; do not mark those complete from unit tests.

| Acceptance | Required verification and expected observation | Basis / evidence |
|---|---|---|
| R1,R3,R7 | Independent explicit cashflow list discounts construction at -T/2, end-year annual payments, dated replacements/overhaul and terminal cashflow. Sum contributions and compare native headline. | Mathematical convention; passed all23 evaluated native cases against independent Decimal dated oracle (`evidence/verification.json`). Relative 1e-10 for positive monetary/energy values and absolute 1e-8 USD/MWh price reconciliation. |
| R2 | R=0 reproduces 104.66770702324638 kg/y external demand at inherited baseline; R=100 gives 4.66770702324638 kg/y. Changing internal recovery changes loss once; fixed R is not recomputed from demand. Oversupply clips purchases and reports curtailment, no sales credit. | Inspected fuel equations and handoff; passed zero/100kg/oversupply/internal-recycle cases in development receipts. |
| R3 | At r=0: PV energy=E*N; IDC=0; costs equal K plus N times annual amounts plus event amounts plus D-S. At T=0 financing factor=1. At N=tau exclude that final replacement. No reserve input reaches headline. | Analytic identities; passed zero-rate/zero-construction/horizon exclusion cases. |
| R3,R5 | Terminal-only perturbations have delta LCOE=`delta(D-S)*(1+r)^(-N)/(E*H)`. Other-overhaul date crossing N removes exactly that event; changing salvage decreases price without changing gross terminal cost. | Timing convention; passed terminal/salvage/overhaul timing cases with full contribution comparison. |
| R4,R6 | Native baseline retains 423.10679410931664 MW; test reduced/sufficient supplied HX area or equipment rating, with cost/capability response and source failure visibility; supported demand change at fixed hardware changes power/fuel/price. | Passed native baseline, source controls, insufficient/sufficient selected rating and two fixed-hardware demand perturbations. |
| R5 | Nonpositive P, invalid rates, noninteger/zero N and invalid schedules leave LCOE unavailable. Engineering-failed positive-P case retains finite conditional LCOE and adverse verdict. Supply support remains0 even when new feed covers requirement. | Passed11 actual refusal cases and engineering-failed finite-price case; existing native diagnostic route retains upstream power/predicates and blocked price for3 financial failures. |
| R6,R7 | Protected-file manifest, isolated Stellaris replay, graph census, generation fixed point and exact case identities. No Python caller fills missing advertised outputs. | Build fixed point and exact input/output identities pass; coordinator protected9104 files and Stellaris1352 outputs/68 responses pass. Native promotion remains coordinator-owned. |
| R8 | Fixed-design r/N/A/cost sensitivities have expected direction except explicit event-count discontinuities; energy/fuel share A and replacement timing changes consistently. | Independent dated development oracle passes; native study evidence remains pending. |

## Current state

Implemented at e44a0ded. Native development verification passes 34 cases (23 evaluated, 11 expected refusals), plus existing-route diagnostic retention for three actual financial failures and exact baseline parity. Generation fixed point passes. Complete validator retains 4 passed/2 failed with exact identities documented in report.md. Independent behavior review is underway; integration and native study evidence remain coordinator/study-worker responsibilities. The independent Decimal oracle is verification only.

Native financial refusal controls must be retained as separate failed attempts beside completed study points, following the design's execution contract. They must not be converted to finite sentinel prices to satisfy study gates. Coordinator entry evidence already establishes 9,104 protected files unchanged and 1,352 Stellaris numeric outputs/68 responses exactly replayed; repeat the preservation check after the delivered increment, reusing the baseline receipt.

Development rows in the acceptance table are evidenced by `evidence/verification.json`, `evidence/development-cases.json`, `evidence/diagnostic-verification.json` and `report.md`. The zero-output fail-fast refusal limitation is explicit and supplemented by separate native diagnostic receipts. Study-dependent sensitivity and sealed integration outcomes remain pending their owning records.
