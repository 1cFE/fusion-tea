Now I have sufficient information to write the gap assessment. No extracted source documents are in the repo — only the dossier summary exists. Let me produce the report.

---

# Gap Assessment: Compact Liquid-Wall HTS Stellarator

## Overall Readiness
**Rating**: Mostly Ready (with one critical extraction gap)
**Summary**: Renaissance Fusion has published three peer-reviewed papers covering the core design point, blanket/neutron management, and power conversion — an unusually strong publication record for a private fusion company. The dossier captures all 12 schema columns at high confidence, and technical parameters supporting an LCOE model (efficiency, geometry, power output, wall loading) are available in outline. The principal gap is that none of the primary sources have been extracted into the knowledge base, meaning the analysis must work from the dossier summaries rather than the full technical content. The Nuclear Fusion 2024 paper is titled "economically optimized design point" and almost certainly contains cost-relevant data not captured in the dossier — this is the most important single source to retrieve.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate-to-Good (strong publications, no full plant study, sources not yet extracted)

**Available**:
- *Nuclear Fusion 64 (2024) 026007*: Peer-reviewed design point paper. Covers geometry (A~4, R≤4 m), magnet design (10 T nominal, 15 T at coil, 20–40 T peak at coil surface), fuel (D-T at 10 keV), heating (NNBI, 60% neutralization efficiency), and claims to present an "economically optimized design point" — implying cost trade-off content that the dossier does not fully capture.
- *J. Nuclear Materials 599 (2024) 155239*: Peer-reviewed blanket paper. Covers liquid Li-LiH wall architecture (15 cm Pb + 18 cm Li-LiH), 25 MW/m² wall loading, fm=1.24 neutron energy multiplication, 99.99% neutron energy absorption, and full radial build (wall + 50 cm VH₂ + 1.3 m concrete bioshield).
- *Energy Conversion and Management 276 (2023) 116572*: Peer-reviewed power conversion paper. Covers sCO2 Brayton-Rankine combined cycle optimized via genetic algorithm, 49–51% cycle efficiency, 34% net plant efficiency.
- Company website and MT29 abstract: Confirms 6 T peak Helmholtz magnet demo at 1.2 m diameter and 20 K; steady-state operation; 1 GWe target.
- UC Berkeley seminar: Additional context on HTS magnet approach and liquid metal wall.

**Missing**:
- Full extracted content of the three primary papers — the dossier captures select values but not full parameter tables, sensitivity analyses, or cost breakdowns that likely exist in the papers.
- No published full-system plant study (comparable to ARIES-CS, HELIAS-5B, or similar stellarator power plant design studies).
- No techno-economic report or white paper with explicit cost estimates.

**Gaps**:
- Full NF 2024 paper content not extracted — `not-yet-sourced` — **blocking** (high probability of containing capital cost parameters and design trade-off data not in the dossier)
- Full JNM 2024 and ECM 2023 paper content not extracted — `not-yet-sourced` — **important** (may contain component-level cost assumptions)
- No plant study equivalent — `truly-unknown` / `proprietary` — **important** (company is pre-pilot; no full BOP system integration study is public)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- The integrated liquid metal wall eliminates the blanket/shield/first-wall cost boundary — the JNM paper gives structural parameters (wall loading, radial build, neutron multiplication) sufficient to begin estimating the "wall system" cost as a single account.
- The sCO2 cycle paper provides efficiency data (34% net plant) and a specific cycle architecture (combined Brayton-Rankine) — enabling BOP cost analogy to industrial sCO2 demonstrators.
- Ignition (Q = ∞) target is explicit — eliminates recirculating power fraction as a variable but introduces large physics uncertainty on whether the plasma actually ignites.
- The NNBI startup heating requirement is specified (60% neutralization efficiency) — bounded startup energy cost.

**Missing**:
- Laser-patterned REBCO film deposition: no published cost model or manufacturing yield data for this process. This is the most novel manufacturing step and has no direct cost analogue.
- Plasma confinement quality at operating parameters: QI optimization for compact (A~4) stellarators is not as mature as W7-X (A~10). Confinement scaling from W7-X to A~4 at 10 T is uncertain.
- Ignition threshold assumptions: the design claims Q = ∞ but the stability and confinement assumptions underpinning that claim are not independently validated.
- Liquid metal flow dynamics and magnetohydrodynamic (MHD) effects at 25 MW/m² and 10 T: no experimental validation at relevant scale.

**Gaps**:
- Magnet manufacturing cost model for laser-patterned HTS film — `truly-unknown` — **blocking** (no analogous manufacturing process exists at scale; must use engineering estimate or REBCO tape area analogy)
- Confinement quality / energy confinement time at operating parameters — `proprietary` (company internal codes) — **important** (affects recirculating power and Q assumptions)
- MHD compatibility of liquid Li-LiH flow at fusion-relevant field strength and wall loading — `not-yet-sourced` — **important** (search: Liquid metal MHD in high-field stellarators, Muon Catalyzed Fusion literature, ENEA/KIT liquid metal blanket MHD studies)
- Ignition margin sensitivity — `not-yet-sourced` — **important** (the NF 2024 paper likely addresses this; extraction needed)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS Magnet Demonstration**: 6 T peak Helmholtz magnet at 1.2 m diameter, 20 K — directly confirms the laser-patterned HTS film approach works at lab scale (MT29 abstract, UC Berkeley seminar). TRL ~3–4.
- **sCO2 Power Cycle**: Industrial-scale sCO2 Brayton demonstrators exist (e.g., Echogen, NET Power, Sandia). The fusion-specific combined Brayton-Rankine is novel but the underlying cycle TRL is ~5–6. Integration with a liquid metal heat source is undemonstrated.
- **Stellarator QI physics**: W7-X at IPP Greifswald demonstrates quasi-isodynamic optimization works at full scale. However, W7-X has A~10 vs. A~4 for Renaissance, and is LTS at lower field — significant extrapolation.
- **Liquid metal wall concept**: Conceptually studied in fusion context (NSTX liquid lithium divertor experiments, ORNL, KIT), but not at Renaissance's claimed 25 MW/m² wall loading or 10 T field environment.

**Missing**:
- No published TRL assessment from the company or independent review.
- No prototype-scale demonstration of laser-patterned HTS film producing a 3D stellarator field (beyond the single Helmholtz demo).
- No flowing liquid metal wall demonstration at fusion-relevant parameters.
- Vacuum vessel and structural systems at compact stellarator geometry: not discussed in available sources.
- Remote handling systems: not addressed (though liquid metal wall reduces activation of surrounding structure).

**Gaps**:
- Laser-patterning HTS for complex 3D stellarator coil geometry (beyond Helmholtz) — `proprietary` — **blocking** (the Helmholtz demo doesn't prove the full stellarator field can be produced this way; company likely has additional internal results)
- Liquid metal wall at operating conditions (25 MW/m², 10 T, steady-state flow) — `not-yet-sourced` — **important** (search: NSTX-U liquid metal PFC results, KIT HCLL/DCLL MHD experiments, ORNL Li wall programs — `unverified — confirm existence before searching`)
- Integrated plasma-facing first wall endurance / replacement schedule — `truly-unknown` — **important** (liquid metal walls self-renewing in principle but pump/containment lifetime is unaddressed)
- Balance-of-plant integration TRL — `not-yet-sourced` — **nice-to-have**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- REBCO HTS tape is identified as the magnet material (from NF 2024 dossier). REBCO tape supply is a known bottleneck for all HTS fusion programs.
- Liquid Li-LiH is identified as the wall/blanket material (from JNM 2024). Li-6 enrichment is an established but capacity-constrained supply chain.
- Pb pebbles for neutron multiplication (from JNM 2024) — Pb is abundant with no supply concerns.

**Missing**:
- No REBCO tape quantity estimate (meters of tape per machine) in the dossier — this is the critical supply chain figure for HTS magnets. However, the Renaissance approach uses deposited film, not wound tape — the manufacturing process is entirely different and the relevant bottleneck is film deposition equipment, not tape supply.
- Li-6 enrichment demand: the 15 cm + 18 cm liquid Li-LiH wall at 1 GWe requires a quantity estimate — not in the dossier.
- No discussion of tritium inventory requirements during startup (the global civilian supply is ~25 kg; startup inventory demand could be significant).
- No discussion of supply chain for laser deposition equipment at scale.
- No discussion of Pb pebble bed manufacturing and replacement logistics.

**Gaps**:
- REBCO film deposition capacity / supply chain (novel process — not tape winding) — `truly-unknown` — **blocking** (no analogue manufacturing process at scale; this is a first-of-kind manufacturing challenge)
- Startup tritium inventory requirement — `derivable` (from plasma volume, density, burn fraction estimates) — **important**
- Li-6 enrichment capacity for full-scale deployment — `not-yet-sourced` — **important** (search: ORNL Li-6 production assessments, DOE tritium supply studies — `unverified — confirm existence before searching`)
- Laser film deposition equipment supply chain — `proprietary` — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial — performance and efficiency parameters available; capital and operating cost data largely absent

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electrical output | 1 GWe | NF 2024 (dossier) | high |
| Thermal-to-electric cycle efficiency | 49–51% | ECM 2023 (dossier) | high |
| Net plant efficiency | 34% | ECM 2023 (dossier) | high |
| Power conversion cycle type | sCO2 Brayton-Rankine combined | ECM 2023 (dossier) | high |
| Plasma gain (Q) | ∞ (ignition target) | NF 2024 (dossier) | high |
| Major radius | ≤4 m | NF 2024 (dossier) | high |
| Aspect ratio | ~4 | NF 2024 (dossier) | high |
| Toroidal field (nominal) | 10 T | NF 2024 (dossier) | high |
| Peak coil field | 15 T (coil), 20–40 T (peak) | NF 2024 (dossier) | high |
| Wall loading | 25 MW/m² | JNM 2024 (dossier) | high |
| Neutron energy multiplication | fm = 1.24 | JNM 2024 (dossier) | high |
| Neutron energy absorption | 99.99% | JNM 2024 (dossier) | high |
| Radial build (blanket+shield) | 15 cm Pb + 18 cm Li-LiH + 50 cm VH₂ + 1.3 m concrete | JNM 2024 (dossier) | high |
| Operation mode | Steady-state (~100% duty cycle) | Company website (dossier) | high |
| Startup heating | NNBI, 60% neutralization efficiency | NF 2024 (dossier) | high |
| Magnet operating temperature | 20 K | MT29/Berkeley (dossier) | high |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (CAS 20–70) | not-yet-sourced / proprietary | blocking | NF 2024 "economically optimized" title suggests some cost content — extract first |
| Magnet system capital cost | truly-unknown | blocking | Novel film deposition process has no existing cost model; REBCO tape cost analogues apply only partially |
| Liquid metal wall system cost | truly-unknown | blocking | No commercial analogues at this scale or field strength |
| Total plant overnight cost ($/kWe) | proprietary | blocking | No published figure |
| Operating & maintenance cost ($/MWh or $/yr) | proprietary | important | Steady-state operation is an advantage but no data |
| Component replacement schedule and cost | truly-unknown | important | Liquid metal wall self-renewing in principle; pump/plumbing lifetime unknown |
| Availability / capacity factor target | not-yet-sourced | important | Company claims "near-100%" — need uncertainty bounds; NF 2024 may address |
| Startup tritium inventory requirement | derivable | important | Can be estimated from plasma parameters |
| Tritium breeding ratio (TBR exact value) | not-yet-sourced | important | Dossier notes fm=1.24 confirmed but TBR ~1.60 unverified; JNM 2024 full paper may clarify |
| Recirculating power fraction | derivable | important | At Q=∞ (ignition), recirculating power dominated by magnets + pumps, not heating — need magnet power estimate |
| Plant lifetime assumption | not-yet-sourced | important | Standard assumption 30–40 yr; design-specific limits from neutron damage or liquid metal corrosion not available |
| Balance of plant cost (non-power-conversion) | not-yet-sourced | nice-to-have | sCO2 BOP has some industrial cost data; fusion integration adds cost |
| Contingency and financing assumptions | truly-unknown | nice-to-have | No public project finance analysis |

---

## Source Recommendations

1. **Extract NF 2024 paper in full** (`not-yet-sourced`, blocking) — Nuclear Fusion 64 (2024) 026007. The "economically optimized design point" title strongly suggests capital cost estimates, design trade-off curves, and sensitivity parameters not captured in the dossier. This is the single highest-priority extraction.

2. **Extract JNM 2024 paper in full** (`not-yet-sourced`, important) — J. Nuclear Materials 599 (2024) 155239. The radial build and wall loading data in the dossier are summarized; the full paper likely contains detailed neutronics, thermal-hydraulic calculations, and breeding performance that feed blanket cost estimation.

3. **Extract ECM 2023 paper in full** (`not-yet-sourced`, important) — Energy Conversion and Management 276 (2023) 116572. The 34% net efficiency is noted but the optimization paper likely contains component-level heat exchanger sizing, turbine specifications, and auxiliary power estimates.

4. **Search for stellarator power plant studies with cost breakdowns** (`not-yet-sourced`, important) — e.g., HELIAS-5B (IPP/KIT), ARIES-CS (UCSD), MHH2, or similar stellarator plant studies that provide CAS-format cost structures. These provide the closest cost analogues even if geometry and magnet technology differ. Suggest search: OSTI.gov "stellarator power plant cost" or "HELIAS LCOE" — `unverified — confirm existence before searching`.

5. **Search for liquid metal wall cost/performance studies in fusion context** (`not-yet-sourced`, important) — KIT, ORNL, or CNL publications on flowing liquid lithium walls, particularly MHD pressure drop calculations at high field which affect pumping power and cost. Suggest search: OSTI.gov "flowing liquid lithium wall fusion MHD" — `unverified — confirm existence before searching`.

6. **Search for REBCO film deposition manufacturing cost studies** (`not-yet-sourced`, nice-to-have) — laser ablation deposition of REBCO on large-area substrates is an active research topic in superconductor manufacturing (separate from tape manufacturing). Any published cost-per-m² data would be valuable. Suggest search: "PLD REBCO large area deposition cost" or "REBCO thin film coated conductor cost" — `unverified — confirm existence before searching`.

---

## Summary

**Proceed to full analysis, with the NF 2024 paper extracted first.**

The available data is sufficient for a solid qualitative write-up (D1 sections 1–3) and a partial quantitative LCOE model. The performance parameters (1 GWe, 34% net efficiency, steady-state, ~100% capacity factor) provide the denominator for LCOE and the physical framing for the cost model. The novel subsystems (laser-patterned HTS film, liquid metal wall) have no direct cost analogues — the analysis should use bounding estimates with explicit uncertainty ranges rather than precise cost figures. The "economically optimized design point" framing in the NF 2024 paper title is the strongest signal that capital cost data exists in the primary literature and has not been captured. Extracting that paper before writing the analysis is the highest-leverage action available.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready (with one critical extraction gap)"
blocking_count: 4
important_count: 7
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Moderate-to-Good (strong publications, no full plant study, sources not yet extracted)"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Partial — performance and efficiency parameters available; capital and operating cost data largely absent"
```
