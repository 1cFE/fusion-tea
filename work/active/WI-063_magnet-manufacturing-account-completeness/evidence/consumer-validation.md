# WI-063 consumer adaptation checks

[AGENT] Historical replay keeps physical geometry and sets only the new sheet-stock price to zero. Public contract additions are explicitly three inputs and five outputs; no prior support input is retired. New inventory arithmetic is independently covered by the WI063 native/oracle suites owned by other workers.

## Commands and receipts

- Initial command: `.codex-test/run python -m pytest tests/study/test_domain_consumers.py tests/study/test_winding_consumers.py -q -k 'not stock_route'`. Result: 57 passed, one failure. The exclusion did not match the native test name, so it prematurely executed against the pre-WI063 generated package and refused the new entry key. Preserved as `consumer-premature-native.log`; this is an execution-selection mistake, not a semantic result.
- Corrected oracle-only command: `.codex-test/run python -m pytest tests/study/test_domain_consumers.py tests/study/test_winding_consumers.py -q -k 'not current_native'`. Result: 57 passed, one deselected; `consumer-oracle-only.log`.

No historical study record was edited.

## Generated package checks

- Producer: `.codex-test/run python work/active/WI-063_magnet-manufacturing-account-completeness/evidence/rederive-consumers.py`; success at semantic17da5a058e674547143f7df8ddb3a71909e4b9f06f465fcdff051b0fb20ac209; `consumer-rederive.log`. Five expectations and explicit reachability contract came from native producer output.
- Family/radius/operating command: `.codex-test/run python -m pytest tests/models/test_model_family_spines.py tests/models/test_mfe_major_radius.py tests/models/test_mfe_operating_heating.py -q`; 39 passes and46 radius fixture errors from stale standalone CLI economic anchors. Preserved `consumer-family-radius.log` and `consumer-stale-cli-anchors.log`. Coordinator corrected independently checked anchors. Complete radius rerun: `.codex-test/run python -m pytest tests/models/test_mfe_major_radius.py -q`; 63 passes in34.13s, `consumer-radius-final.log`. Other39 passes reused.
- Affected native/study command: `.codex-test/run python -m pytest tests/models/test_winding_pack_fit.py tests/models/test_winding_pack_cost.py tests/models/test_tape_procurement.py tests/models/test_conductor_current.py tests/models/test_coil_thermal_inventory.py tests/models/test_structure_translation.py tests/study/test_domain_consumers.py tests/study/test_winding_consumers.py tests/study/test_known_answers.py tests/study/test_major_radius.py tests/study/test_operand_bindings.py tests/study/test_verify_operands.py tests/study/test_verify.py tests/study/test_output_contract.py -q`; 713 passes,1 inherited historical-store skip,6 failures and10 fixture errors in329.43s. `consumer-native-study.log` preserves results. Four failures and10 errors are the expected uncommitted-package refusal; verifier requires a checkpoint. Two actual assertion failures in operand tests were repaired: the independent headline updated from WI060 to WI063, and the explicit ABI arithmetic now uses baseline265 plus named additions (the prior273 already included eight WI062 parameters).

No package-clean rule was bypassed.

## Final focused receipts

- `.codex-test/run python -m pytest tests/study/test_operand_bindings.py -q`: 17 passes in5.95s, `consumer-operands-final.log`; supersedes the two stale operand assertions in the original batch.
- After checkpoint19e47125, `.codex-test/run python -m pytest tests/study/test_verify.py tests/study/test_major_radius.py -q`: 189 passes,1 skipped and1 failure in185.77s, `consumer-clean-final.log`. The skip is the unavailable historical proof-of-life store. All verifier cases passed. The remaining study-radius assertion omitted the inherited WI062 reference-conductor violation at R14; its exact expected set now includes that named predicate. Its native/oracle comparison passed for228/212 channels with worst relative deviation1.7479207264331552e-15 and20 authored verdicts.
- `.codex-test/run python -m pytest tests/study/test_major_radius.py -q`: complete file167 passes in11.63s, `consumer-study-radius-final.log`. This supersedes the remaining stale R14 verdict assertion. No additional model/package changes were needed.

All affected files now have passing final coverage. The original713 passes are retained; focused reruns supersede the unsuccessful cases and are not added as disjoint test totals. Likewise63 model-radius passes supersede46 fixture errors and overlap earlier passing radius cases. The inherited Boolean serializer warnings and unavailable-store skip remain disclosed. No full repository battery is claimed.
