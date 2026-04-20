---
date: 2026-04-19T12:00:00-07:00
researcher: Claude
topic: "Integrating 1costingfe scaled overrides into the fusion-tea pipeline"
tags: [research, pipeline, costingfe, scaling, integration]
status: complete
last_updated: 2026-04-19
---

# Research: Integrating 1costingfe `override_reference_mw` into the Fusion-TEA Pipeline

**Date**: 2026-04-19
**Researcher**: Claude
**Research Type**: Integration / Architecture

## Research Question

How does the current pipeline standardize concept outputs to 1 GW, and how would the
new `override_reference_mw` feature in 1costingfe replace or augment that approach?
What would need to change across the full pipeline (code, prompts, templates, extractor)?

## Summary

- **Current approach**: Post-hoc `scaled_headline` dict — a 5-line block appended to
  each `model_setup.py` that applies a uniform α=0.6 power-law scaling factor to
  LCOE and overnight $/kW after the native-power `model.forward()` run. Only 3 fields
  are scaled (LCOE, overnight $/kW, p_net); the entire CAS breakdown, sensitivities,
  params, q_eng, and capacity_factor remain at native power. 19/19 concepts implemented.
- **New 1costingfe feature**: `model.forward(..., override_reference_mw=X)` scales
  each `cost_override` from reference power X to target power using the model's own
  per-account scaling laws (different exponents for blankets, coils, turbines, etc.).
  Produces a complete, self-consistent `ForwardResult` at the target power.
- **Key difference**: The current approach scales 3 headline *outputs* with a single
  exponent. The new feature scales the *input* cost overrides per-account before
  running the full model, producing a self-consistent CAS breakdown, power table,
  sensitivities, and LCOE at the target power.
- **Integration path**: For costingfe-backed concepts not already at 1 GW, add a
  second `model.forward()` at 1000 MWe using `override_reference_mw=native_power`.
  Expose the full `result_1gw` (CAS breakdown, sensitivities, power table) to the
  explorer. Freeform concepts keep the post-hoc α=0.6 approach.

## Decided Scope

These decisions were confirmed before implementation:

1. **Full 1 GW CAS breakdown** — not just headlines. The extractor and explorer data
   model must be extended to carry the complete `result_1gw` (CAS accounts,
   sensitivities, power table) alongside the native result.
2. **Freeform concepts** — keep post-hoc α=0.6 as-is (no costingfe model to re-run).
3. **Already-at-1GW concepts** — skip `result_1gw` with a conditional in the template
   (no-op when native power is already 1000 MWe).
4. **Test first** — run concept 01 (ARC, 261 MWe) as a test case to quantify the
   LCOE delta before migrating all concepts.
5. **Re-run all affected costingfe concepts** — cold-start regeneration, not
   feedback-based edit. Full list in "Concepts Requiring Re-run" below.
6. **Sensitivity at 1 GW** — the extractor computes this live (see "Extraction
   Contract" below). The `model_setup.py` only needs to expose `result_1gw`; the
   extractor calls `model.sensitivity(result_1gw.params)` itself, consistent with
   how it already handles native sensitivities.
7. **Shared parameter dict** — the template must instruct Claude to factor common
   kwargs into a shared dict to avoid duplication between `result` and `result_1gw`
   forward() calls.

## Detailed Findings

### 1. Current Pipeline: Post-Hoc `scaled_headline`

**Commit**: `3e14589` — "Power standardization: normalize all 19 concepts to 1000 MWe
headline comparison"

**Design docs**:
- `.project/active/power-standardization/spec.md` — requirements, 6 concept buckets
- `.project/active/power-standardization/design.md` — architecture
- `.project/active/power-standardization/plan.md` — 4 phases, all COMPLETE

**Implementation**: Every `model_setup.py` includes this block after the native result:

```python
# Costingfe variant (in model_setup_costingfe.md template, line 56-65):
_ALPHA = 0.6
_p_native = float(result.power_table.p_net)
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
    "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
}
```

**Freeform variant** (in `model_setup_freeform.md`, line 47-72):
Same formula but sources `_p_native` from `results["power"]` dict and computes
`_overnight` manually.

**Properties of this approach**:
- ✅ Uniform — same formula for all 19 concepts, costingfe and freeform alike
- ✅ Non-invasive — native result stays untouched
- ❌ Single-exponent — α=0.6 applied uniformly to total LCOE, doesn't capture
  per-account scaling (coils don't scale like turbines)
- ❌ Headline-only — no CAS breakdown at 1 GW, just 3 top-line numbers
- ❌ No physics re-solve — power balance at 1 GW not computed

### 2. Full Data Model: What Flows from `model_setup.py` → Explorer

The `scaled_headline` only touches 3 of ~80+ fields. Here's the complete data model
consumed by the concept explorer, showing what is currently scaled vs. what stays
at native power:

#### `HeadlineEconomics` (the only thing `scaled_headline` touches today)

| Field | Source (costingfe) | Source (freeform) | Scaled? |
|-------|-------------------|-------------------|---------|
| `lcoe_per_mwh` | `result.costs.lcoe` | `results["economics"]["lcoe_USD_per_MWh"]` | ✅ Yes |
| `overnight_cost_per_kw` | `result.costs.overnight_cost` | computed from `overnight_capital / p_net` | ✅ Yes |
| `p_net_mw` | `result.power_table.p_net` | `results["power"]["p_net_plant"]` | ✅ Yes (set to 1000) |
| `q_eng` | `result.power_table.q_eng` | `results["power"]["Q_eng"]` | ❌ Native |
| `capacity_factor` | `result.params["availability"]` | `params.plant_availability` | ❌ Native |

#### CAS Accounts (18 top-level + 18 CAS22 sub-accounts) — ALL at native power

Each is a `CASAccount(name, cost_m_usd, overridden)`. Extracted from:
- Costingfe: `result.costs.cas10`...`cas90` + `result.cas22_detail`
- Freeform: `results["costs"]` + `results["cas22"]`

**None of these are scaled today.** The explorer shows CAS breakdowns at native power
even though the headline says 1000 MWe. This is the core inconsistency being fixed.

#### Sensitivities — at native power

`SensitivityAnalysis` with `engineering` and `financial` dicts, each containing
`SensitivityEntry(elasticity, baseline)`. Computed via:
- Costingfe: `model.sensitivity(result.params, cost_overrides=...)`
- Freeform: central-difference perturbation on LCOE (1% per param)

Sensitivities are computed at the native design point. A 1 GW result would have
different sensitivities (different parameter importance at larger scale).

#### Parameters — native design point

All numeric `float` fields from `result.params` (costingfe) or `dataclasses.fields()`
(freeform). These are the engineering inputs, not outputs — inherently at native power.

#### Narrative, Metadata, Sources — power-independent

`NarrativeData` (key_bets, risks, eliminated/novel costs), `ParameterMetadata`,
`SourcePaths` — these don't depend on power level.

#### What `override_reference_mw` gives us

With a full `result_1gw = model.forward(net_electric_mw=1000, ...)`:
- ✅ **CAS breakdown at 1 GW** — all 36 accounts self-consistently scaled
- ✅ **Power table at 1 GW** — p_fus, p_th, p_et, p_net, q_eng all recomputed
- ✅ **Sensitivities at 1 GW** — via `model.sensitivity(result_1gw.params, ...)`
- ✅ **LCOE and overnight $/kW** — computed from 1 GW cost structure, not post-hoc

### 3. New 1costingfe Feature: `override_reference_mw`

**File**: `1costingfe/src/costingfe/model.py:379, 793-840`
**Example**: `1costingfe/examples/scaled_overrides.py`

**API**:
```python
result = model.forward(
    net_electric_mw=1000.0,        # target power
    cost_overrides=overrides,       # M$ values valid at reference power
    override_reference_mw=261.0,    # reference power where overrides are valid
    ...
)
```

**Mechanism** (`_scale_overrides`, model.py:793-840):
1. Run model at reference power (no overrides) → get baseline CAS costs at ref
2. Run model at target power (no overrides) → get baseline CAS costs at target
3. For each override key: `scaled_value = user_value × (target_cost / ref_cost)`
4. Use scaled overrides in the final `forward()` at target power

**Per-account scaling laws** (implicit via ratio):

| Account | Scaling Basis | Effective Exponent |
|---------|---------------|-------------------|
| C220101 (Blanket) | Volume × P_th | ~0.6 |
| C220102 (Shield) | Volume × P_th | ~0.6 |
| C220103 (Coils) | Conductor quantity (kA·m) | Geometric (not power-law) |
| C220104 (Heating) | Linear per-MW | 1.0 |
| C220105 (Structure) | Volume × P_et | ~0.5 |
| C220106 (Vessel) | Volume × P_et | ~0.6 |
| C220108 (Divertor) | P_th | ~0.5 |
| CAS23 (Turbine) | P_et × $/MW | 1.0 |
| CAS24-25 (Elec/Misc) | P_et × $/MW | 1.0 |
| CAS26 (Heat rejection) | P_th × $/MW | 1.0 |
| CAS27 (Special materials) | P_net | 1.0 |
| CAS40 (Owner's) | P_net | ~0.5 |
| CAS71 (O&M) | P_net | ~0.5 |

The current single α=0.6 applied to total LCOE is a weighted average of these
different exponents. The weighting depends on the concept's cost structure —
concepts dominated by CAS23 (BOP, exponent ~1.0) would scale differently than
concepts dominated by C220103 (coils, geometric).

## Concept Inventory

### Complete Scaling Status (all 19 concepts with models)

| ID | Name | Type | Native MWe | Needs Migration? |
|----|------|------|-----------|-----------------|
| 01 | HTS Compact Tokamak (CFS ARC) | costingfe | 261 | **YES** |
| 02 | Acoustic ICF / Sonofusion | freeform | ~1000 | No (freeform → keep α=0.6) |
| 03 | Laser ICF Liquid Jet Target | costingfe | 1000 | No (already at 1 GW) |
| 04 | Laser ICF | costingfe | 1000 | No (already at 1 GW) |
| 05 | Planar Coil Stellarator | costingfe | 390 | **YES** |
| 06 | Magnetic Mirror — Pale Blue (p-B11 CHARM) | costingfe | 500 | **YES** |
| 07 | MagLIF | costingfe | 1000 | No (already at 1 GW) |
| 08 | FRC w/ Direct Conversion | costingfe | 1000 (20×50) | No (already at 1 GW, modular) |
| 09 | QI Stellarator HTS | costingfe | 1000 | No (already at 1 GW) |
| 10 | Large-Scale Stellarator | costingfe | 1000 | No (already at 1 GW) |
| 11 | Magnetic Mirror — Realta (D-T CoSMo) | costingfe | 500 | **YES** |
| 12 | Levitated Dipole | freeform | varies | No (freeform → keep α=0.6) |
| 14 | Magnetized Target Fusion (Pneumatic) | costingfe | 300 | **YES** |
| 15 | Sheared-Flow Stabilized Z-Pinch | freeform | varies | No (freeform → keep α=0.6) |
| 17a | Laser ICF Hybrid Drive | costingfe | 400 | **YES** |
| 21 | Spherical Tokamak HTS | costingfe | 600 | **YES** |
| 22 | Projectile ICF | freeform | varies | No (freeform → keep α=0.6) |
| 28 | HTS Tokamak Full-HTS | costingfe | 500 | **YES** |
| 35 | PoloMac | freeform | varies | No (freeform → keep α=0.6) |

### Concepts Requiring Re-run (8 total)

These are all costingfe-backed concepts whose native power is NOT 1000 MWe. They
currently use the post-hoc α=0.6 `scaled_headline` and must be regenerated with the
dual-result pattern using `override_reference_mw`.

| ID | Name | Native MWe | Scale Factor (current α=0.6) |
|----|------|-----------|----------------------------|
| **01** | HTS Compact Tokamak (CFS ARC) | 261 | 0.58 (largest correction) |
| **05** | Planar Coil Stellarator | 390 | 0.69 |
| **06** | Magnetic Mirror — Pale Blue CHARM | 500 | 0.76 |
| **11** | Magnetic Mirror — Realta CoSMo | 500 | 0.76 |
| **14** | Magnetized Target Fusion (Pneumatic) | 300 | 0.63 |
| **17a** | Laser ICF Hybrid Drive | 400 | 0.70 |
| **21** | Spherical Tokamak HTS | 600 | 0.82 |
| **28** | HTS Tokamak Full-HTS | 500 | 0.76 |

**Test concept**: 01 (ARC at 261 MWe) — has the largest scaling correction and the
most thoroughly documented model. Run this first to quantify the LCOE delta before
migrating all 8.

### Concepts NOT Affected

| Category | IDs | Count | Reason |
|----------|-----|-------|--------|
| Costingfe, native 1 GW | 03, 04, 07, 08, 09, 10 | 6 | No scaling needed; template conditional skips `result_1gw` |
| Freeform | 02, 12, 15, 22, 35 | 5 | Keep post-hoc α=0.6 (no costingfe model to re-run) |

## Extraction Contract: How the Extractor Consumes `model_setup.py`

Understanding this contract is critical for knowing what `model_setup.py` must expose
vs. what the extractor computes live.

### Costingfe path (`extract_costingfe()`, extract_explorer_data.py:183-252)

The extractor **imports the module and operates on live objects**:

1. `module = load_module_from_path("model_setup.py")` — imports the script
2. `model = getattr(module, "model")` — grabs the `CostModel` instance
3. `result = getattr(module, "result")` — grabs the `ForwardResult`
4. `sensitivities = build_sensitivity_analysis(model, result)` — **extractor calls
   `model.sensitivity(result.params)` itself** (line 138). The module does NOT
   pre-compute sensitivities for the extractor.
5. `raw = dataclasses.asdict(result)` — flattens result to dict
6. If `scaled_headline` exists on module → override 3 fields in `raw`
7. `CostModelData.from_forward_result(raw, sensitivities)` → final output

**Key insight**: The module's job is to expose `model` and `result` (and optionally
`scaled_headline`). The extractor does all further computation (sensitivities, type
wrapping). The module is a data source, not a computation provider.

### Freeform path (`extract_standalone()`, extract_explorer_data.py:389-540)

The extractor **prefers pre-computed, falls back to live computation**:

1. Tries `module.compute_sensitivity()` (script-provided function)
2. Falls back to `_compute_sensitivity_from_params()` (central-difference perturbation)

Different pattern from costingfe — freeform scripts don't expose a reusable model
object, so the extractor can't call sensitivity on its own without the fallback.

### Implication for 1 GW integration

For costingfe concepts, the extractor should follow its established pattern:

1. `result_1gw = getattr(module, "result_1gw", None)` — grab live object
2. `sens_1gw = build_sensitivity_analysis(model, result_1gw)` — extractor computes
3. `CostModelData.from_forward_result(asdict(result_1gw), sens_1gw)` — wrap

**No `sens_1gw` module-level attribute needed.** The template only needs to produce
`result_1gw`. The extractor computes sensitivities live, consistent with how it
already handles the native `result`.

**`scaled_headline` becomes redundant** for migrated costingfe concepts — the
extractor can derive headlines directly from `result_1gw.costs`. But `scaled_headline`
should remain as backward compat for freeform concepts (which don't have `result_1gw`).

### Note: pre-existing inconsistency

`build_sensitivity_analysis()` (line 138) calls `model.sensitivity(result.params)`
**without** `cost_overrides`. But the scripts themselves compute sensitivities with
overrides for display (e.g., concept 01 line 439:
`model.sensitivity(result.params, cost_overrides=_NOAK_OVERRIDES)`). This means the
extractor's sensitivities may differ slightly from the script's printed output. This
is pre-existing and not introduced by this migration — but worth noting for a future
cleanup.

## Integration Design

### Dual-Result Pattern

For each costingfe `model_setup.py` not already at 1 GW, the template instructs
Claude to produce:

```python
# ── Shared parameters (avoid duplication) ────────────────────────
_SHARED_KWARGS = dict(
    availability=0.75,
    lifetime_yr=30,
    n_mod=1,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.0245,
    noak=True,
    R0=3.3,
    plasma_t=1.13,
    elon=1.84,
    # ... all engineering params ...
    cost_overrides=_NOAK_OVERRIDES,
)

# ── Native design point ─────────────────────────────────────────
result = model.forward(net_electric_mw=261.0, **_SHARED_KWARGS)

# ── 1 GW reference point ────────────────────────────────────────
result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=261.0,
    **_SHARED_KWARGS,
)
```

**Module-level interface contract** (what the extractor expects):
- `model` — `CostModel` instance (existing, unchanged)
- `result` — `ForwardResult` at native power (existing, unchanged)
- `result_1gw` — `ForwardResult` at 1000 MWe (NEW, `None`-equivalent if absent)
- `scaled_headline` — dict with 3 keys (KEEP for backward compat with freeform;
  for migrated costingfe concepts the extractor derives headlines from `result_1gw`
  instead, so `scaled_headline` becomes informational/print-only)

**No `sens_1gw` on the module.** The extractor computes it live via
`build_sensitivity_analysis(model, result_1gw)`.

For concepts already at 1 GW (03, 04, 07, 08, 09, 10): skip the `result_1gw` block
entirely. Template uses a conditional: "If the concept's native power is 1000 MWe,
do NOT add a second forward() call."

## Pipeline Change Inventory

The pipeline that generates `model_setup.py` is an agentic loop: prompt templates
are rendered with concept-specific variables, sent to Claude via `claude -p`, and the
output is validated and written to disk.

### Changes Required

#### 1. Cold-Start Prompt Template (costingfe)
**File**: `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
**Lines**: 47-68 (Power Standardization section)

**Current**: Instructs Claude to add the 5-line post-hoc `scaled_headline` block using
`_ALPHA = 0.6` and `result.power_table.p_net`.

**New**: Replace with instructions to:
- Factor all shared engineering kwargs into a `_SHARED_KWARGS` dict
- Call `model.forward(net_electric_mw=<native>, **_SHARED_KWARGS)` → `result`
- If native power ≠ 1000 MWe: call `model.forward(net_electric_mw=1000.0,
  override_reference_mw=<native>, **_SHARED_KWARGS)` → `result_1gw`
- `scaled_headline` may be kept for print output, but the extractor derives 1 GW
  headlines from `result_1gw` directly (no dependency on `scaled_headline` for
  migrated costingfe concepts)
- Do NOT compute `sens_1gw` in the script — the extractor calls
  `model.sensitivity(result_1gw.params)` itself (see Extraction Contract)
- If native power IS 1000 MWe: skip `result_1gw` entirely

#### 2. Cold-Start Prompt Template (freeform)
**File**: `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`
**Lines**: 47-72

**No change** — freeform concepts keep post-hoc α=0.6.

#### 3. Feedback Template (costingfe)
**File**: `prompt_templates/feedback/power_standardization_costingfe.md`

**Current**: Finding F-1 instructs Claude to add the post-hoc block. Explicitly
prohibits "duplicating forward()" and "adding result_native".

**New**: Rewrite F-1 to instruct adding `result_1gw = model.forward(...)` with
`override_reference_mw`. Remove the prohibition on a second forward() call. Keep the
prohibition on changing the native `result`. Do NOT instruct computing `sens_1gw` —
the extractor handles that.

#### 4. Feedback Template (freeform)
**File**: `prompt_templates/feedback/power_standardization_freeform.md`

**No change** — freeform keeps post-hoc approach.

#### 5. Extractor — full 1 GW data extraction
**File**: `exploration/concept_explorer/extract_explorer_data.py`

**Current** (`extract_costingfe()`, lines 183-252):
1. Imports module → grabs `model` and `result`
2. Calls `build_sensitivity_analysis(model, result)` — extractor computes live
3. If `scaled_headline` on module → overrides 3 headline fields in `raw`
4. Wraps in `CostModelData.from_forward_result(raw, sensitivities)`

**New**: After the existing native extraction, also check for `result_1gw`:

```python
result_1gw = getattr(module, "result_1gw", None)
if result_1gw is not None:
    sens_1gw = build_sensitivity_analysis(model, result_1gw)  # extractor computes live
    raw_1gw = dataclasses.asdict(result_1gw)
    # inject availability (same pattern as native, line 209-210)
    params_1gw = raw_1gw.get("params", {})
    if "availability" in params_1gw:
        raw_1gw.setdefault("power_table", {})["availability"] = params_1gw["availability"]
    cost_model_1gw = CostModelData.from_forward_result(raw_1gw, sens_1gw)
```

No need to read `sens_1gw` from the module — the extractor follows its established
pattern of calling `model.sensitivity()` live.

The `scaled_headline` backward-compat path remains for freeform concepts. For migrated
costingfe concepts, `scaled_headline` becomes informational (print output only) — the
extractor derives the 1 GW headline from `result_1gw` directly.

For freeform concepts (`extract_standalone` path): `cost_model_1gw` stays `None`.
The freeform `scaled_headline` post-hoc approach continues to override only the 3
headline fields as today.

#### 6. Explorer Data Model
**File**: `exploration/concept_explorer/models.py`

**Add `cost_model_1gw` field to `ConceptData`** (line ~345):

```python
class ConceptData(BaseModel):
    # ... existing fields ...
    cost_model: CostModelData | None = None       # Native design point (existing)
    cost_model_1gw: CostModelData | None = None   # 1 GW reference point (NEW)
```

This reuses the existing `CostModelData` type unchanged — it already carries all 36
CAS accounts, headline, sensitivities, and params. The 1 GW instance simply has
different values (p_net=1000, costs scaled per-account, sensitivities at 1 GW).

**`HeadlineEconomics`** — no change. The 1 GW instance's headline naturally has
`p_net_mw=1000`, `lcoe_per_mwh` and `overnight_cost_per_kw` from the model (not
post-hoc). `q_eng` and `capacity_factor` are recomputed at 1 GW.

**`CASAccount`** — no change. The `overridden` flag in the 1 GW instance reflects
which accounts had scaled overrides applied.

**`ConceptManifestEntry`** — no change. The manifest already carries the headline
`lcoe_per_mwh` which comes from `scaled_headline` (backward compat for freeform) or
from `cost_model_1gw.headline.lcoe_per_mwh` (for migrated costingfe concepts).

**JSON output shape** — `data/{id}.json` gains one new top-level key:
```json
{
  "concept_id": "01",
  "cost_model": { ... },          // native (261 MWe) — unchanged
  "cost_model_1gw": {             // NEW — full CostModelData at 1 GW
    "cas10": {"name": "Preconstruction", "cost_m_usd": 16.65, "overridden": false},
    "cas22": {"name": "Reactor Plant Equipment", "cost_m_usd": ..., "overridden": false},
    "cas22_detail": { ... },
    "headline": {
      "lcoe_per_mwh": ...,        // from result_1gw.costs.lcoe (NOT post-hoc)
      "overnight_cost_per_kw": ...,
      "p_net_mw": 1000.0,
      "q_eng": ...,               // recomputed at 1 GW
      "capacity_factor": 0.75
    },
    "sensitivities": { ... },     // computed by extractor via model.sensitivity()
    "params": { ... }             // result_1gw.params
  },
  ...
}
```

For freeform concepts and already-at-1GW costingfe concepts: `"cost_model_1gw": null`.

#### 7. Server / API
**File**: `exploration/concept_explorer/server.py`

**`/api/concepts/{id}`** — no change. Already returns the full `ConceptData` which
now includes `cost_model_1gw`. Pydantic serialization handles it automatically.

**`/api/manifest`** — no change. Manifest entries are built from `cost_model` (native),
not from `cost_model_1gw`.

**`POST /api/compute`** (slider recompute, lines 573-582) — **needs update**. Currently
`_forward_with_overrides()` re-runs the model at native power and returns a single
`CostModelData`. When sliders change, we also need to re-run at 1 GW with scaled
overrides to update `cost_model_1gw`.

Change: If the concept has a non-1GW native power, run a second
`_forward_with_overrides()` at 1000 MWe with `override_reference_mw=native_mw`,
compute sensitivities via `model.sensitivity()` on the 1 GW result (same live
pattern as the extractor), and return both in the response.

**Response shape change** for `/api/compute`:
```python
# Current:
class ComputeResponse(BaseModel):  # implicit — currently returns CostModelData directly
    ...

# New:
class ComputeResponse(BaseModel):
    cost_model: CostModelData           # native
    cost_model_1gw: CostModelData | None  # 1 GW (if applicable)
```

This is a breaking change to the compute endpoint. The frontend `concept_page.js`
slider handler must be updated to consume the new response shape.

#### 8. Frontend — Concept Detail Page
**File**: `exploration/concept_explorer/static/js/concept_page.js`
**File**: `exploration/concept_explorer/templates/concept.html.j2`

**CAS Breakdown section** (concept_page.js lines 450-455): Currently renders a single
CAS bar from `concept.cost_model`. Add a toggle to switch between native and 1 GW
views.

**Implementation**:
- Add a toggle button above the CAS breakdown: "Native (261 MWe) | 1 GW Reference"
- Default to 1 GW view when `cost_model_1gw` is present (this is the normalized
  comparison view)
- On toggle, re-render `renderCASBreakdown()` with CAS data from either
  `concept.cost_model` or `concept.cost_model_1gw`
- When `cost_model_1gw` is null (freeform or already-at-1GW), hide the toggle

**Headline card** (concept_page.js `renderHeadlineCard()`): Currently shows
`cost_model.headline`. When toggled to 1 GW, show `cost_model_1gw.headline` instead
(LCOE, overnight, p_net, q_eng).

**Tornado chart** (concept_page.js `renderTornado()`): Currently shows
`cost_model.sensitivities`. When toggled to 1 GW, show `cost_model_1gw.sensitivities`.

**Slider recompute** (concept_page.js slider handler): Currently POSTs to
`/api/compute` and updates `cost_model`. After the compute endpoint change, also
update `cost_model_1gw` from the response. Re-render whichever view is active.

#### 9. Frontend — Comparison Page
**File**: `exploration/concept_explorer/static/js/comparison.js`
**File**: `exploration/concept_explorer/static/js/view_capex.js`
**File**: `exploration/concept_explorer/static/js/view_summary.js`
**File**: `exploration/concept_explorer/static/js/view_sensitivity.js`

The comparison page uses a `VIEW_REGISTRY` pattern where each view plugin registers
`renderIntegrated()` and `renderLandscape()` functions.

**Option A — Add a "CAS @ 1 GW" view** (new view plugin):
- New file: `static/js/view_capex_1gw.js`
- Register as `window.VIEW_REGISTRY.capex_1gw`
- Identical to `view_capex.js` but reads from `concept.cost_model_1gw` instead of
  `concept.cost_model`
- Falls back to `concept.cost_model` when `cost_model_1gw` is null (freeform/native-1GW)
- Label: "CapEx @ 1 GW"
- Add `<script>` tag in `compare.html.j2`

**Option B — Add toggle to existing CapEx view** (modify view_capex.js):
- Add a "Native | 1 GW" toggle within the CapEx view header
- When toggled, re-render using `cost_model_1gw` data
- Simpler than a new view, but mixes two data sources in one plugin

**Recommendation**: Option A (new view plugin). Cleaner separation, consistent with
the registry pattern, and lets users compare "CapEx native" vs "CapEx @ 1 GW" in the
dual-panel integrated mode.

**Summary view** (`view_summary.js`): Currently shows headline economics table. Add
a column or row for 1 GW headline when available. Or add a separate "Summary @ 1 GW"
view.

**Sensitivity view** (`view_sensitivity.js`): Same pattern — add "Sensitivity @ 1 GW"
view plugin using `cost_model_1gw.sensitivities`.

#### 7. Edit Prompt Templates
**Files**:
- `prompt_templates/model_setup_costingfe_edit.md`
- `prompt_templates/model_setup_freeform_edit.md`

**Not changed for migration** — we're using cold-start re-generation (`--force`)
for the 8 affected concepts, not feedback-based edits. After migration, the
cold-start template handles all future generations correctly.

If desired later, the costingfe edit template could be updated to mention the
dual-result pattern for iterative refinement within the loop.

### No Changes Required

| Component | File | Why No Change |
|-----------|------|---------------|
| Loop orchestration | `scripts/lib/loop.py` | Template variables unchanged; `build_model_vars()` already passes all needed context |
| Concept classification | `scripts/lib/concepts.py` | costingfe vs. freeform mapping unchanged |
| Claude invocation | `scripts/lib/claude.py` | Same `claude -p` call, same retry/validation |
| CLI entry points | `scripts/run_analysis.py` | `cmd_model_setup()` unchanged |
| Validators | `scripts/lib/validators.py` | `validate_python_syntax` still applies |
| Finding extraction | `loop.py:extract_findings()` | F-1 finding format unchanged |
| Template rendering | `scripts/lib/templating.py` | Mustache substitution unchanged |

## Migration Plan

### Phase 0: Test on Concept 01 (ARC)
1. Manually add `result_1gw` to `analyses/01-hts-compact-tokamak/model_setup.py`
   using the dual-result pattern with `_SHARED_KWARGS` (no `sens_1gw` — extractor
   computes that live)
2. Run the script, compare:
   - Old scaled LCOE (post-hoc α=0.6) vs. new LCOE (from `result_1gw`)
   - Old scaled overnight $/kW vs. new
   - Full 1 GW CAS breakdown (new data, no old comparison)
3. Quantify the delta. If >15%, investigate whether it's the scaling or a bug.
4. Decide go/no-go for full migration.

### Phase 1: Data Model + Extractor
5. Add `cost_model_1gw: CostModelData | None = None` to `ConceptData` in `models.py`
6. Update `extract_costingfe()` in `extract_explorer_data.py`: check for `result_1gw`
   on module, call `build_sensitivity_analysis(model, result_1gw)` live, wrap in
   `CostModelData.from_forward_result()`
7. Run extractor on concept 01 (from Phase 0), verify `data/01.json` has
   `cost_model_1gw` with correct CAS values and sensitivities

### Phase 2: Template + Feedback Update
8. Update `model_setup_costingfe.md` lines 47-68 with dual-result instructions
   including `_SHARED_KWARGS` and conditional for 1 GW concepts (no `sens_1gw` —
   extractor computes that)
9. Rewrite `feedback/power_standardization_costingfe.md` F-1 finding

### Phase 3: Re-run All 8 Concepts
10. Cold-start re-generation:
    ```bash
    uv run python exploration/concept_analysis/scripts/run_analysis.py \
        model-setup 01 05 06 11 14 17a 21 28 --force
    ```
11. Run extractor on all 19 concepts, verify:
    - 8 migrated concepts have `cost_model_1gw` populated
    - 6 already-at-1GW concepts have `cost_model_1gw: null`
    - 5 freeform concepts have `cost_model_1gw: null`
12. Compare old vs. new LCOE for each of the 8 concepts (table of deltas)

### Phase 4: Server + Compute Endpoint
13. Update `POST /api/compute` response to return both `cost_model` and
    `cost_model_1gw` (see change #7 above)
14. Update `_forward_with_overrides()` to also recompute at 1 GW when applicable
15. Verify slider recompute returns both views

### Phase 5: Frontend — Concept Detail Page
16. Add native/1GW toggle to CAS breakdown section in `concept_page.js`
17. Wire toggle to also switch headline card and tornado chart between views
18. Update slider handler to consume new compute response shape (both `cost_model`
    and `cost_model_1gw`)
19. Hide toggle when `cost_model_1gw` is null

### Phase 6: Frontend — Comparison Page
20. Create `view_capex_1gw.js` — CAS breakdown view using `cost_model_1gw` data
21. Register in `comparison.js` VIEW_REGISTRY as `capex_1gw` ("CapEx @ 1 GW")
22. Add `<script>` tag in `compare.html.j2`
23. Optionally: create `view_sensitivity_1gw.js` for sensitivity comparison at 1 GW
24. Optionally: extend `view_summary.js` to show 1 GW headline alongside native

### Phase 7: Validate
25. Run full explorer, verify no regressions on existing views
26. Spot-check CAS breakdowns at 1 GW for reasonableness (concept 01 especially)
27. Verify freeform concepts (02, 12, 15, 22, 35) work correctly (no 1GW toggle)
28. Verify already-at-1GW concepts (03, 04, 07, 08, 09, 10) work correctly (no toggle)
29. Test slider recompute on a migrated concept — both views update
30. Test comparison page with mixed concepts (some with 1GW, some without)

## Expected LCOE Differences

The current α=0.6 post-hoc scaling is a single-exponent approximation of a
multi-exponent reality. The per-account scaling will produce different results because:

1. **Coil costs (C220103)** dominate ARC's cost — coils scale geometrically (conductor
   quantity in kA·m), not as P_net^0.6. For ARC at 261→1000 MWe, the costingfe model
   would compute the actual conductor requirement at the larger geometry, which may
   scale more or less favorably than α=0.6.

2. **BOP costs (CAS23-26)** scale approximately linearly with power (exponent ~1.0) —
   less favorable than α=0.6 when scaling UP, meaning per-account scaling would
   produce higher BOP costs at 1 GW than the single-exponent method.

3. **Economy-of-scale accounts (CAS40, CAS71)** use ~0.5 exponent — more favorable
   than α=0.6, partially offsetting BOP.

4. **Indirect costs (CAS30-50)** are fractional multipliers of direct costs, so they
   follow the direct cost scaling automatically.

Net effect depends on cost structure: concepts where CAS23-26 (BOP) is a large share
of total cost will see higher LCOE with per-account scaling. Concepts dominated by
economy-of-scale accounts (coils, buildings) may see lower LCOE.

Expect LCOE differences of 5-15% vs. current post-hoc values for concepts far from
1 GW (like ARC at 261 MWe). Concepts near 1 GW will see negligible differences.

## Code References

### 1costingfe (scaling feature)
- `src/costingfe/model.py:379` — `override_reference_mw` parameter on `forward()`
- `src/costingfe/model.py:793-840` — `_scale_overrides()` implementation
- `examples/scaled_overrides.py` — full working example (400→1000 MWe)

### fusion-tea — templates (CHANGE)
- `prompt_templates/model_setup_costingfe.md:47-68` — post-hoc template (replace)
- `prompt_templates/feedback/power_standardization_costingfe.md` — feedback F-1 (rewrite)

### fusion-tea — templates (NO CHANGE)
- `prompt_templates/model_setup_freeform.md:47-72` — freeform post-hoc (keep)
- `prompt_templates/feedback/power_standardization_freeform.md` — freeform F-1 (keep)

### fusion-tea — extractor (CHANGE)
- `concept_explorer/extract_explorer_data.py:212-217` — costingfe scaled_headline (extend)
- `concept_explorer/extract_explorer_data.py:434-440` — freeform scaled_headline (keep)

### fusion-tea — pipeline machinery (NO CHANGE)
- `scripts/lib/loop.py:624-682` — `build_model_vars()` template variable assembly
- `scripts/lib/loop.py:513-622` — `_run_model_in_iteration()` in-loop model generation
- `scripts/lib/concepts.py:79-101` — `get_model_path()` costingfe vs. freeform routing
- `scripts/lib/concepts.py:10-49` — `COSTINGFE_MAPPING` concept→model mapping
- `scripts/lib/claude.py:228+` — `invoke_claude_validated()` Claude invocation
- `scripts/run_analysis.py:467-544` — `cmd_model_setup()` standalone entry point

### fusion-tea — example model (test target)
- `analyses/01-hts-compact-tokamak/model_setup.py:216-224` — ARC post-hoc (Phase 0 test)

### Explorer data model (CHANGE)
- `models.py:~345` — `ConceptData`: add `cost_model_1gw: CostModelData | None = None`

### Explorer extractor (CHANGE)
- `extract_explorer_data.py:183-252` — `extract_costingfe()`: add `result_1gw` handling + live `build_sensitivity_analysis()` call
- `extract_explorer_data.py:132-153` — `build_sensitivity_analysis()`: reused as-is for 1GW (no change to function, just called twice)

### Explorer server (CHANGE)
- `server.py:573-582` — `POST /api/compute`: return both native and 1GW `CostModelData`

### Explorer frontend (CHANGE)
- `static/js/concept_page.js:450-455` — CAS section: add native/1GW toggle
- `static/js/concept_page.js` — headline card, tornado: wire to toggle
- `static/js/concept_page.js` — slider handler: consume new compute response shape
- `static/js/view_capex_1gw.js` — **NEW**: "CapEx @ 1 GW" comparison view plugin
- `static/js/comparison.js:54-58` — VIEW_REGISTRY: add `capex_1gw` entry
- `templates/compare.html.j2:~93` — add `<script>` for new view

### Explorer frontend (NO CHANGE)
- `static/js/cas_breakdown.js` — rendering component unchanged (just fed different data)
- `static/js/tornado.js` — rendering component unchanged
- `static/css/explorer.css` — reuse existing CAS_COLORS and dark theme

## Open Questions

1. **Should freeform concepts eventually get costingfe models?** That would give them
   proper scaling too, but is a larger modeling effort orthogonal to this integration.
