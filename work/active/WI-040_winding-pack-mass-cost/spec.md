---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-13
Updated: 2026-09-13
---

# WI-040 — Winding-pack mass cost account

## Problem and intended use

[NEED] Price winding-pack materials by mass before implementing WI-038's conductor-grade consequences. Owner request: “WI-040 first, then WI-038”; grounding approval: “approved, please begin”. Governing goal: `work/orchestration/goals/magnet-design-transfer/goal.md@ff3030b5`.

[INHERITED] The existing pack-sizing chain responds to coil current and winding-pack current density, but the winding account prices ampere-metres times a fabrication multiplier. Changing pack cross-section at fixed current and length therefore leaves that account unchanged. See `models/library/analyses/mfe_magnet_cost.sysml`, 'Winding Pack Cost', and WI-036 design D1–D3, D6 and D8.

[INFERRED] The intended use is a bounded comparison of material quantities and costs as the modeled pack changes. The result must distinguish procurement from fabrication and reconcile with the existing conductor, casing and primary-structure accounts.

## Required reading

- `knowledge/holdout/aries-cs/PROTOCOL.md` — model-facing clean-room rules.
- `modeling_project/REQUIREMENTS.md` and `modeling_project/ARCHITECTURE.md` — especially MR-1 through MR-4 and AD-007/008.
- `work/orchestration/goals/magnet-design-transfer/goal.md` and `trail.md`.
- `work/completed/20260901_WI-035_magnet-closure/design.md` and `work/completed/20260903_WI-036_winding-pack-sizing/design.md`.
- `basis.md` — source-table conflict and accounting basis; unresolved decisions remain explicit.

## Requirements

| ID | Requirement | Authority | Verification |
|---|---|---|---|
| MR-WI040-1 | The model SHALL calculate the approved pack materials' quantities from the actual modeled pack geometry and declared composition, exposing material masses and their cost contributions. | [NEED] WI-040 mass-cost objective; [INFERRED] observable breakdown | Source-verified material table; independent volume/mass arithmetic; evaluated public outputs. |
| MR-WI040-2 | The model SHALL distinguish conductor procurement, non-tape material procurement, fabrication, casing and primary structure, identifying any retained overlap or omission before claiming a reconciled magnet cost. | [INFERRED] Approved goal's accounting invariant | Accounting-boundary review against sources and exact rollup identities. |
| MR-WI040-3 | Each density, material fraction, price and markup SHALL have a declared unit and source or explicit assumption. Helium inventory SHALL state the thermodynamic condition used to convert volume to mass. | [INHERITED] Project MR-4; [INFERRED] material-inventory applicability | Source-image or admitted-code inspection and parameter-basis record. |
| MR-WI040-4 | At fixed composition, density and unit prices, changing geometric pack volume SHALL produce proportional material mass and procurement cost; a material's price SHALL affect only its own procurement contribution and downstream totals. | [INFERRED] Mass-based accounting consequence | Controlled local experiments at declared valid inputs, independently calculated expectations. |
| MR-WI040-5 | The account SHALL use the computed winding-pack volume, distinguishing it from additional cold volume attributed to other cryogenic equipment. | [INFERRED] Physical accounting boundary | Binding inspection and independent changes of pack size versus extra cold volume. |
| MR-WI040-6 | The implementation SHALL preserve existing valid physics outputs and operating-limit semantics when only accounting is changed, while reporting the expected changes to magnet capital and downstream economics. | [INFERRED] Goal comparison invariant | Baseline and selected off-reference regressions; before/after cost reconciliation. |
| MR-WI040-7 | Reusable material-account logic SHALL remain in the library, with concept composition and parameter values bound by the instance. Quantities SHALL retain identifiable physical owners and public interfaces consistent with AD-008. | [INHERITED] MR-3 and AD-008 | Model structure, bindings and generated consumer audit. |
| MR-WI040-8 | Invalid material-account inputs SHALL produce deliberate diagnostics instead of silent negative mass/cost, non-finite outputs, or unphysical composition. The supported input domain and boundary behavior SHALL be specified before implementation. | [INFERRED] Broader input applicability | Domain-focused checks of the chosen native executable route. |
| MR-WI040-9 | The changed native package and affected consumers SHALL be coherent, with historical study records preserved and validation evidence distinguished from engineering applicability. | [INHERITED] Goal invariants and native workflow | Relevant model/consumer checks, integration evidence, independent audit. |

## Scope and supported use

[INFERRED, adopted under owner delegation 2026-09-13] Price Table 7's copper, solder, steel and helium; treat unquantified inter-pancake insulation as a disclosed limitation. Source-image verification corrects the inherited backlog list. The owner delegates this technical judgment in the goal's 2026-09-13 amendment.

[INFERRED] Preserve WI-057's existing physical decomposition. The work concerns pack quantities and accounting, not coil configuration, pack/casing fit, a new critical-current surface, or reactor optimization. WI-038 remains subsequent work. A conductor-volume model must not be inferred from ampere-metres without its own basis.

## Research decisions

1. [INFERRED] REQ-040-02 supports the additive procurement and length-based winding estimate selected in design.md. This replaces the unsplit multiplier without claiming to recover its unknown decomposition.
2. [INFERRED] REQ-040-01 supplies material densities, price references and helium state checks. The chosen solder proxy, price-year escalation and transfer limits are documented in design.md and the two research reports.

## Success and stage state

Implementation and current consumer adaptations are committed at 173ac157 with audit repairs at 9e942fac. The full model battery passes 809 tests with 13 inherited skips; stable consumer and integration batches pass 219 and 25 tests. Independent audit returns PASS and SV-100 is passing. See audit.md, plan.md and evidence/ for completion evidence. The existing WI-040 registration is reused; no duplicate item is minted.

Completion requires the requirements above to be evidenced and a positive independent audit. Closing or archiving is owner-held.
