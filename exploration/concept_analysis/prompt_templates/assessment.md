# Assessment: {{concept_name}}

You are evaluating a D1+ concept analysis (and its model setup, if present) for
design-point coherence, override discipline, family-delta concreteness, and
numerical plausibility — against the new pipeline contract.

## Files to Read

### Analysis
Read this file completely: `{{analysis_path}}`

### Analysis Goals

{{@config/analysis_goals.md}}

### Override Semantics (the policy the overrides must satisfy)

The overrides you are assessing are authored against this policy — the same one the
analysis and model-setup agents read. Use its vocabulary (the single invariant, the
S/U/P cost classes, the modular-fleet rationale baseline) when judging override
discipline below.

{{@config/override_semantics.md}}

### Assessment Checklist

{{@config/assessment_checklist.md}}

{{#if model_output_path}}
## Model Output

The concept has a quantitative LCOE model. Its output is at: `{{model_output_path}}`

Evaluate whether:
1. The model's assumptions and parameter values are consistent with the analysis.
2. The 1 GWe projection LCOE (`result_1gw`) is plausible (order of magnitude) for
   this concept type, and the native LCOE is coherent with it.
3. Key cost drivers in the model match the analysis narrative's emphasis.
{{/if}}

## Coherence Flags (computed — interpret, do not just echo)

The pipeline ran cross-artifact coherence checks against this iteration's
artifacts. Read them and factor them into your findings. A `FLAG:` line is a
real discrepancy to investigate; a clean line confirms a check passed.

{{coherence_flags}}

## Override-Count Rubric

{{fit_grade_band}}

Check the count of `enabled` overrides (in `analysis.md` Section 5b, and in
`model_setup.py` if present) against this band. A High-fit concept with many
enabled overrides, or a Low-fit concept with none, is a finding unless the
evidence clearly justifies it.

{{#if concept_landscape}}
## Concept Landscape

The comparables for this concept are fixed upstream. Use the landscape only to
sanity-check that the family-delta prose engages the *fixed* comparables, not an
arbitrary neighbour.

{{concept_landscape}}
{{/if}}

## Instructions

1. Read the analysis completely (and the model output, if present).
2. Evaluate against each checklist area, the coherence flags, and the override
   rubric.
3. Identify the most significant gaps — **at most 3 findings**.
4. For each finding, explain what is insufficient and what should change, and tag
   its `Category` (`analysis` or `model`) by where the fix lands.
5. If the analysis and model adequately satisfy the contract, return `VERDICT: PASS`.

You are NOT checking formatting, style consistency, or template-structure
compliance. Focus on coherence, accountability, and numerical plausibility.

## Output

Write the assessment to this file using the Write tool: `{{feedback_path}}`

Use the exact format below.

{{@config/feedback_format.md}}
