# Package migration plan

[AGENT] Approved one-phase implementation under T-017, 2026-09-11. Execute the whole phase through `my-implement`, then obtain a fresh `my-audit`. Existing goal authorization supplies routine approval. Use `.codex-test/run` for Python/model commands and the documented TEAx PYTHONPATH. No dependency installation or synchronization.

## Phase 1 — Migrate and verify current consumers

- [x] Inspect the audited interface and current route/metadata producer; record the concrete migration and preserve model/generated/history bytes.
- [x] Update current route channels, oracle operand bindings and assertion identities, annex and meaningful test expectations.
- [x] Refresh metadata/manifest through existing native producers; retain exact command and output identities, and reproduce metadata to a fixed point.
- [x] Run actual current-package baseline/reserve/demand execution and oracle/verdict verification. Retain missing-binding, altered-channel and verdict-mismatch negative tests.
- [x] Run the four named consumer modules plus relevant route/shared regression with TEAx required; record counts and exact graph-derived census/reachability expectations.
- [x] Write implementation evidence, preservation results and outstanding limits. Return for fresh independent coding audit; do not self-certify or invoke integration.

## Audit gate

- [ ] Fresh independent `my-audit` verifies SC-1–4, product fit and actual current-package tests. Parent freezes the certificate before any integration task.

## Implementation notes

### Phase 1 completion — 2026-09-11

[AGENT] Implemented the four current package files, four named test modules and six graph fixtures. Three native metadata refreshes reproduce; exact manifest/fixture fixed point and 642 preserved file hashes are recorded in `implementation/verification.md` and its evidence files. Stored baseline/reserve/demand controls independently verify all 18 predicates at worst channel relative deviation 1.3031089676201858e-16. Baseline retains its divertor violation.

Final graph/binding/annex battery: 79 passed. Broader current consumer/publication battery: 150 passed, 86 inherited historical-export failures, one absent historical-store skip. Separate late-added native zero-efficiency tests: two passed. Counts overlap; exact sets, intermediate failures, source identity proof and retained limitations are in `implementation/verification.md`. Formatting-only edits preserve parsed ASTs; scoped Ruff and diff checks pass.

[AGENT] The broader regression's 86 historical-export failures require separately scoped follow-up, not changes to this item's current package interface. Parent confirmed that classification. No shared producer, model, generated file or historical exporter was changed. Implementation is ready for a fresh independent coding audit; this author does not certify SC-4 or invoke integration.
