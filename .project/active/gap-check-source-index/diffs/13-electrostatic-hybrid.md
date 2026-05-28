# Diff: 13-electrostatic-hybrid

**Generated:** 2026-05-22T10:09:09-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 4 | 7 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
166:- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): The four ALPHA concepts (none electrostatic) used modular/compact architectures. The CAS methodology could provide a structural analog for how to organize a cost model for the Orbitron even without specific numbers. Likely to have limited applicability to kWe-scale electrostatic fusion, but worth checking the BOP/indirect cost treatment for modular concepts. Use as a methodology reference only — do not import ALPHA cost numbers as Orbitron analogs.
```

## Blocking-tier lines (baseline)

```
30:- Full-text peer-reviewed papers — `not-yet-sourced` — **blocking** (abstracts only; these likely contain the only quantitative physics data outside company PR)
54:- Recirculating power fraction — `derivable` with large uncertainty (inputs stated in press releases allow rough estimate, but scaling to Q>1 operation is undetermined) — **blocking**
55:- Energy conversion pathway at sub-MW scale — `not-yet-sourced` (small-scale heat engines and thermoelectric options exist but no source discusses them for this device) — **blocking**
56:- Beam-beam vs. thermal fusion regime — `not-yet-sourced` (full-text papers likely address this) — **blocking** (determines whether published fusion rates are achievable at power-relevant density)
57:- Plasma density achievable above Brillouin limit — `proprietary` / `not-yet-sourced` — **blocking**
79:- TRL for energy conversion subsystem — `truly-unknown` (no design disclosed) — **blocking**
80:- TRL for Q>1 plasma physics — `proprietary` (company likely has internal projections) — **blocking**
82:- Component lifetime under 14 MeV neutron fluence (cathode, HV feedthroughs, vacuum envelope) — `truly-unknown` — **blocking** (neutron-induced degradation of HV components is a severe challenge not addressed in any source)
102:- Cathode and HV feedthrough material selection for neutron-exposed operation — `proprietary` — **blocking** (this is the defining engineering challenge; no source discusses it)
```

## Blocking-tier lines (new)

```
146:| Capital cost (by CAS account) | truly-unknown | blocking | No plant design exists at any scale |
147:| Energy conversion efficiency (thermal cycle η) | truly-unknown | blocking | Not designed; at kWe scale, conventional Rankine is impractical |
148:| Capacity factor / availability | truly-unknown | blocking | No operational data; first sustained D-T run hasn't happened |
149:| O&M costs | truly-unknown | blocking | No engineering basis; device not in sustained operation |
150:| Plant scaling to commercial output (MWe) | truly-unknown | blocking | Company says modular stacking but no analysis published |
151:| Recirculating power fraction | truly-unknown | blocking | Q>1 not yet demonstrated; wall-plug efficiency of power supplies uncharacterized |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/13-electrostatic-hybrid.md	2026-05-22 09:21:13.849748408 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/gap_report.md	2026-05-22 10:09:09.088597276 -0700
@@ -1,36 +1,39 @@
+Now I have everything I need to write the assessment. Let me produce the gap report.
+
+---
+
 # Gap Assessment: Electrostatic Hybrid (D-T)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
 
-**Summary**: Avalanche Energy is pre-Q=1 and highly opaque. All available sources are company press releases and a technical blog post — no independent analyses, no plant studies, no peer-reviewed full-text data on device performance. Two peer-reviewed papers exist (AIP Advances 2024, Physics of Plasmas 2025) but only abstracts were captured. A qualitative narrative is feasible but any quantitative LCOE model would require fabricating nearly every input. The concept is too early-stage for a meaningful first-pass LCOE estimate without explicit acknowledgment that essentially all numbers are placeholders.
+The available sources provide a thorough picture of the Orbitron's physics concept, experimental program, and company trajectory, but the device remains a laboratory prototype at TRL 3–4 with no power reactor design, no published cost estimates, and fundamental physics questions unresolved (Coulomb collision thermalization, Q>1 viability). A qualitative narrative of the concept and its challenges can be written, but a quantitative LCOE analysis has no empirical or engineering basis to stand on. All LCOE parameters either don't exist yet (device is pre-power-reactor) or are proprietary internal projections.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Poor (Opaque)
+**Coverage**: Partial
 
 **Available**:
-- Company blog post (CWFest 2023) — best technical source; covers confinement physics, device geometry, performance targets, diagnostics
-- 300 kV milestone press release — voltage milestone, operating parameters (~3 W draw to maintain field)
-- $29M raise press release (2026) — confirms three peer-reviewed publications, near-term roadmap, FusionWERX facility
-- FusionWERX grant press release — neutron factory application, tritium licensing, facility specs
-- Orbitron product page — commercial framing, energy conversion statement, power target range
-- Talk-Polywell forum — community speculation (low authority; useful for flagging unresolved questions)
-- AIP Advances 14(8), 085025 (2024) and Physics of Plasmas 32(9), 092105 (2025) — cited but only abstracts captured
+- Full peer-reviewed physics paper: "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons," *AIP Advances* 14, 085025 (2024) — available in full via `osti-pages-servlets-purl-2582151.md` (62 KB). Covers device design, PIC simulations, subsystem descriptions, diagnostics, instability discussion.
+- CWFest 2023 presentation blog (`avalanche-cwfest2023-blog.md`): CEO-level physics overview, power balance first-order model, scaling contour plots (voltage vs. magnetic field for neutron rate and D-T kW output), team/facility details.
+- Company press releases covering: 300 kV milestone, $29M Series A raise (Feb 2026), FusionWERX facility launch (April 2025), $10M Washington State grant (July 2025).
+- APS abstracts (2023 DPP): ion loading characterization, image current measurements, overview of scientific program.
+- APS poster abstract (DPP 2024): collective effects near the ion space-charge limit.
+- Forum discussion (talk-polywell.org): limited, community speculation only.
 
 **Missing**:
-- Full text of both peer-reviewed papers
-- Any independent technical or economic analysis
-- Any published plant or system study
+- Full text of *Physics of Plasmas* 32(9), 092105 (Sep 2025): "Mode-enhanced ion loading in a 100 kV orbitrap" — likely contains confinement time and density measurements more recent than the AIP paper. Only abstract not captured.
+- Any independent third-party or DOE-sponsored assessment of the Orbitron concept.
+- Any published or disclosed power reactor plant study or commercial design document.
+- The internal first-order power balance model referenced in CWFest2023 is described qualitatively but not published.
 
 **Gaps**:
-- Full-text peer-reviewed papers — `not-yet-sourced` — **blocking** (abstracts only; these likely contain the only quantitative physics data outside company PR)
-- Independent technical analysis — `truly-unknown` (concept too early; no third parties have published analyses)
-- Published plant study or system code output — `truly-unknown` (concept is pre-Q=1; no commercial design exists)
-- Company technical white papers or presentations beyond marketing blog — `proprietary` — **important**
+- Full text of *Physics of Plasmas* 2025 paper — `not-yet-sourced` — important (contains experimental confinement/density data from Marty prototype at higher voltages)
+- No independent technical review of Orbitron claims — `truly-unknown` (company is small, pre-commercial) — nice-to-have
+- No published plant study or power reactor design — `truly-unknown` (doesn't exist yet) — blocking for LCOE
 
 ---
 
@@ -38,48 +41,56 @@
 **Coverage**: Partial
 
 **Available**:
-- Confinement physics described qualitatively (E×B crossed-field, orbitrap-inspired, magnetron-like electron confinement)
-- Device geometry: plasma core "tens of centimeters," full system "fits in pickup bed"
-- Identified energy balance tension: ~1 kW input (600 W cathode + 400 W ion guns) targeting ~1 kW fusion power → Q~1 at breakeven only; recirculating power dominates the economics at this scale
-- Energy conversion stated as "thermal cycle with turbines" — acknowledged as impractical at 1–100 kWe scale even in the dossier
+- The two fundamental criticisms of non-thermal electrostatic fusion are clearly documented in sources (Rider 1995: Coulomb collisions and thermalization exceeding fusion rates; Lakhina/Manheimer 1998: 90° scattering 25× faster than D-T fusion). The CWFest2023 blog discusses Avalanche's response: WarpX PIC simulations suggest non-trivial plasma persists past the predicted thermalization time when density-scaled, but the thermalization question is unresolved.
+- Bremsstrahlung radiation identified as an inherent energy loss mechanism; Rider's paper (1997) referenced in AIP paper (Ref. 58). Quantitative characterization planned but not yet published.
+- Diocotron instability and electron cyclotron drift instability identified as near-term experimental risks.
+- Ion-ion Coulomb collisional diffusion is acknowledged as an open problem (angular momentum transport timescale unknown).
+- Space charge limit: PIC simulations show 50× density enhancement with electron co-confinement (reaching ~5.4×10¹⁰ cm⁻³). Not yet experimentally confirmed above space-charge limit.
+- Operating mode ambiguity: company says steady-state voltage; behavior of the fusion plasma burn at Q>1 scale is uncertain.
 
 **Missing**:
-- Recirculating power fraction at commercial operating conditions
-- Energy conversion pathway engineering (turbines at kWe scale are not viable; no alternative disclosed)
-- Coulomb collision and beam-beam thermalization rates at fusion density (critical for assessing whether thermal D-T or beam-beam fusion dominates — fundamentally different economics)
-- Brillouin-limit behavior at commercial density (flagged as "make or break" by forum source; simulation claims stability but no published data)
-- Ion loss mechanisms and cathode heating rates
+- Quantitative power balance calculation at any operating point — company describes the structure of their model (CWFest2023) but no numbers are published.
+- Energy conversion pathway engineering at power-producing scale: how 1–100 kWe is extracted from 14 MeV neutrons bombarding a small chamber is not designed.
+- Bremsstrahlung power loss measurement at high density — described as future diagnostic work.
+- Plasma behavior under D-T conditions: all experiments to date are D-D (FusionWERX tritium licensing expected 2027).
 
 **Gaps**:
-- Recirculating power fraction — `derivable` with large uncertainty (inputs stated in press releases allow rough estimate, but scaling to Q>1 operation is undetermined) — **blocking**
-- Energy conversion pathway at sub-MW scale — `not-yet-sourced` (small-scale heat engines and thermoelectric options exist but no source discusses them for this device) — **blocking**
-- Beam-beam vs. thermal fusion regime — `not-yet-sourced` (full-text papers likely address this) — **blocking** (determines whether published fusion rates are achievable at power-relevant density)
-- Plasma density achievable above Brillouin limit — `proprietary` / `not-yet-sourced` — **blocking**
+- Quantitative power balance published data — `proprietary` — blocking (company has internal model but hasn't published it)
+- Energy conversion engineering (neutron-to-thermal-to-electric at kWe scale) — `truly-unknown` — blocking (not yet designed)
+- Experimental confirmation of density above space-charge limit — `not-yet-sourced`/`truly-unknown` — important (Physics of Plasmas 2025 paper may address this)
+- Bremsstrahlung characterization at fusion-relevant density — `truly-unknown` — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- High-voltage feedthrough at 300 kV sustained: demonstrated (cited as key innovation vs. prior 30–50 kV state of art) → TRL ~4
-- Ion confinement and elliptical orbit physics: demonstrated at laboratory scale → TRL ~3–4
-- E×B electron co-confinement: demonstrated at low power → TRL ~3
-- Permanent magnet electron confinement (0.05 T): demonstrated in NEO prototype → TRL ~4
-- Basic diagnostics (scintillators, He-3 counters, X-ray/neutron spectroscopy): mature technology → TRL 6–8
+**Available** (from AIP Advances + CWFest2023):
+
+| Subsystem | Status | TRL (approx.) |
+|---|---|---|
+| High-voltage feedthrough (300 kV UHV bushing) | Demonstrated, novel custom design | TRL 5–6 |
+| Cathode (Mo) + anode (Cu) electrodes | Operational on Neo and Marty | TRL 5 |
+| Vacuum system (cryopump + differential pumping, <10⁻⁸ Torr) | Operational | TRL 6 |
+| Ion source (MARK I End Hall, D⁺ beam 1–10 mA) | Modified commercial source, operational | TRL 5–6 |
+| Permanent magnets (Halbach array, 0.05 T) | Operational on Neo | TRL 6 |
+| HTS superconducting magnets (0.3–0.5 T target) | Ordered 2025/2026, not yet integrated | TRL 3–4 |
+| Diagnostics (microwave interferometry, OES, soft x-ray, neutron, image current) | In development | TRL 3–4 |
+| Electron source (field emission from cathode) | Operational | TRL 5 |
 
 **Missing**:
-- Q>1 operation: not demonstrated → TRL ~1–2
-- Energy conversion subsystem: not designed, not demonstrated → TRL ~1
-- Tritium breeding blanket: not designed → TRL ~1
-- Modular scaling to MW-class: not demonstrated → TRL ~1–2
-- Superconducting magnets at 0.3 T for this geometry: not built → TRL ~2–3
+- Energy conversion subsystem (thermal cycle / turbine): not designed or built at any scale.
+- Tritium handling: FusionWERX facility licensing expected 2027; no in-device tritium system designed.
+- Tritium breeding blanket: no concept selected; not feasible at 1–100 kWe scale.
+- Balance of plant: no design exists.
+- Power conditioning and recirculating power systems for sustained Q>1 operation: not designed.
 
 **Gaps**:
-- TRL for energy conversion subsystem — `truly-unknown` (no design disclosed) — **blocking**
-- TRL for Q>1 plasma physics — `proprietary` (company likely has internal projections) — **blocking**
-- TRL for tritium breeding at compact scale — `truly-unknown` — **important**
-- Component lifetime under 14 MeV neutron fluence (cathode, HV feedthroughs, vacuum envelope) — `truly-unknown` — **blocking** (neutron-induced degradation of HV components is a severe challenge not addressed in any source)
+- Energy conversion subsystem — `truly-unknown` — blocking
+- Tritium breeding design — `truly-unknown` — blocking
+- Balance of plant — `truly-unknown` — blocking
+- Power conditioning / recirculating power at Q>1 — `truly-unknown` — important
+- HTS magnet integration results (0.3–0.5 T) — `not-yet-sourced` (magnets ordered 2025–2026; results likely to appear in 2026 publications) — important
 
 ---
 
@@ -87,96 +98,94 @@
 **Coverage**: Poor
 
 **Available**:
-- D-T fuel: tritium supply concerns apply; FusionWERX has tritium handling license (expected fully operational 2027); near-term tritium will be purchased
-- Magnetic components: permanent magnets in current prototypes; superconducting magnets at 0.3 T targeted (low field — relatively accessible compared to tokamak HTS requirements)
-- Neutron shielding: concrete and steel ("concrete castle") — mature, abundant materials
-- Device scale: desktop/pickup-truck scale means material quantities per module are small
+- Cathode: molybdenum (chosen for machinability and field emission properties); conditioning procedures described (current and gas conditioning to remove field emitters).
+- Anode: copper.
+- Insulator: MACOR ceramic (129 MV/m dielectric strength, machineable).
+- Vacuum system: standard UHV materials.
+- Magnets: neodymium Halbach array (current); HTS coils (planned).
+- Shielding: concrete (Marty "concrete castle" for x-ray and neutron shielding).
+- Tritium supply: MoU with Fusion Fuel Cycles (FFC) for fuel cycle support; FusionWERX designed for tritium handling.
 
 **Missing**:
-- HV cathode material specification (must survive neutron bombardment + electrical stress at 300 kV)
-- First wall / inner electrode material for D-T neutron environment
-- Vacuum chamber material and neutron activation concerns
-- HV feedthrough insulator material (ceramic type, neutron tolerance)
+- First wall / inner chamber material under sustained neutron bombardment (14 MeV): no material selection or activation analysis at any power level.
+- Structural material assessment for a power-producing reactor at any scale.
+- Critical materials analysis: HTS wire (REBCO) supply chain for the superconducting magnets.
+- Tritium breeding material (Li-6 enrichment, blanket material): not discussed.
+- Material degradation / replacement schedule under neutron flux.
+- Supply chain risk for the novel 300 kV UHV bushing: custom design, no commercial supplier identified.
 
 **Gaps**:
-- Cathode and HV feedthrough material selection for neutron-exposed operation — `proprietary` — **blocking** (this is the defining engineering challenge; no source discusses it)
-- First wall material at compact geometry with high 14 MeV neutron flux — `not-yet-sourced` (IEC and fusor literature may have analogues) — **important**
-- Tritium breeding material if breeding blanket ever designed — `truly-unknown` — nice-to-have (near-term relies on purchased tritium)
-- Li-6 or beryllium requirements for any future breeding blanket — `truly-unknown` — nice-to-have
+- First wall material selection and activation analysis — `truly-unknown` (power reactor not yet designed) — important
+- HTS magnet supply chain for REBCO conductors — `not-yet-sourced` — nice-to-have
+- Tritium breeding material — `truly-unknown` — important
+- 300 kV UHV bushing commercial supply path — `proprietary` (Avalanche has a custom design; commercial availability unclear) — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Very Poor
+**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Target electrical output per module | 1–100 kWe | Orbitron page | m |
-| Target plant output (modular stacking) | 100s kW to MW | Orbitron page | l |
-| Input power (baseline) | ~1 kW (600W cathode + 400W ion guns) | CWFest 2023 blog | m |
-| Target Q | >1 (aspiration) | $29M PR, 300kV PR | l |
-| Current fusion power output | ~1 kW (target); sub-Q=1 demonstrated | CWFest 2023 blog | m |
-| Neutron output target | mid-10¹¹ n/s | CWFest 2023 blog | m |
-| Energy conversion pathway | Thermal cycle, turbines (D-T) | Orbitron page | l |
-| Operation mode | Steady-state | 300kV PR, $29M PR | m |
-| Fuel type | D-T (primary) | Multiple sources | h |
-| Device voltage | 300 kV sustained | 300kV PR | h |
+|---|---|---|---|
+| Target net electrical output (per module) | 1–100 kWe | Orbitron product page | low (undemonstrated) |
+| Fusion power at target conditions | ~1 kW (at 300 kV, 0.3 T, D-T) | CWFest2023 scaling contour | low (extrapolated from PIC sim) |
+| Driver input power at target conditions | ~1 kW (600 W cathode + 400 W ion guns at ~1 kW fusion) | CWFest2023 | low (rough estimate from CEO) |
+| Energy conversion approach | Thermal cycle / turbines (neutron bombardment → heat) | Orbitron product page | low (undesigned) |
+| Cathode voltage (achieved) | 300 kV steady-state | 300 kV press release | high |
+| Magnetic field (target) | 0.3–0.5 T (HTS, not yet integrated) | AIP Advances, CWFest2023 | medium |
+| D-T neutron energy | 14.1 MeV | Standard physics | high |
+| Team size / funding (as of 2026) | 33+ people, $29M raised, $10M grant | Press releases | high |
+| FusionWERX Q>1 test date target | ~2027 (tritium licensing expected 2027) | $29M press release | medium |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Capital cost per module (or kWe) | `truly-unknown` | Blocking | No cost data published; no analogous system exists |
-| Achieved Q value (not target) | `proprietary` | Blocking | Company has internal data but has not published Q measurements |
-| Thermal conversion efficiency | `truly-unknown` | Blocking | Turbines at 1–100 kWe are implausible; no alternative specified |
-| Recirculating power fraction at commercial Q | `derivable` (crude) | Blocking | ~1 kW input vs. Q>1 fusion output; wall-plug efficiency dominates |
-| Component replacement schedule (cathode, HV, ion gun) | `proprietary` | Blocking | High-voltage components under neutron flux will degrade; no data |
-| Tritium fuel cost assumption (purchased) | `not-yet-sourced` | Important | Market price ~$30k/g; consumption rate calculable if Q and power are known |
-| Capacity factor / availability | `truly-unknown` | Blocking | No maintenance intervals or availability data disclosed |
-| Number of modules per MW plant | `derivable` | Important | Can be estimated from claimed 1–100 kWe range |
-| Balance of plant costs at MW scale | `not-yet-sourced` | Important | Small modular thermal plant literature may provide analogues |
-| Neutron shielding capital cost at commercial scale | `derivable` | Important | Concrete "castle" geometry known; structural analogues available |
-| Tritium breeding cost (if applicable) | `truly-unknown` | Nice-to-have | No breeding design; near-term = purchased tritium |
+|---|---|---|---|
+| Capital cost (by CAS account) | truly-unknown | blocking | No plant design exists at any scale |
+| Energy conversion efficiency (thermal cycle η) | truly-unknown | blocking | Not designed; at kWe scale, conventional Rankine is impractical |
+| Capacity factor / availability | truly-unknown | blocking | No operational data; first sustained D-T run hasn't happened |
+| O&M costs | truly-unknown | blocking | No engineering basis; device not in sustained operation |
+| Plant scaling to commercial output (MWe) | truly-unknown | blocking | Company says modular stacking but no analysis published |
+| Recirculating power fraction | truly-unknown | blocking | Q>1 not yet demonstrated; wall-plug efficiency of power supplies uncharacterized |
+| Fuel cost (tritium procurement) | derivable | important | Can be estimated from market price at small tritium mass; breeding not viable at this scale |
+| Decommissioning cost | truly-unknown | nice-to-have | Activation levels unknown |
+| Construction time | truly-unknown | important | No commercial plant design; desktop scale suggests fast, but modular MWe plant undefined |
 
 ---
 
 ## Source Recommendations
 
-1. **AIP Advances 14(8), 085025 (August 2024)** — "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" — full text. This is the primary peer-reviewed source on confinement physics; likely contains quantitative density, energy, and loss-rate data. `not-yet-sourced` — retrieve full text via institution access or Sci-Hub equivalent.
-
-2. **Physics of Plasmas 32(9), 092105 (September 2025)** — "Mode-enhanced ion loading in a 100 kV orbitrap" — full text. Likely contains ion density, loading efficiency, and performance data at 100 kV. `not-yet-sourced` — same retrieval path as above.
+- **Full text of *Physics of Plasmas* 32(9), 092105 (2025)**: "Mode-enhanced ion loading in a 100 kV orbitrap" — `not-yet-sourced` — likely contains confinement time measurements and density-above-space-charge-limit experimental data from Marty. Search OSTI or AIP Scitation by DOI (appears to be from the same team). This is the highest-priority missing source for Section 2 and Section 3.
 
-3. **APS DPP proceedings (2022–2025)** — search for "Orbitron" or "Avalanche Energy" in APS Division of Plasma Physics conference abstracts. Early-stage companies often present more technical detail at APS DPP than in press releases. `unverified — confirm existence before searching`
+- **Any additional 2025–2026 conference papers from Avalanche Energy** (APS DPP 2025): The DPP 2024 abstract (`meetings-meeting-dpp24-session-np12-69.md`) suggests ongoing experimental work on space-charge collective effects. Search APS/arXiv for Affolter, Merthe, Langtry (2025). `not-yet-sourced`.
 
-4. **DOE SBIR/STTR award database (SEED)** — search Avalanche Energy for any federal contracts with technical scope statements. These sometimes include performance targets and milestones. `unverified — confirm existence before searching`
+- **IEC/fusor analogues for power balance**: Published analyses of Bremsstrahlung vs. fusion power for non-thermal D-T plasmas (e.g., Rider 1997 *Phys. Plasmas* 4, 1039 — cited in AIP paper as Ref. 58, not ingested). Relevant for Section 2 power balance analysis. `not-yet-sourced` — search OSTI or AIP for Rider 1997.
 
-5. **ARPA-E OPEN or BETHE program award records** — Avalanche may have received ARPA-E funding; program documents typically include technical approach descriptions. `unverified — confirm existence before searching`
+- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): The four ALPHA concepts (none electrostatic) used modular/compact architectures. The CAS methodology could provide a structural analog for how to organize a cost model for the Orbitron even without specific numbers. Likely to have limited applicability to kWe-scale electrostatic fusion, but worth checking the BOP/indirect cost treatment for modular concepts. Use as a methodology reference only — do not import ALPHA cost numbers as Orbitron analogs.
 
-6. **IEC/Fusor literature for cathode material analogues** — Search OSTI or Google Scholar for "IEC neutron source cathode lifetime" or "fusor tungsten cathode neutron damage." These studies on related devices (Farnsworth-Hirsch fusors) may provide neutron fluence tolerance data for HV cathode materials. `not-yet-sourced`
-
-7. **Small-scale heat engine and thermoelectric literature** — For the energy conversion gap, search for "kW-scale Stirling engine efficiency," "thermoelectric generator 1 kW," or "compact ORC 10 kW thermal" to find cost and efficiency analogues for the 1–100 kWe range that turbines cannot serve. `not-yet-sourced`
+- **No fleet-wide source in the SOURCE_INDEX is directly applicable** to electrostatic hybrid cost estimation. The MFE D-T TEA sources, IFE sources, and stellarator sources all assume thermal plasmas, gigawatt-scale plants, and standard tokamak/stellarator architectures that do not translate to a 1–100 kWe electrostatic device.
 
 ---
 
 ## Summary
 
-**Do not proceed directly to a full quantitative LCOE analysis without additional source work.**
-
-The available data can support a qualitative narrative covering confinement physics, device architecture, near-term roadmap, and TRL assessments. The physics description is coherent and the dossier captures everything that has been made public. However, all five LCOE-critical parameters — capital cost, achieved Q, thermal conversion efficiency, recirculating power, and availability — are either `truly-unknown` or `proprietary`. A quantitative model built on current data would have no grounding for any of its major inputs.
+The available data is sufficient to write a technically detailed qualitative analysis of the Orbitron concept — covering the physics basis, company status, experimental progress through Marty/300 kV milestone, key physics challenges (Coulomb collisions, space charge, Bremsstrahlung), and the competitive context of non-thermal electrostatic fusion. However, a quantitative LCOE analysis is not feasible: the device has not achieved Q>1, no power reactor has been designed at any scale, and all cost parameters (capital, O&M, capacity factor, energy conversion efficiency) are either unavailable (proprietary), not yet designed (truly-unknown), or undefined (the concept is at TRL 3–4 with no commercial plant geometry). Acquiring the Physics of Plasmas 2025 paper and any APS 2025 abstracts would improve Section 3 (subsystem maturity), but would not unlock LCOE analysis. Proceed to qualitative D1 analysis; mark LCOE quantitative parameters as data-insufficient and describe the critical path to resolving them.
 
-**Recommended path**: Retrieve full text of the two peer-reviewed papers before writing the analysis. These are the only non-marketing sources and likely contain quantitative plasma data (density, confinement time, fusion rate measurements) that could anchor the recirculating power and Q estimates. Even with those, a capital cost estimate and conversion efficiency will remain speculative — the analysis should make this explicit and use the back-solve direction ($0.01/kWh target) as the primary analytical frame rather than a bottom-up LCOE estimate.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
 blocking_count: 6
-important_count: 4
-counting_method: "section_5_missing_parameters"
+important_count: 7
+counting_method: "deduplicated_across_all_sections — blocking: (1) Q>1 physics/power balance basis, (2) energy conversion system design, (3) capital cost data, (4) O&M cost data, (5) capacity factor/availability, (6) tritium breeding design. Important: (1) Physics of Plasmas 2025 full paper, (2) confinement time/density scaling data, (3) Bremsstrahlung characterization, (4) HTS magnet integration results, (5) first wall material selection, (6) tritium breeding material, (7) commercial plant scaling analysis."
 section_coverage:
-  availability_of_data:       "Poor (Opaque)"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Very Poor"
-```
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
