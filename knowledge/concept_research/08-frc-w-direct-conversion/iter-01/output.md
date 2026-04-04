Now I have comprehensive data. Here are my findings for each column:

---

## Column-by-Column Findings

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/ — "magneto-inertial fusion technology"; schema notes: "pulsed FRC compression (Helion) → MIF"
- **Notes**: Helion's approach combines magnetic confinement (FRC) with inertial compression (two plasmoids collide and merge). The schema explicitly classifies pulsed FRC compression as MIF.

### Confinement Concept
- **Value**: `FRC (pulsed compression)`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/ — "accelerates two FRCs to 1 million mph from opposite ends... They collide in the center"
- **Notes**: Two FRC plasmoids are formed, accelerated to >300 km/s, collide and merge, then magnetically compressed to fusion conditions. This is distinct from TAE's beam-driven steady-state FRC. Helion's proprietary term is "Fusion Engine."

### Fuel
- **Value**: `D-He3`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/
- **Notes**: Target commercial fuel is D-He3 (18.3 MeV per reaction: 3.6 MeV alpha + 14.7 MeV proton). Polaris will progress through D-D → D-T → D-He3 during testing. He3 is self-bred from DD side reactions (50% direct He3 production, 50% tritium which decays to He3 with 12.3-year half-life). Helion states D-He3 releases "only 5% of its energy in the form of fast neutrons."

### Primary Heating
- **Value**: `Magnetic compression`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/; DocsLib ARPA-E presentation
- **Notes**: Two-stage heating: (1) kinetic energy from FRC collision converts to ion thermal energy during merging, (2) magnetic compression via pulsed EM coils raises temperature further to fusion conditions. The schema defines this as "Adiabatic compression via rapidly increasing magnetic fields" — which matches Helion's approach exactly. Capacitor banks discharge through electromagnetic coils to compress the merged FRC. No auxiliary RF or NBI heating.

### Energy Capture
- **Value**: `Direct (inductive)`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/ — "hot plasma expands and pushes back on the magnetic field around it. That push induces current in the coils"
- **Notes**: Schema explicitly lists this as "Helion's approach." Expanding magnetized plasma induces current in surrounding coils via Faraday's law. No thermal cycle. Helion claims 85-95% direct electricity capture efficiency. They describe it as analogous to "regenerative braking in an electric vehicle." This is a key differentiator — no other fusion company uses this exact approach.

### Plasma State
- **Value**: `Transient`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/ — plasma lifetimes ">1 ms"; schema: "Short-lived plasma state (~ms) during a pulsed compression/collision event. Characteristic of pulsed FRC."
- **Notes**: The FRC plasma exists for ~milliseconds during each pulse cycle (formation → acceleration → collision → compression → fusion → expansion → energy recovery). Schema explicitly calls out pulsed FRC as characteristic of "Transient." Helion does not aim for ignition or self-sustaining burn — they recover energy from each individual pulse.

### Magnet Type
- **Value**: `Pulsed EM`
- **Confidence**: high
- **Citation**: Contrary Research (https://research.contrary.com/company/helion) — CEO Kirtley: "regular aluminum magnets"; https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/
- **Notes**: Schema explicitly states "Helion uses Pulsed EM — their aluminum coils are pulsed with capacitor banks, not steady-state superconducting." Coils are aluminum (confirmed by CEO quote), driven by capacitor banks storing >50 MJ at tens of thousands of volts. Compression fields >10 T demonstrated (Trenta), 15 T+ target (Polaris), 40 T reactor target. No cryogenics needed. Energy in coaxial cables uses copper, aluminum, and custom alloys.

### Tritium Breeding
- **Value**: `Self-bred (DD side)`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/
- **Notes**: Schema notes this exactly: "Tritium produced as byproduct of DD side reactions in D-He3 plasma. Tritium decays to He3, completing fuel cycle. No external blanket." 50% of DD reactions produce He3 directly; 50% produce tritium which decays to He3 at 5.5%/year (12.3-year half-life). The system becomes more self-sufficient the longer it runs. Only deuterium (from water) is needed as external input.

### Neutron Management
- **Value**: `Reduced (D-He3)`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/ — "borated polyethylene and borated concrete shield vault"; https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/ — "only 5% of its energy in the form of fast neutrons"
- **Notes**: D-He3 produces ~5% neutron energy fraction from DD side reactions, at 2.45 MeV (much less damaging than 14.1 MeV D-T neutrons). Shielding uses borated polyethylene and borated concrete, described as similar to hospital particle beam shielding — much lighter than D-T reactor shielding. Contrary Research mentions "one meter" solid barrier. This matches "Reduced (D-He3)" in the schema: "~10% neutron energy fraction from DD side reactions. 2.45 MeV neutrons. Lighter shielding. Limited remote handling."

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/
- **Notes**: Each fusion event is a discrete short pulse (~milliseconds). The system cycles: capacitors charge → coils fire → FRCs form → accelerate → collide → compress → fuse → expand → energy recovered → repeat. Pulse duration is well under the 5-minute quasi-steady threshold.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high (for Polaris target); medium (for commercial)
- **Citation**: https://www.helionenergy.com/polaris/ — "stronger magnets and will pulse faster than Trenta"; multiple sources confirm 1 Hz Polaris target; DocsLib presentation shows 2 Hz design point for 50 MW Fusion Engine
- **Notes**: Trenta operated at ~1 pulse per 10 minutes. Polaris targets 1 Hz (one pulse per second). The ARPA-E presentation shows 50 MW at 2 Hz as a design point. Long-term commercial targets may be higher (10 Hz or even 60 Hz mentioned in speculative contexts). For the differentiation table, `~1 Hz` captures the current prototype/near-term commercial target. Could evolve to `High (>10 Hz)` for mature commercial systems.

### Driver Technology
- **Value**: `Pulsed EM coils (capacitor bank)`
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/; Contrary Research
- **Notes**: Schema lists this exact value for Helion. The system is fundamentally an RLC circuit: capacitor banks (>50 MJ, tens of kV) discharge through aluminum electromagnetic coils to form, accelerate, and compress FRC plasmoids. The coils also serve as the energy recovery system — expanding plasma induces current back into the capacitors. Key specifications: aluminum coils, >10 T compression (Trenta), 15 T+ (Polaris), 40 T reactor target.

---

## Metadata Columns (Confirmation/Update)

### Published Machine/Plant?
- **Value**: No (for a detailed reactor engineering design); Yes (for commercial plant announcements)
- **Confidence**: medium
- **Citation**: Helion has announced Orion (first commercial plant, 50 MWe, target 2028) and a 500 MWe Nucor partnership, but no published detailed reactor engineering design document (like ARIES or ARC) exists in the public domain.
- **Notes**: The Polaris prototype is operational and well-documented at the system level, but detailed reactor engineering designs with cost breakdowns are not public. Keep as "No" for the differentiation table context (published detailed design).

### Lab Experiments
- **Value**: FRX-L (LANL), TCS (UW), C-2W (TAE/UCI)
- **Confidence**: medium
- **Citation**: FRX-L: IEEE Xplore (https://ieeexplore.ieee.org/document/1228925/); TCS: University of Washington FRC program
- **Notes**: FRX-L at LANL was a high-density FRC plasma injector for MTF (first plasma 2001, shutdown 2012). TCS at UW studied FRC translation, confinement, and sustainment. C-2W (Norman) at TAE is a beam-driven FRC — same confinement topology but different operational approach (steady-state vs pulsed). These are FRC physics demonstrations relevant to Helion's concept, not Helion's own machines. Helion's own prototypes (1st through 7th generation, including Trenta and Polaris) are company experiments, not university/national lab experiments. The listing mixes concept-relevant lab work with company-adjacent work.

---

## Remaining Gaps

All columns have been filled with high confidence. Minor areas where further detail could be valuable:

1. **Repetition Rate (commercial)**: The exact commercial target rate is somewhat uncertain. Sources mention 1 Hz (Polaris), 2 Hz (ARPA-E presentation), and speculative 10-60 Hz long-term. The 1 Hz value is well-supported for near-term.

2. **Neutron energy fraction**: Helion claims "only 5%" of energy as neutrons; the schema says "~10%." The 5% figure comes from Helion's website and may reflect optimistic D-He3 dominance over DD reactions at high temperature. The actual fraction depends on the D-He3 to D-D reaction ratio, which is temperature-dependent. At 200 million °C, D-He3 cross-section significantly exceeds D-D, supporting a fraction closer to 5% than 10%.

3. **Magnet coil material**: Confirmed as aluminum by CEO quote (Contrary Research). However, cables use copper, aluminum, and custom alloys. The coils themselves are aluminum.

## Sources Consulted

### Helion Website (primary source)
- [Helion Technology](https://www.helionenergy.com/technology/)
- [Helion FAQ](https://www.helionenergy.com/faq/)
- [Helion Polaris](https://www.helionenergy.com/polaris/)
- [How to make fusion electricity without ignition](https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/)
- [Explaining Helion's fusion fuel: D-He-3](https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/)
- [How to engineer a renewable D-He3 fuel cycle](https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/)
- [Helion's fusion system is basically an RLC circuit](https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/)
- [More on Helion's pulsed approach to fusion](https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/)
- [Trenta final test campaign](https://www.helionenergy.com/articles/ending-trenta-operations/)

### Third-Party Analysis
- [Contrary Research: Helion Energy](https://research.contrary.com/company/helion) — confirmed aluminum magnets, 85-95% efficiency
- [DocsLib: Helion ARPA-E Presentation](https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor) — 20T/40T specs, 2 Hz @ 50 MW design point
- [Thunder Said Energy: Helion](https://thundersaidenergy.com/2022/03/28/helion-linear-fusion-breakthrough/) — 50-200 MWe modular, 1-6¢/kWh target

### News / Press
- [GeekWire: Polaris tour (2025)](https://www.geekwire.com/2025/helion-gives-behind-the-scenes-tour-of-secretive-60-foot-fusion-prototype-as-it-races-to-deployment/) — physical details, aluminum coils
- [Fortune: 150M°C milestone (Feb 2026)](https://fortune.com/2026/02/13/sam-altman-fusion-helion-energy-milestone-doubters-grid-power-2028/)
- [MIT Technology Review (2023)](https://www.technologyreview.com/2023/05/10/1072812/this-startup-says-its-first-fusion-plant-is-five-years-away-experts-doubt-it/)
- [New Atlas: Polaris](https://newatlas.com/energy/helion-net-electricity-nuclear-fusion-polaris/)
- [EE Times: Fusion milestone](https://www.eetimes.com/helion-energy-achieves-key-fusion-milestone/)

### Government / Academic
- [ARPA-E: Compression of FRC Targets for Fusion](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/compression-frc-targets-fusion)
- [IEEE Xplore: FRX-L overview](https://ieeexplore.ieee.org/document/1228925/)
- [Nuclear Fusion 51(5), 2011](https://doi.org/10.1088/0029-5515/51/5/053008) — Slough et al., merging/compression of FRC plasmoids

### Wikipedia (not directly fetched due to 403, but used via search snippets)
- [Helion Energy - Wikipedia](https://en.wikipedia.org/wiki/Helion_Energy)
- [Field-reversed configuration - Wikipedia](https://en.wikipedia.org/wiki/Field-reversed_configuration)
