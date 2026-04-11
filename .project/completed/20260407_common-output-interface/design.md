# Design: Common Output Interface for Model Setup Scripts

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06T20:51:00-07:00
**Updated:** 2026-04-07
**Completed:** 2026-04-07
**Branch:** design-space-explore
**Commit at creation:** 46afb62

## Overview

Establish a contract between the analysis pipeline's `model_setup.py` generation and the concept explorer's extraction, so that both costingfe and freeform scripts produce data the explorer can consume. This design covers prompt template updates, post-generation validation, extractor routing fix, and an assessment checklist addition.

## Related Artifacts

- **Spec:** `.project/active/common-output-interface/spec.md`
- **Research:** `.project/research/20260406-common-output-interface.md` (Option D analysis, data structure survey)
- **Research:** `.project/research/20260406-model-setup-extraction-interface-gap.md` (gap discovery)

## Research Findings

### Key Files Analyzed

| File | Role | Key Lines |
|------|------|-----------|
| `exploration/concept_analysis/scripts/lib/claude.py` | `run_model()` — post-execution validation | :225-261 |
| `exploration/concept_analysis/scripts/lib/loop.py` | `_run_model_in_iteration()` — calls `run_model()` | :452-514 |
| `exploration/concept_analysis/scripts/lib/validators.py` | `ValidationResult` / `Validator` protocol | :36-45 |
| `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` | costingfe prompt template | Full file |
| `exploration/concept_analysis/prompt_templates/model_setup_freeform.md` | Freeform prompt template | Full file |
| `exploration/concept_analysis/prompt_templates/config/assessment_checklist.md` | Assessment checklist | Full file |
| `exploration/concept_explorer/extract_explorer_data.py` | Extractor routing + both pathways | :554 (routing), :156-219 (costingfe), :227-308 (standalone) |

### Patterns Found

1. **`run_model()` is simple** (`claude.py:225-261`): Runs the script via `uv run python`, checks exit code, non-empty stdout, and "LCOE" in output. Returns `(bool, str)`. Called from three places: `_run_model_in_iteration()` (loop.py:506), `cmd_model_setup` (run_analysis.py:397, :685), and a resume path (run_analysis.py:593). All callers use the same `(ok, msg)` pattern.

2. **Extractor routing is filename-based** (`extract_explorer_data.py:554`): `is_costingfe = (concept_dir / "model_setup.py").exists()`. This is the root cause — freeform scripts also have `model_setup.py`.

3. **Standalone pathway already supports `to_explorer_dict()`** (`extract_explorer_data.py:263-266`): The code loads a `.py` file, checks for `to_explorer_dict`, calls it, and validates via `CostModelData.model_validate()`. This is exactly what freeform scripts need.

4. **`Validator` protocol** (`validators.py:36-45`): `Callable[[str], ValidationResult]` — works on text content. The interface validation we need works on a loaded module, not text. Different mechanism needed.

5. **Assessment template uses `{{@config/assessment_checklist.md}}`** — the checklist is inlined into the prompt via template include. Adding a section is straightforward.

6. **Finding categories** (`assessment.md:29-35`): `analysis` and `model` are the two categories. The `model` category routes findings to the model-setup pass on re-analyze. This is already the correct routing for data model integrity issues.

### Import-Based Detection Approaches

The extractor needs to distinguish costingfe scripts from freeform scripts. Three detection options:

| Approach | Method | Reliability |
|----------|--------|-------------|
| Source scan | `"from costingfe" in source` or `"import costingfe" in source` | Fast, no execution needed, but could false-positive on commented-out imports |
| Module attribute | `hasattr(module, 'model') and isinstance(module.model, CostModel)` | Most reliable, but requires costingfe importable + module already loaded |
| AST scan | Parse source for `costingfe.CostModel(` call | No execution needed, handles comments correctly |

The extractor already loads the module (`load_module_from_path`), so the module attribute approach is the natural fit for the extractor. For `run_model()` validation (which runs the script externally via subprocess), source scanning is the only option without adding module loading.

## Proposed Design

### Component 1: Prompt Template Updates

#### 1a. costingfe template (`model_setup_costingfe.md`)

**Location:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`

Add a new section after "### Structure" item 4 (the `model.forward()` call):

```markdown
### Output Interface (CRITICAL)
The concept explorer consumes `model` and `result` at module level for
cross-concept comparison. You MUST follow this convention:

1. `model = CostModel(...)` at module level (NOT inside a function)
2. `result = model.forward(...)` at module level — this variable MUST be named `result`
3. For multi-scenario scripts (e.g., NOAK vs FOAK), choose the reference case
   (prefer NOAK if available) and assign `result = model.forward(...)` for that case.
   Other scenarios may use any variable name (e.g., `result_foak = model.forward(...)`).
```

This adds ~6 lines to the template. The "CRITICAL" label and capitalized "MUST" match the template's existing style for traceability requirements.

#### 1b. freeform template (`model_setup_freeform.md`)

**Location:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`

Add a new section after "## Sensitivity Analysis":

```markdown
## Output Interface (CRITICAL)
The concept explorer consumes module-level variables and functions for
cross-concept comparison. You MUST expose the following at module level
(outside `main()` or any other function):

### Module-Level Variables
```python
# After defining the dataclass and before main():
params = YourDataclass(...)     # The @dataclass instance with all plant parameters
results = params.compute()      # The full output dict from compute()
```

### Required Functions

#### `to_explorer_dict() -> dict`
Returns a dict with the explorer's expected schema. Map from YOUR compute()
output structure — the keys below are what the explorer requires:
```python
def to_explorer_dict() -> dict:
    """Return structured data for the concept explorer.
    All monetary values in M$ (millions USD). All power values in MW.
    Map from your compute() output to this exact key structure."""
    return {
        "costs": {
            # CAS accounts (lowercase keys, values in M$):
            "cas10": ..., "cas21": ..., "cas22": ..., "cas23": ...,
            "cas24": ..., "cas25": ..., "cas26": ..., "cas27": ...,
            "cas28": ..., "cas29": ..., "cas20": ...,
            "cas30": ..., "cas40": ..., "cas50": ..., "cas60": ...,
            "cas70": ..., "cas71": ..., "cas72": ...,
            "cas80": ..., "cas90": ...,
            "total_capital": ...,       # CAS10-60 sum [M$]
            "lcoe": ...,               # [$/MWh]
            "overnight_cost": ...,     # [$/kW]
        },
        "power_table": {
            "p_fus": ...,        # Fusion power [MW]
            "p_th": ...,         # Total thermal [MW]
            "p_et": ...,         # Gross electric [MW]
            "p_net": ...,        # Net electric [MW]
            "q_sci": ...,        # Scientific Q
            "q_eng": ...,        # Engineering Q
            "availability": ..., # Capacity factor [0-1]
            "rec_frac": ...,     # Recirculating fraction [0-1]
        },
        "cas22_detail": {
            # CAS22 sub-accounts (values in M$):
            "C220101": ..., "C220102": ..., # ... through C220112
            "C220200": ..., "C220300": ..., # ... through C220700
        },
        "params": {
            # All numeric @dataclass fields as {name: value}
        },
        "overridden": [],  # Empty list (freeform scripts don't track overrides)
    }
```

#### `compute_sensitivity() -> dict`
Computes LCOE elasticities for all numeric parameters via central difference:
```python
def compute_sensitivity(dp_fraction=0.01):
    import dataclasses as dc
    base_lcoe = results["economics"]["lcoe_USD_per_MWh"]
    if base_lcoe <= 0:
        return {"engineering": {}, "financial": {}}
    financial_keys = {"interest_rate", "inflation_rate"}
    engineering, financial = {}, {}
    for f in dc.fields(params):
        val = getattr(params, f.name)
        if not isinstance(val, (int, float)) or val == 0.0:
            continue
        dp = abs(val) * dp_fraction
        kw = {**dc.asdict(params), f.name: val + dp}
        lcoe_up = type(params)(**kw).compute()["economics"]["lcoe_USD_per_MWh"]
        kw[f.name] = val - dp
        lcoe_dn = type(params)(**kw).compute()["economics"]["lcoe_USD_per_MWh"]
        elast = (lcoe_up - lcoe_dn) / (2 * dp) * val / base_lcoe
        target = financial if f.name in financial_keys else engineering
        target[f.name] = elast
    return {"engineering": engineering, "financial": financial}
```
```

This is the largest template change (~50 lines). The code examples serve as structural templates for the LLM — the exact variable names will differ per concept but the shape is fixed.

### Component 2: Post-Generation Validation in `run_model()`

**Location:** `exploration/concept_analysis/scripts/lib/claude.py:225-261`

**Approach:** Extend `run_model()` to perform interface validation after the existing checks pass. The validation is informational — warnings printed to stderr. The return type stays `tuple[bool, str]`; callers are unchanged.

**Note on FR-4:** The spec says validation "loads the module and checks" attributes. This design deliberately uses source scanning instead of module loading, because `run_model()` executes the script via subprocess. Loading the module in-process would re-execute it (side effects, duplicate computation, potential import issues). Source scanning is fast and sufficient for detecting naming conventions. The extractor (Component 3) does the authoritative module-level attribute check at extraction time.

**Detection logic inside `run_model()`:** After writing `model_output.txt`, read the source to determine the script type and check interface conformance. Uses the same import-based detection pattern as the extractor (Component 3) — a code comment will note this parallel:

```python
# NOTE: import-based detection logic parallels extract_explorer_data.py routing.
# If you change detection here, update the extractor too.
source = model_path.read_text(encoding="utf-8")
uses_costingfe = "CostModel" in source and ("from costingfe" in source or "import costingfe" in source)
```

Then check:
- **costingfe path:** source-scan for `result = ` at module level (not indented). Check: `re.search(r'^result\s*=', source, re.MULTILINE)`.
- **freeform path:** source-scan for `def to_explorer_dict` at module level.

Warnings are printed to stderr. No caller changes needed.

### Component 3: Extractor Routing Fix

**Location:** `exploration/concept_explorer/extract_explorer_data.py:554`

**Current code:**
```python
is_costingfe = (concept_dir / "model_setup.py").exists()
```

**New code:**
```python
model_setup_path = concept_dir / "model_setup.py"
if model_setup_path.exists():
    source = model_setup_path.read_text(encoding="utf-8")
    is_costingfe = "from costingfe" in source or "import costingfe" in source
else:
    is_costingfe = False
```

This changes routing from filename-based to import-based. Freeform scripts that have `model_setup.py` but don't import costingfe will now route to `extract_standalone()`.

**Edge case — importing costingfe for constants only:** The spec mentions scripts that `import costingfe` for constants but don't instantiate `CostModel`. The source-scan approach would route these to the costingfe pathway, where `extract_costingfe()` would fail because `model` is None. 

Refinement: check for `CostModel` specifically:
```python
is_costingfe = "CostModel" in source and ("from costingfe" in source or "import costingfe" in source)
```

This is more precise. No current freeform script imports costingfe at all, so this handles the edge case without affecting existing scripts.

**Standalone pathway enhancement:** The existing `extract_standalone()` already handles `to_explorer_dict()` at line 263. However, it currently only looks for `.py` files in the concept dir root (line 246-249: `concept_dir.glob("*.py")`). For freeform scripts that ARE `model_setup.py`, this works — `model_setup.py` is in the concept dir root.

One issue: `extract_standalone()` iterates `.py` files and takes the first non-test one (line 246-249). If `model_setup.py` exists alongside other `.py` files, it should be preferred. Current behavior: `sorted()` means `model_setup.py` comes after alphabetically earlier files. Fix: prefer `model_setup.py` if it exists:

```python
# In extract_standalone(), replace the .py file search:
model_setup = concept_dir / "model_setup.py"
if model_setup.exists():
    script_path = model_setup
else:
    for py_file in sorted(concept_dir.glob("*.py")):
        if not py_file.name.startswith("test_"):
            script_path = py_file
            break
```

**Sensitivity extraction for standalone:** When the loaded module has `compute_sensitivity()`, call it and build a `SensitivityAnalysis`:

```python
# After the to_explorer_dict() call in extract_standalone():
compute_sensitivity = getattr(loaded_module, "compute_sensitivity", None)
if compute_sensitivity is not None:
    sens_raw = compute_sensitivity()
    # Build SensitivityAnalysis from the raw dict
    sensitivities = _build_sensitivity_from_dict(sens_raw, raw_dict.get("params", {}))
    cost_model.sensitivities = sensitivities
    has_sensitivities = True
```

A new helper `_build_sensitivity_from_dict()` wraps the raw `{eng: {k: elast}, fin: {k: elast}}` format into `SensitivityAnalysis` with `SensitivityEntry` objects (adding baselines from `params`).

### Component 4: Assessment Checklist Addition

**Location:** `exploration/concept_analysis/prompt_templates/config/assessment_checklist.md`

Add a new section after "## Risk Identification (Goal 5)":

```markdown
## Modeling (Data Model Integrity)
- [ ] If `model_setup.py` exists, its output interface is genuine: `result`
      (costingfe) or `to_explorer_dict()` (freeform) reflects actual model
      computations, not stub values or passthrough wrappers
- [ ] CAS cost values are the result of parameter-driven calculations, not
      hardcoded constants or placeholder zeros across all accounts
- [ ] Sensitivity results (if present) show non-trivial variation — at least
      3 parameters have |elasticity| > 0.01
```

Findings against this section use `Category: model` per FR-8, which is already an established category in the feedback format. No changes to the finding routing logic needed.

## Potential Risks

1. **LLM drift on freeform output interface:** The template additions are detailed but LLMs may still vary the implementation. Mitigation: the post-generation validation warns immediately; the assessor catches quality issues.

2. **Source scanning false positives:** A commented-out `import costingfe` or a string containing "from costingfe" could trigger false detection. Mitigation: unlikely in practice (no current script has this), and the consequence is routing to the wrong pathway which produces a clear error, not silent corruption.

3. **Freeform `compute_sensitivity()` performance:** ~60 forward evaluations per concept at extraction time. Each freeform `compute()` is pure Python arithmetic (~1ms). Total: ~60ms. No risk.

## Integration Strategy

This design touches four independent subsystems that can be implemented and tested in isolation:

1. **Prompt templates** (no code dependencies) — update templates, verify by reading
2. **`run_model()` validation** (lib/claude.py + callers) — unit-testable with fixture scripts
3. **Extractor routing** (extract_explorer_data.py) — testable with existing test suite + new routing tests
4. **Assessment checklist** (config file) — no code change, verify by reading

The changes are additive: existing conforming concepts (01, 07, 08, 10, 14, 28) are unaffected by all four components. Non-conforming concepts get warnings (Component 2) and correct routing (Component 3) but don't block the pipeline.

## Validation Approach

### Automated
- Existing extractor tests continue to pass (costingfe pathway unchanged)
- New test: freeform `model_setup.py` with `to_explorer_dict()` routes to standalone and extracts successfully
- New test: costingfe `model_setup.py` still routes to costingfe pathway
- New test: `run_model()` returns interface warnings for scripts missing `result` or `to_explorer_dict()`
- New test: `run_model()` returns no warnings for conforming scripts

### Manual
- Run extraction on all 11 multi-iteration concepts. Expect: 6 succeed (costingfe), 4 route to standalone (freeform), 1 multi-scenario (09 or 17a) gets a warning
- Pipeline dry-run to verify interface validation output appears in logs

---

## v2 Addendum: Centralized Adapter Fallback (2026-04-07)

### Problem

v1 is implemented: routing fix, templates, `_check_interface()`, checklist all in place. But 2 of 4 freeform scripts (concepts 15, 22) still lack `to_explorer_dict()` — they were generated before the template update or the LLM dropped the function. The extractor warns and produces `cost_model=None` for these.

Re-running the pipeline to regenerate compliant scripts is expensive and fragile. The real issue: all freeform scripts already produce the same `compute()` output shape with standardized CAS keys (enforced by the template's 5-layer architecture). Requiring each script to also implement `to_explorer_dict()` is redundant boilerplate.

### Delta: What Changes

**Only the extractor and template need updates. Everything else from v1 stays.**

#### Change 1: Add centralized adapter in `extract_explorer_data.py`

New function `_freeform_to_explorer_dict(results: dict, params_obj) -> dict` that maps from standard freeform `compute()` output to the explorer dict schema. This is the same mechanical mapping currently in concept 02's `to_explorer_dict()`, but centralized.

The mapping:
- `results["costs"]["CAS10"]` → `"cas10"` (lowercase), etc. for all CAS accounts
- `results["economics"]["CAS70"]` → `"cas70"`, `["lcoe_USD_per_MWh"]` → `"lcoe"`, etc.
- `results["cas22"]["C220101"]` → `"C220101"` (kept uppercase), etc.
- `results["power"]["p_fus"]` → `"p_fus"` scaled by `n_mod`, etc.
- `params_obj` fields → `"params"` dict
- All lookups use `.get(key, 0)` to tolerate missing keys gracefully

#### Change 2: Add centralized sensitivity in `extract_explorer_data.py`

New function `_compute_sensitivity_from_params(params_obj, results: dict) -> dict` — same central-difference elasticity logic currently duplicated in each script's `compute_sensitivity()`, but centralized. Perturbs each float field ±1%, calls `type(params_obj)(**kw).compute()`, computes elasticity. try/except per parameter so one failure doesn't block others.

#### Change 3: Update `extract_standalone()` fallback chain

Current (v1):
```
to_explorer_dict() exists → call it → success
no to_explorer_dict()     → warn, cost_model=None
```

New (v2):
```
to_explorer_dict() exists       → call it (backward compat for concepts 02, 12)
params + results exist as dicts → centralized adapter → success
neither                         → warn, cost_model=None
```

Same pattern for sensitivity: try `compute_sensitivity()` first, fall back to centralized.

Location: `extract_explorer_data.py:294-314` — replace the else branch at line 308.

#### Change 4: Simplify freeform template (going forward)

In `model_setup_freeform.md:95-175`, simplify the "Output Interface (CRITICAL)" section:
- Keep: module-level `params` and `results` requirement
- Remove: `to_explorer_dict()` and `compute_sensitivity()` function requirements (~70 lines)
- Add: brief note that `compute()` must return `{costs, economics, cas22, power}` with standard CAS keys

#### Change 5: Update `_check_interface()` freeform check

In `claude.py:288-295`, check for module-level `params` and `results` instead of `to_explorer_dict`:
```python
has_params = re.search(r"^params\s*=", source, re.MULTILINE)
has_results = re.search(r"^results\s*=", source, re.MULTILINE)
```

### What Does NOT Change (from v1)

- Extractor routing (already import-based) ✓
- costingfe pathway ✓
- costingfe template ✓
- Assessment checklist ✓
- All existing conforming concepts ✓

### Impact

- Concepts 15, 22 become extractable immediately without re-running the pipeline
- Future freeform scripts are simpler to generate (less for LLM to get wrong)
- Concepts 02, 12 unaffected (to_explorer_dict() path still preferred)

---

Next Step: After approval → `/_my_implement`
