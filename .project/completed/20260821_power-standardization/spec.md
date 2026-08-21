# Spec: Power Output Standardization for Cross-Concept Comparison

**Status:** Draft (revised — post-hoc scaling approach)
**Owner:** Reid W
**Created:** 2026-04-12 09:32 PDT
**Updated:** 2026-04-12
**Complexity:** MEDIUM
**Branch:** concept-power-standardization

---

## Business Goals

### Why This Matters

Cross-concept LCOE comparison is a core project output. The 19 concept analysis models currently span 200–1000 MWe net electric output — a 5× range that distorts comparisons via economies of scale. Larger plants get lower LCOE just from being larger, so the current comparisons are partly measuring scale choice rather than concept merit.

### Success Criteria

- [ ] All non-1000-MWe concepts export a `scaled_headline` dict at module level with 1000 MWe-normalized LCOE and overnight $/kW
- [ ] The concept explorer extractor checks for `scaled_headline` and uses it for HeadlineEconomics when present, falling back to native `result`/`results` otherwise
- [ ] Native `result`/`results` is **untouched** — physics, power balance, Q_eng, and CAS breakdown remain internally consistent at the concept's design point
- [ ] Future model generations via the pipeline automatically include `scaled_headline` (prompt templates updated)
- [ ] All 6 currently-at-1000-MWe concepts verified as truly compliant (no `scaled_headline` needed — extractor falls through to native result)
- [ ] CAS breakdown, CAS22 detail, and sensitivities all come from the native result (consistent physics)

### Priority

P1 — foundational to the analysis the project is producing.

---

## Problem Statement

### Current State

- 19 concepts have `model_setup.py` files with inconsistent net electric power levels
- 7 concepts use 1000 MWe; 12 use concept-native levels (200–600 MWe)
- Neither prompt template mentions power standardization
- The concept explorer extraction reads module-level `result`/`results` directly — whatever power level the model uses is what the comparison shows

### Desired Outcome

All 19 concepts produce normalized LCOE and overnight $/kW at a standard 1000 MWe reference level for headline comparison. Native-power results are preserved as-is for CAS breakdowns, sensitivities, and physics consistency. The normalization uses a uniform post-hoc scaling formula (α=0.6 economy-of-scale exponent).

---

## Scope

### In Scope

1. Prompt template updates (both costingfe and freeform)
2. Verification of 6 already-at-1000-MWe concepts
3. Direct `scaled_headline` edits to simple costingfe models (05, 11, 21)
4. Feedback-iteration re-runs for remaining models
5. Extractor support for `scaled_headline` in both costingfe and standalone pathways
6. Re-extraction of all 19 concepts to confirm explorer compliance

### Out of Scope

- Concept explorer frontend changes (no $/kW toggle, no display changes)
- Full re-analysis (analyze→assess) — only model-setup step or targeted edits
- Changes to 1costingfe framework itself
- CAS absolute M$ normalization (CAS $/kW display could be a future enhancement)
- Concepts without existing model_setup.py

### Approach: Post-Hoc Scaling

**Principle**: Every model runs at its native design point. The physics, power balance, Q_eng, and CAS breakdown are all internally consistent at that point. A uniform post-hoc scaling step produces normalized 1000 MWe headline numbers (LCOE, overnight $/kW) for cross-concept comparison.

**Scaling formula** (per-unit metrics like LCOE and overnight $/kW):

```
factor = (p_native / 1000) ** (1 - α)    where α = 0.6
value_1gwe = value_native × factor
```

- For ARC (261 MWe): factor ≈ 0.58 → LCOE drops from ~640 to ~370 $/MWh
- For a 1000 MWe concept: factor = 1.0 → no change

**What this avoids**:
- No inflated Q_eng (stays at native design point)
- No geometry/parasitic inconsistency
- No re-derivation of cost overrides at a different plant size
- Costingfe and freeform use the same scaling approach

**Known limitation**: CAS absolute M$ comparison is at native plant size (different scales). Overnight $/kW and LCOE are already per-unit metrics, so the headline comparison is fair.

---

## Requirements

### Functional Requirements

#### FR-1: Prompt Template Standardization

Both `model_setup_costingfe.md` and `model_setup_freeform.md` MUST be updated to instruct the addition of a `scaled_headline` dict at module level:

- The costingfe template MUST instruct: compute `scaled_headline` using post-hoc scaling with α=0.6 from the native `result`
- The freeform template MUST instruct: compute `scaled_headline` using the same formula from the native `results`
- The template MUST specify that `result`/`results` stays at native power (untouched)
- If the concept's native design point IS 1000 MWe, `scaled_headline` may be omitted (extractor falls through)

#### FR-2: Verification of Existing 1000 MWe Concepts

The following 6 concepts MUST be verified as compliant (native `result`/`results` at 1000 MWe):

| ID | Concept | Current Power | Verification Focus |
|----|---------|--------------|-------------------|
| 03 | Laser ICF Liquid Jet | 1000 MWe | Confirm module-level `result` |
| 04 | Laser ICF p-B11 | 1000 MWe | Confirm module-level `result` |
| 07 | MagLIF | 1000 MWe | Confirm model type and result |
| 08 | FRC w/ Direct Conversion | 1000 MWe (20×50) | Confirm plant-level = 1000 MWe |
| 09 | QI Stellarator HTS | 1000 MWe | Confirm module-level `result` |
| 10 | Large-Scale Stellarator | 1000 MWe | Confirm module-level `result` |

These concepts need NO `scaled_headline` — the extractor falls through to native result.

#### FR-3: Direct Edits for Simple Costingfe Models

The following concepts MUST be updated by adding a `scaled_headline` block after the existing `result`:

| ID | Concept | Native Power | Edit |
|----|---------|-------------|------|
| 05 | Planar Coil Stellarator | 390 MWe | Add `scaled_headline` block |
| 11 | Magnetic Mirror D-T | 500 MWe | Add `scaled_headline` block |
| 21 | Spherical Tokamak HTS | 600 MWe | Add `scaled_headline` block |

Each MUST:
- Leave `result = model.forward(...)` completely untouched at native power
- Add a ~5 line `scaled_headline` dict after `result` using the standard scaling formula
- Verify the model runs successfully after edit

#### FR-4: Feedback Iteration for Costingfe Models

The following concepts MUST be updated via the pipeline's feedback iteration mechanism with a feedback directive to add `scaled_headline`:

| ID | Concept | Native Power |
|----|---------|-------------|
| 01 | HTS Compact Tokamak (ARC) | 261 MWe |
| 06 | Magnetic Mirror p-B11 | 500 MWe |
| 14 | MTF Pneumatic (GF) | 300 MWe |
| 17a | Laser ICF Hybrid (Xcimer) | 400 MWe |
| 28 | HTS Tokamak Full HTS | 500 MWe |

The feedback MUST direct Claude to:
- Keep the existing `result` at native power (do NOT change `net_electric_mw`)
- Keep all cost_overrides at their published/derived values (no re-derivation)
- Add a `scaled_headline` dict at module level using post-hoc scaling (α=0.6)

#### FR-5: Feedback Iteration for Freeform Models

The following freeform concepts MUST be updated via feedback iteration:

| ID | Concept | Native p_net |
|----|---------|-------------|
| 02 | Acoustic ICF/Sonofusion | ~1000 MWe |
| 12 | Levitated Dipole | ~208 MWe |
| 15 | SFS Z-Pinch | ~200 MWe |
| 22 | Projectile ICF | ~333 MWe |
| 35 | PoloMac | computed |

The feedback MUST direct Claude to:
- Keep the physics-derived power balance as-is (do NOT change p_fus, rep_rate, n_mod, etc.)
- Keep `results` at native power
- Add a `scaled_headline` dict at module level using the same post-hoc scaling formula

#### FR-6: Re-extraction and Verification

After all models and the extractor are updated:
- All 19 concepts MUST be re-extracted via the concept explorer extraction script
- The explorer MUST show all concepts at 1000 MWe in the headline `p_net_mw` field
- A spot-check of LCOE values SHOULD confirm they are reasonable at the normalized level

#### FR-7: Extractor Support for `scaled_headline`

Both extraction pathways (`extract_costingfe` and `extract_standalone`) MUST be updated to:
- Check for a `scaled_headline` dict at module level after loading `model_setup.py`
- If present, use its `lcoe_per_mwh`, `overnight_per_kw`, and `p_net_mw` values to override the corresponding fields in HeadlineEconomics
- If absent, fall through to existing behavior (read from native `result`/`results`)
- CAS breakdown, CAS22 detail, sensitivities, and all other fields continue to come from the native result

---

## Acceptance Criteria

### Core Functionality
- [ ] Both prompt templates include `scaled_headline` instructions (FR-1)
- [ ] All 6 already-at-1000-MWe concepts verified compliant (FR-2)
- [ ] All 3 simple costingfe models have `scaled_headline` blocks (FR-3)
- [ ] All 5 costingfe models updated via feedback with `scaled_headline` (FR-4)
- [ ] All 5 freeform models updated via feedback with `scaled_headline` (FR-5)
- [ ] Extractor supports `scaled_headline` in both pathways (FR-7)
- [ ] All 19 concepts re-extracted showing 1000 MWe in explorer headline (FR-6)

### Quality & Integration
- [ ] Every model_setup.py runs without errors (`uv run python model_setup.py`)
- [ ] Native `result`/`results` is untouched — physics, Q_eng, CAS breakdown unchanged
- [ ] No regressions in existing explorer functionality (extraction, comparison views, sliders)
- [ ] Scaling exponent (α=0.6) documented in each modified model

---

## Concept Triage Summary

| Bucket | IDs | Count | Method |
|--------|-----|-------|--------|
| Verify only | 03, 04, 07, 08, 09, 10 | 6 | Read + confirm (no scaled_headline needed) |
| Direct edit | 05, 11, 21 | 3 | Add `scaled_headline` block |
| Feedback iteration (costingfe) | 01, 06, 14, 17a, 28 | 5 | Re-run with feedback → add `scaled_headline` |
| Feedback iteration (freeform) | 02, 12, 15, 22, 35 | 5 | Re-run with feedback → add `scaled_headline` |
| **Total** | | **19** | |

---

## Related Artifacts

- **Research:** `.project/research/20260412-power-standardization-consistency.md`
- **Design:** `.project/active/power-standardization/design.md`
- **Prompt templates:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`, `model_setup_freeform.md`
- **Pipeline:** `exploration/concept_analysis/scripts/run_analysis.py`, `scripts/lib/loop.py`
- **Extraction:** `exploration/concept_explorer/extract_explorer_data.py` (both pathways), `models.py` (`HeadlineEconomics`)
