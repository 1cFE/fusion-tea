---
date: 2026-04-13T12:00:00-05:00
researcher: Claude
topic: "parameter_metadata pipeline trace — why sliders are empty"
tags: [research, concept-explorer, pipeline, sliders]
status: complete
last_updated: 2026-04-13
---

# Research: Parameter Metadata Pipeline Trace

**Date**: 2026-04-13
**Researcher**: Claude
**Research Type**: Codebase / Architecture

## Research Question

Why is `parameter_metadata` empty for all concepts in the explorer? Trace the
full pipeline from prompt → generation → parsing → serving. Specifically:
1. Do our prompts ask the LLM to generate parameter_metadata?
2. Do we have validation for it?
3. If we did ask for it, would it be parsed? How?
4. Where should the fix live, and how should it work?

## Summary

- **No prompt asks for parameter metadata.** Neither `model_setup_costingfe.md` nor `model_setup_freeform.md` mention `parameter_metadata`, `model_metadata.yaml`, display names, ranges, units, or categories.
- **No `model_metadata.yaml` exists** for any of the 22 analyzed concepts. Zero files.
- **The extractor is fully wired** to load `model_metadata.yaml` from each concept directory (`extract_explorer_data.py:553-570`), validate it via Pydantic, and pass it through. It just gets `{}` because the file doesn't exist.
- **The frontend is fully wired** to render sliders from parameter_metadata (`concept_page.js:234-305`). It silently skips when there are no parameters with `range`.
- **The fix should be deterministic code**, not an LLM prompt. All the data needed to generate parameter_metadata already exists in `result.params` (baselines), `model.sensitivity()` (which params matter), and costingfe's own code (categorization, units).

## Detailed Findings

### 1. The Prompt Gap

The two model_setup prompt templates (`exploration/concept_analysis/prompt_templates/`):

- **`model_setup_costingfe.md`** — asks for a Python script with `model.forward()`, sensitivity analysis, traceability comments, and `scaled_headline`. No mention of parameter metadata, display names, units, or ranges.
- **`model_setup_freeform.md`** — asks for a `@dataclass` with `compute()`, sensitivity sweeps, scenario comparison. Same gap: no parameter metadata.

Neither template references `model_metadata.yaml` or `ParameterMetadata`.

### 2. The Validation Gap

The pipeline's validation (`scripts/lib/validators.py`, `scripts/lib/claude.py`):

- `validate_python_syntax` — checks model_setup.py compiles
- `_check_interface` — checks for module-level `result`/`model` (costingfe) or `params`/`results` (freeform)
- `run_model` — checks stdout contains "lcoe"

No validator checks for parameter metadata. No post-generation step creates it.

### 3. The Extraction Path (Already Working)

`extract_explorer_data.py:553-570`:
```python
def load_parameter_metadata(concept_dir, concept_id):
    meta_path = concept_dir / "model_metadata.yaml"
    if not meta_path.exists():
        return {}  # ← This is what always happens
    raw = yaml.safe_load(meta_path.read_text())
    result = {}
    for key, entry in raw.items():
        result[key] = ParameterMetadata.model_validate(entry)
    return result
```

This function is called at `extract_explorer_data.py:785` for every concept. It
returns `{}` because no `model_metadata.yaml` file has ever been created.

The `ParameterMetadata` Pydantic model (`models.py:306-318`) requires:
```python
class ParameterMetadata(BaseModel):
    display_name: str
    category: ParameterCategory       # plasma, geometry, financial, etc.
    confidence: Confidence             # high, medium, low
    baseline: float                    # from result.params
    display_multiplier: float = 1.0    # e.g., 100 for fraction→%
    display_unit: str = ""
    range: tuple[float, float]         # [low, high] — drives slider bounds
    source: str | None = None
    modeling_note: str | None = None
```

The `ConceptData` model validator (`models.py:357-379`) already emits warnings
for sensitivity keys not covered by parameter_metadata — but since metadata is
always empty, it warns on every concept (36 uncovered keys for concept 21).

### 4. What Data Is Already Available

For **costingfe** concepts (15 of 22), we have rich data at extraction time:

| Need | Source | How to get it |
|------|--------|---------------|
| **baseline** | `result.params` | Already a dict of `{param: value}` |
| **which params matter** | `model.sensitivity(result.params)` | Already computed; keys match |
| **category** | `model._engineering_keys()` vs `model._FINANCIAL_KEYS` | Private but stable |
| **display_name** | Not in costingfe | Need a static lookup table |
| **display_unit** | Not in costingfe | Need a static lookup table |
| **display_multiplier** | Not in costingfe | Need a static lookup table |
| **range** | Not in costingfe directly | Can derive: `baseline ± X%` or use param-specific knowledge |
| **confidence** | Not in costingfe | Would need per-concept authoring or a heuristic |

For **freeform** concepts (7 of 22), the `@dataclass` fields + `_compute_sensitivity_from_params()` provide baselines and elasticities. The same static lookup approach works for display metadata.

### 5. Concept 21 Concrete Example

`result.params` has 46 keys. `model.sensitivity()` returns 36 non-zero elasticities
(34 engineering + 2 financial). The slider system needs metadata for those 36 params.

Sample params that would become sliders:
- `availability: 0.80` → display "Availability", unit "%", multiplier 100, range [0.50, 0.95]
- `eta_th: 0.33` → display "Thermal Efficiency", unit "%", multiplier 100, range [0.25, 0.45]
- `R0: 5.0` → display "Major Radius", unit "m", multiplier 1, range [3.0, 7.0]
- `interest_rate: 0.07` → display "Interest Rate", unit "%", multiplier 100, range [0.04, 0.12]

## Where the Fix Should Live

### Recommended: Deterministic generation in the extractor

Add a function to `extract_explorer_data.py` that **auto-generates** `ParameterMetadata`
from data already available at extraction time:

```
extract_explorer_data.py
  └── generate_parameter_metadata(model, result, concept_type="costingfe"|"freeform")
        ├── baselines: from result.params (costingfe) or dataclass fields (freeform)
        ├── display info: from a static PARAM_REGISTRY dict (new file or inline)
        ├── ranges: baseline ± percentage (configurable per param)
        ├── categories: from costingfe._engineering_keys() or static mapping
        └── confidence: default "medium", overridable via model_metadata.yaml
```

The static registry would look like:

```python
PARAM_DISPLAY = {
    "availability":        ("Availability",          "%",  100, 0.30),
    "eta_th":              ("Thermal Efficiency",    "%",  100, 0.30),
    "eta_pin":             ("Heating Efficiency",    "%",  100, 0.30),
    "R0":                  ("Major Radius",          "m",    1, 0.30),
    "interest_rate":       ("Interest Rate",         "%",  100, 0.50),
    "net_electric_mw":     ("Net Electric Power",    "MW",   1, 0.30),
    # ... ~40 params total (union of all costingfe families)
    # Fields: (display_name, display_unit, display_multiplier, range_fraction)
}
```

**range_fraction** means the slider goes from `baseline * (1 - frac)` to
`baseline * (1 + frac)`. This is a reasonable default; individual params can
have hardcoded absolute ranges where physics constrains them (e.g., availability
capped at 1.0, efficiencies capped at 1.0).

**Confidence** defaults to `"medium"` for all auto-generated entries. The existing
`model_metadata.yaml` mechanism remains as an override: if the file exists, its
entries replace the auto-generated ones. This preserves the hand-authored path
for analysts who want to set specific ranges or confidence levels.

### Why NOT an LLM prompt

- The data is already structured and machine-readable (params dict, elasticities)
- Display names / units are domain constants, not concept-specific
- Ranges can be derived from baselines with a simple formula
- An LLM would hallucinate ranges, units, and display names inconsistently across concepts
- 15 costingfe concepts share the same parameter set — one registry covers them all

### Why NOT model_metadata.yaml authoring

- 22 concepts × 30+ params each = 660+ manual entries
- The extractor already loads the file if it exists — it can serve as override
- Auto-generation covers 95% of cases; hand-authoring is needed only for exceptions

## Code References

- `exploration/concept_explorer/extract_explorer_data.py:553-570` — `load_parameter_metadata()` (reads YAML, returns `{}` today)
- `exploration/concept_explorer/extract_explorer_data.py:183-253` — `extract_costingfe()` (passes `param_metadata` to `ConceptData`)
- `exploration/concept_explorer/extract_explorer_data.py:389-545` — `extract_standalone()` (same pattern)
- `exploration/concept_explorer/models.py:306-318` — `ParameterMetadata` Pydantic model
- `exploration/concept_explorer/models.py:357-379` — `ConceptData._warn_on_uncovered_sensitivity_keys()`
- `exploration/concept_explorer/static/js/concept_page.js:234-305` — `renderSliders()` (frontend, fully working)
- `exploration/concept_explorer/static/js/concept_page.js:458-510` — slider init + compute call
- `exploration/concept_explorer/server.py:573-582` — `compute()` endpoint (fully working)
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` — no mention of metadata
- `exploration/concept_analysis/prompt_templates/model_setup_freeform.md` — no mention of metadata
- `exploration/concept_analysis/scripts/lib/claude.py:429-459` — `_check_interface()` (no metadata check)
- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:643-704` — `_engineering_keys()` (param categorization)
- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:779-814` — `sensitivity()` (returns elasticities only)

## Architecture Insights

The system was designed with a clean separation:
- **model_metadata.yaml**: hand-authored per-concept file with display metadata
- **extract_explorer_data.py**: reads it and passes to ConceptData
- **Frontend**: renders sliders from metadata with ranges

The gap is that nobody ever creates model_metadata.yaml. The design assumed
manual authoring; the reality is that 22 concepts need it and nobody has written
one. The fix is to auto-generate what can be auto-generated and keep the YAML
as an override mechanism.

## Feasibility Assessment

**High feasibility.** The fix is:
1. A static display registry (~40 entries, one-time authoring)
2. A ~50-line function in extract_explorer_data.py
3. A merge step: auto-generated metadata overridden by model_metadata.yaml if present

No LLM changes. No prompt changes. No new dependencies. No pipeline changes.
Just the extractor gets smarter about what it already has.

For freeform concepts, the same approach works — `dataclasses.fields()` gives
parameter names and baselines, `_compute_sensitivity_from_params()` gives
which params matter, and the static registry provides display info.

## Recommendations

1. **Create a param display registry** — a dict mapping param names to (display_name, unit, multiplier, range_fraction). Start with costingfe's known params (~35), add freeform-specific ones as needed.

2. **Add `generate_parameter_metadata()` to the extractor** — takes model/result (costingfe) or params_obj (freeform), merges with the registry, produces `dict[str, ParameterMetadata]`.

3. **Keep `load_parameter_metadata()` as override** — if `model_metadata.yaml` exists, its entries replace auto-generated ones. Analysts can hand-tune specific params.

4. **Re-extract all concepts** — one `uv run python $EXTRACT --skip-narrative` populates all 22 concepts with slider metadata.

5. **Don't touch prompts or pipeline** — this is purely an extraction-time enrichment.

## Open Questions

1. **Range strategy**: `baseline ± 30%` is simple but may not be physically meaningful for all params. Some params (efficiencies, availability) have hard caps at 0 and 1. Should we have per-param absolute bounds in the registry?

2. **Confidence heuristic**: Default "medium" is safe but uninformative. Could we derive confidence from the model_setup.py comments (UNCERTAIN tags)?

3. **Freeform display names**: Freeform concepts may have params not in the costingfe registry (concept-specific physics). Fallback to `param_name` as display name? Or require manual override?
