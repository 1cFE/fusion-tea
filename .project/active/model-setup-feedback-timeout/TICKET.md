# TICKET: model-setup feedback pass times out and discards valid work

**Status:** RESOLVED 2026-06-06 — fixes verified end-to-end on concept 24
**Priority:** P0 — SHOWSTOPPER (blocks concept convergence; deadline 2026-06-08)
**Created:** 2026-06-06
**Owner:** Reid W (investigation to be handed to another agent)
**Area:** `exploration/concept_analysis/scripts/` (analysis pipeline, model-setup step)

---

## Resolution (2026-06-06)

Both defects fixed. End-to-end re-run on concept 24:

| Step | Before | After |
|---|---|---|
| iter-2 model-setup | 1800s → discarded (rc=-1) | **88s, validated, promoted (LCOE=13.5 $/MWh)** |
| canonical `model_setup.py` | stamped `# STALE` | clean, matches iter-2 |
| `verdict.json` | `model_ran:false, model_ok:false` | `model_ran:true, model_ok:true` |

(`verdict: FAIL` after the run reflects 3 unresolved assessment findings — domain
non-convergence, not pipeline failure. Two passes were not enough; bump
`--max-passes` for convergence.)

### Fix A — `lib/loop.py:_run_model_in_iteration`

Inverted the check order: validators-on-disk now beat `returncode`. If
`validation_passed=True` and the file exists, the model is honored even when
`returncode != 0`. `rc!=0` now surfaces as a `warn:` line on stderr instead of
silently discarding valid work.

The same rc-before-validation pattern exists at `loop.py:437, 517, 951, 1023`
(cold-start analyze, feedback-pass analyze, assess, source-integration). Left
unchanged for now — same theoretical vulnerability but no documented case.
Easy harmonization later.

### Fix B (diagnosis) — diagnostic harness

`scripts/diagnose_model_setup_slowness.py` is an out-of-band test harness that
reproduces the agent call with `--output-format stream-json
--include-partial-messages` and streams every event to JSONL, so SIGKILL no
longer destroys evidence. It does NOT touch `lib/claude.py` or the production
path. Diagnostic run completed in 411s and revealed the time sink:

| Phase | Time | Cause |
|---|---|---|
| Validator/library archaeology | 0-215s (~50%) | Agent reads `scripts/lib/validators.py`, `canonical_accounts.py`, costingfe source to reverse-engineer override registry constraints |
| Self-verify cold-boots | 267-353s (~20%) | 3× `uv run python model_setup.py` at ~30s each cold-boot, including a C220102 rounding-trap rabbit hole |
| Auto-memory write | 388-395s | Agent writes a new gotcha file to its own auto-memory unprompted |

Production hit 900s+ on both attempts due to LLM sampling variance compounded
by these structural costs.

### Fix B1 — timeout floor for edit-pass

`_run_model_in_iteration` now floors edit-pass timeout at 1800s (cold-start
unchanged; user-supplied larger values still win). Edit-pass naturally takes
4-7× longer than cold-start; the 900s default was below the P95.

### Fix B2 — validator contract in edit prompt

`prompt_templates/model_setup_costingfe_edit.md` now front-loads:

- A "Validator Contract" block enumerating every requirement
  (`validate_python_syntax + validate_file_modified +
  validate_model_setup_contract_strict + validate_override_registry`) —
  six-field shape, `cost_basis: "noak"`, `blocked_by` on disabled, frame
  restrictions, magnitude bound, rollup blocklist — and **explicitly forbids
  reading the validator/library source** to look it up.
- Self-verification budget: at most 2 `uv run python model_setup.py` runs,
  no ad-hoc `/tmp/` test scripts.
- Operational constraints: no auto-memory writes during pipeline runs, no
  library-bug investigation (file `blocked_by` instead).

Combined with B1, this took the edit-pass from a 1800s+ timeout to 88s on
the verification run — faster than cold-start.

### Files changed

- `exploration/concept_analysis/scripts/lib/loop.py` (Defect A + B1)
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe_edit.md` (B2)
- `scripts/diagnose_model_setup_slowness.py` (new — diagnostic harness)

### Side artifact (not deleted)

The diagnostic agent created
`~/.claude/projects/-home-reid-1cfe-fusion-tea/memory/gotcha_cas22_display_rounding.md`
during its run. The new prompt prevents recurrence, but the existing file is
still there.

---

## Original investigation (preserved below)

> **Note to the investigator:** this ticket is a *description of what is known*, written
> from a read-only audit of one failing run. Nothing here has been fixed. Two distinct
> defects are described (A and B); A is deterministic and cheap to fix, B needs a live
> traced run to root-cause. Candidate fixes at the bottom are **candidates, not decisions.**

---

## TL;DR

On a concept re-run (`run_analysis.py analyze 24 --force --max-passes 2`), the
**iter-2 model-setup step burned ~30 minutes and produced no usable result**, even
though the agent had **written a model that passed every validator.** The run ended
`FAIL`, the concept did not converge, and the canonical `model_setup.py` was stamped
`# STALE`.

Two independent defects chained together:

- **Defect A (deterministic, cheap fix):** the orchestrator discards a *valid* model
  if the `claude` process exited with a non-zero return code — even when validation
  passed. A model that passed Python-syntax + three-forward-contract + override-registry
  validators was thrown away because the process was killed at the timeout.
- **Defect B (needs root-cause):** the model-setup agent on the **feedback/edit pass**
  is pathologically slow — it blew through the **900 s** per-attempt timeout on *both*
  attempts (≈1800 s total), versus **205 s** for the same concept's cold-start pass.

---

## Severity / impact

- Any concept that needs a second (feedback) pass can silently fail to converge and
  waste ~30 min per attempt-pair of wall-clock + Claude spend.
- The pipeline then reports `FAIL` and leaves a `# STALE` model that does **not** match
  the iter-2 analysis — so downstream review/assessment compares mismatched artifacts
  and raises spurious findings (this is what produced the confusing C220102 "dispute"
  in the audit that triggered this ticket).
- This is a known-recurring failure mode, not a one-off: see the code comment at
  `lib/claude.py:246-251` referencing prior timeout casualties ("the failure mode that
  left concepts 14 and ...").

---

## Reproduction

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 24 --force --max-passes 2
```

Observed console output:

```
24-dense-plasma-focus: cleared 3 prior iteration(s)
analyze (cold start) 24-dense-plasma-focus ... done (718s, 39196 chars)
  model-setup 24-dense-plasma-focus ... done (205s) → running model ... ok (LCOE=16.0 $/MWh)
assess 24-dense-plasma-focus iter 1 ... 3 findings (378s)
analyze iter 2/2 (feedback pass) 24-dense-plasma-focus ... done (702s)
  model-setup 24-dense-plasma-focus ... FAILED (1800s, rc=-1)
assess 24-dense-plasma-focus iter 2 ... 2 findings (182s)
warn: 24-dense-plasma-focus did not converge in 2 passes
```

---

## Evidence

### From `analyses/24-dense-plasma-focus/iter-2/validation_log.json`

| attempt | time (UTC) | elapsed | result |
|---|---|---|---|
| model-setup #1 | 18:47:32 → 19:02:33 | **900 s** | FAILED — *"File content unchanged (SHA-256 match)"*; `retry_reason: "timeout after 900s (rc=-1, no session_id) — retrying with original prompt, fresh invocation"` |
| model-setup #2 | 19:02:33 → 19:17:33 | **900 s** | **`passed: true — All validators passed`** |

So attempt #1 timed out before it even modified the copied prior model; attempt #2 ran
the full 900 s, **wrote a valid model**, and the process was then killed at the timeout.

### Final state on disk after the run

- `analyses/24-dense-plasma-focus/model_setup.py` — first line `# STALE: analysis-updated-iter-2` (this is the **iter-1** model, not iter-2).
- `analyses/24-dense-plasma-focus/iter-2/model_setup.py` — the **valid** attempt-2 model that was discarded (never run, never promoted).
- `analyses/24-dense-plasma-focus/iter-2/verdict.json` — `verdict: FAIL`, `model_ran: false`, `model_ok: false`.

---

## Defect A — valid model discarded on non-zero process return code

**Deterministic. Located precisely. No agent call needed to fix or verify.**

1. `invoke_claude_validated` validates the **output file on disk**, not the process
   exit. When the file is valid it returns `validation_passed=True` carrying the *last*
   `InvokeResult` — whose `returncode` is `-1` if that invocation timed out.
   See `lib/claude.py:362-386` (reads `output_path`, runs validator, returns
   `ValidatedResult(invoke=result, validation_passed=True, ...)`).
2. The caller then checks the **process return code before** the validation flag:

   ```python
   # lib/loop.py:656-671  (_run_model_in_iteration)
   elapsed = time.time() - ctx.start_time
   if result.invoke.returncode != 0:                 # -1 != 0  → TRUE
       print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
       return False, False                            # ← discards the VALID file
   if not result.validation_passed:                   # never reached in this case
       ...
   ```

   Because `returncode == -1` short-circuits at line 658, the valid model
   (`validation_passed=True`) is never run (`run_model`, line 677) and never promoted.

3. Downstream: `_update_canonical_files(..., model_ok=False)` (loop.py:245) does not
   promote the iter-2 model; `propagate_staleness` (loop.py:278-283) only exempts
   `model_setup.py` from the `# STALE` stamp when `model_ok=True`, so the stale stamp
   lands (stamping logic at `lib/state.py:100-103`).

**Net:** a model that passed all validators is thrown away purely because the process
got killed a moment after writing it. Even with Defect B unfixed, honoring a
validated-on-disk file here would have turned this run into a runnable iteration.

---

## Defect B — feedback/edit-pass model-setup is pathologically slow

**Needs a live, traced run to root-cause. Hypotheses only below.**

- Same concept, same machine: **cold-start model-setup = 205 s; feedback-pass
  model-setup = ≥900 s on each of two attempts.** The edit pass is ~4–9× slower and
  reliably exceeds the timeout.
- The default per-invocation timeout is **900 s** (`run_analysis.py:1385`,
  `--timeout default=900`); `invoke_claude_validated` retries once on a timeout
  (`max_retries=2` → up to 3 attempts; here it returned after 2 because attempt 2's
  file validated). So "1800 s" = two 900 s timeouts back-to-back.
- The agent transcript is **not saved** anywhere, so we cannot see what consumed the
  time from disk. Attempt 1 didn't even capture a `session_id` before being killed.

**Hypotheses (unverified):**
1. Edit-mode self-verification loop: the agent runs `uv run python model_setup.py`
   repeatedly to check its edits, hits the C220102 "displays as 0.0 but is really
   0.0404" rounding trap (see the audit / `model-setup` rationale churn), keeps
   re-reasoning and re-running, and loops itself into the timeout.
2. The iter-1 assessment feedback (the C220102 enabled/disabled finding) sends the
   edit agent down a rabbit hole that doesn't converge.
3. Edit-tool churn / many small failed edits against the copied prior model.
4. costingfe import + forward cost per self-test run × many iterations.
5. (Lower likelihood) the agent spawning subagents; the edit template
   `model_setup_costingfe_edit.md` does not instruct subagent use, but the agent has
   the tools.

---

## Key files / line map for the investigator

| File | Lines | What |
|---|---|---|
| `lib/loop.py` | 582-681 | `_run_model_in_iteration` — the model-setup step in the loop |
| `lib/loop.py` | **656-671** | **Defect A** — returncode checked before `validation_passed` |
| `lib/loop.py` | 245, 278-283 | canonical-promotion + staleness gating on `model_ok` |
| `lib/claude.py` | 264-431 | `invoke_claude_validated` — invoke + validate + retry-on-timeout |
| `lib/claude.py` | 362-386 | validates file on disk; returns `validation_passed=True` even if last invoke `rc=-1` |
| `lib/claude.py` | 94-184, 246-259 | `invoke_claude`, timeout → `rc=-1` sentinel; prior-timeout-casualty comment |
| `lib/state.py` | 92-103 | `# STALE:` stamping |
| `run_analysis.py` | 1385 | `--timeout default=900` |
| `prompt_templates/model_setup_costingfe_edit.md` | — | the edit-pass prompt the slow agent runs |

---

## What is NOT the cause (ruled out)

- **Recent prompt edits for the 1 GWe policy work item are not implicated.** The
  failing run's artifacts are timestamped 2026-06-06 ~18:47-19:20 UTC, which **predates**
  the addition of `{{@config/override_semantics.md}}` to `model_setup_costingfe_edit.md`
  (made later the same session). The cold-start model-setup (which *did* carry the policy
  include in `model_setup_costingfe.md`) completed normally in 205 s — a larger prompt
  does not explain a 15-minute agent loop. (Worth a sanity re-check after the edit-template
  change, but it is not the root cause of the observed timeouts.)

---

## Investigation plan / open questions

1. **Defect A:** confirm by reading `lib/loop.py:656-671` + `lib/claude.py:362-386`.
   Decide the correct semantics: if `validation_passed` and the file is on disk and
   valid, should we run/promote it even when `returncode == -1`? (Likely yes, with a
   warning.) Check for parallel copies of this returncode-before-validation pattern in
   the other step runners (analyze/assess/review) at `loop.py:403, 482, 931, 1015`.
2. **Defect B:** run *only* the model-setup step with streaming output and a long
   timeout to capture the transcript:
   `run_analysis.py model-setup 24 --timeout 3600` (verify the subcommand + flags), or
   instrument `invoke_claude` to persist the agent stdout/transcript per attempt so the
   time sink is visible post-hoc.
   - Is the slowness specific to this concept (C220102 zero/rounding trap, Low fit,
     many zeroed accounts) or general to all feedback passes? Re-test on a second
     concept that needed a feedback pass.
   - Does the agent self-run the model in a loop? Count tool calls / model executions.
3. **Quantify blast radius:** grep prior runs' `verdict.json` for `model_ok: false` +
   `rc=-1` to see how many concepts this has already silently broken.

---

## Candidate fixes (NOT decisions — for discussion)

- **A1:** in `_run_model_in_iteration`, check `result.validation_passed` (and file
  existence/validity) *before* treating `returncode != 0` as fatal — honor a model that
  passed validators even if the process was killed. Emit a warning, don't discard.
- **B1 (band-aid):** raise the model-setup timeout for the edit pass. Treats the symptom,
  not the cause; do only alongside B-root-cause work.
- **B2:** persist the per-attempt agent transcript so future timeouts are diagnosable
  without a re-run.
- **B3:** constrain the edit-mode prompt to forbid open-ended self-verify loops (e.g.
  "make the edits; run the model at most once"), pending root-cause.

---

## Artifacts to inspect

- `exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/validation_log.json`
- `exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/model_setup.py` (the discarded valid model)
- `exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/verdict.json`
- `exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/model_setup_prompt.md` (the rendered edit prompt)
- `exploration/concept_analysis/analyses/24-dense-plasma-focus/model_setup.py` (the STALE iter-1 canonical)
