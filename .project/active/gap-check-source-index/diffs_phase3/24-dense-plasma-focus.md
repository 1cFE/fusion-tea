# Phase 3 diff: 24-dense-plasma-focus

**Generated:** 2026-05-22T15:19:14-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 7 | 5 | -2 |
| important_count  | 6 | 9 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have enough information to write the full gap assessment. I'll compile it from all the sources read.
```

## Blocking-tier lines (new)

```
33:- No third-party validation of QMFE in DPF — `truly-unknown` (no independent experiment has confirmed this) — **blocking**
50:- QMFE experimental confirmation absent — `truly-unknown` — **blocking**
51:- p-B11 reactions not yet achieved in DPF — `truly-unknown` (no external source can fill this) — **blocking**
52:- Direct conversion efficiency unmeasured — `not-yet-sourced` (LPPFusion may have internal estimates; patent gives conceptual design only) — **blocking**
53:- Yield plateau mechanism not fully resolved — `truly-unknown` — **blocking**
75:- 200 Hz operation undemonstrated — `truly-unknown` — **blocking**
76:- X-ray photoelectric converter prototype absent — `truly-unknown` — **blocking**
131:| Demonstrated fusion yield (p-B11) | truly-unknown | blocking | Zero — no p-B11 shots yet; D yield is ~0.25 J vs. 30 kJ target |
132:| Direct conversion system capital cost | truly-unknown | blocking | No design study; patent describes concept only |
133:| Balance of plant capital cost | not-yet-sourced | blocking | No design; no direct conversion BOP analog exists in published literature |
134:| Capacity factor | truly-unknown | blocking | No rep-rate operation demonstrated; no reliability data |
141:| Scaling Q or nτ for p-B11 | truly-unknown | blocking | Wurzel & Hsu 2021 confirm DPF cannot be placed on Lawson criterion plot — no reliable Q estimate exists |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/24-dense-plasma-focus.md	2026-05-22 12:59:21.080505504 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/gap_report.md	2026-05-22 15:19:14.955877719 -0700
@@ -1,12 +1,10 @@
-I now have sufficient information to write the gap assessment. Let me compile the report.
-
----
+I now have enough information to write the full gap assessment. I'll compile it from all the sources read.
 
 # Gap Assessment: Dense Plasma Focus (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-**Summary**: Public physics literature (Lerner 2023 JFE, Lerner 2024 Frontiers) provides good qualitative coverage of the DPF device, confinement mechanism, and experimental results, supporting a solid narrative write-up. However, quantitative LCOE analysis faces severe structural problems: all cost projections originate from company promotional materials, assume undemonstrated physics (QMF effect enabling p-B11 net energy), and rely on mass-production cost models for hardware that does not yet exist as a prototype. The two most capital-cost-relevant subsystems — the direct energy conversion systems (ion beam decelerator and x-ray photovoltaic converter) — have no prototypes, no measured efficiencies, and no cost analogues anywhere in the public literature.
+**Summary**: LPPFusion has a moderately transparent public record via two peer-reviewed company-authored papers and investor materials, providing good coverage of device physics and claimed performance targets. However, the concept sits at a pre-net-energy stage with no p-B11 reactions demonstrated yet, no direct conversion prototype, and no independent third-party cost analysis. A conceptual LCOE model is constructible from company claims, but every major output parameter (fusion yield, rep rate, efficiency, capital cost) rests on unverified projections rather than demonstrated results, making confidence in any LCOE estimate very low.
 
 ---
 
@@ -16,44 +14,44 @@
 **Coverage**: Partial
 
 **Available**:
-- Two recent peer-reviewed papers by Lerner et al.: the 2023 JFE comprehensive review and 2024 Frontiers preparations paper. Both are open access and contain substantial technical detail on plasma physics, experimental results, and the path to net energy.
-- Company website (lppfusion.com) provides technology descriptions, investor materials, and high-level cost claims.
-- Broad DPF literature base from 60 years of international DPF research (referenced in Lerner 2023), though not directly ingested.
-- Patent US #7,482,607 covers the key design innovations (small anode radius, angular momentum control, direct conversion concept) but the full text was not captured.
+- Two peer-reviewed papers (Lerner et al. 2023 *J. Fusion Energy* 42:7; Lerner & Hassan 2024 *Frontiers in Physics* 12:1438880) describing DPF physics, experimental results on FF-1/FF-2B, and the path to p-B11 net energy. Both are company-authored by LPPFusion staff.
+- Company investment materials: executive summary, "our plan to net energy," and technology pages (iter-02 sources) provide commercial targets, timelines, and high-level cost claims.
+- 60+ years of academic DPF literature provides context on the device class (referenced throughout Lerner 2023).
+- Wurzel & Hsu 2021 (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) provides independent context: they explicitly note that for DPF "it is not feasible to report a reliable, achieved Lawson parameter or triple product" due to non-Maxwellian ion distributions — confirming that standard physics-progress benchmarking cannot be applied to DPF.
+- US Patent #7,482,607 covers the DPF design with angular momentum control and direct conversion concept (referenced in sources but not extracted).
 
 **Missing**:
-- Independent peer-reviewed cost analysis or plant study. All cost figures come from the company itself.
-- Full text of Lerner (2011) J. Fusion Energy 30:367 — the earliest quantitative power plant conceptual design paper, referenced in the dossier as the likely source of engineering specs (input energy per shot, capacitor bank sizing for the commercial device).
-- Third-party assessment of the QMF effect claim and whether bremsstrahlung suppression is sufficient for p-B11 gain >1.
-- DPF experiment results at fusion-relevant conditions from other international groups for benchmarking.
+- No independent third-party engineering or cost study of Focus Fusion has been published
+- No government or national-lab assessment of LPPFusion's approach
+- No power plant design study from any organization other than LPPFusion
+- The Lerner 2011 *J. Fusion Energy* 30:367 paper (cited in dossier as containing the original conceptual power plant design) is referenced but not captured in the source set
+- No peer-reviewed paper from independent researchers experimentally validating QMFE in DPF conditions
 
 **Gaps**:
-- No independent techno-economic analysis of DPF/Focus Fusion — `truly-unknown` (no external group has published one) — **important**
-- Lerner (2011) commercial design paper not captured — `not-yet-sourced` — **important** (likely contains device engineering specs for the commercial-scale unit)
+- No independent cost or engineering study — `not-yet-sourced` — **important**
+- Key 2011 Lerner power plant design paper not extracted — `not-yet-sourced` — **important**
+- No third-party validation of QMFE in DPF — `truly-unknown` (no independent experiment has confirmed this) — **blocking**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (qualitative); Poor (quantitative)
+**Coverage**: Partial
 
-**Available**:
-- The Lerner 2023 JFE paper provides an unusually candid account of current experimental failures: yield plateau at >1 MA peak current (unresolved for 20+ years), filament disruption by high-frequency oscillations, switch reliability problems. The factor-of-120,000 gap between current yield (0.25 J) and net-energy target (30 kJ) is explicitly stated.
-- The QMF effect mechanism (bremsstrahlung suppression via ultra-strong magnetic fields) is described in detail; its validity is the central physics bet. Only 0-D simulations exist; no 2-D validated model (Lerner 2023 notes a 2-D model is in progress).
-- The energy capture architecture is described qualitatively: ion beam enters a coil-based "decelerator" (analogous to linear accelerator in reverse), x-rays hit a multilayer photoelectric converter.
-- The cooling challenge at the anode tip (up to 10 kW/cm²) is explicitly flagged as a primary engineering challenge.
-- Repetition rate target (200 Hz) is derived from a thermal-cooling-limited argument, not from operational demonstration.
+**Available**: The sources document the main physical mechanism clearly (pulsed capacitor bank → current sheath → filament instability → plasmoid formation → ion beam + x-ray emission → direct conversion). Lerner 2023 describes the theoretical model quantitatively (scaling laws for yield vs. current, plasmoid radius, density). The energy conversion pathway is described conceptually (ion beam decelerator at ~85% efficiency from accelerator analogy; x-ray photoelectric converter at ~80% claimed efficiency).
 
-**Missing**:
-- Validated efficiency for either direct conversion pathway. The claimed 85% (ion beam) and >80% (x-ray) are derived from principles, not measurements.
-- Any demonstration of repetitive pulsed operation at kA-scale plasma conditions (all experiments are single-shot).
-- Validated 2-D or MHD simulation of plasmoid dynamics with p-B11 fuel.
-- Quantified shot-to-shot variability and its effect on net energy economics.
+**Missing and hard to model**:
+1. **QMFE physics** is the linchpin of p-B11 viability. Simulations show it reduces bremsstrahlung by up to 5× at Bc ~10 GG. These field strengths have never been measured in any laboratory — they would be the highest ever achieved. No independent experimental confirmation exists.
+2. **Shot-to-shot variability** is identified as a major inherent challenge (Lerner 2023: sensitivity to initial angular momentum means small perturbations cause large yield swings). Intrinsic irreproducibility makes capacity factor modeling extremely difficult.
+3. **p-B11 reactions have never been observed in FF-2B** (as of 2024 Frontiers paper: preparations are "nearly complete"). The entire commercial pathway depends on achieving this first.
+4. **Direct energy conversion subsystems** have never been built at any scale. Ion beam decelerator concept borrows from particle accelerator technology (~85% efficiency demonstrated in accelerator context), but adaptation to a fusion device is unproven. X-ray photoelectric converter has no prototype.
+5. **Yield scaling model reliability**: The I⁴ yield scaling has plateaued above 1 MA for 20+ years across multiple DPF devices. LPPFusion attributes this to impurity-driven filament disruption and oscillations, and claims resolution is in progress, but the plateau is a documented empirical observation that calls yield projections into question.
 
 **Gaps**:
-- QMF effect enabling p-B11 gain >1: theoretically predicted, never experimentally confirmed at required field strengths — `truly-unknown` at this point — **blocking** (the entire concept's viability hinges on this)
-- Ion beam decelerator and x-ray photovoltaic converter: conceptual only, no prototype, no efficiency measurement — `truly-unknown` — **blocking** for quantitative cost modeling
-- High-rep-rate operation: no demonstration at fusion-relevant conditions — `truly-unknown` — **blocking** for capacity factor and O&M modeling
-- Shot-to-shot variability impact on plant economics: unquantified — `derivable` (from known shot variance if yield data were available) — **important**
+- QMFE experimental confirmation absent — `truly-unknown` — **blocking**
+- p-B11 reactions not yet achieved in DPF — `truly-unknown` (no external source can fill this) — **blocking**
+- Direct conversion efficiency unmeasured — `not-yet-sourced` (LPPFusion may have internal estimates; patent gives conceptual design only) — **blocking**
+- Yield plateau mechanism not fully resolved — `truly-unknown` — **blocking**
+- Shot-to-shot variability statistics for commercial projection — `proprietary` — **important**
 
 ---
 
@@ -61,24 +59,24 @@
 **Coverage**: Partial
 
 **Available**:
-- **DPF plasma device (physics)**: TRL 3–4. Ion energies >200 keV demonstrated (world record); nτT = 3.4×10²⁰ keV·s/m³ achieved with D fuel. Beryllium electrodes demonstrated with zeff ~1.004. Yield plateau at >1 MA remains unresolved; new switches installed (2023).
-- **Fuel handling (decaborane)**: TRL 3. Isotopically pure decaborane procured; safe handling equipment installed; first p-B11 shots described as imminent in 2024 Frontiers paper.
-- **Diamond photoconductive switches**: Two external sources (compoundsemiconductor.net, LLNL IPO) confirm diamond PCSS development at TRL 3, with record current densities demonstrated. These would be needed for fast switching in the direct conversion circuit.
-- **Capacitor bank / pulsed power driver**: TRL 6–7 (well-established commercial technology; FF-2B uses a 12-capacitor bank at up to 45 kV). Not a technical risk.
+- **DPF device (capacitor bank + electrodes)**: TRL 5. FF-2B demonstrated 2.7 MA single-shot operation. Beryllium electrodes installed 2019. Device cost ~$500k (Lerner 2024 Frontiers).
+- **Plasma purity control**: TRL 5-6 for D fuel. World-record zeff = 1.004 achieved (Lerner 2023). Represents a genuine experimental achievement.
+- **Decaborane fuel handling**: TRL 3-4. Isotopically pure fuel procured (93g for ~$56,000 = $600/g), handling and exhaust systems installed (Lerner 2024 Frontiers). No actual shots yet.
+- **Diamond photoconductive switches**: TRL 3. Two sources (compoundsemiconductor-119149; ipo-ipo-technologies) document prototype development at University of Illinois and LLNL. LLNL device shows 44 A/cm², ~20% efficiency, ~50 kW output. These are critical for reliable high-rep-rate switching but are at TRL 3 — no commercial product.
 
 **Missing**:
-- **Ion beam decelerator**: No prototype at any scale. The concept is described by analogy with particle accelerator beam dumps; efficiencies >85% are claimed from that literature. No fusion-beam-scale hardware exists.
-- **X-ray multilayer photoelectric converter**: Never built. Design is described in the patent (US #7,482,607) but no prototype or test data exists.
-- **Electrode durability at 200 Hz / fusion yield conditions**: Electrode replacement is targeted at "once per month" but no data on erosion rates at fusion-relevant conditions exists. Current experiments run single-shot.
-- **High-rep-rate pulsed power system**: The electrical circuit (180 kHz natural frequency) has never been run repetitively near fusion conditions.
-- **Anode tip cooling system**: Compressed helium cooling conceptualized; not designed or tested.
+- **High-rep-rate operation (~200 Hz)**: Never demonstrated at fusion-relevant conditions. Singular data point is NX2 (Singapore) at 16 Hz for a small X-ray DPF — very different operating regime. TRL 1-2 for the commercial rep rate.
+- **Ion beam decelerator**: TRL 2. Concept exists in patent. No fusion-scale prototype. Accelerator deceleration technology is mature, but the specific geometry and power levels for DPF have never been built.
+- **X-ray photoelectric converter**: TRL 1-2. No prototype of any kind. Only described in the patent and conceptually in Lerner 2023. Calculated efficiency ~80%, but "such a device has never been made" (Lerner 2023, §Steps from Net Energy).
+- **Helium cooling at 10 kW/cm²**: TRL 2-3. Calculated to be feasible (Lerner 2023). Not experimentally demonstrated for DPF anode cooling.
+- **Electrode erosion at 200 Hz**: Entirely unknown. Lerner 2023 states electrode replacement target of "no more than once a month" but gives no experimental basis. This is a critical O&M cost driver.
 
 **Gaps**:
-- Ion beam decelerator: TRL 1–2, no prototype — `truly-unknown` (fusion-specific; accelerator analogy is imperfect) — **blocking**
-- X-ray photovoltaic converter: TRL 1–2, never built — `truly-unknown` — **blocking**
-- Electrode durability at 200 Hz: no data — `truly-unknown` — **blocking** (monthly replacement is target, not validated)
-- Anode tip cooling at 10 kW/cm²: conceptual only — `derivable` from helium cooling literature — **important**
-- Diamond switch integration with DPF pulse power: TRL 3 in general, not validated for DPF application — `not-yet-sourced` — **important**
+- 200 Hz operation undemonstrated — `truly-unknown` — **blocking**
+- X-ray photoelectric converter prototype absent — `truly-unknown` — **blocking**
+- Ion beam decelerator for DPF unbuilt — `not-yet-sourced` (literature on accelerator-based direct conversion exists; TRL uplift path unclear) — **important**
+- Electrode erosion rate at rep-rated operation — `truly-unknown` — **important**
+- Diamond switch scale-up to commercial power level — `not-yet-sourced` — **important**
 
 ---
 
@@ -86,84 +84,90 @@
 **Coverage**: Partial
 
 **Available**:
-- **Beryllium**: Lerner 2023 JFE explicitly flags the supply chain issue. Current global production ~400 t/year; commercial DPF fleet would require ~10x scale-up. The paper notes that "somewhat less-concentrated ores will have to be exploited" but does not quantify cost impact. Beryllium toxicity requires specialized manufacturing controls.
-- **Boron-11 (isotopically pure)**: Decaborane with 0.07% B-10 has been procured (350× enrichment over natural boron). Cost and supply scalability for commercial deployment are not discussed.
-- **p-B11 fuel abundance**: Both boron and hydrogen are abundant; LPPFusion claims a fully commercial global fleet would need only ~10% increase in total boron production. This is credible given the aneutronic, non-tritium fuel cycle.
-- **No tritium**: Eliminates the most severe supply chain constraint of D-T fusion.
-- **No neutron damage**: Eliminates the first-wall material replacement cycle and radioactive waste stream that drive operating costs in D-T concepts.
+- **Boron-11 (natural)**: Abundant. "Switching fully to a Focus Fusion economy would require only about a 10% increase in boron production" (Lerner 2023). Not a supply concern at any scale.
+- **Boron-11 (isotopically pure)**: Isotopically pure B-11 in decaborane form exists but is custom laboratory-scale production at $600/g (iter-02 sources, lppfusion-proton-boron-p11b-fuel-arrives). Mass production pathway would reduce cost enormously per Lerner, but no industrial supplier has been identified publicly.
+- **Beryllium**: Identified as a critical material. Current global production ~400 t/year. Lerner 2023 estimates ~10× scale-up needed for a fully deployed Focus Fusion economy. Beryllium is not rare (comparable to lead in Earth's crust) but requires expensive, specialized processing due to high toxicity. Limited number of producers globally (primarily Materion in the US).
+- **Hydrogen (protons)**: Trivially abundant.
 
 **Missing**:
-- Cost and scalability data for isotopically pure decaborane at commercial volumes.
-- Beryllium manufacturing cost (machined electrodes, monthly replacement cycle).
-- Diamond availability for photoconductive switches (natural diamond is rare; synthetic CVD diamond supply is limited but growing).
-- Any supply chain analysis from an independent source.
+- No supply chain analysis for isotopically pure B-11 at commercial scale. The lppfusion-proton-boron-p11b-fuel-arrives source notes that the 93g lot was made at two separate labs (Russia + Czech Republic) as a "custom item" — no industrial supplier identified.
+- No beryllium electrode fabrication cost at scale.
+- No assessment of diamond material supply for switching at commercial scale.
+- No analysis of electrode material cycling (beryllium dust/erosion/recycling).
 
 **Gaps**:
-- Isotopically pure decaborane supply at commercial scale: no published data — `not-yet-sourced` (industrial chemistry literature may have analogs) — **important**
-- Monthly beryllium electrode replacement cost at scale: no data — `derivable` (from Be pricing and machining cost analogues) — **important**
-- Diamond supply for PCSS switches: no published data for this application — `not-yet-sourced` — **nice-to-have**
+- Commercial-scale isotopically pure B-11 supply chain — `not-yet-sourced` — **important**
+- Beryllium production scale-up economics — `not-yet-sourced` — **important**
+- Beryllium toxicity / manufacturing handling costs — `not-yet-sourced` — **nice-to-have**
+- Diamond switch manufacturing supply chain — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
-All cost figures below originate from LPPFusion company materials (investor documents, peer-reviewed papers authored by company staff). No independent cost analysis exists.
-
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plant electric output (per unit) | 5 MW | Lerner 2023 JFE (p. 14) | medium — derived from 200 Hz × 25 kJ/pulse |
-| Capital cost (mass production) | ~$500K/unit ($0.10/W) | Lerner 2023 JFE (p. 14) | low — assumes mass production; no BOM |
-| LCOE (claimed) | ~0.3 ¢/kWh | Lerner 2023 JFE (p. 14) | low — unvalidated, company estimate |
-| Repetition rate target | 200 Hz | Lerner 2023 JFE | low — undemonstrated; thermal limit argument |
-| Device mass | ~3 tons | Lerner 2023 JFE | medium |
-| Device volume | ~30 m³ | Lerner 2023 JFE | medium |
-| Annual fuel consumption (per unit) | 5 kg p-B11 | Lerner 2023 JFE | medium — physics consistent |
-| Direct conversion claimed efficiency (ion beam) | ≤85% | Lerner 2023 JFE | low — from accelerator analogy, not DPF test |
-| Direct conversion claimed efficiency (x-ray) | >80% | Lerner 2023 JFE | low — theoretical, never prototyped |
-| Phase 2 engineering budget | ~$100M | Lerner 2023 JFE / net energy plan | medium — company estimate |
-| Electrode replacement target | ~monthly | Lerner 2023 JFE | low — target, no erosion data |
-| Input energy per shot | ~115 kJ stored (FF-1 bank) | Lerner 2023 JFE (p. 9) | high (for current experimental device) |
-| Net energy per pulse (commercial target) | ~25 kJ | Lerner 2023 JFE | low — requires unproven 30 kJ gross yield |
+| Device capital cost (unit) | <$1M ($0.10/W) | Lerner 2023 JFE (company claim) | l |
+| Electrical output per unit | 5 MW net | Lerner 2023 JFE (calculated) | l |
+| Rep rate target | ~200 Hz | Lerner 2023 JFE / website | l |
+| Fusion energy per pulse | ~25 kJ net | Lerner 2023 JFE (calculated) | l |
+| Fuel cost | ~$0/kWh (5 kg/yr) | Lerner 2023 JFE | m |
+| Current device cost (FF-2B) | ~$500k | Lerner 2023 JFE | h |
+| Ion beam decelerator efficiency | ~85% (analog) | Lerner 2023 JFE (accelerator literature analogy) | l |
+| X-ray converter efficiency | ~80% (theoretical) | Lerner 2023 JFE (calculated) | l |
+| Electrode cooling rate target | ≤10 kW/cm² | Lerner 2023 JFE (calculated) | l |
+| Overall claimed LCOE | ~0.3 c/kWh | Lerner 2023 JFE (company estimate) | l |
+| Device mass | ~3 tons | Lerner 2023 JFE | m |
+| Electrode replacement interval target | ~monthly | Lerner 2023 JFE (target) | l |
+| Isotopically pure B-11 fuel cost (lab) | $600/g (lab scale) | lppfusion-proton-boron-p11b-fuel-arrives | h |
+| Physics energy budget (net energy threshold) | ~30 kJ/pulse | lppfusion-our-plan-to-net-energy | m |
+| Engineering phase budget | ~$100M | Lerner 2023 JFE / net energy plan | l |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| CAS-level cost breakdown (20–27) | truly-unknown | blocking | No subsystem-level cost estimates; only total unit cost |
-| Direct energy conversion capital cost | truly-unknown | blocking | Novel technology; no analogues; dominates BOP cost |
-| Operating cost (electrode replacement $/yr) | derivable | blocking | Monthly Be electrodes; need Be unit cost + machining |
-| Capacity factor / availability | truly-unknown | blocking | No rep-rate demonstration; electrode wear unquantified |
-| Recirculating power fraction | derivable | blocking | Needed for net electric output; not stated |
-| Balance of plant cost | derivable | important | Could use scaled-down BOP analogues from small DG sets |
-| Cooling system cost (helium at 10 kW/cm²) | not-yet-sourced | important | He cooling engineering literature may have analogues |
-| D&D cost | derivable | nice-to-have | Small, low-activation device; likely minor |
-| Indirect costs (contingency, owner's cost) | derivable | important | ARIES CAS accounts apply; no concept-specific data |
-| Fusion gain Q (at net energy conditions) | truly-unknown | blocking | p-B11 net energy not yet demonstrated; Q=1 target only |
+| Demonstrated fusion yield (p-B11) | truly-unknown | blocking | Zero — no p-B11 shots yet; D yield is ~0.25 J vs. 30 kJ target |
+| Direct conversion system capital cost | truly-unknown | blocking | No design study; patent describes concept only |
+| Balance of plant capital cost | not-yet-sourced | blocking | No design; no direct conversion BOP analog exists in published literature |
+| Capacity factor | truly-unknown | blocking | No rep-rate operation demonstrated; no reliability data |
+| Electrode replacement cost at 200 Hz | truly-unknown | important | Erosion rate unknown; drives O&M strongly |
+| Cooling system capital cost | not-yet-sourced | important | He cooling at 10 kW/cm² for DPF tip — no design study |
+| Isotopically pure B-11 cost at scale | not-yet-sourced | important | Currently lab-scale only; mass-production cost unquantified |
+| O&M labor rate | not-yet-sourced | important | "Some maintenance every month" — no man-hours or cost breakdown |
+| Grid interconnection / BOP electrical | not-yet-sourced | important | For 5 MW modular unit; no design study |
+| Decommissioning / radioactive waste | derivable | nice-to-have | Minimal (trace C-11, minimal Be activation); low but non-zero |
+| Scaling Q or nτ for p-B11 | truly-unknown | blocking | Wurzel & Hsu 2021 confirm DPF cannot be placed on Lawson criterion plot — no reliable Q estimate exists |
 
 ---
 
 ## Source Recommendations
 
-1. **Lerner (2011) J. Fusion Energy 30:367** — Contains the quantitative commercial device conceptual design (full capacitor bank specs, power plant geometry, scaling arguments). High probability of containing the most detailed engineering data available in the public literature. `not-yet-sourced` — search Springer via DOI 10.1007/s10894-010-9342-2.
+1. **Lerner, E.J., Murali, S.K., Haboub, A. (2011)** *J. Fusion Energy* **30**, 367 — Contains the original conceptual power plant design, full parameter table, and cost estimates that are the basis for all subsequent LPPFusion cost claims. Cited in dossier. **Search**: Search SpringerLink for DOI 10.1007/s10894-010-9380-7. `not-yet-sourced` — confirm existence before treating as accessible.
 
-2. **US Patent #7,482,607** (LPPFusion, "Method and apparatus for producing x-rays, ion beams and nuclear fusion energy") — Contains the original direct energy conversion architecture designs. `not-yet-sourced` — free from USPTO.
+2. **US Patent #7,482,607** (Method and apparatus for producing x-rays, ion beams, and nuclear fusion energy) — Contains the ion beam decelerator and x-ray photoelectric converter design. Publicly accessible via USPTO. `not-yet-sourced`.
 
-3. **Abolhasani et al. (2013) J. Fusion Energy 32:189** — Independent simulation of QMF effect in DPF with p-B11, finding gain ~6×. The only independent cross-check of the QMF physics claim in the available sources. `not-yet-sourced`.
+3. **DPF review literature for independent assessment** — Scholz et al. 2019 (*J. Fusion Energy* 38:522) is cited in the Frontiers 2024 paper and assesses p-B11 feasibility in DPF. Search OSTI or Springer for this paper. `not-yet-sourced` — may provide independent physics assessment of whether QMFE conditions are achievable.
 
-4. **ARPA-E ALPHA program documentation** — The ALPHA program (2015–2020) funded low-cost pulsed fusion concepts. If LPPFusion participated, ARPA-E published milestone reports and a revisit costing exercise (already in repo: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`). Check whether DPF was one of the four costed concepts. `unverified — confirm existence before searching`. If DPF was included, this would be the single most valuable fleet-wide source for this concept.
+4. **NX2 device technical reports (Singapore Institute of Manufacturing Technology / NUSE group)** — NX2 has demonstrated 16 Hz DPF operation as an X-ray source. Engineering data on electrode lifetime and rep-rate operation would directly inform O&M and capacity factor estimates for Focus Fusion. **Search**: OSTI, NTU Singapore repositories. `not-yet-sourced` — confirm existence; papers may be sparse.
 
-5. **IFE simplified economics model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — The 14-parameter Monte Carlo LCOE model for pulsed fusion is methodologically applicable to DPF given its pulsed operation and yield-per-shot economics, even though DPF uses direct conversion rather than a thermal cycle. The rep rate, gain, and driver efficiency parameters map directly. Useful for parameterizing a DPF LCOE model in the absence of concept-specific cost data.
+5. **Abolhasani et al. (2013)** *J. Fusion Energy* **32**, 189 — Cited in Lerner 2023 as independent QMFE study finding "fusion yield approximately 6× the input energy." This is one of the only independent QMFE assessments. Would strengthen or challenge the theoretical basis. `not-yet-sourced`.
 
-6. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — The CAS 20–27 framework is the right structure for any LCOE model regardless of concept. Should be used to structure whatever cost estimates can be made for DPF.
+**Fleet-wide source disqualifications:**
 
-7. **International DPF database / Lee model** — S. Lee's DPF scaling code (Lee model) is widely published and used by the international DPF community. It produces quantitative yield predictions vs. capacitor bank parameters. `not-yet-sourced` — search OSTI or Google Scholar for "Lee model dense plasma focus". Could constrain yield-per-shot and rep-rate parameters.
+- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Not opened; disqualified without opening — DPF uses direct conversion, no blanket, no tritium, no superconducting magnets. D-T MFE cost structure shares zero subsystems with DPF. No applicable cost analogues.
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Not directly applicable as a cost analog. DPF has no CAS22 magnets, no CAS23 blanket, no CAS24 shielding, and no CAS26 thermal cycle. The CAS framework could structure a DPF LCOE analysis in principle, but no ARIES-style subsystem costs map onto this device architecture.
+- **ARPA-E ALPHA Revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened. Four concepts analyzed: Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, Flow-stabilized Z-Pinch — DPF not included. Targets ~500 MWe at ~$2.4/W CapEx and ~$43/MWh LCOE. DPF targets 5 MW at <$1M/unit (~$0.20/W) via direct conversion — fundamentally different scale and architecture. No applicable cost analog for DPF's unique subsystems. Disqualified for this concept.
+- **Simplified IFE economic model (Hawker)** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Opened. Fourteen-parameter model built around IFE driver energy, target gain, rep rate, and thermal conversion efficiency. DPF has no thermal conversion cycle, and the "driver" is indistinguishable from the reactor chamber. Methodology provides a conceptual template for pulsed-device LCOE parameterization, but no numerical values transfer directly. Disqualified as a quantitative analog; may provide methodological inspiration only.
+- **Wurzel & Hsu 2021** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Opened and integrated. Explicitly discusses DPF: "it is not feasible to report a reliable, achieved Lawson parameter or triple product" for DPF because of non-Maxwellian distributions. This confirms that the Lawson-criterion gap for DPF is not merely unmeasured but fundamentally uncharacterizable by standard methods — the physics gap (§2 blocking) is more severe than for any other concept in the portfolio. Integrated into §2.
+- **Helios stellarator, HIF economics, energy from IFE, accelerators for IFE, AMPS, Xcimer, ORNL assessment**: Disqualified without opening — none address DPF device physics, direct conversion at this scale, or p-B11 aneutronic fuel cycles in an applicable way.
 
 ---
 
 ## Summary
 
-Proceed to full analysis, but with significant caveats clearly stated. The qualitative sections (1–4) can be written substantively using the available physics literature. The quantitative LCOE model will be highly speculative: the device is single-shot today, net energy has not been demonstrated (either with D or p-B11), the two novel direct conversion systems exist only on paper, and all cost projections come from company investor materials assuming mass production of a working prototype that does not yet exist. The model should be parameterized to make all assumptions explicit and the back-solve analysis ($0.01/kWh target) is actually where this concept shines analytically — the concept's cost structure is plausibly ultra-low if its physics and engineering claims hold, making the binding constraints (Q, rep rate, electrode life, conversion efficiency) the interesting story.
+The Dense Plasma Focus (p-B11) concept is **constructible as a D1+ analysis** — LPPFusion's published papers and investment materials provide sufficient stated parameters to build a parameterized LCOE model. However, the analysis would be almost entirely composed of company claims with no independent verification, and the underlying physics (p-B11 ignition via QMFE, direct conversion efficiency, 200 Hz rep rate) has not been experimentally demonstrated at any scale. The concept has five blocking gaps: p-B11 reactions undemonstrated, QMFE unconfirmed, direct conversion efficiency unmeasured, 200 Hz rep rate undemonstrated, and no credible Q estimate. The most important additional source to acquire before D1+ analysis is Lerner 2011 *J. Fusion Energy* (the original power plant design paper), Abolhasani et al. 2013 (independent QMFE confirmation), and the LPPFusion patent. The analysis can proceed now but must be heavily caveated as speculative given the concept's pre-ignition status; the back-solve to $0.01/kWh is feasible because the company's own numbers are remarkably optimistic.
 
 ---
 
@@ -171,9 +175,9 @@
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 7
-important_count: 6
-counting_method: "deduplicated across all sections: blocking = (QMF physics undemonstrated, ion beam decelerator no prototype, x-ray photovoltaic no prototype, rep-rate operation undemonstrated, electrode durability unknown, no CAS-level cost breakdown, no capacity factor data); important = (no independent TEA, Lerner 2011 not captured, shot-to-shot variability unquantified, anode cooling conceptual, Be electrode replacement cost unquantified, isotopic decaborane supply unknown)"
+blocking_count: 5
+important_count: 9
+counting_method: "deduplicated across all sections: (blocking) p-B11 unrealized, QMFE unconfirmed, direct conversion unmeasured, 200Hz undemonstrated, Q/Lawson uncharacterizable; (important) no independent cost study, no plant design, no BOP cost, electrode erosion unknown, diamond switch unscaled, B11 supply chain unestablished, capacity factor unknown, ion beam decelerator unbuilt, O&M costs unquantified"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
```
