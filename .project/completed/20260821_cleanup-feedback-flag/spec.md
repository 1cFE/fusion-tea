# Spec: Cleanup `--feedback` Flag (Custom Feedback as Iteration Input)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17 09:17 PDT
**Complexity:** LOW
**Branch:** main

---

## Work Item Summary

Replace the current `--feedback PATH` behavior in `scripts/run_analysis.py` with a clean implementation that injects the user-supplied file as `iter-N/pre_feedback.md` and runs the normal iteration loop (analyze → model_setup → assess) end-to-end. The existing implementation runs an analysis-only patch that silently desynchronizes `analysis.md` from `model_setup.py`. After this change, `--feedback` is just "use this file in place of the prior iter's post_feedback as the next iteration's input" — same semantics, same downstream stages, no special path.

## Why This Matters Now

We just hit the footgun on concept 28-hts-tokamak-full-hts: a change request asking for `structure_t`/`vessel_t` updates and a sensitivity sweep was applied to `analysis.md` only. The downstream model_setup regeneration never saw the change request (it consumed the prior iter's auto-assessor `post_feedback.md` instead), so `model_setup.py` is now inconsistent with the prose. Every future use of `--feedback` carries this same risk. The custom-feedback use case is real and recurring — the implementation just routes it through the wrong code path.

## Key Bets / Constraints

- **Bet:** The existing iteration loop in `lib/loop.py` (the producer pattern that builds `pre_feedback.md` from one of five sources) is the right abstraction. `--feedback` should be a sixth producer, not a parallel pipeline.
- **Constraint:** Feedback file format stays as defined in `prompt_templates/config/feedback_format.md` (VERDICT line + F-N findings).
- **Constraint:** Pre/post feedback semantics do not change. `pre_feedback.md` is iteration input; `post_feedback.md` is the assess stage's output transcript.
- **Non-goal:** Do not redesign the iteration loop, stage prompts, or model_setup edit-mode rules.
- **Non-goal:** Do not change the `cmd_model_setup` subcommand's separate `--feedback` flag at `run_analysis.py:1512`. That is a stage-targeted concern outside this spec's scope.

---

## Business Goals

### Why This Matters

The pipeline's value proposition is "iterate a concept to convergence with feedback driving each pass." When a user wants to inject their own findings — e.g., from a cross-concept audit, a domain review, or a targeted change request — they expect the whole iteration to act on that feedback, not just the prose. The current `--feedback` flag violates that expectation silently: it produces a working state where the analysis describes one model and the code implements another, and the user cannot tell from a successful pipeline run that drift occurred. Eliminating that footgun restores trust in the tool and removes the need for the two-step Step-A/Step-B workaround in the README.

### Success Criteria

- [ ] A single command `analyze <id> --feedback PATH` runs a full iteration whose downstream artifacts (model_setup.py, post_feedback.md) reflect the supplied findings.
- [ ] No silent drift between `analysis.md` and `model_setup.py` after a `--feedback` run.
- [ ] The README documents one invocation pattern, not two.
- [ ] Concept 28's specific failure mode (analysis claiming values the model doesn't have) is not reachable with the new flag.

### Priority

Small, isolated cleanup. Tooling-level. Not blocking concept analysis work in progress, but the next time anyone uses external feedback on a concept they will hit the same bug, so worth doing soon. No external dependencies.

---

## Problem Statement

### Current State

`--feedback PATH` on the `analyze` subcommand (`run_analysis.py:301-320`) routes to `_apply_external_feedback` (`run_analysis.py:401-479`), which:

1. Runs only the analyze stage with the analysis template in `feedback_pass=true` mode.
2. Marks downstream artifacts (`model_setup.py`, `synthesis.md`, explorer JSON) stale via `propagate_staleness`.
3. Renames the user's source file to `change_requests_<timestamp>.md` (auto-archive).
4. Does not write `iter-N/pre_feedback.md`, does not run model_setup, does not run assess, does not increment iter.

Mutual-exclusion guards forbid combining `--feedback` with `--resume` or `--force`. To do a full iteration with external feedback, the documented workflow is two commands: Step A (`--feedback`) then Step B (`--resume --add-passes 1 --research`). Step B does not see the original feedback file (already archived) and the model_setup stage consumes whatever findings exist in the prior iter's `post_feedback.md` (which is the auto-assessor's output, not the user's CR). This produces the silent-drift failure mode demonstrated on concept 28-hts-tokamak-full-hts.

### Desired Outcome

`--feedback PATH` becomes a producer in the normal iteration loop. The user runs one command; the loop places the file at `iter-N/pre_feedback.md`; analyze, model_setup, and assess all consume that file the same way they consume any other `pre_feedback.md`. The user's source file is untouched on disk. No mutual-exclusion guards needed — `--feedback` composes naturally with `--resume`, `--add-passes`, and `--research`.

---

## Scope

### In Scope

- The `analyze` subcommand's `--feedback` flag in `scripts/run_analysis.py`.
- The iteration loop in `scripts/lib/loop.py` — adding a producer branch for external feedback.
- Removal of `_apply_external_feedback` and its supporting guards in `cmd_analyze`.
- README sections that document the current Step-A/Step-B workflow.

### Out of Scope

- The `cmd_model_setup` subcommand's separate `--feedback` flag (stage-targeted; unaffected).
- The feedback file format (VERDICT + F-N findings — unchanged).
- The producer-chain logic for review/source-integration/research/assess (unchanged).
- The stage prompt templates (`analysis_v2.md`, `model_setup_costingfe_edit.md`, `assessment.md`).
- The auto-assessor itself.
- Migrating any existing archived `change_requests_*.md` files in concept directories.

### Edge Cases & Considerations

- User supplies a path that does not exist, or points to an empty file, or points to a file that does not match the feedback format.
- User supplies `--feedback` with `--research` (research producer would normally fire — external feedback should take precedence and skip research for that iter).
- User supplies `--feedback` with `--add-passes N > 1` — only the first iter consumes the external file; subsequent iters consume the prior iter's `post_feedback.md` per normal chain.
- **Cold-start incompatibility**: `--feedback` operates in the analyze stage's feedback-pass mode, which edits an existing `analysis.md`. On a concept with no `analysis.md` yet, there is nothing to edit. `--feedback` is a mid-iteration tool, not an alternate cold-start. Reject the invocation rather than silently degrading.
- **`--force` incompatibility**: `--force` re-creates `analysis.md` from scratch (`run_analysis.py:308`) — same shape as cold-start. Reject `--feedback + --force` for the same reason.
- **Findings format must be model-actionable**: the model_setup edit-mode prompt only edits `model_setup.py` for findings tagged `Category: model`. A feedback file with a `VERDICT:` line but no findings, or findings without `Category:` tags, will produce the original drift bug in a new form (model_setup leaves things untouched even though the user expected model changes). Validation has to enforce this structurally, not just check for the `VERDICT:` header.
- Two concurrent `--feedback` invocations on the same concept (out of scope; existing pipeline does not guard against concurrent runs).
- A relative path passed to `--feedback`: resolve against CWD, not against the concept directory or `CONCEPT_ANALYSIS_DIR`.

---

## Requirement Selection Notes

The normative requirements below capture the user-visible contract of the new flag and the named failure modes. Three contract-level decisions are settled here rather than punted to design because each one shapes the user-visible behavior and could re-introduce the original drift bug if left ambiguous:

1. **Cold-start incompatibility (FR-6 (a))**: `--feedback` requires an existing `analysis.md`. Rejected over the alternatives ("layer findings on top of cold-start" — murky semantics; "undefined behavior" — weak) because feedback-pass mode in the analyze template structurally requires an existing analysis to edit. Making `--feedback` purely a mid-iteration tool matches the actual use case (audit, review, change request applied to a concept that has already been analyzed once).
2. **`--force` incompatibility (FR-5)**: Same reasoning. `--force` re-cold-starts the analysis, so `--feedback + --force` reduces to the cold-start case.
3. **Structural format validation (FR-6 (e))**: A `VERDICT:` line alone is not sufficient because the model-setup edit stage only edits `model_setup.py` when findings carry `Category: model` tags. A feedback file without well-formed `### F-N:` blocks would pass a shallow check, get accepted by analyze, and still produce silent model drift. Validation has to enforce findings structure, not just the header.

Implementation specifics (where in `loop.py` the branch sits, how `args` is threaded through, exact error message text, whether to use `shutil.copyfile` vs. read/write, exact regex/parser for finding validation) belong to design. The deletion of `_apply_external_feedback` is normative because preserving it would re-introduce the footgun.

---

## Requirements

### Functional Requirements

1. **FR-1**: When `--feedback PATH` is passed to `analyze`, the pipeline MUST copy the contents of `PATH` to `iter-N/pre_feedback.md` (where N is the iter the loop is about to run) before invoking the analyze stage.
2. **FR-2**: After `pre_feedback.md` is placed, the loop MUST run the standard sequence of stages (analyze, model_setup, assess) on that iter, exactly as it would if `pre_feedback.md` had been produced by any other producer.
3. **FR-3**: `--feedback` MUST take precedence over all other producers (review kick-back, source-integration, research, prior-assess copy) for the iter in which it is supplied. Subsequent iters in the same invocation revert to normal producer selection.
4. **FR-4**: The user-supplied source file at `PATH` MUST NOT be moved, renamed, deleted, or modified by the pipeline. The pipeline only reads it.
5. **FR-5**: `--feedback` MUST compose with `--resume` and `--add-passes N`. The current mutual-exclusion guard between `--feedback` and `--resume` (`run_analysis.py:303-305`) MUST be removed. `--feedback` MUST remain incompatible with `--force`: the guard at `run_analysis.py:306-310` stays, with an updated error message tying it to the cold-start precondition in FR-6 (a). When `--feedback` is combined with `--resume` and `--add-passes N`, the loop starts at the next iter after the latest existing iter and runs N passes; the external file is consumed on the first of those N iters only.
6. **FR-6**: The pipeline MUST fail fast with a clear, actionable error message before invoking Claude or creating any iter directory when:
   - (a) The concept has no existing `analysis.md` (cold-start state). `--feedback` is a mid-iteration tool and requires an analysis to edit.
   - (b) The supplied path does not exist.
   - (c) The supplied file is empty.
   - (d) The supplied file does not contain a `VERDICT:` line.
   - (e) The supplied file has `VERDICT: FINDINGS` but contains zero well-formed findings, where a well-formed finding is an `### F-N:` header followed by at least a `Category:` line whose value is `model` or `analysis`. A `VERDICT: PASS` file with no findings is allowed (it means "no changes needed" and is a no-op iteration).
7. **FR-7**: The existing `_apply_external_feedback` function and its analysis-only code path MUST be deleted. No callers should remain. The `--feedback`+`--resume` mutual-exclusion guard is removed; the `--feedback`+`--force` guard is retained per FR-5.
8. **FR-8**: [INFERRED] The README's documentation of the two-step Step-A/Step-B workflow for external feedback MUST be replaced with documentation of the single-command pattern, including the cold-start precondition (FR-6 (a)) and a note that any finding intended to change `model_setup.py` MUST carry `Category: model`.

### Non-Functional Requirements

- No regression in iteration timing characteristics beyond the trivial cost of one file copy.
- Existing pipeline tests that touch the producer chain (`test_failure_chains.py`, `test_staleness.py`, `test_validators.py`) MUST continue to pass; new tests covering FR-1, FR-4, FR-6 SHOULD be added in the design/implement stages.

---

## Acceptance Criteria

### Core Functionality

- [ ] Running `uv run python scripts/run_analysis.py analyze <id> --feedback PATH` on a concept with existing `analysis.md` produces a new `iter-N/` directory in which `pre_feedback.md` is byte-equal to the supplied PATH file, and `analysis.md`, `model_setup.py`, and `iter-N/post_feedback.md` have all been regenerated.
- [ ] Running `--feedback PATH --add-passes 3` runs 3 iterations: the first uses the supplied file; iters 2 and 3 use the standard prior-assess chain. After the run, the first new iter's `pre_feedback.md` equals the supplied file, and each subsequent iter's `pre_feedback.md` byte-equals the previous iter's `post_feedback.md`.
- [ ] After any `--feedback` run, the source file at PATH exists on disk, unmodified.
- [ ] Reproducing the concept-28 scenario (a change request with `Category: model` findings specifying model parameter changes) results in a `model_setup.py` whose code reflects those changes — analysis-vs-model drift does not occur.

### Failure Modes (all exit non-zero before invoking Claude and before creating any iter directory)

- [ ] `--feedback PATH` on a concept with no existing `analysis.md` errors with a message stating that `--feedback` requires a prior analysis and pointing the user at cold-start (no `--feedback`).
- [ ] `--feedback PATH --force` errors with a message stating `--feedback` and `--force` are incompatible because `--force` re-cold-starts the analysis.
- [ ] `--feedback /nonexistent/path` errors with a message naming the missing path.
- [ ] `--feedback /path/to/empty/file` errors with a message indicating the file is empty.
- [ ] `--feedback /path/to/file/without/verdict` errors with a message indicating the file does not contain a `VERDICT:` line.
- [ ] `--feedback /path/to/findings/file/without/category/tags` (a `VERDICT: FINDINGS` file whose `### F-N:` blocks are missing `Category:` lines) errors with a message indicating findings must be `Category:`-tagged so downstream stages know whether to edit `model_setup.py`.
- [ ] `--feedback /path/to/verdict/pass/file` (VERDICT: PASS, no findings) is accepted and runs a no-op iteration without error.

### Quality & Integration

- [ ] Existing tests in `exploration/concept_analysis/scripts/` continue to pass.
- [ ] `_apply_external_feedback` no longer exists in the codebase; `grep _apply_external_feedback scripts/` returns no matches.
- [ ] README no longer references the Step-A/Step-B workflow for external feedback.

---

## Next-Stage Handoff

**Settled in this spec:**
- `--feedback` is a producer in the iteration loop, not a separate code path.
- The supplied file is read-only from the pipeline's perspective.
- Composes with `--resume` and `--add-passes`. Incompatible with `--force` and incompatible with cold-start (no `analysis.md`).
- Validation enforces presence of a `VERDICT:` line and (when verdict is `FINDINGS`) at least one well-formed `### F-N:` block with a `Category:` line — strong enough that the model-setup edit stage will actually edit `model_setup.py` when the user intends model changes.
- All validation errors fail before invoking Claude and before creating any iter directory.

**Design must figure out:**
- Where in `lib/loop.py` to place the external-feedback branch (before or after the review kick-back check; how it interacts with the `merged_assess` merge logic used by the research path).
- How to thread `args.feedback` through to `run_loop` (currently the flag lives on `cmd_analyze` and is consumed only by `_apply_external_feedback`).
- Whether validation lives in `cmd_analyze` (early reject) or inside the new producer branch (closer to the consumer). Recommendation: cmd_analyze, so failures happen before any iter directory is created.
- Whether to add a one-line log/print announcing "external feedback consumed from PATH" alongside the existing `feedback_source=...` lines so the user can see in stdout that their file was used.

**Watch-outs for design:**
- The `--research` producer normally fires when `getattr(args, "research", False) and iter_num > 1`. External feedback must short-circuit this for its iter only — research should not run on the iter that consumes the user's file (the user's findings are already the input).
- `propagate_staleness` is called by `_apply_external_feedback` today. The new producer does not need to call it explicitly because the normal loop regenerates downstream artifacts anyway, but design should verify this with a smoke test.
- The mutual-exclusion guards for `--feedback` + `--resume` and `--feedback` + `--force` (`run_analysis.py:303-310`) need to be removed cleanly without breaking the help text or argparse setup.

---

## Related Artifacts

- **Research:** `.project/research/20260517-081444_model-setup-inconsistencies.md` — the audit that surfaced the concept-28 drift via a real external-feedback workflow.
- **Design:** `.project/active/cleanup-feedback-flag/design.md` (to be created)
- **Affected source files:**
  - `exploration/concept_analysis/scripts/run_analysis.py` (cmd_analyze, _apply_external_feedback, argparse)
  - `exploration/concept_analysis/scripts/lib/loop.py` (producer chain)
  - `exploration/concept_analysis/README.md` (workflow docs)

---

**Next Steps:** After approval, proceed to `/_my_design`.
