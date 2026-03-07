# Concept Dossier: QI Stellarator - HTS (D-T)

**Company**: Proxima Fusion (Munich, Germany)
**Concept**: Quasi-isodynamic optimized stellarator with HTS magnets
**Published Machine/Plant**: Stellaris (published in Fusion Engineering and Design, Vol. 214, May 2025)
**Lab Experiments**: Wendelstein 7-X (IPP Greifswald), LHD (NIFS Japan), HSX (UW-Madison)

---

## Column Values

### 1. Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology
- **Notes**: Magnetic confinement via externally generated 3D helical fields. Stellarators are archetypal MFE devices — steady-state magnetic confinement with no plasma current.

### 2. Confinement Concept
- **Value**: `Stellarator (QI)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; Stellaris paper DOI: 10.1016/j.fusengdes.2025.114868
- **Notes**: Quasi-isodynamic (QI) optimization — trapped particle orbits are well-confined via poloidally closed contours of the second adiabatic invariant. This is the same optimization approach as Wendelstein 7-X. Proxima's design name is "Stellaris."

### 3. Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained
- **Notes**: Deuterium-Tritium fuel cycle confirmed. Stellaris includes WCLL tritium breeding blanket with TBR of 1.07. Proxima's tritium blog post extensively discusses D-T fuel requirements and breeding self-sufficiency.

### 4. Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: medium
- **Citation**: Inferred from W7-X heritage; https://en.wikipedia.org/wiki/Wendelstein_7-X; ECRH power upgrade paper at EPJ Web of Conferences
- **Notes**: Proxima Fusion has not explicitly specified the heating method for Stellaris in publicly available sources. However, ECRH is the universal stellarator heating method — W7-X uses ECRH exclusively (10 gyrotrons at 140 GHz, 0.6–1.0 MW each). Stellarators lack plasma current, so ohmic heating is unavailable. ECRH is the standard choice for QI stellarators. Confidence is medium because Proxima has not directly confirmed this for Stellaris, but it would be extraordinary if they chose anything else as the primary method.

### 5. Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: Inferred from WCLL blanket design (water-cooled); https://binding.energy/stellarator-fusion-energy/
- **Notes**: Stellaris uses a Water-Cooled Lithium-Lead (WCLL) blanket with water as coolant and EUROFER97 structural steel at <500°C. The water-cooled design strongly implies a steam Rankine cycle for energy conversion — this is the standard power conversion pathway for WCLL blankets in the EUROfusion program. However, Proxima has not explicitly stated the power conversion cycle. Classified as "unspecified" rather than "steam" because no direct confirmation exists. The analogous Helios stellarator design (Thea Energy) uses a Rankine cycle with 635°C superheated steam.

### 6. Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: https://www.proximafusion.com/technology (targeting net energy / commercial power plant)
- **Notes**: Stellaris is designed as a commercial power plant, which implies a burning plasma with Q >> 5 where alpha heating dominates. The Alpha demo (2031) targets "net energy production." However, no specific Q value has been published. Classified as Burning rather than Sustained because the commercial plant target implies ignition-class performance.

### 7. Magnet Type
- **Value**: `HTS (3D stellarator)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; https://binding.energy/stellarator-fusion-energy/; https://www.prnewswire.com/news-releases/faraday-factory-japan-signed-an-agreement-to-deliver-superconductor-tape-for-the-demo-stellarator-magnet-of-proxima-fusion-302486210.html
- **Notes**: HTS magnets producing up to 20 T fields in modular high-field configuration. REBCO tape supplied by Faraday Factory Japan. Developed with PSI & BNET. The 3D non-planar coil geometry is inherent to stellarator design — these are complex twisted coils producing the helical magnetic field externally. The Stellarator Model Coil (SMC) demo magnet is targeted for 2027 to de-risk HTS stellarator coil manufacturing.

### 8. Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained; https://binding.energy/stellarator-fusion-energy/
- **Notes**: Water-Cooled Lithium-Lead (WCLL) blanket with TBR of 1.07. This is a lead-lithium eutectic blanket cooled by pressurized water — the same concept as the EU DEMO WCLL blanket. Proxima notes this is a "concept, not a complete engineering design" and was demonstrated as viable "without suggesting this is the optimal choice." They have also applied for a patent on an "innovative liquid-metal breeding blanket." EUROFER97 structural steel, <500°C operating temperature.

### 9. Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: https://www.proximafusion.com/technology (describes "neutron blanket concept adapted to complex geometry of stellarators"); Stellaris paper DOI: 10.1016/j.fusengdes.2025.114868
- **Notes**: D-T fusion produces 14.1 MeV neutrons requiring heavy shielding. The WCLL blanket serves as both tritium breeder and neutron attenuator — the lead provides neutron multiplication and the water provides moderation. Neutronic simulations were part of the integrated Stellaris design. Classified as "Integrated blanket/shield" because the blanket explicitly serves dual purpose. No separate shielding architecture has been described — the blanket IS the primary neutron management system, adapted to the complex stellarator geometry.

### 10. Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology
- **Notes**: Stellarators are inherently steady-state — no plasma current means no need for current drive or pulsed inductive startup. Proxima explicitly describes "24/7 continuous operation" and "disruption-free design." This is a fundamental advantage of the stellarator approach over tokamaks.

### 11. Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: N/A — continuous steady-state operation
- **Notes**: Repetition rate is structurally inapplicable to steady-state concepts. Stellaris operates continuously, not in pulses.

### 12. Driver Technology
- **Value**: `3D HTS stellarator coils (REBCO, 20 T)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; https://binding.energy/stellarator-fusion-energy/
- **Notes**: The key technology bet is manufacturing complex 3D non-planar HTS coils from REBCO tape at up to 20 T field strength. This is the defining engineering challenge — stellarator coils are far more geometrically complex than tokamak D-shaped coils. Proxima uses AI-driven optimization for coil design. The Stellarator Model Coil (SMC) demo in 2027 is the critical de-risking milestone. Coils developed with PSI & BNET. The combination of QI optimization + HTS + modular architecture is what distinguishes Proxima from other stellarator companies (Type One Energy uses modular coils, Thea Energy uses planar arrays, Renaissance Fusion uses laser-patterned HTS film).

---

## Remaining Gaps

### Low-confidence or inferred values:

1. **Primary Heating (medium)**: ECRH is inferred from stellarator physics and W7-X heritage. To raise to high confidence, would need Proxima to explicitly state the heating method for Stellaris. The Stellaris paper (Fusion Engineering and Design) likely specifies this but is behind a paywall.

2. **Energy Capture (medium)**: "Thermal (unspecified)" because the WCLL blanket strongly implies steam Rankine but Proxima hasn't explicitly confirmed the power cycle. The full Stellaris paper likely discusses this. Could also be upgraded to sCO2 Brayton at some future design iteration.

3. **Plasma State (medium)**: "Burning" is inferred from commercial power plant targets. No specific Q value or ignition target has been published. The Stellaris paper may contain plasma performance targets.

4. **Neutron Management (medium)**: "Integrated blanket/shield" is inferred from the WCLL blanket design and neutronic simulations. The specific shielding architecture beyond the blanket is not described in public sources.

### What would resolve these gaps:
- **Full Stellaris paper** (DOI: 10.1016/j.fusengdes.2025.114868) — likely contains heating specifications, power output, plasma parameters, and detailed blanket/shielding architecture
- **Proxima Fusion technical presentations** at conferences (APS-DPP, IAEA FEC, IEEE SOFE)
- **Future press releases** as they progress toward the SMC demo (2027)

### No conflicting information found
All sources are consistent. The only nuance is that Proxima has stated the WCLL blanket is a concept demonstration, not necessarily the final choice — but it is the published baseline for Stellaris.

---

## Sources Consulted

1. [Proxima Fusion Technology Page](https://www.proximafusion.com/technology) — company technology overview
2. [Proxima Fusion Homepage](https://www.proximafusion.com/) — company overview and timeline
3. [Stellaris Press Release](https://www.proximafusion.com/press-news/proxima-fusion-and-partners-publish-stellaris-fusion-power-plant-concept-to-bring-limitless-safe-clean-energy-to-the-grid) — Stellaris announcement
4. [Proxima Fusion Tritium Blog](https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained) — WCLL blanket details, TBR 1.07
5. [Binding Energy Analysis](https://binding.energy/stellarator-fusion-energy/) — WCLL details, EUROFER97, 20 T magnets, TBR 1.07
6. [Stellaris Paper (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0920379625000705) — paywalled, abstract only
7. [Stellaris Paper (KIT Repository)](https://publikationen.bibliothek.kit.edu/1000179851) — metadata/abstract only
8. [World Nuclear News](https://www.world-nuclear-news.org/articles/german-stellarator-fusion-design-concept-unveiled) — Stellaris announcement coverage
9. [Nuclear Engineering International](https://www.neimagazine.com/news/proxima-unveils-stellaris-fusion-plant-design/) — Stellaris coverage
10. [Fusion Energy Insights](https://fusionenergyinsights.com/blog/post/fusion-energy-insights-examined-an-analysis-of-proxima-fusion-s-bold-plan-for-a-stellarator-power-plant) — analysis (detailed content paywalled)
11. [IEEE Spectrum - Stellarator Showdown](https://spectrum.ieee.org/stellarator) — comparison with Type One Energy (content not extractable)
12. [Faraday Factory Japan PR](https://www.prnewswire.com/news-releases/faraday-factory-japan-signed-an-agreement-to-deliver-superconductor-tape-for-the-demo-stellarator-magnet-of-proxima-fusion-302486210.html) — HTS tape supply for SMC demo
13. [Max Planck Society](https://www.mpg.de/25464702/proxima-fusion-on-the-home-stretch-to-fusion-power) — company profile (content not extractable)
14. [Wikipedia - Proxima Fusion](https://en.wikipedia.org/wiki/Proxima_Fusion) — (403 access error)
15. [Climate Insider](https://climateinsider.com/2025/02/26/proxima-fusion-proposes-next-generation-stellarator-for-fusion-power-plants/) — Stellaris coverage (403 access error)
16. [Wikipedia - Wendelstein 7-X](https://en.wikipedia.org/wiki/Wendelstein_7-X) — ECRH details for reference stellarator
17. [EPJ Web of Conferences - W7-X ECRH Upgrade](https://www.epj-conferences.org/articles/epjconf/abs/2023/03/epjconf_ec212023_04003/epjconf_ec212023_04003.html) — ECRH system specifications
18. [NucNet - RWE/Bavaria MoU](https://www.nucnet.org/news/proxima-fusion-signs-mou-with-rwe-and-bavaria-to-develop-fusion-power-2-5-2026) — Gundremmingen site agreement
19. [Dassault Systèmes](https://www.3ds.com/3dexperiencelab/portfolio/proxima-fusion) — company profile
