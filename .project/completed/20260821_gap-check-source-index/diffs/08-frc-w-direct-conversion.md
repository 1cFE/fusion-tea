# Diff: 08-frc-w-direct-conversion

**Generated:** 2026-05-22T09:51:48-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 7 | 6 | -1 |
| important_count  | 4 | 8 | - |
| overall_rating   | Mostly Ready | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
139:| Analog LCOE (MIF modular) | $34–54/MWh | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | low (different concepts) |
```

## Blocking-tier lines (baseline)

```
37:- No published plant study for Orion — `proprietary` — **blocking** for quantitative LCOE
62:- FRC stability at 40 T compression not demonstrated — `truly-unknown` — **blocking** (core physics risk)
63:- D-He3 ignition/gain (requires 4× higher temperature than D-T demonstrated) — `truly-unknown` — **blocking** for commercial concept validation
91:- Direct energy recovery at sustained 1-2 Hz commercial rep rate — `proprietary/truly-unknown` — **blocking** (95% efficiency not measured at target rate)
117:- Capacitor scale-up manufacturing: production volume, cost per unit, replacement rate — `proprietary` — **blocking** (company-identified risk; drives a large fraction of capital and O&M cost)
152:| Capital cost breakdown (Orion) | proprietary | blocking | No published cost; Orion under construction but no price disclosed |
153:| Fusion gain Q (D-He3) | truly-unknown | blocking | D-He3 not yet demonstrated; D-T only as of Feb 2026 |
154:| Net electricity demonstrated | truly-unknown | blocking | Explicitly not achieved as of Dec 2025; required before LCOE meaningful |
155:| O&M cost structure | proprietary | blocking | No public data; capacitor/coil replacement dominates |
156:| Capacitor replacement cost and schedule | proprietary | blocking | Helion's self-identified main risk; no data |
157:| Coil replacement cost and lifetime | proprietary | blocking | Critical for O&M; no lifetime data at commercial rep rate |
161:| Plant construction cost (Orion) | proprietary | blocking | Microsoft PPA terms with "significant penalties" suggest real commitment, but cost undisclosed |
```

## Blocking-tier lines (new)

```
147:| Capital cost by CAS subsystem | proprietary | blocking | No plant study published; analog from ARPA-E ALPHA revisit (different concepts) is only reference |
148:| Plasma gain Q (commercial design) | proprietary | blocking | Net electricity not yet demonstrated; efficiency formula (η·G=0.24) implies Q requirement but G not specified for Orion |
149:| Capacity factor / availability | truly-unknown | blocking | No commercial-rep-rate operation demonstrated; Trenta ran 16 months but at 1/10 min |
150:| O&M costs (annual) | proprietary | blocking | No published data; capacitor/coil cycling costs are primary unknowns |
151:| Recirculating power fraction | proprietary/derivable | blocking | Need to close the energy balance: G, η_recovery, and recirculating fraction together determine net electric output |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/08-frc-w-direct-conversion.md	2026-05-22 09:21:13.841184674 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/gap_report.md	2026-05-22 09:51:48.780245204 -0700
@@ -1,40 +1,39 @@
-Now I have everything I need. Let me write the assessment.
+I have sufficient information to write the gap assessment. The ARPA-E ALPHA revisit covered four different MIF concepts (not Helion), but provides useful CAS methodology and analog LCOE/CapEx figures for modular pulsed fusion. Now writing the report.
 
 ---
 
-# Gap Assessment: FRC w/ Direct Conversion
+# Gap Assessment: FRC w/ Direct Conversion (D-He3)
 
 ## Overall Readiness
-**Rating**: Mostly Ready
-
-**Summary**: Helion has unusually high public transparency for a private fusion company — the working principle, prototype history, fuel cycle, and energy recovery mechanism are all well-documented. All 12 differentiation columns are filled at high confidence. The main gaps are in LCOE-critical parameters: no published capital cost breakdown, D-He3 gain not yet demonstrated (D-T only as of Feb 2026), and net electricity production not yet confirmed. A qualitative D1+ analysis can proceed confidently; the quantitative LCOE model will require explicit assumptions for several key parameters.
+**Rating**: Significant Gaps
+**Summary**: Helion is the most publicly documented private MIF company, and the physics characterization, fuel cycle, and energy conversion architecture are well-described from company sources and a handful of peer-reviewed papers. However, LCOE parameter extraction faces structural barriers: no plant study has been published for Orion, no CAS-level cost breakdown exists in any public source, and the critical performance milestone (net electricity production, Q≥1) remains undemonstrated as of early 2026. The qualitative analysis sections (availability, system function, subsystem maturity) can proceed well; the quantitative LCOE section will be heavily reliant on analogues with low-to-medium confidence throughout.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate (Rich for physics/concept, Limited for economics)
+**Coverage**: Partial
 
 **Available**:
-- **Company website** (`helion-website-technology.md`): comprehensive narrative on working principle, fuel cycle, energy recovery, prototype history, power targets
-- **ARPA-E presentation** (`docslib-helion-arpa-e-presentation.md`): quantitative plasma parameters (density, temperature, field, FRC velocity), 50 MW / 2 Hz design point, early energy balance (η·Gain = 0.2×1.2)
-- **Wikipedia** (`helion-prototype-generations.md`): full prototype history with measured parameters per generation (Venti triple product, Trenta densities/temperatures/confinement times), funding history, JASON/MITRE criticism summary
-- **Contrary Research** (`contrary-research-helion.md`): third-party synthesis including supply chain risk identification and business terms
-- **Helion Feb 2026 press release** (`helion-milestones-feb2026.md`): latest performance milestone (150M°C D-T, tritium regulatory approval), confirms D-He3 not yet demonstrated
-- **Peer-reviewed literature**: Nuclear Fusion 2011 (Kirtley et al., IPA plasmoid merging) referenced in ARPA-E source — not yet extracted
-- **Expert commentary**: PPPL critic (Jassby), DOE's Allain, Ryan McBride (Sandia), Alan Hoffman (FRC)
+- Company website technical articles covering all major architectural choices: confinement method (FRC pulsed compression), fuel (D-He3 self-bred), energy capture (direct inductive), magnet type (pulsed aluminum coils), neutron management, and modular plant philosophy. (`iter-01/sources/helion-website-technology.md`, `dossier.md`)
+- Wikipedia article synthesizing prototype lineage (IPA → Grande → Venti → Trenta → Polaris → Orion) with published performance values per generation. (`iter-02/sources/helion-prototype-generations.md`)
+- Feb 2026 milestone announcement: first private D-T fusion, 13 keV (150 M°C) on Polaris. (`iter-02/sources/helion-milestones-feb2026.md`)
+- ARPA-E presentation slide (DocsLib): 20T/40T field targets, 2 Hz @ 50 MW design point, plasma density targets, energy efficiency formula. (`iter-01/sources/docslib-helion-arpa-e-presentation.md`)
+- Contrary Research: CEO-level quotes on aluminum magnets, 85–95% efficiency claim, in-house capacitor manufacturing, supply chain risk identification. (`iter-01/sources/contrary-research-helion.md`)
+- Peer-reviewed anchor papers cited in dossier: Slough et al. (Nuclear Fusion, 2011) on merging/compression; Kirtley & Milroy (J. Fusion Energy, 2023) on FRC scaling; Venti triple product 6.4×10¹⁸ keV·s/m³ from 2018 ARPA-E proceedings.
+- Patent: EP 3103119 — Helion's D-He3 fuel cycle self-breeding process.
 
 **Missing**:
-- Independent technical assessments beyond JASON/MITRE 2018 summary
-- Peer-reviewed publications on Trenta or Polaris performance (most data is company press releases)
-- Published plant/system studies (no equivalent of a PROCESS run or system code output)
-- Cost analysis from any public source
+- Kirtley & Milroy (2023) and its peer response (2026) are referenced but not extracted as sources — the scaling arguments and technical criticisms they contain are not directly accessible.
+- No published engineering design document for Orion (equivalent of an ARIES or ARC conceptual design report).
+- No third-party independent technical review of Polaris performance data (DoE endorsement is political, not engineering).
+- No disclosure of Polaris achieved repetition rate (150 M°C milestone did not report pulse frequency).
 
 **Gaps**:
-- No peer-reviewed Trenta/Polaris data publications — `not-yet-sourced` — **important** (all performance claims are company-reported)
-- JASON/MITRE 2018 technical report — `not-yet-sourced` — **important** (provides independent technical assessment; referenced in Wikipedia but not yet extracted)
-- No published plant study for Orion — `proprietary` — **blocking** for quantitative LCOE
+- Polaris rep rate achieved (vs. 1 Hz target) — `proprietary` — important: determines whether scaling claim is on track
+- Kirtley & Milroy (2023) paper content (and peer response) not captured — `not-yet-sourced` — important: contains the core FRC scaling physics used to justify commercial viability
+- Orion engineering design document — `proprietary` — blocking: no plant-level architecture available for cost modeling
 
 ---
 
@@ -42,28 +41,24 @@
 **Coverage**: Partial
 
 **Available**:
-- Direct inductive energy recovery mechanism clearly described: expanding plasma pushes back on coils via Faraday induction, no steam cycle (`helion-website-technology.md`)
-- 95% round-trip energy recovery claimed on Grande (1M pulses) and required for net electricity (`contrary-research-helion.md`, `helion-website-technology.md`)
-- FRC formation, acceleration (>300 km/s), merging, and compression sequence described (`docslib-helion-arpa-e-presentation.md`)
-- He3 breeding pathway (DD→T→He3, t½=12.3 yr) described; patent held by Helion
-- Key physics challenge identified: simultaneous high compression and plasma stability (`helion-prototype-generations.md`, citing JASON report)
-- D-He3 fusion requires ~750M°C; only 150M°C (D-T) demonstrated — gap explicitly flagged in sources
-- Pulsed RLC circuit architecture described; capacitor bank as fundamental driver
+- The operating cycle (form FRC → accelerate → collide → compress → fuse → expand → recover energy) is well-described qualitatively. The "RLC circuit" analogy is explained with key parameters: capacitor bank >50 MJ, tens of kV, pulsed at ~1 Hz target. (`helion-website-technology.md`, `docslib-helion-arpa-e-presentation.md`)
+- Energy recovery mechanism explained via Faraday's law; η=0.7 magnetic energy recovery efficiency stated in ARPA-E presentation; >95% round-trip efficiency demonstrated at subscale (Grande, >1M pulses). (`dossier.md`)
+- ARPA-E presentation gives key efficiency formula: η(=Ed/Eplasma) · Gain = 0.2 · 1.2 — this is the critical condition revealing that net electricity requires very high recovery efficiency rather than plasma ignition.
+- D-He3 fuel cycle self-breeding chain (DD → He3 + T, T → He3 via decay) is documented with timescales (12.3 yr half-life). Patent covers this mechanism.
+- Neutron management for D-He3 (~5% of energy as 2.45 MeV neutrons) clearly articulated.
 
 **Missing**:
-- Electrical subsystem modeling: circuit parameters, inductance, discharge timescales — none published
-- FRC stability scaling from prototype to commercial field strengths (40 T vs. 15 T demonstrated)
-- Wall loading quantification under 1 Hz sustained operation
-- He3 capture and recirculation subsystem: no design details published
-- Coil and capacitor failure modes under sustained high-rep-rate operation
-- Net electricity demonstration: explicitly not yet achieved (not achieved by Dec 2025 per Wikipedia)
+- Commercial-scale direct electricity conversion has not been independently validated. The 85–95% efficiency is a company claim; at what plasma size and rep rate this is achievable is unknown.
+- He3 self-breeding engineering: how large is the tritium inventory, what is the breeding efficiency per pulse, and what are the startup fuel requirements? Only qualitative description available.
+- Plasma stability at 40T compression (commercial requirement): the JASON/MITRE 2018 report flagged this as the primary challenge ("whether they can simultaneously achieve sufficiently high compression while maintaining plasma stability"). No published resolution.
+- Capacitor bank and coil cycling lifetime: how many pulses before component replacement, and what is the replacement cost structure? Not published.
+- He3/D ratio optimization for D-He3 operation at 200 M°C: fuel mix not documented quantitatively.
 
 **Gaps**:
-- FRC stability at 40 T compression not demonstrated — `truly-unknown` — **blocking** (core physics risk)
-- D-He3 ignition/gain (requires 4× higher temperature than D-T demonstrated) — `truly-unknown` — **blocking** for commercial concept validation
-- Direct energy recovery efficiency at commercial pulse rate (1-2 Hz sustained) — `proprietary/truly-unknown` — **important** (95% is required threshold; only demonstrated at low rate)
-- He3 recirculation system design and efficiency — `proprietary` — **important** (unique to Helion; no published data)
-- Circuit parameters for quantitative efficiency modeling — `proprietary` — **important**
+- 40T compression plasma stability at commercial scale — `truly-unknown` (ongoing research) — blocking: determines whether the concept works
+- Quantitative He3 breeding engineering model (inventory, startup, refueling) — `proprietary` — important
+- Commercial direct conversion efficiency validation (system-level, not subscale) — `proprietary` — blocking for LCOE
+- Capacitor/coil cycling lifetime and failure mode data — `proprietary` — important
 
 ---
 
@@ -71,140 +66,133 @@
 **Coverage**: Partial
 
 **Available**:
-- **FRC formation and merging**: Demonstrated across 7 prototype generations; IPA experiments from 2005-2012; Polaris operating (TRL ~5-6)
-- **Magnetic compression**: >8 T on Trenta, 15 T+ on Polaris; 40 T commercial target; TRL ~4-5 for full-scale compression
-- **Plasma temperature**: 100M°C (Trenta), 150M°C D-T (Polaris); D-He3 requires ~750M°C — TRL ~2-3 for commercial fuel cycle
-- **Capacitor bank**: >50 MJ on Polaris; in-house manufacturing; TRL ~4 at current scale
-- **Aluminum pulsed coils**: Fabricated in-house; demonstrated on all prototypes; TRL ~4-5
-- **Repetition rate**: Trenta ~1 pulse/10 min; Polaris target 1 Hz (not confirmed achieved); commercial 2 Hz
-- **Energy recovery**: 95% claimed at Grande scale (1M pulses); TRL ~4 at small scale, much lower at commercial scale
+- Prototype generation history provides TRL-adjacent evidence per subsystem. The dossier and Wikipedia source document performance milestones per generation.
+- FRC formation and acceleration: demonstrated across 7 generations; 300 km/s velocities, D-D neutron production, and D-T fusion confirmed. TRL ~5–6.
+- Magnetic compression to fusion temperature: demonstrated (13 keV on Polaris, D-T). TRL ~5.
+- Pulsed power system (capacitors, IGBTs, switching): >95% round-trip energy recovery demonstrated at subscale (Grande, >1M pulses). TRL ~6 for the energy recovery circuit itself; TRL ~4 at commercial rep rate.
+- Aluminum coil fabrication: in-house, demonstrated across prototypes. TRL ~6.
+- Quartz plasma tubes: in-house manufacturing. TRL ~5–6 for prototype scale.
+- D-T fuel handling: first regulatory approval for private company (Polaris, 2024). TRL ~5.
 
 **Missing**:
-- TRL assessments for He3 separation/recirculation (novel; no published data)
-- Coil/capacitor replacement schedule and lifetime quantification under commercial rep rate
-- Plasma-facing component design for commercial neutron flux
-- Power conditioning and grid integration subsystem design
-- Tritium handling system TRL (regulatory approval received, but scale details unknown)
+- D-He3 operation not yet demonstrated (requires ~200 M°C, Polaris at 150 M°C as of Feb 2026). TRL assessment for D-He3 operation is TRL ~3.
+- High repetition rate operation at commercial scale: Trenta at 1/10 min; Polaris targeting 1 Hz but no confirmed achievement reported. TRL ~3 for 1 Hz rep rate.
+- He3 breeding and processing system: no engineering demonstration, concept only. TRL ~2–3.
+- Commercial-scale capacitor bank (scaling to Orion power levels): in-house manufacturing capability unproven at that scale. TRL ~3–4.
+- System integration at commercial scale (40T field, 500 MWe class): TRL ~2.
 
 **Gaps**:
-- He3 separation and recirculation TRL — `proprietary` — **important** (unique subsystem, critical for fuel economics)
-- Direct energy recovery at sustained 1-2 Hz commercial rep rate — `proprietary/truly-unknown` — **blocking** (95% efficiency not measured at target rate)
-- Long-duration coil/capacitor lifetime (10^9 commercial shot count) — `truly-unknown` — **important** (no analogous pulsed system at this scale)
-- Plasma-facing component design for 2.45 MeV neutron flux — `proprietary` — **important**
-- Tritium system TRL at commercial throughput — `proprietary` — **nice-to-have** (Helion minimizes external tritium need)
+- D-He3 operation TRL (not yet demonstrated on any prototype) — `truly-unknown` (milestone pending) — blocking
+- High rep-rate (≥1 Hz) sustained operation TRL — `proprietary` (Polaris data not released) — blocking
+- He3 breeding subsystem TRL — `truly-unknown` — important
+- Full system integration at commercial field and power — `truly-unknown` — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- **Deuterium**: From water; abundant, low-cost — no supply risk
-- **He3**: Self-bred via DD→T→He3 decay; no external supply required (key competitive advantage); patent held (`helion-prototype-generations.md`)
-- **Aluminum coils**: Standard material, commodity supply; not superconducting — no exotic material requirement (`contrary-research-helion.md`)
-- **Coaxial cables**: Copper, aluminum, and "custom-metal alloys" (~720 miles total per Polaris) — custom alloys unspecified
-- **High-voltage pulsed capacitors**: In-house manufacturing; Helion itself identified this as "main potential risk" (`contrary-research-helion.md`)
-- **No exotic superconductors**: Major advantage vs. tokamak/stellarator approaches — no REBCO or Nb3Sn supply chain dependency
+- Contrary Research identifies in-house manufacturing of quartz tubes and high-voltage capacitors; supply chain noted as "main potential risk" per the report. (`contrary-research-helion.md`)
+- Dossier notes ~720 miles of coaxial cables per machine (copper, aluminum, custom alloys).
+- Capacitor bank parameters known: >50 MJ, tens of kV, high-voltage IGBTs.
+- Aluminum coils explicitly called out as preferable to superconducting magnets (cost/complexity advantage). No cryogenic supply chain needed.
+- D fuel cycle: deuterium from water — essentially unlimited supply, commodity availability.
 
 **Missing**:
-- Capacitor technology specification: dielectric type, voltage rating, energy density — not published
-- Manufacturing scale-up roadmap for capacitors: current production capacity vs. Orion requirements
-- "Custom-metal alloys" specification for coaxial cables
-- Borated polyethylene and concrete shielding quantities (mentioned but not quantified)
-- Neutron-activated component disposal and replacement cost
+- No published materials qualification study for the plasma-facing components (quartz tubes at commercial fluence and cycling rate).
+- No published supply chain assessment for high-voltage pulsed power components at GW-scale manufacturing.
+- Custom high-voltage capacitor supply: partial in-house, partially external — external sourcing not disclosed.
+- IGBT requirements at commercial scale: switching at ≥1 Hz with >50 MJ discharge — no published specification.
+- He3 startup inventory: how much He3 is needed before self-breeding is sufficient? Not published.
+- Tritium handling infrastructure (for Polaris D-T phase): regulatory approved, but commercial-scale is different.
+- Materials irradiation qualification for D-He3 (low neutron flux): likely more tractable than D-T, but no study published.
 
 **Gaps**:
-- Capacitor scale-up manufacturing: production volume, cost per unit, replacement rate — `proprietary` — **blocking** (company-identified risk; drives a large fraction of capital and O&M cost)
-- Custom alloy specification for cables — `proprietary` — **nice-to-have**
-- Component activation and replacement logistics for commercial plant — `not-yet-sourced/derivable` — **important**
+- High-voltage capacitor/IGBT supply chain at commercial volume — `proprietary` — important
+- Quartz tube lifetime and replacement rate at commercial rep rate — `proprietary` — important
+- He3 startup inventory requirement — `proprietary/derivable` — important
+- Materials irradiation database for D-He3 fluence environment — `not-yet-sourced` — important (may exist in D-He3 materials literature)
+- BOP (balance of plant) materials/supply chain — `not-yet-sourced` (no steam cycle — simpler, but no study) — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor for quantitative modeling; Partial for structural understanding
+**Coverage**: Poor
 
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plant electrical output (Orion) | 50 MWe | Helion website, Wikipedia | H |
-| Plant electrical output (future) | 500 MWe | Wikipedia (Nucor agreement) | M |
-| Target repetition rate (commercial) | 2 Hz (ARPA-E design point) | ARPA-E presentation | M |
-| Target repetition rate (Polaris) | 1 Hz | Helion website | M |
-| Direct energy recovery efficiency (claimed) | 95% | Helion website, Contrary | M |
-| Energy conversion pathway | Direct inductive (no steam) | All sources | H |
-| Fuel input | Deuterium only (He3 self-bred) | All sources | H |
-| Compression magnetic field (commercial target) | 40 T | ARPA-E presentation | M |
-| Compression magnetic field (Polaris demonstrated) | 15 T+ | Helion website | H |
-| Early energy balance (ARPA-E) | η·Gain = 0.2 × 1.2 | ARPA-E presentation | L (old/conceptual) |
-| Input energy cost target | <$0.03/MJ | ARPA-E presentation | L (target only) |
-| Capacitor bank energy (Polaris) | >50 MJ | Helion website | H |
-| Plasma temperature (D-T achieved) | 150M°C (13 keV) | Feb 2026 press release | H |
-| Plasma temperature (D-He3 required) | ~750M°C | Contrary Research | M |
-| Neutron fraction (claimed, D-He3) | 5% | Helion website | M |
-| Operation start target (Orion/Microsoft) | 2028 | Wikipedia, press release | H |
-| Pulsed operation mode | Yes; ~24/7 at commercial scale | All sources | H |
+| Net electric power (first plant) | 50 MWe | Helion website / PPA | medium |
+| Net electric power (future) | 500 MWe | Nucor partnership | low |
+| Repetition rate (design point) | 2 Hz @ 50 MW | ARPA-E presentation | medium |
+| Direct conversion efficiency | 85–95% | Contrary Research (CEO claim) | low |
+| Energy recovery (subscale demo) | >95% round-trip | Dossier / Helion press | medium |
+| Magnetic energy recovery η | 0.7 | ARPA-E presentation | medium |
+| Fusion energy per pulse | Not published (implied ~25 MJ at 50 MW, 2 Hz) | Derivable | low |
+| Neutron energy fraction | ~5% | Helion website | medium |
+| Fuel: external input | Deuterium only | Dossier | high |
+| Magnet field (reactor) | 40 T | ARPA-E presentation | medium |
+| Capacitor bank energy | >50 MJ (Polaris) | Helion website | medium |
+| Plant size (modular) | "Shipping container scale" | Helion website | low |
+| Analog LCOE (MIF modular) | $34–54/MWh | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | low (different concepts) |
+| Analog CapEx (MIF modular) | ~$2.4/W, ~$1.2B @ 500 MWe | Same ARPA-E revisit | low (different concepts) |
+| LCOE target (third-party) | $0.01–0.06/kWh | Thunder Said Energy | very low |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost breakdown (Orion) | proprietary | blocking | No published cost; Orion under construction but no price disclosed |
-| Fusion gain Q (D-He3) | truly-unknown | blocking | D-He3 not yet demonstrated; D-T only as of Feb 2026 |
-| Net electricity demonstrated | truly-unknown | blocking | Explicitly not achieved as of Dec 2025; required before LCOE meaningful |
-| O&M cost structure | proprietary | blocking | No public data; capacitor/coil replacement dominates |
-| Capacitor replacement cost and schedule | proprietary | blocking | Helion's self-identified main risk; no data |
-| Coil replacement cost and lifetime | proprietary | blocking | Critical for O&M; no lifetime data at commercial rep rate |
-| Capacity factor / availability | derivable | important | Could estimate from rep rate × pulse duration; no published target |
-| Commercial fusion gain Q (design point) | not-yet-sourced | important | ARPA-E gives early design point (Q~1.2 × η=0.2); outdated |
-| Thermal waste fraction | derivable | important | ~5% neutrons deposited in shield; can estimate from D-He3 spectrum |
-| Plant construction cost (Orion) | proprietary | blocking | Microsoft PPA terms with "significant penalties" suggest real commitment, but cost undisclosed |
-| He3 recirculation energy cost | proprietary | important | Parasitic load from He3 capture system unknown |
-| Deuterium fuel cost | derivable | nice-to-have | ~$1,000/kg, consumption rate derivable from Q and shot energy |
-| Regulatory/licensing cost | not-yet-sourced | nice-to-have | State license obtained; federal NRC pathway unclear |
+| Capital cost by CAS subsystem | proprietary | blocking | No plant study published; analog from ARPA-E ALPHA revisit (different concepts) is only reference |
+| Plasma gain Q (commercial design) | proprietary | blocking | Net electricity not yet demonstrated; efficiency formula (η·G=0.24) implies Q requirement but G not specified for Orion |
+| Capacity factor / availability | truly-unknown | blocking | No commercial-rep-rate operation demonstrated; Trenta ran 16 months but at 1/10 min |
+| O&M costs (annual) | proprietary | blocking | No published data; capacitor/coil cycling costs are primary unknowns |
+| Recirculating power fraction | proprietary/derivable | blocking | Need to close the energy balance: G, η_recovery, and recirculating fraction together determine net electric output |
+| Construction cost / schedule | proprietary | important | Orion groundbreaking July 2025, no cost disclosure |
+| Capacitor bank replacement schedule | proprietary | important | Cycling lifetime at commercial rep rate not published |
+| Fuel cost (D at scale) | derivable | nice-to-have | Deuterium is cheap commodity; extractable from water at well-known cost |
+| He3 startup inventory cost | proprietary/derivable | important | He3 from DD takes years to accumulate; startup fuel cost unknown |
+| Decommissioning cost | not-yet-sourced | nice-to-have | Reduced activation relative to D-T; no published estimate |
+| Thermal rejection (no steam cycle) | derivable | nice-to-have | ~5% neutron energy goes to heat; waste heat management simplified but unquantified |
 
 ---
 
 ## Source Recommendations
 
-1. **JASON/MITRE 2018 Helion Assessment** — search OSTI or DTIC for the full report (Wikipedia references: "Helion requires 40 T for commercial viability; 8 T in prototype; projected 2023 breakeven") — `not-yet-sourced` — *unverified: confirm existence before searching*
+- **Kirtley & Milroy, J. Fusion Energy (2023)** — extract this peer-reviewed paper; it contains the FRC scaling analysis underlying Helion's commercial case, and the 2026 peer response contains independent criticisms. Search: "Kirtley Milroy J Fusion Energy 2023 FRC scaling Helion." Both are in the dossier's key sources but not yet extracted. `not-yet-sourced` — confirm existence via DOI before searching.
 
-2. **Kirtley et al. (2011), Nuclear Fusion 51(5)** — "Creation of a high-temperature plasma through merging and compression of supersonic FRC plasmoids" — foundational peer-reviewed paper on IPA experiments — `not-yet-sourced` — confirmed cited in ARPA-E source
+- **ARPA-E ALPHA 2017 original Bechtel costing report** — the 2020 revisit references it (report no. 26029-000-30R-G01G-00001); the 2017 study covered Helion directly as one of the four ALPHA concepts. If the original (not the revisit) is accessible, it would contain Helion-specific (though possibly proprietary/redacted) CAS cost data. `not-yet-sourced` — may be at woodruffscientific.com/pdf/ARPAE_Costing_Report_2017.pdf. `unverified — confirm existence before searching`.
 
-3. **ARPA-E ALPHA program final reports** — Helion received ARPA-E ALPHA contract (2015) for "Staged Magnetic Compression of FRC Targets"; final technical report may contain design-point parameters — search OSTI for ARPA-E ALPHA Helion final report — `not-yet-sourced` — *unverified: confirm existence before searching*
+- **JASON/MITRE 2018 report on Helion** — cited in Wikipedia; reviewed Helion's 8T vs. 40T challenge and projected breakeven timeline. Available publicly (partially redacted) at ARPA-E. May contain independent technical assessment of subsystem readiness. `not-yet-sourced` — confirm via ARPA-E documents archive. `unverified — confirm existence before searching`.
 
-4. **Alan Hoffman FRC review literature** — quoted as expert in Helion press release (40+ years FRC experience); UW Madison FRC publications may provide scaling law context for compression stability — search Google Scholar for Hoffman FRC reviews — `not-yet-sourced`
+- **Slough et al., Nuclear Fusion 51(5) (2011)** — already referenced in dossier; the merging/compression FRC paper provides the foundational plasma physics. Should be extracted if not already. `not-yet-sourced`.
 
-5. **Slough et al. IPA papers (2012-2014)** — John Slough (Helion co-founder) published on FRC plasmoid merging pre-commercialization; contains pre-commercial plasma parameters — `not-yet-sourced`
+- **DOE Fusion Industry Association (FIA) annual reports** — FIA tracks TRL and investment by company; may contain third-party TRL assessments for Helion subsystems. Search: "Fusion Industry Association State of Fusion Industry 2025." `not-yet-sourced`.
 
-6. **Contrary Research full report** — the sourced file appears to be a summary; the full report may contain more detail on Orion construction cost and timeline — `not-yet-sourced` — *unverified: confirm whether full report is accessible*
+- **Helion ARPA-E ALPHA program reports (2015–2018)** — beyond the slide deck, full ARPA-E project reports may contain engineering details not in public articles. Search OSTI for "Helion ARPA-E ALPHA staged magnetic compression FRC." `not-yet-sourced` — `unverified — confirm existence before searching`.
 
-7. **DOE Fusion Energy Sciences press coverage of Polaris results** — Jean Paul Allain (DOE FES) quoted in press release; DOE FES may have published a supporting technical summary — search energy.gov/science — `not-yet-sourced` — *unverified*
+- **D-He3 nuclear reaction cross-section literature** — needed for neutron fraction (5% vs. 10% dispute) and energy balance at 200 M°C. Standard nuclear physics reference (NRL Plasma Formulary or Bosch & Hale 1992). `not-yet-sourced` — standard reference, confirm availability.
 
 ---
 
 ## Summary
 
-**Proceed to full qualitative analysis.** The data is sufficient to write a high-quality D1+ qualitative write-up. The physics mechanism, fuel cycle, prototype progression, maturity gaps, and supply chain risks are all well-documented — primarily from Helion's own communications but with enough external corroboration (ARPA-E, Wikipedia prototype table, expert quotes) to report with appropriate confidence levels.
+Proceed to full analysis with the following scoping: the qualitative sections (data availability, system function, subsystem maturity, materials) can be written with medium-to-high coverage from available sources, with explicit acknowledgment of Helion's exceptional opacity around plant-level engineering. The LCOE quantitative section should use ARPA-E ALPHA revisit analog values ($2.4/W CapEx, $34–54/MWh LCOE for modular MIF) as order-of-magnitude anchors, and flag that all cost figures are analogues, not Helion-specific. The central uncertainty — whether net electricity is achievable at all — must be treated as a key risk axis in the analysis rather than an assumed baseline. Acquiring the Kirtley & Milroy (2023) paper and the original 2017 Bechtel/ARPA-E ALPHA costing report (if publicly accessible) would most improve LCOE parameter coverage before analysis.
 
-**For quantitative LCOE modeling**, be explicit that several critical inputs require assumptions rather than extracted values:
-- D-He3 fusion gain Q: not yet demonstrated; use ARPA-E early design point (Q~1.2 × η=0.2) with wide uncertainty range
-- Capital cost: no public data; must build bottom-up estimate from component descriptions or use cost-per-watt analogues from other pulsed power systems
-- Capacitor/coil O&M: structurally the dominant cost driver (company-identified), but completely opaque — flag as the primary LCOE uncertainty
-
-The concept is unusual in that **the binding uncertainty is not the energy conversion system** (well-described and plausible) **but the core plasma physics** — D-He3 fusion has not been demonstrated, and reaching 750M°C from 150M°C demonstrated represents a 5× temperature increase. Any LCOE model should treat fusion gain Q as the primary sweep parameter and back-solve to what Q is needed for commercial viability.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready"
-blocking_count: 7
-important_count: 4
-counting_method: "section_5_missing_parameters"
+overall_rating: "Significant Gaps"
+blocking_count: 6
+important_count: 8
+counting_method: "blocking: 5 LCOE parameter gaps (CapEx by CAS, plasma gain Q, capacity factor, O&M, recirculating power fraction) + 1 physics/concept gap (40T compression stability not demonstrated, D-He3 not demonstrated); important: He3 breeding engineering, high rep-rate TRL, capacitor lifecycle, materials irradiation database, He3 startup inventory, construction cost, Kirtley & Milroy paper not extracted, FIA TRL data not sourced; deduplicated across all sections"
 section_coverage:
-  availability_of_data:       "Moderate (Rich for physics/concept, Limited for economics)"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Poor for quantitative modeling; Partial for structural understanding"
-```
+  materials_supply_chain:     "Poor"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
