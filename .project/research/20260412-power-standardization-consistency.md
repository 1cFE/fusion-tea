---
date: 2026-04-12T12:00:00-07:00
researcher: Claude
topic: "Power output standardization consistency across concept analysis models"
tags: [research, concept-analysis, costingfe, power-normalization, lcoe-comparison]
status: complete
last_updated: 2026-04-12
---

# Research: Power Output Standardization Consistency

**Date**: 2026-04-12
**Researcher**: Claude
**Research Type**: Codebase / Architecture

## Research Question

A colleague observed that model outputs don't appear standardized in terms of output power. 1costingfe is designed to support consistent power for like-for-like comparison. Are the concept analysis `model_setup.py` files using consistent power levels?

## Summary

- **1costingfe does NOT enforce a standard power level.** `forward()` accepts arbitrary `net_electric_mw` — standardization is the caller's responsibility.
- **The 19 concept models span 200–1000 MWe net electric output** — a 5× range that distorts LCOE comparisons due to economies of scale.
- **Two philosophies are mixed inconsistently**: some models use concept-native power (company's stated design), others use 1000 MWe as a normalized reference.
- **Six concepts use 1000 MWe** (03, 04, 07, 08, 09, 10); the rest use concept-native values ranging from 200–600 MWe.
- **Freeform models (12, 15, 22, 35) are the hardest to normalize** since their physics is baked into the dataclass parameters, not derived from a requested net_electric_mw.

## Detailed Findings

### 1costingfe Framework Behavior

The framework is power-agnostic. `CostModel.forward(net_electric_mw=...)` accepts any value. The README examples use `compare_all(net_electric_mw=1000.0, ...)` as convention, but nothing enforces this.

**Key file**: `/home/reid/1cfe/1costingfe/src/costingfe/model.py:344` — `forward()` definition.

The framework works backward from net electric to derive fusion power through the efficiency chain (thermal conversion, recirculating power, etc.). Cost accounts scale with power, so different `net_electric_mw` values produce different $/kW and $/MWh even for the same concept.

### Power Levels Across All Models

#### costingfe Models (15 concepts)

| # | Concept | net_electric_mw | avail | n_mod | eta_th | Power Source |
|---|---------|----------------:|------:|------:|-------:|-------------|
| 01 | HTS Compact Tokamak (ARC) | **261** | 0.75 | 1 | 0.46 | ARC pilot design point |
| 03 | Laser ICF Liquid Jet | **1000** | 0.40 | 1 | 0.35 | Standard CAS reference scale |
| 04 | Laser ICF p-B11 (HB11) | **1000** | 0.70 | 1 | 0.35 | HB11 company 1 GW target |
| 05 | Planar Coil Stellarator (Thea) | **390** | 0.88 | 1 | 0.40 | Helios preconceptual design |
| 06 | Magnetic Mirror p-B11 | **500** | 0.80 | 1 | 0.20 | Reference scale (no published design) |
| 07 | MagLIF | **1000** | 0.85 | 1 | 0.42 | Z-IFE reference design |
| 08 | FRC w/ Direct Conversion (Helion) | **1000** | 0.85 | 20 | 0.90* | 20×50 MWe modules |
| 09 | QI Stellarator HTS (Proxima) | **1000** | 0.88 | 1 | 0.38 | Stellaris design target |
| 10 | Large-Scale Stellarator (Gauss) | **1000** | 0.88 | 1 | 0.35 | GIGA 1 GWe design target |
| 11 | Magnetic Mirror D-T (Realta) | **500** | 0.85 | 1 | 0.38 | Commercial scale |
| 14 | MTF Pneumatic (General Fusion) | **300** | 0.80 | 1 | 0.35 | GF stated commercial target |
| 17a | Laser ICF Hybrid (Xcimer) | **400** | 0.85 | 1 | 0.45 | Xcimer Athena pilot |
| 21 | Spherical Tokamak HTS (TE) | **600** | 0.80 | 1 | 0.33 | Mid-range of Rev D |
| 28 | HTS Tokamak Full HTS (ES) | **500** | 0.80 | 1 | 0.40 | Proxy (no published design) |

*Helion's 0.90 represents EM recovery proxy, not thermal efficiency.

#### Freeform Models (5 concepts)

| # | Concept | p_net (approx) | p_fus | avail | n_mod | eta_th | Power Source |
|---|---------|---------------:|------:|------:|------:|-------:|-------------|
| 02 | Acoustic ICF/Sonofusion | ~1000 (4×mod) | varies | 0.75 | 4 | 0.35 | Reference scale |
| 12 | Levitated Dipole (OpenStar) | **~208** | 667 | 0.865 | 1 | 0.38 | Published Reactor A (Simpson et al.) |
| 15 | SFS Z-Pinch (Zap Energy) | **~200** (4×mod) | 190/mod | 0.75 | 4 | 0.33 | Century demo extrapolation |
| 22 | Projectile ICF (First Light) | **~333** | ~990 | 0.85 | 1 | 0.33 | FLF design point |
| 35 | PoloMac (Deutelio) | computed | 500 (assumed) | 0.70 | 1 | 0.38 | ASSUMED (no published design) |

### Distribution of Power Levels

```
1000 MWe: 03, 04, 07, 08, 09, 10, (02)     — 7 concepts (normalized reference)
 500 MWe: 06, 11, 28, (35?)                  — 3-4 concepts (commercial scale proxy)
 300-400: 05 (390), 14 (300), 17a (400), 22 (~333) — 4 concepts (concept-native)
 200-261: 01 (261), 12 (~208), 15 (~200)     — 3 concepts (concept-native)
 600 MWe: 21                                  — 1 concept
```

### Why This Matters for LCOE Comparison

Fusion plant costs exhibit significant economies of scale. Key effects:

1. **Capital cost scaling**: CAS accounts (buildings, turbine plant, electrical plant) scale sub-linearly with power. A 1000 MWe plant costs less than 4× a 250 MWe plant. So $/kW decreases with size.

2. **LCOE scaling**: Since LCOE = annual_cost / annual_energy, and annual_cost scales sub-linearly while annual_energy scales linearly with net power, larger plants always look better on LCOE. A concept at 1000 MWe will appear cheaper per MWh than the same concept at 300 MWe, even if the underlying technology is identical.

3. **Comparison distortion**: Comparing ARC at 261 MWe against Stellaris at 1000 MWe is not an apples-to-apples comparison of confinement concepts — it's partly a comparison of plant size choices.

### Two Competing Design Philosophies

**Philosophy A: Concept-native power** — Use each company's stated design point.
- Pro: Reflects what they plan to build; respects physics constraints (some concepts can't scale to 1 GWe)
- Con: Can't compare LCOE across concepts meaningfully; conflates concept merit with scale choice
- Used by: 01, 05, 12, 14, 15, 17a, 21, 22

**Philosophy B: Normalized reference power** — Use 1000 MWe (or another standard) for all.
- Pro: Enables like-for-like LCOE comparison; isolates concept-specific cost drivers
- Con: May be physically unrealistic for some concepts; obscures real deployment economics
- Used by: 03, 04, 07, 08, 09, 10

**Mixed/unclear**: 06, 11, 28, 35 (use 500 MWe which is neither the company target nor the standard 1000 MWe)

### Additional Inconsistencies

Beyond net power, other parameters that affect comparability:

1. **Availability**: Ranges from 0.40 (Cortex, TRL 1) to 0.88 (stellarators). This is a legitimate concept difference, but the 0.40 for Cortex is more of a "we have no idea" placeholder.

2. **n_mod**: Most use 1, but Helion uses 20 (20×50 MWe) and Z-Pinch/Sonofusion use 4 modules. Multi-module plants have different cost scaling (shared BOP, lower per-module cost).

3. **Thermal efficiency**: Ranges from 0.20 (Mirror p-B11 with DEC) to 0.90 (Helion EM recovery). This is a real concept difference, but the Helion 0.90 is a proxy for EM recovery, not thermal conversion.

## Code References

- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:344` — `forward()` accepts arbitrary `net_electric_mw`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` — costingfe prompt template (no power standardization instruction)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/model_setup_freeform.md` — freeform prompt template (no power standardization instruction)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/scripts/lib/paths.py:25` — `COSTINGFE_DIR` path definition

## Architecture Insights

1. **Neither prompt template mentions power standardization.** The costingfe template says "write a script that uses 1costingfe to produce an LCOE estimate" but doesn't specify a target power level. The freeform template says "compute LCOE from first principles" without any normalization requirement.

2. **The assessment checklist** (`prompt_templates/config/assessment_checklist.md`) likely doesn't check for power normalization either (not verified — would need to read this file).

3. **The concept explorer** (`exploration/concept_explorer/`) consumes `model`/`result` or `params`/`results` at module level for cross-concept comparison. If it's comparing LCOE values directly without adjusting for plant size, the comparison is misleading.

## Feasibility Assessment

### Fixing costingfe models (straightforward)
For the 14 costingfe models, adding a normalized `net_electric_mw=1000.0` run alongside the concept-native run is trivial — just add a second `model.forward()` call. The framework handles all rescaling internally.

### Fixing freeform models (harder)
The 5 freeform models have physics baked into their dataclass parameters. Changing p_fus or target power requires re-deriving the entire power balance. Some concepts may not physically scale to 1000 MWe (e.g., single-module Z-Pinch at 50 MWe).

### Recommended approach: dual-output
Each model could produce two results:
1. **Concept-native**: The company's stated design point (reflects deployment reality)
2. **Normalized**: 1000 MWe reference (or closest feasible scale) for cross-concept comparison

The concept explorer should clearly label which comparison mode is being shown.

## Recommendations

1. **Add a power standardization instruction to both prompt templates** — specify that models should include a 1000 MWe normalized run for cross-concept comparison.

2. **For costingfe models**: Add a `result_normalized = model.forward(net_electric_mw=1000.0, ...)` alongside the concept-native run. Minimal effort.

3. **For freeform models**: Add a scaling method or second parameter set that adjusts to a reference power level. More effort — may require documenting which concepts can't physically scale to 1 GWe.

4. **Update the concept explorer** to distinguish "native LCOE" from "normalized LCOE" in cross-concept comparisons.

5. **Document the choice** in the analysis README or OPERATOR_GUIDE — explain that both native and normalized outputs are produced and when to use each.

6. **Consider whether 1000 MWe is the right reference** — some fusion concepts are inherently modular/small. A 500 MWe or even 300 MWe reference might be more broadly applicable. Or use multiple reference points.

## Open Questions

1. Does the concept explorer currently compare LCOE values directly without power normalization? (Would need to audit `extract_explorer_data.py` and the comparison logic.)

2. For multi-module concepts (Helion 20×50 MWe, Z-Pinch 4×50 MWe), should the "normalized" run scale to 1000 MWe plant-level or 1000 MWe per-module?

3. Should the assessment checklist flag power deviation from the reference as a finding?

4. How should concepts that physically can't reach 1000 MWe (e.g., single-module Z-Pinch at 50 MWe) be handled in the normalized comparison?
