Now let me write the full dossier.

---

## Research Findings: Large-Scale Stellarator (D-T) — Gauss Fusion

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — "high-field magnetic confinement fusion"
- **Notes**: Stellarator is a magnetic confinement concept by definition.

### Confinement Concept
- **Value**: `Stellarator (QI)`
- **Confidence**: high
- **Citation**: Multiple sources confirm GIGA is a quasi-isodynamic (QI) stellarator in the HELIAS lineage. [IPP event](https://www.ipp.mpg.de/events/40887/10021); search results confirming "Gauss Fusion intends to build the first-of-a-kind commercial fusion power plant based around a QI stellarator."
- **Notes**: The initial CSV described this as "Conventional (non-planar) coil design" which is accurate — the coils are non-planar modular coils (40 total, 5 shapes × 8). But the confinement concept is QI, not just generic "modular." The GIGA design directly descends from the HSR4/18 HELIAS reactor study (4 field periods, 18m major radius). Note: the schema lists `Stellarator (modular)` as a standard name — `Stellarator (QI)` is the correct classification since it captures the physics optimization, not just coil geometry. The coils happen to be non-planar modular coils (like W7-X), distinguishing Gauss from planar-coil approaches (Thea Energy) or high-field compact QI (Proxima Fusion).

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: [FusionXInvest profile](https://fusionxinvest.com/company-profile/4362/gauss-fusion/) — "Initial phase: Deuterium-Tritium (DT) operation"
- **Notes**: FusionXInvest also mentions a later D-D phase, but the primary commercial fuel cycle is D-T. The supply chain requirements (75 tonnes lithium, breeder blankets) confirm D-T as the baseline.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: medium
- **Citation**: Not directly confirmed by Gauss Fusion sources. Inferred from: (1) W7-X uses ECRH exclusively as primary heating; (2) HELIAS reactor studies assume ECRH; (3) ECRH is the universal stellarator heating method as noted in the schema.
- **Notes**: Gauss Fusion has not publicly specified their heating system in available sources. ECRH is the overwhelmingly likely choice given the W7-X/HELIAS heritage. W7-X currently uses 140 GHz gyrotrons with plans for 1.5 MW units. A 3 GW thermal plant would likely need 50-100+ MW of ECRH for startup, with much less during steady-state burn. The Helios stellarator study (a different concept) specifies 12 gyrotrons at 10 MW RF during startup, 1 MW during power production — similar order of magnitude expected for GIGA.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: Gauss Fusion CDR covers "heat extraction and cooling loops for power generation" and "power conversion for grid connection" ([Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/)). Supply chain mentions vacuum vessel steel, breeder blankets — classic thermal conversion infrastructure.
- **Notes**: The specific cycle (Rankine steam vs. sCO2 Brayton) is not publicly disclosed. HELIAS reactor studies have explored both He-cooled and DCLL blanket options, both feeding thermal cycles. At 3 GW thermal → 1 GW electric, the implied thermal efficiency is ~33%, consistent with a conventional steam Rankine cycle. A sCO2 cycle would achieve ~40%+ efficiency. The 33% figure suggests steam Rankine or a conservative assumption, but this is speculative.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: A 3 GW thermal stellarator with 1 GW electric output requires a high-Q burning plasma. Stellarators at power-plant scale are designed for ignition or near-ignition.
- **Notes**: The HELIAS reactor studies target ignited plasma (Q → ∞). At 3 GW fusion power, the alpha heating power (~600 MW) vastly exceeds any plausible external heating (~50-100 MW ECRH), confirming a burning plasma state.

### Magnet Type
- **Value**: `LTS+HTS`
- **Confidence**: high
- **Citation**: [MT29 CERN Indico abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — "GFG is developing both LTS and HTS options with a common cross-section (circular with a diameter of about 55mm) and current (100kA) that can be interchangeably used in magnet designs." Supply chain: "~800 tonnes LTS + 26M meters HTS superconductors" ([binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/)).
- **Notes**: This is a dual-track development strategy. The common conductor format (55mm circular, 100kA) allows either LTS or HTS to be used in the same coil design. The €9M BMBF grant funds demountable SC coils developed with KIT. The Tokamak Energy partnership (Oct 2025) is specifically for HTS magnet development. Original HELIAS HSR4/18 used NbTi at ~10T max; GIGA targets 12-13T max coil field, which likely requires at least Nb₃Sn (LTS) or HTS. The 40 non-planar modular coils at ~300 tonnes each are comparable to ITER TF magnets.

### Tritium Breeding
- **Value**: `Li blanket (unspecified)`
- **Confidence**: medium
- **Citation**: Supply chain mentions "~75 tonnes lithium inventory" and "breeder blankets" ([binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/)). Team includes dedicated "Tritium Fuel Cycle & Breeding Module" leads (Paul Staniec, Jacobo Zegri). CDR lists "closed tritium fuel cycle" as a key development challenge.
- **Notes**: The specific blanket type is not publicly disclosed. HELIAS reactor studies have explored two main options: (1) DCLL (Dual Coolant Lithium Lead / LiPb) studied extensively by CIEMAT, and (2) HCPB (Helium-Cooled Pebble Bed). The DCLL is considered more promising for the complex HELIAS geometry due to its liquid breeder and decoupled cooling circuits. Given Gauss Fusion's partnership with KIT (which leads EU blanket R&D) and the lithium inventory mention, a lithium-based blanket is confirmed, but whether it's LiPb, FLiBe, or solid ceramic is not disclosed. `LiPb blanket` would be a reasonable guess given HELIAS studies, but I'll use the more conservative `Li blanket (unspecified)`.

### Neutron Management
- **Value**: `Heavy shielding (14 MeV)`
- **Confidence**: high
- **Citation**: D-T fuel produces 14.1 MeV neutrons. First wall neutron load 1 MW/m² with 5-year blanket life indicates significant neutron damage management. CDR addresses materials "capable of withstanding extreme thermal and neutron loads." Supply chain includes tungsten, RAFM steel, beryllium — all standard neutron management materials.
- **Notes**: If the blanket type turns out to be DCLL (LiPb), then `Integrated blanket/shield` would be more appropriate since the liquid metal blanket serves dual purpose. With the current uncertainty on blanket type, `Heavy shielding (14 MeV)` is the safe classification. The 1 MW/m² first-wall neutron load is moderate (some concepts target 2+ MW/m²), enabling a 5-year blanket replacement cycle.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: [Gauss Fusion website](https://gauss-fusion.com/) — "steady-state operation"; stellarators are inherently steady-state. Multiple sources confirm: "intrinsic steady state capability."
- **Notes**: This is one of the key advantages of stellarators over tokamaks — no need for current drive, no disruptions. The CSV's "Continuous" operation mode maps directly to `Steady-state`.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: N/A — steady-state concept, no pulsed operation.
- **Notes**: Repetition rate is structurally inapplicable to a steady-state stellarator.

### Driver Technology
- **Value**: `Non-planar modular SC coils (LTS+HTS, 40 coils, 6T axis / 12-13T peak, demountable)`
- **Confidence**: high
- **Citation**: [MT29 abstract](https://indico.cern.ch/event/1431972/contributions/6419980/) — 40 coils, 5 shapes × 8, non-planar, conductor-in-plate concept, demountable joints (~250/coil, ~1 nΩ resistance), 100 kA conductor current, ~55mm diameter conductor.
- **Notes**: The distinguishing "hard technology bet" for Gauss Fusion is the combination of: (1) large-scale non-planar modular coils at ITER-comparable size (~300 tonnes each, 30-35m perimeter), (2) demountable joints enabling sector-based maintenance, (3) dual LTS/HTS conductor strategy with a common cross-section, and (4) conductor-in-plate construction avoiding traditional coil casings. This is distinct from Proxima Fusion (compact HTS QI) and Thea Energy (planar HTS coil arrays).

---

## Additional Metadata Columns

### Published Machine/Plant?
- **Value**: Yes — Conceptual Design Report (CDR) released 2025, 1000+ pages covering the GIGA power plant. Not yet at detailed engineering design.
- **Confidence**: high
- **Citation**: [World Nuclear News](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant); [Modern Power Systems](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/)

### Lab Experiments
- **Value**: Wendelstein 7-X (IPP Greifswald), LHD (NIFS Japan)
- **Confidence**: high
- **Citation**: W7-X is the direct physics basis for the HELIAS/QI concept. GIGA builds on W7-X validated physics. Gauss Fusion has collaboration agreements with IPP.
- **Notes**: W7-X has demonstrated good plasma confinement, reduced neoclassical transport consistent with QI optimization, and steady-state-relevant plasma scenarios. LHD in Japan is the other large operating stellarator providing complementary data.

---

## Remaining Gaps

1. **Primary Heating** (medium confidence): No Gauss Fusion source explicitly states ECRH. This is inferred from W7-X heritage and universal stellarator practice. A specific Gauss Fusion technical paper or CDR excerpt would raise confidence to high.

2. **Energy Capture** (medium confidence): Thermal conversion is confirmed but the specific cycle (steam Rankine vs. sCO2) is not disclosed. The ~33% implied efficiency (3 GWth → 1 GWe) hints at steam Rankine, but this could also reflect conservative plant assumptions. The CDR likely specifies this.

3. **Tritium Breeding** (medium confidence): Lithium-based blanket confirmed via supply chain data, but the specific blanket type (LiPb/DCLL, FLiBe, HCPB, etc.) is not publicly disclosed. HELIAS studies favor DCLL (LiPb), which would be the most likely choice. Access to the CDR or a Gauss Fusion blanket paper would resolve this.

4. **Neutron Management**: Classified as `Heavy shielding (14 MeV)` but could be `Integrated blanket/shield` if the blanket type turns out to be a liquid breeder serving dual purpose. This depends on the blanket type gap above.

5. **Magnet conductor specifics**: The LTS conductor type (NbTi vs. Nb₃Sn) is not explicitly stated. At 12-13T peak field, Nb₃Sn is more likely than NbTi (which maxes out around 9-10T). The HTS track is confirmed REBCO via the Tokamak Energy partnership.

## Sources Consulted

- [Gauss Fusion website](https://gauss-fusion.com/)
- [FusionXInvest company profile](https://fusionxinvest.com/company-profile/4362/gauss-fusion/)
- [Gauss Fusion Commercial Roadmap — binding.energy](https://binding.energy/gauss-fusion-commercial-roadmap/)
- [MT29 GIGA magnet system abstract — CERN Indico](https://indico.cern.ch/event/1431972/contributions/6419980/)
- [IPP Garching: Physics and engineering of GIGA](https://www.ipp.mpg.de/events/40887/10021)
- [Lazerson colloquium — U. Greifswald](https://physik.uni-greifswald.de/en/physics-colloquium/details/n/samuel-aaron-lazerson-gauss-fusion-the-physics-of-giga-a-gigawatt-class-stellarator-power-plant-for-europe-208307/)
- [World Nuclear News — GIGA blueprint](https://www.world-nuclear-news.org/articles/gauss-fusion-releases-blueprint-for-development-of-its-giga-fusion-plant)
- [Modern Power Systems — GIGA CDR](https://www.modernpowersystems.com/news/gauss-fusion-unveils-conceptual-design-for-giga-fusion-power-plant/)
- [Nuclear Engineering International — blueprint](https://www.neimagazine.com/news/german-start-up-unveils-fusion-blueprint/)
- [Interesting Engineering — Europe's first commercial fusion design](https://interestingengineering.com/energy/europe-commercial-fusion-plant-design)
- [Innovation News Network — CDR presentation](https://www.innovationnewsnetwork.com/gauss-fusion-presents-europes-first-full-design-for-a-commercial-fusion-power-plant/62378/)
- [Tokamak Energy HTS collaboration announcement](https://tokamakenergy.com/2025/10/07/tokamak-energy-signs-strategic-hts-collaboration-with-gauss-fusion/)
- [Bruker EAS press release](https://www.bruker.com/en/news-and-events/news/2023/european-gauss-fusion-initiative-seeks-to-use-magnetic-fusion.html)
- [Magnetics Magazine — magnetic containment](https://magneticsmag.com/magnetic-containment-of-fusion-energy-seen-as-key-to-breakthrough-of-the-century/)
- [ITER article — "Things are different now"](https://www.iter.org/node/20687/things-are-different-now)
- [Startbase — €9M BMBF funding](https://www.startbase.com/news/gauss-fusion-erhaelt-neun-millionen-euro-foerderung-von-bundesregierung/)
- [IPP — collaboration with fusion companies](https://www.ipp.mpg.de/5575721/zusammenarbeit)
- [KIT Forum Fusion Deutschland presentation (PDF)](https://www.filo.kit.edu/downloads/Forum%20FUSION%20Dtl/Event_FFD_081222/Presentationen/6-Gauss%20Fusion%20Initiative-Introduction%202.pdf)
- [Neil Mitchell IEEE CSC presentation (PDF, unreadable)](https://snf.ieeecsc.org/files/ieeecsc/slides/Mitchell%20presentation.pdf)
- [ResearchGate — HSR4/18 HELIAS reactor](https://www.researchgate.net/publication/27263728_The_Helias_reactor_HSR418)
- [CIEMAT — DCLL BB for HELIAS](https://www.sciencedirect.com/science/article/pii/S0360544223033649)
- [MDPI Energies — HELIAS DCLL neutronic assessments](https://www.mdpi.com/1996-1073/16/11/4430)
- [F4E collaboration agreement](https://fusionforenergy.europa.eu/news/f4e-and-gauss-fusion-sign-collaboration-agreement)
- [FIA 2024 report](https://sciencebusiness.net/sites/default/files/inline-files/FIA_annual%20report%202024.pdf) (Gauss listed as participant)
- [Stellarator Wikipedia](https://en.wikipedia.org/wiki/Stellarator) (background)
- [W7-X Wikipedia](https://en.wikipedia.org/wiki/Wendelstein_7-X) (background)
