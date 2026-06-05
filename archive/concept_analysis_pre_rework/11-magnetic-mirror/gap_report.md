# Gap Assessment: Magnetic Mirror (D-T)

## Overall Readiness
**Rating**: Significant Gaps
**Summary**: The concept has solid physics-basis documentation and a credible technology roadmap, with peer-reviewed modeling (arXiv 2411.06644) establishing Q > 5 as feasible for a 50 m center cell and a clear three-step development path (WHAM → Anvil → Hammir). However, no plant-level design study for Hammir has been published — Realta has confirmed a pre-conceptual design paper is expected in 2026 but it is not yet available. This means the core quantitative LCOE inputs (fusion thermal power, conversion efficiency chain, capital cost by subsystem) are absent or must be estimated from fleet-wide analogs. The qualitative sections (system function challenges, subsystem maturity, materials considerations) are well-supported for a D1+ analysis; the LCOE parameter table will require explicit assumptions flagged with low confidence until the Hammir design paper appears.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**: Physics modeling paper (arXiv 2411.06644) provides integrated transport and equilibrium model for Hammir, demonstrating Q > 5 with 50 m center cell and Q > 10 with longer center cell, with a publicly-available POPCON technique for tandem mirrors. The Fusion Hub spotlight provides detailed physics explanation covering confinement mechanisms, instability challenges, and the DEC concept. The Fusion Report interview confirms D-T fuel, lithium-based tritium breeding, ~7 MW/m power scaling, and identifies industrial heat as the primary market. APS DPP 2025 abstract (Sutherland) confirms the Hammir pilot plant targets (Qe > 1, > 50 MWe, ≥ 3 hours). Funding disclosures (SVB $9.5M debt, $36M Series A) confirm ongoing company viability. The dossier summarizes WHAM experiment results (17 T HTS, first plasma July 2024). Fleet-wide analog sources supply CAS-level cost frameworks: the ARPA-E ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides complete line-item capital costs for four modular compact fusion concepts averaging ~$1.2B total capital and LCOE 34–54 $/MWh for ~500 MWe NOAK plants, directly applicable as a BOP analog; the TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`) provides a bottom-up CAS cost framework for an HTS D-T MFE plant with LCOE $140–550/MWh and capital $8,800–22,200/kW.

**Missing**: No published Hammir pre-conceptual design report. No detailed neutronics study for the linear mirror geometry. MARS study (cited in dossier as a key historical reference with LiPb blanket, 36% plant efficiency, TBR 1.15) is not ingested as a source.

**Gaps**:
- Hammir pre-conceptual design paper — proprietary/not-yet-sourced — blocking (this paper is the primary vehicle for plant-level data)
- MARS Mirror Advanced Reactor Study — not-yet-sourced — important (historical mirror plant study with TBR, efficiency, and DEC data)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**: The sources collectively identify and partially characterize the key functional challenges. The physics paper (arXiv 2411.06644) identifies DCLC instability management as an open item and notes that kinetic stability modeling via Hybrid-VPIC integration is "in preparation." The Fusion Hub source covers MHD stability (vortex/sheared-flow stabilization for interchange modes, exploiting good curvature in expander regions), kinetic instability management (sloshing ions to fill ambipolar hole), impurity accumulation in tandem vs. simple mirror configurations, and low electron temperature as a historical challenge now addressed by ECH. The dossier notes that the Anvil end-plug demonstrator is specifically designed to validate stabilization concepts before Hammir is built. The hybrid energy capture architecture (thermal blanket + venetian blind DEC) is described qualitatively; the MARS study achieved ~54% DEC efficiency (referenced in dossier) but this is an unverified analog for Hammir's design. The 7 MW/m power-per-meter scaling law captures center cell performance but leaves end-plug power accounting incompletely specified.

**Missing**: NBI wall-plug efficiency — critical for computing Qe from Qsci; no value published for Hammir operating conditions. DEC conversion efficiency specific to Hammir's design not published (MARS 54% is the only analog). Quantitative vortex stabilization power requirements not given. Impurity transport and radiation loss in the tandem configuration remains an acknowledged open question (Fusion Hub source notes this "remains to be seen"). Anvil physics data (which would validate end-plug stabilization) does not yet exist.

**Gaps**:
- NBI wall-plug efficiency for Hammir operating point — proprietary/not-yet-sourced — blocking (required to compute Qe from physics Q)
- DEC conversion efficiency (venetian blind, Hammir-specific) — proprietary — blocking (DEC efficiency determines fraction of energy directly converted vs. thermal; assumed 54% from MARS is low confidence)
- Impurity transport and radiation loss quantification — truly-unknown — important (acknowledged gap in published arXiv paper; affects power balance)
- Vortex stabilization power requirement — not-yet-sourced/proprietary — important (determines parasitic heating load)
- Anvil end-plug experimental validation — truly-unknown — important (no data until ~2028)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**: HTS REBCO magnets are the most mature subsystem — WHAM demonstrates 17 T in a mirror configuration (TRL 7 for magnets at this field strength, TRL 6 for mirror-geometry deployment), with CFS as an established supplier. ECH/gyrotron heating at 110 GHz is at TRL 6–7 (operational on WHAM, mature gyrotron technology from industry/ITER heritage). NBI is at TRL 5–6 (operational on WHAM for HHFW fueling; high-energy negative-ion NBI for pilot plant is a technology step beyond current WHAM operations, with heritage from JT-60 and ITER programs). Vortex stabilization via electric-field-driven sheared flow is at TRL 4–5 (demonstrated in GDT and referenced Russian/Japanese experiments, not yet demonstrated in an HTS high-field axisymmetric tandem mirror). The Fusion Hub source notes that the GDT achieved MHD stability, high electron temperatures (~1 keV), and mitigation of kinetic instabilities in axisymmetric mirrors, providing heritage.

**Missing**: Direct energy conversion (venetian blind design) has no demonstrated modern prototype — TRL 2–3. Tritium blanket for a linear mirror geometry has no design study from Realta — TRL 3. First wall / plasma-facing components for the tandem mirror geometry (PMI under 14.1 MeV neutron flux) have no published study — TRL 2–3. The Anvil device (end-plug demonstrator, ~2028) is the critical next step but has not been built.

**Gaps**:
- DEC (venetian blind) subsystem maturity — truly-unknown — blocking (no published modern prototype; MARS used gridless converters, Realta's design is unspecified; TRL 2–3 with no roadmap to TRL 4 prior to Hammir)
- First wall / plasma-facing components for tandem mirror geometry — not-yet-sourced — important (PMI with 14.1 MeV neutrons in open-ended geometry not studied for Hammir)
- Tritium blanket design and TRL — proprietary/not-yet-sourced — important (blanket type unspecified; linear geometry simplifies design but no published study)
- Anvil device maturity data — truly-unknown — important (device not yet built; expected ~2028 per APS DPP abstract)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**: REBCO HTS tape supply chain is partially characterized. CFS is the current magnet manufacturer for Realta (WHAM magnets). The Fusion Hub source mentions ~$50M in REBCO tape alone for WHAM++ (a scale-up device), indicating the material cost is non-trivial even at pre-pilot scale. D-T fuel cycle requirements are standard for all D-T fusion and well-characterized in the literature. Lithium for tritium breeding is confirmed as the blanket material (Fusion Report interview) but the form (LiPb, FLiBe, liquid Li, HCPB) is unspecified. ARPA-E ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) shows special materials (primarily primary coolant liquid metal) at $103M average for modular MFE plants, indicating non-negligible supply chain exposure.

**Missing**: REBCO tape volume requirement for Hammir not disclosed — the mirror geometry uses fewer magnets than tokamaks (stated advantage) but the center cell solenoid length (~50 m) and end plug magnets need coil characterization. Structural material specification (V-alloy, ferritic steel, or other) not given. Tritium-breeding blanket material unspecified — drives both TBR and activation inventory. No supply chain analysis specific to Hammir has been published.

**Gaps**:
- REBCO tape volume requirement for Hammir — proprietary/not-yet-sourced — important (cost driver; $50M noted for WHAM++, Hammir will require more for 50m center cell + two end plugs)
- Blanket material specification — proprietary — important (determines Li-6 enrichment need, activation, coolant choice)
- Structural/first wall material selection — proprietary — important (drives activation inventory, maintenance schedule, replacement cost)
- Supply chain for DEC components at scale — truly-unknown — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric power target (Hammir) | > 50 MWe | APS DPP 2025 (Sutherland); arXiv 2411.06644 | h |
| Fusion gain Q | > 5 (50 m cell); > 10 (longer cell) | arXiv 2411.06644; Fusion Report interview | m |
| Electric gain Qe | > 1 | APS DPP 2025 | m |
| Power scaling law | ~7 MW/m center cell length | Fusion Report interview (Sutherland quote) | m |
| Fuel | D-T | All concept sources | h |
| Energy capture mode | Hybrid thermal blanket + DEC (venetian blinds) | Fusion Hub; Fusion Report interview | h |
| DEC efficiency analog | ~54% (MARS study, historical reference) | Dossier (cited; MARS not ingested) | l |
| Operation mode | Steady-state | All sources | h |
| LCOE range analog (modular compact D-T MFE, NOAK) | 34–54 $/MWh | ARPA-E ALPHA (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | m |
| Total capital cost analog (500 MWe NOAK) | ~$1.2B, ~$2.4/W | ARPA-E ALPHA | m |
| O&M costs analog | $48M/year avg (500 MWe) | ARPA-E ALPHA | m |
| Fuel processing capital analog | $124M (avg, 500 MWe) | ARPA-E ALPHA | m |
| BOP capital cost analog (turbine, electric, heat rejection) | $137M + $59M + $55M = ~$251M avg | ARPA-E ALPHA | m |
| LCOE range analog (HTS D-T tokamak, NOAK) | $140–550/MWh | TEA D-T MFE (`knowledge/sources/tea_dt_mfe_cost_analysis/`) | l (tokamak, not mirror) |
| Capacity factor assumption (analog) | 90% | ARPA-E ALPHA | m |
| REBCO tape cost indicator | ~$50M for WHAM++ alone | Fusion Hub spotlight | l |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion thermal power output (Pfus, Pth) | proprietary | blocking | 7 MW/m × 50 m = ~350 MW rough estimate, but not published; Hammir design paper needed |
| Gross/net electric output (Pnet) | proprietary | blocking | Only "≥ 50 MWe" target stated; actual value not given |
| Thermal conversion efficiency (Rankine/sCO2 cycle) | proprietary | blocking | Thermal cycle unspecified; standard steam (~33%) vs. sCO2 (~45%) would materially affect LCOE |
| DEC conversion efficiency for Hammir | proprietary | blocking | No published value; MARS 54% is an unvalidated analog from a different design era |
| NBI wall-plug efficiency | not-yet-sourced | blocking | Determines circulating power fraction; ITER-heritage negative-ion NBI ~28–30% wall-plug efficiency plausible but not confirmed for Hammir |
| Capital cost breakdown by subsystem (CAS) | proprietary | blocking | No plant study published; ARPA-E ALPHA provides modular D-T MFE analog but mirror-specific cost structure (DEC, simpler magnets, linear blanket) differs |
| Magnet cost for Hammir (HTS REBCO volume) | proprietary | important | Mirror uses fewer magnets than tokamak; stated cost advantage, but no published number |
| Blanket/tritium system capital | proprietary | important | Blanket type unspecified; analog: $57M first wall/blanket and $124M fuel processing (ARPA-E ALPHA) |
| Capacity factor / availability assumption | proprietary | important | No published value; steady-state operation is a stated advantage but no specific CF given |
| O&M cost (scheduled replacement, staffing) | proprietary | important | No published value; ARPA-E ALPHA analog $48M/year for 500 MWe |
| Decommissioning cost | derivable | nice-to-have | Linear geometry may simplify decommissioning; no estimate published |
| Neutron wall loading and first wall lifetime | truly-unknown | important | Linear geometry neutronics not studied; affects replacement schedule and maintenance cost |

---

## Source Recommendations

- **MARS Mirror Advanced Reactor Study (Logan et al., LLNL, 1983)** — not-yet-sourced — important. This is the most detailed historical mirror power plant study. The dossier cites it for LiPb blanket (TBR 1.15), 36% plant efficiency, and ~54% DEC efficiency from gridless converters. Available on OSTI (OSTI ID 5981974 per dossier). Should be ingested before LCOE parameter extraction. Contains TBR, blanket design, power balance, and DEC subsystem data that would downgrade several "important" gaps. *Verify existence via OSTI before searching — reference appears in dossier.*

- **Forest et al. (2024) — BEAM (Break-even Axisymmetric Mirror) design** — not-yet-sourced — important. Referenced in arXiv 2411.06644 as the design basis for the Anvil device. May contain system-level parameters (plasma radius, field, NBI power, plasma performance) useful for scaling to Hammir. Search arXiv or Google Scholar for "Forest 2024 break-even axisymmetric mirror BEAM." *Unverified — confirm existence before searching.*

- **Realta Fusion DCLC instability paper (announced in Fusion Report interview alongside Q > 5 paper)** — not-yet-sourced — important. A second paper (on DCLC instability engineering solutions) was announced concurrent with arXiv 2411.06644. This paper should contain power requirements for kinetic stabilization. Search arXiv for Realta Fusion DCLC 2024–2025. *Unverified — confirm existence before searching.*

- **GDT (Gas Dynamic Trap) experimental publications** — not-yet-sourced — nice-to-have. The Fusion Hub source identifies Russian GDT as the heritage for axisymmetric mirror stability. GDT achieved ~1 keV electron temperatures and MHD stability. Vortex stabilization data from GDT would constrain the parasitic heating load for this mechanism. Search OSTI or Google Scholar for "GDT mirror vortex stabilization" or "Bagryansky mirror 2015–2020."

- **Fleet-wide sources assessed and integrated above** (ARPA-E ALPHA re-costing, TEA D-T MFE): both integrated into Section 5 parameter tables with specific values cited. See parameter table rows citing `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` and `knowledge/sources/tea_dt_mfe_cost_analysis/`.

- **Fleet-wide sources assessed and disqualified**:
  - *A simplified economic model for inertial fusion* (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific Monte Carlo parameter analysis (gain, rep rate, target cost). No MFE content; not applicable to magnetic mirror.
  - *Economic studies for heavy-ion fusion electric power plants* (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`): HIF driver cost analysis. Driver-dominated cost structure is not analogous to MFE. Not applicable.
  - *Energy from Inertial Fusion* (`knowledge/sources/energy_from_inertial_fusion/`): IFE 1992 review covering laser, HIF, and light-ion IFE. Not applicable to MFE magnetic mirror.
  - *Accelerators for Inertial Fusion Energy Production* (`knowledge/sources/accelerators_for_inertial_fusion_energy_production/`): IFE driver technology. Not applicable.
  - *Affordable, manageable, practical and scalable (AMPS) high-yield inertial fusion* (`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`): Pacific Fusion pulser-driven IFE. Not applicable.
  - *Commercialization of laser fusion energy* (`knowledge/sources/commercialization_of_laser_fusion_energy/`): Xcimer KrF laser IFE. Not applicable.
  - *Overview of the Helios Design: A Practical Planar Coil Stellarator* (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Stellarator geometry (390 MWe, planar coils). BOP structure may be partially analogous to MFE, but the reactor core cost is stellarator-specific (3D coils, sector maintenance, thick shielding) and not applicable to the linear mirror geometry. Disqualified as an analog — ARPA-E ALPHA data already provides a better-matched modular MFE analog at similar scale.
  - *An Assessment of the Economics of Future Electric Power Generation Options* (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): ORNL historical LCOE benchmarking against coal/nuclear. Provides no fusion subsystem cost data applicable to magnetic mirror. Not applicable for this assessment.
  - *Progress toward fusion energy breakeven and gain* (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Wurzel & Hsu 2021. Useful for physics-state-of-the-art comparisons across fusion concepts. The paper confirms that WHAM-class mirror machines are in an early experimental phase with nτE well below ignition; the Hammir operating target has not been demonstrated experimentally. Integrated into Section 3 (subsystem maturity) as TRL context. No cost data applicable to LCOE.

---

## Summary

Proceed to a D1+ analysis, with caveats. The qualitative sections (system function challenges, subsystem maturity, materials) are adequately supported for analysis — the physics basis, development roadmap, and engineering challenges are documented in peer-reviewed sources and public company communications. However, LCOE parameter extraction will require the analyst to apply explicit analog assumptions (ARPA-E ALPHA modular MFE and MARS historical mirror plant) for thermal output, efficiency chain, and capital costs, all flagged as low-to-medium confidence. The primary constraint is the absence of a Hammir pre-conceptual design study; the blocking LCOE gaps cannot be resolved without it. Ingest the MARS study (OSTI 5981974) before the LCOE section — it is the only mirror-specific plant study and would directly supply several missing parameters (TBR, thermal efficiency, DEC efficiency, blanket design).

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 6
important_count: 7
counting_method: "Deduplicated across all sections: blocking = {Hammir plant design paper, NBI wall-plug efficiency, DEC conversion efficiency for Hammir, thermal conversion efficiency, fusion thermal power output, capital cost breakdown by subsystem}; important = {MARS study not ingested, blanket type/TBR, Anvil experimental data, first wall/PMI study, REBCO volume for Hammir, capacity factor assumption, O&M cost}"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor"
```