---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-27
Updated: 2026-09-27
---

# WI-097: exchanger thermal requirements

## Purpose

The series/network comparison currently checks heat removal and selected equipment but does not enforce required primary return temperatures or a justified temperature-approach condition. Preferred operations must satisfy the thermal requirements claimed for this comparison. Owner authority: work/orchestration/goals/design-study-exchanger-architecture/evidence/owner-supplement-r2.md. Existing native evidence: exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/record.md@afd96d51.

## Requirements

| ID | Requirement and provenance | Acceptance evidence |
|---|---|---|
| R1 | [NEED] Establish where the cited 30 K condition applies and specify primary return conditions before dependent scientific implementation. Distinguish source facts, comparison choices and unknowns. | Original-page citations and independent source/math review of a concrete contract. |
| R2 | [NEED] Implement justified thermal requirements and re-evaluate leading cases, preserving failures. | Native executable checks with independently verified temperatures, residuals and verdicts. |
| R3 | [NEED] Keep offered equipment fixed unless an alternative is explicitly enumerated and priced. | Input/output and purchase invariants; insufficient-equipment cases remain failed. |
| R4 | [NEED] Support a fair refined comparison of common cycle flow and network split among thermally passing operations. | Native interface preserves operating choices; study owns the declared refinement and resulting comparisons. |
| R5 | [NEED] Keep unknown differential hydraulics and topology costs as conditional break-even allowances. | No invented hydraulic/cost law or unsupported hardware purchase; report assumptions where they affect ranking. |
| R6 | [INHERITED] Preserve original models, packages, studies and owner edits. Use isolated additive sources and package if model changes are needed. | Legacy control replay and explicit owned-path changes; source lineage and regenerated integration evidence. |
| R7 | [INHERITED: MR-7] Document affected quantity roles and bindings; do not hide equipment selection, control or effective-UA changes in checks or reporting. | Independent design review before implementation, applicable sufficient/insufficient supplied-design tests and fixed-cost evidence. |

## Scope and stage status

[AGENT] This item owns model meaning and executable checks; the goal's native study owns exploration and reporting. Formal item closure remains with the owner. Source and interface evidence are r2-thermal-requirements.md, r2-implementation-options.md and the independent r2-source-review.md in the goal's evidence directory.

### 2026-09-27 investigation update

[AGENT] Original-page reading and implementation inspection are complete. The conditional N-R proposal uses exact aggregate cold-return targets He 659.15 K, PbLi 724.15 K and divertor 846.15 K, retaining full delivered duties with pump heat counted once, existing primary flows and hot caps. The replayable necessary-condition assessment at work/orchestration/goals/design-study-exchanger-architecture/evidence/r2-return-screen.py reads all 432 sealed main-grid cases: 324 fail a required-hot cap; the remaining 108 have not been established thermally passing. The unchanged divertor duty/flow/cap relationship limits supplied fusion to 2005.036667 MW under this boundary convention, excluding the former 2200/2300 MW leaders independently of arrangement. This assessment is not native model implementation and changes no historical result.

[AGENT] The source does not uniquely supply per-exchanger terminal minima. The owner subsequently delegated this choice and further study judgments in the goal's evidence/owner-supplement-r3.md. Adopt 30 K at both actual terminals of each of the three primary exchangers for the main conditional comparison. This excludes the recuperator and other plant exchangers; it is an agent-originated engineering requirement, not a source fact. The source-informed N-R returns above are also explicit conditional requirements. Preserve that authority in model doc comments and reports.

### Executable acceptance contract

- [INFERRED, delegated authority] Main thermal acceptance requires complete delivered duty removal, actual maintained primary returns659.15/724.15/846.15K within declared numerical closure tolerance, actual hot temperatures within independently supplied caps, defined exchanger states, and at least30K at all six actual primary-exchanger terminals. Mixed temperatures must not substitute for active exchanger terminals. Sensitivity requirements remain labelled alternatives.
- [INFERRED] Keep a legacy mode that reproduces the old physical/economic outputs and original14predicates, while new diagnostics disclose unmet requirements. A separate explicit control mode may change the thermal operating state through reviewed existing relationships; its flow, mixing and residual outputs must make that change inspectable.
- [INFERRED] Initially keep the original50,000m² exchangers and original ratings. Any alternative exchanger areas are supplied offers with existing native purchase/replacement/annual cost consequences; required area is never bound into inventory. Unpriced control/hydraulic/topology scope is disclosed through conditional allowances and may not be described as cost-free equipment.
- [INFERRED] Independent verification must cover every new hot/return, secondary-temperature, actual terminal, control and predicate channel. Exercise insufficient and sufficient supplied designs, return mismatch and approach failures; distinguish constructed equation fixtures from passing plant candidates. Exact-return tolerance verifies numerical closure and is not a physical acceptance band.

## Plan

- [x] Resolve the thermal contract against original sources and record independent review. Source interpretation accepted in r2-source-review.md; the remaining requirement choice resolved by delegated owner authority and recorded in owner-supplement-r3.md.
- [x] Record the smallest implementation design, quantity roles, affected bindings and acceptance checks. design.md and evidence/design-review.md final PASS; numerical rounded-gap finding resolved before implementation. Original and two explicit priced alternative inventories declared; native controlled/legacy modes and independent verification planned.
- [x] Implement in isolated owned paths; preserve and replay legacy behavior. Native package committed at a97d6db7; stock repeated generation fixed point and seven legacy replays preserve 551 outputs and fourteen verdicts exactly. Implementation report and independent review record the evidence.
- [ ] Independently verify added thermal channels and failure cases; run applicable integration checks.
- [ ] Supply an audited executable interface for the refined study, or document the precise blocked requirement.
