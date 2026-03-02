# Design: Gap 1 — Default Value Extraction Debug & Fix Plan

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-01 21:18 UTC
**Branch:** visualization
**Commit:** 3f2cd66

---

## Overview

Debug investigation to determine why the codegen pipeline produces empty `design_params.json` for the chain spike model, and produce a concrete fix plan. This is a diagnostic/investigation deliverable, not an implementation task.

## Related Artifacts

- **Spec:** `.project/active/gap1-default-value-debug/spec.md`
- **Research:** `.project/research/20260201-210000_codegen-runtime-gaps-root-cause.md`
- **Gap Report:** `.project/reports/codegen-runtime-gaps-2026-02-01-2047.md`
- **Chain Spike Model:** `models/tests/codegen_chain_spike/design.sysml`, `library.sysml`

---

## Research Findings

### Critical Discovery: Path Filter Mismatch (Delta D — Not in Original Spec)

Beyond the three deltas identified in the spec (A, B, C), codebase analysis reveals a **fourth issue** that is likely the primary root cause for the chain spike model specifically.

`extract_design_attributes()` at `sysml-codegen/src/sysml_codegen/analysis/parameter_groups.py:87-127` accepts a `design_path_filter` parameter that defaults to `"models/designs"`:

```python
def extract_design_attributes(
    model: Any,
    design_path_filter: str = "models/designs",  # <-- line 89
) -> dict[Path, list[DesignAttributeData]]:
```

The chain spike model lives at `models/tests/codegen_chain_spike/design.sysml`. The path `models/tests/codegen_chain_spike/design.sysml` does **not** contain the substring `"models/designs"`.

At `initialization.py:140`, the function is called with **no override**:

```python
design_attrs = extract_design_attributes(extractor.model)
```

This means **all design attributes from the chain spike model are filtered out before they reach `_classify_entry_points()`**. The `design_attr_by_qname` dict at `graph_builder.py:210-214` would be empty, so Strategy 1 (DESIGN_ATTRIBUTE) never matches. This alone explains the empty JSON.

### Two Separate Default Value Extraction Implementations

The codebase has **two independent** `_extract_default_value()` functions:

| Location | Used For | Approach |
|----------|----------|----------|
| `extractor.py:336-357` | Calc def input attributes (library) | Simple: checks `feature_value_expression`, then `owned_memberships` with `hasattr(m, 'is_default')` duck typing |
| `parameter_groups.py:158-197` | Design attributes | Comprehensive: handles literals, references, chains, operator expressions, `__str__` fallback |

For Gap 1 (design attribute defaults), the relevant path is through `parameter_groups.py`, **not** `extractor.py`. The spec's three deltas (A, B, C) live in `extractor.py` and primarily affect **library defaults** (Strategy 2 in classification), not design attribute defaults (Strategy 1).

### Design Attribute Data Flow (Strategy 1 — DESIGN_ATTRIBUTE)

```
SysML model (design.sysml)
  → parameter_groups.py:extract_design_attributes()     [PATH FILTER HERE]
    → parameter_groups.py:_extract_single_attribute()    [line 130-152]
      → parameter_groups.py:_extract_default_value()     [line 158-197]
        → SysideAdapter.is_instance()                    [literal type check]
  → graph_builder.py:_classify_entry_points()            [line 232-240]
    → float(attr.default_value)                          [string → float]
  → graph_builder.py:_group_entry_points_via_deriver()   [line 326-336, safety net]
  → entry_point.py:generate_all_derived_jsons_from_graph() [line 616]
    → JSON output (only non-None defaults)
```

### Library Default Data Flow (Strategy 2 — LIBRARY_DEFAULT)

```
SysML model (library.sysml)
  → extractor.py:extract_calculation_definitions()
    → extractor.py:_extract_default_value()              [DELTAS A, B, C here]
      → extractor.py:_extract_literal_value()            [adapter.is_instance()]
  → graph_builder.py:_classify_entry_points()            [line 242-254]
    → _get_library_default(calc_def, param_name)         [line 361-385]
      → float(attr.default_value)                        [string → float]
```

For the chain spike model, the library calc defs have **no defaults** on their inputs (`in attribute length : Real;` — no `= value`). So Strategy 2 correctly produces `None` — these are entry points, and their defaults come from the design file.

### Spec Delta Analysis (Deltas A, B, C in extractor.py)

These deltas are in the **library extraction path** (`extractor.py`), not the design attribute path (`parameter_groups.py`). For the chain spike model where library inputs have no defaults, these deltas are **irrelevant to the immediate bug**. However, they still need investigation for models where library defaults exist.

**Delta A: `str()` wrapping** (`extractor.py:342`)
- Old: `return value` (native float/int)
- New: `return str(value)`
- Impact on chain spike: None — library inputs have no defaults
- Impact generally: Benign — `graph_builder.py:238` does `float(attr.default_value)` which handles both

**Delta B: Adapter `is_instance()` vs Python `isinstance()`** (`extractor.py:364`)
- Old: `isinstance(expr, syside.LiteralRational)`
- New: `self.adapter.is_instance(expr, "LiteralRational")`
- Impact: The adapter at `syside_adapter.py:230-257` uses `elem.isinstance(sysml_type)` (syside's method). This should be equivalent for literal types, but needs empirical verification via diagnostic scripts (FR-1).

**Delta C: `FeatureValue` filtering** (`extractor.py:347-348`)
- Old: `isinstance(membership, syside.FeatureValue)` (Python isinstance)
- New: `hasattr(membership, 'is_default')` (duck typing)
- Impact: Could match different sets of memberships. The old code required `FeatureValue` type AND checked `is_default`. The new code only checks `is_default` presence — potentially broader match, but also skips the type guard.

### Safety Net Analysis (`_group_entry_points_via_deriver`)

The merge at `graph_builder.py:326-336` can override `None` defaults from classification:

```python
if ep.default_value is None and ps.default_value is not None:
    ep = EntryPoint(..., default_value=ps.default_value, ...)
```

This depends on `ParameterGroupDeriver.get_default_value()` at `parameter_groups.py:526-546`. The deriver's `_attr_index` is built from the same `design_attrs` dict that's already empty due to the path filter. So the safety net **also fails** because it depends on the same filtered data.

### Adapter `is_instance()` Analysis

At `syside_adapter.py:230-257`:

```python
@classmethod
def is_instance(cls, elem: Any, type_name: str) -> bool:
    sysml_type = type_map.get(type_name)
    if sysml_type is not None:
        if hasattr(elem, "isinstance"):
            return elem.isinstance(sysml_type)
    return type_name in type(elem).__name__
```

Three mechanisms in play:
1. **Python `isinstance(expr, syside.LiteralRational)`** — old code, checks Python class hierarchy
2. **`expr.isinstance(syside.LiteralRational)`** — syside AST method, checks SysML type hierarchy
3. **`"LiteralRational" in type(expr).__name__`** — string fallback for mocks

For literal types, (1) and (2) should agree — literal nodes are concrete types, not abstract KerML metaclasses. But this needs empirical confirmation (FR-1).

### Validation Level Analysis (FR-5)

| Level | Relevance to Default Extraction | Details |
|-------|---------------------------------|---------|
| L1 (Syntax) | None | Parser-only |
| L2 (Structure) | Indirect | `_has_default_value()` checks `feature_value_expression` exists, but doesn't extract or validate the value |
| L3 (Dataflow) | None | Import cycles only |
| L4 (Constraints) | None | Constraint counting |
| L5 (Semantic) | None | Unit consistency (placeholder) |
| L6 (Traceability) | None | Doc coverage |
| L7 (Architecture) | None | Manifest compliance |
| L8 (Codegen) | Partial | Checks design attrs have `feature_value_expression` (line 417-421), but does NOT validate the value is extractable as numeric |

**Gaps in validation coverage:**
- No check that `feature_value_expression` resolves to a literal type codegen can extract
- No check that design attribute defaults produce non-None values through `_extract_default_value()`
- No check that `design_path_filter` matches the actual design file locations
- ADR-002's `check_static_expressions()` validates expression structure but doesn't test extractability

---

## Proposed Design

### Investigation Architecture

The investigation requires **four diagnostic scripts** (FR-1 through FR-3 from spec, plus a new one for the path filter discovery) and **two analysis documents** (findings + fix plan).

### Component 1: Diagnostic Script — Path Filter Verification (New)

**Purpose:** Confirm the path filter hypothesis is the primary root cause for the chain spike model.

**Location:** `.project/active/gap1-default-value-debug/scripts/diag_path_filter.py`

**What it does:**
1. Load the chain spike model via syside
2. Call `extract_design_attributes(model)` with default filter → expect empty result
3. Call `extract_design_attributes(model, design_path_filter="models/tests")` → expect 3 attributes
4. Call `extract_design_attributes(model, design_path_filter="")` → expect all attributes
5. Print results for each call

**Dependencies:** `sysml-codegen` (installed), `agentic-mbse` (installed), chain spike SysML model

### Component 2: Diagnostic Script — Literal Type Matching (FR-1)

**Purpose:** Empirically test whether `SysideAdapter.is_instance()` matches literal expression types identically to Python `isinstance()`.

**Location:** `.project/active/gap1-default-value-debug/scripts/diag_literal_types.py`

**What it does:**
1. Load chain spike model via syside adapter
2. For each design attribute with `feature_value_expression`:
   - Report `type(expr)` (Python class)
   - Test `isinstance(expr, syside.LiteralRational)` (old behavior)
   - Test `SysideAdapter.is_instance(expr, "LiteralRational")` (new behavior)
   - Test `expr.isinstance(syside.LiteralRational)` (syside's method)
   - Report `expr.value` if accessible
3. Repeat for LiteralInteger, LiteralBoolean, LiteralString

### Component 3: Diagnostic Script — Extraction Pipeline Trace (FR-2)

**Purpose:** Trace `default_value` through each stage of extraction for the chain spike model.

**Location:** `.project/active/gap1-default-value-debug/scripts/diag_extraction_trace.py`

**What it does:**
1. Load chain spike model
2. Run `SysMLDataExtractor.extract_calculation_definitions()` — print `default_value` for each calc def input attribute (expect all `None` since library inputs have no defaults)
3. Run `extract_design_attributes()` with **both** default and corrected path filters — print `default_value` for each `DesignAttributeData`
4. Show side-by-side: which extraction path succeeded for each attribute

### Component 4: Diagnostic Script — Classification Trace (FR-3)

**Purpose:** Trace `default_value` through `_classify_entry_points()` to confirm which strategy fires and whether the default survives.

**Location:** `.project/active/gap1-default-value-debug/scripts/diag_classification.py`

**What it does:**
1. Run `build_pipeline_context()` against chain spike model (uses default path filter → empty design attrs)
2. Print each `EntryPoint`: qualified name, strategy used, default_value
3. Then run with patched path filter and repeat
4. Show the difference

### Component 5: Findings Document (FR-6)

**Location:** `.project/active/gap1-default-value-debug/findings.md`

**Contents:**
- Diagnostic script outputs (actual values from runs)
- Delta-by-delta analysis (A, B, C, D) with correctness assessments
- Confirmed root cause with evidence
- Both extraction paths traced

### Component 6: Fix Plan (FR-7)

**Location:** `.project/active/gap1-default-value-debug/fix-plan.md`

**Contents:**
- Specific file:line changes needed
- Covers both `sysml-codegen` and `agentic-mbse`
- New validation checks to add
- Test strategy

### Execution Order

1. Write and run diagnostic scripts (Components 1-4) — run sequentially since each informs the next
2. Analyze outputs and write findings (Component 5)
3. Write fix plan based on confirmed root cause (Component 6)

---

## Potential Risks

1. **Path filter may not be the only issue.** Even with corrected path filter, `_extract_default_value()` in `parameter_groups.py` might fail for other reasons (e.g., syside literal type mismatch). The diagnostic scripts test both hypotheses.

2. **syside version differences.** The old repo may have used a different syside version where `isinstance()` and `.isinstance()` behaved differently. The FR-1 diagnostic tests this empirically on the current version.

3. **Scope expansion.** If multiple root causes compound (path filter + literal type mismatch + FeatureValue filtering), the fix plan gets more complex. The design handles this by testing each independently.

---

## Integration Strategy

- Diagnostic scripts are standalone Python scripts in the `.project/active/` directory — no integration with the production codebase
- Findings and fix plan are documentation deliverables that feed into a subsequent implementation task
- The fix plan will target `sysml-codegen` (primary) and `agentic-mbse` (if validation gaps found)

---

## Validation Approach

- Each diagnostic script produces concrete output that either confirms or refutes a hypothesis
- The findings document must contain **actual values** from script runs, not hypothesized values
- The fix plan must reference specific file:line locations verified during investigation
- Success: root cause confirmed with evidence, fix plan specifies exact changes

---

Next Step: After approval → implement diagnostic scripts and run them (essentially `/_my_implement`)
