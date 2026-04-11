---
date: 2026-04-08T12:00:00-07:00
researcher: Claude
topic: "Validation retry mechanism failure analysis"
tags: [research, pipeline, validation, concept-analysis]
status: complete
last_updated: 2026-04-08
---

# Research: Why Validation Retries Fail Silently

**Date**: 2026-04-08
**Research Type**: Failure Analysis / Root Cause

## Research Question

The concept analysis pipeline's output validation + retry mechanism
(`invoke_claude_validated`) fails to recover from format violations. Concept 01
iter-10 failed the assess step 3 times identically. Why can't the retry loop
fix a simple format issue?

## Failure Timeline (concept 01, iter-10)

```
06:28:18 UTC  attempt 1  FAIL  "No VERDICT line found"
06:32:02 UTC  attempt 2  FAIL  "No VERDICT line found"  (identical)
06:35:59 UTC  attempt 3  FAIL  "No VERDICT line found"  (identical)
→ verdict.json: ERROR, finding_count: 0, model_ran: false
```

Source: `analyses/01-hts-compact-tokamak/iter-10/validation_log.json`

## The Chain of Failure

### Step 1: Claude is told to write a file

The assessment prompt (`assessment.md:81-82`) instructs:

```
Write the assessment to this file using the Write tool:
`/path/to/iter-10/feedback.md`
```

The prompt also includes `feedback_format.md` — a complete specification with
a concrete example showing `VERDICT: FINDINGS` followed by `### F-1:` blocks.

### Step 2: Claude runs — feedback.md is never created

After Claude finishes, `feedback.md` does not exist at the output path.
This means one of:
- Claude never called the Write tool
- Claude called the Write tool but the path was wrong
- Claude wrote conversational text instead of following the file-write instruction

We do not know which. **Nothing in the pipeline captures this distinction.**

### Step 3: The validator reads the wrong thing

`invoke_claude_validated` (`claude.py:155-161`):

```python
if output_path is not None and output_path.exists():
    text = output_path.read_text(encoding="utf-8")
else:
    text = result.stdout  # ← THIS PATH TAKEN
```

Since `feedback.md` doesn't exist, the validator falls through to
`result.stdout` — which is whatever conversational text Claude returned
via the JSON event stream. This is NOT the feedback content. It's
whatever Claude said in its response (reasoning, explanation, etc.).

The validator pattern-matches `^VERDICT:\s*(PASS|FINDINGS)$` against
conversational stdout. Obviously it doesn't match.

### Step 4: The fix message is blind

The fix message sent to Claude via `--resume` (`validators.py:64-70`):

```
Your feedback file is missing the required verdict line. The file MUST
contain exactly one line reading either `VERDICT: PASS` or
`VERDICT: FINDINGS` (on its own line, at the start of the line, with
no extra text). Please re-write the feedback file with the correct format.
```

Problems with this message:

1. **Does not say the file wasn't written.** Claude doesn't know the
   fundamental problem is that `feedback.md` doesn't exist. It may think
   the file content was wrong, not that the file was never created.

2. **Does not show what was actually seen.** Claude has no idea what the
   validator looked at. It can't diagnose its own failure.

3. **Does not include the format example.** The initial prompt had the
   full `feedback_format.md` with a concrete example. The fix message
   strips all that context. Claude is told to "re-write the feedback file
   with the correct format" without being shown the format.

4. **Does not include the file path.** The fix message says "the feedback
   file" but never restates the path. Claude may not recall it from the
   initial prompt.

### Step 5: Retry produces identical failure

Claude receives the fix message via `--resume`, but has the same
information gap. It doesn't know:
- Whether its file write succeeded or failed
- What file path to write to
- What format to use (beyond "VERDICT: PASS or FINDINGS")

The retry produces the same result. The fix message is identical on
all 3 attempts — no escalation, no additional context.

## Root Causes (ordered by severity)

### RC-1: Validator does not distinguish "file not written" from "file has wrong content"

The most critical failure. When `output_path` doesn't exist, the system
silently falls back to validating stdout. This conflates two completely
different failures:

- **File exists, wrong format** → the fix message about format is correct
- **File doesn't exist** → the fix message is wrong; the real problem is
  the file was never created

Location: `claude.py:157-160`

### RC-2: Fix message contains zero context about what went wrong

The fix message is static text from the validator. It does not include:
- What was actually validated (the text that failed)
- Whether the file was written or not
- The expected format example
- The output file path

Location: `validators.py:64-70` (feedback), `validators.py:124-130` (review)

### RC-3: Fix messages do not escalate across attempts

Attempt 1, 2, and 3 send byte-identical fix messages. The validator
function signature is `Callable[[str], ValidationResult]` — it has no
knowledge of attempt number. The retry loop in `invoke_claude_validated`
does not modify or augment the fix message between attempts.

Location: `claude.py:155-203` (retry loop), `validators.py:45` (type alias)

### RC-4: No diagnostic capture of what Claude actually produced

When validation fails, nothing records:
- Whether Claude used the Write tool
- What Claude wrote to stdout
- Whether the file exists at a different path
- The actual content that was validated

The `validation_log.json` records the validator name, pass/fail, details
string, and fix message — but not the input text that was validated.

Location: `claude.py:164-174` (log entry construction)

## Affected Code Paths

| File | Lines | What |
|------|-------|------|
| `scripts/lib/claude.py` | 125-208 | `invoke_claude_validated()` — retry loop |
| `scripts/lib/claude.py` | 155-161 | File-vs-stdout fallback (RC-1) |
| `scripts/lib/claude.py` | 164-174 | Validation log entry (RC-4) |
| `scripts/lib/validators.py` | 52-110 | `validate_feedback_verdict()` — fix messages (RC-2) |
| `scripts/lib/validators.py` | 45 | `Validator` type alias — no attempt awareness (RC-3) |
| `scripts/lib/loop.py` | 612-619 | `_run_assess()` — calls `invoke_claude_validated` |
| `scripts/lib/loop.py` | 674-700 | `_run_source_integration()` — same pattern |

## What a Working Fix Message Would Look Like

For the "file not written" case (attempt 1):

```
VALIDATION FAILED: The output file was not created.

You must write the assessment to this exact path using the Write tool:
  /home/reid/.../iter-10/feedback.md

Expected format:

  VERDICT: FINDINGS

  ### F-1: [title]
  - **Target:** [section]
  - **Category:** analysis | model
  - **Finding:** [what is wrong]
  - **Recommendation:** [what to do]
  - **Priority:** blocking | important | minor

If no findings: write only `VERDICT: PASS` to the file.
```

For the "file exists but wrong format" case (attempt 2+):

```
VALIDATION FAILED (attempt 2 of 3): The file was written but the
format is wrong.

What was found in feedback.md (first 500 chars):
  [actual content snippet]

The file MUST start with `VERDICT: PASS` or `VERDICT: FINDINGS` on
its own line. Your file does not contain this line.

Write the corrected content to:
  /home/reid/.../iter-10/feedback.md
```

## Relationship to Other Pipeline Failures

This report covers only the validation mechanism. The concept 15/17a
crashes (rc=1 with empty stderr) are a separate issue — the Claude CLI
subprocess fails before any validation can occur. That is a transient
retry problem in `invoke_claude()` itself, not a validation problem.
