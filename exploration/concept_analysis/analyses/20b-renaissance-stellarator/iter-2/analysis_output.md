## Design Point

- Name: 1 GWe economically optimized compact liquid-wall HTS stellarator (Samulski et al., Nuclear Fusion 64 (2024) 026007)
- Maturity: paper-concept
- P_native: 1000 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md
  - knowledge/concept_research/20b-renaissance-stellarator/dossier.md

## 1. Availability of Data

**Rating: Moderate**

Renaissance Fusion has published two peer-reviewed papers that together define a coherent 1 GWe stellarator design point:

1. **Prost & Volpe, Nuclear Fusion 64 (2024) 026007** — "Economically optimized design point of high-field stellarator power-plant." This is the primary design-point paper defining the reactor geometry, physics operating point, and economic optimization. It establishes the major radius, aspect ratio, field strength, and power balance. This paper was not directly extracted in the available source set (it is reference [1] in the blanket paper), but its key parameters are reproduced in the blanket paper's body text and the dossier.

2. **Prost, Ogier-Collin & Volpe, J. Nuclear Materials 599 (2024) 155239** — "Compact fusion blanket using plasma facing liquid Li-LiH walls and Pb pebbles." This defines the blanket concept, radial build, and neutronics performance for the design point established in [1]. This paper is fully extracted and provides detailed quantitative data.[^1]

A third peer-reviewed paper defines the power conversion system:

3. **Famà et al., Energy Conversion and Management 276 (2023) 116572** — optimized sCO2 Brayton-Rankine combined cycle at 49–51% cycle efficiency. Referenced in the dossier but not directly extracted.[^2]

Additional public sources include a UC Berkeley seminar, MT29 conference abstract on the magnet program, company website content, and Innovation News Network coverage. Renaissance Fusion's magnet technology has a demonstrated milestone: a 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K.

**Data strengths:**
- Complete reactor geometry and physics operating point from a peer-reviewed systems study
- Detailed 1D neutronics for the blanket/radial build with OpenMC simulations
- Specific power conversion cycle with published thermodynamic optimization
- Transparent publication strategy — key design choices are in the open literature

**Key data gaps:**
- The design-point paper (Nuclear Fusion 64 (2024) 026007) was not directly extracted; Table 1 from the blanket paper (which reproduces the design point) was lost during PDF extraction. Several parameters (plasma beta, density, plasma temperature profile, detailed coil geometry, peak field on conductor) are therefore not directly verifiable from the extracted sources.
- No published dollar-figure cost estimate for the plant or any subsystem.
- No published capital cost breakdown, LCOE estimate, or cost-of-electricity study.
- No 3D neutronics — only 1D cylindrical model available.
- No thermo-fluid or MHD analysis of the liquid metal wall.
- No detailed coil manufacturing cost data for the laser-patterned HTS film approach.
- The REBCO characterization paper (arxiv 1512.01930, Senatore et al. 2015) in the source set characterizes commercial REBCO conductors from six manufacturers but does not address Renaissance Fusion's specific laser-patterned film approach.

[^1]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §1 Introduction
[^2]: dossier.md §Energy Capture

## 2. Challenges in Capturing System Function

The following challenges are ranked by their impact on LCOE modeling uncertainty:

### 2.1 Liquid Metal Wall Integration (High Impact)

The liquid Li-LiH wall with suspended Pb pebbles serves simultaneously as first wall, breeder, neutron multiplier, neutron shield, and primary coolant. This integrated architecture eliminates the separate first wall, blanket module, and shield that conventional stellarator cost models price as distinct accounts. The 1costingFE library's C220101 (first wall/blanket) and C220102 (radiation shield) accounts assume a solid first wall and a contained blanket — neither applies directly to a flowing liquid metal wall.

> "Thick liquid metal first walls could enable compact fusion blankets and radial build in stellarators while allowing for heat extraction, continuous tritium breeding and neutron shielding"
> — infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §1 Introduction

The key uncertainty is that no thermo-fluid or MHD analysis of this wall has been published. The liquid metal must flow at 700–900°C in a stellarator magnetic geometry with varying field direction — MHD pressure drops, flow stability, and heat extraction uniformity are all open questions.

### 2.2 Laser-Patterned HTS Magnet Cost (High Impact)

Renaissance Fusion's core manufacturing innovation — depositing HTS REBCO film on ~1 m diameter cylindrical surfaces and laser-patterning the current paths — has no cost precedent. Traditional stellarator coils are the dominant cost driver (complex 3D winding, precision assembly). Renaissance's approach eliminates traditional winding entirely, but the cost of the novel process (film deposition, laser ablation, quality control at scale) is not publicly characterized. The 6 T Helmholtz demonstrator at 1.2 m validates the physics concept but provides no manufacturing cost data at reactor scale (10–15 T, multiple cylinders).

### 2.3 Ignited Operating Point (Q = ∞) (Moderate Impact)

The design point assumes ignition — zero external heating at steady state, with alpha heating sustaining the plasma entirely. This is the most aggressive Q target among all stellarator concepts surveyed. If ignition is not achieved and auxiliary heating power is required at steady state, the recirculating power fraction rises, net electric output drops, and CAS22.01.04 (heating systems) becomes a non-trivial cost account. The NNBI system (60% neutralization efficiency) is specified for startup/ramp-up only.

### 2.4 Compact Geometry and Coil Stress (Moderate Impact)

The 91 cm plasma-to-coil radial build is significantly more compact than conventional stellarator designs (typically 1.3 m+). While the blanket paper demonstrates this is neutronically feasible, the structural implications — coil stress at 10.2 T on-axis (with peak fields of 20–40 T at the conductor, per the dossier), electromagnetic forces on the cylindrical magnet assemblies, and the mechanical interface between the liquid metal containment and the HTS cylinders — are not addressed in the available sources.

### 2.5 No Published Cost Data (Moderate Impact)

Unlike some competitors (e.g., CFS with ARC-derived cost studies, or ARIES-CS for classical stellarators), Renaissance Fusion has published no dollar-figure cost estimates for any subsystem. The design-point paper performs an economic optimization (selecting parameters to minimize cost via a systems model), but the resulting cost figures are not publicly available. This means all cost modeling must rely on the archetype library defaults with limited ability to validate or override.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Laser-Patterned HTS Magnets — TRL 3–4
- **Demonstrated:** 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K (MT29 Abstract). Laser patterning of REBCO film on cylindrical surfaces at laboratory scale.
- **On paper only:** Full-scale stellarator field coils at 10–15 T with the required 3D current patterns. Reactor-relevant conductor area and current density. Quench protection for patterned film conductors.
- **Missing at scale:** Film deposition on meter-scale cylinders at the required thickness and uniformity. Quality control of laser-patterned current paths at production rates. Radiation tolerance of the film-on-cylinder architecture under neutron flux. Demonstrated operation above 10 T.

### Flowing Liquid Li-LiH Wall with Pb Pebbles — TRL 2–3
- **Demonstrated:** Neutronics analysis (1D OpenMC) confirms breeding and shielding feasibility. Li-LiH phase behavior is documented (fully liquid above 680°C). Pb pebble neutron multiplier concept has nuclear engineering heritage.
- **On paper only:** The flowing wall concept in a stellarator geometry. MHD flow behavior in the non-axisymmetric stellarator field. Heat extraction uniformity and liquid metal flow stability at 700–900°C. SiC or similar coating durability on Pb pebbles at operating temperature.
- **Missing at scale:** Any experimental demonstration of a thick flowing liquid metal wall in a stellarator (or any fusion) magnetic geometry. Tritium extraction from Li-LiH at plant-relevant rates. Liquid metal handling and circulation systems at the required flow rates.

### Tritium Fuel Cycle — TRL 2–3
- **Demonstrated:** Lab-scale tritium handling and extraction from liquid metals in the broader fusion community.
- **On paper only:** Tritium extraction from the Li-LiH/Pb pebble mixture. Closed-loop fuel cycle with the specific blanket chemistry. TBR of 1.53–1.60 is calculated but depends on full coverage assumptions.
- **Missing at scale:** Industrial-scale tritium processing with Li-LiH. Permeation barriers for the V-Cr-Ti vacuum vessel at 700–900°C. Tritium accountability and safety systems for a flowing liquid metal loop.

### Remote Maintenance — TRL 2–3
- **On paper only:** The cylindrical modular architecture (4 field periods) may simplify maintenance compared to conventional non-planar stellarator coils, but no maintenance concept has been published.
- **Missing at scale:** Remote handling for a liquid-metal-filled stellarator. Access to the vacuum vessel and HTS cylinders. The blanket paper notes that "the stellarator hall will not be accessible by workers during operations."[^3]

### Power Conversion System (sCO2 Brayton-Rankine) — TRL 5–6
- **Demonstrated:** sCO2 Brayton cycles at pilot scale in the power industry. Genetic algorithm optimization of the combined cycle published.
- **On paper only:** Integration with a 700–900°C liquid metal heat source. Heat exchangers compatible with Li-LiH.
- **Missing at scale:** No fusion-specific sCO2 power conversion system has been built.

### Vacuum Vessel (V-Cr-Ti) — TRL 3–4
- **Demonstrated:** V-Cr-Ti alloys characterized for neutron irradiation and corrosion resistance. Used in fission material science programs.
- **Missing at scale:** Large-scale fabrication of V-Cr-Ti structures. Welding and joining at reactor scale. Long-term corrosion behavior in Li-LiH at 700–900°C.

### Neutron Shielding (VH2) — TRL 3
- **Demonstrated:** VH2 characterized as neutron moderator in published literature. Neutronic effectiveness confirmed in the blanket paper simulations.
- **Missing at scale:** Large-volume VH2 production and fabrication into 54 cm thick shielding layers. Long-term stability under neutron irradiation and thermal cycling.

[^3]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §5 Case Study

## 4. Key Materials and Supply Chain Considerations

### HTS REBCO Film
Renaissance Fusion's approach bypasses traditional REBCO tape winding entirely. Instead of procuring thousands of kilometers of tape (as CFS/ARC requires), they deposit REBCO film on cylindrical substrates and laser-pattern the current paths. This potentially eliminates the REBCO tape supply chain bottleneck — global tape production is currently thousands of km/year, while a single ARC-class reactor requires >5,000 km. However, the film deposition process itself requires REBCO precursor materials (rare earth oxides, barium, copper oxide), and the throughput and cost of large-area film deposition at the required quality are unknown. The Senatore et al. (2015) characterization paper in the source set identifies six commercial REBCO manufacturers across four countries, indicating a diversified but still limited supply chain for the underlying materials.

### Liquid Lithium / Lithium Hydride (Li-LiH)
The blanket uses a 5% Li / 95% LiH molar mixture as the primary breeder and coolant. LiH is produced industrially (primarily for hydrogen storage and chemical synthesis), but the quantities required for a reactor blanket — filling the entire flowing wall volume of a 3.8 m major radius stellarator — would represent a significant procurement relative to current production. LiH is pyrophoric and reacts vigorously with water, creating handling and safety considerations. The operating temperature (700–900°C) is above LiH's melting point (692°C), maintaining the mixture in a fully liquid phase.

### Lead (Pb) Pebbles
Lead was selected as the neutron multiplier specifically because tungsten and molybdenum "would increase the cost by several orders of magnitude" compared to Pb.[^4] Lead is an abundant, low-cost commodity metal. The pebble form factor (0.1–5 mm spheres with SiC or similar coatings) requires specific manufacturing but is not fundamentally challenging. The coating must resist high temperatures, corrosion from the Li-LiH, and provide electrical insulation — durability of SiC coatings in this environment is undemonstrated.

### Vanadium Alloy (V-14.5Cr-5Ti)
The 5 cm thick vacuum vessel uses a vanadium-chromium-titanium alloy selected for corrosion resistance and low activation. Vanadium is produced as a byproduct of steel processing (~100,000 t/yr globally), but the specific nuclear-grade V-Cr-Ti alloy has never been produced at the hundreds-of-tonnes scale required. The V-4Cr-4Ti variant studied for tokamak first walls has a market cost estimated at ~$37/kg; the specific 80.5V-14.5Cr-5Ti composition used here may differ.

### Vanadium Hydride (VH2) Shielding
VH2 is identified as the most compact neutron shielding material (54 cm vs. >1 m for concrete alone), but the blanket paper notes that metal hydrides "are not as cost effective as concrete."[^5] Large-volume VH2 production for reactor shielding would be a novel industrial application.

### No Li-6 Enrichment Required (Baseline)
The baseline design uses natural lithium enrichment in the Li-LiH mixture. The blanket paper shows that Li-6 enrichment would provide only minor thickness reduction at "substantially higher cost due to the costly process of Li 6 enrichment."[^6] This is a cost advantage relative to designs that require enriched Li-6 (e.g., solid ceramic breeders).

[^4]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §3.1 Candidate Material
[^5]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §5 Case Study
[^6]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §3.2 Comparison of Breeding Layer Performance

## 5. Design Point Parameters

All parameters describe the 1 GWe economically optimized compact liquid-wall HTS stellarator at its native 1000 MWe scale. Parameters are sourced from the blanket paper body text (which reproduces the design-point paper's values) and the dossier.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 3.8 m | infoscience-bitstreams...output.md §1 Introduction; §2.2 Model Description | high | spec key: `R0` |
| a (minor radius) | ~0.93 m | [inferred: R0/A = 3.8/4.1 = 0.927 m] | medium | spec key: `plasma_t`. Blanket paper uses 1.0 m plasma radius in cylindrical model approximation. |
| Aspect ratio A | 4.1 | infoscience-bitstreams...output.md §1 Introduction; §2.2 | high | |
| elongation | ~1.0 | [inferred: stellarator — no elongation parameter analogous to tokamak; complex 3D shape] | low | spec key: `elon`. Stellarator cross-section is not simply elongated; this parameter has limited meaning for stellarators. |
| B0 (on-axis field) | 10.2 T | infoscience-bitstreams...output.md §1 Introduction | high | spec key: `B` |
| B_peak (on conductor) | 20–40 T | dossier.md §Magnet Type | medium | Range from Nuclear Fusion paper (per dossier); not directly confirmed in extracted blanket paper. Informational only. |
| Number of field periods | 4 | infoscience-bitstreams...output.md §2.2 | high | 4-field period symmetry with piecewise cylindrical coil surfaces |
| Cylinder length (single period) | 6.3 m | infoscience-bitstreams...output.md §2.2 | high | |
| fusion_power_MW | ~2000 MW | infoscience-bitstreams...output.md §1: "approximately 2 GW of fusion power" | high | Informational — library back-solves from p_input + P_native. |
| thermal_power_MW | ~2200 MWth | infoscience-bitstreams...output.md §1: "approximately 2.2 GWth" | high | |
| net_electric_MWe | 1000 MWe | infoscience-bitstreams...output.md §1: "1 GWe" | high | Drives P_native. |
| p_input_MW | 5 MW | dossier.md §Plasma State; analyst estimate (see derivation) | medium | spec key: `p_input`. Design point is ignited (Q = ∞); 5 MW is a conservative estimate for residual burn-control and impurity-management power in an ignited stellarator (cf. Thea Energy Helios: 2.5 MW ECRH for 390 MWe ignited stellarator = 0.64% of P_native; 5 MW / 1000 MWe = 0.5%). NNBI system exists for startup/ramp-up. |
| Q (energy gain) | ∞ (ignited) | dossier.md §Plasma State | high | Zero external heating at operating point. |
| Plasma temperature | ~10 keV | dossier.md §Fuel: "design point at 10 keV" | high | |
| NNBI neutralization efficiency | 60% | dossier.md §Primary Heating | high | Negative Neutral Beam Injection for startup. |
| Thermal cycle efficiency (gross) | 49–51% | dossier.md §Energy Capture: Famà et al. (2023), sCO2 Brayton-Rankine | high | |
| Net plant efficiency | ~34% | dossier.md §Energy Capture | medium | Includes all auxiliary loads and recirculating power. |
| eta_th (net thermal efficiency) | ~0.45 | [inferred: 1000 MWe / 2200 MWth ≈ 0.45; cycle efficiency 49–51% with ~10% aux loads] | medium | spec key: `eta_th` |
| Availability | 80% | infoscience-bitstreams...output.md §2.1: "40 years at 80% availability" | high | |
| Plant lifetime | 40 years | infoscience-bitstreams...output.md §2.1 | high | |
| Radial build (plasma to HTS inboard) | 91 cm | infoscience-bitstreams...output.md §5 Case Study | high | 32 cm liquid metal + 5 cm vessel + 54 cm shield |
| Breeding blanket thickness | 32 cm | infoscience-bitstreams...output.md §5: "10 cm of Pb pebbles, and 22 cm of non enriched Li-LiH" | high | |
| Neutron shield thickness (VH2) | 54 cm | infoscience-bitstreams...output.md §5 | high | |
| Vacuum vessel thickness (V-Cr-Ti) | 5 cm | infoscience-bitstreams...output.md §2.2 | high | |
| Bioshield thickness | 1.3 m (borated concrete) | infoscience-bitstreams...output.md §5 | high | |
| TBR | 1.53–1.60 | infoscience-bitstreams...output.md §5 (1.60) and §6 (1.53) | high | 1.60 for reference case; 1.53 for the complete build with mixed Pb/Li-LiH. |
| Energy multiplication factor (fm) | 1.05–1.07 | infoscience-bitstreams...output.md §5 (1.07) and §6 (1.05) | high | |
| Nuclear heat in liquid metal | 90% (1.6 GW) | infoscience-bitstreams...output.md §5 | high | 3% in vacuum vessel (54 MW), 8% in shield (150 MW) |
| HTS nuclear heating (achieved) | 0.14 mW/cm³ | infoscience-bitstreams...output.md §5 | high | Well below 2 mW/cm³ limit. |
| Structural DPA limit | 200 DPA / 6.25 DPA/yr | infoscience-bitstreams...output.md §2.1 | high | Over 32 full-power years. |
| HTS neutron flux limit | 10¹⁹ n/cm² lifetime | infoscience-bitstreams...output.md §2.1 | high | |
| Neutron source rate (full reactor) | 7.1 × 10²⁰ n/s | infoscience-bitstreams...output.md §1 | high | |
| Liquid metal operating temperature | 700–900°C | infoscience-bitstreams...output.md §2.1 | high | |
| Wall loading | ~25 MW/m² | dossier.md §Tritium Breeding: "Capable of 25 MW/m² wall loading" | medium | Liquid metal wall capability; actual operating wall loading not separately stated. |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | Inherent stellarator advantage — no current drive needed. |
| Fuel | D-T | dossier.md §Fuel | high | |

**Note on missing parameters:** Plasma beta, plasma density (n_e), detailed coil geometry and conductor specifications, and peak-field-on-conductor are referenced in the Nuclear Fusion design-point paper but not reproduced in the extracted blanket paper body text. These are marked as data gaps. The elongation parameter is structurally inapplicable to stellarators (complex 3D cross-section), but a value near 1.0 is used as a modeling placeholder.

## 5b. Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier:** The flowing liquid Li-LiH wall with suspended Pb pebbles replaces the conventional solid first wall and contained blanket entirely. The architecture is fundamentally different from what the library default prices (a solid first wall with a separate blanket module). However, the dossier provides no dollar figure, unit cost, or mass-based cost estimate for the liquid metal wall system. The blanket paper provides material compositions and thicknesses but no cost data. Without a company-grounded cost figure, no override is justified — the library default stands.

**C220102 — Radiation shield:** The 54 cm VH2 neutron shield is a novel material choice (most designs use concrete, water, or steel). The blanket paper notes VH2 is more effective but "not as cost effective as concrete." No cost figure is provided for the VH2 shield. No override.

**C220103 — Confinement magnets / coils:** The laser-patterned HTS REBCO film on cylindrical surfaces is Renaissance Fusion's core innovation. This eliminates traditional coil winding — the dominant cost driver in stellarator magnet fabrication. However, no cost figure is published for the laser-patterned magnets. The 6 T demonstrator provides physics validation but no manufacturing cost data. The argument that cylindrical film deposition should be cheaper than 3D coil winding is plausible but unquantified. No override.

**C220104 — Supplementary plasma heating:** At the ignited design point (Q = ∞), the NNBI system is needed only for startup. Steady-state heating power is zero. The library default scales heating cost per installed MW. If ignition holds, the installed heating capacity is minimal (startup-only), which the library can capture through a small p_input value. No override.

**C220105 — Primary structure:** No company data. No override.

**C220106 — Vacuum system:** No company data. No override.

**C220107 — Power supplies:** No company data. No override.

**C220108 — Divertor:** The stellarator divertor is an island divertor (different from a tokamak X-point divertor), and the liquid metal wall may partially serve divertor-like functions. However, no cost data is provided. No override.

**C220110 — Remote handling:** No published maintenance concept. No override.

**C220111 — Reactor-equipment installation:** No company data. No override.

**CAS21 — Buildings & site structures:** The compact geometry (R=3.8 m, 91 cm radial build) results in a significantly smaller reactor building footprint than conventional stellarators (e.g., HELIAS 5-B at R~22 m or W7-X at R=5.5 m). The blanket paper states that reducing radial build from 1.3 m to 1 m "could reduce a 1 GWe reactor's cost by up to 20%."[^7] This cost reduction is driven in part by smaller buildings. However, the 20% figure is a systems-model output from the design-point paper — it is not a direct dollar estimate for CAS21 specifically. No company-grounded CAS21 figure exists. No override.

**CAS23 — Turbine plant equipment:** The sCO2 Brayton-Rankine combined cycle is specified at 49–51% gross efficiency. The library default handles thermal cycle costing from the thermal efficiency and power level. No specific turbine cost figure is published. No override.

**CAS24 — Electric plant equipment:** No company data. No override.

**CAS26 — Heat rejection system:** No company data. No override.

**CAS27 — Special materials:** The Li-LiH and Pb pebble inventory represents a unique initial fill material. Conventional designs use FLiBe, PbLi, or solid ceramic breeders, each with different unit costs. However, no cost figure for the Li-LiH/Pb inventory is published. No override.

**CAS70 — O&M:** No published maintenance schedule, staffing model, or component replacement rates. The liquid metal wall is claimed to reduce "solid components replacement rates compared with solid first walls,"[^8] which would lower O&M relative to solid-FW designs. However, this is a qualitative claim with no quantified O&M cost. No override.

**CAS80 — Fuel cost:** Standard D-T fuel. No override.

[^7]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §1 Introduction
[^8]: infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §1 Introduction

**Override count: 0 enabled overrides.** This is within the expected 0–4 band for High archetype-fit. The absence of overrides reflects the complete absence of published cost data from Renaissance Fusion — not a judgment that the library defaults are correct. Multiple accounts (C220101, C220103, CAS21, CAS27) would likely warrant overrides if company-grounded cost data were available.

```yaml
overrides: []
```

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Design-point paper (Nucl. Fusion 64, 2024, 026007) not extracted; Table 1 with full reactor parameters lost during PDF extraction | S1, S5 | not-yet-sourced | blocking | Re-extract the Nuclear Fusion paper with improved table handling; this is the primary design-point source. |
| 2 | No published capital cost breakdown, LCOE estimate, or dollar-figure cost data for any subsystem | S1, S5b | proprietary | blocking | The design-point paper performs economic optimization — its cost outputs may be recoverable from the paper or from the authors. |
| 3 | No thermo-fluid or MHD analysis of the flowing Li-LiH wall in stellarator geometry | S2, S3 | truly-unknown | blocking | No published study exists. Renaissance Fusion's internal work (if any) is proprietary. |
| 4 | Plasma beta, density, and detailed confinement parameters not available in extracted sources | S5 | not-yet-sourced | important | Extract the Nuclear Fusion design-point paper directly. |
| 5 | Peak magnetic field on conductor — range (20–40 T) from dossier, not confirmed in extracted sources | S5 | not-yet-sourced | important | The Nuclear Fusion paper likely specifies this precisely. |
| 6 | Laser-patterned HTS film manufacturing cost, throughput, and quality control data | S3, S4 | proprietary | important | Company disclosures or MT29 proceedings may provide partial data. |
| 7 | No 3D neutronics simulation of the blanket design | S3 | derivable | important | The blanket paper notes this as future work. 3D effects may change TBR and shielding adequacy at ports and penetrations. |
| 8 | VH2 neutron shield cost, long-term irradiation stability, and production scalability | S4 | truly-unknown | important | Literature search on vanadium hydride production and irradiation behavior. |
| 9 | V-Cr-Ti vacuum vessel fabrication at reactor scale — welding, joining, industrial supply | S4 | not-yet-sourced | important | ORNL and Japanese V-alloy programs may have relevant data. |
| 10 | No published maintenance concept or remote handling strategy | S3 | truly-unknown | important | The modular cylindrical architecture suggests simpler maintenance than conventional stellarators, but this has not been analyzed. |
| 11 | Li-LiH/Pb pebble initial inventory quantity and cost | S4, S5b | derivable | nice-to-have | Volume can be estimated from blanket geometry; Li-LiH and Pb unit costs are available from commodity markets. |
| 12 | O&M cost structure — staffing, scheduled replacement, liquid metal system maintenance | S2 | truly-unknown | important | No fusion liquid-metal-wall plant has been designed at this level of detail. |

## 7. Family-Delta vs Comparables

The fixed comparables are all MFE stellarator concepts: 05-planar-coil-stellarator (Thea Energy), 09-qi-stellarator-hts (Proxima Fusion), 10-large-scale-stellarator (Gauss Fusion), 20a-type-one-stellarator (Type One Energy), and 36-helical-coil-stellarator (Helical Fusion). No approved analyses exist for any of these comparables, so the delta articulation relies on publicly available concept descriptions and the schema classifications.

### vs. 05-planar-coil-stellarator (Thea Energy)
**Magnet architecture (C220103):** Thea Energy uses arrays of simple flat HTS coils producing stellarator fields via current distribution — fundamentally different from Renaissance's laser-patterned film on cylinders. Thea's approach trades coil simplicity (planar coils are easy to manufacture) for potentially more coils and more complex current optimization. Renaissance trades manufacturing novelty (laser-patterned film is unproven at scale) for geometric simplicity (cylindrical substrates). **Cost direction:** Uncertain — both approaches claim lower manufacturing cost than traditional non-planar coils, but via different mechanisms.

**Blanket (C220101):** Thea Energy has not published a blanket concept. Renaissance's flowing liquid metal wall is a specific cost-differentiating feature that no other stellarator in the comparables has detailed to this degree. **Cost direction:** Unknown pending Thea's blanket specification.

### vs. 09-qi-stellarator-hts (Proxima Fusion)
**Geometry (CAS21, C220103):** Proxima Fusion pursues a quasi-isodynamic stellarator with traditional 3D HTS coils. Renaissance's compact geometry (R=3.8 m, A=4.1) is likely smaller than Proxima's HELIAS-derived design. A smaller major radius directly reduces building volume, coil material, and structural support — all capital cost advantages.

> "Reducing the blanket radial build (plasma-coil distance) from 1.3 m to 1 m could reduce a 1 GWe reactor's cost by up to 20%"
> — infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md §1

**Coil manufacturing (C220103):** Proxima uses conventional HTS winding for complex 3D coils. Renaissance eliminates winding entirely. The cost comparison depends on whether laser-patterned film deposition can achieve lower cost per ampere-meter than wound REBCO tape at the required field levels. **Cost direction:** Potentially advantageous for Renaissance if film deposition scales, but unquantified.

### vs. 10-large-scale-stellarator (Gauss Fusion)
**Scale (all accounts):** Gauss Fusion pursues a large-scale conventional stellarator, likely at HELIAS 5-B scale (R~22 m). Renaissance's compact design at R=3.8 m is roughly 6× smaller in major radius. This is the most dramatic geometric divergence in the comparables set. Capital cost scales roughly with reactor volume (for structures, magnets, and building), giving Renaissance a structural cost advantage — partially offset by higher field strength and higher wall loading.

**Magnet technology (C220103):** Gauss Fusion uses LTS (Nb3Sn/NbTi) or LTS+HTS magnets, not full HTS. Renaissance's all-HTS approach enables the compact geometry through higher field. The HTS cost premium may be offset by the dramatically smaller machine size. **Cost direction:** Net effect is uncertain; Renaissance trades higher magnet unit cost ($/kg of HTS) for lower total magnet mass and smaller supporting structures.

### vs. 20a-type-one-stellarator (Type One Energy)
**Coil geometry (C220103):** Type One Energy uses modular stellarator coils with HTS, emphasizing simplified coil shapes optimized for manufacturability. Renaissance's laser-patterned film takes this simplification further — the "coil" is a patterned cylinder rather than a wound solenoid or saddle coil. Both target manufacturing cost reduction relative to classical stellarator coils, but via different strategies.

**Blanket and operating point:** Type One has not published detailed blanket or operating-point data comparable to Renaissance's peer-reviewed design point. Renaissance's ignited operating point (Q=∞) and flowing liquid metal wall are differentiating features with unclear cost implications absent Type One's design details.

### vs. 36-helical-coil-stellarator (Helical Fusion / HESTIA)
**Coil topology (C220103):** Helical Fusion uses helical coils wound around the torus — a fundamentally different topology from Renaissance's cylindrical patterned magnets. Helical coils are mechanically stressed differently and require different winding technology. **Cost direction:** Unknown — helical winding may be simpler than non-planar modular coils but more complex than Renaissance's cylindrical approach.

**Blanket and geometry:** Both concepts target compact geometry with HTS magnets. Detailed comparison is limited by the absence of published design-point parameters for HESTIA at the level of detail available for Renaissance.

### Summary of Family Deltas

| Subsystem | Renaissance Differentiator | Cost Direction | Magnitude |
|-----------|---------------------------|----------------|-----------|
| C220103 (magnets) | Laser-patterned HTS film on cylinders eliminates coil winding | Potentially advantageous | Unknown — no cost data |
| C220101 (FW/blanket) | Flowing Li-LiH wall with Pb pebbles — integrated FW/blanket/shield | Potentially advantageous (reduced solid component replacement) | Unknown — no cost data |
| CAS21 (buildings) | Compact geometry (R=3.8 m) vs. R=5–22 m for comparables | Advantageous (smaller reactor building) | Up to 20% total cost reduction claimed |
| C220108 (divertor) | Island divertor + liquid metal wall may reduce divertor load | Neutral to advantageous | Unknown |
| C220104 (heating) | Ignited operating point — no steady-state heating | Advantageous (near-zero recirculating power for heating) | Moderate — eliminates ~50–100 MW of auxiliary power |
| CAS23 (turbine) | sCO2 Brayton-Rankine at 49–51% efficiency (vs. typical 33–40% Rankine) | Advantageous (higher efficiency → smaller thermal plant for same MWe) | Moderate |
| CAS27 (special materials) | Li-LiH + Pb fill vs. FLiBe or PbLi | Uncertain — Li-LiH cost is unknown; avoids Be (in FLiBe) and Li-6 enrichment | Unknown |

## 8. Sources

1. **Prost, Ogier-Collin & Volpe, "Compact fusion blanket using plasma facing liquid Li-LiH walls and Pb pebbles," J. Nuclear Materials 599 (2024) 155239.** The primary quantitative source for this analysis. Provides the reactor geometry (R=3.8 m, A=4.1, B=10.2 T), blanket design (Li-LiH + Pb pebbles), radial build (91 cm), neutronics results (TBR=1.53–1.60, fm=1.05–1.07), and design requirements (200 DPA limit, 80% availability, 40-year lifetime). Located at: `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md`

2. **Prost & Volpe, "Economically optimized design point of high-field stellarator power-plant," Nuclear Fusion 64 (2024) 026007.** The design-point paper defining the complete reactor parameters and economic optimization. Referenced as [1] in the blanket paper and throughout the dossier. Not directly extracted in the available source set — key parameters are reproduced via the blanket paper and dossier. URL: https://iopscience.iop.org/article/10.1088/1741-4326/ad142e

3. **Dossier: Compact Liquid-Wall HTS Stellarator (D-T).** Structured research summary providing differentiation table values, key citations, and synthesis of multiple sources including the Nuclear Fusion paper, J. Nuclear Materials paper, MT29 abstract, UC Berkeley seminar, and company website. Located at: `knowledge/concept_research/20b-renaissance-stellarator/dossier.md`

4. **Famà et al., "An optimized power conversion system for a stellarator-based nuclear fusion power plant," Energy Conversion and Management 276 (2023) 116572.** Defines the sCO2 Brayton-Rankine combined cycle at 49–51% gross efficiency and 34% net plant efficiency. Referenced in the dossier. URL: https://doi.org/10.1016/j.enconman.2022.116572

5. **Senatore et al., "Field and temperature scaling of the critical current density in commercial REBCO coated conductors," arXiv:1512.01930 (2015).** Characterizes REBCO conductor performance across six manufacturers. Tangentially relevant to HTS magnet costing — provides context on conductor variability but does not address Renaissance's specific laser-patterned film approach. Located at: `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/arxiv-1512-01930/output.md`

6. **UKAEA PROCESS Stellarator Documentation.** Documents the PROCESS systems code stellarator module, including geometry handling, coil models, and blanket modules. Provides context on how conventional stellarator cost models work (borrowing the tokamak cost module). Located at: `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/ukaea-process-fusion-devices-stellarator/output.md`

7. **Renaissance Fusion company website and public presentations.** Technology overview, papers page, MT29 conference abstract, and UC Berkeley seminar. Provide magnet demonstration data (6 T at 1.2 m) and qualitative descriptions of the approach. URLs listed in dossier §Key Sources.
