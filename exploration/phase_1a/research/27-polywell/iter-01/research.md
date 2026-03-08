# Polywell (D-T) — Research Dossier

**Concept**: Polywell (D-T)
**Company**: EMC2 (Energy Matter Conversion Corporation)
**Researcher**: Claude (automated)
**Date**: 2026-03-08
**Iteration**: 1
**Overall Confidence**: medium-low

---

## Column Findings

### Confinement Family
- **Value**: Electrostatic
- **Confidence**: high
- **Citation**: EMC2 website; Park et al., Phys. Rev. X 5, 021024 (2015)
- **Notes**: The Polywell combines magnetic cusp confinement of electrons with electrostatic confinement of ions. The dominant confinement mechanism for ions is the electrostatic potential well created by magnetically confined electrons. Per the ialtenergy.com summary: "an effective electrostatic confinement device, rather than magnetic confinement, although electromagnets were used to create it." Fits the schema's `Electrostatic` family.

### Confinement Concept
- **Value**: Polywell
- **Confidence**: high
- **Citation**: EMC2 website; Bussard (1985) original concept
- **Notes**: Exact match with schema vocabulary. Portmanteau of "polyhedral cusp" + "electrostatic potential well." Distinguished from IEC/Fusor by the use of magnetic cusp fields to confine electrons rather than a physical grid.

### Fuel
- **Value**: D-T
- **Confidence**: medium
- **Citation**: EMC2 website ("deuterium-tritium fuels"); arXiv:2508.06761 ("deuterium-tritium fuels for achieving net energy gain")
- **Notes**: EMC2's current focus is D-T for energy applications and FPNS neutron source. However, the concept has historically been discussed for multiple fuels. The Rogers (2018) published reactor design used p-B11. Bussard's original vision was p-B11. EMC2's FPNS work is explicitly D-T. For this dossier, D-T is correct per the concept definition in the differentiation table.

### Primary Heating
- **Value**: Electrostatic acceleration
- **Confidence**: high
- **Citation**: EMC2 website; Park et al. (2015); ialtenergy.com description
- **Notes**: Ions are accelerated toward the center by the electrostatic potential well created by magnetically confined electrons. WB-6 achieved 10 keV ion energies from a 10 kV potential well. This is the fundamental heating mechanism — no RF, NBI, or compression involved. The FPNS design also uses ion beams (150-200 keV), but those are external ion guns feeding into the electrostatic well, which is still the core acceleration mechanism.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: Search results referencing ~40% thermal efficiency for D-T Polywell; general physics reasoning
- **Notes**: For D-T fuel, 80% of fusion energy is carried by 14.1 MeV neutrons. Thermal conversion is the only practical option for capturing neutron energy. One source cites ~40% overall thermal efficiency for D-T Polywell. EMC2 has not published a specific thermal cycle choice (Rankine vs sCO2). Note: for the p-B11 variant, Bussard envisioned direct conversion of charged alphas at ~80% efficiency, but that does not apply to the D-T case.

### Plasma State
- **Value**: Confined
- **Confidence**: medium
- **Citation**: Park et al. (2015); EMC2 website description of "high-beta cusp confinement"
- **Notes**: The plasma is magnetically/electrostatically confined but not approaching ignition or self-sustaining burn in any demonstrated experiment. WB-8 achieved high-beta confinement but produced no fusion. The concept targets a sustained confined state, not a burning plasma — the electrostatic well continuously accelerates ions. `Confined` fits best: "Plasma in magnetic confinement but not necessarily approaching ignition." Could be argued as `Sustained` for a theoretical reactor, but given no demonstration of fusion burn, `Confined` is more accurate for the current state.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: Wikipedia (Polywell); search results on WB-series experiments
- **Notes**: All demonstrated Polywell devices (WB-1 through WB-8, WB-X) used resistive copper electromagnets. Bussard's vision for a reactor-scale device involved superconducting coils, and work reportedly began in 2012 on a superconducting Polywell, but no results were published. WB-8 operated at 0.8 T. FPNS design targets 2-3 T at boundary / 4-5 T on coil (magnet type unspecified). For the current state of the technology, `Resistive` is accurate. A reactor design might use superconducting coils, but none has been specified by EMC2.

### Tritium Breeding
- **Value**: TBD
- **Confidence**: medium
- **Citation**: No EMC2 publications on blanket design found
- **Notes**: As a D-T concept, tritium breeding is essential for a power reactor. EMC2 has not published any blanket design or tritium breeding approach. The FPNS work is a neutron source, not a power plant, so it doesn't address breeding. The Rogers (2018) paper used p-B11, not D-T, so it doesn't address breeding either. `TBD` is correct — the question applies but no answer has been disclosed.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: General physics (D-T produces 14.1 MeV neutrons); FPNS design mentions shielding
- **Notes**: D-T Polywell produces standard 14.1 MeV neutrons. The FPNS facility design "includes supporting systems such as tritium handling and shielding." No specific blanket/shield integration has been described for a power reactor. `Heavy shielding (14 MeV)` is the default for any D-T concept without an integrated blanket approach. Could become `Integrated blanket/shield` if EMC2 specifies a combined system, but nothing has been published.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: low
- **Citation**: Rogers (2018) simulated steady-state operation; Bussard's vision was continuous; EMC2 website describes "continuous fusion devices"
- **Notes**: This is the most uncertain column. Experimental devices were all pulsed (due to resistive coil heating — pulses < 1 ms to ~100 ms). However, the intended reactor design is steady-state: Bussard's vision with superconducting coils was continuous operation, Rogers (2018) simulated steady-state via diocotron-pumping, and EMC2's website describes "continuous fusion devices." The concept does not have a fundamental physics reason to be pulsed — pulsing was an engineering limitation of uncooled resistive coils. For the differentiation table (which captures the intended reactor concept, not just current experiments), `Steady-state` is the best fit, but at low confidence.

### Repetition Rate
- **Value**: N/A
- **Confidence**: low
- **Citation**: Follows from steady-state operation mode assignment
- **Notes**: If operation mode is steady-state, repetition rate is N/A. However, if the concept is actually pulsed in practice, a rep rate would apply. Given the low confidence on operation mode, this is also low confidence. N/A is consistent with the intended design.

### Driver Technology
- **Value**: Polyhedral magnetic cusp coils + electron beam injection
- **Confidence**: high
- **Citation**: EMC2 website; Park et al. (2015); multiple sources
- **Notes**: The distinguishing technology is the polyhedral arrangement of electromagnetic coils creating a cusp magnetic field, combined with electron beam injection to form the electrostatic potential well. WB-X used coaxial plasma guns for high-power startup (700 MW pulsed power). The FPNS variant adds external ion beam injection (150-200 keV). The "hard technology bet" is achieving and maintaining high-beta cusp confinement with sufficient electron confinement time.

---

## Metadata Columns

### Concept Name
- **Value**: Polywell (D-T)
- **Notes**: Distinguished from potential p-B11 variant. "Polywell" is the established name (Bussard, 1985).

### Companies
- **Value**: EMC2 (Energy Matter Conversion Corporation)
- **Notes**: Founded 1985 by Robert Bussard. Current president: Jaeyoung Park. Company status uncertain — one source says "ceased operating in 2019" but FPNS proposals with SHINE Technologies (2023-2024) suggest continued activity. Partnered with SHINE Technologies for FPNS.

### Description
- **Value**: Magnetic cusp confinement of electrons to create a deep electrostatic potential well that confines and accelerates ions. Polyhedral arrangement of electromagnetic coils creates cusp magnetic fields; injected electron beams form potential well that electrostatically confines and accelerates fuel ions to fusion energies. Combines magnetic and electrostatic confinement principles.
- **Confidence**: high

### Published Machine/Plant?
- **Value**: No (EMC2 has not published a power plant design). Rogers (2018) published a reactor design in J. Fusion Energy, but this was by an independent researcher, not EMC2.
- **Confidence**: high
- **Citation**: Literature search; Rogers, J.G., J. Fusion Energy 37, 1-17 (2018)

### Lab Experiments
- **Value**: WB-1 through WB-8 series (EMC2, 1985-2013); WB-X (EMC2, 2013); university Polywell experiments (various)
- **Confidence**: high
- **Citation**: Park et al., Phys. Rev. X 5, 021024 (2015); NBC News (2014); multiple sources
- **Notes**: Key results: WB-6 produced ~1 billion neutrons/s with D-D fuel. WB-8 demonstrated 6x higher plasma density but no fusion. WB-X demonstrated high-beta electron confinement (published in Phys. Rev. X). Navy funded WB-7 through WB-8 (~$12M total). Recent arXiv paper (2508.06761, 2025) "Polywell Revisited" with updated physics model.

---

## Remaining Gaps

### Low-confidence columns needing improvement:

1. **Operation Mode** (low confidence): The intended reactor design is steady-state, but all experiments were pulsed. A clearer statement from EMC2 about their commercial reactor operation mode would resolve this. The Rogers (2018) paper or the arXiv "Polywell Revisited" (2025) paper might contain more specific claims.

2. **Repetition Rate** (low confidence): Depends on operation mode resolution. If the concept turns out to be pulsed in commercial design, a rep rate would be needed.

3. **Tritium Breeding** (TBD): EMC2 has published nothing on blanket design. This is a fundamental gap — any D-T power reactor needs a breeding blanket, but EMC2 hasn't progressed to that level of design detail.

4. **Energy Capture** (medium confidence): `Thermal (unspecified)` is the default for D-T, but EMC2 hasn't specified Rankine vs sCO2 or any alternative.

5. **Magnet Type** (medium confidence): Experiments used resistive, but a reactor might use superconducting. EMC2's reactor-scale magnet plans are unclear.

### Conflicting information:

- **Company status**: One source says EMC2 "ceased operating in 2019," but the FPNS proposal with SHINE (2023-2024) and TOFE 2024 presentation suggest continued activity, possibly in a reduced or revived form.
- **WB-8 fusion**: WB-8 achieved high plasma density but produced no fusion, despite earlier WB-6 producing fusion. This discrepancy is acknowledged but not fully explained in public sources.

### Sources that might resolve gaps:

- **arXiv:2508.06761** "Polywell Revisited" (2025) — full text may contain updated reactor design parameters, operation mode specifics
- **Rogers (2018)** full paper — may have more detail on energy capture, though uses p-B11 not D-T
- **TOFE 2024 presentation** by Radel/Krall/Weber — FPNS design details, magnet specifications
- **EMC2 patents** — may contain reactor-level design details not in papers

---

## Sources Consulted

1. EMC2 Fusion website (https://www.emc2fusion.com/) — technology, about-us, FAQ pages (403 on direct fetch, used search snippets)
2. Wikipedia: Polywell (https://en.wikipedia.org/wiki/Polywell) — 403 on fetch, used search snippets
3. Park et al., "High-Energy Electron Confinement in a Magnetic Cusp Configuration," Phys. Rev. X 5, 021024 (2015) — https://journals.aps.org/prx/pdf/10.1103/PhysRevX.5.021024
4. Rogers, J.G., "A Polywell Fusion Reactor Designed for Net Power Generation," J. Fusion Energy 37, 1-17 (2018) — https://link.springer.com/article/10.1007/s10894-017-0147-9
5. arXiv:2508.06761, "Polywell Revisited" (2025) — https://arxiv.org/abs/2508.06761
6. Park, "Polywell Fusion: Electrostatic Fusion in a Magnetic Cusp," FPA 2014 presentation — https://fire.pppl.gov/FPA14_IECM_EMC2_Park.pdf
7. NBC News, "Low-Cost Fusion Project Steps Out of the Shadows" (2014) — https://www.nbcnews.com/science/science-news/low-cost-fusion-project-steps-out-shadows-looks-money-n130661
8. GeekWire, "EMC2 revives quest for nuclear fusion power" (2016) — https://www.geekwire.com/2016/emc2-revives-quest-to-harness-polywell-nuclear-fusion/
9. ialtenergy.com, "Polywell Fusion" — https://www.ialtenergy.com/polywell-fusion.html
10. Talk-Polywell.org forum — EMC2 FPNS proposal thread (https://talk-polywell.org/bb/viewtopic.php?t=6553), WB-7.1/WB-8 operation mode thread (https://talk-polywell.org/bb/viewtopic.php?t=2455)
11. NextBigFuture, "EMC2 Fusion Releases Results" (2014) — https://www.nextbigfuture.com/2014/10/emc2-fusion-releases-results-and-needs.html
12. The Fusion Report, "Interview with EMC2 Fusion" — https://thefusionreport.com/interview-with-emc2-fusion-a-different-approach-to-fusion/
13. Lynceans/EMC2, "The Fork in the Road to Electric Power From Fusion" (PDF) — https://lynceans.org/wp-content/uploads/2021/02/EMC2_US-converted.pdf
14. Sporer (2022), "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement" — https://plasmabay.engin.umich.edu/wp-content/uploads/sites/281/2022/10/Sporer-2022-Analysis-of-Two-Fusion-Reactor-Designs-Based-on-Magnetic-Electrostatic-Plasma-Confinement.pdf
