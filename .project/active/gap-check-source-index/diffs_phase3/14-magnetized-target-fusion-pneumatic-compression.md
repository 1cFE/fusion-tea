# Phase 3 diff: 14-magnetized-target-fusion-pneumatic-compression

**Generated:** 2026-05-22T14:16:04-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 4 | 5 | 1 |
| important_count  | 5 | 7 | - |
| overall_rating   | Significant Gaps | Mostly Ready | - |

## Fleet-source dispositions in new report

```
124:- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — **Integrated**: provides the closest available public cost analog for compact modular MIF (four different concepts, same CAS framework). Covers four ARPA-E ALPHA concepts that are NOT General Fusion. The CAS 27 special materials range ($1–267M, avg $103M) directly informs liquid metal cost uncertainty; driver cost analog (CAS 22.1.7: $12–140M) provides bounds on piston system costs. Used as explicit analog with stated caveat.
125:- `knowledge/sources/tea_dt_mfe_cost_analysis/` — **Disqualified**: tokamak-focused MFE study ($140–550/MWh LCOE), based on superconducting magnets and regulatory assumptions for large-scale MCF; architecturally inapplicable to MTF pulsed-mechanical concepts. Not usable as analog.
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have all the information needed. The ARPA-E ALPHA revisit covers four different MIF concepts (not General Fusion itself), but provides directly applicable CAS-framework cost ranges for compact modular pulsed MIF plants. The TEA D-T MFE source is tokamak-focused with LCOE $140-550/MWh — not applicable to MTF. The Lawson criterion paper is physics-only with no cost relevance to MTF. I have sufficient information to write the assessment.
```

## Blocking-tier lines (new)

```
103:| Capital cost by CAS category (GF-specific) | proprietary | blocking | No plant study published; ARPA-E analog gives order-of-magnitude bounds only |
104:| Recirculating power fraction (piston steam system) | proprietary | blocking | Critical for net output and LCOE; steam self-powering claimed but fraction not disclosed |
105:| Q value / energy per pulse (commercial) | proprietary | blocking | Determines gross fusion power; 350-fold compression to achieve Lawson criterion stated but Q not quantified |
108:| Piston/driver capital cost | proprietary | blocking | Cost of pneumatic piston array is the unique GF cost driver; no public estimate |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/14-magnetized-target-fusion-pneumatic-compression.md	2026-05-22 12:59:21.068601652 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/14-magnetized-target-fusion-pneumatic-compression/gap_report.md	2026-05-22 14:16:04.765197963 -0700
@@ -1,64 +1,42 @@
-Now I have enough information to write the gap assessment. Let me compile the full report.
-
----
+I now have all the information needed. The ARPA-E ALPHA revisit covers four different MIF concepts (not General Fusion itself), but provides directly applicable CAS-framework cost ranges for compact modular pulsed MIF plants. The TEA D-T MFE source is tokamak-focused with LCOE $140-550/MWh — not applicable to MTF. The Lawson criterion paper is physics-only with no cost relevance to MTF. I have sufficient information to write the assessment.
 
 # Gap Assessment: Magnetized Target Fusion - Pneumatic Compression (D-T)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
-**Summary**: General Fusion is among the more transparent private fusion companies — 34 peer-reviewed publications, active national lab collaborations, and a 2025 peer-reviewed fuel cycle study provide solid physics and fuel cycle data. However, no published plant economics study, capital cost breakdown, LCOE estimate, or net Q target for the commercial plant exists anywhere in the sourced literature. The LCOE analysis is severely constrained by the absence of basic economic parameters, and two key system uncertainties (recirculating power fraction, liquid metal selection) propagate directly into cost structure uncertainty.
+**Rating**: Mostly Ready
+
+**Summary**: General Fusion has been moderately transparent about its technology, and the combination of company sources, the peer-reviewed FST 2025 tritium fuel cycle paper (SRNL), and the Wikipedia article provides solid coverage of concept function, subsystem architecture, and known engineering challenges. However, no published cost study or plant-level economic analysis exists for this concept, and several key commercial-scale engineering challenges (1 Hz vacuum re-establishment, pneumatic compression at 4 m scale, recirculating power fraction) remain undemonstrated or unpublished. A qualitative D1+ analysis can proceed, but the LCOE section will require explicit placeholders with stated derivation assumptions rather than source-backed values.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Good
 
-**Available**:
-- Company description of technology concept and commercial target (300 MWe from two 150 MWe units, ~1 Hz, ~4 m cavity diameter): `generalfusion.com/fusion-technology/`, `generalfusion.com/commercialization-path/`
-- Peer-reviewed plasma performance data: >10 ms energy confinement time, ~6×10^19 m^-3 density, >400 eV temperature without active stabilization or auxiliary heating: `generalfusion-post-peer-reviewed-publication-confirms.md`, `globenewswire-news-release-2022-12-12...md`
-- Compression parameters: density target 10^22 to 10^25 ions/m^3, temperature 0.1 to 10 keV, magnetic field 2 to 200 T: dossier citing APS 2018 overview
-- LM26 experimental milestone (April 2025): first integrated plasma compression with lithium liner showing ion temperature and density increases: `metaltechnews-story-2025-05-14...md`
-- Detailed fuel cycle analysis for both PbLi and pure Li blanket options: tritium inventories, TBR values, startup inventory (<1 kg), plant doubling time: `general-fusion-fst-2025-fuel-cycles.md`
-- Commercialization roadmap: Lawson Program (LM26 to mid-2028), then commercialization engineering program, FOAK plant ~2035: `generalfusion-fusion-demo-plant.md`
-- Company collaborations: Hatch (power plant engineering), Kyoto Fusioneering (tritium/liquid metal BOP), CNL (BOP integration study April 2024), PPPL, ORNL, SRNL: `en-wiki-general-fusion.md`
-- Financial and organizational context including May 2025 layoffs (~25% of workforce) and January 2026 SPAC merger plans: `en-wiki-general-fusion.md`
-
-**Missing**:
-- No published plant economics study or conceptual design report (CDR)
-- No LCOE estimate from company or any third party
-- No published Q (fusion gain) target for the commercial plant — LM26 targets the Lawson criterion (nTτ > 10^21 m^-3·keV·s), not Q > 1
-- Hatch/CNL BOP integration study from April 2024 not publicly available
-- No published piston count, piston specifications, or driver cost estimates for the commercial design
+**Available**: Company sources (generalfusion.com technology and commercialization pages) provide a clear operational concept description — liquid metal liner, pneumatic pistons, ~4 m cavity, 1 Hz rep rate, 300 MWe from two 150 MWe modules, steam Rankine energy capture. The FST 2025 paper (SRNL/General Fusion, Fusion Science and Technology, DOI: 10.1080/15361055.2025.2526266) is the most substantive peer-reviewed source, covering tritium fuel cycle in detail for both LLE and pure Li blanket candidates. The IAEA FEC 2025 abstract and GlobeNewswire 2022 press release confirm plasma performance milestones (>10 ms confinement, >400 eV, compression time ~5 ms). The Wikipedia article documents the full R&D history, challenge list, funding (~$430M+), and cancelled UK Fusion Demonstration Program ($400M, 70% scale). Research collaboration partnerships are also documented: Kyoto Fusioneering (fuel cycle/liquid metal systems), Hatch (BOP engineering), CNL (plant integration studies).
+
+**Missing**: No published cost study or plant-level economic analysis. No detailed specifications for commercial-scale piston hardware (materials, count, stroke, synchronization tolerances at 4 m scale). The cancelled UK Fusion Demo Program would have contained the most engineering-complete plant design, but its detailed specifications were not published.
 
 **Gaps**:
-- Published plant economics study (CDR-level) — `proprietary` — **blocking**: Without it, capital cost structure cannot be grounded
-- Commercial plant Q value / fusion energy gain — `proprietary` — **blocking**: Determines whether net electricity output closes without extraordinary Q assumptions
-- Hatch/CNL BOP integration study (April 2024) — `proprietary` — **important**: Could resolve BOP cost and integration questions
+- No published LCOE, capital cost, or plant study for GF MTF — proprietary — blocking
+- Commercial plant engineering specifications (piston count at 4 m scale, valve/seal design, BOP integration) — proprietary — important
+- Status and final design outputs of the cancelled UK Fusion Demo Program (70% scale, $400M) — not-yet-sourced — nice-to-have
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
+**Coverage**: Partial
 
-**Available**:
-The sources clearly enumerate the key physics and engineering unknowns, which is essential for identifying where the LCOE model will carry the most uncertainty:
+**Available**: The operational cycle is well described: plasma injection via Marshall gun → pneumatic piston compression of liquid metal vortex → fusion burn (~1 ms timescale) → neutron energy capture in liquid metal → heat exchanger → steam turbine. The Wikipedia article explicitly lists the known engineering challenges acknowledged by the company's own CSO: liquid metal vaporization, plasma contamination by liquid metal impurities, implosion symmetry, kink instability of the liquid metal shaft, and flux diffusion in the liquid metal. A critical unresolved challenge also noted is re-establishing high-vacuum conditions in the time interval between pulses (< 1 second at commercial rep rate) — this is flagged as the most significant unresolved engineering obstacle for the commercial concept. GlobeNewswire 2022 confirms 5 ms compression time in prototype and 10 ms plasma confinement (sufficient margin). LM26 data (April 2025) shows integrated plasma compression with lithium liner was achieved, but using electromagnetic (not pneumatic) compression of solid (not liquid) lithium — a significant gap relative to the commercial concept.
 
-- **Recirculating power fraction**: Steam from the Rankine cycle partially drives the pistons (`en-wiki-general-fusion.md`: "some of the steam is recycled to power the pistons"). The fraction consumed by piston recharge versus delivered to the grid is not quantified anywhere in the sources. This is the central LCOE uncertainty — a large recirculating fraction would dramatically cut net electrical output.
-- **High-vacuum re-establishment at 1 Hz**: Wikipedia explicitly identifies this as an unresolved engineering obstacle; the 70% scale UK demo planned at 1 pulse/day specifically avoided this problem (86,400× more time to re-establish vacuum). At 1 Hz this requires solving in <1 second.
-- **Plasma-liner instability at fusion conditions**: Wikipedia lists "confinement at high energy density is not known," liquid metal vaporization (LLNL collaboration ongoing), and plasma cooling by liquid metal impurities as open challenges.
-- **Liquid metal selection undecided**: PbLi vs. pure Li each has different TBR, plasma contamination behavior (Pb is high-Z, contaminates plasma via Bremsstrahlung), tritium extraction complexity, and materials compatibility. FST 2025 paper confirms neither has been selected.
-- **Piston synchronization at 4 m scale**: Prototype demonstrated 2 μs timing at 1 m scale. Commercial cavity is ~4 m diameter; synchronization scaling and structural dynamics are not demonstrated.
-
-**Missing**:
-- No system code output (PROCESS, SYSCODE, etc.) for this concept
-- No published analysis of recirculating power fraction
-- No published driver efficiency (piston energy → plasma kinetic energy conversion efficiency)
+**Missing**: Net energy balance and recirculating power fraction (the pistons are steam-driven, partially self-powering, but the fraction of plant output consumed by compression drivers is not published). Scientific gain (Q_sci) projections for the commercial operating point are not public. Integrated liquid metal vortex + plasma compression with pneumatic pistons has not been demonstrated at any scale.
 
 **Gaps**:
-- Recirculating power fraction — `proprietary/derivable` — **blocking**: This directly determines net electrical output and LCOE; no analog or published estimate exists
-- Vacuum re-establishment solution — `not-yet-sourced` — **important**: OSTI/conference literature may have GF or community work on this; unresolved in sources
+- 1 Hz vacuum re-establishment between pulses not solved; no published approach — truly-unknown / proprietary — blocking
+- Integrated liquid metal vortex compression with magnetized plasma not demonstrated (LM26 uses solid Li/EM compression) — truly-unknown (developmental gap) — blocking for cost model anchoring
+- Recirculating power fraction (piston steam consumption as fraction of gross output) — proprietary — blocking
+- Q_sci projections for commercial operating point — proprietary/not-yet-sourced — important
 
 ---
 
@@ -66,134 +44,105 @@
 **Coverage**: Partial
 
 **Available**:
+- **Plasma injector (Marshall gun / PI3)**: TRL ~5-6 — demonstrated at 50% commercial scale; PI3 achieved >10 ms confinement, >400 eV, density ~6×10^19 m^-3 without active stabilization or auxiliary heating; published in *Nuclear Fusion* (peer-reviewed).
+- **Electromagnetic compression / solid lithium liner (LM26 proxy)**: TRL ~4 — LM26 first integrated plasma compression with solid lithium liner in April 2025; electromagnetic proxy for commercial pneumatic system.
+- **Liquid metal cavity compression (water proxy, 1:10 scale)**: TRL ~4 — 1,000+ shots on water cavity prototype validating symmetry and shape sufficient for fusion conditions when scaled; peer-reviewed results.
+- **Power conversion (steam Rankine)**: TRL ~8-9 — fully mature technology; liquid metal heat exchanger coupling is standard.
+- **Tritium processing**: TRL ~3-4 — detailed ASPEN Plus models developed by SRNL (FST 2025) for both LLE and Li blanket options, with startup inventories of 317 g (LLE) and ~847 g (Li); no demonstration facility.
+- **Liquid metal handling/pumping**: TRL ~5 — actively developed with Kyoto Fusioneering; no published performance data at commercial scale.
 
-| Subsystem | TRL Assessment | Basis in Sources |
-|-----------|---------------|-----------------|
-| Plasma injector (compact toroid) | TRL 5–6 | >10 ms confinement at 50% commercial scale demonstrated (PI3/LM26); ~400 eV, 6×10^19 m^-3 without auxiliary heating |
-| Lithium liner compression (electromagnetic) | TRL 4–5 | LM26 integrated test April 2025; initial diagnostics show ion temp/density increase; >1,000 shots on compression prototype |
-| Pneumatic piston system (commercial) | TRL 3–4 | Collaboration with "major automaker" ongoing; 1 m prototype demonstrated (2012–2013) at 50 m/s, 2 μs timing; 4 m commercial scale not demonstrated |
-| Liquid metal vortex flow system | TRL 3–4 | 1:10 scale water compression demonstrated (2021–2022); no full liquid metal vortex at power-plant scale |
-| Tritium breeding/extraction (LLE) | TRL 3–4 | SRNL analysis complete; GLC at 40% efficiency chosen; low TRL for fusion-scale throughputs |
-| Tritium breeding/extraction (pure Li) | TRL 2–3 | LiT electrolysis at "very low TRL" (FST 2025); blanket extraction the critical technology |
-| Heat exchanger / Rankine cycle | TRL 7–8 | Standard industrial technology; liquid metal coupling is an integration challenge but not novel |
-| Seals, valves, liquid metal BOP | TRL 3–4 | Specifically called out by GF commercialization page as the next engineering program focus; not yet designed |
-| High-vacuum re-establishment at 1 Hz | TRL 1–2 | Not demonstrated; explicitly unresolved in Wikipedia |
-
-**Missing**:
-- TRL data for piston synchronization electronics at commercial scale
-- No published materials qualification data for seals/valves in Li or PbLi environments at operating temperatures
-- Plasma-liner integrated test with pneumatic pistons (not electromagnetic) — not yet performed
+**Missing**: No formal TRL assessment by subsystem published. Commercial-scale pneumatic piston system (4 m cavity, 1 Hz, 100+ pistons) has not been built or tested. Seal and valve performance at 1 Hz pulsed liquid metal environment undemonstrated. The commercialization program (mid-2028 per roadmap) plans to demonstrate these, but no data exists yet.
 
 **Gaps**:
-- Pneumatic piston + liquid metal vortex integrated demonstration — `truly-unknown` (awaiting demonstration) — **important**: The commercial concept has not been tested in this configuration at any scale; LM26 uses a different compression mechanism
-- Vacuum re-establishment at 1 Hz — `not-yet-sourced` — **important**: May be addressed in GF conference papers or INFUSE reports not captured in Phase 1a
+- Formal TRL assessment for commercial-scale subsystems not published — not-yet-sourced/proprietary — important
+- Commercial-scale pneumatic piston array (~4 m, 1 Hz, synchronized within 10 μs) — truly-unknown (not yet built) — blocking for TRL section
+- Piston-chamber seals and valves in pulsed liquid metal environment — truly-unknown — important
+- Tritium processing at relevant throughput scale — not-yet-sourced — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- Liquid metal: PbLi or pure Li — both identified, compositions known; neither selected for commercial plant (FST 2025)
-- Lithium supply: commercially available; Li-6 enrichment for higher TBR is an option but natural Li is baselined in some designs
-- Tritium startup inventory: <1 kg (317 g for LLE, ~750 g for Li designs) — manageable from CANDU supply (FST 2025)
-- No superconducting magnets required — eliminates REBCO tape supply chain bottleneck (a key competitive advantage)
-- No high-power lasers or pulse power systems required — conventional mechanical engineering
-- Piston technology: collaboration with "a major automaker" (company unnamed) suggests integration into existing manufacturing supply chains
-- Structural materials: conventional steels; no plasma-facing materials problem (liquid metal wall eliminates first-wall damage)
-
-**Missing**:
-- Piston count and specifications for commercial design are not published; cost-of-goods for the piston array is the primary capital cost unknown that is unique to this concept
-- Li-6 enrichment requirements and supply chain not analyzed in available sources
-- PbLi materials compatibility with structural steels at operating temperatures — partially addressed in broader fusion literature but not in GF-specific sources
-- No published manufacturing plan or supply chain analysis for the piston system
+**Available**: Liquid metal wall material candidates are well documented: lead-lithium eutectic (LLE, Pb-15.8 Li) or pure lithium (Li). FST 2025 paper (SRNL) provides detailed comparison including tritium extraction technologies, TBR values (1.40 for LLE, 1.25–1.80 for Li), in-process tritium inventories (303 g for LLE, 747–749 g for Li at steady state), and startup inventories. Lithium is globally available and not subject to significant supply chain risk. Lead for LLE is mature industrial material. Wikipedia notes plasma contamination by high-Z lead as a risk for LLE specifically, which is why pure Li is being explored despite its higher reactivity. Kyoto Fusioneering partnership addresses liquid metal system development.
+
+**Missing**: Piston and compression hardware material specifications (likely high-strength steel or specialized alloys) not published. Structural chamber materials under D-T neutron fluence not characterized for GF-specific geometry. Annual replacement schedule and costs for consumable components (liquid metal, seals) not published. No supply chain analysis for piston manufacturing at commercial scale.
 
 **Gaps**:
-- Piston array manufacturing cost/supply chain — `proprietary` — **important**: The piston array is the concept-defining cost item with no analog in other fusion approaches; no data available
-- Li-6 enrichment requirements — `derivable` from TBR analysis but not stated — **nice-to-have**
-- PbLi materials compatibility data — `not-yet-sourced` — **nice-to-have**: Exists in the broader fusion materials literature (EUROFER, etc.)
+- Piston and structural material specifications under operational conditions — proprietary — important
+- Neutron activation and material replacement schedule for structural components — not-yet-sourced — important
+- Supply chain for commercial-scale liquid metal system (pumps, heat exchangers, extraction units at Kyoto Fusioneering scale) — not-yet-sourced — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electrical output (commercial) | 300 MWe (2×150 MWe) | `generalfusion-post-peer-reviewed-publication-confirms.md`, `en-wiki-general-fusion.md` | H |
-| Repetition rate (commercial) | ~1 Hz | dossier (multiple sources) | H |
-| Cavity diameter (commercial) | ~4 m | FST 2025 (`general-fusion-fst-2025-fuel-cycles.md`) | H |
-| Plasma compression ratio | ~350× volumetric | FST 2025 | H |
-| Fuel type | D-T | multiple | H |
-| Energy conversion | Thermal Rankine (steam) | multiple | H |
-| TBR (LLE design) | 1.4 | FST 2025 | H |
-| TBR (Li design) | 1.25–1.80 | FST 2025 | H |
-| Tritium startup inventory (LLE) | ~317 g | FST 2025 | M |
-| Tritium startup inventory (Li) | ~750–800 g | FST 2025 | M |
-| Pre-compression plasma density | ~6×10^19 m^-3 | `globenewswire...` press release | M |
-| Pre-compression confinement time | >10 ms | `peer-reviewed-publication-confirms.md` | H |
-| Pre-compression temperature | >400 eV | `globenewswire...`, IAEA FEC 2025 | H |
-| Target compression temperature | 10 keV | IAEA FEC 2025 | H |
-| Target post-compression density | ~10^25 ions/m^3 | dossier (APS 2018) | M |
-| FOAK plant operations target | ~2035 | `generalfusion-fusion-demo-plant.md` | M |
+| Net electric power | 300 MWe (2× 150 MWe modules) | generalfusion.com/commercialization-path | h |
+| Repetition rate | ~1 Hz | FST 2025, company sources | h |
+| Fuel cycle | D-T, tritium bred in-situ | FST 2025, company sources | h |
+| TBR (LLE blanket) | 1.40 | FST 2025 (SRNL/GF) | h |
+| TBR (Li blanket) | 1.25–1.80 | FST 2025 (SRNL/GF) | h |
+| Tritium startup inventory (LLE) | 317 g | FST 2025 | h |
+| Tritium startup inventory (Li) | 747–793 g | FST 2025 | h |
+| Plant doubling time | 56 days (LLE), 67 days (Li) | FST 2025 | h |
+| Cavity diameter (commercial) | ~4 m | FST 2025 | h |
+| Energy capture | Thermal/steam Rankine | Company sources | h |
+| FOAK target date | ~2035 | generalfusion.com | m |
+| MIF analog LCOE (ARPA-E ALPHA, 4 different concepts) | 34–54 $/MWh | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
+| MIF analog CapEx (~500 MWe modular) | $0.84–1.64B | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
+| MIF analog specific capital cost | 2.0–3.3 $/W | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
+| MIF analog O&M | $42–61 M/year | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` | l (analog only) |
 
-**Missing Parameters**:
+**Note on ARPA-E ALPHA analog**: The Woodruff/ARPA-E revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers four compact modular MIF concepts (PJMIF, Stabilized Liner Compressor, Staged Z-Pinch, Zap Energy) using the same CAS framework — none of which is General Fusion. These are the closest available public cost analogs for compact pulsed MIF plants at ~500 MWe scale. Key CAS line items relevant to GF: CAS 22.1.1 (First Wall/Blanket: $4–117M, average $57M), CAS 22.1.7 (Power Supplies — proxy for piston driver system: $12–140M, average $56M), CAS 27 (Special Materials including liquid metal: $1–267M, average $103M). These ranges reflect the wide uncertainty in novel MIF power core components and are usable as order-of-magnitude bounds only.
 
+**Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Net fusion energy gain (Q) for commercial plant | proprietary | blocking | LM26 targets Lawson criterion, not Q > 1; commercial Q not stated anywhere |
-| Recirculating power fraction (pistons) | proprietary | blocking | Steam partly powers pistons; fraction not published; drives net output |
-| Thermal cycle efficiency (steam cycle parameters: T, P) | derivable | blocking | Can assume ~33–35% Rankine but steam T depends on liquid metal operating temp, which is not published |
-| Liquid metal operating temperature | proprietary | important | Determines steam cycle temperature and thus thermal efficiency |
-| Capital cost by subsystem | proprietary | blocking | No published estimate; no CDR or plant study publicly available |
-| Total capital cost (FOAK or nth-of-a-kind) | proprietary | blocking | Not published anywhere in sourced literature |
-| Piston array cost (unit count × unit cost) | proprietary | important | Concept-defining cost item; not analogous to any costed fusion concept |
-| O&M annual cost estimate | proprietary | important | Not published; Rankine cycle analogs exist but piston maintenance is concept-specific |
-| Capacity factor / availability | derivable | important | No published estimate; piston maintenance frequency and duration unknown |
-| Plant lifetime (years) | derivable | nice-to-have | No published estimate; assume 30–40 years as fusion default |
-| First wall replacement schedule | not applicable | — | Liquid metal wall eliminates this cost item (advantage) |
-| Driver energy per pulse | proprietary | important | Not published; needed to calculate recirculating power |
-| Fusion power per pulse | derivable | important | Can be estimated from cavity volume + compression ratio + burn fraction, but burn fraction not published |
-| Burn fraction (β) | partially available | important | FST 2025 gives β = 0.0163 (LLE) and 0.0206 (Li) for fuel cycle modeling — usable |
+| Capital cost by CAS category (GF-specific) | proprietary | blocking | No plant study published; ARPA-E analog gives order-of-magnitude bounds only |
+| Recirculating power fraction (piston steam system) | proprietary | blocking | Critical for net output and LCOE; steam self-powering claimed but fraction not disclosed |
+| Q value / energy per pulse (commercial) | proprietary | blocking | Determines gross fusion power; 350-fold compression to achieve Lawson criterion stated but Q not quantified |
+| Capacity factor / plant availability | not-yet-sourced | important | No published estimate; ~1 Hz rep rate means pulse reliability drives availability |
+| Thermal conversion efficiency | derivable | important | Standard Rankine ~33%; not optimized parameters published |
+| Piston/driver capital cost | proprietary | blocking | Cost of pneumatic piston array is the unique GF cost driver; no public estimate |
+| O&M costs (GF-specific) | proprietary | important | No published estimate; ARPA-E analog gives $42–61 M/year for ~500 MWe |
+| Decommissioning cost | not-yet-sourced | nice-to-have | No published estimate; standard fusion plant assumptions could be borrowed |
+| Learning curve / Nth-of-a-kind cost reduction | proprietary | nice-to-have | ARPA-E ALPHA revisit applies ~learning curve credits yielding COE2 from COE1 |
 
 ---
 
 ## Source Recommendations
 
-**Fleet-wide source to open**: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — The ARPA-E ALPHA program specifically targeted low-cost alternative fusion approaches; at least one of the four costed concepts may have been an MTF/MIF concept. Read `output.md` to check whether any MIF/liner concept was included. If so, this is the strongest available cost analog. Flag: **read before finalizing LCOE model**.
-
-**Fleet-wide source to use for BOP/O&M analogs**: `knowledge/sources/tea_dt_mfe_cost_analysis/` — Standard D-T MFE BOP cost structure (balance of plant, Rankine cycle, tritium handling, decommissioning) should apply directly to GF MTF. The piston array replaces the magnet system; subtract CAS22/23 magnet costs, substitute a piston-array cost estimate.
-
-**PyFECONS**: `~/PyFECONS` — Useful for the LCOE calculation framework and CAS hierarchy. MFE and MIF modules may exist; check whether an MTF-specific configuration is included.
-
-**Gap-filling searches** (not-yet-sourced gaps):
-- **Commercial Q estimate**: Search OSTI and arXiv for "General Fusion MTF gain" or "magnetized target fusion Q commercial" — GF has presented at conferences (APS DPP annual) with operational parameters; some may cite a target gain. `unverified — confirm existence before searching`
-- **Piston driver energy**: The 2013 GF proof-of-concept compression system paper (likely in Journal of Fusion Energy or Nuclear Fusion) may give piston energy and efficiency at 1 m scale. `unverified — confirm existence before searching`
-- **Recirculating power fraction**: Search for "(steam piston OR pneumatic driver) (fusion OR MTF) (recirculating power OR wall plug efficiency)" on OSTI. The INFUSE collaborations with ORNL and PPPL may have produced reports. `unverified — confirm existence before searching`
-- **CNL BOP integration study**: The April 2024 GF/CNL project "to examine and propose the most efficient and cost-effective designs to integrate the fusion machine, balance of plant, and power conversion systems" — check whether this has produced a report or conference abstract. `unverified — confirm existence before searching`
+- **GF MTF cost study / plant design report** — search OSTI for any DOE-funded techno-economic study of General Fusion or MTF concepts from the INFUSE or other programs; search for Hatch engineering study outputs (Hatch is GF's BOP engineering partner); search FIA (Fusion Industry Association) annual reports for any published cost projections — `not-yet-sourced`, `unverified — confirm existence before searching`
+- **CNL plant integration study (2024)** — CNL and General Fusion launched a project in April 2024 to examine cost-effective plant integration designs (Wikipedia); any published output from this collaboration would directly address BOP and power conversion cost estimates — `not-yet-sourced`, `unverified — confirm existence before searching`
+- **ARPA-E ALPHA original 2017 Bechtel costing report** — the 2017 precursor to the Woodruff revisit; General Fusion was not one of the four ALPHA concepts but this report provides the full CAS treatment for pulsed MIF concepts — `not-yet-sourced`, confirmed referenced in revisit paper (http://woodruffscientific.com/pdf/ARPAE_Costing_Report_2017.pdf)
+- **Kyoto Fusioneering publications on liquid metal BOP** — Kyoto Fusioneering is GF's partner on tritium fuel cycle and liquid metal systems; search for any published cost or engineering analyses from this partnership — `not-yet-sourced`, `unverified — confirm existence before searching`
+- **LANL MTF program reports** — LANL has a longstanding MTF program (FRX-L experiments, CRADA with GF); search OSTI for LANL MTF plant concept reports — `not-yet-sourced`
+
+**Fleet-wide source dispositions:**
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — **Integrated**: provides the closest available public cost analog for compact modular MIF (four different concepts, same CAS framework). Covers four ARPA-E ALPHA concepts that are NOT General Fusion. The CAS 27 special materials range ($1–267M, avg $103M) directly informs liquid metal cost uncertainty; driver cost analog (CAS 22.1.7: $12–140M) provides bounds on piston system costs. Used as explicit analog with stated caveat.
+- `knowledge/sources/tea_dt_mfe_cost_analysis/` — **Disqualified**: tokamak-focused MFE study ($140–550/MWh LCOE), based on superconducting magnets and regulatory assumptions for large-scale MCF; architecturally inapplicable to MTF pulsed-mechanical concepts. Not usable as analog.
+- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/` — **Disqualified for LCOE**: provides physics performance compilation only; no cost data, no MTF-specific economic content. Useful for §3 (subsystem maturity / physics progress benchmarking) but provides no new data beyond what is already captured from concept-scoped sources.
 
 ---
 
 ## Summary
 
-The concept is technically well-characterized: the physics approach, current experimental status (LM26 results), fuel cycle behavior (FST 2025), and key design parameters are documented well enough to describe the system and assess maturity. However, the LCOE analysis faces three blocking gaps: (1) no published Q for the commercial plant, (2) no capital cost estimate or plant economics study, and (3) the recirculating power fraction (pistons consume a share of turbine output) is unquantified. These three gaps make it impossible to produce a grounded LCOE estimate without fabricating the key inputs.
-
-**Recommendation**: Proceed to full analysis, but clearly bound assumptions. The LCOE model should: (a) read the ARPA-E ALPHA cost study for MTF cost analogs, (b) use MFE BOP costs as the baseline and substitute piston array for magnets with a wide uncertainty range, and (c) perform a sensitivity analysis over Q (1–5) and recirculating power fraction (10–50%) as the primary uncertain axes. Flag all three blocking gaps explicitly in the qualitative write-up.
+Proceed to full D1+ analysis with stated data limitations. The concept is unusually well-documented at the technology description and fuel cycle levels for a pre-commercial private company. Sections 1–4 can be written substantively, with the engineering challenge list (Section 2) being particularly rich. The LCOE section (Section 5) should be written with explicit analog-based estimates derived from the ARPA-E ALPHA revisit, with prominent uncertainty disclosure — no GF-specific cost data is public, and several cost-driving engineering questions (recirculating power, commercial piston costs, capacity factor) remain proprietary or unresolved. The analysis should note the significant financial and operational uncertainty from GF's May 2025 layoffs (~25% of workforce) and financing constraints, which affect the credibility of the 2035 FOAK timeline.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 4
-important_count: 5
-counting_method: "Gaps flagged 'blocking' across all five sections, deduplicated: (1) no published commercial Q / fusion gain, (2) no capital cost estimate or plant economics study, (3) recirculating power fraction unquantified, (4) thermal cycle parameters (liquid metal operating temperature) unpublished. Gaps flagged 'important' deduplicated: (1) piston array cost unknown, (2) O&M unknown, (3) capacity factor unknown, (4) vacuum re-establishment at 1 Hz unresolved, (5) pneumatic piston + liquid metal vortex not yet integrated."
+overall_rating: "Mostly Ready"
+blocking_count: 5
+important_count: 7
+counting_method: "deduplicated across all sections; LCOE blocking gaps counted once even if they appear in both §2 and §5 (recirculating power, Q value, piston cost, no cost study, 1 Hz vacuum re-establishment)"
 section_coverage:
-  availability_of_data:       "Partial"
-  system_function:            "Good"
+  availability_of_data:       "Good"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Poor"
```
