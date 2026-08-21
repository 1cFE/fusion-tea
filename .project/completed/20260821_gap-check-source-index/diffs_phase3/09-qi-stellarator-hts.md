# Phase 3 diff: 09-qi-stellarator-hts

**Generated:** 2026-05-22T13:55:06-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 3 | 2 | -1 |
| important_count  | 8 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information to write the gap assessment report.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information to write the gap assessment report.
```

## Blocking-tier lines (new)

```
28:- No concept-specific economic or plant study — proprietary — **blocking** (LCOE quantitative model cannot be concept-specific)
140:| Capital cost by subsystem (magnets, blanket, BOP, structures) | proprietary | blocking | No Stellaris-specific estimate; Proxima explicitly defers economic analysis; 3D coil set has no cost analog |
141:| 3D HTS stellarator coil cost | not-yet-sourced | blocking | 50 non-planar REBCO coils ~25 m circumference each; no published $/kA-m at this complexity; planar Helios coils are structurally different |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/09-qi-stellarator-hts.md	2026-05-22 12:59:21.063237128 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/gap_report.md	2026-05-22 13:55:06.223469872 -0700
@@ -1,62 +1,58 @@
-I now have enough information to write the comprehensive gap assessment. Let me compile it.
-
----
+I now have sufficient information to write the gap assessment report.
 
 # Gap Assessment: QI Stellarator - HTS (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The Proxima Fusion Stellaris paper (FED 2025, full text available) provides exceptionally detailed physics and engineering coverage — the most comprehensive publicly available reactor study for this concept. The primary gap is economic: the paper explicitly declares cost modeling "outside the scope" and lists it as future work. No capital cost breakdown, O&M estimate, or capacity factor figure is available from Proxima directly. These gaps are partially bridgeable via the Helios stellarator analog (Thea Energy, comparable HTS QI design, 390 MWe) and the fleet-wide TEA D-T MFE cost study (`knowledge/sources/tea_dt_mfe_cost_analysis/`), but Stellaris-specific cost structure remains unquantified.
+**Summary**: The Stellaris paper (FED 2025, full text extracted) provides exceptional coverage of physics and engineering — the richest conceptual design data in the current portfolio for any private fusion company. Physics and subsystem function are well characterized for a concept at this stage. The core gap for LCOE analysis is that Proxima explicitly defers all economic analysis to future work; no concept-specific capital cost estimate exists for any Stellaris subsystem, and the only cost figures in the paper are generic MFE literature ranges (1–10 $/W overnight, 20–100 $/MWh LCOE). An analog-based quantitative LCOE model is feasible using Helios, ARIES-CS, and TEA-MIT framework data, but a bottom-up Stellaris-specific estimate is not currently possible.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Moderate
 
 **Available**:
-- Full Stellaris paper (FED 214 (2025) 114868, 337 KB extracted, open-access CC BY-NC) — covers plasma physics, magnets, blanket, first wall, divertor, support structure, remote maintenance
-- Proxima technology page and press releases — company direction, magnet development milestones, Alpha demo timeline (EUR 2B, 2031, Q>1)
-- Helios stellarator paper (Thea Energy, arXiv 2512.08027, 176 KB extracted) — comparable QA HTS stellarator, closer to complete plant-level analysis including power balance Sankey diagram
-- WendelsteinW7-X background (Wikipedia, W7-X construction paper) — physics heritage
-- Physics papers (CIEMAT-QI4, arxiv-2404-16440) — turbulent transport basis
-- TEA D-T MFE fleet-wide source — LCOE framework for D-T MFE plants
+- **Full Stellaris paper** (Lion et al., FED 2025, `iter-01/sources/stellaris-design-details.md`): 30+ page peer-reviewed design study covering plasma optimization, heating, blanket, magnets, support structure, remote maintenance, and neutronics. Includes all key plasma and machine parameters (Table 1: R=12.7 m, a=1.5 m, B_axis=5.86 T, B_coil=14.4 T, 2700 MW fusion, ~1000 MW net electric, TBR 1.074).
+- **Proxima company communications**: Technology page, tritium blog, Faraday Factory Japan REBCO agreement, RWE/Bavaria/IPP MoU (Alpha €2B, Gundremmingen site for Stellaris).
+- **Helios stellarator comparison** (`iter-02/sources/helios-stellarator-comparison.md`, arXiv 2512.08027): Thea Energy's preconceptual stellarator plant study — the closest analog in concept family. Provides 390 MWe, 40% thermal efficiency, steam Rankine cycle, 88% capacity factor, biennial 84-day maintenance, 20 T HTS, TBR 1.3.
+- **W7-X physics heritage**: Wikipedia article and SOFE 2009 construction paper provide validated QI stellarator physics basis; W7-X demonstrated neoclassical transport reduction and detachment operation.
+- **Physics literature**: CIEMAT-QI4 turbulence paper (arXiv 2404.16440), Goodman et al. 2024 (arXiv 2405.19860), CIEMAT-QI4X (arXiv 2512.08825) confirm QI optimization advances that underpin Stellaris.
 
 **Missing**:
-- Economic analysis for Stellaris — explicitly deferred to future work in the paper
-- Alpha demo preliminary engineering specs (too early; 2031 target)
-- System code output or sensitivity study from Proxima
-- Published conference proceedings (APS-DPP, IAEA FEC) that may contain cost-adjacent content
+- No Stellaris-specific economic study, capital cost estimate, or LCOE calculation. The Stellaris paper explicitly lists "in-depth studies of economic viability" as future work (`iter-01/sources/stellaris-design-details.md`, §3.2). The only cost numbers in the paper cite generic MFE literature (1–10 $/W; 20–100 $/MWh).
+- No published Alpha demo cost breakdown (only the €2B headline figure from the MoU press release).
 
 **Gaps**:
-- Full economic/cost study for Stellaris — `not-yet-sourced` — **important** (paper confirms it will be done; conference presentations may exist)
-- Cost estimates or trade studies from ARIES-CS full papers (OSTI abstracts only captured, no full text) — `not-yet-sourced` — **important** (ARIES-CS had detailed costing for compact stellarator)
+- No concept-specific economic or plant study — proprietary — **blocking** (LCOE quantitative model cannot be concept-specific)
+- Alpha demo physics validation (Q>1) not yet demonstrated — truly-unknown — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Physics design point well-established: 2.7 GW fusion, 3.1 GW thermal, ~1 GW net electric
-- Confinement basis (W7-X, ISS04 scaling with H=1.4, validated for W7-X) documented with uncertainty acknowledgment
-- Heating scheme (ECRH, O1/X1 modes, 240 GHz) described with technology gap noted (no 240 GHz MW-class gyrotrons exist)
-- Island divertor: paper explicitly acknowledges it does not scale to power plant ("insufficient neutral gas compression"), leaving the problem open
-- Remote maintenance (sector splitting): conceptualized, no duration estimate or efficiency figure given in the paper
-- Turbulent transport: significant remaining uncertainty acknowledged ("neglects electromagnetic effects and radial electric fields")
+The Stellaris paper addresses all major system function challenges with unusual completeness for a private company design study:
+- **Physics performance**: 0.5D power balance analysis, GENE+TANGO turbulence validation of temperature profiles. Two operating points (A: 1800→2700 MW, B: higher density) analyzed. Design point requires ISS04 confinement multiplier of 1.0 — no enhancement assumed.
+- **Heating**: ECRH (50 MW, 230–240 GHz) confirmed as primary method with port design validated for O1/X1 mode heating (`iter-01/sources/stellaris-design-details.md`, §2.5). Wall-plug efficiency issue acknowledged (gyrotron ~50%, multi-stage depressed collector target >60%).
+- **Divertor**: Island divertor validated for heat capture with EMC3-Lite simulations; 97–99% of SOL power captured under strong detachment assumption; peak heat flux 5–9.5 MW/m² depending on edge transport parameters (`iter-01/sources/stellaris-design-details.md`, §2.6).
+- **Power balance**: 3150 MW thermal with power multiplication 1.2 from WCLL blanket; 50 MW ECRH recirculating load included; ~1000 MW net electric implies ~32% overall efficiency.
+- **Steady-state operation**: Island divertor detachment control (following W7-X heritage), density profile control via pellet injection, minimal bootstrap current (23 kA — negligible for island location stability).
+- **Burn control**: Novel challenge noted — no demonstrated burn control scenario for stellarators; authors suggest density/temperature control via ECCD or coil detuning.
 
 **Missing**:
-- Power balance breakdown (recirculating power not specified in detail for Stellaris)
-- "Conduction power to coils: 111 MW" appears in the parameter table — if correct in unit, it implies an enormous cryogenic parasitic load that would severely affect net electric output. This requires clarification (possible OCR/extraction artifact — stored magnetic energy also listed as 111 GJ)
-- Divertor solution: paper covers initial heat load modeling only; neutral gas compression, pumping, detachment control at power-plant scale left for future work
-- Availability/capacity factor: not stated for Stellaris; maintenance duration for sector splitting not quantified
+- Island divertor operation at reactor-relevant power (500 MW SOL exhaust after 90% radiation) not demonstrated at any scale; all W7-X data at <5 MW.
+- Burn control at ignition-level conditions is conceptually described but not supported by experimental data from stellarators.
+- Gyrotron efficiency at 240 GHz: highest demonstrated is ~170 GHz (W7-X); the Stellaris paper acknowledges 240 GHz gyrotrons are required but "future work" for development.
+- High-confinement mode (H-mode) access: The paper notes Stellaris's P/S ratio (~1.18 MW/m²) exceeds H-mode threshold for tokamaks and may require confinement correction — introduces downward uncertainty in plasma performance.
 
 **Gaps**:
-- Recirculating power balance (cryogenics, ECRH, pumping, cooling) — `derivable` from analogy with Helios but uncertain — **blocking** for net electric accuracy
-- Divertor engineering scalability — `truly-unknown` at this stage — **important** (paper itself flags this as open)
-- ECRH at 240 GHz: wall-plug efficiency at this frequency — `not-yet-sourced` — **important**
+- Island divertor at reactor-scale power flux — truly-unknown — **important**
+- Burn control and thermal stability at ignition-level conditions in QI stellarators — truly-unknown — **important**
+- 240 GHz high-power gyrotron capability at MW-scale (required for ECRH) — not-yet-sourced — **important**
+- H-mode confinement correction to design point unknown — truly-unknown — **nice-to-have** (could alter Q and required heating power)
 
 ---
 
@@ -64,23 +60,29 @@
 **Coverage**: Partial
 
 **Available**:
-- **Plasma physics** (TRL ~3-4): W7-X confirms neoclassical optimization at experiment scale. Turbulent transport at reactor densities/temperatures: modeled but not demonstrated. Ignited plasma in QI geometry: never demonstrated.
-- **HTS coils** (TRL ~3): REBCO at 20T demonstrated in large-bore coils (MIT, 20.1 T confirmed). 3D non-planar HTS coil manufacturing: SMC demo planned 2027, not yet realized. W7-X used NbTi (not scalable to 20T).
-- **WCLL blanket** (TRL ~4-5): EU-DEMO heritage. Li-6 enrichment and PbLi handling established. Adapted to stellarator geometry: conceptualized but not validated. TBR 1.07 achieved in homogenized neutronic model.
-- **ECRH at 240 GHz** (TRL ~2-3): W7-X uses 140 GHz (up to 1.5 MW/tube), ITER will use 170 GHz. 240 GHz MW-class gyrotrons: do not exist; active R&D required.
-- **Remote maintenance / sector splitting** (TRL ~2): Conceptualized in paper, CAD-verified for clash-free extraction, but no hardware demonstration. No maintenance duration estimate given.
-- **First wall** (EUROFER97, TRL ~5): EU-DEMO qualified material. Peak DPA: 11/FPY in hot spots, 6/FPY average. Lifetime ~few FPY.
-- **Magnet lifetime** (TRL ~3): ~10 full-power years based on REBCO neutron fluence limit extrapolated from fission irradiation data; uncertainty ×2-3.
+| Subsystem | TRL Assessment | Source |
+|-----------|---------------|--------|
+| Plasma physics basis | TRL 4–5 (W7-X demonstrates QI neoclassical optimization) | W7-X Wikipedia; Stellaris paper §2.2 |
+| ECRH gyrotrons (140–170 GHz) | TRL 7–8 (operational in W7-X, ITER-class) | Stellaris paper §2.5 |
+| WCLL blanket concept | TRL 4 (EU DEMO program; same concept, tokamak geometry) | Stellaris paper §2.8; dossier |
+| EUROFER97 structural steel | TRL 6 (EU DEMO development, not fully irradiation-qualified) | Stellaris paper §2.8 |
+| HTS REBCO conductor (tape form) | TRL 5–6 (45.5 T record achieved; SPARC under construction) | Stellaris paper §2.9 |
+| 3D non-planar HTS stellarator coils | TRL 2–3 (no reactor-scale 3D REBCO coil; SMC demo planned 2027) | Dossier; Stellaris paper §2.9 |
+| Island divertor (W7-X scale) | TRL 5 (demonstrated in W7-X; detachment operation shown) | Stellaris paper §2.6 |
+| Sector-splitting remote maintenance | TRL 2–3 (conceptualized; not demonstrated for stellarator scale) | Stellaris paper §2.11 |
+| Tritium breeding (WCLL concept) | TRL 4 (EU DEMO, not stellarator-geometry validated) | Stellaris paper §2.8 |
 
 **Missing**:
-- TRL assessment for each subsystem (only inferred from paper context)
-- Divertor at reactor-relevant conditions: TRL ~2 for power-plant stellarator divertor
-- First wall lifetime and replacement strategy: acknowledged but not quantified for scheduling
+- 240 GHz gyrotrons at MW-scale are not demonstrated (required specifically for Stellaris field strength). W7-X gyrotrons operate at 140 GHz; ITER at 170 GHz; next generation needed.
+- 3D non-planar REBCO coil manufacturing at reactor scale: SMC demo targeting 2027 is the critical de-risking step; current TRL is estimated at 2–3 (design but no hardware demonstration). Five-fold difference in coil complexity from tokamak TF coils; W7-AS and W7-X used NbTi, not REBCO.
+- WCLL blanket adapted to complex stellarator geometry: EU DEMO heritage exists for uniform tokamak geometry; non-uniform stellarator radial build (0.95–1.37 m plasma-coil distance) creates heterogeneous neutron shielding demands not covered by available data.
+- First wall irradiation qualification at 14.1 MeV neutron fluence: IFMIF-DONES data expected ~2030s; Stellaris analysis uses ARC-DPA estimates with acknowledged uncertainties.
 
 **Gaps**:
-- Gyrotron development at 240 GHz — `not-yet-sourced` (R&D roadmaps may exist in IEEE or Nucl. Fusion literature) — **important**
-- REBCO tape irradiation tolerance: data from fission reactors; fusion neutron spectrum extrapolation uncertain — `not-yet-sourced` — **important**
-- Divertor TRL and development path — `truly-unknown` (acknowledged open problem) — **important**
+- 3D non-planar HTS coil manufacturing at reactor scale — not-yet-sourced — **important**
+- WCLL blanket TRL in stellarator geometry — not-yet-sourced — **important**
+- 240 GHz high-power gyrotron TRL (same gap as §2) — not-yet-sourced — **important**
+- First wall neutron irradiation qualification data — truly-unknown — **nice-to-have** (IFMIF expected 2030s)
 
 ---
 
@@ -88,89 +90,90 @@
 **Coverage**: Partial
 
 **Available**:
-- **REBCO tape**: Faraday Factory Japan MoU for SMC demo quantity. Full Stellaris would require massive scale-up (50 modular coils at 20T, major radius 12.7 m). No cost/volume estimate for commercial quantities.
-- **Li-6 enrichment**: Standard fusion challenge. 6Li enrichment to ~natural or 30% for WCLL (Stellaris uses WCLL; Helios uses 65% enrichment). Supply chain exists (Russia/China dominate enrichment).
-- **EUROFER97**: EU-qualified RAFM steel. Manufacturing capacity adequate for DEMO-scale; commercial fusion scale uncertain.
-- **Pb-Li (PbLi eutectic)**: Abundant; infrastructure underdeveloped at fusion scale.
-- **Tungsten** (divertor plates): Standard industrial material; plasma-facing qualification at power-plant fluence is a challenge.
-- **SiC flow channel inserts**: Noted as required for MHD pressure management in PbLi flow; manufacturing readiness unclear.
+- **REBCO tape supply**: Faraday Factory Japan signed agreement to supply HTS tape for the SMC demo magnet. Proxima states the SMC uses REBCO from this supplier. Supply chain for demo-scale coil is established.
+- **EUROFER97 structural steel**: Standard EU DEMO material, established supplier base in Europe.
+- **Lithium-lead (LiPb) breeding material**: Lead and lithium abundantly available. Li-6 enrichment is standard industry practice (global supply chain exists for ITER and other programs).
+- **Tungsten first-wall armor**: Established supply chain (W7-X and ITER use tungsten plasma-facing components).
+- **Cryogenic helium** (20 K operation): 20 K vs. LTS 4 K increases efficiency of cryo-plant and uses neon/helium cooling; supply chain more flexible than LTS.
+- **Proxima's magnet factory**: Planned with up to 1,000 jobs (Bavarian High-Tech Agenda); explicitly identified as necessary for Stellaris scale-up.
 
 **Missing**:
-- REBCO tape cost projection at commercial volumes
-- Manufacturing bottleneck analysis for 3D non-planar HTS coils (most critical supply chain item)
-- Li-6 supply chain geopolitical risk assessment
-- SiC flow channel insert industrial readiness
+- **REBCO tape quantity estimate for Stellaris**: 50 coils × ~25 m circumference = ~1,250 m total coil circumference; winding pack with ~300 turns per coil suggests hundreds of km of REBCO tape. No cost-per-kA-m estimate or total tape quantity published. At commercial HTS prices (~$10–100/kA-m depending on volume and performance), this is a potentially dominant capital cost item.
+- **3D coil manufacturing supply chain**: Non-planar stellarator coils require fundamentally different manufacturing than tokamak TF coils. No established industrial supply chain exists for complex 3D REBCO coils; W7-X NbTi coils cost ~€300M for the full coil set (50 coils; ~€6M per coil in NbTi — REBCO at higher field would be significantly more expensive).
+- **Li-6 enrichment at commercial scale**: Current global production is modest (ITER requirement); Stellaris WCLL with TBR 1.074 implies reliance on Li-6 enrichment for startup and net positive tritium production.
 
 **Gaps**:
-- 3D non-planar HTS coil manufacturing supply chain — `not-yet-sourced` (some literature on REBCO tape production forecasts exists; ARPA-E reports on HTS manufacturing) — **important**
-- REBCO cost trajectory at GW-scale deployment — `not-yet-sourced` — **important**
-- 240 GHz gyrotron supply chain — `truly-unknown` at MW scale — **important**
+- REBCO tape quantity and cost-per-kA-m at commercial scale — not-yet-sourced — **important**
+- Industrial supply chain for complex 3D REBCO stellarator coils — not-yet-sourced — **important**
+- Li-6 enrichment supply at commercial scale — not-yet-sourced — **nice-to-have**
+- Tritium startup inventory cost (~1–2 kg per the Helios analog; ~$30–130M at current prices) — not-yet-sourced — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Peak fusion power | 2,700 MW | Stellaris paper (Table 2) | h |
-| Total thermal power | ~3,100–3,300 MW | Stellaris paper | h |
-| Net electric output | ~1,000 MW | Stellaris paper (Table 2) | h |
-| Net-to-thermal efficiency (implied) | ~32% | Derived: 1000/3150 | m |
-| ECRH startup power | 50 MW | Stellaris paper (Table 2) | h |
-| ECRH ignited power | ~1 MW (inferred) | Inferred from Helios analog (1 MW ECRH in ignited state) | m |
-| Blanket power multiplier | 1.2 | Stellaris paper (neutronics) | h |
-| TBR (WCLL) | 1.07 | Stellaris paper (neutronics) | h |
-| Magnet lifetime | ~10 FPY (neutron fluence) | Stellaris paper (shielding section) | m |
-| First wall avg DPA rate | 6 DPA/FPY | Stellaris paper | h |
-| Maintenance strategy | Sector splitting | Stellaris paper | h |
-| First wall replacement interval | 4–6 years | Stellaris paper (Section 3.1) | m |
-| Fuel type | D-T | Dossier | h |
-| Thermal conversion (Helios analog) | ~40% gross Rankine | Helios paper | m |
-| Capacity factor (Helios analog) | ~88% (84-day outage/2yr) | Helios paper | m |
-| Overnight capital range (fleet-wide) | 1–10 $/W | Stellaris paper intro (refs [10-13]) | l |
-| LCOE range (fleet-wide D-T MFE) | $140–550/MWh (FOAK) | `tea_dt_mfe_cost_analysis/` | l |
-| Alpha demo cost | ~EUR 2B | Proxima MoU press release | h |
+| Fusion power (peak) | 2700 MW | Stellaris paper, Table 1 | High |
+| Thermal power (blanket output) | ~3100–3300 MW (power mult 1.2) | Stellaris paper, §2.8 | High |
+| Net electric power | ~1000 MW | Stellaris paper, Table 1 | Medium |
+| Overall plant efficiency | ~32% | Derived: 1000 MWe / 3150 MWth | Medium |
+| Thermal efficiency (Rankine analog) | ~40% | Helios analog (helios-stellarator-comparison.md, Table 1) | Medium |
+| Fusion gain Q (implied) | ~36 at Point A (2700 MW / 75 MW input) | Stellaris paper, §2.3 operating points | Medium |
+| ECRH auxiliary power | 50 MW | Stellaris paper, §2.5 | High |
+| Operation mode | Steady-state, 24/7 | Intrinsic stellarator property; confirmed by Proxima | High |
+| TBR | 1.074 | Stellaris paper, §2.8, 3D OpenMC simulation | High |
+| First wall lifetime | ~4–5 FPY | Stellaris paper, §2.8, ARC-DPA model | Medium |
+| Coil lifetime | ~10 FPY at 2700 MW | Stellaris paper, §2.9, 3×10²² m⁻² fluence limit | Medium |
+| Maintenance strategy | Sector splitting, 4–5 year operating cycles | Stellaris paper, §2.11 | Medium |
+| Availability target | ~90% over 4.5-year cycle | Stellaris paper, §2.11 | Low (target, not confirmed) |
+| Maintenance downtime estimate | ~7 months (target: 5 months) | Stellaris paper, §2.11 | Low |
+| Capacity factor (analog) | 88% | Helios (biennial 84-day maintenance; helios-stellarator-comparison.md) | Medium |
+| Generic MFE overnight cost | 1–10 $/W | Cited in Stellaris paper from refs [10–13] | Low (too wide) |
+| Generic MFE LCOE | 20–100 $/MWh | Cited in Stellaris paper from refs [14–15] | Low (too wide) |
+| Compact fusion LCOE (analog) | 34–54 $/MWh avg ~43 $/MWh | ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) CapEx ~$2.4/W | Medium (different concept family) |
+| D-T MFE LCOE range (tokamak analog) | $140–550/MWh; OCC $8800–22,200/kW | TEA MIT (`knowledge/sources/tea_dt_mfe_cost_analysis/`) for 350 MWe ARC | Low (tokamak, conservative regulatory assumptions) |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (coils, blanket, vessel, BOP) | proprietary / not-yet-published | blocking | Stellaris paper explicitly defers; ARIES-CS analogue (not fully ingested) could partially fill |
-| O&M cost (annual) | not-yet-sourced | blocking | No fusion stellarator O&M data available publicly for this class |
-| Cryogenic recirculating power | derivable (with caution) | blocking | Table lists 111 MW to coils but unit/value uncertain; Helios uses ~10 MW for 40 kW at 20K |
-| Capacity factor (Stellaris-specific) | derivable | important | Use Helios 88% as analog; Stellaris cites longer replacement intervals (4-6 yr vs 2 yr for Helios) → possibly higher CF |
-| Blanket/first wall replacement cost | not-yet-sourced | important | Major O&M driver for high-neutron-flux stellarators |
-| Magnet replacement cost (if 10 FPY lifetime) | not-yet-sourced | important | Potentially dominant lifecycle cost |
-| ECRH system capital cost at 240 GHz | not-yet-sourced | important | Novel frequency; no commercial precedent |
-| Confinement enhancement factor risk | derivable | important | H=1.4 assumed (achieved in W7-X); uncertainty propagates to fusion power |
-| Scaling to lower aspect ratio (economic optimum) | not-yet-sourced | nice-to-have | Paper mentions lower AR reduces capital cost but reduces power |
+| Capital cost by subsystem (magnets, blanket, BOP, structures) | proprietary | blocking | No Stellaris-specific estimate; Proxima explicitly defers economic analysis; 3D coil set has no cost analog |
+| 3D HTS stellarator coil cost | not-yet-sourced | blocking | 50 non-planar REBCO coils ~25 m circumference each; no published $/kA-m at this complexity; planar Helios coils are structurally different |
+| O&M costs (annual) | not-yet-sourced | important | Remote maintenance of 3D geometry with activated components; no stellarator-specific O&M study found; standard D-T MFE analog 1–2% capital/year |
+| Achievable capacity factor | derivable | important | 90% target plausible (Helios 88% analog); but 7-month maintenance estimate exceeds 5-month target; Stellaris operates on 4-year first wall cycles, 10-year coil cycles |
+| Steam Rankine cycle specification | derivable | important | WCLL water coolant at <500°C strongly implies Rankine; ~32% overall plant efficiency in Stellaris; Helios confirms 40% thermal efficiency for similar stellarator |
+| First wall/blanket replacement cost | not-yet-sourced | important | ~4-5 FPY replacement intervals; major activated component handling; no per-cycle cost estimate |
+| ECRH system capital cost | not-yet-sourced | important | 56 gyrotrons at 240 GHz (~1 MW each); ITER gyrotrons at 170 GHz ~$10M/unit; 240 GHz not yet demonstrated commercially |
+| Fuel cost (D and Li-6) | derivable | nice-to-have | Deuterium negligible; Li-6 for blanket and tritium startup well-characterized in ITER literature |
+| Decommissioning cost | derivable | nice-to-have | Standard nuclear decommissioning methodology applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **ARIES-CS full papers** (Lyon et al. 2008, FST Vol. 54, OSTI:1014258 — abstract only captured): These contain the most directly applicable stellarator cost breakdown — same compact stellarator class, using ARIES CAS costing. Search OSTI or FST archives. — `not-yet-sourced`, **high priority**
-
-2. **HELIAS reactor study series** (cited as refs [55–60] in Stellaris paper): EUROfusion's HTS stellarator reactor studies. May contain cost estimates from 2010s that can be updated. Search ARIES/EUROfusion document archives. — `not-yet-sourced`, **high priority**
-
-3. **Proxima conference presentations** (APS-DPP 2024-2025, IAEA FEC 2024): Companies sometimes present pre-commercial cost estimates at conferences before formal publication. Search APS-DPP abstract database and IAEA INIS. — `not-yet-sourced`, **medium priority** — *unverified — confirm existence before searching*
-
-4. **PyFECONS** (`/home/reid/PyFECONS`): Contains ARIES-CS costing algorithms implementable for compact stellarators. Can be used to derive capital cost analogues by parameterizing with Stellaris dimensions. — `derivable`, **high utility**
-
-5. **REBCO tape cost forecasts**: ARPA-E funded studies on HTS manufacturing cost trajectories. Search OSTI for "REBCO manufacturing cost" or "HTS tape cost reduction roadmap." — `not-yet-sourced` — *unverified — confirm existence before searching*
-
-6. **Revisit of ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): While targeting MIF and other concepts rather than stellarators, the costing methodology (CAS-based, 500 MWe plants) is directly applicable as a cross-concept methodology anchor. Fleet-wide source already registered — **check for stellarator-applicable parameters**.
+- **Stellaris economic study** (future Proxima publication): The Stellaris paper explicitly identifies this as future work. Search OSTI, FED, and arXiv for Proxima Fusion techno-economic analysis (2025–2026). _Search terms: "Stellaris" AND "cost" OR "LCOE" OR "economic" on Google Scholar/OSTI._ Flag as `unverified — confirm existence before searching`.
+- **ARIES-CS full economic study** (Najmabadi et al., Fusion Science and Technology, 2008): The ARIES-CS compact stellarator study contains a detailed CAS-level cost breakdown for a QA stellarator with LTS coils; applicable as cost structure analog even though magnets differ. OSTI ID 1014258 is the systems study abstract; full paper at FST Vol. 54, No. 3 (2008). _not-yet-sourced_.
+- **HTS coil cost studies from SPARC/CFS or Commonwealth Fusion Systems**: Published analyses of REBCO tape quantities, coil manufacturing costs, and $/kA-m scaling for high-field HTS coils. _not-yet-sourced — search PSFC, CFS reports, and FED for ARC magnet costing_.
+- **Alpha demo specifications** (to emerge 2026–2031): Proxima will publish Alpha detailed design specifications as milestones approach. These will provide the first physics-validated cost anchor for the Stellaris program.
+- **EU DEMO WCLL blanket economic analysis**: Full cost breakdown of the WCLL breeding blanket design from the EUROfusion DEMO project. Applicable to Stellaris's WCLL concept. _not-yet-sourced — search EUROfusion DEMO documentation portal_.
+- **240 GHz gyrotron development program**: KIT/IPP gyrotron development for ITER/DEMO frequency extension. Search IEE Transactions on Plasma Science and KIT publications for 240 GHz progress. _not-yet-sourced_.
+
+**Fleet-wide sources assessed and disqualified**:
+- **PyFECONS** (`/home/reid/PyFECONS`): Codebase that implements ARIES-style fusion costing algorithms. Without Stellaris-specific input parameters (coil geometry, blanket dimensions, support structure mass), running the code would return generic MFE estimates no more informative than the ARIES Cost Account Documentation (`knowledge/sources/aries_cost_account_documentation/`) already provides. The methodology is covered; the input data is what's missing. Disqualified.
+- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Hawker et al. IFE Monte Carlo model (laser/target-driven). Not applicable to MFE stellarator. Disqualified.
+- **Economic studies for heavy-ion-fusion electric power plants** (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`): HIF driver economics for linear accelerator + target factory architecture. Not applicable to stellarator. Disqualified.
+- **Energy from Inertial Fusion** (`knowledge/sources/energy_from_inertial_fusion/`): 1992 IFE concept review. Not applicable. Disqualified.
+- **Accelerators for IFE production** (`knowledge/sources/accelerators_for_inertial_fusion_energy_production/`): IFE driver technology. Not applicable. Disqualified.
+- **Affordable, manageable, practical, and scalable (AMPS)** (`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`): Pacific Fusion high-yield pulser IFE system. Not applicable. Disqualified.
+- **Commercialization of laser fusion energy** (`knowledge/sources/commercialization_of_laser_fusion_energy/`): Xcimer KrF excimer laser IFE. Not applicable. Disqualified.
+- **An Assessment of the Economics of Future Electric Power Generation Options** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Historical ORNL benchmarking study. The MIT TEA paper (`knowledge/sources/tea_dt_mfe_cost_analysis/`) provides more recent and applicable D-T MFE LCOE ranges; this historical baseline adds no concept-specific content for Stellaris. Disqualified.
+- **Progress toward fusion energy breakeven** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Wurzel & Hsu (2021) Lawson parameter compilation. The Stellaris paper itself cites W7-X's peak triple product (5.1×10¹⁹ keV·s/m³ from W7-X, vs. 12.4×10²¹ for Stellaris target), establishing that two orders of magnitude of progress are required in triple product — this physics gap is already documented in the dossier. The Wurzel & Hsu compilation adds no new Stellaris-specific data. Disqualified.
 
 ---
 
 ## Summary
 
-Proceed to full analysis with the following posture: the physics and engineering basis is **strong enough to support D1+ qualitative analysis** and a **preliminary quantitative LCOE model using analogues and ranges**. The Stellaris paper provides fusion power, thermal power, net electric output, TBR, magnet lifetime, and first wall DPA rates. The Helios paper (Thea Energy) supplies the most direct stellarator plant economics analog: 40% Rankine efficiency, 88% capacity factor, power balance Sankey, cryogenic loads. The TEA D-T MFE source provides the LCOE methodology and early-plant range ($140–550/MWh).
-
-**The analysis should not attempt to produce a single LCOE number without wide uncertainty bounds.** The most productive approach is a parametric model with capital cost and O&M as free parameters swept over fusion-literature ranges, sensitivity-tested against capacity factor and magnet lifetime. The $0.01/kWh back-solve will reveal that this concept is not close under any credible parameter set — identifying which costs must fall and by how much is the analytically useful output.
-
-**Before acquiring additional sources**, ingest the ARIES-CS full text (Lyon et al. 2008, FST) and check PyFECONS for stellarator costing algorithms — these are the two highest-leverage actions.
+**Proceed to full analysis.** The Stellaris concept has exceptional source coverage for physics and engineering relative to its development stage, justifying a high-quality D1+ qualitative analysis now. The quantitative LCOE model should be built on an explicit analog basis: Helios stellarator (390 MWe, 88% CF, 40% thermal efficiency, steam Rankine) for plant-level parameters; ARPA-E ALPHA revisit (~$34–54/MWh range) and ARIES cost account framework as the lower and methodological bounds; and MIT TEA D-T MFE ($140–550/MWh, $8800–22,200/kW) as the upper bound for a heavily regulated FOAK scenario. The single blocking gap — no concept-specific capital cost model — should be explicitly flagged in the analysis: the LCOE estimate will be analog-derived with ±50% uncertainty until Proxima publishes economic analysis or the Alpha demo provides cost anchors. The back-solve to $0.01/kWh should highlight 3D HTS coil cost as the dominant uncertainty driver, with Stellaris's ~1 GWe scale and steady-state operation as its strongest economic advantages over tokamak competitors.
 
 ---
 
@@ -178,12 +181,12 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 3
+blocking_count: 2
 important_count: 8
-counting_method: "section_5_missing_parameters (blocking: capital cost breakdown, O&M cost, cryogenic recirculating power) plus cross-section important gaps (divertor scalability, ECRH at 240 GHz, magnet replacement cost, blanket replacement cost, REBCO supply chain, CF derivable-only, confinement H-factor risk)"
+counting_method: "all_sections_deduplicated — §1/§5 share one blocking gap (no concept-specific capital cost model); 3D HTS coil cost counted separately as second blocking (structurally distinct from generic capital cost, no analog); 8 important gaps deduplicated across §2-§5"
 section_coverage:
-  availability_of_data:       "Partial"
-  system_function:            "Partial"
+  availability_of_data:       "Moderate"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
```
