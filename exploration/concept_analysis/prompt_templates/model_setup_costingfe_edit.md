# 1costingfe Model Update: {{concept_name}}

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one
- **Never add or restore** any of: `noak`, `interest_rate`, `inflation_rate`, `eta_th`, `eta_de`, `f_dec`, `eta_dec`, `eta_pin1`, `eta_pin2`. These are owned by `1costingfe` per issue #35. If a finding asks you to "tune" any of them, the fix goes in costingfe (YAML / preset / `forward()` default), not here. See `model_setup_costingfe.md` §"Forbidden Parameters" for the full rationale.
- Sensitivity sweeps or scenario matrices that vary any of those parameters are NOT allowed — delete any existing block that does.

{{#if model_feedback}}
## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

{{model_feedback}}
{{/if}}

## Reference Files

- **Concept Analysis:** `{{analysis_path}}`
- **Example:** `{{example_path}}`
- **Defaults:** `{{defaults_path}}`
- **README:** `{{readme_path}}`
- **Costing Constants:** `{{costing_constants_path}}`

## Output
Write changes to: `{{output_path}}`
