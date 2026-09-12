---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-12
Updated: 2026-09-12
---

# WI-052: MFE financial rate limits

## Overview and authority

Repair removable zero/equal-rate singularities and nearby cancellation in MFE common finance and replacement costs. Preserve the existing financial meanings and plant state, and verify the quantities before they combine into prices.

[INHERITED: work/orchestration/mfe-financial-rate-limits.md@f0bbb7e7] This is Round 7 T-029 under `fusion-audit-remediation`, following the owner instruction “yes re-ground and continue.” The bounded item and numerical acceptance choices are agent-derived, not owner-originated settled policy. Routine stage acceptance belongs to the parent. The [routing response](stage-provenance/spec-routing.md) parks construction-duration zero without establishing a new supported-domain restriction.

[INHERITED: modeling_project/OVERVIEW.md; work/backlog/epic-mfe-cost-modeling.md] This serves RQ-2 (credible LCOE assumptions), RQ-3 (shared finance calculations), and RQ-5 (sensitivity). This project uses RQ identifiers here rather than G/AQ identifiers. DI-002 provides the shared CAS context; no captured insight establishes a different finance limit. The epic's historical broad validation targets do not authorize source adoption or baseline tuning.

## Current state

[INHERITED: work/analysis/20260912-fusion-audit-current-assessment.md@bfc60b91 and its T-028 F01–F07 evidence note] F05 remains partially repaired: WI-049 repaired IFE factors; the MFE shared annuity, DCF, IDC, and held replacement expressions remain singular. Live-calendar exact-zero CRF already exists but nearby cancellation is unverified. These are inherited findings. This spec session inspected the current scoped source and derived the identities below; it did not rerun the original probe or certify production behavior.

- `models/library/analyses/mfe_account_costs.sysml:665` divides closed-form IDC by interest times construction duration. At `:717` the shared annual-cost calculation divides CRF by a power difference and growing-annuity PV by interest minus escalation. Its public outputs are `crf` and `levelized`.
- `models/library/analyses/mfe_lcoe_dcf.sysml:46` repeats the singular CRF; its public output is `lcoe`. Headline construction finance uses the midpoint factor.
- `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:52` has exact-zero live CRF but direct powers nearby. The held branch at `:70` has singular geometric PV and CRF even for zero events. The calendar's normative declaration is `models/library/analyses/mfe_lifecycle.sysml`.
- `models/designs/generic_mfe/mfe_plant.sysml:983` reports closed-form IDC separately; `:1191` computes headline DCF; `:1215` constructs comparison CAS90 from shared CRF and overnight plus reported IDC. CAS71/CAS80 share annual-cost levelization, while calendar CAS72 feeds CAS70. The native descendant is `models/designs/stellarator_09/stellarator_plant.sysml` and its generated stellarator package.

## Mathematical contract

[INFERRED] The equations here derive from the current source expressions, not from a new economic model. Let `i` be interest/discount, `g` escalation, `N` operating duration, `T` construction duration, and `A1 = annual_cost*(1+g)^T`. For integer N, the shared PV is the explicitly dated sum `sum(A1*(1+g)^(k-1)/(1+i)^k, k=1..N)`. Its existing Real-duration extension is retained.

| Quantity | Exact rate-limit identity |
|---|---|
| Capital recovery factor | `CRF(0,N)=1/N` |
| Shared annuity at equal rates | `PV(i,i,N)=A1*N/(1+i)`; levelized cost remains `CRF*PV` |
| Shared annuity at both rates zero | `PV=annual_cost*N`, `levelized=annual_cost` |
| Closed-form IDC at zero interest and positive Real T | `f_idc=0`, hence `cost=0` |
| Headline DCF at zero discount | `(total_capital/N + annual_om)/(8760*net_electric_mw*availability)`; midpoint IDC factor is 1 |
| Replacement at zero interest | `replacement_pv=event_cost*event_count`; `cas72_annual=replacement_pv/N` |
| No replacement events | `replacement_pv=0`, `cas72_annual=0`, including exact-zero interest |

[INFERRED] The construction-duration limit is different: writing the current IDC numerator as `exp(T*log(1+i))-1` gives `lim(T→0) f_idc = log(1+i)/i - 1` for nonzero i. It is generally nonzero and negative at positive i. Assigning zero at T=0 would change the formula's meaning. Under the routing response this extension stays parked; positive Real T and its zero-interest limit remain in scope. This is an unresolved timing question, not permission to reject previously accepted inputs or a declaration that all other domains are validated.

## Modeling requirements

All priorities below are P0. Each requirement is agent-derived `[INFERRED]` unless its preservation authority is explicitly inherited. No requirement is proposed for project-wide promotion.

| ID | Type | Requirement | Rationale and source | Validation |
|---|---|---|---|---|
| MR-WI052-1 | Functional | The model SHALL evaluate CRF, shared annual-cost levelization, headline DCF, and reported closed-form IDC at the exact rate limits above, retaining their distinct finance conventions. | F05; current equations; RQ-2. | SV-090; independent identities and original counterexamples. |
| MR-WI052-2 | Quality | The model SHALL evaluate each tested nonzero financial quantity with relative error at most 1e-9 against an independent reference, including tiny nonzero IDC and nearby rate differences. For a truly zero expected quantity, absolute error SHALL be at most 1e-9 in stated units. | F05 cancellation risk; RQ-5; project MR-5. | SV-090/091; separate factors, PV, annual charges and prices; no absolute floor masking small nonzero errors. |
| MR-WI052-3 | Functional | The model SHALL preserve Real-valued operating and construction durations and the current non-integer algebraic extensions while repairing rate limits for positive durations. The design SHALL justify numerical branches, approximations and its test window. | Alignment and routing; AD-001; current Real formals. | SV-090/091; fractional cases and both sides/exact point of numerical switches. |
| MR-WI052-4 | Functional | The model SHALL evaluate live and held replacement PV and annualized costs stably at zero and nearby signed rates, including zero-event cases, without changing held clipping order/count/timing or live event dates, terminal treatment and availability. | Alignment; WI-046 calendar semantics; F05. | SV-091; independently dated finite sums and separate physical/calendar comparisons. |
| MR-WI052-5 | Constraint | The model SHALL preserve current plant operating inputs, physical outputs, verdict outcomes, account meaning, escalation timing, currency bases, and midpoint-headline versus reported-closed-form IDC separation. Ordinary financial roundoff changes SHALL be tightly bounded and attributed. | [INHERITED] alignment/routing; project MR-1/MR-5. | SV-092; explicit before/after ledger and independent financial reconstruction; investigate larger deviations. |
| MR-WI052-6 | Quality | The model SHALL carry the repair through canonical SysML, native family copies, generated execution and actual public direct callers, with unchanged existing public names and output ordering. Validation SHALL demonstrate no new scoped structural/dependency failures and identify inherited failures individually. | Epic codegen goal; project MR-3/MR-6 and PR-3; alignment. | SV-092; family equality, fresh regeneration, direct module and full native execution, scoped regression and six-level differential report. |
| MR-WI052-7 | Traceability | The model SHALL document each repaired expression's algebra, timing and numerical method with resolvable Source/Ref/Basis citations, and supply an output/dependency handoff identifying changed finance channels and independent coverage. | Project MR-4; alignment; F05/F16 distinction. | Audit citations and handoff against native output census; clearly separate independent numerical checks from generated/oracle parity. |

## Acceptance cases

[INFERRED] SV-090 uses rates `0`, `0.02`, `0.08`, and both signs of `1e-4`, `1e-8`, `1e-12`, `1e-16`, `1e-18`. Shared annuity includes exact `i=g` at 0, 0.02 and -0.02; i or g individually zero; and differences of both signs at the small magnitudes around 0 and 0.02. When a requested difference rounds to equality in binary64, record the actual operands and test equality rather than claiming a distinct neighbor. Use operating durations 30 and 30.5 and construction durations 8 and 8.5, plus a design-justified duration window. These are acceptance probes, not supported-domain bounds.

[INHERITED: .project/reports/20260907-fusion-model-audit.md:100 and its evidence/probe.py:36] Required regression referents are the $1M annual stream at i=g=0.02, N=30, T=8 (approximately $1,538,661.774/year) and the zero-discount DCF with $1B capital, $10M annual cost, 1000 MW, availability 0.85, N=30, T=8 (approximately $5.81968/MWh). Rounded historical numbers locate the cases; recomputed high-precision identities supply pass/fail expectations.

[INFERRED] Independent integer references use explicitly dated cash-flow sums, with at least 60-digit arithmetic; fractional references evaluate the retained analytic continuation independently at high precision. IDC near zero needs high-precision expression evaluation or independently derived series because its expected nonzero value is small. Production-helper reuse and the current unstable study oracle do not constitute independent references. Reference arithmetic must account for the actual represented inputs.

[INFERRED] SV-091 covers both calendar modes, ordinary and fractional operating horizons, no events and multiple events, exact-zero and the signed nearby rate grid, plus cases on both sides and exactly at a replacement/event-boundary condition. Held checks retain floor-then-cap clipping, the inner wall-load floor and the existing ceil-derived event count. Live checks retain strict event completion before N, downtime and dated-energy-bin semantics. Check all eleven public calendar outputs; the legitimate infinite physical life at zero wall load is not a failed financial finiteness check. Verify replacement PV and CAS72 independently of their quotient or final LCOE.

[INFERRED] SV-092 runs the current native baseline and native full-plant zero-discount/equal-rate cases in both held and live modes. It also tests direct callers for the four scoped calculations. Capture entering model/package values before modification. Compare physical channels exactly at fixed inputs and financial channels with MR-WI052-2 tolerance plus per-channel attribution. Full-plant ordinary verdicts retain existing feasibility limitations; finite repaired finance does not establish engineering feasibility. Exercise regeneration with preserved manual bodies and inspect helper side effects before execution. Match any inherited validation/regression failure by identity, not just count.

[INHERITED: native PM registration in this spec session] SV-090, SV-091 and SV-092 are pending entries in `modeling_project/VALIDATION_MATRIX.md`. The CLI emitted existing invalid-Type warnings for `rel dev` and `rel dev\`; this spec does not repair those unrelated rows. Fresh independent native audit is required after implementation; this document does not certify a repair.

## Scope and downstream handoff

[INFERRED] In scope: the three library files named above, their existing generic plant bindings as needed, native family mirrors/generated counterparts, scoped mathematical tests, documentation and regeneration evidence. A small reusable factor definition/manual implementation is an available design option, not a prescribed architecture. Keep reusable calculations in the library and concept values in designs under project MR-3. WI-049 is precedent only.

[INHERITED] Out of scope: current study oracle/adapter modification, integration promotion, study execution, historical study/pin edits, currency normalization, new operating/financial scope, source adoption, quarantine reads/hashes, dependency installation, external-checkout writes, residual acceptance and close/archive. Construction-duration zero remains the parked question stated above. Existing broader financial/input-domain deficiencies receive no closure credit from this bounded repair.

[INFERRED] The consumer handoff must enumerate actual generated names and producer edges for `cas71_calc.crf/levelized`, `cas80_calc.crf/levelized`, `idc.cost`, `calendar.replacement_pv/cas72_annual/dated_energy_ratio`, CAS70, comparison CAS90, headline LCOE, and comparison LCOE. It must also account for every other exposed scalar as changed, unchanged or newly added, and identify whether each affected quantity was independently checked or only propagated. Calendar availability continues feeding fuel and both price denominators; finance-only rate changes must not alter calendar event physics. Internal PV/CRF/IDC factors need scoped verification even when not publicly exported. Current consumer coverage limits remain explicit for the subsequent task.

## Risks and related artifacts

1. [INFERRED, high confidence] A final price can appear accurate while its numerator factors are wrong. Separate-factor/PV checks prevent that false pass.
2. [INHERITED, high impact] The held documentation claims verbatim/bit preservation of unstable algebra. Routing permits attributed financial roundoff within tight tolerances while preserving event and physical semantics; amend affected documentation consistently.
3. [INFERRED, medium likelihood] Generated wrappers may retain stale manual bodies. Native regeneration and actual direct-caller proofs are required, with preserved unrelated implementations.
4. [INHERITED, unresolved gate] Construction-duration zero needs a timing/finance decision if pursued. Larger baseline changes, source conflicts or supported-domain changes return to the parent before dependent work continues.

Related artifacts: [alignment](../../orchestration/mfe-financial-rate-limits.md), [spec brief](stage-provenance/spec-brief.md), [routing](stage-provenance/spec-routing.md), [current assessment](../../analysis/20260912-fusion-audit-current-assessment.md), WI-049 spec/audit, and future `design.md`, `plan.md`, and `audit.md` in this item. The current native source is the mathematical authority for this algebraic repair; inherited external citations remain identified as inherited, not freshly source-verified.
