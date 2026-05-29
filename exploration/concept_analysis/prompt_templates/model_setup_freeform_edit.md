# Free-Form Model Update: {{concept_name}}

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one
- **Never add, restore, or tune** any of: `interest_rate`, `inflation_rate`, NOAK flag, `eta_th`, `eta_de`, `f_dec`, `eta_dec` as per-instance overrides. These are corpus-wide defaults per issue #35 — hardcode them as `@dataclass` defaults matching costingfe (0.07, 0.02, NOAK=True, eta_th per `power_cycle` preset). See `model_setup_freeform.md` §"Mandatory Financial Defaults" for the required values.
- Delete any existing sensitivity sweep or scenario table that varies any of those parameters.

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
