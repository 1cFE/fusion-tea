# Large-Scale Stellarator (D-T)

**Company**: Gauss Fusion
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: medium

## Summary

Gauss Fusion is developing GIGA, a gigawatt-class quasi-isodynamic (QI) stellarator power plant descended from the HELIAS HSR4/18 reactor study and built on Wendelstein 7-X physics. The design uses 40 non-planar modular superconducting coils (5 shapes x 8) with a dual LTS/HTS conductor strategy (likely Nb3Sn + REBCO) and demountable joints, targeting 3 GW thermal / 1 GW electric output. As a stellarator, GIGA offers inherent steady-state operation and disruption-free plasma, avoiding the current-drive and disruption-mitigation challenges of tokamaks. A 1,000+ page Conceptual Design Report (CDR) was released in 2025 and validated by a 13-person expert panel chaired by Zohm.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — "high-field magnetic confinement fusion"
- **Notes**: Stellarator is a magnetic confinement concept by definition.

### Confinement Concept
- **Value**: Stellarator (QI)
- **Confidence**: high
- **Citation**: [IPP event](https://www.ipp.mpg.de/events/40887/10021); CDR describes "stellarator with a four period quasi isodynamic plasma" ([World Nuclear News](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant))
- **Notes**: The CDR explicitly states "four period quasi isodynamic plasma...supported by results from Wendelstein 7-X and advances in plasma modelling and stellarator optimisation." This is the HELIAS lineage (HSR4/18 = 4 field periods, 18m major radius). The coils are non-planar modular (like W7-X), distinguishing Gauss from planar-coil approaches (Thea Energy) or compact HTS QI (Proxima Fusion).

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: [FusionXInvest profile](https://fusionxinvest.com/company-profile/4362/gauss-fusion/) — "Initial phase: Deuterium-Tritium (DT) operation"; supply chain includes 75 tonnes lithium and breeder blankets ([binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/))
- **Notes**: FusionXInvest also mentions a later D-D phase, but the primary commercial fuel cycle is D-T.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: medium
- **Citation**: ECRH is "prime candidate for stellarator heating" per [IPP stellarator heating page](https://www.ipp.mpg.de/ippcms/eng/for/bereiche/e3/index); PROCESS systems code defaults to ECRH for stellarators ([UKAEA PROCESS docs](https://ukaea.github.io/PROCESS/fusion-devices/stellarator/)); W7-X uses 140 GHz ECRH exclusively.
- **Notes**: Gauss Fusion has not publicly specified their heating system. However, ECRH is the universal stellarator heating method — no stellarator power plant study (HELIAS, HSR, or otherwise) has ever baselined anything else as primary heating. At 3 GW thermal with alpha-dominated heating, external ECRH would be needed primarily for startup and profile control (~50-100 MW range). Confidence remains medium because no Gauss-specific source confirms this.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: CDR covers "heat extraction and cooling loops for power generation" and "power conversion for grid connection" ([Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/)). 3 GW thermal to 1 GW electric implies ~33% thermal efficiency.
- **Notes**: The ~33% efficiency is consistent with steam Rankine cycle. HELIAS blanket studies have explored both He-cooled (HCPB, which feeds a He/steam power cycle) and liquid metal cooled (DCLL, which could feed a higher-efficiency cycle). Without knowing the blanket type, the power conversion cycle remains uncertain. The CDR almost certainly specifies this but is behind a download gate.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: 3 GW fusion power with ~600 MW in alpha particles vastly exceeds any plausible external heating (~50-100 MW ECRH). HELIAS reactor studies target ignition (Q -> infinity).
- **Notes**: A 3 GW thermal stellarator is deeply in the burning plasma regime.

### Magnet Type
- **Value**: LTS+HTS
- **Confidence**: high
- **Citation**: [MT29 abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — dual LTS/HTS development, common 55mm/100kA conductor format; [Modern Power Systems partnerships](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/) — ENEA for HTS cables/joints, ICAS for LTS cables + HTS industrial processes; [Tokamak Energy HTS collaboration](https://tokamakenergy.com/2025/10/07/tokamak-energy-signs-strategic-hts-collaboration-with-gauss-fusion/); [F4E agreement](https://fusionforenergy.europa.eu/news/f4e-and-gauss-fusion-sign-collaboration-agreement) covers "dismountable superconducting magnets."
- **Notes**: The LTS conductor is very likely **Nb3Sn** (not NbTi). The predecessor HSR4/18 used NbTi at 10T peak field, but GIGA targets 12-13T peak field, which is beyond practical NbTi limits. HELIAS studies confirm that above ~10T, "a switch from NbTi to Nb3Sn has been implemented." The HTS track is confirmed REBCO via Tokamak Energy and ENEA partnerships. The common conductor format (55mm diameter, 100kA) allows either LTS or HTS in the same coil geometry — a hedge strategy. 40 non-planar modular coils at ~300 tonnes each, comparable to ITER TF magnets.

### Tritium Breeding
- **Value**: Li blanket (unspecified)
- **Confidence**: medium
- **Citation**: KIT + FZJ + IDOM collaboration "finalising the industrial design of the Tritium Breeding Blanket" ([Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/)); Alsymex contracted for TBB prototype fabrication; supply chain includes 75 tonnes lithium ([binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/)); [F4E collaboration](https://fusionforenergy.europa.eu/news/f4e-and-gauss-fusion-sign-collaboration-agreement) covers tritium breeding.
- **Notes**: HELIAS studies have evaluated both **HCPB** (He-Cooled Pebble Bed, Li4SiO4 breeder, 26cm, TBR 1.15) and **DCLL** (Dual Coolant Lithium Lead, PbLi self-cooled, 46cm) for the HELIAS geometry. KIT is the European lead for both HCPB and DCLL development. The Alsymex fabrication contract for "prototype sub-assemblies" suggests the design has progressed to a specific blanket concept, but the type remains undisclosed publicly. Given that the CDR has been reviewed and partnerships are in fabrication-readiness phase, Gauss Fusion has clearly made an internal decision — it's just not public.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: high
- **Citation**: D-T fuel produces 14.1 MeV neutrons. First wall neutron load 1 MW/m² with 5-year blanket life. Supply chain includes tungsten, RAFM steel, beryllium.
- **Notes**: If the blanket turns out to be DCLL (LiPb), reclassification to `Integrated blanket/shield` might be appropriate since liquid metal blankets serve dual purpose. With HCPB, the blanket and shield are more distinct. Either way, the fundamental challenge is 14 MeV neutron management. Current classification is correct for all blanket options.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — "steady-state operation"; CDR describes "intrinsic steady state capability" ([NEI Magazine](https://www.neimagazine.com/news/german-start-up-unveils-fusion-blueprint/)); stellarators are inherently steady-state.
- **Notes**: Key advantage of stellarators over tokamaks — no need for current drive, no disruptions.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: N/A — steady-state concept, no pulsed operation.
- **Notes**: Repetition rate is structurally inapplicable to a steady-state stellarator.

### Driver Technology
- **Value**: Non-planar modular SC coils (LTS+HTS, 40 coils, 6T axis / 12-13T peak, demountable)
- **Confidence**: high
- **Citation**: [MT29 abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — 40 coils (5 shapes x 8), conductor-in-plate design, ~250 demountable joints per coil at ~1 nOhm; partnerships with ENEA, ICAS, Tokamak Energy for conductor development.
- **Notes**: LTS track likely Nb3Sn (12-13T exceeds NbTi capability). The "conductor-in-plate" construction is a key innovation — avoids traditional coil casings. Demountable joints at ~1 nOhm enable sector-based maintenance, critical for the complex stellarator geometry. Each coil is ~300 tonnes with ~30-35m perimeter, comparable to ITER TF magnets. Distinct from Proxima Fusion (compact HTS QI) and Thea Energy (planar HTS coil arrays).

## Remaining Gaps

1. **Primary Heating** (medium confidence): Still no Gauss Fusion-specific source confirming ECRH. This is extremely likely based on all stellarator precedent and HELIAS heritage, but remains inference. **To resolve**: Access the CDR executive summary (behind download gate at gauss-fusion.com/cdr-executive-summary), or find a Gauss Fusion conference presentation specifying heating.

2. **Energy Capture** (medium confidence): Thermal conversion confirmed but specific cycle not disclosed. The blanket type determines the power cycle — HCPB would suggest He/steam, DCLL could enable higher-efficiency options. **To resolve**: CDR access or technical publication.

3. **Tritium Breeding** (medium confidence): Lithium-based blanket confirmed with active partnerships (KIT, FZJ, IDOM, Alsymex) and prototype fabrication underway. Both HCPB and DCLL have been studied for HELIAS geometry. The specific choice is not public. **To resolve**: CDR access, or a KIT/FZJ publication specific to the Gauss Fusion TBB design.

4. **LTS conductor type**: Very likely Nb3Sn based on 12-13T peak field requirement (exceeds NbTi limits), but not explicitly stated by Gauss Fusion. ICAS is manufacturing LTS cables — their capabilities include both NbTi and Nb3Sn.

5. **Neutron Management classification**: Could shift to `Integrated blanket/shield` if the blanket is DCLL (liquid metal serves dual purpose). Depends on gap #3.

All three medium-confidence gaps (Primary Heating, Energy Capture, Tritium Breeding) are likely resolvable only through CDR access or Gauss Fusion technical publications. Public summaries have been thoroughly mined across two iterations. A third iteration is unlikely to yield new information unless new publications appear or the CDR becomes freely accessible.

## Key Sources

1. [MT29 GIGA magnet system abstract — CERN Indico](https://indico.cern.ch/event/1431972/contributions/6419980/) — Most detailed technical source on magnet design
2. [Gauss Fusion Commercial Roadmap — binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/) — Supply chain, timeline, cost targets
3. [Modern Power Systems — GIGA CDR](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/) — CDR overview and plant parameters
4. [Modern Power Systems — European partnerships](https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/) — KIT/FZJ/IDOM for TBB, ENEA/ICAS for conductors, Alsymex for fabrication
5. [F4E-Gauss Fusion collaboration](https://fusionforenergy.europa.eu/news/f4e-and-gauss-fusion-sign-collaboration-agreement) — Tritium breeding, dismountable SC magnets, materials
6. [FusionXInvest company profile](https://fusionxinvest.com/company-profile/4362/gauss-fusion/) — Fuel, funding, team
7. [IPP — Physics and engineering of GIGA](https://www.ipp.mpg.de/events/40887/10021) — Technical seminar
8. [IPP — Stellarator heating](https://www.ipp.mpg.de/ippcms/eng/for/bereiche/e3/index) — ECRH as prime stellarator heating candidate
9. [UKAEA PROCESS stellarator model](https://ukaea.github.io/PROCESS/fusion-devices/stellarator/) — Systems code defaults for stellarators
10. [Gauss Fusion website](https://gauss-fusion.com/) — Official overview
11. [World Nuclear News — GIGA blueprint](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant) — CDR announcement
12. [NEI Magazine — fusion blueprint](https://www.neimagazine.com/news/german-start-up-unveils-fusion-blueprint/) — CDR strategic overview
13. [Tokamak Energy HTS collaboration](https://tokamakenergy.com/2025/10/07/tokamak-energy-signs-strategic-hts-collaboration-with-gauss-fusion/) — HTS magnet partnership
14. [Startbase — Expert panel review](https://www.startbase.com/news/expertengremium-bestaetigt-designkonzept-fuer-fusionskraftwerk-von-gauss-fusion/) — 13-person panel confirmation of CDR
15. [ResearchGate — HSR4/18 HELIAS reactor](https://www.researchgate.net/publication/27263728_The_Helias_reactor_HSR418) — Predecessor design study
16. [CIEMAT — DCLL BB for HELIAS](https://www.sciencedirect.com/science/article/pii/S0360544223033649) — DCLL blanket option for HELIAS geometry
17. [Bongiovi 2022 — HCPB for HELIAS 5-B](https://onlinelibrary.wiley.com/doi/full/10.1002/er.7343) — HCPB blanket option for HELIAS geometry
