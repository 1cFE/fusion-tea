---
ID: 33-state-backed-tokamak-best
Concept: State-Backed Tokamak (Neo / ASIPP-class)
Company: Neo Fusion
Status: draft
Created: 2026-06-04
Approved-Date:
Confinement-Family: MFE
Archetype: TOKAMAK
Archetype-Fit: High
Comparison-Status: costingfe
Comparables:
  - 01-hts-compact-tokamak
  - 21-spherical-tokamak-hts
  - 28-hts-tokamak-full-hts
  - 29-negative-triangularity-tokamak
Design-Point-Name: ARIES-ACT1 advanced-physics / advanced-technology design (Kessel et al., Fusion Sci. Tech. 67 (2015))
Design-Point-Maturity: paper-concept
P-Native: 400
Grounding-Confidence: high
---

## Design Point

- Name: ARIES-ACT1 advanced-physics / advanced-technology design (Kessel et al., Fusion Sci. Tech. 67 (2015))
- Maturity: paper-concept
- P_native: 1000 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md
  - knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/best-research-plan-v1.1-summary.md

## 1. Availability of Data

**Rating: Rich**

The state-backed tokamak pathway benefits from extensive public documentation across multiple national fusion programs. The ARIES-ACT study (Kessel et al., Fusion Science and Technology 67:1, 2015) provides a comprehensive systems analysis of advanced tokamak power plants, including detailed geometry, physics performance, materials choices, and cost-of-electricity projections. This is one of the few fusion concepts with published COE estimates grounded in integrated systems modeling.

> "The ARIES-ACT study explores a wide parameter space by examining four 'corners' representing advanced and conservative choices for both physics and engineering/technology"
> — osti-servlets-purl-1178069.md §II

The ARIES-ACT1 variant specifically represents the advanced-physics / advanced-technology corner, targeting high normalized beta (βN = 5.75), high bootstrap current fraction (91%), and SiC composite blanket structures with self-cooled lead-lithium achieving 58% thermal conversion efficiency.

China's BEST (Burning Plasma Experimental Superconducting Tokamak) program provides additional context. The BEST Research Plan v1.1 (EUROfusion/ASIPP, November 2025) offers unprecedented transparency for a state-backed experimental facility, documenting:

- Complete magnet system specifications (hybrid Nb3Sn/YBCO, ~2000 tonnes total)
- Multi-method heating and current drive portfolio (~50 MW: ECRH, ICRH, LHCD, NBI)
- Test blanket module program validating three breeding concepts (COOL, WCCB, European TBMs)
- Tritium fuel cycle systems and 110g inventory requirements
- Materials testing protocols and post-irradiation examination plans

> "BEST is a burning plasma facility bridging the gaps towards ITER and CFEDR"
> — best-research-plan-v1.1-summary.md §Executive Summary

However, **cost data for CFEDR (the Chinese demonstration reactor) and commercial PFPP designs is sparse**. While CFETR power conversion studies (2021-2025) indicate sCO2 Brayton cycle selection achieving 34.7% efficiency, detailed capital cost breakdowns by CAS account are not publicly available. The ARIES-ACT study itself reports COE values (64.3 for reference case, range 64.3-67.0 for nearby operating points) but units are not specified in the available extraction.

**Key data gaps:**
- Published cost structure for CFEDR/PFPP at CAS22-level granularity
- Manufacturing cost data for hybrid LTS+HTS magnets at scale
- Component replacement schedules and costs for 5 FPY blanket lifetime
- Detailed O&M staffing models for state-backed vs. commercial operation

## 2. Challenges in Capturing System Function

The state-backed tokamak pathway faces challenges common to D-T magnetic confinement plus several unique to the advanced-physics operating regime:

**1. Divertor heat flux management (LCOE impact: high)**

The ARIES-ACT study identifies power scrape-off width as the dominant sizing constraint. Modern formulations predict 3-5 mm scrape-off widths, forcing larger machine size than earlier studies. Using current models, ARIES-AT would exhibit 22.6 MW/m² peak divertor heat flux versus the originally calculated 5 MW/m²:

> "Using the same formulation for ARIES-AT, the peak heat flux on the outboard divertor would be 22.6 MW/m², as opposed to the original 5 MW/m². ... This parameter, which increases the recirculating power associated with the H/CD system, and the treatment for the peak flux in the divertor both contribute to the larger plasma major radius for ARIES-ACT1 at 6.25 m compared with ARIES-AT at 5.20 m."
> — osti-servlets-purl-1178069.md §V.A

The uncertainty range is ±50%; if scrape-off widths prove narrower than predicted, ACT1 would require R > 7 m to maintain tolerable divertor loading. This single parameter can shift overnight capital by 20-30%.

**2. Advanced physics assumptions with limited experimental basis (LCOE impact: high)**

ACT1 depends on simultaneous achievement of:
- βN = 5.75 with wall stabilization
- H98 = 1.65 at Greenwald density
- 91% bootstrap current fraction
- Operation at/above Greenwald limit with maintained confinement

> "The energy confinements assumed here in combination with these n/nGr values are above those demonstrated experimentally. Some density peaking is assumed in all cases, with n(0)/⟨nT⟩ ranging from 1.3 to 1.5"
> — osti-servlets-purl-1178069.md §VI.A

No existing tokamak has demonstrated this combination. If H98 at Greenwald density degrades to 1.3 (still aggressive), required major radius increases ~15% and COE rises proportionally.

**3. Heating and current drive wall-plug efficiency (LCOE impact: medium)**

ARIES-ACT assumes 0.4 wall-plug efficiency for all H/CD systems, down from the 0.7-0.75 assumed in ARIES-AT. This drives recirculating power from 42.7 MW at ACT1 reference to potentially >60 MW if actual systems underperform. The range is 0.25-0.5 based on recent reviews:

> "In the ARIES-AT study, this parameter was generally taken to be 0.7 to 0.75. Recent reviews of this parameter indicate it is 0.4 for all sources (NB, EC, LH, and IC), with a range of 0.25 to 0.5"
> — osti-servlets-purl-1178069.md §V.A

Each 0.05 reduction in efficiency adds ~10 MW recirculating power, reducing net electric output and increasing LCOE by ~2%.

**4. Materials qualification without fusion neutron source (LCOE impact: medium)**

The 5 FPY blanket/first wall lifetime assumes 180 dpa radiation tolerance for RAFM steel or 3% burnup for SiC composites — "well above any fusion-relevant neutron exposure levels, since sources are scarce." No 14 MeV neutron facility exists to validate these limits at prototypical fluence. If actual limits prove half the assumed value (90 dpa for RAFM), replacement intervals halve and availability drops 5-10 percentage points.

> "Development of RAFM steel and extensions of new alloys to higher operating temperature and greater radiation resistance require testing with a fusion-relevant neutron source (especially the impact of higher He generation) to provide the needed database and lifetime projections."
> — osti-servlets-purl-1178069.md §VI.A

**5. Tritium burnup fraction and fuel cycle throughput (LCOE impact: low-medium)**

The tritium burnup fraction remains "a difficult parameter to accurately predict" with estimates ranging 1% (ITER) to 10% (optimistic). A 10× range implies 10× variation in required tritium injection/exhaust throughput, directly impacting fuel processing system capital cost ($50-500M range) and tritium inventory (1-10 kg).

**Ranked by LCOE sensitivity:**
1. Divertor heat flux / scrape-off width (direct sizing constraint)
2. Advanced physics performance shortfall (H98, βN, bootstrap fraction)
3. H/CD wall-plug efficiency degradation
4. Materials radiation tolerance / component lifetime
5. Tritium burnup fraction / fuel cycle throughput

## 3. Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first):

### SiC Composite Blanket Structure (TRL 2-3)

**On paper only:** ARIES-ACT1 blanket structure. Self-cooled PbLi with SiC composite achieving 1000°C maximum temperature and 58% Brayton cycle efficiency.

**Demonstrated:** Small-scale SiC/SiC composites irradiated in fission reactors to ~10 dpa with acceptable property retention. Non-nuclear mechanical properties characterized.

**Missing at scale:** Structural-grade SiC composites meeting fusion design requirements. Full-thickness structures (>10 cm) with complex internal cooling channels. Joining/welding techniques for field assembly. Irradiation database at 100+ dpa with 14 MeV neutrons and simultaneous helium generation.

> "SiC composites have still not reached the properties required for a structural material, in spite of significant developments and excellent nonnuclear and fission-irradiated performance. For nonstructural functions, such as flow channel inserts (in the core) or heat exchanger tubing (out of the core), SiC composite is a strong candidate."
> — osti-servlets-purl-1178069.md §VI.A

**Cost implication:** ACT1's cost advantage over ACT2 (conservative engineering with RAFM steel) hinges on SiC composites enabling high-temperature operation. If SiC fails to mature, fallback to RAFM-steel/DCLL drops thermal efficiency from 58% to ~45%, increasing required fusion power ~30% and major radius ~10%.

### Tritium Breeding Blanket Integration (TRL 3-4)

**Demonstrated:** Small-scale tritium breeding experiments (LIBRA/BABY with D-T neutrons). Helium-cooled pebble-bed and water-cooled lead-lithium mock-ups. Neutron irradiation to ~30-50 dpa in fission reactors. ITER TBM designs in detailed engineering (PDR expected 2026).

**On paper only:** Full-scale integrated blanket modules under simultaneous neutron + heat + tritium extraction + structural loads at fusion-relevant fluence (150-200 dpa lifetime).

**Missing at scale:** 14 MeV neutron testing facility. Industrial-scale lithium ceramic/liquid breeder fabrication. Tritium extraction at kg/day rates. RAFM or SiC structures proven under combined neutron + thermal + tritium environment.

BEST's TBM program tests three concepts (COOL CO2-cooled LiPb, WCCB water-cooled ceramic breeder, European WCLL/HCPB/WLCB) but at 15-40 MW fusion power, not the 1.8 GW required for ACT1:

> "A key long-term goal of the test blanket program is to generate foundational knowledge for assessing and managing the risks, costs, and lifecycle performance of breeding blanket systems."
> — best-research-plan-v1.1-summary.md §3.2.8

**Cost implication:** TBR < 1.05 would require external tritium supply (~5 kg/year at ~$30k/g = $150M/year operating cost) or breeding blanket redesign adding capital cost.

### Highly Radiating Divertor (TRL 4-5)

**Demonstrated:** ITER-style tungsten monoblock divertors tested at 10-20 MW/m² heat flux in facilities like WEST, GLADIS, DTT. Detached/radiative divertor operation (90% radiated power) demonstrated in DIII-D, JET, Asdex-Upgrade.

**On paper only:** 90% radiated power fraction in ACT1-specific geometry (strong target tilt or wide slot with perpendicular target) at 1.8 GW fusion power for 5 FPY without redeposition-induced property degradation.

**Missing at scale:** Long-pulse steady-state radiative divertor at GW thermal power. Remote replacement systems for activated divertor cassettes. Materials surviving 10-20 MW/m² steady-state + neutron damage + ~100 million ELMs over operational lifetime.

> "The highly radiating divertor regime is critical to the power handling for these power plants, and the validation of the simulation predictions with similar divertor geometric features (ITER-like strong target tilt or a wide slot with perpendicular target) and particle control would provide a more sound basis"
> — osti-servlets-purl-1178069.md §VI.A

> "It is found that the energy release per ELM must be reduced by a factor w10 to avoid melting of a tungsten-armored divertor, with the precise level determined by the inter-ELM heat flux. The elimination of ELM-like transients may be required even if the magnitude of the energy release can be reduced significantly, since a power plant will operate for ~1 year between routine maintenances and can accumulate w100 million ELMs."
> — osti-servlets-purl-1178069.md §VI.A

**Cost implication:** Divertor replacement interval is 5 FPY in ACT1 baseline. If ELM damage or erosion/redeposition forces 2-3 FPY replacement, availability drops ~5 percentage points and levelized replacement cost increases 50-100%.

### Tritium Fuel Cycle & Extraction (TRL 4-5)

**Demonstrated:** Lab-scale tritium handling loops, permeation barriers, extraction from liquid/solid breeders. JET and TFTR handled gram quantities. BEST plans 110g inventory with direct internal recycling (DIR) technology:

> "BEST operation represents an excellent opportunity for contributing to closing knowledge and know-how gaps"
> — best-research-plan-v1.1-summary.md §3.3

**On paper only:** Closed-loop kg/day scale self-sufficient fuel cycle with <1% losses.

**Missing at scale:** Industrial tritium processing plants. Low-inventory storage. Permeation-resistant materials at power-plant heat-exchanger throughput. Validated tritium accountancy at 1% loss tolerance (10 kg/year for ACT1 would exceed ITER's total startup inventory).

**Cost implication:** Tritium system capital cost estimated $50M (ARIES baseline). If actual cost scales with ITER's multi-billion-dollar system (even allowing for over-engineering), commercial plant cost could reach $200-500M.

### Remote Maintenance & Handling (TRL 5-6)

**Demonstrated:** ITER remote handling prototypes and full-scale mock-ups for blanket/divertor exchange. BEST planning includes:

> "Due to radiation risks after deuterium-tritium reactions, the system must perform all maintenance tasks entirely through remote handling"
> — best-research-plan-v1.1-summary.md §Chapter 3, §4

**On paper only:** Reliable high-availability (>80% availability) remote maintenance for commercial power plant with activated components.

**Missing at scale:** Radiation-hardened robotics operating inside vessel for years with minimal human intervention. Solid lubricant coatings for remote handling tools:

> "ultra-low outgassing rate solid lubricant coating materials (e.g., MoS₂, WS₂-based, graphite-based, MAX phase, DLC)"
> — best-research-plan-v1.1-summary.md §7

**Cost implication:** ACT1 assumes 12-18 month routine access with staggered sector changeout. If remote handling reliability forces annual shutdowns or extends outage duration 50%, capacity factor drops from 80% baseline to 70%, increasing LCOE ~14%.

### Heating & Current Drive Systems (TRL 6-8)

**Demonstrated:** MW-class gyrotrons (170 GHz), neutral beam injectors, RF systems routinely operated on existing tokamaks. ITER injectors under construction. BEST deploying 50 MW total (15 MW ECRH, 10 MW ICRH, 10 MW LHCD, 12 MW NBI) with upgrade path to 71 MW.

**Missing at scale:** Continuous-wave high-efficiency systems at 50-100 MW level with >50% wall-plug efficiency. ACT1 assumes 40% wall-plug; ITER H/CD systems target similar but have not demonstrated multi-year continuous operation.

**Cost implication:** H/CD capital cost scales ~$5-10M per injected MW. At 43 MW for ACT1, this is $200-400M capital. Efficiency degradation from 0.4 to 0.35 adds ~12 MW recirculating power, reducing Q_eng from 6.6 to 5.8 and net output by ~2%.

### Hybrid LTS+HTS Magnets (TRL 6-7)

**Demonstrated:** ITER-scale Nb3Sn TF coils in fabrication. BEST central solenoid combines Nb3Sn and YBCO achieving 18.8 T peak field in HTS sub-coils. Full-scale HTS magnets at 20 T tested (CFS SPARC prototype, January 2026). ACT1 uses Nb3Sn throughout at 11.8 T peak field (ITER-class).

**Missing at scale:** Reliable km-scale REBCO production with consistent Jc (>150 MA/cm² at 20 K, 20 T). Radiation-hardened insulation for neutron environments. Quench protection under combined high-field + cyclic loads.

> "The further development of the ITER low-temperature superconducting cable-in-conduit conductor design to enable higher fields and current densities should be pursued for next-step fusion facilities."
> — osti-servlets-purl-1178069.md §VI.A

**Cost implication:** BEST's hybrid approach (primarily Nb3Sn with YBCO only in CS high-field coils) is conservative. Full-HTS designs (CFS SPARC) enable compactness but at current REBCO prices (~$30-100/kA-m), magnets dominate capital cost. ACT1's Nb3Sn approach benefits from mature ITER supply chain.

### Balance of Plant (Power Conversion, Turbine, Heat Rejection) (TRL 7-8)

**Demonstrated:** Conventional Rankine/Brayton cycles at GW scale in fission and fossil plants. CFETR studies validate sCO2 Brayton achieving 34.7% efficiency (vs. 26.4% for steam Rankine):

> "S–CO₂ Brayton cycle is characterized by high efficiency, compact structure and low cost"
> — cfetr-power-conversion-studies.md §Introduction

ACT1 targets 58% via high-temperature (1030°C PbLi exit, 1000°C SiC max) Brayton cycle.

**Missing at scale:** Integration with fusion-specific heat sources. Tritium-compatible heat exchangers. High-temperature (1000°C) Brayton cycle demonstration — "not common in industrial power production, they need more attention to guarantee their reliable operation at a DEMO-stage facility."

**Cost implication:** BOP capital cost is typically 20-30% of overnight cost. Thermal efficiency directly gates required fusion power: 58% (ACT1) vs. 45% (ACT2) is 30% less fusion power for same electric output, enabling smaller major radius and lower CAS22 costs.

## 4. Key Materials and Supply Chain Considerations

### RAFM Steel (Reduced-Activation Ferritic-Martensitic)

**Current production:** EUROFER97 (EU), CLAM/CLF-1 (China), F82H (Japan) produced at <100 tonne/year globally in specialty nuclear-grade facilities. BEST blanket structures require "the same structural and functional material with CFEDR blankets" per TBM program requirements.

**Plant-scale demand:** ACT1 first wall, blanket, and divertor structural components total ~500-800 tonnes per reactor. At 5 FPY replacement interval, annual demand for a single plant is ~100-160 t/year. A commercial fleet of 10 reactors would saturate current global capacity.

**Cost trajectory:** Current RAFM cost is estimated $10-15/kg (nuclear-grade premium over commodity steel at ~$1/kg). At scale (10,000 t/year production), learning curves suggest $5-8/kg floor, but this requires dedicated manufacturing facilities with nuclear QA.

**Radiation tolerance gap:** Design limit is 180 dpa but fusion neutron database only extends to ~50 dpa. If actual limit proves 100 dpa (conservative), component lifetime drops from 5 FPY to ~3 FPY, increasing replacement frequency and availability penalty.

> "Development of RAFM steel and extensions of new alloys to higher operating temperature and greater radiation resistance require testing with a fusion-relevant neutron source (especially the impact of higher He generation) to provide the needed database and lifetime projections."
> — osti-servlets-purl-1178069.md §VI.A

### SiC Composite (Silicon Carbide Fiber-Reinforced Ceramic Matrix Composite)

**Current production:** Research-scale only. SiC/SiC composites manufactured by chemical vapor infiltration (CVI) or polymer infiltration and pyrolysis (PIP) at <1 tonne/year globally for aerospace and nuclear applications.

**Plant-scale demand:** ACT1 blanket structure (if SiC is used) requires ~200-300 tonnes initial inventory plus replacement. Not applicable to ACT1 baseline (RAFM steel) but critical to the ACT1 advanced-technology pathway.

**Cost trajectory:** Current cost is $500-2000/kg for nuclear-grade SiC/SiC. Manufacturing at scale (1000 t/year) could reduce to $100-300/kg, but no commercial CVI/PIP facility exists at this throughput. Fiber production (Nicalon, Hi-Nicalon S, Tyranno) is the bottleneck.

**Maturity risk:** ACT1 depends on SiC for 1000°C operation enabling 58% thermal efficiency. Current SiC composites "have still not reached the properties required for a structural material" per ARIES assessment. Fallback to RAFM steel reduces efficiency to ~45%, increasing fusion power requirement ~30%.

### Tungsten and Tungsten Alloys

**Current production:** ~8,500 tonnes/year globally, dominated by China (80% of world capacity). Nuclear-grade tungsten for plasma-facing components is specialty production at ~100 t/year.

**Plant-scale demand:** ACT1 divertor armor and first-wall protection tiles total ~40-60 tonnes per reactor. At 5 FPY replacement (divertor) or 10 FPY (first wall), steady-state demand is ~10 t/year per plant.

**Supply chain shared with:** Defense (kinetic penetrators), aerospace (rocket nozzles), lighting (filaments), and electronics (contacts). Tungsten price is volatile ($30-70/kg over 2015-2025) and supply dominated by single nation.

**Materials challenge:** "The nonnuclear properties of tungsten are not sufficiently well established, and the understanding of the impact of alloying for modifying its properties is very immature. The nuclear performance of tungsten in a fusion-typical neutron spectrum is also poorly understood."

ACT1 uses W-alloy in divertor structure and armor. Advanced oxide-dispersion-strengthened (ODS) RAFM steel is also planned for high-temperature divertor regions, adding another specialty alloy dependency.

### Lead-Lithium Eutectic (Li15.7Pb84.3 at 40% 6Li Enrichment)

**Current production:** PbLi eutectic is not commercially produced at scale. Lead is commodity (5 Mt/year globally); lithium is produced at ~100 kt/year.

**Plant-scale demand:** ACT1 PbLi inventory is ~800-1200 tonnes (estimate from blanket volume and density). With 40% 6Li enrichment, this requires ~50-75 tonnes of enriched lithium. A 10-reactor fleet requires 500-750 t enriched Li inventory.

**Cost trajectory:** Natural lithium is $15-30/kg (2024). Enrichment to 40% 6Li (from natural 7.5% 6Li) adds estimated $50-100/kg, bringing enriched lithium to $65-130/kg. Lead is $2/kg. PbLi eutectic at 40% enrichment is estimated $30-50/kg all-in. ACT1 inventory cost is ~$30-60M (one-time, not annual).

**Supply chain risks:**
- Lithium enrichment capacity is ~10 t/year globally (Russia, China mercury-based process). Scaling to 500 t/year for fleet deployment requires new enrichment facilities.
- Lead is commodity but PbLi eutectic fabrication with controlled isotopics and impurities (ppm oxygen, nitrogen) is specialty chemical engineering.

**Shared supply with:** Molten salt fission reactors (Kairos Power, Terrestrial Energy), which also require FLiBe and potentially enriched lithium. Shared demand may accelerate scale-up.

> "the eutectic's properties of constituency and evolution in prototypical environments (magnetic field, flow rates, heat and mass transfer, with hydrogen and helium production, and in thermal cycles) are not known. The complex thermofluid behavior requires better experimental demonstration, and simulation capability must improve."
> — osti-servlets-purl-1178069.md §VI.A

### Tritium

**Current global inventory:** ~25-30 kg civilian, produced as byproduct of CANDU heavy-water reactors at ~2-2.5 kg/year. CANDU fleet aging; production declining.

**Plant-scale demand:** ACT1 requires ~1 kg startup inventory (estimated) plus TBR > 1.05 to sustain operations. If TBR = 1.02 (within uncertainty), external makeup of ~0.5 kg/year required. At $30,000/g (current CANDU byproduct price), this is $15M/year operating cost.

**Fleet-scale constraint:** A 10-reactor fleet requires ~10 kg startup inventory, consuming ~40% of global civilian tritium. First few fusion plants must demonstrate TBR > 1.05 before fleet can scale. Tritium breeding is existential, not optional.

BEST's 110g inventory is for experimental operations, not power production. CFEDR and PFPP will require kg-scale inventories and self-sufficient breeding.

### Nb3Sn Superconductor

**Current production:** ~500-800 km/year globally for ITER TF coils, accelerator magnets, and MRI systems. Manufacturers: Luvata (Italy), Bruker (Germany), Western Superconducting (China), Furukawa (Japan).

**Plant-scale demand:** ACT1 TF coils (estimated from ITER scaling) require ~1000-1500 km Nb3Sn conductor per reactor. One reactor consumes 2-3 years of current global production.

**Cost trajectory:** Current ITER-grade Nb3Sn is $150-250/kg or $10-20/kA-m. At 10× scale-up (10,000 km/year for fleet deployment), learning curves suggest $80-120/kg floor. Tin and niobium are not supply-constrained; manufacturing capacity is the bottleneck.

**Alternative:** REBCO HTS tape (CFS/Tokamak Energy approach) has higher current density enabling compactness but costs $30-100/kA-m at current production and requires 12-20 T on-coil field. BEST's hybrid approach (Nb3Sn + YBCO in CS only) balances cost and performance.

### 6Li Enrichment Capacity

**Current capacity:** ~10 tonnes/year globally, primarily Russia and China using mercury-based COLEX process (banned in Western countries due to environmental hazard). Alternatives (laser isotope separation, ion exchange) are under development but not at commercial scale.

**Plant-scale demand:** ACT1 requires 40% 6Li enrichment (vs. natural 7.5% 6Li). Total lithium inventory is ~50-75 tonnes, consuming 5-7 years of current enrichment capacity for a single reactor.

**Fleet-scale bottleneck:** A 10-reactor fleet requires ~500-750 t enriched Li, or 50-75 years of current production. This is a binding constraint. Deployment requires:
1. Western enrichment facilities (non-mercury process)
2. 10-20× scale-up of global capacity
3. Or reduced enrichment requirement via improved blanket design (lower TBR margin = lower enrichment)

## 5. Design Point Parameters

**Design point:** ARIES-ACT1 reference case (1000 MWe net electric)

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 6.25 m | osti-servlets-purl-1178069.md §Table I | high | spec key: `R0` |
| a (minor radius) | 1.91 m | [inferred: A = R0/a = 3.27 from Table I; a = 6.25/3.27] | high | spec key: `plasma_t`. Inferred from aspect ratio A = 3.27 stated in Table I |
| elongation (κ) | 2.0 | osti-servlets-purl-1178069.md §Table I | high | spec key: `elon` |
| triangularity (δ) | 0.63 | osti-servlets-purl-1178069.md §Table I | high | spec key: `delta` |
| B0 (on-axis field) | 6.0 T | osti-servlets-purl-1178069.md §Table I | high | spec key: `B` (NOT `B0` — canonical name is `B`) |
| B_peak (on conductor) | 11.8 T | osti-servlets-purl-1178069.md §Table I | high | informational only — not a spec key |
| Ip (plasma current) | 10.9 MA | osti-servlets-purl-1178069.md §Table I | high | spec key: `plasma_current` |
| βN (total normalized beta) | 4.75 | osti-servlets-purl-1178069.md §Table I (thermal: 5.75 in abstract) | high | spec key: `beta_n`. Table I reports βN^tot = 4.75; abstract states thermal βN = 5.75 |
| H98 (confinement multiplier) | 1.65 | osti-servlets-purl-1178069.md §Table I | high | spec key: `h_factor` |
| q95 (safety factor) | 4.5 | osti-servlets-purl-1178069.md §Table I | high | informational only |
| n/nGr (density/Greenwald) | 1.0 | osti-servlets-purl-1178069.md §Table I | high | Operating at Greenwald density |
| fBS (bootstrap fraction) | 0.91 | osti-servlets-purl-1178069.md §Table I | high | 91% bootstrap current |
| fusion_power_MW | 1813 MW | osti-servlets-purl-1178069.md §Table I | high | informational only — `p_fus` is back-solved by library from `p_input` + `P_native` |
| net_electric_MWe | 1000 MWe | [design point specification] | high | drives `P_native` (and module count at 1 GWe comparison) |
| p_input_MW | 42.7 MW | osti-servlets-purl-1178069.md §Table I (H/CD power requirement) | high | spec key: `p_input` — H/CD wallplug power, NOT fusion power |
| Q_eng | 6.6 | osti-servlets-purl-1178069.md §Table I | high | Engineering Q = P_elec / P_recirc = 763 MW / 115.5 MW |
| thermal_efficiency | 0.58 | osti-servlets-purl-1178069.md §II, §IV.B.5 | high | 58% Brayton cycle with SiC/PbLi at 1030°C exit temp |
| average_neutron_wall_loading | 3.45 MW/m² | osti-servlets-purl-1178069.md §Table I | high | informational only |
| peak_divertor_heat_flux | 13.7 MW/m² | osti-servlets-purl-1178069.md §Table I | high | Baseline; range 10.5-14.7 MW/m² in operating zone |
| recirculating_power_MW | 115.5 MW | osti-servlets-purl-1178069.md §Table I | high | includes H/CD (42.7 MW) + pumping (~10-15 MW) + auxiliary (32 MW) |
| blanket_structure_material | SiC composite | osti-servlets-purl-1178069.md §II, §IV.B.1 | high | Advanced technology: SiC/SiC with self-cooled PbLi |
| blanket_breeder_coolant | PbLi (Li15.7Pb84.3, 40% 6Li) | osti-servlets-purl-1178069.md §IV.B.1, §IV.B.7 | high | Self-cooled lead-lithium eutectic |
| TBR (tritium breeding ratio) | 1.05 | osti-servlets-purl-1178069.md §IV.B.7 | high | With 40% 6Li enrichment |
| first_wall_lifetime_FPY | 5 | osti-servlets-purl-1178069.md §IV.B.7 | medium | Based on 180 dpa RAFM limit at 2.3 MW/m² average NWL |
| divertor_lifetime_FPY | 5 | osti-servlets-purl-1178069.md §IV.B.7 | medium | W-alloy + ODS RAFM steel; assumes ELM mitigation |
| structural_ring_lifetime_FPY | 20 | osti-servlets-purl-1178069.md §IV.B.7 | medium | Bainitic steel vacuum vessel |
| COE | 64.3 | osti-servlets-purl-1178069.md §Table III | medium | Units not specified; likely mills/kWh per ARIES convention. Operating zone range: 64.3-67.0 |

**Notes on confidence:**
- Geometric and physics parameters are "high" — directly from published tables
- Thermal efficiency (58%) is "high" — explicitly stated as Brayton cycle performance
- Component lifetimes are "medium" — based on assumed radiation limits (180 dpa RAFM, 3% burnup SiC) that exceed experimental database
- COE is "medium" — value is stated but units unclear, and detailed cost account breakdown not provided in available extraction

**Operating zone flexibility:** The ARIES study identifies that ACT1 has an operating space rather than a single point, with parameter ranges achieving COE within 5% of reference:
- R: 6.0 to 6.75 m
- BT: 5.25 to 7.25 T
- βN^tot: 4.0 to 5.0
- Peak divertor heat flux: 10.5 to 14.7 MW/m²
- Fusion power: 1813 to 2096 MW

This flexibility is a design advantage — allows trade-offs between lower divertor heat (10.5 MW/m² at R=6.75m) vs. smaller size (R=6.0m at 14.7 MW/m²) with minimal LCOE impact.

## 5b. Override Candidates

```yaml
overrides: []
```

**Walkthrough justification:**

The ARIES-ACT1 design point is a paper study, not a company-grounded commercial design. No override candidates are proposed because:

1. **No company data for any account** — The dossier sources are academic studies (ARIES-ACT) and a state-backed experimental program (BEST). Neither provides company-published dollar figures for commercial power plant subsystems.

2. **ARIES COE is reported but without account-level breakdown** — The study states COE = 64.3 (units unclear, likely mills/kWh) but does not decompose this into CAS21, CAS22, CAS23, etc. subcategories that would justify account-specific overrides.

3. **BEST is an experimental device, not a power plant** — The BEST Research Plan documents R&D programs and component specifications for a burning-plasma experiment, not commercial reactor costs. The statement "Identifying cost drivers and risk factors associated with procurement, fabrication, and licensing" indicates cost analysis is planned but not yet completed.

4. **CFEDR/PFPP cost data is not publicly available** — While CFETR power conversion studies indicate sCO2 Brayton cycle achieving 34.7% efficiency, no CAS-level capital cost breakdown for CFEDR or PFPP is documented in the available sources.

**Per-account review:**

- **C220101 (First wall, blanket):** ARIES reports 5 FPY lifetime and SiC/PbLi configuration but no dollar figure. No company override.
- **C220102 (Radiation shield):** No company-grounded cost data. No override.
- **C220103 (Confinement magnets):** BEST uses hybrid Nb3Sn/YBCO (~2000 tonnes total) but this is experimental scale. ACT1 uses Nb3Sn at 11.8 T (ITER-class). No published cost. No override.
- **C220104 (Supplementary heating):** ACT1 requires 42.7 MW H/CD at 0.4 wall-plug efficiency. BEST deploys 50 MW (ECRH/ICRH/LHCD/NBI) with upgrade to 71 MW, but these are R&D system costs, not commercial unit costs. No override.
- **C220105 (Primary structure):** Bainitic steel vacuum vessel (3Cr-3WV) at 350-500°C operating temperature. No published cost. No override.
- **C220106 (Vacuum system):** No company cost data. No override.
- **C220107 (Power supplies):** No company cost data. No override.
- **C220108 (Divertor):** W-alloy + ODS RAFM steel, 13.7 MW/m² peak heat flux baseline. 5 FPY lifetime stated but no cost. No override.
- **C220110 (Remote handling):** BEST documents remote handling requirements but no cost estimate. ARIES does not provide RH cost separately. No override.
- **C220111 (Reactor installation):** No company cost data. No override.
- **CAS21 (Buildings):** No company cost data. No override.
- **CAS23 (Turbine plant):** 58% Brayton cycle for ACT1; CFETR studies report 34.7% sCO2 efficiency and qualitative "low cost" but no quantitative dollar figure. No override.
- **CAS24 (Electric plant equipment):** No company cost data. No override.
- **CAS26 (Heat rejection):** No company cost data. No override.
- **CAS27 (Special materials):** PbLi inventory ~800-1200 tonnes at 40% 6Li enrichment, estimated $30-50/kg = ~$30-60M one-time cost. This is an analyst-derived estimate, not company-published. Provenance would be "derived" with low confidence. Not proposed as override because it lacks direct company sourcing.
- **CAS70 (O&M):** No company cost data. No override.
- **CAS80 (Fuel cost):** Tritium inventory 110g (BEST) or ~1 kg (ACT1 inferred). No published operating cost. No override.

**Override count:** 0 enabled overrides. This falls within the expected band (0-4) for High archetype-fit.

**Rationale for zero overrides:** The archetype fit is High because ARIES-ACT1 *is* a conventional tokamak with D-T fuel, thermal conversion, and magnetic confinement — it matches the 1costingFE archetype exactly. However, it is a **paper concept** without company-grounded commercial cost data. The library default story (built from ARIES-class studies and tokamak heritage) already represents this design point's cost structure. Overrides would only be justified if a state-backed program (e.g., CFEDR) published account-level budgets departing from ARIES assumptions, and no such data is available.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Published CAS-level cost breakdown for CFEDR/PFPP commercial reactors | S1, S5b | not-yet-sourced | important | China Fusion Energy Industry Consortium reports; CFEDR Preliminary Design Reports if declassified |
| 2 | Detailed O&M cost model (staffing, scheduled maintenance, unplanned outages) for state-backed vs. commercial tokamak operation | S1, S5b | not-yet-sourced | important | CFEDR operational planning documents; comparison with ITER operational budgets |
| 3 | Manufacturing cost data for hybrid LTS+HTS magnets at commercial scale (1000+ t Nb3Sn + partial REBCO) | S1, S3, S4 | not-yet-sourced | important | Supplier quotes from Western Superconducting, Luvata, or BEST magnet contractors |
| 4 | Component replacement schedule and costs for 5 FPY first-wall/blanket/divertor lifetime assumption | S1, S2, S3 | derivable | blocking | ARIES-ACT maintenance model (may be in full text not extracted); PROCESS code maintenance modules |
| 5 | Power scrape-off width λq experimental database and uncertainty quantification at ITER/DEMO-scale | S2, S3 | truly-unknown | blocking | ITER divertor physics program; DIII-D/JT-60SA/WEST high-power scaling studies |
| 6 | Advanced physics performance database: H98 = 1.65 at n/nGr = 1.0 with βN = 5.75 and wall stabilization | S2, S3 | truly-unknown | blocking | ITER high-performance scenarios; JT-60SA integrated advanced scenarios; future burning-plasma experiments (BEST Q~5 program) |
| 7 | Tritium burnup fraction and fuel cycle throughput at reactor-relevant conditions (10% vs. 1% range) | S2, S3 | truly-unknown | important | ITER D-T campaign; burning-plasma experiments (BEST, potential SPARC D-T operations) |
| 8 | SiC composite structural properties at 100+ dpa with 14 MeV neutrons and simultaneous He generation | S2, S3, S4 | truly-unknown | blocking (for ACT1 advanced-tech path) | Fusion neutron source (if built); continued fission irradiation + modeling |
| 9 | RAFM steel radiation tolerance limits at 150-200 dpa with fusion-spectrum neutrons (He generation) | S2, S3, S4 | truly-unknown | blocking | Fusion neutron source; BEST/CFEDR/ITER TBM post-irradiation examination programs |
| 10 | PbLi eutectic behavior under prototypical fusion conditions (MHD, corrosion, tritium transport, thermal cycling) | S2, S3, S4 | truly-unknown | important | BEST COOL TBM; WCLL TBM in ITER; dedicated liquid-metal test loops |
| 11 | Divertor erosion/redeposition and lifetime under 90% radiative power fraction with ~100 million ELMs | S2, S3 | truly-unknown | blocking | ITER D-T operations; DIII-D/JET/WEST high-fluence divertor campaigns |
| 12 | ELM suppression or mitigation to <10% of natural ELM energy for W-divertor survival | S2, S3 | truly-unknown | blocking | ITER ELM control demonstrations; resonant magnetic perturbation (RMP) optimization |
| 13 | H/CD system wall-plug efficiency at multi-year continuous operation (0.4 assumed; range 0.25-0.5) | S2, S3, S5 | derivable | important | ITER H/CD system performance; NBI/ECRH/ICRH vendor specifications from BEST/CFEDR procurement |
| 14 | Tritium system capital cost scaling from ITER (multi-billion $) to commercial plant (estimated $50M) | S2, S3, S4 | derivable | important | ITER tritium plant final cost; commercial simplification studies; CFEDR tritium system preliminary design |
| 15 | Remote handling system reliability and outage duration impact on capacity factor (80% baseline) | S2, S3, S5 | derivable | important | ITER remote handling demonstration program; JT-60SA maintenance experience; BEST remote handling development |
| 16 | 6Li enrichment capacity scale-up path from 10 t/year (current) to 500-750 t/year (fleet requirement) | S4 | not-yet-sourced | important (fleet-scale) | Non-mercury enrichment technology roadmaps; laser isotope separation feasibility studies; SHINE/Isologic/LiNa enrichment programs |
| 17 | Nb3Sn superconductor production scale-up from 500-800 km/year to 10,000 km/year for commercial fleet | S4 | derivable | nice-to-have (first plant OK) | ITER conductor procurement experience; supplier capacity expansion plans (Western Superconducting, Luvata, Furukawa) |
| 18 | High-temperature (1000°C) He Brayton cycle demonstration for 58% thermal efficiency validation | S3, S5 | not-yet-sourced | important (ACT1 advanced-tech) | sCO2 Brayton pilot plants; GFR (gas-cooled fast reactor) heat exchanger programs; CFETR power conversion R&D |

**Critical blocking gaps (without resolution, LCOE uncertainty is >50%):**
- #5: Power scrape-off width — directly sizes the machine
- #6: Advanced physics performance — βN = 5.75, H98 = 1.65 at Greenwald density undemonstrated
- #9: RAFM radiation tolerance — 5 FPY lifetime assumes 180 dpa, but database ends at ~50 dpa
- #11: Divertor lifetime under combined neutron + ELM + erosion
- #12: ELM control — without mitigation, W-divertor fails

**Important gaps (contribute 10-30% LCOE uncertainty):**
- #4: Component replacement costs
- #7: Tritium burnup fraction (1% vs. 10% is 10× fuel cycle throughput)
- #10: PbLi blanket behavior (MHD pressure drop, corrosion, tritium extraction)
- #13: H/CD efficiency (0.25-0.5 range is ±25% recirculating power)
- #14: Tritium system capital cost (factor of 5-10 uncertainty)
- #15: Remote handling availability impact

## 7. Family-Delta vs Comparables

**Fixed comparables:**
- 01-hts-compact-tokamak (CFS SPARC / ARC)
- 21-spherical-tokamak-hts (Tokamak Energy ST80-HTS)
- 28-hts-tokamak-full-hts (Energy Singularity HH70)
- 29-negative-triangularity-tokamak (Firefly)

### vs. 01-hts-compact-tokamak (CFS SPARC / ARC)

**Confinement geometry:** ARIES-ACT1 is conventional aspect ratio (A = 3.27) vs. SPARC compact design (A = 2.6, R = 1.85 m). ACT1 major radius is 6.25 m — more than 3× larger than SPARC. This is not a compactness difference; it is a scale difference.

**Magnet technology:** ACT1 uses Nb3Sn LTS throughout (11.8 T peak on-coil) vs. SPARC full-HTS REBCO (20 T on-axis field, 23+ T on conductor). The magnet cost structure is fundamentally different:
- ACT1: Mature ITER-heritage Nb3Sn at $10-20/kA-m, lower field, larger coils, cryogenic at 4 K
- SPARC: Immature REBCO at $30-100/kA-m, higher field, smaller coils, cryogenic at 20 K

**Cost effect:** SPARC's HTS magnets enable 3× smaller major radius, reducing CAS21 (buildings) and CAS22 non-magnet costs (vacuum vessel, blanket, shield). But REBCO unit cost is 3-5× higher than Nb3Sn, and SPARC's magnet mass per MW-electric may be similar to ACT1 despite compactness. **Net effect: uncertain — SPARC wins on building costs, ACT1 wins on magnet $/kg, total capital cost is trade-off between volume and unit cost.**

**Physics performance:** ACT1 assumes advanced physics (βN = 5.75, H98 = 1.65, 91% bootstrap) vs. SPARC conservative physics (βN ~3, H98 ~1, low bootstrap fraction with full current drive). ACT1 requires 42.7 MW H/CD for 1813 MW fusion; SPARC requires ~40-50 MW ICRF for ~140 MW fusion (rough scaling). **Cost effect: ACT1's advanced physics reduces H/CD cost per MW-fusion but increases physics risk. If ACT1 falls short (H98 = 1.3), major radius increases 15% and cost rises proportionally.**

**Blanket technology:** ACT1 uses SiC/PbLi self-cooled blanket achieving 58% thermal efficiency vs. SPARC baseline (likely DCLL or water-cooled with ~40-45% efficiency). **Cost effect: 58% vs. 45% efficiency is 30% less fusion power for same electric output. If ACT1's SiC composites fail to mature, fallback to RAFM/DCLL (45%) erases the advantage and ACT1 becomes larger and more expensive than baseline tokamak. This is ACT1's highest technology risk.**

**Delta summary:** ACT1 vs. SPARC is conventional-scale advanced-physics LTS tokamak vs. compact conservative-physics HTS tokamak. ACT1 bets on materials (SiC) and physics performance (high βN, high H98) to compensate for larger size; SPARC bets on magnets (HTS) to shrink the machine. **Advantage: conditionally SPARC** (compactness is lower-risk than SiC composites), unless ACT1's physics assumptions prove achievable and SiC matures.

### vs. 21-spherical-tokamak-hts (Tokamak Energy ST80-HTS)

**Aspect ratio:** ACT1 conventional tokamak (A = 3.27) vs. ST80 spherical tokamak (A < 2, estimated A ~ 1.6-1.8). Spherical tokamaks achieve higher β at lower field due to favorable geometry but require internal central solenoid or CS-free startup.

**Magnet configuration:** ST80 uses demountable HTS magnets enabling maintenance access vs. ACT1 welded Nb3Sn TF coils requiring sector-based remote handling. **Cost effect: ST80's demountable magnets simplify maintenance (contact maintenance feasible for some components, reducing RH capital cost ~20-30%) but add complexity and potential field errors at joints.**

**Divertor geometry:** Spherical tokamaks have unfavorable divertor geometry — tight radial build at inboard, limited space for divertor cooling. ST80 will face higher peak heat flux per MW-fusion than ACT1. **Cost effect: ST80 may require more frequent divertor replacement or advanced cooling (He/sCO2 jet impingement), increasing CAS22 blanket/divertor costs.**

**Net electric output at given size:** Spherical tokamaks achieve higher power density (MW-electric per unit major radius). ST80 at R ~ 1.5-2 m targets hundreds of MWe vs. ACT1 at R = 6.25 m producing 1000 MWe. **Cost effect: ST80 has lower absolute capital cost (smaller machine) but potentially higher $/kWe if divertor and maintenance challenges dominate.**

**Delta summary:** ACT1 vs. ST80 is conventional-geometry large-scale vs. spherical-geometry compact. ST80 wins on capital cost absolute magnitude (smaller machine = lower CAS21, CAS22 non-magnet). ACT1 wins on divertor power handling and potentially $/kWe at GW scale. **Advantage: ST80 for modular deployment (hundreds of MWe plants), ACT1 for GW-scale baseload** (economies of scale favor large conventional geometry at GW output).

### vs. 28-hts-tokamak-full-hts (Energy Singularity HH70)

**Magnet technology:** Both use superconducting magnets but ACT1 is LTS (Nb3Sn) vs. HH70 full-HTS (REBCO). HH70 benefits from higher field, smaller coils, and 20 K cryogenic (less refrigeration power than 4 K). **Cost effect: same as SPARC comparison — HTS enables compactness but unit cost is 3-5× higher.**

**Physics assumptions:** ACT1 advanced physics (βN = 5.75, H98 = 1.65) vs. HH70 not publicly specified but likely more conservative (China's fusion program historically uses ITER-class assumptions). **Cost effect: if HH70 uses H98 ~ 1.0-1.2, it requires proportionally more H/CD power or larger size than ACT1, erasing HTS compactness advantage.**

**Blanket technology:** ACT1 SiC/PbLi (58% efficiency) vs. HH70 not specified but likely RAFM/water-cooled or RAFM/He-cooled (40-45% efficiency based on CFETR lineage). **Cost effect: same as SPARC — ACT1's thermal efficiency advantage (58% vs. 45%) compensates for size disadvantage, conditional on SiC maturity.**

**State backing:** Both are state-backed programs (US DOE supported ARIES studies historically; China's BEST/CFEDR/HH70 lineage is CAS + CNPC funded). **Cost effect: state backing may reduce financing costs (lower WACC) and enable higher risk tolerance for unproven technologies (SiC composites, advanced physics), but may also introduce inefficiencies vs. commercial programs.**

**Delta summary:** ACT1 vs. HH70 is LTS-conventional vs. HTS-compact within the same state-backed development model. **Advantage: uncertain** — depends on whether HTS supply chain matures faster than SiC composites. If both technologies mature, HH70 wins on compactness; if neither matures fully, fallback designs are similar (RAFM/DCLL, Nb3Sn at moderate field).

### vs. 29-negative-triangularity-tokamak (Firefly)

**Plasma shaping:** ACT1 uses positive triangularity (δ = 0.63) vs. Firefly negative triangularity (δ ~ -0.3 to -0.5). Negative triangularity improves confinement at lower current/field and may enable higher power density without ELMs.

**ELM control:** ACT1 requires ELM suppression (RMP or other) to avoid W-divertor damage over ~100 million ELMs per year. Negative triangularity may naturally operate ELM-free. **Cost effect: if negative-δ eliminates ELMs, divertor lifetime extends from 5 FPY (ACT1 with ELM mitigation) to 10+ FPY, reducing replacement cost 50% and improving availability 3-5 percentage points.**

**Physics database:** Positive triangularity is standard tokamak configuration with 40+ years of data (JET, DIII-D, ASDEX-U, ITER). Negative triangularity is recent innovation with limited high-performance database (DIII-D experiments since 2020s). **Cost effect: ACT1 physics is risky but well-characterized; Firefly physics is risky and poorly-characterized. Uncertainty is higher for Firefly.**

**Blanket and heating:** Likely similar — both D-T tokamaks with RF/NBI heating. **Cost effect: neutral.**

**Delta summary:** ACT1 vs. Firefly is conventional-shaping advanced-physics vs. novel-shaping potentially-simpler-physics. **Advantage: conditionally Firefly** — if negative triangularity proves ELM-free and achieves adequate confinement, it eliminates ACT1's biggest divertor risk. But negative-δ database is thin; ACT1 has 40 years of tokamak heritage. **Risk-adjusted: ACT1 is lower physics risk, Firefly is higher physics risk but higher reward (ELM-free).**

### Cross-Cutting Observations

**All four comparables use HTS magnets; ACT1 uses LTS.** This is the sharpest delta. HTS enables compactness (01, 21, 28) or potentially higher power density (29). ACT1's LTS approach is conservative and benefits from mature ITER supply chain, but sacrifices the size reduction HTS offers.

**ACT1's thermal efficiency (58%) is likely highest among comparables** unless one of them also adopts high-temperature blanket (SiC/PbLi or similar). This is a 20-30% fusion power reduction for same electric output, partially compensating for larger size.

**All five concepts face the same divertor heat flux crisis.** ACT1 assumes 90% radiated power fraction and 5 FPY lifetime; comparables likely assume similar. If scrape-off widths prove narrower than predicted or ELM mitigation fails, all tokamaks face 15-30% size increase. **Firefly's potential ELM-free operation is the only escape route.**

**State-backed (ACT1, HH70) vs. private (SPARC, Firefly, ST80):** State-backed programs may accept lower ROI and longer timelines, enabling higher-risk R&D (SiC composites, advanced physics). Private programs face investor IRR requirements, favoring faster time-to-market (HTS magnets, conservative physics). **Cost effect: state-backed may achieve lower LCOE in 2040s if risky technologies mature; private programs may achieve commercial deployment in 2030s with higher but acceptable LCOE.**

## 8. Sources

Listed in order of importance to this analysis:

1. **ARIES-ACT Study (Kessel et al., 2015)**
   - Full citation: Kessel, C.E., et al., "The ARIES Advanced and Conservative Tokamak Power Plant Study," Fusion Science and Technology 67:1 (2015), 1-32.
   - Extraction: knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md
   - What it contributes: Complete design point parameters for ACT1 (geometry, physics, materials, performance). Four-corners study comparing advanced vs. conservative physics and engineering. COE estimates. Operating zone flexibility analysis. R&D needs assessment.
   - Retrieved from: OSTI (Office of Scientific and Technical Information), DOI 10.13182/FST14-953

2. **BEST Research Plan v1.1 (EUROfusion/ASIPP, 2025)**
   - Full citation: "BEST Research Plan, 1st Edition: Missions and Pathways to Realisation," Version 1.1, 27 November 2025. EUROfusion and ASIPP (Hefei Institutes of Physical Science, Chinese Academy of Sciences).
   - Extraction: knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/best-research-plan-v1.1-summary.md
   - What it contributes: State-backed experimental tokamak program context. Hybrid LTS+HTS magnet specifications (~2000 tonnes). Multi-method H&CD system (50 MW ECRH/ICRH/LHCD/NBI). TBM program validating three breeding concepts. Tritium fuel cycle and 110g inventory. Materials testing protocols (RAFM, SiC, Li ceramics, Be pebbles). Remote handling requirements. Risk analysis (disruptions, ELMs, material damage).
   - Retrieved from: https://euro-fusion.org/wp-content/uploads/2025/11/BEST-Research-Plan-v1.1.pdf

3. **CFETR Power Conversion Studies (2021-2025)**
   - Extraction: knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/cfetr-power-conversion-studies.md
   - What it contributes: Power conversion technology selection for Chinese fusion reactor lineage. Thermal efficiency comparison: water steam Rankine 26.4%, He Brayton + Organic Rankine 23.7%, sCO2 Brayton 34.7%. Qualitative sCO2 advantages: high efficiency, compact structure, low cost. Energy storage system for pulsed heat load management.
   - Retrieved from: ScienceDirect (truncated extraction; full text behind paywall)

4. **Neo Fusion Company Profile (FusionXInvest, 36kr)**
   - Extraction: knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/neo-fusion-company-profile.md
   - What it contributes: Company identity and ownership structure. Neo Fusion (Fusion Energy Technology Co., Ltd / 聚变新能) majority owned by CNPC and CAS. $214M funding. Relationship to ASIPP (BEST host institution). Strategic positioning in China's fusion roadmap (EAST → BEST → CFEDR → PFPP).
   - Retrieved from: FusionXInvest and 36kr business profiles

**Additional references cited but not extracted:**
- ITER cost data and TBM programs (https://www.iter.org)
- PROCESS UKAEA tokamak systems code (https://ukaea.github.io/PROCESS)
- Woodruff Scientific pyFECONS framework (arXiv:2601.21724)
- Various ARIES predecessor studies (ARIES-AT, ARIES-I) referenced in ACT study for comparison
