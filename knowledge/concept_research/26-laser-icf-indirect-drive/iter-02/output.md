Now here is the complete verified dossier:

---

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Schema definition; both companies describe inertial confinement fusion
- **Notes**: Laser-driven inertial confinement. Plasma confined by its own inertia during brief implosion. No change from iter-01.

### Confinement Concept
- **Value**: Laser ICF (indirect drive)
- **Confidence**: high
- **Citation**: https://inertia.com/faq/why-indirect-drive/ ; https://xcimer.energy/approach/ ; Physics of Plasmas 31(11), 112708 (2024)
- **Notes**: Inertia explicitly confirms indirect drive with hohlraum targets based on NIF Hybrid-E design. Xcimer has evolved toward Hybrid Direct Drive (HDD) per their Physics of Plasmas publication — the first laser pulse heats a hohlraum to generate x-rays that ablate the capsule and form a thick plasma atmosphere, then subsequent pulses drive the capsule directly through this atmosphere. HDD still uses a hohlraum but in a fundamentally different way than NIF indirect drive. For schema purposes, classified under "Laser ICF (indirect drive)" due to NIF heritage and hohlraum presence. If a "Laser ICF (hybrid drive)" row is added, Xcimer should be moved there. The APS-DPP 2025 meeting included a Xcimer talk on "Hybrid target design for IFE."

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: https://xcimer.energy/science/ ("DT fuel"); https://inertia.com/ (confirmed in technical context); all NIF ignition experiments used D-T
- **Notes**: Standard ICF fuel. NIF ignition (10 successful experiments through Oct 2025) all used D-T. No change.

### Primary Heating
- **Value**: Laser (indirect drive)
- **Confidence**: high
- **Citation**: https://inertia.com/faq/why-indirect-drive/ ; https://xcimer.energy/science/ ; Xcimer HDD paper
- **Notes**: Laser energy → hohlraum → X-rays → capsule ablation → implosion compression. Inertia: DPSSL (Thunderwall, 10 kJ × 1000-4000 beamlines, 10 Hz, 3ω UV). Xcimer: KrF excimer (ASPEN, 2 amplifiers, 12 MJ, <1 Hz, 248 nm UV). Xcimer's HDD has a more nuanced energy coupling path (first pulse indirect, subsequent pulses direct), but the hohlraum is still present. Schema value "Laser (indirect drive)" remains the best fit.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: medium
- **Citation**: https://xcimer.energy/science/ ("steam, which in turn drives turbines to produce electricity"); Inertia ENR interview ("turning heat into steam, which then drives a turbine"); ASPEN IFE Workshop 2022 presentation (mentions "helium to drive a gas turbine" for HYLIFE-III)
- **Notes**: Both companies reference steam turbines in public-facing materials. However, the 2022 ASPEN/IFE Workshop presentation (LLNL) describes the HYLIFE-III chamber using "helium to drive a gas turbine that extracts 45% of the fusion energy as electricity" — a helium Brayton cycle, not steam Rankine. This discrepancy likely reflects simplification on websites vs. the more detailed engineering design in the HYLIFE-III study. The HYLIFE-II original design used steam Rankine; HYLIFE-III may have updated to helium Brayton. For the table, "Thermal (steam)" is used based on both companies' explicit public statements, but a correction to "Thermal (unspecified)" may be warranted given the helium Brayton reference. Inertia has not specified their cycle beyond "steam."

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Schema definition for IFE; NIF ignition physics
- **Notes**: Plasma driven to fusion conditions by laser-driven implosion. Fuel capsule compressed to ~300 g/cm³ and ~100 million K in nanoseconds. No change.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition; neither company describes magnetic confinement of plasma
- **Notes**: No magnetic confinement of fusion plasma. Xcimer's excimer laser uses electron beams (and now microwave hybrid pumping per HYPER-LASER DOE award) for lasing medium excitation — these are beam-generation magnets, not plasma confinement. No change.

### Tritium Breeding
- **Value**: FLiBe blanket / Liquid Li blanket
- **Confidence**: high
- **Citation**: https://xcimer.energy/approach/ ("flowing liquid lithium salt" / FLiBe); https://inertia.com/faq/where-will-you-get-tritium/ ("pipes full of liquid lithium"); ScienceDirect HYLIFE-III paper (FLiBe, TBR > 1.2)
- **Notes**: Two different blanket materials. **Xcimer**: FLiBe (Li₂BeF₄) molten salt per HYLIFE-III design; TBR > 1.2 per published nuclear analysis. **Inertia**: Liquid lithium pipes lining the chamber; tritium extraction "still an area of active development"; lithium quantity ~equivalent to 15 EVs; on-site tritium inventory ~few hundred grams; startup tritium from U.S. government stockpiles. For a single table value, suggest dual notation: "FLiBe blanket (Xcimer) / Liquid Li blanket (Inertia)" or "Li blanket (unspecified)" as compromise.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: https://xcimer.energy/approach/ ("flowing liquid lithium salt to protect the chamber's structural walls"); https://inertia.com/faq/where-will-you-get-tritium/ (liquid lithium lining); HYLIFE-III paper
- **Notes**: Both designs use flowing liquid (FLiBe or liquid Li) as an integrated blanket that simultaneously breeds tritium, absorbs 14 MeV neutrons, shields structural walls, and carries away heat. Xcimer explicitly notes the liquid wall "directly protect[s] the first structural wall" and extends plant lifetime by minimizing activation — this is the classic HYLIFE "waterfall" concept. Xcimer claims this approach enables use of "readily available commercial materials" and compliance with "waste and safety goals." No change from iter-01.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: https://xcimer.energy/science/ ("every few seconds"); https://inertia.com/ ("10 times per second")
- **Notes**: ICF is inherently pulsed — discrete implosion events. Each shot is a self-contained fusion event lasting nanoseconds. No change.

### Repetition Rate
- **Value**: Sub-Hz / ~10 Hz
- **Confidence**: high
- **Citation**: https://xcimer.energy/approach/ ("less than 1 Hz"); ASPEN presentation (0.25 Hz baseline, 0.5-1 Hz range); https://inertia.com/ ("10 times per second")
- **Notes**: Significant divergence between companies. **Xcimer**: Sub-Hz (<1 Hz), baseline 0.25-0.5 Hz, enabled by higher gain per shot (larger capsules, more energy per pulse). Lower rep rate simplifies chamber clearing and target injection. **Inertia**: ~10 Hz, Thunderwall fires at 10 Hz, higher rep rate compensates for lower energy per beamline. For a single table value, the range "Sub-Hz to ~10 Hz" captures both, or dual notation is needed.

### Driver Technology
- **Value**: Excimer laser (KrF) / Diode-pumped solid-state laser (DPSSL)
- **Confidence**: high
- **Citation**: https://xcimer.energy/ (KrF excimer, Phoenix platform, HYPER-LASER hybrid pumping); https://inertia.com/ (Thunderwall DPSSL, 10 kJ × 10 Hz × 10% efficiency)
- **Notes**: Two fundamentally different laser technologies. **Xcimer**: KrF excimer laser, electron-beam pumped (with hybrid microwave pumping under DOE-funded HYPER-LASER development), 248 nm UV, 2 large amplifiers → 12 MJ on target, gas amplifying medium, pulse compression via stimulated Brillouin scattering. Phoenix (prototype) completed Jun 2025 — first private-sector e-beam excimer laser in 20+ years, record 3 μs pulse length. Vulcan (next-gen, 12 MJ) by 2030. **Inertia**: DPSSL, semiconductor diode pumped, 3ω (frequency-tripled UV), 1000-4000 beamlines at 10 kJ each → 10 MJ total, 10% wallplug efficiency, modular architecture. Thunderwall prototype in development.

## Additional Metadata

### Published Machine/Plant?
- **Inertia**: No published plant design document. General architecture described (Thunderwall laser + target factory + liquid Li chamber) but no HYLIFE-equivalent study.
- **Xcimer**: Yes — ASPEN laser architecture and HYLIFE-III chamber concept published. ASPEN presented at 2022 IFE Workshop at LLNL. HYLIFE-III nuclear analysis published in Fusion Engineering and Design (2024). HDD target physics published in Physics of Plasmas (2024).
- NIF/LLNL heritage: The LIFE (Laser Inertial Fusion Energy) power plant concept was published by LLNL but canceled in 2013 before ignition was achieved. LIFE used NIF-like indirect drive.

### Lab Experiments
- **NIF (LLNL)**: 10 successful ignition experiments (Dec 2022 – Oct 2025). Peak yield 8.6 MJ from 2.08 MJ input (gain ~4.1, Apr 2025). All used indirect drive with hohlraum targets. Enhanced Yield Capability (EYC) project would boost laser to 2.6 MJ → yields >30 MJ possible.
- **Omega (LLE Rochester)**: Direct drive experiments relevant to ICF physics.
- **Xcimer Phoenix**: First private-sector e-beam excimer laser completed Jun 2025. Record 3 μs pulse length achieved May 2025. Laser hardware only — no fusion experiments yet.
- **Inertia**: No laser hardware demonstrated yet (as of Mar 2026). Thunderwall prototype in development.

## Remaining Gaps

1. **Energy Capture — thermal cycle specificity**: Xcimer's website says "steam" but the ASPEN/IFE Workshop 2022 presentation describes HYLIFE-III with "helium to drive a gas turbine at 45% efficiency." This discrepancy is unresolved. The actual HYLIFE-III engineering design may use helium Brayton, while "steam" is simplified for public communications. A direct question to Xcimer or reading the full HYLIFE-III paper would resolve this. Current value "Thermal (steam)" is defensible based on both companies' public statements but may be inaccurate for Xcimer's detailed design.

2. **Tritium Breeding — single table value**: The two companies use different blanket materials (FLiBe vs. liquid Li). The differentiation table needs either dual notation or a compromise value. "Li blanket (unspecified)" works if the table only allows one value per concept row.

3. **Repetition Rate — single table value**: Sub-Hz (Xcimer) vs. ~10 Hz (Inertia) spans over an order of magnitude. Both are valid for indirect-drive ICF but reflect fundamentally different laser architectures.

4. **Driver Technology — single table value**: Two different laser technologies. The concept is defined by target physics (indirect drive + hohlraum) more than by specific laser type.

5. **Xcimer concept classification**: Xcimer's HDD is increasingly distinct from NIF-style pure indirect drive. The first pulse is indirect (hohlraum → x-rays), but the main drive is direct through the formed plasma atmosphere. The 2024 Physics of Plasmas paper and 2025 APS-DPP presentation formalize this as a distinct approach. Schema may need a "Laser ICF (hybrid drive)" row.

6. **Inertia plant design details**: Inertia has not published a detailed power plant study. Their blanket architecture (liquid Li pipes), tritium extraction process, and thermal cycle are described only at high level. More detail may emerge from the SPIE Photonics West 2026 presentation or future publications.

## Sources Consulted

### Iter-02 New Sources (saved to `iter-02/sources/`)
- [Xcimer HDD Physics of Plasmas paper](https://pubs.aip.org/aip/pop/article/31/11/112708/3322685/Hybrid-direct-drive-with-a-two-sided-ultraviolet) — target physics evolution
- [NIF ignition achievements page](https://lasers.llnl.gov/science/achieving-fusion-ignition) — updated through Oct 2025, 10 ignitions, 8.6 MJ record
- [Xcimer Phoenix laser completion](https://xcimer.energy/xcimer-energy-completes-first-private-sector-electron-beam-excimer-laser/) — Jun 2025 milestone
- [Xcimer Vulcan site search](https://xcimer.energy/vulcan-site-search-begins-led-by-brian-boggs/) — 12 MJ, 2030 target
- [Inertia ENR interview (Mike Dunne)](https://www.enr.com/articles/62560-ten-minutes-with-mike-dunne-co-founder-and-cto-of-fusion-power-startup-inertia-enterprises) — plant specs, gain targets
- [Inertia BusinessWire launch](https://www.businesswire.com/news/home/20250826432256/en/) — founding team, technology overview
- [Inertia $450M GlobeNewsWire](https://www.globenewswire.com/news-release/2026/02/11/3236274/0/en/) — funding, steam turbine reference
- [Inertia optics.org coverage](https://optics.org/news/17/2/9) — $450M, Thunderwall specs
- [Bessemer blog on Inertia](https://www.bvp.com/news/powering-the-future-the-path-to-commercial-fusion-energy-with-inertia-enterprises) — investor perspective (limited technical detail)
- [HYLIFE-III nuclear analysis](https://www.sciencedirect.com/science/article/pii/S0920379624001868) — FLiBe, TBR >1.2 (paywalled, details from abstract/search)
- [DOE HYPER-LASER categorical exclusion](https://www.energy.gov/nepa/articles/cx-270844-xcimer-energy-inc-hybrid-pumped-excimer-laser-hyper-laser) — hybrid microwave+e-beam pumping
- [SPIE Photonics West Inertia presentation](https://spie.org/photonics-west/presentation/Introducing-inertia-enterprises--driving-a-direct-path-to-an/13888-11) — abstract only

### Iter-01 Sources (previously saved)
- `iter-01/sources/nif-ignition-achievements.md`
- `iter-01/sources/inertia-enterprises-website-and-faq.md`
- `iter-01/sources/xcimer-energy-website-and-science.md`

### Also Consulted (no new information beyond iter-01)
- [Xcimer approach page](https://xcimer.energy/approach/) — confirmed FLiBe, <1 Hz, HYLIFE-III
- [Xcimer science page](https://xcimer.energy/science/) — confirmed steam, wall-plug gain ~10
- [Inertia FAQ tritium](https://inertia.com/faq/where-will-you-get-tritium/) — liquid Li, government stockpiles
- [LIFE Wikipedia](https://en.wikipedia.org/wiki/Laser_Inertial_Fusion_Energy) — LLNL LIFE canceled 2013
- [SiliconANGLE Inertia funding](https://siliconangle.com/2026/02/11/fusion-power-startup-inertia-raises-450m-round-backed-gv/)
- [Fusion Report Inertia article](https://thefusionreport.com/a-new-player-enters-the-fusion-market/) — limited technical content

**Overall Confidence**: medium-high (upgraded from medium — both companies now have more public detail, NIF experimental record strengthened significantly with 8.6 MJ yield and 10 ignitions, Xcimer has demonstrated hardware)
