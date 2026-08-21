# Design Point Reasoning Trace — 08-frc-w-direct-conversion

## 1. Sources walked

- `knowledge/concept_research/08-frc-w-direct-conversion/dossier.md` — synthesized summary; confirmed Orion as the named first commercial plant (50 MWe, under construction July 2025, 2028 Microsoft delivery), and Nucor 500 MWe partnership; flagged that Orion engineering specs are proprietary
- `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md` — ARPA-E presentation (DocsLib archive); provides the most explicit design-point quantitative data in the public record: 50 MW at 2 Hz, 40 T reactor target, η·Q = 0.2×1.2, magnetic recovery η=0.7
- `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md` — aggregated Helion website content; confirms 50 MWe Microsoft PPA (2028), Nucor 500 MWe partnership (2030 target), Polaris as 7th-generation prototype targeting net electricity demonstration, modular design philosophy
- `knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/contrary-research-helion.md` — Contrary Research company profile; CEO Kirtley direct quotes on magnet materials, 85–95% energy recovery claim, Trenta rep rate (1 pulse/10 min), commercial targets
- `knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md` — Wikipedia Helion Energy article; confirms Orion as 8th-generation machine under construction in Malaga WA for 50 MWe Microsoft delivery, Nucor 500 MWe partnership, Polaris status; provides prototype lineage table
- `knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-milestones-feb2026.md` — Helion press release, February 2026; confirms Polaris achieved D-T fusion at 150M°C (13 keV); confirms Orion under construction as first commercial machine; does not disclose additional design-point parameters

---

## 2. Candidates surfaced

**Polaris — 7th-generation prototype (under operation since late 2024)**
No electrical output by design. Polaris is a physics demonstrator whose objective is to demonstrate net electricity production (not yet achieved as of February 2026). Achieved D-T fusion at 150M°C/13 keV. Target pulse rate 1 Hz. Wikipedia notes it as "expected to increase the pulse rate" from Trenta's 1 pulse/10 min. No design-point electrical output — it is a stepping stone, not the cost-projection target. Does not qualify under the selection rule.

**ARPA-E Fusion Engine design study — 50 MW at 2 Hz**
The ARPA-E DocsLib presentation presents the clearest quantitative design point in the public record: 50 MW net output, 2 Hz repetition rate, 40 T reactor compression field. η·Q parameters explicitly stated. This corresponds to the Fusion Engine concept the ARPA-E ALPHA grant funded (2015–~2020 period). It is not a separately named commercial plant but the underlying physics design study for Helion's commercial architecture — and the figure converges exactly with Orion's contracted output.

**Orion — 8th-generation first commercial plant (50 MWe, 2028 target)**
Named machine, under construction in Malaga, WA since July 2025. Binding 50 MWe power purchase agreement with Microsoft for 2028 grid delivery. Confirmed independently in Helion press releases, Wikipedia, Reuters, and the February 2026 milestone announcement. Engineering specifications are proprietary; the 50 MWe figure is the only published parameter. The ARPA-E design point (50 MW at 2 Hz, 40 T) is the best public proxy for Orion's architecture. Qualifies as `pilot-demonstrator` — under construction, first commercial unit, contracted output published.

**Nucor 500 MWe commercial partnership (2030 target)**
Announced October 2023. No published engineering parameters beyond the 500 MWe contract size and 2030 ambition. No geometry, no rep rate, no efficiency data. Pure aspirational announcement. Does not qualify — no quantitative design data supports a `P_native` derivation.

---

## 3. Selection

Orion is selected as the design point. It is the only named plant in Helion's portfolio that combines a contracted net electrical output figure (50 MWe via Microsoft PPA) with corroborating design-point data (ARPA-E Fusion Engine: 50 MW at 2 Hz). The 50 MWe figure is not a range or a rounding — it is the contracted commitment stated in all public sources. The ARPA-E design study grounds the architecture that Orion instantiates: 40 T reactor compression, 2 Hz repetition, direct inductive energy recovery. Polaris has no electrical output by design and cannot serve as the cost-projection target. The Nucor 500 MWe plant has no published engineering data and cannot support a `P_native`.

```yaml
proposal:
  concept_id: 08-frc-w-direct-conversion
  design_name: "Orion — Helion 8th-generation first commercial plant (50 MWe Microsoft PPA, 2028 target)"
  maturity_tier: pilot-demonstrator
  p_native_mwe: 50
  primary_sources:
    - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md
    - knowledge/concept_research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md
    - knowledge/concept_research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md
  selection_rationale: |
    Orion is Helion's only named first-commercial plant with a published electrical output: 50 MWe committed via a binding Microsoft power purchase agreement for 2028 grid delivery, confirmed across the company's press releases, Reuters, Wikipedia, and the Feb 2026 milestone announcement. The ARPA-E Fusion Engine design study (DocsLib presentation) independently corroborates the same output at 50 MW with explicit architecture parameters (40 T compression field, 2 Hz repetition rate), providing the quantitative grounding that Orion's proprietary engineering documents do not make public. Polaris has no electrical output by design and is a physics demonstrator. The Nucor 500 MWe partnership has no published engineering parameters and cannot ground a P_native.
  alternatives_considered:
    - design: "Nucor 500 MWe commercial plant (2030 ambition)"
      reason_rejected: no published engineering parameters; aspirational contract announcement only
      sensitivity_implication: "if picked instead, P_native would rise substantially (500 vs 50 MWe) → far fewer modules at 1 GWe → 1 GWe LCOE would shift down materially. Worth revisiting if Helion publishes engineering specifications for the Nucor plant ahead of the 2030 target date."
    - design: "Polaris — 7th-generation prototype (D-T physics demonstrator)"
      reason_rejected: no electrical output by design; sub-scale physics prototype
      sensitivity_implication: "n/a — Polaris is not a power-producing design point; no P_native to substitute"
```

---

## 4. Open questions

- **Orion's proprietary engineering specs**: The only published parameter for Orion is the 50 MWe output. Geometry, rep rate, magnetic field achieved, blanket configuration, and net efficiency are not public. If Helion publishes an engineering report for Orion (e.g., in connection with regulatory permitting or the Microsoft delivery), the design point should be verified against that document — particularly whether the 50 MWe is gross or net electrical output.

- **Net electricity milestone on Polaris**: As of February 2026, Polaris has not demonstrated net electricity production. If Helion announces this milestone and discloses the measured Q or net power, it would provide the first empirical anchor for the Orion design-point assumptions and could force revision of the archetype fit grade (currently Low).

- **Nucor 500 MWe timeline and specs**: If Helion publishes engineering parameters for the Nucor plant ahead of the 2030 target, P_native should be revisited. At 500 MWe (10× Orion), the 1 GWe plant would require only two modules and the LCOE structure changes substantially.

- **ARPA-E design study dating**: The DocsLib presentation is undated in the source extraction. It references the 40 T reactor target (consistent with Polaris-era planning) but was published in the context of the ARPA-E ALPHA program (~2015–2020). If a more recent Helion design study becomes available that revises the 50 MW design point, re-evaluate.