# Review brief: WI-095 implementation (fresh, focused, executed evidence)

You are a fresh reviewer with no prior context. Do not orient yourself in the project: read only the files named here; do not read trails, goal directories other than these files, prior reviews or other work items; do not delegate; do not run the generator, the build or any test suite. Budget: about twelve tool calls and a 450-word return. If evidence named here is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict.

## The question

A modeling item added one calculation ('Primary Bypass Control') and two checks to an existing costed assembly so that a loop's return-temperature requirement is enforced. Check the executed evidence against the item's design and the MR-7 requirement, and return PASS, FINDINGS (each marked correct-before-use or note) or OWNER_GATE. Five questions:

1. **The body is the definition.** Compare `exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py` with the calc def's doc in `models/library/analyses/loop_return_control.sysml`: is every output computed as the doc states (the effectiveness-NTU form, the bisection with its two raising guards, `exchanger_return` from the achieved capability in both branches, the residual as `(duty − capability(f)) / C_h` plus the loop-side identity)? Is anything computed from the duty that the design (`work/active/WI-095_loop-return-control/design.md` § 3) says must come from the capability?
2. **Pre-change control.** Does `work/active/WI-095_loop-return-control/evidence/return-control-verification.json` show, for every evaluated case, `compared: 245` numeric channels with zero differences against the WI-094 receipts, and the refused case refused in both? Open one case in both directories (`…/WI-095_loop-return-control/evidence/native_runs/c1-aries-ratios-reselected-ratings/result.json` and `…/WI-094_costed-loop-brayton/evidence/native_runs/c1-aries-ratios-reselected-ratings/result.json`) and compare three channels yourself (`electrical__evaluate__net_electric`, `heat_exchangers__evaluate__he_capability`, `lifecycle_price__evaluate__lcoe`).
3. **The new channels and checks on executed evidence.** In the same WI-095 receipt: is `bypass_fraction` about 0.31 with `feasible` 1, `capability_at_solution` equal to the duty `primary_loop__evaluate__q_ihx` within 1e-9 MW, `return_residual_magnitude` below 1e-9 K, and both new verdicts satisfied? In `c1-ratio1.35-reselected-ratings`: `feasible` 0, `return_residual` about +17.8 K, `return_condition_ok` violated while `bypass_within_limit` is satisfied? Does the identity summary's `identities` block hold on every evaluated case?
4. **MR-7.** In the assembly (`models/designs/costed_loop_brayton/costed_loop_brayton.sysml`, part `return_control` and the two new asserts in part `checks`): are flow, ratio, area and ratings still chosen inputs, is the bypass fraction a calculated setting, are `max_bypass` and `tolerance` declared inputs with their grades, and is nothing sized from a demand? Is 'Bypass Within Limit' vacuous at `max_bypass = 1.0`, and is that stated in the assembly's doc line?
5. **Fixed point, registration and preservation.** Does `…/WI-095_loop-return-control/evidence/build-hashes.json` show `fixed_point: true` with 13 sources and 25 bodies, all `prefix_only: true`? Does `tests/model_families.py` list `analyses/loop_return_control.sysml` in the `costed_loop_brayton` collection? Does `work/orchestration/goals/design-study-parameters/evidence/preservation-check-t010-build.json` show `passed: true`?

## Entry files

- The item: `work/active/WI-095_loop-return-control/{spec.md, design.md}`; `evidence/{build-hashes.json, return-control-verification.json, native_runs/<case>/result.json}`.
- The definition and body: `models/library/analyses/loop_return_control.sysml`; `exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py`; the verifier `exploration/costed_loop_brayton/verify_return_control.py`.
- The assembly: `models/designs/costed_loop_brayton/costed_loop_brayton.sysml` (parts `return_control`, `checks`, `primary_loop`, `heat_exchangers`).
- The WI-094 receipts: `work/active/WI-094_costed-loop-brayton/evidence/native_runs/<case>/result.json`.
- Registration and preservation: `tests/model_families.py`; `work/orchestration/goals/design-study-parameters/evidence/preservation-check-t010-build.json`.
- The requirement: `modeling_project/REQUIREMENTS.md` § MR-7.

## Exclusions

Do not evaluate the goal's study or economics; do not review the oracle module or the manifest (a separate check covers them); do not propose new definitions; do not read the owner brief or the goal trail.
