## Design Point

- Name: GIGA commercial fusion power plant (Gauss Fusion CDR, 2025)
- Maturity: proposed-commercial
- P_native: 1000 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-cdr-review-2026.md
  - knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/gauss-fusion-partnerships-2025.md
  - knowledge/concept_research/10-large-scale-stellarator/iter-01/sources/helias-reactor-context.md

## 1. Availability of Data

**Rating: Moderate**

Gauss Fusion released a comprehensive 1,000+ page Conceptual Design Report (CDR) in 2025, validated by a 13-person independent expert panel chaired by Dr. Hartmut Zohm. The CDR executive summary remains behind a download gate, limiting public access to detailed technical specifications. However, substantial technical information is available through:

- Partnership announcements with European suppliers (ENEA, ICAS, KIT, FZJ, Tokamak Energy) specifying magnet conductor development, tritium breeding blanket design, and supply chain commitments
- A detailed MT29 conference abstract describing the 40-coil modular magnet system with demountable joints
- HELIAS reactor heritage studies (HSR4/18, HSR5/22) providing parametric foundations and blanket/divertor design precedents

> "The configuration HSR4/18 is more compact than the 5-period HSR5/22, which also may lead to a 20% cost reduction of the reactor core"
> — helias-reactor-context.md, §8 Conclusions

The company has disclosed:
- Plant-level power output (3 GW thermal → 1 GW electric)
- Magnet system architecture (40 non-planar modular coils, dual LTS/HTS conductor tracks, ~250 demountable joints per coil, conductor-in-plate construction)
- Supply chain material requirements (~10,000 tonnes vacuum vessel steel, ~35,000 tonnes SC coils, ~75 tonnes lithium)
- First wall neutron load (1 MW/m²) and blanket design life (5 years)

Key data gaps include:
- Blanket type (HCPB vs DCLL — both studied for HELIAS geometry, but Gauss Fusion's selection not public)
- Power conversion cycle (steam Rankine vs sCO₂ Brayton)
- Capital cost breakdown and LCOE projections (€15-18B total cost stated without CAS detail)
- Detailed confinement scaling and beta limits for the GIGA-specific plasma equilibrium

The HELIAS reactor studies provide strong analogues for systems-level parameters, but the extent to which GIGA's optimization differs from HSR4/18 is not fully disclosed. GIGA is based on W7-X experimental results and advances in stellarator optimization, suggesting potential improvements over the historical HELIAS designs.

## 2. Challenges in Capturing System Function

The following challenges are ranked by potential impact on LCOE modeling:

**1. 3D Magnet Geometry and Manufacturing Cost (High impact)**

Stellarator magnets are non-planar and non-axisymmetric — each of the 5 coil shapes must conform to complex 3D optimization requirements. While tokamak TF coils are azimuthally symmetric (one design replicated 18 times), GIGA's 40 coils comprise 5 distinct shapes each replicated 8 times via field-period symmetry. The "conductor-in-plate" construction and demountable joints (~250 per coil at target resistance ~1 nΩ) are engineering innovations without demonstrated cost baselines. The conductor cross-section (circular, ~55 mm diameter) must accommodate either LTS (Nb₃Sn, given 12-13 T peak fields exceed NbTi capability) or HTS (REBCO) interchangeably — a dual-track development strategy that hedges technology risk but complicates supply chain cost estimation.

> "In contrast to axisymmetric devices only two different shapes – inboard and outboard segment – are needed [for blankets], while the three-dimensional geometry requires a large number of different blanket segments"
> — helias-reactor-context.md, §7

HELIAS studies claimed magnet costs "far below those of an ITER-type tokamak reactor" based on lower field (10 T for NbTi at 1.8 K) and weight (<10,000 t total with support). GIGA targets higher fields (12-13 T peak), necessitating either Nb₃Sn or REBCO, both more expensive than NbTi per kA-m. The library's default magnet cost scaling may underestimate the 3D complexity penalty.

**2. Tritium Breeding in 3D Geometry (High impact)**

Stellarator blanket modules must conform to the bean-shaped, toroidally varying plasma cross-section. HELIAS blanket studies identified 80 distinct blanket segments per field period, each with unique curvature and cooling requirements. The bean-shaped inboard region (segment 5) showed structural stress violations under accident scenarios and presented shielding challenges due to "peculiar shape." TBR calculations for HELIAS geometries achieved 1.15 (HCPB) and 1.39 (DCLL), both adequate for self-sufficiency, but relied on idealized models with no inter-segment gaps. Real 3D geometry with maintenance gaps, penetrations, and support structures reduces effective breeding area.

Gauss Fusion partnered with KIT, FZJ, IDOM, and Alsymex to finalize TBB industrial design and fabricate prototype sub-assemblies, but the blanket type (HCPB vs DCLL) remains undisclosed. HCPB (He-cooled Li₄SiO₄ pebble bed) is lighter (7,080 t for HSR5/22) but achieves lower thermal efficiency (~35%). DCLL (self-cooled PbLi) offers >40% efficiency potential but weighs twice as much (14,450 t for HSR5/22, with 12,500 t of PbLi alone). The choice materially affects both capital cost (PbLi inventory at scale) and operational economics (thermal efficiency drives recirculating power fraction).

**3. Divertor Heat Load and Lifetime (Moderate impact)**

Stellarator divertors must handle strike-point heat fluxes on complex 3D island-chain structures. HELIAS studies reported "thermal load of more than 10 MW/m²" on target plates — comparable to tokamak divertor loads despite stellarators lacking ELMs. The first wall neutron load of 1 MW/m² (average) with 5-year blanket life is less punishing than tokamak DEMO targets (2 MW/m², 2-3 year life), but HELIAS studies also noted that 140 dpa structural limits could enable 9-year component life — GIGA's 5-year design conservatively assumes 70 dpa.

The economic sensitivity is capacity factor: replacing blanket modules every 5 years requires extended shutdowns unless the modular maintenance concept (segment replacement through portholes between coils) achieves rapid turnaround. HELIAS proposed 8 portholes per field period (4 top, 4 bottom) for segment extraction without removing entire coil periods. If blanket replacement requires >3 months, capacity factor degrades materially.

**4. MHD Stability at Design Beta (Moderate impact)**

HELIAS HSR4/18 and HSR5/22 studies targeted β = 4.2-4.24%, which simulations showed at the MHD stability limit. Achieving ignition in these configurations required empirical LGS scaling law predictions; the competing ISS04 scaling predicted insufficient confinement. GIGA is optimized using W7-X experimental results and modern stellarator optimization codes (likely CAS3D or VMEC), which may resolve the HSR4/18 beta-limit concerns. However, no public GIGA equilibrium or stability analysis is available. If beta is limited to <4%, fusion power drops by ~15% (scaling roughly linearly with beta at fixed density and temperature), requiring either larger plasma volume or higher density/temperature to maintain 3 GW fusion power.

> "Further theoretical studies are needed to clarify the confinement at the beta-limit, which is expected around 4.3%"
> — helias-reactor-context.md, §8 Conclusions

**5. Confinement Scaling Uncertainty (Moderate impact)**

Stellarator energy confinement time does not follow tokamak H-mode scaling laws. HELIAS studies relied on LGS (Lackner-Gottardi Scaling), which predicted adequate confinement (τ_E ~ 1.6 s for 3 GW fusion power), but warned that ISS04 scaling was too pessimistic. W7-X has produced improved confinement scaling data, and GIGA likely assumes updated empirical fits. However, stellarator confinement physics at reactor-scale plasma volume (1,500 m³, more than 10× W7-X) and density (2.1-2.6 × 10²⁰ m⁻³) remains extrapolated. A 20% confinement degradation relative to projections would require correspondingly higher fusion power to maintain net electric output, increasing reactor size and cost.

## 3. Maturity of Key Subsystems and Components

Subsystems ranked from least to most mature:

**Tritium Breeding Blanket for 3D Stellarator Geometry (TRL 2-3)**

- **On paper only**: Neutronic and thermomechanical studies completed for HELIAS HCPB and DCLL blanket concepts. TBR values of 1.15 (HCPB) and 1.39 (DCLL) calculated with idealized geometry. KIT structural analysis identified stress violations in bean-shaped inboard segments.
- **Missing at scale**: Fabrication and testing of 3D-conformal blanket segments with real gaps, penetrations, and support structures. Prototype sub-assemblies under development with Alsymex (French ITER supplier) but not yet demonstrated. Tritium extraction from flowing PbLi or He-purged pebble beds at fusion-relevant throughput unproven.

**Demountable High-Field Superconducting Coils (TRL 3-4)**

- **Demonstrated**: Tokamak Energy demonstrated HTS tokamak operation at 11.8 T in-vessel field (Demo4, November 2025). Commonwealth Fusion Systems tested 20 T REBCO magnet (SPARC prototype, January 2026). Both prove HTS technology at GIGA-relevant fields.
- **On paper only**: Demountable joints in complex 3D stellarator coil geometry. GIGA targets ~1 nΩ joint resistance across ~250 joints per coil — 10× more joints than ITER TF coils. Conductor-in-plate construction avoids traditional coil casings but has no built precedent.
- **Missing at scale**: Full-scale non-planar modular coil with demountable joints tested under cyclic electromagnetic loads. Each coil is ~300 tonnes with ~30-35 m perimeter — comparable to ITER TF magnets but in far more complex geometry. KIT developing prototypes with €9M BMBF funding.

**3D Divertor for Island-Chain Heat Exhaust (TRL 3-4)**

- **Demonstrated**: W7-X operates with island divertor, demonstrating concept viability. Detachment control and strike-point mapping validated.
- **On paper only**: Reactor-scale island divertor handling 10+ MW/m² steady-state heat flux on 3D target geometry.
- **Missing at scale**: Tungsten monoblock target plates fabricated to complex 3D curvature with embedded cooling. W7-X divertor is water-cooled copper; GIGA requires He-cooled W on structural steel at 500°C material limits.

**Plasma Heating and Fueling (TRL 5-6)**

- **Demonstrated**: ECRH at 140 GHz, multi-MW continuous operation on W7-X (10 MW installed, 170 GHz gyrotrons under test). Pellet injection for fueling demonstrated.
- **On paper only**: ECRH as primary startup and profile control for reactor-scale stellarator. GIGA likely requires 50-100 MW ECRH (estimated, not disclosed) for initial heating and burn control — 5× W7-X capability.
- **Missing at scale**: 170+ GHz gyrotrons at 2+ MW CW each, deployed in arrays of 25-50 units. Supply chain exists (European Microwave Signature Laboratory, Thales, CPI) but not at reactor-plant production volume.

**Helium-Cooled First Wall and Blanket Structures (TRL 5-6)**

- **Demonstrated**: ITER TBM program includes HCPB blanket modules with He cooling at 8 MPa, Li₄SiO₄ breeder pebbles, and Be multiplier. Preliminary Design Review expected 2026.
- **On paper only**: HCPB adapted to stellarator bean-shaped geometry with toroidally varying cross-section. 80 distinct segment designs per field period.
- **Missing at scale**: 14.1 MeV neutron testing of RAFM steel structures (EUROFER 97) under combined thermal, pressure, and electromagnetic loads to 70-140 dpa. No fusion-neutron test facility exists at required fluence.

**Non-Planar Vacuum Vessel (TRL 6-7)**

- **Demonstrated**: W7-X vacuum vessel is a complex 3D structure (bean-shaped cross-sections in 5 field periods) with ports and diagnostic access. Full-scale fabrication and leak-tight assembly proven.
- **Missing at scale**: GIGA vessel is far larger (major radius ~18 m vs W7-X's ~5.5 m) with 3 GW thermal power loading and 8 MPa He blanket pressure interfacing to vessel. Vessel-blanket interface sealing and thermal expansion management at scale.

**Cryogenic Helium Cooling and Cryostat (TRL 7-8)**

- **Demonstrated**: Large-scale He refrigeration plants (ITER-scale, ~75 kW at 4.5 K) are built and tested. W7-X cryostat encloses superconducting coils in 21,500 m³ volume.
- **Missing at scale**: GIGA cryostat volume not disclosed but likely larger than W7-X. If LTS conductor (Nb₃Sn at 1.8 K forced-flow He) is chosen, sub-2 K cooling at multi-kW scale required — beyond current industrial refrigeration plants.

**Power Conversion and Balance of Plant (TRL 8-9)**

- **Demonstrated**: Steam Rankine and sCO₂ Brayton cycles at GW scale in fission plants. Helium-heated intermediate heat exchangers (He/steam interface) tested in HTGR programs.
- **Missing at scale**: Integration of He-cooled HCPB blanket (if chosen) or PbLi-cooled DCLL blanket (if chosen) with power conversion cycle under fusion-specific transients (startup/shutdown thermal cycling, possible plasma disruptions or off-normal events).

## 4. Key Materials and Supply Chain Considerations

**HTS and LTS Superconductor**

Gauss Fusion pursues dual-track magnet development: LTS (likely Nb₃Sn, given 12-13 T peak field exceeds NbTi limits) and HTS (REBCO via Tokamak Energy partnership and ENEA cable development). The common conductor cross-section (~55 mm circular) allows interchangeable use — a technology-hedge strategy.

For LTS: ~800 tonnes of Nb₃Sn conductor required (per gauss-fusion-technical-summary.md §Supply Chain Requirements). Nb₃Sn is strain-sensitive and requires react-and-wind or wind-and-react fabrication. At ~$200-300/kg for Nb₃Sn strand, raw material cost is ~$160-240M. The 3D coil winding and conductor-in-plate construction add substantial manufacturing complexity.

For HTS: 26 million meters of REBCO tape at ~$30-100/kA-m (current pricing, trending toward $10/kA-m at volume). If GIGA targets 100 kA operating current and 260 m tape length per kA-m (at 4 K, 12 T), total cost is ~$780M-2.6B at current pricing, falling to ~$260M at projected volume pricing. REBCO supply chain (Shanghai Superconductor, SuperPower, Fujikura) is scaling but not yet at fusion-plant production volume. Commonwealth Fusion Systems and Tokamak Energy are the lead customers driving REBCO production scaling; Gauss Fusion's HTS partnership with Tokamak Energy provides access to this supply chain.

The dual-track strategy implies Gauss Fusion has not yet committed to a magnet conductor, deferring the decision until both LTS and HTS prototype coils are tested. This flexibility hedges technology risk but complicates supply chain commitments and cost certainty.

**Tritium**

GIGA requires ~75 tonnes of lithium inventory (per gauss-fusion-technical-summary.md). If the blanket is HCPB with Li₄SiO₄ ceramic breeder, lithium is bound in ceramic form, not elemental. If DCLL with liquid PbLi, the 14,450 t blanket includes 12,500 t of PbLi eutectic (15.7% Li by weight = ~1,960 t Li). The 75 t figure likely refers to the elemental lithium content.

Enrichment to 90% Li-6 (for adequate TBR without excessive blanket thickness) is required. Li-6 is currently produced at small scale (Russia and China via mercury amalgam process, Oak Ridge Y-12 via COLEX). Scaling to multi-tonne annual production for a fusion fleet requires new Li-6 separation facilities. At current commodity prices (~$9-15/kg elemental Li metal), raw lithium cost is $675k-1.1M, negligible compared to enrichment and fabrication. Tritium startup inventory (~1 kg at $35,000/g) is $35M.

**RAFM Steel and Tungsten**

EUROFER 97 or similar RAFM steel for blanket structures and first wall operates to 500°C and ~70-140 dpa neutron damage. RAFM production is low-volume specialty steel (~$30-50/kg vs $1-3/kg for commercial stainless). GIGA blanket structural mass not disclosed, but HELIAS HCPB blanket was ~7,080 t total (including breeder/multiplier); structural steel fraction ~30-40% → ~2,100-2,800 t RAFM. At $40/kg, ~$84-112M raw material.

Tungsten armor on the first wall and divertor: 2 mm thick layer covering first wall surface area (~2,600 m² per HELIAS HSR5/22). Tungsten density 19.3 g/cm³ → ~100 tonnes W for 2 mm × 2,600 m². At ~$30-50/kg, raw tungsten ~$3-5M. Fabrication of W monoblocks bonded to CuCrZr or steel heat sinks is the cost driver (~$1,000-2,000/kg installed per tokamak divertor experience).

**Beryllium**

HELIAS HCPB blanket uses Be pebble bed as neutron multiplier (40 mm layers per segment). Total Be mass for HELIAS not stated, but ITER TBM HCPB modules use ~60 kg Be per module; GIGA with 80 segments per period × 4 periods = 320 segments → ~19.2 tonnes Be if scaled linearly. Beryllium supply is constrained (~300 tonnes/year global production, dominated by Materion Corp). Be cost ~$800/kg → $15M raw material. Beryllium pebble fabrication and handling (toxic, pyrophoric) add cost.

If Gauss Fusion selects DCLL blanket instead of HCPB, Be demand drops to zero but PbLi inventory increases to 12,500 tonnes. PbLi at ~$5-10/kg → $62.5-125M for coolant/breeder inventory.

**Vacuum Vessel Steel**

~10,000 tonnes stainless steel (likely 316L) for vacuum vessel and support structures. At $3-5/kg for nuclear-grade stainless, ~$30-50M raw material. Complex 3D fabrication and welding (bean-shaped cross-sections with toroidal variation) drive installed cost far above raw material.

## 5. Design Point Parameters

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Geometry** |  |  |  |  |
| R0 (major radius) | 18.0 m | helias-reactor-context.md §Table II; gauss-fusion-technical-summary.md confirms GIGA is HSR4/18 derivative | high | HELIAS HSR4/18 documented value; GIGA CDR not public but partnerships and geometry consistent with HSR4/18 |
| a (plasma minor radius) | 1.7 m | analyst-patch-spec-anchors.md §Verified spec values; derived from HSR4/18 cross-section | high | Effective average for bean-shaped stellarator cross-section. Spec key: `plasma_t` |
| Plasma volume | 1,500 m³ | gauss-fusion-technical-summary.md §GIGA Power Plant — Key Specifications | high | Spec key: `plasma_volume` |
| Elongation (effective) | 1.6 | analyst-patch-spec-anchors.md §Verified spec values | medium | Averaged over toroidally varying bean/triangular cross-sections. Spec key: `elon` |
| Field periods | 4 | helias-reactor-context.md §Abstract; gauss-fusion-cdr-review-2026.md confirms "four period quasi isodynamic plasma" | high | Distinguishes HSR4/18 from HSR5/22 (5 periods) |
| **Magnetic Field** |  |  |  |  |
| B0 (on-axis field) | 6.0 T | gauss-fusion-technical-summary.md §GIGA Power Plant; analyst-patch-spec-anchors.md | high | Spec key: `B` (NOT `B0` — canonical name is `B`) |
| B_peak (on conductor) | 12-13 T | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Informational only; library uses on-axis B for scaling |
| **Power and Performance** |  |  |  |  |
| P_fusion | ~3,000 MW | gauss-fusion-technical-summary.md §GIGA Power Plant (3 GW thermal); helias-reactor-context.md §Table II (HSR4/18: 2,800 MW) | high | Informational only — `p_fus` back-solved by library from `p_input` + `P_native`. Do NOT put in spec |
| P_native (net electric) | 1,000 MWe | gauss-fusion-technical-summary.md §GIGA Power Plant (3 GW thermal → 1 GW electric) | high | Spec key: `P_native`. Drives module count at 1 GWe fleet comparison |
| p_input (auxiliary heating) | 75 MW | analyst-patch-spec-anchors.md §Verified spec values (ECRH for startup/profile control; 50-100 MW band) | medium | Estimated from HELIAS studies and stellarator heating requirements. Spec key: `p_input` |
| Thermal efficiency (implied) | 33% | [inferred: 1,000 MWe / 3,000 MWth] | medium | 3 GW thermal → 1 GW electric. Consistent with steam Rankine; DCLL blanket could enable 40%+ |
| Average beta | 4.2% | helias-reactor-context.md §Table II (HSR4/18) | medium | At MHD stability limit per HELIAS studies. GIGA optimization may differ |
| Required τ_E | 1.6 s | helias-reactor-context.md §Table II (HSR4/18 LGS scaling prediction) | medium | LGS scaling; ISS04 was pessimistic. GIGA likely assumes improved W7-X-validated scaling |
| Central temperature | 15 keV | helias-reactor-context.md §Table II | medium | HELIAS design point; GIGA specifics not disclosed |
| Average density | 2.1-2.6 × 10²⁰ m⁻³ | helias-reactor-context.md §Table II (HSR4/18: 2.12; HSR5/22: 2.6) | medium | Range from HELIAS variants; GIGA value within this band |
| **First Wall and Blanket** |  |  |  |  |
| First wall neutron load (avg) | 1.0 MW/m² | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Lower than tokamak DEMO (~2 MW/m²); enables longer component life |
| First wall area | ~2,600 m² | helias-reactor-context.md §7 (HSR5/22); GIGA likely similar | medium | Drives blanket surface area and segment count |
| Blanket design life | 5 years | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Conservative vs HELIAS studies (9 years possible at 140 dpa limit) |
| Magnet/vessel life | 40 years | gauss-fusion-technical-summary.md §GIGA Power Plant | high | Stellarator advantage: no disruptions → longer component life |
| **Magnet System** |  |  |  |  |
| Number of coils | 40 | gauss-fusion-technical-summary.md §Magnet System (5 shapes × 8 via symmetry) | high | Non-planar modular coils |
| Coil mass (each) | ~300 tonnes | gauss-fusion-technical-summary.md §Magnet System (comparable to ITER TF magnets) | high | Total magnet system ~35,000 tonnes including support |
| SC conductor type | LTS+HTS dual | gauss-fusion-partnerships-2025.md; gauss-fusion-technical-summary.md §HTS Partnerships | high | LTS likely Nb₃Sn (12-13 T exceeds NbTi); HTS is REBCO via Tokamak Energy |
| Demountable joints/coil | ~250 | gauss-fusion-technical-summary.md §Magnet System | high | Target resistance ~1 nΩ each |
| Conductor cross-section | Circular, ~55 mm diameter | gauss-fusion-technical-summary.md §Magnet System | high | Common format allowing LTS/HTS interchangeability |
| **Materials and Supply Chain** |  |  |  |  |
| Vacuum vessel steel | ~10,000 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | medium | Likely 316L stainless |
| SC coil total mass | ~35,000 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | medium | Includes conductor, structure, cryostat |
| LTS conductor | ~800 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements | medium | If Nb₃Sn selected |
| HTS conductor | 26M meters | gauss-fusion-technical-summary.md §Supply Chain Requirements | medium | If REBCO selected |
| Lithium inventory | ~75 tonnes | gauss-fusion-technical-summary.md §Supply Chain Requirements; gauss-fusion-partnerships-2025.md | medium | Elemental Li content in breeder (HCPB or DCLL) |
| Blanket type | TBD | [No public disclosure; HCPB vs DCLL both studied for HELIAS; KIT/FZJ/IDOM/Alsymex finalizing design per gauss-fusion-partnerships-2025.md] | low | HCPB: He-cooled Li₄SiO₄ pebbles, 7,080 t, TBR~1.15, ~35% η_th. DCLL: self-cooled PbLi, 14,450 t, TBR~1.39, >40% η_th |
| **Costing and Project Data** |  |  |  |  |
| Total project cost (FOAK) | €15-18 billion | gauss-fusion-technical-summary.md §Funding | low | Top-level estimate without CAS breakdown |
| Commissioning target | 2040-2045 | gauss-fusion-technical-summary.md §Roadmap | medium | Grid connection and European rollout |

## 5b. Override Candidates

After walking every canonical 1costingFE account for this archetype (stellarator D-T), **zero overrides are proposed**. The dossier provides no company-grounded unit costs, published dollar figures, or quantitative evidence that justifies departing from the library defaults.

**Rationale**: Gauss Fusion disclosed a top-level €15-18B total cost estimate but no CAS-level breakdown. The HELIAS heritage studies (HSR4/18) claimed "20% reactor core cost reduction" vs HSR5/22 and magnet costs "far below ITER-type tokamak" based on lower field (10 T NbTi) and total weight (<10,000 t). However, GIGA targets 12-13 T peak field, requiring either Nb₃Sn or REBCO — both more expensive than NbTi per kA-m. The conductor-in-plate construction and demountable joints are innovations without demonstrated cost data. Without published magnet procurement costs, blanket fabrication costs, or building cost estimates grounded in GIGA-specific design, no override value can be defensibly anchored to company data.

The expected override count for Archetype-Fit = High is 0-4 enabled overrides. Zero overrides is within this band and reflects honest data availability: GIGA is a conceptual design with supplier partnerships in place but no constructed hardware or bottom-up cost estimates in the public domain.

```yaml
overrides: []
```

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Blanket type (HCPB vs DCLL) | S5 | proprietary | important | CDR access or KIT/FZJ technical publication on Gauss Fusion TBB design |
| 2 | Power conversion cycle (steam Rankine vs sCO₂ Brayton) | S5 | proprietary | important | CDR access; determines thermal efficiency and BOP capital cost |
| 3 | Capital cost breakdown by CAS account | S5b | proprietary | blocking | CDR cost section or Gauss Fusion investor deck with detailed CAPEX |
| 4 | Magnet conductor selection (LTS vs HTS) | S5 | not-yet-decided | important | Technology decision expected post-prototype testing (KIT demountable coil program) |
| 5 | ECRH system specification (power, frequency, gyrotron count) | S5 | proprietary | important | CDR or technical presentation on auxiliary heating |
| 6 | Confinement scaling law and beta limit for GIGA equilibrium | S5, S2 | proprietary | important | Peer-reviewed publication on GIGA plasma optimization or CDR physics chapter |
| 7 | Blanket replacement duration and capacity factor impact | S2, S3 | not-yet-sourced | important | Remote maintenance plan from CDR or engineering studies on stellarator segment replacement |
| 8 | Demountable joint resistance achieved in prototypes | S3, S4 | truly-unknown | important | KIT prototype test results (€9M BMBF-funded program) when published |
| 9 | First wall and blanket segment count and masses | S4, S5 | proprietary | nice-to-have | CDR mechanical design chapter or supplier (Alsymex) fabrication data |
| 10 | Divertor heat flux distribution and target design | S2, S3 | proprietary | important | CDR divertor chapter or plasma edge modeling publication |
| 11 | Cryogenic refrigeration power for LTS option | S4, S5 | derivable | nice-to-have | Calculable from conductor mass and cooling requirements if LTS type (Nb₃Sn) is confirmed |
| 12 | HTS tape length and current-carrying capacity | S4, S5 | proprietary | nice-to-have | Tokamak Energy partnership deliverables or ENEA cable development reports |

## 7. Family-Delta vs Comparables

The fixed comparables are: 05-planar-coil-stellarator (Thea Energy), 09-qi-stellarator-hts (Proxima Fusion), 20a-type-one-stellarator, 20b-renaissance-stellarator, 36-helical-coil-stellarator.

### vs 05-planar-coil-stellarator (Thea Energy)

**Coil architecture divergence (cost penalty for GIGA)**: Thea Energy uses planar HTS coils in rectangular arrays, producing stellarator fields via current distribution optimization rather than 3D coil shaping. Planar coils are manufacturable with conventional racetrack winding; GIGA's non-planar modular coils require complex 3D winding fixtures and conductor-in-plate stacking. Thea's approach trades off plasma optimization (lower performance at given size) for manufacturing simplicity. GIGA invests in the HELIAS optimization (superior confinement, lower coil forces) at the cost of complex fabrication. Magnitude: Non-planar coil fabrication likely adds 30-50% to per-coil cost vs planar equivalents, but GIGA requires fewer coils (40 vs Thea's estimated 100+) and achieves higher performance per unit volume.

**Demountable joints (potential GIGA advantage)**: GIGA's ~250 demountable joints per coil (target ~1 nΩ) enable sector-based maintenance without removing entire coil periods. Thea Energy's planar coils also pursue demountability but in simpler geometry. If GIGA achieves its joint resistance target, maintenance downtime could be shorter than concepts requiring full coil removal. If joints underperform (>10 nΩ), resistive heating adds to cryogenic load and recirculating power. Status: Unproven at scale for both concepts.

**Plasma performance (GIGA advantage)**: HELIAS quasi-isodynamic optimization produces lower neoclassical transport and better fast-particle confinement than generic planar-coil stellarators. At comparable field and size, GIGA likely achieves 1.5-2× longer confinement time, reducing required plasma volume and vessel size for the same fusion power. This translates to ~20-30% lower reactor capital cost at fixed power output (per HELIAS studies comparing HSR4/18 vs simpler configurations).

### vs 09-qi-stellarator-hts (Proxima Fusion)

**Scale and power output (opposite extremes)**: Proxima Fusion targets compact HTS quasi-isodynamic stellarators (Stellaris: likely R0 ~3-5 m, ~100-300 MWe). GIGA is a gigawatt-class device (R0 = 18 m, 1,000 MWe). Both use QI optimization but at radically different scale. Small reactors benefit from HTS enablement (higher field in compact volume), while large reactors can achieve performance with lower field (GIGA's 6 T on-axis vs Proxima's likely 8-10 T). Cost per kWe likely favors large scale (GIGA) due to economy of scale in BOP and fixed costs; cost per kWe per development timeline favors compact (Proxima) due to faster iteration and lower FOAK capital.

**Conductor strategy (Proxima HTS-only vs GIGA dual-track)**: Proxima Fusion commits to HTS (REBCO) magnets exclusively, leveraging Tokamak Energy partnership. GIGA hedges with dual LTS/HTS development. Proxima's single-track approach accelerates supply chain scaling and manufacturing learning; GIGA's dual-track preserves fallback if REBCO supply chain or performance (e.g., AC loss, quench protection) proves problematic. Cost implication: GIGA's dual-track adds R&D cost but derisks schedule; Proxima's HTS commitment is cheaper if REBCO scaling succeeds, costlier if it fails.

**Blanket architecture (comparable challenge)**: Both face 3D blanket segmentation challenges. At GIGA's scale, absolute segment count is higher (80 per period × 4 periods = 320 total, though symmetry reduces unique designs to ~20-25); at Proxima's scale, tighter radial build constraints and higher neutron wall load (compact machine at high power density) stress materials. Comparable difficulty, different limiting factors.

### vs 20a-type-one-stellarator (Type One Energy)

**Optimization heritage (HELIAS vs MUSE)**: GIGA descends from HELIAS (German W7-X lineage); Type One Energy uses MUSE optimization (PPPL/U. Wisconsin lineage). Both are quasi-isodynamic but with different magnetic field spectra and modular coil geometries. HELIAS historically emphasized lower aspect ratio and compact core; MUSE emphasized simpler coil shapes and lower engineering complexity. Cost comparison is speculative without detailed coil designs for both, but HELIAS HSR4/18 claimed "20% cost reduction" vs 5-period HSR5/22 by reducing field periods (4 vs 5) — Type One Energy's field-period count not disclosed.

**Magnet technology (uncertain for Type One)**: Type One Energy has not disclosed conductor type (LTS vs HTS). If LTS at lower field (<10 T, NbTi feasible), coil costs favor Type One; if HTS at high field, comparable to GIGA's HTS track. GIGA's dual-track strategy derisks but adds development cost.

**Scale and maturity (GIGA larger, Type One earlier-stage)**: GIGA targets 1 GWe commercial from the start; Type One Energy likely pursuing smaller pilot-scale first. Development cost and time-to-first-plasma favor smaller concepts; cost per kWe at volume production favors larger.

### vs 20b-renaissance-stellarator (Renaissance Fusion)

**Coil fabrication (laser-patterned HTS film vs wound conductor)**: Renaissance Fusion's laser-patterned HTS film on cylindrical substrates is a radically different manufacturing approach than GIGA's conductor-in-plate wound coils. Renaissance avoids winding fixtures and complex conductor assembly but requires large-area HTS film deposition at thickness and current density not yet demonstrated. If Renaissance's fabrication succeeds, per-coil cost could drop below wound-coil approaches by 50%+; if film uniformity or current density underperforms, fallback to conventional winding is costly. GIGA's conventional winding is lower-risk, higher-cost.

**Blanket chemistry (Renaissance's Li-LiH flowing wall vs GIGA's solid/liquid breeder)**: Renaissance uses flowing liquid Li-LiH wall with Pb pebble neutron multiplier — a hybrid architecture with no tokamak or stellarator precedent. GIGA's blanket (HCPB or DCLL) is based on tokamak TBM heritage. Renaissance's approach simplifies FW/blanket replacement (liquid is self-healing, Pb pebbles are batch-replaceable) but introduces unknowns in Li-LiH chemistry, tritium extraction, and corrosion. GIGA's solid-breeder or liquid-PbLi approach is higher-maturity, higher-maintenance.

**Cost implication**: Renaissance's innovations target manufacturing cost reduction (film deposition, flowing liquid) vs GIGA's optimization focus (QI physics, demountable joints for maintenance). Renaissance's ceiling is lower if innovations fail; GIGA's floor is higher due to conventional high-maturity components.

### vs 36-helical-coil-stellarator

**Coil topology (modular vs helical)**: Helical-coil stellarators (e.g., LHD) use continuous helical windings wrapping the plasma toroidally; GIGA uses discrete modular coils. Helical coils produce smoother magnetic field spectra (lower ripple, better confinement) but are difficult to wind in superconducting materials (strain-sensitive Nb₃Sn or REBCO) and nearly impossible to demount for maintenance. Modular coils accept slightly higher ripple but enable demountable joints and sector-based maintenance. Cost-confinement tradeoff: helical winding may reduce confinement degradation by ~10-15% (enabling smaller reactor), but non-demountable coils force full-period removal for blanket changeouts, devastating capacity factor. GIGA's modular demountable approach is optimized for maintenance access at the cost of ~5-10% larger plasma volume.

**Historical cost context**: LHD (R0 = 3.9 m, helical coils, built 1998) cost ~$300M but is a physics experiment, not a power plant. Scaling to GIGA's 18 m major radius and 3 GW thermal power with helical coils would require continuous multi-kilometer SC winding with no joints — manufacturing risk is prohibitive. Modular coils are costlier per unit length but manufacturable.

## 8. Sources

Listed in order of analytical importance:

1. **helias-reactor-context.md** (HELIAS HSR4/18 and HSR5/22 reactor studies, German stellarator program) — Provides parametric foundations for GIGA: major radius (18 m), plasma volume (1,500 m³), fusion power (2,800-3,000 MW), magnet system mass (<10,000 t), blanket options (HCPB 7,080 t / DCLL 14,450 t), thermal efficiency (35-40%), first wall lifetime (4.6-9 years at 1 MW/m²), confinement scaling (LGS predicts ignition), beta limit (4.2% at MHD stability boundary), and "20% cost reduction" for HSR4/18 vs HSR5/22. Critical for design point parameter extraction where GIGA-specific data is unavailable.

2. **gauss-fusion-technical-summary.md** (Gauss Fusion CDR summary, 2025) — Official GIGA specifications: 3 GW thermal → 1 GW electric, 6 T on-axis / 12-13 T peak field, 1 MW/m² neutron load, 5-year blanket life, 40-year magnet life, 40 coils (5 shapes × 8), conductor-in-plate construction, ~250 demountable joints per coil at ~1 nΩ target, dual LTS/HTS development, material quantities (~10,000 t vessel steel, ~35,000 t magnets, ~800 t LTS or 26M m HTS, ~75 t Li), €15-18B total cost, 2040-2045 commissioning target. Primary source for GIGA-specific values.

3. **helias-blanket-studies.md** (KIT structural and neutronic analysis of HCPB blanket for HELIAS 5-B geometry, 2022) — 80 blanket segments per field period with complex 3D curvature, bean-shaped inboard segment (segment 5) stress violations, TBR = 1.39 with idealized geometry (no gaps), EUROFER 97 RAFM steel at 500°C limit, Li₄SiO₄ and Be pebble bed layers, He cooling at 8 MPa, structural concerns for segment 5 under accident scenarios. Demonstrates blanket engineering challenges for stellarator geometry.

4. **gauss-fusion-partnerships-2025.md** (partnerships with KIT, FZJ, IDOM, Alsymex, ENEA, ICAS, Tokamak Energy, 2025) — KIT/FZJ/IDOM finalizing industrial TBB design, Alsymex fabricating prototype sub-assemblies, ENEA developing HTS cables and joints, ICAS manufacturing LTS cables and maturing HTS processes, Tokamak Energy HTS magnet collaboration. Confirms supply chain commitments and development status.

5. **gauss-fusion-cdr-review-2026.md** (13-person expert panel review chaired by Hartmut Zohm, January 2026) — CDR validation by independent experts, systems engineering approach praised, transition to engineering phase confirmed. Establishes design maturity and credibility.

6. **analyst-patch-spec-anchors.md** (spec provenance document for model reproducibility, 2026) — Verified canonical spec values for 1costingFE modeling: R0 = 18.0 m, plasma_t = 1.7 m, plasma_volume = 1,500 m³, B = 6.0 T, elon = 1.6, P_native = 1,000 MWe, p_input = 75 MW. Ensures cold-start model regeneration matches prior analyses.

**External references** (not in dossier but cited for context):
- W7-X experimental results (Max Planck Institute for Plasma Physics) — validates quasi-isodynamic stellarator confinement scaling
- ITER TBM program (F4E, JAEA, US ITER) — HCPB blanket module development and testing
- Tokamak Energy Demo4 HTS magnet test (11.8 T in-vessel, November 2025) and CFS SPARC 20 T REBCO magnet (January 2026) — demonstrate HTS technology at GIGA-relevant fields
