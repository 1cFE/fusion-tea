# 1costingfe Model Setup: {{concept_name}}

You are generating a runnable 1costingfe model setup script for **{{concept_name}}**
({{company}}).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`{{analysis_path}}`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Closest Example (pattern to follow)
`{{example_path}}`
Follow its structure, commenting style, and output format.

### 3. Concept YAML Defaults
`{{defaults_path}}`

### 4. 1costingfe README
`{{readme_path}}`

### 5. Costing Constants
`{{costing_constants_path}}`

{{#if model_feedback}}
## Assessment Feedback (Model-Targeted)

The following findings from the most recent assessment specifically target
the model code. Address each one when generating the script:

{{model_feedback}}
{{/if}}

## Concept Mapping
- **ConfinementConcept:** `{{costingfe_concept}}`
- **Fuel:** `{{costingfe_fuel}}`
{{#if mapping_notes}}- **Notes:** {{mapping_notes}}{{/if}}

## Script Requirements

### Structure
1. Docstring: modeling approach, concept choice rationale, key deviations
2. Imports and model creation
3. Plant configuration constants with comments
4. `model.forward()` with all parameters and cost_overrides
5. Results printing (LCOE, CAS breakdown, CAS22 detail)
6. Key Assumptions summary
7. Sensitivity analysis via `model.sensitivity()`

### Output Interface (CRITICAL)
The concept explorer consumes `model` and `result` at module level for
cross-concept comparison. You MUST follow this convention:

1. `model = CostModel(...)` at module level (NOT inside a function)
2. `result = model.forward(...)` at module level — this variable MUST be named `result`
3. For multi-scenario scripts (e.g., NOAK vs FOAK), choose the reference case
   (prefer NOAK if available) and assign `result = model.forward(...)` for that case.
   Other scenarios may use any variable name (e.g., `result_foak = model.forward(...)`).

### Traceability (CRITICAL)
Every parameter and cost override MUST have an inline comment citing the source:
```python
eta_th=0.90,  # Direct EM recovery; analysis.md §Section 2, Challenge 4
              # Source: helion-website-technology.md §Direct Energy Recovery
```
For uncertain values, prefix with `# UNCERTAIN:`.

### Anti-Hallucination
- Cost overrides MUST be justified from the analysis
- Unknown costs: use framework defaults with `# DEFAULT: ...` comment
- Do NOT invent cost figures

### Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `{{output_path}}`
