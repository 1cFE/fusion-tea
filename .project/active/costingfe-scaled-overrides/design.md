# Design: Costingfe Scaled Overrides Integration

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-19
**Branch:** main

## Overview

Replace the post-hoc α=0.6 `scaled_headline` approach with 1costingfe's `override_reference_mw` for per-account scaling, producing full self-consistent `ForwardResult` objects at 1 GW for 8 costingfe concepts. The explorer defaults to 1GW data for all views.

## Related Artifacts

- **Spec:** `.project/active/costingfe-scaled-overrides/spec.md`
- **Research:** `.project/research/20260419-costingfe-scaled-overrides-integration.md`
- **Prior work:** `.project/active/power-standardization/` (approach being replaced)

---

## Design Decision: Where 1GW Data Lives

The spec proposed adding a `cost_model_1gw` field to `ConceptData` and updating all frontend code to prefer it. After investigating the full data flow, there's a significantly simpler approach.

### Decision: Put 1GW data directly in `cost_model`

When `result_1gw` exists on a module, the extractor builds `CostModelData` from `result_1gw` (with 1GW sensitivities) and puts it in `cost_model`. No new field. No frontend changes.

**Why this works:**

1. **Zero frontend changes** — `concept_page.js`, all comparison views (`view_capex.js`, `view_summary.js`, `view_sensitivity.js`), index page, and tornado chart all read from `concept.cost_model` already. They automatically show 1GW data.

2. **Zero manifest changes** — `build_manifest()` reads `concept.cost_model.headline.lcoe_per_mwh` (line 660). Comparison page LCOE is automatically at 1GW.

3. **Zero parameter index changes** — `build_parameter_index()` reads `concept.cost_model.sensitivities` (line 698-702). Whisker ranges automatically reflect 1GW sensitivities.

4. **Sliders unaffected** — `POST /api/compute` loads `model_setup.py` directly and calls `_forward_with_overrides(model, result.params, overrides)`. It doesn't read from the JSON `cost_model`. Sliders continue operating on the native `result`.

5. **Native data not lost** — the native `result` is still the primary module-level export in `model_setup.py`. Re-extraction can recover native data anytime. The module IS the authoritative source, not the JSON.

**What changes vs. the spec:**

| Spec proposed | Design uses |
|---|---|
| New `cost_model_1gw` field on `ConceptData` | No new field — `cost_model` carries 1GW data |
| Frontend reads `cost_model_1gw ?? cost_model` | Frontend unchanged — reads `cost_model` |
| Comparison views updated | Comparison views unchanged |
| Manifest builder updated | Manifest builder unchanged |

---

## Proposed Design

### Component 1: Extractor Changes

**File:** `exploration/concept_explorer/extract_explorer_data.py`

#### `extract_costingfe()` (lines 183-253)

Current flow:
1. Load module → grab `model`, `result`
2. `build_sensitivity_analysis(model, result)` → sensitivities at native power
3. `raw = dataclasses.asdict(result)` → dict at native power
4. If `scaled_headline` on module → override 3 fields in `raw`
5. `CostModelData.from_forward_result(raw, sensitivities)`

New flow:
1. Load module → grab `model`, `result`
2. Check `result_1gw = getattr(module, "result_1gw", None)`
3. **If `result_1gw` exists:**
   - `build_sensitivity_analysis(model, result_1gw)` → sensitivities at 1GW
   - `raw = dataclasses.asdict(result_1gw)` → dict at 1GW
   - Inject availability into `raw["power_table"]` (same pattern as native, line 209-210)
   - `CostModelData.from_forward_result(raw, sensitivities_1gw)`
4. **If `result_1gw` absent:**
   - Use native `result` as today (no `scaled_headline` injection — that's removed)
   - For already-at-1GW concepts, native result IS the 1GW result

**Remove:** The `scaled_headline` injection block in `extract_costingfe()` (lines 208-217). Costingfe concepts no longer use `scaled_headline`.

**Keep:** The `_apply_scaled_headline()` path in `extract_standalone()` (lines 435-440) — freeform concepts still use it.

#### Sensitivity for 1GW result

`build_sensitivity_analysis(model, result_1gw)` (line 132-153) calls `model.sensitivity(result_1gw.params)`. This produces elasticities at the 1GW operating point. Same function, different input — no changes to `build_sensitivity_analysis()` itself.

Note: the pre-existing issue where `build_sensitivity_analysis` doesn't pass `cost_overrides` applies equally to the 1GW path. Not addressed here.

**`result_1gw.params` semantics:** The `ForwardResult` returned by `model.forward(..., override_reference_mw=...)` carries the 1GW parameter set in its `.params` attribute — including `net_electric_mw=1000.0` and the scaled override values — so `build_sensitivity_analysis(model, result_1gw)` evaluates elasticities at the 1GW operating point.

### Component 2: Prompt Template Changes

**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`

Replace the "Power Standardization" section (lines 47-68) with dual-result instructions:

**New instructions (replacing lines 47-68):**

```markdown
## Power Standardization: Dual-Result Pattern

The primary `result = model.forward(...)` stays at the concept's **native** power
level. This preserves physics consistency (Q_eng, power balance, CAS breakdown).

**If the concept's native design point is NOT 1000 MWe**, add a second forward()
call to produce a self-consistent 1 GW result using per-account cost scaling:

1. Factor all shared kwargs into a `_SHARED_KWARGS` dict (avoid duplicating
   parameters between the two forward() calls):

   ```python
   _SHARED_KWARGS = dict(
       availability=...,
       lifetime_yr=...,
       # ... all engineering params, cost_overrides, noak, etc.
   )
   ```

2. Compute both results:

   ```python
   result = model.forward(net_electric_mw=<native_power>, **_SHARED_KWARGS)

   result_1gw = model.forward(
       net_electric_mw=1000.0,
       override_reference_mw=<native_power>,
       **_SHARED_KWARGS,
   )
   ```

   `override_reference_mw` tells the framework that `cost_overrides` values are
   valid at `<native_power>` MWe, and it should scale them to 1000 MWe using
   per-account scaling laws.

3. Both `result` and `result_1gw` MUST be module-level variables (not inside a
   function or if-block).

4. Do NOT add `scaled_headline`. Do NOT compute sensitivities for `result_1gw`
   — the extraction pipeline handles that.

**If the concept's native design point IS 1000 MWe**, do NOT add `result_1gw`.
A single `result` at 1000 MWe is sufficient.
```

**Template variable needed:** The template already has `{{net_electric_mw}}` available via `build_model_vars()` in `scripts/lib/loop.py:624-682`. The conditional ("if not 1000 MWe") is in the prompt instructions for Claude to follow, not a Mustache conditional — same pattern as the current `scaled_headline` instructions.

### Component 3: Cleanup — Remove `scaled_headline` from Costingfe Models

After re-generation, the 8 re-run concepts will not have `scaled_headline` (the new template doesn't produce it). The 6 already-at-1GW concepts never had `scaled_headline` (they were exempt). So after re-run, no costingfe model will have `scaled_headline`.

The `scaled_headline` injection code in `extract_costingfe()` (lines 208-217) should be removed to keep the code honest — it would be dead code after migration.

### Component 4: Model Re-generation

**Command (from prior work pattern):**
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py \
    model-setup 01 05 06 11 14 17a 21 28 --force
```

This is the same `--force` cold-start approach used in the power-standardization work. The `--force` flag bypasses the `model_setup.py` existence check and regenerates from the updated template.

**8 concepts to re-run:**

| ID | Name | Native MWe |
|----|------|-----------|
| 01 | HTS Compact Tokamak (ARC) | 261 |
| 05 | Planar Coil Stellarator | 390 |
| 06 | Magnetic Mirror p-B11 | 500 |
| 11 | Magnetic Mirror D-T | 500 |
| 14 | MTF Pneumatic (GF) | 300 |
| 17a | Laser ICF Hybrid (Xcimer) | 400 |
| 21 | Spherical Tokamak HTS | 600 |
| 28 | HTS Tokamak Full-HTS | 500 |

**Per-concept validation (same pattern as prior work):**
- `uv run python model_setup.py` runs without error
- Module exposes `result` (native) and `result_1gw` (1GW)
- No `scaled_headline` attribute
- LCOE from `result_1gw.costs.lcoe` is reasonable (compare to old post-hoc value)

### Component 5: Phase 0 — Manual Test on Concept 01

Before updating the template and running all 8, manually edit `analyses/01-hts-compact-tokamak/model_setup.py` to add the dual-result pattern:

```python
# After the existing result = model.forward(net_electric_mw=261.0, ...) block:

result_1gw = model.forward(
    net_electric_mw=1000.0,
    override_reference_mw=261.0,
    # ... same kwargs as result ...
)
```

Run it, compare:
- Old post-hoc LCOE (from `scaled_headline["lcoe_per_mwh"]`)
- New per-account LCOE (from `result_1gw.costs.lcoe`)
- Full 1GW CAS breakdown (new — inspect for reasonableness)
- Assert `result_1gw.params["net_electric_mw"] == 1000.0` — confirms the `ForwardResult` carries the 1GW parameter set, not the native 261 MWe values
- Assert `result_1gw.power_table.p_net` is ~1000 MWe

Expect 5-15% LCOE delta. Soft gate: proceed unless clearly broken.

### Component 6: Re-extraction and Validation

**Re-extract all 19 concepts:**
```bash
uv run python exploration/concept_explorer/extract_explorer_data.py
```

**Validation script (same pattern as prior work):**
```python
# Verify all concepts show 1000 MWe in cost_model headline
import json
from pathlib import Path
data_dir = Path("exploration/concept_explorer/data")
for f in sorted(data_dir.glob("*.json")):
    if f.name in ("manifest.json", "parameter_index.json"):
        continue
    d = json.loads(f.read_text())
    cm = d.get("cost_model")
    if cm:
        p = cm["headline"]["p_net_mw"]
        lcoe = cm["headline"]["lcoe_per_mwh"]
        print(f"{d['concept_id']:>3s}  p_net={p:.0f}  lcoe={lcoe:.1f}")
```

**Expected results:**
- 8 migrated concepts: `p_net=1000`, LCOE from per-account scaling
- 6 already-at-1GW: `p_net=1000`, LCOE unchanged (no `result_1gw`, native is 1GW)
- 5 freeform: `p_net=1000`, LCOE from post-hoc `scaled_headline` (unchanged)

---

## Potential Risks

1. **`override_reference_mw` produces unexpected costs** — Mitigated by Phase 0 test on concept 01. Per-account scaling is physically grounded; single-exponent was the approximation.

2. **Claude doesn't follow dual-result template** — The `_SHARED_KWARGS` pattern is more complex than the old 5-line `scaled_headline` block. Mitigated by clear template instructions and the `--force` cold-start (Claude sees the full template, not a feedback patch).

3. **Sensitivity differences at 1GW** — Parameter importance changes at different scales. This is correct behavior, not a bug. Tornado charts will show different rankings than before.

4. **Freeform/costingfe parity** — Freeform concepts keep post-hoc α=0.6 while costingfe concepts get per-account scaling. This is an inherent limitation (freeform has no costingfe model to re-run). Acceptable given the user's scoping decision.

## Integration Strategy

This replaces the output of `.project/active/power-standardization/` (post-hoc scaling). The prior work introduced:
- `scaled_headline` in all 19 `model_setup.py` files
- `scaled_headline` injection in the extractor
- Template instructions for `scaled_headline`

This work:
- Removes `scaled_headline` from costingfe models and extractor (costingfe path)
- Keeps `scaled_headline` in freeform models and extractor (standalone path)
- Replaces template instructions with dual-result pattern
- Uses the same `--force` re-run and re-extraction workflow

## Validation Approach

1. **Phase 0**: Manual test on concept 01 — compare old vs. new LCOE, inspect CAS breakdown
2. **Per-concept**: Each re-generated model runs without error, exposes `result_1gw`
3. **Cross-concept**: All 19 concepts re-extracted, all show `p_net=1000` in `cost_model.headline`
4. **Explorer regression**: Start server, browse concept pages and comparison views, verify no errors
5. **LCOE sanity**: Tabulate old vs. new LCOE for all 8 migrated concepts, flag any >20% delta for investigation

---

**Next Step:** After approval → `/_my_plan`
