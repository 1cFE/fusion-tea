# Gap Assessment: Magnetized Target Fusion - Pneumatic Compression (D-T)

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: General Fusion has been moderately transparent about its technology, and the combination of company sources, the peer-reviewed FST 2025 tritium fuel cycle paper (SRNL), and the Wikipedia article provides solid coverage of concept function, subsystem architecture, and known engineering challenges. However, no published cost study or plant-level economic analysis exists for this concept, and several key commercial-scale engineering challenges (1 Hz vacuum re-establishment, pneumatic compression at 4 m scale, recirculating power fraction) remain undemonstrated or unpublished. A qualitative D1+ analysis can proceed, but the LCOE section will require explicit placeholders with stated derivation assumptions rather than source-backed values.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**: Company sources (generalfusion.com technology and commercialization pages) provide a clear operational concept description — liquid metal liner, pneumatic pistons, ~4 m cavity, 1 Hz rep rate, 300 MWe from two 150 MWe modules, steam Rankine energy capture. The FST 2025 paper (SRNL/General Fusion, Fusion Science and Technology, DOI: 10.1080/15361055.2025.2526266) is the most substantive peer-reviewed source, covering tritium fuel cycle in detail for both LLE and pure Li blanket candidates. The IAEA FEC 2025 abstract and GlobeNewswire 2022 press release confirm plasma performance milestones (>10 ms confinement, >400 eV, compression time ~5 ms). The Wikipedia article documents the full R&D history, challenge list, funding (~$430M+), and cancelled UK Fusion Demonstration Program ($400M, 70% scale). Research collaboration partnerships are also documented: Kyoto Fusioneering (fuel cycle/liquid metal systems), Hatch (BOP engineering), CNL (plant integration studies).

**Missing**: No published cost study or plant-level economic analysis. No detailed specifications for commercial-scale piston hardware (materials, count, stroke, synchronization tolerances at 4 m scale). The cancelled UK Fusion Demo Program would have contained the most engineering-complete plant design, but its detailed specifications were not published.

**Gaps**:
- No published LCOE, capital cost, or plant study for GF MTF — proprietary — blocking
- Commercial plant engineering specifications (piston count at 4 m scale, valve/seal design, BOP integration) — proprietary — important
- Status and final design outputs of the cancelled UK Fusion Demo Program (70% scale, $400M) — not-yet-sourced — nice-to-have

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**: The operational cycle is well described: plasma injection via Marshall gun → pneumatic piston compression of liquid metal vortex → fusion burn (~1 ms timescale) → neutron energy capture in liquid metal → heat exchanger → steam turbine. The Wikipedia article explicitly lists the known engineering challenges acknowledged by the company's own CSO: liquid metal vaporization, plasma contamination by liquid metal impurities, implosion symmetry, kink instability of the liquid metal shaft, and flux diffusion in the liquid metal. A critical unresolved challenge also noted is re-establishing high-vacuum conditions in the time interval between pulses (< 1 second at commercial rep rate) — this is flagged as the most significant unresolved engineering obstacle for the commercial concept. GlobeNewswire 2022 confirms 5 ms compression time in prototype and 10 ms plasma confinement (sufficient margin). LM26 data (April 2025) shows integrated plasma compression with lithium liner was achieved, but using electromagnetic (not pneumatic) compression of solid (not liquid) lithium — a significant gap relative to the commercial concept.

**Missing**: Net energy balance and recirculating power fraction (the pistons are steam-driven, partially self-powering, but the fraction of plant output consumed by compression drivers is not published). Scientific gain (Q_sci) projections for the commercial operating point are not public. Integrated liquid metal vortex + plasma compression with pneumatic pistons has not been demonstrated at any scale.

**Gaps**:
- 1 Hz vacuum re-establishment between pulses not solved; no published approach — truly-unknown / proprietary — blocking
- Integrated liquid metal vortex compression with magnetized plasma not demonstrated (LM26 uses solid Li/EM compression) — truly-unknown (developmental gap) — blocking for cost model anchoring
- Recirculating power fraction (piston steam consumption as fraction of gross output) — proprietary — blocking
- Q_sci projections for commercial operating point — proprietary/not-yet-sourced — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Plasma injector (Marshall gun / PI3)**: TRL ~5-6 — demonstrated at 50% commercial scale; PI3 achieved >10 ms confinement, >400 eV, density ~6×10^19 m^-3 without active stabilization or auxiliary heating; published in *Nuclear Fusion* (peer-reviewed).
- **Electromagnetic compression / solid lithium liner (LM26 proxy)**: TRL ~4 — LM26 first integrated plasma compression with solid lithium liner in April 2025; electromagnetic proxy for commercial pneumatic system.
- **Liquid metal cavity compression (water proxy, 1:10 scale)**: TRL ~4 — 1,000+ shots on water cavity prototype validating symmetry and shape sufficient for fusion conditions when scaled; peer-reviewed results.
- **Power conversion (steam Rankine)**: TRL ~8-9 — fully mature technology; liquid metal heat exchanger coupling is standard.
- **Tritium processing**: TRL ~3-4 — detailed ASPEN Plus models developed by SRNL (FST 2025) for both LLE and Li blanket options, with startup inventories of 317 g (LLE) and ~847 g (Li); no demonstration facility.
- **Liquid metal handling/pumping**: TRL ~5 — actively developed with Kyoto Fusioneering; no published performance data at commercial scale.

**Missing**: No formal TRL assessment by subsystem published. Commercial-scale pneumatic piston system (4 m cavity, 1 Hz, 100+ pistons) has not been built or tested. Seal and valve performance at 1 Hz pulsed liquid metal environment undemonstrated. The commercialization program (mid-2028 per roadmap) plans to demonstrate these, but no data exists yet.

**Gaps**:
- Formal TRL assessment for commercial-scale subsystems not published — not-yet-sourced/proprietary — important
- Commercial-scale pneumatic piston array (~4 m, 1 Hz, synchronized within 10 μs) — truly-unknown (not yet built) — blocking for TRL section
- Piston-chamber seals and valves in pulsed liquid metal environment — truly-unknown — important
- Tritium processing at relevant throughput scale — not-yet-sourced — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**: Liquid metal wall material candidates are well documented: lead-lithium eutectic (LLE, Pb-15.8 Li) or pure lithium (Li). FST 2025 paper (SRNL) provides detailed comparison including tritium extraction technologies, TBR values (1.40 for LLE, 1.25–1.80 for Li), in-process tritium inventories (303 g for LLE, 747–749 g for Li at steady state), and startup inventories. Lithium is globally available and not subject to significant supply chain risk. Lead for LLE is mature industrial material. Wikipedia notes plasma contamination by high-Z lead as a risk for LLE specifically, which is why pure Li is being explored despite its higher reactivity. Kyoto Fusioneering partnership addresses liquid metal system development.

**Missing**: Piston and compression hardware material specifications (likely high-strength steel or specialized alloys) not published. Structural chamber materials under D-T neutron fluence not characterized for GF-specific geometry. Annual replacement schedule and costs for consumable components (liquid metal, seals) not published. No supply chain analysis for piston manufacturing at commercial scale.

**Gaps**:
- Piston and structural material specifications under operational conditions — proprietary — important
- Neutron activation and material replacement schedule for structural components — not-yet-sourced — important
- Supply chain for commercial-scale liquid metal system (pumps, heat exchangers, extraction units at Kyoto Fusioneering scale) — not-yet-sourced — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric power | 300 MWe (2× 150 MWe modules) | generalfusion.com/commercialization-path | h |
| Repetition rate | ~1 Hz | FST 2025, company sources | h |
| Fuel cycle | D-T, tritium bred in-situ | FST 2025, company sources | h |
| TBR (LLE blanket) | 1.40 | FST 2025 (SRNL/GF) | h |
| TBR (Li blanket) | 1.25–1.80 | FST 2025 (SRNL/GF) | h |
| Tritium startup inventory (LLE) | 317 g | FST 2025 | h |
| Tritium startup inventory (Li) | 747–793 g | FST 2025 | h |
| Plant doubling time | 56 days (LLE), 67 days (Li) | FST 2025 | h |
| Cavity diameter (commercial) | ~4 m | FST 2025 | h |
| Energy capture | Thermal/steam Rankine | Company sources | h |
| FOAK target date | ~2035 | generalfusion.com | m |
| MIF analog LCOE (ARPA-E ALPHA, 4 different concepts) | 34–54 $/MWh | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
| MIF analog CapEx (~500 MWe modular) | $0.84–1.64B | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
| MIF analog specific capital cost | 2.0–3.3 $/W | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
| MIF analog O&M | $42–61 M/year | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |

**Note on ARPA-E ALPHA analog**: The Woodruff/ARPA-E revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers four compact modular MIF concepts (PJMIF, Stabilized Liner Compressor, Staged Z-Pinch, Zap Energy) using the same CAS framework — none of which is General Fusion. These are the closest available public cost analogs for compact pulsed MIF plants at ~500 MWe scale. Key CAS line items relevant to GF: CAS 22.1.1 (First Wall/Blanket: $4–117M, average $57M), CAS 22.1.7 (Power Supplies — proxy for piston driver system: $12–140M, average $56M), CAS 27 (Special Materials including liquid metal: $1–267M, average $103M). These ranges reflect the wide uncertainty in novel MIF power core components and are usable as order-of-magnitude bounds only.

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by CAS category (GF-specific) | proprietary | blocking | No plant study published; ARPA-E analog gives order-of-magnitude bounds only |
| Recirculating power fraction (piston steam system) | proprietary | blocking | Critical for net output and LCOE; steam self-powering claimed but fraction not disclosed |
| Q value / energy per pulse (commercial) | proprietary | blocking | Determines gross fusion power; 350-fold compression to achieve Lawson criterion stated but Q not quantified |
| Capacity factor / plant availability | not-yet-sourced | important | No published estimate; ~1 Hz rep rate means pulse reliability drives availability |
| Thermal conversion efficiency | derivable | important | Standard Rankine ~33%; not optimized parameters published |
| Piston/driver capital cost | proprietary | blocking | Cost of pneumatic piston array is the unique GF cost driver; no public estimate |
| O&M costs (GF-specific) | proprietary | important | No published estimate; ARPA-E analog gives $42–61 M/year for ~500 MWe |
| Decommissioning cost | not-yet-sourced | nice-to-have | No published estimate; standard fusion plant assumptions could be borrowed |
| Learning curve / Nth-of-a-kind cost reduction | proprietary | nice-to-have | ARPA-E ALPHA revisit applies ~learning curve credits yielding COE2 from COE1 |

---

## Source Recommendations

- **GF MTF cost study / plant design report** — search OSTI for any DOE-funded techno-economic study of General Fusion or MTF concepts from the INFUSE or other programs; search for Hatch engineering study outputs (Hatch is GF's BOP engineering partner); search FIA (Fusion Industry Association) annual reports for any published cost projections — `not-yet-sourced`, `unverified — confirm existence before searching`
- **CNL plant integration study (2024)** — CNL and General Fusion launched a project in April 2024 to examine cost-effective plant integration designs (Wikipedia); any published output from this collaboration would directly address BOP and power conversion cost estimates — `not-yet-sourced`, `unverified — confirm existence before searching`
- **ARPA-E ALPHA original 2017 Bechtel costing report** — the 2017 precursor to the Woodruff revisit; General Fusion was not one of the four ALPHA concepts but this report provides the full CAS treatment for pulsed MIF concepts — `not-yet-sourced`, confirmed referenced in revisit paper (http://woodruffscientific.com/pdf/ARPAE_Costing_Report_2017.pdf)
- **Kyoto Fusioneering publications on liquid metal BOP** — Kyoto Fusioneering is GF's partner on tritium fuel cycle and liquid metal systems; search for any published cost or engineering analyses from this partnership — `not-yet-sourced`, `unverified — confirm existence before searching`
- **LANL MTF program reports** — LANL has a longstanding MTF program (FRX-L experiments, CRADA with GF); search OSTI for LANL MTF plant concept reports — `not-yet-sourced`

**Fleet-wide source dispositions:**
- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — **Integrated**: provides the closest available public cost analog for compact modular MIF (four different concepts, same CAS framework). Covers four ARPA-E ALPHA concepts that are NOT General Fusion. The CAS 27 special materials range ($1–267M, avg $103M) directly informs liquid metal cost uncertainty; driver cost analog (CAS 22.1.7: $12–140M) provides bounds on piston system costs. Used as explicit analog with stated caveat.
- `knowledge/sources/tea_dt_mfe_cost_analysis/` — **Disqualified**: tokamak-focused MFE study ($140–550/MWh LCOE), based on superconducting magnets and regulatory assumptions for large-scale MCF; architecturally inapplicable to MTF pulsed-mechanical concepts. Not usable as analog.
- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/` — **Disqualified for LCOE**: provides physics performance compilation only; no cost data, no MTF-specific economic content. Useful for §3 (subsystem maturity / physics progress benchmarking) but provides no new data beyond what is already captured from concept-scoped sources.

---

## Summary

Proceed to full D1+ analysis with stated data limitations. The concept is unusually well-documented at the technology description and fuel cycle levels for a pre-commercial private company. Sections 1–4 can be written substantively, with the engineering challenge list (Section 2) being particularly rich. The LCOE section (Section 5) should be written with explicit analog-based estimates derived from the ARPA-E ALPHA revisit, with prominent uncertainty disclosure — no GF-specific cost data is public, and several cost-driving engineering questions (recirculating power, commercial piston costs, capacity factor) remain proprietary or unresolved. The analysis should note the significant financial and operational uncertainty from GF's May 2025 layoffs (~25% of workforce) and financing constraints, which affect the credibility of the 2035 FOAK timeline.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 5
important_count: 7
counting_method: "deduplicated across all sections; LCOE blocking gaps counted once even if they appear in both §2 and §5 (recirculating power, Q value, piston cost, no cost study, 1 Hz vacuum re-establishment)"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor"
```