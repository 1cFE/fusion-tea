# Phase 3 diff: 08-frc-w-direct-conversion

**Generated:** 2026-05-22T13:45:43-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 6 | 0 |
| important_count  | 8 | 6 | - |
| overall_rating   | Significant Gaps | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information to write the gap assessment. The ARPA-E ALPHA re-costing source covers four MIF concepts (LANL/HyperJet, Compact Fusion Systems, MIFTI, Zap Energy) — NOT Helion — so it provides cost structure analogues but no Helion-specific cost data.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information to write the gap assessment. The ARPA-E ALPHA re-costing source covers four MIF concepts (LANL/HyperJet, Compact Fusion Systems, MIFTI, Zap Energy) — NOT Helion — so it provides cost structure analogues but no Helion-specific cost data.
```

## Blocking-tier lines (new)

```
130:| Capital cost by CAS subsystem | proprietary | blocking | Orion specs proprietary; no published plant study |
131:| O&M cost (maintenance, replacement schedules) | proprietary | blocking | No published operations data |
132:| Capacity factor / availability target | proprietary | blocking | No published RAMI analysis; rep rate not yet demonstrated at commercial scale |
133:| Q factor / scientific/engineering gain | proprietary | blocking | Key for net electricity calculation; never publicly disclosed |
134:| Commercial repetition rate achieved | proprietary | blocking | Polaris rep rate not disclosed in milestone announcement |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/08-frc-w-direct-conversion.md	2026-05-22 12:59:21.062223191 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/gap_report.md	2026-05-22 13:45:43.250250011 -0700
@@ -1,64 +1,44 @@
-I have sufficient information to write the gap assessment. The ARPA-E ALPHA revisit covered four different MIF concepts (not Helion), but provides useful CAS methodology and analog LCOE/CapEx figures for modular pulsed fusion. Now writing the report.
-
----
+I now have sufficient information to write the gap assessment. The ARPA-E ALPHA re-costing source covers four MIF concepts (LANL/HyperJet, Compact Fusion Systems, MIFTI, Zap Energy) — NOT Helion — so it provides cost structure analogues but no Helion-specific cost data.
 
 # Gap Assessment: FRC w/ Direct Conversion (D-He3)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
-**Summary**: Helion is the most publicly documented private MIF company, and the physics characterization, fuel cycle, and energy conversion architecture are well-described from company sources and a handful of peer-reviewed papers. However, LCOE parameter extraction faces structural barriers: no plant study has been published for Orion, no CAS-level cost breakdown exists in any public source, and the critical performance milestone (net electricity production, Q≥1) remains undemonstrated as of early 2026. The qualitative analysis sections (availability, system function, subsystem maturity) can proceed well; the quantitative LCOE section will be heavily reliant on analogues with low-to-medium confidence throughout.
+**Rating**: Mostly Ready
+**Summary**: Helion Energy is among the most publicly documented private fusion companies, and the physics, technology architecture, and milestone history are well-supported by multiple independent sources. However, virtually all commercial-scale cost data (capital costs by subsystem, O&M, capacity factor, plant-level power balance) is proprietary, and two critical technical milestones remain undemonstrated as of the available sources: net electricity production and D-He3 operation at the required ~200M°C. Qualitative sections 1–3 can be written at high quality; sections 4–5 will require explicit analogue assumptions and gap acknowledgments.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Good
 
-**Available**:
-- Company website technical articles covering all major architectural choices: confinement method (FRC pulsed compression), fuel (D-He3 self-bred), energy capture (direct inductive), magnet type (pulsed aluminum coils), neutron management, and modular plant philosophy. (`iter-01/sources/helion-website-technology.md`, `dossier.md`)
-- Wikipedia article synthesizing prototype lineage (IPA → Grande → Venti → Trenta → Polaris → Orion) with published performance values per generation. (`iter-02/sources/helion-prototype-generations.md`)
-- Feb 2026 milestone announcement: first private D-T fusion, 13 keV (150 M°C) on Polaris. (`iter-02/sources/helion-milestones-feb2026.md`)
-- ARPA-E presentation slide (DocsLib): 20T/40T field targets, 2 Hz @ 50 MW design point, plasma density targets, energy efficiency formula. (`iter-01/sources/docslib-helion-arpa-e-presentation.md`)
-- Contrary Research: CEO-level quotes on aluminum magnets, 85–95% efficiency claim, in-house capacitor manufacturing, supply chain risk identification. (`iter-01/sources/contrary-research-helion.md`)
-- Peer-reviewed anchor papers cited in dossier: Slough et al. (Nuclear Fusion, 2011) on merging/compression; Kirtley & Milroy (J. Fusion Energy, 2023) on FRC scaling; Venti triple product 6.4×10¹⁸ keV·s/m³ from 2018 ARPA-E proceedings.
-- Patent: EP 3103119 — Helion's D-He3 fuel cycle self-breeding process.
-
-**Missing**:
-- Kirtley & Milroy (2023) and its peer response (2026) are referenced but not extracted as sources — the scaling arguments and technical criticisms they contain are not directly accessible.
-- No published engineering design document for Orion (equivalent of an ARIES or ARC conceptual design report).
-- No third-party independent technical review of Polaris performance data (DoE endorsement is political, not engineering).
-- No disclosure of Polaris achieved repetition rate (150 M°C milestone did not report pulse frequency).
+**Available**: Helion has published more technical detail than almost any other private fusion company, across first-party website articles, peer-reviewed papers (Slough et al. *Nuclear Fusion* 51(5) 2011; Kirtley & Milroy *J. Fusion Energy* 2023), ARPA-E presentations (DocsLib ARPA-E presentation: 20T/40T specs, 2 Hz @ 50 MW design point), a detailed third-party research report (Contrary Research), and ongoing press coverage of milestone events. Seven prototype generations are documented. Polaris's Feb 2026 D-T milestone at 150M°C (13 keV) is independently confirmed by DOE/FES and Ryan McBride (Sandia/University of Michigan). Funding history ($500M Series E, $425M Series F, $5.4B valuation), power purchase agreements (50 MWe for Microsoft, 2028; 500 MWe Nucor 2030), and Orion construction (groundbreaking July 2025, Malaga, WA) are confirmed.
+
+**Missing**: No published plant study (ARIES-equivalent), no peer-reviewed capital cost analysis, no independent techno-economic assessment. Orion specifications are entirely proprietary.
 
 **Gaps**:
-- Polaris rep rate achieved (vs. 1 Hz target) — `proprietary` — important: determines whether scaling claim is on track
-- Kirtley & Milroy (2023) paper content (and peer response) not captured — `not-yet-sourced` — important: contains the core FRC scaling physics used to justify commercial viability
-- Orion engineering design document — `proprietary` — blocking: no plant-level architecture available for cost modeling
+- Published plant study / design document for Orion — proprietary — important
+- Independent peer-reviewed cost or TEA study — not-yet-sourced — important
+- Achieved Polaris repetition rate — proprietary (milestone announcement did not disclose rep rate) — important
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
-**Available**:
-- The operating cycle (form FRC → accelerate → collide → compress → fuse → expand → recover energy) is well-described qualitatively. The "RLC circuit" analogy is explained with key parameters: capacitor bank >50 MJ, tens of kV, pulsed at ~1 Hz target. (`helion-website-technology.md`, `docslib-helion-arpa-e-presentation.md`)
-- Energy recovery mechanism explained via Faraday's law; η=0.7 magnetic energy recovery efficiency stated in ARPA-E presentation; >95% round-trip efficiency demonstrated at subscale (Grande, >1M pulses). (`dossier.md`)
-- ARPA-E presentation gives key efficiency formula: η(=Ed/Eplasma) · Gain = 0.2 · 1.2 — this is the critical condition revealing that net electricity requires very high recovery efficiency rather than plasma ignition.
-- D-He3 fuel cycle self-breeding chain (DD → He3 + T, T → He3 via decay) is documented with timescales (12.3 yr half-life). Patent covers this mechanism.
-- Neutron management for D-He3 (~5% of energy as 2.45 MeV neutrons) clearly articulated.
-
-**Missing**:
-- Commercial-scale direct electricity conversion has not been independently validated. The 85–95% efficiency is a company claim; at what plasma size and rep rate this is achievable is unknown.
-- He3 self-breeding engineering: how large is the tritium inventory, what is the breeding efficiency per pulse, and what are the startup fuel requirements? Only qualitative description available.
-- Plasma stability at 40T compression (commercial requirement): the JASON/MITRE 2018 report flagged this as the primary challenge ("whether they can simultaneously achieve sufficiently high compression while maintaining plasma stability"). No published resolution.
-- Capacitor bank and coil cycling lifetime: how many pulses before component replacement, and what is the replacement cost structure? Not published.
-- He3/D ratio optimization for D-He3 operation at 200 M°C: fuel mix not documented quantitatively.
+**Available**: The system function is documented in sufficient qualitative depth across multiple public sources. The RLC circuit analogy is confirmed by CEO Kirtley. The four-phase cycle (FRC formation → acceleration to >300 km/s → collision-compression → inductive energy recovery) is described in the ARPA-E presentation and peer-reviewed IPA papers. Direct inductive energy recovery via Faraday's law is documented with the key constraint: >95% of input energy must be recovered per pulse for net electricity. Energy recovery >95% demonstrated at subscale (>1 million pulses, Grande prototype). The non-ignition economics rationale (high-efficiency energy recovery relaxes the gain requirement) is described in the Helion article "How to Make Fusion Electricity Without Ignition," consistent with the Lawson criterion framework in Wurzel & Hsu (2021) (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) which explicitly addresses pulsed systems where η fraction of plasma energy is recovered.
+
+**Modeling challenges** (not gaps in source availability, but inherent to the concept):
+- The system is an electrical circuit, not a thermal-mechanical system — standard power plant LCOE models (steam cycle → turbine → generator) do not apply at all. The absence of a thermal cycle is the defining structural difference from all other fusion concepts in this analysis.
+- The achievable net gain (Q_eng) is a function of both plasma gain and round-trip energy recovery efficiency — the two must be analyzed together, not sequentially.
+- He3 self-breeding inventory dynamics: tritium (t½=12.3 yr) accumulates in the system, decaying to He3 at 5.5%/year. Full self-sufficiency is a multi-decade process. Startup requires a stock of He3 or a plan to operate D-D or D-T at reduced economics initially.
+- The pulsed operation mode creates fatigue loading on all structural components — chamber, coils, capacitors — at a rate and severity with no comparable industrial precedent.
 
 **Gaps**:
-- 40T compression plasma stability at commercial scale — `truly-unknown` (ongoing research) — blocking: determines whether the concept works
-- Quantitative He3 breeding engineering model (inventory, startup, refueling) — `proprietary` — important
-- Commercial direct conversion efficiency validation (system-level, not subscale) — `proprietary` — blocking for LCOE
-- Capacitor/coil cycling lifetime and failure mode data — `proprietary` — important
+- Q factor / scientific gain (Q_sci or Q_eng) achieved on any prototype — proprietary (never disclosed) — blocking
+- Round-trip energy recovery efficiency at Polaris scale — proprietary — important
+- He3 startup inventory quantity and sourcing plan — derivable (physics-based estimate possible) — important
 
 ---
 
@@ -66,132 +46,139 @@
 **Coverage**: Partial
 
 **Available**:
-- Prototype generation history provides TRL-adjacent evidence per subsystem. The dossier and Wikipedia source document performance milestones per generation.
-- FRC formation and acceleration: demonstrated across 7 generations; 300 km/s velocities, D-D neutron production, and D-T fusion confirmed. TRL ~5–6.
-- Magnetic compression to fusion temperature: demonstrated (13 keV on Polaris, D-T). TRL ~5.
-- Pulsed power system (capacitors, IGBTs, switching): >95% round-trip energy recovery demonstrated at subscale (Grande, >1M pulses). TRL ~6 for the energy recovery circuit itself; TRL ~4 at commercial rep rate.
-- Aluminum coil fabrication: in-house, demonstrated across prototypes. TRL ~6.
-- Quartz plasma tubes: in-house manufacturing. TRL ~5–6 for prototype scale.
-- D-T fuel handling: first regulatory approval for private company (Polaris, 2024). TRL ~5.
-
-**Missing**:
-- D-He3 operation not yet demonstrated (requires ~200 M°C, Polaris at 150 M°C as of Feb 2026). TRL assessment for D-He3 operation is TRL ~3.
-- High repetition rate operation at commercial scale: Trenta at 1/10 min; Polaris targeting 1 Hz but no confirmed achievement reported. TRL ~3 for 1 Hz rep rate.
-- He3 breeding and processing system: no engineering demonstration, concept only. TRL ~2–3.
-- Commercial-scale capacitor bank (scaling to Orion power levels): in-house manufacturing capability unproven at that scale. TRL ~3–4.
-- System integration at commercial scale (40T field, 500 MWe class): TRL ~2.
+- **FRC formation and acceleration** (sequential field reversal, >300 km/s): TRL 5–6; demonstrated across 7 prototype generations, confirmed at Polaris scale with largest FRCs ever produced by Helion. Heritage traces to MSNW/UW IPA experiments 2005–2012.
+- **Magnetic compression to fusion conditions**: TRL 5–6; 40 T reactor target vs. 15 T+ demonstrated on Polaris. The 40 T requirement is the same as the ARPA-E experiment target (MITRE/JASON 2018 assessment flagged this as the primary challenge).
+- **Pulsed EM coils (Al, no superconductors)**: TRL 6–7; proven materials and manufacturing; Polaris coils operational.
+- **Capacitor bank (>50 MJ, tens of kV)**: TRL 5–6; Polaris bank demonstrated; partly manufactured in-house.
+- **Direct inductive energy recovery (IGBTs)**: TRL 5–6; >95% round-trip efficiency demonstrated for >1 million pulses at smaller scale (Grande, 2015); Polaris-scale demonstration in progress.
+- **Shielding (borated polyethylene + borated concrete)**: TRL 8–9; standard materials used in medical particle beam facilities; approximately 1-meter solid barrier confirmed.
+- **Regulatory**: Washington State HB 1018 (2025) classifies fusion as clean energy, enabling local permitting. Washington State DOH Large Broad Scope tritium license granted (Aug 2024). Permitting for Orion site underway.
+
+**Poorly documented**:
+- Repetition rate scale-up: Trenta operated at ~1 pulse/10 min; Polaris targets 1 Hz — a ~600× step in rep rate. No intermediate milestones published.
+- Chamber / first wall lifetime under pulsed loading: not discussed in any public source.
+- Vacuum system and neutral gas management: not described for commercial scale.
+- He3 separation and fuel handling hardware: not documented publicly.
+- IGBT switching hardware at commercial power levels: not documented.
 
 **Gaps**:
-- D-He3 operation TRL (not yet demonstrated on any prototype) — `truly-unknown` (milestone pending) — blocking
-- High rep-rate (≥1 Hz) sustained operation TRL — `proprietary` (Polaris data not released) — blocking
-- He3 breeding subsystem TRL — `truly-unknown` — important
-- Full system integration at commercial field and power — `truly-unknown` — important
+- Achieved repetition rate on Polaris — proprietary — blocking (determines power output and economics)
+- D-He3 operation at ~200M°C — not yet demonstrated (Polaris still demonstrating D-T at 150M°C as of Feb 2026) — blocking (commercial fuel cycle unvalidated)
+- Net electricity demonstration on Polaris — not yet achieved (originally promised 2024, pushed to "during Polaris campaign") — blocking
+- Chamber / first wall lifetime and replacement schedule — proprietary — important
+- He3 separation and fuel handling TRL — not-yet-sourced — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Poor
 
-**Available**:
-- Contrary Research identifies in-house manufacturing of quartz tubes and high-voltage capacitors; supply chain noted as "main potential risk" per the report. (`contrary-research-helion.md`)
-- Dossier notes ~720 miles of coaxial cables per machine (copper, aluminum, custom alloys).
-- Capacitor bank parameters known: >50 MJ, tens of kV, high-voltage IGBTs.
-- Aluminum coils explicitly called out as preferable to superconducting magnets (cost/complexity advantage). No cryogenic supply chain needed.
-- D fuel cycle: deuterium from water — essentially unlimited supply, commodity availability.
-
-**Missing**:
-- No published materials qualification study for the plasma-facing components (quartz tubes at commercial fluence and cycling rate).
-- No published supply chain assessment for high-voltage pulsed power components at GW-scale manufacturing.
-- Custom high-voltage capacitor supply: partial in-house, partially external — external sourcing not disclosed.
-- IGBT requirements at commercial scale: switching at ≥1 Hz with >50 MJ discharge — no published specification.
-- He3 startup inventory: how much He3 is needed before self-breeding is sufficient? Not published.
-- Tritium handling infrastructure (for Polaris D-T phase): regulatory approved, but commercial-scale is different.
-- Materials irradiation qualification for D-He3 (low neutron flux): likely more tractable than D-T, but no study published.
+**Available**: Contrary Research identifies Helion's supply chain as the "main potential risk." Some materials are confirmed:
+- **Coil material**: Aluminum (not superconductors); standard industrial supply
+- **Cable materials**: Copper, aluminum, custom alloys (~720 miles total in Polaris per website)
+- **Quartz tubes**: Manufactured in-house by Helion
+- **High-voltage capacitors**: Partly in-house, partly purchased
+- **High-voltage IGBTs**: Commercial semiconductor components; no specific manufacturer named
+- **Shielding**: Borated polyethylene and borated concrete — established supply chains (medical accelerator industry)
+- **Deuterium**: From water electrolysis; essentially unlimited at cost of ~$1–3/g; no supply constraint
+- **Helium-3**: Self-bred from DD side reactions; requires no external supply at commercial steady-state; startup requires either accumulated tritium/He3 from D-D campaigns or external purchase
+
+**Missing**: No published bill of materials for commercial plant. The scale-up from >50 MJ prototype capacitor bank to a commercial power plant is undefined. There is no published analysis of capacitor bank lifetime, replacement rate, or supply chain.
 
 **Gaps**:
-- High-voltage capacitor/IGBT supply chain at commercial volume — `proprietary` — important
-- Quartz tube lifetime and replacement rate at commercial rep rate — `proprietary` — important
-- He3 startup inventory requirement — `proprietary/derivable` — important
-- Materials irradiation database for D-He3 fluence environment — `not-yet-sourced` — important (may exist in D-He3 materials literature)
-- BOP (balance of plant) materials/supply chain — `not-yet-sourced` (no steam cycle — simpler, but no study) — nice-to-have
+- Commercial-scale capacitor bank specifications and supply chain — proprietary — important
+- High-voltage IGBT supply chain and replacement schedule — not-yet-sourced — important
+- He3 startup inventory strategy (quantity, cost, sourcing prior to self-bred sufficiency) — derivable — important
+- First wall / plasma-facing material specification — proprietary — important
+- Coil fabrication and replacement schedule at commercial rep rate — proprietary — important
+- Critical mineral dependencies — not-yet-sourced — nice-to-have (Al/Cu supply chains are commodity; no REEs or superconductors, which is an explicit advantage)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric power (first plant) | 50 MWe | Helion website / PPA | medium |
-| Net electric power (future) | 500 MWe | Nucor partnership | low |
-| Repetition rate (design point) | 2 Hz @ 50 MW | ARPA-E presentation | medium |
-| Direct conversion efficiency | 85–95% | Contrary Research (CEO claim) | low |
-| Energy recovery (subscale demo) | >95% round-trip | Dossier / Helion press | medium |
-| Magnetic energy recovery η | 0.7 | ARPA-E presentation | medium |
-| Fusion energy per pulse | Not published (implied ~25 MJ at 50 MW, 2 Hz) | Derivable | low |
-| Neutron energy fraction | ~5% | Helion website | medium |
-| Fuel: external input | Deuterium only | Dossier | high |
-| Magnet field (reactor) | 40 T | ARPA-E presentation | medium |
-| Capacitor bank energy | >50 MJ (Polaris) | Helion website | medium |
-| Plant size (modular) | "Shipping container scale" | Helion website | low |
-| Analog LCOE (MIF modular) | $34–54/MWh | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | low (different concepts) |
-| Analog CapEx (MIF modular) | ~$2.4/W, ~$1.2B @ 500 MWe | Same ARPA-E revisit | low (different concepts) |
-| LCOE target (third-party) | $0.01–0.06/kWh | Thunder Said Energy | very low |
+| First commercial plant output | 50 MWe | Contrary Research / Wikipedia (Microsoft PPA) | H |
+| Second plant output | 500 MWe | Wikipedia (Nucor agreement) | H |
+| Repetition rate (target) | ~1–2 Hz | ARPA-E presentation / website | H |
+| Capacitor bank size (prototype) | >50 MJ | Helion website (Polaris) | H |
+| Direct energy recovery efficiency (claimed) | 85–95% | Contrary Research / Helion website | M |
+| Energy recovery (subscale demonstrated) | >95% round-trip | Helion website (Grande, 1M+ pulses) | M |
+| Reactor compression field (commercial target) | 40 T | ARPA-E presentation | H |
+| Reactor compression field (Polaris) | 15 T+ | Helion website | H |
+| D-He3 energy per reaction | 18.3 MeV (3.6 α + 14.7 p) | Helion website | H |
+| Neutron energy fraction (D-He3, claimed) | ~5% | Helion website | M |
+| Fuel input | Deuterium only (from water) | Helion website | H |
+| No steam cycle / no turbines | Confirmed | Multiple sources | H |
+| No superconducting magnets | Confirmed (Al coils) | Contrary Research | H |
+| No tritium breeding blanket | Confirmed (self-bred He3) | Helion website | H |
+| Orion construction start | July 2025, Malaga WA | Wikipedia / Reuters | H |
+| Orion target delivery | 2028 (Microsoft) | Wikipedia | H |
+| LCOE target (aspirational, unverified) | 1–6 ¢/kWh | Thunder Said Energy | L |
+| CAS analogue: structures/site (MIF, 500 MWe) | $174–370M | ARPA-E ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | L (different concepts, different scale) |
+| CAS analogue: electric plant equipment (MIF, 500 MWe) | $44–93M | ARPA-E ALPHA re-costing (same source) | L |
+| CAS analogue: total LCOE range (MIF, 500 MWe) | $34–54/MWh | ARPA-E ALPHA re-costing (same source) | L (thermally-coupled MIF concepts, not direct conversion) |
+
+**ARPA-E ALPHA costing integration note**: The ALPHA re-costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers Plasma-Jet MIF (LANL/HyperJet), Stabilized Liner Compressor (CFS Inc.), Staged Z-Pinch (MIFTI), and Flow-stabilized Z-Pinch (Zap Energy) — none of which use direct inductive energy conversion. Helion is not among the four. CAS accounts that involve a steam/thermal cycle — turbine plant ($101–217M), main heat transfer ($63–184M) — do not apply to Helion. Accounts for structures/site, electric plant equipment, misc, and heat rejection (significantly reduced without steam cycle) provide lower-bound analogues only. Power supplies (22.1.7): $11.9–140.4M average $55.8M in the ALPHA study — Helion's capacitor bank is the dominant unique subsystem and would likely fall in or above this range at commercial scale, but the ALPHA concepts do not use large capacitor banks as the primary power conversion path. This source is useful for CAS framework methodology and BOP structure analogues, but does not resolve any blocking LCOE gaps.
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by CAS subsystem | proprietary | blocking | No plant study published; analog from ARPA-E ALPHA revisit (different concepts) is only reference |
-| Plasma gain Q (commercial design) | proprietary | blocking | Net electricity not yet demonstrated; efficiency formula (η·G=0.24) implies Q requirement but G not specified for Orion |
-| Capacity factor / availability | truly-unknown | blocking | No commercial-rep-rate operation demonstrated; Trenta ran 16 months but at 1/10 min |
-| O&M costs (annual) | proprietary | blocking | No published data; capacitor/coil cycling costs are primary unknowns |
-| Recirculating power fraction | proprietary/derivable | blocking | Need to close the energy balance: G, η_recovery, and recirculating fraction together determine net electric output |
-| Construction cost / schedule | proprietary | important | Orion groundbreaking July 2025, no cost disclosure |
-| Capacitor bank replacement schedule | proprietary | important | Cycling lifetime at commercial rep rate not published |
-| Fuel cost (D at scale) | derivable | nice-to-have | Deuterium is cheap commodity; extractable from water at well-known cost |
-| He3 startup inventory cost | proprietary/derivable | important | He3 from DD takes years to accumulate; startup fuel cost unknown |
-| Decommissioning cost | not-yet-sourced | nice-to-have | Reduced activation relative to D-T; no published estimate |
-| Thermal rejection (no steam cycle) | derivable | nice-to-have | ~5% neutron energy goes to heat; waste heat management simplified but unquantified |
+| Capital cost by CAS subsystem | proprietary | blocking | Orion specs proprietary; no published plant study |
+| O&M cost (maintenance, replacement schedules) | proprietary | blocking | No published operations data |
+| Capacity factor / availability target | proprietary | blocking | No published RAMI analysis; rep rate not yet demonstrated at commercial scale |
+| Q factor / scientific/engineering gain | proprietary | blocking | Key for net electricity calculation; never publicly disclosed |
+| Commercial repetition rate achieved | proprietary | blocking | Polaris rep rate not disclosed in milestone announcement |
+| Capacitor bank cost at commercial scale | proprietary | important | Helion's largest unique cost driver; no published data |
+| Direct conversion system capital cost | proprietary | important | Novel system, no published cost model anywhere in literature |
+| He3 startup fuel inventory cost | derivable | important | Can be estimated from DD reaction fraction, tritium decay rate, and initial plasma conditions |
+| First wall / liner replacement schedule and cost | proprietary | important | Pulsed fatigue loading; no public data |
+| Plant construction cost (civil, modular) | not-yet-sourced | important | Modular factory-manufactured design; analogue from ALPHA costing exists but is for different plant scale (500 vs. 50 MWe) |
+| Net plant efficiency (wall-plug to wire) | not-yet-sourced | important | Derivable if Q and η_recovery are known; both are unknown |
 
 ---
 
 ## Source Recommendations
 
-- **Kirtley & Milroy, J. Fusion Energy (2023)** — extract this peer-reviewed paper; it contains the FRC scaling analysis underlying Helion's commercial case, and the 2026 peer response contains independent criticisms. Search: "Kirtley Milroy J Fusion Energy 2023 FRC scaling Helion." Both are in the dossier's key sources but not yet extracted. `not-yet-sourced` — confirm existence via DOI before searching.
+- **ARPA-E ALPHA re-costing (Woodruff Scientific 2020)** — Integrated above. Covers four MIF concepts, none of which is Helion. Provides CAS structure analogues for structures, BOP, and electric plant equipment. Explicitly does not cover direct inductive conversion or large capacitor banks. Gap type: the ALPHA costing does not resolve any blocking gaps for this concept because the cost architecture differs fundamentally; it is useful only as a lower-bound structural analogue for non-power-conversion cost accounts.
+
+- **Wurzel & Hsu (2021), Lawson criterion paper** — Integrated above. Provides FRC methodology for inferring triple products and peaking values (T₀/⟨T⟩=1.0, n₀/⟨n⟩=1.3 for FRC per Table V). Confirms FRC as a recognized MCF approach within the pulsed MIF category. Helion-specific data is not included (paper predates Trenta publication). Does not resolve any blocking LCOE gaps but supports TRL/physics analysis in sections 2–3.
 
-- **ARPA-E ALPHA 2017 original Bechtel costing report** — the 2020 revisit references it (report no. 26029-000-30R-G01G-00001); the 2017 study covered Helion directly as one of the four ALPHA concepts. If the original (not the revisit) is accessible, it would contain Helion-specific (though possibly proprietary/redacted) CAS cost data. `not-yet-sourced` — may be at woodruffscientific.com/pdf/ARPAE_Costing_Report_2017.pdf. `unverified — confirm existence before searching`.
+- **Simplified IFE economic model (Hawker 2020)** — Disqualified. This paper addresses IFE (specifically laser-driver and related pulsed systems) with a 14-parameter Monte Carlo LCOE model centered on target gain, rep rate, and driver cost. Helion does not use targets, does not use a laser/HI driver, and does not use a steam cycle — the three foundational assumptions of the IFE model. The model cannot be applied to Helion's direct inductive conversion architecture without reconstruction from first principles.
 
-- **JASON/MITRE 2018 report on Helion** — cited in Wikipedia; reviewed Helion's 8T vs. 40T challenge and projected breakeven timeline. Available publicly (partially redacted) at ARPA-E. May contain independent technical assessment of subsystem readiness. `not-yet-sourced` — confirm via ARPA-E documents archive. `unverified — confirm existence before searching`.
+- **Helion ARPA-E ALPHA contract publications** (search ARPA-E ALPHA project archive for "Staged Magnetic Compression of FRC Targets" DE-AR0000393): Helion's own ALPHA contract may have produced public progress reports with quantitative plasma parameters. `not-yet-sourced` — search ARPA-E.energy.gov project pages and OSTI for final reports. `unverified — confirm existence before searching`.
 
-- **Slough et al., Nuclear Fusion 51(5) (2011)** — already referenced in dossier; the merging/compression FRC paper provides the foundational plasma physics. Should be extracted if not already. `not-yet-sourced`.
+- **Kirtley & Milroy (2023) FRC scaling paper** (J. Fusion Energy, doi:10.1007/s10894-023-00367-7) and its 2026 Comment (doi:10.1007/s10894-026-00554-2): Both cited in the dossier but not extracted as sources. These likely contain quantitative scaling analysis for FRC compression and heating that would support the system-function and TRL sections. `not-yet-sourced`. Priority: ingest via Zotero.
 
-- **DOE Fusion Industry Association (FIA) annual reports** — FIA tracks TRL and investment by company; may contain third-party TRL assessments for Helion subsystems. Search: "Fusion Industry Association State of Fusion Industry 2025." `not-yet-sourced`.
+- **MITRE/JASON 2018 report** ("Prospects for Low Cost Fusion Development," JSR-18-Task-011): Cited in Wikipedia on Helion and publicly available (ARPA-E website). Evaluated all ALPHA concepts including Helion. Flagged "whether they can simultaneously achieve sufficiently high compression while maintaining plasma stability" as the primary Helion challenge. Contains independent quantitative assessment. `not-yet-sourced`. Priority: ingest via Zotero.
 
-- **Helion ARPA-E ALPHA program reports (2015–2018)** — beyond the slide deck, full ARPA-E project reports may contain engineering details not in public articles. Search OSTI for "Helion ARPA-E ALPHA staged magnetic compression FRC." `not-yet-sourced` — `unverified — confirm existence before searching`.
+- **Slough et al. (2011) Nuclear Fusion** (doi:10.1088/0029-5515/51/5/053008): Cited in dossier but not extracted as a source. Contains quantitative FRC plasma parameter data from IPA experiments (300 km/s velocities, 2 keV D-D ion temperatures) providing the heritage physics baseline. `not-yet-sourced`. Priority: ingest.
 
-- **D-He3 nuclear reaction cross-section literature** — needed for neutron fraction (5% vs. 10% dispute) and energy balance at 200 M°C. Standard nuclear physics reference (NRL Plasma Formulary or Bosch & Hale 1992). `not-yet-sourced` — standard reference, confirm availability.
+- **GeekWire articles on Polaris tour (2025) and manufacturing at scale (2025)**: Cited in dossier and describe subsystem architecture in accessible language. The manufacturing article reportedly discusses supply chain risks. These are brief journalism pieces but may add qualitative TRL detail for section 3. `not-yet-sourced` (URLs in dossier).
 
 ---
 
 ## Summary
 
-Proceed to full analysis with the following scoping: the qualitative sections (data availability, system function, subsystem maturity, materials) can be written with medium-to-high coverage from available sources, with explicit acknowledgment of Helion's exceptional opacity around plant-level engineering. The LCOE quantitative section should use ARPA-E ALPHA revisit analog values ($2.4/W CapEx, $34–54/MWh LCOE for modular MIF) as order-of-magnitude anchors, and flag that all cost figures are analogues, not Helion-specific. The central uncertainty — whether net electricity is achievable at all — must be treated as a key risk axis in the analysis rather than an assumed baseline. Acquiring the Kirtley & Milroy (2023) paper and the original 2017 Bechtel/ARPA-E ALPHA costing report (if publicly accessible) would most improve LCOE parameter coverage before analysis.
+**Proceed to full qualitative analysis now.** The physics and technology architecture sections (1–3) can be completed at high quality with the existing sources. Section 4 (materials/supply chain) will be thin but can document what is known (aluminum coils, in-house quartz tubes, capacitors, cable materials) alongside explicit gap acknowledgments. Section 5 (LCOE) cannot produce a quantitative model from public sources: capital costs, O&M, capacity factor, and Q factor are all proprietary. The correct approach is to document the structural cost differentiators (no steam cycle, no superconductors, no tritium blanket = significant cost reductions vs. standard MFE), identify the unique cost drivers (capacitor bank, direct conversion hardware, pulsed fatigue maintenance), and use the ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) for non-power-conversion BOP analogues while noting their limitations.
+
+Before detailed LCOE modeling, ingesting the Kirtley & Milroy (2023) scaling paper and the MITRE/JASON 2018 report would most materially improve the analysis. The Kirtley & Milroy paper may contain Q estimates or scaling projections; the JASON report provides an independent expert evaluation of achievability.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
+overall_rating: "Mostly Ready"
 blocking_count: 6
-important_count: 8
-counting_method: "blocking: 5 LCOE parameter gaps (CapEx by CAS, plasma gain Q, capacity factor, O&M, recirculating power fraction) + 1 physics/concept gap (40T compression stability not demonstrated, D-He3 not demonstrated); important: He3 breeding engineering, high rep-rate TRL, capacitor lifecycle, materials irradiation database, He3 startup inventory, construction cost, Kirtley & Milroy paper not extracted, FIA TRL data not sourced; deduplicated across all sections"
+important_count: 6
+counting_method: "deduplicated_across_all_sections — six blocking gaps: (1) Q factor/gain never disclosed, (2) commercial repetition rate not demonstrated or disclosed, (3) net electricity not yet demonstrated on Polaris, (4) D-He3 operation at 200M°C not yet demonstrated, (5) capital costs by CAS subsystem proprietary, (6) O&M costs proprietary; six important gaps: (1) capacity factor/availability not published, (2) capacitor bank commercial-scale cost, (3) direct conversion system cost, (4) He3 startup inventory, (5) first wall/liner replacement schedule, (6) plant civil construction cost at 50 MWe scale"
 section_coverage:
-  availability_of_data:       "Partial"
-  system_function:            "Partial"
+  availability_of_data:       "Good"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
```
