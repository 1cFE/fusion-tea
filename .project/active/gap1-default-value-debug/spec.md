# Spec: Gap 1 — Default Value Extraction Debug & Fix Plan

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-01 21:14 UTC
**Complexity:** MEDIUM
**Branch:** visualization

---

## Business Goals

### Why This Matters

The codegen pipeline generates empty `design_params.json` files (`{}`), which means every generated package requires manual JSON population before `execute_pipeline()` can run. This blocks the codegen chain from being fully automated and will recur for Items 4-5 (solar+battery), where ~15-20 entry-point values would need hand-filling.

The default values exist in the SysML model (`attribute length : Real = 10.0;`) and SHOULD flow through extraction → classification → JSON generation. They don't. This investigation needs to determine exactly where and why they're lost, confirm the correct implementation, and produce a fix plan.

### Success Criteria

- [ ] Every implementation delta between old and new extraction pipelines is documented with file:line references and behavioral analysis
- [ ] A diagnostic Python script has been run against the chain spike model, proving where `default_value` becomes `None`
- [ ] The correct implementation for each delta is identified and justified
- [ ] A fix plan exists with specific file:line changes for `sysml-codegen` and (if relevant) `agentic-mbse`
- [ ] Any SysML model constraints required for codegen to extract defaults are documented (i.e., what the validation checks SHOULD enforce)

### Priority

High — blocks fully automated codegen. Must be resolved before Items 4-5 proceed.

---

## Problem Statement

### Current State

The codegen pipeline (`sysml-codegen`) generates `inputs/design_params.json` as `{}`. The schema file correctly declares the three required fields (no Pydantic defaults), so the EntryPoint module fails at runtime.

The default values (`10.0`, `5.0`, `12.0`) exist in the SysML design model as attribute defaults and are available during extraction. The old monorepo (`fusion_modeling`) had this working — all `fusion_simkit/inputs/*.json` files contain populated values.

### Desired Outcome

A complete understanding of why defaults are lost, which implementation is correct, and a concrete fix plan. This is a debug/investigation deliverable, not an implementation deliverable.

---

## Scope

### In Scope

1. **Three implementation deltas** between old (`fusion_modeling/scripts/sysml_to_teax.py`) and new (`sysml-codegen/src/sysml_codegen/extraction/extractor.py`):
   - Delta A: `str()` wrapping of default values
   - Delta B: Adapter `is_instance()` vs direct Python `isinstance()` for literal type matching
   - Delta C: `FeatureValue` filtering change (`isinstance(m, syside.FeatureValue)` → `hasattr(m, 'is_default')`)

2. **Both default value extraction paths**:
   - Design attribute defaults (e.g., `attribute length : Real = 10.0;` in design part)
   - Library defaults (e.g., `in attribute length : Real;` in calc def — no default here, but the path must be traced)

3. **Full pipeline trace** from SysML model through:
   - `extractor.py:_extract_default_value()` → `_extract_literal_value()`
   - `graph_builder.py:_classify_entry_points()` (all three strategies)
   - `graph_builder.py:_group_entry_points_via_deriver()` (merge safety net)
   - `entry_point.py:generate_all_derived_jsons_from_graph()` (JSON writer)

4. **Diagnostic Python scripts** that load the chain spike SysML model and trace values at each pipeline stage

5. **agentic-mbse syside adapter analysis**: Whether `SysideAdapter.is_instance()` behaves identically to Python `isinstance()` for literal types (`LiteralRational`, `LiteralInteger`, `LiteralBoolean`, `LiteralString`)

6. **agentic-mbse validation checks**: Whether existing SysML checks (levels 1-8) enforce any model patterns that codegen depends on for default extraction, and whether new checks SHOULD be added

### Out of Scope

- Implementing the fixes (separate work item after this spec's plan is approved)
- Gap 2 (RootModel[float] handler) and Gap 3 (static FusionParams) — separate specs
- Changes to `fusion-tea` itself (consumer, not source of bug)
- Changes to the chain spike SysML model (the model is correct)

### Edge Cases & Considerations

- The old repo stored native types in `AttributeInfo.default_value` despite it being typed as `Optional[str]` — a type annotation mismatch that happened to work. The new code "fixed" the annotation by wrapping with `str()`, but this may have broken downstream assumptions.
- `syside`'s `.isinstance()` method (called via `elem.isinstance(type)`) is NOT the same as Python's `isinstance()`. The adapter uses the former; the old code used the latter. These may disagree for literal types.
- The `_group_entry_points_via_deriver()` merge at `graph_builder.py:326-336` is a safety net that can override `None` defaults from `ParameterSource.default_value`. This path needs investigation too — it may be the intended resolution path that's also broken.
- syside version differences between old and new repos could affect literal type resolution.

---

## Requirements

### Functional Requirements

#### Investigation Phase

1. **FR-1**: Write a diagnostic Python script that loads the chain spike SysML model via the `agentic-mbse` adapter and inspects literal expression types. For each attribute with a default value in `design.sysml`, the script MUST report:
   - The Python `type()` of the expression object
   - Whether `isinstance(expr, syside.LiteralRational)` matches (old behavior)
   - Whether `adapter.is_instance(expr, "LiteralRational")` matches (new behavior)
   - Whether `expr.isinstance(syside.LiteralRational)` matches (syside's isinstance)
   - The value of `expr.value` if accessible

2. **FR-2**: Write a diagnostic Python script that runs the `SysMLDataExtractor` on the chain spike model and prints the `default_value` field of every extracted `AttributeInfo`, for both calc def inputs and design attributes. The script MUST show which extraction strategy succeeded or failed for each attribute.

3. **FR-3**: Write a diagnostic Python script that runs `_classify_entry_points()` on the chain spike model's extracted data and prints the classified `EntryPoint.default_value` for each entry point, showing which classification strategy (DESIGN_ATTRIBUTE / LIBRARY_DEFAULT / USAGE_LITERAL) was used and whether the default was found.

4. **FR-4**: Document each of the three deltas (A, B, C) with:
   - Old code (exact lines, with file:line references)
   - New code (exact lines, with file:line references)
   - Behavioral difference (what values each produces for the chain spike model)
   - Correctness assessment (which is correct and why)

5. **FR-5**: Analyze the `agentic-mbse` validation checks (levels 1-8) to determine:
   - Which checks (if any) verify that design attributes have extractable default values
   - Which checks (if any) verify literal expression types that codegen depends on
   - Whether new checks SHOULD be added to catch models where codegen would fail to extract defaults

#### Documentation Phase

6. **FR-6**: Produce a findings document at `.project/active/gap1-default-value-debug/findings.md` containing:
   - Diagnostic script outputs (actual values, not hypothetical)
   - Delta-by-delta analysis with correctness assessments
   - The confirmed root cause (with evidence from diagnostic scripts)

7. **FR-7**: Produce a fix plan at `.project/active/gap1-default-value-debug/fix-plan.md` containing:
   - Specific file:line changes needed in `sysml-codegen`
   - Specific file:line changes needed in `agentic-mbse` (if any)
   - Any new validation checks to add
   - Test strategy for verifying the fix

---

## Acceptance Criteria

### Core Investigation
- [ ] Diagnostic scripts (FR-1, FR-2, FR-3) run successfully against the chain spike model
- [ ] All three deltas (A, B, C) are documented with old/new code, behavioral differences, and correctness assessments
- [ ] Root cause is confirmed with evidence from diagnostic output (not hypothesized)
- [ ] Both extraction paths (design attribute defaults, library defaults) are traced and documented

### Adapter Analysis
- [ ] `SysideAdapter.is_instance()` is tested against all four literal types with actual chain spike model elements
- [ ] Any behavioral difference between Python `isinstance()` and syside `.isinstance()` is documented

### Validation Check Analysis
- [ ] All 8 validation levels in `agentic-mbse` are reviewed for relevance to default value extraction
- [ ] Gaps in validation coverage are identified (checks that SHOULD exist but don't)

### Fix Plan
- [ ] Fix plan specifies exact files, line numbers, and the nature of each change
- [ ] Fix plan covers both `sysml-codegen` and `agentic-mbse` (if relevant)
- [ ] Fix plan includes test strategy

---

## Related Artifacts

- **Research:** `.project/research/20260201-210000_codegen-runtime-gaps-root-cause.md`
- **Gap Report:** `.project/reports/codegen-runtime-gaps-2026-02-01-2047.md`
- **Old Repo Research:** `~/fusion_modeling/project/research/20251208-172130_json-default-value-extraction-bug.md`
- **Old Repo Research:** `~/fusion_modeling/project/research/20251219-224500_null-value-root-cause-analysis.md`
- **Chain Spike SysML:** `models/tests/codegen_chain_spike/design.sysml`, `library.sysml`
- **Migration Epic:** `~/fusion_modeling/project/backlog/repo-migration-epic-v3.md`

### Key Source Files

| Repo | File | Relevance |
|------|------|-----------|
| sysml-codegen | `src/sysml_codegen/extraction/extractor.py:336-373` | `_extract_default_value()`, `_extract_literal_value()` — where deltas A, B, C live |
| sysml-codegen | `src/sysml_codegen/resolution/graph_builder.py:179-281` | `_classify_entry_points()` — where defaults are consumed |
| sysml-codegen | `src/sysml_codegen/resolution/graph_builder.py:284-338` | `_group_entry_points_via_deriver()` — merge safety net |
| sysml-codegen | `src/sysml_codegen/generation/entry_point.py:595-631` | JSON writer — downstream consumer |
| sysml-codegen | `src/sysml_codegen/extraction/data_models.py` | `AttributeInfo`, `DesignAttributeData` field typing |
| agentic-mbse | `src/agentic_mbse/sysml/syside_adapter.py:151-154` | TYPE_MAP for literal types |
| agentic-mbse | `src/agentic_mbse/sysml/syside_adapter.py:230-257` | `is_instance()` implementation |
| agentic-mbse | `src/agentic_mbse/sysml/data_models.py` | Base `AttributeInfo` with `default_value: Any` |
| agentic-mbse | `src/agentic_mbse/validation/` | Levels 1-8 validation checks |
| fusion_modeling | `scripts/sysml_to_teax.py:484-561` | Old extraction (reference implementation) |

---

**Next Steps:** After approval, proceed to `/_my_design` (lightweight — this is primarily a debug task, not a feature build)
