# Spec: Feedback Routing Fix — Target Categories + Assess Finding Preservation

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06 13:46 UTC
**Complexity:** MEDIUM
**Branch:** `design-space-explore`

---

## Business Goals

### Why This Matters

The analysis pipeline's iteration loop runs: feedback → analyze → model-setup → assess. Assessment findings that require model code changes (e.g., "add REBCO to the sensitivity table") are written in the same format as findings that require analysis text changes. The analysis agent can only edit `analysis.md` — it cannot modify `model_setup.py`. The model-setup agent regenerates the script each iteration by reading `analysis.md`, but never sees the assessment findings directly. This creates a two-hop indirection where model-targeted findings must be "laundered" through analysis prose to reach the model agent — which fails in practice.

Demonstrated failure: concept 01-hts-compact-tokamak has had "REBCO cost absent from sensitivity table" flagged as a finding for 4 consecutive iterations (iters 4-7) without resolution.

**Additionally**, there is a second feedback routing bug: when `--research` is enabled and acquires sources, the feedback-producer priority chain in `loop.py` substitutes source-integration output as the feedback, **silently dropping** the prior iteration's assessment findings. The analysis agent never sees findings like "add nearest-neighbor concepts" because it receives "here are new sources to integrate" instead. The assessment re-flags the finding on the next pass, but research runs again and drops it again — a Sisyphean loop.

Demonstrated failure: concepts 07-maglif and 15-sheared-flow-stabilized-z-pinch both have assessment findings (nearest-neighbor designations, rep-rate tables) that were flagged, then dropped by the research step, then re-flagged, then dropped again across multiple iterations. Concept 09-qi-stellarator-hts only made progress on iter-6 because research happened to find nothing that iteration, causing the code to fall through to the assess feedback path.

The pipeline is about to run 28+ concepts through stage1-all with `--research` enabled; without these fixes, both model-targeted and research-displaced findings will burn iterations without converging.

### Success Criteria

- [ ] Assessment findings carry an explicit target category (`analysis` or `model`)
- [ ] Model-setup agent receives model-targeted findings directly as input
- [ ] Analysis agent sees all findings but understands which ones primarily target the model
- [ ] A concept with a model-targeted finding resolves it within 1-2 iterations instead of bouncing indefinitely
- [ ] When research acquires sources, unresolved assessment findings from the prior iteration are preserved and delivered to the analysis agent alongside the source-integration feedback
- [ ] Assessment findings are no longer silently dropped by the research→source-integration feedback path

### Priority

High — blocking the batch pipeline run (`.project/active/batch-pipeline-run/plan.md`).

---

## Problem Statement

### Current State

**Problem A — No target categories**: The feedback format (`config/feedback_format.md`) has four fields per finding: Target (section number), Finding, Recommendation ("what the analysis agent should do differently"), Priority. The `Target` field refers to analysis sections only. There is no vocabulary or mechanism for findings that require model code changes. The model-setup templates accept `analysis_path` as their primary data source with no `feedback_path` input. The analysis template (feedback-pass mode) instructs the agent to "address each finding" by editing `analysis.md` with no guidance on model-targeted findings.

**Problem B — Research drops assessment findings**: The feedback-producer selection in `loop.py` (lines 105-161) is a priority cascade:

```
1. Cold start (iter 1, not resume)
2. Review kick-back (one-shot)
3. Source-integration (resume with new sources detected)
4. Research (--research flag, iter > 1)    ← unconditionally fires
5. Normal assess feedback                  ← fallback
```

Branch 4 fires on **every** iteration > 1 when `--research` is enabled. When research acquires sources, it chains to `_run_source_integration()` which produces feedback about the new sources. The prior iteration's `feedback.md` (assessment findings) is **completely replaced**. The analysis agent receives "here are new sources" instead of "your analysis is missing nearest-neighbor concepts."

The fallback to assess feedback (branch 5) only triggers when research acquires nothing — which is stochastic. Concept 09 only saw its assess findings because research happened to find nothing on iter-6.

### Desired Outcome

Assessment findings are categorized by their primary target. Model-targeted findings are routed directly to the model-setup agent. When research acquires sources, unresolved assessment findings are preserved and merged with the source-integration feedback, so the analysis agent sees both "new sources to integrate" and "findings to address."

---

## Scope

### In Scope

**Problem A — Target categories:**
1. **Feedback format** (`config/feedback_format.md`): Add `Category` field to finding format
2. **Assessment template** (`assessment.md`): Instruct the assessment agent to categorize findings and explain the distinction
3. **Model-setup templates** (`model_setup_costingfe.md`, `model_setup_freeform.md`): Add conditional section for model-targeted feedback
4. **Analysis template** (`analysis_v2.md`, feedback-pass section): Update instructions so the agent understands category semantics
5. **Loop code** (`lib/loop.py`): Extract model-targeted findings from `feedback.md`, pass to `build_model_vars()` as a new template variable

**Problem B — Assess finding preservation:**
6. **Loop code** (`lib/loop.py`): When research acquires sources and chains to source-integration, merge unresolved assessment findings from the prior iteration into the feedback delivered to the analysis agent
7. **Source-integration template** (`source_integration.md`): Update to accept and pass through carried-forward assessment findings (or the loop writes a merged feedback file)

### Out of Scope

- Changing the assessment logic or evaluation criteria
- Adding new pipeline stages
- Changing the 3-finding-per-pass cap (stays at 3 total across both categories)
- Fixing concept 01's or 07's specific issues (those are validation cases)
- Changing how review kick-back works
- Cross-concept knowledge for nearest-neighbor findings (separate issue — the analysis agent lacks sources about other concepts)

### Edge Cases & Considerations

- A finding MAY target both analysis and model (e.g., "parameter table missing X" affects both prose and code). The `Category` field indicates the **primary** target — the analysis agent still reads all findings and updates prose where relevant.
- Legacy `feedback.md` files from prior iterations lack the `Category` field. The loop code MUST treat findings without a category as `analysis` (backward-compatible default).
- The manage-concept agent also produces feedback in this format (per `feedback_format.md` header). Its findings are always analysis-targeted since it doesn't interact with the model step.
- When merging assess findings with source-integration output, the combined feedback may exceed what fits comfortably in a single prompt. The merge SHOULD cap carried-forward findings at the 3-finding limit (same as a normal assessment pass). If the prior assessment had 3 findings, all 3 are carried forward — source-integration additions are supplementary context, not additional findings.
- The first iteration after a research acquisition will receive a larger feedback payload (assess findings + source context). This is acceptable — the analysis agent already handles multi-finding feedback.

---

## Requirements

### Functional Requirements

**Problem A — Target categories:**

1. **FR-1**: The feedback format MUST include a `Category` field on each finding with values `analysis` or `model`.

2. **FR-2**: The assessment template MUST instruct the assessment agent to assign a category to each finding based on whether the fix primarily requires changes to the analysis text or the model code/parameters.

3. **FR-3**: The assessment template MUST provide clear criteria for the `model` category. A finding is `model`-targeted when the recommendation requires changes to: sensitivity sweeps, scenario branches, parameter values in model code, model output formatting, or computational methodology — i.e., things that live in `model_setup.py`, not `analysis.md`.

4. **FR-4**: The model-setup templates MUST accept an optional `model_feedback` variable containing model-targeted findings. When present, the model agent MUST read and address these findings when generating `model_setup.py`.

5. **FR-5**: The analysis template (feedback-pass mode) MUST instruct the agent that findings with `Category: model` primarily target the model code, but the analysis agent SHOULD still update analysis prose (e.g., Section 5 parameter tables, modeling approach descriptions) to support the model change. The analysis agent MUST NOT attempt to address model findings solely through narrative rewording.

6. **FR-6**: The loop code MUST parse `feedback.md` to extract model-targeted findings and pass them to `build_model_vars()` as a template variable. Findings without a `Category` field MUST be treated as `analysis` (backward compatibility).

7. **FR-7**: The 3-finding cap per assessment pass MUST remain at 3 total findings across both categories.

**Problem B — Assess finding preservation:**

8. **FR-8**: When the research step acquires sources and chains to source-integration, the loop MUST read the prior iteration's `feedback.md` and carry forward its findings into the feedback delivered to the analysis agent.

9. **FR-9**: Carried-forward assess findings MUST be clearly delineated from source-integration content in the merged feedback file, so the analysis agent can distinguish "fix these issues from the last assessment" from "integrate these new sources."

10. **FR-10**: The merged feedback MUST be written to a single file in the current iteration's directory (e.g., `iter-N/feedback.md`) that the analysis template's `{{feedback_path}}` variable points to.

11. **FR-11**: If the prior iteration's `feedback.md` has a `VERDICT: PASS`, there are no findings to carry forward — the merge step MUST be skipped and source-integration output used as-is.

12. **FR-12**: The merge MUST NOT alter the original `feedback.md` from the prior iteration (it is an audit artifact). The merged output is a new file in the current iteration's directory.

---

## Acceptance Criteria

### Problem A — Target Categories

- [ ] `feedback_format.md` includes `Category` field with `analysis | model` values
- [ ] `assessment.md` instructs the agent to assign categories with clear criteria
- [ ] `model_setup_costingfe.md` and `model_setup_freeform.md` have conditional `{{#if model_feedback}}` section
- [ ] `analysis_v2.md` feedback-pass section explains category semantics
- [ ] `loop.py` extracts model findings from feedback and passes to model-setup
- [ ] Old feedback files without `Category` field don't break the parser

### Problem B — Assess Finding Preservation

- [ ] When research acquires sources, prior assess findings are merged into the feedback file
- [ ] Merged feedback clearly separates "carried-forward findings" from "source-integration context"
- [ ] Prior iteration's original `feedback.md` is not modified
- [ ] When prior assess was PASS (no findings), merge is skipped — source-integration output used as-is
- [ ] Merged feedback file is written to current `iter-N/` directory

### Validation

- [ ] Dry-run concept 01 iter-8 and verify the model-setup prompt contains model-targeted findings
- [ ] Dry-run concept 07 and verify that after research acquires sources, the analyze prompt contains both source-integration context AND prior assess findings (nearest-neighbor, rep-rate table)
- [ ] Inspect generated prompts to confirm both feedback streams are visible to their target agents

---

## Files to Modify

| File | Change | Problem |
|------|--------|---------|
| `prompt_templates/config/feedback_format.md` | Add `Category` field to format spec | A |
| `prompt_templates/assessment.md` | Add categorization instructions + criteria | A |
| `prompt_templates/model_setup_costingfe.md` | Add conditional model-feedback section | A |
| `prompt_templates/model_setup_freeform.md` | Add conditional model-feedback section | A |
| `prompt_templates/analysis_v2.md` | Update feedback-pass instructions for categories + merged feedback | A+B |
| `scripts/lib/loop.py` | Parse model findings for model-setup; merge assess findings with source-integration when research runs | A+B |

All paths relative to `exploration/concept_analysis/`.

---

## Related Artifacts

- **Evidence (Problem A):** Concept 01 iter 4-7 feedback files — REBCO sensitivity finding bounces because model-setup never sees it
- **Evidence (Problem B):** Concept 07 iter 4-6 and concept 15 iter 2-3 — assess findings dropped when research acquires sources; concept 09 iter-6 shows the fix works when research finds nothing (falls through to assess)
- **Batch plan:** `.project/active/batch-pipeline-run/plan.md`
- **Design:** `.project/active/feedback-routing-fix/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
