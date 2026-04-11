# MagLIF (D-T) — Concept Dossier

**Concept**: MagLIF (D-T) — Magnetized Liner Inertial Fusion
**Companies**: Pacific Fusion, Fuse Energy Technologies
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: high

> **Note on Europa Fusion**: The original concept CSV listed "Europa Fusion" as a company. Extensive searching across two iterations found only an empty LinkedIn page (India-based). No technical information, website, press coverage, FIA membership, or ARPA-E awards exist. **Fuse Energy Technologies** (San Leandro, CA) is a well-documented second MagLIF private company and has been substituted. Europa Fusion may be confused with EUROfusion (EU research consortium) or Fusion for Energy (EU ITER agency).

> **Note on Fuse Energy Technologies**: Fuse's planned pilot plant (Apeiron I) is a **hybrid fusion-fission** concept — using MagLIF fusion neutrons to drive fission in a uranium/spent-fuel blanket, amplifying ~20 MW fusion to ~3 GW thermal. This is architecturally distinct from a pure MagLIF fusion power plant. The MagLIF physics are the same; the power plant concept diverges significantly from the pure-fusion Z-IFE heritage.

## Description

MagLIF uses pulsed power (massive current pulses from capacitor banks) to implode a metal liner around pre-magnetized, optionally laser-preheated deuterium-tritium fuel. The axial magnetic field suppresses thermal conduction losses during implosion, allowing fusion conditions at intermediate density and timescale — between traditional MFE and laser ICF. Developed at Sandia National Laboratories on the Z Machine (20+ MA, ~80 TW), with over 70 successful fusion-producing experiments. Pacific Fusion is developing simplified self-magnetizing targets that eliminate external coils and aim to eliminate laser preheat, using impedance-matched Marx generators (IMGs) as the driver. Pacific Fusion's demonstration system targets 156 pulser modules delivering 60+ MA from ~80 MJ stored energy, with net facility gain by 2030.

---

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: Schema definition; arXiv:2408.15206 ("magneto-inertial fusion"); Wikipedia MagLIF article
- **Notes**: MagLIF is the canonical MIF concept — magnetized plasma compressed by an external pulsed power driver. Intermediate between MFE and IFE in density (~10²⁰–10²³ cm⁻³) and timescale (~100 ns implosion).

### Confinement Concept
- **Value**: `Magnetized target (pulsed power)`
- **Confidence**: high
- **Citation**: Schema vocabulary; Sandia MagLIF program description (https://www.sandia.gov/z-machine/fusion/)
- **Notes**: MagLIF uses pulsed power (Z-machine class) to implode a cylindrical metal liner. This is distinct from `Magnetized target (pneumatic)` (General Fusion) which uses mechanical compression.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Pacific Fusion founders' letter explicitly states "deuterium-tritium fuel" (https://www.pacificfusion.com/updates/founders-letter); Sandia MagLIF experiments use DD for scientific studies but D-T is the target commercial fuel.
- **Notes**: Sandia lab experiments typically use pure deuterium for diagnostic simplicity (DD neutrons are easier to measure), but the commercial concept targets D-T for its higher reactivity and energy yield. Pacific Fusion explicitly confirms D-T.

### Primary Heating
- **Value**: `Pulsed power implosion`
- **Confidence**: high
- **Citation**: Schema definition ("Massive current drives liner implosion; may include laser preheat"); arXiv:2408.15206; Pacific Fusion breakthrough article
- **Notes**: Traditional MagLIF has three stages: (1) axial premagnetization (10–30 T), (2) laser preheat (~100s eV), (3) pulsed power implosion (20+ MA, ~100 ns). Pacific Fusion's self-magnetizing targets eliminate external premagnetization coils, and they are working to eliminate laser preheat entirely. The dominant heating mechanism is adiabatic compression from the liner implosion driven by pulsed current.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: arXiv:2408.15206 ("~80% of the fusion energy released streams out as 14 MeV neutrons... absorbed in surrounding blankets for heat recovery"); Z-IFE SAND2006-7148
- **Notes**: As a D-T concept, ~80% of energy is in 14 MeV neutrons that must be captured thermally. The Z-IFE study (SAND2006-7148) evaluated four power conversion cycles — supercritical CO2 Brayton, steam Rankine, gas Brayton, and combined Brayton-Rankine — and concluded that the combined cycle was optimal for Z-IFE. Neither Pacific Fusion nor Fuse has publicly specified their thermal cycle. Pacific Fusion's demonstration system uses a de-ionized water tank for neutron/X-ray absorption, but this is a demo choice, not a power plant design. Fuse's Apeiron I is a hybrid fusion-fission concept with fundamentally different energy conversion. Recording as `Thermal (unspecified)` since the pure-fusion thermal cycle is undisclosed.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: Schema definition ("Plasma driven to fusion conditions by implosion... Characteristic of IFE and MIF"); MagLIF Wikipedia article
- **Notes**: The fuel is compressed by the imploding liner from initial ~mm radius to ~100 μm, reaching fusion-relevant temperatures (>3.1 keV demonstrated, multi-keV target) and densities. This is a classic compressed plasma state — short-lived, driven by external implosion.

### Magnet Type
- **Value**: `Pulsed EM`
- **Confidence**: high
- **Citation**: arXiv:2408.15206; Pacific Fusion website ("fast-rising, high-current pulses")
- **Notes**: The driving magnetic field is generated by massive pulsed current (20+ MA on Z Machine, 60+ MA target for Pacific Fusion demo) through the liner, creating an intense azimuthal field. The premagnetization field (axial, 10–30 T) is also pulsed (ms timescale). Pacific Fusion's self-magnetizing targets generate the axial field from the drive current itself — no external coils needed. No superconducting magnets are involved; this is purely pulsed resistive/capacitive technology.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: medium
- **Citation**: arXiv:2408.15206 ("tritium-producing blanket to replenish burnt, lost, and decayed inventory"); Z-IFE studies (SAND2006-7148, OSTI biblio/771517)
- **Notes**: Neither Pacific Fusion nor Fuse has publicly specified a blanket type for pure-fusion operation. The Z-IFE power plant concept identified FLiBe as the baseline blanket material — serving as breeder, coolant, and shielding, with the recyclable transmission line (RTL) potentially cast from frozen FLiBe. Fuse's Apeiron I uses a uranium/spent-fuel blanket for hybrid fusion-fission — this is not a tritium breeding blanket in the conventional sense. For a pure MagLIF fusion plant, `FLiBe blanket` is the most likely outcome based on Z-IFE heritage, but no company has confirmed. Recording as `TBD`.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: Z-IFE SAND2006-7148 ("thick-liquid-wall chamber to absorb target emissions"); arXiv:2408.15206; Pacific Fusion interview (water tank for demo)
- **Notes**: MagLIF produces 14.1 MeV D-T neutrons requiring heavy management. The Z-IFE concept uses a thick-liquid-wall chamber (FLiBe) that absorbs X-rays, debris, and neutrons — serving simultaneous roles as energy absorber, tritium breeder, and blast mitigator. This is a natural `Integrated blanket/shield` architecture. Pacific Fusion's demonstration system uses a de-ionized water tank for neutron/X-ray absorption (a simpler choice for a non-power-producing demo). The pulsed nature (each shot produces blast debris from the destroyed liner/RTL) strongly favors an integrated thick-liquid approach over separate solid blanket and shield layers.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: Pacific Fusion website ("process is repeated over and over, like in a piston engine"); MagLIF concept description (100 ns implosion pulse)
- **Notes**: Each fusion event is a discrete ~100 ns implosion. The target (liner + fuel) is destroyed and must be replaced each shot. This is unambiguously pulsed operation.

### Repetition Rate
- **Value**: `Sub-Hz`
- **Confidence**: medium
- **Citation**: Z-IFE studies (0.1 Hz baseline, one shot every ~10 seconds); arXiv:2408.15206 ("Hertz-scale repetition rates"); IMG capability >0.1 Hz
- **Notes**: The Z-IFE power plant concept targeted 0.1 Hz with high yields (2–3 GJ/shot baseline, up to 20 GJ/shot single-chamber variant) to compensate for low rep rate. The arXiv paper mentions "Hertz-scale" as a general target for pulsed magnetic fusion. IMGs support >0.1 Hz repetition. Pacific Fusion describes the process as "like a piston engine" suggesting they aim for ~1 Hz, but no specific rate disclosed. Key constraints on rep rate: target fabrication/insertion, RTL replacement, chamber clearing after each shot. Recording as `Sub-Hz` based on the most detailed engineering study (Z-IFE 0.1 Hz), but `~1 Hz` remains plausible for next-generation IMG-based designs. The Z-IFE multi-chamber concept (12 chambers, 10 active) achieves effective ~1 Hz aggregate rate.

### Driver Technology
- **Value**: `Pulsed power (Z-machine class)`
- **Confidence**: high
- **Citation**: Pacific Fusion website; GA partnership press release; arXiv:2408.15206; Fuse Energy website
- **Notes**: Both Pacific Fusion and Fuse use impedance-matched Marx generators (IMGs) — a next-generation pulsed power architecture with ~90% energy efficiency, 200 kV operation (vs 6 MV for Z Machine), and multi-million shot lifetimes. Pacific Fusion's demonstration system: 156 modules, 320 bricks/module (±100 kV, 160 nF per brick), ~80 MJ stored energy, delivering 60+ MA in ~100 ns. Each module ~1.9 m diameter, fits a shipping container. Fuse's TITAN I: 238 bricks, 14 stages, 0.8 MA, 1.6 MV, 1 TW peak power. Z STAR (2027): 16 TITANs, 15 TW, 12.8 MA.

### Published Machine/Plant?
- **Value**: No (but Z-IFE power plant concept studies exist from Sandia)
- **Confidence**: high
- **Citation**: Z-IFE concept (OSTI biblio/771517, SAND2006-7148); no published reactor design from Pacific Fusion or Fuse
- **Notes**: The Z-IFE power plant concept (ZP3) was a Sandia conceptual study from the 2000s, evaluating multi-chamber pulsed power plants with FLiBe blankets and combined-cycle thermal conversion. Pacific Fusion and Fuse have not published specific reactor or plant designs. Pacific Fusion targets net facility gain by 2030 (demonstration system) and commercial systems by mid-2030s.

### Lab Experiments
- **Value**: Sandia Z Machine (MagLIF experiments, 70+ shots), NRL (magnetized ICF theory/modeling), Fuse FAETON/TITAN
- **Confidence**: high
- **Citation**: Sandia Z Machine fusion page; MagLIF Wikipedia; arXiv:2504.03919; Fuse Energy website
- **Notes**: Over 70 MagLIF experiments on the Z Machine have produced fusion-relevant ion temperatures (>3.1 keV), thermonuclear DD neutron yields up to 1.1 × 10¹³, and demonstrated magnetic trapping of charged fusion particles. Pacific Fusion's self-magnetizing target experiments at Sandia (Feb 2026) demonstrated simplified target concepts with 22 MA pulses. Fuse's FAETON I produces 1+ trillion neutrons; TITAN demonstrated 1 TW IMG with 100+ repetitive shots. NRL has contributed theoretical work on magnetized ICF concepts.

---

## Remaining Gaps

### Columns with medium confidence that could be improved:

1. **Energy Capture** (medium): Neither company has disclosed thermal cycle choice. The Z-IFE study concluded combined Brayton-Rankine is optimal, but this is a 2006-era study. A company press release or DOE/ARPA-E award specifying balance-of-plant would resolve this. Could potentially be upgraded to `Thermal (sCO2)` if companies follow modern fusion plant trends, but no evidence yet.

2. **Tritium Breeding** (medium/TBD): No blanket type disclosed by either company for pure-fusion operation. Z-IFE heritage points to FLiBe. Fuse's hybrid fusion-fission approach (uranium blanket in Apeiron I) is architecturally different. A company disclosure or detailed power plant study would resolve this.

3. **Repetition Rate** (medium): Range spans 0.1 Hz (Z-IFE) to "Hertz-scale" (arXiv paper). Pacific Fusion's "piston engine" analogy and IMG capabilities (>0.1 Hz) suggest they're aiming above 0.1 Hz. A specific company target would resolve this. The Z-IFE multi-chamber approach (12 chambers) sidesteps the per-chamber rate limit.

4. **Neutron Management** (medium): Classified as `Integrated blanket/shield` based on Z-IFE thick-liquid-wall heritage. Pacific Fusion's demo uses water tank (simpler). No commercial plant neutron management architecture disclosed.

### Europa Fusion
- **Status**: Could not verify as a real MagLIF company (searched across two iterations)
- **Sources checked (iter-01)**: Google, LinkedIn, FIA, Fusion Energy Base, Wikipedia list of nuclear fusion companies, Sifted European fusion map
- **Sources checked (iter-02)**: Additional targeted searches for "Europa Fusion company magnetized target fusion" — only General Fusion results
- **Recommendation**: Remove from concept CSV or flag for manual verification. Substitute with Fuse Energy Technologies.

### Fuse Energy — Hybrid Fusion-Fission Note
- Fuse Energy's Apeiron I plant concept is a **hybrid fusion-fission** design, not pure MagLIF fusion. The MagLIF physics for creating fusion neutrons are the same, but the power amplification (~150×) via fission blanket makes it a fundamentally different power plant concept. For differentiation table purposes, the MagLIF fusion physics columns (confinement, fuel, heating, plasma state, etc.) are unchanged. The power plant columns (energy capture, blanket, neutron management) would differ significantly for Fuse's hybrid approach vs. a pure-fusion MagLIF plant.

## Sources Consulted

### Pacific Fusion
- [Pacific Fusion Homepage](https://www.pacificfusion.com/)
- [Pacific Fusion Founders' Letter](https://www.pacificfusion.com/updates/founders-letter)
- [Pacific Fusion 1000x Leap](https://www.pacificfusion.com/updates/a-1000x-leap-toward-commercial-fusion)
- [Pacific Fusion Experimental Breakthrough (Feb 2026)](https://www.pacificfusion.com/updates/experimental-breakthrough-by-pacific-fusion-clears-major-obstacle-to-affordable-commercial-fusion)
- [Pacific Fusion + GA Partnership](https://www.ga.com/pacific-fusion-and-ga-team-up-to-deliver-breakthroughs-in-inertial-fusion-energy)
- [ANS: Pacific Fusion predicts 1000-fold leap](https://www.ans.org/news/2025-04-21/article-6938/)
- [ANS: Pacific Fusion + GA pulser innovation](https://www.ans.org/news/2025-04-24/article-6980/)
- [ANS: Fusion simplification (Feb 2026)](https://www.ans.org/news/2026-02-06/article-7739/)
- [The Fusion Report: Interview with Pacific Fusion](https://thefusionreport.substack.com/p/interview-with-pacific-fusion-on) — demo system specs (156 modules, water tank, 80 MJ, 6 m insulator stack)
- [TechCrunch: Pacific Fusion power plant plan](https://techcrunch.com/2025/04/15/heres-how-pacific-fusion-plans-to-build-a-fusion-power-plant/) (paywalled)
- [Interesting Engineering: Pulser module 2TW](https://interestingengineering.com/energy/pulser-module-to-deliver-fusion-conditions)

### Fuse Energy Technologies
- [Fuse Energy Homepage](https://www.f.energy/)
- [Fuse Energy Wikipedia](https://en.wikipedia.org/wiki/Fuse_Energy_Technologies_Corporation) (403 at time of fetch)
- [Not Boring: Fuse Energy](https://www.notboring.co/p/fuse-energy) — TITAN specs, Z STAR, Apeiron I hybrid fusion-fission details
- [Indian Defence Review: TITAN coverage](https://indiandefencereview.com/built-by-a-25-year-old-this-reactor-just-fired-the-energy-of-800-lightning-bolts/)
- [FusionXInvest: Fuse profile](https://fusionxinvest.com/company-profile/4441/fuse/)

### Technical Papers
- [arXiv:2408.15206 — Opportunities in Pulsed Magnetic Fusion Energy](https://arxiv.org/html/2408.15206v1)
- [arXiv:2504.03919 — Magnetized ICF implosions (NRL)](https://arxiv.org/html/2504.03919v1)
- [arXiv:2505.01784 — ARPA-E BETHE-GAMOW Retrospective](https://arxiv.org/html/2505.01784v2) — Pacific Fusion not mentioned (program-era mismatch)
- [OSTI: Z-IFE Power Plant SAND2006-7148](https://www.osti.gov/servlets/purl/901970/) — thermal cycle analysis (combined Brayton-Rankine recommended)
- [OSTI: Z-Pinch Power Plant Concept](https://www.osti.gov/biblio/771517) — ZP3 conceptual study
- [ScienceDirect: Nuclear design for Z-IFE chambers](https://www.sciencedirect.com/science/article/abs/pii/S092037960500712X) — FLiBe, 0.1 Hz, 20 GJ/shot option
- [Innovation News Network: MD-IFE](https://www.innovationnewsnetwork.com/magnetic-drive-inertial-fusion-energy-md-ife/53054/) (content not extractable)

### Reference
- [Wikipedia: Magnetized liner inertial fusion](https://en.wikipedia.org/wiki/Magnetized_liner_inertial_fusion)
- [Sandia Z Machine Fusion Page](https://www.sandia.gov/z-machine/fusion/)
- [DOE Fusion S&T Roadmap (Oct 2025)](https://www.energy.gov/sites/default/files/2025-10/fusion-s&t-roadmap-101625.pdf)

### Europa Fusion (negative results — both iterations)
- LinkedIn page exists (India-based, no content)
- Not listed: FIA, Wikipedia fusion companies list, Fusion Energy Base, Sifted EU fusion map
- Not found in ARPA-E BETHE retrospective
- Targeted search "Europa Fusion company magnetized target fusion" returned only General Fusion results
