# Gap Assessment: Spherical Tokamak - HTS (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Tokamak Energy is more transparent than most private fusion companies, having published machine parameters (R=5.0m, A=2.3, B=5.25T, 450-750 MWe net), magnet validation data (Demo4 at 11.8T), heating approach (EC-only flat-top), and tritium breeding design (outboard liquid Li, TBR=1.2). The primary gap is the complete absence of company-disclosed cost, LCOE, thermal cycle, Q value, and capacity factor data — all of which must be derived from analogues. The TEA D-T MFE Cost Analysis (Araiinejad & Shirvan, MIT, Applied Energy 2025) provides a directly applicable LCOE framework for D-T MFE tokamaks and substantially reduces what would otherwise be blocking gaps. The analysis can proceed to D1+ with stated assumptions, but quantitative LCOE will carry ±50% uncertainty.

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- Machine parameters well-documented: ST-E1 Revision D — R=5.0m, A=2.3, B=5.25T on-axis, net output 450-750 MWe (DPP 2025 abstract, iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md)
- Magnet validation: Demo4 complete HTS system (14 TF + 2 PF coils) validated at 11.8T at 30K (iter-03/sources/tokamak-energy-demo4-magnets.md)
- Heating approach: EC-only flat-top confirmed by peer-reviewed paper — O-mode polarization capable of sole auxiliary power for flat-top (Alieva et al. EPJ 2026, iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md)
- Tritium breeding: outboard-only liquid Li blanket, TBR=1.2 (DPP 2025 abstract)
- Center-stack shielding: WC cermet, ~32cm radial space, materials characterization including thermal conductivity, mechanical properties, irradiation behavior (Humphry-Baker & Smith 2019, iter-02/sources/spherical-tokamak-center-stack-shielding.md)
- Pulsed operation physics basis: Gryaznevich et al. 2022 establishes volt-second requirements, bootstrap fractions (~90%), CS sizing — 2000s flat-top achievable with a CS radius of 0.2-0.3m (iter-01/sources/pulsed-spherical-tokamak-paper.md)
- Roadmap: ST40 → ST80-HTS (2026) → ST-E1 (mid-2030s); $335M raised, DOE Milestone-Based program participant, Furukawa HTS tape partnership (iter-04)
- MFE D-T cost framework (analogue): TEA D-T MFE Cost Analysis provides capital costs $8,800–22,200/kW and LCOE $140–550/MWh for a 350 MWe D-T MFE tokamak (ARC concept) with full CAS breakdown (`knowledge/sources/tea_dt_mfe_cost_analysis/`)

**Missing**:
- Q value (plasma gain) — not disclosed after 3 research iterations; burning plasma inferred from power output targets
- Thermal cycle type (steam Rankine vs. sCO2) — not disclosed after 3 research iterations; company may not have selected it yet
- Capital cost estimates, LCOE projections, or cost breakdown for ST-E1 — entirely proprietary
- Capacity factor / availability factor — DPP abstract mentions "compatible with reactor-level performance and availability factor" without a number
- Power balance / recirculating power fraction — not stated

**Gaps**:
- Published cost and LCOE data for ST-E1 — proprietary — important (TEA D-T MFE analogue directly applicable; downgraded from blocking)
- Q value — proprietary — important (back-estimable from 450-750 MWe with assumed thermal efficiency, but with wide range ~5-20)
- Thermal cycle type — proprietary/not yet decided — important
- Capacity factor — proprietary — important (standard MFE pilot plant assumptions ~85% applicable)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Pulsed ST physics documented: Gryaznevich et al. 2022 establishes that the HTS CS (radius 0.2-0.3m, 8-15T optimal field) provides 2000s flat-top at approximately 1 mV loop voltage; bootstrap fraction ~90% reduces external CD requirements; BV ramp-up eliminates need for CS volt-seconds during startup (iter-01/sources/pulsed-spherical-tokamak-paper.md)
- Outboard-only blanket constraint: DPP 2025 confirms the architectural tradeoff — compact center-stack precludes inboard breeding; TBR=1.2 achieved with outboard-only configuration (iter-03)
- Center-stack shielding challenge: 32cm radial constraint with competing demands for neutron shielding, magnet protection, and cryogenic load management; Humphry-Baker 2019 shows WC cermet outperforms pure W on most metrics but documents multiple open uncertainties (iter-02/sources/spherical-tokamak-center-stack-shielding.md)
- EC heating and current drive: Alieva et al. 2026 validates O-mode EC as capable of sole flat-top auxiliary power via ray-tracing for three scenarios with different magnetic field and aspect ratio (iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md)
- CS recharging approach: Gryaznevich 2022 proposes RF/microwave recharging during flat-top; implies intermittent efficiency reduction is short-duration and bounded (iter-01)

**Missing**:
- Divertor design and power exhaust approach not detailed in any available source — high heat flux handling at 450-750 MWe scale is a major challenge
- Thermal energy storage for quasi-steady pulsed operation (15-min cycles) — acknowledged in iter-01 as a known challenge with molten salt as candidate, but no ST-E1-specific design published
- Maintenance scheme — cited in DPP abstract as a key design element that was "considered very early on," but no details published
- CS recharging duty cycle and its effect on capacity factor not quantified

**Gaps**:
- Divertor design / power exhaust — not-yet-sourced — important (STEP, MAST-U publications would serve as proxies; search OSTI for "spherical tokamak divertor pilot plant")
- Thermal energy storage for pulsed operation — not-yet-sourced — important
- CS recharging duty cycle impact on availability — derivable — important
- Maintenance scheme / remote handling approach — proprietary — nice-to-have

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- HTS magnet system: Demo4 validated complete 14 TF + 2 PF coil set at 11.8T in tokamak configuration — world-first system-level validation; operates at 30K with plug-in cooling capability — TRL 5-6 (iter-03/sources/tokamak-energy-demo4-magnets.md)
- ST40 plasma physics: Achieved 100M°C ion temperature, highest triple product of any private fusion company, peer-reviewed; operates at < 1 m³ plasma volume; $52M upgrade underway for Li-wall and RF heating — TRL 4-5 for compact ST plasma physics
- ECRH/ECCD: ST40 demonstrated ECRH with 1MW Kyoto Fusioneering gyrotron; Alieva et al. 2026 validates EC current drive via simulation at FPP parameters — TRL 4-5
- WC cermet center-stack shielding: Humphry-Baker & Smith 2019 characterizes thermal conductivity (WC comparable to pure W at ~90-180 W/m-K), fracture toughness (WC-Co cermet flexural strength 3.9 GPa vs ~0.8 GPa for binderless WC), and radiation behavior. WC-FeCr cermet under development — TRL 3-4 (iter-02/sources/spherical-tokamak-center-stack-shielding.md)
- Pulsed ST reactor operation: MAST, JT-60U demonstrate BV ramp-up; MAST-U, NSTX-U provide ongoing spherical tokamak data — subsystem-level physics TRL 4-5

**Missing**:
- Liquid Li blanket: ORNL collaboration on Li-compatible coatings confirmed; but outboard-only reactor-scale Li blanket not demonstrated — estimated TRL 2-3
- Tritium extraction and processing system: Not addressed in any available source
- Divertor / plasma-facing components at reactor power loads: Not detailed
- HTS tape radiation tolerance at 14 MeV fusion neutron fluence: Humphry-Baker explicitly flags that "existing fission reactor irradiation studies may provide an overly optimistic picture of irradiation damage resistance" for REBCO at cryogenic operation temperatures — data gap is fundamental

**Gaps**:
- Liquid Li blanket TRL — not-yet-sourced — important
- Tritium extraction system TRL — not-yet-sourced — important
- HTS tape radiation tolerance at fusion-relevant fluence — truly-unknown — important (Humphry-Baker 2019 identifies this as an open research question requiring cryogenic fusion-spectrum irradiation data not yet available)
- Divertor at ST-E1 power loads — not-yet-sourced — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO HTS tape: Furukawa Electric partnership confirmed for specialist HTS tape provision; Demo4 demonstrates production and integration capability at system level (iter-04/sources/tokamakenergy-about-us-fusion-energy-high-temperature.md)
- WC cermet manufacturing: Humphry-Baker 2019 confirms cermet manufacturing for energy extraction and tooling applications is well-established; fusion-specific fabrication challenges documented but pathway exists (iter-02/sources/spherical-tokamak-center-stack-shielding.md)
- Company supply chain infrastructure: $335M raised; Ridgway Machines division provides industrial manufacturing for superconducting and electrical equipment; General Atomics MOU for large-scale magnet manufacturing (iter-04)

**Missing**:
- REBCO tape volume requirements at ST-E1 pilot plant scale — not published
- Li-6 enrichment requirements for liquid lithium blanket — not discussed in any source
- Tritium startup inventory and ongoing supply — not addressed
- Center-stack replacement strategy — neutron dose limit for WC cermet + HTS tape not quantified; replacement frequency unknown
- WC cermet manufacturing at nuclear-grade quality and scale — not addressed

**Gaps**:
- REBCO tape volume for pilot plant — proprietary — important (REBCO currently ~$100-200/m; pilot plant geometry allows rough estimate but company-specific data unavailable)
- Li-6 enrichment requirements — not-yet-sourced — important (generic D-T blanket literature applicable)
- Tritium inventory and startup supply — not-yet-sourced — important
- WC cermet replacement schedule — truly-unknown — important (radiation damage limit unestablished per Humphry-Baker 2019)

---

### 5. LCOE Parameter Extraction

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric output | 450–750 MWe | DPP 2025 abstract (iter-03) | medium |
| Major radius | 5.0 m | DPP 2025 abstract | high |
| Aspect ratio | 2.3 | DPP 2025 abstract | high |
| On-axis toroidal field | 5.25 T | DPP 2025 abstract | high |
| Tritium breeding ratio | 1.2 | DPP 2025 abstract | high |
| Operation mode | Quasi-steady, 15+ min pulses | Gryaznevich 2022 (iter-01) | high |
| Blanket type | Outboard-only liquid Li | DPP 2025 abstract | high |
| Primary heating | EC-only (flat-top) | Alieva et al. EPJ 2026 (iter-03) | high |
| Capital cost analogue | $8,800–22,200/kW | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/`) | low (analogue only) |
| LCOE analogue | $140–550/MWh | TEA D-T MFE | low (analogue only) |
| CAS cost structure | Accounts 20–27 (direct), 90–98 (indirect) | ARIES Cost Accounts (`knowledge/sources/aries_cost_account_documentation/`); TEA D-T MFE | high (methodology) |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value (plasma gain) | proprietary | important | Back-estimable: 450-750 MWe net, ~35% η_th, ~20% recirc → fusion power ~1300-2200 MW → Q ~5-20 depending on heating power assumptions |
| Thermal cycle type | proprietary/undecided | important | TEA D-T MFE assumes Rankine (η~35%); sCO2 (~45%) also plausible; explicit assumption required with sensitivity sweep |
| Thermal conversion efficiency | proprietary/undecided | important | Dependent on cycle type; range 35-45% bounds the calculation |
| Capacity factor | proprietary | important | DPP abstract: "compatible with reactor-level availability"; ST maintenance scheme assessed as feasible; ~85% pilot plant assumption defensible |
| Recirculating power fraction | derivable | important | EC heating wall-plug efficiency ~35-40%; with Q~10 and 50-100 MW EC input, recirculating fraction ~10-15% |
| Capital cost by CAS sub-account | proprietary | important | TEA D-T MFE provides ARC-class breakdown; ST geometry shifts fractions (lower magnet field, outboard-only blanket) — ±30-50% mapping uncertainty |
| REBCO magnet system cost at pilot scale | proprietary | important | Demo4 validates technology; volume for ST-E1 not published; REBCO tape price trajectory matters |
| O&M costs | not-yet-sourced | important | Standard MFE analogue: 2-3% of overnight capital per year; no ST-E1-specific data available |
| First wall / blanket lifetime | proprietary | important | Determines replacement frequency and its contribution to O&M |
| Center-stack WC cermet replacement schedule | truly-unknown | important | Radiation damage limit for WC + HTS tape under 14 MeV neutrons at cryogenic temperatures not established |
| Decommissioning cost | derivable | nice-to-have | Standard nuclear analogue: 10-15% of overnight capital; applicable |

---

## Source Recommendations

- **ARIES-ST study (Najmabadi et al. 2003, Fusion Eng. Design 65:143)** — Directly cited in pulsed ST paper (iter-01, reference [8]). Pre-conceptual spherical tokamak reactor design study with CAS-level capital cost breakdown, thermal efficiency, and power balance for an ST power plant. Most relevant historical cost reference for this geometry. Search OSTI or `https://doi.org/10.1016/S0920-3796(02)00302-2`. `not-yet-sourced`

- **STEP pre-conceptual design reports (Kingham et al. 2021; Wilson et al. 2022)** — UK government-funded spherical tokamak power plant program sharing the same low-aspect-ratio geometry as ST-E1. Published design parameters include aspect ratio ~1.8, 800 MWe net, power conversion approach, and maintenance scheme. Most contemporary public analogue to ST-E1. Search: "STEP spherical tokamak energy production 2022 concept." `not-yet-sourced`

- **Tokamak Energy ST80-HTS technical papers (APS DPP 2023-2025)** — ST80-HTS is the direct experimental predecessor to ST-E1, designed to validate 15-minute pulses and HTS magnets at scale. Conference papers from APS DPP 2023/2024 may contain updated performance targets. Search APS DPP archives for "ST80" or "Tokamak Energy bridging device." `not-yet-sourced — confirm existence before searching`

- **MAST-U / NSTX-U divertor and confinement papers** — Best publicly available proxies for ST-E1 plasma physics regime (H-mode confinement, power exhaust, divertor heat loads at spherical tokamak geometry). Directly cited in Gryaznevich 2022. Search Nucl. Fusion recent issues for MAST-U high-power divertor results. `not-yet-sourced`

- **REBCO HTS tape cost projections (e.g., van der Laan et al. or fusion magnet cost analyses)** — Magnet costs are a primary capital cost driver for HTS tokamaks. Published analyses of REBCO tape cost vs. volume learning curves would constrain the magnet sub-account. Search: "REBCO HTS tape cost fusion magnet 2023 2024." `not-yet-sourced`

**Fleet-wide source dispositions:**

- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): *Integrated.* Araiinejad & Shirvan (MIT, Applied Energy 2025) provides a bottom-up NOAK capital cost estimate of $8,800–22,200/kW and LCOE $140–550/MWh for a 350 MWe D-T MFE tokamak based on the ARC concept. Full CAS breakdown provided (accounts 21-27, 90, 93, 60); Rankine cycle assumed; fusion-specific component fabrication and regulatory framework identified as primary cost drivers. Directly applicable as primary cost analogue for ST-E1. Capital cost gap downgraded from blocking to important on this basis; ST geometry differences (outboard-only blanket, lower 5.25T vs. ARC's ~12T field) introduce ±30-50% structural uncertainty in the mapping.

- **ARPA-E ALPHA Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): *Integrated for CAS methodology only.* The four concepts are plasma-jet MIF (LANL/HyperJet), stabilized liner compressor (Compact Fusion Systems), staged Z-pinch (MIFTI), and flow-stabilized Z-pinch (Zap Energy) — compact modular MIF/Z-pinch, not spherical tokamaks. Their $43/MWh average LCOE and $2.4/W CapEx at ~500 MWe are for fundamentally different physics and cannot be used as ST-E1 cost analogues. CAS accounts 20-27 and methodology are transferable.

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): *Integrated for CAS methodology.* Documents the definitive fusion cost account hierarchy (Waganer, UCSD-CER-13-01, 2013) with historical lineage from Starfire (1980) through the ARIES series. Confirms accounts 20-27 (direct) and 90-98 (indirect) as the applicable framework; documents GDP Implicit Price Deflator escalation methodology. Foundational reference for any D-T MFE cost model.

- **Lawson criterion progress** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): *Integrated for TRL context.* Wurzel & Hsu (ARPA-E, 2021) compile peer-reviewed triple product data across MCF/ICF/MIF. Paper explicitly notes that "tokamak-based MCF has achieved the highest values of T and nτ," confirming ST40's class has the strongest physics pedigree. Provides framework for contextualizing the gap between ST40's current performance and the burning plasma regime required for ST-E1. Applicable to §3 TRL assessment.

- **Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): *Disqualified.* A 390 MWe planar-coil stellarator with natural stability, thick shielding, and sector maintenance. Different confinement family, geometry, and cost structure — no applicable data for spherical tokamak assessment.

- **ORNL historical assessment** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): *Disqualified.* Historical LCOE benchmarking of fusion against coal/nuclear (pre-HTS era). Contains no ST-specific or HTS-relevant data applicable to current ST-E1 gaps.

- **All IFE sources** (simplified economic model, AMPS/Pacific Fusion, Xcimer, heavy-ion, energy from IFE, accelerators): *Disqualified.* Wrong confinement family (inertial); physics, cost structure, and technology drivers entirely different from MFE spherical tokamak.

- **PyFECONS** (`/home/reid/PyFECONS`): *Deferred to LCOE model construction phase.* A costing codebase for MFE+IFE (not an extracted document in `knowledge/sources/`). Applicable for computing LCOE once parameters are assembled; not a data source for this gap assessment.

---

## Summary

Proceed to full D1+ analysis. The concept is well-defined at the machine parameter level and backed by peer-reviewed publications on magnets, heating, and pulsed operation physics. The TEA D-T MFE Cost Analysis provides a directly applicable LCOE methodology that addresses the most significant structural gap (absent company cost data). **Priority actions before quantitative modeling**: (1) acquire the ARIES-ST study (Najmabadi 2003) as the most concept-specific historical cost reference for spherical tokamak reactor designs, and (2) acquire STEP pre-conceptual design reports as the contemporary public analogue. All other LCOE parameters can be estimated with stated assumptions and explicit sensitivity sweeps on Q value (5–20 range), thermal efficiency (35–45%), and capacity factor (80–90%).

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 0
important_count: 7
counting_method: "deduplicated_across_all_sections: Q_value, thermal_cycle_type, capacity_factor, capital_cost_by_CAS_subaccount, OandM_costs, first_wall_blanket_lifetime, center_stack_replacement_schedule"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```