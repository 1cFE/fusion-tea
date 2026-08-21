# Diff: 09-qi-stellarator-hts

**Generated:** 2026-05-22T09:56:35-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 2 | 3 | 1 |
| important_count  | 8 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
10:**Summary**: The Proxima Fusion Stellaris paper (FED 2025, full text available) provides exceptionally detailed physics and engineering coverage — the most comprehensive publicly available reactor study for this concept. The primary gap is economic: the paper explicitly declares cost modeling "outside the scope" and lists it as future work. No capital cost breakdown, O&M estimate, or capacity factor figure is available from Proxima directly. These gaps are partially bridgeable via the Helios stellarator analog (Thea Energy, comparable HTS QI design, 390 MWe) and the fleet-wide TEA D-T MFE cost study (`knowledge/sources/tea_dt_mfe_cost_analysis/`), but Stellaris-specific cost structure remains unquantified.
159:4. **PyFECONS** (`/home/reid/PyFECONS`): Contains ARIES-CS costing algorithms implementable for compact stellarators. Can be used to derive capital cost analogues by parameterizing with Stellaris dimensions. — `derivable`, **high utility**
163:6. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): While targeting MIF and other concepts rather than stellarators, the costing methodology (CAS-based, 500 MWe plants) is directly applicable as a cross-concept methodology anchor. Fleet-wide source already registered — **check for stellarator-applicable parameters**.
173:**Before acquiring additional sources**, ingest the ARIES-CS full text (Lyon et al. 2008, FST) and check PyFECONS for stellarator costing algorithms — these are the two highest-leverage actions.
```

## Blocking-tier lines (baseline)

```
85:- 3D HTS coil winding demonstration at scale — `truly-unknown` (no one has wound a non-planar 20T HTS coil at power-plant current; this is a genuine TRL gap) — **blocking** for the technology, **important** for the analysis (flag as major risk)
```

## Blocking-tier lines (new)

```
57:- Recirculating power balance (cryogenics, ECRH, pumping, cooling) — `derivable` from analogy with Helios but uncertain — **blocking** for net electric accuracy
139:| Capital cost by subsystem (coils, blanket, vessel, BOP) | proprietary / not-yet-published | blocking | Stellaris paper explicitly defers; ARIES-CS analogue (not fully ingested) could partially fill |
140:| O&M cost (annual) | not-yet-sourced | blocking | No fusion stellarator O&M data available publicly for this class |
141:| Cryogenic recirculating power | derivable (with caution) | blocking | Table lists 111 MW to coils but unit/value uncertain; Helios uses ~10 MW for 40 kW at 20K |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/09-qi-stellarator-hts.md	2026-05-22 09:21:13.842863038 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/gap_report.md	2026-05-22 09:56:35.396443957 -0700
@@ -1,196 +1,190 @@
-Now I have everything needed. Let me write the gap assessment report.
+I now have enough information to write the comprehensive gap assessment. Let me compile it.
 
 ---
 
-# Gap Assessment: QI Stellarator - HTS
+# Gap Assessment: QI Stellarator - HTS (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
 
-**Summary**: The Stellaris paper (Fusion Eng. & Design 2025) is exceptionally detailed for a pre-commercial fusion concept — it covers plasma physics, engineering design, subsystem specifications, and materials in depth across a 337 KB extracted document. The major gap is economic: no cost breakdown by subsystem exists, and the thermal efficiency figure (~32%) is an assumption rather than a detailed cycle study. A high-quality qualitative write-up and a parametric LCOE model can both be produced from available data, but cost estimates will be rough-order-of-magnitude analogues, not bottom-up.
+**Summary**: The Proxima Fusion Stellaris paper (FED 2025, full text available) provides exceptionally detailed physics and engineering coverage — the most comprehensive publicly available reactor study for this concept. The primary gap is economic: the paper explicitly declares cost modeling "outside the scope" and lists it as future work. No capital cost breakdown, O&M estimate, or capacity factor figure is available from Proxima directly. These gaps are partially bridgeable via the Helios stellarator analog (Thea Energy, comparable HTS QI design, 390 MWe) and the fleet-wide TEA D-T MFE cost study (`knowledge/sources/tea_dt_mfe_cost_analysis/`), but Stellaris-specific cost structure remains unquantified.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-
-**Coverage**: Good
+**Coverage**: Partial
 
 **Available**:
-- *Stellaris* peer-reviewed paper (Garabedian et al., Fusion Eng. & Design 2025, DOI: 10.1016/j.fusengdes.2025.114868) — published, open-access extracted, highly detailed. Covers plasma equilibrium, engineering parameters, blanket, magnets, divertor, heating, and shielding. Source: `stellaris-design-details.md` / `stellaris-paper-details.md` (both appear to be extractions of the same document).
-- Thea Energy *Helios* comparison paper (132 KB) — a second QI stellarator design by a different company that serves as an independent data point for design parameters and efficiency assumptions. Source: `helios-stellarator-comparison.md`.
-- Proxima Fusion technology page — describes StarFinder optimization framework, QI-HTS value proposition, and W7-X scientific heritage. Source: `proxima-fusion-technology-page.md`.
-- Proxima/RWE/Bavaria MoU press release (Feb 2026) — confirms Alpha demo (~€2B), site selection, financing structure (~20% private / ~20% Bavaria / RWE + federal), and supplier intent. Source: `proxima-fusion-2026-updates.md`.
+- Full Stellaris paper (FED 214 (2025) 114868, 337 KB extracted, open-access CC BY-NC) — covers plasma physics, magnets, blanket, first wall, divertor, support structure, remote maintenance
+- Proxima technology page and press releases — company direction, magnet development milestones, Alpha demo timeline (EUR 2B, 2031, Q>1)
+- Helios stellarator paper (Thea Energy, arXiv 2512.08027, 176 KB extracted) — comparable QA HTS stellarator, closer to complete plant-level analysis including power balance Sankey diagram
+- WendelsteinW7-X background (Wikipedia, W7-X construction paper) — physics heritage
+- Physics papers (CIEMAT-QI4, arxiv-2404-16440) — turbulent transport basis
+- TEA D-T MFE fleet-wide source — LCOE framework for D-T MFE plants
 
 **Missing**:
-- No dedicated power plant economics report or system code study (analogous to ARIES, EUROfusion DEMO cost studies, or the Helion/CFS investor disclosures) has been sourced.
-- No independent TRL assessment from a third party (e.g., European fusion assessment, DOE FPP-class review).
+- Economic analysis for Stellaris — explicitly deferred to future work in the paper
+- Alpha demo preliminary engineering specs (too early; 2031 target)
+- System code output or sensitivity study from Proxima
+- Published conference proceedings (APS-DPP, IAEA FEC) that may contain cost-adjacent content
 
 **Gaps**:
-- Formal power plant economics study for Stellaris — `not-yet-sourced` — **important** (needed for LCOE section; paper-based analogues can substitute)
-- Independent TRL verification — `not-yet-sourced` — **nice-to-have** (self-reported TRL from Proxima/paper is available; cross-check would improve confidence)
+- Full economic/cost study for Stellaris — `not-yet-sourced` — **important** (paper confirms it will be done; conference presentations may exist)
+- Cost estimates or trade studies from ARIES-CS full papers (OSTI abstracts only captured, no full text) — `not-yet-sourced` — **important** (ARIES-CS had detailed costing for compact stellarator)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-
-**Coverage**: Good
+**Coverage**: Partial
 
 **Available**:
-The Stellaris paper provides a strong basis for identifying cost-modeling challenges:
-- **3D non-planar coil geometry**: 50 modular HTS coils with complex winding packs, optimized via SQuID/StarFinder. No tokamak analogue exists for coil cost. The coil complexity (peak coil current 15.4 MA, stored energy 111 GJ) is described in detail — the challenge is translating geometry into cost, not understanding the geometry.
-- **ECRH heating at 230–240 GHz**: 50 MW from 7 gyrotrons per port × 8 ports = 56 gyrotrons. This frequency is at or beyond current industrial capability (W7-X uses 140 GHz). The paper notes this explicitly.
-- **Island divertor**: Physics well-described (4/4 island chain, tungsten-based), but heat exhaust modeling is acknowledged as still maturing. No demonstrated analog at power-plant wall loads (10 MW/m² target stated).
-- **WCLL blanket TBR**: TBR = 1.07 from neutronics modeling. Paper acknowledges this is a point estimate with sensitivity to geometry and enrichment — relevant to tritium self-sufficiency margin.
-- **Cryo-plant load**: 111 MW conduction to coils is stated. This is a significant recirculating power fraction (~11% of thermal output) with cost implications.
-- **Physics extrapolation**: The H₉₈ confinement enhancement factor required is 1.30 — a 30% improvement over the empirical W7-X scaling. This is the main unvalidated physics claim.
+- Physics design point well-established: 2.7 GW fusion, 3.1 GW thermal, ~1 GW net electric
+- Confinement basis (W7-X, ISS04 scaling with H=1.4, validated for W7-X) documented with uncertainty acknowledgment
+- Heating scheme (ECRH, O1/X1 modes, 240 GHz) described with technology gap noted (no 240 GHz MW-class gyrotrons exist)
+- Island divertor: paper explicitly acknowledges it does not scale to power plant ("insufficient neutral gas compression"), leaving the problem open
+- Remote maintenance (sector splitting): conceptualized, no duration estimate or efficiency figure given in the paper
+- Turbulent transport: significant remaining uncertainty acknowledged ("neglects electromagnetic effects and radial electric fields")
 
 **Missing**:
-- No detailed balance-of-plant (BoP) schematic or heat integration analysis. The 1/3 (~32%) thermal conversion efficiency is an assumption, not a cycle study.
-- No detailed remote maintenance (RM) cost/schedule analysis. RM complexity for non-planar 3D coils is expected to be higher than tokamaks but is not quantified.
+- Power balance breakdown (recirculating power not specified in detail for Stellaris)
+- "Conduction power to coils: 111 MW" appears in the parameter table — if correct in unit, it implies an enormous cryogenic parasitic load that would severely affect net electric output. This requires clarification (possible OCR/extraction artifact — stored magnetic energy also listed as 111 GJ)
+- Divertor solution: paper covers initial heat load modeling only; neutral gas compression, pumping, detachment control at power-plant scale left for future work
+- Availability/capacity factor: not stated for Stellaris; maintenance duration for sector splitting not quantified
 
 **Gaps**:
-- Detailed steam/power cycle design and efficiency justification — `derivable` (can use generic stellarator/fusion plant BoP analogues, e.g., ~33% Rankine at 500°C EUROFER limit) — **important**
-- Remote maintenance cost model — `proprietary` / `not-yet-sourced` — **important** (remote maintenance is typically 10–20% of total OpEx in fusion plant studies; lacking it introduces a large uncertainty band)
-- 3D coil manufacturing cost model — `not-yet-sourced` — **important** (no published bottom-up cost model for non-planar HTS stellarator coils; analogue from ITER TF coils or CFS SPARC coils would be indirect)
-- ECRH system cost at 230–240 GHz — `not-yet-sourced` — **important** (current gyrotron cost analogues are at 140 GHz; higher frequency increases unit cost)
+- Recirculating power balance (cryogenics, ECRH, pumping, cooling) — `derivable` from analogy with Helios but uncertain — **blocking** for net electric accuracy
+- Divertor engineering scalability — `truly-unknown` at this stage — **important** (paper itself flags this as open)
+- ECRH at 240 GHz: wall-plug efficiency at this frequency — `not-yet-sourced` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-
 **Coverage**: Partial
 
 **Available**:
-The Stellaris paper and Proxima tech page provide sufficient basis for TRL assessments on most subsystems:
-
-| Subsystem | Basis Available | Implied TRL | Source |
-|-----------|----------------|-------------|--------|
-| QI plasma equilibrium / confinement physics | W7-X experimental validation at small scale | TRL 4–5 (device-scale demo, scaling unverified) | Stellaris paper §2 |
-| Island divertor | W7-AS and W7-X demonstrated, power-plant loads not tested | TRL 4 | Tech page, paper §3 |
-| HTS REBCO coils (20 T, stellarator geometry) | REBCO tape commercially available; 3D stellarator winding at scale not demonstrated | TRL 2–3 | Dossier, paper §4 |
-| ECRH at 230–240 GHz | W7-X runs at 140 GHz; 230 GHz systems in lab only | TRL 2–3 | Stellaris paper §5 |
-| WCLL blanket | EUROfusion DEMO-class design work; not yet prototyped for stellarator geometry | TRL 2–3 | Stellaris paper §6 |
-| Tungsten first wall | Demonstrated on JET, W7-X; power-plant lifetimes not validated | TRL 4–5 | Stellaris paper §3 |
-| Cryogenic pellet injection | Operational on W7-X; power-plant rep-rate not qualified | TRL 4 | Stellaris paper §5 |
-| EUROFER97 structure | Irradiation data available; power-plant fluence regime (>20 dpa) not yet qualified | TRL 4 | Stellaris paper §6 |
+- **Plasma physics** (TRL ~3-4): W7-X confirms neoclassical optimization at experiment scale. Turbulent transport at reactor densities/temperatures: modeled but not demonstrated. Ignited plasma in QI geometry: never demonstrated.
+- **HTS coils** (TRL ~3): REBCO at 20T demonstrated in large-bore coils (MIT, 20.1 T confirmed). 3D non-planar HTS coil manufacturing: SMC demo planned 2027, not yet realized. W7-X used NbTi (not scalable to 20T).
+- **WCLL blanket** (TRL ~4-5): EU-DEMO heritage. Li-6 enrichment and PbLi handling established. Adapted to stellarator geometry: conceptualized but not validated. TBR 1.07 achieved in homogenized neutronic model.
+- **ECRH at 240 GHz** (TRL ~2-3): W7-X uses 140 GHz (up to 1.5 MW/tube), ITER will use 170 GHz. 240 GHz MW-class gyrotrons: do not exist; active R&D required.
+- **Remote maintenance / sector splitting** (TRL ~2): Conceptualized in paper, CAD-verified for clash-free extraction, but no hardware demonstration. No maintenance duration estimate given.
+- **First wall** (EUROFER97, TRL ~5): EU-DEMO qualified material. Peak DPA: 11/FPY in hot spots, 6/FPY average. Lifetime ~few FPY.
+- **Magnet lifetime** (TRL ~3): ~10 full-power years based on REBCO neutron fluence limit extrapolated from fission irradiation data; uncertainty ×2-3.
 
 **Missing**:
-- No explicit TRL table appears in the Stellaris paper — TRL assessments above are inferred from the technical descriptions and the W7-X/DEMO literature heritage.
-- No magnet factory production rate or per-coil cost estimate is available.
+- TRL assessment for each subsystem (only inferred from paper context)
+- Divertor at reactor-relevant conditions: TRL ~2 for power-plant stellarator divertor
+- First wall lifetime and replacement strategy: acknowledged but not quantified for scheduling
 
 **Gaps**:
-- Explicit TRL table for Stellaris subsystems — `not-yet-sourced` — **nice-to-have** (EUROfusion fusion plant roadmaps and W7-X companion papers may have TRL assessments for overlapping subsystems; unverified — confirm existence before searching)
-- 3D HTS coil winding demonstration at scale — `truly-unknown` (no one has wound a non-planar 20T HTS coil at power-plant current; this is a genuine TRL gap) — **blocking** for the technology, **important** for the analysis (flag as major risk)
+- Gyrotron development at 240 GHz — `not-yet-sourced` (R&D roadmaps may exist in IEEE or Nucl. Fusion literature) — **important**
+- REBCO tape irradiation tolerance: data from fission reactors; fusion neutron spectrum extrapolation uncertain — `not-yet-sourced` — **important**
+- Divertor TRL and development path — `truly-unknown` (acknowledged open problem) — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-
 **Coverage**: Partial
 
 **Available**:
-- **REBCO HTS tape**: Named explicitly as the conductor (20 T capable). Dossier notes REBCO supply chain risk (single-sourcing concern). Global REBCO production is dominated by a small number of manufacturers (SuperPower, SUNAM, SuNAM, Fujikura). The Stellaris paper does not quantify tape length or cost per meter.
-- **EUROFER97**: Structural material for blanket and vessel. European supply chain exists (Böhler/Uddeholms); used in JET and DEMO design studies. Production scale for a power plant is not quantified.
-- **Tungsten**: First wall and divertor armor. Established industrial supply; primary concern is manufacturing to power-plant specifications (plasma-facing surface quality, bonding to structural steel). Sources note W7-X demonstrated tungsten components.
-- **LiPb (lithium-lead eutectic)**: Blanket coolant and tritium breeder. Lithium enrichment (Li-6) required. Global Li-6 production is modest; enrichment is a non-trivial industrial step.
-- **Tritium startup inventory**: D-T fuel requires ~1–2 kg tritium startup charge (from Helios comparison source; Stellaris paper does not state this explicitly). Current global tritium inventory (~25 kg) is limited.
+- **REBCO tape**: Faraday Factory Japan MoU for SMC demo quantity. Full Stellaris would require massive scale-up (50 modular coils at 20T, major radius 12.7 m). No cost/volume estimate for commercial quantities.
+- **Li-6 enrichment**: Standard fusion challenge. 6Li enrichment to ~natural or 30% for WCLL (Stellaris uses WCLL; Helios uses 65% enrichment). Supply chain exists (Russia/China dominate enrichment).
+- **EUROFER97**: EU-qualified RAFM steel. Manufacturing capacity adequate for DEMO-scale; commercial fusion scale uncertain.
+- **Pb-Li (PbLi eutectic)**: Abundant; infrastructure underdeveloped at fusion scale.
+- **Tungsten** (divertor plates): Standard industrial material; plasma-facing qualification at power-plant fluence is a challenge.
+- **SiC flow channel inserts**: Noted as required for MHD pressure management in PbLi flow; manufacturing readiness unclear.
 
 **Missing**:
-- No supply chain risk quantification (cost, lead time, single-point-of-failure analysis) in any source.
-- No REBCO tape length/quantity estimate for Stellaris (needed to assess supply chain feasibility).
-- No Li-6 enrichment requirement calculation specific to Stellaris TBR = 1.07.
+- REBCO tape cost projection at commercial volumes
+- Manufacturing bottleneck analysis for 3D non-planar HTS coils (most critical supply chain item)
+- Li-6 supply chain geopolitical risk assessment
+- SiC flow channel insert industrial readiness
 
 **Gaps**:
-- REBCO tape quantity estimate for Stellaris coils — `derivable` (can estimate from coil geometry and current density specs in the paper) — **important**
-- REBCO production capacity vs. demand timeline — `not-yet-sourced` — **important** (IEA/DOE reports on critical mineral supply chains or published stellarator supply chain studies; unverified — confirm existence before searching)
-- Li-6 enrichment requirements and supply chain — `not-yet-sourced` — **important** (EUROfusion WCLL blanket studies address this; unverified — confirm existence before searching)
-- Tritium startup inventory source and cost — `not-yet-sourced` — **important** (CANDU-sourced tritium at ~$30k/g is the standard assumption; confirm applicability)
+- 3D non-planar HTS coil manufacturing supply chain — `not-yet-sourced` (some literature on REBCO tape production forecasts exists; ARPA-E reports on HTS manufacturing) — **important**
+- REBCO cost trajectory at GW-scale deployment — `not-yet-sourced` — **important**
+- 240 GHz gyrotron supply chain — `truly-unknown` at MW scale — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Peak fusion power | 2.7 GW | Stellaris paper Table 2 | High |
-| Peak thermal power | 3.1–3.3 GW | Stellaris paper | High |
-| Net electrical output | ~1 GW | Stellaris paper / dossier | Medium |
-| Thermal conversion efficiency | ~32% (stated as "1/3") | Stellaris paper §7 | Medium (assumed, not cycle-modeled) |
-| Auxiliary power — ECRH | 50 MW | Stellaris paper Table 2 | High |
-| Recirculating power — cryo | 111 MW | Stellaris paper Table 2 | High |
-| Plasma major radius | 12.7 m | Stellaris paper Table 2 | High |
-| Plasma minor radius | 1.5 m | Stellaris paper Table 2 | High |
-| Number of modular coils | 50 | Stellaris paper | High |
-| Peak coil field | 14.4 T (on-axis) / 20 T (at conductor) | Stellaris paper | High |
-| Stored magnetic energy | 111 GJ | Stellaris paper Table 2 | High |
-| Blanket TBR | 1.07 | Stellaris paper §6 | Medium |
-| Peak wall load | 4.05 MW/m² | Stellaris paper Table 2 | High |
-| Confinement gain (Q) | ~4–6 (fusion power / auxiliary power) | Stellaris paper (derived) | Medium |
-| H₉₈ confinement factor required | 1.30 | Stellaris paper §2 | Medium (unvalidated extrapolation) |
-| Alpha demo cost | ~€2B | Proxima/RWE MoU 2026 | Medium (announcement, not engineering estimate) |
-| ECRH system size | 56 gyrotrons × 1 MW each | Stellaris paper §5 | High |
-| Plasma volume | 448 m³ | Stellaris paper Table 2 | High |
-| Operation mode | Steady-state | Dossier / Stellaris paper | High |
-| Fuel type | D-T | Dossier | High |
+| Peak fusion power | 2,700 MW | Stellaris paper (Table 2) | h |
+| Total thermal power | ~3,100–3,300 MW | Stellaris paper | h |
+| Net electric output | ~1,000 MW | Stellaris paper (Table 2) | h |
+| Net-to-thermal efficiency (implied) | ~32% | Derived: 1000/3150 | m |
+| ECRH startup power | 50 MW | Stellaris paper (Table 2) | h |
+| ECRH ignited power | ~1 MW (inferred) | Inferred from Helios analog (1 MW ECRH in ignited state) | m |
+| Blanket power multiplier | 1.2 | Stellaris paper (neutronics) | h |
+| TBR (WCLL) | 1.07 | Stellaris paper (neutronics) | h |
+| Magnet lifetime | ~10 FPY (neutron fluence) | Stellaris paper (shielding section) | m |
+| First wall avg DPA rate | 6 DPA/FPY | Stellaris paper | h |
+| Maintenance strategy | Sector splitting | Stellaris paper | h |
+| First wall replacement interval | 4–6 years | Stellaris paper (Section 3.1) | m |
+| Fuel type | D-T | Dossier | h |
+| Thermal conversion (Helios analog) | ~40% gross Rankine | Helios paper | m |
+| Capacity factor (Helios analog) | ~88% (84-day outage/2yr) | Helios paper | m |
+| Overnight capital range (fleet-wide) | 1–10 $/W | Stellaris paper intro (refs [10-13]) | l |
+| LCOE range (fleet-wide D-T MFE) | $140–550/MWh (FOAK) | `tea_dt_mfe_cost_analysis/` | l |
+| Alpha demo cost | ~EUR 2B | Proxima MoU press release | h |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capacity factor (%) | derivable | Blocking | Steady-state operation claimed; no explicit CF stated. Can assume 85–90% with stated basis; needs flagging. |
-| CapEx breakdown by subsystem (magnets, blanket, vessel, BoP) | proprietary / not-yet-sourced | Blocking | No cost breakdown in any source. Alpha demo = €2B covers demo-scale. Power plant CapEx must be estimated from analogues ($/W literature ranges: 2–10 $/W for fusion). |
-| Blanket replacement schedule and cost | not-yet-sourced | Important | WCLL blanket lifetime under stellarator neutron flux not quantified. EUROfusion DEMO studies have blanket replacement intervals (~2–5 years); adapt with stated assumptions. |
-| First wall replacement cost | not-yet-sourced | Important | Tungsten first wall lifetime under 4 MW/m² load not stated. Analogues from tokamak studies needed. |
-| O&M staffing cost | truly-unknown | Important | No fusion power plant has operated at scale; all estimates are analogy-based. |
-| Tritium inventory and cost | not-yet-sourced | Important | ~1–2 kg startup from Helios source, not stated in Stellaris paper. Cost ~$30k/g → $30–60M startup inventory. |
-| ECRH system capital cost | not-yet-sourced | Important | 56 × 1 MW gyrotrons at 230–240 GHz. Cost per unit at this frequency not in sources; W7-X gyrotron analogues at 140 GHz available in literature. |
-| Thermal cycle details (sCO₂ vs Rankine, efficiency breakdown) | derivable | Important | "1/3 efficiency" is stated. EUROFER97 limit ~500°C constrains cycle to ~33–35% Rankine. Can derive with stated assumptions. |
-| Remote maintenance cost and schedule | proprietary | Important | Not published. Analogue: tokamak RM cost studies (e.g., ARIES, DEMO). |
-| Decommissioning cost | truly-unknown | Nice-to-have | Standard fusion plant assumption (~10–15% of overnight capital) can be applied. |
-| HTS coil manufacturing cost per coil | not-yet-sourced | Important | REBCO tape cost ~$10–50/m; coil geometry in paper allows tape-length estimate. Total magnet cost derivable with assumptions. |
-| Land/site cost | proprietary | Nice-to-have | Gundremmingen stated as site; decommissioned nuclear site may have infrastructure value. |
+| Capital cost by subsystem (coils, blanket, vessel, BOP) | proprietary / not-yet-published | blocking | Stellaris paper explicitly defers; ARIES-CS analogue (not fully ingested) could partially fill |
+| O&M cost (annual) | not-yet-sourced | blocking | No fusion stellarator O&M data available publicly for this class |
+| Cryogenic recirculating power | derivable (with caution) | blocking | Table lists 111 MW to coils but unit/value uncertain; Helios uses ~10 MW for 40 kW at 20K |
+| Capacity factor (Stellaris-specific) | derivable | important | Use Helios 88% as analog; Stellaris cites longer replacement intervals (4-6 yr vs 2 yr for Helios) → possibly higher CF |
+| Blanket/first wall replacement cost | not-yet-sourced | important | Major O&M driver for high-neutron-flux stellarators |
+| Magnet replacement cost (if 10 FPY lifetime) | not-yet-sourced | important | Potentially dominant lifecycle cost |
+| ECRH system capital cost at 240 GHz | not-yet-sourced | important | Novel frequency; no commercial precedent |
+| Confinement enhancement factor risk | derivable | important | H=1.4 assumed (achieved in W7-X); uncertainty propagates to fusion power |
+| Scaling to lower aspect ratio (economic optimum) | not-yet-sourced | nice-to-have | Paper mentions lower AR reduces capital cost but reduces power |
 
 ---
 
 ## Source Recommendations
 
-1. **EUROfusion DEMO WCLL blanket design studies** — addresses blanket replacement schedule, TBR sensitivity, and Li-6 enrichment requirements. Search: OSTI/EUROfusion publications on "WCLL blanket lifetime" or "WCLL replacement interval." — `not-yet-sourced` — unverified, confirm existence before searching.
+1. **ARIES-CS full papers** (Lyon et al. 2008, FST Vol. 54, OSTI:1014258 — abstract only captured): These contain the most directly applicable stellarator cost breakdown — same compact stellarator class, using ARIES CAS costing. Search OSTI or FST archives. — `not-yet-sourced`, **high priority**
 
-2. **ARIES-CS or HSR stellarator power plant studies** — published system-level cost models for compact stellarator power plants that predate Stellaris but establish parametric cost structures (magnets, blanket, BoP). Search: "ARIES Compact Stellarator" or "Helias Reactor HSR" cost study. — `not-yet-sourced` — ARIES-CS is a known publication (Raffray et al., ~2008); confirm the HSR study exists before citing.
+2. **HELIAS reactor study series** (cited as refs [55–60] in Stellaris paper): EUROfusion's HTS stellarator reactor studies. May contain cost estimates from 2010s that can be updated. Search ARIES/EUROfusion document archives. — `not-yet-sourced`, **high priority**
 
-3. **CFS/SPARC magnet cost analogues** — REBCO HTS magnet cost modeling for high-field fusion magnets. CFS has published engineering cost information on SPARC's TF coils. Applicable as analogue for Stellaris coil cost estimation. — `not-yet-sourced` — unverified, confirm existence before searching.
+3. **Proxima conference presentations** (APS-DPP 2024-2025, IAEA FEC 2024): Companies sometimes present pre-commercial cost estimates at conferences before formal publication. Search APS-DPP abstract database and IAEA INIS. — `not-yet-sourced`, **medium priority** — *unverified — confirm existence before searching*
 
-4. **W7-X companion engineering papers** — detailed cost breakdown for W7-X construction (total ~1B EUR for experimental device). Provides bottom-up magnet manufacturing cost data at relevant scale (though at 2.5 T, not 20 T). Search: "W7-X construction cost" or "Wendelstein 7-X magnet fabrication." — `not-yet-sourced` — unverified, confirm existence before searching.
+4. **PyFECONS** (`/home/reid/PyFECONS`): Contains ARIES-CS costing algorithms implementable for compact stellarators. Can be used to derive capital cost analogues by parameterizing with Stellaris dimensions. — `derivable`, **high utility**
 
-5. **Gyrotron cost literature at high frequency** — 140 GHz unit costs are well-documented (W7-X: ~€3–5M per 1 MW gyrotron); 230 GHz is at developmental stage. Search: "high-frequency gyrotron cost" or "ECRH system cost fusion." — `not-yet-sourced` — unverified, confirm existence before searching.
+5. **REBCO tape cost forecasts**: ARPA-E funded studies on HTS manufacturing cost trajectories. Search OSTI for "REBCO manufacturing cost" or "HTS tape cost reduction roadmap." — `not-yet-sourced` — *unverified — confirm existence before searching*
 
-6. **IEA/DOE critical mineral supply chain reports on REBCO tape** — quantify production bottleneck for HTS tape scale-up. Search: "REBCO supply chain fusion" or "HTS tape production capacity roadmap." — `not-yet-sourced` — unverified, confirm existence before searching.
+6. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): While targeting MIF and other concepts rather than stellarators, the costing methodology (CAS-based, 500 MWe plants) is directly applicable as a cross-concept methodology anchor. Fleet-wide source already registered — **check for stellarator-applicable parameters**.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with caveats noted.**
+Proceed to full analysis with the following posture: the physics and engineering basis is **strong enough to support D1+ qualitative analysis** and a **preliminary quantitative LCOE model using analogues and ranges**. The Stellaris paper provides fusion power, thermal power, net electric output, TBR, magnet lifetime, and first wall DPA rates. The Helios paper (Thea Energy) supplies the most direct stellarator plant economics analog: 40% Rankine efficiency, 88% capacity factor, power balance Sankey, cryogenic loads. The TEA D-T MFE source provides the LCOE methodology and early-plant range ($140–550/MWh).
 
-The Stellaris paper is one of the most detailed pre-commercial fusion power plant design studies available in the public literature — unusually so. Physics parameters, engineering geometry, materials, and subsystem descriptions are documented at a level that fully supports qualitative write-up and parametric LCOE modeling. The concept is well-characterized enough that most missing parameters are `derivable` or can be filled with `not-yet-sourced` analogues rather than being truly unknown.
+**The analysis should not attempt to produce a single LCOE number without wide uncertainty bounds.** The most productive approach is a parametric model with capital cost and O&M as free parameters swept over fusion-literature ranges, sensitivity-tested against capacity factor and magnet lifetime. The $0.01/kWh back-solve will reveal that this concept is not close under any credible parameter set — identifying which costs must fall and by how much is the analytically useful output.
 
-The main caveats to flag in the analysis are: (1) CapEx must be estimated from literature analogue ranges (2–10 $/W), not from a bottom-up Stellaris-specific cost model; (2) the 32% thermal efficiency is an assumption constrained by EUROFER97 temperature limits, not a detailed cycle study; (3) H₉₈ = 1.30 is the critical unvalidated physics assumption — if confinement falls short, Q and power output drop sharply; (4) 3D HTS coil manufacturing at power-plant scale has no demonstrated precedent and represents the single highest-risk TRL gap. These uncertainties can all be surfaced and parameterized in the LCOE model rather than treated as blockers.
+**Before acquiring additional sources**, ingest the ARIES-CS full text (Lyon et al. 2008, FST) and check PyFECONS for stellarator costing algorithms — these are the two highest-leverage actions.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 2
+blocking_count: 3
 important_count: 8
-counting_method: "section_5_missing_parameters"
+counting_method: "section_5_missing_parameters (blocking: capital cost breakdown, O&M cost, cryogenic recirculating power) plus cross-section important gaps (divertor scalability, ECRH at 240 GHz, magnet replacement cost, blanket replacement cost, REBCO supply chain, CF derivable-only, confinement H-factor risk)"
 section_coverage:
-  availability_of_data:       "Good"
-  system_function:            "Good"
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
