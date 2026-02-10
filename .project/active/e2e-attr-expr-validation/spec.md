# Spec: E2E Attribute Expression Validation (Phases A-D)

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-10 03:08:01 UTC
**Complexity:** MEDIUM
**Branch:** e2e-attr-expr

---

## Business Goals

### Why This Matters

Phases 1 and 2 of the expression-aware codegen effort (epics EXPR-CODEGEN and ATTR-EXPR) represent ~15-19 days of sysml-codegen development. These phases introduced CalcDef auto-implementation (15/15 solar_battery, 19/21 CATF) and FORMULA computed attribute synthetic modules. Both epics are complete with passing internal test suites (285 tests in sysml-codegen, 886 in agentic-mbse), but have not been validated end-to-end from a real modeling project through codegen and TEAx execution.

This validation provides confidence that Phase 1+2 features work correctly in the full pipeline (SysML model -> sysml-codegen -> generated Python -> TEAx execution -> numerical output) before investing in Phase 3 (nested hierarchies, ~10-15 days).

### Success Criteria

- [x] Solar_battery regenerated with all 15 CalcDef `_impl.py` auto-implemented + 1 FORMULA synthetic module (`p_net_kw`) — DEVIATION: `--smart-regen` preserved 10 stubs; 5 system-level + p_net_kw are auto-implemented
- [x] New e2e_attr_expr model exercises all 12 validatable patterns with correct numerical outputs against ground truth
- [x] Zero regressions across sysml-codegen, agentic-mbse, and fusion-tea test suites
- [x] Solar_battery TEAx pipeline produces correct LCOE output, matching or improving on prior hybrid pipeline results

### Priority

P0 — gates Phase 3 work and demonstrates Phase 1+2 value in a real project.

---

## Problem Statement

### Current State

- Phase 1+2 features are validated only within sysml-codegen's internal test fixtures (chain_spike, attr_expr_probe, solar_battery fixture, CATF fixture)
- fusion-tea's `generated/solar_battery/` was generated before Phase 1+2 — all 15 `_impl.py` files contain `raise NotImplementedError`, no FORMULA synthetic module exists
- No fusion-tea model exercises the full set of new patterns (FORMULA chains, FORMULA->CalcUsage wiring, CalcDef exponentiation, EXPOSE_PURE aliases)
- No end-to-end TEAx execution has been performed with Phase 1+2 codegen output

### Desired Outcome

- fusion-tea's solar_battery is regenerated and working with Phase 1+2 features
- A purpose-built test model validates all 12 new patterns with numerical ground truth
- Regression confidence established across all three codebases
- TEAx pipeline execution confirmed working end-to-end

---

## Scope

### In Scope

- **Phase A**: Regenerate solar_battery with latest sysml-codegen; verify auto-implementation and FORMULA module generation
- **Phase B**: Create new `models/tests/e2e_attr_expr/` model exercising 12 patterns; codegen; TEAx execution; numerical verification
- **Phase C**: Run regression test suites across sysml-codegen, agentic-mbse, and fusion-tea
- **Phase D**: Execute solar_battery TEAx pipeline end-to-end; verify LCOE output against prior run. Manual adjustments to `pipeline.yaml` are in scope but MUST be fully documented (what changed, why, and the before/after diff)

### Out of Scope

- Phase 3 implementation (CalcUsage-in-PartDef, `:>>` chains, `sum()`, multiplicity, assembly aggregation)
- Changes to sysml-codegen or agentic-mbse source code (this is pure validation; bugs found are filed, not fixed here)
- Removing the hybrid ComponentCostEvaluator from solar_battery (that requires Phase 3)
- Updating fusion-tea's BACKLOG.md or project management artifacts (separate task)

### Edge Cases & Considerations

- The hybrid `pipeline.yaml` was hand-crafted and may need manual updating after regeneration to wire the new `p_net_kw` synthetic module. Any such adjustments MUST be documented with full before/after diffs and rationale.
- `--smart-regen --preserve-handwritten` flags should preserve the ComponentCostEvaluator and other hand-crafted files. If they don't, this is a sysml-codegen bug to file, not fix in this spec.
- The e2e_attr_expr model intentionally avoids all Phase 3 gaps (no nesting, no PartDef CalcUsages, no `sum()`, no multiplicity, no cross-part refs).
- CRF calculation involves floating-point exponentiation — ground truth comparison should use relative tolerance (~1e-6), not exact match.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

#### Phase A: Regenerate Solar Battery

1. **FR-A1**: Run sysml-codegen on `models/tests/solar_battery/` with `--smart-regen --preserve-handwritten` flags, outputting to `generated/solar_battery/`.
2. **FR-A2**: All 15 CalcDef `_impl.py` files MUST have `AUTO_IMPLEMENTED = True` sentinel.
3. **FR-A3**: A synthetic module `solar_battery_plant__p_net_kw` MUST appear in pipeline YAML, marked with `# source: computed_attribute`.
4. **FR-A4**: The `annualized_om` module's `p_net_kw` input MUST be wired to the synthetic module's output (MODULE_OUTPUT), NOT to an entry point or ComponentCostEvaluator output.
5. **FR-A5**: `IMPLEMENTATION_BACKLOG.md` MUST show 0 functions to implement for CalcDef modules and the computed attribute module.
6. **FR-A6**: [INFERRED] Pipeline YAML SHOULD have 6+ modules (5 system-level CalcUsage + 1 FORMULA synthetic) plus ComponentCostEvaluator for component costs.

#### Phase B: New E2E Test Model

7. **FR-B1**: Create SysML model files at `models/tests/e2e_attr_expr/` (library.sysml, design.sysml) per the model design in the research document (Section "Phase B").
8. **FR-B2**: Model MUST parse cleanly with `uv run syside check`.
9. **FR-B3**: Model MUST pass `uv run agentic-mbse validate --complete` with no V2 violations on FORMULA attributes and L8 pass.
10. **FR-B4**: Run sysml-codegen on the model, outputting to `generated/e2e_attr_expr/`.
11. **FR-B5**: All generated `_impl.py` files MUST have `AUTO_IMPLEMENTED = True`.
12. **FR-B6**: FORMULA synthetic modules MUST appear in pipeline YAML for all FORMULA attributes (expect ~6 synthetic modules).
13. **FR-B7**: Execute TEAx pipeline via `uv run python generated/e2e_attr_expr/run_pipeline.py`.
14. **FR-B8**: Numerical outputs MUST match ground truth values from the research document's ground truth table (Section "Phase B: Ground Truth Values") within specified tolerances:
    - Integer/simple arithmetic results: exact match
    - Exponentiation results (CRF, annualized_cost): relative tolerance 1e-6
    - LCOE: relative tolerance 1e-4

15. **FR-B9**: The 12 patterns from the research document (Section "Phase B: Patterns Exercised") MUST all be exercised and validated:
    1. Simple FORMULA (`power_mw = quantity * unit_cost / 1000000.0`)
    2. Chain FORMULA (`power_kw = power_mw * 1000.0`)
    3. 2-hop chain FORMULA (`annual_om = om_rate * power_kw`)
    4. Simple FORMULA binary (`area = length * width`)
    5. 3-term FORMULA (`volume = length * width * height`)
    6. Fan-in FORMULA (`surface_cost = area * cost_per_sqm`)
    7. CalcDef auto-impl with 5 outputs (ComponentCostCalc)
    8. CalcDef with `**` exponentiation (AnnualizedCostCalc CRF)
    9. EXPOSE_PURE (`total_capex = component_cost.total_cost`)
    10. FORMULA->CalcUsage wiring (`energy { in power_mw = power_mw }`)
    11. FORMULA->CalcUsage 2-hop (`lcoe { in annual_om = annual_om }`)
    12. CalcUsage->CalcUsage via EXPOSE (`financial { in total_capex = total_capex }`)

#### Phase C: Regression Testing

16. **FR-C1**: sysml-codegen test suite MUST pass with 0 failures (baseline: 285 tests).
17. **FR-C2**: agentic-mbse test suite MUST pass with 0 failures (baseline: 886 tests).
18. **FR-C3**: fusion-tea test suite MUST pass with 0 failures.
19. **FR-C4**: `uv run agentic-mbse validate models/ --complete` on fusion-tea models MUST pass.

#### Phase D: Solar Battery TEAx Pipeline Execution

20. **FR-D1**: Execute the solar_battery TEAx pipeline using the Phase A regenerated code.
21. **FR-D2**: If `pipeline.yaml` requires manual adjustment to accommodate the new synthetic module, the adjustment MUST be fully documented: what changed, why it was necessary, and a before/after diff.
22. **FR-D3**: Pipeline MUST execute without errors.
23. **FR-D4**: LCOE output MUST match prior hybrid pipeline output (from `generated/solar_battery/outputs/`). If values differ, the difference MUST be explained (e.g., rounding from auto-impl vs. hand-written code).
24. **FR-D5**: [INFERRED] All intermediate outputs (total_capex, annual_energy, annual_om, etc.) SHOULD be spot-checked against prior run values.

### Non-Functional Requirements

25. **NFR-1**: All manual pipeline.yaml adjustments in Phase D MUST include full documentation (before/after diff, rationale, and whether the adjustment is temporary or permanent).
26. **NFR-2**: [INFERRED] Phase B test model SHOULD become a permanent regression test in fusion-tea.
27. **NFR-3**: [INFERRED] Validation results SHOULD be recorded in a report document at `.project/active/e2e-attr-expr-validation/report.md`.

---

## Acceptance Criteria

### Core Functionality

- [x] **Phase A**: Solar_battery regenerated; 15 auto-impl'd CalcDefs + 1 FORMULA module; wiring correct (FR-A1 through FR-A6) — see FR-A2 deviation in report
- [x] **Phase B**: e2e_attr_expr model created, parsed, validated, codegen'd, executed; all 12 patterns pass; numerical outputs match ground truth (FR-B1 through FR-B9)
- [x] **Phase C**: All 3 codebase test suites pass with 0 failures; fusion-tea model validation passes (FR-C1 through FR-C4) — FR-C4 L8 pre-existing issues noted
- [x] **Phase D**: Solar_battery TEAx pipeline executes; LCOE matches prior output; any pipeline.yaml adjustments fully documented (FR-D1 through FR-D5)

### Quality & Integration

- [x] Existing tests continue to pass across all codebases
- [x] No changes made to sysml-codegen or agentic-mbse source code
- [x] Any bugs discovered are documented (not fixed) as part of the validation report — 7 bugs found
- [x] All manual adjustments have documented rationale

---

## Related Artifacts

- **Research:** `.project/research/20260210-attr-expr-e2e-validation-plan.md` (detailed validation plan, model designs, ground truth values, gap analysis)
- **sysml-codegen Epics:**
  - `/home/reid/1cfe/sysml-codegen/.project/backlog/epic_expression_aware_codegen.md` (Phase 1: EXPR-CODEGEN)
  - `/home/reid/1cfe/sysml-codegen/.project/backlog/epic_attribute_expression_capture.md` (Phase 2: ATTR-EXPR)
- **ADRs:**
  - `/home/reid/1cfe/sysml-codegen/docs/architecture/ADR-004-computed-attribute-pipeline-integration.md` (Option C, Step 4.5, naming, backtracker)
  - `/home/reid/1cfe/sysml-codegen/docs/architecture/ADR-005-computed-attribute-classification.md` (5-way classification)
- **Design:** `.project/active/e2e-attr-expr-validation/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
