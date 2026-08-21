# Design: Power Output Standardization for Cross-Concept Comparison

**Status:** Draft (revised — post-hoc scaling approach)
**Owner:** Reid W
**Created:** 2026-04-12 09:45 PDT
**Updated:** 2026-04-12
**Branch:** concept-power-standardization
**Commit:** e5a2cb2

## Overview

Standardize all 19 concept analysis models to produce 1000 MWe-normalized headline metrics (LCOE, overnight $/kW) for fair cross-concept comparison. Uses post-hoc economy-of-scale scaling (α=0.6) rather than re-running models at a different power level. Each model's physics, power balance, Q_eng, and CAS breakdown remain untouched at the concept's native design point.

## Related Artifacts

- **Spec:** `.project/active/power-standardization/spec.md`
- **Research:** `.project/research/20260412-power-standardization-consistency.md`
- **Prompt templates:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`, `model_setup_freeform.md`
- **Pipeline:** `exploration/concept_analysis/scripts/run_analysis.py` (line 467: `cmd_model_setup`), `scripts/lib/loop.py` (line 564: `build_model_vars`)
- **Extraction:** `exploration/concept_explorer/extract_explorer_data.py` (line 183: `extract_costingfe`, line 382: `extract_standalone`), `models.py` (line 87: `HeadlineEconomics`, line 266: headline construction)

## Research Findings

### Feedback Injection Mechanism

The standalone `model-setup` command (`cmd_model_setup` at `run_analysis.py:467`) calls `build_model_vars` without `model_feedback` — it defaults to `""`. The in-loop version (`loop.py:505`) explicitly passes feedback via `extract_model_findings()`.

Both prompt templates already have `{{#if model_feedback}}...{{/if}}` conditional blocks. The template machinery is fully wired — we just need to thread a feedback value through the standalone CLI path.

`extract_model_findings` (`loop.py:259`) parses finding blocks matching:
- Header: `### F-N:` (where N is a digit)
- Category line: `- **Category:** model` (regex: `FINDING_CATEGORY_RE` at `validators.py:24`)

### Extraction Contract

The concept explorer extraction has two pathways:

**Costingfe pathway** (`extract_costingfe`, line 183):
- Reads `module.model` and `module.result`
- Converts `result` to dict via `dataclasses.asdict()`
- Constructs `HeadlineEconomics` from `costs.lcoe`, `costs.overnight_cost`, `power_table.p_net`, `power_table.q_eng`
- Change needed: check for `module.scaled_headline` and override headline fields if present

**Standalone pathway** (`extract_standalone`, line 382):
- Reads `module.params` and `module.results`
- Uses `_freeform_to_explorer_dict()` (line 254) to map results → explorer dict
- HeadlineEconomics constructed from mapped dict in `CostModelData.from_forward_result()`
- Change needed: same — check for `module.scaled_headline` and override headline fields if present

Both pathways ultimately call `CostModelData.from_forward_result()` which constructs `HeadlineEconomics` at `models.py:266`. The override can happen either in the extraction functions (before `from_forward_result`) or after (patching the headline). Patching the raw dict before `from_forward_result` is cleanest — inject `scaled_headline` values into the `costs` and `power_table` dicts.

### Direct-Edit Triage

| ID | Concept | Trivial? | Detail |
|----|---------|----------|--------|
| 05 | Planar Coil Stellarator | **Yes** | No cost_overrides. Single forward() call. |
| 11 | Magnetic Mirror D-T | **Yes** | Explicit empty `cost_overrides={}`. Single forward() call. |
| 21 | Spherical Tokamak HTS | **Yes** | No cost_overrides. Single forward() call. |

All three are costingfe models with no power-dependent overrides. Adding `scaled_headline` is a ~5 line addition.

## Proposed Design

### Scaling Formula

All models use the same formula for per-unit metric normalization:

```python
_ALPHA = 0.6  # Economy-of-scale exponent (standard for fission/fusion)
_p_native = <net electric power from native result>  # MWe
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)  # < 1 for p < 1000 MWe

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": <native LCOE> * _factor,
    "overnight_per_kw": <native overnight $/kW> * _factor,
}
```

For ARC (261 MWe): factor ≈ 0.58, LCOE ~640 → ~370 $/MWh.
For a 1000 MWe concept: factor = 1.0.

### Component 1: Pipeline `--feedback` Flag (ALREADY IMPLEMENTED)

No changes needed. The `--feedback` CLI argument and threading through `cmd_model_setup` were completed in Phase 1. `extract_model_findings` was made public.

### Component 2: Synthetic Feedback Files (REWRITE)

**Purpose**: Version-controlled feedback directives that tell Claude to add a `scaled_headline` block. One per model type. These files already exist from Phase 1 but need content rewrite.

**Location**: `exploration/concept_analysis/prompt_templates/feedback/`

#### `power_standardization_costingfe.md`

```markdown
VERDICT: FINDINGS

### F-1: Add post-hoc scaling headline for 1000 MWe cross-concept comparison

- **Category:** model
- **Severity:** high
- **Description:** For cross-concept comparability, add a `scaled_headline` dict at
  module level with LCOE and overnight $/kW normalized to 1000 MWe using
  economy-of-scale post-hoc scaling.

  Required changes:
  1. Do NOT change `result = model.forward(...)` — keep it at the concept's native
     power level with all existing parameters and cost_overrides untouched.
  2. After the existing `result` computation, add a scaling block:
     ```python
     # Post-hoc scaling to 1000 MWe (cross-concept comparison)
     _ALPHA = 0.6  # economy-of-scale exponent
     _p_native = float(result.power_table.p_net)
     _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

     scaled_headline = {
         "p_net_mw": 1000.0,
         "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
         "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
     }
     ```
  3. Add a brief print line showing the scaled headline values for reference.
  4. Do NOT rename `result`, do NOT add `result_native`, do NOT duplicate forward().
  5. If the model has FOAK/NOAK scenario branches, only the primary `result` needs
     a `scaled_headline`. Scenario branches (e.g., `result_foak`) are informational.
```

#### `power_standardization_freeform.md`

```markdown
VERDICT: FINDINGS

### F-1: Add post-hoc scaling headline for 1000 MWe cross-concept comparison

- **Category:** model
- **Severity:** high
- **Description:** For cross-concept comparability, add a `scaled_headline` dict at
  module level with LCOE and overnight $/kW normalized to 1000 MWe using
  economy-of-scale post-hoc scaling.

  Required changes:
  1. Do NOT change `results` or any physics parameters — keep all computations at
     the concept's native power level. Do NOT change p_fus, rep_rate, n_mod, Q_sci,
     or any plasma physics parameters.
  2. After the existing `results` computation, add a scaling block:
     ```python
     # Post-hoc scaling to 1000 MWe (cross-concept comparison)
     _ALPHA = 0.6  # economy-of-scale exponent
     _p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
     _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
     _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native  # $/kW native

     scaled_headline = {
         "p_net_mw": 1000.0,
         "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
         "overnight_per_kw": _overnight * _factor,
     }
     ```
  3. Add a brief print line showing the scaled headline values for reference.
  4. Do NOT rename `results`, do NOT add `results_native`.
  5. `params` should remain the native physics parameters (unchanged).
```

### Component 3: Prompt Template Updates (FR-1)

**Purpose**: Ensure all future model generations include `scaled_headline`.

#### `model_setup_costingfe.md` — Replace current "Power Standardization" section

```markdown
## Power Standardization (CRITICAL)

All concept models MUST include a `scaled_headline` dict at module level for
cross-concept LCOE comparison at a normalized 1000 MWe reference.

- The primary `result = model.forward(...)` stays at the concept's **native** power
  level. Do NOT change `net_electric_mw` for standardization purposes.
- After the `result` computation, add:
  ```python
  _ALPHA = 0.6  # economy-of-scale exponent
  _p_native = float(result.power_table.p_net)
  _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

  scaled_headline = {
      "p_net_mw": 1000.0,
      "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
      "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
  }
  ```
- If the concept's native design point IS 1000 MWe, `scaled_headline` may be
  omitted (factor = 1.0, extractor falls through to native result).
- Cost overrides stay at their published/derived values — no re-derivation needed.
```

#### `model_setup_freeform.md` — Replace current "Power Standardization" section

```markdown
## Power Standardization (CRITICAL)

All concept models MUST include a `scaled_headline` dict at module level for
cross-concept LCOE comparison at a normalized 1000 MWe reference.

Since freeform models derive power from physics (not as an input), use post-hoc
cost scaling:

- Keep the physics-derived power balance EXACTLY as-is. Do NOT change p_fus,
  rep_rate, n_mod, Q_sci, or any plasma physics parameters.
- The module-level `results` stays at native power.
- After `results` computation, add:
  ```python
  _ALPHA = 0.6  # economy-of-scale exponent
  _p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
  _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
  _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native

  scaled_headline = {
      "p_net_mw": 1000.0,
      "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
      "overnight_per_kw": _overnight * _factor,
  }
  ```
- If the concept's native power IS 1000 MWe, `scaled_headline` may be omitted.
- Document the scaling exponent (α=0.6) in the script's docstring.
```

### Component 4: Direct Edits (FR-3)

**Concepts**: 05, 11, 21 (3 models, all costingfe, no cost_overrides)

**Pattern** (same for all three — ~5 lines added after existing `result`):

```python
# ── Post-hoc scaling to 1000 MWe (cross-concept comparison) ─────────────
_ALPHA = 0.6
_p_native = float(result.power_table.p_net)
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
    "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
}
```

Plus a print line:
```python
print(f"\nScaled headline (1000 MWe, α={_ALPHA}): LCOE {scaled_headline['lcoe_per_mwh']:.1f} $/MWh | "
      f"Overnight {scaled_headline['overnight_per_kw']:.0f} $/kW")
```

No changes to `result`, no duplicate `forward()`, no `result_native`.

**Specific files**:

| File | Native Power |
|------|-------------|
| `analyses/05-planar-coil-stellarator/model_setup.py` | 390 MWe |
| `analyses/11-magnetic-mirror/model_setup.py` | 500 MWe |
| `analyses/21-spherical-tokamak-hts/model_setup.py` | 600 MWe |

**Validation**: Run each with `uv run python model_setup.py` and confirm it prints the scaled headline without errors.

### Component 5: Feedback Iteration Execution (FR-4, FR-5)

**Concepts**: 10 models total (5 costingfe + 5 freeform)

**Execution command** (per concept group):

```bash
PIPELINE="exploration/concept_analysis/scripts/run_analysis.py"

# Costingfe concepts
uv run python $PIPELINE model-setup 01 06 14 17a 28 --force \
  --feedback exploration/concept_analysis/prompt_templates/feedback/power_standardization_costingfe.md

# Freeform concepts
uv run python $PIPELINE model-setup 02 12 15 22 35 --force \
  --feedback exploration/concept_analysis/prompt_templates/feedback/power_standardization_freeform.md
```

**Post-run validation** (per concept):
1. `uv run python analyses/{id}/model_setup.py` — must run without errors
2. Check stdout for scaled headline showing p_net = 1000 MWe
3. Check that `scaled_headline` dict exists at module level
4. Verify native `result`/`results` is unchanged (Q_eng, p_net at native power)

**Expected runtime**: ~15 min per concept. 10 concepts ≈ 2.5 hours sequential.

### Component 6: Verification of Existing 1000 MWe Concepts (FR-2)

**Concepts**: 03, 04, 07, 08, 09, 10

**Verification criteria** (per concept):
1. Module-level `result` (costingfe) or `results` (freeform) exists
2. `net_electric_mw=1000` in the forward() call (costingfe) or `results["power"]["p_net"]` ≈ 1000 (freeform)
3. For 08-FRC (20×50 MWe): confirm `p_net` in the result object is plant-level 1000 MWe

These concepts need no `scaled_headline` — the extractor falls through to native result which is already at 1000 MWe.

### Component 7: Extractor Support for `scaled_headline` (FR-7)

**File**: `exploration/concept_explorer/extract_explorer_data.py`

**Costingfe pathway** (`extract_costingfe`, ~line 192):

After `module = load_module_from_path(...)` and before `cost_model = CostModelData.from_forward_result(raw, ...)`:

```python
# Check for post-hoc scaling headline
scaled_headline = getattr(module, "scaled_headline", None)
if scaled_headline and isinstance(scaled_headline, dict):
    raw.setdefault("costs", {})["lcoe"] = scaled_headline.get("lcoe_per_mwh", raw.get("costs", {}).get("lcoe", 0))
    raw.setdefault("costs", {})["overnight_cost"] = scaled_headline.get("overnight_per_kw", raw.get("costs", {}).get("overnight_cost", 0))
    raw.setdefault("power_table", {})["p_net"] = scaled_headline.get("p_net_mw", raw.get("power_table", {}).get("p_net", 0))
```

**Standalone pathway** (`extract_standalone`, ~line 422):

After `loaded_module = load_module_from_path(...)`, check for `scaled_headline` on the module. The override needs to happen after `_freeform_to_explorer_dict()` produces `raw_dict` but before `from_forward_result()`:

```python
# After raw_dict is constructed, before from_forward_result:
sh = getattr(loaded_module, "scaled_headline", None)
if sh and isinstance(sh, dict):
    raw_dict.setdefault("costs", {})["lcoe"] = sh.get("lcoe_per_mwh", raw_dict.get("costs", {}).get("lcoe", 0))
    raw_dict.setdefault("costs", {})["overnight_cost"] = sh.get("overnight_per_kw", raw_dict.get("costs", {}).get("overnight_cost", 0))
    raw_dict.setdefault("power_table", {})["p_net"] = sh.get("p_net_mw", raw_dict.get("power_table", {}).get("p_net", 0))
```

Total: ~6 lines per pathway, ~12 lines total.

### Component 8: Re-extraction and Spot-Check (FR-6)

After all models and extractor are updated:

```bash
EXTRACT="exploration/concept_explorer/extract_explorer_data.py"

# Re-extract all concepts
uv run python $EXTRACT

# Verify headline p_net_mw for all concepts
uv run python -c "
import json
from pathlib import Path
data_dir = Path('exploration/concept_explorer/data')
for f in sorted(data_dir.glob('*.json')):
    if f.name in ('manifest.json', 'parameter_index.json'):
        continue
    d = json.loads(f.read_text())
    cm = d.get('cost_model')
    if cm:
        p = cm.get('headline', {}).get('p_net_mw', '?')
        lcoe = cm.get('headline', {}).get('lcoe_per_mwh', '?')
        print(f\"{d['concept_id']:>5s}  p_net={p:>8}  LCOE={lcoe:>8}\")
"
```

All concepts should show `p_net=1000.0` (or very close). LCOE should be in a reasonable range.

## Updated Triage

| Bucket | IDs | Count | Method |
|--------|-----|-------|--------|
| Verify only | 03, 04, 07, 08, 09, 10 | 6 | Read + confirm |
| Direct edit | 05, 11, 21 | 3 | Add `scaled_headline` block (~5 lines) |
| Feedback iteration (costingfe) | 01, 06, 14, 17a, 28 | 5 | `--feedback` + re-run model-setup |
| Feedback iteration (freeform) | 02, 12, 15, 22, 35 | 5 | `--feedback` + re-run model-setup |
| **Total** | | **19** | |

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Feedback-iterated models regress quality | Medium | Medium | Compare model before/after via git diff; review source citations |
| Economy-of-scale exponent (0.6) is wrong for some concepts | Low | Low | 0.6 is the standard fusion/fission exponent. Concept-specific deviations documented. Imprecision is accepted. |
| Claude ignores feedback directive | Low | Low | Validate: check for `scaled_headline` at module level. Re-run with `--force` if missing. |
| Extraction breaks with `scaled_headline` injection | Very low | Medium | Override happens on raw dict before `from_forward_result` — same data types, same code path. Easy to test. |
| Formula sign error | Very low | High | Verify: for p_native < 1000, factor must be < 1 (LCOE drops when scaling up). Print and inspect. |

## Integration Strategy

- **`result`/`results` untouched**: All existing extraction, sensitivity, CAS breakdown logic is unaffected. The only change is headline metrics.
- **`scaled_headline` is optional**: If absent, extractor falls through to native result. Zero impact on 1000 MWe concepts or any concept without the dict.
- **Prompt templates**: Additive section. No impact on existing pipeline behavior for concepts not being regenerated.
- **`--feedback` CLI flag**: Already implemented. Optional argument, default=None.
- **Concept explorer frontend**: No changes needed. Shows whatever HeadlineEconomics contains.

## Validation Approach

### Per-Model Validation
1. `uv run python model_setup.py` exits cleanly
2. `scaled_headline` dict exists at module level with `p_net_mw=1000.0`
3. `scaled_headline["lcoe_per_mwh"]` < native LCOE for concepts with p_native < 1000
4. Native `result`/`results` unchanged (Q_eng, p_net at native power)

### Cross-Concept Validation
1. Re-extract all 19 concepts with updated extractor
2. All headline `p_net_mw` values = 1000.0
3. LCOE values are in a plausible range (no order-of-magnitude outliers)
4. Explorer comparison view shows consistent p_net across all concepts

### Regression Check
1. Explorer loads without errors
2. Comparison views render correctly
3. Sliders work for costingfe concepts (live recomputation still uses `model.forward()` at native power)

---

Next Step: After approval → update plan
