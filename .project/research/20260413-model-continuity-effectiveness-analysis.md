---
date: 2026-04-13T10:07:35-07:00
researcher: Claude
topic: "Effectiveness of model-feedback-starvation / analysis loop symmetry changes on iter-6/7"
tags: [research, pipeline, model-continuity, feedback-starvation, template-bug]
status: complete
last_updated: 2026-04-13
---

# Research: Effectiveness of Loop Symmetry Changes on Iterations 6-7

**Date**: 2026-04-13T10:07:35-07:00
**Researcher**: Claude
**Research Type**: Pipeline Effectiveness Analysis

## Research Question

How effective are the changes specified in `.project/active/model-feedback-starvation/spec.md` (feedback starvation fix, model continuity/edit-not-rewrite, stage1-all removal) as observed in iterations 6-7 of concepts 13, 16, and 17b?

## Summary

- **Model continuity is undermined by a template engine bug.** `lib/templating.py:37-42` uses a non-greedy regex for `{{#if}}...{{/if}}` that cannot handle nesting. The model-setup templates nest `{{#if model_feedback}}` inside `{{#if feedback_pass}}` and `{{#if cold_start}}`. The regex matches the outer open to the inner close, orphaning the outer `{{/if}}` and leaking the entire cold-start instruction block into feedback-pass prompts.
- **2 of 3 concepts regressed in iter-7.** Concept 13 dropped viable-conservative scenario + component-level alpha scaling. Concept 16 dropped heat sales sensitivity sweep. Both assessors immediately re-raised the dropped features.
- **Concept 17b showed no regression**, but its iter-6 had no model-targeted findings — the model agent had nothing complex to juggle, so the contradictory instructions had less opportunity to cause damage.
- **Feedback starvation fix**: Working — all findings visible in prompts.
- **stage1-all removal**: Clean.

## The Bug

### Template engine cannot nest conditionals

`lib/templating.py:37-42`:
```python
result = re.sub(
    r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
    replace_conditional,
    result,
    flags=re.DOTALL,
)
```

The `.*?` non-greedy quantifier matches the nearest `{{/if}}`. With nested blocks:

```
{{#if feedback_pass}}       ← outer open
  ...edit instructions...
  {{#if model_feedback}}    ← inner open
  ...findings...
  {{/if}}                   ← regex matches outer open → HERE
  ...
{{/if}}                     ← orphaned, becomes literal text

{{#if cold_start}}          ← outer open
  ...write-from-scratch instructions...
  {{#if model_feedback}}    ← inner open
  ...findings...
  {{/if}}                   ← regex matches outer open → HERE
  ...
{{/if}}                     ← orphaned, becomes literal text
```

When `feedback_pass=true` and `cold_start=""`:
1. The regex matches `{{#if feedback_pass}}` to the inner `{{/if}}` inside the feedback_pass block — emits the edit instructions + findings, but the remaining lines of the feedback_pass block (Reference Files, Output) plus the literal `{{/if}}` leak through.
2. The regex matches `{{#if cold_start}}` to the inner `{{/if}}` inside the cold_start block — `cold_start` is empty, so this inner portion is stripped. But everything after that inner `{{/if}}` up to the orphaned outer `{{/if}}` leaks through as literal text.

### What the model agent actually sees

Confirmed by inspecting rendered prompts (`iter-7/model_setup_prompt.md`) for concepts 13 and 16:

- **Lines 1-15**: Correct feedback-pass instructions ("Edit Existing Model", "Preserve ALL existing sweeps", "do NOT rewrite from scratch")
- **Line 83**: `Follow the MagLIF exemplar's 5-layer structure adapted for {concept}` (cold-start leak)
- **Line 129**: `3. Scenario comparison table (conservative, moderate, optimistic)` (cold-start leak)
- **Line 170**: `Write the script to: {path}` (cold-start leak)

The agent receives contradictory directives: "edit, preserve everything" at the top, and "follow this rigid 5-layer structure with 3 scenarios, write the script to: {path}" at the bottom.

### How this explains the regressions

The cold-start spec prescribes a specific structure: "Scenario comparison table (conservative, moderate, optimistic)" — exactly 3 scenarios. Features that don't fit this template get dropped:

- **Concept 13**: Viable-conservative was a 4th scenario beyond the prescribed 3. Component-level alpha scaling was an additional analysis block beyond the 5-layer structure. Both dropped.
- **Concept 16**: Heat sales sensitivity sweep was a concept-specific addition beyond the prescribed sweep structure. Dropped while adding a different feature (2D CapEx grid) that better fit the template.
- **Concept 17b**: Iter-6 had no model-targeted findings. The model agent made minimal changes, so the contradictory instructions had less surface area to cause damage.

## Detailed Findings

### Deployment Confirmation

Commit `367f614` was committed at 09:38 on 2026-04-13 on branch `fix/feedback-data-leak`. Iter-6/7 runs happened between 09:33-09:53. All spec changes were in the working tree.

### Concept 13: Electrostatic Hybrid — REGRESSION

**Iter-6** (1403 lines): Added component-level alpha scaling (48 lines) + viable-conservative scenario ($193.8/MWh at 1 GWe). Addressed iter-5 findings.

**Iter-7** (1341 lines): Removed both features. Added 3-line alpha annotation. Assessor re-raised the exact same findings as iter-5:
- Iter-7 F-1 ("Missing viable-conservative scenario") = iter-5 F-2
- Iter-7 F-2 ("Component-level alpha scaling absent") = iter-5 F-1

Finding oscillation: iter-5 raises → iter-6 fixes → iter-7 removes → iter-7 re-raises.

### Concept 16: Muon-Catalyzed Fusion — REGRESSION

**Iter-6** (1764 lines): Had heat sales sensitivity sweep (73 lines, two price scenarios at $12 and $20/MWh_th, 9 fraction values from 0-50%) + Acceleron claim scenario.

**Iter-7** (1653 lines): Dropped entire heat sales feature. Added second 2D CapEx feasibility grid instead. Assessor re-raised heat sales as F-1 (important).

Note: Original research incorrectly reported concept 16 as "positive trajectory" with "no model amnesia." This was wrong — the subagent's analysis missed the heat sales regression.

### Concept 17b: Laser-ICF Fast Ignition — NO REGRESSION

**Iter-6**: All findings `Category: analysis`. Model verbatim copy of iter-5. No model-targeted work → no opportunity for contradictory instructions to cause damage.

**Iter-7**: Addressed iter-6 F-2 (G_t causal direction). All 6 sweeps retained. Clean targeted edit.

This is the control case: when the model agent has a simple, focused task and the contradictory cold-start instructions don't conflict with what it's doing, the edit succeeds.

### Tiered Validator Behavior

Validators are selecting correctly. The validators themselves are not the problem — `validate_file_modified` correctly detects that the file changed. The regressions pass validation because the model agent does modify the file; it just also destructively removes prior content.

### Feedback Starvation Fix

Working correctly across all three concepts. All findings visible in prompts with correct framing notes.

## Root Cause and Fix

The root cause is deterministic: `fill_template()` cannot handle nested `{{#if}}` blocks. The fix is to support nesting in the regex, or restructure the templates to avoid nesting.

**Option A — Fix the template engine**: Replace the single-pass `re.sub` with a proper recursive or stack-based parser that handles nested conditionals.

**Option B — Flatten the templates**: Remove nesting by making `model_feedback` blocks standalone (not nested inside `feedback_pass` / `cold_start`). This is simpler but less expressive.

Either fix will eliminate the cold-start instruction leak, which should eliminate the contradictory-directive regression pattern observed in 2 of 3 concepts.

## Code References

- `exploration/concept_analysis/scripts/lib/templating.py:37-42` — The buggy regex
- `exploration/concept_analysis/prompt_templates/model_setup_freeform.md:1-31` — feedback_pass block with nested model_feedback
- `exploration/concept_analysis/prompt_templates/model_setup_freeform.md:33-197` — cold_start block with nested model_feedback
- `exploration/concept_analysis/analyses/13-electrostatic-hybrid/iter-7/model_setup_prompt.md:83` — Cold-start "5-layer structure" leaked into feedback-pass prompt
- `exploration/concept_analysis/analyses/13-electrostatic-hybrid/iter-7/model_setup_prompt.md:129` — Cold-start "conservative, moderate, optimistic" leaked
- `exploration/concept_analysis/analyses/13-electrostatic-hybrid/iter-7/model_setup_prompt.md:170` — Cold-start "Write the script to:" leaked
- `exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-7/model_setup_prompt.md:83,129,170` — Same leaks confirmed
