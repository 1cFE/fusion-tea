# Free-Form Model Update: {{concept_name}}

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one
- **Native scale only**: do NOT add or restore a `scaled_headline` dict or any
  `(p_native/1000)^(1-α)` extrapolation. Freeform models report at the
  concept's native power. If the prior model contains such code, remove it as
  part of the edit. The headline LCOE line must read
  `LCOE: <value> $/MWh   (freeform, native-scale only)` so cross-concept
  tables can flag it.

{{#if model_feedback}}
## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

{{model_feedback}}
{{/if}}

## Reference Files

- **Concept Analysis:** `{{analysis_path}}`
- **Costing Constants:** `{{costing_constants_path}}`

## Output
Write changes to: `{{output_path}}`
