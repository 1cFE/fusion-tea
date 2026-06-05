# Design Point Reasoning Trace — 10-large-scale-stellarator

## 1. Sources walked

- `knowledge/concept_research/10-large-scale-stellarator/iter-01/sources/helias-reactor-context.md` — Beidler et al. IAEA paper "The Helias Reactor"; defines HSR4/18 and HSR5/22 engineering parameters including fusion power, geometry, coil count, efficiency estimate (~35%), and blanket options
- `knowledge/concept_research/10-large-scale-stellarator/iter-01/output.md` — researcher synthesis covering Gauss Fusion/GIGA concept: confirms DT fuel, 3 GWth → ~1 GWe output, LTS+HTS dual-track magnets, 40 non-planar modular coils, F4E collaboration, CDR scope; also sources index listing MT29 abstract, binding.energy supply chain analysis, and news coverage
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-cdr-review-2026.md` — Startbase article (Mar 2026): expert panel chaired by Prof. Hartmut Zohm confirms CDR; marks formal transition from design to engineering phase; confirms GIGA is the "first fully integrated European design concept for a commercial fusion power plant"
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-partnerships-2025.md` — Modern Power Systems article: Gauss Fusion industrial partnerships for TBB design, HTS/LTS conductor tracks, and site selection; confirms "GAUSS GIGA plant concept" and "grid-scale fusion energy"
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/helias-blanket-studies.md` — Bongiovi et al. (KIT/CREATE/Basilicata): HELIAS 5-B HCPB breeding blanket mechanical design; confirms 5-fold symmetry design (72° sectors, 16 rings, 80 BB segments), 3D blanket geometry, EUROFER steel, He-cooled sandwich architecture; no net electric output stated
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/arxiv-2512-08027v1/output.md` — Swanson et al. (Thea Energy): "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant" (arXiv 2512.08027, Dec 2024); explicitly states 390 MWe net, 1.1 GWth, R=8m, A=4.5, 6T axis field, DT, planar HTS coils, 88% capacity factor
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389/output.md` — Moreno et al.: ParaStell parametric modeling toolset for stellarator FWBS systems using WISTELL-D; neutronics tooling paper; no design-point power figures
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/core-outputs-100308302/output.md` — Waganer et al. (Boeing/ARIES): "ARIES-CS Maintenance System Definition and Analysis"; notes 85% plant availability target; no net electric figure from this excerpt
- `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/depositonce-bitstreams-39e36af5-b43a-4d14-b7fd-50c4e8b23aea/output.md` — TU Berlin DepositOnce repository login page; extraction failed (gated content); no usable data

## 2. Candidates surfaced

**GIGA (Gauss Fusion)**
Full Conceptual Design Report (CDR) submitted to the German government October 2025; reviewed by 13-person international expert panel in early 2026. GIGA is a quasi-isodynamic (QI) stellarator directly extrapolated from the HSR4/18 HELIAS design, with upgrades to LTS+HTS dual-track conductors and demountable coil joints. Plant-level parameters: 40 non-planar modular coils (5 shapes × 8), 4 field periods, major radius ~18-20m (HSR4/18 heritage), DT fuel, ~3 GWth thermal output → ~1 GWe net electric. The "GIGA" designation is the company's own description of a gigawatt-class plant; the 1 GWe figure is stated in public CDR summaries and press coverage and is consistent with 3 GWth × ~33% thermal efficiency. Net electric figure is attributed to company press communications; the CDR is not publicly released. `P_native ≈ 1000 MWe`. Most commercially mature design in this concept class.

**Helios (Thea Energy)**
Preconceptual design published December 2024 (arXiv 2512.08027). Two-field-period quasi-axisymmetric (QA) stellarator with planar HTS coils (12 encircling + 324 shaping). R=8m, A=4.5, a=1.8m, B₀=6T, fusion power 958 MW, total thermal power 1.1 GWth, net electric power 390 MWe (explicitly tabulated), thermal conversion efficiency 40% (steam Rankine), DT fuel, 88% capacity factor. Full preconceptual engineering paper with detailed tables. `P_native = 390 MWe`. Well-grounded by explicit publication, but a distinct architecture from the large-scale HELIAS class (compact planar-coil QA rather than large non-planar modular QI).

**HSR4/18 (IPP/EUROfusion HELIAS, 4-period)**
Published IAEA proceedings (Beidler et al.). The academic precursor from which GIGA was designed. R=18m, a=2.1m, B₀=5.0T, 40 NbTi coils (10T max), plasma volume 1421 m³, fusion power ~2.8 GWth. Net efficiency ~35% stated for the class → ~980 MWe gross, minus recirculating → ~920-950 MWe net (inferred; net electric not tabulated directly). Academic paper concept, no company development behind it; GIGA is the commercial successor to this design. `P_native ≈ 950 MWe (inferred)`.

**HSR5/22 (IPP/EUROfusion HELIAS, 5-period)**
Same IAEA proceedings. Direct W7-X extrapolation: R=22m, 50 NbTi coils, B₀=4.75T, plasma volume 1407 m³, fusion power ~3.06 GWth. With 35% efficiency → ~1070 MWe gross. Larger and likely more expensive than HSR4/18; IPP selected HSR4/18 as the more cost-effective variant. GIGA is based on the HSR4/18 lineage. `P_native ≈ 1000-1050 MWe (inferred)`.

**HELIAS 5-B (EUROfusion academic concept)**
Academic concept under EUROfusion, studied primarily for blanket and neutronics. 5-fold symmetry, 72° sectors, 16 rings, 80 BB segments per sector, HCPB He-cooled blanket under study. No net electric output stated in the available source (blanket mechanical design paper only). Cannot assign a defensible P_native from sources at hand.

**ARIES-CS**
Referenced in the Helios paper as a comparator compact stellarator design; maintenance study in source tree (85% availability target). Different architecture from HELIAS lineage; not the archetype for this concept category. Not evaluated further.

## 3. Selection

GIGA (Gauss Fusion) is selected as the design point at `P_native = 1000 MWe`. It is the only company-led, CDR-complete commercial design in the large-scale HELIAS-lineage QI stellarator class, and the most mature overall. The CDR was submitted to the German government in October 2025 and was independently reviewed by a 13-person international expert panel in early 2026 — the first fully integrated European conceptual design for a commercial fusion power plant to pass such a review. The 1 GWe target is the company's stated commercial output (the "GIGA" plant name is itself a gigawatt-class designation), consistent with the publicly stated 3 GWth thermal output and a ~33% thermal conversion efficiency, which matches the efficiency range documented for the HELIAS precursor class in the helias-reactor-context.md source. Grounding is `medium` because the CDR is not publicly released — the 1 GWe figure traces to company press communications and is endorsed by the published HELIAS precursor engineering, but cannot be independently verified against CDR contents.

Helios (Thea Energy) has more precisely published parameters (390 MWe net explicitly tabulated in an open journal paper), but is a fundamentally different architecture: compact (8m vs ~18m major radius), planar-coil QA rather than non-planar modular QI, and at preconceptual stage rather than a reviewed CDR. It is a competitor concept, not the HELIAS-lineage "large-scale stellarator" this taxonomy entry represents.

```yaml
proposal:
  concept_id: 10-large-scale-stellarator
  design_name: "GIGA commercial fusion power plant (Gauss Fusion CDR, 2025)"
  maturity_tier: proposed-commercial
  grounding_confidence: medium
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-cdr-review-2026.md
    - knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-partnerships-2025.md
    - knowledge/concept_research/10-large-scale-stellarator/iter-01/sources/helias-reactor-context.md
  selection_rationale: |
    GIGA is the only company-led, CDR-complete commercial design in the large-scale
    HELIAS-lineage QI stellarator class. The CDR was submitted to the German government
    in October 2025 and reviewed by a 13-person international expert panel in early 2026,
    marking the formal transition to engineering phase — the most mature development status
    of any design in this concept category. The 1 GWe net electric target is the company's
    stated commercial output (the "GIGA" plant name denotes gigawatt-class), consistent
    with the publicly stated 3 GWth thermal target and the ~33–35% thermal conversion
    efficiency documented for the HELIAS precursor class in published IAEA proceedings.
    P_native is a single-module, single-plant value: GIGA is a single large stellarator
    (not a multi-module array), so 1000 MWe is the natural unit.
  alternatives_considered:
    - design: "Helios preconceptual design (Thea Energy, Swanson et al. arXiv 2512.08027, Dec 2024)"
      reason_rejected: >-
        Compact planar-coil QA stellarator (R=8m) — architecturally distinct from the
        large-scale non-planar modular QI class this concept represents; preconceptual
        stage rather than CDR; lower archetype fit
      sensitivity_implication: >-
        If picked instead, P_native drops substantially (390 vs 1000 MWe) →
        significantly more modules at 1 GWe → 1 GWe LCOE shifts up from more reactor
        islands. Worth revisiting if Thea Energy advances to a CDR-level design and the
        taxonomy reclassifies compact QA stellarators under this concept entry.
    - design: "HSR4/18 academic HELIAS reactor (Beidler et al., IAEA proceedings)"
      reason_rejected: >-
        Academic paper concept superseded by GIGA; no company development or CDR behind
        it; GIGA is the direct commercial successor with HTS upgrades
      sensitivity_implication: >-
        If picked instead, P_native shifts slightly lower (inferred ~950 vs 1000 MWe) →
        modestly more modules at 1 GWe → 1 GWe LCOE shifts marginally up. Directional
        impact is small; sensitivity probe is unlikely to change conclusions.
    - design: "HSR5/22 academic HELIAS reactor (Beidler et al., IAEA proceedings)"
      reason_rejected: >-
        Larger 5-period variant (22m radius, 50 coils); IPP explicitly chose HSR4/18
        as the more compact and cost-effective design, and GIGA follows the 4-period
        lineage; no company development
      sensitivity_implication: >-
        If picked instead, P_native rises modestly (~1050 vs 1000 MWe) → slightly
        fewer modules at 1 GWe → 1 GWe LCOE shifts marginally down. Directional
        impact is small given the modest size difference.
    - design: "HELIAS 5-B EUROfusion academic concept (blanket studies phase)"
      reason_rejected: >-
        No net electric output stated in available sources; only blanket mechanical
        design paper ingested; cannot assign defensible P_native
      sensitivity_implication: >-
        HELIAS 5-B is a 5-fold concept, likely ~3 GWth class similar to HSR5/22;
        if a published net electric figure surfaces, it would likely fall in the
        950-1050 MWe range and have minimal directional impact on the design point.
```

## 4. Open questions

- **GIGA net electric figure in the public CDR summary**: The 1 GWe figure currently traces to press communications and is consistent with the thermal target and precursor efficiency data. If Gauss Fusion releases a public CDR summary or the government publishes the expert panel's technical findings, a precise net electric figure should be confirmed and `grounding_confidence` elevated to `high` if it aligns with 1000 MWe or adjusted if materially different.

- **Thermal conversion cycle specification**: The CDR review source confirms heat extraction and power conversion systems are included but the cycle type (steam Rankine vs. sCO2 Brayton) is not publicly stated. If Gauss Fusion's GIGA CDR specifies sCO2 or another advanced cycle achieving >40% thermal efficiency, P_native could shift upward (e.g., 3 GWth × 40% = 1200 MWe), which would force a design-point revision.

- **GIGA major radius confirmation**: The design is described as being in the HSR4/18 lineage (~18m) but the exact major radius of GIGA with upgraded HTS magnets and higher field (12–13T peak vs. 10T for NbTi) is not confirmed in public sources. Higher-field HTS coils could permit a more compact version than HSR4/18 while achieving the same fusion power; if this materially changes the plant geometry or output, it may affect comparability with the HSR4/18 archetype cited here.

- **Helios taxonomy placement**: If a future taxonomy revision separates "compact optimized stellarators" (Thea Energy Helios, Proxima Fusion) from "large-scale HELIAS-lineage stellarators" (GIGA, HSR4/18), Helios would belong in a separate concept entry and would not be an alternative for this design point. This is an open taxonomic question that currently leaves Helios as a rejected alternative here.