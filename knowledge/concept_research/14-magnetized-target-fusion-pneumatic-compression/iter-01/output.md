Now let me write the full dossier.

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — "Magnetized Target Fusion (MTF) technology" combining magnetic confinement with inertial compression
- **Notes**: MTF/MIF are synonymous terms. General Fusion explicitly positions between MCF and ICF — magnetized plasma compressed by an external mechanical driver at intermediate density/timescale.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; schema vocabulary
- **Notes**: The commercial design uses steam-driven pistons to compress liquid metal liner around magnetized plasma. "Pneumatic" in the schema captures the mechanical compression approach. The pistons are steam-driven (not electrically driven or laser-driven). LM26 demo uses electromagnetic compression of solid lithium as a surrogate, but the commercial concept is mechanical/pneumatic.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — tritium breeding is integral to the design; 14.1 MeV neutrons are produced
- **Notes**: Standard D-T fuel cycle. Tritium breeding from liquid lithium is a core design feature.

### Primary Heating
- **Value**: `Mechanical compression`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor — "steam-driven pistons" compress the liquid metal liner which compresses the plasma
- **Notes**: The plasma is initially formed by a Marshall gun (coaxial plasma gun) as a compact toroid (spherical tokamak), but the primary heating to fusion-relevant temperatures comes from mechanical compression of the liquid metal liner driven by steam pistons. The initial plasma formation is at ~400 eV; compression must raise this to ~10 keV (fusion conditions). LM26 uses electromagnetic compression as a demo stand-in, but the commercial heating mechanism is mechanical compression.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951 — "liquid metal wall of the vessel" captures neutron energy; https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor — "lithium flows through heat exchanger → generates steam → spins generator for electricity"
- **Notes**: Standard thermal cycle: fusion neutrons heat the liquid metal liner → liquid metal pumped through heat exchanger → steam Rankine cycle → turbine. The steam also powers the pistons in a partially self-sustaining cycle.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — plasma is mechanically compressed to fusion conditions
- **Notes**: The plasma starts as a compact toroid (spherical tokamak) at ~400 eV and is driven to fusion conditions by implosion of the liquid metal liner. This is characteristic MIF — plasma driven to fusion by external compression, not self-sustaining burn or steady-state confinement.

### Magnet Type
- **Value**: `Self-confined`
- **Confidence**: high
- **Citation**: Schema definition — "mechanically compressed (MTF). No external confinement magnets." The compact toroid plasma is self-magnetized (internal currents sustain magnetic field). The liquid metal liner provides the compression, not external magnets.
- **Notes**: The plasma is a compact toroid (spherical tokamak) with internal magnetic fields sustained by plasma currents. The confining compression comes from the liquid metal liner driven by pistons, not from external magnetic coils. LM26 uses electromagnetic coils for compression as a surrogate, but in the commercial design the confinement/compression is mechanical. The schema explicitly lists General Fusion as `Self-confined`. The plasma does have magnetic fields (it's a compact toroid), but these are self-generated, not from external superconducting magnets.

### Tritium Breeding
- **Value**: `Liquid metal wall`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — liquid metal wall "breed[s] fuel"; https://www.fusionconclusion.com/how-general-fusions-reactor-will-work-or-wont/ — tritium breeding ratio target ~1.5
- **Notes**: The flowing liquid metal (lithium or lead-lithium) serves as both the compression liner AND the tritium breeder. This is distinct from a contained blanket — the liquid metal is the structural wall itself. Original design used lead-lithium (PbLi); current demo uses pure lithium for lower radiation losses; commercial plant may use either. TBR target ~1.5. Fits `Liquid metal wall` precisely — the schema notes this as "Flowing liquid metal serves dual purpose as structural wall/liner AND tritium breeder. Distinct from a contained blanket."

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — liquid metal wall "absorb[s] neutrons and protect[s] the machine from fusion damage, breed[s] fuel and provide[s] efficient heat transfer"
- **Notes**: The liquid metal liner serves triple duty: compression medium, neutron absorber/shield, and tritium breeder. The schema notes that General Fusion's liquid metal wall qualifies for `Integrated blanket/shield` — the blanket explicitly serves dual purpose. 14.1 MeV D-T neutrons are produced but the thick liquid metal liner (~meters of lithium/lead-lithium) provides effective shielding.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/ — "pulsed at 1-10 Hz"; https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951 — "once per second in a commercial plant"
- **Notes**: Discrete compression events. Each pulse: inject plasma → compress with pistons → fusion burn → extract energy → reset. Pulse duration is sub-second (compression takes ~1 ms). Well below the 5-minute threshold for quasi-steady.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951 — commercial plant repeats "once per second"; https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/ — commercial goal "~1 cycle per second"
- **Notes**: Current LM26 operates at approximately one cycle per day. The original concept description said "1-10 Hz" but detailed sources consistently cite ~1 Hz for the commercial target.

### Driver Technology
- **Value**: `Pneumatic pistons + liquid metal`
- **Confidence**: high
- **Citation**: https://generalfusion.com/fusion-technology/; https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor; schema example vocabulary
- **Notes**: Steam-driven pistons (dozens to hundreds) arranged around a spherical vessel compress a vortex of liquid metal (lithium or lead-lithium). The pistons must fire with precise synchronization to create a symmetric compression wave. This is General Fusion's distinguishing engineering bet — replacing lasers or pulsed power with mechanical compression. The schema lists exactly `Pneumatic pistons + liquid metal` as General Fusion's driver technology.

### Published Machine/Plant?
- **Value**: No (confirming initial CSV)
- **Confidence**: high
- **Citation**: No published reactor/plant design found. LM26 is a demonstration machine, not a commercial plant design.
- **Notes**: General Fusion has published extensive experimental results (34 peer-reviewed papers, Nuclear Fusion journal publications) but no published commercial power plant design with detailed specifications.

### Lab Experiments
- **Value**: LANL FRX-L (FRC + metal liner compression), NRL Linus (rotating liquid metal liner), HyperJet Fusion / PLX at LANL (plasma jet driven MTF)
- **Confidence**: high
- **Citation**: https://fusionenergy.lanl.gov/Physics/Magnetized_Target_Fusion.htm (LANL MTF program); https://en.wikipedia.org/wiki/Linus_(fusion_experiment) (NRL Linus); https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/plasma-guns-magnetized-fuel-targets-pjmif (HyperJet/PLX)
- **Notes**: The CSV listed "LANL MTF (Theta Pinch + liner), HyperJet Fusion (plasma jet driven MTF)" which is accurate. LANL's FRX-L experiment used theta-pinch-formed FRC compressed by metal liner Z-pinch, in collaboration with AFRL. NRL's Linus program (1970s-80s) pioneered the rotating liquid metal liner concept that General Fusion builds upon. HyperJet Fusion is developing PJMIF with a 36-gun demo at LANL's PLX facility.

---

## Remaining Gaps

All 12 differentiation columns have been filled with high confidence. No significant gaps remain. Minor areas where additional detail could be valuable:

1. **Liquid metal composition (commercial)**: General Fusion's original design used lead-lithium (PbLi), current demo uses pure lithium. The commercial plant composition hasn't been definitively stated — it may return to PbLi for materials compatibility. This doesn't affect the schema values (both qualify as `Liquid metal wall`) but is worth tracking.

2. **Repetition rate range**: The original concept description says "1-10 Hz" but all detailed sources cite ~1 Hz for commercial. Whether higher rep rates are targeted in later iterations is unclear.

3. **Power output target**: Only "150,000 homes" mentioned (roughly 100-200 MWe depending on assumptions). No specific GW-scale thermal power or net electric output has been published.

## Sources Consulted

- [General Fusion Technology Page](https://generalfusion.com/fusion-technology/)
- [General Fusion Wikipedia](https://en.wikipedia.org/wiki/General_Fusion) (blocked by 403, info from search snippets)
- [Magnetized Target Fusion Wikipedia](https://en.wikipedia.org/wiki/Magnetized_target_fusion) (blocked by 403, info from search snippets)
- [Hackaday: General Fusion Claims Success (2025)](https://hackaday.com/2025/03/27/general-fusion-claims-success-with-magnetized-target-fusion/)
- [Interesting Engineering: Steam-Powered Piston System (2025)](https://interestingengineering.com/energy/steam-driven-nuclear-fusion-reactor)
- [TechCrunch: General Fusion Fires Up Steampunk Reactor (2025)](https://techcrunch.com/2025/03/11/general-fusion-fires-up-its-newest-steampunk-fusion-reactor/)
- [COMSOL: Compressing Timeline to Fusion Future](https://www.comsol.com/story/compressing-the-timeline-to-a-fusion-future-141951)
- [Fusion Conclusion: How General Fusion's Reactor Will Work](https://www.fusionconclusion.com/how-general-fusions-reactor-will-work-or-wont/)
- [General Fusion: Liquid Wall Compression Publication](https://generalfusion.com/post/general-fusion-confirms-liquid-wall-compression-technology-for-commercial-magnetized-target-fusion-in-new-scientific-publication/)
- [General Fusion: Neutron Yield Publication](https://generalfusion.com/post/general-fusion-confirms-significant-fusion-neutron-yield-and-plasma-stability-during-mtf-compression-experiment-series-with-new-peer-reviewed-publication/)
- [General Fusion: LM26 Assembly Complete](https://generalfusion.com/post/building-the-future-of-energy-lm26-assembly-complete/)
- [COMSOL: Magnetomechanical Compression Paper](https://www.comsol.com/paper/magnetomechanical-compression-of-a-solid-lithium-liner-for-magnetized-target-fusion-mtf-136162)
- [LANL MTF Page](https://fusionenergy.lanl.gov/Physics/Magnetized_Target_Fusion.htm)
- [ARPA-E: HyperJet Fusion PJMIF](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/plasma-guns-magnetized-fuel-targets-pjmif)
- [Laberge 2013 PDF](https://generalfusion.com/wp-content/uploads/2022/05/Laberge-2013-Acoustically-Driven-Magnetized-Target-Fusion.pdf) (PDF could not be parsed by WebFetch)
- [Metal Tech News: General Fusion Compresses Plasma with Lithium (2025)](https://www.metaltechnews.com/story/2025/05/14/tech-bytes/general-fusion-compresses-plasma-with-lithium/2278.html)
- [World Nuclear News: Prototype Demonstrates Plasma Compression](https://www.world-nuclear-news.org/Articles/Prototype-machine-demonstrates-plasma-compression)
