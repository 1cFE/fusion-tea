# T-043 verification

Status: Oracle implementation verified; stable native-package acceptance and independent audit pending.

Before changes, eleven public-oracle invalid-input tests failed; raw identities and failures are in `oracle-before-tests.txt`. After deliberate sizing/stress/sustainment guards, all 30 tests in `tests/study/test_winding_consumers.py` pass (`oracle-after-tests.txt`). Commands: `.codex-test/run python -m pytest tests/study/test_winding_consumers.py -k invalid_public -q --tb=short` before changes, then the same command without `-k invalid_public` afterward.

Three saved positive full-oracle maps in `oracle-before.json` remain exactly equal: default, 10% higher current and 20% higher density. Independent checks establish the square pack area in mm², current-density identity, square-root scaling and the factor 1000 in the substituted stress relation. Local zero current returns zero side. Full current-zero execution deliberately refuses at stress; standalone and public zero-field linkage reach the existing sustainment consumer's RuntimeError. Both adapter mappings remain exactly unchanged; no new channel or supported key was added.

Current generation and exact package-receipt consumers point to WI-055. Historical generators, receipts and outputs are unchanged. The radius preservation test excludes only the two explicitly changed winding calculation definitions from its original byte comparison; sustainment retains its original executable-token check. Final current-package checks wait for committed native metadata and will be recorded separately.
