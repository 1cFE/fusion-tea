# Score: {{concept_name}}

You are adding Section 8 (LCOE Downselect Scoring) to an existing synthesis for
the fusion concept **{{concept_name}}** ({{company}}, concept ID: {{concept_id}}).

Your role is to EVALUATE and SCORE using the framework below. Every score must
be justified with specific evidence from the analysis and model output.

## Required Reading

Read ALL of the following before scoring:

### 1. Existing Synthesis
`{{synthesis_path}}`

### 2. Full Analysis
`{{analysis_path}}`

{{#if gap_report_path}}
### 3. Gap Report
`{{gap_report_path}}`
{{/if}}

{{#if model_setup_path}}
### 4. Model Setup
`{{model_setup_path}}`
{{/if}}

{{#if model_output_path}}
### 5. Model Output
`{{model_output_path}}`
{{/if}}

### Approved Prior Syntheses (for cross-concept context)
{{approved_syntheses}}

## Your Task

Write ONLY Section 8 content. Do NOT repeat or modify Sections 1-7.

Write to: `{{output_path}}`

### Section 8: LCOE Downselect Scoring

Score this concept using the scoring framework below. You score C1, C3, C4, C5,
and C8. You also fill the C7 risk matrix (7 functions x 2 subcategories = 14 cells).

**You do NOT score C2, C6, or C7.** These are computed deterministically by Python.
Do not include them in your score table or YAML block.

For each scored criterion, provide:
- The **score** (1-5, where 5 = most favorable)
- **Sub-scores** where the framework defines them
- **2-3 sentences of justification** citing specific data from the analysis,
  model output, CAS breakdown, or gap report. Do not score without evidence.

**Do not double-count between criteria.** C4 measures operational complexity of
the built plant, not physics feasibility. C7 is the sole place where "this might
not work at all" is scored.

#### Score Table

Present C1, C3, C4, C5, C8 as a table with sub-factor breakdowns:

| Criterion | Sub-factors | Score | Key justification |
|-----------|-------------|-------|-------------------|
| C1: Modularization | mode avg: X.X, repetition: +X.X | X.X | ... |
| C3: Supply Chain Learning | A: X.X, B: X.X, C: X.X | X.X | ... |
| C4: Plant Complexity | A: X.X, B: X.X | X.X | ... |
| C5: Customization Needs | A: X, B: X | X.X | ... |
| C8: Data Adequacy | A: X.X, B: X.X, C: X.X, D: X.X | X.X | ... |

#### C7 Risk Matrix

Fill the complete 7-function x 2-subcategory risk matrix. For each of the 14 cells,
provide ALL required fields: plant requirement, best demonstrated value, gap ratio,
closure mechanism, classification (binary/degrading), and evidence tier (1-5).

After the matrix, report the function-level means (F1-F7) as the average of the
physics and hardware evidence tiers for each function.

#### YAML Scores Block

End Section 8 with the YAML block in the exact format specified by the framework.

## Scoring Framework

{{@config/scoring_framework.md}}
