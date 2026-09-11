---
Status: active
Scale: standard
Epic: IFE Cost Modeling
Owner: reid
Created: 2026-09-11
Updated: 2026-09-11
---

# WI-049: IFE zero-discount repair

## Overview and authority

Correct IFE present-value evaluation at zero and nearby signed discount rates. Discounted cost and energy must each be accurate before their quotient can certify an eligible price.

[INHERITED: work/orchestration/ife-zero-discount-repair.md] The owner authorized the grounded `fusion-audit-remediation` goal with “yes ground and proceed.” The parent accepted this bounded Standard scope for round 2 T-010. Numerical requirements below are agent-derived, not owner-originated settled policy; ordinary stage acceptance belongs to the parent.

[INHERITED: modeling_project/OVERVIEW.md] This serves RQ-2 (credible LCOE and its assumptions) and RQ-5 (parameter sensitivity), under the IFE Cost Modeling epic. The project uses RQ identifiers here, not G/AQ identifiers. DI-003 and DI-005 supply the existing target-cost and parameter context. The epic's historical broad LCOE ranges do not certify this numerical limit or require tuning the current baseline.

## Current state

[INHERITED: work/analysis/20260911-141041_ife-zero-discount-assessment.md@692c9f94] Actual sealed execution fails at zero before the price guard and loses cost/energy precision nearby. At 1e-12 the separate quantities err by about 0.00889% while the quotient nearly agrees. The retained 42-case probe and independent 80-digit dated sums establish the defect; these are inherited measurements, not fresh checks by this spec author.

- `models/library/analyses/ife_lcoe.sysml:118` computes construction and operation present-value factors through subtractive power expressions divided by the rate; `:137` exposes their discounted cost and energy. Duration inputs at `:50` are Real.
- `models/library/analyses/ife_lcoe.sysml:141` defines the guarded price contract. `models/designs/generic_ife/ife_plant.sysml:141` binds it. WI-048 already repaired the operating point and strict net-generation rule; its [spec](../WI-048_ife-operating-point-repair/spec.md), [design](../WI-048_ife-operating-point-repair/design.md) and [audit](../WI-048_ife-operating-point-repair/audit.md) are inherited dependencies.
- `exploration/ife_e2e/generated/handwritten/ife_lcoe/ife_lcoe_impl.py:171` is the assessed failing execution. `tests/ife_oracle.py:62` handles only integer durations; that testing restriction is not the production model's domain.

## Modeling requirements

All rows are [INFERRED], priority Must. They derive from the authorized repair, the assessment and the cited existing contracts. No requirement is proposed for project-wide promotion.

| ID | Type | Requirement | Rationale and source | Verification |
|---|---|---|---|---|
| MR-WI049-1 | Functional | The model SHALL evaluate the existing Hawker construction and operation streams at exact zero discount using their continuous finite limits, retaining construction payments in years 1 through Yc and operation payments/energy in years Yc+1 through Yc+Nop for integer durations. | F05 assessment; Hawker Eq. 2.1; AD-003; RQ-2. | Independent high-precision dated annual sums, including cost and energy separately; SV-076. |
| MR-WI049-2 | Quality | The model SHALL return finite discounted cost, discounted energy and eligible Hawker price agreeing independently with the reference to relative error at most 1e-9 for each nonzero expected quantity across the acceptance cases below. For a true-zero expected numerical channel, absolute error SHALL be at most 1e-9 in that channel's stated units. | Near-zero cancellation evidence; project MR-5; RQ-2/RQ-5. | SV-076/SV-077; tests must fail on the original cancellation and singularity, even when the price ratio alone agrees. |
| MR-WI049-3 | Functional | The model SHALL preserve Real-valued duration inputs and the existing non-integer algebraic extension, including A(n,0)=n. The design SHALL justify its rate/duration test window, numerical error and any approximation or switching behavior against an independent high-precision reference. | AD-001/AD-003; assessment fractional probe; alignment. | SV-077: fractional durations plus broader design-selected cases; probe both sides and the exact point of any numerical switch. |
| MR-WI049-4 | Constraint | The model SHALL retain strict actual net power > 0 for generation, invalid zero price and generating=0 for non-generators, and consumer eligibility requiring generating=1 plus satisfied net_positive. Zero and negative net cases SHALL complete their diagnostic cost/energy calculation at the required discount rates without becoming eligible priced generators. | WI-048 MR-WI048-5/-7 and current guard; assessment; RQ-2. | SV-076/SV-078: exact verdicts, flags and invalid sentinels; separately verify signed/zero energy and cost. |
| MR-WI049-5 | Functional | The model SHALL preserve the existing cost streams, annual time constants, dollar bases, replacement charges, power balance, Meier method and comparison labels. At the ordinary 8% baseline it SHALL reproduce each existing numerical output within the stated tolerance and preserve exact verdict/eligibility outcomes. | Hawker Eq. 2.1; WI-048 contract; alignment finance reservation; project MR-5. | SV-078: before/after channel comparison and independent baseline arithmetic; any unexpected movement is investigated. |
| MR-WI049-6 | Quality | The model SHALL carry the repair into the native generated IFE execution and synchronized IFE family copies, preserving native signatures, seals and repeatable regeneration, with scoped regression tests and a positive independent item audit. | Project MR-3/MR-6; WI-048 typed completion precedent; MODELING_PROCESS.md Standard completion rule. | Prototype installed-toolchain execution before production changes; native loader/regeneration and affected consumer tests; Levels 1–3 pass, Levels 4–6 reported with inherited debt distinguished. |
| MR-WI049-7 | Traceability | The model SHALL document the numerical limit and chosen evaluation's derivation with resolving Source/Ref/Basis citations while preserving the source's financial interpretation. | Project MR-4; AD-003; registered Hawker extraction. | Design and independent audit inspect model comments and directly affected traceability records. |

## Acceptance cases

[INFERRED] SV-076 uses the assessment's three operating points (baseline, exact zero net, negative-net counterexample) at 0.08, 0, and both signs of 1e-4, 1e-8, 1e-12, 1e-14, 1e-16 and 1e-18, with durations 5 and 40. The retained [probe](../../analysis/20260911-141041_ife-zero-discount-assessment/probe.py) and `tests/ife_oracle.py` BASE/BOUNDARIES locate the exact inputs. These are required regression referents. Expected cost and energy come from independently reconstructed annual quantities and explicitly dated high-precision sums, not from generated finance expressions. Price comparison applies to eligible generators; non-generator sentinel checks are exact.

[INHERITED: assessment@692c9f94] The generating zero-rate reference is discounted cost 58,111,257,843.81798 dollars, energy 274,751,655.94285715 MWh and price 211.50466825904758 dollars/MWh. At 8%, the references are 13,415,949,859.392101 dollars, 55,744,991.73561758 MWh and 240.66646063955096 dollars/MWh. These displayed numbers are anchors; verification uses full-precision independent references.

[INFERRED] SV-077 repeats the required rate grid for durations 5.5 and 40.5 at the same three operating points, then adds design-justified duration/window and transition probes. Fractional expectations use an independently implemented high-precision evaluation of the current algebraic extension, distinctly labeled from the integer dated-cashflow oracle. Neither fractional-year cash-flow timing nor new duration/rate bounds are established by this check.

[INFERRED] SV-078 verifies the inherited price exclusions through actual generated execution and supported consumers, the ordinary baseline, and preservation of Meier and unaffected channels. The positive neighboring boundary case from WI-048 is also checked at zero, both signs of 1e-12 and 8% so the repair cannot pass by suppressing all prices. Every nonzero expected output uses the same relative tolerance; no absolute floor substitutes for relative checks on small nonzero outputs.

[INHERITED: native PM registration, 2026-09-11] SV-076, SV-077 and SV-078 are pending in `modeling_project/VALIDATION_MATRIX.md`. Historical certifications remain unchanged. Completion requires the scoped tests and model checks in MR-WI049-6 plus fresh independent audit; a passing price-only comparison is insufficient.

## Scope boundaries

[INFERRED] The primary change surface is `models/library/analyses/ife_lcoe.sysml`. Direct IFE wiring, synchronized IFE family copies, generated artifacts under `exploration/ife_e2e/generated/`, affected tests and verification scripts, and direct citations are supporting scope. Reusable numerical definitions belong in library analyses; designs retain case bindings. The design selects the smallest feasible implementation.

[INHERITED: alignment] Out of scope: financial normalization, new supported-domain policy, rates at or below -1 and zero construction-duration policy, shared MFE changes, source/research approval, project-requirement changes, residual acceptance, the pending plant-closure comparison, study metadata/pins/execution, merge/push, close/archive and goal close. Source conflicts or required semantic changes return to the parent before dependent work proceeds.

## Assumptions and risks

1. [INHERITED: WI-048 design:72] The pinned renderer rejected conditional arithmetic. Likelihood of the same limitation: high; impact: implementation feasibility. Design must prototype early; model-level conditionals or stable special functions are not assumed available. A missing shared seam capability is a prerequisite returned to the parent. A bounded typed handwritten completion, if selected, needs an explicit regeneration and numerical-verification design.
2. [INHERITED: assessment] The registered Hawker extraction supports the dated streams and finite zero limit. Confidence: high in the algebra; this stage makes no fresh image-certification claim. An equation transcription conflict discovered during design is surfaced, not silently resolved.
3. [INFERRED] A local series may be inaccurate for large duration-times-rate products or across its switch. Likelihood depends on the chosen scheme; impact: false continuity evidence. The design must justify error and test window without turning evidence bounds into domain policy.

## Traceability and next artifacts

- [INHERITED] Domain source: `knowledge/SOURCE_INDEX.md:28`; `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141` (Eq. 2.1), `:148` (construction and operation durations), and following annual streams. The assessment records the derivation and current executable identity.
- [INHERITED] Governance: `work/orchestration/ife-zero-discount-repair.md`; `work/orchestration/goals/fusion-audit-remediation/{goal,trail}.md`; `work/backlog/epic-ife-cost-modeling.md`; `modeling_project/REQUIREMENTS.md` MR-3/4/5/6 and PR-4/5; `modeling_project/ARCHITECTURE.md` AD-001/003/004/006. Parent owns stage commits.
- [INFERRED] Next: `design.md` with early prototype evidence, then `plan.md`, implementation evidence and independent `audit.md`. Downstream impact is the generic/HIF IFE family and supported execution consumers; study refresh and pin promotion are separate tasks.

## Parent stage acceptance — 2026-09-11

[AGENT] Accepted for design under the grounded goal and inherited alignment. The seven requirements preserve the comparison basis while making separate cost/energy accuracy and fractional algebra explicit. SV-076–078 remain pending until native implementation evidence exists. No owner-reserved decision was exercised.
