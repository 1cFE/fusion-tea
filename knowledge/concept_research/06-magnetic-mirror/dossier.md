# Magnetic Mirror (p-B11)

**Company**: Pale Blue Fusion (pre-incorporation Princeton University spinoff)
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: medium

## Summary

Multi-chamber centrifugal magnetic mirror (CHARM — CHambered Aneutronic Rotating Mirror) using E×B plasma rotation to centrifugally separate lighter protons from heavier boron-11 ions, enabling a nonthermal p-B11 fusion approach. Alpha channeling extracts helium ash energy via RF waves and recycles it into fuel protons, addressing the critical bremsstrahlung and helium poisoning challenges of p-B11 fusion. The concept is led by Nat Fisch, Ian Ochs, and Elijah Kolmes at Princeton, with related centrifugal mirror physics validated on the CMFX experiment at the University of Maryland. As of July 2025, the group has 29 peer-reviewed publications, 4 patent applications, and is pivoting from academic research to incorporation as Pale Blue Fusion with Princeton University support. No dedicated experimental hardware built yet.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: ARPA-E presentation (Day2_08_Fisch.pdf, July 2025) — centrifugal magnetic mirror confinement
- **Notes**: Plasma is confined by external magnetic fields in a mirror geometry, with E×B rotation providing additional centrifugal stabilization and differential species confinement.

### Confinement Concept
- **Value**: Magnetic mirror
- **Confidence**: high
- **Citation**: ARPA-E presentation — "CHARM: CHambered Aneutronic Rotating Mirror"
- **Notes**: Specifically a centrifugal magnetic mirror — a rotating mirror where E×B rotation provides centrifugal enhancement of confinement. The multi-chamber architecture (fusion chamber + heat exchange chamber + plug) is a key distinguishing feature. Proprietary name: CHARM. Related physics validated on CMFX at University of Maryland (separate group, using LTS magnets).

### Fuel
- **Value**: p-B11
- **Confidence**: high
- **Citation**: ARPA-E project title "Economical Proton-Boron11 Fusion"; all publications
- **Notes**: The entire concept is designed around p-B11's mass disparity — protons (1 amu) vs boron-11 (11 amu) enables centrifugal species separation. Fisch describes p-B11 as "the holy grail of really clean, really abundant fusion energy."

### Primary Heating
- **Value**: RF (ICRH)
- **Confidence**: medium
- **Citation**: ARPA-E presentation slides 6, 15; Fisch group publications on alpha channeling (Zhmoginov & Fisch 2009, Fetterman & Fisch 2010); S5 PIC code XB mode conversion simulation
- **Notes**: The primary energy recycling mechanism is alpha channeling — RF waves in the ion cyclotron frequency range extract energy from fusion-born alpha particles and redirect it into fuel protons, maintaining a nonthermal proton distribution. The S5 PIC code simulation shows "XB Mode Conversion in Supersonic Flow" at the upper hybrid resonance, indicating X-mode to Bernstein wave mode conversion in the rotating plasma. In rotating mirrors specifically (Fetterman & Fisch 2010), alpha particle energy can transfer to the radial electric field (plasma rotation energy) via stationary magnetic field perturbations with high azimuthal mode numbers. Initial plasma rotation is established by a biased central electrode, not by RF heating. Schema note: `RF (ICRH)` is the closest standard vocabulary value since the waves operate in the ion cyclotron frequency range, but the mechanism is fundamentally different from conventional ICRH — it is wave-mediated energy recycling from fusion products, not external power injection.

### Energy Capture
- **Value**: Direct (charged particle)
- **Confidence**: medium
- **Citation**: ARPA-E presentation (slide 5: "Can rotation energy be recovered efficiently?", slide 19: "Centrifugal drift energy is recoverable"); Rax, Kolmes & Fisch, "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields", PRX Energy 4, 013007 (2025); Patent US20230298771 (SWDEC, 2023)
- **Notes**: p-B11 fusion produces only charged particles (3 alpha particles per reaction, no neutrons). The CHARM concept captures alpha particle energy via the radial electric field (rotation energy), then recovers that rotation energy via direct energy conversion. The PRX Energy 2025 paper from the core team specifically addresses adiabatic DEC in axisymmetric (mirror) fields, suggesting this is their preferred approach. The earlier SWDEC patent (US20230298771) describes an alternative RF-based Standing Wave DEC from a potentially different inventor group. Whether Pale Blue adopts SWDEC or their own adiabatic DEC is not confirmed, but the core team's publication record points toward the adiabatic approach.

### Plasma State
- **Value**: Sustained
- **Confidence**: medium
- **Citation**: ARPA-E presentation — continuous operation with active RF wave maintenance; power balance (slide 14) showing external heating P_H and alpha channeling efficiency eta_alpha
- **Notes**: The CHARM concept targets a steady-state, actively maintained nonthermal plasma — energetic protons sustained by alpha channeling RF waves while electrons and boron are kept cooler to minimize bremsstrahlung. The power balance diagram shows continuous external heating power P_H with alpha channeling recycling a fraction of fusion power back to protons. This is externally maintained quasi-steady-state operation, fitting `Sustained` better than `Confined` (which implies passive confinement without active energy cycling). The concept is not targeting ignition — it relies on continuous wave-mediated energy recycling, so `Burning` does not apply.

### Magnet Type
- **Value**: TBD
- **Confidence**: low
- **Citation**: ARPA-E presentation shows "Outer mirror coils" and "Inner mirror coils" but no conductor technology specification; no public disclosure from Pale Blue/Fisch group
- **Notes**: The ARPA-E presentation (slides 6, 11) clearly shows solenoidal mirror coils (simple axisymmetric wound geometry) but does not specify the conductor technology. The related CMFX experiment at UMD uses repurposed MRI LTS superconducting magnets (3 T throat, 0.3 T midplane). The WHAM experiment at Wisconsin uses CFS-supplied HTS (REBCO) magnets at 17 T for their mirror. For a reactor-scale CHARM device, HTS wound coils would be the likely choice given the simple solenoidal geometry, benefit from high mirror ratios, and industry trends — but the Pale Blue group's 29 publications and 4 patents focus entirely on plasma physics with no engineering subsystem specifications disclosed.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: ARPA-E presentation slide 1: "No tritium breeding and containment" listed as key p-B11 advantage
- **Notes**: p-B11 fuel cycle produces no tritium. No breeding blanket needed.

### Neutron Management
- **Value**: Minimal (aneutronic)
- **Confidence**: high
- **Citation**: ARPA-E presentation slide 1: "No neutron damage and induced radioactivity"; p-B11 reaction physics
- **Notes**: p-B11 is truly aneutronic (<1% neutron energy from side reactions). The presentation explicitly lists "no neutron damage and induced radioactivity," "no waste storage issues," and "easier regulatory environment" as advantages. Minimal shielding required.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: ARPA-E presentation — continuous plasma flow between chambers; centrifugal mirror physics is inherently steady-state
- **Notes**: CHARM is a steady-state device — plasma continuously rotates in the mirror, boron is centrifugally trapped, and helium ash is continuously extracted via alpha channeling. No pulsed compression or discrete burn events.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state concept — continuous operation
- **Notes**: N/A — continuous operation, no repetition rate applicable.

### Driver Technology
- **Value**: Centrifugal mirror with alpha channeling (RF waves, E×B rotation, ponderomotive barriers)
- **Confidence**: high
- **Citation**: ARPA-E presentation (CHARM concept); 29 published papers; 4 patent applications (March-April 2025)
- **Notes**: The distinguishing technology bet combines: (1) centrifugal confinement via E×B plasma rotation providing species-selective confinement exploiting mass disparity, (2) alpha channeling using RF waves (ion cyclotron range, XB mode conversion) to extract energy from fusion-born helium and channel it into fuel protons, (3) ponderomotive barriers using static magnetic field perturbations for species-selective ion traffic control between chambers ("one-way RF walls"), (4) multi-chamber architecture (fusion + heat exchange + plug) enabling spatial separation of reactants and products, and (5) biased central electrode for establishing plasma rotation with minimal dissipation. 4 US patent applications filed March-April 2025.

## Remaining Gaps

### Magnet Type (TBD, low confidence)
- **Searched**: ARPA-E presentation (all 20 slides), 29 publication titles, 4 patent application titles, CMFX documentation, WHAM project for mirror magnet context, general web searches
- **What would resolve it**: Company disclosure of reactor engineering design, or a published reactor concept study with magnet specifications
- **Another iteration likely to help?**: No — the group's entire body of work focuses on plasma physics, not engineering subsystems. Magnet technology choice will come when the company matures from theoretical physics to device design. The simple solenoidal mirror geometry means any conductor technology could work.

### Primary Heating (medium confidence)
- **Status**: Significantly improved from iter-01 (was low confidence). Now confirmed as RF waves in the ion cyclotron frequency range, with XB mode conversion as the coupling mechanism, used for alpha channeling.
- **Remaining uncertainty**: The exact antenna/launching scheme and operating frequency are not specified. `RF (ICRH)` is the best schema fit but doesn't fully capture the unique alpha channeling mechanism.
- **Another iteration likely to help?**: Unlikely — the ARPA-E presentation is the most detailed public source.

### Energy Capture (medium confidence)
- **Status**: Improved from iter-01. The PRX Energy 2025 paper on adiabatic DEC from the core team strongly suggests this is their preferred approach. Combined with the presentation's emphasis on rotation energy recovery, the picture is clearer.
- **Remaining uncertainty**: Whether the specific DEC technology is the SWDEC (2023 patent) or the adiabatic approach (2025 PRX Energy paper).
- **Another iteration likely to help?**: Unlikely — this is a company disclosure issue.

### Company Status
- **Status**: Pivoting to incorporation as Pale Blue Fusion (July 2025). Princeton University support confirmed. Website mockup shown (palebluefusion.com, "coming soon"). No website, FIA listing, or funding announcements found beyond ARPA-E grant.
- **Another iteration likely to help?**: Possibly — a targeted search for late 2025/early 2026 news might find incorporation or funding announcements.

## Key Sources

1. **ARPA-E presentation** (July 9, 2025): https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf — 20-slide presentation covering CHARM architecture, derisked physics, computational tools, patent portfolio, company pivot. Primary source for both iterations.
2. **ARPA-E project page**: https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/economical-proton-boron11-fusion
3. **Princeton press release** (2022): https://www.princeton.edu/news/2022/03/10/fisch-receives-funding-unlikely-fantastic-clean-energy-technology
4. **Rax, Kolmes & Fisch**, "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields", PRX Energy 4, 013007 (2025)
5. **Ochs, Kolmes & Fisch**, "Preventing ash from poisoning proton-boron 11 fusion plasmas", Phys. Plasmas 32, 052506 (2025) — arXiv:2502.13300
6. **Rubin & Fisch**, "Ponderomotive barriers in rotating mirror devices using static fields", Phys. Plasmas 32, 062104 (2025) — arXiv:2502.02008
7. **Ochs et al.**, "Improving the Feasibility of Economical Proton-Boron 11 Fusion via Alpha Channeling with a Hybrid Fast + Thermal Proton Scheme", Phys. Rev. E 106, 055215 (2022) — arXiv:2210.08076
8. **Kolmes, Ochs & Fisch**, "Wave-Supported Hybrid Beam-Thermal pB11 Fusion", Phys. Plasmas 29, 110701 (2022) — arXiv:2211.17143
9. **Zhmoginov & Fisch**, "Waves for alpha channeling in mirror machines", Phys. Plasmas 16, 112511 (2009)
10. **Fetterman & Fisch**, "Alpha channeling in rotating plasma with stationary waves", Phys. Plasmas 17, 042112 (2010)
11. **Fisch**, "Alpha channeling in mirror machines", Phys. Rev. Lett. 97, 225001 (2006)
12. **Patent US20230298771**: "Direct Energy Converter for Axisymmetric Mirror Fusion Reactor" (SWDEC concept, 2023)
13. **Patent applications** (Fisch group, 2025): US 19/083,790; US 19/084,168; US 19/175,473; US Provisional 63/794,470
14. **CMFX at UMD**: https://ireap.umd.edu/research/centrifugal-mirror-fusion-experiment — LTS magnets (repurposed MRI), 3T throat, 0.3T midplane
15. **arXiv:2505.23047**: CMFX fusion yield measurements (2025)
16. **Princeton breakthrough article** (2025): https://www.princeton.edu/news/2025/12/17/search-next-big-breakthrough-princeton
