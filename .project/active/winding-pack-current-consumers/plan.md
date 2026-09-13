# Plan

- [x] Read T-043/native contracts and write proportional requirements/design/plan.
- [x] Capture prechange oracle positive controls/mappings, add focused tests and implement local/domain guards.
- [x] Coordinate WI-055 helper/receipt; migrate only directly affected current consumers and source expectations.
- [ ] Verify current oracle and stable native package through focused/current coherent suites; join failures by identity.
- [ ] Commit exact owned implementation/evidence and return for fresh independent audit.

No historical completion record is edited. Native package-dependent checks await author stability.

Initial oracle verification: all eleven public invalid-input tests fail on the entering oracle. After implementation all 30 focused tests pass, including local zero sizing, finite/sign cases, composed zero consumers, unchanged positive outputs and unit/scaling identities. The exact 99-input mapping and output mapping remain unchanged.

WI-055 supplied the matching `seed_and_generate` API and candidate receipt paths. The current helper/receipt points there. Existing executable-token preservation for sustainment remains applicable because its canonical change is documentation only. Magnet-field preservation excludes only the two explicitly authorized winding definitions; all text outside them stays compared to WI-051 entering bytes. Native-dependent acceptance is pending stable committed metadata.
