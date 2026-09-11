---
Status: active
Scale: standard
Epic: IFE Cost Modeling
Owner: reid
Created: 2026-09-10
Updated: 2026-09-10
---

# WI-048: IFE operating point repair

## Overview

Repair audit F01–F03 together: correct the Osiris facts, connect the representations of one IFE operating point, and reject non-generating points using the power balance actually priced. Changed numerical results are expected; lower cost is not an acceptance criterion.

## Goals and authority

[NEED] The owner requested remediation of `.project/reports/20260907-fusion-model-audit.md` through run-goal and approved grounding with “yes ground and proceed” on 2026-09-10. Source: `work/orchestration/goals/fusion-audit-remediation/goal.md`, Objective and Reserved gates; `work/orchestration/ife-operating-point-repair.md` records this item's alignment. The parent orchestrator approved routine spec scope and requirements on 2026-09-10.

[INHERITED] RQ-1, RQ-2 and RQ-5 in `modeling_project/OVERVIEW.md:25-43` motivate credible cost dependencies and sensitivity results; this project uses RQ identifiers rather than an invented G/AQ register. MR-3/MR-4 govern organization and citations. Existing MR-1/MR-2/MR-5/MR-6 obligations remain applicable, but the broader CAS-interface defect F08 is outside this repair.

[INHERITED] `work/backlog/epic-ife-cost-modeling.md` supplies the existing IFE framework and HIF instantiation scope. WI-006, WI-007 and WI-008 implemented it; WI-015 supplied execution evidence. This repair does not re-open the entire epic. DI-003 (per-shot target operating cost) and DI-005 (Hawker framework and frequency/yield sensitivity) inform the dependency checks. DI-001's eta-gain threshold remains an economic heuristic; F03 demonstrates it cannot establish positive electricity generation. No project-wide requirement promotion is proposed; that would require the owner's reserved ruling.

## Current state

- `models/designs/hif_ife/hif_plant.sysml:31-33,78-105,154-175` declares beam energy, two repetition rates, gain, conversion efficiency and separate fixed Meier thermal/net powers. Several purported Osiris values disagree with the source image.
- `models/designs/hif_ife/hif_driver.sysml:70-83` computes procurement cost from beam energy and a rate while holding bank energy independently at 14.286 MJ and efficiency at 0.35.
- `models/library/analyses/ife_lcoe.sysml:54-65,72-89` calculates yield, net power, shots and capital from the bank-energy path. `models/designs/generic_ife/ife_plant.sysml:127-185` exposes driver-only recirculation and the eta-gain viability assertion.
- `tests/models/test_model_family_spines.py:398` expects beam mutation to reach only the Meier consumer. That expectation preserves F02 and must change. Historical mirror/range tests in `scripts/verify_ife_lcoe.py` and `scripts/verify_hif_costs.py` are not independent source validation.

## Modeling requirements

All requirements below are [INFERRED] engineering requirements derived from the owner-authorized repair and cited evidence. They are mandatory for this item and remain challengeable against that evidence. All priorities are Must.

| ID | Type | Requirement | Rationale and source | Validation |
|---|---|---|---|---|
| MR-WI048-1 | Traceability | The model SHALL distinguish image-verified Osiris facts from computed quantities and later assumptions, correct the affected source claims, and preserve printed gain 87 and yield 432 MJ without claiming exact equality between them. | F01; project MR-4; source record below. | Inspect every corrected value and citation against the image; SV-073. |
| MR-WI048-2 | Functional | The model SHALL derive HIF bank energy from one authoritative beam energy and efficiency, with bank_J = beam_MJ × 1e6 / efficiency, and use that bank energy consistently in power, gamma normalization, driver capital and replacement costs. | F02; DI-005; RQ-1/RQ-5. | At baseline and beam/efficiency mutations, check energy identity and gamma × bank_J = Meier driver direct cost in dollars to 1e-9 relative; SV-074. |
| MR-WI048-3 | Functional | The model SHALL use one authoritative operating repetition rate for shot production, power and rate-dependent driver procurement in each modeled operating case. | F02; DI-003/DI-005; RQ-5. | Mutate 4.6 to 5 Hz and verify power, annual shots, driver lifetime and procurement inputs respond coherently; independently calculate the Meier rate factor; SV-074. |
| MR-WI048-4 | Functional | The model SHALL derive the powers used in each operating-point cost chain from that case's declared physical assumptions. If a historical Meier/Osiris reference case remains separate, the model and outputs SHALL name it explicitly and identify its thermal/net-power denominator and differences from the computed case. | F01/F02; RQ-2; goal comparison invariant. | Enumerate both cost channels, their units/year-dollar and finance conventions and exact power/availability inputs. Re-derive each numerical baseline and explain every movement; SV-073. |
| MR-WI048-5 | Constraint | The model SHALL reject net electric power less than or equal to zero as a generating operating point, using the actual power balance priced by the IFE LCOE, independently of the eta-gain heuristic. | F03; RQ-2; DI-001 limitation. | Execute the retained negative-net counterexample, zero-net boundary and positive neighboring point. Require a failed net-generation verdict or explicit domain rejection for non-generators; no successful generating result based on negative LCOE; SV-075. |
| MR-WI048-6 | Functional | The model SHALL expose gross, driver, other parasitic and net electric powers with net = gross − driver − other, and unambiguously distinguish driver-only and total parasitic fractions of gross power. | F03; Hawker balance; RQ-2. | Verify both fraction identities and balance at baseline and mutations to 1e-9 relative. Preserve and identify Hawker's equal driver/cooling allowance; SV-075. |
| MR-WI048-7 | Quality | The model SHALL carry the repaired dependencies and constraint into the supported IFE generated execution path and synchronized family copies, with regression checks that detect the original defects. | F01–F03; MR-6; WI-015 execution evidence. | Run applicable model family, generation, live/snapshot and mutation tests. Separate translation parity from independent arithmetic/source checks; SV-074/SV-075. |
| MR-WI048-8 | Quality | The model SHALL pass blocking validation Levels 1–3 for the affected IFE family, report Levels 4–6, preserve unaffected interfaces where possible, and explicitly account for required interface or baseline changes. | Epic validation criterion; MR-3/MR-4/MR-6. | Record actual commands, revisions, failures/skips, affected channel census and fresh independent audit. Attribute existing whole-tree failures separately. |

## Scope boundaries

In scope: `models/designs/hif_ife/{hif_driver,hif_plant}.sysml`, `models/designs/generic_ife/ife_plant.sysml`, and the directly coupled library analyses `models/library/analyses/{ife_lcoe,fusion_cycle,hif_economics}.sysml` where needed. Equivalent IFE family copies, generated IFE artifacts, affected citations, verification scripts and meaningful tests are supporting changes. This is one connected dependency repair; its possible six-file footprint does not create independent concerns requiring decomposition.

Out of scope: monetary normalization, CAS redesign, broad generic-type relocation, shared MFE changes, unrelated audit findings, and source/finance scope expansion. Owner-held gates include research approval, residual acceptance, project-requirement changes, merge/push, item close/archive and goal close. A genuine source or comparison-basis conflict returns to the parent before dependent work proceeds.

## Success criteria and verification contract

- SV-073: exact source transcription plus independently calculated new cost baselines and explicit comparison cases. Both gain/yield source numbers survive; any execution choice is documented in design. No tolerance band may bless the old corrupted literals.
- SV-074: baseline, beam 5→10 MJ, efficiency 0.28→0.35 and rate 4.6→5 Hz checks. Hold other independent inputs fixed per case. Beam doubling doubles bank energy and yield; Meier direct driver cost rises by (0.32 + 0.088×10)/(0.32 + 0.088×5) = 1.5789473684210527, and Hawker's driver capital equals that cost. Efficiency changes bank demand inversely while beam/yield stay fixed. Rate changes shot count and power proportionally and procurement through its documented rate factor. Verify in actual generated execution, not just a mirror.
- SV-075: at eta=0.1, gain=100, blanket multiplier=0.6 and thermal efficiency=0.3, the eta-gain heuristic passes but cycle gain is 1.8 and net power is −0.2 times bank input power. The generation check rejects this case. Test zero and positive neighboring net outputs separately; cost division failures at zero cannot count as the only evidence for the model's named net-generation rule.
- Numerical identity tolerance is 1e-9 relative, with an explicitly reported absolute tolerance for near-zero arithmetic. Predicate expectations and source literals are exact. Printed power identities may show rounding residuals; report those rather than fit them away.
- Applicable IFE execution/mutation and model-family tests pass, Levels 1–3 pass, and the independent item audit evaluates F01/F02/F03 separately. Failed or skipped checks remain visible. Historical broad-range test success cannot certify source fidelity.

SV-073, SV-074 and SV-075 were registered pending using native `pm add-validation`. No existing historical SV certification was rewritten.

## Source record and assumptions

[INHERITED: source image, visually checked by the spec author on 2026-09-10] `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png`, Osiris column: beam 5.0 MJ; gain 87; yield 432 MJ; pulse rate 4.6 Hz; driver efficiency 28%; fusion power 1987 MW; thermal power 2504 MW; thermal efficiency 45%; gross electricity 1127 MW; driver electricity 82 MW; auxiliary electricity 45 MW; net electricity 1000 MW; COE 5.6 in 1992 cents/kWh. These are [REFERENT] transcription targets, not simultaneous exact computational constraints. Source confidence: high for transcription.

1. [INFERRED] Printed gain is rounded independently from yield: 432/5 = 86.4. Design must select and explain the computational interpretation; both historical facts remain preserved. This is a known rounding discrepancy, not an unresolved source conflict.
2. [INHERITED: existing model and Hawker source] Blanket multiplier 1.15, 90% availability, and Hawker's equal driver/cooling allowance differ from the historical Osiris operating table. Do not force the computed Hawker case to 1000 MW. Confidence in this distinction: high; fidelity of those approximations to a real plant is outside this correction.
3. [INFERRED] Changing dependency inputs can retire generated entry points and invalidate old test expectations. Likelihood high; impact bounded to IFE artifacts. Design must document the interface changes and verify actual consumers.
4. [INHERITED: prior work] WI-008 and the approved first-pass research repeat corrupted extraction values; they are historical context, not numerical authority over the source image. Directly affected current citations must point to the verified image or a durable corrected source record. No silent rewrite of historical evidence is authorized.

## Traceability and related artifacts

- Source authority: image above; `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`, Eqs. 2.1–2.16; `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md`, Eqs. 1–5. Design must inspect equation images where transcription matters before changing arithmetic.
- Prior context: `work/completed/20260303_WI-008_hif-concept-instantiation/{spec,design,plan}.md`; `work/completed/20260705_WI-015_ife-end-to-end-demo/{spec,findings}.md`; `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`; `models/README.md`.
- Governing records: `work/orchestration/ife-operating-point-repair.md`; `work/orchestration/goals/fusion-audit-remediation/{goal,trail}.md`; `.project/reports/20260907-fusion-model-audit.md:50-88` (historical finding identifiers).
- Downstream: IFE family execution, standalone IFE/HIF verification scripts and relevant regression fixtures. Shared MFE artifacts remain owner-gated.
- Next artifacts: `design.md`, `plan.md`, implementation evidence and fresh independent `audit.md` in this directory.

## Entry validation and execution notes

[INHERITED: parent execution, 2026-09-10] `.codex-test/run python -m pytest tests/models -q` passed 63 tests and skipped 13 in 17.80 seconds. Evidence: `work/orchestration/goals/fusion-audit-remediation/evidence/entry-model-tests.txt`. This includes IFE family generation/live-snapshot/mutation coverage and is the pre-change reference, not independent source verification. Parent image review: `work/orchestration/goals/fusion-audit-remediation/evidence/round1_source_check.md`.

[INFERRED] MR-WI048-5 requires the zero-net generation rule to remain observable even when LCOE is singular. A zero-net case must not become an apparently valid priced generator. Design may choose explicit non-ranking handling of undefined LCOE; extending financial zero-discount behavior (F05) is outside this item. Relevant consumers include `tests/test_codegen_teax_acceptance.py` and `tests/test_occurrence_mutation_teax.py`, which contain old gain/channel/dependency expectations. The later goal study's package metadata is separate task scope; this item's execution tests and anchors do not imply a study infrastructure expansion.

## Parent stage acceptance — 2026-09-10

[AGENT] Accepted for design under the owner-approved alignment. The eight requirements cover the coupled F01–F03 repair and preserve the reserved finance/source gates. Fresh entry execution with the documented TEAx PYTHONPATH passed all 20 tests in `tests/test_codegen_teax_acceptance.py` and `tests/test_occurrence_mutation_teax.py`; evidence is `work/orchestration/goals/fusion-audit-remediation/evidence/entry-ife-tests.txt`. The first attempt failed at setup because TEAx was absent from PYTHONPATH; the configured rerun changed no model or dependency.
