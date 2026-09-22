---
Status: draft
Created: 2026-09-22
Updated: 2026-09-22
---

# Persistent lifecycle implementation plan

Related Artifacts: spec.md; design.md; goal evidence/author-brief.md. Owner: lifecycle author for the files below; coordinator for registration, source-set changes, integration and studies. Preserve concurrent edits. Implementation is pending independent review/release.

- [x] Inspect accepted plant/fuel/cost bindings and existing generic finance; capture spec, design, assumption register and reuse decisions.
- [ ] Resolve independent source/design findings and obtain coordinator release for the reviewed equation/binding scope.
- [ ] Add `models/library/analyses/integrated_lifecycle_costs.sysml`, assembly finance parts and isolated typed completions in `exploration/aries_integrated/native_completions/lifecycle/`; reuse existing DCF and levelization unchanged. Keep selected parameters and predecessor input keys.
- [ ] Coordinator registers additive source family; inspect actual CLI help and supported generation route, regenerate only the existing integrated package, populate handwritten adapters and verify fixed point. Use `.codex-test/run` for all Python/modeling commands.
- [ ] Record exact generated output IDs, entry-key groups and canonical no-credit/new-feed/source-conditioned cases. Run focused tests and preserve adverse outcomes in WI-091 evidence.
- [ ] Run applicable integrated validation and independent behavior review; coordinator checks protected digest manifest and isolated Stellaris replay. Record known inherited validator exceptions with their identities, not a blanket pass.
- [ ] Hand reviewed coherent package and evidence to coordinator for native integration and one-study-per-round execution. Goal studies own financial sensitivity and fixed-hardware dependency evidence; do not mark those complete from unit tests.

| Acceptance | Required verification and expected observation | Basis / evidence |
|---|---|---|
| R1,R3,R7 | Independent explicit cashflow list discounts construction at -T/2, end-year annual payments, dated replacements/overhaul and terminal cashflow. Sum contributions and compare native headline. | Mathematical convention; evidence pending. Relative 1e-10 for positive monetary/energy values and absolute 1e-8 USD/MWh price reconciliation. |
| R2 | R=0 reproduces 104.66770702324638 kg/y external demand at inherited baseline; R=100 gives 4.66770702324638 kg/y. Changing internal recovery changes loss once; fixed R is not recomputed from demand. Oversupply clips purchases and reports curtailment, no sales credit. | Inspected fuel equations and handoff; evidence pending. |
| R3 | At r=0: PV energy=E*N; IDC=0; costs equal K plus N times annual amounts plus event amounts plus D-S. At T=0 financing factor=1. At N=tau exclude that final replacement. No reserve input reaches headline. | Analytic identities; evidence pending. |
| R3,R5 | Terminal-only perturbations have delta LCOE=`delta(D-S)*(1+r)^(-N)/(E*H)`. Other-overhaul date crossing N removes exactly that event; changing salvage decreases price without changing gross terminal cost. | Timing convention; evidence pending. |
| R4,R6 | Native baseline retains 423.10679410931664 MW; test reduced/sufficient supplied HX area or equipment rating, with cost/capability response and source failure visibility; supported demand change at fixed hardware changes power/fuel/price. | Existing WI-089/090 checks and new native propagation; evidence pending. |
| R5 | Nonpositive P, invalid rates, noninteger/zero N and invalid schedules leave LCOE unavailable. Engineering-failed positive-P case retains finite conditional LCOE and adverse verdict. Supply support remains0 even when new feed covers requirement. | Definedness contract; evidence pending. |
| R6,R7 | Protected-file manifest, isolated Stellaris replay, graph census, generation fixed point and exact case identities. No Python caller fills missing advertised outputs. | Coordinator evidence pending. |
| R8 | Fixed-design r/N/A/cost sensitivities have expected direction except explicit event-count discontinuities; energy/fuel share A and replacement timing changes consistently. | Independent dated oracle plus native study evidence pending. |

## Current state

Design only. No model, completion, registry, package or study changed by this task. Source reviewer has confirmed that Lyon inclusive capital already contains financing/escalation and that original calendar/discount semantics remain unresolved. Await its durable evidence and independent design review. Independent mathematical oracle is verification only and must not become a second production plant model.

Native financial refusal controls must be retained as separate failed attempts beside completed study points, following the design's execution contract. They must not be converted to finite sentinel prices to satisfy study gates. Coordinator entry evidence already establishes 9,104 protected files unchanged and 1,352 Stellaris numeric outputs/68 responses exactly replayed; repeat the preservation check after the delivered increment, reusing the baseline receipt.
