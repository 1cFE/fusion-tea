# Magnetized Target Fusion - Pneumatic Compression (D-T)

**Company**: General Fusion
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: high

## Summary

General Fusion's magnetized target fusion (MTF) concept uses steam-driven pneumatic pistons to compress a vortex of liquid metal (lithium or lead-lithium) around a magnetized compact toroid (spherical torus) plasma, driving it to fusion conditions. Operating at intermediate density and timescale between magnetic confinement (MFE) and inertial confinement (IFE), the system pulses at ~1 Hz in the commercial design targeting 300 MWe. The liquid metal liner serves triple duty as compression medium, neutron absorber/shield, and tritium breeder — a distinctive engineering simplification. The company's current LM26 demonstration machine (50% commercial plasma scale, ~4 m commercial cavity diameter) uses electromagnetic compression of solid lithium as a surrogate, while the commercial concept relies on mechanical/pneumatic compression.

## Differentiation Table Values

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — "Magnetized Target Fusion (MTF) technology"; IAEA FEC 2025 abstract (Hildebrand et al.) — explicitly "Magnetized Target Fusion"
- **Notes**: MTF/MIF are synonymous terms. General Fusion explicitly positions between MCF and ICF — magnetized plasma compressed by an external mechanical driver at intermediate density/timescale.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: high
- **Citation**: FST 2025 paper (DOI: 10.1080/15361055.2025.2526266) — "array of pneumatic piston drivers"; https://generalfusion.com/fusion-technology/; schema vocabulary
- **Notes**: The commercial design uses steam-driven pistons to compress liquid metal liner around magnetized plasma. "Pneumatic" in the schema captures the mechanical compression approach. LM26 demo uses electromagnetic theta-pinch of solid lithium as a surrogate, but the commercial concept is pneumatic/mechanical.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: FST 2025 paper — "spherical torus of deuterium-tritium plasma"; IAEA FEC 2025 — LM26 running with deuterium fuel; https://generalfusion.com/fusion-technology/
- **Notes**: Standard D-T fuel cycle. Tritium breeding from liquid lithium is a core design feature. LM26 demo uses deuterium only (no tritium in demo).

### Primary Heating
- **Value**: `Mechanical compression`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; APS 2018 overview — compression raises plasma from ~0.1 keV to 10 keV; cavity volume reduced by 3 orders of magnitude
- **Notes**: The plasma is initially formed by a Marshall gun (coaxial plasma gun) as a compact toroid (spherical torus), but the primary heating to fusion-relevant temperatures comes from mechanical compression of the liquid metal liner driven by steam pistons. Compression parameters (APS 2018): density 10^22 to 10^25 ions/m^3, temperature 0.1 to 10 keV, magnetic field 2 to 200 T.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951 — "liquid metal wall of the vessel" captures neutron energy; https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor — "lithium flows through heat exchanger -> generates steam -> spins generator for electricity"
- **Notes**: Standard thermal cycle: fusion neutrons heat the liquid metal liner, pumped through heat exchanger, steam Rankine cycle, turbine. The steam also powers the pistons in a partially self-sustaining cycle. No evidence of sCO2 or other advanced power conversion cycles being considered.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: IAEA FEC 2025 — "compressional heating"; APS 2018 overview — 3 orders of magnitude volume compression; https://generalfusion.com/fusion-technology/
- **Notes**: The plasma starts as a compact toroid (spherical torus) at ~0.1 keV and is driven to fusion conditions (~10 keV) by implosion of the liquid metal liner. This is characteristic MIF — plasma driven to fusion by external compression. LM26 April 2025 results confirmed ion temperature and density increases during compression.

### Magnet Type
- **Value**: `Self-confined`
- **Confidence**: high
- **Citation**: Wikipedia (General Fusion) — "magnetic fields supported by internal plasma currents and eddy currents in the wall"; schema definition for MTF
- **Notes**: The plasma is a compact toroid with internal magnetic fields sustained by plasma currents. The confining compression comes from the liquid metal liner driven by pistons, not from external magnetic coils. LM26 uses electromagnetic theta-pinch coils for compression (as a demo surrogate), but these are not confinement magnets — they drive the liner.

### Tritium Breeding
- **Value**: `Liquid metal wall`
- **Confidence**: high
- **Citation**: FST 2025 paper (DOI: 10.1080/15361055.2025.2526266) — evaluates both PbLi and pure Li as liquid metal wall/breeder; https://generalfusion.com/fusion-technology/ — liquid metal wall "breed[s] fuel"; https://www.fusionconclusion.com/how-general-fusions-reactor-will-work-or-wont/ — TBR target ~1.5
- **Notes**: The flowing liquid metal serves as both the compression liner AND the tritium breeder. This is distinct from a contained blanket — the liquid metal is the structural wall itself. Both lead-lithium eutectic (LLE) and pure lithium (Li) remain under evaluation for the commercial plant (FST 2025). TBR analysis differs: Li design has >60% of tritium inventory in blanket; LLE design has >80% in isotope separation system. TBR target ~1.5.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — liquid metal wall "absorb[s] neutrons and protect[s] the machine from fusion damage, breed[s] fuel and provide[s] efficient heat transfer"; FST 2025 paper confirms dual-purpose liquid metal
- **Notes**: The liquid metal liner serves triple duty: compression medium, neutron absorber/shield, and tritium breeder. 14.1 MeV D-T neutrons are produced but the thick liquid metal liner (~meters of lithium/lead-lithium) provides effective shielding. This is the canonical example of "integrated blanket/shield" — no separate blanket and shield structures.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: IAEA FEC 2025 — pulsed compression events; https://generalfusion.com/fusion-technology/ — "pulsed at 1-10 Hz"; https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951 — "once per second in a commercial plant"
- **Notes**: Discrete compression events. Each pulse: inject plasma, compress with pistons, fusion burn, extract energy, reset. Compression timescale ~1 ms. Well below the 5-minute threshold for quasi-steady.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-demo-plant/; https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/ — "~1 cycle per second"; https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951
- **Notes**: All sources consistently cite ~1 Hz for the commercial target. LM26 currently operates at much lower rate (approximately once per day). The original "1-10 Hz" range from early descriptions appears to have narrowed to ~1 Hz in current planning.

### Driver Technology
- **Value**: `Pneumatic pistons + liquid metal`
- **Confidence**: high
- **Citation**: FST 2025 paper — "pneumatic piston drivers"; https://generalfusion.com/fusion-technology/; schema example vocabulary
- **Notes**: Steam-driven pistons (dozens to hundreds) arranged around a spherical vessel compress a vortex of liquid metal (lithium or lead-lithium). The pistons must fire with precise synchronization to create a symmetric compression wave. Commercial cavity is ~4 m diameter (FST 2025). This is General Fusion's distinguishing engineering bet — replacing lasers or pulsed power with mechanical compression.

## Remaining Gaps

All 12 differentiation columns are filled at high confidence with multiple corroborating sources. No schema-level gaps remain.

Minor areas where additional detail could be valuable for later stages:

1. **Liquid metal composition (commercial)**: Both lead-lithium eutectic and pure lithium remain under evaluation (FST 2025). Neither has been selected for the commercial plant. This doesn't affect schema values (both qualify as `Liquid metal wall`) but matters for Stage 2 cost modeling.

2. **Repetition rate range**: The original concept description says "1-10 Hz" but all detailed sources cite ~1 Hz for commercial. Whether higher rep rates are targeted in later iterations is unclear.

3. **Power output target**: Confirmed as 300 MWe (from General Fusion commercialization page). Sufficient for Stage 2 scoping.

4. **Power conversion specifics**: No detail on steam cycle parameters (temperature, pressure, efficiency). Standard Rankine cycle is confirmed but specific cycle optimization is not published.

## Key Sources

1. [FST 2025: Fuel Cycles for Li and PbLi Walls in MTF Power Plant](https://www.tandfonline.com/doi/full/10.1080/15361055.2025.2526266) — peer-reviewed, confirms pneumatic pistons, ~4 m cavity, both Li/PbLi under evaluation, tritium inventory analysis
2. [IAEA FEC 2025: LM26 Abstract (Hildebrand et al.)](https://conferences.iaea.org/event/392/contributions/35891/attachments/19864/33918/IAEA%20FEC%202025%20LM26%20Abstract%20-%20Hildebrand.pdf) — 50% scale, 10 keV target, Lawson criterion 2026 target
3. [General Fusion Technology Page](https://generalfusion.com/fusion-technology/) — primary company source for concept description, liquid metal wall, tritium breeding
4. [General Fusion: Commercialization Path](https://generalfusion.com/commercialization-path/) — 300 MWe target
5. [APS 2018: MTF at General Fusion Overview (PDF)](https://generalfusion.com/wp-content/uploads/2022/04/aps-2018-magnetized-target-fusion-overview.pdf) — compression parameters (density, temperature, B-field)
6. [COMSOL: Compressing Timeline to Fusion Future](https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951) — commercial rep rate, liquid metal wall details
7. [Interesting Engineering: Steam-Powered Piston System (2025)](https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor) — steam-driven piston details, energy capture cycle
8. [Hackaday: General Fusion Claims Success (2025)](https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/) — LM26 results, commercial rep rate target
9. [General Fusion: LM26 First Plasma Compression (April 2025)](https://generalfusion.com/post/watch-general-fusions-lm26-achieves-first-plasma-compression/) — lithium compression milestone
10. [General Fusion: Peer-reviewed Confinement Time](https://generalfusion.com/post/peer-reviewed-publication-confirms-plasma-energy-confinement-time-for-lm26/) — >10 ms energy confinement
11. [Fusion Conclusion: How General Fusion's Reactor Will Work](https://www.fusionconclusion.com/how-general-fusions-reactor-will-work-or-wont/) — TBR target ~1.5, design details
12. [General Fusion: Liquid Wall Compression Publication](https://generalfusion.com/post/general-fusion-confirms-liquid-wall-compression-technology-for-commercial-magnetized-target-fusion-in-new-scientific-publication/) — peer-reviewed validation
13. [General Fusion: Neutron Yield Publication](https://generalfusion.com/post/general-fusion-confirms-significant-fusion-neutron-yield-and-plasma-stability-during-mtf-compression-experiment-series-with-new-peer-reviewed-publication/) — experimental results
14. [COMSOL: Magnetomechanical Compression Paper](https://www.comsol.com/paper/magnetomechanical-compression-of-a-solid-lithium-liner-for-magnetized-target-fusion-mtf-136162) — LM26 electromagnetic compression details
15. [LANL MTF Page](https://fusionenergy.lanl.gov/Physics/Magnetized_Target_Fusion.htm) — LANL MTF program, FRX-L experiments
16. [ARPA-E: HyperJet Fusion PJMIF](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/plasma-guns-magnetized-fuel-targets-pjmif) — related MTF experiments
17. [TechCrunch: General Fusion Fires Up Steampunk Reactor (2025)](https://techcrunch.com/2025/03/11/general-fusion-fires-up-its-newest-steampunk-fusion-reactor/) — LM26 demo context
18. [General Fusion Wikipedia](https://en.wikipedia.org/wiki/General_Fusion) — Marshall gun, compact toroid details
19. [Metal Tech News: General Fusion Compresses Plasma with Lithium (2025)](https://www.metaltechnews.com/story/2025/05/14/tech-bytes/general-fusion-compresses-plasma-with-lithium/2278.html) — LM26 lithium compression results
20. [World Nuclear News: Prototype Demonstrates Plasma Compression](https://www.world-nuclear-news.org/Articles/Prototype-machine-demonstrates-plasma-compression) — demo milestone coverage
21. [Innovation News Network: First MTF Plasma](https://www.innovationnewsnetwork.com/canadas-general-fusion-achieves-first-magnetised-target-fusion-plasma/56354/) — LM26 milestone
