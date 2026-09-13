# Implementation plan

Scope authorized by T-035 brief. All steps are routine work within that scope.

- [x] Capture independent oracle valid controls before edits and add focused invalid/valid tests.
- [x] Implement the two guards and run oracle-only acceptance.
- [ ] After T-034 stable regeneration, run current public-route baseline/coverage controls and classify any failures by identity.
- [ ] Record evidence, commit owned paths and return for coordinator-obtained independent audit.

## Implementation notes

Current adapter has 99 mappings; ambient temperature is not mapped. No adapter change is expected. CURRENT_WORK belongs to another session and will not be edited.

2026-09-13: Added focused test file after capturing four full oracle controls in `implementation/oracle-before.json`. Before correction, 21 named domain cases failed and five valid/coverage cases passed. Added guards before bore and COP divisions without altering existing expressions. After correction, all 26 tests pass; exact valid outputs and independent field/refrigeration identities pass. Native author confirms `ValueError` for the same domains with unchanged interfaces. Native acceptance is pending stable regeneration. Raw command outputs are retained in `implementation/tests-before.txt` and `implementation/tests-after.txt`.
