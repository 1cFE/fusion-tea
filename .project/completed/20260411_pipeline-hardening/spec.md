# Spec: Pipeline Hardening

**Status:** Complete (all 7 phases landed; `/_my_audit_implementation` passed clean on 2026-04-11)
**Owner:** Reid W
**Created:** 2026-04-08 22:09 PDT
**Complexity:** HIGH
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The concept analysis pipeline (`exploration/concept_analysis/scripts/`) silently corrupts output files, loses feedback, and dies on transient API errors. Observed failures: H-01 killed all retries on concept 01 iter-10, H-17 killed concepts 15 and 17a in a batch run. Every `stage1-all --all` run requires manual re-runs and inspection.

### Success Criteria

- [x] Batch runs survive transient API errors (rate limits, network timeouts) without losing concepts (FR-2, `_TRANSIENT_DELAYS = [30, 60]`)
- [x] No pipeline path silently writes wrong data (parsed event text, conversational messages) to output files (FR-14, `file_with_fallback` deleted)
- [x] When something fails, the error message identifies the failure mode and includes actionable context (FR-5, `_augment_fix_message` + validator details)
- [x] All Claude invocation sites validate output format, not just return code (FR-13, all call sites migrated)
- [x] Validation retry fix messages include the output file path and attempt context (FR-5, FR-6)

### Priority

P0 — blocking reliable pipeline operation.

---

## Problem Statement

### Current State

The pipeline trusts Claude's return code as proof of success. When `rc == 0`, every code path assumes the expected output was produced correctly. In reality, `rc == 0` means "the Claude CLI process exited cleanly" — it says nothing about whether Claude followed the prompt's instructions.

`invoke_claude_validated` was added to address this but is only used in 2 of ~10 Claude invocation sites. The other sites use raw `invoke_claude` or `run_claude_step` with no output validation. Additionally, `invoke_claude_validated` itself has a critical bug (H-01) where it falls back to validating parsed event text when the expected file doesn't exist.

### Desired Outcome

Every Claude call site uses validated invocation. `run_claude_step` is replaced — its output-mode enum (`file_with_fallback`, `stdout_to_file`, etc.) becomes unnecessary because validators + the H-01 fix handle file-existence checking uniformly. Transient failures retry with backoff instead of killing the concept.

---

## Scope

### In Scope

- Fix `invoke_claude_validated` foundation (H-01)
- Add transient retry with exponential backoff (H-17)
- Enrich validator context: output path, attempt number, validated text preview (H-12, H-12a, H-13, H-14)
- Replace `run_claude_step` — migrate all callers to `invoke_claude_validated` directly
- Migrate all 10+ Claude call sites to validated invocation
- Add new validators: `validate_non_empty`, `validate_python_syntax`, `validate_file_modified`
- Fix standalone issues: H-03, H-04, H-05, H-08, H-09, H-10, H-15, H-16, H-18, H-19
- Code smell fixes: S-01 (unused import), S-02 (deduplicate `_extract_iter_count`), S-06/S-07 (`sys.exit` → `raise ValueError`)

### Out of Scope

- H-20: Hand-rolled YAML parser → `yaml.safe_load` (deferred)
- H-21: Review feedback extraction position-dependence (low risk, current templates work)
- S-05: Hardcoded absolute paths in `paths.py` (machine-specific, not urgent)
- New pipeline features, prompt changes, or domain logic changes
- Performance optimization beyond retry/backoff

### Edge Cases & Considerations

- **In-place edit validation**: Sites where Claude edits an existing file (feedback pass, address-review, external feedback) need a different validator pattern — snapshot file hash before invocation, check it changed after. The `validate_file_modified` factory handles this.
- **stdout-mode calls**: `cmd_gap_check` currently uses `stdout_to_file` mode. After replacing `run_claude_step`, this needs to validate stdout text directly (`output_path=None`), then write to file explicitly if valid.
- **`research.py` invocation**: Uses `invoke_claude` with post-hoc filesystem diff to measure success. Low value in adding a validator here — the filesystem diff is the real check. Include `validate_non_empty` for consistency but don't block on it.
- **`sys.exit` migration (S-06/S-07)**: `resolve_source_names` and `resolve_concepts` call `sys.exit(1)`. Changing to `raise ValueError` requires updating every CLI call site that relies on the current exit behavior. Must audit callers.
- **Backward compatibility**: `run_claude_step` callers use `skip_if_exists`, `dry_run`, `post_hook`, and template-filling features. These must be handled inline or in a lighter helper during migration. The `post_hook` pattern in particular (`cmd_review`'s `_post`) needs careful migration.

---

## Requirements

### Functional Requirements

#### Foundation Fixes

1. **FR-1**: (H-01) `invoke_claude_validated` MUST treat file-not-written as a distinct failure mode when `output_path` is provided. When the expected file does not exist after invocation, the retry fix message MUST include the full file path and instruct Claude to write to that path. The validator function MUST NOT run against parsed event text — it only runs when the file exists.

2. **FR-2**: (H-17) `invoke_claude()` MUST retry on transient failures with exponential backoff. Transient failure = subprocess returns rc != 0. Retry schedule: 3 attempts with ~30s / 60s / 120s delays. MUST log each retry attempt to stderr. MUST NOT retry when Claude produces rc=0 (that's a content problem, not a transient error).

3. **FR-3**: (H-04) `invoke_claude()` MUST emit a warning to stderr when JSON event stream parsing fails, before falling back to raw stdout. The warning MUST include the exception type and message.

4. **FR-4**: (H-05) `_parse_json_events` MUST raise `ValueError` (not return empty string) when the event stream contains no `type: "result"` event. Callers handle this via the existing `except (json.JSONDecodeError, ValueError)` block, which now correctly triggers the FR-3 warning.

#### Validator Enrichment

5. **FR-5**: (H-12, H-12a) Validator fix messages MUST include:
   - The output file path (when applicable)
   - What format/content was expected (brief description)
   - A format example or key structural requirement

6. **FR-6**: (H-13) The `Validator` type MUST accept attempt context. The retry loop MUST pass the current attempt number (1-indexed) and total max attempts to the validator. On later attempts, fix messages SHOULD escalate (e.g., "This is attempt 3 of 3 — focus on writing the file to the exact path specified").

7. **FR-7**: (H-14) The validation log MUST include a `validated_text_preview` field — first 500 characters of the text that was validated (or "FILE NOT FOUND" / "EMPTY" as appropriate).

8. **FR-8**: (H-15) `validate_feedback_verdict` details string MUST include the detected verdict type (PASS, FINDINGS, or FAIL) when validation succeeds.

#### New Validators

9. **FR-9**: A `validate_non_empty` validator MUST exist. It rejects empty/whitespace-only output with a fix message instructing Claude to produce the requested content.

10. **FR-10**: A `validate_python_syntax` validator MUST exist. It compiles the text with `compile(text, "<model_setup>", "exec")` and returns the `SyntaxError` details in the fix message on failure.

11. **FR-11**: A `validate_file_modified(original_hash)` factory MUST exist. It returns a validator that computes SHA-256 of the current text and rejects if identical to `original_hash`. Fix message instructs Claude to apply changes using the Edit tool.

#### Call Site Migration

12. **FR-12**: `run_claude_step` (`step_runner.py`) MUST be replaced. All callers MUST be migrated to use `invoke_claude_validated` directly (or a minimal helper for shared concerns like template-filling and dry-run). The output-mode enum (`stdout_to_file`, `file_with_fallback`, `file_exists`, `no_output`) MUST be eliminated.

13. **FR-13**: Every Claude invocation site MUST use `invoke_claude_validated` with an appropriate validator, per this migration table:

    **Sites expecting Claude to write a new file:**

    | Call site | File | Expected output | Validator |
    |-----------|------|----------------|-----------|
    | `_run_cold_start` | `loop.py` | `iter-N/analysis_body.md` | `validate_non_empty` |
    | `_run_model_in_iteration` | `loop.py` | `iter-N/model_setup.py` | `validate_python_syntax` |
    | `cmd_model_setup` | `run_analysis.py` | `model_setup.py` | `validate_python_syntax` |
    | `cmd_gap_check` | `run_analysis.py` | `gap_report.md` | `validate_non_empty` |
    | `cmd_review` | `run_analysis.py` | `review.md` | `validate_review_verdict` |
    | `cmd_synthesize` | `run_analysis.py` | `synthesis_body.md` | `validate_non_empty` |

    **Sites expecting Claude to edit a file in-place:**

    | Call site | File | Edited file | Validator |
    |-----------|------|------------|-----------|
    | `_run_feedback_pass` | `loop.py` | `analysis.md` | `validate_file_modified` |
    | `cmd_address_review` | `run_analysis.py` | `analysis.md` + `model_setup.py` | `validate_file_modified` |
    | `_apply_external_feedback` | `run_analysis.py` | `analysis.md` | `validate_file_modified` |

    **Sites using returned stdout:**

    | Call site | File | Validator |
    |-----------|------|-----------|
    | `cmd_gap_check` (stdout path) | `run_analysis.py` | `validate_non_empty` on stdout, then explicit write |
    | `research.py` | `research.py` | `validate_non_empty` (low priority — filesystem diff is primary check) |

14. **FR-14**: (H-02) After migration, no code path SHALL write parsed event text (Claude's conversational message) to an output file. The `file_with_fallback` pattern is eliminated entirely.

#### State/Data Integrity Fixes

15. **FR-15**: (H-03, covered by FR-11/FR-13) Feedback pass MUST verify that `analysis.md` was actually modified. Covered by `validate_file_modified` in the migration table.

16. **FR-16**: (H-08, covered by FR-11/FR-13) External feedback MUST NOT archive the feedback file unless `analysis.md` was actually modified. Covered by `validate_file_modified` — if validation fails (file unchanged), the caller does not proceed to archive.

17. **FR-17**: (H-09, H-10) `_run_source_integration` and `_run_assess` MUST check `result.validation_passed` before proceeding to parse output. If validation failed (all retries exhausted), treat as failure — do not attempt to parse the output file.

18. **FR-18**: (H-16) `_update_canonical_files` MUST NOT copy `model_setup.py` or `model_output.txt` to the concept root when the current iteration's model failed (`model_ok=False`). Only successful models update canonical files.

19. **FR-19**: (H-19) `.stale` marker files MUST be cleaned up when the corresponding explorer data is regenerated. The staleness propagation code (`state.py`) MUST delete any existing `.stale` marker when writing fresh data.

20. **FR-20**: (H-18) `clear_iterations` with `--force` MUST also clear `research_log.json` from the concept root, or document that it becomes orphaned. Prefer clearing it — orphaned logs with dangling iteration references are worse than no log.

#### Code Smell Fixes

21. **FR-21**: (S-01) Remove unused `_has_downstream_artifacts` import from `run_analysis.py`.

22. **FR-22**: (S-02) Remove duplicate `_extract_iter_count` from `run_analysis.py`. Import from `landscape.py` (or extract to a shared utility if `landscape.py` is the wrong dependency direction).

23. **FR-23**: (S-06, S-07) `resolve_source_names` (`sources.py`) and `resolve_concepts` (`concepts.py`) MUST raise `ValueError` instead of calling `sys.exit(1)`. CLI entry points that call these functions MUST catch `ValueError` and exit with an appropriate error message.

---

## Acceptance Criteria

### Core Functionality

- [x] `invoke_claude_validated` never validates parsed event text — only file content or explicit stdout (file-not-found branch is first check inside retry loop)
- [x] Transient failures (rc != 0) retry with exponential backoff before giving up (`_TRANSIENT_DELAYS = [30, 60]`, 3 total attempts; see Phase 2 completion note for the 3-attempt-vs-4-attempt deviation)
- [x] All 10+ Claude call sites use `invoke_claude_validated` with a validator (Phase 4 + Phase 5 migrations)
- [x] `run_claude_step` (and `StepResult`/`OutputMode`/`_MISSING`) deleted; `step_runner.py` repurposed to `prepare_step` + `StepContext` only
- [x] `validate_non_empty`, `validate_python_syntax`, `validate_file_modified` exist and are tested (58 tests in `test_validators.py`, including CRLF + BOM round-trip cases)
- [x] Fix messages include the output file path and expected format (`_augment_fix_message` helper)
- [x] Validation log entries include `validated_text_preview` (verified live on concept 35)
- [x] No code path writes parsed event text to an output file (verified live on concept 35 — no conversational text found anywhere)

### State Integrity

- [x] Canonical model files only updated on successful model runs (FR-18, `_update_canonical_files(*, model_ok=True)` guard)
- [x] `.stale` markers cleaned up on data regeneration (FR-19, verified in-place in `extract_explorer_data.py:797-801` via in-process regression test — see Phase 6 deviations)
- [x] `--force` clears `research_log.json` (FR-20, `clear_iterations` now `unlink(missing_ok=True)` the log)
- [x] External feedback not archived unless analysis.md actually changed (FR-16, `_apply_external_feedback` checks `validation_passed` before archiving)
- [x] `_run_assess` and `_run_source_integration` check `validation_passed` (FR-17)

### Code Quality

- [x] Unused `_has_downstream_artifacts` import removed from `run_analysis.py` (FR-21)
- [x] `_extract_iter_count` deduplicated — now lives in `landscape.py` as public `extract_iter_count`, imported by `run_analysis.py` (FR-22)
- [x] `resolve_source_names` and `resolve_concepts` raise `ValueError`, not `sys.exit` (FR-23)
- [x] Existing tests continue to pass (193/195; 2 pre-existing out-of-scope failures in `test_claude.py::TestCheckInterface::test_freeform_*` — not touched by pipeline-hardening, documented in Phase 1 completion notes)
- [x] Pipeline runs successfully on at least one concept end-to-end after changes (concept 35, `analyze 35 --max-passes 2`, both iterations `FAIL (3 findings)` with `model_ok=true`; see Phase 7 completion notes in `plan.md`)

---

## Issue Cross-Reference

Every audit issue and its resolution in this spec:

| ID | Description | Resolution | Requirement |
|----|-------------|------------|-------------|
| H-01 | Validator reads stdout when file missing | File-existence as first-class check | FR-1 |
| H-02 | step_runner writes stdout to output file | Eliminate `file_with_fallback` pattern | FR-12, FR-14 |
| H-03 | Feedback pass doesn't verify file modified | `validate_file_modified` | FR-15 |
| H-04 | JSON parse errors swallowed silently | Warn to stderr | FR-3 |
| H-05 | Empty result text returned as empty string | Raise ValueError | FR-4 |
| H-06 | No syntax check on model_setup.py | `validate_python_syntax` | FR-10, FR-13 |
| H-07 | Gap check writes unvalidated stdout | Migrated to validated invocation | FR-13 |
| H-08 | External feedback archived even if not applied | Guard archive on `validate_file_modified` | FR-16 |
| H-09 | Source-integration ignores validation_passed | Check the flag | FR-17 |
| H-10 | Assessment ignores validation_passed | Check the flag | FR-17 |
| H-11 | Review has no format validation | Wire up `validate_review_verdict` | FR-13 |
| H-12 | Fix messages have no context | Include path, format, example | FR-5 |
| H-12a | Fix message drops output file path | Include path | FR-5 |
| H-13 | No attempt escalation in retry loop | Pass attempt context to validators | FR-6 |
| H-14 | Validation log missing validated text | Add `validated_text_preview` | FR-7 |
| H-15 | Validator details don't distinguish verdict type | Include verdict in details | FR-8 |
| H-16 | Canonical files overwrite with worse model | Guard on `model_ok` | FR-18 |
| H-17 | No transient retry in invoke_claude() | Exponential backoff | FR-2 |
| H-18 | research_log orphaned after --force | Clear log too | FR-20 |
| H-19 | .stale markers never cleaned up | Clean on regeneration | FR-19 |
| H-20 | Hand-rolled YAML parser | **Deferred** | — |
| H-21 | Review feedback extraction position | **Deferred** | — |
| S-01 | Unused import | Delete | FR-21 |
| S-02 | Duplicated function | Deduplicate | FR-22 |
| S-03 | Inconsistent invoke_claude usage | Resolved by unification | FR-13 |
| S-04 | Confusing _MISSING sentinel | Resolved by replacing run_claude_step | FR-12 |
| S-05 | Hardcoded paths | **Deferred** | — |
| S-06 | sys.exit in library code (sources.py) | Raise ValueError | FR-23 |
| S-07 | sys.exit in library code (concepts.py) | Raise ValueError | FR-23 |

---

## Related Artifacts

- **Research:** `.project/research/20260408-pipeline-holes-comprehensive-audit.md`
- **Prior research:** `.project/research/20260408-validation-retry-failure-analysis.md`
- **Design:** `.project/active/pipeline-hardening/design.md` (to be created)
- **Related active work:** `.project/active/output-validation-retry/` (earlier attempt at H-01 fix — superseded by this spec)
- **Related active work:** `.project/active/step-runner-validation-retry/` (earlier attempt — superseded by this spec)

---

**Next Steps:** After approval, proceed to `/_my_design`
