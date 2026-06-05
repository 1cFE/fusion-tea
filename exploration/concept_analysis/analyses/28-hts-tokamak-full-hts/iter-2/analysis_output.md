## Design Point

**No design point selected upstream due to absence of HH380 specifications.** Energy Singularity's only power-producing machine (HH380 demo power station, planned post-2030) has zero publicly disclosed technical specifications — no net electric output, no geometry, no fusion power target, no subsystem designs. The model uses placeholder scale (500 MWe) per Section 6 recommendation, but this is an analogue assumption, not company-grounded data.

**Roadmap context**: Energy Singularity's disclosed machines are HH70 (experimental prototype, completed 2024, no fusion power), HH170 (Q > 10 demonstrator, planned 2027, no net electric output specified), and HH380 (demo power station, post-2030, zero engineering specifications available). The analysis documents what is known about HH70 and HH170 to characterize the technological approach, but Sections 5 and 5b reflect the fundamental limitation: without HH380 specifications, design-point parameters and company-grounded overrides cannot be provided.

---

## 1. Availability of Data

**Rating: Limited**

Energy Singularity has disclosed substantial technical detail about their experimental prototype HH70 and moderate detail about the physics target for HH170, but essentially no engineering specifications for their power plant concept HH380. The data landscape is highly skewed toward early-stage plasma physics validation and away from power plant design.

**What is publicly available:**

**HH70 prototype** (completed 2024): Comprehensive technical documentation exists across English and Chinese sources, including:
- Complete magnet system specifications (26 HTS coils: 12 TF, 6 PF, 8 CS; all REBCO)
- Demonstrated performance: 1,337-second steady-state plasma (shot #5,755, February 2026)
- Construction timeline and localization: ~95-96% domestic sourcing, built in under 2 years
- Operational tempo: ~100 shots/day vs. 20-30/day at JET
- Funding disclosed: ~$110M for HH70 construction

> "The successful operation of HH70 demonstrates the feasibility of full-HTS tokamaks and provides valuable engineering experience"
> — ScienceDirect abstract, Design and commissioning of HH70

**HH170 demonstrator** (planned 2027): Physics targets disclosed, engineering details sparse:
- Target: Q > 10 ("D-T equivalent" energy gain)
- Magnetic field: ~14 T on-axis, ~25 T peak field on D-shaped HTS magnets
- Size: ~90% diameter of SPARC, ~70% volume of SPARC, with ~110% of SPARC's field
- Funding target: additional $500M being raised
- **No power output, no blanket design, no energy conversion pathway disclosed**

> "Our goal is to reduce the levelized cost of electricity from fusion power to that of thermal power, or even lower"
> — Co-founder Dong Ge, iter-02/sources/energy-singularity-technical-summary.md

**HH380 power plant** (post-2030): Almost no technical information available:
- Designated as "demonstration fusion power station" in roadmap
- Timeline: construction starts after 2030
- **Zero engineering specifications public** — no geometry, no power level, no subsystem designs

**Independent validation:**
- Jingtian prototype magnet: 21.7 T peak field demonstrated (some sources report 22.4 T), validating HTS coil technology at HH170-relevant scales
- IAEA World Fusion Outlook 2025 features Energy Singularity's progress, providing third-party recognition

**What is structurally missing:**

Three research iterations spanning 20+ sources (English and Chinese) have confirmed the following gaps are **structurally unresolvable at current company stage**:

1. **Blanket design / tritium breeding**: No disclosure across any source. HH70 is experimental (no D-T, no neutrons), HH170 may not burn actual D-T fuel, and HH380 blanket engineering decisions haven't been made yet. China's CFETR program develops WCCB, HCCB, and sCO2-cooled LiPb blankets which could influence future choices, but no connection to Energy Singularity exists in public sources.

2. **Energy conversion pathway**: Generic D-T inference suggests thermal conversion (14.1 MeV neutrons), but specific cycle choice (Rankine vs. sCO2 vs. other) not disclosed for any machine.

3. **Neutron shielding approach**: No company-specific design available beyond physics-based inference from D-T fuel choice.

4. **Power plant scale and geometry**: HH380 net electric output not specified — the defining parameter for LCOE modeling.

5. **Heating systems for production machines**: HH70 uses ICRH (confirmed) and electron gun pre-ionization. HH170 and HH380 heating approaches not disclosed.

**Data quality:**
- HH70 data is **high quality** — multiple independent sources, peer-reviewed abstracts, third-party reporting
- HH170 data is **medium quality** — targets stated, but specifics thin
- HH380 data is **opaque** — essentially non-existent for engineering purposes

**Key data gaps for LCOE modeling:**
- No power output (P_native) for any machine
- No fusion power target for HH380
- No auxiliary heating power budget
- No blanket/shield radial build
- No first-wall/divertor specifications
- No capacity factor targets or maintenance schedule
- No component lifetime estimates under neutron loading

The dossier provides an excellent foundation for understanding Energy Singularity's **technological approach and development strategy**, but insufficient foundation for **power plant cost modeling** without substantial analogue-based inference.

---

## 2. Challenges in Capturing System Function

Energy Singularity's HTS tokamak concept presents both familiar tokamak modeling challenges and novel complications arising from data gaps and developmental stage. The challenges are ranked below by impact on LCOE uncertainty, not by technical difficulty.

**1. Unknown power plant scale (blocking challenge)**

No net electric output is specified for HH380, the only power-producing machine in the roadmap. Without P_native, the entire cost structure is indeterminate. Tokamak capital costs scale nonlinearly with size (larger machines have better confinement, lower recirculating power fraction, but higher absolute cost). The corridor between a 100 MWe pilot and a 1 GWe commercial plant spans at least an order of magnitude in specific capital cost ($/kW).

Energy Singularity's stated goal is "world's smallest and lowest-cost tokamak device capable of Q > 10" (iter-02 sources), suggesting compact design philosophy. HH170 is ~70% of SPARC volume with ~110% of SPARC field, implying high power density. But extrapolating from a non-power-producing demonstrator (HH170) to a commercial plant (HH380) without intermediate design points is highly uncertain.

**Uncertainty range**: Without stated P_native, the analysis must either assume a scale based on comparables (e.g., 500 MWe pilot plant) or model a range (100 MWe – 1 GWe). The LCOE sensitivity to this assumption is extreme.

**2. Tritium breeding pathway completely unknown (high impact)**

For a D-T tokamak, tritium breeding is not optional — global civilian tritium inventory is ~25 kg, and a 1 GWe plant requires >55 kg/year throughput. TBR > 1 is existential. Yet Energy Singularity has disclosed no blanket chemistry, no breeding approach, no materials choices for HH380.

China's national fusion program (CFETR) is developing water-cooled ceramic breeder (WCCB), helium-cooled ceramic breeder (HCCB), and sCO2-cooled LiPb blankets. Energy Singularity could adopt one of these, but:
- Each has different cost structure (solid breeder + Be multiplier + He cooling vs. liquid metal breeder/coolant)
- Each has different TBR margins and activation characteristics
- No public connection exists between Energy Singularity and CFETR blanket programs

The 1costingFE library has per-archetype blanket defaults, but these may not represent Energy Singularity's eventual choice. This gap affects CAS27 (special materials — blanket inventory), C220101 (first wall + blanket structure), and potentially C220102 (shield thickness if blanket provides partial shielding).

**Uncertainty range**: Blanket cost for a 500 MWe tokamak could range from ~$200M (FLiBe molten salt) to ~$500M (HCPB ceramic breeder with extensive Be multiplier), a factor of 2.5× on a major cost account.

**3. Full-HTS magnet cost scaling (high impact, moderate uncertainty)**

Energy Singularity's distinguishing feature is **all coils (TF, PF, CS) use REBCO HTS** — unique among tokamak concepts. Most HTS tokamak designs (CFS, Tokamak Energy) use HTS for TF coils only, with LTS or copper for PF/CS. Full-HTS offers:
- **Advantages**: Higher field everywhere, simpler cryogenic system (single 20 K refrigeration vs. dual 20 K + 4 K), potentially faster coil fabrication
- **Penalties**: REBCO tape is expensive (~$30-100/kA-m current pricing, target $10/kA-m for commercial viability); extending it to PF/CS increases tape consumption

HH70 TF coils use 450 m of conductor each × 12 coils = 5,400 m minimum for TF alone. PF and CS coil conductor lengths not disclosed. Jingtian prototype magnet (21.7 T) uses 32 stacked pancake coils and weighs ~7.5 tons — larger than HH70 coils, suggesting HH170/HH380 magnets will require substantial REBCO inventory.

The library's default HTS magnet cost model is calibrated to ARC-class designs (TF-only HTS). Energy Singularity's full-HTS approach may have:
- **Lower cost** if simplified cryogenics and domestic supply chain (96% localization) offset tape costs
- **Higher cost** if PF/CS tape consumption dominates and unit prices remain high

**Uncertainty range**: C220103 (confinement magnets) could range from library default (TF-only HTS analogue) to 1.5× default (full-HTS with high tape costs). This is a $200M – $600M swing for a 500 MWe plant.

**4. Plasma physics assumptions for HH380 (moderate impact)**

HH170 targets Q > 10 with ~14 T on-axis field in ~70% of SPARC volume. Scaling from HH170 (demonstrator, likely pulsed or quasi-steady) to HH380 (power plant, continuous operation) involves:
- Confinement scaling: Does HH380 maintain the compact high-field approach, or does it scale up in size for better confinement?
- Heating power: HH70 uses ICRH; HH170/HH380 heating not disclosed. NBI, ECRH, or combined systems have different cost and efficiency.
- Divertor heat flux: Compact, high-power-density tokamaks have severe divertor challenges. No HH380 divertor design disclosed.

**Uncertainty range**: Auxiliary heating (C220104) could range from ~$50M (ICRH-only at modest power) to ~$200M (NBI + ECRH for high-power steady-state). Recirculating power fraction depends on Q_eng, which depends on plasma performance not yet demonstrated.

**5. Construction time and learning curve (moderate impact on LCOE)**

Energy Singularity built HH70 in under 2 years (March 2022 design start to February 2024 assembly completion), described as "fastest superconducting tokamak construction" (iter-01 sources). This is a factor of 2-3× faster than Western tokamak timelines for comparable-scale machines. If this construction speed translates to HH380, it materially affects LCOE via:
- Lower interest-during-construction (IDC)
- Faster first-of-a-kind to nth-of-a-kind learning
- Lower labor costs (China's construction cost structure differs from US/EU)

However, HH70 is a small experimental device (R0 = 0.75 m). Scaling construction speed to a multi-GW power plant is uncertain. The LCOE model should test sensitivity to construction duration (2 years optimistic, 5 years baseline, 8+ years pessimistic) and to China-specific cost structures.

**6. Regulatory pathway and international deployment (low technical impact, high commercial impact)**

Energy Singularity operates in China under Chinese regulatory frameworks. If the concept targets international deployment (particularly US/EU markets), it faces:
- Technology transfer restrictions (HTS supply chain, IP licensing)
- Different regulatory cost structures (NRC vs. NNSA in US, national authorities in EU)
- Supply chain localization requirements

The dossier emphasizes 95-96% domestic sourcing and "independent intellectual property rights," suggesting a China-first deployment strategy. This affects the cost model's applicability to non-Chinese markets.

**Summary:**

The top three challenges — unknown plant scale, unknown tritium breeding, and full-HTS magnet cost — collectively dominate LCOE uncertainty. Until Energy Singularity discloses HH380 specifications, any LCOE estimate will be primarily driven by assumptions, not by company-grounded data. The per-account override walkthrough (Section 5b) will reflect this: few company-grounded overrides will be possible.

**LCOE context and expectations:**

Compact HTS tokamak concepts in the comparables set model in the range of ~60-120 $/MWh at 1 GWe NOAK (based on published estimates and industry consensus for CFS ARC-class designs and similar HTS tokamak concepts). This concept's library-default result at 1 GWe projection would be expected to fall within this corridor, subject to the following architectural effects:

- **Full-HTS advantage** (if REBCO tape costs fall to <$10/kA-m target): Simpler cryogenics (20 K only) and potentially lower magnet capital cost could drive LCOE toward the lower end of the corridor (70-90 $/MWh).
- **Full-HTS penalty** (if REBCO tape costs remain elevated at $30-100/kA-m): Higher conductor costs for PF/CS coils could drive LCOE toward the upper end or above (100-130 $/MWh).
- **China deployment advantage**: Domestic supply chain (96% localization), rapid construction (2-year timeline on HH70), and lower labor/fabrication costs could provide 15-25% LCOE reduction vs. Western comparables, potentially reaching 50-80 $/MWh for China-deployed plants.
- **International deployment penalty**: Export controls, technology transfer barriers, and supply chain rebuilding could increase LCOE by 20-40% vs. China deployment.
- **Blanket uncertainty**: Unknown tritium breeding approach (FLiBe vs. HCPB vs. LiPb) introduces ±10-20 $/MWh corridor width.

The modeled LCOE for this concept should be interpreted within this 50-130 $/MWh corridor, with the wide range reflecting REBCO price trajectory uncertainty, deployment geography, and unresolved blanket design. The placeholder 500 MWe scale assumption (Section 5) also affects the result — smaller pilot plants (200-300 MWe) typically show 1.3-1.8× higher LCOE than 1 GWe projections due to unfavorable economy of scale.

---

## 3. Maturity of Key Subsystems and Components

Subsystems are ranked in **ascending order of maturity** (least mature first), following the output template specification.

### Missing at commercial scale: Integrated D-T blanket + shield (TRL ~2 for this concept)

**Demonstrated**: Nothing. No blanket design for HH380 exists. HH70 is experimental (no D-T, no neutrons, no breeding). HH170 may not burn actual D-T fuel.

**On paper only**: Generic D-T tokamak blanket concepts exist (ITER TBMs, CFETR blanket studies), but no Energy Singularity-specific design has been published. The company has not stated which blanket family (solid breeder vs. liquid metal vs. molten salt) they will pursue.

**Missing at scale**: Everything required for a commercial D-T power plant:
- Tritium breeding blanket at TBR > 1
- 14.1 MeV neutron shielding protecting HTS coils
- First wall surviving MW/m² heat flux + neutron damage
- Tritium extraction and processing systems
- Remote maintenance for activated blanket modules

**Risk assessment**: This is the largest TRL gap for the concept. China's national CFETR program provides possible technology pathways (WCCB, HCCB, LiPb blankets), but no public connection between Energy Singularity and CFETR blanket development exists. The company's timeline (HH380 post-2030, commercialization before 2035) implies they must select and validate a blanket design within ~5 years — aggressive for a subsystem that has never been demonstrated in a commercial fusion environment.

### Missing at commercial scale: Steady-state divertor (TRL ~3–4)

**Demonstrated**: HH70 has operated for 1,337 seconds steady-state, but at low plasma current and low heat flux (no fusion). No divertor technology demonstrated at HH380-relevant power densities.

**On paper only**: Energy Singularity's compact high-field approach (HH170 is ~70% SPARC volume with ~110% SPARC field) implies high power density. High power density → high divertor heat flux. Standard tungsten monoblock divertors (ITER-style) are designed for ~10-20 MW/m² steady-state. Advanced divertor concepts (detached/radiative divertor, liquid metal divertor) exist in simulation and small-scale experiments but are unproven at scale.

**Missing at scale**: Divertor cassettes surviving >10 MW/m² steady-state heat flux for years of operation, with neutron damage accumulation, thermal cycling, and remote replacement capability.

**Risk assessment**: Compact tokamaks universally face divertor challenges. CFS/SPARC addresses this with advanced materials and active cooling; Energy Singularity has disclosed nothing. The 1costingFE library default for C220108 (divertor) assumes ITER-style W monoblock cassettes, which may underestimate cost if advanced divertor solutions are required.

### Demonstrated at component level: Full-HTS magnet system (TRL ~5–6)

**Demonstrated**:
- **HH70 magnets** (all 26 coils): 12 TF + 6 PF + 8 CS coils, all REBCO, operating at 20 K. Successfully demonstrated in integrated tokamak configuration with 5,755+ shots and up to 1,337-second pulses.
- **Jingtian prototype magnet**: 21.7 T peak field (some sources: 22.4 T) achieved in standalone test. 32 stacked REBCO pancake coils, ~7.5 tons, dimensions ~3 m × 1.4 m. Validates HH170 target field capability.
- **Supplier capability**: Shanghai Superconductor provides REBCO tape; 95-96% domestic component localization achieved on HH70.

> "The coil behavior agrees with engineering simulations"
> — ScienceDirect abstract on HH70 commissioning

**On paper only**: HH170 D-shaped HTS magnets targeting 25 T peak field. D-shaped geometry introduces higher mechanical stresses than HH70's circular coils. Structural design and quench protection for 25 T D-coils not yet demonstrated.

**Missing at scale**:
- Full-size HH380 TF coils at power-plant scale (likely larger than Jingtian magnet)
- Long-term reliability under neutron irradiation (HTS insulation radiation tolerance)
- Supply chain scaling: HH380 will require km-scale REBCO tape production at reduced unit cost

**Risk assessment**: This is Energy Singularity's **strength**. HH70 is the world's first fully HTS tokamak; Jingtian magnet exceeded CFS/MIT's 20 T record. The technology is demonstrated at component level and validated in integrated operation. The remaining challenges are engineering scale-up (larger coils, more tape) and cost reduction (REBCO tape must fall from ~$30-100/kA-m to <$10/kA-m for commercial viability).

**Cost implication**: C220103 (confinement magnets) is a candidate for company-grounded override **if** Energy Singularity publishes HTS tape procurement costs or magnet cost breakdowns. Current data is insufficient for a direct override, but the full-HTS architecture (TF+PF+CS) differs structurally from library defaults calibrated to TF-only HTS designs.

### Demonstrated at prototype scale: Steady-state plasma control (TRL ~6–7)

**Demonstrated**: HH70 achieved 1,337-second steady-state plasma (shot #5,755, February 2026) using AI-based plasma control system. Operational tempo of ~100 shots/day vs. 20-30/day at JET demonstrates robust control and rapid-turnaround capability.

**On paper only**: Scaling plasma control from HH70 (R0 = 0.75 m, B0 = 0.6 T) to HH380 (larger, higher field, burning plasma with alpha heating).

**Missing at scale**: Burning plasma control with real-time alpha power modulation, transient event handling, and disruption avoidance at commercial availability targets (>90%).

**Risk assessment**: Low to moderate. Steady-state operation is demonstrated at HH70 scale. The AI-based control system is an innovation that could accelerate learning on HH170/HH380, but burning plasma control remains undemonstrated by any tokamak worldwide (ITER will be the first). Energy Singularity faces the same challenge as all tokamak developers, with no obvious disadvantage.

### Demonstrated at laboratory scale: ICRH heating (TRL ~6–7 for the hardware, TRL ~3–4 for HH380 application)

**Demonstrated**: HH70 uses ICRH for plasma heating (confirmed). Electron gun provides pre-ionization.

**On paper only**: Heating system for HH170 and HH380 not disclosed. Could be ICRH (継続), NBI, ECRH, or combined.

**Missing at scale**: Steady-state auxiliary heating at the power levels required for HH380 (likely tens of MW) with >50% wall-plug efficiency and long-term reliability under neutron/gamma background.

**Risk assessment**: Moderate. ICRH hardware is mature for steady-state tokamaks, but HH380 heating approach is unknown. If Energy Singularity adopts NBI (common for compact high-field tokamaks), NBI systems have higher capital cost than RF systems. This affects C220104 (supplementary plasma heating).

### Mature: Cryogenic system for HTS (TRL ~7–8)

**Demonstrated**: HH70 operates all coils at 20 K (single-temperature cryogenic system). Large-scale helium refrigeration at 20 K is commercially available and less demanding than 4 K systems required for LTS.

**Missing at scale**: Scaling refrigeration capacity to HH380 (larger heat loads), but this is an engineering scale-up of mature technology, not a fundamental development challenge.

**Risk assessment**: Low. Simplified cryogenics (20 K only, no 4 K) is a cost advantage vs. LTS tokamaks and vs. hybrid HTS/LTS designs.

### Mature: Power supplies and control systems (TRL ~8–9)

**Demonstrated**: HH70 power supplies for 26 HTS coils. High operational tempo (100 shots/day) demonstrates reliable power supply performance.

**Missing at scale**: Larger power supplies for HH380, but DC power supply technology is mature. C220107 cost scales with magnet system power, not with technology novelty.

**Risk assessment**: Low.

### Mature: Vacuum vessel and structural support (TRL ~8–9)

**Demonstrated**: HH70 vacuum vessel constructed and validated. Domestic fabrication capability confirmed (96% localization).

**Missing at scale**: Larger vessel for HH380, but tokamak vessel fabrication is mature technology. China has extensive pressure vessel and nuclear component manufacturing capability (Hualong One reactor program, CFETR vessel).

**Risk assessment**: Low. C220105 (primary structure) and C220106 (vacuum system) should follow library defaults unless Energy Singularity discloses vessel innovations.

**Summary:**

The maturity profile is **bimodal**: HTS magnets, plasma control, and cryogenics are relatively advanced (TRL 5-8), while blanket/shield, divertor, and heating systems are early-stage or unknown (TRL 2-4). This is consistent with a company that has focused on **magnetic confinement physics** (HH70 validation) while deferring **power plant engineering** (HH380 design). The TRL gaps are not unique to Energy Singularity — all tokamak developers face blanket and divertor challenges — but the **lack of disclosed development path** for these subsystems is unusual for a company targeting commercialization before 2035.

---

## 4. Key Materials and Supply Chain Considerations

### REBCO superconducting tape (high criticality, moderate supply chain risk)

**Current state**: HH70 uses 450 m REBCO conductor per TF coil × 12 TF coils = 5,400 m minimum for TF. PF and CS coil lengths not disclosed but collectively comparable. Total HH70 conductor length likely ~10-15 km.

HH380 (larger machine, higher fields) will require substantially more: estimated 50-100 km for a 500 MWe tokamak based on ARC-class scaling.

**Supplier**: Shanghai Superconductor provides REBCO tape for HH70 (iter-01 sources). China has domestic REBCO production capability.

**Global supply chain**: Global REBCO production capacity is currently thousands of km/year (Shanghai Superconductor, Faraday Factory Japan, SuperPower in US, others). A single ARC-class tokamak requires >5,000 km. Energy Singularity's domestic supply chain (96% localization) positions them favorably within China's manufacturing ecosystem, but global supply scaling remains a constraint for fleet deployment.

**Cost trajectory**: Current REBCO pricing ~$30-100/kA-m. Commercial viability target: <$10/kA-m (per fusion industry consensus). Energy Singularity's construction cost advantage (HH70 built for ~$110M, extremely fast timeline) suggests access to favorable tape pricing or manufacturing efficiency, but no published unit costs exist.

**Supply chain risk**: **Moderate for China deployment** (domestic supplier, national industrial policy support). **High for international deployment** (export restrictions, technology transfer barriers). If Energy Singularity targets US/EU markets, REBCO supply becomes a strategic constraint.

**Cost implication**: C220103 (confinement magnets) is dominated by conductor cost. A 10× reduction in tape price (from $100/kA-m to $10/kA-m) could reduce C220103 by a factor of ~3-5×, a potential $300-500M swing for a large tokamak.

### Tritium (high criticality, shared constraint across all D-T concepts)

**Current state**: Global civilian tritium inventory ~25 kg (CANDU reactor byproduct). A 1 GWe D-T tokamak requires startup inventory ~1-5 kg plus >55 kg/year throughput at TBR > 1.

Energy Singularity has disclosed **no tritium breeding approach**, making tritium supply an unresolved strategic constraint.

**Supply chain risk**: **Existential if TBR < 1**. As CANDU reactors retire, external tritium supply shrinks. The first few D-T fusion plants must demonstrate tritium self-sufficiency before fleet scaling is possible.

**Cost implication**: Tritium fuel cost (CAS80) is driven by procurement cost (~$30,000/g for external supply, negligible if bred on-site) plus fuel cycle processing cost. More importantly, blanket design affects C220101 (blanket structure) and CAS27 (blanket materials inventory), together $200-500M for a 500 MWe plant depending on blanket chemistry.

Until Energy Singularity discloses blanket design, CAS27 and portions of C220101 cannot be overridden — library defaults will apply, but with low confidence.

### Lithium-6 enrichment (moderate criticality, limited global supply)

**Conditional on blanket chemistry**: If Energy Singularity adopts a lithium-bearing blanket (FLiBe molten salt, LiPb liquid metal, or Li-ceramic solid breeder), Li-6 enrichment is required for adequate TBR.

**Current state**: Natural lithium is ~7.5% Li-6, 92.5% Li-7. Breeding blankets require 30-90% Li-6 enrichment depending on design. Global Li-6 enrichment capacity is limited (Russia and China via mercury amalgam process banned in most countries; US/EU have small capacity).

**Supply chain risk**: **Low for China** (domestic enrichment capability exists). **Moderate for international deployment** (limited non-Chinese supply).

**Cost implication**: FLiBe cost is estimated ~$150/kg at scale (Araiinejad 2025 study), assuming 20% learning rate and 90% Li-6 enrichment. A 500 MWe tokamak might require 100-500 tons of FLiBe inventory (CAS27), a $15-75M cost item if FLiBe is the chosen blanket coolant.

### Beryllium (moderate criticality if Be multiplier or FLiBe blanket is chosen)

**Conditional on blanket chemistry**: Beryllium is used in two contexts:
1. **Neutron multiplier** in solid breeder blankets (HCPB-style): ~10-100 tons for a 500 MWe plant
2. **FLiBe molten salt** (Li₂BeF₄): ~30-150 tons for inventory depending on blanket thickness

**Current state**: Global Be production ~300 tons/year, dominated by US producer Materion Corp. Beryllium is toxic, expensive (~$800/kg), and has limited supply chain.

**Supply chain risk**: **Moderate**. Adequate for a single plant or small fleet, but fleet scaling (tens of reactors) would strain supply. China has domestic Be production but at smaller scale than US.

**Cost implication**: If FLiBe blanket: 100 tons Be × $800/kg × markup for FLiBe processing = ~$80-150M (CAS27). If HCPB blanket with Be multiplier: ~$30-80M. These are first-order estimates; Energy Singularity's lack of blanket disclosure prevents refinement.

### Tungsten (moderate criticality, adequate supply)

**Application**: First wall armor and divertor plasma-facing components.

**Current state**: Global tungsten production ~85,000 tons/year (China dominates supply). A 500 MWe tokamak requires ~10-50 tons of precision-fabricated tungsten tiles for first wall and divertor.

**Supply chain risk**: **Low**. Tungsten is commodity-available. The challenge is **manufacturing** (large-area tungsten tiles that survive heat flux and thermal cycling without cracking), not raw material supply.

**Cost implication**: C220108 (divertor) and portions of C220101 (first wall) include tungsten fabrication cost. Library defaults assume ITER-style W monoblock on CuCrZr heat sinks. Energy Singularity's compact high-field design may require advanced divertor solutions (higher cost), but no company data exists.

### Structural materials (low criticality, adequate supply)

**Application**: Vacuum vessel, blanket structure, shields, support structures.

**Candidates**: RAFM steels (EUROFER, CLF-1), austenitic stainless steels (316LN), or advanced alloys depending on neutron exposure.

**Supply chain risk**: **Low**. China has extensive steel manufacturing capability (produces >50% of global steel). RAFM steel production is limited globally but can be scaled if demand emerges.

**Cost implication**: C220105 (primary structure) and C220106 (vacuum vessel) are driven by fabrication complexity, not material cost. Domestic fabrication (96% localization on HH70) suggests favorable cost structure for Energy Singularity within China.

### Manufacturing and localization advantage

Energy Singularity's **96% domestic sourcing** and **rapid construction** (HH70 in under 2 years) indicate access to a mature Chinese supply chain for:
- HTS conductor (Shanghai Superconductor)
- Precision machining and coil winding
- Vacuum vessel fabrication
- Power supplies and control systems

This localization provides:
- **Cost advantage** vs. Western concepts relying on global supply chains with import tariffs and logistics overhead
- **Construction speed advantage** reducing IDC (interest during construction)
- **Learning curve potential** if China's industrial policy supports fusion manufacturing scale-up

**Risk**: The localization advantage is **China-specific**. International deployment would require rebuilding supply chains in target markets, increasing cost and timeline.

**Summary:**

The supply chain profile is **favorable for China deployment** (domestic REBCO, Be, W, steel; national industrial policy; fast construction) but **constrained for international deployment** (export controls, technology transfer, REBCO supply). The largest unresolved supply chain question is **tritium breeding** — without a disclosed blanket design, the feasibility of tritium self-sufficiency cannot be assessed, and CAS27 (blanket materials) and C220101 (blanket structure) remain library-default with low confidence.

---

## 5. Design Point Parameters

**Critical limitation**: Energy Singularity has disclosed no power output (P_native), no fusion power target, no geometry, and no subsystem specifications for HH380, the only power-producing machine in their roadmap. Section 5 cannot be completed to standard without a formally selected design point.

**What is known about machines in the roadmap:**

**HH70** (experimental prototype, completed 2024):
- Major radius R0: 0.75 m
- Minor radius a: ~0.25-0.31 m
- Aspect ratio A: ~2.4-3.0
- On-axis field B0: 0.6 T (plasma center)
- Peak field on coils Bmax: 2.5 T
- Not a power plant — no fusion, no D-T fuel

**HH170** (Q > 10 demonstrator, planned 2027):
- Target: Q > 10 ("D-T equivalent" energy gain)
- On-axis field B: ~14 T (inferred from "~110% of SPARC" statement)
- Peak field on coils: ~25 T (target for D-shaped HTS magnets)
- Size: ~90% diameter of SPARC, ~70% volume of SPARC
- Not a power plant — no net electric output specified

**HH380** (demo power station, post-2030):
- **Zero technical specifications publicly available**
- Timeline: construction starts after 2030
- Commercialization target: before 2035

**Implication**: Without HH380 specifications or a selected analogue machine, the parameter table below **cannot be populated** with company-grounded values. The analysis documents this gap.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | TBD | No data for HH380 | N/A | Power plant geometry not disclosed |
| a (minor radius) | TBD | No data for HH380 | N/A | Spec key: `plasma_t` |
| elongation κ | TBD | No data for HH380 | N/A | Spec key: `elon` |
| B (on-axis field) | TBD | No data for HH380 | N/A | Spec key: `B` (canonical name, not `B0`) |
| B_peak (on conductor) | TBD | No data for HH380 | N/A | Informational only; HH170 targets 25 T but HH380 may differ |
| fusion_power_MW | TBD | No data for HH380 | N/A | Informational only; not a spec key (library back-solves from `p_input` + `P_native`) |
| net_electric_MWe | TBD | No data for HH380 | N/A | Must equal P_native when P_native is selected |
| p_input_MW | TBD | No data for HH380 | N/A | Spec key: `p_input` — auxiliary heating wallplug power |
| Q_eng | TBD | No data for HH380 | N/A | Derives from fusion_power / p_input |

**Inference from HH170 (low confidence extrapolation):**

If HH380 scales from HH170 by a factor of ~2-3× in linear dimensions (common path from demonstrator to commercial plant), and maintains similar field strength:

| Parameter | Extrapolated Value | Basis | Confidence |
|-----------|-------------------|-------|------------|
| R0 | ~2.5-4.0 m | 2-3× scale-up from HH170 (which is ~70% of SPARC, SPARC R0 ~1.85 m, so HH170 R0 ~1.3 m) | Very low |
| a | ~0.8-1.3 m | Aspect ratio A ~3 typical for compact tokamaks | Very low |
| B | ~12-16 T | HH170 targets ~14 T; HH380 may increase or maintain | Very low |
| B_peak | ~22-28 T | HH170 targets 25 T peak field; HH380 may increase | Very low |
| net_electric_MWe | ~200-800 MWe | Compact tokamak range; pure speculation | Very low |

**These extrapolations are not company-grounded and should NOT be used for cost modeling.** They are included only to illustrate the scale of uncertainty.

**Recommendation**: The design point selection process should either:
1. **Assign HH380 a representative scale** (e.g., 500 MWe pilot plant) based on comparable tokamak concepts, **with explicit flagging that this is an analogue assumption, not company data**, or
2. **Model a range** (e.g., 200 MWe, 500 MWe, 1 GWe) to bound the corridor, or
3. **Defer cost modeling** until Energy Singularity discloses HH380 specifications

Without one of these paths, Section 5b (Override Candidates) cannot proceed.

---

## 5b. Override Candidates

**Critical limitation**: Override discovery depends on knowing the design point and scale. Without HH380 specifications or a selected P_native, the per-account walkthrough cannot produce company-grounded overrides. The analysis below documents what IS known and what CANNOT be overridden due to data gaps.

**Per-account walkthrough (canonical schema codes only):**

### C220101: First wall, blanket & neutron multiplier

**Company data**: None. Blanket design not disclosed.

**Library default**: Archetype-specific blanket cost model (likely FLiBe molten salt or HCPB ceramic breeder default for D-T tokamak).

**Override justified?**: **No**. Without knowing blanket chemistry, geometry, or materials, no company-grounded override is possible.

**Gap**: This is a $200-500M account for a 500 MWe tokamak. The uncertainty is a major cost corridor width driver.

### C220102: Radiation shield

**Company data**: None. Shield design not disclosed.

**Library default**: Shield thickness scaled to neutron wall loading (14.1 MeV neutrons for D-T fuel).

**Override justified?**: **No**. No company data.

### C220103: Confinement magnets (HTS-REBCO conductor + winding + cryostat)

**Company data**:
- HH70: 12 TF + 6 PF + 8 CS coils, all REBCO, operating at 20 K
- HH70 TF coil: 450 m conductor per coil, 3 double-pancake coils, 270 turns
- Jingtian prototype: 21.7 T peak field, 32 stacked pancakes, ~7.5 tons
- Supplier: Shanghai Superconductor (REBCO tape)
- 96% domestic component localization
- HH70 construction cost: ~$110M total (not magnets alone)

**Unique feature**: **All coils are HTS** (TF + PF + CS) — differs from library default calibrated to TF-only HTS designs.

**Override justified?**: **Potentially, but data insufficient for direct override**.

The full-HTS architecture changes the cost structure:
- **More REBCO tape** (PF + CS now HTS, not LTS or copper) → higher conductor cost
- **Simpler cryogenics** (single 20 K system, not dual 20 K + 4 K) → lower cryogenic CAPEX and OPEX
- **Domestic supply chain** (96% localization, Shanghai Superconductor) → potentially lower unit costs than Western pricing

To propose an override, we would need:
1. HH380 magnet conductor lengths (not disclosed)
2. REBCO tape procurement cost (not disclosed; current market ~$30-100/kA-m, target <$10/kA-m)
3. Full magnet system cost breakdown from Energy Singularity (not available)

**Conclusion**: **No override proposed** due to insufficient data. However, this account should be flagged for **sensitivity analysis** — varying the full-HTS cost multiplier (0.7× to 1.5× library default) would capture the architectural difference.

**Note for future**: If Energy Singularity publishes HH380 magnet costs or REBCO procurement contracts, this becomes the top override candidate.

### C220104: Supplementary plasma heating

**Company data**: HH70 uses ICRH (confirmed). HH170 and HH380 heating systems not disclosed.

**Library default**: NBI/ICRF/ECRH per installed MW, archetype-specific.

**Override justified?**: **No**. Heating approach for power plant unknown.

### C220105: Primary structure

**Company data**: HH70 constructed in under 2 years (March 2022 – February 2024), 96% domestic sourcing.

**Library default**: Archetype-specific primary structure cost.

**Override justified?**: **No direct override**, but construction speed and domestic supply chain suggest **favorable cost structure for China deployment**. This is a qualitative advantage, not a quantitative override without published cost data.

### C220106: Vacuum system

**Company data**: HH70 vacuum vessel constructed domestically.

**Library default**: Archetype-specific vacuum system cost.

**Override justified?**: **No**. No cost data.

### C220107: Power supplies (DC magnet supplies and switchgear)

**Company data**: HH70 power supplies for 26 HTS coils demonstrated. High operational tempo (100 shots/day) suggests reliable power supply performance.

**Library default**: Scales with magnet system power.

**Override justified?**: **No**. No cost or power rating data for HH380.

### C220108: Divertor

**Company data**: None. Divertor design for HH380 not disclosed.

**Library default**: W monoblock cassettes on CuCrZr heat sinks (ITER-style).

**Override justified?**: **No**. However, compact high-field design (HH170 is ~70% SPARC volume with higher field) suggests **high power density → severe divertor heat flux**. Advanced divertor solutions may be required, increasing cost above library default. This is a **risk flag**, not a grounded override.

### C220110: Remote handling & maintenance equipment

**Company data**: None. No maintenance approach disclosed for HH380.

**Library default**: Rad-hardening tier × vessel geometry.

**Override justified?**: **No**.

### C220111: Reactor equipment installation & assembly

**Company data**: HH70 assembled in under 2 years.

**Library default**: Fraction of CAS22 subtotal.

**Override justified?**: **Potentially yes, if construction speed translates to HH380**. Rapid construction reduces IDC and labor costs. However, without HH380 construction plan or cost breakdown, no quantitative override is justified.

**Note**: This account could be overridden **relative to library assumptions on construction duration** if the design point selection assumes faster construction (2-3 years vs. 5-7 year library default for FOAK tokamak). That's a scenario parameter, not a direct company override.

### CAS21: Buildings & site structures

**Company data**: None for HH380.

**Override justified?**: **No**, but China construction costs are generally lower than US/EU. If the cost model targets China deployment, a relative override (`0.6-0.8 × generic.costs.cas21`) might be justified based on **construction cost indices, not company data**. This is an **economic context adjustment**, not a company override.

### CAS23: Turbine plant equipment

**Company data**: None. Energy conversion pathway not disclosed (thermal cycle type unknown).

**Library default**: Thermal cycle; zero if direct-conversion.

**Override justified?**: **No**. Assume thermal conversion (D-T fuel → neutrons → thermal), but cycle type (Rankine vs. sCO2) unknown. Library default applies.

### CAS24: Electric plant equipment

**Company data**: None.

**Override justified?**: **No**.

### CAS26: Heat rejection system

**Company data**: None.

**Override justified?**: **No**.

### CAS27: Special materials (blanket fill / initial reactor inventory)

**Company data**: None. Blanket chemistry not disclosed.

**Library default**: Archetype-specific blanket materials inventory (FLiBe, Li-Pb, or Li-ceramic depending on default assumption).

**Override justified?**: **No**. This is a $15-100M account depending on blanket choice. Cannot override without knowing chemistry.

### CAS70: Annualized O&M + scheduled component replacement

**Company data**: HH70 operational tempo ~100 shots/day (vs. 20-30/day at JET) suggests efficient operations.

**Library default**: Staffing-based O&M model.

**Override justified?**: **No direct override**, but high operational efficiency is a **qualitative positive**. If HH380 maintains this efficiency, O&M costs could be lower than library default. However, without staffing plan or component replacement schedule, no quantitative override is possible.

### CAS80: Annualized fuel cost

**Company data**: None.

**Library default**: Negligible for D-T fuel (deuterium and external tritium procurement if TBR < 1).

**Override justified?**: **No**.

---

**Summary of override walkthrough:**

```yaml
overrides: []
```

**Zero enabled overrides.**

The lack of overrides is not due to close alignment between library defaults and company design — it is due to **absence of company data for HH380**. Every canonical account was considered; none have sufficient company-grounded evidence to justify an override.

**Sensitivity analysis recommendations** (in lieu of overrides):

1. **C220103 (magnets)**: Vary full-HTS cost multiplier (0.7-1.5×) to capture architectural difference
2. **C220101 + CAS27 (blanket)**: Model range of blanket chemistries (FLiBe, LiPb, HCPB) as scenarios
3. **CAS21 (buildings)**: Apply China construction cost index if modeling China deployment
4. **C220111 (installation)**: Vary construction duration (2 yr fast, 5 yr baseline, 8 yr slow) to reflect construction speed uncertainty

These are **scenario parameters**, not company overrides. They belong in the LCOE sensitivity suite, not in the override registry.

---

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | **HH380 net electric output (P_native)** — no power plant scale specified | S5 | truly-unknown | **blocking** | Unlikely to resolve until HH380 engineering phase (post-2030). Modeling recommendation: assign representative scale (500 MWe) based on compact tokamak comparables with explicit flagging as analogue assumption. |
| 2 | **Blanket design / tritium breeding approach** — chemistry, geometry, materials all unknown | S3, S4, S5b | truly-unknown | **blocking** | Unlikely to resolve until HH380 engineering phase. Possible connection to China CFETR blanket programs (WCCB, HCCB, LiPb) but no public link exists. Modeling recommendation: scenario analysis across blanket chemistries. |
| 3 | **HH380 geometry (R0, a, κ, δ)** — no major radius, aspect ratio, or shaping disclosed | S5 | truly-unknown | blocking | Same as gap #1. Could extrapolate from HH170 (~70% SPARC volume, ~14 T field) but confidence very low. |
| 4 | **Auxiliary heating approach for HH380** — HH70 uses ICRH, but power plant heating unknown | S3, S5 | truly-unknown | important | HH170/HH380 engineering publications when released. Affects C220104 cost. |
| 5 | **Energy conversion pathway** — thermal cycle type (Rankine vs. sCO2) not disclosed | S1, S3 | truly-unknown | important | HH380 engineering publications. China CFETR explores sCO2 cycles; possible technology sharing. |
| 6 | **Divertor design** — no disclosure for high-power-density compact tokamak | S3, S5b | truly-unknown | important | HH170/HH380 engineering publications. Compact high-field design implies severe divertor heat flux; advanced solutions may be required. |
| 7 | **REBCO tape procurement cost** — HH70 uses Shanghai Superconductor tape, unit cost not disclosed | S4, S5b | proprietary | important | Possible future disclosure in HH170/HH380 cost breakdown or in Chinese fusion industry publications. Current market pricing ~$30-100/kA-m; target <$10/kA-m. |
| 8 | **HH380 fusion power and Q_eng** — performance targets not disclosed | S5 | truly-unknown | important | HH170 targets Q > 10; HH380 likely higher but unspecified. Affects recirculating power fraction and net electric output. |
| 9 | **Neutron shielding approach** — generic D-T inference only, no company-specific design | S3, S5b | truly-unknown | nice-to-have | HH380 engineering publications. Affects C220102 cost if non-standard shield materials/geometry. |
| 10 | **First wall materials** — no disclosure beyond D-T inference (tungsten armor expected) | S3, S4 | truly-unknown | nice-to-have | HH380 engineering publications. Likely follows ITER baseline (W armor, RAFM structure) but uncertain. |
| 11 | **Capacity factor and maintenance schedule** — no targets disclosed | S2 | truly-unknown | important | HH380 operational plan when released. Affects LCOE via availability. |
| 12 | **Construction cost breakdown for HH70** — total cost ~$110M disclosed, but no account-level detail | S1, S5b | proprietary | nice-to-have | Possible future publication by Energy Singularity or academic partners. Would enable bottom-up validation of magnet costs. |
| 13 | **HH170 on-axis field B0** — inferred as ~14 T from "110% SPARC field" but not directly stated | S5 | derivable | nice-to-have | HH170 commissioning papers (2027+). Low priority; inference is reasonable. |
| 14 | **HH380 timeline and construction duration** — "post-2030" is vague | S2 | truly-unknown | nice-to-have | Corporate roadmap updates. Affects IDC and FOAK-to-NOAK learning timeline. |

**Summary:**

Of 14 identified gaps, **3 are blocking** (gaps #1, #2, #3 — scale, blanket, geometry), **8 are important** (affect major cost accounts or performance), and **3 are nice-to-have** (would improve confidence but not critical).

The blocking gaps are **structurally unresolvable** at current company stage (HH380 engineering decisions not made yet, timeline post-2030). The important gaps fall into two categories:
- **Truly-unknown** (company hasn't decided or hasn't disclosed): heating, energy conversion, divertor, performance targets
- **Proprietary** (company knows but hasn't published): REBCO tape cost, construction cost breakdown

**Modeling path forward**: Given the extent of blocking gaps, the cost model for this concept will be **heavily analogue-driven**. The recommended approach is:
1. **Assign representative scale** (500 MWe) based on compact tokamak comparables (CFS ARC, Tokamak Energy ST80)
2. **Use library defaults** for all accounts except where architectural differences are known (full-HTS magnets)
3. **Run scenario analysis** across blanket chemistries and construction contexts (China vs. international deployment)
4. **Flag the model as low-grounding-confidence** — this is a corridor map, not a company-validated cost estimate

---

## 7. Family-Delta vs Comparables

**Fixed comparables:**
- 01-hts-compact-tokamak (CFS ARC)
- 21-spherical-tokamak-hts (Tokamak Energy)
- 29-negative-triangularity-tokamak (Firefly Fusion, DIII-D derivatives)
- 33-state-backed-tokamak-best (Neo Fusion, ASIPP-class)

Energy Singularity's HTS tokamak concept sits in the compact/spherical tokamak family but with a unique architectural choice: **all coils (TF, PF, CS) use HTS**, not just the TF coils. The family-delta analysis below articulates how this differs from each comparable and the cost implications.

### vs. 01-hts-compact-tokamak (CFS ARC)

**Shared features:**
- Compact tokamak geometry (high field, small major radius)
- HTS REBCO conductor for TF coils enabling high on-axis field (ARC: 9-12 T nominal, 20 T peak field on conductor; Energy Singularity HH170: ~14 T nominal, 25 T peak)
- D-T fuel cycle
- Demountable or segmented magnets for maintenance access (ARC: demountable TF joints; Energy Singularity: not disclosed but HTS enables flexibility)

**Key divergences:**

1. **Full-HTS vs. TF-only HTS**:
   - **ARC**: HTS for TF coils, LTS (Nb3Sn or NbTi) for PF and CS coils
   - **Energy Singularity**: HTS (REBCO) for all 26 coils (12 TF + 6 PF + 8 CS)
   - **Cost effect**: **Ambiguous direction**. More REBCO tape (higher conductor cost) but simpler cryogenics (single 20 K system vs. dual 20 K + 4 K). If REBCO prices fall to <$10/kA-m, full-HTS could be cost-advantageous. At current pricing (~$30-100/kA-m), likely cost-penalty.
   - **Magnitude**: Potentially ±20-40% on C220103 (magnets) depending on tape cost trajectory.

2. **Supply chain and construction speed**:
   - **ARC**: Western supply chain (US/EU/Japan suppliers), conventional tokamak construction timelines (5-10 years FOAK)
   - **Energy Singularity**: 96% domestic Chinese supply chain, HH70 built in under 2 years
   - **Cost effect**: **Advantage** for Energy Singularity in China deployment context. Lower construction cost, faster delivery, reduced IDC.
   - **Magnitude**: Construction duration affects IDC (interest during construction). 2 years vs. 7 years at 8% WACC on $2B plant → ~$150M IDC saving. Plus lower Chinese labor/fabrication costs (rough estimate: 20-40% reduction on fabricated components).

3. **Blanket technology**:
   - **ARC**: FLiBe molten salt blanket (published design)
   - **Energy Singularity**: Unknown (no disclosure)
   - **Cost effect**: **Unknown**. If Energy Singularity adopts FLiBe (same as ARC), cost-neutral. If solid breeder (HCPB) or LiPb, different cost structure.
   - **Magnitude**: CAS27 + portions of C220101 could vary by $100-300M depending on blanket chemistry for a 500 MWe plant.

4. **Technology maturity and validation**:
   - **ARC**: SPARC under construction (TF magnet tested to 20 T, 2026), plasma operations expected late 2020s
   - **Energy Singularity**: HH70 operational (5,755+ shots, 1,337-second steady-state), HH170 planned 2027, HH380 post-2030
   - **Cost effect**: **Neutral to slight advantage** for Energy Singularity on magnet TRL (HH70 fully integrated, SPARC not yet operational). But ARC has more mature power plant design (published blanket, thermal conversion, divertor).
   - **Magnitude**: Lower development risk for magnets (already demonstrated in integrated tokamak), but higher risk for blanket/BOP (not designed yet).

**Net family-delta vs. ARC**:
- **Magnet architecture**: Full-HTS is a genuine innovation with ambiguous cost direction (depends on REBCO price trajectory)
- **Construction cost/speed**: Advantage in China, penalty if deploying internationally
- **Power plant engineering maturity**: Disadvantage (ARC has published reactor design; Energy Singularity does not)

### vs. 21-spherical-tokamak-hts (Tokamak Energy ST80)

**Shared features:**
- HTS magnets (both use REBCO)
- Compact geometry enabling high field
- D-T fuel cycle

**Key divergences:**

1. **Geometry: spherical vs. conventional aspect ratio**:
   - **Tokamak Energy ST80**: Spherical tokamak (aspect ratio A ~1.7-2.0), elongated plasma
   - **Energy Singularity**: Conventional compact tokamak (A ~2.4-3.0 based on HH70, likely similar for HH380)
   - **Cost effect**: **Ambiguous**. Spherical tokamaks have different cost tradeoffs (smaller major radius → smaller magnets, but higher engineering complexity for center column, higher neutron flux on inboard components).
   - **Magnitude**: Different scaling laws — cannot directly compare without full geometry.

2. **Full-HTS vs. TF-only HTS**:
   - **Tokamak Energy**: HTS for TF coils, unclear for PF/CS (likely LTS or copper)
   - **Energy Singularity**: Full-HTS (all coils)
   - **Cost effect**: Same as vs. ARC — ambiguous direction, depends on REBCO price.

3. **Supply chain geography**:
   - **Tokamak Energy**: UK-based, European/global supply chain
   - **Energy Singularity**: China-based, domestic supply chain
   - **Cost effect**: Advantage for Energy Singularity in China, neutral-to-penalty for international deployment.

**Net family-delta vs. Tokamak Energy**:
- **Geometry class**: Different physics (spherical vs. conventional) makes direct cost comparison difficult
- **Magnet architecture**: Full-HTS is a distinguishing feature, cost direction uncertain
- **Geographic context**: Cost advantage in China deployment

### vs. 29-negative-triangularity-tokamak (Firefly Fusion, DIII-D derivatives)

**Shared features:**
- Tokamak geometry
- D-T fuel cycle (assumed for Firefly)
- Advanced plasma shaping for improved confinement/stability

**Key divergences:**

1. **Negative triangularity vs. positive/neutral triangularity**:
   - **Firefly**: Negative triangularity (δ < 0) for improved H-mode access and divertor heat flux mitigation
   - **Energy Singularity**: Shaping not disclosed (HH70 appears circular or slightly D-shaped from images; HH170 described as D-shaped, suggesting positive δ)
   - **Cost effect**: **Potential advantage for Firefly** if negative triangularity enables simpler divertor (lower C220108 cost). Energy Singularity's compact high-field design implies high heat flux → expensive divertor solutions.
   - **Magnitude**: Divertor cost could vary by factor of 2× ($50M vs. $100M for 500 MWe plant) depending on heat flux mitigation strategy.

2. **Magnet technology**:
   - **Firefly**: Magnet technology not disclosed (likely HTS given industry trends, but unclear)
   - **Energy Singularity**: Full-HTS (demonstrated)
   - **Cost effect**: If Firefly uses HTS (TF-only), Energy Singularity's full-HTS is more aggressive. If Firefly uses LTS, Energy Singularity has higher magnet cost but simpler cryogenics.

3. **Developmental stage**:
   - **Firefly**: Early-stage (concept development, no hardware yet as of public info)
   - **Energy Singularity**: Operating prototype (HH70), demonstrated technology
   - **Cost effect**: Energy Singularity has demonstrated full-HTS in integrated tokamak → lower technical risk for magnets.

**Net family-delta vs. Firefly**:
- **Shaping strategy**: Negative-δ (Firefly) vs. positive-δ / high-field (Energy Singularity) represent different physics optimization paths with different divertor cost implications
- **Magnet TRL**: Advantage for Energy Singularity (demonstrated vs. concept-stage)

### vs. 33-state-backed-tokamak-best (Neo Fusion, ASIPP-class)

**Shared features:**
- State-backed development (China national fusion program for both)
- Access to domestic Chinese supply chain
- D-T fuel cycle

**Key divergences:**

1. **HTS vs. LTS magnets**:
   - **ASIPP-class (e.g., EAST, CFETR)**: LTS (Nb3Sn) for ITER-heritage machines
   - **Energy Singularity**: Full-HTS (REBCO)
   - **Cost effect**: **Trade-off**. HTS enables higher field (smaller machine for same performance), but REBCO is expensive. LTS has mature supply chain and lower conductor cost, but requires 4 K cryogenics.
   - **Magnitude**: C220103 (magnets) could be 1.5-2× higher for Energy Singularity at current REBCO prices, but 0.5-0.8× if REBCO prices fall to target (<$10/kA-m).

2. **Scale and development path**:
   - **ASIPP-class**: Large national programs (EAST R0 = 1.7 m, CFETR R0 ~6-7 m), gradual scale-up over decades
   - **Energy Singularity**: Compact machines (HH70 R0 = 0.75 m, HH170 likely R0 ~1.3 m, HH380 unknown but probably <3 m), rapid development (commercialization before 2035)
   - **Cost effect**: **Advantage** for Energy Singularity on construction speed and pilot-scale economics. Smaller machines have lower absolute capital cost (but higher $/kW if performance doesn't scale favorably).

3. **Blanket technology**:
   - **ASIPP-class**: CFETR develops WCCB, HCCB, sCO2-cooled LiPb blankets (national program)
   - **Energy Singularity**: Unknown (no disclosure, but possible technology sharing from national program)
   - **Cost effect**: **Potential advantage** if Energy Singularity adopts CFETR-developed blanket technology (de-risks blanket development, shares R&D cost). But no public connection exists.

**Net family-delta vs. ASIPP-class**:
- **Magnet technology**: HTS vs. LTS represents different technology bets — HTS enables compactness, LTS has mature supply chain
- **Development speed**: Energy Singularity's private-sector approach (faster iteration, commercial focus) vs. national lab approach (methodical, science-driven)
- **Possible technology sharing**: Both operate in China fusion ecosystem; blanket technology transfer from CFETR to Energy Singularity is plausible but unconfirmed

---

**Summary of family-delta:**

Energy Singularity's **full-HTS architecture** is the primary distinguishing feature — it is more aggressive than CFS (TF-only HTS), more demonstrated than Firefly (concept-stage), and fundamentally different from ASIPP-class (LTS-based). The cost implications are **ambiguous in direction** (depends on REBCO price trajectory) but **large in magnitude** (potentially ±30-50% on C220103 magnets).

The **China supply chain and construction speed** provide a cost advantage **in China deployment context** but become a constraint for international markets.

The **lack of disclosed power plant engineering** (blanket, divertor, energy conversion) makes Energy Singularity **less mature than CFS** at the reactor design level, despite having more mature magnet technology at the component level.

**For cost modeling purposes**, the comparables provide useful bounds:
- **Lower bound**: If Energy Singularity achieves China construction costs + low REBCO prices + technology sharing from CFETR blanket programs → cost-competitive with state-backed programs (33)
- **Upper bound**: If REBCO prices remain high + international deployment required + blanket development from scratch → cost-premium vs. CFS (01)

The corridor is wide due to data gaps and technology uncertainties.

---

## 8. Sources

Listed in order of importance:

1. **iter-01/sources/energy-singularity-overview.md** — Comprehensive technical compilation from multiple English and Chinese sources on Energy Singularity, HH70, HH170, Jingtian magnet, and company profile. Primary source for HH70 specifications (26 HTS coils, 0.75 m major radius, 1,337-second steady-state plasma, construction timeline, funding). Found in dossier research iteration 1.

2. **iter-02/sources/energy-singularity-technical-summary.md** — Xinhua News Agency report (February 2026) on HH70's 1,337-second plasma achievement and company goals. Source of quote: "Our goal is to reduce the levelized cost of electricity from fusion power to that of thermal power, or even lower" (co-founder Dong Ge). Confirms 96% localization rate and HH170 development acceleration.

3. **ScienceDirect abstract: "Design, commissioning, and first operation of HH70"** (Fusion Engineering and Design, 2025, DOI: 10.1016/j.fusengdes.2025.115341) — Peer-reviewed abstract confirming HH70 specifications (R0 = 0.7 m, a = 0.25-0.3 m, Bmax = 2.5 T, B0 = 0.6 T, 20 K operation). States "coil behavior agrees with engineering simulations" and "successful operation demonstrates feasibility of full-HTS tokamaks." Full paper paywalled; only abstract extracted.

4. **Xinhua: "Shanghai's 'artificial sun' achieves new tech breakthrough"** (February 2026) — https://english.news.cn/20260206/31e447b7e3504b0d802ef705556f66ef/c.html — Third-party validation of HH70 performance (1,337 seconds, shot #5,755, AI-based control). Cited in dossier.

5. **InterestingEngineering: "Energy Singularity seeks $500M"** — https://interestingengineering.com/energy/500m-target-record-holding-hh70-tokamak — Reports $500M fundraising target for HH170 development, HH70 construction cost ~$110M, company profile (135 employees as of late 2024).

6. **36kr: Chinese private enterprise fusion profile** — https://eu.36kr.com/en/p/3399945429878919 — Chinese tech media coverage of Energy Singularity's progress, domestic supply chain (Shanghai Superconductor), and commercialization timeline (before 2035).

7. **NextBigFuture: "World's First Fully HTS Tokamak"** — https://www.nextbigfuture.com/2024/07/worlds-first-fully-high-temperature-superconducting-tokamak-is-chinas-hh70.html — Early coverage (July 2024) of HH70 commissioning, confirms 26-coil all-REBCO design, provides HH170 targets (Q > 10, ~110% SPARC field).

8. **FusionEnergyBase: HH70 project page** — https://www.fusionenergybase.com/projects/hh70 — Community-maintained database entry with technical specifications, timeline, and key milestones.

9. **IAEA World Fusion Outlook 2025** — https://www-pub.iaea.org/MTCD/publications/PDF/p15935-25-02871E_WFO25_web.pdf — Features Energy Singularity's Jingtian magnet (21.7 T peak field, later sources report 22-22.4 T). Third-party international recognition of technology progress.

10. **ScienceDirect (paywalled): "Development and construction of magnet system for world's first full HTS tokamak"** — Full paper not accessed; likely contains detailed HTS coil design, manufacturing, and testing data for HH70. Referenced in dossier as potential future source.

11. **Dossier (knowledge/concept_research/28-hts-tokamak-full-hts/dossier.md)** — Consolidated differentiation table values with confidence ratings, gap analysis, and research iteration history (3 iterations, 20+ sources). Documents structurally unresolvable gaps (tritium breeding, HH380 specifications).

12. **Baseline concept CSV** — Initial company/concept identification in Phase 1a differentiation table.

**Note on source coverage:**

The sources provide **excellent coverage of HH70** (experimental prototype) and **moderate coverage of HH170** (physics targets stated, engineering details thin), but **near-zero coverage of HH380** (power plant design). Three research iterations spanning English and Chinese sources have exhausted publicly available information. Remaining gaps are structurally unresolvable — they depend on HH380 engineering decisions Energy Singularity hasn't made yet (timeline post-2030).

**Full commissioning papers (paywalled)** exist but were not accessed in this analysis. If critical cost-modeling questions remain, obtaining these papers via institutional access or direct request to Energy Singularity could resolve some HH70/HH170 design details, but would not resolve HH380 gaps (those papers do not exist yet).
