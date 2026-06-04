# Gap Assessment: Renaissance Stellarator (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Renaissance Fusion has published an unusually strong peer-reviewed basis for a pre-commercial startup: three journal papers covering the economic design point (Nuclear Fusion 64, 2024), blanket neutronics (J. Nuclear Materials 599, 2024), and power conversion (Energy Conversion and Management 276, 2023). These sources provide high-confidence values for most physics and engineering parameters. Fleet-wide analogs (TEA D-T MFE cost analysis, Helios stellarator design) fill LCOE methodology and plant-level capacity factor gaps. Two blocking gaps remain: the laser-patterned HTS coil manufacturing process has no published performance or cost data at stellarator scale, and the flowing liquid metal first wall has been characterized only in a 1D simplified model with fundamental MHD engineering challenges unaddressed. A D1+ analysis can proceed but must acknowledge that the two novel subsystems at the heart of the design — the coil and the first wall — have cost and engineering profiles that are genuinely unknown.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- *Nuclear Fusion 64 (2024) 026007* (Prost & Volpe): economically optimized design point — all key physics parameters (R=3.8 m, A=4.1, B=10.2 T, 1 GWe, Q=∞ ignition target, NNBI startup, net plant efficiency 34%)
- *J. Nuclear Materials 599 (2024) 155239* (Prost, Ogier-Collin, Volpe): compact fusion blanket — full 1D neutronics, radial build (32 cm LM + 5 cm vacuum vessel + 54 cm shield = 91 cm total plasma-to-coil), TBR=1.53–1.60, energy multiplication fm=1.07, lifetime assumptions (32 fpy at 80% availability = 40 calendar years), HTS coil dose and DPA budgets
- *Energy Conversion and Management 276 (2023) 116572* (Fama et al.): sCO2 Brayton-Rankine combined cycle — cycle efficiency 49–51%, net plant efficiency 34%, coolant outlet 700–900°C
- *arxiv-1512-01930* (Senatore et al., 2015): Jc(T,B,θ) scaling for REBCO coated conductors from 6 commercial manufacturers — directly applicable to HTS TRL and materials assessment
- *UKAEA PROCESS stellarator documentation*: systems code methodology for generic modular stellarators; ISS04/ISS95 confinement scaling laws, blanket/shield sizing models, availability calculations
- MT29 abstract and UC Berkeley seminar: magnet program; 6 T peak Helmholtz demo at 1.2 m diameter, 20 K validated
- Fleet analog — TEA D-T MFE cost analysis (`knowledge/sources/tea_dt_mfe_cost_analysis/`): LCOE $140–$550/MWh for D-T MFE; CAS accounts 21–27 methodology; includes ARIES-CS compact stellarator references with ~1000 MWe power core mass of 12,555 t; OCC $8,800–$22,200/kWe for HTS tokamak analog (ARAI/ARC)
- Fleet analog — Helios stellarator design (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): 390 MWe HTS planar coil stellarator, 88% capacity factor (84-day biennial outage), 40% thermal conversion efficiency, 40-year coil lifetime, TBR=1.3, minimum plasma-coil distance 1.2 m — directly comparable stellarator plant architecture

**Missing**:
- No published concept-specific capital cost study or CAS-level estimate for the Renaissance Fusion design
- No formal operations and maintenance (O&M) cost analysis
- No published divertor design or power exhaust scenario (the Nuclear Fusion 2024 paper is physics-focused; no plasma-facing divertor hardware is described)
- Company transparency limited; no public engineering roadmap or production schedule

**Gaps**:
- No concept-specific capital cost estimate — proprietary/not-yet-sourced — important (TEA D-T MFE and Helios analogs provide bracketing methodology, so blocking status is relieved)
- No O&M cost data — not-yet-sourced — important
- No divertor engineering design published — not-yet-sourced — nice-to-have

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Blanket system function is well described: J. Nuclear Materials 599 (2024) gives explicit requirements (TBR ≥ 1.15, DPA < 200, dose < 25 μSv/h), material candidates, and a 1D optimization result. The integrated liquid-metal architecture (first wall + breeder + shield + coolant in one layer) is clearly characterized in the 1D neutronics model.
- Power conversion function: the sCO2 combined cycle design is published with genetic-algorithm optimization and efficiency targets (49–51% cycle, 34% net plant). The high coolant outlet temperature (700–900°C from LM wall) is the key enabler and is well-documented.
- Steady-state operation: inherent stellarator advantage (no plasma current drive) is well-documented; PROCESS stellarator documentation describes the physics basis (ISS04 scaling, no disruptions, Sudo density limit).
- Ignition physics extrapolation: the design paper states Q = ∞ and zero external heating at steady state, relying on alpha heating. This is an aggressive extrapolation from existing stellarator experiments but is internally consistent given the design parameters.
- Fleet context — Wurzel & Hsu (Lawson criterion compilation, `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): provides the benchmark that no stellarator has achieved ignition-class triple products; W7-X is the most advanced operational stellarator but remains many orders of magnitude below Renaissance's ignition target. The Q=∞ design represents a physics extrapolation of ~4 orders of magnitude in nTτE from current stellarator experiments.

**Missing**:
- Laser-patterned HTS coil field quality in 3D stellarator geometry: the magnet innovation (depositing HTS REBCO film on cylinders and laser-ablating current paths) produces a 3D field from a modular cylindrical approach. No published data shows that this approach achieves the precise quasi-isodynamic field required for the confinement performance assumed in the design paper. The 6 T Helmholtz demo validates the magnet concept but not stellarator field quality.
- Flowing liquid metal in 3D non-axisymmetric geometry: MHD effects on Li-LiH flow in a stellarator (non-axisymmetric) magnetic field configuration are not characterized. In tokamaks, LM MHD braking is already a major challenge; in a stellarator with complex 3D fields, this is compounded. The blanket paper explicitly states it "provides a promising starting point for in depth neutronic studies which would include specific neutron sources and spectra, shutdown dose rates, decay heat, as well as activation calculations."
- Tritium extraction from the flowing LM wall: no published description of the tritium extraction process from the Li-LiH wall at operational temperature (700–900°C). This is a critical system function given the tritium inventory concerns at GWe scale.
- Recirculating power balance: the 34% net efficiency implies a recirculating fraction accounting for HTS cryogenic load (20 K operation), LM pumping, and auxiliaries. This breakdown is not explicitly published; only the net value appears in the power conversion paper.

**Gaps**:
- Laser-patterned HTS stellarator field quality at scale — truly-unknown — **blocking** (no experiments demonstrate the required 3D field accuracy; cannot characterize plasma confinement or coil cost without this)
- Flowing LM MHD engineering in 3D stellarator geometry — truly-unknown — **blocking** (1D model only; MHD forces in non-axisymmetric field are fundamentally different and will drive both system function and maintenance design)
- Tritium extraction from flowing LM wall — truly-unknown — important
- Recirculating power fraction breakdown — derivable — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- HTS magnet (TRL 3–4): 6 T peak Helmholtz magnet at 1.2 m diameter, 20 K demonstrated. REBCO critical current scaling data available from 6 commercial manufacturers (arxiv-1512-01930); Jc(T,B,θ) characterized to 19 T and 4.2–77 K. Target of 10–15 T on-axis (peak coil field up to 20–40 T per design paper) represents extension of demonstrated capability. The laser-patterning manufacturing process is the key novel step.
- Liquid metal first wall (TRL 2): 1D neutronics model validated; material selection (Li-LiH, Pb pebbles, V-Cr-Ti vessel) supported by published cross-section and property data. No prototype or flow experiment.
- Power conversion sCO2 Brayton-Rankine (TRL 4–5): sCO2 turbines exist commercially (Echogen, various pilot plants to ~10 MWe). The Fama et al. (2023) analysis provides the fusion-adapted design. GWe-scale sCO2 power plants have not been built, but the technology path is well-defined.
- NNBI heating (TRL 6–7): negative NBI exists on JT-60SA and is specified for ITER; 60% neutralization efficiency is a known parameter. For Renaissance's ignited design, NNBI is only needed for startup, reducing its performance criticality.
- Tritium fuel cycle (TRL 2–3): no fusion-scale T breeding demonstrated anywhere; breeding ratio calculation is validated in 1D model. The Helios design analog (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`) confirms that 1–2 kg T startup inventory is the current state of the art for stellarator plant designs (identical value in Helios Table 1).
- Stellarator coil set TRL via Helios analog: the Helios design demonstrates that a planar HTS stellarator coil set can be engineered to 40-year lifetime with proper shielding (1.2 m minimum plasma-coil distance, confirmed in both designs).

**Missing**:
- TRL for laser-patterned HTS manufacturing process: no published scale-up roadmap or intermediate demonstrator beyond the 6 T Helmholtz magnet. No published data on field uniformity, quench performance, or manufacturing yield for the laser-patterned approach.
- No experimental confinement data from any Renaissance Fusion device; all confinement projections rely on W7-X extrapolation via ISS04 scaling.
- Divertor technology for this geometry: no divertor concept has been published for the laser-patterned cylindrical stellarator.

**Gaps**:
- Laser-patterned HTS coil TRL: only single component demo (TRL 3–4), no stellarator integration — truly-unknown for the manufacturing process — important
- Plasma confinement validation (no Renaissance Fusion experiments) — not-yet-sourced (relies on W7-X extrapolation) — important
- Divertor design and TRL — not-yet-sourced — nice-to-have

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- REBCO HTS tape: arxiv-1512-01930 confirms commercial availability from 6 manufacturers (AMSC, Bruker, Fujikura, SuNAM, SuperOx, SuperPower) with characterized Jc(T,B) to 19 T. Supply chain exists; production scale-up for reactor quantities is the key question.
- Pb pebbles: standard industrial material; no supply chain risk.
- LiH/Li: LiH is commercially available as a specialty chemical; 95 mol% LiH + 5 mol% Li mixture is non-standard but components are not rare. The blanket paper notes that Li-6 enrichment would improve performance margins but adds cost via the separation process (referenced in the paper as a cited challenge with reference to Giegerich et al., Fusion Eng. Des. 149, 2019).
- V-Cr-Ti (vanadium alloy): the blanket paper (J. Nucl. Mater.) specifies V-14.5Cr-5Ti for the vacuum vessel for its corrosion resistance and low activation properties. Limited global vanadium production; ITER and DEMO programs have driven some development.
- Vanadium hydride (VH2): specified as the neutron shielding material (54 cm layer achieving 53 cm minimum thickness requirement per Fig. 9 of blanket paper). VH2 is a specialty material with limited production precedent at this scale.
- SiC pebble shells: specified for encapsulating Pb pebbles; SiC is commercially available.

**Missing**:
- Scaled production cost and supply chain for laser-patterned REBCO film deposition on 1 m diameter cylinders: this is an industrial process that does not exist today. Conventional REBCO tape is sputtered on flat Hastelloy substrates; adapting this to large-diameter curved surfaces at reactor quantities requires entirely new manufacturing infrastructure.
- VH2 production at ~tonne scale for neutron shielding: limited precedent; cost is unknown.
- sCO2 turbomachinery supply chain at GWe scale: currently no commercial manufacturer produces GWe-scale sCO2 turbines.

**Gaps**:
- Laser-patterned REBCO film deposition on cylinders at scale — truly-unknown — blocking (this is the manufacturing crux of the entire design; no production process exists)
- VH2 shielding at reactor scale — not-yet-sourced — nice-to-have (ITER shielding studies may provide analog; specialty material but not a rare element)
- sCO2 turbomachinery supply chain at GWe scale — not-yet-sourced — important

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | ~2 GW | J. Nucl. Mater. 599 (2024): "1 GWe ≃ 2.2 GWth, and ≃ 2 GW fusion power" | high |
| Net electrical output | 1 GWe | Nuclear Fusion 64 (2024) design point | high |
| Gross cycle efficiency | 49–51% | Energy Conv. Mgmt. 276 (2023) sCO2 optimization | high |
| Net plant efficiency | 34% | Energy Conv. Mgmt. 276 (2023) | high |
| Coolant outlet temperature | 700–900°C | J. Nucl. Mater. 599 (2024): LM wall operating range | high |
| Plant lifetime (design) | 40 calendar years | J. Nucl. Mater. 599 (2024): "32 fpy assuming 40 years at 80% availability" | high |
| Implied availability | ~80% | Derived from blanket paper lifetime assumption | medium |
| Capacity factor analog | 88% | Helios stellarator (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): 84-day biennial outage | medium (analog) |
| TBR | 1.53–1.60 | J. Nucl. Mater. 599 (2024) case study | high |
| Blanket energy multiplication | 1.07 | J. Nucl. Mater. 599 (2024) | high |
| Radial build (plasma-to-coil) | 91 cm | J. Nucl. Mater. 599 (2024): 32+5+54 cm | high |
| Major radius | 3.8 m | Nuclear Fusion 64 (2024) | high |
| Aspect ratio | 4.1 | Nuclear Fusion 64 (2024) | high |
| On-axis field | 10.2 T | Nuclear Fusion 64 (2024) | high |
| Peak coil field | 15–40 T | Nuclear Fusion 64 (2024) range | medium |
| Wall loading | 25 MW/m² | Dossier (J. Nucl. Mater. paper) | medium |
| LCOE range (D-T MFE analog) | $140–$550/MWh | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/`) | low (analog; HTS tokamak, not stellarator) |
| OCC analog (NOAK D-T MFE) | $8,800–$22,200/kWe | TEA D-T MFE (ARAI, 350 MWe HTS tokamak) | low (analog) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost — CAS-22 magnet (laser-patterned HTS) | truly-unknown | blocking | Novel process; no production cost data; this is the largest unknown in the cost model |
| Capital cost — CAS-22 first wall/blanket (flowing LM system) | truly-unknown | blocking | No prototype; LM pumping infrastructure, tritium extraction hardware, and containment are uncostable without engineering design |
| Capital cost — full CAS breakdown | proprietary/not-yet-sourced | important | No concept-specific costing published; TEA D-T MFE provides framework but Renaissance's novel subsystems deviate from ARIES-CS basis |
| O&M costs (annual) | not-yet-sourced | important | Generic MFE O&M in fleet sources (~$30–60/MWh); Renaissance's continuous LM flow may reduce first-wall replacement costs |
| Recirculating power breakdown | derivable | important | Net - gross efficiency gap (34% vs 49–51%) implies ~30% recirculating fraction; cryo load, LM pumps, and auxiliaries not broken out |
| Construction schedule (FOAK vs NOAK) | not-yet-sourced | important | No published roadmap; affects IDC and financing costs |
| Capacity factor (formal) | derivable | important | ~80% from blanket lifetime; 88% from Helios analog; low uncertainty but not published in concept papers |
| Decommissioning cost | not-yet-sourced | nice-to-have | Generic nuclear analogs applicable; low-activation materials (V-Cr-Ti) may reduce this |
| sCO2 turbomachinery cost | not-yet-sourced | important | GWe-scale cost unknown; emerging technology |

---

## Source Recommendations

- **Prost & Volpe, Nuclear Fusion 64 (2024) 026007** [already sourced]: The primary design paper should be fully extracted if not already done; it is the anchor for all physical parameters.
- **Fama et al., Energy Conversion and Management 276 (2023) 116572** [already sourced]: Power conversion paper; key for efficiency and recirculating power. Confirm whether a recirculating power breakdown table exists in the full text.
- **ARIES-CS design study** (Najmabadi et al., Fusion Science and Technology, ~2008): The only prior compact stellarator power plant design study with CAS-level cost estimates. Would provide the best-available cost analog for Renaissance Fusion's novel subsystems. The TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`) cites ARIES-CS with power core mass ~12,555 t; the original ARIES-CS report would have the CAS-level breakdown. Search OSTI for "ARIES-CS cost account" or "ARIES-CS design study." — not-yet-sourced, unverified exact OSTI accession number.
- **Divertor and power exhaust design** for the Renaissance cylindrical stellarator: search `renfusion.eu/papers` or conference proceedings (SOFT, IAEA FEC) for any unpublished divertor work. Company website lists papers through 2024. — not-yet-sourced.
- **Flowing liquid metal blanket MHD studies** for non-axisymmetric fields: literature search on "liquid metal MHD stellarator" or "LM flow stellarator non-axisymmetric." Relevant experimental programs at KIT (Germany) and UCLA. — not-yet-sourced.
- **VH2 neutron shielding production cost**: Tanaka et al. (Fusion Science and Technology 68, 2015) is cited in the blanket paper for VH2 shielding in FFHR-D1 helical reactor — may contain cost-relevant data. — not-yet-sourced, unverified — confirm existence before searching.
- **Disqualified — Revisit of 2017 ARPA-E ALPHA Concepts** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened and confirmed to cover four ARPA-E ALPHA compact concepts (FRC-like, linear systems). Their modular design economics (average ~$43/MWh) do not map to a GWe-scale toroidal stellarator with distributed LM wall; architecture is fundamentally incompatible as a cost analog.
- **Disqualified — An Assessment of Economics of Future Electric Power Generation Options (ORNL/TM-1999-243)** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Opened and confirmed as a 1999 ORNL benchmarking report. The contemporary LCOE context it provides (comparing fusion to coal, nuclear, wind) is already superseded by the TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`, 2025), which covers the same LCOE benchmarking function with current cost assumptions and is more directly applicable to this concept.
- **Disqualified — IFE sources (Hawker simplified model, HIF economics, Energy from Inertial Fusion, Xcimer, Pacific Fusion/AMPS, Accelerators for IFE)**: All are specific to inertial fusion energy concepts and do not address any gap in a MFE stellarator analysis.

---

## Summary

Proceed to full D1+ analysis with these caveats:

1. **Qualitative sections** (data availability, system function challenges, subsystem maturity, supply chain) can be written to high quality. The three peer-reviewed papers provide unusual depth for a pre-commercial startup, and the fleet analogs (Helios, TEA D-T MFE, ARIES Cost Account Doc) fill the structural gaps.

2. **Quantitative LCOE section** requires explicit acknowledgment that the two novel subsystems at the heart of the design — the laser-patterned HTS coil and the flowing LM first wall — have no published cost data and represent the dominant LCOE uncertainty. Estimates must be presented as methodology-derived bounds using ARIES-CS or Helios analogies, with a wide uncertainty band reflecting genuinely unknown manufacturing costs.

3. The ARIES-CS design study is the highest-priority source acquisition before finalizing quantitative costs. It is the only published CAS-level costing of a compact stellarator and would directly address the largest outstanding gap.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 2
important_count: 8
counting_method: "deduplicated across all sections: blocking = (1) laser-patterned HTS coil cost/performance at scale, (2) flowing LM first wall MHD engineering at scale; important = (1) full CAS capital cost, (2) O&M costs, (3) recirculating power breakdown, (4) capacity factor (derivable but not formally stated), (5) plasma confinement validation (no experiments), (6) divertor design, (7) sCO2 turbomachinery supply at GWe scale, (8) construction schedule/FOAK-NOAK split"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```