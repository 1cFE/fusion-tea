---
Status: active
Scale: standard
Owner: reid
Created: 2026-09-22
Updated: 2026-09-22
---

# WI-090: Integrated ARIES equipment and costs

## Outcome and authority

[INHERITED: work/orchestration/goals/aries-integrated-equipment-costs/evidence/owner-brief.md] Extend the delivered integrated ARIES assembly with selected inventory, cost ownership, engineering margins and annual/scheduled expenditures. Deliver native generated outputs suitable for the successor financial goal. This is a conditional post-reveal engineering estimate. The original Stellaris, prior transfer cases and frozen evidence remain preserved. Formal closure remains owner-held.

## Requirements

- **R1 [INHERITED]:** Continue `models/designs/aries_cs_integrated/plant.sysml` and `exploration/aries_integrated/`. All advertised amounts, inventories, checks and balances must be produced by the generated graph. Reuse applicable definitions unchanged; additions are generic and concept values remain in the assembly.
- **R2 [INHERITED]:** Selected magnet/conductor, blanket/shield, divertor, primary cooling, conversion, electrical, fuel, facilities and auxiliary scope must have owners. Demand must not select purchase quantity, geometry, capacity or price. Each varied equipment capability must connect to selected inventory, upfront cost and its applicable operating demand.
- **R3 [INHERITED]:** Use one disjoint CAS account map with explicit currency/year, installation boundary, and direct/indirect/contingency classification. Every material account must have an amount or estimate range. Separate initial equipment, fuel/coolant inventory, annual throughput and scheduled replacement. Preserve source miscellaneous/special-material meanings.
- **R4 [INHERITED]:** Compare the provisional account assembly with a separately labeled source-budget alternative. Supplied fixed budgets remain visible during physical sweeps. Do not label a source financed total as overnight or silently mix dollar years.
- **R5 [INHERITED]:** Supply unlevelized annual O&M, fuel/consumable costs, replacement event costs, schedule basis and availability assumptions for the successor. Do not subtract recirculating electricity twice or hide scheduled costs in annual O&M.
- **R6 [NEED]:** “Before ranking equipment or economic alternatives, test sensitivity to the principal thermal assumptions and connect each varied equipment capability to its selected inventory, purchase cost and applicable operating demand. Preserve the source-case failures and label the 423.1 MW case as the assumed integrated baseline.” Source: goal.md owner quote.
- **R7 [INHERITED]:** Unsupported field/conductor, breeding, hydraulic/material and machine-map qualifications remain unverified independently of numerical adequacy. No inapplicable REBCO law may establish Nb3Sn support. Preserve source-conditioned failures and full canonical input maps.
- **R8 [INFERRED]:** Validate fixed-hardware demand response, insufficient/sufficient selected equipment, thermal-assumption response, disjoint cost rollups and schedule semantics. Independent review must inspect the proposed relations before implementation and consequential generated behavior afterward. Trace every quantitative assumption under MR-4.

## Acceptance

The delivered package executes the four inherited scenarios, with the assumed integrated baseline reproducing 423.106794 MW before any intentional changed assumption. Required tests demonstrate that density changes demand and annual consumption but leave selected inventories/upfront costs unchanged; an exchanger-area alternative changes both finite thermal capability and purchase cost; a rating alternative changes its inventory, capital and adequacy without secretly changing demand. Thermal sensitivities precede any equipment/economic ranking. Every account reconciles to its children with separately exposed source discrepancies. Initial and replacement amounts occupy distinct channels. Price sensitivity changes costs without changing physics. Scientific unsupported states remain unsupported.

Numerical balance tolerances retain WI-089's `max(1e-6 MW, 1e-9 * total input MW)`. Account arithmetic tolerance is `max(0.01 USD2004, 1e-10 * account amount)`; source discrepancies are outputs, not tolerance inflation. Monetary ranges are scenario bounds, not statistical confidence intervals.

## Scope and gates

New source interpretation, inventory ownership, equation and public-input changes require independent review. `design.md` is the single new assumption register; `plan.md` tracks remaining work. Detailed structural stress, coil field/current/conductor qualification, neutronics, machine maps, vendor quotations, financing/LCOE and optimization remain successor work. A provisional cost is permitted; an unknown silently represented as zero is not.

## Verification registry

[AGENT] Native verification `SV-134` is passing in `modeling_project/VALIDATION_MATRIX.md`, based on the66-case native receipt and accepted independent implementation review. Complete-validator L2/L6 exceptions remain explicitly scoped, not a full pass. Existing unrelated matrix type warnings were reported by registration and do not establish this item’s validation.

[AGENT clarification, 2026-09-22] Source residuals are not all rounding. The accepted source review retains unresolved parent/child discrepancies and distinct mass/account boundaries; wording above now names those discrepancies without assigning a cause. No source amount or model equation changes.
