# Gap Assessment: Spherical Tokamak - CS-free p-B11 (p-B11)

## Overall Readiness
**Rating**: Insufficient Data
**Summary**: ENN's CS-free p-B11 spherical tokamak concept is at TRL ~2: EHL-2 (the next device) remains under construction and targets physics verification, not power production. No power plant design, blanket, energy conversion system, or economic data has been published. The physics basis for the critical hot-ion mode (Ti/Te >> 1) required for p-B11 net energy is actively contested in peer-reviewed literature. While the device parameters and roadmap are well-documented, the concept cannot support a quantitative LCOE analysis in its current state — a qualitative feasibility and challenge assessment is possible, but only the physics-challenge and subsystem-TRL sections can be populated with meaningful specificity.

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- ENN roadmap (arXiv:2401.11338 / Phys. Plasmas 31, 062507, 2024): EHL-2 device parameters (R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA, Ti0 ≈ 30 keV target), heating system (17 MW NBI + 6 MW ECRH), CS-free startup approach, and a multi-step roadmap toward a burning plasma device.
- EHL-2 physics design overview (PST, doi:10.1088/2058-6272/ad981a): magnet/vacuum vessel geometry, heat flux estimates (~20 MW/m² at divertor at low density).
- EXL-50U experimental results (ENN Research site): 1 MA plasma current at 1.2 T, TF coils at 150 kA — the predecessor device milestone.
- Peer-reviewed physics critique (arXiv:2406.15495, Li & Zhi 2024): argues the required Ti/Te = 4 hot-ion mode is inaccessible under physically achievable conditions.
- Independent Lawson criterion analysis (Frontiers in Nuclear Engineering, Ahmad et al. 2026): quantifies net-energy conditions for p-B11 — only achievable at Ti ≥ 125–190 keV with Te/Ti ≤ 0.5, minimum Lawson parameter 1.3×10²² – 1.2×10²³ m⁻³s.
- ENN website disclosures: explicit intent for direct energy conversion as the commercial capture pathway; no engineering design provided.

**Missing**:
- Any published power plant design, system study, or commercial reactor concept.
- Plant-level performance parameters (net Q, gross/net electric output, recirculating power fraction).
- Any cost or economic analysis.
- Detailed English-language coil engineering paper for EHL-2 (conductor type, current density, structural design).
- Post-EHL-2 roadmap with design parameters for the next-stage burning plasma device.

**Gaps**:
- No commercial plant study exists — proprietary (ENN may be developing internal roadmaps) + not-yet-sourced (no indication published) — **blocking**
- EHL-2 engineering detail limited; Chinese-language technical reports likely contain more specifics — not-yet-sourced — **important**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Hot-ion mode feasibility is the central physics challenge: the Frontiersin paper (Ahmad et al. 2026) establishes that net energy requires Te/Ti ≤ 0.5 at Ti = 190–330 keV, or Te/Ti ≤ 0.25 for a wider window. The Li & Zhi comment (arXiv:2406.15495) argues that even under the most optimistic heating assumptions, Ti/Te < 1.5 is realistic (not 4 as ENN's roadmap assumes), and that achieving Ti/Te = 4 by external heating would require ~20× fusion power in heating input — making the system economically nonsensical.
- CS-free startup challenge is well-documented: the central solenoid provides very limited volt-seconds; non-inductive ECRH ramp-up to MA-scale currents is identified as the key engineering bet. EXL-50 demonstrated ~1 A/W ECRH current drive efficiency.
- Bremsstrahlung dominance: at Te = Ti, the bremsstrahlung radiation rate exceeds the p-B11 fusion energy rate across the full 75–500 keV range (Ahmad et al. 2026, Fig. 2). The high effective charge of the p-B11 mixture (Zeff ~ 2.4) amplifies this.
- Divertor heat flux: EHL-2 physics paper notes ~20 MW/m² target heat flux at low density, which is at or beyond current tokamak divertor limits. The engineering solution is not specified.
- Direct energy conversion (DEC): ENN's commercial strategy depends on capturing charged alpha particles from p-B11 (3 alphas, ~8.68 MeV total). No DEC engineering design has been published; the technology is exploratory.

**Missing**:
- Engineering solution for divertor/plasma-facing components at p-B11 conditions (high temperature, high alpha flux, low density).
- Assessment of plasma-wall interactions with boron-containing plasma.
- Alpha particle energy deposition and confinement analysis for a power-plant-scale device.
- Specific DEC technology selection and efficiency projections.

**Gaps**:
- Hot-ion mode physics feasibility (Ti/Te >> 1) is actively contested — will require experimental resolution; cannot be assumed for economic modeling — truly-unknown — **blocking**
- DEC technology: no published engineering design, efficiency unknown — truly-unknown — **blocking**
- Divertor engineering solution at 20+ MW/m² in a low-density p-B11 plasma — truly-unknown — **blocking**
- Bremsstrahlung mitigation strategy beyond hot-ion mode remains speculative — truly-unknown — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- CS-free spherical tokamak plasma: EXL-50U demonstrated 1 MA / 1.2 T with ECRH-only current drive (TRL ~3-4 for this specific capability). EHL-2 targeting 3 MA / 3 T — a significant scale-up not yet demonstrated.
- NBI heating: 17 MW NBI for EHL-2 is demanding but within range of existing neutral beam technology. Mature at this scale (TRL ~6 for NBI subsystem).
- ECRH current drive: demonstrated at ~1 A/W efficiency on EXL-50 (TRL ~4 for this application).
- Resistive (copper) magnets: EXL-50U TF at 150 kA / 1.2 T is consistent with copper Bitter-plate coils. EHL-2 at 3 T / 1.05 m is within copper-coil range. TRL ~5-6 for the magnet subsystem if copper.
- p-B11 fuel cycle basics: proton (hydrogen) + boron-11 fuel is well-characterized as chemistry; no tritium breeding needed (simplification vs. D-T). No fuel cycle engineering for a power plant exists.

**Missing**:
- TRL assessment for direct energy conversion (DEC) at relevant alpha-particle energies (~2.9 MeV per alpha). Electrostatic DEC exists in theoretical literature; prototype demonstrations are at TRL 2-3 at most.
- Plasma performance at power-plant-relevant Ti (100-300 keV) in any device — not yet approached (EHL-2 targets 30 keV, a factor of ~5-10 below what is needed for net energy).
- EHL-2 coil engineering: conductor type (copper vs HTS) not definitively stated in public English-language sources.
- Long-pulse/steady-state operation assessment.

**Gaps**:
- p-B11 plasma at required temperatures (Ti ~ 100-300 keV with Ti/Te >> 1): no experimental precedent anywhere — truly-unknown — **blocking**
- DEC at relevant alpha energies: TRL 1-2, no power-plant-scale design — truly-unknown — **blocking**
- EHL-2 magnet conductor type unconfirmed — not-yet-sourced (EHL-2 coil paper likely exists in Chinese literature) — **important**
- CS-free current drive scalability to power-plant plasma currents (>10 MA) — truly-unknown — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- p-B11 fuel: Natural boron is ~80% ¹¹B / 20% ¹⁰B by abundance. Some isotope enrichment is needed but the starting isotopic fraction is favorable. Proton fuel (hydrogen) is abundant and straightforward.
- No tritium breeding required (aneutronic): eliminates lithium blanket supply chain, tritium processing infrastructure, and associated cost and regulatory overhead — a significant simplification vs. D-T.
- Copper coils (if confirmed): copper supply chain is mature; no exotic materials expected for resistive magnets at this scale.
- Low neutron flux: structural material activation is greatly reduced vs. D-T; first-wall replacement cycle expected to be much less frequent.

**Missing**:
- Boron-11 enrichment cost and supply chain at commercial scale (no published analysis found in Phase 1a sources).
- First-wall/plasma-facing material selection for high-temperature, high-alpha-flux, low-neutron p-B11 conditions.
- DEC component materials (high-voltage electrodes, particle collectors at MeV energies) — not yet defined.
- Alpha particle management at 8.68 MeV: helium ash exhaust strategy in steady-state operation.

**Gaps**:
- Boron-11 enrichment supply chain and cost at power-plant scale: no published analysis — not-yet-sourced — **important**
- First-wall material specification for p-B11 plasma conditions (alpha bombardment, no neutron breeding driver) — not-yet-sourced — **important**
- DEC component materials and manufacturing — truly-unknown — **important**
- Helium ash exhaust design (alpha particles accumulate in steady-state plasma) — truly-unknown — **important**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Major radius (R₀) | 1.05 m (EHL-2) | arXiv:2401.11338 | high |
| Toroidal field (B₀) | 3 T (EHL-2) | arXiv:2401.11338 | high |
| Plasma current (Ip) | 3 MA (EHL-2 target) | arXiv:2401.11338 | high |
| Ion temperature target (Ti0) | 30 keV (EHL-2 physics phase) | arXiv:2401.11338 | high |
| Required Ti for net energy | 125–330 keV (depending on Te/Ti) | Frontiersin (Ahmad et al. 2026) | medium |
| Heating power (EHL-2) | 23 MW (17 NBI + 6 ECRH) | arXiv:2401.11338 | high |
| Energy capture mode | Direct (charged particle) — intent only | ENN website; arXiv:2401.11338 | medium |
| Magnet type | Resistive (copper inferred) | EXL-50U datapoints | low |
| Fuel | p-B11 (aneutronic) | arXiv:2401.11338 | high |
| D-T tokamak LCOE analog | $140–550/MWh | TEA D-T MFE (knowledge/sources/tea_dt_mfe_cost_analysis/) | low analog |
| D-T tokamak capital cost analog | $8,800–22,200/kW (350 MWe plant) | TEA D-T MFE | low analog |
| ARIES-ST blanket cost analog | ~$155.7M (LiPb+He, D-T blanket) | ARIES Cost Account (knowledge/sources/aries_cost_account_documentation/) | low analog |

*Note on fleet-wide analogs: The D-T MFE TEA and ARIES-ST cost data are methodology references only. p-B11 eliminates the blanket/tritium system (removing a major cost driver) but replaces the steam Rankine cycle with an undesigned DEC system. Net LCOE impact of these substitutions cannot be estimated without a plant design.*

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net electrical output (MWe) | truly-unknown | blocking | No power plant design exists; EHL-2 is experimental |
| Engineering gain Q (Qeng) | truly-unknown | blocking | Physics verification has not begun; required Lawson criterion not yet approached |
| Energy conversion efficiency (DEC) | truly-unknown | blocking | DEC technology unspecified; theoretical efficiency 60-90% cited for alpha capture but no design exists |
| Capacity factor / availability | truly-unknown | blocking | No basis for estimate without operational device or design |
| Capital cost by CAS account | derivable (rough D-T analog only) | blocking | BOP and structures can be estimated from D-T analog; power conversion (DEC) and first-wall systems cannot |
| O&M cost (annual) | derivable (rough analog) | blocking | No concept-specific basis; D-T analogs available but power conversion system is fundamentally different |
| Fuel cycle cost (B-11 enrichment) | not-yet-sourced | important | Natural boron ~80% ¹¹B; enrichment cost not published |
| Recirculating power fraction | truly-unknown | blocking | Heating efficiency and recirculation requirements at power-plant scale not defined |
| Replacement/maintenance schedule | truly-unknown | important | First-wall lifetime under alpha bombardment not characterized |
| Plant thermal power (MWth) | truly-unknown | blocking | No net-power design; EHL-2 is non-power |

---

## Source Recommendations

**Integrated fleet-wide sources:**

- **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Read and integrated. Covers CAS methodology (COA 21-27) and LCOE $140–550/MWh for a 350 MWe D-T tokamak. Useful as a methodology template and for BOP/structures analog costs. Cannot resolve p-B11-specific blocking gaps (DEC replaces Rankine cycle; no blanket/tritium system). Does not downgrade any blocking gap to important.

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Read and integrated. Contains ARIES-ST (spherical torus with normal conducting coils, LiPb+He D-T blanket) cost data — the closest architectural analog in the fleet-wide sources. ARIES-ST direct costs (~$54–58/kW level from table, CAS 22 blanket at ~$155.7M) confirm that the spherical torus architecture is costed in the ARIES framework. However, ARIES-ST's LiPb blanket and steam cycle are absent from p-B11; the DEC system has no ARIES analog. Does not downgrade any blocking gap.

- **Wurzel & Hsu Lawson criterion** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Read and integrated. Provides the physics benchmark framework. For p-B11, the required Lawson parameter is orders of magnitude above any achieved value and far above EHL-2's design target (Ti0 = 30 keV vs. the 125–330 keV needed for net energy). This source reinforces the "blocking" classification for the physics-feasibility gap but cannot resolve it.

**Disqualified fleet-wide sources:**

- **Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Read (grep). The four ALPHA concepts are compact modular systems (liner compression, HyperJet, Z-pinch type) — none are spherical tokamaks or p-B11 concepts. The $43/MWh LCOE figure applies to D-T compact concepts with conventional power conversion. Not applicable to this concept.

- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific (target, driver, rep rate). Not applicable to MFE.

- **Economic studies for heavy-ion fusion** (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`): HIF driver-dominated economics. Not applicable.

- **Energy from Inertial Fusion**, **Accelerators for IFE**, **AMPS high-yield IFE**, **Commercialization of laser fusion energy**: All IFE-specific. Not applicable.

- **Overview of the Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Stellarator architecture with HTS coils — different confinement topology and power conversion system. Not applicable.

- **An Assessment of the Economics of Future Electric Power** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Historical LCOE benchmark. General energy context only; does not address p-B11 or spherical tokamaks specifically. Disqualified as not filling any specific gap.

**Recommended searches for not-yet-sourced gaps:**

1. *EHL-2 magnet / coil engineering*: Search Fusion Engineering and Design, Plasma Science and Technology, and IEEE Trans. Applied Superconductivity for "EHL-2" + coil/magnet. Chinese-language technical reports at ENN Research or CNKI may contain specifics. Flag: `unverified — confirm existence before searching`

2. *Boron-11 enrichment economics*: Search OSTI and commercial isotope supply literature for boron-11 enrichment cost estimates and supply chain capacity. Companies like Ames Laboratory and 5N Plus supply enriched boron; pricing may be available. Flag: `unverified — confirm existence before searching`

3. *Direct energy conversion for aneutronic fusion*: Search for publications from Rostoker/UC Irvine group (Field Reversed Configuration DEC), TAE Technologies, and the broader MFE DEC literature. Kulcinski/Santarius Wisconsin papers on p-B11 DEC may provide efficiency ranges. Flag: `unverified — confirm existence before searching`

4. *p-B11 burning plasma studies*: Lawson criterion analysis tailored to spherical tokamak geometry (e.g., Meschini et al. 2021/2023 cited in the Frontiersin paper). Search OSTI / arXiv for p-B11 + spherical tokamak + burning plasma.

---

## Summary

This concept cannot support a D1+ analysis at the full quantitative level. **Proceed to a qualitative analysis only**: the physics challenges (hot-ion mode feasibility, bremsstrahlung dominance, CS-free current drive scalability), subsystem TRL assessment, and technology risk analysis are well-supported by available sources. LCOE parameter extraction is not possible — every major economic input is absent or physically undefined. The path forward requires either (a) additional ENN publications post-EHL-2 completion, or (b) construction of a bottom-up analog analysis using D-T MFE plant costs as a baseline, with explicit placeholder assumptions for DEC efficiency, capacity factor, and capital costs — clearly flagged as speculative.

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 8
important_count: 6
counting_method: "all_sections_deduplicated — unique blocking gaps: (1) no power plant design/net electric output, (2) Q/Lawson criterion not approached, (3) DEC technology undefined, (4) hot-ion mode physics contested, (5) capital cost (no concept-specific data), (6) capacity factor undefined, (7) O&M undefined, (8) recirculating power fraction undefined. Important gaps: magnet type unconfirmed, CS-free scalability, boron-11 supply chain, first-wall materials, DEC materials, helium ash exhaust."
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```