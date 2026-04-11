# QI Stellarator - HTS (D-T)

**Company**: Proxima Fusion (Munich, Germany)
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

Quasi-isodynamic (QI) optimized stellarator using HTS (REBCO) magnets at up to 20 T, designed by Proxima Fusion as a spin-off from Max Planck Institute for Plasma Physics. The published power plant concept, Stellaris (Fusion Engineering and Design, 2025), features 3D non-planar HTS coils, a Water-Cooled Lithium-Lead (WCLL) blanket with TBR 1.07, EUROFER97 structural steel, and inherently steady-state, disruption-free operation. Peak fusion power is 2.7 GW, thermal power ~3.1 GW, with ~1 GW net electrical output. The design builds directly on the Wendelstein 7-X QI stellarator physics basis while leveraging HTS magnets for compactness and higher field strength.

In February 2026, Proxima signed an MoU with RWE, Bavaria, and Max Planck IPP to build Alpha (demo stellarator, Q>1, ~2031, Garching) followed by Stellaris (commercial plant, Gundremmingen, later 2030s). Alpha is estimated at €2 billion.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology
- **Notes**: Magnetic confinement via externally generated 3D helical fields. Stellarators are archetypal MFE devices — steady-state magnetic confinement with no plasma current.

### Confinement Concept
- **Value**: `Stellarator (QI)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; Stellaris paper DOI: 10.1016/j.fusengdes.2025.114868
- **Notes**: Quasi-isodynamic optimization — trapped particle orbits are well-confined via poloidally closed contours of the second adiabatic invariant. Same optimization approach as Wendelstein 7-X. Proxima's published design is "Stellaris." Volume-averaged plasma beta ~2.76%.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained
- **Notes**: Deuterium-Tritium fuel cycle confirmed. Stellaris includes WCLL tritium breeding blanket with TBR of 1.07. Peak fusion power 2.7 GW from D-T reactions.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: medium
- **Citation**: Inferred from stellarator physics and W7-X heritage; confirmed as universal stellarator heating method by Helios design (https://arxiv.org/html/2512.08027v1) which uses ECRH at 170 GHz
- **Notes**: Not explicitly specified for Stellaris in publicly available sources. ECRH is the universal stellarator heating method — W7-X uses ECRH exclusively (10 gyrotrons at 140 GHz). The Helios stellarator power plant design (Thea Energy) also uses ECRH at 170 GHz with ITER-spec gyrotrons. Stellarators lack plasma current, so ohmic heating is unavailable; NBI is possible but has never been the primary heating method for any QI stellarator design. The full Stellaris paper (paywalled) likely specifies the heating method. Confidence remains medium because Proxima has not directly confirmed this in any public source found.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: Inferred from WCLL blanket design (water-cooled, EUROFER97 <500°C); Helios comparison uses steam Rankine at 635°C
- **Notes**: WCLL blanket with water coolant and EUROFER97 at <500°C strongly implies steam Rankine cycle — the standard pathway for WCLL blankets in the EUROfusion DEMO program. Proxima has not explicitly stated the power conversion cycle. The analogous Helios stellarator design (Thea Energy) uses Rankine cycle with 635°C superheated steam at ~40% efficiency. Stellaris achieves ~1 GW net electrical from ~3.1 GW thermal, implying ~32% overall plant efficiency (thermal-to-net-electric), which is consistent with steam Rankine after accounting for recirculating power and auxiliary loads. A research paper on optimized stellarator power conversion (ScienceDirect) suggests combined Brayton-Rankine cycles could achieve >50%, but this is not the baseline for any current stellarator design. Value could be refined to `Thermal (steam)` if the full paper confirms Rankine.

### Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: https://www.proximafusion.com/technology; Stellaris paper (2.7 GW fusion power, ~1 GW electrical)
- **Notes**: Stellaris targets commercial power production with 2.7 GW peak fusion power and ~1 GW net electrical output. Alpha demo (2031) targets Q>1 ("net energy gain"). No specific Q value published for Stellaris commercial plant, but 2.7 GW fusion power from a compact device implies high Q (likely Q>>10) where alpha heating dominates — consistent with "Burning" classification. The Helios stellarator (comparable design) requires only 10 MW ECRH for startup and 1 MW in ignited phase, suggesting these stellarator designs target full ignition. Confidence medium because no explicit Q value or ignition target is stated for Stellaris.

### Magnet Type
- **Value**: `HTS (3D stellarator)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; https://www.prnewswire.com/news-releases/faraday-factory-japan-signed-an-agreement-to-deliver-superconductor-tape-for-the-demo-stellarator-magnet-of-proxima-fusion-302486210.html
- **Notes**: HTS magnets producing up to 20 T in modular high-field configuration. REBCO tape from Faraday Factory Japan. Complex 3D non-planar coils producing the helical magnetic field externally. Stellarator Model Coil (SMC) demo magnet targeted for 2027 to de-risk manufacturing. Coils developed with PSI & BNET. Proxima planning magnet factory with up to 1,000 jobs.

### Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained; https://binding.energy/stellarator-fusion-energy/
- **Notes**: Water-Cooled Lithium-Lead (WCLL) blanket with TBR of 1.07, same concept as EU DEMO WCLL. Proxima notes this is a "concept, not a complete engineering design" demonstrated as viable "without suggesting this is the optimal choice." Patent applied for an innovative liquid-metal breeding blanket. EUROFER97 structural steel, <500°C operating temperature. Adapted to complex stellarator geometry with neutronic simulations.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: Stellaris paper DOI: 10.1016/j.fusengdes.2025.114868; https://www.proximafusion.com/technology
- **Notes**: D-T fusion produces 14.1 MeV neutrons. WCLL blanket serves as both tritium breeder and neutron attenuator — lead provides neutron multiplication, water provides moderation. The Stellaris paper scope includes "first wall cooling, divertor considerations, blanket design, magnet quench safety, support structures, and remote maintenance solutions" — indicating comprehensive neutron management was analyzed. No separate shielding architecture described in public sources; blanket is the primary neutron management system. For comparison, the Helios stellarator uses a multi-layer shield (tungsten carbide + boron carbide + steel + borated water + borated HDPE) with minimum 1.2 m plasma-coil distance — Stellaris likely has a similar approach but specifics are in the paywalled paper. Confidence medium because the detailed shielding architecture is not in public sources.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; https://www.proximafusion.com/press-news/proxima-fusion-rwe-the-free-state-of-bavaria-and-max-planck-institute-for-plasma-physics-sign-agreement-to-build-the-worlds-first-commercial-fusion-power-plant-in-europe
- **Notes**: Stellarators are inherently steady-state — no plasma current means no need for current drive or pulsed inductive startup. Proxima explicitly describes "24/7 continuous operation" and "disruption-free design." The RWE MoU describes Stellaris as "designed to operate reliably and continuously." Alpha will be "the first stellarator to demonstrate net energy gain" in continuous operation mode.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: N/A — continuous steady-state operation
- **Notes**: Repetition rate is structurally inapplicable to steady-state concepts.

### Driver Technology
- **Value**: `3D HTS stellarator coils (REBCO, 20 T)`
- **Confidence**: high
- **Citation**: https://www.proximafusion.com/technology; https://binding.energy/stellarator-fusion-energy/
- **Notes**: The key technology bet is manufacturing complex 3D non-planar HTS coils from REBCO tape at up to 20 T. Stellarator coils are far more geometrically complex than tokamak D-shaped coils. AI-driven optimization for coil and magnetic field design. SMC demo in 2027 is critical de-risking milestone. Coils developed with PSI & BNET, REBCO tape from Faraday Factory Japan. Distinguishes Proxima from other stellarator companies: Type One Energy uses modular coils, Thea Energy uses planar arrays, Renaissance Fusion uses laser-patterned HTS film. Magnet factory planned with up to 1,000 jobs.

## Remaining Gaps

### Medium-confidence values (4 of 12 columns):

1. **Primary Heating** (medium): ECRH inferred from stellarator physics, W7-X heritage, and Helios comparison. Every QI stellarator design in existence uses ECRH as primary heating. However, Proxima has not explicitly confirmed this in any public source. The full Stellaris paper (paywalled, DOI: 10.1016/j.fusengdes.2025.114868) almost certainly specifies the heating method.

2. **Energy Capture** (medium): "Thermal (unspecified)" because WCLL blanket with water cooling strongly implies steam Rankine, and the comparable Helios stellarator confirms this pattern. However, combined Brayton-Rankine or sCO2 cycles are theoretically possible. The ~32% overall plant efficiency (1 GW net from 3.1 GW thermal) is consistent with steam Rankine after recirculating power deductions. Full Stellaris paper likely discusses the power conversion cycle.

3. **Plasma State** (medium): "Burning" inferred from 2.7 GW fusion power target and commercial power plant purpose. Alpha targets Q>1. Helios stellarator targets ignition (1 MW ECRH in ignited phase). No specific Q value published for Stellaris commercial plant.

4. **Neutron Management** (medium): "Integrated blanket/shield" inferred from WCLL blanket design and comprehensive neutronic simulations described in paper scope. Specific shielding layers and distances not available in public sources. Helios uses multi-layer shield for comparison.

### What would resolve these gaps:
- **Full Stellaris paper** (DOI: 10.1016/j.fusengdes.2025.114868) — this single source would likely resolve all 4 medium-confidence values. It covers heating, blanket, neutronics, and full power balance.
- **Proxima Fusion conference presentations** (APS-DPP, IAEA FEC)
- **Alpha demo detailed specifications** as they emerge

### Conflicts: None
All sources are consistent. The only nuance is that Proxima has stated the WCLL blanket is a concept demonstration, not necessarily the final choice — they have a patent for an innovative liquid-metal breeding blanket that may be different.

## Key Sources

1. [Proxima Fusion Technology Page](https://www.proximafusion.com/technology) — primary company technology overview
2. [Stellaris Paper](https://www.sciencedirect.com/science/article/pii/S0920379625000705) (DOI: 10.1016/j.fusengdes.2025.114868) — Fusion Engineering and Design, Vol. 214, May 2025 (paywalled, abstract only accessed)
3. [Stellaris Paper - KIT Repository](https://publikationen.bibliothek.kit.edu/1000179851) — alternate access point, abstract available
4. [Proxima Fusion Tritium Blog](https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained) — WCLL blanket details, TBR 1.07
5. [Binding Energy Analysis](https://binding.energy/stellarator-fusion-energy/) — WCLL details, EUROFER97, 20 T magnets, TBR 1.07
6. [Faraday Factory Japan PR](https://www.prnewswire.com/news-releases/faraday-factory-japan-signed-an-agreement-to-deliver-superconductor-tape-for-the-demo-stellarator-magnet-of-proxima-fusion-302486210.html) — HTS REBCO tape supply for SMC demo
7. [Stellaris Press Release](https://www.proximafusion.com/press-news/proxima-fusion-and-partners-publish-stellaris-fusion-power-plant-concept-to-bring-limitless-safe-clean-energy-to-the-grid) — announcement
8. [World Nuclear News](https://www.world-nuclear-news.org/articles/german-stellarator-fusion-design-concept-unveiled) — Stellaris coverage
9. [RWE/Bavaria/IPP MoU Press Release](https://www.proximafusion.com/press-news/proxima-fusion-rwe-the-free-state-of-bavaria-and-max-planck-institute-for-plasma-physics-sign-agreement-to-build-the-worlds-first-commercial-fusion-power-plant-in-europe) — Feb 2026 agreement
10. [ANS Nuclear Newswire - MoU Coverage](https://www.ans.org/news/2026-03-03/article-7810/proxima-fusion-signs-mou-with-bavaria-rwe-and-max-planck-ipp-to-build-german-stellarator-power-plant/) — Alpha €2B cost, timeline
11. [Proxima W7-X Blog](https://www.proximafusion.com/press-news/how-the-most-advanced-stellarator-in-the-world-set-the-stage-for-commercial-fusion) — W7-X heritage, island divertor, triple product records
12. [Helios Stellarator Design (ArXiv)](https://arxiv.org/html/2512.08027v1) — comparison QI stellarator: ECRH 170 GHz, steam Rankine, PbLi blanket
13. [Fusion Energy Insights Analysis](https://fusionenergyinsights.com/blog/post/fusion-energy-insights-examined-an-analysis-of-proxima-fusion-s-bold-plan-for-a-stellarator-power-plant) — independent analysis
14. [NEI Magazine](https://www.neimagazine.com/news/proxima-unveils-stellaris-fusion-plant-design/) — Stellaris coverage with technical details
15. [Wikipedia - Proxima Fusion](https://en.wikipedia.org/wiki/Proxima_Fusion) — overview
16. [NucNet - RWE/Bavaria MoU](https://www.nucnet.org/news/proxima-fusion-signs-mou-with-rwe-and-bavaria-to-develop-fusion-power-2-5-2026) — Gundremmingen site agreement

## Sources Consulted (Iter-02 specific)

### Fetched and yielded information:
- https://fusionenergyinsights.com/blog/post/fusion-energy-insights-examined-an-analysis-of-proxima-fusion-s-bold-plan-for-a-stellarator-power-plant
- https://publikationen.bibliothek.kit.edu/1000179851
- https://www.neimagazine.com/news/proxima-unveils-stellaris-fusion-plant-design/
- https://www.proximafusion.com/press-news/how-the-most-advanced-stellarator-in-the-world-set-the-stage-for-commercial-fusion
- https://www.ans.org/news/2026-03-03/article-7810/proxima-fusion-signs-mou-with-bavaria-rwe-and-max-planck-ipp-to-build-german-stellarator-power-plant/
- https://arxiv.org/html/2512.08027v1 (Helios stellarator comparison)
- https://binding.energy/stellarator-fusion-energy/

### Attempted but blocked/empty:
- https://www.sciencedirect.com/science/article/pii/S0920379625000705 (403 - paywalled)
- https://www.researchgate.net/publication/389324843 (403)
- https://climateinsider.com/2025/02/26/proxima-fusion-proposes-next-generation-stellarator-for-fusion-power-plants/ (403)
- https://en.wikipedia.org/wiki/Proxima_Fusion (403 on fetch)
- https://spectrum.ieee.org/stellarator (JS-rendered, no article body)
- https://www.eetimes.com/proxima-fusion-unveils-stellaris-a-breakthrough-in-fusion-power/ (timeout)
- https://insights.globalspec.com/article/23597/stellarator-designed-to-advance-fusion-power (403)
- https://www.enlit.world/library/proxima-fusion-publishes-pioneering-qi-stellarator-power-plant-concept (403)
- https://www.innovationnewsnetwork.com/proxima-fusion-unveils-breakthrough-concept-for-commercial-fusion-power-plant/55878/ (403)
- https://www.businesswire.com/news/home/20250226083304/en/ (timeout)

### Web searches performed:
1. "Proxima Fusion Stellaris stellarator ECRH heating power conversion 2025 2026"
2. "Proxima Fusion Stellaris paper Fusion Engineering Design 2025 stellarator power plant"
3. "Stellaris quasi-isodynamic stellarator ECRH fusion power GW heating system 2025"
4. "Proxima Fusion Stellaris 2.7 GW fusion power 1 GW electrical thermal cycle blanket shield details"
5. "arxiv Stellaris stellarator quasi-isodynamic HTS Proxima Fusion preprint 2024 2025"
6. "Proxima Fusion Stellaris thermal power / electrical output / net electric / power conversion / Rankine / steam cycle"
7. "Proxima Fusion stellarator ECRH / electron cyclotron / heating system / gyrotron"
8. "Proxima Fusion Stellaris 1 GW / 1 GWe / net electric / gross electric power plant specifications"
9. "Stellaris stellarator water-cooled / WCLL / lithium-lead steam / Rankine / power cycle"
10. "Proxima Fusion stellarator plasma beta / energy confinement / ISS04 / Q = / fusion gain / recirculating power"
11. "Proxima Fusion Stellaris Enlit RWE site Gundremmingen 2026 latest news update"
12. "Proxima Fusion Stellaris paper abstract 2.7 GW / 3.1 GW / peak fusion / thermal heating blanket shield"
13. "Proxima Fusion technology page Alpha stellarator demo specifications power 2031"
