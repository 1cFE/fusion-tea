# Concept Dossier: Sheared-Flow Stabilized Z-Pinch (D-T)

**Company**: Zap Energy
**Founded**: 2017 (spinoff from University of Washington FuZE program)
**HQ**: Everett, WA (with facilities in Mukilteo, WA)
**Funding**: ~$330M total (Series C); DOE Milestone-Based Fusion Development Program participant (May 2023)
**Key People**: Uri Shumlak (co-founder, UW professor — pioneered sheared-flow stabilization), Brian A. Nelson (CTO, UW professor), Benj Conway (co-founder, CEO)

---

## Metadata

- **Concept Name**: Sheared-Flow Stabilized Z-Pinch (D-T)
- **Companies**: Zap Energy
- **Description**: Axial current creates self-pinching magnetic field; sheared axial plasma flow stabilizes MHD instabilities. No external magnets required. Pulsed operation at ~10 Hz with liquid metal (LiPb) walls serving as electrode, blanket, shield, and coolant. Compact geometry (~3 m tall reactor).
- **Published Machine/Plant?**: Yes — a conceptual reactor design has been published in "Engineering Paradigms for Sheared-Flow-Stabilized Z-Pinch Fusion Energy" (Fusion Science and Technology, 2023) describing a 190 MWt reactor with LiPb blanket, 10 Hz rep rate, and steam cycle. Not a detailed engineering plant design, but a published reactor concept.
- **Lab Experiments**: ZaP (UW), ZaP-HD (UW), FuZE (UW — 1-3 keV electron temps, LLNL-verified neutrons), FuZE-3 (Zap Energy — gigapascal plasma pressures), FuZE-Q (targeting Q=1), Century (integrated engineering demo with liquid metal and repetitive pulsed power)

---

## Differentiation Columns

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Schema notes: "Z-pinch concepts that use self-generated fields are MFE"; IEEE Spectrum title: "Magnetic-Confinement Fusion Without the Magnets"; Zap Energy website describes it as magnetic confinement via self-generated fields
- **Notes**: The plasma is confined by its own self-generated magnetic field (from axial current). This is magnetic confinement, even though no external magnets are used. The schema explicitly classifies Z-pinch as MFE. The initial CSV listed "Magnetized Target Fusion" (MIF) but this is incorrect — there is no external compression driver. The confinement is purely magnetic (self-field).

### Confinement Concept
- **Value**: `Z-pinch (sheared-flow)`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works; schema vocabulary lists this exact value
- **Notes**: Exact match to schema vocabulary. Proprietary feature is the sheared-flow stabilization pioneered by Uri Shumlak at UW, which stabilizes the Z-pinch against MHD kink and sausage instabilities.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works — "deuterium and tritium isotopes"; Engineering Paradigms paper describes D-T fusion at 190 MWt with tritium breeding
- **Notes**: D-T is the target commercial fuel. Current experiments use deuterium (FuZE) or hydrogen/helium (Century).

### Primary Heating
- **Value**: `Ohmic (self-pinch)`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works — "the higher the current sent through the plasma, the tighter it will be constricted by magnetic fields and the hotter and denser it will become"; schema description matches: "Plasma current provides both confinement and heating via resistive dissipation"
- **Notes**: The large axial current (~650 kA to 1.5 MA) both confines the plasma (via J×B pinch force) and heats it ohmically. There is no separate heating system (no NBI, no RF). The compression from the pinch effect also contributes adiabatic heating. This is the defining feature — the same current does confinement and heating simultaneously.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: medium
- **Citation**: Blog analysis at benbridgerengineering.com (2023) states "LiPb to steam cycle"; Engineering Paradigms paper describes LiPb as primary heat transfer medium
- **Notes**: The published reactor concept uses LiPb liquid metal as the heat transfer medium, feeding a steam cycle. This is described in secondary analysis of the Engineering Paradigms paper. The company website does not explicitly state "steam" — it says liquid metal walls "capture fusion energy." The thermal cycle choice (Rankine vs sCO2) may evolve, but steam is the currently published baseline. Confidence is medium because the primary source (Taylor & Francis paper) was behind a paywall and the "steam" detail comes from a third-party summary.

### Plasma State
- **Value**: `Pinch`
- **Confidence**: high
- **Citation**: Schema definition: "Self-compressed plasma column maintained by its own current. Characteristic of Z-pinch." This is the exact use case.
- **Notes**: The plasma column (~50 cm long, ~1 mm diameter) is self-compressed by the J×B force from its own axial current. Beta ≈ 1 (plasma pressure equals magnetic pressure). The sheared flow extends the pinch lifetime but doesn't change the fundamental plasma state.

### Magnet Type
- **Value**: `Self-confined`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works — "confines plasma using the magnetic field generated by a powerful electrical current in the plasma instead of using external magnets"; schema: "Plasma generates its own confining magnetic field (Z-pinch, DPF)"
- **Notes**: No external magnets of any kind. The confining Bθ field is generated by the axial plasma current itself. This is a core differentiator — eliminates superconducting magnet cost, cryogenic systems, and MHD forces on liquid metal coolant. The schema specifically lists Z-pinch as the example for `Self-confined`.

### Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: Engineering Paradigms paper (2023): LiPb eutectic (17% Li, 83% Pb), TBR ~1.1 with 3 m blanket; https://www.zapenergy.com/how-it-works — "mix of lead and lithium in the walls will produce tritium"
- **Notes**: The LiPb serves quadruple duty: outer electrode, heat transfer medium, biological shield, and tritium breeder. Lead provides neutron multiplication. The weir-wall design allows LiPb to cascade under gravity to form the first wall. TBR of 1.1 is marginal but positive. The absence of external magnets greatly simplifies liquid metal handling (no MHD drag).

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: Engineering Paradigms paper: LiPb blanket provides tritium breeding AND biological shielding; Monte Carlo simulations show neutron irradiation confined near pinch region
- **Notes**: The thick (~3 m) LiPb blanket serves as both tritium breeder and neutron shield in a single integrated system. The compact plasma geometry concentrates neutron emission, and the liquid metal surrounding the pinch absorbs and thermalizes neutrons. No separate shield structure is described. Schema note: "Use Integrated blanket/shield when the blanket explicitly serves dual purpose" — this is exactly the case here.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works — "ten plasma pulses per second"; Engineering Paradigms paper: 10 Hz pulsed operation
- **Notes**: Each Z-pinch event is a discrete pulse lasting on the order of microseconds to milliseconds. At 10 Hz, the system fires 10 pulses per second. This is clearly pulsed (not quasi-steady — individual pulses are far shorter than 5 minutes). Century demo has operated at 0.1-0.2 Hz; the 10 Hz target is for the commercial reactor.

### Repetition Rate
- **Value**: `~10 Hz`
- **Confidence**: high
- **Citation**: https://www.zapenergy.com/how-it-works — "ten plasma pulses per second"; Engineering Paradigms paper: 10 Hz
- **Notes**: 10 Hz is the target commercial repetition rate. Current experimental devices operate at much lower rates (Century at 0.1-0.2 Hz demonstrated, with targets up to higher rates). The 10 Hz target determines the time-averaged power output from the 190 MWt-per-pulse reactor concept.

### Driver Technology
- **Value**: `Pulsed power (sheared-flow Z-pinch)`
- **Confidence**: high
- **Citation**: FuZE-Q specs: ~1 MJ capacitor bank, up to 1.5 MA, passive pulse-forming networks (PFNs); https://www.zapenergy.com/how-it-works
- **Notes**: The driver is a capacitor bank discharging through pulse-forming networks to deliver shaped current waveforms (fast rise, long flattop) to the plasma. Target currents: 650 kA–1.5 MA. Wall-plug to plasma efficiency ~70%. The PFN design with inductively isolated capacitors allows flexible waveform shaping. This is the same vocabulary value used in the schema example for Zap Energy.

---

## Remaining Gaps

All 12 columns have been filled with medium or high confidence. Specific areas where additional detail could improve confidence:

1. **Energy Capture** (medium confidence): The "LiPb to steam cycle" detail comes from a third-party blog summary of the Engineering Paradigms paper, not directly from the paper itself (paywalled). Direct access to the paper would confirm whether steam Rankine is explicitly stated or if other thermal cycles (sCO2) are considered. However, given LiPb operating temperatures and the early stage of the concept, steam Rankine is the most likely baseline.

2. **Published Machine/Plant?**: Changed from "No" (initial CSV) to "Yes" based on the Engineering Paradigms paper (2023) which describes a conceptual reactor at 190 MWt. This is not a detailed plant design (no turbine island, no BoP), but it is a published reactor concept with specific parameters.

3. **Confinement Family**: Changed from "Magnetized Target Fusion" (initial CSV) to "MFE" per schema rules. The Z-pinch uses self-generated magnetic fields for confinement — there is no external compression driver characteristic of MIF. The schema explicitly states Z-pinch is MFE.

---

## Sources Consulted

### Primary sources (yielded key data)
- [Zap Energy — How It Works](https://www.zapenergy.com/how-it-works) — fuel, operation mode, rep rate, no-magnet design, driver
- [Engineering Paradigms for SFS Z-Pinch Fusion Energy (2023)](https://www.tandfonline.com/doi/full/10.1080/15361055.2023.2209131) — reactor specs (190 MWt, LiPb, TBR, 10 Hz, steam cycle). Paywalled; details from search snippets and third-party summaries.
- [The Zap Energy approach to commercial fusion (Physics of Plasmas, 2023)](https://pubs.aip.org/aip/pop/article/30/9/090603/2911595/The-Zap-Energy-approach-to-commercial-fusion) — overview paper. Paywalled.
- [Zap Energy — Century demo press release](https://www.zapenergy.com/news/zap-attracts-130m-as-demo-system-begins-operations) — Century specs, liquid bismuth, pulsed power demo
- [Century: Lightning Strikes 12 Times Per Minute](https://www.zapenergy.com/news/lightning-strikes-12-times-per-minute-century) — Century 0.2 Hz, 500 kA, 100+ shots
- [DOE Certifies Zap Energy Milestone](https://www.zapenergy.com/news/doe-century-milestone) — 1000+ shots at ≥100 kA
- [FuZE-3 gigapascal pressures press release](https://www.zapenergy.com/news/zap-energy-exceeds-gigapascal-fusion-plasma-pressures-on-new-fusion-device-fuze-3) — 830 MPa electron, 1.6 GPa total
- [Inside a Zap Fusion Core (blog)](https://www.zapenergy.com/blog/inside-zap-fusion-core) — PFN design, current waveforms
- [Zap Energy blog: A Moving Stream](https://www.zapenergy.com/blog/a-moving-stream-zap-energys-novel-approach-to-stabilizing-fusion) — sheared-flow explanation
- [Ben Bridger Engineering blog on Zap Energy](https://benbridgerengineering.com/2023/08/29/zap-energy/) — "LiPb to steam cycle" detail, TBR 1.1
- [FPA 2020 presentation by Brian Nelson](https://firefusionpower.org/FPA20_SFS_Nelson_ZapEnergy.pdf) — image-based PDF, limited extraction

### Secondary sources (context and background)
- [Zap Energy Wikipedia](https://en.wikipedia.org/wiki/Zap_Energy) — founding, funding, device history
- [IEEE Spectrum: Magnetic-Confinement Fusion Without the Magnets](https://spectrum.ieee.org/zap-energy-fusion-reactor) — classification context
- [UW Flow Z-Pinch Lab](https://sites.uw.edu/zpinchlab/) — academic origins
- [UW ECE: ZaP-HD and FuZE](https://www.ece.uw.edu/projects/zap-hd-and-fusion-z-pinch-experiments-fuze/) — lab experiment details
- [ARPA-E: Electrode Technology Development](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/electrode-technology-development-sheared-flow-z-pinch-fusion-reactor) — electrode R&D
- [ARPA-E: SFS Z-Pinch Performance Improvement](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/sheared-flow-stabilized-z-pinch-performance-improvement) — performance program
- [Century paper in Fusion Science and Technology (2025)](https://www.tandfonline.com/doi/full/10.1080/15361055.2025.2532331) — paywalled
- [Electrode durability paper (Physics of Plasmas, 2023)](https://pubs.aip.org/aip/pop/article/30/10/100601/2915124/Electrode-durability-and-sheared-flow-stabilized-Z) — paywalled
- [Fusion Energy News: Simplifying Fusion Energy](https://www.fusion-energy-news.com/zap-energy-shear-flow-stabilized-fusion-simplifying-fusion-energy) — overview
