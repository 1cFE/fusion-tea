# Design: feedback-dispatch file naming symmetry

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-25
**Updated:** 2026-04-25
**Branch:** pipeline-cleanup
**Commit:** f84b36a

---

## Overview

Rename the per-iteration feedback file from one ambiguous `feedback.md` (which means "input on entry, output on exit") into two temporally distinct files: `pre_feedback.md` (input to analyze) and `post_feedback.md` (output from assess). Every iteration > 1 gets both. The dispatch chain's only job becomes "produce `iter-N/pre_feedback.md`."

## Related Artifacts

- Spec: `.project/active/feedback-dispatch-symmetry/spec.md`
- Affected code (primary): `exploration/concept_analysis/scripts/lib/loop.py:115-178` (dispatch), `:703-774` (`_run_assess`), `:777-843` (`_run_source_integration`), `:293-333` (`_merge_feedback`), `:847-852` (`_get_prior_feedback`)
- Affected docs: `docs/concept-pipeline/actual-mechanics.md` (the "which `feedback.md` is which?" table), `docs/concept-pipeline/diagrams/dispatch.d2`
- Related work items (verified non-overlapping): `loop-dry-run-symmetry`, `model-feedback-starvation`, `power-standardization`

## Research Findings

**Dispatch chain** (`loop.py:115-178`) writes feedback files in three of five cases under three different conventions:
- Case 2: extracted text → `iter-N/feedback.md` (collides with assess output written ~600 lines later)
- Case 3: `_run_source_integration` → `iter-N/source_integration_output.md` (no collision)
- Case 4: `_merge_feedback` → `iter-N/feedback.md` (collides with assess output)
- Cases 1 and 5 write nothing.

**Assess output** (`loop.py:717`): `_run_assess` always writes `iter-N/feedback.md`. In Cases 2 and 4 this overwrites the input file written at the start of the same iteration — the input bytes are lost after iteration completion.

**Cross-iteration handoff** (`loop.py:847-852`): `_get_prior_feedback` reads `iter-(N-1)/feedback.md`. This is the only consumer of "what assess wrote in iter N-1" inside the dispatch.

**Existing artifact inventory** (38 concepts, ~100-200 iter dirs total): every iter-N/ contains `feedback.md` (assess output). About a third also contain `source_integration_output.md`. None contain a separate input-feedback artifact today.

**Template references**: `analysis_v2.md`, `assessment.md`, `source_integration.md` use a `{{feedback_path}}` template variable. The variable is filled at render time with whatever absolute path the loop computes — none of the templates hardcode the filename, so the rename does not require template edits.

**Tests**: `test_failure_chains.py` and `test_validated.py` create `feedback.md` files at synthetic paths. They construct the path explicitly each time; nothing is loaded from a real iter dir. So tests need a mechanical search-and-replace plus a few path constructions updated, not deeper changes.

**Staleness system** (`lib/state.py`): No references to `feedback.md` anywhere. The producer-clears-on-write contract is keyed off model/analysis files, not feedback files.

## Core Concept

**An iteration is a two-phase transaction**: it ingests a *pre-feedback* (what to react to) and emits a *post-feedback* (what was concluded). Today both phases share one filename. The fix is to give them different names that name the phase: `pre_feedback.md` and `post_feedback.md`.

Once that split exists, the dispatch chain has exactly one job — produce `iter-N/pre_feedback.md` — and the five cases become five strategies for populating it. Assess always writes `iter-N/post_feedback.md` and never overwrites anything. Every iter dir is a pure transcript: pre + post + supporting artifacts.

The split also removes the cross-iteration mutation smell: `iter-(N-1)/post_feedback.md` is read by Case 5 to materialize `iter-N/pre_feedback.md`, but nothing in iter-N modifies anything in iter-(N-1).

## Key Bets & Decisions

- **Pre/post naming over case-specific names.** Distinct names like `review_feedback.md` per case (the spec's Option B) communicate which case fired, but you have to memorize four filenames to know "this is the input." Pre/post communicates the temporal relationship in the name itself, which is the actual property operators care about. The case label still lives in `verdict.json` for anyone who needs it.

- **Rename `feedback.md` → `post_feedback.md` (expanding spec's out-of-scope).** Without renaming the assess output, the new `pre_feedback.md` would sit next to a file still called `feedback.md`, and readers would still ask "wait, which one is the new one?" The whole point is to make the temporal direction explicit, which requires symmetric names.

- **One-shot migration of the existing 38 concept dirs.** Alternative was dual-read code (try `post_feedback.md`, fall back to `feedback.md`) living in `_get_prior_feedback`, tests, and the migration script. That's permanent debt for a one-time pain. The migration is mechanical (rename one file in each `iter-N/`), runs in seconds, and ships in the same change with `--dry-run` first.

- **Case 5 copies prior post-feedback into current iter's pre-feedback.** Strict symmetry — `ls iter-N/` always answers "what fed me?" by showing `pre_feedback.md`. Disk cost is negligible (~5 KB × few hundred iters = tens of MB). Symlinks would avoid the copy but introduce cross-platform fragility for no real win.

- **Keep raw producer artifacts (`source_integration_output.md`, `research_output.json`) alongside `pre_feedback.md`.** They have distinct semantic value: producer artifacts are "what the producer wrote, untouched," while `pre_feedback.md` is "what was actually fed to analyze (possibly merged with carried-forward findings)." Separating them keeps the merge step's effect inspectable on disk.

- **Dispatch chain keeps five cases.** The asymmetry being fixed is in *output convention*, not in *control flow*. The cases still have genuinely different triggers and producers; collapsing them is an unrelated concern.

## Architecture

### Per-iter directory layout (post-change)

```
iter-N/
├── analyze_prompt.md
├── pre_feedback.md            ← NEW: input to analyze (iter > 1 only)
├── analysis_output.md
├── model_setup_prompt.md
├── model_setup.py
├── model_output.txt
├── source_integration_prompt.md   (only if Case 3 or 4 fired)
├── source_integration_output.md   (only if Case 3 or 4 fired — raw producer artifact, kept)
├── research_prompt.md             (only if Case 4 fired)
├── research_output.json           (only if Case 4 fired)
├── assess_prompt.md
├── post_feedback.md           ← RENAMED from feedback.md: assess output (always)
├── verdict.json
└── validation_log.json
```

### Per-case behavior under the new convention

| Case | Trigger | What gets written to `iter-N/pre_feedback.md` |
|------|---------|------------------------------------------------|
| 1 (cold start) | iter 1, no resume | (none — no `pre_feedback.md`) |
| 2 (review kick-back) | `Review-Status: revise`, one-shot | text extracted from `review.md` |
| 3 (source-integration) | new sources detected, one-shot | bytes copied from `source_integration_output.md` |
| 4 (research+merge) | `--research`, iter > 1, sources acquired | `_merge_feedback(prior post_feedback, source_integration_output)` |
| 5 (default) | else, iter > 1 | bytes copied from `iter-(N-1)/post_feedback.md` |

The dispatch's logical shape becomes:

```python
def _populate_pre_feedback(...) -> tuple[str, Path | None]:
    """Returns (feedback_source_label, pre_feedback_path or None for cold start)."""
    pre = iter_dir / "pre_feedback.md"
    # five-case chain, each branch writes pre and returns ("label", pre)
    # cold-start returns ("cold_start", None)
```

`_run_feedback_pass` then receives `pre` as its `feedback_path` argument — no signature change.

### Cross-iteration handoff (`_get_prior_feedback`)

Becomes a thin one-line read of `iter-(N-1)/post_feedback.md`. Used in two places after the change:
- Case 5: copy bytes to `iter-N/pre_feedback.md`.
- Case 4: pass to `_merge_feedback` for "carried-forward findings" semantics.

### Migration script

A new script (`scripts/migrate_feedback_filenames.py`, modeled on the existing `migrate_iterations.py`) walks every `analyses/*/iter-*/` and renames `feedback.md → post_feedback.md`. Idempotent (skips if `post_feedback.md` already exists), supports `--dry-run`, and ships with the code change so the rename happens atomically with the code that depends on it.

## Required Invariants

1. **`iter-N/post_feedback.md` is immutable after assess writes it.** Nothing else in the codebase ever writes to that path.
2. **`iter-N/pre_feedback.md` is written at most once per iteration.** Created at the start; never touched again. Absence implies cold start.
3. **For every iter N > 1 in a completed run, both `pre_feedback.md` and `post_feedback.md` exist.** The producer-clears-on-write contract for analysis/model files is unchanged and operates independently.
4. **`feedback_source` in `verdict.json` continues to be the authoritative case label.** The on-disk file shape is now consistent enough that operators rarely need it, but it remains the source of truth.
5. **Producer artifacts (`source_integration_output.md`, `research_output.json`) are not modified by the merge/copy that produces `pre_feedback.md`.** They remain the untouched record of what each producer step wrote.

## Component Overview

- **`_populate_pre_feedback` (new, replaces inline dispatch in `run_stage1_loop`)** — `lib/loop.py`. The dispatch chain extracted into a helper so it can be tested independently. Returns `(feedback_source_label, pre_feedback_path | None)`.
- **`_run_assess` — same signature, output path renamed.** `lib/loop.py:703-774`. One-line change: `feedback_path = iter_dir / "post_feedback.md"`. Validation, parsing, and verdict logic unchanged.
- **`_run_source_integration` — unchanged.** Still writes `source_integration_output.md`. The dispatch (not this function) decides whether/how to copy bytes into `pre_feedback.md`.
- **`_merge_feedback` — `output_path` argument now points at `pre_feedback.md`.** Internals unchanged.
- **`_get_prior_feedback` — body becomes `iter-(N-1)/post_feedback.md`.** One-line change, signature preserved.
- **`scripts/migrate_feedback_filenames.py` (new)** — one-shot rename script for existing 38 concept dirs.
- **`actual-mechanics.md`** — "So which `feedback.md` is which?" section is rewritten as a one-paragraph rule plus a small per-case table that shows where the *content* originates (review extract / source-integration / merge / prior post-feedback) — every row points at the same path: `iter-N/pre_feedback.md`.
- **`dispatch.d2`** — diagram artifact tags renamed `feedback.md → pre_feedback.md`. Single-arrow output convention rather than per-case different artifact labels.

## Non-Goals

- Changing dispatch priority order or the gate conditions for any case.
- Changing whether Case 2 merges with prior post-feedback (the asymmetry-with-Case-4 question is real but is its own design discussion).
- Changing `verdict.json` schema, `--resume` semantics, or `--add-passes` behavior.
- Changing template file contents (`analysis_v2.md`, `assessment.md`, `source_integration.md`) — they reference `{{feedback_path}}`, which the loop fills in.
- Touching the staleness propagation system.
- Renaming `source_integration_output.md` or `research_output.json` (those *are* producer artifacts; the new `pre_feedback.md` is the input-to-analyze artifact, distinct concept).

## Implementation Notes

- **Migration ordering**: the migration script must run *before* the new code is merged into a running pipeline, OR `_get_prior_feedback` needs a transitional fallback. Simplest path: ship migration + code change in one commit, run migration as part of the deploy step. Existing concept dirs are completed runs; no concurrent writers.
- **Test updates**: `test_failure_chains.py` and `test_validated.py` build synthetic `feedback.md` paths in tmpdirs. Mechanical replace `feedback.md → post_feedback.md` for assess-output paths and `feedback.md → pre_feedback.md` for input paths. ~30 occurrences total based on grep.
- **`migrate_iterations.py`** has its own constant `"feedback_iter_{n}.md": "feedback.md"`. That's an unrelated migration (pre-iter-N layout → iter-N layout). Update its target to `post_feedback.md` so the legacy migration produces the new convention if anyone ever re-runs it on archived data.
- **Diagrams**: `dispatch.d2` uses different "out:" labels per case today. New shape: every case's `out:` label is `pre_feedback.md` (or absent for cold start). Forces a small visual restructure but matches the simpler rule.
- **The existing CLI flag `--feedback <path>`** in `_apply_external_feedback` (`run_analysis.py:389-433`) accepts an arbitrary external feedback file. That code path does not touch the iter dir convention and is unaffected.

## Potential Risks

- **Mid-flight runs during deploy**: If someone is mid-`analyze --resume` when the new code lands, the in-progress iter dir has a `feedback.md` that the new code won't recognize as `post_feedback.md`. Mitigation: migration script renames everything at deploy time, including any partially-completed `iter-N/feedback.md`. Risk window is the few seconds between code merge and migration run; acceptable since this is solo dev.
- **Test path changes are easy to miss**: ~30 occurrences across two test files. Mitigation: a `grep -r "feedback\.md"` over `scripts/` after the change should return zero matches in non-test code and only producer-clears-on-write semantics in test files (now both renamed).
- **Migration script edge cases**: an `iter-N/` that already has a `post_feedback.md` (e.g., partial dev experiment) should be skipped, not error. Migration script must be idempotent.
- **Documentation drift**: `actual-mechanics.md` has many cross-references to `feedback.md`. Search-and-replace is mechanical but tedious. Mitigation: include doc updates in the same commit; reviewer reads the final doc end-to-end.

## Integration Strategy

Single PR with three commits, in order:

1. **Migration script** (`scripts/migrate_feedback_filenames.py`) — adds the script, tested with `--dry-run` against current state. No code path uses the new names yet.
2. **Code rename** (`lib/loop.py` and tests) — switches `_run_assess` to write `post_feedback.md`, dispatch to write `pre_feedback.md`, `_get_prior_feedback` to read `post_feedback.md`. Tests updated. Run migration script as the first step in this commit's deployment.
3. **Doc rewrite** (`actual-mechanics.md` + diagrams) — collapses the per-case table into the new single rule.

The PR can be reviewed by reading commit (2) end-to-end against the spec's success criteria.

## Validation Approach

**Smoke test (per spec acceptance criteria)**: Run `analyze NN --add-passes 1 --dry-run` on three concepts in different states:
- One with `Review-Status: revise` (triggers Case 2)
- One with new source files added since last iter (triggers Case 3)
- One in steady-state (triggers Case 5)

For each, inspect the saved `analyze_prompt.md` and verify it references the expected `pre_feedback.md` path.

**Disk inspection**: After a real (non-dry-run) iteration completes:
- `iter-N/pre_feedback.md` exists for iter > 1, contents match the case's expected source.
- `iter-N/post_feedback.md` exists, contains assess's `VERDICT:` line.
- The two files are not byte-identical (when Case 5 fired and assess produced findings).

**Migration script verification**: Before merge, run `migrate_feedback_filenames.py --dry-run` and confirm the output lists ~100-200 renames with no errors. Run the actual migration in a worktree first; diff against original tree to verify only renames happened.

**Existing tests**: `uv run python -m pytest exploration/concept_analysis/scripts/` should pass after test path updates with no semantic changes.

## Next-Stage Handoff

**Fixed for the plan phase:**
- Filenames: `pre_feedback.md` (input) and `post_feedback.md` (output).
- Migration approach: one-shot rename script, no dual-read code.
- Case 5 strategy: copy prior `post_feedback.md` into current `pre_feedback.md`.
- Producer artifacts (`source_integration_output.md`, `research_output.json`) stay alongside `pre_feedback.md`.
- Three-commit PR shape (migration script, code rename, doc rewrite).

**Open / for the plan to resolve:**
- Whether to extract the dispatch chain into `_populate_pre_feedback` helper or refactor inline. (Lean: extract, since it makes testing the rule easier.)
- Whether the migration script should also rewrite any internal references inside completed iter artifacts (e.g., a stale `feedback.md` path string in an old `analyze_prompt.md`). Lean: no — those are historical transcripts, prompts already point at the right path at *render* time.

**De-risk first:** the migration script. Build it and run `--dry-run` against current state before touching `loop.py`. If the dry-run output looks wrong (unexpected file matches, weird counts), the rest of the plan is suspect.

---
Next Step: After approval → `/_my_plan` for phased implementation.
