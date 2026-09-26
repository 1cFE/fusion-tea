# Review brief: WI-094 implementation (fresh, focused, executed evidence)

You are a fresh reviewer with no prior context. Do not orient yourself in the project: read only the files named here; do not read trails, goal directories other than these files, prior reviews or precedent collections; do not delegate; do not run the generator, the build or any test suite (you may run the two replay commands named below into a scratch directory if you judge it necessary; they take a few minutes). Budget: about twelve tool calls and a 450-word return. If evidence named here is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict.

## The question

A modeling work item implemented a costed variant of an existing assembly (a Stellaris helium primary loop feeding an ARIES Brayton cycle, with purchase, fuel, ledger and lifecycle accounting added from existing definitions). Check the executed evidence against the item's acceptance criteria and the MR-7 requirement, and return PASS, FINDINGS (each marked correct-before-use or note) or OWNER_GATE. Answer these five questions:

1. **Reuse rule.** Does `evidence/build-hashes.json` show every copied completion body `prefix_only: true` with `typed_adapter: false`, a `fixed_point: true`, and the staged sources equal to the canonical files? Spot-check two body diffs yourself (`diff` the source and target paths it names): only the import prefix (`from stellarator_tea.` / `from aries_integrated.` / `'aries_integrated.` → the new package name) may differ.
2. **Control replay.** Does `evidence/native_runs/summary.json` show the four positive-net control cases `control_exact: true` (every C-1 channel equal to its sealed WI-093 value under the key-prefix map) and the 4,000 kg/s case refused by the lifecycle body with the message `LCOE undefined for nonpositive net electricity`? Open one control's `result.json` and the sealed one and compare three channels yourself (`electrical__evaluate__net_electric`, `heat_exchangers__evaluate__unmet_heat`, `primary_loop__evaluate__q_ihx`).
3. **Identities.** Does `evidence/verification-summary.json` show `passed: true` with zero failures over every evaluated case, and does `verify.py` actually recompute the purchases, the capital chain, the annual accounts and the contribution sum from stored inputs and outputs rather than comparing the package to itself (read its `verify_case`)?
4. **MR-7 on executed evidence.** In the starting-point receipt on the ARIES-selected inventory (`native_runs/best-screen-point-aries-ratings/result.json` and `c1-aries-ratios-aries-ratings/result.json`): are the compressor and helium-duty screens violated with the booked purchase equal to the selected (smaller) rating's price, i.e. the inadequate selection stays visible and nothing was enlarged from demand? In the I-R receipt (`c1-aries-ratios-reselected-ratings`), do the purchases equal reference cost × selected / reference for all six priced items, with `cost_extrapolated` = 1 for the five ratings beyond 1.5× and 0 for the exchanger?
5. **Preservation and registration.** Does the goal's `evidence/preservation-check-t004-build.json` (and `-run.json` if present) show `passed: true` over the protected files, and does `tests/model_families.py` contain the `costed_loop_brayton` collection listing exactly the eleven library files the build stages plus the design file?

## Entry files

- The item: `work/active/WI-094_costed-loop-brayton/{spec.md (R1–R8), design.md (§ 1, § 3, § 4, § 6, § 7), report.md}`; `evidence/build-hashes.json`, `evidence/native_runs/summary.json` and the `result.json` files it names, `evidence/verification-summary.json`.
- The scripts: `exploration/costed_loop_brayton/{build.py, run.py, verify.py}`; the assembly `models/designs/costed_loop_brayton/costed_loop_brayton.sysml`.
- The sealed controls: `work/completed/20260926_WI-093_combination-assemblies/evidence/native_runs/<case>/result.json` (cases `baseline`, `c1-aries-ratios-reselected-ratings`, `c1-ratio1.35-reselected-ratings`, `c1-flow1400-aries-ratings`, `c1-flow4000-reselected-ratings`); their C-1 keys carry the prefix `combinations_loop_brayton__loop_brayton__`, the new package's `costed_loop_brayton__plant__`.
- Preservation: `work/orchestration/goals/design-study-parameters/evidence/preservation-check-t004-build.json` (and `-run.json`); registration: `tests/model_families.py`.
- The requirement: `modeling_project/REQUIREMENTS.md` § MR-7.
- Optional replay (scratch only): `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/costed_loop_brayton/run.py --root /tmp/wi094-replay'` then `.codex-test/run python exploration/costed_loop_brayton/verify.py --runs /tmp/wi094-replay --out-dir /tmp/wi094-replay`.

## Exclusions

Do not evaluate the study or the economics; do not review the oracle module or the manifest (a separate check covers them); do not propose new definitions; do not read the owner brief or the goal trail.
