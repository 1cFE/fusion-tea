# Design Point Reasoning Trace — 20a-type-one-stellarator

## 1. Sources walked

- `knowledge/concept_research/20a-type-one-stellarator/dossier.md` — synthesized summary; established Infinity Two as the only commercial design in the portfolio (R=12.5 m, A=10, B=9 T, 800 MW fusion / 350 MWe net, HCPB blanket); flagged Infinity One as a sub-scale validation device
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/typeoneenergy-type-one-energy-issues-first-realistic/output.md` — Type One Energy press release (Mar 2025); states "800 MW of fusion power and delivers a nominal 350 MWe to the power grid"; describes D-T fuel and steady-state stellarator architecture
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-journals-journal-of-plasma-physics-article/output.md` — JPP special issue overview paper (E65, Anderson/Canik/Hegna/Mowry 2025); confirms "800 MW of fusion power," "nominal 350 MWe," 4-field-period quasi-isodynamic configuration, A=10, R not stated in abstract but cross-referenced to Hegna et al.; confirms TVA Cooperative Agreement for "nominal 350 MWe Infinity Two fusion power plant… as early as mid-2030s"
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-services-aop-cambridge-core-content-view/output.md` — JPP E67 paper "Power and particle exhaust for the Infinity Two fusion pilot plant" (Bader et al. 2025); provides Table 1 with full operational parameters: 4 field periods, a=1.25 m, R=12.5 m, B=9 T, Pfus=800 MW; confirms single operating point, no multi-phase variants
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/modernsciences-type-one-energy-fusion-pilot-plant-design/output.md` — secondary news summary; confirms 800 MW fusion, Q=40, gas-cooled solid breeder blanket; mentions TVA partnership and Infinity Two as the commercial target
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/ans-news-2025-04-01-article-6903/output.md` — ANS Nuclear Newswire item; confirms publication of physics design basis for Infinity Two; content gated beyond headline
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/arxiv-2512-08027/output.md` — arXiv preprint for Thea Energy's "Helios" planar coil stellarator (Swanson et al., Dec 2025); 390 MWe net, 1.1 GW thermal, QA configuration. **This is a different company (Thea Energy, formerly Stellarex), not Type One Energy.** Present in the source directory as a stellarator comparator but out of scope for this concept's design-point selection.
- `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/science-media-fes-pdf-fes-presentations-2022-pearson/output.md` — DOE FES 2022 presentation by Kyoto Fusioneering on tritium and blanket resource supply; tangential context on blanket fuel cycles, no Type One Energy design parameters

## 2. Candidates surfaced

**Infinity Two** — Type One Energy's commercial fusion pilot power plant, the primary product the company is developing for TVA. P_native: 350 MWe net (800 MW fusion power). Published 2025. Geometry: R=12.5 m, a=1.25 m, aspect ratio 10, 4-field-period QI/maximum-J, B=9 T. D-T fuel. HCPB solid breeder blanket (TBR=1.30, confirmed by OpenMC neutronics). Rankine steam cycle. Q > 40 (burning plasma). Steady-state. Six peer-reviewed papers in Journal of Plasma Physics (2025) providing physics basis for plasma confinement, alpha-particle behavior, MHD equilibrium, blanket/tritium cycle, power exhaust, and core plasma performance. Formal TVA Cooperative Agreement (Jan 2025). Formal design review completed May 2025. Maturity: proposed-commercial. **Qualifies as design point.**

**Infinity One** — sub-scale validation and design-verification stellarator. Explicitly described in the JPP overview as "a subscale stellarator to validate the choices made for Infinity Two." Planned operation in 2029 at TVA's Bull Run site. No net electrical output by design — its stated purpose is physics validation and divertor testing (specifically LIBD concept verification). Not designed to produce commercial electricity. **Does not qualify as a design point candidate.**

**Thea Energy Helios** — planar coil QA stellarator from a different company (Thea Energy), published Dec 2025. 390 MWe net, 1.1 GW thermal, 88% capacity factor. Present in source materials as a stellarator comparator. This is a different concept and company, not within the scope of concept 20a (Type One Energy). **Not a candidate for this concept's design point.**

## 3. Selection

Infinity Two is the only design in Type One Energy's portfolio with a published electrical output target. It is the single commercial design the company is developing, with a utility partnership and a six-paper peer-reviewed physics basis. The selection rule is unambiguous: there is only one candidate with a P_native.

```yaml
proposal:
  concept_id: 20a-type-one-stellarator
  design_name: "Infinity Two fusion pilot power plant (Hegna et al. 2025, J. Plasma Phys. special issue)"
  maturity_tier: proposed-commercial
  grounding_confidence: high
  p_native_mwe: 350
  primary_sources:
    - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/typeoneenergy-type-one-energy-issues-first-realistic/output.md
    - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-journals-journal-of-plasma-physics-article/output.md
    - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-services-aop-cambridge-core-content-view/output.md
  selection_rationale: |
    Infinity Two is Type One Energy's only published commercial design and the only design
    in the portfolio with a stated P_native. The 350 MWe net figure is stated directly by
    the company press release and confirmed in the JPP overview paper ("nominal 350 MWe
    Infinity Two fusion power plant") and the TVA Cooperative Agreement language. The
    design is a single machine with a single published operating point (800 MW DT fusion,
    R=12.5 m, B=9 T, HCPB blanket); no multi-phase variants or alternative operating
    cases are published. The only other device in the portfolio — Infinity One — is a
    sub-scale validation machine with no electrical output by design and therefore does
    not qualify as a design point.
  alternatives_considered:
    - design: "Infinity One (sub-scale validation stellarator)"
      reason_rejected: no electrical output by design; purpose is physics validation for Infinity Two
      sensitivity_implication: >
        Infinity One has no P_native and cannot serve as a design point; picking it would
        force a freeform route with no cost projection possible. This is not a sensitivity
        branch — it is a categorical exclusion. The relevant sensitivity question is whether
        Infinity Two's 350 MWe figure shifts if Type One Energy publishes a revised commercial
        design following Infinity One validation results; if the validated operating point
        differs materially from the 2025 physics basis, P_native could rise or fall, shifting
        n_mod and 1 GWe LCOE accordingly. Worth revisiting after 2029 Infinity One results.
```

## 4. Open questions

- **Post-Infinity One revision risk.** The JPP papers explicitly state that design margins in Infinity Two will be revised after Infinity One validation (planned 2029). If Infinity One results support relaxing margins, the commercial design could shift to a higher operating point (plasma physics solutions reportedly exist up to ~3 GW fusion power per the JPP overview). A revised Infinity Two with higher P_native would reduce n_mod and shift the 1 GWe LCOE down. This is the primary watch item for re-selection.
- **Net electrical accounting.** The 350 MWe figure is described as "nominal" in company and utility sources; no detailed recirculating power breakdown (ECRH, cryogenics, pellet injection, pumping) has been published in the six JPP papers reviewed. A full engineering power balance could revise the net figure modestly in either direction when the blanket and balance-of-plant engineering is completed.
- **Rankine cycle efficiency confirmation.** The dossier and JPP papers reference >30% thermal efficiency for the Rankine steam cycle, but the engineering design of the power conversion system has not been published at parameter level. If the thermal efficiency is lower than assumed, gross electrical output would decrease from what a 800 MW fusion source implies, potentially reducing P_native below 350 MWe.
- **Infinity Two engineering design maturity.** As of the 2025 physics basis, magnet, blanket, and shielding engineering are still progressing. The May 2025 formal design review completion is a positive indicator, but full engineering parameters remain unpublished. This does not change the selection — Infinity Two is clearly the correct design point — but it is the source of the gap between `high` grounding confidence on the physics basis and the eventual engineering design verification.