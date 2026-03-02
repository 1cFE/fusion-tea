# Fix Plan: Gap 1 — Default Value Extraction

**Date:** 2026-02-01
**Status:** Implemented and verified — see `plan_revisit.md` (2026-02-01)
**Based on:** `findings.md` (diagnostic evidence)

---

## Overview

Five changes needed across two repos. The primary fix (Change 1) fully resolves the empty JSON for the chain spike model. Changes 2-5 are hardening/robustness improvements discovered during investigation.

---

## Change 1: Pass `design_path_filter` from CLI config (PRIMARY FIX)

**Repo:** `sysml-codegen`
**Severity:** Critical — sole root cause of empty JSON

### Option A: Add `design_path_filter` parameter to `build_pipeline_context()` (Recommended)

**File:** `src/sysml_codegen/generation/initialization.py`

**Line 82** — Add parameter to function signature:
```python
def build_pipeline_context(
    model_paths: list[Path],
    targets: list[str] | None = None,
    include_all: bool = True,
    design_path_filter: str = "",    # ← ADD: empty = no filtering
) -> PipelineContext:
```

**Line 140** — Pass the filter:
```python
    design_attrs = extract_design_attributes(extractor.model, design_path_filter=design_path_filter)
```

**File:** `src/sysml_codegen/cli/__init__.py`

**Line 52** — Add to `GenerationConfig`:
```python
    design_path_filter: str = ""   # Empty = accept all design files
```

**Line 610** — Pass through:
```python
    ctx = build_pipeline_context(
        [config.models_path],
        design_path_filter=config.design_path_filter,
    )
```

**Rationale:** The default changes from `"models/designs"` (restrictive, breaks test models) to `""` (permissive). The caller can still restrict if needed. This is safe because:
1. Design attributes are identified by `feature_value_expression` presence, not just path
2. Library calc def inputs (without defaults) are NOT `AttributeUsage` elements with `feature_value_expression`, so they won't pollute the results
3. Library OUTPUT attributes DO have `feature_value_expression`, but their defaults will be non-numeric expressions (OperatorExpressions) — handled by Change 2

### Option B: Change the default filter (Minimal change)

**File:** `src/sysml_codegen/analysis/parameter_groups.py`

**Line 89** — Change default:
```python
    design_path_filter: str = "",   # was: "models/designs"
```

**Tradeoff:** Simpler, but loses the ability for callers to filter. Option A is preferred.

---

## Change 2: Guard `_extract_default_value()` against OperatorExpression crashes

**Repo:** `sysml-codegen`
**Severity:** Medium — prevents crash when path filter matches library files

**File:** `src/sysml_codegen/analysis/parameter_groups.py`

**Lines 186-189** — Wrap `evaluate_true_static_expression()` in try/except:

**Current:**
```python
    elif SysideAdapter.is_instance(expr, "OperatorExpression"):
        # CRITICAL: Import from agentic-mbse
        result = evaluate_true_static_expression(expr)
        return str(result)
```

**Fixed:**
```python
    elif SysideAdapter.is_instance(expr, "OperatorExpression"):
        try:
            result = evaluate_true_static_expression(expr)
            return str(result)
        except (ValueError, TypeError):
            # Non-static expression (references features) — not extractable as default
            return None
```

**Rationale:** `evaluate_true_static_expression()` raises `ValueError` for expressions that reference features (e.g., `length * width` in library output attrs). This is expected — these are not design defaults. Returning `None` lets the extraction continue gracefully. Confirmed by Script 1: broad filters crash at this exact location.

---

## Change 3: (Optional) Fix Strategy 1 qualified name matching

**Repo:** `sysml-codegen`
**Severity:** Low — safety net works correctly, Strategy 1 is effectively dead code

**File:** `src/sysml_codegen/resolution/graph_builder.py`

**Lines 210-215** — The `design_attr_by_qname` index uses design attribute qualified names (`ChainSpikeDesign__spike_design__length`), but entry point names include the calc usage segment (`ChainSpikeDesign__spike_design__area_calc__length`). Strategy 1's `qname in design_attr_by_qname` check at line 233 can never match.

**Two possible fixes:**

**3a: Add suffix matching** (line 233):
```python
        # Strategy 1: Design attribute match (check by suffix/simple_name)
        matching_attr = None
        for da_qname, attr in design_attr_by_qname.items():
            if qname.endswith(f"__{attr.name}") and attr.parent_part in qname:
                matching_attr = attr
                break
        if matching_attr is not None:
            entry_type = EntryPointType.DESIGN_ATTRIBUTE
            if matching_attr.default_value:
                try:
                    default_value = float(matching_attr.default_value)
                except (ValueError, TypeError):
                    pass
```

**3b: Leave as-is** — The safety net at `_group_entry_points_via_deriver()` (lines 326-336) correctly handles this via `ParameterGroupDeriver.get_default_value()`. The only consequence is `entry_type=USAGE_LITERAL` instead of `DESIGN_ATTRIBUTE`, which is cosmetic.

**Recommendation:** Defer (3b). The safety net works. Fix only if entry_type accuracy matters for downstream consumers.

---

## Change 4: Add extractability validation to Level 8

**Repo:** `agentic-mbse`
**Severity:** Medium — prevents silent codegen failures

**File:** `src/agentic_mbse/validation/level8_codegen.py`

**In `check_design_attr_completeness()`, after line 421** — Add extraction test:

```python
        # Existing check (line 418-421):
        has_value = (
            hasattr(attr, "feature_value_expression")
            and attr.feature_value_expression is not None
        )

        # NEW: Verify the expression is actually extractable
        if has_value:
            from agentic_mbse.sysml.expression import evaluate_true_static_expression
            try:
                evaluate_true_static_expression(attr.feature_value_expression)
            except (ValueError, TypeError) as e:
                issues.append(QualityCheckResult(
                    check_id="L8_DESIGN_ATTR_UNEXTRACTABLE",
                    severity="error",
                    message=(
                        f"Design attribute '{attr_name}' has expression but codegen "
                        f"cannot extract a numeric default: {e}"
                    ),
                    file=str(source_file),
                    line=source_line,
                ))
```

**Rationale:** Currently, Level 8 checks that `feature_value_expression` exists but not that it produces a usable value. A model can pass all 8 validation levels and still produce empty JSON.

---

## Change 5: Align validation path filter with codegen path filter

**Repo:** `agentic-mbse`
**Severity:** Low — informational consistency

**File:** `src/agentic_mbse/validation/level8_codegen.py`

**Line 400** — Currently:
```python
        if "designs" not in doc_path.parts:
            continue
```

**Recommendation:** Document that this filter is intentionally different from the codegen filter, or parameterize it. If Change 1 Option A is implemented (empty default filter), this divergence becomes moot since codegen will process all files.

---

## Test Strategy

### Unit Tests (sysml-codegen)

1. **Test `extract_design_attributes()` with various path filters:**
   ```python
   def test_extract_design_attributes_default_filter():
       """Default filter should not exclude test models."""
       # Load chain spike model
       # Call extract_design_attributes(model)  # no filter arg
       # Assert 3 attributes returned with non-None defaults
   ```

2. **Test `_extract_default_value()` with OperatorExpression:**
   ```python
   def test_extract_default_value_operator_expression():
       """Non-static OperatorExpressions should return None, not crash."""
       # Load chain spike model (includes library with output expressions)
       # Call extract_design_attributes(model, design_path_filter="")
       # Assert no crash, non-literal attrs have None default
   ```

3. **Test full pipeline produces populated JSON:**
   ```python
   def test_chain_spike_json_populated():
       """build_pipeline_context should produce entry points with defaults."""
       ctx = build_pipeline_context([chain_spike_model_path])
       for group in ctx.computation_graph.entry_point_groups:
           for ep in group.parameters:
               assert ep.default_value is not None, f"{ep.qualified_name} has None default"
   ```

### Integration Test (fusion-tea)

```bash
# Re-run codegen on chain spike model
cd /home/reid/1cfe/fusion-tea
uv run sysml-codegen generate \
    --models models/tests/codegen_chain_spike/ \
    --output generated/codegen_chain_spike/ \
    --package-name chain_spike

# Verify JSON is populated
uv run python -c "
import json
data = json.load(open('generated/codegen_chain_spike/inputs/design_params.json'))
assert len(data) == 3, f'Expected 3 params, got {len(data)}'
assert data['ChainSpikeDesign__spike_design__area_calc__length'] == 10.0
assert data['ChainSpikeDesign__spike_design__area_calc__width'] == 5.0
assert data['ChainSpikeDesign__spike_design__cost_calc__rate'] == 12.0
print('PASS: design_params.json is correctly populated')
"
```

---

## Implementation Priority

| Change | Priority | Risk | Effort |
|--------|----------|------|--------|
| 1 (path filter fix) | **P0** — blocks all codegen | Very Low | Small (3 files, ~10 lines) |
| 2 (crash guard) | P1 — prevents crashes | Very Low | Trivial (4 lines) |
| 4 (validation check) | P2 — prevents silent failures | Low | Small (15 lines) |
| 5 (filter consistency) | P3 — documentation | Zero | Trivial (comment) |
| 3 (Strategy 1 fix) | P4 — cosmetic | Low | Medium (refactor matching logic) |

**Recommended order:** 1 → 2 → 4 → 5 → 3 (or skip 3 entirely)
