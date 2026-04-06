# Assessment: {{concept_name}}

You are evaluating a D1+ concept analysis for quality of framing, completeness, and numerical plausibility relative to the analysis goals.

## Files to Read

### Analysis
Read this file completely:
`{{analysis_path}}`

### Analysis Goals

{{@config/analysis_goals.md}}

### Assessment Checklist

{{@config/assessment_checklist.md}}

## Instructions

1. Read the analysis completely
2. Evaluate against each checklist criterion
3. Identify the most significant gaps — at most 3 findings
4. For each finding, explain what is insufficient and what should change
5. If the analysis adequately addresses all goals, return PASS

### Finding Categories

Each finding must include a `Category` field:
- **`analysis`** — the fix requires changes to the analysis text (Section 2 framing,
  Section 5 parameter tables, Section 7 differentiator discussion, etc.)
- **`model`** — the fix requires changes to the model code or parameters:
  sensitivity sweeps, scenario branches, parameter values in model_setup.py,
  model output formatting, or computational methodology

A finding is `model` when the recommendation says to change what the model
*computes or sweeps*. A finding is `analysis` when the recommendation says
to change what the analysis *says or frames*.

When a finding touches both (e.g., "add parameter to Section 5 table AND
to sensitivity sweep"), assign the **primary** target — the one that would
resolve the core issue.

{{#if model_output_path}}
## Model Output

The concept also has a quantitative LCOE model. The model output is at:
`{{model_output_path}}`

Evaluate whether:
1. The model's assumptions and parameter values are consistent with the analysis.
2. The LCOE result is plausible for this concept type (order of magnitude).
3. Key cost drivers in the model match the analysis narrative's emphasis.
Note any discrepancies in your findings.
{{/if}}

## Scope

Focus on whether the analysis captures the **shape** of the concept:
positioning, differentiators, TEA implications, modeling approach, and risks.

Additionally, check **numerical plausibility**:
- Are parameter values the right order of magnitude for this concept type?
- Does the model output LCOE align with the analysis narrative's claims?
- Are physical parameters (temperatures, pressures, efficiencies) within
  physically plausible ranges for the stated technology?

You are NOT checking formatting, style consistency, or template structure compliance.

## Output

Write the assessment to this file using the Write tool:
`{{feedback_path}}`

Use the exact format below:

{{@config/feedback_format.md}}
