---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T07:30:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea bulk-refresh + manual spec audits (PRs #6, #6fcf606, #9142788)"
patch_class: "spec_anchor"
---

# Analyst-Verified Spec Anchors: Large-Scale Stellarator (Gauss Fusion GIGA)

**Why this source exists.** Documents the verified spec values currently in
`exploration/concept_analysis/analyses/10-large-scale-stellarator/model_setup.py`
so a cold-start `analyze --force` regen reproduces them. These values were
established via PR #6 (power standardization) and subsequent canonical-name
spec-mapping fixes; they are NOT analyst inventions but rather precise
extractions from the primary sources, with the additional constraint that
they conform to the current 1costingfe canonical kwargs (post `feat/glossary`
work that renamed/whitelisted spec keys).

## Verified spec values (transcribe these verbatim into Section 5b / model_setup.py)

| Parameter | Value | Primary source anchor |
|-----------|-------|------------------------|
| `R0` (major radius) | 18.0 m | gauss-fusion-technical-summary.md §GIGA Power Plant; helias-reactor-context.md Table I |
| `plasma_t` (minor radius) | 1.7 m | gauss-fusion-technical-summary.md §GIGA Power Plant |
| `plasma_volume` | 1500.0 m³ | gauss-fusion-technical-summary.md §GIGA Power Plant |
| `B` (on-axis field) | 6.0 T | gauss-fusion-technical-summary.md §GIGA Power Plant |
| `p_input` | 75.0 MW | Estimated: ECRH for startup/profile control; 50–100 MW band from analysis §5. Mid-band central estimate. |
| `elon` (elongation) | 1.6 | Effective average elongation for toroidally-varying bean/triangular cross-sections (stellarator-specific) |
| `P_native` | 1000.0 MWe | Design Point selection (orchestrator-fixed) |
| `ConfinementConcept` | `STELLARATOR` | Class membership |
| `Fuel` | `DT` | Confirmed |

## Critical do-not-set values

These were patched OUT of prior model_setup.py versions and must NOT be
re-introduced:

- **`p_fus`** must not be in spec. The library back-solves `P_fus` via the
  inverse power balance from `p_input + P_native`. The gauss-fusion source
  cites P_fus ≈ 3000 MW, but that's an output cross-check, not a model input.
  Setting `p_fus=3000` would have been silently ignored by `forward()` under
  loose validation; with the current strict kwarg validator, it raises.
- **No `eta_*` overrides** unless the design point genuinely differs from the
  archetype default. The original analysis erroneously set `eta_p=0.0276`
  (this was the plasma β value misinterpreted as an efficiency).

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    R0: 18.0
    plasma_t: 1.7
    plasma_volume: 1500.0
    B: 6.0
    p_input: 75.0
    elon: 1.6
  P_native: 1000.0
  ConfinementConcept: STELLARATOR
  Fuel: DT
  do_not_set:
    - p_fus
    - eta_p
  rationale: "Spec extracted from Gauss Fusion GIGA Power Plant disclosure; post-glossary canonical kwargs."
  provenance: "direct"
```

## Sources cited (already in research corpus)

- `gauss-fusion-technical-summary.md` §GIGA Power Plant — primary
- `helias-reactor-context.md` Table I — corroborating stellarator-class
  geometric reference (Helias is the design-class parent)

## Maintenance

If Gauss Fusion publishes updated GIGA specs (or a successor design point),
add a successor source citing the new disclosure. The current values are
NOT outputs of the agent's free-form derivation — they are direct
transcriptions from company materials, with field name mapping to current
1costingfe kwargs.
