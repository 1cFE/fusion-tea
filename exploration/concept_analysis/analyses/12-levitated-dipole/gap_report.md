# Gap Assessment: Levitated Dipole (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: OpenStar's arXiv 2602.20564 (Simpson et al., 2026) provides exceptional depth for a pre-commercial concept — two full power plant design points with detailed physics, power balances, material masses, neutron transport, and an explicit optimization framework. Sections 1–4 of the D1+ analysis can be written at high quality. The critical gap is economic: OpenStar explicitly withholds absolute capital cost and LCOE figures, describing them as "preliminary results from a model currently in development" (§3.3), blocking Section 5 from being completed quantitatively without relying on fleet-wide analogs. A partial LCOE analysis is possible using the D-T MFE TEA analog (`knowledge/sources/tea_dt_mfe_cost_analysis/`), but key dipole-specific cost drivers (annual core magnet replacement, modular concrete vessel, REBCO tape at scale) are not captured by that source.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**: OpenStar has published two peer-reviewed papers and a public prototype roadmap. Simpson et al. 2026 (arXiv 2602.20564, 262 KB) is the primary source — a detailed FOAK power plant design study with full reactor geometry, power balance, neutron transport (OpenMC), structural mechanics (COMSOL FEA), material masses, and confinement physics. Chisholm et al. 2025 (arXiv 2508.17691) documents the Junior prototype. The Bloomberg and IEEE Spectrum articles confirm the Feb 2026 Junior demonstration and the Tahi/Maui/Tama Nui roadmap. The company has ~80 staff and is funded to ~NZD 35M (USD 21M). The concept has a 35-year academic heritage (LDX at MIT, RT-1 in Japan).

**Missing**: No third-party independent techno-economic assessment has been published. OpenStar's internal cost model is explicitly not yet published (paper §3.1 states "preliminary results from this model… subject to change… we avoid quoting specific values"). The concept has no DEMO-scale or commercial precursor — the nearest analogs (LDX, RT-1) are small academic experiments that did not produce fusion.

**Gaps**:
- No published absolute cost estimate — proprietary — blocking (§5 consequence)
- No independent third-party TEA or cost validation — not-yet-sourced — important
- Academic heritage (LDX/RT-1) does not cover D-T neutronics at plant scale — truly-unknown — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**: The design paper (arXiv 2602.20564) provides exceptionally clear documentation of the key engineering innovations: (a) REBCO CICC coil with two-section sacrificial/permanent architecture; (b) on-board HTS flux pump (patented transformer-rectifier) maintaining ~30 kA without physical connections; (c) neon slush cryogenic reservoir for extended float time (~45 min per cycle); (d) W+B4C layered neutron shield radiatively cooled to first wall; (e) Li2O ceramic breeding blanket at TBR 1.1. The core magnet is physically decoupled from the vacuum vessel — the design's central maintenance advantage. Power balance (Table 9 in arXiv 2602.20564) is fully specified: 667 MW fusion → 741 MW thermal → 296 MW gross → 208 MW net for Reactor A, with explicit accounting for cryogenic loads, heating recirculating power, and duty cycle losses.

**Missing**: Three genuine physics uncertainties remain unresolved and are acknowledged as such in the paper. First, energy confinement scaling has no experimental basis at fusion-relevant conditions — the paper's approach is explicitly reversed (design to minimize required τe, then back-calculate what a demonstration device must achieve). Second, edge pedestal physics is unknown — the paper assumes I-mode-like conditions (T_lcfs = 790 eV, p_lcfs = 10³ Pa) but states "will be confirmed with future levitated dipole experiments." Third, transport in the good-curvature region (Ψ < Ψ₀) is assumed to be classical but unverified — the paper notes "determining this is out of scope and will be a focus of future experiments." Divertor design is also unaddressed; the paper uses an outboard-limiter configuration as a "test of feasibility" only.

**Gaps**:
- Energy confinement scaling law for dipoles — truly-unknown — blocking (the Qsci=15 target is unvalidatable without this; can only be noted as assumed)
- Edge pedestal physics (magnitude of T_lcfs, p_lcfs) — truly-unknown — important
- Good-curvature region transport — truly-unknown — important
- Divertor design — not-yet-sourced — important (acknowledged in paper as required for final design; referenced papers on diverted dipole equilibria exist but not captured)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**: arXiv 2508.17691 (Junior) and arXiv 2602.20564 document TRL status for major subsystems with reasonable granularity. Junior demonstrated: (1) REBCO NI solder-impregnated coil to 600 A (42% of design), (2) flux pump charging to 95 MJ stored energy — world record for HTS flux pump delivery at time of publication, (3) levitated plasma confinement with He gas, (4) flat-density profiles consistent with supported operation (not yet levitated for plasma experiments). The design paper provides detailed analysis of REBCO tape critical current behavior under neutron irradiation, tungsten shield thermal creep, and FEA stress results for the coil structural overband.

**Missing**: ICRH coupling in dipole magnetic geometry remains experimentally immature — the paper notes RT-1 results were "mixed" and Wallace et al. 2025 is ongoing. The flux pump has only been demonstrated at the Junior scale (170 kJ, ~5.6 T); the power plant requires ~20.8 GJ stored energy and 23 T — this is an enormous gap in stored energy (×100,000). The CICC architecture assumed in the power plant has not been built at any scale; the Junior uses NI pancake coils. Neon slush reservoir on a levitating magnet is an undemonstrated integration. No fusion neutron environment testing of any OpenStar component has occurred.

**TRL Estimates** (based on arXiv 2602.20564 and 2508.17691):

| Subsystem | TRL | Basis |
|-----------|-----|-------|
| REBCO HTS coil (NI pancake, ~5.6 T) | 5 | Junior demonstrated |
| REBCO CICC architecture (23 T, power plant) | 3 | Design only; SPARC analogy cited |
| On-board HTS flux pump | 4 | Junior demonstrated at small scale |
| Neon slush on-board reservoir (levitated) | 2 | Concept; materials properties characterized |
| Levitated plasma confinement | 4 | Junior achieved first plasma; levitation demonstrated Feb 2026 |
| ICRH on dipole plasma | 2 | RT-1 mixed results; RT-1 scale far below reactor |
| W+B4C neutron shielding (geometry) | 3 | OpenMC design study; no fabrication at scale |
| Li2O HCPB blanket | 4 | Well-studied in ITER context; dipole integration novel |
| Energy confinement scaling | 1 | No fusion-relevant experimental data for levitated dipoles |
| Hot-cell magnet replacement system | 1 | Concept described; not designed |

**Gaps**:
- Flux pump scaling from 170 kJ → 20.8 GJ (×120,000) — truly-unknown — important
- CICC architecture for levitated dipole application — not-yet-sourced — important
- ICRH coupling efficiency in dipole magnetic geometry at relevant densities — not-yet-sourced — important
- Confinement scaling to fusion-relevant conditions — truly-unknown — blocking (energy confinement)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**: arXiv 2602.20564 provides complete material inventory for both reactor designs (Table 5). For Reactor A: 4,320 km REBCO tape, 1,760 tonnes tungsten tiles, 82.3 tonnes B4C, 168 tonnes WC, 199 tonnes SS316LN/Cu coil conduit, 351 tonnes SS316LN magnet structure, 3,490 tonnes Li2O blanket, 325 tonnes Inconel 718 inner vessel, 38,700 tonnes reinforced concrete outer vessel. The paper explicitly addresses neon supply ("if neon proves challenging, hydrogen is a viable alternative"), tungsten tile recrystallization behavior above 1600 K, and the 1-year tungsten cooldown before recycling. REBCO tape: the paper references Faraday Factory "Mirai" REBCO at >1000 A/mm² engineering current density as an expected improvement (+30% over current product), indicating awareness of supply chain trajectory.

**Missing**: 4,320 km of REBCO tape is a massive scale-up challenge — current global annual REBCO production is estimated at hundreds of km for the highest-output manufacturers. No supply chain analysis or cost-at-scale estimate for REBCO procurement is published for this concept. Tungsten boride materials (identified as superior to W+B4C) are explicitly noted as "not yet manufactured at scale due to lower technological maturity." Hot cell remote handling systems for annual 2,500-tonne magnet replacements are mentioned conceptually but not designed. The ~38,700-tonne reinforced concrete outer vessel is compared to NASA's Space Power Facility as a size analogy, but no cost estimate is provided.

**Gaps**:
- REBCO tape at 4,320 km scale: supply chain and cost — not-yet-sourced — important (this is the single largest non-concrete cost driver; no published cost-at-scale for this quantity)
- Tungsten boride materials manufacturing at scale — not-yet-sourced — nice-to-have (current design uses W+B4C which avoids this gap, but future designs require it)
- Hot cell and remote handling systems for annual magnet replacement — not-yet-sourced — important
- Neon supply chain at plant scale (6 t/year estimated per reactor) — derivable — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric output (Reactor A) | 208 MW | arXiv 2602.20564, Table 5 | High |
| Net electric output (Reactor B) | 74.5 MW | arXiv 2602.20564, Table 5 | High |
| Fusion power (Reactor A) | 667 MW | arXiv 2602.20564, Table 6 | High |
| Thermal power (Reactor A) | 741 MW | arXiv 2602.20564, Table 9 | High |
| Thermal efficiency (assumed) | 40% | arXiv 2602.20564, Table 2 | Medium (model assumption, not validated) |
| ICRH heating efficiency (assumed) | 70% | arXiv 2602.20564, Table 2 | Medium (cited from ARIES-AT; not demonstrated for dipole) |
| Cryogenic system COP | 1.25% | arXiv 2602.20564, Table 2 | Medium |
| Plant availability factor | ~96% | arXiv 2602.20564, Table 5 | Medium |
| Core magnet duty cycle | 90.1% | arXiv 2602.20564, Table 5 | Medium |
| Auxiliary heating power (Reactor A) | 44.5 MW | arXiv 2602.20564, Table 9 | High |
| Cryogenic power load | 1.31 MW | arXiv 2602.20564, Table 9 | Medium |
| Annual core magnet replacement cycle | 1/year (sacrificial section) | arXiv 2602.20564, §2.3.1 | High |
| REBCO tape quantity (Reactor A) | 4,320 km | arXiv 2602.20564, Table 5 | High |
| Concrete outer vessel mass | 38,700 tonnes | arXiv 2602.20564, Table 5 | High |
| Total reactor mass | 45,100 tonnes | arXiv 2602.20564, Table 5 | High |
| LCOE (D-T MFE tokamak analog) | $140–550/MWh | knowledge/sources/tea_dt_mfe_cost_analysis/ | Low (different architecture) |
| OCC (D-T MFE tokamak analog, NOAK) | $8,800–22,200/kWe | knowledge/sources/tea_dt_mfe_cost_analysis/ | Low (different architecture) |
| LCOE (compact modular fusion, avg) | $43/MWh ($34–54 range) | knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/ | Low (MIF/Z-pinch concepts, not dipole) |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Absolute overnight capital cost (CAS-level) | proprietary | blocking | Paper §3.3 explicitly states: "OpenStar is currently in the process of developing a model… topic of future work. We avoid quoting specific values here." Internal model exists but unpublished. |
| Annual O&M cost | not-yet-sourced | blocking | No O&M analysis published for levitated dipole. Fleet analog from tea_dt_mfe_cost_analysis (CAS 60+ accounts) applicable at ±50% uncertainty. |
| Thermal cycle type (Rankine vs sCO2) | truly-unknown | important | Confirmed absent after re-checking arXiv HTML; paper focuses on nuclear island only. BOP cycle not specified. |
| Balance of plant capital cost (CAS 23–27) | not-yet-sourced | important | Partially addressable: tea_dt_mfe_cost_analysis provides ARC-like tokamak BOP (Rankine cycle turbine plant, electrical equipment, heat rejection) at 350 MWe — applicable analog for CAS 23–27 pending cycle type confirmation. This downgrades from blocking to important. |
| First-wall and blanket replacement schedule/cost | not-yet-sourced | important | 4,020 m² first wall area; large Li2O blanket (3,490 tonnes). Replacement frequency unspecified. |
| Annual core magnet replacement cost | not-yet-sourced | blocking | 2,560-tonne magnet replaced annually; hot cell required. No cost estimate published. REBCO tape cost at scale is key input. |
| Construction time / interest during construction | not-yet-sourced | important | Needed for IDC calculation. Revisit_of_2017_costing uses 3-year construction time for modular fusion; partially applicable. |
| Capacity factor / unplanned availability reduction | derivable | important | 96% stated in design paper but excludes unplanned outages in first commercial units. Standard FOAK derating to 75–85% is common practice but unsupported by data. |
| Fuel cost (D-T supply chain) | derivable | nice-to-have | TBR=1.1 assumed sufficient for self-sufficiency. External tritium startup cost applies. Standard for D-T MFE. |
| Decommissioning cost | not-yet-sourced | nice-to-have | Concrete vessel and activated tungsten. Comparable to fission plant decommissioning for regulatory purposes. |

**Fleet-wide source integration**:

- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Opened and read. Covers NOAK ARAI (ARC-like tokamak, 350 MWe) with OCC $8,800–22,200/kWe and LCOE $140–550/MWh. Uses EEDB COA framework (CAS 21–27 direct, 90+ indirect). The BOP cost structure (CAS 23 turbine-generator, 24 electrical plant, 26 heat rejection, 27 misc) is directly applicable to any D-T MFE plant including the levitated dipole, assuming Rankine cycle — this partial applicability allows the "BOP capital cost" gap to be downgraded from blocking to important. However, the reactor plant equipment cost (CAS 22) — dominated by the levitated dipole's unique core magnet — is not transferable. The LCOE range ($140–550/MWh) serves as a rough order-of-magnitude sanity check only.

- **ARPA-E ALPHA Costing Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened and read. Covers four compact MIF/Z-pinch concepts (~500 MWe average, $43/MWh average LCOE, $2.4/W CapEx). The modular design assumptions (3-year construction, factory manufacturing) are partially analogous to the levitated dipole's expected deployment model. However, the four ALPHA concepts are MIF/Z-pinch and have fundamentally different physics, cost structures, and fuel cycles from the levitated dipole. The LCOE figure ($43/MWh) is useful only as a lower-bound benchmark for compact modular fusion economics and cannot be applied directly to the dipole.

---

## Source Recommendations
- **Annual magnet replacement cost** (blocking gap, proprietary): Search OSTI/arXiv for REBCO tape cost-at-scale studies — specifically "REBCO tape manufacturing cost projection" or "HTS tape learning curve fusion." The SPARC program (Commonwealth Fusion Systems) has published analysis of REBCO tape procurement at scale that may provide cost per meter as a transferable input. `unverified — confirm existence before searching`
- **O&M cost analog** (blocking gap, not-yet-sourced): The ARIES-AT power plant study (referenced in TEA D-T MFE source) includes O&M cost assumptions for a comparable-scale D-T MFE tokamak; applicable as an analog pending blanket/magnet replacement-specific adjustments. Search ARIES-AT final reports on OSTI.
- **Divertor design for levitated dipole** (important gap, not-yet-sourced): Wallace et al. 2025 ("Ion Cyclotron Heating in a Levitated Dipole Fusion Reactor") is cited in arXiv 2602.20564 — this paper may cover edge and scrape-off layer physics relevant to divertor design. `unverified — confirm existence before searching`
- **REBCO tape at scale / supply chain**: Molodyk et al. 2021 ("Development and large volume production of extremely high current density YBa2Cu3O7 superconducting wires for fusion") is cited in arXiv 2602.20564 — it may contain production volume and cost data for REBCO at fusion-relevant scales. `unverified — confirm existence before searching`
- **Thermal cycle type**: No publication is expected to resolve this; balance-of-plant cycle selection is genuinely internal to OpenStar. A reasonable analysis assumption is Rankine steam cycle at 40% (consistent with the paper's thermal efficiency assumption), with sensitivity to sCO2 Brayton at 45–48%.

---

## Summary
**Proceed to full D1+ analysis with noted gaps.** The concept is exceptionally well-documented at the physics and nuclear-engineering layer for a pre-commercial company: two optimized design points, full power balances, neutron transport (OpenMC), and structural mechanics (COMSOL FEA) are all published. Sections 1–4 can be completed at D1+ quality. Section 5 (LCOE) is the weak link: OpenStar deliberately withholds absolute cost data pending finalization of their internal model, the annual core magnet replacement cost is a unique and unquantified cost driver, and the thermal cycle is unspecified. A D1+ LCOE section should present the power balance parameters that are known, apply the D-T MFE TEA source as a BOP analog (with explicit stated assumptions), flag the capital cost as proprietary/not-yet-available, and present the $140–550/MWh tokamak analog range only as a benchmark for comparison rather than as a concept-specific estimate. The two blocking quantitative LCOE gaps (absolute capital cost, O&M) do not prevent a qualitative or partial quantitative analysis.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 2
important_count: 8
counting_method: "deduplicated across all sections; blocking = prevents Section 5 quantitative LCOE completion (capital cost CAS breakdown [proprietary], annual O&M cost [not-yet-sourced]); important = reduces analysis quality but workable with assumptions or analogs (energy confinement scaling, edge pedestal physics, ICRH dipole coupling, flux pump scale-up, REBCO supply chain, thermal cycle, BOP capital cost, first-wall/blanket replacement cost)"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```