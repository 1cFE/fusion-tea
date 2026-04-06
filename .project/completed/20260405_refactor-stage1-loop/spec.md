# Spec: Stage 1 Loop Refactor (Work Item #2)

**Status:** Complete
**Owner:** reid
**Created:** 2026-04-05
**Complexity:** MEDIUM
**Branch:** design-space-explore
**Depends on:** `.project/active/refactor-run-analysis/` (Work Item #1 — code cleanup)

---

## Business Goals

### Why This Matters

Today the analyze command is a binary choice: `--force` (start over) or skip. If you run 2 iterations and the analysis converges but you later want to add 2 more with `--research` enabled, or after manually adding a new source, there's no way to continue from where you left off. You either wipe the slate or do nothing.

Additionally, `stage1-all` currently runs a pipeline of `analyze → model-setup → review`, but model-setup only runs *after* the analyze loop exits. This means the autonomous quality loop (assess) never evaluates the model — only the prose analysis. Moving model-setup inside the loop means each iteration produces both an analysis and a model, and the assess step evaluates both.

Finally, the autonomous-source-acquisition spec (FR-A3) needs a clean extension point between ASSESS and ANALYZE in the loop. Today that would mean adding another branch to the 270-line `cmd_analyze`. This refactor gives the research step a natural slot instead.

### Success Criteria

- [ ] `--resume` adds iterations to an existing analysis without restarting, regardless of whether the prior iteration's verdict was PASS, FAIL, or interrupted.
- [ ] `--research` enables an autonomous research pre-step on iterations after the first, which plugs in cleanly (not a branch in cmd_analyze).
- [ ] model-setup runs inside the loop so the assess step can evaluate the model alongside the analysis.
- [ ] Existing 36 concept directories are migrated to the new layout via a one-shot script.
- [ ] `update-analysis` is replaced by `source add` + `stage1-all --resume`, which uses the source-integration prompt as its feedback-producer for the first resumed iteration.

### Priority

Prerequisite for autonomous-source-acquisition. Direct improvement to the day-to-day analysis workflow via `--resume`.

---

## Problem Statement

### Current State

- `cmd_analyze` (270 lines) inlines the assess↔analyze loop as a `for` statement with four branches (cold-start, feedback-mode, `--feedback` flag, and the assess loop itself).
- Iteration artifacts are flat files in the concept root: `analysis_prompt_iter_1.md`, `feedback_iter_1.md`, `assessment_prompt_iter_1.md`. There is no per-iteration directory, no structured verdict file, and no way to query "which iteration am I on" without counting files.
- `model_setup` runs after the loop exits via `stage1-all`. The assess step never sees the model.
- `update-analysis` (150 lines) duplicates the feedback-pass wiring to inject new sources. Its behavior is opaque ("run a source-integration prompt, then a feedback-pass") and does not advance the iteration counter.
- The verdict (`VERDICT: PASS/FAIL`) is parsed from the assess output markdown via regex and not persisted structurally. `--resume` would need to re-parse this.

### Desired Outcome

- The stage1 loop is an explicit object with a per-iteration directory structure that records prompts, outputs, and verdicts.
- `--resume` reads the existing iteration state and starts the next iteration from where things left off.
- The loop body per iteration is: `[feedback-producer] → analyze(feedback-pass) → model-setup → assess`.
- The feedback-producer is **substitutable**: normal loop iterations use the prior assess output; post-source-add iterations use the source-integration prompt; future research iterations will use research findings. All three produce feedback in the same `config/feedback_format.md` schema (`VERDICT: PASS/FAIL` + `### F-N:` findings).
- `update-analysis` is replaced by `source add` + `stage1-all --resume`, which selects the source-integration prompt as the feedback-producer for the first resumed iteration. The `source_integration.md` template is preserved.
- Per-concept directory clutter is reduced: iteration artifacts live in `iter-N/`, non-iteration prompts move to `prompts/`.

---

## Scope

### In Scope

1. **`iter-N/` directory layout** — per-iteration subdirs under each concept's analysis dir.
2. **`prompts/` subdirectory** — non-iteration prompts moved out of concept root for cleanliness.
3. **`verdict.json`** — structured verdict file written at the end of each iteration, including which feedback-producer was used.
4. **`--resume` flag** on `stage1-all` (and `analyze` for backward compat) — continues from the last completed or interrupted iteration.
5. **Move model-setup inside the loop** — each iteration generates a model and runs it, so the assess step can evaluate model quality.
6. **Substitutable feedback-producers** — the analyze step's feedback-pass mode consumes feedback from a context-dependent producer (assess output, source-integration, or future research). All producers share the `config/feedback_format.md` output schema.
7. **Replace `update-analysis`** — its behavior becomes `source add` + `stage1-all --resume`, which auto-selects the source-integration prompt as feedback-producer when new sources are detected. The `source_integration.md` template is preserved.
8. **Research extension point** — a slot in the loop where a research step can be injected as another feedback-producer. This spec defines the slot; the autonomous-source-acquisition spec (FR-A3) defines what fills it.
9. **`--research` flag** — enables the research extension point on iterations > 1. (Stub/no-op until autonomous-source-acquisition is implemented.)
10. **Migration script** — reorganizes existing flat artifacts into `iter-N/` and `prompts/` subdirs for all 36 concepts.
11. **Update `get_concept_state`** — read `verdict.json` for richer state information (current iter, last verdict, whether loop is in progress).

### Out of Scope

- **Prompt template changes.** The analyze, assess, model-setup, and review prompts stay as-is. (Work Item #3 may change the review prompt.)
- **Human-facing review changes.** The `review` step stays outside the loop, unchanged. Work Item #3 rescopes it.
- **The autonomous research step itself.** This spec creates the slot; the autonomous-source-acquisition spec fills it. Until that lands, `--research` is accepted but no-ops.
- **Synthesize/approve changes.** Those are Work Item #3.
- **CLI verb consolidation** (14 → 6). The `analyze` and `stage1-all` commands keep their names. CLI simplification can happen later if desired.
- **New `run` / `step` / `source` top-level commands** from the original design doc.

### Edge Cases & Considerations

- **Interrupted iterations.** If the process dies mid-iteration (after analyze but before assess), `--resume` should detect the incomplete state (e.g., analysis output exists but no verdict.json) and re-run the iteration from the incomplete step, not start a new one.
- **model-setup failure inside the loop.** If model generation fails or the model produces no output, the loop should continue to the assess step anyway — the assess prompt already handles missing model context. The failure is logged in verdict.json.
- **Cold-start vs feedback-pass.** Iteration 1 uses the `cold_start` template mode. Iterations 2+ use `feedback_pass` mode consuming feedback from whatever producer ran. This is unchanged behavior, just made explicit.
- **Feedback-producer selection.** When resuming after `source add`, the loop must detect that new sources exist (sources not referenced in any prior iteration's prompt) and select the source-integration prompt as the feedback-producer for the first new iteration. Subsequent iterations within the same run revert to normal assess-driven feedback.
- **`--force` with `--resume`.** `--force` should mean "restart from iter-1, wiping prior iterations." `--resume` means "continue from where I left off." They are mutually exclusive.
- **`--max-passes` interaction.** `--max-passes 3` still means "at most 3 iterations." When resuming, the cap applies to the total iteration count, not the number of new iterations.  E.g., if 2 iterations exist and `--max-passes 4`, resume runs at most 2 more.
- **Backward compatibility of `analyze` command.** `analyze 02` without `--resume` should behave as today: skip if analysis.md exists, `--force` to restart. `analyze 02 --resume` adds iterations. This preserves the muscle memory of existing usage.
- **`source_paths` refresh.** After each iteration (and especially after a research step), `find_sources()` must be re-called so newly-added sources appear in the next analyze prompt. This is already called per-concept in the current code but not per-iteration.

---

## Requirements

### Per-Iteration Directory Layout

1. **FR-1:** Each iteration of the stage1 loop SHALL produce artifacts in `analyses/{concept_id}/iter-{N}/` where N is a 1-indexed integer.

2. **FR-2:** Each iteration directory SHALL contain at minimum:
   - `analyze_prompt.md` — the rendered prompt sent to Claude for the analyze step.
   - `analysis_output.md` — the raw body output from the analyze step (currently `analysis_body.md` for iter 1, implicit for feedback passes).
   - `assess_prompt.md` — the rendered prompt for the assess step.
   - `feedback.md` — the assess step's output (was `feedback_iter_N.md`).
   - `verdict.json` — structured verdict (see FR-3).
   - `model_setup.py` — the model script generated this iteration (see FR-6).
   - `model_output.txt` — model execution output (if model ran successfully).

3. **FR-3:** `verdict.json` SHALL contain at minimum:
   - `iteration`: integer.
   - `verdict`: `"PASS"` | `"FAIL"` | `"ERROR"` | `"INTERRUPTED"` | `"SINGLE_PASS"`.
   - `finding_count`: integer (number of `### F-N:` findings in feedback.md).
   - `model_ran`: boolean.
   - `model_ok`: boolean (false if model errored or missing LCOE).
   - `research_ran`: boolean.
   - `timestamp`: ISO 8601 datetime.

4. **FR-4:** The top-level `analyses/{concept_id}/analysis.md` SHALL continue to exist as the canonical analysis, rebuilt after each iteration from frontmatter + the latest `iter-N/analysis_output.md`. Downstream consumers (review, synthesize, approve) read this file and are unaffected by the iter-N layout.

5. **FR-5:** The top-level `analyses/{concept_id}/model_setup.py` and `model_output.txt` SHALL be copies (or symlinks) of the latest iteration's versions, so downstream consumers are unaffected.

### Model-Setup Inside the Loop

6. **FR-6:** Each iteration of the stage1 loop SHALL run model-setup after analyze and before assess. The assess step's prompt inputs SHALL include the model output path so the assessor can evaluate model quality alongside the analysis.

7. **FR-7:** Model-setup failure (generation failure or model execution failure) SHALL NOT abort the iteration. The assess step proceeds with whatever model context is available (possibly none). The failure is recorded in `verdict.json` (`model_ok: false`).

8. **FR-8:** [INFERRED] The assess prompt template MAY need a new `{{model_output_path}}` variable if it doesn't already have one. If the template change is trivial (adding one variable), it's in scope; if it requires a prompt redesign, defer to a separate work item.

### Resume Semantics

9. **FR-9:** `stage1-all` and `analyze` SHALL accept a `--resume` flag. When set:
   - The loop reads the existing `iter-*/` directories to determine the current iteration count and last verdict.
   - If the last iteration is incomplete (artifacts exist but no `verdict.json`), re-run that iteration from the first missing step.
   - If the last iteration is complete, start a new iteration (iter N+1) regardless of whether the last verdict was PASS or FAIL.
   - `--resume` does NOT require `--force`. It is a third mode alongside "skip if exists" (default) and "restart from scratch" (`--force`).

10. **FR-10:** `--resume` and `--force` SHALL be mutually exclusive. If both are passed, exit with an error message.

11. **FR-11:** `--max-passes` SHALL apply to the total iteration count when resuming. If `iter-2/` exists with verdict FAIL and `--max-passes 4` is set, resume runs at most 2 more iterations (3 and 4).

12. **FR-12:** When resuming, `find_sources()` SHALL be re-called before each iteration so any sources added since the last run are picked up by the analyze prompt.

### Research Extension Point

13. **FR-13:** The loop body SHALL have a defined extension point that runs *before* the analyze step on iterations > 1 (after the prior iteration's assess output is available). This is where the autonomous research step (from the autonomous-source-acquisition spec, FR-A3) plugs in.

14. **FR-14:** A `--research` flag SHALL be accepted by `stage1-all` and `analyze`. When enabled, the extension point is active. Until the autonomous-source-acquisition step is implemented, `--research` SHALL be accepted without error but produce a log message like "research step not yet implemented — skipping" and proceed.

15. **FR-15:** After the research extension point runs (when implemented), the loop SHALL re-call `find_sources()` and rebuild `source_paths` before invoking analyze, so newly-acquired sources appear in the prompt. (Overlaps with FR-12 but the timing is distinct: FR-12 is start-of-iteration, FR-15 is after-research-within-iteration.)

### Substitutable Feedback-Producers

16. **FR-16:** The loop SHALL support substitutable feedback-producers. On iterations > 1, the analyze step always runs in `feedback_pass` mode, consuming feedback from whatever producer ran. The feedback-producer is selected per-iteration based on context:

    | Context | Feedback-producer | Prompt template |
    |---|---|---|
    | Iter 1 (fresh) | *(none — cold start)* | `analysis_v2.md` with `cold_start=true` |
    | Iter 2+ (normal loop) | Prior iteration's **assess** output | `analysis_v2.md` with `feedback_pass=true` |
    | Iter after `source add` | **Source-integration** assessment of new sources | `source_integration.md` → then `analysis_v2.md` with `feedback_pass=true` |
    | Iter after research step | **Research findings** (future) | *(defined by autonomous-source-acquisition spec)* |

    All feedback-producers MUST output in `config/feedback_format.md` schema (`VERDICT: PASS/FAIL` + `### F-N:` findings). The analyze step does not care which producer generated the feedback.

17. **FR-17:** The `source_integration.md` prompt template SHALL be preserved and used as the feedback-producer when `--resume` detects new sources (sources present in `find_sources()` but not referenced in any prior iteration's analyze prompt). The source-integration step:
    1. Reads the new source documents and the existing `analysis.md`.
    2. Produces structured findings about what material information the new sources add.
    3. Writes its output to `iter-N/feedback.md` (same location as normal assess output).
    4. The analyze step then consumes this feedback in `feedback_pass` mode, same as any other iteration.

18. **FR-18:** The `update-analysis` CLI subcommand SHALL be removed. Its equivalent workflow becomes:
    1. `add-source <concept> <source>` (unchanged).
    2. `stage1-all <concept> --resume` — the loop detects new sources and selects the source-integration feedback-producer for the first new iteration.

19. **FR-19:** `verdict.json` SHALL record which feedback-producer was used for the iteration (`"feedback_source": "assess" | "source_integration" | "research" | "cold_start"`), so `--resume` can reconstruct context.

### Directory Cleanup

20. **FR-20:** Non-iteration prompt files (gap-check, review, synthesis, address-review prompts) SHALL be stored in a `prompts/` subdirectory under each concept's analysis dir, rather than at the concept root. This applies to:
    - `gap_check_prompt.md` → `prompts/gap_check_prompt.md`
    - `review_prompt.md` → `prompts/review_prompt.md`
    - `synthesis_prompt.md` → `prompts/synthesis_prompt.md`
    - `address_review_prompt.md` → `prompts/address_review_prompt.md`
    - `model_setup_prompt.md` → `prompts/model_setup_prompt.md` (for non-loop model-setup runs; inside the loop, model-setup prompts go in `iter-N/`)

21. **FR-21:** The concept root SHALL contain only canonical artifacts and directories:
    ```
    analyses/{concept_id}/
    ├── analysis.md              # canonical (rebuilt each iter)
    ├── model_setup.py           # latest model (copy from latest iter)
    ├── model_output.txt         # latest model output
    ├── gap_report.md            # gap check output
    ├── review.md                # human review
    ├── address_log.md           # address-review log
    ├── synthesis.md             # synthesis
    ├── iter-1/                  # iteration artifacts
    ├── iter-2/
    └── prompts/                 # non-iteration prompts
    ```

### Migration

22. **FR-22:** A one-shot migration script SHALL reorganize existing concept directories:
    - Move iteration artifacts into `iter-N/` subdirectories:
      - `analysis_prompt_iter_1.md` → `iter-1/analyze_prompt.md`
      - `feedback_iter_1.md` → `iter-1/feedback.md`
      - `assessment_prompt_iter_1.md` → `iter-1/assess_prompt.md`
      - (and similarly for iter 2, 3, etc.)
      - `analysis_body.md` (if still present) → `iter-1/analysis_output.md`
    - Move non-iteration prompts into `prompts/`:
      - `gap_check_prompt.md`, `review_prompt.md`, `synthesis_prompt.md`, `address_review_prompt.md`, `model_setup_prompt.md`, `analysis_prompt.md` (the pre-loop-era prompt) → `prompts/`
    - Move `update-analysis` artifacts into the appropriate `iter-N/` or `prompts/`:
      - `source_integration_prompt_*.md`, `feedback_update_*.md`, `update_analysis_prompt_*.md` → `prompts/` (these are audit-trail artifacts from prior runs)
    - `model_setup.py`, `model_output.txt` remain at concept root as canonical copies (FR-5).

23. **FR-23:** The migration script SHALL generate a `verdict.json` for each migrated iteration by re-parsing the `feedback_iter_N.md` verdict regex. If no feedback file exists for an iteration, verdict is `"INTERRUPTED"`.

24. **FR-24:** The migration script SHALL be idempotent — running it twice on the same concept directory produces the same result.

---

## Acceptance Criteria

### Resume

- [ ] `stage1-all 02 --resume` on a concept with 2 existing iterations starts iteration 3 without touching iter-1/ or iter-2/.
- [ ] `stage1-all 02 --resume` on a concept with a PASS verdict at iter-2 still starts iter-3 (user chose to continue).
- [ ] `stage1-all 02 --resume --max-passes 2` on a concept with 2 existing iterations exits cleanly with "max passes reached."
- [ ] `stage1-all 02 --resume` on a concept with an interrupted iter-2 (analysis exists, no verdict.json) re-runs iter-2 from the assess step.
- [ ] `analyze 02 --resume --force` exits with a clear error about mutual exclusivity.
- [ ] `analyze 02` (no --resume, no --force) on a concept with an existing analysis.md skips as before.

### Loop Structure

- [ ] Each iteration produces all expected files in `iter-N/`.
- [ ] `verdict.json` is written at the end of every iteration, including on error.
- [ ] `analysis.md` at concept root is always the frontmatter + latest iteration's body.
- [ ] `model_setup.py` at concept root matches the latest iteration's version.
- [ ] Model-setup failure does not abort the iteration — assess still runs, verdict.json records `model_ok: false`.

### Substitutable Feedback-Producers

- [ ] After `add-source 02 <path>` + `stage1-all 02 --resume`, the first new iteration uses the source-integration prompt as its feedback-producer (not the prior assess output).
- [ ] The source-integration findings appear in `iter-N/feedback.md` in the standard `config/feedback_format.md` schema.
- [ ] Subsequent iterations within the same run revert to normal assess-driven feedback.
- [ ] `verdict.json` records which feedback-producer was used (`feedback_source` field).

### Research Extension Point

- [ ] `stage1-all 02 --resume --research` runs without error, logs "research step not yet implemented — skipping", and proceeds normally.
- [ ] The code has a clear, documented place (function call, hook, or callback) where the autonomous-source-acquisition step will plug in, with a code comment referencing FR-A3.

### Directory Layout & Migration

- [ ] Migration script converts all 36 existing concept directories: iteration artifacts into `iter-N/`, non-iteration prompts into `prompts/`.
- [ ] Running migration twice is idempotent.
- [ ] Concept root contains only canonical artifacts and directories (per FR-21).
- [ ] `status` command works correctly before and after migration.
- [ ] `verdict.json` generated for each migrated iteration matches the regex-parsed verdict from the original feedback files.
- [ ] `update-analysis` artifacts (`source_integration_prompt_*.md`, `feedback_update_*.md`, `update_analysis_prompt_*.md`) are moved to `prompts/`.

### Backward Compatibility

- [ ] `analyze 02` (without --resume) still works as before: skip-if-exists or --force to restart.
- [ ] `stage1-all 02` (without --resume) still runs the full pipeline from scratch (or skips completed steps).
- [ ] All non-stage1 commands (review, address-review, synthesize, approve, status, list) are unaffected — they read from concept root (`analysis.md`, `review.md`, etc.) which is unchanged.
- [ ] Prompts rendered by the loop are identical to what the current code produces for the same inputs (verify via `--dry-run` on a test concept).

### Quality

- [ ] No file exceeds ~400 lines (building on Work Item #1's split).
- [ ] `update-analysis` subcommand removed from argparse and dispatch.

---

## Related Artifacts

- **Prereq:** `.project/active/refactor-run-analysis/spec.md` (Work Item #1 — code cleanup, must land first).
- **Design concept:** `.project/active/refactor-run-analysis/design-concept.md` — the broader vision. This spec implements the Loop primitive and iter-N layout from that doc, without the full Step/Pipeline abstraction.
- **Autonomous source acquisition:** `.project/active/autonomous-source-acquisition/spec.md` — the research step (FR-A3) that plugs into the extension point created here.
- **Research:** `.project/research/20260405-concept-analysis-refactor.md` — architecture review.
- **Follow-on:** Work Item #3 (final-stages rescope — human review kick-back, final approval gate).

---

**Next Steps:** After approval, proceed to `/_my_design` to work out the loop object's implementation shape and the migration script approach.
