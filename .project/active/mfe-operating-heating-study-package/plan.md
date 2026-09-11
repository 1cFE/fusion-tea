# Package migration plan

[AGENT] Approved one-phase implementation under T-017, 2026-09-11. Execute the whole phase through `my-implement`, then obtain a fresh `my-audit`. Existing goal authorization supplies routine approval. Use `.codex-test/run` for Python/model commands and the documented TEAx PYTHONPATH. No dependency installation or synchronization.

## Phase 1 — Migrate and verify current consumers

- [ ] Inspect the audited interface and current route/metadata producer; record the concrete migration and preserve model/generated/history bytes.
- [ ] Update current route channels, oracle operand bindings and assertion identities, annex and meaningful test expectations.
- [ ] Refresh metadata/manifest through existing native producers; retain exact command and output identities, and reproduce metadata to a fixed point.
- [ ] Run actual current-package baseline/reserve/demand execution and oracle/verdict verification. Retain missing-binding, altered-channel and verdict-mismatch negative tests.
- [ ] Run the four named consumer modules plus relevant route/shared regression with TEAx required; record counts and exact graph-derived census/reachability expectations.
- [ ] Write implementation evidence, preservation results and outstanding limits. Return for fresh independent coding audit; do not self-certify or invoke integration.

## Audit gate

- [ ] Fresh independent `my-audit` verifies SC-1–4, product fit and actual current-package tests. Parent freezes the certificate before any integration task.
