# Gap Assessment: FRC w/ Direct Conversion (D-He3)

## Overall Readiness
**Rating**: Mostly Ready
**Summary**: Helion Energy is among the most publicly documented private fusion companies, and the physics, technology architecture, and milestone history are well-supported by multiple independent sources. However, virtually all commercial-scale cost data (capital costs by subsystem, O&M, capacity factor, plant-level power balance) is proprietary, and two critical technical milestones remain undemonstrated as of the available sources: net electricity production and D-He3 operation at the required ~200M°C. Qualitative sections 1–3 can be written at high quality; sections 4–5 will require explicit analogue assumptions and gap acknowledgments.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**: Helion has published more technical detail than almost any other private fusion company, across first-party website articles, peer-reviewed papers (Slough et al. *Nuclear Fusion* 51(5) 2011; Kirtley & Milroy *J. Fusion Energy* 2023), ARPA-E presentations (DocsLib ARPA-E presentation: 20T/40T specs, 2 Hz @ 50 MW design point), a detailed third-party research report (Contrary Research), and ongoing press coverage of milestone events. Seven prototype generations are documented. Polaris's Feb 2026 D-T milestone at 150M°C (13 keV) is independently confirmed by DOE/FES and Ryan McBride (Sandia/University of Michigan). Funding history ($500M Series E, $425M Series F, $5.4B valuation), power purchase agreements (50 MWe for Microsoft, 2028; 500 MWe Nucor 2030), and Orion construction (groundbreaking July 2025, Malaga, WA) are confirmed.

**Missing**: No published plant study (ARIES-equivalent), no peer-reviewed capital cost analysis, no independent techno-economic assessment. Orion specifications are entirely proprietary.

**Gaps**:
- Published plant study / design document for Orion — proprietary — important
- Independent peer-reviewed cost or TEA study — not-yet-sourced — important
- Achieved Polaris repetition rate — proprietary (milestone announcement did not disclose rep rate) — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Good

**Available**: The system function is documented in sufficient qualitative depth across multiple public sources. The RLC circuit analogy is confirmed by CEO Kirtley. The four-phase cycle (FRC formation → acceleration to >300 km/s → collision-compression → inductive energy recovery) is described in the ARPA-E presentation and peer-reviewed IPA papers. Direct inductive energy recovery via Faraday's law is documented with the key constraint: >95% of input energy must be recovered per pulse for net electricity. Energy recovery >95% demonstrated at subscale (>1 million pulses, Grande prototype). The non-ignition economics rationale (high-efficiency energy recovery relaxes the gain requirement) is described in the Helion article "How to Make Fusion Electricity Without Ignition," consistent with the Lawson criterion framework in Wurzel & Hsu (2021) (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) which explicitly addresses pulsed systems where η fraction of plasma energy is recovered.

**Modeling challenges** (not gaps in source availability, but inherent to the concept):
- The system is an electrical circuit, not a thermal-mechanical system — standard power plant LCOE models (steam cycle → turbine → generator) do not apply at all. The absence of a thermal cycle is the defining structural difference from all other fusion concepts in this analysis.
- The achievable net gain (Q_eng) is a function of both plasma gain and round-trip energy recovery efficiency — the two must be analyzed together, not sequentially.
- He3 self-breeding inventory dynamics: tritium (t½=12.3 yr) accumulates in the system, decaying to He3 at 5.5%/year. Full self-sufficiency is a multi-decade process. Startup requires a stock of He3 or a plan to operate D-D or D-T at reduced economics initially.
- The pulsed operation mode creates fatigue loading on all structural components — chamber, coils, capacitors — at a rate and severity with no comparable industrial precedent.

**Gaps**:
- Q factor / scientific gain (Q_sci or Q_eng) achieved on any prototype — proprietary (never disclosed) — blocking
- Round-trip energy recovery efficiency at Polaris scale — proprietary — important
- He3 startup inventory quantity and sourcing plan — derivable (physics-based estimate possible) — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **FRC formation and acceleration** (sequential field reversal, >300 km/s): TRL 5–6; demonstrated across 7 prototype generations, confirmed at Polaris scale with largest FRCs ever produced by Helion. Heritage traces to MSNW/UW IPA experiments 2005–2012.
- **Magnetic compression to fusion conditions**: TRL 5–6; 40 T reactor target vs. 15 T+ demonstrated on Polaris. The 40 T requirement is the same as the ARPA-E experiment target (MITRE/JASON 2018 assessment flagged this as the primary challenge).
- **Pulsed EM coils (Al, no superconductors)**: TRL 6–7; proven materials and manufacturing; Polaris coils operational.
- **Capacitor bank (>50 MJ, tens of kV)**: TRL 5–6; Polaris bank demonstrated; partly manufactured in-house.
- **Direct inductive energy recovery (IGBTs)**: TRL 5–6; >95% round-trip efficiency demonstrated for >1 million pulses at smaller scale (Grande, 2015); Polaris-scale demonstration in progress.
- **Shielding (borated polyethylene + borated concrete)**: TRL 8–9; standard materials used in medical particle beam facilities; approximately 1-meter solid barrier confirmed.
- **Regulatory**: Washington State HB 1018 (2025) classifies fusion as clean energy, enabling local permitting. Washington State DOH Large Broad Scope tritium license granted (Aug 2024). Permitting for Orion site underway.

**Poorly documented**:
- Repetition rate scale-up: Trenta operated at ~1 pulse/10 min; Polaris targets 1 Hz — a ~600× step in rep rate. No intermediate milestones published.
- Chamber / first wall lifetime under pulsed loading: not discussed in any public source.
- Vacuum system and neutral gas management: not described for commercial scale.
- He3 separation and fuel handling hardware: not documented publicly.
- IGBT switching hardware at commercial power levels: not documented.

**Gaps**:
- Achieved repetition rate on Polaris — proprietary — blocking (determines power output and economics)
- D-He3 operation at ~200M°C — not yet demonstrated (Polaris still demonstrating D-T at 150M°C as of Feb 2026) — blocking (commercial fuel cycle unvalidated)
- Net electricity demonstration on Polaris — not yet achieved (originally promised 2024, pushed to "during Polaris campaign") — blocking
- Chamber / first wall lifetime and replacement schedule — proprietary — important
- He3 separation and fuel handling TRL — not-yet-sourced — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**: Contrary Research identifies Helion's supply chain as the "main potential risk." Some materials are confirmed:
- **Coil material**: Aluminum (not superconductors); standard industrial supply
- **Cable materials**: Copper, aluminum, custom alloys (~720 miles total in Polaris per website)
- **Quartz tubes**: Manufactured in-house by Helion
- **High-voltage capacitors**: Partly in-house, partly purchased
- **High-voltage IGBTs**: Commercial semiconductor components; no specific manufacturer named
- **Shielding**: Borated polyethylene and borated concrete — established supply chains (medical accelerator industry)
- **Deuterium**: From water electrolysis; essentially unlimited at cost of ~$1–3/g; no supply constraint
- **Helium-3**: Self-bred from DD side reactions; requires no external supply at commercial steady-state; startup requires either accumulated tritium/He3 from D-D campaigns or external purchase

**Missing**: No published bill of materials for commercial plant. The scale-up from >50 MJ prototype capacitor bank to a commercial power plant is undefined. There is no published analysis of capacitor bank lifetime, replacement rate, or supply chain.

**Gaps**:
- Commercial-scale capacitor bank specifications and supply chain — proprietary — important
- High-voltage IGBT supply chain and replacement schedule — not-yet-sourced — important
- He3 startup inventory strategy (quantity, cost, sourcing prior to self-bred sufficiency) — derivable — important
- First wall / plasma-facing material specification — proprietary — important
- Coil fabrication and replacement schedule at commercial rep rate — proprietary — important
- Critical mineral dependencies — not-yet-sourced — nice-to-have (Al/Cu supply chains are commodity; no REEs or superconductors, which is an explicit advantage)

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| First commercial plant output | 50 MWe | Contrary Research / Wikipedia (Microsoft PPA) | H |
| Second plant output | 500 MWe | Wikipedia (Nucor agreement) | H |
| Repetition rate (target) | ~1–2 Hz | ARPA-E presentation / website | H |
| Capacitor bank size (prototype) | >50 MJ | Helion website (Polaris) | H |
| Direct energy recovery efficiency (claimed) | 85–95% | Contrary Research / Helion website | M |
| Energy recovery (subscale demonstrated) | >95% round-trip | Helion website (Grande, 1M+ pulses) | M |
| Reactor compression field (commercial target) | 40 T | ARPA-E presentation | H |
| Reactor compression field (Polaris) | 15 T+ | Helion website | H |
| D-He3 energy per reaction | 18.3 MeV (3.6 α + 14.7 p) | Helion website | H |
| Neutron energy fraction (D-He3, claimed) | ~5% | Helion website | M |
| Fuel input | Deuterium only (from water) | Helion website | H |
| No steam cycle / no turbines | Confirmed | Multiple sources | H |
| No superconducting magnets | Confirmed (Al coils) | Contrary Research | H |
| No tritium breeding blanket | Confirmed (self-bred He3) | Helion website | H |
| Orion construction start | July 2025, Malaga WA | Wikipedia / Reuters | H |
| Orion target delivery | 2028 (Microsoft) | Wikipedia | H |
| LCOE target (aspirational, unverified) | 1–6 ¢/kWh | Thunder Said Energy | L |
| CAS analogue: structures/site (MIF, 500 MWe) | $174–370M | ARPA-E ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | L (different concepts, different scale) |
| CAS analogue: electric plant equipment (MIF, 500 MWe) | $44–93M | ARPA-E ALPHA re-costing (same source) | L |
| CAS analogue: total LCOE range (MIF, 500 MWe) | $34–54/MWh | ARPA-E ALPHA re-costing (same source) | L (thermally-coupled MIF concepts, not direct conversion) |

**ARPA-E ALPHA costing integration note**: The ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers Plasma-Jet MIF (LANL/HyperJet), Stabilized Liner Compressor (CFS Inc.), Staged Z-Pinch (MIFTI), and Flow-stabilized Z-Pinch (Zap Energy) — none of which use direct inductive energy conversion. Helion is not among the four. CAS accounts that involve a steam/thermal cycle — turbine plant ($101–217M), main heat transfer ($63–184M) — do not apply to Helion. Accounts for structures/site, electric plant equipment, misc, and heat rejection (significantly reduced without steam cycle) provide lower-bound analogues only. Power supplies (22.1.7): $11.9–140.4M average $55.8M in the ALPHA study — Helion's capacitor bank is the dominant unique subsystem and would likely fall in or above this range at commercial scale, but the ALPHA concepts do not use large capacitor banks as the primary power conversion path. This source is useful for CAS framework methodology and BOP structure analogues, but does not resolve any blocking LCOE gaps.

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by CAS subsystem | proprietary | blocking | Orion specs proprietary; no published plant study |
| O&M cost (maintenance, replacement schedules) | proprietary | blocking | No published operations data |
| Capacity factor / availability target | proprietary | blocking | No published RAMI analysis; rep rate not yet demonstrated at commercial scale |
| Q factor / scientific/engineering gain | proprietary | blocking | Key for net electricity calculation; never publicly disclosed |
| Commercial repetition rate achieved | proprietary | blocking | Polaris rep rate not disclosed in milestone announcement |
| Capacitor bank cost at commercial scale | proprietary | important | Helion's largest unique cost driver; no published data |
| Direct conversion system capital cost | proprietary | important | Novel system, no published cost model anywhere in literature |
| He3 startup fuel inventory cost | derivable | important | Can be estimated from DD reaction fraction, tritium decay rate, and initial plasma conditions |
| First wall / liner replacement schedule and cost | proprietary | important | Pulsed fatigue loading; no public data |
| Plant construction cost (civil, modular) | not-yet-sourced | important | Modular factory-manufactured design; analogue from ALPHA costing exists but is for different plant scale (500 vs. 50 MWe) |
| Net plant efficiency (wall-plug to wire) | not-yet-sourced | important | Derivable if Q and η_recovery are known; both are unknown |

---

## Source Recommendations

- **ARPA-E ALPHA re-costing (Woodruff Scientific 2020)** — Integrated above. Covers four MIF concepts, none of which is Helion. Provides CAS structure analogues for structures, BOP, and electric plant equipment. Explicitly does not cover direct inductive conversion or large capacitor banks. Gap type: the ALPHA costing does not resolve any blocking gaps for this concept because the cost architecture differs fundamentally; it is useful only as a lower-bound structural analogue for non-power-conversion cost accounts.

- **Wurzel & Hsu (2021), Lawson criterion paper** — Integrated above. Provides FRC methodology for inferring triple products and peaking values (T₀/⟨T⟩=1.0, n₀/⟨n⟩=1.3 for FRC per Table V). Confirms FRC as a recognized MCF approach within the pulsed MIF category. Helion-specific data is not included (paper predates Trenta publication). Does not resolve any blocking LCOE gaps but supports TRL/physics analysis in sections 2–3.

- **Simplified IFE economic model (Hawker 2020)** — Disqualified. This paper addresses IFE (specifically laser-driver and related pulsed systems) with a 14-parameter Monte Carlo LCOE model centered on target gain, rep rate, and driver cost. Helion does not use targets, does not use a laser/HI driver, and does not use a steam cycle — the three foundational assumptions of the IFE model. The model cannot be applied to Helion's direct inductive conversion architecture without reconstruction from first principles.

- **Helion ARPA-E ALPHA contract publications** (search ARPA-E ALPHA project archive for "Staged Magnetic Compression of FRC Targets" DE-AR0000393): Helion's own ALPHA contract may have produced public progress reports with quantitative plasma parameters. `not-yet-sourced` — search ARPA-E.energy.gov project pages and OSTI for final reports. `unverified — confirm existence before searching`.

- **Kirtley & Milroy (2023) FRC scaling paper** (J. Fusion Energy, doi:10.1007/s10894-023-00367-7) and its 2026 Comment (doi:10.1007/s10894-026-00554-2): Both cited in the dossier but not extracted as sources. These likely contain quantitative scaling analysis for FRC compression and heating that would support the system-function and TRL sections. `not-yet-sourced`. Priority: ingest via Zotero.

- **MITRE/JASON 2018 report** ("Prospects for Low Cost Fusion Development," JSR-18-Task-011): Cited in Wikipedia on Helion and publicly available (ARPA-E website). Evaluated all ALPHA concepts including Helion. Flagged "whether they can simultaneously achieve sufficiently high compression while maintaining plasma stability" as the primary Helion challenge. Contains independent quantitative assessment. `not-yet-sourced`. Priority: ingest via Zotero.

- **Slough et al. (2011) Nuclear Fusion** (doi:10.1088/0029-5515/51/5/053008): Cited in dossier but not extracted as a source. Contains quantitative FRC plasma parameter data from IPA experiments (300 km/s velocities, 2 keV D-D ion temperatures) providing the heritage physics baseline. `not-yet-sourced`. Priority: ingest.

- **GeekWire articles on Polaris tour (2025) and manufacturing at scale (2025)**: Cited in dossier and describe subsystem architecture in accessible language. The manufacturing article reportedly discusses supply chain risks. These are brief journalism pieces but may add qualitative TRL detail for section 3. `not-yet-sourced` (URLs in dossier).

---

## Summary

**Proceed to full qualitative analysis now.** The physics and technology architecture sections (1–3) can be completed at high quality with the existing sources. Section 4 (materials/supply chain) will be thin but can document what is known (aluminum coils, in-house quartz tubes, capacitors, cable materials) alongside explicit gap acknowledgments. Section 5 (LCOE) cannot produce a quantitative model from public sources: capital costs, O&M, capacity factor, and Q factor are all proprietary. The correct approach is to document the structural cost differentiators (no steam cycle, no superconductors, no tritium blanket = significant cost reductions vs. standard MFE), identify the unique cost drivers (capacitor bank, direct conversion hardware, pulsed fatigue maintenance), and use the ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) for non-power-conversion BOP analogues while noting their limitations.

Before detailed LCOE modeling, ingesting the Kirtley & Milroy (2023) scaling paper and the MITRE/JASON 2018 report would most materially improve the analysis. The Kirtley & Milroy paper may contain Q estimates or scaling projections; the JASON report provides an independent expert evaluation of achievability.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 6
important_count: 6
counting_method: "deduplicated_across_all_sections — six blocking gaps: (1) Q factor/gain never disclosed, (2) commercial repetition rate not demonstrated or disclosed, (3) net electricity not yet demonstrated on Polaris, (4) D-He3 operation at 200M°C not yet demonstrated, (5) capital costs by CAS subsystem proprietary, (6) O&M costs proprietary; six important gaps: (1) capacity factor/availability not published, (2) capacitor bank commercial-scale cost, (3) direct conversion system cost, (4) He3 startup inventory, (5) first wall/liner replacement schedule, (6) plant civil construction cost at 50 MWe scale"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Good"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```