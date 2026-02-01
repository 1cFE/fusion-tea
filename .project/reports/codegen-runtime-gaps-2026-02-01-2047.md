# Codegen Runtime Gaps: Pipeline Cannot Execute Without Manual Fixes

**Date:** 2026-02-01
**Context:** Audit of codegen-chain-spike (Item 2, end-to-end pipeline derisking epic)
**Severity:** Major — generated code does not run without manual intervention
**Codegen repo:** `/home/reid/1cfe/sysml-codegen/`

---

## Executive Summary

The codegen chain spike (Item 2) was marked GO with "all 4 evaluation stages passed, zero failures." This verdict evaluated **structural correctness** — whether the right files exist with the right wiring. It did not attempt to **run the generated pipeline**.

When actually executing the pipeline via `execute_pipeline()`, three gaps prevent execution. All three require manual workarounds. These gaps will recur for Items 4-5 (solar+battery codegen) unless fixed in sysml-codegen.

---

## Gap 1: `design_params.json` Generated Empty

### Symptom

The generated `inputs/design_params.json` contains `{}`. The `DesignParams` schema in `schemas/design_params.py` correctly declares the three required fields (no defaults), so the EntryPoint module fails at runtime when loading the empty JSON.

**Generated schema (correct):**
```python
class DesignParams(BaseModel):
    ChainSpikeDesign__spike_design__area_calc__length: float = Field(description="Entry point: length")
    ChainSpikeDesign__spike_design__area_calc__width: float = Field(description="Entry point: width")
    ChainSpikeDesign__spike_design__cost_calc__rate: float = Field(description="Entry point: rate")
    model_config = {"frozen": True, "extra": "forbid"}
```

**Generated JSON (broken):**
```json
{}
```

**Expected JSON:**
```json
{
    "ChainSpikeDesign__spike_design__area_calc__length": 10.0,
    "ChainSpikeDesign__spike_design__area_calc__width": 5.0,
    "ChainSpikeDesign__spike_design__cost_calc__rate": 12.0
}
```

These values exist in the SysML model as attribute defaults (`attribute length : Real = 10.0;` etc.) and are available during extraction.

### Root Cause

**File:** `sysml-codegen/src/sysml_codegen/generation/entry_point.py`
**Function:** `generate_all_derived_jsons_from_graph()` (lines 595-631)

The JSON writer skips parameters whose `default_value` is `None`:

```python
data = {}
for ep in group.parameters:
    if ep.default_value is not None:
        data[ep.qualified_name] = ep.default_value
```

The defaults are `None` because the upstream extraction doesn't propagate them. The classification logic in `graph_builder.py` function `_classify_entry_points()` (lines 179-281) has three cases for extracting defaults:

1. **DESIGN_ATTRIBUTE** (lines 233-240): Parses `attr.default_value` from string — may fail on numeric types
2. **LIBRARY_DEFAULT** (lines 243-254): Calls `_get_library_default()` with `float()` conversion — may fail silently
3. **USAGE_LITERAL** (lines 259-267): Tries to parse `source_path` as float — likely fails

There's also a merge attempt in `_group_entry_points_via_deriver()` (lines 327-336) where `ParameterSource.default_value` can override `None`, suggesting the classification path is known to be incomplete.

### Fix Scope

Medium. Requires tracing the default value through the extraction pipeline:
- `extraction/data_models.py` — `AttributeInfo.default_value` field typing
- `resolution/graph_builder.py` — `_classify_entry_points()` all three branches
- `generation/entry_point.py` — downstream consumer (correct once defaults flow through)

### Manual Workaround

Populate the JSON by hand using the SysML model attribute defaults:

```bash
cat > generated/codegen_chain_spike/inputs/design_params.json << 'EOF'
{
    "ChainSpikeDesign__spike_design__area_calc__length": 10.0,
    "ChainSpikeDesign__spike_design__area_calc__width": 5.0,
    "ChainSpikeDesign__spike_design__cost_calc__rate": 12.0
}
EOF
```

---

## Gap 2: ExitPoint Type `RootModel[float]` Has No Output Router Handler

### Symptom

Pipeline execution fails at validation with:

```
simkit.core.pipeline_validator.PipelineValidationError: ExitPoint output type has no registered write handler
```

The ExitPoint in the generated pipeline YAML declares `RootModel[float]` as the output type for all three calc results:

```yaml
exit_point:
    module_type: ExitPoint
    outputs:
      ChainSpikeDesign__spike_design__area_calc__area: RootModel[float] ChainSpikeDesign__spike_design__area_calc__area.json
      ChainSpikeDesign__spike_design__cost_calc__total_cost: RootModel[float] ChainSpikeDesign__spike_design__cost_calc__total_cost.json
      ChainSpikeDesign__spike_design__summary__cost_per_area: RootModel[float] ChainSpikeDesign__spike_design__summary__cost_per_area.json
```

But the generated `__init__.py` only registers `DesignParams` in `CUSTOM_SCHEMA_TYPES`:

```python
CUSTOM_SCHEMA_TYPES = [    DesignParams]
```

When `execute_pipeline()` auto-creates the output router from `CUSTOM_SCHEMA_TYPES`, it registers handlers for `["DesignParams"]` plus built-in TEAx types. `RootModel[float]` is not among them.

### Root Cause

**File:** `sysml-codegen/src/sysml_codegen/generation/registry.py`
**Function:** `generate_registry_function()` (lines 30-74)
**Template:** `sysml-codegen/src/sysml_codegen/templates/registry_function.py.jinja2` (lines 38-47)

`CUSTOM_SCHEMA_TYPES` is populated only from `entry_point_groups` (parameter group schemas). Exit point types are generated in a completely separate path:

- `generation/pipeline.py` function `_build_exit_points()` (lines 196-227) generates the `RootModel[float]` type string at line 218
- But this information is **never passed** to `generate_registry_function()`
- The CLI orchestrator at `cli/__init__.py:317-343` only passes `entry_point_groups` to the registry generator

### Fix Scope

Trivial to small. Options:

1. **Trivial**: Hardcode `"RootModel[float]"` (and other primitive wrappers) as always-registered types in the template
2. **Small**: Pass the set of unique ExitPoint types from `ComputationGraph` to `generate_registry_function()` and include them in `CUSTOM_SCHEMA_TYPES`

Option 2 is more correct — it handles any output type, not just `RootModel[float]`.

### Manual Workaround

Create the output router explicitly when calling `execute_pipeline`:

```python
from simkit.io.output_router import create_output_router_with_json_schemas
from chain_spike import create_chain_spike_registry, CUSTOM_SCHEMA_TYPES

registry = create_chain_spike_registry()

# Must manually add RootModel[float] — codegen doesn't include it
type_names = [t.__name__ for t in CUSTOM_SCHEMA_TYPES] + ['RootModel[float]']
router = create_output_router_with_json_schemas(type_names, include_builtins=True)

result = execute_pipeline(
    spec_path='generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml',
    output_dir='generated/codegen_chain_spike/test_run_output',
    registry=registry,
    output_router=router,
    custom_schema_types=CUSTOM_SCHEMA_TYPES,
)
```

---

## Gap 3: `chain_spike_schemas.py` Contains Unrelated `FusionParams`

### Symptom

The generated package includes `chain_spike_schemas.py` containing a `FusionParams` class with PyFECONS CATF/MFE-specific fields (`p_fusion`, `eta_thermal`, `m_neutron`, etc.). This class is:

- Not referenced by any module wrapper
- Not referenced by the pipeline YAML
- Not referenced by `CUSTOM_SCHEMA_TYPES`
- Specific to a completely different domain (fusion reactor physics vs. the spike's trivial area/cost domain)

```python
class FusionParams(BaseModel):
    """Fusion reactor parameters for CATF MFE design.
    Source: PyFECONS CATF/mfe/DefineInputs.py
    """
    p_fusion: float = Field(..., gt=0, description="Total fusion power [MW]")
    p_input: float = Field(..., ge=0, description="Auxiliary heating power [MW]")
    m_neutron: float = Field(..., ge=1.0, le=1.5, description="Neutron multiplication factor")
    # ... 5 more fusion-specific fields
```

### Root Cause

**File:** `sysml-codegen/src/sysml_codegen/cli/__init__.py`
**Function:** `_generate_schemas()` (lines 127-162)

A static template file is **unconditionally copied** into every generated package:

```python
ref_schema = Path(__file__).parent.parent / "templates" / "schemas_ref.py"
if ref_schema.exists():
    dest = config.output_path / f"{config.package_name}_schemas.py"
    shutil.copy(ref_schema, dest)
```

**Template file:** `sysml-codegen/src/sysml_codegen/templates/schemas_ref.py`

This is a leftover from early development when the codegen was hardcoded for fusion models. The CLI header comments (lines 3-7) reference "CRITICAL CHANGES: Parameterized all hardcoded values — Removed CATF-specific references" — but this template was not cleaned up as part of that work.

### Fix Scope

Trivial. Either:
1. Delete `templates/schemas_ref.py` and remove the copy operation
2. Make the copy conditional on whether the model actually uses fusion-specific schemas
3. Generate `{package}_schemas.py` dynamically from model content instead of copying a static file

### Impact

Low direct impact (unused file), but it creates confusion about what the codegen is model-aware vs. hardcoded. For Items 4-5 where `FusionParams` *is* relevant, this file would coincidentally appear correct while still being a static copy rather than generated from the model.

---

## Reproduction Steps

### Prerequisites

```bash
# Working directory
cd /home/reid/1cfe/fusion-tea

# Ensure stencils are implemented (or use the ones already filled in)
# areacalc_impl.py:  return inputs.length * inputs.width
# costcalc_impl.py:  return inputs.area * inputs.rate
# summarycalc_impl.py: return inputs.cost / inputs.area
```

### Reproduce Gap 1 (empty JSON)

```bash
# Reset the JSON to the codegen-generated state
echo '{}' > generated/codegen_chain_spike/inputs/design_params.json

# Attempt to run — will fail at EntryPoint loading
PYTHONPATH="generated:$PYTHONPATH" uv run python -c "
from simkit.core.pipeline import execute_pipeline
from chain_spike import create_chain_spike_registry, CUSTOM_SCHEMA_TYPES
from simkit.io.output_router import create_output_router_with_json_schemas

registry = create_chain_spike_registry()
type_names = [t.__name__ for t in CUSTOM_SCHEMA_TYPES] + ['RootModel[float]']
router = create_output_router_with_json_schemas(type_names, include_builtins=True)

result = execute_pipeline(
    spec_path='generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml',
    output_dir='/tmp/chain_spike_test',
    registry=registry,
    output_router=router,
    custom_schema_types=CUSTOM_SCHEMA_TYPES,
)
"
```

### Reproduce Gap 2 (missing RootModel handler)

```bash
# Populate JSON first (fix Gap 1) so we reach Gap 2
cat > generated/codegen_chain_spike/inputs/design_params.json << 'ENDJSON'
{
    "ChainSpikeDesign__spike_design__area_calc__length": 10.0,
    "ChainSpikeDesign__spike_design__area_calc__width": 5.0,
    "ChainSpikeDesign__spike_design__cost_calc__rate": 12.0
}
ENDJSON

# Use ONLY the generated CUSTOM_SCHEMA_TYPES (no manual RootModel registration)
PYTHONPATH="generated:$PYTHONPATH" uv run python -c "
from simkit.core.pipeline import execute_pipeline
from chain_spike import create_chain_spike_registry, CUSTOM_SCHEMA_TYPES

registry = create_chain_spike_registry()

result = execute_pipeline(
    spec_path='generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml',
    output_dir='/tmp/chain_spike_test',
    registry=registry,
    custom_schema_types=CUSTOM_SCHEMA_TYPES,
)
"
# Expected error:
# PipelineValidationError: ExitPoint output type has no registered write handler
```

### Reproduce Gap 3 (FusionParams template)

```bash
# Inspect the file — FusionParams has nothing to do with the chain spike model
cat generated/codegen_chain_spike/chain_spike_schemas.py
# Shows FusionParams with p_fusion, eta_thermal, m_neutron, etc.

# Verify it's unused
grep -r "FusionParams" generated/codegen_chain_spike/ --include="*.py" --include="*.yaml"
# Only hit is chain_spike_schemas.py itself and its __all__
```

### Successful Run (all gaps manually resolved)

```bash
# Requires: symlink for package imports
ln -sfn generated/codegen_chain_spike generated/chain_spike

PYTHONPATH="generated:$PYTHONPATH" uv run python -c "
from simkit.core.pipeline import execute_pipeline
from simkit.io.output_router import create_output_router_with_json_schemas
from chain_spike import create_chain_spike_registry, CUSTOM_SCHEMA_TYPES

registry = create_chain_spike_registry()
type_names = [t.__name__ for t in CUSTOM_SCHEMA_TYPES] + ['RootModel[float]']
router = create_output_router_with_json_schemas(type_names, include_builtins=True)

result = execute_pipeline(
    spec_path='generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml',
    output_dir='/tmp/chain_spike_test',
    registry=registry,
    output_router=router,
    custom_schema_types=CUSTOM_SCHEMA_TYPES,
)

print('Outputs:', dict(result.outputs))
# Expected:
#   area_calc__area: 50.0       (10.0 * 5.0)
#   cost_calc__total_cost: 600.0 (50.0 * 12.0)
#   summary__cost_per_area: 12.0 (600.0 / 50.0)
"
```

---

## Additional Finding: Package Name vs Directory Mismatch

The generated code uses `from chain_spike.modules...` but the output directory is `codegen_chain_spike/`. This requires either a symlink (`ln -sfn codegen_chain_spike chain_spike`) or `PYTHONPATH` manipulation. This is a convention issue rather than a bug — the `--package-name chain_spike` flag sets the import name while `--output` sets the directory. But it means there's no way to `import chain_spike` without manual setup.

---

## Impact on Items 4-5

All three gaps will recur when codegen runs on the solar+battery model:

| Gap | Items 4-5 Impact |
|-----|------------------|
| Empty `design_params.json` | Will need ~15-20 entry-point values populated by hand |
| Missing `RootModel[float]` handler | Same error — 5 calc outputs all use `RootModel[float]` |
| `FusionParams` template | Will coincidentally look correct for fusion, masking the bug |

Gaps 1 and 2 are **blockers** for any `execute_pipeline()` call on generated output. They should be fixed in sysml-codegen before Items 4-5 proceed, or documented as mandatory manual post-generation steps.

---

## Source References

| File | Lines | What |
|------|-------|------|
| `sysml-codegen/src/sysml_codegen/generation/entry_point.py` | 595-631 | JSON generation (Gap 1 symptom) |
| `sysml-codegen/src/sysml_codegen/resolution/graph_builder.py` | 179-281 | Default value extraction (Gap 1 root cause) |
| `sysml-codegen/src/sysml_codegen/generation/registry.py` | 30-74 | Registry/CUSTOM_SCHEMA_TYPES generation (Gap 2) |
| `sysml-codegen/src/sysml_codegen/templates/registry_function.py.jinja2` | 38-47 | Template for CUSTOM_SCHEMA_TYPES (Gap 2) |
| `sysml-codegen/src/sysml_codegen/generation/pipeline.py` | 196-227 | ExitPoint type generation (Gap 2 source of RootModel type) |
| `sysml-codegen/src/sysml_codegen/cli/__init__.py` | 127-162 | Unconditional schema copy (Gap 3) |
| `sysml-codegen/src/sysml_codegen/templates/schemas_ref.py` | entire | Static FusionParams template (Gap 3) |
