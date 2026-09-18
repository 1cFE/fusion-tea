---
Status: active
Scale: standard
Epic: standalone
Owner: reid
Created: 2026-09-18
Updated: 2026-09-18
---

# Installed cooling equipment costs

## Problem and intended use

[NEED] Determine whether the helium cooling system's pumps/circulators, piping and heat exchangers can be separately sized and priced from calculated plant heat-removal requirements, including installation and appropriate lifecycle costs. The owner requests existing R7.S3 before the ARIES comparison. Complete costing may increase levelized cost of electricity (LCOE); lowering LCOE or recovering feasibility is not acceptance.

[INHERITED] Exact target authority is `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`, row 7 S3: “Pumps, piping, heat exchangers as separately sized subaccounts.” Its general S3 test requires independently sized children rolling up through appropriate quantity, fabrication, installation, spares, replacement and maintenance logic. Source: owner prompt for goal `installed-cooling-equipment-costs`, 2026-09-18.

## Required reading

- `knowledge/holdout/aries-cs/PROTOCOL.md` — clean-room rules; barred sources and derivatives are excluded.
- `work/orchestration/goals/installed-cooling-equipment-costs/goal.md` — authorization, invariants and reserved gates.
- `work/orchestration/goals/installed-cooling-equipment-costs/evidence/account-boundary-map.md` — actual current interfaces and overlap risks.
- `work/orchestration/goals/installed-cooling-equipment-costs/evidence/starting-cases.json` and `entering-replay.json` — historical/current scenario distinction.
- `modeling_project/MODELING_PROCESS.md`, `MODELING_GUIDE.md`, `REQUIREMENTS.md`; `.agentic-mbse/codex.md` and `.project/codex-test-setup.md`.

## Requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| CE-01 | [NEED] Identify equipment and accounting boundaries for primary/intermediate circulators, piping, exchangers, coolant inventory and auxiliaries; distinguish turbine, rejection, cryogenics and buildings. Each cost belongs once. | Account map naming replaced aggregate scope, retained scope, newly added scope and omissions. |
| CE-02 | [NEED] Derive circulator quantity, flow, head, power and conditions from calculated heat/hydraulics and circuit count; do not treat duty/count alone as purchasable equipment. | Unit-checked calculation, topology/drive assumptions and source operating-domain comparison. |
| CE-03 | [NEED] Size exchangers from duty and explicit thermal, pressure and material assumptions. | Area or other source-supported sizing, temperature approaches, pressure/material basis and exposed missing inputs. |
| CE-04 | [NEED] Price piping from explicit diameter, wall or pressure class, material, length and fittings/supports. | Calculated quantities distinguished from layout allowances; hydraulic consistency and layout-cost sensitivity. |
| CE-05 | [NEED] Separate source-supported circulator, piping and exchanger costs respond to engineered quantities. | Original values, technology/scale, source currency/year, uncertainty, conversion/escalation rationale and purchased/fabricated/installed boundaries retained. No invented installation factors or water-to-helium price transfer. |
| CE-06 | [NEED] Include appropriate procurement, fabrication, installation, spares, replacement and maintenance without duplicate scope. | Equipment service-life/exclusion rationale, cash-flow treatment, reconciliation with existing O&M, indirects, supplementary charges and availability. |
| CE-07 | [NEED] Integrate accounts into executable CAS and LCOE, preserving pump-electricity/net-power coupling. | Model declarations and generated execution agree; rollup and demand/circuit responses verified. Renamed aggregate or duplicated child lump fails acceptance. |
| CE-08 | [NEED] Verify units, operating ranges, quantities, price boundaries, rollups and lifecycle; compare independent engineering examples where available. | Independent source/applicability review distinct from software parity; targeted regression and consumer results with entering failures separated. |
| CE-09 | [NEED] Run focused native study with saved reference and latest selected design where applicable; retain failures. | Equipment/cost accounts, purchased/installed scope, demand/circuit responses, pumping/net/LCOE, predicate results and cost/layout sensitivities. Matched comparisons separate added costs from design changes; no unsupported optimum. |
| CE-10 | [NEED] Obtain fresh review before substantial implementation and fresh exact R7.S grade after execution. | Source/sizing, price scope, replacements, omissions/duplicates and verification/study-plan review; final assessor inspects model and executable evidence. |
| CE-11 | [HARD] Preserve helium scenario, targets/limits, ARIES quarantine, r2 archive and historical results; no merge/push. | New artifacts separately identified and preservation checked. Major scope/scientific decisions, technology changes, reveal, frozen-comparison replacement and formal goal closure remain owner-held. |

## Affected definitions and consumers

[INFERRED] Expected producer is heat transport in `models/library/structure/mfe_plant_systems.sysml`, with reusable equipment calculations in `models/library/analyses/` and explicit stellarator instance assumptions in `models/designs/stellarator_09/stellarator_plant.sysml`. CAS22 and lifecycle consumers reside in `models/designs/generic_mfe/mfe_plant.sysml`; identify all inheriting instances before changes. Preserve or deliberately regenerate the plant-facing coolant-cost interface, generated package, oracle, census, manifests and downstream consumer contracts. This is a proposed implementation boundary, not a settled design.

[INHERITED] Existing C220200 combines net-power-scaled primary and thermal-power-scaled intermediate estimates. Reactor installation excludes this account. CAS50 spares exclude CAS22; current CAS72 replaces in-vessel equipment only. Generic O&M and building/auxiliary accounts require boundary reconciliation before additive cooling charges.

## Current evidence and unresolved design

[INHERITED] `evidence/sizing-source-review.md` under the goal independently confirms source exchanger area and distinguishes effective UF from independently determined U. Source topology and complete pipe construction/layout are unresolved. Equal parallel circulators may be an explicit conceptual assumption, subject to source-price applicability. No combined preimplementation approval has been issued.

[INHERITED] Four diagnostic current replays preserve all 23 retained cooling/economic channels per case. The historical selected 18/14-circuit cases now fail computed breeding; both historical r2 controls also retain prior failures. Do not call those current full-plant passes. The entering cooling test batch has 131 passes and six existing consumer-contract failures; it is not a clean full suite.

[INHERITED] Round2/3 source research and independent corrective review now support the conceptual equipment methods in `combined-design.md`. The owner approved HITEC270–465°C intermediate cooling with primary helium retained. Implementation is released under explicit source-transfer, auxiliary and conversion-interface limitations; executable S3 acceptance remains pending.

## Verification and study responsibilities

[INFERRED] Use independent hand checks for dimensions, per-circuit/per-machine splitting, heat/work balance, exchanger thermal approaches and pipe mass. Check original source tables/images and applicable operating/material/size ranges separately. Test account replacement identities and the flow from direct cost through indirects, supplementary costs and annual expenses into LCOE. Review explicit lifecycle schedules and availability assumptions. Compare unchanged-input old/new accounts before circuit or demand variations; expose a cost-basis mode only if its ownership and preservation are reviewed.

[NEED] Use `.codex-test/run` and native modeling/integration/study procedures. Report static findings, partial checks, oracle exclusions and pre-existing failures precisely. Substantial implementation starts only after fresh review of a concrete source-supported design and study plan. If the evidence cannot support S3, retain this item open with specific missing inputs and investigated methods; a blocked record does not close the gap.
