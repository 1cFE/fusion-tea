---
ID: 10-large-scale-stellarator
Concept: Large-Scale Stellarator
Company: Gauss Fusion
Status: draft
Created: 2026-04-06
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Large-Scale Stellarator (Gauss Fusion GIGA)

**Concept**: Large-Scale Stellarator (D-T, quasi-isodynamic)
**Company**: Gauss Fusion GmbH (Munich, Germany)
**Reference Design**: GIGA — derived from HELIAS HSR4/18 reactor study; W7-X physics heritage
**Date**: 2026-04-06

---

## Section 1: Availability of Data

**Rating: Moderate**

Gauss Fusion occupies an unusual position among fusion startups: more transparent than most (a 1,000-page CDR was released in 2025 and reviewed by a 13-person independent expert panel), but the CDR itself is not freely accessible. The concept benefits from a deep scientific heritage in the HELIAS program at IPP Garching — decades of published reactor studies that substitute for much of what is proprietary at the company level. For TEA purposes, HELIAS literature provides the physics and engineering foundation, while Gauss-specific disclosures provide machine parameters and partnership context.

**Scientific Literature (Rich)**
The HELIAS concept has been studied since the 1990s through the HSR5/22 and HSR4/18 reactor studies, both published in open literature. These provide plasma parameters, coil geometry, blanket options, and component mass estimates that are directly applicable to GIGA, which is explicitly derived from HSR4/18 (4 field periods, 18 m major radius). The helias-reactor-context.md source is a comprehensive synthesis of these studies and provides the most complete parameter set available for LCOE modeling.

> "The reduction from 5 to 4 field periods...will also reduce the cost of the Helias reactor — specifically, HSR4/18 may lead to a 20% cost reduction of the reactor core compared to HSR5/22."
> — helias-reactor-context.md, §Conclusions

**Blanket Studies (Moderate)**
Two independent blanket options have been studied for HELIAS geometry: the HCPB (He-Cooled Pebble Bed) and the DCLL (Dual Coolant Liquid Lead) configurations. The helias-blanket-studies.md source provides a detailed structural mechanics and neutronics assessment of the HCPB option for the HELIAS 5-B geometry, including TBR estimates, segment counts, material choices, and failure modes. This is peer-reviewed literature and provides the most complete blanket engineering picture in the public domain.

> "A promising TBR value (1.3863) has been calculated for this configuration, using a neutronic model characterized by idealistic design features (no gaps in between blanket segments and big breeding zone's radial thickness)."
> — helias-blanket-studies.md, §2 "THE BREEDING BLANKET OF THE HELIAS 5-B REACTOR"

**Gauss Fusion Disclosures (Moderate)**
Machine parameters (3 GWth / 1 GWe, plasma dimensions, coil count), supply chain volumes, and partnership details are publicly stated across the CDR announcement, press materials, and conference abstracts. The MT29 (2024) abstract on the GIGA magnet system is the most technically detailed single source: it discloses the conductor format (55 mm diameter, 100 kA), joint count (~250 per coil), joint resistance target (~1 nΩ), coil geometry (conductor-in-plate design), and the dual LTS/HTS development strategy [gauss-fusion-technical-summary.md, §Magnet System].

**Independent Validation (Limited)**
The 13-member expert panel (chaired by Sibylle Günter, formerly IPP director) validated the CDR but its detailed review is not public. Brown (2018, IEEE TPS) provides the most useful independent comparative cost analysis across stellarator, standard tokamak, and spherical tokamak configurations, but is not GIGA-specific [referenced in dossier.md §Key Sources].

**Key Data Gaps**
1. CDR cost data — behind a download gate; cost structure by subsystem unpublished
2. Blanket type selection (HCPB vs. DCLL) — internal decision made, not disclosed
3. Power conversion cycle — undisclosed; depends on blanket type
4. NOAK cost projections — FOAK estimate only (€15–18B); no learning rate or fleet assumptions published
5. Capacity factor target — not stated in any public source

---

## Section 2: Challenges in Capturing System Function

Challenges are ranked by LCOE impact. The large-scale stellarator has a distinctive challenge profile: the steady-state advantage is real and TEA-favorable, but the very large machine scale and 3D geometry complexity impose capital cost and blanket engineering penalties that dominate the LCOE.

**1. FOAK Capital Cost: €15,000–18,000/kWe (Impact: Critical)**

The stated first-of-a-kind cost range of €15–18B for 1 GWe output [gauss-fusion-technical-summary.md, §Funding] implies a FOAK specific capital cost of ~€15,000–18,000/kWe. At a fixed charge rate of 15% and 80% capacity factor, capital cost alone drives the LCOE above €0.30/kWh — roughly 5–10× the competitive power target. NOAK cost reduction via fleet learning is essential, but no projection is published. Analogues from large LTS superconducting projects (ITER: ~€20B, 500 MWth, no electricity output) suggest these cost ranges are credible for a first-of-kind machine but leave unclear how far serial production and supply chain development can reduce per-unit costs. This is the single most important modeling gap — and it must be captured as a sensitivity parameter, not a point estimate. The model should sweep `noak_fraction` over 0.40–0.70 (NOAK as a fraction of FOAK), with the FOAK cost as the reference point. Key assumption: "NOAK may be 40–60% of FOAK" (a factor-of-2 uncertainty range) — see H1 in Key Hypotheses below.

> "The GIGA fusion plant has an estimated cost of €15–18 billion for its first-of-a-kind commercial reactor."
> — gauss-fusion-technical-summary.md, §Funding

**2. Blanket Type Uncertainty: Power Cycle and TBR Unknown (Impact: High)**

Gauss Fusion has not disclosed whether GIGA uses an HCPB (He-Cooled Pebble Bed) or DCLL (Dual Coolant Liquid Lead) blanket. Both options have been studied for the HELIAS geometry. This gap is not trivially bridgeable: the two blanket types differ fundamentally in coolant temperature (~450°C He for HCPB vs. ~600°C PbLi outlet for advanced DCLL), which propagates directly into power conversion cycle choice (steam Rankine vs. potentially sCO2 Brayton) and net thermal efficiency (35% vs. potentially 40%+). The 10-year LCOE gap between a 33% and 40% conversion efficiency plant is 20–25% of total system cost. The TBR margin differs similarly: HCPB achieves TBR~1.15 with the HELIAS geometry at realistic design [Bongiovi 2022, via dossier.md §Tritium Breeding]; DCLL can achieve higher TBR via LiPb self-shielding. The blanket type is the single greatest source of downstream LCOE uncertainty at the subsystem level.

**3. Blanket Geometry Complexity: 3D Segment Diversity (Impact: High)**

The HELIAS/GIGA blanket must conform to a complex, three-dimensionally varying wall geometry. Where a conventional tokamak requires essentially two blanket segment shapes (inboard and outboard), the HELIAS 5-B design requires 80 segments per blanket sector (16 rings × 5 shapes), with mandatory poloidal and toroidal gaps of 20 mm between segments [helias-blanket-studies.md, §2]. These gaps reduce coverage and lower the effective TBR below the idealized calculation. Structurally, the bean-shaped blanket rings create regions of high mechanical stress under accident loads — one of the five segment types (Segment 5) was found to exceed the RCC-MRx structural criterion under postulated accident loads in the published HCPB study [helias-blanket-studies.md, §6]. The maintenance scheme for the HELIAS blanket is explicitly undefined at the time of the published study. This geometry complexity translates into: higher blanket fabrication cost (many unique segment types), longer replacement downtime (complex remote manipulation in 3D space), and uncertain TBR margins. No analogue in the tokamak cost literature directly addresses this cost driver.

A key dimension of this challenge — specific to QI non-planar coil designs — is that blanket performance optimization is not separable from magnet protection in regions of minimum plasma-coil clearance. The ParaStell scoping study (Moreno et al., 2024) on a comparable quasi-isodynamic geometry (WISTELL-D, 10.1 m major radius) identified this explicitly: in tight-spacing regions with only 30 cm available between back wall and coil face, increasing the total blanket build thickness does not improve local magnet shielding, because the space in those regions is fixed by the coil geometry [frontiersin-journals-nuclear-engineering-articles-10-3389.md, §Discussion]. The only way to increase local shielding in those regions is to reduce the breeder fraction (giving more space to the HTS shield), which directly trades TBR margin for magnet protection. This constraint does not arise in tokamaks or in QA planar-coil stellarators (Helios) where coil geometry is more uniform — it is a structural design risk specific to QI non-planar architectures such as GIGA.

> "At the current stage, no attachment system has been developed...the BB segments are assumed as integral to the VV."
> — helias-blanket-studies.md, §2 "THE BREEDING BLANKET OF THE HELIAS 5-B REACTOR"

**4. Scale Extrapolation: 18 m Major Radius (Impact: High)**

GIGA targets 18 m major radius — three times the major radius of ITER (6.2 m) and more than three times W7-X (5.5 m). The HELIAS coil system alone involves 40 non-planar modular coils, each estimated at ~300 tonnes and ~30–35 m perimeter, with supply requirements of ~35,000 tonnes total superconducting coil mass and ~10,000 tonnes of vacuum vessel steel [gauss-fusion-technical-summary.md, §Supply Chain Requirements]. Construction at this scale involves challenges in factory capacity (module fabrication), shipping logistics (component dimensions and weight exceed highway and rail limits), and on-site assembly (tolerances for complex 3D coils at 30–35 m scale). W7-X provides the manufacturing template for non-planar modular coils at 5.5 m scale; GIGA's 18 m scale is a factor-of-3 extrapolation in a dimension where tolerances compound nonlinearly. No engineering study of GIGA-scale assembly logistics has been published.

**Note**: This scale-extrapolation challenge is specific to GIGA's quasi-isodynamic (QI) non-planar modular coil architecture. The Helios/Thea Energy quasi-axisymmetric (QA) stellarator design achieves a commercial reactor at 8 m major radius using planar coils — half GIGA's scale and without the non-planar coil manufacturing challenge. GIGA's scale is a consequence of the QI physics approach, not an intrinsic stellarator requirement.

**5. Conductor Technology Uncertainty: LTS vs. HTS Cost Range (Impact: Moderate)**

Gauss Fusion is pursuing dual development tracks: LTS (likely Nb3Sn, capable of the 12–13 T peak field required) and HTS (REBCO, higher field ceiling but ~3–5× higher conductor cost per kA-m at current prices). The common 55 mm / 100 kA conductor format allows either conductor in the same coil geometry — a deliberate hedge strategy [gauss-fusion-technical-summary.md, §Magnet System]. The supply requirement of ~26 million meters of HTS superconductor [gauss-fusion-technical-summary.md, §Supply Chain Requirements] is larger than global REBCO production capacity by more than an order of magnitude, making the HTS track contingent on massive supply chain scale-up. The LTS (Nb3Sn) track has lower conductor cost but requires 4 K cryogenics, higher cryogenic power load, and has a less favorable long-term cost trajectory. The choice between tracks — or the mix — will determine magnet system costs and is not yet decided.

**6. Steady-State Advantage: Quantifying the Capacity Factor Benefit (Impact: Moderate)**

Stellarators are inherently steady-state and disruption-free, which in principle allows higher capacity factors than pulsed or disruption-prone tokamaks. This is a genuine TEA advantage. The Thea Energy Helios preconceptual design — a quasi-axisymmetric planar-coil stellarator — provides the first engineering-grounded capacity factor figure for a commercial stellarator: **88%**, based on a biennial maintenance schedule of ~84 days every two years [arxiv-2512-08027v1.md, §2 Summary of the design].

> "The Helios maintenance operation occurs during one planned outage of approximately 84 days every two years, enabling an 88% capacity factor."
> — arxiv-2512-08027v1.md, §2 Summary of the design

Helios is a different design (QA/planar coil, 8 m major radius) from GIGA (QI/non-planar, 18 m), and its maintenance cycle may be more favorable because planar coils allow simpler sector access. GIGA's more complex 3D blanket geometry (80 segment shapes, undefined maintenance scheme) could push planned outage duration higher — partially offsetting the steady-state advantage. The net effect is that 85–90% is a plausible model range for GIGA's capacity factor, with Helios's 88% as the upper anchor and a modest downward adjustment for GIGA's blanket access complexity. For comparison, a pulsed tokamak (DEMO design basis) targets ~75–80% availability, implying a ~10–15% capacity factor advantage for the stellarator — roughly 10–15% LCOE reduction at constant capital cost. Disruption avoidance eliminates the largest source of unplanned outage in tokamaks (PFC replacement after high-energy events), and the absence of current-drive power simplifies the auxiliary heating system (no NBI or ECRH for current sustainment, only startup/profile control at ~50–100 MW). The TG Brown (2018) comparative study provides the most relevant framework but predates Gauss Fusion's CDR and uses older HELIAS parameters.

**O&M Considerations (Sparse Data)**

No published O&M cost breakdown is available for GIGA or for the HELIAS reactor studies. Key O&M drivers are expected to include: (a) blanket replacement at 5-year intervals (component cycling over a 40-year plant life = ~8 replacement campaigns), (b) remote handling equipment capital and maintenance, (c) ECRH gyrotron replacement (limited lifetime at MW-class power), and (d) superconductor-related maintenance including cryogenic system operations. The demountable joint design (~250 joints per coil at ~1 nΩ) is intended to enable sector-based coil replacement without full machine disassembly — an O&M advantage over conventional welded coil designs — but no published estimate of replacement frequency or cost exists. A placeholder O&M estimate of 2–4% of NOAK capital cost per year (analogous to fission plant estimates) is the only viable approach given current data.

**Cryogenic Parasitic Power Load (Distinct Recirculating Power Component)**

For large superconducting stellarators, the cryogenic power required to maintain the magnet system at operating temperature is a significant and potentially dominant recirculating power component — distinct from ECRH and pumping. Neutron irradiation of the superconducting coils deposits heat that must be actively removed by the cryogenic plant; the electrical cost of that removal is unfavorably large due to Carnot efficiency penalties at 4 K or 20 K. The ParaStell study (Moreno et al., 2024, Frontiers in Nuclear Engineering) quantified this for WISTELL-D — a quasi-isodynamic stellarator at 10.1 m major radius, 2113 MWth — and found total magnet nuclear heating of 152 kW, yielding an estimated cryogenic load of ~63.3 MWe (referenced against the ARIES-CS baseline of 12 kW heating → 5 MWe cryogenic load) [frontiersin-journals-nuclear-engineering-articles-10-3389.md, §Discussion]. This represents approximately 3.0% of WISTELL-D's fusion power devoted entirely to cryogenic load — a 12.7× increase from the ARIES-CS data point.

> "For ARIES-CS, the total magnet nuclear heating was calculated to be 12 kW and deemed acceptable for that stellarator configuration as the resultant liquid He cryogenic load was estimated to be 5 MWe... a total magnet nuclear heating metric of 152.0 kW would correspond to an estimated 63.3 MWe cryogenic load."
> — frontiersin-journals-nuclear-engineering-articles-10-3389.md, §Discussion

For GIGA at 18 m major radius (vs. WISTELL-D's 10.1 m) and 3,000 MWth, scaling from the WISTELL-D data point suggests the cryogenic contribution could reach 3–5% of fusion power or higher. This is material: the analysis currently attributes the 5–7% gap between gross thermal efficiency (~37–40%) and net efficiency (33.3%) primarily to ECRH and pumping. If cryogenic load at GIGA scale is itself in the 3–5% range, the total recirculating power fraction may be understated — and GIGA's net efficiency advantage over a pulsed tokamak (which does not require continuous cryogenic power at this level) may be smaller than the steady-state framing suggests. This is a cost-modeling risk that is absent in the tokamak literature.

---

### Modeling Framework

This analysis uses a **FOAK-anchored free-form modeling approach** rather than a bottom-up CAS-level cost build. The rationale is forced by the data: the only public cost reference for GIGA is a single FOAK figure (€15–18B), with no CAS account breakdown, no subsystem-level cost disclosure, and no published NOAK projection. A bottom-up build would require cost allocations invented rather than sourced. The model is therefore testing the FOAK-to-NOAK learning hypothesis — parameterized as `noak_fraction` (NOAK overnight cost as a fraction of FOAK) — rather than validating a bottom-up cost build. This means the `noak_fraction` sweep is the primary modeling contribution, not a secondary sensitivity; the central LCOE estimate (~$186/MWh) reflects a 55% NOAK fraction applied to the FOAK midpoint, and the uncertainty range is dominated by how much learning the supply chain can achieve, not by errors in subsystem cost estimation. Readers should interpret this analysis as bounding the commercial viability conditions for the learning hypothesis, not as a precise cost estimate.

---

### Key Hypotheses

The following propositions structure the cost model's sensitivity sweep. Each maps to at least one parameter in the Section 5 table and one sensitivity dimension in the model. A finding that falsifies a hypothesis changes the TEA conclusion, not just a data point.

**H1 (FOAK-to-NOAK learning):** If NOAK capital cost reaches 50–60% of FOAK, LCOE falls below ~$100/MWh — the threshold for commercial competitiveness in the 2040–2050 market. The FOAK-implied specific cost of ~€15,000–18,000/kWe means a 50% NOAK fraction yields ~€7,500–9,000/kWe. At 15% FCR and 88% capacity factor, this produces an LCOE of ~$100–120/MWh — marginal but within range. If NOAK fraction exceeds 70% (i.e., minimal learning), LCOE remains above $150/MWh regardless of other assumptions. This is the highest-leverage single parameter in the model.

**H2 (Blanket type and thermal efficiency):** HCPB vs. DCLL blanket choice shifts LCOE by ~20–25% via thermal efficiency (~35% steam Rankine vs. ~40% advanced Brayton). The same fusion power output at 40% vs. 35% conversion efficiency is a ~14% difference in net electrical output — equivalent to a ~14% reduction in LCOE at constant capital cost. Combined with secondary effects (power cycle capital cost, O&M complexity), the blanket type choice is worth ~20–25% in LCOE space. **Cryogenic load caveat:** Unlike the ECRH recirculating power (which scales with startup/profile control requirements and is smaller at burning plasma), the cryogenic parasitic load is continuous and scales with coil neutron irradiation. The WISTELL-D analog suggests ~3% of fusion power for a 10.1 m QI machine; GIGA at 18 m may exceed this. For the stellarator case, net efficiency may be more sensitive to cryogenic load than to ECRH power — the inverse of the tokamak assumption. The model's 5–7% total recirculating power estimate should be treated as a lower bound pending GIGA-specific cryogenic calculations.

**H3 (Steady-state capacity factor advantage):** Steady-state operation at ≥85% capacity factor reduces LCOE by ~10–15% relative to an equivalent pulsed tokamak at 75–80% availability. The Helios 88% figure [arxiv-2512-08027v1.md, §2] provides the upper anchor; the question is whether GIGA's 3D blanket complexity reduces this. A sensitivity sweep over 75–90% capacity factor quantifies the range of this advantage.

**H4 (Scale premium):** GIGA's 18 m machine scale imposes a capital cost premium over a hypothetical compact stellarator at 8–10 m (Helios-class). If the QA/planar design path (Helios) achieves similar physics performance at smaller scale, GIGA's QI approach bears a structural capital cost disadvantage that is not recoverable through learning alone — it is a design-space risk, not a manufacturing maturity risk.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**Non-Planar HTS Stellarator Coils (Demountable) — TRL 3–4**

*This TRL assessment applies specifically to GIGA's quasi-isodynamic (QI) non-planar modular coil architecture. An alternative large-scale stellarator approach — the quasi-axisymmetric (QA) planar-coil design pursued by Thea Energy (Helios) — uses conventionally wound planar and convex coils at significantly relaxed manufacturing tolerances and would carry a different, likely higher, TRL rating for its coil system. The challenges below are QI-specific.*

- **Demonstrated**: W7-X demonstrated 50 non-planar modular superconducting coils (NbTi conductor) at 5.5 m major radius, achieving the target magnetic field configuration and operating since 2015. This is the direct physics and engineering predecessor. At the component level, single REBCO coils have been tested at 20 T (CFS SPARC insert, 2021) and Tokamak Energy demonstrated 11.8 T in a complete HTS coil set (Demo4, Nov 2025). KIT has developed prototype demountable superconducting coil joints under a €9M BMBF grant (April 2024 start) [gauss-fusion-technical-summary.md, §Magnet System; dossier.md §Magnet Type].
- **On paper only**: A 55 mm / 100 kA HTS conductor in the GIGA non-planar modular coil geometry. The "conductor-in-plate" construction concept (plates stack to form coils, avoiding traditional casings) is described in conference abstract [gauss-fusion-technical-summary.md, §Magnet System] but has not been demonstrated at full scale. Demountable joints achieving ~1 nΩ at 100 kA have been designed but not prototyped at production scale.
- **Missing at scale**: Manufacture and qualification of 40 non-planar coils at ~300 tonnes / ~30–35 m perimeter — a 3× scale-up from W7-X in every dimension. Radiation hardening of REBCO tape and joint insulation under 14 MeV neutron flux. Long-term joint resistance stability under neutron irradiation and thermal cycling. Supply chain for 26 million meters of REBCO tape (current global capacity is thousands of km/year).

---

**Demountable Coil Joints at Reactor Scale — TRL 3–4**

- **Demonstrated**: Room-temperature copper joint prototypes and small-scale HTS joint demonstrations at ~10 kA class exist in the literature. ARC/SPARC demountable HTS joint concepts have been developed at CFS (internal, not independently published). Gauss Fusion's KIT collaboration is targeting ~1 nΩ at 100 kA.
- **On paper only**: 250 joints per coil operating at 1 nΩ resistance under sustained current, cryogenic temperatures, and vibration loads from the magnetic force environment. Total joint count across 40 coils is ~10,000 individual joints, each a potential failure point.
- **Missing at scale**: Long-term (decades) joint resistance stability under neutron-induced microstructural changes. Maintenance procedure for joint replacement in a radioactive environment. The tolerable joint resistance sets the maximum recirculating power loss from resistive heating; the ~1 nΩ target is stated but the tolerance analysis (and consequences of exceeding it) is not published.

---

**Breeding Blanket in HELIAS 3D Geometry — TRL 3–4**

- **Demonstrated**: ITER TBM components (both HCPB and DCLL variants) have been designed and prototyped at module scale (EU DEMO TBM program). EUROFER 97 RAFM steel has been characterized under neutron irradiation. KIT and FZJ are the lead developers for both blanket types. An Alsymex fabrication contract for GIGA TBB prototype sub-assemblies is underway [gauss-fusion-partnerships-2025.md, §Partnerships].
- **On paper only**: A full-sector HCPB or DCLL blanket adapted to the HELIAS geometry. The structural study [helias-blanket-studies.md] shows that the bean-shaped sector geometry creates high-stress regions under accident loads and requires extensive segment diversity (80 segments per sector). The maintenance scheme — including how blanket segments are attached to and detached from the vacuum vessel — is explicitly undefined.
- **Missing at scale**: Full-sector 3D neutronics validation at GIGA geometry (current TBR calculations use "idealistic" models without gaps or accurate geometry). Structural qualification of all five segment types under combined neutron, thermal, and accident loads (Segment 5 currently fails RCC-MRx in accident scenario [helias-blanket-studies.md, §6]). Remote handling tooling for a 3D-varying blanket segment population. Industrial-scale production of Li₄SiO₄ pebble beds (if HCPB) or LiPb eutectic management systems (if DCLL). Resolution of the TBR/shielding trade-off constraint in tight LCFS-to-coil spacing regions: the ParaStell study (Moreno et al., 2024) demonstrates for a comparable QI geometry (WISTELL-D, 10.1 m) that regions of minimum plasma-coil clearance (~30 cm available space after structure) cannot be better shielded by increasing total blanket build thickness — the available space in those regions is fixed by the coil geometry. The only path to improved local magnet protection is reducing the local breeder fraction (increasing the HTS shield layer), which directly reduces TBR in those regions [frontiersin-journals-nuclear-engineering-articles-10-3389.md, §Discussion]. This TBR/shielding coupling is a structural constraint specific to QI non-planar designs; it is absent in QA planar-coil stellarators (Helios) and in tokamaks, strengthening the QI vs. QA design-risk comparison in Section 7.

> "Segment 5 is the only one showing some areas where the equivalent stress exceeded 500 MPa (Figure 19), and the criteria are not verified (Table 22)... mainly due to the very peculiar shape of the segment, which makes the proposed CP design unable to fully withstand the accidental loads."
> — helias-blanket-studies.md, §6 "DISCUSSION AND RESULTS COMPARISON"

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: JET and TFTR handled gram-scale tritium. ITER fuel cycle design is mature (tritium exhaust processing, storage, fueling). Lab-scale tritium extraction from lithium-bearing systems (FLiBe, solid ceramics) is demonstrated.
- **On paper only**: Closed-loop, kg/day-scale tritium processing at GIGA's required throughput. GIGA requires ~55 kg/year tritium throughput (1 GWe D-T at ~100 MW·days/g fusion = ~56 g/day), implying a tritium inventory and processing system comparable to ITER's design.
- **Missing at scale**: Industrial tritium processing at kg/day rates. TBR > 1 demonstrated in a D-T burning environment (no D-T-burning stellarator has ever operated). The GIGA blanket TBR margin (idealistic HCPB: 1.3863 vs. realistic with gaps: ~1.15 [Bongiovi 2022]) leaves limited buffer for unaccounted losses. If the DCLL blanket achieves higher TBR (~1.2–1.3 without gap penalties), the margin is more comfortable.

---

**Divertor in 3D Stellarator Geometry — TRL 4–5**

- **Demonstrated**: Tokamak divertors (ITER W-monoblock, tungsten armor at >10 MW/m² in WEST/DTT/AUG) are a mature technology in 2D toroidal geometry. W7-X has operated an island divertor (a stellarator-specific design concept) since 2018 and demonstrated detached operation. The HELIAS reactor context cites "preliminary computations indicate a thermal load of more than 10 MW/m²" on target plates [helias-reactor-context.md, §Conclusions].
- **On paper only**: An island divertor for GIGA at reactor-scale heat loads. The W7-X island divertor has operated at ~8 MW injected power; GIGA at 3 GWth burn requires handling uncaptured heat fluxes orders of magnitude higher. The 3D geometry of stellarator divertors introduces distributed strike-point patterns and complex target shaping.
- **Missing at scale**: Tungsten target materials qualified for sustained 10+ MW/m² and 14 MeV neutron co-damage at GIGA's 40-year timescale. Remote replacement in a complex 3D geometry. Detachment physics validated at burning-plasma conditions.

---

**Remote Maintenance System — TRL 4–5**

- **Demonstrated**: ITER remote handling prototypes for blanket and divertor exchange are in detailed design/fabrication. Sector-based maintenance concepts for tokamaks are well developed.
- **On paper only**: A sector-based maintenance scheme for GIGA exploiting the demountable coil joints to allow blanket section removal. No published maintenance procedure or tooling specification has been released for GIGA. The demountable joint concept enables coil removal in principle; the operational procedure is not designed.
- **Missing at scale**: Radiation-hardened robotic systems for a 3D blanket with 80 different segment shapes. Precise alignment tooling for reinstalling demountable coil joints at ~1 nΩ resistance. Maintenance cycle time estimates (which determine planned availability loss per blanket replacement campaign).

---

**ECRH Heating Systems — TRL 6–7**

- **Demonstrated**: 170 GHz MW-class gyrotrons routinely operate on W7-X, ITER heating system gyrotrons are in production, and ECRH systems up to tens of MW exist. ECRH is the universal stellarator heating method and has been confirmed on every major stellarator to date.
- **On paper only**: ECRH at the power levels needed for GIGA startup (estimated ~50–100 MW; no Gauss-published specification). Continuous-wave operation at GW-class plant with high wall-plug efficiency.
- **Missing at scale**: High-efficiency CW gyrotrons (current wall-plug efficiency ~50–55%; improvement to >60% needed to limit recirculating power). Launcher design in the complex GIGA port geometry.

---

**Vacuum Vessel and Cryostat — TRL 7–8**

- **Demonstrated**: ITER vacuum vessel sectors are manufactured and welded at full scale (~10,000-tonne total VV). W7-X vacuum vessel successfully contains a complex 3D plasma volume.
- **Missing at scale**: A 3D vacuum vessel conforming to GIGA's 18 m geometry (~10,000 tonnes steel [gauss-fusion-technical-summary.md, §Supply Chain Requirements]), with precisely positioned porthole openings (8 large portholes per field period = 32 total in GIGA) and integration with the demountable coil support structure.

---

**Balance of Plant (Power Conversion) — TRL 8–9**

- **Demonstrated**: Steam Rankine cycles at GW scale are fully mature technology from fission and fossil plants. sCO2 Brayton cycles are at TRL 5–6 for the cycle itself.
- **Missing at scale**: Integration with GIGA-specific heat sources (He coolant at 8 MPa / ~480°C for HCPB, or PbLi at higher temperatures for DCLL), tritium permeation management through primary heat exchangers, and qualification of heat exchanger materials in the tritium environment.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO HTS Tape — Critical Bottleneck**

GIGA's supply requirement of ~26 million meters of HTS superconductor [gauss-fusion-technical-summary.md, §Supply Chain Requirements] is the single largest supply chain constraint. Current global REBCO production is estimated at thousands of km/year across all manufacturers (Shanghai Superconductor Technology, SuperPower, Fujikura, SuNAM, Tokamak Energy tape manufacturing). Meeting GIGA's 26,000 km requirement for a single plant would require multiple years of current total global production. Cost targets for commercial fusion viability are on the order of $5–10/kA-m (vs. current market prices of ~$30–100/kA-m). The Gauss Fusion / Tokamak Energy HTS collaboration [dossier.md §Magnet Type; gauss-fusion-partnerships-2025.md §HTS Partnerships] is explicitly oriented toward supply chain development, but the scale of ramp-up required is unprecedented. This constraint is shared with all HTS-dependent fusion concepts (CFS, Tokamak Energy ST-E1, Proxima Fusion).

**Nb3Sn (LTS Track) — Available but Complex**

If the LTS development track (likely Nb3Sn) wins for the GIGA production design, supply constraints are more manageable — the ITER program required ~600 tonnes of Nb3Sn strand and GIGA's ~800t LTS estimate [gauss-fusion-technical-summary.md, §Supply Chain Requirements] is comparable. Nb3Sn production techniques are mature. The key supply consideration is Nb3Sn's brittleness and sensitivity to strain, which makes winding non-planar stellarator coil geometries mechanically demanding. The "conductor-in-plate" approach may partially address this by winding into pre-formed plates rather than complex curved forms.

**Beryllium (HCPB Neutron Multiplier) — Constrained Supply**

HCPB blankets use beryllium pebble beds (~40 mm thick per layer) as neutron multipliers [helias-blanket-studies.md, §3.2]. Global beryllium production is approximately 300 tonnes/year, dominated by a single US producer (Materion Corp). A GW-scale HCPB blanket requires tens to hundreds of tonnes of Be multiplier — a significant fraction of annual global production. Beryllium is toxic (berylliosis risk), limiting manufacturing to specialized facilities. If GIGA uses the DCLL blanket, beryllium requirements drop substantially (LiPb provides neutron multiplication via Pb). This uncertainty (HCPB vs. DCLL) propagates directly into supply chain risk.

**EUROFER 97 RAFM Steel — Limited Production at Quality**

All HELIAS blanket designs use EUROFER 97 (Reduced Activation Ferritic-Martensitic steel) as the primary structural material, with a maximum operating temperature of 500°C [helias-blanket-studies.md, §3.2]. EUROFER 97 production is limited to a handful of European producers and has never been manufactured at the scale required for a commercial fusion plant. Irradiation swelling and creep data at fusion-relevant fluences (>10 dpa) are still being developed. For GIGA's 80 blanket segments per sector × 8 sectors = 640 segments total, each requiring precise EUROFER fabrication in complex 3D geometry, production scale-up from current R&D quantities is a significant manufacturing challenge.

**Li₄SiO₄ Pebble Beds (HCPB Breeder) — Limited Industrial Scale**

HCPB breeding uses lithium orthosilicate (Li₄SiO₄) pebbles at 15.5 mm poloidal thickness per layer [helias-blanket-studies.md, §3.2]. Li₄SiO₄ pebble production at reactor scale does not currently exist as an industrial process — ITER TBMs have used small batches from research facilities. A full GIGA HCPB blanket would require industrial-scale Li₄SiO₄ production with controlled Li-6 enrichment (natural Li-6 fraction is 7.6%; enrichment to ~30–40% Li-6 is common for solid breeders). If DCLL is chosen, LiPb eutectic (80%Pb / 20%Li by atoms) replaces solid breeders; LiPb is more readily producible but introduces liquid metal compatibility issues (corrosion, MHD pressure drops, tritium permeation to coolant).

**Lithium — Adequate Supply**

GIGA's stated lithium inventory is ~75 tonnes [gauss-fusion-technical-summary.md, §Supply Chain Requirements], plausibly consistent with HCPB solid breeder requirements. Lithium is produced in substantial quantity globally (~100,000 tonnes/year, dominated by Chile, Australia, China) and is not a near-term supply constraint for fusion at the single-plant scale. Li-6 enrichment requires specialized isotope separation facilities; global capacity is limited to a few facilities, but at 75-tonne scale, this is manageable.

**Tungsten — Adequate Supply, Manufacturing Challenges**

First wall tungsten armor (2 mm thick [helias-blanket-studies.md, §3.2]) is standard in ITER-heritage designs. Tungsten is not a supply constraint but presents manufacturing challenges: large, precisely-shaped tungsten components that survive extreme heat loads and neutron damage without cracking. The 3D GIGA wall geometry increases the number of unique tungsten shapes required, similar to the blanket segment diversity problem.

**Vacuum Vessel Steel — Feasible at Scale**

~10,000 tonnes of vacuum vessel steel [gauss-fusion-technical-summary.md, §Supply Chain Requirements] is within the range of large industrial steel fabrication. The tolerancing requirements for the complex 3D vacuum vessel (which must position blanket attachment points and port openings to millimeter precision) are the primary challenge, not material supply.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output | 1 GWe | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Stated as design target |
| Thermal (fusion) power | 3 GW | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Implied by 3 GW thermal → 1 GW electric |
| Net thermal efficiency | 33.3% | [inferred: 1 GWe / 3 GWth; no explicit gross efficiency stated] | medium | Likely net after recirculating power; gross thermal conversion may be ~37–40% |
| Gross thermal efficiency (HELIAS reference) | ~35% standard; >40% TAURO advanced | helias-reactor-context.md §7. The Helias Reactor as a Power Plant | medium | For HELIAS design point; GIGA not explicitly stated; lower net (33%) consistent with 35% gross minus ~5–7% recirculating |
| Major radius | 18 m | gauss-fusion-technical-summary.md §GIGA Power Plant; dossier.md §Driver Technology | high | HSR4/18 heritage (4 field periods, R=18m) |
| Minor radius (plasma) | 1.7 m | gauss-fusion-technical-summary.md §GIGA Power Plant | high | |
| Plasma volume | 1,500 m³ | gauss-fusion-technical-summary.md §GIGA Power Plant | high | |
| On-axis magnetic field | 6 T | dossier.md §Driver Technology | high | Peak coil field 12–13 T (exceeds NbTi practical limit) |
| Peak coil field | 12–13 T | dossier.md §Driver Technology; dossier.md §Magnet Type | high | Basis for Nb3Sn/REBCO requirement over NbTi |
| Number of coils | 40 (5 shapes × 8) | gauss-fusion-technical-summary.md §Magnet System | high | Non-planar modular; ~250 demountable joints per coil |
| Coil current | 100 kA | gauss-fusion-technical-summary.md §Magnet System | high | Common cross-section: 55 mm diameter |
| Demountable joint resistance target | ~1 nΩ | gauss-fusion-technical-summary.md §Magnet System | high | Per joint; total dissipation across ~10,000 joints is LCOE-relevant |
| First wall neutron load (average) | 1 MW/m² | dossier.md §Neutron Management; helias-reactor-context.md §7 | high | Peak 1.7 MW/m² (HELIAS reference) |
| Blanket/first wall design life | 5 years | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Implies ~8 replacement campaigns over 40-year life |
| Magnet and vacuum vessel life | 40 years | gauss-fusion-technical-summary.md §GIGA Power Plant | high | |
| FOAK capital cost estimate | €15–18B | gauss-fusion-technical-summary.md §Funding | medium | First-of-a-kind only; no NOAK projection published |
| FOAK specific capital cost | ~€15,000–18,000/kWe | [inferred: €15–18B / 1 GWe] | medium | Derivation: FOAK cost / net electric output; excludes IDC |
| Supply: HTS superconductor | ~26 million meters | gauss-fusion-technical-summary.md §Supply Chain Requirements | high | ~26,000 km — exceeds current global annual REBCO production by >10× |
| Supply: LTS superconductor | ~800 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | high | Likely Nb3Sn if LTS track selected |
| Supply: total SC coil mass | ~35,000 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | high | Including casing, structure |
| Supply: vacuum vessel steel | ~10,000 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | high | |
| Supply: lithium inventory | ~75 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | high | For tritium breeding blanket |
| Energy confinement time (required) | 1.6 s | helias-reactor-context.md §7. The Helias Reactor as a Power Plant | medium | For HSR4/18 design point; applicable to GIGA with same geometry |
| HCPB TBR (idealistic, no gaps) | 1.3863 | helias-blanket-studies.md §2 | medium | Idealized model; realistic value lower |
| HCPB TBR (realistic estimate) | ~1.15 | dossier.md §Tritium Breeding [citing Bongiovi 2022] | medium | With geometry, gaps, and manufacturing constraints |
| HCPB He coolant pressure | 8.0 MPa | helias-blanket-studies.md §Table 5 | high | Normal operating condition; design pressure 9.2 MPa |
| HCPB coolant outlet temperature | ~445–485°C (segment-dependent) | helias-blanket-studies.md §Table 5 | high | Helium coolant; enables steam Rankine cycle |
| Alpha particle loss fraction | ~2.5% | helias-reactor-context.md §Conclusions | medium | Stochastic ripple diffusion; "considered tolerable" |
| HSR4/18 component lifetime (wall) | 4.6 years | helias-reactor-context.md §7. The Helias Reactor as a Power Plant | medium | Vs. 2.3 years for DEMO tokamak at same power — stellarator advantage from lower average wall loading |
| HELIAS core cost reduction (HSR4 vs. HSR5) | ~20% | helias-reactor-context.md §Conclusions | medium | Reduction from 5 to 4 field periods; directly applicable as GIGA uses 4-period design |
| Blanket segment count | 80 per sector, 640 total | helias-blanket-studies.md §2 [inferred: 80 × 8 field periods for GIGA] | medium | 16 rings × 5 shapes; 20 mm gaps between segments |
| W7-X coil count (predecessor) | 50 non-planar (NbTi) | helias-reactor-context.md §2. Coil System | high | At 5.5 m major radius; LTS predecessor to GIGA |
| Capacity factor (analog — Helios/Thea Energy QA stellarator) | 88% | arxiv-2512-08027v1.md §2 Summary of the design | medium | Basis: ~84-day biennial outage; Helios is QA/planar-coil design at 8 m, not QI GIGA at 18 m — use as plausibility anchor; model range 85–90% |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| NOAK capital cost / $/kWe | proprietary | blocking | FOAK figure is given; no fleet learning projection published |
| Capacity factor (GIGA-specific) | not-yet-sourced | important | Helios (QA/planar, 8 m) provides 88% analog; GIGA-specific target undisclosed. Model range 85–90% pending disclosure |
| Blanket type (HCPB vs. DCLL) | proprietary | blocking | Determines power cycle, TBR margin, coolant chemistry |
| Gross thermal efficiency | derivable | important | Can be estimated from blanket type once known; ~35% (HCPB/steam) or ~40%+ (DCLL/sCO2) |
| Recirculating power fraction | derivable | important | Dominated by ECRH power + cryogenic load; ECRH startup power not published. WISTELL-D analog (Moreno et al. 2024): ~3% of fusion power for cryogenic load alone at 10.1 m QI geometry — lower bound for GIGA at 18 m. Total recirculating 5–7% estimate may be understated if cryogenic load scales with size |
| Cryogenic parasitic load (standalone) | derivable | important | WISTELL-D (10.1 m, 2113 MWth): 152 kW magnet heating → 63.3 MWe cryogenic load (~3% of fusion power). ARIES-CS reference: 12 kW → 5 MWe (12.7× lower). GIGA at 18 m not calculated; likely 3–5%+ of fusion power [frontiersin-journals-nuclear-engineering-articles-10-3389.md §Discussion] |
| O&M cost (fixed + variable) | truly-unknown | important | No HELIAS or GIGA O&M estimate published; placeholder 2–4% of NOAK capital |
| ECRH startup/profile power | derivable | important | At burning plasma conditions (~50–100 MW range, but unstated); affects recirculating power |
| Realistic TBR with geometric penalties | not-yet-sourced | important | Full 3D MCNP calculation needed; idealistic (1.386) vs. realistic (1.15) gap is ~20% |
| Demountable joint ohmic dissipation | derivable | important | ~1 nΩ × I² × N_joints = loss; not published as integrated power figure |
| Coil mass per unit (GIGA-scale) | not-yet-sourced | nice-to-have | HSR4/18 HELIAS gives 94t per coil (NbTi); GIGA may differ with HTS conductor |
| Power conversion cycle (steam vs. sCO2) | proprietary | important | Depends on blanket; determines BoP cost and efficiency |
| Beta value (operating point) | not-yet-sourced | nice-to-have | HSR4/18 HELIAS gives 4.2% at design; GIGA not explicitly stated |
| Blanket complexity multiplier (fabrication cost premium) | truly-unknown | important | 80+ unique segment shapes vs. ~2 for tokamak; no cost analogue in literature. Range: 1.0–2.5× applied to blanket/VV sub-component of CAS22. Model sweep needed — this is GIGA's most distinctive cost-penalty differentiator and must not be hidden inside the aggregate NOAK fraction |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | NOAK capital cost by CAS subsystem | S1, S5 | proprietary | blocking | CDR access; HELIAS cost study (TG Brown 2018 provides comparative framework) |
| 2 | Capacity factor (GIGA-specific) | S2, S5 | not-yet-sourced | important | Helios QA stellarator provides 88% analog (biennial 84-day outage); GIGA-specific figure remains undisclosed. Downgraded from blocking: 85–90% model range now has an engineering anchor |
| 3 | Blanket type (HCPB vs. DCLL) | S2, S3, S5 | proprietary | blocking | CDR; KIT/FZJ publications on GIGA-specific blanket design |
| 4 | O&M cost breakdown (fixed vs. variable, scheduled vs. unplanned) | S2, S5 | truly-unknown | important | No HELIAS-scale O&M cost study exists; analogue from ARIES-CS (ARIES stellarator study) |
| 5 | Recirculating power fraction | S2, S5 | derivable | important | Derivable from ECRH power + cryogenic load + pumping; requires ECRH power to be stated |
| 6 | Gross thermal efficiency | S5 | derivable | important | Derivable from blanket type (HCPB: ~35%; DCLL: ~38–42%); resolves when gap #3 resolves |
| 7 | Realistic TBR with GIGA geometry gaps | S3, S5 | not-yet-sourced | important | Full 3D MCNP calculation for GIGA geometry with 20 mm gaps and accurate segment shapes |
| 8 | Demountable joint performance at scale (resistance stability, lifetime) | S3 | truly-unknown | important | No published test result at 100 kA / nΩ scale; ongoing KIT program |
| 9 | Blanket maintenance procedure and replacement cycle time | S3 | truly-unknown | important | HELIAS blanket study explicitly states maintenance scheme is undefined; availability impact unknown |
| 10 | ECRH startup and profile control power | S2, S5 | derivable | nice-to-have | At burning plasma conditions, alpha heating dominates; ECRH likely ~50–100 MW; no Gauss-specific statement |
| 11 | HTS vs. LTS conductor cost differential for stellarator geometry | S4, S5 | proprietary | important | Gauss pursuing dual track; cost comparison drives NOAK magnet cost; ICAS / Tokamak Energy supply chain negotiations |
| 12 | HSR4/18 to GIGA scaling: coil mass and cost at 12–13 T vs. 10 T | S3, S5 | derivable | important | HELIAS gives 94t/coil for NbTi at 10 T; GIGA targets 12–13 T requiring conductor upgrade; mass/cost scaling not published |
| 13 | Segment 5 structural fix (current design fails RCC-MRx in accident loads) | S3 | not-yet-sourced | important | helias-blanket-studies.md identifies failure; resolution (CP redesign or geometry change) not published |

---

## Section 7: Cross-Concept Notes

**Nearest neighbors**: Conventional large-scale tokamak (DEMO / ARIES-AT class) — primary reference; Spherical tokamak HTS (Tokamak Energy ST-E1) — secondary reference. Both are approved prior analyses.

---

### Comparison 1: Conventional Large-Scale Tokamak (DEMO / ARIES-AT Class)

The conventional large-aspect-ratio D-T tokamak is the primary reference for GIGA: both concepts target 1 GWe net output, use EUROFER-heritage RAFM structural materials, operate in the 6–7 T on-axis field range, and plan for HTS or advanced superconducting coil systems in future designs. GIGA's differentiators are best understood as departures from this baseline.

**Shared elements:** D-T fuel cycle; tritium breeding blanket requirements (TBR > 1, HCPB or DCLL heritage); EUROFER 97 structural steel; first-wall tungsten armor; superconducting magnet system; similar thermal output class (DEMO targets ~2 GWe, ARIES-AT targets ~1 GWe); blanket replacement as the primary maintenance driver.

**Key divergences with TEA implications:**

| Divergence | DEMO/ARIES-AT | GIGA Stellarator | TEA Impact | CAS Account |
|-----------|---------------|-----------------|-----------|------------|
| Current drive requirement | CS + NBI for current sustainment | None — rotational transform geometric | GIGA saves ~50–200 MW recirculating power; removes CS magnet cost | CAS22 lower (no CS magnet); reduced auxiliary heating capital |
| Operation mode | Pulsed (~75–80% CF) or long-pulse | Inherently steady-state (~85–90% CF) | +10–15% LCOE improvement for GIGA at constant capital cost | CAS70 lower (reduced unplanned outage O&M) |
| Disruption risk | Significant; forces PFC overdesign | Absent — disruption-free | GIGA avoids unplanned outage cost; lowers O&M uncertainty | CAS70 lower (no disruption-driven PFC replacement) |
| Blanket geometry | ~2 unique segment shapes (in/outboard) | 80+ unique shapes across 3D surface | GIGA blanket fabrication more expensive; maintenance more complex | CAS22 higher (blanket fabrication sub-accounts) |
| Machine scale | R ≈ 6–9 m (DEMO: 9 m, ARIES-AT: 5.2 m) | R = 18 m | GIGA coil system mass ~4–8× larger; dominant cost driver | CAS22 higher (coil system mass); CAS21 higher (buildings/structures) |
| Blanket component lifetime | 2.3 years at DEMO power | 4.6–9 years (HELIAS at lower avg. wall load) [helias-reactor-context.md §7] | Fewer replacement campaigns over plant life → lower blanket O&M cost | CAS70 lower (scheduled blanket replacement campaigns) |
| Coil geometry | 2D toroidal (manufacturable) | 3D non-planar modular (novel at scale) | GIGA bears additional manufacturing R&D cost vs. established tokamak coil practice | CAS22 higher (coil fabrication complexity) |

**Net TEA assessment vs. conventional tokamak:** GIGA's primary arguments are steady-state operation (capacity factor advantage), no current drive (recirculating power advantage), and longer blanket lifetime (O&M advantage). These are real but bounded: the capacity factor benefit is worth ~10–15% in LCOE, and the recirculating power advantage is worth a few percent. Both are smaller in magnitude than the penalty from GIGA's 3× larger machine radius, which drives capital cost up in a scale relationship that is not offset by these advantages at FOAK. The stellarator TEA case therefore rests entirely on NOAK learning: if the non-planar coil system and complex blanket can be manufactured serially at near-tokamak unit cost, the operational advantages tip the balance. If not, GIGA remains structurally more expensive to build and only marginally cheaper to operate.

---

### Comparison 2: Spherical Tokamak HTS (Tokamak Energy ST-E1)

The large-scale stellarator and spherical tokamak share the D-T fuel cycle and REBCO HTS magnet dependency, but diverge in ways that matter significantly for TEA.

**Shared supply chain assumptions (reused from 21-spherical-tokamak-hts):**
- REBCO tape supply and cost trajectory are shared constraints. Both concepts require supply chain scale-up by one to two orders of magnitude from current production, and both target $5–10/kA-m as the commercial viability threshold. The Tokamak Energy HTS collaboration with Gauss Fusion [dossier.md §Magnet Type] literally shares an industrial partner, creating direct supply chain interdependence.
- The D-T tritium supply problem is identical: global civilian tritium inventory of ~25 kg, CANDU decline, need for TBR > 1. The HELIAS TBR targets (1.15–1.39) and the ST-E1 TBR = 1.2 are both in the marginal range; neither has wide margin for geometric losses or manufacturing tolerances.

**Divergences from 21-spherical-tokamak-hts:**

*Steady-state vs. pulsed operation (major TEA divergence):*
The ST-E1 analysis (Section 2, challenge #4) identifies pulsed operation as an LCOE cost driver: thermal energy storage buffer, CS re-magnetization downtime, plasma restart PFC stress. The large-scale stellarator eliminates all of these: inherent steady-state operation removes the need for a thermal buffer (~$50–200M estimate for grid-scale storage) and avoids plasma restart transient wear. This is the stellarator's strongest TEA argument and is not captured in the Brown (2018) comparative cost study.

*Current drive vs. ECRH-only flat-top (recirculating power):*
The ST-E1 analysis identifies ECRH-only current drive as a significant recirculating power challenge (wall-plug efficiency ~50–55%). The GIGA stellarator does not require current drive — the rotational transform is generated geometrically by the coil winding law. ECRH is needed only for startup and profile control (~50–100 MW range), not for flat-top current sustainment. This reduces recirculating power fraction relative to the ST-E1, improving plant gain Q_p.

*Blanket geometry complexity (large-scale stellarator disadvantage):*
The ST-E1 outboard-only liquid lithium blanket has geometric simplicity (though poor TBR margin from half-solid-angle coverage). The GIGA blanket has the opposite profile: full 4π solid angle coverage potential, but 80 unique segment shapes and structurally challenging bean-shaped regions [helias-blanket-studies.md, §3]. Remote maintenance of 640 unique blanket segments across a complex 3D geometry is likely more expensive than remote maintenance of a simpler outboard-only tokamak blanket. This is an LCOE disadvantage for the stellarator that is absent in the ST analysis.

*Machine scale (large-scale stellarator disadvantage):*
The ST-E1 has R = 5.0 m; GIGA has R = 18 m. Capital cost does not scale linearly with machine size, but for large superconducting coil systems, it scales approximately as R^2 to R^2.5 (coil volume and mass). At equal thermal power, the stellarator achieves steady-state but at 3× the machine scale, which dominates the capital cost comparison. The fundamental question for the stellarator TEA — never yet definitively answered in a published study — is whether the operational advantages (capacity factor, Q_p, maintenance predictability) justify the capital cost premium of a larger machine.

*No disruption risk (stellarator advantage not in ST analysis):*
Disruption events in tokamaks can destroy PFCs and force unplanned outages. The ST analysis does not model this explicitly, but it is a background risk that inflates expected maintenance costs and availability loss. The stellarator's disruption-free operation is a genuine O&M advantage. Quantifying this requires a disruption frequency model for the tokamak reference; no such comparative calculation exists in the public literature.

---

### Design Path Note: QI Non-Planar (GIGA) vs. QA Planar-Coil (Helios/Thea Energy)

The large-scale stellarator concept space contains at least two commercially pursued design paths with fundamentally different engineering profiles:

**Quasi-isodynamic (QI) non-planar modular — GIGA/HELIAS heritage (this analysis):** 18 m major radius; 40 non-planar coils in 5 distinct shapes; ~300 tonnes per coil; tolerances compound nonlinearly at scale; manufacturing precedent only at W7-X (5.5 m); coil complexity is the primary LCOE risk; higher physics confidence (HELIAS heritage, decades of stellarator optimization).

**Quasi-axisymmetric (QA) planar-coil — Helios/Thea Energy:** 8 m major radius; planar and convex coils wound conventionally; large gaps between encircling coils enable sector-based maintenance (entire toroidal sectors removable, vs. GIGA's 222-component serial extraction from ARIES-CS analysis [arxiv-2512-08027v1.md, §1 Introduction]); coils are further from the plasma, significantly easing blanket design; independently adjustable shaping coil currents enable field correction during operation, relaxing manufacturing tolerance requirements [arxiv-2512-08027v1.md, §4.1].

> "Because of the small gaps between ARIES-CS coils, there were only three small ports envisioned for maintenance. Consequently 222 individual components had to be serially removed through these ports. Helios has large gaps between large, planar encircling coils, and the shaping coils can be removed from between them. Entire toroidal sectors may be removed and replaced at a time."
> — arxiv-2512-08027v1.md, §1 Introduction

**TEA implication:** The challenges in Section 2 (#1 scale and capital cost, #4 non-planar coil manufacturing, #5 conductor technology at scale) and Section 3 (coil TRL 3–4) are QI-specific, not inherent stellarator constraints. If the QA planar-coil path proves viable at commercial scale, GIGA's capital cost premium from coil complexity becomes a design-choice risk — a consequence of pursuing quasi-isodynamic physics — rather than a physics-imposed constraint on all stellarators. The Helios 88% capacity factor anchor (Section 5) likely represents the performance achievable by the simpler QA architecture; whether GIGA achieves comparable capacity factor with its more complex maintenance geometry is an open question. This is material to Goal 1 (concept positioning): GIGA is best understood as the large-scale QI stellarator, not simply the large-scale stellarator.

---

## Section 8: Sources

1. **gauss-fusion-technical-summary.md** — Primary Gauss Fusion machine parameter source. Provides GIGA dimensions, power targets, magnet architecture, supply chain volumes, and FOAK cost estimate. Derived from Gauss Fusion press materials, MT29 conference abstract (2024), and CDR announcement summaries. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-01/sources/gauss-fusion-technical-summary.md`

2. **helias-reactor-context.md** — Comprehensive synthesis of the HELIAS HSR4/18 and HSR5/22 reactor studies (IPP Garching, published literature). Provides the complete HELIAS parameter set: plasma parameters, coil geometry and mass, blanket mass options, neutron wall loading, component lifetime estimates, and cost comparison rationale between 4- and 5-period designs. The most complete LCOE parameter source for GIGA by analogy. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-01/sources/helias-reactor-context.md`

3. **helias-blanket-studies.md** — Peer-reviewed structural mechanics study of the HELIAS 5-B HCPB breeding blanket (2022). Provides: detailed segment geometry (80 segments/sector), TBR estimates (idealistic: 1.3863; realistic lower), material specifications (EUROFER 97, Li₄SiO₄, Be, W armor), coolant conditions (8 MPa He, 445–485°C), and identification of structural failure modes under accident loads. Critical source for blanket maturity assessment. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/helias-blanket-studies.md`

4. **dossier.md** — Phase 1a research dossier for the large-scale stellarator. Provides confidence-rated values for all differentiation table columns with multi-iteration sourcing. The most complete single-document summary of what is publicly known about GIGA's design choices. Located at: `knowledge/concept_research/10-large-scale-stellarator/dossier.md`

5. **gauss-fusion-partnerships-2025.md** — Partnership announcements covering KIT/FZJ/IDOM (TBB), ENEA/ICAS (conductors), Alsymex (TBB prototype fabrication), and Tokamak Energy (HTS). Important for supply chain maturity assessment and understanding the dual-track magnet strategy. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-partnerships-2025.md`

6. **gauss-fusion-cdr-review-2026.md** — Press coverage of the CDR independent review (13-member expert panel, 2025–2026). Provides context for institutional validation but minimal quantitative content. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-cdr-review-2026.md`

7. **Bongiovi et al. (2022)** — HCPB blanket study for HELIAS 5-B geometry (cited in dossier.md §Tritium Breeding as source for realistic TBR ~1.15). Published in International Journal of Energy Research. Provides the realistic-design TBR accounting for geometric penalties. Not directly extracted as a source document; cited via dossier.

8. **Brown, T.G. (2018)** — "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements." IEEE Transactions on Plasma Science 46(6). The most relevant published comparative cost study across concept families. Provides cost element breakdown methodology applicable to GIGA. Cited in dossier.md §Key Sources and handwritten exemplar 01-hts-compact-tokamak.md.

9. **21-spherical-tokamak-hts analysis** (approved) — Cross-concept reference providing analysis of Tokamak Energy ST-E1, which shares REBCO supply chain dependency, D-T tritium constraints, and ECRH heating considerations with GIGA. Divergences (steady-state vs. pulsed, current drive vs. none, blanket geometry) identified in Section 7. Located at: `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/`

10. **frontiersin-journals-nuclear-engineering-articles-10-3389.md** — ParaStell scoping study (Moreno et al., 2024, Frontiers in Nuclear Engineering) on parametric stellarator blanket and shield design for WISTELL-D (quasi-isodynamic, 10.1 m major radius, 2113 MWth). Key contributions: quantified magnet nuclear heating (152 kW) and cryogenic electrical load (~63.3 MWe, ~3% of fusion power); identified the TBR/shielding trade-off coupling in tight LCFS-to-coil spacing regions; ARIES-CS comparison (12 kW → 5 MWe, 12.7× lower than WISTELL-D). Directly analogous to GIGA's QI geometry. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389.md`

10. **arxiv-2512-08027v1.md** — Thea Energy Helios preconceptual design paper. Provides the only engineering-grounded capacity factor figure for a commercial stellarator (88%, biennial 84-day outage), quasi-axisymmetric planar-coil architecture description, maintenance scheme comparison vs. ARIES-CS serial extraction, and energetic particle confinement rationale. Used as analog source for capacity factor and as cross-concept design path contrast in Section 7. Located at: `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/arxiv-2512-08027v1.md`
