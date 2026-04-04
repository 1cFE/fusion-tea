# Concept Dossier: PoloMac Magnetic Confinement (Deutelio)

**Concept**: PoloMac (Poloidal Magnetic Confinement)
**Company**: Deutelio AG (Luxembourg-registered, Swiss origins)
**Overall Confidence**: medium-low

## Description

The Polomac is a poloidal magnetic confinement concept that uses an internal dipole coil to create a closed poloidal magnetic field. The key innovation is "magnetic tunnels" — regions where outboard magnetic field lines are deviated aside together with the plasma to create physical access channels to the internal dipole coil for structural support, power feed, and cooling. This solves the central problem that killed earlier poloidal confinement experiments in the 1980s: the internal coil supports contacted the plasma, destroying confinement. Deutelio's CTO Filippo Elio (University of Padua) revisited and refined this concept starting in 2014, publishing the foundational paper in Fusion Engineering and Design Vol. 89.

The concept is functionally similar to a levitated dipole, but with physical supports (shielded by magnetic tunnels) rather than magnetic levitation. It claims very high beta (20-30%) and steady-state operation at magnetic fields 3-5x lower than tokamaks.

---

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: JTSP 2024 technical report (DOI: 10.31281/med9bh43); Elio 2014, Fusion Engineering and Design Vol. 89
- **Notes**: Plasma confined by external/internal magnetic fields in steady-state. Clearly magnetic confinement.

### Confinement Concept
- **Value**: Levitated dipole
- **Confidence**: medium
- **Citation**: JTSP 2024 technical report; Wuslopebology fusion tier list 2024 ("like a levitated dipole where the dipole is really big and held in place with physical supports")
- **Notes**: The Polomac is a variant of the dipole concept — it uses an internal dipole coil creating a poloidal field, but instead of magnetic levitation (as in LDX/MIT), the coil is physically supported through "magnetic tunnels" that prevent plasma-support contact. The schema has `Levitated dipole` as the closest match, though "supported dipole" or "poloidal dipole" would be more precise. The proprietary name is "Polomac" (from "poloidal magnetic confinement"). Not a true levitated dipole since the coil is structurally supported, not levitated. Could also be described as a novel poloidal confinement concept distinct from standard dipole categories.

### Fuel
- **Value**: D-D
- **Confidence**: high
- **Citation**: JTSP 2024 technical report; Novable profile; Luxembourg Startup Directory; multiple Deutelio communications
- **Notes**: Deutelio explicitly targets D-D fusion to avoid the need for a tritium breeding blanket. The 2024 technical report states that with tokamak-strength fields, poloidal confinement can achieve D-D conditions. The company name itself (DEUTerio + ELIO = deuterium + helium) reflects this fuel choice. They acknowledge D-T is achievable at lower fields (3x weaker than tokamak) but position D-D as their commercial target.

### Primary Heating
- **Value**: Unknown
- **Confidence**: low
- **Citation**: No source specifies the heating method
- **Notes**: No publicly available information on the planned heating scheme. For a dipole-type concept, RF heating (ECRH or ICRH) would be physically plausible, as would neutral beam injection. The prototype uses only vacuum vessel and copper coils — no heating system has been described. D-D requires very high temperatures (~50-100 keV ion temperature), making the heating choice a critical design parameter that remains undisclosed.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: low
- **Citation**: Deutelio development roadmap mentions "heat generators" then "electrical generation plants"
- **Notes**: The development roadmap (Swiss Startup Association interview, Novable) describes first building "small heat generators operating with Deuterium" before "electrical generation plants with superconducting magnets." This implies thermal energy capture for the heat generator phase. D-D fusion produces 2.45 MeV neutrons (50% of reactions) plus charged particles (protons, tritons, He-3), so a thermal cycle for the neutron energy is the standard approach. However, no specific cycle (steam, sCO2) has been specified. The staged approach (heat first, electricity later) is unusual and may reflect the early development stage.

### Plasma State
- **Value**: Confined
- **Confidence**: medium
- **Citation**: JTSP 2024 technical report; Elio 2014 FED paper
- **Notes**: The concept targets steady-state magnetic confinement. Given the very early stage (no plasma demonstrated yet) and the D-D fuel choice (which requires extreme conditions for ignition), the realistic near-term target is "Confined" — plasma in magnetic confinement but not necessarily approaching ignition. If D-D ignition were achieved the state would be "Burning," but this is speculative for any D-D concept. The high beta (20-30%) claim, if validated, would support efficient confinement.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: JTSP 2024 technical report (prototype: water-cooled copper coils, 0.2-0.3 T); development roadmap mentions future superconducting magnets
- **Notes**: Current prototype uses resistive (water-cooled copper) coils at 0.2-0.3 T. The commercial roadmap envisions a transition to superconducting magnets for electrical generation plants, but the specific superconductor technology (HTS vs LTS) has not been disclosed. The 2014 FED paper describes a reactor-scale design with 1.4-1.8 T fields, which is achievable with either LTS or HTS. For the current state of the concept, `Resistive` is accurate; for the target commercial reactor, it would likely be HTS or LTS (TBD).

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: JTSP 2024 technical report; multiple company communications explicitly state D-D avoids tritium breeding blanket
- **Notes**: Deutelio explicitly targets D-D fusion specifically to avoid the need for a tritium breeding blanket. While D-D is not truly aneutronic (50% of D-D reactions produce 2.45 MeV neutrons, and the T and He-3 byproducts can undergo secondary D-T and D-He3 reactions), the fuel cycle does not require external tritium supply or breeding. The `N/A (aneutronic)` value is the closest schema match — D-D doesn't require tritium breeding. Note: D-D is not strictly "aneutronic" but it is "tritium-free" in terms of fuel supply. A more precise value might be "N/A — no tritium in primary fuel cycle" but the schema doesn't have that option.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: General D-D fusion physics; no Deutelio-specific neutron management information
- **Notes**: D-D fusion produces 2.45 MeV neutrons in ~50% of reactions. Additionally, the tritium and He-3 produced as D-D byproducts can undergo secondary D-T reactions (14.1 MeV neutrons) and D-He3 reactions within the plasma. At reactor-relevant conditions, secondary D-T reactions contribute significantly to the neutron spectrum, potentially producing 14 MeV neutrons. Therefore `Heavy shielding (14 MeV)` is appropriate, though the total neutron flux and energy spectrum will differ from a pure D-T reactor. Deutelio has not disclosed any neutron management approach. The schema notes D-D concepts should be assessed case-by-case.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: JTSP 2024 technical report ("works stably and continuously"); Elio 2014 FED paper; Novable ("works stably and continuously"); initial CSV ("Continuous")
- **Notes**: Multiple sources confirm steady-state operation. This is presented as a key advantage over tokamaks (which are pulsed or quasi-steady). Poloidal/dipole confinement is inherently steady-state — there is no inductive current drive cycle to interrupt.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed repetition.

### Driver Technology
- **Value**: Internal dipole coil with magnetic tunnel supports
- **Confidence**: high
- **Citation**: JTSP 2024 technical report (DOI: 10.31281/med9bh43); Elio 2014, FED Vol. 89
- **Notes**: The distinguishing technology is the magnetic tunnel concept — physically supported internal dipole coil where magnetic field lines are shaped to create plasma-free channels for structural supports, power feeds, and cooling lines. This is the "hard technology bet" for Polomac. If magnetic tunnels work as described (shielding supports from plasma contact without ruining confinement), this solves the central problem that killed poloidal confinement research in the 1980s. Skeptics (e.g., Wuslopebology tier list) question whether the magnetic tunnels can truly prevent plasma contact without degrading confinement. Prototype uses water-cooled copper coils (0.2-0.3 T); reactor design envisions 1.4-1.8 T with superconducting coils.

### Published Machine/Plant?
- **Value**: No (prototype design only)
- **Confidence**: high
- **Citation**: JTSP 2024 technical report describes small prototype vessel; Elio 2014 FED paper describes reactor-scale parameters
- **Notes**: The 2014 FED paper describes a reactor-scale design (dipole radius 5.4 m, plasma volume ~1300 m³, 1.4-1.8 T), but this is a conceptual design, not a published power plant. A small prototype vessel is described in the 2024 JTSP paper. No published machine or plant design exists.

### Lab Experiments
- **Value**: Prototype vessel constructed; no published plasma results
- **Confidence**: medium
- **Citation**: JTSP 2024 technical report (describes prototype vessel); ResearchGate figure "The vessel of the small Polomac prototype"
- **Notes**: A small prototype vessel has been built (shown in the 2024 technical report). The development plan calls for hydrogen plasma experiments to validate magnetic tunnels. No published plasma experimental results have been found. The concept rests on computational modeling validated against historical poloidal confinement data from the 1980s. Deutelio plans to "fine tune the Polomac technology in a laboratory" over the next 3 years (as of 2025).

---

## Remaining Gaps

### Unresolved columns:

1. **Primary Heating** (Unknown): No source describes the heating method. This is a significant gap — D-D fusion requires extreme temperatures and the heating scheme is a major engineering decision. The JTSP and FED papers focus on confinement geometry, not heating. A future iteration should look for any conference presentations or patent filings that might disclose the heating approach.

2. **Energy Capture** (low confidence): Only inferred from vague roadmap language ("heat generators" → "electrical generation plants"). No specific thermal cycle or conversion technology has been disclosed.

3. **Magnet Type** (medium confidence for current, unknown for commercial): Prototype uses resistive copper. Commercial path mentions "superconducting" but doesn't specify HTS vs LTS. Given the low field requirements (1.4-1.8 T), either could work.

4. **Neutron Management** (medium confidence): No Deutelio-specific information. Value inferred from D-D fusion physics. The secondary D-T neutron contribution in a D-D plasma is a real concern but Deutelio hasn't addressed it publicly.

5. **Plasma State** (medium confidence): "Confined" is used as a conservative assessment. Deutelio's actual target plasma state (sustained vs burning) is not clearly stated.

### What would raise confidence:

- **Full text of the 2014 FED paper** (behind ScienceDirect paywall): Likely contains more detail on plasma parameters, heating approach, and reactor design.
- **Full text of the 2024 JTSP paper** (CC-BY, should be downloadable): May contain prototype specifications and computational results.
- **Patent filings**: Could reveal heating method, magnet design, or energy capture approach.
- **Conference presentations**: Any APS-DPP, EPS, or SOFT presentations by the team.

### Corrections to initial data:

- **Boldbrain**: The initial description says "Boldbrain Startup Challenge 2025" but the actual placement was **2024 edition** (4th place, 10,000 CHF prize). The 2025 edition has selected 20 projects but results aren't out yet.
- **Company registration**: Luxembourg, not Switzerland (though Swiss-associated through Boldbrain/Innosuisse).

---

## Sources Consulted

1. **JTSP 2024 Technical Report**: https://www.jtsp.eu/jtsp/article/view/32 — Primary technical source. DOI: 10.31281/med9bh43
2. **Elio 2014 FED Paper**: https://www.sciencedirect.com/science/article/pii/S0920379614003834 — Foundational paper (paywall, details from abstract/search snippets only)
3. **ResearchGate PDF**: https://www.researchgate.net/publication/385187195_Technical_Report_The_Polomac_approach_to_fusion_energy — Mirror of JTSP paper with figures
4. **Swiss Startup Association Interview**: https://swissstartupassociation.ch/2025/03/03/meet-francesco-elio-co-founder-and-ceo-of-deutelio-ag/ — CEO interview with development timeline
5. **Novable Profile**: https://novable.com/5-innovative-solutions-in-the-fusion-energy-industry/ — Company description with 4-5x field reduction claim and 2030 target
6. **Deutelio Website**: https://www.deutelio.com/ — Did not load useful content (JavaScript-only rendering)
7. **Deutelio Facebook**: https://www.facebook.com/deutelio — Video about poloidal confinement to Polomac evolution
8. **Luxembourg Startup Directory**: https://directory.startupluxembourg.com/companies/deutelio — Company registration details
9. **Boldbrain 2024 Results**: https://www.boldbrain.ch/en/2024-edition/ — 4th place, 10,000 CHF
10. **Startupticker Boldbrain**: https://www.startupticker.ch/en/news/expediting-drug-discovery-with-ai-in-virtuo-labs-wins-boldbrain-startup-challenge — 2024 edition winner announcement
11. **Wuslopebology Fusion Tier List**: https://kunimune.blog/2024/04/22/fusion-company-tier-list-2024/ — C− rating with skepticism about magnetic tunnel feasibility
12. **Nuclear Business Platform**: https://www.nuclearbusiness-platform.com/media/insights/62-billion-fusion-energy-funding-race-turning-the-dream-of-creating-a-star-on-earth-into-reality — Brief mention
