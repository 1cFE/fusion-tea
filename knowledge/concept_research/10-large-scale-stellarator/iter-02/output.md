Now here are my findings for all columns:

---

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — stellarator is magnetic confinement by definition
- **Notes**: No change from previous iteration. Confirmed.

### Confinement Concept
- **Value**: Stellarator (QI)
- **Confidence**: high
- **Citation**: [IPP seminar](https://www.ipp.mpg.de/events/40887/10021); CDR describes "stellarator with a four period quasi isodynamic plasma" ([World Nuclear News](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant))
- **Notes**: The CDR description explicitly states "four period quasi isodynamic plasma...supported by results from Wendelstein 7-X and advances in plasma modelling and stellarator optimisation." This is the HELIAS lineage (HSR4/18 = 4 field periods, 18m major radius). The coils are non-planar modular (like W7-X), not planar or helical.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: [FusionXInvest](https://fusionxinvest.com/company-profile/4362/gauss-fusion/) — "Initial phase: Deuterium-Tritium (DT) operation"; supply chain includes 75 tonnes lithium and breeder blankets ([binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/))
- **Notes**: No change. D-T is the primary commercial fuel cycle. FusionXInvest mentions a later D-D phase but this is aspirational.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: medium
- **Citation**: ECRH is "prime candidate for stellarator heating" per [IPP stellarator heating page](https://www.ipp.mpg.de/ippcms/eng/for/bereiche/e3/index); PROCESS systems code defaults to ECRH for stellarators ([UKAEA PROCESS docs](https://ukaea.github.io/PROCESS/fusion-devices/stellarator/)); W7-X uses 140 GHz ECRH exclusively
- **Notes**: Gauss Fusion has still not publicly specified their heating system. However, ECRH is the universal stellarator heating method — no stellarator power plant study (HELIAS, HSR, or otherwise) has ever baselined anything else as primary heating. The PROCESS stellarator code offers ECRH, LH, and NBI as options with ECRH as default. At 3 GW thermal with alpha-dominated heating, external ECRH would be needed primarily for startup and profile control (~50-100 MW range). Confidence remains medium because no Gauss-specific source confirms this; raising to high would require CDR access or a Gauss Fusion technical publication.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: CDR covers "heat extraction and cooling loops for power generation" and "power conversion for grid connection" ([Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/)); 3 GW thermal → 1 GW electric implies ~33% thermal efficiency
- **Notes**: The ~33% efficiency is consistent with steam Rankine cycle. HELIAS blanket studies have explored both He-cooled (HCPB, which feeds a He/steam power cycle) and liquid metal cooled (DCLL, which could feed a higher-efficiency cycle). Without knowing the blanket type, the power conversion cycle remains uncertain. The CDR almost certainly specifies this, but it's behind a download gate.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: 3 GW fusion power with ~600 MW in alpha particles vastly exceeds any plausible external heating (~50-100 MW ECRH). HELIAS reactor studies target ignition (Q → ∞).
- **Notes**: No change. A 3 GW thermal stellarator is deeply in the burning plasma regime.

### Magnet Type
- **Value**: LTS+HTS
- **Confidence**: high
- **Citation**: [MT29 abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — dual LTS/HTS development, common 55mm/100kA conductor format; [Modern Power Systems partnerships](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/) — ENEA for HTS cables/joints, ICAS for LTS cables + HTS industrial processes; [Tokamak Energy HTS collaboration](https://tokamakenergy.com/2025/10/07/tokamak-energy-signs-strategic-hts-collaboration-with-gauss-fusion/); F4E agreement covers "dismountable superconducting magnets"
- **Notes**: New detail from this iteration: The LTS conductor is very likely **Nb3Sn** (not NbTi). The predecessor HSR4/18 used NbTi at 10T peak field, but GIGA targets 12-13T peak field, which is beyond practical NbTi limits. Search results confirm that above ~10T, "a switch from NbTi to Nb3Sn has been implemented" in HELIAS studies. The HTS track is confirmed REBCO via Tokamak Energy and ENEA partnerships. The common conductor format (55mm diameter, 100kA) allows either LTS or HTS to be used in the same coil geometry — a hedge strategy.

### Tritium Breeding
- **Value**: Li blanket (unspecified)
- **Confidence**: medium
- **Citation**: KIT + FZJ + IDOM collaboration "finalising the industrial design of the Tritium Breeding Blanket" ([Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/)); Alsymex contracted for TBB prototype fabrication; supply chain includes 75 tonnes lithium; F4E collaboration covers tritium breeding
- **Notes**: This iteration adds important context but doesn't resolve the specific blanket type. HELIAS studies have evaluated both **HCPB** (He-Cooled Pebble Bed, Li4SiO4 breeder, 26cm, TBR 1.15) and **DCLL** (Dual Coolant Lithium Lead, PbLi self-cooled, 46cm) for the HELIAS geometry. KIT is the European lead for both HCPB and DCLL development. The Alsymex fabrication contract for "prototype sub-assemblies" suggests the design has progressed to a specific blanket concept, but the type remains undisclosed publicly. Given that the CDR has been reviewed and partnerships are in fabrication-readiness phase, Gauss Fusion has clearly made an internal decision — it's just not public.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: high
- **Citation**: D-T fuel produces 14.1 MeV neutrons; first wall neutron load 1 MW/m² with 5-year blanket life; supply chain includes tungsten, RAFM steel, beryllium
- **Notes**: If the blanket turns out to be DCLL (LiPb), reclassification to `Integrated blanket/shield` might be appropriate since liquid metal blankets serve dual purpose. With HCPB, the blanket and shield are more distinct. Either way, the fundamental challenge is 14 MeV neutron management. Current classification is correct for all blanket options.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — "steady-state operation"; CDR describes "intrinsic steady state capability"; stellarators are inherently steady-state ([NEI Magazine](https://www.neimagazine.com/news/german-start-up-unveils-fusion-blueprint/))
- **Notes**: No change. This is the defining advantage of the stellarator approach.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: N/A — steady-state concept, no pulsed operation
- **Notes**: Structurally inapplicable to a steady-state stellarator.

### Driver Technology
- **Value**: Non-planar modular SC coils (LTS+HTS, 40 coils, 6T axis / 12-13T peak, demountable)
- **Confidence**: high
- **Citation**: [MT29 abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — 40 coils (5 shapes × 8), conductor-in-plate design, ~250 demountable joints per coil at ~1 nΩ; partnerships with ENEA, ICAS, Tokamak Energy for conductor development
- **Notes**: Updated detail: LTS track likely Nb3Sn (12-13T exceeds NbTi capability). The "conductor-in-plate" construction is a key innovation — avoids traditional coil casings. Demountable joints at ~1 nΩ enable sector-based maintenance, which is critical for the complex stellarator geometry. Each coil is ~300 tonnes with ~30-35m perimeter, comparable to ITER TF magnets.

---

## Remaining Gaps

1. **Primary Heating** (medium confidence): Still no Gauss Fusion-specific source confirming ECRH. This is extremely likely based on all stellarator precedent and HELIAS heritage, but remains inference. **To resolve**: Access the CDR executive summary (behind download gate at gauss-fusion.com/cdr-executive-summary), or find a Gauss Fusion conference presentation specifying heating.

2. **Energy Capture** (medium confidence): Thermal conversion confirmed but specific cycle not disclosed. The blanket type determines the power cycle — HCPB would suggest He/steam, DCLL could enable higher-efficiency options. **To resolve**: CDR access or technical publication.

3. **Tritium Breeding** (medium confidence): Lithium-based blanket confirmed with active partnerships (KIT, FZJ, IDOM, Alsymex) and prototype fabrication underway. Both HCPB and DCLL have been studied for HELIAS geometry. The specific choice is not public. **To resolve**: CDR access, or a KIT/FZJ publication specific to the Gauss Fusion TBB design.

4. **LTS conductor type**: Very likely Nb3Sn based on 12-13T peak field requirement (exceeds NbTi limits), but not explicitly stated by Gauss Fusion. ICAS is manufacturing LTS cables — their capabilities include both NbTi and Nb3Sn.

5. **Neutron Management classification**: Could shift to `Integrated blanket/shield` if the blanket is DCLL (liquid metal serves dual purpose). Depends on gap #3.

## Sources Consulted

### Sources with useful technical content
1. [Gauss Fusion CDR executive summary landing page](https://gauss-fusion.com/cdr-executive-summary) — gated, no content accessible
2. [World Nuclear News — GIGA CDR](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant) — CDR overview, plant parameters (3 GW thermal, 1 GW electric, 18m major radius, 6T axis, 12-13T peak)
3. [Modern Power Systems — European partnerships](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/) — KIT/FZJ/IDOM for TBB, ENEA/ICAS for conductors, Alsymex for TBB fabrication
4. [F4E-Gauss Fusion collaboration](https://fusionforenergy.europa.eu/news/f4e-and-gauss-fusion-sign-collaboration-agreement) — Tritium breeding, dismountable SC magnets, materials, nuclear analysis
5. [Startbase — Expert panel review](https://www.startbase.com/news/expertengremium-bestaetigt-designkonzept-fuer-fusionskraftwerk-von-gauss-fusion/) — 13-person panel chaired by Zohm confirmed CDR
6. [UKAEA PROCESS stellarator model](https://ukaea.github.io/PROCESS/fusion-devices/stellarator/) — ECRH as default stellarator heating, blanket options (KIT HCPB)
7. [IPP stellarator heating page](https://www.ipp.mpg.de/ippcms/eng/for/bereiche/e3/index) — ECRH as prime candidate for stellarator heating
8. [ResearchGate — HSR4/18](https://www.researchgate.net/publication/27263728_The_Helias_reactor_HSR418) — NbTi at 10T, 40 coils, 18m major radius (GIGA predecessor)
9. [CIEMAT — DCLL for HELIAS](https://www.sciencedirect.com/science/article/pii/S0360544223033649) — DCLL blanket option, 46cm thickness, TBR at design limit
10. [Bongiovì 2022 — HCPB for HELIAS 5-B](https://onlinelibrary.wiley.com/doi/full/10.1002/er.7343) — HCPB blanket option, 26cm thickness, TBR 1.15
11. [binding.energy — Commercial roadmap](https://binding.energy/gauss-fusion-commercial-roadmap/) — Supply chain: 800t LTS + 26M m HTS, 75t lithium, timeline
12. [MT29 abstract — GIGA magnet system](https://indico.cern.ch/event/1431972/contributions/6419980/) — 40 coils, 5 shapes × 8, 55mm conductor, 100kA, demountable joints
13. [Gauss Fusion site mapping study](https://www.enlit.world/library/gauss-delivers-landmark-site-map-for-europes-first-fusion-plant) — 150 clusters, 900 sites across Europe

### Sources checked but yielded no new technical detail
14. [NEI Magazine — fusion blueprint](https://www.neimagazine.com/news/german-start-up-unveils-fusion-blueprint/) — Strategic only
15. [Innovation News Network — CDR presentation](https://www.innovationnewsnetwork.com/gauss-fusion-presents-europes-first-full-design-for-a-commercial-fusion-power-plant/62378/) — Strategic only
16. [EnerTherm Engineering — CDR](https://enertherm-engineering.com/europes-first-full-design-for-commercial-fusion-power-plant-unveiled-by-gauss-fusion/) — Strategic only
17. [Energy Curated — GIGA design](https://energycurated.com/conventional-fuels/gauss-unveils-europes-first-fusion-power-plant-design/) — Strategic only, incorrectly mentions "laser-based fusion"
18. Gauss Fusion expert panel press release PDF — binary, unreadable via WebFetch
19. Gauss Fusion partnerships press release PDF — binary, unreadable via WebFetch
20. Warmer 2024 paper (Fusion Eng. Design 202) — paywalled at ScienceDirect and iris.unipa.it
