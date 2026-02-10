# Spec: E2E Attribute Expression Validation V2 (Post-Fix Verification)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-10 06:42:11 UTC
**Complexity:** MEDIUM
**Branch:** e2e-attr-expr

---

## Business Goals

### Why This Matters

The original E2E validation (v1) confirmed that Phase 1+2 sysml-codegen features (CalcDef auto-implementation, FORMULA computed attributes, EXPOSE_PURE aliases) produce correct numerical results, but required 7 manual workarounds across codegen bugs in backtracker wiring, module generation, exit point serialization, smart-regen, name sanitization, and package structure.

All 7 bugs have since been fixed:
- **sysml-codegen** (Bugs 1-3, 5-7): commit `93f0a55` — FORMULA entry points, backtracker wiring, Float/float types, smart-regen stub upgrade, special character sanitization, intermediate `__init__.py`
- **TEAx** (Bug 4): commit `5d6496a` — ExitPoint bare primitive type support (float/int/str/bool)

These fixes were validated within each codebase's own test suites (313 tests in sysml-codegen, 197 in TEAx), but have NOT been validated end-to-end through the real fusion-tea pipeline. This validation provides the final gate confirmation before Phase 3 (COST-PATTERN epic) investment.

### Success Criteria

- [ ] e2e_attr_expr model: codegen produces correct, executable pipeline with **zero manual workarounds** — all 16 ground truth values pass
- [ ] solar_battery model: codegen produces correct output with **zero manual workarounds** for codegen-generated modules — all 7 verification metrics pass (ComponentCostEvaluator hybrid merge documented but not counted as a workaround)
- [ ] Per-bug verification: each of the 7 original bugs has a specific PASS/FAIL against its fix criteria
- [ ] Zero regressions across sysml-codegen, agentic-mbse, and fusion-tea test suites
- [ ] Side-by-side comparison report: v1 (manual workarounds) vs v2 (expected: zero workarounds)

### Priority

P0 — gates Phase 3 (COST-PATTERN epic). MUST be completed before COST-PATTERN backlog begins.

---

## Problem Statement

### Current State

- V1 validation artifacts exist at `generated/e2e_attr_expr/` and `generated/solar_battery/` with manual workarounds baked in (modified pipeline.yaml, patched module wrappers, manual run_pipeline.py writes)
- All 7 bugs have been fixed in their respective codebases (sysml-codegen, TEAx) with passing internal test suites
- No end-to-end validation has been performed through the real fusion-tea pipeline with the fixed codegen and TEAx
- The fixes need independent confirmation before Phase 3 investment

### Desired Outcome

- Fresh codegen output for both models in separate directories (`generated/e2e_attr_expr_v2/`, `generated/solar_battery_v2/`) enabling side-by-side comparison with v1
- Confirmed zero manual workarounds needed for pure codegen output
- A report documenting per-bug fix verification, numerical results, and v1-vs-v2 comparison

---

## Scope

### In Scope

- **Phase A**: Regression baseline — run test suites across all 3 codebases
- **Phase B**: Fresh e2e_attr_expr codegen to `generated/e2e_attr_expr_v2/` — codegen, TEAx execution, numerical verification against all 16 ground truth values
- **Phase C**: Fresh solar_battery codegen to `generated/solar_battery_v2/` — codegen, hybrid pipeline merge (ComponentCostEvaluator), TEAx execution, numerical verification against all 7 metrics
- **Phase D**: Per-bug fix verification — specific PASS/FAIL for each of the 7 original bugs
- **Phase E**: Report — side-by-side v1 vs v2 comparison, per-bug matrix, overall gate decision

### Out of Scope

- Modifying existing v1 artifacts (`generated/e2e_attr_expr/`, `generated/solar_battery/`)
- Changes to sysml-codegen, TEAx, or agentic-mbse source code (validation only; new bugs found are documented, not fixed)
- New SysML model creation (reuses existing `models/tests/e2e_attr_expr/` and `models/tests/solar_battery/`)
- Phase 3 implementation (COST-PATTERN epic)
- Updating fusion-tea's BACKLOG.md or project management artifacts

### Edge Cases & Considerations

- **ComponentCostEvaluator hybrid merge**: solar_battery requires merging the ComponentCostEvaluator into the generated pipeline. This is expected and architectural (not a bug workaround). It MUST be documented in the report but SHOULD NOT count as a "manual workaround" for bug verification purposes.
- **Smart-regen vs fresh codegen**: V2 runs fresh codegen (no `--smart-regen`) to isolate fix verification. The `--smart-regen` stub upgrade fix (Bug 5) SHOULD be verified separately with a targeted test.
- **Ground truth values**: V2 uses the same ground truth values from the v1 research document. These are mathematical constants — they MUST NOT change.
- **Floating-point tolerances**: Same as v1 — exact match for integer/simple arithmetic, relative tolerance 1e-6 for exponentiation (CRF, annualized_cost), relative tolerance 1e-4 for LCOE.
- **Output directory isolation**: V2 output goes to `_v2` directories to enable side-by-side comparison. The `run_pipeline.py` output paths MUST be adjusted to write within the v2 directory.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

#### Phase A: Regression Baseline

1. **FR-A1**: sysml-codegen test suite MUST pass with 0 failures (baseline: 313 tests post-fix).
2. **FR-A2**: agentic-mbse test suite MUST pass with 0 failures (baseline: 886 tests).
3. **FR-A3**: fusion-tea test suite MUST pass with 0 failures (baseline: 48 tests).

#### Phase B: Fresh E2E Attr Expr Codegen + TEAx

4. **FR-B1**: Run sysml-codegen on `models/tests/e2e_attr_expr/`, outputting to `generated/e2e_attr_expr_v2/`.
5. **FR-B2**: Generated `design_params.py` MUST contain all 7 FORMULA input parameters without manual addition (Bug 1 fix verification).
6. **FR-B3**: Generated `pipeline.yaml` MUST wire CalcUsage inputs referencing FORMULA/EXPOSE attributes to upstream MODULE_OUTPUT, not ENTRY_POINT (Bug 2 fix verification).
7. **FR-B4**: All FORMULA module wrapper Input classes MUST use `float` type, not `Float`/`RootModel[float]` (Bug 3 fix verification).
8. **FR-B5**: All generated `_impl.py` files MUST have `AUTO_IMPLEMENTED = True`.
9. **FR-B6**: FORMULA synthetic modules MUST appear in pipeline YAML for all 6 FORMULA attributes.
10. **FR-B7**: Execute TEAx pipeline via `uv run python generated/e2e_attr_expr_v2/run_pipeline.py` with **zero manual modifications** to any generated file.
11. **FR-B8**: Pipeline MUST execute without errors, including multi-output channel serialization to JSON (Bug 4 fix verification).
12. **FR-B9**: All 16 numerical outputs MUST match v1 ground truth values within specified tolerances.
13. **FR-B10**: All 12 patterns from v1 MUST be exercised and validated.

#### Phase C: Fresh Solar Battery Codegen + TEAx

14. **FR-C1**: Run sysml-codegen on `models/tests/solar_battery/`, outputting to `generated/solar_battery_v2/`.
15. **FR-C2**: [INFERRED] Generated code MUST have valid Python identifiers for all parts, including `Racking_&_Mounting` (Bug 6 fix verification).
16. **FR-C3**: [INFERRED] All intermediate directories MUST contain `__init__.py` files (Bug 7 fix verification).
17. **FR-C4**: Merge ComponentCostEvaluator into generated pipeline (document all changes in report). Start with pure codegen output; merge MUST be documented with full before/after diffs.
18. **FR-C5**: Execute solar_battery TEAx pipeline with **zero manual workarounds** beyond the documented ComponentCostEvaluator merge.
19. **FR-C6**: All 7 verification metrics MUST match v1 values (total_capex, annual_energy_mwh, annual_om_cost, annual_fuel_cost, capital_recovery_factor, annualized_capital_cost, lcoe_per_mwh).

#### Phase D: Per-Bug Fix Verification

20. **FR-D1**: Each of the 7 original bugs MUST receive a specific PASS/FAIL determination with evidence.
21. **FR-D2**: For any bug that FAILs, the failure MUST be documented with root cause and whether it represents a regression or incomplete fix.

#### Phase E: Report

22. **FR-E1**: Report MUST include side-by-side comparison: v1 manual workarounds vs v2 results.
23. **FR-E2**: Report MUST include per-bug fix verification matrix (Bug #, Description, v1 Status, v2 Status, Evidence).
24. **FR-E3**: Report MUST include gate decision: PASS (proceed to Phase 3) or FAIL (with blocking issues).
25. **FR-E4**: [INFERRED] Report MUST document all ComponentCostEvaluator merge steps with before/after diffs.

### Non-Functional Requirements

26. **NFR-1**: V2 output directories (`generated/e2e_attr_expr_v2/`, `generated/solar_battery_v2/`) MUST coexist with v1 directories for side-by-side comparison.
27. **NFR-2**: [INFERRED] Report written to `.project/active/e2e-attr-expr-validation-v2/report.md`.

---

## Acceptance Criteria

### Core Functionality

- [ ] **Phase A**: All 3 codebase test suites pass with 0 failures (FR-A1 through FR-A3)
- [ ] **Phase B**: e2e_attr_expr freshly generated, pipeline executes with zero manual workarounds, all 16 ground truth values pass (FR-B1 through FR-B10)
- [ ] **Phase C**: solar_battery freshly generated, pipeline executes with only the documented ComponentCostEvaluator merge, all 7 metrics match (FR-C1 through FR-C6)
- [ ] **Phase D**: All 7 bugs have specific PASS/FAIL with evidence (FR-D1, FR-D2)
- [ ] **Phase E**: Report with v1-vs-v2 comparison, per-bug matrix, and gate decision (FR-E1 through FR-E4)

### Quality & Integration

- [ ] Existing tests continue to pass across all codebases
- [ ] No changes made to sysml-codegen, TEAx, or agentic-mbse source code
- [ ] V1 artifacts untouched — side-by-side comparison possible
- [ ] Any new bugs discovered are documented (not fixed) in the report

---

## Related Artifacts

- **V1 Spec:** `.project/active/e2e-attr-expr-validation/spec.md`
- **V1 Report:** `.project/active/e2e-attr-expr-validation/report.md`
- **V1 Research:** `.project/research/20260210-attr-expr-e2e-validation-plan.md`
- **Bug Fix Spec (codegen):** `/home/reid/1cfe/sysml-codegen/.project/active/codegen-bug-fixes/spec.md`
- **Bug Fix Spec (TEAx):** `/home/reid/1cfe/teax/.project/active/exitpoint-primitive-types/spec.md`
- **Design:** `.project/active/e2e-attr-expr-validation-v2/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
