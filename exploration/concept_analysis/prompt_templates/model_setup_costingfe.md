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
## Assessment Feedback

The following findings were raised by the most recent assessment. Not all
findings require model changes — address findings that affect what the model
computes, sweeps, or parameterizes. Findings tagged `Category: analysis` may
still have model implications (e.g., a new parameter identified in the analysis
text that should also appear in a sensitivity sweep).

{{model_feedback}}
{{/if}}

## Concept Mapping
- **ConfinementConcept:** `{{costingfe_concept}}`
- **Fuel:** `{{costingfe_fuel}}`
{{#if mapping_notes}}- **Notes:** {{mapping_notes}}{{/if}}

## Power Standardization: Dual-Result Pattern

The primary `result = model.forward(...)` stays at the concept's **native** power
level. This preserves physics consistency (Q_eng, power balance, CAS breakdown).

**If the concept's native design point is NOT 1000 MWe**, add a second forward()
call to produce a self-consistent 1 GW result using per-account cost scaling:

1. Factor all shared kwargs into a `_SHARED_KWARGS` dict (avoid duplicating
   parameters between the two forward() calls):

   ```python
   _SHARED_KWARGS = dict(
       availability=...,
       lifetime_yr=...,
       # ... all engineering params, cost_overrides, etc.
       # DO NOT include noak / interest_rate / inflation_rate / eta_th / eta_de
       # / f_dec / eta_dec / eta_pin1 / eta_pin2 — see "Forbidden Parameters".
   )
   ```

2. Compute both results:

   ```python
   result = model.forward(net_electric_mw=<native_power>, **_SHARED_KWARGS)

   result_1gw = model.forward(
       net_electric_mw=1000.0,
       override_reference_mw=<native_power>,
       **_SHARED_KWARGS,
   )
   ```

   `override_reference_mw` tells the framework that `cost_overrides` values are
   valid at `<native_power>` MWe, and it should scale them to 1000 MWe using
   per-account scaling laws.

3. Both `result` and `result_1gw` MUST be module-level variables (not inside a
   function or if-block).

4. Do NOT add `scaled_headline`. Do NOT compute sensitivities for `result_1gw`
   — the extraction pipeline handles that.

**If the concept's native design point IS 1000 MWe**, do NOT add `result_1gw`.
A single `result` at 1000 MWe is sufficient.

## Forbidden Parameters (issue #35) — CRITICAL

The following parameters MUST NOT be set in this script. They are owned by
`1costingfe` and concepts inherit the framework's defaults so cross-concept
LCOE comparisons remain apples-to-apples. If your reading of the source
suggests a different value, the fix goes in `1costingfe` (YAML / preset /
forward() default), NOT in `model_setup.py`.

| Param | Why owned by costingfe | costingfe default source |
|---|---|---|
| `noak` | This is a NOAK costing tool; the corpus is uniformly NOAK. | `forward()` default `True` |
| `interest_rate` | Uniform discount rate across the corpus. | `forward()` default `0.07` |
| `inflation_rate` | Uniform inflation assumption. | `forward()` default `0.02` |
| `eta_th` | Driven by the `power_cycle` ENUM (RANKINE / BRAYTON_SCO2 / COMBINED). | `POWER_CYCLE_DEFAULTS` |
| `eta_de` | DEC efficiency. | Concept YAML |
| `f_dec` | DEC fraction (0 = no DEC). | Concept YAML |
| `eta_dec` | Inductive DEC efficiency (Helion-style). | Concept YAML |
| `eta_pin1`, `eta_pin2` | Retired in the Apr 2026 pulsed-power-balance revamp; single `eta_pin` replaces them. | n/a — do not pass |

**Do NOT:**
- Pass any of these as kwargs to `model.forward(...)`, `model.sensitivity(...)`, or any other 1costingfe entry point.
- Define a `SCREAMING_SNAKE` constant for any of them at module scope.
- Build scenario sweeps or sensitivity matrices that override any of these values.

**OK to:**
- Read them back from `result.params["eta_th"]` (etc.) for display or downstream physics-side arithmetic.
- Choose the `power_cycle` ENUM (which selects `eta_th`) by passing it to `CostModel(...)` at construction time — that is the supported way to pick a thermal cycle.

**Allowed efficiency parameters:** `eta_pin` (driver/heating wall-plug) and
`eta_p` (coolant pumping) ARE legitimate concept-architecture overrides and may
still be set when the concept's driver class diverges from the YAML default.

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
eta_pin=0.07,  # KrF excimer driver wall-plug, NOAK; [XEC] §Challenge 3
               # Source: xec-20260224-commercialization-whtppr.md
```
For uncertain values, prefix with `# UNCERTAIN:`. Note: do not pick `eta_th` —
it is owned by the `power_cycle` ENUM (see "Forbidden Parameters" above).

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
