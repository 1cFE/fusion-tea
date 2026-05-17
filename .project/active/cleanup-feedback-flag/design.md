# Design: Cleanup `--feedback` Flag (Custom Feedback as Iteration Input)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17 09:35 PDT
**Branch:** main
**Spec:** `.project/active/cleanup-feedback-flag/spec.md`

---

## Overview

Convert `--feedback PATH` from a parallel analysis-only patch path into a sixth producer in `lib/loop.py:run_stage1_loop`. The user-supplied file becomes `iter-N/pre_feedback.md` for one iteration; analyze, model_setup, and assess all consume it through the existing channels.

---

## Related Artifacts

- **Spec:** `.project/active/cleanup-feedback-flag/spec.md`
- **Research:** `.project/research/20260517-081444_model-setup-inconsistencies.md`
- **Affected files:**
  - `exploration/concept_analysis/scripts/run_analysis.py` — `cmd_analyze` guards, deletion of `_apply_external_feedback`, argparse help text
  - `exploration/concept_analysis/scripts/lib/loop.py` — new producer branch in `run_stage1_loop`
  - `exploration/concept_analysis/README.md` — producer table, flag table, mutual-exclusion list

---

## Research Findings

- **Producer chain lives in `lib/loop.py:115-185`** as a flat if/elif cascade selecting one of: cold_start, review, source_integration, research, assess. Each branch produces `iter-N/pre_feedback.md` (or, for cold_start, leaves `feedback_path = None` so a different prompt template fires).
- **`_copy_to_pre_feedback(source, iter_dir)` at `lib/loop.py:284`** is the exact helper for "copy this file to `iter-N/pre_feedback.md` and return the destination path." Already used by four of the five existing branches. Direct reuse.
- **`validate_feedback_verdict(text)` at `lib/validators.py:61`** already enforces the format spec FR-6 (d)(e) requires: (1) `VERDICT:` line, (2) if `FINDINGS`, at least one `### F-N:` block, (3) each block has a `Category:` field. Returns a `ValidationResult` with `valid: bool` and a `fix_message`. Direct reuse — no new parser needed.
- **`run_stage1_loop(concept, args, *, resume, common_vars, analysis_template, assessment_template)`** already takes `args: argparse.Namespace`. `args.feedback` is reachable inside the loop via `getattr(args, "feedback", None)` without any signature change.
- **`cmd_analyze` at `run_analysis.py:301-321`** routes to `_apply_external_feedback` whenever `--feedback` is set, bypassing the loop entirely. The branch is 3 lines (`if feedback: _apply_external_feedback(...); return`). The bypassed function is `_apply_external_feedback` at `run_analysis.py:401-479` (79 lines).
- **Argparse `--feedback`** is at `run_analysis.py:1491-1492` with help text "Apply feedback file to existing analysis (skips cold-start)." Help text needs updating to reflect new behavior.
- **README content to update:**
  - Line 221 — flag table description.
  - Lines 228-231 — mutual-exclusion list (`--feedback + --resume` row is removed; `--feedback + --force` row stays with a new tagline).
  - Lines 92-100 — producer-selection table (new row for external feedback at priority 0, above review).

---

## Core Concept

The iteration loop already has the right abstraction: each iter consumes exactly one `pre_feedback.md` and runs analyze → model_setup → assess on it. Where that `pre_feedback.md` comes from is determined by a producer selector at the top of the iter body. The fix is to add `--feedback` as a sixth producer with highest priority. The producer reads the user's file, copies it to `iter-N/pre_feedback.md` via the existing `_copy_to_pre_feedback` helper, and falls back to the normal chain for any subsequent iters in the same invocation. Validation happens once, up front, in `cmd_analyze` — before any iter directory is created and before Claude is invoked. After this change, `--feedback` carries no special downstream behavior: the rest of the pipeline cannot tell whether `pre_feedback.md` came from the user or from a prior assessor.

The key insight is that all the silent-drift failure modes of the current implementation come from `--feedback` being a *different* path. Once it produces the same artifact (`pre_feedback.md`) consumed by the same stages with the same prompts, there's nowhere for analyze and model_setup to disagree.

---

## Key Bets & Decisions

- **Bet: validation in `cmd_analyze`, not in the loop branch.** Failing fast before any iter directory exists or any Claude call is made keeps the failure modes auditable and the loop branch trivial. The alternative (validate inside the producer) would either duplicate the guard or trip after the loop has already mutated state.
- **Bet: reuse `validate_feedback_verdict`** rather than write a new parser. The validator was built for the assess output schema, but the schema *is* the format we want for external feedback. Same input, same checks.
- **Decision: `--feedback` implicitly sets `resume = True` in `cmd_analyze`.** When the user passes `--feedback` alone (no `--resume`, no `--add-passes`), the loop should append a new iter, not cold-start at iter 1. Setting resume implicitly mirrors how `--add-passes` already implies resume (`run_analysis.py:291-292`). The producer branch can then assume `iter_num >= 1` with `analysis.md` present.
- **Decision: producer branch fires once via `used_external_feedback` flag**, exactly like `used_review_feedback` and `used_source_integration`. Subsequent iters in the same `--add-passes N` invocation fall through to the normal assess chain.
- **Decision: keep the `--feedback + --force` guard, drop the `--feedback + --resume` guard.** `--force` re-cold-starts the analysis; combining it with `--feedback` is incoherent. `--resume` is now the implicit default for `--feedback` so the old guard becomes wrong.
- **Alternative considered (rejected): merge user feedback with prior assess findings.** This is what the `--research` path does at `lib/loop.py:169` via `_merge_feedback`. Rejected because the user explicitly wants their CR to be *the* input, not blended (see conversation context: "I want to use custom feedback"). Open findings from the prior assessor will resurface on the next iter via the normal assess chain if they're still real problems in the post-CR state.

---

## Architecture

**Producer chain — new state**

```
priority 0: external_feedback (--feedback set, one-shot per invocation)  ← NEW
priority 1: cold_start         (iter 1, no resume)
priority 2: review             (Review-Status: revise, one-shot)
priority 3: source_integration (new sources, one-shot)
priority 4: research           (--research, iter > 1)
priority 5: assess             (default: prior iter's post_feedback)
```

**Data flow with `analyze 28 --feedback my_cr.md --add-passes 2`** (concept at iter-3):

```
cmd_analyze
  ├── guard: --feedback + --force? error.
  ├── guard: my_cr.md exists / non-empty / passes validate_feedback_verdict?
  ├── guard: concept's analysis.md exists?
  ├── set resume = True implicitly
  └── run_stage1_loop(args=args, resume=True, ...)
         │
         ├── iter-4  ← used_external_feedback=False, args.feedback set
         │     producer: external_feedback → cp my_cr.md iter-4/pre_feedback.md
         │     used_external_feedback = True
         │     analyze + model_setup + assess consume iter-4/pre_feedback.md
         │     assess writes iter-4/post_feedback.md
         │
         └── iter-5  ← used_external_feedback=True
               producer: assess (default) → cp iter-4/post_feedback.md → iter-5/pre_feedback.md
               (rest of normal chain)
```

**Integration boundaries**

- `cmd_analyze` owns: argparse, guard ordering, validation, implicit-resume promotion, single-concept enforcement, calling `run_stage1_loop`.
- `run_stage1_loop` owns: iter directory creation, producer dispatch, stage invocation.
- `lib/validators.validate_feedback_verdict` owns: format validation.
- `lib/loop._copy_to_pre_feedback` owns: file copy mechanics.

Nothing else needs to know `--feedback` exists.

---

## Required Invariants

1. **The user-supplied source file is never written to.** Only `_copy_to_pre_feedback` touches it, and that helper opens for read.
2. **`iter-N/pre_feedback.md` is byte-equal to the source file** on the iter where external feedback fires. (Verifiable post-run.)
3. **All `cmd_analyze` guards fail before any filesystem mutation** in the concept directory. No partial iter-N/ directories left behind on validation failure.
4. **No code path other than the new producer reads `args.feedback`** inside the loop. The stage prompts and downstream helpers stay agnostic.
5. **`_apply_external_feedback` has zero callers** after this change. `grep _apply_external_feedback scripts/` returns nothing.
6. **`--feedback` implies `resume = True`** in `cmd_analyze` whenever passed. There is no `--feedback` invocation that starts at iter 1 of a concept that already has `analysis.md`.

---

## Component Overview

### `cmd_analyze` (modified) — `run_analysis.py:275-356`

Adds guard block before delegating to `run_stage1_loop`. Removes the early-return branch that called `_apply_external_feedback`. Promotes `resume = True` implicitly when `--feedback` is set. Updates the `--feedback + --force` error message; removes the `--feedback + --resume` guard.

### `_apply_external_feedback` (deleted) — `run_analysis.py:401-479`

Deleted in full. No callers remain after `cmd_analyze` is updated.

### `run_stage1_loop` (modified) — `lib/loop.py:55-`

Adds `used_external_feedback = False` to the producer-flag init at line 102-103. Adds a new top-priority branch in the producer cascade at line 115. No signature change.

### Argparse `--feedback` (help text only) — `run_analysis.py:1491-1492`

Help text rewritten to describe the new behavior.

### README (modified) — `exploration/concept_analysis/README.md`

Producer table row added (priority 0). Flag table description updated. Mutual-exclusion list shortened. No structural changes.

---

## Non-Goals

- No change to `cmd_model_setup`'s separate `--feedback` flag (`run_analysis.py:1512`).
- No change to feedback file format (still VERDICT + F-N findings).
- No change to stage prompt templates.
- No change to the existing producer branches.
- No new tests in this design (plan/implement stage).

---

## Implementation Notes

**New producer branch (pseudocode, ~10 lines, goes at the top of the cascade in `lib/loop.py` at line 120):**

```python
if not used_external_feedback and getattr(args, "feedback", None):
    used_external_feedback = True
    feedback_source = "external"
    feedback_path = _copy_to_pre_feedback(Path(args.feedback), iter_dir)
    print(f"  {cid} iter {iter_num}: using external feedback "
          f"{args.feedback.name}")
elif iter_num == 1 and not resume:
    # existing cold_start branch
```

**Guard order in `cmd_analyze` (top to bottom, fail-fast):**

1. `--resume + --force` → exit 1 (existing, unchanged).
2. If `feedback` set:
   a. `--feedback + --force` → exit 1 (existing, message updated).
   b. `len(targets) != 1` → exit 1 (existing, unchanged).
   c. `not feedback.is_file()` → exit 1 (existing, unchanged).
   d. `feedback.stat().st_size == 0` → exit 1 (NEW: empty-file check).
   e. `validate_feedback_verdict(feedback.read_text())` returns invalid → exit 1 with the validator's `fix_message` (NEW).
   f. After concept resolution: `not analysis_path.exists()` → exit 1 (NEW: cold-start incompatibility per FR-6 (a)).
   g. Set `resume = True` (NEW).
3. Continue to existing skip logic / loop dispatch.

Guard (f) needs to land inside the per-concept loop because `analysis_path` is built from the resolved concept ID. Guards (a)–(e) can fire before concept resolution because they're file-level.

**`--feedback + --resume` guard removal:** delete `run_analysis.py:303-305` outright. The implicit-resume promotion makes this state unreachable.

**Cold-start interaction:** with `resume = True` implicitly, the existing `iter_num == 1 and not resume` cold-start branch (line 120) can no longer fire on a `--feedback` invocation. Guard (f) makes this an explicit precondition rather than an emergent property — if a future change drops the implicit-resume, the explicit guard still rejects.

**Skip-logic interaction:** `run_analysis.py:333-335` skips concepts where `analysis.md` exists without `--force`/`--resume`. With implicit `resume = True`, this branch is bypassed. No conflict.

**README updates:**

Producer table (line 92-100) — insert as new top row:

```
| 0 | `--feedback PATH` set | **external** (one-shot) | User-supplied file → `iter-N/pre_feedback.md` → `analysis_v2.md` feedback mode |
```

Flag table (line 221) — change description to:

```
| `--feedback PATH` | `analyze` | — | Use file as `iter-N/pre_feedback.md` for next iter (requires existing analysis.md; implies --resume; runs full iter end-to-end) |
```

Mutual-exclusion list (line 228-231) — remove the `--feedback and --resume` line, keep the `--feedback and --force` line with updated tagline:

```
- `--feedback` and `--force` are mutually exclusive (--force re-cold-starts, which contradicts --feedback's "edit existing analysis" mode)
```

Argparse help text (line 1492) — change to:

```
help="Use file as pre_feedback.md for next iter (requires existing analysis.md, implies --resume)"
```

**No staleness propagation needed.** `_apply_external_feedback` called `propagate_staleness` because it only ran analyze; the new path runs the full loop, which regenerates all downstream artifacts naturally.

---

## Potential Risks

- **Risk: an older concept ships a `change_requests_*.md` file from the legacy archive.** No active code reads these; they're dead bytes. No migration needed, but the README workflow change is the user-visible signal that the old pattern is gone.
- **Risk: a future `--feedback` invocation accidentally double-fires** if some refactor changes the one-shot flag wiring. Mitigation: the `used_external_feedback` flag is set inside the branch before any side effects, mirroring the established pattern from `used_review_feedback`.
- **Risk: validation regex drift.** If `validate_feedback_verdict` is loosened in the future for assess output, that loosening propagates to external feedback. This is the correct coupling — both inputs need to satisfy the same format the model-setup edit prompt expects — but worth noting in code review of any future validator change.

---

## Integration Strategy

This is a strict subtraction-plus-six-lines change inside one subcommand. No new modules, no new dependencies, no schema changes, no template changes. Existing producer-chain tests in `test_failure_chains.py` already exercise the surrounding plumbing and will not need modification. Concepts mid-iteration continue to work unchanged.

Rollout: one PR, mergeable in isolation. No flag staging, no feature toggle.

---

## Validation Approach

**Manual smoke test** after implementation:

1. Pick a concept with an existing `analysis.md` and at least one iter (e.g., 28-hts-tokamak-full-hts post-cleanup).
2. Write a CR with `VERDICT: FINDINGS` + one `Category: model` finding asking for a specific param change.
3. Run `analyze <id> --feedback path/to/cr.md`.
4. Verify: new `iter-N/pre_feedback.md` byte-equals the CR; `model_setup.py` reflects the requested param change; `iter-N/post_feedback.md` exists; source CR file is unchanged.
5. Re-run with `--add-passes 2`: verify iter-(N+1) consumes iter-N's `post_feedback.md`, not the CR again.

**Failure-mode smoke tests:**

- `--feedback /nope` → exits 1, error names the missing path.
- `--feedback <empty>` → exits 1, error mentions empty file.
- `--feedback <no-verdict>` → exits 1, error from `validate_feedback_verdict.fix_message`.
- `--feedback <no-Category>` → exits 1, error from `validate_feedback_verdict.fix_message`.
- `--feedback <pass>` (`VERDICT: PASS` only) → accepted, runs a no-op iteration.
- `--feedback <path> --force` → exits 1 with new message.
- `--feedback <path>` on concept with no `analysis.md` → exits 1, error mentions cold-start.

**Regression**: existing `test_failure_chains.py`, `test_staleness.py`, `test_validators.py` should pass unchanged.

---

## Next-Stage Handoff

**Fixed (plan should not revisit):**
- Producer branch placement at top of the cascade.
- Reuse of `validate_feedback_verdict` and `_copy_to_pre_feedback` — no new helpers.
- Validation in `cmd_analyze`, not in the loop.
- Implicit-resume promotion.
- `_apply_external_feedback` deleted, not refactored.

**Open (plan should sequence):**
- Whether to land argparse help text + README in one PR with the code, or split. Recommendation: one PR — the docs are part of the contract.
- Whether to add a new unit test for the external-feedback branch in `test_failure_chains.py` or a new test file. Plan stage decides; either is fine.

**De-risk first:** the validation guard ordering in `cmd_analyze`. Getting the order right (size check before parse check; analysis.md check after concept resolution) avoids index-error-style bugs that the existing test suite probably wouldn't catch.

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`.
