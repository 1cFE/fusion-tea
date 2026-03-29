# Source Integration Assessment: {{concept_name}}

You are evaluating new source documents that have been added to a concept
that already has a completed analysis. Your job is to identify what material
information from the new sources should be incorporated into the existing
analysis, and produce structured feedback for the analysis agent.

## Existing Analysis
Read this file completely:
`{{analysis_path}}`

## New Source Documents (use subagents)

Spawn one subagent per new source document. Ask each subagent:
- What new technical, economic, or performance data does this source contain?
- Does it contain information that contradicts or updates claims in the analysis?
- What LCOE-relevant parameters or cost data are present?
- What risk, timeline, or TRL information is relevant?

New sources:
{{new_source_paths}}

## Analysis Goals (for reference)

{{@config/analysis_goals.md}}

## Instructions

1. Read the existing analysis completely
2. Spawn subagents to read each new source
3. Compare the new information against what the analysis already covers
4. Identify material gaps — information that would change the analysis's
   conclusions, parameter values, risk assessment, or modeling recommendations
5. Do NOT flag information the analysis already covers adequately
6. Do NOT flag minor/cosmetic additions — focus on material impact

## Output

Write structured feedback to this file using the Write tool:
`{{feedback_path}}`

Use this exact format:

{{@config/feedback_format.md}}

**Adaptation for source integration**: The "Finding" field should describe
what new information the source provides. The "Recommendation" field should
specify exactly where and how to incorporate it into the analysis (which
section, what to add/update). The "Target" field should reference the analysis
section that needs updating.

If the new sources contain no material information beyond what the analysis
already covers, return `VERDICT: PASS`.
