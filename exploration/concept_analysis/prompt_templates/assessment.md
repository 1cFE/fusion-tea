# Assessment: {{concept_name}}

You are evaluating a D1+ concept analysis for quality of framing and completeness relative to the analysis goals. You are NOT checking numerical accuracy — that is the review stage's responsibility.

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

{{#if model_output_path}}
## Model Output

The concept also has a quantitative LCOE model. The model output is at:
`{{model_output_path}}`

Evaluate whether the model's assumptions and parameter values are consistent
with the analysis. Note any discrepancies in your findings.
{{/if}}

## What You Are NOT Checking

Do NOT evaluate any of the following — they are the review stage's responsibility:
- Numerical accuracy of parameter values
- Citation correctness (whether quotes match sources)
- Calculation verification (whether inferred values are derived correctly)
- Formatting or style consistency
- Whether the analysis matches the output template structure exactly

Focus exclusively on whether the analysis captures the **shape** of the concept: positioning, differentiators, TEA implications, modeling approach, and risks.

## Output

Write the assessment to this file using the Write tool:
`{{feedback_path}}`

Use the exact format below:

{{@config/feedback_format.md}}
