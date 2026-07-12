# Validation Stack Gap Audit — Do We Catch "Unworkable SysML"?

**Date**: 2026-07-05
**Question** (user): the epic surfaced SysML patterns that parse cleanly but break evaluation or codegen (self-named binding recursion, `return`-style calcs, silently dropped constraints, etc.). Does the agentic-mbse 6-level validation stack catch these today? If not, where should each check live? "I thought we actually had tests for avoiding unworkable sysml code."

## Short answer

**No — the traps are not caught today.** What exists is real but narrower than the docs imply: Level 6 checks ADR-002 operator support and calc-def structure, Level 2 checks that bindings *exist* — but nothing catches evaluation-time traps (name-shadowing recursion) or extraction-contract traps (`return` style, missing part usage, constraint dropping). The rules exist only as prose in RAW_LEARNINGS.md as of this epic. The architecture is sound; the implementation is incomplete. One convention doc is actively wrong: the sysml-conventions skill's calc stencil shows `return` — the exact pattern that crashes codegen.

## Gap matrix

| # | Trap | Caught today? | Where it should go | Severity |
|---|------|---------------|--------------------|----------|
| 1 | Self-named binding (`in x = x;`) → infinite recursion at evaluation | **NO** | **Level 2** (`level2_structure.py`, extend `check_unbound_inputs`): flag bindings whose RHS resolves to the parameter being bound (owner = same calc usage) | FAIL |
| 2 | Calc `return` style → zero codegen outputs, template crash | **PARTIAL** — `level6_architecture.py:279-281` checks an output *exists*, not its style | **Level 6** (refine `check_calc_def_structure`): distinguish `ReturnParameterUsage` (✗) from out `AttributeUsage` (✓) | FAIL |
| 3 | `assert constraint` silently dropped by codegen (Phase 6 stub) | **NO** — Level 4 only counts constraints (`level4_constraints.py:113-114`) | **Level 6** (new check): inventory ConstraintUsages, WARN "not executable downstream — apply in harness"; *plus* a codegen-side warning (the silent drop is codegen's bug) | WARN |
| 4 | Part def with calcs but no concrete part usage → codegen emits nothing | **NO** | **Level 6** (new check): every calc-containing part def in designs/ needs ≥1 PartUsage typed by it | FAIL |
| 5 | Derived attr `x = calc.result` dropped at extraction (EXPOSE_PURE); value survives only as raw channel | **NO** (informational at best) | Primary: **sysml-codegen extraction layer** (preserve alias or warn); secondary: Level 6 INFO note in `check_design_attr_completeness` | INFO/WARN |
| 6 | Arithmetic envelope (`exp()`, conditionals → manual AI-pass impls) | **PARTIAL** — `adr002.py:25-26` has `SUPPORTED_OPERATORS` but the set is inconsistent (`**` excluded despite being in-envelope; no function-call detection) | **Level 6 ADR-002**: fix the operator set; detect FunctionInvocation nodes → WARN "will need manual Python impl (AI pass)" — a WARN, not FAIL, now that the AI pass exists | WARN |
| 7 | No loops in SysML (iterative formulas must be pre-solved to closed form — the Hawker DCF case) | **NO**, and not documented anywhere | **MODELING_GUIDE.md / ADR-002 prose** — a modeling rule, not a validator (nothing to detect: the language can't express it) | doc |

Two additions from WI-015 (same class, discovered after the audit started):
- **Quoted SysML names leak into generated Python** unsanitized → package can't import. Codegen-side fix (deterministic sanitizer exists as a WI-015 workaround, `exploration/ife_e2e/sanitize_names.py`).
- **Cross-part bindings drop to unwired entry points** — biggest MFE-relevant extraction gap; codegen-side.

## Why the belief didn't match

The Level 6 description ("expressions follow supported patterns", "calc definitions in the right places") accurately describes its *intent*, and ADR-002 operator checking plus calc-structure checking do exist and run. But the negative-fixture suite (`tests/fixtures/l6_negative/`) covers missing outputs, not output *style*; the regression baselines are built from `sample_models/` which contain none of these traps — so the suite passes whether or not the checks exist. The traps found this epic are exactly the kind that only surface when you *execute* the pipeline, which is what WI-013/014/015 did for the first time.

## Recommended next step

File as an agentic-mbse backlog item ("validation: unworkable-SysML trap checks", items 1–6 above + negative fixtures for each), and fix the sysml-conventions skill stencil (`return` → `out attribute`) immediately — that one is actively teaching agents the broken pattern.

**Full agent audit with file:line evidence**: retained in the epic progress log; source findings in `work/active/WI-014_*/findings.md` and `work/active/WI-015_*/findings.md`.
