# WI-064 implementation evidence

[AGENT] Native optional sizing is implemented in the four spec-owned canonical files and their exact MFE exploration twins. `current_sizing` owns the six named outputs and exposes each through Magnet System. Winding Pack owns `sizing_mode` and `inventory_multiplier`; Stellaris explicitly selects entering values 0 and 1. The grade calculation remains unchanged and supplies the legacy density input. The selected density feeds existing pack sizing, so physical inventory propagates through existing geometry, mass, cryogenic, procurement and cost consumers.

[INHERITED] Source/domain authority and conditional limits remain WI-062 and the independently released WI-064 design at `work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md`. No source research or empirical normalization was added. Continuous tape count is an inventory estimate, not a manufacturable integer stack. Existing geometric/stress/thermal approximations remain unqualified.

## Shared consumers

[AGENT] Search of production `models/**/*.sysml` finds one Magnet System ownership site: `models/designs/generic_mfe/mfe_plant.sysml:103`, in abstract MFE Power Plant. Its only concrete production instance is `models/designs/stellarator_09/stellarator_plant.sysml:32`, Stellaris. Winding Pack occurs inside Magnet System at `models/library/cost_structure/mfe_power_core.sysml:122`; the generic plant redefines its inherited temperature binding. The MFE exploration tree contains exact twins of these sites. No additional production concrete Magnet System consumer was found. Historical WI-051/WI-053 evidence/prototype copies are not production consumers.

## Checks completed by model implementer

- [x] Independent design release read before edits.
- [x] Four canonical/twin pairs remain byte-identical; regeneration inventory verifies every MFE-owned pair.
- [x] Guarded current-to-tape-to-area calculation and selector added with all physical/performance inputs bound.
- [x] Existing 25 manual completion bodies preserved byte-for-byte against WI-063 reviewed seed inventory.
- [x] Fresh generation reproduced exactly twice using `evidence/regenerate.py`; 26 explicit seed hashes, model hashes, package hashes and generation changes deposited alongside it.
- [x] Component wrapper and direct completion tests: 204 passed, recorded in `evidence/component-tests.txt`.
- [ ] Coordinator: native all-source validation, prior scalar/predicate preservation, coupled oracle agreement and integration candidate.
- [ ] Independent coupled implementation assessment and study handoff.

[AGENT] Component tests cover an analytic 10-tape reference conductor, 4.48e-6 m² conductor area, 4.48e-5 m² pack area, unchanged density under turn repartition, exact mode0 passthrough, grade-density independence in mode1, explicit extra inventory, all input nonfinite/negative refusals, unsupported domain/switch/fraction refusals, and arithmetic overflow/underflow. Both wrapper and direct completion execute the same cases. This establishes component behavior; coordinator-owned integration establishes assembled behavior and old scalar/predicate preservation.

[AGENT] Generation uses the established strict WI-040 seed protocol, with the WI-063 inventory as the preservation baseline. The new manual function declares exactly `tuple[float, float, float, float, float, float]`; the pinned generator requires exact output tuple arity and does not accept a variadic tuple annotation. Generated schemas, contracts and pipeline are native generator outputs. The generated `special_materials_capital` automatic body changes only generated positional ordering; it is not one of the preserved manual seeds.

[AGENT] Mode0 computes required sizing diagnostics before selecting its exact legacy density. Thus it retains the released caveat that extreme arithmetic may refuse additional points outside the tested entering/reference/off-design set. No clipping, tolerance, epsilon or predicate change was introduced. Exact current closure at multiplier1 may carry signed floating roundoff; report the existing predicate result and relative residual separately. The 1.01 scenario adds purchased physical inventory.

## Coordinator integration and validation

[AGENT] Nine full-route checks pass in evidence/integration-tests.log. They establish every entering native reference output/predicate unchanged, all218 current oracle-mapped outputs at six cases, selected-envelope cancellation in sizing mode1, physical extra-inventory scaling, and allocation→field→required tape→length/cost propagation. Independent current-oracle regression14passed. Metadata is derived by evidence/repin.py:312 public inputs, unchanged reference LCOE144.74743129583516, current manifest/census/structural snapshot. The original single-file validator invocation discovered zero files and is retained in native-validation.log as invalid coverage, not a pass. Correct complete-tree invocation in native-validation-complete.log checks all levels: L1/L3/L4/L5pass; L2ten inherited literal placeholders and L6fails. Exact diagnostic comparison in L6-delta.json finds six added pure-EXPOSE unsupported-dot diagnostics,290→296, no removed identities. Generated/runtime checks resolve those six outputs. This is not a green static-validator claim.

[AGENT] Current-generation consumer adaptation preserves historical numerical evidence and explicitly adds2 inputs/6 outputs. consumer-validation.md records166passes before the later documentation-only source citation fix. Fresh generation after that fix preserves all manual code; final-consumers.log checks current family/snapshot/metadata. Existing Boolean serialization warnings remain.
