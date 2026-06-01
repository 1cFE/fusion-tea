# Gap Assessment: Dense Plasma Focus (p-B11)

## Overall Readiness
**Rating**: Significant Gaps
**Summary**: LPPFusion has a moderately transparent public record via two peer-reviewed company-authored papers and investor materials, providing good coverage of device physics and claimed performance targets. However, the concept sits at a pre-net-energy stage with no p-B11 reactions demonstrated yet, no direct conversion prototype, and no independent third-party cost analysis. A conceptual LCOE model is constructible from company claims, but every major output parameter (fusion yield, rep rate, efficiency, capital cost) rests on unverified projections rather than demonstrated results, making confidence in any LCOE estimate very low.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial

**Available**:
- Two peer-reviewed papers (Lerner et al. 2023 *J. Fusion Energy* 42:7; Lerner & Hassan 2024 *Frontiers in Physics* 12:1438880) describing DPF physics, experimental results on FF-1/FF-2B, and the path to p-B11 net energy. Both are company-authored by LPPFusion staff.
- Company investment materials: executive summary, "our plan to net energy," and technology pages (iter-02 sources) provide commercial targets, timelines, and high-level cost claims.
- 60+ years of academic DPF literature provides context on the device class (referenced throughout Lerner 2023).
- Wurzel & Hsu 2021 (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) provides independent context: they explicitly note that for DPF "it is not feasible to report a reliable, achieved Lawson parameter or triple product" due to non-Maxwellian ion distributions — confirming that standard physics-progress benchmarking cannot be applied to DPF.
- US Patent #7,482,607 covers the DPF design with angular momentum control and direct conversion concept (referenced in sources but not extracted).

**Missing**:
- No independent third-party engineering or cost study of Focus Fusion has been published
- No government or national-lab assessment of LPPFusion's approach
- No power plant design study from any organization other than LPPFusion
- The Lerner 2011 *J. Fusion Energy* 30:367 paper (cited in dossier as containing the original conceptual power plant design) is referenced but not captured in the source set
- No peer-reviewed paper from independent researchers experimentally validating QMFE in DPF conditions

**Gaps**:
- No independent cost or engineering study — `not-yet-sourced` — **important**
- Key 2011 Lerner power plant design paper not extracted — `not-yet-sourced` — **important**
- No third-party validation of QMFE in DPF — `truly-unknown` (no independent experiment has confirmed this) — **blocking**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**: The sources document the main physical mechanism clearly (pulsed capacitor bank → current sheath → filament instability → plasmoid formation → ion beam + x-ray emission → direct conversion). Lerner 2023 describes the theoretical model quantitatively (scaling laws for yield vs. current, plasmoid radius, density). The energy conversion pathway is described conceptually (ion beam decelerator at ~85% efficiency from accelerator analogy; x-ray photoelectric converter at ~80% claimed efficiency).

**Missing and hard to model**:
1. **QMFE physics** is the linchpin of p-B11 viability. Simulations show it reduces bremsstrahlung by up to 5× at Bc ~10 GG. These field strengths have never been measured in any laboratory — they would be the highest ever achieved. No independent experimental confirmation exists.
2. **Shot-to-shot variability** is identified as a major inherent challenge (Lerner 2023: sensitivity to initial angular momentum means small perturbations cause large yield swings). Intrinsic irreproducibility makes capacity factor modeling extremely difficult.
3. **p-B11 reactions have never been observed in FF-2B** (as of 2024 Frontiers paper: preparations are "nearly complete"). The entire commercial pathway depends on achieving this first.
4. **Direct energy conversion subsystems** have never been built at any scale. Ion beam decelerator concept borrows from particle accelerator technology (~85% efficiency demonstrated in accelerator context), but adaptation to a fusion device is unproven. X-ray photoelectric converter has no prototype.
5. **Yield scaling model reliability**: The I⁴ yield scaling has plateaued above 1 MA for 20+ years across multiple DPF devices. LPPFusion attributes this to impurity-driven filament disruption and oscillations, and claims resolution is in progress, but the plateau is a documented empirical observation that calls yield projections into question.

**Gaps**:
- QMFE experimental confirmation absent — `truly-unknown` — **blocking**
- p-B11 reactions not yet achieved in DPF — `truly-unknown` (no external source can fill this) — **blocking**
- Direct conversion efficiency unmeasured — `not-yet-sourced` (LPPFusion may have internal estimates; patent gives conceptual design only) — **blocking**
- Yield plateau mechanism not fully resolved — `truly-unknown` — **blocking**
- Shot-to-shot variability statistics for commercial projection — `proprietary` — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **DPF device (capacitor bank + electrodes)**: TRL 5. FF-2B demonstrated 2.7 MA single-shot operation. Beryllium electrodes installed 2019. Device cost ~$500k (Lerner 2024 Frontiers).
- **Plasma purity control**: TRL 5-6 for D fuel. World-record zeff = 1.004 achieved (Lerner 2023). Represents a genuine experimental achievement.
- **Decaborane fuel handling**: TRL 3-4. Isotopically pure fuel procured (93g for ~$56,000 = $600/g), handling and exhaust systems installed (Lerner 2024 Frontiers). No actual shots yet.
- **Diamond photoconductive switches**: TRL 3. Two sources (compoundsemiconductor-119149; ipo-ipo-technologies) document prototype development at University of Illinois and LLNL. LLNL device shows 44 A/cm², ~20% efficiency, ~50 kW output. These are critical for reliable high-rep-rate switching but are at TRL 3 — no commercial product.

**Missing**:
- **High-rep-rate operation (~200 Hz)**: Never demonstrated at fusion-relevant conditions. Singular data point is NX2 (Singapore) at 16 Hz for a small X-ray DPF — very different operating regime. TRL 1-2 for the commercial rep rate.
- **Ion beam decelerator**: TRL 2. Concept exists in patent. No fusion-scale prototype. Accelerator deceleration technology is mature, but the specific geometry and power levels for DPF have never been built.
- **X-ray photoelectric converter**: TRL 1-2. No prototype of any kind. Only described in the patent and conceptually in Lerner 2023. Calculated efficiency ~80%, but "such a device has never been made" (Lerner 2023, §Steps from Net Energy).
- **Helium cooling at 10 kW/cm²**: TRL 2-3. Calculated to be feasible (Lerner 2023). Not experimentally demonstrated for DPF anode cooling.
- **Electrode erosion at 200 Hz**: Entirely unknown. Lerner 2023 states electrode replacement target of "no more than once a month" but gives no experimental basis. This is a critical O&M cost driver.

**Gaps**:
- 200 Hz operation undemonstrated — `truly-unknown` — **blocking**
- X-ray photoelectric converter prototype absent — `truly-unknown` — **blocking**
- Ion beam decelerator for DPF unbuilt — `not-yet-sourced` (literature on accelerator-based direct conversion exists; TRL uplift path unclear) — **important**
- Electrode erosion rate at rep-rated operation — `truly-unknown` — **important**
- Diamond switch scale-up to commercial power level — `not-yet-sourced` — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **Boron-11 (natural)**: Abundant. "Switching fully to a Focus Fusion economy would require only about a 10% increase in boron production" (Lerner 2023). Not a supply concern at any scale.
- **Boron-11 (isotopically pure)**: Isotopically pure B-11 in decaborane form exists but is custom laboratory-scale production at $600/g (iter-02 sources, lppfusion-proton-boron-p11b-fuel-arrives). Mass production pathway would reduce cost enormously per Lerner, but no industrial supplier has been identified publicly.
- **Beryllium**: Identified as a critical material. Current global production ~400 t/year. Lerner 2023 estimates ~10× scale-up needed for a fully deployed Focus Fusion economy. Beryllium is not rare (comparable to lead in Earth's crust) but requires expensive, specialized processing due to high toxicity. Limited number of producers globally (primarily Materion in the US).
- **Hydrogen (protons)**: Trivially abundant.

**Missing**:
- No supply chain analysis for isotopically pure B-11 at commercial scale. The lppfusion-proton-boron-p11b-fuel-arrives source notes that the 93g lot was made at two separate labs (Russia + Czech Republic) as a "custom item" — no industrial supplier identified.
- No beryllium electrode fabrication cost at scale.
- No assessment of diamond material supply for switching at commercial scale.
- No analysis of electrode material cycling (beryllium dust/erosion/recycling).

**Gaps**:
- Commercial-scale isotopically pure B-11 supply chain — `not-yet-sourced` — **important**
- Beryllium production scale-up economics — `not-yet-sourced` — **important**
- Beryllium toxicity / manufacturing handling costs — `not-yet-sourced` — **nice-to-have**
- Diamond switch manufacturing supply chain — `not-yet-sourced` — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Device capital cost (unit) | <$1M ($0.10/W) | Lerner 2023 JFE (company claim) | l |
| Electrical output per unit | 5 MW net | Lerner 2023 JFE (calculated) | l |
| Rep rate target | ~200 Hz | Lerner 2023 JFE / website | l |
| Fusion energy per pulse | ~25 kJ net | Lerner 2023 JFE (calculated) | l |
| Fuel cost | ~$0/kWh (5 kg/yr) | Lerner 2023 JFE | m |
| Current device cost (FF-2B) | ~$500k | Lerner 2023 JFE | h |
| Ion beam decelerator efficiency | ~85% (analog) | Lerner 2023 JFE (accelerator literature analogy) | l |
| X-ray converter efficiency | ~80% (theoretical) | Lerner 2023 JFE (calculated) | l |
| Electrode cooling rate target | ≤10 kW/cm² | Lerner 2023 JFE (calculated) | l |
| Overall claimed LCOE | ~0.3 c/kWh | Lerner 2023 JFE (company estimate) | l |
| Device mass | ~3 tons | Lerner 2023 JFE | m |
| Electrode replacement interval target | ~monthly | Lerner 2023 JFE (target) | l |
| Isotopically pure B-11 fuel cost (lab) | $600/g (lab scale) | lppfusion-proton-boron-p11b-fuel-arrives | h |
| Physics energy budget (net energy threshold) | ~30 kJ/pulse | lppfusion-our-plan-to-net-energy | m |
| Engineering phase budget | ~$100M | Lerner 2023 JFE / net energy plan | l |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Demonstrated fusion yield (p-B11) | truly-unknown | blocking | Zero — no p-B11 shots yet; D yield is ~0.25 J vs. 30 kJ target |
| Direct conversion system capital cost | truly-unknown | blocking | No design study; patent describes concept only |
| Balance of plant capital cost | not-yet-sourced | blocking | No design; no direct conversion BOP analog exists in published literature |
| Capacity factor | truly-unknown | blocking | No rep-rate operation demonstrated; no reliability data |
| Electrode replacement cost at 200 Hz | truly-unknown | important | Erosion rate unknown; drives O&M strongly |
| Cooling system capital cost | not-yet-sourced | important | He cooling at 10 kW/cm² for DPF tip — no design study |
| Isotopically pure B-11 cost at scale | not-yet-sourced | important | Currently lab-scale only; mass-production cost unquantified |
| O&M labor rate | not-yet-sourced | important | "Some maintenance every month" — no man-hours or cost breakdown |
| Grid interconnection / BOP electrical | not-yet-sourced | important | For 5 MW modular unit; no design study |
| Decommissioning / radioactive waste | derivable | nice-to-have | Minimal (trace C-11, minimal Be activation); low but non-zero |
| Scaling Q or nτ for p-B11 | truly-unknown | blocking | Wurzel & Hsu 2021 confirm DPF cannot be placed on Lawson criterion plot — no reliable Q estimate exists |

---

## Source Recommendations

1. **Lerner, E.J., Murali, S.K., Haboub, A. (2011)** *J. Fusion Energy* **30**, 367 — Contains the original conceptual power plant design, full parameter table, and cost estimates that are the basis for all subsequent LPPFusion cost claims. Cited in dossier. **Search**: Search SpringerLink for DOI 10.1007/s10894-010-9380-7. `not-yet-sourced` — confirm existence before treating as accessible.

2. **US Patent #7,482,607** (Method and apparatus for producing x-rays, ion beams, and nuclear fusion energy) — Contains the ion beam decelerator and x-ray photoelectric converter design. Publicly accessible via USPTO. `not-yet-sourced`.

3. **DPF review literature for independent assessment** — Scholz et al. 2019 (*J. Fusion Energy* 38:522) is cited in the Frontiers 2024 paper and assesses p-B11 feasibility in DPF. Search OSTI or Springer for this paper. `not-yet-sourced` — may provide independent physics assessment of whether QMFE conditions are achievable.

4. **NX2 device technical reports (Singapore Institute of Manufacturing Technology / NUSE group)** — NX2 has demonstrated 16 Hz DPF operation as an X-ray source. Engineering data on electrode lifetime and rep-rate operation would directly inform O&M and capacity factor estimates for Focus Fusion. **Search**: OSTI, NTU Singapore repositories. `not-yet-sourced` — confirm existence; papers may be sparse.

5. **Abolhasani et al. (2013)** *J. Fusion Energy* **32**, 189 — Cited in Lerner 2023 as independent QMFE study finding "fusion yield approximately 6× the input energy." This is one of the only independent QMFE assessments. Would strengthen or challenge the theoretical basis. `not-yet-sourced`.

**Fleet-wide source disqualifications:**

- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Not opened; disqualified without opening — DPF uses direct conversion, no blanket, no tritium, no superconducting magnets. D-T MFE cost structure shares zero subsystems with DPF. No applicable cost analogues.
- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Not directly applicable as a cost analog. DPF has no CAS22 magnets, no CAS23 blanket, no CAS24 shielding, and no CAS26 thermal cycle. The CAS framework could structure a DPF LCOE analysis in principle, but no ARIES-style subsystem costs map onto this device architecture.
- **ARPA-E ALPHA Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened. Four concepts analyzed: Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-stabilized Z-Pinch — DPF not included. Targets ~500 MWe at ~$2.4/W CapEx and ~$43/MWh LCOE. DPF targets 5 MW at <$1M/unit (~$0.20/W) via direct conversion — fundamentally different scale and architecture. No applicable cost analog for DPF's unique subsystems. Disqualified for this concept.
- **Simplified IFE economic model (Hawker)** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Opened. Fourteen-parameter model built around IFE driver energy, target gain, rep rate, and thermal conversion efficiency. DPF has no thermal conversion cycle, and the "driver" is indistinguishable from the reactor chamber. Methodology provides a conceptual template for pulsed-device LCOE parameterization, but no numerical values transfer directly. Disqualified as a quantitative analog; may provide methodological inspiration only.
- **Wurzel & Hsu 2021** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Opened and integrated. Explicitly discusses DPF: "it is not feasible to report a reliable, achieved Lawson parameter or triple product" for DPF because of non-Maxwellian distributions. This confirms that the Lawson-criterion gap for DPF is not merely unmeasured but fundamentally uncharacterizable by standard methods — the physics gap (§2 blocking) is more severe than for any other concept in the portfolio. Integrated into §2.
- **Helios stellarator, HIF economics, energy from IFE, accelerators for IFE, AMPS, Xcimer, ORNL assessment**: Disqualified without opening — none address DPF device physics, direct conversion at this scale, or p-B11 aneutronic fuel cycles in an applicable way.

---

## Summary

The Dense Plasma Focus (p-B11) concept is **constructible as a D1+ analysis** — LPPFusion's published papers and investment materials provide sufficient stated parameters to build a parameterized LCOE model. However, the analysis would be almost entirely composed of company claims with no independent verification, and the underlying physics (p-B11 ignition via QMFE, direct conversion efficiency, 200 Hz rep rate) has not been experimentally demonstrated at any scale. The concept has five blocking gaps: p-B11 reactions undemonstrated, QMFE unconfirmed, direct conversion efficiency unmeasured, 200 Hz rep rate undemonstrated, and no credible Q estimate. The most important additional source to acquire before D1+ analysis is Lerner 2011 *J. Fusion Energy* (the original power plant design paper), Abolhasani et al. 2013 (independent QMFE confirmation), and the LPPFusion patent. The analysis can proceed now but must be heavily caveated as speculative given the concept's pre-ignition status; the back-solve to $0.01/kWh is feasible because the company's own numbers are remarkably optimistic.

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 5
important_count: 9
counting_method: "deduplicated across all sections: (blocking) p-B11 unrealized, QMFE unconfirmed, direct conversion unmeasured, 200Hz undemonstrated, Q/Lawson uncharacterizable; (important) no independent cost study, no plant design, no BOP cost, electrode erosion unknown, diamond switch unscaled, B11 supply chain unestablished, capacity factor unknown, ion beam decelerator unbuilt, O&M costs unquantified"
section_coverage:
  availability_of_data:       "Partial"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Poor"
```