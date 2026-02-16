# Implementation Plan: E2E Post-Codegen Validation (COST-PATTERN Epic)

**Status:** Draft
**Created:** 2026-02-10
**Last Updated:** 2026-02-13

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
- [x] **PASS**: 520 passed, 0 failed

#### 1.2 agentic-mbse tests
```bash
cd ~/1cfe/agentic-mbse && uv run python -m pytest -q
```
- [x] **PASS**: 886 passed, 1 skipped, 0 failed

#### 1.3 fusion-tea core tests
```bash
cd ~/1cfe/fusion-tea && uv run python -m pytest tests/ -q
```
- [x] **PASS**: 48 passed, 1 skipped, 0 failed

#### 1.4 fusion-tea generated package tests (existing v2)
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr_v2/tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/solar_battery/tests/ -q
```
- [x] **PASS**: e2e_attr_expr_v2: 4 passed
- [x] **PASS**: solar_battery: 27 passed, 1 failed (known: `test_all_seven_metrics` KeyError `capital_recovery_factor`)

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
  --overwrite --verbose 2>&1 | tee .project/active/e2e-post-codegen-validation/e2e_codegen_v3.log
```
- [x] Codegen completes without errors
- [x] Log saved for analysis

#### 2.2 Bug 1 — FORMULA entry point omission
Check that `design_params.py` contains all 7 FORMULA input parameters without manual addition.
```bash
# Inspect design_params.py for FORMULA params: quantity, unit_cost, length, width, height, cost_per_sqm, om_rate
grep -c "quantity\|unit_cost\|length\|width\|height\|cost_per_sqm\|om_rate" \
  generated/e2e_attr_expr_v3/schemas/design_params.py
```
- [x] **PASS**: All 7 FORMULA input parameters present (count = 9)

#### 2.3 Bug 2 — EXPOSE→CalcUsage wiring (the V2 partial fix)
Check if `financial.total_capex` is wired to MODULE_OUTPUT (component_cost.total_cost) not ENTRY_POINT (design_params).
```bash
# Check pipeline.yaml for total_capex wiring
grep -A5 "total_capex" generated/e2e_attr_expr_v3/pipelines/pipeline.yaml
```
- [x] **PASS**: `total_capex` wired to `E2EAttrExprDesign__e2e_plant__component_cost__total_cost` (MODULE_OUTPUT). Bug 2 FULLY FIXED by OutputRegistry redesign.

#### 2.4 Bug 3 — Float/float type mismatch
Check FORMULA module wrapper Input classes use `float` not `Float`.
```bash
grep -r "Float" generated/e2e_attr_expr_v3/modules/ --include="*.py" -l
```
- [x] **PASS**: 10 files contain `Float` but only in output types (ModuleBase[..., Float]) and imports. All Input class fields use lowercase `float`.

#### 2.5 Bug 6 — Special character sanitization
Not applicable to e2e_attr_expr (no `&` in part names). Verified in Phase 4.

#### 2.6 Bug 7 — Missing `__init__.py`
Check all generated Python package directories have `__init__.py`.
```bash
find generated/e2e_attr_expr_v3 -type d -exec sh -c \
  '[ -f "$1/__init__.py" ] || echo "MISSING: $1/__init__.py"' _ {} \;
```
- [x] **FAIL (broader scope)**: 6 top-level dirs missing __init__.py (handwritten/, modules/, schemas/, inputs/, pipelines/, tests/). Intermediate package dirs (e2eattrexprdesign/, e2e_plant/) have __init__.py — original Bug 7 scope FIXED. Same as V2.

#### 2.7 All implementations auto-generated
```bash
grep -r "AUTO_IMPLEMENTED" generated/e2e_attr_expr_v3/handwritten/ --include="*_impl.py" -l | wc -l
grep -r "NotImplementedError" generated/e2e_attr_expr_v3/handwritten/ --include="*_impl.py" -l | wc -l
```
- [x] **PASS**: 10 AUTO_IMPLEMENTED, 0 NotImplementedError

#### 2.8 IMPLEMENTATION_BACKLOG.md
```bash
grep "functions to implement" generated/e2e_attr_expr_v3/IMPLEMENTATION_BACKLOG.md
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
- [x] Created run_pipeline.py adapted from v2 with `e2e_attr_expr_v3` imports
- [x] No Bug 2 workaround needed — OutputRegistry fix confirmed in Phase 2

#### 3.2 Execute pipeline
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python generated/e2e_attr_expr_v3/run_pipeline.py
```
- [x] Pipeline executes without errors — zero workarounds applied
- [x] Bug 4 verified: multi-output float channels serialize to JSON (no manual writes needed)

#### 3.3 Create verify_pipeline.py for v3
Adapt from v2 — update package name in JSON filename patterns.

**File:** `generated/e2e_attr_expr_v3/verify_pipeline.py` (NEW — adapt from `generated/e2e_attr_expr_v2/verify_pipeline.py`)
- [x] Created verify_pipeline.py — channel naming identical to v2, no changes needed
- [x] Output directory prefix: `e2e-attr-expr-v3-results-*`

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
PYTHONPATH=generated uv run python -m pytest generated/e2e_attr_expr_v3/tests/ -v
```
- [x] **PASS**: 4 passed (ComponentCostCalc, AnnualizedCostCalc, EnergyCalc, SimpleLCOECalc)

#### 3.6 Regression check
```bash
uv run python -m pytest tests/ -q
```
- [x] **PASS**: 48 passed, 1 skipped (unchanged from Phase 1)

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
  --overwrite --verbose 2>&1 | tee .project/active/e2e-post-codegen-validation/solar_codegen_v3.log
```
- [x] Codegen completes without errors (36 modules in computation graph, 15 CalcDefs fully compilable)
- [x] Log saved for analysis

#### 4.2 Template CalcUsage Instantiation (Item 2 feature)
Verify 9 leaf-part cost modules are generated with hierarchy-aware names.

```bash
# Check for leaf-part cost model modules in pipeline.yaml or module directories
grep -i "cost_model" generated/solar_battery_v3/pipelines/pipeline.yaml
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

**Expected design parameter resolutions** (from `design.sysml` `:>>` overrides):
- [x] `pv_module.wattage` — field exists in system_design.py schema
- [x] `pv_module.efficiency` — field exists in system_design.py schema
- [x] `inverter.power_rating` — field exists in system_design.py schema
- [x] `array_bos.string_count` — field exists in system_design.py schema
- [x] `array_bos.panel_count` — field exists in system_design.py schema
- [x] `battery_pack.capacity_kwh` — field exists in system_design.py schema
- [x] `battery_pack.chemistry_factor` — field exists in system_design.py schema
- [x] `hybrid_inverter.power_rating` — field exists in system_design.py schema
- [x] `battery_bos.pack_count` — field exists in system_design.py schema
- [x] `racking.panel_count` — field exists in system_design.py schema
- [x] `racking.tilt_angle` — field exists in system_design.py schema
- [x] `electrical_panel.circuit_count` — field exists in system_design.py schema
- [x] `permitting.system_capacity_kw` — field exists in system_design.py schema

**FINDING**: All 13 `:>>` override fields are present in the SystemDesign schema. However, the resolved LITERAL VALUES (400.0, 0.21, etc.) are NOT populated as defaults — the fields are required without defaults. The system_design.json only has 3 entries (multiplicity counts). The JSON template will need manual population for pipeline execution.

#### 4.4 Aggregation Module Generation (Items 3+4 feature)
Verify 4 assembly aggregation modules are generated with `# source: aggregation` markers.

```bash
grep -i "aggregation\|capital_cost\|raw_material_cost\|fabrication_cost\|installation_cost" \
  generated/solar_battery_v3/pipelines/pipeline.yaml | head -30
```

**Expected 4 aggregation assemblies** (each may have multiple cost attributes):
- [x] `solar_array__capital_cost` (with `module_count` and `inverter_count` multiplier entry points)
- [x] `battery_system__capital_cost` (with `pack_count` multiplier entry point)
- [x] `site_infra__capital_cost` (singletons only, no multipliers)
- [x] `solar_battery_plant__capital_cost` (top-level aggregation)

**FINDING**: Actually 20 aggregation modules generated (5 cost attributes × 4 assemblies = 20), not 4. Each assembly has: capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index. All 20 have `# source: aggregation` markers. All 20 have auto-generated implementations.

#### 4.5 Multiplicity Entry Points (Item 3 feature)
Verify multiplicity counts appear as DESIGN_ATTRIBUTE entry points.

```bash
grep -E "module_count|inverter_count|pack_count" \
  generated/solar_battery_v3/schemas/design_params.py
```
- [x] `module_count` present (default 20) — in system_design.json AND system_design.py schema
- [x] `inverter_count` present (default 4) — in system_design.json AND system_design.py schema
- [x] `pack_count` present (default 8) — in system_design.json AND system_design.py schema

#### 4.6 Topological Ordering
Verify pipeline YAML shows correct dependency order: leaf cost calcs → aggregation → system-level calcs.

```bash
# Extract module order from pipeline.yaml
grep "^  - name:" generated/solar_battery_v3/pipelines/pipeline.yaml
```
- [x] Leaf cost_model modules appear before aggregation modules
- [x] Sub-assembly aggregation now precedes plant-level aggregation, which precedes system-level CalcUsages. Ordering is topologically correct.
- [x] `lcoe` appears last (depends on all upstream)

#### 4.7 System-Level CalcUsage Wiring
Verify `annualized_financial.total_capex` wires to aggregation module output (not entry point).

```bash
grep -A10 "annualized_financial\|total_capex" generated/solar_battery_v3/pipelines/pipeline.yaml
```
- [x] `total_capex` input wires to `SolarBatteryDesign__solar_battery_plant__capital_cost__capital_cost.root` (MODULE_OUTPUT from plant-level aggregation). **Bug 2 FULLY FIXED for system-level CalcUsages.**

#### 4.8 Bug 6 — Special character sanitization
```bash
grep -r "Racking" generated/solar_battery_v3/ --include="*.py" -l | head -5
# Verify no & in Python identifiers
grep -r "&" generated/solar_battery_v3/ --include="*.py" | grep -v "#\|doc\|comment\|string" | head -5
```
- [x] **PASS**: No `&` characters found in Python identifiers. Part names use `site_infra` not `Racking_&_Mounting`.

#### 4.9 Bug 7 — `__init__.py` completeness
```bash
find generated/solar_battery_v3 -type d -exec sh -c \
  '[ -f "$1/__init__.py" ] || echo "MISSING: $1/__init__.py"' _ {} \;
```
- [x] **FAIL (broader scope)**: 6 top-level dirs missing `__init__.py` (handwritten/, modules/, schemas/, inputs/, pipelines/, tests/). All intermediate package dirs HAVE `__init__.py`. Same broader-scope issue as e2e_attr_expr_v3.

#### 4.10 All implementations auto-generated
```bash
grep -rl "AUTO_IMPLEMENTED" generated/solar_battery_v3/handwritten/ --include="*_impl.py" | wc -l
grep -rl "NotImplementedError" generated/solar_battery_v3/handwritten/ --include="*_impl.py" | wc -l
cat generated/solar_battery_v3/IMPLEMENTATION_BACKLOG.md | head -5
```
- [x] **PASS**: 36 `AUTO_IMPLEMENTED` (15 CalcDef + 1 computed attr + 20 aggregation), 0 `NotImplementedError`, BACKLOG shows "0 functions to implement"

#### 4.11 Compare v3 vs v2 module counts
```bash
echo "=== v2 modules ===" && ls generated/solar_battery_v2/modules/ 2>/dev/null | wc -l
echo "=== v3 modules ===" && ls generated/solar_battery_v3/modules/ 2>/dev/null | wc -l
echo "=== v2 handwritten ===" && find generated/solar_battery_v2/handwritten/ -name "*_impl.py" 2>/dev/null | wc -l
echo "=== v3 handwritten ===" && find generated/solar_battery_v3/handwritten/ -name "*_impl.py" 2>/dev/null | wc -l
```
- [x] **PASS**: v2 had 4 module dirs and 16 handwritten _impl.py files. v3 has 36 module .py files (15 CalcDef + 1 computed attr + 20 aggregation) and 36 handwritten _impl.py files. Significant increase from hierarchy-aware codegen.

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

**File:** `generated/solar_battery_v3/run_pipeline.py` (NEW)
- [ ] If native hierarchy: create simple pipeline runner (like e2e_attr_expr_v2 pattern)
- [ ] If hybrid needed: adapt from v2, documenting what manual merge is still required

#### 5.3 Create design_params.json for v3
The pipeline needs input parameter values. These should be auto-generated by codegen, but may need verification.

```bash
cat generated/solar_battery_v3/inputs/design_params.json | python3 -m json.tool | head -30
```
- [ ] All `:>>` literal values present (wattage=400, efficiency=0.21, etc.)
- [ ] All multiplicity counts present (module_count=20, inverter_count=4, pack_count=8)
- [ ] All CalcDef defaults present (cost_per_watt=1.07, fab_factor=0.45, etc.)

#### 5.4 Execute pipeline
```bash
cd ~/1cfe/fusion-tea
PYTHONPATH=generated uv run python generated/solar_battery_v3/run_pipeline.py
```
- [ ] Pipeline executes without errors
- [ ] All modules execute in correct order

#### 5.5 Create verify_pipeline.py for v3

**File:** `generated/solar_battery_v3/verify_pipeline.py` (NEW — adapt from v2)
- [ ] Same 7 expected values and tolerances as v1/v2
- [ ] Update output directory prefix if naming changed

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

- [ ] **PASS/FAIL**: 7/7 values pass

#### 5.7 Bug 5 — Smart-regen stub upgrade (targeted test)
Run codegen again on the v3 directory with `--smart-regen`:
```bash
uv run sysml-codegen generate \
  --models models/tests/solar_battery/ \
  --output generated/solar_battery_v3 \
  --package-name solar_battery_v3 \
  --smart-regen --preserve-handwritten --verbose 2>&1 | tail -20
```
- [ ] All `_impl.py` files remain `AUTO_IMPLEMENTED` (not downgraded to stubs)
- [ ] No regression in pipeline execution after smart-regen

#### 5.8 Regression check
```bash
uv run python -m pytest tests/ -q
PYTHONPATH=generated uv run python -m pytest generated/solar_battery_v3/tests/ -v
```
- [ ] Core tests: 48 passed, 1 skipped
- [ ] Generated tests: all pass

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

**File:** `.project/active/e2e-post-codegen-validation/report.md` (NEW)

Report structure:
- [ ] Executive Summary (1 paragraph: pass/fail, workaround count, key findings)
- [ ] Phase 1: Regression Baseline (test counts, any issues)
- [ ] Phase 2-3: E2E Attr Expr Results (16/16 values, per-bug matrix)
- [ ] Phase 4-5: Solar Battery Results (7/7 values, hierarchy feature matrix)
- [ ] Per-Bug Fix Verification Matrix (V1→V2→V3 for all 7 bugs)
- [ ] Hierarchy Feature Verification Matrix (9 leaf modules, 4 aggregation, multiplicity, `:>>` resolution)
- [ ] V1 vs V2 vs V3 Comparison Table (workaround counts, module counts, test counts)
- [ ] New Issues Discovered (if any)
- [ ] Gate Decision: PASS/FAIL for COST-PATTERN Item 5

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
- **PASS** if: all 16 e2e_attr_expr values pass, all 7 solar_battery values pass, all 7 bugs fully resolved (no partials), hierarchy features generate correctly
- **PASS with conditions** if: numerical values pass but minor structural issues remain (e.g., Bug 7 broader scope still partial)
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
**Completed:** 2026-02-13
**Actual Changes:** No changes — validation only (test execution)
**Results:**
- [x] 1.1 sysml-codegen: 520 passed, 0 failed (up from 454 baseline — Items 1-4 added tests)
- [x] 1.2 agentic-mbse: 886 passed, 1 skipped, 0 failed
- [x] 1.3 fusion-tea core: 48 passed, 1 skipped, 0 failed
- [x] 1.4 e2e_attr_expr_v2: 4 passed
- [x] 1.4 solar_battery: 27 passed, 1 failed (known: `test_all_seven_metrics` KeyError `capital_recovery_factor`)
**Issues:** None — all match expected baselines
**Deviations:** sysml-codegen test count higher than plan baseline (520 vs 454) due to Items 1-4 test additions. This is expected and positive.

### Phase 2 Completion (Re-run after OutputRegistry redesign)
**Completed:** 2026-02-13
**Actual Changes:** Re-generated e2e_attr_expr_v3 with sysml-codegen OutputRegistry (commits 8373175..973d2bc). No source code changes.
**Phase 1 re-check:** sysml-codegen 641 passed (up from 520), agentic-mbse 886 passed, fusion-tea 48 passed.
**Results:** 6 PASS, 1 FAIL (broader scope only):
- Bug 1 (FORMULA entry points): PASS (count=9)
- Bug 2 (EXPOSE→CalcUsage): **PASS** — total_capex now wires to `E2EAttrExprDesign__e2e_plant__component_cost__total_cost` (MODULE_OUTPUT). OutputRegistry fix confirmed!
- Bug 3 (Float/float): PASS — All Input class fields use lowercase `float`
- Bug 7 (__init__.py): FAIL — broader scope, 6 top-level dirs missing (handwritten/, modules/, schemas/, inputs/, pipelines/, tests/). Intermediate package dirs fine.
- Auto-implementations: PASS — 10/10 AUTO_IMPLEMENTED, 0 NotImplementedError
- IMPLEMENTATION_BACKLOG: PASS — 0 functions to implement
**Issues:** Bug 7 broader scope remains. Bug 2 is now FULLY FIXED.
**Deviations:** Bug 2 changed from FAIL→PASS compared to first Phase 2 run. This is the key improvement from the OutputRegistry redesign.

### Phase 3 Completion
**Completed:** 2026-02-13
**Actual Changes:** Created run_pipeline.py and verify_pipeline.py for v3. Pipeline executed, all 16 values verified.
**Results:**
- Pipeline: executed without errors, zero workarounds
- Numerical: 16/16 PASS (all ground truth values match v1/v2 baselines)
- Generated tests: 4/4 PASS
- Regression: 48 passed, 1 skipped (unchanged)
- Bug 2: FULLY FIXED — total_capex correctly wired via OutputRegistry, no pipeline.yaml rewire needed
- Bug 4: PASS — all float channels serialize to JSON via ExitPoint
**Workaround Count (v3 vs v2):**
- v2: 1 workaround (Bug 2 EXPOSE→CalcUsage rewire) + 2 __init__.py additions
- v3: **0 workarounds** (Bug 2 fixed by OutputRegistry)
**Issues:** None
**Deviations:** Plan anticipated possible Bug 2 workaround in 3.1 — not needed.

### Phase 4 Completion (Rerun #3 — after expanded wiring fixes)
**Completed:** 2026-02-15
**Actual Changes:** Regenerated solar_battery_v3 after sysml-codegen expanded scoped registry wiring fixes. No fusion-tea source code changes.

**Codegen Log Improvements (vs prior runs):**
- OutputRegistry: 293 total keys (same)
- NEW resolved via scoped registry: inverter (4), allocation_model (1), racking (4), permitting.capital_cost (1), ALL plant-level inputs (12), ALL idiot_index assembly inputs (6), ALL battery_system singletons (8)
- NEW explicit warnings for 3 unresolved: `permitting.raw_material_cost`, `permitting.fabrication_cost`, `permitting.installation_cost` in site_infra

**Results Summary:**
- [x] 4.1 Codegen: PASS — 36 modules, 15 CalcDefs fully compilable, 20 aggregation modules
- [x] 4.2 Template instantiation: PASS — All 9 leaf-part + 1 allocation module with hierarchy names
- [x] 4.3 `:>>` resolution: PARTIAL — 13 fields in SystemDesign schema, literal values NOT populated as defaults or in JSON (system_design.json has 3 multiplicity counts only)
- [x] 4.4 Aggregation modules: PASS — 20 generated (5 cost attrs × 4 assemblies)
- [x] 4.5 Multiplicity entry points: PASS — module_count=20, inverter_count=4, pack_count=8 in system_design.json
- [x] 4.6 Topological ordering: **PASS** — sub-assembly aggregation now precedes plant-level, which precedes system-level CalcUsages. lcoe last.
- [x] 4.7 System CalcUsage wiring: PASS — total_capex → capital_cost.root (MODULE_OUTPUT). Bug 2 FIXED.
- [x] 4.8 Bug 6: PASS — 0 `&` in identifiers
- [x] 4.9 Bug 7: FAIL (broader scope) — 6 top-level dirs missing `__init__.py`
- [x] 4.10 Auto-implementations: PASS — 36/36 AUTO_IMPLEMENTED, 0 NotImplementedError, 0 BACKLOG
- [x] 4.11 Module counts: PASS — v3 (36 modules, 36 impls) >> v2 (4 module dirs, 16 impls)

**Aggregation Wiring Progress (run 1 → run 2 → run 3):**
- Wired to MODULE_OUTPUT: 8 → 12 → **54**
- Unwired: 62 → 58 → **16**

**Remaining Unwired (16) by Category:**
- **Multiplicity counts as raw channels** (12): module_count ×4, inverter_count ×4, pack_count ×4 — values exist in system_design.json but pipeline references use raw channel names instead of `system_design.` prefix
- **Permitting sub-cost wiring** (3): permitting.raw_material_cost, .fabrication_cost, .installation_cost — scoped registry tried but failed to resolve (tried 'solar_battery_plant.site_infra.permitting.raw_material_cost'). Note: permitting.capital_cost DID resolve. Likely a naming mismatch between aggregation term names and CalcDef output names.
- **misc_hardware_cost** (1): EXPOSE_PURE attribute that references `allocation_model.total_allocation` — codegen can't resolve the cross-CalcUsage reference

**Issues:**
1. OutputRegistry key collisions (15 warnings) — expected with hierarchy
2. 10 "Registry unresolved" warnings for system-level CalcUsage params
3. EXPOSE_PURE `misc_hardware_cost` unresolved
4. 3 permitting singleton terms unresolved → ENTRY_POINT

**Deviations:**
- Plan expected 4 aggregation modules; actual is 20
- Topological ordering now PASSES (was PARTIAL in runs 1-2)
- `:>>` literal values extracted (13 design overrides) but not written to JSON templates

### Phase 4 Completion (Rerun #4 — after Bug 7 fix, aggregation wiring fix, literal propagation fix)
**Completed:** 2026-02-16
**Actual Changes:** Regenerated solar_battery_v3 after 3 sysml-codegen fixes:
- `b626c59` Fix literal value propagation: carry `:>>` redefinition values into JSON templates
- `b9702b0` Fix Bug 7 broader scope: generate `__init__.py` in all top-level output subdirectories
- `20b720e` Fix aggregation wiring: FCE/OE dispatch ordering + LocalTerm sibling resolution
No fusion-tea source code changes.

**Phase 1 re-check:** sysml-codegen 664 passed (up from 641), fusion-tea 48 passed, 1 skipped.

**Results Summary:**
- [x] 4.1 Codegen: PASS — 36 modules, 15 CalcDefs fully compilable, 20 aggregation modules
- [x] 4.2 Template instantiation: PASS — All 9 leaf-part + 1 allocation module with hierarchy names
- [x] 4.3 `:>>` resolution: **PASS** — 13 fields in SystemDesign schema, ALL WITH literal defaults (wattage=400.0, efficiency=0.21, etc.) AND 16 values in system_design.json (13 design + 3 multiplicity)
- [x] 4.4 Aggregation modules: PASS — 20 generated (5 cost attrs × 4 assemblies)
- [x] 4.5 Multiplicity entry points: PASS — module_count=20, inverter_count=4, pack_count=8 in system_design.json
- [x] 4.6 Topological ordering: PASS — leaf → sub-assembly aggregation → plant-level → system-level → lcoe
- [x] 4.7 System CalcUsage wiring: PASS — total_capex → capital_cost.root (MODULE_OUTPUT). Bug 2 FIXED.
- [x] 4.8 Bug 6: PASS — 0 `&` in identifiers
- [x] 4.9 Bug 7: **PASS** — 0 directories missing `__init__.py`. Bug 7 broader scope FIXED.
- [x] 4.10 Auto-implementations: PASS — 36/36 AUTO_IMPLEMENTED, 0 NotImplementedError, 0 BACKLOG
- [x] 4.11 Module counts: PASS — v3 (36 modules, 36 impls) >> v2 (4 module dirs, 16 impls)

**Aggregation Wiring Progress (run 1 → run 2 → run 3 → run 4):**
- Total pipeline inputs: 135
- Wired to MODULE_OUTPUT: 8 → 12 → 54 → **92** (68.1%)
- Wired to design_params: 11 (8.1%)
- Wired to library_params: 32 (23.7%)
- Unwired (ENTRY_POINT): 62 → 58 → 16 → **4**

**Remaining Unwired (4) by Category:**
- **Permitting sub-cost wiring** (3): `permitting.raw_material_cost`, `.fabrication_cost`, `.installation_cost` in site_infra aggregation — scoped registry tried but failed to resolve. The CalcDef outputs `material_cost`/`fab_cost`/`install_cost` but aggregation terms reference `raw_material_cost`/`fabrication_cost`/`installation_cost` (naming mismatch). Note: `permitting.capital_cost` DID resolve correctly.
- **misc_hardware_cost** (1): EXPOSE_PURE attribute referencing `allocation_model.total_allocation` — codegen can't resolve cross-CalcUsage reference

**Key Improvements vs Rerun #3:**
1. Bug 7 broader scope: FAIL → **PASS** (6 missing `__init__.py` → 0)
2. `:>>` literal propagation: PARTIAL → **PASS** (3 JSON entries → 16 JSON entries, 0 defaults → 13 defaults)
3. Multiplicity count wiring: raw channel names → fully-qualified channel names with `int` type
4. Unwired inputs: 16 → **4** (75% reduction)

**Issues:**
1. OutputRegistry key collisions (15 warnings) — expected with hierarchy, same as Rerun #3
2. 10 "Registry unresolved" warnings for system-level CalcUsage params — same as Rerun #3
3. EXPOSE_PURE `misc_hardware_cost` unresolved — same as Rerun #3
4. 3 permitting singleton terms unresolved → ENTRY_POINT — same as Rerun #3
5. 4 required SystemDesign fields without defaults or JSON values: `misc_hardware_cost`, `permitting_raw_material_cost`, `permitting_fabrication_cost`, `permitting_installation_cost` — will need values for Phase 5 pipeline execution

**Deviations:** None — all improvements as expected from the 3 targeted bug fixes.

### Phase 4 Completion (Rerun #5 — after EXPOSE_PURE fix + permitting default values)
**Completed:** 2026-02-16
**Actual Changes:** Regenerated solar_battery_v3 after sysml-codegen uncommitted fixes targeting the final 4 unwired inputs:
- `extraction/data_models.py`, `extraction/hierarchy_resolver.py` — EXPOSE_PURE resolution for misc_hardware_cost
- `resolution/graph_builder.py` — permitting sub-cost default value propagation
- `generation/initialization.py` — default value emission for unresolved ENTRY_POINTs
No fusion-tea source code changes.

**Phase 1 re-check:** sysml-codegen 667 passed (up from 664), fusion-tea 48 passed, 1 skipped.

**Results Summary:**
- [x] 4.1 Codegen: PASS — 36 modules, 15 CalcDefs fully compilable, 20 aggregation modules
- [x] 4.2 Template instantiation: PASS — All 9 leaf-part + 1 allocation module with hierarchy names
- [x] 4.3 `:>>` resolution: PASS — 13 design override defaults + 19 system_design.json values (13 design + 3 multiplicity + 3 permitting defaults)
- [x] 4.4 Aggregation modules: PASS — 20 generated (5 cost attrs × 4 assemblies)
- [x] 4.5 Multiplicity entry points: PASS — module_count=20, inverter_count=4, pack_count=8
- [x] 4.6 Topological ordering: PASS — leaf → sub-assembly aggregation → plant-level → system-level → lcoe
- [x] 4.7 System CalcUsage wiring: PASS — total_capex → capital_cost.root (MODULE_OUTPUT)
- [x] 4.8 Bug 6: PASS — 0 `&` in identifiers
- [x] 4.9 Bug 7: PASS — 0 directories missing `__init__.py`
- [x] 4.10 Auto-implementations: PASS — 36/36 AUTO_IMPLEMENTED, 0 NotImplementedError, 0 BACKLOG
- [x] 4.11 Module counts: PASS — v3 (36 modules, 36 impls)

**Aggregation Wiring Progress (run 1 → run 2 → run 3 → run 4 → run 5):**
- Total pipeline inputs: 135
- Wired to MODULE_OUTPUT: 8 → 12 → 54 → 92 → **93** (68.9%)
- Wired to design_params: 11 (8.1%)
- Wired to library_params: 32 (23.7%)
- Unwired (ENTRY_POINT with defaults): 62 → 58 → 16 → 4 → **3**

**Key Improvements vs Rerun #4:**
1. **misc_hardware_cost: FIXED** — now wired to `allocation_model.total_allocation` (MODULE_OUTPUT). EXPOSE_PURE cross-CalcUsage reference resolved.
2. **3 permitting sub-costs: IMPROVED** — still ENTRY_POINT but now have `default=0.0` in SystemDesign schema AND system_design.json. Pipeline can execute without manual JSON edits.
3. **SystemDesign schema**: `misc_hardware_cost` field REMOVED (no longer needed — wired to MODULE_OUTPUT). 3 permitting fields remain with defaults.

**Remaining 3 ENTRY_POINTs (with defaults):**
- `permitting_raw_material_cost` = 0.0 (ENTRY_POINT in site_infra raw_material_cost aggregation)
- `permitting_fabrication_cost` = 0.0 (ENTRY_POINT in site_infra fabrication_cost aggregation)
- `permitting_installation_cost` = 0.0 (ENTRY_POINT in site_infra installation_cost aggregation)

These represent a naming mismatch: the aggregation terms use `permitting.raw_material_cost` but the CalcDef outputs `material_cost`. The 0.0 defaults are numerically correct for fab_cost and install_cost (permitting has no fabrication/installation component), but raw_material_cost=0.0 means permitting's material cost contribution is missing from the site_infra raw_material_cost aggregation. This does NOT affect capital_cost or LCOE (which use total_cost via `permitting.capital_cost`, correctly wired to MODULE_OUTPUT).

**Issues:**
1. OutputRegistry key collisions (15 warnings) — expected with hierarchy
2. 10 "Registry unresolved" warnings for system-level CalcUsage params — design_params entries, expected
3. EXPOSE_PURE `misc_hardware_cost` warning still emitted during analysis but now correctly wired in graph builder

**Deviations:** None.

### Phase 5 Completion
**Completed:** [Timestamp]
**Actual Changes:** [What actually changed]
**Issues:** [Problems encountered and solutions]
**Deviations:** [How this differed from plan and why]

### Phase 6 Completion
**Completed:** [Timestamp]
**Actual Changes:** [What actually changed]
**Issues:** [Problems encountered and solutions]
**Deviations:** [How this differed from plan and why]

---

**Status**: Draft → In Progress → Complete
