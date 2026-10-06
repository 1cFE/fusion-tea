---
Status: completed
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-27
Updated: '2026-10-06'
---

# WI-098: Whole-plant conversion comparison

## Problem and intended use

[NEED] Determine how steam versus helium Brayton conversion changes complete-plant exported electricity and lifecycle cost for the same reactor. The verified WI-096 conversion-only comparison omits reactor/fuel and primary circulation loads/costs. Owner authority: work/orchestration/goals/design-study-whole-plant-conversion/evidence/owner-brief.md@2c8db9db. Goal: that directory's goal.md. The result supports the component-choice example in the owner's write-up; do not edit the article.

## Requirements

| ID | Requirement and origin | Acceptance evidence |
|---|---|---|
| R1 | [NEED] Use one explicit compatible reactor inventory and common supplied source condition within each pair. | Configuration/account table traces geometry, blanket, primary, auxiliaries and operating/service assumptions. Source heat, fusion power, deposited heating and recovered primary work are distinct. Across-load changes preserve selected installed inventory or declare different designs. |
| R2 | [NEED] Compute complete net export inside the model. | Conversion net minus primary pumping, heating wall-plug, cryogenic, fuel-processing, vacuum/control and remaining declared auxiliaries, with no double subtraction of cycle shaft work. Independent power ledger and imported/nonpositive-power checks. |
| R3 | [NEED] Compute whole-plant LCOE inside the model with a disjoint complete cost inventory. | Major CAS accounts, annual expenses, fuel, replacements and terminal items are traced and reconciled. Removed old conversion allowances are explicit. All prices share a declared currency year and common finance/service convention. Costs follow chosen inventories. |
| R4 | [NEED] Use explicit assumptions and sensitivities for remaining uncertainty. | Material unknowns have a justified scenario range or break-even calculation; no arbitrary tritium threshold or unexplained fuel-price headline. Conditional supplied-source assumptions do not claim independently reconstructed plasma operation. |
| R5 | [NEED] Reuse verified conversion physics and enforce interfaces. | Prior controls replay with unchanged conversion outputs when the boundary alone changes. Source/exchanger return, approach, finite cooling, property and capacity constraints remain executed. Failed/unsupported cases retain their states and cannot rank. |
| R6 | [INHERITED: MR-7] Keep supplied design, demand, capacity, solved states and selection policy distinct. | Design role/binding table; independent pre-implementation review; insufficient/sufficient supplied choices and demand-only changes demonstrate unchanged hardware and coherent costs. Controllers solve actions, not purchases. |
| R7 | [NEED] Enable whole-plant reranking over finite explicit offers and supported operating choices. | Complete inputs/outputs/check status and native study route support all relevant offers. Report different branch operating freedoms. Sensitivity axes include prices, efficiencies, common reactor accounts/loads, fuel and availability as justified. |
| R8 | [NEED] Preserve existing baselines, source evidence, studies and other work. | Additive models/package; protected-file preservation checks; explicit-path commits; no report edit, push or merge. |
| R9 | [INHERITED: MR-1–6, MODELING_PROCESS.md] Use native model conventions, generated execution and proportional independent verification. | Native registration, reviewed design, generated-package fixed point, source/body census, validation dispositions, independent output/predicate checks and substantive integration review. |

## Scope and review

[INFERRED] Start with the existing Stellaris helium-primary scenario and repaired component-alternatives assembly. T-001 determines which upstream definitions and fixed inventory can be transferred honestly. Record remaining source or installed-capacity uncertainty before implementation. New equations, source interpretations and changed interface ownership require independent design review. A coupled whole-plant audit precedes the main study. Reuse the predecessor's valid evidence without treating it as verification of new upstream calculations.

[NEED] The goal owns study execution, final figures and economic conclusion. This item supplies the verified native system model and replayable study interface. Item completion alone cannot satisfy the goal's plant-level question. Formal closure remains with the owner.

## Entry evidence

- WI-096 spec/design/report, repaired numerical report, and sealed study 20260926-design-study-component-alternatives-b.
- T-001 upstream-accounting.md and conversion-interfaces.md in the goal's evidence directory, when returned.
- modeling_project/REQUIREMENTS.md; modeling_project/STUDY_POLICY.md; modeling_project/MODELING_PROCESS.md.
