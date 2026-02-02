# Implementation Plan: Codegen CalcUsage-Chain Spike

**Status:** Complete
**Created:** 2026-02-01
**Last Updated:** 2026-02-01

## Source Documents
- **Spec:** `.project/active/codegen-chain-spike/spec.md`
- **Design:** `.project/active/codegen-chain-spike/design.md` — See here for CalcDef table, SysML listings, evaluation checklist, and risk analysis

## Implementation Strategy

**Phasing Rationale:**
Three sequential phases matching the spike's natural flow: build model → run codegen → document findings. Each phase has a clear gate before the next can proceed.

**Overall Validation Approach:**
- Phase 1 gate: `syside check` exits 0
- Phase 2 gate: codegen exits 0 (or failure is documented)
- Phase 3 gate: go/no-go decision written with evidence

No automated test suite for this spike — validation is compilation checks and manual inspection of generated artifacts.

---

## Phase 1: Write & Compile the Chain Model

### Goal
Create the minimal 3-CalcDef chain model and confirm it compiles. This is prerequisite to everything else.

### Validation-First: Compilation Check
```bash
# Run this after writing each file to catch syntax errors early
uv run syside check models/tests/codegen_chain_spike/
```

### Changes Required

**See `design.md#component-1-minimal-chain-model` for:**
- CalcDef table (inputs, outputs, what each tests)
- Full SysML listing for `design.sysml`
- Diamond dependency diagram

#### 1. Library File
**File:** `models/tests/codegen_chain_spike/library.sysml` (NEW)
- [x] Create package `ChainSpikeLibrary`
- [x] Add `AreaCalc` CalcDef — 2 inputs (`length`, `width`), 1 output (`area`)
- [x] Add `CostCalc` CalcDef — 2 inputs (`area`, `rate`), 1 output (`total_cost`)
- [x] Add `SummaryCalc` CalcDef — 2 inputs (`area`, `cost`), 1 output (`cost_per_area`)

#### 2. Design File
**File:** `models/tests/codegen_chain_spike/design.sysml` (NEW)
- [x] Create package `ChainSpikeDesign` importing `ChainSpikeLibrary::*`
- [x] Add `spike_design` part with 3 entry-point attributes (`length`, `width`, `rate`)
- [x] Add `area_calc` CalcUsage — REFERENCE bindings only
- [x] Add `cost_calc` CalcUsage — one CHAIN binding (`area_calc.area`) + one REFERENCE
- [x] Add `summary` CalcUsage — two CHAIN bindings (`area_calc.area`, `cost_calc.total_cost`)
- [x] Use exact SysML from `design.md#designsysml-25-lines`

### Validation

**Automated:**
- [x] `uv run syside check models/tests/codegen_chain_spike/` exits 0

**Manual:**
- [x] Visually confirm 3 CalcDefs in library, 3 CalcUsages in design
- [x] Confirm chain bindings use dot notation (`area_calc.area`, `cost_calc.total_cost`)

**Phase 1 Gate:** Model compiles cleanly. Proceed to Phase 2.

---

## Phase 2: Run Codegen & Evaluate Output

### Goal
Execute sysml-codegen on the chain model and evaluate generated artifacts against the 4-stage checklist in the design doc. This is the core of the spike.

### Changes Required

**See `design.md#component-2-codegen-execution` for:** invocation command
**See `design.md#component-3-evaluation-checklist` for:** full 4-stage checklist

#### 1. Run Codegen
- [x] Execute codegen command from `design.md#component-2` (run from sysml-codegen directory)
- [x] Capture stdout/stderr (verbose mode)
- [x] Note exit code

#### 2. Evaluate Stage 1 — Extraction
- [x] Count discovered CalcUsages (expect 3)
- [x] Check binding types in verbose output (CHAIN vs REFERENCE)

#### 3. Evaluate Stage 2 — Graph Building
- [x] Check if output catalog has entries for `area_calc.area` and `cost_calc.total_cost`
- [x] Confirm chain bindings resolved to `MODULE_OUTPUT`
- [x] Confirm entry-point bindings resolved to `ENTRY_POINT`

#### 4. Evaluate Stage 3 — Pipeline YAML
- [x] Read `generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml`
- [x] Verify all 3 modules present
- [x] Verify topological order: `area_calc` → `cost_calc` → `summary`
- [x] Verify inter-module wiring (channel names per checklist)
- [x] Verify entry-point wiring for `length`, `width`, `rate`

#### 5. Evaluate Stage 4 — Generated Code Structure
- [x] Check `modules/` for 3 module wrappers
- [x] Check `handwritten/` for 3 implementation stencils
- [x] Check `__init__.py` for registry function

### Validation

**Automated:**
- [x] Codegen exit code 0 (or failure documented with error message)

**Manual:**
- [x] Pipeline YAML inspected against all Stage 3 checklist items
- [x] Generated module/stencil files exist and have correct structure

**If codegen fails:** Document the error, which pipeline stage it occurs in, and the error message. This is a valid spike outcome — proceed directly to Phase 3.

**Phase 2 Gate:** Codegen output fully evaluated (pass or fail). Proceed to Phase 3.

---

## Phase 3: Document Findings

### Goal
Write the go/no-go decision with supporting evidence from Phase 2. This is the spike deliverable.

### Changes Required

**See `design.md#component-4-findings-document` for:** findings template

#### 1. Write Spike Results
**File:** `.project/active/codegen-chain-spike/design.md` (APPEND results section)
- [x] Add `## Spike Results` section
- [x] Set go/no-go verdict: GO, NO-GO, or PARTIAL
- [x] List what works (passing checklist items from Phase 2)
- [x] List what doesn't work (failing items with error details)
- [x] For each failure: estimate fix scope (trivial / small / medium / large)
- [x] Write implications for Items 4-5

#### 2. Update Status
- [x] Update `design.md` status: Draft → Complete
- [x] Update `spec.md` status: Draft → Complete

### Validation

**Manual:**
- [x] Findings section has a clear verdict
- [x] Every checklist item from Phase 2 is accounted for (pass or fail)
- [x] Implications for Items 4-5 are actionable

**Phase 3 Gate:** Go/no-go decision documented. Spike complete.

---

## Environment Setup

**See CLAUDE.md for full environment rules** — use `uv run` for all Python/syside commands.

Codegen must be run from `/home/reid/1cfe/sysml-codegen/` (its own `pyproject.toml`).

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If syside rejects the model, compare syntax character-by-character against `models/tests/solar_battery/design.sysml:68-97`
- **Phase 2**: If codegen crashes, capture the full traceback — the stack trace itself tells us which pipeline stage failed and scopes the fix

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Created `models/tests/codegen_chain_spike/library.sysml` — 3 CalcDefs (AreaCalc, CostCalc, SummaryCalc)
- Created `models/tests/codegen_chain_spike/design.sysml` — 3 CalcUsages with chain bindings in spike_design part
- `uv run syside check` exits 0 on first attempt
**Issues:** None
**Deviations:** None — exact SysML from design.md used verbatim

### Phase 2 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Ran codegen from `/home/reid/1cfe/sysml-codegen/` with `--verbose`
- Exit code 0, all 3 CalcUsages extracted, computation graph built with 3 modules
- Generated output at `generated/codegen_chain_spike/` — pipeline YAML, 3 module wrappers, 3 stencils, registry, schemas, tests
**Issues:** None — all 4 evaluation stages passed
**Deviations:** None

### Phase 3 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Added `## Spike Results` section to `design.md` with GO verdict and full checklist evaluation
- Updated `design.md` status: Draft → Complete
- Updated `spec.md` status: Draft → Complete
- Updated `plan.md` status: Draft → Complete, all checkboxes marked
**Issues:** None
**Deviations:** None

---

**Status**: Complete
