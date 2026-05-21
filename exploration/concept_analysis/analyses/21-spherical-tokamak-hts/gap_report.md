Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: Spherical Tokamak - HTS

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: Tokamak Energy is one of the more transparent private fusion companies, and three research iterations have produced solid coverage of machine parameters, magnet technology, heating approach, blanket concept, and roadmap. The major gaps for LCOE analysis are Q value (deliberately unpublished), power conversion cycle selection (not yet made or disclosed), capital cost breakdown (proprietary), and EC heating power level for the pilot plant. These gaps are characteristic of a pre-conceptual design at this stage — they can be partially bridged with analogues from conventional tokamak power plant studies and the broader spherical tokamak literature (STEP programme). The analysis can proceed with clearly flagged assumptions.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Machine parameters for ST-E1 Rev D are public: R=5.0 m, A=2.3, B=5.25 T on-axis, 450-750 MWe net, outboard-only liquid Li blanket TBR=1.2 (DPP 2025 abstract; `dpp2025-abstract.md`)
- Design evolution from initial (2023) through Rev D (2025) is documented, showing significant growth in both machine size and power ambition (`st-e1-design-evolution.md`)
- Magnet system: REBCO HTS, Demo4 complete 14 TF + 2 PF coil set validated at 11.8 T (`tokamak-energy-demo4-magnets.md`)
- Heating: EC-only flat-top operation confirmed in peer-reviewed EPJ 2026 paper (`tokamak-energy-ec-heating-pilot-plant.md`)
- Center-stack shielding: WC cermet in ~32 cm radial envelope, peer-reviewed 2019 study (`spherical-tokamak-center-stack-shielding.md`)
- Pulsed operation rationale and 15-minute pulse target documented (`pulsed-spherical-tokamak-paper.md`, `tokamak-energy-roadmap.md`)
- Company transparency: Tokamak Energy is part of the US DOE Milestone-Based Fusion Development Program, which requires regular public reporting. More disclosure than most private companies, but still pre-conceptual level detail.

**Missing**:
- No published plant study with cost breakdown (nothing comparable to a GASC/PROCESS system code output)
- Q value for Rev D design not stated anywhere
- Plasma current (Ip) for Rev D not stated (only pre-Rev D value of 13.6 MA available from disruption paper)
- No capital cost estimates, even rough, from Tokamak Energy

**Gaps**:
- Capital cost data — `proprietary` — **important**: can use analogue from conventional tokamak studies and STEP programme estimates
- Q value — `proprietary` / `truly-unknown` — **blocking** for LCOE: must assume or bound-estimate from power output targets
- Published plant study — `not-yet-sourced` — **important**: STEP programme (UK UKAEA spherical tokamak power plant) may have comparable published system code outputs

---

### 2. Challenges in Capturing System Function
**Coverage**: Good (challenges well-characterized)

**Available**:
- Asymmetric blanket/shielding architecture is well-understood: outboard blanket covers fusion-relevant surface; inboard center-stack uses WC cermet shield with no tritium breeding. This is a fundamental ST cost/performance challenge documented in the literature.
- EC-only heating for flat-top is documented as a design choice with physics rationale (O-mode efficiency, ray-tracing optimization). Power level for the pilot plant is undisclosed, but the approach is clear.
- Pulsed operation and its implications for power conversion (need for thermal energy storage) are noted, with molten salt buffering as a referenced approach.
- Center stack engineering challenge is well-documented: 32 cm shielding envelope, WC cermet candidates, radiation damage to HTS tapes.
- Design volatility is observable: the major power target change from 85 MWe to 450-750 MWe between initial (2023) and Rev D (2025) illustrates that the design is immature and uncertainty bands on performance are wide.

**Missing**:
- Thermal energy storage (TES) system design and cost — not covered in any source
- Disruption frequency and energy management approach for pilot plant — only pre-Rev D disruption modelling available (arxiv:2512.16604 using old parameters)
- Quantified recirculating power fraction — EC heating typically has low wall-plug efficiency (~30-40%), and the EC power needed for a 450-750 MWe plant is unknown

**Gaps**:
- Recirculating power / EC system wall-plug efficiency — `derivable` from analogues — **important**: EC current drive recirculating power fraction strongly affects net electric output
- TES system for pulsed operation — `not-yet-sourced` — **nice-to-have**: STEP and DEMO studies have addressed this
- Disruption handling for Rev D parameters — `not-yet-sourced` — **nice-to-have**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **HTS magnets (REBCO)**: TRL 5-6 — Demo4 validated complete 14 TF + 2 PF system at 11.8 T (Nov 2025). World-first for a complete tokamak coil set. Beyond single-coil demos (CFS, 20 T in 2021).
- **ST40 experimental device**: operational, demonstrated 100M°C plasma ion temperature (2022), highest triple product of private fusion companies.
- **ST80-HTS**: under construction, build completion ~2026. First large-scale HTS spherical tokamak. TRL 4-5 system level.
- **EC heating (gyrotrons)**: TRL 6-7 — 1 MW gyrotron from Kyoto Fusioneering installed on ST40. Commercial gyrotron technology exists; integration at pilot plant scale is the challenge.
- **WC cermet center-stack shielding**: TRL 3-4 — material properties characterized (2019 paper), but irradiation damage under fusion neutrons not characterized. Manufacturing at scale for 32 cm annular center stack is untested.
- **Liquid lithium blanket (outboard)**: TRL 3-4 — concept well-defined, TBR=1.2 targeted. No prototype at reactor scale for any tokamak concept.
- **Tritium breeding/processing system**: TRL 3-4 — no pilot-scale lithium blanket with T extraction demonstrated for any fusion concept.

**Missing**:
- TRL assessment for power conversion system (steam/sCO2 — not yet selected)
- TRL for vacuum vessel / first wall at pilot plant scale
- TRL for remote maintenance systems (noted as an early design priority but no details)

**Gaps**:
- First wall / divertor TRL and lifetime — `not-yet-sourced` — **important**: W or W-alloy first wall replacement schedule drives maintenance costs; ITER/DEMO analogue literature exists
- Remote maintenance system TRL — `not-yet-sourced` — **important**: DPP 2025 notes maintenance was an "early-stage priority" but no technical details published
- Power conversion system TRL — `derivable` (depends on cycle selection) — **important** but not blocking

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO HTS tape**: identified as key material. 12 mm wide, <0.1 mm thick. ~200× current density of copper. Supply chain is a known bottleneck for the entire fusion-HTS sector (shared with CFS, TAE, and others). Current global REBCO production is far below what pilot plants would require.
- **Tritium supply**: D-T fuel cycle identified; no tritium supply analysis in sources. This is a known industry-wide constraint — civilian tritium supply is currently ~5-10 kg/year globally (CANDU reactors), and startup tritium inventory requirements are uncertain.
- **Tungsten carbide (WC cermet)**: center-stack shielding material. WC is an established industrial material, but fusion-grade WC cermet in the specific form factor has no supply chain.
- **Liquid lithium**: outboard blanket coolant/breeder. Lithium supply is adequate; Li-6 enrichment capacity is the bottleneck if natural Li is insufficient.

**Missing**:
- Quantified REBCO tape requirements for ST-E1 magnet system
- Any supply chain analysis or manufacturing readiness assessment
- Tritium startup inventory estimate for the ST-E1 plant size

**Gaps**:
- REBCO tape quantity and cost for full magnet system — `proprietary` / `not-yet-sourced` — **important**: industry scaling estimates exist (e.g., from CFS arc magnet costing studies), unverified for this geometry; flag as `unverified — confirm existence before searching`
- Tritium startup inventory — `derivable` — **important**: can be estimated from fusion power, tritium consumption rate, TBR, and buildup time; analogue from ITER/DEMO tritium studies
- Li-6 enrichment requirements — `derivable` — **nice-to-have**
- WC cermet manufacturing readiness — `truly-unknown` — **nice-to-have**: insufficient irradiation data is noted in the 2019 paper itself

---

### 5. LCOE Parameter Extraction

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Net electric output | 450-750 MWe | DPP 2025 abstract | medium (wide range reflects physics/tech uncertainty) |
| Major radius | 5.0 m | DPP 2025 abstract | high |
| Aspect ratio | 2.3 | DPP 2025 abstract | high |
| On-axis toroidal field | 5.25 T | DPP 2025 abstract | high |
| Blanket concept | Outboard liquid Li, TBR=1.2 | DPP 2025 abstract | high |
| Operation mode | Quasi-steady, 15+ min pulses | Multiple sources | high |
| Primary heating (flat-top) | EC only | EPJ 2026 | high |
| Magnet material | REBCO HTS, 11.8 T at coil validated | Demo4 (Nov 2025) | high |
| Timeline | Mid-2030s pilot plant | Multiple sources | medium |
| Center-stack shielding | WC cermet, ~32 cm radial | Humphry-Baker & Smith 2019 | medium (smaller device) |
| Fusion power (initial design) | 800 MW | DPP 2024 (pre-Rev D) | low (superseded) |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value / fusion gain | proprietary | blocking | 450-750 MWe net implies burning plasma; Q can be bounded assuming ~30-40% thermal efficiency and estimated recirculating power |
| Fusion power (Rev D) | proprietary | blocking | Not stated in DPP 2025 abstract; must derive from Q + heating power assumptions |
| Thermal efficiency / power conversion cycle | not-yet-sourced | important | Steam Rankine vs. sCO2 not selected; STEP programme evaluations may bound this; ~33-40% is a reasonable analogue range |
| EC heating power level for ST-E1 | proprietary | important | Drives recirculating power fraction; can be partially bounded by requiring Q×P_fusion > P_EC + parasitic loads |
| Capital cost by subsystem | proprietary | blocking | No cost estimates in any source; must use analogue scaling from tokamak plant studies (e.g., ARIES, EUROfusion DEMO, STEP) |
| First wall / divertor lifetime | not-yet-sourced | important | Determines blanket/wall replacement frequency and maintenance cost contribution |
| Availability factor | not-yet-sourced | important | DPP 2025 notes "demonstrated compatibility with reactor-level performance and availability factor" but no number given |
| Capacity factor target | not-yet-sourced | important | Likely 85-90% based on design intent but not stated |
| Annual O&M cost | truly-unknown | important | No data; analogue from nuclear power plant O&M per GWe |
| REBCO tape cost at scale | not-yet-sourced | important | Current market price ~$10-50/m (highly variable); required quantity unknown |
| Tritium startup inventory | derivable | important | Estimable from fusion power and breeding curve assumptions |
| Plant construction timeline | derivable | nice-to-have | Drives financing costs in LCOE |

---

## Source Recommendations

1. **STEP programme system code outputs / plant studies** — `not-yet-sourced` — UKAEA's Spherical Tokamak for Energy Production programme is the closest public analogue. Published system code (PROCESS) results for STEP may provide capital cost scaling, thermal efficiency, and availability assumptions applicable to ST-E1. Search: OSTI/UKAEA publications, "STEP PROCESS power plant study" — *unverified — confirm existence before searching*.

2. **ARIES / EUROfusion DEMO capital cost databases** — `not-yet-sourced` — Conventional tokamak plant studies (ARIES-AT, EU DEMO) have detailed CAS breakdowns that can serve as analogues for magnet, blanket, vacuum vessel, and balance-of-plant costs. These are publicly available and well-established. Scaling to ST geometry requires care (different aspect ratio, no inboard blanket).

3. **Fusion power output for Rev D** — the DPP 2025 full presentation (not just abstract) likely contains more parameters than the abstract extracted in Phase 1a. The full talk by Erik Maartensson (APS DPP 2025, gm12/8) may have been recorded or slides may be available — *unverified — confirm existence before searching*.

4. **REBCO tape supply chain and cost scaling** — CFS has published some information on HTS tape quantities and costs for their magnet system. Search: "REBCO tape cost fusion magnet" or CFS ARC/SPARC magnet costing publications — *unverified — confirm existence before searching*.

5. **Pulsed tokamak power conversion and thermal storage** — Academic literature on molten salt thermal energy storage for pulsed tokamaks likely contains efficiency and cost data relevant to the ST-E1 thermal cycle problem. Search: "molten salt thermal energy storage pulsed tokamak" — *unverified — confirm existence before searching*.

6. **Tritium startup inventory and breeding curve** — The tritium fuel cycle challenge is covered in ITER and DEMO tritium studies. The "tritium start-up problem" literature (Abdou et al., various) provides conservative and optimistic scenarios. Search OSTI for "fusion tritium startup inventory breeding" — well-established published literature.

---

## Summary

**Proceed to full analysis.** The available data is sufficient for a D1+ qualitative write-up and a first-pass quantitative LCOE model with clearly stated assumptions. The key blocking gaps — Q value, fusion power, capital costs — are all amenable to bounded estimation using analogues from the broader tokamak plant study literature (ARIES, EUROfusion DEMO, STEP). Tokamak Energy's transparency on machine parameters, magnet technology, heating approach, and blanket concept gives a stronger foundation than most private fusion concepts at comparable development stage.

The two most important analogue sources to acquire before writing the quantitative model are: (1) a STEP or EU DEMO system code output for capital cost scaling, and (2) an estimate of EC heating power requirements at pilot plant scale to constrain the recirculating power fraction. Both are tractable with targeted literature search. The analysis should note that the 450-750 MWe output range is explicitly tied to "technology and physics assumptions" per Tokamak Energy — this 40% uncertainty band should be reflected directly in the LCOE sensitivity sweep.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 3
important_count: 8
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Moderate"
  system_function:            "Good (challenges well-characterized)"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Unknown"
```
