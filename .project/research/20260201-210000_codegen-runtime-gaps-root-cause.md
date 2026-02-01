---
date: 2026-02-01T21:00:00-05:00
researcher: Claude
topic: "Codegen runtime gaps root cause analysis"
tags: [research, sysml-codegen, migration, regression]
status: complete
last_updated: 2026-02-01
---

# Research: Codegen Runtime Gaps — Root Cause Analysis

**Date**: 2026-02-01T21:00:00-05:00
**Researcher**: Claude
**Research Type**: Codebase / Migration Regression Analysis

## Research Question

Three gaps prevent generated codegen output from executing without manual intervention. Were these introduced during the monorepo→3-repo migration, or are they pre-existing? What exactly broke, and where are the fixes?

## Summary

- **Gap 1 (Empty JSON)**: Hybrid — the codegen logic is identical between old and new repos, but the extractor's `_extract_default_value()` now wraps values with `str()`, AND the adapter abstraction may fail to match literal types in edge cases. Additionally, the DesignAttributeData objects may not have `default_value` populated by the SysML extraction layer. The old repo had a **dedicated fix** (commit `af10e0a`, research report `20251208-172130`) that switched JSON generation from `generate_parameter_group_jsons()` to `generate_all_derived_jsons()` — this fix exists in the new code but the upstream default extraction pipeline still drops values.
- **Gap 2 (Missing RootModel[float] handler)**: **Pre-existing**. Never fixed in codegen. The old repo used a manual workaround in `run_fusion_simkit_pipeline.py` (commit `09a4466`) that explicitly registered `RootModel[float]` as a write handler. This workaround was never codegen-ized.
- **Gap 3 (Static FusionParams)**: **Pre-existing**. Always a static template copy. The old repo was CATF-only so it didn't matter. Now model-agnostic, it's a visible bug.

## Detailed Findings

### Gap 1: Empty design_params.json

#### History in fusion_modeling (7 research reports)

This was the most-investigated codegen issue in the old repo:

| Report | Key Finding |
|--------|-------------|
| `20251208-172130_json-default-value-extraction-bug.md` | Root cause: reading from `AttributeInfo.default_value` (calc def inputs, no defaults) instead of `DerivedParameterGroup.parameters[].default_value` (design attributes, have defaults) |
| `20251219-224500_null-value-root-cause-analysis.md` | 16 null values remained; 15/16 are wiring params (not true entry points); only `magnet_volume` was a real missing default |
| `20251207-105523_codegen-v2-implementation-gap.md` | Two codegen pipelines exist: Phase A (from library) and Phase B (with design defaults); user was only running Phase A |
| `20251201-120000_entry-point-identification-analysis.md` | Entry points identified by binding chain backtracing, not "unbound params" |

The fix applied in the old repo (commit `af10e0a`) switched from `generate_parameter_group_jsons()` to `generate_all_derived_jsons()`. The old repo's `fusion_simkit/inputs/*.json` files are all **populated with actual values**.

#### What Changed in Migration

Two changes in the extraction layer:

1. **`_extract_default_value()` now returns `str` instead of native types**:
   - OLD (`sysml_to_teax.py:510`): `return value` — returns native float/int
   - NEW (`extractor.py:342`): `return str(value)` — wraps with str()
   - Impact: Benign for Gap 1. The downstream `graph_builder.py:238` does `float(attr.default_value)` which handles both `float(0.5)` and `float("0.5")`.

2. **`_extract_literal_value()` uses adapter instead of direct isinstance**:
   - OLD (`sysml_to_teax.py:551`): `isinstance(expr, syside.LiteralRational)`
   - NEW (`extractor.py:364`): `self.adapter.is_instance(expr, "LiteralRational")`
   - Impact: The adapter's `is_instance()` uses `elem.isinstance(sysml_type)` (syside's isinstance, not Python's). This SHOULD work identically, but adds an indirection layer that could fail if syside's `.isinstance()` method doesn't match Python `isinstance()` for literal types. The `LiteralRational` IS in the adapter's TYPE_MAP (line 152), so this is not a missing mapping.

3. **Strategy 2 in `_extract_default_value()` changed membership filtering**:
   - OLD (`sysml_to_teax.py:520`): `isinstance(membership, syside.FeatureValue)` — direct Python isinstance
   - NEW (`extractor.py:348`): `hasattr(membership, 'is_default')` — duck-typing check
   - Impact: Potentially different filtering behavior. The old code requires the membership to be a `FeatureValue` instance. The new code only checks for `is_default` attribute presence, which could match more or fewer memberships.

#### Where the Default Actually Gets Lost

The `_classify_entry_points()` in `graph_builder.py:232-240` has three strategies for finding defaults. For the chain spike model, Strategy 1 (DESIGN_ATTRIBUTE) applies. The logic at line 236:

```python
if attr.default_value:
    try:
        default_value = float(attr.default_value)
    except (ValueError, TypeError):
        pass
```

This reads `attr.default_value` from `DesignAttributeData`, which is populated by the extraction layer. If the extraction layer's `_extract_default_value()` returns `None` for chain spike attributes (because the literal value extraction failed via the adapter), then `DesignAttributeData.default_value` is `None`, and the JSON gets `{}`.

**Most likely root cause**: The adapter's `is_instance()` method doesn't match literal expressions in the chain spike SysML model, causing `_extract_literal_value()` to return `None`, which propagates through to empty JSON.

#### Fix Location

Primary: `sysml-codegen/src/sysml_codegen/extraction/extractor.py:359-373` — `_extract_literal_value()` needs debugging to confirm whether the adapter correctly identifies `LiteralRational` etc. for chain spike model elements.

Secondary: `sysml-codegen/src/sysml_codegen/resolution/graph_builder.py:232-240` — the `float()` conversion is a fallback; if the value was already extracted as native float/int, the `str()` wrapping adds an unnecessary round-trip.

### Gap 2: Missing RootModel[float] Handler

#### History in fusion_modeling (3 research reports)

| Report | Key Finding |
|--------|-------------|
| `20251224-041936_exitpoint-write-handler-error.md` | Root cause: `pipeline_generator.py:187` emits `RootModel[float]` type string but output router has no handler for it |
| `20251208-062018_type-mismatch-rootmodel-vs-float.md` | TEAx design: module inputs use raw `float`, outputs use `RootModel[float]` |
| `20251207-225800_codegen-remaining-issues.md` | Documented as primary pipeline blocker alongside hardcoded PARAMETER_GROUPS |

The fix was a **manual workaround** in the run script, NOT in codegen:

```python
# File: ~/fusion_modeling/scripts/run_fusion_simkit_pipeline.py:22-28
json_handler = WriteHandler(fn=writers.write_json_model, extension=".json")
router.register_handler("RootModel[float]", json_handler)
primitive_handler = WriteHandler(fn=write_json_primitive, extension=".json")
router.register_handler("float", primitive_handler)
```

#### What Changed in Migration

**Nothing.** The codegen logic for exit points is identical:
- `pipeline_generator.py:198-229` (old) ≡ `pipeline.py:196-227` (new)
- `registration.py` (old) ≡ `registry.py` (new)
- `registry_function.py.jinja2` template: identical

The `CUSTOM_SCHEMA_TYPES` was always populated only from entry point parameter groups (e.g., `HeatingParams`, `PhysicsParams`). Exit point types (`RootModel[float]`) were never included.

#### Fix Options

1. **Trivial (recommended for immediate unblock)**: Have the codegen generate a `RootModel[float]` registration in the `__init__.py` or run script template. The codegen already generates `primitives.py` with `Float = RootModel[float]` — it just needs to register it.

2. **Proper**: Pass the set of unique exit point types from `ComputationGraph` to `generate_registry_function()` and include them in `CUSTOM_SCHEMA_TYPES` or generate explicit handler registrations.

#### Fix Location

- `sysml-codegen/src/sysml_codegen/generation/registry.py:30-74` — add exit point type collection
- `sysml-codegen/src/sysml_codegen/templates/registry_function.py.jinja2:38-47` — include exit point types in CUSTOM_SCHEMA_TYPES or generate handler registrations
- `sysml-codegen/src/sysml_codegen/cli/__init__.py:317-343` — pass exit point types to registry generator

### Gap 3: Static FusionParams Template

#### History

The `schemas_ref.py` template was introduced in the old repo (commit `d8115d0`) as a hardcoded "golden standard" schema with 8 PyFECONS CATF/MFE parameters. It was unconditionally copied by `generate_catf_code.py:237-249`.

During migration, the copy operation was preserved in `cli/__init__.py:127-143` with the filename parameterized (`{package_name}_schemas.py`) but content unchanged.

#### What Changed in Migration

Only the output filename changed:
- OLD: Always `fusion_schemas.py`
- NEW: `{config.package_name}_schemas.py` (parameterized)

Content is identical: 8 hardcoded FusionParams fields. The CLI header comments (lines 3-7) say "CRITICAL CHANGES: Parameterized all hardcoded values — Removed CATF-specific references" but this template was NOT cleaned up.

#### Fix Options

1. **Trivial (recommended)**: Delete `templates/schemas_ref.py` and remove the copy operation from `cli/__init__.py`. The file is unused by any generated code — `CUSTOM_SCHEMA_TYPES` only references dynamically generated schema classes.
2. **Proper**: Generate `{package}_schemas.py` dynamically from model content instead of copying a static file.

#### Fix Location

- Delete: `sysml-codegen/src/sysml_codegen/templates/schemas_ref.py`
- Edit: `sysml-codegen/src/sysml_codegen/cli/__init__.py:127-162` — remove the `_generate_schemas()` static copy

## Code References

### Old Repo (fusion_modeling)

| File | Lines | What |
|------|-------|------|
| `scripts/sysml_to_teax.py` | 484-536 | Old `_extract_default_value()` — returns native types |
| `scripts/sysml_to_teax.py` | 538-561 | Old `_extract_literal_value()` — uses direct `isinstance()` |
| `scripts/codegen/graph_builder.py` | 179-281 | `_classify_entry_points()` — identical to new |
| `scripts/codegen/entry_point.py` | 595-631 | JSON generation — identical to new |
| `scripts/run_fusion_simkit_pipeline.py` | 22-28 | **Manual RootModel[float] handler fix** |
| `scripts/generate_catf_code.py` | 237-249 | Static `fusion_schemas_ref.py` copy |
| `scripts/templates/fusion_schemas_ref.py` | entire | Static FusionParams template |

### New Repo (sysml-codegen)

| File | Lines | What |
|------|-------|------|
| `src/sysml_codegen/extraction/extractor.py` | 336-357 | New `_extract_default_value()` — wraps with `str()` |
| `src/sysml_codegen/extraction/extractor.py` | 359-373 | New `_extract_literal_value()` — uses adapter |
| `src/sysml_codegen/resolution/graph_builder.py` | 179-281 | `_classify_entry_points()` — identical to old |
| `src/sysml_codegen/generation/entry_point.py` | 595-631 | JSON generation — identical to old |
| `src/sysml_codegen/generation/registry.py` | 30-74 | Registry generation — no exit point types |
| `src/sysml_codegen/generation/pipeline.py` | 196-227 | `_build_exit_points()` — generates RootModel[float] strings |
| `src/sysml_codegen/cli/__init__.py` | 127-162 | `_generate_schemas()` — unconditional static copy |
| `src/sysml_codegen/templates/schemas_ref.py` | entire | Static FusionParams template (unchanged) |

### Adapter (agentic-mbse)

| File | Lines | What |
|------|-------|------|
| `src/agentic_mbse/sysml/syside_adapter.py` | 151-154 | TYPE_MAP includes LiteralRational/Integer/Boolean/String |
| `src/agentic_mbse/sysml/syside_adapter.py` | 230-257 | `is_instance()` — adapter indirection for type checking |

## Architecture Insights

1. **The migration was structurally faithful** — codegen logic files are nearly line-for-line identical between old and new repos. Import paths changed, type annotations modernized, but algorithms preserved.

2. **Two changes introduced risk in the extraction layer**: (a) the `str()` wrapping of default values, and (b) the adapter abstraction replacing direct `isinstance()` checks. Both are defensible design choices but created a subtle regression path.

3. **The old repo relied on manual workarounds** rather than fixing codegen itself for Gaps 2 and 3. The migration faithfully preserved the codegen code but did NOT port the workarounds from `run_fusion_simkit_pipeline.py`.

4. **The `_group_entry_points_via_deriver()` merge at graph_builder.py:326-336** has a safety net: if `EntryPoint.default_value` is `None` but `ParameterSource.default_value` is not, it merges. This suggests the team knew the classification path was incomplete.

## Feasibility Assessment

All three gaps are fixable in `sysml-codegen`:

| Gap | Fix Difficulty | Risk | Approach |
|-----|---------------|------|----------|
| 1 | Medium | Low | Debug `_extract_literal_value()` with adapter on chain spike model; verify `DesignAttributeData.default_value` is populated; if adapter is fine, trace through `_classify_entry_points()` to find where value drops |
| 2 | Small | Very Low | Add exit point types to `CUSTOM_SCHEMA_TYPES` or generate explicit handler registrations in the template |
| 3 | Trivial | Zero | Delete `schemas_ref.py` and remove the copy operation |

## Recommendations

### Immediate (fix in sysml-codegen before Items 4-5)

1. **Gap 3 first** — trivial delete, zero risk, removes confusion
2. **Gap 2 second** — small template change, straightforward
3. **Gap 1 third** — requires debugging the extraction pipeline; write a test that runs the extractor on the chain spike SysML model and asserts non-None `default_value` on the extracted attributes

### Diagnostic for Gap 1

Run a targeted extraction test:
```python
# Extract chain spike model and check default values
from sysml_codegen.extraction.extractor import SysMLDataExtractor
extractor = SysMLDataExtractor(adapter)
data = extractor.extract(["models/tests/codegen_chain_spike/"])
for calc in data.calculations:
    for attr in calc.input_attributes:
        print(f"{calc.calc_name}.{attr.name}: default={attr.default_value}")
```

If defaults show up here but not in the JSON, the bug is in `graph_builder.py` classification. If defaults are `None` here, the bug is in the extractor/adapter layer.

## Open Questions

1. Does `syside`'s `.isinstance()` method (used by the adapter) behave identically to Python `isinstance()` for literal types? The old code used Python `isinstance(expr, syside.LiteralRational)` while the new code uses `elem.isinstance(syside.LiteralRational)`. These are different mechanisms.

2. Were there any syside version changes between the old and new repos that might affect literal type resolution?

3. The `FeatureValue` filtering changed from `isinstance(membership, syside.FeatureValue)` to `hasattr(membership, 'is_default')` — does this duck-typing approach match the same set of memberships?
