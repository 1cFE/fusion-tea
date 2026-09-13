# Plan

- [x] Read T-043/native contracts and write proportional requirements/design/plan.
- [x] Capture prechange oracle positive controls/mappings, add focused tests and implement local/domain guards.
- [x] Coordinate WI-055 helper/receipt; migrate only directly affected current consumers and source expectations.
- [x] Verify current oracle and stable native package through focused/current coherent suites; join failures by identity.
- [x] Commit exact owned implementation/evidence and return for fresh independent audit.

No historical completion record is edited. Native package-dependent checks await author stability.

Initial oracle verification: all eleven public invalid-input tests fail on the entering oracle. After implementation all 30 focused tests pass, including local zero sizing, finite/sign cases, composed zero consumers, unchanged positive outputs and unit/scaling identities. The exact 99-input mapping and output mapping remain unchanged.

WI-055 supplied the matching `seed_and_generate` API and candidate receipt paths. The current helper/receipt points there. Existing executable-token preservation for sustainment remains applicable because its canonical change is documentation only. Magnet-field preservation excludes only the two explicitly authorized winding definitions; all text outside them stays compared to WI-051 entering bytes. Native-dependent acceptance is pending stable committed metadata.

Completion: Implementation `483fa60b` was included in WI-055's coherent suite at native commit `747a8a35`: 592 passed, 13 inherited skips, no failures/errors. Native attribution records 26 new passing nodes and no removed/failed nodes; the native author also added and passed two sustainment-zero tests after that collection. Reused that evidence without repeating the full model suite. Independent consumer acceptance on the committed package passed 195 tests: one three-point current/density route comparison, 27 existing clearance/cryo oracle checks and 167 existing radius/coverage checks. All eleven actual prechange oracle failures are joined by identity in `implementation/oracle-failure-attribution.json`; no pre-consumer native failure count was invented. Independent audit remains coordinator-owned.
