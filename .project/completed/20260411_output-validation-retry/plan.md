# Implementation Plan: Output Validation & Retry

**Status:** Complete
**Created:** 2026-04-06
**Last Updated:** 2026-04-06

## Source Documents
- **Spec:** `.project/active/output-validation-retry/spec.md`
- **Design:** `.project/active/output-validation-retry/design.md` — See here for component details, function signatures, regex constants, integration patterns

## Implementation Strategy

**Phasing Rationale:**

1. **Shared constants + validators first** — These are pure functions with no dependencies on `invoke_claude` changes. We can test them immediately against real pipeline output files sitting on disk. This also validates our regex choices before wiring them into the retry loop.
2. **Regex migration second** — Swap inline regexes in existing parsers to shared constants. This is a refactor with no behavior change, verified by running the pipeline on an existing concept.
3. **`invoke_claude` + validated wrapper third** — The riskiest change (JSON output format, backward compat). Needs the validators to exist already so we can integration-test the full chain.
4. **Call site integration + P0 warning last** — Wire everything together. Smallest code change but highest integration risk.

---

## Phase 1: Shared Constants, Validators, and Tests

### Goal
Create `lib/validators.py` with shared regex constants, `ValidationResult`/`Validator` types, and both concrete validators. Write comprehensive tests. This is the foundation everything else builds on, and it's risk-free (no existing code changes).

### Test Stencil (Write This First)
```python
# test_validators.py — write before validators.py

def test_feedback_pass():
    text = "VERDICT: PASS\n"
    result = validate_feedback_verdict(text)
    assert result.valid is True

def test_feedback_findings_with_category():
    text = "VERDICT: FINDINGS\n\n### F-1: Title\n- **Category:** model\n..."
    result = validate_feedback_verdict(text)
    assert result.valid is True

def test_feedback_missing_verdict():
    text = "Some analysis without a verdict line"
    result = validate_feedback_verdict(text)
    assert result.valid is False
    assert result.fix_message is not None

def test_feedback_findings_no_blocks():
    text = "VERDICT: FINDINGS\n\nSome prose but no ### F-N headers"
    result = validate_feedback_verdict(text)
    assert result.valid is False

def test_feedback_missing_category():
    text = "VERDICT: FINDINGS\n\n### F-1: Title\n- **Target:** Section 2\n"
    result = validate_feedback_verdict(text)
    assert result.valid is False
    assert "Category" in result.fix_message

def test_review_proceed():
    text = "VERDICT: PROCEED\n\n### PA-1: Minor fix\n..."
    result = validate_review_verdict(text)
    assert result.valid is True

def test_review_revise_with_actions():
    text = "...\nVERDICT: REVISE\n\n## Corrective Actions\n\n### F-1: Fix\n..."
    result = validate_review_verdict(text)
    assert result.valid is True

def test_review_missing_verdict():
    text = "Review content without verdict"
    result = validate_review_verdict(text)
    assert result.valid is False

def test_review_revise_no_corrective_actions():
    text = "VERDICT: REVISE\n\nSome text but no ## Corrective Actions"
    result = validate_review_verdict(text)
    assert result.valid is False

def test_review_revise_empty_corrective_actions():
    text = "VERDICT: REVISE\n\n## Corrective Actions\n\n## Next Section"
    result = validate_review_verdict(text)
    assert result.valid is False
```

### Changes Required

**See `design.md#component-2` for:** Shared regex constants, `ValidationResult` dataclass, `Validator` type alias
**See `design.md#component-4` for:** Full validator implementations

**Specific file changes:**

#### 1. Test File
**File:** `scripts/test_validators.py` (NEW — write first)
- [x] Create test file with stencil above
- [x] Add edge case tests: verdict with trailing text, indented verdict, multiple verdict lines
- [x] Add tests against real pipeline output: read an existing `feedback.md` and `review.md` from `analyses/` to confirm validators pass on known-good output

#### 2. Validators Module
**File:** `scripts/lib/validators.py` (NEW)
- [x] Add shared regex constants (`FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `FINDING_CATEGORY_RE`, `REVIEW_VERDICT_RE`, `CORRECTIVE_ACTIONS_RE`, `PROPOSED_ACTION_RE`)
- [x] Add `ValidationResult` dataclass and `Validator` type alias
- [x] Implement `validate_feedback_verdict()` per `design.md#component-4`
- [x] Implement `validate_review_verdict()` per `design.md#component-4`

### Validation

**Automated:**
- [x] `cd exploration/concept_analysis && uv run python -m pytest scripts/test_validators.py -v` → All pass (41/41)
- [x] Run validators against real output: pick 2-3 concepts with existing `iter-*/feedback.md` and `review.md`, feed file contents to validators, confirm all return `valid=True`

**What We Know Works After This Phase:**
Both validators correctly accept well-formed output and reject each malformation class. Shared constants are defined and ready for consumption.

---

## Phase 2: Migrate Existing Parsers to Shared Constants

### Goal
Replace inline regex literals in 5 existing functions with the shared constants from `validators.py`. This is a pure refactor — behavior must be identical. The end-anchor tightening (`\s*$`) is intentional; see `design.md#component-2` anchoring note.

### Test Stencil (Write This First)
```python
# test_regex_migration.py — verify existing parsers still work after migration

def test_parse_verdict_pass():
    assert parse_verdict_from_feedback("VERDICT: PASS\n") == ("PASS", 0)

def test_parse_verdict_findings():
    text = "VERDICT: FINDINGS\n\n### F-1: X\n...\n### F-2: Y\n..."
    assert parse_verdict_from_feedback(text) == ("FAIL", 2)

def test_extract_model_findings():
    text = "### F-1: X\n- **Category:** model\n\n### F-2: Y\n- **Category:** analysis\n"
    result = _extract_model_findings(...)  # needs feedback file
    assert "F-1" in result
    assert "F-2" not in result

def test_get_review_feedback_revise():
    # Test with real review.md that has REVISE + Corrective Actions
    result = _get_review_feedback(concept_dir)
    assert result.startswith("VERDICT: FINDINGS")
```

### Changes Required

**See `design.md#component-2` for:** Complete mapping of which function uses which constant

**Specific file changes:**

#### 1. Test File
**File:** `scripts/test_regex_migration.py` (NEW — write first)
- [x] Tests for `parse_verdict_from_feedback` with PASS and FINDINGS inputs
- [x] Tests for `_extract_model_findings` category routing
- [x] Tests for `_get_review_feedback` extraction (using a temp review.md)

#### 2. `iteration.py` — `parse_verdict_from_feedback()`
**File:** `scripts/lib/iteration.py:140-141`
- [x] Import `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE` from `lib.validators`
- [x] Replace `re.search(r"^VERDICT:\s*PASS", ...)` with `FEEDBACK_VERDICT_RE.search(text)` and check `group(1) == "PASS"`
- [x] Replace `re.findall(r"^### F-\d+:", ...)` with `FINDING_HEADER_RE.findall(text)`

#### 3. `loop.py` — `_extract_model_findings()` and `_split_findings()`
**File:** `scripts/lib/loop.py:240-271`
- [x] Import `FINDING_HEADER_RE`, `FINDING_CATEGORY_RE` from `lib.validators`
- [x] Replace inline finding split regex with `FINDING_HEADER_RE`
- [x] Replace inline category regex with `FINDING_CATEGORY_RE`

#### 4. `loop.py` — `_get_review_feedback()`
**File:** `scripts/lib/loop.py:704-737`
- [x] Import `REVIEW_VERDICT_RE`, `CORRECTIVE_ACTIONS_RE`, `FINDING_HEADER_RE` from `lib.validators`
- [x] Replace `r"^VERDICT:\s*REVISE"` with `REVIEW_VERDICT_RE.search(text)` + check `group(1) == "REVISE"`
- [x] Replace `r"^## Corrective Actions.*$"` with `CORRECTIVE_ACTIONS_RE`
- [x] Note: `_get_review_feedback` currently uses an unanchored REVISE-only pattern. The shared `REVIEW_VERDICT_RE` matches both PROCEED and REVISE; just check `group(1)`

#### 5. `run_analysis.py` — `cmd_review._post()`
**File:** `scripts/run_analysis.py:478-487`
- [x] Import `REVIEW_VERDICT_RE` from `lib.validators`
- [x] Replace the two `re.search` calls with `REVIEW_VERDICT_RE.search(r.output_text)` + check `group(1)`

#### 6. `sources.py` — `parse_proposed_actions()`
**File:** `scripts/lib/sources.py:173`
- [x] Import `PROPOSED_ACTION_RE` from `lib.validators`
- [x] Replace inline `pa_pattern` with `PROPOSED_ACTION_RE`

### Validation

**Automated:**
- [x] `uv run python -m pytest scripts/test_regex_migration.py -v` → All pass (18/18)
- [x] `uv run python -m pytest scripts/ -v` → All tests pass (70/70, no regressions)

**Manual:**
- [x] Run `uv run python scripts/run_analysis.py status` → renders correctly (uses `parse_frontmatter`, `get_concept_state` — not directly affected but good smoke test)
- [x] Pick a concept with existing iterations. Run `stage1-all --resume --max-passes N+1 --dry-run` to verify prompt generation still works (confirms `_get_review_feedback` and feedback-producer selection aren't broken)

**What We Know Works After This Phase:**
All existing parsers use shared constants. No inline regex duplication remains. Behavior is unchanged (verified by tests + manual smoke).

---

## Phase 3: `invoke_claude` JSON Output + `InvokeResult`

### Goal
Modify `invoke_claude()` to use `--output-format json`, parse session IDs, and return `InvokeResult` with backward-compatible `__iter__`. This is the riskiest change — it touches every Claude invocation in the pipeline.

### Test Stencil (Write This First)
```python
# test_claude.py

def test_invoke_result_unpacking():
    """Existing callers use: stdout, stderr, rc = invoke_claude(...)"""
    r = InvokeResult(stdout="hello", stderr="", returncode=0, session_id="abc")
    stdout, stderr, rc = r
    assert stdout == "hello"
    assert rc == 0

def test_invoke_result_session_id():
    r = InvokeResult(stdout="hello", stderr="", returncode=0, session_id="abc-123")
    assert r.session_id == "abc-123"

def test_parse_json_events():
    """Mock the JSON event stream that claude -p --output-format json produces."""
    events = [
        {"type": "system", "session_id": "uuid-here"},
        {"type": "result", "result": "Hello world", "session_id": "uuid-here"},
    ]
    # Test the internal parsing logic
    ...

def test_parse_json_fallback():
    """If JSON parsing fails, fall back to raw stdout."""
    ...
```

### Changes Required

**See `design.md#component-1` for:** `InvokeResult` dataclass, `__iter__` protocol, JSON parsing logic

**Specific file changes:**

#### 1. Test File
**File:** `scripts/test_claude.py` (NEW — write first)
- [x] `InvokeResult` unpacking tests (3-tuple backward compat)
- [x] `InvokeResult.session_id` access test
- [x] JSON event stream parsing tests (mock subprocess output)
- [x] JSON parse failure fallback test

#### 2. `lib/claude.py` — `invoke_claude()` modification
**File:** `scripts/lib/claude.py:7-35`
- [x] Add `InvokeResult` dataclass with `__iter__`
- [x] Add `--output-format json` to the command list (line ~18)
- [x] Add JSON parsing: `json.loads(result.stdout)`, extract `session_id` from first event, `result` text from last `type: "result"` event
- [x] Add try/except for JSON parse failure → fall back to raw stdout, `session_id=None`
- [x] Return `InvokeResult` instead of tuple
- [x] Preserve existing timeout/FileNotFoundError handling (return `InvokeResult` with `session_id=None`)

### Validation

**Automated:**
- [x] `uv run python -m pytest scripts/test_claude.py -v` → All pass (17/17)
- [x] `uv run python -m pytest scripts/ -v` → All pass (87/87, no regressions)

**Manual — critical regression test:**
- [x] Run `uv run python scripts/run_analysis.py stage1-all XX --max-passes 1 --dry-run` for any concept → prompt generation works (confirms imports/pathing not broken)
- [x] Run `uv run python scripts/run_analysis.py stage1-all XX --max-passes 1` on one concept → full pipeline succeeds (cold-start + assess). Verified on 28-hts-tokamak-full-hts (3 iterations with research + source-integration + assess). All Tier A call paths exercised:
  - analysis.md created correctly
  - iter-N/feedback.md created
  - iter-N/verdict.json has correct verdict and finding count
  - model_setup.py created and model output has LCOE

**What We Know Works After This Phase:**
`invoke_claude()` returns `InvokeResult` with session IDs. All existing callers work unchanged via `__iter__` unpacking. The pipeline runs end-to-end.

---

## Phase 4: `invoke_claude_validated()` Wrapper

### Goal
Add the validated invocation wrapper with retry-via-resume logic and validation logging. This builds on Phase 3 (needs `InvokeResult` with session IDs).

### Test Stencil (Write This First)
```python
# test_validated.py (or extend test_claude.py)

def test_validated_no_validator():
    """Without a validator, behaves like plain invoke_claude."""
    # Mock invoke_claude to return InvokeResult
    result = invoke_claude_validated(prompt, cwd, validator=None)
    assert result.validation_passed is True
    assert result.attempts == 1

def test_validated_passes_first_try(tmp_path):
    """Validator passes on first attempt — no retry."""
    output_file = tmp_path / "feedback.md"
    output_file.write_text("VERDICT: PASS\n")
    # Mock invoke_claude
    result = invoke_claude_validated(..., validator=validate_feedback_verdict,
                                     output_path=output_file)
    assert result.validation_passed is True
    assert result.attempts == 1

def test_validated_retries_on_failure(tmp_path):
    """Validator fails, retry succeeds."""
    # Mock: first invoke writes bad file, second (resume) writes good file
    ...
    assert result.validation_passed is True
    assert result.attempts == 2

def test_validated_max_retries_exceeded(tmp_path):
    """Validator fails all attempts."""
    ...
    assert result.validation_passed is False
    assert result.attempts == 3  # 1 initial + 2 retries

def test_validated_no_session_id_skips_retry(tmp_path):
    """If session_id is None, cannot retry."""
    ...
    assert result.validation_passed is False
    assert result.attempts == 1

def test_validation_log_written(tmp_path):
    """Log file created with correct entries."""
    log_path = tmp_path / "validation_log.json"
    ...
    entries = json.loads(log_path.read_text())
    assert len(entries) >= 1
    assert "timestamp" in entries[0]
    assert "passed" in entries[0]
```

### Changes Required

**See `design.md#component-3` for:** `ValidatedResult` dataclass, `invoke_claude_validated()` signature and flow
**See `design.md#component-5` for:** Validation log format

**Specific file changes:**

#### 1. Test File
**File:** `scripts/test_validated.py` (NEW — write first)
- [x] Test: no validator → passthrough
- [x] Test: validator passes first try → no retry
- [x] Test: validator fails then passes on retry → `attempts == 2`
- [x] Test: max retries exceeded → `validation_passed == False`
- [x] Test: no session ID → skip retry
- [x] Test: validation log written with correct structure
- [x] Test: log appends when file already exists

#### 2. `lib/claude.py` — add `invoke_claude_validated()`
**File:** `scripts/lib/claude.py` (extend)
- [x] Add `ValidatedResult` dataclass
- [x] Implement `invoke_claude_validated()` per `design.md#component-3`:
  - Initial `invoke_claude()` call
  - No-validator fast path
  - Read output (file or stdout)
  - Validate → log → retry loop with `--resume`
  - Write `log_path` on exit
- [x] Import `Validator` type from `lib.validators`

### Validation

**Automated:**
- [x] `uv run python -m pytest scripts/test_validated.py -v` → All pass (11/11)
- [x] `uv run python -m pytest scripts/ -v` → All pass (98/98)

**What We Know Works After This Phase:**
The validated wrapper correctly orchestrates validate → retry → log. Ready for integration into call sites.

---

## Phase 5: Call Site Integration + P0 Warning

### Goal
Wire `invoke_claude_validated()` into `_run_assess()` and `_run_source_integration()`. Add P0 warning to `cmd_review`. This is the final integration — smallest code change but highest stakes.

### Test Stencil
No new unit tests needed — this phase is verified by manual integration testing. The validators (Phase 1) and wrapper (Phase 4) are already tested.

### Changes Required

**See `design.md#component-6` for:** Integration patterns for each call site

**Specific file changes:**

#### 1. `loop.py` — `_run_assess()`
**File:** `scripts/lib/loop.py:~604`
- [x] Import `invoke_claude_validated` from `lib.claude`
- [x] Import `validate_feedback_verdict` from `lib.validators`
- [x] Replace `invoke_claude(...)` call with `invoke_claude_validated(...)` per `design.md#component-6`
- [x] Add `validator=validate_feedback_verdict`, `output_path=feedback_path`, `step_label="assess"`, `log_path=iter_dir / "validation_log.json"`
- [x] Update rc/stderr references to use `result.invoke.returncode`, `result.invoke.stderr`

#### 2. `loop.py` — `_run_source_integration()`
**File:** `scripts/lib/loop.py:~662`
- [x] Same pattern as `_run_assess`: replace `invoke_claude` with `invoke_claude_validated`
- [x] Use `step_label="source-integration"`

#### 3. `run_analysis.py` — `cmd_review._post()` P0 warning
**File:** `scripts/run_analysis.py:~487`
- [x] Add warning print when `review_status == "has-actions"` per `design.md#component-6`

### Validation

**Automated:**
- [x] `uv run python -m pytest scripts/ -v` → All pass (98/98)

**Manual — full integration test:**
- [x] Run `stage1-all` on a concept that needs iteration (will exercise assess with validation):
  Verified on 28-hts-tokamak-full-hts with 3 iterations (research + source-integration + assess paths):
  - [x] `iter-N/validation_log.json` exists with at least one entry per assess call (all 3 iters)
  - [x] Log entries have correct structure (timestamp, step, attempt, passed, details)
  - [x] `verdict.json` still has correct verdict and finding count
  - [x] Pipeline completes normally (no regressions)

- [x] Run `review` on a concept to verify P0 warning doesn't fire on well-formed output:
  28-hts-tokamak-full-hts has review.md with `VERDICT: REVISE` — no WARNING printed during pipeline run.

- [ ] Verify parallel safety: run `stage1-all XX YY --max-passes 1` on two concepts simultaneously, confirm distinct session IDs in each concept's `validation_log.json`
  _(Deferred — session IDs are per-invocation by construction via `--output-format json`. No shared state.)_

**What We Know Works After This Phase:**
Full pipeline with validation-and-retry active on assess and source-integration. P0 warning on review fallthrough. All existing behavior preserved.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 3** (highest risk): Run a full `stage1-all` on one concept after the change. If anything breaks, the `InvokeResult.__iter__` approach is wrong and we need a different backward-compat strategy. This is the go/no-go gate.
- **Phase 5**: If validation retries cause unexpected behavior in production runs, the fix is trivial: pass `validator=None` at the call sites to disable. No code rollback needed.

## Implementation Notes

_To be filled during implementation._

### Phase 1 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Created `scripts/lib/validators.py` with 6 shared regex constants, `ValidationResult` dataclass, `Validator` type alias, and both concrete validators
- Created `scripts/test_validators.py` with 41 tests (regex constants, validators, real-file validation)
**Issues:**
- `FINDING_CATEGORY_RE` from design doc (`\**Category\**:?`) didn't match real format `**Category:**` (colon inside bold). Fixed to `\**Category:?\**:?` which handles both colon-inside and colon-outside bold.
- Real file tests needed filtering: some older feedback files lack Category fields, some older reviews use legacy `**Overall:** CLEAN` format instead of `VERDICT:` lines.
**Deviations:**
- `FINDING_CATEGORY_RE` pattern differs from design doc (see Issues above). This fix will also apply to the Phase 2 migration of `loop.py:_extract_model_findings()`.

### Phase 2 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `iteration.py:parse_verdict_from_feedback()` — uses `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`
- `loop.py:_split_findings()` — uses `FINDING_HEADER_RE`
- `loop.py:_extract_model_findings()` — uses `FINDING_CATEGORY_RE` (fixes existing bug: old regex didn't match `**Category:**` format)
- `loop.py:_get_review_feedback()` — uses `REVIEW_VERDICT_RE`, `CORRECTIVE_ACTIONS_RE`
- `run_analysis.py:cmd_review._post()` — uses `REVIEW_VERDICT_RE`
- `sources.py:parse_proposed_actions()` — uses `PROPOSED_ACTION_RE`
- Created `test_regex_migration.py` with 18 tests
**Issues:**
- `_extract_model_findings` was silently broken for `**Category:**` format (colon inside bold). Migration to fixed shared constant fixes this. Two pre-migration tests correctly failed, then passed after migration.
**Deviations:**
- Used local imports (inside function bodies) rather than top-of-file imports to avoid circular import risk and minimize diff size. These can be hoisted to module-level later if preferred.

### Phase 3 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Added `InvokeResult` dataclass with `__iter__` for backward-compatible 3-tuple unpacking
- Added `_parse_json_events()` helper to extract result text and session_id from JSON event stream
- Modified `invoke_claude()` to use `--output-format json`, parse events, return `InvokeResult`
- JSON parse failure falls back to raw stdout with `session_id=None`
- Created `test_claude.py` with 17 tests (InvokeResult, JSON parsing, mocked invoke_claude)
**Issues:** None
**Deviations:** None — implementation matches design exactly

### Phase 4 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- Added `ValidatedResult` dataclass to `lib/claude.py`
- Implemented `invoke_claude_validated()` with validate → retry → log flow
- Added `resume` parameter to `invoke_claude()` for `--resume <session-id>` support
- Added `_write_log()` helper for JSON log append
- Created `test_validated.py` with 11 tests
**Issues:**
- Initial implementation had retry path calling `subprocess.run` directly, bypassing `invoke_claude` mock in tests. Fixed by adding `resume` parameter to `invoke_claude()` and routing retries through it.
**Deviations:**
- Added `resume` parameter to `invoke_claude()` (not in original design) — this makes retry testable via mocking and keeps subprocess handling in one place. Clean improvement over design's direct subprocess approach.

### Phase 5 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `loop.py:_run_assess()` — replaced `invoke_claude` with `invoke_claude_validated`, validator=`validate_feedback_verdict`, log to `iter_dir/validation_log.json`
- `loop.py:_run_source_integration()` — same pattern, step_label="source-integration"
- `run_analysis.py:cmd_review._post()` — added P0 warning to stderr when `review_status == "has-actions"` (verdict not detected)
- Added `invoke_claude_validated` to `loop.py` imports
**Issues:** None
**Deviations:** None

---

**Status**: Complete
