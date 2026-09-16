# WI-063 consumer adaptation checks

[AGENT] Historical replay keeps physical geometry and sets only the new sheet-stock price to zero. Public contract additions are explicitly three inputs and five outputs; no prior support input is retired. New inventory arithmetic is independently covered by the WI063 native/oracle suites owned by other workers.

## Commands and receipts

- Initial command: `.codex-test/run python -m pytest tests/study/test_domain_consumers.py tests/study/test_winding_consumers.py -q -k 'not stock_route'`. Result: 57 passed, one failure. The exclusion did not match the native test name, so it prematurely executed against the pre-WI063 generated package and refused the new entry key. Preserved as `consumer-premature-native.log`; this is an execution-selection mistake, not a semantic result.
- Corrected oracle-only command: `.codex-test/run python -m pytest tests/study/test_domain_consumers.py tests/study/test_winding_consumers.py -q -k 'not current_native'`. Result: 57 passed, one deselected; `consumer-oracle-only.log`.

Native-dependent checks await regenerated package and coordinator repin. No historical study record was edited.
