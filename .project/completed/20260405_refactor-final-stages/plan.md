# Implementation Plan: Final Stages Rescope

**Status:** Draft
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/refactor-final-stages/spec.md`
- **Design:** `.project/active/refactor-final-stages/design.md` — see here for component details, code snippets, regex patterns, data flow

## Implementation Strategy

**Phasing Rationale:**
Prompt templates first (zero code risk, defines output format everything else depends on), then PROCEED-path plumbing (makes new verdicts functional), then REVISE kick-back (riskiest piece, needs PROCEED path as known-good baseline).

**No automated tests exist for this pipeline.** The pipeline is a headless Claude orchestrator — validation is manual (run commands, inspect output). The design's validation approach (section: "Validation Approach") defines the manual test matrix. Each phase includes the relevant subset.

---

## Phase 1: Prompt Templates

### Goal
Replace the review prompt, update assessment scope, relax feedback format config. After this phase, running `review` or `assess` will produce output in the new format — but the pipeline won't recognize the new verdict yet.

### Changes Required

**See `design.md#component-1` for full prompt structure, `#component-5` for assessment changes, `#component-6` for feedback format.**

#### 1. Review prompt rewrite
**File:** `exploration/concept_analysis/prompt_templates/review.md` (REWRITE)
- [x] Replace entire 144-line template with strategic review prompt from design Component 1
- [x] Include machine-parsed comments on VERDICT, Minor Fixes, and Corrective Actions headings
- [x] Add `{{model_output_path}}` and `{{approved_syntheses}}` template variables (these won't be populated yet — Phase 2 wires them up, but the template should reference them now so Phase 2 is just a code change)

#### 2. Assessment prompt update
**File:** `exploration/concept_analysis/prompt_templates/assessment.md`
- [x] Replace "What You Are NOT Checking" block (lines 37-46) with "Scope" block per design Component 5, Change 1
- [x] Replace model output conditional (lines 27-35) with strengthened version per design Component 5, Change 2
- [x] Remove "You are NOT checking numerical accuracy" from line 3 task description

#### 3. Feedback format config
**File:** `exploration/concept_analysis/prompt_templates/config/feedback_format.md`
- [x] Replace line 26-27 (numerical accuracy exclusion) with plausibility-focused rule per design Component 6

### Validation

**Manual:**
- [ ] Read all three updated templates — verify no broken Handlebars syntax (`{{#if}}`, `{{@config/...}}`)
- [ ] `review.md` references all template variables listed in design Component 1
- [ ] `assessment.md` still includes `{{@config/feedback_format.md}}` and `{{@config/assessment_checklist.md}}`
- [ ] `feedback_format.md` example section still valid

**What We Know Works After This Phase:**
Prompt templates are correct. Running `review` will produce new-format output (with VERDICT line), but `Review-Status` will be set to `has-actions` since the post-hook doesn't recognize VERDICT yet. That's expected — Phase 2 fixes detection.

---

## Phase 2: PROCEED Path Plumbing

### Goal
Wire up verdict detection, template variable injection, gates, and state detection. After this phase, the full PROCEED path works: review → optional address-review → synthesize → approve.

### Changes Required

**See `design.md#component-2` through `#component-3`, `#component-7` through `#component-10` for code snippets.**

#### 1. Verdict detection in post-hook
**File:** `exploration/concept_analysis/scripts/run_analysis.py:470-473`
- [x] Replace `review_status` detection block with new PROCEED/REVISE regex + legacy fallback per design Component 2
- [x] Preserve `Review-Iterations` and `Last-Review` updates (lines 474-478 unchanged)

#### 2. Template variable additions for cmd_review
**File:** `exploration/concept_analysis/scripts/run_analysis.py:456-468` (`_build_vars` closure)
- [x] Add `model_output_path` variable (model_output.txt path if exists, else empty string)
- [x] Add `approved_syntheses` variable using `find_approved_syntheses()` + `format_path_list()` (both already imported)
- [x] Compute `approved_syntheses` outside the closure (like `sources` on line 454), exclude current concept

#### 3. Address-review guard
**File:** `exploration/concept_analysis/scripts/run_analysis.py:515-517` (after `review_path.exists()` check)
- [x] Add `Review-Status: revise` guard per design Component 7 — print redirect message, `continue`

#### 4. Approve gate
**File:** `exploration/concept_analysis/scripts/run_analysis.py:757` (after already-approved check, before synthesis gate)
- [x] Add review gate: skip if `Review-Status` not in `("proceed", "addressed", "clean")` and not `--force`
- [x] Keep existing synthesis gate below it unchanged

#### 5. State detection update
**File:** `exploration/concept_analysis/scripts/lib/state.py:33`
- [x] Add `"proceed"` to the reviewed status set: `("addressed", "clean", "proceed")`

#### 6. Synthesize gate update
**File:** `exploration/concept_analysis/scripts/run_analysis.py:632`
- [x] Add `"proceed"` to the gate set: `("addressed", "clean", "proceed")`

### Validation

**Manual — PROCEED path:**
- [ ] Run `review <concept>` on a concept with analysis.md → verify `review.md` output has `VERDICT:` line
- [ ] Check `analysis.md` frontmatter: `Review-Status: proceed` (or `revise`)
- [ ] Check `Review-Iterations` incremented, `Last-Review` set
- [ ] If PROCEED with PA-N actions: fill decisions, run `address-review` → verify `Review-Status: addressed`
- [ ] Run `synthesize <concept>` → verify gate passes for `proceed` or `addressed`
- [ ] Run `approve <concept>` → verify new review gate + existing synthesis gate both pass

**Manual — Guards:**
- [ ] Run `address-review` on concept with `Review-Status: revise` → verify redirect message
- [ ] Run `approve` on concept without review → verify refusal message
- [ ] Run `approve --force` on same concept → verify override works

**Manual — Backward compat:**
- [ ] Run `synthesize` on concept with `Review-Status: addressed` (old format) → verify gate passes
- [ ] Run `approve` on concept with `Review-Status: clean` (old format) → verify gate passes
- [ ] Run `status` → verify concepts display correctly in all states

**What We Know Works After This Phase:**
Full PROCEED path is functional. Legacy concepts still work. The REVISE path sets `Review-Status: revise` correctly but can't kick back to stage1 yet — that's Phase 3.

---

## Phase 3: REVISE Kick-Back

### Goal
Add review as a feedback-producer in the stage1 loop. After this phase, REVISE verdicts trigger stage1 re-iteration with review corrective actions as feedback.

### Changes Required

**See `design.md#component-4` for full implementation, helpers, and contract.**

#### 1. New helper functions
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (top-level, after imports)
- [x] Add `_has_revise_status(analysis_path)` — reads frontmatter, returns `bool`
- [x] Add `_get_review_feedback(concept_dir)` — extracts F-N findings from review.md, returns `str | None`

#### 2. Feedback-producer selection
**File:** `exploration/concept_analysis/scripts/lib/loop.py:92` (init block) and `~111` (selection block)
- [x] Add `used_review_feedback = False` alongside `used_source_integration` on line 92
- [x] Insert review kick-back check at priority 2 (after cold_start, before source-integration) per design Component 4
- [x] Write feedback text to `iter_dir / "feedback.md"` in the caller (loop owns file I/O)

### Validation

**Manual — REVISE round-trip:**
- [ ] Start with a concept that has `Review-Status: revise` and a `review.md` containing `VERDICT: REVISE` + `### Corrective Actions` with F-N findings
- [ ] Run `stage1-all <concept> --resume`
- [ ] Verify: new `iter-N/feedback.md` created with content extracted from review.md
- [ ] Verify: `iter-N/verdict.json` has `"feedback_source": "review"`
- [ ] Verify: subsequent iterations fall through to assess (one-shot behavior)
- [ ] After convergence: run `review` again → verify `Review-Iterations` increments

**Manual — Edge cases:**
- [ ] REVISE review with no `### Corrective Actions` section → verify falls through to assess feedback
- [ ] REVISE review with `### Corrective Actions` but no F-N findings → verify falls through

**What We Know Works After This Phase:**
Full REVISE round-trip: stage1 → review(REVISE) → stage1 --resume → review(PROCEED) → address-review → synthesize → approve.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Prompt quality is the biggest unknown. If review output doesn't include a clear VERDICT line, Phase 2's regex won't match — but the legacy fallback defaults to `has-actions`, which is safe (blocks further progress until human intervenes).
- **Phase 2**: Multiple small changes across one file (run_analysis.py). Risk of typos in gate sets. Mitigate by testing each gate independently.
- **Phase 3**: Regex extraction of F-N from review.md is fragile. Mitigate by testing with a real REVISE review output before wiring into the loop.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Rewrote `prompt_templates/review.md` — 144-line numerical QA template → 124-line strategic review with VERDICT, Minor Fixes (PA-N), Corrective Actions (F-N) sections
- Updated `prompt_templates/assessment.md` — removed "NOT checking numerical accuracy" exclusion from task description and body, added "Scope" section with numerical plausibility checks, strengthened model output conditional to check LCOE plausibility and cost driver alignment
- Updated `prompt_templates/config/feedback_format.md` — replaced numerical accuracy exclusion rule with plausibility-focused guidance
**Issues:** None
**Deviations:**
- Review template uses `##` (h2) for top-level sections (Verdict, Minor Fixes, Corrective Actions) instead of `###` (h3) as shown in design Component 1. This is structurally correct (F-N/PA-N items use `###`, sections use `##`). Phase 3's `_get_review_feedback()` regex needs to match `^## Corrective Actions` instead of `^### Corrective Actions`.

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- `run_analysis.py:476-487` — verdict detection: PROCEED/REVISE regex with legacy `**Overall:** CLEAN` fallback
- `run_analysis.py:455-468` — added `model_output_path` and `approved_syntheses` template vars to `_build_vars`, computed outside closure excluding current concept
- `run_analysis.py:533-540` — address-review guard: skips with redirect message when `Review-Status: revise`
- `run_analysis.py:781-786` — approve review gate: requires `Review-Status` in `(proceed, addressed, clean)` or `--force`
- `run_analysis.py:655` — synthesize gate: added `"proceed"` to allowed set
- `lib/state.py:33` — added `"proceed"` to reviewed state set
**Issues:** None
**Deviations:** None — all changes match design exactly

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- `lib/loop.py` — added `_has_revise_status()` helper: checks `Review-Status: revise` in frontmatter
- `lib/loop.py` — added `_get_review_feedback()` helper: extracts corrective actions from `## Corrective Actions` section of review.md, returns formatted feedback text with `VERDICT: FINDINGS` header
- `lib/loop.py:93` — added `used_review_feedback = False` init flag
- `lib/loop.py:112-124` — inserted review kick-back at priority 2 in feedback-producer selection. One-shot via `used_review_feedback` flag, writes feedback.md directly, falls through to assess if no F-N findings extractable
**Issues:** None
**Deviations:**
- `_get_review_feedback()` regex uses `^## Corrective Actions` (h2) matching the actual review template output, not `^### Corrective Actions` (h3) as shown in design Component 4. This aligns with the Phase 1 deviation where the review template correctly uses h2 for sections.

---

**Status**: Complete
