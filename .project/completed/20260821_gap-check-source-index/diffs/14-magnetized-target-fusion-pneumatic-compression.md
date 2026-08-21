# Diff: 14-magnetized-target-fusion-pneumatic-compression

**Generated:** 2026-05-22T10:12:35-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 4 | 0 |
| important_count  | 8 | 5 | - |
| overall_rating   | Mostly Ready (with significant LCOE-specific gaps) | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
165:**Fleet-wide source to open**: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — The ARPA-E ALPHA program specifically targeted low-cost alternative fusion approaches; at least one of the four costed concepts may have been an MTF/MIF concept. Read `output.md` to check whether any MIF/liner concept was included. If so, this is the strongest available cost analog. Flag: **read before finalizing LCOE model**.
167:**Fleet-wide source to use for BOP/O&M analogs**: `knowledge/sources/tea_dt_mfe_cost_analysis/` — Standard D-T MFE BOP cost structure (balance of plant, Rankine cycle, tritium handling, decommissioning) should apply directly to GF MTF. The piston array replaces the magnet system; subtract CAS22/23 magnet costs, substitute a piston-array cost estimate.
169:**PyFECONS**: `~/PyFECONS` — Useful for the LCOE calculation framework and CAS hierarchy. MFE and MIF modules may exist; check whether an MTF-specific configuration is included.
```

## Blocking-tier lines (baseline)

```
30:- No plant study or system code output — `proprietary` — **blocking** (no structured cost baseline exists)
53:- Recirculating power fraction for piston system — `proprietary` — **blocking** (drives net electrical efficiency; cannot close energy balance without it)
54:- Commercial Q target — `proprietary` — **blocking** (cannot estimate gross fusion power or energy gain)
76:- Pneumatic piston compression at any scale — `not-yet-sourced` — **blocking** (critical to TRL assessment; patent literature may contain design details; search USPTO/Google Patents for General Fusion piston patents)
77:- Liquid metal vortex stability at commercial repetition rate — `truly-unknown` — **blocking** (no experiment approaching this has been reported)
129:| Fusion gain Q (commercial target) | proprietary | blocking | Cannot close energy balance or derive gross fusion power |
130:| Recirculating power fraction (piston steam) | proprietary | blocking | Pistons powered by steam; fraction consumed could dominate net efficiency |
132:| Capital cost (any subsystem) | proprietary | blocking | No plant cost study or breakdown published |
133:| Piston system capital cost | proprietary | blocking | No analogues for this specific system exist in literature |
```

## Blocking-tier lines (new)

```
36:- Published plant economics study (CDR-level) — `proprietary` — **blocking**: Without it, capital cost structure cannot be grounded
37:- Commercial plant Q value / fusion energy gain — `proprietary` — **blocking**: Determines whether net electricity output closes without extraordinary Q assumptions
60:- Recirculating power fraction — `proprietary/derivable` — **blocking**: This directly determines net electrical output and LCOE; no analog or published estimate exists
146:| Net fusion energy gain (Q) for commercial plant | proprietary | blocking | LM26 targets Lawson criterion, not Q > 1; commercial Q not stated anywhere |
147:| Recirculating power fraction (pistons) | proprietary | blocking | Steam partly powers pistons; fraction not published; drives net output |
148:| Thermal cycle efficiency (steam cycle parameters: T, P) | derivable | blocking | Can assume ~33–35% Rankine but steam T depends on liquid metal operating temp, which is not published |
150:| Capital cost by subsystem | proprietary | blocking | No published estimate; no CDR or plant study publicly available |
151:| Total capital cost (FOAK or nth-of-a-kind) | proprietary | blocking | Not published anywhere in sourced literature |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/14-magnetized-target-fusion-pneumatic-compression.md	2026-05-22 09:21:13.851465318 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/14-magnetized-target-fusion-pneumatic-compression/gap_report.md	2026-05-22 10:12:35.753649213 -0700
@@ -1,59 +1,64 @@
+Now I have enough information to write the gap assessment. Let me compile the full report.
+
+---
+
 # Gap Assessment: Magnetized Target Fusion - Pneumatic Compression (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready (with significant LCOE-specific gaps)
-
-**Summary**: General Fusion is unusually transparent about physics and architecture for a private fusion company — the concept's operating principle, system configuration, liquid metal roles, and commercial targets are well-documented in peer-reviewed literature and company materials. However, essentially no cost data (capital, operating, or performance-economic parameters) has been published, and several critical commercial-scale subsystems (pneumatic piston array, liquid metal handling at 1 Hz, recirculating power fraction) have no public analogues or estimates. A first-pass LCOE model can be constructed with stated assumptions, but the capital cost side will require analogue-based estimation throughout.
+**Rating**: Significant Gaps
+**Summary**: General Fusion is among the more transparent private fusion companies — 34 peer-reviewed publications, active national lab collaborations, and a 2025 peer-reviewed fuel cycle study provide solid physics and fuel cycle data. However, no published plant economics study, capital cost breakdown, LCOE estimate, or net Q target for the commercial plant exists anywhere in the sourced literature. The LCOE analysis is severely constrained by the absence of basic economic parameters, and two key system uncertainties (recirculating power fraction, liquid metal selection) propagate directly into cost structure uncertainty.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Partial
 
 **Available**:
-- Peer-reviewed physics results from LM26 compression experiments (Nuclear Fusion journal, 2025 — cited in dossier sources)
-- FST 2025 paper (Fuel Cycles, doi:10.1080/15361055.2025.2526266): confirms pneumatic pistons, ~4 m cavity diameter, liquid metal composition candidates (Li vs. PbLi), tritium inventory analysis
-- IAEA FEC 2025 abstract: 50% scale confirmation, milestone targets (10 keV by 2025, Lawson by 2026)
-- Company website: concept description, tritium breeding role, liquid metal wall function, commercial target (300 MWe, ~1 Hz)
-- APS 2018 overview: compression parameter ranges (density 10²²→10²⁵ m⁻³, temp 0.1→10 keV, B-field 2→200 T)
-- 34 peer-reviewed publications and 210 patents (per company, though most not ingested)
+- Company description of technology concept and commercial target (300 MWe from two 150 MWe units, ~1 Hz, ~4 m cavity diameter): `generalfusion.com/fusion-technology/`, `generalfusion.com/commercialization-path/`
+- Peer-reviewed plasma performance data: >10 ms energy confinement time, ~6×10^19 m^-3 density, >400 eV temperature without active stabilization or auxiliary heating: `generalfusion-post-peer-reviewed-publication-confirms.md`, `globenewswire-news-release-2022-12-12...md`
+- Compression parameters: density target 10^22 to 10^25 ions/m^3, temperature 0.1 to 10 keV, magnetic field 2 to 200 T: dossier citing APS 2018 overview
+- LM26 experimental milestone (April 2025): first integrated plasma compression with lithium liner showing ion temperature and density increases: `metaltechnews-story-2025-05-14...md`
+- Detailed fuel cycle analysis for both PbLi and pure Li blanket options: tritium inventories, TBR values, startup inventory (<1 kg), plant doubling time: `general-fusion-fst-2025-fuel-cycles.md`
+- Commercialization roadmap: Lawson Program (LM26 to mid-2028), then commercialization engineering program, FOAK plant ~2035: `generalfusion-fusion-demo-plant.md`
+- Company collaborations: Hatch (power plant engineering), Kyoto Fusioneering (tritium/liquid metal BOP), CNL (BOP integration study April 2024), PPPL, ORNL, SRNL: `en-wiki-general-fusion.md`
+- Financial and organizational context including May 2025 layoffs (~25% of workforce) and January 2026 SPAC merger plans: `en-wiki-general-fusion.md`
 
 **Missing**:
-- Published plant/power study (no equivalent of ARIES, DEMO, or STARFIRE-style plant report)
-- Techno-economic assessment or pre-FEED study
-- System code outputs (no PROCESS or equivalent published)
-- Independent third-party technical reviews
+- No published plant economics study or conceptual design report (CDR)
+- No LCOE estimate from company or any third party
+- No published Q (fusion gain) target for the commercial plant — LM26 targets the Lawson criterion (nTτ > 10^21 m^-3·keV·s), not Q > 1
+- Hatch/CNL BOP integration study from April 2024 not publicly available
+- No published piston count, piston specifications, or driver cost estimates for the commercial design
 
 **Gaps**:
-- No plant study or system code output — `proprietary` — **blocking** (no structured cost baseline exists)
-- 34 peer-reviewed publications largely uninspected — `not-yet-sourced` — **important** (technical details on piston design, liner dynamics, and plasma performance may exist)
-- No independent techno-economic analysis published — `truly-unknown` — **important** (academic groups have not yet published MTF cost models)
+- Published plant economics study (CDR-level) — `proprietary` — **blocking**: Without it, capital cost structure cannot be grounded
+- Commercial plant Q value / fusion energy gain — `proprietary` — **blocking**: Determines whether net electricity output closes without extraordinary Q assumptions
+- Hatch/CNL BOP integration study (April 2024) — `proprietary` — **important**: Could resolve BOP cost and integration questions
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Clear description of energy flow: fusion neutrons → liquid metal heating → heat exchanger → steam → turbine + piston power
-- Understanding of pulsed nature: ~1 Hz, ~1 ms compression, discrete burn events
-- Liquid metal triple function (compression medium, neutron absorber, tritium breeder) is well documented
-- Plasma formation via Marshall gun (compact toroid) is described
+The sources clearly enumerate the key physics and engineering unknowns, which is essential for identifying where the LCOE model will carry the most uncertainty:
+
+- **Recirculating power fraction**: Steam from the Rankine cycle partially drives the pistons (`en-wiki-general-fusion.md`: "some of the steam is recycled to power the pistons"). The fraction consumed by piston recharge versus delivered to the grid is not quantified anywhere in the sources. This is the central LCOE uncertainty — a large recirculating fraction would dramatically cut net electrical output.
+- **High-vacuum re-establishment at 1 Hz**: Wikipedia explicitly identifies this as an unresolved engineering obstacle; the 70% scale UK demo planned at 1 pulse/day specifically avoided this problem (86,400× more time to re-establish vacuum). At 1 Hz this requires solving in <1 second.
+- **Plasma-liner instability at fusion conditions**: Wikipedia lists "confinement at high energy density is not known," liquid metal vaporization (LLNL collaboration ongoing), and plasma cooling by liquid metal impurities as open challenges.
+- **Liquid metal selection undecided**: PbLi vs. pure Li each has different TBR, plasma contamination behavior (Pb is high-Z, contaminates plasma via Bremsstrahlung), tritium extraction complexity, and materials compatibility. FST 2025 paper confirms neither has been selected.
+- **Piston synchronization at 4 m scale**: Prototype demonstrated 2 μs timing at 1 m scale. Commercial cavity is ~4 m diameter; synchronization scaling and structural dynamics are not demonstrated.
 
 **Missing**:
-- **Recirculating power fraction**: Steam from the thermal cycle powers the pistons. The fraction of gross power consumed by piston recharging is undisclosed and could be 20–50%+ — this is the dominant LCOE driver after capital cost.
-- **Gain (Q) assumptions**: No commercial Q target has been published. Without Q, net electrical output cannot be calculated.
-- **Piston synchronization and reset time**: The pistons must fire, retract, and recharge within 1 second. Whether this is achievable with steam at commercial scale is undocumented.
-- **Plasma formation energy cost**: The Marshall gun consumes energy each pulse; no estimate available.
-- **Energy balance at 1 Hz**: No published analysis of whether the energy balance (power in from steam to pistons vs. power out from fusion) closes at the commercial scale.
+- No system code output (PROCESS, SYSCODE, etc.) for this concept
+- No published analysis of recirculating power fraction
+- No published driver efficiency (piston energy → plasma kinetic energy conversion efficiency)
 
 **Gaps**:
-- Recirculating power fraction for piston system — `proprietary` — **blocking** (drives net electrical efficiency; cannot close energy balance without it)
-- Commercial Q target — `proprietary` — **blocking** (cannot estimate gross fusion power or energy gain)
-- Piston reset feasibility at 1 Hz — `not-yet-sourced` — **important** (mechanical engineering papers may exist; search OSTI/Google Scholar for "magnetized target fusion piston repetition" or General Fusion patent filings)
-- LM26 → commercial scale-up physics fidelity — `truly-unknown` — **important** (LM26 uses electromagnetic compression, not pneumatic; pneumatic system at commercial scale never tested)
+- Recirculating power fraction — `proprietary/derivable` — **blocking**: This directly determines net electrical output and LCOE; no analog or published estimate exists
+- Vacuum re-establishment solution — `not-yet-sourced` — **important**: OSTI/conference literature may have GF or community work on this; unresolved in sources
 
 ---
 
@@ -61,22 +66,27 @@
 **Coverage**: Partial
 
 **Available**:
-- **Plasma injector (Marshall gun / compact toroid)**: Demonstrated at LM26 scale (50% of commercial plasma size). >10 ms confinement time confirmed (peer-reviewed). TRL ~4.
-- **Electromagnetic compression (LM26 surrogate)**: Operational. 18 MJ coils, 2 m diameter. Ion temperature increase and 190× density compression confirmed. TRL ~4 for this configuration.
-- **Liquid metal handling (basic)**: General Fusion demonstrated liquid lithium contact with plasma (2019). TRL ~3.
-- **Steam Rankine BOP**: Mature commercial technology. TRL 9.
+
+| Subsystem | TRL Assessment | Basis in Sources |
+|-----------|---------------|-----------------|
+| Plasma injector (compact toroid) | TRL 5–6 | >10 ms confinement at 50% commercial scale demonstrated (PI3/LM26); ~400 eV, 6×10^19 m^-3 without auxiliary heating |
+| Lithium liner compression (electromagnetic) | TRL 4–5 | LM26 integrated test April 2025; initial diagnostics show ion temp/density increase; >1,000 shots on compression prototype |
+| Pneumatic piston system (commercial) | TRL 3–4 | Collaboration with "major automaker" ongoing; 1 m prototype demonstrated (2012–2013) at 50 m/s, 2 μs timing; 4 m commercial scale not demonstrated |
+| Liquid metal vortex flow system | TRL 3–4 | 1:10 scale water compression demonstrated (2021–2022); no full liquid metal vortex at power-plant scale |
+| Tritium breeding/extraction (LLE) | TRL 3–4 | SRNL analysis complete; GLC at 40% efficiency chosen; low TRL for fusion-scale throughputs |
+| Tritium breeding/extraction (pure Li) | TRL 2–3 | LiT electrolysis at "very low TRL" (FST 2025); blanket extraction the critical technology |
+| Heat exchanger / Rankine cycle | TRL 7–8 | Standard industrial technology; liquid metal coupling is an integration challenge but not novel |
+| Seals, valves, liquid metal BOP | TRL 3–4 | Specifically called out by GF commercialization page as the next engineering program focus; not yet designed |
+| High-vacuum re-establishment at 1 Hz | TRL 1–2 | Not demonstrated; explicitly unresolved in Wikipedia |
 
 **Missing**:
-- **Pneumatic piston array at commercial scale**: LM26 uses electromagnetic compression as a surrogate — the commercial pneumatic system has not been tested at any scale representative of the 4 m commercial cavity. This is the most critical undemonstrated subsystem.
-- **Liquid metal vortex formation at commercial rep rate**: Whether the liquid metal can form a stable vortex cavity, accept a plasma, be compressed, and be re-established 1×/second is undemonstrated.
-- **Tritium extraction system**: Li and PbLi extraction are analyzed in FST 2025 but no experimental demonstration cited.
-- **First wall / structural materials**: The liquid metal wall eliminates solid first-wall issues, but the pressure vessel and piston ports must survive radiation and thermal cycling.
+- TRL data for piston synchronization electronics at commercial scale
+- No published materials qualification data for seals/valves in Li or PbLi environments at operating temperatures
+- Plasma-liner integrated test with pneumatic pistons (not electromagnetic) — not yet performed
 
 **Gaps**:
-- Pneumatic piston compression at any scale — `not-yet-sourced` — **blocking** (critical to TRL assessment; patent literature may contain design details; search USPTO/Google Patents for General Fusion piston patents)
-- Liquid metal vortex stability at commercial repetition rate — `truly-unknown` — **blocking** (no experiment approaching this has been reported)
-- Tritium extraction system TRL — `not-yet-sourced` — **important** (FST 2025 paper covers inventory but not extraction technology maturity)
-- Radiation damage to piston actuators/ports — `truly-unknown` — **important** (neutron streaming through piston channels is a unique challenge with no clear analogue)
+- Pneumatic piston + liquid metal vortex integrated demonstration — `truly-unknown` (awaiting demonstration) — **important**: The commercial concept has not been tested in this configuration at any scale; LM26 uses a different compression mechanism
+- Vacuum re-establishment at 1 Hz — `not-yet-sourced` — **important**: May be addressed in GF conference papers or INFUSE reports not captured in Phase 1a
 
 ---
 
@@ -84,105 +94,107 @@
 **Coverage**: Partial
 
 **Available**:
-- Liquid metal identified as Li or PbLi (FST 2025 — both under evaluation)
-- TBR target ~1.5 (Fusion Conclusion blog, dossier)
-- Li-6 enrichment needed for tritium breeding from natural lithium is implicit (Li-6 is the active isotope)
-- D-T fuel cycle confirmed (standard tritium supply chain issues apply)
+- Liquid metal: PbLi or pure Li — both identified, compositions known; neither selected for commercial plant (FST 2025)
+- Lithium supply: commercially available; Li-6 enrichment for higher TBR is an option but natural Li is baselined in some designs
+- Tritium startup inventory: <1 kg (317 g for LLE, ~750 g for Li designs) — manageable from CANDU supply (FST 2025)
+- No superconducting magnets required — eliminates REBCO tape supply chain bottleneck (a key competitive advantage)
+- No high-power lasers or pulse power systems required — conventional mechanical engineering
+- Piston technology: collaboration with "a major automaker" (company unnamed) suggests integration into existing manufacturing supply chains
+- Structural materials: conventional steels; no plasma-facing materials problem (liquid metal wall eliminates first-wall damage)
 
 **Missing**:
-- **Li-6 enrichment requirement**: Li-6 is ~7.5% of natural lithium. Commercial tritium breeding requires enriched Li-6 (typically 30–90%). The commercial enrichment pathway (CECE process or other) is not discussed.
-- **Lithium inventory for a 300 MWe plant**: The liquid metal volume at ~4 m cavity at 1 Hz operation is significant. Total plant lithium inventory not published.
-- **Piston materials**: The commercial pistons must withstand steam pressure cycling, potentially neutron flux through piston ports, and thermal gradients. Material specifications are not published.
-- **Structural materials**: Pressure vessel, piston housing — material choices not disclosed.
-- **Lead supply (if PbLi)**: Lead-lithium eutectic is ~83% lead by mass. Large volume requirements; supply chain implications not analyzed.
+- Piston count and specifications for commercial design are not published; cost-of-goods for the piston array is the primary capital cost unknown that is unique to this concept
+- Li-6 enrichment requirements and supply chain not analyzed in available sources
+- PbLi materials compatibility with structural steels at operating temperatures — partially addressed in broader fusion literature but not in GF-specific sources
+- No published manufacturing plan or supply chain analysis for the piston system
 
 **Gaps**:
-- Li-6 enrichment pathway and cost — `not-yet-sourced` — **important** (standard fusion fuel cycle literature applies; ORNL and ITER documentation are authoritative)
-- Plant lithium/PbLi inventory (and associated cost) — `derivable` from cavity geometry and density assumptions — **important**
-- Piston material specifications — `proprietary` — **nice-to-have** (analogues from steam/pneumatic engineering exist)
-- Tritium startup inventory — `derivable` from TBR target and fusion power assumptions — **important**
+- Piston array manufacturing cost/supply chain — `proprietary` — **important**: The piston array is the concept-defining cost item with no analog in other fusion approaches; no data available
+- Li-6 enrichment requirements — `derivable` from TBR analysis but not stated — **nice-to-have**
+- PbLi materials compatibility data — `not-yet-sourced` — **nice-to-have**: Exists in the broader fusion materials literature (EUROFER, etc.)
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plant power output | 300 MWe | LM26 milestones, GF commercialization page | h |
-| Repetition rate | ~1 Hz | Multiple sources | h |
-| Cavity diameter | ~4 m | FST 2025 paper | h |
-| Compression timescale | ~1 ms | APS 2018, technical details | h |
-| Pre-compression density | 10²² m⁻³ | APS 2018 | m |
-| Peak density | 10²⁵ m⁻³ | APS 2018 | m |
-| Pre-compression temperature | ~0.1 keV | APS 2018 | m |
-| Target temperature | 10 keV | LM26 milestones, IAEA FEC 2025 | h |
-| Energy conversion pathway | Steam Rankine | Multiple sources | h |
-| Tritium breeding ratio target | ~1.5 | Fusion Conclusion / dossier | m |
-| Plasma scale (LM26) | 50% of commercial | IAEA FEC 2025 | h |
-| Commercial deployment timeline | Early-mid 2030s | COMSOL, dossier | m |
-| Fuel type | D-T | All sources | h |
+| Net electrical output (commercial) | 300 MWe (2×150 MWe) | `generalfusion-post-peer-reviewed-publication-confirms.md`, `en-wiki-general-fusion.md` | H |
+| Repetition rate (commercial) | ~1 Hz | dossier (multiple sources) | H |
+| Cavity diameter (commercial) | ~4 m | FST 2025 (`general-fusion-fst-2025-fuel-cycles.md`) | H |
+| Plasma compression ratio | ~350× volumetric | FST 2025 | H |
+| Fuel type | D-T | multiple | H |
+| Energy conversion | Thermal Rankine (steam) | multiple | H |
+| TBR (LLE design) | 1.4 | FST 2025 | H |
+| TBR (Li design) | 1.25–1.80 | FST 2025 | H |
+| Tritium startup inventory (LLE) | ~317 g | FST 2025 | M |
+| Tritium startup inventory (Li) | ~750–800 g | FST 2025 | M |
+| Pre-compression plasma density | ~6×10^19 m^-3 | `globenewswire...` press release | M |
+| Pre-compression confinement time | >10 ms | `peer-reviewed-publication-confirms.md` | H |
+| Pre-compression temperature | >400 eV | `globenewswire...`, IAEA FEC 2025 | H |
+| Target compression temperature | 10 keV | IAEA FEC 2025 | H |
+| Target post-compression density | ~10^25 ions/m^3 | dossier (APS 2018) | M |
+| FOAK plant operations target | ~2035 | `generalfusion-fusion-demo-plant.md` | M |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion gain Q (commercial target) | proprietary | blocking | Cannot close energy balance or derive gross fusion power |
-| Recirculating power fraction (piston steam) | proprietary | blocking | Pistons powered by steam; fraction consumed could dominate net efficiency |
-| Thermal efficiency of steam cycle | derivable | important | No steam parameters published; standard Rankine ~33–38% can be assumed |
-| Capital cost (any subsystem) | proprietary | blocking | No plant cost study or breakdown published |
-| Piston system capital cost | proprietary | blocking | No analogues for this specific system exist in literature |
-| Liquid metal system capital cost | not-yet-sourced | important | Molten salt and LBE analogues from fission may provide bounds |
-| Annual piston replacement rate | proprietary | important | Mechanical fatigue in pulsed service is the key lifetime driver |
-| Liquid metal pump/handling opex | not-yet-sourced | important | Industrial analogues from sodium-cooled fission reactors may exist |
-| Plasma injector replacement rate | proprietary | important | Marshall gun wear at 1 Hz × 8760 hr/yr ≈ 31M shots/yr |
-| Capacity factor / availability | truly-unknown | important | No published estimate; piston maintenance cycles not disclosed |
-| Net plant efficiency (gross to net) | derivable | important | Requires Q, recirculating power, and thermal efficiency |
-| Tritium startup inventory cost | derivable | important | Standard D-T fusion economics; ~$30K/g current tritium price |
-| Plant footprint / land cost | not-yet-sourced | nice-to-have | No published plant layout |
+| Net fusion energy gain (Q) for commercial plant | proprietary | blocking | LM26 targets Lawson criterion, not Q > 1; commercial Q not stated anywhere |
+| Recirculating power fraction (pistons) | proprietary | blocking | Steam partly powers pistons; fraction not published; drives net output |
+| Thermal cycle efficiency (steam cycle parameters: T, P) | derivable | blocking | Can assume ~33–35% Rankine but steam T depends on liquid metal operating temp, which is not published |
+| Liquid metal operating temperature | proprietary | important | Determines steam cycle temperature and thus thermal efficiency |
+| Capital cost by subsystem | proprietary | blocking | No published estimate; no CDR or plant study publicly available |
+| Total capital cost (FOAK or nth-of-a-kind) | proprietary | blocking | Not published anywhere in sourced literature |
+| Piston array cost (unit count × unit cost) | proprietary | important | Concept-defining cost item; not analogous to any costed fusion concept |
+| O&M annual cost estimate | proprietary | important | Not published; Rankine cycle analogs exist but piston maintenance is concept-specific |
+| Capacity factor / availability | derivable | important | No published estimate; piston maintenance frequency and duration unknown |
+| Plant lifetime (years) | derivable | nice-to-have | No published estimate; assume 30–40 years as fusion default |
+| First wall replacement schedule | not applicable | — | Liquid metal wall eliminates this cost item (advantage) |
+| Driver energy per pulse | proprietary | important | Not published; needed to calculate recirculating power |
+| Fusion power per pulse | derivable | important | Can be estimated from cavity volume + compression ratio + burn fraction, but burn fraction not published |
+| Burn fraction (β) | partially available | important | FST 2025 gives β = 0.0163 (LLE) and 0.0206 (Li) for fuel cycle modeling — usable |
 
 ---
 
 ## Source Recommendations
 
-1. **General Fusion patent portfolio** — `not-yet-sourced` — Search USPTO/Google Patents for "General Fusion" assignee. Piston design, synchronization control, and liquid metal vortex formation may be described in patents. Flag as `unverified — confirm existence before searching`.
+**Fleet-wide source to open**: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — The ARPA-E ALPHA program specifically targeted low-cost alternative fusion approaches; at least one of the four costed concepts may have been an MTF/MIF concept. Read `output.md` to check whether any MIF/liner concept was included. If so, this is the strongest available cost analog. Flag: **read before finalizing LCOE model**.
 
-2. **General Fusion's 34 peer-reviewed publications** — `not-yet-sourced` — The dossier cites company press releases about peer-reviewed publications; the actual papers are likely on Google Scholar under "General Fusion" OR "magnetized target fusion" OR "MTF piston." APS and Nuclear Fusion journal are most likely venues.
+**Fleet-wide source to use for BOP/O&M analogs**: `knowledge/sources/tea_dt_mfe_cost_analysis/` — Standard D-T MFE BOP cost structure (balance of plant, Rankine cycle, tritium handling, decommissioning) should apply directly to GF MTF. The piston array replaces the magnet system; subtract CAS22/23 magnet costs, substitute a piston-array cost estimate.
 
-3. **OSTI search for MTF system studies** — `not-yet-sourced` — Search OSTI for "magnetized target fusion power plant" or "MTF economics." DOE-funded MTF work (e.g., LANL FRX-L program) may include system-level analyses. Flag as `unverified — confirm existence before searching`.
+**PyFECONS**: `~/PyFECONS` — Useful for the LCOE calculation framework and CAS hierarchy. MFE and MIF modules may exist; check whether an MTF-specific configuration is included.
 
-4. **Lead-lithium / sodium-cooled fission BOP analogues** — `not-yet-sourced` — For liquid metal handling cost analogues, sodium fast reactor (SFR) plant studies (e.g., ARC-100, EBR-II) and Gen IV designs provide documented liquid metal pump, heat exchanger, and piping cost estimates. IAEA and DOE have published these.
-
-5. **ITER tritium systems documentation** — `not-yet-sourced` — For tritium extraction system costs and Li-6 enrichment chain, ITER's tritium breeding and processing documentation (published by ITER Organization) provides quantitative cost analogues usable with stated scale assumptions.
-
-6. **MTF system code / conceptual design study** — `truly-unknown` — No academic MTF plant study equivalent to ARIES (tokamak) is known to exist. If one exists, it would be transformative for LCOE estimation. Consider a search of IAEA Nuclear Fusion and Fusion Engineering and Design for "magnetized target fusion power plant study." Flag as `unverified — confirm existence before searching`.
+**Gap-filling searches** (not-yet-sourced gaps):
+- **Commercial Q estimate**: Search OSTI and arXiv for "General Fusion MTF gain" or "magnetized target fusion Q commercial" — GF has presented at conferences (APS DPP annual) with operational parameters; some may cite a target gain. `unverified — confirm existence before searching`
+- **Piston driver energy**: The 2013 GF proof-of-concept compression system paper (likely in Journal of Fusion Energy or Nuclear Fusion) may give piston energy and efficiency at 1 m scale. `unverified — confirm existence before searching`
+- **Recirculating power fraction**: Search for "(steam piston OR pneumatic driver) (fusion OR MTF) (recirculating power OR wall plug efficiency)" on OSTI. The INFUSE collaborations with ORNL and PPPL may have produced reports. `unverified — confirm existence before searching`
+- **CNL BOP integration study**: The April 2024 GF/CNL project "to examine and propose the most efficient and cost-effective designs to integrate the fusion machine, balance of plant, and power conversion systems" — check whether this has produced a report or conference abstract. `unverified — confirm existence before searching`
 
 ---
 
 ## Summary
 
-**Proceed to full qualitative analysis now; quantitative LCOE requires explicit assumption documentation.**
+The concept is technically well-characterized: the physics approach, current experimental status (LM26 results), fuel cycle behavior (FST 2025), and key design parameters are documented well enough to describe the system and assess maturity. However, the LCOE analysis faces three blocking gaps: (1) no published Q for the commercial plant, (2) no capital cost estimate or plant economics study, and (3) the recirculating power fraction (pistons consume a share of turbine output) is unquantified. These three gaps make it impossible to produce a grounded LCOE estimate without fabricating the key inputs.
 
-The qualitative write-up (D1+ sections 1–3) can be completed at good quality with available data. General Fusion's concept is architecturally clear, the physics pathway is well-described, and subsystem TRLs can be assessed with moderate confidence. The key narrative gap — that the commercial pneumatic piston system has never been tested and represents the central unproven engineering bet — is itself well-evidenced and worth stating prominently.
+**Recommendation**: Proceed to full analysis, but clearly bound assumptions. The LCOE model should: (a) read the ARPA-E ALPHA cost study for MTF cost analogs, (b) use MFE BOP costs as the baseline and substitute piston array for magnets with a wide uncertainty range, and (c) perform a sensitivity analysis over Q (1–5) and recirculating power fraction (10–50%) as the primary uncertain axes. Flag all three blocking gaps explicitly in the qualitative write-up.
 
-For the quantitative LCOE model, proceed with the following posture:
-- **Use 300 MWe output** as the fixed anchor.
-- **Assume Q = 5–20** as a range (commercial D-T MTF targets; no published value — document this assumption explicitly).
-- **Assume steam Rankine efficiency 33–35%** (standard, no GF-specific data).
-- **Assume recirculating power 20–40%** (wide range; this is the single largest uncertainty and should be the primary sensitivity axis).
-- **Capital cost**: Use a bottom-up analogue approach: BOP from fission analogues (~$1,000–1,500/kWe), piston/compression system as a novel cost item with wide uncertainty (±50%).
-- The back-solve to $0.01/kWh will be informative precisely because the piston recirculating power and capital cost uncertainties are so large — those become the binding constraints to discuss.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with significant LCOE-specific gaps)"
+overall_rating: "Significant Gaps"
 blocking_count: 4
-important_count: 8
-counting_method: "section_5_missing_parameters"
+important_count: 5
+counting_method: "Gaps flagged 'blocking' across all five sections, deduplicated: (1) no published commercial Q / fusion gain, (2) no capital cost estimate or plant economics study, (3) recirculating power fraction unquantified, (4) thermal cycle parameters (liquid metal operating temperature) unpublished. Gaps flagged 'important' deduplicated: (1) piston array cost unknown, (2) O&M unknown, (3) capacity factor unknown, (4) vacuum re-establishment at 1 Hz unresolved, (5) pneumatic piston + liquid metal vortex not yet integrated."
 section_coverage:
-  availability_of_data:       "Moderate"
-  system_function:            "Partial"
+  availability_of_data:       "Partial"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
