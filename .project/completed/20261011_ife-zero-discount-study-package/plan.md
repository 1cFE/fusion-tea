# Package refresh plan

[AGENT] Approved one-phase implementation under T-011 on 2026-09-11. Use `my-implement`, then fresh `my-audit`; no extra permission pause is needed. All Python runs through `.codex-test/run`; use the documented TEAx PYTHONPATH. Preserve other worktree edits.

## Phase 1 — Migrate and verify the package

- [x] Update route channels, oracle duration-key validation, metadata axis declaration and annex to match WI-049.
- [x] Update meaningful native route tests for 32 outputs, new duration keys, old-key rejection and exact zero/signed-near-zero/non-generation cases. Preserve ordinary failures and strict eligibility.
- [x] Run the native metadata producer into fresh local validation storage; retain its command and output identity. Repeat to verify metadata fixed point.
- [x] Run affected route and shared multiplication verifier/indicator tests with actual TEAx execution. Record counts, limitations and model/package non-mutation.
- [x] Record implementation evidence and request fresh coding audit. Audit owns success-criterion certification; parent owns later integration and study decisions.

## Implementation notes

[AGENT] Completed 2026-09-11. `implementation.md` records 45 passing tests, twenty actual stored cases, native metadata fixed point and unchanged audited model/package. One first-run failure exposed a test's dependency on the prior live axis declaration; its physical-axis multiplication assertions now use an explicit test declaration and remain unchanged. The current discount-rate declaration is separately asserted. No additional implementation stage or shared-tool change was needed. Fresh coding audit remains pending.
