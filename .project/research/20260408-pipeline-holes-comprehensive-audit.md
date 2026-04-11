---
date: 2026-04-08T15:00:00-07:00
researcher: Claude
topic: "Comprehensive pipeline holes, unhandled errors, and code quality audit"
tags: [research, pipeline, concept-analysis, code-quality, error-handling]
status: complete
last_updated: 2026-04-08
---

# Research: Every Hole in the Concept Analysis Pipeline

**Date**: 2026-04-08
**Research Type**: Code Quality / Error Handling Audit
**Trigger**: Prior research (20260408-validation-retry-failure-analysis.md) exposed systemic issues; user requested full trace of ALL holes.

## Research Question

Where are all the logic holes, unhandled errors, silent failures, and general slop in the concept analysis pipeline (`exploration/concept_analysis/scripts/`)?

## Summary

The pipeline has **22 distinct issues** across 10 files, clustered into 6 categories:

1. **Silent fallback to wrong data** (5 issues) — the most dangerous class. Code silently reads parsed event text instead of expected files, or falls back to empty strings when data is missing.
2. **Fire-and-forget Claude calls** (6 issues) — Claude is invoked, output checked only for rc==0, with no verification that the expected file was actually written or contains valid content.
3. **Validator blindness** (5 issues) — validators have no awareness of what they're validating, can't distinguish failure modes, and send useless fix messages with no file paths.
4. **No transient retry** (1 issue) — `invoke_claude()` gives up immediately on subprocess failure with no backoff/retry, killing entire pipeline runs on rate limits or transient errors.
5. **State/data integrity gaps** (3 issues) — lost data and inconsistent state that can't be detected after the fact.
6. **Fragile parsing** (2 issues) — regex-based parsing that breaks on edge cases.

---

## Category 1: Silent Fallback to Wrong Data

### H-01: Validator reads stdout when file doesn't exist (KNOWN — RC-1)

**File**: `claude.py:157-160`
**Severity**: Critical

```python
if output_path is not None and output_path.exists():
    text = output_path.read_text(encoding="utf-8")
else:
    text = result.stdout  # ← WRONG DATA
```

When Claude fails to write the expected file, the validator pattern-matches against `result.stdout` — which is NOT raw subprocess stdout. `_parse_json_events` extracts the `"result"` field from Claude's JSON event stream, which is Claude's final conversational message (e.g., "I've written the assessment to feedback.md"). The validator sees this conversational text, not the actual feedback content. It will never match the expected format. Every retry then fails identically because the fix message describes a format problem when the real problem is a missing file.

**Impact**: 100% retry failure rate for the "file not written" case. Observed in concept 01 iter-10.

### H-02: `step_runner.py` file_with_fallback writes stdout as if it were the expected output

**File**: `step_runner.py:120-125`
**Severity**: High

```python
elif output_mode == "file_with_fallback":
    if output_path.exists():
        output_text = output_path.read_text(encoding="utf-8")
    elif stdout.strip():
        output_path.write_text(stdout, encoding="utf-8")  # ← WRITES WRONG DATA TO DISK
        output_text = stdout
```

When Claude doesn't write the expected file but does produce stdout, the runner writes Claude's conversational text to the output path. This means `review.md` or `gap_report.md` could contain Claude's reasoning/explanation instead of the structured output. Downstream consumers (frontmatter parsing, verdict detection) then parse garbage.

**Impact**: Corrupted output files that look like they succeeded. The `_post` hook in `cmd_review` (run_analysis.py:536-560) then tries to detect `VERDICT: PROCEED/REVISE` in what might be conversational text, and falls through to the `"has-actions"` default — which is wrong but not an error, so it silently proceeds.

### H-03: `_run_feedback_pass` doesn't verify analysis.md was actually updated

**File**: `loop.py:381-430`
**Severity**: High

After a feedback pass, the function only checks `rc != 0`. It does NOT check:
- Whether `analysis.md` was actually modified (Claude edits it in-place via Edit tool)
- Whether the content changed at all
- Whether the frontmatter is still valid

The cold-start path (`_run_cold_start`, loop.py:319-378) does check for `body_path.exists()`, but feedback pass has no equivalent check. If Claude returns rc=0 but doesn't actually edit analysis.md, the pipeline treats the iteration as successful.

**Impact**: Silent no-op iterations that consume API credits and increment iteration counts without making progress.

### H-04: `invoke_claude` swallows JSON parse errors silently

**File**: `claude.py:106-111`
**Severity**: Medium

```python
try:
    text, session_id = _parse_json_events(result.stdout)
except (json.JSONDecodeError, ValueError):
    text = result.stdout  # Fall back to raw stdout
    session_id = None
```

If the JSON event stream is malformed (partial write, Claude crash mid-output), the raw unparsed stdout becomes the "result text". This includes JSON brackets, event metadata, and other non-content. Downstream code then validates or writes this garbage. No warning is emitted.

**Impact**: Garbage-in at the foundation layer. Every downstream consumer (validators, file writers, verdict parsers) gets corrupted input with no indication that parsing failed.

### H-05: `_parse_json_events` returns empty string if no result event exists

**File**: `claude.py:36-58`
**Severity**: Medium

If the JSON event stream parses correctly but contains no event with `type: "result"`, `result_text` stays `""`. The caller gets an empty string with no error. This can happen if Claude crashes or if the CLI format changes.

**Impact**: Empty output treated as valid. In `step_runner.py:123`, empty stdout makes it fall through to the failure branch (good). But in `invoke_claude_validated`, the empty string gets passed to the validator, which fails with a confusing "No VERDICT line found" message rather than "output was empty".

---

## Category 2: Fire-and-Forget Claude Calls

### H-06: `_run_model_in_iteration` — no check that Claude wrote model_setup.py with valid Python

**File**: `loop.py:453-515`
**Severity**: Medium

After invoking Claude for model-setup, the code checks `model_script.exists()` (line 499). But it does NOT check:
- Whether the file is valid Python (syntax check)
- Whether it's non-empty
- Whether it contains the required interface (`result = ...` or `params = ...` / `results = ...`)

The `_check_interface` function in `claude.py:268-302` runs AFTER `run_model` succeeds, so interface warnings only appear for models that actually run. A syntax error in model_setup.py causes `run_model` to fail with a generic "model failed" message, and the pipeline continues with `model_ok=False`.

**Impact**: Model failures are non-fatal (by design, FR-7), so this is by-design acceptable. But the error message is unhelpful — you get `model failed (rc=1)` with a snippet of Python traceback, not "model_setup.py has a syntax error on line 42".

### H-07: `cmd_gap_check` uses `stdout_to_file` mode — writes whatever Claude says

**File**: `run_analysis.py:223-234`
**Severity**: Low-Medium

Gap check uses `output_mode="stdout_to_file"`, which writes Claude's parsed stdout directly to `gap_report.md`. There's no validation that the output is actually a gap report (has expected sections, reasonable length, etc.). If Claude produces a partial response or an error message, that becomes the gap report.

**Impact**: Garbage gap reports that look like they succeeded. Low severity because gap reports are informational, not consumed by downstream pipeline stages.

### H-08: `_apply_external_feedback` — no verification that analysis was actually changed

**File**: `run_analysis.py:363-423`
**Severity**: Medium

After applying external feedback, the function checks `rc != 0` and then:
- Propagates staleness
- Archives the feedback file (`feedback.rename(archived)`)

But it never checks whether analysis.md was actually modified. If Claude returns rc=0 but doesn't edit anything, the feedback file gets archived (destroyed) and staleness propagated for no reason.

**Impact**: Feedback file is lost even when it wasn't applied. User has to recreate the feedback.

### H-09: `_run_source_integration` — validation passes but file might be empty

**File**: `loop.py:644-705`
**Severity**: Medium

After `invoke_claude_validated`, the function checks `result.invoke.returncode != 0` and `output_path.exists()`. But the validated result might have `validation_passed=False` and this is NOT checked. The function reads `feedback_text` from the file regardless:

```python
if result.invoke.returncode != 0:
    print(f" FAILED ...")
    return None

if not output_path.exists():
    print(f" FAILED ...")
    return None

feedback_text = output_path.read_text(encoding="utf-8")  # ← might be invalid
verdict, finding_count = parse_verdict_from_feedback(feedback_text)
```

If validation failed (all retries exhausted), the file might not exist (H-01 scenario) — caught by the exists() check. But if the file exists with wrong content (wrote something but not the right format), the code proceeds to parse it anyway.

**Impact**: Malformed feedback from source-integration gets parsed with `parse_verdict_from_feedback`, which returns `("FAIL", 0)` for any text that doesn't match the VERDICT pattern. This means source-integration with bad output returns a `FAIL` verdict with 0 findings — confusing but not pipeline-breaking since the caller checks for `verdict == "PASS"`.

### H-10: `_run_assess` — same validation_passed gap as H-09

**File**: `loop.py:575-641`
**Severity**: Medium

Same pattern. After `invoke_claude_validated`, the code checks rc and file existence but doesn't check `result.validation_passed`. If validation exhausted all retries, the code reads `feedback_path` anyway and parses whatever is there.

**Impact**: Assessment with wrong format gets parsed. The resulting verdict/finding_count drives the loop's continue/stop logic. Wrong finding_count means the pipeline might stop early (0 findings → "PASS"-like behavior) or continue pointlessly.

### H-11: `cmd_review` doesn't use validated invocation

**File**: `run_analysis.py:562-574`
**Severity**: Medium

The review step uses `run_claude_step` (not `invoke_claude_validated`), so review output has NO format validation. The `_post` hook (run_analysis.py:536-560) does a best-effort verdict detection:

```python
verdict_match = REVIEW_VERDICT_RE.search(r.output_text)
if verdict_match and verdict_match.group(1) == "PROCEED":
    review_status = "proceed"
elif verdict_match and verdict_match.group(1) == "REVISE":
    review_status = "revise"
else:
    # Legacy fallback
    ...
    review_status = "has-actions"
```

If the review output is conversational text (H-02 scenario), this silently defaults to "has-actions" and writes that to frontmatter. The next stage (`cmd_address_review`) then skips the concept because "has-actions" is not "revise".

**Impact**: Reviews that should trigger REVISE → re-analysis flow get stuck in "has-actions" limbo. The user has to manually inspect and re-run.

---

## Category 3: Validator Blindness

### H-12: Fix messages are static — no context about what failed (KNOWN — RC-2)

**File**: `validators.py:63-69`, `validators.py:126-131`
**Severity**: Critical

Fix messages don't include:
- Whether the file was written or not
- What text was actually validated
- The format example

This was thoroughly documented in the prior research report. Adding here for completeness.

### H-12a: Fix message drops the output file path

**File**: `validators.py:64-69`
**Severity**: High (one-line fix, high impact)

The assess prompt includes `feedback_path` (the full path to write to). But the fix message says "re-write the feedback file" without restating WHERE. Claude's `--resume` context may not retain the path from the original prompt. This is a distinct issue from H-12's general "no context" problem — it's specifically that the one piece of information Claude most needs (the file path) is dropped.

The same pattern exists in `validate_review_verdict` (line 126-131): "re-write the review file" with no path.

**Fix**: The validator needs access to the output path. Either pass it as a parameter or use a factory function that closes over it.

### H-13: Validators have no attempt awareness (KNOWN — RC-3)

**File**: `validators.py:45`, `claude.py:155-203`
**Severity**: High

The `Validator` type alias is `Callable[[str], ValidationResult]` — it takes only the text to validate. The retry loop passes the same validator on every attempt with no way to escalate the fix message or add diagnostic context.

### H-14: Validation log doesn't capture the validated text (KNOWN — RC-4)

**File**: `claude.py:164-174`
**Severity**: Medium

The log entry records `validator`, `passed`, `details`, and `fix_message_sent` — but NOT the actual text that was validated. Post-mortem debugging requires guessing what the validator saw.

### H-15: `validate_feedback_verdict` doesn't distinguish VERDICT types in details

**File**: `validators.py:52-110`
**Severity**: Low

When validation passes, the details string is always "Feedback format valid" regardless of whether the verdict was PASS or FINDINGS. For logging/debugging, it would help to know which.

---

## Category 4: No Transient Retry

### H-17: `invoke_claude()` has no transient retry / backoff

**File**: `claude.py:61-112`
**Severity**: Critical

`invoke_claude()` runs `subprocess.run(["claude", "-p", ...])` exactly once. If the Claude CLI returns a non-zero exit code — rate limiting, network timeout, transient API error — the caller gets `rc != 0` and gives up. There is no retry, no backoff, no distinction between transient and permanent failures.

This blocks ALL pipeline steps, not just validated ones. Observed in today's run: concepts 15 and 17a both died with `rc=1` and empty stderr (likely rate limiting). The pipeline printed `FAILED (rc=1)` and moved on, wasting all prior iteration work for those concepts.

```python
result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, ...)
# rc=1 → caller prints FAILED → concept abandoned. No retry.
```

Every call site inherits this behavior: cold-start, feedback-pass, model-setup, assess, source-integration, research, review, synthesis, address-review, gap-check.

**Impact**: A single transient API hiccup kills an entire concept's pipeline run. With multi-concept batch runs (`stage1-all --all`), one rate-limit burst can fail half the concepts. The user has to manually re-run with `--resume`, concept by concept.

**Fix**: Add exponential backoff retry in `invoke_claude()` for transient failures (rc=1 with empty or rate-limit-indicating stderr). 2-3 retries with 30s/60s/120s delays would handle most cases.

---

## Category 5: State/Data Integrity Gaps

### H-16: `_update_canonical_files` silently overwrites concept-root model files

**File**: `loop.py:762-774`
**Severity**: Medium

Each iteration copies `model_setup.py` and `model_output.txt` from `iter-N/` to the concept root. If iteration N's model is worse than N-1's (e.g., syntax error), the concept root's "canonical" model gets overwritten with the broken one. There's no comparison or rollback.

**Impact**: The concept's canonical model can regress between iterations. Downstream consumers (`cmd_synthesize`, concept explorer) pick up the broken model.

### H-18: `clear_iterations` with `--force` doesn't preserve research_log.json

**File**: `iteration.py:157-164`, `loop.py:71-75`

When `--force` clears all `iter-*/` directories, the research log at `{concept_dir}/research_log.json` survives (it's in the concept root, not in iter dirs). But all the actual research artifacts (research_output.json, research_prompt.md) in the iter dirs are destroyed. The research log then references iteration numbers that no longer exist.

**Impact**: Research log becomes orphaned — it says "iteration 3 acquired source X" but iter-3/ no longer exists. Not a runtime error, but confusing for debugging.

### H-19: `.stale` marker files never cleaned up

**File**: `state.py:93-101`

```python
stale_marker = explorer_json.with_suffix(".json.stale")
if not stale_marker.exists():
    stale_marker.write_text(reason, encoding="utf-8")
```

This creates `.json.stale` files alongside explorer data. But nothing in the pipeline or explorer checks or cleans up these markers after re-extraction. They accumulate indefinitely.

**Impact**: Once a concept is marked stale, it stays "stale" in status output even after the explorer data is regenerated, unless someone manually deletes the `.stale` file.

---

## Category 6: Fragile Parsing

### H-20: `parse_frontmatter` is a hand-rolled YAML parser

**File**: `frontmatter.py:8-53`
**Severity**: Low-Medium

The parser handles single-line `key: value` pairs and list items, but does NOT handle:
- Quoted values (`key: "value with: colons"`)
- Multi-line values
- Nested structures
- Comments (`# comment`)
- YAML special values (booleans, nulls)

Any frontmatter value containing a colon gets split incorrectly: `Company: General Fusion: A Story` becomes `{"Company": "General Fusion"}` with `: A Story` lost.

**Impact**: Mostly fine because current frontmatter values don't contain colons. But it's a latent bug that will bite when a concept name or company contains `:`.

### H-21: `_get_review_feedback` text extraction is position-dependent

**File**: `loop.py:725-759`
**Severity**: Low-Medium

The function extracts corrective actions from review.md by searching for `## Corrective Actions` after the VERDICT line, then finding the next `## ` header. The regex for "next section" is `^## ` (exactly two `#`), which means `### ` subsections within Corrective Actions don't terminate the block. This is correct.

However, the search for `## Corrective Actions` starts from `verdict_match.end()`, not from the VERDICT line itself. If the review has `## Corrective Actions` BEFORE the VERDICT line (e.g., in a template that puts actions first and verdict last), this will match the wrong section.

**Impact**: Depends on review template format. Current templates put VERDICT before Corrective Actions, so this works. But it's format-fragile.

---

## Code Smell Index (not bugs, but maintenance hazards)

| ID | File | Issue |
|----|------|-------|
| S-01 | `run_analysis.py:55` | Imports private `_has_downstream_artifacts` from `state.py` — unused in run_analysis.py |
| S-02 | `run_analysis.py:94-99` | `_extract_iter_count` duplicated in both `run_analysis.py` and `landscape.py` |
| S-03 | `loop.py:20-21` | `invoke_claude` imported but only used in `_run_cold_start` and `_run_feedback_pass` — could use `invoke_claude_validated` for consistency |
| S-04 | `step_runner.py:42` | `_MISSING = object()` sentinel for mandatory post_hook — confusing API; make it required |
| S-05 | `paths.py:25-32` | Hardcoded absolute paths (`/home/reid/1cfe/...`) — machine-specific, breaks on any other machine |
| S-06 | `sources.py:131-139` | `resolve_source_names` calls `sys.exit(1)` — library code shouldn't exit |
| S-07 | `concepts.py:223-230` | `resolve_concepts` calls `sys.exit(1)` — same issue |

---

## Priority Ranking (what to fix first)

### Tier 1 — Fix Now (causes data loss or silent corruption)

| ID | Issue | Effort |
|----|-------|--------|
| H-01 | Validator reads parsed event text when file missing | Small — add file-existence check before validation |
| H-02 | step_runner writes parsed event text to output file | Small — remove the fallback write, fail instead |
| H-12 | Fix messages have no context | Medium — pass output_path and attempt number to validators |
| H-12a | Fix message drops the output file path | Small — include path in fix message |
| H-13 | No attempt escalation in retry loop | Medium — extend Validator signature |
| H-17 | No transient retry in invoke_claude() | Medium — add exponential backoff for rc=1 |

### Tier 2 — Fix Soon (causes confusing behavior)

| ID | Issue | Effort |
|----|-------|--------|
| H-03 | Feedback pass doesn't verify analysis was modified | Small — compare mtime or hash before/after |
| H-04 | JSON parse errors swallowed silently | Small — add warning to stderr |
| H-09 | Source-integration ignores validation_passed | Small — check the flag |
| H-10 | Assessment ignores validation_passed | Small — check the flag |
| H-11 | Review has no format validation | Medium — add validate_review_verdict to review step |
| H-14 | Validation log missing validated text | Small — add `"validated_text_preview"` field |
| H-16 | Canonical files overwrite with worse model | Medium — check model_ok before copying |

### Tier 3 — Fix When Touching (won't bite unless provoked)

| ID | Issue | Effort |
|----|-------|--------|
| H-05 | Empty result text from JSON events | Small — return error instead of empty string |
| H-06 | No syntax check on generated model_setup.py | Small — run `python -c "compile(...)"` check |
| H-07 | Gap check writes unvalidated stdout | Low priority — informational output |
| H-08 | External feedback archived even if not applied | Small — compare mtime |
| H-18 | research_log orphaned after --force | Small — document or clear log too |
| H-19 | .stale marker never cleaned up | Small — clean up in extraction step |
| H-20 | Hand-rolled YAML parser | Medium — switch to `yaml.safe_load` |
| H-21 | Review feedback extraction position | Low risk currently |

---

## Architectural Observation

The root pattern behind most of these issues is the same: **the pipeline trusts Claude's return code as proof of success**. When `rc == 0`, every code path assumes the expected output was produced correctly. In reality, `rc == 0` means "the Claude CLI process exited cleanly" — it says nothing about whether Claude followed the prompt's instructions.

The `invoke_claude_validated` function was added to address this, but it's only used in 2 of ~8 Claude invocation sites (assess and source-integration). The other 6 sites (cold-start, feedback-pass, model-setup, gap-check, review, address-review, synthesis, external feedback) all use raw `invoke_claude` or `run_claude_step` with no output validation.

---

## Guidance: Unify on `invoke_claude_validated` Everywhere

### The Principle

Every Claude call site should use `invoke_claude_validated`. No exceptions. The validator is `Callable[[str], ValidationResult]` — even a trivial "is this non-empty" check gives you the retry mechanism, the file-vs-stdout distinction, and the audit log for free.

### Prerequisites

Before migrating call sites, fix H-01 in `invoke_claude_validated` itself:

**File-existence must be a first-class check, not a silent fallback.** When `output_path` is provided and the file doesn't exist after invocation, that is a distinct failure mode ("file not written") with its own fix message (including the path). The validator function should only run when the file exists. Current code silently falls through to validating stdout — this must become an error.

### Call Site Migration Map

Every production Claude invocation, what it currently does, and what it should do:

#### Sites that expect Claude to **write a new file**

| Call site | File | Expected output | Current method | Validator to add |
|-----------|------|----------------|---------------|-----------------|
| `_run_cold_start` | loop.py:355 | `iter-N/analysis_body.md` | `invoke_claude` + manual exists check | `validate_non_empty` (or content-specific) |
| `_run_model_in_iteration` | loop.py:489 | `iter-N/model_setup.py` | `invoke_claude` + manual exists check | `validate_python_syntax` |
| `cmd_model_setup` | run_analysis.py:465 | `model_setup.py` | `run_claude_step(file_exists)` | `validate_python_syntax` |
| `cmd_gap_check` | run_analysis.py:223 | `gap_report.md` | `run_claude_step(stdout_to_file)` | `validate_non_empty` (stdout mode — see note below) |
| `cmd_review` | run_analysis.py:562 | `review.md` | `run_claude_step(file_with_fallback)` | `validate_review_verdict` (already exists, just not wired up) |
| `cmd_synthesize` | run_analysis.py:809 | `synthesis_body.md` | `run_claude_step(file_with_fallback)` | `validate_non_empty` (or section-header check) |
| `_run_assess` | loop.py:612 | `iter-N/feedback.md` | `invoke_claude_validated` | Already migrated |
| `_run_source_integration` | loop.py:679 | `iter-N/source_integration_output.md` | `invoke_claude_validated` | Already migrated |

#### Sites that expect Claude to **edit an existing file in-place**

These need a different validator pattern: snapshot the file hash before invocation, then check it changed.

| Call site | File | Edited file | Current method | Validator to add |
|-----------|------|------------|---------------|-----------------|
| `_run_feedback_pass` | loop.py:418 | `analysis.md` | `invoke_claude` + rc check only | `validate_file_modified(original_hash)` |
| `cmd_address_review` | run_analysis.py:678 | `analysis.md` + `model_setup.py` | `run_claude_step(no_output)` | `validate_file_modified(original_hash)` |
| `_apply_external_feedback` | run_analysis.py:402 | `analysis.md` | `invoke_claude` + rc check only | `validate_file_modified(original_hash)` |

#### Sites that use returned stdout (no expected file)

| Call site | File | Current method | Validator to add |
|-----------|------|---------------|-----------------|
| `cmd_gap_check` | run_analysis.py:223 | `run_claude_step(stdout_to_file)` | `validate_non_empty` on stdout text (pass `output_path=None`) |
| `research.py` | research.py:86 | `invoke_claude` + post-hoc filesystem diff | `validate_non_empty` (low value — research success measured by filesystem diff) |

### New Validators Needed

```python
def validate_non_empty(text: str) -> ValidationResult:
    """Minimum viable validator — output must exist and be non-empty."""
    if not text.strip():
        return ValidationResult(
            valid=False,
            fix_message="Your output was empty. Please re-read the instructions and produce the requested output.",
        )
    return ValidationResult(valid=True, details=f"Non-empty ({len(text)} chars)")


def validate_python_syntax(text: str) -> ValidationResult:
    """Check that model_setup.py is parseable Python."""
    try:
        compile(text, "<model_setup>", "exec")
    except SyntaxError as e:
        return ValidationResult(
            valid=False,
            fix_message=f"The Python file has a syntax error: {e}. Please fix and re-write the file.",
            details=f"SyntaxError: {e}",
        )
    return ValidationResult(valid=True, details="Valid Python syntax")


def validate_file_modified(original_hash: str) -> Validator:
    """Factory: returns a validator that checks the file content actually changed."""
    def check(text: str) -> ValidationResult:
        import hashlib
        current = hashlib.sha256(text.encode()).hexdigest()
        if current == original_hash:
            return ValidationResult(
                valid=False,
                fix_message="The file was not modified. You must apply the requested changes using the Edit tool.",
            )
        return ValidationResult(valid=True, details="File content changed")
    return check
```

### What Happens to `run_claude_step`?

`run_claude_step` (`step_runner.py`) currently wraps `invoke_claude` with its own output-mode logic (`stdout_to_file`, `file_with_fallback`, `file_exists`, `no_output`). Two options:

1. **Replace it**: Migrate all `run_claude_step` callers to use `invoke_claude_validated` directly with appropriate validators. `run_claude_step`'s template-filling, skip-if-exists, dry-run, and post-hook features become inline or move into a lighter helper.

2. **Retrofit it**: Make `run_claude_step` accept an optional `validator` parameter and call `invoke_claude_validated` internally instead of `invoke_claude`. The output-mode enum can be simplified or removed — the validator replaces it.

Option 2 is less churn. The output-mode enum (`file_with_fallback`, etc.) becomes irrelevant because the validator + the H-01 fix handle file-existence checking uniformly.

### What This Fixes

Migrating to `invoke_claude_validated` everywhere, combined with the H-01 fix, eliminates these issues by construction:

| Issue | How it's resolved |
|-------|------------------|
| H-01 | Fixed in `invoke_claude_validated` itself — file-existence is a first-class check |
| H-02 | `file_with_fallback` mode eliminated — no more writing stdout to disk |
| H-03 | `validate_file_modified` catches no-op edits |
| H-06 | `validate_python_syntax` catches broken model scripts before execution |
| H-07 | Gap check gets `validate_non_empty` |
| H-08 | `validate_file_modified` — feedback not archived if file didn't change |
| H-09 | Moot — `validation_passed` is checked by the unified path |
| H-10 | Moot — same |
| H-11 | Review gets `validate_review_verdict` |
| H-12 | Fixed in `invoke_claude_validated` — fix messages include file path and context |
| H-12a | Fixed by same mechanism — output path passed through to fix messages |
| H-13 | Fixed in `invoke_claude_validated` — attempt number available for escalation |
| H-14 | Fixed in `invoke_claude_validated` — log includes validated text preview |

That's **13 of 22 issues** resolved by a single architectural change.

## Remaining Recommendations

1. **Immediate**: Fix H-01 in `invoke_claude_validated` (file-existence as first-class check, not fallback). Fix H-17 (transient retry in `invoke_claude`). These are independent and can be done in parallel.
2. **Then**: Retrofit `run_claude_step` to accept a `validator` param and use `invoke_claude_validated` internally.
3. **Then**: Migrate all call sites per the table above, adding validators as needed.
4. **Then**: Fix the remaining 9 issues individually (H-04, H-05, H-15, H-16, H-18-H-21) — these are independent of the unification.
