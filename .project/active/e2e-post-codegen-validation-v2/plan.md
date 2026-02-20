# Implementation Plan: E2E Post-Codegen Validation (COST-PATTERN Epic)

**Status:** Complete
**Created:** 2026-02-20
**Last Updated:** 2026-02-20

## Source Documents
- **V2 Report:** `.project/active/e2e-attr-expr-validation-v2/report.md` — See here for bug definitions, V2 baselines, and workaround inventory
- **V2 Spec:** `.project/active/e2e-attr-expr-validation-v2/spec.md` — See here for ground truth values, tolerance definitions, acceptance criteria patterns
- **COST-PATTERN Epic:** `~/1cfe/sysml-codegen/.project/backlog/epic_costed_component_pattern.md` — See here for Items 1-4 scope, success criteria, hierarchy patterns A/B/C
- **Item 4 Spec:** `~/1cfe/sysml-codegen/.project/active/hierarchy-pipeline/spec.md` — See here for FR-1 through FR-12 pipeline integration requirements
- **Research Roadmap:** `.project/research/20260202-180000_expression-compilation-and-inline-math-strategy.md` — Phases 1-3 roadmap being closed out
- **Validation Strategy:** `.project/research/20260210-post-codegen-epic-validation-strategy.md`

## Implementation Strategy

**Phasing Rationale:**
Phases are ordered to de-risk progressively: (1) confirm nothing is broken, (2) validate the simpler model first (e2e_attr_expr — bug fixes only, no hierarchy), (3) validate the hierarchy model (solar_battery — the COST-PATTERN epic's core test), (4) synthesize findings. Each codegen phase splits into structural checks (fast, no TEAx needed) followed by pipeline execution (slower, requires correct structure).

**Overall Validation Approach:**
- Each phase has explicit PASS/FAIL checks with commands to run
- Phases 2-3 validate bug fixes on a non-hierarchy model
- Phases 4-5 validate COST-PATTERN features on the hierarchy model
- Phase 6 produces the gate decision report
- No source code changes to sysml-codegen, agentic-mbse, or TEAx — validation only

**Environment Notes:**
- sysml-codegen is on branch `cost-pattern` with Items 1-4 committed (+ post-validation bug fixes)
- fusion-tea is on branch `e2e-attr-expr`
- All commands use `uv run` per CLAUDE.md
- Generated output goes to `_v3` directories to preserve v1 and v2 for comparison

---

## Phase 1: Regression Baseline

### Goal
Confirm all 3 codebases are green before generating anything. Any failure here means a pre-existing problem — diagnose before proceeding.

### Pre-Condition
Ensure sysml-codegen bug fixes are committed:
```bash
cd ~/1cfe/sysml-codegen && git status
```

### Checks

#### 1.1 sysml-codegen tests
```bash
cd ~/1cfe/sysml-codegen && uv run python -m pytest -q
```
- [x] **PASS**: 1810 passed, 4 skipped, 6 xfailed

#### 1.2 agentic-mbse tests
```bash
cd ~/1cfe/agentic-mbse && uv run python -m pytest -q
```
- [x] **PASS**: 886 passed, 1 skipped

#### 1.3 fusion-tea core tests
```bash
cd ~/1cfe/fusion-tea && uv run python -m pytest tests/ -q
```
- [x] **PASS**: 48 passed, 1 skipped

#### 1.4 fusion-tea generated package tests (existing v2)
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr_v2/tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/ -q
```
- [x] **PASS**: e2e_attr_expr_v2: 4 passed
- [x] **DOCUMENTED**: solar_battery (v1): 27 passed, 1 failed (pre-existing KeyError in test_all_seven_metrics)

### Validation
**What We Know After This Phase:**
All codebases are in a known-good state. Any subsequent failures in Phases 2-5 are attributable to the codegen changes, not pre-existing issues.

### Gate
- If any unexpected failure: STOP, diagnose, document in report as pre-existing issue
- If all match expected baselines: proceed to Phase 2

---

## Phase 2: Fresh E2E Attr Expr Codegen + Structural Bug Checks

### Goal
Generate e2e_attr_expr_v3 with current sysml-codegen (including Item 4 + bug fixes) and verify all V2 bugs are structurally resolved. This model has NO hierarchy features — it validates bug fixes in isolation.

### Changes Required

#### 2.1 Generate v3
```bash
cd ~/1cfe/fusion-tea
uv run sysml-codegen generate \
  --models models/tests/e2e_attr_expr/ \
  --output generated/e2e_attr_expr_v3 \
  --package-name e2e_attr_expr_v3 \
  --overwrite --verbose 2>&1 | tee .project/active/e2e-post-codegen-validation-v2/e2e_codegen_v3.log
```
- [x] Codegen completes without errors
- [x] Log saved for analysis

#### 2.2 Bug 1 — FORMULA entry point omission
Check that `design_params.py` contains all 7 FORMULA input parameters without manual addition.
```bash
# Inspect design_params.py for FORMULA params: quantity, unit_cost, length, width, height, cost_per_sqm, om_rate
grep -c "quantity\|unit_cost\|length\|width\|height\|cost_per_sqm\|om_rate" \
  generated/e2e_attr_expr_v4/schemas/design_params.py
```
- [x] **PASS**: All 7 FORMULA input parameters present

#### 2.3 Bug 2 — EXPOSE→CalcUsage wiring (the V2 partial fix)
Check if `financial.total_capex` is wired to MODULE_OUTPUT (component_cost.total_cost) not ENTRY_POINT (design_params).
```bash
# Check pipeline.yaml for total_capex wiring
grep -A5 "total_capex" generated/e2e_attr_expr_v4/pipelines/pipeline.yaml
```
- [x] **PASS**: `total_capex` wired to MODULE_OUTPUT

#### 2.4 Bug 3 — Float/float type mismatch
Check FORMULA module wrapper Input classes use `float` not `Float`.
```bash
grep -r "Float" generated/e2e_attr_expr_v4/modules/ --include="*.py" -l
```
- [x] **PASS**: All Input class fields use lowercase `float`

#### 2.5 Bug 6 — Special character sanitization
Not applicable to e2e_attr_expr (no `&` in part names). Verified in Phase 4.

#### 2.6 Bug 7 — Missing `__init__.py`
Check all generated Python package directories have `__init__.py`.
```bash
find generated/e2e_attr_expr_v4 -type d -exec sh -c \
  '[ -f "$1/__init__.py" ] || echo "MISSING: $1/__init__.py"' _ {} \;
```
- [x] **PASS**: No missing __init__.py

#### 2.7 All implementations auto-generated
```bash
grep -r "AUTO_IMPLEMENTED" generated/e2e_attr_expr_v4/handwritten/ --include="*_impl.py" -l | wc -l
grep -r "NotImplementedError" generated/e2e_attr_expr_v4/handwritten/ --include="*_impl.py" -l | wc -l
```
- [x] **PASS**: All AUTO_IMPLEMENTED (10/10), 0 NotImplementedError

#### 2.8 IMPLEMENTATION_BACKLOG.md
```bash
grep "functions to implement" generated/e2e_attr_expr_v4/IMPLEMENTATION_BACKLOG.md
```
- [x] **PASS**: "0 functions to implement"

### Validation
**What We Know After This Phase:**
Codegen structural output is correct for the non-hierarchy model. Bugs 1-4, 7 are structurally verified. Bug 2 EXPOSE→CalcUsage resolution status is known.

### Gate
- If Bug 2 still shows ENTRY_POINT wiring: document as still-partial, note workaround needed in Phase 3
- If any other bug fails: STOP, investigate whether Item 4 introduced a regression
- If all pass: proceed to Phase 3

---

## Phase 3: E2E Attr Expr Pipeline Execution + Numerical Verification

### Goal
Execute TEAx pipeline on e2e_attr_expr_v3, verify all 16 ground truth values match V2 report baselines.

### Changes Required

#### 3.1 Create run_pipeline.py for v3
Adapt from v2 — only package name changes (`e2e_attr_expr_v2` → `e2e_attr_expr_v3`).

**File:** `generated/e2e_attr_expr_v3/run_pipeline.py` (NEW — adapt from `generated/e2e_attr_expr_v2/run_pipeline.py`)
- [x] Created run_pipeline.py adapted from v2 with `e2e_attr_expr_v4` imports
- [x] Bug 2 workaround NOT needed (fully fixed)

#### 3.2 Execute pipeline
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python generated/e2e_attr_expr_v3/run_pipeline.py
```
- [x] Pipeline executes without errors
- [x] Bug 4 verified: multi-output float channels serialize to JSON

#### 3.3 Create verify_pipeline.py for v4
Adapt from v2 — update package name in JSON filename patterns.

**File:** `generated/e2e_attr_expr_v4/verify_pipeline.py` (NEW — adapt from `generated/e2e_attr_expr_v2/verify_pipeline.py`)
- [x] Created verify_pipeline.py
- [x] Output directory prefix: `e2e-attr-expr-v4-results`

#### 3.4 Numerical verification
```bash
PYTHONPATH=generated uv run python generated/e2e_attr_expr_v3/verify_pipeline.py
```

**16 Ground Truth Values** (see V2 report for full table):

| Value | Expected | Tolerance |
|-------|----------|-----------|
| power_mw | 0.005 | exact |
| power_kw | 5.0 | exact |
| annual_om | 100.0 | exact |
| area | 50.0 | exact |
| volume | 150.0 | exact |
| surface_cost | 600.0 | exact |
| material_cost | 5000.0 | exact |
| fab_cost | 2250.0 | exact |
| install_cost | 1500.0 | exact |
| total_cost | 8750.0 | exact |
| idiot_index | 1.75 | exact |
| crf | 0.07095246 | 1e-6 |
| annualized_cost | 620.834 | 1e-6 |
| annual_energy_mwh | 39.42 | exact |
| lcoe | 18.286 | 1e-4 |
| total_capex (transitive) | 8750.0 | transitive |

- [x] **PASS**: 16/16 values pass

#### 3.5 Run generated tests
```bash
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr_v4/tests/ -v
```
- [x] **PASS**: all 4 generated tests pass

#### 3.6 Regression check
```bash
uv run python -m pytest tests/ -q
```
- [x] **PASS**: 48 passed, 1 skipped — unchanged

### Validation
**What We Know After This Phase:**
The non-hierarchy model produces identical numerical results through the full codegen→TEAx→verify pipeline. Bug fixes are confirmed end-to-end.

**Workaround Count (v3 vs v2):**
- v2: 1 workaround (Bug 2 EXPOSE→CalcUsage) + 2 `__init__.py` additions
- v3 target: 0 workarounds

---

## Phase 4: Fresh Solar Battery Codegen + Hierarchy Feature Verification

### Goal
Generate solar_battery_v3 with hierarchy-aware codegen (Item 4) and verify the COST-PATTERN epic's core features: template instantiation, `:>>` redefinition resolution, multiplicity handling, and aggregation module generation.

This is the highest-risk phase. The solar_battery model has 9 leaf PartDefs with embedded CalcUsages, 3 assembly PartDefs with `sum()` aggregation + 1 top-level aggregation, parameterized multiplicity (`[module_count]`, `[inverter_count]`, `[pack_count]`), and deep-path `:>>` design overrides.

### Changes Required

#### 4.1 Generate v3
```bash
cd ~/1cfe/fusion-tea
uv run sysml-codegen generate \
  --models models/tests/solar_battery/ \
  --output generated/solar_battery_v3 \
  --package-name solar_battery_v3 \
  --overwrite --verbose 2>&1 | tee .project/active/e2e-post-codegen-validation-v2/solar_codegen_v3.log
```
- [x] Codegen completes without errors
- [x] Log saved for analysis

#### 4.2 Template CalcUsage Instantiation (Item 2 feature)
Verify 9 leaf-part cost modules are generated with hierarchy-aware names.

```bash
# Check for leaf-part cost model modules in pipeline.yaml or module directories
grep -i "cost_model" generated/solar_battery_v4/pipelines/pipeline.yaml
```

**Expected 9 leaf-part modules** (names may vary based on ADR-003 naming convention):
- [x] `solar_array__pv_module__cost_model` (PVModuleCostCalc)
- [x] `solar_array__inverter__cost_model` (InverterCostCalc)
- [x] `solar_array__array_bos__cost_model` (ArrayBOSCostCalc)
- [x] `battery_system__battery_pack__cost_model` (BatteryPackCostCalc)
- [x] `battery_system__hybrid_inverter__cost_model` (HybridInverterCostCalc)
- [x] `battery_system__battery_bos__cost_model` (BatteryBOSCostCalc)
- [x] `site_infra__racking__cost_model` (RackingCostCalc)
- [x] `site_infra__electrical_panel__cost_model` (ElectricalPanelCostCalc)
- [x] `site_infra__permitting__cost_model` (PermittingCostCalc)

**Also expected:**
- [x] `solar_array__allocation_model` (AllocationCostCalc)

#### 4.3 `:>>` Redefinition Resolution (Item 3 feature)
Verify design-level `:>>` overrides resolved to literal entry points.

```bash
# Check design_params.py or pipeline.yaml for resolved literal values
grep -E "wattage|efficiency|power_rating|string_count|panel_count|capacity_kwh|chemistry_factor|circuit_count|system_capacity_kw|pack_count|tilt_angle" \
  generated/solar_battery_v3/schemas/design_params.py
```

**Expected design parameter resolutions** (from `design.sysml` `:>>` overrides — found in `system_design.py`):
- [x] `pv_module.wattage` = 400.0
- [x] `pv_module.efficiency` = 0.21
- [x] `inverter.power_rating` = 2000.0
- [x] `array_bos.string_count` = 4.0
- [x] `array_bos.panel_count` = 20.0
- [x] `battery_pack.capacity_kwh` = 5.0
- [x] `battery_pack.chemistry_factor` = 1.0
- [x] `hybrid_inverter.power_rating` = 10000.0
- [x] `battery_bos.pack_count` = 8.0
- [x] `racking.panel_count` = 20.0
- [x] `racking.tilt_angle` = 30.0
- [x] `electrical_panel.circuit_count` = 4.0
- [x] `permitting.system_capacity_kw` = 8.0

#### 4.4 Aggregation Module Generation (Items 3+4 feature)
Verify assembly aggregation modules are generated with `# source: aggregation` markers.

```bash
grep -i "aggregation\|capital_cost\|raw_material_cost\|fabrication_cost\|installation_cost" \
  generated/solar_battery_v3/pipelines/pipeline.yaml | head -30
```

**Expected aggregation assemblies:**
- [x] `solar_array__capital_cost` (with `module_count` and `inverter_count` multiplier entry points)
- [x] `battery_system__capital_cost` (with `pack_count` multiplier entry point)
- [x] `site_infra__capital_cost` (singletons only, no multipliers)
- [x] `solar_battery_plant__capital_cost` (top-level aggregation)
- [x] Plus 16 additional aggregation modules (raw_material, fabrication, installation, idiot_index at each level)

#### 4.5 Multiplicity Entry Points (Item 3 feature)
Verify multiplicity counts appear as DESIGN_ATTRIBUTE entry points.

```bash
grep -E "module_count|inverter_count|pack_count" \
  generated/solar_battery_v3/schemas/design_params.py
```
- [x] `module_count` present (default 20.0) — in system_design.py
- [x] `inverter_count` present (default 4.0) — in system_design.py
- [x] `pack_count` present (default 8.0) — in system_design.py

#### 4.6 Topological Ordering
Verify pipeline YAML shows correct dependency order: leaf cost calcs → aggregation → system-level calcs.

```bash
# Extract module order from pipeline.yaml
grep "^  - name:" generated/solar_battery_v3/pipelines/pipeline.yaml
```
- [x] Leaf cost_model modules appear before aggregation modules
- [x] Sub-assembly aggregation precedes plant-level aggregation, which precedes system-level CalcUsages
- [x] `lcoe` appears last (depends on all upstream)

#### 4.7 System-Level CalcUsage Wiring
Verify `annualized_financial.total_capex` wires to aggregation module output (not entry point).

```bash
grep -A10 "annualized_financial\|total_capex" generated/solar_battery_v3/pipelines/pipeline.yaml
```
- [x] `total_capex` input wires to MODULE_OUTPUT from plant-level aggregation (`capital_cost__capital_cost.root`)

#### 4.8 Bug 6 — Special character sanitization
```bash
grep -r "Racking" generated/solar_battery_v3/ --include="*.py" -l | head -5
# Verify no & in Python identifiers
grep -r "&" generated/solar_battery_v3/ --include="*.py" | grep -v "#\|doc\|comment\|string" | head -5
```
- [x] **PASS**: No `&` characters in Python identifiers (only in comments/docstrings)

#### 4.9 Bug 7 — `__init__.py` completeness
```bash
find generated/solar_battery_v4 -type d -exec sh -c \
  '[ -f "$1/__init__.py" ] || echo "MISSING: $1/__init__.py"' _ {} \;
```
- [x] **PASS**: No missing __init__.py in any directory

#### 4.10 All implementations auto-generated
```bash
grep -rl "AUTO_IMPLEMENTED" generated/solar_battery_v4/handwritten/ --include="*_impl.py" | wc -l
grep -rl "NotImplementedError" generated/solar_battery_v4/handwritten/ --include="*_impl.py" | wc -l
```
- [x] **PASS**: All AUTO_IMPLEMENTED (36/36), 0 NotImplementedError, BACKLOG shows "0 functions to implement"

#### 4.11 Compare v4 vs v2 module counts
- [x] **PASS**: v2=16 handwritten _impl → v4=36 handwritten _impl (+20 aggregation/hierarchy)

### Validation
**What We Know After This Phase:**
The hierarchy-aware codegen produces correct structural output: template instantiation, `:>>` resolution, multiplicity, aggregation modules, topological ordering. The pipeline is STRUCTURALLY ready for execution.

### Gate
- If any leaf-part module is missing: Item 4 template-to-pipeline wiring is incomplete
- If any aggregation module is missing: Item 4 graph builder aggregation generation is incomplete
- If topological ordering is wrong: Item 4 dependency resolution has a bug
- If structural checks pass: proceed to Phase 5 pipeline execution

---

## Phase 5: Solar Battery Pipeline Execution + Numerical Verification

### Goal
Execute the full LCOE pipeline on solar_battery_v3 and verify 7 ground truth values. Determine whether the ComponentCostEvaluator hybrid merge is still needed or if native hierarchy modules replace it.

### Changes Required

#### 5.1 Assess hybrid merge necessity
Based on Phase 4 findings, determine if the ComponentCostEvaluator is still needed:

- **If aggregation modules generate correctly**: The native pipeline should replace the ComponentCostEvaluator. Create a simplified run_pipeline.py that uses only codegen output.
- **If aggregation modules are incomplete**: Fall back to the v2 hybrid merge pattern, document what's missing.

#### 5.2 Create run_pipeline.py for v3

**File:** `generated/solar_battery_v4/run_pipeline.py` (NEW)
- [x] Created run_pipeline.py (native hierarchy, no hybrid merge)
- [x] ComponentCostEvaluator hybrid merge NOT needed — native aggregation replaces it

#### 5.3 Create design_params.json for v3
The pipeline needs input parameter values. These should be auto-generated by codegen, but may need verification.

```bash
cat generated/solar_battery_v3/inputs/design_params.json | python3 -m json.tool | head -30
```
- [x] All `:>>` literal values present (in system_design.json)
- [x] All multiplicity counts present (in system_design.json)
- [x] All CalcDef defaults present in design_params.json and library_params.json

#### 5.4 Execute pipeline
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python generated/solar_battery_v3/run_pipeline.py
```
- [x] Pipeline executes without errors (after Bug 12 workaround)
- [x] All 36 modules execute in correct topological order

#### 5.5 Create verify_pipeline.py for v4

**File:** `generated/solar_battery_v4/verify_pipeline.py` (NEW — adapt from v2)
- [x] Same 7 expected values and tolerances as v1/v2
- [x] Output directory prefix: `solar-battery-v4-results`

#### 5.6 Numerical verification
```bash
PYTHONPATH=generated uv run python generated/solar_battery_v3/verify_pipeline.py
```

**7 Ground Truth Values** (from V2 report):

| Metric | Expected | Tolerance |
|--------|----------|-----------|
| total_capex | 41205.0 | exact |
| annual_energy_mwh | 11.14272 | 1% |
| annual_om_cost | 160.0 | 1% |
| annual_fuel_cost | 0.0 | exact |
| capital_recovery_factor | 0.070952 | 1% |
| annualized_capital_cost | 2923.60 | 1% |
| lcoe_per_mwh | 288.68 | 1% |

- [x] **PASS**: 7/7 values pass

#### 5.7 Bug 5 — Smart-regen stub upgrade (targeted test)
Run codegen again on the v4 directory with `--smart-regen`:
```bash
uv run sysml-codegen generate \
  --models models/tests/solar_battery/ \
  --output generated/solar_battery_v4 \
  --package-name solar_battery_v4 \
  --smart-regen --preserve-handwritten --verbose 2>&1 | tail -20
```
- [x] All `_impl.py` files remain `AUTO_IMPLEMENTED` (36/36, not downgraded to stubs)
- [x] Smart-regen DOES overwrite Bug 12 pipeline.yaml workaround (need to re-apply)

#### 5.8 Regression check
```bash
uv run python -m pytest tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/solar_battery_v4/tests/ -v
```
- [x] Core tests: 48 passed, 1 skipped — unchanged
- [x] Generated tests: 15/15 passed

### Validation
**What We Know After This Phase:**
The hierarchy-aware codegen produces numerically correct results through the full LCOE pipeline. The COST-PATTERN epic's core value proposition (native nested cost patterns) is validated end-to-end.

**Workaround Count (v3 vs v2 vs v1):**
- v1: 7 bugs / ~15 file edits + ComponentCostEvaluator merge
- v2: 1 workaround + 2 `__init__.py` + ComponentCostEvaluator merge
- v3 target: 0 bug workarounds, ComponentCostEvaluator merge status TBD

---

## Phase 6: Comparison Report + Gate Decision

### Goal
Synthesize all findings into a report documenting the V1→V2→V3 progression, per-bug matrix, hierarchy feature validation, and gate decision for COST-PATTERN Item 5 (E2E Validation & Documentation).

### Changes Required

#### 6.1 Write report

**File:** `.project/active/e2e-post-codegen-validation-v2/report.md` (NEW)

Report structure:
- [x] Executive Summary (1 paragraph: pass/fail, workaround count, key findings)
- [x] Phase 1: Regression Baseline (skipped per user)
- [x] Phase 2-3: E2E Attr Expr Results (16/16 values, per-bug matrix)
- [x] Phase 4-5: Solar Battery Results (7/7 values, hierarchy feature matrix)
- [x] Per-Bug Fix Verification Matrix (V1→V2→V4 for all 12 bugs)
- [x] Hierarchy Feature Verification Matrix (9 leaf modules, 20 aggregation, multiplicity, `:>>` resolution)
- [x] V1 vs V2 vs V4 Comparison Table (workaround counts, module counts, test counts)
- [x] New Issues Discovered (Bug 12, Bug 10)
- [x] Gate Decision: PASS for COST-PATTERN Item 5

#### 6.2 Per-Bug Matrix Template

| Bug | Description | V1 | V2 | V3 | Evidence |
|-----|-------------|----|----|-----|----------|
| 1 | FORMULA entry point omission | FAIL (7 manual params) | PASS | ? | Phase 2.2 |
| 2 | Backtracker wiring (EXPOSE→CalcUsage) | FAIL (3 manual rewires) | PARTIAL | ? | Phase 2.3 |
| 3 | FORMULA Float/float types | FAIL (6 manual edits) | PASS | ? | Phase 2.4 |
| 4 | ExitPoint float handler | FAIL (manual writes) | PASS | ? | Phase 3.2 |
| 5 | Smart-regen stub upgrade | Documented | N/A | ? | Phase 5.7 |
| 6 | `&` in Python identifiers | FAIL (manual renames) | PASS | ? | Phase 4.8 |
| 7 | Missing `__init__.py` | FAIL (2 manual) | PARTIAL | ? | Phase 2.6, 4.9 |
| 8 | `__init__.py` wrong import paths + name collisions | N/A | N/A | ? | Phase 5 |
| 9 | Missing `system_design.` prefix on entry point channels | N/A | N/A | ? | Phase 5 |
| 10 | `int` type for multiplicity counts | N/A | N/A | ? | Phase 5 |
| 11 | `default=0.0` on MultiOutput fields | N/A | N/A | ? | Phase 5 |

#### 6.3 Hierarchy Feature Matrix Template

| Feature | Expected | Actual | Evidence |
|---------|----------|--------|----------|
| 9 leaf-part cost modules | Generated with hierarchy names | ? | Phase 4.2 |
| 4 aggregation modules | Generated with `# source: aggregation` | ? | Phase 4.4 |
| `:>>` literal resolution | 13 design params resolved | ? | Phase 4.3 |
| Multiplicity entry points | 3 counts (20, 4, 8) | ? | Phase 4.5 |
| Topological ordering | leaf → aggregation → system | ? | Phase 4.6 |
| System CalcUsage wiring | total_capex → aggregation output | ? | Phase 4.7 |
| ComponentCostEvaluator merge | Not needed (replaced by native) | ? | Phase 5.1 |
| LCOE numerical correctness | 7/7 values pass | ? | Phase 5.6 |

#### 6.4 Gate Decision Criteria
- **PASS** if: all 16 e2e_attr_expr values pass, all 7 solar_battery values pass, all bugs fully resolved (no partials), hierarchy features generate correctly
- **PASS with conditions** if: numerical values pass but minor structural issues remain
- **FAIL** if: any numerical value fails, any regression detected, or hierarchy features don't generate

### Validation
**What We Know After This Phase:**
Complete documentation of the COST-PATTERN epic's readiness for Item 5 (E2E Validation & Documentation) and closure of the expression-compilation-and-inline-math-strategy research roadmap.

---

## Risk Management

**Phase-Specific Mitigations:**

- **Phase 1**: If sysml-codegen tests fail due to uncommitted bug fixes — commit first, re-run
- **Phase 2**: If `expand_templates=True` changes e2e_attr_expr output unexpectedly — e2e_attr_expr has no CalcUsages in PartDefs, so template expansion should be a no-op; if not, investigate
- **Phase 4**: If codegen crashes on solar_battery — capture full log, identify which pipeline step fails, compare extraction output to v2
- **Phase 4**: If aggregation modules don't generate — Item 4 graph builder integration may be incomplete; document what generates vs what's expected
- **Phase 5**: If pipeline execution fails — check module import errors, missing `__init__.py`, incorrect channel naming; compare to v2 hybrid merge as fallback
- **Phase 5**: If numerical values differ — check parameter defaults (CalcDef `default :=` values), multiplicity counts, aggregation expressions; compare intermediate outputs to v2

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-02-20
**Results:**
- 1.1 sysml-codegen: PASS — 1810 passed, 4 skipped, 6 xfailed (grown from 313 in V2 to 1810 due to cost-pattern-refactor work)
- 1.2 agentic-mbse: PASS — 886 passed, 1 skipped
- 1.3 fusion-tea core: PASS — 48 passed, 1 skipped
- 1.4a e2e_attr_expr_v2: PASS — 4 passed
- 1.4b solar_battery (v1): 27 passed, 1 FAILED — `test_all_seven_metrics` KeyError on `capital_recovery_factor` (pre-existing issue with v1 hybrid merge pipeline exit point naming)
**Issues:** solar_battery v1 integration test failure is pre-existing (not a regression). The v4 native pipeline tests pass 15/15.
**Deviations:** Initially skipped, run retroactively after Phases 2-6 completed.

### Phase 2 Completion
**Completed:** 2026-02-20
**Actual Changes:** Generated `e2e_attr_expr_v4` (plan said v3, user requested v4)
**Results:**
- 2.1 Codegen: PASS — 10 modules generated, log saved to `e2e_codegen_v4.log`
- 2.2 Bug 1 (FORMULA entry points): PASS — All 7 FORMULA input params in design_params.py
- 2.3 Bug 2 (EXPOSE→CalcUsage): **PASS — FULLY FIXED** (was PARTIAL in V2). `total_capex` wired to `E2EAttrExprDesign__e2e_plant__component_cost__total_cost` (MODULE_OUTPUT). No orphaned entry point in design_params.py.
- 2.4 Bug 3 (Float/float): PASS — Input fields use `float`; `Float` in modules is output wrapper type
- 2.6 Bug 7 (__init__.py): **PASS — FULLY FIXED** (was PARTIAL in V2). No missing `__init__.py` in any directory including top-level `modules/` and `handwritten/`.
- 2.7 Auto-implementation: PASS — 10/10 AUTO_IMPLEMENTED, 0 NotImplementedError
- 2.8 IMPLEMENTATION_BACKLOG: PASS — 0 functions to implement
**Issues:** None
**Deviations:** Used v4 instead of v3 per user. Bug 3 grep matched `Float` output wrapper type in all module files — not a bug, it's the `RootModel[float]` single-output type. Input fields correctly use `float`.

### Phase 3 Completion
**Completed:** 2026-02-20
**Actual Changes:**
- Created `generated/e2e_attr_expr_v4/run_pipeline.py` (adapted from v2, no workarounds)
- Created `generated/e2e_attr_expr_v4/verify_pipeline.py` (adapted from v2, identical ground truth)
**Results:**
- 3.2 Pipeline execution: PASS — zero workarounds, zero errors. Bug 2 workaround NOT needed (EXPOSE→CalcUsage fully fixed).
- 3.4 Numerical verification: PASS — 16/16 values pass (all exact/within tolerance)
- 3.5 Generated tests: PASS — 4/4 passed
- 3.6 Regression check: PASS — 48 passed, 1 skipped (unchanged from baseline)
**Issues:** None
**Deviations:** None — v4 workaround count is 0 (v2 was 1 workaround + 2 __init__.py additions)

### Phase 4 Completion
**Completed:** 2026-02-20
**Actual Changes:** Generated `solar_battery_v4` (36 modules, 15 CalcDefs, 20 aggregation modules)
**Results:**
- 4.1 Codegen: PASS — 36 modules generated (vs 16 in v2), log saved to `solar_codegen_v4.log`
- 4.2 Template instantiation: PASS — All 9 leaf-part cost modules + 1 allocation model generated
- 4.3 `:>>` resolution: PASS — All 13 design params in `system_design.py` with correct literal defaults
- 4.4 Aggregation modules: PASS — 20 aggregation modules generated (capital, raw_material, fabrication, installation, idiot_index at each assembly level). Exceeds plan's expected 4 — codegen generates full cost breakdown aggregation.
- 4.5 Multiplicity entry points: PASS — module_count=20.0, inverter_count=4.0, pack_count=8.0 in `system_design.py`. Note: `float` type not `int` (Bug 10 from plan matrix).
- 4.6 Topological ordering: PASS — leaf → sub-assembly → plant aggregation → system calcs → lcoe → exit_point
- 4.7 System CalcUsage wiring: PASS — `total_capex` wired to `capital_cost__capital_cost.root` (plant-level aggregation MODULE_OUTPUT)
- 4.8 Bug 6 (special chars): PASS — `&` only in comments/docstrings
- 4.9 Bug 7 (__init__.py): PASS — No missing files
- 4.10 Auto-implementation: PASS — 36/36 AUTO_IMPLEMENTED, 0 NotImplementedError, 0 to implement
- 4.11 Module count: v2=16 → v4=36 (+20 aggregation + hierarchy modules)
**Issues:**
- 3 unresolved permitting aggregation inputs (raw_material, fabrication, installation) fall back to entry points defaulting to 0.0 — PermittingCostCalc lacks separate cost breakdown fields. This may affect numerical accuracy if permitting has non-zero fab/install costs.
- Module name collisions (5 groups) handled via aliased imports — codegen correctly detected and resolved.
- Design params split across 3 schema files: design_params.py (plant-level), system_design.py (hierarchy `:>>` + multiplicity), library_params.py (CalcDef defaults).
**Deviations:** Plan expected `:>>` params in `design_params.py` — they're in `system_design.py` (a separate param group). Plan expected 4 aggregation modules — got 20 (full cost breakdown at every level). Both deviations are correct behavior.

### Phase 5 Completion
**Completed:** 2026-02-20
**Actual Changes:**
- Created `generated/solar_battery_v4/run_pipeline.py` (native hierarchy, NO ComponentCostEvaluator)
- Created `generated/solar_battery_v4/verify_pipeline.py` (same 7 ground truth values as v1/v2)
- Applied Bug 12 workaround to `pipeline.yaml` (permitting module outputs reduced to total_cost only)
**Results:**
- 5.1 Hybrid merge necessity: **NOT NEEDED** — native aggregation modules (20) replace ComponentCostEvaluator entirely
- 5.3 Input JSON: PASS — all `:>>` literals, multiplicity counts, and CalcDef defaults present across 3 JSON files
- 5.4 Pipeline execution: PASS — 36 modules executed in correct topological order, zero errors
- 5.6 Numerical verification: PASS — 7/7 values pass (total_capex=41205.0 exact, lcoe_per_mwh=288.68 within 1%)
- 5.7 Smart-regen: PASS — 36/36 AUTO_IMPLEMENTED preserved, 0 NotImplementedError. Smart-regen regenerates pipeline.yaml (overwriting Bug 12 workaround), confirming Bug 12 needs codegen fix.
- 5.8 Regression: PASS — core tests 48 passed, 1 skipped; generated tests 15/15 passed
**Issues:**
- **Bug 12 (NEW)**: Pipeline.yaml declares 5 outputs for PermittingCostCalc, but TEAx registry only registers 1 (`total_cost`). Cause: PermittingCostCalcOutput schema has `default=0.0` on material_cost, fab_cost, install_cost, idiot_index fields. TEAx's `create_registry()` excludes fields with defaults from output metadata. Workaround: 2 edits to pipeline.yaml (module outputs + exit_point). Root cause in codegen: pipeline generation should respect registry output registration, not SysML attribute count.
- Smart-regen overwrites Bug 12 workaround — need to re-apply after each smart-regen.
**Deviations:**
- Plan expected potential ComponentCostEvaluator fallback — not needed, native hierarchy pipeline works completely.
- Bug 12 is new (not in plan's bug matrix). Added as row to Phase 6 report.

### Phase 6 Completion
**Completed:** 2026-02-20
**Actual Changes:** Created `report.md` with full comparison report, per-bug matrix, hierarchy feature matrix, V1→V2→V4 comparison, and gate decision.
**Issues:** None
**Deviations:** Used V4 (not V3) throughout. Added Bug 12 to the per-bug matrix (not in original plan). Bug 10 documented as cosmetic (not in plan scope).

---

### **UPDATE: V5 Clean Regeneration (2026-02-20)**

**Purpose:** Regenerated both packages from scratch as `_v5` to confirm Bug 11/12 fixes are in the codegen itself — no manual workarounds needed.

**Commands run:**
```bash
uv run sysml-codegen generate --models models/tests/solar_battery --output generated/solar_battery_v5 --package-name solar_battery_v5 --overwrite --verbose
uv run sysml-codegen generate --models models/tests/e2e_attr_expr --output generated/e2e_attr_expr_v5 --package-name e2e_attr_expr_v5 --overwrite --verbose
```

**Results:**
- **Bug 11 FIXED:** `PermittingCostCalcOutput` schema no longer has `default=0.0` on fields. All fields use `Field(description=...)` — TEAx registers all 5 outputs correctly.
- **Bug 12 FIXED:** pipeline.yaml declares all 5 PermittingCostCalc outputs (`material_cost`, `fab_cost`, `install_cost`, `total_cost`, `idiot_index`). No workaround comments. ExitPoint exports all 5.
- **All 15 CalcDefs fully_compilable:** 0 manual implementations needed. IMPLEMENTATION_BACKLOG shows "0 functions to implement".
- **solar_battery_v5 pipeline:** ALL 7 VALUES PASS (LCOE = 288.68 $/MWh)
- **e2e_attr_expr_v5 pipeline:** ALL 16 VALUES PASS (all 12 patterns verified)
- **Zero workarounds required.** Both pipelines run from clean codegen output with no manual edits.

**Remaining informational warnings (not bugs):**
- 10 "Registry unresolved" warnings for binding-traced params — resolve via JSON entry points (working as designed)
- 3 unresolved aggregation inputs for `permitting.{raw_material_cost, fabrication_cost, installation_cost}` — fall back to `system_design` JSON defaulting to 0.0 (correct for soft-cost-only component)

**Revised workaround count:** V1 = ~23 edits + hybrid merge → V2 = 4 edits + hybrid merge → V4 = 2 edits (Bug 12) → **V5 = 0 edits, 0 workarounds**

---

**Status**: Complete
