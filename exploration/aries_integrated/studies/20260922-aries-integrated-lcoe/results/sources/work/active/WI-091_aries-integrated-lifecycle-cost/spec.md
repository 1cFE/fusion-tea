---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-22
Updated: 2026-09-22
---

# Conditional integrated lifecycle cost

## Problem and intended use

The accepted integrated plant has selected equipment, net electricity and disjoint costs, but no complete lifecycle numerator. This item connects those native channels to a declared financial convention for conditional USD2004/MWh comparisons. Its consumer is the `aries-integrated-lcoe` goal and successor design studies. Scientific qualification remains separate from financial definedness.

## Requirements

| ID | Requirement and provenance | Observable acceptance |
|---|---|---|
| R1 | [NEED] Complete conditional LCOE from the same selected integrated configuration. Source: goal evidence/owner-brief.md, Prerequisite and goal. | Native outputs expose capital, construction financing, annual operating, fuel, replacement, terminal and energy contributions, whose sum reconciles to finite LCOE for positive net energy. |
| R2 | [NEED] Report no-breeding-credit and explicitly defined tritium-supply cases without double-counting recycling. Source: evidence/owner-supplement.md. | Zero added supply reproduces predecessor annual external demand; an independently supplied new T feed reduces purchases once. Exhaust recycling is retained inside loss. Supply support and incremental service cost remain explicit. |
| R3 | [NEED] Finance overnight capital once, use replacement events or reserve, and complete terminal costs. Source: same supplement. | Headline uses overnight plus one construction treatment; dated replacements exclude initial and end-of-life purchases; decommissioning/disposal and salvage occur at declared terminal timing. Reserve and already-financed source capital never enter that numerator. |
| R4 | [INHERITED] MR-1–7, particularly preservation of selected hardware and calculation ownership. Source: modeling_project/REQUIREMENTS.md. | Fixed-hardware demand changes propagate through native electricity and fuel to LCOE without resizing; sufficient/insufficient selected hardware and source failures remain visible. |
| R5 | [NEED] Declare finance, lifetime, availability, price-year and full expense assumptions and supported domains. Source: owner-brief.md, Work to accomplish. | Assumption register gives units, ranges, qualifications and replacement conditions; nonpositive energy and unsupported finance produce undefined LCOE, while engineering failure can coexist with defined conditional finance. |
| R6 | [NEED] Preserve Stellaris, frozen predecessors and 423.10679410931664 MW assumed integrated baseline. Source: goal.md and owner brief. | Coordinator preservation manifests and isolated replay pass; native baseline power agrees within 1e-9 MW; known source failures persist. |
| R7 | [NEED] Advertised outputs belong to the generated native graph. Source: owner-brief.md rule 7. | Sealed generated package exposes all reported model costs and LCOE; independent arithmetic serves verification only. |
| R8 | [INFERRED] Verify analytic limits and price/cost perturbations before downstream studies. Basis: consequences of R1–R7. | Zero rate, no replacements, terminal-only, supplied-feed, invalid-domain and fixed-physical-design sensitivities have independent expected results. |

## Scope and limits

Keep `models/designs/aries_cs_integrated/plant.sysml` and package `exploration/aries_integrated/aries_integrated`. Reuse generic finance where meanings fit and add isolated definitions where needed. Preserve historical source comparisons; reconcile published 77.6 USD2004/MWh and 1 GW using a separately labeled supplied financial boundary. This item does not reconstruct an unknown source discount convention or establish breeding, conductor, materials, reliability or supply-chain qualification. No recovery optimization is authorized.

The owner authorizes transparent scenario assumptions. Their selected values in design.md remain [AGENT], not source facts or settled owner decisions. Independent equation/binding review precedes implementation. Coordinator owns PM registration, source-set integration, goal records, commits, promotion and studies.

[INFERRED] The source-conditioned comparison holds recurring expenses, blanket replacement amounts/dates and terminal/overhaul/salvage fractions fixed. Substituting source inclusive capital changes the absolute fraction-based allowances. Report these changed amounts explicitly alongside the supplied capital and net-power boundary; the comparison does not reconstruct source expenses.

## References

`work/orchestration/goals/aries-integrated-lcoe/{goal.md,evidence/owner-brief.md,evidence/owner-supplement.md}`; predecessor `work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/{design.md,evidence/financial-handoff.md}`; source review under this goal's evidence directory.
