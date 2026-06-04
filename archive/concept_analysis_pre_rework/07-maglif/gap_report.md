# Gap Assessment: MagLIF (D-T)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: MagLIF is well-documented at the physics and driver technology level, with Pacific Fusion's 2025 AMPS paper, the 2024 community PMF whitepaper, and the 2006 Z-IFE plant study collectively covering subsystem TRLs, target scaling, engineering challenges, and a preliminary system cost framework. The principal gaps are not data availability per se but commercial-regime unknowns — target cost at scale, capacitor/switch lifetime at rep rate, and a published LCOE study for a commercial power plant (the AMPS paper defers this to subsequent publications). A quantitative LCOE model can be built using Hawker's 14-parameter IFE framework populated with Z-IFE and AMPS data, but key cost parameters will require explicit assumption flags.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- *arXiv:2408.15206* ("Opportunities in Pulsed Magnetic Fusion Energy", Ellison et al. 2024): 84 KB comprehensive PMF review covering driver architecture, MagLIF target physics (χ=0.084 on Z), TRL roadmap, chamber design engineering challenges, and commercialization barriers. Authored by Pacific Fusion, Sandia, LLNL, LANL, and University of Rochester scientists — the authoritative cross-institution assessment.
- *arXiv:2504.10680v1* (Pacific Fusion AMPS paper, 2025): Pacific Fusion's own 246 KB technical paper detailing the DS physics basis, simulated performance (Qf = 1.36–4.75 at 56 MA, yields of 109–380 MJ), facility specs (80 MJ, 60+ MA, 156 modules, 73m × 80m), and engineering path to commercial power (cassette replacement, vacuum operation, tritium breeding discussion). Contains a direct facility cost comparison noting DS is 1/10 the capital of NIF. Explicitly defers detailed technoeconomics to subsequent publications.
- *SAND2006-7148* (Z-IFE Power Plant Final Report FY2006): Full plant study for a 1000 MWe Z-pinch IFE facility including COE vs. chamber rep-rate charts (Figures 3.4–3.6), driver cost model, four thermal cycle analyses, FLiBe blanket characterization, and RTL automation study. Primary source for plant-level LCOE structure.
- *Pacific Fusion founders' letter, breakthrough press releases, CRADA announcements, interview with The Fusion Report*: Confirm D-T fuel, 60+ MA facility scale, cassette-per-shot architecture, Qf>1 target by 2030, first commercial system mid-2030s, $900M+ funding.
- *Fuse Energy Not Boring deep dive*: Detailed TITAN I/II and Z STAR/APEIRON I architecture, business model, capacitor lifetime bottleneck quantified (need ~10× improvement from ~1M to ~10M shots).
- *Fleet-wide — affordable_manageable_practical_and_scalable_amps_high* (`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`): Read in full. Pacific Fusion's 2025 AMPS paper provides physics basis, FLASH simulation benchmarks against Z experiments, DS facility design, and Section 4 "Path to commercial power" covering component lifetime, cassette/chamber design, and tritium breeding concept. Table 1 gives NIF vs. DS performance comparison. This is the single most important source for modern MagLIF commercial viability.
- *Fleet-wide — a_simplified_economic_model_for_inertial_fusion* (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Read. Hawker (2020) 14-parameter technology-agnostic IFE LCOE model directly applicable to MagLIF. Key constraint: competitive LCOE ($25/MWh) requires gain >500 and yield >5 GJ; MagLIF simulates yield 109–380 MJ (AMPS) and Qtarget ~13–45, well below Hawker's optimistic threshold. This framework can anchor the MagLIF LCOE model and flag what commercial targets must be reached. Downgrading "LCOE methodology gap" from blocking to important since the framework exists.

**Missing**:
- Published LCOE/TEA study for a modern commercial MagLIF power plant (AMPS paper defers to subsequent publications)
- Commercial repetition rate (not disclosed by Pacific Fusion or Fuse Energy; Z-IFE baseline is 0.1 Hz)

**Gaps**:
- No published commercial LCOE or TEA for MagLIF power plant — not-yet-sourced — important
- Commercial repetition rate target not disclosed by either company — proprietary — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Target gain scaling: AMPS paper provides FLASH simulation benchmarks vs. HYDRA at Z-scale and current-scaling from 15–65 MA. Similarity-scaled MagLIF predicts ignition at ≥50 MA, Qf>1 at 56 MA in 1D simulations. Self-heating non-linearity (Qtarget ∝ E³) is documented and advantageous vs. laser ICF.
- Energy delivery chain: Full efficiency chain documented in AMPS (stored energy → target: 10%; target → fuel: 12.5% of target energy = 1.25% overall stored-to-fuel), explaining how DS outperforms NIF despite 4× less stored energy.
- Chamber clearing: AMPS Section 4.2 discusses post-shot vacuum impulse response, cassette replacement design, and pumping/reloading. DS is designed for ≥1 shot/day with cassette-per-shot architecture. Cassette assembled offline, cryo layering performed in situ.
- Tritium breeding: AMPS Section 4.3 mentions tritium breeding as a key engineering requirement; no commercial design or TBR analysis disclosed.
- Z-IFE (2006): Covers thick liquid wall FLiBe chamber concept, RTL automation, and shock mitigation as the primary engineering baseline.

**Missing**:
- 2D/3D target performance: Published results are conservative 1D FLASH simulations. Real implosion degradation from Rayleigh-Taylor instability, mix, and asymmetry could suppress gain by 2–10× vs. 1D. AMPS notes this is "an ongoing area of development" (HYDRA vs. FLASH divergence at high current).
- Cassette/inner-MITL cost and replacement throughput at commercial rates: AMPS designs for ≥1 shot/day on DS; commercial requires ~1 Hz (86,400 shots/day). Cost per cassette and replacement logistics at that rate are entirely uncharacterized.
- Plasma energy recirculation fraction: No commercial plant analysis gives the wall-plug efficiency or recirculating power fraction.

**Gaps**:
- Target gain degradation from 1D to 2D/3D at commercial conditions — derivable (with high uncertainty from scaling degradation factors) — blocking
- Cassette/inner-MITL cost and replacement logistics at commercial rep rates (~1 Hz) — truly unknown — blocking
- Commercial wall-plug efficiency and recirculating power fraction — derivable from Z-IFE analog but not for modern architecture — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- *Pulsed power driver (IMG architecture)*: TRL 4–5. TITAN I demonstrated (0.8 MA, 1 TW, 100+ consecutive shots, $7.1M to build). DS (60+ MA, 80 MJ) under construction. arXiv:2408.15206 quantifies IMG advantages: 90% energy efficiency vs. ~50% for conventional pulsers, 2× reduction in physical area, lower-voltage switches (200 kV vs. 6 MV), factor ~14 lower coulomb transfer per switch. Commercial targets: must decrease energy storage/switch cost by 5–10× and increase lifetime by 1000× at Hertz rep rates.
- *MagLIF target physics (Z-scale)*: TRL 3–4. χ = 0.084 ± 0.009 demonstrated on Z (current best). Conservative similarity scaling (χ ∝ I³) projects χ ~2.4 and ~60 MJ yield at 60 MA. AMPS paper validates FLASH against Z experiments including shot 2977.
- *Self-magnetizing targets*: TRL 3. Feb 2026 breakthrough: 4 shots on Z at 22 MA, 120 ns, demonstrated magnetic field penetration with composite Al/plastic liner, eliminating need for external Helmholtz coils. Laser preheat elimination is next experimental objective.
- *Rep-rate pulsed power*: TRL 2–3. TITAN I demonstrated 100+ consecutive shots; Fuse Energy FAETON fires 50+ shots/day at sub-fusion current. No demonstrated rep-rate fusion at ≥10 MA.
- *Balance of plant / thermal cycle*: TRL 3. Z-IFE evaluated supercritical CO₂ Brayton, steam Rankine, gas Brayton, and combined Brayton-Rankine (recommended as highest efficiency). Combined cycle efficiency ~40–50% at high temperature with advanced materials.
- *Cassette/target injection and replacement*: TRL 3 (DS-scale). AMPS describes offline cassette assembly, in-situ cryo layering, and ≥1 shot/day capability. Commercial rate undemonstrated.

**Missing**:
- Commercial blanket/chamber design: Neither Pacific Fusion nor Fuse Energy has published a commercial power plant blanket architecture. Z-IFE FLiBe thick-liquid-wall concept remains the only engineering study (2006, no modern follow-on).
- Tritium breeding design and TBR: Z-IFE points to FLiBe, AMPS acknowledges the need — no TBR calculation published for modern MagLIF geometry.
- Diagnostics and control at commercial rep rate: AMPS discusses the diagnostic suite for DS (one shot at a time); commercial rep-rate instrumentation not addressed.

**Gaps**:
- Commercial chamber/blanket design (no modern engineering study since Z-IFE 2006) — not-yet-sourced — blocking
- Capacitor and switch commercial lifetime at rep rate (1000× improvement required per arXiv:2408.15206) — truly unknown — blocking
- Tritium breeding design and TBR for modern liner/pulsed geometry — not-yet-sourced — important
- Target fabrication throughput and per-shot cost at commercial scale — not-yet-sourced — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- *Capacitors and spark gap switches*: The identified primary commercial bottleneck. arXiv:2408.15206 states: "energy storage and switching component replacement lifespan must extend by at least a factor of 1000 at Hertz operating rate. The cost of energy storage and switching must decrease by a factor of 5 to 10." Fuse Energy quantifies this: need ~10M shot lifetime vs current ~1M. Mass-manufacturing path exists (Gigafactory/Terafactory concept) but not yet demonstrated.
- *Target materials*: Simple commodity materials — aluminum, plastic composite, potentially beryllium for liner or DT ice for fuel layer. No exotic rare-earth or constrained supply materials. AMPS Feb 2026 targets: 50 µm and 200 µm aluminum layer bonded to plastic insulator. Orders-of-magnitude simpler than NIF cryogenic hohlraum targets.
- *Structural materials*: F82H RAFM steel identified in Z-IFE as baseline chamber material. Hastelloy studied as alternative. F82H irradiation data available; commercially available. No HTS magnets required (no REBCO tape supply concern).
- *Tritium*: Standard D-T constraint — limited production (~20 kg/year global, largely from CANDU reactors). Startup inventory needs TBR >~1.05 for self-sufficiency. Shared bottleneck with all D-T fusion.
- *Recyclable Transmission Lines (RTL)*: Z-IFE concept uses solid FLiBe RTL (recyclable), providing both electrical transmission and partial neutron shielding. Characterization of FLiBe/steel interaction documented in SAND2006-7148. Pacific Fusion uses water-insulated transmission lines (DS design) — different architecture.
- *No superconducting magnets*: Eliminates REBCO/HTS tape supply chain concern.

**Missing**:
- FLiBe supply chain for power plant scale: FLiBe requires enriched Li-6 and beryllium (limited global supply, toxic). If FLiBe is the commercial blanket choice, a supply chain does not exist for fusion-scale quantities.
- Capacitor and switch supply chain for mass manufacturing: The Terafactory concept is Fuse Energy's long-term plan; no mass-manufacturing supply chain exists today for high-voltage, high-rep-rate fusion-grade capacitors.

**Gaps**:
- FLiBe supply chain (Li-6 enrichment, Be availability) if adopted as blanket material — not-yet-sourced — important
- High-rep-rate fusion-grade capacitor supply chain for mass manufacturing — not-yet-sourced — important

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Driver stored energy | 80 MJ (DS) | AMPS paper (arXiv:2504.10680), §3.1 | high |
| Stored-to-fuel coupling efficiency | ~1.25% (DS: 80 MJ stored → 1 MJ fuel internal energy) | AMPS paper, §2.3 | high |
| Target gain Qtarget (simulated) | 13–45 at 56 MA (1D FLASH, DT ice liner) | AMPS Table 1 | medium |
| Target gain Qf (facility, simulated) | 1.36–4.75 at 56 MA | AMPS Table 1 | medium |
| Target yield per shot (simulated) | 109–380 MJ at 56 MA | AMPS Table 1 | medium |
| Driver efficiency (IMG) | ~90% stored → electrical pulse | arXiv:2408.15206, §3.2 | high |
| Fusion energy split | ~80% neutrons, ~20% alphas | arXiv:2408.15206, §7.1 | high |
| Thermal cycle efficiency | ~40–50% (combined Brayton-Rankine) | Z-IFE SAND2006-7148, §3.2 | medium |
| Rep rate (Z-IFE baseline) | 0.1 Hz | Z-IFE SAND2006-7148, Figure 3.4 | medium |
| Plant scale (Z-IFE baseline) | 1000 MWe | Z-IFE SAND2006-7148, §3.1 | low (2006 reference) |
| DS facility footprint | 73m × 80m | AMPS §3.1, Fusion Report interview | high |
| DS modules and energy storage | 156 modules, 80 MJ, 800 J/capacitor | AMPS §3.2, Fusion Report interview | high |
| COE vs. rep rate relationship | COE decreases with higher rep rate; 1–3 chambers optimal over 10 | Z-IFE Figures 3.4–3.6 | medium (2006) |
| Capacity factor | Not yet published | — | — |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Commercial plant capital cost (overnight) | proprietary | blocking | AMPS defers to "subsequent papers"; DS cost is demonstration-scale, not power-plant-scale. Z-IFE LTD driver cost is 2006 architecture, outdated by IMG design. Use Hawker's parameterized driver cost model as proxy. |
| Target/cassette cost per shot at commercial rep rate | proprietary / truly-unknown | blocking | Inner MITL + target assembly + cassette replacement cost. Critical LCOE lever for any IFE concept. No estimate published anywhere for modern MagLIF architecture. |
| Capacity factor / availability | derivable (high uncertainty) | blocking | Depends on capacitor/switch lifetime at rep rate (currently ~1M shots, need ~10M), and cassette replacement time. Cannot estimate without resolving lifetime gap. |
| Commercial plant repetition rate | proprietary | important | Range: 0.1 Hz (Z-IFE baseline) to ~1 Hz (Pacific Fusion "piston engine" aspiration). Defines whether one chamber achieves baseload power. |
| Commercial plant net electrical output | derivable | important | No commercial plant design published. Derivable from yield × rep rate × thermal efficiency × capacity factor, but all have high uncertainty. |
| O&M costs (annual) | not-yet-sourced | important | No published estimate. Capacitor replacement and target fabrication are likely dominant O&M components. |
| Blanket/tritium breeding capital cost | not-yet-sourced | important | No commercial design; Z-IFE FLiBe blanket concept is the baseline. |

---

## Source Recommendations

- *Subsequent Pacific Fusion LCOE paper*: AMPS paper explicitly states "elaborate on technoeconomics in subsequent papers." Monitor arXiv (Pacific Fusion authors) for a follow-on TEA/LCOE publication — this would directly resolve the blocking capital cost and target cost gaps. `not-yet-sourced`

- *OSTI / Sandia Z-IFE follow-on reports*: Search OSTI for Z-IFE reports post-2006 (SAND2007–SAND2012 range) for updated driver cost models, RTL automation studies, or thermal cycle refinements. The SAND2006-7148 roadmap describes follow-on ZN facility experiments as the next planned phase. `not-yet-sourced — confirm existence before searching`

- *arXiv papers on MagLIF scaling to high current*: The AMPS paper references Ruiz et al. (Ref [28]) "similarity scaling study" and HYDRA-based gain curves at 15–60 MA. This published study (likely Ref: Ruiz et al. 2023/2024, Phys. Plasmas) should be sourced to validate the 1D vs. 2D/3D gain degradation. `not-yet-sourced`

- *IFE target cost literature*: For target/cassette cost at scale, search for published analyses of target cost for pulsed-power IFE vs. laser ICF. The Z-IFE program studied RTL remanufacturing cost; IFE target cost studies (e.g., from LLNL's LIFE study) may provide order-of-magnitude analogs. `not-yet-sourced — confirm existence before searching`

- *Fleet-wide — revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts* (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): **Read executive summary.** Reports average LCOE of 43 $/MWh ($34–54 range) for ~500 MWe modular fusion plants using CAS framework. The four ALPHA program concepts are unnamed in the executive summary; one may be MIFTI (a Z-pinch MIF concept) per acknowledgment of "Samuel Langendorf" as POC, who has Sandia/pulsed-power affiliation. Without confirming the four concepts, cannot determine direct applicability to MagLIF. As a CAS framework and modular plant cost analog, the 43 $/MWh figure and ~$2.4/W CapEx are useful benchmarks for a first-pass LCOE model.

- *Fleet-wide — progress_toward_fusion_breakeven_lawson_criterion* (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): **Disqualified for separate reading.** The AMPS paper (arXiv:2504.10680) incorporates and extends the Wurzel & Hsu (2021) Lawson criterion compilation, which this source represents. All relevant data (MagLIF Pτ performance, comparison to laser ICF and tokamaks) is already present in the AMPS paper read above. Reading the original would add no new MagLIF-specific data.

- *Fleet-wide — tea_dt_mfe_cost_analysis* (`knowledge/sources/tea_dt_mfe_cost_analysis/`): **Disqualified.** MFE-specific TEA focused on tokamak/steady-state economics. MagLIF uses pulsed driver architecture with fundamentally different cost structure (no superconducting magnets, target-dominated operating costs). CAS accounts differ significantly; this source does not address any current gap for pulsed IFE economics.

---

## Summary

Proceed to full analysis. MagLIF has unusually rich physics documentation for a private fusion concept at this stage, anchored by Pacific Fusion's AMPS paper (2025), the Sandia-led community PMF whitepaper (2024), and the Z-IFE power plant study (2006). A D1+ qualitative analysis can be written now at high confidence. A quantitative LCOE model can be built using Hawker's 14-parameter IFE framework with Z-IFE as the plant-level analog, AMPS for driver efficiency and gain parameters, and explicit assumption flags on target cost per shot, commercial rep rate, and capital cost — the three most consequential unknowns. The 2D/3D gain degradation relative to 1D simulations is the most consequential physics uncertainty for commercial viability; the AMPS paper acknowledges ongoing HYDRA vs. FLASH divergence at high current as an open area of development. The 1 c/kWh back-solve will likely reveal that commercial MagLIF requires significantly higher yield per shot (GJ-class), higher rep rate (≥0.1 Hz), and much lower target cost (<<$1,000/shot) than any currently published data can confirm.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 6
important_count: 8
counting_method: "all_sections_deduplicated — six unique blocking gaps: (1) target gain degradation 2D/3D, (2) cassette/RTL cost and throughput at commercial rep rate, (3) capacitor/switch commercial lifetime, (4) commercial chamber/blanket design, (5) commercial plant capital cost, (6) target cost per shot; eight unique important gaps: (1) no published LCOE/TEA, (2) commercial rep rate undisclosed, (3) tritium breeding design and TBR, (4) target fabrication commercial scale, (5) plasma recirculating power fraction, (6) FLiBe supply chain, (7) capacity factor/availability, (8) O&M costs"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```