# Design Point Reasoning Trace — 05-planar-coil-stellarator

## 1. Sources walked

- `knowledge/concept_research/05-planar-coil-stellarator/dossier.md` — synthesized summary; used for orientation and machine identification
- `knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md` — Swanson et al. 2025 Helios overview paper (arXiv:2512.08027); Table 1 directly states 390 MWe net, 1,094 MW thermal, R=8 m, A=4.5, D-T fuel; also contains the speculative 25 T scaling note
- `knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-website-and-press.md` — confirms Eos as D-D neutron source with no electrical output, confirms Helios as first power plant
- `knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-doe-certification-jan2026.md` — DOE Milestone certification, January 13, 2026; independent expert confirmation of Helios physics and engineering basis
- `knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md` — hardware prototype paper; confirms REBCO but introduces no new P_native candidate
- `exploration/concept_analysis/analyses/05-planar-coil-stellarator/analysis.md` — existing D1+ analysis; used only to locate sources; design-point choice not inherited

## 2. Candidates surfaced

**Helios — 390 MWe net** (commercial pilot plant, preconceptual design)

Table 1 of arXiv:2512.08027 explicitly states: Net electric power = 390 MWe; Total thermal = 1,094 MW; Fusion power = 958 MW; thermal efficiency ~40%; D-T with LiPb breeding blanket; capacity factor 88%. Single-unit architecture (not multi-module). DOE Milestone-certified January 13, 2026 following independent expert review. P_native = 390 MWe.

**Helios speculative 25 T variant — ~1,000 MWe** (scaling note only, not a design)

Section 2 of the paper contains a parenthetical: "If, in the future, 25 T on-tape is found to be plausible, the field on-axis would be 7.5 T, the total fusion power would be 2.3 GW and the net electric power would be 1.0 GW." Explicitly labeled as contingent on undemonstrated tape performance. No geometry changes documented, no engineering architecture developed. Not a design point.

**Eos — no electrical output** (D-D neutron source demonstrator)

Thea's near-term demonstration device, operating D-D, designed to validate coil physics and produce ~0.2 g/day tritium. First plasma 2030. No electrical output by design. Does not qualify.

## 3. Selection

Helios is the only design with a published, engineered P_native. The 390 MWe figure traces directly to a complete thermal cycle documented in arXiv:2512.08027 Table 1.

```yaml
proposal:
  concept_id: 05-planar-coil-stellarator
  design_name: "Helios preconceptual design (Swanson et al. 2025, arXiv:2512.08027)"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 390
  primary_sources:
    - knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md
    - knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-doe-certification-jan2026.md
    - knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-website-and-press.md
  selection_rationale: |
    Helios is Thea Energy's only published fusion power plant design and the only candidate
    with a documented P_native. Table 1 of arXiv:2512.08027 states 390 MWe net electric
    output, derived from a complete thermal cycle: 1,094 MW total thermal × ~40% gross
    efficiency = 438 MWe gross − 48 MWe facility parasitic load = 390 MWe net. The design
    is a single-unit stellarator (not multi-module), so P_native is the full plant output.
    DOE Milestone certification (January 13, 2026) provides independent expert validation
    of the physics and engineering basis, making this the most externally reviewed design
    in the current concept batch.
  alternatives_considered:
    - design: "Helios speculative 25 T variant (~1,000 MWe)"
      reason_rejected: "scaling note only — no engineering design, no geometry changes documented; explicitly labeled hypothetical contingent on undemonstrated tape performance"
      sensitivity_implication: |
        If the 25 T variant were taken as a design point, P_native would rise roughly 2.5×
        → fewer modules at 1 GWe → 1 GWe LCOE would shift downward. Worth revisiting only
        if REBCO manufacturers publish demonstrated 25 T on-tape performance and Thea
        releases an engineering design around that operating point.
    - design: "Eos (D-D neutron source demonstrator)"
      reason_rejected: "no electrical output by design — demonstration device only"
      sensitivity_implication: "n/a — Eos has no P_native and cannot be a cost-projection target"
```

## 4. Open questions

- **No bottom-up cost account published.** LCOE targets ($150 → $60/MWh) are asserted without a supporting capital cost breakdown. Design-point selection is unaffected, but downstream LCOE projection will rely on analogue cost structures.
- **Eos physics validation (2030).** H_ISS04 = 1.4 (required for 958 MW fusion power) has never been demonstrated in any QA stellarator. If Eos demonstrates a materially lower H_ISS04, the Helios operating point may require a size increase — potentially shifting P_native upward. This is the most plausible trigger for a design-point re-selection.
- **25 T tape roadmap.** If REBCO manufacturers publish a demonstrated 25 T on-tape pathway and Thea releases an engineering design for the higher-field variant, the speculative ~1,000 MWe scenario becomes a genuine alternative and should displace this selection.
- **Eos electrical output question.** If Eos is later specified to include a power conversion system, it could become a pilot-demonstrator design point at a lower P_native. No electrical output is indicated in any current source.