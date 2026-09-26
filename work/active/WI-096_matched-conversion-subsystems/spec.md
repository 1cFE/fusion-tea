---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-26
Updated: 2026-09-26
---

# WI-096: Matched Conversion Subsystems

## Problem and intended use

[NEED] Compare the existing steam and helium Brayton components on the same supported heat-source boundary, with explained net electricity, equipment and conditional conversion-subsystem cost per net MWh. The owner permits an isolated subsystem experiment, small justified extensions and an honestly partial economic result. Authority: `work/orchestration/goals/design-study-component-alternatives/evidence/owner-brief.md`; governing goal and comparison contract in that directory.

[INHERITED] Existing steam/Brayton packages do not establish that comparison. Their source interfaces, circulation loads, cooler checks and cost boundaries differ. The Brayton historical starting point requires unpriced bypass hardware; the steam IHX checks area adequacy without predicting control at excess capacity. Evidence: the three interface/cost audits and `evidence/feasibility-review.md` in the goal. The later WI-079 inclusive steam package owns its represented SG/reheater children; the cost audit's earlier unresolved-scope reading is superseded by its follow-up.

## Requirements

| ID | Requirement and authority | Observable acceptance |
|---|---|---|
| R1 | [NEED] Each technology receives identical delivered heat, hot/required-return temperatures and source flow within a pair; preserve source heat and pumping accounting. | The two native branches read one source owner. Independent balances verify the supplied helium energy identity and each branch's actual return/heat transfer. No upstream pump or recovered heat is counted twice. |
| R2 | [NEED: owner-direction-fourth-submission.md] Preserve selected source heat, cycle flow, pressure ratio and installed equipment. Required physical equalities belong in model calculations; inconsistent choices fail. [INFERRED] Reuse the existing primary bypass controller with explicit assumed inventory, pressure service and cost. | Independently selected source offers 2500/2800/3000 MW drive the unchanged primary loop. Both branches consume its full actual tuple. Model-owned controls calculate bypass flow; inadequate exchanger or controller capability fails. Actual heat and demand remain distinct, including failed downstream execution. No source-heat or ratio matching search runs outside or inside the model. |
| R3 | [NEED] Reuse the steam state/profile solver and helium Brayton components where their domains support use; record every extension and failed case. | Steam temperature/pressure conditions and independent installed ratings remain enforced. Brayton source heat/return and machine limits are enforced. Execution refusal, engineering failure and unqualified assumptions remain separate. |
| R4 | [NEED] Include conversion electricity and heat rejection, including salt/steam/water pumps and generator/mechanical losses. [INFERRED] Add a finite-UA water-flow operating closure for Brayton conditioners. | Independently selected cooler UA, duty, pump flow and power are evaluated. Actual endpoint and property-knot temperature gaps and water-pump heat location are explicit. Whole-subsystem `Q_delivered − P_net − Q_rejected` closes. Unmodeled low-grade heat transfer is reported unverified, never admitted by a Boolean switch. |
| R5 | [INHERITED: MR-7] Choices, calculated operating demands, required conditions, installed capabilities and search policies remain distinct. | Insufficient/sufficient equipment tests change verdicts while preserving selected designs and purchase bases. Demand-only changes alter demand and margin without buying hardware. Pressure ratios remain chosen; controller bypass and coolant flow are calculated operating states. All new handwritten bodies and iterative closures are counted explicitly. |
| R6 | [NEED] Costs have disjoint installed-equipment scopes, common currency/finance conventions and explicit recurring costs. | Retain inclusive steam package; separate connector, salt and rejection accounts; keep Brayton services and transport ownership explicit. Actual cooling replacement terms are split algebraically. Unknown currency conversions or missing scope remain explicit factors/corrections. Qualified economic ranking is withheld while consequential corrections are unresolved. |
| R7 | [NEED] Preserve existing models/packages and historical studies. [INHERITED: MR-1–4, MR-6–7] Use native modeling conventions and reviewed definitions. | Additive models/package only; originals hash unchanged. Unchanged components replay their deposited controls, including near-zero rather than falsely exact-zero bypass. Native generated outputs agree with an independent oracle and every executed check is re-derived. |
| R8 | [INFERRED] Supply a reviewable package handoff supporting a bounded study. | Source/body inventory, offered catalog, full inputs, outputs, failed cases, identities, verifier, study interface/manifest and integration return are retained. A fresh design review precedes implementation; fresh implementation review precedes main study release. |

## Supported use and limits

[AGENT] The experiment compares the supplied steam offer against tested Brayton offers at independently selected operating powers of the existing source-loop model. Steam IHX circuits are selected from 10/11/12/14. Source and conversion hardware remain chosen; existing finite-UA bypass controllers calculate feasible flow division. Explicit hypothetical controller ratings, price, electrical load and a common imposed pressure-service scenario are reviewed assumptions. The pressure law includes reference IHX losses and does not predict new valve curves or branch hydraulics. Conditional agreement with this source model does not establish plasma/blanket turndown, procurement qualification or equally optimized technology performance.

[AGENT] The intended monetary output is a conditional subsystem estimate with explicit assumption levels and a cost-correction frontier. Complete economic recommendation remains unmet if currency, installed scope or recurring-cost support is inadequate. A native performance result can still be accepted within its declared assumptions without calling it engineering qualification.

## Governing evidence and handoff

- Owner and goal: `work/orchestration/goals/design-study-component-alternatives/{goal.md,comparison-contract.md,evidence/owner-brief.md}`.
- Scope and physical findings: `evidence/{model-design-brief,steam-interface-audit,brayton-interface-audit,cost-audit,feasibility-review}.md` under that goal.
- Pre-change numerical controls: goal `evidence/readiness-screen.json`; upstream source nominal is the unchanged Stellaris output, with `T_comp_in = 561.9353658449644 K`, `q_ihx = 3301.2132114869937 MW`.
- Prior source-coupling diagnostic `evidence/source-coupling-probe.json` remains historical evidence; its external matching policy is superseded. Fourth-submission source/controller and thermal diagnostics are retained separately, including failed offers and the explicit revised cooler specification. They are development evidence, not native integrated validation.
- Owner continuation: goal `evidence/owner-direction-fourth-submission.md` and `fourth-submission-brief.md`; exactly one additional design review is authorized.
- Applicable acceptance cases and proposed definitions are in [design.md](design.md). No implementation is authorized by the existence of these documents; the coordinator commissions the fresh review.
