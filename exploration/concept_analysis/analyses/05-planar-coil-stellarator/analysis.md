---
ID: 05-planar-coil-stellarator
Concept: Planar-Coil Stellarator (Thea Energy)
Company: Thea Energy
Status: draft
Created: 2026-06-05
Approved-Date:
Confinement-Family: MFE
Archetype: STELLARATOR
Archetype-Fit: High
Comparison-Status: costingfe
Comparables:
  - 09-qi-stellarator-hts
  - 10-large-scale-stellarator
  - 20a-type-one-stellarator
  - 20b-renaissance-stellarator
  - 36-helical-coil-stellarator
Design-Point-Name: Helios preconceptual design (Swanson et al. 2025, arXiv:2512.08027)
Design-Point-Maturity: paper-concept
P-Native: 390
Grounding-Confidence: high
---

## Design Point

- Name: Helios preconceptual design (Swanson et al. 2025, arXiv:2512.08027)
- Maturity: paper-concept
- P_native: 390 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md
  - knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-doe-certification-jan2026.md
  - knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-website-and-press.md

## Section 1: Availability of Data

**Rating: Rich**

The planar-coil stellarator concept is among the most thoroughly documented private fusion designs. The primary source is the ~200-page Helios preconceptual design paper (arXiv:2512.08027, Swanson et al. 2025)[^1], which covers plasma physics, equilibrium design, MHD stability, turbulent transport, energetic particle confinement, coil engineering, blanket and shielding neutronics, thermal cycle power flows, fuel cycle, maintenance architecture, electrical systems, and instrumentation. This paper is the foundation of a special issue in *Fusion Engineering and Design* comprising 15 companion papers on individual subsystems.

> "Practicality, conservatism, and engineering margin are primary design drivers."
> — thea-energy-helios-arxiv-2512-08027.md §1 Introduction

The Helios design was certified by the U.S. Department of Energy under its Milestone-Based Fusion Development Program in January 2026 — Thea Energy was the first awardee company to complete this certification[^2]. The certification involved review by independent experts from national laboratories and universities, confirming "the physics and engineering basis of the Helios design, and its feasibility to put fusion energy on the grid."[^2]

Additional sources include:

- **Canis prototype paper** (arXiv:2503.18960): Reports experimental results from a superconducting 3×3 planar coil array, demonstrating closed-loop magnetic field control to within 1% RMS of predictions[^3]. Confirms REBCO conductor and validates manufacturing repeatability across three HTS suppliers.
- **Four peer-reviewed papers in Nuclear Fusion** (Vol. 65, Issue 2, Jan 2025): Cover planar coil stellarator systems, coil optimization, Eos neutron source design, and fast ion confinement[^4].
- **Thea Energy website and press releases**: Provide high-level value proposition but no quantitative cost data[^5].

The design is notably self-consistent: the paper presents a complete power flow Sankey diagram, interdependent equilibrium-coil-blanket-shield-thermal cycle, and verified physics with state-of-the-art codes (DESC, TERPSICHORE, M3D-C1, STELLOPT/BEAMS3D, GX gyrokinetic).

**Key data gaps:**

- **No published cost estimates or LCOE projections.** The Helios paper contains no capital cost breakdown, no $/kW figures, and no LCOE analysis. The dossier lists an LCOE target of "$150/MWh → $60/MWh at scale," but this figure does not appear in any extracted source and may originate from investor materials or press coverage not in our corpus.
- **No REBCO tape quantity or mass.** The paper notes that "total HTS tape length may be optimized directly" but does not state how much tape the Helios coil set requires. This is critical for costing the magnet system.
- **No neutron wall loading figure.** The average first wall neutron loading (MW/m²) is not explicitly stated, though it can be inferred from fusion power and plasma geometry.
- **No O&M cost breakdown.** No fixed vs. variable operating costs, staffing estimates, or scheduled replacement costs are provided.

[^1]: thea-energy-helios-arxiv-2512-08027.md, full document
[^2]: thea-energy-doe-certification-jan2026.md §DOE Certification
[^3]: thea-energy-canis-prototype-arxiv-2503-18960.md §VI-B Field Shaping Campaign
[^4]: thea-press-release-thea-energy-announces-peer-reviewed.md
[^5]: thea-energy-website-and-press.md

## Section 2: Challenges in Capturing System Function

The following challenges are ranked by LCOE impact, from highest to lowest:

### 1. Missing Cost Basis (Critical)

The Helios paper is an engineering and physics design document, not a cost study. No capital cost estimates, LCOE projections, or subsystem cost breakdowns exist in the public domain for this concept. This means all costing must rely on library defaults (per the 1costingFE archetype) with only limited data for overrides. The absence of cost data is the single largest modeling challenge.

### 2. Magnet Cost Uncertainty (High)

The planar coil architecture is the defining innovation, but its cost implications are ambiguous. The design uses 12 encircling coils and 324 shaping coils, all HTS REBCO at 20 T maximum field. Key unknowns:

- Total REBCO tape length is not published.
- The shaping coils use a novel partially-insulated, soldered-metal-insulation (SMI) architecture demonstrated only at prototype scale (Canis, 9 coils).
- Whether planar coils are genuinely cheaper per ampere-meter than 3D modular coils is plausible but unquantified. The claim rests on manufacturing simplification (winding in tension, single pancake size for all 324 shaping coils, relaxed tolerances) rather than demonstrated cost data.

> "All three [HSX, NCSX, W7-X] exhibited cost and schedule overruns, and identified significant practical difficulty in designing, manufacturing, and assembling complexly curved, 3D coils to the required precision. NCSX was canceled partway through manufacturing."
> — thea-energy-helios-arxiv-2512-08027.md §1 Introduction

### 3. Confinement and Ignition Assumptions (High)

Helios operates in an essentially ignited regime: 958 MW fusion power with only ~1 MW ECRH during steady state. This requires:

- ISS04 confinement enhancement factor H_ISS04 = 1.4, claimed to be "achieved in the W7-X stellarator." Gyrokinetic verification yields H_ISS04 = 1.33[^6].
- Volume-averaged beta of 2.7%, which is conservative relative to ARIES-CS (~5-6%) but still undemonstrated at reactor scale in a QA stellarator.
- No large quasi-axisymmetric stellarator has been built. QA physics validation comes from the small HSX experiment and from simulations. The Eos facility (first plasma ~2030) is the planned verification step before Helios.

If confinement falls short of H_ISS04 = 1.4, the plant would need substantially more auxiliary heating power, increasing recirculating power and reducing net electric output.

### 4. First Wall Material (V-4Cr-4Ti) Maturity (Medium-High)

The first wall uses V-4Cr-4Ti ("V44") vanadium alloy, chosen for its 15 full-power-year neutron damage tolerance (compared to ~7 years for RAFM steels). The paper itself acknowledges:

> "Considerations potentially contraindicating V44 include its high affinity for hydrogenic species, swelling under irradiation, and immature supply chain."
> — thea-energy-helios-arxiv-2512-08027.md §4.2

V-4Cr-4Ti has never been produced at the multi-hundred-tonne scale required for a power plant. Its market and supply chain are essentially nonexistent. If V44 proves impractical, fallback to EUROFER97 would halve the first wall lifetime to ~7 years, increasing component replacement frequency and reducing capacity factor.

### 5. Novel Divertor Concept (Medium)

Helios features the first tokamak-like X-point divertor in a stellarator power plant design, claimed to exhaust gas "10 times more effectively than existing stellarator divertors."[^7] This is unproven experimentally in any stellarator. The divertor targets are 51,000 tessellated hexagonal tungsten tiles cooled by helium impingement jets. Heat flux management to the assumed 10 MW/m² limit requires "some combination of radiative impurity seeding in the edge, or detachment, or enhanced core radiation, or finely contoured targets."[^8]

### 6. Capacity Factor Validation (Medium)

The claimed 88% capacity factor derives from one 84-day planned outage every two years. This depends on the sector-based maintenance scheme working as designed and the 15-year first wall lifetime being achieved. Both are undemonstrated. For comparison, ARIES-CS assumed ~85% availability but with a port-based maintenance scheme that was recognized as impractical.

[^6]: thea-energy-helios-arxiv-2512-08027.md §3.5
[^7]: thea-energy-helios-arxiv-2512-08027.md §2 Summary
[^8]: thea-energy-helios-arxiv-2512-08027.md §3.7

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Quasi-Axisymmetric Stellarator Equilibrium at Reactor Scale, TRL 2–3

- **Demonstrated**: QA stellarator physics demonstrated at small scale (HSX, R ~ 1.2 m). Gyrokinetic and MHD simulations verify the Helios equilibrium properties. Canis prototype validated field shaping with a 3×3 planar coil array at 20 K.
- **On paper only**: The specific Helios two-field-period QA equilibrium at R = 8 m with bootstrap-current-dominated rotational transform. No QA stellarator at this scale has been built.
- **Missing at scale**: Experimental validation of QA confinement and stability at reactor-relevant parameters. Eos (first plasma ~2030) will be the first integrated test of the planar coil stellarator concept.

### Tokamak-Like X-Point Divertor in a Stellarator, TRL 2–3

- **Demonstrated**: X-point divertors are mature in tokamaks. Stellarator divertors (island type) demonstrated in W7-X.
- **On paper only**: A tokamak-like continuous X-point divertor in a stellarator is described for the first time in Helios. Simulated to compress neutral density 10× more effectively than existing stellarator divertors.
- **Missing at scale**: No experimental stellarator has implemented this divertor topology. Heat flux management to 10 MW/m² limit is assumed but unverified.

### V-4Cr-4Ti First Wall, TRL 3–4

- **Demonstrated**: Small-scale V-4Cr-4Ti specimens irradiated and tested. Alloy composition and properties are characterized.
- **On paper only**: Fabrication of large-scale first wall panels with integrated helium cooling channels and tungsten armor coating.
- **Missing at scale**: Industrial-scale V-4Cr-4Ti production, welding and joining at power plant scale, long-term irradiation performance data at fusion-relevant fluences. Immature supply chain explicitly acknowledged by Thea Energy.

### Sector-Based Remote Maintenance, TRL 3–4

- **Demonstrated**: Tokamak-inspired concept; ITER remote handling prototypes exist for tokamak sector removal.
- **On paper only**: Stellarator sector removal from between planar encircling coils, with shaping coil removal and replacement. Ground-based remote handling platform with overhead manipulators designed at preconceptual level.
- **Missing at scale**: No stellarator has performed sector-based maintenance. Integration of shaping coil removal, cooling disconnects, and sector re-alignment after reinsertion.

### Tritium Breeding Blanket (DCLL — Pb-17Li), TRL 3–4

- **Demonstrated**: Lead-lithium eutectic properties characterized. EUROFER97 structural material tested in non-fusion environments. SiC flow channel inserts fabricated at small scale. EU-DEMO DCLL design at advanced conceptual level.
- **On paper only**: Uniform 50 cm blanket with 65% Li-6 enrichment, TBR 1.3 idealized. TMAP8 fuel cycle modeling shows TBR > 1.15 sufficient.
- **Missing at scale**: No integrated blanket module tested under fusion neutron spectrum. Tritium extraction from LiPb at plant scale. SiC MHD inserts at reactor dimensions.

### HTS Planar Coil Array (REBCO), TRL 4–5

- **Demonstrated**: Canis 3×3 superconducting planar coil array operated at 20 K with closed-loop field control achieving 0.56–0.60% RMS field error[^9]. REBCO coils wound from three different suppliers without process modification. Manufacturing takt time target of 1 double-pancake per day demonstrated[^10]. Large-bore 20 T HTS magnets demonstrated (CFS SPARC model coil).
- **On paper only**: 336-coil set (12 encircling + 324 shaping) at reactor scale with 20 T peak field.
- **Missing at scale**: Full encircling coil at Helios bore dimensions. Shaping coils at >14 T field on conductor (vs. ~3 T in Canis). Quench protection system validated at full stored energy. REBCO tape production at the thousands-of-kilometers scale needed.

### ECRH Heating System, TRL 6–8

- **Demonstrated**: ITER-specification 170 GHz gyrotrons at MW class routinely operated. W7-X heated by ECRH.
- **Missing at scale**: Continuous-wave operation at 10 MW for startup, with high-field-side X1 launch in a QA stellarator geometry.

### Power Conversion (Steam Rankine), TRL 8–9

- **Demonstrated**: Three-stage steam turbine Rankine cycle at 635°C is mature industrial technology. The thermal cycle design achieves ~40.2% combined efficiency.
- **Missing at scale**: Coupling to fusion-specific heat sources (LiPb and helium intermediate heat exchangers with tritium permeation barriers).

[^9]: thea-energy-canis-prototype-arxiv-2503-18960.md §VI-B, Table VI
[^10]: thea-energy-canis-prototype-arxiv-2503-18960.md §III

## Section 4: Key Materials and Supply Chain Considerations

### REBCO HTS Tape

The Helios coil set (12 encircling + 324 shaping coils, all operating at 20 K, up to 20 T peak field) represents a major REBCO tape demand, though the exact quantity is not published. For comparison, a single ARC-class tokamak requires >5,000 km of REBCO tape. Global REBCO production is currently on the order of thousands of km/year. The Canis program demonstrated insensitivity to HTS supplier by using tape from three different manufacturers (YBCO and GdBCO) without modifying the baseline manufacturing process[^11]. Key manufacturers include Shanghai Superconductor Technology, Faraday Factory Japan, SuperPower, and CFS's in-house production. Current REBCO prices range from $30–100/kA-m; commercial fusion viability is generally estimated to require ~$10/kA-m.

The partially-insulated SMI architecture used for shaping coils is a Thea-specific innovation. Its scalability to thousands of coils is plausible (same pancake dimensions for all 324 shaping coils) but undemonstrated at production volumes.

### Vanadium Alloy (V-4Cr-4Ti)

The first wall is 2 cm thick V-4Cr-4Ti with tungsten armor. Global vanadium production is ~100,000 tonnes/year, but the specific nuclear-grade V-4Cr-4Ti alloy has never been produced at the multi-hundred-tonne scale needed for a single reactor. The alloy requires controlled impurities (particularly O, N, C, Si) to maintain ductility under irradiation. The paper explicitly acknowledges the "immature supply chain."[^12] If V44 proves impractical, EUROFER97 is the fallback — a more mature material but with roughly half the neutron damage tolerance.

### Lead-Lithium Eutectic (Pb-17Li) with Li-6 Enrichment

The blanket uses 50 cm of Pb-17Li with 65% Li-6 isotopic enrichment. Natural lithium contains ~7.5% Li-6; enrichment to 65% requires substantial isotopic separation capacity. Global Li-6 enrichment facilities are limited (primarily Russia and China using mercury-based processes banned elsewhere). The volume of Pb-17Li needed for a uniform 50 cm blanket at R = 8 m is substantial — likely hundreds of tonnes.

### EUROFER97 (Blanket Structure)

EUROFER97 reduced-activation ferritic-martensitic steel is used for blanket structural components. It is in advanced development for EU-DEMO and other fusion applications but is not yet mass-produced. Shared demand with DEMO-class reactor programs may eventually support a supply chain.

### Tungsten (Divertor and First Wall Armor)

The divertor consists of 51,000 tessellated hexagonal tungsten tiles, each 2.5 cm wide, cooled by helium impingement jets. Tungsten supply is adequate globally (~100,000 tonnes/year), but fabricating precision plasma-facing tiles that withstand thermal cycling without cracking remains an active manufacturing challenge. The first wall also carries a thin tungsten armor layer over the V-4Cr-4Ti substrate.

### Silicon Carbide (SiC) Flow Channel Inserts

SiC inserts form an electrically insulating, thermally conductive barrier between flowing Pb-17Li and the EUROFER97 structure, critical for managing MHD drag. SiC composite manufacturing at the required quality and scale is not established for fusion applications.

[^11]: thea-energy-canis-prototype-arxiv-2503-18960.md §III
[^12]: thea-energy-helios-arxiv-2512-08027.md §4.2

## Section 5: Design Point Parameters

All parameters describe the Helios preconceptual design at its native 390 MWe scale.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| R0 (major radius) | 8 m | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | spec key: `R0` |
| a (minor radius) | 1.8 m | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | spec key: `plasma_t`. Given A=4.5, a = R0/A = 8/4.5 = 1.78 m; paper states 1.8 m. |
| Aspect ratio (A) | 4.5 | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| B (on-axis field) | 6 T | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | spec key: `B` |
| B_peak (on conductor) | 20 T | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational only — design limit, achieved by SPARC model coil |
| Plasma volume | 500 m³ | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| Volume-averaged beta | 2.7% | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | enforced as hard limit for conservatism |
| Peak ion temperature | 20 keV | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| Peak electron density | 2.1 × 10²⁰ /m³ | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| Energy confinement time | 1.8 s | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| H_ISS04 | 1.4 | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | medium | achieved in W7-X; gyrokinetic verification yields 1.33 |
| Elongation | ~1.0 | [inferred: QA stellarator cross-sections shown in Fig. 4 are roughly circular with bean-shaping; no explicit elongation stated] | low | spec key: `elon`. Stellarator cross-section is not described by a single elongation; value approximate. |
| fusion_power_MW | 958 MW | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational — library back-solves from p_input + P_native |
| Thermal power (total) | 1,094 MW | thea-energy-helios-arxiv-2512-08027.md §4.4 | high | includes 135 MW from exothermic Li-6 breeding reaction |
| Gross electric power | 438 MWe | thea-energy-helios-arxiv-2512-08027.md §4.4 | high | 460 MWe generated minus 22 MWe pumping |
| net_electric_MWe | 390 MWe | thea-energy-helios-arxiv-2512-08027.md §2 Table 1, §4.4 | high | drives P_native |
| Thermal conversion efficiency (eta_th) | 40.2% | thea-energy-helios-arxiv-2512-08027.md §4.4 | high | Rankine cycle at 635°C superheated steam |
| p_input_MW (auxiliary heating) | 2.5 MW | thea-energy-helios-arxiv-2512-08027.md §4.4 | high | spec key: `p_input`. 1 MW ECRH + overhead during ignited operation. 10 MW during startup only. |
| Recirculating power (total auxiliary) | ~48 MW | thea-energy-helios-arxiv-2512-08027.md §4.4 | high | to maintain facility in power-producing state |
| Total auxiliary power (steady-state) | ~70 MW | thea-energy-helios-arxiv-2512-08027.md §4.6 | high | includes thermal-hydraulics, tritium processing, cryogenics, maintenance |
| Capacity factor | 88% | thea-energy-helios-arxiv-2512-08027.md §2, §4.5 | medium | based on 84-day biennial maintenance outage |
| Number of field periods | 2 | thea-energy-helios-arxiv-2512-08027.md §2 | high | informational — QA stellarator |
| Number of encircling coils | 12 | thea-energy-helios-arxiv-2512-08027.md §2 | high | 4 unique shapes |
| Number of shaping coils | 324 | thea-energy-helios-arxiv-2512-08027.md §2 | high | all same inner/outer diameter; individually controllable |
| Magnet operating temperature | 20 K | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| Minimum plasma-coil distance | 1.2 m | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | enables uniform radial build |
| First wall material | V-4Cr-4Ti + W armor | thea-energy-helios-arxiv-2512-08027.md §4.2 | high | informational |
| First wall lifetime | 15 full-power years | thea-energy-helios-arxiv-2512-08027.md §4.2 | medium | based on V44 neutron damage tolerance |
| Blanket type | DCLL Pb-17Li, 65% Li-6, 50 cm | thea-energy-helios-arxiv-2512-08027.md §4.3 | high | EUROFER97 structure, SiC MHD inserts, He-cooled |
| TBR (idealized) | 1.3 | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | medium | homogenized geometry; required TBR ~1.15 |
| Tritium startup inventory | 1–2 kg | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | informational |
| Coil minimum lifetime | 40 years | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | medium | based on thick shielding attenuating neutrons |
| Divertor heat flux limit | 10 MW/m² | thea-energy-helios-arxiv-2512-08027.md §3.7 | medium | assumed engineering limit |
| Neutron wall loading (average) | ~1.5 MW/m² | [inferred: 766 MW neutron power (80% × 958 MW) / ~500 m² first wall area (estimated from R=8 m, a=1.8 m geometry)] | low | not explicitly stated; estimate from power and geometry |
| Rotational transform (iota, 2/3 surface) | 0.46 | thea-energy-helios-arxiv-2512-08027.md §2 Table 1 | high | ~1/3 vacuum, ~2/3 bootstrap current |
| Cryostat heat leak (20 K) | ~40 kW | thea-energy-helios-arxiv-2512-08027.md §4.5 | high | informational |
| Cryoplant power | ~10 MW | thea-energy-helios-arxiv-2512-08027.md §4.5 | high | at 25% Carnot efficiency |

## Section 5b: Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier**: The dossier provides detailed blanket specifications (Pb-17Li, 65% Li-6, 50 cm, EUROFER97 structure, SiC inserts, TBR 1.3) and specifies V-4Cr-4Ti first wall with W armor. However, no dollar costs, unit prices, or mass quantities for the blanket system are published. The library default for a liquid-metal blanket at this plasma size is the appropriate baseline. **No override.**

**C220102 — Radiation shield**: Multi-layer shield specified (WC → B4C → 316L SS vacuum vessel → borated water → borated HDPE → 2 m concrete bioshield). Minimum 1.2 m plasma-to-coil distance provides generous shielding space. However, no cost data is published. **No override.**

**C220103 — Confinement magnets / coils**: This is the account where the planar coil concept is most distinctive. The design uses 12 large encircling coils + 324 smaller shaping coils, all planar REBCO HTS at 20 T. The manufacturing claim — all shaping coils are the same pancake size, wound in tension, relaxed tolerances — is qualitatively compelling but no REBCO tape quantity, mass, or dollar cost is published. The Canis prototype demonstrated manufacturing repeatability but at ~3 T, not 20 T. Without a published tape length or unit cost, the library's ampere-meter-based coil cost computation from B and R0 is the best available estimate. **No override.**

**C220104 — Supplementary plasma heating**: Helios uses 10 MW ECRH for startup and 1 MW (2.5 MW budgeted) during ignited operation. ITER-specification 170 GHz gyrotrons. The heating power is remarkably low because the plasma is ignited. At 2.5 MW wallplug, this is a trivially small cost item compared to library defaults for stellarators. However, no per-MW gyrotron cost is published by Thea. The library's per-installed-MW ECRH default applies. **No override.**

**C220105 — Primary structure**: Stainless steel coil cases with stresses below 800 MPa, central support structure, inter-coil trusses. "No part of the structure exceeds 800 MPa, compatible with widely available stainless steel alloys."[^13] This is a positive cost signal — no exotic alloys needed — but no tonnage or dollar figure is published. **No override.**

**C220106 — Vacuum system**: The vacuum vessel is 316L stainless steel, integrated into the neutron shield stack. Turbomolecular pumps (not cryosorption) enabled by the high neutral compression of the X-point divertor. No cost data. **No override.**

**C220107 — Power supplies**: DC magnet power supplies for 12 encircling coils (up to 50 kA) and 324 shaping coils (150 A nominal via modular DC/DC converters). The shaping coil supplies use "inexpensive COTS relays for current commutation"[^14] due to the low 150 A operating current. No cost data published. **No override.**

**C220108 — Divertor**: 51,000 tessellated hexagonal tungsten tiles, 2.5 cm width, helium impingement jet cooling, vanadium alloy support structure. Novel topology (X-point in stellarator) but conventional materials. No cost data. **No override.**

**C220110 — Remote handling & maintenance**: Sector-based removal with ground-based remote handling platform extended through side panel ports and overhead manipulators through dome ports. Encircling coils remain integrated. Novel for stellarators but inspired by tokamak practice. No cost data. **No override.**

**C220111 — Reactor-equipment installation & assembly**: No data. **No override.**

**CAS21 — Buildings & site structures**: The paper describes a ~2 m concrete bioshield and cryostat dimensions but provides no building cost data. **No override.**

**CAS23 — Turbine plant equipment**: Steam Rankine cycle with three-stage turbines at 635°C superheated steam. Twin 300 MVA transformers. Mature technology. No cost data. **No override.**

**CAS24 — Electric plant equipment**: 34.5 kV medium-voltage backbone, 345 kV grid connection, STATCOM/SVC, BESS. Standard industrial design. No cost data. **No override.**

**CAS26 — Heat rejection system**: 681 MW waste heat to be rejected. No specific cooling system design or cost data. **No override.**

**CAS27 — Special materials (initial inventory)**: 1–2 kg tritium startup inventory (~$30k–$70k/g). Pb-17Li initial fill at 65% Li-6 enrichment — this is a substantial cost item but no volume or cost is published. Enriched Li-6 is expensive and supply-constrained. Without a published mass or cost, the library default applies. **No override.**

**CAS70 — Annualized O&M**: No O&M cost breakdown is published. The 84-day biennial outage implies significant maintenance operations but no staffing or cost data exists. **No override.**

**CAS80 — Annualized fuel cost**: D-T fuel costs are negligible at any reasonable assumption. No data to override. **No override.**

### Override Count

**Enabled overrides: 0.** This falls within the expected band of 0–4 for a High archetype-fit grade. The zero count reflects the complete absence of published cost data from Thea Energy. The Helios paper is an exceptionally detailed engineering and physics design document, but it contains no economic analysis whatsoever. All costing must rely entirely on library defaults computed from the design point parameters.

```yaml
overrides: []
```

[^13]: thea-energy-helios-arxiv-2512-08027.md §4.1
[^14]: thea-energy-canis-prototype-arxiv-2503-18960.md §V-F

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No LCOE estimate or capital cost breakdown published | S1 | proprietary | blocking | Request from Thea Energy or commission independent cost study |
| 2 | REBCO tape quantity (km or tonnes) for Helios coil set not published | S4, S5 | proprietary | blocking | Essential for coil cost estimate; could be derived from coil geometry and current density if detailed coil specs published |
| 3 | Average neutron wall loading (MW/m²) not explicitly stated | S5 | derivable | important | Can be estimated from fusion power, neutron fraction, and first wall area (~1.5 MW/m² inferred) |
| 4 | V-4Cr-4Ti cost, availability, and fabrication at scale | S4 | truly-unknown | important | No industrial supplier exists; need alloy cost estimate and production feasibility study |
| 5 | O&M cost breakdown (fixed, variable, staffing, scheduled replacement) | S1 | not-yet-sourced | important | Standard fusion plant O&M assumptions can be applied; Helios-specific data would refine |
| 6 | Li-6 enrichment cost and Pb-17Li initial fill volume/mass | S4 | not-yet-sourced | important | Volume derivable from blanket geometry; enrichment cost from nuclear industry data |
| 7 | Shaping coil manufacturing cost at production volume (324 units) | S3 | proprietary | important | Canis demonstrated process but no cost per coil published |
| 8 | Divertor heat flux performance validation in stellarator geometry | S3 | truly-unknown | important | Requires experimental program (Eos or dedicated test facility) |
| 9 | Elongation / cross-section shape parameter for cost modeling | S5 | derivable | nice-to-have | QA stellarator cross-section is not well-described by single elongation; use plasma volume directly |
| 10 | QA stellarator confinement at reactor-relevant parameters | S2 | truly-unknown | important | No large QA stellarator exists; Eos will provide first data ~2030 |

## Section 7: Family-Delta vs Comparables

### vs. 09-qi-stellarator-hts (Proxima Fusion / Stellaris — QI stellarator with HTS)

**Optimization philosophy**: Helios is quasi-axisymmetric (QA); the QI stellarator is quasi-isodynamic (QI, W7-X heritage). QA produces tokamak-like transport properties and enables a tokamak-like X-point divertor. QI has stronger experimental validation (W7-X) but requires more strongly shaped plasma boundaries and closer coil-plasma spacing.

**Coil architecture** (C220103): This is the primary delta. Helios uses planar coils (12 encircling + 324 shaping, all flat and convex) vs. complex 3D non-planar HTS coils for the QI approach. The planar architecture claims manufacturing simplification (winding in tension, single pancake geometry, relaxed tolerances via software error correction) but trades this for a large number of coils (336 total) with complex current optimization and control systems. **Cost direction: potential advantage** — manufacturing simplicity and mass-producibility of identical shaping coils vs. bespoke 3D-wound coils. Magnitude unknown; the QI approach has fewer total coils but each is harder to build.

**Plasma-coil distance**: Helios maintains 1.2 m minimum, enabling a uniform blanket (C220101) and thick shielding. QI stellarators typically require closer coil-plasma spacing for field accuracy, potentially requiring non-uniform blankets (as in ARIES-CS). **Cost direction: advantage** for Helios in blanket simplicity and coil shielding/lifetime.

**Maintenance** (C220110): Helios sector-based scheme removes entire toroidal sectors from between encircling coils. QI stellarators with close-fitted 3D coils face the ARIES-CS problem of serial port-based extraction of hundreds of components. **Cost direction: advantage** for Helios in maintenance access and capacity factor.

**Divertor** (C220108): Helios has a tokamak-like X-point divertor (novel for stellarators). QI stellarators use island divertors. The X-point approach leverages decades of tokamak experience and claims 10× better gas compression. **Cost direction: likely neutral to slight advantage** — the divertor is tungsten in both cases, but better pumping efficiency may reduce vacuum system costs.

### vs. 10-large-scale-stellarator (Gauss Fusion — large-scale W7-X successor)

**Scale**: Gauss Fusion pursues a W7-X-class large stellarator with LTS or LTS+HTS magnets. Helios at R = 8 m is similar in scale to ARIES-CS but uses a fundamentally different coil architecture.

**Magnet technology** (C220103): Gauss may use LTS (Nb3Sn, W7-X heritage) or LTS+HTS. Helios uses all-HTS (REBCO) at 20 T. HTS enables higher field density and 20 K operation (simpler cryogenics than 4 K LTS). **Cost direction: uncertain** — HTS tape is currently more expensive per unit length but enables compactness; LTS is more mature but requires 4 K operation.

**Coil geometry**: Gauss Fusion likely uses 3D modular coils (W7-X heritage). Same planar vs. modular delta as above. **Cost direction: potential advantage** for Helios in manufacturing.

**Blanket uniformity** (C220101): Helios uniform 50 cm blanket vs. likely non-uniform blanket in a close-coupled modular coil design. **Cost direction: advantage** for Helios.

### vs. 20a-type-one-stellarator (Type One Energy)

**Coil approach** (C220103): Type One Energy uses a modular stellarator with HTS coils, targeting manufacturing-friendly designs. Both concepts aim to simplify stellarator coil manufacturing relative to W7-X, but via different strategies: Type One uses optimized-but-still-3D HTS coils; Helios uses planar coils with software control. **Cost direction: unclear** — both claim manufacturing advantages over W7-X but neither has published cost data.

**Field periods**: Type One may use more field periods (higher twist) while Helios uses 2 field periods. Fewer field periods generally means larger, more tokamak-like coils with bigger gaps for maintenance.

### vs. 20b-renaissance-stellarator (Renaissance Fusion)

**Coil manufacturing** (C220103): Renaissance Fusion uses laser-patterned HTS film deposited on cylindrical substrates — a radically different manufacturing approach from both conventional winding and Thea's planar pancake winding. **Cost direction: unknown** — both claim manufacturing disruption but via incompatible methods. Renaissance's approach eliminates tape winding entirely; Thea's simplifies it to planar geometry.

**Blanket** (C220101): Renaissance uses a flowing Li-LiH wall with Pb pebble neutron multiplier (Other/hybrid) vs. Helios's conventional DCLL Pb-17Li. Renaissance's blanket requires a per-concept cost override; Helios's is library-compatible. **Cost direction: advantage** for Helios in modeling tractability and maturity of blanket concept.

### vs. 36-helical-coil-stellarator (Helical Fusion — HESTIA, helical coil with HTS)

**Coil topology** (C220103): Helical Fusion uses continuous helical HTS coils (heliotron/torsatron approach, LHD heritage). Helios uses discrete planar coils. Helical coils are conceptually simpler (one continuous winding path) but extremely long and require complex 3D support structures. **Cost direction: uncertain** — helical coils avoid the N-coil control complexity of Helios but may have structural support cost penalties.

**Physics maturity**: Heliotron/torsatron stellarators (LHD heritage) have a strong experimental base but historically suffered higher energetic particle losses than optimized QA/QI designs. Helios's QA optimization claims superior alpha particle confinement. **Cost direction: advantage** for Helios if it translates to smaller required plasma volume for the same net power.

**First wall**: Helical Fusion may use different first wall materials. Helios's choice of V-4Cr-4Ti is distinctive and risky across all comparables.

### Summary of Family-Deltas

| Subsystem | Delta vs. Comparables | Cost Direction | Magnitude |
|-----------|-----------------------|----------------|-----------|
| Magnet coils (C220103) | Planar vs. 3D/helical/film | Potential advantage | Unknown — no cost data on either side |
| Blanket (C220101) | Uniform DCLL vs. non-uniform or exotic | Advantage (simplicity) | Moderate — avoids ARIES-CS non-uniformity problem |
| Maintenance (C220110) | Sector-based vs. port-based/field-period | Advantage (access, CF) | Moderate — enables 88% CF claim |
| First wall material | V-4Cr-4Ti vs. EUROFER97 | Penalty (maturity risk) | Potentially significant if V44 supply chain fails |
| Divertor (C220108) | Tokamak X-point vs. island | Neutral to slight advantage | Small — similar materials, better pumping |
| Heating (C220104) | Very low power (ignited) | Advantage | Small in absolute cost |

## Section 8: Sources

1. **Swanson, C.P.S. et al. (2025)** "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant." arXiv:2512.08027. *Primary technical source for the entire analysis — provides all design point parameters, engineering subsystem designs, plasma physics analysis, power flow, maintenance architecture, and fuel cycle.* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md`

2. **Thea Energy (2026)** "U.S. Department of Energy Certifies Thea Energy's Fusion Pilot Plant Preconceptual Design." Press release, January 13, 2026. *Provides DOE Milestone Program certification context, independent expert validation, and timeline (Eos 2030, Helios 2030s).* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-doe-certification-jan2026.md`

3. **Canis Prototype Paper** (arXiv:2503.18960, 2025). *Reports experimental results from the 3×3 superconducting planar coil array prototype — validates field shaping (0.56–0.60% RMS error), confirms REBCO conductor, demonstrates manufacturing repeatability across three suppliers, and establishes double-pancake takt time targets.* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md`

4. **Thea Energy website and press releases** (various dates). *High-level value proposition: mass-manufacturable planar magnets, software-controlled fields, elimination of complex 3D coils. No quantitative cost data.* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-website-and-press.md`

5. **ANS Nuclear Newswire** (2025-12-18, article 7628). *Journalistic coverage of Helios release with quotes from Carlos Paz-Soldan (Columbia) validating the X-point divertor innovation and planar coil manufacturing advantages.* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-03/sources/ans-news-2025-12-18-article-7628.md`

6. **Thea Energy Press Release — Peer-Reviewed Publications** (January 29, 2025). *Announces four Nuclear Fusion papers; provides Eos sizing context (< 40 MW input power, approximately half the linear dimension of Helios, ~0.2 g/day tritium production).* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-03/sources/thea-press-release-thea-energy-announces-peer-reviewed.md`

7. **Thea Energy Press Release — DOE Certification** (January 13, 2026). *Announces Thea Energy as first DOE Milestone Program awardee to complete design review certification.* Path: `knowledge/concept_research/05-planar-coil-stellarator/iter-03/sources/thea-press-release-u-s-department-of-energy-certifies-thea.md`
