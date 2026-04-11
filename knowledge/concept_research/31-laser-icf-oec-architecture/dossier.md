# Laser ICF - OEC Architecture (D-T)

**Company**: Blue Laser Fusion (BLF)
**Last updated**: 2026-03-07
**Iterations completed**: 1
**Overall confidence**: medium-high

## Summary

Blue Laser Fusion (BLF) is developing a laser-based inertial fusion energy system using a novel Optical Enhancement Cavity (OEC) architecture combined with Coherent Beam Combining (CBC) of fiber lasers. Founded in 2022 by 2014 Nobel Laureate Shuji Nakamura (inventor of the blue LED), the company is based in Goleta, CA with offices in Silicon Valley and Tokyo. The core innovation replaces the massive diode-pumped solid-state laser amplifier chains of NIF/HiPER/LIFE with compact, mass-produced fiber lasers injected into high-finesse Fabry-Perot optical cavities derived from LIGO gravitational wave detector technology, achieving pulse-stacking enhancement factors up to 100,000x. The reactor concept uses direct-drive shock ignition of cryogenic D-T targets at 1-10 Hz, with a helium-gas-cooled lithium-lead blanket for tritium breeding and a dual-channel energy capture system (70% thermal, 30% direct energy conversion).

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47120 (2025); https://bluelaserfusion.com/
- **Notes**: Laser-driven inertial confinement fusion. No ambiguity.

### Confinement Concept
- **Value**: Laser ICF (direct drive)
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104 (2025): "cryogenic deuterium-tritium targets in a direct drive scheme"
- **Notes**: Specifically uses shock ignition (SI) scheme with direct drive. 500 beams (360 compression + 140 ignition) illuminate the target directly. The OEC/CBC laser architecture is the distinguishing feature vs. other direct-drive concepts (which use DPSSL or KrF). BLF's proprietary technology is the "Optical Enhancement Cavity" laser system.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025); BLF website homepage: "DT based target for high gain fusion reaction"
- **Notes**: All primary sources (peer-reviewed paper, company website) consistently specify cryogenic D-T targets. One secondary news article (Interesting Engineering) mentions BLF "looking at boron" as a future fuel — this appears to be an aspirational long-term statement or journalist error. The current reactor design, power balance calculations, and blanket design are all built around D-T.

### Primary Heating
- **Value**: Laser (direct drive)
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47105 (2025)
- **Notes**: Direct-drive shock ignition. Initial compression at ~5x10^14 W/cm^2 (5-10 ns pulse), followed by high-intensity ignition pulse at 10^15-10^16 W/cm^2 (0.5-1 ns). CBC fiber lasers at 1060 nm, frequency-tripled to 350 nm UV via THG in KDP/DKDP crystals. 5 MJ total laser energy per shot delivered by 500 OEC modules.

### Energy Capture
- **Value**: Hybrid (thermal + direct)
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47117 (2025), Table 2 and Fig. 10
- **Notes**: Explicitly dual-channel energy conversion:
  - **70% of fusion energy** (14.1 MeV neutrons) -> lithium-lead blanket -> helium gas cooling -> conventional turbine generator (eta_th* = 0.44 including 10% exothermic breeding contribution)
  - **30% of fusion energy** (alpha particles + plasma exhaust) -> magnetically guided to DEC exhaust ports -> direct energy conversion electrodes (eta_DEC = 0.44)
  - Total conversion efficiency: eta_e = 0.7 x 0.44 + 0.3 x 0.44 = 0.44
  - BLF website confirms: "Generates steam with the heat from the blanket" + "directly converts captured charged particles into electricity"

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47105 (2025)
- **Notes**: Laser-driven implosion compresses cryogenic D-T fuel to fusion conditions. Shock ignition scheme: slow implosion achieves high density/areal density, then strong shock wave triggers thermonuclear burn. Standard IFE compressed plasma state.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115 (2025)
- **Notes**: No magnetic confinement of plasma. The reactor incorporates "embedded magnetic fields" at laser ports and a "magnetized dry-wall chamber," but these magnets deflect charged particles toward DEC exhaust ports and protect the first wall — they do not confine the fusion plasma. Per the schema definition: "Driver subsystem may contain magnets, but these confine the beam, not the plasma."

### Tritium Breeding
- **Value**: LiPb blanket
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47116 (2025): "natural lithium (containing 7.5% 6Li and 92.5% 7Li) as breeding material and a lead neutron multiplier (Pb)"
- **Notes**: Helium-gas-cooled lithium-lead blanket. Lead provides neutron multiplication (n + 208Pb -> 207Pb + 2n). Blanket uses SiC-based ceramics, investigating integration with high-temperature gas-cooled reactor (HTGR) technology. The thermal conversion efficiency includes a 10% boost from exothermic 6Li(n,alpha)T breeding reaction. IFE advantage: tritium inventory in chamber limited to a few mg per target.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47115-47116 (2025)
- **Notes**: The lithium-lead blanket captures ~70% of fusion energy carried by 14.1 MeV neutrons, performing both breeding and energy capture functions. The first wall uses tungsten facing + RAFM steel with helium gas cooling. Embedded magnetic fields deflect charged particles. The paper does not describe a separate dedicated shielding system beyond the blanket/first wall — the blanket serves the integrated function. Remote handling and robotic inspection systems are mentioned for component replacement.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025): "Laser operation frequency: 1 to 10 Hz"
- **Notes**: Discrete fusion burn events at 1-10 Hz repetition rate. Each shot: laser fires -> target implodes -> fusion burn -> energy capture -> new target injected. Standard IFE pulsed operation.

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), Table 2 (2025): "f = 1 to 10 Hz"
- **Notes**: Design range is 1-10 Hz. At 10 Hz, the system achieves maximum power output (2.8 GW_e) and minimum recirculating power fraction (0.170). At 1 Hz, output drops to ~102 MW with recirculation fraction of 0.426. Using ~10 Hz as the primary value since that is the target for a practical power plant.

### Driver Technology
- **Value**: CBC fiber laser + OEC, 5 MJ UV
- **Confidence**: high
- **Citation**: Sunahara et al., *Optics Express* 33(22), 47104-47111 (2025)
- **Notes**: This is BLF's core innovation and primary differentiator. Key specs:
  - 500 CBC-OEC modules, each producing ~10 kJ
  - Fiber lasers at 1060 nm, coherently beam-combined
  - Injected into high-finesse Fabry-Perot optical cavities (OECs)
  - OEC stacks pulses to achieve enhancement factors up to 100,000x
  - Frequency-tripled to 350 nm UV (eta_3omega ~ 0.6)
  - Wall-plug-to-UV efficiency: ~10%
  - Derived from LIGO gravitational wave detector cavity technology
  - Prototype (1.5 m): finesse 419,000, enhancement factor 59,000 demonstrated (2024)
  - 15 m systems under construction (2025)
  - 150 m scale planned for reactor-class output

## Remaining Gaps

1. **Neutron Management** (medium confidence): The paper describes the blanket and first wall but doesn't provide detailed shielding specifications or activation analysis. The `Integrated blanket/shield` classification is inferred from the design description — a dedicated shielding analysis paper would raise confidence to high.

2. **Blanket TBR**: The paper doesn't state a specific tritium breeding ratio. The blanket design (natural Li + Pb multiplier) is standard but no TBR calculation is provided. This doesn't affect column values but is a gap for deeper economic analysis.

3. **DEC technology specifics**: The paper references theoretical work on adiabatic direct energy conversion in axisymmetric fields (Rax et al., 2025) but doesn't specify the exact DEC design BLF will use. eta_DEC = 0.44 is described as "conservative."

4. **Target gain validation**: The assumed target gain of 160 is based on Froula et al. simulations for CBET-mitigated direct drive, not experimentally demonstrated. BLF claims their multicolor/SRP/broadband approach will achieve gains "beyond the CBET-mitigated curve." This is critical for power balance but doesn't affect differentiation column values.

5. **Advanced fuel roadmap**: One secondary source mentions boron fuel interest. All primary sources are D-T only. Not a gap for current classification but may be relevant for future iterations.

## Key Sources

1. **Sunahara et al., "Laser-based inertial fusion energy system enabled by optical enhancement cavities and a direct-drive configuration reactor," *Optics Express* 33(22), 47104-47120 (2025). DOI: 10.1364/OE.575181** — Primary authority source. Peer-reviewed paper with reactor parameters, power balance, and OEC prototype results.
   - Saved: `iter-01/sources/optics-express-2025-paper.md`

2. **Blue Laser Fusion website** (https://bluelaserfusion.com/) — Company homepage, technology page, about page, blog posts. Confirms D-T fuel, dual energy conversion, 5 MJ laser, 1 GW target.
   - Saved: `iter-01/sources/blf-website-and-news.md`

3. **ITOCHU press release** (March 2024): https://www.itochu.co.jp/en/news/press/2024/240307.html — Capital and business alliance.

4. **Semiconductor Today / Optics.org** — INFUSE awards, JST Moonshot selection, $25M seed round context.

5. **Santa Barbara Independent** (Oct 2025) — Local coverage with company background.
