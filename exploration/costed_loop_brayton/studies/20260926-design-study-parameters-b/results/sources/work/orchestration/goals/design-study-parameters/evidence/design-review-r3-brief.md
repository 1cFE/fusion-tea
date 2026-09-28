# Review brief: WI-095 design (fresh, focused)

You are a fresh reviewer with no prior context. Do not orient yourself in the project: read only the files named here; do not read trails, goal directories other than the two files named, prior reviews or other work items; do not delegate; run nothing. Budget: about eight tool calls and a 400-word return. If evidence named here is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict.

## The question

A modeling item designs a small additive control calculation that enforces a loop's return-temperature requirement in an assembly that couples a helium primary loop to a closed Brayton cycle through one exchanger. Answer the five questions in `work/active/WI-095_loop-return-control/design.md` § 8 against the entry files, and return PASS, FINDINGS (each marked `correct-before-implementation` or `note`) or OWNER_GATE. Check the physics of § 1–§ 2 yourself: derive the mixed-return identity from the definitions, check the monotonicity claim on the effectiveness-NTU form, and check whether the cycle stream's outlet depends on anything but the transferred duty.

## Entry files

- The item: `work/active/WI-095_loop-return-control/{spec.md, design.md}`.
- The loop definition: `models/library/analyses/mfe_primary_loop.sysml` (the 'Primary Coolant Loop' doc block and its equations, lines 1–75).
- The closure: `models/library/analyses/integrated_heat_electricity.sysml` (calc def 'Network Heat Driven Closure', lines 110–200) and its body `exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py` (lines 15–105).
- The assembly the bindings go into: `models/designs/costed_loop_brayton/costed_loop_brayton.sysml` (parts `primary_loop` lines 32–70, `heat_exchangers` lines 213–262, `checks` lines 449–463).
- The requirement: `modeling_project/REQUIREMENTS.md` § MR-7.
- The owner's direction the item answers: `work/orchestration/goals/design-study-parameters/evidence/owner-direction-round3.md`; the residuals it responds to: `work/orchestration/goals/design-study-parameters/evidence/return-condition-check.md`.

## Exclusions

Do not evaluate the goal's study, its economics or the sealed record; do not propose alternative control architectures beyond judging the two the design names; do not read the owner brief or the goal trail.
