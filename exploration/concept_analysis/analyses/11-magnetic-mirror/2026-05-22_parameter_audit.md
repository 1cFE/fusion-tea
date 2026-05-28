# Parameter Audit — Realta Fusion (Concept 11)

**Date:** 2026-05-22
**Author:** Reid (session-driven review with Claude)
**Scope:** Audit of `model_setup.py` inputs against arXiv:2411.06644 and other ingested sources
**Status:** Findings for review; no edits applied to model_setup.py yet

---

## Why this report exists

While walking through the costing inputs for Realta's CoSMo / Hammir model, an explicit Hammir pilot operating point in arXiv:2411.06644 (line 300 of the extracted source, paper §3.2) was surfaced that **directly anchors five of our parameters** — but the model currently uses values that diverge from this anchor in several places. In addition, an internal inconsistency between the geometry-sizing block and the power-balance block was identified: the two blocks are implicitly assuming different "MW per meter" rates, producing a ~3× discrepancy in implied fusion power between geometry and power balance.

This report documents the findings so they can be reviewed before re-running the analysis or model.

---

## The anchor passage (arXiv:2411.06644, line 300 of extracted source)

> "Assuming neutral beam efficiencies $\eta_{NBI} = 60\%$, an electrical conversion efficiency $\eta_{ele} = 50\%$ assuming the use of a Brayton cycle, a blanket neutron energy multiplication factor $C_{mult} = 1.1$, and $P_{NBI} = 30$ MW into the end plugs; it was found a tandem mirror would need to produce $157.4$ MW of fusion power to satisfy the NASEM 50 MWe requirement."

This is a fully specified Hammir pilot recipe. It also implicitly uses **no DEC contribution** to reach 50 MWe — the thermal cycle alone gets there.

Plus, from the acknowledgments (line 473):

> "Realta is developing compact magnetic mirror fusion power plants as the low capital cost path to fusion power, and targeting initial fusion power plant deployment at the **100 – 200 MW scale** at industrial sites and datacenters for process heat and/or electricity."

This is the Realta-stated commercial deployment target. It is 2.5×–5× smaller than the model's 500 MWe native design point.

---

## 3. Summary of Issues, by Severity

### 🔴 Material Errors (will move LCOE noticeably)

1. **`_NATIVE_MW = 500`** — Realta's published deployment scale is 100–200 MW. Model is 2.5×–5× too large. The 1 GWe scaling variant is even more divorced from anything Realta has said.
   - Sources contradicted: arXiv §Acknowledgments (100–200 MW); APS DPP 2025 (Pe > 50 MWe pilot)
   - Current model justification: "MARS/MINIMARS LCOE saturates near ~600 MWe (1983 technology analogue)"

2. **`p_input = 40 MW`** — Paper explicitly uses 30 MW total NBI into both end plugs. 33% high.
   - Source contradicted: arXiv:2411.06644 §3.2 (line 300): "$P_{NBI} = 30$ MW into the end plugs"
   - Current model justification: "arXiv pilot: 30–40 MW; constant end-plug thesis" — note the upper bound was selected without a stated reason.

3. **`chamber_length = 70 m` justified by 7 MW/m claim** — Paper's actual 3.5–4 MW/m makes this length yield ~245 MWt, not ~490 MWt. The geometry sizing and the power balance use *inconsistent* MW/m assumptions inside the same model. See §4.
   - Sources contradicted: arXiv Table 3 (Optimum: 175 MW / 50 m = 3.5 MW/m; Alternate: 200 MW / 50 m = 4.0 MW/m); arXiv §3.2 POPCON example (157.4 MW / 50 m = 3.15 MW/m)
   - Current model justification: Fusion Report interview's ~7 MW/m claim (secondary source, marketing-grade)

### 🟡 Methodological Choices (defensible but worth flagging)

4. **`eta_th = 0.55`** — Project canonical override per `scoring_framework.md` §309 ("Hybrid (thermal+direct)" energy capture). Established 2026-04-29 for cross-concept comparability.
   - Paper's actual is 0.50 (Brayton cycle). Only ~10% high.
   - The override is a deliberate methodological choice to control conversion-cycle assumptions across concepts, **not an error in this concept's authoring**. Worth re-examining whether the canonical 0.55 for "Hybrid" is appropriate when the underlying paper uses 0.50.

5. **`eta_pin = 0.50`** — Paper has 0.60. Conservative by 17%.
   - Source: arXiv §3.2 (line 300): "$\eta_{NBI} = 60\%$"
   - Defensible if intent is to penalize unverified vendor claims, but should be stated explicitly if so.

### 🟢 Verified Against Paper / Physics

6. **`mn = 1.1`** — Direct match with arXiv's $C_{mult} = 1.1$.
7. **`f_dec = 0.20`** — Physics-fixed (D-T alpha energy fraction).
8. **`plasma_t = 0.75 m`** — Within arXiv Table 3 pilot range (a_c: 0.54–0.78 m).
9. **`cost_overrides = {}`** — Honest call. Only published cost signal is $50M REBCO tape for WHAM++, which cannot be extrapolated to commercial CAS22 without magnet geometry and current specs.

---

## 4. The Internal Inconsistency

The model has a silent inconsistency between its geometry block and its power-balance block.

**Geometry block** (sized for ~490 MWt fusion power):
- `chamber_length = 70 m`
- `plasma_t = 0.75 m`
- Implicit assumption: 7 MW/m × 70 m = 490 MWt
- Drives: blanket/shield/vessel volumes in CAS22, building footprint in CAS21

**Power-balance block** (back-solves to net 500 MWe at the model's efficiencies):
- `p_input = 40 MW`, `eta_th = 0.55`, `eta_pin = 0.50`, `eta_de = 0.54`, `f_dec = 0.20`
- Forced by `net_electric_mw = 500`
- Output reports: `Fusion: 1593 MW`

**The mismatch:**

| Block | Implied P_fus |
|---|---|
| Geometry (at 7 MW/m × 70 m) | ~490 MWt |
| Power balance (back-solve from 500 MWe) | ~1593 MWt |
| Ratio | **3.3×** |

The blanket / shield / vessel volumes in CAS22 are sized for the small machine; the fusion power, neutron load, and balance-of-plant cooling/recirculation are computed for the big one. The cost model uses geometry sizes for volume-based costs and power numbers for thermal/cooling costs, so the resulting LCOE blends two physically inconsistent operating points.

Either:
- the geometry needs to grow to be self-consistent at ~1593 MWt (would need ~230 m at 7 MW/m, or ~455 m at the paper's 3.5 MW/m), OR
- the power balance needs to settle at a smaller `net_electric_mw` consistent with the geometry's ~490 MWt × 0.55 thermal × (1 - recirc) ≈ ~200 MWe.

The second option happens to align with Realta's published 100–200 MW deployment target.

---

## 5. Recommended Re-anchoring

Two paths forward, depending on intent.

### Option A — Paper-faithful pilot baseline

Treat the model as a baseline of Realta's *actually-published* Hammir pilot, then run a separate scaled scenario if commercial extrapolation is wanted.

| Parameter | Current | Paper-anchored | Change |
|---|---|---|---|
| `_NATIVE_MW` | 500 MWe | ~100 MWe | mid of Realta's 100–200 MW deployment target |
| `chamber_length` | 70 m | 50 m | matches arXiv pilot |
| `p_input` | 40 MW | 30 MW | arXiv §3.2 line 300 |
| `eta_pin` | 0.50 | 0.60 | arXiv §3.2 line 300 |
| `eta_th` | 0.55 (canonical) | 0.50 OR keep 0.55 | judgment call — see issue #4 |
| `availability`, `mn`, `plasma_t`, `eta_de`, `f_dec` | as-is | as-is | already aligned |

### Option B — Consistent commercial extrapolation

Keep the 500 MWe native point but make the geometry consistent with the power balance and explicitly document the linear-scaling extrapolation as the dominant uncertainty.

- Set `chamber_length` to whatever the paper's 3.5 MW/m implies at the chosen P_fus (e.g., ~455 m for 1593 MWt, or shrink ambition to ~140 MWe net @ 70 m), OR
- Keep 70 m, drop `net_electric_mw` to match (~140–200 MWe).
- State the Realta interview's 7 MW/m claim as an additional sensitivity case rather than the baseline.

### Option C — Two design points (recommended discussion point)

Run both: a "paper-faithful 100 MWe pilot" and a "Realta-interview-claim 500 MWe extrapolation," and report both LCOEs with their respective sourcing. Makes the data-quality gradient visible to readers of the synthesis.

---

## How to apply changes

The pipeline-faithful way to act on these findings is to draft a feedback file and run:

```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 11 \
    --feedback exploration/concept_analysis/analyses/11-magnetic-mirror/feedback_2026-05-22_param_audit.md
```

A draft feedback file is not included here; see Appendix B for findings in roughly the format `address-review` consumes.

---

## Appendix A — All Default / Inherited Parameters in Current Model

These are parameters that the model_setup.py uses but that are **not** specifically derived from a Realta-anchored source — they come either from `costingfe`'s `steady_state_mirror.yaml` defaults, framework `costing_constants.yaml` D-T defaults, or canonical values from `scoring_framework.md`. Listed here for reviewer awareness because they collectively make up a large fraction of the cost basis.

### A.1 — Geometry defaults (from `steady_state_mirror.yaml`)

| Param | Value | Origin | What it drives |
|---|---|---|---|
| `R0` | 0.0 m | Mirror is cylindrical, not toroidal | No toroidal radius offset |
| `blanket_t` | 0.80 m | `steady_state_mirror.yaml` default | Blanket annular thickness → blanket volume → CAS22 blanket cost |
| `ht_shield_t` | 0.20 m | `steady_state_mirror.yaml` default | Hot shield thickness → volume → cost |
| `structure_t` | 0.15 m | `steady_state_mirror.yaml` default | Structural annulus thickness → volume → cost |
| `vessel_t` | 0.10 m | `steady_state_mirror.yaml` default | Vacuum vessel thickness → volume → cost |

**Implication:** Roughly 1.25 m of radial annulus material wraps around the 0.75 m plasma column over the full 70 m length. The cylindrical annular volume at outer radius (0.75 + 0.80 + 0.20 + 0.15 + 0.10) = 2.0 m is substantial — π × (2.0² − 0.75²) × 70 ≈ 755 m³ of layered material. None of this is anchored to a Realta-published blanket/shield/structure design.

### A.2 — Power-balance defaults

| Param | Value | Origin | What it drives |
|---|---|---|---|
| `eta_p` | 0.50 | `steady_state_mirror.yaml` default | Pumping efficiency |
| `f_sub` | 0.03 | `steady_state_mirror.yaml` default | BOP subsystem fraction of gross electric |
| `eta_de` | 0.54 | MARS 1983 analogue (not Realta-specific) | DEC efficiency on alpha channel |
| `eta_th` | 0.55 | Canonical override from `scoring_framework.md` §309 ("Hybrid") | Thermal cycle efficiency |
| `eta_pin` | 0.50 | "Blended NBI+ECH default" judgment (paper says 0.60 for NBI) | Heating wall-plug efficiency |

### A.3 — House loads

| Param | Value | Origin | Notes |
|---|---|---|---|
| `p_coils` | 8 MW | Elevated from default 5 MW (judgment, no Realta data) | Magnet ohmic / leads losses |
| `p_cryo` | 2 MW | Elevated from default 1 MW (judgment) | REBCO ~20 K cooling |
| `p_cool` | 22 MW | Elevated from default 20 MW (judgment) | First wall + blanket cooling |
| `p_pump` | 1.5 MW | `steady_state_mirror.yaml` default | Coolant pumping |
| `p_trit` | 10 MW | `steady_state_mirror.yaml` default | Tritium processing |
| `p_house` | 4 MW | `steady_state_mirror.yaml` default | Housekeeping / lighting |

None of A.3 has a Realta-published anchor. They are educated guesses that scale roughly with plant size.

### A.4 — Financial / lifecycle defaults

| Param | Value | Origin | Notes |
|---|---|---|---|
| `availability` | 0.85 | Canonical for MCF/SS/D-T per `scoring_framework.md` | No Realta target published |
| `lifetime_yr` | 30 | Standard fusion reference | Project canonical |
| `construction_time_yr` | 5.0 | `steady_state_mirror.yaml` default | Linear geometry argued simpler than toroid |
| `interest_rate` | 0.07 | Standard | Project canonical |
| `inflation_rate` | 0.02 | Standard | Project canonical |
| `noak` | True | NOAK plant assumption (not FOAK) | Project canonical |
| `n_mod` | 1 | One reactor module | n/a |

### A.5 — D-T fuel cycle defaults (from `costing_constants.yaml`)

These are applied automatically because `Fuel.DT` was selected. No Realta override is possible without explicit `cost_overrides`.

| Constant | Value | What it covers |
|---|---|---|
| `blanket_unit_cost_dt` | 0.60 M$/m³ | LiPb-grade breeding blanket per unit volume |
| `fuel_handling_dt_base` | 120 M$ at 1 GWe | Tritium processing facility (scales with plant size) |
| `remote_handling_dt_base` | 150 M$ at 1 GWe | Full remote handling suite for neutron-activated components |
| `licensing_cost_dt` | 5 M$ | NRC Part 30 licensing for D-T plants |
| `om_cost_dt` | 52 M$/yr at 1 GWe | Annualized neutron + tritium overhead |
| `decom_provision_dt` | 127 M$ at 1 GWe | Decommissioning sinking fund |

### A.6 — Inferred/derivative parameters with no Realta anchor

| Param | Value | Justification | Risk |
|---|---|---|---|
| `mn` | 1.1 | Matches arXiv's $C_{mult}$ — verified | none |
| `plasma_t` | 0.75 m | High end of arXiv Table 3 pilot range | low |

---

## Appendix B — Findings in feedback file format (draft)

Format: standard `analyze --feedback` consumable, max 3 findings per file. The material errors fit in a single file.

```markdown
VERDICT: REVISE

### F-1: Native design point inconsistent with Realta's published deployment target
**Target:** model_setup.py:72 `_NATIVE_MW = 500.0`; analysis.md §Section 5 net electrical output row
**Finding:** Realta's published commercial deployment target is 100–200 MW (arXiv:2411.06644 Acknowledgments, line 473). The model's 500 MWe native point and 1 GWe scaling variant are 2.5×–5× larger than any Realta-published target, and rest on a MARS 1983 LCOE-saturation analogue (~600 MWe) using fundamentally different magnet technology.
**Recommendation:** Either (a) re-baseline _NATIVE_MW to 100 MWe (mid of Realta's stated range) and run 200 MWe / 500 MWe as scenario variants with explicit extrapolation caveats, or (b) document the 500 MWe extrapolation as a forward-looking commercial scenario distinct from the Hammir pilot, and add a 100 MWe paper-faithful comparison point.
**Priority:** high

### F-2: p_input inflated above paper's explicit Hammir value
**Target:** model_setup.py:120 `p_input=40.0`; analysis.md §Section 5 "NBI+ECH input power" row
**Finding:** arXiv:2411.06644 §3.2 (paper text immediately following equation block, line 300 of extracted source) explicitly states "P_NBI = 30 MW into the end plugs" as the design assumption used to derive Hammir's 157.4 MW fusion / 50 MWe net operating point. The model uses 40 MW with the rationale "30–40 MW for 50 m pilot" — the 40 MW upper bound was selected without source justification.
**Recommendation:** Set p_input = 30 MW to match the arXiv anchor. If a higher value is desired to capture ECH contribution beyond NBI, document the breakdown explicitly and cite a source.
**Priority:** high

### F-3: chamber_length and 7 MW/m claim inconsistent with paper; geometry block disagrees with power-balance block by 3.3×
**Target:** model_setup.py:100 `chamber_length=70.0`; analysis.md §Section 2 Challenge 2; §Section 5 "Center cell fusion power scaling" row
**Finding:** The 70 m chamber length was sized to deliver ~490 MWt at the Fusion Report interview's "~7 MW per meter" claim. The arXiv paper's modeled rates are 3.5 MW/m (Optimum, 175/50) and 4.0 MW/m (Alternate, 200/50). At the paper's rates, 70 m yields ~245 MWt — half of what the geometry block assumes. Separately, the model's power-balance block back-solves to P_fus ≈ 1593 MWt to deliver 500 MWe, which would require ~455 m at 3.5 MW/m or ~230 m at 7 MW/m. The geometry block and power-balance block are internally inconsistent by a factor of ~3.3×.
**Recommendation:** Reconcile the two blocks. Either (a) shrink net_electric_mw to ~140–200 MWe so the implied P_fus matches the 70 m geometry at the paper's 3.5 MW/m, or (b) grow chamber_length to be self-consistent with the chosen net_electric_mw. Either way, treat the 7 MW/m interview claim as a sensitivity case rather than the baseline, and cite arXiv Table 3 / POPCON example as the primary anchor.
**Priority:** high
```
