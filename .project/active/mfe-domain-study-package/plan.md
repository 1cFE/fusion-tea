# Implementation plan

Scope authorized by T-035 brief. All steps are routine work within that scope.

- [x] Capture independent oracle valid controls before edits and add focused invalid/valid tests.
- [x] Implement the two guards and run oracle-only acceptance.
- [x] After T-034 stable regeneration, run current public-route baseline/coverage controls and classify any failures by identity.
- [x] Record evidence, commit owned paths and return for coordinator-obtained independent audit.

## Implementation notes

Current adapter has 99 mappings; ambient temperature is not mapped. No adapter change is expected. CURRENT_WORK belongs to another session and will not be edited.

2026-09-13: Added focused test file after capturing four full oracle controls in `implementation/oracle-before.json`. Before correction, 21 named domain cases failed and five valid/coverage cases passed. Added guards before bore and COP divisions without altering existing expressions. After correction, all 26 tests pass; exact valid outputs and independent field/refrigeration identities pass. Native author confirms `ValueError` for the same domains with unchanged interfaces. Native acceptance is pending stable regeneration. Raw command outputs are retained in `implementation/tests-before.txt` and `implementation/tests-after.txt`.

2026-09-13 completion: The original 13 m coil-centre counterexample was added, producing 27 focused passes. After stable native metadata, the current-route suite passed 166 checks and stopped one baseline verifier on the uncommitted generated package. After native production commit `3d9711e2`, that exact failed check passed. All 167 current-route checks now pass across the initial attempt and bounded retry. Full baseline/R=14 control maps, package identity and verification summary are retained alongside raw outputs. Production is committed at `c6c04d32`; completion evidence is returned for coordinator-obtained independent audit. No adapter or historical-test changes were needed.
