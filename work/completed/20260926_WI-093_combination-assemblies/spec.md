---
Status: completed
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-26
Updated: '2026-09-26'
---

# Combination assemblies from existing definitions

## Problem and intended use

[INHERITED: goal `design-space-combinations`, owner brief part A] The write-up's structural claim is untested: "This work demonstrated particular connections and reuse, not a systematic set of substitutions between the Stellaris and ARIES assemblies." Round 1 of the goal mapped which alternatives are interface- and range-compatible (`work/orchestration/goals/design-space-combinations/evidence/compatibility-map.md` § 2–3) and executed the input-expressible ones. This item builds the assembly-level combinations from existing definitions only and evaluates them, so the goal can record which combinations execute, which satisfy the evaluated engineering checks, and which need new model behavior.

## Requirements

- R1 [NEED, brief A] Assemble previously untested compatible combinations from existing definitions: C-1 the Stellaris helium loop into the ARIES Brayton chain; C-2 the Stellaris parabolic plasma into the ARIES deposition, branch, closure, electrical and fuel chain with the ARIES capacity screens; C-4 the three ARIES branch temperatures into the lumped efficiency law with its domain constraint; C-5 the ARIES selected-purchase law on the Stellaris helium circulator. C-3 (ARIES divertor circuit into the Stellaris steam path) is deferred with its reason recorded.
- R2 [NEED, brief A] No new `calc def`, `part def`, `constraint def` or `port def`; no change to any reviewed completion body (a copy with the package prefix adapted, or the typed adapter the ARIES build applies, is reuse). A combination that would need either is recorded as requiring new behavior, with the missing relationship named, and is not implemented.
- R3 [NEED, MR-7] Every assembly states the role of each quantity (chosen, calculated, requirement, installed capacity, policy-selected); no automatic sizing; supplied ratings stay the basis of their screens; inherited operating-point directions ('Primary Coolant Loop' flow from duty and rise; the closure solving temperatures only) are disclosed, not changed; re-selected ratings and pressure ratios are explicit choices.
- R4 [NEED, MR-4] Every inherited value carries its source and grade: `[INHERITED: Stellaris]` from `models/designs/stellarator_09/stellarator_plant.sysml` or the documented baseline `work/analysis/model-evaluation-diagnostics/baseline.json`; `[INHERITED: ARIES]` from `models/designs/aries_cs_integrated/plant.sysml`; `[ASSUMED]` for re-selections, with the reason.
- R5 [NEED, brief A] Each assembly is evaluated through the generated package's own graph with its constraint report on named cases; per case the record states executes / satisfies which checks / refused with the body's message. Independent verification is by energy, state and accounting identities on the stored outputs (the WI-087 pattern), not a second implementation.
- R6 [INFERRED] Reuse is counted by the transfer register's measurement rule: definitions instantiated unchanged, copied completion bodies with prefix adaptation counted separately from mathematical changes, new case bindings; no reuse fraction over arbitrary counts.
- R7 [INFERRED] The new design directory is registered in `tests/model_families.py` and the package builds to a fixed point under stock regeneration with preserved handwritten bodies; the Stellaris and ARIES packages, the library and both live assemblies are unchanged (goal preservation manifest).

## Scope and limits

In scope: `models/designs/combinations/*.sysml`, `exploration/combinations/` (build, package, run, verify, evidence), the registry entry. Out of scope: any library or body change; C-3; costing beyond C-5's one leaf; scientific qualification of any inherited value; a study record (the cases are this item's native evidence). Review: focused fresh design review before implementation (new interfaces between definitions that never partnered) and fresh implementation review after.

## References

Goal `work/orchestration/goals/design-space-combinations/` (`goal.md`, `evidence/compatibility-map.md`, `choice-inventory.md`, `scratch-screens.md`, `learnings.md` L-001, L-002, L-007); `modeling_project/REQUIREMENTS.md` MR-3, MR-4, MR-7; `work/orchestration/aries-transfer-experiment/change-register.md` § Measurement rule; `exploration/aries_transfer/nominal_brayton/{build.py, run.py}` (package pattern); `exploration/aries_integrated/build.py` (typed adapters, fixed-point proof).
