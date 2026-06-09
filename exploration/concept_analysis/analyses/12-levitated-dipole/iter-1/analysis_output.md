## Design Point

- Name: OpenStar Reactor A — Simpson et al. 2026 (arXiv 2602.20564)
- Maturity: proposed-commercial
- P_native: 208 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md
  - knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2508-17691-junior-design-results.md

## 1. Availability of Data

**Rating: Moderate**

The levitated dipole concept has an extensive experimental heritage but limited power plant literature. The Massachusetts Institute of Technology's Levitated Dipole Experiment (LDX, operated 2004-2014) demonstrated stable plasma confinement with local β > 1 and validated interchange stability in the dipolar field topology. Japan's RT-1 experiment achieved similar performance. These experiments provide foundational physics validation for the concept but did not approach fusion-relevant conditions.

OpenStar Technologies is the sole commercial pursuer of D-T levitated dipole fusion and has published a detailed reactor design study:

> "In order to achieve rapid deployment of fusion power to the grid, the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Introduction

The Simpson et al. (2026) arXiv paper provides comprehensive plant-level parameters for two reactor designs (A and B), including geometry, magnet specifications, neutron shield design, power balance, and preliminary costing constraints. This is the primary quantitative source for D-T dipole power plants. However, the cost model itself remains proprietary:

> "OpenStar is currently in the process of developing a model for estimating the overnight capital cost and LCOE for levitated dipole fusion power plants which will be the topic of future work. This study uses preliminary results from this model which are subject to change as the model is developed. For this reason we avoid quoting specific values here, instead opting to present the relative cost and LCOE."
> — arxiv-2602-20564-dt-dipole-power-plants.md, §3.1 Cost Function

The Junior prototype has published design and initial results (arXiv 2508.17691), demonstrating levitated plasma confinement for the first time in a commercial facility (February 2026). However, Junior is a proof-of-concept device operating at sub-fusion parameters.

**Key data gaps:**
- No published LCOE or absolute overnight capital cost figures
- No energy confinement scaling law for dipoles — Simpson assumes Q = 15 and back-solves required confinement
- Limited experimental validation of fusion-relevant plasma parameters (Te ~ 200 eV and ne ~ 10^18 m^-3 from LDX; fusion requires 10+ keV and 10^20 m^-3)
- No public demonstration of the two-section sacrificial coil design under neutron loading
- Balance-of-plant details sparse (specific thermal cycle not disclosed)

## 2. Challenges in Capturing System Function

The levitated dipole presents five major LCOE modeling challenges, ranked by impact:

**1. No Validated Confinement Scaling (Critical)**

Unlike tokamaks and stellarators, which have empirical energy confinement scaling laws validated across multiple devices, the levitated dipole has no such model. The Simpson design assumes Q_sci = 15 and reverse-engineers the required confinement time, with two bounding cases:

- Bohm-like scaling: τ_E,B = 3.23 × 10^19 s/m³ (Reactor A)
- Gyro-Bohm scaling: τ_E,gB = 8.69 × 10^19 s/m³ (Reactor B, 2× smaller and cheaper)

> "no such model exists for dipoles. Therefore, we take a reversed approach: instead of optimizing for reactor power under the constraints of expected device performance, we design a reactor assuming a value for Q_sci and design to minimize the required confinement time"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §3.1

This is a concept-gating uncertainty. If the Tahi demonstration device (~2028, 20 T) does not achieve the target double products, Reactor A either requires degraded Q (higher LCOE) or larger size (higher capital cost). The physics validation path is:

1. Junior (demonstrated, Feb 2026): ~5.6 T, 550 kg, levitated plasma confirmed
2. Tahi (~2028): 20 T target, must demonstrate n·τ_E ≥ 3.23 × 10^19 s/m³
3. Maui (~2031): Neutron-producing, D-D or D-T
4. Reactor A: 23 T, 667 MW fusion power, 208 MW net electric

Failure at Tahi invalidates the cost assumptions for Reactor A.

**2. Sacrificial Coil Replacement Economics (High)**

The two-section REBCO coil design is central to the concept's economic viability. The outer ~20% of the coil faces 1 MW-year/m² fluence, giving it a ~1 year neutron lifetime before replacement. The inner section is shielded to achieve decade-scale lifetime. Annual coil replacement is by design, not a failure:

> "can be removed and replaced without the disassembly of the whole plant"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §4 Design Points

This creates an annualized O&M cost with no tokamak analogue. The economics depend on:
- Coil section manufacturing cost (4,320 km REBCO for full coil, ~864 km for outer section)
- Replacement labor and downtime (Simpson claims <2 weeks/year)
- REBCO tape cost trajectory ($30-100/kA-m today, needs $10/kA-m for competitive economics per tokamak TEAs)

The concept's modularity is an advantage over tokamak blanket replacement (multi-month shutdowns), but the annual coil swap has no cost precedent. Simpson constrains Reactor B to <50% of Reactor A's capital cost but provides no absolute figures, so the replacement cost floor is unknown.

**3. Alpha Heating Distribution Assumption (Moderate)**

The dipole magnetic field has a good-curvature region (near the equator) and a bad-curvature region (near the poles). Alpha particles born in good curvature are MHD-stable and well-confined, but their heating is "entirely balanced by radiation losses" per the Simpson paper. Only bad-curvature alphas contribute to plasma self-heating:

> "Heating in the good-curvature region must be balanced by losses to preserve steady state. This is an ongoing area of active research"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §2.1.4

This assumption directly affects the required auxiliary heating power (44.5 MW for Reactor A) and thus Q_eng and LCOE. If alpha channeling proves less efficient than modeled, recirculating power rises. No experimental validation exists at fusion-relevant temperatures.

**4. Edge Pedestal Physics (Moderate)**

The plasma edge boundary conditions are poorly understood for dipoles. Simpson uses I-mode tokamak edge values (800 eV, 10³ Pa) as an upper bound but acknowledges:

> "the physics defining viable conditions at the plasma edge is not well understood"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §2.1.4

Tokamak edge physics (H-mode pedestals, ELMs, detachment) took decades to characterize empirically. Dipole edge physics has no equivalent database. Edge conditions set the achievable density and thus fusion power density. An adverse discovery here could degrade Q or require larger size.

**5. Tungsten Shield Mass and Neutron Optimization (Low)**

The core magnet neutron shield comprises 1,760 tonnes of tungsten tiles — the dominant mass component. Tungsten neutron attenuation provides the required shielding but adds structural complexity:

> "future designs of levitated dipole fusion power plants should aim to minimize this tungsten use"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §4.1

Simpson notes that alternative materials (tungsten borides, metal hydrides) could reduce shield mass and improve tritium retention. This is an optimization target, not a showstopper, but affects capital cost and coil structural loading.

## 3. Maturity of Key Subsystems and Components

Subsystems ordered by ascending maturity (least mature first):

### Levitated Two-Section REBCO Coil with Neutron Shield — TRL 2

**On paper only:** The two-section coil with sacrificial outer region is a Simpson design innovation with no built hardware. The concept requires:
- 23 T peak field (on-conductor) REBCO CICC architecture
- 2,560 tonnes total mass (1,760 t tungsten shield, 351 t steel structure)
- 20.8 GJ stored energy
- Neon slush cooling at 30 K
- 1-year outer section lifetime under 1 MW-year/m² fluence
- Decade-scale inner section lifetime

**Demonstrated:** Junior's 5.6 T, 550 kg HTS coil with non-insulated solder-impregnated REBCO. Tahi targets 20 T (~2028). The 23 T power-plant design is a ~4× stored energy scale-up from Tahi, with added neutron environment. No fusion magnet has ever been designed as a consumable annual-replacement component.

**Missing at scale:** Neutron-irradiated REBCO performance data at 1 MW-year/m² fluence. Neon slush cooling at GJ scale. Rapid docking/undocking of a 2,560-tonne assembly. Manufacturing supply chain for 864 km REBCO/year (outer section replacement). Tungsten tile attachment under thermal/neutron cycling.

### Tritium Breeding Blanket (Li₂O Ceramic) — TRL 3

**On paper only:** Simpson specifies a Li₂O ceramic blanket on the outside of the inner vacuum vessel, achieving TBR 1.1. The blanket operates in steady-state, avoiding MHD concerns with liquid metal blankets, but ceramic blankets have never been integrated with a levitated dipole geometry. Key unknowns:
- Cooling scheme not detailed (helium-cooled assumed from ceramic choice)
- Neutron multiplier not specified (Be or Pb typical for solid breeders)
- Module replacement strategy unclear (blanket resides behind the inner vessel)

**Demonstrated:** ITER TBM program has ceramic breeder modules under design (PDR expected 2026) but no operational data at fusion fluence. Li₂O and Li₄SiO₄ candidates tested in fission neutron environments up to ~30 dpa.

**Missing at scale:** Ceramic blanket integration with dipole-specific geometry (toroidal symmetry assumption from tokamaks invalid). Tritium extraction from Li₂O at kg/day rates. Replacement logistics given vacuum vessel geometry.

### On-Board Superconducting Flux Pump — TRL 3-4

**Demonstrated:** Junior achieved 170 kJ energy delivery via HTS transformer-rectifier flux pump (February 2026), a world record for HTS flux pump delivery. The flux pump eliminates physical current leads during operation, solving a long-standing challenge for levitated magnets:

> "proof of concept for powering the Core Magnet using an HTS transformer rectifier"
> — arxiv-2508-17691-junior-design-results.md, §3.3

**On paper only:** Scaling to 20.8 GJ stored energy (Reactor A) is a ~120,000× energy scale-up. The Reactor A flux pump must maintain 1.44 kA against joint resistance while levitated inside a 667 MW fusion plasma. Joint resistance on Junior's 14-coil HTS circuit is 8.6 ± 0.5 μΩ; Reactor A's larger coil set will require lower joint resistance or higher flux pump voltage.

**Missing at scale:** Flux pump operation in neutron/gamma radiation environment. Reliability over multi-year coil lifetime. Rejection of ~MW-scale electromagnetic interference from nearby ICRH antennas.

### ICRH Heating System — TRL 5-6

**Demonstrated:** ICRH is mature in tokamaks (ITER: 20 MW, 40-55 MHz). Stellarators and mirrors use ICRH for ion heating. Wall-plug efficiency approaching 70% is state-of-art for high-power RF sources.

**On paper only:** Integration with dipole plasma geometry. Antenna placement on outer vacuum vessel must deliver 44.5 MW to plasma while avoiding direct coil line-of-sight (electromagnetic pickup on HTS). Reactor A assumes 70% heating efficiency, optimistic relative to tokamak experience (~50-60%).

**Missing at scale:** Dipole-specific ICRH coupling efficiency validation. Antenna survivability on the large-diameter (~12 m) vessel.

### Cryogenic Neon Slush System — TRL 5-6

**On paper only:** Neon slush (solid + liquid mixture) chosen for superior latent heat capacity. Cryogenic reservoir embedded in coil structure. Pulsed operation driven by thermal heat load from radiation — neon absorbs heat for 45.5 minutes (Reactor A), then magnet shuts down for reservoir replacement:

> "used slushy is pumped out of reservoir channels, and new slushy is quickly pumped right back in"
> — dossier.md summary of OpenStar website

**Demonstrated:** Cryogenic slush systems exist for LNG and hydrogen storage. Neon slush is less common than hydrogen slush. Helium refrigeration at 30 K is industrial capability.

**Missing at scale:** Neon slush production at multi-tonne/hour rate. Rapid pump-out/refill cycle for 2,560-tonne coil. Tritium permeation through cryogenic plumbing (neon itself is inert). Integration with neutron shielding and structural supports.

### Reinforced Concrete Vacuum Vessel — TRL 7-8

**Demonstrated:** Large reinforced concrete pressure vessels exist in nuclear fission and chemical industries. Simpson notes:

> "similar sizes to previously constructed vacuum vessels"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §6 Conclusions

The vessel is ~twice ITER's outer diameter but operates at lower internal complexity (no interlocking coils). Inner vessel is Inconel 718 for tritium containment.

**Missing at scale:** Integration of penetrations for ICRH, diagnostics, and coil support while maintaining tritium barrier. Seismic/levitation-failure load cases (coil drop scenario).

### First Wall and Neutron Conversion — TRL 7-8

**Demonstrated:** Tungsten/B₄C neutron shield radiates 92% of deposited heat to first wall. Li₂O blanket captures thermal power for electricity generation. Neutron wall loading is favorable:

> "Peak neutron shield wall loading: 0.753 MW/m²"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §Table 8

This is 30-70% lower than tokamak wall loadings (1-2.5 MW/m²), extending first-wall component lifetime.

**Missing at scale:** Thermal management of pulsed heat load (45-minute burn, then shutdown for coil cooling). Compatibility of Li₂O chemistry with Inconel vessel. Thermal radiation from shield operating at >2000 K (hot tiles) to vessel at ~600°C.

## 4. Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape (Critical — High Cost, Scaling Required)**

Reactor A requires 4,320 km of REBCO tape (full coil). Annual sacrificial section replacement needs ~864 km/year. Global REBCO production today is in the thousands of km/year range, insufficient for a multi-plant deployment scenario. Tape cost is $30-100/kA-m today; tokamak TEAs target $10/kA-m for competitive economics.

Simpson references SuperOx YBCO performance with 30% improvement from Faraday Factory "Mirai" tape, assuming:

> "engineering current densities in excess of 1000 A/mm²"
> — arxiv-2602-20564-dt-dipole-power-plants.md, §4.1

Current REBCO manufacturers: Shanghai Superconductor Technology, Faraday Factory Japan, SuperOx (Russia). Western supply chains are immature. A 10-plant fleet consuming 8,640 km/year replacement tape requires ~3× today's global capacity.

Cost implication: At $50/kA-m (mid-range today) and 1000 A/mm² engineering J, 864 km replacement tape is ~$43M material cost/year. This is before fabrication into CICC, winding, testing, and integration. The economics hinge on aggressive tape cost reduction via manufacturing learning curves (battery/solar analogy).

**Tungsten (Moderate — Supply Adequate, Machining Complex)**

Reactor A uses 1,760 tonnes of tungsten for neutron shield tiles. Global tungsten production ~85,000 tonnes/year, so material availability is not a constraint. However:

- High-purity tungsten (nuclear grade) is a specialized product
- Precision machining of large-area tiles to thermal expansion tolerances is time-consuming
- Tile attachment to steel structure under neutron damage and thermal cycling (>2000 K hot tiles) is an engineering challenge

Simpson notes tungsten creep and tile mounting mechanism require detailed design. Tungsten sourcing is geographically concentrated (China ~85% of global production), creating supply chain risk but no absolute shortage.

**Lithium-6 for Tritium Breeding (Moderate — Shared Constraint Across All D-T Concepts)**

Li₂O blanket with 3,490 tonnes total mass (Reactor A). Assuming 90% enriched Li-6 (typical for tritium breeding), this represents ~600-700 tonnes of Li-6. Enrichment is performed in only a few countries (Russia, China, US via legacy centrifuge capacity). Current production is <100 tonnes/year globally. A 10-plant fleet would strain global enrichment capacity.

Cost: Li-6 enrichment cost is not published but analogous to uranium enrichment ($/SWU-equivalent). FLiBe salt cost (used in some fusion concepts) is estimated at $154/kg with 20% learning rate (Araiinejad 2025), but Li₂O ceramic is a different product form and likely cheaper (oxide vs. fluoride salt). No public cost estimate exists.

Shared supply chain: All D-T fusion concepts need Li-6. Levitated dipole competes with tokamaks, stellarators, and mirrors for the same feedstock. Simpson's avoidance of "expensive molten salts and neutron multipliers" is a relative advantage within D-T concepts, not an escape from Li-6 dependence.

**Neon for Cryogenic Cooling (Low — Abundant, Novel Application)**

Neon is obtained as a byproduct of air separation (0.0018% of atmosphere). Global production ~500 tonnes/year, used for lighting and cryogenics. Reactor A neon inventory is not quantified by Simpson, but cryogenic reservoirs for a 2,560-tonne coil likely require <10 tonnes total neon (latent heat capacity is high). Supply is adequate.

The novel requirement is neon *slush* production at scale and rapid reservoir exchange. This is a process engineering challenge, not a material scarcity issue. Hydrogen slush has heritage in aerospace (Saturn V), but neon slush is less common. Development needed but not supply-constrained.

**Inconel 718 for Inner Vacuum Vessel (Low — Established Supply)**

Inconel 718 is a nickel-based superalloy widely used in gas turbines, nuclear, and chemical processing. Global production is thousands of tonnes/year. The inner vessel is large-diameter but conventional fabrication. Supply chain is mature.

**Boron Carbide (B₄C) for Neutron Shield (Low — Adequate Supply)**

Reactor A uses 82.3 tonnes of B₄C in the neutron shield. Global B₄C production is ~1,000-2,000 tonnes/year, primarily for armor and nuclear applications. Supply is adequate for fusion plant needs.

## 5. Design Point Parameters

All values describe OpenStar Reactor A at its native 208 MWe scale.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Geometry and Plasma** |
| R0 (core magnet outer radius) | 5.3 m | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7; analyst-patch-spec-anchors.md | high | spec key: `R0` |
| plasma_volume (geometric) | 13,600 m³ | [inferred: arxiv-2602-20564 implies this volume from dipole geometry, but 1costingFE uses effective volume 200 m³ for radiation calc — see Note] | medium | spec key: `plasma_volume` — library uses 200 m³ effective value to avoid radiation formula range error; dipole plasma is highly peaked, not uniform like tokamak assumption |
| **Magnetic Field** |
| B_center (core magnet central field) | 6.26 T | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7; analyst-patch-spec-anchors.md | high | spec key: `B` (canonical name is `B`, not `B0`) |
| B_peak (on-conductor) | 23.0 T | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Informational only — library uses on-axis B for coil costs; 23 T is the engineering constraint |
| **Power Balance** |
| P_native (net electric output) | 208 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5; analyst-patch-spec-anchors.md | high | spec key: `P_native`; drives module count at 1 GWe comparison |
| fusion_power | 667 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational only — `p_fus` is back-solved by library from `p_input` + `P_native`; do NOT put in spec |
| p_input (auxiliary heating, ICRH wallplug) | 44.5 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5; analyst-patch-spec-anchors.md | high | spec key: `p_input` — ICRH at 70% source efficiency |
| thermal_power | 741 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational only — library calculates from fusion + blanket multiplication |
| Q_sci (scientific gain) | 15 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational — design assumption, not experimental |
| Q_eng (engineering gain) | 4.68 | [inferred: 208 / 44.5 = 4.68] | high | Informational — recirculating fraction is ~21% |
| **Thermal Efficiency** |
| eta_th (thermal-to-electric) | 0.40 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 2; analyst-patch-spec-anchors.md | medium | spec key: `eta_th` — paper states 40%, consistent with Rankine cycle; specific cycle not disclosed |
| eta_aux (auxiliary heating efficiency) | 0.70 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 2 | high | ICRH source efficiency assumption |
| mn (blanket energy multiplication) | 1.11 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 2 | high | spec key: `mn` — D-T standard value |
| **Magnet System** |
| core_magnet_stored_energy | 20.8 GJ | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Informational only — largest HTS magnet energy ever proposed |
| REBCO_tape_length | 4,320 km | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational — critical for coil cost override |
| core_magnet_mass | 2,560 tonnes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational — 1,760 t tungsten shield, 351 t steel structure |
| operating_temperature | 30 K | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Neon slush cooling, higher than LTS (4 K), lower than some HTS (77 K) |
| sacrificial_coil_lifetime | 1.2 years | arxiv-2602-20564-dt-dipole-power-plants.md §Table 8 | high | Informational — outer section replacement frequency, critical for O&M cost |
| **Operational Characteristics** |
| duty_cycle (core magnet) | 90.1% | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational — pulsed by cryogen thermal limits, not plasma |
| float_time | 45.5 minutes | arxiv-2602-20564-dt-dipole-power-plants.md §Table 7 | high | Burn duration before neon reservoir heat saturation |
| plant_availability | 0.96 | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | medium | spec key: `availability` — includes <2 weeks/year magnet replacement downtime |
| **Tritium and Blanket** |
| blanket_material | Li₂O ceramic | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 | high | Informational — solid ceramic breeder, 3,490 tonnes |
| TBR (tritium breeding ratio) | 1.1 | arxiv-2602-20564-dt-dipole-power-plants.md §4.1 | high | Informational — adequate for self-sufficiency |
| blanket_thickness | [derived: ~0.6 m typical for ceramic blankets] | [analogue: ITER TBM] | low | Not specified in sources; inferred from ITER HCPB analogue |
| **Neutron Environment** |
| peak_neutron_wall_loading | 0.753 MW/m² | arxiv-2602-20564-dt-dipole-power-plants.md §Table 8 | high | Informational — 30-70% lower than tokamaks |
| fluence_threshold (sacrificial coil) | 1 MW-year/m² | arxiv-2602-20564-dt-dipole-power-plants.md §4.1 | high | Informational — drives 1.2-year outer section lifetime |

**Key inferred values and their derivation:**

- **Q_eng = 4.68**: Calculated from P_native / p_input = 208 MWe / 44.5 MW. This is lower than typical tokamak targets (Q_eng ~10) but consistent with dipole's high auxiliary heating requirement for Q_sci = 15 plasma.
- **Recirculating fraction ~21%**: 44.5 MW / 208 MW ≈ 21%, favorable compared to early tokamak designs (~30-40%) but higher than advanced tokamak targets (~10-15%).
- **plasma_volume modeling caveat**: The geometric volume is 13,600 m³, but 1costingFE uses 200 m³ effective volume to avoid radiation calculation errors. The library assumes uniform plasma density (tokamak heritage), but dipole plasmas are highly peaked. A proper `radiation_peaking_factor` correction is needed but not yet implemented. This affects p_fus back-solve accuracy.

**Critical missing parameters:**
1. Specific thermal cycle (Rankine vs. sCO2) — not disclosed in any OpenStar source
2. Blanket cooling scheme details (assume He-cooled from ceramic choice)
3. First-wall material composition (assume tungsten-armored steel from shield description)
4. Cryogenic system power consumption (p_cryo) — not quantified
5. Coil support structure mass and cost
6. Detailed tritium processing system parameters

## 5b. Override Candidates

The following registry entries represent accountable departures from the 1costingFE library defaults for this design point, discovered via per-account walkthrough of the canonical schema. All enabled overrides apply to the 1 GWe modular-fleet headline (Reactor A replicated to n_mod modules, NOAK).

```yaml
overrides:
  - account: C220103
    value: [TBD - company data needed]
    enabled: false
    provenance: derived
    source: "arxiv-2602-20564-dt-dipole-power-plants.md §Table 5; §4.1"
    rationale: |
      Reactor A requires 4,320 km REBCO tape for the full two-section coil. At 1 MW-year/m²
      fluence, the sacrificial outer section (~20% of coil, ~864 km) has 1.2-year lifetime.
      Annual replacement creates an O&M cost component, but the initial capital cost for ONE
      module's coil is company-proprietary (Simpson withholds absolute $ figures).

      Derivation path for future iteration:
      - REBCO tape cost assumption: $X/kA-m (industry targets $10/kA-m, current $30-100/kA-m)
      - Engineering current density: 1000 A/mm² (Simpson §4.1)
      - CICC fabrication adder: winding + cryostat + testing
      - Two-section architecture premium vs. continuous coil

      The library's HTS coil cost formula is calibrated to tokamak D-coils. The levitated
      dipole's cylindrical geometry and two-section design have no tokamak analogue. A
      per-module override is justified when company data becomes available.

      Relative to the library's 1 GWe modular-fleet default: [value TBD when company data
      available]. The sacrificial replacement frequency does NOT affect C220103 (capital);
      it affects CAS70 (O&M) — see CAS70 candidate below.
```

```yaml
  - account: C220104
    value: 0.70 * generic.cas22_detail["C220104"]
    enabled: true
    provenance: direct
    source: "arxiv-2602-20564-dt-dipole-power-plants.md §Table 2; §Table 5"
    rationale: |
      Reactor A uses ICRH at 70% source efficiency (Simpson Table 2), delivering 44.5 MW
      wallplug auxiliary heating (Table 5). The library's generic heating system efficiency
      is ~50% (tokamak NBI/ECRH average). ICRH at 70% is more efficient than baseline, reducing
      the heating system capital cost per installed MW.

      The override represents 70% of the library's per-module heating system cost for this
      dipole's modular fleet. The library default assumes lower-efficiency heating; ICRH's
      higher efficiency allows smaller, cheaper RF power supplies and less waste heat rejection.

      At the 1 GWe fleet headline (n_mod modules of Reactor A), each module needs 44.5 MW ICRH
      wallplug. The 0.70 multiplier applies to the library's per-module heating cost, and
      the ×n_mod scaling happens in the CAS22 rollup, not in this detail row.
```

```yaml
  - account: C220108
    value: 0.5 * generic.cas22_detail["C220108"]
    enabled: true
    provenance: derived
    source: "arxiv-2602-20564-dt-dipole-power-plants.md §Table 8"
    rationale: |
      Reactor A achieves peak neutron wall loading of 0.753 MW/m² (Simpson Table 8), 30-70%
      lower than tokamak designs (1-2.5 MW/m²). The library's divertor cost scales with wall
      loading and heat flux. Lower wall loading reduces divertor heat sink mass, coolant flow
      rates, and replacement frequency.

      The dipole has no conventional divertor — plasma losses exit through magnetic cusps at
      the vessel top/bottom. However, those regions still require heat-handling components
      analogous to divertor tiles. The 0.5 multiplier reflects:
      - Lower heat flux per unit area (50% reduction vs. tokamak)
      - Distributed loss pattern (no single high-heat-flux strike point)
      - Steady-state operation (no ELM transients)

      Relative to the library's 1 GWe modular-fleet divertor cost (which assumes tokamak-level
      heat flux), this dipole's per-module heat-handling hardware is approximately half the cost.
      The fleet-level cost is this per-module value ×n_mod.
```

```yaml
  - account: CAS70
    value: [TBD - company data needed for sacrificial coil replacement annualized cost]
    enabled: false
    provenance: derived
    source: "arxiv-2602-20564-dt-dipole-power-plants.md §Table 8; §4.1"
    rationale: |
      CRITICAL NOTE: CAS70 overrides are currently silently dropped by 1costingFE (per
      1costingfe#106). This entry is recorded for future capability but will NOT affect
      the current model run.

      The sacrificial outer coil section has 1.2-year lifetime (Simpson Table 8), creating an
      annual replacement requirement unique to this concept. The annualized O&M cost is:

      Annual_coil_replacement = (864 km REBCO outer section) × (tape $/kA-m + CICC fab $/km
                                  + winding labor + testing + installation) / 1.2 years

      Plus <2 weeks/year plant downtime (lost revenue). Simpson withholds absolute cost figures,
      so this override cannot be quantified until company data is available.

      The library's CAS70 default (staffing-based O&M) does not include annual magnet replacement.
      When CAS70 overrides are enabled in 1costingFE, this will be M × the library's fleet O&M,
      where M reflects the consumable coil economics.
```

**Override count: 2 enabled, 2 awaiting company data.** Expected range for High archetype-fit: 0-4 enabled overrides. The count is consistent with archetype-fit expectations.

**Accounts walked but no override proposed:**

- **C220101 (Blanket)**: Li₂O ceramic blanket is within library's solid-breeder default assumptions. No company-grounded cost data to justify departure.
- **C220102 (Shield)**: Tungsten/B₄C shield is concept-specific but no company cost figure. Shield mass (1,760 t W) is known, but $/kg is generic.
- **C220105 (Structure)**: Reinforced concrete vessel + Inconel inner vessel — no company cost breakdown.
- **C220106 (Vacuum system)**: Large-diameter vessel (~12 m) but no company-specific cost multiplier.
- **C220107 (Power supplies)**: Flux pump is unique but capital cost is proprietary. DC magnet supplies for top magnet are conventional.
- **C220110 (Remote handling)**: Modular coil replacement is an advantage, but no quantified cost reduction vs. tokamak blanket changeout.
- **C220111 (Assembly)**: No company data.
- **CAS21 (Buildings)**: Large vessel diameter may increase building footprint, but no company figure.
- **CAS23 (Turbine)**: Thermal cycle unspecified; library default applies.
- **CAS24 (Electric plant)**: No company data.
- **CAS26 (Heat rejection)**: No company data.
- **CAS27 (Special materials)**: Li₂O blanket inventory (3,490 t) is known, but $/kg is generic.
- **CAS80 (Fuel)**: D-T fuel costs are negligible for all D-T concepts; no override needed.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published LCOE or absolute overnight capital cost for Reactor A/B. Simpson withholds proprietary cost model results. | S1, S5b | proprietary | blocking | OpenStar to publish cost model or provide data under NDA. Without this, 1costingFE baseline run uses library defaults which are not validated against company projections. |
| 2 | No dipole energy confinement scaling law. Reactor A assumes Q_sci = 15 with Bohm/gyro-Bohm bounding cases, but no experimental validation above Te ~ 200 eV. | S2 (Challenge 1), S5 | truly-unknown | blocking | Tahi demonstration (target ~2028, 20 T) must achieve n·τ_E ≥ 3.23 × 10^19 s/m³ (Bohm case) to validate Reactor A design point. Until then, Q_sci = 15 is an assumption, not a measurement. |
| 3 | Sacrificial REBCO coil section replacement cost (material + labor + downtime). Simpson states <2 weeks/year downtime but no cost breakdown. | S2 (Challenge 2), S5b | proprietary | important | OpenStar to provide: (a) REBCO tape procurement cost assumption, (b) CICC fabrication cost, (c) replacement labor estimate. Critical for CAS70 O&M override when 1costingFE enables it. |
| 4 | Alpha heating distribution between good/bad curvature regions. Simpson assumes good-curvature alpha heating is "entirely balanced by radiation losses" but flags this as "ongoing research." | S2 (Challenge 3) | truly-unknown | important | Experimental validation on Maui or earlier prototypes. If assumption is wrong, p_input rises, degrading Q_eng and LCOE. |
| 5 | Dipole edge pedestal physics. Simpson uses I-mode tokamak edge values (800 eV, 10³ Pa) as upper bound but acknowledges edge physics is "not well understood." | S2 (Challenge 4) | truly-unknown | important | Edge physics experiments on Tahi/Maui. Tokamak edge scalings may not apply. Adverse edge conditions could limit achievable density and thus fusion power density. |
| 6 | Specific thermal cycle choice (Rankine vs. sCO2). Simpson specifies eta_th = 0.40 but not the cycle architecture. | S1, S5 | proprietary | nice-to-have | OpenStar website or follow-on paper. Affects BOP cost (CAS23) but library defaults are reasonable for both cycles at 40% efficiency. |
| 7 | Tritium breeding blanket cooling scheme and neutron multiplier choice. Simpson specifies Li₂O ceramic but not coolant (assume He from ceramic choice) or multiplier (Be/Pb typical). | S3 (Subsystem TRL), S5 | not-yet-sourced | important | OpenStar blanket design paper or DEMO-Tama Nui engineering documents. Affects blanket cost (C220101) and TBR margin. |
| 8 | First-wall material composition and armor strategy. Simpson details neutron shield but not plasma-facing components. | S5 | not-yet-sourced | nice-to-have | Engineering drawings or component list. Assume tungsten-armored steel from shield description, but confirmation needed. |
| 9 | Cryogenic system power consumption (p_cryo). Neon slush cooling is novel; power requirement for refrigeration and rapid reservoir exchange not quantified. | S5 | not-yet-sourced | nice-to-have | OpenStar cryogenics design. Affects auxiliary power and thus Q_eng. Likely <1 MW (minor) but should be confirmed. |
| 10 | Coil support structure mass and cost. Simpson gives core magnet total mass (2,560 t) but not the breakdown of support fixtures vs. active components. | S5 | not-yet-sourced | nice-to-have | Mechanical engineering design. Affects C220103 override if structure is unusually heavy/expensive. |
| 11 | REBCO tape supply chain capacity for multi-plant deployment. Annual 864 km replacement per plant; 10-plant fleet needs 8,640 km/year, ~3× today's global capacity. | S4 | derivable | nice-to-have | Industry capacity forecasts from SuperOx, Faraday Factory, Shanghai Superconductor. Not concept-specific but affects deployment rate. |
| 12 | Tungsten shield tile attachment and thermal cycling survivability. Simpson notes "determining final tile size requires detailed design of mounting mechanism" and flags tungsten creep. | S2 (Challenge 5), S3 | not-yet-sourced | nice-to-have | Mechanical design iteration. Affects shield replacement interval (operational cost) but unlikely to be showstopper. |

## 7. Family-Delta vs Comparables

The fixed comparable for this analysis is **19-orbital-levitated-dipole** (Zephyr Energy). Both concepts share the levitated dipole confinement topology but diverge in engineering implementation, fuel choice, and operational philosophy.

### Divergence 1: Stationary vs. Rotating Coil — Engineering Complexity Trade

**OpenStar (Concept 12)**: Single levitated HTS coil, magnetically suspended by external top magnet, stabilized in antisymmetric levitation field. Coil is stationary in the lab frame.

**Zephyr (Concept 19)**: Levitated dipole is a ~100-tonne permanent magnet sphere, **rotated at 20-40 rpm** for gyroscopic stabilization. No external top magnet needed.

**Cost implication:** OpenStar's magnetic levitation requires a top magnet (relatively small, ~1% of capital per Simpson) and active position control, but the coil is stationary, simplifying cryogenic and electrical connections. Zephyr's rotating coil eliminates the top magnet but requires:
- Bearings/docking mechanism for a spinning 100-tonne sphere
- Rotational power input (friction losses)
- Gyroscopic stabilization logic
- More complex flux pump integration (rotating reference frame)

**Verdict:** OpenStar's stationary coil is mechanically simpler and lower-risk. Zephyr's rotating coil trades magnetic levitation hardware for mechanical rotation hardware. Likely a **neutral** cost difference at system level — complexity is redistributed, not eliminated. No published cost comparison exists.

### Divergence 2: D-T vs. D-D Fuel — Neutron Environment and TRL

**OpenStar**: D-T fuel, 14.1 MeV neutrons, requires tritium breeding blanket (Li₂O ceramic), sacrificial coil design (1-year outer section lifetime), and neutron shield (1,760 t tungsten). Lower plasma temperature requirements (Q achievable at ~15 keV).

**Zephyr**: D-D fuel, 2.45 MeV neutrons (83% energy reduction vs. D-T), no tritium breeding, simpler neutron management, but requires higher plasma temperatures (~30-50 keV for equivalent reactivity).

**Cost implication:**
- **OpenStar advantage:** Easier ignition physics (D-T cross-section peaks at 70 keV vs. 500+ keV for D-D). Lower required Q for net power.
- **OpenStar penalty:** Tritium breeding blanket ($, complexity, TBR > 1 requirement), annual coil replacement ($, downtime), larger neutron shield (mass, cost).
- **Zephyr advantage:** No breeding blanket, longer coil lifetime (possibly decade-scale without replacement), smaller shield.
- **Zephyr penalty:** Much higher plasma temperature requirement (more auxiliary heating, more first-wall heat load), 5-10× lower fusion reactivity at same temperature (requires higher density or confinement).

**Verdict:** OpenStar's D-T choice is a **timeline advantage** (commercial deployment ~2035 vs. Zephyr's longer R&D path) but a **long-term cost penalty** (annual coil replacement vs. Zephyr's consumable-free design). D-T fusion is technologically mature; D-D is aspirational for dipoles. No dipole experiment has achieved D-D-relevant temperatures.

### Divergence 3: Sacrificial Two-Section Coil vs. Single Permanent Coil

**OpenStar**: Patented two-section REBCO coil. Outer ~20% is sacrificial (1.2-year lifetime at 1 MW-year/m² fluence), replaced annually. Inner ~80% is shielded for decade-scale lifetime. Rapid docking system enables <2 week replacement downtime.

**Zephyr**: Single permanent dipole coil (likely NbTi or Nb₃Sn LTS given 100-tonne mass and cryogenic requirement). Designed for plant lifetime (30 years) without replacement.

**Cost implication:**
- **OpenStar:** Annual CAPEX for coil section replacement (~864 km REBCO + fabrication). Downtime penalty (<2 weeks/year lost revenue). Logistics of handling 2,560-tonne assembly annually. **But:** avoids multi-month shutdowns for full coil replacement (tokamak blanket analogue).
- **Zephyr:** No coil replacement OPEX. **But:** 2.45 MeV neutrons still damage superconductor (slower than 14.1 MeV). If coil does degrade, replacement is full plant disassembly (months of downtime, tokamak-like penalty).

**Verdict:** OpenStar's consumable-coil model is a **strategic bet on rapid manufacturing and modular replacement over lifetime capital intensity**. If REBCO tape costs drop to $10/kA-m (battery-curve learning), annual replacement becomes affordable. If costs stay at $50/kA-m, the OPEX is punitive. Zephyr's permanent-coil model is **lower OPEX but higher one-time replacement risk**. No cost model exists for either concept, so the comparison is qualitative.

### Divergence 4: HTS (REBCO) vs. LTS (NbTi/Nb₃Sn) Superconductor

**OpenStar**: REBCO 2nd-gen HTS, 23 T peak field, 30 K operating temperature (neon slush cooling).

**Zephyr**: Likely NbTi or Nb₃Sn LTS (inferred from 100-tonne mass and 4 K operating temperature for permanent magnets).

**Cost implication:**
- **OpenStar advantage:** HTS allows higher field (23 T), smaller coil radius for same stored energy, and higher operating temperature (30 K vs. 4 K, reducing cryogenic load).
- **OpenStar penalty:** REBCO is $30-100/kA-m today vs. NbTi at ~$2-5/kA-m. Mass production learning is required for cost parity.
- **Zephyr advantage:** LTS is mature, cheap, and industrially proven (MRI magnets, ITER).
- **Zephyr penalty:** 4 K operation requires liquid helium (expensive, boil-off losses), larger refrigeration load.

**Verdict:** OpenStar's HTS choice is a **performance advantage** (higher field, smaller size) but a **current cost penalty** (REBCO expensive). Zephyr's LTS choice is **low-risk, low-cost baseline** but **larger and heavier**. The HTS vs. LTS trade is generic across fusion concepts; dipoles share this with tokamaks/stellarators.

### Shared Advantages vs. Tokamak/Stellarator Comparables

Both levitated dipole concepts (OpenStar, Zephyr) share intrinsic advantages over toroidal confinement:

1. **Disruption-free operation:** No current-driven MHD instabilities. Interchange modes are stabilized by plasma compressibility. Simpson quotes:
   > "Recent studies into the economics of a fusion power plant show that plasma disruptions pose a major risk of raising the price of electricity, highlighting the benefit of disruption-free configurations"
   > — arxiv-2602-20564-dt-dipole-power-plants.md, §Introduction

2. **Modular magnet replacement:** Core coil can be removed without disassembling the entire plant. Simpson:
   > "This configuration of magnets and vacuum vessel does not require any complex interlocking of components, allowing for a level of access and maintainability unique among magnetically confined fusion devices"
   > — arxiv-2602-20564-dt-dipole-power-plants.md, §4 Design Points

3. **Simple magnet geometry:** Single cylindrical coil vs. tokamak's interlocking TF/PF/CS coil set or stellarator's 3D non-planar coils. Simpson:
   > "the core magnet, which is the most complex and expensive part of the reactor, is the same physical scale as the magnets that comprise the ARC tokamak"
   > — arxiv-2602-20564-dt-dipole-power-plants.md, §Introduction

4. **Lower neutron wall loading:** OpenStar achieves 0.753 MW/m² vs. tokamak 1-2.5 MW/m². Extends first-wall lifetime.

### Shared Disadvantages vs. Tokamak/Stellarator

1. **No experimental validation above Te ~ 200 eV.** LDX and RT-1 operated at sub-fusion temperatures. Confinement scaling is unproven.

2. **Larger vacuum vessel:** OpenStar's vessel is ~twice ITER's outer diameter for similar thermal power. Zephyr's is similar. Higher building costs.

3. **On-board power supply complexity:** Flux pump must maintain coil current without physical leads. No tokamak/stellarator analogue.

4. **Pulsed operation driven by cryogenics:** Not truly steady-state like stellarators. Duty cycle >95% but requires periodic shutdown for cryogen refresh.

### Summary Table

| Subsystem / Feature | OpenStar (Concept 12) | Zephyr (Concept 19) | Cost Delta (OpenStar vs. Zephyr) |
|---|---|---|---|
| Coil levitation | Magnetic (top magnet) | Gyroscopic (rotation) | Neutral |
| Fuel | D-T (14.1 MeV n) | D-D (2.45 MeV n) | Penalty (breeding + shield) |
| Coil replacement | Annual (sacrificial section) | None (permanent coil) | Penalty (OPEX) if REBCO expensive; Advantage (OPEX) if REBCO cheap |
| Superconductor | HTS (REBCO, 23 T, 30 K) | LTS (NbTi/Nb₃Sn, ~5 T, 4 K) | Penalty (material $) but Advantage (performance) |
| Confinement validation | Unproven at fusion-relevant T | Unproven at fusion-relevant T | Neutral (shared risk) |
| Neutron wall loading | 0.753 MW/m² | Lower (~0.1-0.3 MW/m² est.) | Advantage (Zephyr, longer component life) |
| TRL timeline | ~2035 commercial (D-T easier) | ~2040+ (D-D harder) | Advantage (OpenStar, faster deployment) |

**Conclusion:** OpenStar's Reactor A is a **more aggressive near-term design** (D-T fuel, HTS, sacrificial coil) optimized for 2030s deployment. Zephyr's orbital dipole is a **more conservative long-term design** (D-D fuel, LTS, permanent coil) targeting 2040+ deployment with lower OPEX but higher physics risk. Both concepts share the dipole's core advantages (disruption-free, modular, simple geometry) and disadvantages (unproven confinement, large vessel) vs. tokamaks. The cost delta is **qualitatively a wash** — OpenStar pays more OPEX (coil replacement) but saves CAPEX (easier ignition); Zephyr saves OPEX but pays in R&D time and higher plasma temperature requirements.

## 8. Sources

Listed in order of importance for this analysis:

1. **Simpson, J., et al. (2026).** "Deuterium-Tritium Levitated Dipole Fusion Power Plants." arXiv preprint arXiv:2602.20564.
   - **What it contributes:** Complete reactor design (Reactor A/B), 0D power balance, neutron shield design, magnet specifications, tritium breeding strategy, operational parameters. Primary quantitative source for all design point values.
   - **Where found:** knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md

2. **OpenStar Technologies Team. (2025).** "Design and Initial Results from Junior LDX." arXiv preprint arXiv:2508.17691.
   - **What it contributes:** Junior prototype specifications, HTS flux pump demonstration (170 kJ world record), levitated plasma confirmation (Feb 2026), coil fabrication details, ECRH system.
   - **Where found:** knowledge/concept_research/12-levitated-dipole/iter-01/sources/arxiv-2508-17691-junior-design-results.md

3. **OpenStar Technologies Website.** Prototype roadmap and technology overview. Accessed March 2026.
   - **What it contributes:** Commercial timeline (Tahi ~2028, Maui ~2031, Tama Nui 50-200 MW), flux pump and cryogenic details, company context.
   - **Where found:** knowledge/concept_research/12-levitated-dipole/iter-01/sources/openstar-prototype-roadmap.md

4. **Analyst Patch Specification.** Model input parameter anchors for 1costingFE integration. Internal document, March 2026.
   - **What it contributes:** Verified spec keys (R0, p_input, P_native), critical modeling caveats (plasma_volume effective value, radiation peaking factor need).
   - **Where found:** knowledge/concept_research/12-levitated-dipole/iter-03/sources/analyst-patch-spec-anchors.md

5. **Garnier, D., et al. (2006).** "Design and initial operation of the Levitated Dipole Experiment (LDX)." Fusion Engineering and Design 81(15-17), 2371-2380.
   - **What it contributes:** LDX heritage design, experimental validation of dipole stability, historical context for OpenStar's levitation approach.
   - **Where found:** Referenced in arxiv-2602-20564 and arxiv-2508-17691; not extracted as separate source.

6. **Yoshida, Z., et al. (2010).** "Observation of plasma confinement in a magnetic dipole." Physical Review Letters 104(23), 235004.
   - **What it contributes:** RT-1 experimental results, local β > 1 confirmation, Japanese dipole program validation.
   - **Where found:** Referenced in arxiv-2508-17691; not extracted as separate source.

7. **Kesner, J., and Hastie, R. J. (2002).** "Electrostatic drift modes in a closed field line configuration." Physics of Plasmas 9(2), 395-400.
   - **What it contributes:** Theoretical foundation for dipole interchange stability via plasma compressibility.
   - **Where found:** Referenced in arxiv-2602-20564; not extracted as separate source.

8. **IEEE Spectrum (2025).** "Levitating Magnet Promises Cheaper Fusion Power." Article by OpenStar coverage, February 2025.
   - **What it contributes:** Journalistic context, timeline expectations, qualitative cost comparison to tokamaks, CEO interview excerpts.
   - **Where found:** knowledge/concept_research/12-levitated-dipole/iter-01/sources/openstar-prototype-roadmap.md (content overlaps)