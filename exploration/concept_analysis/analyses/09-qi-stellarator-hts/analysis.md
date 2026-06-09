---
ID: 09-qi-stellarator-hts
Concept: QI Stellarator HTS (Proxima Fusion / Stellaris)
Company: Proxima Fusion
Status: draft
Created: 2026-06-09
Approved-Date:
Confinement-Family: MFE
Archetype: STELLARATOR
Archetype-Fit: High
Comparison-Status: costingfe
Comparables:
  - 05-planar-coil-stellarator
  - 10-large-scale-stellarator
  - 20a-type-one-stellarator
  - 20b-renaissance-stellarator
  - 36-helical-coil-stellarator
Design-Point-Name: Stellaris commercial plant concept (Proxima Fusion, FED Vol. 214, 2025)
Design-Point-Maturity: paper-concept
P-Native: 1000
Grounding-Confidence: high
---

## Design Point

- Name: Stellaris commercial plant concept (Proxima Fusion, FED Vol. 214, 2025)
- Maturity: paper-concept
- P_native: 1000 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
  - knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md
  - knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md

## 1. Availability of Data

**Rating: Moderate**

Proxima Fusion published the Stellaris power plant concept in Fusion Engineering and Design (Vol. 214, May 2025), providing a comprehensive technical reference spanning plasma physics, magnets, breeding blanket, neutronics, divertor, first wall, remote maintenance, and safety. The paper presents a fully integrated design incorporating electromagnetic, structural, thermal, and neutronics simulations — the first stellarator concept to achieve this level of cross-domain integration. The design targets 2.7 GW peak fusion power and ~1 GW net electrical output with a 90% availability target based on a 4-year operating cycle.

The company maintains active transparency through technical blogs (tritium fuel cycle, W7-X heritage, optimization tools) and partnership announcements. In February 2026, Proxima signed an MoU with RWE, the Free State of Bavaria, and Max Planck IPP to build Alpha (demonstration stellarator, Q>1, ~€2B, operational 2031 in Garching) followed by Stellaris (commercial plant, Gundremmingen former nuclear site, later 2030s). The Alpha project timeline and budget provide some grounding for commercialization readiness, though these are first-of-a-kind demonstration targets rather than NOAK cost data.

Proxima is a spin-off from Max Planck Institute for Plasma Physics, inheriting W7-X stellarator physics validation. W7-X demonstrated quasi-isodynamic (QI) optimization at scale with steady-state 8-minute plasmas and confirmed confinement quality, giving Stellaris a stronger physics basis than paper-only stellarator concepts. The company has developed StarFinder, a cloud-based QI stellarator optimization framework that "allows rapid iteration on QI stellarator designs at lower costs and higher speed than ever before."

**Key data gaps:**
- No published LCOE estimate or detailed cost breakdown for Stellaris
- Divertor heat flux mitigation (detachment, impurity seeding, control) remains unvalidated at commercial-plant scale
- Economic analysis explicitly deferred: "Economic aspects — including parasitic electricity consumption and availability — are outside the scope of this paper, but are paramount to assessing the feasibility of a commercial power plant" (Stellaris paper)
- Maintenance duration estimates are provisional (4-5 months per blanket replacement cycle)
- High-fidelity 3D quench modeling not yet completed for HTS coils
- Manufacturing feasibility for complex 3D HTS coils and blanket/first-wall integration remains to be demonstrated

The available data supports credible physics and engineering analysis but lacks the bottom-up economic validation needed for LCOE confidence. Compared to tokamak concepts with decades of ARIES-class systems studies, stellarator economic modeling remains underdeveloped.

## 2. Challenges in Capturing System Function

Stellaris presents five major challenges for LCOE modeling, ranked by impact on cost uncertainty:

### 1. **HTS magnet manufacturing cost and scalability** (highest uncertainty)

The design requires 50 unique modular coils with complex 3D non-planar geometry, each 10.4 m tall with 9.9 m radial extent, operating at up to 20 T. Peak field locations see 14.4 T on-axis. The winding pack uses REBCO tape in a flat-plate "radial" stacked concept with 225-324 turns per coil. Unlike tokamak D-coils, stellarator coils cannot be manufactured as toroidal arrays of identical units — each of the 50 coils is a unique shape requiring custom winding fixtures and precision assembly.

> "The feasibility of this manufacturing process will be the focus of subsequent studies."
> — stellaris-design-details.md §First Wall

Commonwealth Fusion Systems and Tokamak Energy have demonstrated HTS coil manufacturing at 20+ T for tokamaks, but the geometric complexity here is higher. Proxima plans to establish a magnet factory with up to 1,000 jobs, indicating internal manufacturing rather than reliance on commodity tape suppliers. The cost per coil will depend on achieving series production learning despite each coil being geometrically unique — a different cost-scaling challenge than tokamak coil multiplication.

The Stellaris paper provides coil dimensions and material fractions but no cost estimates. For LCOE modeling, the magnet cost could range from an optimistic tokamak-analogy scaling (HTS $/kg applied to coil mass) to a pessimistic one-of-a-kind fabrication assumption. The spread is likely a factor of 3-5×, dominating capital cost uncertainty.

### 2. **Divertor performance and heat flux management** (critical for availability)

Stellaris uses the island divertor concept validated on W7-X, but the power densities are far higher: 4.05 MW/m² peak neutron wall load vs. W7-X's ~0.1 MW/m². The EMC3-Lite modeling presented in the Stellaris paper assumes 97% power capture by divertor plates under specific assumptions (60% core+edge radiation, perpendicular diffusion coefficient D⊥), but the authors caution:

> "the EMC3-Lite model... should not be mistaken for accurate heat flux predictions"
> — stellaris-design-details.md §Island Divertor

The paper identifies divertor heat flux as a critical future-work item:

> "divertor design, to include heat load calculations in attached and detached conditions, active control schemes (including stable detachment steady-state detachment conditions), particle recycling, neutral gas compression, and pumping"
> — stellaris-design-details.md §Further Improvements

W7-X has demonstrated stable detachment and control in island divertors, but only at research-plasma power levels. Stellaris's 2.7 GW fusion power would require either sustained detachment operation or advanced impurity seeding at scales never tested. If steady-state detachment cannot be achieved, the divertor becomes a life-limiting component requiring frequent replacement, devastating for the 90% availability target.

This uncertainty cannot be resolved without a high-power stellarator demonstration (Alpha may provide partial validation if it reaches high enough fusion power, but that depends on achieving the Q>1 target). For LCOE, the sensitivity is in capacity factor and replacement costs: the difference between 90% availability (as designed) and 75% availability (if divertor replacement intervals are shorter than planned) is a ~20% LCOE penalty.

### 3. **Material lifetime under 14.1 MeV neutron flux** (moderate uncertainty, common to all D-T concepts)

The first wall uses EUROFER97 with a projected 10 full-power-year lifetime at 2700 MW fusion power, driven by ductile-to-brittle transition temperature (DBTT) shift under neutron irradiation. The Stellaris paper notes:

> "It is important to note that the DBTT value carries significant uncertainties due to the limited material dataset available for radiation damage at 14 MeV neutron energy"
> — stellaris-design-details.md §Neutronics

The coil lifetime (99th quantile: ~10 full-power years) is set by critical current density degradation in REBCO tape from neutron fluence. Shielding is designed to keep neutron flux below the tape tolerance, but the damage threshold is "estimated using measurements of ReBCO HTS exposed to neutrons from a fission core" — an extrapolation from a different neutron spectrum.

These lifetimes drive scheduled replacement costs and plant availability (the 4-year operating cycle with 4-5 month blanket replacement assumes a 10-year first wall). If actual lifetimes are shorter, the LCOE impact is moderate (replacement cost scales linearly with replacement frequency), but if the coils degrade faster than expected, the capital amortization becomes front-loaded.

### 4. **Tritium breeding and extraction at commercial scale** (shared with all D-T stellarators and tokamaks)

The Water-Cooled Lithium-Lead (WCLL) blanket achieves TBR = 1.074 in neutronic simulations, including margins for uncertainties. This exceeds the 1.05 target generally considered necessary for self-sufficiency. However, as Proxima notes in their tritium blog:

> "the WCLL blanket is a concept demonstration, not necessarily the final choice — they have a patent for an innovative liquid-metal breeding blanket that may differ"
> — proxima-fusion-technology-page.md §Tritium

The WCLL concept is adapted from EUROfusion DEMO designs and operates at EUROFER97's <550°C limit. Tritium extraction from PbLi via vacuum degassing or permeation is not demonstrated at fusion-plant scale, and tritium permeation through hot structural materials creates inventory management challenges. Proxima's patent-pending alternative blanket may address these issues but remains undisclosed.

For LCOE, the tritium system capital cost ($50M-$100M by analogy to ITER) and operating cost (extraction losses, permeation control, regulatory compliance) are modest compared to magnets and balance-of-plant, but tritium supply risk is existential: if TBR < 1 in practice, the plant cannot operate at full power without external tritium, and global civilian tritium inventory (~25 kg) cannot support a commercial fleet.

### 5. **Quasi-steady plasma control and startup** (lowest cost impact but physics-critical)

Stellarators are disruption-free by design, but they still require active control during startup and density/temperature transients. The Stellaris design uses 50 MW ECRH at 230-240 GHz for startup and <1 MW during ignited operation (per Helios stellarator analogy). The plasma must transition through startup conditions (pellet injection for density ramp, ECRH heating to ignition) without loss of confinement or hitting density limits.

> "Magnetic control is required... Preliminary modeling suggests that the planar coil set... is sufficient to provide this control"
> — helios-stellarator-comparison.md §Startup control

W7-X has demonstrated controlled plasma operations at research scale. Stellaris assumes similar control authority but at higher beta (volume-averaged ~2.76% vs. W7-X's <2%) and higher density. If startup requires more auxiliary power or longer ramp times than assumed, the impact is a modest increase in ECRH system capital cost ($10-20M per gyrotron) and slightly higher recirculating power, not a fundamental LCOE driver.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in **ascending order of maturity** (least mature first):

### **3D Non-Planar HTS Coils — TRL ~3**

**On paper only**: Full-scale 3D non-planar stellarator coils using REBCO tape at 20 T peak field have never been built. The Stellaris design requires 50 unique coil shapes, each 10.4 m tall, with complex curvature optimized for quasi-isodynamic plasma confinement.

**Demonstrated**: REBCO HTS tape production at scale (Faraday Factory Japan supplies Proxima for the SMC demo). Tokamak HTS coils at 20+ T (Commonwealth Fusion Systems SPARC prototype, Tokamak Energy Demo4 at 11.8 T in full-device configuration). Flat-plate "radial" winding pack concept for HTS has been tested at component level.

**Missing at scale**: Manufacturing of geometrically complex 3D coils with the precision required for stellarator field quality (coil placement tolerances typically <1 mm). The Stellarator Model Coil (SMC) demonstration targeted for 2027 will de-risk one coil, but series production of 50 unique coils has no precedent. Quench protection for 3D geometry under neutron flux is unvalidated: "there remains a source of uncertainty for stellarator reactor studies" regarding quench behavior in non-uniform fields.

### **WCLL Breeding Blanket (stellarator-adapted) — TRL ~3–4**

**Demonstrated**: Water-Cooled Lithium-Lead (WCLL) blanket concept is the baseline for EUROfusion DEMO. Small-scale prototypes and neutron irradiation tests up to ~30-50 dpa in fission reactors. Neutronic simulations show TBR = 1.074 for Stellaris geometry.

**On paper only**: Adapting WCLL to the complex 3D stellarator plasma-facing geometry. The Stellaris design maintains uniform 0.95-1.37 m plasma-coil distance (much better than W7-X), but the blanket must conform to non-axisymmetric surfaces. Remote maintenance via sector splitting is novel: "offers a significant advantage over traditional port-based maintenance approaches" and is "particularly suited for stellarators."

**Missing at scale**: Tritium extraction from PbLi at kg/day rates in a stellarator geometry. MHD effects in flowing PbLi under 3D magnetic fields. Corrosion of EUROFER97 in PbLi over 10-year exposure. The Stellaris paper identifies "further tritium blanket analyses, including simulating MHD effects in the PbLi, estimations of corrosion, simulation of tritium transport" as critical future work.

### **Island Divertor for Stellarator — TRL ~4–5**

**Demonstrated**: W7-X has operated an island divertor successfully since 2015, achieving stable detachment, radiative cooling, and steady-state heat exhaust at research-plasma power levels. The magnetic island structure at the plasma edge naturally creates flux-expansion surfaces ideal for distributing heat.

**On paper only**: Island divertor operation at commercial-plant power densities (4.05 MW/m² peak neutron wall load). The EMC3-Lite simulations for Stellaris assume 97% power capture and 60% radiative fraction, but the authors warn these "should not be mistaken for accurate heat flux predictions." Robust control in attached mode and access to stable detachment at high power remain to be demonstrated.

**Missing at scale**: Integrated divertor-blanket systems for stellarators. W7-X's divertor is uncooled carbon; Stellaris uses tungsten tiles backed by flowing coolant. Particle recycling, neutral compression, and pumping at 2.7 GW fusion power are unproven. The divertor system is not independent — it couples to edge physics, impurity transport, and fueling, all of which shift under power plant conditions.

### **Gyrotron ECRH Heating (170-240 GHz, steady-state) — TRL ~5–6**

**Demonstrated**: ITER-specification gyrotrons at 170 GHz, 1 MW continuous-wave (CW) are commercial products (e.g., Thales, Gycom). W7-X uses 10 gyrotrons at 140 GHz delivering up to 10 MW total.

**On paper only**: 230-240 GHz gyrotrons for optimal ECRH coupling at 14.4 T on-axis field. The Helios stellarator design (analogous QI concept) specifies 170 GHz ITER gyrotrons and extrapolates to Stellaris-class fields, but Stellaris's higher field would benefit from higher-frequency sources. Continuous-wave operation at 50 MW total power (startup) is within demonstrated capabilities, but <1 MW steady-state ignited operation depends on achieving high plasma gain.

**Missing at scale**: Long-term reliability (>10,000 hours) of high-frequency gyrotrons under continuous-duty commercial plant conditions. Transmission line and launcher integration for stellarator geometry. Cost at scale: ITER gyrotrons are ~$5-10M each; Stellaris would need 50-100 MW capacity (10-20 units for redundancy).

### **EUROFER97 Structural Steel (first wall / blanket) — TRL ~6–7**

**Demonstrated**: EUROFER97 is a Reduced Activation Ferritic/Martensitic (RAFM) steel developed for EU fusion programs. Material properties characterized up to ~50 dpa in fission reactors. DBTT shift and mechanical property evolution under neutron irradiation are extensively documented (though with large uncertainties for 14 MeV fusion neutron spectra).

**On paper only**: 10 full-power-year lifetime for first wall in a 2.7 GW stellarator. The Stellaris paper notes: "the safety margin relative to the yield strength limit might be exceeded" under peak neutron loading.

**Missing at scale**: Fabrication of complex stellarator-geometry first-wall modules from EUROFER97. Welding, forming, and quality assurance for 3D blanket cassettes. Long-term exposure to PbLi eutectic (corrosion, embrittlement). Alternative materials (High-Entropy Alloys, ODS steels) "could offer significantly improved performance... However, these materials currently have a lower technological readiness level (TRL)."

### **Remote Maintenance Systems (stellarator sector-split) — TRL ~3–4**

**Demonstrated**: ITER has developed full-scale remote handling prototypes for tokamak divertor and blanket exchange. Sector-based maintenance has been analyzed for stellarators (ARIES-CS proposed vertical extraction of 222 individual components through three ports, though this was identified as a maintenance nightmare).

**On paper only**: Stellaris's sector-split approach extracts entire toroidal sectors horizontally, accessing the plasma-facing surface without vertical ports. The concept is detailed in the Stellaris paper (10-step process) but has never been prototyped. Provisional estimate of 4-5 months for full blanket replacement drives the 90% availability target.

**Missing at scale**: Radiation-hardened robotics for stellarator geometry. Tooling for high-capacity cranes and sector extraction in a radioactive environment. Demonstration of <5-month turnaround time at commercial scale. Stellaris paper: "the feasibility of this manufacturing process will be the focus of subsequent studies."

### **Supercritical CO₂ Brayton Cycle (if used for balance-of-plant) — TRL ~6–7**

**Demonstrated**: sCO₂ Brayton cycles have been demonstrated at pilot scale in fossil and fission applications. Higher thermal efficiency (~45-50%) and compactness compared to steam Rankine. The Helios stellarator (comparable QI design) uses steam Rankine at ~40% efficiency; Stellaris's thermal conversion efficiency is not disclosed but ~32% overall plant efficiency (3.3 GW thermal → 1 GW electrical) implies either steam Rankine or sCO₂.

**On paper only**: Integration with pulseless steady-state fusion heat source. Stellaris would require ~3 GW thermal cycle.

**Missing at scale**: Gigawatt-scale sCO₂ plant deployment. Turbomachinery at fusion-plant inlet temperatures. If Stellaris uses steam Rankine instead, this subsystem drops to TRL 8-9 (mature).

### **REBCO HTS Tape Supply Chain — TRL ~7–8**

**Demonstrated**: REBCO tape is commercially produced (Faraday Factory Japan, Shanghai Superconductor Technology, CFS). Critical current density >150 MA/cm² at 20 K, 20 T is achieved in production tape. Proxima has secured REBCO supply from Faraday Factory Japan for SMC demo.

**Missing at scale**: Kilometers of tape needed for 50 full-scale coils. Radiation-hardened insulation and quench-protection systems for fusion neutron environments. Stellaris coils operate at 20 K (supercritical helium cooling at 15-20 bar), which is colder than typical HTS tokamak coils (20-50 K), increasing refrigeration cost but improving tape performance.

## 4. Key Materials and Supply Chain Considerations

### **REBCO Superconducting Tape (HTS)**

**Current production vs. plant-scale demand**: Global REBCO production capacity is on the order of thousands of kilometers per year. A single Stellaris plant requires tape for 50 unique coils, with winding packs of 225-324 turns per coil (total conductor length: order of tens of kilometers per coil, ~thousands of kilometers total). Scaling production by 10-100× for a fleet of plants requires massive capital investment in tape manufacturing.

**Cost trajectory**: Current prices are roughly $30-100/kA-m (highly variable by supplier and specification). CFS has driven REBCO costs down for SPARC; Proxima plans its own magnet factory, suggesting vertical integration or localized supply chain. The target is to reach ~$10/kA-m for commercial viability (tokamak benchmarks). Cost reduction depends on manufacturing learning curves and economies of scale, both of which are uncertain for REBCO given the technology's relative immaturity compared to LTS.

**Sole-source risks**: Only a few suppliers globally (Faraday Factory Japan, Shanghai Superconductor, SuperOx in Russia, and a few others). Geopolitical risks and export controls could constrain supply. Proxima's planned magnet factory (up to 1,000 jobs) suggests in-house winding capability, but tape production may remain external.

**Shared supply chains**: Commonwealth Fusion Systems, Tokamak Energy, Type One Energy, Thea Energy, and other HTS fusion companies all compete for the same REBCO supply. Non-fusion applications (high-field magnets for NMR, particle accelerators, maglev) add demand. The supply chain is expanding but remains a bottleneck for fleet deployment.

### **Lithium-6 Enriched Lead-Lithium (PbLi eutectic)**

**Current production vs. plant-scale demand**: Natural lithium is ~7.5% Li-6. WCLL blankets use eutectic PbLi (16 at% Li) with the lithium further enriched. The Stellaris paper does not specify enrichment level; EUROfusion DEMO targets 30-90% Li-6 enrichment for TBR optimization. A single plant requires hundreds of tonnes of PbLi (comparable to tokamak blanket inventories). Lead is commodity-scale; lithium enrichment is the constraint.

**Cost trajectory**: Lithium enrichment is currently performed in Russia and China using mercury-based COLEX process (banned in the West) or centrifuge enrichment (under development in the US). Costs are poorly characterized but estimated at $1000s per kg of enriched lithium. At plant scale, the blanket inventory cost is ~$10-50M (comparable to tokamak estimates), but the supply chain is underdeveloped.

**Sole-source risks**: Only a few enrichment facilities globally. US DOE is investing in domestic Li-6 enrichment to support fusion programs, but capacity remains limited. If a fleet of D-T fusion plants deploys, Li-6 enrichment could become a binding constraint unless capacity scales.

**Shared supply chains**: Fission molten-salt reactors (e.g., Kairos Power, Terrestrial Energy) use similar Li-7 depleted salts for neutron economy, creating potential synergy for enrichment infrastructure. However, D-T fusion is the only application requiring large quantities of Li-6, so the enrichment plant economics depend on fusion deployment scale.

### **EUROFER97 Reduced Activation Ferritic/Martensitic Steel**

**Current production vs. plant-scale demand**: EUROFER97 is not mass-produced; it is manufactured in small batches for fusion research programs (EUROfusion, ITER TBM campaigns). A single Stellaris plant would require hundreds of tonnes for blanket structure. The steel is an Fe-Cr-W-V-Ta alloy with controlled impurities to minimize long-lived activation products.

**Cost trajectory**: Specialty nuclear-grade RAFM steels are expensive (estimated $10-50/kg vs. $1-2/kg for commodity stainless steel). Scaling to commercial production could reduce costs via learning curves and larger heats, but RAFM will always carry a premium over standard steels due to composition control and traceability requirements.

**Sole-source risks**: Limited suppliers (specialized foundries in Europe and Japan that produce research quantities). Scaling to plant-construction rates requires investment in RAFM production capacity.

**Shared supply chains**: All D-T magnetic fusion concepts (tokamaks, stellarators) using RAFM blankets compete for the same supply. The Stellaris paper notes that alternative materials (High-Entropy Alloys, ODS steels) "could offer significantly improved performance... However, these materials currently have a lower technological readiness level (TRL)."

### **Tungsten (plasma-facing material)**

**Current production vs. plant-scale demand**: Tungsten is the universal plasma-facing material for D-T fusion (first wall, divertor). Global tungsten production is ~100,000 tonnes/year (dominated by China), adequate for a fusion fleet. However, fusion-grade tungsten (high purity, controlled grain structure, formed into monoblocks or tiles) is a specialty product.

**Cost trajectory**: Raw tungsten is ~$25-50/kg. Fabricated divertor tiles or first-wall armor are orders of magnitude more expensive (~$500-5000/kg) due to precision machining, bonding to heat sinks (CuCrZr), and quality control. ITER divertor procurement provides some cost benchmarks, but ITER pricing reflects one-of-a-kind fabrication. At scale, costs should decrease, but tungsten will remain a premium material.

**Sole-source risks**: China controls ~80% of global tungsten supply. Export restrictions or geopolitical tensions could constrain access. Western fusion programs are investing in tungsten supply-chain diversification.

**Shared supply chains**: All D-T fusion concepts (tokamaks, stellarators, mirrors) require tungsten armor. Fission advanced reactor programs (gas-cooled reactors with tungsten structural components) add demand, but fusion is the dominant application for high-purity specialty tungsten.

### **Tritium (fuel)**

**Current production vs. plant-scale demand**: Global civilian tritium inventory is ~25-30 kg, produced primarily as a byproduct of CANDU heavy-water reactors. A single D-T plant startup requires 1-5 kg tritium. As CANDU reactors retire, the external tritium supply will shrink. Stellaris targets TBR = 1.074, sufficient for self-sufficiency, but must bootstrap from external inventory.

**Cost trajectory**: Current market rate is >$30,000/g ($30M/kg). A Stellaris plant's initial inventory ($30-150M) is a modest capital cost, but the supply constraint is absolute: without tritium breeding, the plant cannot operate, and there is insufficient tritium to fuel more than a handful of first-generation plants.

**Sole-source risks**: Canada (CANDU reactors) is the primary source. US DOE has a small strategic reserve. Tritium decays at 5.5%/year, so inventory must be continuously replenished or bred.

**Shared supply chains**: Every D-T fusion concept (tokamaks, stellarators, IFE, MIF) competes for the same startup tritium. Tritium breeding is not optional for commercial deployment — it is the critical path to scaling beyond demonstration plants.

## 5. Design Point Parameters

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 12.0 m | stellaris-design-details.md §Overview, Table 2 | high | spec key: `R0` |
| a (minor radius) | 1.5 m | stellaris-design-details.md §Overview, Table 2 | high | spec key: `plasma_t` (canonical name for minor radius in library) |
| plasma_volume | 448 m³ | stellaris-design-details.md §Overview, Table 2; analyst-patch-spec-anchors.md | high | spec key: `plasma_volume` |
| elongation | 1.0 | analyst-patch-spec-anchors.md (typical for stellarators) | medium | spec key: `elon` |
| aspect_ratio | 8.0 | Computed: R0/a = 12.0/1.5 | high | informational |
| B (on-axis field) | 5.86 T | stellaris-design-details.md §Overview, Table 2; analyst-patch-spec-anchors.md | high | spec key: `B` (NOT `B0` — canonical name is `B`) |
| B_peak (on conductor) | 14.4 T | stellaris-design-details.md §Overview, Table 2 | high | informational — library uses on-axis B for ampere-meter quantity |
| peak_fusion_power_MW | 2700 MW | stellaris-design-details.md §Overview, Table 2 | high | informational — `p_fus` is back-solved by library from `p_input` + `P_native`; do NOT put `p_fus` in spec |
| peak_thermal_power_MW | 3300 MW | stellaris-design-details.md §Overview, Table 2 (includes blanket multiplier) | high | informational |
| net_electric_MWe | 1000 MW | stellaris-design-details.md §Overview, Table 2; dossier.md; analyst-patch-spec-anchors.md | high | drives `P_native` (and module count at 1 GWe comparison) |
| p_input_MW (auxiliary heating) | 50 MW | stellaris-design-details.md §Overview, Table 2 (ECRH); analyst-patch-spec-anchors.md | high | spec key: `p_input` — auxiliary heating wallplug, NOT fusion power. **Critical**: prior modeling errors set this to 2700 MW (fusion power), inflating LCOE to $303/MWh. Correct value is 50 MW ECRH at 230-240 GHz |
| peak_neutron_wall_load | 4.05 MW/m² | stellaris-design-details.md §Overview, Table 2 | high | informational |
| TBR (tritium breeding ratio) | 1.074 | stellaris-design-details.md §Breeding Blanket | high | informational — exceeds 1.05 viability threshold |
| availability_target | 90% | stellaris-design-details.md §Remote Maintenance (4.5-year cycle: 4 years operation + 4-5 months maintenance) | medium | informational — provisional, assumes 10-year first-wall lifetime and <5-month replacement |
| plasma_beta_volumetric | 2.76% | Inferred from dossier.md ("volume-averaged plasma beta ~2.76%") | medium | informational — stellarator beta values are typically quoted volume-averaged |
| conduction_power_to_coils_MW | 111 MW | stellaris-design-details.md §Overview, Table 2 | high | informational — heat leak to HTS coils at 20 K |
| blanket_power_multiplication | 1.17 | stellaris-design-details.md §Breeding Blanket (17% increase from neutron reactions in blanket) | high | informational |
| first_wall_lifetime_FPY | 10 | stellaris-design-details.md §Neutronics (DBTT-limited at 2700 MW fusion power) | medium | informational — drives 4-year replacement cycle |
| coil_lifetime_FPY | 10 | stellaris-design-details.md §Coils, Table 6 (99th quantile, neutron fluence limit for REBCO) | medium | informational — critical for capital amortization |
| plasma_coil_distance_min | 0.95 m | stellaris-design-details.md §Overview, Table 3 | high | informational — allows integrated blanket+shield |
| plasma_coil_distance_max | 1.37 m | stellaris-design-details.md §Overview, Table 3 | high | informational |
| num_modular_coils | 50 | stellaris-design-details.md §Coils | high | informational — each geometrically unique |
| HTS_operating_temperature | 20 K | stellaris-design-details.md §Coils (supercritical helium at 15-20 bar) | high | informational |
| blanket_type | Water-Cooled Lithium-Lead (WCLL) | stellaris-design-details.md §Breeding Blanket; dossier.md | high | informational — EUROFER97 structure, <550°C limit |
| divertor_type | Island divertor (W7-X heritage) | stellaris-design-details.md §Island Divertor; dossier.md | high | informational — tungsten tiles |
| structural_material_blanket | EUROFER97 | stellaris-design-details.md §Breeding Blanket, §Neutronics | high | informational — RAFM steel, <550°C operating limit |
| plasma_facing_material | Tungsten (W) | stellaris-design-details.md §Plasma Properties | high | informational — first wall and divertor |

## 5b. Override Candidates

```yaml
overrides: []
```

**Rationale for zero overrides:**

After walking the canonical 1costingFE account schema, **no company-grounded cost data justifies departing from library defaults**. The Stellaris paper and all public sources provide extensive physics and engineering parameters but explicitly defer economic analysis:

> "Economic aspects — including parasitic electricity consumption and availability — are outside the scope of this paper, but are paramount to assessing the feasibility of a commercial power plant."
> — stellaris-design-details.md §Introduction

The dossier provides no published dollar figures, unit costs, or vendor quotes for any CAS account. The Alpha demonstration plant budget (€2B) is a FOAK facility-construction estimate, not a decomposable NOAK cost basis for Stellaris components. The available data (coil dimensions, blanket composition, material fractions) enables physics-based library scaling but does not ground override values.

**Archetype-fit grade is High → expected override count is 0-4.** Zero enabled overrides falls within this band. If Proxima publishes detailed cost breakdowns (e.g., HTS coil fabrication quotes, blanket unit costs, BOP vendor estimates) in future iterations, overrides on C220103 (confinement magnets), C220101 (blanket), or CAS21 (buildings adapted to stellarator geometry) could be justified.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | LCOE estimate or detailed capital cost breakdown for Stellaris | S1, S2 | truly-unknown | blocking | Proxima investor materials, detailed engineering study, or ARIES-class systems analysis |
| 2 | HTS coil manufacturing cost (50 unique 3D coils, REBCO tape, winding fixtures) | S2 | truly-unknown | blocking | Magnet factory feasibility study, vendor quotes for HTS tape at scale, learning curve projections |
| 3 | Divertor heat flux control validation at 4 MW/m² (detachment, impurity seeding, steady-state) | S2, S3 | truly-unknown | important | Alpha demonstration data (if achieves high fusion power), high-power stellarator experiments |
| 4 | First-wall and coil lifetime under 14.1 MeV neutrons (DBTT shift, REBCO degradation) | S2, S3 | truly-unknown | important | Fusion-neutron test facility (IFMIF-DONES), accelerated irradiation campaigns |
| 5 | Remote maintenance turnaround time (sector-split, 4-5 month target) | S2, S3 | truly-unknown | important | Full-scale maintenance mockup, ITER remote handling lessons learned applied to stellarator geometry |
| 6 | Tritium extraction from PbLi in stellarator 3D magnetic geometry (MHD effects, corrosion, transport) | S2, S4 | not-yet-sourced | important | Blanket test program (TBM-equivalent for stellarators), MHD modeling benchmarked to experiments |
| 7 | Balance-of-plant thermal cycle choice (steam Rankine vs. sCO₂ Brayton) and efficiency | S5 | proprietary | nice-to-have | Full Stellaris paper (paywalled), Proxima conference presentations, Alpha BOP design |
| 8 | Primary heating method confirmation (ECRH frequency, gyrotron count) | S5 | proprietary | nice-to-have | Full Stellaris paper §Heating Systems, Alpha heating system procurement |
| 9 | Quench behavior and protection for 3D HTS coils under neutron flux | S3 | truly-unknown | important | SMC demonstration (2027), high-fidelity 3D quench modeling (acknowledged gap in Stellaris paper) |
| 10 | Manufacturing feasibility for complex 3D first-wall and blanket modules (EUROFER97 forming, welding, QA) | S3, S4 | not-yet-sourced | important | Fabrication trials, ITER blanket fabrication lessons learned, sector-split prototype |

## 7. Family-Delta vs Comparables

### **Comparable: 05 Planar-Coil Stellarator (Thea Energy)**

**Divergence**: **Magnet architecture — 3D non-planar coils vs. planar coil arrays**

Thea Energy (Helios design) uses 12 plasma-encircling "tokamak-like" coils plus 324 individually controllable planar field-shaping coils, all of which are flat and convex. This architecture enables conventional winding in tension, relaxed tolerances (errors corrected via control system), and modular mass manufacturing (all 324 shaping coils use identical inner/outer diameters).

Stellaris uses 50 modular coils with complex 3D non-planar geometry, each geometrically unique. This is the classic stellarator coil architecture (W7-X heritage, ARIES-CS legacy) optimized for plasma confinement quality but penalized by manufacturing difficulty.

**Cost implication**: **Planar coils (Thea) likely cheaper to manufacture; 3D coils (Proxima) likely require higher per-coil fabrication cost.**

Thea's architecture is explicitly designed for cost reduction: "all planar and convex, and can be wound in tension... tolerances are significantly relaxed as manufacturing and assembly errors can be corrected during operation." ARIES-CS (3D coils) faced "significant practical difficulty in designing, manufacturing, and assembling complexly curved, 3D coils to the required precision" and required a 3,000-ton structure "envisioned to be 3D printed on-site, as it was too big to transport."

Proxima's planned magnet factory (up to 1,000 jobs) and SMC demo (2027) suggest they believe the 3D coil challenge is surmountable, but this is a manufacturing bet against the planar-coil approach. The cost delta depends on whether Proxima achieves series production learning despite geometric uniqueness, or whether planar coils achieve a factor-of-few cost advantage.

**Neutral or shared**: Both use REBCO HTS tape at ~20 T. Both target ~1 GW net electric (Helios: 390 MWe, Stellaris: 1000 MWe). Both use lead-lithium breeding blankets (Helios: PbLi; Stellaris: WCLL). Both claim 40-year coil lifetimes via thick neutron shielding.

### **Comparable: 10 Large-Scale Stellarator (Gauss Fusion)**

**Insufficient public data on Gauss Fusion to articulate specific deltas.** Gauss Fusion is developing a large-scale stellarator but has not published a detailed power plant design comparable to Stellaris or Helios. The family-delta cannot be quantified without knowing Gauss's magnet type (HTS vs. LTS), coil architecture (planar vs. 3D), and scale targets.

### **Comparable: 20a Type-One Stellarator (Type One Energy)**

**Divergence**: **Modular coil approach vs. continuous-winding approach**

Type One Energy uses a modular coil architecture where individual coil cassettes can be manufactured off-site and assembled on-site. This approach trades plasma optimization (modular coils constrain the achievable field quality) for manufacturing simplicity and maintainability.

Stellaris uses 50 modular coils but each is a large, complex 3D structure (10.4 m tall, 9.9 m radial extent). These are not small cassettes — they are multi-ton assemblies requiring precision winding and on-site integration. The "modular" label for Stellaris refers to the number of discrete coils (50), not to plug-and-play replaceability.

**Cost implication**: **Type One's smaller modular cassettes likely easier to transport and replace; Stellaris's larger modular coils likely cheaper per unit volume but harder to handle.**

Type One's approach may reduce installation time and enable partial coil replacement without full device disassembly. Stellaris's approach optimizes for plasma performance (QI confinement quality) at the cost of coil complexity. The cost delta is ambiguous: Type One pays a multiplier for more coil units and more joints; Stellaris pays for precision fabrication of large 3D structures.

**Neutral or shared**: Both use HTS magnets. Both target D-T fuel. Both inherit stellarator advantages (steady-state, disruption-free).

### **Comparable: 20b Renaissance Stellarator (Renaissance Fusion)**

**Divergence**: **Laser-patterned HTS film on cylindrical arrays vs. REBCO tape in wound coils**

Renaissance Fusion uses laser-patterned HTS films deposited on rotating cylindrical surfaces, creating stellarator fields via current distribution in the film. This is a radically different manufacturing approach: no winding, no discrete coils, but requires precision laser ablation and superconducting film deposition at scale.

Stellaris uses conventional REBCO tape wound into discrete coils (flat-plate "radial" stacked concept). This is an extension of tokamak HTS coil technology to 3D geometry, inheriting the tokamak manufacturing base (CFS, Tokamak Energy).

**Cost implication**: **Manufacturing risk profiles are orthogonal — Renaissance bets on film deposition, Proxima bets on 3D winding.**

Renaissance's approach eliminates winding labor and potentially reduces conductor material (film can be patterned only where needed), but film deposition at fusion-scale dimensions is unproven. Proxima's approach uses demonstrated tape technology but faces geometric complexity. It is not obvious which is cheaper at scale; the answer depends on learning curves for two completely different manufacturing paradigms.

**Neutral or shared**: Both use HTS. Both are stellarators (disruption-free, steady-state). Renaissance also uses liquid-metal blanket (flowing Li-LiH wall + Pb pebble neutron multiplier), structurally different from Stellaris's WCLL but serving the same tritium-breeding function.

### **Comparable: 36 Helical-Coil Stellarator (Helical Fusion, HESTIA)**

**Divergence**: **Helical continuous coils vs. modular discrete coils**

Helical-coil stellarators (e.g., Large Helical Device in Japan, HESTIA concept) use continuous helical windings that wrap around the torus. This geometry is simpler to model and can be manufactured as a single continuous coil (or a small number of helical sections).

Stellaris uses 50 modular coils, each a discrete unit. Modular coils enable sector-split maintenance (Stellaris's key maintenance innovation) but complicate coil-to-coil field matching and increase the number of electrical connections and cryogenic interfaces.

**Cost implication**: **Helical coils likely simpler to manufacture; modular coils enable better maintenance access.**

Continuous helical coils reduce the number of high-current joints and cryogenic penetrations, potentially lowering both capital cost (fewer coil units) and operating cost (fewer failure points). Modular coils enable the sector-split maintenance approach, which Stellaris claims "offers a significant advantage over traditional port-based maintenance approaches." The cost-availability tradeoff depends on whether sector-split maintenance delivers the promised 4-5 month turnaround (reducing downtime and improving capacity factor) or whether coil modularity adds cost without sufficient availability benefit.

**Neutral or shared**: Both use HTS (if HESTIA adopts HTS; LHD uses LTS). Both are stellarators (steady-state, disruption-free). Both require tritium breeding for D-T operation.

## 8. Sources

Listed in order of importance:

1. **Stellaris Design Details** — `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` (342 KB)
   - Full Stellaris power plant concept (Fusion Engineering and Design Vol. 214, May 2025)
   - Comprehensive technical reference: plasma physics, magnets, breeding blanket, neutronics, divertor, first wall, remote maintenance, safety
   - Key parameters: 2.7 GW fusion, 3.3 GW thermal, 1 GW electrical, TBR 1.074, 90% availability target, 50 HTS coils at 20 T
   - Explicit future work gaps: economic analysis, divertor control validation, high-fidelity quench modeling, manufacturing feasibility
   - **Most comprehensive source for Stellaris design point**

2. **Proxima Fusion 2026 Updates** — `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md` (8 KB)
   - February 2026 MoU with RWE, Bavaria, and Max Planck IPP
   - Alpha demonstration plant: Q>1, €2B, operational 2031 in Garching
   - Stellaris commercial plant: Gundremmingen former nuclear site, later 2030s
   - Magnet factory plans: up to 1,000 jobs
   - European supply chain emphasis
   - **Primary source for commercialization timeline and partnership structure**

3. **Helios Stellarator Comparison** — `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md` (177 KB)
   - Thea Energy's Helios QI stellarator design (comparable architecture, different coil approach)
   - Key comparables: 390 MWe net electric, 958 MW fusion, 88% capacity factor, 40-year coil lifetime
   - Planar coil architecture (12 plasma-encircling + 324 planar shaping coils) vs. Stellaris's 3D non-planar coils
   - Advantages over ARIES-CS and modular-coil stellarators explicitly discussed
   - **Best reference for stellarator-specific cost drivers and manufacturing tradeoffs**

4. **Proxima Fusion Technology Page** — `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md` (4 KB)
   - Company technology overview: QI optimization, HTS magnets, island divertor, W7-X heritage
   - StarFinder optimization framework ("lower costs and higher speed than ever before")
   - Disruption-free steady-state operation emphasis
   - **High-level technology positioning, minimal quantitative data**

5. **Analyst Patch Spec Anchors** — `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md` (3 KB)
   - Verified parameter registry to prevent modeling errors
   - Documents critical error: prior modeling set `p_input = 2700 MW` (fusion power) instead of 50 MW (ECRH), inflating LCOE to ~$303/MWh
   - F9 validator enforces `p_input/P_native ≤ 0.5` to prevent regression
   - **Critical for LCOE modeling — prevents parameter mis-assignment**

6. **Dossier** — `knowledge/concept_research/09-qi-stellarator-hts/dossier.md`
   - Differentiation table values with citations and confidence ratings
   - Summary: QI stellarator, HTS REBCO magnets up to 20 T, WCLL blanket, 1 GW net electric, steady-state disruption-free operation
   - Medium-confidence gaps: primary heating (ECRH inferred), energy capture (thermal unspecified), plasma state (burning inferred), neutron management
   - **Consolidated metadata and gap inventory**

7. **W7-X Heritage** — Referenced in multiple sources (Proxima technology page, Stellaris paper)
   - Wendelstein 7-X: world's largest QI stellarator, operational since 2015
   - Demonstrated: QI confinement quality, island divertor, 8-minute steady-state plasmas
   - Proxima is Max Planck IPP spin-off, inheriting W7-X physics validation
   - **Physics basis for QI stellarator scaling to power plant**

8. **ARIES-CS Stellarator Study** — Referenced in Helios comparison
   - Late-2000s US stellarator power plant study (comparable to ARIES-AT for tokamaks)
   - Identified challenges: 3,000-ton coil structure (too large to transport), tight tolerances, 222-component serial maintenance
   - Stellaris and Helios designs explicitly address ARIES-CS shortcomings
   - **Historical stellarator cost modeling reference**

9. **EUROfusion DEMO WCLL Blanket Program** — Referenced in Stellaris paper
   - Water-Cooled Lithium-Lead blanket baseline for EU tokamak DEMO
   - TBR targets, EUROFER97 structural material, <550°C operating limit
   - Stellaris adapts WCLL to stellarator geometry
   - **Blanket technology heritage for D-T stellarators**

10. **Commonwealth Fusion Systems SPARC and Tokamak Energy Demo4** — Referenced in maturity assessment
    - SPARC: 20 T HTS tokamak TF coil demonstrated (CFS, 2024-2026)
    - Demo4: 11.8 T HTS in full tokamak configuration (Tokamak Energy, Nov 2025)
    - **HTS magnet technology validation at stellarator-relevant field strengths**
