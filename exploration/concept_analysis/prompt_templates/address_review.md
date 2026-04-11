# Address Review: {{concept_name}}

You are applying user-approved review decisions to the concept analysis and
model setup for **{{concept_name}}**.

## Decisions to Apply

{{decisions_block}}

## Files to Edit

- Analysis: `{{analysis_path}}`
{{#if model_setup_path}}
- Model setup: `{{model_setup_path}}`
{{/if}}

## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`{{log_path}}`

Append to the file (do not overwrite). Use this format:

```
## Iteration {{iteration}} — {{date}}

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
