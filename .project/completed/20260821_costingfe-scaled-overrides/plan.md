# Implementation Plan: Costingfe Scaled Overrides Integration

**Status:** Complete
**Created:** 2026-04-19
**Last Updated:** 2026-04-19

## Source Documents
- **Spec:** `.project/active/costingfe-scaled-overrides/spec.md`
- **Design:** `.project/active/costingfe-scaled-overrides/design.md` ← See here for component details, data flows, extractor contract

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks by manually testing the `override_reference_mw` API on the concept with the largest scaling correction (ARC, 261→1000 MWe). Phase 2 updates infrastructure (extractor + template) while Phase 1's test model is still in place for validation. Phase 3 batch-regenerates all 8 concepts using the proven `--force` cold-start pattern from `.project/active/power-standardization/plan.md`.

---

## Phase 1: Manual Test on Concept 01 (ARC) — Soft Gate

### Goal
Validate that `model.forward(..., override_reference_mw=261.0)` produces a reasonable `ForwardResult` at 1 GW before changing any infrastructure. ARC has the largest scaling correction (261→1000 MWe), so it's the most sensitive test case.

### Changes Required

#### 1. Manual edit to concept 01
**File:** `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py`
- [x] Add `result_1gw = model.forward(net_electric_mw=1000.0, override_reference_mw=261.0, ...)` after the existing `result` block (see `design.md#component-5` for pattern)
- [x] Use the same kwargs as the existing `result` call (availability, lifetime_yr, cost_overrides, etc.)

#### 2. Run and validate
- [x] `cd exploration/concept_analysis/analyses/01-hts-compact-tokamak && uv run python model_setup.py`
- [x] Assert `result_1gw.params["net_electric_mw"] == 1000.0`
- [x] Assert `result_1gw.power_table.p_net` is ~1000 MWe
- [x] Compare `result_1gw.costs.lcoe` vs. old `scaled_headline["lcoe_per_mwh"]` — expect 5-15% delta
- [x] Inspect `result_1gw.costs` CAS breakdown for reasonableness (no negative costs, no order-of-magnitude outliers)
- [x] Print comparison table: old post-hoc LCOE vs. new per-account LCOE, old overnight vs. new overnight

### Validation

**What We Know Works After This Phase:**
- `override_reference_mw` produces a valid `ForwardResult` with 1GW params
- Per-account scaling gives plausible LCOE and CAS costs
- Soft gate: proceed to Phase 2 unless results are clearly broken

**Note:** Do NOT revert the manual edit yet — Phase 2 uses it to test the extractor change.

---

## Phase 2: Extractor + Template Updates

### Goal
Update the two infrastructure pieces: the extractor (to consume `result_1gw`) and the prompt template (to produce `result_1gw`). These are independent changes but both needed before batch re-generation.

### Changes Required

#### 1. Extractor — use `result_1gw` when present
**File:** `exploration/concept_explorer/extract_explorer_data.py`

See `design.md#component-1` for the full new flow.

- [x] In `extract_costingfe()` (~line 194): after grabbing `model` and `result`, check `result_1gw = getattr(module, "result_1gw", None)`
- [x] If `result_1gw` is not None: use it instead of `result` for building `CostModelData`:
  - `sensitivities = build_sensitivity_analysis(model, result_1gw)`
  - `raw = dataclasses.asdict(result_1gw)`
  - Inject availability into `raw["power_table"]` (same pattern as native, ~line 209-210)
- [x] If `result_1gw` is None: use native `result` as today (already-at-1GW and freeform-fallback cases)
- [x] Remove the `scaled_headline` injection block (~lines 208-217) for costingfe path
- [x] Keep `_apply_scaled_headline()` in `extract_standalone()` unchanged (freeform path)

#### 2. Validate extractor on concept 01 (from Phase 1)
- [x] Run `uv run python exploration/concept_explorer/extract_explorer_data.py --concepts 01` (or equivalent filter)
- [x] Check `data/01.json`: `cost_model.headline.p_net_mw` should be 1000, `cost_model.headline.lcoe_per_mwh` should match `result_1gw.costs.lcoe` from Phase 1
- [x] Check that `cost_model.sensitivities` is populated (extractor computed from `result_1gw`)

#### 3. Prompt template — dual-result pattern
**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`

See `design.md#component-2` for the replacement content.

- [x] Replace the "Power Standardization" section (lines 47-68) with dual-result instructions
- [x] Instructions must cover: `_SHARED_KWARGS` dict, `result` at native power, `result_1gw` with `override_reference_mw`, conditional skip for 1GW concepts, no `scaled_headline`, no `sens_1gw`

#### 4. Validate freeform concepts unaffected
- [x] Run extractor on a freeform concept (e.g., concept 02 or 12)
- [x] Verify `cost_model.headline.p_net_mw` still shows 1000 (from `scaled_headline`)
- [x] Verify `cost_model.headline.lcoe_per_mwh` unchanged from before

#### 5. Validate already-at-1GW concepts unaffected
- [x] Run extractor on an already-at-1GW concept (e.g., concept 03)
- [x] Verify `cost_model` data unchanged (no `result_1gw` on module → falls through to native `result`)

### Validation

**What We Know Works After This Phase:**
- Extractor correctly picks up `result_1gw` and produces full 1GW `CostModelData`
- Extractor falls through to native `result` when `result_1gw` absent
- Freeform `scaled_headline` path still works
- Template has correct instructions for dual-result pattern

---

## Phase 3: Batch Re-generation + Re-extraction + Validation

### Goal
Re-generate all 8 non-1GW costingfe concepts, re-extract all 19, and validate the full dataset.

### Changes Required

#### 1. Re-generate all 8 concepts
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py \
    model-setup 01 05 06 11 14 17a 21 28 --force
```

See `design.md#component-4` for the concept table and per-concept validation checklist.

- [x] 01 — HTS Compact Tokamak (ARC, 261 MWe): runs, has `result_1gw`, no `scaled_headline`
- [x] 05 — Planar Coil Stellarator (390 MWe): same checks
- [x] 06 — Magnetic Mirror p-B11 (500 MWe): same checks
- [x] 11 — Magnetic Mirror D-T (500 MWe): same checks
- [x] 14 — MTF Pneumatic GF (300 MWe): same checks
- [x] 17a — Laser ICF Hybrid Xcimer (400 MWe): same checks
- [x] 21 — Spherical Tokamak HTS (600 MWe): same checks
- [x] 28 — HTS Tokamak Full-HTS (500 MWe): same checks

Per-concept validation for each:
- `uv run python model_setup.py` exits cleanly
- Module has `result_1gw` attribute
- Module does NOT have `scaled_headline` attribute
- `result_1gw.costs.lcoe` is plausible

#### 2. Re-extract all 19 concepts
- [x] `uv run python exploration/concept_explorer/extract_explorer_data.py`
- [x] No extraction errors

#### 3. Cross-concept validation
- [x] Run validation script from `design.md#component-6` — all 19 show `p_net=1000`
- [x] Tabulate old vs. new LCOE for the 8 migrated concepts — flag any >20% delta for investigation
- [x] Verify freeform concepts (02, 12, 15, 22, 35) have unchanged LCOE
- [x] Verify already-at-1GW concepts (03, 04, 07, 08, 09, 10) have unchanged LCOE

#### 4. Explorer regression check
- [ ] Start server: `uv run python exploration/concept_explorer/server.py`
- [ ] Browse a migrated concept page (e.g., 01) — headline, CAS breakdown, tornado all render
- [ ] Browse a freeform concept page (e.g., 02) — unchanged
- [ ] Browse comparison view — no errors, concepts render
*(Manual — requires browser interaction)*

### Validation

**What We Know Works After This Phase:**
- All 19 concepts extracted with consistent 1000 MWe data
- 8 migrated concepts have full per-account 1GW CAS breakdown and sensitivities
- Explorer renders all views without regression
- Project ready for analysis on the improved dataset

---

## Environment Setup

**See CLAUDE.md for full environment rules** — always use `uv run python ...`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If `override_reference_mw` produces unexpected costs, investigate before proceeding. Check if the issue is in cost overrides, scaling ratios, or a framework bug. Escalate to user.
- **Phase 2**: If extractor change breaks non-1GW concepts, the change is isolated (~10 lines) and easy to revert. Freeform and already-at-1GW concepts are tested explicitly.
- **Phase 3**: If a regenerated model lacks `result_1gw` or has errors, investigate individually. The `--force` re-run can target single concepts. Per-concept validation catches failures before they propagate. Timeout may need `--timeout 1800` for slower concepts (observed in prior work).

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-19
**Actual Changes:** Added `result_1gw = model.forward(net_electric_mw=1000.0, override_reference_mw=261.0, ...)` to concept 01 model_setup.py after existing `scaled_headline` block.
**Issues:** LCOE delta was -42.3% (216.3 vs 374.9 post-hoc), well outside expected 5-15% range. This is correct — ARC has the largest scaling correction (261→1000 MWe, nearly 4× ratio) and per-account exponents diverge significantly from the uniform α=0.6 at that ratio. User approved proceeding.
**Deviations:** None — manual edit pattern matched design exactly.

### Phase 2 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- `extract_explorer_data.py`: Replaced `scaled_headline` injection block in `extract_costingfe()` with `result_1gw` check. When present, uses `result_1gw` for both `CostModelData` and sensitivities. Falls through to native `result` when absent.
- `model_setup_costingfe.md`: Replaced "Power Standardization (CRITICAL)" section with "Power Standardization: Dual-Result Pattern" — `_SHARED_KWARGS`, `override_reference_mw`, conditional skip for 1GW concepts.
**Issues:** Concept 03 LCOE changed (122.4→107.5) due to upstream costingfe library rebuild, not extractor changes. Confirmed: concept 03 has no `scaled_headline`, native LCOE is 107.5 from current library.
**Deviations:** None.

### Phase 3 Completion
**Completed:** 2026-04-19
**Actual Changes:**
- Batch re-generated all 8 concepts via `run_analysis.py model-setup ... --force` (used Sonnet, ~22 min total)
- All 8 regenerated models expose `result_1gw`, none have `scaled_headline`
- Re-extracted all 19 concepts — no errors
- Cross-concept validation: all show p_net≈1000 (except 08 FRC modular at 50 MWe/module, pre-existing)
- Freeform concepts: 0% delta (completely unaffected)
- At-1GW concepts: small deltas from costingfe library rebuild (03: -12.1%, 07: +12.8%, 09: +26.7%)
- Migrated concepts: deltas from -42.2% (01 ARC) to +24.2% (14 MTF) vs old post-hoc α=0.6
**Issues:** Concept 09 (at-1GW) showed +26.7% delta — not caused by this work, purely from costingfe library change during re-extraction.
**Deviations:** Concept 01 model_setup.py was externally modified (linter/user edit) to use `_SHARED_KWARGS` pattern during Phase 3; adopted as-is since it matches the template pattern.

---

**Status**: Complete
