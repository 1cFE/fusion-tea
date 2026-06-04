# Gap Assessment: Sheared-Flow Stabilized Z-Pinch (D-T)

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The SFS Z-pinch is unusually well-documented for a pre-commercial fusion concept. The Engineering Paradigms paper (Thompson et al., FST 2023) provides a coherent conceptual plant design with nominal power parameters, energy balance logic, and qualitative cost drivers. The ARPA-E ALPHA concepts study (Woodruff Scientific, 2020) explicitly costed the Zap Energy flow-stabilized Z-pinch alongside three other concepts, providing a CAS-structured LCOE benchmark (~$43/MWh for a ~500 MWe plant) even though concept-specific figures were delivered proprietary. The main gap is physics maturity: FuZE-3's best result (1.6 GPa pressure, ~1 keV electron temperature) is still orders of magnitude below the plant-relevant conditions (35 keV, Q > 10) assumed in the conceptual design, and no published Q estimates from experiments exist. Most cost-model parameters are derivable from published conceptual design values, but the critical pulsed power driver cost is highly uncertain and likely proprietary.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Full conceptual plant design paper (Thompson et al., FST 2023) covering plasma parameters at each development step, plant architecture, blanket concept, and efficiency rationale. Open access.
- ARPA-E ALPHA concepts costing study (Woodruff Scientific 2020) explicitly includes Zap Energy's flow-stabilized Z-pinch; provides anonymized CAS-level cost averages across four pulsed modular concepts as a benchmark.
- Experimental device progression (FuZE → FuZE-Q → FuZE-3) documented via press releases and APS DPP abstracts.
- Century demo platform documented: 100 kW input power, 0.2 Hz, 500 kA, liquid bismuth wall, press releases confirm 50 MWe per module as Zap's stated plant target.
- OSTI pulsed power roadmap (2025) characterizes pulsed power component supply chain gaps directly relevant to Z-pinch driver systems.
- Zap Energy company: ~$330M raised, ~150 employees, DOE Milestone-Based Fusion Development Program participant — high corporate transparency relative to most alt-fusion startups.

**Missing**:
- Full text of paywalled key papers (Thompson FST 2023 — obtained via extracted PDF; Physics of Plasmas 2023 overview paper — NOT in sources; Century FST 2025 paper — NOT in sources beyond press release snippets).
- The Physics of Plasmas 2023 paper (Levitt et al.) likely contains updated plasma physics basis but only the APS DPP 2025 abstract is available.

**Gaps**:
- Full text of Physics of Plasmas 2023 overview paper — `not-yet-sourced` — nice-to-have (Thompson FST 2023 covers most content)
- Full text of Century FST 2025 paper — `not-yet-sourced` — important (engineering platform details for plant power handling subsystems)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Thompson FST 2023 provides clear system function description: pulsed axial current → pinch → ohmic heating → fusion → LiPb absorbs energy → steam Rankine cycle. No external magnets, no auxiliary heating.
- Wall-plug to plasma electrical efficiency ~70% explicitly documented (AC-DC rectification ~90%, pulsed power modulator ~80%).
- Pulsed operation analogy to internal combustion engine clearly articulated; load-following capability described.
- Recirculating power discussion: tokamaks cited at 0.4-0.6 recirculating fraction; SFS Z-pinch argued to be lower due to direct coupling.
- Engineering Paradigms paper identifies cathode as the primary materials challenge (direct plasma contact, neutron bombardment); all other solid structure shielded by LiPb.
- OSTI pulsed power roadmap (2025) characterizes the key engineering challenge for all pulsed-power-driven fusion: high-voltage capacitor lifetime (currently 10⁴–10⁵ shots; plant needs 10⁹), solid-state switching for 50–200 kV at repetitive rates, and lead time for large-volume capacitor orders (4–6 years; 10,000–216,000 capacitors per plant).

**Missing**:
- The path from 0.2 Hz (Century current) to 10 Hz (commercial target) involves a ~50× increase in average input power, from ~100 kW to ~10 MW per module. The engineering challenges of this scaling are acknowledged but not quantified in published sources.
- Tritium handling and extraction from LiPb at continuous-operation rates is not described in detail in public sources.
- Actual recirculating power fraction at plant conditions: stated qualitatively as "better than tokamaks" but no published number.

**Gaps**:
- Recirculating power fraction (quantitative) — `proprietary` — important (critical for net electric efficiency calculation)
- Rep-rate scaling from 0.2 Hz to 10 Hz engineering solution — `proprietary` — important (determines capacity factor trajectory)
- Tritium extraction process details from LiPb — `not-yet-sourced` — nice-to-have (LiPb tritium extraction literature exists from ITER blanket studies)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- Plasma physics (TRL 3–4): FuZE-3 demonstrated 1.6 GPa total pressure, ~1 keV electron temperature, 3–5×10²⁴ m⁻³ density. Thermonuclear neutron production confirmed on FuZE (Zhang et al., PRL 2019). Still ~2 orders of magnitude below plant-relevant plasma conditions.
- Pulsed power driver (TRL 4): Solid-state thyristor switches demonstrated at 80% efficiency at 5 Hz (Hegeler et al., 2011, cited in Thompson FST 2023). Century testing at 0.2 Hz with 100 kW. Path to 10 Hz and 10 MW per module not yet demonstrated.
- Liquid metal wall (TRL 3–4): Century is "one of the largest tests of a plasma-facing liquid metal blanket to date." Liquid bismuth used in Century (not LiPb). 1,080 consecutive shots demonstrated.
- Cathode durability (TRL 2–3): Identified as key challenge. Decades of arc smelting furnace experience cited as analogy (60 MW, non-nuclear). No direct testing at plant-relevant neutron flux.
- Blanket/breeding (TRL 2–3): TBR ~1.1 calculated for LiPb; Monte Carlo simulations only. Not tested with actual D-T neutron flux.
- Pulsed power supply chain (TRL 2–3): OSTI 2025 roadmap explicitly identifies this as a blocking supply chain gap across all pulsed fusion concepts; capacitor lifetime and solid-state switch development are pre-commercial.

**Missing**:
- Q > 1 demonstration: Current experiments are sub-breakeven by orders of magnitude. No published estimate of when Q > 1 is expected.
- TRL assessment for the LiPb tritium breeding system under actual neutron irradiation.

**Gaps**:
- Q > 1 / scientific breakeven demonstration — `truly-unknown` (hasn't happened yet) — blocking (required to anchor any cost model Q assumption)
- Cathode lifetime under DT-relevant neutron flux — `proprietary` — important (drives scheduled replacement cost, major O&M driver)
- Capacitor/switch lifetime at 10 Hz, 10⁹ shots — `truly-unknown` at required spec — blocking (supply chain fundamentally not ready per OSTI 2025 roadmap; no commercial product at required lifetime)
- LiPb tritium breeding tested under neutron flux — `truly-unknown` (only Monte Carlo calculations) — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- LiPb eutectic (17% Li, 83% Pb): Properties documented; neutron multiplication via Pb(n,2n) reaction leveraged for TBR ~1.1. Activation products (²¹⁰Po, ²⁰³Hg) identified; ²⁰³Hg mitigable by isotope control. No superconducting magnets — eliminates dominant ITER/tokamak material cost driver.
- Cathode material: Unspecified in published sources; arc smelting analogs cited. Copper or graphite-based analogues likely but not confirmed.
- Capacitor dielectrics: OSTI 2025 roadmap characterizes current BOPP film capacitors at 1–3 J/cm³ energy density, 10⁴–10⁵ shot lifetime; advanced films (Peak Nano NanoPlex) could reduce volume by 4–8×. 10 year–15 year valley-of-death for new dielectric scale-up.
- OSTI 2025: "If 150 fusion power plants were to be built today to service the United States, the time required to build the required capacitors is approximately 125–250 years given western world available manufacturers." Directly characterizes the Z-pinch supply chain bottleneck.
- Solid-state switches: WBG materials (SiC MOSFETs at 6.5–10 kV commercial; custom at 15–20 kV); target 100–200 kV/100–200 kA switches do not currently exist.

**Missing**:
- Lithium-6 enrichment needs for LiPb with adequate TBR — not explicitly stated in sources.
- Lead supply chain: Lead is abundant but specific isotope or purity requirements not stated.
- Structural material (first-wall surroundings, tank): Not specified in published sources.

**Gaps**:
- Cathode material specification and supply chain — `proprietary` — nice-to-have (small mass, replaceable)
- Li-6 enrichment fraction needed for TBR — `not-yet-sourced` — important (affects tritium self-sufficiency)
- High-rep-rate solid-state switch supply chain at 100–200 kV/100–200 kA — `truly-unknown` at required spec — blocking for commercial plant (per OSTI 2025 roadmap)
- Capacitor supply chain at 10⁹ shot lifetime — `truly-unknown` at required spec — blocking for commercial plant

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Thermal power per core | ~200 MWt | Thompson FST 2023, Table I | h |
| Net electric power per module | ~50 MWe | Century press release (Zap) | m |
| Net electric power (plant, 3–4 modules) | ~383–814 MWe | ARPA-E ALPHA (Woodruff 2020), Table 2 | m |
| Repetition rate (commercial target) | 10 Hz | Thompson FST 2023, Zap website | h |
| Fusion energy per pulse | 19 MJ | Thompson FST 2023, Table I | m |
| Plant Q (fusion power / input power) | > 10 | Thompson FST 2023 | m |
| Wall-plug to plasma efficiency | ~70% | Thompson FST 2023 (AC-DC ~90%, modulator ~80%) | h |
| Energy conversion cycle | Steam Rankine | Thompson FST 2023, Ben Bridger blog | h |
| Tritium breeding ratio | ~1.1 | Thompson FST 2023 (Monte Carlo only) | m |
| Plant availability / capacity factor | 90% | ARPA-E ALPHA (Woodruff 2020, costing assumption) | m |
| Total Capital Cost (benchmark, ~500 MWe 4-concept avg) | $1.2B avg ($0.8–1.6B range) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
| CapEx (benchmark) | ~2.4 $/W ($2.0–3.3) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
| LCOE (benchmark, learning-curve COE2) | ~43 $/MWh ($34–54 range) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
| O&M costs (benchmark) | ~48 M$/year ($42–61) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
| Scheduled replacement costs (benchmark) | ~17 M$/year ($6–30) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
| Power supplies CAS 22.1.7 (benchmark) | $55.8M avg ($11.9–140.4M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
| First wall/blanket CAS 22.1.1 (benchmark) | $57.3M avg ($3.6–116.5M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
| Special materials CAS 27 (LiPb, benchmark) | $103.1M avg ($1.4–266.9M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
| Fuel cost | ~negligible | ARPA-E ALPHA (Woodruff 2020) ~$0.1M/yr | h |

*Note: ARPA-E ALPHA values are anonymized averages across four concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, and Flow-stabilized Z-Pinch). Zap Energy-specific CAS line items were delivered proprietary. Low confidence for Z-pinch-specific cost application.*

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net thermal-to-electric efficiency (quantitative) | derivable | blocking | 50 MWe / 200 MWt implies ~25% gross, but recirculating power fraction unknown; net unclear |
| Recirculating power fraction | proprietary | blocking | Thompson FST 2023 argues "better than tokamaks" (0.4–0.6) but gives no number; plant Q > 10 implies substantial recirculation headroom |
| Capital cost breakdown (Z-pinch specific, CAS 22.1.7 pulsed power driver) | proprietary | blocking | Widest cost range in ALPHA study ($11.9–140.4M for power supplies) — Zap's specific value proprietary |
| Cathode replacement schedule and unit cost | proprietary | important | Dominant scheduled replacement cost driver; only qualitative treatment in published sources |
| LiPb loop cost (pumps, heat exchangers, tritium extraction) | derivable | important | ITER/DEMO LiPb loop engineering studies exist; LiPb is common blanket material |
| Plant scaling: modules per plant, shared infrastructure | proprietary | important | Thompson FST 2023 mentions multi-module plants sharing tritium infrastructure but no specific module count or cost allocation |
| Capacity factor trajectory to commercial operation | proprietary | important | Century at 0.2 Hz; commercial at 10 Hz — no published ramp schedule or first-plant CF estimate |
| O&M staffing and annual costs (Z-pinch specific) | derivable | important | Could use ARPA-E ALPHA analog ($48M/yr) scaled to single-concept estimates |
| Physics performance gap to plant conditions | truly-unknown | blocking | 1.6 GPa / ~1 keV (FuZE-3) vs. 35 keV / Q > 10 required; 2+ orders of magnitude in T, ~3 in density |

---

## Source Recommendations

1. **Physics of Plasmas 2023 — "The Zap Energy approach to commercial fusion" (Levitt et al.)** — `not-yet-sourced`. This appears to be the primary peer-reviewed overview paper for the commercialization strategy. DOI: 10.1063/5.0211179 (AIP). May be open-access or available via OSTI. Search OSTI for the DOI. Would improve physics basis section.

2. **Century FST 2025 paper** — `not-yet-sourced`. Full engineering platform paper. DOI: 10.1080/15361055.2025.2532331 (Taylor & Francis). Likely paywalled; check if OSTI preprint available. Would provide quantitative Century performance data (shot count, thermal load, electrode erosion rates).

3. **FuZE-3 journal publication (planned for 2026 per Zap press release)** — `not-yet-sourced` (paper announced but not yet published as of research date). Monitor arXiv physics.plasm-ph for Zap Energy FuZE-3 results. Would provide triple product data at 1 keV / high density.

4. **ARPA-E ALPHA proprietary Z-pinch costing report** — `proprietary`. The Woodruff Scientific study delivered a proprietary CAS-level cost breakdown to Zap Energy. Not publicly available. The public report provides only four-concept anonymized averages. A future public release (e.g., DOE report database) is possible; search OSTI for Woodruff/Zap/ALPHA updates.

5. **ITER/DEMO LiPb blanket engineering literature** — `not-yet-sourced`. Published LiPb loop cost scaling models from ITER and DEMO studies could provide analogous cost for LiPb heat transfer system (CAS 22.2 / 27). Search OSTI for "LiPb blanket cost" or "lithium lead tritium extraction cost."

6. **Zap Energy DOE Milestone-Based Fusion Development Program milestone reports** — `not-yet-sourced`. DOE FES Milestone reports may contain performance data and cost projections. Search DOE FES website and OSTI for Zap Energy milestone program deliverables (`unverified — confirm existence before searching`).

---

## Summary

The SFS Z-pinch is **ready for a D1+ qualitative analysis** and a **partial quantitative analysis**. The engineering concept is exceptionally well-articulated for its development stage — Thompson FST 2023 provides the most detailed public plant design of any pre-commercial alt-fusion concept in this project. The ARPA-E ALPHA study provides a CAS-structured LCOE estimate (~$43/MWh) directly applicable as a benchmark for the concept, though Zap-specific cost line items are proprietary. The main qualitative caveat — which should be prominently flagged in the analysis — is that demonstrated physics performance (1.6 GPa, ~1 keV) remains far from plant conditions (35 keV, Q > 10), making any cost model highly sensitive to whether sheared-flow stabilization holds at MA-scale currents. The pulsed power supply chain (capacitor lifetime, solid-state switch availability) is a genuinely blocking commercialization constraint identified by the 2025 OSTI roadmap. Proceed to full analysis with explicit uncertainty framing on: (1) physics extrapolation from current experiments to breakeven, (2) pulsed power driver cost (widest CAS variance in the ALPHA study), and (3) recirculating power fraction.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 4
important_count: 6
counting_method: "section_5_missing_parameters_plus_sections_3_4_deduplicated: physics_gap_to_plant_conditions, net_electric_efficiency, pulsed_power_driver_cost (all blocking); capacitor_lifetime and solid_state_switch_availability collapsed into single supply_chain blocking gap from sections 3+4"
section_coverage:
  availability_of_data:       "Good"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial"
```