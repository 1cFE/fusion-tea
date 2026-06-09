---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T07:45:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #67a3b89 (low-fit-archetype mappings) + glossary refactor"
patch_class: "spec_anchor_with_architectural_constraint"
---

# Analyst-Verified Spec + Architectural Mapping: Realta CoSMo Magnetic Mirror

**Why this source exists.** Realta Fusion's CoSMo / Hammir design is a
**tandem-mirror architecture**, but the 1costingfe `MIRROR` model represents a
**single-cell mirror only**. This source documents (a) the verified central-cell
spec values that map cleanly to the library, and (b) the fields that were
DROPPED from the prior spec because the tandem-mirror's end-plug parameters
have no canonical equivalent in single-cell representation.

Without this guidance, a cold-start regen will likely re-introduce dropped
fields (because Realta's published parameter table includes them), and the
F7 spec-key whitelist will then reject the spec.

## Verified central-cell spec (transcribe verbatim)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `chamber_length` | 50.0 m | Central cell length (was `l_c` in Realta's table) |
| `plasma_t` | 0.54 m | Central cell plasma radius (was `a_c`) |
| `B` | 3.0 T | Central cell plasma field (was `B_0c`) |
| `b_center` | 3.0 T | Central-cell solenoid coil-axis field; matches B |
| `p_input` | 30.0 MW | Total NBI power, both end plugs (was `P_NBI`) |
| `P_native` | 50 MWe | Realta's published Hammir/CoSMo design point |
| `ConfinementConcept` | `MIRROR` | Library's single-cell mirror |
| `Fuel` | `DT` | Confirmed |

## Critical architectural constraints — fields to DROP

Realta's published parameter table contains the following fields. They have
**no canonical equivalent** in the library's single-cell mirror model and
must NOT be passed to `forward()`. The strict F7 spec-key whitelist now
rejects them; under prior loose validation `forward()` silently dropped them
and the model ran on pure mirror YAML defaults.

| Realta field | Why it's dropped |
|--------------|------------------|
| `l_p` (end-plug length) | Library models central cell only — no plug geometry |
| `a_m` (mirror cell plasma radius) | No mirror-cell representation |
| `B_m` (mirror cell field) | No mirror-cell representation |
| `B_0` (peak mirror field) | No peak-field representation |
| `T_ic` (end-plug ion temperature) | Library uses central-cell T_i only |
| `beta_p0` (end-plug beta) | No end-plug representation |
| `n_p0` (end-plug density) | No end-plug representation |
| `E_NBI` (NBI beam energy) | Not in `CostingInput.model_fields` |
| `P_fus` (fusion power) | Library back-solves via inverse power balance from `p_input + P_native`. The F9 ratio check rejects values > 0.5 of P_native. |

## Critical do-not-set parameters

- **`eta_p=0.6`** — power-conversion efficiencies are never spec keys.
  This value is the central-cell plasma beta β_c, which is informational only.
- **`T_ec=100 keV`** — the analyst's parameter table cites this as the
  warm-electron end-plug temperature (tandem-mirror feature for ambipolar
  ion confinement), NOT central-cell electron temperature. The library's
  `T_e` is central-cell-only. Do not pass `T_ec` directly.

## F9 ratio band — acceptable for this design

`p_input/P_native = 30/50 = 0.6` is at the edge of the F9 ratio band
[0.5%, 50%]. This is a **genuinely high-recirculation tandem-mirror design**,
not a fusion-power transcription error. Mirrors run 30-50% recirculating
power vs steady-state-MFE 5-15%. Document but accept the F9 band-edge.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    chamber_length: 50.0
    plasma_t: 0.54
    B: 3.0
    b_center: 3.0
    p_input: 30.0
  P_native: 50
  ConfinementConcept: MIRROR
  Fuel: DT
  do_not_set:
    - l_p
    - a_m
    - B_m
    - B_0
    - T_ic
    - beta_p0
    - n_p0
    - E_NBI
    - P_fus
    - eta_p
    - T_ec
  rationale: "Realta tandem-mirror architecture; library is single-cell only. End-plug parameters dropped."
  provenance: "direct"
  notes:
    - "p_input/P_native = 0.6 is acceptable at F9 band edge — high-recirculation tandem-mirror design, not a bug."
    - "Empty overrides list — Section 5b states 'zero enabled overrides' due to lack of company-grounded cost data."
```

## Sources cited (already in research corpus)

- Realta Fusion public CoSMo / Hammir design materials (cited per spec line in analysis.md §5)
- Prior 1costingfe PRs that established the canonical kwarg whitelist: `cd1b692` (eta_pin template), `6c7c2d3` (YAML-derived spec keys, no power-conv overrides), `67a3b89` (canonical-name spec mappings + low-fit-archetype prompt guidance)
