# Implementation Plan: Cleanup `--feedback` Flag

**Status:** Draft
**Created:** 2026-05-17 09:42 PDT
**Last Updated:** 2026-05-17 09:42 PDT

## Source Documents

- **Spec:** `.project/active/cleanup-feedback-flag/spec.md`
- **Design:** `.project/active/cleanup-feedback-flag/design.md` ← component details, guard order, README diffs, invariants

## Implementation Strategy

**Phasing Rationale:**

Three phases, ordered by failure-surface. Phase 1 ships the `cmd_analyze` guard block (the part most likely to misorder or skip a check); it's pure validation, no loop changes, so it can be exercised end-to-end before any production code path actually consumes the new producer. Phase 2 wires the producer branch into `lib/loop.py` and deletes `_apply_external_feedback` — the smallest possible code change once Phase 1 has proven guard correctness. Phase 3 lands docs and argparse help, which are part of the contract per the design but carry no execution risk.

**Critical Path:**

cmd_analyze guards (Phase 1) → loop producer branch + deletion (Phase 2) → docs (Phase 3). Each phase is independently mergeable; together they satisfy all spec acceptance criteria.

**First Proof Point:**

A `cmd_analyze` invocation with `--feedback /nonexistent`, `--feedback <empty>`, `--feedback <no-VERDICT>`, and `--feedback <no-Category>` all exit 1 with distinct, design-mandated messages — before any iter directory is created. If that proof passes, the rest of the change is mechanical.

**Overall Validation Approach:**

- Each phase starts with a test stencil.
- Phase 1 and Phase 2 ship unit tests in `exploration/concept_analysis/scripts/test_failure_chains.py` (the project's existing failure-mode test file).
- Phase 2 includes a real-pipeline smoke test on concept 28 (the original failure case).
- Existing `test_failure_chains.py`, `test_staleness.py`, `test_validators.py` must pass unchanged across all phases.

---

## Phase 1: `cmd_analyze` Guard Block

### Goal

Replace the existing guard cluster + `_apply_external_feedback` dispatch in `cmd_analyze` with a fail-fast guard block that enforces FR-5, FR-6 (a)(b)(c)(d)(e), and the implicit-resume promotion. **Do not yet rewire the loop** — Phase 1 leaves `_apply_external_feedback` in place but unreachable (calls go through the new guards first, then fall into the existing dispatch). This isolates the guard work for verification before the loop changes land.

### Assumption Under Test

That the guard order in `design.md#implementation-notes` produces correct fail-fast behavior in all six failure modes from the spec's acceptance criteria, and that the implicit-resume promotion doesn't disturb other code paths.

### Test Stencil (write first)

```python
class TestExternalFeedbackGuards:
    def test_missing_file_exits_one(self, tmp_path, capsys):
        rc = run_cmd_analyze(["analyze", "28", "--feedback", str(tmp_path / "nope.md")])
        assert rc == 1
        assert "not found" in capsys.readouterr().err.lower()

    def test_empty_file_exits_one(self, tmp_path, capsys):
        f = tmp_path / "empty.md"; f.write_text("")
        rc = run_cmd_analyze(["analyze", "28", "--feedback", str(f)])
        assert rc == 1 and "empty" in capsys.readouterr().err.lower()

    def test_no_verdict_exits_one(self, tmp_path):
        # writes a file with content but no VERDICT line; expects validator's fix_message
        ...

    def test_no_category_exits_one(self, tmp_path):
        # VERDICT: FINDINGS + ### F-1 header, no Category line; expects fix_message
        ...

    def test_force_combo_exits_one(self, tmp_path):
        # --feedback + --force; existing guard with updated message
        ...

    def test_missing_analysis_md_exits_one(self, tmp_path):
        # concept dir has no analysis.md; spec FR-6(a)
        ...
```

### Changes Required

**See design for:** `design.md#component-overview` (cmd_analyze), `design.md#implementation-notes` (guard order a–g).

- [x] **Test file:** add `TestExternalFeedbackGuards` to `exploration/concept_analysis/scripts/test_failure_chains.py` using the stencil. One test per failure mode in `spec.md#failure-modes-all-exit-non-zero-before-invoking-claude-and-before-creating-any-iter-directory`.
- [x] **`run_analysis.py:301-321`** — replaced the existing `--feedback` guard block with the new guard order.
- [x] **Guard (f) cold-start incompatibility** — placed in the file-level guard block instead of the per-concept loop (see deviation note in Phase 1 Completion).
- [x] **Leave `_apply_external_feedback` and its dispatch in place** — still reachable in Phase 1.
- [x] **Import** `validate_feedback_verdict` at the top of `run_analysis.py`.

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_failure_chains.py -k ExternalFeedbackGuards` → 7 passed
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/` → 257 passed, 5 skipped (pre-existing)

**Manual:** deferred — covered by automated tests above; no production smoke run in Phase 1 because the new path is gated by Phase 2's producer.

**What We Know Works After This Phase:**

All six failure modes correctly reject before any iter directory is created. Implicit-resume promotion is in place. `_apply_external_feedback` still runs on valid input (legacy behavior preserved temporarily). Phase 2 can swap the dispatch with confidence that the guards are correct.

---

## Phase 2: Producer Branch + Delete Legacy

### Goal

Add the external-feedback producer branch to `lib/loop.py` and delete `_apply_external_feedback` plus its dispatch in `cmd_analyze`. After this phase, the new producer is the only `--feedback` code path.

### Assumption Under Test

That a `--feedback` invocation produces an `iter-N/pre_feedback.md` byte-equal to the source file, the source file is untouched, and the full analyze → model_setup → assess sequence runs against the user's findings (FR-1 through FR-4).

### Test Stencil (write first)

```python
class TestExternalFeedbackProducer:
    def test_pre_feedback_byte_equal_to_source(self, fixture_concept_at_iter3, tmp_path):
        cr = tmp_path / "cr.md"
        cr.write_text("VERDICT: FINDINGS\n\n### F-1: x\n- Category: model\n")
        # Mock invoke_claude so analyze/model_setup/assess return success without calling out.
        run_loop(fixture_concept_at_iter3, feedback=cr, add_passes=1)
        new_iter = fixture_concept_at_iter3.dir / "iter-4"
        assert (new_iter / "pre_feedback.md").read_bytes() == cr.read_bytes()
        assert cr.exists()  # source untouched
```

Plus one integration-style test that runs `--add-passes 2` and asserts iter-(N+1) consumes iter-N's `post_feedback.md`, not the source CR (FR-3).

### Changes Required

**See design for:** `design.md#architecture` (producer chain), `design.md#component-overview` (run_stage1_loop), `design.md#implementation-notes` (pseudocode for the branch).

- [x] **Test file:** added `TestExternalFeedbackProducer` to `test_failure_chains.py` (2 tests: byte-equality + one-shot fall-through).
- [x] **`lib/loop.py`** — added `used_external_feedback = False` to producer-flag init.
- [x] **`lib/loop.py`** — inserted external-feedback branch at top of producer cascade.
- [x] **`run_analysis.py`** — deleted the `_apply_external_feedback` dispatch.
- [x] **`run_analysis.py`** — deleted `_apply_external_feedback` function in full.
- [x] **`run_analysis.py`** — removed now-unused `propagate_staleness` and `datetime` imports.
- [x] **Grep check:** only one match remains, a comment in `test_failure_chains.py` noting the H-08 tests' removal.

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/test_failure_chains.py -k ExternalFeedbackProducer` → 2 passed
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/` → 257 passed, 5 skipped (no regressions)
- [x] `grep _apply_external_feedback exploration/concept_analysis/scripts/` → only the comment remains

**Manual smoke test on concept 28:** deferred to user — requires a real Claude run. The byte-equality and one-shot-fall-through invariants are covered by `TestExternalFeedbackProducer`.

**What We Know Works After This Phase:**

The concept-28 silent-drift bug is no longer reachable. Full end-to-end iteration runs from a custom feedback file. `_apply_external_feedback` is gone. All previously-passing tests still pass.

---

## Phase 3: Docs and Argparse Help

### Goal

Update the README and argparse help text to reflect the new contract. No code paths change in this phase; this is the user-facing surface area called out in spec FR-8.

### Assumption Under Test

That a user reading the README or `--help` output for the first time after this change can produce a working `--feedback` invocation without needing the conversation history that produced this spec.

### Test Stencil (write first)

```python
def test_readme_documents_single_step_workflow():
    text = Path("exploration/concept_analysis/README.md").read_text()
    # Old two-step pattern must be gone.
    assert "Step A" not in text and "Step B" not in text
    # New producer-table row exists.
    assert "external" in text and "--feedback PATH" in text
    # Mutual-exclusion list no longer claims --feedback + --resume conflict.
    assert "--feedback` and `--resume`" not in text
```

(One small grep-style test in any existing test file is sufficient — this is a regression guard against the docs drifting back.)

### Changes Required

**See design for:** `design.md#component-overview` (README block) and `design.md#implementation-notes` (exact replacement copy).

- [x] **`README.md`** — inserted priority-0 producer-table row.
- [x] **`README.md`** — replaced `--feedback PATH` flag-table description.
- [x] **`README.md`** — removed the `--feedback` and `--resume` line; updated the `--feedback` and `--force` line with the cold-start tagline.
- [x] **`run_analysis.py`** — replaced argparse help text.
- [x] **Stale-reference search** — `grep "Step A|Step B|change_requests"` against the README returned no matches.

### Validation

**Automated:**
- [x] New regression test (`test_readme_documents_single_step_external_feedback`) passes.
- [x] `grep "Step A\|Step B\|change_requests" exploration/concept_analysis/README.md` → no matches.
- [x] `analyze --help` displays the new `--feedback` text.

**Manual:** producer table and flag table reviewed in-place; rows read cleanly with surrounding context.

**What We Know Works After This Phase:**

Docs match the implementation. A new user can discover and use `--feedback` correctly from the README alone.

---

## Environment Setup

See `CLAUDE.md` for `uv` usage. All test invocations: `uv run python -m pytest <path>`. Pipeline smoke: `uv run python exploration/concept_analysis/scripts/run_analysis.py ...`.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-specific mitigations:**

- **Phase 1:** Guard ordering is the dominant risk. Mitigated by writing one test per failure mode *before* the guard implementation — if the order is wrong, the tests fail with diagnostics that point at which check triggered.
- **Phase 2:** Subtle producer-chain interaction (could the new branch fire twice? Could it interact with `used_review_feedback`?). Mitigated by mirroring the established one-shot-flag pattern exactly (`used_external_feedback = False; ... = True` inside the branch).
- **Phase 3:** Documentation drift. Mitigated by the regression test in the stencil.

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion

**Completed:** 2026-05-17

**Changes Made:**
- `exploration/concept_analysis/scripts/run_analysis.py`: imported `validate_feedback_verdict`; replaced the `--feedback` guard block (was lines 301-321) with the new fail-fast sequence (force, single-concept, file-exists, non-empty, format, cold-start). Set `resume = True` implicitly when `--feedback` is set. The `_apply_external_feedback` dispatch remains in place (deleted in Phase 2).
- `exploration/concept_analysis/scripts/test_failure_chains.py`: added `TestExternalFeedbackGuards` with 7 tests covering all FR-6 (a–e) failure modes + the `--feedback + --force` combo + a happy-path test asserting valid input still reaches `_apply_external_feedback` (Phase 1 dispatch).

**Deviations from Plan:**
- Guard (f) (cold-start incompatibility / missing `analysis.md`) was placed in the file-level guard block in `cmd_analyze` rather than in the per-concept loop body as suggested. Rationale: in Phase 1 the per-concept loop is unreachable for `--feedback` runs because `_apply_external_feedback` still dispatches with `return`. Putting guard (f) in the per-concept loop would have made `test_missing_analysis_md_exits_one` un-testable until Phase 2. Single-concept enforcement (guard b) means `targets[0]` is well-defined, so resolving `ANALYSES_DIR / targets[0]["_id"] / "analysis.md"` in the file-level block is safe.

**Validation:**
- `uv run python -m pytest exploration/concept_analysis/scripts/test_failure_chains.py -k ExternalFeedbackGuards` → 7 passed
- `uv run python -m pytest exploration/concept_analysis/scripts/` → 257 passed, 5 skipped (no regressions)


### Phase 2 Completion

**Completed:** 2026-05-17

**Changes Made:**
- `exploration/concept_analysis/scripts/lib/loop.py`: added `used_external_feedback = False` flag init; inserted the new external-feedback producer branch at the top of the cascade. The branch checks `getattr(args, "feedback", None)`, sets `feedback_source = "external"`, calls `_copy_to_pre_feedback(Path(args.feedback), iter_dir)`, prints a one-line announcement, and short-circuits research / review / source-integration / assess producers for the one iter it fires.
- `exploration/concept_analysis/scripts/run_analysis.py`: removed the `if feedback: _apply_external_feedback(...); return` dispatch; deleted `_apply_external_feedback` (79 lines); removed now-unused `propagate_staleness` and `datetime` imports.
- `exploration/concept_analysis/scripts/test_failure_chains.py`:
  - Deleted `TestIntegration_ExternalFeedback` (the two H-08 tests for the legacy function) and replaced with a comment pointing readers to the new producer tests.
  - Re-wired `TestExternalFeedbackGuards._run` to patch `run_stage1_loop` (not `_apply_external_feedback`); renamed unpack targets accordingly.
  - Rewrote `test_valid_pass_verdict_dispatches_to_legacy` → `test_valid_input_dispatches_to_loop_with_resume`, asserting the implicit `resume=True` promotion.
  - Added `TestExternalFeedbackProducer` with 2 tests: byte-equality of `iter-N/pre_feedback.md` to source + source file untouched (FR-1, FR-4); one-shot semantics across two iters with `--add-passes 2` (FR-3).

**Deviations from Plan:**
- None of substance. Used `file_writes` rather than `file_edits` in the FakeClaude scripts because there is no prior `model_setup.py` in iter-1 (fresh write), and `file_writes` works whether or not the path exists.

**Validation:**
- Producer tests: 2/2 passed
- Guard tests after rewiring: 7/7 passed
- Full suite: 257 passed, 5 skipped (pre-existing). `_apply_external_feedback` grep returns only the explanatory comment in test_failure_chains.py.


### Phase 3 Completion

**Completed:** 2026-05-17

**Changes Made:**
- `exploration/concept_analysis/README.md`: added priority-0 row to the producer-selection table for the external-feedback producer; rewrote the `--feedback PATH` flag-table description to match the new contract (requires `analysis.md`, implies `--resume`, runs full iter); deleted the `--feedback` and `--resume` mutual-exclusion bullet and rewrote the `--feedback` and `--force` bullet with the cold-start tagline.
- `exploration/concept_analysis/scripts/run_analysis.py`: replaced argparse help text for `--feedback`.
- `exploration/concept_analysis/scripts/test_failure_chains.py`: added `test_readme_documents_single_step_external_feedback` doc-drift regression guard.

**Deviations from Plan:** none.

**Validation:**
- `uv run python -m pytest exploration/concept_analysis/scripts/` → 258 passed, 5 skipped.
- `analyze --help` shows the new flag text.

---

## Final Status

All three phases complete. The cleanup-feedback-flag work item is done:
- The `--feedback` flag is a sixth producer in the iteration loop.
- The concept-28 silent-drift bug is no longer reachable.
- `_apply_external_feedback` is deleted (grep returns only a comment).
- README and `--help` reflect the new single-command contract.

**Suggested follow-up:** `/_my_audit_implementation` to independently verify against spec acceptance criteria before merging.

---

**Status:** Complete

**Next:** `/_my_implement` to execute Phase 1.
