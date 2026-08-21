# Spec: Fix Template Nesting Bug in Model-Setup Prompts

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-13T10:17:57-07:00
**Complexity:** LOW
**Branch:** fix/feedback-data-leak

---

## Business Goals

### Why This Matters

The template engine (`lib/templating.py`) cannot handle nested `{{#if}}` conditionals. Both model-setup templates nest `{{#if model_feedback}}` inside `{{#if feedback_pass}}`/`{{#if cold_start}}`. The non-greedy regex matches the outer open tag to the inner close tag, orphaning the outer `{{/if}}` and leaking the entire cold-start instruction block into feedback-pass prompts.

This is a deterministic bug — every feedback-pass prompt for every concept gets contradictory "edit existing model" + "write from scratch" directives. Confirmed in iter-7 rendered prompts for concepts 13 and 16, causing regressions in both (dropped sweeps, dropped scenarios).

### Success Criteria

- [ ] Feedback-pass model prompts contain ONLY feedback-pass instructions (no cold-start content)
- [ ] Cold-start model prompts contain ONLY cold-start instructions (no feedback-pass content)
- [ ] `model_feedback` content renders correctly in both modes when present
- [ ] `model_feedback` content absent renders cleanly (no orphaned headers) when empty
- [ ] No change to prompt content — only structural split, no wording changes

### Priority

High — actively blocking convergence on concepts 13 and 16. Each wasted iteration costs ~$2-5 + pipeline time.

---

## Problem Statement

### Current State

`lib/templating.py:37-42` uses a single-pass regex for conditionals:

```python
result = re.sub(
    r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
    replace_conditional,
    result,
    flags=re.DOTALL,
)
```

The `.*?` non-greedy quantifier matches the nearest `{{/if}}`. With nested blocks, this matches the outer open to the inner close, leaving everything after the inner close (including the outer `{{/if}}`) as literal text in the output.

Both `model_setup_freeform.md` and `model_setup_costingfe.md` nest `{{#if model_feedback}}` inside `{{#if feedback_pass}}` and `{{#if cold_start}}`, triggering this bug on every feedback-pass render.

### Desired Outcome

Eliminate nesting from model-setup templates by splitting each into two files — one for cold start, one for feedback pass. This follows the existing pattern where `build_model_vars()` already selects between `model_setup_costingfe.md` and `model_setup_freeform.md` based on concept type.

---

## Scope

### In Scope

- Split `model_setup_freeform.md` into cold-start and feedback-pass variants
- Split `model_setup_costingfe.md` into cold-start and feedback-pass variants
- Update `build_model_vars()` in `loop.py` to select the correct template variant
- Replace nested `{{#if model_feedback}}` with plain `{{model_feedback}}` substitution in templates (empty string renders harmlessly)

### Out of Scope

- Fixing the template engine regex to support nesting (unnecessary once nesting is eliminated)
- Splitting `analysis_v2.md` (no nesting — all `{{#if}}` blocks are top-level)
- Splitting `assessment.md` (no nesting)
- Any wording changes to template content

### Edge Cases & Considerations

- Cold-start with `model_feedback` present: possible when standalone `cmd_model_setup` is called with feedback. The cold-start template SHOULD include `{{model_feedback}}` with its header so feedback renders if provided.
- Feedback-pass with empty `model_feedback`: the "Assessment Findings" header + empty string renders harmlessly. Alternatively, keep the `{{#if model_feedback}}` conditional in the edit template since it's no longer nested and the regex handles it fine at top level.

---

## Requirements

### Functional Requirements

> All requirements below are from the user's request and research findings.

1. **FR-1**: Split `model_setup_freeform.md` into `model_setup_freeform.md` (cold start only, lines 33-197 of current file) and `model_setup_freeform_edit.md` (feedback pass only, lines 1-31 of current file)
2. **FR-2**: Split `model_setup_costingfe.md` into `model_setup_costingfe.md` (cold start only, lines 36-150 of current file) and `model_setup_costingfe_edit.md` (feedback pass only, lines 1-34 of current file)
3. **FR-3**: Update `build_model_vars()` in `loop.py` to append `_edit` suffix to template name when `prior_model_path` is set (feedback pass mode)
4. **FR-4**: Remove outer `{{#if feedback_pass}}`/`{{/if}}` and `{{#if cold_start}}`/`{{/if}}` wrappers from all four resulting templates (each file is mode-specific, no conditional needed)
5. **FR-5**: Convert nested `{{#if model_feedback}}` blocks to top-level `{{#if model_feedback}}` (no longer nested, regex handles correctly) or plain `{{model_feedback}}` substitution
6. **FR-6**: No template engine changes required — the bug is avoided by eliminating nesting

---

## Acceptance Criteria

### Core Functionality

- [ ] `model_setup_freeform.md` contains only cold-start content, no `{{#if cold_start}}` wrapper
- [ ] `model_setup_freeform_edit.md` contains only feedback-pass content, no `{{#if feedback_pass}}` wrapper
- [ ] `model_setup_costingfe.md` contains only cold-start content, no `{{#if cold_start}}` wrapper
- [ ] `model_setup_costingfe_edit.md` contains only feedback-pass content, no `{{#if feedback_pass}}` wrapper
- [ ] `build_model_vars()` returns `model_setup_freeform_edit.md` when `prior_model_path` is set and concept is freeform
- [ ] `build_model_vars()` returns `model_setup_costingfe_edit.md` when `prior_model_path` is set and concept is costingfe
- [ ] No `{{#if}}` nesting exists in any model-setup template

### Regression

- [ ] Cold-start prompt content identical to current correct render (when nesting bug doesn't fire — i.e., no `model_feedback` present)
- [ ] Feedback-pass prompt content identical to what SHOULD have rendered (edit instructions + findings, no cold-start leak)
- [ ] `model_setup_costingfe.md` `{{#if mapping_notes}}` (line 81, top-level, non-nested) continues to work

---

## Related Artifacts

- **Research:** `.project/research/20260413-model-continuity-effectiveness-analysis.md`
- **Parent work item:** `.project/active/model-feedback-starvation/spec.md`
- **Bug location:** `exploration/concept_analysis/scripts/lib/templating.py:37-42`
- **Templates:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`, `model_setup_costingfe.md`
- **Template selection:** `exploration/concept_analysis/scripts/lib/loop.py:621-682`

---

**Next Steps:** After approval, proceed to `/_my_design` (or skip to `/_my_implement` given low complexity — the design is specified in the research).
