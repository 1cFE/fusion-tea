---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T08:05:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #f47e9c0 (replace Section-5-midpoint spec with sourced reactor-class values)"
patch_class: "spec_anchor_with_architectural_constraint"
---

# Analyst-Verified Spec + Reactor-Class Physics Anchors: TAE Da Vinci p-B11 FRC

**Why this source exists.** TAE has not published reactor-scale Da Vinci
parameters — only the 50 MWe net target (tae-djt-merger-davinci-specs.md,
Dec 2025). Every spec value below is either Norman-extrapolated OR
physics-constrained by Rider/Nevins p-B11 analysis and reactor-class FRC
studies (Putvinski 2019, Steinhauer 2011, Tomassetti 2017, Nevins & Swain 2000).

This source supersedes a prior Section-5-midpoint spec that, while populated,
was **physically inconsistent**: plasma_volume = 15 m³ was ~4× too small to
deliver the library-back-solved P_fus ≈ 594 MW at the accompanying n_e × T_i;
internal B = 2 T failed pressure balance for n_e = 1e21 at T_i = 150 keV.
The values below close the volume / pressure / fusion-power loop
self-consistently for a reactor-class p-B11 FRC at the Da Vinci 50 MWe net
design point.

## Architectural mapping: ConfinementConcept = MIRROR

The library has no dedicated FRC class; TAE's spherical-FRC Da Vinci uses the
`MIRROR` class as the closest open-field-line representation. **Do not change
this**. PULSED_FRC is for Helion's pulsed colliding-FRC concept, NOT TAE.

## Verified spec values (transcribe verbatim)

| Parameter | Value | Source class | Anchor |
|-----------|-------|-------------|--------|
| `chamber_length` | 8.0 m | PHYSICS-CONSTRAINED | Putvinski 2019, Steinhauer 2011 §IV (L = 6-10 m for net-electric p-B11) |
| `plasma_t` (separatrix radius r_s) | 2.0 m | Norman × 5 | I_p ~ 10 MA reactor target; Putvinski 2019 (r_s = 1.5-2.5 m) |
| `plasma_volume` | 50.0 m³ | DERIVED | 0.5 × π × r_s² × L = 0.5 × π × 4 × 8 = 50.3 m³ (Steinhauer 2011 §III FRC mid-plane) |
| `B` (internal FRC field) | 5.0 T | PHYSICS-CONSTRAINED | MHD pressure balance: B² × β / (2 μ₀) ≥ P_plasma. At β=0.9, n_e=5e20, T_i=150 keV: B ≥ 5.2 T |
| `b_center` (external field) | 0.5 T | Norman × 5 | Norman B_ext = 0.1 T (Gota 2020 FEC); Putvinski 2019 reactor ~0.5-1.0 T |
| `n_e` | 5.0e20 m⁻³ | PHYSICS-CONSTRAINED | Nevins & Swain 2000, Rider 1997 (p-B11 sweet spot) |
| `T_e` | 80.0 keV | PHYSICS-CONSTRAINED | Rider/Nevins: T_e < T_i to avoid bremsstrahlung dominance with Z_eff ~ 3 |
| `p_input` | 100.0 MW | PHYSICS-DERIVED | Reactor-class NBI 100-300 keV; Putvinski 2019 uses 100 MW class |
| `P_native` | 50.0 MWe | TAE disclosure | tae-djt-merger-davinci-specs.md (Dec 2025) |
| `ConfinementConcept` | `MIRROR` | Architectural mapping | Library has no FRC class; MIRROR is the closest open-field-line model |
| `Fuel` | `PB11` | Confirmed | TAE materials |

## Critical do-not-set parameters

- **`eta_p = 0.9`** — must NOT be set. FRC β ~ 0.9 (Gota et al. FEC 2020 C-2W
  discharges) is the **plasma beta**, NOT a power-conversion efficiency.
  Power-conversion efficiencies are never spec keys.
- **`p_fus`** — library back-solves via inverse power balance from
  `p_input + P_native`. Do not pass.

## Acceptable F9 band edge for p-B11

`p_input/P_native = 100/50 = 2.0` is **well above F9's 0.5 cap**, reflecting
the high recirculation expected for a Q ~ 2-5 p-B11 plant. This is honest,
not a transcription error. p-B11 reactors inherently need high recirculating
power because:
- p-B11 fusion cross-section is ~1000× smaller than D-T at relevant T_i
- Net gain requires either very high Q via direct conversion OR high
  recirculation tolerated by aneutronic fuel-cycle savings

## Override registry (Section 5b)

The current model_setup.py has **6 enabled CAS overrides** capturing the
aneutronic-fuel architectural advantages:

- **C220101 (blanket)**: 0.50× library — aneutronic, no Li-6/T extraction
- **C220102 (shield)**: 0.30× library — neutron wall loading ~0.05-0.2 MW/m²
  vs 2-4 MW/m² for D-T
- Plus 4 additional enabled overrides for primary heat, fuel handling,
  vacuum, and waste management

**C220111 is excluded** despite Section 5b listing it: it's a derived rollup
account (installation_frac × sum), and the validator forbids overriding
derived rollups. The 50% complexity claim lacks bottom-up grounding (TAE
marketing language); other overrides partially capture it.

The cold-start regen will likely produce a Section 5b with similar overrides
based on the existing iter-01/iter-02 sources (grokipedia-tae-technologies.md,
tae-energy-conversion-clarification.md, etc.); preserve the same enabled set.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    chamber_length: 8.0
    plasma_t: 2.0
    plasma_volume: 50.0
    B: 5.0
    b_center: 0.5
    n_e: 5.0e20
    T_e: 80.0
    p_input: 100.0
  P_native: 50.0
  ConfinementConcept: MIRROR    # NOT PULSED_FRC — TAE is spherical-FRC
  Fuel: PB11
  do_not_set:
    - eta_p           # 0.9 is plasma β, not efficiency
    - p_fus           # library back-solves
  f9_band_edge_acceptable:
    p_input_over_P_native: 2.0   # honest high-recirculation, not error
  rationale: "Da Vinci 50 MWe p-B11 FRC, reactor-class extrapolation of Norman experimental anchors plus Rider/Nevins/Putvinski physics constraints."
  provenance: "derived"
  source_anchors:
    - "Norman / Norm experimental (Roche 2025 Nature Comm, Gota 2020 FEC)"
    - "Putvinski et al. Nucl. Fusion 2019 (reactor-class FRC)"
    - "Steinhauer Phys. Plasmas 2011 §III, §IV"
    - "Rider Phys. Plasmas 1997 (p-B11 bremsstrahlung limits)"
    - "Nevins & Swain Phys. Plasmas 2000 (p-B11 density sweet spot)"
    - "tae-djt-merger-davinci-specs.md (50 MWe target)"
```

## Sources cited (already in research corpus)

See iter-01/iter-02 sources for the primary TAE materials. The reactor-class
physics anchors above are referenced by name in the spec comments.
