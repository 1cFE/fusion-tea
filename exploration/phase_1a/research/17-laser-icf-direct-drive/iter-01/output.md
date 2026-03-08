Now I have enough information to provide the complete dossier. One important note: this concept entry says "Laser ICF - Direct Drive" but the two companies use quite different approaches — Xcimer uses **hybrid direct drive** (2 opposed beams, KrF excimer) while Focused Energy uses **direct-drive proton fast ignition** (DPSSL + petawatt ignition laser). These are arguably two different confinement concepts in the schema. Let me note this clearly.

---

## Research Findings: Laser ICF - Direct Drive (D-T)

**Important Note**: Xcimer Energy and Focused Energy, while both "direct drive" IFE companies, use substantially different approaches:
- **Xcimer**: Hybrid Direct Drive (HDD) with KrF excimer laser, two opposed beams, sub-Hz rep rate, HYLIFE III FLiBe chamber
- **Focused Energy**: Direct-Drive Proton Fast Ignition with DPSSL compression + short-pulse ignition laser, ~10 Hz rep rate, conventional steam cycle

The schema's `Laser ICF (direct drive)` confinement concept covers both, but `Laser ICF (fast ignition)` may be more appropriate for Focused Energy specifically. I'll note this tension below.

---

### Confinement Family
- **Value**: `IFE`
- **Confidence**: high
- **Citation**: Both companies explicitly describe inertial confinement fusion; laser-driven implosion of fuel capsules
- **Notes**: Straightforward classification.

### Confinement Concept
- **Value**: `Laser ICF (direct drive)`
- **Confidence**: medium
- **Citation**: Xcimer: https://xcimer.energy/approach/ ; Focused Energy: https://www.focused-energy.co/technology
- **Notes**: This is a combined entry, but the two companies have meaningfully different physics:
  - **Xcimer** uses "Hybrid Direct Drive" (HDD) — two opposed KrF beams at 248 nm, a variant of direct drive that relaxes uniformity requirements. Still classified as direct drive.
  - **Focused Energy** uses "Direct-Drive Proton Fast Ignition" — DPSSL compression beams + a separate short-pulse laser that accelerates protons to ignite compressed fuel. This could equally be classified as `Laser ICF (fast ignition)` in the schema, since it explicitly separates compression and ignition. The company self-describes as "direct drive" but the physics is fast ignition.
  - **Recommendation**: Consider splitting into two rows, or at minimum note that Focused Energy's approach maps to `Laser ICF (fast ignition)` per the schema vocabulary.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Both companies explicitly state deuterium-tritium fuel. Xcimer: "DT hydrogen isotope mixture"; Focused Energy: "Deuterium-Tritium fusion fuel"
- **Notes**: No ambiguity.

### Primary Heating
- **Value**: `Laser (direct drive)`
- **Confidence**: high (Xcimer) / medium (Focused Energy)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ; Focused Energy: https://www.focused-energy.co/technology
- **Notes**: 
  - Xcimer's hybrid direct drive is a variant of direct drive — laser ablates the capsule directly (no hohlraum/X-ray intermediary).
  - Focused Energy's approach technically combines `Laser (direct drive)` for compression with `Laser (fast ignition)` for ignition — the proton fast ignition step is a separate physics mechanism. If using a single value, `Laser (fast ignition)` may be more accurate for Focused Energy per the schema definition ("Separate compression and ignition laser pulses").

### Energy Capture
- **Value**: `Thermal (unspecified)` — but can be refined:
  - **Xcimer**: Helium gas turbine (Brayton cycle), ~45% efficiency. Could be recorded as `Thermal (sCO2)` equivalent but it's actually helium Brayton, which isn't in the controlled vocabulary. Closest: `Thermal (unspecified)` with note.
  - **Focused Energy**: "Conventional steam cycle" per Physics World interview → `Thermal (steam)`
- **Confidence**: medium (Xcimer), high (Focused Energy)
- **Citation**: Xcimer: HYLIFE III concept from LLNL heritage, confirmed on approach page ("heat exchanged with helium to drive a gas turbine"); Focused Energy: Physics World interview with Debbie Callahan
- **Notes**: Xcimer's helium Brayton cycle is not `Thermal (steam)` or `Thermal (sCO2)` — it's a helium gas turbine. The schema doesn't have this as a specific option. Recommend `Thermal (unspecified)` with a note: "Helium Brayton cycle, ~45% efficiency, per HYLIFE III concept." For Focused Energy, `Thermal (steam)` is directly stated. If this is a combined row, use `Thermal (unspecified)` to cover both.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: Schema definition: "Plasma driven to fusion conditions by implosion (laser, projectile, pulsed power, mechanical). Characteristic of IFE and MIF."
- **Notes**: Both approaches use laser ablation to compress and (directly or via fast ignition) ignite fuel capsules. `Compressed` is the correct IFE plasma state.

### Magnet Type
- **Value**: `None (IFE)`
- **Confidence**: high
- **Citation**: Schema definition: "Inertial confinement — no magnetic confinement of plasma."
- **Notes**: Neither company uses magnetic confinement of the plasma. Xcimer's laser uses electron beams (which may have magnets) but those confine the electron beam, not the plasma.

### Tritium Breeding
- **Value**: 
  - **Xcimer**: `FLiBe blanket` — directly stated as HYLIFE III with flowing FLiBe/FLiNaBe, TBR ~1.17
  - **Focused Energy**: `TBD` — no blanket type disclosed publicly. They mention fuel "from seawater and lithium" implying lithium breeding, but no specific blanket architecture.
  - Combined row: `FLiBe blanket` (Xcimer) / `TBD` (Focused Energy)
- **Confidence**: high (Xcimer), low (Focused Energy)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ("flowing liquid lithium salt"); HYLIFE III heritage from LLNL. Focused Energy: no public disclosure found.
- **Notes**: Xcimer's HYLIFE III is one of the most well-developed IFE chamber concepts, with decades of LLNL research behind it. The FLiBe serves triple duty: neutron shielding, tritium breeding, and heat transfer medium.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high (Xcimer), medium (Focused Energy)
- **Citation**: Xcimer: HYLIFE III concept — thick flowing FLiBe jets shield first wall, moderate neutron spectrum to fission-like levels, breed tritium. First solid wall designed as lifetime component.
- **Notes**: Xcimer's approach is a textbook case of `Integrated blanket/shield` — the FLiBe simultaneously breeds tritium and provides neutron protection. Focused Energy hasn't disclosed their neutron management approach but as a D-T IFE concept they will need heavy neutron management. For a combined row, `Integrated blanket/shield` captures Xcimer's known approach; Focused Energy's is TBD but will likely be similar.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: Both companies describe discrete laser shots on individual fuel capsules — characteristic IFE pulsed operation.
- **Notes**: No ambiguity. All laser IFE concepts are pulsed.

### Repetition Rate
- **Value**: 
  - **Xcimer**: `Sub-Hz` — "less than 1 Hz" per their approach page
  - **Focused Energy**: `~10 Hz` — target ~10 shots/second for power plant
  - Combined: range from `Sub-Hz` to `~10 Hz`
- **Confidence**: high (both)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ("less than 1 Hz"); Focused Energy: Physics World interview, journal paper references ("10 Hz")
- **Notes**: This is a significant differentiator between the two companies. Xcimer's high-energy-per-shot (~10 MJ laser) approach allows sub-Hz operation. Focused Energy's lower energy per shot requires higher rep rate. This difference reinforces the case for separate rows.

### Driver Technology
- **Value**: 
  - **Xcimer**: `Excimer laser (KrF, 248 nm, 10+ MJ)`
  - **Focused Energy**: `Diode-pumped solid-state laser (Nd:glass, 527 nm) + petawatt ignition laser`
- **Confidence**: high (both)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ; Focused Energy: https://www.focused-energy.co/technology, Optica OPN article
- **Notes**: Very different driver technologies:
  - Xcimer: Gas laser (KrF excimer), electron-beam pumped, 248 nm UV, ~10+ MJ per pulse. Heritage from SDI program. ASPEN architecture with spatial/temporal pulse compression. Low cost per joule.
  - Focused Energy: Solid-state laser (DPSSL), Nd:glass frequency-doubled to 527 nm (green), ~10% wall-plug efficiency. Partnered with Amplitude. Plus a separate petawatt-class short-pulse laser for proton fast ignition.

### Published Machine/Plant?
- **Value**: No (neither company has a published full plant design)
- **Confidence**: medium
- **Citation**: Xcimer has a pre-conceptual design under DOE program (CX-029047) but not a published plant design document. Focused Energy has the "LightHouse" concept but no published specifications.
- **Notes**: Xcimer's HYLIFE III chamber concept has extensive LLNL heritage (HYLIFE-II report is published), but Xcimer's specific integrated plant design is not yet published. Focused Energy's LightHouse™ is named but not described in technical detail publicly.

### Lab Experiments
- **Value**: NIF (LLNL, indirect drive achieved ignition Q>1), OMEGA (U. Rochester, direct drive ICF), LMJ (France), SG-III (China), Colorado State University (proton fast ignition for Focused Energy)
- **Confidence**: high
- **Citation**: OMEGA: https://www.lle.rochester.edu/education/research-areas/omega_experiments/ ; Colorado State: Focused Energy DOE milestone completion announcement
- **Notes**: NIF demonstrated ignition with indirect drive (not direct drive), but the underlying physics of D-T capsule implosion is relevant. OMEGA is the primary direct-drive ICF facility. Colorado State experiments specifically demonstrated Focused Energy's proton fast ignition approach.

---

## Remaining Gaps

1. **Energy Capture (Focused Energy)**: Confirmed as `Thermal (steam)` from Physics World interview. However, Xcimer's helium Brayton cycle doesn't fit the schema's controlled vocabulary perfectly — neither `Thermal (steam)` nor `Thermal (sCO2)`. Recommend adding "Thermal (He Brayton)" or using `Thermal (unspecified)` with a note. **What would help**: Xcimer's ASPEN/HYLIFE III technical report.

2. **Tritium Breeding (Focused Energy)**: `TBD` — no public disclosure. **What would help**: Focused Energy journal paper (behind paywall) or investor presentation may have chamber/blanket details.

3. **Neutron Management (Focused Energy)**: Inferred as needing heavy shielding (D-T) but no specific approach disclosed. Likely similar to other IFE concepts. **What would help**: Same as above.

4. **Concept Classification Tension**: Focused Energy's approach is technically "fast ignition" (separate compression and ignition pulses) but they self-describe as "direct drive." The schema has both `Laser ICF (direct drive)` and `Laser ICF (fast ignition)` — Focused Energy straddles both. **Recommendation**: Either split into two rows or classify Focused Energy as `Laser ICF (fast ignition)` with a note.

5. **Quantitative Plant Parameters**: Neither company has published detailed plant electrical output, thermal power, or net efficiency numbers. Xcimer's ASPEN workshop presentation (PDF at LLNL, couldn't extract) likely contains more quantitative details.

---

## Sources Consulted

- [Xcimer Energy — Approach](https://xcimer.energy/approach/)
- [Xcimer Energy — Hybrid Direct Drive blog post](https://xcimer.energy/advancing-fusion-target-design-with-hybrid-direct-drive/)
- [Xcimer Energy — DOE $9M Award announcement](https://xcimer.energy/xcimer-energy-announces-9-million-us-department-of-energy-award-to-develop-laser-driven-inertial-fusion-energy/)
- [Xcimer Energy — First private-sector electron-beam excimer laser](https://xcimer.energy/xcimer-energy-completes-first-private-sector-electron-beam-excimer-laser/)
- [Xcimer Energy — Fusion Energy Base profile](https://www.fusionenergybase.com/organizations/xcimer-energy)
- [Xcimer $100M funding — Optics.org](https://optics.org/news/15/6/6)
- [DOE CX-029047: IFE Pilot Plant with HYLIFE Concept](https://www.energy.gov/nepa/articles/cx-029047-ife-pilot-plant-low-cost-high-energy-excimer-driver-and-hylife-concept)
- [ASPEN Laser IFE Workshop 2022 presentation (PDF, not extractable)](https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf)
- [Mehlhorn 2024 — "From KMS Fusion to HB11 Energy and Xcimer Energy" (Physics of Plasmas)](https://pubs.aip.org/aip/pop/article/31/2/020602/3267722/)
- [Hybrid direct drive with two-sided UV laser (Physics of Plasmas 2024)](https://pubs.aip.org/aip/pop/article/31/11/112708/3322685/)
- [Focused Energy — Technology page](https://www.focused-energy.co/technology)
- [Focused Energy — LightHouse page](https://www.focused-energy.co/technology/lighthouse)
- [Focused Energy — Amplitude $40M agreement](https://www.focused-energy.co/news-release/focused-energy-and-amplitude-enter-40-million-agreement-to-advance-high-energy-lasers-beyond-the-state-of-the-art-for-inertial-fusion-energy)
- [Focused Energy — DOE Milestone completion](https://www.focused-energy.co/news-release/focused-energy-completes-its-first-milestones-through-does-milestone-based-fusion-development-program)
- [Focused Energy J. Fusion Energy 2023 paper (abstract only)](https://link.springer.com/article/10.1007/s10894-023-00363-x)
- [Direct Drive Laser Fusion Facility and Pilot Plant — J. Fusion Energy 2024 (abstract only)](https://link.springer.com/article/10.1007/s10894-024-00416-9)
- [Physics World — Debbie Callahan interview](https://physicsworld.com/a/focusing-on-fusion-debbie-callahan-talks-commercial-laser-fusion/)
- [Optica OPN — Fusion's Direct Drive (June 2023)](https://www.optica-opn.org/home/articles/volume_34/june_2023/features/fusion_s_direct_drive/)
- [Science/AAAS — Direct approach to laser-powered fusion](https://www.science.org/content/article/direct-approach-laser-powered-fusion-promises-simpler-power-production)
- [OMEGA Experiments — LLE Rochester](https://www.lle.rochester.edu/education/research-areas/omega_experiments/)
- [U. Rochester — Direct-drive fusion "spark plug" achievement](https://www.rochester.edu/newscenter/spark-plug-direct-drive-inertial-confinement-fusion-591822/)
- [INFUSE award — Simulation of DDH two opposed beams](https://infuse.ornl.gov/awards/simulation-of-direct-drive-hybrid-using-two-opposed-beams-for-inertial-fusion-energy/)
- [Gigascale — Xcimer profile](https://gigascale.com/profiles/xcimer-commercializing-fusion-energy/)
- [Focused Energy roadmap presentation (ALP conference)](https://www.asso-alp.fr/wp-content/uploads/2023/07/2.7-Roadmap-of-Focused-Energy-Vaisseau.pdf)
- [Laserlab-Europe IFE strategic direction 2025](https://laserlab-europe.eu/wp-content/uploads/lle-aisbl_icf-ife_europes-strategic-direction_2025.pdf)
