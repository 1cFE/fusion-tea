# 1costingfe Model Update: {{concept_name}}

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply
**targeted edits** based on the assessment findings below. Use the Edit tool — do
NOT rewrite the file from scratch, and do NOT restructure conforming code.

## Preserve the three-forward contract

The file already follows the canonical shape; keep it:
1. `spec` dict (design-point inputs only) + `P_native`
2. `model = CostModel(...)`
3. `generic = generic_reference(model, spec, P_native)` — the mandatory
   overrides-off forward (forward 1), the reference a relative override is written against
4. `overrides = [ ... ]` — six-field registry entries
5. `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`

with `model`, `generic`, `native`, `result_1gw` at module level and the
`print_cas_breakdown(generic, native, result_1gw, overrides)` call retained. Do
not convert the helper call into an inline two-knob `forward()` (the contract
validator rejects it), do not drop the mandatory `generic` line, and do not
re-introduce `# DEFAULT:` comments or the uniform financial parameters
(`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`) into `spec`.
A relative override references `generic` (never `native` or `result_1gw`).

**Rules**:
- Preserve all existing sweeps, scenarios, and sensitivity analyses unless a
  finding specifically says to change them.
- Add content incrementally; every change must be traceable to a specific finding
  or a direct consequence of one.
- Any override you add or change uses a **canonical** account code (schema below)
  and the six-field shape; keep `provenance` honest and show derivation arithmetic
  in `rationale`.

{{#if model_feedback}}
## Assessment Findings

Focus on findings tagged `Category: model`. Findings tagged `Category: analysis`
are informational (the analysis agent handles prose), but you may adjust model
parameters if an analysis finding implies the model's assumptions are wrong.

{{model_feedback}}
{{/if}}

## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `{{analysis_path}}`
- **Example (pattern):** `{{example_path}}`
- **README:** `{{readme_path}}`
- **Costing Constants:** `{{costing_constants_path}}`
- **Concept mapping:** `ConfinementConcept.{{costingfe_concept}}`, `Fuel.{{costingfe_fuel}}`

### Canonical account schema (for any new/changed override)

{{canonical_accounts}}

## Output
Write changes to: `{{output_path}}`
