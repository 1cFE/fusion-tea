---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-064: Current-driven magnet inventory sizing

## Contract

[NEED] Implement only missing behavior needed for a consistent joint current/inventory/geometry calculation, preserving entering behavior and every acceptance limit. Source: work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md, initiating owner request.

[INFERRED] Add optional native current-driven inventory sizing. Independent radial allocation determines actual peak field first. The existing performance law then determines required tape count and pack area at held construction, turn current and allowable fraction. The selected physical inventory drives all existing downstream consumers. No iteration is necessary for independently chosen allocation; computed required cavity is compared with it, never fed back as available space.

[INHERITED] Required reading: knowledge/holdout/aries-cs/PROTOCOL.md; modeling_project/REQUIREMENTS.md; MODELING_PROCESS.md; existing WI-062 source/design and WI-061 geometry reviews. Do not read quarantined content. Retain construction transfer, uniform field/orientation and price/manufacturing limitations.

## Design for independent review

[AGENT] Use one new reusable typed manual calculation, `Current Driven Pack Sizing`, in mfe_conductor_current.sysml. Inputs: mode exactly 0/1, inventory_multiplier >=1, incoming legacy effective density, coil ampere-turns, turn current, four non-tape fractions, tape width/thickness, actual peak field, temperature, reference tape current, material/orientation factors, three retention factors, allowable_fraction and extrapolation switch. Reuse precisely the current performance equation/domain from WI-062; no new empirical facts.

[AGENT] With tape area At=w*t in m², residual tape fraction ft=1-sum(non-tape fractions), available tape current Ia=Ic_tape*cabling*degradation*sharing, calculate N_required=I_turn/(u_allow*Ia), A_conductor_required=N_required*At/ft, A_pack_required=(NI/I_turn)*A_conductor_required, j_required=NI/(A_pack_required*1e6). Select j_effective=legacy_j_effective in mode0, otherwise j_required/inventory_multiplier. Output these five required quantities plus selected_j_effective (six outputs: required_tapes, required_conductor_area, required_pack_area, required_effective_density, selected_effective_density, tape_available_current). Pack sizing uses selected density. Physical extra inventory is explicit; it does not relax allowable fraction. Counts remain continuous homogenized reference-conductor counts, not integer manufacturing stacks.

[AGENT] Keep conductor_grade unchanged. Winding Pack's effective density EXPOSE binds the selector output instead of conductor_grade output. Selector receives the grade output directly. Thus mode1 selected envelope no longer multiplies actual-field inventory a second time; its unchanged predicate remains independent. Legacy grade quantity/effective diagnostics remain visible and are labeled legacy. No input j_wp is redefined as a material gain. Public owner inputs are Winding Pack sizing_mode(default0) and inventory_multiplier(default1). Both are explicitly bound in Stellaris. Magnet-owned calc uses existing producer interfaces and exposes all six outputs. Existing reference current predicate independently reconstructs count from final procurement inventory. Exact closure can incur signed floating roundoff; preserve its exact >=0 rule and report that result. Studies use an explicit 1% additional-inventory scenario (multiplier1.01), with boundary diagnostics separately.

[AGENT] Preserve all twenty predicates and all previous manual bodies. Mode0 must preserve every entering scalar/predicate at reference and representative off-design points. Mode1 uses the same valid 20K, 4–6mm, 56µm, 20–32T domain and >24T extrapolation permission. Validate all inputs, finite/positive intermediates, residual tape fraction in(0,1], nonnegative component fractions and invalid switches. No loss/yield/qualification is implied by the multiplier.

## Affected ownership and supported comparisons

[AGENT] Canonical and MFE exploration twins: analyses/mfe_conductor_current.sysml, structure/mfe_magnet_parts.sysml, cost_structure/mfe_power_core.sysml and stellarator design. Generated package and strict manual seed inventory; independent oracle and entry/output mapping; manifest, census, snapshot and affected tests. Shared Magnet System consumers are enumerated before editing. Fixed turn current at50kA avoids claiming free winding/lead/joint tradeoffs. Fixed composition and square aspect are the principal study; declared cavity allocations are assumptions, with no 3D space or wall-strength certification. Existing stress and thermal area approximations remain explicit.

## Acceptance and checks

- [x] Independent source/math/interface release before implementation. See goal evidence/source-design-review.md.
- [x] Native and generated optional sizing implements equations with guarded domains; existing manual bodies and twenty predicates preserved.
- [x] Independent oracle rederives required area from ampere-turn/tape capability, with all new outputs mapped; component tests cover analytic values, boundaries and refusals.
- [x] Mode0 entering preservation; mode1 reference/off-design inventory-current-geometry-procurement agreement, including grade cancellation and declared extra inventory.
- [x] Shared consumer checks, native validation and reproducible generation; disclose static-validator residue. Integration CANDIDATE is the next native seam task.
- [x] Independent coupled implementation audit and study-ready handoff.

[AGENT] Use rtol1e-9/atol1e-9 for mapped scalar agreement (units carried); report current closure relative residual explicitly. No acceptance predicate tolerance changes. Source/math review and integration audit may use one continuing fresh non-author reviewer. Native spec combines design and checklist under MODELING_PROCESS scale guidance.
