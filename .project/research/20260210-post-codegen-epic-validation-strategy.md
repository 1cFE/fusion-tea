---
date: 2026-02-10T22:00:00-06:00
researcher: Claude
topic: "Post-codegen epic validation strategy from fusion-tea"
tags: [research, validation, codegen, e2e, cost-pattern]
status: complete
last_updated: 2026-02-10
---

# Research: Post-Codegen Epic Validation Strategy from Fusion-Tea

**Date**: 2026-02-10T22:00:00-06:00
**Researcher**: Claude
**Research Type**: Integration / Validation Strategy

## Research Question

After completing COST-PATTERN epic Items 1-3 and the preceding EXPR-CODEGEN + ATTR-EXPR epics (which close out the expression-compilation-and-inline-math-strategy research roadmap), what is the best way to validate from fusion-tea that everything works and that the bugs identified in the V2 report are resolved?

## Status Discrepancy

**Important finding**: The COST-PATTERN epic shows Items 1-3 as complete but **Item 4 (Pipeline Integration) as "Not Started"**. The latest sysml-codegen commit is `7887d07` (Item 3). Item 4's spec/design/plan documents are drafted but no implementation exists.

This means:
- Items 1-3 are **extraction-layer changes** (template detection, redefinition resolution, multiplicity, aggregation data models)
- These do NOT affect pipeline output yet — the data flows through new extraction functions but **isn't wired into the pipeline generator** (that's Item 4)
- The existing e2e_attr_expr and solar_battery models should produce **identical codegen output** to the V2 report baseline (same bugs, same workarounds)

**What HAS changed since the V2 report**: Nothing in the pipeline-affecting code path. The bug fixes (commit `93f0a55`) were BEFORE the V2 report. Items 1-3 add new extraction capabilities that Item 4 will wire in.

## Summary

- **For V2 bug verification**: A re-run of the V2 validation protocol is the right approach, but it will produce the same results because no pipeline-affecting changes were made after the V2 report.
- **For COST-PATTERN validation**: Item 4 must be implemented first. Then a new E2E validation (Item 5 of the epic) can test the hierarchy-aware pipeline.
- **The best immediate action is a quick regression check** to confirm the extraction-layer changes in Items 1-3 didn't break anything, followed by planning Item 4 implementation.

## Detailed Findings

### What the V2 Report Found (Bugs Still Open)

| Bug | V2 Status | Root Cause | Can Items 1-3 Fix It? |
|-----|-----------|------------|----------------------|
| Bug 2 (EXPOSE→CalcUsage wiring) | PARTIAL | Pipeline generator doesn't translate EXPOSE binding detection to MODULE_OUTPUT wiring | **No** — this is a pipeline generation issue (Item 4 territory) |
| Bug 5 (smart-regen stub upgrade) | N/A | Only manifests on re-runs with existing stubs | **No** — needs targeted test, not extraction changes |
| Bug 7 (top-level `__init__.py`) | PARTIAL | `modules/` and `handwritten/` dirs missing `__init__.py` | **Possibly** — `_ensure_package_init_files()` was enhanced in bug fix commit, but scope depends on whether codegen creates these dirs |

### What Items 1-3 Actually Changed

**Item 1 (Spike)**: Research only — no code changes to production codegen

**Item 2 (Template Detection)**:
- Added `is_template`, `owning_part_def_qn`, `raw_element` to `CalcUsageData`
- Added `_find_part_usages_of_definition()` and `_create_virtual_calc_usage()` to `usage_extractor.py`
- `extract_calculation_usages()` now accepts `expand_templates=True` (default)
- **Impact on existing models**: The `expand_templates=True` default means e2e_attr_expr and solar_battery will now have template CalcUsages expanded into virtual instances. If these models have CalcUsages inside PartDefinitions, the extraction output will differ. However, since Item 4 isn't wired, this may or may not affect the final pipeline.

**Item 3 (Hierarchy Resolver)**:
- New module: `extraction/hierarchy_resolver.py` (499 LOC)
- New data models: `RedefinitionData`, `MultiplicityData`, `AggregationExpressionData`, etc.
- Enhanced `expression_utils.py` with `reconstruct_expression()` for `sum()` handling
- **Impact on existing models**: New extraction pass runs but results aren't consumed by pipeline generator

### Validation Tiers

#### Tier 1: Regression Check (Do Now — 15 minutes)

Confirms Items 1-3 extraction changes don't break existing codegen output.

```bash
# 1. Run sysml-codegen tests (baseline: 454)
cd ~/1cfe/sysml-codegen && uv run python -m pytest -q

# 2. Run agentic-mbse tests (baseline: 886)
cd ~/1cfe/agentic-mbse && uv run python -m pytest -q

# 3. Run fusion-tea tests (baseline: 48 passed, 1 skipped)
cd ~/1cfe/fusion-tea && uv run python -m pytest tests/ -q

# 4. Run generated package tests
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr/tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr_v2/tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/ -q
```

**Expected**: All pass. If any fail, Items 1-3 introduced a regression.

**Known issue**: `solar_battery/tests/test_pipeline_integration.py::test_all_seven_metrics` has a pre-existing KeyError for `capital_recovery_factor` (1 failure).

#### Tier 2: Fresh Codegen Smoke Test (Do Now — 30 minutes)

Confirms that running codegen with Items 1-3 changes produces working output.

```bash
# Generate to a NEW directory (v3) to avoid clobbering v2
cd ~/1cfe/fusion-tea

# E2E Attr Expr
uv run sysml-codegen generate \
  --models models/tests/e2e_attr_expr/ \
  --output generated/e2e_attr_expr_v3 \
  --package-name e2e_attr_expr_v3 \
  --overwrite --verbose

# Solar Battery
uv run sysml-codegen generate \
  --models models/tests/solar_battery/ \
  --output generated/solar_battery_v3 \
  --package-name solar_battery_v3 \
  --overwrite --verbose
```

**Check points**:
1. Codegen completes without errors
2. All `_impl.py` files are `AUTO_IMPLEMENTED = True`
3. `IMPLEMENTATION_BACKLOG.md` shows 0 functions to implement
4. Compare file counts: v3 should have same or more files than v2
5. Check if `expand_templates=True` default produces different module set

**Key question**: Does template expansion in Item 2 change the solar_battery output? The solar_battery model HAS CalcUsages inside PartDefinitions (that's what the COST-PATTERN epic targets). With `expand_templates=True`, `extract_calculation_usages()` may return virtual instances instead of templates. If the downstream pipeline doesn't handle these, codegen could produce different (possibly broken) output.

**Mitigation**: If v3 codegen breaks, re-run with `expand_templates=False` to confirm it's the template expansion causing issues, not a regression.

#### Tier 3: V2 Bug Recheck (Do If Tier 2 Passes — 45 minutes)

Repeat the V2 report's structural checks on v3 output.

**Bug 2 (EXPOSE→CalcUsage)**:
```bash
# Check if financial.total_capex is wired to MODULE_OUTPUT in pipeline.yaml
grep -A5 "total_capex" generated/e2e_attr_expr_v3/pipelines/pipeline.yaml
# Expected (Bug 2 fixed): source references component_cost__total_cost (MODULE_OUTPUT)
# Expected (Bug 2 still present): source references design_params.* (ENTRY_POINT)
```

**Bug 7 (broader `__init__.py`)**:
```bash
# Check for __init__.py in all generated directories
find generated/solar_battery_v3 -type d | while read d; do
  [ -f "$d/__init__.py" ] || echo "MISSING: $d/__init__.py"
done
```

**Bug 5 (smart-regen stub upgrade)**:
```bash
# Run codegen AGAIN on an existing directory to test smart-regen
uv run sysml-codegen generate \
  --models models/tests/e2e_attr_expr/ \
  --output generated/e2e_attr_expr_v3 \
  --package-name e2e_attr_expr_v3 \
  --smart-regen --preserve-handwritten --verbose
# Check: all _impl.py files should still be AUTO_IMPLEMENTED (not downgraded to stubs)
```

#### Tier 4: Pipeline Execution (Do If Tier 3 Passes — 1 hour)

Run TEAx pipelines on v3 output and verify numerical results.

**E2E Attr Expr** (16 values):
```bash
cd ~/1cfe/fusion-tea
# May need to adapt run_pipeline.py for v3 package name
# Or copy v2's run_pipeline.py and verify_pipeline.py, adjusting imports
PYTHONPATH=generated uv run python generated/e2e_attr_expr_v3/run_pipeline.py
PYTHONPATH=generated uv run python generated/e2e_attr_expr_v3/verify_pipeline.py
```

**Solar Battery** (7 values):
```bash
# Solar battery requires hybrid merge (ComponentCostEvaluator)
# This is the same architectural integration as v1/v2
# Merge handwritten files from v2, then run
PYTHONPATH=generated uv run python generated/solar_battery_v3/run_pipeline.py
PYTHONPATH=generated uv run python generated/solar_battery_v3/verify_pipeline.py
```

**Expected**: All values match V2 report ground truth within tolerances.

#### Tier 5: Hierarchy Validation (After Item 4 is Implemented)

This tier validates the COST-PATTERN epic's core value proposition. **Cannot run until Item 4 is complete.**

**Test**: Run codegen on solar_battery model and verify hierarchy-aware output:

1. **9 leaf-part cost modules generated** with hierarchy-aware names:
   - `solar_array__pv_module__cost_model`
   - `solar_array__inverter__cost_model`
   - `solar_array__array_bos__cost_model`
   - `battery_system__battery_pack__cost_model`
   - `battery_system__hybrid_inverter__cost_model`
   - `battery_system__battery_bos__cost_model`
   - `site_infra__racking__cost_model`
   - `site_infra__electrical_panel__cost_model`
   - `site_infra__permitting__cost_model`

2. **4 aggregation modules generated**:
   - `solar_array__capital_cost` (with multiplicity entry points)
   - `battery_system__capital_cost`
   - `site_infra__capital_cost`
   - `solar_battery_plant__capital_cost`

3. **System-level CalcUsages wire to hierarchy outputs** (not entry points)

4. **LCOE pipeline produces numerically correct result end-to-end**

5. **IMPLEMENTATION_BACKLOG.md shows 0 functions to implement**

6. **No workarounds needed** (Bug 2 should be fully fixed by Item 4's binding rewriting)

## Recommendations

### Immediate Actions (Today)

1. **Run Tier 1 (regression check)** — 15 min, zero risk
2. **Run Tier 2 (fresh codegen smoke test)** — 30 min, watch for template expansion effects
3. **If Tier 2 passes**: Run Tiers 3-4 for full V2 revalidation

### Strategic Decision

The research roadmap (expression-compilation-and-inline-math-strategy) is NOT fully closed out:
- Phase 1 (Expression Compiler / EXPR-CODEGEN) = DONE
- Phase 2 (Attribute Expression Capture / ATTR-EXPR) = DONE
- Phase 3 (Hierarchy/Multiplicity/Aggregation / COST-PATTERN) = **INCOMPLETE** (Items 1-3 of 5 done, Item 4 is the critical integration step)

**To close out the research roadmap**, the path is:
1. Implement Item 4 (Pipeline Integration) — ~2-2.5 days
2. Run Tier 5 validation (hierarchy-aware E2E)
3. Implement Item 5 (E2E Validation & Documentation) — ~1.5-2 days
4. Write ADR-006, ADR-007, amend ADR-002

### Validation Script Template

For Tier 4, here's a reusable validation script pattern that can be adapted for v3:

```python
#!/usr/bin/env python3
"""Validation script for post-codegen-epic verification."""

import json
import sys
from pathlib import Path

EXPECTED_VALUES = {
    # E2E Attr Expr ground truth (16 values)
    "power_mw": (0.005, 0.0),
    "power_kw": (5.0, 0.0),
    "annual_om": (100.0, 0.0),
    "area": (50.0, 0.0),
    "volume": (150.0, 0.0),
    "surface_cost": (600.0, 0.0),
    "material_cost": (5000.0, 0.0),
    "fab_cost": (2250.0, 0.0),
    "install_cost": (1500.0, 0.0),
    "total_cost": (8750.0, 0.0),
    "idiot_index": (1.75, 0.0),
    "crf": (0.07095246, 1e-6),
    "annualized_cost": (620.834, 1e-6),
    "annual_energy_mwh": (39.42, 0.0),
    "lcoe": (18.286, 1e-4),
    "total_capex": (8750.0, 0.0),
}

def check_value(name, expected, actual, tolerance):
    if tolerance == 0.0:
        ok = expected == actual
    else:
        ok = abs(expected - actual) <= tolerance
    status = "PASS" if ok else "FAIL"
    print(f"  {status}: {name} = {actual} (expected {expected}, tol {tolerance})")
    return ok

def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not output_dir or not output_dir.exists():
        print(f"Usage: python validate.py <output_dir>")
        sys.exit(1)

    all_pass = True
    for name, (expected, tol) in EXPECTED_VALUES.items():
        json_file = output_dir / f"{name}.json"
        if not json_file.exists():
            # Try channel-prefixed naming
            candidates = list(output_dir.glob(f"*__{name}.json"))
            if candidates:
                json_file = candidates[0]
            else:
                print(f"  SKIP: {name} — no output file found")
                continue
        with open(json_file) as f:
            data = json.load(f)
        actual = data.get("root", data.get("value", data.get(name)))
        if actual is None:
            print(f"  FAIL: {name} — could not extract value from {json_file}")
            all_pass = False
            continue
        if not check_value(name, expected, actual, tol):
            all_pass = False

    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
```

## Open Questions

1. **Does `expand_templates=True` (Item 2 default) affect solar_battery codegen output?** The solar_battery model has CalcUsages inside PartDefinitions. With template expansion, the extraction layer returns virtual instances. If the downstream pipeline can't handle the longer qualified names or different binding structure, codegen may break. This needs testing.

2. **Should we implement Item 4 before running Tiers 3-4?** If Item 2's template expansion changes the solar_battery output, we may be validating against a moving target. Consider running Tier 2 first to assess impact.

3. **What's the fastest path to close the research roadmap?** Item 4 is the critical bottleneck. It has detailed spec/design/plan already written. Estimated 2-2.5 days.

---

**Related Commands:**
- Run validation: Tier 1-4 commands above
- Next implementation: Item 4 of COST-PATTERN epic
- After Item 4: Item 5 (E2E Validation & Documentation)

**Last Updated**: 2026-02-10
