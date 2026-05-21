Now I have everything needed. Let me write the gap assessment report.

---

# Gap Assessment: QI Stellarator - HTS

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The Stellaris paper (Fusion Eng. & Design 2025) is exceptionally detailed for a pre-commercial fusion concept — it covers plasma physics, engineering design, subsystem specifications, and materials in depth across a 337 KB extracted document. The major gap is economic: no cost breakdown by subsystem exists, and the thermal efficiency figure (~32%) is an assumption rather than a detailed cycle study. A high-quality qualitative write-up and a parametric LCOE model can both be produced from available data, but cost estimates will be rough-order-of-magnitude analogues, not bottom-up.

---

## Section Coverage

### 1. Availability of Data

**Coverage**: Good

**Available**:
- *Stellaris* peer-reviewed paper (Garabedian et al., Fusion Eng. & Design 2025, DOI: 10.1016/j.fusengdes.2025.114868) — published, open-access extracted, highly detailed. Covers plasma equilibrium, engineering parameters, blanket, magnets, divertor, heating, and shielding. Source: `stellaris-design-details.md` / `stellaris-paper-details.md` (both appear to be extractions of the same document).
- Thea Energy *Helios* comparison paper (132 KB) — a second QI stellarator design by a different company that serves as an independent data point for design parameters and efficiency assumptions. Source: `helios-stellarator-comparison.md`.
- Proxima Fusion technology page — describes StarFinder optimization framework, QI-HTS value proposition, and W7-X scientific heritage. Source: `proxima-fusion-technology-page.md`.
- Proxima/RWE/Bavaria MoU press release (Feb 2026) — confirms Alpha demo (~€2B), site selection, financing structure (~20% private / ~20% Bavaria / RWE + federal), and supplier intent. Source: `proxima-fusion-2026-updates.md`.

**Missing**:
- No dedicated power plant economics report or system code study (analogous to ARIES, EUROfusion DEMO cost studies, or the Helion/CFS investor disclosures) has been sourced.
- No independent TRL assessment from a third party (e.g., European fusion assessment, DOE FPP-class review).

**Gaps**:
- Formal power plant economics study for Stellaris — `not-yet-sourced` — **important** (needed for LCOE section; paper-based analogues can substitute)
- Independent TRL verification — `not-yet-sourced` — **nice-to-have** (self-reported TRL from Proxima/paper is available; cross-check would improve confidence)

---

### 2. Challenges in Capturing System Function

**Coverage**: Good

**Available**:
The Stellaris paper provides a strong basis for identifying cost-modeling challenges:
- **3D non-planar coil geometry**: 50 modular HTS coils with complex winding packs, optimized via SQuID/StarFinder. No tokamak analogue exists for coil cost. The coil complexity (peak coil current 15.4 MA, stored energy 111 GJ) is described in detail — the challenge is translating geometry into cost, not understanding the geometry.
- **ECRH heating at 230–240 GHz**: 50 MW from 7 gyrotrons per port × 8 ports = 56 gyrotrons. This frequency is at or beyond current industrial capability (W7-X uses 140 GHz). The paper notes this explicitly.
- **Island divertor**: Physics well-described (4/4 island chain, tungsten-based), but heat exhaust modeling is acknowledged as still maturing. No demonstrated analog at power-plant wall loads (10 MW/m² target stated).
- **WCLL blanket TBR**: TBR = 1.07 from neutronics modeling. Paper acknowledges this is a point estimate with sensitivity to geometry and enrichment — relevant to tritium self-sufficiency margin.
- **Cryo-plant load**: 111 MW conduction to coils is stated. This is a significant recirculating power fraction (~11% of thermal output) with cost implications.
- **Physics extrapolation**: The H₉₈ confinement enhancement factor required is 1.30 — a 30% improvement over the empirical W7-X scaling. This is the main unvalidated physics claim.

**Missing**:
- No detailed balance-of-plant (BoP) schematic or heat integration analysis. The 1/3 (~32%) thermal conversion efficiency is an assumption, not a cycle study.
- No detailed remote maintenance (RM) cost/schedule analysis. RM complexity for non-planar 3D coils is expected to be higher than tokamaks but is not quantified.

**Gaps**:
- Detailed steam/power cycle design and efficiency justification — `derivable` (can use generic stellarator/fusion plant BoP analogues, e.g., ~33% Rankine at 500°C EUROFER limit) — **important**
- Remote maintenance cost model — `proprietary` / `not-yet-sourced` — **important** (remote maintenance is typically 10–20% of total OpEx in fusion plant studies; lacking it introduces a large uncertainty band)
- 3D coil manufacturing cost model — `not-yet-sourced` — **important** (no published bottom-up cost model for non-planar HTS stellarator coils; analogue from ITER TF coils or CFS SPARC coils would be indirect)
- ECRH system cost at 230–240 GHz — `not-yet-sourced` — **important** (current gyrotron cost analogues are at 140 GHz; higher frequency increases unit cost)

---

### 3. Maturity of Key Subsystems and Components

**Coverage**: Partial

**Available**:
The Stellaris paper and Proxima tech page provide sufficient basis for TRL assessments on most subsystems:

| Subsystem | Basis Available | Implied TRL | Source |
|-----------|----------------|-------------|--------|
| QI plasma equilibrium / confinement physics | W7-X experimental validation at small scale | TRL 4–5 (device-scale demo, scaling unverified) | Stellaris paper §2 |
| Island divertor | W7-AS and W7-X demonstrated, power-plant loads not tested | TRL 4 | Tech page, paper §3 |
| HTS REBCO coils (20 T, stellarator geometry) | REBCO tape commercially available; 3D stellarator winding at scale not demonstrated | TRL 2–3 | Dossier, paper §4 |
| ECRH at 230–240 GHz | W7-X runs at 140 GHz; 230 GHz systems in lab only | TRL 2–3 | Stellaris paper §5 |
| WCLL blanket | EUROfusion DEMO-class design work; not yet prototyped for stellarator geometry | TRL 2–3 | Stellaris paper §6 |
| Tungsten first wall | Demonstrated on JET, W7-X; power-plant lifetimes not validated | TRL 4–5 | Stellaris paper §3 |
| Cryogenic pellet injection | Operational on W7-X; power-plant rep-rate not qualified | TRL 4 | Stellaris paper §5 |
| EUROFER97 structure | Irradiation data available; power-plant fluence regime (>20 dpa) not yet qualified | TRL 4 | Stellaris paper §6 |

**Missing**:
- No explicit TRL table appears in the Stellaris paper — TRL assessments above are inferred from the technical descriptions and the W7-X/DEMO literature heritage.
- No magnet factory production rate or per-coil cost estimate is available.

**Gaps**:
- Explicit TRL table for Stellaris subsystems — `not-yet-sourced` — **nice-to-have** (EUROfusion fusion plant roadmaps and W7-X companion papers may have TRL assessments for overlapping subsystems; unverified — confirm existence before searching)
- 3D HTS coil winding demonstration at scale — `truly-unknown` (no one has wound a non-planar 20T HTS coil at power-plant current; this is a genuine TRL gap) — **blocking** for the technology, **important** for the analysis (flag as major risk)

---

### 4. Key Materials and Supply Chain Considerations

**Coverage**: Partial

**Available**:
- **REBCO HTS tape**: Named explicitly as the conductor (20 T capable). Dossier notes REBCO supply chain risk (single-sourcing concern). Global REBCO production is dominated by a small number of manufacturers (SuperPower, SUNAM, SuNAM, Fujikura). The Stellaris paper does not quantify tape length or cost per meter.
- **EUROFER97**: Structural material for blanket and vessel. European supply chain exists (Böhler/Uddeholms); used in JET and DEMO design studies. Production scale for a power plant is not quantified.
- **Tungsten**: First wall and divertor armor. Established industrial supply; primary concern is manufacturing to power-plant specifications (plasma-facing surface quality, bonding to structural steel). Sources note W7-X demonstrated tungsten components.
- **LiPb (lithium-lead eutectic)**: Blanket coolant and tritium breeder. Lithium enrichment (Li-6) required. Global Li-6 production is modest; enrichment is a non-trivial industrial step.
- **Tritium startup inventory**: D-T fuel requires ~1–2 kg tritium startup charge (from Helios comparison source; Stellaris paper does not state this explicitly). Current global tritium inventory (~25 kg) is limited.

**Missing**:
- No supply chain risk quantification (cost, lead time, single-point-of-failure analysis) in any source.
- No REBCO tape length/quantity estimate for Stellaris (needed to assess supply chain feasibility).
- No Li-6 enrichment requirement calculation specific to Stellaris TBR = 1.07.

**Gaps**:
- REBCO tape quantity estimate for Stellaris coils — `derivable` (can estimate from coil geometry and current density specs in the paper) — **important**
- REBCO production capacity vs. demand timeline — `not-yet-sourced` — **important** (IEA/DOE reports on critical mineral supply chains or published stellarator supply chain studies; unverified — confirm existence before searching)
- Li-6 enrichment requirements and supply chain — `not-yet-sourced` — **important** (EUROfusion WCLL blanket studies address this; unverified — confirm existence before searching)
- Tritium startup inventory source and cost — `not-yet-sourced` — **important** (CANDU-sourced tritium at ~$30k/g is the standard assumption; confirm applicability)

---

### 5. LCOE Parameter Extraction

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Peak fusion power | 2.7 GW | Stellaris paper Table 2 | High |
| Peak thermal power | 3.1–3.3 GW | Stellaris paper | High |
| Net electrical output | ~1 GW | Stellaris paper / dossier | Medium |
| Thermal conversion efficiency | ~32% (stated as "1/3") | Stellaris paper §7 | Medium (assumed, not cycle-modeled) |
| Auxiliary power — ECRH | 50 MW | Stellaris paper Table 2 | High |
| Recirculating power — cryo | 111 MW | Stellaris paper Table 2 | High |
| Plasma major radius | 12.7 m | Stellaris paper Table 2 | High |
| Plasma minor radius | 1.5 m | Stellaris paper Table 2 | High |
| Number of modular coils | 50 | Stellaris paper | High |
| Peak coil field | 14.4 T (on-axis) / 20 T (at conductor) | Stellaris paper | High |
| Stored magnetic energy | 111 GJ | Stellaris paper Table 2 | High |
| Blanket TBR | 1.07 | Stellaris paper §6 | Medium |
| Peak wall load | 4.05 MW/m² | Stellaris paper Table 2 | High |
| Confinement gain (Q) | ~4–6 (fusion power / auxiliary power) | Stellaris paper (derived) | Medium |
| H₉₈ confinement factor required | 1.30 | Stellaris paper §2 | Medium (unvalidated extrapolation) |
| Alpha demo cost | ~€2B | Proxima/RWE MoU 2026 | Medium (announcement, not engineering estimate) |
| ECRH system size | 56 gyrotrons × 1 MW each | Stellaris paper §5 | High |
| Plasma volume | 448 m³ | Stellaris paper Table 2 | High |
| Operation mode | Steady-state | Dossier / Stellaris paper | High |
| Fuel type | D-T | Dossier | High |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capacity factor (%) | derivable | Blocking | Steady-state operation claimed; no explicit CF stated. Can assume 85–90% with stated basis; needs flagging. |
| CapEx breakdown by subsystem (magnets, blanket, vessel, BoP) | proprietary / not-yet-sourced | Blocking | No cost breakdown in any source. Alpha demo = €2B covers demo-scale. Power plant CapEx must be estimated from analogues ($/W literature ranges: 2–10 $/W for fusion). |
| Blanket replacement schedule and cost | not-yet-sourced | Important | WCLL blanket lifetime under stellarator neutron flux not quantified. EUROfusion DEMO studies have blanket replacement intervals (~2–5 years); adapt with stated assumptions. |
| First wall replacement cost | not-yet-sourced | Important | Tungsten first wall lifetime under 4 MW/m² load not stated. Analogues from tokamak studies needed. |
| O&M staffing cost | truly-unknown | Important | No fusion power plant has operated at scale; all estimates are analogy-based. |
| Tritium inventory and cost | not-yet-sourced | Important | ~1–2 kg startup from Helios source, not stated in Stellaris paper. Cost ~$30k/g → $30–60M startup inventory. |
| ECRH system capital cost | not-yet-sourced | Important | 56 × 1 MW gyrotrons at 230–240 GHz. Cost per unit at this frequency not in sources; W7-X gyrotron analogues at 140 GHz available in literature. |
| Thermal cycle details (sCO₂ vs Rankine, efficiency breakdown) | derivable | Important | "1/3 efficiency" is stated. EUROFER97 limit ~500°C constrains cycle to ~33–35% Rankine. Can derive with stated assumptions. |
| Remote maintenance cost and schedule | proprietary | Important | Not published. Analogue: tokamak RM cost studies (e.g., ARIES, DEMO). |
| Decommissioning cost | truly-unknown | Nice-to-have | Standard fusion plant assumption (~10–15% of overnight capital) can be applied. |
| HTS coil manufacturing cost per coil | not-yet-sourced | Important | REBCO tape cost ~$10–50/m; coil geometry in paper allows tape-length estimate. Total magnet cost derivable with assumptions. |
| Land/site cost | proprietary | Nice-to-have | Gundremmingen stated as site; decommissioned nuclear site may have infrastructure value. |

---

## Source Recommendations

1. **EUROfusion DEMO WCLL blanket design studies** — addresses blanket replacement schedule, TBR sensitivity, and Li-6 enrichment requirements. Search: OSTI/EUROfusion publications on "WCLL blanket lifetime" or "WCLL replacement interval." — `not-yet-sourced` — unverified, confirm existence before searching.

2. **ARIES-CS or HSR stellarator power plant studies** — published system-level cost models for compact stellarator power plants that predate Stellaris but establish parametric cost structures (magnets, blanket, BoP). Search: "ARIES Compact Stellarator" or "Helias Reactor HSR" cost study. — `not-yet-sourced` — ARIES-CS is a known publication (Raffray et al., ~2008); confirm the HSR study exists before citing.

3. **CFS/SPARC magnet cost analogues** — REBCO HTS magnet cost modeling for high-field fusion magnets. CFS has published engineering cost information on SPARC's TF coils. Applicable as analogue for Stellaris coil cost estimation. — `not-yet-sourced` — unverified, confirm existence before searching.

4. **W7-X companion engineering papers** — detailed cost breakdown for W7-X construction (total ~1B EUR for experimental device). Provides bottom-up magnet manufacturing cost data at relevant scale (though at 2.5 T, not 20 T). Search: "W7-X construction cost" or "Wendelstein 7-X magnet fabrication." — `not-yet-sourced` — unverified, confirm existence before searching.

5. **Gyrotron cost literature at high frequency** — 140 GHz unit costs are well-documented (W7-X: ~€3–5M per 1 MW gyrotron); 230 GHz is at developmental stage. Search: "high-frequency gyrotron cost" or "ECRH system cost fusion." — `not-yet-sourced` — unverified, confirm existence before searching.

6. **IEA/DOE critical mineral supply chain reports on REBCO tape** — quantify production bottleneck for HTS tape scale-up. Search: "REBCO supply chain fusion" or "HTS tape production capacity roadmap." — `not-yet-sourced` — unverified, confirm existence before searching.

---

## Summary

**Proceed to full analysis with caveats noted.**

The Stellaris paper is one of the most detailed pre-commercial fusion power plant design studies available in the public literature — unusually so. Physics parameters, engineering geometry, materials, and subsystem descriptions are documented at a level that fully supports qualitative write-up and parametric LCOE modeling. The concept is well-characterized enough that most missing parameters are `derivable` or can be filled with `not-yet-sourced` analogues rather than being truly unknown.

The main caveats to flag in the analysis are: (1) CapEx must be estimated from literature analogue ranges (2–10 $/W), not from a bottom-up Stellaris-specific cost model; (2) the 32% thermal efficiency is an assumption constrained by EUROFER97 temperature limits, not a detailed cycle study; (3) H₉₈ = 1.30 is the critical unvalidated physics assumption — if confinement falls short, Q and power output drop sharply; (4) 3D HTS coil manufacturing at power-plant scale has no demonstrated precedent and represents the single highest-risk TRL gap. These uncertainties can all be surfaced and parameterized in the LCOE model rather than treated as blockers.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 2
important_count: 8
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Good"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Unknown"
```
