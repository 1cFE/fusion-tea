# Phase 3 diff: 13-electrostatic-hybrid

**Generated:** 2026-05-22T14:12:24-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 7 | 12 | - |
| overall_rating   | Insufficient Data | Significant Gaps | - |

## Fleet-source dispositions in new report

```
117:- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened and read. The four concepts are Plasma-Jet MIF (HyperJet Fusion), Stabilized Liner Compressor (CFS), Staged Z-Pinch (MIFTI), and Flow-Stabilized Z-Pinch (Zap Energy) — all pulsed MIF at ~500 MWe plant scale. The Orbitron operates at 1–100 kWe per module, a scale 4–6 orders of magnitude smaller; the CAS cost structure and plant economics do not transfer. **Disqualified**: wrong confinement family, wrong power scale, no cost analog applicable to electrostatic kWe-scale devices.
121:- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Covers D-T MFE at ~1 GWe tokamak scale with CAS 20–29 cost breakdowns. The Orbitron is 7+ orders of magnitude smaller; BOP and cost driver structures are completely different. D-T fuel cycle fraction would be similarly irrelevant given the scale mismatch. **Disqualified**: scale mismatch makes all cost analogs inapplicable.
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have all the information needed to write the gap assessment. All concept-scoped and relevant fleet-wide sources have been read.
```

## Blocking-tier lines (new)

```
35:- Non-thermal Q>1 feasibility: no quantitative published power balance at target operating conditions — `proprietary` (company likely has unpublished models) — **blocking**
36:- Ion confinement time τ at target density (>10¹¹ cm⁻³): not measured, extrapolated only — `not-yet-sourced` (Physics of Plasmas Sep 2025 may address) — **blocking**
38:- Energy conversion system architecture at kWe scale: entirely unspecified — `truly-unknown` (no kWe-scale fusion thermal conversion precedent exists) — **blocking**
60:- Thermal energy conversion system: no concept at kWe scale — `truly-unknown` — **blocking**
104:| Capital cost breakdown (by CAS account) | truly-unknown | blocking | No plant study; device doesn't yet demonstrate net energy |
105:| Thermal conversion efficiency (η_th) | truly-unknown | blocking | No cycle type specified; at 1–100 kWe, conventional steam turbines are not viable |
106:| Plant capacity factor | truly-unknown | blocking | No maintenance model; no lifetime estimate |
107:| Q at commercial scale (engineering gain) | truly-unknown | blocking | Only Q~1 targeted for D-T test; commercial plant needs Q_eng >1 after recirculation losses |
108:| O&M costs | truly-unknown | blocking | No facility operating cost model exists |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/13-electrostatic-hybrid.md	2026-05-22 12:59:21.067635786 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/gap_report.md	2026-05-22 14:12:24.820753464 -0700
@@ -1,124 +1,82 @@
-Now I have everything I need to write the assessment. Let me produce the gap report.
-
----
+I now have all the information needed to write the gap assessment. All concept-scoped and relevant fleet-wide sources have been read.
 
 # Gap Assessment: Electrostatic Hybrid (D-T)
 
 ## Overall Readiness
-**Rating**: Insufficient Data
-
-The available sources provide a thorough picture of the Orbitron's physics concept, experimental program, and company trajectory, but the device remains a laboratory prototype at TRL 3–4 with no power reactor design, no published cost estimates, and fundamental physics questions unresolved (Coulomb collision thermalization, Q>1 viability). A qualitative narrative of the concept and its challenges can be written, but a quantitative LCOE analysis has no empirical or engineering basis to stand on. All LCOE parameters either don't exist yet (device is pre-power-reactor) or are proprietary internal projections.
+**Rating**: Significant Gaps
+**Summary**: The Orbitron concept (Avalanche Energy) has one substantive peer-reviewed paper covering device physics and prototype engineering (AIP Advances, Aug 2024), supplemented by company press releases and a detailed CWFest 2023 technical presentation. These sources provide adequate coverage of confinement physics, subsystem architecture, and near-term milestones. However, the concept remains pre-Q=1, and there are no capital cost estimates, no published power balance with quantitative outputs, no thermal conversion system design, and no plant study of any kind. The LCOE section cannot be populated with real numbers — only aspirational targets and derived estimates would be possible. A qualitative analysis of concept function and subsystem maturity is feasible; quantitative LCOE modeling is not.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Poor
+
+**Available**: The primary technical source is the AIP Advances paper (Affolter et al., 2024; `osti-pages-servlets-purl-2582151.md`), which covers device physics, prototype design, key subsystems, and PIC simulations. The CWFest 2023 blog (`avalanche-cwfest2023-blog.md`) contains the best system-level discussion including a first-order Q model and power balance reasoning. Company press releases ($29M raise 2026, 300 kV milestone, FusionWERX launch) provide program status and commercial roadmap context. Three APS abstracts confirm experimental work at 100+ keV ion energies and space-charge limit characterization. All sources originate from Avalanche Energy or describe Avalanche's work; there are no independent assessments.
 
-**Available**:
-- Full peer-reviewed physics paper: "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons," *AIP Advances* 14, 085025 (2024) — available in full via `osti-pages-servlets-purl-2582151.md` (62 KB). Covers device design, PIC simulations, subsystem descriptions, diagnostics, instability discussion.
-- CWFest 2023 presentation blog (`avalanche-cwfest2023-blog.md`): CEO-level physics overview, power balance first-order model, scaling contour plots (voltage vs. magnetic field for neutron rate and D-T kW output), team/facility details.
-- Company press releases covering: 300 kV milestone, $29M Series A raise (Feb 2026), FusionWERX facility launch (April 2025), $10M Washington State grant (July 2025).
-- APS abstracts (2023 DPP): ion loading characterization, image current measurements, overview of scientific program.
-- APS poster abstract (DPP 2024): collective effects near the ion space-charge limit.
-- Forum discussion (talk-polywell.org): limited, community speculation only.
-
-**Missing**:
-- Full text of *Physics of Plasmas* 32(9), 092105 (Sep 2025): "Mode-enhanced ion loading in a 100 kV orbitrap" — likely contains confinement time and density measurements more recent than the AIP paper. Only abstract not captured.
-- Any independent third-party or DOE-sponsored assessment of the Orbitron concept.
-- Any published or disclosed power reactor plant study or commercial design document.
-- The internal first-order power balance model referenced in CWFest2023 is described qualitatively but not published.
+**Missing**: No independent peer review of the Q feasibility claim; no government reports, ARPA-E analysis, or academic benchmarking of the Orbitron concept specifically; only one peer-reviewed paper (full text) available, with a second paper (Physics of Plasmas 32(9), Sep 2025) referenced in the dossier but available only as a title; the APS DPP24 poster (NP12.69) captured as title/author list only.
 
 **Gaps**:
-- Full text of *Physics of Plasmas* 2025 paper — `not-yet-sourced` — important (contains experimental confinement/density data from Marty prototype at higher voltages)
-- No independent technical review of Orbitron claims — `truly-unknown` (company is small, pre-commercial) — nice-to-have
-- No published plant study or power reactor design — `truly-unknown` (doesn't exist yet) — blocking for LCOE
+- No independent techno-economic or technical assessment — `proprietary` / `not-yet-sourced` — **important**
+- Physics of Plasmas Sep 2025 paper not captured — `not-yet-sourced` — **important** (may contain confinement time data critical for §2)
+- All quantitative performance claims originate from the concept developer — `proprietary` — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**:
-- The two fundamental criticisms of non-thermal electrostatic fusion are clearly documented in sources (Rider 1995: Coulomb collisions and thermalization exceeding fusion rates; Lakhina/Manheimer 1998: 90° scattering 25× faster than D-T fusion). The CWFest2023 blog discusses Avalanche's response: WarpX PIC simulations suggest non-trivial plasma persists past the predicted thermalization time when density-scaled, but the thermalization question is unresolved.
-- Bremsstrahlung radiation identified as an inherent energy loss mechanism; Rider's paper (1997) referenced in AIP paper (Ref. 58). Quantitative characterization planned but not yet published.
-- Diocotron instability and electron cyclotron drift instability identified as near-term experimental risks.
-- Ion-ion Coulomb collisional diffusion is acknowledged as an open problem (angular momentum transport timescale unknown).
-- Space charge limit: PIC simulations show 50× density enhancement with electron co-confinement (reaching ~5.4×10¹⁰ cm⁻³). Not yet experimentally confirmed above space-charge limit.
-- Operating mode ambiguity: company says steady-state voltage; behavior of the fusion plasma burn at Q>1 scale is uncertain.
-
-**Missing**:
-- Quantitative power balance calculation at any operating point — company describes the structure of their model (CWFest2023) but no numbers are published.
-- Energy conversion pathway engineering at power-producing scale: how 1–100 kWe is extracted from 14 MeV neutrons bombarding a small chamber is not designed.
-- Bremsstrahlung power loss measurement at high density — described as future diagnostic work.
-- Plasma behavior under D-T conditions: all experiments to date are D-D (FusionWERX tritium licensing expected 2027).
+**Available**: The AIP Advances paper provides detailed treatment of single-particle confinement physics (E×B orbits, magnetron electron confinement, electrostatically-plugged magnetic mirror), field perturbations at high density, and PIC simulations showing 5.4×10¹⁰ cm⁻³ average ion density with co-confinement (vs. 1.1×10⁹ cm⁻³ for pure ion plasma). Loss mechanisms identified include: Coulomb scattering (ion–ion, ion–electron), diffusion to conducting walls, diocotron instability (observed in pure electron simulations), electron cyclotron drift instability (potential), and Bremsstrahlung radiation. The CWFest blog explicitly addresses the Rider (1995) and Lampe/Manheimer (NRL) critiques of non-thermal fusion feasibility and describes a first-order Q model with a peak near 63 keV CoM energy and ~15 keV electron temperature for D-T — conditions where Deuterium-Tritium's Coulomb scattering term is balanced by electron-driven ion upscattering. The company claims density-scaled PIC results show the plasma survives past the Lampe-Manheimer thermalization time, but no quantitative confinement time at target density is published.
+
+**Missing**: The fundamental challenge for cost modeling is that the non-thermal plasma Q>1 claim is undemonstrated and contested in the literature — no published power balance with actual simulated numbers is available; only a first-order model sketch exists. At operating density (~10¹¹ cm⁻³), ion confinement time is extrapolated from low-density measurements (<10⁸ cm⁻³). Energy conversion at 1–100 kWe scale is entirely unspecified; the turbine thermal cycle stated on the product page is implausible at these scales and almost certainly describes a long-term vision rather than a validated design.
 
 **Gaps**:
-- Quantitative power balance published data — `proprietary` — blocking (company has internal model but hasn't published it)
-- Energy conversion engineering (neutron-to-thermal-to-electric at kWe scale) — `truly-unknown` — blocking (not yet designed)
-- Experimental confirmation of density above space-charge limit — `not-yet-sourced`/`truly-unknown` — important (Physics of Plasmas 2025 paper may address this)
-- Bremsstrahlung characterization at fusion-relevant density — `truly-unknown` — important
+- Non-thermal Q>1 feasibility: no quantitative published power balance at target operating conditions — `proprietary` (company likely has unpublished models) — **blocking**
+- Ion confinement time τ at target density (>10¹¹ cm⁻³): not measured, extrapolated only — `not-yet-sourced` (Physics of Plasmas Sep 2025 may address) — **blocking**
+- Bremsstrahlung power loss fraction at operating conditions: no published numbers — `proprietary` — **important**
+- Energy conversion system architecture at kWe scale: entirely unspecified — `truly-unknown` (no kWe-scale fusion thermal conversion precedent exists) — **blocking**
+- Collective instabilities at high density: diocotron and ECDI only studied at low density — `not-yet-sourced` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available** (from AIP Advances + CWFest2023):
+**Available**: The AIP Advances paper provides the most detailed subsystem-level breakdown available:
+- **HV cathode/bushing**: Custom 300 kV UHV bushing designed and tested (MACOR insulator, Mo cathode, Cu anode). Conditioned to 300 kV; sustained for hours (2025 milestone). TRL ~3–4.
+- **Vacuum system**: Commercial cryopump (2500 l/s for H₂), base pressure ~10⁻⁹ Torr, operating pressure ~10⁻⁸ Torr with ion source. UHV requirement is well-understood from orbital ion trap heritage. TRL ~5 (off-shelf components at lab scale).
+- **Ion source**: Modified MARK I End Hall, 0.7 A discharge, up to 20 keV, 75% D⁺ / 20% D₂⁺ / 5% D₃⁺. Required beam current 1–10 mA for target density. TRL ~4.
+- **Electron source**: Field emission from conditioned Mo cathode (~1–10 mA leakage current); dedicated electron gun designed as backup. TRL ~3.
+- **Permanent magnets**: Neodymium Halbach array at 0.05 T operational. TRL ~5 for current prototype scale.
+- **HTS magnets (next-gen)**: Ordered but not yet deployed; targeting 0.5 T at mid-plane. Two specially designed HTS coil pairs. TRL ~2–3 for this application.
+- **Neutron diagnostics**: He-3 proportional counters, bubble detectors, PSD scintillators, neutron camera. TRL ~4–5 for individual components.
+- **Microwave interferometry**: 60 GHz V-band system for electron density. TRL ~3.
 
-| Subsystem | Status | TRL (approx.) |
-|---|---|---|
-| High-voltage feedthrough (300 kV UHV bushing) | Demonstrated, novel custom design | TRL 5–6 |
-| Cathode (Mo) + anode (Cu) electrodes | Operational on Neo and Marty | TRL 5 |
-| Vacuum system (cryopump + differential pumping, <10⁻⁸ Torr) | Operational | TRL 6 |
-| Ion source (MARK I End Hall, D⁺ beam 1–10 mA) | Modified commercial source, operational | TRL 5–6 |
-| Permanent magnets (Halbach array, 0.05 T) | Operational on Neo | TRL 6 |
-| HTS superconducting magnets (0.3–0.5 T target) | Ordered 2025/2026, not yet integrated | TRL 3–4 |
-| Diagnostics (microwave interferometry, OES, soft x-ray, neutron, image current) | In development | TRL 3–4 |
-| Electron source (field emission from cathode) | Operational | TRL 5 |
-
-**Missing**:
-- Energy conversion subsystem (thermal cycle / turbine): not designed or built at any scale.
-- Tritium handling: FusionWERX facility licensing expected 2027; no in-device tritium system designed.
-- Tritium breeding blanket: no concept selected; not feasible at 1–100 kWe scale.
-- Balance of plant: no design exists.
-- Power conditioning and recirculating power systems for sustained Q>1 operation: not designed.
+**Missing**: No tritium fuel handling subsystem described for the Orbitron device itself (FusionWERX will have external tritium infrastructure via MoU with FFC, but no Orbitron-integrated D-T fuel injector design is described). No first wall or chamber material selection for D-T neutron bombardment. No thermal energy conversion system at any TRL. No tritium breeding blanket concept at any stage.
 
 **Gaps**:
-- Energy conversion subsystem — `truly-unknown` — blocking
-- Tritium breeding design — `truly-unknown` — blocking
-- Balance of plant — `truly-unknown` — blocking
-- Power conditioning / recirculating power at Q>1 — `truly-unknown` — important
-- HTS magnet integration results (0.3–0.5 T) — `not-yet-sourced` (magnets ordered 2025–2026; results likely to appear in 2026 publications) — important
+- Tritium fuel injector integrated with Orbitron (D-T operation): no design disclosed — `proprietary` — **important**
+- Thermal energy conversion system: no concept at kWe scale — `truly-unknown` — **blocking**
+- Tritium breeding blanket: explicitly TBD — `truly-unknown` at this stage — **important** (near-term tritium would be purchased)
+- First wall material for 14 MeV neutron environment: not specified — `not-yet-sourced` — **important**
+- HTS magnet specification (REBCO vs. Bi-2212, winding configuration): not disclosed — `proprietary` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Poor
 
-**Available**:
-- Cathode: molybdenum (chosen for machinability and field emission properties); conditioning procedures described (current and gas conditioning to remove field emitters).
-- Anode: copper.
-- Insulator: MACOR ceramic (129 MV/m dielectric strength, machineable).
-- Vacuum system: standard UHV materials.
-- Magnets: neodymium Halbach array (current); HTS coils (planned).
-- Shielding: concrete (Marty "concrete castle" for x-ray and neutron shielding).
-- Tritium supply: MoU with Fusion Fuel Cycles (FFC) for fuel cycle support; FusionWERX designed for tritium handling.
-
-**Missing**:
-- First wall / inner chamber material under sustained neutron bombardment (14 MeV): no material selection or activation analysis at any power level.
-- Structural material assessment for a power-producing reactor at any scale.
-- Critical materials analysis: HTS wire (REBCO) supply chain for the superconducting magnets.
-- Tritium breeding material (Li-6 enrichment, blanket material): not discussed.
-- Material degradation / replacement schedule under neutron flux.
-- Supply chain risk for the novel 300 kV UHV bushing: custom design, no commercial supplier identified.
+**Available**: The AIP Advances paper identifies specific materials for the HV subsystem: molybdenum (cathode, for low field emission rates), copper (anode), MACOR ceramic (dielectric; 129 MV/m dielectric strength; machinable; used as UHV spacer), and potting compounds (oil, RTV silicone, or resin) at atmospheric pressure behind the bushing. Neodymium magnets for the 0.05 T Halbach array are used in current prototypes. Future research on alternative HV materials is noted as a priority item. Vacuum system uses commercial UHV components (cryopump). No supply chain analysis, no manufacturing readiness assessment, and no critical material risk analysis has been published.
+
+**Missing**: The Orbitron's proposed 1–100 kWe modular product implies mass manufacturing, but no manufacturing readiness level (MRL) assessment exists. HTS wire type and quantity for the superconducting magnet upgrade is unspecified. Near-term tritium supply strategy is not analyzed beyond noting FusionWERX will have handling capability. No neutron-tolerant structural material has been identified for the chamber wall under D-T bombardment.
 
 **Gaps**:
-- First wall material selection and activation analysis — `truly-unknown` (power reactor not yet designed) — important
-- HTS magnet supply chain for REBCO conductors — `not-yet-sourced` — nice-to-have
-- Tritium breeding material — `truly-unknown` — important
-- 300 kV UHV bushing commercial supply path — `proprietary` (Avalanche has a custom design; commercial availability unclear) — nice-to-have
+- Manufacturing readiness for key proprietary components (HV bushing, cathode): no assessment — `proprietary` — **important**
+- HTS wire supply (type, quantity, vendor): not disclosed — `not-yet-sourced` — **important**
+- Tritium supply cost and sourcing for D-T program: not analyzed — `not-yet-sourced` — **important**
+- First wall material selection and neutron tolerance: not analyzed — `truly-unknown` at this TRL — **important**
+- MACOR alternative materials for HV: flagged as future work in AIP paper — `not-yet-sourced` — nice-to-have
 
 ---
 
@@ -126,64 +84,73 @@
 **Coverage**: Poor
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
-|---|---|---|---|
-| Target net electrical output (per module) | 1–100 kWe | Orbitron product page | low (undemonstrated) |
-| Fusion power at target conditions | ~1 kW (at 300 kV, 0.3 T, D-T) | CWFest2023 scaling contour | low (extrapolated from PIC sim) |
-| Driver input power at target conditions | ~1 kW (600 W cathode + 400 W ion guns at ~1 kW fusion) | CWFest2023 | low (rough estimate from CEO) |
-| Energy conversion approach | Thermal cycle / turbines (neutron bombardment → heat) | Orbitron product page | low (undesigned) |
-| Cathode voltage (achieved) | 300 kV steady-state | 300 kV press release | high |
-| Magnetic field (target) | 0.3–0.5 T (HTS, not yet integrated) | AIP Advances, CWFest2023 | medium |
-| D-T neutron energy | 14.1 MeV | Standard physics | high |
-| Team size / funding (as of 2026) | 33+ people, $29M raised, $10M grant | Press releases | high |
-| FusionWERX Q>1 test date target | ~2027 (tritium licensing expected 2027) | $29M press release | medium |
+|-----------|-------------|--------|------------|
+| Net electric power per module | 1–100 kWe | Orbitron product page | m |
+| Cathode voltage (operating target) | 300 kV | 300 kV press release, AIP paper | h |
+| Magnetic field (target) | 0.3–0.5 T | AIP paper, CWFest blog | m |
+| Ion density target | >10¹¹ cm⁻³ | AIP paper (PIC: 5.4×10¹⁰ cm⁻³ achieved in simulation) | l |
+| Input power at Q~1 estimate | ~1000 W (600 W cathode + 400 W ion guns) | CWFest blog | l |
+| Fusion power at 300 kV / 0.3 T | ~1 kW (D-T) | CWFest blog (PIC-derived) | l |
+| Neutron yield target (D-T) | mid-10¹¹ n/s | CWFest blog | l |
+| Energy conversion pathway | Thermal + turbines (type unspecified) | Orbitron product page | l |
+| Fuel type | D-T (primary), D-D (current experiments) | Multiple sources | h |
+| Scale-up approach | Modular stacking to MW scale | Press releases | m |
+| Capital to first commercial ops (aspirational) | <$1B (company stated goal) | CWFest blog | l |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
-|---|---|---|---|
-| Capital cost (by CAS account) | truly-unknown | blocking | No plant design exists at any scale |
-| Energy conversion efficiency (thermal cycle η) | truly-unknown | blocking | Not designed; at kWe scale, conventional Rankine is impractical |
-| Capacity factor / availability | truly-unknown | blocking | No operational data; first sustained D-T run hasn't happened |
-| O&M costs | truly-unknown | blocking | No engineering basis; device not in sustained operation |
-| Plant scaling to commercial output (MWe) | truly-unknown | blocking | Company says modular stacking but no analysis published |
-| Recirculating power fraction | truly-unknown | blocking | Q>1 not yet demonstrated; wall-plug efficiency of power supplies uncharacterized |
-| Fuel cost (tritium procurement) | derivable | important | Can be estimated from market price at small tritium mass; breeding not viable at this scale |
-| Decommissioning cost | truly-unknown | nice-to-have | Activation levels unknown |
-| Construction time | truly-unknown | important | No commercial plant design; desktop scale suggests fast, but modular MWe plant undefined |
+|-----------|----------|-------------|-------|
+| Capital cost breakdown (by CAS account) | truly-unknown | blocking | No plant study; device doesn't yet demonstrate net energy |
+| Thermal conversion efficiency (η_th) | truly-unknown | blocking | No cycle type specified; at 1–100 kWe, conventional steam turbines are not viable |
+| Plant capacity factor | truly-unknown | blocking | No maintenance model; no lifetime estimate |
+| Q at commercial scale (engineering gain) | truly-unknown | blocking | Only Q~1 targeted for D-T test; commercial plant needs Q_eng >1 after recirculation losses |
+| O&M costs | truly-unknown | blocking | No facility operating cost model exists |
+| Tritium cost ($/g) and annual consumption | not-yet-sourced | important | Near-term purchased tritium; breeding blanket TBD |
+| Plant lifetime | truly-unknown | important | Not disclosed |
+| First wall replacement schedule | truly-unknown | important | 14 MeV neutron fluence on compact geometry untested |
+| Decommissioning cost | derivable | nice-to-have | Could use fission analog at low activation levels |
+| Balance of plant costs | derivable | important | Could use standard power industry analogs if cycle type were known |
+
+**Fleet-wide source disposition**:
+
+- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Opened and read. The four concepts are Plasma-Jet MIF (HyperJet Fusion), Stabilized Liner Compressor (CFS), Staged Z-Pinch (MIFTI), and Flow-Stabilized Z-Pinch (Zap Energy) — all pulsed MIF at ~500 MWe plant scale. The Orbitron operates at 1–100 kWe per module, a scale 4–6 orders of magnitude smaller; the CAS cost structure and plant economics do not transfer. **Disqualified**: wrong confinement family, wrong power scale, no cost analog applicable to electrostatic kWe-scale devices.
+
+- **Progress toward fusion energy breakeven (Lawson criterion)** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Opened and read. The paper explicitly states it "does not consider non-thermal ion or electron populations such as those with beam-like distributions" and notes that non-thermal approaches face the Rider (1995) constraint. The Orbitron is a non-Maxwellian beam-beam device, placing it outside this paper's scope for Lawson benchmarking. The paper does confirm the fundamental theoretical challenge for non-thermal approaches cited in the CWFest blog. **Disqualified for Lawson benchmarking**: methodology explicitly excludes non-thermal plasma; no Orbitron-applicable data points exist in the compilation.
+
+- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Covers D-T MFE at ~1 GWe tokamak scale with CAS 20–29 cost breakdowns. The Orbitron is 7+ orders of magnitude smaller; BOP and cost driver structures are completely different. D-T fuel cycle fraction would be similarly irrelevant given the scale mismatch. **Disqualified**: scale mismatch makes all cost analogs inapplicable.
 
 ---
 
 ## Source Recommendations
 
-- **Full text of *Physics of Plasmas* 32(9), 092105 (2025)**: "Mode-enhanced ion loading in a 100 kV orbitrap" — `not-yet-sourced` — likely contains confinement time measurements and density-above-space-charge-limit experimental data from Marty. Search OSTI or AIP Scitation by DOI (appears to be from the same team). This is the highest-priority missing source for Section 2 and Section 3.
+1. **Physics of Plasmas 32(9), 092105 (Sep 2025)** — Avalanche paper "Mode-enhanced ion loading in a 100 kV orbitrap" — likely contains ion confinement time measurements and mode-loading characterization at higher density. `not-yet-sourced`; search OSTI or AIP Scitation. This is the highest-priority acquisition for §2 and §3.
 
-- **Any additional 2025–2026 conference papers from Avalanche Energy** (APS DPP 2025): The DPP 2024 abstract (`meetings-meeting-dpp24-session-np12-69.md`) suggests ongoing experimental work on space-charge collective effects. Search APS/arXiv for Affolter, Merthe, Langtry (2025). `not-yet-sourced`.
+2. **APS DPP24 poster NP12.69 (Merthe et al., Oct 2024, Atlanta)** — "Collective Effects near the Ion Space-Charge Limit of the Orbitron" — abstract captured, content not available. Could contain experimental data on space-charge mitigation and confinement at higher density. `not-yet-sourced`; contact Avalanche or search OSTI for preprint.
 
-- **IEC/fusor analogues for power balance**: Published analyses of Bremsstrahlung vs. fusion power for non-thermal D-T plasmas (e.g., Rider 1997 *Phys. Plasmas* 4, 1039 — cited in AIP paper as Ref. 58, not ingested). Relevant for Section 2 power balance analysis. `not-yet-sourced` — search OSTI or AIP for Rider 1997.
+3. **Fusion Fuel Cycles (FFC) MoU documentation** — Avalanche signed an MoU with FFC for tritium breeding blanket development. FFC may have published any D-T fuel cycle analysis relevant to small-scale fusion devices. Search FFC website and proceedings for tritium blanket sizing at kWe scale. `not-yet-sourced`; existence of any published analysis unverified.
 
-- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): The four ALPHA concepts (none electrostatic) used modular/compact architectures. The CAS methodology could provide a structural analog for how to organize a cost model for the Orbitron even without specific numbers. Likely to have limited applicability to kWe-scale electrostatic fusion, but worth checking the BOP/indirect cost treatment for modular concepts. Use as a methodology reference only — do not import ALPHA cost numbers as Orbitron analogs.
+4. **IEC / Farnsworth-Hirsch fusor TRL and cost literature** — The Orbitron is a close relative of inertial electrostatic confinement (IEC) devices, which have more published literature on scaling, wall bombardment, and vacuum system costs. Search OSTI for "IEC fusion economics" or "neutron generator cost model." Might provide BOP cost analogs. `not-yet-sourced`; confirmed to exist as a research area.
 
-- **No fleet-wide source in the SOURCE_INDEX is directly applicable** to electrostatic hybrid cost estimation. The MFE D-T TEA sources, IFE sources, and stellarator sources all assume thermal plasmas, gigawatt-scale plants, and standard tokamak/stellarator architectures that do not translate to a 1–100 kWe electrostatic device.
+5. **Small-scale neutron generator cost data** — Commercial D-T neutron generators (Adelphi, Sodern, ThermoFisher) publish cost and operating data in the 10⁸–10¹¹ n/s range. These are the closest commercial analogs to the FusionWERX neutron source application. Could anchor capital cost and O&M estimates for the near-term product. `not-yet-sourced`; search vendor literature and published nuclear instrumentation studies.
 
 ---
 
 ## Summary
 
-The available data is sufficient to write a technically detailed qualitative analysis of the Orbitron concept — covering the physics basis, company status, experimental progress through Marty/300 kV milestone, key physics challenges (Coulomb collisions, space charge, Bremsstrahlung), and the competitive context of non-thermal electrostatic fusion. However, a quantitative LCOE analysis is not feasible: the device has not achieved Q>1, no power reactor has been designed at any scale, and all cost parameters (capital, O&M, capacity factor, energy conversion efficiency) are either unavailable (proprietary), not yet designed (truly-unknown), or undefined (the concept is at TRL 3–4 with no commercial plant geometry). Acquiring the Physics of Plasmas 2025 paper and any APS 2025 abstracts would improve Section 3 (subsystem maturity), but would not unlock LCOE analysis. Proceed to qualitative D1 analysis; mark LCOE quantitative parameters as data-insufficient and describe the critical path to resolving them.
+Sufficient data exists to write a qualitative description of the Orbitron concept — confinement mechanism, device architecture, subsystem TRL landscape, key physics challenges, and near-term program status. The AIP Advances 2024 paper in particular provides substantial engineering detail at prototype scale. However, the concept is pre-Q=1, has no capital cost data, no thermal conversion design, and no plant study. The LCOE section will require large assumptions (or explicit acknowledgment that no numbers can be responsibly derived). Acquiring the Physics of Plasmas Sep 2025 paper before writing §2 (system function) and §3 (subsystem maturity) would materially improve the confinement time characterization. The concept qualifies for a qualitative D1+ analysis with heavy caveats on LCOE — proceed with flagged assumptions rather than withholding analysis.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Insufficient Data"
+overall_rating: "Significant Gaps"
 blocking_count: 6
-important_count: 7
-counting_method: "deduplicated_across_all_sections — blocking: (1) Q>1 physics/power balance basis, (2) energy conversion system design, (3) capital cost data, (4) O&M cost data, (5) capacity factor/availability, (6) tritium breeding design. Important: (1) Physics of Plasmas 2025 full paper, (2) confinement time/density scaling data, (3) Bremsstrahlung characterization, (4) HTS magnet integration results, (5) first wall material selection, (6) tritium breeding material, (7) commercial plant scaling analysis."
+important_count: 12
+counting_method: "all_sections_deduplicated — blocking: non-thermal Q feasibility, confinement time at target density, thermal conversion system architecture/efficiency, capital cost for Q>1 system, plant capacity factor, O&M costs (plant-level); important: no independent assessment, Physics of Plasmas paper not captured, bremsstrahlung budget unpublished, collective instabilities at high density, tritium breeding undefined, tritium fuel injector design, first wall material, HTS magnet specification, manufacturing readiness, HTS supply chain, tritium supply cost, balance of plant"
 section_coverage:
-  availability_of_data:       "Partial"
+  availability_of_data:       "Poor"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
```
