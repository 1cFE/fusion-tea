Now here is the complete verified dossier with all columns:

---

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Both companies explicitly describe inertial confinement fusion; laser-driven implosion of fuel capsules. Xcimer: https://xcimer.energy/approach/ ; Focused Energy: https://www.focused-energy.co/technology
- **Notes**: Straightforward classification. No change from iter-01.

### Confinement Concept
- **Value**: Laser ICF (direct drive)
- **Confidence**: medium
- **Citation**: Xcimer: https://xcimer.energy/approach/ ("Hybrid Direct Drive"); Focused Energy: https://www.focused-energy.co/technology ("direct-drive, proton fast ignition")
- **Notes**: Classification tension remains. Xcimer uses "Hybrid Direct Drive" (HDD) — two opposed KrF beams at 248 nm, a variant of direct drive that relaxes uniformity requirements. Focused Energy uses direct-drive compression but adds a separate petawatt short-pulse laser for proton fast ignition — this straddles `Laser ICF (direct drive)` and `Laser ICF (fast ignition)`. Focused Energy self-describes as "direct drive" but the physics pathway is fast ignition. Recommend splitting into two rows or reclassifying Focused Energy as `Laser ICF (fast ignition)`.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Xcimer: "DT hydrogen isotope mixture" (science page); Focused Energy: "Deuterium-Tritium fusion fuel" (technology page), Callahan interview: "deuterium-tritium fuel derived from sea water and lithium"
- **Notes**: No ambiguity. Both companies explicitly state deuterium-tritium fuel.

### Primary Heating
- **Value**: Laser (direct drive)
- **Confidence**: high (Xcimer) / medium (Focused Energy)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ; Focused Energy: https://www.focused-energy.co/technology ; Callahan Physics World interview
- **Notes**: Xcimer's HDD is unambiguously direct drive — laser ablates the capsule directly with no hohlraum/X-ray intermediary. Focused Energy combines `Laser (direct drive)` for compression with `Laser (fast ignition)` for ignition. If using a single value, `Laser (fast ignition)` may be more accurate for Focused Energy per the schema definition ("Separate compression and ignition laser pulses"). The proton fast ignition step is a distinct physics mechanism from the compression drive.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: Xcimer Science page: "generate steam, which in turn drives turbines" (https://xcimer.energy/science/); HYLIFE heritage literature: "exchange heat with helium to drive a gas turbine" (~45% efficiency); Focused Energy Callahan interview: "We will use a conventional steam cycle to convert the heat into electricity"
- **Notes**: The two companies likely differ. Focused Energy explicitly confirms `Thermal (steam)`. Xcimer has contradictory signals: their Science page mentions steam turbines, but HYLIFE heritage literature (on which their chamber concept is based) describes a helium Brayton gas turbine cycle at ~45% efficiency. The HYLIFE-III 2024 nuclear analysis paper (Fusion Eng. Des.) doesn't resolve this. Using `Thermal (unspecified)` as the combined value. If rows are split: Focused Energy → `Thermal (steam)`, Xcimer → `Thermal (unspecified)` pending clarification (He Brayton vs steam). Schema may benefit from adding "Thermal (He Brayton)" vocabulary.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Schema definition: "Plasma driven to fusion conditions by implosion (laser, projectile, pulsed power, mechanical). Characteristic of IFE and MIF."
- **Notes**: Both approaches use laser ablation to compress fuel capsules to extreme densities. Standard IFE plasma state. No change.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition: "Inertial confinement — no magnetic confinement of plasma. (Driver subsystem may contain magnets, but these confine the beam, not the plasma.)"
- **Notes**: Neither company uses magnetic confinement of the plasma. Xcimer's electron-beam pumped KrF laser uses pulsed power / electron beams (may involve magnets for electron beam steering) but these are driver subsystem magnets, not plasma confinement.

### Tritium Breeding
- **Value**: FLiBe blanket
- **Confidence**: high (Xcimer) / medium (Focused Energy)
- **Citation**: Xcimer: https://xcimer.energy/approach/ ("flowing liquid lithium salt"); HYLIFE-III 2024 paper (Fusion Eng. Des., S0920379624001868) confirms FLiBe as preferred breeding material with TBR analysis. Focused Energy: Callahan interview confirms "lithium blankets" and collaboration with Savannah River National Lab on tritium extraction, but does NOT specify blanket type.
- **Notes**: Upgraded Focused Energy from `low` to `medium` confidence based on the Callahan interview confirming lithium blanket breeding and SRNL partnership. Specific blanket chemistry (FLiBe vs LiPb vs liquid Li) remains undisclosed for Focused Energy. Value reflects Xcimer's well-documented HYLIFE-III FLiBe approach. If rows split: Xcimer → `FLiBe blanket` (high), Focused Energy → `Li blanket (unspecified)` (medium).

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high (Xcimer) / medium (Focused Energy)
- **Citation**: Xcimer: HYLIFE-III concept — thick flowing FLiBe jets shield first wall, moderate neutron spectrum, breed tritium, and transfer heat. 2024 nuclear analysis paper confirms FLiBe protective wet-wall analyzed at various thicknesses for first wall neutron activation and structural damage. Xcimer claims 30-year facility lifetime without first-wall replacement. Focused Energy: no specific chamber/shielding approach disclosed.
- **Notes**: Xcimer's approach is a textbook case of `Integrated blanket/shield` — the FLiBe simultaneously breeds tritium and provides neutron protection, enabling a lifetime first wall. Focused Energy, as a D-T IFE concept, will require heavy neutron management but hasn't disclosed their approach. The combined value is based on Xcimer's known approach; Focused Energy's would default to `Heavy shielding (14 MeV)` or `Integrated blanket/shield` depending on their eventual chamber design.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Both companies describe discrete laser shots on individual fuel capsules. Xcimer: "every couple seconds" (https://xcimer.energy/science/); Focused Energy: "900,000 shots a day — about 10 per second" (Callahan interview)
- **Notes**: No ambiguity. All laser IFE concepts are pulsed by definition.

### Repetition Rate
- **Value**: Sub-Hz (Xcimer) / ~10 Hz (Focused Energy)
- **Confidence**: high
- **Citation**: Xcimer: https://xcimer.energy/approach/ ("less than 1 Hz"), science page ("every couple seconds"); Focused Energy: Callahan Physics World interview ("about 10 per second")
- **Notes**: Significant differentiator between the two companies. Xcimer's high-energy-per-shot (~10+ MJ laser, much higher fusion yield) allows sub-Hz operation. Focused Energy's lower energy per shot requires ~10 Hz for competitive time-averaged power. This difference strongly reinforces the case for separate rows. HYLIFE-II heritage was 6 Hz (heavy-ion driver, 350 MJ yield); HYLIFE-III reduced to sub-Hz by dramatically increasing yield per shot.

### Driver Technology
- **Value**: Excimer laser (KrF, 248 nm, 10+ MJ) [Xcimer] / Diode-pumped solid-state laser (Nd:glass, 527 nm) + petawatt ignition laser [Focused Energy]
- **Confidence**: high
- **Citation**: Xcimer: https://xcimer.energy/approach/, ASPEN architecture presentation (LLNL IFE Workshop 2022), June 2025 milestone: first private-sector electron-beam excimer laser completed. Focused Energy: https://www.focused-energy.co/technology, $40M Amplitude partnership for DPSSL, T-STAR facility planned for Bay Area with 8 beamlines (4 long-pulse + 4 short-pulse).
- **Notes**: Very different driver technologies. **Xcimer**: KrF excimer gas laser, electron-beam pumped, 248 nm UV, 10+ MJ per pulse, ASPEN architecture with Raman beam combining + stimulated Brillouin scattering pulse compression. Cost target $20-30/J on-target. Record 3-microsecond pulse length achieved (global record for KrF). Phoenix prototype on track for 2026. **Focused Energy**: DPSSL (Nd:glass) frequency-doubled to 527 nm (green), ~10% wall-plug efficiency, partnered with Amplitude. Separate petawatt-class short-pulse laser generates proton beam for fast ignition via cone-in-shell target geometry. T-STAR facility with 8 beamlines planned for science de-risking from 2028.

### Published Machine/Plant?
- **Value**: Pre-conceptual designs exist for both
- **Confidence**: medium
- **Citation**: Xcimer: HYLIFE-III pre-conceptual design under DOE CX-029047 ("IFE Pilot Plant with Low-Cost, High-Energy Excimer Driver and HYLIFE Concept"); 2024 nuclear analysis paper in Fusion Eng. Des. Focused Energy: "LightHouse" concept described on website and in company presentations, but no published technical specifications. J. Fusion Energy 2023 paper describes the approach conceptually.
- **Notes**: Neither has a fully published, detailed plant design with quantitative specifications (MW output, efficiency, etc.). Xcimer has the more mature pre-conceptual design through HYLIFE-III heritage and the 2024 neutronics paper. Focused Energy's LightHouse is described at a marketing level ("gigawatt-scale output") without engineering detail.

### Lab Experiments
- **Value**: OMEGA (LLE Rochester), NIF (LLNL), Naval Research Laboratory (Nike KrF)
- **Confidence**: high
- **Citation**: OMEGA: 28 kJ direct-drive D-T implosion experiments, "spark plug" achievement (Nature Physics 2024); NIF: indirect-drive ignition (Dec 2022), with direct-drive-relevant physics; FLUX broadband laser at LLE (initial experiments April 2025, ramping to >100 J in 2026); Nike KrF laser at NRL (heritage for Xcimer's excimer approach)
- **Notes**: Direct-drive ICF has extensive national lab experimental heritage. Rochester/LLE OMEGA is the primary direct-drive ICF facility (largest academic laser in the US). NIF demonstrated ignition with indirect drive but the physics informs all ICF approaches. Focused Energy's proton fast ignition has been demonstrated at smaller scales (LFEX laser, Osaka; OMEGA EP). Xcimer's KrF excimer heritage traces to SDI-era programs and NRL's Nike laser.

## Remaining Gaps

1. **Confinement Concept (medium confidence)**: The classification tension between Xcimer (genuine direct drive variant) and Focused Energy (fast ignition physics with direct drive compression) remains unresolved. This requires a project-level decision on row splitting. Recommendation: split into two rows — one for Xcimer as `Laser ICF (direct drive)` and one for Focused Energy as `Laser ICF (fast ignition)`.

2. **Energy Capture — Xcimer cycle ambiguity**: Xcimer's Science page says "steam" but HYLIFE heritage literature describes a helium Brayton gas turbine (~45% efficiency). These may reflect: (a) simplified marketing language, (b) a design change from heritage, or (c) a combined cycle. The HYLIFE-III 2024 nuclear analysis paper (behind ScienceDirect paywall) may contain the answer. Resolution: access the full HYLIFE-III paper or contact Xcimer directly.

3. **Tritium Breeding — Focused Energy**: Confirmed lithium blanket breeding with SRNL partnership, but specific blanket chemistry undisclosed. Focused Energy's J. Fusion Energy 2023 paper (behind Springer paywall) may contain chamber/blanket details. Resolution: access the full paper.

4. **Neutron Management — Focused Energy**: No specific approach disclosed. Inferred from D-T IFE requirements. Same paper sources could resolve.

5. **Quantitative Plant Parameters**: Neither company has published electrical output, thermal power, or net efficiency numbers. HYLIFE-II heritage gives 940 MWe at 6 Hz as a reference point, but HYLIFE-III parameters with sub-Hz Xcimer driver differ significantly. Focused Energy targets "gigawatt-scale" without specifics.

## Sources Consulted

### Company Websites
1. [Xcimer Energy — Approach](https://xcimer.energy/approach/) — HDD, KrF excimer, HYLIFE chamber, sub-Hz rep rate
2. [Xcimer Energy — Science](https://xcimer.energy/science/) — gain targets, energy conversion ("steam"), capsule coupling
3. [Focused Energy — Technology](https://www.focused-energy.co/technology) — DPSSL + proton fast ignition
4. [Focused Energy — LightHouse](https://www.focused-energy.co/technology/lighthouse) — marketing-level plant description (no quantitative specs)
5. [Focused Energy — How It Works](https://www.focused-energy.co/how-it-works) — marketing overview (no quantitative specs)
6. [Xcimer Energy — Company](https://xcimer.energy/company/) — founding, investors
7. [Fusion Energy Base — Xcimer](https://www.fusionenergybase.com/organizations/xcimer-energy) — directory listing (minimal detail)

### Technical Papers & Reports
8. [HYLIFE-III Nuclear Analysis (Fusion Eng. Des. 2024)](https://www.sciencedirect.com/science/article/pii/S0920379624001868) — FLiBe TBR analysis, neutron spectra (abstract only; full paper behind paywall)
9. [HYLIFE-II Final Report (Fusion Technology 1994)](https://www.tandfonline.com/doi/abs/10.13182/FST94-A30234) — 940 MWe, 6 Hz, FLiBe, 30-yr lifetime reference design
10. [Hybrid direct drive with two-sided UV laser (Physics of Plasmas 2024)](https://pubs.aip.org/aip/pop/article/31/11/112708/3322685/) — HDD physics paper
11. [Focused Energy, J. Fusion Energy 2023](https://link.springer.com/article/10.1007/s10894-023-00363-x) — concept paper (abstract only)
12. [Mehlhorn 2024 — "From KMS Fusion to HB11 Energy" (Physics of Plasmas)](https://pubs.aip.org/aip/pop/article/31/2/020602/3267722/) — KrF heritage history

### Interviews & News
13. [Physics World — Debbie Callahan interview](https://physicsworld.com/a/focusing-on-fusion-debbie-callahan-talks-commercial-laser-fusion/) — Steam cycle confirmed, 10 Hz, gain >50, SRNL tritium partnership
14. [Physics World — Focused Energy charts course](https://physicsworld.com/a/laser-fusion-focused-energy-charts-a-course-to-commercial-viability/) — podcast announcement (no technical detail)
15. [Xcimer — First private-sector electron-beam excimer laser (June 2025)](https://xcimer.energy/xcimer-energy-completes-first-private-sector-electron-beam-excimer-laser/) — Phoenix prototype milestone
16. [Focused Energy — $40M Amplitude agreement](https://www.focused-energy.co/news-release/focused-energy-and-amplitude-enter-40-million-agreement-to-advance-high-energy-lasers-beyond-the-state-of-the-art-for-inertial-fusion-energy) — DPSSL partnership
17. [Focused Energy completes DOE milestones (World Nuclear News)](https://www.world-nuclear-news.org/articles/focused-energy-completes-first-milestones-on-us-fusion-programme) — high-gain target design report

### DOE & Government
18. [DOE CX-029047: IFE Pilot Plant with HYLIFE Concept](https://www.energy.gov/nepa/articles/cx-029047-ife-pilot-plant-low-cost-high-energy-excimer-driver-and-hylife-concept) — Xcimer DOE program
19. [DOE Fusion Milestone Program selectees](https://www.energy.gov/articles/us-department-energy-announces-selectees-107-million-fusion-innovation-research-engine) — Focused Energy selected

### Lab Experiments
20. [U. Rochester — Direct-drive fusion "spark plug" (2024)](https://www.rochester.edu/newscenter/spark-plug-direct-drive-inertial-confinement-fusion-591822/) — OMEGA direct-drive milestone
21. [LLE Rochester — OMEGA Experiments](https://www.lle.rochester.edu/education/research-areas/omega_experiments/) — direct-drive ICF facility
22. [LLE — FLUX broadband laser](https://www.lle.rochester.edu/publications/flux-a-next-generation-broadband-laser-for-direct-drive-fusion-experiments/) — next-gen broadband laser for direct drive
23. [ASPEN Laser / IFE Workshop 2022 (LLNL)](https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf) — Xcimer presentation (PDF, not extractable via web fetch)

### Other
24. [Optica OPN — Fusion's Direct Drive (June 2023)](https://www.optica-opn.org/home/articles/volume_34/june_2023/features/fusion_s_direct_drive/) — overview of both companies (from iter-01)
25. [SRNL — Fusion Fuel Cycle R&D](https://www.srnl.gov/fact-sheets/fusion-fuel-cycle-research-and-development/) — tritium extraction research (general, not Focused Energy-specific)
26. [Focused Energy roadmap (ALP conference PDF)](https://www.asso-alp.fr/wp-content/uploads/2023/07/2.7-Roadmap-of-Focused-Energy-Vaisseau.pdf) — not extractable via web fetch
27. [Science.org — Direct approach to laser-powered fusion](https://www.science.org/content/article/direct-approach-laser-powered-fusion-promises-simpler-power-production) — overview article
