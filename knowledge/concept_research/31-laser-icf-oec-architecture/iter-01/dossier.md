# Concept Dossier: Laser ICF - OEC Architecture (D-T)

**Company**: Blue Laser Fusion (BLF)
**Overall Confidence**: medium
**Last updated**: 2026-03-07
**Iteration**: 1

## Summary

Blue Laser Fusion Inc. (BLF) is developing a laser-based inertial fusion energy system using a novel Optical Enhancement Cavity (OEC) architecture combined with Coherent Beam Combining (CBC) of fiber lasers. Founded in 2022 by Nobel Laureate Shuji Nakamura (2014 Physics Nobel for blue LEDs), the company is based in Goleta, CA with offices in Silicon Valley and Tokyo. The core innovation is using high-finesse Fabry-Pérot optical cavities (derived from LIGO technology) to stack laser pulses >100,000×, enabling MJ-class UV laser output from compact, mass-produced fiber lasers at 1-10 Hz repetition rates. The reactor concept uses direct-drive shock ignition of cryogenic D-T targets, with a helium-gas-cooled lithium-lead blanket for neutron capture/tritium breeding and a direct energy conversion system for charged particle energy recovery. Target plant output is 0.1-2.8 GW_e.

---

## Column Assessments

### Confinement Family
- **Value**: `IFE`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47120 (2025); https://bluelaserfusion.com/
- **Notes**: Laser-driven inertial confinement fusion. No ambiguity.

### Confinement Concept
- **Value**: `Laser ICF (direct drive)`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104 (2025): "cryogenic deuterium-tritium targets in a direct drive scheme"
- **Notes**: Specifically uses shock ignition (SI) scheme with direct drive. 500 beams (360 compression + 140 ignition) illuminate the target directly. The OEC/CBC laser architecture is the distinguishing feature vs. other direct-drive concepts (which use DPSSL or KrF). BLF's proprietary technology is the "Optical Enhancement Cavity" laser system.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025); BLF website homepage: "DT based target for high gain fusion reaction"
- **Notes**: All primary sources (peer-reviewed paper, company website) consistently specify cryogenic D-T targets. One secondary news article (Interesting Engineering) mentions BLF "looking at boron" as a future fuel — this appears to be an aspirational long-term statement. The current reactor design, power balance calculations, and blanket design are all built around D-T.

### Primary Heating
- **Value**: `Laser (direct drive)`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47105 (2025)
- **Notes**: Direct-drive shock ignition. Initial compression at ~5×10¹⁴ W/cm² (5-10 ns pulse), followed by high-intensity ignition pulse at 10¹⁵-10¹⁶ W/cm² (0.5-1 ns). CBC fiber lasers at 1060 nm, frequency-tripled to 350 nm UV via THG in KDP/DKDP crystals. 5 MJ total laser energy per shot delivered by 500 OEC modules.

### Energy Capture
- **Value**: `Hybrid (thermal + direct)`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47117 (2025), Table 2 and Fig. 10
- **Notes**: Explicitly dual-channel energy conversion:
  - **70% of fusion energy** (14.1 MeV neutrons) → lithium-lead blanket → helium gas cooling → conventional turbine generator (η_th* = 0.44 including 10% exothermic breeding contribution)
  - **30% of fusion energy** (alpha particles + plasma exhaust) → magnetically guided to DEC exhaust ports → direct energy conversion electrodes (η_DEC = 0.44)
  - Total conversion efficiency: η_e = 0.7×0.44 + 0.3×0.44 = 0.44
  - BLF website confirms: "Generates steam with the heat from the blanket" + "directly converts captured charged particles into electricity"

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47105 (2025)
- **Notes**: Laser-driven implosion compresses cryogenic D-T fuel to fusion conditions. Shock ignition scheme: slow implosion achieves high density/areal density, then strong shock wave triggers thermonuclear burn. Standard IFE compressed plasma state.

### Magnet Type
- **Value**: `None (IFE)`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115 (2025)
- **Notes**: No magnetic confinement of plasma. However, the reactor does incorporate "embedded magnetic fields" at laser ports and a "magnetized dry-wall chamber" — these magnets deflect charged particles toward DEC exhaust ports and protect the first wall, not confine the fusion plasma. Per the schema definition: "Driver subsystem may contain magnets, but these confine the beam, not the plasma." The chamber magnets serve wall protection and energy routing functions.

### Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47116 (2025): "natural lithium (containing 7.5% ⁶Li and 92.5% ⁷Li) as breeding material and a lead neutron multiplier (Pb)"
- **Notes**: Helium-gas-cooled lithium-lead blanket. Lead provides neutron multiplication (n + ²⁰⁸Pb → ²⁰⁷Pb + 2n). Blanket uses SiC-based ceramics, investigating integration with high-temperature gas-cooled reactor (HTGR) technology. The thermal conversion efficiency includes a 10% boost from exothermic ⁶Li(n,α)T breeding reaction. IFE advantage: tritium inventory in chamber limited to a few mg per target.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47116 (2025)
- **Notes**: The lithium-lead blanket captures ~70% of fusion energy carried by 14.1 MeV neutrons, performing both breeding and energy capture functions. The first wall uses tungsten facing + RAFM steel with helium gas cooling. Embedded magnetic fields deflect charged particles. The paper does not describe a separate dedicated shielding system beyond the blanket/first wall — the blanket serves the integrated function. Remote handling and robotic inspection systems are mentioned for component replacement.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025): "Laser operation frequency: 1 to 10 Hz"
- **Notes**: Discrete fusion burn events at 1-10 Hz repetition rate. Each shot: laser fires → target implodes → fusion burn → energy capture → new target injected. Standard IFE pulsed operation.

### Repetition Rate
- **Value**: `~10 Hz`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025): "f = 1 to 10 Hz"
- **Notes**: Design range is 1-10 Hz. At 10 Hz, the system achieves maximum power output (2.8 GW_e) and minimum recirculating power fraction (0.170). At 1 Hz, output drops to ~102 MW with recirculation fraction of 0.426. The `~10 Hz` value captures the upper design target; `~1 Hz` would also be valid for the lower range. Using `~10 Hz` as the primary value since that's the target for a practical power plant.

### Driver Technology
- **Value**: `CBC fiber laser + Optical Enhancement Cavity (OEC), 5 MJ UV`
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47111 (2025)
- **Notes**: This is BLF's core innovation and primary differentiator. Key specs:
  - 500 CBC-OEC modules, each producing ~10 kJ
  - Fiber lasers at 1060 nm, coherently beam-combined
  - Injected into high-finesse Fabry-Pérot optical cavities (OECs)
  - OEC stacks pulses to achieve enhancement factors up to 100,000×
  - Frequency-tripled to 350 nm UV (η_3ω ≈ 0.6)
  - Wall-plug-to-UV efficiency: ~10%
  - Derived from LIGO gravitational wave detector cavity technology
  - Prototype (1.5 m): finesse 419,000, enhancement factor 59,000 demonstrated
  - 15 m systems under construction (2025)
  - 150 m scale planned for reactor-class output

---

## Metadata

### Published Machine/Plant?
- **Value**: Conceptual reactor design published
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Section 4 (2025)
- **Notes**: The Optics Express paper presents a conceptual reactor design with power balance calculations (Table 2, Fig. 10). It includes specific subsystem parameters but is not a detailed engineering design — it's a conceptual architecture with parametric performance estimates. No specific machine name has been assigned.

### Lab Experiments
- **Value**: OEC prototype demonstrations; no fusion experiments
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Section 2 (2025); BLF website
- **Notes**:
  - 1.5 m OEC prototype: achieved finesse 419,000 and energy enhancement factor 59,000 in CW operation (2024)
  - 15 m OEC systems under construction at Goleta (US) and Osaka University (Japan), targeting 100 J pulse energy with 10 kW injection laser
  - 8-channel CBC fiber rod amplifier system under construction
  - No fusion burn experiments performed by BLF
  - Relies on NIF's ignition demonstration (Dec 2022) as physics proof-of-concept
  - BLF builds on direct-drive shock ignition research from University of Rochester/LLE (OMEGA)
  - Partners: Caltech (INFUSE 2024), Colorado State University (INFUSE 2025), Osaka University (Moonshot)

---

## Remaining Gaps

1. **Neutron Management** (medium confidence): The paper describes the blanket and first wall but doesn't provide detailed shielding specifications or activation analysis. The `Integrated blanket/shield` classification is inferred from the design description — a dedicated shielding analysis would raise confidence.

2. **Target gain of 160**: This is a projected value based on Froula et al. simulations for CBET-mitigated direct drive. BLF claims their multicolor/SRP/broadband approach will achieve gains "beyond the CBET-mitigated curve." The actual gain has not been demonstrated experimentally. This affects the power balance calculations significantly.

3. **Advanced fuel aspirations**: One secondary source mentions boron fuel interest. All primary sources are D-T only. If BLF has a public roadmap for advanced fuels, it would be worth documenting but doesn't change the current classification.

4. **Blanket TBR**: The paper doesn't state a specific tritium breeding ratio. The blanket design (natural Li + Pb multiplier) is standard but no TBR calculation is provided.

5. **DEC technology specifics**: The paper references theoretical work on adiabatic direct energy conversion in axisymmetric fields (Rax et al., 2025) but doesn't specify the exact DEC design BLF will use. η_DEC = 0.44 is described as "conservative."

## Sources Consulted

### Primary Sources (yielded substantial information)
- Sunahara et al., "Laser-based inertial fusion energy system enabled by optical enhancement cavities and a direct-drive configuration reactor," *Optics Express* 33(22), 47104-47120 (2025). DOI: 10.1364/OE.575181 — **Primary authority source**
- Blue Laser Fusion website: https://bluelaserfusion.com/ (homepage, technology page, about page, blog posts)
- Blue Laser Fusion INFUSE 2025 press release: https://bluelaserfusion.com/blue-laser-fusion-wins-us-department-of-energy-2025-infuse-project-award/
- Semiconductor Today news articles on INFUSE awards and JST Moonshot selection

### Secondary Sources (context, funding, partnerships)
- ITOCHU press release (March 2024): https://www.itochu.co.jp/en/news/press/2024/240307.html
- Santa Barbara Independent (Oct 2025): https://www.independent.com/2025/10/17/blue-laser-fusion-in-goleta-looks-to-harness-nuclear-fusions-powerful-potential/
- Interesting Engineering: https://interestingengineering.com/innovation/nobel-laureate-rapid-fire-lasers-nuclear-fusion-reactor — **Note**: This article's claim about boron fuel contradicts all primary sources
- Optics.org: https://optics.org/news/14/7/44 ($25M seed round)
- ARPA-E presentation PDF (July 2025): https://arpa-e.energy.gov/sites/default/files/2025-08/Day1_02_Pattison.pdf — PDF not readable via web fetch

### Sources checked but not useful for gaps
- FIA 2023 industry report — BLF not prominently featured
- Wikipedia (Aneutronic fusion, ICF) — general background only
- AIP Advances paper on laser-driven IFE reactor perspectives — 403 access denied
