# Findings: Gap 1 — Default Value Extraction Debug

**Date:** 2026-02-01
**Status:** Complete — Fix verified in `plan_revisit.md` (2026-02-01)
**Branch:** visualization

---

## Confirmed Root Cause

**The sole root cause for empty `design_params.json` is a path filter mismatch (Delta D).**

`extract_design_attributes()` at `parameter_groups.py:87-127` defaults to `design_path_filter="models/designs"`. The chain spike model lives at `models/tests/codegen_chain_spike/design.sysml`, which does not contain the substring `"models/designs"`. Result: zero design attributes extracted, zero defaults available, empty JSON.

The fix is confirmed working: with `design_path_filter="design.sysml"`, all 3 attributes are extracted with correct defaults (`10.0`, `5.0`, `12.0`), and the full pipeline produces populated JSON.

---

## Diagnostic Script Outputs

### Script 1: Path Filter Verification (`diag_path_filter.py`)

```
Default filter ('models/designs'): 0 attributes
Specific filter ('design.sysml'):  3 attributes
  ChainSpikeDesign__spike_design__length = '10.0' (type: Real)
  ChainSpikeDesign__spike_design__width = '5.0' (type: Real)
  ChainSpikeDesign__spike_design__rate = '12.0' (type: Real)
Broad filter ('models/tests'):     CRASHED (ValueError: Feature reference in OperatorExpression)
No filter (''):                    CRASHED (same error)
```

**Interpretation:** Default filter yields zero results, confirming the hypothesis. The specific filter produces all 3 expected attributes with correct defaults. Broad and empty filters crash due to a secondary bug (see below).

### Script 2: Literal Type Matching (`diag_literal_types.py`)

```
spike_design.length:  LiteralRational, value=10.0
  Adapter.is_instance():    True
  Python isinstance():      True
  syside .isinstance():     True

spike_design.width:   LiteralRational, value=5.0
  Adapter.is_instance():    True
  Python isinstance():      True
  syside .isinstance():     True

spike_design.rate:    LiteralRational, value=12.0
  Adapter.is_instance():    True
  Python isinstance():      True
  syside .isinstance():     True
```

All three mechanisms (adapter, Python isinstance, syside isinstance) agree for all design attributes. All values are `LiteralRational` with native `float` values. **Zero disagreements detected.**

Library output attributes (`AreaCalc.area`, `CostCalc.total_cost`, `SummaryCalc.cost_per_area`) are `OperatorExpression` — correctly not matching any literal type.

### Script 3: Extraction Pipeline Trace (`diag_extraction_trace.py`)

```
Path 1 — Library Extraction (extractor.py):
  AreaCalc:    INPUT length=None, INPUT width=None, OUTPUT area=None
  CostCalc:    INPUT area=None,   INPUT rate=None,  OUTPUT total_cost=None
  SummaryCalc: INPUT area=None,   INPUT cost=None,  OUTPUT cost_per_area=None
  → 0/6 library inputs have defaults (correct — library inputs are untyped)

Path 2 — Design Attribute Extraction (parameter_groups.py):
  Default filter ('models/designs'): 0 attributes
  Specific filter ('design.sysml'):  3 attributes, ALL with non-None defaults

Side-by-Side:
  Attribute                                          Library    Design(def)  Design(fix)
  AreaCalc.length                                    None       -            -
  ChainSpikeDesign__spike_design__length             -          -            10.0
  ChainSpikeDesign__spike_design__width              -          -            5.0
  ChainSpikeDesign__spike_design__rate               -          -            12.0
```

**Interpretation:** Library extraction correctly returns `None` for all inputs (they have no defaults in the SysML model). Design extraction works correctly with the right filter. The two paths produce complementary data — library inputs identify entry points, design attributes provide their defaults.

### Script 4: Classification Trace (`diag_classification.py`)

```
RUN 1 (default filter, broken):
  Design attributes extracted: 0
  Entry points (all USAGE_LITERAL, all default=None):
    ChainSpikeDesign__spike_design__area_calc__length:  None
    ChainSpikeDesign__spike_design__area_calc__width:   None
    ChainSpikeDesign__spike_design__cost_calc__rate:    None

RUN 2 (design.sysml filter, working):
  Design attributes extracted: 3
  Entry points (still USAGE_LITERAL, but defaults populated):
    ChainSpikeDesign__spike_design__area_calc__length:  10.0
    ChainSpikeDesign__spike_design__area_calc__width:   5.0
    ChainSpikeDesign__spike_design__cost_calc__rate:    12.0

QUALIFIED NAME MISMATCH:
  Design attr QNames:  [...__spike_design__length,  ...__spike_design__width,  ...__spike_design__rate]
  Entry point QNames:  [...__spike_design__area_calc__length,  ...__spike_design__area_calc__width,  ...__spike_design__cost_calc__rate]
  Matching: NONE

SAFETY NET:
  deriver._attr_index: 3 entries (design attr qnames)
  deriver.get_default_value(..area_calc__length): 10.0  ← resolves correctly
  deriver.get_default_value(..area_calc__width):  5.0   ← resolves correctly
  deriver.get_default_value(..cost_calc__rate):   12.0  ← resolves correctly
```

**Critical discovery:** Design attribute qualified names and entry point qualified names do NOT match (design attrs omit the calc usage segment). Strategy 1 (`DESIGN_ATTRIBUTE`) in `_classify_entry_points()` **can never match** for this model. But the safety net in `_group_entry_points_via_deriver()` at `graph_builder.py:326-336` correctly resolves defaults through `ParameterGroupDeriver.get_default_value()`, which performs a fuzzy match by simple name.

The entry points remain classified as `USAGE_LITERAL` (not `DESIGN_ATTRIBUTE`), but they get correct default values through the merge path. This is the intended resolution mechanism.

---

## Delta-by-Delta Analysis

### Delta D: Path Filter Mismatch (PRIMARY ROOT CAUSE)

| | Details |
|---|---|
| **Location** | `parameter_groups.py:89` — `design_path_filter: str = "models/designs"` |
| **Called at** | `initialization.py:140` — no override passed |
| **Impact** | All design attributes filtered out → empty `design_attr_by_qname` → empty JSON |
| **Evidence** | Script 1: 0 attributes with default filter, 3 with `"design.sysml"` |
| **Correctness** | The hardcoded default is **wrong** for any model not in `models/designs/`. The caller (`initialization.py`) should pass the correct filter or the default should be more permissive. |

### Delta A: `str()` Wrapping of Default Values

| | Details |
|---|---|
| **Old** | `extractor.py` returned native `float`/`int` from `_extract_default_value()` |
| **New** | `extractor.py:342` — `return str(value)` |
| **Impact** | **Benign.** `graph_builder.py:238` does `float(attr.default_value)` which handles both `float(0.5)` and `float("0.5")`. Script 4 confirms `float()` conversion succeeds. |
| **Correctness** | Both old and new are correct. The `str()` wrapping is slightly wasteful but harmless. |

### Delta B: Adapter `is_instance()` vs Python `isinstance()`

| | Details |
|---|---|
| **Old** | `isinstance(expr, syside.LiteralRational)` — Python isinstance |
| **New** | `self.adapter.is_instance(expr, "LiteralRational")` — adapter indirection |
| **Impact** | **Benign.** Script 2 confirms all three mechanisms agree for all literal types. Zero disagreements. |
| **Correctness** | Both are correct. The adapter adds mock support without breaking real behavior. |

### Delta C: `FeatureValue` Filtering

| | Details |
|---|---|
| **Old** | `isinstance(membership, syside.FeatureValue)` |
| **New** | `hasattr(membership, 'is_default')` |
| **Impact** | **Not exercised** for chain spike model. Library inputs have no defaults, so the membership-scanning fallback path is never reached. |
| **Correctness** | Cannot determine from chain spike model alone. Needs testing with models where library calc def inputs DO have defaults. For now, this is a **deferred concern**. |

---

## Secondary Bug: OperatorExpression Crash

**Location:** `parameter_groups.py:188` → `evaluate_true_static_expression(expr)` → `expression.py:416`

When `extract_design_attributes()` encounters library output attributes (e.g., `out attribute area : Real = length * width`), it tries to evaluate the OperatorExpression. The expression references features (`length`, `width`), which causes `evaluate_true_static_expression()` to raise `ValueError`.

**Impact:** Not directly causing the empty JSON (the path filter prevents these from being reached in production). But if the path filter were broadened (e.g., to support test models), this crash would occur. The function should catch and return `None` for non-static expressions rather than crashing.

**Evidence:** Scripts 1 and 3 — `"models/tests"` and `""` filters both crash with `ValueError: Feature reference 'length' found in static expression`.

---

## Qualified Name Mismatch (Important Observation)

Design attributes and entry points use different qualified name schemes:

| Element | QName Pattern | Example |
|---------|--------------|---------|
| Design attribute | `Package__part__attr_name` | `ChainSpikeDesign__spike_design__length` |
| Entry point | `Package__part__calc_usage__param_name` | `ChainSpikeDesign__spike_design__area_calc__length` |

This means Strategy 1 (`DESIGN_ATTRIBUTE`) in `_classify_entry_points()` at `graph_builder.py:232-240` will **never match** for any model using this binding pattern. The defaults always come through the safety net (`_group_entry_points_via_deriver` at line 326-336).

This is not a bug per se — the safety net is the intended resolution path. But it means:
1. The `entry_type` field on EntryPoint is always `USAGE_LITERAL` instead of `DESIGN_ATTRIBUTE`
2. Strategy 1 code is dead code for this model pattern
3. If the safety net were removed, defaults would be lost even with correct path filter

---

## Validation Coverage Analysis (FR-5)

### Current Coverage

| Level | Check | Relevance to Default Extraction |
|-------|-------|--------------------------------|
| L2 | `_has_default_value()` (line 263-283) | Checks `feature_value_expression` **presence** only |
| L2/ADR-002 | `check_static_expressions()` (adr002.py:418-510) | Validates expression **structure** (no feature refs), NOT extractability |
| L8 | `check_design_attr_completeness()` (line 372-439) | Checks `feature_value_expression is not None`, filters by `"designs" in path.parts` |

### Gaps in Coverage

1. **No extractability check:** No validation verifies that `evaluate_true_static_expression()` succeeds on design attribute expressions. A model can pass all 8 levels but still produce empty JSON.

2. **No literal type check:** No validation checks that `feature_value_expression` is a literal type codegen can handle (LiteralRational, LiteralInteger, etc.).

3. **Path filter consistency:** L8 uses `"designs" in doc_path.parts` (line 400) but codegen uses `"models/designs" in str(source_file)` (parameter_groups.py:110). These are different matching criteria.

4. **No crash guard:** `_extract_default_value()` in parameter_groups.py can crash on OperatorExpressions with feature references. No validation catches this ahead of time.

---

## Summary of All Issues Found

| Issue | Severity | Root Cause | Fix Location |
|-------|----------|-----------|--------------|
| Empty JSON (primary) | **Critical** | Path filter default `"models/designs"` doesn't match test models | `initialization.py:140` or `parameter_groups.py:89` |
| OperatorExpression crash | Medium | `_extract_default_value()` doesn't catch ValueError from `evaluate_true_static_expression()` | `parameter_groups.py:188` |
| QName mismatch (Strategy 1 dead) | Low | Design attr qnames and entry point qnames use different hierarchy depth | `graph_builder.py:210-214` (index building) |
| No extractability validation | Medium | L8 checks presence but not extractability of default values | `level8_codegen.py:418-421` |
| Path filter inconsistency | Low | L8 and codegen use different path matching logic | `level8_codegen.py:400` vs `parameter_groups.py:110` |
