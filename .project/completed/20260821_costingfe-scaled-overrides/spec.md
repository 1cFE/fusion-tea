# Spec: Costingfe Scaled Overrides Integration

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-19 09:49 PDT
**Complexity:** MEDIUM
**Branch:** main

---

## Business Goals

### Why This Matters

The current cross-concept comparison uses a single-exponent (α=0.6) post-hoc scaling to normalize all concepts to 1000 MWe. This produces only 3 headline numbers (LCOE, overnight $/kW, p_net) — the entire CAS breakdown, sensitivities, and power table remain at native power. The explorer shows CAS breakdowns at 261 MWe alongside a headline claiming 1000 MWe. This is the core inconsistency.

The new `override_reference_mw` feature in 1costingfe scales each cost override from reference power to target power using the model's own per-account scaling laws (different exponents for blankets, coils, turbines, etc.), producing a complete, self-consistent `ForwardResult` at the target power. This gives us full CAS breakdowns, sensitivities, and power tables at 1 GW — enabling genuine apples-to-apples comparison.

### Success Criteria

- [ ] All 8 non-1GW costingfe concepts produce a full `result_1gw` via `override_reference_mw`
- [ ] Explorer shows 1GW data (CAS breakdown, headline, tornado) by default — extractor puts 1GW data in `cost_model` directly, no new field needed
- [ ] `scaled_headline` is removed from costingfe concepts (no longer needed)
- [ ] Freeform concepts continue working with their existing post-hoc α=0.6 approach
- [ ] Already-at-1GW costingfe concepts (03, 04, 07, 08, 09, 10) are unaffected

### Priority

P1 — direct improvement to the core analytical output.

---

## Problem Statement

### Current State

- 19 concepts have `model_setup.py` files; 8 costingfe concepts run at native power (261–600 MWe) with a post-hoc `scaled_headline` dict that provides 3 numbers at 1000 MWe
- The explorer shows CAS breakdowns, sensitivities, and params at native power — inconsistent with the 1000 MWe headline
- The single α=0.6 exponent is a rough average of per-account exponents that range from 0.5 (buildings, O&M) to 1.0 (BOP, heating) — concepts with different cost structures get distorted differently

### Desired Outcome

8 costingfe concepts produce a full `result_1gw` using 1costingfe's per-account scaling. The explorer defaults to the 1GW data for all views. `scaled_headline` is dropped from costingfe models. Freeform concepts unchanged.

---

## Scope

### In Scope

1. Costingfe prompt template — replace post-hoc `scaled_headline` with dual-result pattern
2. Extractor — when `result_1gw` exists, build `CostModelData` from it (with live sensitivities) and put it in `cost_model` directly
3. Test on concept 01 (ARC, 261 MWe) as soft gate
6. Cold-start re-run all 8 costingfe concepts via `--force`
7. Re-extraction of all 19 concepts + cross-concept validation

### Out of Scope

- Freeform concept changes (keep post-hoc α=0.6 as-is)
- Native/1GW toggle UI (just default to 1GW)
- Slider recompute at 1GW (`POST /api/compute` unchanged — sliders operate on native result)
- Comparison page new view plugins (existing comparison uses manifest data which already has correct LCOE)
- Changes to 1costingfe itself
- Feedback template updates (using cold-start `--force`, not feedback-based edits)

### Edge Cases & Considerations

- **Concept 08 (FRC)**: Modular plant (20×50 MWe). Already at 1 GW plant-level. Skip `result_1gw` — same as concepts 03, 04, 07, 09, 10.
- **LCOE delta from old approach**: Expect 5–15% differences for concepts far from 1 GW (ARC especially). This is expected and correct — the per-account scaling is more physically grounded than the single-exponent approximation.
- **Sensitivity pre-existing inconsistency**: `build_sensitivity_analysis()` calls `model.sensitivity(result.params)` without `cost_overrides`. Same behavior applies to `result_1gw`. This is pre-existing and not addressed here.

---

## Requirements

### Functional Requirements

#### FR-1: Costingfe Prompt Template — Dual-Result Pattern

The `model_setup_costingfe.md` template MUST be updated to replace the post-hoc `scaled_headline` section with:
- Factor shared engineering kwargs into a `_SHARED_KWARGS` dict
- `result = model.forward(net_electric_mw=<native>, **_SHARED_KWARGS)`
- If native power != 1000 MWe: `result_1gw = model.forward(net_electric_mw=1000.0, override_reference_mw=<native>, **_SHARED_KWARGS)`
- If native power IS 1000 MWe: skip `result_1gw` entirely
- Do NOT compute `sens_1gw` — the extractor calls `model.sensitivity()` live
- Do NOT generate `scaled_headline` — the extractor derives headlines from `result_1gw`

#### FR-2: Extractor — Full 1GW Data Extraction

Update `extract_costingfe()` in `extract_explorer_data.py` to:
1. Check for `result_1gw = getattr(module, "result_1gw", None)`
2. If present: call `build_sensitivity_analysis(model, result_1gw)` (extractor computes live)
3. Build `CostModelData.from_forward_result(asdict(result_1gw), sens_1gw)` and put it in `cost_model` directly — no new field
4. If absent: use native `result` as today

The existing `scaled_headline` injection path for costingfe concepts SHOULD be removed. The freeform `_apply_scaled_headline` path MUST remain unchanged.

#### FR-3: Test on Concept 01 (ARC)

Before full migration:
1. Manually add `result_1gw` to `analyses/01-hts-compact-tokamak/model_setup.py` using the dual-result pattern
2. Run the script, compare old post-hoc LCOE vs. new per-account LCOE
3. Quantify the delta
4. Soft gate: proceed unless something is clearly broken

#### FR-4: Cold-Start Re-run All 8 Concepts

Re-generate all 8 non-1GW costingfe concepts via:
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py \
    model-setup 01 05 06 11 14 17a 21 28 --force
```

Each regenerated model MUST:
- Run without errors
- Expose `result` at native power and `result_1gw` at 1000 MWe
- NOT contain `scaled_headline`

#### FR-5: Re-extraction and Validation

After all models are updated:
- Re-extract all 19 concepts
- All 8 migrated concepts MUST have `cost_model_1gw` populated in their JSON
- 6 already-at-1GW + 5 freeform concepts MUST have `cost_model_1gw: null`
- Spot-check LCOE values for reasonableness

---

## Acceptance Criteria

### Core Functionality
- [ ] Costingfe template produces dual-result pattern with `_SHARED_KWARGS` (FR-1)
- [ ] Extractor builds `CostModelData` from `result_1gw` and puts it in `cost_model` directly (FR-2)
- [ ] Concept 01 tested and delta quantified (FR-3)
- [ ] All 8 concepts re-generated with `result_1gw` (FR-4)
- [ ] All 19 concepts re-extracted and validated (FR-5)

### Quality & Integration
- [ ] Every `model_setup.py` runs without errors
- [ ] Native `result` untouched — physics, Q_eng, CAS breakdown at native power
- [ ] Freeform concepts unaffected (still use post-hoc `scaled_headline`)
- [ ] Already-at-1GW concepts unaffected
- [ ] No regressions in explorer (extraction, comparison views)

---

## Related Artifacts

- **Research:** `.project/research/20260419-costingfe-scaled-overrides-integration.md`
- **Prior work:** `.project/active/power-standardization/` (post-hoc approach being replaced)
- **Prompt template:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- **Extractor:** `exploration/concept_explorer/extract_explorer_data.py`
- **Data model:** `exploration/concept_explorer/models.py`
- **Frontend:** `exploration/concept_explorer/static/js/concept_page.js`
- **1costingfe feature:** `1costingfe/src/costingfe/model.py:379, 793-840`

---

**Next Steps:** After approval, proceed to `/_my_design`
